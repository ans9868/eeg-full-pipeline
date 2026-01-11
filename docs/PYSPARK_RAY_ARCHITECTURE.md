# PySpark and Ray Architecture Overview

This document explains how PySpark and Ray containers work together in the EEG Full Pipeline, including how they exchange information and read from configuration files.

## 🏗️ Overall Architecture

The pipeline consists of two main stages that run sequentially:

1. **PySpark Container** - Data processing and feature extraction
2. **Ray Container** - Machine learning hyperparameter optimization

Both containers read from the **same YAML configuration file** and communicate through **shared file system mounts**.

---

## 📦 Container Architecture

### Container Definitions

The containers are defined in `start-pipelines.py`:

```44:88:start-pipelines.py
CONTAINER_CONFIG = {
    "pyspark": {
        "docker_image": "nour333/eeg-spark-pipeline:latest",
        "singularity_image": "./containers/eeg-pyspark-pipeline.sif",
        "entrypoint": "/app/main.py",
        "command": "spark-submit",
        "job_name": "pyspark-pipeline",
        # Spark-submit specific configurations (most Spark configs are in session_builder.py)
        "spark_configs": ["--conf", "spark.jars.ivy=/tmp/.ivy2"],
        "mounts": [
            # ("./config_handler.py", "/app/config_handler.py"),
            (
                "./config/spark",
                "/opt/bitnami/spark/conf",
            ),  # Spark configs (editable) - removing this puts spark logs in console
            
            # Log mounts are now added dynamically based on config[project][config_name]
            # ("./logs/spark-events", "/opt/bitnami/spark/logs/"),  # Spark event logs - COMMENTED OUT: Added dynamically
            # Done through config file
            # (f"./config/{user_config_namec}", "/app/config"),   # User YAML configs (editable)
            # ("./data", "/app/data"),
            # and all the eeg data
        ],
        "ports": ["4040:4040"],
        "expose_spark_ui": True,  # Whether to expose Spark UI port for HPC access
    },
    "ray": {
        "docker_image": "nour333/eeg-ray-tuner:latest",
        "singularity_image": "./containers/eeg-ray-tuner.sif",
        "entrypoint": "/app/main.py",
        # "entrypoint": "/app/test-ray.py",
        "command": "python",
        "job_name": "ray-tuner",
        "mounts": [
            # ("./config_handler.py", "/app/config_handler.py"),
            # Log mounts are now added dynamically based on config[project][config_name]
            # ("./logs/ray-events", "/app/logs/ray-events"),  # Ray event logs - COMMENTED OUT: Added dynamically
            # Done through config file
            # (f"./config/{user_config_namec}", "/app/config"),   # User YAML configs (editable)
            # ("./data", "/app/data"),
        ],
        # "ports": [ # TODO: add ray ports if needed]
        "ports": ["8265:8265"], # ask ports in config but now using those ... ? 
    },
}
```

### Container Images

1. **PySpark Container** (`nour333/eeg-spark-pipeline:latest`)
   - Based on `bitnamilegacy/spark:4.0.0`
   - Contains PySpark and all data processing libraries
   - Entrypoint: `/app/main.py`
   - Command: `spark-submit /app/main.py --config /app/config.yaml`

2. **Ray Container** (`nour333/eeg-ray-tuner:latest`)
   - Based on `python:3.10-slim`
   - Contains Ray, Ray Tune, and ML libraries
   - Entrypoint: `/app/main.py`
   - Command: `python /app/main.py --config /app/config.yaml`

---

## 📂 Shared File System Architecture

### Key Mount Points

Both containers share the same mounts for communication:

```261:313:start-pipelines.py
def get_all_mount_mappings(
    container_type: str, config_path: str, config_data: Dict[str, Any]
) -> List[Tuple[str, str]]:
    """Get all mount mappings for a container type based on CONTAINER_CONFIG."""
    container_config = CONTAINER_CONFIG[container_type]
    mount_mappings = []

    # Add specific config file mount
    mount_mappings.append((config_path, "/app/config.yaml"))

    # Get output directory from config or use default
    output_dir = config_data.get("project", {}).get("output_dir", "./data")

    # Get config name for dynamic log directory creation
    config_name = config_data.get("project", {}).get("name", "default")
    
    # Generate timestamp in format '2025-09-03_1741' for current datetime
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    
    # Create dynamic log directories based on config name and timestamp
    if container_type == "pyspark":
        log_dir = f"./logs/spark-events/{config_name}_{timestamp}"
        container_log_path = "/opt/bitnami/spark/logs/"
    elif container_type == "ray":
        log_dir = f"./logs/ray-events/{config_name}_{timestamp}"
        container_log_path = "/app/logs/ray-events"
    else:
        log_dir = None
        container_log_path = None
    
    # Create the log directory if it exists
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        print(f"{EMOJI_CREATING} Created/verified log directory: {log_dir}")
        # Add dynamic log mount
        mount_mappings.append((log_dir, container_log_path))
        print(f"{EMOJI_MOUNTING} Adding dynamic log mount: {log_dir} -> {container_log_path}")

    # TODO don't need to mount .set directories for ray tuner
    # Create required directories
    create_required_directories(output_dir)

    # Add static mounts from configuration
    mount_mappings.extend(container_config["mounts"])

    # Add output directory mount with write permissions
    mount_mappings.append((output_dir, "/app/data"))

    # Add dynamic mounts (built from user config)
    dynamic_mounts = build_user_mounts(config_data)
    mount_mappings.extend(dynamic_mounts)

    return mount_mappings
```

### Shared Mounts

| Host Path | PySpark Container | Ray Container | Purpose |
|-----------|-------------------|---------------|---------|
| `config_path` | `/app/config.yaml` | `/app/config.yaml` | **Shared configuration file** |
| `output_dir` (e.g., `./data`) | `/app/data` | `/app/data` | **Shared data directory** |
| `./config/spark` | `/opt/bitnami/spark/conf` | N/A | Spark configuration |
| `logs/spark-events/{name}_{timestamp}` | `/opt/bitnami/spark/logs/` | N/A | Spark logs |
| `logs/ray-events/{name}_{timestamp}` | N/A | `/app/logs/ray-events` | Ray logs |
| Input data files (from config) | Same paths | Same paths | Raw EEG data files |

---

## 🔄 Data Flow Between Containers

### Phase 1: PySpark Container Execution

1. **Configuration Loading**
   - Reads `/app/config.yaml` (mounted from host)
   - Uses `UnifiedConfigHandler` to parse and validate config

2. **Data Processing**
   - Reads raw EEG data from mounted input paths
   - Processes subjects through stages:
     - `processed_subjects/` - Initial processing
     - `transformed/` - Final transformed features

3. **Output Structure**
   PySpark writes output to `/app/data/{project_name}/` with this structure:
   ```
   /app/data/{project_name}/
   ├── processed_subjects/
   │   └── fold_*/  (depending on split strategy)
   │       └── *.parquet
   └── transformed/
       └── fold_*/  (depending on split strategy)
           └── *.parquet
   ```

   The output directory structure depends on the `data_leakage_strategy`:
   - **Within-subject**: `transformed/fold_*/`
   - **LPSO**: `transformed/lpso_*/`
   - **1 test/1 train split**: `transformed/train/` and `transformed/test/`
   - **All data together**: `transformed/all/`

### Phase 2: Ray Container Execution

1. **Wait for PySpark** (in SLURM mode)
   - Ray job has `--dependency=afterok:{pyspark_job_id}`

2. **Configuration Loading**
   - Reads **same** `/app/config.yaml` file
   - Uses `UnifiedConfigHandler` to get data paths

3. **Data Discovery**
   Ray discovers where PySpark wrote the data:
   
   ```1477:1531:eeg-ray-tuner/eeg_ray_tuner/tuning/base_search_strategy.py
        This function now supports both processed_subjects and transformed stages,
   ```
   
   It looks for data in this order:
   1. **Transformed stage** (preferred for ML) - `transformed/`
   2. **Processed subjects stage** (fallback) - `processed_subjects/`

