#!/usr/bin/env python3
"""
Trap 1 — Raincloud 2×2
  Row 0 (top)    : PCA features
  Row 1 (bottom) : ANOVA features
  Col 0 (left)   : Fingerprinting (purple)  vs  Disease-overlap (red)   – within-subject
  Col 1 (right)  : Disease-overlap (red)    vs  Disease-disjoint (blue) – LPSO P=6

Within-subject experiments have exactly 1 fold per HP (3 HPs → n=3 total per model×feature).
All 3 HP runs are plotted to give a minimal distribution.

Disjoint (LPSO): best-HP-per-model (highest median) → n=50 per model×feature.

Visual style mirrors trap1_design5_raincloud.png exactly.
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

# ── Palette (unchanged from design5) ─────────────────────────────────────────
COL = {
    "fingerprint": "#7b2d8b",
    "overlap":     "#d62728",
    "disjoint":    "#1f77b4",
}
MODEL_ORDER = ["MLP", "XGBoost", "SVM", "KNN"]

# ── Load & filter ─────────────────────────────────────────────────────────────
raw = pd.read_csv(DATA)

# Within-subject: ALL HPs (n=3 per model×feature — one fold per HP config)
finger  = raw[raw["experiment"].str.contains("W_F")].copy()
overlap = raw[raw["experiment"].str.contains("W_C")].copy()

# Subject-disjoint: best HP per model×feature (n=50 per selection)
_dj_all = raw[(raw["experiment_type"] == "LPSO_Random_50") &
              (raw["holdout_size_P"]  == 6)].copy()

def best_hp_disjoint(fs):
    """Keep only the HP with highest median per model for the given feature set."""
    sub  = _dj_all[_dj_all["feature_set"] == fs]
    rows = []
    for model in MODEL_ORDER:
        m = sub[sub["model"] == model]
        if m.empty:
            continue
        top = m.groupby("hyperparams")["test_accuracy"].median().idxmax()
        rows.append(m[m["hyperparams"] == top])
    return pd.concat(rows) if rows else pd.DataFrame()

# ── half_violin — identical params to design5 ─────────────────────────────────
def half_violin(ax, vals, x, width=0.35, color="steelblue", alpha=0.7, side="right",
                bw=0.3):
    if len(vals) < 3:
        return
    kde     = gaussian_kde(vals, bw_method=bw)
    y_range = np.linspace(max(0.20, vals.min() - 0.05),
                          min(1.05, vals.max() + 0.05), 200)
    density = kde(y_range)
    density = density / density.max() * width
    if side == "right":
        ax.fill_betweenx(y_range, x, x + density, color=color, alpha=alpha)
    else:
        ax.fill_betweenx(y_range, x - density, x, color=color, alpha=alpha)

# ── draw one panel ────────────────────────────────────────────────────────────
def draw_panel(ax, fs, left_df, right_df, col_L, col_R, bw_L=0.5, bw_R=0.3):
    """
    For each model: left half-violin (col_L) + right half-violin (col_R),
    jitter dots, median ticks — exactly as design5.
    """
    ax.axhline(0.5, color="red", linewidth=1.2, linestyle=":", alpha=0.7,
               label="Chance (0.5)")

    for mi, model in enumerate(MODEL_ORDER):
        xi   = mi
        L    = left_df[(left_df["model"]       == model) &
                       (left_df["feature_set"] == fs)]["test_accuracy"].values
        R    = right_df[(right_df["model"]       == model) &
                        (right_df["feature_set"] == fs)]["test_accuracy"].values

        # Half-violins
        half_violin(ax, L, xi - 0.02, width=0.32, color=col_L,
                    alpha=0.65, side="left",  bw=bw_L)
        half_violin(ax, R, xi + 0.02, width=0.32, color=col_R,
                    alpha=0.65, side="right", bw=bw_R)

        # Jitter dots
        if len(L) > 0:
            jit_L = np.random.uniform(xi - 0.30, xi - 0.05, len(L))
            ax.scatter(jit_L, L, color=col_L, s=18, alpha=0.55, linewidths=0)
        if len(R) > 0:
            jit_R = np.random.uniform(xi + 0.05, xi + 0.30, len(R))
            ax.scatter(jit_R, R, color=col_R, s=18, alpha=0.55, linewidths=0)

        # Median ticks
        if len(L) > 0:
            ax.plot([xi - 0.34, xi - 0.03], [np.median(L)] * 2,
                    color=col_L, linewidth=2.5)
        if len(R) > 0:
            ax.plot([xi + 0.03, xi + 0.34], [np.median(R)] * 2,
                    color=col_R, linewidth=2.5)

    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax.set_ylim(0.25, 1.08)
    ax.set_xlim(-0.65, len(MODEL_ORDER) - 0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# ── Build figure ──────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(13, 11),
                         sharey=True, sharex="col",
                         gridspec_kw={"hspace": 0.38, "wspace": 0.06})

fig.suptitle(
    "Trap 1 — Subject identity leakage inflates classification accuracy\n"
    "Left: fingerprinting mirrors disease accuracy (within-subject)  ·  "
    "Right: accuracy collapses when subjects are disjoint",
    fontsize=11, fontweight="bold", y=1.01,
)

COL_TITLES = [
    "Within-subject splits\nFingerprinting  vs  Disease – subject-overlap",
    "Disease classification\nSubject-overlap  vs  Subject-disjoint (LPSO P=6)",
]

for row_i, fs in enumerate(["PCA", "ANOVA"]):   # PCA top, ANOVA bottom
    dj = best_hp_disjoint(fs)

    # ── Left panel: finger (left, purple) vs overlap (right, red) ────────────
    ax = axes[row_i][0]
    draw_panel(ax, fs, finger, overlap,
               col_L=COL["fingerprint"], col_R=COL["overlap"],
               bw_L=0.5, bw_R=0.5)          # broader BW for sparse n=3 data

    if row_i == 0:
        ax.set_title(COL_TITLES[0], fontsize=10, fontweight="bold")
    ax.legend(handles=[
        mpatches.Patch(facecolor=COL["fingerprint"],
                       label="Fingerprinting (subject-ID)"),
        mpatches.Patch(facecolor=COL["overlap"],
                       label="Disease – subject-overlap"),
    ], fontsize=8.5, loc="lower right")
    ax.set_ylabel(f"{'PCA' if fs=='PCA' else 'ANOVA'} features\nTest accuracy",
                  fontsize=10)

    # ── Right panel: overlap (left, red) vs disjoint (right, blue) ───────────
    ax = axes[row_i][1]
    draw_panel(ax, fs, overlap, dj,
               col_L=COL["overlap"], col_R=COL["disjoint"],
               bw_L=0.5, bw_R=0.3)          # tight BW for large n=50 disjoint

    if row_i == 0:
        ax.set_title(COL_TITLES[1], fontsize=10, fontweight="bold")
    ax.legend(handles=[
        mpatches.Patch(facecolor=COL["overlap"],
                       label="Disease – subject-overlap"),
        mpatches.Patch(facecolor=COL["disjoint"],
                       label="Disease – subject-disjoint (LPSO)"),
    ], fontsize=8.5, loc="lower right")

# ── Save ──────────────────────────────────────────────────────────────────────
out = OUTDIR / "trap1_raincloud_2x2.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"  {out}")
