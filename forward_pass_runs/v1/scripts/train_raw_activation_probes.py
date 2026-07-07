from __future__ import annotations

import argparse
import json
import os
import random
import shutil
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score
from joblib import Parallel, delayed
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

try:
    from threadpoolctl import threadpool_limits
except ImportError:  # pragma: no cover - scikit-learn normally installs this.
    threadpool_limits = None


SPLITS = ["train", "val", "test"]

SENTENCE_FAMILY = "sentence_basis_changed"
# Directional feature-control: can a probe recover the activation-space direction
# from basis -> changed on held-out examples? This is the mechanistically useful
# delta control. Positive = changed - basis. Negative = basis - changed.
DELTA_DIRECTION_FAMILY = "delta_direction_basis_to_changed"

TEXT_SENTENCE_FAMILY = "text_sentence_basis_changed"
TEXT_DELTA_DIRECTION_FAMILY = "text_delta_direction_basis_to_changed"

NULL_SENTENCE_FAMILY = "null_label_shuffle_sentence"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def safe_torch_load(path: Path) -> dict[str, Any]:
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


def safe_auroc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    try:
        return float(roc_auc_score(y_true, y_score))
    except ValueError:
        return float("nan")


def prediction_scores(model: Pipeline, x: Any) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(x)[:, 1]
    return model.decision_function(x)


def evaluate(model: Pipeline, x: Any, y: np.ndarray, split: str) -> dict[str, float | int]:
    pred = model.predict(x)
    score = prediction_scores(model, x)

    return {
        f"{split}_accuracy": float(accuracy_score(y, pred)),
        f"{split}_balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        f"{split}_f1": float(f1_score(y, pred, zero_division=0)),
        f"{split}_auroc": safe_auroc(y, score),
        f"{split}_n": int(len(y)),
        f"{split}_positive_rate": float(np.mean(y)),
    }


def bootstrap_auroc_ci(
    y_true: np.ndarray,
    y_score: np.ndarray,
    n_bootstrap: int,
    seed: int,
    confidence: float = 0.95,
) -> dict[str, float | int]:
    if n_bootstrap <= 0 or len(y_true) == 0 or len(np.unique(y_true)) < 2:
        return {"ci_lower": np.nan, "ci_upper": np.nan, "bootstrap_valid_samples": 0}

    rng = np.random.default_rng(seed)
    n = len(y_true)
    values: list[float] = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        y_sample = y_true[idx]
        if len(np.unique(y_sample)) < 2:
            continue
        values.append(safe_auroc(y_sample, y_score[idx]))

    values = [v for v in values if not np.isnan(v)]
    if not values:
        return {"ci_lower": np.nan, "ci_upper": np.nan, "bootstrap_valid_samples": 0}

    alpha = (1.0 - confidence) / 2.0
    lo, hi = np.quantile(np.asarray(values, dtype=np.float64), [alpha, 1.0 - alpha])
    return {
        "ci_lower": float(lo),
        "ci_upper": float(hi),
        "bootstrap_valid_samples": int(len(values)),
    }


def add_bootstrap_columns(
    row: dict[str, Any],
    model: Pipeline,
    data: dict[str, tuple[Any, np.ndarray]],
    n_bootstrap: int,
    seed: int,
) -> dict[str, Any]:
    if n_bootstrap <= 0:
        return row
    for split_idx, split in enumerate(["val", "test"]):
        x, y = data[split]
        score = prediction_scores(model, x)
        ci = bootstrap_auroc_ci(y, score, n_bootstrap=n_bootstrap, seed=seed + 10_000 * split_idx)
        row[f"{split}_auroc_ci_lower"] = ci["ci_lower"]
        row[f"{split}_auroc_ci_upper"] = ci["ci_upper"]
        row[f"{split}_auroc_bootstrap_valid_samples"] = ci["bootstrap_valid_samples"]
    return row


def activation_model(c: float, max_iter: int, seed: int) -> Pipeline:
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "logreg",
                LogisticRegression(
                    penalty="l2",
                    C=c,
                    solver="lbfgs",
                    max_iter=max_iter,
                    random_state=seed,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def text_model(kind: str, max_features: int, c: float, max_iter: int, seed: int) -> Pipeline:
    if kind == "word_tfidf":
        return Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        analyzer="word",
                        ngram_range=(1, 2),
                        lowercase=False,
                        max_features=max_features,
                        min_df=1,
                    ),
                ),
                (
                    "logreg",
                    LogisticRegression(
                        penalty="l2",
                        C=c,
                        solver="lbfgs",
                        max_iter=max_iter,
                        random_state=seed,
                        class_weight="balanced",
                    ),
                ),
            ]
        )

    if kind == "char_tfidf":
        return Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        analyzer="char",
                        ngram_range=(3, 5),
                        lowercase=False,
                        max_features=max_features,
                        min_df=1,
                    ),
                ),
                (
                    "logreg",
                    LogisticRegression(
                        penalty="l2",
                        C=c,
                        solver="lbfgs",
                        max_iter=max_iter,
                        random_state=seed,
                        class_weight="balanced",
                    ),
                ),
            ]
        )

    if kind == "length_punct":
        return activation_model(c=c, max_iter=max_iter, seed=seed)

    raise ValueError(f"Unknown text baseline kind: {kind}")


def text_length_features(texts: list[str]) -> np.ndarray:
    rows = []
    for s in texts:
        rows.append(
            [
                len(s),
                len(s.split()),
                sum(ch.isupper() for ch in s),
                sum(ch.isdigit() for ch in s),
                sum(ch.isspace() for ch in s),
                s.count("."),
                s.count(","),
                s.count(";"),
                s.count(":"),
                s.count("?"),
                s.count("!"),
                s.count("'"),
                s.count('"'),
                s.count("-"),
                s.count("("),
                s.count(")"),
                s.count("["),
                s.count("]"),
                s.count("/"),
            ]
        )
    return np.asarray(rows, dtype=np.float32)


def tensor_np(x: torch.Tensor) -> np.ndarray:
    return x.detach().cpu().float().numpy()


def probe_state(model: Pipeline) -> dict[str, torch.Tensor]:
    scaler: StandardScaler = model.named_steps["scaler"]
    logreg: LogisticRegression = model.named_steps["logreg"]
    return {
        "scaler_mean": torch.tensor(scaler.mean_, dtype=torch.float32),
        "scaler_scale": torch.tensor(scaler.scale_, dtype=torch.float32),
        "coef": torch.tensor(logreg.coef_, dtype=torch.float32),
        "intercept": torch.tensor(logreg.intercept_, dtype=torch.float32),
        "classes": torch.tensor(logreg.classes_, dtype=torch.long),
    }


