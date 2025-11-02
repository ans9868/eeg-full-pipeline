# Discrepancy Analysis: Missing Tasks in L_2 Config

## Summary

**Issue**: L_2 config (2-person folds) has 588 tasks instead of expected 600 tasks
- **Expected**: 4 models × 3 hyperparams × 50 folds = 600 tasks
- **Actual L_6**: 600 tasks ✅
- **Actual L_2**: 588 tasks ❌ (missing 12 tasks)

## Root Cause

**The last fold (fold 49) was not processed during task generation for the L_2 config.**

### Evidence:

1. **Config Files are Correct** ✅ **VERIFIED**:
   - `config_20251101_213555.yaml` (L_2): **50/50 folds** (size 2) ✅
   - `config_20251101_213406.yaml` (L_6): **50/50 folds** (size 6) ✅
   - Both have `total_folds: 50` in metadata
   - Both have 50 entries in `lpso_folds` list
   - **All current production configs also verified to have 50 folds each** ✅

2. **Task Table Discrepancy**:
   - `task_table-9.csv` (L_6): 600 tasks, folds 0-49 ✅
   - `task_table-10.csv` (L_2): 588 tasks, folds 0-48 ❌
   - **Missing**: All 12 tasks for fold 49 in L_2 config

3. **Last Fold Content (Fold 49)**:
   - L_2 config: `sub-003` + `sub-062` (looks normal)
   - L_6 config: 6 subjects (looks normal)
   - No obvious issues with the fold definition itself

## Conclusion

This is **NOT a config generation issue** - the configs are correct.

This is a **Ray task generation bug** in the eeg-ray-tuner code:
- The task generation logic failed to create tasks for fold 49 in the L_2 config
- Possible causes:
  1. Off-by-one error in fold iteration
  2. Range/loop termination issue (e.g., `range(len(folds)-1)` instead of `range(len(folds))`)
  3. Silent failure during task creation for the last fold
  4. Index boundary issue specific to certain fold counts

## Recommended Action

1. **Immediate**: Re-run the L_2 experiment to see if the issue reproduces
2. **Investigation**: Check Ray task generation code for off-by-one errors
3. **Code Review**: Look for fold iteration logic that might skip the last fold
4. **Testing**: Add validation to ensure `len(tasks) == expected_tasks` before starting execution

## Task Generation Formula

```
Expected tasks = num_models × num_hyperparams_per_model × num_folds
              = 4 × 3 × 50
              = 600
```

For L_2 config:
- **Expected**: 12 tasks/fold × 50 folds = 600 tasks
- **Actual**: 12 tasks/fold × 49 folds = 588 tasks
- **Missing**: 12 tasks (entire fold 49)

