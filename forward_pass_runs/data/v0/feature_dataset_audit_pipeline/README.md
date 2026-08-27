# Feature Dataset Audit Pipeline

This pipeline audits synthetic feature-dataset JSONL files before they are accepted into the project.

It has two stages:

1. **Deterministic validation**
   - valid JSONL
   - required fields
   - ID format
   - variable ID consistency
   - language code validity
   - surface type validity
   - contrast field validity
   - split matches ID range
   - basis/changed pair structure
   - sentence length
   - duplicate sentence pairs
   - duplicate IDs
   - empty fields

2. **LLM judge validation**
   - uses `Qwen/Qwen2.5-14B-Instruct`
   - checks linguistic validity, grammaticality, language match, semantic drift, contrast isolation, and surface-artifact problems
   - only runs on examples that pass deterministic validation

## Expected example schema

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

## Install

For validator-only use:

```bash
pip install -r requirements.txt
```

For Lambda GPU judging with vLLM:

```bash
pip install -r requirements-lambda.txt
```

## Run validator only

```bash
python validate_and_judge.py \
  --input data/feature_dataset \
  --output audit_outputs \
  --mode validate
```

## Run validator + Qwen judge

```bash
python validate_and_judge.py \
  --input data/feature_dataset \
  --output audit_outputs \
  --mode validate_and_judge \
  --model Qwen/Qwen2.5-14B-Instruct \
  --tensor-parallel-size 1 \
  --max-model-len 8192 \
  --judge-batch-size 8
```

## Outputs

```text
audit_outputs/
  validation_passed.jsonl
  validation_failed.jsonl
  judge_results.jsonl
  judge_flagged.jsonl
  accepted_after_judge.jsonl
  summary.json
```

`validation_failed.jsonl` contains examples that failed deterministic checks. These are not sent to the LLM judge.

`validation_passed.jsonl` contains examples that passed deterministic checks and are eligible for LLM judging.

`judge_results.jsonl` contains all LLM judge results.

`judge_flagged.jsonl` contains examples the judge marked as `flag` or `reject`.

`accepted_after_judge.jsonl` contains examples that passed deterministic validation and were marked `keep` by the judge.

## Notes

The deterministic validator should be treated as mandatory. The LLM judge is useful but not authoritative. Final dataset versions should still receive a small manual review sample per variable.
