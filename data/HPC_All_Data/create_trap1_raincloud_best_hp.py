#!/usr/bin/env python3
"""
Trap 1 — Raincloud variant: best hyperparameter per model only.

Layout: 2 rows (ANOVA, PCA) × 2 cols
  Col A: Within-subject — Fingerprinting vs Disease (subject-overlap)
  Col B: Disease — Subject-overlap vs Subject-disjoint (LPSO)

Each model group shows two half-clouds side by side.
Within-subject data has n=1 after best-HP selection → shown as a large dot + tick.
LPSO data has n=50 after best-HP selection → full raincloud.
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import gaussian_kde
from pathlib import Path

matplotlib.use("Agg")
np.random.seed(42)

BASE   = Path(__file__).parent
DATA   = BASE / "all_experiments_combined.csv"
OUTDIR = BASE / "paper_subject_eval_outputs" / "trap1_figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

COL = {
    "fingerprint": "#7b2d8b",   # purple
    "overlap":     "#d62728",   # red
    "disjoint":    "#1f77b4",   # blue
}
MODEL_ORDER = ["MLP", "XGBoost", "SVM", "KNN"]

# ── Load data ─────────────────────────────────────────────────────────────────
raw      = pd.read_csv(DATA)
finger   = raw[raw["experiment"].str.contains("W_F")].copy()
overlap  = raw[raw["experiment"].str.contains("W_C")].copy()
disjoint = raw[(raw["experiment_type"] == "LPSO_Random_50") &
               (raw["holdout_size_P"] == 6)].copy()


def best_hp(df, feature_set):
    """Return subset keeping only the HP with highest median per model."""
    sub = df[df["feature_set"] == feature_set].copy()
    rows = []
    for model in MODEL_ORDER:
        m = sub[sub["model"] == model]
        if m.empty:
            continue
        top_hp = m.groupby("hyperparams")["test_accuracy"].median().idxmax()
        rows.append(m[m["hyperparams"] == top_hp])
    return pd.concat(rows) if rows else pd.DataFrame()


def half_violin(ax, vals, x, width=0.30, color="steelblue", alpha=0.68, side="right"):
    """Draw a half KDE violin; skipped silently if < 5 points."""
    if len(vals) < 5:
        return
    kde = gaussian_kde(vals, bw_method=0.35)
    yr  = np.linspace(max(0.20, vals.min() - 0.04),
                      min(1.06, vals.max() + 0.04), 200)
    d   = kde(yr)
    d   = d / d.max() * width
    if side == "right":
        ax.fill_betweenx(yr, x, x + d, color=color, alpha=alpha)
    else:
        ax.fill_betweenx(yr, x - d, x, color=color, alpha=alpha)


def draw_pair(ax, vals_L, vals_R, xi, col_L, col_R):
    """
    Draw two rainclouds around position xi.
    Left cloud  (col_L): half-violin flipped left + jitter left + median tick left.
    Right cloud (col_R): half-violin right + jitter right + median tick right.
    Single-point data (n=1): large star marker + annotated value instead of violin.
    """
    W = 0.30   # max violin half-width
    J = 0.28   # jitter band half-width

    for vals, col, side, sign in [(vals_L, col_L, "left", -1),
                                   (vals_R, col_R, "right", +1)]:
        if len(vals) == 0:
            continue

        half_violin(ax, vals, xi + sign * 0.02,
                    width=W, color=col, alpha=0.65, side=side)

        # Jitter dots (or single prominent dot)
        if len(vals) == 1:
            ax.scatter([xi + sign * 0.18], vals, color=col,
                       s=140, marker="D", zorder=6, edgecolors="white", linewidths=0.8)
        else:
            jx = np.random.uniform(xi + sign * 0.05, xi + sign * J, len(vals))
            ax.scatter(jx, vals, color=col, s=20, alpha=0.55, linewidths=0, zorder=4)

        # Median tick
        med = np.median(vals)
        ax.plot([xi + sign * 0.04, xi + sign * (W + 0.04)],
                [med, med], color=col, linewidth=2.8, zorder=5)
        # Median value label
        ax.text(xi + sign * (W + 0.08), med,
                f"{med:.2f}",
                ha="left" if sign > 0 else "right",
                va="center", fontsize=7.5, color=col, fontweight="bold")


# ── Figure: 2 rows (ANOVA, PCA) × 2 cols (left comp, right comp) ─────────────
fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharey=True, sharex="col")
fig.suptitle(
    "Trap 1 — Subject fingerprinting mirrors overlap-prone disease accuracy\n"
    "Best hyperparameter per model shown  |  Each dot = one fold  |  Diamond = single available fold",
    fontsize=12, fontweight="bold", y=1.01,
)

COL_TITLES = [
    "Within-subject splits\nFingerprinting (◆)  vs  Disease – Subject-overlap (◆)",
    "Disease classification\nSubject-overlap (◆)  vs  Subject-disjoint – LPSO (cloud)",
]
ROW_LABELS = ["ANOVA features", "PCA features"]

for row_i, fs in enumerate(["ANOVA", "PCA"]):
    # Best-HP subsets for this feature set
    fp_b  = best_hp(finger,   fs)
    ov_b  = best_hp(overlap,  fs)
    dj_b  = best_hp(disjoint, fs)

    # ── Col 0: Fingerprinting vs Disease-Overlap ───────────────────────────
    ax = axes[row_i][0]
    ax.axhline(0.5, color="red", linestyle=":", linewidth=1.2, alpha=0.6, label="Chance (0.5)")

    for mi, model in enumerate(MODEL_ORDER):
        vfp = fp_b[fp_b["model"] == model]["test_accuracy"].values
        vov = ov_b[ov_b["model"] == model]["test_accuracy"].values
        draw_pair(ax, vfp, vov, mi, COL["fingerprint"], COL["overlap"])

    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax.set_ylim(0.25, 1.12)
    ax.set_xlim(-0.65, len(MODEL_ORDER) - 0.35)
    ax.set_title(COL_TITLES[0], fontsize=9.5, fontweight="bold")
    if row_i == 0:
        ax.legend(handles=[
            mpatches.Patch(facecolor=COL["fingerprint"], label="Fingerprinting (subject-ID)"),
            mpatches.Patch(facecolor=COL["overlap"],     label="Disease – subject-overlap"),
        ], fontsize=9, loc="lower right")
    ax.set_ylabel(f"{ROW_LABELS[row_i]}\nTest accuracy", fontsize=10)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    # ── Col 1: Disease-Overlap vs Disease-Disjoint ─────────────────────────
    ax = axes[row_i][1]
    ax.axhline(0.5, color="red", linestyle=":", linewidth=1.2, alpha=0.6)

    for mi, model in enumerate(MODEL_ORDER):
        vov = ov_b[ov_b["model"] == model]["test_accuracy"].values
        vdj = dj_b[dj_b["model"] == model]["test_accuracy"].values
        draw_pair(ax, vov, vdj, mi, COL["overlap"], COL["disjoint"])

    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax.set_xlim(-0.65, len(MODEL_ORDER) - 0.35)
    ax.set_title(COL_TITLES[1], fontsize=9.5, fontweight="bold")
    if row_i == 0:
        ax.legend(handles=[
            mpatches.Patch(facecolor=COL["overlap"],  label="Disease – subject-overlap"),
            mpatches.Patch(facecolor=COL["disjoint"], label="Disease – subject-disjoint (LPSO)"),
        ], fontsize=9, loc="lower right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# Row labels on right side
for row_i, label in enumerate(ROW_LABELS):
    axes[row_i][1].annotate(
        label, xy=(1.02, 0.5), xycoords="axes fraction",
        fontsize=10, fontweight="bold", rotation=270,
        va="center", ha="left", color="gray",
    )

plt.tight_layout()
out = OUTDIR / "trap1_raincloud_best_hp.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"  {out}")
