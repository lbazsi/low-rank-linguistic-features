# Low-Rank Linguistic Features

This project studies whether structural linguistic features are represented inside language models in ways that can be discovered, measured, and causally tested.

The core hypothesis is that linguistic structure is not only a surface property of prompts. Features such as evidentiality, modality, negation, agent prominence, social deixis, discourse relations, and speech-act force may shape how models internally represent uncertainty, responsibility, authority, truth, obligation, and perspective.

The project builds a controlled mechanistic pipeline for identifying these structures in model activations, comparing raw activation probes with sparse autoencoder features, and testing whether candidate features affect downstream behavior through ablation and steering.

## Research Question

Can structural linguistic variables be recovered from language-model activations, represented by sparse autoencoder latents or feature clusters, and causally linked to behaviorally meaningful changes in model outputs?

The project focuses on four linked questions:

1. Are structural linguistic variables linearly or nonlinearly recoverable from internal activations?
2. Do sparse autoencoders expose interpretable features or feature clusters corresponding to these variables?
3. Are the recovered features robust across surface forms, languages, and lexical content?
4. Do interventions on these features change model behavior in predictable ways?

## Typological Basis

The feature inventory is grounded in the typological orientation of **The World Atlas of Language Structures Online (WALS)**. WALS organizes cross-linguistic structural variation across domains such as morphology, nominal categories, verbal categories, word order, simple clauses, complex sentences, lexicon, and writing systems.

The project does not directly copy WALS chapters. Instead, it adapts typological categories into an experimental feature map for mechanistic interpretability.

Recommended general citation:

> Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013. **WALS Online (v2020.4)** [Data set]. Zenodo. https://doi.org/10.5281/zenodo.13950591. Available online at https://wals.info.

The current feature map contains forty structural variables, including subject expression, constituent order, case marking, agreement, evidentiality, modality, negation, discourse relations, topic-comment structure, social deixis, speech-act force, and orthographic/tokenization effects.

See `List of features.md` for the full feature map.

## Methodological Basis

The project is methodologically inspired by:

> Brinkmann, J., Wendler, C., Bartelt, C., & Mueller, A. (2025). **Large Language Models Share Representations of Latent Grammatical Concepts Across Typologically Diverse Languages.** *Proceedings of NAACL 2025*. arXiv:2501.06346.  
> https://arxiv.org/abs/2501.06346

That work trains sparse autoencoders on multilingual language-model activations, identifies latent grammatical features such as number, gender, and tense, and validates candidate features through causal interventions. This project adapts the same broad methodological pattern to a wider WALS-aligned feature map, including structural variables such as evidentiality, modality, agent prominence, negation, topic-comment structure, social deixis, discourse relations, and speech-act force.

## Dataset Strategy

The project uses a controlled **feature dataset** organized around contrast pairs. Each example contains a basis sentence and a changed sentence. The pair changes one target structural property while keeping surrounding meaning as stable as possible.

Example schema:

```json
{
  "id": "26_001",
  "variable_id": 26,
  "variable": "evidentiality",
  "approach": "EN+XL",
  "language": "tr",
  "surface_type": "xl",
  "contrast": "direct_to_reported",
  "split": "train",
  "pair": [
    {
      "type": "basis",
      "sentence": "..."
    },
    {
      "type": "changed",
      "sentence": "..."
    }
  ]
}
```

The default split structure is:

```text
001-400 = train
401-450 = val
451-500 = test
```

For variables with 500 examples, this gives an 80/10/10 train/validation/test split. Splits are kept explicit in the data even when they can be derived from the ID.

The feature dataset is separate from the SAE training corpus. The feature dataset is controlled, labeled, and variable-specific. The SAE corpus is broad natural text used to train sparse autoencoders on a less artificial activation distribution.

See `Feature dataset construction.md` for the full language and dataset-construction strategy.

## Language Strategy

The experiment uses a compact multilingual pool:

- English
- Turkish
- Japanese
- Korean
- Spanish
- Russian
- Arabic
- Mandarin Chinese

Each variable is assigned one of four construction approaches:

| Label | Meaning |
|---|---|
| `EN` | English templates are sufficient. |
| `EN+ctrl` | English is usable, but controlled templates or lexical substitutions are needed. |
| `XL` | English underdetermines the feature; use one selected non-English language. |
| `EN+XL` | English gives a partial contrast; the full structural contrast uses one selected non-English language. |

For simplicity and interpretability, each `XL` or `EN+XL` variable uses at most one non-English language. This avoids mixing too many confounds inside a single variable, such as script, tokenization, morphology, model familiarity, and corpus quality.

## Models

The initial experiments use two complementary models.

### Pythia-70M-deduped

`EleutherAI/pythia-70m-deduped` is used as the small English-first interpretability sandbox.

Its role is to test the full pipeline cheaply:

- controlled feature examples;
- activation extraction;
- all-layer scanning;
- sparse autoencoder training;
- raw activation probes;
- SAE latent probes;
- feature ranking;
- ablation;
- steering;
- result formatting.

Because the model is small, it is practical to scan most or all layers and debug the full pipeline before scaling to larger or multilingual models.

### XGLM-564M

`facebook/xglm-564M` is used as the first multilingual causal language model.

Its role is to test whether the same pipeline can recover structural features across the project’s multilingual feature set. This is especially important for variables that are absent, weak, or structurally underdetermined in English, such as evidentiality, pro-drop, honorifics, topic-comment structure, rich case marking, gender agreement, and Mandarin-style tense optionality.