4. **Data Loading**
   Ray loads parquet files using `ray.data.read_parquet()`:
   
   ```40:78:eeg-ray-tuner/eeg_ray_tuner/models/model_runner.py
   def load_data_directory(data_dir: str, logger=None) -> Optional[ray.data.Dataset]:
       """this loads the data from the directory
   
       Parameters
       ----------
       data_dir : str
           path to the directory containing the data
       logger : _type_, optional
           logger instance for logging
   
       Returns
       -------
       Optional[ray.data.Dataset]
           ray.data.Dataset if successful, None if failed
       """
   
       if logger is None:
           logger = logging.getLogger(__name__)
       
       try:
           print(f"   🔄 Attempting to load directory: {data_dir}")
           logger.info(f"   🔄 Attempting to load directory: {data_dir}")
           # Restrict to parquet files only to avoid hidden files like ._SUCCESS.crc
           # Sort paths to ensure deterministic loading order across runs
           parquet_paths = sorted(glob.glob(os.path.join(data_dir, "*.parquet")))
           if not parquet_paths:
               logger.warning(f"   ⚠️  No parquet files found in directory: {data_dir}")
               return None
           logger.info(f"   📁 Loading {len(parquet_paths)} parquet files in deterministic order")
           ds = ray.data.read_parquet(parquet_paths)
           row_count = ds.count()
           logger.info(f"   ✅ Successfully loaded directory: {row_count} rows")
           print(f"   ✅ Successfully loaded directory: {row_count} rows")
           return ds
       except Exception as e:
           logger.warning(f"   ⚠️  Failed to load directory {data_dir}: {e}")
           print(f"   ❌ Failed to load directory {data_dir}: {e}")
           return None
   ```

5. **ML Training & Optimization**
   - Ray runs hyperparameter optimization
   - Saves results to `/app/data/{project_name}/ml_results_{strategy}/`

---

## 📋 Configuration File Structure

Both containers read from the **same YAML configuration file**. The config contains:

### Sections Read by Both Containers

1. **`project`** - Project metadata
   - `name`: Project name
   - `output_dir`: Shared output directory
   - `experiment_type`: Determines if Ray runs

2. **`data_input`** - Input data paths
   - Both containers need access to raw EEG files

### Sections Read by PySpark Only

- `preprocessing` - Signal preprocessing settings
- `feature_extraction` - Feature extraction configuration
- `feature_transformations` - Transformations applied
- `data_leakage_prevention` - Split strategies

### Sections Read by Ray Only

- `ray` - Ray cluster and tuning configuration
- `models` - Model configurations to train
- `hyperparameter_search` - Search strategies (grid, ax, etc.)

### Configuration Loading

Both containers use the same `UnifiedConfigHandler`:

```41:86:config_handler.py
    def __init__(self, config_path: str):
        """Initialize the unified configuration handler.

        Parameters
        ----------
        config_path : str
            Path to the configuration YAML file
        """
        self.config_path = config_path
        self.raw_config = None
        self._load_and_validate()

    # ========================================
    # CORE LOADING AND VALIDATION
    # ========================================

    def _load_and_validate(self) -> None:
        """Load and validate the configuration in one step."""
        self.raw_config = self._load_config()
        self._validate_config()
        print("✅ Configuration loaded and validated successfully!")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        print(f"🔧 Loading configuration from: {self.config_path}")

        # Check if config file exists
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, "r") as f:
                config = cast(Dict[str, Any], yaml.safe_load(f))

            if config is None:
                raise ValueError("Configuration file is empty")

            print("📋 Configuration loaded successfully!")
            return config

        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML configuration: {e}")
            raise
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            raise
```

---

## 🔗 Container Execution Flow

### Local/Docker Execution

```606:612:start-pipelines.py
def run_docker(config_path: str) -> None:
    print(f"\n{EMOJI_DOCKER} Running PySpark container...")
    run_docker_container("pyspark", config_path)

    print(f"\n{EMOJI_DOCKER} Running Ray pipeline container...")
    run_docker_container("ray", config_path)
```

1. PySpark container runs first
2. Ray container runs after PySpark completes

