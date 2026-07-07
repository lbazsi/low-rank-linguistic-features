from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


SENTENCE_FAMILY = "sentence_basis_changed"
DELTA_MISMATCH_FAMILY = "delta_true_vs_mismatched"


def ensure(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_table(df: pd.DataFrame, stem: Path, md: bool = True) -> None:
    df.to_parquet(stem.with_suffix(".parquet"), index=False)
    df.to_csv(stem.with_suffix(".csv"), index=False)
    if md:
        with stem.with_suffix(".md").open("w", encoding="utf-8") as f:
            f.write(df.to_markdown(index=False))


def rounded(df: pd.DataFrame, digits: int = 3) -> pd.DataFrame:
    out = df.copy()
    cols = out.select_dtypes(include=["float", "float32", "float64"]).columns
    out[cols] = out[cols].round(digits)
    return out


def heatmap(df: pd.DataFrame, family: str, representation: str, metric: str, out: Path) -> None:
    d = df[(df["probe_family"] == family) & (df["representation"] == representation)].copy()
    if d.empty:
        return

    pivot = d.pivot_table(index="variable_id", columns="layer_idx", values=metric, aggfunc="mean").sort_index()

    fig, ax = plt.subplots(figsize=(10, max(9, 0.28 * len(pivot.index) + 2)))
    im = ax.imshow(pivot.values, aspect="auto", interpolation="nearest", vmin=0.5, vmax=1.0)

    ax.set_title(f"{family} | {representation} | {metric}")
    ax.set_xlabel("Layer")
    ax.set_ylabel("Variable ID")
    ax.set_xticks(np.arange(len(pivot.columns)))
    ax.set_xticklabels([str(c) for c in pivot.columns])
    ax.set_yticks(np.arange(len(pivot.index)))
    ax.set_yticklabels([str(i) for i in pivot.index])

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(metric)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def line_by_layer(df: pd.DataFrame, metric: str, out: Path) -> None:
    g = (
        df.groupby(["probe_family", "representation", "layer_idx"], as_index=False)[metric]
        .mean()
        .sort_values(["probe_family", "representation", "layer_idx"])
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    for (family, rep), sub in g.groupby(["probe_family", "representation"]):
        ax.plot(sub["layer_idx"], sub[metric], marker="o", label=f"{family} | {rep}")

    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.set_xlabel("Layer")
    ax.set_ylabel(metric)
    ax.set_title(f"Mean {metric} by layer")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def scatter_activation_vs_text(comparison: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))

    for family, sub in comparison.groupby("probe_family"):
        ax.scatter(sub["best_text_test_auroc"], sub["activation_test_auroc"], label=family, alpha=0.75)
        for _, row in sub.iterrows():
            ax.annotate(str(int(row["variable_id"])), (row["best_text_test_auroc"], row["activation_test_auroc"]), fontsize=7, xytext=(3, 3), textcoords="offset points")

    ax.plot([0.45, 1.0], [0.45, 1.0], linestyle=":", linewidth=1)
    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.axvline(0.5, linestyle="--", linewidth=1)
    ax.set_xlim(0.45, 1.0)
    ax.set_ylim(0.45, 1.0)
    ax.set_xlabel("Best text baseline test AUROC")
    ax.set_ylabel("Best activation probe test AUROC")
    ax.set_title("Activation probe vs best text baseline")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def bar_evidence_status(status: pd.DataFrame, out: Path) -> None:
    counts = status["evidence_status"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(11, max(5, 0.5 * len(counts) + 2)))
    ax.barh(np.arange(len(counts)), counts.values)
    ax.set_yticks(np.arange(len(counts)))
    ax.set_yticklabels(counts.index)
    ax.set_xlabel("Variable count")
    ax.set_title("Evidence status by variable")
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def bar_margins(status: pd.DataFrame, out: Path) -> None:
    if "sentence_activation_minus_text" not in status.columns:
        return

    d = status.sort_values("sentence_activation_minus_text", ascending=True).copy()
    labels = d["variable_id"].astype(int).astype(str).tolist()

    fig, ax = plt.subplots(figsize=(10, max(9, 0.28 * len(d) + 2)))
    ax.barh(np.arange(len(d)), d["sentence_activation_minus_text"])
    ax.axvline(0.0, linestyle="--", linewidth=1)
    ax.axvline(0.05, linestyle=":", linewidth=1)
    ax.set_yticks(np.arange(len(d)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Sentence activation test AUROC - best text baseline test AUROC")
    ax.set_ylabel("Variable ID")
    ax.set_title("Activation margin over text baseline")
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


def write_report(
    candidate: pd.DataFrame,
    best: pd.DataFrame,
    text: pd.DataFrame,
    nulls: pd.DataFrame,
    comparison: pd.DataFrame,
    status: pd.DataFrame,
    out: Path,
) -> None:
    status_counts = status["evidence_status"].value_counts()
    promising = status[status["mechanistic_claim_allowed"] == True].copy() if "mechanistic_claim_allowed" in status.columns else pd.DataFrame()

    with out.open("w", encoding="utf-8") as f:
        f.write("# Strict Raw Activation Probe Analysis\n\n")
        f.write("This report is intentionally conservative. It does not treat high activation AUROC as sufficient evidence.\n\n")

        f.write("## Counts\n\n")
        f.write(f"- Candidate activation probes: `{len(candidate):,}`\n")
        f.write(f"- Best activation probes: `{len(best):,}`\n")
        f.write(f"- Text baseline runs: `{len(text):,}`\n")
        f.write(f"- Null control runs: `{len(nulls):,}`\n")
        f.write(f"- Variables: `{status['variable_id'].nunique():,}`\n\n")

        f.write("## Evidence status counts\n\n")
        f.write(status_counts.to_markdown())
        f.write("\n\n")

        f.write("## Variables currently allowed to move to manual inspection / SAE follow-up\n\n")
        if promising.empty:
            f.write("None under the current conservative criteria.\n\n")
        else:
            cols = [
                "variable_id",
                "variable",
                "sentence_activation_test_auroc",
                "sentence_best_text_test_auroc",
                "sentence_activation_minus_text",
                "sentence_best_layer_idx",
                "delta_mismatch_activation_test_auroc",
                "evidence_status",
            ]
            cols = [c for c in cols if c in promising.columns]
            f.write(rounded(promising[cols]).to_markdown(index=False))
            f.write("\n\n")

        f.write("## Best activation probes\n\n")
        cols = [
            "probe_family",
            "variable_id",
            "variable",
            "representation",
            "layer_idx",
            "val_auroc",
            "test_auroc",
            "test_accuracy",
            "suspiciously_high_test_auroc",
            "possible_overfit",
        ]
        cols = [c for c in cols if c in best.columns]
        f.write(rounded(best[cols].sort_values(["probe_family", "test_auroc"], ascending=[True, False])).to_markdown(index=False))
        f.write("\n\n")

        f.write("## Interpretation rule\n\n")
        f.write("- If text baseline matches or beats activation, the result should be treated as surface-classifiable.\n")
        f.write("- If the best activation layer is 0 or 1 and AUROC is high, artifact risk is high.\n")
        f.write("- If activation is weak, call it weak. Do not rescue it with qualitative interpretation.\n")
        f.write("- A promising result is only a candidate for manual inspection, not a mechanistic claim.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze strict raw activation probe outputs.")
    parser.add_argument(
        "--probe-dir",
        type=Path,
        default=Path("artifacts/probe_data/raw_activation_probes_strict/pythia70m"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/results/raw_activation_probes_strict/pythia70m"),
    )
    args = parser.parse_args()

    probe_dir = args.probe_dir
    out = args.output_dir
    tables = out / "tables"
    figs = out / "figures"
    ensure(tables)
    ensure(figs)

    paths = {
        "candidate": probe_dir / "candidate_activation_probe_results.parquet",
        "best": probe_dir / "best_activation_probe_results.parquet",
        "text": probe_dir / "text_baseline_results.parquet",
        "null": probe_dir / "null_label_shuffle_results.parquet",
        "comparison": probe_dir / "activation_vs_text_and_null_comparison.parquet",
        "status": probe_dir / "evidence_status_by_variable.parquet",
    }

    for name, path in paths.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing {name}: {path}")

    candidate = pd.read_parquet(paths["candidate"])
    best = pd.read_parquet(paths["best"])
    text = pd.read_parquet(paths["text"])
    nulls = pd.read_parquet(paths["null"])
    comparison = pd.read_parquet(paths["comparison"])
    status = pd.read_parquet(paths["status"])

    save_table(candidate, tables / "candidate_activation_probe_results", md=False)
    save_table(best, tables / "best_activation_probe_results", md=True)
    save_table(text, tables / "text_baseline_results", md=False)
    save_table(nulls, tables / "null_label_shuffle_results", md=False)
    save_table(comparison, tables / "activation_vs_text_and_null_comparison", md=True)
    save_table(status, tables / "evidence_status_by_variable", md=True)

    compact_cols = [
        "variable_id",
        "variable",
        "evidence_status",
        "mechanistic_claim_allowed",
        "sentence_activation_test_auroc",
        "sentence_best_text_test_auroc",
        "sentence_activation_minus_text",
        "sentence_best_layer_idx",
        "delta_mismatch_activation_test_auroc",
        "delta_mismatch_best_text_test_auroc",
        "recommended_next_action",
    ]
    compact_cols = [c for c in compact_cols if c in status.columns]
    save_table(rounded(status[compact_cols]), tables / "evidence_status_compact", md=True)

    for family in sorted(candidate["probe_family"].unique()):
        for rep in sorted(candidate["representation"].unique()):
            heatmap(candidate, family, rep, "test_auroc", figs / f"heatmap_{family}_{rep}_test_auroc.png")

    line_by_layer(candidate, "test_auroc", figs / "mean_test_auroc_by_layer.png")
    line_by_layer(candidate, "val_auroc", figs / "mean_val_auroc_by_layer.png")
    scatter_activation_vs_text(comparison, figs / "activation_vs_text_test_auroc.png")
    bar_evidence_status(status, figs / "evidence_status_counts.png")
    bar_margins(status, figs / "sentence_activation_margin_over_text.png")

    report = out / "strict_probe_analysis_report.md"
    write_report(candidate, best, text, nulls, comparison, status, report)

    manifest = {
        "probe_dir": str(probe_dir),
        "output_dir": str(out),
        "tables": str(tables),
        "figures": str(figs),
        "report": str(report),
        "num_candidate_activation_probes": int(len(candidate)),
        "num_best_activation_probes": int(len(best)),
        "num_text_baselines": int(len(text)),
        "num_null_controls": int(len(nulls)),
        "evidence_status_counts": status["evidence_status"].value_counts().to_dict(),
    }
    with (out / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("Strict analysis complete.")
    print(f"Report: {report}")
    print(f"Figures: {figs}")
    print(f"Tables: {tables}")


if __name__ == "__main__":
    main()
