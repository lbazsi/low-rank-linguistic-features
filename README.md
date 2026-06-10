# Project 1 Brief: SAE-Based Discovery of Structural Linguistic Signals in a 50M Language Model

## Working Title

**Sparse Feature Discovery of Structural Linguistic Signals in Small Language Models**

Alternative titles:

- **Mapping Structural Linguistic Features in Small Transformer Representations with Sparse Autoencoders**
- **Do Small Language Models Encode Low-Level Linguistic Structure as Sparse Features?**
- **A Pilot Study for SAE-Based Discovery of Typological Signals in Language Models**

---

## 1. Project Motivation

The broader research program asks whether structural properties of language can influence model behavior, bias, calibration, agency attribution, authority sensitivity, and eventually alignment-relevant behavior.

Before building larger experimental systems, pseudo-languages, LoRA interventions, or a constitutional language, the first necessary question is representational:

> **Are low-level structural linguistic variables visible inside a model's internal representations, and can they be identified using sparse autoencoders?**

This project tests that question in a controlled, low-compute setting using a small language model.

The goal is not to prove that all large LLMs encode language structure in the same way. The goal is to validate a pipeline:

1. Train or use a small transformer model.
2. Train layerwise sparse autoencoders on its activations.
3. Generate controlled linguistic contrast datasets.
4. Search SAE features for structural linguistic variables.
5. Test whether discovered features are interpretable, localized, and causally usable.
6. Use the result as the methodological foundation for later larger-model and intervention studies.

---

## 2. Core Research Question

### Main Question

> **Can sparse autoencoders recover low-level structural linguistic signals from the representations of a 50M parameter language model?**

### Subquestions

1. Which linguistic variables are most easily detected by SAE features?
2. Where in the model do different structural variables appear?
3. Are these variables represented sparsely or diffusely?
4. Are discovered SAE features structural, or are they merely token/string artifacts?
5. Can SAE-based interventions alter downstream model behavior?
6. Does a small model provide a useful proof-of-concept for later 1B–7B model studies?

---

## 3. Why Use a 50M Model First?

A 50M model is small enough to make the full pipeline feasible with limited compute, while still being large enough to develop nontrivial internal structure.

This scale allows:

- fast experimentation,
- cheap failed runs,
- repeated SAE training,
- layerwise analysis,
- debugging of feature discovery methods,
- controlled comparison across many linguistic variables.

The 50M model should be treated as a **method validation platform**, not as final evidence about frontier LLMs.

A good framing is:

> **This project validates whether an SAE-based pipeline can discover and intervene on structural linguistic features in a small transformer. Later work tests whether the same findings scale to larger models.**

---

## 4. High-Level Methodology

The project has six stages:

```text
50M language model
↓
activation collection across selected layers
↓
layerwise SAE training
↓
controlled linguistic contrast datasets
↓
feature discovery and localization
↓
ablation / steering / causal testing
```

The central output is a map:

```text
linguistic variable → detectable SAE features → layer location → sparsity/distribution → causal relevance
```

---

## 5. Model Setup

### Option A: Use an Existing 50M Model

This is faster and useful for pipeline validation.

Advantages:

- no model training required,
- quicker start,
- easier comparison with known model behavior.

Disadvantages:

- less control over the training distribution,
- linguistic signals may be weak or absent,
- hard to separate model-internal structure from pretraining artifacts.

### Option B: Train a 50M Model

This is more aligned with the long-term project.

Advantages:

- controlled training language,
- ability to add pseudo-English structural data,
- better link between training language and representation.

Disadvantages:

- more engineering,
- additional compute,
- need to ensure the model is competent enough for linguistic analysis.

### Recommended First Approach

Use a hybrid sequence:

1. Begin with an existing small model if available.
2. Build the SAE and linguistic analysis pipeline.
3. Then train a controlled 50M model if the first pipeline works.

If training a 50M model, use a mixture:

```text
80–90% broad English/simple text
10–20% controlled pseudo-English structural examples
```

