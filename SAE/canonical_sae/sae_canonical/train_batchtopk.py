from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch
import torch.nn.functional as F

from batchtopk import BatchTopKSAE

from common import (
    activation_scale_from_manifest,
    append_jsonl,
    exact_steps_per_epoch,
    load_activation_shard,
    load_config,
    load_manifest,
    seed_everything,
    write_json,
)


def lr_multiplier(
    step,
    total_steps,
    warmup,
    decay_fraction,
):
    if warmup > 0 and step < warmup:
        return max(
            1e-8,
            (step + 1) / warmup,
        )

    decay_steps = max(
        1,
        int(
            total_steps
            * decay_fraction
        ),
    )

    decay_start = (
        total_steps
        - decay_steps
    )

    if step < decay_start:
        return 1.0

    progress = (
        step - decay_start
    ) / decay_steps

    progress = min(
        1.0,
        max(0.0, progress),
    )

    return 0.5 * (
        1.0
        + math.cos(
            math.pi
            * progress
        )
    )


@torch.inference_mode()
def evaluate(
    sae,
    cfg,
    manifest,
    split,
    scale,
    device,
):
    root = (
        Path(
            cfg["data"][
                "activation_root"
            ]
        )
        / split
    )

    bs = int(
        cfg["evaluation"][
            "batch_size_tokens"
        ]
    )

    mean = (
        torch.tensor(
            manifest[
                "mean_activation"
            ],
            dtype=torch.float64,
        )
        * scale
    )

    total = 0
    sse = 0.0
    centered_ss = 0.0
    cosine_sum = 0.0
    l0_sum = 0.0

    counts = torch.zeros(
        sae.d_sae,
        dtype=torch.int64,
    )

    cutoffs = []

    for shard in manifest["shards"]:
        x_cpu = load_activation_shard(
            root / shard["file"]
        )

        for start in range(
            0,
            x_cpu.shape[0],
            bs,
        ):
            x = x_cpu[
                start:start + bs
            ].to(
                device,
                dtype=torch.float32,
            )

            x = x * scale

            recon, acts, _, cutoff = sae(x)

            err = x - recon

            n = x.shape[0]
            total += n

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

            active = acts > 0

            counts += (
                active.sum(dim=0)
                .cpu()
            )

            l0_sum += active.sum().item()

            cutoffs.append(
                float(cutoff.item())
            )

    freq = (
        counts.float()
        / total
    )

    return {
        "tokens": total,
        "mse":
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
            cosine_sum / total,
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
            float(freq.mean()),
        "frequency_median":
            float(freq.median()),
        "batch_cutoff_mean":
            sum(cutoffs)
            / len(cutoffs),
        "batch_cutoff_min":
            min(cutoffs),
        "batch_cutoff_max":
            max(cutoffs),
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        required=True,
    )

    args = parser.parse_args()

    cfg = load_config(
        args.config
    )

    seed_everything(
        int(cfg["seed"])
    )

    device = torch.device("cuda")

    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    dc = cfg["data"]
    sc = cfg["sae"]
    tc = cfg["training"]

    train_manifest = load_manifest(
        dc["activation_root"],
        "train",
    )

    val_manifest = load_manifest(
        dc["activation_root"],
        "val",
    )

    d_in = int(
        cfg["model"]["d_in"]
    )

    d_sae = int(
        sc["d_sae"]
    )

    k = int(
        sc["k"]
    )

    batch_size = int(
        tc["batch_size_tokens"]
    )

    epochs = int(
        tc["epochs"]
    )

    dead_window = int(
        tc["dead_feature_window"]
    )

    scale = (
        activation_scale_from_manifest(
            train_manifest,
            d_in,
        )
    )

    mean_act = (
        torch.tensor(
            train_manifest[
                "mean_activation"
            ],
            dtype=torch.float32,
        )
        * scale
    )

    sae = BatchTopKSAE(
        d_in=d_in,
        d_sae=d_sae,
        k=k,
        b_dec_init=mean_act,
        apply_decoder_bias_to_input=bool(
            sc[
                "apply_decoder_bias_to_input"
            ]
        ),
    ).to(
        device,
        dtype=torch.float32,
    )

    base_lr = float(
        tc["learning_rate"]
    )

    optimizer = torch.optim.Adam(
        sae.parameters(),
        lr=base_lr,
        betas=(
            float(
                tc["adam_beta1"]
            ),
            float(
                tc["adam_beta2"]
            ),
        ),
        weight_decay=float(
            tc.get(
                "weight_decay",
                0.0,
            )
        ),
    )

    steps_per_epoch = (
        exact_steps_per_epoch(
            train_manifest,
            batch_size,
        )
    )

    total_steps = (
        steps_per_epoch
        * epochs
    )

    run_dir = Path(
        tc["run_dir"]
    )

    run_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics_path = (
        run_dir
        / "metrics.jsonl"
    )

    if metrics_path.exists():
        metrics_path.unlink()

    steps_since_fired = torch.zeros(
        d_sae,
        dtype=torch.int64,
        device=device,
    )

    train_root = (
        Path(
            dc["activation_root"]
        )
        / "train"
    )

    write_json(
        run_dir / "run_info.json",
        {
            "architecture":
                "BatchTopK",
            "d_in":
                d_in,
            "d_sae":
                d_sae,
            "k":
                k,
            "aux_k":
                sc["aux_k"],
            "aux_penalty":
                sc["aux_penalty"],
            "dead_feature_window":
                dead_window,
            "epochs":
                epochs,
            "unique_train_tokens":
                train_manifest[
                    "tokens"
                ],
            "planned_token_presentations":
                train_manifest[
                    "tokens"
                ]
                * epochs,
            "steps_per_epoch":
                steps_per_epoch,
            "total_steps":
                total_steps,
            "activation_scale":
                scale,
            "config":
                cfg,
        },
    )

    print()
    print("BATCHTOPK PILOT")
    print("================")
    print(
        "Dictionary:",
        f"{d_in} -> {d_sae}",
    )
    print("k:", k)
    print(
        "AuxK:",
        sc["aux_k"],
    )
    print(
        "Aux penalty:",
        sc["aux_penalty"],
    )
    print(
        "Dead window:",
        dead_window,
    )
    print(
        "Total steps:",
        total_steps,
    )

    global_step = 0
    tokens_seen = 0

    for epoch in range(epochs):

        g = torch.Generator().manual_seed(
            int(cfg["seed"])
            + 10000 * epoch
        )

        shard_order = torch.randperm(
            len(
                train_manifest[
                    "shards"
                ]
            ),
            generator=g,
        ).tolist()

        for shard_idx in shard_order:

            shard = (
                train_manifest[
                    "shards"
                ][shard_idx]
            )

            x_cpu = load_activation_shard(
                train_root
                / shard["file"]
            )

            g_rows = (
                torch.Generator()
                .manual_seed(
                    int(cfg["seed"])
                    + epoch * 1_000_000
                    + shard_idx
                )
            )

            perm = torch.randperm(
                x_cpu.shape[0],
                generator=g_rows,
            )

            x_cpu = x_cpu[perm]

            for start in range(
                0,
                x_cpu.shape[0],
                batch_size,
            ):
                x = x_cpu[
                    start:
                    start + batch_size
                ].to(
                    device,
                    dtype=torch.float32,
                    non_blocking=True,
                )

                x = x * scale

                dead_mask = (
                    steps_since_fired
                    > dead_window
                )

                optimizer.zero_grad(
                    set_to_none=True
                )

                (
                    recon,
                    acts,
                    raw,
                    cutoff,
                ) = sae(x)

                recon_loss = (
                    (x - recon)
                    .pow(2)
                    .sum(dim=-1)
                    .mean()
                )

                aux_loss = sae.auxiliary_loss(
                    x=x,
                    recon=recon,
                    raw=raw,
                    dead_mask=dead_mask,
                    aux_k=int(
                        sc["aux_k"]
                    ),
                    aux_penalty=float(
                        sc["aux_penalty"]
                    ),
                )

                loss = (
                    recon_loss
                    + aux_loss
                )

                loss.backward()

                sae.remove_decoder_grad_parallel_()

                torch.nn.utils.clip_grad_norm_(
                    sae.parameters(),
                    float(
                        tc[
                            "grad_clip_norm"
                        ]
                    ),
                )

                lr_mult = lr_multiplier(
                    global_step,
                    total_steps,
                    int(
                        tc[
                            "lr_warmup_steps"
                        ]
                    ),
                    float(
                        tc[
                            "lr_decay_fraction"
                        ]
                    ),
                )

                for pg in optimizer.param_groups:
                    pg["lr"] = (
                        base_lr
                        * lr_mult
                    )

                optimizer.step()

                sae.normalize_decoder_()

                with torch.no_grad():
                    did_fire = (
                        (acts > 0)
                        .any(dim=0)
                    )

                    steps_since_fired += 1

                    steps_since_fired[
                        did_fire
                    ] = 0

                    train_l0 = (
                        (acts > 0)
                        .sum(dim=-1)
                        .float()
                        .mean()
                        .item()
                    )

                global_step += 1
                tokens_seen += x.shape[0]

                if (
                    global_step
                    % int(
                        tc[
                            "log_every_steps"
                        ]
                    )
                    == 0
                    or global_step == 1
                ):
                    dead_now = (
                        steps_since_fired
                        > dead_window
                    )

                    metric = {
                        "step":
                            global_step,
                        "epoch":
                            epoch,
                        "tokens_seen":
                            tokens_seen,
                        "loss":
                            float(
                                loss.item()
                            ),
                        "reconstruction_loss":
                            float(
                                recon_loss.item()
                            ),
                        "aux_loss":
                            float(
                                aux_loss.item()
                            ),
                        "train_l0":
                            train_l0,
                        "train_dead_features":
                            int(
                                dead_now
                                .sum()
                                .item()
                            ),
                        "train_dead_fraction":
                            float(
                                dead_now
                                .float()
                                .mean()
                                .item()
                            ),
                        "batch_cutoff":
                            float(
                                cutoff.item()
                            ),
                        "lr":
                            optimizer
                            .param_groups[0][
                                "lr"
                            ],
                    }

                    append_jsonl(
                        metrics_path,
                        metric,
                    )

                    print(
                        f"step "
                        f"{global_step:4d}"
                        f"/{total_steps} | "
                        f"recon "
                        f"{metric['reconstruction_loss']:.3f} | "
                        f"aux "
                        f"{metric['aux_loss']:.3f} | "
                        f"L0 "
                        f"{train_l0:.1f} | "
                        f"dead "
                        f"{metric['train_dead_fraction']:.3f}"
                    )

                if (
                    global_step
                    % int(
                        tc[
                            "validate_every_steps"
                        ]
                    )
                    == 0
                ):
                    val = evaluate(
                        sae,
                        cfg,
                        val_manifest,
                        "val",
                        scale,
                        device,
                    )

                    dead_now = (
                        steps_since_fired
                        > dead_window
                    )

                    metric = {
                        "kind":
                            "validation",
                        "step":
                            global_step,
                        "val_explained_variance":
                            val[
                                "explained_variance"
                            ],
                        "val_mse":
                            val["mse"],
                        "val_cosine_similarity":
                            val[
                                "cosine_similarity"
                            ],
                        "val_l0":
                            val[
                                "mean_l0"
                            ],
                        "val_zero_fire_fraction":
                            val[
                                "zero_fire_fraction"
                            ],
                        "train_dead_fraction":
                            float(
                                dead_now
                                .float()
                                .mean()
                                .item()
                            ),
                        "batch_cutoff_mean":
                            val[
                                "batch_cutoff_mean"
                            ],
                    }

                    append_jsonl(
                        metrics_path,
                        metric,
                    )

                    print(
                        "VAL | "
                        f"EV "
                        f"{metric['val_explained_variance']:.4f} | "
                        f"L0 "
                        f"{metric['val_l0']:.1f} | "
                        f"zero "
                        f"{metric['val_zero_fire_fraction']:.3f} | "
                        f"dead "
                        f"{metric['train_dead_fraction']:.3f}"
                    )

    val = evaluate(
        sae,
        cfg,
        val_manifest,
        "val",
        scale,
        device,
    )

    torch.save(
        {
            "model_state":
                sae.state_dict(),
            "activation_scale":
                scale,
            "steps_since_fired":
                steps_since_fired.cpu(),
            "config":
                cfg,
        },
        run_dir
        / "sae_final.pt",
    )

    final = {
        "kind":
            "final_validation",
        "step":
            global_step,
        **{
            "val_" + key:
                value
            for key, value
            in val.items()
        },
        "train_dead_features":
            int(
                (
                    steps_since_fired
                    > dead_window
                )
                .sum()
                .item()
            ),
        "train_dead_fraction":
            float(
                (
                    steps_since_fired
                    > dead_window
                )
                .float()
                .mean()
                .item()
            ),
    }

    write_json(
        run_dir
        / "final_metrics.json",
        final,
    )

    append_jsonl(
        metrics_path,
        final,
    )

    print()
    print("TRAINING COMPLETE")
    print("=================")
    print(
        json.dumps(
            final,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
