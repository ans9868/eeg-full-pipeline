# Resume From CSV Implementation Plan

## Assumption
We have `config_handler.resume_from_csv(csv_path: str)` that returns a dictionary with:
- `tasks: List[Dict[str, Any]]` - List of task dictionaries from CSV
- `csv_path: Path` - Path to the CSV file
- `results_path: Path` - Results directory path
- `incomplete_tasks: List[Dict[str, Any]]` - Tasks with status != 'completed'

## Code Changes Required

### 1. Modify `BaseSearchStrategy.__init__()` 
**File:** `eeg-ray-tuner/eeg_ray_tuner/tuning/base_search_strategy.py`

**Location:** After line 350 (after `self._initialize_workers()`)

**Add:**
```python
# Check for resume mode from config_handler
self.resume_mode = False
self.resume_csv_path = None
self.resume_data = None

if hasattr(config_handler, 'resume_from_csv') and config_handler.resume_from_csv:
    self.resume_mode = True
    # Resume data will be loaded in _run_static_optimization()
    # Store CSV path if provided by config_handler
    if hasattr(config_handler, 'resume_csv_path'):
        self.resume_csv_path = config_handler.resume_csv_path
```

### 2. Add `_load_tasks_from_csv()` method
**File:** `eeg-ray-tuner/eeg_ray_tuner/tuning/base_search_strategy.py`

**Location:** After `_save_tasks_csv()` method (around line 1982)

**Add:**
```python
def _load_tasks_from_csv(self, csv_path: str) -> List[MLTask]:
    """
    Load tasks from existing CSV file.
    
    This method reads a task_table.csv and reconstructs MLTask objects
    from the CSV data. It handles parsing hyperparams JSON and filtering
    incomplete tasks.
    
    Parameters
    ----------
    csv_path : str
        Path to the task_table.csv file
        
    Returns
    -------
    List[MLTask]
        List of MLTask objects loaded from CSV
    """
    import json
    
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"Resume CSV file not found: {csv_path}")
    
    print(f"📂 Loading tasks from: {csv_path}")
    logger.info(f"📂 Loading tasks from: {csv_path}")
    
    # Load CSV
    df = pd.read_csv(csv_file)
    
    if df.empty:
        raise ValueError(f"Resume CSV is empty: {csv_path}")
    
    print(f"📊 Found {len(df)} total tasks in CSV")
    
    # Convert CSV rows to MLTask objects
    tasks = []
    for _, row in df.iterrows():
        try:
            # Parse hyperparams JSON string back to dict
            hyperparams_str = row.get('hyperparams', '{}')
            if isinstance(hyperparams_str, str):
                hyperparams = json.loads(hyperparams_str)
            else:
                hyperparams = hyperparams_str
            
            # Create MLTask from row data
            task_dict = {
                'task_id': row['task_id'],
                'model_name': row['model_name'],
                'label_type': row['label_type'],
                'label_value': row['label_value'],
                'hyperparams': hyperparams,
                'train_data_path': row['train_data_path'],
                'test_data_path': row['test_data_path'],
                'results_path': row['results_path'],
                'fold_id': str(row['fold_id']),
                'status': row.get('status', 'pending'),
                'priority': int(row.get('priority', 0)),
                'created_at': row.get('created_at'),
                'started_at': row.get('started_at'),
                'completed_at': row.get('completed_at'),
                'error_message': row.get('error_message'),
                'worker_id': row.get('worker_id')
            }
            
            task = MLTask.from_dict(task_dict)
            tasks.append(task)
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to load task {row.get('task_id', 'unknown')}: {e}")
            continue
    
    print(f"✅ Loaded {len(tasks)} tasks from CSV")
    logger.info(f"✅ Loaded {len(tasks)} tasks from CSV")
    
    return tasks

def _filter_incomplete_tasks(self, tasks: List[MLTask]) -> List[MLTask]:
    """
    Filter tasks to only include incomplete ones (pending, running, failed).
    
    Parameters
    ----------
    tasks : List[MLTask]
        List of all tasks
        
    Returns
    -------
    List[MLTask]
        List of incomplete tasks only
    """
    incomplete = [t for t in tasks if t.status != 'completed']
    
    # Reset 'running' tasks to 'pending' (may have been interrupted)
    for task in incomplete:
        if task.status == 'running':
            task.status = 'pending'
            task.started_at = None
            task.worker_id = None
            logger.info(f"🔄 Resetting 'running' task {task.task_id} to 'pending'")
    
    print(f"📊 Incomplete tasks: {len(incomplete)} (pending: {sum(1 for t in incomplete if t.status == 'pending')}, "
          f"failed: {sum(1 for t in incomplete if t.status == 'failed')})")
    logger.info(f"📊 Found {len(incomplete)} incomplete tasks")
    
    return incomplete
```

