#!/usr/bin/env python3

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(
    "artifacts/causal_interventions/ablation_screen"
)

RESULTS = ROOT / "ablation_results.csv"
COMPARE = ROOT / "ablation_target_vs_controls.csv"

OUT_CSV = ROOT / "ablation_variable_summary.csv"
OUT_JSON = ROOT / "ablation_variable_summary.json"


results = pd.read_csv(RESULTS)
compare = pd.read_csv(COMPARE)


# ============================================================
# HELD-OUT TEST, TARGET INTERVENTION ONLY
# ============================================================

target = results[
    (results["split"] == "test")
    &
    (results["intervention_kind"] == "target")
].copy()

if len(target) != 40:
    raise RuntimeError(
        f"Expected 40 test target rows; found {len(target)}"
    )


cmp = compare[
    compare["split"] == "test"
].copy()

if len(cmp) != 40:
    raise RuntimeError(
        f"Expected 40 test comparison rows; found {len(cmp)}"
    )


# ============================================================
# BENJAMINI-HOCHBERG FDR
# ============================================================

def bh_adjust(p):
    p = np.asarray(
        p,
        dtype=float,
    )

    n = len(p)

    order = np.argsort(p)
    ranked = p[order]

    adjusted = (
        ranked
        * n
        / np.arange(
            1,
            n + 1,
        )
    )

    adjusted = np.minimum.accumulate(
        adjusted[::-1]
    )[::-1]

    adjusted = np.clip(
        adjusted,
        0,
        1,
    )

    out = np.empty(
        n,
        dtype=float,
    )

    out[order] = adjusted

    return out


cmp[
    "target_vs_control_fdr_q"
] = bh_adjust(
    cmp[
        "target_minus_control_bootstrap_p"
    ].values
)


# ============================================================
# MERGE
# ============================================================

keep_target = [
    "variable_id",
    "variable",
    "inspection_grade",
    "ablation_role",
    "target_feature",
    "intervention_side",
    "baseline_downstream_score",
    "intervention_downstream_score",
    "mean_attenuation",
    "attenuation_fraction",
    "attenuation_ci_low",
    "attenuation_ci_high",
    "attenuation_bootstrap_p",
    "mean_final_repr_cosine_to_baseline",
    "target_train_basis_mean_activation",
    "target_train_changed_mean_activation",
    "target_train_basis_fire_rate",
    "target_train_changed_fire_rate",
]

keep_cmp = [
    "variable_id",
    "matched_control_mean_attenuation",
    "target_minus_control_attenuation",
    "target_minus_control_ci_low",
    "target_minus_control_ci_high",
    "target_minus_control_bootstrap_p",
    "target_vs_control_fdr_q",
    "control_features",
]

df = target[
    keep_target
].merge(
    cmp[
        keep_cmp
    ],
    on="variable_id",
    how="left",
    validate="one_to_one",
)


# ============================================================
# DESCRIPTIVE CAUSAL CATEGORIES
#
# These are NOT exclusion criteria.
# ============================================================

def classify(row):

    target_positive = (
        row[
            "mean_attenuation"
        ] > 0
    )

    control_specific = (
        row[
            "target_minus_control_attenuation"
        ] > 0
    )

    fdr_specific = (
        row[
            "target_vs_control_fdr_q"
        ] < 0.05
        and control_specific
    )

    if (
        target_positive
        and fdr_specific
    ):
        return "specific_positive"

    if (
        target_positive
        and control_specific
    ):
        return "positive_control_advantage"

    if target_positive:
        return "positive_nonspecific"

    return "null_or_reverse"


df[
    "causal_screen_category"
] = df.apply(
    classify,
    axis=1,
)


# Representation disturbance:
# 0 = intervention leaves overall final representation unchanged.
df[
    "final_repr_distortion"
] = (
    1.0
    -
    df[
        "mean_final_repr_cosine_to_baseline"
    ]
)


# Absolute attenuation fraction is useful because the
# raw downstream direction scales vary across variables.
df[
    "abs_attenuation_fraction"
] = (
    df[
        "attenuation_fraction"
    ].abs()
)


# ============================================================
# SAVE
# ============================================================

df = df.sort_values(
    [
        "causal_screen_category",
        "target_minus_control_attenuation",
    ],
    ascending=[
        True,
        False,
    ],
)

df.to_csv(
    OUT_CSV,
    index=False,
)


summary = {
    "variables": 40,

    "positive_target_attenuation":
        int(
            (
                df[
                    "mean_attenuation"
                ]
                > 0
            ).sum()
        ),

    "target_better_than_controls":
        int(
            (
                df[
                    "target_minus_control_attenuation"
                ]
                > 0
            ).sum()
        ),

    "positive_and_fdr_specific":
        int(
            (
                (
                    df[
                        "mean_attenuation"
                    ]
                    > 0
                )
                &
                (
                    df[
                        "target_minus_control_attenuation"
                    ]
                    > 0
                )
                &
                (
                    df[
                        "target_vs_control_fdr_q"
                    ]
                    < 0.05
                )
            ).sum()
        ),

    "categories":
        df[
            "causal_screen_category"
        ].value_counts().to_dict(),

    "by_inspection_grade":
        pd.crosstab(
            df[
                "inspection_grade"
            ],
            df[
                "causal_screen_category"
            ],
        ).to_dict(),

    "interpretation": (
        "Categories are descriptive evidence levels, "
        "not filters. All variables remain available "
        "for steering and behavioral evaluation."
    ),
}


OUT_JSON.write_text(
    json.dumps(
        summary,
        indent=2,
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)


print()
print(
    "STEP 7B — ABLATION SYNTHESIS"
)

print(
    "============================"
)

print(
    "Variables:",
    len(df),
)

print(
    "Positive target attenuation:",
    summary[
        "positive_target_attenuation"
    ],
)

print(
    "Target > controls:",
    summary[
        "target_better_than_controls"
    ],
)

print(
    "Positive + FDR-specific:",
    summary[
        "positive_and_fdr_specific"
    ],
)

print()
print(
    "Categories:"
)

print(
    df[
        "causal_screen_category"
    ].value_counts()
)

print()
print(
    "By inspection grade:"
)

print(
    pd.crosstab(
        df[
            "inspection_grade"
        ],
        df[
            "causal_screen_category"
        ],
    )
)

print()

print(
    "Representation locality:"
)

print(
    df[
        "mean_final_repr_cosine_to_baseline"
    ].describe()
)

print()

cols = [
    "variable_id",
    "variable",
    "inspection_grade",
    "target_feature",
    "causal_screen_category",
    "mean_attenuation",
    "attenuation_fraction",
    "matched_control_mean_attenuation",
    "target_minus_control_attenuation",
    "target_vs_control_fdr_q",
    "mean_final_repr_cosine_to_baseline",
]

print(
    df[
        cols
    ]
    .sort_values(
        "target_minus_control_attenuation",
        ascending=False,
    )
    .to_string(
        index=False
    )
)

print()
print(
    "Saved:",
    OUT_CSV,
)

print(
    "Saved:",
    OUT_JSON,
)
