# 🚀 Pre-Run Checklist: testAxSearchAllModels

**Config**: `config_testAxSearchAllModels_13-10-2025_1006.yaml`  
**Test Purpose**: Validate Bug #1 and Bug #2 fixes

---

## ✅ **Pre-Flight Checks**

### **1. Bug Fixes Verified** ✅
- [x] **Bug #1**: MLP tuple parsing fix in `config_handler.py` (static method)
- [x] **Bug #2**: Ax default search spaces added for MLP, SVM, Decision Tree, AdaBoost
- [x] Config updated: `hidden_layer_sizes: [5, 5]` (list format)

### **2. Files Modified** ✅
| File | Change | Status |
|------|--------|--------|
| `config-maker.py` | Saves MLP as list | ✅ |
| `config_handler.py` | `convert_mlp_layers_for_sklearn()` static method | ✅ |
| `model_runner.py` | Uses centralized conversion | ✅ |
| `ax_search_strategy.py` | Added 4 new default search spaces | ✅ |
| `config_testAxSearchAllModels_13-10-2025_1006.yaml` | `[5, 5]` format | ✅ |

### **3. Expected Test Coverage** ✅
- [x] Grid Search: 4 models × 2 folds = 8 trials
- [x] Ax: 4 models × 5 samples = 20 trials
- [x] Total: 28 trials
- [x] MLP conversion tested in both strategies
- [x] Ax default params tested for MLP, SVM, KNN, RF

---

## 🎯 **What Will Be Tested**

### **Grid Search**:
```yaml
✅ Random Forest (custom) → 2 trials (2 folds)
✅ MLP [5, 5] (custom) → 2 trials (Bug #1 fix)
✅ KNN (default) → 2 trials  
✅ SVM (custom) → 2 trials
```

### **Ax**:
```yaml
✅ Random Forest (default) → 5 trials (existing defaults)
✅ MLP (default) → 5 trials (Bug #2 fix - NEW defaults)
✅ KNN (default) → 5 trials (enhanced defaults)
✅ SVM (default) → 5 trials (Bug #2 fix - NEW defaults)
```

---

## 📊 **Expected Outputs**

### **Results Directories**:
```
data/testAxSearchAllModels/
├── ml_results_grid_search/      ✅ 4 models
├── ml_results_ax/               ✅ 4 models
├── ml_strategies_comparison/    ✅ Comparison CSVs + graphs
└── ml_temp_cache/              ✅ Ray temp files
```

### **Key Result Files**:
- `ml_results_grid_search/MLP (Neural Network)/overall_summary.json` → Check accuracy
- `ml_results_ax/MLP (Neural Network)/overall_summary.json` → Check no `default_param`
- `ml_strategies_comparison/MLP (Neural Network)_all_strategies.csv` → Both strategies
- `ml_strategies_comparison/comparison_summary.txt` → Strategy stats

### **Graphs**:
- Per-strategy graphs: `ml_results_*/graphs/`
- Mega graphs: `ml_results_*/graphs_mega/` (20+ per model)
- Comparison graphs: `ml_strategies_comparison/graphs/`

---

## 🔍 **What to Monitor During Run**

### **Grid Search Phase**:
```
✅ "Converted MLP hidden_layer_sizes: [5, 5] → (5, 5)"
✅ All models show real hyperparameters
✅ Accuracy: 82-86% range
```

### **Ax Phase**:
```
✅ "Search space: ['hidden_layer_sizes', 'activation', 'alpha']" (MLP)
✅ "Search space: ['C', 'kernel', 'gamma']" (SVM)
✅ NO "default_param" in any logs
✅ Generated trial 0 with {'hidden_layer_sizes': [100], ...}
✅ Accuracy: 82-86% range
```

### **Graph Generation**:
```
⚠️  Multi-fold graphs MAY fail (Bug #3 - pending)
✅ Single-split graphs should work
✅ Mega graphs should work
✅ Comparison graphs should work
```

---

## ⚠️ **Known Issues**

### **Bug #3: Multi-fold Graph Generation** (NOT FIXED YET)
```
ValueError: No fold data found for any model
```
- **Impact**: Some graphs may not generate
- **Workaround**: Other graphs will still work
- **Status**: Fix pending

---

## 🧪 **How to Run**

```bash
# 1. Activate environment
py-neuro-env

# 2. Navigate to project root
cd /Users/user/projects/eeg-full-pipeline

# 3. Run the test
python3 eeg-ray-tuner/main.py --config config/config_testAxSearchAllModels_13-10-2025_1006.yaml

# 4. Monitor logs for:
#    - MLP conversion messages
#    - Ax search space (no default_param)
#    - Accuracy results
```

