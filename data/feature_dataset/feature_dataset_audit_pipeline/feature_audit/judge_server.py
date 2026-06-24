from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

from openai import OpenAI
from tqdm import tqdm

from .prompts import JUDGE_SYSTEM_PROMPT, build_judge_prompt
from .judge_qwen import normalize_judge_result


class ServerJudge:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000/v1",
        api_key: str = "local-qwen-key",
        model: str = "Qwen/Qwen2.5-14B-Instruct",
        temperature: float = 0.0,
        max_tokens: int = 700,
        top_p: float = 0.8,
        concurrency: int = 8,
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=180.0)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.concurrency = max(1, concurrency)

    def judge_one(self, example: Dict[str, Any]) -> Dict[str, Any]:
        user_prompt = build_judge_prompt(example)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
            )

            raw_text = response.choices[0].message.content or ""
            return normalize_judge_result(example, raw_text)

        except Exception as e:
            return {
                "id": example.get("id"),
                "decision": "flag",
                "confidence": 0.0,
                "failures": [
                    {
                        "category": "other",
                        "severity": "major",
                        "message": f"Judge request failed: {type(e).__name__}: {e}",
                    }
                ],
                "summary": "Judge request failed.",
                "suggested_fix": "Re-run judge or inspect manually.",
                "raw_judge_output": "",
                "example": example,
            }

    def judge_many(self, examples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any] | None] = [None] * len(examples)

        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = {
                executor.submit(self.judge_one, example): idx
                for idx, example in enumerate(examples)
            }

            for future in tqdm(as_completed(futures), total=len(futures), desc="LLM judging"):
                idx = futures[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    example = examples[idx]
                    results[idx] = {
                        "id": example.get("id"),
                        "decision": "flag",
                        "confidence": 0.0,
                        "failures": [
                            {
                                "category": "other",
                                "severity": "major",
                                "message": f"Unexpected judge failure: {type(e).__name__}: {e}",
                            }
                        ],
                        "summary": "Unexpected judge failure.",
                        "suggested_fix": "Re-run judge or inspect manually.",
                        "raw_judge_output": "",
                        "example": example,
                    }

        return [r for r in results if r is not None]


def run_server_judge(
    examples: List[Dict[str, Any]],
    *,
    base_url: str,
    api_key: str,
    model: str,
    judge_batch_size: int,
    temperature: float,
    max_tokens: int,
    top_p: float,
    judge_concurrency: int = 8,
) -> List[Dict[str, Any]]:
    judge = ServerJudge(
        base_url=base_url,
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        concurrency=judge_concurrency,
    )

    # judge_batch_size is kept for CLI compatibility, but server mode now uses
    # judge_concurrency for true concurrent requests.
    return judge.judge_many(examples)
