# Booklet vs Paper Comparison: Missing Graphs and Analyses

## Figures Mentioned in Paper Draft

### ✅ **Figure 1: Within-Subject 80/20 Fingerprinting (PCA vs F-test)**
**Status:** ✅ **HAVE**  
**Location:** `data/intra-subject/IntraSubject_Box_Plots/`
- `PCA_Fingerprinting_Random_10.png`
- `ANOVA_Fingerprinting_Random_10.png`
- `Fingerprinting_Combined.png` (PCA + ANOVA side-by-side)

**Note:** We have box plots showing variance across 10 random seeds, which matches the paper's requirement.

---

### ✅ **Figure 2: Within-Subject 80/20 Condition Prediction (PCA vs F-test)**
**Status:** ✅ **HAVE**  
**Location:** `data/intra-subject/IntraSubject_Box_Plots/`
- `PCA_Classification_Random_10.png`
- `ANOVA_Classification_Random_10.png`
- `Classification_Combined.png` (PCA + ANOVA side-by-side)

**Note:** We have box plots showing variance across 10 random seeds, which matches the paper's requirement.

---

### ✅ **Figure 3: Small-Multiples Boxplots (PCA vs F-test; Systematic-12 vs Random-50)**
**Status:** ✅ **HAVE**  
**Location:** `data/HPC_All_Data/LPSO_Box_Plots/`
- `LPSO_Systematic_vs_Random_Combined.png` (2x2 grid)
- Individual plots: `PCA_Systematic_12.png`, `PCA_Random_50.png`, `ANOVA_Systematic_12.png`, `ANOVA_Random_50.png`

**Note:** Perfect match - shows PCA/ANOVA × Systematic-12/Random-50 comparison.

---

### ❌ **Figure 4: Histogram/Density of Fold Accuracies (Random-50, P=6)**
**Status:** ❌ **MISSING**  
**Paper Description:** "histogram or density of fold accuracies (Random-50, P=6) showing heavy tails and lucky-fold region"

**What We Have:**
- Box plots showing fold distributions ✅
- Fold instability tables ✅
- **Missing:** Histogram/density plot showing the distribution shape and "lucky fold" region

**Action Needed:** Create histogram/density plot of all fold accuracies for Random-50 P=6, highlighting the lucky-fold region (e.g., >90% accuracy).

---

### ❌ **Figure 5: Running Median Accuracy vs Number of Resamples**
**Status:** ❌ **MISSING**  
**Paper Description:** "running median accuracy vs number of resamples k (k = 1,2,3,5,10,20,50) with running IQR or bootstrap CI band"

**What We Have:**
- Convergence analysis markdown documents ✅
- Mathematical convergence analysis ✅
- **Missing:** Visual plot showing running median ± IQR as k increases from 1 to 50

**Action Needed:** Create line plot showing:
- X-axis: Number of resamples (k = 1, 2, 3, 5, 10, 20, 50)
- Y-axis: Running median accuracy
- Error bands: Running IQR or bootstrap CI
- Separate lines for PCA and ANOVA

---

### ✅ **Figure 6: Posterior Alpha Biomarkers**
**Status:** ✅ **HAVE**  
**Location:** `data/HPC_All_Data/analysis_booklet/07_biomarkers/`
- `key_plot1_posterior_alpha_boxplots.png` (box plots with group means and CI whiskers)

**Note:** Matches paper requirement for posterior alpha biomarkers.

---

## Tables Mentioned in Paper Draft

### ✅ **Table 1: LPSO P=6 Medians ± IQR and Min/Max per Model**
**Status:** ✅ **HAVE**  
**Location:** Multiple tables in `04_performance_tables/`
- `table_c_lpso_leaderboard.md` - Leaderboard by transform
- `table_b_cross_subject_summary.md` - Cross-subject summary
- Various `table*_fold_variance_*.md` files

**Note:** We have comprehensive tables showing medians, IQR, min/max for all models.

---

### ✅ **Table 2: Variance vs P (Random-50)**
**Status:** ✅ **HAVE**  
**Location:** 
- `04_performance_tables/table_d_holdout_sensitivity.md` - Hold-out size sensitivity
- `LPSO_Box_Plots/Figure4_Variance_vs_HoldOut_Size.png` - Visual comparison

**Note:** We have both the table and the figure comparing P=6 vs P=2.

---

### ✅ **Table 3: Top 5-8 Biomarkers**
**Status:** ✅ **HAVE**  
**Location:** `07_biomarkers/top10_biomarkers_table.csv`
- Contains AD/control means, percent delta, Cohen's d, 95% CI, p-values

**Note:** We have top 10 biomarkers (paper asks for 5-8, so we have more).

---

## Summary: Missing Items

### Missing Graphs (2):

1. **Figure 4: Histogram/Density Plot of Fold Accuracies**
   - **Purpose:** Show distribution of fold accuracies, highlight "lucky fold" region
   - **Data Available:** ✅ (all fold accuracies from Random-50 P=6)
   - **Action:** Create histogram/density plot

2. **Figure 5: Running Median Convergence Plot**
   - **Purpose:** Show how median stabilizes as more resamples are included
   - **Data Available:** ✅ (can compute running medians from fold data)
   - **Action:** Create line plot with running median ± IQR bands

### Missing Statistical Analyses:

1. **Bootstrapped Confidence Intervals for Running Median**
   - Paper mentions "bootstrap CI band" for Figure 5
   - We have convergence analysis but may need bootstrap CIs

2. **Cliff's Delta Effect Sizes**
   - Paper mentions Cliff's δ in abstract and throughout
   - We have `UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md` ✅
   - Need to verify all comparisons have Cliff's δ

---

## Additional Items in Booklet (Beyond Paper)

The booklet includes **additional analyses** not in the paper:

1. ✅ **Intra-Subject Convergence Analysis** - Mathematical convergence analysis with 3 techniques
2. ✅ **LPSO Convergence Analysis** - 12-fold vs 50-fold convergence comparison
3. ✅ **LPSO vs Intra-Subject Convergence Comparison** - Direct comparison
4. ✅ **Per-Subject Variance Analysis** - Detailed per-subject success rate variance
5. ✅ **Variance Elbow Analysis** - How variance changes with number of folds
6. ✅ **Deep Variance Analysis** - Comprehensive variance analysis reports
7. ✅ **Clustering Analysis** - Subject clustering results
8. ✅ **Comprehensive Threshold Analysis** - Detailed threshold methodology

---

## Recommendations

### High Priority (Paper Requirements):

1. **Create Figure 4:** Histogram/density plot of fold accuracies
   - Show distribution of all fold accuracies (Random-50, P=6)
   - Highlight "lucky fold" region (e.g., >90% accuracy)
   - Show heavy tails visually

2. **Create Figure 5:** Running median convergence plot
   - X-axis: k = 1, 2, 3, 5, 10, 20, 50 resamples
   - Y-axis: Running median accuracy
   - Error bands: Running IQR or bootstrap CI
   - Separate lines for PCA and ANOVA

### Medium Priority (Enhancement):

3. **Add Bootstrap CIs** to convergence plots if not already present
4. **Verify Cliff's δ** is calculated for all key comparisons
5. **Add fold-by-fold accuracy plots** if not already present

---

*Comparison Date: January 20, 2025*  
*Paper Draft: lucky_fold_trap_draft.pdf*  
*Booklet: EEG_Analysis_Booklet.pdf*