### 3. Modify `_run_static_optimization()` method
**File:** `eeg-ray-tuner/eeg_ray_tuner/tuning/base_search_strategy.py`

**Location:** Replace the entire `_run_static_optimization()` method (starting at line 718)

**Change:**
```python
def _run_static_optimization(self) -> None:
    """
    Run static optimization workflow (Grid Search).
    
    This workflow pre-computes ALL tasks before execution, OR loads
    existing tasks from CSV if resuming.
    
    Phase 1: Discover data folds (skip if resuming)
    Phase 2: Generate all tasks OR load from CSV (skip if resuming)
    Phase 3: Optimize task ordering (skip if resuming)
    Phase 4: Save task table to CSV (skip if resuming)
    Phase 5: Execute all tasks in parallel
    Phase 6: Process and save results
    """
    # Check for resume mode
    resume_mode = False
    resume_csv_path = None
    
    # Check if config_handler has resume_from_csv attribute
    if hasattr(self.config_handler, 'resume_from_csv') and self.config_handler.resume_from_csv:
        resume_mode = True
        # Get CSV path from config_handler or use default location
        if hasattr(self.config_handler, 'resume_csv_path') and self.config_handler.resume_csv_path:
            resume_csv_path = self.config_handler.resume_csv_path
        else:
            # Default: look for task_table.csv in results directory
            default_csv = self.results_path / 'task_table.csv'
            if default_csv.exists():
                resume_csv_path = str(default_csv)
            else:
                print(f"⚠️ Resume mode enabled but no CSV found at {default_csv}")
                print(f"   Continuing with normal task generation...")
                resume_mode = False
    
    if resume_mode and resume_csv_path:
        # RESUME MODE: Load existing tasks from CSV
        print(f"\n🔄 RESUME MODE: Loading tasks from CSV")
        print("=" * 70)
        print(f"📂 CSV path: {resume_csv_path}")
        
        # Load all tasks from CSV
        all_tasks = self._load_tasks_from_csv(resume_csv_path)
        
        # Filter to incomplete tasks only
        incomplete_tasks = self._filter_incomplete_tasks(all_tasks)
        
        if not incomplete_tasks:
            print("✅ All tasks already completed! Nothing to resume.")
            print("   If you want to regenerate results, please delete the CSV or disable resume mode.")
            return
        
        # Set tasks to incomplete ones only
        self.tasks = incomplete_tasks
        
        print(f"✅ Loaded {len(incomplete_tasks)} incomplete tasks to resume")
        print(f"📊 Skipping {len(all_tasks) - len(incomplete_tasks)} completed tasks")
        logger.info(f"🔄 Resume mode: {len(incomplete_tasks)} tasks to execute")
        
        # Print task summary
        self._print_task_summary()
        
        # Skip phases 1-4, go directly to execution
        # Phase 5: Execute all tasks
        print(f"\n📋 PHASE 5: Executing Remaining Tasks")
        print("=" * 70)
        self._execute_all_tasks()
        
        # Phase 6: Process results
        print(f"\n📋 PHASE 6: Processing Results")
        print("=" * 70)
        self._process_results()
        
    else:
        # NORMAL MODE: Generate tasks from scratch
        # Phase 1: Discover data folds
        print(f"\n📋 PHASE 1: Discovering Data Folds")
        print("=" * 70)
        
        fold_configs = self._discover_data_folds()
        if not fold_configs:
            print("❌ No data folds found. Please run the PySpark pipeline first.")
            logger.error("❌ No data folds found")
            return
        
        self._print_fold_summary(fold_configs)
        logger.info(f"✅ Discovered {len(fold_configs)} data folds")
        
        # Phase 2: Generate all tasks
        print(f"\n📋 PHASE 2: Generating Tasks")
        print("=" * 70)
        
        self._generate_tasks(fold_configs)
        
        if not self.tasks:
            print("❌ No tasks generated. Check configuration.")
            logger.error("❌ No tasks generated")
            return
        
        print(f"✅ Generated {len(self.tasks)} tasks")
        logger.info(f"✅ Generated {len(self.tasks)} tasks")
        
        # Phase 3: Optimize task ordering
        print(f"\n📋 PHASE 3: Optimizing Task Order")
        print("=" * 70)
        self._optimize_task_ordering()
        
        # Phase 4: Save task table
        print(f"\n📋 PHASE 4: Saving Task Table")
        print("=" * 70)
        self._save_tasks_csv()
        self._print_task_summary()
        
        # Phase 5: Execute all tasks
        print(f"\n📋 PHASE 5: Executing Tasks")
        print("=" * 70)
        self._execute_all_tasks()
        
        # Phase 6: Process results
        print(f"\n📋 PHASE 6: Processing Results")
        print("=" * 70)
        self._process_results()
```

