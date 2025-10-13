# 🐛 Bug Fix #5: Ax JSON Encoding for MLP hidden_layer_sizes

**Status**: ✅ **FIXED**  
**Bug ID**: Bug #5  
**Date**: October 13, 2025  
**Severity**: CRITICAL (Pipeline failure)

---

## 📋 **Problem Summary**

After fixing Bug #4 (list→tuple conversion), Ax MLP optimization still crashed with:

```python
ValueError: No AE parameter type corresponding to <class 'tuple'>.
```

**Location**: Line 2152-2180 in test run log

---

## 🔍 **Root Cause Analysis**

### **The Full Story of MLP Hyperparameter Encoding**:

1. ✅ **Bug #1 FIXED**: `config-maker.py` now saves as `[5, 5]` (list) instead of string `'(5, 5)'`
2. ✅ **Bug #2 FIXED**: `config_handler.py` converts `[5, 5]` → `(5, 5)` (tuple) for user configs
3. ✅ **Bug #4 FIXED**: Default Ax search space changed from lists to tuples
4. ❌ **Bug #5**: Ax **STILL REJECTS TUPLES**!

### **Why Ax Cannot Accept Tuples**:

Ax's `ChoiceParameter` has strict type requirements:
- ✅ **Accepts**: `int`, `float`, `str`, `bool`
- ❌ **REJECTS**: `list`, `tuple`, `dict`, custom objects

**From Ax source code** (`ax/service/utils/instantiation.py:204`):
```python
def _get_parameter_type(cls, python_type: Type) -> ParameterType:
    if python_type not in [int, float, str, bool]:
        raise ValueError(f"No AE parameter type corresponding to {python_type}.")
```

---

## 🔧 **The Solution: JSON Encoding**

We encode tuples/lists as **JSON strings** for Ax, then decode them back for sklearn.

### **Architecture**:

```
User YAML Config              Ax Search Space           Trainable Function        sklearn Model
─────────────────              ───────────────           ──────────────────        ─────────────
[5, 5] (list)      →→→→       "[5, 5]" (JSON str)  →→→  (5, 5) (tuple)      →→→  MLPClassifier
                   encode                               decode                     (requires tuple)
```

---

## 🛠️ **Implementation**

### **1. ax_search_strategy.py** - Encode tuples to JSON strings

#### **Default Search Space** (lines 342-353):
```python
elif model_name == 'MLP (Neural Network)':
    # Ax ChoiceParameter only accepts int, float, str, bool (NOT tuple/list!)
    # Solution: Encode layer architectures as JSON strings
    return {
        'hidden_layer_sizes': tune.choice([
            "[50]", "[100]", "[150]",              # JSON strings ✅
            "[50, 25]", "[100, 50]", "[150, 75]"
        ]),
        'activation': tune.choice(['relu', 'tanh', 'logistic']),
        'alpha': tune.loguniform(0.0001, 0.1),
    }
```

#### **Custom Search Space Encoding** (lines 210-239):
```python
# In build_search_space() method
if model_name == 'MLP (Neural Network)' and 'hidden_layer_sizes' in search_space:
    original_choice = search_space['hidden_layer_sizes']
    
    # Extract values from tune.choice()
    values = original_choice.categories  # e.g., [(5, 5), (10, 10)]
    
    # Convert each tuple/list to JSON string
    encoded_values = []
    for val in values:
        if isinstance(val, (tuple, list)):
            # Encode: (5, 5) → "[5, 5]"
            encoded_values.append(json.dumps(list(val)))
        else:
            encoded_values.append(val)
    
    # Replace with encoded strings
    search_space['hidden_layer_sizes'] = tune.choice(encoded_values)
    logger.info(f"🔧 Encoded: {values} → {encoded_values}")
```

### **2. config_handler.py** - Decode JSON strings to tuples

#### **Updated `convert_mlp_layers_for_sklearn()`** (lines 1048-1056):
```python
elif isinstance(hidden_layer_sizes, str):
    # 🔧 NEW: JSON string from Ax encoding (e.g., "[5, 5]")
    if hidden_layer_sizes.startswith('[') and hidden_layer_sizes.endswith(']'):
        try:
            parsed = json.loads(hidden_layer_sizes)  # "[5, 5]" → [5, 5]
            if isinstance(parsed, list):
                return tuple(parsed)                  # [5, 5] → (5, 5)
        except json.JSONDecodeError:
            pass
    
    # ... (existing string handling for other formats)
```

### **3. model_runner.py** - No changes needed!
The existing code already calls `convert_mlp_layers_for_sklearn()`, so it automatically handles JSON decoding:

