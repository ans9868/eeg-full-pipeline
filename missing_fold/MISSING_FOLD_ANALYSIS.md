# Missing Fold Analysis Summary

## Problem
- **Size 2 (LPSO=2)**: 588 tasks instead of expected 600 tasks (12 models × 50 folds)
- **Size 6 (LPSO=6)**: 600 tasks (12 models × 50 folds) ✅

**Missing**: 12 tasks (exactly 1 fold worth of tasks)

## Root Cause
**Fold ID 49 is missing from size_2 task table!**

### Details:
- **YAML file**: Contains **50 LPSO folds** ✅ (correct)
- **Size 2 task table**: Contains **49 folds** (fold IDs 0-48) ❌
- **Size 6 task table**: Contains **50 folds** (fold IDs 0-49) ✅

### Missing Fold Details:
- **Fold ID**: 49
- **Missing Fold Subjects (for size_2/LPSO=2)**: `sub-003`, `sub-062`
- **Missing Tasks**: 12 tasks (all 12 models for fold 49)
- **Expected Directory**: `sub-3_sub-62` (for LPSO=2, normalized from sub-003/sub-062)

### Calculation:
- **Size 2**: 49 folds × 12 models = 588 tasks ✅
- **Size 6**: 50 folds × 12 models = 600 tasks ✅
- **Missing**: 1 fold × 12 models = 12 tasks

## Why This Happened
The YAML configuration has all 50 folds correctly defined, but fold 49 was never processed/created in the size_2 task table. This could be due to:
1. An error during fold generation that stopped at fold 48
2. Fold 49 being skipped during task table creation
3. An off-by-one error in the fold processing loop

## Resolution
To fix this, you need to:
1. Check why fold 49 was skipped during task table creation
2. Regenerate fold 49 tasks manually, OR
3. Re-run the task table generation to include all 50 folds

## Verification Commands

```bash
# Count folds in YAML
grep "^  - -" data_transform_strategy.yaml | wc -l
# Expected: 50

# Count folds in task tables
python3 -c "
import csv
with open('task_table-size_2.csv') as f:
    fold_ids = set(int(row['fold_id']) for row in csv.DictReader(f))
    print(f'Size 2: {len(fold_ids)} folds, range {min(fold_ids)}-{max(fold_ids)}')
    
with open('task_table-size_6.csv') as f:
    fold_ids = set(int(row['fold_id']) for row in csv.DictReader(f))
    print(f'Size 6: {len(fold_ids)} folds, range {min(fold_ids)}-{max(fold_ids)}')
"
```

## Files Analyzed
- `data_transform_strategy.yaml`: Contains 50 LPSO folds
- `task_table-size_2.csv`: Contains 588 tasks (49 folds)
- `task_table-size_6.csv`: Contains 600 tasks (50 folds)
- `task_progress-size_2.json`: Shows 588 completed tasks
- `task_progress-size_6.json`: Shows 600 completed tasks

