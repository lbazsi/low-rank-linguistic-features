import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def read_jsonl(path: Path) -> Iterable[Tuple[int, Optional[Dict[str, Any]], Optional[str]]]:
    """Yield (line_number, object_or_none, raw_error_or_none)."""
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                yield i, None, "empty_line"
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as e:
                yield i, None, f"json_decode_error: {e}"
                continue
            if not isinstance(obj, dict):
                yield i, None, "json_line_is_not_object"
                continue
            yield i, obj, None


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def iter_jsonl_files(input_path: Path) -> List[Path]:
    if input_path.is_file():
        return [input_path]
    return sorted(input_path.rglob("*.jsonl"))


def canonicalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‘’]", "'", text)
    return text


def split_from_index(index: int) -> str:
    if 1 <= index <= 400:
        return "train"
    if 401 <= index <= 450:
        return "val"
    if 451 <= index <= 500:
        return "test"
    return "out_of_range"


def parse_example_id(example_id: str) -> Optional[Tuple[int, int]]:
    """Parse IDs like 26_001 into (variable_id, index)."""
    match = re.fullmatch(r"(\d{1,2})_(\d{3})", example_id)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def is_empty_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    if isinstance(value, dict) and len(value) == 0:
        return True
    return False
