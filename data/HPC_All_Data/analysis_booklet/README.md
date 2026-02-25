# 📚 EEG Analysis Booklet

**Complete collection of all analysis markdown files from HPC_All_Data**

## 📁 Structure

```
analysis_booklet/
├── 00_BOOKLET_INDEX.md          ⭐ START HERE - Complete index
├── README.md                    (This file)
│
├── 01_threshold_analysis/      (8 files - cleaned)
│   ├── anova_pca_L6_L2_threshold_analysis.md  ⭐ PRIMARY FILE
│   ├── UNIFORM_VS_RANDOM_SUMMARY.md           ⭐ QUICK REFERENCE
│   ├── UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md ⭐ STATISTICAL RIGOR
│   ├── SAME_SUBJECTS_CONTROL_FLOWCHART.md      ⭐ METHODOLOGY
│   └── ... (current threshold analysis files only)
│
├── 02_per_subject_analysis/     (42 files)
│   ├── SUBJECT_SUCCESS_RATE_VARIANCE_SUMMARY.md
│   ├── CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md
│   └── ... (per-subject analysis files)
│
├── 03_clustering/               (2 files)
│   ├── clustering_results_summary.md
│   └── clustering_analysis_summary.md
│
├── 04_performance_tables/       (15 files)
│   ├── performance_tables.md
│   ├── fold_instability_tables.md
│   └── ... (table files)
│
├── 05_other_analyses/           (3 files)
│   ├── comprehensive_analysis_report.md
│   └── ... (other analysis files)
│
├── 07_biomarkers/               (4 files)
│   ├── ANALYSIS_SUMMARY.md      ⭐ PRIMARY FILE
│   ├── top10_biomarkers_table.csv
│   └── ... (key visualizations)
│
├── 08_variance_analysis/       (3 files)
│   ├── ANOVA_PCA_VARIANCE_COMPARISON.md  ⭐ COMPREHENSIVE COMPARISON
│   ├── PCA_VARIANCE_ANALYSIS_SUMMARY.md  ⭐ PCA ANALYSIS
│   └── ANOVA_VARIANCE_ANALYSIS_SUMMARY.md ⭐ ANOVA ANALYSIS
│
└── 06_indexes/                  (3 files)
    ├── THRESHOLD_ANALYSIS_FILES_INDEX.md  ⭐ FILE STATUS GUIDE
    └── ... (index files)
```

## 🎯 Quick Start

1. **Read the Index:** Open [00_BOOKLET_INDEX.md](00_BOOKLET_INDEX.md) for complete navigation
2. **Threshold Analysis:** Start with [01_threshold_analysis/anova_pca_L6_L2_threshold_analysis.md](01_threshold_analysis/anova_pca_L6_L2_threshold_analysis.md)
3. **File Status:** Check [06_indexes/THRESHOLD_ANALYSIS_FILES_INDEX.md](06_indexes/THRESHOLD_ANALYSIS_FILES_INDEX.md) to see which files are current vs replaced

## 📊 Statistics

- **Total Files:** 82 markdown files (cleaned - removed 11 replaced/outdated files, added variance analyses)
- **Categories:** 8 main categories (added Biomarker Analysis and Variance Analysis)
- **Primary Files:** 10 current/recommended files (added ANOVA variance analysis and comparison)
- **Status:** All files are **copies** - originals remain untouched
- **Cleanup:** Removed all replaced/outdated intermediate versions

## ⚠️ Important Notes

- **Files are COPIED, not moved** - originals remain in their original locations
- Some files are **replaced/outdated** - check the index for status
- **Start with the index** to find the best current versions

## 🔗 Key Files

### Threshold Analysis (Current):
- `01_threshold_analysis/anova_pca_L6_L2_threshold_analysis.md` - Main comprehensive report
- `01_threshold_analysis/UNIFORM_VS_RANDOM_SUMMARY.md` - Quick summary
- `01_threshold_analysis/UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md` - Bootstrapped CIs & effect sizes
- `01_threshold_analysis/SAME_SUBJECTS_CONTROL_FLOWCHART.md` - Subject filtering methodology

### Per-Subject Analysis:
- `02_per_subject_analysis/SUBJECT_SUCCESS_RATE_VARIANCE_SUMMARY.md`
- `02_per_subject_analysis/CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md`

### Biomarker Analysis:
- `07_biomarkers/ANALYSIS_SUMMARY.md` - Complete biomarker analysis
- `07_biomarkers/top10_biomarkers_table.csv` - Quick reference table

### Variance Analysis:
- `08_variance_analysis/ANOVA_PCA_VARIANCE_COMPARISON.md` - Comprehensive comparison of ANOVA vs PCA
- `08_variance_analysis/PCA_VARIANCE_ANALYSIS_SUMMARY.md` - PCA variance analysis (complete XGBoost coverage)
- `08_variance_analysis/ANOVA_VARIANCE_ANALYSIS_SUMMARY.md` - ANOVA variance analysis (XGBoost dominance)

### Indexes:
- `00_BOOKLET_INDEX.md` - Complete navigation index
- `06_indexes/THRESHOLD_ANALYSIS_FILES_INDEX.md` - File status guide

---

*Created: December 12, 2025*  
*All files copied from: `/Users/user/projects/eeg-full-pipeline/data/HPC_All_Data/`*


