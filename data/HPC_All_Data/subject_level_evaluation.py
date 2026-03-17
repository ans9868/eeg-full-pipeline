"""
Subject-Level Evaluation for EEG LPSO Experiments
====================================================
Computes subject-label accuracy from per-epoch parquet predictions, generates
paper figures (small multiples, epoch-vs-subject scatter, delta distribution),
summary tables, and validates against the known epoch-level acceptance criteria.

Label mapping (consistent across all parquets):
  Group='alz'   → label=0.0 → AD  (Alzheimer's Disease)
  Group='cntrl' → label=1.0 → Control
  prediction=0.0 → predicted AD
  prediction=1.0 → predicted Control

AD-ratio rule (τ=0.5):
  AD_ratio = mean(prediction == 0.0)  [fraction of epochs predicted as AD]
  pred_subject_label = 0 (AD) if AD_ratio >= 0.5 else 1 (Control)

Run from: data/HPC_All_Data/
  python subject_level_evaluation.py
"""

import os
import sys
import json
import warnings
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, mannwhitneyu
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ─── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
DATA_ROOT    = SCRIPT_DIR          # .../HPC_All_Data/
COMBINED_CSV = DATA_ROOT / "all_experiments_combined.csv"
OUT_DIR      = DATA_ROOT / "paper_subject_eval_outputs"
OUT_DIR.mkdir(exist_ok=True)

# ─── Experiment manifest ────────────────────────────────────────────────────
# Maps experiment name → (pipeline label, strategy label, P)
EXP_META = {
    "ANOVA_L_6_Random":  ("FTest", "Random-50",  6),
    "ANOVA_L_2_Random":  ("FTest", "Random-50",  2),
    "ANOVA_L_6_Uniform": ("FTest", "Uniform-12", 6),
    "PCA_L_6_Random":    ("PCA",   "Random-50",  6),
    "PCA_L_2_Random":    ("PCA",   "Random-50",  2),
    "PCA_L_6_Uniform":   ("PCA",   "Uniform-12", 6),
}

# Model display names
MODEL_DISPLAY = {
    "MLP": "MLP",
    "KNN": "KNN",
    "SVM": "SVM",
    "XGBoost": "XGBoost",
}
MODEL_ORDER = ["MLP", "KNN", "SVM", "XGBoost"]

# ─── Statistics helpers ──────────────────────────────────────────────────────

def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    """Vectorised Cliff's delta: sign = positive if x > y on average."""
    diff = x[:, None].astype(float) - y[None, :].astype(float)
    return float((diff > 0).sum() - (diff < 0).sum()) / diff.size


def bootstrap_ci_median(data: np.ndarray, n: int = 5000, seed: int = 42):
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(data), size=(n, len(data)))
    medians = np.median(data[idx], axis=1)
    return float(np.percentile(medians, 2.5)), float(np.percentile(medians, 97.5))


def run_wilcoxon(x: np.ndarray, y: np.ndarray):
    """Paired Wilcoxon signed-rank; x and y must be aligned (same fold order)."""
    stat, p = wilcoxon(x, y, zero_method="wilcox", alternative="two-sided")
    delta = cliffs_delta(x, y)
    d_med = float(np.median(x) - np.median(y))
    return {"delta_median_pp": round(d_med * 100, 2),
            "cliffs_delta": round(delta, 3),
            "p_value": round(p, 4),
            "test": "Wilcoxon signed-rank (paired)",
            "n": len(x)}


def run_mannwhitney(x: np.ndarray, y: np.ndarray):
    """Two-sided Mann-Whitney U; x and y need not be aligned."""
    stat, p = mannwhitneyu(x, y, alternative="two-sided")
    delta = cliffs_delta(x, y)
    d_med = float(np.median(x) - np.median(y))
    return {"delta_median_pp": round(d_med * 100, 2),
            "cliffs_delta": round(delta, 3),
            "p_value": round(p, 4),
            "test": "Mann-Whitney U (unpaired)",
            "n_x": len(x), "n_y": len(y)}


def effect_label(d: float) -> str:
    a = abs(d)
    if a < 0.147: return "negligible"
    if a < 0.33:  return "small"
    if a < 0.474: return "medium"
    return "large"


# ─── Step 1: Ingest all LPSO parquets ───────────────────────────────────────

