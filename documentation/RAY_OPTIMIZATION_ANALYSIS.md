# Ray Tuner Optimization Analysis

## Problem Statement
Heavy thread thrashing in HPC environments causing performance degradation. Need to optimize:
1. Thread control for ML libraries (numpy, scikit-learn, etc.)
2. CPU resource allocation per ML task
3. Multiple 80/20 partition support (reduce from 9 configs to 1)

## ✅ IMPLEMENTED FIXES (2025-01-11)

### 1. TaskWorker Resource Allocation
**File:** `eeg_ray_tuner/tuning/base_search_strategy.py`
```python
@ray.remote(
    num_cpus=1,          # Reserve exactly 1 CPU per actor
    max_restarts=3,      # Allow up to 3 restarts on failure
    max_task_retries=1,  # Retry failed tasks once before giving up
)
class TaskWorker:
```
Note: `max_calls` is for stateless functions, not actors. Actors use `max_restarts` and `max_task_retries`.

### 2. Ray Runtime Environment Thread Limits
**File:** `eeg_ray_tuner/core/session_builder.py`
```python
'runtime_env': {
    'env_vars': {
        'OMP_NUM_THREADS': '1',
        'MKL_NUM_THREADS': '1',
        'OPENBLAS_NUM_THREADS': '1',
        'NUMEXPR_NUM_THREADS': '1',
        'VECLIB_MAXIMUM_THREADS': '1',
        'BLIS_NUM_THREADS': '1',
    },
    ...
}
```

### 3. n_jobs=1 for Supported Models
**File:** `eeg_ray_tuner/models/model_runner.py`
```python
MODELS_WITH_N_JOBS = {
    'Random Forest',       # RandomForestClassifier.n_jobs
    'KNN',                 # KNeighborsClassifier.n_jobs
    'Logistic Regression', # LogisticRegression.n_jobs
    'XGBoost',             # XGBClassifier.n_jobs
}
if model_name in MODELS_WITH_N_JOBS:
    hyperparams['n_jobs'] = 1
```

---

## Previous State Analysis (Before Fix)

### 1. Thread Management Issues

**Previous State:**
- ❌ No explicit thread control for numpy/scikit-learn
- ❌ No `n_jobs` parameter set for sklearn models
- ❌ No environment variables set (OMP_NUM_THREADS, MKL_NUM_THREADS, etc.)
- ❌ Ray workers can spawn unlimited threads per task

**Current State (FIXED):**
- ✅ Thread limits set via Ray runtime_env
- ✅ n_jobs=1 for supported sklearn models
- ✅ BLAS/OpenMP limited to 1 thread per worker

---

### 2. CPU Resource Allocation

**Previous State:**
- ❌ `TaskWorker` has no `@ray.remote(num_cpus=1)` decorator
- ❌ `execute_task.remote()` has no resource requirements
- ❌ Ray scheduler doesn't know each task needs 1 CPU

**Current State (FIXED):**
- ✅ `@ray.remote(num_cpus=1)` guarantees 1 CPU per worker
- ✅ `max_restarts=3` handles worker failures gracefully
- ✅ `max_task_retries=1` retries failed tasks once

---

### 3. Multiple 80/20 Partitions

**Current State:**
- ❌ Only supports single train/test split per config
- ❌ Need 9 separate config files for 9 different 80/20 splits
- ❌ No support for multiple partitions in same experiment

**Location:**
- `eeg_ray_tuner/tuning/base_search_strategy.py` - Data discovery
- `eeg-pyspark-pipeline/eeg_spark_etl/core/data_io.py` - Data splitting

**Impact:** 🟡 **MEDIUM** - Workflow inefficiency (future work)

---

## Optimization Opportunities

### Priority 1: Thread Thrashing Fixes

#### 1.1 Force Libraries to Use 1 Thread
**Location:** `eeg_ray_tuner/tuning/base_search_strategy.py:116` (TaskWorker.__init__)

**Changes Needed:**
```python
def __init__(self, config_handler_dict: Dict[str, Any]):
    # Set environment variables BEFORE importing numpy/sklearn
    import os
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'
    os.environ['VECLIB_MAXIMUM_THREADS'] = '1'
    
    # Now import libraries (they will respect env vars)
    import numpy as np
    import sklearn
    # ... rest of initialization
```

**Impact:** 🟢 **HIGH** - Eliminates thread contention at library level

---

#### 1.2 Force sklearn Models to Use n_jobs=1
**Location:** `eeg_ray_tuner/models/model_runner.py:432` (train_and_evaluate_model)

**Changes Needed:**
```python
# Add n_jobs=1 to all sklearn models that support it
if model_name in ['Random Forest', 'SVM', 'KNN', 'Decision Tree']:
    hyperparams['n_jobs'] = 1  # Force single-threaded
```

**Impact:** 🟢 **HIGH** - Prevents sklearn from spawning threads

---

#### 1.3 Set Thread Limits in Ray Worker Environment
**Location:** `eeg_ray_tuner/core/session_builder.py` (Ray initialization)

**Changes Needed:**
```python
# Set thread limits in Ray runtime environment
ray_params['runtime_env'] = {
    'env_vars': {
        'OMP_NUM_THREADS': '1',
        'MKL_NUM_THREADS': '1',
        'OPENBLAS_NUM_THREADS': '1',
        'NUMEXPR_NUM_THREADS': '1',
        'VECLIB_MAXIMUM_THREADS': '1',
    },
    'worker_process_setup_hook': 'eeg_ray_tuner.core.ray_logging.setup_logging'
}
```

