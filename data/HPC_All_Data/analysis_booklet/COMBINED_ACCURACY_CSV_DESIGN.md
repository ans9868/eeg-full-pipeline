# Building One Combined Accuracy CSV (HPC_All_Data)

**Goal:** One CSV that compiles all model run data (fold-level accuracy) across experiments, with checks for data integrity and expected run counts.

**Last updated:** After data audit (Feb 2026).

---

## 0. Review Notes (Data Audit Findings)

### What the original design got right

- The data source pattern (walk `results.json` files) is correct; every `results.json` contains `test_results.accuracy` and `hyperparams`.
- The 4 models (KNN, SVM, XGBoost, MLP) are present in every experiment.
- Every fold dir contains exactly **3 task subdirs** (3 HP configs per model per fold), uniformly across all experiments.
- The schema proposal (experiment, model, fold_id, task_id, test_accuracy, hyperparams) is sound.

### What was wrong or incomplete — corrections

1. **CRITICAL: Duplicate / overlap directories in `grid_50_random_folds/`.**

   There are **7** directories under `grid_50_random_folds/`, not just 4:

   | Directory | What it actually is |
   |-----------|---------------------|
   | `ANOVA_L_6_complete` | ANOVA P=6, **50 folds, all 3 HP per fold per model** (complete). 150 results.json per model. |
   | `Anova_L_6_Incomplete_ml_results` | ANOVA P=6, **same 50 fold names** as `ANOVA_L_6_complete`, but **missing some HP tasks**. MLP only has 45 folds with results (88 results.json), others have 115–127. |
   | `ANOVA_L_2_complete` | ANOVA P=2, 50 folds, complete. 150 results.json per model. |
   | `Anova_L_2_incomplete_ml_results` | ANOVA P=2, same 50 fold names, missing some HP tasks (94–132 results.json per model). |
   | `PCA_L_6_ml_results` | PCA P=6, 50 folds, complete. 150 results.json per model. |
   | `PCA_L_2_ml_results` | PCA P=2, 50 folds, complete. 150 results.json per model. |
   | `ml_results_grid_search` | **MERGED directory** containing both ANOVA P=6 (50 folds) AND ANOVA P=2 (50 folds) = 100 folds total, 300 results.json per model. This is a superset. **Must be excluded** from the combined CSV to avoid double-counting. |

   **Relationship between "complete" and "incomplete":**
   - `ANOVA_L_6_complete` and `Anova_L_6_Incomplete_ml_results` share the **exact same 50 fold names**.
   - "Incomplete" was the original partial run; "complete" is the finished version with all HP tasks filled in.
   - **Use `*_complete` for the combined CSV.** The scripts (Table D, Figure 4) reference the "incomplete" dirs because they were written before the complete runs existed — but this means those scripts use slightly fewer data points for ANOVA. For the combined CSV, use "complete" for maximum integrity.

   **Decision:** For the combined CSV, use these **4 canonical experiments** from `grid_50_random_folds/`:

   | Canonical name | Directory | Status |
   |----------------|-----------|--------|
   | ANOVA_L_6_Random | `ANOVA_L_6_complete` | Complete (150/model) |
   | ANOVA_L_2_Random | `ANOVA_L_2_complete` | Complete (150/model) |
   | PCA_L_6_Random | `PCA_L_6_ml_results` | Complete (150/model) |
   | PCA_L_2_Random | `PCA_L_2_ml_results` | Complete (150/model) |

   **Exclude:** `Anova_L_6_Incomplete_ml_results`, `Anova_L_2_incomplete_ml_results` (subsets of complete), and `ml_results_grid_search` (merged duplicate).

2. **Within-subject experiments have 1 split × 3 HP, not "folds".**

   `ANOVA_W_C`, `ANOVA_W_F`, `PCA_W_C-3`, `PCA_W_F-3` each have a single `within_subject_split/` directory (not fold dirs named `sub-X_sub-Y`). Inside: 3 task dirs per model (3 HP configs). So 3 results.json per model, not 12 or 50.

