#!/usr/bin/env python3
"""
Trap 1 raincloud — using the full v1-v10 intra-subject runs.

Data sources:
  Within-subject (v1-v10): data/HPC_All_Data/intra-subject/{PCA,ANOVA}_{W_F,W_C}/
    For each version directory, the BEST HP accuracy per model is extracted → n≈10.
  Subject-disjoint LPSO P=6: all_experiments_combined.csv, best-HP per model → n=50.

Figures produced:
  trap1_raincloud_v10_pca.png    — PCA only, 1×2
  trap1_raincloud_v10_2x2.png   — PCA (top) + ANOVA (bottom), 2×2
"""

import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

matplotlib.use("Agg")
np.random.seed(42)

BASE      = Path(__file__).parent
INTRA_DIR = BASE / "intra-subject"       # resolves via symlink
DATA_CSV  = BASE / "all_experiments_combined.csv"
OUTDIR    = BASE / "paper_subject_eval_outputs" / "trap1_figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

COL = {
    "fingerprint": "#7b2d8b",
    "overlap":     "#d62728",
    "disjoint":    "#1f77b4",
}
MODEL_ORDER = ["MLP", "XGBoost", "SVM", "KNN"]

MODEL_NAME_MAP = {
    "MLP (Neural Network)": "MLP",
    "MLP_(Neural_Network)": "MLP",
    "MLP": "MLP",
    "XGBoost": "XGBoost",
    "SVM": "SVM",
    "KNN": "KNN",
}

def _norm(name: str) -> str:
    return MODEL_NAME_MAP.get(name.replace("_", " ").strip(), name)


# ── Load within-subject v1-v10 data ──────────────────────────────────────────
def extract_best_per_version(exp_name: str) -> dict:
    """
    Walk every version dir under INTRA_DIR/<exp_name>/.
    For each version, pick the single best HP accuracy per model.
    Returns {model: [acc_v1, acc_v2, …]}.
    """
    exp_path = INTRA_DIR / exp_name
    results  = defaultdict(list)

    if not exp_path.exists():
        print(f"  WARNING: {exp_path} not found")
        return results

    version_dirs = sorted(
        [d for d in exp_path.iterdir()
         if d.is_dir() and re.match(rf"{re.escape(exp_name)}_v\d+$", d.name)],
        key=lambda d: int(d.name.split("_v")[-1]),
    )
    print(f"  {exp_name}: {len(version_dirs)} versions found")

    for vdir in version_dirs:
        ml_path = vdir / "ml_results_grid_search"
        if not ml_path.exists():
            continue

        version_best: dict = {}
        for model_dir in ml_path.iterdir():
            if not model_dir.is_dir() or model_dir.name in {"graphs", "debug"}:
                continue
            model = _norm(model_dir.name)
            if model not in MODEL_ORDER:
                continue

            best_acc = None
            for rf in model_dir.rglob("results.json"):
                try:
                    data = json.loads(rf.read_text())
                    acc  = (data.get("test_results", {}).get("accuracy")
                            or data.get("test_accuracy")
                            or data.get("detailed_results", {}).get("test_accuracy"))
                    if acc is not None:
                        acc = float(acc)
                        if best_acc is None or acc > best_acc:
                            best_acc = acc
                except Exception:
                    pass

            if best_acc is not None:
                version_best[model] = best_acc

        for model, acc in version_best.items():
            results[model].append(acc)

    for model in MODEL_ORDER:
        vals = results.get(model, [])
        print(f"    {model}: n={len(vals)}  vals={[round(v,3) for v in vals]}")

    return results


print("Loading within-subject data …")
data_ws = {}
for exp in ["PCA_W_F", "PCA_W_C", "ANOVA_W_F", "ANOVA_W_C"]:
    data_ws[exp] = extract_best_per_version(exp)


# ── Load disjoint LPSO (best HP → n=50) ──────────────────────────────────────
raw   = pd.read_csv(DATA_CSV)
_dj   = raw[(raw["experiment_type"] == "LPSO_Random_50") & (raw["holdout_size_P"] == 6)]

def best_hp_disjoint(fs: str) -> dict:
    sub = _dj[_dj["feature_set"] == fs]
    out = {}
    for model in MODEL_ORDER:
        m   = sub[sub["model"] == model]
        if m.empty: continue
        top = m.groupby("hyperparams")["test_accuracy"].median().idxmax()
        out[model] = m[m["hyperparams"] == top]["test_accuracy"].values
    return out

dj_pca  = best_hp_disjoint("PCA")
dj_anova = best_hp_disjoint("ANOVA")


# ── Drawing helpers ───────────────────────────────────────────────────────────
def half_violin(ax, vals, x, width=0.32, color="steelblue", alpha=0.65,
                side="right", bw=0.35):
    if len(vals) < 4:
        return
    kde     = gaussian_kde(vals, bw_method=bw)
    y_range = np.linspace(max(0.0,  vals.min() - 0.04),
                          min(1.0,  vals.max() + 0.04), 200)
    density = kde(y_range)
    density = density / density.max() * width
    if side == "right":
        ax.fill_betweenx(y_range, x, x + density, color=color, alpha=alpha)
    else:
        ax.fill_betweenx(y_range, x - density, x, color=color, alpha=alpha)


