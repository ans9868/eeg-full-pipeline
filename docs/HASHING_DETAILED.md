# Detailed Config Hashing System

This document provides a comprehensive explanation of how the config hashing system works in the EEG Spark ETL pipeline.

## 📍 Location

All hashing functions are located in `eeg_spark_etl/core/data_io.py`:

```python
from eeg_spark_etl.core.data_io import (
    hash_stage_config,
    config_matches, 
    save_stage_hash,
    check_stage_reuse
)
```

## 🔧 Core Functions

### 1. `hash_stage_config(config, keys) -> str`

Creates a SHA256 hash of selected configuration keys.

```python
def hash_stage_config(config: Dict[str, Any], keys: List[str]) -> str:
    """Create a consistent hash of selected config keys."""
    relevant = {key: config.get(key) for key in keys}
    serialized = json.dumps(relevant, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()
```

**Example:**
```python
config = {
    "preprocessing": {"window_size": 2, "sliding_window": 0.5},
    "feature_extraction": {"method": "fft"},
    "project": {"name": "test"}
}

# Hash only preprocessing config
hash_val = hash_stage_config(config, ["preprocessing"])
# Result: "a1b2c3d4..." (consistent for same preprocessing settings)
```

### 2. `config_matches(output_dir, stage, config, keys) -> bool`

Compares current config hash with saved hash for a stage.

```python
def config_matches(output_dir: Path, stage: str, config: Dict[str, Any], keys: List[str]) -> bool:
    """Check if saved hash for a stage matches current config."""
    hash_file = output_dir / stage / ".config_hash.txt"
    if not hash_file.exists():
        return False
    saved_hash = hash_file.read_text().strip()
    current_hash = hash_stage_config(config, keys)
    return saved_hash == current_hash
```

### 3. `save_stage_hash(output_dir, stage, config, keys) -> None`

Saves the current config hash to the stage directory.

```python
def save_stage_hash(output_dir: Path, stage: str, config: Dict[str, Any], keys: List[str]) -> None:
    """Save hash of relevant config keys for a stage."""
    hash_val = hash_stage_config(config, keys)
    stage_dir = output_dir / stage
    stage_dir.mkdir(exist_ok=True)
    (stage_dir / ".config_hash.txt").write_text(hash_val)
    print(f"💾 Saved config hash for {stage}: {hash_val[:8]}...")
```

### 4. `check_stage_reuse(output_dir, stage, config, keys, reuse_flag) -> bool`

Main reuse logic that encapsulates the entire validation process.

```python
def check_stage_reuse(output_dir: Path, stage: str, config: Dict[str, Any], keys: List[str], reuse_flag: str) -> bool:
    """
    Check if we can reuse existing output for a stage.
    Returns True if reuse is safe, False if we need to regenerate.
    """
    if reuse_flag != "Yes":
        return False
    
    if not config_matches(output_dir, stage, config, keys):
        print(f"⚠️  Config mismatch detected in {stage}. Re-generating...")
        print(f"   Relevant keys: {keys}")
        return False
    
    print(f"✅ Config matches for {stage}, reusing existing output")
    return True
```

## 🎯 Stage-Specific Configuration

Each processing stage tracks only the configuration keys that affect its output:

### Raw Stage
- **Keys**: `["preprocessing", "data_input"]`
- **Reuse Flag**: `config["data_input"]["reuse_raw"]`
- **Save Flag**: `config["data_input"]["save_raw"]`
- **Hash File**: `{output_dir}/raw/.config_hash.txt`

### Processed Features Stage  
- **Keys**: `["feature_extraction", "preprocessing"]`
- **Reuse Flag**: `config["data_input"]["reuse_processed_features"]`
- **Save Flag**: `config["data_input"]["save_processed_features"]`
- **Hash File**: `{output_dir}/processed_features/.config_hash.txt`

### Transformed Stage
- **Keys**: `["transformation", "feature_extraction"]`
- **Reuse Flag**: `config["data_input"]["reuse_transformed"]`
- **Save Flag**: `config["data_input"]["save_transformed"]`
- **Hash File**: `{output_dir}/transformed/.config_hash.txt`

## 🔄 Usage Examples

### Example 1: Hierarchical Hash Checking with DataFrames

