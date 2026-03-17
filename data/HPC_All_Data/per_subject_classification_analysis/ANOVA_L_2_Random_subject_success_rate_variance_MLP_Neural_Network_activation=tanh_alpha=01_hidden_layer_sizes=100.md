# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_2_Random

## Model×Hyperparameters: MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_layer_sizes=[100])


## Methods

This analysis examines how the variance of per-subject success rates (>50% accuracy) 
changes as we include more folds in the analysis.


**Methodology:**

1. For each subject, calculate the percentage of folds where that subject's accuracy > 50%

2. Calculate the variance of these percentages across all subjects

3. Repeat for different numbers of folds (1 to N folds)

4. For each number of folds, sample 30 random combinations to estimate variance


**Key Metrics:**

- **Variance**: How much subjects differ in their success rates

- **Mean Success Rate**: Average percentage of folds where subjects exceed 50% accuracy


## Results


| Number of Folds | Mean Variance | Std Dev of Variance | Mean Success Rate |

|----------------|---------------|---------------------|-------------------|

| 1 | 0.0667 | 0.1729 | 93.33% |

| 2 | 0.1083 | 0.1369 | 88.06% |

| 3 | 0.1444 | 0.0952 | 84.44% |

| 4 | 0.1317 | 0.0963 | 84.07% |

| 5 | 0.1211 | 0.0833 | 86.22% |

| 6 | 0.1243 | 0.0696 | 85.97% |

| 7 | 0.1183 | 0.0540 | 86.87% |

| 8 | 0.1271 | 0.0386 | 85.85% |

| 9 | 0.1089 | 0.0586 | 87.71% |

| 10 | 0.1064 | 0.0500 | 88.17% |

| 11 | 0.1212 | 0.0314 | 86.51% |

| 12 | 0.1176 | 0.0482 | 86.58% |

| 13 | 0.1045 | 0.0356 | 88.36% |

| 14 | 0.1195 | 0.0314 | 86.59% |

| 15 | 0.1086 | 0.0399 | 87.72% |

| 16 | 0.1197 | 0.0327 | 86.41% |

| 17 | 0.1143 | 0.0296 | 86.99% |

| 18 | 0.1272 | 0.0342 | 85.38% |

| 19 | 0.1244 | 0.0300 | 85.55% |

| 20 | 0.1223 | 0.0298 | 85.98% |

| 21 | 0.1198 | 0.0274 | 86.32% |

| 22 | 0.1110 | 0.0256 | 87.40% |

| 23 | 0.1215 | 0.0273 | 85.91% |

| 24 | 0.1178 | 0.0245 | 86.45% |

| 25 | 0.1190 | 0.0305 | 86.21% |

| 26 | 0.1204 | 0.0249 | 86.04% |

| 27 | 0.1223 | 0.0211 | 85.98% |

| 28 | 0.1179 | 0.0197 | 86.27% |

| 29 | 0.1126 | 0.0222 | 87.08% |

| 30 | 0.1214 | 0.0190 | 86.01% |

| 31 | 0.1202 | 0.0189 | 85.95% |

| 32 | 0.1153 | 0.0164 | 86.69% |

| 33 | 0.1205 | 0.0156 | 86.13% |

| 34 | 0.1178 | 0.0139 | 86.29% |

| 35 | 0.1159 | 0.0147 | 86.66% |

| 36 | 0.1160 | 0.0135 | 86.43% |

| 37 | 0.1176 | 0.0161 | 86.21% |

| 38 | 0.1133 | 0.0132 | 86.80% |

| 39 | 0.1160 | 0.0120 | 86.54% |

| 40 | 0.1151 | 0.0093 | 86.52% |

| 41 | 0.1162 | 0.0115 | 86.33% |

| 42 | 0.1151 | 0.0101 | 86.52% |

| 43 | 0.1123 | 0.0111 | 86.92% |

| 44 | 0.1143 | 0.0087 | 86.64% |

| 45 | 0.1133 | 0.0089 | 86.72% |

| 46 | 0.1130 | 0.0058 | 86.66% |

| 47 | 0.1122 | 0.0077 | 86.84% |

| 48 | 0.1133 | 0.0038 | 86.68% |

| 49 | 0.1123 | 0.0029 | 86.75% |

| 50 | 0.1122 | 0.0000 | 86.73% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.0667 at 1 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1122

- Mean Success Rate: 86.73%
