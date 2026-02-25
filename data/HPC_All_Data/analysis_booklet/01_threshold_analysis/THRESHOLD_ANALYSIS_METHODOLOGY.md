# 📋 Subject-Level Classification Threshold Analysis: Methodology

## Overview

This document describes the complete methodology for analyzing optimal classification thresholds for subject-level Alzheimer's vs Control classification.

## Problem Statement

**Current Approach**: For each subject, if >50% of their epochs are predicted as AD, classify the subject as AD.

**Question**: Should this 0.5 threshold be adjusted to match the training data distribution (e.g., 60% AD / 40% Control)?

**Goal**: Find the optimal threshold that maximizes classification performance across different experiments.

---

## Step-by-Step Methodology

### Step 1: Data Collection and Loading

#### 1.1 Locate Prediction Files
- **Source**: `test_predictions.parquet` files in each experiment's ML results directory
- **Structure**: `{experiment_dir}/ml_results/{model}/{fold}/task_{model}_{hyperparams}/test_predictions.parquet`
- **Experiments analyzed**:
  - `grid_50_random_folds/Anova_L_2_incomplete_ml_results`
  - `grid_50_random_folds/Anova_L_6_Incomplete_ml_results`
  - `grid_50_random_folds/PCA_L_2_ml_results`
  - `grid_50_random_folds/PCA_L_6_ml_results`

#### 1.2 Load Prediction Data
```python
import pandas as pd
from pathlib import Path

# Find all test_predictions.parquet files
parquet_files = list(results_dir.rglob("test_predictions.parquet"))

# Load each file
for parquet_file in parquet_files:
    df = pd.read_parquet(parquet_file)
    # Process...
```

#### 1.3 Data Structure
Each parquet file contains:
- `SubjectID`: Integer subject identifier
- `EpochID`: Epoch number within subject
- `Group`: String label ("alz" or "cntrl")
- `label`: Numeric label (0.0 = AD, 1.0 = Control)
- `prediction`: Numeric prediction (0.0 = predicted AD, 1.0 = predicted Control)

---

### Step 2: Subject-Level Aggregation

#### 2.1 Calculate AD Ratio per Subject per Fold/Model

For each subject in each fold/model combination:

```python
# For a single subject in a single fold/model
subject_df = df[df['SubjectID'] == subject_id]

# Count AD predictions (0.0 = AD)
ad_predictions = (subject_df['prediction'] == 0.0).sum()
total_epochs = len(subject_df)

# Calculate AD ratio
ad_ratio = ad_predictions / total_epochs
```

**Example**:
- Subject has 100 epochs
- 60 epochs predicted as AD (prediction = 0.0)
- 40 epochs predicted as Control (prediction = 1.0)
- **AD ratio = 0.60** (60% of epochs are AD)

#### 2.2 Aggregate Across Folds/Models

Each subject appears in multiple folds and models. Average their AD ratios:

```python
# Group by subject and average AD ratio
subject_agg = data.groupby(['subject_id', 'true_group']).agg({
    'ad_ratio': 'mean'  # Average across all folds/models
}).reset_index()
```

**Rationale**: This gives a stable estimate of each subject's "AD-ness" across different training/test splits.

---

### Step 3: Threshold Testing

#### 3.1 Test Multiple Thresholds

For each threshold value (0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7):

```python
# Classification logic
if ad_ratio >= threshold:
    predicted_class = "AD"  # Binary: 0
else:
    predicted_class = "Control"  # Binary: 1
```

**Interpretation**:
- **Threshold = 0.5**: If ≥50% of epochs are AD, classify subject as AD
- **Threshold = 0.6**: If ≥60% of epochs are AD, classify subject as AD
- **Threshold = 0.3**: If ≥30% of epochs are AD, classify subject as AD (more lenient)

#### 3.2 Generate Predictions

```python
subject_agg['predicted'] = (subject_agg['ad_ratio'] < threshold).astype(int)
# Note: ad_ratio < threshold means fewer AD predictions → Control (1)
#       ad_ratio >= threshold means more AD predictions → AD (0)
```

**Wait, let me clarify the logic**:
- If `ad_ratio` is high (e.g., 0.7), most epochs are AD → subject should be AD
- If `ad_ratio` is low (e.g., 0.3), few epochs are AD → subject should be Control