The two-model setup separates pipeline validation from multilingual representational claims:

```text
Pythia-70M-deduped = cheap pipeline validation and English controls
XGLM-564M = multilingual structural feature discovery
```

## Methodology

### 1. Controlled Feature Construction

For each linguistic variable, the project constructs contrast pairs. Each pair contains a basis sentence and a changed sentence. The contrast label records the structural change, such as:

```text
direct_to_reported
active_to_passive
assertion_to_request
obligation_to_permission
definite_to_indefinite
affirmed_to_negated
```

The goal is not to make the model recognize individual trigger words. The goal is to test whether broader structural distinctions are represented internally.

### 2. Activation Collection

The controlled feature dataset and broad background text are passed through each model using forward passes. The model weights are not updated. During these forward passes, activations are cached from selected internal sites, especially residual-stream positions across layers.

For small models, the project caches activations from all or nearly all layers. This allows the analysis to test where each linguistic variable is most recoverable, rather than assuming that foundational linguistic features are localized to one or two specific layers.

### 3. SAE Training

Sparse autoencoders are trained on natural-text activations. The SAE corpus is separate from the feature dataset to avoid training the autoencoder only on artificial contrast examples.

The project may train separate SAEs by model and activation site. For multilingual experiments, the SAE corpus should cover every language used in controlled feature probes.

### 4. Probing

The project trains simple probes on both raw activations and SAE latents.

Probe targets include:

- basis vs changed classification;
- variable-specific contrast detection;
- language-specific and cross-language recoverability;
- layer-wise feature localization;
- raw activation vs SAE-latent performance.

Probe results are not treated as causal evidence by themselves. They are used to identify where a feature may be represented and which layers or SAE latents are worth inspecting further.

### 5. Feature Ranking

Candidate SAE features are ranked using contrast-pair activation differences, probe relevance, top-activating examples, and robustness across surface forms.

For each variable, the project records whether the signal appears to be:

- concentrated in a small number of features;
- distributed across feature clusters;
- stronger in raw activations than SAE latents;
- stronger in SAE latents than raw activations;
- language-specific;
- stable across layers;
- dependent on shallow lexical artifacts.

### 6. Feature Inspection

Top-activating examples are inspected to determine whether candidate features track the intended linguistic structure or merely respond to repeated words, punctuation, templates, or tokenization artifacts.

This step is especially important for variables such as evidentiality, negation, modality, and social deixis, where shallow surface markers can easily masquerade as structural features.

### 7. Ablation

Candidate SAE features or feature clusters are ablated to test whether removing them weakens representation of the target variable or changes downstream model behavior.

Ablation is used to distinguish correlational recoverability from causal involvement.

### 8. Steering

Candidate features are steered to test whether increasing or decreasing them changes model outputs in predictable ways.

Possible steering targets include:

- uncertainty expression;
- deference to authority;
- responsibility attribution;
- truth-framing;
- refusal behavior;
- instruction-following;
- sensitivity to evidential cues;
- sensitivity to social pressure;
- perspective anchoring.

### 9. Behavioral Evaluation

The behavioral evaluation dataset tests whether structural linguistic changes affect model outputs.

The feature dataset asks:

```text
Can the structure be represented or recovered?
```

The behavioral evaluation asks:

```text
Does the structure affect model behavior?
```

Behavioral evaluations are kept separate from the controlled feature dataset because they measure downstream output effects rather than representational recoverability.

## Repository Structure

Recommended project structure:

```text
data/
  feature_dataset/
    variable_01_subject_expression/
    variable_02_constituent_order/
    ...
    variable_40_orthographic_tokenization/

  sae_corpus/
    raw/
    processed/
    metadata.yaml

  behavioral_eval/
    uncertainty/
    deference/
    responsibility_attribution/
    truth_framing/
    refusal_stability/
    social_pressure/
    authority_sensitivity/

artifacts/
  activation_cache/
    feature_dataset/
    behavioral_eval/

  probe_data/
    raw_activation_probes/
    sae_latent_probes/

  trained_saes/
  trained_probes/

  results/
    feature_rankings/
    ablations/
    steering/
    behavioral_eval/
```

Stable, manually constructed datasets belong in `data/`. Generated outputs, caches, trained models, and experiment results belong in `artifacts/`.

## Expected Outputs

The project is designed to produce:

- a controlled feature dataset for structural linguistic variables;
- a broad multilingual SAE corpus;
- a behavioral evaluation dataset;
- activation caches across layers and models;
- trained sparse autoencoders;
- raw-activation and SAE-latent probe results;
- ranked candidate features for each variable;
- top-activating example analyses;
- ablation results;
- steering results;
- behavioral evaluation results.

## Research Contribution

A successful result would show that at least some structural linguistic variables are:

- recoverable from model activations;
- represented in sparse latent features or feature clusters;
- partially robust across surface forms and languages;
- causally involved in model predictions or generations;
- relevant to alignment-adjacent behaviors such as uncertainty, deference, refusal stability, and truth-framing.

The long-term motivation is to build an empirical foundation for Constitutional Language research: studying whether deliberately structured languages or intermediate representations can make model behavior more stable, transparent, and less sensitive to framing, social pressure, hidden assumptions, or linguistic bias.
