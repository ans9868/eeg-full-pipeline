# 🎯 Comprehensive All-Subjects Threshold Analysis

## Analysis Overview

**Key Features**:
- **ALL subjects** across ALL experiments analyzed (no sampling)
- Each experiment treated **independently**
- Per model×hyperparameter×experiment threshold optimization
- **Fair comparison**: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)

## 📊 Subject Coverage by Experiment

### ANOVA_L_2
- Model×HP combinations analyzed: 12
- **Common subjects (used for all models)**: 17
- Subject IDs: [np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(16), np.int32(17), np.int32(18), np.int32(39), np.int32(41), np.int32(42), np.int32(44), np.int32(51), np.int32(54), np.int32(58), np.int32(59), np.int32(61), np.int32(62)]

### ANOVA_L_6
- Model×HP combinations analyzed: 12
- **Common subjects (used for all models)**: 45
- Subject IDs: [np.int32(1), np.int32(2), np.int32(5), np.int32(10), np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(17), np.int32(20), np.int32(21), np.int32(24), np.int32(25), np.int32(26), np.int32(27), np.int32(28), np.int32(29), np.int32(30), np.int32(32), np.int32(33), np.int32(34), np.int32(35), np.int32(36), np.int32(37), np.int32(38), np.int32(41), np.int32(43), np.int32(44), np.int32(45), np.int32(46), np.int32(47), np.int32(48), np.int32(49), np.int32(52), np.int32(53), np.int32(55), np.int32(56), np.int32(57), np.int32(58), np.int32(59), np.int32(60), np.int32(61), np.int32(62), np.int32(64), np.int32(65)]

### PCA_L_2
- Model×HP combinations analyzed: 12
- **Common subjects (used for all models)**: 49
- Subject IDs: [np.int32(1), np.int32(2), np.int32(3), np.int32(4), np.int32(5), np.int32(6), np.int32(7), np.int32(8), np.int32(11), np.int32(13), np.int32(14), np.int32(15), np.int32(16), np.int32(17), np.int32(18), np.int32(19), np.int32(21), np.int32(22), np.int32(23), np.int32(24), np.int32(28), np.int32(30), np.int32(33), np.int32(35), np.int32(36), np.int32(37), np.int32(38), np.int32(39), np.int32(40), np.int32(41), np.int32(42), np.int32(44), np.int32(47), np.int32(48), np.int32(49), np.int32(50), np.int32(51), np.int32(54), np.int32(55), np.int32(56), np.int32(57), np.int32(58), np.int32(59), np.int32(60), np.int32(61), np.int32(62), np.int32(63), np.int32(64), np.int32(65)]

### PCA_L_6
- Model×HP combinations analyzed: 12
- **Common subjects (used for all models)**: 65


**Total Analysis Points**: 432

## 📊 Results by Experiment and Model×Hyperparameter

## ANOVA_L_2

### KNN

#### KNN (n_neighbors=1)

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

#### KNN (n_neighbors=15)

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

#### KNN (n_neighbors=7)

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

### MLP

#### MLP (hidden=100)

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

#### MLP (hidden=150_50)

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

#### MLP (hidden=200_100_50)

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

### SVM

#### SVM (kernel=linear)

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

#### SVM (kernel=poly)

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

#### SVM (kernel=rbf)

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

### XGBoost

#### XGBoost (max_depth=3)

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

#### XGBoost (max_depth=6)

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

#### XGBoost (max_depth=9)

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

## ANOVA_L_6

### KNN

#### KNN (n_neighbors=1)

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

#### KNN (n_neighbors=15)

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

#### KNN (n_neighbors=7)

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

### MLP

#### MLP (hidden=100)

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

#### MLP (hidden=150_50)

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

#### MLP (hidden=200_100_50)

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

### SVM

#### SVM (kernel=linear)

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

#### SVM (kernel=poly)

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

#### SVM (kernel=rbf)

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

### XGBoost

#### XGBoost (max_depth=3)

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

#### XGBoost (max_depth=6)

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

#### XGBoost (max_depth=9)

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

## PCA_L_2

### KNN

#### KNN (n_neighbors=1)

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

#### KNN (n_neighbors=15)

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

#### KNN (n_neighbors=7)

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