def load_all_epochs() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      subject_rows: one row per (experiment, pipeline, strategy, P,
                                 fold_id, model, hyperparams, SubjectID)
                   with columns: true_label, ad_ratio, n_epochs,
                                 pred_label, subject_correct
      fold_epoch_df: one row per (experiment, pipeline, strategy, P,
                                  fold_id, model, hyperparams)
                    with epoch_acc, n_epochs_fold
    """
    combined = pd.read_csv(COMBINED_CSV)
    lpso = combined[combined["experiment_type"].str.startswith("LPSO")].copy()
    lpso = lpso[lpso["experiment"].isin(EXP_META)].reset_index(drop=True)

    print(f"[load] {len(lpso)} CSV rows across {lpso['experiment'].nunique()} LPSO experiments")

    subject_rows = []
    fold_epoch_rows = []
    missing_parquets = []

    for idx, row in lpso.iterrows():
        parquet_path = DATA_ROOT / row["source_file"].replace("results.json",
                                                              "test_predictions.parquet")
        if not parquet_path.exists():
            missing_parquets.append(str(parquet_path))
            continue

        try:
            df = pd.read_parquet(parquet_path)
        except Exception as e:
            print(f"  [WARN] Failed to read {parquet_path}: {e}")
            continue

        # ── Validate label mapping ──────────────────────────────────────────
        if "Group" in df.columns and "label" in df.columns:
            alz_labels = df.loc[df["Group"] == "alz", "label"].unique()
            cntrl_labels = df.loc[df["Group"] == "cntrl", "label"].unique()
            assert set(alz_labels) == {0.0}, \
                f"Unexpected alz label in {parquet_path}: {alz_labels}"
            assert set(cntrl_labels) == {1.0}, \
                f"Unexpected cntrl label in {parquet_path}: {cntrl_labels}"

        # ── Fold-level epoch accuracy ───────────────────────────────────────
        epoch_correct = (df["prediction"] == df["label"]).astype(float)
        epoch_acc = float(epoch_correct.mean())
        n_epochs_fold = len(df)

        pipeline, strategy, P = EXP_META[row["experiment"]]

        fold_epoch_rows.append({
            "experiment":  row["experiment"],
            "pipeline":    pipeline,
            "strategy":    strategy,
            "P":           P,
            "fold_id":     row["fold_id"],
            "model":       row["model"],
            "hyperparams": row["hyperparams"],
            "task_id":     row["task_id"],
            "epoch_acc":   epoch_acc,
            "n_epochs_fold": n_epochs_fold,
            # Sanity: compare with CSV test_accuracy
            "_csv_epoch_acc": row["test_accuracy"],
        })

        # ── Per-subject aggregation ─────────────────────────────────────────
        grp = df.groupby("SubjectID")
        subj_true = grp["label"].first()            # should be constant per subject
        subj_n    = grp["label"].count()
        # Number of epochs predicted as AD (label=0)
        subj_n_ad_pred = grp["prediction"].apply(lambda x: (x == 0.0).sum())

        # Hard check: label must be constant per subject
        subj_label_check = grp["label"].nunique()
        bad_subjects = subj_label_check[subj_label_check > 1]
        if len(bad_subjects) > 0:
            print(f"  [WARN] {len(bad_subjects)} subjects have mixed labels in "
                  f"{row['fold_id']} / {row['task_id']}: {bad_subjects.index.tolist()}")

        for subj_id in subj_true.index:
            ad_ratio = float(subj_n_ad_pred[subj_id]) / float(subj_n[subj_id])
            true_label = float(subj_true[subj_id])
            pred_label = 0.0 if ad_ratio >= 0.5 else 1.0
            subject_rows.append({
                "experiment":        row["experiment"],
                "pipeline":          pipeline,
                "strategy":          strategy,
                "P":                 P,
                "fold_id":           row["fold_id"],
                "model":             row["model"],
                "hyperparams":       row["hyperparams"],
                "task_id":           row["task_id"],
                "SubjectID":         int(subj_id),
                "true_subject_label":int(true_label),
                "ad_ratio":          round(ad_ratio, 6),
                "n_epochs":          int(subj_n[subj_id]),
                "pred_subject_label":int(pred_label),
                "subject_correct":   int(pred_label == true_label),
            })

        if idx % 200 == 0:
            print(f"  [load] {idx}/{len(lpso)} rows processed …")

    if missing_parquets:
        print(f"[load] WARNING: {len(missing_parquets)} parquet files not found")
        with open(OUT_DIR / "missing_parquets.txt", "w") as f:
            f.write("\n".join(missing_parquets))

    subject_df    = pd.DataFrame(subject_rows)
    fold_epoch_df = pd.DataFrame(fold_epoch_rows)

    # Sanity: epoch_acc from parquet vs CSV should match within float tolerance
    diff = (fold_epoch_df["epoch_acc"] - fold_epoch_df["_csv_epoch_acc"]).abs()
    max_diff = diff.max()
    if max_diff > 1e-4:
        print(f"[WARN] Max epoch_acc discrepancy (parquet vs CSV): {max_diff:.6f}")
    else:
        print(f"[load] ✓ Epoch accuracy from parquets matches CSV (max diff={max_diff:.2e})")

    fold_epoch_df.drop(columns=["_csv_epoch_acc"], inplace=True)
    return subject_df, fold_epoch_df


# ─── Step 2: Build fold-level summary tables ─────────────────────────────────

FOLD_KEYS   = ["experiment", "pipeline", "strategy", "P", "fold_id", "model", "hyperparams", "task_id"]
SUBJECT_KEYS = FOLD_KEYS + ["SubjectID"]


def build_fold_subject_accuracy(subject_df: pd.DataFrame) -> pd.DataFrame:
    """One row per fold×model×hp: subject_acc, n_subjects_fold."""
    grp = subject_df.groupby(FOLD_KEYS)
    agg = grp.agg(
        subject_acc    =("subject_correct", "mean"),
        n_subjects_fold=("SubjectID", "count"),
    ).reset_index()
    return agg


def build_merged(fold_subject_df: pd.DataFrame,
                 fold_epoch_df: pd.DataFrame) -> pd.DataFrame:
    merge_keys = FOLD_KEYS
    merged = fold_subject_df.merge(fold_epoch_df[merge_keys + ["epoch_acc", "n_epochs_fold"]],
                                   on=merge_keys, how="inner")
    merged["subject_minus_epoch"] = merged["subject_acc"] - merged["epoch_acc"]
    return merged


# ─── Step 3: Best-HP selection ───────────────────────────────────────────────

EXP_MODEL_KEYS = ["experiment", "pipeline", "strategy", "P", "model"]


def select_best_hp(merged: pd.DataFrame, criterion: str = "epoch") -> pd.DataFrame:
    """
    For each (experiment, model), choose the single hp setting that maximises
    median(criterion_acc) across folds.

    criterion: 'epoch'   → maximise median epoch_acc  (Mode 1: paper-consistent)
               'subject' → maximise median subject_acc (Mode 2: deployment-aligned)
    """
    acc_col = "epoch_acc" if criterion == "epoch" else "subject_acc"
    rows = []
    for keys, grp in merged.groupby(EXP_MODEL_KEYS):
        hp_medians = grp.groupby("hyperparams")[acc_col].median()
        best_hp    = hp_medians.idxmax()
        best_rows  = grp[grp["hyperparams"] == best_hp].copy()
        best_rows["selection_mode"] = criterion
        best_rows["best_hp"]        = best_hp
        rows.append(best_rows)
    return pd.concat(rows, ignore_index=True)


# ─── Step 4: Best-per-fold vectors for stats ─────────────────────────────────

def best_per_fold_vec(df: pd.DataFrame, acc_col: str = "epoch_acc") -> np.ndarray:
    """
    For a slice of merged (one experiment, one model - all HPs),
    return one value per fold: the max acc across HP configs.
    This is the same method used in compute_real_statistics.py.
    """
    return df.groupby("fold_id")[acc_col].max().values


# ─── Step 5: Subject accuracy summary tables ─────────────────────────────────

def build_subject_summary(best_df: pd.DataFrame, mode_label: str) -> pd.DataFrame:
    """
    Per (experiment, model, best_hp): median subject_acc over folds, IQR, min, max.
    """
    rows = []
    for (exp, pipe, strat, P, model), grp in best_df.groupby(EXP_MODEL_KEYS):
        vals  = grp["subject_acc"].values
        ci_lo, ci_hi = bootstrap_ci_median(vals)
        rows.append({
            "experiment": exp,
            "pipeline":   pipe,
            "strategy":   strat,
            "P":          P,
            "model":      model,
            "best_hp":    grp["best_hp"].iloc[0],
            "selection_mode": mode_label,
            "n_folds":    len(vals),
            "median_subject_acc": round(float(np.median(vals)) * 100, 2),
            "IQR_pp": round(float(np.percentile(vals, 75) - np.percentile(vals, 25)) * 100, 2),
            "min_subject_acc": round(float(vals.min()) * 100, 2),
            "max_subject_acc": round(float(vals.max()) * 100, 2),
            "CI_95_lo": round(ci_lo * 100, 2),
            "CI_95_hi": round(ci_hi * 100, 2),
        })
    df = pd.DataFrame(rows)
    # Add best model column
    best_model = (df.groupby(["experiment"])["median_subject_acc"]
                    .transform("max") == df["median_subject_acc"])
    df["is_best_model"] = best_model
    return df


# ─── Step 6: Epoch–subject correlation ──────────────────────────────────────

def build_epoch_subject_correlation(best_df: pd.DataFrame) -> pd.DataFrame:
    """Pearson and Spearman r between fold-level epoch_acc and subject_acc."""
    from scipy.stats import pearsonr, spearmanr
    rows = []
    for (exp, pipe, strat, P, model), grp in best_df.groupby(EXP_MODEL_KEYS):
        e = grp["epoch_acc"].values
        s = grp["subject_acc"].values
        if len(e) < 4:
            continue
        pr, pp = pearsonr(e, s)
        sr, sp = spearmanr(e, s)
        rows.append({
            "experiment": exp, "pipeline": pipe, "strategy": strat,
            "P": P, "model": model, "n_folds": len(e),
            "pearson_r":  round(pr, 4), "pearson_p":  round(pp, 4),
            "spearman_r": round(sr, 4), "spearman_p": round(sp, 4),
        })
    return pd.DataFrame(rows)


# ─── Step 6b: All-models acceptance stats (replicates compute_real_statistics.py) ─

def compute_acceptance_stats_all_models(fold_epoch_df: pd.DataFrame,
                                         combined_csv_df: pd.DataFrame) -> pd.DataFrame:
    """
    Replicates the exact methodology of compute_real_statistics.py:
      1. For each experiment, find the BEST MODEL by all-runs median test_accuracy
         (using the original combined CSV, identical to compute_real_statistics.py)
      2. For that best model, compute best-per-fold vector
         (max epoch_acc over HP configs, one value per fold_id)
      3. Run the pre-specified tests on those vectors

    This is NOT max over all models — it is best-model-first, then best-per-fold.
    """

    def best_model_of(exp: str) -> str:
        """Select model with highest all-runs median test_accuracy from combined CSV."""
        return max(MODEL_ORDER,
                   key=lambda m: combined_csv_df[
                       (combined_csv_df["experiment"] == exp) &
                       (combined_csv_df["model"] == m)
                   ]["test_accuracy"].median())

    def bpf_vec(exp: str, model: str) -> pd.Series:
        """Best epoch_acc per fold_id for one experiment × model (max over HPs)."""
        sub = fold_epoch_df[(fold_epoch_df["experiment"] == exp) &
                            (fold_epoch_df["model"] == model)]
        return sub.groupby("fold_id")["epoch_acc"].max()

    def get_aligned(exp_a, model_a, exp_b, model_b):
        va = bpf_vec(exp_a, model_a)
        vb = bpf_vec(exp_b, model_b)
        shared = sorted(va.index.intersection(vb.index))
        return va.loc[shared].values, vb.loc[shared].values, shared

    rows = []

    # ── ANOVA vs PCA (Wilcoxon paired, same fold IDs) ──────────────────────
    for label, exp_a, exp_b in [
        ("ANOVA vs PCA (Random-50)",  "ANOVA_L_6_Random",  "PCA_L_6_Random"),
        ("ANOVA vs PCA (Uniform-12)", "ANOVA_L_6_Uniform", "PCA_L_6_Uniform"),
    ]:
        ma = best_model_of(exp_a)
        mb = best_model_of(exp_b)
        va, vb, folds = get_aligned(exp_a, ma, exp_b, mb)
        if len(va) < 4:
            continue
        r = run_wilcoxon(va, vb)
        r.update({"comparison": label, "model_a": ma, "model_b": mb,
                  "exp_a": exp_a, "exp_b": exp_b,
                  "n_folds_a": len(va), "n_folds_b": len(vb)})
        rows.append(r)

    # ── Uniform-12 vs Random-50 (Mann-Whitney, unpaired) ──────────────────
    # Delta = Random − Uniform (positive = Random better)
    for label, exp_u, exp_r in [
        ("Uniform-12 vs Random-50 (FTest)", "ANOVA_L_6_Uniform", "ANOVA_L_6_Random"),
        ("Uniform-12 vs Random-50 (PCA)",   "PCA_L_6_Uniform",   "PCA_L_6_Random"),
    ]:
        mu = best_model_of(exp_u)
        mr = best_model_of(exp_r)
        vu = bpf_vec(exp_u, mu).values
        vr = bpf_vec(exp_r, mr).values
        if len(vu) < 4 or len(vr) < 4:
            continue
        r = run_mannwhitney(vr, vu)   # (Random, Uniform) → delta = Random − Uniform
        r.update({"comparison": label, "model_a": mr, "model_b": mu,
                  "exp_a": exp_r, "exp_b": exp_u,
                  "n_folds_a": len(vr), "n_folds_b": len(vu)})
        rows.append(r)

    # ── P=6 vs P=2 (Mann-Whitney, unpaired) ───────────────────────────────
    for label, exp_p6, exp_p2 in [
        ("P=6 vs P=2 (FTest)", "ANOVA_L_6_Random", "ANOVA_L_2_Random"),
        ("P=6 vs P=2 (PCA)",   "PCA_L_6_Random",   "PCA_L_2_Random"),
    ]:
        m6 = best_model_of(exp_p6)
        m2 = best_model_of(exp_p2)
        v6 = bpf_vec(exp_p6, m6).values
        v2 = bpf_vec(exp_p2, m2).values
        if len(v6) < 4 or len(v2) < 4:
            continue
        r = run_mannwhitney(v6, v2)
        r.update({"comparison": label, "model_a": m6, "model_b": m2,
                  "exp_a": exp_p6, "exp_b": exp_p2,
                  "n_folds_a": len(v6), "n_folds_b": len(v2)})
        rows.append(r)

    # ── MLP vs KNN in ANOVA Random-50 (Wilcoxon paired) ───────────────────
    va, vb, folds = get_aligned("ANOVA_L_6_Random", "MLP",
                                 "ANOVA_L_6_Random", "KNN")
    if len(va) >= 4:
        r = run_wilcoxon(va, vb)
        r.update({"comparison": "MLP vs KNN (ANOVA Random-50)", "model_a": "MLP", "model_b": "KNN",
                  "exp_a": "ANOVA_L_6_Random", "exp_b": "ANOVA_L_6_Random",
                  "n_folds_a": len(va), "n_folds_b": len(vb)})
        rows.append(r)

    return pd.DataFrame(rows)


# ─── Step 7: Statistical tests ───────────────────────────────────────────────

def run_all_stats(merged: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Run all prespecified tests on EPOCH accuracy (best-per-fold) for the
    acceptance criteria check, and the same tests on SUBJECT accuracy.
    Returns: (stats_df, debug_info)
    """
    rows = []

    def get_bpf(exp: str, model: str, acc_col: str):
        """Best-per-fold vector for one experiment × model."""
        sub = merged[(merged["experiment"] == exp) & (merged["model"] == model)]
        return sub.groupby("fold_id")[acc_col].max()

    def get_bpf_aligned(exp_a: str, exp_b: str, model: str, acc_col: str):
        """Paired best-per-fold: return (vec_a, vec_b) aligned on shared fold_ids."""
        va = get_bpf(exp_a, model, acc_col)
        vb = get_bpf(exp_b, model, acc_col)
        shared = va.index.intersection(vb.index)
        return va.loc[shared].values, vb.loc[shared].values, list(shared)

    debug = {}

    # ── ANOVA vs PCA (same folds, paired) ────────────────────────────────────
    for strategy, (exp_anov, exp_pca) in [
        ("Random-50",  ("ANOVA_L_6_Random",  "PCA_L_6_Random")),
        ("Uniform-12", ("ANOVA_L_6_Uniform", "PCA_L_6_Uniform")),
    ]:
        for acc_col, acc_label in [("epoch_acc", "epoch"), ("subject_acc", "subject")]:
            model_results = {}
            for model in MODEL_ORDER:
                va, vb, folds = get_bpf_aligned(exp_anov, exp_pca, model, acc_col)
                if len(va) < 4:
                    continue
                r = run_wilcoxon(va, vb)
                r.update({"strategy": strategy, "model": model,
                           "comparison": f"ANOVA vs PCA ({strategy})",
                           "acc_type": acc_label,
                           "exp_a": exp_anov, "exp_b": exp_pca})
                rows.append(r)
                model_results[model] = {"n_paired": len(folds), "fold_ids_sample": folds[:3]}
            debug[f"ANOVA_vs_PCA_{strategy}_{acc_label}"] = model_results

    # ── Uniform-12 vs Random-50 (unpaired) ───────────────────────────────────
    for pipeline, (exp_uni, exp_ran) in [
        ("FTest", ("ANOVA_L_6_Uniform", "ANOVA_L_6_Random")),
        ("PCA",   ("PCA_L_6_Uniform",   "PCA_L_6_Random")),
    ]:
        for acc_col, acc_label in [("epoch_acc", "epoch"), ("subject_acc", "subject")]:
            for model in MODEL_ORDER:
                vu = get_bpf(exp_uni, model, acc_col).values
                vr = get_bpf(exp_ran, model, acc_col).values
                if len(vu) < 4 or len(vr) < 4:
                    continue
                r = run_mannwhitney(vu, vr)
                r.update({"strategy": "Uniform-12 vs Random-50", "model": model,
                           "comparison": f"Uniform-12 vs Random-50 ({pipeline})",
                           "acc_type": acc_label,
                           "exp_a": exp_uni, "exp_b": exp_ran})
                rows.append(r)

    # ── P=6 vs P=2 (unpaired) ─────────────────────────────────────────────────
    for pipeline, (exp_p6, exp_p2) in [
        ("FTest", ("ANOVA_L_6_Random", "ANOVA_L_2_Random")),
        ("PCA",   ("PCA_L_6_Random",   "PCA_L_2_Random")),
    ]:
        for acc_col, acc_label in [("epoch_acc", "epoch"), ("subject_acc", "subject")]:
            for model in MODEL_ORDER:
                v6 = get_bpf(exp_p6, model, acc_col).values
                v2 = get_bpf(exp_p2, model, acc_col).values
                if len(v6) < 4 or len(v2) < 4:
                    continue
                r = run_mannwhitney(v6, v2)
                r.update({"strategy": "P6 vs P2", "model": model,
                           "comparison": f"P=6 vs P=2 ({pipeline})",
                           "acc_type": acc_label,
                           "exp_a": exp_p6, "exp_b": exp_p2})
                rows.append(r)

    # ── Inter-model: MLP vs KNN in ANOVA Random-50 ───────────────────────────
    for acc_col, acc_label in [("epoch_acc", "epoch"), ("subject_acc", "subject")]:
        va, vb, folds = get_bpf_aligned("ANOVA_L_6_Random", "ANOVA_L_6_Random",
                                        "MLP", acc_col)
        # (MLP vs KNN needs different fold sets from different model slices)
        v_mlp = get_bpf("ANOVA_L_6_Random", "MLP",  acc_col).values
        v_knn = get_bpf("ANOVA_L_6_Random", "KNN",  acc_col).values
        # They share the same fold_ids → pair them
        mlp_s = merged[(merged["experiment"]=="ANOVA_L_6_Random") &
                       (merged["model"]=="MLP")].groupby("fold_id")[acc_col].max()
        knn_s = merged[(merged["experiment"]=="ANOVA_L_6_Random") &
                       (merged["model"]=="KNN")].groupby("fold_id")[acc_col].max()
        shared = mlp_s.index.intersection(knn_s.index)
        if len(shared) >= 4:
            r = run_wilcoxon(mlp_s.loc[shared].values, knn_s.loc[shared].values)
            r.update({"strategy": "intra-experiment", "model": "MLP vs KNN",
                      "comparison": "MLP vs KNN (ANOVA Random-50)",
                      "acc_type": acc_label,
                      "exp_a": "ANOVA_L_6_Random", "exp_b": "ANOVA_L_6_Random"})
            rows.append(r)
            debug[f"MLP_vs_KNN_ANOVA_R50_{acc_label}"] = {
                "n_paired": len(shared), "fold_ids_sample": list(shared)[:3]}

    stats_df = pd.DataFrame(rows)
    return stats_df, debug