This avoids the SAE learning only artificial tags while still exposing the model to the structures of interest.

---

## 6. SAE Setup

### What the SAE Does

A sparse autoencoder takes an internal activation vector and reconstructs it using a sparse set of learned features.

Simplified:

```text
activation x
→ encoder
→ sparse feature vector z
→ decoder
→ reconstructed activation x-hat
```

The objective is:

```text
reconstruct activation accurately
while using as few active features as possible
```

The hope is that SAE features correspond to more interpretable directions than individual neurons.

### Important Correction

Do not train one SAE on the entire “full activation space” at once.

Instead, train **one SAE per activation site**, such as:

```text
residual stream, layer 2
residual stream, layer 4
residual stream, layer 6
...
```

This gives a layerwise map of where each feature appears.

### Recommended Activation Sites

For a 12-layer-ish 50M transformer:

```text
Layer 2: early / surface features
Layer 4: early-middle
Layer 6: middle
Layer 8: middle-late
Layer 10: late
Layer 12: final / output-proximal
```

Start with residual stream activations.

Optional later:

- MLP output,
- attention output,
- pre-residual stream,
- post-residual stream.

### Recommended SAE Types

Use one of:

- **TopK SAE**
- **Gated SAE**
- **JumpReLU SAE**

For the first implementation, choose the architecture that is easiest to reproduce from existing codebases. The project should not become an SAE architecture paper.

### Suggested First SAE Sizes

For a 50M model:

```text
SAE width: 4k, 8k, or 16k features
Training tokens: 5M–50M
Layers: 3–6 layers
```

A first debugging run can be much smaller:

```text
1 layer
1M–5M tokens
4k features
```

---

## 7. Linguistic Variables to Test

The project begins from a 40-variable map of structural linguistic variables.

The full list:

1. Subject explicitness / pro-drop
2. Agent prominence / passive
3. Causativity
4. Evidentiality
5. Grammatical gender
6. Honorific/status marking
7. Word order
8. Case marking
9. Agglutinative morphology
10. Analytic vs synthetic grammar
11. Definiteness/articles
12. Number marking
13. Animacy marking
14. Person hierarchy
15. Inclusive/exclusive we
16. Genericity
17. Habitual aspect
18. Tense prominence
19. Aspect
20. Negation placement
21. Double negation
22. Quantifier scope
23. Conditionals
24. Topic-comment structure
25. Focus marking
26. Given/new marking
27. Pronoun richness/reduction
28. Formal/informal you
29. Status agreement
30. Direct/indirect request grammar
31. Motion encoding
32. Emotion grammar
33. Possession structure
34. Whitespace segmentation
35. Character vs subword units
36. Script variation
37. Punctuation structure
38. Redundancy
39. Ambiguity density
40. Optionality vs obligatoriness

### Recommended Initial Subset

Do not begin with all 40 equally.

Begin with 8:

1. Evidentiality
2. Case marking
3. Number marking
4. Tense
5. Agency / passive deletion
6. Grammatical gender
7. Status / honorifics
8. Negation

These are preferred because they are:

- easier to label,
- likely to be detectable,
- relevant to prior work,
- connected to safety-relevant behavior,
- possible to control with minimal pairs.

Then expand to the full 40 once the pipeline works.

---

## 8. Dataset Design

The analysis requires controlled contrast datasets.

Each dataset should contain:

1. positive examples,
2. negative examples,
3. minimal pairs,
4. lexical controls,
5. token controls,
6. semantic controls,
7. mixed-feature examples.

### Example: Evidentiality

```text
[SAW] Bob broke the vase.
[HEARD] Bob broke the vase.
[REPORTED] Bob broke the vase.
[INFERRED] Bob broke the vase.
[UNKNOWN] Bob broke the vase.
```

Controls:

```text
Alice saw Bob near the vase.
The word SAW appeared on the wall.
Bob reportedly broke the vase.
It was inferred that Bob broke the vase.
Someone said Bob broke the vase.
```

The key question:

