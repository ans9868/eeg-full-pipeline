# 🎯 Comprehensive All-Experiments Threshold Analysis

## Analysis Overview

**Key Features**:
- **ALL experiments** in HPC_All_Data automatically discovered and analyzed
- **ALL subjects** across ALL experiments analyzed (no sampling)
- Each experiment treated **independently**
- Per model×hyperparameter×experiment threshold optimization
- **Fair comparison**: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)

## 📊 Experiments Analyzed

- **grid_12_folds_ANOVA_L_6_C_Resource_Boosted**: 12 model×HP combinations, 65 common subjects
- **grid_12_folds_ANOVA_W_C**: 12 model×HP combinations, 65 common subjects
- **grid_12_folds_ANOVA_W_F**: 12 model×HP combinations, 65 common subjects
- **grid_12_folds_PCA_L_6_C-3**: 12 model×HP combinations, 65 common subjects
- **grid_12_folds_PCA_W_C-3**: 12 model×HP combinations, 65 common subjects
- **grid_12_folds_PCA_W_F-3**: 12 model×HP combinations, 65 common subjects
- **grid_50_random_folds**: 12 model×HP combinations, 65 common subjects
- **grid_50_random_folds_Anova_L_2_incomplete**: 12 model×HP combinations, 17 common subjects
- **grid_50_random_folds_Anova_L_6_Incomplete**: 12 model×HP combinations, 45 common subjects
- **grid_50_random_folds_PCA_L_2**: 12 model×HP combinations, 49 common subjects
- **grid_50_random_folds_PCA_L_6**: 12 model×HP combinations, 65 common subjects

## 📊 Results by Experiment and Model×Hyperparameter

## grid_12_folds_ANOVA_L_6_C_Resource_Boosted

**Common subjects (used for all models)**: 65

### ANOVA

#### ANOVA (hidden=100)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 46 | 19 | 49 | 33 | 16 | 16 | 0.754 |
| 0.55 ⭐ | 65 | 36 | 29 | 43 | 22 | 52 | 33 | 19 | 13 | 0.800 |
| 0.60 | 65 | 36 | 29 | 40 | 25 | 51 | 31 | 20 | 14 | 0.785 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 43 (66.2%)
- **Predicted as Control**: 22 (33.8%)
- **Correctly Classified**: 52 out of 65 (80.0%)
  - Correct AD: 33 out of 36 (91.7%)
  - Correct Control: 19 out of 29 (65.5%)
- **Incorrectly Classified**: 13 (20.0%)
  - AD → Control: 3
  - Control → AD: 10

---

#### ANOVA (hidden=150_50)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 65 | 36 | 29 | 41 | 24 | 52 | 32 | 20 | 13 | 0.800 |
| 0.50 | 65 | 36 | 29 | 37 | 28 | 48 | 28 | 20 | 17 | 0.738 |
| 0.55 | 65 | 36 | 29 | 33 | 32 | 48 | 26 | 22 | 17 | 0.738 |
| 0.60 | 65 | 36 | 29 | 31 | 34 | 48 | 25 | 23 | 17 | 0.738 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 41 (63.1%)
- **Predicted as Control**: 24 (36.9%)
- **Correctly Classified**: 52 out of 65 (80.0%)
  - Correct AD: 32 out of 36 (88.9%)
  - Correct Control: 20 out of 29 (69.0%)
- **Incorrectly Classified**: 13 (20.0%)
  - AD → Control: 4
  - Control → AD: 9

---

#### ANOVA (hidden=200_100_50)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 65 | 36 | 29 | 41 | 24 | 50 | 31 | 19 | 15 | 0.769 |
| 0.50 | 65 | 36 | 29 | 36 | 29 | 47 | 27 | 20 | 18 | 0.723 |
| 0.55 | 65 | 36 | 29 | 32 | 33 | 47 | 25 | 22 | 18 | 0.723 |
| 0.60 | 65 | 36 | 29 | 30 | 35 | 47 | 24 | 23 | 18 | 0.723 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 41 (63.1%)
- **Predicted as Control**: 24 (36.9%)
- **Correctly Classified**: 50 out of 65 (76.9%)
  - Correct AD: 31 out of 36 (86.1%)
  - Correct Control: 19 out of 29 (65.5%)
- **Incorrectly Classified**: 15 (23.1%)
  - AD → Control: 5
  - Control → AD: 10

---

#### ANOVA (kernel=linear)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 44 | 21 | 51 | 33 | 18 | 14 | 0.785 |
| 0.55 ⭐ | 65 | 36 | 29 | 41 | 24 | 54 | 33 | 21 | 11 | 0.831 |
| 0.60 | 65 | 36 | 29 | 41 | 24 | 54 | 33 | 21 | 11 | 0.831 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 41 (63.1%)
- **Predicted as Control**: 24 (36.9%)
- **Correctly Classified**: 54 out of 65 (83.1%)
  - Correct AD: 33 out of 36 (91.7%)
  - Correct Control: 21 out of 29 (72.4%)
- **Incorrectly Classified**: 11 (16.9%)
  - AD → Control: 3
  - Control → AD: 8

---

#### ANOVA (kernel=poly)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 50 | 15 | 47 | 34 | 13 | 18 | 0.723 |
| 0.55 | 65 | 36 | 29 | 48 | 17 | 49 | 34 | 15 | 16 | 0.754 |
| 0.60 | 65 | 36 | 29 | 45 | 20 | 48 | 32 | 16 | 17 | 0.738 |
| 0.65 ⭐ | 65 | 36 | 29 | 43 | 22 | 50 | 32 | 18 | 15 | 0.769 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 43 (66.2%)
- **Predicted as Control**: 22 (33.8%)
- **Correctly Classified**: 50 out of 65 (76.9%)
  - Correct AD: 32 out of 36 (88.9%)
  - Correct Control: 18 out of 29 (62.1%)
- **Incorrectly Classified**: 15 (23.1%)
  - AD → Control: 4
  - Control → AD: 11

---

#### ANOVA (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 50 | 15 | 47 | 34 | 13 | 18 | 0.723 |
| 0.55 | 65 | 36 | 29 | 48 | 17 | 49 | 34 | 15 | 16 | 0.754 |
| 0.60 ⭐ | 65 | 36 | 29 | 47 | 18 | 50 | 34 | 16 | 15 | 0.769 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 47 (72.3%)
- **Predicted as Control**: 18 (27.7%)
- **Correctly Classified**: 50 out of 65 (76.9%)
  - Correct AD: 34 out of 36 (94.4%)
  - Correct Control: 16 out of 29 (55.2%)
- **Incorrectly Classified**: 15 (23.1%)
  - AD → Control: 2
  - Control → AD: 13

---

#### ANOVA (max_depth=3)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 40 | 25 | 47 | 29 | 18 | 18 | 0.723 |
| 0.55 | 65 | 36 | 29 | 40 | 25 | 47 | 29 | 18 | 18 | 0.723 |
| 0.60 | 65 | 36 | 29 | 40 | 25 | 47 | 29 | 18 | 18 | 0.723 |
| 0.65 ⭐ | 65 | 36 | 29 | 32 | 33 | 51 | 27 | 24 | 14 | 0.785 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 32 (49.2%)
- **Predicted as Control**: 33 (50.8%)
- **Correctly Classified**: 51 out of 65 (78.5%)
  - Correct AD: 27 out of 36 (75.0%)
  - Correct Control: 24 out of 29 (82.8%)
- **Incorrectly Classified**: 14 (21.5%)
  - AD → Control: 9
  - Control → AD: 5

---

#### ANOVA (max_depth=6)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 41 | 24 | 46 | 29 | 17 | 19 | 0.708 |
| 0.55 | 65 | 36 | 29 | 38 | 27 | 47 | 28 | 19 | 18 | 0.723 |
| 0.60 | 65 | 36 | 29 | 35 | 30 | 46 | 26 | 20 | 19 | 0.708 |
| 0.65 ⭐ | 65 | 36 | 29 | 31 | 34 | 48 | 25 | 23 | 17 | 0.738 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 31 (47.7%)
- **Predicted as Control**: 34 (52.3%)
- **Correctly Classified**: 48 out of 65 (73.8%)
  - Correct AD: 25 out of 36 (69.4%)
  - Correct Control: 23 out of 29 (79.3%)
- **Incorrectly Classified**: 17 (26.2%)
  - AD → Control: 11
  - Control → AD: 6

---

#### ANOVA (max_depth=9)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 39 | 26 | 48 | 29 | 19 | 17 | 0.738 |
| 0.55 | 65 | 36 | 29 | 37 | 28 | 48 | 28 | 20 | 17 | 0.738 |
| 0.60 ⭐ | 65 | 36 | 29 | 34 | 31 | 49 | 27 | 22 | 16 | 0.754 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 34 (52.3%)
- **Predicted as Control**: 31 (47.7%)
- **Correctly Classified**: 49 out of 65 (75.4%)
  - Correct AD: 27 out of 36 (75.0%)
  - Correct Control: 22 out of 29 (75.9%)
- **Incorrectly Classified**: 16 (24.6%)
  - AD → Control: 9
  - Control → AD: 7

---

#### ANOVA (n_neighbors=1)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 65 | 36 | 29 | 37 | 28 | 54 | 31 | 23 | 11 | 0.831 |
| 0.55 | 65 | 36 | 29 | 31 | 34 | 52 | 27 | 25 | 13 | 0.800 |
| 0.60 | 65 | 36 | 29 | 28 | 37 | 53 | 26 | 27 | 12 | 0.815 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 37 (56.9%)
- **Predicted as Control**: 28 (43.1%)
- **Correctly Classified**: 54 out of 65 (83.1%)
  - Correct AD: 31 out of 36 (86.1%)
  - Correct Control: 23 out of 29 (79.3%)
- **Incorrectly Classified**: 11 (16.9%)
  - AD → Control: 5
  - Control → AD: 6

---

#### ANOVA (n_neighbors=15)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 65 | 36 | 29 | 36 | 29 | 53 | 30 | 23 | 12 | 0.815 |
| 0.55 | 65 | 36 | 29 | 35 | 30 | 52 | 29 | 23 | 13 | 0.800 |
| 0.60 | 65 | 36 | 29 | 34 | 31 | 51 | 28 | 23 | 14 | 0.785 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 53 out of 65 (81.5%)
  - Correct AD: 30 out of 36 (83.3%)
  - Correct Control: 23 out of 29 (79.3%)
- **Incorrectly Classified**: 12 (18.5%)
  - AD → Control: 6
  - Control → AD: 6

---

