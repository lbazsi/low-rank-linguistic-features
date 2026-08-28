# Post-Canonical SAE Linguistic Feature Analysis

This document summarizes all analysis performed **after freezing the canonical XGLM-564M sparse autoencoder** in the Low-Rank Linguistic Features project.

The purpose of this stage was to test whether the unsupervised SAE dictionary contains features associated with 40 controlled linguistic variables, whether those associations generalize beyond the training examples, whether they are selective rather than generic change detectors, how they compare with earlier supervised activation probes, and whether top-ranked SAE features are actually interpretable as the intended linguistic structures.

The post-canonical analysis produced an important distinction:

```text
statistical SAE recoverability
        ≠
clean structural feature interpretation
```

---

## 1. Controlled evaluation dataset

The evaluation dataset contains:

```text
40 linguistic variables
500 contrast pairs per variable
20,000 total pairs
40,000 total sentences
```

Each pair contains:

- a `basis` sentence;
- a structurally modified `changed` sentence.

Each example also records metadata such as:

- `variable_id`
- `variable`
- `approach`
- `language`
- `surface_type`
- `contrast`
- `split`
- `marker_family`
- `lexical_domain`

The controlled dataset was **not** used to train the SAE.

It was used only after the SAE dictionary had been frozen.

---

## 2. Controlled SAE activation extraction

Every controlled sentence was passed through:

```text
facebook/xglm-564M
        ↓
hidden state index 12
        ↓
activation scale = 0.02065550797801016
        ↓
frozen canonical SAE
        ↓
fixed JumpReLU threshold = 0.11494007418131039
```

Native BatchTopK inference was not used.

The fixed-threshold SAE therefore encoded each sentence independently.

### Extraction statistics

```text
variable caches       = 40
pairs                  = 20,000
sentences              = 40,000
tokens                 = 691,959
possible truncations   = 0

mean token L0          = 295.0545
mean final-token L0    = 73.03885
```

The controlled corpus was distributionally different from the natural SAE corpus, so its mean L0 was not expected to match the natural-corpus value exactly.

The low final-token L0 was consistent with many controlled sentences ending in punctuation or other low-information final tokens.

---

## 3. Representation choices

Two SAE representations were retained:

1. **mean-pooled token activations**
2. **final-token activations**

For each basis/changed pair:

```text
delta_mean  = changed_mean  - basis_mean
delta_final = changed_final - basis_final
```

Mean pooling was later treated as the **primary representation** because:

- it was less dominated by final punctuation;
- it yielded greater cross-variable specificity;
- final-token candidates showed substantially more feature reuse across variables.

Final-token results were retained as secondary evidence and for comparison with earlier probe conventions.

---

## 4. Feature-wide association analysis

For every variable and every one of the 16,384 SAE features, a paired normalized effect was calculated.

The primary statistic was:

```text
effect_j =
mean(delta_j)
/
sqrt(mean(delta_j^2))
```

where:

```text
delta_j = changed activation_j - basis activation_j
```

This statistic is bounded between `-1` and `1` and naturally penalizes effects that appear only in a small fraction of pairs.

Additional descriptive statistics included:

- mean signed delta;
- Cohen's paired `d_z`;
- positive-direction fraction;
- negative-direction fraction;
- nonzero fraction;
- dominant-direction fraction.

Candidate ranking used the **training split only**.

For each variable and pooling representation, the top 25 features by absolute training effect were retained.

This produced:

```text
40 variables
× 2 pooling representations
× 25 candidate features
= 2,000 candidate rows
```

---

## 5. Initial train / validation / test generalization

The highest-ranked training feature was first inspected descriptively on validation and test.

Many variables showed strong same-direction generalization.

However, several top-1 features reversed or weakened substantially on held-out data.

This motivated retaining the full top-25 candidate set rather than treating rank 1 as the final feature.

The later corrected-null analysis showed that weaker training-ranked candidates often generalized more reliably than the top-ranked feature.

---

## 6. Paired sign-flip null testing

Because each variable searched over 16,384 features, ordinary per-feature significance would have been misleading.

A paired sign-flip permutation null was therefore used.

