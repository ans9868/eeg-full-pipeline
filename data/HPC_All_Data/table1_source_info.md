# Source of "Median ± IQR" Recommendation

The recommendation to **"report median ± IQR to summarize cross-subject performance robustly"** comes from the fold instability analysis, specifically:

## Primary Sources:

1. **`fold_instability_tables.md`** (line 3):
   > "This document demonstrates the dramatic variance in performance across individual LPSO folds, showing why **median + IQR over many folds is required for robust evaluation**."

2. **`mlp_anova_fold_details.md`** (line 71):
   > "**Why Median + IQR?** This example clearly shows why reporting median and interquartile range (IQR) over many folds is essential for robust evaluation. A single fold can be highly misleading."

3. **`analyze_fold_instability.py`** (line 332):
   > "Median + IQR over many folds is required for robust evaluation."

## Context:

This recommendation was developed after analyzing the dramatic fold-to-fold variance observed in the LPSO experiments, where single-fold performance can vary by 60+ percentage points (e.g., 39.8% to 98.3% for MLP).

---
*Generated from analysis files in `data/HPC_All_Data/`*
