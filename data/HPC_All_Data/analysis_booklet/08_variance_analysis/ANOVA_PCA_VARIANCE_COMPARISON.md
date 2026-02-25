# ANOVA vs PCA Variance Analysis Comparison

## Overview

Comparative analysis of variance in accuracy across 10 experiments for both ANOVA and PCA feature extraction methods, examining both W_F (within-fold) and W_C (within-control) configurations.

---

## Summary Statistics

### Experiment Coverage

| Feature Set | Total Results | Unique Models | Experiments | XGBoost Coverage |
|------------|---------------|---------------|-------------|------------------|
| **ANOVA_W_F** | 139 | 16 | 11 (includes v0) | ✅ All 10 (v1-v10) |
| **ANOVA_W_C** | 120 | 12 | 10 | ✅ All 10 (v1-v10) |
| **PCA_W_F** | 138 | 12 | 10 | ✅ All 10 (v1-v10) |
| **PCA_W_C** | 143 | 16 | 10 (v0-v9) | ⚠️ v10 not yet run |

---

## Top Performers by Feature Extraction Method

### ANOVA Features - Best Models

**ANOVA_W_F:**
1. **XGBoost (depth=6)**: 97.47% accuracy, variance = 0.000003 (n=12)
2. **XGBoost (depth=9)**: 97.37% accuracy, variance = 0.000004 (n=10)
3. **XGBoost (depth=3)**: 97.46% accuracy, variance = 0.000035 (n=12)

**ANOVA_W_C:**
1. **XGBoost (depth=3)**: 97.56% accuracy, variance = 0.000005 (n=10)
2. **XGBoost (depth=9)**: 97.41% accuracy, variance = 0.000006 (n=10)
3. **XGBoost (depth=6)**: 97.50% accuracy, variance = 0.000006 (n=10)

### PCA Features - Best Models

**PCA_W_F:**
1. **MLP [200, 100, 50]**: 98.18% accuracy, variance = 0.000004 (n=10) ✅
2. **MLP [150, 50]**: 97.55% accuracy, variance = 0.000013 (n=10) ✅
3. **MLP [100]**: 96.26% accuracy, variance = 0.000018 (n=10) ✅

**PCA_W_C:**
1. **MLP [200, 100, 50]**: 98.18% accuracy, variance = 0.000005 (n=10) ✅
2. **MLP [150, 50]**: 97.48% accuracy, variance = 0.000009 (n=10) ✅
3. **MLP [100]**: 96.27% accuracy, variance = 0.000014 (n=10) ✅

---

## Key Comparisons

### 1. Best Overall Accuracy

- **PCA features** achieve slightly higher peak accuracy (~98.18%) with MLP architectures
- **ANOVA features** achieve ~97.5% with XGBoost
- **Difference:** ~0.7 percentage points in favor of PCA

### 2. Model Type Performance

#### XGBoost
- **ANOVA:** Excellent performance (~97-98% accuracy, extremely low variance)
- **PCA:** Good performance (~89-90% accuracy, low variance)
- **Insight:** XGBoost performs significantly better with ANOVA features

#### MLP (Neural Network)
- **ANOVA:** Variable performance (89-94% accuracy, higher variance for complex architectures)
- **PCA:** Excellent performance (96-98% accuracy, very low variance)
- **Insight:** MLP performs significantly better with PCA features

#### SVM
- **ANOVA:** Poor performance for rbf/poly (~3-4% accuracy), moderate for linear (~54-55%)
- **PCA:** Good performance for linear (~94% accuracy), poor for rbf/poly (~56-64%)
- **Insight:** SVM (linear) works well with PCA, not with ANOVA

#### KNN
- **ANOVA:** Moderate performance (~52-54% accuracy, low variance)
- **PCA:** Moderate performance (~64-67% accuracy, high variance)
- **Insight:** KNN performs better with PCA but with higher variance

### 3. Variance Patterns

| Model Type | ANOVA Variance | PCA Variance | Winner |
|------------|----------------|--------------|--------|
| **XGBoost** | Extremely low (0.000003-0.000035) | Low (0.000021-0.000183) | ANOVA |
| **MLP [200,100,50]** | High (0.000557-0.000709) | Very low (0.000004-0.000005) | PCA |
| **MLP [150,50]** | Moderate (0.000188-0.000237) | Very low (0.000009-0.000013) | PCA |
| **MLP [100]** | Low (0.000018-0.000163) | Low (0.000014-0.000018) | Tie |
| **SVM (linear)** | Low (0.000027-0.000319) | Low (0.000027) | Tie |
| **KNN** | Low (0.000037-0.000432) | High (0.000489-0.000839) | ANOVA |

