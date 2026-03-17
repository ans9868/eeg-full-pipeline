# 🎯 Hyperparameter-Specific Threshold Analysis

## Analysis Overview

This analysis finds optimal thresholds for **each model×hyperparameter combination separately**.
For example, KNN with n_neighbors=7 and KNN with n_neighbors=3 are analyzed independently.

## 📊 Results by Experiment and Model×Hyperparameter

## ANOVA_L_2

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 25 | 13 | 12 | 14 | 11 | 22 | 12 | 10 | 3 | 0.880 |
| 0.50 | 25 | 13 | 12 | 14 | 11 | 22 | 12 | 10 | 3 | 0.880 |
| 0.55 | 25 | 13 | 12 | 13 | 12 | 21 | 11 | 10 | 4 | 0.840 |
| 0.60 | 25 | 13 | 12 | 9 | 16 | 17 | 7 | 10 | 8 | 0.680 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 25
- **True AD**: 13 | **True Control**: 12
- **Predicted as AD**: 14 (56.0%)
- **Predicted as Control**: 11 (44.0%)
- **Correctly Classified**: 22 out of 25 (88.0%)
  - Correct AD: 12 out of 13 (92.3%)
  - Correct Control: 10 out of 12 (83.3%)
- **Incorrectly Classified**: 3 (12.0%)
  - AD → Control: 1
  - Control → AD: 2

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.45**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.45 ⭐ | 18 | 9 | 9 | 11 | 7 | 16 | 9 | 7 | 2 | 0.889 |
| 0.50 | 18 | 9 | 9 | 10 | 8 | 15 | 8 | 7 | 3 | 0.833 |
| 0.55 | 18 | 9 | 9 | 9 | 9 | 14 | 7 | 7 | 4 | 0.778 |
| 0.60 | 18 | 9 | 9 | 8 | 10 | 13 | 6 | 7 | 5 | 0.722 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 18
- **True AD**: 9 | **True Control**: 9
- **Predicted as AD**: 11 (61.1%)
- **Predicted as Control**: 7 (38.9%)
- **Correctly Classified**: 16 out of 18 (88.9%)
  - Correct AD: 9 out of 9 (100.0%)
  - Correct Control: 7 out of 9 (77.8%)
- **Incorrectly Classified**: 2 (11.1%)
  - AD → Control: 0
  - Control → AD: 2

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.40**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.40 ⭐ | 28 | 14 | 14 | 16 | 12 | 26 | 14 | 12 | 2 | 0.929 |
| 0.50 | 28 | 14 | 14 | 16 | 12 | 26 | 14 | 12 | 2 | 0.929 |
| 0.55 | 28 | 14 | 14 | 16 | 12 | 26 | 14 | 12 | 2 | 0.929 |
| 0.60 | 28 | 14 | 14 | 15 | 13 | 25 | 13 | 12 | 3 | 0.893 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 28
- **True AD**: 14 | **True Control**: 14
- **Predicted as AD**: 16 (57.1%)
- **Predicted as Control**: 12 (42.9%)
- **Correctly Classified**: 26 out of 28 (92.9%)
  - Correct AD: 14 out of 14 (100.0%)
  - Correct Control: 12 out of 14 (85.7%)
- **Incorrectly Classified**: 2 (7.1%)
  - AD → Control: 0
  - Control → AD: 2

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 27 | 13 | 14 | 16 | 11 | 22 | 12 | 10 | 5 | 0.815 |
| 0.55 | 27 | 13 | 14 | 16 | 11 | 22 | 12 | 10 | 5 | 0.815 |
| 0.60 ⭐ | 27 | 13 | 14 | 15 | 12 | 23 | 12 | 11 | 4 | 0.852 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 27
- **True AD**: 13 | **True Control**: 14
- **Predicted as AD**: 15 (55.6%)
- **Predicted as Control**: 12 (44.4%)
- **Correctly Classified**: 23 out of 27 (85.2%)
  - Correct AD: 12 out of 13 (92.3%)
  - Correct Control: 11 out of 14 (78.6%)
- **Incorrectly Classified**: 4 (14.8%)
  - AD → Control: 1
  - Control → AD: 3

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 21 | 9 | 12 | 12 | 9 | 18 | 9 | 9 | 3 | 0.857 |
| 0.55 ⭐ | 21 | 9 | 12 | 11 | 10 | 19 | 9 | 10 | 2 | 0.905 |
| 0.60 | 21 | 9 | 12 | 11 | 10 | 19 | 9 | 10 | 2 | 0.905 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 21
- **True AD**: 9 | **True Control**: 12
- **Predicted as AD**: 11 (52.4%)
- **Predicted as Control**: 10 (47.6%)
- **Correctly Classified**: 19 out of 21 (90.5%)
  - Correct AD: 9 out of 9 (100.0%)
  - Correct Control: 10 out of 12 (83.3%)
- **Incorrectly Classified**: 2 (9.5%)
  - AD → Control: 0
  - Control → AD: 2

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 12 | 6 | 6 | 8 | 4 | 10 | 6 | 4 | 2 | 0.833 |
| 0.55 | 12 | 6 | 6 | 8 | 4 | 10 | 6 | 4 | 2 | 0.833 |
| 0.60 | 12 | 6 | 6 | 8 | 4 | 10 | 6 | 4 | 2 | 0.833 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 12
- **True AD**: 6 | **True Control**: 6
- **Predicted as AD**: 8 (66.7%)
- **Predicted as Control**: 4 (33.3%)
- **Correctly Classified**: 10 out of 12 (83.3%)
  - Correct AD: 6 out of 6 (100.0%)
  - Correct Control: 4 out of 6 (66.7%)
- **Incorrectly Classified**: 2 (16.7%)
  - AD → Control: 0
  - Control → AD: 2

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 23 | 11 | 12 | 15 | 8 | 19 | 11 | 8 | 4 | 0.826 |
| 0.55 | 23 | 11 | 12 | 15 | 8 | 19 | 11 | 8 | 4 | 0.826 |
| 0.60 | 23 | 11 | 12 | 15 | 8 | 19 | 11 | 8 | 4 | 0.826 |
| 0.65 ⭐ | 23 | 11 | 12 | 14 | 9 | 20 | 11 | 9 | 3 | 0.870 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 23
- **True AD**: 11 | **True Control**: 12
- **Predicted as AD**: 14 (60.9%)
- **Predicted as Control**: 9 (39.1%)
- **Correctly Classified**: 20 out of 23 (87.0%)
  - Correct AD: 11 out of 11 (100.0%)
  - Correct Control: 9 out of 12 (75.0%)
