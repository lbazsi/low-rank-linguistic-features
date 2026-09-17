#!/usr/bin/env python3
from pathlib import Path
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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


def repo_root() -> Path:
    here = Path.cwd()
    for p in [here] + list(here.parents):
        if (p / ".git").exists():
            return p
    raise FileNotFoundError("Run this script from inside the repository.")


def find_csv(root: Path, filename: str, required: set[str]) -> Path:
    for p in root.rglob(filename):
        try:
            cols = set(pd.read_csv(p, nrows=1).columns)
        except Exception:
            continue
        if required.issubset(cols):
            return p
    raise FileNotFoundError(f"Could not find {filename} with columns {sorted(required)}")


def load_evidence(root: Path) -> pd.DataFrame:
    ps = pd.read_csv(find_csv(root, "probe_sae_comparison.csv", {"variable_id", "variable", "sae_tier"}))
    if "probe_core_134_pass_count" in ps.columns:
        n = ps["probe_core_134_pass_count"].astype(str).str.extract(r"(\d+)")[0].fillna("0").astype(int)
        ps["probe"] = n.map(lambda x: "R" if x >= 3 else "N")
    elif "probe_status" in ps.columns:
        ps["probe"] = ps["probe_status"].astype(str).map(lambda x: "R" if "robust" in x.lower() else "N")
    else:
        raise KeyError("No probe robustness column found.")

    insp = None
    for p in root.rglob("*.csv"):
        try:
            d = pd.read_csv(p, nrows=3)
        except Exception:
            continue
        if {"variable_id", "inspection_grade"}.issubset(d.columns):
            insp = pd.read_csv(p)[["variable_id", "inspection_grade"]]
            break
    if insp is None:
        raise FileNotFoundError("Could not find inspection grades.")

    return (
        ps[["variable_id", "variable", "probe", "sae_tier"]]
        .merge(insp, on="variable_id", how="left")
        .sort_values("variable_id")
        .reset_index(drop=True)
    )


def load_causal(root: Path):
    abl = pd.read_csv(find_csv(root, "ablation_variable_summary.csv", {"variable_id", "target_minus_control_attenuation", "causal_screen_category"}))
    steer = pd.read_csv(find_csv(root, "steering_variable_summary.csv", {"variable_id", "target_minus_control_attenuation", "steering_screen_category"}))
    pre = pd.read_csv(find_csv(root, "PREBEHAVIOR_PRIMARY_COHORT.csv", {"variable_id"}))
    final = pd.read_csv(find_csv(root, "FULL_CHAIN_PRIMARY_RESULTS.csv", {"variable_id"}))
    if "primary_dose" in steer.columns:
        steer = steer[steer["primary_dose"] == True].copy()
    return abl, steer, pre, final


def make_evidence(root: Path, out: Path) -> None:
    df = load_evidence(root)
    df["inspection_grade"] = df["inspection_grade"].fillna("?")

    probe_colors = {"R": "#4C78A8", "N": "#D9D9D9", "?": "#F2F2F2"}
    grade_colors = {"A": "#2CA02C", "B1": "#8BCF6A", "B2": "#D8C84C", "C": "#F0A44B", "D": "#E15759", "?": "#F2F2F2"}

    panels = [df.iloc[:20].copy(), df.iloc[20:].copy()]
    titles = ["Variables 1–20", "Variables 21–40"]
    for panel in panels:
        panel["name"] = panel["variable"].map(lambda x: textwrap.fill(str(x), width=23, break_long_words=False))
        panel["height"] = panel["name"].map(lambda x: 0.78 + 0.38 * x.count("\n"))

    max_body = max(panel["height"].sum() for panel in panels)
    fig = plt.figure(figsize=(13.5, max_body * 0.54 + 2.5))
    gs = fig.add_gridspec(1, 2, wspace=0.15)

    specs = [("ID", 0.75), ("Variable", 5.2), ("Probe", 0.95), ("SAE", 0.9), ("Insp.", 0.9)]
    edges = [0.0]
    for _, w in specs:
        edges.append(edges[-1] + w)
    total_w = edges[-1]

    for panel, title, cell in zip(panels, titles, [gs[0, 0], gs[0, 1]]):
        ax = fig.add_subplot(cell)
        body_h = panel["height"].sum()
        ax.set_xlim(0, total_w)
        ax.set_ylim(0, body_h + 2.0)
        ax.axis("off")
        ax.text(0, body_h + 1.45, title, fontsize=11, fontweight="bold", ha="left")

        header_y = body_h + 0.35
        for i, (label, width) in enumerate(specs):
            ax.add_patch(Rectangle((edges[i], header_y), width, 0.9, facecolor="#EAEAEA", edgecolor="#BBBBBB", linewidth=0.7))
            ax.text(edges[i] + width / 2, header_y + 0.45, label, ha="center", va="center", fontsize=9, fontweight="bold")

        cursor = body_h
        for row_i, (_, row) in enumerate(panel.iterrows()):
            h = float(row["height"])
            y = cursor - h
            cursor = y
            base = "#FFFFFF" if row_i % 2 == 0 else "#FAFAFA"

            for col in (0, 1):
                ax.add_patch(Rectangle((edges[col], y), specs[col][1], h, facecolor=base, edgecolor="#DDDDDD", linewidth=0.55))

            ax.text(edges[0] + specs[0][1] / 2, y + h / 2, f"{int(row['variable_id']):02d}", ha="center", va="center", fontsize=8.3)
            ax.text(edges[1] + 0.10, y + h / 2, row["name"], ha="left", va="center", fontsize=7.4, linespacing=1.05)

            vals = [(2, str(row["probe"]), probe_colors), (3, str(row["sae_tier"]), grade_colors), (4, str(row["inspection_grade"]), grade_colors)]
            for col, value, cmap in vals:
                ax.add_patch(Rectangle((edges[col], y), specs[col][1], h, facecolor=cmap.get(value, "#F2F2F2"), edgecolor="#DDDDDD", linewidth=0.55))
                ax.text(edges[col] + specs[col][1] / 2, y + h / 2, value, ha="center", va="center", fontsize=8.4, fontweight="bold")

    fig.suptitle("Evidence summary across forty linguistic variables", fontsize=13, fontweight="bold", y=0.985)
    fig.text(0.05, 0.025, "Probe: R = robust, N = non-robust. SAE and inspection columns show categorical grades.", fontsize=8.8)
    fig.subplots_adjust(left=0.035, right=0.99, top=0.94, bottom=0.065)
    fig.savefig(out / "evidence.png", bbox_inches="tight", dpi=400)
    plt.close(fig)
    print(f"Saved: {out / 'evidence.png'}")