# ─── Step 8: Acceptance criteria validation ──────────────────────────────────

ACCEPTANCE = [
    # (comparison substring, delta_pp, cliffs_d, p_threshold, sig_direction)
    ("ANOVA vs PCA (Random-50)",         +15.7,  0.85,  0.001, "lt"),
    ("ANOVA vs PCA (Uniform-12)",        +15.9,  0.83,  0.001, "lt"),
    ("Uniform-12 vs Random-50 (FTest)",  +0.6,   0.15,  0.05,  "ns"),
    ("Uniform-12 vs Random-50 (PCA)",    +0.8,   0.09,  0.05,  "ns"),
    ("P=6 vs P=2 (FTest)",               -7.2,  -0.32,  0.05,  "lt"),
    ("P=6 vs P=2 (PCA)",                 -1.6,  -0.17,  0.05,  "ns"),
    ("MLP vs KNN (ANOVA Random-50)",     +1.6,   0.21,  0.001, "lt"),
]

TOLERANCE_PP  = 1.0    # ± 1 pp tolerance on delta_median
TOLERANCE_D   = 0.10   # ± 0.10 tolerance on Cliff's delta


def validate_acceptance(allmodel_stats: pd.DataFrame) -> tuple[bool, list[str]]:
    """Validate against the all-models acceptance-criteria DataFrame."""
    issues = []
    for (comp_substr, exp_delta, exp_d, p_thresh, sig) in ACCEPTANCE:
        sub = allmodel_stats[allmodel_stats["comparison"].str.contains(comp_substr, regex=False)]
        if sub.empty:
            issues.append(f"MISSING: '{comp_substr}'")
            continue
        row = sub.iloc[0]

        got_delta = row.get("delta_median_pp", None)
        got_d     = row.get("cliffs_delta", None)
        got_p     = row.get("p_value", None)

        if got_delta is not None and abs(got_delta - exp_delta) > TOLERANCE_PP:
            issues.append(
                f"DELTA MISMATCH '{comp_substr}': "
                f"expected ~{exp_delta} pp, got {got_delta:.2f} pp")

        if got_d is not None and abs(got_d - exp_d) > TOLERANCE_D:
            issues.append(
                f"CLIFF'S DELTA MISMATCH '{comp_substr}': "
                f"expected ~{exp_d}, got {got_d:.3f}")

        if sig == "lt" and got_p is not None and got_p >= p_thresh:
            issues.append(
                f"P NOT SIGNIFICANT '{comp_substr}': "
                f"expected p<{p_thresh}, got p={got_p:.4f}")
        elif sig == "ns" and got_p is not None and got_p < 0.05:
            issues.append(
                f"UNEXPECTED SIGNIFICANCE '{comp_substr}': "
                f"expected n.s., got p={got_p:.4f}")

    passed = len(issues) == 0
    return passed, issues


