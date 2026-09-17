#!/usr/bin/env python3
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch, Rectangle
import numpy as np
import pandas as pd

mpl.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
})


def find_repo_root(start: Path) -> Path:
    for path in [start] + list(start.parents):
        if (path / "SAE").exists() and (path / "causal_steps").exists():
            return path
    raise FileNotFoundError(
        "Could not find repository root. Run this script from inside the repo, "
        "or place it in the repo root next to README.md."
    )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    pdf_path = output_dir / f"{stem}.pdf"
    png_path = output_dir / f"{stem}.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", dpi=400)
    print(f"Saved: {pdf_path}")
    print(f"Saved: {png_path}")


def wrap_label(text: str, width: int = 28) -> str:
    text = str(text).replace("_", " ")
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def short_var_label(variable_id: int, variable: str, width: int = 28) -> str:
    return f"{int(variable_id):02d}  {wrap_label(variable, width=width)}"


def load_csv(root: Path, relative_path: str) -> pd.DataFrame:
    path = root / relative_path
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def plot_pipeline(output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(14, 6.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    c_data = "#DCEAF7"
    c_model = "#E6F4E8"
    c_sparse = "#F3E4F7"
    c_causal = "#FCE8D6"
    c_behavior = "#FDE2E4"
    edge = "#2F2F2F"

    def box(x, y, w, h, title, body, fc):
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            linewidth=1.1,
            edgecolor=edge,
            facecolor=fc,
        )
        ax.add_patch(patch)
        ax.text(x + 0.02 * w, y + h - 0.08 * h, title,
                ha="left", va="top", fontsize=11, fontweight="bold")
        ax.text(x + 0.02 * w, y + h - 0.24 * h, body,
                ha="left", va="top", fontsize=9, linespacing=1.25)

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", mutation_scale=12,
            linewidth=1.2, color=edge,
            connectionstyle="arc3,rad=0.0",
        ))

    box(0.03, 0.62, 0.20, 0.26,
        "1. Controlled feature construction",
        "40 linguistic variables\n20,000 contrast pairs\nHeld-out marker families\nHeld-out lexical domains",
        c_data)
    box(0.28, 0.62, 0.18, 0.26,
        "2. Activation collection",
        "XGLM-564M forward passes\nLayerwise residual activations\nMean-pooled + final-token views",
        c_model)
    box(0.51, 0.62, 0.18, 0.26,
        "3. Supervised probes",
        "Recoverability across layers\nSeed robustness checks\nActivation vs text controls",
        c_model)
    box(0.74, 0.62, 0.23, 0.26,
        "4. Sparse autoencoder",
        "BatchTopK SAE on natural text\n16× expansion, k = 256\nExported fixed-threshold inference model",
        c_sparse)
    box(0.08, 0.18, 0.19, 0.26,
        "5. Feature ranking",
        "Train/val/test effects\nNull-corrected candidate ranking\nCross-variable specificity",
        c_sparse)
    box(0.32, 0.18, 0.19, 0.26,
        "6. Feature inspection",
        "Natural-text top activations\nSemantic review\nInterpretation grades A–D",
        c_sparse)
    box(0.56, 0.18, 0.18, 0.26,
        "7–8. Causal interventions",
        "Matched ablation\nMatched steering\nDose-response checks\nMechanistic convergence",
        c_causal)
    box(0.79, 0.18, 0.16, 0.26,
        "9. Behavioral evaluation",
        "Branch-point next-token tests\nTarget vs matched controls\nFrozen primary cohort",
        c_behavior)

    arrow(0.23, 0.75, 0.28, 0.75)
    arrow(0.46, 0.75, 0.51, 0.75)
    arrow(0.69, 0.75, 0.74, 0.75)
    arrow(0.86, 0.62, 0.20, 0.46)
    arrow(0.27, 0.31, 0.32, 0.31)
    arrow(0.51, 0.31, 0.56, 0.31)
    arrow(0.74, 0.31, 0.79, 0.31)

    ax.text(
        0.5, 0.97,
        "Pipeline from representational recoverability to causal and behavioral evaluation",
        ha="center", va="top", fontsize=13, fontweight="bold"
    )

    save_figure(fig, output_dir, "pipeline")
    plt.close(fig)


