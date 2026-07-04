# Feature Dataset Language Strategy

This document specifies the language strategy for constructing the **feature dataset**.

The experiment uses a compact multilingual language pool specified later below.

For simplicity and interpretability, each **XL** or **EN+XL** variable uses **at most one non-English language**. This keeps the experiment easier to debug and reduces confounds from mixing language identity, script, morphology, tokenization, and corpus quality within the same variable.

## Legend

| Label | Meaning |
|---|---|
| **EN** | English templates are sufficient. |
| **EN+ctrl** | English is usable, but controlled templates or lexical substitutions are needed to reduce confounds. |
| **XL** | English underdetermines the feature; use one selected non-English language from the experiment language pool. |
| **EN+XL** | English gives a partial contrast, but the full structural contrast uses one selected non-English language. |

## Experiment Language Pool

| Language | Main use |
|---|---|
| **English** | Baseline language; strong for syntax, modality, negation, embedding, conditionals, discourse, and behavioral evaluations. |
| **Turkish** | Agglutination, case marking, evidentiality, causativity, pro-drop, rich morphology. |
| **Japanese** | Pro-drop, SOV order, topic-comment structure, honorifics, quotation/reporting patterns, stance particles. |
| **Korean** | Honorifics, speech levels, SOV order, topic/focus particles, stance and sentence-final marking. |
| **Spanish** | Pro-drop, grammatical gender, agreement, person marking, tense/aspect morphology. |
| **Russian** | Case marking, gender, aspect, animacy-sensitive morphology, flexible word order. |
| **Arabic** | Script variation, root-pattern morphology, gender/number agreement, dual, VSO/SVO variation. |
| **Mandarin Chinese** | Analytic structure, topic-comment structure, classifier-like nominal structure, no obligatory tense, script/tokenization contrast. |

Japanese and Korean should not both be used for the same variable unless there is a strong reason. Spanish and Russian should also usually be treated as alternatives rather than combined within the same variable.

## Language letter codes

Use the following two-letter language codes in dataset metadata, filenames, and split definitions.

| Language | Code |
|---|---|
| English | `en` |
| Turkish | `tr` |
| Japanese | `ja` |
| Korean | `ko` |
| Spanish | `es` |
| Russian | `ru` |
| Arabic | `ar` |
| Mandarin Chinese | `zh` |

## Corpus Principle

The **feature dataset** and the **SAE training corpus** serve different purposes.

The feature dataset is variable-specific and typologically targeted. Its goal is to build a template for all following datasets and experiments.

The SAE training corpus should be broad and multilingual enough to cover every language used in the feature dataset. If Turkish, Japanese, Korean, Spanish, Russian, Arabic, or Mandarin is used in controlled probes, the SAE corpus should include natural text from that language.

The SAE corpus should be constructed purely as multilingual natural text with one shared multilingual SAE for cross-language feature discovery.

## Recommended Dataset Schema

Each controlled example should use the same metadata format.

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

## Split types

Each feature-dataset example should belong to exactly one split.

| Split | Purpose |
|---|---|
| `train` | Used to train probes on raw activations and SAE latents. |
| `val` | Used to tune probe settings, inspect early results, and choose analysis thresholds. |
| `test` | Used for final evaluation on unseen instances. (cross validation) |

Default split ratio:

```text
train: 80%
val: 10%
test: 10%
```

With separation by id:

```text
001-400 = train
401-450 = val
451-500 = test
```

## Forty-Variable Construction Table