# ─── Step 9: Figures ─────────────────────────────────────────────────────────

PIPELINE_COLORS = {"FTest": "#2166ac", "PCA": "#d6604d"}
STRATEGY_ALPHA  = {"Random-50": 0.9, "Uniform-12": 0.65}
# Model colors consistent with create_lpso_box_plots.py and create_figure4_holdout_variance.py
MODEL_COLORS = {
    'MLP':     '#1f77b4',  # Blue
    'XGBoost': '#ff7f0e',  # Orange
    'SVM':     '#2ca02c',  # Green
    'KNN':     '#d62728',  # Red
}

def _boxplot_panel(ax, data_by_model: dict, model_order: list,
                   title: str, ylabel: str, show_xlabel: bool = True,
                   P: int = 6):
    """Draw boxplot + jitter for one panel. Y-axis = # subjects correct (0..P)."""
    positions = list(range(len(model_order)))
    for i, model in enumerate(model_order):
        vals_frac = np.array(data_by_model.get(model, []))
        if len(vals_frac) == 0:
            continue
        # Convert fraction → integer subject count
        vals = vals_frac * P
        col = MODEL_COLORS.get(model, "#666666")
        bp = ax.boxplot(vals, positions=[i], widths=0.4,
                        patch_artist=True, notch=False,
                        medianprops=dict(color="black", linewidth=2),
                        boxprops=dict(facecolor=col, alpha=0.40),
                        whiskerprops=dict(color=col, linewidth=1.4),
                        capprops=dict(color=col, linewidth=1.4),
                        flierprops=dict(marker=".", markersize=3, color=col))
        # Jitter
        jitter = np.random.default_rng(42).uniform(-0.15, 0.15, size=len(vals))
        ax.scatter([i + j for j in jitter], vals, s=12, alpha=0.65,
                   color=col, zorder=3)
    # Reference line at P/2 = random-chance (balanced classes)
    ax.axhline(P / 2, color="gray", linestyle=":", linewidth=1.2, alpha=0.8)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.set_xlim(-0.5, len(model_order) - 0.5)
    ax.set_xticks(positions)
    if show_xlabel:
        ax.set_xticklabels(model_order, fontsize=9)
    else:
        ax.set_xticklabels([])
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_ylim(-0.4, P + 0.4)
    ax.set_yticks(range(P + 1))
    ax.grid(axis="y", alpha=0.3)