def validate_inputs(cache: dict[str, Any], sentence_meta: pd.DataFrame, pair_meta: pd.DataFrame) -> None:
    required_cache = {"final_token", "mean_pooled"}
    missing_cache = required_cache - set(cache.keys())
    if missing_cache:
        raise ValueError(f"Activation cache missing keys: {sorted(missing_cache)}")

    required_sentence = {
        "sentence_row_idx",
        "sentence_id",
        "pair_id",
        "variable_id",
        "variable",
        "split",
        "type",
        "sentence",
        "marker_family",
        "lexical_domain",
    }
    required_pair = {
        "pair_row_idx",
        "pair_id",
        "variable_id",
        "variable",
        "split",
        "basis_sentence_row_idx",
        "changed_sentence_row_idx",
        "marker_family",
        "lexical_domain",
    }

    missing_sentence = required_sentence - set(sentence_meta.columns)
    missing_pair = required_pair - set(pair_meta.columns)

    if missing_sentence:
        raise ValueError(f"sentence metadata missing columns: {sorted(missing_sentence)}")
    if missing_pair:
        raise ValueError(f"pair metadata missing columns: {sorted(missing_pair)}")

    if len(sentence_meta) != cache["final_token"].shape[0]:
        raise ValueError("sentence metadata row count does not match final_token")
    if len(sentence_meta) != cache["mean_pooled"].shape[0]:
        raise ValueError("sentence metadata row count does not match mean_pooled")

    observed = set(sentence_meta["type"].unique())
    if observed != {"basis", "changed"}:
        raise ValueError(f"Expected basis/changed types, got {sorted(observed)}")

    for split in SPLITS:
        if split not in set(sentence_meta["split"].unique()):
            raise ValueError(f"Missing sentence split: {split}")
        if split not in set(pair_meta["split"].unique()):
            raise ValueError(f"Missing pair split: {split}")

    for key in required_cache:
        x = cache[key].float()
        if torch.isnan(x).any().item():
            raise ValueError(f"{key} contains NaN")
        if torch.isinf(x).any().item():
            raise ValueError(f"{key} contains Inf")


def get_layer_names(cache: dict[str, Any]) -> list[str]:
    if "layer_names" in cache and cache["layer_names"] is not None:
        return list(cache["layer_names"])
    return [f"layer_{i}" for i in range(int(cache["final_token"].shape[1]))]


def variables(sentence_meta: pd.DataFrame) -> pd.DataFrame:
    return (
        sentence_meta[["variable_id", "variable"]]
        .drop_duplicates()
        .sort_values("variable_id")
        .reset_index(drop=True)
    )


