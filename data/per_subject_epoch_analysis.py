#!/usr/bin/env python3
"""
Per-subject epoch count and classification success analysis for LPSO P=6 ANOVA.

For each disease (AD, FTD, MDD EC, MDD EO):
  1. Use the best HP for MLP on ANOVA_L_6.
  2. Load all test_predictions.parquet files (one per fold).
  3. Pool all held-out epochs per subject across folds.
  4. Compute per-subject: total test epochs, n_correct, success_rate.
  5. Produce bar chart figure (style: Figure 6 in preprint).

Output:
  anova_feature_analysis/per_subject_epochs_<disease>.csv
  anova_feature_analysis/fig_per_subject_epochs.png
"""

from pathlib import Path
import glob
import json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "sans-serif"]

BASE   = Path(__file__).parent
HPC    = BASE / "HPC_All_Data"
FTD    = BASE / "ftd_vs_C"
MDD    = BASE / "mdd_vs_cntrl"
SCZ    = BASE.parent / "scz_vs_cntrl_all_results"
OUTDIR = BASE / "anova_feature_analysis"
OUTDIR.mkdir(exist_ok=True)


def get_best_hp_mlp(results_dir: Path, model_name: str = "MLP_(Neural_Network)") -> str | None:
    """Find best HP for MLP by median test accuracy across all folds."""
    mlp_dir = results_dir / model_name
    if not mlp_dir.exists():
        return None
    hp_acc = {}
    for fold_dir in mlp_dir.iterdir():
        if not fold_dir.is_dir():
            continue
        for task_dir in fold_dir.iterdir():
            if not task_dir.is_dir():
                continue
            rj = task_dir / "results.json"
            if not rj.exists():
                continue
            try:
                d = json.loads(rj.read_text())
                hp = json.dumps(d.get("hyperparams", {}), sort_keys=True)
                acc = d.get("test_results", {}).get("accuracy",
                      d.get("test_accuracy", float("nan")))
                if hp not in hp_acc:
                    hp_acc[hp] = []
                hp_acc[hp].append(acc)
            except Exception:
                continue
    if not hp_acc:
        return None
    best = max(hp_acc, key=lambda h: np.median(hp_acc[h]))
    print(f"    Best HP: {best}  median={np.median(hp_acc[best]):.3f}  n_folds={len(hp_acc[best])}")
    return best


def load_subject_epochs(results_dir: Path, model_name: str, best_hp: str,
                        deduplicate: bool = False) -> pd.DataFrame:
    """Load all test_predictions.parquet for the given model/HP and pool by subject."""
    mlp_dir = results_dir / model_name
    rows = []
    seen = set()
    for fold_dir in mlp_dir.iterdir():
        if not fold_dir.is_dir():
            continue
        fold_id = fold_dir.name
        for task_dir in fold_dir.iterdir():
            if not task_dir.is_dir():
                continue
            rj_path = task_dir / "results.json"
            pq_path = task_dir / "test_predictions.parquet"
            if not rj_path.exists() or not pq_path.exists():
                continue
            try:
                rj = json.loads(rj_path.read_text())
                hp = json.dumps(rj.get("hyperparams", {}), sort_keys=True)
                if hp != best_hp:
                    continue
                key = (fold_id, hp)
                if deduplicate:
                    if key in seen:
                        continue
                    seen.add(key)
                df_pq = pd.read_parquet(pq_path)
                df_pq["fold_id"] = fold_id
                rows.append(df_pq)
            except Exception as e:
                print(f"    Warning: {task_dir}: {e}")
                continue
    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True)


def compute_per_subject(df: pd.DataFrame, disease_group: str) -> pd.DataFrame:
    """Aggregate per-subject: total epochs, correct, success_rate, disease flag."""
    rows = []
    for sid, grp in df.groupby("SubjectID"):
        n_epochs = len(grp)
        n_correct = int((grp["label"] == grp["prediction"]).sum())
        success_rate = n_correct / n_epochs if n_epochs > 0 else 0.0
        group = grp["Group"].iloc[0] if "Group" in grp.columns else "unknown"
        is_disease = (group.lower() == disease_group.lower())
        rows.append({
            "SubjectID": sid,
            "Group": group,
            "is_disease": is_disease,
            "n_epochs": n_epochs,
            "n_correct": n_correct,
            "success_rate": success_rate,
        })
    return pd.DataFrame(rows).sort_values(["is_disease", "SubjectID"], ascending=[False, True])


# ═══════════════════════════════════════════════════════════════════════════════
DISEASES = [
    {
        "name":       "AD",
        "results_dir": HPC / "grid_50_random_folds" / "ANOVA_L_6_complete",
        "disease_group": "alz",
        "deduplicate": False,
        "color_dis":  "#d62728",
        "color_ctrl": "#1f77b4",
    },
    {
        "name":       "FTD",
        "results_dir": FTD / "lpso_random50" / "ANOVA_L_6_FTD_C_random50" / "ml_results_grid_search",
        "disease_group": "ftd",
        "deduplicate": False,
        "color_dis":  "#ff7f0e",
        "color_ctrl": "#1f77b4",
    },
    {
        "name":       "MDD EC",
        "results_dir": MDD / "ANOVA_L_6_mdd_cntrl_random50_EC" / "ml_results_grid_search",
        "disease_group": "mdd",
        "deduplicate": False,
        "color_dis":  "#2ca02c",
        "color_ctrl": "#1f77b4",
    },
    {
        "name":       "MDD EO",
        "results_dir": MDD / "ANOVA_L_6_mdd_cntrl_random50_eyesopen_EO" / "ml_results_grid_search",
        "disease_group": "mdd",
        "deduplicate": False,
        "color_dis":  "#9467bd",
        "color_ctrl": "#1f77b4",
    },
    {
        "name":       "SCZ",
        "results_dir": SCZ / "ANOVA_L_6_scz_cntrl_random50" / "ml_results_grid_search",
        "disease_group": "scz",
        "deduplicate": False,
        "color_dis":  "#8c564b",
        "color_ctrl": "#1f77b4",
    },
]

