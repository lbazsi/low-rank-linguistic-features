from __future__ import annotations

import argparse
import json
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
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm


SPLITS = ["train", "val", "test"]

SENTENCE_FAMILY = "sentence_basis_changed"
DELTA_MISMATCH_FAMILY = "delta_true_vs_mismatched"

TEXT_SENTENCE_FAMILY = "text_sentence_basis_changed"
TEXT_DELTA_MISMATCH_FAMILY = "text_delta_true_vs_mismatched"

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


def evaluate(model: Pipeline, x: Any, y: np.ndarray, split: str) -> dict[str, float | int]:
    pred = model.predict(x)
    if hasattr(model, "predict_proba"):
        score = model.predict_proba(x)[:, 1]
    else:
        score = model.decision_function(x)

    return {
        f"{split}_accuracy": float(accuracy_score(y, pred)),
        f"{split}_balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        f"{split}_f1": float(f1_score(y, pred)),
        f"{split}_auroc": safe_auroc(y, score),
        f"{split}_n": int(len(y)),
        f"{split}_positive_rate": float(np.mean(y)),
    }


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
    }
    required_pair = {
        "pair_row_idx",
        "pair_id",
        "variable_id",
        "variable",
        "split",
        "basis_sentence_row_idx",
        "changed_sentence_row_idx",
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


def deranged(indices: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = len(indices)
    if n < 2:
        raise ValueError("Need at least two items to construct mismatched control.")

    perm = np.arange(n)
    for _ in range(100):
        rng.shuffle(perm)
        if np.all(perm != np.arange(n)):
            return indices[perm]
    return np.roll(indices, 1)


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


def delta_mismatch_activation_data(
    pair_meta: pd.DataFrame,
    activation_tensor: torch.Tensor,
    variable_id: int,
    layer_idx: int,
    seed: int,
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    var = pair_meta[pair_meta["variable_id"] == variable_id]
    out = {}

    for split_num, split in enumerate(SPLITS):
        d = var[var["split"] == split].reset_index(drop=True)

        basis_idx = d["basis_sentence_row_idx"].to_numpy(dtype=np.int64)
        changed_idx = d["changed_sentence_row_idx"].to_numpy(dtype=np.int64)

        mismatched_basis_idx = deranged(
            basis_idx,
            seed=seed + variable_id * 100_000 + split_num * 10_000 + 11,
        )
        mismatched_changed_idx = deranged(
            changed_idx,
            seed=seed + variable_id * 100_000 + split_num * 10_000 + 29,
        )

        b = torch.tensor(basis_idx, dtype=torch.long)
        c = torch.tensor(changed_idx, dtype=torch.long)
        mb = torch.tensor(mismatched_basis_idx, dtype=torch.long)
        mc = torch.tensor(mismatched_changed_idx, dtype=torch.long)

        true_delta = activation_tensor[c, layer_idx, :].float() - activation_tensor[b, layer_idx, :].float()
        negative_a = activation_tensor[c, layer_idx, :].float() - activation_tensor[mb, layer_idx, :].float()
        negative_b = activation_tensor[mc, layer_idx, :].float() - activation_tensor[b, layer_idx, :].float()

        x = torch.cat([true_delta, negative_a, negative_b], dim=0).numpy()
        y = np.concatenate(
            [
                np.ones(len(true_delta), dtype=np.int64),
                np.zeros(len(negative_a), dtype=np.int64),
                np.zeros(len(negative_b), dtype=np.int64),
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

                # Delta mismatch task.
                key = f"{DELTA_MISMATCH_FAMILY}|var={vid}|repr={repr_name}|layer={layer_idx}"
                data = delta_mismatch_activation_data(pair_meta, tensor, vid, layer_idx, seed)
                model, metrics = train_one_activation(data, c, max_iter, seed)
                row = {
                    "candidate_key": key,
                    "probe_family": DELTA_MISMATCH_FAMILY,
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
                        "probe_family": DELTA_MISMATCH_FAMILY,
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


def delta_mismatch_text_data(
    sentence_meta: pd.DataFrame,
    pair_meta: pd.DataFrame,
    variable_id: int,
    seed: int,
) -> dict[str, tuple[list[str], np.ndarray]]:
    var = pair_meta[pair_meta["variable_id"] == variable_id]
    sentence_lookup = sentence_meta.set_index("sentence_row_idx")["sentence"].to_dict()
    out = {}

    for split_num, split in enumerate(SPLITS):
        d = var[var["split"] == split].reset_index(drop=True)
        basis_idx = d["basis_sentence_row_idx"].to_numpy(dtype=np.int64)
        changed_idx = d["changed_sentence_row_idx"].to_numpy(dtype=np.int64)
        mismatched_basis_idx = deranged(
            basis_idx,
            seed=seed + variable_id * 100_000 + split_num * 10_000 + 11,
        )
        mismatched_changed_idx = deranged(
            changed_idx,
            seed=seed + variable_id * 100_000 + split_num * 10_000 + 29,
        )

        pos = []
        neg = []

        for b, c, mb, mc in zip(basis_idx, changed_idx, mismatched_basis_idx, mismatched_changed_idx):
            basis = str(sentence_lookup[int(b)])
            changed = str(sentence_lookup[int(c)])
            mismatch_basis = str(sentence_lookup[int(mb)])
            mismatch_changed = str(sentence_lookup[int(mc)])

            pos.append(f"BASIS: {basis} [PAIR_SEP] CHANGED: {changed}")
            neg.append(f"BASIS: {mismatch_basis} [PAIR_SEP] CHANGED: {changed}")
            neg.append(f"BASIS: {basis} [PAIR_SEP] CHANGED: {mismatch_changed}")

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
        data_delta = delta_mismatch_text_data(sentence_meta, pair_meta, vid, seed)

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

            metrics = fit_text_baseline(data_delta, kind, max_features, c, max_iter, seed)
            row = {
                "text_probe_family": TEXT_DELTA_MISMATCH_FAMILY,
                "variable_id": vid,
                "variable": vname,
                "model_kind": kind,
            }
            row.update(metrics)
            rows.append(row)
            pbar.update(1)
    pbar.close()
    return pd.DataFrame(rows)


def train_null_label_controls(
    sentence_meta: pd.DataFrame,
    cache: dict[str, Any],
    c: float,
    max_iter: int,
    seed: int,
    num_permutations: int,
) -> pd.DataFrame:
    if num_permutations <= 0:
        return pd.DataFrame()

    rows = []
    var_table = variables(sentence_meta)
    layer_names = get_layer_names(cache)
    reprs = {"final_token": cache["final_token"], "mean_pooled": cache["mean_pooled"]}

    expected = len(var_table) * len(layer_names) * len(reprs) * num_permutations
    pbar = tqdm(total=expected, desc="Null label-shuffle controls")

    for _, vr in var_table.iterrows():
        vid = int(vr["variable_id"])
        vname = str(vr["variable"])

        for repr_name, tensor in reprs.items():
            for layer_idx, layer_name in enumerate(layer_names):
                true_data = sentence_activation_data(sentence_meta, tensor, vid, layer_idx)
                x_train, y_train_true = true_data["train"]

                for perm_id in range(num_permutations):
                    rng = np.random.default_rng(seed + vid * 100_000 + layer_idx * 1_000 + perm_id)
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
                        "variable_id": vid,
                        "variable": vname,
                        "representation": repr_name,
                        "layer_idx": int(layer_idx),
                        "layer_name": str(layer_name),
                        "permutation_id": int(perm_id),
                    }
                    row.update(metrics)
                    rows.append(row)
                    pbar.update(1)

    pbar.close()
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


def compare_results(best_activation: pd.DataFrame, text_results: pd.DataFrame, null_results: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    best_text = best_text_by_task(text_results)
    best_null = best_null_by_variable(null_results)

    rows = []

    for _, a in best_activation.iterrows():
        vid = int(a["variable_id"])
        family = a["probe_family"]

        if family == SENTENCE_FAMILY:
            text_family = TEXT_SENTENCE_FAMILY
        elif family == DELTA_MISMATCH_FAMILY:
            text_family = TEXT_DELTA_MISMATCH_FAMILY
        else:
            continue

        t = best_text[(best_text["variable_id"] == vid) & (best_text["text_probe_family"] == text_family)]
        if len(t) == 1:
            t = t.iloc[0]
            text_kind = t["model_kind"]
            text_val = float(t["val_auroc"])
            text_test = float(t["test_auroc"])
        else:
            text_kind = None
            text_val = np.nan
            text_test = np.nan

        n_val = np.nan
        n_test = np.nan
        if family == SENTENCE_FAMILY and not best_null.empty:
            n = best_null[best_null["variable_id"] == vid]
            if len(n) == 1:
                n_val = float(n.iloc[0]["val_auroc"])
                n_test = float(n.iloc[0]["test_auroc"])

        rows.append(
            {
                "probe_family": family,
                "variable_id": vid,
                "variable": a["variable"],
                "activation_representation": a["representation"],
                "activation_layer_idx": int(a["layer_idx"]),
                "activation_layer_name": a["layer_name"],
                "activation_val_auroc": float(a["val_auroc"]),
                "activation_test_auroc": float(a["test_auroc"]),
                "activation_test_accuracy": float(a["test_accuracy"]),
                "best_text_model_kind": text_kind,
                "best_text_val_auroc": text_val,
                "best_text_test_auroc": text_test,
                "activation_minus_text_test_auroc": float(a["test_auroc"] - text_test) if not np.isnan(text_test) else np.nan,
                "best_null_val_auroc": n_val,
                "best_null_test_auroc": n_test,
                "activation_minus_null_test_auroc": float(a["test_auroc"] - n_test) if not np.isnan(n_test) else np.nan,
                "suspiciously_high_test_auroc": bool(a.get("suspiciously_high_test_auroc", False)),
                "possible_overfit": bool(a.get("possible_overfit", False)),
                "weak_signal": bool(a.get("weak_signal", False)),
            }
        )

    comparison = pd.DataFrame(rows).sort_values(["probe_family", "variable_id"]).reset_index(drop=True)

    # Variable-level evidence status. This is not a loophole. It is a blunt classification of what the result permits.
    status_rows = []
    for vid, group in comparison.groupby("variable_id", sort=True):
        variable = group["variable"].iloc[0]
        sent = group[group["probe_family"] == SENTENCE_FAMILY]
        delta = group[group["probe_family"] == DELTA_MISMATCH_FAMILY]

        row = {"variable_id": int(vid), "variable": variable}

        if len(sent) == 1:
            s = sent.iloc[0]
            row.update({
                "sentence_activation_test_auroc": float(s["activation_test_auroc"]),
                "sentence_best_text_test_auroc": float(s["best_text_test_auroc"]),
                "sentence_activation_minus_text": float(s["activation_minus_text_test_auroc"]),
                "sentence_best_layer_idx": int(s["activation_layer_idx"]),
                "sentence_best_representation": s["activation_representation"],
            })

        if len(delta) == 1:
            d = delta.iloc[0]
            row.update({
                "delta_mismatch_activation_test_auroc": float(d["activation_test_auroc"]),
                "delta_mismatch_best_text_test_auroc": float(d["best_text_test_auroc"]),
                "delta_mismatch_activation_minus_text": float(d["activation_minus_text_test_auroc"]),
                "delta_mismatch_best_layer_idx": int(d["activation_layer_idx"]),
                "delta_mismatch_best_representation": d["activation_representation"],
            })

        # Conservative evidence classification.
        s_auc = row.get("sentence_activation_test_auroc", np.nan)
        s_text = row.get("sentence_best_text_test_auroc", np.nan)
        s_margin = row.get("sentence_activation_minus_text", np.nan)
        s_layer = row.get("sentence_best_layer_idx", -1)
        d_auc = row.get("delta_mismatch_activation_test_auroc", np.nan)
        d_margin = row.get("delta_mismatch_activation_minus_text", np.nan)

        if np.isnan(s_auc):
            status = "missing_sentence_result"
        elif s_auc < 0.65:
            status = "failed_low_activation_recoverability"
        elif not np.isnan(s_text) and s_text >= s_auc - 0.02:
            status = "failed_text_baseline_matches_or_beats_activation"
        elif s_layer <= 1 and s_auc >= 0.80:
            status = "artifact_risk_best_layer_too_early"
        elif s_margin >= 0.05 and s_auc >= 0.70 and (np.isnan(d_auc) or d_auc >= 0.60):
            status = "promising_activation_signal_needs_inspection"
        else:
            status = "unclear_or_weak_after_controls"

        row["evidence_status"] = status
        row["mechanistic_claim_allowed"] = bool(status == "promising_activation_signal_needs_inspection")
        row["recommended_next_action"] = {
            "failed_low_activation_recoverability": "Do not pursue this variable in Pythia-70M until dataset/model changes.",
            "failed_text_baseline_matches_or_beats_activation": "Inspect examples and redesign splits/templates; current result is likely surface-classifiable.",
            "artifact_risk_best_layer_too_early": "Inspect token-level artifacts; require later-layer or cross-template evidence before claiming structure.",
            "promising_activation_signal_needs_inspection": "Manually inspect templates, run token/text baselines, then consider SAE-latent analysis.",
            "unclear_or_weak_after_controls": "Treat as inconclusive; improve dataset controls before scaling.",
            "missing_sentence_result": "Debug missing probe result.",
        }[status]

        status_rows.append(row)

    status = pd.DataFrame(status_rows).sort_values("variable_id").reset_index(drop=True)
    return comparison, status


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
        "script": "strict_train_raw_activation_probes.py",
        "activation_families": [SENTENCE_FAMILY, DELTA_MISMATCH_FAMILY],
        "text_baseline_families": [TEXT_SENTENCE_FAMILY, TEXT_DELTA_MISMATCH_FAMILY],
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
        description="Strict raw activation probe run with text baselines and null controls."
    )
    parser.add_argument(
        "--activation-cache",
        type=Path,
        default=Path("artifacts/activation_cache/feature_dataset/pythia70m/pythia70m_feature_activations.pt"),
    )
    parser.add_argument(
        "--sentence-metadata",
        type=Path,
        default=Path("artifacts/activation_cache/feature_dataset/pythia70m/sentence_metadata.parquet"),
    )
    parser.add_argument(
        "--pair-metadata",
        type=Path,
        default=Path("artifacts/activation_cache/feature_dataset/pythia70m/pair_metadata.parquet"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/probe_data/raw_activation_probes_strict/pythia70m"),
    )
    parser.add_argument(
        "--github-export-dir",
        type=Path,
        default=Path("artifacts/probe_data/raw_activation_probes_strict/pythia70m_github_export"),
    )
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--max-iter", type=int, default=2000)
    parser.add_argument("--text-max-features", type=int, default=5000)
    parser.add_argument("--num-null-permutations", type=int, default=3)
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

    text_results = train_text_baselines(
        sentence_meta=sentence_meta,
        pair_meta=pair_meta,
        c=args.c,
        max_iter=args.max_iter,
        seed=args.seed,
        max_features=args.text_max_features,
    )

    null_results = train_null_label_controls(
        sentence_meta=sentence_meta,
        cache=cache,
        c=args.c,
        max_iter=args.max_iter,
        seed=args.seed,
        num_permutations=args.num_null_permutations,
    )

    comparison, evidence_status = compare_results(best, text_results, null_results)

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
        args=args,
    )


if __name__ == "__main__":
    main()