Within each permutation, every basis/changed pair was randomly assigned a sign:

```text
+delta
or
-delta
```

This is equivalent to randomly swapping basis and changed labels within pairs.

For every permutation, the maximum absolute effect across **all 16,384 SAE features** was recorded.

The resulting max-statistic null controls feature-search multiplicity within each variable/pooling analysis.

### Parameters

```text
permutations = 2,000
seed         = 42
```

The minimum empirical p-value was:

```text
1 / 2001 ≈ 0.00050
```

### Survival rule

A first-stage candidate was considered fully surviving when:

1. it was significant under the train max-statistic null;
2. validation preserved the train effect direction;
3. test preserved the train effect direction.

### Result

All 40 variables had at least one top-25 candidate that satisfied these conditions in at least one pooling representation.

This established **broad SAE recoverability**.

However, this did not establish that those features specifically represented the intended linguistic structure.

---

## 7. Feature reuse and cross-variable specificity

The next analysis asked whether candidate features were specific to the target variable or were generic features reused by many transformations.

This was necessary because several feature IDs appeared repeatedly among top-ranked candidates.

Final-token features showed especially high reuse.

Examples included features such as:

- `8182`
- `9465`
- `164`
- `15059`
- `14004`
- `9622`
- `14795`
- `5159`

Some final-token features appeared among the top-25 candidates for roughly half of the 40 variables.

This indicated that final-token features often captured broad/shared properties rather than individual linguistic variables.

---

## 8. Specificity metrics

For each candidate feature, the target variable's training effect was compared with that feature's effects across all 40 variables.

Metrics included:

- target rank among the 40 variables;
- target effect magnitude;
- maximum non-target effect magnitude;
- specificity ratio against the strongest non-target variable;
- target-vs-other margin;
- z-score relative to other variables;
- target share of the feature's total absolute association.

Candidate selection for the specificity stage used:

1. training max-statistic significance;
2. validation same-direction survival;
3. training cross-variable specificity.

**Test performance was not used for this feature-selection step.**

---

## 9. Mean pooling as the primary representation

The specificity analysis showed that mean-pooled features were generally more target-specific than final-token features.

For many variables, the selected mean-pooled feature was the feature's strongest-associated variable among all 40.

Examples of strong specificity included:

```text
variable 10:
feature 6125
specificity rank = 1 / 40
specificity ratio ≈ 5.11

variable 13:
feature 9749
specificity rank = 1 / 40
specificity ratio ≈ 2.89

variable 19:
feature 6062
specificity rank = 1 / 40
specificity ratio ≈ 3.53

variable 37:
feature 2081
specificity rank = 1 / 40
specificity ratio ≈ 2.77
```

Mean pooling was therefore frozen as the **primary SAE representation** for the variable-evidence analysis.

Final-token results remain useful secondary evidence.

---

## 10. Held-out marker-family and lexical-domain robustness

The controlled dataset was deliberately structured so that marker families and lexical domains were held out across splits.

For almost every variable:

```text
validation:
  unseen marker families ≥ 1
  unseen lexical domains = 2

test:
  unseen marker families ≥ 2
  unseen lexical domains = 3
```

Some variables had even more unseen marker families.

This provided a meaningful out-of-construction test.

The selected SAE feature for each variable was evaluated separately across:

- marker families;
- lexical domains;
- train;
- validation;
- test.

Only metadata groups with at least five examples were included in the subgroup-direction summaries.

---

## 11. Subgroup robustness findings

The held-out subgroup analysis separated variables sharply.

Some selected mean-pooled features preserved direction across every eligible unseen marker family and lexical domain.

Others preserved the overall test direction but failed on individual construction groups.

Still others reversed completely on held-out constructions.

Examples of strong construction robustness included:

- variable 4 — case marking;
- variable 5 — morphosyntactic alignment;
- variable 8 — causativity / valency change;
- variable 10 — morphological segmentation type;
- variable 13 — cumulative exponence;
- variable 16 — gender / noun class;
- variable 20 — pronoun richness / reduction;
- variable 21 — possession / alienability;
- variable 27 — mirativity / stance;
- variable 30 — conditional / counterfactual marking;
- variable 31 — subordination / embedding;
- variable 32 — quotation / reported speech;
- variable 38 — speech-act force / request directness.

