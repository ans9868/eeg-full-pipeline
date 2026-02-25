# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_6_Random

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

| 1 | 0.2844 | 0.0408 | 54.44% |

| 2 | 0.2624 | 0.0191 | 53.99% |

| 3 | 0.2541 | 0.0131 | 52.22% |

| 4 | 0.2488 | 0.0130 | 53.52% |

| 5 | 0.2438 | 0.0154 | 54.20% |

| 6 | 0.2422 | 0.0118 | 53.49% |

| 7 | 0.2405 | 0.0129 | 53.68% |

| 8 | 0.2366 | 0.0127 | 53.75% |

| 9 | 0.2321 | 0.0115 | 53.13% |

| 10 | 0.2344 | 0.0105 | 52.09% |

| 11 | 0.2336 | 0.0134 | 52.03% |

| 12 | 0.2281 | 0.0157 | 53.35% |

| 13 | 0.2234 | 0.0141 | 53.04% |

| 14 | 0.2228 | 0.0133 | 52.86% |

| 15 | 0.2219 | 0.0136 | 52.01% |

| 16 | 0.2151 | 0.0139 | 51.86% |

| 17 | 0.2148 | 0.0113 | 52.64% |

| 18 | 0.2167 | 0.0136 | 51.75% |

| 19 | 0.2149 | 0.0126 | 51.55% |

| 20 | 0.2117 | 0.0127 | 52.20% |

| 21 | 0.2107 | 0.0134 | 51.89% |

| 22 | 0.2111 | 0.0132 | 52.29% |

| 23 | 0.2047 | 0.0101 | 51.14% |

| 24 | 0.2020 | 0.0111 | 52.37% |

| 25 | 0.2000 | 0.0128 | 50.97% |

| 26 | 0.2009 | 0.0137 | 51.05% |

| 27 | 0.1956 | 0.0107 | 51.51% |

| 28 | 0.2013 | 0.0113 | 50.17% |

| 29 | 0.1940 | 0.0100 | 51.30% |

| 30 | 0.1962 | 0.0124 | 51.20% |

| 31 | 0.1932 | 0.0107 | 50.43% |

| 32 | 0.1893 | 0.0106 | 51.04% |

| 33 | 0.1881 | 0.0138 | 50.59% |

| 34 | 0.1812 | 0.0085 | 50.61% |

| 35 | 0.1840 | 0.0090 | 50.54% |

| 36 | 0.1810 | 0.0082 | 50.98% |

| 37 | 0.1822 | 0.0103 | 51.08% |

| 38 | 0.1827 | 0.0108 | 50.57% |

| 39 | 0.1779 | 0.0071 | 51.21% |

| 40 | 0.1778 | 0.0069 | 50.74% |

| 41 | 0.1737 | 0.0050 | 51.01% |

| 42 | 0.1760 | 0.0068 | 50.42% |

| 43 | 0.1728 | 0.0058 | 50.63% |

| 44 | 0.1746 | 0.0068 | 49.98% |

| 45 | 0.1733 | 0.0046 | 50.16% |

| 46 | 0.1723 | 0.0047 | 50.42% |

| 47 | 0.1694 | 0.0056 | 50.43% |

| 48 | 0.1692 | 0.0043 | 50.27% |

| 49 | 0.1677 | 0.0031 | 50.34% |

| 50 | 0.1657 | 0.0000 | 50.41% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1657 at 50 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1657

- Mean Success Rate: 50.41%
