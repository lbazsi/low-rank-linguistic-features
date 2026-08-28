from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from safetensors.torch import save_file

from batchtopk import BatchTopKSAE
from common import (
    load_activation_shard,
    load_config,
    load_manifest,
)


@torch.inference_mode()
def calibrate_threshold(
    sae,
    root,
    manifest,
    scale,
    batch_size,
    ema_lr=0.01,
):
    """
    Mirror SAE Lens BatchTopK export logic:
    update a global threshold as an EMA of the
    minimum positive BatchTopK activation.
    """

    threshold = torch.tensor(
        0.0,
        dtype=torch.float64,
        device="cuda",
    )

    cutoffs = []
    n_batches = 0

    for shard in manifest["shards"]:
        x_cpu = load_activation_shard(
            root / shard["file"]
        )

        for start in range(
            0,
            x_cpu.shape[0],
            batch_size,
        ):
            x = x_cpu[
                start:start + batch_size
            ].to(
                "cuda",
                dtype=torch.float32,
            )

            x = x * scale

            raw = sae.raw_activations(x)

            flat = raw.flatten()

            n_samples = raw.shape[0]

            n_keep = min(
                sae.k * n_samples,
                flat.numel(),
            )

            values = torch.topk(
                flat,
                n_keep,
                sorted=False,
            ).values

            positive = values[
                values > 0
            ]

            if positive.numel() == 0:
                continue

            cutoff = (
                positive.min()
                .double()
            )

            threshold = (
                (1.0 - ema_lr)
                * threshold
                + ema_lr
                * cutoff
            )

            cutoffs.append(
                float(cutoff.item())
            )

            n_batches += 1

    return {
        "threshold":
            float(threshold.item()),
        "batches":
            n_batches,
        "cutoff_mean":
            sum(cutoffs)
            / len(cutoffs),
        "cutoff_min":
            min(cutoffs),
        "cutoff_max":
            max(cutoffs),
        "ema_lr":
            ema_lr,
    }