### MLP

#### MLP (hidden=100)

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

#### MLP (hidden=150_50)

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

#### MLP (hidden=200_100_50)

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

### SVM

#### SVM (kernel=linear)

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

#### SVM (kernel=poly)

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

#### SVM (kernel=rbf)

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

### XGBoost

#### XGBoost (max_depth=3)

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

#### XGBoost (max_depth=6)

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

#### XGBoost (max_depth=9)

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

## PCA_L_6

### KNN

#### KNN (n_neighbors=1)

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

#### KNN (n_neighbors=15)

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

#### KNN (n_neighbors=7)

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

### MLP

#### MLP (hidden=100)

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

#### MLP (hidden=150_50)

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

#### MLP (hidden=200_100_50)

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

### SVM

#### SVM (kernel=linear)

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

#### SVM (kernel=poly)

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

#### SVM (kernel=rbf)

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

### XGBoost

#### XGBoost (max_depth=3)

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

#### XGBoost (max_depth=6)

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

#### XGBoost (max_depth=9)

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

## 📋 Summary: Optimal Thresholds by Model×Hyperparameter×Experiment

| Experiment | Model×Hyperparameters | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |
|------------|------------------------|-------------------|----------------|---------|-----------|----------|
| ANOVA_L_2 | KNN_n_neighbors=1 | 0.40 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | KNN_n_neighbors=15 | 0.40 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | KNN_n_neighbors=7 | 0.40 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | MLP_hidden=100 | 0.65 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | MLP_hidden=150_50 | 0.55 | 17 | 14 | 3 | 0.824 |
| ANOVA_L_2 | MLP_hidden=200_100_50 | 0.65 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | SVM_kernel=linear | 0.70 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | SVM_kernel=poly | 0.55 | 17 | 13 | 4 | 0.765 |
| ANOVA_L_2 | SVM_kernel=rbf | 0.60 | 17 | 13 | 4 | 0.765 |
| ANOVA_L_2 | XGBoost_max_depth=3 | 0.55 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | XGBoost_max_depth=6 | 0.55 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | XGBoost_max_depth=9 | 0.55 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_6 | KNN_n_neighbors=1 | 0.55 | 45 | 39 | 6 | 0.867 |
| ANOVA_L_6 | KNN_n_neighbors=15 | 0.50 | 45 | 38 | 7 | 0.844 |
| ANOVA_L_6 | KNN_n_neighbors=7 | 0.60 | 45 | 39 | 6 | 0.867 |
| ANOVA_L_6 | MLP_hidden=100 | 0.55 | 45 | 40 | 5 | 0.889 |
| ANOVA_L_6 | MLP_hidden=150_50 | 0.60 | 45 | 38 | 7 | 0.844 |
| ANOVA_L_6 | MLP_hidden=200_100_50 | 0.45 | 45 | 40 | 5 | 0.889 |
| ANOVA_L_6 | SVM_kernel=linear | 0.65 | 45 | 39 | 6 | 0.867 |
| ANOVA_L_6 | SVM_kernel=poly | 0.65 | 45 | 35 | 10 | 0.778 |
| ANOVA_L_6 | SVM_kernel=rbf | 0.60 | 45 | 35 | 10 | 0.778 |
| ANOVA_L_6 | XGBoost_max_depth=3 | 0.50 | 45 | 36 | 9 | 0.800 |
| ANOVA_L_6 | XGBoost_max_depth=6 | 0.50 | 45 | 37 | 8 | 0.822 |
| ANOVA_L_6 | XGBoost_max_depth=9 | 0.55 | 45 | 36 | 9 | 0.800 |
| PCA_L_2 | KNN_n_neighbors=1 | 0.30 | 49 | 24 | 25 | 0.490 |
| PCA_L_2 | KNN_n_neighbors=15 | 0.35 | 49 | 32 | 17 | 0.653 |
| PCA_L_2 | KNN_n_neighbors=7 | 0.30 | 49 | 33 | 16 | 0.673 |
| PCA_L_2 | MLP_hidden=100 | 0.70 | 49 | 27 | 22 | 0.551 |
| PCA_L_2 | MLP_hidden=150_50 | 0.70 | 49 | 29 | 20 | 0.592 |
| PCA_L_2 | MLP_hidden=200_100_50 | 0.60 | 49 | 27 | 22 | 0.551 |
| PCA_L_2 | SVM_kernel=linear | 0.60 | 49 | 26 | 23 | 0.531 |
| PCA_L_2 | SVM_kernel=poly | 0.30 | 49 | 25 | 24 | 0.510 |
| PCA_L_2 | SVM_kernel=rbf | 0.70 | 49 | 33 | 16 | 0.673 |
| PCA_L_2 | XGBoost_max_depth=3 | 0.70 | 49 | 29 | 20 | 0.592 |
| PCA_L_2 | XGBoost_max_depth=6 | 0.65 | 49 | 29 | 20 | 0.592 |
| PCA_L_2 | XGBoost_max_depth=9 | 0.30 | 49 | 27 | 22 | 0.551 |
| PCA_L_6 | KNN_n_neighbors=1 | 0.30 | 65 | 29 | 36 | 0.446 |
| PCA_L_6 | KNN_n_neighbors=15 | 0.35 | 65 | 43 | 22 | 0.662 |
| PCA_L_6 | KNN_n_neighbors=7 | 0.35 | 65 | 45 | 20 | 0.692 |
| PCA_L_6 | MLP_hidden=100 | 0.70 | 65 | 39 | 26 | 0.600 |
| PCA_L_6 | MLP_hidden=150_50 | 0.70 | 65 | 41 | 24 | 0.631 |
| PCA_L_6 | MLP_hidden=200_100_50 | 0.65 | 65 | 41 | 24 | 0.631 |
| PCA_L_6 | SVM_kernel=linear | 0.70 | 65 | 37 | 28 | 0.569 |
| PCA_L_6 | SVM_kernel=poly | 0.30 | 65 | 36 | 29 | 0.554 |
| PCA_L_6 | SVM_kernel=rbf | 0.70 | 65 | 43 | 22 | 0.662 |
| PCA_L_6 | XGBoost_max_depth=3 | 0.70 | 65 | 40 | 25 | 0.615 |
| PCA_L_6 | XGBoost_max_depth=6 | 0.70 | 65 | 44 | 21 | 0.677 |
| PCA_L_6 | XGBoost_max_depth=9 | 0.70 | 65 | 42 | 23 | 0.646 |