Examples of clearly unstable mean-pooled results included:

- variable 1;
- variable 3;
- variable 15;
- variable 22;
- variable 23;
- variable 26;
- variable 33;
- variable 40.

---

## 12. Descriptive SAE evidence tiers

The primary mean-pooled selected feature for each variable was summarized using descriptive evidence tiers.

The tiers were **not additional hypothesis tests**.

They were used to summarize several already-computed properties.

### Tier A

The feature:

- preserved direction on held-out test;
- preserved direction across all eligible held-out marker families;
- preserved direction across all eligible held-out lexical domains;
- was the strongest-associated variable for that feature among all 40 variables.

### Tier B1

The feature showed complete construction robustness but was shared / non-specific across variables.

### Tier B2

The feature preserved the overall held-out direction and showed substantial, but incomplete, construction robustness.

### Tier C

The overall held-out direction survived, but construction-level robustness was poor.

### Tier D

The selected feature was unstable on the held-out test.

---

## 13. SAE evidence-tier results

The final tier counts were:

```text
Tier A  = 11
Tier B1 = 2
Tier B2 = 16
Tier C  = 3
Tier D  = 8
```

Thus:

```text
A/B evidence = 29 / 40 = 72.5%
overall held-out direction preserved = 32 / 40 = 80%
```

The Tier-D variables were:

```text
1, 3, 15, 22, 23, 26, 33, 40
```

Tier-C variables were:

```text
2, 17, 24
```

---

## 14. Tier-A variables

The eleven Tier-A variables and initially selected features were:

```text
04 → 13269   case marking
10 → 6125    morphological segmentation type
13 → 9749    redundancy / cumulative exponence
16 → 5205    gender / noun class
20 → 7551    pronoun richness and reduction
21 → 9576    possession and alienability
27 → 1887    mirativity / stance / affect
30 → 15951   conditional / counterfactual marking
31 → 7643    subordination and embedding
32 → 1754    quotation / reported speech
38 → 3396    speech-act force / request directness
```

At this stage these were statistically strong candidates only.

They were **not yet interpreted as confirmed structural SAE features**.

---

## 15. Supervised probe ↔ SAE comparison

The SAE results were compared with the earlier supervised activation-probe pipeline.

A direct apples-to-apples comparison retained:

```text
XGLM layer 12
mean-pooled representation
basis → changed delta direction
```

The original probe evidence pipeline was also retained as a stricter multi-level measure.

The strict probe-core definition required Levels 1, 3, and 4 to pass in every available seed.

Learned activation-direction viability was recorded separately and **was not treated as an explicit pass/fail barrier**.

Three probe seeds were available:

```text
42
1
2
```

---

## 16. Probe ↔ SAE result

The 40 variables separated into four groups:

```text
Probe robust + SAE strong        = 23
Probe not robust + SAE strong    = 6
Probe robust + SAE weak          = 3
Both weak / unstable             = 8
```

Where:

```text
SAE strong = Tier A, B1, or B2
```

and:

```text
probe robust = Levels 1, 3, and 4 pass in all 3 available seeds
```

---

## 17. Convergent variables

The 23 variables with robust probe evidence and strong SAE evidence were:

```text
04
05
06
07
08
09
10
11
14
16
18
19
20
21
25
27
28
29
30
32
34
35
36
```

These provide convergent evidence that the corresponding controlled distinction is both linearly recoverable and associated with sparse SAE structure.

---

## 18. SAE-strong / probe-nonrobust variables

Six variables had strong SAE evidence but did not satisfy the strict probe criterion across all three seeds:

```text
12
13
31
37
38
39
```

This does not mean the supervised layer-12 signal was absent.

Several retained substantial layer-12 delta-probe AUROC:

```text
12 → 0.724
13 → 0.785
37 → 0.750
38 → 0.907
39 → 0.731
```

These cases are better interpreted as:

```text
substantial representational signal
+
failure of the stricter multi-level / cross-seed probe criterion
```

rather than simple "probe failures."

---

## 19. Probe-robust / SAE-weak variables

