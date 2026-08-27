# Metadata Split-Control Extension

This document specifies a metadata-level extension to the feature-dataset construction system. The extension adds explicit split-control inventories for marker families and lexical domains to each variable-specific metadata file.

The purpose of the extension is to make train, validation, and test splits more diagnostically useful for mechanistic probing. The revised metadata does not only define what feature should be generated. It also defines which surface-realization families and lexical domains are allowed in each split.

## Scope of the Change

The change applies to the forty variable-specific `metadata.yaml` files.

Each metadata file keeps its existing content unchanged and adds two new top-level fields:

```yaml
marker_families:
  train:
    - ...
  val:
    - ...
  test:
    - ...

lexical_domains:
  train:
    - ...
  val:
    - ...
  test:
    - ...
```

No existing variable identifiers, variable names, language assignments, approaches, surface types, target contrasts, generation notes, or split rules are changed by this extension.

## Relation to the Original YAML Metadata

The original metadata files specified the core generation target for each variable:

- `variable_id`
- `variable`
- `approach`
- `languages`
- `surface_types`
- `target_contrasts`
- `generation_notes`
- `split_rule`

The extended metadata keeps these fields intact and adds split-control inventories.

The new fields are not replacement fields. They are constraints on generation and validation. They specify which families of surface realization and which lexical domains should appear in train, validation, and test examples.

## Marker Families

A `marker_family` is a broad class of surface realization used to express the target contrast.

For example, in a modality variable, marker families may distinguish auxiliary modals, periphrastic constructions, impersonal constructions, nominalized constructions, or adverbial modality. In a negation variable, marker families may distinguish simple clausal negation, negative quantification, negative polarity environments, lexical negation, and scope-sensitive negation.

The marker-family field is intended to reduce over-reliance on a single visible cue. If the same marker family appears in every split, a probe may learn the presence of a specific word, suffix, particle, construction, or punctuation pattern rather than a more general structural distinction.

The split-specific marker-family lists therefore define a stronger generalization condition:

```text
train = marker families available for probe training
val   = marker families used for model selection and threshold inspection
test  = held-out marker families used for final evaluation
```

The most important constraint is that marker families assigned to the test split should not also appear in the train split.

## Lexical Domains

A `lexical_domain` is the semantic or topical domain used to instantiate the sentence pair.

Examples include domains such as medical, legal, engineering, education, logistics, finance, science, administration, public safety, and domestic events. The exact inventory is variable-specific.

The lexical-domain field is intended to reduce topic leakage and repeated-domain memorization. A dataset can accidentally make train and test too similar if the same types of events, actors, and objects appear throughout all splits.

The split-specific lexical-domain lists define a second generalization condition:

```text
train = domains available for probe training
val   = domains used for model selection and inspection
test  = held-out domains used for final evaluation
```

A strong split should avoid assigning the same lexical domain to both train and test unless there is a specific reason to do so.

## Relation to the Original JSONL Dataset

The original JSONL examples use a shared controlled-pair schema:

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

The metadata extension does not modify the existing JSONL files by itself. It defines additional generation and validation constraints for future dataset construction or regeneration.

For a regenerated dataset, each JSONL example should include two additional fields:

```json
{
  "marker_family": "...",
  "lexical_domain": "..."
}
```

A regenerated example should therefore have the following extended form:

```json
{
  "id": "26_451",
  "variable_id": 26,
  "variable": "evidentiality",
  "approach": "EN+XL",
  "language": "tr",
  "surface_type": "xl",
  "contrast": "direct_to_reported",
  "marker_family": "heldout_reportative_strategy",
  "lexical_domain": "legal",
  "split": "test",
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

The pair structure remains unchanged. The basis sentence and changed sentence still form a controlled contrast pair. The new fields describe how the contrast is realized and in which lexical domain the example is situated.

## Split Semantics

The default numerical split remains:

```text
001-400 = train
401-450 = val
451-500 = test
```

The extension changes what those splits are expected to mean.

In the original construction, the split was primarily an ID-based separation. In the extended construction, the split should also correspond to a controlled generalization difference:

- train examples use train-assigned marker families and lexical domains;
- validation examples use validation-assigned marker families and lexical domains;
- test examples use test-assigned marker families and lexical domains.

This makes the test set a stronger evaluation of generalization. A probe should not succeed merely by detecting a marker family that was already seen repeatedly in training.

## Validation Requirements

A validator for the extended metadata and regenerated JSONL dataset should check the following conditions.

### YAML validation

For each metadata file:

1. `marker_families` must exist.
2. `lexical_domains` must exist.
3. Each must contain `train`, `val`, and `test` keys.
4. Each split list must be non-empty.
5. Marker-family values should not overlap across train, validation, and test unless explicitly justified.
6. Lexical-domain values should not overlap across train, validation, and test unless explicitly justified.

### JSONL validation

For each generated example:

1. `marker_family` must exist.
2. `lexical_domain` must exist.
3. `marker_family` must be listed under the example's split in the corresponding metadata file.
4. `lexical_domain` must be listed under the example's split in the corresponding metadata file.
5. The original required schema fields must still be present.
6. The example must contain exactly one basis sentence and one changed sentence.
7. The target contrast must remain one of the variable's allowed `target_contrasts`.

## Reason and intended effect

In v0, the feature dataset produced strong raw activation probe scores, but the same basis/changed distinctions were often recoverable by simple text baselines such as TF-IDF or character n-grams. This suggested that probes were frequently learning surface markers like specific words, particles, suffixes, punctuation, spacing, or recurring construction patterns rather than deeper structural linguistic representations.

The most problematic result was that the dataset split was administratively clean but not experimentally hard enough: train, validation, and test examples often shared similar marker families and lexical domains. As a result, high test performance did not necessarily show generalization to unseen structural realizations.

The added marker_families and lexical_domains fields are meant to make the split auditable: held-out test examples should use different marker families and domains from training, so future probe results better reflect structural generalization rather than memorization of surface cues.