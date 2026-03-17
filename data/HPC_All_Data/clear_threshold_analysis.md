# 📊 Clear Threshold Analysis - Per Subject Classification Results

## Analysis Overview

This analysis shows **actual numbers** of subjects classified and correctly classified for each threshold.
The threshold is chosen **per model × experiment** based on overall accuracy, NOT using per-subject information.

## 📈 Results by Experiment and Model

## ANOVA_L_2

### KNN

**Optimal Threshold: 0.45**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.45 ⭐ | 43 | 21 | 22 | 21 | 22 | 39 | 19 | 20 | 4 | 0.907 |
| 0.50 | 43 | 21 | 22 | 21 | 22 | 39 | 19 | 20 | 4 | 0.907 |
| 0.55 | 43 | 21 | 22 | 20 | 23 | 38 | 18 | 20 | 5 | 0.884 |
| 0.60 | 43 | 21 | 22 | 18 | 25 | 36 | 16 | 20 | 7 | 0.837 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 43
- **True AD Subjects**: 21
- **True Control Subjects**: 22

- **Predicted as AD**: 21 (48.8%)
- **Predicted as Control**: 22 (51.2%)

- **Correctly Classified**: 39 (90.7%)
  - Correct AD: 19 out of 21 true AD (90.5%)
  - Correct Control: 20 out of 22 true Control (90.9%)

- **Incorrectly Classified**: 4 (9.3%)
  - AD misclassified as Control: 2
  - Control misclassified as AD: 2

---

### XGBoost

**Optimal Threshold: 0.55**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 43 | 21 | 22 | 23 | 20 | 35 | 18 | 17 | 8 | 0.814 |
| 0.55 ⭐ | 43 | 21 | 22 | 21 | 22 | 37 | 18 | 19 | 6 | 0.860 |
| 0.60 | 43 | 21 | 22 | 18 | 25 | 34 | 15 | 19 | 9 | 0.791 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 43
- **True AD Subjects**: 21
- **True Control Subjects**: 22

- **Predicted as AD**: 21 (48.8%)
- **Predicted as Control**: 22 (51.2%)

- **Correctly Classified**: 37 (86.0%)
  - Correct AD: 18 out of 21 true AD (85.7%)
  - Correct Control: 19 out of 22 true Control (86.4%)

- **Incorrectly Classified**: 6 (14.0%)
  - AD misclassified as Control: 3
  - Control misclassified as AD: 3

---

### SVM

**Optimal Threshold: 0.45**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.45 ⭐ | 40 | 21 | 19 | 30 | 10 | 31 | 21 | 10 | 9 | 0.775 |
| 0.50 | 40 | 21 | 19 | 29 | 11 | 30 | 20 | 10 | 10 | 0.750 |
| 0.55 | 40 | 21 | 19 | 28 | 12 | 31 | 20 | 11 | 9 | 0.775 |
| 0.60 | 40 | 21 | 19 | 26 | 14 | 31 | 19 | 12 | 9 | 0.775 |

**Detailed Breakdown at Optimal Threshold (0.45):**

- **Total Subjects**: 40
- **True AD Subjects**: 21
- **True Control Subjects**: 19

- **Predicted as AD**: 30 (75.0%)
- **Predicted as Control**: 10 (25.0%)

- **Correctly Classified**: 31 (77.5%)
  - Correct AD: 21 out of 21 true AD (100.0%)
  - Correct Control: 10 out of 19 true Control (52.6%)

- **Incorrectly Classified**: 9 (22.5%)
  - AD misclassified as Control: 0
  - Control misclassified as AD: 9

---

### MLP

**Optimal Threshold: 0.60**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 39 | 20 | 19 | 26 | 13 | 33 | 20 | 13 | 6 | 0.846 |
| 0.55 | 39 | 20 | 19 | 26 | 13 | 33 | 20 | 13 | 6 | 0.846 |
| 0.60 ⭐ | 39 | 20 | 19 | 25 | 14 | 34 | 20 | 14 | 5 | 0.872 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 39
- **True AD Subjects**: 20
- **True Control Subjects**: 19

- **Predicted as AD**: 25 (64.1%)
- **Predicted as Control**: 14 (35.9%)

- **Correctly Classified**: 34 (87.2%)
  - Correct AD: 20 out of 20 true AD (100.0%)
  - Correct Control: 14 out of 19 true Control (73.7%)

- **Incorrectly Classified**: 5 (12.8%)
  - AD misclassified as Control: 0
  - Control misclassified as AD: 5

---

## ANOVA_L_6

### XGBoost

**Optimal Threshold: 0.50**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 ⭐ | 64 | 35 | 29 | 41 | 23 | 50 | 31 | 19 | 14 | 0.781 |
| 0.55 | 64 | 35 | 29 | 36 | 28 | 47 | 27 | 20 | 17 | 0.734 |
| 0.60 | 64 | 35 | 29 | 32 | 32 | 49 | 26 | 23 | 15 | 0.766 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 64
- **True AD Subjects**: 35
- **True Control Subjects**: 29