> Does the SAE find a source-of-knowledge feature, or only the token `[SAW]`?

### Example: Case Marking

```text
Alice-NOM helped Bob-ACC.
Bob-ACC was helped by Alice-NOM.
Bob-NOM helped Alice-ACC.
```

Controls:

```text
Alice helped Bob.
Bob helped Alice.
Alice-NOM saw Bob-ACC.
```

The key question:

> Does the SAE represent grammatical role, or just the string `-NOM`?

### Example: Agency / Agent Deletion

```text
Alice broke the vase.
The vase was broken by Alice.
The vase was broken.
The vase broke.
```

The key question:

> Does the model separately represent agent presence, causal structure, and responsibility?

### Example: Status Marking

```text
HIGH says the answer is A.
LOW says the answer is B.
SPEAKER-HIGH tells LISTENER-LOW that X.
SPEAKER-LOW tells LISTENER-HIGH that X.
```

The key question:

> Does the model encode social hierarchy structurally, and does that affect agreement or deference?

---

## 9. Feature Discovery Pipeline

For each linguistic variable:

### Step 1: Generate Labelled Examples

Each example should have metadata:

```json
{
  "feature": "evidentiality",
  "variant": "reported",
  "sentence": "[REPORTED] Bob broke the vase.",
  "semantic_event": {
    "agent": "Bob",
    "action": "break",
    "patient": "vase",
    "source": "reported"
  }
}
```

### Step 2: Run Model and Cache Activations

Collect activations from selected layers.

Recommended initial sites:

```text
residual stream at layers 2, 4, 6, 8, 10, 12
```

### Step 3: Encode Activations Through SAE

For each activation vector:

```text
activation → SAE → sparse feature activations
```

### Step 4: Find Predictive Features

For each linguistic label, find SAE latents that distinguish variants.

Methods:

- correlation with label,
- mutual information,
- logistic regression on SAE features,
- difference in mean activation,
- top activating examples,
- sparse feature attribution.

### Step 5: Inspect Features

For each candidate feature:

- top activating examples,
- bottom activating examples,
- activation distribution,
- whether it fires across lexical variation,
- whether it fires across syntactic variation,
- whether it fires only on artificial tags.

### Step 6: Compare Against Baselines

Baselines:

- raw neuron activations,
- PCA directions,
- linear probe on raw activations,
- random SAE features,
- token-only classifier,
- bag-of-words classifier.

The SAE result is stronger if it beats or complements these baselines.

### Step 7: Causal Testing

Use interventions:

- ablate top SAE features,
- increase feature activation,
- patch features between examples,
- measure changes in model output or probe prediction.

Example:

```text
Ablate reported-evidence feature
→ does the model become less sensitive to reported vs seen evidence?
```

---

## 10. What Results to Retain

For each of the 40 variables, classify results into buckets.

### Bucket A: Clean Sparse Feature Found

A small number of SAE features reliably encode the variable.

Example:

```text
Feature 1832 activates for plural number across many nouns.
```

### Bucket B: Distributed Feature Found

The variable is detectable, but only through many weak features.

Example:

```text
Status marking is represented, but no single feature dominates.
```

### Bucket C: Probe Detects It, SAE Does Not

Raw activations contain the signal, but the SAE decomposition does not isolate it clearly.

This is still informative.

### Bucket D: Token Artifact

SAE features track a marker token or string pattern, not the structural variable.

Example:

```text
Feature fires on the literal token "-NOM" but does not generalize to other role-marking forms.
```

### Bucket E: No Detectable Signal

No reliable feature, probe, or causal effect is found.

This is also useful: it helps identify which variables may require larger models, better datasets, or different methods.

---

## 11. Core Evaluation Tables

The final report should include tables like these.

### Feature Detectability Table

| Variable | Probe Accuracy | SAE Feature Found? | Best Layer | Sparse/Distributed | Artifact Risk |
|---|---:|---|---|---|---|
| Evidentiality | 0.91 | yes | L8 | sparse | medium |
| Case marking | 0.95 | yes | L6 | sparse | high |
| Status | 0.74 | partial | L10 | distributed | medium |
| Agency deletion | 0.82 | yes | L8 | distributed | low |

