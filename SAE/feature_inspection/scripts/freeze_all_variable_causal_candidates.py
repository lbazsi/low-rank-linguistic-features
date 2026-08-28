#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(
    "artifacts/linguistic_feature_eval"
)

SUMMARY = ROOT / "summary"

OUTDIR = (
    ROOT
    / "inspection"
    / "all_variables"
)

OUTDIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# MANUAL FEATURE-INSPECTION DECISIONS
#
# Grades:
#
# A = strong target-aligned candidate
#
# B = clearly relevant feature, but narrower,
#     language-specific, surface-heavy, or has
#     some statistical imperfection
#
# C = plausible / partial proxy; exploratory
#     causal intervention is still worthwhile
#
# D = natural activations do not convincingly
#     match the target. Still retained in the
#     broad ablation screen as a diagnostic.
#
# IMPORTANT:
# NO VARIABLE IS REMOVED FROM ABLATION.
# ============================================================

decisions = [
    (
        1,
        8041,
        "C",
        "mixed_subject_expression_proxy",
        "Multilingual subject/pronoun-related activation; "
        "not a clean pro-drop latent, but strong held-out "
        "association makes exploratory ablation worthwhile.",
    ),
    (
        2,
        932,
        "C",
        "clause_order_proxy",
        "Cross-lingual pronoun/function-word and clause "
        "structure feature. Not clean constituent order, "
        "but plausibly related to syntactic organization.",
    ),
    (
        3,
        4426,
        "C",
        "prenominal_possessive_modifier",
        "Strong Spanish possessive determiner 'su' feature. "
        "A narrow nominal-modifier surface feature despite "
        "held-out direction instability.",
    ),
    (
        4,
        13269,
        "B",
        "case_bearing_nominals",
        "Natural activations contain case-bearing nominal "
        "forms, especially Turkish. Target-relevant but "
        "partly lexical/language-specific.",
    ),
    (
        5,
        7247,
        "D",
        "shared_punctuation_proxy",
        "Statistically associated but natural activation "
        "is dominated by punctuation and shared structure. "
        "Useful diagnostic rather than interpretable alignment.",
    ),
    (
        6,
        164,
        "C",
        "argument_structure_morphology_proxy",
        "Morphosyntactic material plausibly related to "
        "argument structure, but shared across variables "
        "and not a clean transitivity latent.",
    ),
    (
        7,
        8235,
        "A",
        "voice_passive_participle_structure",
        "Natural activations repeatedly contain passive/"
        "participial morphology across languages and agree "
        "with strong probe and SAE evidence.",
    ),
    (
        8,
        8182,
        "D",
        "causativity_association_uninterpretable",
        "Strong quantitative association but natural examples "
        "do not isolate causative or increased-valency structure.",
    ),
    (
        9,
        144,
        "C",
        "analytic_synthetic_morphology_proxy",
        "Hindi case/postpositional morphology provides a "
        "narrow grammatical proxy for analytic-versus-synthetic "
        "encoding, but not a language-general representation.",
    ),
    (
        10,
        15843,
        "B",
        "turkish_suffixal_morphology",
        "Clear Turkish suffix/person/possessive morphology. "
        "Narrower than abstract segmentation type, but strongly "
        "relevant to morphological segmentation.",
    ),
    (
        11,
        758,
        "C",
        "agreement_inflection_proxy",
        "Natural examples contain inflectional gender/number "
        "material. Plausibly agreement-related but does not "
        "cleanly encode agreement-density as an abstraction.",
    ),
    (
        12,
        9607,
        "D",
        "optionality_uninterpretable",
        "Natural activation is dominated by Japanese temporal "
        "marker material rather than optional/obligatory marking.",
    ),
    (
        13,
        4814,
        "B",
        "cumulative_inflection_morphology",
        "Russian inflectional endings plausibly combine multiple "
        "grammatical dimensions and are relevant to cumulative "
        "exponence, though language-specific.",
    ),
    (
        14,
        12995,
        "C",
        "indefinite_one_proxy",
        "Japanese 'one' material is potentially related to "
        "indefiniteness/specificity, but natural interpretation "
        "is narrower and ambiguous.",
    ),
    (
        15,
        8685,
        "B",
        "plural_number_morphology",
        "Natural activations strongly track plural morphology "
        "such as English -s and plural suffixes in other scripts. "
        "Worth causal testing despite split-direction instability.",
    ),
    (
        16,
        5205,
        "A",
        "grammatical_gender_feminine_morphology",
        "Strong Arabic and Urdu feminine/gender morphology with "
        "excellent train/validation/test consistency.",
    ),
    (
        17,
        6618,
        "D",
        "animacy_lexical_proxy",
        "Natural activation mostly identifies artificial-"
        "intelligence lexical material rather than a general "
        "animacy/humanness distinction.",
    ),
    (
        18,
        13235,
        "B",
        "first_person_plural_marking",
        "Telugu first-person plural/pronominal morphology is "
        "directly person-related, though language-specific and "
        "narrower than the full person hierarchy.",
    ),
    (
        19,
        6062,
        "C",
        "first_person_pronoun_proxy",
        "Strong Chinese first-person pronoun feature. Relevant "
        "to person reference but not specifically inclusive/"
        "exclusive distinction.",
    ),
    (
        20,
        6944,
        "A",
        "crosslingual_third_person_pronouns",
        "Natural activations identify third-person pronouns "
        "across several languages; strong grammatical and "
        "cross-lingual target alignment.",
    ),
    (
        21,
        15325,
        "C",
        "kinship_possession_proxy",
        "Natural examples repeatedly involve kinship and "
        "possessive relations. Relevant to possession but "
        "does not isolate alienability itself.",
    ),
    (
        22,
        1385,
        "C",
        "temporal_reference_lexemes",
        "Natural activations include week/month/year and other "
        "temporal reference material. Tense-related surface "
        "feature despite held-out instability.",
    ),
    (
        23,
        6216,
        "B",
        "progressive_aspect_ing",
        "Natural activations strongly track English -ing/"
        "progressive event morphology. Clear aspect-related "
        "feature despite train/validation/test direction mismatch.",
    ),
    (
        24,
        13197,
        "A",
        "deontic_modality_markers",
        "Cross-lingual modal material including should/debes/"
        "debemos. Strongly interpretable modality feature with "
        "held-out survival.",
    ),
    (
        25,
        15221,
        "A",
        "epistemic_uncertainty_markers",
        "Cross-lingual uncertainty/epistemic markers such as "
        "perhaps, vielleicht, quizás and doute. Strong target "
        "alignment and quantitative evidence.",
    ),
    (
        26,
        6900,
        "B",
        "turkish_indirect_evidential_mis",
        "Natural activations strongly track Turkish -miş, a "
        "canonical indirect/reportative evidential marker. "
        "Excellent semantic interpretation despite held-out "
        "construction instability.",
    ),
    (
        27,
        1887,
        "C",
        "mirativity_japanese_entangled",
        "Natural contexts often contain surprise/mirative "
        "content but activation is heavily entangled with "
        "Japanese punctuation and language identity.",
    ),
    (
        28,
        4382,
        "D",
        "negation_association_uninterpretable",
        "Strong statistical association but the natural feature "
        "mostly tracks entre/zwischen rather than negation or "
        "polarity.",
    ),
    (
        29,
        8551,
        "B",
        "quantified_noun_phrases",
        "Natural activations repeatedly contain numerically "
        "quantified noun phrases across languages. Relevant "
        "to quantification, though scope/distributivity itself "
        "is not established.",
    ),
    (
        30,
        11810,
        "B",
        "counterfactual_conditional_morphology",
        "French and English counterfactual constructions such "
        "as aurais/aurait and if-had structures. Strong target "
        "interpretation with some uneven validation strength.",
    ),
    (
        31,
        11461,
        "B",
        "complementizer_embedding",
        "Natural activations strongly track complementizers "
        "that/qu in embedded clauses. Clear structural surface "
        "feature despite held-out sign reversal.",
    ),
    (
        32,
        1754,
        "B",
        "quotation_mark_surface_control",
        "Highly specific quotation-mark feature. It is a "
        "surface realization rather than deep reported-speech "
        "semantics, but is an excellent positive causal control.",
    ),
    (
        33,
        9728,
        "D",
        "discourse_relation_uninterpretable",
        "Natural activations are mixed lexical material and do "
        "not provide a convincing discourse-relation feature.",
    ),
    (
        34,
        1302,
        "D",
        "topic_comment_uninterpretable",
        "Natural activation is dominated by language-specific "
        "verbal morphology and does not isolate topic-comment "
        "organization.",
    ),
    (
        35,
        7136,
        "B",
        "japanese_korean_focus_particles",
        "Japanese ga and Korean i-like grammatical particles "
        "are plausibly related to focus/new-subject marking. "
        "Language-specific but directly worth causal testing.",
    ),
    (
        36,
        1858,
        "D",
        "genericity_quantifier_proxy",
        "Plural/quantified noun material occurs naturally but "
        "does not cleanly distinguish generic or kind-level "
        "reference.",
    ),
    (
        37,
        2081,
        "A",
        "korean_formal_honorific_morphology",
        "Natural activations strongly track Korean formal/"
        "honorific endings such as -습니다/-했습니다 with "
        "strong specificity.",
    ),
    (
        38,
        14406,
        "C",
        "speech_act_exclamation_surface",
        "Exclamation punctuation is a direct surface correlate "
        "of speech-act force. It does not isolate request "
        "directness, but is useful for exploratory ablation.",
    ),
    (
        39,
        14441,
        "A",
        "crosslingual_temporal_deixis",
        "Natural activations track now/current/today expressions "
        "across Japanese, Korean, Turkish and other languages. "
        "Strong deixis-related feature.",
    ),
    (
        40,
        3132,
        "B",
        "orthographic_punctuation_interface",
        "Comma/punctuation activation is exactly relevant to "
        "the orthographic-tokenization interface variable. "
        "Statistical instability does not make it an artifact "
        "for this target.",
    ),
]