### 4. Optional: Add resume mode to config_handler validation
**File:** `config_handler.py` (if we want to add this feature)

**Location:** In the class that handles resume logic

**Add attributes:**
```python
# Resume configuration
self.resume_from_csv = config.get('resume', {}).get('enabled', False)
self.resume_csv_path = config.get('resume', {}).get('csv_path', None)
```

### 5. Optional: Add resume flag to config YAML structure
**File:** `config-maker.py` or documentation

**Location:** Add resume configuration option

**Add to config structure:**
```yaml
resume:
  enabled: true  # Set to true to enable resume mode
  csv_path: /path/to/task_table.csv  # Optional: specify CSV path, otherwise auto-detect
```

### 6. Validation checks needed

**In `_load_tasks_from_csv()` add validation:**

```python
# Validate CSV schema
required_columns = ['task_id', 'model_name', 'hyperparams', 'train_data_path', 
                    'test_data_path', 'results_path', 'fold_id', 'status']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"CSV missing required columns: {missing_columns}")

# Validate data paths exist (optional, can warn instead of fail)
for task in tasks:
    if not Path(task.train_data_path).exists():
        logger.warning(f"⚠️ Train data path does not exist: {task.train_data_path}")
    if not Path(task.test_data_path).exists():
        logger.warning(f"⚠️ Test data path does not exist: {task.test_data_path}")
```

## Summary

The key changes are:

1. **Add resume mode detection** in `__init__()` to check if `config_handler.resume_from_csv` is enabled
2. **Add `_load_tasks_from_csv()`** method to parse CSV and reconstruct MLTask objects
3. **Add `_filter_incomplete_tasks()`** method to filter out completed tasks and reset 'running' to 'pending'
4. **Modify `_run_static_optimization()`** to check for resume mode and skip phases 1-4 if resuming
5. **Add validation** for CSV schema and data paths

The flow becomes:
- **Normal mode**: Discover folds → Generate tasks → Save CSV → Execute → Process results
- **Resume mode**: Load CSV → Filter incomplete → Execute → Process results

## Testing Checklist

- [ ] Test loading CSV with all task statuses (pending, running, completed, failed)
- [ ] Test filtering incomplete tasks correctly
- [ ] Test resetting 'running' tasks to 'pending'
- [ ] Test validation of CSV schema
- [ ] Test handling missing CSV file
- [ ] Test handling empty CSV
- [ ] Test handling corrupted hyperparams JSON
- [ ] Test normal mode still works when resume is disabled
- [ ] Test resume mode when all tasks are completed
- [ ] Test resume mode with mixed completed/incomplete tasks

