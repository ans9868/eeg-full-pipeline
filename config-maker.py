from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List

import questionary
import yaml
import re


def infer_target() -> str:
    this_file = Path(
        __file__
    )  # no resolve as it gets absolute path which will be the parent directory as we are simlinking
    repo_name = this_file.parent.name
    print(f"Running config_maker from: {repo_name}")

    if repo_name == "eeg-pyspark-pipeline":
        return "pyspark-only"
    elif repo_name == "eeg-ray-tuner":
        return "ray-only"
    else:
        return "full"


def validate_downsampling_rate(rate_str: Optional[str]) -> Optional[float]:
    """Validate and convert downsampling rate input."""
    if not rate_str or rate_str.lower() == "none":
        return None
    try:
        rate = float(rate_str)
        if rate <= 0:
            raise ValueError("Rate must be positive")
        return rate
    except ValueError:
        print(
            "[ERROR] Invalid downsampling rate. Please enter a positive number or 'None'."
        )
        return None


def validate_integer_input(prompt: str, default: str = "", min_value: int = 1) -> str:
    """Validate and get integer input with retry logic."""
    while True:
        value = questionary.text(prompt, default=default).ask()
        try:
            int_value = int(value)
            if int_value < min_value:
                print(f"[ERROR] Value must be at least {min_value}. Please try again.")
                continue
            return str(int_value)
        except ValueError:
            print("[ERROR] Please enter a valid integer. Please try again.")
            continue


