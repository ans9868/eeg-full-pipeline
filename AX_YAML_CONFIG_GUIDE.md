# Ax Search Space Configuration via YAML

## 📝 Overview

You can manually define Ax search spaces for **ANY model** directly in your config YAML file, bypassing the interactive config-maker's defaults.

---

## 🎯 YAML Structure

```yaml
ray:
  ax:
    models:
      - KNN
      - MLP (Neural Network)
      - SVM
      # ... add any models
    
    model_configs:
      # For each model, define search space
      ModelName:
        use_default: false  # IMPORTANT: Set to false to use custom config
        hyperparameters:
          param_name:
            type: uniform|loguniform|quniform|choice
            bounds: [low, high]  # for uniform/loguniform/quniform
            values: [...]        # for choice
            q: step              # for quniform only
        num_samples: 50  # Number of Ax trials for this model
```

---

## 📊 Parameter Types

### 1. **uniform** - Continuous range (linear scale)
```yaml
learning_rate:
  type: uniform
  bounds: [0.01, 0.3]
```
→ Ax will explore values uniformly between 0.01 and 0.3

### 2. **loguniform** - Continuous range (log scale)
```yaml
learning_rate:
  type: loguniform
  bounds: [0.001, 0.3]
```
→ Better for learning rates (more exploration at lower values)

### 3. **quniform** - Discrete steps (converted to randint)
```yaml
n_estimators:
  type: quniform
  bounds: [50, 500]
  q: 50
```
→ Will test 50, 100, 150, ..., 500
(Note: Currently converted to randint(50, 501) for Ax compatibility)

### 4. **choice** - Categorical/discrete values
```yaml
kernel:
  type: choice
  values: ['rbf', 'linear', 'poly', 'sigmoid']
```
→ Ax will intelligently explore these discrete options

---

## 🤖 Model-Specific Examples

### KNN (K-Nearest Neighbors)
```yaml
KNN:
  use_default: false
  hyperparameters:
    n_neighbors:
      type: quniform
      bounds: [1, 15]
      q: 2
    weights:
      type: choice
      values: ['uniform', 'distance']
    metric:
      type: choice
      values: ['euclidean', 'manhattan', 'minkowski']
  num_samples: 30
```

### Random Forest
```yaml
Random Forest:
  use_default: false
  hyperparameters:
    n_estimators:
      type: quniform
      bounds: [50, 500]
      q: 50
    max_depth:
      type: choice
      values: [10, 20, 30, 50, null]  # null = None in Python
    min_samples_split:
      type: quniform
      bounds: [2, 20]
      q: 2
    max_features:
      type: choice
      values: ['sqrt', 'log2']
  num_samples: 50
```

### XGBoost
```yaml
XGBoost:
  use_default: false
  hyperparameters:
    n_estimators:
      type: quniform
      bounds: [50, 500]
      q: 50
    max_depth:
      type: quniform
      bounds: [3, 15]
      q: 3
    learning_rate:
      type: loguniform  # Log scale is better for learning rates
      bounds: [0.001, 0.3]
    subsample:
      type: uniform
      bounds: [0.6, 1.0]
    colsample_bytree:
      type: uniform
      bounds: [0.6, 1.0]
  num_samples: 100
```

### MLP (Neural Network)
```yaml
MLP (Neural Network):
  use_default: false
  hyperparameters:
    hidden_layer_sizes:
      type: choice
      values: ['(50,)', '(100,)', '(50, 25)', '(100, 50)', '(100, 50, 25)']
      # Note: Must be strings representing tuples
    activation:
      type: choice
      values: ['relu', 'tanh', 'logistic']
    alpha:
      type: loguniform
      bounds: [0.0001, 0.1]
    learning_rate_init:
      type: loguniform
      bounds: [0.001, 0.01]
  num_samples: 50
```

### SVM (Support Vector Machine)
```yaml
SVM:
  use_default: false
  hyperparameters:
    C:
      type: loguniform
      bounds: [0.1, 100.0]
    kernel:
      type: choice
      values: ['rbf', 'linear', 'poly']
    gamma:
      type: choice
      values: ['scale', 'auto']  # Keep only strings OR only numbers
      # OR use numeric only:
      # type: loguniform
      # bounds: [0.001, 1.0]
  num_samples: 40
```

### Gradient Boosting
```yaml
Gradient Boosting:
  use_default: false
  hyperparameters:
    n_estimators:
      type: quniform
      bounds: [50, 300]
      q: 50
    max_depth:
      type: quniform
      bounds: [3, 12]
      q: 3
    learning_rate:
      type: loguniform
      bounds: [0.01, 0.3]
    subsample:
      type: uniform
      bounds: [0.6, 1.0]
  num_samples: 50
```

### Decision Tree
```yaml
Decision Tree:
  use_default: false
  hyperparameters:
    max_depth:
      type: choice
      values: [5, 10, 15, 20, 30, null]  # null = unlimited depth
    min_samples_split:
      type: quniform
      bounds: [2, 20]
      q: 2
    max_features:
      type: choice
      values: ['sqrt', 'log2', null]
  num_samples: 30
```

### Logistic Regression
```yaml
Logistic Regression:
  use_default: false
  hyperparameters:
    C:
      type: loguniform
      bounds: [0.1, 100.0]
    solver:
      type: choice
      values: ['lbfgs', 'liblinear', 'saga']
    max_iter:
      type: quniform
      bounds: [100, 1000]
      q: 100
  num_samples: 30
```

### AdaBoost
```yaml
AdaBoost:
  use_default: false
  hyperparameters:
    n_estimators:
      type: quniform
      bounds: [50, 300]
      q: 50
    learning_rate:
      type: loguniform
      bounds: [0.01, 2.0]
    algorithm:
      type: choice
      values: ['SAMME', 'SAMME.R']
  num_samples: 30
```

