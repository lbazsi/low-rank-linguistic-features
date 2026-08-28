#!/usr/bin/env python3

import argparse
import csv
import hashlib
import heapq
import json
from pathlib import Path

import numpy as np
import torch
from safetensors.torch import load_file
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(block)
    return h.hexdigest()


def read_csv(path):
    with path.open(
        encoding="utf-8-sig",
        newline="",
    ) as f:
        return list(csv.DictReader(f))


def load_jsonl(path):
    with path.open(
        encoding="utf-8",
    ) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def push_top(heap, item, k, counter):
    score = float(item["activation"])
    entry = (
        score,
        counter,
        item,
    )

    if len(heap) < k:
        heapq.heappush(
            heap,
            entry,
        )
        return

    if score > heap[0][0]:
        heapq.heapreplace(
            heap,
            entry,
        )


def heap_sorted(heap):
    return [
        item
        for _, _, item
        in sorted(
            heap,
            key=lambda x: x[0],
            reverse=True,
        )
    ]


def encode_batch(
    texts,
    tokenizer,
    model,
    selected_W,
    selected_b,
    selected_threshold,
    b_dec,
    activation_scale,
    hidden_state_index,
    max_length,
    device,
):
    encoded = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        add_special_tokens=False,
        return_tensors="pt",
    )

    input_ids = (
        encoded["input_ids"]
        .to(device)
    )

    attention_mask = (
        encoded["attention_mask"]
        .to(device)
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
            outputs.hidden_states[
                hidden_state_index
            ]
            .float()
        )

        scaled = (
            hidden
            * activation_scale
        )

        pre = (
            (scaled - b_dec)
            @ selected_W
            + selected_b
        )

        raw = torch.relu(pre)

        acts = torch.where(
            raw > selected_threshold,
            raw,
            torch.zeros_like(raw),
        )

        acts = acts.masked_fill(
            ~attention_mask.bool().unsqueeze(-1),
            0.0,
        )

        sentence_max, token_pos = (
            acts.max(dim=1)
        )

    return (
        input_ids,
        attention_mask,
        sentence_max,
        token_pos,
    )


