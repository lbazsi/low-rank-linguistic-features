# WALS-Aligned Structural Feature Map

This document defines the structural linguistic feature map used by the Low-Rank Linguistic Features project. The map is designed for mechanistic interpretability experiments on language models: each variable should be expressible through controlled contrasts, recoverable from model activations if represented, and testable through ablation or steering interventions.

The feature map is aligned with the general typological orientation of **The World Atlas of Language Structures Online (WALS)**, which organizes structural linguistic properties across domains such as morphology, nominal categories, nominal syntax, verbal categories, word order, simple clauses, complex sentences, lexicon, and writing systems.

Recommended general citation:

> Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013. **WALS Online (v2020.4)** [Data set]. Zenodo. https://doi.org/10.5281/zenodo.13950591. Available online at https://wals.info.

The present map is not a direct copy of WALS chapters. It adapts typological categories into an experimental feature inventory for studying foundational linguistic effects in language models.

## Design Principles

The list aims to satisfy four constraints:

1. **Typological grounding**  
   Variables should correspond to structural properties known to vary across languages.

2. **Experimental isolability**  
   Variables should be expressible through minimal pairs, counterfactual templates, or controlled synthetic variants.

3. **Mechanistic usefulness**  
   Variables should plausibly correspond to recoverable internal features, feature clusters, or directions in model activations.

4. **Behavioral relevance**  
   Variables should plausibly affect model behavior, including uncertainty, deference, responsibility attribution, truth-framing, refusal behavior, reasoning style, or sensitivity to social pressure.

## Variable Map