- **Incorrectly Classified**: 3 (13.0%)
  - AD → Control: 0
  - Control → AD: 3

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 33 | 15 | 18 | 24 | 9 | 22 | 14 | 8 | 11 | 0.667 |
| 0.55 ⭐ | 33 | 15 | 18 | 19 | 14 | 23 | 12 | 11 | 10 | 0.697 |
| 0.60 | 33 | 15 | 18 | 19 | 14 | 23 | 12 | 11 | 10 | 0.697 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 33
- **True AD**: 15 | **True Control**: 18
- **Predicted as AD**: 19 (57.6%)
- **Predicted as Control**: 14 (42.4%)
- **Correctly Classified**: 23 out of 33 (69.7%)
  - Correct AD: 12 out of 15 (80.0%)
  - Correct Control: 11 out of 18 (61.1%)
- **Incorrectly Classified**: 10 (30.3%)
  - AD → Control: 3
  - Control → AD: 7

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 30 | 14 | 16 | 20 | 10 | 24 | 14 | 10 | 6 | 0.800 |
| 0.55 | 30 | 14 | 16 | 19 | 11 | 25 | 14 | 11 | 5 | 0.833 |
| 0.60 ⭐ | 30 | 14 | 16 | 18 | 12 | 26 | 14 | 12 | 4 | 0.867 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 30
- **True AD**: 14 | **True Control**: 16
- **Predicted as AD**: 18 (60.0%)
- **Predicted as Control**: 12 (40.0%)
- **Correctly Classified**: 26 out of 30 (86.7%)
  - Correct AD: 14 out of 14 (100.0%)
  - Correct Control: 12 out of 16 (75.0%)
- **Incorrectly Classified**: 4 (13.3%)
  - AD → Control: 0
  - Control → AD: 4

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 34 | 16 | 18 | 21 | 13 | 25 | 14 | 11 | 9 | 0.735 |
| 0.55 | 34 | 16 | 18 | 19 | 15 | 27 | 14 | 13 | 7 | 0.794 |
| 0.60 | 34 | 16 | 18 | 18 | 16 | 26 | 13 | 13 | 8 | 0.765 |
| 0.70 ⭐ | 34 | 16 | 18 | 14 | 20 | 28 | 12 | 16 | 6 | 0.824 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 34
- **True AD**: 16 | **True Control**: 18
- **Predicted as AD**: 14 (41.2%)
- **Predicted as Control**: 20 (58.8%)
- **Correctly Classified**: 28 out of 34 (82.4%)
  - Correct AD: 12 out of 16 (75.0%)
  - Correct Control: 16 out of 18 (88.9%)
- **Incorrectly Classified**: 6 (17.6%)
  - AD → Control: 4
  - Control → AD: 2

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 25 | 12 | 13 | 15 | 10 | 22 | 12 | 10 | 3 | 0.880 |
| 0.55 | 25 | 12 | 13 | 15 | 10 | 22 | 12 | 10 | 3 | 0.880 |
| 0.60 | 25 | 12 | 13 | 13 | 12 | 22 | 11 | 11 | 3 | 0.880 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 25
- **True AD**: 12 | **True Control**: 13
- **Predicted as AD**: 15 (60.0%)
- **Predicted as Control**: 10 (40.0%)
- **Correctly Classified**: 22 out of 25 (88.0%)
  - Correct AD: 12 out of 12 (100.0%)
  - Correct Control: 10 out of 13 (76.9%)
- **Incorrectly Classified**: 3 (12.0%)
  - AD → Control: 0
  - Control → AD: 3

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 22 | 11 | 11 | 14 | 8 | 19 | 11 | 8 | 3 | 0.864 |
| 0.55 ⭐ | 22 | 11 | 11 | 13 | 9 | 20 | 11 | 9 | 2 | 0.909 |
| 0.60 | 22 | 11 | 11 | 12 | 10 | 19 | 10 | 9 | 3 | 0.864 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 22
- **True AD**: 11 | **True Control**: 11
- **Predicted as AD**: 13 (59.1%)
- **Predicted as Control**: 9 (40.9%)
- **Correctly Classified**: 20 out of 22 (90.9%)
  - Correct AD: 11 out of 11 (100.0%)
  - Correct Control: 9 out of 11 (81.8%)
- **Incorrectly Classified**: 2 (9.1%)
  - AD → Control: 0
  - Control → AD: 2

---

## ANOVA_L_6

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 61 | 33 | 28 | 33 | 28 | 51 | 28 | 23 | 10 | 0.836 |
| 0.55 ⭐ | 61 | 33 | 28 | 30 | 31 | 52 | 27 | 25 | 9 | 0.852 |
| 0.60 | 61 | 33 | 28 | 23 | 38 | 45 | 20 | 25 | 16 | 0.738 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 61
- **True AD**: 33 | **True Control**: 28
- **Predicted as AD**: 30 (49.2%)
- **Predicted as Control**: 31 (50.8%)
- **Correctly Classified**: 52 out of 61 (85.2%)
  - Correct AD: 27 out of 33 (81.8%)
  - Correct Control: 25 out of 28 (89.3%)
- **Incorrectly Classified**: 9 (14.8%)
  - AD → Control: 6
  - Control → AD: 3

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 50 | 26 | 24 | 24 | 26 | 42 | 21 | 21 | 8 | 0.840 |
| 0.55 ⭐ | 50 | 26 | 24 | 23 | 27 | 43 | 21 | 22 | 7 | 0.860 |
| 0.60 | 50 | 26 | 24 | 22 | 28 | 42 | 20 | 22 | 8 | 0.840 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 50
- **True AD**: 26 | **True Control**: 24
- **Predicted as AD**: 23 (46.0%)
- **Predicted as Control**: 27 (54.0%)
- **Correctly Classified**: 43 out of 50 (86.0%)
  - Correct AD: 21 out of 26 (80.8%)
  - Correct Control: 22 out of 24 (91.7%)