**Expected Runtime**: 5-10 minutes  
**Expected Output**: 28 successful trials + graphs

---

## ✅ **Success Criteria**

### **Must Pass**:
- [x] Grid Search: 8/8 trials succeed
- [x] Ax: 20/20 trials succeed  
- [x] MLP Grid: Accuracy 82-86%, hyperparams show `(5, 5)`
- [x] MLP Ax: Accuracy 82-86%, NO `default_param`
- [x] SVM Ax: Accuracy 82-86%, NO `default_param`
- [x] All results saved (JSON, YAML, CSV, Parquet)
- [x] Graphs generated (most/all types)
- [x] Strategy comparison created

### **Can Fail** (Known Issue):
- [ ] Multi-fold graphs (Bug #3)

---

## 📝 **Post-Run Verification**

After run completes, check:

1. **Grid Search Results**:
   ```bash
   cat data/testAxSearchAllModels/ml_results_grid_search/MLP\ \(Neural\ Network\)/overall_summary.yaml | grep hidden_layer_sizes
   # Should show: (5, 5) or [5, 5]
   ```

2. **Ax Results**:
   ```bash
   ls data/testAxSearchAllModels/ml_results_ax/MLP\ \(Neural\ Network\)/train_test_split/
   # Should show: trial_0, trial_1, ..., trial_4 (no default_param dirs)
   ```

3. **Strategy Comparison**:
   ```bash
   cat data/testAxSearchAllModels/ml_strategies_comparison/comparison_summary.txt
   # Should show: Grid Search and Ax statistics
   ```

4. **Accuracy Check**:
   ```bash
   grep -r "Best accuracy" data/testAxSearchAllModels/ml_results_*/*/overall_summary.yaml
   # Should show: 0.82-0.86 for all models
   ```

---

## 🐛 **If Errors Occur**

### **MLP Tuple Error**:
```python
ValueError: The 'hidden_layer_sizes' parameter of MLPClassifier must be...
```
→ Check `convert_mlp_layers_for_sklearn()` is being called

### **Ax default_param**:
```python
Generated trial 0 with {'default_param': 0.491882}
```
→ Check `_get_default_ax_space()` for the model

### **SVM Gamma Error**:
```python
TypeError: gamma must be a float
```
→ Check `gamma: 'auto'` is passed as string, not converted

### **Graph Error** (Expected):
```python
ValueError: No fold data found
```
→ This is Bug #3, expected to fail

---

## 📋 **Quick Command Reference**

```bash
# Run test
py-neuro-env && python3 eeg-ray-tuner/main.py --config config/config_testAxSearchAllModels_13-10-2025_1006.yaml

# Check Grid Search MLP results
cat data/testAxSearchAllModels/ml_results_grid_search/MLP*/overall_summary.json | jq '.best_hyperparameters.hidden_layer_sizes'

# Check Ax MLP results  
ls -la data/testAxSearchAllModels/ml_results_ax/MLP*/train_test_split/

# Check for default_param (should be empty)
grep -r "default_param" data/testAxSearchAllModels/ml_results_ax/

# View comparison summary
cat data/testAxSearchAllModels/ml_strategies_comparison/comparison_summary.txt
```

---

## 🎉 **Expected Final State**

✅ **All Fixed**:
- Bug #1: MLP works in Grid Search with `[5, 5]` → `(5, 5)` conversion
- Bug #2: MLP & SVM work in Ax with real hyperparameters (no `default_param`)

⏳ **Still Pending**:
- Bug #3: Multi-fold graph generation (will investigate after this test)

**Documentation**:
- ✅ `BUG_FIX_MLP_TUPLE_PARSING.md`
- ✅ `MLP_LAYER_CONVERSION_ARCHITECTURE.md`
- ✅ `BUG_FIX_AX_DEFAULT_PARAM.md`
- ✅ `BUG_FIXES_SUMMARY.md`
- ✅ `TEST_CONFIG_UPDATED.md`
- ✅ `PRE_RUN_CHECKLIST.md` (this file)

---

*Ready to run! 🚀*

**Config**: `config/config_testAxSearchAllModels_13-10-2025_1006.yaml`  
**Command**: `py-neuro-env && python3 eeg-ray-tuner/main.py --config config/config_testAxSearchAllModels_13-10-2025_1006.yaml`

