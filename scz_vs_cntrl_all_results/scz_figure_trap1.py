#!/usr/bin/env python3
"""
SCZ vs C — Trap 1 figure (both PCA and ANOVA, KNN=7).
1×2 layout: Left = PCA, Right = ANOVA
Each panel: LPSO disjoint (blue) vs subject-overlap W_C (red).

Dataset: SCZ vs Control
  SCZ: 14 subjects | Control: 14 subjects | Total: 28
  Chance (balanced): 0.500
"""

from collections import defaultdict
from pathlib import Path

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "sans-serif"]
np.random.seed(42)

BASE      = Path(__file__).parent
DATA_CSV  = BASE / "scz_all_experiments_combined.csv"
OUTDIR    = BASE / "scz_figures"
OUTDIR.mkdir(exist_ok=True)

MODEL_ORDER  = ["MLP", "XGBoost", "SVM", "KNN"]
LOCKED_KNN_K = 7

CHANCE_EPOCH = 0.500   # balanced 14/14
SEEDS = list(range(42, 52))

COL_DIS = "#d62728"   # red   — subject-overlap W_C
COL_DJ  = "#1f77b4"   # blue  — LPSO disjoint


def load_wc_direct(feature: str) -> dict:
    """Load W_C subject-overlap accuracy from hyperparameter_comparison.csv."""
    results = defaultdict(list)
    for seed in SEEDS:
        dname = f"{feature}_W_C_scz_cntrl_seed{seed}"
        ml_dir = BASE / dname / "ml_results_grid_search"
        if not ml_dir.exists():
            continue
        for model in MODEL_ORDER:
            mname = "MLP_(Neural_Network)" if model == "MLP" else model
            mdir  = ml_dir / mname
            if not mdir.is_dir():
                continue
            hp_csv = mdir / "hyperparameter_comparison.csv"
            if not hp_csv.exists():
                continue
            df = pd.read_csv(hp_csv)
            if model == "KNN":
                k_col = next((c for c in df.columns if "neighbor" in c.lower()), None)
                if k_col:
                    row = df[df[k_col].astype(str) == str(LOCKED_KNN_K)]
                    if not row.empty:
                        acc_col = next((c for c in df.columns if "accuracy" in c.lower()), None)
                        if acc_col:
                            results[model].append(float(row[acc_col].iloc[0]))
                continue
            acc_col = next((c for c in df.columns if "accuracy" in c.lower()), None)
            if acc_col:
                results[model].append(float(df[acc_col].max()))
    return dict(results)


def load_disjoint(feature: str) -> dict:
    """Load LPSO P=6 best-HP per model from compiled CSV."""
    df = pd.read_csv(DATA_CSV)
    exp_name = f"{feature}_L_6_SCZ"
    sub = df[df["experiment"] == exp_name]
    out = {}
    KNN_K7_HP = '{"metric": "euclidean", "n_neighbors": 7, "weights": "uniform"}'
    for model in MODEL_ORDER:
        m = sub[sub["model"] == model]
        if m.empty:
            continue
        if model == "KNN":
            k7 = m[m["hyperparams"] == KNN_K7_HP]
            if not k7.empty:
                out[model] = k7["test_accuracy"].values
            continue
        best_hp = m.groupby("hyperparams")["test_accuracy"].median().idxmax()
        out[model] = m[m["hyperparams"] == best_hp]["test_accuracy"].values
    return out


def half_violin(ax, vals, x, width=0.30, color="steelblue", alpha=0.65,
                side="right", bw=0.35):
    vals = np.asarray(vals)
    if len(vals) < 3:
        return
    kde = gaussian_kde(vals, bw_method=bw)
    y_range = np.linspace(max(0.0, vals.min() - 0.04),
                          min(1.0, vals.max() + 0.04), 200)
    density = kde(y_range)
    density = density / density.max() * width
    if side == "right":
        ax.fill_betweenx(y_range, x, x + density, color=color, alpha=alpha)
    else:
        ax.fill_betweenx(y_range, x - density, x, color=color, alpha=alpha)