- **Incorrectly Classified**: 7 (14.0%)
  - AD → Control: 5
  - Control → AD: 2

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 58 | 33 | 25 | 33 | 25 | 50 | 29 | 21 | 8 | 0.862 |
| 0.55 | 58 | 33 | 25 | 31 | 27 | 48 | 27 | 21 | 10 | 0.828 |
| 0.60 | 58 | 33 | 25 | 29 | 29 | 48 | 26 | 22 | 10 | 0.828 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 58
- **True AD**: 33 | **True Control**: 25
- **Predicted as AD**: 33 (56.9%)
- **Predicted as Control**: 25 (43.1%)
- **Correctly Classified**: 50 out of 58 (86.2%)
  - Correct AD: 29 out of 33 (87.9%)
  - Correct Control: 21 out of 25 (84.0%)
- **Incorrectly Classified**: 8 (13.8%)
  - AD → Control: 4
  - Control → AD: 4

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 47 | 24 | 23 | 29 | 18 | 40 | 23 | 17 | 7 | 0.851 |
| 0.55 | 47 | 24 | 23 | 29 | 18 | 40 | 23 | 17 | 7 | 0.851 |
| 0.60 | 47 | 24 | 23 | 28 | 19 | 39 | 22 | 17 | 8 | 0.830 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 47
- **True AD**: 24 | **True Control**: 23
- **Predicted as AD**: 29 (61.7%)
- **Predicted as Control**: 18 (38.3%)
- **Correctly Classified**: 40 out of 47 (85.1%)
  - Correct AD: 23 out of 24 (95.8%)
  - Correct Control: 17 out of 23 (73.9%)
- **Incorrectly Classified**: 7 (14.9%)
  - AD → Control: 1
  - Control → AD: 6

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 42 | 20 | 22 | 23 | 19 | 35 | 18 | 17 | 7 | 0.833 |
| 0.55 | 42 | 20 | 22 | 21 | 21 | 35 | 17 | 18 | 7 | 0.833 |
| 0.60 | 42 | 20 | 22 | 21 | 21 | 35 | 17 | 18 | 7 | 0.833 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 42
- **True AD**: 20 | **True Control**: 22
- **Predicted as AD**: 23 (54.8%)
- **Predicted as Control**: 19 (45.2%)
- **Correctly Classified**: 35 out of 42 (83.3%)
  - Correct AD: 18 out of 20 (90.0%)
  - Correct Control: 17 out of 22 (77.3%)
- **Incorrectly Classified**: 7 (16.7%)
  - AD → Control: 2
  - Control → AD: 5

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 35 | 17 | 18 | 23 | 12 | 29 | 17 | 12 | 6 | 0.829 |
| 0.55 | 35 | 17 | 18 | 22 | 13 | 30 | 17 | 13 | 5 | 0.857 |
| 0.60 | 35 | 17 | 18 | 20 | 15 | 30 | 16 | 14 | 5 | 0.857 |
| 0.65 ⭐ | 35 | 17 | 18 | 19 | 16 | 31 | 16 | 15 | 4 | 0.886 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 35
- **True AD**: 17 | **True Control**: 18
- **Predicted as AD**: 19 (54.3%)
- **Predicted as Control**: 16 (45.7%)
- **Correctly Classified**: 31 out of 35 (88.6%)
  - Correct AD: 16 out of 17 (94.1%)
  - Correct Control: 15 out of 18 (83.3%)
- **Incorrectly Classified**: 4 (11.4%)
  - AD → Control: 1
  - Control → AD: 3

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 47 | 24 | 23 | 30 | 17 | 39 | 23 | 16 | 8 | 0.830 |
| 0.55 ⭐ | 47 | 24 | 23 | 29 | 18 | 40 | 23 | 17 | 7 | 0.851 |
| 0.60 | 47 | 24 | 23 | 29 | 18 | 40 | 23 | 17 | 7 | 0.851 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 47
- **True AD**: 24 | **True Control**: 23
- **Predicted as AD**: 29 (61.7%)
- **Predicted as Control**: 18 (38.3%)
- **Correctly Classified**: 40 out of 47 (85.1%)
  - Correct AD: 23 out of 24 (95.8%)
  - Correct Control: 17 out of 23 (73.9%)
- **Incorrectly Classified**: 7 (14.9%)
  - AD → Control: 1
  - Control → AD: 6

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 61 | 34 | 27 | 48 | 13 | 43 | 32 | 11 | 18 | 0.705 |
| 0.55 | 61 | 34 | 27 | 45 | 16 | 44 | 31 | 13 | 17 | 0.721 |
| 0.60 ⭐ | 61 | 34 | 27 | 41 | 20 | 46 | 30 | 16 | 15 | 0.754 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 61
- **True AD**: 34 | **True Control**: 27
- **Predicted as AD**: 41 (67.2%)
- **Predicted as Control**: 20 (32.8%)
- **Correctly Classified**: 46 out of 61 (75.4%)
  - Correct AD: 30 out of 34 (88.2%)
  - Correct Control: 16 out of 27 (59.3%)
- **Incorrectly Classified**: 15 (24.6%)
  - AD → Control: 4
  - Control → AD: 11

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 51 | 28 | 23 | 38 | 13 | 37 | 26 | 11 | 14 | 0.725 |
| 0.55 | 51 | 28 | 23 | 37 | 14 | 38 | 26 | 12 | 13 | 0.745 |
| 0.60 ⭐ | 51 | 28 | 23 | 35 | 16 | 40 | 26 | 14 | 11 | 0.784 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 51
- **True AD**: 28 | **True Control**: 23
- **Predicted as AD**: 35 (68.6%)
- **Predicted as Control**: 16 (31.4%)
- **Correctly Classified**: 40 out of 51 (78.4%)
  - Correct AD: 26 out of 28 (92.9%)
  - Correct Control: 14 out of 23 (60.9%)
- **Incorrectly Classified**: 11 (21.6%)
  - AD → Control: 2
  - Control → AD: 9

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 40 | 22 | 18 | 27 | 13 | 31 | 20 | 11 | 9 | 0.775 |
| 0.55 | 40 | 22 | 18 | 26 | 14 | 30 | 19 | 11 | 10 | 0.750 |
| 0.60 | 40 | 22 | 18 | 23 | 17 | 31 | 18 | 13 | 9 | 0.775 |
| 0.65 ⭐ | 40 | 22 | 18 | 20 | 20 | 34 | 18 | 16 | 6 | 0.850 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 40
- **True AD**: 22 | **True Control**: 18
- **Predicted as AD**: 20 (50.0%)
- **Predicted as Control**: 20 (50.0%)
- **Correctly Classified**: 34 out of 40 (85.0%)
  - Correct AD: 18 out of 22 (81.8%)
  - Correct Control: 16 out of 18 (88.9%)
