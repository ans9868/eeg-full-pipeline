# Per-Subject Summary: ANOVA_L_2_Random
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
| sub-1 | 91.38% | 91.01% | 2 | 24 |
| sub-2 | 60.71% | 59.99% | 2 | 24 |
| sub-3 | 84.24% | 76.85% | 2 | 24 |
| sub-4 | 95.81% | 93.62% | 1 | 12 |
| sub-5 | 78.39% | 77.84% | 2 | 24 |
| sub-6 | 32.74% | 33.53% | 2 | 24 |
| sub-7 | 95.08% | 91.90% | 3 | 36 |
| sub-8 | 98.76% | 96.97% | 2 | 24 |
| sub-9 | N/A | N/A | 0 | 0 |
| sub-10 | N/A | N/A | 0 | 0 |
| sub-11 | 89.81% | 85.10% | 2 | 24 |
| sub-12 | N/A | N/A | 0 | 0 |
| sub-13 | 68.15% | 74.00% | 1 | 12 |
| sub-14 | 85.70% | 85.55% | 3 | 36 |
| sub-15 | 73.82% | 73.03% | 4 | 48 |
| sub-16 | 93.52% | 89.65% | 1 | 12 |
| sub-17 | 92.12% | 92.23% | 1 | 12 |
| sub-18 | 89.86% | 89.38% | 6 | 72 |
| sub-19 | 86.58% | 79.87% | 2 | 24 |
| sub-20 | N/A | N/A | 0 | 0 |
| sub-21 | 97.20% | 90.98% | 1 | 12 |
| sub-22 | 71.66% | 73.70% | 1 | 12 |
| sub-23 | 59.78% | 66.75% | 1 | 12 |
| sub-24 | 92.48% | 93.18% | 3 | 36 |
| sub-25 | N/A | N/A | 0 | 0 |
| sub-26 | N/A | N/A | 0 | 0 |
| sub-27 | N/A | N/A | 0 | 0 |
| sub-28 | 86.62% | 77.88% | 2 | 24 |
| sub-29 | N/A | N/A | 0 | 0 |
| sub-30 | 89.33% | 88.67% | 2 | 24 |
| sub-31 | N/A | N/A | 0 | 0 |
| sub-32 | N/A | N/A | 0 | 0 |
| sub-33 | 76.70% | 77.06% | 1 | 12 |
| sub-34 | N/A | N/A | 0 | 0 |
| sub-35 | 83.80% | 87.06% | 2 | 24 |
| sub-36 | 50.09% | 55.84% | 1 | 12 |
| sub-37 | 66.07% | 65.47% | 1 | 12 |
| sub-38 | 58.48% | 55.23% | 2 | 24 |
| sub-39 | 72.28% | 70.17% | 3 | 36 |
| sub-40 | 72.93% | 71.39% | 1 | 12 |
| sub-41 | 72.05% | 61.66% | 2 | 24 |
| sub-42 | 82.74% | 79.23% | 2 | 24 |
| sub-43 | N/A | N/A | 0 | 0 |
| sub-44 | 57.71% | 58.58% | 4 | 48 |
| sub-45 | N/A | N/A | 0 | 0 |
| sub-46 | N/A | N/A | 0 | 0 |
| sub-47 | 74.51% | 72.66% | 1 | 12 |
| sub-48 | 73.82% | 71.20% | 2 | 24 |
| sub-49 | 87.19% | 84.63% | 4 | 48 |
| sub-50 | 22.55% | 20.62% | 1 | 12 |
| sub-51 | 44.53% | 42.44% | 2 | 24 |
| sub-52 | N/A | N/A | 0 | 0 |
| sub-53 | N/A | N/A | 0 | 0 |
| sub-54 | 78.02% | 75.28% | 4 | 48 |
| sub-55 | 89.47% | 83.92% | 1 | 12 |
| sub-56 | 76.84% | 77.63% | 3 | 36 |
| sub-57 | 78.59% | 74.75% | 1 | 12 |
| sub-58 | 70.91% | 68.56% | 2 | 24 |
| sub-59 | 4.76% | 11.84% | 3 | 36 |
| sub-60 | 55.71% | 43.06% | 1 | 12 |
| sub-61 | 27.75% | 27.17% | 3 | 36 |
| sub-62 | 82.15% | 83.06% | 3 | 36 |
| sub-63 | 45.07% | 41.76% | 2 | 24 |
| sub-64 | 94.25% | 93.16% | 1 | 12 |
| sub-65 | 52.01% | 44.21% | 1 | 12 |

## Summary Statistics

- **Subjects with test data**: 49
- **Subjects without test data**: 16
- **Median accuracy (across subjects, median)**: 76.84%
- **Mean accuracy (across subjects, mean)**: 71.01%
- **Min accuracy**: 4.76%
- **Max accuracy**: 98.76%
- **Mean N folds per subject**: 2.0
- **Median N folds per subject**: 2
- **Mean N observations per subject**: 24.5
- **Median N observations per subject**: 24