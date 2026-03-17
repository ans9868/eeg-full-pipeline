# Per-Subject Summary: All Experiments
================================================================================

**Note**: Accuracies calculated from `test_predictions.parquet` files.

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