# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_6_Random

## Model×Hyperparameters: SVM (C=0.1, gamma=auto, kernel=linear)


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

| 1 | 0.2200 | 0.0698 | 72.22% |

| 2 | 0.2260 | 0.0415 | 68.82% |

| 3 | 0.2060 | 0.0412 | 72.40% |

| 4 | 0.2121 | 0.0312 | 70.54% |

| 5 | 0.2034 | 0.0285 | 72.51% |

| 6 | 0.1997 | 0.0263 | 73.38% |

| 7 | 0.1982 | 0.0253 | 73.37% |

| 8 | 0.2034 | 0.0185 | 72.53% |

| 9 | 0.1965 | 0.0217 | 73.77% |

| 10 | 0.1932 | 0.0149 | 74.55% |

| 11 | 0.1966 | 0.0165 | 73.79% |

| 12 | 0.1986 | 0.0146 | 73.23% |

| 13 | 0.1883 | 0.0161 | 75.36% |

| 14 | 0.1944 | 0.0140 | 74.11% |

| 15 | 0.1927 | 0.0148 | 74.32% |

| 16 | 0.1905 | 0.0093 | 74.92% |

| 17 | 0.1876 | 0.0110 | 75.38% |

| 18 | 0.1902 | 0.0096 | 74.97% |

| 19 | 0.1830 | 0.0103 | 76.07% |

| 20 | 0.1863 | 0.0102 | 75.43% |

| 21 | 0.1888 | 0.0103 | 75.03% |

| 22 | 0.1854 | 0.0106 | 75.71% |

| 23 | 0.1890 | 0.0099 | 74.98% |

| 24 | 0.1868 | 0.0087 | 75.49% |

| 25 | 0.1857 | 0.0075 | 75.53% |

| 26 | 0.1862 | 0.0080 | 75.43% |

| 27 | 0.1867 | 0.0073 | 75.33% |

| 28 | 0.1870 | 0.0072 | 75.29% |

| 29 | 0.1829 | 0.0070 | 75.96% |

| 30 | 0.1852 | 0.0064 | 75.63% |

| 31 | 0.1844 | 0.0059 | 75.70% |

| 32 | 0.1853 | 0.0069 | 75.58% |

| 33 | 0.1848 | 0.0054 | 75.62% |

| 34 | 0.1861 | 0.0049 | 75.45% |

| 35 | 0.1847 | 0.0046 | 75.65% |

| 36 | 0.1856 | 0.0041 | 75.44% |

| 37 | 0.1838 | 0.0037 | 75.82% |

| 38 | 0.1850 | 0.0044 | 75.65% |

| 39 | 0.1845 | 0.0040 | 75.67% |

| 40 | 0.1853 | 0.0041 | 75.52% |

| 41 | 0.1830 | 0.0034 | 75.90% |

| 42 | 0.1839 | 0.0026 | 75.74% |

| 43 | 0.1839 | 0.0018 | 75.72% |

| 44 | 0.1836 | 0.0011 | 75.75% |

| 45 | 0.1834 | 0.0023 | 75.81% |

| 46 | 0.1836 | 0.0014 | 75.77% |

| 47 | 0.1838 | 0.0010 | 75.73% |

| 48 | 0.1836 | 0.0010 | 75.77% |

| 49 | 0.1835 | 0.0002 | 75.77% |

| 50 | 0.1835 | 0.0000 | 75.77% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1829 at 29 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1835

- Mean Success Rate: 75.77%
