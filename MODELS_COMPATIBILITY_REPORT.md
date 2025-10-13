# ML Models Compatibility Report: Grid Search vs Ax

## 📊 Summary

This report analyzes the compatibility of different ML models with both **Grid Search** and **Ax (Bayesian Optimization)** strategies in the EEG Ray Tuner pipeline.

---

## ✅ Fully Supported Models

### 1. **KNN (K-Nearest Neighbors)**
- **Grid Search**: ✅ Full support
- **Ax**: ✅ Full support
- **Parameters**:
  - `n_neighbors`: Integer (tune.randint)
  - `weights`: Categorical (tune.choice: ['uniform', 'distance'])
  - `metric`: Categorical (tune.choice: ['euclidean', 'manhattan', etc.])
- **Status**: **WORKING** (verified)

### 2. **Random Forest**
- **Grid Search**: ✅ Full support
- **Ax**: ✅ Custom configuration implemented
- **Parameters**:
  - `n_estimators`: Integer (tune.randint or tune.quniform)
  - `max_depth`: Integer or None (tune.randint or tune.choice)
  - `min_samples_split`: Integer (tune.randint)
  - `max_features`: Categorical (tune.choice: ['sqrt', 'log2', None])
- **Status**: **READY**

### 3. **XGBoost**
- **Grid Search**: ✅ Full support
- **Ax**: ✅ Custom configuration implemented
- **Parameters**:
  - `n_estimators`: Integer (tune.randint)
  - `max_depth`: Integer (tune.randint)
  - `learning_rate`: Float (tune.loguniform or tune.uniform)
  - `subsample`: Float (tune.uniform or tune.choice)
  - `colsample_bytree`: Float (tune.uniform or tune.choice)
- **Status**: **READY**

---

## ⚠️ Limited Support Models

### 4. **MLP (Neural Network)**
- **Grid Search**: ✅ Full support
  - Uses string representation of tuples: `"(50, 25)"` for hidden layers
  - Supports `activation`: ['relu', 'tanh', 'logistic']
  - Supports `alpha`: [0.0001, 0.001, 0.01, 0.1]
  
- **Ax**: ⚠️ **Default configuration only**
  - Config falls back to `use_default = True`
  - No custom search space implemented yet
  - **Potential Issues**:
    - Tuple format for `hidden_layer_sizes` needs proper handling
    - May not explore architecture space efficiently

**Recommendation**: 
- Grid Search: Use for systematic architecture exploration
- Ax: Will work but won't optimize architectures intelligently

### 5. **SVM (Support Vector Machine)**
- **Grid Search**: ✅ Full support
  - `C`: Float [0.1, 0.5, 1.0, 5.0, 10.0, 50.0]
  - `kernel`: Categorical ['rbf', 'linear', 'poly', 'sigmoid']
  - `gamma`: **Mixed type** ['scale', 'auto', 0.001, 0.01, 0.1]
  
- **Ax**: ⚠️ **Default configuration only**
  - Config falls back to `use_default = True`
  - **Potential Issues**:
    - `gamma` parameter has both string ('scale', 'auto') and numeric values
    - Ax may struggle with mixed-type parameters

**Recommendation**:
- Grid Search: Fully functional
- Ax: Test carefully - gamma parameter might cause issues

### 6. **Gradient Boosting**
- **Grid Search**: ✅ Full support
- **Ax**: ⚠️ **Default configuration only**
  - Similar to XGBoost parameters
  - Should work but no custom search space

**Status**: **Should work** but not optimized

### 7. **Decision Tree**
- **Grid Search**: ✅ Full support
  - `max_depth`: Can be None or integer
  - `max_features`: Can be 'sqrt', 'log2', None, or number
  
- **Ax**: ⚠️ **Default configuration only**
  - **Potential Issues**:
    - None values need special handling
    - Mixed type parameters

**Recommendation**: Use Grid Search for reliability

### 8. **Logistic Regression**
- **Grid Search**: ✅ Full support
- **Ax**: ⚠️ **Default configuration only**

**Status**: **Should work**

### 9. **AdaBoost**
- **Grid Search**: ✅ Full support
- **Ax**: ⚠️ **Default configuration only**

**Status**: **Should work**

---

## 🔧 Technical Details

### Ax Parameter Type Conversion

The `CustomAxSearcher` converts Ray Tune types to Ax format:

```python
✅ tune.uniform(low, high)     → Ax range (float)
✅ tune.randint(low, high)     → Ax range (int, inclusive bounds adjusted)
✅ tune.loguniform(low, high)  → Ax range (float, log_scale=True)
✅ tune.choice(categories)     → Ax choice (categorical, unordered)
```

