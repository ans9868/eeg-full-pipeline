# EEG Pipeline Hashing Flow

```mermaid
graph TB
    %% Configuration and Input
    CONFIG[📄 YAML Config<br/>config_testlaptop_03-08-2025_1830.yaml]
    SPARK[⚡ SparkSession]
    
    %% Main Process Flow
    PROCESS_SUBJECTS[🔄 process_subjects.py<br/>Main Processing Function]
    
    %% Configuration Extraction
    PROJECT_CONFIG[📋 Project Config<br/>name, output_dir]
    DATA_INPUT_CONFIG[📋 Data Input Config<br/>groups, reuse flags, save flags]
    
    %% Hashing System Components
    HASH_STAGE_CONFIG[🔐 hash_stage_config<br/>Creates SHA256 hash]
    CONFIG_MATCHES[🔍 config_matches<br/>Compares saved vs current hash]
    SAVE_STAGE_HASH[💾 save_stage_hash<br/>Saves hash to file]
    CHECK_STAGE_REUSE[✅ check_stage_reuse<br/>Main reuse logic]
    
    %% Stage-specific checks
    PROCESSED_SUBJECTS_CHECK[🔍 Check processed_subjects<br/>reuse_processed_subjects]
    
    %% Data Processing Components
    SUBJECTS_DF[📊 Subjects DataFrame<br/>Created from config groups]
    PROCESSED_SUBJECTS_DF[📊 Processed Subjects DataFrame<br/>Union of all subjects]
    TRANSFORMED_DF[📊 Transformed DataFrame<br/>After feature transformations]
    
    %% File System Operations
    OUTPUT_DIR[📁 Output Directory<br/>./data/testLaptop]
    PROCESSED_SUBJECTS_PATH[📁 processed_subjects/<br/>.config_hash.txt + *.parquet]
    
    %% Processing Functions
    PROCESS_SUBJECT[🔄 process_subject<br/>Individual subject processing]
    TRANSFORM_FEATURES[🔄 transform_features<br/>Feature transformations]
    GET_FEATURE_SCHEMA[📋 get_feature_schema<br/>Schema definition]
    
    %% Config Keys for Hashing
    PROCESSED_FEATURES_KEYS[🔑 Keys: feature_extraction, preprocessing]
    PROCESSED_SUBJECTS_KEYS[🔑 Keys: feature_extraction, preprocessing]
    
    %% Flow Connections
    CONFIG --> PROCESS_SUBJECTS
    SPARK --> PROCESS_SUBJECTS
    
    %% Configuration extraction
    PROCESS_SUBJECTS --> PROJECT_CONFIG
    PROCESS_SUBJECTS --> DATA_INPUT_CONFIG
    
    %% Initial processed_subjects check
    PROCESS_SUBJECTS --> PROCESSED_SUBJECTS_CHECK
    PROCESSED_SUBJECTS_CHECK --> CHECK_STAGE_REUSE
    CHECK_STAGE_REUSE --> CONFIG_MATCHES
    CONFIG_MATCHES --> HASH_STAGE_CONFIG
    PROCESSED_SUBJECTS_KEYS --> HASH_STAGE_CONFIG
    PROCESSED_SUBJECTS_PATH --> CONFIG_MATCHES
    
    %% Subject processing flow
    PROCESS_SUBJECTS --> SUBJECTS_DF
    SUBJECTS_DF --> PROCESSED_SUBJECTS_CHECK
    PROCESSED_SUBJECTS_CHECK --> CHECK_STAGE_REUSE
    PROCESSED_SUBJECTS_KEYS --> HASH_STAGE_CONFIG
    PROCESSED_SUBJECTS_PATH --> CONFIG_MATCHES
    
    %% Data processing
    PROCESS_SUBJECTS --> PROCESS_SUBJECT
    PROCESS_SUBJECT --> PROCESSED_SUBJECTS_DF
    GET_FEATURE_SCHEMA --> PROCESSED_SUBJECTS_DF
    
    %% Saving processed subjects
    PROCESSED_SUBJECTS_DF --> SAVE_STAGE_HASH
    SAVE_STAGE_HASH --> PROCESSED_SUBJECTS_PATH
    PROCESSED_SUBJECTS_KEYS --> SAVE_STAGE_HASH
    
    %% Transformation flow
    PROCESSED_SUBJECTS_DF --> TRANSFORM_FEATURES
    TRANSFORM_FEATURES --> TRANSFORMED_DF
    
    %% Saving transformed features
    TRANSFORMED_DF --> SAVE_STAGE_HASH
    SAVE_STAGE_HASH --> PROCESSED_FEATURES_PATH
    PROCESSED_FEATURES_KEYS --> SAVE_STAGE_HASH
    
    %% Output directory structure
    OUTPUT_DIR --> PROCESSED_SUBJECTS_PATH
    OUTPUT_DIR --> PROCESSED_FEATURES_PATH
    
    %% Styling
    classDef configClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef processClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef hashClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef dataClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef fileClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class CONFIG,PROJECT_CONFIG,DATA_INPUT_CONFIG configClass
    class PROCESS_SUBJECTS,PROCESS_SUBJECT,TRANSFORM_FEATURES processClass
    class HASH_STAGE_CONFIG,CONFIG_MATCHES,SAVE_STAGE_HASH,CHECK_STAGE_REUSE hashClass
    class SUBJECTS_DF,PROCESSED_SUBJECTS_DF,TRANSFORMED_DF dataClass
    class OUTPUT_DIR,PROCESSED_SUBJECTS_PATH,PROCESSED_FEATURES_PATH fileClass
```