def sentence_activation_data(
    sentence_meta: pd.DataFrame,
    activation_tensor: torch.Tensor,
    variable_id: int,
    layer_idx: int,
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    var = sentence_meta[sentence_meta["variable_id"] == variable_id]
    out = {}
    for split in SPLITS:
        d = var[var["split"] == split]
        idx = d["sentence_row_idx"].to_numpy(dtype=np.int64)
        y = (d["type"].to_numpy() == "changed").astype(np.int64)
        x = tensor_np(activation_tensor[idx, layer_idx, :])
        out[split] = (x, y)
    return out


def delta_direction_activation_data(
    pair_meta: pd.DataFrame,
    activation_tensor: torch.Tensor,
    variable_id: int,
    layer_idx: int,
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Build a held-out direction-consistency task for pair deltas.

    Positive examples are the actual intervention direction changed - basis.
    Negative examples are the reversed direction basis - changed for the exact
    same pairs. This asks whether the linguistic transformation has a stable,
    reusable direction in activation space.
    """
    var = pair_meta[pair_meta["variable_id"] == variable_id]
    out = {}

    for split in SPLITS:
        d = var[var["split"] == split].reset_index(drop=True)

        basis_idx = d["basis_sentence_row_idx"].to_numpy(dtype=np.int64)
        changed_idx = d["changed_sentence_row_idx"].to_numpy(dtype=np.int64)

        b = torch.tensor(basis_idx, dtype=torch.long)
        c = torch.tensor(changed_idx, dtype=torch.long)

        forward_delta = activation_tensor[c, layer_idx, :].float() - activation_tensor[b, layer_idx, :].float()
        reverse_delta = -forward_delta

        x = torch.cat([forward_delta, reverse_delta], dim=0).numpy()
        y = np.concatenate(
            [
                np.ones(len(forward_delta), dtype=np.int64),
                np.zeros(len(reverse_delta), dtype=np.int64),
            ]
        )
        out[split] = (x, y)

    return out


def train_one_activation(
    data: dict[str, tuple[np.ndarray, np.ndarray]],
    c: float,
    max_iter: int,
    seed: int,
) -> tuple[Pipeline, dict[str, float | int]]:
    model = activation_model(c=c, max_iter=max_iter, seed=seed)
    x_train, y_train = data["train"]
    model.fit(x_train, y_train)
    metrics = {}
    for split in SPLITS:
        x, y = data[split]
        metrics.update(evaluate(model, x, y, split))
    return model, metrics


def result_flags(row: dict[str, Any]) -> dict[str, Any]:
    test = row.get("test_auroc", float("nan"))
    val = row.get("val_auroc", float("nan"))
    train = row.get("train_auroc", float("nan"))

    row["suspiciously_high_test_auroc"] = bool(not np.isnan(test) and test >= 0.97)
    row["possible_overfit"] = bool(
        not np.isnan(train) and not np.isnan(val) and (train - val) >= 0.15
    )
    row["weak_signal"] = bool(not np.isnan(test) and test < 0.60)
    return row


def select_best(candidate: pd.DataFrame) -> pd.DataFrame:
    d = candidate.copy()
    d["_val_auroc"] = d["val_auroc"].fillna(-1.0)
    d["_val_bal_acc"] = d["val_balanced_accuracy"].fillna(-1.0)
    d = d.sort_values(
        ["probe_family", "variable_id", "_val_auroc", "_val_bal_acc"],
        ascending=[True, True, False, False],
        kind="stable",
    )
    out = (
        d.groupby(["probe_family", "variable_id"], as_index=False)
        .head(1)
        .drop(columns=["_val_auroc", "_val_bal_acc"])
        .reset_index(drop=True)
    )
    out["selected_by"] = "validation_auroc_then_validation_balanced_accuracy"
    return out


def train_activation_probes(
    cache: dict[str, Any],
    sentence_meta: pd.DataFrame,
    pair_meta: pd.DataFrame,
    c: float,
    max_iter: int,
    seed: int,
    save_all_weights: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any], dict[str, Any]]:
    layer_names = get_layer_names(cache)
    var_table = variables(sentence_meta)

    reprs = {
        "final_token": cache["final_token"],
        "mean_pooled": cache["mean_pooled"],
    }

    expected = len(var_table) * len(reprs) * len(layer_names) * 2
    rows = []
    all_weights = {}

    pbar = tqdm(total=expected, desc="Activation probes")

    for _, vr in var_table.iterrows():
        vid = int(vr["variable_id"])
        vname = str(vr["variable"])

        for repr_name, tensor in reprs.items():
            for layer_idx, layer_name in enumerate(layer_names):
                # Sentence task.
                key = f"{SENTENCE_FAMILY}|var={vid}|repr={repr_name}|layer={layer_idx}"
                data = sentence_activation_data(sentence_meta, tensor, vid, layer_idx)
                model, metrics = train_one_activation(data, c, max_iter, seed)
                row = {
                    "candidate_key": key,
                    "probe_family": SENTENCE_FAMILY,
                    "variable_id": vid,
                    "variable": vname,
                    "representation": repr_name,
                    "layer_idx": int(layer_idx),
                    "layer_name": str(layer_name),
                    "hidden_dim": int(tensor.shape[-1]),
                    "regularization_c": float(c),
                }
                row.update(metrics)
                rows.append(result_flags(row))
                if save_all_weights:
                    all_weights[key] = {
                        "probe_family": SENTENCE_FAMILY,
                        "variable_id": vid,
                        "variable": vname,
                        "representation": repr_name,
                        "layer_idx": int(layer_idx),
                        "layer_name": str(layer_name),
                        "state": probe_state(model),
                    }
                pbar.update(1)

                # Delta direction task: does basis -> changed form a stable held-out direction?
                key = f"{DELTA_DIRECTION_FAMILY}|var={vid}|repr={repr_name}|layer={layer_idx}"
                data = delta_direction_activation_data(pair_meta, tensor, vid, layer_idx)
                model, metrics = train_one_activation(data, c, max_iter, seed)
                row = {
                    "candidate_key": key,
                    "probe_family": DELTA_DIRECTION_FAMILY,
                    "variable_id": vid,
                    "variable": vname,
                    "representation": repr_name,
                    "layer_idx": int(layer_idx),
                    "layer_name": str(layer_name),
                    "hidden_dim": int(tensor.shape[-1]),
                    "regularization_c": float(c),
                }
                row.update(metrics)
                rows.append(result_flags(row))
                if save_all_weights:
                    all_weights[key] = {
                        "probe_family": DELTA_DIRECTION_FAMILY,
                        "variable_id": vid,
                        "variable": vname,
                        "representation": repr_name,
                        "layer_idx": int(layer_idx),
                        "layer_name": str(layer_name),
                        "state": probe_state(model),
                    }
                pbar.update(1)

    pbar.close()

    candidate = pd.DataFrame(rows)
    best = select_best(candidate)

    best_weights = {}
    if save_all_weights:
        for _, row in best.iterrows():
            final_key = f"{row['probe_family']}|var={int(row['variable_id'])}"
            best_weights[final_key] = all_weights[row["candidate_key"]]

    return candidate, best, all_weights, best_weights


def add_activation_bootstrap_cis(
    best: pd.DataFrame,
    cache: dict[str, Any],
    sentence_meta: pd.DataFrame,
    pair_meta: pd.DataFrame,
    c: float,
    max_iter: int,
    seed: int,
    n_bootstrap: int,
) -> pd.DataFrame:
    out = best.copy()
    if n_bootstrap <= 0 or out.empty:
        return out

    reprs = {
        "final_token": cache["final_token"],
        "mean_pooled": cache["mean_pooled"],
    }

    for col in [
        "val_auroc_ci_lower",
        "val_auroc_ci_upper",
        "val_auroc_bootstrap_valid_samples",
        "test_auroc_ci_lower",
        "test_auroc_ci_upper",
        "test_auroc_bootstrap_valid_samples",
    ]:
        if col not in out.columns:
            out[col] = np.nan

    for idx, row in out.iterrows():
        family = row["probe_family"]
        vid = int(row["variable_id"])
        repr_name = str(row["representation"])
        layer_idx = int(row["layer_idx"])
        tensor = reprs[repr_name]

        if family == SENTENCE_FAMILY:
            data = sentence_activation_data(sentence_meta, tensor, vid, layer_idx)
        elif family == DELTA_DIRECTION_FAMILY:
            data = delta_direction_activation_data(pair_meta, tensor, vid, layer_idx)
        else:
            continue

        model, _ = train_one_activation(data, c=c, max_iter=max_iter, seed=seed)
        ci_row = add_bootstrap_columns({}, model, data, n_bootstrap=n_bootstrap, seed=seed + vid * 100_000 + layer_idx * 1_000)
        for k, v in ci_row.items():
            out.at[idx, k] = v

    return out


def longest_adjacent_run(layers: list[int]) -> int:
    if not layers:
        return 0
    layers = sorted(set(int(x) for x in layers))
    best = 1
    current = 1
    for prev, cur in zip(layers, layers[1:]):
        if cur == prev + 1:
            current += 1
        else:
            best = max(best, current)
            current = 1
    return max(best, current)


def layer_stability_profile(candidate: pd.DataFrame, threshold: float) -> pd.DataFrame:
    rows = []
    if candidate.empty:
        return pd.DataFrame()

    for (family, vid, variable), group in candidate.groupby(["probe_family", "variable_id", "variable"], sort=True):
        ranked = group.copy()
        ranked["_val_auroc"] = ranked["val_auroc"].fillna(-1.0)
        ranked["_test_auroc"] = ranked["test_auroc"].fillna(-1.0)
        best = ranked.sort_values(["_val_auroc", "_test_auroc"], ascending=[False, False]).iloc[0]

        layer_best = (
            group.sort_values(["layer_idx", "test_auroc"], ascending=[True, False])
            .groupby("layer_idx", as_index=False)
            .head(1)
            .sort_values("layer_idx")
        )
        above = layer_best[layer_best["test_auroc"] > threshold]["layer_idx"].astype(int).tolist()

        rows.append({
            "probe_family": family,
            "variable_id": int(vid),
            "variable": variable,
            "layer_stability_threshold": float(threshold),
            "best_layer_idx": int(best["layer_idx"]),
            "best_layer_name": str(best["layer_name"]),
            "best_representation": str(best["representation"]),
            "best_val_auroc": float(best["val_auroc"]),
            "best_test_auroc": float(best["test_auroc"]),
            "layers_above_threshold_count": int(len(above)),
            "max_adjacent_layers_above_threshold": int(longest_adjacent_run(above)),
            "signal_beyond_layer_2": bool(any(layer > 2 for layer in above)),
            "layers_above_threshold": json.dumps(above),
        })

    return pd.DataFrame(rows).sort_values(["probe_family", "variable_id"]).reset_index(drop=True)


def sentence_text_data(sentence_meta: pd.DataFrame, variable_id: int) -> dict[str, tuple[list[str], np.ndarray]]:
    var = sentence_meta[sentence_meta["variable_id"] == variable_id]
    out = {}
    for split in SPLITS:
        d = var[var["split"] == split]
        out[split] = (
            d["sentence"].astype(str).tolist(),
            (d["type"].to_numpy() == "changed").astype(np.int64),
        )
    return out


def delta_direction_text_data(
    sentence_meta: pd.DataFrame,
    pair_meta: pd.DataFrame,
    variable_id: int,
) -> dict[str, tuple[list[str], np.ndarray]]:
    """Text baseline analogue of the activation delta-direction task.

    Positive examples are BASIS -> CHANGED. Negative examples reverse the same
    pair as CHANGED -> BASIS. This asks whether surface text alone makes the
    direction recoverable under the same train/val/test split.
    """
    var = pair_meta[pair_meta["variable_id"] == variable_id]
    sentence_lookup = sentence_meta.set_index("sentence_row_idx")["sentence"].to_dict()
    out = {}

    for split in SPLITS:
        d = var[var["split"] == split].reset_index(drop=True)
        basis_idx = d["basis_sentence_row_idx"].to_numpy(dtype=np.int64)
        changed_idx = d["changed_sentence_row_idx"].to_numpy(dtype=np.int64)

        pos = []
        neg = []
        for b, c in zip(basis_idx, changed_idx):
            basis = str(sentence_lookup[int(b)])
            changed = str(sentence_lookup[int(c)])
            pos.append(f"FROM: {basis} [DIRECTION_SEP] TO: {changed}")
            neg.append(f"FROM: {changed} [DIRECTION_SEP] TO: {basis}")

        texts = pos + neg
        y = np.concatenate([np.ones(len(pos), dtype=np.int64), np.zeros(len(neg), dtype=np.int64)])
        out[split] = (texts, y)

    return out


def fit_text_baseline(
    data: dict[str, tuple[list[str], np.ndarray]],
    kind: str,
    max_features: int,
    c: float,
    max_iter: int,
    seed: int,
) -> dict[str, float | int]:
    model = text_model(kind, max_features, c, max_iter, seed)

    train_texts, y_train = data["train"]
    if kind == "length_punct":
        x_train = text_length_features(train_texts)
    else:
        x_train = train_texts

    model.fit(x_train, y_train)

    metrics = {}
    for split in SPLITS:
        texts, y = data[split]
        if kind == "length_punct":
            x = text_length_features(texts)
        else:
            x = texts
        metrics.update(evaluate(model, x, y, split))
    return metrics


def train_text_baselines(
    sentence_meta: pd.DataFrame,
    pair_meta: pd.DataFrame,
    c: float,
    max_iter: int,
    seed: int,
    max_features: int,
) -> pd.DataFrame:
    rows = []
    kinds = ["word_tfidf", "char_tfidf", "length_punct"]
    var_table = variables(sentence_meta)

    pbar = tqdm(total=len(var_table) * len(kinds) * 2, desc="Text baselines")
    for _, vr in var_table.iterrows():
        vid = int(vr["variable_id"])
        vname = str(vr["variable"])

        data_sentence = sentence_text_data(sentence_meta, vid)
        data_direction = delta_direction_text_data(sentence_meta, pair_meta, vid)

        for kind in kinds:
            metrics = fit_text_baseline(data_sentence, kind, max_features, c, max_iter, seed)
            row = {
                "text_probe_family": TEXT_SENTENCE_FAMILY,
                "variable_id": vid,
                "variable": vname,
                "model_kind": kind,
            }
            row.update(metrics)
            rows.append(row)
            pbar.update(1)

            metrics = fit_text_baseline(data_direction, kind, max_features, c, max_iter, seed)
            row = {
                "text_probe_family": TEXT_DELTA_DIRECTION_FAMILY,
                "variable_id": vid,
                "variable": vname,
                "model_kind": kind,
            }
            row.update(metrics)
            rows.append(row)
            pbar.update(1)

    pbar.close()
    return pd.DataFrame(rows)


def add_best_text_bootstrap_cis(
    text_results: pd.DataFrame,
    sentence_meta: pd.DataFrame,
    pair_meta: pd.DataFrame,
    c: float,
    max_iter: int,
    seed: int,
    max_features: int,
    n_bootstrap: int,
) -> pd.DataFrame:
    out = text_results.copy()
    if n_bootstrap <= 0 or out.empty:
        return out

    for col in [
        "val_auroc_ci_lower",
        "val_auroc_ci_upper",
        "val_auroc_bootstrap_valid_samples",
        "test_auroc_ci_lower",
        "test_auroc_ci_upper",
        "test_auroc_bootstrap_valid_samples",
    ]:
        if col not in out.columns:
            out[col] = np.nan

    best_text = best_text_by_task(out)
    for _, row in best_text.iterrows():
        family = row["text_probe_family"]
        vid = int(row["variable_id"])
        kind = str(row["model_kind"])

        if family == TEXT_SENTENCE_FAMILY:
            data = sentence_text_data(sentence_meta, vid)
        elif family == TEXT_DELTA_DIRECTION_FAMILY:
            data = delta_direction_text_data(sentence_meta, pair_meta, vid)
        else:
            continue

        model = text_model(kind, max_features=max_features, c=c, max_iter=max_iter, seed=seed)
        train_texts, y_train = data["train"]
        x_train = text_length_features(train_texts) if kind == "length_punct" else train_texts
        model.fit(x_train, y_train)

        prepared = {}
        for split, (texts, y) in data.items():
            x = text_length_features(texts) if kind == "length_punct" else texts
            prepared[split] = (x, y)

        ci_row = add_bootstrap_columns({}, model, prepared, n_bootstrap=n_bootstrap, seed=seed + vid * 100_000)
        mask = (
            (out["variable_id"] == vid)
            & (out["text_probe_family"] == family)
            & (out["model_kind"] == kind)
        )
        for k, v in ci_row.items():
            out.loc[mask, k] = v

    return out


def _threadpool_context(limits: int):
    if threadpool_limits is None:
        class _NoopContext:
            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc_value, traceback):
                return False

        return _NoopContext()
    return threadpool_limits(limits=limits)


def _fit_null_config(
    cfg_idx: int,
    cfg: dict[str, Any],
    sentence_meta: pd.DataFrame,
    tensor: torch.Tensor,
    c: float,
    max_iter: int,
    seed: int,
    num_permutations: int,
    threadpool_limit: int,
    null_control_scope: str,
) -> list[dict[str, Any]]:
    vid = int(cfg["variable_id"])
    vname = str(cfg["variable"])
    repr_name = str(cfg["representation"])
    layer_idx = int(cfg["layer_idx"])
    layer_name = str(cfg["layer_name"])

    true_data = sentence_activation_data(sentence_meta, tensor, vid, layer_idx)
    x_train, y_train_true = true_data["train"]
    rows: list[dict[str, Any]] = []

    with _threadpool_context(threadpool_limit):
        for perm_id in range(num_permutations):
            rng = np.random.default_rng(seed + vid * 100_000 + cfg_idx * 1_000 + perm_id)
            y_train = y_train_true.copy()
            rng.shuffle(y_train)

            model = activation_model(c, max_iter, seed + perm_id)
            model.fit(x_train, y_train)

            metrics = {}
            for split in SPLITS:
                x, y_true = true_data[split]
                metrics.update(evaluate(model, x, y_true, split))

            row = {
                "null_family": NULL_SENTENCE_FAMILY,
                "null_control_scope": null_control_scope,
                "variable_id": vid,
                "variable": vname,
                "representation": repr_name,
                "layer_idx": int(layer_idx),
                "layer_name": layer_name,
                "permutation_id": int(perm_id),
            }
            row.update(metrics)
            rows.append(row)

    return rows


def train_null_label_controls(
    sentence_meta: pd.DataFrame,
    cache: dict[str, Any],
    c: float,
    max_iter: int,
    seed: int,
    num_permutations: int,
    best_activation: pd.DataFrame | None = None,
    null_control_scope: str = "all_candidates",
    n_jobs: int = 8,
    threadpool_limit: int = 1,
) -> pd.DataFrame:
    if num_permutations <= 0:
        return pd.DataFrame()

    var_table = variables(sentence_meta)
    layer_names = get_layer_names(cache)
    reprs = {"final_token": cache["final_token"], "mean_pooled": cache["mean_pooled"]}

    configs: list[dict[str, Any]] = []
    if null_control_scope == "best_sentence" and best_activation is not None and not best_activation.empty:
        best_sentence = best_activation[best_activation["probe_family"] == SENTENCE_FAMILY].copy()
        for _, row in best_sentence.iterrows():
            configs.append({
                "variable_id": int(row["variable_id"]),
                "variable": str(row["variable"]),
                "representation": str(row["representation"]),
                "layer_idx": int(row["layer_idx"]),
                "layer_name": str(row["layer_name"]),
            })
    elif null_control_scope == "all_candidates":
        for _, vr in var_table.iterrows():
            for repr_name in reprs:
                for layer_idx, layer_name in enumerate(layer_names):
                    configs.append({
                        "variable_id": int(vr["variable_id"]),
                        "variable": str(vr["variable"]),
                        "representation": repr_name,
                        "layer_idx": int(layer_idx),
                        "layer_name": str(layer_name),
                    })
    else:
        raise ValueError("null_control_scope must be 'best_sentence' or 'all_candidates'")

    if not configs:
        return pd.DataFrame()

    n_jobs = int(n_jobs)
    if n_jobs < 0:
        n_jobs = max(1, (os.cpu_count() or 1) + 1 + n_jobs)
    if n_jobs == 0:
        n_jobs = 1
    threadpool_limit = max(1, int(threadpool_limit))

    print(
        f"Null label-shuffle controls: {len(configs):,} configs × {num_permutations:,} permutations "
        f"using {n_jobs:,} worker(s)."
    )

    def run_one(item: tuple[int, dict[str, Any]]) -> list[dict[str, Any]]:
        cfg_idx, cfg = item
        tensor = reprs[str(cfg["representation"])]
        return _fit_null_config(
            cfg_idx=cfg_idx,
            cfg=cfg,
            sentence_meta=sentence_meta,
            tensor=tensor,
            c=c,
            max_iter=max_iter,
            seed=seed,
            num_permutations=num_permutations,
            threadpool_limit=threadpool_limit,
            null_control_scope=null_control_scope,
        )

    items = list(enumerate(configs))
    if n_jobs == 1:
        chunks = [run_one(item) for item in tqdm(items, desc="Null label-shuffle controls")]
    else:
        chunks = Parallel(n_jobs=n_jobs, prefer="threads")(
            delayed(run_one)(item) for item in tqdm(items, desc="Null label-shuffle controls")
        )

    rows = [row for chunk in chunks for row in chunk]
    return pd.DataFrame(rows)

def best_text_by_task(text_results: pd.DataFrame) -> pd.DataFrame:
    d = text_results.copy()
    d["_val_auroc"] = d["val_auroc"].fillna(-1)
    d = d.sort_values(["text_probe_family", "variable_id", "_val_auroc"], ascending=[True, True, False])
    return d.groupby(["text_probe_family", "variable_id"], as_index=False).head(1).drop(columns=["_val_auroc"])


def best_null_by_variable(null_results: pd.DataFrame) -> pd.DataFrame:
    if null_results.empty:
        return pd.DataFrame()
    d = null_results.copy()
    d["_val_auroc"] = d["val_auroc"].fillna(-1)
    d = d.sort_values(["variable_id", "_val_auroc"], ascending=[True, False])
    return d.groupby(["variable_id"], as_index=False).head(1).drop(columns=["_val_auroc"])


def split_control_profile(pair_meta: pd.DataFrame) -> pd.DataFrame:
    """Summarize whether validation/test splits hold out marker families/domains.

    This does not decide scientific success by itself. It records whether a high
    score is actually cross-marker/cross-domain evidence or merely same-family
    interpolation.
    """
    rows = []
    for (vid, variable), g in pair_meta.groupby(["variable_id", "variable"], sort=True):
        split_sets: dict[str, dict[str, set[str]]] = {}
        for split in SPLITS:
            d = g[g["split"] == split]
            split_sets[split] = {
                "marker_family": set(d["marker_family"].dropna().astype(str)),
                "lexical_domain": set(d["lexical_domain"].dropna().astype(str)),
            }

        train_markers = split_sets["train"]["marker_family"]
        train_domains = split_sets["train"]["lexical_domain"]
        test_markers = split_sets["test"]["marker_family"]
        test_domains = split_sets["test"]["lexical_domain"]
        val_markers = split_sets["val"]["marker_family"]
        val_domains = split_sets["val"]["lexical_domain"]

        test_marker_overlap = test_markers & train_markers
        test_domain_overlap = test_domains & train_domains
        val_marker_overlap = val_markers & train_markers
        val_domain_overlap = val_domains & train_domains

        test_has_heldout_marker = len(test_markers - train_markers) > 0
        test_has_heldout_domain = len(test_domains - train_domains) > 0
        test_markers_all_heldout = len(test_markers) > 0 and len(test_marker_overlap) == 0
        test_domains_all_heldout = len(test_domains) > 0 and len(test_domain_overlap) == 0

        if test_markers_all_heldout and test_domains_all_heldout:
            split_strength = "strong_test_marker_and_domain_holdout"
        elif test_has_heldout_marker and test_has_heldout_domain:
            split_strength = "partial_test_marker_and_domain_holdout"
        elif test_has_heldout_marker or test_has_heldout_domain:
            split_strength = "weak_partial_test_holdout"
        else:
            split_strength = "no_test_marker_or_domain_holdout_detected"

        rows.append({
            "variable_id": int(vid),
            "variable": variable,
            "train_marker_family_count": int(len(train_markers)),
            "val_marker_family_count": int(len(val_markers)),
            "test_marker_family_count": int(len(test_markers)),
            "train_lexical_domain_count": int(len(train_domains)),
            "val_lexical_domain_count": int(len(val_domains)),
            "test_lexical_domain_count": int(len(test_domains)),
            "test_has_heldout_marker_family": bool(test_has_heldout_marker),
            "test_has_heldout_lexical_domain": bool(test_has_heldout_domain),
            "test_marker_families_all_heldout_from_train": bool(test_markers_all_heldout),
            "test_lexical_domains_all_heldout_from_train": bool(test_domains_all_heldout),
            "test_marker_train_overlap_count": int(len(test_marker_overlap)),
            "test_lexical_train_overlap_count": int(len(test_domain_overlap)),
            "val_marker_train_overlap_count": int(len(val_marker_overlap)),
            "val_lexical_train_overlap_count": int(len(val_domain_overlap)),
            "split_control_strength": split_strength,
            "train_marker_families": json.dumps(sorted(train_markers), ensure_ascii=False),
            "test_marker_families": json.dumps(sorted(test_markers), ensure_ascii=False),
            "train_lexical_domains": json.dumps(sorted(train_domains), ensure_ascii=False),
            "test_lexical_domains": json.dumps(sorted(test_domains), ensure_ascii=False),
        })

    return pd.DataFrame(rows).sort_values("variable_id").reset_index(drop=True)


def text_evidence_category(activation_auc: float, text_auc: float, margin: float = 0.05) -> str:
    if np.isnan(text_auc):
        return "text_baseline_missing"
    if activation_auc >= text_auc + margin:
        return "A_activation_stronger_than_text"
    if abs(activation_auc - text_auc) <= margin:
        return "B_activation_comparable_to_text"
    return "C_text_stronger_than_activation"


def compare_results(
    best_activation: pd.DataFrame,
    text_results: pd.DataFrame,
    null_results: pd.DataFrame,
    pair_meta: pd.DataFrame,
    layer_stability: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    best_text = best_text_by_task(text_results)
    best_null = best_null_by_variable(null_results)
    split_profile = split_control_profile(pair_meta)

    rows = []

    for _, a in best_activation.iterrows():
        vid = int(a["variable_id"])
        family = a["probe_family"]

        if family == SENTENCE_FAMILY:
            text_family = TEXT_SENTENCE_FAMILY
        elif family == DELTA_DIRECTION_FAMILY:
            text_family = TEXT_DELTA_DIRECTION_FAMILY
        else:
            continue

        t_match = best_text[(best_text["variable_id"] == vid) & (best_text["text_probe_family"] == text_family)]
        if len(t_match) == 1:
            t_row = t_match.iloc[0]
            text_kind = t_row["model_kind"]
            text_val = float(t_row["val_auroc"])
            text_val_ci_lower = float(t_row.get("val_auroc_ci_lower", np.nan))
            text_val_ci_upper = float(t_row.get("val_auroc_ci_upper", np.nan))
            text_test = float(t_row["test_auroc"])
            text_test_ci_lower = float(t_row.get("test_auroc_ci_lower", np.nan))
            text_test_ci_upper = float(t_row.get("test_auroc_ci_upper", np.nan))
        else:
            text_kind = None
            text_val = np.nan
            text_val_ci_lower = np.nan
            text_val_ci_upper = np.nan
            text_test = np.nan
            text_test_ci_lower = np.nan
            text_test_ci_upper = np.nan

        n_val = np.nan
        n_test = np.nan
        if family == SENTENCE_FAMILY and not best_null.empty:
            n = best_null[best_null["variable_id"] == vid]
            if len(n) == 1:
                n_val = float(n.iloc[0]["val_auroc"])
                n_test = float(n.iloc[0]["test_auroc"])

        rows.append({
            "probe_family": family,
            "variable_id": vid,
            "variable": a["variable"],
            "activation_representation": a["representation"],
            "activation_layer_idx": int(a["layer_idx"]),
            "activation_layer_name": a["layer_name"],
            "activation_val_auroc": float(a["val_auroc"]),
            "activation_val_auroc_ci_lower": float(a.get("val_auroc_ci_lower", np.nan)),
            "activation_val_auroc_ci_upper": float(a.get("val_auroc_ci_upper", np.nan)),
            "activation_test_auroc": float(a["test_auroc"]),
            "activation_test_auroc_ci_lower": float(a.get("test_auroc_ci_lower", np.nan)),
            "activation_test_auroc_ci_upper": float(a.get("test_auroc_ci_upper", np.nan)),
            "activation_test_accuracy": float(a["test_accuracy"]),
            "best_text_model_kind": text_kind,
            "best_text_val_auroc": text_val,
            "best_text_val_auroc_ci_lower": text_val_ci_lower,
            "best_text_val_auroc_ci_upper": text_val_ci_upper,
            "best_text_test_auroc": text_test,
            "best_text_test_auroc_ci_lower": text_test_ci_lower,
            "best_text_test_auroc_ci_upper": text_test_ci_upper,
            "activation_minus_text_test_auroc": float(a["test_auroc"] - text_test) if not np.isnan(text_test) else np.nan,
            "best_null_val_auroc": n_val,
            "best_null_test_auroc": n_test,
            "activation_minus_null_test_auroc": float(a["test_auroc"] - n_test) if not np.isnan(n_test) else np.nan,
            "suspiciously_high_test_auroc": bool(a.get("suspiciously_high_test_auroc", False)),
            "possible_overfit": bool(a.get("possible_overfit", False)),
            "weak_signal": bool(a.get("weak_signal", False)),
        })

    comparison = pd.DataFrame(rows).sort_values(["probe_family", "variable_id"]).reset_index(drop=True)

    status_rows = []
    for vid, group in comparison.groupby("variable_id", sort=True):
        variable = group["variable"].iloc[0]
        sent = group[group["probe_family"] == SENTENCE_FAMILY]
        direction = group[group["probe_family"] == DELTA_DIRECTION_FAMILY]
        row = {"variable_id": int(vid), "variable": variable}

        if len(sent) == 1:
            s = sent.iloc[0]
            row.update({
                "sentence_activation_test_auroc": float(s["activation_test_auroc"]),
                "sentence_activation_test_auroc_ci_lower": float(s.get("activation_test_auroc_ci_lower", np.nan)),
                "sentence_activation_test_auroc_ci_upper": float(s.get("activation_test_auroc_ci_upper", np.nan)),
                "sentence_activation_val_auroc": float(s["activation_val_auroc"]),
                "sentence_activation_val_auroc_ci_lower": float(s.get("activation_val_auroc_ci_lower", np.nan)),
                "sentence_activation_val_auroc_ci_upper": float(s.get("activation_val_auroc_ci_upper", np.nan)),
                "sentence_best_text_test_auroc": float(s["best_text_test_auroc"]),
                "sentence_best_text_test_auroc_ci_lower": float(s.get("best_text_test_auroc_ci_lower", np.nan)),
                "sentence_best_text_test_auroc_ci_upper": float(s.get("best_text_test_auroc_ci_upper", np.nan)),
                "sentence_best_text_model_kind": s["best_text_model_kind"],
                "sentence_activation_minus_text": float(s["activation_minus_text_test_auroc"]),
                "sentence_activation_minus_null": float(s["activation_minus_null_test_auroc"]),
                "sentence_best_layer_idx": int(s["activation_layer_idx"]),
                "sentence_best_representation": s["activation_representation"],
                "sentence_possible_overfit": bool(s["possible_overfit"]),
            })

        if len(direction) == 1:
            d = direction.iloc[0]
            row.update({
                "delta_direction_activation_test_auroc": float(d["activation_test_auroc"]),
                "delta_direction_activation_test_auroc_ci_lower": float(d.get("activation_test_auroc_ci_lower", np.nan)),
                "delta_direction_activation_test_auroc_ci_upper": float(d.get("activation_test_auroc_ci_upper", np.nan)),
                "delta_direction_activation_val_auroc": float(d["activation_val_auroc"]),
                "delta_direction_activation_val_auroc_ci_lower": float(d.get("activation_val_auroc_ci_lower", np.nan)),
                "delta_direction_activation_val_auroc_ci_upper": float(d.get("activation_val_auroc_ci_upper", np.nan)),
                "delta_direction_best_text_test_auroc": float(d["best_text_test_auroc"]),
                "delta_direction_best_text_test_auroc_ci_lower": float(d.get("best_text_test_auroc_ci_lower", np.nan)),
                "delta_direction_best_text_test_auroc_ci_upper": float(d.get("best_text_test_auroc_ci_upper", np.nan)),
                "delta_direction_best_text_model_kind": d["best_text_model_kind"],
                "delta_direction_activation_minus_text": float(d["activation_minus_text_test_auroc"]),
                "delta_direction_best_layer_idx": int(d["activation_layer_idx"]),
                "delta_direction_best_representation": d["activation_representation"],
                "delta_direction_possible_overfit": bool(d["possible_overfit"]),
            })

        sp = split_profile[split_profile["variable_id"] == int(vid)]
        if len(sp) == 1:
            for k, v in sp.iloc[0].to_dict().items():
                if k not in {"variable_id", "variable"}:
                    row[k] = v

        for family, prefix in [(SENTENCE_FAMILY, "sentence"), (DELTA_DIRECTION_FAMILY, "delta_direction")]:
            ls = layer_stability[(layer_stability["variable_id"] == int(vid)) & (layer_stability["probe_family"] == family)]
            if len(ls) == 1:
                for k, v in ls.iloc[0].to_dict().items():
                    if k not in {"probe_family", "variable_id", "variable"}:
                        row[f"{prefix}_layer_stability_{k}"] = v

        s_auc = row.get("sentence_activation_test_auroc", np.nan)
        s_val = row.get("sentence_activation_val_auroc", np.nan)
        s_text = row.get("sentence_best_text_test_auroc", np.nan)
        s_layer = row.get("sentence_best_layer_idx", -1)
        s_null_margin = row.get("sentence_activation_minus_null", np.nan)
        dir_auc = row.get("delta_direction_activation_test_auroc", np.nan)
        dir_val = row.get("delta_direction_activation_val_auroc", np.nan)

        # Level 1: recoverability from activations.
        level_1_pass = bool(not np.isnan(s_auc) and s_auc >= 0.65)

        # Level 2: text/artifact control. Non-blocking by design, because many
        # structural linguistic cues are intentionally surface-visible. This field
        # narrows the claim instead of rejecting the variable.
        l2_status = text_evidence_category(s_auc, s_text) if not np.isnan(s_auc) else "missing_sentence_result"
        level_2_activation_beats_text = bool(l2_status == "A_activation_stronger_than_text")
        level_2_surface_visible = bool(l2_status in {
            "B_activation_comparable_to_text",
            "C_text_stronger_than_activation",
        })

        # Level 3: stable basis -> changed direction.
        level_3_pass = bool(not np.isnan(dir_auc) and dir_auc >= 0.65)

        # Level 4: performance survives the dataset's held-out split design.
        has_split_holdout = bool(
            row.get("test_has_heldout_marker_family", False)
            or row.get("test_has_heldout_lexical_domain", False)
        )
        strong_split_holdout = bool(
            row.get("test_marker_families_all_heldout_from_train", False)
            and row.get("test_lexical_domains_all_heldout_from_train", False)
        )
        level_4_pass = bool(level_1_pass and level_3_pass and has_split_holdout)

        # Level 5 is supplied by the learned activation direction viability check.
        level_5_pass = False
        level_5_status = "not_run"

        sentence_has_later_signal = bool(row.get("sentence_layer_stability_signal_beyond_layer_2", False))
        early_layer_risk = bool(s_layer <= 1 and not np.isnan(s_auc) and s_auc >= 0.80 and not sentence_has_later_signal)
        null_control_pass = bool(np.isnan(s_null_margin) or s_null_margin >= 0.10)
        overfit_flag = bool(row.get("sentence_possible_overfit", False) or row.get("delta_direction_possible_overfit", False))

        row.update({
            "level_1_activation_recoverability_pass": level_1_pass,
            "level_1_threshold": 0.65,
            "level_2_text_evidence_category": l2_status,
            "level_2_text_artifact_status": l2_status,
            "level_2_activation_beats_text_pass": level_2_activation_beats_text,
            "level_2_text_control_nonblocking": True,
            "level_2_surface_visible_nonblocking": level_2_surface_visible,
            "level_3_directional_consistency_pass": level_3_pass,
            "level_3_threshold": 0.65,
            "level_4_split_generalization_pass": level_4_pass,
            "level_4_has_test_marker_or_domain_holdout": has_split_holdout,
            "level_4_strong_marker_and_domain_holdout": strong_split_holdout,
            "learned_activation_direction_viability_pass": level_5_pass,
            "learned_activation_direction_viability_status": level_5_status,
            "early_layer_artifact_risk": early_layer_risk,
            "null_label_control_pass": null_control_pass,
            "possible_overfit_flag": overfit_flag,
        })

        if not level_1_pass:
            status = "level1_failed_low_activation_recoverability"
            next_action = "Do not pursue this variable under the current model/dataset until activation recoverability improves."
        elif not null_control_pass:
            status = "failed_null_label_control"
            next_action = "Inspect for leakage or train/eval bugs; activation result is too close to the best shuffled-label control."
        elif overfit_flag:
            status = "overfit_risk_needs_rerun_or_more_data"
            next_action = "Rerun with stronger regularization or more examples; do not interpret before overfit risk is resolved."
        elif not level_3_pass:
            status = "level3_failed_unstable_delta_direction"
            next_action = "Keep as recoverable but not directionally stable; do not move to SAE-style interpretation yet."
        elif not level_4_pass:
            status = "level4_split_generalization_not_established"
            next_action = "The activation/direction signal exists, but the split design does not yet establish held-out marker/domain generalization."
        elif early_layer_risk:
            status = "levels1_3_4_passed_but_early_layer_artifact_risk"
            next_action = "Manual inspection required; prefer later-layer corroboration before any strong claim."
        else:
            status = "levels1_3_4_passed_ready_for_learned_activation_direction_viability"
            next_action = "Run the learned activation direction viability check before treating the direction as stable enough for deeper interpretation."

        row["evidence_status"] = status
        row["ready_for_learned_activation_direction_viability"] = bool(status in {
            "levels1_3_4_passed_ready_for_learned_activation_direction_viability",
            "levels1_3_4_passed_but_early_layer_artifact_risk",
        })
        row["mechanistic_claim_allowed"] = bool(level_1_pass and level_3_pass and level_4_pass and level_5_pass)
        row["claim_scope"] = (
            "activation-recoverable structural cue; surface-visible text cue also present"
            if level_2_surface_visible
            else "activation-recoverable structural cue with activation stronger than text baseline"
        )
        row["recommended_next_action"] = next_action

        status_rows.append(row)

    status = pd.DataFrame(status_rows).sort_values("variable_id").reset_index(drop=True)
    return comparison, status, split_profile

def save_all(
    output_dir: Path,
    github_export_dir: Path | None,
    candidate: pd.DataFrame,
    best: pd.DataFrame,
    all_weights: dict[str, Any],
    best_weights: dict[str, Any],
    text_results: pd.DataFrame,
    null_results: pd.DataFrame,
    comparison: pd.DataFrame,
    evidence_status: pd.DataFrame,
    split_profile: pd.DataFrame,
    layer_stability: pd.DataFrame,
    args: argparse.Namespace,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    files = {}

    def save_df(df: pd.DataFrame, name: str) -> None:
        pq = output_dir / f"{name}.parquet"
        csv = output_dir / f"{name}.csv"
        df.to_parquet(pq, index=False)
        df.to_csv(csv, index=False)
        files[name] = {"parquet": pq.name, "csv": csv.name}

    save_df(candidate, "candidate_activation_probe_results")
    save_df(best, "best_activation_probe_results")
    save_df(text_results, "text_baseline_results")
    save_df(null_results, "null_label_shuffle_results")
    save_df(comparison, "activation_vs_text_and_null_comparison")
    save_df(evidence_status, "evidence_status_by_variable")
    save_df(split_profile, "split_control_profile_by_variable")
    save_df(layer_stability, "layer_stability_by_variable")

    candidate_weights_path = output_dir / "candidate_activation_probe_weights.pt"
    best_weights_path = output_dir / "best_activation_probe_weights.pt"

    torch.save(
        {
            "candidate_probe_states": all_weights,
            "note": "All candidate probe weights. Keep local/Lambda; usually do not commit.",
        },
        candidate_weights_path,
    )
    torch.save(
        {
            "best_probe_states": best_weights,
            "note": "Best selected probe weights per activation family and variable.",
        },
        best_weights_path,
    )

    manifest = {
        "script": "train_raw_activation_probes.py",
        "activation_families": [SENTENCE_FAMILY, DELTA_DIRECTION_FAMILY],
        "text_baseline_families": [TEXT_SENTENCE_FAMILY, TEXT_DELTA_DIRECTION_FAMILY],
        "null_family": NULL_SENTENCE_FAMILY,
        "num_candidate_activation_probes": int(len(candidate)),
        "num_best_activation_probes": int(len(best)),
        "num_text_baselines": int(len(text_results)),
        "num_null_controls": int(len(null_results)),
        "files": files,
        "weights": {
            "candidate_activation_probe_weights": candidate_weights_path.name,
            "best_activation_probe_weights": best_weights_path.name,
        },
        "args": vars(args),
    }

    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False, default=str)

    if github_export_dir is not None:
        github_export_dir.mkdir(parents=True, exist_ok=True)
        # Export compact evidence/results only, plus best weights.
        export_names = [
            "best_activation_probe_results",
            "text_baseline_results",
            "null_label_shuffle_results",
            "activation_vs_text_and_null_comparison",
            "evidence_status_by_variable",
            "split_control_profile_by_variable",
            "layer_stability_by_variable",
        ]
        for name in export_names:
            for suffix in [".parquet", ".csv"]:
                src = output_dir / f"{name}{suffix}"
                if src.exists():
                    shutil.copy2(src, github_export_dir / src.name)
        shutil.copy2(best_weights_path, github_export_dir / best_weights_path.name)
        shutil.copy2(manifest_path, github_export_dir / manifest_path.name)

    print()
    print("Strict probe run complete.")
    print(f"Full output: {output_dir}")
    if github_export_dir:
        print(f"GitHub export: {github_export_dir}")
    print()
    print("Evidence status counts:")
    print(evidence_status["evidence_status"].value_counts().to_string())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Raw activation probe run with text baselines, null controls, bootstrap CIs, and layer-stability reporting."
    )
    parser.add_argument(
        "--activation-cache",
        type=Path,
        default=Path("artifacts/activation_cache/feature_dataset/xglm564m/xglm564m_feature_activations.pt"),
    )
    parser.add_argument(
        "--sentence-metadata",
        type=Path,
        default=Path("artifacts/activation_cache/feature_dataset/xglm564m/sentence_metadata.parquet"),
    )
    parser.add_argument(
        "--pair-metadata",
        type=Path,
        default=Path("artifacts/activation_cache/feature_dataset/xglm564m/pair_metadata.parquet"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/probe_data/raw_activation_probes_strict/xglm564m"),
    )
    parser.add_argument(
        "--github-export-dir",
        type=Path,
        default=Path("artifacts/probe_data/raw_activation_probes_strict/xglm564m_github_export"),
    )
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--max-iter", type=int, default=2000)
    parser.add_argument("--text-max-features", type=int, default=5000)
    parser.add_argument("--num-null-permutations", type=int, default=50)
    parser.add_argument("--null-control-scope", choices=["best_sentence", "all_candidates"], default="all_candidates")
    parser.add_argument("--null-n-jobs", type=int, default=8)
    parser.add_argument("--null-threadpool-limit", type=int, default=1)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--layer-stability-threshold", type=float, default=0.70)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-save-all-weights", action="store_true")
    args = parser.parse_args()
    set_seed(args.seed)

    for p in [args.activation_cache, args.sentence_metadata, args.pair_metadata]:
        if not p.exists():
            raise FileNotFoundError(f"Missing required input: {p}")

    print("Loading cache and metadata...")
    cache = safe_torch_load(args.activation_cache)
    sentence_meta = pd.read_parquet(args.sentence_metadata)
    pair_meta = pd.read_parquet(args.pair_metadata)
    validate_inputs(cache, sentence_meta, pair_meta)

    print(f"Model:     {cache.get('model_name', 'unknown')}")
    print(f"Sentences: {len(sentence_meta):,}")
    print(f"Pairs:     {len(pair_meta):,}")
    print(f"Variables: {sentence_meta['variable_id'].nunique():,}")
    print(f"Layers:    {cache['final_token'].shape[1]}")
    print(f"Hidden dim:{cache['final_token'].shape[2]}")
    print()

    candidate, best, all_weights, best_weights = train_activation_probes(
        cache=cache,
        sentence_meta=sentence_meta,
        pair_meta=pair_meta,
        c=args.c,
        max_iter=args.max_iter,
        seed=args.seed,
        save_all_weights=not args.no_save_all_weights,
    )
    best = add_activation_bootstrap_cis(
        best=best,
        cache=cache,
        sentence_meta=sentence_meta,
        pair_meta=pair_meta,
        c=args.c,
        max_iter=args.max_iter,
        seed=args.seed,
        n_bootstrap=args.bootstrap_samples,
    )
    layer_stability = layer_stability_profile(candidate, threshold=args.layer_stability_threshold)

    text_results = train_text_baselines(
        sentence_meta=sentence_meta,
        pair_meta=pair_meta,
        c=args.c,
        max_iter=args.max_iter,
        seed=args.seed,
        max_features=args.text_max_features,
    )
    text_results = add_best_text_bootstrap_cis(
        text_results=text_results,
        sentence_meta=sentence_meta,
        pair_meta=pair_meta,
        c=args.c,
        max_iter=args.max_iter,
        seed=args.seed,
        max_features=args.text_max_features,
        n_bootstrap=args.bootstrap_samples,
    )

    null_results = train_null_label_controls(
        sentence_meta=sentence_meta,
        cache=cache,
        c=args.c,
        max_iter=args.max_iter,
        seed=args.seed,
        num_permutations=args.num_null_permutations,
        best_activation=best,
        null_control_scope=args.null_control_scope,
        n_jobs=args.null_n_jobs,
        threadpool_limit=args.null_threadpool_limit,
    )

    comparison, evidence_status, split_profile = compare_results(best, text_results, null_results, pair_meta, layer_stability)

    save_all(
        output_dir=args.output_dir,
        github_export_dir=args.github_export_dir,
        candidate=candidate,
        best=best,
        all_weights=all_weights,
        best_weights=best_weights,
        text_results=text_results,
        null_results=null_results,
        comparison=comparison,
        evidence_status=evidence_status,
        split_profile=split_profile,
        layer_stability=layer_stability,
        args=args,
    )


if __name__ == "__main__":
    main()