def make_causal(root: Path, out: Path) -> None:
    abl, steer, pre, final = load_causal(root)
    df = (
        abl[["variable_id", "variable", "target_minus_control_attenuation", "causal_screen_category"]]
        .rename(columns={"target_minus_control_attenuation": "ablation", "causal_screen_category": "ablation_category"})
        .merge(
            steer[["variable_id", "target_minus_control_attenuation", "steering_screen_category"]]
            .rename(columns={"target_minus_control_attenuation": "steering", "steering_screen_category": "steering_category"}),
            on="variable_id", how="left"
        )
    )

    primary_ids = set(pre["variable_id"].astype(int))
    final_ids = set(final["variable_id"].astype(int))
    df["primary"] = df["variable_id"].isin(primary_ids)
    df["final"] = df["variable_id"].isin(final_ids)

    counts = {
        "Ranked candidates": len(df),
        "Ablation-specific": int((abl["causal_screen_category"] == "specific_positive").sum()),
        "Steering-specific": int((steer["steering_screen_category"] == "specific_positive").sum()),
        "Primary mechanistic": len(pre),
        "Full-chain primary": len(final),
    }

    fig = plt.figure(figsize=(13.0, 5.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.05, 1.05], wspace=0.40)

    ax = fig.add_subplot(gs[0, 0])
    other = df[~df["primary"]]
    primary = df[df["primary"] & ~df["final"]]
    full = df[df["final"]]

    ax.scatter(other["ablation"], other["steering"], s=34, color="#C8C8C8", edgecolor="white", linewidth=0.7, label="Other variables", zorder=2)
    ax.scatter(primary["ablation"], primary["steering"], s=56, color="#4C78A8", edgecolor="white", linewidth=0.8, label="Primary mechanistic cohort", zorder=3)
    ax.scatter(full["ablation"], full["steering"], s=120, color="#D62728", marker="*", edgecolor="white", linewidth=0.8, label="Full-chain primary", zorder=4)

    offsets = {6: (6, 5), 10: (6, -10), 16: (6, 0), 17: (6, 0), 19: (6, -10), 21: (6, 0), 23: (6, 6), 27: (6, 6)}
    for _, row in df[df["variable_id"].isin(final_ids | {6, 16})].iterrows():
        dx, dy = offsets.get(int(row["variable_id"]), (6, 4))
        ax.annotate(f"{int(row['variable_id']):02d}", (row["ablation"], row["steering"]), xytext=(dx, dy), textcoords="offset points", fontsize=8, ha="left", va="center")

    ax.axhline(0, color="#777777", lw=0.9, ls="--", zorder=1)
    ax.axvline(0, color="#777777", lw=0.9, ls="--", zorder=1)
    ax.set_xlabel("Ablation target-minus-control effect")
    ax.set_ylabel("Steering target-minus-control effect")
    ax.set_title("(a) Matched ablation and steering effects", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper left")

    ax2 = fig.add_subplot(gs[0, 1])
    labels = [textwrap.fill(x, width=13, break_long_words=False) for x in counts.keys()]
    values = list(counts.values())
    colors = ["#D9D9D9", "#9ECAE1", "#A1D99B", "#FDAE6B", "#FB6A4A"]
    bars = ax2.barh(range(len(labels)), values, color=colors, edgecolor="#333333", linewidth=0.6)
    ax2.set_yticks(range(len(labels)))
    ax2.set_yticklabels(labels, fontsize=8.4, linespacing=1.02)
    ax2.invert_yaxis()
    ax2.set_xlabel("Variables")
    ax2.set_xlim(0, max(values) * 1.21)
    ax2.set_title("(b) Progression through causal criteria", loc="left", fontweight="bold")
    for bar, value in zip(bars, values):
        ax2.text(bar.get_width() + 0.7, bar.get_y() + bar.get_height() / 2, str(value), va="center", ha="left", fontsize=10, fontweight="bold")

    fig.suptitle("Representation of mechanistic candidates and related causal evidence", fontsize=13, fontweight="bold", y=0.985)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.875, bottom=0.14)
    fig.savefig(out / "causal.png", bbox_inches="tight", dpi=400)
    plt.close(fig)
    print(f"Saved: {out / 'causal.png'}")


def main() -> None:
    root = repo_root()
    out = root / "paper_figures"
    out.mkdir(parents=True, exist_ok=True)
    make_evidence(root, out)
    make_causal(root, out)


if __name__ == "__main__":
    main()
