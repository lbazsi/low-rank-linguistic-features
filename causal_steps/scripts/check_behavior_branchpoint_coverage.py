#!/usr/bin/env python3

import json
from pathlib import Path

import numpy as np
import pandas as pd
from transformers import AutoTokenizer


DATA = Path(
    "data/feature_dataset"
)

CONFIG = Path(
    "artifacts/sae_canonical/"
    "xglm564m_hidden12_batchtopk16x_k256/"
    "sae_inference_config.json"
)

PRIMARY = Path(
    "artifacts/causal_interventions/"
    "mechanistic_convergence/"
    "PREBEHAVIOR_PRIMARY_COHORT.csv"
)

OUTDIR = Path(
    "artifacts/causal_interventions/"
    "behavioral_evaluation"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True,
)


TEXT_KEYS = (
    "text",
    "sentence",
    "content",
)


def get_text(x):
    for k in TEXT_KEYS:
        if k in x:
            return str(
                x[k]
            )

    raise RuntimeError(
        f"No text key: "
        f"{list(x.keys())}"
    )


def get_pair(row):

    basis = None
    changed = None

    for item in row["pair"]:

        typ = str(
            item.get(
                "type",
                "",
            )
        ).lower()

        if typ == "basis":
            basis = get_text(
                item
            )

        elif typ in {
            "changed",
            "change",
            "contrast",
            "target",
        }:
            changed = get_text(
                item
            )

    if basis is None or changed is None:

        assert len(
            row["pair"]
        ) == 2

        basis = get_text(
            row[
                "pair"
            ][0]
        )

        changed = get_text(
            row[
                "pair"
            ][1]
        )

    return (
        basis,
        changed,
    )


config = json.loads(
    CONFIG.read_text(
        encoding="utf-8"
    )
)


tokenizer = (
    AutoTokenizer
    .from_pretrained(
        config[
            "model"
        ],
        use_fast=False,
    )
)


primary_ids = set(
    pd.read_csv(
        PRIMARY
    )[
        "variable_id"
    ].astype(
        int
    )
)


rows = []


for path in sorted(
    DATA.rglob(
        "*.jsonl"
    )
):

    with path.open(
        encoding="utf-8"
    ) as f:

        for line in f:

            if not line.strip():
                continue

            obj = json.loads(
                line
            )

            split = str(
                obj[
                    "split"
                ]
            ).lower()

            if split in {
                "validation",
                "valid",
                "dev",
            }:
                split = "val"

            if split not in {
                "val",
                "test",
            }:
                continue

            basis, changed = (
                get_pair(
                    obj
                )
            )

            b = tokenizer.encode(
                basis,
                add_special_tokens=False,
            )

            c = tokenizer.encode(
                changed,
                add_special_tokens=False,
            )

            k = 0

            while (
                k < len(b)
                and
                k < len(c)
                and
                b[k] == c[k]
            ):
                k += 1

            has_divergence = (
                k < len(b)
                and
                k < len(c)
            )

            rows.append({
                "variable_id":
                    int(
                        obj[
                            "variable_id"
                        ]
                    ),

                "variable":
                    str(
                        obj[
                            "variable"
                        ]
                    ),

                "pair_id":
                    str(
                        obj[
                            "id"
                        ]
                    ),

                "split":
                    split,

                "primary_mechanistic":
                    int(
                        obj[
                            "variable_id"
                        ]
                    )
                    in primary_ids,

                "basis_tokens":
                    len(
                        b
                    ),

                "changed_tokens":
                    len(
                        c
                    ),

                "common_prefix_tokens":
                    k,

                "eligible_shared_prefix":
                    bool(
                        has_divergence
                        and
                        k >= 1
                    ),

                "diverges_at_first_token":
                    bool(
                        has_divergence
                        and
                        k == 0
                    ),

                "identical_token_sequence":
                    bool(
                        b == c
                    ),
            })


df = pd.DataFrame(
    rows
)


pair_path = (
    OUTDIR
    / "branchpoint_pair_coverage.csv"
)

df.to_csv(
    pair_path,
    index=False,
)


summary = (
    df.groupby(
        [
            "variable_id",
            "variable",
            "split",
            "primary_mechanistic",
        ],
        as_index=False,
    )
    .agg(
        pairs=(
            "pair_id",
            "size",
        ),

        eligible=(
            "eligible_shared_prefix",
            "sum",
        ),

        first_token_divergence=(
            "diverges_at_first_token",
            "sum",
        ),

        identical=(
            "identical_token_sequence",
            "sum",
        ),

        mean_common_prefix_tokens=(
            "common_prefix_tokens",
            "mean",
        ),

        median_common_prefix_tokens=(
            "common_prefix_tokens",
            "median",
        ),
    )
)


summary[
    "eligible_fraction"
] = (
    summary[
        "eligible"
    ]
    /
    summary[
        "pairs"
    ]
)


summary_path = (
    OUTDIR
    / "branchpoint_coverage_summary.csv"
)

summary.to_csv(
    summary_path,
    index=False,
)


test = summary[
    summary[
        "split"
    ]
    == "test"
].copy()


print()
print(
    "STEP 9 BRANCH-POINT COVERAGE"
)

print(
    "============================"
)

print()

print(
    test[
        [
            "variable_id",
            "variable",
            "primary_mechanistic",
            "pairs",
            "eligible",
            "eligible_fraction",
            "first_token_divergence",
            "mean_common_prefix_tokens",
        ]
    ].to_string(
        index=False
    )
)


primary = test[
    test[
        "primary_mechanistic"
    ]
]


print()
print(
    "PRIMARY COHORT"
)

print(
    "--------------"
)

print(
    "Variables:",
    len(
        primary
    ),
)

print(
    "Mean eligible fraction:",
    primary[
        "eligible_fraction"
    ].mean(),
)

print(
    "Minimum variable eligible fraction:",
    primary[
        "eligible_fraction"
    ].min(),
)

print(
    "Total eligible pairs:",
    int(
        primary[
            "eligible"
        ].sum()
    ),
)

print(
    "/",
    int(
        primary[
            "pairs"
        ].sum()
    ),
)

print()

print(
    "Saved:",
    pair_path,
)

print(
    "Saved:",
    summary_path,
)
