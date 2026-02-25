# Intra-Subject (W_F/W_C) vs LPSO: Accuracy and Variance Comparison

## Overview

This document compares the performance characteristics between **intra-subject** evaluation strategies (W_F and W_C) and **Leave-P-Subjects-Out (LPSO)** cross-validation, highlighting fundamental differences in problem difficulty and variance patterns.

---

## Problem Statement Comparison

### Intra-Subject (W_F and W_C): Similar Problem Difficulty

**Within-Subject Fingerprinting (W_F):**
- **Task:** Identify which subject an EEG recording belongs to
- **Training/Test Split:** 80/20 split **within each subject**
- **Key Characteristic:** Same subjects appear in both training and test sets
- **Difficulty Level:** **Moderate** - Models learn subject-specific patterns

**Within-Subject Classification (W_C):**
- **Task:** Classify group membership (e.g., alz vs cntrl) using within-subject splits
- **Training/Test Split:** 80/20 split **within each subject**
- **Key Characteristic:** Same subjects appear in both training and test sets
- **Difficulty Level:** **Moderate** - Models learn subject-specific patterns that correlate with group membership

**Why W_F and W_C are Similar:**
- ✅ **Same data split strategy:** Both use 80/20 within-subject splits
- ✅ **Same subjects in train/test:** Both allow models to learn subject-specific patterns
- ✅ **Similar difficulty:** Both tasks benefit from subject-specific signal learning
- ✅ **Similar variance patterns:** Both show very low variance across random seeds

### LPSO: Fundamentally Different Problem

**Leave-P-Subjects-Out (LPSO):**
- **Task:** Classify group membership using **cross-subject** evaluation
- **Training/Test Split:** Different subjects in training vs testing
- **Key Characteristic:** Models must generalize to **completely unseen subjects**
- **Difficulty Level:** **Much Higher** - Requires true cross-subject generalization

**Why LPSO is Different:**
- ❌ **Different subjects:** Training and test sets contain completely different subjects
- ❌ **No subject-specific learning:** Models cannot rely on subject-specific patterns
- ❌ **True generalization required:** Must learn features that generalize across subjects
- ❌ **Higher difficulty:** Much harder problem requiring robust feature extraction

---

## Accuracy Comparison

### Summary Statistics

| Evaluation Strategy | Best Accuracy | Mean Accuracy | Standard Deviation | Problem Type |
|---------------------|---------------|---------------|-------------------|--------------|
| **Intra-Subject (W_F)** | 98.18% | ~97-98% | 0.0018-0.0059 | Subject identification |
| **Intra-Subject (W_C)** | 97.56% | ~97-98% | 0.0022-0.0059 | Group classification |
| **LPSO (P=6)** | 89.74% | 53-70% | 6.04-8.92% | Cross-subject classification |

### Key Observations

1. **Intra-Subject Performance:**
   - **W_F and W_C show similar high accuracy** (~97-98%)
   - Both benefit from subject-specific pattern learning
   - Small differences reflect task-specific nuances, not fundamental difficulty differences

2. **LPSO Performance:**
   - **Significantly lower accuracy** (53-70% median, 89.74% best)
   - **Large performance drop** from intra-subject (~24 points for PCA, ~5 points for ANOVA)
   - Reflects the true difficulty of cross-subject generalization

3. **Accuracy Gap:**
   - **PCA:** 98.17% (intra) → 74.08% (LPSO) = **-24.1 points**
   - **ANOVA:** 94.94% (intra) → 89.74% (LPSO) = **-5.2 points**
   - ANOVA shows better preservation of generalizable signal

---

## Variance Comparison

### Intra-Subject Variance (Across 10 Random Seeds)

**ANOVA Features:**
- **XGBoost:** Variance = 0.000003-0.000035 (extremely low)
- **MLP [100]:** Variance = 0.000018-0.000163 (very low)
- **MLP [150,50]:** Variance = 0.000188-0.000237 (low)
- **MLP [200,100,50]:** Variance = 0.000557-0.000709 (moderate)
- **KNN:** Variance = 0.000037-0.000432 (low to moderate)
- **SVM (linear):** Variance = 0.000027-0.000319 (low)

