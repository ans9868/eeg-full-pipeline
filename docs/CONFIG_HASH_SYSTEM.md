# Config Hash System

The config hash system ensures reproducibility and intelligent reuse of pipeline outputs by tracking configuration changes.

## 🔍 Overview

The system uses SHA256 hashes of relevant configuration subsets to detect when pipeline parameters have changed, preventing inappropriate reuse of outdated outputs.

## 📁 Location

The hashing functions are located in `eeg_spark_etl/core/data_io.py`:

- `hash_stage_config()` - Creates consistent hashes of config subsets
- `config_matches()` - Compares current and saved hashes
- `save_stage_hash()` - Saves hashes to stage directories
- `check_stage_reuse()` - Main reuse logic with config validation

## 🎯 How It Works

### 1. **Stage-Specific Config Keys**
Each processing stage tracks only the configuration keys that affect its output:

```python
# Raw stage - tracks preprocessing parameters
raw_keys = ["preprocessing", "data_input"]

# Processed features stage - tracks feature extraction parameters  
processed_keys = ["feature_extraction", "preprocessing"]

# Transformed stage - tracks transformation parameters
transformed_keys = ["transformation", "feature_extraction"]
```

### 2. **Hash Generation**
```python
def hash_stage_config(config: Dict[str, Any], keys: List[str]) -> str:
    relevant = {key: config.get(key) for key in keys}
    serialized = json.dumps(relevant, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()
```

### 3. **Reuse Logic**
```python
def check_stage_reuse(output_dir: Path, stage: str, config: Dict[str, Any], keys: List[str], reuse_flag: str) -> bool:
    if reuse_flag != "Yes":
        return False
    
    if not config_matches(output_dir, stage, config, keys):
        print(f"⚠️  Config mismatch detected in {stage}. Re-generating...")
        return False
    
    print(f"✅ Config matches for {stage}, reusing existing output")
    return True
```

## 📊 Stage Configuration

| Stage | Reuse Flag | Save Flag | Config Keys | Hash File Location |
|-------|------------|-----------|-------------|-------------------|
| `processed_subjects` | `reuse_processed_subjects` | `save_processed_subjects` | `["feature_extraction", "preprocessing"]` | `{output_dir}/processed_subjects/.config_hash.txt` |
| `transformed` | `reuse_transformed` | `save_transformed` | `["transformation", "feature_extraction"]` | `{output_dir}/transformed/.config_hash.txt` |

## 🔄 Usage Flow

1. **Before Processing**: Check if reuse is enabled and config matches
2. **During Processing**: Generate stage outputs
3. **After Processing**: Save config hash if save flag is enabled

## 🎯 Benefits

- **Reproducibility**: Ensures consistent outputs for identical configurations
- **Performance**: Avoids unnecessary recomputation when configs haven't changed
- **Safety**: Prevents silent reuse of outdated outputs
- **Transparency**: Clear logging of reuse decisions and config mismatches

## 🔧 Integration

The hashing system is integrated into the main pipeline flow with hierarchical checking:

- **`main.py`**: Checks `transformed` stage hash and returns early if matches
- **`process_subjects()`**: Checks `processed_subjects` stage hash before processing subjects using DataFrames
- **`process_subject()`**: Processes individual subjects with feature extraction
- **Configuration system**: YAML config loading and validation

### Example: Hierarchical Hash Checking with DataFrames

```python
# main.py - checks transformed stage
def main():
    if check_stage_reuse(output_dir, "transformed", config, transformed_keys, reuse_transformed):
        print("✅ Pipeline completed - using existing transformed data")
        return  # Early exit
    
    # Continue with processing if no transformed data exists
    result = process_subjects(spark, config)

# process_subjects.py - checks processed_subjects stage using DataFrames
def process_subjects(spark: SparkSession, config: Dict[str, Any]) -> Dict[str, str]:
    if check_stage_reuse(output_dir, "processed_subjects", config, processed_keys, reuse_processed_subjects):
        return {"status": "completed", "message": "reused existing processed_subjects data"}
    
    # Process subjects using DataFrames
    subjects_df = spark.createDataFrame(subjects, "subject string")
    feature_dfs = []
    for subject_row in subjects_df.collect():
        subject_features_df = process_subject(subject_id, spark)
        feature_dfs.append(subject_features_df)
    
    # Union all subject DataFrames
    combined_df = feature_dfs[0].union(feature_dfs[1:])
    return {"status": "completed", "message": "processed and saved new processed_subjects data"}

# process_subject.py - processes individual subjects
def process_subject(subject_id: str, spark: SparkSession) -> DataFrame:
    # Process individual subject with feature extraction
    # - Load EEG data from file paths
    # - Apply preprocessing and feature extraction
    # - Return feature DataFrame for this subject
    
    # Process epochs and return DataFrame
    all_features = []
    for epoch_id in range(1, num_epochs + 1):
        epoch_features = process_epoch(epoch_id, subject_id)
        all_features.extend(epoch_features)
    
    return spark.createDataFrame(all_features)
```

For detailed implementation examples, see `HASHING_DETAILED.md`. 