#!/usr/bin/env python3
"""
Alternatives to Figure 9 (violin of subject_acc − epoch_acc).
All figures use P=6 data only.  Gap = subject-label acc − epoch acc (pp).
Positive gap → epoch UNDER-estimates subject-label performance.
Negative gap → epoch OVER-estimates.

fig9.alt.1  — Stat callout table (heatmap-style)
fig9.alt.2  — Horizontal % bar: "epoch over-estimates in X% of folds"
fig9.alt.3  — Strip / dot plot (each dot = one fold)
fig9.alt.4  — Histogram split by pipeline, coloured by sign of gap
fig9.alt.5  — ECDF (cumulative distribution)
fig9.alt.6  — Dot-and-whisker: median ± IQR, 4 conditions
fig9.alt.7  — Diverging bar: % epoch-over vs subject-over
fig9.alt.8  — Signed area chart: running median of gap across sorted folds
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from pathlib import Path

matplotlib.use("Agg")

BASE   = Path(__file__).parent
MERGED = BASE / "paper_subject_eval_outputs" / "fold_epoch_vs_subject_merged.csv"
OUTDIR = BASE / "paper_subject_eval_outputs" / "fig9_alternatives"
OUTDIR.mkdir(parents=True, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────
raw = pd.read_csv(MERGED)
raw["gap"] = (raw["subject_acc"] - raw["epoch_acc"]) * 100
df  = raw[raw["P"] == 6].copy()

PIPE_LABEL  = {"FTest": "ANOVA (F-test)", "PCA": "PCA"}
STRAT_LABEL = {"Random-50": "Random-50", "Uniform-12": "Uniform-12"}
PIPE_COL    = {"FTest": "#4472c4", "PCA": "#ed7d31"}
STRAT_COL   = {"Random-50": "#4472c4", "Uniform-12": "#ed7d31"}
CONDITIONS  = [("FTest","Random-50"), ("FTest","Uniform-12"),
               ("PCA","Random-50"),   ("PCA","Uniform-12")]

def stats(pipe, strat):
    s = df[(df["pipeline"]==pipe) & (df["strategy"]==strat)]["gap"]
    return dict(
        n       = len(s),
        median  = s.median(),
        iqr     = s.quantile(0.75) - s.quantile(0.25),
        q25     = s.quantile(0.25),
        q75     = s.quantile(0.75),
        pct_ep_over   = (s < 0).mean() * 100,   # epoch > subject
        pct_subj_over = (s > 0).mean() * 100,   # subject > epoch
        pct_equal     = (s == 0).mean() * 100,
        vals    = s.values,
    )

ST = {(p,s): stats(p,s) for p,s in CONDITIONS}

def save(fig, name, suffix=""):
    path = OUTDIR / f"{name}.png"
    plt.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {name}.png  {suffix}")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.1 — Stat callout table
# 4 rows × 4 columns: Median gap | IQR | % epoch over-estimates | n folds
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 3.2))
ax.axis("off")

col_labels = ["Pipeline", "Strategy", "Median gap\n(subject − epoch)", "IQR", "Epoch over-estimates\nsubject-label acc in…", "n folds"]
rows = []
for pipe, strat in CONDITIONS:
    s = ST[(pipe, strat)]
    rows.append([
        PIPE_LABEL[pipe],
        strat,
        f"{s['median']:+.1f} pp",
        f"{s['iqr']:.1f} pp",
        f"{s['pct_ep_over']:.0f}% of folds",
        str(s['n']),
    ])

tbl = ax.table(cellText=rows, colLabels=col_labels,
               cellLoc="center", loc="center")
tbl.auto_set_font_size(False)
tbl.set_fontsize(10.5)
tbl.scale(1.0, 2.0)

# Colour header row
for j in range(len(col_labels)):
    tbl[(0, j)].set_facecolor("#2c3e50")
    tbl[(0, j)].set_text_props(color="white", fontweight="bold")

# Colour pipeline rows
pipe_row_cols = ["#dbeafe", "#dbeafe", "#fde8d8", "#fde8d8"]
for i, rc in enumerate(pipe_row_cols, start=1):
    for j in range(len(col_labels)):
        tbl[(i, j)].set_facecolor(rc)

# Bold the median column (index 2)
for i in range(1, 5):
    tbl[(i, 2)].set_text_props(fontweight="bold")

ax.set_title("Gap = subject-label accuracy − epoch accuracy  (P=6 folds only)\n"
             "Positive = epoch under-estimates  |  Negative = epoch over-estimates",
             fontsize=10.5, fontweight="bold", pad=12)
save(fig, "fig9.alt.1_stat_table", "(numeric callout table)")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.2 — Horizontal % bar: epoch over-estimates vs subject-over
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 3.8))

labels = [f"{PIPE_LABEL[p]}\n{s}" for p,s in CONDITIONS]
pct_ep   = [ST[(p,s)]["pct_ep_over"]   for p,s in CONDITIONS]
pct_subj = [ST[(p,s)]["pct_subj_over"] for p,s in CONDITIONS]
pct_eq   = [ST[(p,s)]["pct_equal"]     for p,s in CONDITIONS]
y = np.arange(len(CONDITIONS))

ax.barh(y, pct_ep,   color="#e74c3c", alpha=0.85, height=0.5,
        label="Epoch accuracy over-estimates subject-label accuracy")
ax.barh(y, pct_subj, left=pct_ep, color="#2ecc71", alpha=0.85, height=0.5,
        label="Subject-label accuracy ≥ epoch accuracy")

for i, (ep, subj) in enumerate(zip(pct_ep, pct_subj)):
    if ep > 5:
        ax.text(ep/2, i, f"{ep:.0f}%", ha="center", va="center",
                fontsize=10, fontweight="bold", color="white")
    if subj > 5:
        ax.text(ep + subj/2, i, f"{subj:.0f}%", ha="center", va="center",
                fontsize=10, fontweight="bold", color="white")

ax.axvline(50, color="black", linewidth=1.2, linestyle="--", alpha=0.5)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10.5)
ax.set_xlim(0, 100)
ax.set_xlabel("% of folds (P=6)", fontsize=10)
ax.set_title("In what fraction of folds does epoch accuracy over-estimate subject-label accuracy?\n"
             "Red = epoch inflates performance  |  Green = epoch equal or conservative",
             fontsize=9.5, fontweight="bold")
ax.legend(fontsize=9, loc="lower right")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
save(fig, "fig9.alt.2_pct_bar", "(% folds epoch over-estimates)")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.3 — Strip plot (each dot = one fold), 4 conditions
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 4.5))
np.random.seed(42)

for i, (pipe, strat) in enumerate(CONDITIONS):
    vals  = ST[(pipe,strat)]["vals"]
    jitter = np.random.uniform(-0.18, 0.18, size=len(vals))
    col = PIPE_COL[pipe]
    ax.scatter(vals, np.full(len(vals), i) + jitter,
               color=col, alpha=0.25, s=18, linewidths=0)
    med = ST[(pipe,strat)]["median"]
    ax.plot([med, med], [i-0.35, i+0.35], color=col, linewidth=2.5)
    ax.text(med + 0.8, i + 0.38, f"median={med:+.1f}pp",
            fontsize=8.5, color=col, fontweight="bold", va="bottom")

ax.axvline(0, color="black", linewidth=1.2, linestyle="--", alpha=0.6)
ax.set_yticks(range(len(CONDITIONS)))
ax.set_yticklabels([f"{PIPE_LABEL[p]}  /  {s}" for p,s in CONDITIONS], fontsize=10)
ax.set_xlabel("Subject-label accuracy − epoch accuracy (pp)", fontsize=10)
ax.set_title("Every fold as a dot  (P=6)\n"
             "Right of 0 = epoch under-estimates  |  Left of 0 = epoch over-estimates  |  Line = median",
             fontsize=9.5, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
save(fig, "fig9.alt.3_strip_plot", "(each dot = one fold)")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.4 — Histogram split by pipeline, coloured by sign of gap
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
BINS = np.arange(-50, 55, 5)

for ax, pipe in zip(axes, ["FTest", "PCA"]):
    vals = df[df["pipeline"] == pipe]["gap"].values
    pos  = vals[vals >= 0]
    neg  = vals[vals < 0]
    ax.hist(neg, bins=BINS, color="#e74c3c", alpha=0.75,
            label=f"Epoch over-estimates  (n={len(neg)}, {len(neg)/len(vals)*100:.0f}%)")
    ax.hist(pos, bins=BINS, color="#2ecc71", alpha=0.75,
            label=f"Epoch under-estimates  (n={len(pos)}, {len(pos)/len(vals)*100:.0f}%)")
    ax.axvline(0, color="black", linewidth=1.3, linestyle="--")
    med = np.median(vals)
    ax.axvline(med, color=PIPE_COL[pipe], linewidth=2.0,
               linestyle="-", label=f"Median = {med:+.1f} pp")
    ax.set_title(PIPE_LABEL[pipe], fontsize=12, fontweight="bold")
    ax.set_xlabel("Subject-label acc − epoch acc (pp)", fontsize=10)
    ax.legend(fontsize=8.5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

axes[0].set_ylabel("Number of folds", fontsize=10)
fig.suptitle("Distribution of gap = (subject-label accuracy − epoch accuracy)  (P=6)\n"
             "Green = epoch conservative (good)  |  Red = epoch inflates performance",
             fontsize=10, fontweight="bold")
save(fig, "fig9.alt.4_histogram", "(histogram by pipeline)")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.5 — ECDF
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)

for ax, pipe in zip(axes, ["FTest", "PCA"]):
    for strat, ls in [("Random-50", "-"), ("Uniform-12", "--")]:
        vals = np.sort(ST[(pipe,strat)]["vals"])
        ecdf = np.arange(1, len(vals)+1) / len(vals)
        ax.plot(vals, ecdf, color=PIPE_COL[pipe], linestyle=ls, linewidth=2.0,
                label=strat)
    ax.axvline(0, color="black", linewidth=1.2, linestyle=":", alpha=0.7)
    ax.axhline(0.5, color="gray", linewidth=0.8, linestyle=":", alpha=0.7)
    ax.set_title(PIPE_LABEL[pipe], fontsize=12, fontweight="bold")
    ax.set_xlabel("Subject-label acc − epoch acc (pp)", fontsize=10)
    ax.legend(fontsize=9)
    ax.set_xlim(-55, 55)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

axes[0].set_ylabel("Cumulative fraction of folds", fontsize=10)
fig.suptitle("ECDF of gap = (subject-label accuracy − epoch accuracy)  (P=6)\n"
             "Where curve crosses x=0: fraction of folds where epoch over-estimates",
             fontsize=10, fontweight="bold")
save(fig, "fig9.alt.5_ecdf", "(cumulative distribution)")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.6 — Dot-and-whisker: median ± IQR (most compact summary)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 4.0))

xs = [0, 1, 3, 4]
labels_dw = [f"{PIPE_LABEL[p]}\n{s}" for p,s in CONDITIONS]
cols_dw   = [PIPE_COL[p] for p,s in CONDITIONS]

for xi, (pipe,strat), col in zip(xs, CONDITIONS, cols_dw):
    s = ST[(pipe,strat)]
    ax.plot([xi, xi], [s["q25"], s["q75"]], color=col, linewidth=3.5, alpha=0.5)
    ax.scatter(xi, s["median"], color=col, s=100, zorder=5)
    ax.text(xi, s["q75"] + 1.2, f"{s['median']:+.1f} pp",
            ha="center", fontsize=9, fontweight="bold", color=col)

ax.axhline(0, color="black", linewidth=1.2, linestyle="--", alpha=0.6)
ax.set_xticks(xs); ax.set_xticklabels(labels_dw, fontsize=9.5)
ax.set_ylabel("Subject-label acc − epoch acc (pp)", fontsize=10)
ax.set_title("Median gap ± IQR per condition  (P=6)\n"
             "Dot = median  |  Bar = IQR  |  Above 0 = epoch under-estimates",
             fontsize=9.5, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
legend_items = [mpatches.Patch(facecolor=PIPE_COL["FTest"], label="ANOVA (F-test)"),
                mpatches.Patch(facecolor=PIPE_COL["PCA"],   label="PCA")]
ax.legend(handles=legend_items, fontsize=9)
save(fig, "fig9.alt.6_dot_whisker", "(median ± IQR dot-and-whisker)")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.7 — Diverging bar: % epoch-over (left, red) vs % subject-over (right, green)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 3.8))

labels_div = [f"{PIPE_LABEL[p]}  /  {s}" for p,s in CONDITIONS]
y = np.arange(len(CONDITIONS))
pct_ep_l   = [-ST[(p,s)]["pct_ep_over"]   for p,s in CONDITIONS]   # go left
pct_subj_r = [ ST[(p,s)]["pct_subj_over"] for p,s in CONDITIONS]   # go right

bars_l = ax.barh(y, pct_ep_l,   color="#e74c3c", alpha=0.85, height=0.5)
bars_r = ax.barh(y, pct_subj_r, color="#2ecc71", alpha=0.85, height=0.5)

for i, (l, r) in enumerate(zip(pct_ep_l, pct_subj_r)):
    ax.text(l - 1.5, i, f"{-l:.0f}%", ha="right",   va="center", fontsize=10, fontweight="bold", color="#c0392b")
    ax.text(r + 1.5, i, f"{r:.0f}%",  ha="left",    va="center", fontsize=10, fontweight="bold", color="#27ae60")

ax.axvline(0, color="black", linewidth=1.5)
ax.set_yticks(y); ax.set_yticklabels(labels_div, fontsize=10.5)
ax.set_xlim(-105, 105)
ax.set_xlabel("← Epoch over-estimates (%)    |    Subject-label acc ≥ epoch acc (%)", fontsize=9.5)
ax.set_title("For each condition: which metric is larger?  (P=6)\n"
             "Red = epoch inflates reported accuracy  |  Green = epoch is conservative or equal",
             fontsize=9.5, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{abs(v):.0f}%"))
save(fig, "fig9.alt.7_diverging_bar", "(diverging %, epoch-over vs subject-over)")


# ═══════════════════════════════════════════════════════════════════════════════
# alt.8 — Sorted gap chart: each fold as a line from 0, sorted by gap magnitude
# Shows how "bad" the worst folds are
# ═══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)

for ax, pipe in zip(axes, ["FTest", "PCA"]):
    for strat, alpha in [("Random-50", 0.7), ("Uniform-12", 0.5)]:
        vals = np.sort(ST[(pipe,strat)]["vals"])
        xi   = np.arange(len(vals))
        pos  = vals >= 0
        ax.fill_between(xi[pos],  0, vals[pos],  color="#2ecc71", alpha=alpha*0.5)
        ax.fill_between(xi[~pos], 0, vals[~pos], color="#e74c3c", alpha=alpha*0.5)
        ax.plot(xi, vals, color=PIPE_COL[pipe], alpha=alpha, linewidth=1.2, label=strat)
    ax.axhline(0, color="black", linewidth=1.2, linestyle="--", alpha=0.7)
    ax.set_title(PIPE_LABEL[pipe], fontsize=12, fontweight="bold")
    ax.set_xlabel("Folds sorted by gap (ascending)", fontsize=10)
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

axes[0].set_ylabel("Subject-label acc − epoch acc (pp)", fontsize=10)
fig.suptitle("Sorted gap per fold  (P=6)\n"
             "Area above 0 (green) = epoch under-estimates  |  Area below 0 (red) = epoch over-estimates",
             fontsize=10, fontweight="bold")
save(fig, "fig9.alt.8_sorted_gap", "(sorted gap per fold, area chart)")


print(f"\nAll fig9 alternatives saved to:\n  {OUTDIR}")
