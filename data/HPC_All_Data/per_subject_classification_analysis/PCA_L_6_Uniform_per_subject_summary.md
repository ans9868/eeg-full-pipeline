# Per-Subject Summary: PCA_L_6_Uniform
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
| sub-1 | 100.00% | 83.75% | 1 | 12 |
| sub-2 | 95.32% | 76.04% | 1 | 12 |
| sub-3 | 98.28% | 74.22% | 1 | 12 |
| sub-4 | 100.00% | 80.74% | 1 | 12 |
| sub-5 | 100.00% | 80.45% | 1 | 12 |
| sub-6 | 97.04% | 74.98% | 1 | 12 |
| sub-7 | 94.88% | 74.13% | 1 | 12 |
| sub-8 | 91.99% | 73.08% | 1 | 12 |
| sub-9 | 74.63% | 63.46% | 1 | 12 |
| sub-10 | 89.26% | 64.48% | 1 | 12 |
| sub-11 | 76.94% | 61.71% | 1 | 12 |
| sub-12 | 88.61% | 64.25% | 1 | 12 |
| sub-13 | 99.81% | 67.94% | 1 | 12 |
| sub-14 | 98.50% | 68.16% | 1 | 12 |
| sub-15 | 88.18% | 62.64% | 1 | 12 |
| sub-16 | 100.00% | 83.55% | 1 | 12 |
| sub-17 | 100.00% | 82.48% | 1 | 12 |
| sub-18 | 100.00% | 82.27% | 1 | 12 |
| sub-19 | 99.25% | 78.58% | 1 | 12 |
| sub-20 | 99.73% | 82.28% | 1 | 12 |
| sub-21 | 100.00% | 81.25% | 1 | 12 |
| sub-22 | 99.90% | 82.79% | 1 | 12 |
| sub-23 | 99.90% | 81.44% | 1 | 12 |
| sub-24 | 100.00% | 82.97% | 1 | 12 |
| sub-25 | 71.26% | 59.81% | 1 | 12 |
| sub-26 | 100.00% | 76.82% | 1 | 12 |
| sub-27 | 99.90% | 78.13% | 1 | 12 |
| sub-28 | 100.00% | 89.60% | 1 | 12 |
| sub-29 | 100.00% | 90.07% | 1 | 12 |
| sub-30 | 100.00% | 89.58% | 1 | 12 |
| sub-31 | 95.20% | 70.89% | 1 | 12 |
| sub-32 | 99.74% | 75.35% | 1 | 12 |
| sub-33 | 99.57% | 75.12% | 1 | 12 |
| sub-34 | 100.00% | 93.03% | 1 | 12 |
| sub-35 | 100.00% | 93.49% | 1 | 12 |
| sub-36 | 99.64% | 89.67% | 1 | 12 |
| sub-37 | 7.78% | 24.26% | 2 | 24 |
| sub-38 | 3.48% | 25.89% | 2 | 24 |
| sub-39 | 29.14% | 40.84% | 2 | 24 |
| sub-40 | 15.35% | 33.81% | 2 | 24 |
| sub-41 | 7.47% | 19.08% | 2 | 24 |
| sub-42 | 15.30% | 24.84% | 2 | 24 |
| sub-43 | 0.65% | 19.03% | 2 | 24 |
| sub-44 | 58.39% | 59.85% | 1 | 12 |
| sub-45 | 17.18% | 32.30% | 1 | 12 |
| sub-46 | 44.84% | 52.83% | 1 | 12 |
| sub-47 | 31.96% | 46.27% | 1 | 12 |
| sub-48 | 45.09% | 52.79% | 1 | 12 |
| sub-49 | 45.09% | 53.61% | 1 | 12 |
| sub-50 | 2.30% | 32.53% | 1 | 12 |
| sub-51 | 2.99% | 33.37% | 1 | 12 |
| sub-52 | 7.54% | 25.61% | 1 | 12 |
| sub-53 | 2.63% | 23.65% | 1 | 12 |
| sub-54 | 2.74% | 23.79% | 1 | 12 |
| sub-55 | 22.01% | 34.30% | 1 | 12 |
| sub-56 | 13.57% | 33.87% | 1 | 12 |
| sub-57 | 12.81% | 30.27% | 1 | 12 |
| sub-58 | 1.87% | 23.42% | 1 | 12 |
| sub-59 | 0.00% | 17.29% | 1 | 12 |
| sub-60 | 0.00% | 17.09% | 1 | 12 |
| sub-61 | 7.06% | 26.91% | 1 | 12 |
| sub-62 | 32.66% | 39.13% | 1 | 12 |
| sub-63 | 1.30% | 23.92% | 1 | 12 |
| sub-64 | 36.50% | 40.71% | 1 | 12 |
| sub-65 | 0.18% | 12.81% | 1 | 12 |

## Summary Statistics

- **Subjects with test data**: 65
- **Subjects without test data**: 0
- **Median accuracy (across subjects, median)**: 88.18%
- **Mean accuracy (across subjects, mean)**: 57.13%
- **Min accuracy**: 0.00%
- **Max accuracy**: 100.00%
- **Mean N folds per subject**: 1.1
- **Median N folds per subject**: 1
- **Mean N observations per subject**: 13.3
- **Median N observations per subject**: 12