### 4. Stability Rankings

**Most Stable Models (Lowest Variance):**

1. **ANOVA + XGBoost (depth=6)**: Variance = 0.000003
2. **PCA + MLP [200,100,50]**: Variance = 0.000004-0.000005
3. **ANOVA + XGBoost (depth=9)**: Variance = 0.000004-0.000006
4. **PCA + MLP [150,50]**: Variance = 0.000009-0.000013
5. **ANOVA + XGBoost (depth=3)**: Variance = 0.000005-0.000035

**Least Stable Models (Highest Variance):**

1. **PCA + KNN (n=7)**: Variance = 0.000839
2. **PCA + KNN (n=15)**: Variance = 0.000680
3. **PCA + KNN (n=1)**: Variance = 0.000614
4. **ANOVA + MLP [200,100,50]**: Variance = 0.000557-0.000709

---

## Feature Extraction Method Recommendations

### Use ANOVA Features When:
- ✅ **XGBoost is the primary model** (best performance: ~97-98% accuracy)
- ✅ **Maximum stability is required** (XGBoost has extremely low variance)
- ✅ **KNN stability is important** (lower variance than with PCA)

### Use PCA Features When:
- ✅ **MLP is the primary model** (best performance: ~96-98% accuracy)
- ✅ **SVM (linear) is being used** (much better performance: ~94% vs ~54-55%)
- ✅ **Maximum accuracy is the goal** (slightly higher peak: ~98.18% vs ~97.56%)

---

## Model-Specific Recommendations

### For Maximum Accuracy:
1. **PCA + MLP [200, 100, 50]**: 98.18% accuracy
2. **ANOVA + XGBoost (depth=3)**: 97.56% accuracy
3. **PCA + MLP [150, 50]**: 97.48-97.55% accuracy

### For Maximum Stability:
1. **ANOVA + XGBoost (depth=6)**: Variance = 0.000003
2. **PCA + MLP [200, 100, 50]**: Variance = 0.000004-0.000005
3. **ANOVA + XGBoost (depth=9)**: Variance = 0.000004-0.000006

### For Balanced Performance:
1. **PCA + MLP [150, 50]**: High accuracy (97.5%) + very low variance (0.000009-0.000013)
2. **ANOVA + XGBoost (any depth)**: High accuracy (97.4-97.6%) + extremely low variance
3. **PCA + MLP [100]**: Good accuracy (96.3%) + low variance (0.000014-0.000018)

---

## W_F vs W_C Comparison

### ANOVA: W_F vs W_C
- **Similar performance patterns** for both configurations
- **XGBoost** performs consistently well in both
- **MLP variance** slightly higher in W_F for complex architectures
- **ANOVA_W_C** has complete n=10 coverage for all models

### PCA: W_F vs W_C
- **Very similar performance** between W_F and W_C
- **MLP** shows consistent high performance in both
- **XGBoost** shows slightly different variance rankings but similar means
- **PCA_W_F** has complete n=10 coverage, **PCA_W_C** missing v10

---

## Conclusions

1. **Feature extraction method choice depends on model type:**
   - ANOVA → Best for XGBoost
   - PCA → Best for MLP and SVM (linear)

2. **XGBoost with ANOVA** provides the most stable high-performance solution (~97-98% accuracy, extremely low variance)

3. **MLP with PCA** provides the highest peak accuracy (~98.18%) with very low variance

4. **With v10 added:** ANOVA_W_C now has complete n=10 coverage for all models across all 10 experiments

5. **SVM (rbf/poly)** should be excluded from ANOVA analysis due to very poor performance

6. **PCA_W_C v10:** Needs to be run to complete the dataset

---

## Files Generated

### ANOVA
- `ANOVA_W_F/variance_boxplot_all_models.png`
- `ANOVA_W_F/variance_summary_table.csv`
- `ANOVA_W_C/variance_boxplot_all_models.png`
- `ANOVA_W_C/variance_summary_table.csv`

### PCA
- `PCA_W_F/variance_boxplot_all_models.png`
- `PCA_W_F/variance_summary_table.csv`
- `PCA_W_C/variance_boxplot_all_models.png`
- `PCA_W_C/variance_summary_table.csv`

---

*Analysis Date: January 13, 2025*  
*Scripts: `analyze_anova_variance.py`, `analyze_pca_variance.py`*  
*Versions analyzed: ANOVA (v1-v10), PCA_W_F (v1-v10), PCA_W_C (v0-v9)*