#### ANOVA (n_neighbors=7)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 65 | 36 | 29 | 39 | 26 | 54 | 32 | 22 | 11 | 0.831 |
| 0.50 | 65 | 36 | 29 | 37 | 28 | 54 | 31 | 23 | 11 | 0.831 |
| 0.55 | 65 | 36 | 29 | 35 | 30 | 52 | 29 | 23 | 13 | 0.800 |
| 0.60 | 65 | 36 | 29 | 32 | 33 | 53 | 28 | 25 | 12 | 0.815 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 39 (60.0%)
- **Predicted as Control**: 26 (40.0%)
- **Correctly Classified**: 54 out of 65 (83.1%)
  - Correct AD: 32 out of 36 (88.9%)
  - Correct Control: 22 out of 29 (75.9%)
- **Incorrectly Classified**: 11 (16.9%)
  - AD → Control: 4
  - Control → AD: 7

---

## grid_12_folds_ANOVA_W_C

**Common subjects (used for all models)**: 65

### ANOVA

#### ANOVA (hidden=100)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 43 | 22 | 56 | 35 | 21 | 9 | 0.862 |
| 0.55 | 65 | 36 | 29 | 40 | 25 | 57 | 34 | 23 | 8 | 0.877 |
| 0.60 | 65 | 36 | 29 | 39 | 26 | 58 | 34 | 24 | 7 | 0.892 |
| 0.70 ⭐ | 65 | 36 | 29 | 36 | 29 | 61 | 34 | 27 | 4 | 0.938 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 61 out of 65 (93.8%)
  - Correct AD: 34 out of 36 (94.4%)
  - Correct Control: 27 out of 29 (93.1%)
- **Incorrectly Classified**: 4 (6.2%)
  - AD → Control: 2
  - Control → AD: 2

---

#### ANOVA (hidden=150_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 37 | 28 | 62 | 35 | 27 | 3 | 0.954 |
| 0.50 | 65 | 36 | 29 | 33 | 32 | 62 | 33 | 29 | 3 | 0.954 |
| 0.55 | 65 | 36 | 29 | 32 | 33 | 61 | 32 | 29 | 4 | 0.938 |
| 0.60 | 65 | 36 | 29 | 31 | 34 | 60 | 31 | 29 | 5 | 0.923 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 37 (56.9%)
- **Predicted as Control**: 28 (43.1%)
- **Correctly Classified**: 62 out of 65 (95.4%)
  - Correct AD: 35 out of 36 (97.2%)
  - Correct Control: 27 out of 29 (93.1%)
- **Incorrectly Classified**: 3 (4.6%)
  - AD → Control: 1
  - Control → AD: 2

---

