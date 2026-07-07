from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


SENTENCE_FAMILY = "sentence_basis_changed"
DELTA_DIRECTION_FAMILY = "delta_direction_basis_to_changed"


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


def merge_viability_results(status: pd.DataFrame, viability_path: Path | None) -> pd.DataFrame:
    if viability_path is None:
        return status
    if not viability_path.exists():
        raise FileNotFoundError(f"Missing learned activation direction viability file: {viability_path}")

    if viability_path.suffix == ".parquet":
        viability = pd.read_parquet(viability_path)
    else:
        viability = pd.read_csv(viability_path)

    required = {"variable_id", "learned_activation_direction_viability_pass"}
    missing = required - set(viability.columns)
    if missing:
        raise ValueError(f"Viability file missing columns: {sorted(missing)}")

    viability_cols = [c for c in viability.columns if c != "variable"]
    out = status.drop(columns=[c for c in viability_cols if c in status.columns and c != "variable_id"], errors="ignore")
    out = out.merge(viability[viability_cols], on="variable_id", how="left")

    pass_col = "learned_activation_direction_viability_pass"
    if pass_col in out.columns:
        out["learned_activation_direction_viability_status"] = np.where(
            out[pass_col].fillna(False),
            "passed",
            np.where(out[pass_col].isna(), "not_run", "failed"),
        )
        l1 = out.get("level_1_activation_recoverability_pass", False)
        l3 = out.get("level_3_directional_consistency_pass", False)
        l4 = out.get("level_4_split_generalization_pass", False)
        l5 = out[pass_col].fillna(False)
        out["mechanistic_claim_allowed"] = (l1 & l3 & l4 & l5).astype(bool)
        out["evidence_status"] = np.where(
            out["mechanistic_claim_allowed"],
            "levels1_3_4_5_passed_direction_viability_candidate",
            out["evidence_status"],
        )
    return out

