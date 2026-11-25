#!/usr/bin/env python3
"""Generate the three revised main-paper figures from committed CSV results.

From the repository root in a Codespace:
    python -m pip install matplotlib
    python generate_paper_figures.py

Writes exactly three PNG files to figures/paper/ (overwritten on reruns).
The probe plot averages sentence AUROC margins over seeds 1, 2, and 42.
Core status requires evidence levels 1, 3, and 4 in every seed. The causal
counts and behavioral intervals come from the canonical intervention results.
"""

import csv
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "figures" / "paper"
PROBES = ROOT / "forward_pass_runs" / "v1"
CAUSAL = ROOT / "causal_steps" / "causal_interventions"
BLUE = "#356CA5"
GRAY = "#A3A9AF"
GREEN = "#008B70"
PURPLE = "#7861A8"


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    indexed = {int(row["variable_id"]): row for row in rows}
    if len(indexed) != 40 or len(rows) != 40 or set(indexed) != set(range(1, 41)):
        raise ValueError(f"Expected one row per variable 1–40 in {path}")
    return indexed


def flag(row, key):
    value = row[key].strip().lower()
    if value not in {"true", "false"}:
        raise ValueError(f"Invalid boolean for {key}: {row[key]!r}")
    return value == "true"


def label(row, width=32):
    name = row["variable"].replace("_", " ").replace("/", " / ")
    name = " ".join(name.split()).capitalize()
    return textwrap.fill(f"{int(row['variable_id']):02d}  {name}", width)


def save(fig, name):
    path = OUTPUT / name
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(path.relative_to(ROOT))


