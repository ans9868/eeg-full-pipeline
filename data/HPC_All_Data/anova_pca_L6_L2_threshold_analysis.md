# 🎯 Threshold Analysis: ANOVA/PCA L_6 and L_2 - Uniform vs Random Comparison

## Analysis Overview

**Key Features**:
- **L_6 and L_2 experiments** analyzed (ANOVA_L_6, ANOVA_L_2, PCA_L_6, PCA_L_2)
- **Comparison of Uniform (12-fold) vs Random (50-fold)** cross-validation strategies
- **Fair comparison on SAME test subjects**: Uniform experiments filtered to only include subjects present in random experiments
- **ALL subjects** across these experiments analyzed (no sampling)
- Each experiment treated **independently**
- Per model×hyperparameter×experiment threshold optimization
- **Fair comparison**: Only subjects present in ALL model×hp combinations AND in both uniform/random are analyzed

## 📊 Experiments Analyzed

- **grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform** (uniform): 12 model×HP combinations, 45 common subjects
- **grid_12_folds_PCA_L_6_C-3_uniform** (uniform): 12 model×HP combinations, 65 common subjects
- **grid_50_random_folds_Anova_L_2_incomplete_random** (random): 12 model×HP combinations, 17 common subjects
- **grid_50_random_folds_Anova_L_6_Incomplete_random** (random): 12 model×HP combinations, 45 common subjects
- **grid_50_random_folds_PCA_L_2_random** (random): 12 model×HP combinations, 49 common subjects
- **grid_50_random_folds_PCA_L_6_random** (random): 12 model×HP combinations, 65 common subjects

## 🔄 Uniform vs Random Comparison

### Anova L 6

**Comparison on SAME test subjects:**
- Uniform subjects: 45
- Random subjects: 45
- **Intersection (used for comparison): 45 subjects**
- Subject IDs: [np.int32(1), np.int32(2), np.int32(5), np.int32(10), np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(17), np.int32(20), np.int32(21), np.int32(24), np.int32(25), np.int32(26), np.int32(27), np.int32(28), np.int32(29), np.int32(30), np.int32(32), np.int32(33), np.int32(34), np.int32(35), np.int32(36), np.int32(37), np.int32(38), np.int32(41), np.int32(43), np.int32(44), np.int32(45), np.int32(46), np.int32(47), np.int32(48), np.int32(49), np.int32(52), np.int32(53), np.int32(55), np.int32(56), np.int32(57), np.int32(58), np.int32(59), np.int32(60), np.int32(61), np.int32(62), np.int32(64), np.int32(65)]

| Model×Hyperparameters | Uniform Threshold | Uniform Accuracy | Uniform Subjects | Random Threshold | Random Accuracy | Random Subjects | Accuracy Difference |
|------------------------|-------------------|------------------|-----------------|------------------|-----------------|-----------------|---------------------|
| HIDDEN=100 | 0.55 | 0.822 | 45 | 0.55 | 0.889 | 45 | 🟢 +0.067 |
| HIDDEN=150_50 | 0.45 | 0.822 | 45 | 0.60 | 0.844 | 45 | 🟢 +0.022 |
| HIDDEN=200_100_50 | 0.70 | 0.756 | 45 | 0.45 | 0.889 | 45 | 🟢 +0.133 |
| KERNEL=LINEAR | 0.55 | 0.867 | 45 | 0.65 | 0.867 | 45 | ⚪ 0.000 |
| KERNEL=POLY | 0.65 | 0.778 | 45 | 0.65 | 0.778 | 45 | ⚪ 0.000 |
| KERNEL=RBF | 0.65 | 0.778 | 45 | 0.60 | 0.778 | 45 | ⚪ 0.000 |
| MAX_DEPTH=3 | 0.65 | 0.778 | 45 | 0.50 | 0.800 | 45 | 🟢 +0.022 |
| MAX_DEPTH=6 | 0.70 | 0.756 | 45 | 0.50 | 0.822 | 45 | 🟢 +0.067 |
| MAX_DEPTH=9 | 0.70 | 0.778 | 45 | 0.55 | 0.800 | 45 | 🟢 +0.022 |
| N_NEIGHBORS=1 | 0.50 | 0.844 | 45 | 0.55 | 0.867 | 45 | 🟢 +0.022 |
| N_NEIGHBORS=15 | 0.40 | 0.822 | 45 | 0.50 | 0.844 | 45 | 🟢 +0.022 |
| N_NEIGHBORS=7 | 0.45 | 0.844 | 45 | 0.60 | 0.867 | 45 | 🟢 +0.022 |

