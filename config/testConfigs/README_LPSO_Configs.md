# LPSO Test Configurations

This directory contains various LPSO (Leave-P-Subjects-Out) test configurations for the EEG pipeline. All configs use the same 4 subjects and Z-score standardization for consistency.

## Test Subjects
- **alz group**: sub-037, sub-038
- **cntrl group**: sub-035, sub-036

## Configuration Files

### 1. `config_lpso_default_individual.yaml`
- **Type**: Individual LPSO (each subject as test)
- **Folds**: 4 folds (one per subject)
- **Test subjects per fold**: 1
- **Description**: Each subject gets its own test fold, regardless of group
- **Use case**: Testing individual subject performance

### 2. `config_lpso_default_group.yaml`
- **Type**: Group-based LPSO (1 subject per group per fold)
- **Folds**: 2 folds
- **Test subjects per fold**: 2 (1 from each group)
- **Description**: Systematic selection ensuring balanced group representation
- **Use case**: Balanced cross-validation with group representation

### 3. `config_lpso_custom_4subjects.yaml`
- **Type**: Custom group-based LPSO (2 subjects per group per fold)
- **Folds**: 1 fold
- **Test subjects per fold**: 4 (2 from each group)
- **Description**: Leaves out all subjects in one fold
- **Use case**: Testing with maximum test set size

### 4. `config_lpso_individual_balanced.yaml`
- **Type**: Individual LPSO with balanced groups
- **Folds**: 4 folds (one per subject)
- **Test subjects per fold**: 1
- **Description**: Same as default individual but emphasizes balanced representation
- **Use case**: Individual testing with group balance awareness

### 5. `config_lpso_group_2folds.yaml`
- **Type**: Group-based LPSO with 2 clear folds
- **Folds**: 2 folds
- **Test subjects per fold**: 2 (1 from each group)
- **Description**: Clear demonstration of 2-fold group-based LPSO
- **Use case**: Standard 2-fold cross-validation

### 6. `config_lpso_edge_case_all.yaml`
- **Type**: Edge case - all subjects as test
- **Folds**: 1 fold
- **Test subjects per fold**: 4 (all subjects)
- **Description**: Edge case where all subjects are left out
- **Use case**: Testing edge case handling

## LPSO Types Explained

### Individual LPSO
- Each subject gets its own test fold
- `individual_lpso: true`
- Each fold contains exactly 1 subject
- Good for: Individual subject analysis, maximum test coverage

### Group-based LPSO
- Systematic selection maintaining group balance
- `individual_lpso: false`
- Each fold contains subjects from all groups
- Good for: Balanced cross-validation, group representation

## Testing with config-maker.py

To test these configurations with the config-maker:

```bash
# Test individual LPSO
python config-maker.py
# Select: LPSO (Leave-P-Subjects-Out) - systematic cross-validation
# Select: Leave-P-Subjects-Out (Individual) - each subject as test

# Test group-based LPSO
python config-maker.py
# Select: LPSO (Leave-P-Subjects-Out) - systematic cross-validation
# Select: Default (2 subjects - 1 per group per fold)

# Test custom LPSO
python config-maker.py
# Select: LPSO (Leave-P-Subjects-Out) - systematic cross-validation
# Select: Custom number of subjects
# Enter: 4 (for 2 per group per fold)
```

## Expected Directory Structures

### Individual LPSO
```
transformed/
├── sub-035/
├── sub-036/
├── sub-037/
└── sub-038/
```

### Group-based LPSO
```
transformed/
├── sub-035_sub-037/
└── sub-036_sub-038/
```

### Custom 4-subject LPSO
```
transformed/
└── sub-035_sub-036_sub-037_sub-038/
```

## Validation

Each config has been validated to ensure:
- ✅ Correct fold generation
- ✅ Proper group balance
- ✅ Valid subject counts
- ✅ Consistent metadata
- ✅ Z-score standardization only
- ✅ Same 4 test subjects across all configs
