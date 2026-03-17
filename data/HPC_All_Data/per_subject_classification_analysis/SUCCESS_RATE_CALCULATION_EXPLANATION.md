# Per-Subject Success Rate Calculation Explanation

## Overview

The `*_per_subject_success_rate.png` plots contain two graphs showing different metrics for each subject. Both metrics are calculated from per-subject accuracies derived from `test_predictions.parquet` files.

## Data Source

All calculations use per-subject accuracy values calculated from `test_predictions.parquet` files:
- For each subject in each fold×model combination
- Accuracy = `(label == prediction).sum() / len(subject_data)`
- This gives us a list of accuracies for each subject across all fold×model combinations

---

## Graph 1: Per-Subject Classification Success Rate

### What It Shows
**Percentage of fold×model combinations where the subject's accuracy > 50%**

### Calculation Method

For each subject:
1. Collect all accuracy values from all fold×model combinations
2. Count how many of these accuracies are > 50%
3. Calculate percentage: `(count > 50%) / (total) × 100%`

### Pseudocode

```python
function calculate_success_rate(subject_accuracies_per_fold):
    """
    Calculate success rate: % of fold×model combinations where accuracy > 50%.
    
    Input:
        subject_accuracies_per_fold: list of accuracy scores (0.0 to 1.0)
                                     for a single subject across all fold×model combinations
    
    Output:
        success_rate: percentage (0 to 100)
    """
    successful_folds = 0
    total_folds = length(subject_accuracies_per_fold)
    
    if total_folds == 0:
        return 0
    
    for accuracy in subject_accuracies_per_fold:
        if accuracy > 0.50:  # 50% threshold
            successful_folds = successful_folds + 1
    
    success_rate = (successful_folds / total_folds) * 100
    return success_rate
```

### Example

Subject: sub-1
- Fold×Model combinations: 12 total
- Accuracies: [0.85, 0.90, 0.45, 0.88, 0.92, 0.75, 0.60, 0.55, 0.40, 0.80, 0.70, 0.65]
- Accuracies > 50%: 10 out of 12
- Success Rate = (10 / 12) × 100% = 83.33%

### Interpretation

- **100%**: Subject is correctly classified (>50% accuracy) in ALL fold×model combinations
- **0%**: Subject is NEVER correctly classified (>50% accuracy) in any fold×model combination
- **Partial (e.g., 75%)**: Subject is correctly classified in 75% of fold×model combinations

---

## Graph 2: Per-Subject Mean Accuracy

### What It Shows
**Average accuracy across all fold×model combinations for each subject**

### Calculation Method

For each subject:
1. Collect all accuracy values from all fold×model combinations
2. Calculate arithmetic mean: `sum(accuracies) / count(accuracies) × 100%`

### Pseudocode

```python
function calculate_mean_accuracy(subject_accuracies_per_fold):
    """
    Calculate mean accuracy: average of all fold×model accuracies.
    
    Input:
        subject_accuracies_per_fold: list of accuracy scores (0.0 to 1.0)
                                     for a single subject across all fold×model combinations
    
    Output:
        mean_accuracy: percentage (0 to 100)
    """
    total_accuracy_sum = 0
    total_folds = length(subject_accuracies_per_fold)
    
    if total_folds == 0:
        return 0
    
    for accuracy in subject_accuracies_per_fold:
        total_accuracy_sum = total_accuracy_sum + accuracy
    
    mean_accuracy = (total_accuracy_sum / total_folds) * 100
    return mean_accuracy
```

### Example

Subject: sub-1
- Fold×Model combinations: 12 total
- Accuracies: [0.85, 0.90, 0.45, 0.88, 0.92, 0.75, 0.60, 0.55, 0.40, 0.80, 0.70, 0.65]
- Sum = 8.40
- Mean Accuracy = (8.40 / 12) × 100% = 70.00%

### Interpretation

- Shows the **average performance** across all experimental conditions
- A subject with 70% mean accuracy performs, on average, at 70% across all fold×model combinations
- Can be >50% even if success rate <100% (some folds below 50%, but average is above)

---

## Key Differences

| Metric | Success Rate | Mean Accuracy |
|--------|-------------|---------------|
| **What it measures** | % of times accuracy > 50% | Average accuracy value |
| **Range** | 0-100% | 0-100% |
| **Interpretation** | Consistency of correct classification | Overall performance level |
| **Example** | 80% success rate = correct in 8/10 folds | 70% mean = average of 0.70 across all folds |

## Important Notes

1. **Both metrics use the same data source**: Per-subject accuracies from `test_predictions.parquet` files
2. **Accuracy calculation**: For each subject in each fold×model: `(correct predictions) / (total predictions)`
3. **Success Rate**: Binary threshold (above/below 50%)
4. **Mean Accuracy**: Continuous average (can be any value 0-100%)

## Visual Elements

- **Green bars**: 100% success rate (always correctly classified)
- **Yellow bars**: Partial success (some folds >50%, some <50%)
- **Pink bars**: 0% success rate (never correctly classified)
- **Red dashed line**: 50% threshold for reference

---

*Calculations performed using data from test_predictions.parquet files*


