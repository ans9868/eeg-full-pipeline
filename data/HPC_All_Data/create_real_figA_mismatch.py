#!/usr/bin/env python3
"""
Create 5 real-data versions of Figure A — the conceptual epoch–subject mismatch
illustration, but populated with actual fold data.

Each version follows the same 3-panel layout:
  Left:   per-subject accuracy bars (green ≥50% correct, red otherwise)
  Middle: epoch count per subject (blue = high epoch, orange = low epoch)
  Right:  epoch accuracy vs subject accuracy comparison + Δ annotation

Saved as figA.1_conceptual_mismatch.png … figA.5_conceptual_mismatch.png
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

np.random.seed(42)
merged = pd.read_csv(MERGED)
preds  = pd.read_csv(PREDS)
merged["mismatch"] = (merged["epoch_acc"] - merged["subject_acc"]) * 100


def pick_cases():
    m6 = merged[merged["P"] == 6]

    # Case 1 — largest epoch > subject gap (ANOVA)
    c1 = m6[m6["pipeline"] == "FTest"].nlargest(1, "mismatch").iloc[0]

    # Case 2 — largest epoch > subject gap (PCA, different experiment)
    c2 = m6[(m6["pipeline"] == "PCA") & (m6["experiment"] != c1["experiment"])]\
         .nlargest(1, "mismatch").iloc[0]

    # Case 3 — subject >> epoch (epoch underestimates, rare)
    c3 = m6.nsmallest(1, "mismatch").iloc[0]

    # Case 4 — near-perfect agreement, high overall performance
    c4 = m6[(m6["mismatch"].abs() < 1.5) & (m6["epoch_acc"] > 0.75)].iloc[0]

    # Case 5 — high epoch accuracy, very low subject accuracy (most misleading)
    # Use bottom-10th percentile of subject_acc combined with high epoch_acc
    low_subj_thresh = m6["subject_acc"].quantile(0.10)
    c5_pool = m6[(m6["subject_acc"] <= low_subj_thresh) &
                 (m6["experiment"] != c1["experiment"]) &
                 (m6["experiment"] != c2["experiment"])]
    if c5_pool.empty:
        c5_pool = m6[m6["subject_acc"] <= low_subj_thresh]
    c5 = c5_pool.nlargest(1, "epoch_acc").iloc[0]

    return [c1, c2, c3, c4, c5]


CASE_TITLES = [
    "Case 1 — Largest mismatch (ANOVA pipeline)\n"
    "Epoch accuracy flatters performance; most subjects misclassified",

    "Case 2 — Largest mismatch (PCA pipeline)\n"
    "Same trap in the PCA feature space",

    "Case 3 — Reversed mismatch: subject accuracy > epoch accuracy\n"
    "Epoch accuracy under-estimates; correctly-classified subjects had fewer epochs",

    "Case 4 — Near-perfect agreement (high performance fold)\n"
    "Epoch and subject accuracy agree when epoch counts are balanced",

    "Case 5 — Most misleading fold: high epoch acc, 0% subject accuracy\n"
    "Every subject misclassified despite strong epoch-level performance",
]


def make_real_figA(case_row, case_idx, case_title):
    """Build a 3-panel figure A from a real fold."""
    fold_preds = preds[
        (preds["experiment"] == case_row["experiment"]) &
        (preds["fold_id"]    == case_row["fold_id"])    &
        (preds["task_id"]    == case_row["task_id"])
    ].copy()

    if fold_preds.empty:
        print(f"  figA.{case_idx}: no matching predictions, skipping.")
        return

    # Sort by epoch count descending so high-epoch subjects appear left
    fold_preds = fold_preds.sort_values("n_epochs", ascending=False).reset_index(drop=True)

    subjects     = [f"Sub-{int(s)}" for s in fold_preds["SubjectID"]]
    n_epochs     = fold_preds["n_epochs"].values.astype(float)
    correct      = fold_preds["subject_correct"].values
    ad_ratio     = fold_preds["ad_ratio"].values          # fraction of epochs that voted for true label
    correct_votes = (ad_ratio * n_epochs).round().astype(int)  # raw # correct epoch votes
    other_votes   = (n_epochs - correct_votes).astype(int)

    epoch_acc_pct   = case_row["epoch_acc"]   * 100
    subject_acc_pct = case_row["subject_acc"] * 100
    delta           = epoch_acc_pct - subject_acc_pct
    delta_sign      = "over-estimates" if delta > 0 else "under-estimates"

    # Subject denominator for explicit label: e.g. "33.3% (2/6 subjects)"
    n_subjects      = len(subjects)
    n_correct_subj  = int(correct.sum())
    subj_label      = f"{subject_acc_pct:.1f}% ({n_correct_subj}/{n_subjects} subjects)"

    ep_thresh = np.median(n_epochs)
    ep_colors = ["#4a9ede" if n >= ep_thresh else "#f5a623" for n in n_epochs]

    # Annotation: above-median subjects and their share of total epochs
    above_mask       = n_epochs >= ep_thresh
    n_above          = int(above_mask.sum())
    pct_epochs_above = n_epochs[above_mask].sum() / n_epochs.sum() * 100

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.8))
    fig.suptitle(
        case_title + "\n"
        f"Experiment: {case_row['experiment']}  |  Strategy: {case_row['strategy']}  |  "
        f"Model: {case_row['model']}",
        fontsize=9.5, fontweight="bold", y=1.02,
    )

    # ── Panel 1: stacked bar — correct vs other epoch votes ───────────────────
    # Full bar = total epochs; bottom colored section = correct votes;
    # top gray = other votes. Green bottom = correctly classified, red = not.
    ax = axes[0]
    x = np.arange(len(subjects))
    bot_cols = ["#4caf50" if c else "#e53935" for c in correct]   # vivid green / red
    ax.bar(x, correct_votes, color=bot_cols, edgecolor="black",
           linewidth=0.7, alpha=0.85, width=0.6, label="Votes for true label")
    ax.bar(x, other_votes, bottom=correct_votes, color="#cccccc",
           edgecolor="black", linewidth=0.7, alpha=0.6, width=0.6, label="Votes for other labels")

    # Label each bar with "correct_votes / total" and outcome
    for i, (cv, ne, c) in enumerate(zip(correct_votes, n_epochs, correct)):
        outcome = "✓" if c else "✗"
        ax.text(i, ne + n_epochs.max() * 0.02,
                f"{outcome} {cv}/{int(ne)}", ha="center", fontsize=7.5,
                color="#1b5e20" if c else "#b71c1c", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(subjects, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Number of epoch votes", fontsize=10)
    ax.set_title(
        "Epoch votes per subject\n"
        "Coloured = votes for that subject's true label  |  ✓ = correctly classified  |  ✗ = misclassified",
        fontsize=8.5, fontweight="bold",
    )
    ax.set_ylim(0, n_epochs.max() * 1.18)
    legend_items = [
        mpatches.Patch(facecolor="#4caf50", label="Correct-label votes — subject classified correctly (plurality)"),
        mpatches.Patch(facecolor="#e53935", label="Correct-label votes — subject misclassified (plurality)"),
        mpatches.Patch(facecolor="#cccccc", label="Votes for other subject labels"),
    ]
    ax.legend(handles=legend_items, fontsize=7.5, loc="upper right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    # ── Panel 2: epoch count per subject ──────────────────────────────────────
    ax = axes[1]
    bars2 = ax.bar(x, n_epochs, color=ep_colors, edgecolor="black",
                   linewidth=0.7, alpha=0.85, width=0.6)
    ax.axhline(ep_thresh, color="black", linestyle=":", linewidth=1.2, alpha=0.6,
               label=f"Median: {ep_thresh:.0f} epochs")
    for i, ne in enumerate(n_epochs):
        ax.text(i, ne + n_epochs.max() * 0.015, f"{int(ne)}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(subjects, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Total number of epochs", fontsize=10)
    ax.set_title(
        "Epoch count per subject\n"
        "Subjects with more epochs contribute more weight to epoch accuracy",
        fontsize=8.5, fontweight="bold",
    )
    ax.set_ylim(0, n_epochs.max() * 1.18)
    legend_ep = [
        mpatches.Patch(facecolor="#4a9ede", label=f"Above-median epoch count (≥{ep_thresh:.0f})"),
        mpatches.Patch(facecolor="#f5a623", label=f"Below-median epoch count (<{ep_thresh:.0f})"),
    ]
    ax.legend(handles=legend_ep, fontsize=7.5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    # ── Panel 3: epoch acc vs subject acc comparison ──────────────────────────
    ax = axes[2]
    vals = [epoch_acc_pct, subject_acc_pct]
    cols = ["#4a9ede", "#e07b39"]
    bar3 = ax.bar([0, 1], vals, color=cols, edgecolor="black",
                  linewidth=0.9, alpha=0.88, width=0.55)

    # Shade the gap between the two bars to show the mismatch visually
    hi, lo = max(vals), min(vals)
    hi_x   = 0 if vals[0] > vals[1] else 1
    lo_x   = 1 - hi_x
    ax.fill_between(
        [lo_x - 0.275, lo_x + 0.275], lo, hi,
        color="#ffeb3b", alpha=0.55, zorder=0,
        label=f"Gap = {abs(delta):.1f} pp  (epoch {delta_sign} subject-label acc)",
    )
    ax.axhline(50, color="red", linestyle="--", linewidth=1.4,
               alpha=0.7, label="50% chance level")

    # Value labels on top of bars
    for bar, val in zip(bar3, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1.2,
                f"{val:.1f}%", ha="center", fontsize=13, fontweight="bold")

    ax.set_xticks([0, 1])
    ax.set_xticklabels([
        "Epoch accuracy\n(weighted by epoch count)",
        "Subject-label accuracy\n(1 vote per subject)",
    ], fontsize=9.5)
    ax.set_ylabel("Accuracy (%)", fontsize=10)
    ax.set_title(
        "The mismatch: two ways to aggregate\n"
        "Yellow band = gap between the two metrics",
        fontsize=8.5, fontweight="bold",
    )
    ax.set_ylim(0, 115)
    ax.legend(fontsize=8, loc="upper left")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = OUTDIR / f"figA.{case_idx}_conceptual_mismatch.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close()
    print(f"  Saved: {out.name}  (Δ = {delta:+.1f} pp)")


if __name__ == "__main__":
    cases = pick_cases()
    print(f"Selected {len(cases)} real folds\n")
    for i, (case_row, title) in enumerate(zip(cases, CASE_TITLES), 1):
        make_real_figA(case_row, i, title)
    print(f"\nAll figA.x files saved to:\n  {OUTDIR}")
