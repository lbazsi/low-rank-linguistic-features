import json
from typing import Dict, Any


JUDGE_SYSTEM_PROMPT = """You are a strict linguistic dataset auditor.

You evaluate contrast-pair examples for a mechanistic interpretability dataset. Each example contains a basis sentence and a changed sentence. The changed sentence should isolate the named structural contrast while keeping unrelated semantic content stable.

Return only valid JSON. Do not use markdown. Do not include explanations outside the JSON object.
"""


def build_judge_prompt(example: Dict[str, Any]) -> str:
    pair = example.get("pair", [])
    basis = next((x.get("sentence", "") for x in pair if x.get("type") == "basis"), "")
    changed = next((x.get("sentence", "") for x in pair if x.get("type") == "changed"), "")

    payload = {
        "id": example.get("id"),
        "variable_id": example.get("variable_id"),
        "variable": example.get("variable"),
        "approach": example.get("approach"),
        "language": example.get("language"),
        "surface_type": example.get("surface_type"),
        "contrast": example.get("contrast"),
        "basis_sentence": basis,
        "changed_sentence": changed,
    }

    return f"""Audit this dataset example.

Check all of the following:
1. The basis sentence is grammatical and natural enough for the stated language.
2. The changed sentence is grammatical and natural enough for the stated language.
3. The language label is correct.
4. The changed sentence isolates the intended contrast.
5. The pair does not introduce unrelated semantic drift.
6. The contrast label accurately describes the difference between the two sentences.
7. The pair is not merely a trivial lexical trigger if the target variable is structural.
8. The example is useful for probing internal representations of the stated variable.

Use this decision policy:
- "keep": no meaningful issues.
- "flag": usable but has minor or moderate concerns.
- "reject": serious issue; should not enter the dataset without repair.

Return exactly this JSON schema:
{{
  "id": "<example id>",
  "decision": "keep|flag|reject",
  "confidence": 0.0,
  "failures": [
    {{
      "category": "grammar|language_mismatch|contrast_mismatch|semantic_drift|unnatural|surface_artifact|metadata_mismatch|other",
      "severity": "minor|major",
      "message": "specific failure"
    }}
  ],
  "summary": "one sentence summary",
  "suggested_fix": "brief fix or empty string"
}}

Example to audit:
{json.dumps(payload, ensure_ascii=False, indent=2)}
"""