def plot_evidence(root: Path, output_dir: Path) -> None:
    probe = load_csv(root, "SAE/post_canonical/post_canonical/evidence/probe/probe_sae_comparison.csv")
    sae = load_csv(root, "SAE/post_canonical/post_canonical/evidence/sae/sae_variable_evidence.csv")
    inspect_df = load_csv(root, "SAE/feature_inspection/all_variables/causal_candidate_ranking.csv")

    df = (
        probe[["variable_id", "variable", "probe_core_status"]]
        .merge(sae[["variable_id", "evidence_tier"]], on="variable_id", how="left")
        .merge(inspect_df[["variable_id", "inspection_grade", "feature_id", "ablation_role"]], on="variable_id", how="left")
        .sort_values("variable_id")
        .reset_index(drop=True)
    )

    probe_map = {"robust_3of3": "Robust", "no_core_pass_0of3": "Non-robust"}
    df["probe_status"] = df["probe_core_status"].map(probe_map).fillna("Non-robust")

    probe_colors = {"Robust": "#1f77b4", "Non-robust": "#d9d9d9"}
    sae_colors = {"A": "#2166ac", "B1": "#4393c3", "B2": "#92c5de", "C": "#f4a582", "D": "#d6604d"}
    inspection_colors = {"A": "#1b9e77", "B": "#66a61e", "C": "#e6ab02", "D": "#d95f02"}

    n = len(df)
    fig_h = max(10.5, 0.23 * n + 2.0)
    fig = plt.figure(figsize=(8.8, fig_h))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.9, 1.6], wspace=0.03)
    ax_labels = fig.add_subplot(gs[0, 0])
    ax_cells = fig.add_subplot(gs[0, 1])

    ax_labels.set_xlim(0, 1)
    ax_labels.set_ylim(-0.5, n - 0.5)
    ax_labels.invert_yaxis()
    ax_labels.axis("off")
    for i, row in df.iterrows():
        ax_labels.text(0.0, i, short_var_label(row["variable_id"], row["variable"], width=34),
                       va="center", ha="left", fontsize=8.7)

    ax_cells.set_xlim(0, 3)
    ax_cells.set_ylim(-0.5, n - 0.5)
    ax_cells.invert_yaxis()
    ax_cells.set_xticks(np.arange(3) + 0.5)
    ax_cells.set_xticklabels(["Probe", "SAE", "Inspection"], fontweight="bold")
    ax_cells.xaxis.tick_top()
    ax_cells.set_yticks([])
    ax_cells.tick_params(length=0)
    for x in range(4):
        ax_cells.axvline(x, color="#888888", lw=0.6)
    for y in range(n + 1):
        ax_cells.axhline(y - 0.5, color="#E6E6E6", lw=0.5)

    for i, row in df.iterrows():
        vals = [row["probe_status"], row["evidence_tier"], row["inspection_grade"]]
        colors = [
            probe_colors.get(vals[0], "white"),
            sae_colors.get(vals[1], "white"),
            inspection_colors.get(vals[2], "white"),
        ]
        labels = ["R" if vals[0] == "Robust" else "N", vals[1], vals[2]]
        for j, (fc, lab) in enumerate(zip(colors, labels)):
            ax_cells.add_patch(Rectangle((j, i - 0.5), 1, 1, facecolor=fc, edgecolor="white", linewidth=1.1))
            text_color = "white" if fc not in ["#d9d9d9", "#92c5de", "#f4a582", "#e6ab02"] else "black"
            ax_cells.text(j + 0.5, i, lab, ha="center", va="center", fontsize=8.8,
                          fontweight="bold", color=text_color)

    fig.suptitle("Evidence overview across 40 linguistic variables", y=0.995, fontsize=13, fontweight="bold")
    fig.text(0.53, 0.013,
             "Probe column: R = robust, N = non-robust. SAE and inspection columns show categorical grades.",
             ha="left", va="bottom", fontsize=8.5)
    fig.subplots_adjust(bottom=0.045)
    save_figure(fig, output_dir, "evidence")
    plt.close(fig)


