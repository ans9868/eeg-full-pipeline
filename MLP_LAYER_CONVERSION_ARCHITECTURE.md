# 🏗️ MLP Layer Conversion Architecture

**Centralized in**: `config_handler.py`  
**Method**: `UnifiedConfigHandler.convert_mlp_layers_for_sklearn()`  
**Status**: ✅ **Refactored & Centralized**

---

## 📋 **Overview**

The MLP `hidden_layer_sizes` parameter requires special handling because:
1. **YAML serialization**: Tuples become strings `"(5, 5)"`
2. **sklearn requirement**: MLPClassifier requires tuple format `(5, 5)`
3. **Multiple formats**: Configs can have lists `[5, 5]`, tuples `(5, 5)`, or strings

**Solution**: Centralized conversion logic in `config_handler.py` that all components use.

---

## 🏛️ **Architecture**

### **Two-Method Approach**

1. **`_convert_mlp_architectures()`** (Instance Method)
   - **Purpose**: Validate and normalize during config loading
   - **Input**: Various formats (strings, tuples, lists)
   - **Output**: Clean lists `[[5, 5], [100]]`
   - **Used by**: Config validation (Grid Search & Ax)
   - **When**: During config loading/validation

2. **`convert_mlp_layers_for_sklearn()`** (Static Method) ✨ **NEW**
   - **Purpose**: Convert to sklearn-compatible tuple
   - **Input**: Any format (list, tuple, string, int)
   - **Output**: Tuple `(5, 5)` or `(100,)`
   - **Used by**: Model runners, strategies
   - **When**: Before passing to MLPClassifier

---

## 🔄 **Data Flow**

### **1. Config Creation** (`config-maker.py`)
```python
# User inputs: 2 layers, 5 neurons each
layer_sizes = [5, 5]
mlp_architectures.append(layer_sizes)  # Store as list

# YAML output:
# hidden_layer_sizes: [[5, 5]]  ✅ List of lists
```

### **2. Config Loading** (`config_handler.py`)
```python
# Validation converts any format to lists
def _convert_mlp_architectures(architectures, context):
    # Handles: "(5, 5)" → [5, 5]
    # Handles: [5, 5] → [5, 5] (validates)
    # Handles: (5, 5) → [5, 5]
    return [[5, 5]]  # Always returns list of lists
```

### **3. Strategy Usage** (Grid Search / Ax)
```python
# Grid Search: wraps in tune.grid_search()
search_space = {
    'hidden_layer_sizes': tune.grid_search([[5, 5], [100]])
}

# Ax: wraps in choice or custom search
# Lists work fine here
```

### **4. Model Instantiation** (`model_runner.py`)
```python
# Uses centralized conversion
from config_handler import UnifiedConfigHandler

hyperparams['hidden_layer_sizes'] = [5, 5]  # From config

# Convert to sklearn format
hyperparams['hidden_layer_sizes'] = \
    UnifiedConfigHandler.convert_mlp_layers_for_sklearn([5, 5])
# → (5, 5)  ✅ Tuple for sklearn

model = MLPClassifier(hidden_layer_sizes=(5, 5))  # ✅ Works!
```

---

## 📚 **Method Details**

### **`convert_mlp_layers_for_sklearn()` - Static Method**

**Location**: `config_handler.py` lines 1003-1066

**Signature**:
```python
@staticmethod
def convert_mlp_layers_for_sklearn(
    hidden_layer_sizes: Union[List[int], Tuple[int], Any]
) -> Tuple[int]:
```

**Handles**:
- ✅ `[5, 5]` → `(5, 5)`
- ✅ `[100]` → `(100,)`
- ✅ `(5, 5)` → `(5, 5)` (already tuple)
- ✅ `"(5, 5)"` → `(5, 5)` (parses string)
- ✅ `100` → `(100,)` (single layer)

**Why Static?**
- Can be called without config_handler instance
- Reusable across different modules
- Clear single responsibility: format conversion only

**Example Usage**:
```python
from config_handler import UnifiedConfigHandler

# In model_runner.py
layers_tuple = UnifiedConfigHandler.convert_mlp_layers_for_sklearn([5, 5])
# Returns: (5, 5)

# In grid_search_strategy.py (if needed)
sklearn_format = UnifiedConfigHandler.convert_mlp_layers_for_sklearn(config_value)
```

---

## 🔌 **Integration Points**

### **1. model_runner.py** (Lines 422-430)
```python
# 🔧 FIX: Convert MLP hidden_layer_sizes to sklearn-compatible tuple format
# Uses centralized conversion from UnifiedConfigHandler
if model_name == 'MLP (Neural Network)' and 'hidden_layer_sizes' in hyperparams:
    from config_handler import UnifiedConfigHandler
    original = hyperparams['hidden_layer_sizes']
    hyperparams['hidden_layer_sizes'] = \
        UnifiedConfigHandler.convert_mlp_layers_for_sklearn(original)
    self.logger.debug(
        f"Converted MLP hidden_layer_sizes: {original} → {hyperparams['hidden_layer_sizes']}"
    )
```

### **2. config_handler.py** (Grid Search Validation)
```python
# Lines 815-820
if model_name == "MLP (Neural Network)" and "hidden_layer_sizes" in hyperparams:
    hyperparams["hidden_layer_sizes"] = self._convert_mlp_architectures(
        hyperparams["hidden_layer_sizes"], 
        f"Grid Search {model_name}"
    )
```

