import json
from typing import Dict, Any


JUDGE_SYSTEM_PROMPT = """You are a strict but fair linguistic dataset auditor.

You evaluate contrast-pair examples for a mechanistic interpretability dataset. Each example contains a basis sentence and a changed sentence. The changed sentence should isolate the named structural contrast while keeping unrelated semantic content stable.

Important judging principle:
Do not flag a meaning difference as semantic drift if that difference is exactly the intended linguistic contrast.

For example:
- In causativity examples, adding a causer can be the intended contrast.
- In valency-change examples, adding or removing an argument can be the intended contrast.
- In transitivity examples, changing from intransitive to transitive, transitive to ditransitive, or adding an object/beneficiary/instrument can be the intended contrast.
- In voice examples, changing agent prominence or hiding the agent can be the intended contrast.
- In evidentiality examples, changing the information source can be the intended contrast.
- In modality examples, changing obligation, permission, possibility, or ability can be the intended contrast.

Only flag semantic drift when the pair changes content outside the target contrast, such as:
- different time
- different place
- different event
- different result
- different patient/theme
- different domain
- different factual scenario
- different emotional intensity
- different specificity level when not required by the contrast

For causativity, transitivity, and valency-change examples:
Do not reject merely because the changed sentence adds a causer, changes who initiates the event, or changes the number of arguments. Reject or flag only if the causer makes the sentence ungrammatical, unnatural, pragmatically implausible, or changes the core event beyond the intended valency/causativity contrast.

Your job is not to enforce perfect semantic identity. Your job is to decide whether the example is useful for testing the stated linguistic contrast.

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

Semantic-drift policy:
Do not treat the intended contrast itself as semantic drift. Some variables require real structural or argument-structure changes. For causativity, transitivity, and valency-change examples, adding a causer, causee, object, beneficiary, or instrument may be correct and should not be flagged unless it introduces an unrelated event change, time/place change, malformed language, or pragmatic implausibility.

For causativity / valency-change examples, focus especially on:
- whether the added causer is plausible;
- whether the caused event remains the same core event;
- whether time and place remain stable;
- whether the changed sentence is grammatical and natural;
- whether the basis and changed pair still isolate the intended valency or causativity contrast.

Use this decision policy:
- "keep": no meaningful issues, or only the intended contrast changes.
- "flag": usable but has concrete minor or moderate concerns that a human may want to inspect.
- "reject": serious issue; should not enter the dataset without repair.

Do not choose "flag" merely because the sentence pair changes valency, adds a causer, or changes argument structure when that is the stated contrast.

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