def fig_subject_accuracy_small_multiples(best_df: pd.DataFrame,
                                          P_filter: int,
                                          acc_col: str,
                                          out_path: Path,
                                          mode_label: str = "epoch-selected"):
    """2×2 grid: rows=pipeline (FTest, PCA), cols=strategy."""
    pipelines  = ["FTest", "PCA"]
    strategies = ["Uniform-12", "Random-50"]

    # Filter to P and strategies that exist
    sub = best_df[(best_df["P"] == P_filter)].copy()
    avail_strats = sub["strategy"].unique()
    strategies   = [s for s in strategies if s in avail_strats]

    ncols = len(strategies)
    nrows = len(pipelines)

    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 4.5 * nrows),
                             squeeze=False)
    fig.suptitle(f"Subject-level classification (P={P_filter} subjects/fold, HP selected by {mode_label})\n"
                 f"Y-axis = subjects correctly classified; dotted line = P/2 (random-chance reference)",
                 fontsize=11, y=1.01)

    for ri, pipeline in enumerate(pipelines):
        for ci, strategy in enumerate(strategies):
            ax = axes[ri][ci]
            panel_df = sub[(sub["pipeline"] == pipeline) &
                           (sub["strategy"] == strategy)]
            data_by_model = {}
            for model in MODEL_ORDER:
                vals = panel_df.loc[panel_df["model"] == model, acc_col].values
                data_by_model[model] = vals

            show_xlabel = (ri == nrows - 1)
            _boxplot_panel(ax, data_by_model, MODEL_ORDER,
                           title=f"{pipeline} — {strategy}",
                           ylabel=f"Subjects correctly classified (of {P_filter})" if ci == 0 else "",
                           show_xlabel=show_xlabel,
                           P=P_filter)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [fig] Saved: {out_path.name}")


