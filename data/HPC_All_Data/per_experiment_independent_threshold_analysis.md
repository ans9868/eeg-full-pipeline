# 🎯 Per-Experiment Independent Threshold Analysis

## Analysis Overview

**Key Difference**: Each experiment is treated **independently**. A subject's performance in Experiment 1 is completely separate from their performance in Experiment 2.

**Example**:
- Subject 1 in Experiment 1: 20% accuracy → Incorrectly classified
- Subject 1 in Experiment 2: 91% accuracy → Correctly classified
- Result: Subject 1 is correctly classified **1 out of 2 times** (50%), NOT averaged

**Method**:
1. For each experiment separately
2. For each model×hyperparameter combination
3. Calculate per-subject AD ratio (averaged across folds within that experiment only)
4. Apply threshold to classify subjects
5. Count correct/incorrect classifications
6. Find optimal threshold per model×experiment×hyperparameter

## 📊 Results by Experiment and Model×Hyperparameter

## ANOVA_L_2

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 33 | 17 | 16 | 19 | 14 | 31 | 17 | 14 | 2 | 0.939 |
| 0.55 | 33 | 17 | 16 | 17 | 16 | 29 | 15 | 14 | 4 | 0.879 |
| 0.60 | 33 | 17 | 16 | 15 | 18 | 27 | 13 | 14 | 6 | 0.818 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 33
- **True AD**: 17 | **True Control**: 16
- **Predicted as AD**: 19 (57.6%)
- **Predicted as Control**: 14 (42.4%)
- **Correctly Classified**: 31 out of 33 (93.9%)
  - Correct AD: 17 out of 17 (100.0%)
  - Correct Control: 14 out of 16 (87.5%)
- **Incorrectly Classified**: 2 (6.1%)
  - AD → Control: 0
  - Control → AD: 2

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 15 | 7 | 8 | 9 | 6 | 13 | 7 | 6 | 2 | 0.867 |
| 0.50 | 15 | 7 | 8 | 8 | 7 | 12 | 6 | 6 | 3 | 0.800 |
| 0.55 | 15 | 7 | 8 | 8 | 7 | 12 | 6 | 6 | 3 | 0.800 |
| 0.60 | 15 | 7 | 8 | 7 | 8 | 11 | 5 | 6 | 4 | 0.733 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 15
- **True AD**: 7 | **True Control**: 8
- **Predicted as AD**: 9 (60.0%)
- **Predicted as Control**: 6 (40.0%)
- **Correctly Classified**: 13 out of 15 (86.7%)
  - Correct AD: 7 out of 7 (100.0%)
  - Correct Control: 6 out of 8 (75.0%)
- **Incorrectly Classified**: 2 (13.3%)
  - AD → Control: 0
  - Control → AD: 2

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 36 | 18 | 18 | 19 | 17 | 33 | 17 | 16 | 3 | 0.917 |
| 0.55 | 36 | 18 | 18 | 18 | 18 | 32 | 16 | 16 | 4 | 0.889 |
| 0.60 | 36 | 18 | 18 | 17 | 19 | 31 | 15 | 16 | 5 | 0.861 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 36
- **True AD**: 18 | **True Control**: 18
- **Predicted as AD**: 19 (52.8%)
- **Predicted as Control**: 17 (47.2%)
- **Correctly Classified**: 33 out of 36 (91.7%)
  - Correct AD: 17 out of 18 (94.4%)
  - Correct Control: 16 out of 18 (88.9%)
- **Incorrectly Classified**: 3 (8.3%)
  - AD → Control: 1
  - Control → AD: 2

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 30 | 16 | 14 | 19 | 11 | 25 | 15 | 10 | 5 | 0.833 |
| 0.55 | 30 | 16 | 14 | 18 | 12 | 26 | 15 | 11 | 4 | 0.867 |
| 0.60 ⭐ | 30 | 16 | 14 | 17 | 13 | 27 | 15 | 12 | 3 | 0.900 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 30
- **True AD**: 16 | **True Control**: 14
- **Predicted as AD**: 17 (56.7%)
- **Predicted as Control**: 13 (43.3%)
- **Correctly Classified**: 27 out of 30 (90.0%)
  - Correct AD: 15 out of 16 (93.8%)
  - Correct Control: 12 out of 14 (85.7%)
- **Incorrectly Classified**: 3 (10.0%)
  - AD → Control: 1
  - Control → AD: 2

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 19 | 8 | 11 | 10 | 9 | 17 | 8 | 9 | 2 | 0.895 |
| 0.50 | 19 | 8 | 11 | 10 | 9 | 17 | 8 | 9 | 2 | 0.895 |
| 0.55 | 19 | 8 | 11 | 10 | 9 | 17 | 8 | 9 | 2 | 0.895 |
| 0.60 | 19 | 8 | 11 | 10 | 9 | 17 | 8 | 9 | 2 | 0.895 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 19
- **True AD**: 8 | **True Control**: 11
- **Predicted as AD**: 10 (52.6%)
- **Predicted as Control**: 9 (47.4%)
- **Correctly Classified**: 17 out of 19 (89.5%)
  - Correct AD: 8 out of 8 (100.0%)
  - Correct Control: 9 out of 11 (81.8%)
- **Incorrectly Classified**: 2 (10.5%)
  - AD → Control: 0
  - Control → AD: 2

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 9 | 4 | 5 | 6 | 3 | 7 | 4 | 3 | 2 | 0.778 |
| 0.55 | 9 | 4 | 5 | 6 | 3 | 7 | 4 | 3 | 2 | 0.778 |
| 0.60 | 9 | 4 | 5 | 6 | 3 | 7 | 4 | 3 | 2 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 9
- **True AD**: 4 | **True Control**: 5
- **Predicted as AD**: 6 (66.7%)
- **Predicted as Control**: 3 (33.3%)
- **Correctly Classified**: 7 out of 9 (77.8%)
  - Correct AD: 4 out of 4 (100.0%)
  - Correct Control: 3 out of 5 (60.0%)
- **Incorrectly Classified**: 2 (22.2%)
  - AD → Control: 0
  - Control → AD: 2

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 11 | 6 | 5 | 8 | 3 | 9 | 6 | 3 | 2 | 0.818 |
| 0.50 | 11 | 6 | 5 | 8 | 3 | 9 | 6 | 3 | 2 | 0.818 |
| 0.55 | 11 | 6 | 5 | 8 | 3 | 9 | 6 | 3 | 2 | 0.818 |
| 0.60 | 11 | 6 | 5 | 8 | 3 | 9 | 6 | 3 | 2 | 0.818 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 11
- **True AD**: 6 | **True Control**: 5
- **Predicted as AD**: 8 (72.7%)
- **Predicted as Control**: 3 (27.3%)
- **Correctly Classified**: 9 out of 11 (81.8%)
  - Correct AD: 6 out of 6 (100.0%)
  - Correct Control: 3 out of 5 (60.0%)
