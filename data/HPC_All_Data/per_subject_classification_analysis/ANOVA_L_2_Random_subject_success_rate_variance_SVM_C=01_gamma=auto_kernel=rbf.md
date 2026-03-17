# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_2_Random

## Model×Hyperparameters: SVM (C=0.1, gamma=auto, kernel=rbf)


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

| 1 | 0.1333 | 0.2249 | 86.67% |

| 2 | 0.1972 | 0.1358 | 76.39% |

| 3 | 0.1806 | 0.0945 | 78.17% |

| 4 | 0.1915 | 0.0648 | 76.88% |

| 5 | 0.1713 | 0.0747 | 79.33% |

| 6 | 0.1786 | 0.0640 | 78.13% |

| 7 | 0.1818 | 0.0500 | 77.67% |

| 8 | 0.1949 | 0.0475 | 74.73% |

| 9 | 0.1643 | 0.0507 | 80.06% |

| 10 | 0.1791 | 0.0527 | 77.23% |

| 11 | 0.1749 | 0.0461 | 78.08% |

| 12 | 0.1643 | 0.0374 | 80.03% |

| 13 | 0.1739 | 0.0319 | 78.59% |

| 14 | 0.1664 | 0.0341 | 79.68% |

| 15 | 0.1772 | 0.0349 | 77.74% |

| 16 | 0.1720 | 0.0377 | 78.48% |

| 17 | 0.1799 | 0.0245 | 77.42% |

| 18 | 0.1766 | 0.0232 | 77.99% |

| 19 | 0.1854 | 0.0204 | 76.43% |

| 20 | 0.1795 | 0.0281 | 77.28% |

| 21 | 0.1738 | 0.0208 | 78.40% |

| 22 | 0.1786 | 0.0237 | 77.48% |

| 23 | 0.1741 | 0.0246 | 78.20% |

| 24 | 0.1776 | 0.0189 | 77.72% |

| 25 | 0.1816 | 0.0191 | 76.93% |

| 26 | 0.1739 | 0.0204 | 78.27% |

| 27 | 0.1793 | 0.0206 | 77.27% |

| 28 | 0.1785 | 0.0186 | 77.45% |

| 29 | 0.1757 | 0.0171 | 77.96% |

| 30 | 0.1838 | 0.0160 | 76.49% |

| 31 | 0.1798 | 0.0177 | 77.19% |

| 32 | 0.1823 | 0.0113 | 76.80% |

| 33 | 0.1792 | 0.0125 | 77.34% |

| 34 | 0.1796 | 0.0155 | 77.22% |

| 35 | 0.1795 | 0.0139 | 77.24% |

| 36 | 0.1775 | 0.0120 | 77.61% |

| 37 | 0.1831 | 0.0115 | 76.60% |

| 38 | 0.1777 | 0.0122 | 77.56% |

| 39 | 0.1800 | 0.0096 | 77.17% |

| 40 | 0.1797 | 0.0073 | 77.23% |

| 41 | 0.1796 | 0.0060 | 77.25% |

| 42 | 0.1782 | 0.0101 | 77.46% |

| 43 | 0.1807 | 0.0064 | 77.03% |

| 44 | 0.1789 | 0.0070 | 77.34% |

| 45 | 0.1779 | 0.0070 | 77.52% |

| 46 | 0.1790 | 0.0054 | 77.33% |

| 47 | 0.1795 | 0.0044 | 77.24% |

| 48 | 0.1779 | 0.0044 | 77.51% |

| 49 | 0.1778 | 0.0029 | 77.53% |

| 50 | 0.1777 | 0.0000 | 77.55% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1333 at 1 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1777

- Mean Success Rate: 77.55%