- **Incorrectly Classified**: 6 (15.0%)
  - AD → Control: 4
  - Control → AD: 2

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 51 | 27 | 24 | 31 | 20 | 41 | 24 | 17 | 10 | 0.804 |
| 0.55 | 51 | 27 | 24 | 27 | 24 | 41 | 22 | 19 | 10 | 0.804 |
| 0.60 | 51 | 27 | 24 | 26 | 25 | 40 | 21 | 19 | 11 | 0.784 |
| 0.70 ⭐ | 51 | 27 | 24 | 23 | 28 | 43 | 21 | 22 | 8 | 0.843 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 51
- **True AD**: 27 | **True Control**: 24
- **Predicted as AD**: 23 (45.1%)
- **Predicted as Control**: 28 (54.9%)
- **Correctly Classified**: 43 out of 51 (84.3%)
  - Correct AD: 21 out of 27 (77.8%)
  - Correct Control: 22 out of 24 (91.7%)
- **Incorrectly Classified**: 8 (15.7%)
  - AD → Control: 6
  - Control → AD: 2

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.50**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 ⭐ | 60 | 34 | 26 | 37 | 23 | 49 | 30 | 19 | 11 | 0.817 |
| 0.55 | 60 | 34 | 26 | 35 | 25 | 47 | 28 | 19 | 13 | 0.783 |
| 0.60 | 60 | 34 | 26 | 31 | 29 | 47 | 26 | 21 | 13 | 0.783 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 60
- **True AD**: 34 | **True Control**: 26
- **Predicted as AD**: 37 (61.7%)
- **Predicted as Control**: 23 (38.3%)
- **Correctly Classified**: 49 out of 60 (81.7%)
  - Correct AD: 30 out of 34 (88.2%)
  - Correct Control: 19 out of 26 (73.1%)
- **Incorrectly Classified**: 11 (18.3%)
  - AD → Control: 4
  - Control → AD: 7

---

## PCA_L_2

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 23 | 11 | 12 | 0 | 23 | 12 | 0 | 12 | 11 | 0.522 |
| 0.50 | 23 | 11 | 12 | 0 | 23 | 12 | 0 | 12 | 11 | 0.522 |
| 0.55 | 23 | 11 | 12 | 0 | 23 | 12 | 0 | 12 | 11 | 0.522 |
| 0.60 | 23 | 11 | 12 | 0 | 23 | 12 | 0 | 12 | 11 | 0.522 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 23
- **True AD**: 11 | **True Control**: 12
- **Predicted as AD**: 0 (0.0%)
- **Predicted as Control**: 23 (100.0%)
- **Correctly Classified**: 12 out of 23 (52.2%)
  - Correct AD: 0 out of 11 (0.0%)
  - Correct Control: 12 out of 12 (100.0%)
- **Incorrectly Classified**: 11 (47.8%)
  - AD → Control: 11
  - Control → AD: 0

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 28 | 14 | 14 | 8 | 20 | 18 | 6 | 12 | 10 | 0.643 |
| 0.50 | 28 | 14 | 14 | 2 | 26 | 14 | 1 | 13 | 14 | 0.500 |
| 0.55 | 28 | 14 | 14 | 2 | 26 | 14 | 1 | 13 | 14 | 0.500 |
| 0.60 | 28 | 14 | 14 | 2 | 26 | 14 | 1 | 13 | 14 | 0.500 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 28
- **True AD**: 14 | **True Control**: 14
- **Predicted as AD**: 8 (28.6%)
- **Predicted as Control**: 20 (71.4%)
- **Correctly Classified**: 18 out of 28 (64.3%)
  - Correct AD: 6 out of 14 (42.9%)
  - Correct Control: 12 out of 14 (85.7%)
- **Incorrectly Classified**: 10 (35.7%)
  - AD → Control: 8
  - Control → AD: 2

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 30 | 15 | 15 | 12 | 18 | 21 | 9 | 12 | 9 | 0.700 |
| 0.50 | 30 | 15 | 15 | 3 | 27 | 14 | 1 | 13 | 16 | 0.467 |
| 0.55 | 30 | 15 | 15 | 3 | 27 | 14 | 1 | 13 | 16 | 0.467 |
| 0.60 | 30 | 15 | 15 | 2 | 28 | 13 | 0 | 13 | 17 | 0.433 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 30
- **True AD**: 15 | **True Control**: 15
- **Predicted as AD**: 12 (40.0%)
- **Predicted as Control**: 18 (60.0%)
- **Correctly Classified**: 21 out of 30 (70.0%)
  - Correct AD: 9 out of 15 (60.0%)
  - Correct Control: 12 out of 15 (80.0%)
- **Incorrectly Classified**: 9 (30.0%)
  - AD → Control: 6
  - Control → AD: 3

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 30 | 16 | 14 | 30 | 0 | 16 | 16 | 0 | 14 | 0.533 |
| 0.50 | 30 | 16 | 14 | 30 | 0 | 16 | 16 | 0 | 14 | 0.533 |
| 0.55 | 30 | 16 | 14 | 30 | 0 | 16 | 16 | 0 | 14 | 0.533 |
| 0.60 | 30 | 16 | 14 | 30 | 0 | 16 | 16 | 0 | 14 | 0.533 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 30
- **True AD**: 16 | **True Control**: 14
- **Predicted as AD**: 30 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 16 out of 30 (53.3%)
  - Correct AD: 16 out of 16 (100.0%)
  - Correct Control: 0 out of 14 (0.0%)
- **Incorrectly Classified**: 14 (46.7%)
  - AD → Control: 0
  - Control → AD: 14

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 24 | 11 | 13 | 23 | 1 | 12 | 11 | 1 | 12 | 0.500 |
| 0.50 | 24 | 11 | 13 | 23 | 1 | 12 | 11 | 1 | 12 | 0.500 |
| 0.55 | 24 | 11 | 13 | 23 | 1 | 12 | 11 | 1 | 12 | 0.500 |
| 0.60 | 24 | 11 | 13 | 23 | 1 | 12 | 11 | 1 | 12 | 0.500 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 24
- **True AD**: 11 | **True Control**: 13
- **Predicted as AD**: 23 (95.8%)
- **Predicted as Control**: 1 (4.2%)
- **Correctly Classified**: 12 out of 24 (50.0%)
  - Correct AD: 11 out of 11 (100.0%)
  - Correct Control: 1 out of 13 (7.7%)
