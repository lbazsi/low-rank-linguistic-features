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


def find_repo_root(start: Path) -> Path:
    for path in [start] + list(start.parents):
        if (path / ".git").exists():
            return path
    raise FileNotFoundError("Run this script from inside the repository.")


def find_existing_csv(root: Path, candidates: list[str], fallback_name: str, required_cols: set[str]) -> Path:
    for rel in candidates:
        p = root / rel
        if p.exists():
            return p
    for p in root.rglob(fallback_name):
        try:
            cols = set(pd.read_csv(p, nrows=1).columns)
        except Exception:
            continue
        if required_cols.issubset(cols):
            return p
    raise FileNotFoundError(f"Could not find {fallback_name} with columns {sorted(required_cols)}")


def wrap_label(text: str, width: int = 28) -> str:
    return textwrap.fill(str(text), width=width, break_long_words=False)


def load_probe_sae(root: Path) -> pd.DataFrame:
    path = find_existing_csv(
        root,
        [
            "artifacts/probe_comparison/summary/probe_sae_comparison.csv",
            "SAE/post_canonical_analysis/probe_comparison/summary/probe_sae_comparison.csv",
        ],
        "probe_sae_comparison.csv",
        {"variable_id", "variable", "sae_tier"},
    )
    df = pd.read_csv(path)

    if "probe_core_134_pass_count" in df.columns:
        counts = (
            df["probe_core_134_pass_count"]
            .astype(str)
            .str.extract(r"(\d+)")
            .fillna("0")[0]
            .astype(int)
        )
        df["probe_label"] = counts.map(lambda x: "R" if x >= 3 else "N")
    elif "probe_status" in df.columns:
        df["probe_label"] = df["probe_status"].astype(str).map(
            lambda x: "R" if "robust" in x.lower() else "N"
        )
    else:
        raise KeyError("Could not infer probe robustness column.")

    return df[["variable_id", "variable", "probe_label", "sae_tier"]].copy()


def load_inspection(root: Path) -> pd.DataFrame:
    candidates = [
        "artifacts/feature_inspection/summary/inspection_summary.csv",
        "artifacts/feature_inspection/summary/feature_inspection_summary.csv",
        "artifacts/feature_inspection/summary/all_variable_feature_review.csv",
        "feature_inspection/all_variable_feature_review.csv",
        "feature_inspection/inspection_summary.csv",
    ]

    for rel in candidates:
        p = root / rel
        if not p.exists():
            continue
        df = pd.read_csv(p)
        if {"variable_id", "inspection_grade"}.issubset(df.columns):
            return df[["variable_id", "inspection_grade"]].copy()
        if {"variable_id", "grade"}.issubset(df.columns):
            return df[["variable_id", "grade"]].rename(columns={"grade": "inspection_grade"})

    for p in root.rglob("*.csv"):
        try:
            df = pd.read_csv(p, nrows=5)
        except Exception:
            continue
        cols = set(df.columns)
        if {"variable_id", "inspection_grade"}.issubset(cols):
            full = pd.read_csv(p)
            return full[["variable_id", "inspection_grade"]].copy()
        if {"variable_id", "grade"}.issubset(cols) and "inspection" in p.name.lower():
            full = pd.read_csv(p)
            return full[["variable_id", "grade"]].rename(columns={"grade": "inspection_grade"})

    raise FileNotFoundError("Could not find a feature-inspection summary CSV with inspection grades.")


def load_causal_tables(root: Path):
    abl = pd.read_csv(find_existing_csv(
        root,
        [
            "causal_steps/causal_interventions/ablation_screen/ablation_variable_summary.csv",
            "artifacts/causal_interventions/ablation_screen/ablation_variable_summary.csv",
        ],
        "ablation_variable_summary.csv",
        {"variable_id", "target_minus_control_attenuation", "causal_screen_category"},
    ))
    steer = pd.read_csv(find_existing_csv(
        root,
        [
            "causal_steps/causal_interventions/steering_screen/steering_variable_summary.csv",
            "artifacts/causal_interventions/steering_screen/steering_variable_summary.csv",
        ],
        "steering_variable_summary.csv",
        {"variable_id", "target_minus_control_attenuation", "steering_screen_category"},
    ))
    pre = pd.read_csv(find_existing_csv(
        root,
        [
            "causal_steps/causal_interventions/mechanistic_convergence/PREBEHAVIOR_PRIMARY_COHORT.csv",
            "artifacts/causal_interventions/mechanistic_convergence/PREBEHAVIOR_PRIMARY_COHORT.csv",
        ],
        "PREBEHAVIOR_PRIMARY_COHORT.csv",
        {"variable_id"},
    ))
    final = pd.read_csv(find_existing_csv(
        root,
        [
            "causal_steps/causal_interventions/final_summary/FULL_CHAIN_PRIMARY_RESULTS.csv",
            "artifacts/causal_interventions/final_summary/FULL_CHAIN_PRIMARY_RESULTS.csv",
        ],
        "FULL_CHAIN_PRIMARY_RESULTS.csv",
        {"variable_id"},
    ))
    return abl, steer, pre, final


