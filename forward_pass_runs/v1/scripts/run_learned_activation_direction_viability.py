from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch


SENTENCE_FAMILY = "sentence_basis_changed"


def safe_torch_load(path: Path) -> dict[str, Any]:
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50, 50)))


def tensor_np(x: torch.Tensor) -> np.ndarray:
    return x.detach().cpu().float().numpy()


def probe_changed_probability(probe_state: dict[str, torch.Tensor], x: np.ndarray) -> np.ndarray:
    mean = tensor_np(probe_state["scaler_mean"])
    scale = tensor_np(probe_state["scaler_scale"])
    coef = tensor_np(probe_state["coef"]).reshape(-1)
    intercept = float(tensor_np(probe_state["intercept"]).reshape(-1)[0])
    z = ((x - mean) / scale) @ coef + intercept
    return sigmoid(z)


def load_best_sentence_probe(best_weights: dict[str, Any], variable_id: int) -> dict[str, Any]:
    states = best_weights.get("best_probe_states", best_weights)
    key = f"{SENTENCE_FAMILY}|var={int(variable_id)}"
    if key not in states:
        raise KeyError(
            f"Missing best sentence probe state for variable {variable_id}. "
            "Run train_raw_activation_probes.py without --no-save-all-weights."
        )
    return states[key]


def mean_train_delta_direction(
    pair_meta: pd.DataFrame,
    activation_tensor: torch.Tensor,
    variable_id: int,
    layer_idx: int,
) -> tuple[np.ndarray, float]:
    d = pair_meta[(pair_meta["variable_id"] == variable_id) & (pair_meta["split"] == "train")]
    if d.empty:
        raise ValueError(f"No train pairs for variable {variable_id}")

    basis_idx = d["basis_sentence_row_idx"].to_numpy(dtype=np.int64)
    changed_idx = d["changed_sentence_row_idx"].to_numpy(dtype=np.int64)

    deltas = activation_tensor[changed_idx, layer_idx, :].float() - activation_tensor[basis_idx, layer_idx, :].float()
    deltas_np = tensor_np(deltas)
    direction = deltas_np.mean(axis=0)
    norm = float(np.linalg.norm(direction))
    if norm <= 1e-8:
        raise ValueError(f"Near-zero mean direction for variable {variable_id}")

    median_delta_norm = float(np.median(np.linalg.norm(deltas_np, axis=1)))
    unit_direction = direction / norm
    return unit_direction.astype(np.float32), median_delta_norm


