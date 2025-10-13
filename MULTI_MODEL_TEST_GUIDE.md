# Multi-Model Test Guide

## 🧪 Test Configuration: `config_multimodel_test_13-10-2025.yaml`

Testing 5 models with both Grid Search and Ax strategies.

---

## 📊 Models Under Test

| Model | Grid Search Trials | Ax Trials | Complexity |
|-------|-------------------|-----------|------------|
| **KNN** | 12 (3×2×2) | 20 | Low ✅ |
| **MLP** | 12 (3×2×2) | 30 | Medium ⚠️ |
| **SVM** | 8 (2×2×2) | 25 | Medium ⚠️ |
| **Decision Tree** | 12 (3×2×2) | 20 | Low ✅ |
| **XGBoost** | 16 (2×2×2×2) | 40 | Medium ✅ |

**Total Trials:**
- Grid Search: 60 trials
- Ax: 135 trials
- **Grand Total: 195 trials**

---

## ⚠️ What to Watch For

### 1. **MLP (Neural Network)**
**Potential Issue**: Tuple string parsing for `hidden_layer_sizes`
- Grid Search: `['(50,)', '(100,)', '(50, 25)']` (strings)
- Ax: Same format
- **Watch for**: String → tuple conversion errors

**If it fails**: 
- Check logs for `hidden_layer_sizes` parsing errors
- May need to adjust string format

### 2. **SVM**
**Potential Issue**: Mixed-type `gamma` parameter
- Using only strings: `['scale', 'auto']` (should be safe)
- **Watch for**: Ax handling of categorical gamma

**If it fails**:
- Ax might struggle with string-only gamma
- Consider switching to numeric: `{type: loguniform, bounds: [0.001, 1.0]}`

### 3. **Decision Tree**
**Potential Issue**: `None` value handling
- `max_depth: [10, 20, 30, null]` (null = None)
- **Watch for**: None → null conversion issues

**If it fails**:
- Check if `null` is properly converted to Python `None`

### 4. **XGBoost** ✅
**Expected**: Should work perfectly
- Well-tested numeric parameters
- Ax has custom config support

### 5. **KNN** ✅
**Expected**: Should work perfectly
- Already verified working

---

## 🏃 How to Run

### Option 1: Using start-pipelines.py
```bash
cd /Users/user/projects/eeg-full-pipeline
python start-pipelines.py config/config_multimodel_test_13-10-2025.yaml
```

### Option 2: Direct Docker (if using containers)
```bash
docker run --rm \
  -v ./config/config_multimodel_test_13-10-2025.yaml:/app/config.yaml \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  your-image:tag python /app/main.py --config /app/config.yaml
```

---

## 📈 Expected Results Structure

```
data/multiModelTest/
├── processed_subjects/
├── transformed/
├── ml_results_grid_search/
│   ├── KNN/
│   ├── MLP (Neural Network)/
│   ├── SVM/
│   ├── Decision Tree/
│   ├── XGBoost/
│   ├── graphs/
│   ├── graphs_mega/          ← 100+ graphs!
│   ├── overall_summary.json
│   └── model_comparison.csv
├── ml_results_ax/
│   ├── KNN/
│   ├── MLP (Neural Network)/
│   ├── SVM/
│   ├── Decision Tree/
│   ├── XGBoost/
│   ├── graphs/
│   ├── graphs_mega/          ← 100+ graphs!
│   ├── overall_summary.json
│   └── model_comparison.csv
└── ml_strategies_comparison/
    ├── KNN_all_strategies.csv
    ├── MLP (Neural Network)_all_strategies.csv
    ├── SVM_all_strategies.csv
    ├── Decision Tree_all_strategies.csv
    ├── XGBoost_all_strategies.csv
    ├── strategy_performance.csv
    ├── comparison_summary.json
    └── graphs/
        ├── strategy_accuracy_comparison.png
        └── best_models_comparison.png
```

---

## ✅ Success Indicators

### During Execution:
- ✅ Grid Search completes all 60 trials
- ✅ Ax completes all 135 trials
- ✅ No Python errors in trial execution
- ✅ Hyperparameters are varying (not stuck on defaults)
- ✅ All 5 models run successfully

### In Results:
- ✅ Each model has results in both `ml_results_grid_search/` and `ml_results_ax/`
- ✅ `overall_summary.json` shows all 5 models
- ✅ `model_comparison.csv` has entries for all models
- ✅ Graphs generated for all models
- ✅ Strategy comparison shows all 5 models

### In Mega Graphs:
- ✅ ~20 graphs per model per strategy
- ✅ Clear epoch-level vs subject-level labels
- ✅ Metrics tables showing both accuracy types

---

## 🐛 Common Issues & Quick Fixes