- **Incorrectly Classified**: 2 (18.2%)
  - AD → Control: 0
  - Control → AD: 2

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 28 | 14 | 14 | 22 | 6 | 18 | 13 | 5 | 10 | 0.643 |
| 0.50 | 28 | 14 | 14 | 22 | 6 | 18 | 13 | 5 | 10 | 0.643 |
| 0.55 | 28 | 14 | 14 | 20 | 8 | 18 | 12 | 6 | 10 | 0.643 |
| 0.60 | 28 | 14 | 14 | 20 | 8 | 18 | 12 | 6 | 10 | 0.643 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 28
- **True AD**: 14 | **True Control**: 14
- **Predicted as AD**: 22 (78.6%)
- **Predicted as Control**: 6 (21.4%)
- **Correctly Classified**: 18 out of 28 (64.3%)
  - Correct AD: 13 out of 14 (92.9%)
  - Correct Control: 5 out of 14 (35.7%)
- **Incorrectly Classified**: 10 (35.7%)
  - AD → Control: 1
  - Control → AD: 9

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 32 | 15 | 17 | 24 | 8 | 23 | 15 | 8 | 9 | 0.719 |
| 0.50 | 32 | 15 | 17 | 23 | 9 | 22 | 14 | 8 | 10 | 0.688 |
| 0.55 | 32 | 15 | 17 | 23 | 9 | 22 | 14 | 8 | 10 | 0.688 |
| 0.60 | 32 | 15 | 17 | 20 | 12 | 23 | 13 | 10 | 9 | 0.719 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 32
- **True AD**: 15 | **True Control**: 17
- **Predicted as AD**: 24 (75.0%)
- **Predicted as Control**: 8 (25.0%)
- **Correctly Classified**: 23 out of 32 (71.9%)
  - Correct AD: 15 out of 15 (100.0%)
  - Correct Control: 8 out of 17 (47.1%)
- **Incorrectly Classified**: 9 (28.1%)
  - AD → Control: 0
  - Control → AD: 9

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 27 | 11 | 16 | 17 | 10 | 21 | 11 | 10 | 6 | 0.778 |
| 0.55 ⭐ | 27 | 11 | 16 | 15 | 12 | 23 | 11 | 12 | 4 | 0.852 |
| 0.60 | 27 | 11 | 16 | 14 | 13 | 22 | 10 | 12 | 5 | 0.815 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 27
- **True AD**: 11 | **True Control**: 16
- **Predicted as AD**: 15 (55.6%)
- **Predicted as Control**: 12 (44.4%)
- **Correctly Classified**: 23 out of 27 (85.2%)
  - Correct AD: 11 out of 11 (100.0%)
  - Correct Control: 12 out of 16 (75.0%)
- **Incorrectly Classified**: 4 (14.8%)
  - AD → Control: 0
  - Control → AD: 4

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 18 | 8 | 10 | 11 | 7 | 15 | 8 | 7 | 3 | 0.833 |
| 0.55 | 18 | 8 | 10 | 11 | 7 | 15 | 8 | 7 | 3 | 0.833 |
| 0.60 | 18 | 8 | 10 | 10 | 8 | 14 | 7 | 7 | 4 | 0.778 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 18
- **True AD**: 8 | **True Control**: 10
- **Predicted as AD**: 11 (61.1%)
- **Predicted as Control**: 7 (38.9%)
- **Correctly Classified**: 15 out of 18 (83.3%)
  - Correct AD: 8 out of 8 (100.0%)
  - Correct Control: 7 out of 10 (70.0%)
- **Incorrectly Classified**: 3 (16.7%)
  - AD → Control: 0
  - Control → AD: 3

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 30 | 15 | 15 | 15 | 15 | 24 | 12 | 12 | 6 | 0.800 |
| 0.55 ⭐ | 30 | 15 | 15 | 13 | 17 | 26 | 12 | 14 | 4 | 0.867 |
| 0.60 | 30 | 15 | 15 | 12 | 18 | 25 | 11 | 14 | 5 | 0.833 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 30
- **True AD**: 15 | **True Control**: 15
- **Predicted as AD**: 13 (43.3%)
- **Predicted as Control**: 17 (56.7%)
- **Correctly Classified**: 26 out of 30 (86.7%)
  - Correct AD: 12 out of 15 (80.0%)
  - Correct Control: 14 out of 15 (93.3%)
- **Incorrectly Classified**: 4 (13.3%)
  - AD → Control: 3
  - Control → AD: 1

---

## ANOVA_L_6

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 50 | 28 | 22 | 28 | 22 | 42 | 24 | 18 | 8 | 0.840 |
| 0.50 | 50 | 28 | 22 | 26 | 24 | 42 | 23 | 19 | 8 | 0.840 |
| 0.55 | 50 | 28 | 22 | 23 | 27 | 41 | 21 | 20 | 9 | 0.820 |
| 0.60 | 50 | 28 | 22 | 18 | 32 | 36 | 16 | 20 | 14 | 0.720 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 50
- **True AD**: 28 | **True Control**: 22
- **Predicted as AD**: 28 (56.0%)
- **Predicted as Control**: 22 (44.0%)
- **Correctly Classified**: 42 out of 50 (84.0%)
  - Correct AD: 24 out of 28 (85.7%)
  - Correct Control: 18 out of 22 (81.8%)
- **Incorrectly Classified**: 8 (16.0%)
  - AD → Control: 4
  - Control → AD: 4

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 49 | 27 | 22 | 26 | 23 | 40 | 22 | 18 | 9 | 0.816 |
| 0.55 | 49 | 27 | 22 | 25 | 24 | 39 | 21 | 18 | 10 | 0.796 |
| 0.60 | 49 | 27 | 22 | 25 | 24 | 39 | 21 | 18 | 10 | 0.796 |
| 0.65 ⭐ | 49 | 27 | 22 | 21 | 28 | 41 | 20 | 21 | 8 | 0.837 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 49
- **True AD**: 27 | **True Control**: 22
- **Predicted as AD**: 21 (42.9%)
- **Predicted as Control**: 28 (57.1%)
- **Correctly Classified**: 41 out of 49 (83.7%)
  - Correct AD: 20 out of 27 (74.1%)
  - Correct Control: 21 out of 22 (95.5%)