| # | Variable | Approach | Selected language(s) | Dataset construction specification |
|---:|---|---|---|---|
| 1 | Subject expression / pro-drop | XL | Turkish | Contrast explicit subjects with grammatically licensed subject omission. |
| 2 | Basic constituent order | EN+XL | English + Japanese | Use English for limited controlled perturbations and Japanese for natural SOV order contrasts. |
| 3 | Nominal modifier order | EN+XL | English + Spanish | Contrast English adjective-noun order with Spanish noun-adjective and genitive/modifier alternatives. |
| 4 | Case marking | XL | Russian | Use overt case-marked noun phrases and compare them with role inference from word order. |
| 5 | Morphosyntactic alignment | XL | Turkish | Use Turkish case/role contrasts as an approximate alignment-related probe. Full ergativity is outside the simplified experiment. |
| 6 | Transitivity / valency | EN | English | Build intransitive, transitive, ditransitive, experiencer, beneficiary, and instrument frames. |
| 7 | Voice and agent prominence | EN | English | Contrast active, passive, by-phrase passive, agentless passive, middle-like, and impersonal event descriptions. |
| 8 | Causativity and valency change | EN+XL | English + Turkish | Use English periphrastic causatives and Turkish structural/morphological causative contrasts. |
| 9 | Analytic vs synthetic encoding | EN+XL | English + Turkish | Contrast English function-word-heavy expression with Turkish morphologically packed expression. |
| 10 | Morphological segmentation type | XL | Turkish | Use Turkish agglutinative morphology as the main segmentation contrast. |
| 11 | Agreement / indexing density | XL | Spanish | Use Spanish agreement and person/number marking as the main richer-agreement contrast. |
| 12 | Optionality vs obligatoriness of marking | XL | Mandarin | Use Mandarin to test absence/optionality of tense-like marking against context and temporal adverbs. |
| 13 | Redundancy / cumulative exponence | XL | Russian | Use Russian bundled case/gender/number morphology and agreement redundancy. |
| 14 | Definiteness and specificity | EN | English | Use definite, indefinite, specific, nonspecific, generic, and unique-reference contrasts. |
| 15 | Number marking | EN+XL | English + Arabic | Use English singular/plural and Arabic dual/richer number agreement. |
| 16 | Gender / noun class | XL | Spanish | Use grammatical gender and agreement. Full noun-class systems are outside the simplified experiment. |
| 17 | Animacy and humanness | EN+ctrl | English | Use controlled lexical sets for human, animate, sentient, living, and non-living entities. |
| 18 | Person marking and person hierarchy | EN+XL | English + Spanish | Use English for basic person contrasts and Spanish for richer person/agreement marking. |
| 19 | Inclusive/exclusive distinction | XL | Mandarin | Keep as a weak placeholder using Mandarin inclusive-like lexical contrasts where possible. True grammatical inclusive/exclusive requires future extension. |
| 20 | Pronoun richness and reduction | EN+XL | English + Japanese | Contrast overt pronouns in English with Japanese pronoun omission and context-dependent reference. |
| 21 | Possession and alienability | EN+ctrl | English | Use controlled lexical possession contrasts. True grammatical alienability is outside the simplified experiment. |
| 22 | Tense prominence | EN+XL | English + Mandarin | Contrast English tense marking with Mandarin context/adverb-based temporal interpretation. |
| 23 | Aspect and event structure | EN+XL | English + Russian | Use English aspectual forms and Russian aspect contrasts. |
| 24 | Modality and mood | EN | English | Contrast must, should, may, can, might, imperative, permission, ability, obligation, and necessity. |
| 25 | Epistemic modality | EN+ctrl | English | Use controlled modal and adverbial contrasts: certainly, probably, possibly, maybe, apparently. |
| 26 | Evidentiality | EN+XL | English + Turkish | Use English source-marking pilots and Turkish grammatical evidential contrasts. |
| 27 | Mirativity, stance, and affect marking | XL | Japanese | Use Japanese stance, sentence-final, surprise, and affective constructions. |
| 28 | Negation and polarity structure | EN | English | Contrast affirmation, simple negation, denial, contradiction, negative polarity items, and scope ambiguity. |
| 29 | Quantifier scope and distributivity | EN | English | Use all/some/none/most/every/each and collective vs distributive readings. |
| 30 | Conditional and counterfactual marking | EN | English | Contrast real conditionals, hypotheticals, counterfactuals, concessives, and if/then dependency. |
| 31 | Subordination and embedding | EN | English | Use embedded belief, claim, desire, reason, evidence, and recursive clause structures. |
| 32 | Quotation and reported speech structure | EN+XL | English + Japanese | Control quotation punctuation in English and use Japanese quotative/reporting structures. |
| 33 | Discourse relation marking | EN+ctrl | English | Contrast because, although, however, therefore, while, since, despite, so. Control connective identity. |
| 34 | Topic-comment structure | XL | Japanese | Use topic particles, topic-fronting, and topic-comment constructions. |
| 35 | Focus and given/new marking | EN+XL | English + Japanese | Use English clefts/contrastive templates and Japanese focus/topic particles. |
| 36 | Genericity and kind-level reference | EN | English | Contrast specific individuals, kinds, generics, habitual generalizations, and norm-like claims. |
| 37 | Social deixis / honorifics / status encoding | EN+XL | English + Korean | Use English authority/deference behavior and Korean honorifics/speech-level contrasts. |
| 38 | Speech-act force and request directness | EN+ctrl | English | Contrast assertion, question, command, request, warning, advice, promise, threat, and indirect request forms. |
| 39 | Deixis and perspective anchoring | EN | English | Contrast here/there, now/then, this/that, I/you/we/they, proximal/distal, and speaker-centered framing. |
| 40 | Orthographic and tokenization interface | EN+XL | English + Mandarin | Use English punctuation/case/spacing controls and Mandarin script/segmentation contrasts. |