def build_config(target: str) -> Tuple[Dict[str, Any], str]:
    config: Dict[str, Any] = {}

    # 0. Metadata
    print("\n[0] Project Metadata")
    config["project"] = {}
    config["project"]["name"] = questionary.text("0.1 Project name:").ask()
    output_dir = questionary.text("0.2 Output directory (default is ./data):").ask()
    config["project"]["output_dir"] = output_dir if output_dir else "./data"
    config["project"]["experiment_type"] = questionary.select(
        "0.3 Experiment Type:", choices=["Classification", "Regression", "Clustering"]
    ).ask()

    # 0.4 Deployment Method
    config["project"]["deployment_method"] = questionary.select(
        "0.4 Deployment Method:",
        choices=["Docker", "Singularity with Slurm", "Singularity without Slurm"]
    ).ask()

    # 0.5 PySpark Resource Configuration
    if target == "pyspark" or target == "pyspark-only" or target == "full":
        print("\n[0.5] PySpark Resource Configuration")
        print("For example, for a 8-core CPU with 16GB memory, we can safely allocate:")
        print("  - 4 cores for the driver (master)")
        print("  - 6GB memory for the driver")
        print("  - 6GB memory for executors")
        print("  - 2 cores per executor")
        print("  - 8 shuffle partitions")
        print("This is the default and lightweight for testing.")
        
        edit_spark_config = questionary.select(
            "Do you want to edit the PySpark resource configuration?",
            choices=["Yes", "No (use defaults)"]
        ).ask()
        
        if edit_spark_config == "Yes":
            config["pyspark"] = {}
            config["pyspark"]["master"] = validate_integer_input(
                "Enter number of cores/threads to allocate (master):",
                default="4"
            )
            config["pyspark"]["driver_memory"] = validate_integer_input(
                "Enter driver memory in GB (e.g., 6):",
                default="6"
            )
            config["pyspark"]["executor_memory"] = validate_integer_input(
                "Enter executor memory in GB (e.g., 6):",
                default="6"
            )
            config["pyspark"]["executor_cores"] = validate_integer_input(
                "Enter executor cores/threads:",
                default="2"
            )
            config["pyspark"]["shuffle_partitions"] = validate_integer_input(
                "Enter shuffle partitions:",
                default="8"
            )
        else:
            # Use defaults
            config["pyspark"] = {
                "master": "4",
                "driver_memory": "6",
                "executor_memory": "6", 
                "executor_cores": "2",
                "shuffle_partitions": "8"
            }

    # If Singularity with Slurm is selected, ask for Slurm options based on target
    if config["project"]["deployment_method"] == "Singularity with Slurm":
        print("\n[0.6] SLURM Configuration")
        
        # Always ask for build options when using SLURM
        print("Recommended build options (10 minutes, 8GB RAM, 2 CPUs):")
        print("  --time=00:10:00 --mem=8G --cpus-per-task=2")
        build_slurm_options = questionary.text(
            "Enter SLURM options for building .sif containers:",
            default="--time=00:10:00 --mem=8G --cpus-per-task=2"
        ).ask()
        config["project"]["slurm_options_build"] = sanitize_slurm_options(build_slurm_options) if build_slurm_options else ""
        
        if target == "full":
            # Ask if user wants same or different SLURM options for PySpark and Ray
            slurm_choice = questionary.select(
                "SLURM options for PySpark and Ray:",
                choices=["Same options for both", "Different options for each"]
            ).ask()
            
            if slurm_choice == "Same options for both":
                slurm_options = questionary.text(
                    "Enter SLURM options for both PySpark and Ray (e.g., --time=24:00:00 --mem=16G --cpus-per-task=4):"
                ).ask()
                config["project"]["slurm_options_pyspark"] = sanitize_slurm_options(slurm_options) if slurm_options else ""
                config["project"]["slurm_options_ray"] = sanitize_slurm_options(slurm_options) if slurm_options else ""
            else:  # Different options
                pyspark_slurm = questionary.text(
                    "Enter SLURM options for PySpark (e.g., --time=12:00:00 --mem=8G --cpus-per-task=2):"
                ).ask()
                ray_slurm = questionary.text(
                    "Enter SLURM options for Ray (e.g., --time=24:00:00 --mem=16G --cpus-per-task=4):"
                ).ask()
                config["project"]["slurm_options_pyspark"] = sanitize_slurm_options(pyspark_slurm) if pyspark_slurm else ""
                config["project"]["slurm_options_ray"] = sanitize_slurm_options(ray_slurm) if ray_slurm else ""
        
        elif target == "pyspark-only":
            slurm_options = questionary.text(
                "Enter SLURM options for PySpark (e.g., --time=12:00:00 --mem=8G --cpus-per-task=2):"
            ).ask()
            config["project"]["slurm_options_pyspark"] = sanitize_slurm_options(slurm_options) if slurm_options else ""
        
        elif target == "ray-only":
            slurm_options = questionary.text(
                "Enter SLURM options for Ray (e.g., --time=24:00:00 --mem=16G --cpus-per-task=4):"
            ).ask()
            config["project"]["slurm_options_ray"] = sanitize_slurm_options(slurm_options) if slurm_options else ""

    # Use user-supplied project name and timestamp for config name
    project_name = config["project"]["name"] or "project"
    # Sanitize project name: lowercase, replace spaces with underscores, remove non-alphanumeric/underscore
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', project_name.replace(' ', '_').lower())
    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M")
    config_name = f"config_{sanitized_name}_{timestamp}.yaml"
    config["project"]["config_name"] = config_name

    if target == "pyspark-only" or target == "full":
        # 1. Data Input
        print("\n[1] Data Input")
        config["data_input"] = {}
        config["data_input"]["groups"] = {}
        group_number = 1
        while True:
            group_input = questionary.text(
                f"Enter comma-separated EEG paths for Group {group_number} (or 'done'):"
            ).ask()
            if group_input.lower() == "done":
                break
            if not group_input.strip():
                print("[ERROR] Please enter valid paths to the *.set/.fif files or 'done'")
                continue
            try:
                valid_paths = validate_eeg_paths([path.strip() for path in group_input.split(",") if path.strip()])
                config["data_input"]["groups"][f"group_{group_number}"] = valid_paths
            except ValueError as e:
                print(f"[ERROR] {e}")
                continue
            group_number += 1

        config["data_input"]["reuse_expanded"] = questionary.select(
            "Reuse expanded .set/.fif files if they exist?", choices=["Yes", "No"]
        ).ask()

        config["data_input"]["save_expanded"] = questionary.select(
            "Save expanded .set/.fif files for reuse?", choices=["Yes", "No"]
        ).ask()

        # 2. Preprocessing
        print("\n[2] Preprocessing")
        config["preprocessing"] = {}
        config["preprocessing"]["bands"] = questionary.checkbox(
            "Select bandpass filters to apply (for more precise options edit the config file directly):",
            choices=["Delta", "Theta", "Alpha", "Beta", "Gamma"],
        ).ask()

        # Ask for sliding window amount (float between 0 and 0.95)
        while True:
            sliding_window_input = questionary.text(
                "Sliding window amount (0 for none, up to 0.95 for max):"
            ).ask()
            try:
                sliding_window = float(sliding_window_input)
                if 0 <= sliding_window <= 0.95:
                    break
                else:
                    print("[ERROR] Please enter a float between 0 and 0.95.")
            except (ValueError, TypeError):
                print("[ERROR] Please enter a valid float value.")
        config["preprocessing"]["sliding_window"] = sliding_window

        # Handle downsampling rate with validation
        while True:
            downsampling_input = questionary.text("Downsampling rate (Hz) or 'None':").ask()
            downsampling_rate = validate_downsampling_rate(downsampling_input)
            if downsampling_rate is not None or downsampling_input.lower() == "none":
                break
        config["preprocessing"]["downsampling"] = downsampling_rate

        config["preprocessing"]["artifact_removal"] = questionary.select(
            "Artifact removal method:",
            choices=["ICA", "Auto-reject", "Where noted in the data", "None"],
        ).ask()

        # 3. Feature Extraction
        print("\n[3] Feature Extraction")
        config["feature_extraction"] = {}
        config["feature_extraction"]["method"] = questionary.select(
            "Extraction method:",
            choices=[
                "Welch (default)",
                "Multitaper (slower, more precise)",
                "Raw FFT (slowest, most precise)",
            ],
        ).ask()
        config["feature_extraction"]["features"] = questionary.checkbox(
            "Select features to compute:",
            choices=[
                "Band Power (averaged across all channels/bands)",
                "Band Power (per channel, averaged across bands)",
                "Band Power (averaged across channels, per band) *(not usually used)",
                "Band Power (per channel per band) *recommended",
            ],
        ).ask()

        # 4. Feature Transformation
        print("\n[4] Feature Transformation")
        config["feature_transformation"] = {}
        config["feature_transformation"]["transformations"] = questionary.select(
            "Select a transformation to apply (for more precise options edit the config file directly):",
            choices=[
                "PCA (retain 95% variance)",
                "PCA (manual count)",
                # "SPCA (manual count)",
                "MinMax scaler",
                "Z-score standardization",
                "None",
            ],
        ).ask()

        config["feature_transformation"]["synthetic"] = questionary.select(
            "Synthetic data generation method:",
            choices=[
                # "SMOTE",
                # "Random over-sampling",
                # "Class weights only",
                "None"
            ],
        ).ask()

    if target == "ray-only" or target == "full":
        # 5. Classification
        print("\n[5] Classification")
        config["classification"] = {}
        config["classification"]["split_method"] = questionary.select(
            "How should we split the test/train sets?",
            choices=[
                "By subject",
                "By epoch",
                # "By event(s)",
                # "Custom"
            ],
        ).ask()

        # Ask for split details based on the selected method (only for ray target)
        if config["classification"]["split_method"] == "By subject":
            split_input = questionary.text(
                "Enter number of subjects for test set (e.g., 5) or percentage (e.g., 20%):"
            ).ask()
        else:  # By epoch
            split_input = questionary.text(
                "Enter percentage of epochs for test set (e.g., 20%):"
            ).ask()
        
        config["classification"]["test_split"] = split_input

    return config, config_name


