#!/usr/bin/env python3
"""Generate only the two-panel activation-versus-text figure.

From the repository root:
    python -m pip install matplotlib
    python generate_activation_figure.py

Writes figures/paper/activation_vs_text.png, overwriting it on reruns.
The left panel contains the first 20 variables in the original descending
AUROC-margin order; the right panel continues with the remaining 20.
Both panels use the same horizontal limits and ticks.
"""

import csv
from pathlib import Path
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "figures" / "paper" / "activation_vs_text.png"
PROBES = ROOT / "forward_pass_runs" / "v1"
SEEDS = (1, 2, 42)
BLUE = "#356CA5"
GRAY = "#A3A9AF"


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
    return textwrap.fill(
        f"{int(row['variable_id']):02d}  {name}", width,
        break_long_words=False, break_on_hyphens=False,
    )


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

    # Split the existing global ordering; do not re-sort within either panel.
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 10.2), sharex=True)
    fig.subplots_adjust(left=0.24, right=0.985, top=0.88, bottom=0.13, wspace=1.3)
    lower = min(-0.05, min(margins.values()))
    upper = max(0.05, max(margins.values()))
    padding = max(0.02, (upper - lower) * 0.05)

    for ax, panel_ids in zip(axes, (order[:20], order[20:])):
        ax.axvspan(-0.05, 0.05, color="#F0F2F4", zorder=0)
        ax.axvline(0, color="#60666C", linewidth=0.8)
        for value in (-0.05, 0.05):
            ax.axvline(value, color="#8C9298", linestyle="--", linewidth=0.8)
        for y, vid in enumerate(panel_ids):
            color = BLUE if vid in core else GRAY
            ax.hlines(y, 0, margins[vid], color=color, alpha=0.35, linewidth=1.0)
            ax.plot(margins[vid], y, "o", color=color, markersize=5)
        ax.set_yticks(range(20))
        ax.set_yticklabels([label(seeds[0][vid]) for vid in panel_ids])
        ax.tick_params(axis="y", length=0, labelsize=12.5, labelleft=True)
        for tick in ax.get_yticklabels():
            tick.set_linespacing(1.0)
        ax.tick_params(axis="x", labelsize=12)
        ax.set_ylim(19.8, -0.8)
        ax.set_xlim(lower - padding, upper + padding)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
        ax.spines[["top", "right", "left"]].set_visible(False)

    fig.suptitle(
        "Activation recovery relative to surface-text baselines", fontsize=16, y=0.98
    )
    fig.legend(handles=[
        Line2D([], [], marker="o", color=BLUE, linestyle="none",
               label=f"Core probe criterion ({len(core)}/40)"),
        Line2D([], [], marker="o", color=GRAY, linestyle="none",
               label=f"Remaining variables ({40-len(core)}/40)"),
    ], loc="upper center", bbox_to_anchor=(0.5, 0.946), ncol=2,
       frameon=False, fontsize=12)
    fig.supxlabel(
        "Sentence activation AUROC − best text-baseline AUROC", fontsize=13, y=0.075
    )
    fig.text(
        0.03, 0.015,
        "Mean margin across seeds 1, 2, and 42. Dashed lines mark ±0.05 AUROC.\n"
        "Core status requires levels 1, 3, and 4 in all three seeds.",
        fontsize=10,
    )
    return fig


def main():
    seeds = [
        read_rows(PROBES / f"results_seed_{seed}" / "visuals-tables" / "tables"
                  / "evidence_status_by_variable.csv")
        for seed in SEEDS
    ]
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "axes.axisbelow": True,
    })
    fig = probe_figure(seeds)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