3. **`model_comparison.csv` `total_tasks` field is unreliable.**

   For `PCA_L_2_ml_results`, `model_comparison.csv` reports `total_tasks=50` per model, but actual count is 150 (50 folds × 3 HP). The `num_folds=50` field is correct. Use `num_folds` for validation, not `total_tasks`.

4. **`results.json` schema** (verified from actual files):

   ```json
   {
     "task_id": "KNN_0_1641",
     "model_name": "KNN",
     "fold_id": "0",
     "hyperparams": { "n_neighbors": 7, "weights": "uniform", "metric": "euclidean" },
     "test_results": { "accuracy": 0.488, "f1": 0.324, "precision": 0.647, "recall": 0.488 },
     "train_results": { "accuracy": 0.917, "f1": 0.917, "precision": 0.917, "recall": 0.917 }
   }
   ```

   Note: `fold_id` inside the JSON is always `"0"` — the real fold identity comes from the **parent directory name** (e.g. `sub-10_sub-17_sub-30_sub-41_sub-44_sub-60`). For within-subject, the parent is `within_subject_split`.

---

## 1. Canonical Experiment Manifest

### 1.1 `grid_50_random_folds/` — LPSO Random 50-fold

| # | Canonical Name | Directory | Feature | P | Folds | Models | HP/fold/model | results.json/model | Use |
|---|---------------|-----------|---------|---|-------|--------|---------------|--------------------|----|
| 1 | ANOVA_L_6_Random | `ANOVA_L_6_complete` | ANOVA | 6 | 50 | 4 | 3 | **150** | YES |
| 2 | ANOVA_L_2_Random | `ANOVA_L_2_complete` | ANOVA | 2 | 50 | 4 | 3 | **150** | YES |
| 3 | PCA_L_6_Random | `PCA_L_6_ml_results` | PCA | 6 | 50 | 4 | 3 | **150** | YES |
| 4 | PCA_L_2_Random | `PCA_L_2_ml_results` | PCA | 2 | 50 | 4 | 3 | **150** | YES |

**Excluded (duplicates/subsets):**

| Directory | Reason |
|-----------|--------|
| `Anova_L_6_Incomplete_ml_results` | Subset of `ANOVA_L_6_complete` (same folds, missing tasks). Used by legacy scripts (Table D, Figure 4). |
| `Anova_L_2_incomplete_ml_results` | Subset of `ANOVA_L_2_complete` (same folds, missing tasks). |
| `ml_results_grid_search` | Merged ANOVA L_6 + L_2 (100 folds, 300 results.json/model). Duplicate data. |

### 1.2 `grid_12_folds/` — LPSO Systematic 12-fold

| # | Canonical Name | Directory | Feature | P | Folds | Models | HP/fold/model | results.json/model | Use |
|---|---------------|-----------|---------|---|-------|--------|---------------|--------------------|----|
| 5 | ANOVA_L_6_Uniform | `ANOVA_L_6_C_Resource_Boosted` | ANOVA | 6 | 12 | 4 | 3 | **36** | YES |
| 6 | PCA_L_6_Uniform | `PCA_L_6_C-3` | PCA | 6 | 12 | 4 | 3 | **36** | YES |

### 1.3 `grid_12_folds/` — Within-Subject (single split, 3 HP configs)

| # | Canonical Name | Directory | Feature | Task | Splits | Models | HP/split/model | results.json/model | Use |
|---|---------------|-----------|---------|------|--------|--------|----------------|--------------------|----|
| 7 | ANOVA_W_C | `ANOVA_W_C` | ANOVA | Classification | 1 | 4 | 3 | **3** | YES |
| 8 | ANOVA_W_F | `ANOVA_W_F` | ANOVA | Fingerprinting | 1 | 4 | 3 | **3** | YES |
| 9 | PCA_W_C | `PCA_W_C-3` | PCA | Classification | 1 | 4 | 3 | **3** | YES |
| 10 | PCA_W_F | `PCA_W_F-3` | PCA | Fingerprinting | 1 | 4 | 3 | **3** | YES |