- **Incorrectly Classified**: 8 (16.3%)
  - AD → Control: 7
  - Control → AD: 1

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 55 | 29 | 26 | 32 | 23 | 48 | 27 | 21 | 7 | 0.873 |
| 0.55 | 55 | 29 | 26 | 31 | 24 | 47 | 26 | 21 | 8 | 0.855 |
| 0.60 | 55 | 29 | 26 | 30 | 25 | 48 | 26 | 22 | 7 | 0.873 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 55
- **True AD**: 29 | **True Control**: 26
- **Predicted as AD**: 32 (58.2%)
- **Predicted as Control**: 23 (41.8%)
- **Correctly Classified**: 48 out of 55 (87.3%)
  - Correct AD: 27 out of 29 (93.1%)
  - Correct Control: 21 out of 26 (80.8%)
- **Incorrectly Classified**: 7 (12.7%)
  - AD → Control: 2
  - Control → AD: 5

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 61 | 32 | 29 | 35 | 26 | 52 | 29 | 23 | 9 | 0.852 |
| 0.55 | 61 | 32 | 29 | 34 | 27 | 51 | 28 | 23 | 10 | 0.836 |
| 0.60 | 61 | 32 | 29 | 32 | 29 | 49 | 26 | 23 | 12 | 0.803 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 61
- **True AD**: 32 | **True Control**: 29
- **Predicted as AD**: 35 (57.4%)
- **Predicted as Control**: 26 (42.6%)
- **Correctly Classified**: 52 out of 61 (85.2%)
  - Correct AD: 29 out of 32 (90.6%)
  - Correct Control: 23 out of 29 (79.3%)
- **Incorrectly Classified**: 9 (14.8%)
  - AD → Control: 3
  - Control → AD: 6

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 27 | 14 | 13 | 15 | 12 | 22 | 12 | 10 | 5 | 0.815 |
| 0.55 ⭐ | 27 | 14 | 13 | 14 | 13 | 23 | 12 | 11 | 4 | 0.852 |
| 0.60 | 27 | 14 | 13 | 13 | 14 | 22 | 11 | 11 | 5 | 0.815 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 27
- **True AD**: 14 | **True Control**: 13
- **Predicted as AD**: 14 (51.9%)
- **Predicted as Control**: 13 (48.1%)
- **Correctly Classified**: 23 out of 27 (85.2%)
  - Correct AD: 12 out of 14 (85.7%)
  - Correct Control: 11 out of 13 (84.6%)
- **Incorrectly Classified**: 4 (14.8%)
  - AD → Control: 2
  - Control → AD: 2

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 29 | 12 | 17 | 16 | 13 | 25 | 12 | 13 | 4 | 0.862 |
| 0.50 | 29 | 12 | 17 | 15 | 14 | 24 | 11 | 13 | 5 | 0.828 |
| 0.55 | 29 | 12 | 17 | 13 | 16 | 24 | 10 | 14 | 5 | 0.828 |
| 0.60 | 29 | 12 | 17 | 11 | 18 | 24 | 9 | 15 | 5 | 0.828 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 29
- **True AD**: 12 | **True Control**: 17
- **Predicted as AD**: 16 (55.2%)
- **Predicted as Control**: 13 (44.8%)
- **Correctly Classified**: 25 out of 29 (86.2%)
  - Correct AD: 12 out of 12 (100.0%)
  - Correct Control: 13 out of 17 (76.5%)
- **Incorrectly Classified**: 4 (13.8%)
  - AD → Control: 0
  - Control → AD: 4

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 37 | 21 | 16 | 23 | 14 | 33 | 20 | 13 | 4 | 0.892 |
| 0.55 | 37 | 21 | 16 | 23 | 14 | 33 | 20 | 13 | 4 | 0.892 |
| 0.60 | 37 | 21 | 16 | 23 | 14 | 33 | 20 | 13 | 4 | 0.892 |
| 0.70 ⭐ | 37 | 21 | 16 | 21 | 16 | 35 | 20 | 15 | 2 | 0.946 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 37
- **True AD**: 21 | **True Control**: 16
- **Predicted as AD**: 21 (56.8%)
- **Predicted as Control**: 16 (43.2%)
- **Correctly Classified**: 35 out of 37 (94.6%)
  - Correct AD: 20 out of 21 (95.2%)
  - Correct Control: 15 out of 16 (93.8%)
- **Incorrectly Classified**: 2 (5.4%)
  - AD → Control: 1
  - Control → AD: 1

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 56 | 32 | 24 | 44 | 12 | 40 | 30 | 10 | 16 | 0.714 |
| 0.55 | 56 | 32 | 24 | 42 | 14 | 40 | 29 | 11 | 16 | 0.714 |
| 0.60 | 56 | 32 | 24 | 38 | 18 | 42 | 28 | 14 | 14 | 0.750 |
| 0.65 ⭐ | 56 | 32 | 24 | 37 | 19 | 43 | 28 | 15 | 13 | 0.768 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 56
- **True AD**: 32 | **True Control**: 24
- **Predicted as AD**: 37 (66.1%)
- **Predicted as Control**: 19 (33.9%)
- **Correctly Classified**: 43 out of 56 (76.8%)
  - Correct AD: 28 out of 32 (87.5%)
  - Correct Control: 15 out of 24 (62.5%)
- **Incorrectly Classified**: 13 (23.2%)
  - AD → Control: 4
  - Control → AD: 9

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 54 | 29 | 25 | 42 | 12 | 39 | 28 | 11 | 15 | 0.722 |
| 0.55 | 54 | 29 | 25 | 41 | 13 | 40 | 28 | 12 | 14 | 0.741 |
| 0.60 ⭐ | 54 | 29 | 25 | 38 | 16 | 43 | 28 | 15 | 11 | 0.796 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 54
- **True AD**: 29 | **True Control**: 25
- **Predicted as AD**: 38 (70.4%)
- **Predicted as Control**: 16 (29.6%)
- **Correctly Classified**: 43 out of 54 (79.6%)
  - Correct AD: 28 out of 29 (96.6%)
  - Correct Control: 15 out of 25 (60.0%)
