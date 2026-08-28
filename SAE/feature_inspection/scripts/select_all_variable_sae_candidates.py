#!/usr/bin/env python3

from pathlib import Path
import pandas as pd


ROOT = Path(
    "artifacts/linguistic_feature_eval"
)

SPEC = (
    ROOT
    / "summary"
    / "cross_variable_specificity.csv"
)

SELECTED = (
    ROOT
    / "summary"
    / "trainval_selected_features.csv"
)

OUTDIR = (
    ROOT
    / "inspection"
    / "all_variables"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUT = (
    OUTDIR
    / "all_variable_candidate_selection.csv"
)


spec = pd.read_csv(SPEC)
selected = pd.read_csv(SELECTED)


# ============================================================
# MEAN-POOLED REPRESENTATION ONLY
# ============================================================

spec = spec[
    spec["pooling"].eq("mean")
].copy()

selected = selected[
    selected["pooling"].eq("mean")
].copy()


if len(selected) != 40:
    raise RuntimeError(
        f"Expected 40 mean-pooled selected rows; "
        f"found {len(selected)}"
    )


# ============================================================
# BUILD 5-CANDIDATE SET PER VARIABLE
#
# IMPORTANT:
# test_effect, test_same_direction and full_survival
# are NOT used for selection.
# ============================================================

rows = []

for variable_id in range(1, 41):

    pool = spec[
        spec["variable_id"].eq(
            variable_id
        )
    ].copy()

    if len(pool) != 25:
        raise RuntimeError(
            f"Variable {variable_id}: "
            f"expected 25 mean candidates, "
            f"found {len(pool)}"
        )

    primary = selected[
        selected["variable_id"].eq(
            variable_id
        )
    ]

    if len(primary) != 1:
        raise RuntimeError(
            f"Variable {variable_id}: "
            f"expected one selected feature, "
            f"found {len(primary)}"
        )

    primary_feature = int(
        primary.iloc[0][
            "feature_id"
        ]
    )

    # ----------------------------------------
    # Candidate quality classes.
    #
    # 0 = train FWER significant + val direction
    # 1 = train FWER significant
    # 2 = everything else
    #
    # This is intentionally permissive.
    # ----------------------------------------

    pool["candidate_class"] = 2

    train_sig = (
        pool[
            "train_fwer_significant"
        ].astype(bool)
    )

    val_dir = (
        pool[
            "val_same_direction"
        ].astype(bool)
    )

    pool.loc[
        train_sig,
        "candidate_class",
    ] = 1

    pool.loc[
        train_sig & val_dir,
        "candidate_class",
    ] = 0

    pool["abs_train_effect"] = (
        pool["train_effect"].abs()
    )

    # ----------------------------------------
    # Preserve original selected feature first.
    # ----------------------------------------

    primary_row = pool[
        pool["feature_id"].eq(
            primary_feature
        )
    ]

    if len(primary_row) != 1:
        raise RuntimeError(
            f"Variable {variable_id}: "
            f"primary feature {primary_feature} "
            f"not found in specificity table."
        )

    chosen = [
        primary_row.iloc[0]
    ]

    # ----------------------------------------
    # Rank remaining candidates.
    #
    # NO TEST INFORMATION.
    # ----------------------------------------

    remaining = pool[
        ~pool["feature_id"].eq(
            primary_feature
        )
    ].copy()

    remaining = remaining.sort_values(
        [
            "candidate_class",
            "target_rank_among_40_variables",
            "specificity_ratio_vs_max_other",
            "abs_train_effect",
            "rank",
        ],
        ascending=[
            True,
            True,
            False,
            False,
            True,
        ],
    )

    for _, r in remaining.head(
        4
    ).iterrows():
        chosen.append(r)

    if len(chosen) != 5:
        raise RuntimeError(
            f"Variable {variable_id}: "
            f"expected 5 candidates, "
            f"found {len(chosen)}"
        )

    for slot, r in enumerate(
        chosen,
        start=1,
    ):

        cls = int(
            r["candidate_class"]
        )

        if slot == 1:
            basis = (
                "original_trainval_selected"
            )
        elif cls == 0:
            basis = (
                "train_fwer_plus_val_direction"
            )
        elif cls == 1:
            basis = (
                "train_fwer_only"
            )
        else:
            basis = (
                "exploratory_top25"
            )

        rows.append(
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
                    slot,

                "feature_id":
                    int(
                        r[
                            "feature_id"
                        ]
                    ),

                "selection_basis":
                    basis,

                "original_candidate_rank":
                    int(
                        r["rank"]
                    ),

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

                "p_maxT":
                    float(
                        r["p_maxT"]
                    ),

                "train_fwer_significant":
                    bool(
                        r[
                            "train_fwer_significant"
                        ]
                    ),

                "val_same_direction":
                    bool(
                        r[
                            "val_same_direction"
                        ]
                    ),

                "specificity_rank":
                    int(
                        r[
                            "target_rank_among_40_variables"
                        ]
                    ),

                "specificity_ratio":
                    float(
                        r[
                            "specificity_ratio_vs_max_other"
                        ]
                    ),

                "specificity_margin":
                    float(
                        r[
                            "specificity_margin"
                        ]
                    ),

                "specificity_z":
                    float(
                        r[
                            "specificity_z_vs_other_variables"
                        ]
                    ),
            }
        )


result = pd.DataFrame(rows)

if len(result) != 200:
    raise RuntimeError(
        f"Expected 200 rows, "
        f"found {len(result)}"
    )

counts = (
    result
    .groupby("variable_id")
    .size()
)

if not (
    counts == 5
).all():
    raise RuntimeError(
        "Not every variable has "
        "exactly five candidates."
    )


result.to_csv(
    OUT,
    index=False,
)


print(
    "ALL-VARIABLE CANDIDATE SELECTION"
)
print(
    "================================"
)

print(
    "Variables:",
    result[
        "variable_id"
    ].nunique(),
)

print(
    "Candidate-variable pairs:",
    len(result),
)

print(
    "Unique SAE features:",
    result[
        "feature_id"
    ].nunique(),
)

print()

print(
    result[
        "selection_basis"
    ].value_counts()
)

print()

for vid, group in result.groupby(
    "variable_id",
    sort=True,
):

    print(
        f"{vid:02d} "
        f"{group.iloc[0]['variable']}"
    )

    for _, r in group.iterrows():

        print(
            f"  #{int(r['selection_slot'])} "
            f"feature={int(r['feature_id']):5d} "
            f"train={r['train_effect']:+.3f} "
            f"val={r['val_effect']:+.3f} "
            f"spec={r['specificity_ratio']:.2f} "
            f"rank40={int(r['specificity_rank']):2d} "
            f"{r['selection_basis']}"
        )

print()
print(
    "Selection did NOT use test data."
)

print(
    "Saved:",
    OUT,
)
