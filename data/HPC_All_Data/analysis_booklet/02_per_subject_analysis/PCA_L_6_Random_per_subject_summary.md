# Per-Subject Summary: PCA_L_6_Random
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
| sub-1 | 100.00% | 78.08% | 2 | 24 |
| sub-2 | 90.82% | 68.87% | 5 | 60 |
| sub-3 | 95.57% | 73.09% | 2 | 24 |
| sub-4 | 100.00% | 84.98% | 5 | 60 |
| sub-5 | 100.00% | 81.08% | 7 | 84 |
| sub-6 | 85.46% | 64.86% | 7 | 84 |
| sub-7 | 98.62% | 76.66% | 4 | 48 |
| sub-8 | 99.55% | 74.01% | 7 | 84 |
| sub-9 | 99.88% | 80.65% | 2 | 24 |
| sub-10 | 83.37% | 62.81% | 2 | 24 |
| sub-11 | 97.33% | 76.06% | 6 | 72 |
| sub-12 | 99.09% | 88.26% | 2 | 24 |
| sub-13 | 99.90% | 80.26% | 5 | 60 |
| sub-14 | 99.72% | 73.27% | 5 | 60 |
| sub-15 | 97.04% | 79.20% | 7 | 84 |
| sub-16 | 99.91% | 81.32% | 3 | 36 |
| sub-17 | 100.00% | 84.48% | 5 | 60 |
| sub-18 | 99.91% | 79.35% | 4 | 48 |
| sub-19 | 99.67% | 83.47% | 3 | 36 |
| sub-20 | 100.00% | 82.95% | 3 | 36 |
| sub-21 | 100.00% | 81.29% | 3 | 36 |
| sub-22 | 99.18% | 77.53% | 2 | 24 |
| sub-23 | 99.90% | 80.91% | 2 | 24 |
| sub-24 | 100.00% | 89.20% | 3 | 36 |
| sub-25 | 51.49% | 52.50% | 3 | 36 |
| sub-26 | 100.00% | 79.51% | 4 | 48 |
| sub-27 | 99.90% | 81.45% | 4 | 48 |
| sub-28 | 100.00% | 79.55% | 7 | 84 |
| sub-29 | 100.00% | 74.66% | 3 | 36 |
| sub-30 | 100.00% | 83.92% | 4 | 48 |
| sub-31 | 84.70% | 62.99% | 2 | 24 |
| sub-32 | 98.81% | 70.04% | 6 | 72 |
| sub-33 | 100.00% | 83.53% | 3 | 36 |
| sub-34 | 100.00% | 77.41% | 3 | 36 |
| sub-35 | 100.00% | 75.53% | 7 | 84 |
| sub-36 | 99.01% | 73.85% | 8 | 96 |
| sub-37 | 18.76% | 34.41% | 5 | 60 |
| sub-38 | 3.04% | 24.85% | 6 | 72 |
| sub-39 | 36.90% | 42.57% | 4 | 48 |
| sub-40 | 17.81% | 33.95% | 5 | 60 |
| sub-41 | 8.16% | 29.20% | 8 | 96 |
| sub-42 | 9.70% | 26.96% | 4 | 48 |
| sub-43 | 3.54% | 22.84% | 5 | 60 |
| sub-44 | 34.93% | 40.89% | 11 | 132 |
| sub-45 | 0.39% | 18.20% | 8 | 96 |
| sub-46 | 46.67% | 53.16% | 2 | 24 |
| sub-47 | 12.75% | 36.29% | 5 | 60 |
| sub-48 | 14.65% | 31.95% | 4 | 48 |
| sub-49 | 29.38% | 40.55% | 6 | 72 |
| sub-50 | 0.52% | 25.46% | 2 | 24 |
| sub-51 | 1.00% | 22.75% | 6 | 72 |
| sub-52 | 23.12% | 32.99% | 2 | 24 |
| sub-53 | 3.47% | 26.15% | 4 | 48 |
| sub-54 | 19.53% | 37.57% | 6 | 72 |
| sub-55 | 21.54% | 33.10% | 5 | 60 |
| sub-56 | 19.47% | 34.81% | 3 | 36 |
| sub-57 | 13.00% | 34.36% | 7 | 84 |
| sub-58 | 13.51% | 29.40% | 5 | 60 |
| sub-59 | 0.00% | 22.98% | 4 | 48 |
| sub-60 | 0.00% | 20.64% | 10 | 120 |
| sub-61 | 11.08% | 31.89% | 6 | 72 |
| sub-62 | 42.39% | 45.69% | 3 | 36 |
| sub-63 | 3.16% | 26.25% | 3 | 36 |
| sub-64 | 50.91% | 52.16% | 6 | 72 |
| sub-65 | 0.18% | 22.12% | 5 | 60 |

## Summary Statistics

- **Subjects with test data**: 65
- **Subjects without test data**: 0
- **Median accuracy (across subjects, median)**: 85.46%
- **Mean accuracy (across subjects, mean)**: 57.10%
- **Min accuracy**: 0.00%
- **Max accuracy**: 100.00%
- **Mean N folds per subject**: 4.6
- **Median N folds per subject**: 4
- **Mean N observations per subject**: 55.4
- **Median N observations per subject**: 48