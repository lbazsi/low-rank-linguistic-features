#!/usr/bin/env python3

from pathlib import Path
import pandas as pd


SRC = Path(
    "artifacts/linguistic_feature_eval/"
    "summary/cross_variable_specificity.csv"
)

OUT = Path(
    "artifacts/linguistic_feature_eval/"
    "inspection/alternative_feature_candidates.csv"
)

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


# Variables whose initially selected Tier-A feature
# was artifact-dominated or not cleanly interpretable.
TARGETS = {
    4: 13269,
    10: 6125,
    13: 9749,
    20: 7551,
    21: 9576,
    27: 1887,
    31: 7643,
    38: 3396,
}


df = pd.read_csv(SRC)

# Primary SAE representation only.
df = df[
    df["pooling"].eq("mean")
].copy()

# Only variables requiring alternative inspection.
df = df[
    df["variable_id"].isin(TARGETS)
].copy()

# Selection evidence:
# - train maxT/FWER significant
# - validation same direction
# This field was already constructed without test-based selection.
df = df[
    df["trainval_candidate"].astype(bool)
].copy()

# Explicitly exclude the previously inspected feature.
df = df[
    df.apply(
        lambda r:
            int(r["feature_id"])
            != TARGETS[int(r["variable_id"])],
        axis=1,
    )
].copy()

df["abs_train_effect"] = (
    df["train_effect"].abs()
)

# Same selection logic as the earlier train/val selection:
# 1. minimize target rank across 40 variables
# 2. maximize specificity ratio
# 3. maximize training effect
# 4. use original within-variable rank as final tie-breaker
#
# IMPORTANT:
# test_effect and test_same_direction are NOT used here.
df = df.sort_values(
    [
        "variable_id",
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

selected = (
    df.groupby(
        "variable_id",
        sort=True,
        group_keys=False,
    )
    .head(3)
    .copy()
)

counts = (
    selected
    .groupby("variable_id")
    .size()
)

for variable_id in TARGETS:
    n = int(
        counts.get(
            variable_id,
            0,
        )
    )

    if n != 3:
        raise RuntimeError(
            f"Variable {variable_id}: "
            f"expected 3 alternatives, found {n}"
        )


# Save ONLY train/validation selection information here.
# Test evidence is deliberately omitted from this selection artifact.
cols = [
    "variable_id",
    "variable",
    "pooling",
    "rank",
    "feature_id",
    "train_effect",
    "val_effect",
    "p_maxT",
    "train_fwer_significant",
    "val_same_direction",
    "target_train_abs_effect",
    "max_other_variable_abs_effect",
    "target_rank_among_40_variables",
    "specificity_ratio_vs_max_other",
    "specificity_margin",
    "specificity_z_vs_other_variables",
    "target_share_of_feature_abs_effect",
]

selected = selected[cols]

selected.to_csv(
    OUT,
    index=False,
)

print()
print("ALTERNATIVE SAE CANDIDATES")
print("==========================")
print(
    f"Variables: {selected['variable_id'].nunique()}"
)
print(
    f"Candidates: {len(selected)}"
)
print()

for variable_id, group in selected.groupby(
    "variable_id",
    sort=True,
):
    print(
        f"{variable_id:02d}  "
        f"{group.iloc[0]['variable']}"
    )

    for _, r in group.iterrows():
        print(
            f"    feature={int(r['feature_id']):5d} "
            f"rank40={int(r['target_rank_among_40_variables']):2d} "
            f"spec={float(r['specificity_ratio_vs_max_other']):.3f} "
            f"train={float(r['train_effect']):+.3f} "
            f"val={float(r['val_effect']):+.3f} "
            f"pmaxT={float(r['p_maxT']):.5f}"
        )

    print()

print("Saved:", OUT)
