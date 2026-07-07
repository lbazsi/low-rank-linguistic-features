# scripts/flatten_feature_pairs.py

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_TOP_LEVEL_FIELDS = [
    "id",
    "variable_id",
    "variable",
    "approach",
    "language",
    "surface_type",
    "contrast",
    "split",
    "pair",
]

REQUIRED_PAIR_FIELDS = ["type", "sentence"]

VALID_PAIR_TYPES = {"basis", "changed"}
TYPE_ORDER = {"basis": 0, "changed": 1}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8-sig") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {path} at line {line_num}: {e}") from e

            if not isinstance(obj, dict):
                raise ValueError(f"Expected JSON object in {path} at line {line_num}")

            obj["_source_file"] = path.name
            obj["_source_line"] = line_num
            records.append(obj)

    return records


def validate_top_level_record(obj: dict[str, Any]) -> None:
    source = f"{obj.get('_source_file')}:{obj.get('_source_line')}"

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in obj:
            raise ValueError(f"Missing top-level field '{field}' in {source}")

    if not isinstance(obj["pair"], list):
        raise ValueError(f"'pair' must be a list in {source}")

    if len(obj["pair"]) != 2:
        raise ValueError(f"'pair' must contain exactly 2 items in {source}")

    seen_types = set()

    for item in obj["pair"]:
        if not isinstance(item, dict):
            raise ValueError(f"Each pair item must be an object in {source}")

        for field in REQUIRED_PAIR_FIELDS:
            if field not in item:
                raise ValueError(f"Missing pair field '{field}' in {source}")

        pair_type = item["type"]

        if pair_type not in VALID_PAIR_TYPES:
            raise ValueError(
                f"Invalid pair type '{pair_type}' in {source}; "
                f"expected one of {sorted(VALID_PAIR_TYPES)}"
            )

        if pair_type in seen_types:
            raise ValueError(f"Duplicate pair type '{pair_type}' in {source}")

        seen_types.add(pair_type)

        sentence = item["sentence"]

        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError(f"Empty or invalid sentence for type '{pair_type}' in {source}")

    if seen_types != VALID_PAIR_TYPES:
        raise ValueError(
            f"Pair must contain exactly one basis and one changed item in {source}"
        )


def flatten_record(obj: dict[str, Any]) -> list[dict[str, Any]]:
    validate_top_level_record(obj)

    rows = []

    for item in obj["pair"]:
        pair_type = item["type"]

        row = {
            "sentence_id": f"{obj['id']}_{pair_type}",
            "pair_id": obj["id"],
            "variable_id": obj["variable_id"],
            "variable": obj["variable"],
            "approach": obj["approach"],
            "language": obj["language"],
            "surface_type": obj["surface_type"],
            "contrast": obj["contrast"],
            "split": obj["split"],
            "type": pair_type,
            "sentence": item["sentence"],
            "source_file": obj["_source_file"],
            "source_line": obj["_source_line"],
        }

        rows.append(row)

    return rows


def extract_numeric_suffix(pair_id: str) -> int:
    """
    Converts ids like '26_001' into 1 for stable sorting.
    Falls back to a large number if the format is unexpected.
    """
    match = re.search(r"_(\d+)$", pair_id)
    if match is None:
        return 10**9
    return int(match.group(1))


def flatten_feature_dataset(input_dir: Path, pattern: str, output_path: Path) -> pd.DataFrame:
    input_files = sorted(input_dir.glob(pattern))

    if not input_files:
        raise FileNotFoundError(
            f"No files found in {input_dir} matching pattern '{pattern}'"
        )

    all_rows = []

    for path in input_files:
        records = load_jsonl(path)

        for obj in records:
            all_rows.extend(flatten_record(obj))

    df = pd.DataFrame(all_rows)

    if df.empty:
        raise ValueError("No rows were produced. Check your input files.")

    duplicate_sentence_ids = df[df["sentence_id"].duplicated(keep=False)]

    if not duplicate_sentence_ids.empty:
        examples = duplicate_sentence_ids["sentence_id"].head(20).tolist()
        raise ValueError(f"Duplicate sentence_id values found, e.g. {examples}")

    duplicate_pair_type = df[df.duplicated(subset=["pair_id", "type"], keep=False)]

    if not duplicate_pair_type.empty:
        examples = duplicate_pair_type[["pair_id", "type"]].head(20).to_dict("records")
        raise ValueError(f"Duplicate pair_id/type rows found, e.g. {examples}")

    df["_pair_num"] = df["pair_id"].map(extract_numeric_suffix)
    df["_type_order"] = df["type"].map(TYPE_ORDER)

    df = df.sort_values(
        by=["variable_id", "_pair_num", "_type_order"],
        kind="stable",
    ).drop(columns=["_pair_num", "_type_order"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    return df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Flatten feature contrast-pair JSONL files into one model-input parquet."
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/feature_dataset"),
        help="Directory containing feature JSONL files.",
    )

    parser.add_argument(
        "--pattern",
        type=str,
        default="feature*_001_500.jsonl",
        help="Glob pattern for input files, e.g. feature*_001_500.jsonl.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/probe_data/feature_inputs.parquet"),
        help="Output parquet path.",
    )

    args = parser.parse_args()

    df = flatten_feature_dataset(
        input_dir=args.input_dir,
        pattern=args.pattern,
        output_path=args.output,
    )

    print(f"Wrote: {args.output}")
    print(f"Rows: {len(df):,}")
    print(f"Pairs: {df['pair_id'].nunique():,}")
    print(f"Variables: {df['variable_id'].nunique():,}")
    print()
    print("Rows by type:")
    print(df["type"].value_counts().sort_index().to_string())
    print()
    print("Rows by split:")
    print(df["split"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()