from __future__ import annotations

import json
from pathlib import Path

import torch

from batchtopk import BatchTopKSAE
from common import (
    load_activation_shard,
    load_config,
    load_manifest,
)


RUNS = {
    "4epoch": {
        "config": (
            "configs/"
            "xglm564m_batchtopk_16x_k256_pilot4.yaml"
        ),
        "run": (
            "artifacts/sae_runs/"
            "xglm564m_hidden12_batchtopk16x_k256_pilot4"
        ),
    },
    "8epoch": {
        "config": (
            "configs/"
            "xglm564m_batchtopk_16x_k256_final.yaml"
        ),
        "run": (
            "artifacts/sae_runs/"
            "xglm564m_hidden12_batchtopk16x_k256_final"
        ),
    },
}


@torch.inference_mode()
def evaluate_run(name, info):
    cfg = load_config(info["config"])

    run = Path(info["run"])

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
        b_dec_init=torch.zeros(d_in),
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

    root = Path(
        cfg["data"]["activation_root"]
    )

    bs = int(
        cfg["evaluation"][
            "batch_size_tokens"
        ]
    )

    total_counts = torch.zeros(
        d_sae,
        dtype=torch.int64,
    )

    total_tokens = 0
    l0_sum = 0

    split_results = {}

    for split in ("train", "val"):
        manifest = load_manifest(
            cfg["data"]["activation_root"],
            split,
        )

        counts = torch.zeros(
            d_sae,
            dtype=torch.int64,
        )

        tokens = 0
        split_l0 = 0

        for shard in manifest["shards"]:
            x_cpu = load_activation_shard(
                root
                / split
                / shard["file"]
            )

            for start in range(
                0,
                x_cpu.shape[0],
                bs,
            ):
                x = x_cpu[
                    start:start + bs
                ].to(
                    "cuda",
                    dtype=torch.float32,
                )

                x = x * scale

                acts, _, _ = sae.encode(x)

                active = acts > 0

                counts += (
                    active
                    .sum(dim=0)
                    .cpu()
                )

                n = x.shape[0]

                tokens += n

                split_l0 += int(
                    active.sum().item()
                )

        total_counts += counts
        total_tokens += tokens
        l0_sum += split_l0

        freq = (
            counts.float()
            / tokens
        )

        split_results[split] = {
            "tokens":
                tokens,
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
            "mean_l0":
                split_l0 / tokens,
            "median_frequency":
                float(
                    freq.median()
                    .item()
                ),
        }

    corpus_freq = (
        total_counts.float()
        / total_tokens
    )

    result = {
        "run":
            name,
        "tokens":
            total_tokens,
        "mean_l0":
            l0_sum
            / total_tokens,
        "zero_fire_features":
            int(
                (total_counts == 0)
                .sum()
                .item()
            ),
        "zero_fire_fraction":
            float(
                (total_counts == 0)
                .float()
                .mean()
                .item()
            ),
        "active_features":
            int(
                (total_counts > 0)
                .sum()
                .item()
            ),
        "frequency_gt_1e-6":
            int(
                (corpus_freq > 1e-6)
                .sum()
                .item()
            ),
        "frequency_gt_1e-5":
            int(
                (corpus_freq > 1e-5)
                .sum()
                .item()
            ),
        "frequency_gt_1e-4":
            int(
                (corpus_freq > 1e-4)
                .sum()
                .item()
            ),
        "frequency_gt_1e-3":
            int(
                (corpus_freq > 1e-3)
                .sum()
                .item()
            ),
        "train":
            split_results["train"],
        "val":
            split_results["val"],
    }

    torch.save(
        {
            "activation_counts":
                total_counts,
            "activation_frequency":
                corpus_freq,
        },
        run
        / "corpus_feature_frequency.pt",
    )

    with open(
        run
        / "corpus_feature_frequency.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
        )

    return result


results = {}

for name, info in RUNS.items():
    print()
    print(
        f"Evaluating {name} over "
        f"the full unique corpus..."
    )

    results[name] = evaluate_run(
        name,
        info,
    )


print()
print("FULL CORPUS COMPARISON")
print("======================")
print(
    "run\tL0\tzero-fire\t"
    "active\t>1e-5\t>1e-4\t>1e-3"
)

for name, r in results.items():
    print(
        f"{name}\t"
        f"{r['mean_l0']:.1f}\t"
        f"{r['zero_fire_fraction']:.4f}\t"
        f"{r['active_features']}\t"
        f"{r['frequency_gt_1e-5']}\t"
        f"{r['frequency_gt_1e-4']}\t"
        f"{r['frequency_gt_1e-3']}"
    )

print()
print("VALIDATION RECONSTRUCTION")

for name, info in RUNS.items():
    final = json.loads(
        (
            Path(info["run"])
            / "final_metrics.json"
        ).read_text()
    )

    print(
        name,
        "| EV =",
        round(
            final[
                "val_explained_variance"
            ],
            6,
        ),
        "| MSE =",
        round(
            final["val_mse"],
            6,
        ),
        "| trainer dead =",
        round(
            final[
                "train_dead_fraction"
            ],
            5,
        ),
    )