### Potential Issues

1. **quniform → randint conversion**: 
   - Config uses `quniform(low, high, q)` 
   - Converted to `randint(low, high+1)` 
   - Should work but loses the "q" step information

2. **None values**:
   - Parameters like `max_depth=None` are passed as choice
   - Ax handles this as categorical parameter
   - Should work correctly

3. **String + Numeric mix** (e.g., gamma='scale' or gamma=0.01):
   - Ax expects consistent types within a parameter
   - **May cause errors** if not handled properly

4. **Tuple parameters** (MLP hidden_layer_sizes):
   - Stored as string `"(50, 25)"`
   - Needs special parsing in model instantiation
   - Grid Search handles this, Ax default config untested

---

## 🧪 Recommended Testing Order

### Phase 1: Verified Models (Start Here)
1. ✅ **KNN** - Fully tested and working
2. ✅ **Random Forest** - Custom Ax config, should work
3. ✅ **XGBoost** - Custom Ax config, should work

### Phase 2: Should Work (Test Next)
4. **Gradient Boosting** - Similar to XGBoost
5. **Logistic Regression** - Simple parameters
6. **AdaBoost** - Standard parameters

### Phase 3: Potential Issues (Test Carefully)
7. **SVM** - Mixed type gamma parameter
8. **Decision Tree** - None values
9. **MLP** - Tuple architecture, complex

---

## 🐛 Known Issues & Workarounds

### Issue 1: Ax "use_default" fallback
**Models affected**: MLP, SVM, Decision Tree, Gradient Boosting, Logistic Regression, AdaBoost

**Problem**: Config-maker sets `use_default=True` for these models in Ax, meaning custom hyperparameters aren't used.

**Workaround**: 
1. For now, use Grid Search for these models
2. Future: Implement custom Ax configurations similar to Random Forest/XGBoost

### Issue 2: Mixed-type parameters (SVM gamma)
**Problem**: SVM's `gamma` can be 'scale', 'auto', or numeric

**Workaround**:
1. In Grid Search: Use choice with both strings and numbers
2. In Ax: Might need to split into two separate experiments or use only numeric values

### Issue 3: Tuple parameters (MLP architectures)
**Problem**: `hidden_layer_sizes` expects tuple like `(50, 25)`

**Current handling**:
- Stored as string `"(50, 25)"` in config
- Model runner parses string to tuple
- Works for Grid Search
- Ax default config: **untested**

---

## 📋 Pre-Flight Checklist

Before running with multiple models, verify:

- [ ] **KNN**: Works with both strategies ✅
- [ ] **Random Forest**: Test with Ax custom config
- [ ] **XGBoost**: Test with Ax custom config
- [ ] **MLP**: Test Grid Search first, then Ax with defaults
- [ ] **SVM**: Watch for gamma parameter errors
- [ ] **Decision Tree**: Verify None handling
- [ ] **Others**: Start with Grid Search

---

## 🚀 Recommendations

### For Production Use:
1. **Start with Grid Search** for all models to ensure baseline functionality
2. **Add Ax for KNN, Random Forest, XGBoost** (fully supported)
3. **Test Ax with simpler models** (Logistic Regression, AdaBoost) next
4. **Use Grid Search for complex models** (MLP, SVM, Decision Tree) until custom Ax configs are implemented

### For Testing:
1. Run small test with KNN + Random Forest (both strategies)
2. Gradually add more models
3. Monitor for errors in Ax trials
4. Check that hyperparameters are actually being varied (not stuck on defaults)

---

## 📝 Future Enhancements

To fully support all models with Ax:

1. **Implement custom Ax configurations** for:
   - MLP (with architecture search)
   - SVM (handle mixed-type gamma)
   - Decision Tree (handle None values)
   - Gradient Boosting
   - Logistic Regression
   - AdaBoost

2. **Add parameter validation** before Ax experiment creation

3. **Create model-specific search space generators** in `ax_search_strategy.py`

---

## ✅ TL;DR

**SAFE TO USE NOW:**
- ✅ Grid Search: All models
- ✅ Ax: KNN, Random Forest, XGBoost

**TEST BEFORE RELYING ON:**
- ⚠️ Ax: MLP, SVM, Decision Tree, Gradient Boosting, Logistic Regression, AdaBoost

**RECOMMENDED APPROACH:**
1. Use Grid Search for everything initially
2. Enable Ax for KNN/Random Forest/XGBoost
3. Test other models one at a time with Ax
4. Check mega graphs to verify hyperparameters are varying

---

*Last Updated: 2025-10-13*
*Status: Ready for practice runs with recommended models*