def draw_panel(ax, left_vals: dict, right_vals: dict, col_L, col_R,
               bw_L=0.45, bw_R=0.3):
    ax.axhline(0.5, color="red", linewidth=1.2, linestyle=":", alpha=0.7)

    for mi, model in enumerate(MODEL_ORDER):
        xi = mi
        L  = np.asarray(left_vals.get(model, []))
        R  = np.asarray(right_vals.get(model, []))

        # Left half-violin + jitter + median tick
        half_violin(ax, L, xi - 0.02, color=col_L, side="left",  bw=bw_L)
        if len(L) > 0:
            jit = np.random.uniform(xi - 0.30, xi - 0.05, len(L))
            ax.scatter(jit, L, color=col_L, s=18, alpha=0.55, linewidths=0)
            ax.plot([xi - 0.34, xi - 0.03], [np.median(L)] * 2,
                    color=col_L, linewidth=2.5)

        # Right half-violin + jitter + median tick
        half_violin(ax, R, xi + 0.02, color=col_R, side="right", bw=bw_R)
        if len(R) > 0:
            jit = np.random.uniform(xi + 0.05, xi + 0.30, len(R))
            ax.scatter(jit, R, color=col_R, s=18, alpha=0.55, linewidths=0)
            ax.plot([xi + 0.03, xi + 0.34], [np.median(R)] * 2,
                    color=col_R, linewidth=2.5)

    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax.set_ylim(0.0, 1.0)
    ax.set_yticks(np.arange(0.0, 1.01, 0.1))
    ax.set_xlim(-0.65, len(MODEL_ORDER) - 0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


LEGEND_FP = mpatches.Patch(facecolor=COL["fingerprint"], label="Fingerprinting (subject-ID)")
LEGEND_OV = mpatches.Patch(facecolor=COL["overlap"],     label="Disease – subject-overlap")
LEGEND_DJ = mpatches.Patch(facecolor=COL["disjoint"],    label="Disease – subject-disjoint (LPSO)")

TITLE_L = "Within-subject splits\nFingerprinting  vs  Disease – subject-overlap"
TITLE_R = "Disease classification\nSubject-overlap  vs  Subject-disjoint (LPSO P=6)"


# ══ Figure 1: PCA only, 1×2 ══════════════════════════════════════════════════
fig, (ax_L, ax_R) = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
fig.suptitle(
    "Trap 1 — Subject identity leakage inflates classification accuracy  (PCA features)\n"
    "n=10 random seeds per within-subject condition  ·  n=50 folds for subject-disjoint",
    fontsize=11, fontweight="bold",
)

fp_pca = {m: np.asarray(data_ws["PCA_W_F"][m]) for m in MODEL_ORDER}
ov_pca = {m: np.asarray(data_ws["PCA_W_C"][m]) for m in MODEL_ORDER}

draw_panel(ax_L, fp_pca, ov_pca, COL["fingerprint"], COL["overlap"], bw_L=0.45, bw_R=0.45)
ax_L.set_title(TITLE_L, fontsize=10, fontweight="bold")
ax_L.set_ylabel("Test accuracy", fontsize=11)
ax_L.legend(handles=[LEGEND_FP, LEGEND_OV], fontsize=8.5, loc="lower right")

draw_panel(ax_R, ov_pca, dj_pca, COL["overlap"], COL["disjoint"], bw_L=0.45, bw_R=0.3)
ax_R.set_title(TITLE_R, fontsize=10, fontweight="bold")
ax_R.legend(handles=[LEGEND_OV, LEGEND_DJ], fontsize=8.5, loc="lower right")

plt.tight_layout()
out1 = OUTDIR / "trap1_raincloud_v10_pca.png"
fig.savefig(out1, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\n  {out1}")


# ══ Figure 2: 2×2 — PCA (top) + ANOVA (bottom) ═══════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(13, 11), sharey=True, sharex="col",
                         gridspec_kw={"hspace": 0.38, "wspace": 0.06})
fig.suptitle(
    "Trap 1 — Subject identity leakage inflates classification accuracy\n"
    "n=10 random seeds per within-subject condition  ·  n=50 folds for subject-disjoint",
    fontsize=11, fontweight="bold", y=1.01,
)

for row_i, (fs_label, fs_key, dj) in enumerate([
    ("PCA",   "PCA",   dj_pca),
    ("ANOVA", "ANOVA", dj_anova),
]):
    fp = {m: np.asarray(data_ws[f"{fs_key}_W_F"][m]) for m in MODEL_ORDER}
    ov = {m: np.asarray(data_ws[f"{fs_key}_W_C"][m]) for m in MODEL_ORDER}

    ax = axes[row_i][0]
    draw_panel(ax, fp, ov, COL["fingerprint"], COL["overlap"], bw_L=0.45, bw_R=0.45)
    if row_i == 0:
        ax.set_title(TITLE_L, fontsize=10, fontweight="bold")
    ax.set_ylabel(f"{fs_label} features\nTest accuracy", fontsize=10)
    ax.legend(handles=[LEGEND_FP, LEGEND_OV], fontsize=8.5, loc="lower right")

    ax = axes[row_i][1]
    draw_panel(ax, ov, dj, COL["overlap"], COL["disjoint"], bw_L=0.45, bw_R=0.3)
    if row_i == 0:
        ax.set_title(TITLE_R, fontsize=10, fontweight="bold")
    ax.legend(handles=[LEGEND_OV, LEGEND_DJ], fontsize=8.5, loc="lower right")

plt.tight_layout()
out2 = OUTDIR / "trap1_raincloud_v10_2x2.png"
fig.savefig(out2, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"  {out2}")
