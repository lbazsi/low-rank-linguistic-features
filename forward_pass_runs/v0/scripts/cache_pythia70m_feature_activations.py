# scripts/cache_pythia70m_feature_activations.py

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "EleutherAI/pythia-70m-deduped"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def parse_torch_dtype(dtype_name: str) -> torch.dtype:
    mapping = {
        "float32": torch.float32,
        "fp32": torch.float32,
        "float16": torch.float16,
        "fp16": torch.float16,
        "bfloat16": torch.bfloat16,
        "bf16": torch.bfloat16,
    }

    if dtype_name not in mapping:
        raise ValueError(f"Unsupported dtype: {dtype_name}")

    return mapping[dtype_name]


def choose_device(requested_device: str) -> torch.device:
    if requested_device != "auto":
        return torch.device(requested_device)

    if torch.cuda.is_available():
        return torch.device("cuda")

    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def choose_compute_dtype(device: torch.device, requested_dtype: str) -> torch.dtype:
    if requested_dtype != "auto":
        return parse_torch_dtype(requested_dtype)

    if device.type == "cuda":
        return torch.float16

    # CPU/MPS are safer in fp32 for this small model.
    return torch.float32


def normalize_feature_inputs(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = {
        "sentence_id",
        "pair_id",
        "variable_id",
        "variable",
        "approach",
        "language",
        "surface_type",
        "contrast",
        "split",
        "type",
        "sentence",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Input parquet is missing columns: {sorted(missing)}")

    valid_types = {"basis", "changed"}
    observed_types = set(df["type"].unique())

    if not observed_types.issubset(valid_types):
        raise ValueError(f"Unexpected values in 'type': {sorted(observed_types)}")

    df = df.copy()

    type_order = {"basis": 0, "changed": 1}
    df["_type_order"] = df["type"].map(type_order)

    # Stable ordering is important because tensor row i must match metadata row i.
    df = df.sort_values(
        by=["variable_id", "pair_id", "_type_order"],
        kind="stable",
    ).drop(columns=["_type_order"])

    df = df.reset_index(drop=True)
    df.insert(0, "sentence_row_idx", np.arange(len(df), dtype=np.int64))

    duplicates = df[df["sentence_id"].duplicated(keep=False)]

    if not duplicates.empty:
        examples = duplicates["sentence_id"].head(20).tolist()
        raise ValueError(f"Duplicate sentence_id values found, e.g. {examples}")

    return df


def build_pair_metadata(sentence_df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    grouped = sentence_df.groupby("pair_id", sort=False)

    for pair_idx, (pair_id, group) in enumerate(grouped):
        types = set(group["type"].tolist())

        if types != {"basis", "changed"}:
            raise ValueError(
                f"pair_id={pair_id} must contain exactly one basis and one changed row; "
                f"found {sorted(types)}"
            )

        if len(group) != 2:
            raise ValueError(f"pair_id={pair_id} has {len(group)} rows, expected 2")

        basis_row = group[group["type"] == "basis"].iloc[0]
        changed_row = group[group["type"] == "changed"].iloc[0]

        shared_fields = [
            "pair_id",
            "variable_id",
            "variable",
            "approach",
            "language",
            "surface_type",
            "contrast",
            "split",
            "source_file",
            "source_line",
        ]

        row = {
            "pair_row_idx": pair_idx,
            "pair_id": pair_id,
            "basis_sentence_row_idx": int(basis_row["sentence_row_idx"]),
            "changed_sentence_row_idx": int(changed_row["sentence_row_idx"]),
            "basis_sentence_id": basis_row["sentence_id"],
            "changed_sentence_id": changed_row["sentence_id"],
        }

        for field in shared_fields:
            if field in sentence_df.columns and field not in row:
                row[field] = basis_row[field]

        rows.append(row)

    pair_df = pd.DataFrame(rows)

    if pair_df.empty:
        raise ValueError("No pairs found.")

    return pair_df


def get_layer_hidden_states(
    hidden_states: tuple[torch.Tensor, ...],
    include_embedding_layer: bool,
) -> list[torch.Tensor]:
    """
    Hugging Face returns hidden_states as:

        hidden_states[0] = embedding output
        hidden_states[1:] = residual stream after each transformer block

    For the first pass, default to transformer block outputs only.
    """
    if include_embedding_layer:
        return list(hidden_states)

    return list(hidden_states[1:])


def pool_hidden_states(
    layer_hidden_states: list[torch.Tensor],
    attention_mask: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Returns:

        final_token_batch: [batch, num_layers, hidden_dim]
        mean_pooled_batch: [batch, num_layers, hidden_dim]
    """
    lengths = attention_mask.sum(dim=1)
    final_positions = lengths - 1

    batch_size = attention_mask.shape[0]
    batch_indices = torch.arange(batch_size, device=attention_mask.device)

    mask = attention_mask.unsqueeze(-1).to(dtype=layer_hidden_states[0].dtype)
    denom = lengths.clamp_min(1).unsqueeze(-1).to(dtype=layer_hidden_states[0].dtype)

    final_per_layer = []
    mean_per_layer = []

    for h in layer_hidden_states:
        # h shape: [batch, seq_len, hidden_dim]
        final_h = h[batch_indices, final_positions, :]
        mean_h = (h * mask).sum(dim=1) / denom

        final_per_layer.append(final_h)
        mean_per_layer.append(mean_h)

    final_token_batch = torch.stack(final_per_layer, dim=1)
    mean_pooled_batch = torch.stack(mean_per_layer, dim=1)

    return final_token_batch, mean_pooled_batch


def run_forward_passes(
    sentence_df: pd.DataFrame,
    model_name: str,
    batch_size: int,
    max_length: int,
    device: torch.device,
    compute_dtype: torch.dtype,
    storage_dtype: torch.dtype,
    include_embedding_layer: bool,
) -> tuple[torch.Tensor, torch.Tensor, list[str]]:
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_kwargs = {}

    if device.type == "cuda":
        model_kwargs["torch_dtype"] = compute_dtype

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        **model_kwargs,
    )

    model.eval()
    model.to(device)

    sentences = sentence_df["sentence"].astype(str).tolist()
    num_sentences = len(sentences)

    # One tiny dry run to discover num_layers and hidden_dim.
    dry_batch = tokenizer(
        sentences[: min(2, num_sentences)],
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length,
    )

    dry_batch = {k: v.to(device) for k, v in dry_batch.items()}

    with torch.inference_mode():
        dry_outputs = model(
            **dry_batch,
            output_hidden_states=True,
            use_cache=False,
        )

    dry_layers = get_layer_hidden_states(
        dry_outputs.hidden_states,
        include_embedding_layer=include_embedding_layer,
    )

    num_layers = len(dry_layers)
    hidden_dim = dry_layers[0].shape[-1]

    if include_embedding_layer:
        layer_names = ["embedding"] + [f"layer_{i}" for i in range(num_layers - 1)]
    else:
        layer_names = [f"layer_{i}" for i in range(num_layers)]

    print(f"Model: {model_name}")
    print(f"Device: {device}")
    print(f"Compute dtype: {compute_dtype}")
    print(f"Storage dtype: {storage_dtype}")
    print(f"Sentences: {num_sentences:,}")
    print(f"Layers cached: {num_layers}")
    print(f"Hidden dim: {hidden_dim}")
    print(f"Batch size: {batch_size}")
    print(f"Max length: {max_length}")

    final_token = torch.empty(
        size=(num_sentences, num_layers, hidden_dim),
        dtype=storage_dtype,
        device="cpu",
    )

    mean_pooled = torch.empty(
        size=(num_sentences, num_layers, hidden_dim),
        dtype=storage_dtype,
        device="cpu",
    )

    for start in tqdm(range(0, num_sentences, batch_size), desc="Forward passes"):
        end = min(start + batch_size, num_sentences)
        batch_sentences = sentences[start:end]

        encoded = tokenizer(
            batch_sentences,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        )

        encoded = {k: v.to(device) for k, v in encoded.items()}

        with torch.inference_mode():
            outputs = model(
                **encoded,
                output_hidden_states=True,
                use_cache=False,
            )

        layer_hidden_states = get_layer_hidden_states(
            outputs.hidden_states,
            include_embedding_layer=include_embedding_layer,
        )

        batch_final, batch_mean = pool_hidden_states(
            layer_hidden_states=layer_hidden_states,
            attention_mask=encoded["attention_mask"],
        )

        final_token[start:end] = batch_final.detach().to("cpu", dtype=storage_dtype)
        mean_pooled[start:end] = batch_mean.detach().to("cpu", dtype=storage_dtype)

    return final_token, mean_pooled, layer_names


def compute_pair_deltas(
    final_token: torch.Tensor,
    mean_pooled: torch.Tensor,
    pair_df: pd.DataFrame,
    storage_dtype: torch.dtype,
) -> tuple[torch.Tensor, torch.Tensor]:
    basis_indices = torch.tensor(
        pair_df["basis_sentence_row_idx"].to_numpy(),
        dtype=torch.long,
    )

    changed_indices = torch.tensor(
        pair_df["changed_sentence_row_idx"].to_numpy(),
        dtype=torch.long,
    )

    # Compute in fp32 for cleaner deltas, then store compactly.
    delta_final_token = (
        final_token[changed_indices].float() - final_token[basis_indices].float()
    ).to(dtype=storage_dtype)

    delta_mean_pooled = (
        mean_pooled[changed_indices].float() - mean_pooled[basis_indices].float()
    ).to(dtype=storage_dtype)

    return delta_final_token, delta_mean_pooled


def save_activation_cache(
    output_dir: Path,
    model_name: str,
    final_token: torch.Tensor,
    mean_pooled: torch.Tensor,
    delta_final_token: torch.Tensor,
    delta_mean_pooled: torch.Tensor,
    sentence_df: pd.DataFrame,
    pair_df: pd.DataFrame,
    layer_names: list[str],
    args: argparse.Namespace,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    activation_path = output_dir / "pythia70m_feature_activations.pt"
    sentence_metadata_path = output_dir / "sentence_metadata.parquet"
    pair_metadata_path = output_dir / "pair_metadata.parquet"
    manifest_path = output_dir / "manifest.json"

    sentence_df.to_parquet(sentence_metadata_path, index=False)
    pair_df.to_parquet(pair_metadata_path, index=False)

    torch.save(
        {
            "model_name": model_name,
            "layer_names": layer_names,
            "final_token": final_token,
            "mean_pooled": mean_pooled,
            "delta_final_token": delta_final_token,
            "delta_mean_pooled": delta_mean_pooled,
            "notes": {
                "final_token": "[num_sentences, num_layers, hidden_dim]",
                "mean_pooled": "[num_sentences, num_layers, hidden_dim]",
                "delta_final_token": "[num_pairs, num_layers, hidden_dim], changed - basis",
                "delta_mean_pooled": "[num_pairs, num_layers, hidden_dim], changed - basis",
                "sentence_metadata": str(sentence_metadata_path.name),
                "pair_metadata": str(pair_metadata_path.name),
            },
        },
        activation_path,
    )

    manifest = {
        "model_name": model_name,
        "activation_file": activation_path.name,
        "sentence_metadata_file": sentence_metadata_path.name,
        "pair_metadata_file": pair_metadata_path.name,
        "num_sentences": int(len(sentence_df)),
        "num_pairs": int(len(pair_df)),
        "num_layers": int(final_token.shape[1]),
        "hidden_dim": int(final_token.shape[2]),
        "final_token_shape": list(final_token.shape),
        "mean_pooled_shape": list(mean_pooled.shape),
        "delta_final_token_shape": list(delta_final_token.shape),
        "delta_mean_pooled_shape": list(delta_mean_pooled.shape),
        "layer_names": layer_names,
        "args": vars(args),
    }

    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False, default=str)

    print()
    print(f"Wrote activation cache: {activation_path}")
    print(f"Wrote sentence metadata: {sentence_metadata_path}")
    print(f"Wrote pair metadata: {pair_metadata_path}")
    print(f"Wrote manifest: {manifest_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Pythia-70M forward passes over flattened feature inputs."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path("artifacts/probe_data/feature_inputs.parquet"),
        help="Input parquet from Step 2.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/activation_cache/feature_dataset/pythia70m"),
        help="Output directory for activation cache.",
    )

    parser.add_argument(
        "--model-name",
        type=str,
        default=MODEL_NAME,
        help="Hugging Face model name.",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Forward-pass batch size.",
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=128,
        help="Maximum tokenized sentence length.",
    )

    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help="auto, cuda, cpu, mps, cuda:0, etc.",
    )

    parser.add_argument(
        "--compute-dtype",
        type=str,
        default="auto",
        choices=["auto", "float32", "fp32", "float16", "fp16", "bfloat16", "bf16"],
        help="Model compute dtype. Default: fp16 on CUDA, fp32 otherwise.",
    )

    parser.add_argument(
        "--storage-dtype",
        type=str,
        default="float16",
        choices=["float32", "fp32", "float16", "fp16", "bfloat16", "bf16"],
        help="Activation storage dtype. Use float16 to keep files compact.",
    )

    parser.add_argument(
        "--include-embedding-layer",
        action="store_true",
        help="Also cache hidden_states[0], the embedding output. Default caches transformer layer outputs only.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    args = parser.parse_args()

    set_seed(args.seed)

    if not args.input.exists():
        raise FileNotFoundError(f"Input parquet not found: {args.input}")

    device = choose_device(args.device)
    compute_dtype = choose_compute_dtype(device, args.compute_dtype)
    storage_dtype = parse_torch_dtype(args.storage_dtype)

    sentence_df = pd.read_parquet(args.input)
    sentence_df = normalize_feature_inputs(sentence_df)
    pair_df = build_pair_metadata(sentence_df)

    expected_num_rows = len(pair_df) * 2

    if len(sentence_df) != expected_num_rows:
        raise ValueError(
            f"Expected exactly 2 sentence rows per pair. "
            f"Got {len(sentence_df):,} sentence rows and {len(pair_df):,} pairs."
        )

    final_token, mean_pooled, layer_names = run_forward_passes(
        sentence_df=sentence_df,
        model_name=args.model_name,
        batch_size=args.batch_size,
        max_length=args.max_length,
        device=device,
        compute_dtype=compute_dtype,
        storage_dtype=storage_dtype,
        include_embedding_layer=args.include_embedding_layer,
    )

    delta_final_token, delta_mean_pooled = compute_pair_deltas(
        final_token=final_token,
        mean_pooled=mean_pooled,
        pair_df=pair_df,
        storage_dtype=storage_dtype,
    )

    save_activation_cache(
        output_dir=args.output_dir,
        model_name=args.model_name,
        final_token=final_token,
        mean_pooled=mean_pooled,
        delta_final_token=delta_final_token,
        delta_mean_pooled=delta_mean_pooled,
        sentence_df=sentence_df,
        pair_df=pair_df,
        layer_names=layer_names,
        args=args,
    )


if __name__ == "__main__":
    main()