# 🐛 Bug Report: Multi-Model Test Run
**Date**: October 13, 2025  
**Config**: `config_testAxSearchAllModels_13-10-2025_1006.yaml`  
**Test Scope**: Random Forest, MLP, KNN, SVM with Grid Search & Ax strategies

---

## 📊 **EXECUTIVE SUMMARY**

| Strategy | Models Tested | ✅ Worked | ❌ Failed | Success Rate |
|----------|---------------|-----------|-----------|--------------|
| **Grid Search** | 4 | 3 | 1 | 75% |
| **Ax** | 4 | 2 | 2 | 50% |

**Critical Issues**: 3 major bugs identified  
**Graph Generation**: Failed for both strategies

---

## ✅ **WHAT WORKED**

### Grid Search ✅ (3/4 models)
1. **✅ Random Forest** - FULLY FUNCTIONAL
   - Trials: 4 (2 per fold)
   - Accuracy: ~77-78%
   - Config: Custom hyperparameters (`n_estimators`, `max_depth`, etc.)

2. **✅ KNN** - FULLY FUNCTIONAL
   - Trials: 20 (10 per fold)
   - Accuracy: ~45-51%
   - Config: `use_default: true` (10 default configs tested)

3. **✅ SVM** - FULLY FUNCTIONAL
   - Trials: 2 (1 per fold)
   - Accuracy: ~52-56%
   - Config: Custom hyperparameters (`C=0.5`, `kernel=rbf`, `gamma=auto`)

### Ax ✅ (2/4 models)
1. **✅ Random Forest** - FULLY FUNCTIONAL
   - Trials: 5
   - Accuracy: ~77.73%
   - Config: `use_default: true`
   - Best params: `{'n_estimators': 96, 'max_depth': 10, 'min_samples_split': 9, 'min_samples_leaf': 1}`

2. **✅ KNN** - FULLY FUNCTIONAL
   - Trials: 5
   - Accuracy: ~51.36%
   - Config: `use_default: true`
   - Best params: `{'n_neighbors': 5}`

---

## 🐛 **BUG #1: MLP `hidden_layer_sizes` Parameter Error**

### **Severity**: 🔴 **CRITICAL**

### **Affected Strategies**: Grid Search only (Ax failed differently)

### **Error Message**:
```
❌ Critical error training MLP (Neural Network): The 'hidden_layer_sizes' parameter of 
MLPClassifier must be an array-like or an int in the range [1, inf). Got '(5, 5)' instead.
```

### **Root Cause**:
The config specifies `hidden_layer_sizes: [(5, 5)]` in YAML, which gets converted to the **string** `'(5, 5)'` instead of a **tuple** `(5, 5)`.

### **Config (Lines 112-113)**:
```yaml
hidden_layer_sizes:
  - (5, 5)        # ❌ YAML interprets this as STRING '(5, 5)'
```

### **Expected Behavior**:
Should be parsed as a Python tuple `(5, 5)` or list of integers `[5, 5]`.

### **Fix Options**:
1. **Quick Fix**: Use list format in YAML:
   ```yaml
   hidden_layer_sizes:
     - [5, 5]     # ✅ This creates a list [5, 5]
   ```

2. **Proper Fix**: Update `config_handler.py` or `config-maker.py` to convert string tuples like `"(5, 5)"` to actual tuples:
   ```python
   import ast
   if isinstance(value, str) and value.startswith('('):
       value = ast.literal_eval(value)  # Converts "(5, 5)" -> (5, 5)
   ```