### Pca L 6

**Comparison on SAME test subjects:**
- Uniform subjects: 65
- Random subjects: 65
- **Intersection (used for comparison): 65 subjects**

| Model×Hyperparameters | Uniform Threshold | Uniform Accuracy | Uniform Subjects | Random Threshold | Random Accuracy | Random Subjects | Accuracy Difference |
|------------------------|-------------------|------------------|-----------------|------------------|-----------------|-----------------|---------------------|
| HIDDEN=100 | 0.70 | 0.600 | 65 | 0.70 | 0.600 | 65 | ⚪ 0.000 |
| HIDDEN=150_50 | 0.70 | 0.600 | 65 | 0.70 | 0.631 | 65 | 🟢 +0.031 |
| HIDDEN=200_100_50 | 0.30 | 0.600 | 65 | 0.65 | 0.631 | 65 | 🟢 +0.031 |
| KERNEL=LINEAR | 0.30 | 0.554 | 65 | 0.70 | 0.569 | 65 | 🟢 +0.015 |
| KERNEL=POLY | 0.30 | 0.554 | 65 | 0.30 | 0.554 | 65 | ⚪ 0.000 |
| KERNEL=RBF | 0.70 | 0.692 | 65 | 0.70 | 0.662 | 65 | 🔴 -0.031 |
| MAX_DEPTH=3 | 0.70 | 0.631 | 65 | 0.70 | 0.615 | 65 | 🔴 -0.015 |
| MAX_DEPTH=6 | 0.70 | 0.615 | 65 | 0.70 | 0.677 | 65 | 🟢 +0.062 |
| MAX_DEPTH=9 | 0.70 | 0.631 | 65 | 0.70 | 0.646 | 65 | 🟢 +0.015 |
| N_NEIGHBORS=1 | 0.45 | 0.492 | 65 | 0.30 | 0.446 | 65 | 🔴 -0.046 |
| N_NEIGHBORS=15 | 0.30 | 0.615 | 65 | 0.35 | 0.662 | 65 | 🟢 +0.046 |
| N_NEIGHBORS=7 | 0.35 | 0.631 | 65 | 0.35 | 0.692 | 65 | 🟢 +0.062 |


## 📊 Detailed Results by Experiment and Model×Hyperparameter

## grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform (uniform)

**Fold Strategy**: UNIFORM
**Common subjects (used for all models)**: 45
Subject IDs: [np.int32(1), np.int32(2), np.int32(5), np.int32(10), np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(17), np.int32(20), np.int32(21), np.int32(24), np.int32(25), np.int32(26), np.int32(27), np.int32(28), np.int32(29), np.int32(30), np.int32(32), np.int32(33), np.int32(34), np.int32(35), np.int32(36), np.int32(37), np.int32(38), np.int32(41), np.int32(43), np.int32(44), np.int32(45), np.int32(46), np.int32(47), np.int32(48), np.int32(49), np.int32(52), np.int32(53), np.int32(55), np.int32(56), np.int32(57), np.int32(58), np.int32(59), np.int32(60), np.int32(61), np.int32(62), np.int32(64), np.int32(65)]

### ANOVA