```python
# main.py - checks transformed stage
def main():
    transformed_reuse = config.get('data_input', {}).get('reuse_transformed', 'No')
    if transformed_reuse == "Yes":
        transformed_keys = ["transformation", "feature_extraction"]
        if check_stage_reuse(output_dir, "transformed", config, transformed_keys, transformed_reuse):
            print("✅ Pipeline completed - using existing transformed data")
            return  # Early exit
    
    # Continue with processing if no transformed data exists
    result = process_subjects(spark, config)

# process_subjects.py - checks processed_features stage using DataFrames
def process_subjects(spark: SparkSession, config: Dict[str, Any]) -> Dict[str, str]:
    reuse_processed_features = config.get('data_input', {}).get('reuse_processed_features', 'No')
    processed_features_keys = ["feature_extraction", "preprocessing"]
    
    if check_stage_reuse(output_dir, "processed_features", config, processed_features_keys, reuse_processed_features):
        return {"status": "completed", "message": "reused existing processed_features data"}
    
    # Process subjects using DataFrames
    subjects_df = spark.createDataFrame(subjects, "subject string")
    feature_dfs = []
    for subject_row in subjects_df.collect():
        subject_features_df = process_subject(subject_id, spark)
        feature_dfs.append(subject_features_df)
    
    # Union all subject DataFrames
    combined_df = feature_dfs[0].union(feature_dfs[1:])
    return {"status": "completed", "message": "processed and saved new processed_features data"}

# process_subject.py - TODO: will check raw stage
def process_subject(subject_id: str, spark: SparkSession) -> DataFrame:
    # TODO: Check for existing raw data with hash validation
    # - Check if reuse_raw flag is enabled
    # - Validate hash for raw stage (preprocessing, data_input keys)
    # - Load existing raw data if hash matches
    # - Process raw data if no reuse possible
    
    # Process epochs and return DataFrame
    all_features = []
    for epoch_id in range(1, num_epochs + 1):
        epoch_features = process_epoch(epoch_id, subject_id)
        all_features.extend(epoch_features)
    
    return spark.createDataFrame(all_features)
```

### Example 2: Schema-Based Feature Processing

```python
from eeg_spark_etl.core.shema_definition import get_feature_schema

# process_epoch.py - generates features matching schema
def process_epoch(epoch_id: int, subject_id: str) -> List[Row]:
    features = []
    electrodes = ["Fp1", "Fp2", "F3", "F4", "C3", "C4"]
    wavebands = ["alpha", "beta", "theta", "delta"]
    feature_names = ["power", "frequency", "amplitude"]
    
    for electrode in electrodes:
        for waveband in wavebands:
            for feature_name in feature_names:
                feature_row = Row(
                    SubjectID=subject_id,
                    EpochID=str(epoch_id),
                    Electrode=electrode,
                    WaveBand=waveband,
                    FeatureName=feature_name,
                    FeatureValue=random.uniform(0.1, 10.0),
                    table_type="epoch"
                )
                features.append(feature_row)
    
    return features
```

### Example 3: Saving Stage Hash
```python
from eeg_spark_etl.core.data_io import save_stage_hash

# After processing processed_features stage
save_stage_hash(
    output_dir=output_dir,
    stage="processed_features", 
    config=config,
    keys=["feature_extraction", "preprocessing"]
)
```

## 🔍 Hash Properties

### Consistency
- Same config → Same hash (deterministic)
- Different config → Different hash
- Order-independent (JSON sorted keys)

### Example Hash Values
```python
# Config 1
config1 = {"preprocessing": {"window_size": 2, "sliding_window": 0.5}}
hash1 = hash_stage_config(config1, ["preprocessing"])
# Result: "a1b2c3d4e5f6..."

# Config 2 (same values, different order)
config2 = {"preprocessing": {"sliding_window": 0.5, "window_size": 2}}
hash2 = hash_stage_config(config2, ["preprocessing"])
# Result: "a1b2c3d4e5f6..." (same hash!)

# Config 3 (different values)
config3 = {"preprocessing": {"window_size": 1, "sliding_window": 0.5}}
hash3 = hash_stage_config(config3, ["preprocessing"])
# Result: "f9e8d7c6b5a4..." (different hash!)
```

## 🐛 Debugging

### Check Hash Files
```bash
# View saved hashes
cat ./data/my_project/raw/.config_hash.txt
cat ./data/my_project/processed_features/.config_hash.txt
cat ./data/my_project/transformed/.config_hash.txt
```

### Manual Hash Generation
```python
from eeg_spark_etl.core.data_io import hash_stage_config

# Generate hash for current config
current_hash = hash_stage_config(config, ["preprocessing", "data_input"])
print(f"Current hash: {current_hash}")

# Compare with saved hash
with open("./data/my_project/raw/.config_hash.txt", "r") as f:
    saved_hash = f.read().strip()
    print(f"Saved hash: {saved_hash}")
    print(f"Match: {current_hash == saved_hash}")
```

### Hash File Structure
```
./data/my_project/
├── raw/
│   └── .config_hash.txt          # Hash of preprocessing + data_input
├── processed_features/
│   └── .config_hash.txt          # Hash of feature_extraction + preprocessing  
└── transformed/
    └── .config_hash.txt          # Hash of transformation + feature_extraction
```

## 🎯 Benefits

1. **Reproducibility**: Identical configs always produce identical outputs
2. **Performance**: Skip recomputation when configs haven't changed
3. **Safety**: Prevent silent reuse of outdated outputs
4. **Transparency**: Clear logging of reuse decisions
5. **Flexibility**: Stage-specific config tracking
6. **Schema Enforcement**: DataFrame approach with proper schema validation
7. **Optimization**: Catalyst optimizer benefits for DataFrame operations

## 🔧 Integration Points

The hashing system integrates with:

- **`main.py`**: Checks `transformed` stage hash and returns early if matches
- **`process_subjects()`**: Checks `processed_features` stage hash before processing subjects using DataFrames
- **`process_subject()`**: TODO - Will check `raw` stage hash (to be implemented)
- **`process_epoch()`**: Generates features matching the defined schema
- **Configuration system**: YAML config loading and validation

This hierarchical DataFrame approach ensures that your EEG processing pipeline is both efficient and reproducible! 🚀 