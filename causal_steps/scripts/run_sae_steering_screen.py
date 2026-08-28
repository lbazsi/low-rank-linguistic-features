#!/usr/bin/env python3

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from safetensors.torch import load_file
from transformers import AutoModelForCausalLM, AutoTokenizer


TEXT_KEYS = ("text", "sentence", "content")


def extract_text(item):
    for key in TEXT_KEYS:
        if key in item:
            return str(item[key])
    raise KeyError(f"No text field. Keys: {list(item.keys())}")


def extract_pair(row):
    basis = None
    changed = None

    for item in row["pair"]:
        typ = str(item.get("type", "")).strip().lower()

        if typ == "basis":
            basis = extract_text(item)
        elif typ in {"changed", "change", "contrast", "target"}:
            changed = extract_text(item)

    if basis is None or changed is None:
        pair = row["pair"]
        if len(pair) != 2:
            raise RuntimeError(f"Cannot resolve pair {row.get('id')}")
        basis = extract_text(pair[0])
        changed = extract_text(pair[1])

    return basis, changed


def normalize_split(x):
    x = str(x).strip().lower()
    if x in {"validation", "valid", "dev"}:
        return "val"
    return x


def load_dataset(root):
    root = Path(root)
    grouped = {}

    files = sorted(root.rglob("*.jsonl"))

    if len(files) != 40:
        raise RuntimeError(f"Expected 40 JSONLs, found {len(files)}")

    for path in files:
        with path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue

                row = json.loads(line)
                vid = int(row["variable_id"])
                basis, changed = extract_pair(row)

                grouped.setdefault(vid, []).append({
                    "id": str(row["id"]),
                    "variable": str(row["variable"]),
                    "split": normalize_split(row["split"]),
                    "basis": basis,
                    "changed": changed,
                })

    if set(grouped) != set(range(1, 41)):
        raise RuntimeError("Expected variable IDs 1..40")

    for vid, rows in grouped.items():
        if len(rows) != 500:
            raise RuntimeError(
                f"Variable {vid}: expected 500 pairs, found {len(rows)}"
            )

    return grouped


def cosine_rows(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    num = (a * b).sum(axis=1)
    den = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)

    return num / np.maximum(den, 1e-12)


def bootstrap_mean_ci(x, n_boot, seed):
    x = np.asarray(x, dtype=np.float64)
    n = len(x)

    rng = np.random.default_rng(seed)

    idx = rng.integers(
        0,
        n,
        size=(n_boot, n),
    )

    boot = x[idx].mean(axis=1)

    mean = float(x.mean())

    lo, hi = np.quantile(
        boot,
        [0.025, 0.975],
    )

    p_lo = (np.sum(boot <= 0) + 1) / (n_boot + 1)
    p_hi = (np.sum(boot >= 0) + 1) / (n_boot + 1)

    p = min(
        1.0,
        2.0 * min(p_lo, p_hi),
    )

    return (
        mean,
        float(lo),
        float(hi),
        float(p),
    )