@torch.inference_mode()
def evaluate_threshold(
    sae,
    root,
    manifest,
    scale,
    batch_size,
    threshold,
    reconstruction=True,
):
    counts = torch.zeros(
        sae.d_sae,
        dtype=torch.int64,
    )

    total = 0
    l0_sum = 0

    sse = 0.0
    centered_ss = 0.0
    cosine_sum = 0.0

    mean = (
        torch.tensor(
            manifest["mean_activation"],
            dtype=torch.float64,
        )
        * scale
    )

    threshold_t = torch.tensor(
        threshold,
        dtype=torch.float32,
        device="cuda",
    )

    for shard in manifest["shards"]:
        x_cpu = load_activation_shard(
            root / shard["file"]
        )

        for start in range(
            0,
            x_cpu.shape[0],
            batch_size,
        ):
            x = x_cpu[
                start:start + batch_size
            ].to(
                "cuda",
                dtype=torch.float32,
            )

            x = x * scale

            raw = sae.raw_activations(x)

            acts = (
                raw
                * (
                    raw > threshold_t
                )
            )

            active = acts > 0

            counts += (
                active.sum(dim=0)
                .cpu()
            )

            n = x.shape[0]

            total += n

            l0_sum += int(
                active.sum().item()
            )

            if reconstruction:
                recon = sae.decode(acts)

                err = x - recon

                sse += (
                    err.pow(2)
                    .sum()
                    .item()
                )

                centered_ss += (
                    (
                        x.double().cpu()
                        - mean
                    )
                    .pow(2)
                    .sum()
                    .item()
                )

                cosine_sum += (
                    F.cosine_similarity(
                        x,
                        recon,
                        dim=-1,
                    )
                    .sum()
                    .item()
                )

    freq = (
        counts.float()
        / total
    )

    result = {
        "tokens":
            total,
        "mean_l0":
            l0_sum / total,
        "active_fraction":
            l0_sum
            / (
                total
                * sae.d_sae
            ),
        "zero_fire_features":
            int(
                (counts == 0)
                .sum()
                .item()
            ),
        "zero_fire_fraction":
            float(
                (counts == 0)
                .float()
                .mean()
                .item()
            ),
        "frequency_mean":
            float(
                freq.mean()
                .item()
            ),
        "frequency_median":
            float(
                freq.median()
                .item()
            ),
    }

    if reconstruction:
        result.update(
            {
                "mse_per_dimension":
                    sse
                    / (
                        total
                        * sae.d_in
                    ),
                "explained_variance":
                    1.0
                    - sse
                    / centered_ss,
                "cosine_similarity":
                    cosine_sum
                    / total,
            }
        )

    return result, counts


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        required=True,
    )

    parser.add_argument(
        "--ema-lr",
        type=float,
        default=0.01,
    )

    args = parser.parse_args()

    cfg = load_config(
        args.config
    )

    run = Path(
        cfg["training"]["run_dir"]
    )

    ckpt = torch.load(
        run / "sae_final.pt",
        map_location="cpu",
    )

    d_in = int(
        cfg["model"]["d_in"]
    )

    d_sae = int(
        cfg["sae"]["d_sae"]
    )

    k = int(
        cfg["sae"]["k"]
    )

    scale = float(
        ckpt["activation_scale"]
    )

    sae = BatchTopKSAE(
        d_in=d_in,
        d_sae=d_sae,
        k=k,
        b_dec_init=torch.zeros(
            d_in,
        ),
        apply_decoder_bias_to_input=bool(
            cfg["sae"][
                "apply_decoder_bias_to_input"
            ]
        ),
    )

    sae.load_state_dict(
        ckpt["model_state"]
    )

    sae = sae.to(
        "cuda",
        dtype=torch.float32,
    ).eval()

    activation_root = Path(
        cfg["data"][
            "activation_root"
        ]
    )

    train_manifest = load_manifest(
        cfg["data"][
            "activation_root"
        ],
        "train",
    )

    val_manifest = load_manifest(
        cfg["data"][
            "activation_root"
        ],
        "val",
    )

    bs = int(
        cfg["evaluation"][
            "batch_size_tokens"
        ]
    )

    print(
        "Calibrating global threshold "
        "on TRAINING corpus..."
    )

    calibration = calibrate_threshold(
        sae=sae,
        root=activation_root / "train",
        manifest=train_manifest,
        scale=scale,
        batch_size=bs,
        ema_lr=args.ema_lr,
    )

    threshold = calibration[
        "threshold"
    ]

    print()
    print(
        "Threshold:",
        threshold,
    )

    print()
    print(
        "Evaluating JumpReLU inference "
        "on TRAIN..."
    )

    train_eval, train_counts = (
        evaluate_threshold(
            sae=sae,
            root=activation_root / "train",
            manifest=train_manifest,
            scale=scale,
            batch_size=bs,
            threshold=threshold,
            reconstruction=True,
        )
    )

    print(
        "Evaluating JumpReLU inference "
        "on VAL..."
    )

    val_eval, val_counts = (
        evaluate_threshold(
            sae=sae,
            root=activation_root / "val",
            manifest=val_manifest,
            scale=scale,
            batch_size=bs,
            threshold=threshold,
            reconstruction=True,
        )
    )

    corpus_counts = (
        train_counts
        + val_counts
    )

    corpus_tokens = (
        train_eval["tokens"]
        + val_eval["tokens"]
    )

    corpus_freq = (
        corpus_counts.float()
        / corpus_tokens
    )

    corpus_eval = {
        "tokens":
            corpus_tokens,
        "zero_fire_features":
            int(
                (
                    corpus_counts == 0
                )
                .sum()
                .item()
            ),
        "zero_fire_fraction":
            float(
                (
                    corpus_counts == 0
                )
                .float()
                .mean()
                .item()
            ),
        "active_features":
            int(
                (
                    corpus_counts > 0
                )
                .sum()
                .item()
            ),
        "frequency_gt_1e-5":
            int(
                (
                    corpus_freq > 1e-5
                )
                .sum()
                .item()
            ),
        "frequency_gt_1e-4":
            int(
                (
                    corpus_freq > 1e-4
                )
                .sum()
                .item()
            ),
        "frequency_gt_1e-3":
            int(
                (
                    corpus_freq > 1e-3
                )
                .sum()
                .item()
            ),
    }

    result = {
        "source_checkpoint":
            str(
                run
                / "sae_final.pt"
            ),
        "architecture_training":
            "BatchTopK",
        "architecture_inference":
            "JumpReLU",
        "k_training":
            k,
        "calibration":
            calibration,
        "train":
            train_eval,
        "validation":
            val_eval,
        "full_unique_corpus":
            corpus_eval,
    }

    with open(
        run
        / "inference_evaluation.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
        )

    # Inference-only weights.
    weights = {
        "W_enc":
            sae.W_enc
            .detach()
            .cpu()
            .contiguous(),
        "W_dec":
            sae.W_dec
            .detach()
            .cpu()
            .contiguous(),
        "b_enc":
            sae.b_enc
            .detach()
            .cpu()
            .contiguous(),
        "b_dec":
            sae.b_dec
            .detach()
            .cpu()
            .contiguous(),
        "threshold":
            torch.full(
                (d_sae,),
                threshold,
                dtype=torch.float32,
            ),
    }

    save_file(
        weights,
        run
        / "sae_inference.safetensors",
    )

    inference_cfg = {
        "architecture":
            "JumpReLU",
        "trained_as":
            "BatchTopK",
        "model":
            cfg["model"]["name"],
        "hidden_state_index":
            cfg["model"][
                "hidden_state_index"
            ],
        "d_in":
            d_in,
        "d_sae":
            d_sae,
        "training_k":
            k,
        "threshold":
            threshold,
        "activation_scale":
            scale,
        "apply_decoder_bias_to_input":
            bool(
                cfg["sae"][
                    "apply_decoder_bias_to_input"
                ]
            ),
        "source_config":
            args.config,
        "source_checkpoint":
            str(
                run
                / "sae_final.pt"
            ),
    }

    with open(
        run
        / "sae_inference_config.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            inference_cfg,
            f,
            indent=2,
        )

    torch.save(
        {
            "train_activation_counts":
                train_counts,
            "val_activation_counts":
                val_counts,
            "corpus_activation_counts":
                corpus_counts,
            "corpus_activation_frequency":
                corpus_freq,
        },
        run
        / "inference_feature_stats.pt",
    )

    print()
    print(
        "INFERENCE EXPORT COMPLETE"
    )
    print(
        "========================="
    )

    print(
        json.dumps(
            result,
            indent=2,
        )
    )

    print()
    print(
        "Saved:",
        run
        / "sae_inference.safetensors",
    )
    print(
        "Saved:",
        run
        / "sae_inference_config.json",
    )


if __name__ == "__main__":
    main()
