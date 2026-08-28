from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Tuple

import numpy as np
import torch
import yaml
from safetensors.torch import load_file


def load_config(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_parent(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_json(path: str | Path, obj: Any) -> None:
    path = Path(path)
    ensure_parent(path)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def append_jsonl(path: str | Path, obj: Dict[str, Any]) -> None:
    path = Path(path)
    ensure_parent(path)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def iter_jsonl(path: str | Path) -> Iterator[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except Exception as e:
                raise RuntimeError(f"Invalid JSON on line {line_no}: {e}") from e
            if "id" not in row or "text" not in row:
                raise RuntimeError(f"Line {line_no} must contain id and text.")
            yield row


def stable_split(example_id: str, seed: int, val_fraction: float) -> str:
    payload = f"{seed}:{example_id}".encode("utf-8")
    value = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big") / 2**64
    return "val" if value < val_fraction else "train"


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def torch_dtype(name: str) -> torch.dtype:
    table = {
        "float16": torch.float16,
        "fp16": torch.float16,
        "bfloat16": torch.bfloat16,
        "bf16": torch.bfloat16,
        "float32": torch.float32,
        "fp32": torch.float32,
    }
    if name not in table:
        raise ValueError(f"Unsupported dtype: {name}")
    return table[name]


def shard_paths(root: str | Path, split: str) -> List[Path]:
    d = Path(root) / split
    return sorted(d.glob("shard_*.safetensors"))


def load_manifest(root: str | Path, split: str) -> Dict[str, Any]:
    p = Path(root) / split / "manifest.json"
    if not p.exists():
        raise FileNotFoundError(f"Missing activation manifest: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_activation_shard(path: str | Path) -> torch.Tensor:
    obj = load_file(str(path), device="cpu")
    return obj["activations"]


def exact_steps_per_epoch(manifest: Dict[str, Any], batch_size: int) -> int:
    return sum(math.ceil(int(s["tokens"]) / batch_size) for s in manifest["shards"])


def activation_scale_from_manifest(manifest: Dict[str, Any], d_in: int) -> float:
    mean_norm = float(manifest["mean_l2_norm"])
    if mean_norm <= 0:
        raise ValueError("Activation mean L2 norm must be positive.")
    return math.sqrt(d_in) / mean_norm