- **Incorrectly Classified**: 12 (50.0%)
  - AD → Control: 0
  - Control → AD: 12

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 23 | 11 | 12 | 23 | 0 | 11 | 11 | 0 | 12 | 0.478 |
| 0.55 | 23 | 11 | 12 | 23 | 0 | 11 | 11 | 0 | 12 | 0.478 |
| 0.60 | 23 | 11 | 12 | 22 | 1 | 12 | 11 | 1 | 11 | 0.522 |
| 0.65 ⭐ | 23 | 11 | 12 | 21 | 2 | 13 | 11 | 2 | 10 | 0.565 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 23
- **True AD**: 11 | **True Control**: 12
- **Predicted as AD**: 21 (91.3%)
- **Predicted as Control**: 2 (8.7%)
- **Correctly Classified**: 13 out of 23 (56.5%)
  - Correct AD: 11 out of 11 (100.0%)
  - Correct Control: 2 out of 12 (16.7%)
- **Incorrectly Classified**: 10 (43.5%)
  - AD → Control: 0
  - Control → AD: 10

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 27 | 13 | 14 | 27 | 0 | 13 | 13 | 0 | 14 | 0.481 |
| 0.50 | 27 | 13 | 14 | 27 | 0 | 13 | 13 | 0 | 14 | 0.481 |
| 0.55 | 27 | 13 | 14 | 27 | 0 | 13 | 13 | 0 | 14 | 0.481 |
| 0.60 | 27 | 13 | 14 | 27 | 0 | 13 | 13 | 0 | 14 | 0.481 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 27
- **True AD**: 13 | **True Control**: 14
- **Predicted as AD**: 27 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 13 out of 27 (48.1%)
  - Correct AD: 13 out of 13 (100.0%)
  - Correct Control: 0 out of 14 (0.0%)
- **Incorrectly Classified**: 14 (51.9%)
  - AD → Control: 0
  - Control → AD: 14

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 24 | 11 | 13 | 24 | 0 | 11 | 11 | 0 | 13 | 0.458 |
| 0.50 | 24 | 11 | 13 | 24 | 0 | 11 | 11 | 0 | 13 | 0.458 |
| 0.55 | 24 | 11 | 13 | 24 | 0 | 11 | 11 | 0 | 13 | 0.458 |
| 0.60 | 24 | 11 | 13 | 24 | 0 | 11 | 11 | 0 | 13 | 0.458 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 24
- **True AD**: 11 | **True Control**: 13
- **Predicted as AD**: 24 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 11 out of 24 (45.8%)
  - Correct AD: 11 out of 11 (100.0%)
  - Correct Control: 0 out of 13 (0.0%)
- **Incorrectly Classified**: 13 (54.2%)
  - AD → Control: 0
  - Control → AD: 13

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 25 | 13 | 12 | 23 | 2 | 15 | 13 | 2 | 10 | 0.600 |
| 0.55 | 25 | 13 | 12 | 23 | 2 | 15 | 13 | 2 | 10 | 0.600 |
| 0.60 | 25 | 13 | 12 | 22 | 3 | 16 | 13 | 3 | 9 | 0.640 |
| 0.65 ⭐ | 25 | 13 | 12 | 21 | 4 | 17 | 13 | 4 | 8 | 0.680 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 25
- **True AD**: 13 | **True Control**: 12
- **Predicted as AD**: 21 (84.0%)
- **Predicted as Control**: 4 (16.0%)
- **Correctly Classified**: 17 out of 25 (68.0%)
  - Correct AD: 13 out of 13 (100.0%)
  - Correct Control: 4 out of 12 (33.3%)
- **Incorrectly Classified**: 8 (32.0%)
  - AD → Control: 0
  - Control → AD: 8

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 27 | 14 | 13 | 25 | 2 | 16 | 14 | 2 | 11 | 0.593 |
| 0.55 | 27 | 14 | 13 | 25 | 2 | 16 | 14 | 2 | 11 | 0.593 |
| 0.60 | 27 | 14 | 13 | 25 | 2 | 16 | 14 | 2 | 11 | 0.593 |
| 0.70 ⭐ | 27 | 14 | 13 | 23 | 4 | 18 | 14 | 4 | 9 | 0.667 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 27
- **True AD**: 14 | **True Control**: 13
- **Predicted as AD**: 23 (85.2%)
- **Predicted as Control**: 4 (14.8%)
- **Correctly Classified**: 18 out of 27 (66.7%)
  - Correct AD: 14 out of 14 (100.0%)
  - Correct Control: 4 out of 13 (30.8%)
- **Incorrectly Classified**: 9 (33.3%)
  - AD → Control: 0
  - Control → AD: 9

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 26 | 12 | 14 | 24 | 2 | 14 | 12 | 2 | 12 | 0.538 |
| 0.55 | 26 | 12 | 14 | 24 | 2 | 14 | 12 | 2 | 12 | 0.538 |
| 0.60 ⭐ | 26 | 12 | 14 | 23 | 3 | 15 | 12 | 3 | 11 | 0.577 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 26
- **True AD**: 12 | **True Control**: 14
- **Predicted as AD**: 23 (88.5%)
- **Predicted as Control**: 3 (11.5%)
- **Correctly Classified**: 15 out of 26 (57.7%)
  - Correct AD: 12 out of 12 (100.0%)
  - Correct Control: 3 out of 14 (21.4%)
- **Incorrectly Classified**: 11 (42.3%)
  - AD → Control: 0
  - Control → AD: 11

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 32 | 15 | 17 | 25 | 7 | 18 | 13 | 5 | 14 | 0.562 |
| 0.55 | 32 | 15 | 17 | 24 | 8 | 17 | 12 | 5 | 15 | 0.531 |
| 0.60 | 32 | 15 | 17 | 22 | 10 | 19 | 12 | 7 | 13 | 0.594 |
| 0.70 ⭐ | 32 | 15 | 17 | 21 | 11 | 20 | 12 | 8 | 12 | 0.625 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 32
- **True AD**: 15 | **True Control**: 17
- **Predicted as AD**: 21 (65.6%)
- **Predicted as Control**: 11 (34.4%)
- **Correctly Classified**: 20 out of 32 (62.5%)
  - Correct AD: 12 out of 15 (80.0%)
  - Correct Control: 8 out of 17 (47.1%)
- **Incorrectly Classified**: 12 (37.5%)
  - AD → Control: 3
  - Control → AD: 9

