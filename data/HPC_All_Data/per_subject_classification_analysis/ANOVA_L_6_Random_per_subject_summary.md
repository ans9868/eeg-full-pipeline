# Per-Subject Summary: ANOVA_L_6_Random
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
| sub-1 | 93.47% | 90.13% | 2 | 22 |
| sub-2 | 52.10% | 56.69% | 5 | 48 |
| sub-3 | 65.52% | 72.21% | 2 | 19 |
| sub-4 | 97.79% | 94.10% | 5 | 43 |
| sub-5 | 78.71% | 78.92% | 7 | 48 |
| sub-6 | 31.68% | 32.96% | 7 | 51 |
| sub-7 | 95.57% | 91.57% | 4 | 26 |
| sub-8 | 97.29% | 94.49% | 7 | 48 |
| sub-9 | 84.11% | 79.09% | 2 | 10 |
| sub-10 | 45.27% | 51.97% | 2 | 24 |
| sub-11 | 90.05% | 84.30% | 6 | 65 |
| sub-12 | 66.33% | 72.01% | 2 | 16 |
| sub-13 | 75.87% | 76.95% | 5 | 46 |
| sub-14 | 91.59% | 90.42% | 5 | 52 |
| sub-15 | 74.24% | 72.52% | 7 | 68 |
| sub-16 | 95.73% | 92.16% | 3 | 26 |
| sub-17 | 93.22% | 92.64% | 5 | 54 |
| sub-18 | 85.73% | 87.46% | 4 | 34 |
| sub-19 | 96.33% | 84.79% | 3 | 21 |
| sub-20 | 80.04% | 79.92% | 3 | 33 |
| sub-21 | 97.04% | 91.24% | 3 | 33 |
| sub-22 | 70.33% | 74.18% | 2 | 12 |
| sub-23 | 72.80% | 73.64% | 2 | 19 |
| sub-24 | 93.27% | 91.76% | 3 | 29 |
| sub-25 | 20.69% | 21.99% | 3 | 24 |
| sub-26 | 88.09% | 86.80% | 4 | 41 |
| sub-27 | 94.61% | 92.69% | 4 | 45 |
| sub-28 | 92.54% | 83.48% | 7 | 62 |
| sub-29 | 75.27% | 75.24% | 3 | 23 |
| sub-30 | 93.45% | 88.92% | 4 | 46 |
| sub-31 | 36.18% | 43.48% | 2 | 16 |
| sub-32 | 96.03% | 89.84% | 6 | 64 |
| sub-33 | 81.49% | 79.78% | 3 | 29 |
| sub-34 | 82.37% | 85.43% | 3 | 30 |
| sub-35 | 89.34% | 87.38% | 7 | 67 |
| sub-36 | 52.70% | 55.04% | 8 | 74 |
| sub-37 | 60.88% | 61.60% | 5 | 47 |
| sub-38 | 59.82% | 53.22% | 6 | 49 |
| sub-39 | 71.66% | 67.84% | 4 | 31 |
| sub-40 | 69.09% | 69.45% | 5 | 38 |
| sub-41 | 63.89% | 58.09% | 8 | 85 |
| sub-42 | 78.29% | 74.73% | 4 | 29 |
| sub-43 | 19.03% | 21.56% | 5 | 52 |
| sub-44 | 57.71% | 58.66% | 11 | 91 |
| sub-45 | 38.42% | 35.71% | 8 | 71 |
| sub-46 | 66.88% | 68.37% | 2 | 17 |
| sub-47 | 68.24% | 65.32% | 5 | 43 |
| sub-48 | 75.80% | 74.65% | 4 | 44 |
| sub-49 | 84.20% | 84.17% | 6 | 49 |
| sub-50 | 28.71% | 24.23% | 2 | 16 |
| sub-51 | 37.31% | 37.44% | 6 | 42 |
| sub-52 | 45.54% | 47.71% | 2 | 24 |
| sub-53 | 63.89% | 60.90% | 4 | 38 |
| sub-54 | 76.98% | 73.51% | 6 | 45 |
| sub-55 | 90.04% | 81.82% | 5 | 46 |
| sub-56 | 79.94% | 77.65% | 3 | 29 |
| sub-57 | 81.93% | 75.87% | 7 | 64 |
| sub-58 | 74.56% | 69.82% | 5 | 47 |
| sub-59 | 5.33% | 11.34% | 4 | 45 |
| sub-60 | 50.00% | 41.97% | 10 | 102 |
| sub-61 | 28.04% | 27.16% | 6 | 57 |
| sub-62 | 86.29% | 85.30% | 3 | 31 |
| sub-63 | 43.68% | 40.19% | 3 | 25 |
| sub-64 | 94.16% | 93.01% | 6 | 60 |
| sub-65 | 51.01% | 45.58% | 5 | 51 |

## Summary Statistics

- **Subjects with test data**: 65
- **Subjects without test data**: 0
- **Median accuracy (across subjects, median)**: 75.80%
- **Mean accuracy (across subjects, mean)**: 68.97%
- **Min accuracy**: 5.33%
- **Max accuracy**: 97.79%
- **Mean N folds per subject**: 4.6
- **Median N folds per subject**: 4
- **Mean N observations per subject**: 42.1
- **Median N observations per subject**: 43