all_subject_data = {}

for config in DISEASES:
    name = config["name"]
    print(f"\n{'='*60}")
    print(f"Processing {name} …")
    results_dir = config["results_dir"]
    if not results_dir.exists():
        print(f"  ERROR: {results_dir} not found")
        continue

    print(f"  Finding best MLP HP …")
    best_hp = get_best_hp_mlp(results_dir)
    if best_hp is None:
        print(f"  ERROR: Could not determine best HP")
        continue

    print(f"  Loading test_predictions …")
    df_epochs = load_subject_epochs(results_dir, "MLP_(Neural_Network)", best_hp,
                                    deduplicate=config["deduplicate"])
    if df_epochs.empty:
        print(f"  ERROR: No prediction data found")
        continue

    print(f"  Loaded {len(df_epochs):,} epoch predictions")
    subj_df = compute_per_subject(df_epochs, config["disease_group"])
    subj_df.to_csv(OUTDIR / f"per_subject_epochs_{name.replace(' ', '_')}.csv", index=False)
    all_subject_data[name] = (subj_df, config)

    print(f"  Subjects: {len(subj_df)}")
    print(f"  Epochs/subject: median={subj_df['n_epochs'].median():.0f}  "
          f"range={subj_df['n_epochs'].min()}–{subj_df['n_epochs'].max()}")
    print(f"  Success rate: median={subj_df['success_rate'].median():.3f}  "
          f"disease={subj_df[subj_df['is_disease']]['success_rate'].median():.3f}  "
          f"ctrl={subj_df[~subj_df['is_disease']]['success_rate'].median():.3f}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure: per-subject epoch count × success rate bar chart
# ═══════════════════════════════════════════════════════════════════════════════

n_diseases = len(all_subject_data)
if n_diseases == 0:
    print("No data to plot")
    exit()

fig, axes = plt.subplots(2, n_diseases, figsize=(5 * n_diseases, 8),
                          gridspec_kw={"hspace": 0.45, "wspace": 0.35,
                                       "height_ratios": [1.5, 1]})
if n_diseases == 1:
    axes = axes.reshape(2, 1)

for col_i, (name, (subj_df, config)) in enumerate(all_subject_data.items()):
    ax_bar  = axes[0, col_i]  # epoch count bars
    ax_rate = axes[1, col_i]  # success rate bars

    dis_df  = subj_df[subj_df["is_disease"]]
    ctrl_df = subj_df[~subj_df["is_disease"]]

    # Sort disease then ctrl, by SubjectID
    ordered = pd.concat([dis_df, ctrl_df], ignore_index=True)
    x = np.arange(len(ordered))
    colors = [config["color_dis"] if r else config["color_ctrl"]
              for r in ordered["is_disease"]]

    # --- Top panel: epoch counts ---
    ax_bar.bar(x, ordered["n_epochs"], color=colors, alpha=0.75,
               edgecolor="none", width=0.85)
    n_dis = dis_df["SubjectID"].nunique()
    ax_bar.axvline(n_dis - 0.5, color="black", lw=1.2, ls="--", alpha=0.5)
    ax_bar.set_title(name, fontsize=11, fontweight="bold")
    ax_bar.set_ylabel("Test epochs (all folds)", fontsize=8)
    ax_bar.set_xlabel("Subject index", fontsize=8)
    ax_bar.tick_params(labelsize=7)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    ax_bar.grid(axis="y", alpha=0.2)

    # --- Bottom panel: success rate ---
    bar_colors_correct   = [config["color_dis"] if r else config["color_ctrl"]
                             for r in ordered["is_disease"]]
    bar_colors_incorrect = ["#cccccc"] * len(ordered)
    # Stacked: correct on top of 0, incorrect in lighter shade
    correct   = ordered["success_rate"].values
    incorrect = 1.0 - correct

    ax_rate.bar(x, correct,   color=bar_colors_correct,   alpha=0.75, width=0.85, label="Correct")
    ax_rate.bar(x, incorrect, bottom=correct, color="#dddddd", alpha=0.5, width=0.85, label="Incorrect")
    ax_rate.axhline(0.5, color="gray", lw=0.9, ls=":", alpha=0.7)
    ax_rate.axvline(n_dis - 0.5, color="black", lw=1.2, ls="--", alpha=0.5)
    ax_rate.set_ylim(0, 1.05)
    ax_rate.set_ylabel("Epoch success rate", fontsize=8)
    ax_rate.set_xlabel("Subject index", fontsize=8)
    ax_rate.tick_params(labelsize=7)
    ax_rate.spines["top"].set_visible(False)
    ax_rate.spines["right"].set_visible(False)
    ax_rate.grid(axis="y", alpha=0.2)

    # Shared legend for first column
    if col_i == 0:
        dis_patch  = mpatches.Patch(color=config["color_dis"],  alpha=0.75, label="Disease")
        ctrl_patch = mpatches.Patch(color=config["color_ctrl"], alpha=0.75, label="Control")
        ax_bar.legend(handles=[dis_patch, ctrl_patch], fontsize=7, loc="upper right")

fig.suptitle("Per-Subject Test Epoch Counts and Classification Success Rate\n"
             "(LPSO P=6, ANOVA features, MLP best HP; dashed line = disease|control boundary)",
             fontsize=11, fontweight="bold", y=1.02)

outfile = OUTDIR / "fig_per_subject_epochs.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"\nSaved per-subject figure → {outfile}")
