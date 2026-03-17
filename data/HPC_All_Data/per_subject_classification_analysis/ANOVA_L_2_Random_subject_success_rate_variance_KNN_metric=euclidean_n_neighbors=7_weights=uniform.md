# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_2_Random

## Model×Hyperparameters: KNN (metric=euclidean, n_neighbors=7, weights=uniform)


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

| 1 | 0.1667 | 0.2397 | 83.33% |

| 2 | 0.0861 | 0.1247 | 90.83% |

| 3 | 0.1011 | 0.1004 | 89.33% |

| 4 | 0.0760 | 0.0811 | 92.04% |

| 5 | 0.0880 | 0.0793 | 90.47% |

| 6 | 0.0809 | 0.0678 | 91.30% |

| 7 | 0.1082 | 0.0547 | 88.20% |

| 8 | 0.1058 | 0.0533 | 88.43% |

| 9 | 0.1039 | 0.0540 | 88.55% |

| 10 | 0.0957 | 0.0544 | 89.50% |

| 11 | 0.1086 | 0.0322 | 88.19% |

| 12 | 0.0844 | 0.0443 | 90.87% |

| 13 | 0.0949 | 0.0370 | 89.71% |

| 14 | 0.0905 | 0.0304 | 90.28% |

| 15 | 0.0941 | 0.0390 | 89.71% |

| 16 | 0.0924 | 0.0278 | 90.04% |

| 17 | 0.0968 | 0.0347 | 89.39% |

| 18 | 0.0935 | 0.0258 | 89.87% |

| 19 | 0.1025 | 0.0321 | 88.69% |

| 20 | 0.0785 | 0.0311 | 91.58% |

| 21 | 0.0926 | 0.0294 | 89.90% |

| 22 | 0.1001 | 0.0246 | 89.00% |

| 23 | 0.0983 | 0.0170 | 89.29% |

| 24 | 0.0923 | 0.0244 | 89.95% |

| 25 | 0.0966 | 0.0277 | 89.39% |

| 26 | 0.0948 | 0.0202 | 89.66% |

| 27 | 0.1005 | 0.0176 | 88.97% |

| 28 | 0.0849 | 0.0196 | 90.86% |

| 29 | 0.0945 | 0.0166 | 89.70% |

| 30 | 0.0921 | 0.0195 | 89.98% |

| 31 | 0.0940 | 0.0152 | 89.76% |

| 32 | 0.0943 | 0.0134 | 89.73% |

| 33 | 0.0942 | 0.0166 | 89.72% |

| 34 | 0.0959 | 0.0151 | 89.52% |

| 35 | 0.0947 | 0.0151 | 89.66% |

| 36 | 0.0961 | 0.0127 | 89.49% |

| 37 | 0.0931 | 0.0137 | 89.85% |

| 38 | 0.0930 | 0.0115 | 89.86% |

| 39 | 0.0976 | 0.0088 | 89.30% |

| 40 | 0.0960 | 0.0093 | 89.50% |

| 41 | 0.0937 | 0.0108 | 89.78% |

| 42 | 0.0949 | 0.0090 | 89.64% |

| 43 | 0.0949 | 0.0087 | 89.64% |

| 44 | 0.0893 | 0.0101 | 90.31% |

| 45 | 0.0930 | 0.0075 | 89.86% |

| 46 | 0.0950 | 0.0049 | 89.62% |

| 47 | 0.0931 | 0.0059 | 89.85% |

| 48 | 0.0937 | 0.0042 | 89.78% |

| 49 | 0.0943 | 0.0009 | 89.70% |

| 50 | 0.0935 | 0.0000 | 89.80% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.0760 at 4 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.0935

- Mean Success Rate: 89.80%