### **Impact**:
- Grid Search: 2 MLP trials failed (both folds)
- Ax: Not applicable (see Bug #2)

---

## 🐛 **BUG #2: Ax Using `default_param` Instead of Custom Search Space**

### **Severity**: 🔴 **CRITICAL**

### **Affected Models**: MLP, SVM in Ax strategy

### **Symptoms**:
- Ax generates trials with `default_param` instead of actual hyperparameters
- All trials report **0.0% accuracy**
- Models don't actually train

### **Evidence**:

#### MLP (Ax):
```
🔍 Search space: ['default_param']
Generated new trial 0 with parameters {'default_param': 0.491882}
...
Best accuracy: 0.0000
```

#### SVM (Ax):
```
🔍 Search space: ['default_param']
Generated new trial 0 with parameters {'default_param': 0.396376}
...
Best accuracy: 0.0000
```

### **Config (Lines 141-148)**:
```yaml
ax:
  models:
    - Random Forest
    - MLP (Neural Network)
    - KNN
    - SVM
  model_configs:
    ...
    MLP (Neural Network):
      use_default: true      # ❌ Using defaults
      num_samples: 5
    SVM:
      use_default: true      # ❌ Using defaults
      num_samples: 5
```

### **Root Cause**:
When `use_default: true` is set for Ax, the system is supposed to generate a default search space, but instead it's generating a **dummy parameter** `default_param` which causes the model to fail.

### **Expected Behavior**:
- `use_default: true` should generate appropriate default search spaces for each model type
- MLP should get: `hidden_layer_sizes`, `activation`, `alpha`, etc.
- SVM should get: `C`, `kernel`, `gamma`, etc.

### **Actual Behavior**:
- Ax creates a dummy `default_param` parameter
- Model training doesn't receive valid hyperparameters
- All trials report 0% accuracy

### **Code Location**:
Likely in `eeg-ray-tuner/eeg_ray_tuner/tuning/ax_search_strategy.py`:
- `build_search_space()` method
- `_convert_yaml_config_to_tune_space()` method

### **Fix Required**:
1. **Investigate** `ax_search_strategy.py` - the `build_search_space()` method
2. **Ensure** `use_default: true` generates proper default search spaces for MLP and SVM
3. **Alternative**: Always require explicit hyperparameter definitions for Ax (no `use_default`)

### **Impact**:
- MLP (Ax): 5 trials, all 0% accuracy, complete failure
- SVM (Ax): 5 trials, all 0% accuracy, complete failure

---

## 🐛 **BUG #3: Graph Generation Failure - "No fold data found"**

### **Severity**: 🟠 **HIGH**

### **Affected**: Both Grid Search and Ax strategies

### **Error Message**:
```
💥 CRITICAL ERROR generating best models multi-fold graph: No fold data found for any model
ValueError: No fold data found for any model
```

### **Symptoms**:
- Multi-fold graph generation fails for both strategies
- Error occurs in `multi_fold_graphs.py` line 107
- Graphs directory is empty

### **Evidence**:
```
2025-10-13 14:35:03 - ray_driver - INFO - 📊 Processing model: KNN
2025-10-13 14:35:03 - ray_driver - INFO - Found 2 fold directories for KNN
2025-10-13 14:35:03 - ray_driver - INFO - 📊 Processing model: Random_Forest
2025-10-13 14:35:03 - ray_driver - INFO - Found 2 fold directories for Random_Forest
2025-10-13 14:35:03 - ray_driver - INFO - 📊 Processing model: SVM
2025-10-13 14:35:03 - ray_driver - INFO - Found 2 fold directories for SVM
2025-10-13 14:35:03 - ray_driver - ERROR - 💥 CRITICAL ERROR: No fold data found for any model
```

### **Root Cause (Hypothesis)**:
The graph generator **finds** the fold directories but then fails to **extract data** from them. Likely issues:
1. Directory structure doesn't match expected pattern
2. Missing `results.json` or parquet files in expected locations
3. Directory naming mismatch (e.g., `sub-1_sub-37` vs `fold_0`)

### **Code Location**:
- `eeg-ray-tuner/eeg_ray_tuner/visualization/multi_fold_graphs.py` line 107
- `_load_multifold_model_data()` method

### **Debug Steps**:
1. Check directory structure: `ml_results_grid_search/KNN/`
2. Verify what files exist in fold directories
3. Compare with what `multi_fold_graphs.py` expects

### **Workaround**:
Graph generation fails but doesn't stop the pipeline - results are still saved correctly.

---

## ⚠️ **MINOR ISSUES**

### 1. **CRC File Warnings** (Low Priority)
**Symptom**:
```
⚠️  Failed to load directory: Could not read schema from '._SUCCESS.crc'
```
**Impact**: None (fallback method works)  
**Fix**: Ignore `.crc` files in data loading, or handle MacOS-specific hidden files better

### 2. **`debug` Directory Treated as Model** (Low Priority)
**Symptom**: Graph generator tries to process `ml_results_ax/debug/` as a model  
**Impact**: Warning only, no functional issue  
**Fix**: Already fixed in newer code - exclude `debug` from model detection

---

## 📋 **TESTING MATRIX**

| Model | Grid Search | Grid Accuracy | Ax | Ax Accuracy | Notes |
|-------|-------------|---------------|-----|-------------|-------|
| **Random Forest** | ✅ PASS | 77-78% | ✅ PASS | 77.73% | Both work perfectly |
| **MLP** | ❌ FAIL | N/A | ❌ FAIL | 0% | Bug #1 (Grid), Bug #2 (Ax) |
| **KNN** | ✅ PASS | 45-51% | ✅ PASS | 51.36% | Both work perfectly |
| **SVM** | ✅ PASS | 52-56% | ❌ FAIL | 0% | Grid works, Ax Bug #2 |

---

## 🔧 **PRIORITY FIXES**

### **IMMEDIATE (P0)**:
1. **Fix Bug #2**: Ax `default_param` issue for MLP and SVM
   - Investigate `ax_search_strategy.py`
   - Ensure `use_default: true` generates proper search spaces
   - Test with explicit YAML configs as workaround

2. **Fix Bug #1**: MLP `hidden_layer_sizes` tuple parsing
   - Update config parser to handle tuple strings
   - Or document proper YAML format: `[5, 5]` instead of `(5, 5)`

### **HIGH (P1)**:
3. **Fix Bug #3**: Graph generation for multi-fold
   - Debug `multi_fold_graphs.py` line 107
   - Check directory structure expectations
   - Verify data extraction logic

### **LOW (P2)**:
4. Filter out `.crc` files in data loading
5. Ensure `debug` directory is excluded from model detection (already done?)

---

## 🎯 **RECOMMENDATIONS**

### **For Immediate Testing**:
1. **MLP**: Use YAML list format `[5, 5]` instead of tuple `(5, 5)`
2. **Ax MLP/SVM**: Define explicit search spaces in YAML (don't use `use_default: true`)
   ```yaml
   MLP (Neural Network):
     use_default: false
     hyperparameters:
       hidden_layer_sizes:
         type: choice
         values: [[50], [100], [50, 25]]
       activation:
         type: choice
         values: ['relu', 'tanh']
   ```

### **For Production**:
1. **Always test with explicit hyperparameter configs** (avoid `use_default: true` for Ax)
2. **Add validation** in config-maker to prevent tuple-as-string issues
3. **Improve error messages** to distinguish between:
   - Config parsing errors (before model runs)
   - Model parameter errors (during model initialization)
   - Search space errors (during Ax setup)

---

## 📁 **OUTPUT SUMMARY**

### **Grid Search Results**:
```
✅ Total Models: 3 (Random Forest, KNN, SVM)
✅ Total Trials: 26 successful, 2 failed
✅ Best Model: Random Forest (78.97% accuracy)
📁 Location: data/testAxSearchAllModels/ml_results_grid_search/
```

### **Ax Results**:
```
✅ Total Models: 2 (Random Forest, KNN)
❌ Failed Models: 2 (MLP, SVM - 0% accuracy)
✅ Total Trials: 10 (5 per working model)
✅ Best Model: Random Forest (77.73% accuracy)
📁 Location: data/testAxSearchAllModels/ml_results_ax/
```

### **Strategy Comparison**:
```
✅ Generated: KNN_all_strategies.csv (15 trials)
✅ Generated: SVM_all_strategies.csv (1 trial - only Grid Search worked)
✅ Generated: comparison_summary.txt
📁 Location: data/testAxSearchAllModels/ml_strategies_comparison/
```

### **Graphs**:
```
❌ Grid Search graphs: FAILED (Bug #3)
❌ Ax graphs: FAILED (Bug #3)
✅ Comparison graphs: SUCCESS (2 graphs generated)
```

---

## 🔍 **FILES TO INVESTIGATE**

1. **`eeg-ray-tuner/eeg_ray_tuner/tuning/ax_search_strategy.py`**
   - `build_search_space()` method
   - `_convert_yaml_config_to_tune_space()` method
   - Default search space generation logic

2. **`config-maker.py` or `config_handler.py`**
   - Tuple/list parsing for `hidden_layer_sizes`
   - Type conversion for hyperparameter values

3. **`eeg-ray-tuner/eeg_ray_tuner/visualization/multi_fold_graphs.py`**
   - Line 107: `_load_multifold_model_data()` method
   - Fold directory structure expectations

---

## ✅ **NEXT STEPS**

1. ✅ **Document bugs** (this file)
2. ⏳ **Fix Bug #2** (Ax `default_param`) - CRITICAL
3. ⏳ **Fix Bug #1** (MLP tuple parsing) - CRITICAL
4. ⏳ **Fix Bug #3** (Graph generation) - HIGH
5. ⏳ **Re-run test** with fixes
6. ⏳ **Test with explicit Ax configs** (as workaround)

---

*Report generated from: `output.log` analysis*  
*Config file: `config/config_testAxSearchAllModels_13-10-2025_1006.yaml`*