#### ANOVA (hidden=100)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 32 | 13 | 34 | 22 | 12 | 11 | 0.756 |
| 0.55 ⭐ | 45 | 23 | 22 | 29 | 16 | 37 | 22 | 15 | 8 | 0.822 |
| 0.60 | 45 | 23 | 22 | 26 | 19 | 36 | 20 | 16 | 9 | 0.800 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 29 (64.4%)
- **Predicted as Control**: 16 (35.6%)
- **Correctly Classified**: 37 out of 45 (82.2%)
  - Correct AD: 22 out of 23 (95.7%)
  - Correct Control: 15 out of 22 (68.2%)
- **Incorrectly Classified**: 8 (17.8%)
  - AD → Control: 1
  - Control → AD: 7

---

#### ANOVA (hidden=150_50)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 45 | 23 | 22 | 27 | 18 | 37 | 21 | 16 | 8 | 0.822 |
| 0.50 | 45 | 23 | 22 | 25 | 20 | 35 | 19 | 16 | 10 | 0.778 |
| 0.55 | 45 | 23 | 22 | 21 | 24 | 35 | 17 | 18 | 10 | 0.778 |
| 0.60 | 45 | 23 | 22 | 20 | 25 | 34 | 16 | 18 | 11 | 0.756 |

**Detailed Breakdown at Optimal Threshold (0.45):**

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

#### ANOVA (hidden=200_100_50)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 24 | 21 | 32 | 17 | 15 | 13 | 0.711 |
| 0.55 | 45 | 23 | 22 | 20 | 25 | 32 | 15 | 17 | 13 | 0.711 |
| 0.60 | 45 | 23 | 22 | 19 | 26 | 33 | 15 | 18 | 12 | 0.733 |
| 0.70 ⭐ | 45 | 23 | 22 | 18 | 27 | 34 | 15 | 19 | 11 | 0.756 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 18 (40.0%)
- **Predicted as Control**: 27 (60.0%)
- **Correctly Classified**: 34 out of 45 (75.6%)
  - Correct AD: 15 out of 23 (65.2%)
  - Correct Control: 19 out of 22 (86.4%)
- **Incorrectly Classified**: 11 (24.4%)
  - AD → Control: 8
  - Control → AD: 3

---

#### ANOVA (kernel=linear)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 30 | 15 | 36 | 22 | 14 | 9 | 0.800 |
| 0.55 ⭐ | 45 | 23 | 22 | 27 | 18 | 39 | 22 | 17 | 6 | 0.867 |
| 0.60 | 45 | 23 | 22 | 27 | 18 | 39 | 22 | 17 | 6 | 0.867 |

**Detailed Breakdown at Optimal Threshold (0.55):**

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

#### ANOVA (kernel=poly)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 35 | 10 | 31 | 22 | 9 | 14 | 0.689 |
| 0.55 | 45 | 23 | 22 | 33 | 12 | 33 | 22 | 11 | 12 | 0.733 |
| 0.60 | 45 | 23 | 22 | 31 | 14 | 33 | 21 | 12 | 12 | 0.733 |
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

#### ANOVA (kernel=rbf)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 35 | 10 | 31 | 22 | 9 | 14 | 0.689 |
| 0.55 | 45 | 23 | 22 | 33 | 12 | 33 | 22 | 11 | 12 | 0.733 |
| 0.60 | 45 | 23 | 22 | 32 | 13 | 34 | 22 | 12 | 11 | 0.756 |
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

#### ANOVA (max_depth=3)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 27 | 18 | 33 | 19 | 14 | 12 | 0.733 |
| 0.55 | 45 | 23 | 22 | 27 | 18 | 33 | 19 | 14 | 12 | 0.733 |
| 0.60 | 45 | 23 | 22 | 27 | 18 | 33 | 19 | 14 | 12 | 0.733 |
| 0.65 ⭐ | 45 | 23 | 22 | 23 | 22 | 35 | 18 | 17 | 10 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 23 (51.1%)
- **Predicted as Control**: 22 (48.9%)
- **Correctly Classified**: 35 out of 45 (77.8%)
  - Correct AD: 18 out of 23 (78.3%)
  - Correct Control: 17 out of 22 (77.3%)