- **Incorrectly Classified**: 11 (20.4%)
  - AD → Control: 1
  - Control → AD: 10

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 54 | 27 | 27 | 32 | 22 | 43 | 24 | 19 | 11 | 0.796 |
| 0.55 | 54 | 27 | 27 | 30 | 24 | 41 | 22 | 19 | 13 | 0.759 |
| 0.60 | 54 | 27 | 27 | 26 | 28 | 41 | 20 | 21 | 13 | 0.759 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 54
- **True AD**: 27 | **True Control**: 27
- **Predicted as AD**: 32 (59.3%)
- **Predicted as Control**: 22 (40.7%)
- **Correctly Classified**: 43 out of 54 (79.6%)
  - Correct AD: 24 out of 27 (88.9%)
  - Correct Control: 19 out of 27 (70.4%)
- **Incorrectly Classified**: 11 (20.4%)
  - AD → Control: 3
  - Control → AD: 8

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 57 | 32 | 25 | 38 | 19 | 45 | 29 | 16 | 12 | 0.789 |
| 0.55 | 57 | 32 | 25 | 34 | 23 | 43 | 26 | 17 | 14 | 0.754 |
| 0.60 | 57 | 32 | 25 | 30 | 27 | 45 | 25 | 20 | 12 | 0.789 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 57
- **True AD**: 32 | **True Control**: 25
- **Predicted as AD**: 38 (66.7%)
- **Predicted as Control**: 19 (33.3%)
- **Correctly Classified**: 45 out of 57 (78.9%)
  - Correct AD: 29 out of 32 (90.6%)
  - Correct Control: 16 out of 25 (64.0%)
- **Incorrectly Classified**: 12 (21.1%)
  - AD → Control: 3
  - Control → AD: 9

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 54 | 30 | 24 | 30 | 24 | 44 | 25 | 19 | 10 | 0.815 |
| 0.55 | 54 | 30 | 24 | 29 | 25 | 43 | 24 | 19 | 11 | 0.796 |
| 0.60 | 54 | 30 | 24 | 27 | 27 | 43 | 23 | 20 | 11 | 0.796 |
| 0.70 ⭐ | 54 | 30 | 24 | 22 | 32 | 46 | 22 | 24 | 8 | 0.852 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 54
- **True AD**: 30 | **True Control**: 24
- **Predicted as AD**: 22 (40.7%)
- **Predicted as Control**: 32 (59.3%)
- **Correctly Classified**: 46 out of 54 (85.2%)
  - Correct AD: 22 out of 30 (73.3%)
  - Correct Control: 24 out of 24 (100.0%)
- **Incorrectly Classified**: 8 (14.8%)
  - AD → Control: 8
  - Control → AD: 0

---

## PCA_L_2

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 20 | 10 | 10 | 0 | 20 | 10 | 0 | 10 | 10 | 0.500 |
| 0.50 | 20 | 10 | 10 | 0 | 20 | 10 | 0 | 10 | 10 | 0.500 |
| 0.55 | 20 | 10 | 10 | 0 | 20 | 10 | 0 | 10 | 10 | 0.500 |
| 0.60 | 20 | 10 | 10 | 0 | 20 | 10 | 0 | 10 | 10 | 0.500 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 20
- **True AD**: 10 | **True Control**: 10
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 20 (100.0%)
- **Correctly Classified**: 10 out of 20 (50.0%)
  - Correct AD: 0 out of 10 (0.0%)
  - Correct Control: 10 out of 10 (100.0%)
- **Incorrectly Classified**: 10 (50.0%)
  - AD → Control: 10
  - Control → AD: 0

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.35**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.35 ⭐ | 22 | 10 | 12 | 4 | 18 | 16 | 4 | 12 | 6 | 0.727 |
| 0.50 | 22 | 10 | 12 | 1 | 21 | 13 | 1 | 12 | 9 | 0.591 |
| 0.55 | 22 | 10 | 12 | 0 | 22 | 12 | 0 | 12 | 10 | 0.545 |
| 0.60 | 22 | 10 | 12 | 0 | 22 | 12 | 0 | 12 | 10 | 0.545 |

**Detailed Breakdown at Optimal Threshold (0.35):**

- **Total Subjects**: 22
- **True AD**: 10 | **True Control**: 12
- **Predicted as AD**: 4 (18.2%)
- **Predicted as Control**: 18 (81.8%)
- **Correctly Classified**: 16 out of 22 (72.7%)
  - Correct AD: 4 out of 10 (40.0%)
  - Correct Control: 12 out of 12 (100.0%)
- **Incorrectly Classified**: 6 (27.3%)
  - AD → Control: 6
  - Control → AD: 0

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 23 | 12 | 11 | 8 | 15 | 17 | 7 | 10 | 6 | 0.739 |
| 0.50 | 23 | 12 | 11 | 0 | 23 | 11 | 0 | 11 | 12 | 0.478 |
| 0.55 | 23 | 12 | 11 | 0 | 23 | 11 | 0 | 11 | 12 | 0.478 |
| 0.60 | 23 | 12 | 11 | 0 | 23 | 11 | 0 | 11 | 12 | 0.478 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 23
- **True AD**: 12 | **True Control**: 11
- **Predicted as AD**: 8 (34.8%)
- **Predicted as Control**: 15 (65.2%)
- **Correctly Classified**: 17 out of 23 (73.9%)
  - Correct AD: 7 out of 12 (58.3%)
  - Correct Control: 10 out of 11 (90.9%)
- **Incorrectly Classified**: 6 (26.1%)
  - AD → Control: 5
  - Control → AD: 1

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 27 | 14 | 13 | 27 | 0 | 14 | 14 | 0 | 13 | 0.519 |
| 0.55 | 27 | 14 | 13 | 27 | 0 | 14 | 14 | 0 | 13 | 0.519 |
| 0.60 | 27 | 14 | 13 | 27 | 0 | 14 | 14 | 0 | 13 | 0.519 |
| 0.65 ⭐ | 27 | 14 | 13 | 26 | 1 | 15 | 14 | 1 | 12 | 0.556 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 27
- **True AD**: 14 | **True Control**: 13
- **Predicted as AD**: 26 (96.3%)
- **Predicted as Control**: 1 (3.7%)
- **Correctly Classified**: 15 out of 27 (55.6%)
  - Correct AD: 14 out of 14 (100.0%)
  - Correct Control: 1 out of 13 (7.7%)
