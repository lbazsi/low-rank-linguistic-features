#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from tqdm import tqdm

from feature_audit.utils import iter_jsonl_files, read_jsonl, write_jsonl
from feature_audit.validator import ValidationConfig, ValidationState, validate_example
from feature_audit.judge_qwen import run_qwen_judge


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and judge feature-dataset JSONL files.")

    parser.add_argument("--input", required=True, help="Input JSONL file or directory containing JSONL files.")
    parser.add_argument("--output", required=True, help="Output audit directory.")
    parser.add_argument(
        "--mode",
        choices=["validate", "validate_and_judge"],
        default="validate",
        help="Run deterministic validation only, or validation plus Qwen judge.",
    )

    parser.add_argument("--min-sentence-chars", type=int, default=5)
    parser.add_argument("--max-sentence-chars", type=int, default=600)
    parser.add_argument("--max-examples-per-variable", type=int, default=500)
    parser.add_argument(
        "--no-strict-surface-type",
        action="store_true",
        help="Disable strict consistency checks between approach, language, and surface_type.",
    )

    parser.add_argument("--model", default="Qwen/Qwen2.5-14B-Instruct")
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--max-model-len", type=int, default=8192)
    parser.add_argument("--judge-batch-size", type=int, default=8)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=700)

    parser.add_argument(
        "--judge-backend",
        choices=["local_vllm", "server"],
        default="local_vllm",
        help="local_vllm loads the model inside this script; server uses a persistent vLLM server.",
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--api-key", default="local-qwen-key")
    parser.add_argument("--top-p", type=float, default=0.8)
    parser.add_argument("--judge-concurrency", type=int, default=8)

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = iter_jsonl_files(input_path)
    if not files:
        raise FileNotFoundError(f"No JSONL files found under: {input_path}")

    config = ValidationConfig(
        min_sentence_chars=args.min_sentence_chars,
        max_sentence_chars=args.max_sentence_chars,
        max_examples_per_variable=args.max_examples_per_variable,
        strict_surface_type=not args.no_strict_surface_type,
    )
    state = ValidationState()

    validation_passed: List[Dict[str, Any]] = []
    validation_failed: List[Dict[str, Any]] = []
    raw_json_errors: List[Dict[str, Any]] = []

    total_lines = 0

    for path in files:
        rows = list(read_jsonl(path))
        for line_number, obj, raw_error in tqdm(rows, desc=f"Validating {path.name}"):
            total_lines += 1

            if raw_error is not None:
                raw_json_errors.append(
                    {
                        "source_file": str(path),
                        "line_number": line_number,
                        "passed": False,
                        "errors": [{"code": "raw_jsonl_error", "message": raw_error}],
                        "warnings": [],
                        "example": None,
                    }
                )
                continue

            assert obj is not None
            passed, result = validate_example(
                obj,
                source_file=str(path),
                line_number=line_number,
                state=state,
                config=config,
            )

            if passed:
                validation_passed.append(result)
            else:
                validation_failed.append(result)

    validation_failed_all = raw_json_errors + validation_failed

    write_jsonl(output_dir / "validation_passed.jsonl", validation_passed)
    write_jsonl(output_dir / "validation_failed.jsonl", validation_failed_all)

    judge_results: List[Dict[str, Any]] = []
    judge_flagged: List[Dict[str, Any]] = []
    accepted_after_judge: List[Dict[str, Any]] = []

    if args.mode == "validate_and_judge":
        examples_for_judge = [row["example"] for row in validation_passed]
        if args.judge_backend == "server":
            from feature_audit.judge_server import run_server_judge

            judge_results = run_server_judge(
                examples_for_judge,
                base_url=args.base_url,
                api_key=args.api_key,
                model=args.model,
                judge_batch_size=args.judge_batch_size,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=args.top_p,
                judge_concurrency=args.judge_concurrency,
            )
        else:
            judge_results = run_qwen_judge(
                examples_for_judge,
                model=args.model,
                tensor_parallel_size=args.tensor_parallel_size,
                max_model_len=args.max_model_len,
                judge_batch_size=args.judge_batch_size,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )

        judge_flagged = [row for row in judge_results if row.get("decision") in {"flag", "reject"}]
        accepted_after_judge = [row for row in judge_results if row.get("decision") == "keep"]

        write_jsonl(output_dir / "judge_results.jsonl", judge_results)
        write_jsonl(output_dir / "judge_flagged.jsonl", judge_flagged)
        write_jsonl(output_dir / "accepted_after_judge.jsonl", accepted_after_judge)

    summary = {
        "input": str(input_path),
        "files_scanned": [str(p) for p in files],
        "total_lines": total_lines,
        "validation_passed": len(validation_passed),
        "validation_failed": len(validation_failed_all),
        "mode": args.mode,
        "judge_total": len(judge_results),
        "judge_keep": sum(1 for r in judge_results if r.get("decision") == "keep"),
        "judge_flag": sum(1 for r in judge_results if r.get("decision") == "flag"),
        "judge_reject": sum(1 for r in judge_results if r.get("decision") == "reject"),
    }

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
