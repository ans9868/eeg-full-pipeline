#!/usr/bin/env python3
"""
Extract top ANOVA-selected features (by Cohen's d and F-statistic) for all diseases.

Diseases: AD (Alzheimer's), FTD (Frontotemporal Dementia), MDD EC, MDD EO.
Output:
  - top_anova_features_<disease>.csv   — ranked feature table
  - fig_top_anova_features.png         — bar chart: top features by |Cohen's d| per disease

Feature space: 95 relative-band-power features (19 EEG channels × 5 bands).
Feature mapping: HPC_All_Data/biomarkers/feature_mapping.csv
"""

from pathlib import Path
import glob
import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "sans-serif"]

BASE = Path(__file__).parent
HPC  = BASE / "HPC_All_Data"
FTD  = BASE / "ftd_vs_C"
MDD  = BASE / "mdd_vs_cntrl"
SCZ  = BASE.parent / "scz_vs_cntrl_all_results"

OUTDIR = BASE / "anova_feature_analysis"
OUTDIR.mkdir(exist_ok=True)

N_FEATURES = 95
BANDS      = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
N_BANDS    = len(BANDS)

# Load feature mapping
feat_map = pd.read_csv(HPC / "biomarkers" / "feature_mapping.csv")
# Create short label: channel + band
feat_map["label"] = feat_map["channel_name"] + "_" + feat_map["band_name"]


# ── Helper functions ──────────────────────────────────────────────────────────

