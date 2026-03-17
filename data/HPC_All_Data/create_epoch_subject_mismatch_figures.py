#!/usr/bin/env python3
"""
Diagnostic figures: Epoch-accuracy vs Subject-label-accuracy mismatch (Trap 3).

Epoch accuracy reweights subjects by epoch count (high-epoch subjects dominate).
Subject-label accuracy treats every subject equally (majority vote per subject).

Figures produced
----------------
A  Conceptual synthetic illustration of the mismatch mechanism
B  Real-data scatter: epoch_acc vs subject_acc per fold (all experiments)
C  Distribution of (epoch_acc - subject_acc) per fold — violin by pipeline/strategy
D  Subject epoch-count variability within folds (imbalance)
E  Epoch-count imbalance ratio vs mismatch magnitude (scatter)
F  Per-subject epoch counts vs classification outcome (boxplot)
G  "Hall of shame": top-20 folds with largest epoch > subject divergence
H  Per-experiment summary: mean epoch_acc vs mean subject_acc side-by-side
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from pathlib import Path

matplotlib.use("Agg")

BASE    = Path(__file__).parent
PREDS   = BASE / "paper_subject_eval_outputs" / "per_subject_fold_predictions.csv"
MERGED  = BASE / "paper_subject_eval_outputs" / "fold_epoch_vs_subject_merged.csv"
OUTDIR  = BASE / "paper_subject_eval_outputs" / "epoch_subject_mismatch_figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

PIPE_COLORS = {"FTest": "#2166ac", "PCA": "#d6604d"}
STRAT_COLORS = {"Random-50": "#4dac26", "Uniform-12": "#b8860b"}
EXP_COLORS = {
    "ANOVA_L_6_Random": "#1f77b4", "PCA_L_6_Random": "#ff7f0e",
    "ANOVA_L_2_Random": "#2ca02c", "PCA_L_2_Random": "#d62728",
    "ANOVA_L_6_Uniform": "#9467bd", "PCA_L_6_Uniform": "#8c564b",
}

np.random.seed(42)

# ── Load data ─────────────────────────────────────────────────────────────────
merged = pd.read_csv(MERGED)
preds  = pd.read_csv(PREDS)

print(f"Merged: {len(merged):,} fold rows")
print(f"Preds : {len(preds):,} subject rows")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure A — Conceptual synthetic illustration
# ═══════════════════════════════════════════════════════════════════════════════
def fig_A_conceptual():
    """
    5 synthetic subjects.  Two 'rich' subjects have 800 epochs and 85% accuracy.
    Three 'poor' subjects have 150 epochs and 25% accuracy.

    Epoch accuracy (weighted)  ≈ 0.85×1600/(1600+450) + 0.25×450/(1600+450) ≈ 71%
    Subject accuracy (unweighted) = (2×0.85 + 3×0.25)/5 = 49%
    """
    subjects   = ["Sub-A\n(800 ep)", "Sub-B\n(800 ep)",
                  "Sub-C\n(150 ep)", "Sub-D\n(150 ep)", "Sub-E\n(150 ep)"]
    n_epochs   = [800, 800, 150, 150, 150]
    subj_acc   = [0.85, 0.85, 0.25, 0.25, 0.25]
    colors     = ["#90EE90" if a > 0.5 else "#FF6B6B" for a in subj_acc]

    total_ep     = sum(n_epochs)
    epoch_acc    = sum(a * n / total_ep for a, n in zip(subj_acc, n_epochs))
    subject_acc  = np.mean(subj_acc)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle(
        "Conceptual illustration: epoch accuracy misleads subject-level decisions\n"
        "Epoch accuracy weights subjects by epoch count; subject accuracy treats every subject equally",
        fontsize=11, fontweight="bold",
    )

    # Left: per-subject accuracy bars
    ax = axes[0]
    bars = ax.bar(range(5), [a * 100 for a in subj_acc], color=colors,
                  edgecolor="black", alpha=0.85, width=0.6)
    ax.axhline(50, color="red", linestyle="--", linewidth=1.5, label="50% chance")
    ax.set_xticks(range(5)); ax.set_xticklabels(subjects, fontsize=9)
    ax.set_ylabel("Per-subject accuracy (%)", fontsize=10)
    ax.set_title("Step 1: Per-subject accuracy", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 105); ax.legend(fontsize=8)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    # Middle: epoch count bars
    ax = axes[1]
    ep_colors = ["#4a9ede" if n >= 500 else "#f5a623" for n in n_epochs]
    ax.bar(range(5), n_epochs, color=ep_colors, edgecolor="black", alpha=0.85, width=0.6)
    ax.set_xticks(range(5)); ax.set_xticklabels(subjects, fontsize=9)
    ax.set_ylabel("Number of epochs", fontsize=10)
    ax.set_title("Step 2: Epoch count per subject\n(determines reweighting)", fontsize=10, fontweight="bold")
    legend_ep = [
        mpatches.Patch(facecolor="#4a9ede", label="High-epoch subjects (800)"),
        mpatches.Patch(facecolor="#f5a623", label="Low-epoch subjects (150)"),
    ]
    ax.legend(handles=legend_ep, fontsize=8)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    # Right: the two aggregate metrics compared
    ax = axes[2]
    metric_vals = [epoch_acc * 100, subject_acc * 100]
    metric_cols = ["#4a9ede", "#e07b39"]
    bars = ax.bar([0, 1], metric_vals, color=metric_cols,
                  edgecolor="black", alpha=0.85, width=0.5)
    ax.axhline(50, color="red", linestyle="--", linewidth=1.5, label="50% chance")
    ax.set_xticks([0, 1])
    ax.set_xticklabels([
        f"Epoch accuracy\n(weighted by epoch count)\n→ {epoch_acc*100:.1f}%",
        f"Subject accuracy\n(equal weight per subject)\n→ {subject_acc*100:.1f}%",
    ], fontsize=9)
    ax.set_ylabel("Accuracy (%)", fontsize=10)
    ax.set_title(
        f"Step 3: The mismatch\nΔ = {(epoch_acc - subject_acc)*100:.1f} pp\n"
        f"(epoch overestimates by {(epoch_acc - subject_acc)*100:.1f} pp)",
        fontsize=10, fontweight="bold",
    )
    ax.set_ylim(0, 105)
    for bar, val in zip(bars, metric_vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1.5,
                f"{val:.1f}%", ha="center", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = OUTDIR / "figA_conceptual_mismatch.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure B — Real-data scatter: epoch_acc vs subject_acc per fold
# ═══════════════════════════════════════════════════════════════════════════════
def fig_B_scatter():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.suptitle(
        "Real data: epoch accuracy vs subject-label accuracy per fold\n"
        "Points above the diagonal → epoch accuracy over-estimates subject performance",
        fontsize=11, fontweight="bold",
    )
    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax  = axes[ai]
        sub = merged[merged["pipeline"] == pipeline]
        for exp, grp in sub.groupby("experiment"):
            col = EXP_COLORS.get(exp, "#888")
            ax.scatter(grp["epoch_acc"] * 100, grp["subject_acc"] * 100,
                       alpha=0.35, s=18, color=col, label=exp, zorder=2)
        lo, hi = 0, 105
        ax.plot([lo, hi], [lo, hi], "k--", lw=1.2, alpha=0.5, label="y = x (perfect agreement)")
        ax.axhline(50, color="gray", linestyle=":", alpha=0.4, linewidth=1)
        ax.axvline(50, color="gray", linestyle=":", alpha=0.4, linewidth=1)
        ax.set_xlabel("Epoch accuracy per fold (%)", fontsize=10)
        if ai == 0:
            ax.set_ylabel("Subject-label accuracy per fold (%)", fontsize=10)
        ax.set_title(f"{'ANOVA (FTest)' if pipeline == 'FTest' else 'PCA'} pipeline",
                     fontsize=10, fontweight="bold")
        ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
        ax.legend(fontsize=7, ncol=1, loc="upper left")
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = OUTDIR / "figB_scatter_epoch_vs_subject.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure C — Distribution of mismatch (epoch_acc - subject_acc)
# ═══════════════════════════════════════════════════════════════════════════════
def fig_C_mismatch_distribution():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        "Distribution of fold-level mismatch: epoch_acc − subject_acc (%)\n"
        "Positive = epoch accuracy over-estimates; Negative = epoch under-estimates",
        fontsize=11, fontweight="bold",
    )
    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax  = axes[ai]
        sub = merged[merged["pipeline"] == pipeline].copy()
        sub["mismatch_pct"] = sub["subject_minus_epoch"] * -100  # epoch-subject (positive = epoch > subject)
        groups, labels, colors_v = [], [], []
        for strat in ["Random-50", "Uniform-12"]:
            g = sub[sub["strategy"] == strat]["mismatch_pct"].dropna()
            if g.empty: continue
            groups.append(g.values); labels.append(strat)
            colors_v.append(STRAT_COLORS.get(strat, "#888"))
        if groups:
            vp = ax.violinplot(groups, positions=range(len(groups)),
                               showmedians=True, showextrema=True)
            for body, col in zip(vp["bodies"], colors_v):
                body.set_facecolor(col); body.set_alpha(0.6)
            ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=10)
        ax.axhline(0, color="black", linewidth=1.5, linestyle="--", alpha=0.8,
                   label="No mismatch (epoch = subject)")
        ax.set_ylabel("epoch_acc − subject_acc (pp)", fontsize=10)
        ax.set_title(f"{'ANOVA (FTest)' if pipeline == 'FTest' else 'PCA'} pipeline",
                     fontsize=10, fontweight="bold")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:+.0f}%"))
        ax.legend(fontsize=9)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    out = OUTDIR / "figC_mismatch_distribution.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure D — Epoch-count variability within folds
# ═══════════════════════════════════════════════════════════════════════════════
def fig_D_epoch_count_variability():
    """Show how unequal epoch counts create the reweighting problem."""
    # Compute per-fold epoch-count range (max/min) and std
    fold_stats = preds.groupby(
        ["experiment", "pipeline", "strategy", "fold_id", "model", "task_id"]
    )["n_epochs"].agg(
        n_min="min", n_max="max", n_std="std", n_mean="mean"
    ).reset_index()
    fold_stats["imbalance_ratio"] = fold_stats["n_max"] / fold_stats["n_min"].clip(lower=1)

    # Merge with mismatch data
    fold_stats2 = preds.groupby(
        ["experiment", "pipeline", "strategy", "fold_id"]
    )["n_epochs"].agg(n_min="min", n_max="max", n_std="std").reset_index()
    fold_stats2["imbalance_ratio"] = fold_stats2["n_max"] / fold_stats2["n_min"].clip(lower=1)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        "Epoch-count imbalance within folds\n"
        "Subjects within the same fold can contribute very different numbers of epochs",
        fontsize=11, fontweight="bold",
    )
    for ai, (pipeline, label) in enumerate([("FTest", "ANOVA (FTest)"), ("PCA", "PCA")]):
        ax  = axes[ai]
        sub = fold_stats2[fold_stats2["pipeline"] == pipeline]
        ax.hist(sub["imbalance_ratio"], bins=40, color=PIPE_COLORS[pipeline],
                edgecolor="black", alpha=0.75)
        ax.axvline(1.0, color="black", linestyle="--", linewidth=1.2,
                   label="Ratio = 1 (perfectly balanced)")
        med = sub["imbalance_ratio"].median()
        ax.axvline(med, color="red", linestyle=":", linewidth=1.5,
                   label=f"Median ratio = {med:.1f}×")
        ax.set_xlabel("Epoch-count imbalance ratio  (max epochs / min epochs in fold)", fontsize=10)
        ax.set_ylabel("Number of folds", fontsize=10)
        ax.set_title(label, fontsize=10, fontweight="bold")
        ax.legend(fontsize=9)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    out = OUTDIR / "figD_epoch_count_imbalance.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure E — Imbalance ratio vs mismatch magnitude
# ═══════════════════════════════════════════════════════════════════════════════
def fig_E_imbalance_vs_mismatch():
    """Does higher epoch-count imbalance correlate with larger mismatch?"""
    fold_ep = preds.groupby(
        ["experiment", "pipeline", "strategy", "fold_id", "task_id"]
    )["n_epochs"].agg(n_min="min", n_max="max").reset_index()
    fold_ep["imbalance_ratio"] = fold_ep["n_max"] / fold_ep["n_min"].clip(lower=1)

    # Merge with fold-level mismatch
    mdf = merged.copy()
    mdf["mismatch_pct"] = (mdf["epoch_acc"] - mdf["subject_acc"]) * 100

    key_cols = ["experiment", "pipeline", "strategy", "fold_id", "task_id"]
    combined = mdf.merge(fold_ep, on=key_cols, how="inner")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.suptitle(
        "Epoch-count imbalance ratio vs mismatch magnitude\n"
        "Higher imbalance → potential for larger epoch accuracy over-estimation",
        fontsize=11, fontweight="bold",
    )
    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax  = axes[ai]
        sub = combined[combined["pipeline"] == pipeline]
        for exp, grp in sub.groupby("experiment"):
            col = EXP_COLORS.get(exp, "#888")
            ax.scatter(grp["imbalance_ratio"], grp["mismatch_pct"],
                       alpha=0.3, s=14, color=col, label=exp, zorder=2)
        ax.axhline(0, color="black", linestyle="--", linewidth=1.2, alpha=0.7,
                   label="No mismatch")
        ax.set_xlabel("Epoch-count imbalance ratio (max/min epochs in fold)", fontsize=10)
        if ai == 0:
            ax.set_ylabel("epoch_acc − subject_acc (pp)", fontsize=10)
        ax.set_title(f"{'ANOVA (FTest)' if pipeline == 'FTest' else 'PCA'} pipeline",
                     fontsize=10, fontweight="bold")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:+.0f}%"))
        ax.legend(fontsize=7, ncol=1, loc="upper right")
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.2)

    plt.tight_layout()
    out = OUTDIR / "figE_imbalance_vs_mismatch.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure F — Epoch count vs classification outcome (boxplot)
# ═══════════════════════════════════════════════════════════════════════════════
def fig_F_epoch_count_vs_outcome():
    """
    Do correctly-classified subjects tend to have more epochs?
    If yes, epoch accuracy is biased upward.
    """
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle(
        "Epoch count: correctly classified vs misclassified subjects\n"
        "If correctly-classified subjects have more epochs, epoch accuracy is biased upward",
        fontsize=11, fontweight="bold",
    )
    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax  = axes[ai]
        sub = preds[preds["pipeline"] == pipeline]
        correct   = sub[sub["subject_correct"] == 1]["n_epochs"].values
        incorrect = sub[sub["subject_correct"] == 0]["n_epochs"].values
        bp = ax.boxplot([correct, incorrect], labels=["Correctly\nclassified", "Misclassified"],
                        patch_artist=True, showfliers=False, widths=0.45,
                        medianprops=dict(color="black", linewidth=1.5))
        bp["boxes"][0].set_facecolor("#90EE90"); bp["boxes"][0].set_alpha(0.75)
        bp["boxes"][1].set_facecolor("#FF6B6B"); bp["boxes"][1].set_alpha(0.75)
        # Jitter
        for xi, (data, col) in enumerate([(correct, "#2e8b57"), (incorrect, "#c0392b")], 1):
            jitter = np.random.normal(0, 0.07, len(data))
            ax.scatter(xi + jitter, data, alpha=0.25, s=8, color=col, zorder=3)
        med_c = np.median(correct);  med_i = np.median(incorrect)
        ax.set_ylabel("Number of epochs per subject", fontsize=10)
        ax.set_title(
            f"{'ANOVA (FTest)' if pipeline == 'FTest' else 'PCA'} pipeline\n"
            f"Median correct: {med_c:.0f}  |  Median misclassified: {med_i:.0f}",
            fontsize=10, fontweight="bold",
        )
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    out = OUTDIR / "figF_epoch_count_vs_outcome.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure G — Hall of shame: 20 folds with largest epoch > subject divergence
# ═══════════════════════════════════════════════════════════════════════════════
def fig_G_hall_of_shame():
    """Worst-case folds: high epoch_acc, low subject_acc."""
    worst = (
        merged
        .assign(mismatch=(merged["epoch_acc"] - merged["subject_acc"]) * 100)
        .nlargest(20, "mismatch")
        .reset_index(drop=True)
    )
    worst["label"] = (
        worst["experiment"].str.replace("_Random", "", regex=False)
                           .str.replace("_Uniform", "", regex=False)
        + "\n" + worst["model"].str[:8]
        + "\nfold " + worst.index.astype(str)
    )

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(worst))
    w = 0.35
    bars_e = ax.bar(x - w/2, worst["epoch_acc"] * 100, w,
                    color="#4a9ede", edgecolor="black", alpha=0.8, label="Epoch accuracy")
    bars_s = ax.bar(x + w/2, worst["subject_acc"] * 100, w,
                    color="#e07b39", edgecolor="black", alpha=0.8, label="Subject accuracy")
    ax.axhline(50, color="red", linestyle="--", linewidth=1.2, alpha=0.7, label="50% chance")
    ax.set_xticks(x); ax.set_xticklabels(worst["label"], rotation=45, ha="right", fontsize=7.5)
    ax.set_ylabel("Accuracy (%)", fontsize=10)
    ax.set_title(
        "Top-20 folds with largest epoch_acc − subject_acc gap\n"
        "(Hall of Shame: epoch accuracy most misleading here)",
        fontsize=11, fontweight="bold",
    )
    ax.set_ylim(0, 110)
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25)

    # Annotate delta
    for i, (_, row) in enumerate(worst.iterrows()):
        delta = (row["epoch_acc"] - row["subject_acc"]) * 100
        ax.text(i, max(row["epoch_acc"], row["subject_acc"]) * 100 + 2,
                f"+{delta:.0f}pp", ha="center", fontsize=6.5, color="#333")

    plt.tight_layout()
    out = OUTDIR / "figG_hall_of_shame_worst_folds.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure H — Per-experiment mean epoch vs mean subject accuracy
# ═══════════════════════════════════════════════════════════════════════════════
def fig_H_per_experiment_summary():
    summary = merged.groupby(["experiment", "pipeline", "strategy"]).agg(
        mean_epoch   =("epoch_acc",   "mean"),
        mean_subject =("subject_acc", "mean"),
        n_folds      =("fold_id",     "count"),
    ).reset_index()
    summary["label"] = summary["experiment"].str.replace("_Random", "\nRandom", regex=False)\
                                            .str.replace("_Uniform", "\nUniform", regex=False)

    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle(
        "Per-experiment summary: mean epoch accuracy vs mean subject accuracy\n"
        "Gap = systematic over-estimation from epoch weighting",
        fontsize=11, fontweight="bold",
    )
    for ai, pipeline in enumerate(["FTest", "PCA"]):
        ax  = axes[ai]
        sub = summary[summary["pipeline"] == pipeline].sort_values("mean_epoch", ascending=False)
        x   = np.arange(len(sub))
        w   = 0.35
        ax.bar(x - w/2, sub["mean_epoch"] * 100, w,
               color="#4a9ede", edgecolor="black", alpha=0.82, label="Mean epoch accuracy")
        ax.bar(x + w/2, sub["mean_subject"] * 100, w,
               color="#e07b39", edgecolor="black", alpha=0.82, label="Mean subject accuracy")
        ax.axhline(50, color="red", linestyle="--", linewidth=1.2, alpha=0.6, label="50% chance")
        for i, (_, row) in enumerate(sub.iterrows()):
            delta = (row["mean_epoch"] - row["mean_subject"]) * 100
            if abs(delta) > 0.5:
                ax.annotate(f"Δ={delta:+.1f}pp",
                            xy=(i, max(row["mean_epoch"], row["mean_subject"]) * 100 + 1),
                            ha="center", fontsize=8, color="#333")
        ax.set_xticks(x); ax.set_xticklabels(sub["label"], fontsize=8)
        ax.set_ylabel("Accuracy (%)", fontsize=10)
        ax.set_title(f"{'ANOVA (FTest)' if pipeline == 'FTest' else 'PCA'} pipeline",
                     fontsize=10, fontweight="bold")
        ax.set_ylim(0, 110)
        ax.legend(fontsize=9)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    out = OUTDIR / "figH_per_experiment_summary.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure I — Real example fold: per-subject epochs & accuracy (like conceptual)
# ═══════════════════════════════════════════════════════════════════════════════
def fig_I_real_example_fold():
    """
    Pick the single fold with the largest epoch > subject mismatch and show it
    like Figure A — making it concrete with real subject IDs.
    """
    worst_fold = (
        merged
        .assign(mismatch=(merged["epoch_acc"] - merged["subject_acc"]) * 100)
        .nlargest(1, "mismatch")
        .iloc[0]
    )

    fold_preds = preds[
        (preds["experiment"] == worst_fold["experiment"]) &
        (preds["fold_id"]    == worst_fold["fold_id"])    &
        (preds["task_id"]    == worst_fold["task_id"])
    ].copy()

    if fold_preds.empty:
        print("  figI: no matching fold found, skipping.")
        return

    fold_preds = fold_preds.sort_values("n_epochs", ascending=False)
    subjects   = [f"Sub-{int(s)}" for s in fold_preds["SubjectID"]]
    n_ep       = fold_preds["n_epochs"].values
    correct    = fold_preds["subject_correct"].values
    colors     = ["#90EE90" if c else "#FF6B6B" for c in correct]

    epoch_acc   = worst_fold["epoch_acc"]
    subject_acc = worst_fold["subject_acc"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        f"Real example — worst-case fold: {worst_fold['experiment']}  |  "
        f"fold: {worst_fold['fold_id'][:40]}…\n"
        f"Epoch accuracy: {epoch_acc*100:.1f}%   |   "
        f"Subject accuracy: {subject_acc*100:.1f}%   |   "
        f"Mismatch: {(epoch_acc-subject_acc)*100:+.1f} pp",
        fontsize=10, fontweight="bold",
    )

    ax = axes[0]
    ax.bar(range(len(subjects)), n_ep, color=colors, edgecolor="black", alpha=0.82, width=0.6)
    ax.set_xticks(range(len(subjects))); ax.set_xticklabels(subjects, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Number of epochs", fontsize=10)
    ax.set_title("Epoch counts (green = correctly classified, red = misclassified)",
                 fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    legend_items = [
        mpatches.Patch(facecolor="#90EE90", label="Correctly classified"),
        mpatches.Patch(facecolor="#FF6B6B", label="Misclassified"),
    ]
    ax.legend(handles=legend_items, fontsize=9)

    ax = axes[1]
    metric_cols = ["#4a9ede", "#e07b39"]
    b = ax.bar([0, 1], [epoch_acc * 100, subject_acc * 100],
               color=metric_cols, edgecolor="black", alpha=0.85, width=0.5)
    ax.axhline(50, color="red", linestyle="--", linewidth=1.5, label="50% chance")
    ax.set_xticks([0, 1])
    ax.set_xticklabels([
        f"Epoch accuracy\n(weighted)\n{epoch_acc*100:.1f}%",
        f"Subject accuracy\n(equal weight)\n{subject_acc*100:.1f}%",
    ], fontsize=10)
    ax.set_ylabel("Accuracy (%)", fontsize=10)
    ax.set_title(f"The resulting mismatch: Δ = {(epoch_acc-subject_acc)*100:+.1f} pp",
                 fontsize=10, fontweight="bold")
    ax.set_ylim(0, 110)
    for bar, val in zip(b, [epoch_acc * 100, subject_acc * 100]):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1.5,
                f"{val:.1f}%", ha="center", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = OUTDIR / "figI_real_example_worst_fold.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(); print(f"  Saved: {out.name}")


# ─── Run all ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nGenerating epoch–subject mismatch diagnostic figures...\n")
    fig_A_conceptual()
    fig_B_scatter()
    fig_C_mismatch_distribution()
    fig_D_epoch_count_variability()
    fig_E_imbalance_vs_mismatch()
    fig_F_epoch_count_vs_outcome()
    fig_G_hall_of_shame()
    fig_H_per_experiment_summary()
    fig_I_real_example_fold()
    print(f"\nAll figures saved to: {OUTDIR}")