def draw_panel(ax, left_vals, right_vals, col_L, col_R,
               chance_line, ylim=(0.0, 1.0), bw_L=0.3, bw_R=0.4):
    for mi, model in enumerate(MODEL_ORDER):
        L = np.asarray(left_vals.get(model, []))
        R = np.asarray(right_vals.get(model, []))
        xi = mi

        half_violin(ax, L, xi - 0.02, color=col_L, side="left", bw=bw_L)
        if len(L) > 0:
            jit = np.random.uniform(xi - 0.28, xi - 0.04, len(L))
            ax.scatter(jit, L, color=col_L, s=20, alpha=0.6, linewidths=0)
            ax.plot([xi - 0.32, xi - 0.03], [np.median(L)] * 2,
                    color=col_L, linewidth=2.5)

        half_violin(ax, R, xi + 0.02, color=col_R, side="right", bw=bw_R)
        if len(R) > 0:
            jit = np.random.uniform(xi + 0.04, xi + 0.28, len(R))
            ax.scatter(jit, R, color=col_R, s=20, alpha=0.6, linewidths=0)
            ax.plot([xi + 0.03, xi + 0.32], [np.median(R)] * 2,
                    color=col_R, linewidth=2.5)

    ax.axhline(chance_line, color="red", lw=1.2, ls=":", alpha=0.7)
    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=10)
    ax.set_ylim(*ylim)
    ax.set_xlim(-0.55, len(MODEL_ORDER) - 0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2, linestyle="--")


# ── Load data ──────────────────────────────────────────────────────────────────
print("Loading W_C overlap data …")
pca_wc   = load_wc_direct("PCA")
anova_wc = load_wc_direct("ANOVA")

print("Loading LPSO P=6 disjoint data …")
dj_pca   = load_disjoint("PCA")
dj_anova = load_disjoint("ANOVA")

for m in MODEL_ORDER:
    print(f"  {m}: WC_PCA={len(pca_wc.get(m,[]))}  WC_ANOVA={len(anova_wc.get(m,[]))}  "
          f"DJ_PCA={len(dj_pca.get(m,[]))}  DJ_ANOVA={len(dj_anova.get(m,[]))}")


# ── Figure: 1×2 (cols=PCA/ANOVA) ──────────────────────────────────────────────
LEG_DIS = mpatches.Patch(facecolor=COL_DIS, label="SCZ – subject-overlap (W_C)")
LEG_DJ  = mpatches.Patch(facecolor=COL_DJ,  label="SCZ – LPSO P=6 (disjoint)")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5),
                         gridspec_kw={"wspace": 0.26})

panels = [
    (axes[0], dj_pca,   pca_wc,   CHANCE_EPOCH, (0.3, 1.0), "PCA"),
    (axes[1], dj_anova, anova_wc, CHANCE_EPOCH, (0.3, 1.0), "ANOVA"),
]

for ax, dj, wc, chance, ylim, title in panels:
    draw_panel(ax, dj, wc, COL_DJ, COL_DIS, chance_line=chance, ylim=ylim)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(handles=[LEG_DJ, LEG_DIS], fontsize=8, loc="lower right")

axes[0].set_ylabel("Epoch accuracy", fontsize=10)

fig.suptitle("Trap 1: Subject-Overlap Memorization — SCZ vs Control (KNN $k$=7)\n"
             "Blue = LPSO disjoint (50 folds) · Red = Subject-overlap (10 seeds) · "
             "Dotted = chance (0.500)",
             fontsize=11, fontweight="bold", y=1.02)

outfile = OUTDIR / "scz_trap1.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"\nSaved → {outfile}")

# Print stats
for label, data in [("LPSO PCA", dj_pca), ("LPSO ANOVA", dj_anova),
                    ("WC PCA", pca_wc), ("WC ANOVA", anova_wc)]:
    print(f"\n{label}:")
    for m in MODEL_ORDER:
        v = np.array(data.get(m, []))
        if len(v) > 0:
            print(f"  {m}: median={np.median(v):.3f}  n={len(v)}")