## Possible Limitations

The one-XL-language rule keeps the experiment clean, but it narrows the typological range of several variables.

| Variable | Limitation | Consequence |
|---|---|---|
| Morphosyntactic alignment | Turkish does not provide a full ergative/split-ergative system. | The experiment tests role/case structure more than true alignment typology. |
| Analytic vs synthetic encoding | English + Turkish gives a useful contrast but not the full typological space. | Results should not be interpreted as covering all analytic/synthetic possibilities. |
| Morphological segmentation type | Turkish only covers agglutinative morphology strongly. | Fusional, introflexive, and polysynthetic systems remain outside the experiment. |
| Inclusive/exclusive distinction | Mandarin does not provide a clean grammatical inclusive/exclusive contrast. | This variable should be treated as weakly covered or kept as a placeholder. |
| Possession and alienability | English controlled examples do not test grammatical alienability. | Results only address lexical/semantic possession, not true alienable/inalienable grammar. |
| Gender / noun class | Spanish covers grammatical gender but not noun-class systems. | Noun-class generalization is not tested. |
| Mirativity / stance / affect | Japanese gives useful stance marking but not the full mirativity typology. | Results should be interpreted as stance/affect marking, not universal mirativity. |
| Social deixis / honorifics | Korean gives a strong honorific/speech-level system but only one social-deixis realization. | Cross-cultural or cross-linguistic generalization is not tested. |
| Orthographic/tokenization interface | Mandarin covers script/segmentation but not the full range of scripts. | Findings may reflect Mandarin-specific tokenization rather than script effects generally. |
| Topic/focus systems | Japanese is used for both topic-comment and focus/given-new contrasts. | Shared language-specific artifacts must be controlled carefully. |

The simplified design is still appropriate for this experiment because overengineering one variable with many languages would make the results harder to interpret, more expensive to run, and less useful for debugging the full SAE/probing/intervention pipeline.

## File Layout

```text
data/
  linguistic_features/
    variable_01_subject_expression/
      xl_tr.jsonl
      metadata.yaml

    variable_02_constituent_order/
      en.jsonl
      xl_ja.jsonl
      metadata.yaml

    variable_03_nominal_modifier_order/
      en.jsonl
      xl_es.jsonl
      metadata.yaml

    ...

    variable_40_orthographic_tokenization/
      en.jsonl
      xl_zh.jsonl
      metadata.yaml
```

## Construction Rules

1. Keep one shared schema across all variables.
2. Use at most one XL language per XL or EN+XL variable.
3. Do not force every variable into English.
4. Do not force every variable into pseudo-English.
5. Use English controls where English captures the behavioral phenomenon but not the full grammatical structure.
6. Use the selected XL language where the grammatical feature is absent or severely underdetermined in English.
7. For every language used in controlled probes, include that language in the broad SAE corpus.
8. Keep lexical content stable across counterfactual pairs.
9. Include held-out lexical templates and held-out surface markers.
10. Treat marked or pseudo-English forms as diagnostic controls, not as the main evidence for typological variables.