### Layer Localization Table

| Variable | Early Layers | Middle Layers | Late Layers | Interpretation |
|---|---|---|---|---|
| Number | weak | strong | medium | morphosyntactic |
| Case | medium | strong | weak | role structure |
| Evidentiality | weak | medium | strong | discourse/epistemic |
| Status | weak | medium | strong | social abstraction |

### Causal Intervention Table

| Variable | Intervention | Behavioral Effect | Strength |
|---|---|---|---|
| Evidentiality | ablate source feature | lower source sensitivity | medium |
| Case | ablate role feature | more role confusion | strong |
| Status | amplify HIGH feature | more agreement with high-status source | weak/medium |

---

## 12. Possible Behavioral Tests

The SAE study should not only identify features. It should test whether some features matter behaviorally.

### Evidentiality

Prompt:

```text
[SAW] The medicine caused harm.
[REPORTED] The medicine caused harm.
[INFERRED] The medicine caused harm.
```

Measure:

- confidence,
- uncertainty,
- willingness to assert,
- source qualification.

### Agency

Prompt:

```text
Alice broke the vase.
The vase broke.
The vase was broken.
```

Measure:

- blame attribution,
- responsibility,
- causal judgment.

### Status

Prompt:

```text
HIGH says answer is A.
LOW says answer is B.
```

Measure:

- agreement with high-status source,
- contradiction handling,
- authority bias.

### Gender

Prompt:

```text
doctor-MASC helped nurse-FEM.
doctor-FEM helped nurse-MASC.
```

Measure:

- pronoun prediction,
- competence attribution,
- stereotype completion.

---

## 13. What This Project Can and Cannot Claim

### It Can Claim

- A 50M model contains detectable representations of some structural linguistic variables.
- SAEs can recover some of these variables as sparse or semi-sparse features.
- Different variables appear more strongly at different layers.
- Some features survive lexical/token controls.
- Some SAE features can be causally intervened on.
- The pipeline is suitable for scaling to larger models.

### It Should Not Claim Yet

- Large LLMs universally encode all linguistic structures in the same way.
- Language structure directly causes high-level alignment behavior.
- A constitutional language is validated.
- SAE features are complete explanations of model behavior.
- All 40 variables are equally meaningful or detectable.

---

## 14. Main Risks

### Risk 1: Token Artifacts

The SAE may learn artificial markers like `[SAW]`, `-NOM`, or `HIGH`.

Mitigation:

- multiple notations for the same feature,
- natural-language paraphrases,
- lexical controls,
- held-out marker systems.

### Risk 2: Model Too Small

A 50M model may not develop rich enough abstractions.

Mitigation:

- treat this as a pipeline pilot,
- later test 300M–1B and 7B models,
- include easy known features like number/tense as sanity checks.

### Risk 3: Too Many Variables

Testing all 40 at once may dilute the project.

Mitigation:

- start with 8,
- build infrastructure for 40,
- report full 40 only if pipeline stabilizes.

### Risk 4: SAE Instability

Different SAE runs may produce different features.

Mitigation:

- run multiple seeds on a small subset,
- use probe-level validation,
- focus on reproducible feature families.

### Risk 5: Weak Behavioral Effects

A feature may be represented but not behaviorally important.

Mitigation:

- separate representational claims from behavioral claims,
- use causal tests only for strongest features,
- leave broad behavioral mapping for later papers.

---

## 15. Minimal 2–3 Week Version

A realistic intensive sprint should aim for:

### Must Have

- one 50M model or existing small model,
- activation collection working,
- SAEs trained on 3–4 layers,
- 5–8 linguistic variables,
- labelled contrast datasets,
- feature discovery scripts,
- top-feature inspection,
- probe baselines,
- one or two causal ablation tests,
- short technical report.