| # | Feature | WALS-aligned domain | Experimental handle |
|---:|---|---|---|
| 1 | Subject expression / pro-drop | Simple clauses / nominal syntax | Explicit subject vs omitted subject where recoverable from agreement or context. |
| 2 | Basic constituent order | Word order | SVO, SOV, VSO, OSV-style variants or controlled argument-order permutations. |
| 3 | Nominal modifier order | Word order / nominal syntax | Noun-adjective, adjective-noun, genitive-noun, noun-genitive, demonstrative-noun ordering. |
| 4 | Case marking | Nominal categories / simple clauses | Overt role marking vs role inferred from position. |
| 5 | Morphosyntactic alignment | Simple clauses | Nominative-accusative, ergative-absolutive, active-stative, neutral alignment patterns. |
| 6 | Transitivity / valency | Simple clauses | Intransitive, transitive, ditransitive, experiencer, beneficiary, and instrument structures. |
| 7 | Voice and agent prominence | Simple clauses / verbal categories | Active, passive, antipassive, middle, impersonal, and agentless event framing. |
| 8 | Causativity and valency change | Verbal categories / simple clauses | Direct causation, indirect causation, permissive causation, lexical causatives, causative morphology. |
| 9 | Analytic vs synthetic encoding | Morphology | Grammatical relations expressed through separate words vs bound morphology. |
| 10 | Morphological segmentation type | Morphology | Isolating, agglutinative, fusional, introflexive, polysynthetic-style encoding. |
| 11 | Agreement / indexing density | Morphology / simple clauses | Whether person, number, gender, case, or role are redundantly marked on verbs, nouns, or dependents. |
| 12 | Optionality vs obligatoriness of marking | Morphology / grammar-wide | Whether distinctions such as tense, evidentiality, number, or politeness must be encoded. |
| 13 | Redundancy / cumulative exponence | Morphology | Whether the same information is marked once, repeatedly, or bundled with other features. |
| 14 | Definiteness and specificity | Nominal categories | Definite, indefinite, specific, nonspecific, familiar, and unique-reference marking. |
| 15 | Number marking | Nominal categories | Singular, plural, dual, paucal, collective, or unmarked number. |
| 16 | Gender / noun class | Nominal categories | Gender, noun class, classifier, or agreement-class encoding. |
| 17 | Animacy and humanness | Nominal categories / simple clauses | Human, animate, sentient, living, non-living, and object distinctions. |
| 18 | Person marking and person hierarchy | Nominal categories / verbal categories | First, second, third person and hierarchy effects in agreement or role marking. |
| 19 | Inclusive/exclusive distinction | Nominal categories | Inclusive “we” vs exclusive “we.” |
| 20 | Pronoun richness and reduction | Nominal categories / nominal syntax | Rich pronoun systems vs reduced or context-dependent pronoun systems. |
| 21 | Possession and alienability | Nominal syntax | Alienable vs inalienable possession, ownership, kinship, body-part, and control relations. |
| 22 | Tense prominence | Verbal categories | Whether temporal location is obligatory, optional, absent, or inferred. |
| 23 | Aspect and event structure | Verbal categories | Perfective, imperfective, progressive, habitual, completive, iterative, prospective. |
| 24 | Modality and mood | Verbal categories / complex sentences | Necessity, possibility, permission, ability, obligation, imperative, subjunctive, optative. |
| 25 | Epistemic modality | Verbal categories / discourse | Certainty, probability, possibility, doubt, confidence, and epistemic distance. |
| 26 | Evidentiality | Verbal categories / discourse | Direct evidence, inference, report, hearsay, assumption, institutional source. |
| 27 | Mirativity, stance, and affect marking | Verbal categories / discourse | Surprise, unexpectedness, speaker attitude, affective stance, evaluative marking. |
| 28 | Negation and polarity structure | Simple clauses / complex sentences | Negation position, negation scope, negative concord, double negation, polarity items. |
| 29 | Quantifier scope and distributivity | Nominal syntax / semantics | All, some, most, none, each, every, collective vs distributive readings. |
| 30 | Conditional and counterfactual marking | Complex sentences | If/then, hypothetical, counterfactual, concessive conditional, realis/irrealis conditionals. |
| 31 | Subordination and embedding | Complex sentences | Embedded clauses, belief reports, desire reports, causal embedding, recursive clausal structure. |
| 32 | Quotation and reported speech structure | Complex sentences / discourse | Direct quotation, indirect speech, free indirect discourse, source attribution, embedded claims. |
| 33 | Discourse relation marking | Complex sentences / discourse | Cause, contrast, concession, evidence, elaboration, sequence, conclusion, explanation. |
| 34 | Topic-comment structure | Information structure | Explicit topic marking vs subject-predicate organization. |
| 35 | Focus and given/new marking | Information structure | Contrastive focus, new information, old information, clefts, particles, prosodic equivalents in text. |
| 36 | Genericity and kind-level reference | Nominal categories / discourse | Generic claims, kind statements, habitual generalizations, norm-like statements. |
| 37 | Social deixis / honorifics / status encoding | Nominal categories / pragmatics | Formality, rank, respect, humility, speaker-listener hierarchy, referent honorification. |
| 38 | Speech-act force and request directness | Simple clauses / pragmatics | Assertion, question, command, request, warning, advice, promise, threat; direct vs indirect forms. |
| 39 | Deixis and perspective anchoring | Nominal categories / discourse | Here/there, now/then, this/that, I/you/we/they, proximal/distal, speaker-centered framing. |
| 40 | Orthographic and tokenization interface | Writing systems / other | Script, punctuation, whitespace, capitalization, segmentation, character vs subword exposure. |

## Experimental Use

For each variable, the project should construct:

- controlled minimal pairs;
- counterfactual templates;
- held-out lexical templates;
- held-out surface forms;
- token/bag-of-words baselines;
- raw-activation probes;
- SAE-latent probes;
- candidate feature rankings;
- top-activating-example inspection;
- ablation tests;
- steering tests;
- behavioral evaluations.

The map should be treated as a living experimental ontology. Variables can be split, merged, or deprioritized as the project reveals which distinctions are mechanistically recoverable and behaviorally important.
