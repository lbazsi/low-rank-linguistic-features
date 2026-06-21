# Low-Rank Linguistic Features

This project studies whether structural features of language are represented inside language models in ways that can be discovered, interpreted, and causally tested.

The motivating idea is that language is not only a medium through which prompts are expressed. Its structure may shape how models represent uncertainty, responsibility, authority, generality, negation, social relation, and other behaviorally important concepts. If these features can be located in model activations, they may become useful objects for interpretability, robustness, and future work on Constitutional Languages.

## Research Goal

The project builds a mechanistic pipeline for studying low-level linguistic structure in language models. It focuses on whether structural variables can be recovered from internal activations, whether sparse autoencoders can expose them as interpretable features, and whether interventions on those features change model behavior.

The long-term goal is to create a reusable empirical foundation for Constitutional Language research: the study of deliberately structured languages or intermediate representations that could make model behavior more stable, transparent, and less sensitive to framing, social pressure, or hidden linguistic bias.

## Methodological Basis

The methodology is based on sparse-autoencoder interpretability methods used in:

> Brinkmann, J., Wendler, C., Bartelt, C., & Mueller, A. (2025). **Large Language Models Share Representations of Latent Grammatical Concepts Across Typologically Diverse Languages.** arXiv:2501.06346.  
> https://arxiv.org/abs/2501.06346

The project adapts the paper's general mechanistic approach: train sparse autoencoders on model activations, identify linguistic features in SAE latents, rank candidate features by their relevance to target variables, and test those features through ablation and steering interventions.

## Core Research Question

Can sparse autoencoders recover structural linguistic variables from language-model activations, and can those recovered features be causally linked to downstream model behavior?

A positive result would suggest that some linguistic structures are not only surface-level prompt patterns, but internal representational features that influence how models reason, respond, defer, attribute responsibility, express uncertainty, or frame truth.

## Initial Focus

The first experiments focus on four feature families:

1. **Evidentiality**  
   How language marks the source or reliability of information: direct observation, inference, report, hearsay, uncertainty, or institutional source.

2. **Agency and responsibility marking**  
   How syntax foregrounds or hides the actor responsible for an event: active voice, passive voice, agent deletion, impersonal framing, or causal distance.

3. **Status and authority marking**  
   How language encodes social rank, expertise, politeness, institutional authority, or pressure to defer.

4. **Negation and truth-framing**  
   How language structures denial, contradiction, uncertainty, refusal, indirect truth claims, and scope of negation.

These four variables are prioritized because they are directly connected to alignment-relevant behaviors such as calibration, authority bias, sycophancy, responsibility attribution, refusal stability, and sensitivity to framing.

## Forty Structural Linguistic Variables

The broader research map contains forty linguistic variables that may affect model representations and behavior.

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

## Experiment Overview

The first experiment constructs a controlled interpretability pipeline around the four initial variables.

### 1. Dataset Construction

For each variable, the project creates controlled sentence sets using minimal pairs and counterfactual templates. Each example changes one structural property while keeping the surrounding content as stable as possible.

Example contrast types:

- direct observation vs reported information;
- active agency vs passive or agentless framing;
- high-authority speaker vs low-authority speaker;
- affirmed statement vs negated, denied, or indirectly contradicted statement.

Each variable is expressed through multiple surface forms so that the model cannot succeed only by detecting one obvious marker. The dataset includes held-out templates and held-out phrasings for evaluation.

### 2. Activation Collection

A small pretrained language model is run on the controlled examples and on broader background text. Internal activations are cached from selected residual-stream layers.

The controlled examples are used to study the target variables. The broader text is used to train sparse autoencoders on a less artificial activation distribution.

### 3. Sparse Autoencoder Training

Sparse autoencoders are trained on selected activation sites. Their purpose is to decompose dense model activations into sparse latent features that may correspond to interpretable linguistic or behavioral structure.

The first runs use a small model and a small number of layers to keep the experiment fast, inspectable, and cheap. Later runs can scale to additional layers, model sizes, and feature families.

### 4. Probing and Feature Discovery

The project trains simple probes on both raw activations and SAE latents to test whether each linguistic variable is recoverable.

Candidate SAE features are then ranked using measures such as label association, probe contribution, activation differences across contrast pairs, and top-activating examples. The goal is to identify features or feature clusters that track the target linguistic structures.

### 5. Feature Inspection

For each candidate feature, the project inspects the examples that activate it most strongly. This step checks whether the feature appears to represent the intended structural variable or whether it is mostly responding to shallow artifacts such as a single token, phrase, or template.

### 6. Ablation

The strongest candidate features are ablated and the model is re-evaluated. If removing a feature weakens the model's ability to represent or respond to the relevant variable, this provides evidence that the feature is causally involved rather than merely correlated.

### 7. Steering

Candidate features are also steered in the opposite direction. For example, the experiment can increase features associated with reported evidence, hidden agency, authority pressure, or negated truth-framing and test whether model outputs shift accordingly.

### 8. Behavioral Evaluation

The final stage tests whether feature interventions affect behaviorally meaningful outputs. Evaluation focuses on changes in uncertainty, deference, responsibility attribution, truth framing, refusal behavior, and sensitivity to social or evidential cues.

## Expected Outputs

The repository is intended to produce:

- controlled datasets for the initial four variables;
- reusable templates for expanding to the full forty-variable map;
- cached activations from selected language models;
- trained sparse autoencoders;
- probe results over raw activations and SAE latents;
- ranked candidate features for each variable;
- top-activating examples for interpretability;
- ablation and steering results;
- behavioral evaluations of feature interventions;
- documentation of artifact controls and failure cases.

## Artifact Controls

The project includes controls to distinguish genuine structural representations from shallow pattern matching.

Planned controls include:

- held-out lexical templates;
- held-out surface markers;
- multiple phrasings for each variable;
- token-level and bag-of-words baselines;
- random-feature ablation baselines;
- comparison between raw-activation probes and SAE-latent probes;
- behavioral tests that separate surface imitation from representational effects.

The aim is not to show that a model can recognize words like “reportedly,” “expert,” or “not.” The aim is to test whether broader structural patterns are internally represented and causally usable.

## Research Contribution

A successful result would show that at least some structural linguistic variables are:

- recoverable from internal activations;
- represented in sparse latent features or feature clusters;
- robust across surface forms;
- causally involved in model predictions or generations;
- relevant to alignment-related behavior.

This would create an empirical foundation for later Constitutional Language research by identifying which linguistic structures are worth designing around, which are too entangled to control directly, and which may influence model behavior more strongly than expected.

## Long-Term Direction

This project is the first layer of a broader research program on language structure and alignment.

Future work can use the pipeline to:

- expand from four variables to the full forty-variable map;
- compare models of different sizes and training distributions;
- study interactions between linguistic variables;
- test artificial or semi-artificial language systems;
- investigate whether structural language design can reduce framing sensitivity;
- build constitutional representations that improve robustness, transparency, or behavioral stability.

The long-term aim is to understand whether language structure itself can become an alignment tool.
