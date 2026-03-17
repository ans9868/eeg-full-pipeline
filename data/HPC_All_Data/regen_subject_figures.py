#!/usr/bin/env python3
"""
Regenerate all subject-level evaluation figures with canonical styling.
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker
from pathlib import Path

matplotlib.use("Agg")

OUT_DIR = Path(__file__).parent / "paper_subject_eval_outputs"
MODEL_ORDER = ["MLP", "KNN", "SVM", "XGBoost"]
EXP_MODEL_KEYS = ["experiment", "pipeline", "strategy", "P", "model"]
MODEL_COLORS = {
    "MLP": "#1f77b4",
    "XGBoost": "#ff7f0e",
    "SVM": "#2ca02c",
    "KNN": "#d62728",
}
STRATEGY_MARKERS = {"Random-50": "o", "Uniform-12": "s"}


def display_pipeline_name(pipeline: str) -> str:
    """Pretty display label for pipeline names in figure titles."""
    return "F-test" if pipeline == "FTest" else pipeline


def select_best_hp(df, criterion="epoch"):
    acc_col = "epoch_acc" if criterion == "epoch" else "subject_acc"
    rows = []
    for _k, grp in df.groupby(EXP_MODEL_KEYS):
        best_hp = grp.groupby("hyperparams")[acc_col].median().idxmax()
        best_rows = grp[grp["hyperparams"] == best_hp].copy()
        best_rows["best_hp"] = best_hp
        rows.append(best_rows)
    return pd.concat(rows, ignore_index=True)


def _boxplot_panel(ax, data_by_model, model_order, title, ylabel,
                   show_xlabel=True, P=6):
    """Single panel of small-multiples figure with canonical LPSO-style boxplots."""
    for i, model in enumerate(model_order):
        vals_frac = np.array(data_by_model.get(model, []))
        if len(vals_frac) == 0:
            continue
        vals = vals_frac * P
        col = MODEL_COLORS.get(model, "#666666")

        bp = ax.boxplot(
            vals, positions=[i], widths=0.6,
            patch_artist=True, showmeans=False, showfliers=False,
            medianprops=dict(color="black", linewidth=1.2),
            whiskerprops=dict(color="black", linewidth=1.2),
            capprops=dict(color="black", linewidth=1.2),
        )
        for patch in bp["boxes"]:
            patch.set_facecolor(col)
            patch.set_alpha(0.7)
            patch.set_edgecolor("black")
            patch.set_linewidth(1.2)

        # Adaptive jitter: less spread near the mean
        mean_val = np.mean(vals)
        distances = np.abs(vals - mean_val)
        max_d = np.max(distances) if np.max(distances) > 0 else 1.0
        jit_scales = 1.0 / (1.0 + 2.0 * (distances / max_d))
        jitter = np.random.normal(0, 0.03, len(vals)) * jit_scales
        ax.scatter(
            i + jitter, vals,
            alpha=0.5, s=20, color=col,
            edgecolors="black", linewidth=0.5, zorder=10,
        )

    ax.axhline(P / 2, color="gray", linestyle=":", alpha=0.6, linewidth=1.0,
               label=f"Chance (P/2 = {P//2})")
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.set_xlim(-0.5, len(model_order) - 0.5)
    ax.set_xticks(range(len(model_order)))
    ax.set_xticklabels(model_order if show_xlabel else [""] * len(model_order),
                       fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_ylim(-0.4, P + 0.4)
    ax.set_yticks(range(P + 1))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def make_small_multiples(best_df, P_filter, out_path):
    """Box-plots: one subplot per (pipeline x strategy). Y = # subjects correct."""
    sub = best_df[best_df["P"] == P_filter]
    strategies = [s for s in ["Uniform-12", "Random-50"]
                  if s in sub["strategy"].unique()]
    pipelines = [p for p in ["FTest", "PCA"]
                 if p in sub["pipeline"].unique()]

    # Preferred diagnostic layout for P=2 with one strategy available:
    # side-by-side panels (FTest left, PCA right) instead of vertical stacking.
    side_by_side = (len(strategies) == 1 and len(pipelines) == 2)

    if side_by_side:
        nrows, ncols = 1, 2
    else:
        nrows, ncols = len(pipelines), len(strategies)

    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(4.5 * ncols, 4.5 * nrows),
        squeeze=False,
    )
    fig.suptitle(
        f"Subject-level classification  (P={P_filter} subjects/fold,  "
        f"HP selected by median epoch accuracy)\n"
        f"Y = subjects correctly classified;  dotted line = chance level (P/2)",
        fontsize=11, y=1.02,
    )

    if side_by_side:
        strategy = strategies[0]
        for ci, pipeline in enumerate(pipelines):
            panel = sub[(sub["pipeline"] == pipeline) & (sub["strategy"] == strategy)]
            data_by_model = {
                m: panel.loc[panel["model"] == m, "subject_acc"].values
                for m in MODEL_ORDER
            }
            _boxplot_panel(
                axes[0][ci], data_by_model, MODEL_ORDER,
                title=f"{display_pipeline_name(pipeline)}  —  {strategy}",
                ylabel=(f"Subjects correctly classified (of {P_filter})"
                        if ci == 0 else ""),
                show_xlabel=True,
                P=P_filter,
            )
    else:
        for ri, pipeline in enumerate(pipelines):
            for ci, strategy in enumerate(strategies):
                panel = sub[(sub["pipeline"] == pipeline) & (sub["strategy"] == strategy)]
                data_by_model = {
                    m: panel.loc[panel["model"] == m, "subject_acc"].values
                    for m in MODEL_ORDER
                }
                _boxplot_panel(
                    axes[ri][ci], data_by_model, MODEL_ORDER,
                    title=f"{display_pipeline_name(pipeline)}  —  {strategy}",
                    ylabel=(f"Subjects correctly classified (of {P_filter})"
                            if ci == 0 else ""),
                    show_xlabel=(ri == nrows - 1),
                    P=P_filter,
                )

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"  Saved: {out_path.name}")


