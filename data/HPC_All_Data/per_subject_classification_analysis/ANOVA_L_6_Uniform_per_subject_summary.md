# Per-Subject Summary: ANOVA_L_6_Uniform
================================================================================

**Calculation Method**: Per-subject accuracy calculated from `test_predictions.parquet` files.
For each subject in each fold×model combination:
- Filter predictions where `SubjectID == subject_id`
- Calculate: `accuracy = (label == prediction).sum() / len(subject_data)`
- Then aggregate across folds and model×HP combinations

For each subject (1-65), shows:
- **Median Accuracy**: Median accuracy across all folds and model×HP combinations
- **Mean Accuracy**: Mean accuracy across all folds and model×HP combinations
- **N Folds Observed**: Number of unique folds where subject appeared in test set
- **N Observations**: Total number of fold×model combinations
- **NA**: Subject not observed in any test fold

| Subject | Median Accuracy | Mean Accuracy | N Folds | N Observations |
|---------|----------------|---------------|---------|----------------|
| sub-1 | 96.08% | 93.10% | 1 | 12 |
| sub-2 | 70.65% | 65.38% | 1 | 12 |
| sub-3 | 72.41% | 71.76% | 1 | 12 |
| sub-4 | 95.58% | 93.01% | 1 | 12 |
| sub-5 | 73.76% | 75.75% | 1 | 12 |
| sub-6 | 35.82% | 33.08% | 1 | 12 |
| sub-7 | 99.41% | 94.69% | 1 | 12 |
| sub-8 | 98.53% | 94.54% | 1 | 12 |
| sub-9 | 86.58% | 80.87% | 1 | 12 |
| sub-10 | 50.00% | 55.46% | 1 | 12 |
| sub-11 | 90.41% | 85.07% | 1 | 12 |
| sub-12 | 67.74% | 70.01% | 1 | 12 |
| sub-13 | 79.44% | 77.98% | 1 | 12 |
| sub-14 | 82.43% | 86.23% | 1 | 12 |
| sub-15 | 80.91% | 78.36% | 1 | 12 |
| sub-16 | 91.72% | 87.60% | 1 | 12 |
| sub-17 | 84.89% | 81.68% | 1 | 12 |
| sub-18 | 92.73% | 90.13% | 1 | 12 |
| sub-19 | 79.67% | 75.74% | 1 | 12 |
| sub-20 | 78.61% | 76.02% | 1 | 12 |
| sub-21 | 97.12% | 91.64% | 1 | 12 |
| sub-22 | 75.05% | 77.77% | 1 | 12 |
| sub-23 | 68.10% | 68.88% | 1 | 12 |
| sub-24 | 94.95% | 91.73% | 1 | 12 |
| sub-25 | 17.93% | 19.25% | 1 | 12 |
| sub-26 | 73.82% | 71.01% | 1 | 12 |
| sub-27 | 98.55% | 97.98% | 1 | 12 |
| sub-28 | 83.46% | 68.44% | 1 | 12 |
| sub-29 | 69.03% | 63.06% | 1 | 12 |
| sub-30 | 87.65% | 86.53% | 1 | 12 |
| sub-31 | 39.92% | 42.36% | 1 | 12 |
| sub-32 | 97.22% | 91.60% | 1 | 12 |
| sub-33 | 79.57% | 79.04% | 1 | 12 |
| sub-34 | 89.37% | 90.01% | 1 | 12 |
| sub-35 | 89.84% | 89.49% | 1 | 12 |
| sub-36 | 56.76% | 55.60% | 1 | 12 |
| sub-37 | 65.17% | 64.40% | 2 | 24 |
| sub-38 | 60.89% | 57.11% | 2 | 24 |
| sub-39 | 72.19% | 69.70% | 2 | 24 |
| sub-40 | 71.75% | 72.63% | 2 | 24 |
| sub-41 | 71.70% | 62.22% | 2 | 24 |
| sub-42 | 82.65% | 78.04% | 2 | 24 |
| sub-43 | 18.38% | 22.71% | 2 | 24 |
| sub-44 | 55.48% | 53.45% | 1 | 12 |
| sub-45 | 29.05% | 29.02% | 1 | 12 |
| sub-46 | 68.28% | 67.08% | 1 | 12 |
| sub-47 | 74.12% | 72.45% | 1 | 12 |
| sub-48 | 76.75% | 73.96% | 1 | 12 |
| sub-49 | 97.11% | 89.02% | 1 | 12 |
| sub-50 | 28.60% | 25.68% | 1 | 12 |
| sub-51 | 36.32% | 34.66% | 1 | 12 |
| sub-52 | 44.44% | 44.97% | 1 | 12 |
| sub-53 | 49.26% | 52.14% | 1 | 12 |
| sub-54 | 64.91% | 64.84% | 1 | 12 |
| sub-55 | 92.31% | 85.20% | 1 | 12 |
| sub-56 | 83.63% | 80.78% | 1 | 12 |
| sub-57 | 86.14% | 81.76% | 1 | 12 |
| sub-58 | 60.06% | 57.22% | 1 | 12 |
| sub-59 | 2.95% | 9.52% | 1 | 12 |
| sub-60 | 23.89% | 21.53% | 1 | 12 |
| sub-61 | 35.29% | 32.94% | 1 | 12 |
| sub-62 | 92.39% | 90.30% | 1 | 12 |
| sub-63 | 39.87% | 39.90% | 1 | 12 |
| sub-64 | 92.52% | 90.88% | 1 | 12 |
| sub-65 | 56.03% | 47.53% | 1 | 12 |

## Summary Statistics

- **Subjects with test data**: 65
- **Subjects without test data**: 0
- **Median accuracy (across subjects, median)**: 74.12%
- **Mean accuracy (across subjects, mean)**: 68.04%
- **Min accuracy**: 2.95%
- **Max accuracy**: 99.41%
- **Mean N folds per subject**: 1.1
- **Median N folds per subject**: 1
- **Mean N observations per subject**: 13.3
- **Median N observations per subject**: 12