---

## PCA_L_6

### KNN

#### KNN (n_neighbors=1)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 49 | 24 | 25 | 5 | 44 | 26 | 3 | 23 | 23 | 0.531 |
| 0.50 | 49 | 24 | 25 | 4 | 45 | 25 | 2 | 23 | 24 | 0.510 |
| 0.55 | 49 | 24 | 25 | 4 | 45 | 25 | 2 | 23 | 24 | 0.510 |
| 0.60 | 49 | 24 | 25 | 4 | 45 | 25 | 2 | 23 | 24 | 0.510 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 49
- **True AD**: 24 | **True Control**: 25
- **Predicted as AD**: 5 (10.2%)
- **Predicted as Control**: 44 (89.8%)
- **Correctly Classified**: 26 out of 49 (53.1%)
  - Correct AD: 3 out of 24 (12.5%)
  - Correct Control: 23 out of 25 (92.0%)
- **Incorrectly Classified**: 23 (46.9%)
  - AD → Control: 21
  - Control → AD: 2

---

#### KNN (n_neighbors=15)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 47 | 23 | 24 | 15 | 32 | 25 | 8 | 17 | 22 | 0.532 |
| 0.55 | 47 | 23 | 24 | 12 | 35 | 26 | 7 | 19 | 21 | 0.553 |
| 0.60 ⭐ | 47 | 23 | 24 | 11 | 36 | 27 | 7 | 20 | 20 | 0.574 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 47
- **True AD**: 23 | **True Control**: 24
- **Predicted as AD**: 11 (23.4%)
- **Predicted as Control**: 36 (76.6%)
- **Correctly Classified**: 27 out of 47 (57.4%)
  - Correct AD: 7 out of 23 (30.4%)
  - Correct Control: 20 out of 24 (83.3%)
- **Incorrectly Classified**: 20 (42.6%)
  - AD → Control: 16
  - Control → AD: 4

---

#### KNN (n_neighbors=7)

**Optimal Threshold: 0.55**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 55 | 28 | 27 | 20 | 35 | 33 | 13 | 20 | 22 | 0.600 |
| 0.55 ⭐ | 55 | 28 | 27 | 18 | 37 | 35 | 13 | 22 | 20 | 0.636 |
| 0.60 | 55 | 28 | 27 | 14 | 41 | 35 | 11 | 24 | 20 | 0.636 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 55
- **True AD**: 28 | **True Control**: 27
- **Predicted as AD**: 18 (32.7%)
- **Predicted as Control**: 37 (67.3%)
- **Correctly Classified**: 35 out of 55 (63.6%)
  - Correct AD: 13 out of 28 (46.4%)
  - Correct Control: 22 out of 27 (81.5%)
- **Incorrectly Classified**: 20 (36.4%)
  - AD → Control: 15
  - Control → AD: 5

---

### MLP

#### MLP (hidden=100)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 58 | 32 | 26 | 57 | 1 | 31 | 31 | 0 | 27 | 0.534 |
| 0.55 | 58 | 32 | 26 | 56 | 2 | 32 | 31 | 1 | 26 | 0.552 |
| 0.60 | 58 | 32 | 26 | 54 | 4 | 34 | 31 | 3 | 24 | 0.586 |
| 0.65 ⭐ | 58 | 32 | 26 | 51 | 7 | 37 | 31 | 6 | 21 | 0.638 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 58
- **True AD**: 32 | **True Control**: 26
- **Predicted as AD**: 51 (87.9%)
- **Predicted as Control**: 7 (12.1%)
- **Correctly Classified**: 37 out of 58 (63.8%)
  - Correct AD: 31 out of 32 (96.9%)
  - Correct Control: 6 out of 26 (23.1%)
- **Incorrectly Classified**: 21 (36.2%)
  - AD → Control: 1
  - Control → AD: 20

---

#### MLP (hidden=150_50)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 45 | 23 | 22 | 40 | 5 | 24 | 21 | 3 | 21 | 0.533 |
| 0.55 | 45 | 23 | 22 | 39 | 6 | 25 | 21 | 4 | 20 | 0.556 |
| 0.60 ⭐ | 45 | 23 | 22 | 38 | 7 | 26 | 21 | 5 | 19 | 0.578 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 45
- **True AD**: 23 | **True Control**: 22
- **Predicted as AD**: 38 (84.4%)
- **Predicted as Control**: 7 (15.6%)
- **Correctly Classified**: 26 out of 45 (57.8%)
  - Correct AD: 21 out of 23 (91.3%)
  - Correct Control: 5 out of 22 (22.7%)
- **Incorrectly Classified**: 19 (42.2%)
  - AD → Control: 2
  - Control → AD: 17

---

#### MLP (hidden=200_100_50)

**Optimal Threshold: 0.65**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 58 | 31 | 27 | 48 | 10 | 31 | 26 | 5 | 27 | 0.534 |
| 0.55 | 58 | 31 | 27 | 44 | 14 | 31 | 24 | 7 | 27 | 0.534 |
| 0.60 | 58 | 31 | 27 | 43 | 15 | 32 | 24 | 8 | 26 | 0.552 |
| 0.65 ⭐ | 58 | 31 | 27 | 40 | 18 | 33 | 23 | 10 | 25 | 0.569 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 58
- **True AD**: 31 | **True Control**: 27
- **Predicted as AD**: 40 (69.0%)
- **Predicted as Control**: 18 (31.0%)
- **Correctly Classified**: 33 out of 58 (56.9%)
  - Correct AD: 23 out of 31 (74.2%)
  - Correct Control: 10 out of 27 (37.0%)
- **Incorrectly Classified**: 25 (43.1%)
  - AD → Control: 8
  - Control → AD: 17

---

### SVM

#### SVM (kernel=linear)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 52 | 29 | 23 | 52 | 0 | 29 | 29 | 0 | 23 | 0.558 |
| 0.55 | 52 | 29 | 23 | 52 | 0 | 29 | 29 | 0 | 23 | 0.558 |
| 0.60 | 52 | 29 | 23 | 52 | 0 | 29 | 29 | 0 | 23 | 0.558 |
| 0.70 ⭐ | 52 | 29 | 23 | 51 | 1 | 30 | 29 | 1 | 22 | 0.577 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 52
- **True AD**: 29 | **True Control**: 23
- **Predicted as AD**: 51 (98.1%)
- **Predicted as Control**: 1 (1.9%)
- **Correctly Classified**: 30 out of 52 (57.7%)
  - Correct AD: 29 out of 29 (100.0%)
  - Correct Control: 1 out of 23 (4.3%)
