# ANOVA F-test FWE Mode Test Configurations Summary

## Overview
This document describes the test configurations created for testing the ANOVA F-test transformer with FWE (Family-Wise Error) selection mode across different scenarios.

## What is FWE (Family-Wise Error Rate)?
According to PySpark documentation:
> "fwe chooses all features whose p-values are below a threshold. The threshold is scaled by 1 / numFeatures, thus controlling the family-wise error rate of selection."

FWE is the **most conservative** feature selection method, controlling the probability of making even one false positive among all the tests. This is the Bonferroni correction approach.

## Test Configurations Created

### 1. `config_testanova_fwe_group_classification_31-10-2025.yaml`
- **Experiment Type**: ML Classification
- **ANOVA Label Column**: Group
- **Selection Mode**: fwe
- **Threshold**: 0.05
- **Expected Behavior**: Uses existing 'label' column (hot-encoded groups). This is the **ideal match** scenario.
- **Use Case**: Standard disease vs. control classification with conservative feature selection

### 2. `config_testanova_fwe_subjectid_fingerprinting_31-10-2025.yaml`
- **Experiment Type**: ML Fingerprinting
- **ANOVA Label Column**: SubjectID
- **Selection Mode**: fwe
- **Threshold**: 0.05
- **Expected Behavior**: Uses existing 'label' column (hot-encoded subjects). This is the **ideal match** scenario.
- **Use Case**: Subject fingerprinting with conservative feature selection to identify subject-specific features

### 3. `config_testanova_fwe_subjectid_in_classification_31-10-2025.yaml`
- **Experiment Type**: ML Classification
- **ANOVA Label Column**: SubjectID
- **Selection Mode**: fwe
- **Threshold**: 0.05
- **Expected Behavior**: Creates temporary 'anova_subject_label' column. This is the **mismatch** scenario.
- **Use Case**: Testing for subject memorization in a classification task - helps identify if model is learning subject-specific patterns rather than disease patterns

### 4. `config_testanova_fwe_group_in_fingerprinting_31-10-2025.yaml`
- **Experiment Type**: ML Fingerprinting
- **ANOVA Label Column**: Group
- **Selection Mode**: fwe
- **Threshold**: 0.05
- **Expected Behavior**: Creates temporary 'anova_group_label' column. This is the **mismatch** scenario.
- **Use Case**: Selecting features that distinguish disease groups during fingerprinting (unusual but valid for multi-disease fingerprinting)

### 5. `config_testanova_fwe_strict_31-10-2025.yaml`
- **Experiment Type**: ML Classification
- **ANOVA Label Column**: Group
- **Selection Mode**: fwe
- **Threshold**: 0.01
- **Expected Behavior**: Very strict feature selection (only p < 0.01 / numFeatures)
- **Use Case**: Ultra-conservative feature selection for high-confidence biomarker discovery

### 6. `config_testanova_fwe_lenient_31-10-2025.yaml`
- **Experiment Type**: ML Classification
- **ANOVA Label Column**: Group
- **Selection Mode**: fwe
- **Threshold**: 0.1
- **Expected Behavior**: More lenient feature selection (p < 0.1 / numFeatures)
- **Use Case**: Exploratory analysis with slightly relaxed family-wise error control

## Testing Strategy

### Scenario Coverage
✅ **Matched scenarios**: Configs 1 & 2 (no temp column creation needed)  
✅ **Mismatch scenarios**: Configs 3 & 4 (temp column creation required)  
✅ **Threshold variations**: Configs 5 & 6 (strict vs. lenient)  

### Expected Outputs
For each config, the transformer should:
1. Parse the FWE configuration correctly
2. Fit on training data with appropriate label column
3. Select features with p-values below threshold / numFeatures
4. Report number of selected features
5. Transform test data consistently
6. Clean up any temporary columns

### Key Testing Points

#### 1. Label Column Handling Logic
```python
if experiment_type == "ML Classification" and target_label_column == "Group":
    # Use existing 'label' column
elif experiment_type == "ML Fingerprinting" and target_label_column == "SubjectID":
    # Use existing 'label' column
else:
    # Create temporary ANOVA label column
```

#### 2. FWE Threshold Scaling
The actual p-value threshold used = `anova_selection_threshold / numFeatures`

For example:
- **Config 1-4**: threshold = 0.05, if 1000 features → accept features with p < 0.00005
- **Config 5**: threshold = 0.01, if 1000 features → accept features with p < 0.00001
- **Config 6**: threshold = 0.1, if 1000 features → accept features with p < 0.0001

#### 3. Comparison with Other Selection Modes
- **fwe**: Most conservative, Bonferroni correction
- **fdr**: Less conservative, Benjamini-Hochberg procedure
- **fpr**: False positive rate (no correction)
- **percentile**: Fixed percentage of features
- **numTopFeatures**: Fixed number of features

## Running the Tests

```bash
# Test matched scenario (Group classification)
py-neuro-env python start-pipelines.py --config config/config_testanova_fwe_group_classification_31-10-2025.yaml

# Test matched scenario (SubjectID fingerprinting)
py-neuro-env python start-pipelines.py --config config/config_testanova_fwe_subjectid_fingerprinting_31-10-2025.yaml

# Test mismatch scenario (SubjectID in classification)
py-neuro-env python start-pipelines.py --config config/config_testanova_fwe_subjectid_in_classification_31-10-2025.yaml

# Test mismatch scenario (Group in fingerprinting)
py-neuro-env python start-pipelines.py --config config/config_testanova_fwe_group_in_fingerprinting_31-10-2025.yaml

# Test strict threshold
py-neuro-env python start-pipelines.py --config config/config_testanova_fwe_strict_31-10-2025.yaml

# Test lenient threshold
py-neuro-env python start-pipelines.py --config config/config_testanova_fwe_lenient_31-10-2025.yaml
```

## Expected Feature Selection Results

Given the conservative nature of FWE:
- **Strict (0.01)**: Expect very few features selected (only strongest effects)
- **Standard (0.05)**: Expect moderate feature reduction (medium-strong effects)
- **Lenient (0.1)**: Expect more features selected (weaker effects included)

The exact number depends on:
1. Initial feature dimensionality
2. True effect sizes in the data
3. Between-group/subject variance

## Debugging Tips

If issues arise, check:
1. ✅ Is the transformer creating/using the correct label column?
2. ✅ Are temporary columns being cleaned up after transformation?
3. ✅ Is the feature count reasonable for the threshold?
4. ✅ Are p-values being correctly scaled by 1/numFeatures?
5. ✅ Does the transformer handle both fit and transform consistently?

## Related Files
- Transformer implementation: `eeg-pyspark-pipeline/eeg_spark_etl/features/transformers/anova_f_test_transformer.py`
- Original test config: `config/config_testanova_09-10-2025_1727.yaml`
- PySpark docs: `pyspark.ml.feature.UnivariateFeatureSelector`

---
**Created**: October 31, 2025  
**Purpose**: Comprehensive FWE mode testing for ANOVA F-test transformer