**Impact:** 🟢 **HIGH** - Ensures all Ray workers have thread limits

---

### Priority 2: CPU Resource Allocation

#### 2.1 Add num_cpus=1 to TaskWorker
**Location:** `eeg_ray_tuner/tuning/base_search_strategy.py:116`

**Changes Needed:**
```python
@ray.remote(num_cpus=1)  # Force 1 CPU per worker
class TaskWorker:
    # ... existing code
```

**Impact:** 🟢 **HIGH** - Guarantees 1 CPU per worker instance

---

#### 2.2 Add num_cpus=1 to execute_task calls
**Location:** `eeg_ray_tuner/tuning/base_search_strategy.py:2248`

**Changes Needed:**
```python
# When calling execute_task, specify resources
future = worker.execute_task.options(num_cpus=1).remote(task.to_dict())
```

**Impact:** 🟡 **MEDIUM** - Redundant if TaskWorker already has num_cpus=1, but provides extra safety

---

#### 2.3 Ensure Tasks Run Until Completion
**Current State:** ✅ Already handled - Ray waits for futures

**Impact:** 🟢 **NONE** - Already working correctly

---

### Priority 3: Multiple 80/20 Partitions

#### 3.1 Add Partition Support to Config
**Location:** `config_handler.py` - Add new config section

**Changes Needed:**
```yaml
data_transformation_strategy:
  intra_test_train_split:
    enabled: true
    num_partitions: 9  # Support multiple 80/20 splits
    test_size: 0.2
    random_seed: 42
```

**Impact:** 🟡 **MEDIUM** - Reduces config file management overhead

---

#### 3.2 Discover Multiple Partitions in Data Discovery
**Location:** `eeg_ray_tuner/tuning/base_search_strategy.py:_discover_all_data_together_folds`

**Changes Needed:**
```python
def _discover_all_data_together_folds(self, data_path: str, config_handler):
    # Check for multiple partition directories
    # transformed/all_data_together/partition_0/, partition_1/, etc.
    partitions = []
    base_dir = os.path.join(data_path, "transformed", "all_data_together")
    
    for i in range(num_partitions):
        partition_dir = os.path.join(base_dir, f"partition_{i}")
        if os.path.exists(partition_dir):
            partitions.append({
                'fold_id': i,
                'fold_name': f'partition_{i}',
                'train_data_paths': [...],
                'test_data_paths': [...]
            })
    return partitions
```

**Impact:** 🟡 **MEDIUM** - Enables single config for multiple partitions

---

#### 3.3 Update PySpark Pipeline to Generate Multiple Partitions
**Location:** `eeg-pyspark-pipeline/eeg_spark_etl/core/data_io.py`

**Changes Needed:**
- Generate multiple 80/20 splits with different random seeds
- Save each to `partition_0/`, `partition_1/`, etc.

**Impact:** 🟡 **MEDIUM** - Requires PySpark pipeline changes

---

## Impact Summary

| Optimization | Impact Level | Effort | Priority |
|-------------|-------------|--------|----------|
| 1.1 Force Libraries 1 Thread | 🔴 CRITICAL | Low | P0 |
| 1.2 sklearn n_jobs=1 | 🔴 CRITICAL | Low | P0 |
| 1.3 Ray Runtime Env Threads | 🔴 CRITICAL | Low | P0 |
| 2.1 TaskWorker num_cpus=1 | 🔴 CRITICAL | Low | P0 |
| 2.2 execute_task num_cpus | 🟡 MEDIUM | Low | P1 |
| 3.1 Multiple Partitions Config | 🟡 MEDIUM | Medium | P2 |
| 3.2 Discover Multiple Partitions | 🟡 MEDIUM | Medium | P2 |
| 3.3 PySpark Multiple Partitions | 🟡 MEDIUM | High | P2 |

---

## Implementation Order

### Phase 1: Thread Thrashing Fixes (P0)
1. Add environment variables to TaskWorker.__init__
2. Add n_jobs=1 to sklearn models
3. Add thread limits to Ray runtime_env
4. Add num_cpus=1 to TaskWorker decorator

**Expected Impact:** 
- Eliminate thread contention
- Predictable CPU usage
- 20-50% performance improvement in HPC environments

### Phase 2: Multiple Partitions (P2)
1. Add config support for num_partitions
2. Update data discovery to find multiple partitions
3. Update PySpark pipeline to generate partitions

**Expected Impact:**
- Reduce config file management
- Single experiment for multiple splits
- Easier comparison across partitions

---

## Testing Strategy

1. **Thread Control Test:**
   - Monitor thread count during task execution
   - Verify OMP_NUM_THREADS is respected
   - Check CPU utilization per task

2. **Resource Allocation Test:**
   - Verify only 1 task per CPU core
   - Check Ray dashboard for resource usage
   - Monitor task completion times

3. **Multiple Partitions Test:**
   - Generate 9 partitions in PySpark
   - Verify all discovered in Ray Tuner
   - Check results saved correctly

---

## Notes

- Thread control must be set BEFORE importing numpy/sklearn
- Environment variables in Ray runtime_env apply to all workers
- num_cpus=1 on TaskWorker ensures exclusive CPU access
- Multiple partitions require coordination between PySpark and Ray Tuner

