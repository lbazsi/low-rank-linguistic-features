#!/usr/bin/env python3

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from safetensors.torch import load_file
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


TEXT_KEYS = (
    "text",
    "sentence",
    "content",
)


def extract_text(item):
    for key in TEXT_KEYS:
        if key in item:
            return str(item[key])

    raise KeyError(
        f"No text field in pair item. "
        f"Available keys: {list(item.keys())}"
    )


def extract_pair(row):
    pair = row["pair"]

    basis = None
    changed = None

    for item in pair:
        typ = str(
            item.get(
                "type",
                "",
            )
        ).strip().lower()

        if typ == "basis":
            basis = extract_text(item)

        elif typ in {
            "changed",
            "change",
            "contrast",
            "target",
        }:
            changed = extract_text(item)

    # Safe fallback for the known 2-member pair schema.
    if basis is None or changed is None:
        if len(pair) != 2:
            raise RuntimeError(
                f"Could not resolve basis/changed "
                f"for row {row.get('id')}"
            )

        basis = extract_text(pair[0])
        changed = extract_text(pair[1])

    return basis, changed


def normalize_split(x):
    x = str(x).strip().lower()

    if x in {
        "validation",
        "valid",
        "dev",
    }:
        return "val"

    return x


def load_controlled_dataset(root):
    root = Path(root)

    grouped = {}

    files = sorted(
        root.rglob("*.jsonl")
    )

    if len(files) != 40:
        raise RuntimeError(
            f"Expected 40 JSONLs; found {len(files)}"
        )

    for path in files:
        with path.open(
            encoding="utf-8"
        ) as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                row = json.loads(line)

                vid = int(
                    row["variable_id"]
                )

                basis, changed = extract_pair(
                    row
                )

                grouped.setdefault(
                    vid,
                    [],
                ).append(
                    {
                        "id":
                            str(
                                row["id"]
                            ),

                        "variable":
                            str(
                                row["variable"]
                            ),

                        "split":
                            normalize_split(
                                row["split"]
                            ),

                        "basis":
                            basis,

                        "changed":
                            changed,
                    }
                )

    if set(grouped) != set(
        range(1, 41)
    ):
        raise RuntimeError(
            "Dataset does not contain exactly "
            "variable IDs 1..40."
        )

    for vid in grouped:
        if len(grouped[vid]) != 500:
            raise RuntimeError(
                f"Variable {vid}: expected 500 pairs, "
                f"found {len(grouped[vid])}"
            )

    return grouped


def bootstrap_mean_ci(
    x,
    *,
    n_boot,
    rng,
):
    x = np.asarray(
        x,
        dtype=np.float64,
    )

    n = len(x)

    if n == 0:
        return (
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        )

    samples = rng.integers(
        0,
        n,
        size=(
            n_boot,
            n,
        ),
    )

    boot = x[
        samples
    ].mean(
        axis=1
    )

    mean = float(
        x.mean()
    )

    lo, hi = np.quantile(
        boot,
        [
            0.025,
            0.975,
        ],
    )

    p_lo = (
        np.sum(
            boot <= 0
        )
        + 1
    ) / (
        n_boot
        + 1
    )

    p_hi = (
        np.sum(
            boot >= 0
        )
        + 1
    ) / (
        n_boot
        + 1
    )

    p_two = min(
        1.0,
        2.0
        * min(
            p_lo,
            p_hi,
        ),
    )

    return (
        mean,
        float(lo),
        float(hi),
        float(p_two),
    )