- **Incorrectly Classified**: 12 (44.4%)
  - AD → Control: 0
  - Control → AD: 12

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 28 | 13 | 15 | 26 | 2 | 15 | 13 | 2 | 13 | 0.536 |
| 0.55 | 28 | 13 | 15 | 26 | 2 | 15 | 13 | 2 | 13 | 0.536 |
| 0.60 | 28 | 13 | 15 | 26 | 2 | 15 | 13 | 2 | 13 | 0.536 |
| 0.65 ⭐ | 28 | 13 | 15 | 25 | 3 | 16 | 13 | 3 | 12 | 0.571 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 28
- **True AD**: 13 | **True Control**: 15
- **Predicted as AD**: 25 (89.3%)
- **Predicted as Control**: 3 (10.7%)
- **Correctly Classified**: 16 out of 28 (57.1%)
  - Correct AD: 13 out of 13 (100.0%)
  - Correct Control: 3 out of 15 (20.0%)
- **Incorrectly Classified**: 12 (42.9%)
  - AD → Control: 0
  - Control → AD: 12

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 26 | 14 | 12 | 26 | 0 | 14 | 14 | 0 | 12 | 0.538 |
| 0.55 | 26 | 14 | 12 | 26 | 0 | 14 | 14 | 0 | 12 | 0.538 |
| 0.60 | 26 | 14 | 12 | 25 | 1 | 15 | 14 | 1 | 11 | 0.577 |
| 0.65 ⭐ | 26 | 14 | 12 | 24 | 2 | 16 | 14 | 2 | 10 | 0.615 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 26
- **True AD**: 14 | **True Control**: 12
- **Predicted as AD**: 24 (92.3%)
- **Predicted as Control**: 2 (7.7%)
- **Correctly Classified**: 16 out of 26 (61.5%)
  - Correct AD: 14 out of 14 (100.0%)
  - Correct Control: 2 out of 12 (16.7%)
- **Incorrectly Classified**: 10 (38.5%)
  - AD → Control: 0
  - Control → AD: 10

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 25 | 13 | 12 | 25 | 0 | 13 | 13 | 0 | 12 | 0.520 |
| 0.55 | 25 | 13 | 12 | 25 | 0 | 13 | 13 | 0 | 12 | 0.520 |
| 0.60 ⭐ | 25 | 13 | 12 | 24 | 1 | 14 | 13 | 1 | 11 | 0.560 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 25
- **True AD**: 13 | **True Control**: 12
- **Predicted as AD**: 24 (96.0%)
- **Predicted as Control**: 1 (4.0%)
- **Correctly Classified**: 14 out of 25 (56.0%)
  - Correct AD: 13 out of 13 (100.0%)
  - Correct Control: 1 out of 12 (8.3%)
- **Incorrectly Classified**: 11 (44.0%)
  - AD → Control: 0
  - Control → AD: 11

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 29 | 14 | 15 | 29 | 0 | 14 | 14 | 0 | 15 | 0.483 |
| 0.50 | 29 | 14 | 15 | 29 | 0 | 14 | 14 | 0 | 15 | 0.483 |
| 0.55 | 29 | 14 | 15 | 29 | 0 | 14 | 14 | 0 | 15 | 0.483 |
| 0.60 | 29 | 14 | 15 | 29 | 0 | 14 | 14 | 0 | 15 | 0.483 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 29
- **True AD**: 14 | **True Control**: 15
- **Predicted as AD**: 29 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 14 out of 29 (48.3%)
  - Correct AD: 14 out of 14 (100.0%)
  - Correct Control: 0 out of 15 (0.0%)
- **Incorrectly Classified**: 15 (51.7%)
  - AD → Control: 0
  - Control → AD: 15

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 23 | 13 | 10 | 22 | 1 | 14 | 13 | 1 | 9 | 0.609 |
| 0.55 | 23 | 13 | 10 | 22 | 1 | 14 | 13 | 1 | 9 | 0.609 |
| 0.60 | 23 | 13 | 10 | 19 | 4 | 17 | 13 | 4 | 6 | 0.739 |
| 0.70 ⭐ | 23 | 13 | 10 | 18 | 5 | 18 | 13 | 5 | 5 | 0.783 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 23
- **True AD**: 13 | **True Control**: 10
- **Predicted as AD**: 18 (78.3%)
- **Predicted as Control**: 5 (21.7%)
- **Correctly Classified**: 18 out of 23 (78.3%)
  - Correct AD: 13 out of 13 (100.0%)
  - Correct Control: 5 out of 10 (50.0%)
- **Incorrectly Classified**: 5 (21.7%)
  - AD → Control: 0
  - Control → AD: 5

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 23 | 12 | 11 | 22 | 1 | 13 | 12 | 1 | 10 | 0.565 |
| 0.55 | 23 | 12 | 11 | 22 | 1 | 13 | 12 | 1 | 10 | 0.565 |
| 0.60 | 23 | 12 | 11 | 22 | 1 | 13 | 12 | 1 | 10 | 0.565 |
| 0.65 ⭐ | 23 | 12 | 11 | 21 | 2 | 14 | 12 | 2 | 9 | 0.609 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 23
- **True AD**: 12 | **True Control**: 11
- **Predicted as AD**: 21 (91.3%)
- **Predicted as Control**: 2 (8.7%)
- **Correctly Classified**: 14 out of 23 (60.9%)
  - Correct AD: 12 out of 12 (100.0%)
  - Correct Control: 2 out of 11 (18.2%)
- **Incorrectly Classified**: 9 (39.1%)
  - AD → Control: 0
  - Control → AD: 9

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 25 | 12 | 13 | 22 | 3 | 15 | 12 | 3 | 10 | 0.600 |
| 0.55 | 25 | 12 | 13 | 22 | 3 | 15 | 12 | 3 | 10 | 0.600 |
| 0.60 ⭐ | 25 | 12 | 13 | 21 | 4 | 16 | 12 | 4 | 9 | 0.640 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 25
- **True AD**: 12 | **True Control**: 13
- **Predicted as AD**: 21 (84.0%)
- **Predicted as Control**: 4 (16.0%)
- **Correctly Classified**: 16 out of 25 (64.0%)
  - Correct AD: 12 out of 12 (100.0%)
  - Correct Control: 4 out of 13 (30.8%)
- **Incorrectly Classified**: 9 (36.0%)
  - AD → Control: 0
  - Control → AD: 9

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 30 | 13 | 17 | 27 | 3 | 14 | 12 | 2 | 16 | 0.467 |
| 0.55 | 30 | 13 | 17 | 27 | 3 | 14 | 12 | 2 | 16 | 0.467 |
| 0.60 | 30 | 13 | 17 | 26 | 4 | 13 | 11 | 2 | 17 | 0.433 |
| 0.70 ⭐ | 30 | 13 | 17 | 24 | 6 | 15 | 11 | 4 | 15 | 0.500 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 30
- **True AD**: 13 | **True Control**: 17
- **Predicted as AD**: 24 (80.0%)
- **Predicted as Control**: 6 (20.0%)
- **Correctly Classified**: 15 out of 30 (50.0%)
  - Correct AD: 11 out of 13 (84.6%)
  - Correct Control: 4 out of 17 (23.5%)