**PCA Features:**
- **MLP [200,100,50]:** Variance = 0.000004-0.000005 (extremely low)
- **MLP [150,50]:** Variance = 0.000009-0.000013 (very low)
- **MLP [100]:** Variance = 0.000014-0.000018 (very low)
- **XGBoost:** Variance = 0.000021-0.000183 (low)
- **SVM (linear):** Variance = 0.000027 (very low)
- **KNN:** Variance = 0.000489-0.000839 (moderate to high)

### LPSO Variance (Across 50 Folds)

**PCA Features:**
- **Mean Accuracy:** 54.57% ± 6.04% (SD)
- **Best Model:** KNN at 53.2% median
- **Variance:** ~36.5 (SD² = 6.04²)

**ANOVA Features:**
- **Mean Accuracy:** 69.72% ± 8.92% (SD)
- **Best Model:** MLP at 69.5% median
- **Variance:** ~79.6 (SD² = 8.92²)

### Variance Comparison Table

| Metric | Intra-Subject (W_F/W_C) | LPSO (P=6) | Ratio |
|--------|------------------------|------------|-------|
| **Best Model Variance** | 0.000003-0.000005 | ~36-72 | **~10,000x higher** |
| **Standard Deviation** | 0.0018-0.0059 | 6.04-8.50% | **~1,000-5,000x higher** |
| **Coefficient of Variation** | ~0.002-0.006 | ~0.11-0.12 | **~20-60x higher** |

---

## Why Variance Differs So Dramatically

### 1. Problem Difficulty

**Intra-Subject (W_F/W_C):**
- Models learn **subject-specific patterns** that are consistent across random seeds
- Same subjects in train/test → patterns are reproducible
- **Low variance** because the problem is relatively easy and consistent

**LPSO:**
- Models must learn **generalizable features** that work across different subjects
- Different subjects in each fold → high variability in difficulty
- **High variance** because different subject combinations have different difficulty levels

### 2. Data Leakage vs True Generalization

**Intra-Subject:**
- Some degree of **subject-specific leakage** (same subjects in train/test)
- Models can memorize subject characteristics
- Results are **optimistic** but **consistent**

**LPSO:**
- **No data leakage** - completely different subjects
- Models must truly generalize
- Results are **realistic** but **variable**

### 3. Fold-to-Fold Variability

**Intra-Subject:**
- Random seed only affects **epoch assignment** within subjects
- Subject characteristics remain constant
- **Low variability** across seeds

**LPSO:**
- Each fold has **different subject combinations**
- Some subject combinations are easier/harder to classify
- **High variability** across folds

---

## Model Performance Patterns

### Intra-Subject: Model Rankings

**Best Performers:**
1. **PCA + MLP [200,100,50]:** 98.18% accuracy, variance = 0.000004-0.000005
2. **ANOVA + XGBoost (depth=6):** 97.47% accuracy, variance = 0.000003
3. **PCA + MLP [150,50]:** 97.48-97.55% accuracy, variance = 0.000009-0.000013

**Key Pattern:** MLP excels with PCA, XGBoost excels with ANOVA

### LPSO: Model Rankings

**Best Performers:**
1. **ANOVA + MLP:** 69.5% median accuracy
2. **ANOVA + KNN:** 68.9% median accuracy
3. **ANOVA + XGBoost:** 67.4% median accuracy
4. **PCA + KNN:** 53.2% median accuracy

**Key Pattern:** ANOVA features preserve generalizable signal much better than PCA

---

## Key Insights

### 1. W_F and W_C are Fundamentally Similar

- ✅ **Same split strategy:** Both use within-subject 80/20 splits
- ✅ **Same difficulty level:** Both allow subject-specific learning
- ✅ **Similar accuracy:** ~97-98% for both
- ✅ **Similar variance:** Very low variance (0.000003-0.000709)
- ✅ **Same problem type:** Subject-specific pattern recognition