---

## 📋 Complete Example Config

Here's a full example with multiple models:

```yaml
ray:
  search_strategies:
    - grid_search
    - ax
  
  grid_search:
    models:
      - KNN
      - Random Forest
    model_configs:
      KNN:
        use_default: false
        hyperparameters:
          n_neighbors: [1, 3, 5, 7, 11]
          weights: ['uniform', 'distance']
          metric: ['euclidean']
      Random Forest:
        use_default: false
        hyperparameters:
          n_estimators: [100, 200, 300]
          max_depth: [10, 20, 30]
          min_samples_split: [2, 5, 10]
    max_concurrent: 4
    cv_folds: 5
  
  ax:
    models:
      - KNN
      - Random Forest
      - XGBoost
      - MLP (Neural Network)
    
    model_configs:
      KNN:
        use_default: false
        hyperparameters:
          n_neighbors:
            type: quniform
            bounds: [1, 15]
            q: 2
          weights:
            type: choice
            values: ['uniform', 'distance']
          metric:
            type: choice
            values: ['euclidean', 'manhattan']
        num_samples: 30
      
      Random Forest:
        use_default: false
        hyperparameters:
          n_estimators:
            type: quniform
            bounds: [50, 500]
            q: 50
          max_depth:
            type: choice
            values: [10, 20, 30, null]
          min_samples_split:
            type: quniform
            bounds: [2, 20]
            q: 2
        num_samples: 50
      
      XGBoost:
        use_default: false
        hyperparameters:
          n_estimators:
            type: quniform
            bounds: [50, 300]
            q: 50
          max_depth:
            type: quniform
            bounds: [3, 12]
            q: 3
          learning_rate:
            type: loguniform
            bounds: [0.01, 0.3]
          subsample:
            type: uniform
            bounds: [0.6, 1.0]
        num_samples: 80
      
      MLP (Neural Network):
        use_default: false
        hyperparameters:
          hidden_layer_sizes:
            type: choice
            values: ['(50,)', '(100,)', '(50, 25)', '(100, 50)']
          activation:
            type: choice
            values: ['relu', 'tanh']
          alpha:
            type: loguniform
            bounds: [0.0001, 0.1]
        num_samples: 40
    
    max_concurrent: 4
    cv_folds: 5
  
  metric: accuracy
  mode: max
```

---

## ⚠️ Important Notes

### 1. **Model Name Matching**
- Model names in YAML must **exactly match** the names in the models list
- Case-sensitive: `"MLP (Neural Network)"` not `"mlp"`

### 2. **use_default: false**
- **MUST** set `use_default: false` to use custom config
- If `use_default: true`, all hyperparameters are ignored

### 3. **num_samples per Model**
- Each model can have a different number of trials
- Ax will run this many trials for each model independently

### 4. **None/null Values**
- Use `null` in YAML (converts to Python `None`)
- Example: `max_depth: [10, 20, null]`

### 5. **Tuple Values (MLP)**
- Must be **strings**: `'(50, 25)'` not `(50, 25)`
- Model runner will parse the string to tuple

### 6. **Mixed Type Parameters** ⚠️
- Avoid mixing strings and numbers in same parameter
- **Bad**: `gamma: ['scale', 'auto', 0.001, 0.01]`
- **Good**: `gamma: ['scale', 'auto']` OR `gamma: [0.001, 0.01, 0.1]`

---

## 🔧 How to Use

### Method 1: Edit Existing Config
1. Open your generated config YAML
2. Find the `ray.ax.model_configs` section
3. Change `use_default: true` → `use_default: false`
4. Add hyperparameters following examples above

### Method 2: Create from Template
1. Copy example config above
2. Modify for your models
3. Save as `my_custom_config.yaml`
4. Run pipeline with your config

### Method 3: Hybrid Approach
1. Use config-maker for Grid Search
2. Manually edit YAML to add Ax configurations
3. Run both strategies with full control

---

## ✅ Validation Checklist

Before running, verify:

- [ ] `use_default: false` for custom configs
- [ ] All parameter `type` values are valid: uniform/loguniform/quniform/choice
- [ ] `bounds` has exactly 2 values [low, high]
- [ ] `values` is a list for `choice` type
- [ ] `q` is specified for `quniform`
- [ ] Model names match exactly (including spaces and capitalization)
- [ ] `num_samples` is set for each model
- [ ] No mixed string/numeric values in same parameter

---

## 🚀 Quick Start Example

**Minimal working Ax config for 3 models:**

```yaml
ray:
  ax:
    models:
      - KNN
      - Random Forest
      - XGBoost
    
    model_configs:
      KNN:
        use_default: false
        hyperparameters:
          n_neighbors: {type: quniform, bounds: [1, 15], q: 2}
          weights: {type: choice, values: ['uniform', 'distance']}
        num_samples: 20
      
      Random Forest:
        use_default: false
        hyperparameters:
          n_estimators: {type: quniform, bounds: [50, 300], q: 50}
          max_depth: {type: choice, values: [10, 20, 30]}
        num_samples: 30
      
      XGBoost:
        use_default: false
        hyperparameters:
          learning_rate: {type: loguniform, bounds: [0.01, 0.3]}
          max_depth: {type: quniform, bounds: [3, 12], q: 3}
        num_samples: 40
    
    max_concurrent: 4
    cv_folds: 5
```

---

## 📚 Additional Resources

- See `MODELS_COMPATIBILITY_REPORT.md` for parameter recommendations per model
- Check existing configs in `config/` directory for examples
- Use `config-maker.py` to generate base configs, then customize YAML

---

*Happy Hyperparameter Tuning!* 🎯

