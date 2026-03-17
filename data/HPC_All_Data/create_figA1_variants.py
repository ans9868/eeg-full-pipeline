#!/usr/bin/env python3
"""
figA.1.x — Five variants of the leftmost panel of figA.1.
Each variant changes how the stacked bar legend / labelling is presented
so the class membership (Control vs Alzheimer's) is immediately readable.

Variants:
  figA.1.1 — Subject-class in x-axis labels  ("Sub-27 (Ctrl ✓)")
  figA.1.2 — 4-colour legend (class × outcome)
  figA.1.3 — Full true→pred mapping in x-axis  ("Sub-27  Ctrl→Ctrl ✓")
  figA.1.4 — Subjects grouped by class (all Controls left, ADs right)
  figA.1.5 — Vote-fraction bar + class background shading

Panels 2 & 3 (epoch counts and accuracy comparison) are unchanged from figA.1.
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

CLASS_NAMES = {0: "Ctrl", 1: "AD"}          # change here if labels differ
CLASS_FULL  = {0: "Control", 1: "Alzheimer's"}

# ── Load figA.1 fold data ─────────────────────────────────────────────────────
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

subjects       = fp["SubjectID"].values
true_labels    = fp["true_subject_label"].values.astype(int)
pred_labels    = fp["pred_subject_label"].values.astype(int)
correct        = fp["subject_correct"].values.astype(bool)
n_epochs       = fp["n_epochs"].values.astype(float)
ad_ratio       = fp["ad_ratio"].values
correct_votes  = (ad_ratio * n_epochs).round().astype(int)
other_votes    = (n_epochs - correct_votes).astype(int)

epoch_acc_pct   = case["epoch_acc"]   * 100
subject_acc_pct = case["subject_acc"] * 100
delta           = epoch_acc_pct - subject_acc_pct
ep_thresh       = np.median(n_epochs)
ep_colors       = ["#4a9ede" if n >= ep_thresh else "#f5a623" for n in n_epochs]

# ── Colour palettes for the 4-class scheme ───────────────────────────────────
# (class, outcome) → hex
COL = {
    (0, True):  "#2ecc71",   # Control, correct  — strong green
    (0, False): "#f39c12",   # Control, wrong    — amber
    (1, True):  "#3498db",   # AD, correct       — blue
    (1, False): "#e74c3c",   # AD, wrong         — red
}

# ── Shared helpers ────────────────────────────────────────────────────────────
def add_panels_2_3(axes, x):
    """Draw panels 2 and 3 identically for all variants."""
    # Panel 2 — epoch counts
    ax = axes[1]
    bars2 = ax.bar(x, n_epochs, color=ep_colors, edgecolor="black",
                   linewidth=0.7, alpha=0.85, width=0.6)
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
    legend_ep = [
        mpatches.Patch(facecolor="#4a9ede", label=f"≥{ep_thresh:.0f} epochs (above median)"),
        mpatches.Patch(facecolor="#f5a623", label=f"<{ep_thresh:.0f} epochs (below median)"),
    ]
    ax.legend(handles=legend_ep, fontsize=7.5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    # Panel 3 — accuracy comparison
    ax = axes[2]
    vals = [epoch_acc_pct, subject_acc_pct]
    cols = ["#4a9ede", "#e07b39"]
    bar3 = ax.bar([0, 1], vals, color=cols, edgecolor="black",
                  linewidth=0.9, alpha=0.88, width=0.55)
    hi, lo = max(vals), min(vals)
    hi_x = 0 if vals[0] > vals[1] else 1
    lo_x = 1 - hi_x
    ax.fill_between([lo_x - 0.275, lo_x + 0.275], lo, hi,
                    color="#ffeb3b", alpha=0.55, zorder=0,
                    label=f"Gap = {abs(delta):.1f} pp  (epoch over-estimates subject-label acc)")
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


SUPTITLE = (
    f"figA.1 — ANOVA (F-test) pipeline  |  Experiment: {case['experiment']}  "
    f"|  Strategy: {case['strategy']}  |  Model: {case['model']}\n"
    f"Epoch acc = {epoch_acc_pct:.1f}%  |  Subject-label acc = {subject_acc_pct:.1f}%  "
    f"|  Δ = {delta:+.1f} pp"
)

# ═══════════════════════════════════════════════════════════════════════════════
#  Variant 1 — class + outcome in x-tick labels
#  "Sub-27 (Ctrl ✓)"  /  "Sub-61 (AD ✗)"
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]
x = np.arange(len(subjects))
bot_cols = [COL[(tl, c)] for tl, c in zip(true_labels, correct)]
ax.bar(x, correct_votes, color=bot_cols, edgecolor="black",
       linewidth=0.7, alpha=0.85, width=0.6, label="Correct-label votes")
ax.bar(x, other_votes, bottom=correct_votes, color="#cccccc",
       edgecolor="black", linewidth=0.7, alpha=0.6, width=0.6, label="Other-label votes")
for i, (cv, ne) in enumerate(zip(correct_votes, n_epochs)):
    ax.text(i, ne + n_epochs.max() * 0.02, f"{cv}/{int(ne)}",
            ha="center", fontsize=7.5, fontweight="bold")
tick_labels = [
    f"Sub-{s}\n({CLASS_NAMES[tl]} {'✓' if c else '✗'})"
    for s, tl, c in zip(subjects, true_labels, correct)
]
ax.set_xticks(x); ax.set_xticklabels(tick_labels, fontsize=8.5)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\nX-axis shows true class and outcome",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.18)
legend_items = [
    mpatches.Patch(facecolor=COL[(0, True)],  label="Correct-label votes — Control, correctly classified"),
    mpatches.Patch(facecolor=COL[(0, False)], label="Correct-label votes — Control, misclassified"),
    mpatches.Patch(facecolor=COL[(1, True)],  label="Correct-label votes — AD, correctly classified"),
    mpatches.Patch(facecolor=COL[(1, False)], label="Correct-label votes — AD, misclassified"),
    mpatches.Patch(facecolor="#cccccc",        label="Votes for other labels"),
]
ax.legend(handles=legend_items, fontsize=7.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes, x)
save_fig(fig, 1, "(class in x-tick labels)")


# ═══════════════════════════════════════════════════════════════════════════════
#  Variant 2 — 4-colour bars, minimal x-tick labels
#  Legend clearly says: "Correct-label votes for Control subject (correctly classified)" etc.
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]
x = np.arange(len(subjects))
bot_cols = [COL[(tl, c)] for tl, c in zip(true_labels, correct)]
ax.bar(x, correct_votes, color=bot_cols, edgecolor="black",
       linewidth=0.7, alpha=0.88, width=0.6)
ax.bar(x, other_votes, bottom=correct_votes, color="#dddddd",
       edgecolor="black", linewidth=0.7, alpha=0.6, width=0.6)
for i, (cv, ne) in enumerate(zip(correct_votes, n_epochs)):
    ax.text(i, ne + n_epochs.max() * 0.02, f"{cv}/{int(ne)}",
            ha="center", fontsize=7.5, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([f"Sub-{s}" for s in subjects], rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\nBar colour = (subject class) × (correctly classified?)",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.25)
legend_items = [
    mpatches.Patch(facecolor=COL[(0, True)],  label="Correct-label votes for Control subject  (classified correctly)"),
    mpatches.Patch(facecolor=COL[(0, False)], label="Correct-label votes for Control subject  (misclassified)"),
    mpatches.Patch(facecolor=COL[(1, True)],  label="Correct-label votes for Alzheimer's subject  (classified correctly)"),
    mpatches.Patch(facecolor=COL[(1, False)], label="Correct-label votes for Alzheimer's subject  (misclassified)"),
    mpatches.Patch(facecolor="#dddddd",        label="Votes for other subject labels"),
]
ax.legend(handles=legend_items, fontsize=7.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes, x)
save_fig(fig, 2, "(4-colour legend: class × outcome)")


# ═══════════════════════════════════════════════════════════════════════════════
#  Variant 3 — Full true→pred mapping in x-tick labels
#  "Sub-27\nCtrl → Ctrl ✓"   /   "Sub-61\nAD → Ctrl ✗"
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]
x = np.arange(len(subjects))
bot_cols = [COL[(tl, c)] for tl, c in zip(true_labels, correct)]
ax.bar(x, correct_votes, color=bot_cols, edgecolor="black",
       linewidth=0.7, alpha=0.85, width=0.6)
ax.bar(x, other_votes, bottom=correct_votes, color="#cccccc",
       edgecolor="black", linewidth=0.7, alpha=0.6, width=0.6)
for i, (cv, ne) in enumerate(zip(correct_votes, n_epochs)):
    ax.text(i, ne + n_epochs.max() * 0.02, f"{cv}/{int(ne)}",
            ha="center", fontsize=7.5, fontweight="bold")
tick_labels = [
    f"Sub-{s}\n{CLASS_NAMES[tl]}→{CLASS_NAMES[pl]} {'✓' if c else '✗'}"
    for s, tl, pl, c in zip(subjects, true_labels, pred_labels, correct)
]
ax.set_xticks(x); ax.set_xticklabels(tick_labels, fontsize=8.5)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\nX-axis: True class → Predicted class",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.18)
legend_items = [
    mpatches.Patch(facecolor=COL[(0, True)],  label="Correct-label votes — Control subject (correct prediction)"),
    mpatches.Patch(facecolor=COL[(0, False)], label="Correct-label votes — Control subject (wrong prediction)"),
    mpatches.Patch(facecolor=COL[(1, True)],  label="Correct-label votes — AD subject (correct prediction)"),
    mpatches.Patch(facecolor=COL[(1, False)], label="Correct-label votes — AD subject (wrong prediction)"),
    mpatches.Patch(facecolor="#cccccc",        label="Votes for other labels"),
]
ax.legend(handles=legend_items, fontsize=7.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes, x)
save_fig(fig, 3, "(full true→pred in x-tick labels)")


# ═══════════════════════════════════════════════════════════════════════════════
#  Variant 4 — Subjects grouped by class (Controls left, ADs right)
#  Background shading per group makes the class split immediately obvious
# ═══════════════════════════════════════════════════════════════════════════════
ctrl_mask = true_labels == 0
ad_mask   = true_labels == 1
ctrl_idx  = np.where(ctrl_mask)[0]
ad_idx    = np.where(ad_mask)[0]
# Reorder: all Controls first, then all ADs
order     = list(ctrl_idx) + list(ad_idx)
n_ctrl    = ctrl_mask.sum()

fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]
x = np.arange(len(subjects))

# Draw background bands
ax.axvspan(-0.5, n_ctrl - 0.5,     color="#d5e8d4", alpha=0.35, zorder=0, label="_nolegend_")
ax.axvspan(n_ctrl - 0.5, len(subjects) - 0.5, color="#dae8fc", alpha=0.35, zorder=0, label="_nolegend_")

bot_cols_ord = [COL[(true_labels[i], correct[i])] for i in order]
cv_ord = correct_votes[order]; ov_ord = other_votes[order]; ne_ord = n_epochs[order]
sub_ord = subjects[order]; tl_ord = true_labels[order]; pl_ord = pred_labels[order]; c_ord = correct[order]

ax.bar(x, cv_ord, color=bot_cols_ord, edgecolor="black",
       linewidth=0.7, alpha=0.85, width=0.6)
ax.bar(x, ov_ord, bottom=cv_ord, color="#cccccc",
       edgecolor="black", linewidth=0.7, alpha=0.6, width=0.6)
for i, (cv, ne) in enumerate(zip(cv_ord, ne_ord)):
    ax.text(i, ne + n_epochs.max() * 0.02, f"{cv}/{int(ne)}",
            ha="center", fontsize=7.5, fontweight="bold")

tick_labels = [
    f"Sub-{s}\n({'✓' if c else '✗'})"
    for s, c in zip(sub_ord, c_ord)
]
ax.set_xticks(x); ax.set_xticklabels(tick_labels, fontsize=9)

# Group header annotations
mid_ctrl = (n_ctrl - 1) / 2
mid_ad   = n_ctrl + (len(subjects) - n_ctrl - 1) / 2
ax.text(mid_ctrl, n_epochs.max() * 1.12, "— Control subjects —",
        ha="center", fontsize=10, fontweight="bold", color="#27ae60")
ax.text(mid_ad,   n_epochs.max() * 1.12, "— Alzheimer's subjects —",
        ha="center", fontsize=10, fontweight="bold", color="#2980b9")

ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject  (grouped by class)\n"
             "Green band = Control subjects  |  Blue band = Alzheimer's subjects",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.25)
legend_items = [
    mpatches.Patch(facecolor=COL[(0, True)],  label="Correct-label votes — Control, classified correctly"),
    mpatches.Patch(facecolor=COL[(0, False)], label="Correct-label votes — Control, misclassified"),
    mpatches.Patch(facecolor=COL[(1, True)],  label="Correct-label votes — Alzheimer's, classified correctly"),
    mpatches.Patch(facecolor=COL[(1, False)], label="Correct-label votes — Alzheimer's, misclassified"),
    mpatches.Patch(facecolor="#cccccc",        label="Votes for other labels"),
]
ax.legend(handles=legend_items, fontsize=7.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes, x)
save_fig(fig, 4, "(grouped by class)")


# ═══════════════════════════════════════════════════════════════════════════════
#  Variant 5 — Vote fraction bar (ad_ratio as percentage text) + class label
#  Shows the "confidence" of the epoch vote alongside the raw count
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
fig.suptitle(SUPTITLE, fontsize=9, fontweight="bold", y=1.02)
ax = axes[0]
x = np.arange(len(subjects))
bot_cols = [COL[(tl, c)] for tl, c in zip(true_labels, correct)]
ax.bar(x, correct_votes, color=bot_cols, edgecolor="black",
       linewidth=0.7, alpha=0.85, width=0.6)
ax.bar(x, other_votes, bottom=correct_votes, color="#cccccc",
       edgecolor="black", linewidth=0.7, alpha=0.6, width=0.6)

# Annotate each bar with vote fraction percentage AND class label
for i, (cv, ne, ratio, tl, c) in enumerate(zip(correct_votes, n_epochs, ad_ratio, true_labels, correct)):
    # vote fraction text inside bar
    y_text = cv / 2 if cv > ne * 0.15 else cv + ne * 0.03
    ax.text(i, y_text, f"{ratio*100:.0f}%\nvote for\ntrue label",
            ha="center", va="center", fontsize=6.5, color="black", fontweight="bold")
    # class badge above bar
    badge_col = "#27ae60" if tl == 0 else "#2980b9"
    ax.text(i, ne + n_epochs.max() * 0.035,
            f"{CLASS_FULL[tl]}\n{'✓' if c else '✗'}",
            ha="center", fontsize=8, color=badge_col, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels([f"Sub-{s}" for s in subjects], rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Number of epoch votes", fontsize=10)
ax.set_title("Epoch votes per subject\n"
             "% inside bar = fraction of epochs that voted for the subject's true label",
             fontsize=8.5, fontweight="bold")
ax.set_ylim(0, n_epochs.max() * 1.30)
legend_items = [
    mpatches.Patch(facecolor=COL[(0, True)],  label="Correct-label votes — Control, classified correctly"),
    mpatches.Patch(facecolor=COL[(0, False)], label="Correct-label votes — Control, misclassified"),
    mpatches.Patch(facecolor=COL[(1, True)],  label="Correct-label votes — Alzheimer's, classified correctly"),
    mpatches.Patch(facecolor=COL[(1, False)], label="Correct-label votes — Alzheimer's, misclassified"),
    mpatches.Patch(facecolor="#cccccc",        label="Votes for other labels"),
]
ax.legend(handles=legend_items, fontsize=7.5, loc="upper right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
add_panels_2_3(axes, x)
save_fig(fig, 5, "(vote % inside bar + class badge above)")


print(f"\nAll figA.1.x files saved to:\n  {OUTDIR}")
