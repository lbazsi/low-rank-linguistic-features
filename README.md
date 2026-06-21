# Low-Rank Linguistic Features

This project investigates whether low-level structural linguistic features are represented inside language models in ways that are discoverable, measurable, and causally relevant to model behavior.

Rather than treating linguistic structure as a surface property of prompts, the project studies whether grammatical and quasi-grammatical variables such as evidentiality, agency marking, authority/status marking, and negation correspond to internal representational features. The central hypothesis is that such features can influence model behavior, including deference, uncertainty, attribution of responsibility, truth-framing, and response style.

## Research Goal

The goal is to build an exploratory mechanistic pipeline for identifying linguistic features that may later inform the design of Constitutional Languages: deliberately structured languages or intermediate representations intended to make model behavior more stable, transparent, and less sensitive to harmful framing effects.

The project focuses on four initial feature families:

1. **Evidentiality**  
   How information source is marked, such as direct observation, report, inference, hearsay, or uncertainty.

2. **Agency and responsibility marking**  
   How syntax encodes who caused an event, including active voice, passive voice, agent deletion, and impersonal constructions.

3. **Status and authority marking**  
   How linguistic markers encode social rank, expertise, politeness, institutional authority, or deference pressure.

4. **Negation and truth-framing**  
   How statements are framed through negation, denial, contradiction, uncertainty, or indirect truth claims.

These features are intentionally messier than standard grammatical categories such as number, tense, or gender. The project starts with the difficult cases because they are closer to the behavioral phenomena relevant for alignment research.

## Methodological Basis

The project adapts methods from sparse-autoencoder-based interpretability work on grammatical representations in language models. The methodological skeleton is:

- collect controlled linguistic datasets using minimal-pair and counterfactual templates;
- run a pretrained language model and cache internal activations;
- train sparse autoencoders on selected residual stream activations;
- identify SAE features associated with the target linguistic variables;
- train probes over both raw activations and SAE latents;
- rank and inspect candidate features;
- perform ablation and steering interventions;
- measure whether interventions affect downstream behavior.

The project does not aim to exactly replicate previous grammatical-feature experiments. Instead, it uses their mechanistic methodology as a foundation for studying alignment-relevant structural linguistic variables.

## Main Outputs

This repository is intended to produce a reusable research resource consisting of:

- controlled datasets for the four target feature families;
- minimal pairs and counterfactual examples for linguistic-structure interventions;
- activation caches from small pretrained language models;
- trained sparse autoencoders for selected model layers;
- feature rankings for each linguistic variable;
- probe results over raw activations and SAE latents;
- top-activating examples for candidate features;
- ablation and steering results;
- behavioral evaluations showing whether feature interventions change model outputs;
- documentation of failure modes and artifact controls.

The end product is not only a set of experimental results, but also a reusable pipeline for testing additional linguistic variables.

## Intended Research Contribution

The project asks whether structural linguistic features can be treated as mechanistic objects inside language models.

A successful result would show that some linguistic variables are:

- linearly or sparsely recoverable from internal activations;
- represented by interpretable SAE features or feature clusters;
- robust across lexical templates and notation systems;
- causally involved in model predictions or generated behavior;
- useful for designing later controlled language or representation systems.

This would support future research into Constitutional Languages by identifying which linguistic structures are promising candidates for deliberate design and which are likely too entangled, distributed, or behaviorally weak.

## Initial Experimental Scope

The first phase focuses on small pretrained language models, such as Pythia-style models, and a small number of residual-stream layers.

The initial experimental loop is:

1. Generate controlled examples for evidentiality, agency, status, and negation.
2. Cache model activations on these examples and on broad background text.
3. Train sparse autoencoders on selected activation sites.
4. Train probes to test whether the variables are represented.
5. Identify candidate SAE features associated with each variable.
6. Inspect top-activating examples for interpretability.
7. Ablate candidate features and measure changes in probe or model behavior.
8. Steer candidate features and test whether outputs shift in the expected direction.

## Artifact Controls

Because the target variables are subtle and behaviorally loaded, the project emphasizes controls against shallow artifacts.

Planned controls include:

- held-out lexical templates;
- held-out surface markers;
- multiple notation systems for each variable;
- token-level and bag-of-words baselines;
- random-feature ablation baselines;
- comparison between raw-activation probes and SAE-latent probes;
- behavioral evaluations that separate surface imitation from genuine representational effects.

The goal is not merely to show that a model detects words such as "reportedly" or "authority." The goal is to test whether broader structural patterns are represented and causally usable.

## Long-Term Role in Constitutional Language Research

This project is the first empirical layer in a larger research program on Constitutional Language.

Future projects can use this resource to:

- expand the feature set beyond the initial four cases;
- compare different model scales and architectures;
- test whether linguistic features compose linearly or interfere with each other;
- study whether structural language design can reduce framing sensitivity;
- build controlled artificial or semi-artificial languages;
- evaluate whether constitutional representations improve robustness, transparency, or alignment-relevant behavior.

In the long term, the project aims to help determine whether language structure itself can be engineered as part of model alignment, rather than being treated as a neutral input medium.
