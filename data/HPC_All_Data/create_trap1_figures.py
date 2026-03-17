#!/usr/bin/env python3
"""
Six publication-quality figures for Trap 1:
Subject overlap inflates disease classification accuracy (EEG fingerprinting leakage).

Data mapping:
  W_F  = Within-subject Fingerprinting  (subject ID, overlap-prone)
  W_C  = Within-subject Classification  (disease, overlap-prone)
  L_*  = LPSO experiments               (disease, subject-disjoint)

Saved to: paper_subject_eval_outputs/trap1_figures/
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
from scipy.stats import gaussian_kde
from pathlib import Path

matplotlib.use("Agg")
np.random.seed(42)

BASE   = Path(__file__).parent
DATA   = BASE / "all_experiments_combined.csv"
OUTDIR = BASE / "paper_subject_eval_outputs" / "trap1_figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

# ── Palette (colorblind-safe) ─────────────────────────────────────────────────
COL = {
    "fingerprint": "#7b2d8b",   # purple
    "overlap":     "#d62728",   # red
    "disjoint":    "#1f77b4",   # blue
    "ANOVA":       "#2ca02c",   # green
    "PCA":         "#ff7f0e",   # orange
    "MLP":         "#1f77b4",
    "XGBoost":     "#ff7f0e",
    "SVM":         "#2ca02c",
    "KNN":         "#d62728",
}
MODEL_ORDER = ["MLP", "XGBoost", "SVM", "KNN"]

# ── Load & segment data ───────────────────────────────────────────────────────
raw = pd.read_csv(DATA)

finger = raw[raw["experiment"].str.contains("W_F")].copy()
overlap = raw[raw["experiment"].str.contains("W_C")].copy()
disjoint = raw[
    (raw["experiment_type"] == "LPSO_Random_50") &
    (raw["holdout_size_P"] == 6)
].copy()
disjoint_p2 = raw[
    (raw["experiment_type"] == "LPSO_Random_50") &
    (raw["holdout_size_P"] == 2)
].copy()

def save(fig, name):
    path = OUTDIR / f"{name}.png"
    plt.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  {path}")

# ─────────────────────────────────────────────────────────────────────────────
# Design 1 — "The Inflation Side-by-Side"
# Left: Fingerprinting | Right: Overlap-prone vs Subject-disjoint disease
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)
fig.suptitle(
    "Trap 1: Subject overlap inflates disease classification accuracy\n"
    "Left: fingerprinting near-ceiling confirms subject-specific signal exists",
    fontsize=11, fontweight="bold",
)

# Panel A — Fingerprinting by model × feature set
ax = axes[0]
ax.set_title("A.  Subject fingerprinting accuracy\n(subject-ID classification, overlap-prone splits)",
             fontsize=9.5, fontweight="bold")
xticks, xticklabels = [], []
offset = {"ANOVA": -0.2, "PCA": 0.2}
for mi, model in enumerate(MODEL_ORDER):
    for fs in ["ANOVA", "PCA"]:
        vals = finger[(finger["model"] == model) & (finger["feature_set"] == fs)]["test_accuracy"].values
        xi = mi + offset[fs]
        ax.boxplot(vals, positions=[xi], widths=0.3, patch_artist=True,
                   boxprops=dict(facecolor=COL[fs], alpha=0.65),
                   medianprops=dict(color="black", linewidth=2),
                   whiskerprops=dict(linewidth=1.2),
                   flierprops=dict(marker="o", markersize=3, alpha=0.4))
    xticks.append(mi); xticklabels.append(model)
ax.set_xticks(xticks); ax.set_xticklabels(xticklabels, fontsize=11)
ax.axhline(0.5, color="red", linestyle="--", linewidth=1.3, alpha=0.7, label="Chance (0.5)")
ax.set_ylabel("Test accuracy", fontsize=11)
ax.set_ylim(0.25, 1.08)
ax.legend(handles=[
    mpatches.Patch(facecolor=COL["ANOVA"], label="ANOVA features"),
    mpatches.Patch(facecolor=COL["PCA"],   label="PCA features"),
    mpatches.Patch(facecolor="none", edgecolor="none", label=""),
    mpatches.Patch(facecolor="none", edgecolor="red",  label="Chance (0.5)", linestyle="--"),
], fontsize=8.5, loc="lower right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# Panel B — Disease classification: overlap vs disjoint, ANOVA only (clearer story)
ax = axes[1]
ax.set_title("B.  Disease classification accuracy\nRed = overlap-prone  |  Blue = subject-disjoint (LPSO)",
             fontsize=9.5, fontweight="bold")
offset2 = {"overlap": -0.22, "disjoint": 0.22}
for mi, model in enumerate(MODEL_ORDER):
    for cond, cdf, col in [("overlap", overlap, COL["overlap"]),
                             ("disjoint", disjoint, COL["disjoint"])]:
        vals = cdf[cdf["model"] == model]["test_accuracy"].values
        xi = mi + offset2[cond]
        ax.boxplot(vals, positions=[xi], widths=0.36, patch_artist=True,
                   boxprops=dict(facecolor=col, alpha=0.65),
                   medianprops=dict(color="black", linewidth=2),
                   whiskerprops=dict(linewidth=1.2),
                   flierprops=dict(marker="o", markersize=3, alpha=0.4))
ax.set_xticks(range(len(MODEL_ORDER))); ax.set_xticklabels(MODEL_ORDER, fontsize=11)
ax.axhline(0.5, color="red", linestyle="--", linewidth=1.3, alpha=0.7)
ax.legend(handles=[
    mpatches.Patch(facecolor=COL["overlap"],  label="Overlap-prone (within-subject split)"),
    mpatches.Patch(facecolor=COL["disjoint"], label="Subject-disjoint (LPSO, P=6)"),
], fontsize=8.5, loc="lower right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

save(fig, "trap1_design1_sidebyside")


# ─────────────────────────────────────────────────────────────────────────────
# Design 2 — "The Paired Drop" (slopegraph)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.set_title(
    "Trap 1: Accuracy drop from overlap-prone to subject-disjoint evaluation\n"
    "Every model and feature set declines; left endpoints approach fingerprinting ceiling",
    fontsize=10, fontweight="bold",
)

# Fingerprinting ceiling band
fp_med = finger["test_accuracy"].median()
fp_iqr_lo = finger["test_accuracy"].quantile(0.25)
fp_iqr_hi = finger["test_accuracy"].quantile(0.75)
ax.axhspan(fp_iqr_lo, fp_iqr_hi, color=COL["fingerprint"], alpha=0.12)
ax.axhline(fp_med, color=COL["fingerprint"], linewidth=1.5, linestyle="-", alpha=0.5)
ax.text(1.05, fp_med, "Fingerprinting\nceiling", color=COL["fingerprint"],
        fontsize=8, va="center", fontweight="bold")

ls_map = {"ANOVA": "-", "PCA": "--"}
for fs in ["ANOVA", "PCA"]:
    for model in MODEL_ORDER:
        ov_med = overlap[(overlap["model"]==model) & (overlap["feature_set"]==fs)]["test_accuracy"].median()
        dj_med = disjoint[(disjoint["model"]==model) & (disjoint["feature_set"]==fs)]["test_accuracy"].median()
        col = COL[model]
        ax.plot([0, 1], [ov_med, dj_med], color=col, linewidth=2.0,
                linestyle=ls_map[fs], alpha=0.85)
        ax.scatter([0], [ov_med], color=col, s=60, zorder=5)
        ax.scatter([1], [dj_med], color=col, s=60, zorder=5)
    # Label right endpoints for first feature set
    if fs == "ANOVA":
        for model in MODEL_ORDER:
            dj_med = disjoint[(disjoint["model"]==model) & (disjoint["feature_set"]==fs)]["test_accuracy"].median()
            ax.text(1.03, dj_med, model, color=COL[model], fontsize=8.5, va="center", fontweight="bold")

ax.axhline(0.5, color="red", linestyle=":", linewidth=1.4, alpha=0.7)
ax.text(1.05, 0.5, "Chance", color="red", fontsize=8, va="center")
ax.set_xlim(-0.15, 1.25)
ax.set_ylim(0.3, 1.05)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Overlap-prone\n(within-subject split)", "Subject-disjoint\n(LPSO, P=6)"],
                   fontsize=11, fontweight="bold")
ax.set_ylabel("Median test accuracy", fontsize=11)
ax.legend(handles=[
    mpatches.Patch(facecolor="gray",             label="Solid line = ANOVA features"),
    mpatches.Patch(facecolor="white", edgecolor="gray",  label="Dashed line = PCA features"),
    *[mpatches.Patch(facecolor=COL[m], label=m) for m in MODEL_ORDER],
    mpatches.Patch(facecolor=COL["fingerprint"], alpha=0.4, label="Fingerprinting median ± IQR"),
], fontsize=8, loc="lower left", ncol=2)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

save(fig, "trap1_design2_slopegraph")


# ─────────────────────────────────────────────────────────────────────────────
# Design 3 — "The ECDF Shift" (no boxplots)
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5.0), sharey=True, sharex=True)
fig.suptitle(
    "Trap 1: Full distribution of accuracy shifts toward chance under subject-disjoint evaluation",
    fontsize=11, fontweight="bold",
)

for ax, fs in zip(axes, ["ANOVA", "PCA"]):
    # Individual model ECDFs (thin)
    for model in MODEL_ORDER:
        for cond, cdf, col, lw, alpha in [
            ("overlap",  overlap,  COL["overlap"],  1.0, 0.35),
            ("disjoint", disjoint, COL["disjoint"], 1.0, 0.35),
        ]:
            vals = np.sort(cdf[(cdf["model"]==model) & (cdf["feature_set"]==fs)]["test_accuracy"].values)
            if len(vals) == 0: continue
            y = np.arange(1, len(vals)+1) / len(vals)
            ax.plot(vals, y, color=col, linewidth=lw, alpha=alpha)

    # Condition-average bold ECDF
    for cond, cdf, col in [
        ("overlap",  overlap,  COL["overlap"]),
        ("disjoint", disjoint, COL["disjoint"]),
    ]:
        vals = np.sort(cdf[cdf["feature_set"]==fs]["test_accuracy"].values)
        y = np.arange(1, len(vals)+1) / len(vals)
        med = np.median(vals)
        ax.plot(vals, y, color=col, linewidth=2.8, label=f"{cond.capitalize()} (median={med:.2f})")
        ax.axvline(med, color=col, linewidth=1.0, linestyle=":", alpha=0.7)

    # Fingerprinting reference
    fp_vals = np.sort(finger[finger["feature_set"]==fs]["test_accuracy"].values)
    if len(fp_vals):
        y_fp = np.arange(1, len(fp_vals)+1) / len(fp_vals)
        ax.plot(fp_vals, y_fp, color=COL["fingerprint"], linewidth=1.8,
                linestyle="-.", label=f"Fingerprinting (median={np.median(fp_vals):.2f})")

    ax.axvline(0.5, color="red", linewidth=1.3, linestyle="--", alpha=0.7, label="Chance (0.5)")
    ax.set_title(f"{'ANOVA' if fs=='ANOVA' else 'PCA'} features", fontsize=11, fontweight="bold")
    ax.set_xlabel("Test accuracy", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_xlim(0.25, 1.05)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

axes[0].set_ylabel("Cumulative fraction of runs", fontsize=10)

save(fig, "trap1_design3_ecdf")


# ─────────────────────────────────────────────────────────────────────────────
# Design 4 — "Schematic + Evidence Hybrid"
# Top row: leakage mechanism schematic | Bottom row: empirical boxplots
# ─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 8.5))
gs  = gridspec.GridSpec(2, 2, figure=fig, height_ratios=[1, 2.5], hspace=0.45, wspace=0.3)

# ── Schematic panels ─────────────────────────────────────────────────────────
for col_idx, (fs_label, split_label, colors, outcome) in enumerate([
    ("Random epoch split (overlap-prone)",
     "Same subject in TRAIN and TEST",
     {"train": "#d62728", "test": "#ff9999", "border": "#f5a623"},
     "Model learns subject identity → high disease accuracy"),
    ("Subject-disjoint split (LPSO)",
     "Train and test subjects never overlap",
     {"train": "#1f77b4", "test": "#aec7e8", "border": "#1f77b4"},
     "Model must generalise → honest disease accuracy"),
]):
    ax_s = fig.add_subplot(gs[0, col_idx])
    ax_s.set_xlim(0, 10); ax_s.set_ylim(0, 4); ax_s.axis("off")
    ax_s.set_title(fs_label, fontsize=10, fontweight="bold",
                   color=colors["train"], pad=4)

    # Draw subject rows
    for row, (subj, train_blocks, test_blocks) in enumerate([
        ("Subject A", [(0.2, 1.5), (2.0, 1.0), (4.5, 1.2)], [(3.5, 0.8), (6.0, 1.0)]),
        ("Subject B", [(0.5, 1.8), (3.0, 0.9), (5.5, 1.3)], [(2.0, 0.8), (7.0, 0.9)]),
    ]):
        y = 2.8 - row * 1.6
        ax_s.text(-0.1, y + 0.15, subj, fontsize=9, fontweight="bold", va="center")
        for (x, w) in train_blocks:
            ax_s.add_patch(mpatches.FancyBboxPatch((x, y), w, 0.4,
                boxstyle="round,pad=0.04", facecolor=colors["train"], alpha=0.75, edgecolor="none"))
        for (x, w) in test_blocks:
            fc = colors["test"]
            ec = colors["border"] if col_idx == 0 else "none"
            lw = 2.0 if col_idx == 0 else 0
            ax_s.add_patch(mpatches.FancyBboxPatch((x, y), w, 0.4,
                boxstyle="round,pad=0.04", facecolor=fc, alpha=0.85,
                edgecolor=ec, linewidth=lw))

    ax_s.text(5.0, 0.3, outcome, ha="center", fontsize=8.5, fontstyle="italic",
              color=colors["train"], fontweight="bold")
    ax_s.legend(handles=[
        mpatches.Patch(facecolor=colors["train"], alpha=0.75, label="Train epochs"),
        mpatches.Patch(facecolor=colors["test"],  alpha=0.85, label="Test epochs"),
    ], loc="upper right", fontsize=8)

# ── Empirical panels ──────────────────────────────────────────────────────────
for col_idx, fs in enumerate(["ANOVA", "PCA"]):
    ax_e = fig.add_subplot(gs[1, col_idx])

    # Fingerprinting reference band
    fp_med = finger[finger["feature_set"]==fs]["test_accuracy"].median()
    fp_lo  = finger[finger["feature_set"]==fs]["test_accuracy"].quantile(0.25)
    fp_hi  = finger[finger["feature_set"]==fs]["test_accuracy"].quantile(0.75)
    ax_e.axhspan(fp_lo, fp_hi, color=COL["fingerprint"], alpha=0.12)
    ax_e.axhline(fp_med, color=COL["fingerprint"], linewidth=1.4, linestyle="--", alpha=0.6,
                 label=f"Fingerprinting median ({fp_med:.2f})")

    off = {"overlap": -0.22, "disjoint": 0.22}
    for mi, model in enumerate(MODEL_ORDER):
        for cond, cdf, col in [("overlap", overlap, COL["overlap"]),
                                ("disjoint", disjoint, COL["disjoint"])]:
            vals = cdf[(cdf["model"]==model) & (cdf["feature_set"]==fs)]["test_accuracy"].values
            xi = mi + off[cond]
            ax_e.boxplot(vals, positions=[xi], widths=0.35, patch_artist=True,
                         boxprops=dict(facecolor=col, alpha=0.65),
                         medianprops=dict(color="black", linewidth=2),
                         whiskerprops=dict(linewidth=1.1),
                         flierprops=dict(marker="o", markersize=3, alpha=0.4))

    ax_e.axhline(0.5, color="red", linestyle=":", linewidth=1.3, alpha=0.7, label="Chance (0.5)")
    ax_e.set_xticks(range(len(MODEL_ORDER))); ax_e.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax_e.set_title(f"{'B' if col_idx==0 else 'C'}.  {fs} features — disease classification",
                   fontsize=10, fontweight="bold")
    ax_e.set_ylabel("Test accuracy" if col_idx==0 else "", fontsize=10)
    ax_e.set_ylim(0.25, 1.08)
    ax_e.legend(handles=[
        mpatches.Patch(facecolor=COL["overlap"],     label="Overlap-prone (within-subject)"),
        mpatches.Patch(facecolor=COL["disjoint"],    label="Subject-disjoint (LPSO P=6)"),
        mpatches.Patch(facecolor=COL["fingerprint"], alpha=0.4, label="Fingerprinting ± IQR"),
    ], fontsize=8, loc="lower right")
    ax_e.spines["top"].set_visible(False); ax_e.spines["right"].set_visible(False)

fig.suptitle(
    "Trap 1: How subject overlap creates a data leakage path\n"
    "Top: mechanism schematic  |  Bottom: empirical accuracy across conditions",
    fontsize=11, fontweight="bold", y=1.01,
)
save(fig, "trap1_design4_schematic_hybrid")


# ─────────────────────────────────────────────────────────────────────────────
# Design 5 — "The Raincloud" (no boxplots, P=6, ANOVA only for clarity)
# ─────────────────────────────────────────────────────────────────────────────
def half_violin(ax, vals, x, width=0.35, color="steelblue", alpha=0.7, side="right"):
    if len(vals) < 3: return
    kde = gaussian_kde(vals, bw_method=0.3)
    y_range = np.linspace(max(0.2, vals.min()-0.05), min(1.05, vals.max()+0.05), 200)
    density = kde(y_range)
    density = density / density.max() * width
    if side == "right":
        ax.fill_betweenx(y_range, x, x + density, color=color, alpha=alpha)
    else:
        ax.fill_betweenx(y_range, x - density, x, color=color, alpha=alpha)

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
fig.suptitle(
    "Trap 1: Distribution shape reveals the fingerprinting effect\n"
    "Overlap-prone distributions are tight and high; subject-disjoint are broad and lower",
    fontsize=11, fontweight="bold",
)

for ax, fs in zip(axes, ["ANOVA", "PCA"]):
    ax.set_title(f"{'ANOVA' if fs=='ANOVA' else 'PCA'} features", fontsize=11, fontweight="bold")

    # Reference: fingerprinting
    fp_med = finger[finger["feature_set"]==fs]["test_accuracy"].median()
    ax.axhline(fp_med, color=COL["fingerprint"], linewidth=1.5, linestyle="--", alpha=0.6,
               label=f"Fingerprinting median ({fp_med:.2f})")
    ax.axhline(0.5, color="red", linewidth=1.2, linestyle=":", alpha=0.7, label="Chance (0.5)")

    for mi, model in enumerate(MODEL_ORDER):
        xi = mi
        # Overlap-prone — half violin right + jitter + median tick
        ov_vals = overlap[(overlap["model"]==model) & (overlap["feature_set"]==fs)]["test_accuracy"].values
        dj_vals = disjoint[(disjoint["model"]==model) & (disjoint["feature_set"]==fs)]["test_accuracy"].values

        half_violin(ax, ov_vals, xi + 0.02, width=0.32, color=COL["overlap"], alpha=0.65, side="right")
        half_violin(ax, dj_vals, xi - 0.02, width=0.32, color=COL["disjoint"], alpha=0.65, side="left")

        # Jitter dots
        jit_ov = np.random.uniform(xi + 0.05, xi + 0.30, len(ov_vals))
        jit_dj = np.random.uniform(xi - 0.30, xi - 0.05, len(dj_vals))
        ax.scatter(jit_ov, ov_vals, color=COL["overlap"],  s=18, alpha=0.5, linewidths=0)
        ax.scatter(jit_dj, dj_vals, color=COL["disjoint"], s=18, alpha=0.5, linewidths=0)

        # Median ticks
        ax.plot([xi + 0.03, xi + 0.34], [np.median(ov_vals)]*2,
                color=COL["overlap"],  linewidth=2.5)
        ax.plot([xi - 0.34, xi - 0.03], [np.median(dj_vals)]*2,
                color=COL["disjoint"], linewidth=2.5)

    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax.set_ylim(0.25, 1.08)
    ax.legend(handles=[
        mpatches.Patch(facecolor=COL["overlap"],     label="Overlap-prone (within-subject)"),
        mpatches.Patch(facecolor=COL["disjoint"],    label="Subject-disjoint (LPSO P=6)"),
        mpatches.Patch(facecolor=COL["fingerprint"], alpha=0.5, label="Fingerprinting median"),
    ], fontsize=8.5, loc="lower right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

axes[0].set_ylabel("Test accuracy", fontsize=11)

save(fig, "trap1_design5_raincloud")


# ─────────────────────────────────────────────────────────────────────────────
# Design 6 — "The Delta Panel" (overlap minus disjoint)
# Uses within-subject overlap medians vs LPSO disjoint per-fold bootstrap
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5.0), sharey=True)
fig.suptitle(
    "Trap 1: Accuracy inflation = overlap-prone accuracy − subject-disjoint accuracy\n"
    "Points above zero represent folds/runs where subject overlap inflated reported performance",
    fontsize=11, fontweight="bold",
)

# For each (model, feature_set): bootstrap delta distributions
# Sample overlap_vals with replacement, sample disjoint_vals with replacement, compute median diff
N_BOOT = 800

for ax, fs in zip(axes, ["ANOVA", "PCA"]):
    ax.axhline(0, color="black", linewidth=1.8, linestyle="--")
    ax.axhspan(0, 0.6, color="#e74c3c", alpha=0.06)
    ax.text(3.6, 0.55, "Overlap inflates ↑", color="#c0392b", fontsize=8.5, ha="right", fontstyle="italic")

    for mi, model in enumerate(MODEL_ORDER):
        ov = overlap[(overlap["model"]==model) & (overlap["feature_set"]==fs)]["test_accuracy"].values
        dj = disjoint[(disjoint["model"]==model) & (disjoint["feature_set"]==fs)]["test_accuracy"].values
        if len(ov) == 0 or len(dj) == 0: continue

        # bootstrap: resample each independently, compute median difference
        deltas = [
            np.median(np.random.choice(ov, len(ov), replace=True)) -
            np.median(np.random.choice(dj, len(dj), replace=True))
            for _ in range(N_BOOT)
        ]
        deltas = np.array(deltas)
        pct_above = (deltas > 0).mean() * 100

        # Violin
        kde = gaussian_kde(deltas, bw_method=0.3)
        yy  = np.linspace(deltas.min()-0.01, deltas.max()+0.01, 200)
        dd  = kde(yy); dd = dd / dd.max() * 0.35
        ax.fill_betweenx(yy, mi - dd, mi + dd, color=COL[model], alpha=0.55)
        ax.scatter(mi, np.median(deltas), color=COL[model], s=70, zorder=5)
        ax.text(mi, deltas.max() + 0.01, f"{pct_above:.0f}%\nabove 0",
                ha="center", fontsize=7.5, color=COL[model], fontweight="bold")

    ax.set_xticks(range(len(MODEL_ORDER)))
    ax.set_xticklabels(MODEL_ORDER, fontsize=11)
    ax.set_title(f"{'ANOVA' if fs=='ANOVA' else 'PCA'} features", fontsize=11, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

axes[0].set_ylabel("Δ accuracy  (overlap − disjoint)", fontsize=11)
axes[0].legend(handles=[mpatches.Patch(facecolor=COL[m], label=m) for m in MODEL_ORDER],
               fontsize=9, loc="upper left")

save(fig, "trap1_design6_delta_panel")


print(f"\nAll 6 figures saved to:\n  {OUTDIR}/")
