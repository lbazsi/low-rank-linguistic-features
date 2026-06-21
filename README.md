# Low-Rank Linguistic Features

This project investigates whether low-level structural linguistic features are represented inside language models in ways that are discoverable, measurable, and causally relevant to model behavior.

Rather than treating linguistic structure as a surface property of prompts, the project studies whether grammatical and quasi-grammatical variables such as evidentiality, agency marking, authority/status marking, and negation correspond to internal representational features. The central hypothesis is that such features can influence model behavior, including deference, uncertainty, attribution of responsibility, truth-framing, and response style.

## Research Goal

The goal is to build an exploratory mechanistic pipeline for identifying linguistic features that may later inform the design of Constitutional Languages: deliberately structured languages or intermediate representations intended to make model behavior more stable, transparent, and less sensitive to harmful framing effects.

The project starts with four intentionally difficult feature families:

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

The methodology is based on the sparse-autoencoder interpretability approach used in:

> Brinkmann, J., Wendler, C., Bartelt, C., & Mueller, A. (2025). **Large Language Models Share Representations of Latent Grammatical Concepts Across Typologically Diverse Languages.** arXiv:2501.06346.  
> https://arxiv.org/abs/2501.06346

That paper trains sparse autoencoders on internal activations of large language models, identifies SAE features corresponding to morphosyntactic concepts, uses attribution patching to locate causally relevant features, and validates those features through ablation and steering interventions.

This project does not aim to reproduce the paper's exact experimental targets, such as number, tense, or grammatical gender. Instead, it adapts the paper's methodological skeleton to alignment-relevant structural linguistic variables.

The adapted pipeline is:

- collect controlled linguistic datasets using minimal-pair and counterfactual templates;
- run a pretrained language model and cache internal activations;
- train sparse autoencoders on selected residual stream activations;
- identify SAE features associated with the target linguistic variables;
- train probes over both raw activations and SAE latents;
- rank and inspect candidate features;
- perform ablation and steering interventions;
- measure whether interventions affect downstream behavior.

## Core Research Question

Can sparse autoencoders recover low-level structural linguistic variables from language-model representations, and can those recovered features be causally linked to downstream behavior?

The project asks whether structural linguistic features can be treated as mechanistic objects inside language models rather than merely as surface properties of prompts.

## Research Variable Map

The long-term research program begins from a 40-variable map of structural linguistic features. The first experiments focus on evidentiality, agency, status/authority, and negation, but the repository is designed to grow into a broader reusable resource.

| # | Variable | Short description |
|---:|---|---|
| 1 | Subject explicitness / pro-drop | Whether subjects must be explicitly stated or can be omitted. |
| 2 | Agent prominence / passive | How strongly the grammar foregrounds the acting agent. |
| 3 | Causativity | Whether causation is encoded directly, indirectly, or through special marking. |
| 4 | Evidentiality | Whether information source is grammatically or structurally marked. |
| 5 | Grammatical gender | Whether nouns, pronouns, or agreement patterns encode gender classes. |
| 6 | Honorific/status marking | Whether social rank, politeness, or respect are structurally encoded. |
| 7 | Word order | How subject, object, verb, and modifiers are ordered. |
| 8 | Case marking | Whether grammatical roles are marked through morphology or position. |
| 9 | Agglutinative morphology | Whether words are built from separable chains of morphemes. |
| 10 | Analytic vs synthetic grammar | Whether relations are expressed mostly through word order/function words or morphology. |
| 11 | Definiteness/articles | Whether known/unknown or specific/non-specific reference is explicitly marked. |
| 12 | Number marking | Whether singular, plural, dual, or other number distinctions are marked. |
| 13 | Animacy marking | Whether living/sentient entities are grammatically distinguished from non-living ones. |
| 14 | Person hierarchy | Whether first, second, and third person are structurally ranked or treated differently. |
| 15 | Inclusive/exclusive we | Whether “we including you” and “we excluding you” are distinguished. |
| 16 | Genericity | How general claims, kinds, norms, or universal statements are encoded. |
| 17 | Habitual aspect | Whether repeated or characteristic actions are structurally marked. |
| 18 | Tense prominence | How strongly time location is grammatically required. |
| 19 | Aspect | How event structure, completion, duration, or ongoingness are marked. |
| 20 | Negation placement | Where negation appears and how it scopes over a sentence. |
| 21 | Double negation | Whether multiple negatives cancel, intensify, or preserve negation. |
| 22 | Quantifier scope | How “all,” “some,” “none,” “most,” and similar operators bind meaning. |
| 23 | Conditionals | How hypothetical, counterfactual, and causal dependency structures are marked. |
| 24 | Topic-comment structure | Whether sentences explicitly separate what is being discussed from what is said about it. |
| 25 | Focus marking | How new, contrastive, or emphasized information is structurally highlighted. |
| 26 | Given/new marking | Whether old information and new information are grammatically distinguished. |
| 27 | Pronoun richness/reduction | How much pronouns encode person, gender, number, formality, or social relation. |
| 28 | Formal/informal you | Whether the second person distinguishes intimacy, distance, politeness, or hierarchy. |
| 29 | Status agreement | Whether grammar changes depending on social relation between speaker, listener, or referent. |
| 30 | Direct/indirect request grammar | How commands, requests, suggestions, and obligations are structurally encoded. |
| 31 | Motion encoding | How path, manner, direction, source, and goal of movement are expressed. |
| 32 | Emotion grammar | Whether emotional state, evaluation, or affect are structurally encoded. |
| 33 | Possession structure | How ownership, relation, alienability, and control are encoded. |
| 34 | Whitespace segmentation | Whether word boundaries are explicit or implicit. |
| 35 | Character vs subword units | Whether linguistic structure is exposed through characters, morphemes, or subword tokens. |
| 36 | Script variation | How writing systems influence segmentation, abstraction, and visual/token structure. |
| 37 | Punctuation structure | How punctuation encodes hierarchy, emphasis, quotation, or discourse relation. |
| 38 | Redundancy | How often the same information is marked multiple times across a sentence. |
| 39 | Ambiguity density | How much meaning is left underspecified by the surface form. |
| 40 | Optionality vs obligatoriness | Which distinctions must be encoded and which can be left implicit. |

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
- documentation of failure modes and artifact controls;
- a scalable template for expanding from the initial four variables to the full 40-variable map.

The end product is not only a set of experimental results, but also a reusable pipeline for testing additional linguistic variables.

## Intended Research Contribution

A successful result would show that some structural linguistic variables are:

- linearly or sparsely recoverable from internal activations;
- represented by interpretable SAE features or feature clusters;
- robust across lexical templates and notation systems;
- causally involved in model predictions or generated behavior;
- useful for designing later controlled language or representation systems.

This would support future research into Constitutional Languages by identifying which linguistic structures are promising candidates for deliberate design and which are likely too entangled, distributed, or behaviorally weak.

## Experimental Loop

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
