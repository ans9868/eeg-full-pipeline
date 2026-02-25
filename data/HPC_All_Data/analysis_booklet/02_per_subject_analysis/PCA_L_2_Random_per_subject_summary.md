# Per-Subject Summary: PCA_L_2_Random
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
| sub-1 | 100.00% | 79.83% | 2 | 24 |
| sub-2 | 94.74% | 70.92% | 2 | 24 |
| sub-3 | 96.06% | 75.49% | 2 | 24 |
| sub-4 | 100.00% | 78.73% | 1 | 12 |
| sub-5 | 99.89% | 78.11% | 2 | 24 |
| sub-6 | 91.73% | 69.53% | 2 | 24 |
| sub-7 | 99.51% | 73.00% | 3 | 36 |
| sub-8 | 99.77% | 75.35% | 2 | 24 |
| sub-9 | N/A | N/A | 0 | 0 |
| sub-10 | N/A | N/A | 0 | 0 |
| sub-11 | 97.82% | 77.17% | 2 | 24 |
| sub-12 | N/A | N/A | 0 | 0 |
| sub-13 | 100.00% | 80.39% | 1 | 12 |
| sub-14 | 99.35% | 75.85% | 3 | 36 |
| sub-15 | 87.92% | 73.91% | 4 | 48 |
| sub-16 | 100.00% | 80.40% | 1 | 12 |
| sub-17 | 100.00% | 81.01% | 1 | 12 |
| sub-18 | 100.00% | 81.76% | 6 | 72 |
| sub-19 | 99.83% | 82.43% | 2 | 24 |
| sub-20 | N/A | N/A | 0 | 0 |
| sub-21 | 99.92% | 77.18% | 1 | 12 |
| sub-22 | 99.69% | 80.56% | 1 | 12 |
| sub-23 | 99.12% | 76.40% | 1 | 12 |
| sub-24 | 100.00% | 73.15% | 3 | 36 |
| sub-25 | N/A | N/A | 0 | 0 |
| sub-26 | N/A | N/A | 0 | 0 |
| sub-27 | N/A | N/A | 0 | 0 |
| sub-28 | 100.00% | 80.34% | 2 | 24 |
| sub-29 | N/A | N/A | 0 | 0 |
| sub-30 | 99.85% | 82.51% | 2 | 24 |
| sub-31 | N/A | N/A | 0 | 0 |
| sub-32 | N/A | N/A | 0 | 0 |
| sub-33 | 100.00% | 79.47% | 1 | 12 |
| sub-34 | N/A | N/A | 0 | 0 |
| sub-35 | 100.00% | 79.17% | 2 | 24 |
| sub-36 | 99.91% | 80.90% | 1 | 12 |
| sub-37 | 17.96% | 37.29% | 1 | 12 |
| sub-38 | 3.48% | 20.16% | 2 | 24 |
| sub-39 | 19.52% | 36.70% | 3 | 36 |
| sub-40 | 13.88% | 31.43% | 1 | 12 |
| sub-41 | 6.60% | 23.77% | 2 | 24 |
| sub-42 | 15.30% | 30.63% | 2 | 24 |
| sub-43 | N/A | N/A | 0 | 0 |
| sub-44 | 24.40% | 38.29% | 4 | 48 |
| sub-45 | N/A | N/A | 0 | 0 |
| sub-46 | N/A | N/A | 0 | 0 |
| sub-47 | 28.82% | 41.08% | 1 | 12 |
| sub-48 | 32.99% | 39.89% | 2 | 24 |
| sub-49 | 42.49% | 44.85% | 4 | 48 |
| sub-50 | 0.63% | 20.81% | 1 | 12 |
| sub-51 | 0.25% | 19.95% | 2 | 24 |
| sub-52 | N/A | N/A | 0 | 0 |
| sub-53 | N/A | N/A | 0 | 0 |
| sub-54 | 16.60% | 32.76% | 4 | 48 |
| sub-55 | 45.35% | 46.43% | 1 | 12 |
| sub-56 | 19.76% | 36.58% | 3 | 36 |
| sub-57 | 10.61% | 32.79% | 1 | 12 |
| sub-58 | 12.72% | 36.94% | 2 | 24 |
| sub-59 | 0.00% | 19.20% | 3 | 36 |
| sub-60 | 0.00% | 13.97% | 1 | 12 |
| sub-61 | 13.14% | 30.36% | 3 | 36 |
| sub-62 | 24.45% | 38.30% | 3 | 36 |
| sub-63 | 5.48% | 23.51% | 2 | 24 |
| sub-64 | 57.12% | 55.99% | 1 | 12 |
| sub-65 | 0.27% | 20.20% | 1 | 12 |

## Summary Statistics

- **Subjects with test data**: 49
- **Subjects without test data**: 16
- **Median accuracy (across subjects, median)**: 87.92%
- **Mean accuracy (across subjects, mean)**: 55.42%
- **Min accuracy**: 0.00%
- **Max accuracy**: 100.00%
- **Mean N folds per subject**: 2.0
- **Median N folds per subject**: 2
- **Mean N observations per subject**: 24.5
- **Median N observations per subject**: 24