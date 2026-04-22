#!/usr/bin/env python3
"""
Compile SCZ vs C experimental results into CSVs needed for the three trap figures.

Outputs:
  scz_all_experiments_combined.csv   — LPSO results (used by Trap 2 / Figure 4)
  scz_fold_epoch_vs_subject.csv      — per-fold epoch+subject accuracy (used by Trap 3)

Dataset: SCZ vs Control
  SCZ: 14 subjects (sub-015 to sub-028)
  Control: 14 subjects (sub-001 to sub-014)
  Total: 28 subjects
  Chance (balanced): 0.500
"""

import json
import re
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).parent

MODEL_NORMALIZE = {
    "KNN": "KNN",
    "SVM": "SVM",
    "XGBoost": "XGBoost",
    "MLP_(Neural_Network)": "MLP",
}

EXPERIMENTS = [
    {"name": "ANOVA_L_6_SCZ", "dir": "ANOVA_L_6_scz_cntrl_random50",
     "type": "LPSO_Random_50", "feature": "ANOVA", "P": 6},
    {"name": "ANOVA_L_2_SCZ", "dir": "ANOVA_L_2_scz_cntrl_random50",
     "type": "LPSO_Random_50", "feature": "ANOVA", "P": 2},
    {"name": "PCA_L_6_SCZ",   "dir": "PCA_L_6_scz_cntrl_random50",
     "type": "LPSO_Random_50", "feature": "PCA",   "P": 6},
    {"name": "PCA_L_2_SCZ",   "dir": "PCA_L_2_scz_cntrl_random50",
     "type": "LPSO_Random_50", "feature": "PCA",   "P": 2},
]


# ── Part 1: Compile LPSO combined CSV ────────────────────────────────────────
print("=" * 70)
print("Part 1: Compiling LPSO results → scz_all_experiments_combined.csv")
print("=" * 70)

rows = []
for exp in EXPERIMENTS:
    exp_dir = BASE / exp["dir"]
    ml_dir = exp_dir / "ml_results_grid_search"
    if not ml_dir.exists():
        print(f"  MISSING: {exp_dir}")
        continue
    n_found = 0
    for model_dir in ml_dir.iterdir():
        if not model_dir.is_dir():
            continue
        model_raw = model_dir.name
        model = MODEL_NORMALIZE.get(model_raw, model_raw)
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir():
                continue
            # Skip non-fold directories
            if not fold_dir.name.startswith("sub-"):
                continue
            fold_id = fold_dir.name
            for task_dir in fold_dir.iterdir():
                if not task_dir.is_dir():
                    continue
                rj_path = task_dir / "results.json"
                if not rj_path.exists():
                    continue
                try:
                    rj = json.loads(rj_path.read_text())
                except Exception:
                    continue
                hp = json.dumps(rj.get("hyperparams", {}), sort_keys=True)
                rows.append({
                    "experiment":       exp["name"],
                    "experiment_type":  exp["type"],
                    "feature_set":      exp["feature"],
                    "holdout_size_P":   exp["P"],
                    "model":            model,
                    "fold_id":          fold_id,
                    "task_id":          task_dir.name,
                    "hyperparams":      hp,
                    "test_accuracy":    rj.get("test_results", {}).get("accuracy",
                                         rj.get("test_accuracy", float("nan"))),
                    "train_accuracy":   rj.get("train_results", {}).get("accuracy",
                                         rj.get("train_accuracy", float("nan"))),
                })
                n_found += 1
    print(f"  {exp['name']}: {n_found} results")

combined_df = pd.DataFrame(rows)
out_csv = BASE / "scz_all_experiments_combined.csv"
combined_df.to_csv(out_csv, index=False)
print(f"\nSaved {len(combined_df):,} rows → {out_csv.name}")
print(f"  Experiments: {combined_df['experiment'].unique()}")
print(f"  Folds per experiment:")
for exp_name, grp in combined_df.groupby("experiment"):
    print(f"    {exp_name}: {grp['fold_id'].nunique()} folds, {len(grp)} rows")


# ── Part 2: Build fold epoch+subject accuracy CSV ────────────────────────────
print("\n" + "=" * 70)
print("Part 2: Computing subject accuracy from parquet → scz_fold_epoch_vs_subject.csv")
print("=" * 70)


def subject_accuracy_from_parquet(parquet_path: Path, threshold: float = 0.5):
    """Majority-vote subject accuracy: label=1 (SCZ) if ≥threshold of epochs classified as SCZ."""
    df = pd.read_parquet(parquet_path)
    results = []
    for sid, grp in df.groupby("SubjectID"):
        true_label = grp["label"].iloc[0]
        pred_frac = (grp["prediction"] == 1.0).mean()
        predicted = 1.0 if pred_frac >= threshold else 0.0
        results.append({"subj": sid, "true": true_label, "pred": predicted})
    sub_df = pd.DataFrame(results)
    accuracy = (sub_df["true"] == sub_df["pred"]).mean()
    return accuracy, len(sub_df)


PIPELINE_MAP = {
    "ANOVA_L_6_SCZ": ("FTest", "Random-50", 6),
    "ANOVA_L_2_SCZ": ("FTest", "Random-50", 2),
    "PCA_L_6_SCZ":   ("PCA",   "Random-50", 6),
    "PCA_L_2_SCZ":   ("PCA",   "Random-50", 2),
}

fold_rows = []
for exp in EXPERIMENTS:
    pipeline, strategy, P = PIPELINE_MAP[exp["name"]]
    exp_dir = BASE / exp["dir"]
    ml_dir = exp_dir / "ml_results_grid_search"
    if not ml_dir.exists():
        continue

    n_processed = 0
    for model_dir in ml_dir.iterdir():
        if not model_dir.is_dir():
            continue
        model_raw = model_dir.name
        model = MODEL_NORMALIZE.get(model_raw, model_raw)

        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir():
                continue
            if not fold_dir.name.startswith("sub-"):
                continue
            fold_id = fold_dir.name

            for task_dir in fold_dir.iterdir():
                if not task_dir.is_dir():
                    continue
                pq_path = task_dir / "test_predictions.parquet"
                rj_path = task_dir / "results.json"
                if not pq_path.exists() or not rj_path.exists():
                    continue
                try:
                    rj = json.loads(rj_path.read_text())
                    epoch_acc = rj.get("test_results", {}).get("accuracy",
                                rj.get("test_accuracy", float("nan")))
                    df_pq = pd.read_parquet(pq_path)
                    n_epochs = len(df_pq)
                    subj_acc, n_subjects = subject_accuracy_from_parquet(pq_path)
                    hp = json.dumps(rj.get("hyperparams", {}), sort_keys=True)
                    fold_rows.append({
                        "experiment":      exp["name"],
                        "pipeline":        pipeline,
                        "strategy":        strategy,
                        "P":               P,
                        "fold_id":         fold_id,
                        "model":           model,
                        "hyperparams":     hp,
                        "task_id":         task_dir.name,
                        "subject_acc":     subj_acc,
                        "n_subjects_fold": n_subjects,
                        "epoch_acc":       epoch_acc,
                        "n_epochs_fold":   n_epochs,
                        "subject_minus_epoch": subj_acc - epoch_acc,
                    })
                    n_processed += 1
                except Exception as e:
                    print(f"  Error {task_dir}: {e}")
                    continue

    print(f"  {exp['name']}: {n_processed} fold×HP rows")

fold_df = pd.DataFrame(fold_rows)
fold_out = BASE / "scz_fold_epoch_vs_subject.csv"
fold_df.to_csv(fold_out, index=False)
print(f"\nSaved {len(fold_df):,} rows → {fold_out.name}")