def cosine_rows(
    a,
    b,
):
    a = np.asarray(
        a,
        dtype=np.float64,
    )

    b = np.asarray(
        b,
        dtype=np.float64,
    )

    num = (
        a * b
    ).sum(
        axis=1
    )

    den = (
        np.linalg.norm(
            a,
            axis=1,
        )
        *
        np.linalg.norm(
            b,
            axis=1,
        )
    )

    return num / np.maximum(
        den,
        1e-12,
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data-dir",
        default=(
            "data/feature_dataset"
        ),
    )

    parser.add_argument(
        "--sae-dir",
        default=(
            "artifacts/sae_canonical/"
            "xglm564m_hidden12_batchtopk16x_k256"
        ),
    )

    parser.add_argument(
        "--candidates",
        default=(
            "artifacts/causal_candidates/"
            "ablation_primary_candidates.csv"
        ),
    )

    parser.add_argument(
        "--ranking",
        default=(
            "artifacts/causal_candidates/"
            "causal_candidate_ranking.csv"
        ),
    )

    parser.add_argument(
        "--output-dir",
        default=(
            "artifacts/causal_interventions/"
            "ablation_screen"
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
        "--num-controls",
        type=int,
        default=3,
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

    outdir = Path(
        args.output_dir
    )

    outdir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # DATA + CANDIDATES
    # ========================================================

    dataset = load_controlled_dataset(
        args.data_dir
    )

    candidates = pd.read_csv(
        args.candidates
    ).sort_values(
        "variable_id"
    )

    ranking = pd.read_csv(
        args.ranking
    ).sort_values(
        "variable_id"
    )

    if len(candidates) != 40:
        raise RuntimeError(
            f"Expected 40 candidate rows; "
            f"found {len(candidates)}"
        )

    if candidates[
        "variable_id"
    ].nunique() != 40:
        raise RuntimeError(
            "Candidate table does not contain "
            "40 unique variables."
        )

    grade_map = {
        int(r["variable_id"]):
            str(
                r[
                    "inspection_grade"
                ]
            )
        for _, r
        in ranking.iterrows()
    }

    role_map = {
        int(r["variable_id"]):
            str(
                r[
                    "ablation_role"
                ]
            )
        for _, r
        in ranking.iterrows()
    }

    candidate_by_variable = {
        int(r["variable_id"]):
            int(r["feature_id"])
        for _, r
        in candidates.iterrows()
    }

    selected_feature_ids = sorted(
        set(
            candidate_by_variable.values()
        )
    )

    feature_to_col = {
        fid: i
        for i, fid
        in enumerate(
            selected_feature_ids
        )
    }

    print(
        "Variables:",
        len(candidate_by_variable),
    )

    print(
        "Unique selected SAE features:",
        len(selected_feature_ids),
    )

    # ========================================================
    # SAE CONFIG
    # ========================================================

    sae_dir = Path(
        args.sae_dir
    )

    config = json.loads(
        (
            sae_dir
            / "sae_inference_config.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    weights_path = (
        sae_dir
        / "sae_inference.safetensors"
    )

    if not weights_path.is_file():
        raise FileNotFoundError(
            weights_path
        )

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    if device.type != "cuda":
        raise RuntimeError(
            "CUDA is required."
        )

    # ========================================================
    # MODEL
    # ========================================================

    print(
        "Loading tokenizer..."
    )

    tokenizer = (
        AutoTokenizer
        .from_pretrained(
            config["model"],
            use_fast=False,
        )
    )

    tokenizer.padding_side = "right"

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = (
            tokenizer.eos_token
        )

    print(
        "Loading XGLM..."
    )

    model = (
        AutoModelForCausalLM
        .from_pretrained(
            config["model"],
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        )
    )

    model.to(
        device
    )

    model.eval()

    if not (
        hasattr(
            model,
            "model",
        )
        and hasattr(
            model.model,
            "layers",
        )
    ):
        raise RuntimeError(
            "Could not locate XGLM decoder layers."
        )

    layers = model.model.layers

    hidden_state_index = int(
        config[
            "hidden_state_index"
        ]
    )

    intervention_layer_index = (
        hidden_state_index
        - 1
    )

    if not (
        0
        <= intervention_layer_index
        < len(layers)
    ):
        raise RuntimeError(
            f"Invalid intervention layer "
            f"{intervention_layer_index}"
        )

    intervention_layer = layers[
        intervention_layer_index
    ]

    print(
        "Hidden-state index:",
        hidden_state_index,
    )

    print(
        "Intervening after decoder layer:",
        intervention_layer_index,
    )

    # ========================================================
    # LOAD ONLY NECESSARY SAE TENSORS
    # ========================================================

    print(
        "Loading SAE..."
    )

    sd = load_file(
        str(
            weights_path
        ),
        device="cpu",
    )

    selected_index_cpu = torch.tensor(
        selected_feature_ids,
        dtype=torch.long,
    )

    W_enc = (
        sd["W_enc"][
            :,
            selected_index_cpu,
        ]
        .float()
        .to(
            device
        )
    )

    W_dec = (
        sd["W_dec"][
            selected_index_cpu,
            :,
        ]
        .float()
        .to(
            device
        )
    )

    b_enc = (
        sd["b_enc"][
            selected_index_cpu
        ]
        .float()
        .to(
            device
        )
    )

    threshold = (
        sd["threshold"][
            selected_index_cpu
        ]
        .float()
        .to(
            device
        )
    )

    b_dec = (
        sd["b_dec"]
        .float()
        .to(
            device
        )
    )

    del sd

    activation_scale = float(
        config[
            "activation_scale"
        ]
    )

    decoder_norms = (
        W_dec
        .norm(
            dim=1
        )
        .detach()
        .cpu()
        .numpy()
    )

    # ========================================================
    # FORWARD HELPERS
    # ========================================================

    def make_ablation_hook(
        feature_col,
    ):
        w_enc = W_enc[
            :,
            feature_col,
        ]

        w_dec = W_dec[
            feature_col,
            :,
        ]

        bias = b_enc[
            feature_col
        ]

        thresh = threshold[
            feature_col
        ]

        def hook(
            module,
            inputs,
            output,
        ):
            if isinstance(
                output,
                tuple,
            ):
                h = output[0]
            else:
                h = output

            original_dtype = (
                h.dtype
            )

            h32 = h.float()

            x_scaled = (
                h32
                * activation_scale
            )

            pre = (
                (
                    x_scaled
                    - b_dec
                )
                @ w_enc
                + bias
            )

            raw = torch.relu(
                pre
            )

            act = torch.where(
                raw > thresh,
                raw,
                torch.zeros_like(
                    raw
                ),
            )

            # Exact removal of this feature's
            # decoder contribution in original
            # XGLM residual units.
            delta = (
                act.unsqueeze(
                    -1
                )
                * w_dec
            ) / activation_scale

            h_new = (
                h32
                - delta
            ).to(
                original_dtype
            )

            if isinstance(
                output,
                tuple,
            ):
                return (
                    h_new,
                    *output[1:],
                )

            return h_new

        return hook

    def forward_texts(
        texts,
        *,
        intervention_feature=None,
        collect_selected_acts=False,
    ):
        representations = []
        mean_acts = []
        fire_flags = []

        handle = None

        if intervention_feature is not None:
            col = feature_to_col[
                int(
                    intervention_feature
                )
            ]

            handle = (
                intervention_layer
                .register_forward_hook(
                    make_ablation_hook(
                        col
                    )
                )
            )

        try:
            for start in range(
                0,
                len(texts),
                args.batch_size,
            ):
                batch_texts = texts[
                    start:
                    start
                    + args.batch_size
                ]

                encoded = tokenizer(
                    batch_texts,
                    padding=True,
                    truncation=True,
                    max_length=args.max_length,
                    add_special_tokens=False,
                    return_tensors="pt",
                )

                input_ids = (
                    encoded[
                        "input_ids"
                    ]
                    .to(
                        device
                    )
                )

                attention_mask = (
                    encoded[
                        "attention_mask"
                    ]
                    .to(
                        device
                    )
                )

                with torch.inference_mode():
                    outputs = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        output_hidden_states=True,
                        use_cache=False,
                        return_dict=True,
                    )

                final_hidden = (
                    outputs
                    .hidden_states[
                        -1
                    ]
                    .float()
                )

                mask = (
                    attention_mask
                    .float()
                    .unsqueeze(
                        -1
                    )
                )

                pooled = (
                    (
                        final_hidden
                        * mask
                    )
                    .sum(
                        dim=1
                    )
                    /
                    mask.sum(
                        dim=1
                    ).clamp_min(
                        1.0
                    )
                )

                representations.append(
                    pooled
                    .cpu()
                    .numpy()
                )

                if collect_selected_acts:
                    layer_hidden = (
                        outputs
                        .hidden_states[
                            hidden_state_index
                        ]
                        .float()
                    )

                    x_scaled = (
                        layer_hidden
                        * activation_scale
                    )

                    pre = (
                        (
                            x_scaled
                            - b_dec
                        )
                        @ W_enc
                        + b_enc
                    )

                    raw = torch.relu(
                        pre
                    )

                    acts = torch.where(
                        raw
                        > threshold,
                        raw,
                        torch.zeros_like(
                            raw
                        ),
                    )

                    acts = (
                        acts
                        * mask
                    )

                    sentence_mean = (
                        acts.sum(
                            dim=1
                        )
                        /
                        mask.sum(
                            dim=1
                        ).clamp_min(
                            1.0
                        )
                    )

                    sentence_fire = (
                        (
                            acts
                            > 0
                        )
                        .any(
                            dim=1
                        )
                        .float()
                    )

                    mean_acts.append(
                        sentence_mean
                        .cpu()
                        .numpy()
                    )

                    fire_flags.append(
                        sentence_fire
                        .cpu()
                        .numpy()
                    )

                del outputs

        finally:
            if handle is not None:
                handle.remove()

        reps = np.concatenate(
            representations,
            axis=0,
        )

        if not collect_selected_acts:
            return (
                reps,
                None,
                None,
            )

        return (
            reps,
            np.concatenate(
                mean_acts,
                axis=0,
            ),
            np.concatenate(
                fire_flags,
                axis=0,
            ),
        )

    # ========================================================
    # MAIN SCREEN
    # ========================================================

    summary_rows = []
    compare_rows = []
    control_rows = []
    pair_rows = []

    rng_master = np.random.default_rng(
        args.seed
    )

    for variable_id in range(
        1,
        41,
    ):
        records = dataset[
            variable_id
        ]

        variable = records[
            0
        ][
            "variable"
        ]

        target_feature = (
            candidate_by_variable[
                variable_id
            ]
        )

        target_col = (
            feature_to_col[
                target_feature
            ]
        )

        print()
        print(
            "=" * 80
        )

        print(
            f"VARIABLE {variable_id:02d}: "
            f"{variable}"
        )

        print(
            f"Target feature: "
            f"{target_feature}"
        )

        print(
            "=" * 80
        )

        ids = np.array(
            [
                r["id"]
                for r
                in records
            ],
            dtype=object,
        )

        splits = np.array(
            [
                r["split"]
                for r
                in records
            ],
            dtype=object,
        )

        basis_texts = [
            r["basis"]
            for r
            in records
        ]

        changed_texts = [
            r["changed"]
            for r
            in records
        ]

        # ----------------------------------------------------
        # Baseline forward passes
        # ----------------------------------------------------

        basis_repr, basis_acts, basis_fire = (
            forward_texts(
                basis_texts,
                collect_selected_acts=True,
            )
        )

        changed_repr, changed_acts, changed_fire = (
            forward_texts(
                changed_texts,
                collect_selected_acts=True,
            )
        )

        train_mask = (
            splits
            == "train"
        )

        if not train_mask.any():
            raise RuntimeError(
                f"Variable {variable_id}: "
                f"no train examples."
            )

        # ----------------------------------------------------
        # Train-only downstream linguistic direction.
        #
        # This is learned at the FINAL XGLM layer.
        # Therefore the causal outcome is downstream
        # from the SAE intervention layer.
        # ----------------------------------------------------

        train_delta = (
            changed_repr[
                train_mask
            ]
            -
            basis_repr[
                train_mask
            ]
        )

        direction = (
            train_delta.mean(
                axis=0
            )
        )

        direction_norm = float(
            np.linalg.norm(
                direction
            )
        )

        if direction_norm < 1e-12:
            raise RuntimeError(
                f"Variable {variable_id}: "
                f"zero downstream train direction."
            )

        direction = (
            direction
            / direction_norm
        )

        # ----------------------------------------------------
        # Decide which side actually contains more
        # target-feature activation using TRAIN ONLY.
        # ----------------------------------------------------

        target_basis_mean = float(
            basis_acts[
                train_mask,
                target_col,
            ].mean()
        )

        target_changed_mean = float(
            changed_acts[
                train_mask,
                target_col,
            ].mean()
        )

        target_basis_fire = float(
            basis_fire[
                train_mask,
                target_col,
            ].mean()
        )

        target_changed_fire = float(
            changed_fire[
                train_mask,
                target_col,
            ].mean()
        )

        if (
            target_changed_mean
            >= target_basis_mean
        ):
            intervention_side = (
                "changed"
            )

            side_acts = (
                changed_acts[
                    train_mask
                ]
            )

            side_fire = (
                changed_fire[
                    train_mask
                ]
            )

        else:
            intervention_side = (
                "basis"
            )

            side_acts = (
                basis_acts[
                    train_mask
                ]
            )

            side_fire = (
                basis_fire[
                    train_mask
                ]
            )

        print(
            "Intervention side:",
            intervention_side,
        )

        print(
            "Train target mean acts:",
            f"basis={target_basis_mean:.6f}",
            f"changed={target_changed_mean:.6f}",
        )

        # ----------------------------------------------------
        # TRAIN-ONLY activation-matched controls.
        #
        # Controls are selected from the other 39
        # causal-candidate features based on:
        #   - activation magnitude on intervention side
        #   - firing rate
        #   - decoder norm
        #
        # Heldout val/test data are not used.
        # ----------------------------------------------------

        side_mean = (
            side_acts.mean(
                axis=0
            )
        )

        side_fire_rate = (
            side_fire.mean(
                axis=0
            )
        )

        tm = float(
            side_mean[
                target_col
            ]
        )

        tf = float(
            side_fire_rate[
                target_col
            ]
        )

        tn = float(
            decoder_norms[
                target_col
            ]
        )

        matches = []

        for col, fid in enumerate(
            selected_feature_ids
        ):
            if fid == target_feature:
                continue

            cm = float(
                side_mean[
                    col
                ]
            )

            cf = float(
                side_fire_rate[
                    col
                ]
            )

            cn = float(
                decoder_norms[
                    col
                ]
            )

            activation_distance = abs(
                math.log1p(
                    max(
                        cm,
                        0.0,
                    )
                )
                -
                math.log1p(
                    max(
                        tm,
                        0.0,
                    )
                )
            )

            fire_distance = abs(
                cf - tf
            )

            norm_distance = abs(
                math.log(
                    max(
                        cn,
                        1e-8,
                    )
                    /
                    max(
                        tn,
                        1e-8,
                    )
                )
            )

            distance = (
                activation_distance
                + 2.0
                * fire_distance
                + 0.25
                * norm_distance
            )

            matches.append(
                (
                    distance,
                    fid,
                    cm,
                    cf,
                    cn,
                )
            )

        matches.sort(
            key=lambda x:
                x[0]
        )

        controls = [
            int(
                x[1]
            )
            for x
            in matches[
                :args.num_controls
            ]
        ]

        print(
            "Matched controls:",
            controls,
        )

        for rank_idx, item in enumerate(
            matches[
                :args.num_controls
            ],
            start=1,
        ):
            (
                distance,
                fid,
                cm,
                cf,
                cn,
            ) = item

            control_rows.append(
                {
                    "variable_id":
                        variable_id,

                    "variable":
                        variable,

                    "target_feature":
                        target_feature,

                    "intervention_side":
                        intervention_side,

                    "control_rank":
                        rank_idx,

                    "control_feature":
                        int(
                            fid
                        ),

                    "matching_distance":
                        float(
                            distance
                        ),

                    "target_side_mean_activation":
                        tm,

                    "control_side_mean_activation":
                        float(
                            cm
                        ),

                    "target_side_fire_rate":
                        tf,

                    "control_side_fire_rate":
                        float(
                            cf
                        ),

                    "target_decoder_norm":
                        tn,

                    "control_decoder_norm":
                        float(
                            cn
                        ),
                }
            )

        # ----------------------------------------------------
        # Heldout intervention
        # ----------------------------------------------------

        for split in (
            "val",
            "test",
        ):
            split_mask = (
                splits == split
            )

            split_idx = np.where(
                split_mask
            )[0]

            if len(
                split_idx
            ) == 0:
                continue

            b = basis_repr[
                split_mask
            ]

            c = changed_repr[
                split_mask
            ]

            baseline_delta = (
                c - b
            )

            baseline_score = (
                baseline_delta
                @ direction
            )

            intervention_features = [
                target_feature,
                *controls,
            ]

            attenuation_by_feature = {}

            for intervention_feature in (
                intervention_features
            ):
                if (
                    intervention_side
                    == "changed"
                ):
                    texts = [
                        changed_texts[
                            i
                        ]
                        for i
                        in split_idx
                    ]

                    inter_repr, _, _ = (
                        forward_texts(
                            texts,
                            intervention_feature=(
                                intervention_feature
                            ),
                            collect_selected_acts=False,
                        )
                    )

                    intervention_delta = (
                        inter_repr
                        - b
                    )

                    local_cosine = (
                        cosine_rows(
                            inter_repr,
                            c,
                        )
                    )

                else:
                    texts = [
                        basis_texts[
                            i
                        ]
                        for i
                        in split_idx
                    ]

                    inter_repr, _, _ = (
                        forward_texts(
                            texts,
                            intervention_feature=(
                                intervention_feature
                            ),
                            collect_selected_acts=False,
                        )
                    )

                    intervention_delta = (
                        c
                        - inter_repr
                    )

                    local_cosine = (
                        cosine_rows(
                            inter_repr,
                            b,
                        )
                    )

                intervention_score = (
                    intervention_delta
                    @ direction
                )

                attenuation = (
                    baseline_score
                    - intervention_score
                )

                attenuation_by_feature[
                    intervention_feature
                ] = attenuation

                split_seed = (
                    args.seed
                    + variable_id
                    * 1000
                    + (
                        0
                        if split == "val"
                        else 500
                    )
                    + feature_to_col[
                        intervention_feature
                    ]
                )

                rng = (
                    np.random.default_rng(
                        split_seed
                    )
                )

                (
                    mean_att,
                    ci_lo,
                    ci_hi,
                    p_boot,
                ) = bootstrap_mean_ci(
                    attenuation,
                    n_boot=args.bootstrap,
                    rng=rng,
                )

                mean_baseline = float(
                    baseline_score.mean()
                )

                mean_intervention = float(
                    intervention_score.mean()
                )

                fraction = (
                    mean_att
                    /
                    max(
                        abs(
                            mean_baseline
                        ),
                        1e-12,
                    )
                )

                kind = (
                    "target"
                    if intervention_feature
                    == target_feature
                    else "matched_control"
                )

                summary_rows.append(
                    {
                        "variable_id":
                            variable_id,

                        "variable":
                            variable,

                        "inspection_grade":
                            grade_map[
                                variable_id
                            ],

                        "ablation_role":
                            role_map[
                                variable_id
                            ],

                        "split":
                            split,

                        "intervention_kind":
                            kind,

                        "target_feature":
                            target_feature,

                        "intervention_feature":
                            intervention_feature,

                        "intervention_side":
                            intervention_side,

                        "n_pairs":
                            len(
                                split_idx
                            ),

                        "train_direction_norm":
                            direction_norm,

                        "target_train_basis_mean_activation":
                            target_basis_mean,

                        "target_train_changed_mean_activation":
                            target_changed_mean,

                        "target_train_basis_fire_rate":
                            target_basis_fire,

                        "target_train_changed_fire_rate":
                            target_changed_fire,

                        "baseline_downstream_score":
                            mean_baseline,

                        "intervention_downstream_score":
                            mean_intervention,

                        "mean_attenuation":
                            mean_att,

                        "attenuation_fraction":
                            fraction,

                        "attenuation_ci_low":
                            ci_lo,

                        "attenuation_ci_high":
                            ci_hi,

                        "attenuation_bootstrap_p":
                            p_boot,

                        "mean_final_repr_cosine_to_baseline":
                            float(
                                local_cosine.mean()
                            ),
                    }
                )

                for local_i, global_i in enumerate(
                    split_idx
                ):
                    pair_rows.append(
                        {
                            "variable_id":
                                variable_id,

                            "variable":
                                variable,

                            "pair_id":
                                ids[
                                    global_i
                                ],

                            "split":
                                split,

                            "intervention_kind":
                                kind,

                            "target_feature":
                                target_feature,

                            "intervention_feature":
                                intervention_feature,

                            "intervention_side":
                                intervention_side,

                            "baseline_downstream_score":
                                float(
                                    baseline_score[
                                        local_i
                                    ]
                                ),

                            "intervention_downstream_score":
                                float(
                                    intervention_score[
                                        local_i
                                    ]
                                ),

                            "attenuation":
                                float(
                                    attenuation[
                                        local_i
                                    ]
                                ),

                            "final_repr_cosine_to_baseline":
                                float(
                                    local_cosine[
                                        local_i
                                    ]
                                ),
                        }
                    )

            # ------------------------------------------------
            # Target vs matched-control causal specificity
            # ------------------------------------------------

            target_att = (
                attenuation_by_feature[
                    target_feature
                ]
            )

            control_att = np.stack(
                [
                    attenuation_by_feature[
                        fid
                    ]
                    for fid
                    in controls
                ],
                axis=0,
            ).mean(
                axis=0
            )

            target_minus_control = (
                target_att
                - control_att
            )

            rng_compare = (
                np.random.default_rng(
                    args.seed
                    + variable_id
                    * 10000
                    + (
                        1
                        if split == "val"
                        else 2
                    )
                )
            )

            (
                compare_mean,
                compare_lo,
                compare_hi,
                compare_p,
            ) = bootstrap_mean_ci(
                target_minus_control,
                n_boot=args.bootstrap,
                rng=rng_compare,
            )

            compare_rows.append(
                {
                    "variable_id":
                        variable_id,

                    "variable":
                        variable,

                    "inspection_grade":
                        grade_map[
                            variable_id
                        ],

                    "ablation_role":
                        role_map[
                            variable_id
                        ],

                    "split":
                        split,

                    "target_feature":
                        target_feature,

                    "intervention_side":
                        intervention_side,

                    "control_features":
                        ",".join(
                            str(x)
                            for x
                            in controls
                        ),

                    "target_mean_attenuation":
                        float(
                            target_att.mean()
                        ),

                    "matched_control_mean_attenuation":
                        float(
                            control_att.mean()
                        ),

                    "target_minus_control_attenuation":
                        compare_mean,

                    "target_minus_control_ci_low":
                        compare_lo,

                    "target_minus_control_ci_high":
                        compare_hi,

                    "target_minus_control_bootstrap_p":
                        compare_p,
                }
            )

    # ========================================================
    # SAVE
    # ========================================================

    summary_df = pd.DataFrame(
        summary_rows
    )

    compare_df = pd.DataFrame(
        compare_rows
    )

    control_df = pd.DataFrame(
        control_rows
    )

    pair_df = pd.DataFrame(
        pair_rows
    )

    summary_path = (
        outdir
        / "ablation_results.csv"
    )

    compare_path = (
        outdir
        / "ablation_target_vs_controls.csv"
    )

    control_path = (
        outdir
        / "control_matching.csv"
    )

    pair_path = (
        outdir
        / "ablation_pair_level.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
    )

    compare_df.to_csv(
        compare_path,
        index=False,
    )

    control_df.to_csv(
        control_path,
        index=False,
    )

    pair_df.to_csv(
        pair_path,
        index=False,
    )

    manifest = {
        "stage":
            "Step 7 — SAE feature ablation",

        "variables":
            40,

        "all_inspection_grades_included":
            True,

        "selected_features":
            candidate_by_variable,

        "intervention": (
            "For each token at XGLM hidden state "
            f"{hidden_state_index}, compute the selected "
            "fixed-threshold SAE activation and subtract "
            "a_f * W_dec[f] / activation_scale from the "
            "residual stream."
        ),

        "intervention_side_rule": (
            "Use training data only. Ablate whichever "
            "condition (basis or changed) has higher "
            "mean target-feature activation."
        ),

        "primary_outcome": (
            "Attenuation of a train-only linguistic "
            "pair-difference direction measured at the "
            "final XGLM hidden layer on heldout val/test."
        ),

        "positive_attenuation_means": (
            "Ablation reduced the downstream distinction "
            "between changed and basis."
        ),

        "controls": (
            f"{args.num_controls} other selected SAE "
            "features matched using training-only "
            "activation magnitude, firing rate, and "
            "decoder norm."
        ),

        "bootstrap_resamples":
            args.bootstrap,

        "seed":
            args.seed,

        "model":
            config[
                "model"
            ],

        "hidden_state_index":
            hidden_state_index,

        "decoder_layer_intervened":
            intervention_layer_index,

        "max_length":
            args.max_length,

        "batch_size":
            args.batch_size,

        "outputs": {
            "ablation_results":
                str(
                    summary_path
                ),

            "target_vs_controls":
                str(
                    compare_path
                ),

            "control_matching":
                str(
                    control_path
                ),

            "pair_level":
                str(
                    pair_path
                ),
        },
    }

    manifest_path = (
        outdir
        / "ablation_manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(
        "=" * 80
    )

    print(
        "STEP 7 ABLATION SCREEN COMPLETE"
    )

    print(
        "=" * 80
    )

    print(
        "Summary rows:",
        len(
            summary_df
        ),
    )

    print(
        "Target/control comparison rows:",
        len(
            compare_df
        ),
    )

    print(
        "Pair-level rows:",
        len(
            pair_df
        ),
    )

    print()

    print(
        "Saved:",
        summary_path,
    )

    print(
        "Saved:",
        compare_path,
    )

    print(
        "Saved:",
        control_path,
    )

    print(
        "Saved:",
        pair_path,
    )

    print(
        "Saved:",
        manifest_path,
    )


if __name__ == "__main__":
    main()