## 🎯 KNN-Specific Summary (All Subjects, Per Experiment)

| Experiment | KNN Hyperparameters | Threshold | Total | Correct | Incorrect | Accuracy |
|------------|---------------------|-----------|-------|---------|-----------|----------|
| ANOVA_L_2 | n_neighbors=1 | 0.40 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | n_neighbors=15 | 0.40 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_2 | n_neighbors=7 | 0.40 | 17 | 15 | 2 | 0.882 |
| ANOVA_L_6 | n_neighbors=1 | 0.55 | 45 | 39 | 6 | 0.867 |
| ANOVA_L_6 | n_neighbors=15 | 0.50 | 45 | 38 | 7 | 0.844 |
| ANOVA_L_6 | n_neighbors=7 | 0.60 | 45 | 39 | 6 | 0.867 |
| PCA_L_2 | n_neighbors=1 | 0.30 | 49 | 24 | 25 | 0.490 |
| PCA_L_2 | n_neighbors=15 | 0.35 | 49 | 32 | 17 | 0.653 |
| PCA_L_2 | n_neighbors=7 | 0.30 | 49 | 33 | 16 | 0.673 |
| PCA_L_6 | n_neighbors=1 | 0.30 | 65 | 29 | 36 | 0.446 |
| PCA_L_6 | n_neighbors=15 | 0.35 | 65 | 43 | 22 | 0.662 |
| PCA_L_6 | n_neighbors=7 | 0.35 | 65 | 45 | 20 | 0.692 |

## ✅ Subject Coverage Verification

- **Total experiments analyzed**: 4
- **Total model×HP×experiment combinations**: 48
- **All parquet files processed** (no sampling)
- **Each experiment analyzed independently**

---
*Analysis completed: 2025-12-12 21:20*
*ALL subjects across ALL experiments - no sampling*
*Each experiment treated independently*
*Fair comparison: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)*