def write_report(
    candidate: pd.DataFrame,
    best: pd.DataFrame,
    text: pd.DataFrame,
    nulls: pd.DataFrame,
    comparison: pd.DataFrame,
    status: pd.DataFrame,
    split_profile: pd.DataFrame | None,
    out: Path,
) -> None:
    status_counts = status["evidence_status"].value_counts()
    ready_col = "ready_for_learned_activation_direction_viability"
    ready = status[status.get(ready_col, False) == True].copy() if ready_col in status.columns else pd.DataFrame()
    mechanistic = status[status["mechanistic_claim_allowed"] == True].copy() if "mechanistic_claim_allowed" in status.columns else pd.DataFrame()

    with out.open("w", encoding="utf-8") as f:
        f.write("# Raw Activation Probe Analysis\n\n")
        f.write("This report uses a five-level evidence ladder. Text baselines are diagnostic, not an automatic rejection gate, because many linguistic variables are intentionally surface-visible.\n\n")

        f.write("## Counts\n\n")
        f.write(f"- Candidate activation probes: `{len(candidate):,}`\n")
        f.write(f"- Best activation probes: `{len(best):,}`\n")
        f.write(f"- Text baseline runs: `{len(text):,}`\n")
        f.write(f"- Null control runs: `{len(nulls):,}`\n")
        f.write(f"- Variables: `{status['variable_id'].nunique():,}`\n\n")

        f.write("## Evidence ladder\n\n")
        f.write("1. **Activation recoverability:** sentence-level basis vs changed classification from activations.\n")
        f.write("2. **Text/artifact control:** records whether text baselines also solve the task. This narrows the claim but does not automatically reject surface-visible variables.\n")
        f.write("3. **Directional consistency:** basis → changed deltas must form a stable held-out direction.\n")
        f.write("4. **Split generalization:** successful performance must occur on held-out marker families or lexical domains.\n")
        f.write("5. **Learned activation direction viability:** the learned direction must move held-out basis activations toward the changed class under the selected probe.\n\n")

        f.write("## Evidence status counts\n\n")
        f.write(status_counts.to_markdown())
        f.write("\n\n")

        f.write("## Variables ready for learned activation direction viability\n\n")
        if ready.empty:
            f.write("None.\n\n")
        else:
            cols = [
                "variable_id",
                "variable",
                "sentence_activation_test_auroc",
                "delta_direction_activation_test_auroc",
                "level_2_text_evidence_category",
                "split_control_strength",
                "sentence_best_layer_idx",
                "early_layer_artifact_risk",
                "evidence_status",
            ]
            cols = [c for c in cols if c in ready.columns]
            f.write(rounded(ready[cols]).to_markdown(index=False))
            f.write("\n\n")

        f.write("## Variables with learned activation direction viability passed\n\n")
        if mechanistic.empty:
            f.write("None yet. This is expected unless a viability file was supplied.\n\n")
        else:
            cols = [
                "variable_id",
                "variable",
                "sentence_activation_test_auroc",
                "delta_direction_activation_test_auroc",
                "direction_effect_mean",
                "direction_effect_positive_rate",
                "evidence_status",
            ]
            cols = [c for c in cols if c in mechanistic.columns]
            f.write(rounded(mechanistic[cols]).to_markdown(index=False))
            f.write("\n\n")

        if split_profile is not None and not split_profile.empty:
            f.write("## Split-control profile\n\n")
            cols = [
                "variable_id",
                "variable",
                "split_control_strength",
                "test_has_heldout_marker_family",
                "test_has_heldout_lexical_domain",
                "test_marker_train_overlap_count",
                "test_lexical_train_overlap_count",
            ]
            cols = [c for c in cols if c in split_profile.columns]
            f.write(rounded(split_profile[cols]).to_markdown(index=False))
            f.write("\n\n")

        if "sentence_layer_stability_layers_above_threshold_count" in status.columns:
            f.write("## Layer-stability profile\n\n")
            cols = [
                "variable_id",
                "variable",
                "sentence_layer_stability_best_layer_idx",
                "sentence_layer_stability_best_representation",
                "sentence_layer_stability_layers_above_threshold_count",
                "sentence_layer_stability_max_adjacent_layers_above_threshold",
                "sentence_layer_stability_signal_beyond_layer_2",
                "delta_direction_layer_stability_best_layer_idx",
                "delta_direction_layer_stability_layers_above_threshold_count",
                "delta_direction_layer_stability_max_adjacent_layers_above_threshold",
                "delta_direction_layer_stability_signal_beyond_layer_2",
            ]
            cols = [c for c in cols if c in status.columns]
            f.write(rounded(status[cols]).to_markdown(index=False))
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
        f.write("- Strong text baselines mean the result is surface-visible, not useless. The claim becomes narrower: activation recoverability of a surface-visible linguistic cue.\n")
        f.write("- Text baselines no longer kill variables by themselves.\n")
        f.write("- Early-layer wins are flagged because they may reflect tokenization/orthography rather than abstract representation.\n")
        f.write("- Level 5 is never inferred from probe AUROC; it requires an explicit learned-direction viability result.\n")

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze raw activation probe outputs.")
    parser.add_argument(
        "--probe-dir",
        type=Path,
        default=Path("artifacts/probe_data/raw_activation_probes_strict/xglm564m"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/results/raw_activation_probes_strict/xglm564m"),
    )
    parser.add_argument(
        "--learned-activation-direction-viability",
        type=Path,
        default=None,
        help="Optional CSV/parquet from the learned activation direction viability check.",
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
        "split_profile": probe_dir / "split_control_profile_by_variable.parquet",
        "layer_stability": probe_dir / "layer_stability_by_variable.parquet",
    }

    for name, path in paths.items():
        if name in {"split_profile", "layer_stability"}:
            continue
        if not path.exists():
            raise FileNotFoundError(f"Missing {name}: {path}")

    candidate = pd.read_parquet(paths["candidate"])
    best = pd.read_parquet(paths["best"])
    text = pd.read_parquet(paths["text"])
    nulls = pd.read_parquet(paths["null"])
    comparison = pd.read_parquet(paths["comparison"])
    status = pd.read_parquet(paths["status"])
    status = merge_viability_results(status, args.learned_activation_direction_viability)
    split_profile = pd.read_parquet(paths["split_profile"]) if paths["split_profile"].exists() else pd.DataFrame()
    layer_stability = pd.read_parquet(paths["layer_stability"]) if paths["layer_stability"].exists() else pd.DataFrame()

    save_table(candidate, tables / "candidate_activation_probe_results", md=False)
    save_table(best, tables / "best_activation_probe_results", md=True)
    save_table(text, tables / "text_baseline_results", md=False)
    save_table(nulls, tables / "null_label_shuffle_results", md=False)
    save_table(comparison, tables / "activation_vs_text_and_null_comparison", md=True)
    save_table(status, tables / "evidence_status_by_variable", md=True)
    if not split_profile.empty:
        save_table(split_profile, tables / "split_control_profile_by_variable", md=True)
    if not layer_stability.empty:
        save_table(layer_stability, tables / "layer_stability_by_variable", md=True)

    compact_cols = [
        "variable_id",
        "variable",
        "evidence_status",
        "mechanistic_claim_allowed",
        "sentence_activation_test_auroc",
        "sentence_best_text_test_auroc",
        "level_1_activation_recoverability_pass",
        "level_2_text_evidence_category",
        "level_3_directional_consistency_pass",
        "level_4_split_generalization_pass",
        "learned_activation_direction_viability_status",
        "ready_for_learned_activation_direction_viability",
        "sentence_activation_minus_text",
        "sentence_activation_test_auroc_ci_lower",
        "sentence_activation_test_auroc_ci_upper",
        "sentence_best_layer_idx",
        "sentence_layer_stability_layers_above_threshold_count",
        "sentence_layer_stability_max_adjacent_layers_above_threshold",
        "sentence_layer_stability_signal_beyond_layer_2",
        "delta_direction_activation_test_auroc",
        "delta_direction_best_text_test_auroc",
        "split_control_strength",
        "claim_scope",
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

    report = out / "probe_analysis_report.md"
    write_report(candidate, best, text, nulls, comparison, status, split_profile, report)

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
        "learned_activation_direction_viability": str(args.learned_activation_direction_viability) if args.learned_activation_direction_viability else None,
    }
    with (out / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("Strict analysis complete.")
    print(f"Report: {report}")
    print(f"Figures: {figs}")
    print(f"Tables: {tables}")


if __name__ == "__main__":
    main()