- **Predicted as AD**: 41 (64.1%)
- **Predicted as Control**: 23 (35.9%)

- **Correctly Classified**: 50 (78.1%)
  - Correct AD: 31 out of 35 true AD (88.6%)
  - Correct Control: 19 out of 29 true Control (65.5%)

- **Incorrectly Classified**: 14 (21.9%)
  - AD misclassified as Control: 4
  - Control misclassified as AD: 10

---

### SVM

**Optimal Threshold: 0.55**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 63 | 35 | 28 | 47 | 16 | 47 | 33 | 14 | 16 | 0.746 |
| 0.55 ⭐ | 63 | 35 | 28 | 44 | 19 | 50 | 33 | 17 | 13 | 0.794 |
| 0.60 | 63 | 35 | 28 | 42 | 21 | 48 | 31 | 17 | 15 | 0.762 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 63
- **True AD Subjects**: 35
- **True Control Subjects**: 28

- **Predicted as AD**: 44 (69.8%)
- **Predicted as Control**: 19 (30.2%)

- **Correctly Classified**: 50 (79.4%)
  - Correct AD: 33 out of 35 true AD (94.3%)
  - Correct Control: 17 out of 28 true Control (60.7%)

- **Incorrectly Classified**: 13 (20.6%)
  - AD misclassified as Control: 2
  - Control misclassified as AD: 11

---

### KNN

**Optimal Threshold: 0.50**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 ⭐ | 64 | 35 | 29 | 36 | 28 | 55 | 31 | 24 | 9 | 0.859 |
| 0.55 | 64 | 35 | 29 | 35 | 29 | 54 | 30 | 24 | 10 | 0.844 |
| 0.60 | 64 | 35 | 29 | 31 | 33 | 54 | 28 | 26 | 10 | 0.844 |

**Detailed Breakdown at Optimal Threshold (0.50):**

- **Total Subjects**: 64
- **True AD Subjects**: 35
- **True Control Subjects**: 29

- **Predicted as AD**: 36 (56.2%)
- **Predicted as Control**: 28 (43.8%)

- **Correctly Classified**: 55 (85.9%)
  - Correct AD: 31 out of 35 true AD (88.6%)
  - Correct Control: 24 out of 29 true Control (82.8%)

- **Incorrectly Classified**: 9 (14.1%)
  - AD misclassified as Control: 4
  - Control misclassified as AD: 5

---

### MLP

**Optimal Threshold: 0.55**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 60 | 32 | 28 | 34 | 26 | 50 | 28 | 22 | 10 | 0.833 |
| 0.55 ⭐ | 60 | 32 | 28 | 33 | 27 | 51 | 28 | 23 | 9 | 0.850 |
| 0.60 | 60 | 32 | 28 | 30 | 30 | 50 | 26 | 24 | 10 | 0.833 |

**Detailed Breakdown at Optimal Threshold (0.55):**

- **Total Subjects**: 60
- **True AD Subjects**: 32
- **True Control Subjects**: 28

- **Predicted as AD**: 33 (55.0%)
- **Predicted as Control**: 27 (45.0%)

- **Correctly Classified**: 51 (85.0%)
  - Correct AD: 28 out of 32 true AD (87.5%)
  - Correct Control: 23 out of 28 true Control (82.1%)

- **Incorrectly Classified**: 9 (15.0%)
  - AD misclassified as Control: 4
  - Control misclassified as AD: 5

---

## PCA_L_2

### KNN

**Optimal Threshold: 0.35**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.35 ⭐ | 48 | 25 | 23 | 7 | 41 | 26 | 5 | 21 | 22 | 0.542 |
| 0.50 | 48 | 25 | 23 | 4 | 44 | 25 | 3 | 22 | 23 | 0.521 |
| 0.55 | 48 | 25 | 23 | 4 | 44 | 25 | 3 | 22 | 23 | 0.521 |
| 0.60 | 48 | 25 | 23 | 2 | 46 | 23 | 1 | 22 | 25 | 0.479 |

**Detailed Breakdown at Optimal Threshold (0.35):**

- **Total Subjects**: 48
- **True AD Subjects**: 25
- **True Control Subjects**: 23

- **Predicted as AD**: 7 (14.6%)
- **Predicted as Control**: 41 (85.4%)

- **Correctly Classified**: 26 (54.2%)
  - Correct AD: 5 out of 25 true AD (20.0%)
  - Correct Control: 21 out of 23 true Control (91.3%)

- **Incorrectly Classified**: 22 (45.8%)
  - AD misclassified as Control: 20
  - Control misclassified as AD: 2

