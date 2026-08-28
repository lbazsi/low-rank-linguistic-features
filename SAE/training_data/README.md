# SAE Corpus

This directory contains the corpus-construction and cleaning pipeline used to prepare a multilingual natural-language dataset for sparse autoencoder (SAE) training in the **Low-Rank Linguistic Features** project.

The corpus is designed for unsupervised representation learning. Linguistic metadata is retained for auditing and later analysis, but SAE training itself uses only the sentence text and example ID.

## Canonical dataset

The canonical dataset carried forward is:

`data/sae_train_150k_v1_2_final.jsonl`

Final integrity:

- 149,338 rows
- 149,338 unique IDs
- 0 schema failures
- 0 normalized duplicate extras
- 0 Unicode replacement characters
- 0 empty texts

This metadata-retained JSONL is the single source of truth. A text-only training file may be derived from it when convenient, but should not be maintained as an independent dataset version.

Each row follows the structure:

```json
{
  "id": "sae_train_000001",
  "text": "...",
  "language": "tr",
  "variables_present": [4, 8, 11],
  "lexical_domain": "workplace",
  "length_bucket": "medium"
}
```

`variables_present` is retained as audit metadata and should **not** be treated as ground-truth supervision for SAE training or feature evaluation.

## Corpus construction

The initial corpus contained 150,000 multilingual sentences.

Generation used a static construction × language × lexical-domain batch plan. Each generation request specified:

- a primary linguistic variable;
- a construction family;
- a language;
- a lexical domain;
- a target length bucket.

Sentence generation and metadata annotation were performed in separate model calls. The annotation stage therefore did not modify the generated sentence.

Generation was performed locally with a multilingual 32B instruction model through vLLM. The plan and prompt policy are retained under `corpus_generation/`.

Relevant files:

```text
corpus_generation/
├── PROMPT_POLICY.md
├── BATCH_PLAN.md
├── requirements.txt
├── configs/
│   ├── generation.yaml
│   ├── variable_constructions.yaml
│   └── batch_plan_150k.csv
└── scripts/
    ├── generate_150k.py
    ├── generate_150k_fast.py
    ├── validate_plan.py
    └── audit_corpus.py
```

## Corpus cleaning and repair

Cleaning was deliberately conservative because many unusual linguistic constructions are scientifically relevant and can be incorrectly normalized by general-purpose language models.

The process consisted of three stages.

### 1. Deterministic audit

The initial 150,000-row corpus was checked for:

- schema and ID integrity;
- exact and normalized duplicates;
- mixed-script contamination;
- model/instruction leakage;
- metalinguistic content;
- runaway repetition;
- strong multi-sentence generation artifacts;
- likely truncation;
- malformed or out-of-inventory language metadata.

High-confidence corrupt rows were removed, leaving 149,338 retained examples.

### 2. Detector-only multilingual review

A conservative multilingual reviewer was run over all 149,338 retained rows.

The reviewer was used only to identify suspicious examples. It was **not** permitted to rewrite the corpus automatically, because general-purpose LLMs can incorrectly treat valid marked constructions as errors.

The full review produced:

- 145,035 `KEEP`
- 3,534 `FIX`
- 769 `REVIEW`

These labels were treated as diagnostic signals rather than ground truth.

### 3. Objective corruption repair

Only rows with independently defensible corruption were eligible for repair.

A total of 1,373 objectively corrupted rows were identified:

- 1,362 truncations;
- 9 foreign-script contaminations;
- 2 Unicode replacement-character errors.

Of these:

- 519 were repaired conservatively while preserving the original metadata and linguistic structure;
- 854 could not be reconstructed reliably and were replaced with newly generated sentences using the same language, lexical-domain and length metadata.

A final isolated Unicode corruption was repaired separately.

No other rows were rewritten.

See:

`corpus_repair/SAE_Corpus_Repair_Summary.md`

for the concise repair record.

## Reproducibility files

The minimum files required to document and reproduce corpus construction are:

```text
SAE/
├── README.md
├── data/
│   └── sae_train_150k_v1_2_final.jsonl
│
├── corpus_generation/
│   ├── PROMPT_POLICY.md
│   ├── BATCH_PLAN.md
│   ├── requirements.txt
│   ├── configs/
│   │   ├── generation.yaml
│   │   ├── variable_constructions.yaml
│   │   └── batch_plan_150k.csv
│   └── scripts/
│       ├── generate_150k.py
│       ├── generate_150k_fast.py
│       ├── validate_plan.py
│       └── audit_corpus.py
│
└── corpus_repair/
    ├── SAE_Corpus_Repair_Summary.md
    ├── review_sae_detector_only.py
    ├── repair_objective_corruptions.py
    ├── regenerate_unresolved_rows.py
    └── validate_final_corpus.py
```

Historical pilot corpora, old checkpoints, activation caches, review dumps, raw generation batches, logs and superseded corpus versions are not required for the main repository.

## SAE training use

For SAE activation caching and training, only the following fields should be consumed:

```text
id
text
```

The remaining metadata should be retained for corpus auditing and later feature analysis.

Before SAE training, the final corpus should be tokenized with the exact tokenizer of the target forward model and the total usable activation-token count should be recorded. Training schedules should be defined in terms of activation tokens rather than sentence count.

The first planned SAE experiment uses XGLM-564M residual-stream activations and a JumpReLU SAE architecture.

## Dataset versioning

The canonical version is:

**SAE Corpus v1.2**

File:

`sae_train_150k_v1_2_final.jsonl`

Any later filtered, text-only or model-tokenized representation should be treated as a derived artifact and should reference this file as its source.