Three variables had robust supervised-probe evidence but weak or unstable SAE evidence:

```text
01
17
22
```

These cases are consistent with information being linearly recoverable from the residual stream without being cleanly isolated into one stable sparse SAE feature.

They are particularly relevant to the distinction between:

```text
distributed recoverability
and
single-feature sparse representation
```

---

## 20. Weak / unstable under both methods

Eight variables were weak or unstable under both the strict probe criterion and SAE evidence tiers:

```text
02
03
15
23
24
26
33
40
```

These variables provide relatively little evidence for a stable representation under the current experimental setup.

This does not establish absence of representation in the model in general.

Possible explanations include:

- representation at another layer;
- distributed representation;
- construction sensitivity;
- dataset limitations;
- weak contrast design;
- tokenization effects;
- insufficient SAE feature alignment.

---

## 21. Probe ↔ SAE agreement statistics

The binary strong/weak comparison produced:

```text
agreement       = 0.775
Jaccard         = 0.719
Cohen's kappa   = 0.480
odds ratio      = 10.222
Fisher p        = 0.007012
```

The corresponding contingency table was:

| | SAE strong | SAE weak |
|---|---:|---:|
| Probe robust | 23 | 3 |
| Probe not robust | 6 | 8 |

The Fisher exact result is supportive evidence that the two representational methods are associated.

Because both methods use the same underlying controlled dataset, this should be interpreted as a descriptive/supporting comparison rather than completely independent confirmation.

---

## 22. Why feature inspection was necessary

Up to this point, the SAE analysis established that many linguistic contrasts were:

- recoverable;
- significant after corrected feature search;
- generalizing across train/validation/test;
- sometimes selective across variables;
- sometimes robust across unseen constructions.

However, none of those tests answer the most important interpretability question:

```text
What does the SAE feature actually activate on in natural text?
```

A feature can distinguish a controlled linguistic contrast because of:

- one repeated token;
- punctuation;
- language identity;
- morphology specific to one language;
- lexical content;
- tokenization boundaries;
- template structure.

For this reason, the eleven Tier-A features were subjected to top-activating-example inspection.

---

## 23. Feature-inspection procedure

The original natural SAE training corpus was temporarily restored.

For each of the eleven Tier-A features, the analysis collected the strongest natural-text examples according to maximum token activation within each sentence.

The controlled 40-variable dataset was inspected in parallel.

For every selected feature, the analysis retained:

- top natural examples;
- activation magnitude;
- maximally activating token;
- token position;
- available natural-corpus metadata;
- top controlled examples;
- controlled target-variable fraction.

The natural corpus used for inspection was the same broad corpus used to train the SAE rather than the synthetic controlled feature dataset.

This was essential for detecting shallow synthetic artifacts.

---

## 24. Feature-inspection overview

The quantitative Tier-A status did **not** generally survive semantic interpretation.

Several statistically excellent features were dominated by shallow lexical, language, punctuation, or tokenization patterns.

This substantially changed the interpretation of the SAE results.

---

## 25. Variable 4 — case marking — feature 13269

Natural top activations included tokens such as:

```text
ülke
parti
```

and nominal material in multiple languages.

The examples contained potentially case-marked nominals, but the feature did not cleanly isolate case morphology.

Inspection verdict:

```text
mixed_not_confirmed
```

Interpretation:

The feature is quantitatively selective for the controlled case-marking variable but the natural examples do not establish that it represents grammatical case itself.

Alternative surviving candidates should be inspected before causal use.

---

## 26. Variable 10 — morphological segmentation — feature 6125

Natural activation was strongly dominated by Turkish lexical/tokenization patterns, particularly:

```text
İstanbul
```

and a small number of Turkish token forms.

The controlled target fraction among the top 50 controlled examples was:

```text
0%
```

Inspection verdict:

```text
surface_artifact
```

Interpretation:

Feature 6125 appears substantially closer to a Turkish lexical or tokenization feature than a language-general morphological-segmentation feature.

---

## 27. Variable 13 — cumulative exponence — feature 9749

Natural top activations were overwhelmingly dominated by the Spanish token:

```text
para
```