def save_config(config: Dict[str, Any], config_name: str) -> None:
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)

    full_path = config_dir / config_name

    # Check if any other config files already exist
    existing = list(config_dir.glob("config_*.yaml"))
    if existing:
        print(f"⚠️ Found {len(existing)} existing config(s) in 'config/'.")
        print(f"⚠️ This new one will be used by default: {config_name}")

    # Save new config file
    with open(full_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"\n✅ Saved configuration to {full_path.resolve()}")


def sanitize_slurm_options(options: str) -> str:
    # Remove newlines and extra spaces
    return ' '.join(options.split())


def validate_eeg_paths(paths: List[str]) -> List[str]:
    """Validate EEG file paths - check they exist and don't contain spaces."""
    valid_paths = []
    for path in paths:
        path = path.strip()
        if not path:
            continue
            
        # Check for spaces in path
        if ' ' in path:
            raise ValueError(f"Path contains spaces: '{path}'. Please use paths without spaces.")
        
        # Check if file exists
        if not Path(path).exists():
            raise ValueError(f"File does not exist: '{path}'")
        
        # Check if it's a valid EEG file (optional - basic check)
        if not (path.endswith('.set') or path.endswith('.fif')):
            print(f"⚠️ Warning: '{path}' doesn't end with .set or .fif")
        
        valid_paths.append(path)
    
    return valid_paths


if __name__ == "__main__":
    target: str = infer_target()
    print(f"Generating config for target: {target}")
    config, config_name = build_config(target=target)
    save_config(config, config_name)