def plot_causal(root: Path, output_dir: Path) -> None:
    abl = load_csv(root, "causal_steps/causal_interventions/ablation_screen/ablation_variable_summary.csv")
    steer = load_csv(root, "causal_steps/causal_interventions/steering_screen/steering_variable_summary.csv")
    pre = load_csv(root, "causal_steps/causal_interventions/mechanistic_convergence/PREBEHAVIOR_PRIMARY_COHORT.csv")
    final = load_csv(root, "causal_steps/causal_interventions/final_summary/FULL_CHAIN_PRIMARY_RESULTS.csv")

    steer_primary = steer[steer["primary_dose"] == True].copy()
    df = (
        abl[["variable_id", "variable", "inspection_grade", "target_minus_control_attenuation", "causal_screen_category"]]
        .rename(columns={"target_minus_control_attenuation": "ablation_effect", "causal_screen_category": "ablation_category"})
        .merge(
            steer_primary[["variable_id", "target_minus_control_attenuation", "steering_screen_category", "dose_monotonic_non_decreasing"]]
            .rename(columns={"target_minus_control_attenuation": "steering_effect", "steering_screen_category": "steering_category"}),
            on="variable_id", how="left"
        )
    )

    primary_ids = set(pre["variable_id"].tolist())
    final_ids = set(final["variable_id"].tolist())
    df["is_primary"] = df["variable_id"].isin(primary_ids)
    df["is_final"] = df["variable_id"].isin(final_ids)

    n_total = len(df)
    n_abl = int((abl["causal_screen_category"] == "specific_positive").sum())
    n_steer = int((steer_primary["steering_screen_category"] == "specific_positive").sum())
    n_pre = len(pre)
    n_final = len(final)

    fig = plt.figure(figsize=(11.6, 5.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.2, 1.2], wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    bg = df[~df["is_primary"]]
    pr = df[df["is_primary"] & ~df["is_final"]]
    fin = df[df["is_final"]]

    ax.scatter(bg["ablation_effect"], bg["steering_effect"], s=36, c="#C7C7C7", edgecolors="white", linewidths=0.8, label="Other variables")
    ax.scatter(pr["ablation_effect"], pr["steering_effect"], s=58, c="#4C78A8", edgecolors="white", linewidths=0.9, label="Primary mechanistic cohort")
    ax.scatter(fin["ablation_effect"], fin["steering_effect"], s=100, c="#D62728", marker="*", edgecolors="white", linewidths=0.7, label="Full-chain primary")

    for _, row in df.iterrows():
        if row["is_primary"]:
            ax.text(row["ablation_effect"], row["steering_effect"], f" {int(row['variable_id']):02d}", fontsize=8, va="center")

    ax.axhline(0, color="#6E6E6E", lw=0.9, ls="--")
    ax.axvline(0, color="#6E6E6E", lw=0.9, ls="--")
    ax.set_xlabel("Ablation target-minus-control effect")
    ax.set_ylabel("Steering target-minus-control effect")
    ax.set_title("(a) Causal intervention effects by variable", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper left")

    ax2 = fig.add_subplot(gs[0, 1])
    stages = ["Ranked\ncandidates", "Ablation-\nspecific", "Steering-\nspecific", "Primary\nmechanistic", "Full-chain\nprimary"]
    counts = [n_total, n_abl, n_steer, n_pre, n_final]
    colors = ["#D9D9D9", "#9ECAE1", "#A1D99B", "#FDAE6B", "#FB6A4A"]
    bars = ax2.bar(range(len(stages)), counts, color=colors, edgecolor="black", linewidth=0.6)
    ax2.set_xticks(range(len(stages)))
    ax2.set_xticklabels(stages)
    ax2.set_ylabel("Variables")
    ax2.set_ylim(0, max(counts) * 1.18)
    ax2.set_title("(b) Funnel from candidate features to final causal evidence", loc="left", fontweight="bold")
    for bar, count in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.7, str(count),
                 ha="center", va="bottom", fontsize=10, fontweight="bold")

    fig.suptitle("From mechanistic candidates to causal evidence", y=1.02, fontsize=13, fontweight="bold")
    save_figure(fig, output_dir, "causal")
    plt.close(fig)


def plot_behavior(root: Path, output_dir: Path) -> None:
    beh = load_csv(root, "causal_steps/causal_interventions/behavioral_evaluation/behavioral_variable_summary.csv")
    final = load_csv(root, "causal_steps/causal_interventions/final_summary/FULL_CHAIN_PRIMARY_RESULTS.csv")

    df = beh[beh["primary_mechanistic"] == True].copy()
    df["is_final"] = df["variable_id"].isin(final["variable_id"].tolist())
    df = df.sort_values("target_minus_control_behavioral_effect", ascending=True).reset_index(drop=True)

    category_colors = {
        "specific_positive": "#1b9e77",
        "positive_control_advantage": "#7570b3",
        "positive_nonspecific": "#e7298a",
        "null_or_reverse": "#9E9E9E",
    }

    fig_h = max(5.8, 0.36 * len(df) + 1.7)
    fig, ax = plt.subplots(figsize=(10.2, fig_h))

    for i, row in df.iterrows():
        color = category_colors.get(row["behavioral_category"], "#9E9E9E")
        ax.hlines(i, row["target_minus_control_ci_low"], row["target_minus_control_ci_high"], color=color, lw=2.0, zorder=1)
        marker = "*" if row["is_final"] else "o"
        size = 110 if row["is_final"] else 42
        edgecolor = "black" if row["is_final"] else "white"
        ax.scatter(row["target_minus_control_behavioral_effect"], i, s=size, c=color, marker=marker,
                   edgecolors=edgecolor, linewidths=0.7, zorder=2)
        ax.text(row["target_minus_control_behavioral_effect"], i,
                f"  {int(row['variable_id']):02d}", va="center", ha="left", fontsize=8)

    ax.axvline(0, color="#6E6E6E", lw=1.0, ls="--")
    labels = [short_var_label(r.variable_id, r.variable, width=34) for r in df.itertuples()]
    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Behavioral effect (target minus matched controls)")
    ax.set_ylabel("Primary mechanistic cohort")
    ax.set_title("Behavioral effects after steering in the frozen primary cohort", fontweight="bold")

    xmin = min(df["target_minus_control_ci_low"].min(), -0.03)
    xmax = max(df["target_minus_control_ci_high"].max(), 0.03)
    ax.set_xlim(xmin * 1.1, xmax * 1.1)

    handles = [Patch(facecolor=v, edgecolor="none", label=k.replace("_", " ")) for k, v in category_colors.items()]
    handles.append(Line2D([0], [0], marker="*", color="w", markerfacecolor="#D62728",
                          markeredgecolor="black", markersize=11, linestyle="None", label="Full-chain primary"))
    ax.legend(handles=handles, loc="lower right", frameon=False)

    fig.tight_layout()
    save_figure(fig, output_dir, "behavior")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate publication-ready paper figures.")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="paper_figures",
        help="Directory in which to save the generated figures.",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    output_dir = repo_root / args.output_dir
    ensure_dir(output_dir)

    print(f"Repository root: {repo_root}")
    print(f"Output directory: {output_dir}")

    plot_pipeline(output_dir)
    plot_evidence(repo_root, output_dir)
    plot_causal(repo_root, output_dir)
    plot_behavior(repo_root, output_dir)

    print("Done.")


if __name__ == "__main__":
    main()
