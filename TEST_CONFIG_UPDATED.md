# ✅ Updated Test Config: testAxSearchAllModels

**Config File**: `config_testAxSearchAllModels_13-10-2025_1006.yaml`  
**Date Updated**: October 13, 2025  
**Purpose**: Test all bug fixes (Bug #1 and Bug #2)

---

## 🔧 **Changes Made**

### **Line 113: MLP hidden_layer_sizes Format**

**Before** (Tuple format - would fail):
```yaml
hidden_layer_sizes:
  - (5, 5)  ❌ Old format
```

**After** (List format - Bug #1 fix):
```yaml
hidden_layer_sizes:
  - [5, 5]  ✅ New format
```

**Why**: 
- Lists serialize cleanly in YAML
- `config_handler.py` converts to tuple for sklearn
- Uses new centralized `convert_mlp_layers_for_sklearn()` method

---

## 🧪 **What This Test Will Validate**

### **Grid Search** (Lines 91-130):

| Model | Config | Tests |
|-------|--------|-------|
| **Random Forest** | Custom params | ✅ Standard model |
| **MLP** | Custom `[5, 5]` | ✅ **Bug #1 Fix**: List → tuple conversion |
| **KNN** | `use_default: true` | ✅ Default Grid Search params |
| **SVM** | Custom params | ✅ Standard model |

**Expected Results**:
- ✅ All 4 models train successfully
- ✅ MLP correctly converts `[5, 5]` → `(5, 5)` for sklearn
- ✅ Accuracy: 82-86% for all models
- ✅ Total trials: 8 (2 folds × 4 models)

---

### **Ax** (Lines 131-151):

| Model | Config | Tests |
|-------|--------|-------|
| **Random Forest** | `use_default: true` | ✅ Existing default search space |
| **MLP** | `use_default: true` | ✅ **Bug #2 Fix**: New default search space |
| **KNN** | `use_default: true` | ✅ Enhanced default (weights, metric) |
| **SVM** | `use_default: true` | ✅ **Bug #2 Fix**: New default search space |

**Expected Results**:
- ✅ All 4 models use real hyperparameters (no `default_param`)
- ✅ MLP gets: hidden_layer_sizes, activation, alpha
- ✅ SVM gets: C, kernel, gamma
- ✅ KNN gets: n_neighbors, weights, metric
- ✅ RF gets: n_estimators, max_depth, etc.
- ✅ Accuracy: 82-86% for all models
- ✅ Total trials: 20 (5 samples × 4 models)

---

## 📊 **Test Coverage**

### **Bug #1: MLP Tuple Parsing**
- ✅ **Grid Search**: Tests `[5, 5]` format with custom config
- ✅ **Ax**: Tests default search space with choice of architectures
- ✅ **Conversion**: Uses centralized `convert_mlp_layers_for_sklearn()`

### **Bug #2: Ax Default Param**
- ✅ **MLP**: Tests new default search space (3 params)
- ✅ **SVM**: Tests new default search space (3 params)
- ✅ **KNN**: Tests enhanced default (3 params)
- ✅ **RF**: Tests existing default (4 params)

### **Overall System**
- ✅ Dual strategy execution (Grid Search + Ax)
- ✅ 2 CV folds per strategy
- ✅ Resource management (6 CPUs, 12GB RAM)
- ✅ Result saving and aggregation
- ✅ Graph generation (single-split, mega, comparison)
- ✅ Strategy comparison module

---

## 📁 **Expected Output Structure**

```
data/testAxSearchAllModels/
├── ml_results_grid_search/
│   ├── Random Forest/
│   │   ├── fold_1/
│   │   ├── fold_2/
│   │   └── ... (results, graphs)
│   ├── MLP (Neural Network)/  ✅ Bug #1: Should work!
│   │   ├── fold_1/
│   │   ├── fold_2/
│   │   └── ... (results with [5,5] → (5,5))
│   ├── KNN/
│   ├── SVM/
│   └── graphs/
│
├── ml_results_ax/
│   ├── Random Forest/
│   │   ├── train_test_split/
│   │   │   ├── trial_0/  ✅ Real params!
│   │   │   ├── trial_1/
│   │   │   └── ...
│   │   └── ... (results, graphs)
│   ├── MLP (Neural Network)/  ✅ Bug #2: Should work!
│   │   └── train_test_split/
│   │       ├── trial_0/  ✅ No default_param!
│   │       └── ... (real hidden_layer_sizes, activation, alpha)
│   ├── KNN/  ✅ Enhanced defaults!
│   │   └── ... (n_neighbors, weights, metric)
│   ├── SVM/  ✅ Bug #2: Should work!
│   │   └── ... (C, kernel, gamma)
│   ├── debug/
│   └── graphs/
│
├── ml_strategies_comparison/
│   ├── strategy_performance.csv
│   ├── KNN_all_strategies.csv
│   ├── MLP (Neural Network)_all_strategies.csv
│   ├── Random Forest_all_strategies.csv
│   ├── SVM_all_strategies.csv
│   ├── comparison_summary.txt
│   └── graphs/
│
└── ml_temp_cache/
    └── ... (Ray Tune temp files)
```

---

## ✅ **Success Criteria**

### **Must Pass**:
1. ✅ **Grid Search MLP**: Trains with `[5, 5]`, converts to `(5, 5)`, gets 82-86%
2. ✅ **Ax MLP**: Uses default search space, no `default_param`, gets 82-86%
3. ✅ **Ax SVM**: Uses default search space, no `default_param`, gets 82-86%
4. ✅ All 8 models complete successfully (4 Grid + 4 Ax)
5. ✅ Total trials: 28 (8 Grid + 20 Ax)
6. ✅ All results saved correctly (parquet, JSON, YAML, CSV)
7. ✅ All graphs generated (per-strategy + comparison)

### **Key Files to Check**:
- `ml_results_grid_search/MLP (Neural Network)/*/results.json` → Check hyperparams show `(5, 5)`
- `ml_results_ax/MLP (Neural Network)/*/results.json` → No `default_param`, real params
- `ml_results_ax/SVM/*/results.json` → No `default_param`, real C/kernel/gamma
- `ml_strategies_comparison/MLP (Neural Network)_all_strategies.csv` → Both strategies present

### **Logs to Monitor**:
```
✅ Converted MLP hidden_layer_sizes: [5, 5] → (5, 5)
✅ Search space: ['hidden_layer_sizes', 'activation', 'alpha']  (Not 'default_param'!)
✅ Generated trial 0 with {'hidden_layer_sizes': [100], 'activation': 'relu', ...}
✅ Best accuracy: 0.8235
```

---

## 🚀 **How to Run**

```bash
# Activate Python environment
py-neuro-env

# Run the test
python3 main.py --config config/config_testAxSearchAllModels_13-10-2025_1006.yaml

# Expected runtime: 5-10 minutes
# Expected output: 28 successful trials
```

---

## 📋 **Verification Checklist**

After run completes, verify:

- [ ] Grid Search completed: 8 trials (4 models × 2 folds)
- [ ] Ax completed: 20 trials (4 models × 5 samples)
- [ ] MLP Grid Search: `hidden_layer_sizes` is `(5, 5)` in results
- [ ] MLP Ax: No `default_param`, has real params
- [ ] SVM Ax: No `default_param`, has C/kernel/gamma
- [ ] All accuracies: 82-86% range
- [ ] Graphs generated: single-split, mega, comparison
- [ ] No errors in logs
- [ ] Strategy comparison shows both strategies

---

## 🐛 **What If It Fails?**

### **If MLP Grid Search Fails**:
- Check `hidden_layer_sizes` conversion in logs
- Verify `config_handler.py` is parsing `[5, 5]` correctly
- Check `model_runner.py` is converting to tuple

### **If MLP Ax Fails**:
- Check if `default_param` appears in logs
- Verify `_get_default_ax_space()` is being called
- Check search space in Ax experiment creation

### **If SVM Ax Fails**:
- Same checks as MLP Ax
- Verify `gamma: 'auto'` is handled correctly (string value)

### **If Graphs Fail** (Bug #3):
- This is expected (pending fix)
- Note the error for Bug #3 investigation
- Other graphs should still work

---

## 📝 **Notes**

- This config uses **4 subjects total** (2 per group)
- **LPSO with 2 folds**: Each fold tests on different subjects
- **Grid Search**: Exhaustive search (small space for testing)
- **Ax**: Bayesian optimization (5 samples per model for quick test)
- **Feature selection**: ANOVA at 50% → should give ~19 features
- **Expected data quality**: Good (not the 1-feature issue from before)

---

*Config updated and ready to test both bug fixes! 🧪*

