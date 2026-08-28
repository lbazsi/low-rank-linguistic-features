#!/usr/bin/env python3

import json
from pathlib import Path

import pandas as pd


ROOT = Path(
    "artifacts/causal_interventions"
)

ABL = (
    ROOT
    / "ablation_screen"
    / "ablation_variable_summary.csv"
)

STR = (
    ROOT
    / "steering_screen"
    / "steering_variable_summary.csv"
)

OUTDIR = (
    ROOT
    / "mechanistic_convergence"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True,
)


a = pd.read_csv(
    ABL
).sort_values(
    "variable_id"
)

s = pd.read_csv(
    STR
).sort_values(
    "variable_id"
)


assert len(a) == 40
assert len(s) == 40


keep_a = [
    "variable_id",
    "variable",
    "inspection_grade",
    "target_feature",
    "causal_screen_category",
    "mean_attenuation",
    "attenuation_fraction",
    "target_minus_control_attenuation",
    "target_vs_control_fdr_q",
    "mean_final_repr_cosine_to_baseline",
]

keep_s = [
    "variable_id",
    "steering_screen_category",
    "target_mean_attenuation_primary",
    "target_attenuation_fraction_primary",
    "target_minus_control_attenuation",
    "target_vs_control_fdr_q",
    "dose_monotonic_non_decreasing",
    "target_final_repr_cosine_primary",
    "feature_high_side",
    "steering_side",
    "train_target_activation_gap",
]


a = a[
    keep_a
].rename(
    columns={
        "causal_screen_category":
            "ablation_category",

        "mean_attenuation":
            "ablation_mean_attenuation",

        "attenuation_fraction":
            "ablation_attenuation_fraction",

        "target_minus_control_attenuation":
            "ablation_target_minus_control",

        "target_vs_control_fdr_q":
            "ablation_fdr_q",

        "mean_final_repr_cosine_to_baseline":
            "ablation_final_repr_cosine",
    }
)


s = s[
    keep_s
].rename(
    columns={
        "steering_screen_category":
            "steering_category",

        "target_mean_attenuation_primary":
            "steering_mean_attenuation",

        "target_attenuation_fraction_primary":
            "steering_attenuation_fraction",

        "target_minus_control_attenuation":
            "steering_target_minus_control",

        "target_vs_control_fdr_q":
            "steering_fdr_q",

        "target_final_repr_cosine_primary":
            "steering_final_repr_cosine",
    }
)


df = a.merge(
    s,
    on="variable_id",
    validate="one_to_one",
)


df[
    "ablation_specific"
] = (
    df[
        "ablation_category"
    ]
    == "specific_positive"
)

df[
    "steering_specific"
] = (
    df[
        "steering_category"
    ]
    == "specific_positive"
)


df[
    "primary_mechanistic"
] = (
    df[
        "ablation_specific"
    ]
    &
    df[
        "steering_specific"
    ]
    &
    df[
        "dose_monotonic_non_decreasing"
    ]
)


def cohort(row):

    if row[
        "primary_mechanistic"
    ]:
        return (
            "primary_bidirectional"
        )

    if (
        row[
            "ablation_specific"
        ]
        or
        row[
            "steering_specific"
        ]
    ):
        return (
            "secondary_one_direction"
        )

    return "exploratory"


df[
    "behavior_cohort"
] = df.apply(
    cohort,
    axis=1,
)


out_csv = (
    OUTDIR
    / "mechanistic_convergence.csv"
)

df.to_csv(
    out_csv,
    index=False,
)


primary = df[
    df[
        "primary_mechanistic"
    ]
].copy()


primary_path = (
    OUTDIR
    / "PREBEHAVIOR_PRIMARY_COHORT.csv"
)

primary.to_csv(
    primary_path,
    index=False,
)


summary = {
    "stage":
        "Steps 7-8 mechanistic freeze",

    "behavior_results_consulted":
        False,

    "variables":
        40,

    "primary_mechanistic_count":
        int(
            len(
                primary
            )
        ),

    "primary_definition": (
        "Ablation specific_positive AND "
        "steering specific_positive AND "
        "monotonic 0.5x→1x→2x steering "
        "dose response."
    ),

    "primary_variable_ids":
        primary[
            "variable_id"
        ].astype(
            int
        ).tolist(),

    "cohort_counts":
        df[
            "behavior_cohort"
        ].value_counts().to_dict(),

    "behavior_plan": (
        "Primary behavioral inference is "
        "performed on the frozen primary "
        "mechanistic cohort. All 40 variables "
        "may additionally be evaluated and "
        "reported exploratorily."
    ),
}


json_path = (
    OUTDIR
    / "mechanistic_convergence.json"
)

json_path.write_text(
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
    "MECHANISTIC COHORT FROZEN"
)

print(
    "========================="
)

print(
    "Primary:",
    len(
        primary
    ),
)

print(
    "Primary variable IDs:",
    ",".join(
        f"{x:02d}"
        for x
        in primary[
            "variable_id"
        ].astype(
            int
        )
    ),
)

print()

print(
    df[
        "behavior_cohort"
    ].value_counts()
)

print()

print(
    primary[
        [
            "variable_id",
            "variable",
            "target_feature",
            "inspection_grade",
            "ablation_category",
            "steering_category",
        ]
    ].to_string(
        index=False
    )
)

print()

print(
    "Saved:",
    out_csv,
)

print(
    "Saved:",
    primary_path,
)

print(
    "Saved:",
    json_path,
)
