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
        "0.3 Experiment Type:", choices=["Classification", "Clustering"] # "Regression"
    ).ask()

    config["project"]["subjects_or_events"] = questionary.select(
        "0.4 Are we analyzing subjects or events:", choices=["subjects", "events"]
    ).ask()

    # 0.4.1 Event selection (only if analyzing events)
    if config["project"]["subjects_or_events"] == "events":
        events_input = questionary.text(
            "0.4.1 Enter comma-separated list of events to analyze (must match exactly as written in the data):"
        ).ask()
        if events_input.strip():
            config["project"]["events_of_interest"] = [event.strip() for event in events_input.split(",") if event.strip()]
        else:
            config["project"]["events_of_interest"] = []

    # 0.4.2 Artifact removal method (fundamental metadata)
    config["project"]["artifact_removal"] = questionary.select(
        "0.4.2 Artifact removal method (defines how data was processed):",
        choices=["ICA", "Auto-reject where noted in the data", "None"], #costum list of events to remove
    ).ask()

 

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
        # TODO: Check if the paths are in the correct group in [1] data inputs
        # TODO: check if there is no overlap between the groups
        while True:
            # Ask for group name first
            group_name = questionary.text(
                f"What is the name for group number {group_number}? (e.g., 'alz', 'control', 'patient') (or 'done' to finish):"
            ).ask()
            
            if group_name.lower() == "done":
                # Check if we have at least 1 group with at least 1 path
                if len(config["data_input"]["groups"]) == 0:
                    print("[ERROR] You must enter at least 1 group with at least 1 path before finishing.")
                    continue
                break
            
            if not group_name.strip():
                print("[ERROR] Please enter a valid group name or 'done'")
                continue
            
            # Validate group name length and content
            if len(group_name.strip()) > 8:
                print("[ERROR] Group name must be 8 characters or less. Please use a shorter name.")
                continue
            
            # Check if group name contains file path indicators (likely user mistake)
            if '/' in group_name or '\\' in group_name or group_name.endswith('.set') or group_name.endswith('.fif'):
                print("[ERROR] It looks like you entered file paths instead of a group name.")
                print("Please enter a short group name (e.g., 'alz', 'control', 'patient') and then provide the file paths in the next step.")
                continue
            
            # Sanitize group name: lowercase, replace spaces with underscores, remove non-alphanumeric/underscore
            sanitized_group_name = re.sub(r'[^a-zA-Z0-9_]', '', group_name.replace(' ', '_').lower())
            
            # Check if group name already exists
            if sanitized_group_name in config["data_input"]["groups"]:
                print(f"[ERROR] Group name '{sanitized_group_name}' already exists. Please choose a different name.")
                continue
            
            # Ask for paths for this group - use a separate loop for path validation
            while True:
                group_input = questionary.text(
                    f"Enter comma-separated EEG paths for the '{group_name}' group:"
                ).ask()
                
                if not group_input.strip():
                    print("[ERROR] Please enter valid paths to the *.set/.fif files")
                    continue
                    
                try:
                    valid_paths = validate_eeg_paths([path.strip() for path in group_input.split(",") if path.strip()])
                    if len(valid_paths) == 0:
                        print("[ERROR] At least 1 valid path is required per group.")
                        continue
                    config["data_input"]["groups"][sanitized_group_name] = valid_paths
                    group_number += 1
                    break  # Successfully added group, exit the path input loop
                except ValueError as e:
                    print(f"[ERROR] {e}")
                    # Continue the inner loop to ask for paths again
                    continue

        config["data_input"]["reuse_expanded"] = questionary.select(
            "Reuse expanded .set/.fif files if they exist?", choices=["Yes", "No"]
        ).ask()

        config["data_input"]["save_expanded"] = questionary.select(
            "Save expanded .set/.fif files for reuse?", choices=["Yes", "No"]
        ).ask()

        config["data_input"]["reuse_feature_extracted"] = questionary.select(
            "Reuse feature extracted table (bandpower, entropy etc.) if it exists?", choices=["Yes", "No"]
        ).ask()

        config["data_input"]["save_feature_extracted"] = questionary.select(
            "Save feature extracted table (bandpower, entropy etc.) for reuse?", choices=["Yes", "No"]
        ).ask()

        config["data_input"]["reuse_transformed"] = questionary.select(
            "Reuse transformed table (extracted table post PCA, z-score etc.) if it exists?", choices=["Yes", "No"]
        ).ask()

        config["data_input"]["save_transformed"] = questionary.select(
            "Save transformed table (extracted table post PCA, z-score etc.) for reuse?", choices=["Yes", "No"]
        ).ask()


        # 2. Preprocessing
        print("\n[2] Preprocessing")
        config["preprocessing"] = {}
        
        
        
        # Define band frequency ranges
        band_ranges = {
            "Delta (0.5-4 Hz)": {"Delta": [0.5, 4]},
            "Theta (4-8 Hz)": {"Theta": [4, 8]},
            "Alpha (8-12 Hz)": {"Alpha": [8, 12]},
            "Beta (12-30 Hz)": {"Beta": [12, 30]},
            "Gamma (30-50 Hz)": {"Gamma": [30, 50]}
        }
        
        selected_bands_display = questionary.checkbox(
            "Select bandpass filters to apply (for more precise options edit the config file directly):",
            choices=[ key for key in band_ranges.keys() ],
        ).ask()
        
        # Convert display names to structured band data
        config["preprocessing"]["bands"] = {}
        for band_display in selected_bands_display:
            if band_display in band_ranges:
                config["preprocessing"]["bands"].update(band_ranges[band_display])

        # Ask for window size
        while True:
            window_size_input = questionary.text(
                "Enter window size in seconds (e.g., 1):"
            ).ask()
            try:
                window_size = float(window_size_input)
                if window_size > 0:
                    break
                else:
                    print("[ERROR] Please enter a positive number.")
            except (ValueError, TypeError):
                print("[ERROR] Please enter a valid number.")
        config["preprocessing"]["window_size"] = window_size

        # Ask for sliding window amount (float between 0 and 0.95)
        while True:
            sliding_window_input = questionary.text(
                "Sliding window amount as a percentage of the window size (0 for none, up to 0.95 for max):"
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

        # 5. Data Leakage Prevention (only if Classification and Feature Transformation are enabled)
        if target == "pyspark-only" or target == "full":
            if config["project"]["experiment_type"] == "Classification" and config["feature_transformation"]["transformations"] != "None":
                print("\n[5] Data Leakage Prevention")
                print("⚠️  WARNING: You selected Classification with Feature Transformation.")
                print("   This can cause data leakage if test data influences training transforms.")
                
                config["data_leakage_prevention"] = {}
                
                # Question 1: Data leakage prevention strategy
                config["data_leakage_prevention"]["strategy"] = questionary.select(
                    "How would you like to handle data leakage during feature transformation?",
                    choices=[
                        "Rotate test subjects and recompute transforms for each fold (slow, very storage heavy, most reliable)",
                        "1 test/1 train split with transforms applied to training set only (faster, single split)",
                        "Transform all data together (no split - fastest, and potential data leakage)"
                    ]
                ).ask()
                
                # Question 2: Test subject definition (if rotation is selected)
                if "Rotate test subjects" in config["data_leakage_prevention"]["strategy"]:
                    config["data_leakage_prevention"]["test_subject_method"] = questionary.select(
                        "How would you like to define test subjects for rotation?",
                        choices=[
                            "Manually select X test subjects per fold and provide full paths",
                            "Automatically rotate all subjects (leave-X-out cross-validation)"
                        ]
                    ).ask()
                    
                    if "Manually select" in config["data_leakage_prevention"]["test_subject_method"]:
                        # Ask for number of test subjects per fold
                        while True:
                            test_subjects_count = questionary.text(
                                "Enter the number of test subjects per fold (e.g., 2):"
                            ).ask()
                            try:
                                count = int(test_subjects_count)
                                if count > 0:
                                    config["data_leakage_prevention"]["test_subjects_per_fold"] = count
                                    break
                                else:
                                    print("[ERROR] Please enter a positive number.")
                            except ValueError:
                                print("[ERROR] Please enter a valid integer.")
                        
                        # Ask for fold paths
                        config["data_leakage_prevention"]["fold_paths"] = {}
                        fold_number = 1
                        
                        # Get available group names for reference
                        available_groups = list(config["data_input"]["groups"].keys())
                        groups_text = ", ".join(available_groups)
                        
                        while True:
                            fold_input = questionary.text(
                                f"Enter comma-separated paths to test subjects for fold {fold_number} (or 'done')\n*Notice these paths should have been inputed in the correct group in [1] data inputs.\nAvailable groups: {groups_text}"
                            ).ask()
                            if fold_input.lower() == "done":
                                break
                            if not fold_input.strip():
                                print("[ERROR] Please enter valid paths or 'done'")
                                continue
                            
                            # Validate paths
                            try:
                                fold_paths = [path.strip() for path in fold_input.split(",") if path.strip()]
                                valid_fold_paths = validate_eeg_paths(fold_paths)
                                
                                # Check if paths exist in groups from part 1
                                found_paths, missing_paths = check_paths_in_groups(valid_fold_paths, config["data_input"]["groups"])
                                
                                if missing_paths:
                                    print(f"⚠️  WARNING: The following paths were not found in part 1 groups: {', '.join(missing_paths)}")
                                    action = questionary.select(
                                        "What would you like to do?",
                                        choices=["Exit program (go back to [1] to add missing paths)", "Re-enter paths for this fold"]
                                    ).ask()
                                    if action == "Exit program (go back to [1] to add missing paths)":
                                        print("Exiting config maker. Please run it again and add the missing paths in [1] Data Input.")
                                        exit(0)
                                    else:
                                        continue
                                
                                # Check if number of subjects matches expected count
                                if len(valid_fold_paths) != config["data_leakage_prevention"]["test_subjects_per_fold"]:
                                    confirm = questionary.select(
                                        f"⚠️  You entered {len(valid_fold_paths)} subjects but expected {config['data_leakage_prevention']['test_subjects_per_fold']}. Continue anyway?",
                                        choices=["Yes, continue", "No, re-enter"]
                                    ).ask()
                                    if confirm == "No, re-enter":
                                        continue
                                
                                config["data_leakage_prevention"]["fold_paths"][f"fold_{fold_number}"] = valid_fold_paths
                                fold_number += 1
                                
                            except ValueError as e:
                                print(f"[ERROR] {e}")
                                continue
                    
                    elif "Automatically rotate" in config["data_leakage_prevention"]["test_subject_method"]:
                        # Ask for number of test subjects to leave out
                        while True:
                            leave_out_count = questionary.text(
                                "Enter the number of subjects to leave out per fold (e.g., 2):"
                            ).ask()
                            try:
                                count = int(leave_out_count)
                                if count > 0:
                                    config["data_leakage_prevention"]["leave_out_count"] = count
                                    break
                                else:
                                    print("[ERROR] Please enter a positive number.")
                            except ValueError:
                                print("[ERROR] Please enter a valid integer.")
                
                # Question 2: Single train/test set definition (if single split is selected)
                elif "1 test/1 train split" in config["data_leakage_prevention"]["strategy"]:
                    config["data_leakage_prevention"]["single_split_method"] = questionary.select(
                        "How would you like to define this 1 training/testing set?",
                        choices=[
                            "Manually select test subjects and provide full paths",
                            "Automatically split subjects (e.g., 5 test subjects)"
                        ]
                    ).ask()
                    
                    if "Manually select" in config["data_leakage_prevention"]["single_split_method"]:
                        # Ask for number of test subjects
                        while True:
                            test_subjects_count = questionary.text(
                                "Enter the number of test subjects (e.g., 5):"
                            ).ask()
                            try:
                                count = int(test_subjects_count)
                                if count > 0:
                                    config["data_leakage_prevention"]["test_subjects_count"] = count
                                    break
                                else:
                                    print("[ERROR] Please enter a positive number.")
                            except ValueError:
                                print("[ERROR] Please enter a valid integer.")
                        
                        # Ask for test subject paths with validation
                        # Get available group names for reference
                        available_groups = list(config["data_input"]["groups"].keys())
                        groups_text = ", ".join(available_groups)
                        
                        while True:
                            test_subjects_input = questionary.text(
                                f"Enter comma-separated paths to test subjects (expected {config['data_leakage_prevention']['test_subjects_count']} subjects)\n*Notice these paths should have been inputed in the correct group in [1] data inputs.\nAvailable groups: {groups_text}"
                            ).ask()
                            if not test_subjects_input.strip():
                                print("[ERROR] Please enter valid paths.")
                                continue
                            
                            try:
                                test_paths = [path.strip() for path in test_subjects_input.split(",") if path.strip()]
                                valid_test_paths = validate_eeg_paths(test_paths)
                                
                                # Check if paths exist in groups from part 1
                                found_paths, missing_paths = check_paths_in_groups(valid_test_paths, config["data_input"]["groups"])
                                
                                if missing_paths:
                                    print(f"⚠️  WARNING: The following paths were not found in part 1 groups: {', '.join(missing_paths)}")
                                    action = questionary.select(
                                        "What would you like to do?",
                                        choices=["Exit program (go back to [1] to add missing paths)", "Re-enter paths for this test set"]
                                    ).ask()
                                    if action == "Exit program (go back to [1] to add missing paths)":
                                        print("Exiting config maker. Please run it again and add the missing paths in [1] Data Input.")
                                        exit(0)
                                    else:
                                        continue
                                
                                # Check if number of subjects matches expected count
                                if len(valid_test_paths) != config["data_leakage_prevention"]["test_subjects_count"]:
                                    confirm = questionary.select(
                                        f"⚠️  You entered {len(valid_test_paths)} subjects but expected {config['data_leakage_prevention']['test_subjects_count']}. Continue anyway?",
                                        choices=["Yes, continue", "No, re-enter"]
                                    ).ask()
                                    if confirm == "No, re-enter":
                                        continue
                                
                                config["data_leakage_prevention"]["test_subjects_paths"] = valid_test_paths
                                break
                                
                            except ValueError as e:
                                print(f"[ERROR] {e}")
                                continue
                    
                    elif "Automatically split" in config["data_leakage_prevention"]["single_split_method"]:
                        # Ask for number of test subjects
                        while True:
                            test_subjects_count = questionary.text(
                                "Enter number of subjects for test set (e.g., 5):"
                            ).ask()
                            try:
                                count = int(test_subjects_count)
                                if count > 0:
                                    config["data_leakage_prevention"]["test_subjects_count"] = count
                                    break
                                else:
                                    print("[ERROR] Please enter a positive number.")
                            except ValueError:
                                    print("[ERROR] Please enter a valid integer.")
                
                # Question 2: No split needed (if transform all data is selected)
                elif "Transform all data together" in config["data_leakage_prevention"]["strategy"]:
                    print("⚠️  WARNING: You selected to transform all data together.")
                    print("   This may cause data leakage as test data will influence training transforms.")
                    print("   No additional configuration needed - all data will be transformed together.")
                
    else:
        print("\nSkipping [1] Data Input [2] Preprocessing [3] Feature Extraction [4] Feature Transformation, and [5] Data Leakage Prevention as we are not using PySpark")

    # 6. Deployment Configuration
    print("\n[6] Deployment Configuration")
    config["project"]["deployment_method"] = questionary.select(
        "6.1 Deployment Method:",
        choices=["Docker", "Singularity with Slurm", "Singularity without Slurm"]
    ).ask()

    # 6.2 PySpark Resource Configuration
    if target == "pyspark" or target == "pyspark-only" or target == "full":
        print("\n[6.2] PySpark Resource Configuration")
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

    # 6.3 SLURM Configuration (if Singularity with Slurm is selected)
    if config["project"]["deployment_method"] == "Singularity with Slurm":
        print("\n[6.3] SLURM Configuration")
        
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


def check_paths_in_groups(paths: List[str], groups: Dict[str, List[str]]) -> Tuple[List[str], List[str]]:
    """Check which paths exist in groups and which don't. Returns (found_paths, missing_paths)."""
    found_paths = []
    missing_paths = []
    
    # Flatten all paths from all groups
    all_group_paths = []
    for group_paths in groups.values():
        all_group_paths.extend(group_paths)
    
    for path in paths:
        if path in all_group_paths:
            found_paths.append(path)
        else:
            missing_paths.append(path)
    
    return found_paths, missing_paths


if __name__ == "__main__":
    target: str = infer_target()
    print(f"Generating config for target: {target}")
    config, config_name = build_config(target=target)
    save_config(config, config_name)