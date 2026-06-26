# Construction Process

## Workflow

1. Initial prompt to generate the `001-100` dataset per feature.
2. Thorough analysis of the generated dataset using `feature_dataset_audit_pipeline/`.
3. Generate a revised prompt to mitigate the identified failure points.
4. Regenerate the dataset from `001-500`.
5. Thorough analysis of the `001-500` dataset using `feature_dataset_audit_pipeline/`.
6. Regenerate the final `001-500` dataset based on the identified issues.

## Initial Generation Prompt

```text
You are generating a controlled synthetic feature dataset for a mechanistic interpretability project called Low-Rank Linguistic Features.
Please read the attached files before generating anything:
Feature dataset construction.md
List of features.md
The variable-specific metadata.yaml attached to this chat
Your task is to generate synthetic contrast-pair examples for the variable specified in the attached metadata.yaml.

Generation target
Generate exactly 100 JSONL examples.
Use IDs from:
[VARIABLE_ID]_001 to [VARIABLE_ID]_100

Each output line must be one valid JSON object. Do not wrap the output in a Markdown code block. Do not add explanations, comments, headings, or bullet points. Output JSONL only.

Required schema
Each example must follow this exact schema:
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

Use the actual values from the attached metadata.yaml.

Split rule
Assign split based on the numeric ID:
001-400 = train
401-450 = val
451-500 = test

Language and surface type
Follow the variable-specific approach, languages, and surface_types from the attached metadata.yaml.
Use only allowed project language codes:
en, tr, ja, ko, es, ru, ar, zh

Use only allowed surface types:
en
en_ctrl
xl
pseudo

For ordinary English examples, use:
"language": "en",
"surface_type": "en"

For controlled English examples, use:
"language": "en",
"surface_type": "en_ctrl"

For non-English structural examples, use:
"surface_type": "xl"

Contrast-pair requirements
Each example must contain exactly two sentences:
{"type": "basis", "sentence": "..."}
{"type": "changed", "sentence": "..."}

The changed sentence must isolate the target contrast as much as possible.

Keep the following stable across basis and changed sentences:
event content
participants
domain
approximate sentence length
named entities, unless the contrast requires changing them
factual scenario
emotional intensity
level of specificity

Only change what is needed for the target linguistic contrast.

Diversity requirements
Across the generated examples, vary:
event domains
sentence structures
names and entities
social contexts
technical/non-technical scenarios
formal and neutral registers
short and medium sentence lengths
contrast labels, if multiple target contrasts are listed in the metadata

Avoid generating many examples that differ only by one repeated word or marker.
Avoid relying on a single surface trigger unless the variable specifically requires it.

Quality requirements
Each sentence must be grammatical and natural enough for the stated language.

Do not generate:
empty fields
duplicate IDs
duplicate sentence pairs
identical basis and changed sentences
examples where unrelated meaning changes
examples where the contrast label does not match the actual sentence difference
examples that are only shallow lexical substitutions when the variable is structural
examples outside the language or approach specified in the metadata

Output format
Return only a downloadable JSONL.
Do not include Markdown.
Do not include explanations.
Do not include a surrounding list.
Do not include trailing commas.

Now generate examples for:
Variable ID: [VARIABLE_ID]
Variable name: [VARIABLE_NAME]
ID range: 001-100
Number of pairs: 100
```