def bh_adjust(p):
    p = np.asarray(p, dtype=float)
    n = len(p)

    order = np.argsort(p)
    ranked = p[order]

    adjusted = (
        ranked
        * n
        / np.arange(1, n + 1)
    )

    adjusted = np.minimum.accumulate(
        adjusted[::-1]
    )[::-1]

    adjusted = np.clip(
        adjusted,
        0,
        1,
    )

    out = np.empty(n)
    out[order] = adjusted

    return out


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data-dir",
        default="data/feature_dataset",
    )

    parser.add_argument(
        "--sae-dir",
        default=(
            "artifacts/sae_canonical/"
            "xglm564m_hidden12_batchtopk16x_k256"
        ),
    )

    parser.add_argument(
        "--ablation-summary",
        default=(
            "artifacts/causal_interventions/"
            "ablation_screen/"
            "ablation_variable_summary.csv"
        ),
    )

    parser.add_argument(
        "--control-matching",
        default=(
            "artifacts/causal_interventions/"
            "ablation_screen/"
            "control_matching.csv"
        ),
    )

    parser.add_argument(
        "--output-dir",
        default=(
            "artifacts/causal_interventions/"
            "steering_screen"
        ),
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=192,
    )

    parser.add_argument(
        "--bootstrap",
        type=int,
        default=2000,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    args = parser.parse_args()

    doses = [0.5, 1.0, 2.0]

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset(args.data_dir)

    summary = pd.read_csv(args.ablation_summary).sort_values(
        "variable_id"
    )

    controls_df = pd.read_csv(args.control_matching).sort_values(
        ["variable_id", "control_rank"]
    )

    if len(summary) != 40:
        raise RuntimeError(
            f"Expected 40 ablation summary rows, found {len(summary)}"
        )

    target_features = {
        int(r["variable_id"]): int(r["target_feature"])
        for _, r in summary.iterrows()
    }

    controls = {}

    for vid in range(1, 41):
        rows = controls_df[
            controls_df["variable_id"] == vid
        ].sort_values("control_rank")

        if len(rows) != 3:
            raise RuntimeError(
                f"Variable {vid}: expected 3 controls, found {len(rows)}"
            )

        controls[vid] = [
            int(x)
            for x in rows["control_feature"].tolist()
        ]

    feature_ids = sorted(set(
        list(target_features.values())
        + [
            f
            for fs in controls.values()
            for f in fs
        ]
    ))

    # ========================================================
    # SAE
    # ========================================================

    sae_dir = Path(args.sae_dir)

    config = json.loads(
        (sae_dir / "sae_inference_config.json").read_text()
    )

    sd = load_file(
        str(sae_dir / "sae_inference.safetensors"),
        device="cpu",
    )

    device = torch.device("cuda")

    feature_index = torch.tensor(
        feature_ids,
        dtype=torch.long,
    )

    W_dec = (
        sd["W_dec"][feature_index, :]
        .float()
        .to(device)
    )

    del sd

    feature_to_col = {
        fid: i
        for i, fid in enumerate(feature_ids)
    }

    decoder_norms = (
        W_dec.norm(dim=1)
        .detach()
        .cpu()
        .numpy()
    )

    activation_scale = float(
        config["activation_scale"]
    )

    hidden_state_index = int(
        config["hidden_state_index"]
    )

    intervention_layer_index = (
        hidden_state_index - 1
    )

    # ========================================================
    # XGLM
    # ========================================================

    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        config["model"],
        use_fast=False,
    )

    tokenizer.padding_side = "right"

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading XGLM...")

    model = AutoModelForCausalLM.from_pretrained(
        config["model"],
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )

    model.to(device)
    model.eval()

    layer = model.model.layers[
        intervention_layer_index
    ]

    print("Model:", config["model"])
    print("Hidden state index:", hidden_state_index)
    print("Intervention decoder layer:", intervention_layer_index)
    print("Unique target/control features:", len(feature_ids))

    # ========================================================
    # FORWARD
    # ========================================================

    def make_steering_hook(
        feature_id,
        coefficient,
        attention_mask,
    ):
        col = feature_to_col[int(feature_id)]

        # coefficient is in SAE activation units.
        vector = (
            float(coefficient)
            * W_dec[col]
            / activation_scale
        )

        mask = (
            attention_mask
            .float()
            .unsqueeze(-1)
        )

        def hook(module, inputs, output):
            if isinstance(output, tuple):
                h = output[0]
            else:
                h = output

            dtype = h.dtype

            h_new = (
                h.float()
                + mask * vector
            ).to(dtype)

            if isinstance(output, tuple):
                return (
                    h_new,
                    *output[1:],
                )

            return h_new

        return hook

    def forward(
        texts,
        *,
        feature_id=None,
        coefficient=None,
    ):
        reps = []

        for start in range(
            0,
            len(texts),
            args.batch_size,
        ):
            batch = texts[
                start:start + args.batch_size
            ]

            encoded = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=args.max_length,
                add_special_tokens=False,
                return_tensors="pt",
            )

            input_ids = encoded["input_ids"].to(device)
            attention_mask = encoded["attention_mask"].to(device)

            handle = None

            if feature_id is not None:
                handle = layer.register_forward_hook(
                    make_steering_hook(
                        feature_id,
                        coefficient,
                        attention_mask,
                    )
                )

            try:
                with torch.inference_mode():
                    out = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        output_hidden_states=True,
                        use_cache=False,
                        return_dict=True,
                    )
            finally:
                if handle is not None:
                    handle.remove()

            final_hidden = (
                out.hidden_states[-1]
                .float()
            )

            mask = (
                attention_mask
                .float()
                .unsqueeze(-1)
            )

            pooled = (
                (final_hidden * mask).sum(dim=1)
                /
                mask.sum(dim=1).clamp_min(1.0)
            )

            reps.append(
                pooled.cpu().numpy()
            )

            del out

        return np.concatenate(
            reps,
            axis=0,
        )

    # ========================================================
    # RUN
    # ========================================================

    result_rows = []
    compare_rows = []
    pair_rows = []

    for vid in range(1, 41):

        row = summary[
            summary["variable_id"] == vid
        ].iloc[0]

        records = dataset[vid]

        variable = str(
            row["variable"]
        )

        target_feature = int(
            row["target_feature"]
        )

        high_side = str(
            row["intervention_side"]
        )

        low_side = (
            "basis"
            if high_side == "changed"
            else "changed"
        )

        basis_mean = float(
            row[
                "target_train_basis_mean_activation"
            ]
        )

        changed_mean = float(
            row[
                "target_train_changed_mean_activation"
            ]
        )

        activation_gap = abs(
            changed_mean - basis_mean
        )

        if activation_gap <= 0:
            raise RuntimeError(
                f"Variable {vid}: non-positive activation gap"
            )

        target_col = feature_to_col[
            target_feature
        ]

        target_norm = float(
            decoder_norms[
                target_col
            ]
        )

        print()
        print("=" * 80)
        print(
            f"VARIABLE {vid:02d}: {variable}"
        )
        print("Target feature:", target_feature)
        print("Feature-high side:", high_side)
        print("Steering side:", low_side)
        print(
            "Train activation gap:",
            f"{activation_gap:.8f}",
        )
        print(
            "Controls:",
            controls[vid],
        )

        basis_texts = [
            r["basis"]
            for r in records
        ]

        changed_texts = [
            r["changed"]
            for r in records
        ]

        splits = np.array([
            r["split"]
            for r in records
        ])

        pair_ids = np.array([
            r["id"]
            for r in records
        ])

        # ----------------------------------------------------
        # Baseline representations
        # ----------------------------------------------------

        basis_repr = forward(
            basis_texts
        )

        changed_repr = forward(
            changed_texts
        )

        train_mask = (
            splits == "train"
        )

        # Train-only downstream direction
        train_delta = (
            changed_repr[train_mask]
            -
            basis_repr[train_mask]
        )

        direction = train_delta.mean(
            axis=0
        )

        norm = np.linalg.norm(
            direction
        )

        if norm <= 1e-12:
            raise RuntimeError(
                f"Variable {vid}: zero train direction"
            )

        direction = direction / norm

        # ----------------------------------------------------
        # Heldout steering
        # ----------------------------------------------------

        for split in ["val", "test"]:

            split_mask = (
                splits == split
            )

            idx = np.where(
                split_mask
            )[0]

            b = basis_repr[
                split_mask
            ]

            c = changed_repr[
                split_mask
            ]

            baseline_delta = c - b

            baseline_score = (
                baseline_delta
                @ direction
            )

            attenuation_store = {}

            intervention_features = [
                target_feature,
                *controls[vid],
            ]

            for dose in doses:

                attenuation_store[
                    dose
                ] = {}

                for intervention_feature in intervention_features:

                    col = feature_to_col[
                        intervention_feature
                    ]

                    feature_norm = float(
                        decoder_norms[col]
                    )

                    if intervention_feature == target_feature:
                        coefficient = (
                            activation_gap
                            * dose
                        )
                        kind = "target"

                    else:
                        # Exact residual-L2 matching:
                        # coefficient_control * ||W_control||
                        # =
                        # coefficient_target * ||W_target||
                        coefficient = (
                            activation_gap
                            * dose
                            * target_norm
                            / max(
                                feature_norm,
                                1e-12,
                            )
                        )

                        kind = "matched_control"

                    if low_side == "basis":
                        texts = [
                            basis_texts[i]
                            for i in idx
                        ]

                        steered = forward(
                            texts,
                            feature_id=intervention_feature,
                            coefficient=coefficient,
                        )

                        intervention_delta = (
                            c - steered
                        )

                        baseline_low = b

                    else:
                        texts = [
                            changed_texts[i]
                            for i in idx
                        ]

                        steered = forward(
                            texts,
                            feature_id=intervention_feature,
                            coefficient=coefficient,
                        )

                        intervention_delta = (
                            steered - b
                        )

                        baseline_low = c

                    intervention_score = (
                        intervention_delta
                        @ direction
                    )

                    attenuation = (
                        baseline_score
                        -
                        intervention_score
                    )

                    attenuation_store[
                        dose
                    ][
                        intervention_feature
                    ] = attenuation

                    cosine = cosine_rows(
                        steered,
                        baseline_low,
                    )

                    (
                        mean_att,
                        ci_lo,
                        ci_hi,
                        p_boot,
                    ) = bootstrap_mean_ci(
                        attenuation,
                        args.bootstrap,
                        (
                            args.seed
                            + vid * 100000
                            + int(dose * 1000) * 100
                            + feature_to_col[
                                intervention_feature
                            ]
                            + (
                                0
                                if split == "val"
                                else 50000
                            )
                        ),
                    )

                    mean_baseline = float(
                        baseline_score.mean()
                    )

                    result_rows.append({
                        "variable_id": vid,
                        "variable": variable,
                        "inspection_grade": row["inspection_grade"],
                        "ablation_screen_category": row["causal_screen_category"],
                        "split": split,
                        "dose": dose,
                        "primary_dose": dose == 1.0,
                        "intervention_kind": kind,
                        "target_feature": target_feature,
                        "intervention_feature": intervention_feature,
                        "feature_high_side": high_side,
                        "steering_side": low_side,
                        "train_target_activation_gap": activation_gap,
                        "steering_coefficient": coefficient,
                        "baseline_downstream_score": mean_baseline,
                        "steered_downstream_score": float(
                            intervention_score.mean()
                        ),
                        "mean_attenuation": mean_att,
                        "attenuation_fraction": (
                            mean_att
                            /
                            max(
                                abs(mean_baseline),
                                1e-12,
                            )
                        ),
                        "attenuation_ci_low": ci_lo,
                        "attenuation_ci_high": ci_hi,
                        "attenuation_bootstrap_p": p_boot,
                        "mean_final_repr_cosine_to_baseline": float(
                            cosine.mean()
                        ),
                    })

                    for local_i, global_i in enumerate(idx):
                        pair_rows.append({
                            "variable_id": vid,
                            "variable": variable,
                            "pair_id": pair_ids[global_i],
                            "split": split,
                            "dose": dose,
                            "intervention_kind": kind,
                            "target_feature": target_feature,
                            "intervention_feature": intervention_feature,
                            "feature_high_side": high_side,
                            "steering_side": low_side,
                            "baseline_downstream_score": float(
                                baseline_score[local_i]
                            ),
                            "steered_downstream_score": float(
                                intervention_score[local_i]
                            ),
                            "attenuation": float(
                                attenuation[local_i]
                            ),
                            "final_repr_cosine_to_baseline": float(
                                cosine[local_i]
                            ),
                        })

                # --------------------------------------------
                # Target vs mean matched controls
                # --------------------------------------------

                target_att = attenuation_store[
                    dose
                ][
                    target_feature
                ]

                control_att = np.stack([
                    attenuation_store[
                        dose
                    ][
                        f
                    ]
                    for f in controls[vid]
                ]).mean(axis=0)

                difference = (
                    target_att - control_att
                )

                (
                    mean_diff,
                    lo_diff,
                    hi_diff,
                    p_diff,
                ) = bootstrap_mean_ci(
                    difference,
                    args.bootstrap,
                    (
                        args.seed
                        + vid * 1000000
                        + int(dose * 1000)
                        + (
                            0
                            if split == "val"
                            else 500000
                        )
                    ),
                )

                compare_rows.append({
                    "variable_id": vid,
                    "variable": variable,
                    "inspection_grade": row["inspection_grade"],
                    "ablation_screen_category": row["causal_screen_category"],
                    "split": split,
                    "dose": dose,
                    "primary_dose": dose == 1.0,
                    "target_feature": target_feature,
                    "feature_high_side": high_side,
                    "steering_side": low_side,
                    "train_target_activation_gap": activation_gap,
                    "control_features": ",".join(
                        str(x)
                        for x in controls[vid]
                    ),
                    "target_mean_attenuation": float(
                        target_att.mean()
                    ),
                    "matched_control_mean_attenuation": float(
                        control_att.mean()
                    ),
                    "target_minus_control_attenuation": mean_diff,
                    "target_minus_control_ci_low": lo_diff,
                    "target_minus_control_ci_high": hi_diff,
                    "target_minus_control_bootstrap_p": p_diff,
                })

    # ========================================================
    # SAVE RAW RESULTS
    # ========================================================

    results_df = pd.DataFrame(
        result_rows
    )

    compare_df = pd.DataFrame(
        compare_rows
    )

    pairs_df = pd.DataFrame(
        pair_rows
    )

    results_path = (
        outdir
        / "steering_results.csv"
    )

    compare_path = (
        outdir
        / "steering_target_vs_controls.csv"
    )

    pairs_path = (
        outdir
        / "steering_pair_level.csv"
    )

    results_df.to_csv(
        results_path,
        index=False,
    )

    compare_df.to_csv(
        compare_path,
        index=False,
    )

    pairs_df.to_csv(
        pairs_path,
        index=False,
    )

    # ========================================================
    # PRIMARY TEST:
    # TEST SPLIT, 1.0× DOSE ONLY
    # ========================================================

    primary = compare_df[
        (compare_df["split"] == "test")
        &
        (compare_df["dose"] == 1.0)
    ].copy()

    if len(primary) != 40:
        raise RuntimeError(
            f"Expected 40 primary rows, found {len(primary)}"
        )

    primary[
        "target_vs_control_fdr_q"
    ] = bh_adjust(
        primary[
            "target_minus_control_bootstrap_p"
        ].values
    )

    target_primary = results_df[
        (results_df["split"] == "test")
        &
        (results_df["dose"] == 1.0)
        &
        (
            results_df[
                "intervention_kind"
            ]
            == "target"
        )
    ][[
        "variable_id",
        "mean_attenuation",
        "attenuation_fraction",
        "mean_final_repr_cosine_to_baseline",
    ]].rename(columns={
        "mean_attenuation":
            "target_mean_attenuation_primary",

        "attenuation_fraction":
            "target_attenuation_fraction_primary",

        "mean_final_repr_cosine_to_baseline":
            "target_final_repr_cosine_primary",
    })

    primary = primary.merge(
        target_primary,
        on="variable_id",
        validate="one_to_one",
    )

    # Dose response
    target_test = results_df[
        (results_df["split"] == "test")
        &
        (
            results_df[
                "intervention_kind"
            ]
            == "target"
        )
    ].copy()

    pivot = target_test.pivot(
        index="variable_id",
        columns="dose",
        values="mean_attenuation",
    )

    pivot = pivot.rename(columns={
        0.5: "target_attenuation_dose_0_5",
        1.0: "target_attenuation_dose_1_0",
        2.0: "target_attenuation_dose_2_0",
    }).reset_index()

    primary = primary.merge(
        pivot,
        on="variable_id",
        validate="one_to_one",
    )

    primary[
        "dose_monotonic_non_decreasing"
    ] = (
        (
            primary[
                "target_attenuation_dose_0_5"
            ]
            <=
            primary[
                "target_attenuation_dose_1_0"
            ]
        )
        &
        (
            primary[
                "target_attenuation_dose_1_0"
            ]
            <=
            primary[
                "target_attenuation_dose_2_0"
            ]
        )
    )

    def classify(r):
        target_positive = (
            r[
                "target_mean_attenuation_primary"
            ]
            > 0
        )

        better_controls = (
            r[
                "target_minus_control_attenuation"
            ]
            > 0
        )

        fdr_specific = (
            better_controls
            and
            r[
                "target_vs_control_fdr_q"
            ]
            < 0.05
        )

        if target_positive and fdr_specific:
            return "specific_positive"

        if target_positive and better_controls:
            return "positive_control_advantage"

        if target_positive:
            return "positive_nonspecific"

        return "null_or_reverse"

    primary[
        "steering_screen_category"
    ] = primary.apply(
        classify,
        axis=1,
    )

    primary_path = (
        outdir
        / "steering_variable_summary.csv"
    )

    primary.to_csv(
        primary_path,
        index=False,
    )

    manifest = {
        "stage": "Step 8 — SAE feature steering",
        "variables": 40,
        "all_variables_included": True,

        "intervention": (
            "Add the selected SAE decoder direction "
            "to the feature-low member of each pair "
            "at XGLM hidden state 12."
        ),

        "steering_coefficient": (
            "Target feature coefficient is the absolute "
            "train mean activation gap multiplied by dose. "
            "Control feature coefficients are decoder-norm "
            "adjusted so residual perturbation L2 matches "
            "the target perturbation."
        ),

        "doses": [0.5, 1.0, 2.0],

        "primary_dose": 1.0,

        "dose_selection": (
            "Fixed before heldout evaluation. "
            "0.5x and 2.0x are descriptive dose-response "
            "conditions; 1.0x is the primary inferential test."
        ),

        "primary_outcome": (
            "Attenuation of the train-only final-layer "
            "linguistic pair-difference direction."
        ),

        "positive_attenuation_means": (
            "Steering the feature-low sentence toward the "
            "feature-high SAE direction reduced the downstream "
            "linguistic distinction."
        ),

        "controls": (
            "Three Step-7 training-only matched SAE control "
            "features per variable, with exact decoder-vector "
            "L2 perturbation matching during steering."
        ),

        "multiple_comparisons": (
            "Benjamini-Hochberg FDR across the 40 variables "
            "for the primary 1.0x test condition."
        ),

        "bootstrap_resamples": args.bootstrap,
        "seed": args.seed,
        "model": config["model"],
        "hidden_state_index": hidden_state_index,
        "intervention_decoder_layer": intervention_layer_index,
    }

    manifest_path = (
        outdir
        / "steering_manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )

    print()
    print("=" * 80)
    print("STEP 8 STEERING COMPLETE")
    print("=" * 80)

    print(
        "Positive target steering:",
        int(
            (
                primary[
                    "target_mean_attenuation_primary"
                ]
                > 0
            ).sum()
        ),
        "/ 40",
    )

    print(
        "Target > controls:",
        int(
            (
                primary[
                    "target_minus_control_attenuation"
                ]
                > 0
            ).sum()
        ),
        "/ 40",
    )

    print(
        "Positive + FDR-specific:",
        int(
            (
                (
                    primary[
                        "target_mean_attenuation_primary"
                    ]
                    > 0
                )
                &
                (
                    primary[
                        "target_minus_control_attenuation"
                    ]
                    > 0
                )
                &
                (
                    primary[
                        "target_vs_control_fdr_q"
                    ]
                    < 0.05
                )
            ).sum()
        ),
        "/ 40",
    )

    print(
        "Monotonic 0.5→1→2 dose response:",
        int(
            primary[
                "dose_monotonic_non_decreasing"
            ].sum()
        ),
        "/ 40",
    )

    print()
    print("Categories:")
    print(
        primary[
            "steering_screen_category"
        ].value_counts()
    )

    print()
    print("Primary intervention locality:")
    print(
        primary[
            "target_final_repr_cosine_primary"
        ].describe()
    )

    print()

    cols = [
        "variable_id",
        "variable",
        "inspection_grade",
        "ablation_screen_category",
        "target_feature",
        "steering_side",
        "target_mean_attenuation_primary",
        "target_attenuation_fraction_primary",
        "matched_control_mean_attenuation",
        "target_minus_control_attenuation",
        "target_vs_control_fdr_q",
        "dose_monotonic_non_decreasing",
        "target_final_repr_cosine_primary",
        "steering_screen_category",
    ]

    print(
        primary[
            cols
        ]
        .sort_values(
            "target_minus_control_attenuation",
            ascending=False,
        )
        .to_string(
            index=False
        )
    )

    print()
    print("Saved:", results_path)
    print("Saved:", compare_path)
    print("Saved:", primary_path)
    print("Saved:", pairs_path)
    print("Saved:", manifest_path)


if __name__ == "__main__":
    main()