---

### MLP

**Optimal Threshold: 0.30**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.30 ⭐ | 40 | 20 | 20 | 40 | 0 | 20 | 20 | 0 | 20 | 0.500 |
| 0.50 | 40 | 20 | 20 | 40 | 0 | 20 | 20 | 0 | 20 | 0.500 |
| 0.55 | 40 | 20 | 20 | 40 | 0 | 20 | 20 | 0 | 20 | 0.500 |
| 0.60 | 40 | 20 | 20 | 40 | 0 | 20 | 20 | 0 | 20 | 0.500 |

**Detailed Breakdown at Optimal Threshold (0.30):**

- **Total Subjects**: 40
- **True AD Subjects**: 20
- **True Control Subjects**: 20

- **Predicted as AD**: 40 (100.0%)
- **Predicted as Control**: 0 (0.0%)

- **Correctly Classified**: 20 (50.0%)
  - Correct AD: 20 out of 20 true AD (100.0%)
  - Correct Control: 0 out of 20 true Control (0.0%)

- **Incorrectly Classified**: 20 (50.0%)
  - AD misclassified as Control: 0
  - Control misclassified as AD: 20

---

### XGBoost

**Optimal Threshold: 0.70**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 43 | 23 | 20 | 42 | 1 | 22 | 22 | 0 | 21 | 0.512 |
| 0.55 | 43 | 23 | 20 | 42 | 1 | 22 | 22 | 0 | 21 | 0.512 |
| 0.60 | 43 | 23 | 20 | 41 | 2 | 23 | 22 | 1 | 20 | 0.535 |
| 0.70 ⭐ | 43 | 23 | 20 | 37 | 6 | 27 | 22 | 5 | 16 | 0.628 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 43
- **True AD Subjects**: 23
- **True Control Subjects**: 20

- **Predicted as AD**: 37 (86.0%)
- **Predicted as Control**: 6 (14.0%)

- **Correctly Classified**: 27 (62.8%)
  - Correct AD: 22 out of 23 true AD (95.7%)
  - Correct Control: 5 out of 20 true Control (25.0%)

- **Incorrectly Classified**: 16 (37.2%)
  - AD misclassified as Control: 1
  - Control misclassified as AD: 15

---

### SVM

**Optimal Threshold: 0.60**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 38 | 20 | 18 | 38 | 0 | 20 | 20 | 0 | 18 | 0.526 |
| 0.55 | 38 | 20 | 18 | 38 | 0 | 20 | 20 | 0 | 18 | 0.526 |
| 0.60 ⭐ | 38 | 20 | 18 | 37 | 1 | 21 | 20 | 1 | 17 | 0.553 |

**Detailed Breakdown at Optimal Threshold (0.60):**

- **Total Subjects**: 38
- **True AD Subjects**: 20
- **True Control Subjects**: 18

- **Predicted as AD**: 37 (97.4%)
- **Predicted as Control**: 1 (2.6%)

- **Correctly Classified**: 21 (55.3%)
  - Correct AD: 20 out of 20 true AD (100.0%)
  - Correct Control: 1 out of 18 true Control (5.6%)

- **Incorrectly Classified**: 17 (44.7%)
  - AD misclassified as Control: 0
  - Control misclassified as AD: 17

---

## PCA_L_6

### SVM

**Optimal Threshold: 0.65**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.55 | 65 | 36 | 29 | 65 | 0 | 36 | 36 | 0 | 29 | 0.554 |
| 0.60 | 65 | 36 | 29 | 64 | 1 | 37 | 36 | 1 | 28 | 0.569 |
| 0.65 ⭐ | 65 | 36 | 29 | 63 | 2 | 38 | 36 | 2 | 27 | 0.585 |

**Detailed Breakdown at Optimal Threshold (0.65):**

- **Total Subjects**: 65
- **True AD Subjects**: 36
- **True Control Subjects**: 29

- **Predicted as AD**: 63 (96.9%)
- **Predicted as Control**: 2 (3.1%)

- **Correctly Classified**: 38 (58.5%)
  - Correct AD: 36 out of 36 true AD (100.0%)
  - Correct Control: 2 out of 29 true Control (6.9%)

- **Incorrectly Classified**: 27 (41.5%)
  - AD misclassified as Control: 0
  - Control misclassified as AD: 27

---

### MLP

**Optimal Threshold: 0.70**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 63 | 34 | 29 | 58 | 5 | 37 | 33 | 4 | 26 | 0.587 |
| 0.55 | 63 | 34 | 29 | 54 | 9 | 37 | 31 | 6 | 26 | 0.587 |
| 0.60 | 63 | 34 | 29 | 50 | 13 | 39 | 30 | 9 | 24 | 0.619 |
| 0.70 ⭐ | 63 | 34 | 29 | 47 | 16 | 40 | 29 | 11 | 23 | 0.635 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 63
- **True AD Subjects**: 34
- **True Control Subjects**: 29