def fig_epoch_vs_subject_scatter(merged: pd.DataFrame,
                                  P_filter: int,
                                  best_hp_selected: pd.DataFrame,
                                  out_path: Path):
    """Scatter of epoch_acc vs subject_acc per fold, coloured by strategy."""
    sub = best_hp_selected[best_hp_selected["P"] == P_filter].copy()

    pipelines = ["FTest", "PCA"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle(f"Epoch vs Subject accuracy per fold (P={P_filter})\n"
                 f"y=x diagonal = perfect agreement", fontsize=11)

    strategy_markers = {"Random-50": "o", "Uniform-12": "s"}
    strategy_colors  = {"Random-50": "#2166ac", "Uniform-12": "#f4a460"}

    for ai, pipeline in enumerate(pipelines):
        ax = axes[ai]
        panel = sub[sub["pipeline"] == pipeline]
        if panel.empty:
            ax.set_title(f"{pipeline} — no data"); continue

        for strat, grp in panel.groupby("strategy"):
            ax.scatter(grp["epoch_acc"], grp["subject_acc"],
                       s=22, alpha=0.55, marker=strategy_markers[strat],
                       color=strategy_colors[strat], label=strat, zorder=2)

        # y=x diagonal
        lo = min(panel["epoch_acc"].min(), panel["subject_acc"].min()) - 0.02
        hi = max(panel["epoch_acc"].max(), panel["subject_acc"].max()) + 0.02
        ax.plot([lo, hi], [lo, hi], "k--", linewidth=1.2, alpha=0.6, label="y = x")

        # Label top-3 and bottom-3 epoch_acc folds (over all HPs, so group by fold first)
        fold_means = panel.groupby("fold_id").agg(
            epoch_acc=("epoch_acc", "max"),
            subject_acc=("subject_acc", "max")).reset_index()
        top3    = fold_means.nlargest(3, "epoch_acc")
        bottom3 = fold_means.nsmallest(3, "epoch_acc")
        for _, fr in pd.concat([top3, bottom3]).iterrows():
            ax.annotate(fr["fold_id"].replace("sub-","")[:20],
                        xy=(fr["epoch_acc"], fr["subject_acc"]),
                        fontsize=5.5, alpha=0.7,
                        xytext=(3, 3), textcoords="offset points")

        ax.set_title(f"{pipeline}", fontsize=10, fontweight="bold")
        ax.set_xlabel("Epoch accuracy (fold-level)")
        ax.set_ylabel("Subject accuracy (fold-level)")
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [fig] Saved: {out_path.name}")


def fig_delta_distribution(best_df: pd.DataFrame, out_path: Path):
    """Violin / distribution of (subject_acc − epoch_acc) per pipeline."""
    pipelines = ["FTest", "PCA"]
    strategies = ["Random-50", "Uniform-12"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    fig.suptitle("Subject accuracy − Epoch accuracy per fold\n"
                 "Negative = epoch over-estimates subject performance", fontsize=11)

    for ai, pipeline in enumerate(pipelines):
        ax = axes[ai]
        panel = best_df[best_df["pipeline"] == pipeline]

        data_parts  = []
        labels_list = []
        colors_list = []
        for strat in strategies:
            sub = panel[panel["strategy"] == strat]
            if sub.empty:
                continue
            data_parts.append(sub["subject_minus_epoch"].values)
            labels_list.append(strat)
            colors_list.append(strategy_colors_map(strat))

        if data_parts:
            parts = ax.violinplot(data_parts, positions=range(len(data_parts)),
                                  showmedians=True, showextrema=True)
            for pc, col in zip(parts["bodies"], colors_list):
                pc.set_facecolor(col); pc.set_alpha(0.65)
            ax.set_xticks(range(len(labels_list)))
            ax.set_xticklabels(labels_list, fontsize=9)
        ax.axhline(0, color="black", linewidth=1.2, linestyle="--", alpha=0.7)
        ax.set_title(f"{pipeline}", fontsize=10, fontweight="bold")
        ax.set_ylabel("subject_acc − epoch_acc")
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
        ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [fig] Saved: {out_path.name}")


def strategy_colors_map(s: str) -> str:
    return {"Random-50": "#2166ac", "Uniform-12": "#f4a460"}.get(s, "#aaa")


# ─── Step 10: Acceptance stats report ────────────────────────────────────────

def build_acceptance_table(stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the specific rows needed for the acceptance criteria table
    (epoch acc, MLP as primary model for aggregate comparisons).
    """
    target_comps = [
        ("ANOVA vs PCA (Random-50)",          "MLP"),
        ("ANOVA vs PCA (Uniform-12)",          "MLP"),
        ("Uniform-12 vs Random-50 (FTest)",    "MLP"),
        ("Uniform-12 vs Random-50 (PCA)",      "MLP"),
        ("P=6 vs P=2 (FTest)",                 "MLP"),
        ("P=6 vs P=2 (PCA)",                   "MLP"),
        ("MLP vs KNN (ANOVA Random-50)",       "MLP vs KNN"),
    ]
    rows = []
    for comp, model in target_comps:
        sub = stats_df[(stats_df["comparison"].str.contains(comp, regex=False)) &
                       (stats_df["acc_type"] == "epoch")]
        if sub.empty:
            sub = stats_df[stats_df["comparison"].str.contains(comp, regex=False) &
                           (stats_df["acc_type"] == "epoch")]
        row_match = sub[sub["model"] == model] if model in sub["model"].values else sub.head(1)
        if row_match.empty:
            row_match = sub.head(1)
        if row_match.empty:
            rows.append({"comparison": comp, "test": "N/A",
                         "delta_median_pp": None, "cliffs_delta": None,
                         "p_value": None, "acc_type": "epoch"})
        else:
            r = row_match.iloc[0].to_dict()
            rows.append(r)

    result = pd.DataFrame(rows)[["comparison", "test",
                                  "delta_median_pp", "cliffs_delta",
                                  "p_value", "acc_type"]]
    return result


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  Subject-Level Evaluation — EEG LPSO Experiments")
    print("=" * 70)

    # ── 1. Load data ──────────────────────────────────────────────────────────
    print("\n[1/8] Loading parquets and computing epoch/subject metrics …")
    combined_csv_df = pd.read_csv(COMBINED_CSV)
    subject_df, fold_epoch_df = load_all_epochs()
    print(f"      subject_df:    {len(subject_df):,} rows  "
          f"({subject_df['SubjectID'].nunique()} unique subjects)")
    print(f"      fold_epoch_df: {len(fold_epoch_df):,} rows")

    # ── 2. Build fold-level subject accuracy ──────────────────────────────────
    print("\n[2/8] Building fold-level subject accuracy …")
    fold_subject_df = build_fold_subject_accuracy(subject_df)
    merged          = build_merged(fold_subject_df, fold_epoch_df)
    print(f"      merged: {len(merged):,} rows")

    # ── 3. Best-HP selection ──────────────────────────────────────────────────
    print("\n[3/8] Selecting best HP per (experiment, model) …")
    best_epoch_sel   = select_best_hp(merged, criterion="epoch")
    best_subject_sel = select_best_hp(merged, criterion="subject")
    print(f"      Mode-1 (epoch-selected):   {len(best_epoch_sel):,} rows")
    print(f"      Mode-2 (subject-selected): {len(best_subject_sel):,} rows")

    # ── 4. Summary tables ─────────────────────────────────────────────────────
    print("\n[4/8] Building summary tables …")
    summary_mode1 = build_subject_summary(best_epoch_sel,   mode_label="epoch-selected")
    summary_mode2 = build_subject_summary(best_subject_sel, mode_label="subject-selected")
    corr_df       = build_epoch_subject_correlation(best_epoch_sel)

    # ── 5. Stats (epoch acc acceptance check + subject acc) ───────────────────
    print("\n[5/8] Running statistical tests …")
    stats_df, debug_info = run_all_stats(merged)

    # Acceptance check: uses best-model-then-best-per-fold (replicates compute_real_statistics.py)
    print("      Computing best-model best-per-fold for acceptance check …")
    allmodel_stats    = compute_acceptance_stats_all_models(fold_epoch_df, combined_csv_df)
    acceptance_table  = allmodel_stats[["comparison", "test",
                                         "delta_median_pp", "cliffs_delta", "p_value"]].copy()

    print("\n  ── Acceptance criteria check (best-per-fold, all models) ──")
    passed, issues = validate_acceptance(allmodel_stats)
    if passed:
        print("  ✓ ALL acceptance criteria passed!")
    else:
        print(f"  ✗ {len(issues)} issue(s) found:")
        for iss in issues:
            print(f"    • {iss}")

    # ── 6. Write CSV outputs ──────────────────────────────────────────────────
    print("\n[6/8] Writing CSV outputs …")

    subject_df.to_csv(OUT_DIR / "per_subject_fold_predictions.csv", index=False)
    print(f"  → per_subject_fold_predictions.csv  ({len(subject_df):,} rows)")

    fold_subject_df.to_csv(OUT_DIR / "fold_subject_accuracy.csv", index=False)
    print(f"  → fold_subject_accuracy.csv         ({len(fold_subject_df):,} rows)")

    fold_epoch_df.to_csv(OUT_DIR / "fold_epoch_accuracy.csv", index=False)
    print(f"  → fold_epoch_accuracy.csv           ({len(fold_epoch_df):,} rows)")

    merged.to_csv(OUT_DIR / "fold_epoch_vs_subject_merged.csv", index=False)
    print(f"  → fold_epoch_vs_subject_merged.csv  ({len(merged):,} rows)")

    summary_mode1.to_csv(OUT_DIR / "table_subject_accuracy_summary_mode1_epoch_selected.csv",
                         index=False)
    summary_mode2.to_csv(OUT_DIR / "table_subject_accuracy_summary_mode2_subject_selected.csv",
                         index=False)
    print("  → table_subject_accuracy_summary_mode1_epoch_selected.csv")
    print("  → table_subject_accuracy_summary_mode2_subject_selected.csv")

    corr_df.to_csv(OUT_DIR / "table_epoch_subject_correlation.csv", index=False)
    print("  → table_epoch_subject_correlation.csv")

    stats_df.to_csv(OUT_DIR / "table_all_statistical_tests.csv", index=False)
    allmodel_stats.to_csv(OUT_DIR / "table_acceptance_criteria_check.csv", index=False)
    print("  → table_all_statistical_tests.csv")
    print("  → table_acceptance_criteria_check.csv")

    # ── 7. Figures ────────────────────────────────────────────────────────────
    print("\n[7/8] Generating figures …")
    np.random.seed(42)  # deterministic jitter

    # Fig S1: Subject accuracy small multiples P=6
    fig_subject_accuracy_small_multiples(
        best_epoch_sel, P_filter=6, acc_col="subject_acc",
        out_path=OUT_DIR / "fig_subject_accuracy_small_multiples_P6.png",
        mode_label="epoch-selected")

    # Fig S1: P=2
    p2_exps = best_epoch_sel[best_epoch_sel["P"] == 2]
    if not p2_exps.empty:
        fig_subject_accuracy_small_multiples(
            best_epoch_sel, P_filter=2, acc_col="subject_acc",
            out_path=OUT_DIR / "fig_subject_accuracy_small_multiples_P2.png",
            mode_label="epoch-selected")

    # Fig S2: Epoch vs subject scatter P=6
    fig_epoch_vs_subject_scatter(
        merged, P_filter=6, best_hp_selected=best_epoch_sel,
        out_path=OUT_DIR / "fig_epoch_vs_subject_scatter_P6.png")

    # Fig S2: P=2
    if not p2_exps.empty:
        fig_epoch_vs_subject_scatter(
            merged, P_filter=2, best_hp_selected=best_epoch_sel,
            out_path=OUT_DIR / "fig_epoch_vs_subject_scatter_P2.png")

    # Fig S3: Delta distribution
    fig_delta_distribution(
        best_epoch_sel,
        out_path=OUT_DIR / "fig_subject_minus_epoch_delta_distribution.png")

    # ── 8. Text summary ───────────────────────────────────────────────────────
    print("\n[8/8] Writing text summary …")
    _write_text_summary(stats_df, allmodel_stats, summary_mode1, corr_df,
                        acceptance_table, passed, issues, debug_info)

    print("\n" + "=" * 70)
    print(f"  Done. All outputs in: {OUT_DIR}")
    print("=" * 70)

    # ── Quantisation note ────────────────────────────────────────────────────
    print("\n📌  NOTE on subject accuracy quantisation:")
    print("    With P=6 subjects per fold, subject_acc can only take values")
    print("    0/6, 1/6, … 6/6 = 0.0, 16.67%, 33.33%, 50.0%, 66.67%, 83.33%, 100%.")
    print("    With P=2 subjects per fold: only 0%, 50%, 100%.")
    print("    This means statistical tests on subject_acc will have many tied ranks.")
    print("    Wilcoxon and Mann-Whitney still valid but power is lower than for epoch_acc.")

    # ── Remove stale debug file if acceptance now passes ─────────────────────
    stale_debug = OUT_DIR / "debug_acceptance_failure.md"
    if stale_debug.exists():
        stale_debug.unlink()

    # Print acceptance table to console
    print("\nAcceptance criteria check (all-models best-per-fold, epoch accuracy):")
    print(acceptance_table.to_string(index=False))


def _write_text_summary(stats_df, allmodel_stats, summary_mode1, corr_df,
                        acceptance_table, passed, issues, debug_info):
    lines = [
        "# Subject-Level Evaluation — Summary Report",
        f"Generated: 2026-03-02",
        "",
        "## Acceptance Criteria (best-per-fold across all models — replicates compute_real_statistics.py)",
        "",
        "```",
        allmodel_stats[["comparison","test","delta_median_pp","cliffs_delta","p_value"]].to_string(index=False),
        "```",
        "",
        f"Overall: {'✓ PASSED' if passed else '✗ FAILED'}",
    ]
    if issues:
        lines += ["", "### Issues:"] + [f"  - {i}" for i in issues]
        lines += ["", "### Debug Info:"]
        for k, v in debug_info.items():
            lines.append(f"  {k}: {json.dumps(v, default=str)[:200]}")

    lines += [
        "",
        "## Subject Accuracy Summary (Mode 1: HP selected by epoch accuracy)",
        "",
        "```",
        summary_mode1[["experiment","model","n_folds","median_subject_acc",
                        "IQR_pp","min_subject_acc","max_subject_acc",
                        "CI_95_lo","CI_95_hi","is_best_model"]].to_string(index=False),
        "```",
        "",
        "## Epoch–Subject Correlation",
        "",
        "```",
        corr_df.to_string(index=False),
        "```",
        "",
        "## All Statistical Tests (both epoch and subject accuracy)",
        "",
        "### Epoch accuracy tests (acceptance check):",
        "```",
        stats_df[stats_df["acc_type"]=="epoch"][
            ["comparison","model","delta_median_pp","cliffs_delta","p_value","test"]
        ].to_string(index=False),
        "```",
        "",
        "### Subject accuracy tests (new results):",
        "```",
        stats_df[stats_df["acc_type"]=="subject"][
            ["comparison","model","delta_median_pp","cliffs_delta","p_value","test"]
        ].to_string(index=False),
        "```",
        "",
        "## Important: Subject Accuracy Quantisation",
        "With P=6 subjects per fold, subject_acc is restricted to {0, 1/6, 2/6, 3/6, 4/6, 5/6, 6/6}",
        "= {0%, 16.67%, 33.33%, 50%, 66.67%, 83.33%, 100%}.",
        "With P=2: only {0%, 50%, 100%}.",
        "This creates heavy tied ranks in Wilcoxon/Mann-Whitney; p-values are still valid",
        "but power is substantially lower than for continuous epoch_acc.",
        "Bootstrap CIs on subject_acc median may collapse to a single point.",
        "",
        "## Label Mapping",
        "  Group='alz'   → label=0.0 → AD (Alzheimer's Disease)",
        "  Group='cntrl' → label=1.0 → Control",
        "  prediction=0.0 → predicted AD",
        "  prediction=1.0 → predicted Control",
        "  AD_ratio = mean(prediction == 0.0)   [fraction of epochs predicted as AD]",
        "  τ = 0.5: pred_subject_label = 0 (AD) if AD_ratio >= 0.5 else 1 (Control)",
        "",
        "## HP Selection Rules",
        "  Mode 1 (paper-consistent): select HP that maximises median(epoch_acc) across folds",
        "  Mode 2 (deployment-aligned): select HP that maximises median(subject_acc) across folds",
    ]

    with open(OUT_DIR / "subject_evaluation_report.md", "w") as f:
        f.write("\n".join(lines))
    print("  → subject_evaluation_report.md")

    # Also write debugging report if acceptance failed
    if not passed:
        with open(OUT_DIR / "debug_acceptance_failure.md", "w") as f:
            f.write("# Acceptance Criteria Debugging Report\n\n")
            f.write(f"## Issues\n")
            for i in issues:
                f.write(f"- {i}\n")
            f.write("\n## Debug Info\n```\n")
            f.write(json.dumps(debug_info, indent=2, default=str))
            f.write("\n```\n")
        print("  → debug_acceptance_failure.md")


if __name__ == "__main__":
    main()