- **Incorrectly Classified**: 22 (42.3%)
  - AD → Control: 0
  - Control → AD: 22

---

#### SVM (kernel=poly)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 54 | 29 | 25 | 54 | 0 | 29 | 29 | 0 | 25 | 0.537 |
| 0.50 | 54 | 29 | 25 | 54 | 0 | 29 | 29 | 0 | 25 | 0.537 |
| 0.55 | 54 | 29 | 25 | 54 | 0 | 29 | 29 | 0 | 25 | 0.537 |
| 0.60 | 54 | 29 | 25 | 54 | 0 | 29 | 29 | 0 | 25 | 0.537 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 54
- **True AD**: 29 | **True Control**: 25
- **Predicted as AD**: 54 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 29 out of 54 (53.7%)
  - Correct AD: 29 out of 29 (100.0%)
  - Correct Control: 0 out of 25 (0.0%)
- **Incorrectly Classified**: 25 (46.3%)
  - AD → Control: 0
  - Control → AD: 25

---

#### SVM (kernel=rbf)

**Optimal Threshold: 0.60**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 53 | 28 | 25 | 50 | 3 | 31 | 28 | 3 | 22 | 0.585 |
| 0.55 | 53 | 28 | 25 | 50 | 3 | 31 | 28 | 3 | 22 | 0.585 |
| 0.60 ⭐ | 53 | 28 | 25 | 47 | 6 | 34 | 28 | 6 | 19 | 0.642 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 53
- **True AD**: 28 | **True Control**: 25
- **Predicted as AD**: 47 (88.7%)
- **Predicted as Control**: 6 (11.3%)
- **Correctly Classified**: 34 out of 53 (64.2%)
  - Correct AD: 28 out of 28 (100.0%)
  - Correct Control: 6 out of 25 (24.0%)
- **Incorrectly Classified**: 19 (35.8%)
  - AD → Control: 0
  - Control → AD: 19

---

### XGBoost

#### XGBoost (max_depth=3)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 50 | 28 | 22 | 50 | 0 | 28 | 28 | 0 | 22 | 0.560 |
| 0.50 | 50 | 28 | 22 | 50 | 0 | 28 | 28 | 0 | 22 | 0.560 |
| 0.55 | 50 | 28 | 22 | 50 | 0 | 28 | 28 | 0 | 22 | 0.560 |
| 0.60 | 50 | 28 | 22 | 50 | 0 | 28 | 28 | 0 | 22 | 0.560 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 50
- **True AD**: 28 | **True Control**: 22
- **Predicted as AD**: 50 (100.0%)
- **Predicted as Control**: 0 (0.0%)
- **Correctly Classified**: 28 out of 50 (56.0%)
  - Correct AD: 28 out of 28 (100.0%)
  - Correct Control: 0 out of 22 (0.0%)
- **Incorrectly Classified**: 22 (44.0%)
  - AD → Control: 0
  - Control → AD: 22

---

#### XGBoost (max_depth=6)

**Optimal Threshold: 0.70**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.50 | 60 | 34 | 26 | 54 | 6 | 36 | 32 | 4 | 24 | 0.600 |
| 0.55 | 60 | 34 | 26 | 52 | 8 | 34 | 30 | 4 | 26 | 0.567 |
| 0.60 | 60 | 34 | 26 | 50 | 10 | 36 | 30 | 6 | 24 | 0.600 |
| 0.70 ⭐ | 60 | 34 | 26 | 42 | 18 | 40 | 28 | 12 | 20 | 0.667 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 60
- **True AD**: 34 | **True Control**: 26
- **Predicted as AD**: 42 (70.0%)
- **Predicted as Control**: 18 (30.0%)
- **Correctly Classified**: 40 out of 60 (66.7%)
  - Correct AD: 28 out of 34 (82.4%)
  - Correct Control: 12 out of 26 (46.2%)
- **Incorrectly Classified**: 20 (33.3%)
  - AD → Control: 6
  - Control → AD: 14

---

#### XGBoost (max_depth=9)

**Optimal Threshold: 0.30**

| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |
|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|
| 0.30 ⭐ | 47 | 25 | 22 | 38 | 9 | 30 | 23 | 7 | 17 | 0.638 |
| 0.50 | 47 | 25 | 22 | 28 | 19 | 28 | 17 | 11 | 19 | 0.596 |
| 0.55 | 47 | 25 | 22 | 24 | 23 | 24 | 13 | 11 | 23 | 0.511 |
| 0.60 | 47 | 25 | 22 | 23 | 24 | 25 | 13 | 12 | 22 | 0.532 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 47
- **True AD**: 25 | **True Control**: 22
- **Predicted as AD**: 38 (80.9%)
- **Predicted as Control**: 9 (19.1%)
- **Correctly Classified**: 30 out of 47 (63.8%)
  - Correct AD: 23 out of 25 (92.0%)
  - Correct Control: 7 out of 22 (31.8%)
- **Incorrectly Classified**: 17 (36.2%)
  - AD → Control: 2
  - Control → AD: 15

---

## 📋 Summary: Optimal Thresholds by Model×Hyperparameter

