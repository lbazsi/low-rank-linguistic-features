#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from safetensors.torch import load_file
from transformers import AutoModelForCausalLM, AutoTokenizer


TEXT_KEYS = ("text", "sentence", "content")


def get_text(item):
    for key in TEXT_KEYS:
        if key in item:
            return str(item[key])

    raise RuntimeError(
        f"No sentence text field. Keys: {list(item.keys())}"
    )


def get_pair(row):
    basis = None
    changed = None

    for item in row["pair"]:
        typ = str(
            item.get("type", "")
        ).strip().lower()

        if typ == "basis":
            basis = get_text(item)

        elif typ in {
            "changed",
            "change",
            "contrast",
            "target",
        }:
            changed = get_text(item)

    if basis is None or changed is None:
        pair = row["pair"]

        if len(pair) != 2:
            raise RuntimeError(
                f"Could not resolve pair {row.get('id')}"
            )

        basis = get_text(pair[0])
        changed = get_text(pair[1])

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


def load_dataset(root):
    grouped = {}

    files = sorted(
        Path(root).rglob("*.jsonl")
    )

    if len(files) != 40:
        raise RuntimeError(
            f"Expected 40 JSONLs, found {len(files)}"
        )

    for path in files:
        with path.open(
            encoding="utf-8"
        ) as f:

            for line in f:

                if not line.strip():
                    continue

                row = json.loads(line)

                vid = int(
                    row["variable_id"]
                )

                basis, changed = get_pair(
                    row
                )

                grouped.setdefault(
                    vid,
                    [],
                ).append({
                    "id":
                        str(row["id"]),

                    "variable":
                        str(row["variable"]),

                    "split":
                        normalize_split(
                            row["split"]
                        ),

                    "basis":
                        basis,

                    "changed":
                        changed,
                })

    if set(grouped) != set(range(1, 41)):
        raise RuntimeError(
            "Expected variable IDs 1..40"
        )

    return grouped


def bootstrap_mean_ci(
    x,
    n_boot,
    seed,
):
    x = np.asarray(
        x,
        dtype=np.float64,
    )

    n = len(x)

    rng = np.random.default_rng(
        seed
    )

    idx = rng.integers(
        0,
        n,
        size=(n_boot, n),
    )

    boot = x[
        idx
    ].mean(
        axis=1
    )

    mean = float(
        x.mean()
    )

    lo, hi = np.quantile(
        boot,
        [0.025, 0.975],
    )

    p_lo = (
        np.sum(
            boot <= 0
        )
        + 1
    ) / (
        n_boot + 1
    )

    p_hi = (
        np.sum(
            boot >= 0
        )
        + 1
    ) / (
        n_boot + 1
    )

    p = min(
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
        float(p),
    )