#### ANOVA (hidden=200_100_50)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 38 | 27 | 63 | 36 | 27 | 2 | 0.969 |
| 0.55 | 65 | 36 | 29 | 38 | 27 | 63 | 36 | 27 | 2 | 0.969 |
| 0.60 ⭐ | 65 | 36 | 29 | 37 | 28 | 64 | 36 | 28 | 1 | 0.985 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 37 (56.9%)
- **Predicted as Control**: 28 (43.1%)
- **Correctly Classified**: 64 out of 65 (98.5%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 28 out of 29 (96.6%)
- **Incorrectly Classified**: 1 (1.5%)
  - AD → Control: 0
  - Control → AD: 1

---

#### ANOVA (kernel=linear)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 44 | 21 | 53 | 34 | 19 | 12 | 0.815 |
| 0.55 | 65 | 36 | 29 | 40 | 25 | 57 | 34 | 23 | 8 | 0.877 |
| 0.60 | 65 | 36 | 29 | 39 | 26 | 58 | 34 | 24 | 7 | 0.892 |
| 0.65 ⭐ | 65 | 36 | 29 | 38 | 27 | 59 | 34 | 25 | 6 | 0.908 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 38 (58.5%)
- **Predicted as Control**: 27 (41.5%)
- **Correctly Classified**: 59 out of 65 (90.8%)
  - Correct AD: 34 out of 36 (94.4%)
  - Correct Control: 25 out of 29 (86.2%)
- **Incorrectly Classified**: 6 (9.2%)
  - AD → Control: 2
  - Control → AD: 4

---

#### ANOVA (kernel=poly)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 50 | 15 | 47 | 34 | 13 | 18 | 0.723 |
| 0.55 | 65 | 36 | 29 | 48 | 17 | 49 | 34 | 15 | 16 | 0.754 |
| 0.60 ⭐ | 65 | 36 | 29 | 45 | 20 | 50 | 33 | 17 | 15 | 0.769 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 45 (69.2%)
- **Predicted as Control**: 20 (30.8%)
- **Correctly Classified**: 50 out of 65 (76.9%)
  - Correct AD: 33 out of 36 (91.7%)
  - Correct Control: 17 out of 29 (58.6%)
- **Incorrectly Classified**: 15 (23.1%)
  - AD → Control: 3
  - Control → AD: 12

---

#### ANOVA (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 51 | 14 | 48 | 35 | 13 | 17 | 0.738 |
| 0.55 | 65 | 36 | 29 | 49 | 16 | 50 | 35 | 15 | 15 | 0.769 |
| 0.60 ⭐ | 65 | 36 | 29 | 46 | 19 | 51 | 34 | 17 | 14 | 0.785 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 46 (70.8%)
- **Predicted as Control**: 19 (29.2%)
- **Correctly Classified**: 51 out of 65 (78.5%)
  - Correct AD: 34 out of 36 (94.4%)
  - Correct Control: 17 out of 29 (58.6%)
- **Incorrectly Classified**: 14 (21.5%)
  - AD → Control: 2
  - Control → AD: 12

---

#### ANOVA (max_depth=3)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 38 | 27 | 63 | 36 | 27 | 2 | 0.969 |
| 0.55 ⭐ | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.60 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 65 out of 65 (100.0%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 0 (0.0%)
  - AD → Control: 0
  - Control → AD: 0

---

#### ANOVA (max_depth=6)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.50 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.55 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.60 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 65 out of 65 (100.0%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 0 (0.0%)
  - AD → Control: 0
  - Control → AD: 0

---

#### ANOVA (max_depth=9)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.50 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.55 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.60 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 65 out of 65 (100.0%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 0 (0.0%)
  - AD → Control: 0
  - Control → AD: 0

---

#### ANOVA (n_neighbors=1)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.50 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.55 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.60 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 65 out of 65 (100.0%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 0 (0.0%)
  - AD → Control: 0
  - Control → AD: 0

---

#### ANOVA (n_neighbors=15)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.50 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.55 | 65 | 36 | 29 | 35 | 30 | 64 | 35 | 29 | 1 | 0.985 |
| 0.60 | 65 | 36 | 29 | 34 | 31 | 63 | 34 | 29 | 2 | 0.969 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 65 out of 65 (100.0%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 0 (0.0%)
  - AD → Control: 0
  - Control → AD: 0

---

#### ANOVA (n_neighbors=7)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.50 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.55 | 65 | 36 | 29 | 36 | 29 | 65 | 36 | 29 | 0 | 1.000 |
| 0.60 | 65 | 36 | 29 | 34 | 31 | 63 | 34 | 29 | 2 | 0.969 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 65 out of 65 (100.0%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 0 (0.0%)
  - AD → Control: 0
  - Control → AD: 0

---

## grid_12_folds_ANOVA_W_F

**Common subjects (used for all models)**: 65

### ANOVA

#### ANOVA (hidden=100)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### ANOVA (hidden=150_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### ANOVA (hidden=200_100_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### ANOVA (kernel=linear)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 65 (100.0%)
- **Correctly Classified**: 29 out of 65 (44.6%)
  - Correct AD: 0 out of 36 (0.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 36 (55.4%)
  - AD → Control: 36
  - Control → AD: 0

---

#### ANOVA (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 65 (100.0%)
- **Correctly Classified**: 29 out of 65 (44.6%)
  - Correct AD: 0 out of 36 (0.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 36 (55.4%)
  - AD → Control: 36
  - Control → AD: 0

---

#### ANOVA (kernel=rbf)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 65 (100.0%)
- **Correctly Classified**: 29 out of 65 (44.6%)
  - Correct AD: 0 out of 36 (0.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 36 (55.4%)
  - AD → Control: 36
  - Control → AD: 0

---

#### ANOVA (max_depth=3)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### ANOVA (max_depth=6)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### ANOVA (max_depth=9)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### ANOVA (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 65 (100.0%)
- **Correctly Classified**: 29 out of 65 (44.6%)
  - Correct AD: 0 out of 36 (0.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 36 (55.4%)
  - AD → Control: 36
  - Control → AD: 0

---

#### ANOVA (n_neighbors=15)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### ANOVA (n_neighbors=7)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

## grid_12_folds_PCA_L_6_C-3

**Common subjects (used for all models)**: 65

### PCA

#### PCA (hidden=100)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.55 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.60 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.70 ⭐ | 65 | 36 | 29 | 60 | 5 | 39 | 35 | 4 | 26 | 0.600 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 60 (92.3%)
- **Predicted as Control**: 5 (7.7%)
- **Correctly Classified**: 39 out of 65 (60.0%)
  - Correct AD: 35 out of 36 (97.2%)
  - Correct Control: 4 out of 29 (13.8%)
- **Incorrectly Classified**: 26 (40.0%)
  - AD → Control: 1
  - Control → AD: 25

---

#### PCA (hidden=150_50)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.60 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.70 ⭐ | 65 | 36 | 29 | 62 | 3 | 39 | 36 | 3 | 26 | 0.600 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 62 (95.4%)
- **Predicted as Control**: 3 (4.6%)
- **Correctly Classified**: 39 out of 65 (60.0%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 3 out of 29 (10.3%)
- **Incorrectly Classified**: 26 (40.0%)
  - AD → Control: 0
  - Control → AD: 26

---

#### PCA (hidden=200_100_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 48 | 17 | 39 | 29 | 10 | 26 | 0.600 |
| 0.50 | 65 | 36 | 29 | 45 | 20 | 36 | 26 | 10 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 44 | 21 | 37 | 26 | 11 | 28 | 0.569 |
| 0.60 | 65 | 36 | 29 | 44 | 21 | 37 | 26 | 11 | 28 | 0.569 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 48 (73.8%)
- **Predicted as Control**: 17 (26.2%)
- **Correctly Classified**: 39 out of 65 (60.0%)
  - Correct AD: 29 out of 36 (80.6%)
  - Correct Control: 10 out of 29 (34.5%)
- **Incorrectly Classified**: 26 (40.0%)
  - AD → Control: 7
  - Control → AD: 19

---

#### PCA (kernel=linear)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.50 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 65 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 36 out of 65 (55.4%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 0 out of 29 (0.0%)
- **Incorrectly Classified**: 29 (44.6%)
  - AD → Control: 0
  - Control → AD: 29

---

#### PCA (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.50 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 65 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 36 out of 65 (55.4%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 0 out of 29 (0.0%)
- **Incorrectly Classified**: 29 (44.6%)
  - AD → Control: 0
  - Control → AD: 29

---

#### PCA (kernel=rbf)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.55 | 65 | 36 | 29 | 61 | 4 | 40 | 36 | 4 | 25 | 0.615 |
| 0.60 | 65 | 36 | 29 | 60 | 5 | 41 | 36 | 5 | 24 | 0.631 |
| 0.70 ⭐ | 65 | 36 | 29 | 54 | 11 | 45 | 35 | 10 | 20 | 0.692 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 54 (83.1%)
- **Predicted as Control**: 11 (16.9%)
- **Correctly Classified**: 45 out of 65 (69.2%)
  - Correct AD: 35 out of 36 (97.2%)
  - Correct Control: 10 out of 29 (34.5%)
- **Incorrectly Classified**: 20 (30.8%)
  - AD → Control: 1
  - Control → AD: 19

---

#### PCA (max_depth=3)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.55 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.60 | 65 | 36 | 29 | 61 | 4 | 40 | 36 | 4 | 25 | 0.615 |
| 0.70 ⭐ | 65 | 36 | 29 | 60 | 5 | 41 | 36 | 5 | 24 | 0.631 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 60 (92.3%)
- **Predicted as Control**: 5 (7.7%)
- **Correctly Classified**: 41 out of 65 (63.1%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 5 out of 29 (17.2%)
- **Incorrectly Classified**: 24 (36.9%)
  - AD → Control: 0
  - Control → AD: 24

---

#### PCA (max_depth=6)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 56 | 9 | 37 | 32 | 5 | 28 | 0.569 |
| 0.55 | 65 | 36 | 29 | 55 | 10 | 38 | 32 | 6 | 27 | 0.585 |
| 0.60 | 65 | 36 | 29 | 54 | 11 | 39 | 32 | 7 | 26 | 0.600 |
| 0.70 ⭐ | 65 | 36 | 29 | 51 | 14 | 40 | 31 | 9 | 25 | 0.615 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 51 (78.5%)
- **Predicted as Control**: 14 (21.5%)
- **Correctly Classified**: 40 out of 65 (61.5%)
  - Correct AD: 31 out of 36 (86.1%)
  - Correct Control: 9 out of 29 (31.0%)
- **Incorrectly Classified**: 25 (38.5%)
  - AD → Control: 5
  - Control → AD: 20

---

#### PCA (max_depth=9)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.55 | 65 | 36 | 29 | 62 | 3 | 39 | 36 | 3 | 26 | 0.600 |
| 0.60 | 65 | 36 | 29 | 60 | 5 | 39 | 35 | 4 | 26 | 0.600 |
| 0.70 ⭐ | 65 | 36 | 29 | 58 | 7 | 41 | 35 | 6 | 24 | 0.631 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 58 (89.2%)
- **Predicted as Control**: 7 (10.8%)
- **Correctly Classified**: 41 out of 65 (63.1%)
  - Correct AD: 35 out of 36 (97.2%)
  - Correct Control: 6 out of 29 (20.7%)
- **Incorrectly Classified**: 24 (36.9%)
  - AD → Control: 1
  - Control → AD: 23

---

#### PCA (n_neighbors=1)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 65 | 36 | 29 | 3 | 62 | 32 | 3 | 29 | 33 | 0.492 |
| 0.50 | 65 | 36 | 29 | 2 | 63 | 31 | 2 | 29 | 34 | 0.477 |
| 0.55 | 65 | 36 | 29 | 2 | 63 | 31 | 2 | 29 | 34 | 0.477 |
| 0.60 | 65 | 36 | 29 | 2 | 63 | 31 | 2 | 29 | 34 | 0.477 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 3 (4.6%)
- **Predicted as Control**: 62 (95.4%)
- **Correctly Classified**: 32 out of 65 (49.2%)
  - Correct AD: 3 out of 36 (8.3%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 33 (50.8%)
  - AD → Control: 33
  - Control → AD: 0

---

#### PCA (n_neighbors=15)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 31 | 34 | 40 | 21 | 19 | 25 | 0.615 |
| 0.50 | 65 | 36 | 29 | 15 | 50 | 38 | 12 | 26 | 27 | 0.585 |
| 0.55 | 65 | 36 | 29 | 11 | 54 | 36 | 9 | 27 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 10 | 55 | 35 | 8 | 27 | 30 | 0.538 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 31 (47.7%)
- **Predicted as Control**: 34 (52.3%)
- **Correctly Classified**: 40 out of 65 (61.5%)
  - Correct AD: 21 out of 36 (58.3%)
  - Correct Control: 19 out of 29 (65.5%)
- **Incorrectly Classified**: 25 (38.5%)
  - AD → Control: 15
  - Control → AD: 10

---

#### PCA (n_neighbors=7)

**Optimal Threshold: 0.35**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.35 ⭐ | 65 | 36 | 29 | 26 | 39 | 41 | 19 | 22 | 24 | 0.631 |
| 0.50 | 65 | 36 | 29 | 19 | 46 | 38 | 14 | 24 | 27 | 0.585 |
| 0.55 | 65 | 36 | 29 | 17 | 48 | 36 | 12 | 24 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 14 | 51 | 35 | 10 | 25 | 30 | 0.538 |

**Detailed Breakdown at Optimal Threshold (0.35):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 26 (40.0%)
- **Predicted as Control**: 39 (60.0%)
- **Correctly Classified**: 41 out of 65 (63.1%)
  - Correct AD: 19 out of 36 (52.8%)
  - Correct Control: 22 out of 29 (75.9%)
- **Incorrectly Classified**: 24 (36.9%)
  - AD → Control: 17
  - Control → AD: 7

---

## grid_12_folds_PCA_W_C-3

**Common subjects (used for all models)**: 65

### PCA

#### PCA (hidden=100)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (hidden=150_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (hidden=200_100_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (kernel=linear)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (kernel=rbf)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 65 (100.0%)
- **Correctly Classified**: 29 out of 65 (44.6%)
  - Correct AD: 0 out of 36 (0.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 36 (55.4%)
  - AD → Control: 36
  - Control → AD: 0

---

#### PCA (max_depth=3)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (max_depth=6)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (max_depth=9)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (n_neighbors=15)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (n_neighbors=7)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

## grid_12_folds_PCA_W_F-3

**Common subjects (used for all models)**: 65

### PCA

#### PCA (hidden=100)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (hidden=150_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (hidden=200_100_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (kernel=linear)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (kernel=rbf)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 65 (100.0%)
- **Correctly Classified**: 29 out of 65 (44.6%)
  - Correct AD: 0 out of 36 (0.0%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 36 (55.4%)
  - AD → Control: 36
  - Control → AD: 0

---

#### PCA (max_depth=3)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (max_depth=6)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (max_depth=9)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (n_neighbors=15)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

#### PCA (n_neighbors=7)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 1 | 64 | 30 | 1 | 29 | 35 | 0.462 |
| 0.50 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.55 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |
| 0.60 | 65 | 36 | 29 | 0 | 65 | 29 | 0 | 29 | 36 | 0.446 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 1 (1.5%)
- **Predicted as Control**: 64 (98.5%)
- **Correctly Classified**: 30 out of 65 (46.2%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 29 out of 29 (100.0%)
- **Incorrectly Classified**: 35 (53.8%)
  - AD → Control: 35
  - Control → AD: 0

---

## grid_50_random_folds

**Common subjects (used for all models)**: 65

### ml

#### ml (hidden=100)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 40 | 25 | 53 | 32 | 21 | 12 | 0.815 |
| 0.55 ⭐ | 65 | 36 | 29 | 39 | 26 | 54 | 32 | 22 | 11 | 0.831 |
| 0.60 | 65 | 36 | 29 | 37 | 28 | 54 | 31 | 23 | 11 | 0.831 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 39 (60.0%)
- **Predicted as Control**: 26 (40.0%)
- **Correctly Classified**: 54 out of 65 (83.1%)
  - Correct AD: 32 out of 36 (88.9%)
  - Correct Control: 22 out of 29 (75.9%)
- **Incorrectly Classified**: 11 (16.9%)
  - AD → Control: 4
  - Control → AD: 7

---

#### ml (hidden=150_50)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 38 | 27 | 53 | 31 | 22 | 12 | 0.815 |
| 0.55 ⭐ | 65 | 36 | 29 | 35 | 30 | 54 | 30 | 24 | 11 | 0.831 |
| 0.60 | 65 | 36 | 29 | 35 | 30 | 54 | 30 | 24 | 11 | 0.831 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 35 (53.8%)
- **Predicted as Control**: 30 (46.2%)
- **Correctly Classified**: 54 out of 65 (83.1%)
  - Correct AD: 30 out of 36 (83.3%)
  - Correct Control: 24 out of 29 (82.8%)
- **Incorrectly Classified**: 11 (16.9%)
  - AD → Control: 6
  - Control → AD: 5

---

#### ml (hidden=200_100_50)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 65 | 36 | 29 | 36 | 29 | 53 | 30 | 23 | 12 | 0.815 |
| 0.55 | 65 | 36 | 29 | 34 | 31 | 53 | 29 | 24 | 12 | 0.815 |
| 0.60 | 65 | 36 | 29 | 31 | 34 | 50 | 26 | 24 | 15 | 0.769 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 53 out of 65 (81.5%)
  - Correct AD: 30 out of 36 (83.3%)
  - Correct Control: 23 out of 29 (79.3%)
- **Incorrectly Classified**: 12 (18.5%)
  - AD → Control: 6
  - Control → AD: 6

---

#### ml (kernel=linear)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 44 | 21 | 51 | 33 | 18 | 14 | 0.785 |
| 0.55 | 65 | 36 | 29 | 42 | 23 | 53 | 33 | 20 | 12 | 0.815 |
| 0.60 | 65 | 36 | 29 | 42 | 23 | 53 | 33 | 20 | 12 | 0.815 |
| 0.65 ⭐ | 65 | 36 | 29 | 41 | 24 | 54 | 33 | 21 | 11 | 0.831 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 41 (63.1%)
- **Predicted as Control**: 24 (36.9%)
- **Correctly Classified**: 54 out of 65 (83.1%)
  - Correct AD: 33 out of 36 (91.7%)
  - Correct Control: 21 out of 29 (72.4%)
- **Incorrectly Classified**: 11 (16.9%)
  - AD → Control: 3
  - Control → AD: 8

---

#### ml (kernel=poly)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 51 | 14 | 46 | 34 | 12 | 19 | 0.708 |
| 0.55 | 65 | 36 | 29 | 48 | 17 | 47 | 33 | 14 | 18 | 0.723 |
| 0.60 | 65 | 36 | 29 | 44 | 21 | 49 | 32 | 17 | 16 | 0.754 |
| 0.65 ⭐ | 65 | 36 | 29 | 43 | 22 | 50 | 32 | 18 | 15 | 0.769 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 43 (66.2%)
- **Predicted as Control**: 22 (33.8%)
- **Correctly Classified**: 50 out of 65 (76.9%)
  - Correct AD: 32 out of 36 (88.9%)
  - Correct Control: 18 out of 29 (62.1%)
- **Incorrectly Classified**: 15 (23.1%)
  - AD → Control: 4
  - Control → AD: 11

---

#### ml (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 50 | 15 | 47 | 34 | 13 | 18 | 0.723 |
| 0.55 | 65 | 36 | 29 | 49 | 16 | 48 | 34 | 14 | 17 | 0.738 |
| 0.60 ⭐ | 65 | 36 | 29 | 46 | 19 | 51 | 34 | 17 | 14 | 0.785 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 46 (70.8%)
- **Predicted as Control**: 19 (29.2%)
- **Correctly Classified**: 51 out of 65 (78.5%)
  - Correct AD: 34 out of 36 (94.4%)
  - Correct Control: 17 out of 29 (58.6%)
- **Incorrectly Classified**: 14 (21.5%)
  - AD → Control: 2
  - Control → AD: 12

---

#### ml (max_depth=3)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 43 | 22 | 50 | 32 | 18 | 15 | 0.769 |
| 0.55 ⭐ | 65 | 36 | 29 | 40 | 25 | 51 | 31 | 20 | 14 | 0.785 |
| 0.60 | 65 | 36 | 29 | 34 | 31 | 49 | 27 | 22 | 16 | 0.754 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 40 (61.5%)
- **Predicted as Control**: 25 (38.5%)
- **Correctly Classified**: 51 out of 65 (78.5%)
  - Correct AD: 31 out of 36 (86.1%)
  - Correct Control: 20 out of 29 (69.0%)
- **Incorrectly Classified**: 14 (21.5%)
  - AD → Control: 5
  - Control → AD: 9

---

#### ml (max_depth=6)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 65 | 36 | 29 | 41 | 24 | 52 | 32 | 20 | 13 | 0.800 |
| 0.55 | 65 | 36 | 29 | 37 | 28 | 52 | 30 | 22 | 13 | 0.800 |
| 0.60 | 65 | 36 | 29 | 32 | 33 | 51 | 27 | 24 | 14 | 0.785 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 41 (63.1%)
- **Predicted as Control**: 24 (36.9%)
- **Correctly Classified**: 52 out of 65 (80.0%)
  - Correct AD: 32 out of 36 (88.9%)
  - Correct Control: 20 out of 29 (69.0%)
- **Incorrectly Classified**: 13 (20.0%)
  - AD → Control: 4
  - Control → AD: 9

---

#### ml (max_depth=9)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 39 | 26 | 50 | 30 | 20 | 15 | 0.769 |
| 0.55 | 65 | 36 | 29 | 38 | 27 | 51 | 30 | 21 | 14 | 0.785 |
| 0.60 ⭐ | 65 | 36 | 29 | 31 | 34 | 52 | 27 | 25 | 13 | 0.800 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 31 (47.7%)
- **Predicted as Control**: 34 (52.3%)
- **Correctly Classified**: 52 out of 65 (80.0%)
  - Correct AD: 27 out of 36 (75.0%)
  - Correct Control: 25 out of 29 (86.2%)
- **Incorrectly Classified**: 13 (20.0%)
  - AD → Control: 9
  - Control → AD: 4

---

#### ml (n_neighbors=1)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 65 | 36 | 29 | 38 | 27 | 55 | 32 | 23 | 10 | 0.846 |
| 0.50 | 65 | 36 | 29 | 36 | 29 | 55 | 31 | 24 | 10 | 0.846 |
| 0.55 | 65 | 36 | 29 | 32 | 33 | 55 | 29 | 26 | 10 | 0.846 |
| 0.60 | 65 | 36 | 29 | 26 | 39 | 49 | 23 | 26 | 16 | 0.754 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 38 (58.5%)
- **Predicted as Control**: 27 (41.5%)
- **Correctly Classified**: 55 out of 65 (84.6%)
  - Correct AD: 32 out of 36 (88.9%)
  - Correct Control: 23 out of 29 (79.3%)
- **Incorrectly Classified**: 10 (15.4%)
  - AD → Control: 4
  - Control → AD: 6

---

#### ml (n_neighbors=15)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 65 | 36 | 29 | 37 | 28 | 54 | 31 | 23 | 11 | 0.831 |
| 0.50 | 65 | 36 | 29 | 35 | 30 | 54 | 30 | 24 | 11 | 0.831 |
| 0.55 | 65 | 36 | 29 | 33 | 32 | 54 | 29 | 25 | 11 | 0.831 |
| 0.60 | 65 | 36 | 29 | 32 | 33 | 53 | 28 | 25 | 12 | 0.815 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 37 (56.9%)
- **Predicted as Control**: 28 (43.1%)
- **Correctly Classified**: 54 out of 65 (83.1%)
  - Correct AD: 31 out of 36 (86.1%)
  - Correct Control: 23 out of 29 (79.3%)
- **Incorrectly Classified**: 11 (16.9%)
  - AD → Control: 5
  - Control → AD: 6

---

#### ml (n_neighbors=7)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 65 | 36 | 29 | 36 | 29 | 55 | 31 | 24 | 10 | 0.846 |
| 0.55 | 65 | 36 | 29 | 35 | 30 | 54 | 30 | 24 | 11 | 0.831 |
| 0.60 | 65 | 36 | 29 | 31 | 34 | 54 | 28 | 26 | 11 | 0.831 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 55 out of 65 (84.6%)
  - Correct AD: 31 out of 36 (86.1%)
  - Correct Control: 24 out of 29 (82.8%)
- **Incorrectly Classified**: 10 (15.4%)
  - AD → Control: 5
  - Control → AD: 5

---

## grid_50_random_folds_Anova_L_2_incomplete

**Common subjects (used for all models)**: 17
Subject IDs: [np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(16), np.int32(17), np.int32(18), np.int32(39), np.int32(41), np.int32(42), np.int32(44), np.int32(51), np.int32(54), np.int32(58), np.int32(59), np.int32(61), np.int32(62)]

### Anova

#### Anova (hidden=100)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.55 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.60 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.65 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (hidden=150_50)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |
| 0.55 ⭐ | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.60 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 10 (58.8%)
- **Predicted as Control**: 7 (41.2%)
- **Correctly Classified**: 14 out of 17 (82.4%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 7 out of 10 (70.0%)
- **Incorrectly Classified**: 3 (17.6%)
  - AD → Control: 0
  - Control → AD: 3

---

#### Anova (hidden=200_100_50)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |
| 0.55 | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |
| 0.60 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.65 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (kernel=linear)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.55 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.60 | 17 | 7 | 10 | 10 | 7 | 14 | 7 | 7 | 3 | 0.824 |
| 0.70 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (kernel=poly)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 12 | 5 | 12 | 7 | 5 | 5 | 0.706 |
| 0.55 ⭐ | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |
| 0.60 | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 11 (64.7%)
- **Predicted as Control**: 6 (35.3%)
- **Correctly Classified**: 13 out of 17 (76.5%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 6 out of 10 (60.0%)
- **Incorrectly Classified**: 4 (23.5%)
  - AD → Control: 0
  - Control → AD: 4

---

#### Anova (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 12 | 5 | 12 | 7 | 5 | 5 | 0.706 |
| 0.55 | 17 | 7 | 10 | 12 | 5 | 12 | 7 | 5 | 5 | 0.706 |
| 0.60 ⭐ | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 11 (64.7%)
- **Predicted as Control**: 6 (35.3%)
- **Correctly Classified**: 13 out of 17 (76.5%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 6 out of 10 (60.0%)
- **Incorrectly Classified**: 4 (23.5%)
  - AD → Control: 0
  - Control → AD: 4

---

#### Anova (max_depth=3)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 12 | 5 | 12 | 7 | 5 | 5 | 0.706 |
| 0.55 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.60 | 17 | 7 | 10 | 8 | 9 | 14 | 6 | 8 | 3 | 0.824 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (max_depth=6)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |
| 0.55 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.60 | 17 | 7 | 10 | 8 | 9 | 14 | 6 | 8 | 3 | 0.824 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (max_depth=9)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 17 | 7 | 10 | 11 | 6 | 13 | 7 | 6 | 4 | 0.765 |
| 0.55 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.60 | 17 | 7 | 10 | 8 | 9 | 14 | 6 | 8 | 3 | 0.824 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (n_neighbors=1)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.50 | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.55 | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.60 | 17 | 7 | 10 | 7 | 10 | 13 | 5 | 8 | 4 | 0.765 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (n_neighbors=15)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.50 | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.55 | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.60 | 17 | 7 | 10 | 8 | 9 | 14 | 6 | 8 | 3 | 0.824 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

#### Anova (n_neighbors=7)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.50 | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.55 | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |
| 0.60 | 17 | 7 | 10 | 9 | 8 | 15 | 7 | 8 | 2 | 0.882 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 17
- **True AD**: 7 | **True Control**: 10
- **Predicted as AD**: 9 (52.9%)
- **Predicted as Control**: 8 (47.1%)
- **Correctly Classified**: 15 out of 17 (88.2%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 8 out of 10 (80.0%)
- **Incorrectly Classified**: 2 (11.8%)
  - AD → Control: 0
  - Control → AD: 2

---

## grid_50_random_folds_Anova_L_6_Incomplete

**Common subjects (used for all models)**: 45
Subject IDs: [np.int32(1), np.int32(2), np.int32(5), np.int32(10), np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(17), np.int32(20), np.int32(21), np.int32(24), np.int32(25), np.int32(26), np.int32(27), np.int32(28), np.int32(29), np.int32(30), np.int32(32), np.int32(33), np.int32(34), np.int32(35), np.int32(36), np.int32(37), np.int32(38), np.int32(41), np.int32(43), np.int32(44), np.int32(45), np.int32(46), np.int32(47), np.int32(48), np.int32(49), np.int32(52), np.int32(53), np.int32(55), np.int32(56), np.int32(57), np.int32(58), np.int32(59), np.int32(60), np.int32(61), np.int32(62), np.int32(64), np.int32(65)]

### Anova

#### Anova (hidden=100)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 26 | 19 | 38 | 21 | 17 | 7 | 0.844 |
| 0.55 ⭐ | 45 | 23 | 22 | 24 | 21 | 40 | 21 | 19 | 5 | 0.889 |
| 0.60 | 45 | 23 | 22 | 23 | 22 | 39 | 20 | 19 | 6 | 0.867 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 24 (53.3%)
- **Predicted as Control**: 21 (46.7%)
- **Correctly Classified**: 40 out of 45 (88.9%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 19 out of 22 (86.4%)
- **Incorrectly Classified**: 5 (11.1%)
  - AD → Control: 2
  - Control → AD: 3

---

#### Anova (hidden=150_50)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 25 | 20 | 35 | 19 | 16 | 10 | 0.778 |
| 0.55 | 45 | 23 | 22 | 23 | 22 | 37 | 19 | 18 | 8 | 0.822 |
| 0.60 ⭐ | 45 | 23 | 22 | 22 | 23 | 38 | 19 | 19 | 7 | 0.844 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 22 (48.9%)
- **Predicted as Control**: 23 (51.1%)
- **Correctly Classified**: 38 out of 45 (84.4%)
  - Correct AD: 19 out of 23 (82.6%)
  - Correct Control: 19 out of 22 (86.4%)
- **Incorrectly Classified**: 7 (15.6%)
  - AD → Control: 4
  - Control → AD: 3

---

#### Anova (hidden=200_100_50)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 45 | 23 | 22 | 26 | 19 | 40 | 22 | 18 | 5 | 0.889 |
| 0.50 | 45 | 23 | 22 | 26 | 19 | 40 | 22 | 18 | 5 | 0.889 |
| 0.55 | 45 | 23 | 22 | 22 | 23 | 38 | 19 | 19 | 7 | 0.844 |
| 0.60 | 45 | 23 | 22 | 21 | 24 | 37 | 18 | 19 | 8 | 0.822 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 26 (57.8%)
- **Predicted as Control**: 19 (42.2%)
- **Correctly Classified**: 40 out of 45 (88.9%)
  - Correct AD: 22 out of 23 (95.7%)
  - Correct Control: 18 out of 22 (81.8%)
- **Incorrectly Classified**: 5 (11.1%)
  - AD → Control: 1
  - Control → AD: 4

---

#### Anova (kernel=linear)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 30 | 15 | 36 | 22 | 14 | 9 | 0.800 |
| 0.55 | 45 | 23 | 22 | 28 | 17 | 38 | 22 | 16 | 7 | 0.844 |
| 0.60 | 45 | 23 | 22 | 28 | 17 | 38 | 22 | 16 | 7 | 0.844 |
| 0.65 ⭐ | 45 | 23 | 22 | 27 | 18 | 39 | 22 | 17 | 6 | 0.867 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 27 (60.0%)
- **Predicted as Control**: 18 (40.0%)
- **Correctly Classified**: 39 out of 45 (86.7%)
  - Correct AD: 22 out of 23 (95.7%)
  - Correct Control: 17 out of 22 (77.3%)
- **Incorrectly Classified**: 6 (13.3%)
  - AD → Control: 1
  - Control → AD: 5

---

#### Anova (kernel=poly)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 36 | 9 | 30 | 22 | 8 | 15 | 0.667 |
| 0.55 | 45 | 23 | 22 | 33 | 12 | 31 | 21 | 10 | 14 | 0.689 |
| 0.60 | 45 | 23 | 22 | 30 | 15 | 34 | 21 | 13 | 11 | 0.756 |
| 0.65 ⭐ | 45 | 23 | 22 | 29 | 16 | 35 | 21 | 14 | 10 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 29 (64.4%)
- **Predicted as Control**: 16 (35.6%)
- **Correctly Classified**: 35 out of 45 (77.8%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 14 out of 22 (63.6%)
- **Incorrectly Classified**: 10 (22.2%)
  - AD → Control: 2
  - Control → AD: 8

---

#### Anova (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 35 | 10 | 31 | 22 | 9 | 14 | 0.689 |
| 0.55 | 45 | 23 | 22 | 34 | 11 | 32 | 22 | 10 | 13 | 0.711 |
| 0.60 ⭐ | 45 | 23 | 22 | 31 | 14 | 35 | 22 | 13 | 10 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 31 (68.9%)
- **Predicted as Control**: 14 (31.1%)
- **Correctly Classified**: 35 out of 45 (77.8%)
  - Correct AD: 22 out of 23 (95.7%)
  - Correct Control: 13 out of 22 (59.1%)
- **Incorrectly Classified**: 10 (22.2%)
  - AD → Control: 1
  - Control → AD: 9

---

#### Anova (max_depth=3)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 45 | 23 | 22 | 28 | 17 | 36 | 21 | 15 | 9 | 0.800 |
| 0.55 | 45 | 23 | 22 | 27 | 18 | 35 | 20 | 15 | 10 | 0.778 |
| 0.60 | 45 | 23 | 22 | 23 | 22 | 35 | 18 | 17 | 10 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 28 (62.2%)
- **Predicted as Control**: 17 (37.8%)
- **Correctly Classified**: 36 out of 45 (80.0%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 15 out of 22 (68.2%)
- **Incorrectly Classified**: 9 (20.0%)
  - AD → Control: 2
  - Control → AD: 7

---

#### Anova (max_depth=6)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 45 | 23 | 22 | 27 | 18 | 37 | 21 | 16 | 8 | 0.822 |
| 0.55 | 45 | 23 | 22 | 25 | 20 | 35 | 19 | 16 | 10 | 0.778 |
| 0.60 | 45 | 23 | 22 | 23 | 22 | 37 | 19 | 18 | 8 | 0.822 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 27 (60.0%)
- **Predicted as Control**: 18 (40.0%)
- **Correctly Classified**: 37 out of 45 (82.2%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 16 out of 22 (72.7%)
- **Incorrectly Classified**: 8 (17.8%)
  - AD → Control: 2
  - Control → AD: 6

---

#### Anova (max_depth=9)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 25 | 20 | 35 | 19 | 16 | 10 | 0.778 |
| 0.55 ⭐ | 45 | 23 | 22 | 24 | 21 | 36 | 19 | 17 | 9 | 0.800 |
| 0.60 | 45 | 23 | 22 | 19 | 26 | 35 | 16 | 19 | 10 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 24 (53.3%)
- **Predicted as Control**: 21 (46.7%)
- **Correctly Classified**: 36 out of 45 (80.0%)
  - Correct AD: 19 out of 23 (82.6%)
  - Correct Control: 17 out of 22 (77.3%)
- **Incorrectly Classified**: 9 (20.0%)
  - AD → Control: 4
  - Control → AD: 5

---

#### Anova (n_neighbors=1)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 24 | 21 | 38 | 20 | 18 | 7 | 0.844 |
| 0.55 ⭐ | 45 | 23 | 22 | 21 | 24 | 39 | 19 | 20 | 6 | 0.867 |
| 0.60 | 45 | 23 | 22 | 18 | 27 | 36 | 16 | 20 | 9 | 0.800 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 21 (46.7%)
- **Predicted as Control**: 24 (53.3%)
- **Correctly Classified**: 39 out of 45 (86.7%)
  - Correct AD: 19 out of 23 (82.6%)
  - Correct Control: 20 out of 22 (90.9%)
- **Incorrectly Classified**: 6 (13.3%)
  - AD → Control: 4
  - Control → AD: 2

---

#### Anova (n_neighbors=15)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 45 | 23 | 22 | 24 | 21 | 38 | 20 | 18 | 7 | 0.844 |
| 0.55 | 45 | 23 | 22 | 22 | 23 | 38 | 19 | 19 | 7 | 0.844 |
| 0.60 | 45 | 23 | 22 | 21 | 24 | 37 | 18 | 19 | 8 | 0.822 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 24 (53.3%)
- **Predicted as Control**: 21 (46.7%)
- **Correctly Classified**: 38 out of 45 (84.4%)
  - Correct AD: 20 out of 23 (87.0%)
  - Correct Control: 18 out of 22 (81.8%)
- **Incorrectly Classified**: 7 (15.6%)
  - AD → Control: 3
  - Control → AD: 4

---

#### Anova (n_neighbors=7)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 24 | 21 | 38 | 20 | 18 | 7 | 0.844 |
| 0.55 | 45 | 23 | 22 | 23 | 22 | 37 | 19 | 18 | 8 | 0.822 |
| 0.60 ⭐ | 45 | 23 | 22 | 21 | 24 | 39 | 19 | 20 | 6 | 0.867 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 21 (46.7%)
- **Predicted as Control**: 24 (53.3%)
- **Correctly Classified**: 39 out of 45 (86.7%)
  - Correct AD: 19 out of 23 (82.6%)
  - Correct Control: 20 out of 22 (90.9%)
- **Incorrectly Classified**: 6 (13.3%)
  - AD → Control: 4
  - Control → AD: 2

---

## grid_50_random_folds_PCA_L_2

**Common subjects (used for all models)**: 49
Subject IDs: [np.int32(1), np.int32(2), np.int32(3), np.int32(4), np.int32(5), np.int32(6), np.int32(7), np.int32(8), np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(16), np.int32(17), np.int32(18), np.int32(19), np.int32(21), np.int32(22), np.int32(23), np.int32(24), np.int32(28), np.int32(30), np.int32(33), np.int32(35), np.int32(36), np.int32(37), np.int32(38), np.int32(39), np.int32(40), np.int32(41), np.int32(42), np.int32(44), np.int32(47), np.int32(48), np.int32(49), np.int32(50), np.int32(51), np.int32(54), np.int32(55), np.int32(56), np.int32(57), np.int32(58), np.int32(59), np.int32(60), np.int32(61), np.int32(62), np.int32(63), np.int32(64), np.int32(65)]

### PCA

#### PCA (hidden=100)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |
| 0.55 | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |
| 0.60 | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |
| 0.70 ⭐ | 49 | 25 | 24 | 47 | 2 | 27 | 25 | 2 | 22 | 0.551 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 47 (95.9%)
- **Predicted as Control**: 2 (4.1%)
- **Correctly Classified**: 27 out of 49 (55.1%)
  - Correct AD: 25 out of 25 (100.0%)
  - Correct Control: 2 out of 24 (8.3%)
- **Incorrectly Classified**: 22 (44.9%)
  - AD → Control: 0
  - Control → AD: 22

---

#### PCA (hidden=150_50)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 25 | 24 | 45 | 4 | 27 | 24 | 3 | 22 | 0.551 |
| 0.55 | 49 | 25 | 24 | 44 | 5 | 28 | 24 | 4 | 21 | 0.571 |
| 0.60 | 49 | 25 | 24 | 44 | 5 | 28 | 24 | 4 | 21 | 0.571 |
| 0.70 ⭐ | 49 | 25 | 24 | 43 | 6 | 29 | 24 | 5 | 20 | 0.592 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 43 (87.8%)
- **Predicted as Control**: 6 (12.2%)
- **Correctly Classified**: 29 out of 49 (59.2%)
  - Correct AD: 24 out of 25 (96.0%)
  - Correct Control: 5 out of 24 (20.8%)
- **Incorrectly Classified**: 20 (40.8%)
  - AD → Control: 1
  - Control → AD: 19

---

#### PCA (hidden=200_100_50)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |
| 0.55 | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |
| 0.60 ⭐ | 49 | 25 | 24 | 47 | 2 | 27 | 25 | 2 | 22 | 0.551 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 47 (95.9%)
- **Predicted as Control**: 2 (4.1%)
- **Correctly Classified**: 27 out of 49 (55.1%)
  - Correct AD: 25 out of 25 (100.0%)
  - Correct Control: 2 out of 24 (8.3%)
- **Incorrectly Classified**: 22 (44.9%)
  - AD → Control: 0
  - Control → AD: 22

---

#### PCA (kernel=linear)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 25 | 24 | 49 | 0 | 25 | 25 | 0 | 24 | 0.510 |
| 0.55 | 49 | 25 | 24 | 49 | 0 | 25 | 25 | 0 | 24 | 0.510 |
| 0.60 ⭐ | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 48 (98.0%)
- **Predicted as Control**: 1 (2.0%)
- **Correctly Classified**: 26 out of 49 (53.1%)
  - Correct AD: 25 out of 25 (100.0%)
  - Correct Control: 1 out of 24 (4.2%)
- **Incorrectly Classified**: 23 (46.9%)
  - AD → Control: 0
  - Control → AD: 23

---

#### PCA (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 49 | 25 | 24 | 49 | 0 | 25 | 25 | 0 | 24 | 0.510 |
| 0.50 | 49 | 25 | 24 | 49 | 0 | 25 | 25 | 0 | 24 | 0.510 |
| 0.55 | 49 | 25 | 24 | 49 | 0 | 25 | 25 | 0 | 24 | 0.510 |
| 0.60 | 49 | 25 | 24 | 49 | 0 | 25 | 25 | 0 | 24 | 0.510 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 49 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 25 out of 49 (51.0%)
  - Correct AD: 25 out of 25 (100.0%)
  - Correct Control: 0 out of 24 (0.0%)
- **Incorrectly Classified**: 24 (49.0%)
  - AD → Control: 0
  - Control → AD: 24

---

#### PCA (kernel=rbf)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 25 | 24 | 46 | 3 | 28 | 25 | 3 | 21 | 0.571 |
| 0.55 | 49 | 25 | 24 | 46 | 3 | 28 | 25 | 3 | 21 | 0.571 |
| 0.60 | 49 | 25 | 24 | 43 | 6 | 31 | 25 | 6 | 18 | 0.633 |
| 0.70 ⭐ | 49 | 25 | 24 | 41 | 8 | 33 | 25 | 8 | 16 | 0.673 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 41 (83.7%)
- **Predicted as Control**: 8 (16.3%)
- **Correctly Classified**: 33 out of 49 (67.3%)
  - Correct AD: 25 out of 25 (100.0%)
  - Correct Control: 8 out of 24 (33.3%)
- **Incorrectly Classified**: 16 (32.7%)
  - AD → Control: 0
  - Control → AD: 16

---

#### PCA (max_depth=3)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |
| 0.55 | 49 | 25 | 24 | 48 | 1 | 26 | 25 | 1 | 23 | 0.531 |
| 0.60 | 49 | 25 | 24 | 46 | 3 | 28 | 25 | 3 | 21 | 0.571 |
| 0.70 ⭐ | 49 | 25 | 24 | 45 | 4 | 29 | 25 | 4 | 20 | 0.592 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 45 (91.8%)
- **Predicted as Control**: 4 (8.2%)
- **Correctly Classified**: 29 out of 49 (59.2%)
  - Correct AD: 25 out of 25 (100.0%)
  - Correct Control: 4 out of 24 (16.7%)
- **Incorrectly Classified**: 20 (40.8%)
  - AD → Control: 0
  - Control → AD: 20

---

#### PCA (max_depth=6)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 25 | 24 | 46 | 3 | 28 | 25 | 3 | 21 | 0.571 |
| 0.55 | 49 | 25 | 24 | 46 | 3 | 28 | 25 | 3 | 21 | 0.571 |
| 0.60 | 49 | 25 | 24 | 44 | 5 | 28 | 24 | 4 | 21 | 0.571 |
| 0.65 ⭐ | 49 | 25 | 24 | 43 | 6 | 29 | 24 | 5 | 20 | 0.592 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 43 (87.8%)
- **Predicted as Control**: 6 (12.2%)
- **Correctly Classified**: 29 out of 49 (59.2%)
  - Correct AD: 24 out of 25 (96.0%)
  - Correct Control: 5 out of 24 (20.8%)
- **Incorrectly Classified**: 20 (40.8%)
  - AD → Control: 1
  - Control → AD: 19

---

#### PCA (max_depth=9)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 49 | 25 | 24 | 47 | 2 | 27 | 25 | 2 | 22 | 0.551 |
| 0.50 | 49 | 25 | 24 | 44 | 5 | 26 | 23 | 3 | 23 | 0.531 |
| 0.55 | 49 | 25 | 24 | 39 | 10 | 25 | 20 | 5 | 24 | 0.510 |
| 0.60 | 49 | 25 | 24 | 38 | 11 | 26 | 20 | 6 | 23 | 0.531 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 47 (95.9%)
- **Predicted as Control**: 2 (4.1%)
- **Correctly Classified**: 27 out of 49 (55.1%)
  - Correct AD: 25 out of 25 (100.0%)
  - Correct Control: 2 out of 24 (8.3%)
- **Incorrectly Classified**: 22 (44.9%)
  - AD → Control: 0
  - Control → AD: 22

---

#### PCA (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 49 | 25 | 24 | 0 | 49 | 24 | 0 | 24 | 25 | 0.490 |
| 0.50 | 49 | 25 | 24 | 0 | 49 | 24 | 0 | 24 | 25 | 0.490 |
| 0.55 | 49 | 25 | 24 | 0 | 49 | 24 | 0 | 24 | 25 | 0.490 |
| 0.60 | 49 | 25 | 24 | 0 | 49 | 24 | 0 | 24 | 25 | 0.490 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 49 (100.0%)
- **Correctly Classified**: 24 out of 49 (49.0%)
  - Correct AD: 0 out of 25 (0.0%)
  - Correct Control: 24 out of 24 (100.0%)
- **Incorrectly Classified**: 25 (51.0%)
  - AD → Control: 25
  - Control → AD: 0

---

#### PCA (n_neighbors=15)

**Optimal Threshold: 0.35**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.35 ⭐ | 49 | 25 | 24 | 14 | 35 | 32 | 11 | 21 | 17 | 0.653 |
| 0.50 | 49 | 25 | 24 | 4 | 45 | 24 | 2 | 22 | 25 | 0.490 |
| 0.55 | 49 | 25 | 24 | 3 | 46 | 23 | 1 | 22 | 26 | 0.469 |
| 0.60 | 49 | 25 | 24 | 3 | 46 | 23 | 1 | 22 | 26 | 0.469 |

**Detailed Breakdown at Optimal Threshold (0.35):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 14 (28.6%)
- **Predicted as Control**: 35 (71.4%)
- **Correctly Classified**: 32 out of 49 (65.3%)
  - Correct AD: 11 out of 25 (44.0%)
  - Correct Control: 21 out of 24 (87.5%)
- **Incorrectly Classified**: 17 (34.7%)
  - AD → Control: 14
  - Control → AD: 3

---

#### PCA (n_neighbors=7)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 49 | 25 | 24 | 25 | 24 | 33 | 17 | 16 | 16 | 0.673 |
| 0.50 | 49 | 25 | 24 | 5 | 44 | 23 | 2 | 21 | 26 | 0.469 |
| 0.55 | 49 | 25 | 24 | 2 | 47 | 22 | 0 | 22 | 27 | 0.449 |
| 0.60 | 49 | 25 | 24 | 2 | 47 | 22 | 0 | 22 | 27 | 0.449 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 49
- **True AD**: 25 | **True Control**: 24
- **Predicted as AD**: 25 (51.0%)
- **Predicted as Control**: 24 (49.0%)
- **Correctly Classified**: 33 out of 49 (67.3%)
  - Correct AD: 17 out of 25 (68.0%)
  - Correct Control: 16 out of 24 (66.7%)
- **Incorrectly Classified**: 16 (32.7%)
  - AD → Control: 8
  - Control → AD: 8

---

## grid_50_random_folds_PCA_L_6

**Common subjects (used for all models)**: 65

### PCA

#### PCA (hidden=100)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.55 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.60 | 65 | 36 | 29 | 62 | 3 | 37 | 35 | 2 | 28 | 0.569 |
| 0.70 ⭐ | 65 | 36 | 29 | 60 | 5 | 39 | 35 | 4 | 26 | 0.600 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 60 (92.3%)
- **Predicted as Control**: 5 (7.7%)
- **Correctly Classified**: 39 out of 65 (60.0%)
  - Correct AD: 35 out of 36 (97.2%)
  - Correct Control: 4 out of 29 (13.8%)
- **Incorrectly Classified**: 26 (40.0%)
  - AD → Control: 1
  - Control → AD: 25

---

#### PCA (hidden=150_50)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.55 | 65 | 36 | 29 | 61 | 4 | 38 | 35 | 3 | 27 | 0.585 |
| 0.60 | 65 | 36 | 29 | 59 | 6 | 38 | 34 | 4 | 27 | 0.585 |
| 0.70 ⭐ | 65 | 36 | 29 | 54 | 11 | 41 | 33 | 8 | 24 | 0.631 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 54 (83.1%)
- **Predicted as Control**: 11 (16.9%)
- **Correctly Classified**: 41 out of 65 (63.1%)
  - Correct AD: 33 out of 36 (91.7%)
  - Correct Control: 8 out of 29 (27.6%)
- **Incorrectly Classified**: 24 (36.9%)
  - AD → Control: 3
  - Control → AD: 21

---

#### PCA (hidden=200_100_50)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 61 | 4 | 36 | 34 | 2 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 57 | 8 | 34 | 31 | 3 | 31 | 0.523 |
| 0.60 | 65 | 36 | 29 | 55 | 10 | 36 | 31 | 5 | 29 | 0.554 |
| 0.65 ⭐ | 65 | 36 | 29 | 50 | 15 | 41 | 31 | 10 | 24 | 0.631 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 50 (76.9%)
- **Predicted as Control**: 15 (23.1%)
- **Correctly Classified**: 41 out of 65 (63.1%)
  - Correct AD: 31 out of 36 (86.1%)
  - Correct Control: 10 out of 29 (34.5%)
- **Incorrectly Classified**: 24 (36.9%)
  - AD → Control: 5
  - Control → AD: 19

---

#### PCA (kernel=linear)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.70 ⭐ | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 64 (98.5%)
- **Predicted as Control**: 1 (1.5%)
- **Correctly Classified**: 37 out of 65 (56.9%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 1 out of 29 (3.4%)
- **Incorrectly Classified**: 28 (43.1%)
  - AD → Control: 0
  - Control → AD: 28

---

#### PCA (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.50 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 65 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 36 out of 65 (55.4%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 0 out of 29 (0.0%)
- **Incorrectly Classified**: 29 (44.6%)
  - AD → Control: 0
  - Control → AD: 29

---

#### PCA (kernel=rbf)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 62 | 3 | 39 | 36 | 3 | 26 | 0.600 |
| 0.55 | 65 | 36 | 29 | 61 | 4 | 40 | 36 | 4 | 25 | 0.615 |
| 0.60 | 65 | 36 | 29 | 61 | 4 | 40 | 36 | 4 | 25 | 0.615 |
| 0.70 ⭐ | 65 | 36 | 29 | 56 | 9 | 43 | 35 | 8 | 22 | 0.662 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 56 (86.2%)
- **Predicted as Control**: 9 (13.8%)
- **Correctly Classified**: 43 out of 65 (66.2%)
  - Correct AD: 35 out of 36 (97.2%)
  - Correct Control: 8 out of 29 (27.6%)
- **Incorrectly Classified**: 22 (33.8%)
  - AD → Control: 1
  - Control → AD: 21

---

#### PCA (max_depth=3)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.55 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.60 | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |
| 0.70 ⭐ | 65 | 36 | 29 | 61 | 4 | 40 | 36 | 4 | 25 | 0.615 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 61 (93.8%)
- **Predicted as Control**: 4 (6.2%)
- **Correctly Classified**: 40 out of 65 (61.5%)
  - Correct AD: 36 out of 36 (100.0%)
  - Correct Control: 4 out of 29 (13.8%)
- **Incorrectly Classified**: 25 (38.5%)
  - AD → Control: 0
  - Control → AD: 25

---

#### PCA (max_depth=6)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 62 | 3 | 39 | 36 | 3 | 26 | 0.600 |
| 0.55 | 65 | 36 | 29 | 61 | 4 | 38 | 35 | 3 | 27 | 0.585 |
| 0.60 | 65 | 36 | 29 | 60 | 5 | 37 | 34 | 3 | 28 | 0.569 |
| 0.70 ⭐ | 65 | 36 | 29 | 53 | 12 | 44 | 34 | 10 | 21 | 0.677 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 53 (81.5%)
- **Predicted as Control**: 12 (18.5%)
- **Correctly Classified**: 44 out of 65 (67.7%)
  - Correct AD: 34 out of 36 (94.4%)
  - Correct Control: 10 out of 29 (34.5%)
- **Incorrectly Classified**: 21 (32.3%)
  - AD → Control: 2
  - Control → AD: 19

---

#### PCA (max_depth=9)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 65 | 36 | 29 | 58 | 7 | 35 | 32 | 3 | 30 | 0.538 |
| 0.55 | 65 | 36 | 29 | 56 | 9 | 35 | 31 | 4 | 30 | 0.538 |
| 0.60 | 65 | 36 | 29 | 54 | 11 | 37 | 31 | 6 | 28 | 0.569 |
| 0.70 ⭐ | 65 | 36 | 29 | 41 | 24 | 42 | 27 | 15 | 23 | 0.646 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 41 (63.1%)
- **Predicted as Control**: 24 (36.9%)
- **Correctly Classified**: 42 out of 65 (64.6%)
  - Correct AD: 27 out of 36 (75.0%)
  - Correct Control: 15 out of 29 (51.7%)
- **Incorrectly Classified**: 23 (35.4%)
  - AD → Control: 9
  - Control → AD: 14

---

#### PCA (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 65 | 36 | 29 | 2 | 63 | 29 | 1 | 28 | 36 | 0.446 |
| 0.50 | 65 | 36 | 29 | 1 | 64 | 28 | 0 | 28 | 37 | 0.431 |
| 0.55 | 65 | 36 | 29 | 1 | 64 | 28 | 0 | 28 | 37 | 0.431 |
| 0.60 | 65 | 36 | 29 | 1 | 64 | 28 | 0 | 28 | 37 | 0.431 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 2 (3.1%)
- **Predicted as Control**: 63 (96.9%)
- **Correctly Classified**: 29 out of 65 (44.6%)
  - Correct AD: 1 out of 36 (2.8%)
  - Correct Control: 28 out of 29 (96.6%)
- **Incorrectly Classified**: 36 (55.4%)
  - AD → Control: 35
  - Control → AD: 1

---

#### PCA (n_neighbors=15)

**Optimal Threshold: 0.35**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.35 ⭐ | 65 | 36 | 29 | 36 | 29 | 43 | 25 | 18 | 22 | 0.662 |
| 0.50 | 65 | 36 | 29 | 15 | 50 | 40 | 13 | 27 | 25 | 0.615 |
| 0.55 | 65 | 36 | 29 | 11 | 54 | 36 | 9 | 27 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 5 | 60 | 32 | 4 | 28 | 33 | 0.492 |

**Detailed Breakdown at Optimal Threshold (0.35):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 36 (55.4%)
- **Predicted as Control**: 29 (44.6%)
- **Correctly Classified**: 43 out of 65 (66.2%)
  - Correct AD: 25 out of 36 (69.4%)
  - Correct Control: 18 out of 29 (62.1%)
- **Incorrectly Classified**: 22 (33.8%)
  - AD → Control: 11
  - Control → AD: 11

---

#### PCA (n_neighbors=7)

**Optimal Threshold: 0.35**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.35 ⭐ | 65 | 36 | 29 | 32 | 33 | 45 | 24 | 21 | 20 | 0.692 |
| 0.50 | 65 | 36 | 29 | 14 | 51 | 41 | 13 | 28 | 24 | 0.631 |
| 0.55 | 65 | 36 | 29 | 10 | 55 | 37 | 9 | 28 | 28 | 0.569 |
| 0.60 | 65 | 36 | 29 | 5 | 60 | 32 | 4 | 28 | 33 | 0.492 |

**Detailed Breakdown at Optimal Threshold (0.35):**

- **Total Subjects**: 65
- **True AD**: 36 | **True Control**: 29
- **Predicted as AD**: 32 (49.2%)
- **Predicted as Control**: 33 (50.8%)
- **Correctly Classified**: 45 out of 65 (69.2%)
  - Correct AD: 24 out of 36 (66.7%)
  - Correct Control: 21 out of 29 (72.4%)
- **Incorrectly Classified**: 20 (30.8%)
  - AD → Control: 12
  - Control → AD: 8

---

## 📋 Summary: Optimal Thresholds by Model×Hyperparameter×Experiment

| Experiment | Model×Hyperparameters | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |
|------------|------------------------|-------------------|----------------|---------|-----------|----------|
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_hidden=100 | 0.55 | 65 | 52 | 13 | 0.800 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_hidden=150_50 | 0.45 | 65 | 52 | 13 | 0.800 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_hidden=200_100_50 | 0.45 | 65 | 50 | 15 | 0.769 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_kernel=linear | 0.55 | 65 | 54 | 11 | 0.831 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_kernel=poly | 0.65 | 65 | 50 | 15 | 0.769 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_kernel=rbf | 0.60 | 65 | 50 | 15 | 0.769 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_max_depth=3 | 0.65 | 65 | 51 | 14 | 0.785 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_max_depth=6 | 0.65 | 65 | 48 | 17 | 0.738 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_max_depth=9 | 0.60 | 65 | 49 | 16 | 0.754 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_n_neighbors=1 | 0.50 | 65 | 54 | 11 | 0.831 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_n_neighbors=15 | 0.50 | 65 | 53 | 12 | 0.815 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted | ANOVA_n_neighbors=7 | 0.45 | 65 | 54 | 11 | 0.831 |
| grid_12_folds_ANOVA_W_C | ANOVA_hidden=100 | 0.70 | 65 | 61 | 4 | 0.938 |
| grid_12_folds_ANOVA_W_C | ANOVA_hidden=150_50 | 0.30 | 65 | 62 | 3 | 0.954 |
| grid_12_folds_ANOVA_W_C | ANOVA_hidden=200_100_50 | 0.60 | 65 | 64 | 1 | 0.985 |
| grid_12_folds_ANOVA_W_C | ANOVA_kernel=linear | 0.65 | 65 | 59 | 6 | 0.908 |
| grid_12_folds_ANOVA_W_C | ANOVA_kernel=poly | 0.60 | 65 | 50 | 15 | 0.769 |
| grid_12_folds_ANOVA_W_C | ANOVA_kernel=rbf | 0.60 | 65 | 51 | 14 | 0.785 |
| grid_12_folds_ANOVA_W_C | ANOVA_max_depth=3 | 0.55 | 65 | 65 | 0 | 1.000 |
| grid_12_folds_ANOVA_W_C | ANOVA_max_depth=6 | 0.30 | 65 | 65 | 0 | 1.000 |
| grid_12_folds_ANOVA_W_C | ANOVA_max_depth=9 | 0.30 | 65 | 65 | 0 | 1.000 |
| grid_12_folds_ANOVA_W_C | ANOVA_n_neighbors=1 | 0.40 | 65 | 65 | 0 | 1.000 |
| grid_12_folds_ANOVA_W_C | ANOVA_n_neighbors=15 | 0.40 | 65 | 65 | 0 | 1.000 |
| grid_12_folds_ANOVA_W_C | ANOVA_n_neighbors=7 | 0.40 | 65 | 65 | 0 | 1.000 |
| grid_12_folds_ANOVA_W_F | ANOVA_hidden=100 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_ANOVA_W_F | ANOVA_hidden=150_50 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_ANOVA_W_F | ANOVA_hidden=200_100_50 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_ANOVA_W_F | ANOVA_kernel=linear | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_12_folds_ANOVA_W_F | ANOVA_kernel=poly | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_12_folds_ANOVA_W_F | ANOVA_kernel=rbf | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_12_folds_ANOVA_W_F | ANOVA_max_depth=3 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_ANOVA_W_F | ANOVA_max_depth=6 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_ANOVA_W_F | ANOVA_max_depth=9 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_ANOVA_W_F | ANOVA_n_neighbors=1 | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_12_folds_ANOVA_W_F | ANOVA_n_neighbors=15 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_ANOVA_W_F | ANOVA_n_neighbors=7 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_L_6_C-3 | PCA_hidden=100 | 0.70 | 65 | 39 | 26 | 0.600 |
| grid_12_folds_PCA_L_6_C-3 | PCA_hidden=150_50 | 0.70 | 65 | 39 | 26 | 0.600 |
| grid_12_folds_PCA_L_6_C-3 | PCA_hidden=200_100_50 | 0.30 | 65 | 39 | 26 | 0.600 |
| grid_12_folds_PCA_L_6_C-3 | PCA_kernel=linear | 0.30 | 65 | 36 | 29 | 0.554 |
| grid_12_folds_PCA_L_6_C-3 | PCA_kernel=poly | 0.30 | 65 | 36 | 29 | 0.554 |
| grid_12_folds_PCA_L_6_C-3 | PCA_kernel=rbf | 0.70 | 65 | 45 | 20 | 0.692 |
| grid_12_folds_PCA_L_6_C-3 | PCA_max_depth=3 | 0.70 | 65 | 41 | 24 | 0.631 |
| grid_12_folds_PCA_L_6_C-3 | PCA_max_depth=6 | 0.70 | 65 | 40 | 25 | 0.615 |
| grid_12_folds_PCA_L_6_C-3 | PCA_max_depth=9 | 0.70 | 65 | 41 | 24 | 0.631 |
| grid_12_folds_PCA_L_6_C-3 | PCA_n_neighbors=1 | 0.45 | 65 | 32 | 33 | 0.492 |
| grid_12_folds_PCA_L_6_C-3 | PCA_n_neighbors=15 | 0.30 | 65 | 40 | 25 | 0.615 |
| grid_12_folds_PCA_L_6_C-3 | PCA_n_neighbors=7 | 0.35 | 65 | 41 | 24 | 0.631 |
| grid_12_folds_PCA_W_C-3 | PCA_hidden=100 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_hidden=150_50 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_hidden=200_100_50 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_kernel=linear | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_kernel=poly | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_kernel=rbf | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_12_folds_PCA_W_C-3 | PCA_max_depth=3 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_max_depth=6 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_max_depth=9 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_n_neighbors=1 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_n_neighbors=15 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_C-3 | PCA_n_neighbors=7 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_hidden=100 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_hidden=150_50 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_hidden=200_100_50 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_kernel=linear | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_kernel=poly | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_kernel=rbf | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_12_folds_PCA_W_F-3 | PCA_max_depth=3 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_max_depth=6 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_max_depth=9 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_n_neighbors=1 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_n_neighbors=15 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_12_folds_PCA_W_F-3 | PCA_n_neighbors=7 | 0.30 | 65 | 30 | 35 | 0.462 |
| grid_50_random_folds | ml_hidden=100 | 0.55 | 65 | 54 | 11 | 0.831 |
| grid_50_random_folds | ml_hidden=150_50 | 0.55 | 65 | 54 | 11 | 0.831 |
| grid_50_random_folds | ml_hidden=200_100_50 | 0.50 | 65 | 53 | 12 | 0.815 |
| grid_50_random_folds | ml_kernel=linear | 0.65 | 65 | 54 | 11 | 0.831 |
| grid_50_random_folds | ml_kernel=poly | 0.65 | 65 | 50 | 15 | 0.769 |
| grid_50_random_folds | ml_kernel=rbf | 0.60 | 65 | 51 | 14 | 0.785 |
| grid_50_random_folds | ml_max_depth=3 | 0.55 | 65 | 51 | 14 | 0.785 |
| grid_50_random_folds | ml_max_depth=6 | 0.50 | 65 | 52 | 13 | 0.800 |
| grid_50_random_folds | ml_max_depth=9 | 0.60 | 65 | 52 | 13 | 0.800 |
| grid_50_random_folds | ml_n_neighbors=1 | 0.45 | 65 | 55 | 10 | 0.846 |
| grid_50_random_folds | ml_n_neighbors=15 | 0.45 | 65 | 54 | 11 | 0.831 |
| grid_50_random_folds | ml_n_neighbors=7 | 0.50 | 65 | 55 | 10 | 0.846 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_hidden=100 | 0.65 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_hidden=150_50 | 0.55 | 17 | 14 | 3 | 0.824 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_hidden=200_100_50 | 0.65 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_kernel=linear | 0.70 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_kernel=poly | 0.55 | 17 | 13 | 4 | 0.765 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_kernel=rbf | 0.60 | 17 | 13 | 4 | 0.765 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_max_depth=3 | 0.55 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_max_depth=6 | 0.55 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_max_depth=9 | 0.55 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_n_neighbors=1 | 0.40 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_n_neighbors=15 | 0.40 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete | Anova_n_neighbors=7 | 0.40 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_hidden=100 | 0.55 | 45 | 40 | 5 | 0.889 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_hidden=150_50 | 0.60 | 45 | 38 | 7 | 0.844 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_hidden=200_100_50 | 0.45 | 45 | 40 | 5 | 0.889 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_kernel=linear | 0.65 | 45 | 39 | 6 | 0.867 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_kernel=poly | 0.65 | 45 | 35 | 10 | 0.778 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_kernel=rbf | 0.60 | 45 | 35 | 10 | 0.778 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_max_depth=3 | 0.50 | 45 | 36 | 9 | 0.800 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_max_depth=6 | 0.50 | 45 | 37 | 8 | 0.822 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_max_depth=9 | 0.55 | 45 | 36 | 9 | 0.800 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_n_neighbors=1 | 0.55 | 45 | 39 | 6 | 0.867 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_n_neighbors=15 | 0.50 | 45 | 38 | 7 | 0.844 |
| grid_50_random_folds_Anova_L_6_Incomplete | Anova_n_neighbors=7 | 0.60 | 45 | 39 | 6 | 0.867 |
| grid_50_random_folds_PCA_L_2 | PCA_hidden=100 | 0.70 | 49 | 27 | 22 | 0.551 |
| grid_50_random_folds_PCA_L_2 | PCA_hidden=150_50 | 0.70 | 49 | 29 | 20 | 0.592 |
| grid_50_random_folds_PCA_L_2 | PCA_hidden=200_100_50 | 0.60 | 49 | 27 | 22 | 0.551 |
| grid_50_random_folds_PCA_L_2 | PCA_kernel=linear | 0.60 | 49 | 26 | 23 | 0.531 |
| grid_50_random_folds_PCA_L_2 | PCA_kernel=poly | 0.30 | 49 | 25 | 24 | 0.510 |
| grid_50_random_folds_PCA_L_2 | PCA_kernel=rbf | 0.70 | 49 | 33 | 16 | 0.673 |
| grid_50_random_folds_PCA_L_2 | PCA_max_depth=3 | 0.70 | 49 | 29 | 20 | 0.592 |
| grid_50_random_folds_PCA_L_2 | PCA_max_depth=6 | 0.65 | 49 | 29 | 20 | 0.592 |
| grid_50_random_folds_PCA_L_2 | PCA_max_depth=9 | 0.30 | 49 | 27 | 22 | 0.551 |
| grid_50_random_folds_PCA_L_2 | PCA_n_neighbors=1 | 0.30 | 49 | 24 | 25 | 0.490 |
| grid_50_random_folds_PCA_L_2 | PCA_n_neighbors=15 | 0.35 | 49 | 32 | 17 | 0.653 |
| grid_50_random_folds_PCA_L_2 | PCA_n_neighbors=7 | 0.30 | 49 | 33 | 16 | 0.673 |
| grid_50_random_folds_PCA_L_6 | PCA_hidden=100 | 0.70 | 65 | 39 | 26 | 0.600 |
| grid_50_random_folds_PCA_L_6 | PCA_hidden=150_50 | 0.70 | 65 | 41 | 24 | 0.631 |
| grid_50_random_folds_PCA_L_6 | PCA_hidden=200_100_50 | 0.65 | 65 | 41 | 24 | 0.631 |
| grid_50_random_folds_PCA_L_6 | PCA_kernel=linear | 0.70 | 65 | 37 | 28 | 0.569 |
| grid_50_random_folds_PCA_L_6 | PCA_kernel=poly | 0.30 | 65 | 36 | 29 | 0.554 |
| grid_50_random_folds_PCA_L_6 | PCA_kernel=rbf | 0.70 | 65 | 43 | 22 | 0.662 |
| grid_50_random_folds_PCA_L_6 | PCA_max_depth=3 | 0.70 | 65 | 40 | 25 | 0.615 |
| grid_50_random_folds_PCA_L_6 | PCA_max_depth=6 | 0.70 | 65 | 44 | 21 | 0.677 |
| grid_50_random_folds_PCA_L_6 | PCA_max_depth=9 | 0.70 | 65 | 42 | 23 | 0.646 |
| grid_50_random_folds_PCA_L_6 | PCA_n_neighbors=1 | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_50_random_folds_PCA_L_6 | PCA_n_neighbors=15 | 0.35 | 65 | 43 | 22 | 0.662 |
| grid_50_random_folds_PCA_L_6 | PCA_n_neighbors=7 | 0.35 | 65 | 45 | 20 | 0.692 |

## 🎯 KNN-Specific Summary (All Experiments)


## ✅ Analysis Verification

- **Total experiments analyzed**: 11
- **Total model×HP×experiment combinations**: 132
- **All parquet files processed** (no sampling)
- **Each experiment analyzed independently**
- **Fair comparison**: Only subjects present in ALL model×hp combinations within each experiment

---
*Analysis completed: 2025-12-12 21:22*
*ALL experiments in HPC_All_Data - automatically discovered*
*ALL subjects across ALL experiments - no sampling*
*Each experiment treated independently*
*Fair comparison: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)*