| Experiment | Model×Hyperparameters | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |
|------------|------------------------|-------------------|----------------|---------|-----------|----------|
| ANOVA_L_2 | KNN_n_neighbors=1 | 0.40 | 25 | 22 | 3 | 0.880 |
| ANOVA_L_2 | KNN_n_neighbors=15 | 0.45 | 18 | 16 | 2 | 0.889 |
| ANOVA_L_2 | KNN_n_neighbors=7 | 0.40 | 28 | 26 | 2 | 0.929 |
| ANOVA_L_2 | MLP_hidden=100 | 0.60 | 27 | 23 | 4 | 0.852 |
| ANOVA_L_2 | MLP_hidden=150_50 | 0.55 | 21 | 19 | 2 | 0.905 |
| ANOVA_L_2 | MLP_hidden=200_100_50 | 0.50 | 12 | 10 | 2 | 0.833 |
| ANOVA_L_2 | SVM_kernel=linear | 0.65 | 23 | 20 | 3 | 0.870 |
| ANOVA_L_2 | SVM_kernel=poly | 0.55 | 33 | 23 | 10 | 0.697 |
| ANOVA_L_2 | SVM_kernel=rbf | 0.60 | 30 | 26 | 4 | 0.867 |
| ANOVA_L_2 | XGBoost_max_depth=3 | 0.70 | 34 | 28 | 6 | 0.824 |
| ANOVA_L_2 | XGBoost_max_depth=6 | 0.50 | 25 | 22 | 3 | 0.880 |
| ANOVA_L_2 | XGBoost_max_depth=9 | 0.55 | 22 | 20 | 2 | 0.909 |
| ANOVA_L_6 | KNN_n_neighbors=1 | 0.55 | 61 | 52 | 9 | 0.852 |
| ANOVA_L_6 | KNN_n_neighbors=15 | 0.55 | 50 | 43 | 7 | 0.860 |
| ANOVA_L_6 | KNN_n_neighbors=7 | 0.50 | 58 | 50 | 8 | 0.862 |
| ANOVA_L_6 | MLP_hidden=100 | 0.50 | 47 | 40 | 7 | 0.851 |
| ANOVA_L_6 | MLP_hidden=150_50 | 0.50 | 42 | 35 | 7 | 0.833 |
| ANOVA_L_6 | MLP_hidden=200_100_50 | 0.65 | 35 | 31 | 4 | 0.886 |
| ANOVA_L_6 | SVM_kernel=linear | 0.55 | 47 | 40 | 7 | 0.851 |
| ANOVA_L_6 | SVM_kernel=poly | 0.60 | 61 | 46 | 15 | 0.754 |
| ANOVA_L_6 | SVM_kernel=rbf | 0.60 | 51 | 40 | 11 | 0.784 |
| ANOVA_L_6 | XGBoost_max_depth=3 | 0.65 | 40 | 34 | 6 | 0.850 |
| ANOVA_L_6 | XGBoost_max_depth=6 | 0.70 | 51 | 43 | 8 | 0.843 |
| ANOVA_L_6 | XGBoost_max_depth=9 | 0.50 | 60 | 49 | 11 | 0.817 |
| PCA_L_2 | KNN_n_neighbors=1 | 0.30 | 23 | 12 | 11 | 0.522 |
| PCA_L_2 | KNN_n_neighbors=15 | 0.30 | 28 | 18 | 10 | 0.643 |
| PCA_L_2 | KNN_n_neighbors=7 | 0.30 | 30 | 21 | 9 | 0.700 |
| PCA_L_2 | MLP_hidden=100 | 0.30 | 30 | 16 | 14 | 0.533 |
| PCA_L_2 | MLP_hidden=150_50 | 0.30 | 24 | 12 | 12 | 0.500 |
| PCA_L_2 | MLP_hidden=200_100_50 | 0.65 | 23 | 13 | 10 | 0.565 |
| PCA_L_2 | SVM_kernel=linear | 0.30 | 27 | 13 | 14 | 0.481 |
| PCA_L_2 | SVM_kernel=poly | 0.30 | 24 | 11 | 13 | 0.458 |
| PCA_L_2 | SVM_kernel=rbf | 0.65 | 25 | 17 | 8 | 0.680 |
| PCA_L_2 | XGBoost_max_depth=3 | 0.70 | 27 | 18 | 9 | 0.667 |
| PCA_L_2 | XGBoost_max_depth=6 | 0.60 | 26 | 15 | 11 | 0.577 |
| PCA_L_2 | XGBoost_max_depth=9 | 0.70 | 32 | 20 | 12 | 0.625 |
| PCA_L_6 | KNN_n_neighbors=1 | 0.30 | 49 | 26 | 23 | 0.531 |
| PCA_L_6 | KNN_n_neighbors=15 | 0.60 | 47 | 27 | 20 | 0.574 |
| PCA_L_6 | KNN_n_neighbors=7 | 0.55 | 55 | 35 | 20 | 0.636 |
| PCA_L_6 | MLP_hidden=100 | 0.65 | 58 | 37 | 21 | 0.638 |
| PCA_L_6 | MLP_hidden=150_50 | 0.60 | 45 | 26 | 19 | 0.578 |
| PCA_L_6 | MLP_hidden=200_100_50 | 0.65 | 58 | 33 | 25 | 0.569 |
| PCA_L_6 | SVM_kernel=linear | 0.70 | 52 | 30 | 22 | 0.577 |
| PCA_L_6 | SVM_kernel=poly | 0.30 | 54 | 29 | 25 | 0.537 |
| PCA_L_6 | SVM_kernel=rbf | 0.60 | 53 | 34 | 19 | 0.642 |
| PCA_L_6 | XGBoost_max_depth=3 | 0.30 | 50 | 28 | 22 | 0.560 |
| PCA_L_6 | XGBoost_max_depth=6 | 0.70 | 60 | 40 | 20 | 0.667 |
| PCA_L_6 | XGBoost_max_depth=9 | 0.30 | 47 | 30 | 17 | 0.638 |

## 🎯 KNN-Specific Summary

| Experiment | KNN Hyperparameters | Threshold | Total | Correct | Accuracy |
|----------------|-------------|-----------|-------|---------|----------|
| ANOVA_L_2 | n_neighbors=1 | 0.40 | 25 | 22 | 0.880 |
| ANOVA_L_2 | n_neighbors=15 | 0.45 | 18 | 16 | 0.889 |
| ANOVA_L_2 | n_neighbors=7 | 0.40 | 28 | 26 | 0.929 |
| ANOVA_L_6 | n_neighbors=1 | 0.55 | 61 | 52 | 0.852 |
| ANOVA_L_6 | n_neighbors=15 | 0.55 | 50 | 43 | 0.860 |
| ANOVA_L_6 | n_neighbors=7 | 0.50 | 58 | 50 | 0.862 |
| PCA_L_2 | n_neighbors=1 | 0.30 | 23 | 12 | 0.522 |
| PCA_L_2 | n_neighbors=15 | 0.30 | 28 | 18 | 0.643 |
| PCA_L_2 | n_neighbors=7 | 0.30 | 30 | 21 | 0.700 |
| PCA_L_6 | n_neighbors=1 | 0.30 | 49 | 26 | 0.531 |
| PCA_L_6 | n_neighbors=15 | 0.60 | 47 | 27 | 0.574 |
| PCA_L_6 | n_neighbors=7 | 0.55 | 55 | 35 | 0.636 |

---
*Analysis completed: 2025-12-12 21:05*
*Each model×hyperparameter combination analyzed separately*
