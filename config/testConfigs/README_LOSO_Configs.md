# LOSO Test Configurations

This directory contains various LOSO (Leave-One-Subject-Out) test configurations for the EEG pipeline. All configs use the same 4 subjects and Z-score standardization for consistency.

## Test Subjects
- **alz group**: sub-037, sub-038
- **cntrl group**: sub-035, sub-036

## Configuration Files

### 1. `config_loso_default_individual.yaml`
- **Type**: Individual LOSO (each subject as test)
- **Folds**: 4 folds (one per subject)
- **Test subjects per fold**: 1
- **Description**: Each subject gets its own test fold, regardless of group
- **Use case**: Testing individual subject performance

### 2. `config_loso_default_group.yaml`
- **Type**: Group-based LOSO (1 subject per group per fold)
- **Folds**: 2 folds
- **Test subjects per fold**: 2 (1 from each group)
- **Description**: Systematic selection ensuring balanced group representation
- **Use case**: Balanced cross-validation with group representation

### 3. `config_loso_custom_4subjects.yaml`
- **Type**: Custom group-based LOSO (2 subjects per group per fold)
- **Folds**: 1 fold
- **Test subjects per fold**: 4 (2 from each group)
- **Description**: Leaves out all subjects in one fold
- **Use case**: Testing with maximum test set size

### 4. `config_loso_individual_balanced.yaml`
- **Type**: Individual LOSO with balanced groups
- **Folds**: 4 folds (one per subject)
- **Test subjects per fold**: 1
- **Description**: Same as default individual but emphasizes balanced representation
- **Use case**: Individual testing with group balance awareness

### 5. `config_loso_group_2folds.yaml`
- **Type**: Group-based LOSO with 2 clear folds
- **Folds**: 2 folds
- **Test subjects per fold**: 2 (1 from each group)
- **Description**: Clear demonstration of 2-fold group-based LOSO
- **Use case**: Standard 2-fold cross-validation

### 6. `config_loso_edge_case_all.yaml`
- **Type**: Edge case - all subjects as test
- **Folds**: 1 fold
- **Test subjects per fold**: 4 (all subjects)
- **Description**: Edge case where all subjects are left out
- **Use case**: Testing edge case handling

## LOSO Types Explained

### Individual LOSO
- Each subject gets its own test fold
- `individual_loso: true`
- Each fold contains exactly 1 subject
- Good for: Individual subject analysis, maximum test coverage

### Group-based LOSO
- Systematic selection maintaining group balance
- `individual_loso: false`
- Each fold contains subjects from all groups
- Good for: Balanced cross-validation, group representation

## Testing with config-maker.py

To test these configurations with the config-maker:

```bash
# Test individual LOSO
python config-maker.py
# Select: LOSO (Leave-One-Subject-Out) - systematic cross-validation
# Select: Leave-One-Subject-Out (Individual) - each subject as test

# Test group-based LOSO
python config-maker.py
# Select: LOSO (Leave-One-Subject-Out) - systematic cross-validation
# Select: Default (2 subjects - 1 per group per fold)

# Test custom LOSO
python config-maker.py
# Select: LOSO (Leave-One-Subject-Out) - systematic cross-validation
# Select: Custom number of subjects
# Enter: 4 (for 2 per group per fold)
```

## Expected Directory Structures

### Individual LOSO
```
transformed/
├── sub-035/
├── sub-036/
├── sub-037/
└── sub-038/
```

### Group-based LOSO
```
transformed/
├── sub-035_sub-037/
└── sub-036_sub-038/
```

### Custom 4-subject LOSO
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
