# 150k SAE Corpus Generation Policy

## Two-pass generation

Every example is produced in two genuinely separate model calls:

1. **Sentence pass** — generate exactly one natural sentence from a pre-defined batch brief.
2. **Annotation pass** — provide that finished sentence to the model in a new prompt and ask it to produce the complete JSON object.

The annotation call must not rewrite the sentence. The generator checks that the JSON `text` field exactly matches the sentence produced in pass 1.

## Final JSONL schema

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

`variables_present` is a conservative audit annotation. The SAE will not receive these labels.

## Batch design

- 3,000 batches
- 50 examples per batch
- 150,000 examples total
- 40 variables
- 5 construction families per variable
- 15 batches per variable × construction combination
- 750 primary examples per construction family
- 3,750 primary examples per variable

Each batch has one primary variable, one construction family, one planned language, three rotating lexical domains, and a 15/25/10 short/medium/long target mix.

The schedule is static in `configs/batch_plan_150k.csv`. It is not sampled at runtime.

## Sentence-generation rules

The model must:

- write exactly one plausible standalone sentence;
- write in the planned language, using its normal script and orthography;
- clearly instantiate the planned construction;
- keep the primary linguistic variable structurally relevant;
- fit the assigned lexical domain and approximate length target;
- vary vocabulary, participants, predicates, sentence openings, and discourse setting;
- allow other linguistic variables to occur naturally;
- avoid grammar-book commentary and metalinguistic labels;
- avoid deterministic templates, slot filling, pseudo-morphology, or artificial token corruption;
- avoid relying on one stock word or marker when the construction admits alternatives.

## Annotation rules

The second model call sees only the finished sentence plus the planned primary target as context. It must:

- copy the sentence verbatim into `text`;
- give the actual ISO-style language code;
- conservatively list all clearly instantiated variables from the 40-variable catalog;
- include the primary variable only if the sentence genuinely realizes it;
- choose the closest allowed lexical domain;
- assign `short`, `medium`, or `long`.

The generation script rejects and retries examples when the JSON is invalid, the planned language is not recovered, the primary variable is absent, or the sentence duplicates an earlier sentence.

## Resumability

Each batch is written independently. A completed valid batch is skipped on restart. Raw sentence-pass outputs are also preserved for provenance. The final 150k JSONL is assembled only from valid completed batches.