def probe_figure(seeds):
    levels = (
        "level_1_activation_recoverability_pass",
        "level_3_directional_consistency_pass",
        "level_4_split_generalization_pass",
    )
    core = {
        vid for vid in seeds[0]
        if all(flag(seed[vid], key) for seed in seeds for key in levels)
    }
    margins = {
        vid: sum(
            float(seed[vid]["sentence_activation_test_auroc"])
            - float(seed[vid]["sentence_best_text_test_auroc"])
            for seed in seeds
        ) / len(seeds)
        for vid in seeds[0]
    }
    order = sorted(margins, key=lambda vid: (-margins[vid], vid))
    fig, ax = plt.subplots(figsize=(9.0, 13.2))
    fig.subplots_adjust(left=0.40, right=0.97, top=0.93, bottom=0.085)
    ax.axvspan(-0.05, 0.05, color="#F0F2F4", zorder=0)
    ax.axvline(0, color="#60666C", linewidth=0.8)
    for value in (-0.05, 0.05):
        ax.axvline(value, color="#8C9298", linestyle="--", linewidth=0.8)
    for y, vid in enumerate(order):
        color = BLUE if vid in core else GRAY
        ax.hlines(y, 0, margins[vid], color=color, alpha=0.35, linewidth=1.0)
        ax.plot(margins[vid], y, "o", color=color, markersize=5)
    ax.set_yticks(range(40), [label(seeds[0][vid], 39) for vid in order])
    ax.tick_params(axis="y", length=0, labelsize=8)
    ax.set_ylim(39.8, -0.8)
    ax.set_xlabel("Sentence activation AUROC − best text-baseline AUROC")
    ax.set_title("Activation recovery relative to surface-text baselines", pad=38)
    ax.legend(handles=[
        Line2D([], [], marker="o", color=BLUE, linestyle="none",
               label=f"Core probe criterion ({len(core)}/40)"),
        Line2D([], [], marker="o", color=GRAY, linestyle="none",
               label=f"Remaining variables ({40-len(core)}/40)"),
    ], loc="lower center", bbox_to_anchor=(0.5, 1.005), ncol=1,
       frameon=False, fontsize=8)
    fig.text(0.40, 0.025,
             "Mean margin across seeds 1, 2, and 42. Dashed lines mark ±0.05 AUROC.\n"
             "Core status requires levels 1, 3, and 4 in all three seeds.", fontsize=8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    save(fig, "activation_vs_text.png")


def causal_figure(rows):
    primary = {vid for vid, row in rows.items() if flag(row, "primary_mechanistic")}
    full = {vid for vid, row in rows.items() if flag(row, "full_chain_primary")}
    ablation = {vid for vid, row in rows.items() if flag(row, "ablation_specific")}
    steering = {vid for vid, row in rows.items() if flag(row, "steering_specific")}
    expected_primary = {
        vid for vid in ablation & steering if flag(rows[vid], "steering_dose_monotonic")
    }
    if primary != expected_primary or not full <= primary:
        raise ValueError("Causal cohort flags disagree with the cohort criteria")
    fig, (ax, diagram) = plt.subplots(
        1, 2, figsize=(11.5, 6.2), gridspec_kw={"width_ratios": [1.1, 1]}
    )
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.16, top=0.87, wspace=0.28)
    for vid, row in rows.items():
        x = float(row["ablation_target_minus_control"])
        y = float(row["steering_target_minus_control"])
        color = BLUE if vid in primary else GRAY
        ax.scatter(x, y, color=color, s=23, alpha=0.8)
        if vid in full:
            ax.scatter(x, y, marker="*", s=105, color="#C04C46",
                       edgecolor="white", linewidth=0.5, zorder=4)
        if vid in full or vid in {6, 16}:
            offsets = {10: (12, -10), 19: (-18, -18), 23: (16, 4), 27: (-18, 12)}
            ax.annotate(str(vid), (x, y), xytext=offsets.get(vid, (5, 5)),
                        textcoords="offset points", fontsize=7,
                        arrowprops={"arrowstyle": "-", "color": "#737A81", "lw": 0.5})
    ax.axhline(0, color=GRAY, linestyle="--", linewidth=0.8)
    ax.axvline(0, color=GRAY, linestyle="--", linewidth=0.8)
    ax.set_xlabel("Ablation target-minus-control effect")
    ax.set_ylabel("Steering target-minus-control effect")
    ax.set_title("(a) Internal representation effects", fontsize=11, pad=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(handles=[
        Line2D([], [], marker="o", linestyle="none", color=GRAY, label="Other variables"),
        Line2D([], [], marker="o", linestyle="none", color=BLUE, label="Primary cohort"),
        Line2D([], [], marker="*", linestyle="none", color="#C04C46",
               markersize=10, label="Behavioral criterion passed"),
    ], frameon=False, fontsize=8, loc="upper left")
    diagram.set(xlim=(0, 1), ylim=(0, 1))
    diagram.axis("off")
    diagram.set_title("(b) Parallel intervention screens", fontsize=11, pad=14)

    def box(x, y, width, height, text, color):
        diagram.add_patch(FancyBboxPatch(
            (x, y), width, height, boxstyle="round,pad=0.012",
            facecolor=color, edgecolor="#C2C7CC", linewidth=0.8,
        ))
        diagram.text(x + width/2, y + height/2, text, ha="center", va="center", fontsize=9)

    def arrow(start, end):
        diagram.annotate("", xy=end, xytext=start,
                         arrowprops={"arrowstyle": "->", "color": "#737A81", "lw": 1})

    box(0.20, 0.83, 0.60, 0.12, f"{len(rows)} selected candidates", "#EEF1F4")
    box(0.01, 0.56, 0.44, 0.15, f"Specific-positive ablation\n{len(ablation)}/{len(rows)}", "#DFEBF5")
    box(0.55, 0.56, 0.44, 0.15, f"Specific-positive steering\n{len(steering)}/{len(rows)}", "#DFEBF5")
    arrow((0.39, 0.82), (0.23, 0.72))
    arrow((0.61, 0.82), (0.77, 0.72))
    box(0.13, 0.27, 0.74, 0.16,
        f"Both screens + monotonic steering\nPrimary cohort {len(primary)}/{len(rows)}", "#DEEDE8")
    arrow((0.23, 0.55), (0.37, 0.44))
    arrow((0.77, 0.55), (0.63, 0.44))
    box(0.13, 0.01, 0.74, 0.15,
        f"Positive, control-specific next-token effect\nPrimary-family FDR criterion {len(full)}/{len(primary)}", "#F6E5DF")
    arrow((0.50, 0.26), (0.50, 0.17))
    fig.text(0.08, 0.04,
             "Ablation and steering screen the same 40 candidates in parallel. "
             "Steering uses the primary 1× dose.\n"
             "The 15-variable cohort was frozen before behavioral evaluation. "
             "Point labels are variable IDs.", fontsize=8)
    save(fig, "causal.png")


def behavioral_figure(rows, causal):
    primary = [row for row in rows.values() if flag(row, "primary_mechanistic")]
    primary.sort(key=lambda row: -float(row["target_minus_control_behavioral_effect"]))
    fig, ax = plt.subplots(figsize=(10, 8.2))
    fig.subplots_adjust(left=0.39, right=0.97, top=0.91, bottom=0.19)
    colors = {"specific_positive": GREEN, "positive_control_advantage": PURPLE,
              "positive_nonspecific": "#C35090", "null_or_reverse": GRAY}
    for y, row in enumerate(primary):
        vid = int(row["variable_id"])
        value = float(row["target_minus_control_behavioral_effect"])
        low = float(row["target_minus_control_ci_low"])
        high = float(row["target_minus_control_ci_high"])
        color = colors[row["behavioral_category"]]
        ax.hlines(y, low, high, color=color, linewidth=1.5)
        ax.plot(value, y, "o", color=color, markersize=4)
        if flag(causal[vid], "full_chain_primary"):
            ax.plot(value, y, "*", color=color, markeredgecolor="#263238",
                    markeredgewidth=0.6, markersize=11, zorder=4)
    ax.axvline(0, color="#737A81", linestyle="--", linewidth=0.9)
    ax.set_yticks(range(len(primary)), [label(row) for row in primary])
    ax.tick_params(axis="y", labelsize=9, length=0)
    ax.set_ylim(len(primary)-0.5, -0.5)
    ax.set_xlabel("Target-minus-control change in next-token logit margin (logits)")
    ax.set_title("Next-token effects in the frozen primary cohort", fontsize=12, pad=16)
    ax.spines[["top", "right", "left"]].set_visible(False)
    present = {row["behavioral_category"] for row in primary}
    descriptions = {"specific_positive": "Positive and control-specific",
                    "positive_control_advantage": "Positive, control advantage",
                    "positive_nonspecific": "Positive, nonspecific",
                    "null_or_reverse": "Null or reverse"}
    ax.legend(handles=[
        Line2D([], [], marker="o", linestyle="none", color=color,
               label=descriptions[key]) for key, color in colors.items() if key in present
    ] + [Line2D([], [], marker="*", linestyle="none", color="white",
                markeredgecolor="#263238", markersize=10, label="Full behavioral criterion")],
        frameon=False, fontsize=8, loc="lower right")
    unchanged = sum(
        float(row["baseline_high_token_preference_rate"])
        == float(row["steered_high_token_preference_rate"]) for row in primary
    )
    fig.text(0.05, 0.04,
             "Points show the primary 1× dose; intervals are paired-bootstrap 95% CIs. "
             "FDR correction uses the frozen 15-variable family.\n"
             f"Aggregate feature-high token preference rates were unchanged for {unchanged}/{len(primary)} variables under target steering.\n"
             "Equal aggregate rates can include offsetting changes on individual pairs.", fontsize=8)
    save(fig, "behavior.png")


def main():
    seeds = [read_rows(PROBES / f"results_seed_{seed}" / "visuals-tables" / "tables"
                       / "evidence_status_by_variable.csv") for seed in (1, 2, 42)]
    causal = read_rows(CAUSAL / "final_summary" / "final_causal_evidence.csv")
    behavior = read_rows(CAUSAL / "behavioral_evaluation" / "behavioral_variable_summary.csv")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.titlesize": 12, "axes.labelsize": 10,
                         "xtick.labelsize": 9, "axes.axisbelow": True})
    probe_figure(seeds)
    causal_figure(causal)
    behavioral_figure(behavior, causal)


if __name__ == "__main__":
    main()