def fig_epoch_vs_subject_scatter(best_df, P_filter, out_path):
    """
    Fold-level scatter: epoch accuracy vs # subjects correctly classified.
    No colour coding — single neutral colour for all points.
    """
    sub = best_df[best_df["P"] == P_filter]
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle(
        f"Epoch accuracy vs subjects correctly classified per fold  (P={P_filter})\n"
        f"Each point = one fold (best HP per model).  Dashed diagonal = equal performance.",
        fontsize=11,
    )

    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax = axes[ai]
        panel = sub[sub["pipeline"] == pipeline]
        if panel.empty:
            ax.set_title(f"{pipeline} — no data")
            continue

        epoch_vals = panel["epoch_acc"].values
        subj_counts = (panel["subject_acc"] * P_filter).round().astype(int).values

        ax.scatter(epoch_vals, subj_counts,
                   s=22, alpha=0.55, color="#444444", zorder=2)

        x_lo = max(0.0, float(epoch_vals.min()) - 0.03)
        x_hi = min(1.0, float(epoch_vals.max()) + 0.03)
        ax.plot([x_lo, x_hi], [x_lo * P_filter, x_hi * P_filter],
                "k--", linewidth=1.2, alpha=0.55, label="subject acc = epoch acc")

        ax.set_title(display_pipeline_name(pipeline), fontsize=10, fontweight="bold")
        ax.set_xlabel("Epoch accuracy (fold-level)", fontsize=9)
        if ai == 0:
            ax.set_ylabel(f"Subjects correctly classified (of {P_filter})", fontsize=9)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
        ax.set_ylim(-0.4, P_filter + 0.4)
        ax.set_yticks(range(P_filter + 1))
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"  Saved: {out_path.name}")


