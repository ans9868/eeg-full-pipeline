# PySpark Pipeline Investigation: Missing Fold 49 in L_2 Config

## Investigation Summary

**Problem**: L_2 config (2-person folds) creates only 49 directories instead of 50 during PySpark transformation.

## Code Investigation

### Key Findings:

1. **Config Loading is Correct** ✅
   - **Location**: `process_subjects.py` line 362
   - `lpso_folds: List[List[str]] = config_handler.lpso_folds or []`
   - ConfigHandler correctly loads all 50 folds from both L_2 and L_6 configs
   - Verified: Both raw YAML and ConfigHandler show 50 folds

2. **Fold Iteration Logic is Correct** ✅
   - **Location**: `process_subjects.py` line 394
   - `for fold_idx, test_subject_paths in enumerate(lpso_folds):`
   - Uses standard Python `enumerate()` which should iterate over ALL items
   - No filtering, slicing, or conditional logic that would skip folds
   - No code that checks fold size (2 vs 6) before processing

3. **No Fold Size Filtering** ✅
   - Checked entire `process_subjects.py` file
   - No `if len(fold) == 2:` or similar conditions
   - No filtering based on number of subjects per fold
   - Loop processes all folds regardless of size

4. **Error Handling**
   - **Location**: `process_subjects.py` line 470-472
   - `except Exception as e:` followed by `raise`
   - Errors should propagate, not be silently caught
   - However, if an error occurs for fold 49, it would stop the entire pipeline

## Potential Root Causes

Since the code logic appears correct, the issue might be:

### 1. **Runtime Exception for Fold 49 (L_2 only)**
   - Something specific about fold 49's subjects (sub-003, sub-062) causes an error
   - Error might be caught somewhere upstream or cause silent failure
   - **To check**: Look at PySpark logs for fold 49 errors

### 2. **Memory/Resource Issue**
   - Last fold might hit memory limits or timeouts
   - Could be specific to 2-person folds vs 6-person folds
   - **To check**: Check if fold 49 processing starts but doesn't complete

### 3. **File System / Directory Creation Issue**
   - `save_transformed_data()` creates directory: `sub-003_sub-062`
   - Maybe there's a conflict or permission issue with this specific directory name?
   - **To check**: Check if directory creation fails silently

### 4. **YAML Parsing Edge Case (unlikely)**
   - Config loads correctly via ConfigHandler, so this is unlikely
   - But maybe PySpark reads config differently than our test?
   - **To check**: Verify how PySpark actually loads the config in Docker

### 5. **Config Copy Issue**
   - Line 406-407: `fold_config = config.copy()` (shallow copy)
   - Then creates temp file, loads via ConfigHandler
   - Maybe the temp file creation or deletion has an issue for fold 49?
   - **To check**: Check if temp file handling has edge cases

## Where to Look Next

1. **Check PySpark Execution Logs**:
   - Look for any error messages related to fold 49
   - Check if fold 49 processing starts but fails
   - Look for memory/timeout errors

2. **Check Directory Creation**:
   - Verify if directory `sub-003_sub-062` is attempted to be created
   - Check for permission or file system errors
   - Check if there's a naming conflict

3. **Check Transform Features**:
   - `transform_features()` is called for each fold
   - Maybe there's an issue specific to fold 49 in that function?
   - Check if it handles 2-subject folds differently than 6-subject folds

4. **Check Pipeline Transformer**:
   - `pipeline.update_lpso_fold(fold_idx, lpso_folds)` might have an off-by-one bug
   - Could be in `FeaturePipeline` class in `pipeline_transformer.py`

## Code Locations to Review

1. **Main Loop**: `eeg_spark_etl/processing/process_subjects.py` lines 394-472
2. **Transform Function**: `eeg_spark_etl/features/feature_transformations.py` line 17
3. **Pipeline Update**: `eeg_spark_etl/features/transformers/pipeline_transformer.py` (check `update_lpso_fold`)
4. **Save Function**: `eeg_spark_etl/core/data_io.py` lines 848-1040

## Conclusion

The code structure appears correct - there's no obvious filtering or off-by-one error in the loop. The issue is likely:
- A runtime error for fold 49 that's not being properly logged
- A resource/memory issue that silently fails
- An edge case in directory creation or file handling

**Recommendation**: Check actual PySpark execution logs to see what happens when processing fold 49 for the L_2 config.


