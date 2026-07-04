import json
import re
from typing import Any, Dict, List, Optional

from tqdm import tqdm

from .prompts import JUDGE_SYSTEM_PROMPT, build_judge_prompt


def extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Robustly extract the first JSON object from a model response."""
    text = text.strip()
    if not text:
        return None

    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None

    candidate = text[start : end + 1]
    try:
        obj = json.loads(candidate)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        return None

    return None


def normalize_judge_result(example: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
    obj = extract_json_object(raw_text)
    if obj is None:
        return {
            "id": example.get("id"),
            "decision": "flag",
            "confidence": 0.0,
            "failures": [
                {
                    "category": "other",
                    "severity": "major",
                    "message": "Judge output could not be parsed as JSON.",
                }
            ],
            "summary": "Judge output parse failure.",
            "suggested_fix": "Re-run judge or manually inspect.",
            "raw_judge_output": raw_text,
            "example": example,
        }

    decision = obj.get("decision")
    if decision not in {"keep", "flag", "reject"}:
        decision = "flag"

    failures = obj.get("failures")
    if not isinstance(failures, list):
        failures = [
            {
                "category": "other",
                "severity": "major",
                "message": "Judge did not return a valid failures list.",
            }
        ]

    try:
        confidence = float(obj.get("confidence", 0.0))
    except Exception:
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))

    return {
        "id": example.get("id"),
        "decision": decision,
        "confidence": confidence,
        "failures": failures,
        "summary": str(obj.get("summary", "")),
        "suggested_fix": str(obj.get("suggested_fix", "")),
        "raw_judge_output": raw_text,
        "example": example,
    }


class QwenJudge:
    def __init__(
        self,
        model: str = "Qwen/Qwen2.5-14B-Instruct",
        tensor_parallel_size: int = 1,
        max_model_len: int = 8192,
        temperature: float = 0.0,
        max_tokens: int = 700,
    ):
        try:
            from vllm import LLM, SamplingParams
        except ImportError as e:
            raise ImportError(
                "vLLM is required for QwenJudge. Install requirements-lambda.txt."
            ) from e

        self.SamplingParams = SamplingParams
        self.llm = LLM(
            model=model,
            tensor_parallel_size=tensor_parallel_size,
            max_model_len=max_model_len,
            trust_remote_code=True,
        )
        self.sampling_params = SamplingParams(
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def _format_chat(self, user_prompt: str) -> str:
        return (
            "<|im_start|>system\n"
            + JUDGE_SYSTEM_PROMPT
            + "<|im_end|>\n"
            + "<|im_start|>user\n"
            + user_prompt
            + "<|im_end|>\n"
            + "<|im_start|>assistant\n"
        )

    def judge_batch(self, examples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        prompts = [self._format_chat(build_judge_prompt(ex)) for ex in examples]
        outputs = self.llm.generate(prompts, self.sampling_params)
        results: List[Dict[str, Any]] = []

        for example, output in zip(examples, outputs):
            try:
                raw_text = output.outputs[0].text
            except Exception:
                raw_text = ""
            results.append(normalize_judge_result(example, raw_text))

        return results


def run_qwen_judge(
    examples: List[Dict[str, Any]],
    *,
    model: str,
    tensor_parallel_size: int,
    max_model_len: int,
    judge_batch_size: int,
    temperature: float,
    max_tokens: int,
) -> List[Dict[str, Any]]:
    judge = QwenJudge(
        model=model,
        tensor_parallel_size=tensor_parallel_size,
        max_model_len=max_model_len,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    all_results: List[Dict[str, Any]] = []
    for i in tqdm(range(0, len(examples), judge_batch_size), desc="LLM judging"):
        batch = examples[i : i + judge_batch_size]
        all_results.extend(judge.judge_batch(batch))
    return all_results