### **3. config_handler.py** (Ax Validation)
```python
# Lines 1072-1077
if model_name == "MLP (Neural Network)" and param_name == "hidden_layer_sizes":
    param_config["values"] = self._convert_mlp_architectures(
        values, 
        f"Ax {model_name}"
    )
```

---

## ✅ **Benefits of Centralization**

### **Before** (Distributed Logic):
```
config-maker.py:    Saves as string "(5, 5)" ❌
config_handler.py:  No validation ❌
model_runner.py:    if isinstance(list): tuple() ⚠️
```

### **After** (Centralized):
```
config-maker.py:    Saves as list [5, 5] ✅
config_handler.py:  
  ├─ _convert_mlp_architectures() → Validates & normalizes ✅
  └─ convert_mlp_layers_for_sklearn() → Converts to sklearn format ✅
model_runner.py:    Uses centralized method ✅
```

### **Advantages**:
1. ✅ **Single Source of Truth**: One method for sklearn conversion
2. ✅ **Reusable**: Static method usable anywhere
3. ✅ **Maintainable**: Fix bugs in one place
4. ✅ **Testable**: Isolated logic, easy to unit test
5. ✅ **Documented**: Clear docstrings with examples

---

## 🧪 **Testing**

### **Test the Static Method**:
```python
from config_handler import UnifiedConfigHandler

# Test cases
assert UnifiedConfigHandler.convert_mlp_layers_for_sklearn([5, 5]) == (5, 5)
assert UnifiedConfigHandler.convert_mlp_layers_for_sklearn([100]) == (100,)
assert UnifiedConfigHandler.convert_mlp_layers_for_sklearn((5, 5)) == (5, 5)
assert UnifiedConfigHandler.convert_mlp_layers_for_sklearn("(5, 5)") == (5, 5)
assert UnifiedConfigHandler.convert_mlp_layers_for_sklearn(100) == (100,)
```

### **Integration Test**:
```yaml
# config.yaml
ray:
  grid_search:
    models:
      - MLP (Neural Network)
    model_configs:
      MLP (Neural Network):
        hyperparameters:
          hidden_layer_sizes:
            - [5, 5]      # List format
            - [100]       # Single layer
            - [50, 25]    # Two layers
```

**Expected**:
1. Config validation: Lists validated and normalized ✅
2. Model training: Converted to tuples `(5, 5)`, `(100,)`, `(50, 25)` ✅
3. sklearn MLPClassifier: Receives correct tuples ✅

---

## 📊 **Comparison**

| Aspect | Old Approach | New Centralized Approach |
|--------|--------------|--------------------------|
| **Storage** | String `"(5, 5)"` | List `[5, 5]` |
| **Validation** | None | In `_convert_mlp_architectures()` |
| **Conversion** | In `model_runner.py` only | Centralized static method |
| **Reusability** | Low (coupled to model_runner) | High (static, importable) |
| **Maintenance** | Hard (scattered logic) | Easy (single method) |
| **Testing** | Difficult | Easy (isolated static method) |
| **Documentation** | Minimal | Comprehensive with examples |

---

## 🔍 **Code Locations**

| File | Lines | Purpose |
|------|-------|---------|
| `config_handler.py` | 919-1001 | `_convert_mlp_architectures()` - Validation |
| `config_handler.py` | 1003-1066 | `convert_mlp_layers_for_sklearn()` - Sklearn conversion |
| `config_handler.py` | 815-820 | Grid Search validation hook |
| `config_handler.py` | 1072-1077 | Ax validation hook |
| `model_runner.py` | 422-430 | Uses centralized conversion |
| `config-maker.py` | 2951-2954 | Creates lists (not strings) |

---

## 💡 **Best Practices**

### **For Future Model Parameters**:

If another model has similar serialization issues:

1. **Create a static conversion method** in `config_handler.py`:
   ```python
   @staticmethod
   def convert_X_for_sklearn(param: Any) -> CorrectType:
       """Convert parameter X to sklearn format."""
       # Centralized conversion logic
       pass
   ```

2. **Use in model_runner.py**:
   ```python
   if model_name == 'ModelX' and 'param_name' in hyperparams:
       hyperparams['param_name'] = \
           UnifiedConfigHandler.convert_X_for_sklearn(hyperparams['param_name'])
   ```

3. **Validate in config_handler.py**:
   ```python
   if model_name == "ModelX" and "param_name" in hyperparams:
       hyperparams["param_name"] = self._normalize_X(hyperparams["param_name"])
   ```

### **Pattern**:
1. **Store** in YAML-friendly format (lists, dicts)
2. **Validate** during config loading
3. **Convert** using static method before model instantiation
4. **Centralize** all conversion logic in `config_handler.py`

---

## 📝 **Summary**

The MLP layer conversion is now:
- ✅ **Centralized** in `config_handler.py`
- ✅ **Reusable** via static method
- ✅ **Maintainable** with single source of truth
- ✅ **Robust** handling all input formats
- ✅ **Documented** with examples and docstrings
- ✅ **Testable** isolated static method

**Key Method**: `UnifiedConfigHandler.convert_mlp_layers_for_sklearn()`

---

*Centralized architecture ensures consistency and maintainability across the codebase.*