**Conclusion:** W_F and W_C represent the **same level of difficulty** with slightly different task objectives. The similarity in results confirms they are evaluating similar problem complexity.

### 2. LPSO is a Fundamentally Different Problem

- ❌ **Different split strategy:** Cross-subject evaluation
- ❌ **Much higher difficulty:** Requires true generalization
- ❌ **Much lower accuracy:** 53-70% vs 97-98%
- ❌ **Much higher variance:** 6-8.5% SD vs 0.0018-0.0059 SD
- ❌ **Different problem type:** Cross-subject generalization

**Conclusion:** LPSO evaluates a **completely different problem** - true cross-subject generalization. The dramatic difference in accuracy and variance reflects the fundamental increase in problem difficulty.

### 3. Variance as a Difficulty Indicator

**Low Variance (Intra-Subject):**
- Indicates **consistent problem difficulty**
- Same subjects → consistent patterns
- Models can reliably learn subject-specific features

**High Variance (LPSO):**
- Indicates **variable problem difficulty**
- Different subject combinations → variable difficulty
- Some folds easier (similar subjects), some harder (dissimilar subjects)

### 4. Feature Extraction Method Matters More in LPSO

**Intra-Subject:**
- Both PCA and ANOVA achieve high accuracy (~97-98%)
- Small differences in variance
- Both methods work well with subject-specific learning

**LPSO:**
- **ANOVA preserves generalizable signal** much better (70% vs 54%)
- **PCA loses generalizable signal** in cross-subject setting
- ANOVA variance (8.9% SD) vs PCA variance (6.04% SD) - but ANOVA has higher mean

---

## Implications for Research

### When to Use Intra-Subject (W_F/W_C)

✅ **Use for:**
- Subject identification tasks
- Within-subject pattern analysis
- Optimistic performance estimates
- When subject-specific patterns are the goal

❌ **Don't use for:**
- Generalization claims
- Clinical deployment evaluation
- Cross-subject performance assessment

### When to Use LPSO

✅ **Use for:**
- True generalization evaluation
- Clinical deployment assessment
- Cross-subject performance claims
- Realistic performance estimates

❌ **Don't use for:**
- Subject-specific pattern analysis
- Optimistic performance estimates
- When same subjects will be in production

---

## Summary Table

| Aspect | Intra-Subject (W_F/W_C) | LPSO (P=6) |
|--------|-------------------------|------------|
| **Problem Type** | Subject-specific learning | Cross-subject generalization |
| **Difficulty** | Moderate | High |
| **Best Accuracy** | 97-98% | 70-89% |
| **Mean Accuracy** | 97-98% | 53-70% |
| **Variance** | 0.000003-0.000709 | ~36-72 |
| **SD** | 0.0018-0.0059 | 6.04-8.92% |
| **CV Ratio** | ~0.002-0.006 | ~0.11-0.12 |
| **Data Leakage** | Some (same subjects) | None |
| **Generalization** | Subject-specific | True cross-subject |
| **W_F vs W_C** | Similar (same difficulty) | N/A |

---

## Conclusions

1. **W_F and W_C are similar problems:** Both use within-subject splits and show similar accuracy/variance patterns, confirming they evaluate similar difficulty levels.

2. **LPSO is a different problem:** Cross-subject evaluation represents a fundamentally harder problem, reflected in lower accuracy and much higher variance.

3. **Variance reflects difficulty:** Low variance in intra-subject indicates consistent problem difficulty. High variance in LPSO indicates variable difficulty across different subject combinations.

4. **Feature extraction matters more in LPSO:** ANOVA preserves generalizable signal much better than PCA in cross-subject settings.

5. **Choose evaluation strategy based on goal:** Use intra-subject for subject-specific analysis, use LPSO for true generalization assessment.

---

*Analysis Date: January 13, 2025*  
*Data Sources: Intra-subject variance analysis (v1-v10), LPSO performance tables (P=6, 50 folds)*