- **Predicted as AD**: 47 (74.6%)
- **Predicted as Control**: 16 (25.4%)

- **Correctly Classified**: 40 (63.5%)
  - Correct AD: 29 out of 34 true AD (85.3%)
  - Correct Control: 11 out of 29 true Control (37.9%)

- **Incorrectly Classified**: 23 (36.5%)
  - AD misclassified as Control: 5
  - Control misclassified as AD: 18

---

### KNN

**Optimal Threshold: 0.40**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.40 ⭐ | 62 | 34 | 28 | 13 | 49 | 35 | 10 | 25 | 27 | 0.565 |
| 0.50 | 62 | 34 | 28 | 10 | 52 | 34 | 8 | 26 | 28 | 0.548 |
| 0.55 | 62 | 34 | 28 | 8 | 54 | 32 | 6 | 26 | 30 | 0.516 |
| 0.60 | 62 | 34 | 28 | 5 | 57 | 31 | 4 | 27 | 31 | 0.500 |

**Detailed Breakdown at Optimal Threshold (0.40):**

- **Total Subjects**: 62
- **True AD Subjects**: 34
- **True Control Subjects**: 28

- **Predicted as AD**: 13 (21.0%)
- **Predicted as Control**: 49 (79.0%)

- **Correctly Classified**: 35 (56.5%)
  - Correct AD: 10 out of 34 true AD (29.4%)
  - Correct Control: 25 out of 28 true Control (89.3%)

- **Incorrectly Classified**: 27 (43.5%)
  - AD misclassified as Control: 24
  - Control misclassified as AD: 3

---

### XGBoost

**Optimal Threshold: 0.70**

| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |
|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|
| 0.50 | 65 | 36 | 29 | 62 | 3 | 37 | 35 | 2 | 28 | 0.569 |
| 0.55 | 65 | 36 | 29 | 62 | 3 | 37 | 35 | 2 | 28 | 0.569 |
| 0.60 | 65 | 36 | 29 | 61 | 4 | 38 | 35 | 3 | 27 | 0.585 |
| 0.70 ⭐ | 65 | 36 | 29 | 52 | 13 | 45 | 34 | 11 | 20 | 0.692 |

**Detailed Breakdown at Optimal Threshold (0.70):**

- **Total Subjects**: 65
- **True AD Subjects**: 36
- **True Control Subjects**: 29

- **Predicted as AD**: 52 (80.0%)
- **Predicted as Control**: 13 (20.0%)

- **Correctly Classified**: 45 (69.2%)
  - Correct AD: 34 out of 36 true AD (94.4%)
  - Correct Control: 11 out of 29 true Control (37.9%)

- **Incorrectly Classified**: 20 (30.8%)
  - AD misclassified as Control: 2
  - Control misclassified as AD: 18

---

## 📋 Summary: Optimal Thresholds by Model × Experiment

| Experiment | Model | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |
|------------|-------|-------------------|----------------|---------|-----------|----------|
| ANOVA_L_2 | KNN | 0.45 | 43 | 39 | 4 | 0.907 |
| ANOVA_L_2 | XGBoost | 0.55 | 43 | 37 | 6 | 0.860 |
| ANOVA_L_2 | SVM | 0.45 | 40 | 31 | 9 | 0.775 |
| ANOVA_L_2 | MLP | 0.60 | 39 | 34 | 5 | 0.872 |
| ANOVA_L_6 | XGBoost | 0.50 | 64 | 50 | 14 | 0.781 |
| ANOVA_L_6 | SVM | 0.55 | 63 | 50 | 13 | 0.794 |
| ANOVA_L_6 | KNN | 0.50 | 64 | 55 | 9 | 0.859 |
| ANOVA_L_6 | MLP | 0.55 | 60 | 51 | 9 | 0.850 |
| PCA_L_2 | KNN | 0.35 | 48 | 26 | 22 | 0.542 |
| PCA_L_2 | MLP | 0.30 | 40 | 20 | 20 | 0.500 |
| PCA_L_2 | XGBoost | 0.70 | 43 | 27 | 16 | 0.628 |
| PCA_L_2 | SVM | 0.60 | 38 | 21 | 17 | 0.553 |
| PCA_L_6 | SVM | 0.65 | 65 | 38 | 27 | 0.585 |
| PCA_L_6 | MLP | 0.70 | 63 | 40 | 23 | 0.635 |
| PCA_L_6 | KNN | 0.40 | 62 | 35 | 27 | 0.565 |
| PCA_L_6 | XGBoost | 0.70 | 65 | 45 | 20 | 0.692 |

---
*Analysis completed: 2025-12-08 16:10*
*Threshold chosen per model × experiment based on overall accuracy*
