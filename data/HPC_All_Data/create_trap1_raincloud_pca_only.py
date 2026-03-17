#!/usr/bin/env python3
"""
Trap 1 — Raincloud, PCA only, 1×2
  Left  : Fingerprinting (purple) vs Disease-overlap (red)   — within-subject
  Right : Disease-overlap (red)   vs Disease-disjoint (blue) — LPSO P=6 best HP

Y-axis: 0.0 – 1.0   Chance line at 0.5
Style: identical to trap1_design5_raincloud.png
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
    "fingerprint": "#7b2d8b",
    "overlap":     "#d62728",
    "disjoint":    "#1f77b4",
}
MODEL_ORDER = ["MLP", "XGBoost", "SVM", "KNN"]
FS = "PCA"

# ── Load & filter ─────────────────────────────────────────────────────────────
raw     = pd.read_csv(DATA)
finger  = raw[raw["experiment"].str.contains("W_F")].copy()
overlap = raw[raw["experiment"].str.contains("W_C")].copy()

_dj_all = raw[(raw["experiment_type"] == "LPSO_Random_50") &
              (raw["holdout_size_P"]  == 6)].copy()

def best_hp_disjoint(fs):
    sub, rows = _dj_all[_dj_all["feature_set"] == fs], []
    for model in MODEL_ORDER:
        m = sub[sub["model"] == model]
        if m.empty: continue
        top = m.groupby("hyperparams")["test_accuracy"].median().idxmax()
        rows.append(m[m["hyperparams"] == top])
    return pd.concat(rows) if rows else pd.DataFrame()

# ── half_violin ───────────────────────────────────────────────────────────────
def half_violin(ax, vals, x, width=0.32, color="steelblue", alpha=0.65,
                side="right", bw=0.3):
    if len(vals) < 3:
        return
    kde     = gaussian_kde(vals, bw_method=bw)
    y_range = np.linspace(max(0.0, vals.min() - 0.05),
                          min(1.0, vals.max() + 0.05), 200)
    density = kde(y_range)
    density = density / density.max() * width
    if side == "right":
        ax.fill_betweenx(y_range, x, x + density, color=color, alpha=alpha)
    else:
        ax.fill_betweenx(y_range, x - density, x, color=color, alpha=alpha)

# ── draw one panel ────────────────────────────────────────────────────────────
def draw_panel(ax, left_df, right_df, col_L, col_R, bw_L=0.5, bw_R=0.3):
    ax.axhline(0.5, color="red", linewidth=1.2, linestyle=":", alpha=0.7)

    for mi, model in enumerate(MODEL_ORDER):
        xi = mi
        L  = left_df [(left_df ["model"] == model) & (left_df ["feature_set"] == FS)]["test_accuracy"].values
        R  = right_df[(right_df["model"] == model) & (right_df["feature_set"] == FS)]["test_accuracy"].values

        half_violin(ax, L, xi - 0.02, color=col_L, side="left",  bw=bw_L)
        half_violin(ax, R, xi + 0.02, color=col_R, side="right", bw=bw_R)

        if len(L) > 0:
            jit_L = np.random.uniform(xi - 0.30, xi - 0.05, len(L))
            ax.scatter(jit_L, L, color=col_L, s=18, alpha=0.55, linewidths=0)
            ax.plot([xi - 0.34, xi - 0.03], [np.median(L)] * 2,
                    color=col_L, linewidth=2.5)

        if len(R) > 0:
            jit_R = np.random.uniform(xi + 0.05, xi + 0.30, len(R))
            ax.scatter(jit_R, R, color=col_R, s=18, alpha=0.55, linewidths=0)
            ax.plot([xi + 0.03, xi + 0.34], [np.median(R)] * 2,
                    color=col_R, linewidth=2.5)

    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlim(-0.65, len(MODEL_ORDER) - 0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# ── Figure ────────────────────────────────────────────────────────────────────
fig, (ax_L, ax_R) = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)

fig.suptitle(
    "Trap 1 — Subject identity leakage inflates classification accuracy  (PCA features)",
    fontsize=11, fontweight="bold",
)

dj = best_hp_disjoint(FS)

# Left panel
draw_panel(ax_L, finger, overlap,
           col_L=COL["fingerprint"], col_R=COL["overlap"],
           bw_L=0.5, bw_R=0.5)
ax_L.set_title("Within-subject splits\nFingerprinting  vs  Disease – subject-overlap",
               fontsize=10, fontweight="bold")
ax_L.set_ylabel("Test accuracy", fontsize=11)
ax_L.set_yticks(np.arange(0.0, 1.01, 0.1))
ax_L.legend(handles=[
    mpatches.Patch(facecolor=COL["fingerprint"], label="Fingerprinting (subject-ID)"),
    mpatches.Patch(facecolor=COL["overlap"],     label="Disease – subject-overlap"),
], fontsize=8.5, loc="lower right")

# Right panel
draw_panel(ax_R, overlap, dj,
           col_L=COL["overlap"], col_R=COL["disjoint"],
           bw_L=0.5, bw_R=0.3)
ax_R.set_title("Disease classification\nSubject-overlap  vs  Subject-disjoint (LPSO P=6)",
               fontsize=10, fontweight="bold")
ax_R.legend(handles=[
    mpatches.Patch(facecolor=COL["overlap"],  label="Disease – subject-overlap"),
    mpatches.Patch(facecolor=COL["disjoint"], label="Disease – subject-disjoint (LPSO)"),
], fontsize=8.5, loc="lower right")

plt.tight_layout()
out = OUTDIR / "trap1_raincloud_pca_only.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"  {out}")
