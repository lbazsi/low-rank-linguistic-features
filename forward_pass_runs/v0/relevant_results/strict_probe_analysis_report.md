# Strict Raw Activation Probe Analysis

This report is intentionally conservative. It does not treat high activation AUROC as sufficient evidence.

## Counts

- Candidate activation probes: `960`
- Best activation probes: `80`
- Text baseline runs: `240`
- Null control runs: `1,440`
- Variables: `40`

## Evidence status counts

|                                                  |   evidence_status |
|:-------------------------------------------------|------------------:|
| failed_text_baseline_matches_or_beats_activation |                33 |
| artifact_risk_best_layer_too_early               |                 5 |
| unclear_or_weak_after_controls                   |                 2 |

## Variables currently allowed to move to manual inspection / SAE follow-up

None under the current conservative criteria.

## Best activation probes

| probe_family             |   variable_id | variable                                 | representation   |   layer_idx |   val_auroc |   test_auroc |   test_accuracy | suspiciously_high_test_auroc   | possible_overfit   |
|:-------------------------|--------------:|:-----------------------------------------|:-----------------|------------:|------------:|-------------:|----------------:|:-------------------------------|:-------------------|
| delta_true_vs_mismatched |             1 | Subject expression / pro-drop            | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             2 | basic_constituent_order                  | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             3 | nominal_modifier_order                   | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             4 | case_marking                             | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             5 | morphosyntactic_alignment                | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             6 | transitivity_valency                     | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             7 | voice_and_agent_prominence               | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             8 | causativity_and_valency_change           | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |             9 | analytic_vs_synthetic_encoding           | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            10 | morphological_segmentation_type          | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            11 | agreement_indexing_density               | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            12 | optionality_vs_obligatoriness_of_marking | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            13 | redundancy_cumulative_exponence          | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            14 | definiteness_and_specificity             | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            15 | number_marking                           | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            16 | gender_noun_class                        | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            17 | animacy_and_humanness                    | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            18 | person_marking_and_person_hierarchy      | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            19 | inclusive_exclusive_distinction          | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            20 | pronoun_richness_and_reduction           | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            21 | possession_and_alienability              | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            22 | tense_prominence                         | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            23 | aspect_and_event_structure               | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            24 | modality_and_mood                        | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            25 | epistemic_modality                       | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            26 | evidentiality                            | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            27 | mirativity_stance_and_affect_marking     | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            28 | negation_and_polarity_structure          | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            29 | quantifier_scope_and_distributivity      | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            30 | conditional_and_counterfactual_marking   | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            31 | subordination_and_embedding              | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            32 | quotation_and_reported_speech_structure  | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            33 | discourse_relation_marking               | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            34 | topic_comment_structure                  | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            35 | focus_and_given_new_marking              | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            36 | genericity_and_kind_level_reference      | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            37 | social_deixis_honorifics_status_encoding | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            38 | speech_act_force_and_request_directness  | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            39 | deixis_and_perspective_anchoring         | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| delta_true_vs_mismatched |            40 | orthographic_and_tokenization_interface  | final_token      |           0 |       0.5   |        0.5   |           0.667 | False                          | False              |
| sentence_basis_changed   |             7 | voice_and_agent_prominence               | mean_pooled      |           5 |       1     |        1     |           1     | True                           | False              |
| sentence_basis_changed   |             9 | analytic_vs_synthetic_encoding           | mean_pooled      |           0 |       1     |        1     |           1     | True                           | False              |
| sentence_basis_changed   |            10 | morphological_segmentation_type          | final_token      |           0 |       1     |        1     |           0.99  | True                           | False              |
| sentence_basis_changed   |            19 | inclusive_exclusive_distinction          | mean_pooled      |           0 |       1     |        1     |           1     | True                           | False              |
| sentence_basis_changed   |            20 | pronoun_richness_and_reduction           | final_token      |           0 |       1     |        1     |           1     | True                           | False              |
| sentence_basis_changed   |            27 | mirativity_stance_and_affect_marking     | final_token      |           2 |       1     |        1     |           1     | True                           | False              |
| sentence_basis_changed   |            29 | quantifier_scope_and_distributivity      | mean_pooled      |           2 |       1     |        1     |           0.99  | True                           | False              |
| sentence_basis_changed   |            39 | deixis_and_perspective_anchoring         | mean_pooled      |           0 |       1     |        1     |           1     | True                           | False              |
| sentence_basis_changed   |            37 | social_deixis_honorifics_status_encoding | final_token      |           3 |       1     |        0.998 |           0.98  | True                           | False              |
| sentence_basis_changed   |            11 | agreement_indexing_density               | mean_pooled      |           3 |       0.979 |        0.996 |           0.98  | True                           | False              |
| sentence_basis_changed   |            32 | quotation_and_reported_speech_structure  | final_token      |           3 |       1     |        0.996 |           0.97  | True                           | False              |
| sentence_basis_changed   |             4 | case_marking                             | mean_pooled      |           0 |       0.98  |        0.996 |           0.97  | True                           | False              |
| sentence_basis_changed   |            33 | discourse_relation_marking               | mean_pooled      |           1 |       0.996 |        0.994 |           0.97  | True                           | False              |
| sentence_basis_changed   |             1 | Subject expression / pro-drop            | mean_pooled      |           2 |       1     |        0.99  |           0.94  | True                           | False              |
| sentence_basis_changed   |            16 | gender_noun_class                        | mean_pooled      |           1 |       1     |        0.99  |           0.96  | True                           | False              |
| sentence_basis_changed   |            13 | redundancy_cumulative_exponence          | mean_pooled      |           5 |       0.964 |        0.98  |           0.92  | True                           | False              |
| sentence_basis_changed   |            30 | conditional_and_counterfactual_marking   | mean_pooled      |           0 |       0.985 |        0.98  |           0.91  | True                           | False              |
| sentence_basis_changed   |            38 | speech_act_force_and_request_directness  | mean_pooled      |           4 |       0.978 |        0.979 |           0.9   | True                           | False              |
| sentence_basis_changed   |            14 | definiteness_and_specificity             | mean_pooled      |           1 |       0.98  |        0.975 |           0.91  | True                           | False              |
| sentence_basis_changed   |             6 | transitivity_valency                     | mean_pooled      |           2 |       0.974 |        0.973 |           0.91  | True                           | False              |
| sentence_basis_changed   |            28 | negation_and_polarity_structure          | mean_pooled      |           1 |       0.951 |        0.965 |           0.86  | False                          | False              |
| sentence_basis_changed   |             2 | basic_constituent_order                  | mean_pooled      |           4 |       0.998 |        0.962 |           0.95  | False                          | False              |
| sentence_basis_changed   |            15 | number_marking                           | mean_pooled      |           4 |       0.972 |        0.962 |           0.91  | False                          | False              |
| sentence_basis_changed   |            22 | tense_prominence                         | mean_pooled      |           3 |       0.966 |        0.961 |           0.91  | False                          | False              |
| sentence_basis_changed   |            26 | evidentiality                            | mean_pooled      |           4 |       0.995 |        0.961 |           0.86  | False                          | False              |
| sentence_basis_changed   |            35 | focus_and_given_new_marking              | final_token      |           0 |       0.987 |        0.952 |           0.82  | False                          | False              |
| sentence_basis_changed   |            25 | epistemic_modality                       | mean_pooled      |           1 |       0.96  |        0.941 |           0.86  | False                          | False              |
| sentence_basis_changed   |            17 | animacy_and_humanness                    | mean_pooled      |           1 |       0.949 |        0.938 |           0.83  | False                          | False              |
| sentence_basis_changed   |            31 | subordination_and_embedding              | final_token      |           4 |       0.97  |        0.932 |           0.85  | False                          | False              |
| sentence_basis_changed   |            40 | orthographic_and_tokenization_interface  | mean_pooled      |           0 |       0.926 |        0.914 |           0.79  | False                          | False              |
| sentence_basis_changed   |            23 | aspect_and_event_structure               | mean_pooled      |           0 |       0.886 |        0.89  |           0.83  | False                          | False              |
| sentence_basis_changed   |            21 | possession_and_alienability              | mean_pooled      |           0 |       0.786 |        0.889 |           0.84  | False                          | True               |
| sentence_basis_changed   |             3 | nominal_modifier_order                   | mean_pooled      |           3 |       0.893 |        0.881 |           0.85  | False                          | False              |
| sentence_basis_changed   |             8 | causativity_and_valency_change           | final_token      |           2 |       0.879 |        0.86  |           0.78  | False                          | False              |
| sentence_basis_changed   |            36 | genericity_and_kind_level_reference      | final_token      |           3 |       0.939 |        0.852 |           0.74  | False                          | False              |
| sentence_basis_changed   |            34 | topic_comment_structure                  | final_token      |           0 |       0.912 |        0.843 |           0.71  | False                          | False              |
| sentence_basis_changed   |            12 | optionality_vs_obligatoriness_of_marking | final_token      |           0 |       0.859 |        0.84  |           0.67  | False                          | False              |
| sentence_basis_changed   |             5 | morphosyntactic_alignment                | mean_pooled      |           3 |       0.791 |        0.811 |           0.73  | False                          | True               |
| sentence_basis_changed   |            24 | modality_and_mood                        | final_token      |           3 |       0.839 |        0.756 |           0.63  | False                          | False              |
| sentence_basis_changed   |            18 | person_marking_and_person_hierarchy      | mean_pooled      |           5 |       0.876 |        0.724 |           0.59  | False                          | False              |

## Interpretation rule

- If text baseline matches or beats activation, the result should be treated as surface-classifiable.
- If the best activation layer is 0 or 1 and AUROC is high, artifact risk is high.
- If activation is weak, call it weak. Do not rescue it with qualitative interpretation.
- A promising result is only a candidate for manual inspection, not a mechanistic claim.