**Grand total: 10 canonical experiments.**

---

## 2. Expected Run Counts (Integrity Check Table)

### 2.1 Per-experiment × per-model expected `results.json` counts

This is the **ground truth** measured from the filesystem (Feb 2026 audit):

| Experiment | KNN | SVM | XGBoost | MLP | Total | Status |
|-----------|-----|-----|---------|-----|-------|--------|
| **ANOVA_L_6_complete** | 150 | 150 | 150 | 150 | 600 | COMPLETE |
| **ANOVA_L_2_complete** | 150 | 150 | 150 | 150 | 600 | COMPLETE |
| **PCA_L_6_ml_results** | 150 | 150 | 150 | 150 | 600 | COMPLETE |
| **PCA_L_2_ml_results** | 150 | 150 | 150 | 150 | 600 | COMPLETE |
| **ANOVA_L_6_C_Resource_Boosted** | 36 | 36 | 36 | 36 | 144 | COMPLETE |
| **PCA_L_6_C-3** | 36 | 36 | 36 | 36 | 144 | COMPLETE |
| **ANOVA_W_C** | 3 | 3 | 3 | 3 | 12 | COMPLETE |
| **ANOVA_W_F** | 3 | 3 | 3 | 3 | 12 | COMPLETE |
| **PCA_W_C-3** | 3 | 3 | 3 | 3 | 12 | COMPLETE |
| **PCA_W_F-3** | 3 | 3 | 3 | 3 | 12 | COMPLETE |
| **GRAND TOTAL** | | | | | **2,736** | |

### 2.2 Per-experiment fold-dir counts (folds, not tasks)

| Experiment | Expected folds | Actual fold dirs (per model) | Match? |
|-----------|---------------|------------------------------|--------|
| ANOVA_L_6_complete | 50 | 50 | YES |
| ANOVA_L_2_complete | 50 | 50 | YES |
| PCA_L_6_ml_results | 50 | 50 | YES |
| PCA_L_2_ml_results | 50 | 50 | YES |
| ANOVA_L_6_C_Resource_Boosted | 12 | 12 | YES |
| PCA_L_6_C-3 | 12 | 12 | YES |
| ANOVA_W_C | 1 (within_subject_split) | 1 | YES |
| ANOVA_W_F | 1 (within_subject_split) | 1 | YES |
| PCA_W_C-3 | 1 (within_subject_split) | 1 | YES |
| PCA_W_F-3 | 1 (within_subject_split) | 1 | YES |

### 2.3 Integrity for excluded/incomplete directories (for reference)

| Excluded Directory | KNN | SVM | XGBoost | MLP | Notes |
|-------------------|-----|-----|---------|-----|-------|
| Anova_L_6_Incomplete | 127 | 126 | 115 | 88 | MLP only 45/50 folds have data |
| Anova_L_2_incomplete | 132 | 124 | 114 | 94 | All 50 folds present but many missing 1-2 HP tasks |
| ml_results_grid_search | 300 | 300 | 300 | 300 | Merged L_6+L_2 (100 folds). DO NOT USE. |

### 2.4 Validation checks the build script must run

1. **Count check:** For each `(experiment, model)`, count `results.json` files and compare to Section 2.1 table. Flag any mismatch.
2. **Fold-dir check:** For each `(experiment, model)`, count unique fold directories. Must match Section 2.2.
3. **HP-per-fold check:** For each fold dir, verify exactly 3 task subdirs (3 HP configs). Flag any fold with != 3.
4. **No duplicates:** Ensure no `results.json` path appears twice in the output CSV.
5. **Cross-check with `model_comparison.csv`:** Where present, verify `num_folds` matches the fold-dir count. (Do NOT use `total_tasks` — it is unreliable in some experiments.)
6. **Grand total:** Combined CSV should have exactly **2,736 rows** (one per `results.json`).

---

