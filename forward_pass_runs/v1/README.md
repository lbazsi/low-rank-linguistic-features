# Main Differences Between the Initial and Updated Pipeline

The updated pipeline changes the project from a relatively direct activation-probing workflow into a stricter validation framework for linguistic-feature evidence. The initial version was already cautious: it trained activation probes, compared them against text baselines, used shuffled-label controls, and produced a conservative evidence status. The updated version goes further. It asks not only whether a feature is decodable, but whether the feature behaves like a stable representational direction that survives stronger split controls and can support a mechanistic interpretation.

The most important change is therefore conceptual: the updated version separates **activation recoverability**, **surface-text visibility**, **directional consistency**, **split generalization**, and **learned-direction viability** into distinct evidence levels. This prevents a high AUROC score from being treated as a single all-purpose proof of success.

## 1. The model target changed from Pythia-70M to XGLM-564M

The initial activation cache script used `EleutherAI/pythia-70m-deduped` to test whether the pipeline has research validity, on which the second version builds by using the multilinguial `facebook/xglm-564M`.

This matters because the dataset is multilingual and structurally linguistic. Pythia-70M is useful for cheap prototyping, but it is too small and too English-oriented to be a strong default model for cross-linguistic structural features. XGLM-564M is still computationally manageable, but it is a more appropriate target for a project where language, morphology, and non-English surface forms are central rather than incidental.

## 2. The dataset schema now preserves split-control metadata

The initial `flatten_feature_pairs.py` required the core contrast-pair fields: variable ID, variable name, approach, language, surface type, contrast, split, and pair. The updated version additionally requires and propagates two fields:

- `marker_family`
- `lexical_domain`

This is one of the most important methodological changes. In the initial pipeline, train/validation/test splits existed, but the scripts did not explicitly know whether a test example used marker families or lexical domains that were held out from training. As a result, a high test score could still be compatible with template familiarity or marker memorization.

The updated pipeline makes the split design auditable. It can now report whether test-set success reflects interpolation within familiar markers/domains or generalization to held-out marker families and lexical domains. This is essential for a synthetic linguistic-feature dataset, because otherwise the model may appear to learn a structural feature while actually learning a narrow set of recurring surface cues.

The updated flattener also searches recursively by default and prints marker-family and lexical-domain counts by split. The reason is straightforward: the dataset has become more structured, so the preprocessing step must verify that the structure is actually present before later results are interpreted.

## 3. Activation caching now carries richer metadata and fixes a pooling risk

The activation cache still stores sentence-level representations, including final-token and mean-pooled activations, and it still builds pair metadata for basis/changed contrasts. The updated version, however, carries `marker_family` and `lexical_domain` through both sentence metadata and pair metadata.

The updated cache script also explicitly sets right padding before final-token pooling. This is a small but important correction. Final-token pooling is only meaningful if the selected token is the final real token rather than a padding artifact. Since padding behavior can differ across tokenizers and models, forcing right padding makes the representation extraction more reliable.

The reason for this change is methodological hygiene. If a probe succeeds because final-token pooling accidentally selects inconsistent padding or tokenizer artifacts, the result would be uninterpretable. The updated version reduces that risk before the probing stage begins.

## 4. The delta task changed from mismatch detection to directional consistency

The initial training script used a delta task named `delta_true_vs_mismatched`. Positive examples were true changed-minus-basis deltas. Negative examples were constructed by mismatching basis and changed sentences across different pairs.

The updated script replaces this with `delta_direction_basis_to_changed`. Positive examples are still the forward direction, changed minus basis. Negative examples are now the reverse direction for the same pair, basis minus changed.

## 5. Text baselines were reinterpreted rather than used as an automatic rejection gate

In the initial evidence logic, if a text baseline matched or exceeded activation performance, the variable could be marked as failing the text-baseline control. This was conservative, but too blunt for the present research question.

The updated pipeline treats text baselines as diagnostic rather than fatal. It classifies text evidence into categories such as activation stronger than text, comparable to text, or text stronger than activation. However, surface visibility no longer automatically invalidates a result.

## 6. The evidence standard became a five-level ladder

The initial pipeline used a compact conservative status system. It asked whether activation AUROC was high enough, whether text baselines matched or beat activations, whether the best layer looked suspiciously early, and whether the result was promising enough for inspection.

The updated version formalizes interpretation into five levels:

1. **Activation recoverability**: can basis and changed examples be decoded from activations?
2. **Text/artifact control**: does surface text also solve the task, and how should that narrow the claim?
3. **Directional consistency**: does the basis-to-changed delta form a stable held-out direction?
4. **Split generalization**: does performance survive held-out marker-family or lexical-domain structure?
5. **Learned activation direction viability**: does adding the learned direction to held-out basis activations move them toward the changed class under the selected probe?

## 7. Bootstrap confidence intervals were added

The initial training script reported point estimates for metrics such as AUROC, accuracy, balanced accuracy, and F1. The updated script adds bootstrap confidence intervals for validation and test AUROC, both for activation probes and for the best text baselines.

This improves the statistical interpretation of the results. With only point estimates, a variable with AUROC 0.69 and another with AUROC 0.75 may appear meaningfully different even if the uncertainty is large. Confidence intervals make it easier to distinguish robust effects from unstable estimates caused by finite test-set size, class balance, or random variation.

## 8. Null controls became stronger and more scalable

The initial version used shuffled-label null controls with a default of three permutations. The updated version raises the default to fifty permutations and adds options for the control scope, parallel execution, and threadpool limits.

The reason is that probe pipelines can overfit quietly, especially when many layers, representations, and variables are searched. A stronger null distribution helps distinguish genuine signal from a favorable search over many candidate probes.

## 9. Layer-stability reporting was added

The updated training script now builds a layer-stability profile. It records, for each variable and probe family, how many layers exceed a threshold, whether the signal appears beyond early layers, and whether there are adjacent runs of above-threshold layers.

The reason for this addition is to avoid overvaluing the single best layer. Selecting the best layer by validation performance can hide the difference between a broad representational pattern and a one-layer artifact.

## 10. Split-control profiling was added to the result tables

Because the updated dataset now includes marker-family and lexical-domain metadata, the training script can produce `split_control_profile_by_variable`. This table records whether validation and test sets contain marker families or lexical domains held out from training, whether all test markers/domains are held out, and how much overlap remains.

The reason is to protect the core research claim. The project is not merely asking whether a classifier can learn recurring templates. It is asking whether controlled structural contrasts produce representational signals that generalize beyond the exact surface forms seen during training.

## 11. A learned activation direction viability check was introduced

The updated archive adds a new script: `run_learned_activation_direction_viability.py`. This script takes variables that are ready for the next stage, computes the mean training direction from basis to changed activations, adds that direction to held-out basis activations, and checks whether the selected sentence probe assigns a higher probability to the changed class.

The reason for adding this script is that mechanistic claims require more than decodability. A representation can be decodable yet not steerable, not stable, or not aligned with the intended transformation. This check is mainly for purposes of future analysis, it does not necessarily conclude that a variable is not worth investigating.

## 12. The analysis report now reflects the stronger evidence model

The initial analysis script produced a strict raw activation probe report with figures, tables, evidence status counts, and conservative interpretation rules. The updated analysis script expands this report around the evidence ladder.

It can now merge learned-direction viability results, update `mechanistic_claim_allowed` only when the viability check passes, report variables ready for the viability stage, include split-control profiles, and include layer-stability summaries.