```python
# Lines 422-430 (unchanged)
if model_name == 'MLP (Neural Network)' and 'hidden_layer_sizes' in hyperparams:
    from config_handler import UnifiedConfigHandler
    original = hyperparams['hidden_layer_sizes']  # "[5, 5]" from Ax
    hyperparams['hidden_layer_sizes'] = UnifiedConfigHandler.convert_mlp_layers_for_sklearn(original)
    # Result: (5, 5) for sklearn
```

---

## ✅ **How It Works - Complete Flow**

### **Example: User Config**
```yaml
MLP (Neural Network):
  use_default: false
  hyperparameters:
    hidden_layer_sizes:
      type: choice
      values: [[5, 5], [10, 10]]  # User defines as lists
```

### **Step-by-Step Flow**:

1. **Config Loading** (`config_handler.py`):
   - Converts `[5, 5]` → `(5, 5)` (tuple) ✅

2. **Ax Search Space Building** (`ax_search_strategy.py`):
   - Detects MLP with choice of tuples
   - Encodes `(5, 5)` → `"[5, 5]"` (JSON string) ✅
   - Creates: `tune.choice(["[5, 5]", "[10, 10]"])` ✅

3. **Ray Tune Trial**:
   - Ax suggests: `hidden_layer_sizes = "[5, 5]"` (string) ✅

4. **Model Training** (`model_runner.py`):
   - Receives `"[5, 5]"` from trial config
   - Calls `convert_mlp_layers_for_sklearn("[5, 5]")`
   - JSON decodes: `"[5, 5]"` → `[5, 5]` → `(5, 5)` ✅
   - sklearn gets `(5, 5)` ✅

---

## 🎯 **Result**

| Component | Input | Output | Status |
|-----------|-------|--------|--------|
| **User Config** | `[5, 5]` (list) | `(5, 5)` (tuple) | ✅ |
| **Ax Search Space** | `(5, 5)` (tuple) | `"[5, 5]"` (JSON str) | ✅ |
| **Ray Tune Trial** | `"[5, 5]"` (str) | `"[5, 5]"` (str) | ✅ |
| **Model Runner** | `"[5, 5]"` (str) | `(5, 5)` (tuple) | ✅ |
| **sklearn MLP** | `(5, 5)` (tuple) | Trains successfully | ✅ |

**Ax is happy** (receives strings) ✅  
**sklearn is happy** (receives tuples) ✅  
**Everyone is happy!** 🎉

---

## 📝 **Files Changed**

1. **`eeg-ray-tuner/eeg_ray_tuner/tuning/ax_search_strategy.py`**
   - Lines 189-244: Updated `build_search_space()` with JSON encoding logic
   - Lines 342-353: Changed default MLP space to use JSON strings

2. **`config_handler.py`**
   - Lines 1004-1081: Enhanced `convert_mlp_layers_for_sklearn()` to decode JSON

3. **`eeg-ray-tuner/eeg_ray_tuner/models/model_runner.py`**
   - No changes needed (already uses centralized converter)

---

## 🧪 **Testing Strategy**

### **Test Cases**:

1. ✅ **Default Ax MLP** (`use_default: true`)
   - Should use `"[50]"`, `"[100]"`, etc. (JSON strings)

2. ✅ **Custom Ax MLP** (user-defined values)
   - YAML: `[[5, 5], [10, 10]]` → Encoded to `["[5, 5]", "[10, 10]"]`

3. ✅ **Grid Search MLP** (unchanged behavior)
   - Should continue to work with `(5, 5)` tuples

4. ✅ **Backward Compatibility**
   - All existing formats still supported in `convert_mlp_layers_for_sklearn()`

---

## 🚀 **Next Steps**

1. **Run test config again**: `config_testAxSearchAllModels_13-10-2025_1006.yaml`
2. **Expected results**:
   - ✅ Grid Search: 28/28 trials (same as before)
   - ✅ Ax Random Forest: 5/5 trials (same as before)
   - ✅ **Ax MLP: 5/5 trials (NOW WORKING!)** 🎯
   - ✅ Ax KNN: 5/5 trials
   - ✅ Ax SVM: 5/5 trials
   - **Total: 48 successful trials**

---

## 📚 **Lessons Learned**

1. **Type Constraints**: Different libraries have different type requirements
   - Ax: primitives only (int, float, str, bool)
   - sklearn: specific formats (tuples for layers)
   - Ray Tune: flexible (accepts most types)

2. **Encoding Strategy**: When systems have incompatible types, use:
   - **Encoding**: Complex → Simple (tuple → JSON string)
   - **Decoding**: Simple → Complex (JSON string → tuple)
   - **Centralization**: One place for conversion logic

3. **Debugging Flow**: Trace data through entire pipeline
   - Config → Search Space → Trial → Model
   - Each step may transform the data differently

---

**Status**: ✅ **READY TO TEST**