### SLURM Execution (HPC)

```711:749:start-pipelines.py
def run_singularity_with_slurm_separate_options(
    config_path: str, pyspark_slurm_options: str = "", ray_slurm_options: str = ""
) -> None:
    """Run full pipeline with separate SLURM options for each container."""
    print(f"\n{EMOJI_SUBMITTING} Submitting PySpark SLURM job...")

    # Create temporary SLURM script for PySpark
    pyspark_slurm_content = create_slurm_script(
        "pyspark", config_path, pyspark_slurm_options
    )

    with open("./containers/temp_pyspark.slurm", "w") as f:
        f.write(pyspark_slurm_content)

    pyspark_submit = subprocess.run(
        ["sbatch", "./containers/temp_pyspark.slurm"], capture_output=True, text=True
    )
    print(pyspark_submit.stdout.strip())

    # Extract job ID
    try:
        job_id = pyspark_submit.stdout.strip().split()[-1]
    except IndexError:
        print(f"{EMOJI_ERROR} Failed to get job ID from sbatch output.")
        sys.exit(1)

    # Create temporary SLURM script for Ray with dependency
    ray_slurm_content = create_slurm_script(
        "ray", config_path, ray_slurm_options, job_id
    )

    with open("./containers/temp_ray.slurm", "w") as f:
        f.write(ray_slurm_content)

    print(
        f"\n{EMOJI_SUBMITTING} Submitting Ray pipeline SLURM job (after PySpark job {job_id})..."
    )
    subprocess.run(["sbatch", "./containers/temp_ray.slurm"], check=True)

    # Clean up temporary files
    os.remove("./containers/temp_pyspark.slurm")
    os.remove("./containers/temp_ray.slurm")
```

1. Submit PySpark SLURM job
2. Wait for job ID
3. Submit Ray SLURM job with `--dependency=afterok:{pyspark_job_id}`
4. SLURM scheduler ensures Ray runs after PySpark completes

---

## 📊 Data Exchange Mechanism

### How Data Flows

1. **PySpark writes to**: `/app/data/{project_name}/transformed/`
2. **Ray reads from**: `/app/data/{project_name}/transformed/`
3. **Ray writes to**: `/app/data/{project_name}/ml_results_{strategy}/`

Both containers see the **same `/app/data` directory** because it's mounted from the same host path (`output_dir` from config).

### Path Resolution in Containers

**PySpark Container:**
- Output: `/app/data/{project_name}/transformed/fold_*/`
- Determined from `config_handler.output_dir` + `config_handler.project_name`

**Ray Container:**
- Input: Same paths discovered dynamically
- Checks for `/app/data` first (container mode), then falls back to host paths
- Uses `_discover_transformed_folds()` to find PySpark output

---

## 🔍 Key Design Decisions

### Why Shared Mounts?

1. **No Network Communication Needed** - Both containers access the same filesystem
2. **Simple Dependency Management** - File presence indicates completion
3. **Container Independence** - Containers don't need to know about each other
4. **HPC Compatible** - Works with SLURM job dependencies

### Why Same Config File?

1. **Consistency** - Both containers use same project name and paths
2. **Single Source of Truth** - One config file to maintain
3. **Validation** - `UnifiedConfigHandler` ensures both sides validate the same way

### Why Parquet Format?

1. **PySpark Native** - PySpark writes parquet efficiently
2. **Ray Compatible** - Ray can read parquet with `ray.data.read_parquet()`
3. **Columnar Format** - Efficient for ML workloads
4. **Schema Preservation** - Maintains data types and column names

---

## 🚀 Summary

The architecture uses:

1. **Two Container Images**: Separate PySpark and Ray containers
2. **Shared File System**: Same config file and data directory mounted into both
3. **Sequential Execution**: PySpark writes → Ray reads (via SLURM dependency or sequential Docker)
4. **Unified Config**: Both containers use `UnifiedConfigHandler` to read the same YAML
5. **Dynamic Discovery**: Ray automatically finds PySpark output based on config strategy

This design allows the containers to work together seamlessly without requiring network communication or shared state management systems.