- **Incorrectly Classified**: 10 (22.2%)
  - AD → Control: 5
  - Control → AD: 5

---

#### ANOVA (max_depth=6)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 27 | 18 | 33 | 19 | 14 | 12 | 0.733 |
| 0.55 | 45 | 23 | 22 | 25 | 20 | 33 | 18 | 15 | 12 | 0.733 |
| 0.60 | 45 | 23 | 22 | 23 | 22 | 31 | 16 | 15 | 14 | 0.689 |
| 0.70 ⭐ | 45 | 23 | 22 | 20 | 25 | 34 | 16 | 18 | 11 | 0.756 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 20 (44.4%)
- **Predicted as Control**: 25 (55.6%)
- **Correctly Classified**: 34 out of 45 (75.6%)
  - Correct AD: 16 out of 23 (69.6%)
  - Correct Control: 18 out of 22 (81.8%)
- **Incorrectly Classified**: 11 (24.4%)
  - AD → Control: 7
  - Control → AD: 4

---

#### ANOVA (max_depth=9)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 27 | 18 | 33 | 19 | 14 | 12 | 0.733 |
| 0.55 | 45 | 23 | 22 | 25 | 20 | 33 | 18 | 15 | 12 | 0.733 |
| 0.60 | 45 | 23 | 22 | 23 | 22 | 33 | 17 | 16 | 12 | 0.733 |
| 0.70 ⭐ | 45 | 23 | 22 | 19 | 26 | 35 | 16 | 19 | 10 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 19 (42.2%)
- **Predicted as Control**: 26 (57.8%)
- **Correctly Classified**: 35 out of 45 (77.8%)
  - Correct AD: 16 out of 23 (69.6%)
  - Correct Control: 19 out of 22 (86.4%)
- **Incorrectly Classified**: 10 (22.2%)
  - AD → Control: 7
  - Control → AD: 3

---