def run_viability_check(
    cache: dict[str, Any],
    pair_meta: pd.DataFrame,
    evidence: pd.DataFrame,
    best_weights: dict[str, Any],
    alpha: float,
    max_pairs_per_variable: int | None,
    seed: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    ready_col = "ready_for_learned_activation_direction_viability"
    if ready_col in evidence.columns:
        todo = evidence[evidence[ready_col] == True].copy()
    else:
        todo = evidence.copy()

    for _, ev in todo.iterrows():
        vid = int(ev["variable_id"])
        variable = str(ev["variable"])
        repr_name = str(ev.get("sentence_best_representation", "final_token"))
        layer_idx = int(ev["sentence_best_layer_idx"])

        if repr_name not in cache:
            raise KeyError(f"Activation cache has no representation '{repr_name}'")

        tensor = cache[repr_name].float()
        probe_bundle = load_best_sentence_probe(best_weights, vid)
        probe_state = probe_bundle["state"]

        unit_direction, median_delta_norm = mean_train_delta_direction(pair_meta, tensor, vid, layer_idx)
        learned_direction = alpha * median_delta_norm * unit_direction

        test_pairs = pair_meta[(pair_meta["variable_id"] == vid) & (pair_meta["split"] == "test")].copy()
        if max_pairs_per_variable is not None and len(test_pairs) > max_pairs_per_variable:
            keep = rng.choice(test_pairs.index.to_numpy(), size=max_pairs_per_variable, replace=False)
            test_pairs = test_pairs.loc[keep].sort_index()

        basis_idx = test_pairs["basis_sentence_row_idx"].to_numpy(dtype=np.int64)
        changed_idx = test_pairs["changed_sentence_row_idx"].to_numpy(dtype=np.int64)

        basis = tensor_np(tensor[basis_idx, layer_idx, :])
        changed = tensor_np(tensor[changed_idx, layer_idx, :])
        moved = basis + learned_direction.reshape(1, -1)
        reversed_move = basis - learned_direction.reshape(1, -1)

        p_basis = probe_changed_probability(probe_state, basis)
        p_changed = probe_changed_probability(probe_state, changed)
        p_moved = probe_changed_probability(probe_state, moved)
        p_reversed = probe_changed_probability(probe_state, reversed_move)

        direction_effect = p_moved - p_basis
        reverse_effect = p_reversed - p_basis
        changed_gap_closed = (p_moved - p_basis) / np.maximum(p_changed - p_basis, 1e-6)

        effect_mean = float(np.mean(direction_effect))
        effect_median = float(np.median(direction_effect))
        positive_rate = float(np.mean(direction_effect > 0.0))
        reverse_mean = float(np.mean(reverse_effect))
        gap_closed_median = float(np.median(changed_gap_closed))

        passed = bool(effect_mean >= 0.10 and positive_rate >= 0.75 and reverse_mean <= -0.03)

        rows.append({
            "variable_id": vid,
            "variable": variable,
            "viability_mode": "learned_activation_direction_probe_check",
            "representation": repr_name,
            "layer_idx": layer_idx,
            "alpha": float(alpha),
            "test_pairs_used": int(len(test_pairs)),
            "median_train_delta_norm": float(median_delta_norm),
            "direction_effect_mean": effect_mean,
            "direction_effect_median": effect_median,
            "direction_effect_positive_rate": positive_rate,
            "reverse_direction_effect_mean": reverse_mean,
            "changed_probability_basis_mean": float(np.mean(p_basis)),
            "changed_probability_changed_mean": float(np.mean(p_changed)),
            "changed_probability_moved_basis_mean": float(np.mean(p_moved)),
            "changed_probability_reverse_moved_basis_mean": float(np.mean(p_reversed)),
            "median_fraction_of_probe_gap_closed": gap_closed_median,
            "learned_activation_direction_viability_pass": passed,
            "learned_activation_direction_viability_note": (
                "Adding the learned basis-to-changed direction to held-out basis activations moved them toward the changed class under the selected probe."
            ),
        })

    return pd.DataFrame(rows).sort_values("variable_id").reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether learned activation directions remain viable on held-out examples.")
    parser.add_argument("--activation-cache", type=Path, required=True)
    parser.add_argument("--pair-metadata", type=Path, required=True)
    parser.add_argument("--evidence-status", type=Path, required=True)
    parser.add_argument("--best-weights", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--max-pairs-per-variable", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    cache = safe_torch_load(args.activation_cache)
    pair_meta = pd.read_parquet(args.pair_metadata)
    evidence = pd.read_parquet(args.evidence_status) if args.evidence_status.suffix == ".parquet" else pd.read_csv(args.evidence_status)
    best_weights = safe_torch_load(args.best_weights)

    results = run_viability_check(
        cache=cache,
        pair_meta=pair_meta,
        evidence=evidence,
        best_weights=best_weights,
        alpha=args.alpha,
        max_pairs_per_variable=args.max_pairs_per_variable,
        seed=args.seed,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results.to_parquet(args.output_dir / "learned_activation_direction_viability_results.parquet", index=False)
    results.to_csv(args.output_dir / "learned_activation_direction_viability_results.csv", index=False)
    with (args.output_dir / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump({"script": "run_learned_activation_direction_viability.py", "args": vars(args), "rows": int(len(results))}, f, indent=2, default=str)

    print("Learned activation direction viability check complete.")
    print(args.output_dir / "learned_activation_direction_viability_results.parquet")
    if not results.empty:
        cols = [
            "variable_id",
            "variable",
            "direction_effect_mean",
            "direction_effect_positive_rate",
            "reverse_direction_effect_mean",
            "learned_activation_direction_viability_pass",
        ]
        print(results[cols].to_string(index=False))


if __name__ == "__main__":
    main()
