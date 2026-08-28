#!/usr/bin/env python3

import json
from pathlib import Path

import pandas as pd


ROOT = Path(
    "artifacts"
)

INSPECT = (
    ROOT
    / "linguistic_feature_eval"
    / "inspection"
    / "all_variables"
)

SUMMARY = (
    ROOT
    / "linguistic_feature_eval"
    / "summary"
)

PROBE = (
    ROOT
    / "probe_comparison"
    / "summary"
)


selection = pd.read_csv(
    INSPECT
    / "PRETEST_SELECTION_FROZEN.csv"
)

specificity = pd.read_csv(
    SUMMARY
    / "cross_variable_specificity.csv"
)

evidence = pd.read_csv(
    SUMMARY
    / "sae_variable_evidence.csv"
)

probe = pd.read_csv(
    PROBE
    / "probe_sae_comparison.csv"
)


# Mean only.
specificity = specificity[
    specificity[
        "pooling"
    ].eq(
        "mean"
    )
].copy()


# Index natural examples by feature.
natural = {}

with (
    INSPECT
    / "all_variable_natural_top_activations.jsonl"
).open(
    encoding="utf-8"
) as f:

    for line in f:

        r = json.loads(
            line
        )

        natural[
            int(
                r[
                    "feature_id"
                ]
            )
        ] = r[
            "examples"
        ]


# Test annotation.
test_cols = [
    "variable_id",
    "feature_id",
    "test_effect",
    "test_same_direction",
    "full_survival",
]

test = specificity[
    test_cols
].copy()


review = selection.merge(
    test,
    on=[
        "variable_id",
        "feature_id",
    ],
    how="left",
    validate="one_to_one",
)


tier_map = {
    int(r["variable_id"]):
        r["evidence_tier"]
    for _, r in evidence.iterrows()
}


probe_map = {
    int(r["variable_id"]):
        {
            "status":
                r[
                    "probe_core_status"
                ],

            "l12_delta":
                float(
                    r[
                        "probe_l12_delta_test_auroc"
                    ]
                ),
        }
    for _, r in probe.iterrows()
}


out = (
    INSPECT
    / "ALL_VARIABLE_FEATURE_REVIEW.md"
)


with out.open(
    "w",
    encoding="utf-8",
) as f:

    f.write(
        "# All-Variable SAE Feature Review\n\n"
    )

    f.write(
        "Five mean-pooled SAE candidates were selected "
        "for each of the 40 linguistic variables before "
        "test evidence was consulted.\n\n"
    )

    f.write(
        "The purpose of this document is exploratory "
        "feature interpretation for later causal work. "
        "A candidate is **not automatically rejected** "
        "because of a test-direction mismatch, imperfect "
        "specificity, subgroup weakness, or a lower prior "
        "SAE evidence tier. Those properties should be "
        "treated as evidence weights rather than binary "
        "barriers.\n\n"
    )


    for variable_id in range(
        1,
        41,
    ):

        group = review[
            review[
                "variable_id"
            ].eq(
                variable_id
            )
        ].sort_values(
            "selection_slot"
        )


        if len(group) != 5:

            raise RuntimeError(
                f"Variable {variable_id}: "
                f"expected 5 rows, "
                f"found {len(group)}"
            )


        variable = (
            group.iloc[0][
                "variable"
            ]
        )


        p = probe_map[
            variable_id
        ]


        f.write(
            f"# Variable {variable_id:02d}: "
            f"{variable}\n\n"
        )


        f.write(
            f"- Original SAE evidence tier: "
            f"**{tier_map[variable_id]}**\n"
        )

        f.write(
            f"- Probe core status: "
            f"**{p['status']}**\n"
        )

        f.write(
            f"- Layer-12 mean delta probe test AUROC: "
            f"**{p['l12_delta']:.3f}**\n\n"
        )


        for _, r in group.iterrows():

            fid = int(
                r[
                    "feature_id"
                ]
            )


            f.write(
                f"## Candidate {int(r['selection_slot'])}: "
                f"feature {fid}\n\n"
            )


            f.write(
                f"- selection: `{r['selection_basis']}`\n"
            )

            f.write(
                f"- train effect: `{r['train_effect']:+.3f}`\n"
            )

            f.write(
                f"- validation effect: `{r['val_effect']:+.3f}`\n"
            )

            f.write(
                f"- test effect: `{r['test_effect']:+.3f}`\n"
            )

            f.write(
                f"- train maxT significant: "
                f"`{r['train_fwer_significant']}`\n"
            )

            f.write(
                f"- validation same direction: "
                f"`{r['val_same_direction']}`\n"
            )

            f.write(
                f"- test same direction: "
                f"`{r['test_same_direction']}`\n"
            )

            f.write(
                f"- full survival: "
                f"`{r['full_survival']}`\n"
            )

            f.write(
                f"- specificity rank among 40: "
                f"`{int(r['specificity_rank'])}`\n"
            )

            f.write(
                f"- specificity ratio: "
                f"`{r['specificity_ratio']:.3f}`\n\n"
            )


            examples = natural.get(
                fid,
                [],
            )


            f.write(
                "### Top natural activations\n\n"
            )


            for i, ex in enumerate(
                examples[:8],
                start=1,
            ):

                text = (
                    str(
                        ex[
                            "text"
                        ]
                    )
                    .replace(
                        "\n",
                        " "
                    )
                )

                f.write(
                    f"{i}. "
                    f"`act={ex['activation']:.4f}` "
                    f"`token={ex['token']!r}`  \n"
                )

                f.write(
                    f"   {text}\n\n"
                )


        f.write(
            "---\n\n"
        )


print(
    "Saved:",
    out,
)