def fig_delta_distribution(best_df, out_path):
    """Violin plots of (subject_acc - epoch_acc) by strategy."""
    strategy_colors = {"Random-50": "#2166ac", "Uniform-12": "#f4a460"}

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    fig.suptitle(
        "Subject accuracy minus epoch accuracy per fold\n"
        "Negative = epoch accuracy over-estimates subject-level performance",
        fontsize=11,
    )

    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax = axes[ai]
        panel = best_df[best_df["pipeline"] == pipeline]
        data_parts, labels_list, colors_list = [], [], []

        for strat in ["Random-50", "Uniform-12"]:
            sub = panel[panel["strategy"] == strat]
            if sub.empty:
                continue
            data_parts.append(sub["subject_minus_epoch"].values)
            labels_list.append(strat)
            colors_list.append(strategy_colors.get(strat, "#aaa"))

        if data_parts:
            parts = ax.violinplot(data_parts,
                                  positions=range(len(data_parts)),
                                  showmedians=True, showextrema=True)
            for pc, col in zip(parts["bodies"], colors_list):
                pc.set_facecolor(col)
                pc.set_alpha(0.65)
            ax.set_xticks(range(len(labels_list)))
            ax.set_xticklabels(labels_list, fontsize=9)

        ax.axhline(0, color="black", linewidth=1.2, linestyle="--", alpha=0.7)
        ax.set_title(display_pipeline_name(pipeline), fontsize=10, fontweight="bold")
        ax.set_ylabel("subject_acc − epoch_acc")
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
        ax.grid(axis="y", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"  Saved: {out_path.name}")


def fig_aggregate_epoch_vs_subject(merged_df, P_filter, out_path):
    """
    Aggregate scatter — one point per (model x hyperparams) configuration.

    X = mean epoch accuracy (%) across ALL folds for that config + strategy + pipeline.
    Y = total subjects correctly classified / total subjects × 100 (%).

    Colour  = model (canonical project colours).
    Marker  = strategy  (circle = Random-50,  square = Uniform-12).
    """
    sub = merged_df[merged_df["P"] == P_filter].copy()

    agg_rows = []
    for (pipeline, strategy, model, hyperparams), grp in sub.groupby(
            ["pipeline", "strategy", "model", "hyperparams"]):
        mean_epoch_pct = grp["epoch_acc"].mean() * 100
        total_subjects = grp["n_subjects_fold"].sum()
        subjects_correct = (grp["subject_acc"] * grp["n_subjects_fold"]).sum()
        pct_correct = (subjects_correct / total_subjects * 100
                       if total_subjects > 0 else 0.0)
        agg_rows.append({
            "pipeline": pipeline,
            "strategy": strategy,
            "model": model,
            "mean_epoch_pct": mean_epoch_pct,
            "pct_subjects_correct": pct_correct,
            "total_subjects": int(total_subjects),
        })
    agg_df = pd.DataFrame(agg_rows)

    n_random = sub[sub["strategy"] == "Random-50"]["fold_id"].nunique() if "fold_id" in sub.columns else 50
    n_uniform = sub[sub["strategy"] == "Uniform-12"]["fold_id"].nunique() if "fold_id" in sub.columns else 12

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.suptitle(
        f"Aggregate subject accuracy vs mean epoch accuracy  (P={P_filter} subjects/fold)\n"
        f"One point = one model × hyperparameter config, aggregated over all folds.\n"
        f"Circle = Random-50 folds,   Square = Uniform-12 folds",
        fontsize=10, y=1.04,
    )

    added_labels = set()
    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax = axes[ai]
        panel = agg_df[agg_df["pipeline"] == pipeline]
        if panel.empty:
            ax.set_title(f"{display_pipeline_name(pipeline)} — no data")
            continue

        for model in MODEL_ORDER:
            col = MODEL_COLORS.get(model, "#666666")
            for strat, marker in STRATEGY_MARKERS.items():
                pts = panel[(panel["model"] == model) & (panel["strategy"] == strat)]
                if pts.empty:
                    continue
                lkey = (model, strat)
                label = f"{model} — {strat}" if lkey not in added_labels else ""
                ax.scatter(
                    pts["mean_epoch_pct"], pts["pct_subjects_correct"],
                    color=col, marker=marker, s=55, alpha=0.82,
                    edgecolors="black", linewidth=0.5, zorder=3,
                    label=label,
                )
                if label:
                    added_labels.add(lkey)

        # Diagonal reference line (y = x means subject acc == epoch acc)
        lo = panel["mean_epoch_pct"].min() - 3
        hi = panel["mean_epoch_pct"].max() + 3
        ax.plot([lo, hi], [lo, hi], "k--", lw=1.0, alpha=0.40,
                label="y = x  (subject acc = epoch acc)" if ai == 0 else "")

        ax.axhline(50, color="gray", linestyle=":", alpha=0.5, linewidth=1.0,
                   label="Chance (50 %)" if ai == 0 else "")

        ax.set_title(display_pipeline_name(pipeline), fontsize=11, fontweight="bold")
        ax.set_xlabel("Mean epoch accuracy across folds (%)", fontsize=10)
        if ai == 0:
            ax.set_ylabel(
                f"Subjects correctly classified (%)\n"
                f"(aggregated over all P={P_filter} folds)",
                fontsize=10,
            )
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=100))
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=100))
        ax.grid(alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Shared legend below both panels
    handles, labels = [], []
    for ax in axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l and l not in labels:
                handles.append(h)
                labels.append(l)
    fig.legend(
        handles, labels,
        loc="lower center", bbox_to_anchor=(0.5, -0.12),
        ncol=4, fontsize=8.5, framealpha=0.88, edgecolor="gray",
    )

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"  Saved: {out_path.name}")