### Issue 1: MLP hidden_layer_sizes Error
**Error**: `ValueError: invalid literal for int()`
**Fix**: Check if string → tuple parsing is working
**Quick workaround**: Use only simple architectures: `['(50,)', '(100,)']`

### Issue 2: SVM gamma Not Varying
**Symptom**: All Ax trials have same gamma value
**Fix**: Switch to numeric:
```yaml
gamma:
  type: loguniform
  bounds: [0.001, 1.0]
```

### Issue 3: Ax Trials Stuck at 0 Accuracy
**Symptom**: All Ax trials show 0% accuracy
**Check**: 
1. Feature count (should be >1 after ANOVA)
2. Data variance (features should vary)
3. Model hyperparameters are being applied

### Issue 4: Decision Tree "None" Error
**Error**: `TypeError: 'str' object cannot be interpreted as an integer`
**Fix**: Ensure `null` in YAML converts to Python `None`

---

## 📊 Performance Expectations

### Grid Search:
- **Time**: ~10-30 min (depends on data size)
- **Trials**: 60 total
- **Expected**: Systematic exploration, all combinations tested

### Ax:
- **Time**: ~20-60 min (135 trials)
- **Trials**: 135 total
- **Expected**: Intelligent exploration, may find better configs than Grid Search

### Comparison:
- Ax should explore more combinations
- Ax may find better hyperparameters (especially for XGBoost, MLP)
- Grid Search provides systematic baseline

---

## 🔍 Post-Test Analysis

### 1. Check Overall Performance
```bash
# Grid Search summary
cat data/multiModelTest/ml_results_grid_search/overall_summary.txt

# Ax summary
cat data/multiModelTest/ml_results_ax/overall_summary.txt

# Strategy comparison
cat data/multiModelTest/ml_strategies_comparison/comparison_summary.txt
```

### 2. Compare Strategies per Model
```bash
# View all KNN trials from both strategies
cat data/multiModelTest/ml_strategies_comparison/KNN_all_strategies.csv

# Same for other models
cat data/multiModelTest/ml_strategies_comparison/MLP\ \(Neural\ Network\)_all_strategies.csv
cat data/multiModelTest/ml_strategies_comparison/SVM_all_strategies.csv
cat data/multiModelTest/ml_strategies_comparison/Decision\ Tree_all_strategies.csv
cat data/multiModelTest/ml_strategies_comparison/XGBoost_all_strategies.csv
```

### 3. View Mega Graphs
```bash
# Grid Search graphs
open data/multiModelTest/ml_results_grid_search/graphs_mega/

# Ax graphs
open data/multiModelTest/ml_results_ax/graphs_mega/

# Strategy comparison graphs
open data/multiModelTest/ml_strategies_comparison/graphs/
```

---

## 📋 Test Completion Checklist

- [ ] Pipeline completes without fatal errors
- [ ] Grid Search: 60 trials completed
- [ ] Ax: 135 trials completed
- [ ] All 5 models present in both strategies
- [ ] Hyperparameters vary across trials (not all identical)
- [ ] Accuracies > 0% (models are actually learning)
- [ ] Mega graphs generated (check counts)
- [ ] Strategy comparison CSVs created
- [ ] No "use_default=True" in Ax model configs (verify custom configs are used)

---

## 🎯 Key Metrics to Track

### Model Performance:
1. **Best Accuracy per Model** (Grid Search vs Ax)
2. **Hyperparameter Sensitivity** (which params matter most)
3. **Convergence** (does Ax improve over time?)

### System Validation:
1. **Checkpoint Loading** (are models saved/loaded correctly?)
2. **Metric Consistency** (epoch-level vs subject-level)
3. **Graph Generation** (all graphs present?)

### Strategy Comparison:
1. **Winner per Model** (which strategy found better config?)
2. **Exploration Efficiency** (Ax vs Grid Search)
3. **Reliability** (both strategies agree on good configs?)

---

## 🚀 Next Steps After Test

### If Successful ✅:
1. Review `comparison_summary.txt` for strategy winner
2. Check mega graphs for insights
3. Note which models work best
4. Plan production runs with winning configs

### If Issues Found ⚠️:
1. Check compatibility report: `MODELS_COMPATIBILITY_REPORT.md`
2. Review logs for specific errors
3. Try models individually to isolate issues
4. Adjust YAML configs based on error messages

---

## 💡 Pro Tips

1. **Start Small**: If first run fails, reduce `num_samples` for Ax
2. **Check Features**: Run `inspect_parquet.py` on transformed data to verify features
3. **Monitor Resources**: Watch CPU/memory during execution
4. **Save Logs**: Keep terminal output for debugging
5. **Compare Configs**: Look at which hyperparameters Ax prefers vs Grid Search

---

*Good luck with your test run! 🚀*

**Expected Duration**: ~30-90 minutes total
**Expected Graphs**: 200+ graphs across all models and strategies
**Expected CSVs**: 10+ comparison and result files