#### ANOVA (n_neighbors=1)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 45 | 23 | 22 | 26 | 19 | 38 | 21 | 17 | 7 | 0.844 |
| 0.55 | 45 | 23 | 22 | 22 | 23 | 38 | 19 | 19 | 7 | 0.844 |
| 0.60 | 45 | 23 | 22 | 20 | 25 | 38 | 18 | 20 | 7 | 0.844 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 26 (57.8%)
- **Predicted as Control**: 19 (42.2%)
- **Correctly Classified**: 38 out of 45 (84.4%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 17 out of 22 (77.3%)
- **Incorrectly Classified**: 7 (15.6%)
  - AD → Control: 2
  - Control → AD: 5

---

#### ANOVA (n_neighbors=15)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 45 | 23 | 22 | 27 | 18 | 37 | 21 | 16 | 8 | 0.822 |
| 0.50 | 45 | 23 | 22 | 25 | 20 | 37 | 20 | 17 | 8 | 0.822 |
| 0.55 | 45 | 23 | 22 | 24 | 21 | 36 | 19 | 17 | 9 | 0.800 |
| 0.60 | 45 | 23 | 22 | 24 | 21 | 36 | 19 | 17 | 9 | 0.800 |

**Detailed Breakdown at Optimal Threshold (0.40):**

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

#### ANOVA (n_neighbors=7)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 45 | 23 | 22 | 26 | 19 | 38 | 21 | 17 | 7 | 0.844 |
| 0.50 | 45 | 23 | 22 | 25 | 20 | 37 | 20 | 17 | 8 | 0.822 |
| 0.55 | 45 | 23 | 22 | 24 | 21 | 36 | 19 | 17 | 9 | 0.800 |
| 0.60 | 45 | 23 | 22 | 22 | 23 | 38 | 19 | 19 | 7 | 0.844 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 26 (57.8%)
- **Predicted as Control**: 19 (42.2%)
- **Correctly Classified**: 38 out of 45 (84.4%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 17 out of 22 (77.3%)
- **Incorrectly Classified**: 7 (15.6%)
  - AD → Control: 2
  - Control → AD: 5

---

## grid_12_folds_PCA_L_6_C-3_uniform (uniform)

**Fold Strategy**: UNIFORM
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

## grid_50_random_folds_Anova_L_2_incomplete_random (random)

**Fold Strategy**: RANDOM
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

## grid_50_random_folds_Anova_L_6_Incomplete_random (random)

**Fold Strategy**: RANDOM
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

## grid_50_random_folds_PCA_L_2_random (random)

**Fold Strategy**: RANDOM
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

## grid_50_random_folds_PCA_L_6_random (random)

**Fold Strategy**: RANDOM
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

| Experiment | Fold Type | Model×Hyperparameters | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |
|------------|-----------|------------------------|-------------------|----------------|---------|-----------|----------|
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_hidden=100 | 0.55 | 45 | 37 | 8 | 0.822 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_hidden=150_50 | 0.45 | 45 | 37 | 8 | 0.822 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_hidden=200_100_50 | 0.70 | 45 | 34 | 11 | 0.756 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_kernel=linear | 0.55 | 45 | 39 | 6 | 0.867 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_kernel=poly | 0.65 | 45 | 35 | 10 | 0.778 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_kernel=rbf | 0.65 | 45 | 35 | 10 | 0.778 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_max_depth=3 | 0.65 | 45 | 35 | 10 | 0.778 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_max_depth=6 | 0.70 | 45 | 34 | 11 | 0.756 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_max_depth=9 | 0.70 | 45 | 35 | 10 | 0.778 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_n_neighbors=1 | 0.50 | 45 | 38 | 7 | 0.844 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_n_neighbors=15 | 0.40 | 45 | 37 | 8 | 0.822 |
| grid_12_folds_ANOVA_L_6_C_Resource_Boosted_uniform | uniform | ANOVA_n_neighbors=7 | 0.45 | 45 | 38 | 7 | 0.844 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_hidden=100 | 0.70 | 65 | 39 | 26 | 0.600 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_hidden=150_50 | 0.70 | 65 | 39 | 26 | 0.600 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_hidden=200_100_50 | 0.30 | 65 | 39 | 26 | 0.600 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_kernel=linear | 0.30 | 65 | 36 | 29 | 0.554 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_kernel=poly | 0.30 | 65 | 36 | 29 | 0.554 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_kernel=rbf | 0.70 | 65 | 45 | 20 | 0.692 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_max_depth=3 | 0.70 | 65 | 41 | 24 | 0.631 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_max_depth=6 | 0.70 | 65 | 40 | 25 | 0.615 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_max_depth=9 | 0.70 | 65 | 41 | 24 | 0.631 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_n_neighbors=1 | 0.45 | 65 | 32 | 33 | 0.492 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_n_neighbors=15 | 0.30 | 65 | 40 | 25 | 0.615 |
| grid_12_folds_PCA_L_6_C-3_uniform | uniform | PCA_n_neighbors=7 | 0.35 | 65 | 41 | 24 | 0.631 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_hidden=100 | 0.65 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_hidden=150_50 | 0.55 | 17 | 14 | 3 | 0.824 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_hidden=200_100_50 | 0.65 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_kernel=linear | 0.70 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_kernel=poly | 0.55 | 17 | 13 | 4 | 0.765 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_kernel=rbf | 0.60 | 17 | 13 | 4 | 0.765 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_max_depth=3 | 0.55 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_max_depth=6 | 0.55 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_max_depth=9 | 0.55 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_n_neighbors=1 | 0.40 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_n_neighbors=15 | 0.40 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_2_incomplete_random | random | Anova_n_neighbors=7 | 0.40 | 17 | 15 | 2 | 0.882 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_hidden=100 | 0.55 | 45 | 40 | 5 | 0.889 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_hidden=150_50 | 0.60 | 45 | 38 | 7 | 0.844 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_hidden=200_100_50 | 0.45 | 45 | 40 | 5 | 0.889 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_kernel=linear | 0.65 | 45 | 39 | 6 | 0.867 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_kernel=poly | 0.65 | 45 | 35 | 10 | 0.778 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_kernel=rbf | 0.60 | 45 | 35 | 10 | 0.778 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_max_depth=3 | 0.50 | 45 | 36 | 9 | 0.800 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_max_depth=6 | 0.50 | 45 | 37 | 8 | 0.822 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_max_depth=9 | 0.55 | 45 | 36 | 9 | 0.800 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_n_neighbors=1 | 0.55 | 45 | 39 | 6 | 0.867 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_n_neighbors=15 | 0.50 | 45 | 38 | 7 | 0.844 |
| grid_50_random_folds_Anova_L_6_Incomplete_random | random | Anova_n_neighbors=7 | 0.60 | 45 | 39 | 6 | 0.867 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_hidden=100 | 0.70 | 49 | 27 | 22 | 0.551 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_hidden=150_50 | 0.70 | 49 | 29 | 20 | 0.592 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_hidden=200_100_50 | 0.60 | 49 | 27 | 22 | 0.551 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_kernel=linear | 0.60 | 49 | 26 | 23 | 0.531 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_kernel=poly | 0.30 | 49 | 25 | 24 | 0.510 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_kernel=rbf | 0.70 | 49 | 33 | 16 | 0.673 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_max_depth=3 | 0.70 | 49 | 29 | 20 | 0.592 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_max_depth=6 | 0.65 | 49 | 29 | 20 | 0.592 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_max_depth=9 | 0.30 | 49 | 27 | 22 | 0.551 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_n_neighbors=1 | 0.30 | 49 | 24 | 25 | 0.490 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_n_neighbors=15 | 0.35 | 49 | 32 | 17 | 0.653 |
| grid_50_random_folds_PCA_L_2_random | random | PCA_n_neighbors=7 | 0.30 | 49 | 33 | 16 | 0.673 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_hidden=100 | 0.70 | 65 | 39 | 26 | 0.600 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_hidden=150_50 | 0.70 | 65 | 41 | 24 | 0.631 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_hidden=200_100_50 | 0.65 | 65 | 41 | 24 | 0.631 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_kernel=linear | 0.70 | 65 | 37 | 28 | 0.569 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_kernel=poly | 0.30 | 65 | 36 | 29 | 0.554 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_kernel=rbf | 0.70 | 65 | 43 | 22 | 0.662 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_max_depth=3 | 0.70 | 65 | 40 | 25 | 0.615 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_max_depth=6 | 0.70 | 65 | 44 | 21 | 0.677 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_max_depth=9 | 0.70 | 65 | 42 | 23 | 0.646 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_n_neighbors=1 | 0.30 | 65 | 29 | 36 | 0.446 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_n_neighbors=15 | 0.35 | 65 | 43 | 22 | 0.662 |
| grid_50_random_folds_PCA_L_6_random | random | PCA_n_neighbors=7 | 0.35 | 65 | 45 | 20 | 0.692 |

## 🎯 KNN-Specific Summary (All Experiments)


## ✅ Analysis Verification

- **Total experiments analyzed**: 6
- **Total model×HP×experiment combinations**: 72
- **All parquet files processed** (no sampling)
- **Each experiment analyzed independently**
- **Fair comparison**: Only subjects present in ALL model×hp combinations within each experiment

---
*Analysis completed: 2025-12-12 22:01*
*Only ANOVA/PCA L_6 and L_2 experiments analyzed*
*ALL subjects across these experiments - no sampling*
*Each experiment treated independently*
*Fair comparison: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)*