The top natural examples repeatedly activated on the same lexical token across otherwise unrelated sentences.

The controlled target fraction among the top examples was:

```text
0%
```

Inspection verdict:

```text
surface_artifact
```

Interpretation:

The feature is a clear lexical correlate rather than convincing evidence for redundancy / cumulative exponence.

---

## 28. Variable 16 — gender / noun class — feature 5205

This was the clearest linguistically aligned inspected feature.

Top activations included:

- Arabic feminine `ة`;
- Urdu morphology associated with feminine nouns/forms.

Examples repeatedly involved feminine referents and feminine grammatical marking.

Inspection verdict:

```text
target_aligned_language_specific
```

Interpretation:

Feature 5205 plausibly represents a grammatical-gender / feminine-class morphological pattern.

However, it is not yet evidence for a language-general gender/noun-class feature because the strongest activations are concentrated in particular languages and morphological markers.

This is currently one of the strongest candidates for deeper inspection and possible later causal work.

---

## 29. Variable 20 — pronoun richness / reduction — feature 7551

Natural top examples were dominated by the Chinese third-person pronoun:

```text
他
```

The feature is therefore genuinely pronoun-related, but mostly at a lexical / language-specific level.

Inspection verdict:

```text
partial_target_alignment_lexical
```

Interpretation:

The feature supports sensitivity to pronouns but does not establish a representation of the broader typological variable "pronoun richness and reduction."

Alternative candidates should be inspected.

---

## 30. Variable 21 — possession / alienability — feature 9576

Natural top examples were dominated by:

```text
letzten
letzte
last
dernière
```

and similar lexical material related to "last."

This pattern has no clear relationship to possession or alienability.

Inspection verdict:

```text
surface_artifact
```

Interpretation:

The quantitative association does not survive natural-text interpretation.

Alternative candidates are required.

---

## 31. Variable 27 — mirativity / stance / affect — feature 1887

Natural examples were heavily concentrated in Japanese.

The maximally activating tokens were often punctuation:

```text
、
。
```

Some of the top contexts did contain surprise or mirative content, for example statements equivalent to:

- "it is surprising";
- "I was amazed";
- unexpected discoveries.

However, the feature is strongly entangled with Japanese sentence-final punctuation and language identity.

Inspection verdict:

```text
mixed_language_punctuation
```

Interpretation:

There may be genuine semantic overlap with mirativity, but feature 1887 cannot currently be interpreted as a clean mirativity feature.

Alternative candidates should be inspected.

---

## 32. Variable 30 — conditional / counterfactual marking — feature 15951

Several natural top examples contained clear conditional, hypothetical, modal, or counterfactual structures:

```text
if ...
would have ...
could have ...
if better positioned ...
if I had reviewed ...
```

Other top examples were less clearly related.

Inspection verdict:

```text
partial_target_alignment
```

Interpretation:

Feature 15951 is a plausible broader conditional/modal feature.

It is not perfectly specific, but it is one of the strongest candidates for deeper inspection.

---

## 33. Variable 31 — subordination / embedding — feature 7643

Top natural examples were dominated by Romance-language contexts and common function words.

Many sentences were clause-rich and did include subordinate structures.

However, the maximally activating token was not consistently the embedding marker, and the feature may partly encode:

- language identity;
- frequent Romance function words;
- general clause structure.

Inspection verdict:

```text
mixed_not_confirmed
```

Interpretation:

The feature may contain syntactic signal, but the current evidence does not justify interpreting it specifically as subordination / embedding.

Alternative candidates should be inspected.

---

## 34. Variable 32 — quotation / reported speech — feature 1754

This feature was extremely target-specific in the controlled dataset.

The top natural activations were dominated by quotation-mark tokens such as:

```text
„
「
```

The controlled top-50 target-variable fraction was:

```text
100%
```

Inspection verdict:

```text
surface_target_proxy
```

Interpretation:

The feature is highly specific to quotation surface marking.

It is useful evidence that the SAE learned a sparse quotation-mark feature, but it should not be presented as evidence for a deeper representation of reported-speech structure.

This feature is especially useful as a **surface-feature control** in later experiments.

---