def make_evidence_figure(root: Path, out_dir: Path) -> None:
    probe_sae = load_probe_sae(root)
    inspection = load_inspection(root)

    df = (
        probe_sae.merge(inspection, on="variable_id", how="left")
        .sort_values("variable_id")
        .reset_index(drop=True)
    )
    df["inspection_grade"] = df["inspection_grade"].fillna("?")

    probe_colors = {"R": "#4C78A8", "N": "#D9D9D9", "?": "#F2F2F2"}
    grade_colors = {
        "A": "#2CA02C",
        "B1": "#8BCF6A",
        "B2": "#D8C84C",
        "C": "#F0A44B",
        "D": "#E15759",
        "?": "#F2F2F2",
    }

    fig = plt.figure(figsize=(12.6, 11.0))
    gs = fig.add_gridspec(1, 2, wspace=0.18)
    panels = [df.iloc[:20].copy(), df.iloc[20:].copy()]
    panel_titles = ["Variables 1–20", "Variables 21–40"]

    col_specs = [
        ("ID", 0.85),
        ("Variable", 5.65),
        ("Probe", 1.05),
        ("SAE", 1.00),
        ("Insp.", 1.00),
    ]
    total_w = sum(w for _, w in col_specs)
    x_edges = [0]
    for _, w in col_specs:
        x_edges.append(x_edges[-1] + w)

    for panel, title, cell in zip(panels, panel_titles, [gs[0, 0], gs[0, 1]]):
        ax = fig.add_subplot(cell)
        ax.set_xlim(0, total_w)
        ax.set_ylim(0, len(panel) + 1.8)
        ax.axis("off")
        ax.text(0, len(panel) + 1.35, title, fontsize=11, fontweight="bold", ha="left", va="bottom")

        y_header = len(panel) + 0.35
        for i, (label, width) in enumerate(col_specs):
            ax.add_patch(Rectangle((x_edges[i], y_header), width, 0.95,
                                   facecolor="#EAEAEA", edgecolor="#BBBBBB", linewidth=0.8))
            ax.text(x_edges[i] + width / 2, y_header + 0.48, label,
                    ha="center", va="center", fontweight="bold", fontsize=9)

        for row_idx, (_, row) in enumerate(panel.iterrows()):
            y = len(panel) - row_idx - 0.55
            base_fill = "#FFFFFF" if row_idx % 2 == 0 else "#FAFAFA"

            ax.add_patch(Rectangle((x_edges[0], y), col_specs[0][1], 0.92,
                                   facecolor=base_fill, edgecolor="#DDDDDD", linewidth=0.6))
            ax.text(x_edges[0] + col_specs[0][1] / 2, y + 0.46,
                    f"{int(row['variable_id']):02d}", ha="center", va="center", fontsize=8.5)

            ax.add_patch(Rectangle((x_edges[1], y), col_specs[1][1], 0.92,
                                   facecolor=base_fill, edgecolor="#DDDDDD", linewidth=0.6))
            ax.text(x_edges[1] + 0.12, y + 0.46, wrap_label(row["variable"], 28),
                    ha="left", va="center", fontsize=7.8)

            probe = str(row["probe_label"])
            ax.add_patch(Rectangle((x_edges[2], y), col_specs[2][1], 0.92,
                                   facecolor=probe_colors.get(probe, "#F2F2F2"),
                                   edgecolor="#DDDDDD", linewidth=0.6))
            ax.text(x_edges[2] + col_specs[2][1] / 2, y + 0.46, probe,
                    ha="center", va="center", fontsize=9, fontweight="bold")

            sae = str(row["sae_tier"])
            ax.add_patch(Rectangle((x_edges[3], y), col_specs[3][1], 0.92,
                                   facecolor=grade_colors.get(sae, "#F2F2F2"),
                                   edgecolor="#DDDDDD", linewidth=0.6))
            ax.text(x_edges[3] + col_specs[3][1] / 2, y + 0.46, sae,
                    ha="center", va="center", fontsize=8.5, fontweight="bold")

            insp = str(row["inspection_grade"])
            ax.add_patch(Rectangle((x_edges[4], y), col_specs[4][1], 0.92,
                                   facecolor=grade_colors.get(insp, "#F2F2F2"),
                                   edgecolor="#DDDDDD", linewidth=0.6))
            ax.text(x_edges[4] + col_specs[4][1] / 2, y + 0.46, insp,
                    ha="center", va="center", fontsize=8.5, fontweight="bold")

    fig.suptitle("Evidence summary across forty linguistic variables",
                 fontsize=13, fontweight="bold", y=0.985)
    fig.text(0.08, 0.03,
             "Probe: R = robust, N = non-robust. SAE and inspection columns show categorical grades.",
             ha="left", fontsize=9)
    fig.subplots_adjust(left=0.05, right=0.985, top=0.95, bottom=0.07)

    out = out_dir / "evidence.png"
    fig.savefig(out, bbox_inches="tight", dpi=400)
    plt.close(fig)
    print(f"Saved: {out}")


def make_causal_figure(root: Path, out_dir: Path) -> None:
    abl, steer, pre, final = load_causal_tables(root)

    if "primary_dose" in steer.columns:
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
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=8,
            ha="left",
            va="center",
        )

    ax.axhline(0, color="#777777", lw=0.9, ls="--", zorder=1)
    ax.axvline(0, color="#777777", lw=0.9, ls="--", zorder=1)
    ax.set_xlabel("Ablation target-minus-control effect")
    ax.set_ylabel("Steering target-minus-control effect")
    ax.set_title("(a) Matched ablation and steering effects", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper left")

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
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
        )

    fig.subplots_adjust(left=0.08, right=0.985, top=0.93, bottom=0.14)

    out = out_dir / "causal.png"
    fig.savefig(out, bbox_inches="tight", dpi=400)
    plt.close(fig)
    print(f"Saved: {out}")


def main() -> None:
    root = find_repo_root(Path.cwd())
    out_dir = root / "paper_figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    make_evidence_figure(root, out_dir)
    make_causal_figure(root, out_dir)


if __name__ == "__main__":
    main()