def cohen_d(group1, group2):
    """Compute Cohen's d (signed: positive = disease > control)."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return 0.0
    s_pool = np.sqrt(((n1 - 1) * np.var(group1, ddof=1) +
                      (n2 - 1) * np.var(group2, ddof=1)) / (n1 + n2 - 2))
    if s_pool == 0:
        return 0.0
    return (np.mean(group1) - np.mean(group2)) / s_pool


def compute_feature_stats(feat_matrix, labels, disease_label=1, ctrl_label=0):
    """
    Compute per-feature F-stat, p-value, Cohen's d.
    feat_matrix: (n_epochs, 95) array
    labels: (n_epochs,) array, disease=1 ctrl=0
    Returns DataFrame with feature stats.
    """
    rows = []
    dis_mask  = labels == disease_label
    ctrl_mask = labels == ctrl_label
    for fi in range(N_FEATURES):
        dis_vals  = feat_matrix[dis_mask, fi]
        ctrl_vals = feat_matrix[ctrl_mask, fi]
        f_stat, p_val = stats.f_oneway(dis_vals, ctrl_vals)
        d = cohen_d(dis_vals, ctrl_vals)
        rows.append({
            "feature_idx": fi,
            "label": feat_map.loc[feat_map["feature_index"] == fi, "label"].values[0]
                     if fi in feat_map["feature_index"].values else f"feature_{fi}",
            "channel": feat_map.loc[feat_map["feature_index"] == fi, "channel_name"].values[0]
                       if fi in feat_map["feature_index"].values else "",
            "band":    feat_map.loc[feat_map["feature_index"] == fi, "band_name"].values[0]
                       if fi in feat_map["feature_index"].values else "",
            "f_stat":  f_stat,
            "p_value": p_val,
            "cohen_d": d,
            "abs_d":   abs(d),
            "mean_disease":  np.mean(dis_vals),
            "mean_control":  np.mean(ctrl_vals),
            "n_disease":     int(dis_mask.sum()),
            "n_control":     int(ctrl_mask.sum()),
        })
    df = pd.DataFrame(rows).sort_values("abs_d", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df


def load_parquet_features(parquet_dir: Path):
    """Load all parquet files from a processed_subjects directory."""
    files = list(parquet_dir.glob("*.parquet"))
    if not files:
        return None, None
    dfs = [pd.read_parquet(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    # Extract feature values array
    feat_vals = np.array([row["values"] if isinstance(row, dict) else row
                          for row in df["features"]])
    labels = df["label"].values.astype(float)
    return feat_vals, labels


# ═══════════════════════════════════════════════════════════════════════════════
# 1. AD (Alzheimer's)
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("Processing AD (Alzheimer's Disease) …")
ad_df = pd.read_csv(HPC / "biomarkers" / "full_data_with_features.csv")
ad_feat = ad_df[[f"feature_{i}" for i in range(N_FEATURES)]].values
ad_labels = (ad_df["Group"] == "alz").astype(float).values
print(f"  Epochs: {len(ad_feat)}  AD: {int(ad_labels.sum())}  CN: {int((1-ad_labels).sum())}")

ad_stats = compute_feature_stats(ad_feat, ad_labels)
ad_stats.to_csv(OUTDIR / "top_anova_features_AD.csv", index=False)
print(f"  Top 5 features: {ad_stats['label'].head(5).tolist()}")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. FTD (Frontotemporal Dementia)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Processing FTD …")

# Use seed 42 ANOVA W_C processed_subjects (all subjects present)
ftd_parquet_dir = FTD / "intra-subject_seed_runs" / "ANOVA_W_C_ftd_vs_cntrl_seed42" / "processed_subjects"
ftd_feat, ftd_labels = load_parquet_features(ftd_parquet_dir)
if ftd_feat is not None:
    print(f"  Epochs: {len(ftd_feat)}  FTD: {int(ftd_labels.sum())}  CN: {int((1-ftd_labels).sum())}")
    ftd_stats = compute_feature_stats(ftd_feat, ftd_labels)
    ftd_stats.to_csv(OUTDIR / "top_anova_features_FTD.csv", index=False)
    print(f"  Top 5 features: {ftd_stats['label'].head(5).tolist()}")
else:
    print("  ERROR: No parquet files found")
    ftd_stats = None


# ═══════════════════════════════════════════════════════════════════════════════
# 3. MDD Eyes-Closed (EC)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Processing MDD EC (Eyes-Closed) …")

mdd_ec_parquet_dir = MDD / "PCA_W_C_mdd_cs_cntrl_seed42_EC" / "processed_subjects"
mdd_ec_feat, mdd_ec_labels = load_parquet_features(mdd_ec_parquet_dir)
if mdd_ec_feat is not None:
    print(f"  Epochs: {len(mdd_ec_feat)}  MDD: {int(mdd_ec_labels.sum())}  CN: {int((1-mdd_ec_labels).sum())}")
    mdd_ec_stats = compute_feature_stats(mdd_ec_feat, mdd_ec_labels)
    mdd_ec_stats.to_csv(OUTDIR / "top_anova_features_MDD_EC.csv", index=False)
    print(f"  Top 5 features: {mdd_ec_stats['label'].head(5).tolist()}")
else:
    print("  ERROR: No parquet files found")
    mdd_ec_stats = None


# ═══════════════════════════════════════════════════════════════════════════════
# 4. MDD Eyes-Open (EO)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Processing MDD EO (Eyes-Open) …")

mdd_eo_parquet_dir = MDD / "PCA_W_C_mdd_cs_cntrl_seed42_eyesopen_EO" / "processed_subjects"
mdd_eo_feat, mdd_eo_labels = load_parquet_features(mdd_eo_parquet_dir)
if mdd_eo_feat is not None:
    print(f"  Epochs: {len(mdd_eo_feat)}  MDD: {int(mdd_eo_labels.sum())}  CN: {int((1-mdd_eo_labels).sum())}")
    mdd_eo_stats = compute_feature_stats(mdd_eo_feat, mdd_eo_labels)
    mdd_eo_stats.to_csv(OUTDIR / "top_anova_features_MDD_EO.csv", index=False)
    print(f"  Top 5 features: {mdd_eo_stats['label'].head(5).tolist()}")
else:
    print("  ERROR: No parquet files found")
    mdd_eo_stats = None


# ═══════════════════════════════════════════════════════════════════════════════
# 5. SCZ (Schizophrenia)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Processing SCZ (Schizophrenia) …")

scz_parquet_dir = SCZ / "ANOVA_W_C_scz_cntrl_seed42" / "processed_subjects"
scz_feat, scz_labels = load_parquet_features(scz_parquet_dir)
if scz_feat is not None:
    print(f"  Epochs: {len(scz_feat)}  SCZ: {int(scz_labels.sum())}  CN: {int((1-scz_labels).sum())}")
    scz_stats = compute_feature_stats(scz_feat, scz_labels)
    scz_stats.to_csv(OUTDIR / "top_anova_features_SCZ.csv", index=False)
    print(f"  Top 5 features: {scz_stats['label'].head(5).tolist()}")
else:
    print("  ERROR: No parquet files found")
    scz_stats = None


# ═══════════════════════════════════════════════════════════════════════════════
# 7. Combined figure: Top-10 features by |Cohen's d| for each disease
# ═══════════════════════════════════════════════════════════════════════════════

DATASETS = []
if ad_stats is not None:
    DATASETS.append(("AD", ad_stats, "#1f77b4"))
if ftd_stats is not None:
    DATASETS.append(("FTD", ftd_stats, "#ff7f0e"))
if mdd_ec_stats is not None:
    DATASETS.append(("MDD EC", mdd_ec_stats, "#2ca02c"))
if mdd_eo_stats is not None:
    DATASETS.append(("MDD EO", mdd_eo_stats, "#d62728"))
if scz_stats is not None:
    DATASETS.append(("SCZ", scz_stats, "#8c564b"))

N_TOP = 10
n_diseases = len(DATASETS)
fig, axes = plt.subplots(1, n_diseases, figsize=(5 * n_diseases, 5),
                          gridspec_kw={"wspace": 0.45})
if n_diseases == 1:
    axes = [axes]

for ax, (name, df_stats, color) in zip(axes, DATASETS):
    top = df_stats.head(N_TOP)
    bars = ax.barh(range(N_TOP)[::-1], top["abs_d"].values,
                   color=color, alpha=0.75, edgecolor="black", linewidth=0.5)
    ax.set_yticks(range(N_TOP)[::-1])
    ax.set_yticklabels(top["label"].values, fontsize=8)
    ax.set_xlabel("|Cohen's d|", fontsize=9)
    ax.set_title(name, fontsize=11, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(0.2, color="gray", lw=0.8, ls=":", alpha=0.6, label="small (0.2)")
    ax.axvline(0.5, color="gray", lw=0.8, ls="--", alpha=0.6, label="medium (0.5)")
    ax.axvline(0.8, color="gray", lw=0.8, ls="-", alpha=0.4, label="large (0.8)")
    if ax == axes[0]:
        ax.legend(fontsize=7, loc="lower right")
    ax.grid(axis="x", alpha=0.2)

fig.suptitle("Top-10 EEG Features by |Cohen's d| — Disease vs Control\n"
             "(95 relative band-power features; 19 channels × 5 bands)",
             fontsize=11, fontweight="bold", y=1.02)

outfile = OUTDIR / "fig_top_anova_features.png"
fig.savefig(outfile, dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"\nSaved combined figure → {outfile}")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. Cross-disease feature overlap table
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Cross-disease top-10 feature comparison:")
for name, df_stats, _ in DATASETS:
    top10 = df_stats.head(10)["label"].tolist()
    print(f"\n{name}:")
    for i, feat in enumerate(top10, 1):
        d = df_stats.loc[df_stats["label"] == feat, "cohen_d"].values[0]
        p = df_stats.loc[df_stats["label"] == feat, "p_value"].values[0]
        direction = "↑" if d > 0 else "↓"
        print(f"  {i:2d}. {feat:<22s}  |d|={abs(d):.3f}  {direction}  p={p:.2e}")

print(f"\nOutput directory: {OUTDIR}")
