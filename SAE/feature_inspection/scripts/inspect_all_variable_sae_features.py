#!/usr/bin/env python3

import argparse
import heapq
import json
from pathlib import Path

import pandas as pd
import torch
from safetensors.torch import load_file
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


def load_jsonl(path):

    with path.open(
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if line:
                yield json.loads(
                    line
                )


def add_to_heap(
    heap,
    activation,
    counter,
    item,
    k,
):

    record = (
        float(activation),
        counter,
        item,
    )

    if len(heap) < k:

        heapq.heappush(
            heap,
            record,
        )

    elif activation > heap[0][0]:

        heapq.heapreplace(
            heap,
            record,
        )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--selection-csv",
        default=(
            "artifacts/"
            "linguistic_feature_eval/"
            "inspection/"
            "all_variables/"
            "all_variable_candidate_selection.csv"
        ),
    )

    parser.add_argument(
        "--natural-corpus",
        default=(
            "data/"
            "inspection_corpus/"
            "sae_train_150k_v1_2_final.jsonl"
        ),
    )

    parser.add_argument(
        "--sae-dir",
        default=(
            "artifacts/"
            "sae_canonical/"
            "xglm564m_hidden12_batchtopk16x_k256"
        ),
    )

    parser.add_argument(
        "--output-dir",
        default=(
            "artifacts/"
            "linguistic_feature_eval/"
            "inspection/"
            "all_variables"
        ),
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=20,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=192,
    )

    args = parser.parse_args()

    selection_path = Path(
        args.selection_csv
    )

    corpus_path = Path(
        args.natural_corpus
    )

    sae_dir = Path(
        args.sae_dir
    )

    output_dir = Path(
        args.output_dir
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    if not corpus_path.is_file():

        raise FileNotFoundError(
            corpus_path
        )


    selection = pd.read_csv(
        selection_path
    )

    if len(selection) != 200:

        raise RuntimeError(
            f"Expected 200 candidate rows, "
            f"found {len(selection)}"
        )


    feature_ids = sorted(
        selection[
            "feature_id"
        ]
        .astype(int)
        .unique()
        .tolist()
    )


    # A feature may be selected for more
    # than one linguistic variable.
    feature_targets = {}

    for _, r in selection.iterrows():

        fid = int(
            r["feature_id"]
        )

        feature_targets.setdefault(
            fid,
            [],
        ).append(
            {
                "variable_id":
                    int(
                        r[
                            "variable_id"
                        ]
                    ),

                "variable":
                    r["variable"],

                "selection_slot":
                    int(
                        r[
                            "selection_slot"
                        ]
                    ),

                "selection_basis":
                    r[
                        "selection_basis"
                    ],

                "train_effect":
                    float(
                        r[
                            "train_effect"
                        ]
                    ),

                "val_effect":
                    float(
                        r[
                            "val_effect"
                        ]
                    ),

                "specificity_rank":
                    int(
                        r[
                            "specificity_rank"
                        ]
                    ),

                "specificity_ratio":
                    float(
                        r[
                            "specificity_ratio"
                        ]
                    ),
            }
        )


    config = json.loads(
        (
            sae_dir
            / "sae_inference_config.json"
        ).read_text(
            encoding="utf-8"
        )
    )


    weights_path = (
        sae_dir
        / "sae_inference.safetensors"
    )

    if not weights_path.is_file():

        raise FileNotFoundError(
            weights_path
        )


    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    if device.type != "cuda":

        raise RuntimeError(
            "CUDA required."
        )


    print(
        "Selected candidate-variable pairs:",
        len(selection),
    )

    print(
        "Unique SAE features:",
        len(feature_ids),
    )


    print(
        "Loading tokenizer..."
    )

    tokenizer = (
        AutoTokenizer
        .from_pretrained(
            config["model"],
            use_fast=False,
        )
    )

    tokenizer.padding_side = (
        "right"
    )

    if tokenizer.pad_token_id is None:

        tokenizer.pad_token = (
            tokenizer.eos_token
        )


    print(
        "Loading XGLM..."
    )

    model = (
        AutoModelForCausalLM
        .from_pretrained(
            config["model"],
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        )
    )

    model.to(
        device
    )

    model.eval()


    print(
        "Loading canonical SAE..."
    )

    sd = load_file(
        str(
            weights_path
        ),
        device=str(
            device
        ),
    )


    feature_index = torch.tensor(
        feature_ids,
        dtype=torch.long,
        device=device,
    )


    W_enc = (
        sd["W_enc"][
            :,
            feature_index,
        ]
        .float()
    )

    b_enc = (
        sd["b_enc"][
            feature_index
        ]
        .float()
    )

    threshold = (
        sd["threshold"][
            feature_index
        ]
        .float()
    )

    b_dec = (
        sd["b_dec"]
        .float()
    )


    activation_scale = float(
        config[
            "activation_scale"
        ]
    )

    hidden_state_index = int(
        config[
            "hidden_state_index"
        ]
    )


    heaps = {
        fid: []
        for fid in feature_ids
    }

    counters = {
        fid: 0
        for fid in feature_ids
    }


    total_rows = 0
    possible_truncations = 0


    def process_batch(
        rows
    ):

        nonlocal possible_truncations


        texts = [
            str(
                r["text"]
            )
            for r in rows
        ]


        enc = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=args.max_length,
            add_special_tokens=False,
            return_tensors="pt",
        )


        input_ids = (
            enc[
                "input_ids"
            ]
            .to(
                device
            )
        )

        attention_mask = (
            enc[
                "attention_mask"
            ]
            .to(
                device
            )
        )


        lengths = (
            attention_mask
            .sum(
                dim=1
            )
        )

        possible_truncations += int(
            (
                lengths
                >= args.max_length
            )
            .sum()
            .item()
        )


        with torch.inference_mode():

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_hidden_states=True,
                use_cache=False,
                return_dict=True,
            )


            hidden = (
                outputs
                .hidden_states[
                    hidden_state_index
                ]
                .float()
            )


            x_scaled = (
                hidden
                * activation_scale
            )


            pre = (
                (
                    x_scaled
                    - b_dec
                )
                @ W_enc
                + b_enc
            )


            raw = torch.relu(
                pre
            )


            acts = torch.where(
                raw
                > threshold,
                raw,
                torch.zeros_like(
                    raw
                ),
            )


            acts = (
                acts
                .masked_fill(
                    ~attention_mask
                    .bool()
                    .unsqueeze(
                        -1
                    ),
                    0.0,
                )
            )


            sentence_max, token_pos = (
                acts.max(
                    dim=1
                )
            )


        sentence_max = (
            sentence_max
            .cpu()
        )

        token_pos = (
            token_pos
            .cpu()
        )

        input_ids_cpu = (
            input_ids
            .cpu()
        )


        for feature_col, fid in enumerate(
            feature_ids
        ):

            values = (
                sentence_max[
                    :,
                    feature_col,
                ]
            )

            positions = (
                token_pos[
                    :,
                    feature_col,
                ]
            )


            for i, row in enumerate(
                rows
            ):

                activation = float(
                    values[
                        i
                    ].item()
                )

                if activation <= 0:
                    continue


                pos = int(
                    positions[
                        i
                    ].item()
                )


                token_id = int(
                    input_ids_cpu[
                        i,
                        pos,
                    ].item()
                )


                token = (
                    tokenizer
                    .convert_ids_to_tokens(
                        token_id
                    )
                )


                metadata = {
                    k: v
                    for k, v
                    in row.items()
                    if k != "text"
                }


                item = {
                    "feature_id":
                        fid,

                    "activation":
                        activation,

                    "token_position":
                        pos,

                    "token":
                        token,

                    "text":
                        str(
                            row[
                                "text"
                            ]
                        ),

                    "metadata":
                        metadata,
                }


                counters[
                    fid
                ] += 1


                add_to_heap(
                    heaps[
                        fid
                    ],
                    activation,
                    counters[
                        fid
                    ],
                    item,
                    args.top_k,
                )


    batch = []


    for row in tqdm(
        load_jsonl(
            corpus_path
        ),
        desc="Natural corpus",
        unit="row",
    ):

        if "text" not in row:

            raise RuntimeError(
                "Natural corpus row "
                "missing 'text'."
            )


        batch.append(
            row
        )

        total_rows += 1


        if len(batch) >= args.batch_size:

            process_batch(
                batch
            )

            batch = []


    if batch:

        process_batch(
            batch
        )


    output_jsonl = (
        output_dir
        / "all_variable_natural_top_activations.jsonl"
    )


    summary_rows = []


    with output_jsonl.open(
        "w",
        encoding="utf-8",
    ) as f:


        for fid in feature_ids:


            examples = [
                x[2]
                for x in sorted(
                    heaps[
                        fid
                    ],
                    key=lambda z:
                        z[0],
                    reverse=True,
                )
            ]


            record = {
                "feature_id":
                    fid,

                "targets":
                    feature_targets[
                        fid
                    ],

                "examples":
                    examples,
            }


            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )


            tokens = [
                x["token"]
                for x in examples
            ]


            languages = [
                str(
                    x[
                        "metadata"
                    ].get(
                        "language",
                        "",
                    )
                )
                for x in examples
            ]


            for target in (
                feature_targets[
                    fid
                ]
            ):


                summary_rows.append(
                    {
                        **target,

                        "feature_id":
                            fid,

                        "top_examples":
                            len(
                                examples
                            ),

                        "unique_top_tokens":
                            len(
                                set(
                                    tokens
                                )
                            ),

                        "unique_languages":
                            len(
                                {
                                    x
                                    for x
                                    in languages
                                    if x
                                }
                            ),
                    }
                )


    summary = pd.DataFrame(
        summary_rows
    )


    summary_path = (
        output_dir
        / "all_variable_inspection_summary.csv"
    )


    summary.to_csv(
        summary_path,
        index=False,
    )


    manifest = {
        "purpose":
            (
                "Broad natural-text inspection "
                "of five SAE candidates for "
                "every controlled linguistic "
                "variable."
            ),

        "variables":
            40,

        "candidate_variable_pairs":
            len(selection),

        "unique_sae_features":
            len(feature_ids),

        "candidate_selection_used_test":
            False,

        "interpretation_policy":
            (
                "Candidates are not automatically "
                "rejected for small test, "
                "specificity, or subgroup failures. "
                "Natural interpretability and the "
                "full evidence profile are reviewed "
                "jointly before causal selection."
            ),

        "natural_rows":
            total_rows,

        "possible_truncations":
            possible_truncations,

        "top_k":
            args.top_k,

        "model":
            config[
                "model"
            ],

        "hidden_state_index":
            hidden_state_index,

        "activation_scale":
            activation_scale,

        "outputs": {
            "activations":
                str(
                    output_jsonl
                ),

            "summary":
                str(
                    summary_path
                ),
        },
    }


    (
        output_dir
        / "all_variable_inspection_manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


    print()
    print(
        "ALL-VARIABLE FEATURE INSPECTION COMPLETE"
    )

    print(
        "========================================"
    )

    print(
        "Natural rows:",
        total_rows,
    )

    print(
        "Candidate-variable pairs:",
        len(selection),
    )

    print(
        "Unique features:",
        len(feature_ids),
    )

    print(
        "Possible truncations:",
        possible_truncations,
    )

    print(
        "Saved:",
        output_jsonl,
    )

    print(
        "Saved:",
        summary_path,
    )


if __name__ == "__main__":
    main()