# ============================================================
# LOAD EXISTING QUANTITATIVE EVIDENCE
# ============================================================

spec = pd.read_csv(
    SUMMARY
    / "cross_variable_specificity.csv"
)

spec = spec[
    spec["pooling"].eq("mean")
].copy()


sae_evidence = pd.read_csv(
    SUMMARY
    / "sae_variable_evidence.csv"
)


probe = pd.read_csv(
    "artifacts/probe_comparison/"
    "summary/probe_sae_comparison.csv"
)


sae_tier = {
    int(r["variable_id"]):
        r["evidence_tier"]
    for _, r
    in sae_evidence.iterrows()
}


probe_info = {
    int(r["variable_id"]): {
        "probe_core_status":
            r["probe_core_status"],

        "probe_l12_delta_test_auroc":
            float(
                r[
                    "probe_l12_delta_test_auroc"
                ]
            ),
    }
    for _, r
    in probe.iterrows()
}


# ============================================================
# VERIFY AND JOIN
# ============================================================

rows = []

for (
    variable_id,
    feature_id,
    grade,
    interpretation,
    rationale,
) in decisions:

    found = spec[
        spec["variable_id"].eq(
            variable_id
        )
        &
        spec["feature_id"].eq(
            feature_id
        )
    ]

    if len(found) != 1:
        raise RuntimeError(
            f"{variable_id}/{feature_id}: "
            f"expected 1 row, found {len(found)}"
        )

    r = found.iloc[0]

    if grade == "A":
        role = "primary_causal"
    elif grade == "B":
        role = "causal_worth_testing"
    elif grade == "C":
        role = "exploratory_causal"
    else:
        role = "diagnostic_control"

    rows.append(
        {
            "variable_id":
                variable_id,

            "variable":
                r["variable"],

            "feature_id":
                feature_id,

            "inspection_grade":
                grade,

            "ablation_include":
                True,

            "ablation_role":
                role,

            "interpretation":
                interpretation,

            "inspection_rationale":
                rationale,

            "original_sae_tier":
                sae_tier[
                    variable_id
                ],

            "probe_core_status":
                probe_info[
                    variable_id
                ][
                    "probe_core_status"
                ],

            "probe_l12_delta_test_auroc":
                probe_info[
                    variable_id
                ][
                    "probe_l12_delta_test_auroc"
                ],

            "train_effect":
                float(
                    r[
                        "train_effect"
                    ]
                ),

            "validation_effect":
                float(
                    r[
                        "val_effect"
                    ]
                ),

            "test_effect":
                float(
                    r[
                        "test_effect"
                    ]
                ),

            "train_fwer_significant":
                bool(
                    r[
                        "train_fwer_significant"
                    ]
                ),

            "validation_same_direction":
                bool(
                    r[
                        "val_same_direction"
                    ]
                ),

            "test_same_direction":
                bool(
                    r[
                        "test_same_direction"
                    ]
                ),

            "full_survival":
                bool(
                    r[
                        "full_survival"
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
        }
    )


if len(rows) != 40:
    raise RuntimeError(
        f"Expected 40 decisions, "
        f"found {len(rows)}"
    )


df = pd.DataFrame(
    rows
).sort_values(
    "variable_id"
)


# ============================================================
# SAVE
# ============================================================

csv_path = (
    OUTDIR
    / "causal_candidate_ranking.csv"
)

df.to_csv(
    csv_path,
    index=False,
)


summary = {
    "stage":
        "post_inspection_causal_candidate_freeze",

    "variables":
        40,

    "all_variables_included_in_ablation":
        True,

    "grading_policy": {
        "A":
            (
                "Strong natural target alignment; "
                "primary causal candidate."
            ),

        "B":
            (
                "Clearly target-relevant but narrower, "
                "language-specific, surface-heavy, or "
                "statistically imperfect. Still a main "
                "ablation candidate."
            ),

        "C":
            (
                "Plausible or partial target proxy. "
                "Retained for exploratory ablation."
            ),

        "D":
            (
                "No convincing target interpretation. "
                "Retained in broad ablation as a "
                "diagnostic/negative feature control."
            ),
    },

    "grade_counts":
        dict(
            Counter(
                df[
                    "inspection_grade"
                ]
            )
        ),

    "important_methodological_note":
        (
            "Small validation/test direction failures, "
            "imperfect specificity, language specificity, "
            "and surface realization were treated as "
            "evidence weights rather than automatic "
            "exclusion criteria. All 40 variables are "
            "retained in the initial ablation screen."
        ),

    "candidates":
        df.to_dict(
            orient="records"
        ),
}


json_path = (
    OUTDIR
    / "causal_candidate_ranking.json"
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


# Minimal file consumed by ablation code.
ablation_path = (
    OUTDIR
    / "ablation_primary_candidates.csv"
)

df[
    [
        "variable_id",
        "variable",
        "feature_id",
        "inspection_grade",
        "ablation_role",
    ]
].to_csv(
    ablation_path,
    index=False,
)


print()
print(
    "CAUSAL CANDIDATE SET FROZEN"
)

print(
    "==========================="
)

print(
    "Variables:",
    len(df),
)

print()

print(
    df[
        "inspection_grade"
    ].value_counts()
    .sort_index()
)

print()

print(
    "A/B primary-or-strong:",
    int(
        df[
            "inspection_grade"
        ]
        .isin(
            ["A", "B"]
        )
        .sum()
    ),
)

print(
    "A/B/C target-oriented:",
    int(
        df[
            "inspection_grade"
        ]
        .isin(
            ["A", "B", "C"]
        )
        .sum()
    ),
)

print(
    "D diagnostic controls:",
    int(
        (
            df[
                "inspection_grade"
            ]
            == "D"
        )
        .sum()
    ),
)

print()

print(
    "Saved:",
    csv_path,
)

print(
    "Saved:",
    json_path,
)

print(
    "Saved:",
    ablation_path,
)