## 🔄 **Process Flow Explanation**

### **1. Configuration Loading**
- YAML config file contains all settings
- `process_subjects()` extracts project and data input configs
- Config determines reuse/save behavior for each stage

### **2. Hash-Based Reuse System**
- **`check_stage_reuse()`**: Main entry point for reuse logic
- **`config_matches()`**: Compares current config hash with saved hash
- **`hash_stage_config()`**: Creates SHA256 hash of relevant config keys
- **`save_stage_hash()`**: Saves hash to `.config_hash.txt` file

### **3. Stage-Specific Processing**

#### **Processed Subjects Stage**
- **Keys**: `["feature_extraction", "preprocessing"]`
- **Reuse Flag**: `reuse_processed_subjects`
- **Save Flag**: `save_processed_subjects`
- **Path**: `./data/testLaptop/processed_subjects/`

### **4. Data Processing Pipeline**
1. **Extract subjects** from config groups
2. **Check for existing data** using hash validation
3. **Process subjects** (if not reusing) using DataFrames
4. **Save processed subjects** (if configured)
5. **Apply transformations** (if not 'None')
6. **Save transformed features** (if configured)

### **5. Hash File Structure**
```
./data/testLaptop/
├── processed_subjects/
│   ├── .config_hash.txt    # Hash of feature_extraction + preprocessing
│   └── *.parquet          # Processed subjects data
└── transformed/
    ├── .config_hash.txt    # Hash of feature_transformation + feature_extraction
    └── *.parquet          # Transformed features data
```

## 🎯 **Key Benefits**

1. **Reproducibility**: Identical configs always produce identical outputs
2. **Performance**: Skip recomputation when configs haven't changed
3. **Safety**: Prevent silent reuse of outdated outputs
4. **Transparency**: Clear logging of reuse decisions
5. **Flexibility**: Stage-specific config tracking
6. **Schema Enforcement**: DataFrame approach with proper schema validation

## 🔧 **Integration Points**

- **`process_subjects()`**: Orchestrates the entire pipeline
- **`data_io.py`**: Provides all hashing and reuse functionality
- **`process_subject()`**: Individual subject processing
- **`transform_features()`**: Feature transformations
- **`get_feature_schema()`**: Schema definition for DataFrames

This hierarchical approach ensures your EEG processing pipeline is both efficient and reproducible! 🚀 