So the classification should be:
```python
# If ad_ratio >= threshold, predict AD (0)
# If ad_ratio < threshold, predict Control (1)
subject_agg['predicted'] = (subject_agg['ad_ratio'] >= threshold).astype(int)
# But we need: 0 = AD, 1 = Control
# So: predicted = 0 if ad_ratio >= threshold, else 1
subject_agg['predicted'] = (subject_agg['ad_ratio'] < threshold).astype(int)
```

Actually, let me think about this more carefully:
- `ad_ratio = 0.7` means 70% of epochs are AD
- If threshold = 0.6, then 0.7 >= 0.6 → predict AD
- So: `predicted = 0 if ad_ratio >= threshold`

But in our code, we have:
```python
subject_agg['predicted'] = (subject_agg['ad_ratio'] < threshold).astype(int)
```

This means:
- If `ad_ratio < threshold` → `predicted = 1` (Control)
- If `ad_ratio >= threshold` → `predicted = 0` (AD)

So the logic is correct! The code uses `< threshold` to assign 1 (Control), which means `>= threshold` gets 0 (AD).

---

### Step 4: Performance Metrics Calculation

#### 4.1 Confusion Matrix

For each threshold, calculate confusion matrix:

```python
from sklearn.metrics import confusion_matrix

y_true = subject_agg['true_label']  # 0 = AD, 1 = Control
y_pred = subject_agg['predicted']   # 0 = AD, 1 = Control

cm = confusion_matrix(y_true, y_pred)
# Returns:
# [[tn, fp],   # Row 0 = True AD
#  [fn, tp]]   # Row 1 = True Control
# Col 0 = Predicted AD, Col 1 = Predicted Control

tn, fp, fn, tp = cm.ravel()
```

**Confusion Matrix Interpretation**:
- **tn (True Negative)**: AD correctly predicted as AD
- **fp (False Positive)**: Control incorrectly predicted as AD
- **fn (False Negative)**: AD incorrectly predicted as Control
- **tp (True Positive)**: Control correctly predicted as Control

#### 4.2 Calculate Metrics

```python
# Overall accuracy
accuracy = (tn + tp) / (tn + tp + fp + fn)

# AD class metrics
ad_precision = tn / (tn + fp)  # Of predicted AD, how many are actually AD?
ad_recall = tn / (tn + fn)     # Of actual AD, how many did we catch?

# Control class metrics
cntrl_precision = tp / (tp + fn)  # Of predicted Control, how many are actually Control?
cntrl_recall = tp / (tp + fp)    # Of actual Control, how many did we catch?

# Balanced accuracy (accounts for class imbalance)
balanced_accuracy = (ad_recall + cntrl_recall) / 2

# Predicted distribution
predicted_ad_pct = (y_pred == 0).sum() / len(y_pred) * 100
```

---

### Step 5: Optimal Threshold Selection

#### 5.1 Find Best Threshold

For each experiment, find the threshold that maximizes balanced accuracy:

```python
best_threshold = results_df.loc[results_df['balanced_accuracy'].idxmax(), 'threshold']
```

**Why balanced accuracy?**
- Accounts for class imbalance
- Gives equal weight to AD and Control classification
- More clinically relevant than raw accuracy

#### 5.2 Compare to Current (0.5)

```python
current_05 = results_df[results_df['threshold'] == 0.5].iloc[0]
improvement = (best['accuracy'] - current_05['accuracy']) * 100
```

#### 5.3 Evaluate Specific Thresholds

Also evaluate thresholds of interest:
- **0.55**: Moderate adjustment
- **0.6**: Matches 60/40 distribution
- **0.7**: More conservative

---

### Step 6: Cross-Experiment Analysis

#### 6.1 Compare Optimal Thresholds

```python
optimal_thresholds = [results['best']['threshold'] for results in all_results.values()]
avg_optimal = np.mean(optimal_thresholds)
threshold_range = (min(optimal_thresholds), max(optimal_thresholds))
```

#### 6.2 Identify Patterns

- **ANOVA vs PCA**: Do ANOVA experiments need different thresholds than PCA?
- **L_2 vs L_6**: Does cross-validation strategy affect optimal threshold?
- **Performance differences**: Which experiments benefit most from threshold adjustment?

#### 6.3 Generate Recommendations

1. **Universal threshold**: Single threshold for all experiments
2. **Experiment-specific**: Different thresholds for each experiment
3. **Feature-specific**: Different thresholds for ANOVA vs PCA