if __name__ == "__main__":
    # ── Load ──────────────────────────────────────────────────────────────────
    merged = pd.read_csv(OUT_DIR / "fold_epoch_vs_subject_merged.csv")
    print(f"Loaded merged data: {len(merged):,} rows")
    print(f"  Strategies : {sorted(merged['strategy'].unique())}")
    print(f"  Pipelines  : {sorted(merged['pipeline'].unique())}")
    print(f"  P values   : {sorted(merged['P'].unique())}")
    print(f"  Models     : {sorted(merged['model'].unique())}")

    np.random.seed(42)
    best = select_best_hp(merged, "epoch")
    print(f"Best-HP selected: {len(best):,} rows\n")

    # ── 1. Small multiples  P=6 ──────────────────────────────────────────────
    make_small_multiples(
        best, 6,
        OUT_DIR / "fig_subject_accuracy_small_multiples_P6.png",
    )

    # ── 2. Small multiples  P=2 ──────────────────────────────────────────────
    if not best[best["P"] == 2].empty:
        make_small_multiples(
            best, 2,
            OUT_DIR / "fig_subject_accuracy_small_multiples_P2.png",
        )

    # ── 3. Scatter  P=6 ──────────────────────────────────────────────────────
    fig_epoch_vs_subject_scatter(
        best, 6,
        OUT_DIR / "fig_epoch_vs_subject_scatter_P6.png",
    )

    # ── 4. Scatter  P=2 ──────────────────────────────────────────────────────
    if not best[best["P"] == 2].empty:
        fig_epoch_vs_subject_scatter(
            best, 2,
            OUT_DIR / "fig_epoch_vs_subject_scatter_P2.png",
        )

    # ── 5. Delta distribution (unchanged) ────────────────────────────────────
    fig_delta_distribution(
        best,
        OUT_DIR / "fig_subject_minus_epoch_delta_distribution.png",
    )

    # ── 6. NEW: aggregate scatter  P=6 ───────────────────────────────────────
    fig_aggregate_epoch_vs_subject(
        merged, 6,
        OUT_DIR / "fig_aggregate_epoch_vs_subject_P6.png",
    )

    print("\nAll figures regenerated.")