- **Incorrectly Classified**: 15 (50.0%)
  - AD → Control: 2
  - Control → AD: 13

---

## PCA_L_6

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 56 | 30 | 26 | 3 | 53 | 27 | 2 | 25 | 29 | 0.482 |
| 0.50 | 56 | 30 | 26 | 1 | 55 | 25 | 0 | 25 | 31 | 0.446 |
| 0.55 | 56 | 30 | 26 | 0 | 56 | 26 | 0 | 26 | 30 | 0.464 |
| 0.60 | 56 | 30 | 26 | 0 | 56 | 26 | 0 | 26 | 30 | 0.464 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 56
- **True AD**: 30 | **True Control**: 26
- **Predicted as AD**: 3 (5.4%)
- **Predicted as Control**: 53 (94.6%)
- **Correctly Classified**: 27 out of 56 (48.2%)
  - Correct AD: 2 out of 30 (6.7%)
  - Correct Control: 25 out of 26 (96.2%)
- **Incorrectly Classified**: 29 (51.8%)
  - AD → Control: 28
  - Control → AD: 1

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.35**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.35 ⭐ | 53 | 27 | 26 | 31 | 22 | 35 | 20 | 15 | 18 | 0.660 |
| 0.50 | 53 | 27 | 26 | 21 | 32 | 33 | 14 | 19 | 20 | 0.623 |
| 0.55 | 53 | 27 | 26 | 17 | 36 | 31 | 11 | 20 | 22 | 0.585 |
| 0.60 | 53 | 27 | 26 | 14 | 39 | 32 | 10 | 22 | 21 | 0.604 |

**Detailed Breakdown at Optimal Threshold (0.35):**

- **Total Subjects**: 53
- **True AD**: 27 | **True Control**: 26
- **Predicted as AD**: 31 (58.5%)
- **Predicted as Control**: 22 (41.5%)
- **Correctly Classified**: 35 out of 53 (66.0%)
  - Correct AD: 20 out of 27 (74.1%)
  - Correct Control: 15 out of 26 (57.7%)
- **Incorrectly Classified**: 18 (34.0%)
  - AD → Control: 7
  - Control → AD: 11

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 54 | 30 | 24 | 19 | 35 | 33 | 14 | 19 | 21 | 0.611 |
| 0.50 | 54 | 30 | 24 | 15 | 39 | 31 | 11 | 20 | 23 | 0.574 |
| 0.55 | 54 | 30 | 24 | 11 | 43 | 33 | 10 | 23 | 21 | 0.611 |
| 0.60 | 54 | 30 | 24 | 9 | 45 | 31 | 8 | 23 | 23 | 0.574 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 54
- **True AD**: 30 | **True Control**: 24
- **Predicted as AD**: 19 (35.2%)
- **Predicted as Control**: 35 (64.8%)
- **Correctly Classified**: 33 out of 54 (61.1%)
  - Correct AD: 14 out of 30 (46.7%)
  - Correct Control: 19 out of 24 (79.2%)
