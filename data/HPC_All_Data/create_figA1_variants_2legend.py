#!/usr/bin/env python3
"""
figA.1.6–11 — Variants of figA.1 leftmost panel with exactly 2 legend items.

Since classification is binary (Control=0 / AD=1), every epoch votes for
exactly one of two labels — so "other votes" IS just "votes for the other class".
This lets us reduce to 2 legend entries while moving class/outcome info into
x-tick labels, bar text, or hatch patterns instead.

Variants:
  figA.1.6  — 2-colour by OUTCOME; class shown in x-tick label
  figA.1.7  — 2-colour by CLASS; outcome shown as hatch (misclassified = hatched)
  figA.1.8  — 2-colour by VOTE DIRECTION (true-label vs opposite-label votes); class+outcome in x-tick
  figA.1.9  — 2-colour by CLASS; only correct-label votes shown (no stacking); total as ghost bar
  figA.1.10 — 2-colour by OUTCOME; vote % printed inside bar; class badge above
  figA.1.11 — Diverging bars: true-label votes go UP, opposite-label votes go DOWN; 2-item legend
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

CLASS_NAME = {0: "Ctrl", 1: "AD"}
CLASS_FULL = {0: "Control", 1: "Alzheimer's"}
CLASS_COL  = {0: "#27ae60", 1: "#2980b9"}      # green=Control, blue=AD
OUT_COL    = {True: "#2ecc71", False: "#e74c3c"} # green=correct, red=wrong

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
pred_labels   = fp["pred_subject_label"].values.astype(int)
correct       = fp["subject_correct"].values.astype(bool)
n_epochs      = fp["n_epochs"].values.astype(float)
ad_ratio      = fp["ad_ratio"].values
correct_votes = (ad_ratio * n_epochs).round().astype(int)
other_votes   = (n_epochs - correct_votes).astype(int)
x             = np.arange(len(subjects))

epoch_acc_pct   = case["epoch_acc"]   * 100
subject_acc_pct = case["subject_acc"] * 100
delta           = epoch_acc_pct - subject_acc_pct
ep_thresh       = np.median(n_epochs)
ep_colors       = ["#4a9ede" if n >= ep_thresh else "#f5a623" for n in n_epochs]

SUPTITLE = (
    f"figA.1 — ANOVA (F-test)  |  Experiment: {case['experiment']}  "
    f"|  Strategy: {case['strategy']}  |  Model: {case['model']}\n"
    f"Epoch acc = {epoch_acc_pct:.1f}%  |  Subject-label acc = {subject_acc_pct:.1f}%  "
    f"|  Δ = {delta:+.1f} pp"
)

# ── Shared panels 2 & 3 ───────────────────────────────────────────────────────
def add_panels_2_3(axes):
    ax = axes[1]
    ax.bar(x, n_epochs, color=ep_colors, edgecolor="black", linewidth=0.7, alpha=0.85, width=0.6)
    ax.axhline(ep_thresh, color="black", linestyle=":", linewidth=1.2, alpha=0.6,
               label=f"Median: {ep_thresh:.0f} epochs")
    for i, ne in enumerate(n_epochs):
        ax.text(i, ne + n_epochs.max() * 0.015, f"{int(ne)}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([f"Sub-{s}" for s in subjects], rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Total number of epochs", fontsize=10)
    ax.set_title("Epoch count per subject\nBlue = above median  |  Orange = below median",
                 fontsize=8.5, fontweight="bold")
    ax.set_ylim(0, n_epochs.max() * 1.18)
    ax.legend(handles=[
        mpatches.Patch(facecolor="#4a9ede", label=f"≥{ep_thresh:.0f} epochs (above median)"),
        mpatches.Patch(facecolor="#f5a623", label=f"<{ep_thresh:.0f} epochs (below median)"),
    ], fontsize=7.5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    ax = axes[2]
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


def save_fig(fig, variant, suffix=""):
    path = OUTDIR / f"figA.1.{variant}_mismatch_variants.png"
    plt.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: figA.1.{variant}_mismatch_variants.png  {suffix}")


# ═══════════════════════════════════════════════════════════════════════════════
# Variant 6 — 2 colours by OUTCOME; class in x-tick label
# Legend: "✓ Correctly classified subject" / "✗ Misclassified subject"
# Bar = true-label votes (bottom, coloured) + opposite-label votes (top, lighter)
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]

bot_cols = [OUT_COL[c] for c in correct]
top_cols = [(*matplotlib.colors.to_rgb(OUT_COL[c]), 0.30) for c in correct]

for i, (cv, ov, bc, tc) in enumerate(zip(correct_votes, other_votes, bot_cols, top_cols)):
    ax.bar(i, cv, color=bc, edgecolor="black", linewidth=0.7, alpha=0.88, width=0.6)
    ax.bar(i, ov, bottom=cv, color=tc[:3], edgecolor="black",
           linewidth=0.7, alpha=0.35, width=0.6)

for i, (cv, ne) in enumerate(zip(correct_votes, n_epochs)):
    ax.text(i, ne + n_epochs.max() * 0.02, f"{cv}/{int(ne)}",
            ha="center", fontsize=8, fontweight="bold")

tick_labels = [f"Sub-{s}\n({CLASS_NAME[tl]})" for s, tl in zip(subjects, true_labels)]
ax.set_xticks(x); ax.set_xticklabels(tick_labels, fontsize=9)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\n"
             "Colour = outcome  |  Class shown in x-axis label",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.18)
ax.legend(handles=[
    mpatches.Patch(facecolor=OUT_COL[True],  label="✓  Correctly classified subject"),
    mpatches.Patch(facecolor=OUT_COL[False], label="✗  Misclassified subject"),
], fontsize=8.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes)
save_fig(fig, 6, "(2-colour by outcome, class in x-tick)")


# ═══════════════════════════════════════════════════════════════════════════════
# Variant 7 — 2 colours by CLASS; misclassified = hatched
# Legend: "Control subject" / "Alzheimer's subject"
# Outcome conveyed by hatch (solid = correct, hatched = misclassified)
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]

for i, (cv, ov, tl, c) in enumerate(zip(correct_votes, other_votes, true_labels, correct)):
    hatch = None if c else "////"
    col   = CLASS_COL[tl]
    ax.bar(i, cv, color=col, edgecolor="black", linewidth=0.7,
           alpha=0.85, width=0.6, hatch=hatch)
    ax.bar(i, ov, bottom=cv, color=col, edgecolor="black",
           linewidth=0.7, alpha=0.25, width=0.6, hatch=hatch)

for i, (cv, ne, c) in enumerate(zip(correct_votes, n_epochs, correct)):
    ax.text(i, ne + n_epochs.max() * 0.02,
            f"{'✓' if c else '✗'} {cv}/{int(ne)}",
            ha="center", fontsize=8, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels([f"Sub-{s}" for s in subjects], rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\n"
             "Colour = class  |  Hatched = misclassified  |  Solid = correctly classified",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.18)
ax.legend(handles=[
    mpatches.Patch(facecolor=CLASS_COL[0], label="Control subject  (hatched if misclassified)"),
    mpatches.Patch(facecolor=CLASS_COL[1], label="Alzheimer's subject  (hatched if misclassified)"),
], fontsize=8.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes)
save_fig(fig, 7, "(2-colour by class, hatch=misclassified)")


# ═══════════════════════════════════════════════════════════════════════════════
# Variant 8 — 2 colours by VOTE DIRECTION (true-label vs opposite-label)
# Legend: "Votes for subject's true label" / "Votes for opposite label"
# Class + outcome in x-tick: "Sub-27 Ctrl ✓"
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]

TRUE_COL  = "#3d6fad"   # muted blue — "voted correctly"
OTHER_COL = "#b0b0b0"   # gray — "voted for the other class"

for i, (cv, ov, tl, c) in enumerate(zip(correct_votes, other_votes, true_labels, correct)):
    edge_col = "#1a1a1a" if c else "#cc0000"
    ax.bar(i, cv, color=TRUE_COL, edgecolor=edge_col, linewidth=1.4, alpha=0.85, width=0.6)
    ax.bar(i, ov, bottom=cv, color=OTHER_COL, edgecolor=edge_col, linewidth=1.4, alpha=0.7, width=0.6)

for i, (cv, ne) in enumerate(zip(correct_votes, n_epochs)):
    ax.text(i, ne + n_epochs.max() * 0.02, f"{cv}/{int(ne)}",
            ha="center", fontsize=8, fontweight="bold")

tick_labels = [
    f"Sub-{s}  {CLASS_NAME[tl]} {'✓' if c else '✗'}"
    for s, tl, c in zip(subjects, true_labels, correct)
]
ax.set_xticks(x); ax.set_xticklabels(tick_labels, rotation=25, ha="right", fontsize=8.5)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\n"
             "Class + outcome in x-axis  |  Red border = misclassified",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.18)
ax.legend(handles=[
    mpatches.Patch(facecolor=TRUE_COL,  label="Votes for subject's true label"),
    mpatches.Patch(facecolor=OTHER_COL, label="Votes for the opposite label"),
], fontsize=8.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes)
save_fig(fig, 8, "(2-colour by vote direction, class+outcome in x-tick)")


# ═══════════════════════════════════════════════════════════════════════════════
# Variant 9 — 2 colours by CLASS; no stacking; only correct-label votes shown
# Total epochs shown as a faint ghost bar behind
# Legend: "Control subject" / "Alzheimer's subject"
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]

for i, (cv, ne, tl, c) in enumerate(zip(correct_votes, n_epochs, true_labels, correct)):
    # Ghost = total epochs
    ax.bar(i, ne, color=CLASS_COL[tl], edgecolor="black", linewidth=0.5,
           alpha=0.18, width=0.6)
    # Solid = correct-label votes
    hatch = None if c else "////"
    ax.bar(i, cv, color=CLASS_COL[tl], edgecolor="black", linewidth=0.9,
           alpha=0.85, width=0.6, hatch=hatch,
           label=CLASS_FULL[tl] if i == [k for k, t in enumerate(true_labels) if t == tl][0] else "_nolegend_")
    ax.text(i, ne + n_epochs.max() * 0.02,
            f"{'✓' if c else '✗'}  {cv}/{int(ne)}",
            ha="center", fontsize=8, fontweight="bold",
            color=CLASS_COL[tl])

ax.set_xticks(x)
ax.set_xticklabels([f"Sub-{s}" for s in subjects], rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Epoch votes for true label", fontsize=10)
ax.set_title("True-label votes per subject  (faint bar = total epochs)\n"
             "Hatched = misclassified  |  ✓/✗ shows outcome",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.22)
ax.legend(handles=[
    mpatches.Patch(facecolor=CLASS_COL[0], label="Control subject  (hatched if misclassified)"),
    mpatches.Patch(facecolor=CLASS_COL[1], label="Alzheimer's subject  (hatched if misclassified)"),
], fontsize=8.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes)
save_fig(fig, 9, "(class colour, ghost bar for total epochs)")


# ═══════════════════════════════════════════════════════════════════════════════
# Variant 10 — 2 colours by OUTCOME; vote % printed inside bar; class badge above
# Legend: "✓ Correctly classified" / "✗ Misclassified"
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]

for i, (cv, ov, ne, ratio, tl, c) in enumerate(
        zip(correct_votes, other_votes, n_epochs, ad_ratio, true_labels, correct)):
    col = OUT_COL[c]
    ax.bar(i, cv, color=col, edgecolor="black", linewidth=0.7, alpha=0.88, width=0.6)
    ax.bar(i, ov, bottom=cv, color=col, edgecolor="black", linewidth=0.7, alpha=0.28, width=0.6)
    # Vote % inside the coloured section
    if cv > ne * 0.10:
        ax.text(i, cv / 2, f"{ratio*100:.0f}%", ha="center", va="center",
                fontsize=9, color="white", fontweight="bold")
    # Class badge above bar
    ax.text(i, ne + n_epochs.max() * 0.04,
            CLASS_NAME[tl],
            ha="center", fontsize=9, fontweight="bold", color=CLASS_COL[tl])

ax.set_xticks(x)
ax.set_xticklabels([f"Sub-{s}" for s in subjects], rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\n"
             "% inside bar = fraction voting for true label  |  Class badge above",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.22)
ax.legend(handles=[
    mpatches.Patch(facecolor=OUT_COL[True],  label="✓  Correctly classified subject"),
    mpatches.Patch(facecolor=OUT_COL[False], label="✗  Misclassified subject"),
], fontsize=8.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes)
save_fig(fig, 10, "(outcome colour, % inside, class badge above)")


# ═══════════════════════════════════════════════════════════════════════════════
# Variant 11 — Diverging bars: true-label votes UP, opposite-label votes DOWN
# Baseline = 0; bar above = correct-label votes; bar below = opposite-label votes
# Legend: "Votes for subject's true label (↑)" / "Votes for opposite label (↓)"
# Class + outcome in x-tick
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]

TRUE_UP  = "#3d6fad"
OTHER_DN = "#c0392b"

max_half = n_epochs.max()
for i, (cv, ov, tl, c) in enumerate(zip(correct_votes, other_votes, true_labels, correct)):
    edge = "#1a1a1a"
    ax.bar(i,  cv, color=TRUE_UP,  edgecolor=edge, linewidth=0.8, alpha=0.85, width=0.6)
    ax.bar(i, -ov, color=OTHER_DN, edgecolor=edge, linewidth=0.8, alpha=0.65, width=0.6)
    ax.text(i,  cv + max_half * 0.025, f"{cv}", ha="center", fontsize=7.5, color=TRUE_UP,  fontweight="bold")
    ax.text(i, -ov - max_half * 0.045, f"{int(ov)}", ha="center", fontsize=7.5, color=OTHER_DN, fontweight="bold")

ax.axhline(0, color="black", linewidth=1.0)
tick_labels = [
    f"Sub-{s}\n{CLASS_NAME[tl]} {'✓' if c else '✗'}"
    for s, tl, c in zip(subjects, true_labels, correct)
]
ax.set_xticks(x); ax.set_xticklabels(tick_labels, fontsize=9)
ax.set_ylabel("← Opposite-label votes  |  True-label votes →", fontsize=9)
ax.set_title("Epoch votes per subject — diverging view\n"
             "↑ Votes for true label  |  ↓ Votes for opposite label",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(-max_half * 1.15, max_half * 1.15)
ax.legend(handles=[
    mpatches.Patch(facecolor=TRUE_UP,  label="↑  Votes for subject's true label"),
    mpatches.Patch(facecolor=OTHER_DN, label="↓  Votes for the opposite label"),
], fontsize=8.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes)
save_fig(fig, 11, "(diverging bars: true-label up, opposite down)")


print(f"\nAll figA.1.6–11 files saved to:\n  {OUTDIR}")