## 3. What the combined CSV should contain (recommended schema)

Columns:

| Column | Description | Example |
|--------|-------------|---------|
| `experiment` | Canonical name | `ANOVA_L_6_Random` |
| `experiment_dir` | Relative path from `HPC_All_Data/` | `grid_50_random_folds/ANOVA_L_6_complete` |
| `experiment_type` | `LPSO_Random_50`, `LPSO_Systematic_12`, or `Within_Subject` | `LPSO_Random_50` |
| `feature_set` | `ANOVA` or `PCA` | `ANOVA` |
| `holdout_size_P` | 6, 2, or `N/A` (within-subject) | `6` |
| `model` | Normalized model name | `KNN` |
| `fold_id` | Fold dir name (e.g. `sub-10_sub-17_...`) or `within_subject_split` | `sub-10_sub-17_sub-30_sub-41_sub-44_sub-60` |
| `task_id` | Task dir name | `task_KNN_0_1641` |
| `hyperparams` | JSON string of hyperparams | `{"n_neighbors": 7, ...}` |
| `test_accuracy` | Float | `0.488` |
| `train_accuracy` | Float | `0.917` |
| `test_f1` | Float | `0.324` |
| `test_precision` | Float | `0.647` |
| `test_recall` | Float | `0.488` |
| `source_file` | Relative path to `results.json` | `grid_50_random_folds/ANOVA_L_6_complete/KNN/sub-.../task_.../results.json` |

---

## 4. Steps to build it

1. **Define manifest** — Use the 10-row table from Section 1 as the experiment manifest. Hard-code the canonical names and paths.
2. **For each experiment:**
   - Resolve `ml_results_path`: for `grid_12_folds/*`, use `{dir}/ml_results_grid_search/`; for `grid_50_random_folds/*`, use `{dir}/` directly (models are at root level).
   - For each model subdir (KNN, SVM, XGBoost, MLP_(Neural_Network)):
     - For each fold subdir (named `sub-*` for LPSO, or `within_subject_split` for within-subject):
       - For each task subdir (`task_*`):
         - Read `results.json`, extract fields, emit one CSV row.
3. **Run integrity checks** (Section 2.4) and print a report.
4. **Output:**
   - `data/HPC_All_Data/all_experiments_combined.csv` — the combined CSV.
   - `data/HPC_All_Data/all_experiments_integrity_report.md` — fold counts, task counts, any warnings.

---

## 5. References (booklet + graph scripts)

- **Booklet:** `data/HPC_All_Data/analysis_booklet/`
  - `02_per_subject_analysis/SUMMARY_ALL_EXPERIMENTS.md` — 6 LPSO experiments, fold strategies.
  - `02_per_subject_analysis/INDEX.md` — per-subject CSVs and experiment list.
  - `04_performance_tables/table_d_holdout_sensitivity.md` — P=6 vs P=2 (uses `Anova_L_6_Incomplete` / `Anova_L_2_incomplete` — legacy paths).
  - `06_indexes/markdown_files_index.md` — index of analyses.
- **Scripts that read run data (and which dirs they use):**
  - `create_table_d_holdout_sensitivity.py` — uses `Anova_L_6_Incomplete`, `ANOVA_L_2_complete`, `PCA_L_6`, `PCA_L_2`. Reads `rglob("results.json")`.
  - `create_figure4_holdout_variance.py` — uses same dirs + `detailed_results.json` fallback.
  - `create_lpso_box_plots.py` — uses `grid_12_folds/` (Systematic-12) and `grid_50_random_folds/ANOVA_L_6_complete` (Random-50).
  - `create_table_b_cross_subject_summary.py`, `create_table_c_lpso_leaderboard.py` — P=6 only (PCA + ANOVA).
  - `compare_within_vs_lpso_p6.py` — within-subject dirs + LPSO P=6.

**Note:** Some legacy scripts point to the "incomplete" ANOVA dirs. For the combined CSV, always use the "complete" versions. Consider updating those scripts later to use the complete dirs for consistency.
