#!/usr/bin/env python3
"""
figA.1.7.1 — figA.1.7 with the middle (epoch-count) panel removed.
Two panels only:
  Left:  stacked bars by class colour, hatch = misclassified
  Right: epoch accuracy vs subject-label accuracy comparison
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

matplotlib.use("Agg")

BASE   = Path(__file__).parent
PREDS  = BASE / "paper_subject_eval_outputs" / "per_subject_fold_predictions.csv"
MERGED = BASE / "paper_subject_eval_outputs" / "fold_epoch_vs_subject_merged.csv"
OUTDIR = BASE / "paper_subject_eval_outputs" / "epoch_subject_mismatch_figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

CLASS_COL = {0: "#27ae60", 1: "#2980b9"}   # green=Control, blue=AD

# ── Load figA.1 fold ──────────────────────────────────────────────────────────
merged   = pd.read_csv(MERGED)
preds_df = pd.read_csv(PREDS)
merged["mismatch"] = (merged["epoch_acc"] - merged["subject_acc"]) * 100
m6   = merged[merged["P"] == 6]
case = m6[m6["pipeline"] == "FTest"].nlargest(1, "mismatch").iloc[0]

fp = preds_df[
    (preds_df["experiment"] == case["experiment"]) &
    (preds_df["pipeline"]   == case["pipeline"])   &
    (preds_df["strategy"]   == case["strategy"])   &
    (preds_df["P"]          == case["P"])           &
    (preds_df["fold_id"]    == case["fold_id"])     &
    (preds_df["model"]      == case["model"])       &
    (preds_df["hyperparams"]== case["hyperparams"])
].copy()

subjects      = fp["SubjectID"].values
true_labels   = fp["true_subject_label"].values.astype(int)
correct       = fp["subject_correct"].values.astype(bool)
n_epochs      = fp["n_epochs"].values.astype(float)
ad_ratio      = fp["ad_ratio"].values
correct_votes = (ad_ratio * n_epochs).round().astype(int)
other_votes   = (n_epochs - correct_votes).astype(int)
# Sort by epoch count descending (most epochs on the left)
order         = np.argsort(n_epochs)[::-1]
subjects      = subjects[order]
true_labels   = true_labels[order]
correct       = correct[order]
n_epochs      = n_epochs[order]
correct_votes = correct_votes[order]
other_votes   = other_votes[order]

x             = np.arange(len(subjects))

epoch_acc_pct   = case["epoch_acc"]   * 100
subject_acc_pct = case["subject_acc"] * 100
delta           = epoch_acc_pct - subject_acc_pct

# ── Figure: 2 panels ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5.8))
fig.suptitle(
    f"figA.1 — ANOVA (F-test)  |  Experiment: {case['experiment']}  "
    f"|  Strategy: {case['strategy']}  |  Model: {case['model']}\n"
    f"Epoch acc = {epoch_acc_pct:.1f}%  |  Subject-label acc = {subject_acc_pct:.1f}%  "
    f"|  Δ = {delta:+.1f} pp",
    fontsize=9, fontweight="bold", y=1.02,
)

# ── Panel 1: stacked bars, class colour, hatch = misclassified ───────────────
ax = axes[0]
for i, (cv, ov, tl, c) in enumerate(zip(correct_votes, other_votes, true_labels, correct)):
    col = CLASS_COL[tl]
    ax.bar(i, cv, color=col, edgecolor="black", linewidth=0.7,
           alpha=0.85, width=0.6)
    ax.bar(i, ov, bottom=cv, color=col, edgecolor="black",
           linewidth=0.7, alpha=0.25, width=0.6)

for i, (cv, ne, c) in enumerate(zip(correct_votes, n_epochs, correct)):
    sym_col = "#27ae60" if c else "#e74c3c"
    sym     = "✓" if c else "✗"
    # Large symbol above the bar
    ax.text(i, ne + n_epochs.max() * 0.03,
            sym, ha="center", va="bottom", fontsize=22,
            fontweight="bold", color=sym_col)
    # Smaller vote ratio below the symbol
    ax.text(i, ne + n_epochs.max() * 0.01,
            f"{cv}/{int(ne)}",
            ha="center", va="bottom", fontsize=7.5, color="#333333")

ax.set_xticks(x)
ax.set_xticklabels([f"Sub-{s}" for s in subjects], rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\n"
             "Colour = class  |  ✓ = correctly classified  |  ✗ = misclassified",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.28)
ax.legend(handles=[
    mpatches.Patch(facecolor=CLASS_COL[0], label="Control subject"),
    mpatches.Patch(facecolor=CLASS_COL[1], label="Alzheimer's subject"),
], fontsize=8.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# ── Panel 2: epoch acc vs subject-label acc ───────────────────────────────────
ax = axes[1]
vals = [epoch_acc_pct, subject_acc_pct]
bar3 = ax.bar([0, 1], vals, color=["#4a9ede", "#e07b39"],
              edgecolor="black", linewidth=0.9, alpha=0.88, width=0.55)
hi, lo = max(vals), min(vals)
hi_x = 0 if vals[0] > vals[1] else 1; lo_x = 1 - hi_x
ax.fill_between([lo_x - 0.275, lo_x + 0.275], lo, hi,
                color="#ffeb3b", alpha=0.55, zorder=0,
                label=f"Gap = {abs(delta):.1f} pp")
ax.axhline(50, color="red", linestyle="--", linewidth=1.4, alpha=0.7, label="50% chance level")
for bar, val in zip(bar3, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 1.2,
            f"{val:.1f}%", ha="center", fontsize=13, fontweight="bold")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Epoch accuracy\n(weighted by epoch count)",
                    "Subject-label accuracy\n(1 vote per subject)"], fontsize=9.5)
ax.set_ylabel("Accuracy (%)", fontsize=10)
ax.set_title("The mismatch: two ways to aggregate\nYellow band = gap between the two metrics",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, 115)
ax.legend(fontsize=8, loc="upper left")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

plt.tight_layout()
out = OUTDIR / "figA.1.7.1_mismatch_variants.png"
fig.savefig(out, dpi=140, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out}")