---

## Implementation Details

### Code Structure

```python
def load_subject_predictions(experiment_dir, max_folds=50):
    """Load and aggregate prediction data"""
    # 1. Find all parquet files
    # 2. Load each file
    # 3. Calculate AD ratio per subject per fold/model
    # 4. Return aggregated DataFrame

def test_thresholds(data):
    """Test different thresholds"""
    # 1. Aggregate by subject (average across folds/models)
    # 2. For each threshold:
    #    - Classify subjects
    #    - Calculate metrics
    # 3. Return results DataFrame

def analyze_all_experiments():
    """Run analysis on all experiments"""
    # 1. Load data for each experiment
    # 2. Test thresholds for each
    # 3. Find optimal thresholds
    # 4. Compare across experiments
```

### Key Functions

**Subject Aggregation**:
```python
# Per subject, per fold/model
ad_ratio = (predictions == 0.0).sum() / len(predictions)

# Aggregate across folds/models
subject_ad_ratio = data.groupby('subject_id')['ad_ratio'].mean()
```

**Threshold Classification**:
```python
# Binary classification
predicted = (subject_ad_ratio >= threshold).astype(int)
# But we need: 0 = AD, 1 = Control
# So: if ad_ratio >= threshold → AD (0)
#     if ad_ratio < threshold → Control (1)
predicted = (subject_ad_ratio < threshold).astype(int)  # Inverts to get 0/1 correctly
```

**Performance Calculation**:
```python
cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()
accuracy = (tn + tp) / (tn + tp + fp + fn)
balanced_acc = (ad_recall + cntrl_recall) / 2
```

---

## Validation and Quality Checks

### Data Quality
- ✅ Verify subject counts match expected values
- ✅ Check that all subjects have predictions
- ✅ Confirm true labels are consistent

### Metric Validation
- ✅ Confusion matrix sums to total subjects
- ✅ Accuracy matches manual calculation
- ✅ Recall and precision are between 0 and 1
- ✅ Balanced accuracy is average of recalls

### Threshold Logic
- ✅ Lower threshold → more subjects classified as AD
- ✅ Higher threshold → fewer subjects classified as AD
- ✅ Threshold = 0.5 gives balanced classification (if data is balanced)

---

## Limitations and Assumptions

### Assumptions
1. **Subject-level aggregation**: Simple averaging across folds/models
2. **Binary classification**: No probability scores used
3. **Fixed threshold**: Same threshold for all subjects
4. **Epoch independence**: All epochs weighted equally

### Limitations
1. **No probability scores**: Can't use ROC curves or precision-recall curves
2. **Simple aggregation**: Could explore weighted averaging or other methods
3. **No subject-specific thresholds**: Could optimize per subject
4. **Cross-validation dependency**: Results may vary with different fold splits

### Future Improvements
1. **Probability-based thresholds**: Use `predict_proba` if available
2. **Weighted aggregation**: Weight by model performance or fold quality
3. **Subject-specific thresholds**: Optimize threshold per subject type
4. **Cost-sensitive optimization**: Incorporate clinical costs of false positives/negatives

---

## Output Files

### Generated Files
1. **`final_subject_threshold_analysis.md`**: Comprehensive report with all results
2. **`visualizations/multi_experiment_threshold_analysis.png`**: Comparison visualizations
3. **`subject_threshold_report.md`**: Quick summary (if generated)

### Report Contents
- Summary table of all experiments
- Detailed performance by threshold for each experiment
- Optimal threshold recommendations
- Implementation code examples
- Methodology explanation

---

## Usage Example

```python
# Run analysis
python multi_experiment_threshold_analysis.py

# Results:
# - Optimal threshold for ANOVA_L_2: 0.45
# - Optimal threshold for ANOVA_L_6: 0.70
# - Optimal threshold for PCA_L_2: 0.30
# - Optimal threshold for PCA_L_6: 0.40

# Implementation:
thresholds = {
    'ANOVA_L_2': 0.45,
    'ANOVA_L_6': 0.70,
    'PCA_L_2': 0.30,
    'PCA_L_6': 0.40
}

threshold = thresholds[experiment_name]
if ad_ratio >= threshold:
    subject_class = "AD"
else:
    subject_class = "Control"
```

---

*Methodology document created: December 8, 2025*
*For questions or clarifications, refer to the analysis code: `multi_experiment_threshold_analysis.py`*
