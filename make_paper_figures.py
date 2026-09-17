#!/usr/bin/env python3
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

mpl.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 400,
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def find_repo_root(start: Path) -> Path:
    for path in [start] + list(start.parents):
        if (path / "SAE").exists() and (path / "causal_steps").exists():
            return path
    raise FileNotFoundError("Run this script from inside the repository.")


def load_csv(root: Path, rel: str) -> pd.DataFrame:
    path = root / rel
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def main() -> None:
    root = find_repo_root(Path.cwd())
    out_dir = root / "paper_figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    abl = load_csv(
        root,
        "causal_steps/causal_interventions/ablation_screen/ablation_variable_summary.csv",
    )
    steer = load_csv(
        root,
        "causal_steps/causal_interventions/steering_screen/steering_variable_summary.csv",
    )
    pre = load_csv(
        root,
        "causal_steps/causal_interventions/mechanistic_convergence/PREBEHAVIOR_PRIMARY_COHORT.csv",
    )
    final = load_csv(
        root,
        "causal_steps/causal_interventions/final_summary/FULL_CHAIN_PRIMARY_RESULTS.csv",
    )

    steer = steer[steer["primary_dose"] == True].copy()

    df = (
        abl[["variable_id", "variable", "target_minus_control_attenuation", "causal_screen_category"]]
        .rename(columns={
            "target_minus_control_attenuation": "ablation_effect",
            "causal_screen_category": "ablation_category",
        })
        .merge(
            steer[["variable_id", "target_minus_control_attenuation", "steering_screen_category"]]
            .rename(columns={
                "target_minus_control_attenuation": "steering_effect",
                "steering_screen_category": "steering_category",
            }),
            on="variable_id",
            how="left",
        )
    )

    primary_ids = set(pre["variable_id"].astype(int))
    final_ids = set(final["variable_id"].astype(int))
    df["is_primary"] = df["variable_id"].isin(primary_ids)
    df["is_final"] = df["variable_id"].isin(final_ids)

    counts = {
        "Ranked candidates": len(df),
        "Ablation-specific": int((abl["causal_screen_category"] == "specific_positive").sum()),
        "Steering-specific": int((steer["steering_screen_category"] == "specific_positive").sum()),
        "Primary mechanistic": len(pre),
        "Full-chain primary": len(final),
    }

    fig = plt.figure(figsize=(12.4, 5.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.15, 1.05], wspace=0.32)

    # ------------------------------------------------------------------
    # (a) Ablation vs steering
    # ------------------------------------------------------------------
    ax = fig.add_subplot(gs[0, 0])

    other = df[~df["is_primary"]]
    primary = df[df["is_primary"] & ~df["is_final"]]
    full = df[df["is_final"]]

    ax.scatter(
        other["ablation_effect"], other["steering_effect"],
        s=34, color="#C8C8C8", edgecolor="white", linewidth=0.7,
        label="Other variables", zorder=2,
    )
    ax.scatter(
        primary["ablation_effect"], primary["steering_effect"],
        s=56, color="#4C78A8", edgecolor="white", linewidth=0.8,
        label="Primary mechanistic cohort", zorder=3,
    )
    ax.scatter(
        full["ablation_effect"], full["steering_effect"],
        s=120, color="#D62728", marker="*", edgecolor="white", linewidth=0.8,
        label="Full-chain primary", zorder=4,
    )

    # Label only the final six and two important high-effect mechanistic cases.
    label_ids = final_ids | {6, 16}
    offsets = {
        6: (5, 4), 10: (5, -10), 16: (5, 0), 17: (5, 0),
        19: (5, -10), 21: (5, 0), 23: (5, 5), 27: (5, 5),
    }
    for _, row in df[df["variable_id"].isin(label_ids)].iterrows():
        dx, dy = offsets.get(int(row["variable_id"]), (5, 4))
        ax.annotate(
            f"{int(row['variable_id']):02d}",
            (row["ablation_effect"], row["steering_effect"]),
            xytext=(dx, dy), textcoords="offset points",
            fontsize=8, ha="left", va="center",
        )

    ax.axhline(0, color="#777777", lw=0.9, ls="--", zorder=1)
    ax.axvline(0, color="#777777", lw=0.9, ls="--", zorder=1)
    ax.set_xlabel("Ablation target-minus-control effect")
    ax.set_ylabel("Steering target-minus-control effect")
    ax.set_title("(a) Matched ablation and steering effects", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper left")

    # ------------------------------------------------------------------
    # (b) Evidence funnel as horizontal bars to avoid label overlap
    # ------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])

    labels = list(counts.keys())
    values = list(counts.values())
    colors = ["#D9D9D9", "#9ECAE1", "#A1D99B", "#FDAE6B", "#FB6A4A"]

    y = list(range(len(labels)))
    bars = ax2.barh(y, values, color=colors, edgecolor="#333333", linewidth=0.6)
    ax2.set_yticks(y)
    ax2.set_yticklabels(labels)
    ax2.invert_yaxis()
    ax2.set_xlabel("Variables")
    ax2.set_xlim(0, max(values) * 1.18)
    ax2.set_title("(b) Progression through causal criteria", loc="left", fontweight="bold")

    for bar, value in zip(bars, values):
        ax2.text(
            bar.get_width() + 0.7,
            bar.get_y() + bar.get_height() / 2,
            str(value),
            va="center", ha="left", fontsize=10, fontweight="bold",
        )

    fig.subplots_adjust(left=0.08, right=0.985, top=0.93, bottom=0.14)

    out = out_dir / "causal.png"
    fig.savefig(out, bbox_inches="tight", dpi=400)
    plt.close(fig)

    print(f"Saved only: {out}")


if __name__ == "__main__":
    main()