- **Incorrectly Classified**: 21 (38.9%)
  - AD → Control: 16
  - Control → AD: 5

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 46 | 23 | 23 | 42 | 4 | 25 | 22 | 3 | 21 | 0.543 |
| 0.55 | 46 | 23 | 23 | 41 | 5 | 26 | 22 | 4 | 20 | 0.565 |
| 0.60 | 46 | 23 | 23 | 41 | 5 | 26 | 22 | 4 | 20 | 0.565 |
| 0.70 ⭐ | 46 | 23 | 23 | 38 | 8 | 27 | 21 | 6 | 19 | 0.587 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 46
- **True AD**: 23 | **True Control**: 23
- **Predicted as AD**: 38 (82.6%)
- **Predicted as Control**: 8 (17.4%)
- **Correctly Classified**: 27 out of 46 (58.7%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 6 out of 23 (26.1%)
- **Incorrectly Classified**: 19 (41.3%)
  - AD → Control: 2
  - Control → AD: 17

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 53 | 27 | 26 | 50 | 3 | 28 | 26 | 2 | 25 | 0.528 |
| 0.55 | 53 | 27 | 26 | 49 | 4 | 27 | 25 | 2 | 26 | 0.509 |
| 0.60 | 53 | 27 | 26 | 49 | 4 | 27 | 25 | 2 | 26 | 0.509 |
| 0.70 ⭐ | 53 | 27 | 26 | 47 | 6 | 29 | 25 | 4 | 24 | 0.547 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 53
- **True AD**: 27 | **True Control**: 26
- **Predicted as AD**: 47 (88.7%)
- **Predicted as Control**: 6 (11.3%)
- **Correctly Classified**: 29 out of 53 (54.7%)
  - Correct AD: 25 out of 27 (92.6%)
  - Correct Control: 4 out of 26 (15.4%)
- **Incorrectly Classified**: 24 (45.3%)
  - AD → Control: 2
  - Control → AD: 22

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 52 | 30 | 22 | 43 | 9 | 33 | 27 | 6 | 19 | 0.635 |
| 0.55 | 52 | 30 | 22 | 41 | 11 | 33 | 26 | 7 | 19 | 0.635 |
| 0.60 ⭐ | 52 | 30 | 22 | 40 | 12 | 34 | 26 | 8 | 18 | 0.654 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 52
- **True AD**: 30 | **True Control**: 22
- **Predicted as AD**: 40 (76.9%)
- **Predicted as Control**: 12 (23.1%)
- **Correctly Classified**: 34 out of 52 (65.4%)
  - Correct AD: 26 out of 30 (86.7%)
  - Correct Control: 8 out of 22 (36.4%)
- **Incorrectly Classified**: 18 (34.6%)
  - AD → Control: 4
  - Control → AD: 14

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 58 | 32 | 26 | 58 | 0 | 32 | 32 | 0 | 26 | 0.552 |
| 0.55 | 58 | 32 | 26 | 58 | 0 | 32 | 32 | 0 | 26 | 0.552 |
| 0.60 | 58 | 32 | 26 | 58 | 0 | 32 | 32 | 0 | 26 | 0.552 |
| 0.70 ⭐ | 58 | 32 | 26 | 57 | 1 | 33 | 32 | 1 | 25 | 0.569 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 58
- **True AD**: 32 | **True Control**: 26
- **Predicted as AD**: 57 (98.3%)
- **Predicted as Control**: 1 (1.7%)
- **Correctly Classified**: 33 out of 58 (56.9%)
  - Correct AD: 32 out of 32 (100.0%)
  - Correct Control: 1 out of 26 (3.8%)
- **Incorrectly Classified**: 25 (43.1%)
  - AD → Control: 0
  - Control → AD: 25

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 53 | 28 | 25 | 53 | 0 | 28 | 28 | 0 | 25 | 0.528 |
| 0.50 | 53 | 28 | 25 | 53 | 0 | 28 | 28 | 0 | 25 | 0.528 |
| 0.55 | 53 | 28 | 25 | 53 | 0 | 28 | 28 | 0 | 25 | 0.528 |
| 0.60 | 53 | 28 | 25 | 53 | 0 | 28 | 28 | 0 | 25 | 0.528 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 53
- **True AD**: 28 | **True Control**: 25
- **Predicted as AD**: 53 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 28 out of 53 (52.8%)
  - Correct AD: 28 out of 28 (100.0%)
  - Correct Control: 0 out of 25 (0.0%)
- **Incorrectly Classified**: 25 (47.2%)
  - AD → Control: 0
  - Control → AD: 25

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 53 | 27 | 26 | 51 | 2 | 29 | 27 | 2 | 24 | 0.547 |
| 0.55 | 53 | 27 | 26 | 50 | 3 | 30 | 27 | 3 | 23 | 0.566 |
| 0.60 | 53 | 27 | 26 | 50 | 3 | 30 | 27 | 3 | 23 | 0.566 |
| 0.65 ⭐ | 53 | 27 | 26 | 46 | 7 | 34 | 27 | 7 | 19 | 0.642 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 53
- **True AD**: 27 | **True Control**: 26
- **Predicted as AD**: 46 (86.8%)
- **Predicted as Control**: 7 (13.2%)
- **Correctly Classified**: 34 out of 53 (64.2%)
  - Correct AD: 27 out of 27 (100.0%)
  - Correct Control: 7 out of 26 (26.9%)
- **Incorrectly Classified**: 19 (35.8%)
  - AD → Control: 0
  - Control → AD: 19

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 48 | 26 | 22 | 48 | 0 | 26 | 26 | 0 | 22 | 0.542 |
| 0.55 | 48 | 26 | 22 | 48 | 0 | 26 | 26 | 0 | 22 | 0.542 |
| 0.60 ⭐ | 48 | 26 | 22 | 47 | 1 | 27 | 26 | 1 | 21 | 0.562 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 48
- **True AD**: 26 | **True Control**: 22
- **Predicted as AD**: 47 (97.9%)
- **Predicted as Control**: 1 (2.1%)
- **Correctly Classified**: 27 out of 48 (56.2%)
  - Correct AD: 26 out of 26 (100.0%)
  - Correct Control: 1 out of 22 (4.5%)
- **Incorrectly Classified**: 21 (43.8%)
  - AD → Control: 0
  - Control → AD: 21

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 57 | 30 | 27 | 55 | 2 | 32 | 30 | 2 | 25 | 0.561 |
| 0.50 | 57 | 30 | 27 | 55 | 2 | 32 | 30 | 2 | 25 | 0.561 |
| 0.55 | 57 | 30 | 27 | 53 | 4 | 30 | 28 | 2 | 27 | 0.526 |
| 0.60 | 57 | 30 | 27 | 53 | 4 | 30 | 28 | 2 | 27 | 0.526 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 57
- **True AD**: 30 | **True Control**: 27
- **Predicted as AD**: 55 (96.5%)
- **Predicted as Control**: 2 (3.5%)
- **Correctly Classified**: 32 out of 57 (56.1%)
  - Correct AD: 30 out of 30 (100.0%)
  - Correct Control: 2 out of 27 (7.4%)
- **Incorrectly Classified**: 25 (43.9%)
  - AD → Control: 0
  - Control → AD: 25

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 24 | 21 | 36 | 9 | 29 | 22 | 7 | 16 | 0.644 |
| 0.55 | 45 | 24 | 21 | 34 | 11 | 29 | 21 | 8 | 16 | 0.644 |
| 0.60 | 45 | 24 | 21 | 34 | 11 | 29 | 21 | 8 | 16 | 0.644 |
| 0.65 ⭐ | 45 | 24 | 21 | 33 | 12 | 30 | 21 | 9 | 15 | 0.667 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 45
- **True AD**: 24 | **True Control**: 21
- **Predicted as AD**: 33 (73.3%)
- **Predicted as Control**: 12 (26.7%)
- **Correctly Classified**: 30 out of 45 (66.7%)
  - Correct AD: 21 out of 24 (87.5%)
  - Correct Control: 9 out of 21 (42.9%)
- **Incorrectly Classified**: 15 (33.3%)
  - AD → Control: 3
  - Control → AD: 12

---

## 📋 Summary: Optimal Thresholds by Model×Hyperparameter×Experiment

| Experiment | Model×Hyperparameters | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |
|------------|------------------------|-------------------|----------------|---------|-----------|----------|
| ANOVA_L_2 | KNN_n_neighbors=1 | 0.50 | 33 | 31 | 2 | 0.939 |
| ANOVA_L_2 | KNN_n_neighbors=15 | 0.45 | 15 | 13 | 2 | 0.867 |
| ANOVA_L_2 | KNN_n_neighbors=7 | 0.50 | 36 | 33 | 3 | 0.917 |
| ANOVA_L_2 | MLP_hidden=100 | 0.60 | 30 | 27 | 3 | 0.900 |
| ANOVA_L_2 | MLP_hidden=150_50 | 0.45 | 19 | 17 | 2 | 0.895 |
| ANOVA_L_2 | MLP_hidden=200_100_50 | 0.50 | 9 | 7 | 2 | 0.778 |
| ANOVA_L_2 | SVM_kernel=linear | 0.40 | 11 | 9 | 2 | 0.818 |
| ANOVA_L_2 | SVM_kernel=poly | 0.45 | 28 | 18 | 10 | 0.643 |
| ANOVA_L_2 | SVM_kernel=rbf | 0.45 | 32 | 23 | 9 | 0.719 |
| ANOVA_L_2 | XGBoost_max_depth=3 | 0.55 | 27 | 23 | 4 | 0.852 |
| ANOVA_L_2 | XGBoost_max_depth=6 | 0.50 | 18 | 15 | 3 | 0.833 |
| ANOVA_L_2 | XGBoost_max_depth=9 | 0.55 | 30 | 26 | 4 | 0.867 |
| ANOVA_L_6 | KNN_n_neighbors=1 | 0.45 | 50 | 42 | 8 | 0.840 |
| ANOVA_L_6 | KNN_n_neighbors=15 | 0.65 | 49 | 41 | 8 | 0.837 |
| ANOVA_L_6 | KNN_n_neighbors=7 | 0.50 | 55 | 48 | 7 | 0.873 |
| ANOVA_L_6 | MLP_hidden=100 | 0.50 | 61 | 52 | 9 | 0.852 |
| ANOVA_L_6 | MLP_hidden=150_50 | 0.55 | 27 | 23 | 4 | 0.852 |
| ANOVA_L_6 | MLP_hidden=200_100_50 | 0.45 | 29 | 25 | 4 | 0.862 |
| ANOVA_L_6 | SVM_kernel=linear | 0.70 | 37 | 35 | 2 | 0.946 |
| ANOVA_L_6 | SVM_kernel=poly | 0.65 | 56 | 43 | 13 | 0.768 |
| ANOVA_L_6 | SVM_kernel=rbf | 0.60 | 54 | 43 | 11 | 0.796 |
| ANOVA_L_6 | XGBoost_max_depth=3 | 0.50 | 54 | 43 | 11 | 0.796 |
| ANOVA_L_6 | XGBoost_max_depth=6 | 0.50 | 57 | 45 | 12 | 0.789 |
| ANOVA_L_6 | XGBoost_max_depth=9 | 0.70 | 54 | 46 | 8 | 0.852 |
| PCA_L_2 | KNN_n_neighbors=1 | 0.30 | 20 | 10 | 10 | 0.500 |
| PCA_L_2 | KNN_n_neighbors=15 | 0.35 | 22 | 16 | 6 | 0.727 |
| PCA_L_2 | KNN_n_neighbors=7 | 0.30 | 23 | 17 | 6 | 0.739 |
| PCA_L_2 | MLP_hidden=100 | 0.65 | 27 | 15 | 12 | 0.556 |
| PCA_L_2 | MLP_hidden=150_50 | 0.65 | 28 | 16 | 12 | 0.571 |
| PCA_L_2 | MLP_hidden=200_100_50 | 0.65 | 26 | 16 | 10 | 0.615 |
| PCA_L_2 | SVM_kernel=linear | 0.60 | 25 | 14 | 11 | 0.560 |
| PCA_L_2 | SVM_kernel=poly | 0.30 | 29 | 14 | 15 | 0.483 |
| PCA_L_2 | SVM_kernel=rbf | 0.70 | 23 | 18 | 5 | 0.783 |
| PCA_L_2 | XGBoost_max_depth=3 | 0.65 | 23 | 14 | 9 | 0.609 |
| PCA_L_2 | XGBoost_max_depth=6 | 0.60 | 25 | 16 | 9 | 0.640 |
| PCA_L_2 | XGBoost_max_depth=9 | 0.70 | 30 | 15 | 15 | 0.500 |
| PCA_L_6 | KNN_n_neighbors=1 | 0.30 | 56 | 27 | 29 | 0.482 |
| PCA_L_6 | KNN_n_neighbors=15 | 0.35 | 53 | 35 | 18 | 0.660 |
| PCA_L_6 | KNN_n_neighbors=7 | 0.45 | 54 | 33 | 21 | 0.611 |
| PCA_L_6 | MLP_hidden=100 | 0.70 | 46 | 27 | 19 | 0.587 |
| PCA_L_6 | MLP_hidden=150_50 | 0.70 | 53 | 29 | 24 | 0.547 |
| PCA_L_6 | MLP_hidden=200_100_50 | 0.60 | 52 | 34 | 18 | 0.654 |
| PCA_L_6 | SVM_kernel=linear | 0.70 | 58 | 33 | 25 | 0.569 |
| PCA_L_6 | SVM_kernel=poly | 0.30 | 53 | 28 | 25 | 0.528 |
| PCA_L_6 | SVM_kernel=rbf | 0.65 | 53 | 34 | 19 | 0.642 |
| PCA_L_6 | XGBoost_max_depth=3 | 0.60 | 48 | 27 | 21 | 0.562 |
| PCA_L_6 | XGBoost_max_depth=6 | 0.45 | 57 | 32 | 25 | 0.561 |
| PCA_L_6 | XGBoost_max_depth=9 | 0.65 | 45 | 30 | 15 | 0.667 |

## 🎯 KNN-Specific Summary (Per Experiment)

| Experiment | KNN Hyperparameters | Threshold | Total | Correct | Incorrect | Accuracy |
|------------|---------------------|-----------|-------|---------|-----------|----------|
| ANOVA_L_2 | n_neighbors=1 | 0.50 | 33 | 31 | 2 | 0.939 |
| ANOVA_L_2 | n_neighbors=15 | 0.45 | 15 | 13 | 2 | 0.867 |
| ANOVA_L_2 | n_neighbors=7 | 0.50 | 36 | 33 | 3 | 0.917 |
| ANOVA_L_6 | n_neighbors=1 | 0.45 | 50 | 42 | 8 | 0.840 |
| ANOVA_L_6 | n_neighbors=15 | 0.65 | 49 | 41 | 8 | 0.837 |
| ANOVA_L_6 | n_neighbors=7 | 0.50 | 55 | 48 | 7 | 0.873 |
| PCA_L_2 | n_neighbors=1 | 0.30 | 20 | 10 | 10 | 0.500 |
| PCA_L_2 | n_neighbors=15 | 0.35 | 22 | 16 | 6 | 0.727 |
| PCA_L_2 | n_neighbors=7 | 0.30 | 23 | 17 | 6 | 0.739 |
| PCA_L_6 | n_neighbors=1 | 0.30 | 56 | 27 | 29 | 0.482 |
| PCA_L_6 | n_neighbors=15 | 0.35 | 53 | 35 | 18 | 0.660 |
| PCA_L_6 | n_neighbors=7 | 0.45 | 54 | 33 | 21 | 0.611 |

## 🔑 Key Points

1. **Each experiment analyzed independently** - no cross-experiment averaging
2. **Per-subject performance calculated within each experiment** - averaged across folds only
3. **Threshold optimization per model×experiment×hyperparameter** - each combination gets its own optimal threshold
4. **Subject counts are per experiment** - same subject in different experiments counted separately

---
*Analysis completed: 2025-12-12 21:12*
*Each experiment treated independently - no cross-experiment averaging*