### Nice to Have

- all 40 variables in dataset format,
- layerwise feature map,
- steering experiments,
- multiple SAE seeds,
- comparison to existing SAEs or larger model,
- polished paper draft.

### Not Realistic in 2–3 Weeks

- full 40-feature robust causal analysis,
- complete 7B replication,
- LoRA/ReFT intervention suite,
- constitutional language proposal,
- publication-ready full paper unless the scope is very narrow.

---

## 16. Proposed 2–3 Week Schedule

### Week 1: Infrastructure and Data

- choose model,
- implement activation caching,
- choose SAE library,
- generate datasets for 5–8 variables,
- train first SAE on one layer,
- verify reconstruction and sparsity,
- run first feature search.

### Week 2: Layerwise SAE Map

- train SAEs on 3–4 layers,
- run probes on raw activations and SAE features,
- inspect top features,
- filter out token artifacts,
- create detectability tables.

### Week 3: Causal Tests and Report

- ablate top features,
- steer selected features,
- measure behavioral/probe effects,
- write technical report,
- package code and datasets,
- decide whether to expand to 40 features or scale model size.

---

## 17. Suggested Paper Structure

### Abstract

Present the project as a pilot study using SAEs to identify structural linguistic variables in small language models.

### Introduction

Motivate the need to understand how language structure appears in model representations.

### Related Work

Cover:

- sparse autoencoders,
- multilingual morphosyntactic representations,
- probing,
- typology,
- synthetic language experiments,
- causal interventions.

### Methods

Describe:

- model,
- activations,
- SAE architecture,
- linguistic variables,
- dataset generation,
- probes,
- intervention methods.

### Results

Include:

- feature detectability,
- layer localization,
- examples of SAE features,
- artifact controls,
- ablation/steering results.

### Discussion

Explain:

- what this reveals,
- what it does not reveal,
- how it motivates larger-model work,
- how it connects to pseudo-language labs and later interventions.

### Conclusion

Frame this as the first step in a broader research program.

---

## 18. Relationship to the Broader Research Program

This first project supports the later sequence:

```text
Paper 1:
SAE discovery of structural linguistic features in small models

Paper 2:
Scaling the same discovery to larger models

Paper 3:
Controlled pseudo-language lab for manipulating structural variables during training

Paper 4:
LoRA/ReFT/activation-based interventions on linguistic structures and behavior

Final synthesis:
Constitutional language or constitutional languages as alignment-relevant training/inference media
```

The first project answers the foundational question:

> **Is there something internally measurable to manipulate later?**

If yes, the later lab and intervention work has a stronger basis.

If no, the research program still learns something important:

> Some structural linguistic variables may not be cleanly represented as sparse features in small models, and different methods may be needed.

---

## 19. Recommended First Variables

Start with these 8:

| Variable | Reason |
|---|---|
| Number | sanity check; likely detectable |
| Tense | sanity check; prior work relevance |
| Case marking | role structure; clean labels |
| Evidentiality | source tracking and calibration relevance |
| Agency/passive deletion | blame and responsibility relevance |
| Grammatical gender | bias relevance |
| Status/honorifics | authority and sycophancy relevance |
| Negation | logic and refusal relevance |

If these work, expand to the remaining 32.

---

## 20. Final Project Summary

This first project is a compact but serious mechanistic interpretability study.

It asks whether structural linguistic variables can be discovered inside a small language model using sparse autoencoders. It uses a 50M parameter model as a low-compute proof-of-concept, trains SAEs across multiple layers, evaluates 5–8 core linguistic variables first, and then expands toward a 40-variable structural map.

The most important outputs are:

1. a controlled linguistic contrast dataset,
2. trained layerwise SAEs,
3. a feature detectability map,
4. layer localization results,
5. artifact controls,
6. basic causal interventions,
7. a technical report that can become the first paper in a larger research program.

The project is valuable even if many features are not found, because it establishes which structural linguistic signals are detectable, where they appear, and which methods are suitable for future scaling.