def bh_adjust(p):
    p = np.asarray(
        p,
        dtype=float,
    )

    n = len(p)

    order = np.argsort(p)
    ranked = p[order]

    adjusted = (
        ranked
        * n
        / np.arange(
            1,
            n + 1,
        )
    )

    adjusted = np.minimum.accumulate(
        adjusted[::-1]
    )[::-1]

    adjusted = np.clip(
        adjusted,
        0,
        1,
    )

    out = np.empty(
        n,
        dtype=float,
    )

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
        "--convergence",
        default=(
            "artifacts/causal_interventions/"
            "mechanistic_convergence/"
            "mechanistic_convergence.csv"
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
            "behavioral_evaluation"
        ),
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
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

    doses = [
        0.5,
        1.0,
        2.0,
    ]

    outdir = Path(
        args.output_dir
    )

    outdir.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset = load_dataset(
        args.data_dir
    )

    convergence = pd.read_csv(
        args.convergence
    ).sort_values(
        "variable_id"
    )

    controls_df = pd.read_csv(
        args.control_matching
    ).sort_values(
        [
            "variable_id",
            "control_rank",
        ]
    )

    if len(convergence) != 40:
        raise RuntimeError(
            "Expected 40 convergence rows."
        )

    # ========================================================
    # PREDECLARED COHORT / FEATURES
    # ========================================================

    target_features = {
        int(r["variable_id"]):
            int(r["target_feature"])
        for _, r
        in convergence.iterrows()
    }

    primary_ids = set(
        convergence.loc[
            convergence[
                "primary_mechanistic"
            ].astype(bool),
            "variable_id",
        ].astype(int)
    )

    if len(primary_ids) != 15:
        raise RuntimeError(
            f"Expected frozen primary cohort of 15; "
            f"found {len(primary_ids)}"
        )

    controls = {}

    for vid in range(
        1,
        41,
    ):
        x = controls_df[
            controls_df[
                "variable_id"
            ]
            == vid
        ].sort_values(
            "control_rank"
        )

        if len(x) != 3:
            raise RuntimeError(
                f"Variable {vid}: expected 3 controls"
            )

        controls[
            vid
        ] = [
            int(v)
            for v
            in x[
                "control_feature"
            ].tolist()
        ]

    feature_ids = sorted(
        set(
            list(
                target_features.values()
            )
            +
            [
                feature
                for xs in controls.values()
                for feature in xs
            ]
        )
    )

    feature_to_col = {
        feature: i
        for i, feature
        in enumerate(feature_ids)
    }

    # ========================================================
    # SAE
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

    sd = load_file(
        str(
            sae_dir
            / "sae_inference.safetensors"
        ),
        device="cpu",
    )

    device = torch.device(
        "cuda"
    )

    feature_index = torch.tensor(
        feature_ids,
        dtype=torch.long,
    )

    W_dec = (
        sd[
            "W_dec"
        ][
            feature_index,
            :,
        ]
        .float()
        .to(device)
    )

    del sd

    decoder_norms = (
        W_dec.norm(
            dim=1
        )
        .detach()
        .cpu()
        .numpy()
    )

    activation_scale = float(
        config[
            "activation_scale"
        ]
    )

    hidden_state_index = int(
        config[
            "hidden_state_index"
        ]
    )

    intervention_layer_index = (
        hidden_state_index
        - 1
    )

    # ========================================================
    # MODEL
    # ========================================================

    tokenizer = (
        AutoTokenizer
        .from_pretrained(
            config["model"],
            use_fast=False,
        )
    )

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = (
            tokenizer.eos_token
        )

    if tokenizer.bos_token_id is None:
        raise RuntimeError(
            "Tokenizer has no BOS token; "
            "cannot evaluate first-token divergences "
            "with a common unconditional context."
        )

    print(
        "BOS token:",
        tokenizer.bos_token,
        tokenizer.bos_token_id,
    )

    print(
        "Loading XGLM..."
    )

    model = (
        AutoModelForCausalLM
        .from_pretrained(
            config["model"],
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True,
        )
    )

    model.to(
        device
    )

    model.eval()

    intervention_layer = (
        model.model.layers[
            intervention_layer_index
        ]
    )

    # ========================================================
    # BRANCH POINT CONSTRUCTION
    # ========================================================

    def make_branch_record(
        record,
        high_side,
    ):
        basis_ids = tokenizer.encode(
            record["basis"],
            add_special_tokens=False,
        )

        changed_ids = tokenizer.encode(
            record["changed"],
            add_special_tokens=False,
        )

        k = 0

        while (
            k < len(basis_ids)
            and
            k < len(changed_ids)
            and
            basis_ids[k]
            == changed_ids[k]
        ):
            k += 1

        # Identical token sequence gives no behavioral branch.
        if (
            basis_ids
            == changed_ids
        ):
            return None

        # One sequence ending exactly at the divergence
        # also provides no competing next-token pair.
        if (
            k >= len(basis_ids)
            or
            k >= len(changed_ids)
        ):
            return None

        if k == 0:
            context = [
                tokenizer.bos_token_id
            ]

            bos_fallback = True

        else:
            context = basis_ids[
                :k
            ]

            bos_fallback = False

        if len(context) > args.max_length:
            context = context[
                -args.max_length:
            ]

        if high_side == "changed":
            high_token = changed_ids[
                k
            ]

            low_token = basis_ids[
                k
            ]

        elif high_side == "basis":
            high_token = basis_ids[
                k
            ]

            low_token = changed_ids[
                k
            ]

        else:
            raise RuntimeError(
                f"Unknown feature_high_side: "
                f"{high_side}"
            )

        if high_token == low_token:
            raise RuntimeError(
                "Internal divergence error."
            )

        return {
            "pair_id":
                record["id"],

            "split":
                record["split"],

            "context_ids":
                context,

            "common_prefix_tokens":
                k,

            "bos_fallback":
                bos_fallback,

            "high_token":
                int(high_token),

            "low_token":
                int(low_token),
        }

    # ========================================================
    # FORWARD
    # ========================================================

    def make_hook(
        feature_id,
        coefficient,
        attention_mask,
    ):
        col = feature_to_col[
            int(feature_id)
        ]

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

        def hook(
            module,
            inputs,
            output,
        ):
            if isinstance(
                output,
                tuple,
            ):
                hidden = output[0]
            else:
                hidden = output

            dtype = hidden.dtype

            modified = (
                hidden.float()
                +
                mask * vector
            ).to(dtype)

            if isinstance(
                output,
                tuple,
            ):
                return (
                    modified,
                    *output[1:],
                )

            return modified

        return hook

    def margins(
        branch_rows,
        *,
        feature_id=None,
        coefficient=None,
    ):
        output_margins = []

        for start in range(
            0,
            len(branch_rows),
            args.batch_size,
        ):
            batch = branch_rows[
                start:
                start + args.batch_size
            ]

            max_len = max(
                len(
                    x[
                        "context_ids"
                    ]
                )
                for x in batch
            )

            input_ids = torch.full(
                (
                    len(batch),
                    max_len,
                ),
                tokenizer.pad_token_id,
                dtype=torch.long,
                device=device,
            )

            attention_mask = torch.zeros(
                (
                    len(batch),
                    max_len,
                ),
                dtype=torch.long,
                device=device,
            )

            for i, x in enumerate(
                batch
            ):
                ids = x[
                    "context_ids"
                ]

                n = len(ids)

                input_ids[
                    i,
                    :n,
                ] = torch.tensor(
                    ids,
                    dtype=torch.long,
                    device=device,
                )

                attention_mask[
                    i,
                    :n,
                ] = 1

            handle = None

            if feature_id is not None:
                handle = (
                    intervention_layer
                    .register_forward_hook(
                        make_hook(
                            feature_id,
                            coefficient,
                            attention_mask,
                        )
                    )
                )

            try:
                with torch.inference_mode():
                    outputs = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        use_cache=False,
                        return_dict=True,
                    )

            finally:
                if handle is not None:
                    handle.remove()

            logits = (
                outputs.logits.float()
            )

            last_positions = (
                attention_mask.sum(
                    dim=1
                )
                - 1
            )

            row_indices = torch.arange(
                len(batch),
                device=device,
            )

            next_logits = logits[
                row_indices,
                last_positions,
                :,
            ]

            high_tokens = torch.tensor(
                [
                    x["high_token"]
                    for x in batch
                ],
                dtype=torch.long,
                device=device,
            )

            low_tokens = torch.tensor(
                [
                    x["low_token"]
                    for x in batch
                ],
                dtype=torch.long,
                device=device,
            )

            high_logits = next_logits.gather(
                1,
                high_tokens.unsqueeze(1),
            ).squeeze(1)

            low_logits = next_logits.gather(
                1,
                low_tokens.unsqueeze(1),
            ).squeeze(1)

            margin = (
                high_logits
                - low_logits
            )

            output_margins.extend(
                margin.cpu().numpy()
            )

            del outputs

        return np.asarray(
            output_margins,
            dtype=np.float64,
        )

    # ========================================================
    # EVALUATION
    # ========================================================

    result_rows = []
    pair_rows = []

    for vid in range(
        1,
        41,
    ):
        meta = convergence[
            convergence[
                "variable_id"
            ]
            == vid
        ].iloc[0]

        variable = str(
            meta[
                "variable"
            ]
        )

        target_feature = int(
            meta[
                "target_feature"
            ]
        )

        high_side = str(
            meta[
                "feature_high_side"
            ]
        )

        activation_gap = float(
            meta[
                "train_target_activation_gap"
            ]
        )

        if activation_gap <= 0:
            raise RuntimeError(
                f"Variable {vid}: invalid activation gap"
            )

        target_col = (
            feature_to_col[
                target_feature
            ]
        )

        target_norm = float(
            decoder_norms[
                target_col
            ]
        )

        branch_rows = []

        for record in dataset[
            vid
        ]:
            if record[
                "split"
            ] not in {
                "val",
                "test",
            }:
                continue

            x = make_branch_record(
                record,
                high_side,
            )

            if x is not None:
                branch_rows.append(
                    x
                )

        print()
        print("=" * 80)

        print(
            f"VARIABLE {vid:02d}: "
            f"{variable}"
        )

        print(
            "Target feature:",
            target_feature,
        )

        print(
            "Primary cohort:",
            vid in primary_ids,
        )

        print(
            "Behavioral branch rows:",
            len(branch_rows),
        )

        print(
            "BOS fallback:",
            sum(
                x[
                    "bos_fallback"
                ]
                for x in branch_rows
            ),
        )

        for split in [
            "val",
            "test",
        ]:
            rows = [
                x
                for x in branch_rows
                if x[
                    "split"
                ]
                == split
            ]

            if not rows:
                print(
                    f"WARNING: variable {vid} "
                    f"has zero {split} branch rows"
                )

                continue

            baseline_margin = margins(
                rows
            )

            effects_by_dose = {}

            for dose in doses:
                effects_by_dose[
                    dose
                ] = {}

                interventions = [
                    target_feature,
                    *controls[
                        vid
                    ],
                ]

                for feature in interventions:
                    col = feature_to_col[
                        feature
                    ]

                    feature_norm = float(
                        decoder_norms[
                            col
                        ]
                    )

                    if (
                        feature
                        == target_feature
                    ):
                        coefficient = (
                            activation_gap
                            * dose
                        )

                        kind = "target"

                    else:
                        coefficient = (
                            activation_gap
                            * dose
                            * target_norm
                            /
                            max(
                                feature_norm,
                                1e-12,
                            )
                        )

                        kind = (
                            "matched_control"
                        )

                    steered_margin = margins(
                        rows,
                        feature_id=feature,
                        coefficient=coefficient,
                    )

                    effect = (
                        steered_margin
                        - baseline_margin
                    )

                    effects_by_dose[
                        dose
                    ][
                        feature
                    ] = effect

                    (
                        mean_effect,
                        ci_lo,
                        ci_hi,
                        p_boot,
                    ) = bootstrap_mean_ci(
                        effect,
                        args.bootstrap,
                        (
                            args.seed
                            + vid * 100000
                            + int(
                                dose
                                * 1000
                            )
                            * 100
                            + feature_to_col[
                                feature
                            ]
                            + (
                                0
                                if split == "val"
                                else 50000
                            )
                        ),
                    )

                    high_preference_before = float(
                        (
                            baseline_margin
                            > 0
                        ).mean()
                    )

                    high_preference_after = float(
                        (
                            steered_margin
                            > 0
                        ).mean()
                    )

                    result_rows.append({
                        "variable_id":
                            vid,

                        "variable":
                            variable,

                        "primary_mechanistic":
                            vid in primary_ids,

                        "inspection_grade":
                            meta[
                                "inspection_grade"
                            ],

                        "ablation_category":
                            meta[
                                "ablation_category"
                            ],

                        "steering_category":
                            meta[
                                "steering_category"
                            ],

                        "split":
                            split,

                        "dose":
                            dose,

                        "primary_dose":
                            dose == 1.0,

                        "intervention_kind":
                            kind,

                        "target_feature":
                            target_feature,

                        "intervention_feature":
                            feature,

                        "feature_high_side":
                            high_side,

                        "train_target_activation_gap":
                            activation_gap,

                        "steering_coefficient":
                            coefficient,

                        "n_pairs":
                            len(rows),

                        "bos_fallback_pairs":
                            int(
                                sum(
                                    x[
                                        "bos_fallback"
                                    ]
                                    for x in rows
                                )
                            ),

                        "baseline_mean_logit_margin":
                            float(
                                baseline_margin.mean()
                            ),

                        "steered_mean_logit_margin":
                            float(
                                steered_margin.mean()
                            ),

                        "mean_behavioral_effect":
                            mean_effect,

                        "behavioral_effect_ci_low":
                            ci_lo,

                        "behavioral_effect_ci_high":
                            ci_hi,

                        "behavioral_effect_bootstrap_p":
                            p_boot,

                        "baseline_high_token_preference_rate":
                            high_preference_before,

                        "steered_high_token_preference_rate":
                            high_preference_after,

                        "high_token_preference_rate_change":
                            (
                                high_preference_after
                                -
                                high_preference_before
                            ),
                    })

                    for i, x in enumerate(
                        rows
                    ):
                        pair_rows.append({
                            "variable_id":
                                vid,

                            "variable":
                                variable,

                            "pair_id":
                                x[
                                    "pair_id"
                                ],

                            "split":
                                split,

                            "dose":
                                dose,

                            "intervention_kind":
                                kind,

                            "target_feature":
                                target_feature,

                            "intervention_feature":
                                feature,

                            "common_prefix_tokens":
                                x[
                                    "common_prefix_tokens"
                                ],

                            "bos_fallback":
                                x[
                                    "bos_fallback"
                                ],

                            "high_token_id":
                                x[
                                    "high_token"
                                ],

                            "low_token_id":
                                x[
                                    "low_token"
                                ],

                            "baseline_logit_margin":
                                float(
                                    baseline_margin[
                                        i
                                    ]
                                ),

                            "steered_logit_margin":
                                float(
                                    steered_margin[
                                        i
                                    ]
                                ),

                            "behavioral_effect":
                                float(
                                    effect[
                                        i
                                    ]
                                ),
                        })

                # --------------------------------------------
                # Target vs control comparison
                # --------------------------------------------

                target_effect = (
                    effects_by_dose[
                        dose
                    ][
                        target_feature
                    ]
                )

                control_effect = np.stack(
                    [
                        effects_by_dose[
                            dose
                        ][
                            f
                        ]
                        for f
                        in controls[
                            vid
                        ]
                    ],
                    axis=0,
                ).mean(
                    axis=0
                )

                difference = (
                    target_effect
                    - control_effect
                )

                (
                    mean_difference,
                    diff_lo,
                    diff_hi,
                    diff_p,
                ) = bootstrap_mean_ci(
                    difference,
                    args.bootstrap,
                    (
                        args.seed
                        + vid * 1000000
                        + int(
                            dose
                            * 1000
                        )
                        + (
                            0
                            if split == "val"
                            else 500000
                        )
                    ),
                )

                result_rows.append({
                    "variable_id":
                        vid,

                    "variable":
                        variable,

                    "primary_mechanistic":
                        vid in primary_ids,

                    "inspection_grade":
                        meta[
                            "inspection_grade"
                        ],

                    "ablation_category":
                        meta[
                            "ablation_category"
                        ],

                    "steering_category":
                        meta[
                            "steering_category"
                        ],

                    "split":
                        split,

                    "dose":
                        dose,

                    "primary_dose":
                        dose == 1.0,

                    "intervention_kind":
                        "target_vs_controls",

                    "target_feature":
                        target_feature,

                    "intervention_feature":
                        -1,

                    "feature_high_side":
                        high_side,

                    "train_target_activation_gap":
                        activation_gap,

                    "steering_coefficient":
                        np.nan,

                    "n_pairs":
                        len(rows),

                    "bos_fallback_pairs":
                        int(
                            sum(
                                x[
                                    "bos_fallback"
                                ]
                                for x in rows
                            )
                        ),

                    "baseline_mean_logit_margin":
                        float(
                            baseline_margin.mean()
                        ),

                    "steered_mean_logit_margin":
                        np.nan,

                    "mean_behavioral_effect":
                        mean_difference,

                    "behavioral_effect_ci_low":
                        diff_lo,

                    "behavioral_effect_ci_high":
                        diff_hi,

                    "behavioral_effect_bootstrap_p":
                        diff_p,

                    "baseline_high_token_preference_rate":
                        float(
                            (
                                baseline_margin
                                > 0
                            ).mean()
                        ),

                    "steered_high_token_preference_rate":
                        np.nan,

                    "high_token_preference_rate_change":
                        np.nan,
                })

    # ========================================================
    # SAVE RAW
    # ========================================================

    results = pd.DataFrame(
        result_rows
    )

    pairs = pd.DataFrame(
        pair_rows
    )

    results_path = (
        outdir
        / "behavioral_branchpoint_results.csv"
    )

    pair_path = (
        outdir
        / "behavioral_branchpoint_pair_level.csv"
    )

    results.to_csv(
        results_path,
        index=False,
    )

    pairs.to_csv(
        pair_path,
        index=False,
    )

    # ========================================================
    # PRIMARY 1x TEST
    # ========================================================

    primary_target = results[
        (
            results[
                "split"
            ]
            == "test"
        )
        &
        (
            results[
                "dose"
            ]
            == 1.0
        )
        &
        (
            results[
                "intervention_kind"
            ]
            == "target"
        )
    ].copy()

    primary_compare = results[
        (
            results[
                "split"
            ]
            == "test"
        )
        &
        (
            results[
                "dose"
            ]
            == 1.0
        )
        &
        (
            results[
                "intervention_kind"
            ]
            == "target_vs_controls"
        )
    ].copy()

    if len(
        primary_target
    ) != 40:
        raise RuntimeError(
            f"Expected 40 target test rows, "
            f"found {len(primary_target)}"
        )

    if len(
        primary_compare
    ) != 40:
        raise RuntimeError(
            f"Expected 40 comparison test rows, "
            f"found {len(primary_compare)}"
        )

    target_keep = primary_target[[
        "variable_id",
        "variable",
        "primary_mechanistic",
        "inspection_grade",
        "ablation_category",
        "steering_category",
        "target_feature",
        "feature_high_side",
        "n_pairs",
        "bos_fallback_pairs",
        "baseline_mean_logit_margin",
        "steered_mean_logit_margin",
        "mean_behavioral_effect",
        "behavioral_effect_ci_low",
        "behavioral_effect_ci_high",
        "behavioral_effect_bootstrap_p",
        "baseline_high_token_preference_rate",
        "steered_high_token_preference_rate",
        "high_token_preference_rate_change",
    ]].rename(columns={
        "mean_behavioral_effect":
            "target_behavioral_effect",

        "behavioral_effect_ci_low":
            "target_behavioral_effect_ci_low",

        "behavioral_effect_ci_high":
            "target_behavioral_effect_ci_high",

        "behavioral_effect_bootstrap_p":
            "target_behavioral_effect_p",
    })

    compare_keep = primary_compare[[
        "variable_id",
        "mean_behavioral_effect",
        "behavioral_effect_ci_low",
        "behavioral_effect_ci_high",
        "behavioral_effect_bootstrap_p",
    ]].rename(columns={
        "mean_behavioral_effect":
            "target_minus_control_behavioral_effect",

        "behavioral_effect_ci_low":
            "target_minus_control_ci_low",

        "behavioral_effect_ci_high":
            "target_minus_control_ci_high",

        "behavioral_effect_bootstrap_p":
            "target_minus_control_p",
    })

    summary = target_keep.merge(
        compare_keep,
        on="variable_id",
        validate="one_to_one",
    )

    # Primary FDR = frozen 15 only.
    primary_mask = (
        summary[
            "primary_mechanistic"
        ].astype(bool)
    )

    summary[
        "primary_cohort_fdr_q"
    ] = np.nan

    summary.loc[
        primary_mask,
        "primary_cohort_fdr_q",
    ] = bh_adjust(
        summary.loc[
            primary_mask,
            "target_minus_control_p",
        ].values
    )

    # Exploratory FDR across all 40.
    summary[
        "all40_exploratory_fdr_q"
    ] = bh_adjust(
        summary[
            "target_minus_control_p"
        ].values
    )

    # --------------------------------------------------------
    # Dose response, target intervention only
    # --------------------------------------------------------

    target_test_all_doses = results[
        (
            results[
                "split"
            ]
            == "test"
        )
        &
        (
            results[
                "intervention_kind"
            ]
            == "target"
        )
    ]

    dose_pivot = target_test_all_doses.pivot(
        index="variable_id",
        columns="dose",
        values="mean_behavioral_effect",
    ).rename(columns={
        0.5:
            "behavior_effect_dose_0_5",

        1.0:
            "behavior_effect_dose_1_0",

        2.0:
            "behavior_effect_dose_2_0",
    }).reset_index()

    summary = summary.merge(
        dose_pivot,
        on="variable_id",
        validate="one_to_one",
    )

    summary[
        "dose_monotonic_non_decreasing"
    ] = (
        (
            summary[
                "behavior_effect_dose_0_5"
            ]
            <=
            summary[
                "behavior_effect_dose_1_0"
            ]
        )
        &
        (
            summary[
                "behavior_effect_dose_1_0"
            ]
            <=
            summary[
                "behavior_effect_dose_2_0"
            ]
        )
    )

    def category(r):
        positive = (
            r[
                "target_behavioral_effect"
            ]
            > 0
        )

        specific = (
            r[
                "target_minus_control_behavioral_effect"
            ]
            > 0
        )

        if r[
            "primary_mechanistic"
        ]:
            significant = (
                specific
                and
                r[
                    "primary_cohort_fdr_q"
                ]
                < 0.05
            )
        else:
            significant = (
                specific
                and
                r[
                    "all40_exploratory_fdr_q"
                ]
                < 0.05
            )

        if positive and significant:
            return "specific_positive"

        if positive and specific:
            return "positive_control_advantage"

        if positive:
            return "positive_nonspecific"

        return "null_or_reverse"

    summary[
        "behavioral_category"
    ] = summary.apply(
        category,
        axis=1,
    )

    summary_path = (
        outdir
        / "behavioral_variable_summary.csv"
    )

    summary.to_csv(
        summary_path,
        index=False,
    )

    manifest = {
        "stage":
            "Step 9 — behavioral branch-point evaluation",

        "model":
            config[
                "model"
            ],

        "primary_cohort_frozen_before_behavior":
            True,

        "primary_variable_count":
            len(
                primary_ids
            ),

        "primary_variable_ids":
            sorted(
                primary_ids
            ),

        "primary_dose":
            1.0,

        "descriptive_doses":
            [
                0.5,
                2.0,
            ],

        "behavioral_outcome": (
            "Change in next-token logit margin between "
            "the feature-high and feature-low linguistic "
            "realizations at the first token divergence."
        ),

        "zero_shared_prefix_handling": (
            "When the two members diverge at token 1, "
            "XGLM BOS is used as the common context."
        ),

        "positive_effect_means": (
            "SAE steering increases model preference "
            "for the feature-high linguistic realization."
        ),

        "controls": (
            "The same three Step-7 training-only matched "
            "SAE features, residual-L2 matched to the "
            "target steering perturbation."
        ),

        "primary_multiple_comparison_family": (
            "Benjamini-Hochberg FDR across the frozen "
            "15-variable primary mechanistic cohort only."
        ),

        "exploratory_multiple_comparison_family": (
            "Separate Benjamini-Hochberg FDR across all "
            "40 variables."
        ),

        "bootstrap_resamples":
            args.bootstrap,

        "seed":
            args.seed,
    }

    manifest_path = (
        outdir
        / "behavioral_manifest.json"
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

    # ========================================================
    # PRINT
    # ========================================================

    primary_summary = summary[
        summary[
            "primary_mechanistic"
        ].astype(bool)
    ]

    print()
    print("=" * 80)

    print(
        "STEP 9 BEHAVIORAL EVALUATION COMPLETE"
    )

    print("=" * 80)

    print()

    print(
        "PRIMARY COHORT:",
        len(
            primary_summary
        ),
    )

    print(
        "Positive behavioral target effect:",
        int(
            (
                primary_summary[
                    "target_behavioral_effect"
                ]
                > 0
            ).sum()
        ),
        "/",
        len(
            primary_summary
        ),
    )

    print(
        "Target > controls:",
        int(
            (
                primary_summary[
                    "target_minus_control_behavioral_effect"
                ]
                > 0
            ).sum()
        ),
        "/",
        len(
            primary_summary
        ),
    )

    print(
        "Positive + primary-FDR-specific:",
        int(
            (
                (
                    primary_summary[
                        "target_behavioral_effect"
                    ]
                    > 0
                )
                &
                (
                    primary_summary[
                        "target_minus_control_behavioral_effect"
                    ]
                    > 0
                )
                &
                (
                    primary_summary[
                        "primary_cohort_fdr_q"
                    ]
                    < 0.05
                )
            ).sum()
        ),
        "/",
        len(
            primary_summary
        ),
    )

    print(
        "Monotonic dose response:",
        int(
            primary_summary[
                "dose_monotonic_non_decreasing"
            ].sum()
        ),
        "/",
        len(
            primary_summary
        ),
    )

    print()

    print(
        "Primary categories:"
    )

    print(
        primary_summary[
            "behavioral_category"
        ].value_counts()
    )

    print()

    cols = [
        "variable_id",
        "variable",
        "target_feature",
        "n_pairs",
        "bos_fallback_pairs",
        "baseline_mean_logit_margin",
        "target_behavioral_effect",
        "target_minus_control_behavioral_effect",
        "primary_cohort_fdr_q",
        "high_token_preference_rate_change",
        "dose_monotonic_non_decreasing",
        "behavioral_category",
    ]

    print(
        primary_summary[
            cols
        ]
        .sort_values(
            "target_minus_control_behavioral_effect",
            ascending=False,
        )
        .to_string(
            index=False
        )
    )

    print()

    print(
        "ALL-40 EXPLORATORY:"
    )

    print(
        summary[
            "behavioral_category"
        ].value_counts()
    )

    print()

    print(
        "Saved:",
        results_path,
    )

    print(
        "Saved:",
        pair_path,
    )

    print(
        "Saved:",
        summary_path,
    )

    print(
        "Saved:",
        manifest_path,
    )


if __name__ == "__main__":
    main()