def natural_inspection(
    corpus_path,
    top_k,
    batch_size,
    tokenizer,
    model,
    selected_features,
    selected_W,
    selected_b,
    selected_threshold,
    b_dec,
    activation_scale,
    hidden_state_index,
    max_length,
    device,
):
    heaps = {
        feature_id: []
        for feature_id
        in selected_features
    }

    counters = {
        feature_id: 0
        for feature_id
        in selected_features
    }

    rows_batch = []
    texts_batch = []

    total_rows = 0
    possible_truncations = 0

    def process_batch(
        rows_batch,
        texts_batch,
    ):
        nonlocal possible_truncations

        (
            input_ids,
            attention_mask,
            sentence_max,
            token_pos,
        ) = encode_batch(
            texts=texts_batch,
            tokenizer=tokenizer,
            model=model,
            selected_W=selected_W,
            selected_b=selected_b,
            selected_threshold=
                selected_threshold,
            b_dec=b_dec,
            activation_scale=
                activation_scale,
            hidden_state_index=
                hidden_state_index,
            max_length=max_length,
            device=device,
        )

        lengths = (
            attention_mask
            .sum(dim=1)
        )

        possible_truncations += int(
            (lengths >= max_length)
            .sum()
            .item()
        )

        sentence_max = (
            sentence_max.cpu()
        )

        token_pos = (
            token_pos.cpu()
        )

        input_ids_cpu = (
            input_ids.cpu()
        )

        for feature_col, feature_id in enumerate(
            selected_features
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

            for i in range(
                len(texts_batch)
            ):

                value = float(
                    values[i].item()
                )

                if value <= 0:
                    continue

                pos = int(
                    positions[i].item()
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

                row = rows_batch[i]

                metadata = {}

                for key in (
                    "id",
                    "language",
                    "source",
                    "corpus",
                    "length_bucket",
                ):
                    if key in row:
                        metadata[key] = row[key]

                item = {
                    "feature_id":
                        feature_id,

                    "activation":
                        value,

                    "token_position":
                        pos,

                    "token":
                        token,

                    "text":
                        texts_batch[i],

                    "metadata":
                        metadata,
                }

                counters[
                    feature_id
                ] += 1

                push_top(
                    heaps[feature_id],
                    item,
                    top_k,
                    counters[
                        feature_id
                    ],
                )

    for row in tqdm(
        load_jsonl(corpus_path),
        desc="Natural corpus",
        unit="row",
    ):
        if "text" not in row:
            raise RuntimeError(
                "Natural corpus row "
                "does not contain 'text'."
            )

        text = str(
            row["text"]
        )

        rows_batch.append(row)
        texts_batch.append(text)

        total_rows += 1

        if len(texts_batch) >= batch_size:

            process_batch(
                rows_batch,
                texts_batch,
            )

            rows_batch = []
            texts_batch = []

    if texts_batch:
        process_batch(
            rows_batch,
            texts_batch,
        )

    return {
        feature_id:
            heap_sorted(
                heaps[feature_id]
            )
        for feature_id
        in selected_features
    }, {
        "rows":
            total_rows,

        "possible_truncations":
            possible_truncations,
    }


def controlled_inspection(
    data_dir,
    top_k,
    batch_size,
    tokenizer,
    model,
    selected_features,
    selected_W,
    selected_b,
    selected_threshold,
    b_dec,
    activation_scale,
    hidden_state_index,
    max_length,
    device,
):
    heaps = {
        feature_id: []
        for feature_id
        in selected_features
    }

    counters = {
        feature_id: 0
        for feature_id
        in selected_features
    }

    examples = []

    for path in sorted(
        data_dir.glob("*.jsonl")
    ):
        for row in load_jsonl(path):

            pair = {
                item["type"]:
                    item["sentence"]
                for item in row["pair"]
            }

            for pair_type in (
                "basis",
                "changed",
            ):
                examples.append(
                    {
                        "text":
                            pair[pair_type],

                        "pair_id":
                            row["id"],

                        "pair_type":
                            pair_type,

                        "variable_id":
                            int(
                                row[
                                    "variable_id"
                                ]
                            ),

                        "variable":
                            row["variable"],

                        "split":
                            row["split"],

                        "marker_family":
                            row.get(
                                "marker_family",
                                "",
                            ),

                        "lexical_domain":
                            row.get(
                                "lexical_domain",
                                "",
                            ),

                        "language":
                            row.get(
                                "language",
                                "",
                            ),
                    }
                )

    for start in tqdm(
        range(
            0,
            len(examples),
            batch_size,
        ),
        desc="Controlled corpus",
        unit="batch",
    ):

        batch = examples[
            start:
            start + batch_size
        ]

        texts = [
            x["text"]
            for x in batch
        ]

        (
            input_ids,
            attention_mask,
            sentence_max,
            token_pos,
        ) = encode_batch(
            texts=texts,
            tokenizer=tokenizer,
            model=model,
            selected_W=selected_W,
            selected_b=selected_b,
            selected_threshold=
                selected_threshold,
            b_dec=b_dec,
            activation_scale=
                activation_scale,
            hidden_state_index=
                hidden_state_index,
            max_length=max_length,
            device=device,
        )

        sentence_max = (
            sentence_max.cpu()
        )

        token_pos = (
            token_pos.cpu()
        )

        input_ids = (
            input_ids.cpu()
        )

        for feature_col, feature_id in enumerate(
            selected_features
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

            for i, example in enumerate(
                batch
            ):

                value = float(
                    values[i].item()
                )

                if value <= 0:
                    continue

                pos = int(
                    positions[i].item()
                )

                token_id = int(
                    input_ids[
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

                item = {
                    "feature_id":
                        feature_id,

                    "activation":
                        value,

                    "token_position":
                        pos,

                    "token":
                        token,

                    **example,
                }

                counters[
                    feature_id
                ] += 1

                push_top(
                    heaps[feature_id],
                    item,
                    top_k,
                    counters[
                        feature_id
                    ],
                )

    return {
        feature_id:
            heap_sorted(
                heaps[feature_id]
            )
        for feature_id
        in selected_features
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--natural-corpus",
        default=(
            "data/inspection_corpus/"
            "sae_train_150k_v1_2_final.jsonl"
        ),
    )

    parser.add_argument(
        "--feature-data-dir",
        default="data/feature_dataset",
    )

    parser.add_argument(
        "--sae-dir",
        default=(
            "artifacts/sae_canonical/"
            "xglm564m_hidden12_batchtopk16x_k256"
        ),
    )

    parser.add_argument(
        "--evidence-csv",
        default=(
            "artifacts/"
            "linguistic_feature_eval/"
            "summary/"
            "sae_variable_evidence.csv"
        ),
    )

    parser.add_argument(
        "--output-dir",
        default=(
            "artifacts/"
            "linguistic_feature_eval/"
            "inspection"
        ),
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=50,
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

    natural_corpus = Path(
        args.natural_corpus
    )

    feature_data_dir = Path(
        args.feature_data_dir
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

    evidence = read_csv(
        Path(args.evidence_csv)
    )

    tier_a = [
        r
        for r in evidence
        if r[
            "evidence_tier"
        ] == "A"
    ]

    if len(tier_a) != 11:
        raise RuntimeError(
            f"Expected 11 Tier-A features; "
            f"found {len(tier_a)}"
        )

    tier_a.sort(
        key=lambda r:
            int(r["variable_id"])
    )

    selected_features = [
        int(r["feature_id"])
        for r in tier_a
    ]

    target_variable_by_feature = {
        int(r["feature_id"]):
            int(r["variable_id"])
        for r in tier_a
    }

    feature_metadata = {
        int(r["feature_id"]): {
            "variable_id":
                int(r["variable_id"]),

            "variable":
                r["variable"],

            "feature_id":
                int(r["feature_id"]),

            "sae_tier":
                r["evidence_tier"],
        }
        for r in tier_a
    }

    config = json.loads(
        (
            sae_dir
            / "sae_inference_config.json"
        ).read_text()
    )

    weights_path = (
        sae_dir
        / "sae_inference.safetensors"
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

    tokenizer = (
        AutoTokenizer
        .from_pretrained(
            config["model"],
            use_fast=False,
        )
    )

    tokenizer.padding_side = "right"

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = (
            tokenizer.eos_token
        )

    model = (
        AutoModelForCausalLM
        .from_pretrained(
            config["model"],
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        )
    )

    model.to(device)
    model.eval()

    sd = load_file(
        str(weights_path),
        device=str(device),
    )

    feature_index = torch.tensor(
        selected_features,
        device=device,
        dtype=torch.long,
    )

    selected_W = (
        sd["W_enc"][
            :,
            feature_index,
        ]
        .float()
    )

    selected_b = (
        sd["b_enc"][
            feature_index
        ]
        .float()
    )

    selected_threshold = (
        sd["threshold"][
            feature_index
        ]
        .float()
    )

    b_dec = (
        sd["b_dec"]
        .float()
    )

    print(
        "FEATURE INSPECTION"
    )
    print(
        "=================="
    )

    for r in tier_a:
        print(
            f"{int(r['variable_id']):02d} "
            f"→ feature "
            f"{int(r['feature_id'])} "
            f"→ {r['variable']}"
        )

    natural, natural_stats = (
        natural_inspection(
            corpus_path=
                natural_corpus,

            top_k=args.top_k,

            batch_size=
                args.batch_size,

            tokenizer=
                tokenizer,

            model=model,

            selected_features=
                selected_features,

            selected_W=
                selected_W,

            selected_b=
                selected_b,

            selected_threshold=
                selected_threshold,

            b_dec=b_dec,

            activation_scale=
                float(
                    config[
                        "activation_scale"
                    ]
                ),

            hidden_state_index=
                int(
                    config[
                        "hidden_state_index"
                    ]
                ),

            max_length=
                args.max_length,

            device=device,
        )
    )

    controlled = (
        controlled_inspection(
            data_dir=
                feature_data_dir,

            top_k=args.top_k,

            batch_size=
                args.batch_size,

            tokenizer=
                tokenizer,

            model=model,

            selected_features=
                selected_features,

            selected_W=
                selected_W,

            selected_b=
                selected_b,

            selected_threshold=
                selected_threshold,

            b_dec=b_dec,

            activation_scale=
                float(
                    config[
                        "activation_scale"
                    ]
                ),

            hidden_state_index=
                int(
                    config[
                        "hidden_state_index"
                    ]
                ),

            max_length=
                args.max_length,

            device=device,
        )
    )

    summary_rows = []

    natural_path = (
        output_dir
        / "natural_top_activations.jsonl"
    )

    controlled_path = (
        output_dir
        / "controlled_top_activations.jsonl"
    )

    with natural_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        for feature_id in selected_features:

            record = {
                **feature_metadata[
                    feature_id
                ],

                "examples":
                    natural[
                        feature_id
                    ],
            }

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    with controlled_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        for feature_id in selected_features:

            examples = controlled[
                feature_id
            ]

            target_variable = (
                target_variable_by_feature[
                    feature_id
                ]
            )

            target_count = sum(
                int(
                    x["variable_id"]
                    == target_variable
                )
                for x in examples
            )

            record = {
                **feature_metadata[
                    feature_id
                ],

                "target_variable_fraction":
                    (
                        target_count
                        / len(examples)
                        if examples
                        else 0.0
                    ),

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

            natural_examples = (
                natural[
                    feature_id
                ]
            )

            natural_tokens = [
                x["token"]
                for x
                in natural_examples
            ]

            controlled_tokens = [
                x["token"]
                for x
                in examples
            ]

            summary_rows.append(
                {
                    "variable_id":
                        target_variable,

                    "variable":
                        feature_metadata[
                            feature_id
                        ]["variable"],

                    "feature_id":
                        feature_id,

                    "natural_examples":
                        len(
                            natural_examples
                        ),

                    "controlled_examples":
                        len(examples),

                    "controlled_target_fraction":
                        (
                            target_count
                            / len(examples)
                            if examples
                            else 0.0
                        ),

                    "natural_unique_top_tokens":
                        len(
                            set(
                                natural_tokens
                            )
                        ),

                    "controlled_unique_top_tokens":
                        len(
                            set(
                                controlled_tokens
                            )
                        ),
                }
            )

    summary_csv = (
        output_dir
        / "feature_inspection_summary.csv"
    )

    with summary_csv.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(
                summary_rows[0]
                .keys()
            ),
        )

        writer.writeheader()
        writer.writerows(
            summary_rows
        )

    manifest = {
        "purpose":
            (
                "Top-activating-example "
                "inspection for Tier-A "
                "SAE features."
            ),

        "features":
            feature_metadata,

        "natural_corpus":
            str(
                natural_corpus
            ),

        "natural_corpus_sha256":
            sha256(
                natural_corpus
            ),

        "natural_rows":
            natural_stats[
                "rows"
            ],

        "possible_natural_truncations":
            natural_stats[
                "possible_truncations"
            ],

        "controlled_data_dir":
            str(
                feature_data_dir
            ),

        "top_k":
            args.top_k,

        "ranking":
            (
                "sentence maximum "
                "token activation"
            ),

        "model":
            config["model"],

        "hidden_state_index":
            config[
                "hidden_state_index"
            ],

        "activation_scale":
            config[
                "activation_scale"
            ],

        "threshold":
            config[
                "threshold"
            ],

        "sae_weights_sha256":
            sha256(
                weights_path
            ),

        "outputs": {
            "natural":
                str(
                    natural_path
                ),

            "controlled":
                str(
                    controlled_path
                ),

            "summary":
                str(
                    summary_csv
                ),
        },
    }

    (
        output_dir
        / "inspection_manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )

    print()
    print(
        "FEATURE INSPECTION COMPLETE"
    )
    print(
        "==========================="
    )
    print(
        "Natural rows:",
        natural_stats[
            "rows"
        ],
    )
    print(
        "Natural truncations:",
        natural_stats[
            "possible_truncations"
        ],
    )
    print(
        "Saved:",
        natural_path,
    )
    print(
        "Saved:",
        controlled_path,
    )
    print(
        "Saved:",
        summary_csv,
    )


if __name__ == "__main__":
    main()