## 35. Variable 38 — speech-act force / request directness — feature 3396

Natural examples were dominated by lexical material corresponding to:

```text
wait
waiting
esperar
```

across multiple languages.

The pattern did not align cleanly with requests or speech-act directness.

Inspection verdict:

```text
surface_artifact
```

Interpretation:

The feature does not currently support the intended structural interpretation.

Alternative candidates should be inspected.

---

## 36. Feature-inspection summary

The eleven originally Tier-A features separated approximately as follows.

### Strongest linguistically aligned candidate

```text
5205 — gender / noun class
```

Plausible grammatical feature, but strongly language-specific.

### Plausible partial structural candidate

```text
15951 — conditional / counterfactual marking
```

Shows meaningful conditional/modal activation alongside unrelated contexts.

### Useful shallow/surface control

```text
1754 — quotation / reported speech
```

Highly specific but largely a quotation-mark detector.

### Pronoun-related but lexical

```text
7551 — pronoun richness / reduction
```

Mostly Chinese `他`.

### Mixed / not yet confirmed

```text
13269 — case marking
1887  — mirativity / stance
7643  — subordination / embedding
```

### Clear shallow/artifact-dominated candidates

```text
6125 — morphological segmentation
9749 — cumulative exponence
9576 — possession / alienability
3396 — request directness
```

---

## 37. Central methodological conclusion

The post-canonical analysis demonstrates that these statements are not equivalent:

```text
a feature discriminates a controlled contrast
```

```text
a feature survives corrected statistical testing
```

```text
a feature generalizes to held-out constructions
```

```text
a feature is specific relative to other controlled variables
```

```text
the feature represents the intended linguistic structure
```

The first four can all hold while the fifth is false.

This is a central result of the project.

---

## 38. What the SAE results currently support

The evidence supports the following claims.

### Claim 1

Low-level linguistic manipulations are broadly recoverable from XGLM internal representations.

This is supported by both supervised probes and SAE latent associations.

### Claim 2

Sparse SAE features often capture information correlated with the controlled linguistic variables.

A large majority of variables produced statistically surviving SAE candidates.

### Claim 3

Supervised probes and SAE evidence agree substantially but not perfectly.

The strong/weak classification agreed on:

```text
31 / 40 variables = 77.5%
```

### Claim 4

Sparse recoverability is not equivalent to clean mechanistic interpretation.

Top-activating natural examples revealed that many highly ranked SAE features were shallow proxies.

### Claim 5

Human or automated feature inspection is necessary before causal intervention.

Ablating or steering an artifact-dominated feature and labeling it by the controlled variable would produce misleading mechanistic conclusions.

---

## 39. What the results do not currently support

The current evidence does **not** justify claiming that:

- all 40 linguistic variables correspond to distinct SAE features;
- the 11 Tier-A features are clean structural linguistic features;
- the identified features are language-general;
- SAE feature association implies causal involvement;
- the feature labels inferred from the controlled dataset are necessarily the true semantic meanings of those features.

Those stronger claims require additional inspection and causal testing.

---

## 40. Recommended next step before ablation

The immediate next stage should **not** be blind ablation of the eleven original Tier-A features.

Instead:

1. take each variable whose selected feature was artifact-dominated;
2. return to the already-surviving top-25 candidate set;
3. inspect alternative candidates that:
   - passed the corrected train null;
   - generalized on validation;
   - generalized on test;
   - showed good cross-variable specificity;
4. inspect their top natural activations;
5. retain only candidates whose natural behavior agrees with the intended linguistic interpretation.

This can be done without retraining the SAE.

---

## 41. Causal-validation candidate roles

Based on the current inspection:

### Candidate for deeper structural inspection

```text
feature 5205
target: gender / noun class
```

### Candidate for deeper structural inspection

```text
feature 15951
target: conditional / counterfactual marking
```

### Surface-feature control

```text
feature 1754
target proxy: quotation marking
```

The quotation feature is useful precisely because it is shallow and interpretable.

It can serve as a positive control demonstrating what causal manipulation of an obvious surface feature looks like.

---

## 42. Ablation stage

Once genuinely interpretable candidates have been identified, ablation can test whether removing the relevant SAE feature weakens:

- representation of the controlled contrast;
- downstream discrimination;
- model behavior associated with the feature.

Ablation should include matched controls such as:

- random SAE features;
- firing-frequency-matched features;
- norm-matched decoder directions;
- features associated with unrelated linguistic variables.

---

## 43. Steering stage

Steering should test whether increasing or decreasing selected SAE features produces predictable directional changes.

Potential interventions include:

- adding the decoder direction;
- suppressing latent activation;
- increasing latent activation;
- basis → changed direction intervention;
- changed → basis direction intervention.

Steering should only be interpreted linguistically when feature inspection already supports that interpretation.

---

## 44. Behavioral evaluation stage

Behavioral evaluation remains separate from the controlled representational dataset.

The controlled feature dataset asks:

```text
Can the structural distinction be represented or recovered?
```

Behavioral evaluation asks:

```text
Does that structural distinction affect model outputs or decisions?
```

Potential downstream behaviors include:

- uncertainty expression;
- deference to authority;
- responsibility attribution;
- truth framing;
- refusal behavior;
- instruction following;
- sensitivity to evidential cues;
- social pressure;
- perspective anchoring.

These evaluations require a separate behavioral dataset rather than reusing the representational feature pairs as outcome tasks.

---

## 45. Main post-canonical conclusion

The post-canonical stage produced a more nuanced result than simple feature discovery.

A substantial majority of the 40 controlled linguistic variables are recoverable both through supervised probes and sparse SAE activations.

Sparse representations frequently generalize across held-out examples and even across unseen marker families and lexical domains.

However, inspection of top-activating natural examples shows that many statistically strong SAE candidates correspond to shallow correlates such as:

- lexical tokens;
- punctuation;
- language identity;
- morphology specific to one language;
- tokenization patterns.

Therefore:

```text
recoverability is strong evidence that information is present
```

but:

```text
recoverability alone is not evidence that a sparse latent
is the intended abstract linguistic feature
```

The next phase of the project must therefore combine alternative-feature inspection with causal intervention rather than treating the highest-ranked SAE latent as automatically interpretable.

---

## 46. Important post-canonical artifacts

The compact analysis evidence includes:

### Controlled SAE extraction

- `cache_manifest.json`

### Feature ranking

- `candidate_features.csv`
- `best_features.csv`
- `analysis_manifest.json`

### Null testing

- `null_tested_candidates.csv`
- `null_tested_top_features.csv`
- `null_test_manifest.json`

### Cross-variable specificity

- `cross_variable_specificity.csv`
- `feature_reuse.csv`
- `trainval_selected_features.csv`
- `specificity_manifest.json`

### Construction robustness

- `dataset_group_structure.csv`
- `subgroup_robustness_detail.csv`
- `subgroup_robustness_summary.csv`
- `subgroup_robustness_manifest.json`

### SAE evidence synthesis

- `sae_variable_evidence.csv`
- `sae_variable_evidence_summary.json`

### Probe comparison

- `probe_sae_comparison.csv`
- `probe_sae_comparison_summary.json`
- `probe_sae_agreement_summary.json`

### Feature inspection

- `natural_top_activations.jsonl`
- `controlled_top_activations.jsonl`
- `feature_inspection_summary.csv`
- `inspection_manifest.json`
- `feature_inspection_verdicts.csv`
- `feature_inspection_verdicts.json`

---

## 47. Relevant post-canonical scripts

The post-canonical analysis is implemented by:

- `cache_feature_sae_activations.py`
- `analyze_linguistic_features.py`
- `run_feature_nulls.py`
- `analyze_cross_variable_specificity.py`
- `analyze_subgroup_robustness.py`
- `summarize_sae_variable_evidence.py`
- `compare_probe_sae.py`
- `summarize_probe_sae_agreement.py`
- `inspect_sae_features.py`

---

## 48. Status

The **representational-analysis and first-pass feature-inspection stage is complete**.

The next experimental work is:

```text
alternative candidate inspection
        ↓
ablation
        ↓
steering
        ↓
behavioral evaluation
```

The canonical SAE remains frozen throughout these stages.
