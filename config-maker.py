import re
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import questionary
import yaml

"""
max push for m4 mini 24gb
should allow for this here type of setup ... more things to setup
spark.master                          spark://localhost:7077
spark.dynamicAllocation.enabled       false

spark.driver.cores                    2
spark.driver.memory                   6g
spark.driver.maxResultSize            4g

spark.executor.instances              1
spark.executor.cores                  8
spark.executor.memory                 14g
spark.executor.memoryOverhead         3g

spark.sql.shuffle.partitions          96
spark.serializer                      org.apache.spark.serializer.KryoSerializer
spark.sql.execution.arrow.pyspark.enabled true


"""


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
    elif repo_name == "eeg-full-pipeline":
        return "full"
    else:
        raise ValueError(
            f"Invalid repo name: {repo_name}. Please run this script from the root of the repository who's directory name is one of the following: (eeg-full-pipeline, eeg-ray-tuner, eeg-pyspark-pipeline)."
        )


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
    project_name_input = questionary.text("0.1 Project name:").ask()
    config["project"]["name"] = project_name_input.strip() if project_name_input else ""

    # Ensure project name is not empty
    if not config["project"]["name"]:
        print("⚠️  Warning: Project name is empty, using default name 'project'")
        config["project"]["name"] = "project"

    output_dir = questionary.text("0.2 Output directory (default is ./data):").ask()
    config["project"]["output_dir"] = output_dir.strip() if output_dir else "./data"
    experiment_type_choice = questionary.select(
        "0.3 Experiment Type:",
        choices=[
            "ML (Classification) - Predict categories (e.g., patient vs control, disease stages)",
            "ML (Clustering) - Find patterns/groups in data with labels",
            "Analysis (No Ray ML) - Process data for manual analysis, no automated ML",
        ],
    ).ask()

    # Extract simplified experiment type from the choice
    if "ML (Classification)" in experiment_type_choice:
        config["project"]["experiment_type"] = "ML (Classification)"
    elif "ML (Clustering)" in experiment_type_choice:
        config["project"]["experiment_type"] = "ML (Clustering)"
    elif "Analysis (No Ray ML)" in experiment_type_choice:
        config["project"]["experiment_type"] = "Analysis (No Ray ML)"
    else:
        config["project"]["experiment_type"] = "ML (Classification)"  # Default fallback

    config["project"]["subjects_or_events"] = questionary.select(
        "0.4 Are we analyzing subjects or events:", choices=["subjects", "events"]
    ).ask()

    # 0.4.1 Event selection (only if analyzing events)
    if config["project"]["subjects_or_events"] == "events":
        events_input = questionary.text(
            "0.4.1 Enter comma-separated list of events to analyze (must match exactly as written in the data):"
        ).ask()
        if events_input.strip():
            config["project"]["events_of_interest"] = [
                event.strip() for event in events_input.split(",") if event.strip()
            ]
        else:
            config["project"]["events_of_interest"] = []

    # 0.4.2 Artifact removal method (fundamental metadata)
    config["project"]["artifact_removal"] = questionary.select(
        "0.4.2 Artifact removal method (defines how data was processed):",
        choices=[
            # "ICA",
            "None",
        ],  # costum list of events to remove
    ).ask()

    # Use user-supplied project name and timestamp for config name
    project_name = config["project"]["name"] or "project"
    # Sanitize project name: lowercase, replace spaces with underscores, remove non-alphanumeric/underscore/dot
    sanitized_name = re.sub(
        r"[^a-zA-Z0-9_.]", "", project_name.replace(" ", "_").lower()
    )

    # Debug: show the sanitized name
    print(f"📝 Project name: '{project_name}' -> sanitized: '{sanitized_name}'")

    timestamp = datetime.now().strftime("%d-%m-%Y_%H%M")
    config_name = f"config_{sanitized_name}_{timestamp}.yaml"
    print(f"📝 Config name: '{config_name}'")
    config["project"]["config_name"] = config_name

    if target == "pyspark-only" or target == "full":
        # 1. Data Input
        print("\n[1] Data Input")
        config["data_input"] = {}
        config["data_input"]["groups"] = {}
        group_number = 1
        # TODO: check if there is no overlap between the groups
        while True:
            # Ask for group name first
            group_name_input = questionary.text(
                f"1.1.{group_number} What is the name for group number {group_number}? (e.g., 'alz', 'control', 'patient') (or 'done' to finish):"
            ).ask()
            group_name = group_name_input.strip() if group_name_input else ""

            if group_name.lower() == "done":
                # Check if we have at least 1 group with at least 1 path
                if len(config["data_input"]["groups"]) == 0:
                    print(
                        "[ERROR] You must enter at least 1 group with at least 1 path before finishing."
                    )
                    continue
                break

            if not group_name:
                print("[ERROR] Please enter a valid group name or 'done'")
                continue

            # Validate group name length and content
            if len(group_name.strip()) > 8:
                print(
                    "[ERROR] Group name must be 8 characters or less. Please use a shorter name."
                )
                continue

            # Check if group name contains file path indicators (likely user mistake)
            if (
                "/" in group_name
                or "\\" in group_name
                or group_name.endswith(".set")
                or group_name.endswith(".fif")
            ):
                print(
                    "[ERROR] It looks like you entered file paths instead of a group name."
                )
                print(
                    "Please enter a short group name (e.g., 'alz', 'control', 'patient') and then provide the file paths in the next step."
                )
                continue

            # Sanitize group name: lowercase, replace spaces with underscores, remove non-alphanumeric/underscore
            sanitized_group_name = re.sub(
                r"[^a-zA-Z0-9_]", "", group_name.replace(" ", "_").lower()
            )

            # Check if group name already exists
            if sanitized_group_name in config["data_input"]["groups"]:
                print(
                    f"[ERROR] Group name '{sanitized_group_name}' already exists. Please choose a different name."
                )
                continue

            # Ask for paths for this group - use a separate loop for path validation
            while True:
                group_input = questionary.text(
                    f"1.2.{group_number} Enter comma-separated EEG paths for the '{group_name}' group:"
                ).ask()

                if not group_input.strip():
                    print("[ERROR] Please enter valid paths to the *.set/.fif files")
                    continue

                try:
                    valid_paths = validate_eeg_paths(
                        [
                            path.strip()
                            for path in group_input.split(",")
                            if path.strip()
                        ]
                    )
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

        # This was to expand the EEG data into spark dataframes
        # config["data_input"]["reuse_raw"] = questionary.select(
        #     "Reuse raw data processing if it exists?", choices=["Yes", "No"]
        # ).ask()
        # config["data_input"]["save_raw"] = questionary.select(
        #     "Save raw data processing for reuse?", choices=["Yes", "No"]
        # ).ask()

        config["data_input"]["reuse_processed_subjects"] = questionary.select(
            "1.3 Reuse processed features (bandpower, entropy etc.) if they exist?",
            choices=["Yes", "No"],
        ).ask()
        config["data_input"]["save_processed_subjects"] = questionary.select(
            "1.4 Save processed features (bandpower, entropy etc.) for reuse?",
            choices=["Yes", "No"],
        ).ask()

        config["data_input"]["reuse_transformed"] = questionary.select(
            "1.5 Reuse transformed data (post PCA, z-score etc.) if it exists?",
            choices=["Yes", "No"],
        ).ask()
        config["data_input"]["save_transformed"] = questionary.select(
            "1.6 Save transformed data (post PCA, z-score etc.) for reuse? (Necessary for RayTuner to work)",
            choices=["Yes", "No"],
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
            "Gamma (30-50 Hz)": {"Gamma": [30, 50]},
        }

        selected_bands_display = questionary.checkbox(
            "2.1 Select bandpass filters to apply (for more precise options edit the config file directly) (all recommended except Gamma):",
            choices=[key for key in band_ranges.keys()],
        ).ask()

        # Convert display names to structured band data
        config["preprocessing"]["bands"] = {}
        for band_display in selected_bands_display:
            if band_display in band_ranges:
                config["preprocessing"]["bands"].update(band_ranges[band_display])

        # Ask for window size
        while True:
            window_size_input = questionary.text(
                "2.2 Enter window size in seconds (e.g., 3.0):"
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
                "2.3 Sliding window size as a percentage of the window size (0 for none, up to 0.95 for max):"
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

        # Ask for reject by annotation setting
        config["preprocessing"]["reject_by_annotation"] = questionary.select(
            "2.4 Reject epochs based on annotations (e.g., boundary events)?",
            choices=["Yes", "No"],
        ).ask()

        # Ask for epoch rejection settings
        print("\n📊 Epoch Rejection Settings")
        print("   This will reject individual epochs based on peak-to-peak amplitude thresholds.")
        print("   - Reject threshold: Maximum acceptable peak-to-peak amplitude per epoch")
        print("   - Flat threshold: Minimum acceptable peak-to-peak amplitude per epoch")
        print("   - Applied during epoch creation (more efficient than annotation)")
        print("   - Note: Values are entered in μV but automatically converted to V for MNE")
        
        # Enable/disable epoch rejection
        config["preprocessing"]["use_epoch_rejection"] = questionary.select(
            "2.5 Enable epoch rejection based on amplitude?",
            choices=["Yes", "No"],
        ).ask()

        if config["preprocessing"]["use_epoch_rejection"] == "Yes":
            # Ask for reject threshold (maximum acceptable peak-to-peak amplitude)
            while True:
                reject_input = questionary.text(
                    "2.5.1 Reject threshold (microvolts):\n   Maximum acceptable peak-to-peak amplitude per epoch.\n   Default is 800 (typical for EEG):"
                ).ask()
                try:
                    reject = float(reject_input)
                    if reject > 0:
                        break
                    else:
                        print("[ERROR] Please enter a positive number.")
                except (ValueError, TypeError):
                    print("[ERROR] Please enter a valid number.")
            
            # Ask for flat threshold (minimum acceptable peak-to-peak amplitude)
            while True:
                flat_input = questionary.text(
                    "2.5.2 Flat threshold (microvolts):\n   Minimum acceptable peak-to-peak amplitude per epoch.\n   Default is 0.1 (detects flat epochs):"
                ).ask()
                try:
                    flat = float(flat_input)
                    if flat >= 0:
                        break
                    else:
                        print("[ERROR] Please enter a non-negative number.")
                except (ValueError, TypeError):
                    print("[ERROR] Please enter a valid number.")
            
            config["preprocessing"]["epoch_rejection"] = {
                "reject": reject,
                "flat": flat,
            }
            
            print(f"✅ Epoch rejection enabled with {reject}μV reject, {flat}μV flat")
            print(f"   🔄 Will be converted to {reject*1e-6:.6f}V and {flat*1e-6:.6f}V for MNE processing")
        else:
            config["preprocessing"]["epoch_rejection"] = None
            print("ℹ️  Epoch rejection disabled")

        # # Ask for extreme datapoint removal settings
        # print("\n📊 Extreme Datapoint Removal Settings")
        # print("   This will remove extreme values (outliers) from the processed features.")
        # print("   - Percentile-based removal: Remove data points above/below specified percentiles")
        # print("   - Applied to processed features before transformation")
        
        # # Enable/disable extreme datapoint removal
        # config["preprocessing"]["remove_extreme_datapoints"] = questionary.select(
        #     "2.6 Enable extreme datapoint removal?",
        #     choices=["Yes", "No"],
        # ).ask()

        # if config["preprocessing"]["remove_extreme_datapoints"] == "Yes":
        #     # Ask for lower percentile threshold
        #     while True:
        #         lower_percentile_input = questionary.text(
        #             "2.6.1 Lower percentile threshold (decimal):\n   Data points below this percentile will be removed.\n   Default is 0.01 (1% - very conservative):"
        #         ).ask()
        #         try:
        #             lower_percentile = float(lower_percentile_input)
        #             if 0 <= lower_percentile <= 0.5:
        #                 break
        #             else:
        #                 print("[ERROR] Please enter a decimal between 0 and 0.5 (e.g., 0.01 for 1%).")
        #         except (ValueError, TypeError):
        #             print("[ERROR] Please enter a valid decimal number.")
        #     
        #     # Ask for upper percentile threshold
        #     while True:
        #         upper_percentile_input = questionary.text(
        #             "2.6.2 Upper percentile threshold (decimal):\n   Data points above this percentile will be removed.\n   Default is 0.99 (99% - very conservative):"
        #         ).ask()
        #         try:
        #             upper_percentile = float(upper_percentile_input)
        #             if 0.5 <= upper_percentile <= 1:
        #                 break
        #             else:
        #                 print("[ERROR] Please enter a decimal between 0.5 and 1 (e.g., 0.99 for 99%).")
        #         except (ValueError, TypeError):
        #             print("[ERROR] Please enter a valid decimal number.")
        #     
        #     # Validate that lower < upper
        #     if lower_percentile >= upper_percentile:
        #         print("[ERROR] Lower percentile must be less than upper percentile.")
        #         print(f"   Lower: {lower_percentile}, Upper: {upper_percentile}")
        #         print("   Using default values: Lower 0.01, Upper 0.99")
        #         lower_percentile = 0.01
        #         upper_percentile = 0.99
        #     
        #     config["preprocessing"]["extreme_datapoint_removal"] = {
        #         "lower_percentile": lower_percentile,
        #         "upper_percentile": upper_percentile,
        #         "method": "percentile"  # Can be extended to other methods later
        #     }
        #     
        #     print(f"✅ Extreme datapoint removal enabled: {lower_percentile} - {upper_percentile}")
        # else:
        #     config["preprocessing"]["extreme_datapoint_removal"] = None
        #     print("ℹ️  Extreme datapoint removal disabled")
        
        # Default to disabled since the section is commented out
        config["preprocessing"]["extreme_datapoint_removal"] = None
        print("ℹ️  Extreme datapoint removal section disabled (commented out in code)")

        # # Handle downsampling rate with validation
        # # https://mne.tools/stable/auto_tutorials/preprocessing/30_filtering_resampling.html
        # while True:
        #     downsampling_input = questionary.text(
        #         "2.7 Downsampling rate (Hz) or 'None': (not yet implemented)"
        #     ).ask()
        #     downsampling_rate = validate_downsampling_rate(downsampling_input)
        #     if downsampling_rate is not None or downsampling_input.lower() == "none":
        #         break
        # config["preprocessing"]["downsampling"] = downsampling_rate

        # 3. Feature Extraction
        print("\n[3] Feature Extraction")
        config["feature_extraction"] = {}
        config["feature_extraction"]["method"] = questionary.select(
            "3.1 Extraction method (welch is default and fastest, multitaper is slower but more precise):",
            choices=[
                "welch",
                "multitaper",
            ],
        ).ask()

        # config[ask]

        print(
            "3.2 Select features to compute:\n*My personal recomendation is to do only select per channel per band features in 3.2.4*"
        )
        print("\n📊 Computational Difficulty Guide:")
        print("band_power: 1/5 - Fastest, most commonly used")
        print("energy: 1/5 - Very fast")
        print("mean/std/variance: 1/5 - Standard statistics, optimized in numpy")
        print("rms: 1/5 - Simple calculation")
        print("\nModerate Complexity (Good Balance):")
        print("hjorth_mobility: 2/5 - Good feature, reasonable computation")
        print("spectral_entropy: 2/5 - Informative, moderate cost")
        print("\nComputationally Expensive (Use Sparingly):")
        print("hjorth_complexity: 3/5 - More complex but valuable")
        print("skewness: 4/5 - Very expensive, consider carefully")
        print("kurtosis: 4/5 - Very expensive, use only if needed")
        print("spectral_entropy: 4/5 - Most expensive, use only if needed")
        print()

        # Initialize the features dictionary
        config["feature_extraction"]["features"] = {}

        # Function to validate feature selections
        def validate_feature_selection(selected_features):
            if "none" in selected_features and len(selected_features) > 1:
                return (
                    False,
                    "❌ You cannot select 'none' along with other features. Please choose either 'none' or specific features, not both.",
                )
            return True, ""

        # Function to get feature selection with validation
        def get_feature_selection(
            prompt: str,
            psd_choices: List[str],
            time_domain_choices: List[str],
            config_key: str,
        ):
            print(f"\n📊 {prompt}")
            print(
                "   ┌─ This feature type supports both PSD (spectral) and Time Domain features"
            )

            # Ask for PSD features first
            psd_features = questionary.checkbox(
                f"   ├─ PSD Features (spectral):\n   │  💡 Tip: Select 'none' for no features, or select specific features (not both)",
                choices=psd_choices,
            ).ask()

            # Validate PSD features
            is_valid, error_message = validate_feature_selection(psd_features)
            if not is_valid:
                print(error_message)
                print("Please try again.\n")
                return get_feature_selection(
                    prompt, psd_choices, time_domain_choices, config_key
                )

            # Ask for time domain features
            time_domain_features = questionary.checkbox(
                f"   └─ Time Domain Features:\n      💡 Tip: Select 'none' for no features, or select specific features (not both)",
                choices=time_domain_choices,
            ).ask()

            # Validate time domain features
            is_valid, error_message = validate_feature_selection(time_domain_features)
            if not is_valid:
                print(error_message)
                print("Please try again.\n")
                return get_feature_selection(
                    prompt, psd_choices, time_domain_choices, config_key
                )

            # Combine and save features
            all_features = psd_features + time_domain_features
            # Remove duplicates if any
            all_features = list(set(all_features))
            config["feature_extraction"]["features"][config_key] = all_features

        # Define feature choices
        # My thinking is that if we do a band pass such as per channel per band , we can't do time domain features as how are we going to bandpass time domain features? right ! They have to be psd features
        psd_feature_choices = [  # for per channel_per_band
            "none",
            "band_power",
            "spectral_entropy",
        ]
        time_domain_feature_choices = (
            [  # for per channel_per_band and per_channel_across_bands
                "none",
                "energy",
                "mean",
                "std",
                "variance",
                "rms",
                "hjorth_mobility",
                "hjorth_complexity",
                "skewness",
                "kurtosis",
            ]
        )

        # Keep for the future, not used yet
        # Get feature selections using the reusable function
        # get_feature_selection(
        #     "3.2.1 Which features to compute (Average across all channels and bands)?",
        #     all_feature_choices,
        #     "avg_all_channels_all_bands"
        # )

        # Keep for the future, not used yet
        # get_feature_selection(
        #     "3.2.2 Which features to compute (Average across all channels per band)?",
        #     all_feature_choices,
        #     "avg_all_channels_per_band"
        # )
        print("3.2.1 and 3.2.2 are not created yet, but will be in the future")

        get_feature_selection(
            "3.2.3 Which features to compute (per channel across bands)?",
            psd_feature_choices,
            time_domain_feature_choices,
            "per_channel_across_bands",
        )

        # For per_channel_per_band, we only need PSD features (no time domain features)
        def get_psd_only_feature_selection(
            prompt: str, psd_choices: List[str], config_key: str
        ):
            print(f"\n📊 {prompt}")
            print("   └─ PSD Features only (spectral):")
            print(
                "      💡 Note: Time domain features not available for per-channel-per-band analysis"
            )

            while True:
                selected_features = questionary.checkbox(
                    f"      💡 Tip: Select 'none' for no features, or select specific features (not both)",
                    choices=psd_choices,
                ).ask()

                is_valid, error_message = validate_feature_selection(selected_features)
                if is_valid:
                    config["feature_extraction"]["features"][
                        config_key
                    ] = selected_features
                    break
                else:
                    print(error_message)
                    print("Please try again.\n")

        get_psd_only_feature_selection(
            "3.2.4 Which features to compute (per channel per band)? *recommended",
            psd_feature_choices,
            "per_channel_per_band",
        )

        # Ask for PSD normalization
        config["preprocessing"]["normalize_psd"] = questionary.select(
            "3.3 Normalize PSD values? (Highly recommended, is the default on almost all EEG software)",
            choices=["Yes", "No"],
        ).ask()

        # Ask for intermediate results display
        config["feature_extraction"]["show_intermediate_results"] = questionary.select(
            "3.4 Show intermediate results (DataFrame previews)? (Not recommended for large datasets)",
            choices=["No", "Yes"],
        ).ask()

        # Ask for intermediate counts display
        config["feature_extraction"]["show_intermediate_counts"] = questionary.select(
            "3.5 Show intermediate counts (row counts during processing)? (Not recommended for large datasets)",
            choices=["No", "Yes"],
        ).ask()

        # Automatically set output format based on experiment type
        if "ML" in config["project"]["experiment_type"]:
            config["feature_extraction"]["output_format"] = "ml"
            print(
                "   ✅ Auto-selected: ml format (one row per epoch, optimized for machine learning)"
            )
            print("      📊 Each row contains all features for one time window")
            print("      🤖 Perfect for training ML models")
        else:
            config["feature_extraction"]["output_format"] = "analysis"
            print(
                "   ✅ Auto-selected: analysis format (one row per channel-band, good for data analysis)"
            )
            print(
                "      📊 Each row contains one feature for one channel/band combination"
            )
            print("      🔍 Perfect for exploratory data analysis")

        # 4. Feature Transformation
        print("\n[4] Feature Transformation")
        config["feature_transformation"] = {}
        config["feature_transformation"]["transformations"] = questionary.select(
            "4.1 Select a transformation to apply (for more precise options edit the config file directly):",
            choices=[
                "Dummy (+1)",
                "PCA (retain 95% variance)",
                "PCA (manual count)",
                "SPCA (manual count)",
                "MinMax scaler",
                "Z-score standardization",
                "ICA",
                "ICA (manual count)",
                "Cohen test (manual count)",
                "Cohen test (limit to % for example 0.05)",
                "None",
            ],
        ).ask()

        config["feature_transformation"]["synthetic"] = questionary.select(
            "4.2 Synthetic data generation method:",
            choices=[
                # "SMOTE",
                # "Random over-sampling",
                # "Class weights only",
                "None"
            ],
        ).ask()

        # 5. Data Leakage Prevention (only if ML Classification and Feature Transformation are enabled)
        if target == "pyspark-only" or target == "full":
            if (
                config["project"]["experiment_type"] == "ML (Classification)"
                and config["feature_transformation"]["transformations"] != "None"
            ):
                print("\n[5] Data Leakage Prevention")
                print(
                    "⚠️  WARNING: You selected Classification with Feature Transformation."
                )
                print(
                    "   This can cause data leakage if test data influences training transforms."
                )

                config["data_leakage_prevention"] = {}

                # Question 1: Data leakage prevention strategy
                config["data_leakage_prevention"]["strategy"] = questionary.select(
                    "5.1 How would you like to handle data leakage during feature transformation?",
                    choices=[
                        # "Rotate test subjects and recompute transforms for each fold (slow, very storage heavy, most reliable ml results)",
                        "1 test/1 train split with transforms applied to training set only (faster, single split)",
                        "Transform all data together (no split - fastest, and potential data leakage)",
                    ],
                ).ask()

                # Question 2: Test subject definition (if rotation is selected)
                if (
                    "Rotate test subjects"
                    in config["data_leakage_prevention"]["strategy"]
                ):
                    config["data_leakage_prevention"]["test_subject_method"] = (
                        questionary.select(
                            "5.2.1 How would you like to define test subjects for rotation?",
                            choices=[
                                "Manually select X test subjects per fold and provide full paths",
                                "Automatically rotate all subjects (leave-X-out cross-validation)",
                            ],
                        ).ask()
                    )

                    if (
                        "Manually select"
                        in config["data_leakage_prevention"]["test_subject_method"]
                    ):
                        # Ask for number of test subjects per fold
                        while True:
                            test_subjects_count = questionary.text(
                                "5.2.2 Enter the number of test subjects per fold (e.g., 2):"
                            ).ask()
                            try:
                                count = int(test_subjects_count)
                                if count > 0:
                                    config["data_leakage_prevention"][
                                        "test_subjects_per_fold"
                                    ] = count
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
                                f"5.2.3.{fold_number} Enter comma-separated paths to test subjects for fold {fold_number} (or 'done')\n*Notice these paths should have been inputed in the correct group in [1] data inputs.\nAvailable groups: {groups_text}"
                            ).ask()
                            if fold_input.lower() == "done":
                                break
                            if not fold_input.strip():
                                print("[ERROR] Please enter valid paths or 'done'")
                                continue

                            # Validate paths
                            try:
                                fold_paths = [
                                    path.strip()
                                    for path in fold_input.split(",")
                                    if path.strip()
                                ]
                                valid_fold_paths = validate_eeg_paths(fold_paths)

                                # Check if paths exist in groups from part 1
                                found_paths, missing_paths = check_paths_in_groups(
                                    valid_fold_paths, config["data_input"]["groups"]
                                )

                                if missing_paths:
                                    print(
                                        f"⚠️  WARNING: The following paths were not found in part 1 groups: {', '.join(missing_paths)}"
                                    )
                                    action = questionary.select(
                                        "What would you like to do?",
                                        choices=[
                                            "Exit program (go back to [1] to add missing paths)",
                                            "Re-enter paths for this fold",
                                        ],
                                    ).ask()
                                    if (
                                        action
                                        == "Exit program (go back to [1] to add missing paths)"
                                    ):
                                        print(
                                            "Exiting config maker. Please run it again and add the missing paths in [1] Data Input."
                                        )
                                        exit(0)
                                    else:
                                        continue

                                # Check if number of subjects matches expected count
                                if (
                                    len(valid_fold_paths)
                                    != config["data_leakage_prevention"][
                                        "test_subjects_per_fold"
                                    ]
                                ):
                                    confirm = questionary.select(
                                        f"⚠️  You entered {len(valid_fold_paths)} subjects but expected {config['data_leakage_prevention']['test_subjects_per_fold']}. Continue anyway?",
                                        choices=["Yes, continue", "No, re-enter"],
                                    ).ask()
                                    if confirm == "No, re-enter":
                                        continue

                                config["data_leakage_prevention"]["fold_paths"][
                                    f"fold_{fold_number}"
                                ] = valid_fold_paths
                                fold_number += 1

                            except ValueError as e:
                                print(f"[ERROR] {e}")
                                continue

                    elif (
                        "Automatically rotate"
                        in config["data_leakage_prevention"]["test_subject_method"]
                    ):
                        # Ask for number of test subjects to leave out
                        while True:
                            leave_out_count = questionary.text(
                                "5.2.2 Enter the number of subjects to leave out per fold (e.g., 2):"
                            ).ask()
                            try:
                                count = int(leave_out_count)
                                if count > 0:
                                    config["data_leakage_prevention"][
                                        "leave_out_count"
                                    ] = count
                                    break
                                else:
                                    print("[ERROR] Please enter a positive number.")
                            except ValueError:
                                print("[ERROR] Please enter a valid integer.")

                # Question 2: Single train/test set definition (if single split is selected)
                elif (
                    "1 test/1 train split"
                    in config["data_leakage_prevention"]["strategy"]
                ):
                    config["data_leakage_prevention"]["single_split_method"] = (
                        questionary.select(
                            "5.2.1 How would you like to define this 1 training/testing set?",
                            choices=[
                                "Manually select test subjects and provide full paths",
                                "Automatically split subjects (e.g., 5 test subjects)",
                            ],
                        ).ask()
                    )

                    if (
                        "Manually select"
                        in config["data_leakage_prevention"]["single_split_method"]
                    ):
                        # Ask for number of test subjects
                        while True:
                            test_subjects_count = questionary.text(
                                "5.2.2 Enter the number of test subjects (e.g., 5):"
                            ).ask()
                            try:
                                count = int(test_subjects_count)
                                if count > 0:
                                    config["data_leakage_prevention"][
                                        "test_subjects_count"
                                    ] = count
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
                                f"5.2.3 Enter comma-separated paths to test subjects (expected {config['data_leakage_prevention']['test_subjects_count']} subjects)\n*Notice these paths should have been inputed in the correct group in [1] data inputs.\nAvailable groups: {groups_text}"
                            ).ask()
                            if not test_subjects_input.strip():
                                print("[ERROR] Please enter valid paths.")
                                continue

                            try:
                                test_paths = [
                                    path.strip()
                                    for path in test_subjects_input.split(",")
                                    if path.strip()
                                ]
                                valid_test_paths = validate_eeg_paths(test_paths)

                                # Check if paths exist in groups from part 1
                                found_paths, missing_paths = check_paths_in_groups(
                                    valid_test_paths, config["data_input"]["groups"]
                                )

                                if missing_paths:
                                    print(
                                        f"⚠️  WARNING: The following paths were not found in part 1 groups: {', '.join(missing_paths)}"
                                    )
                                    action = questionary.select(
                                        "What would you like to do?",
                                        choices=[
                                            "Exit program (go back to [1] to add missing paths)",
                                            "Re-enter paths for this test set",
                                        ],
                                    ).ask()
                                    if (
                                        action
                                        == "Exit program (go back to [1] to add missing paths)"
                                    ):
                                        print(
                                            "Exiting config maker. Please run it again and add the missing paths in [1] Data Input."
                                        )
                                        exit(0)
                                    else:
                                        continue

                                # Check if number of subjects matches expected count
                                if (
                                    len(valid_test_paths)
                                    != config["data_leakage_prevention"][
                                        "test_subjects_count"
                                    ]
                                ):
                                    confirm = questionary.select(
                                        f"⚠️  You entered {len(valid_test_paths)} subjects but expected {config['data_leakage_prevention']['test_subjects_count']}. Continue anyway?",
                                        choices=["Yes, continue", "No, re-enter"],
                                    ).ask()
                                    if confirm == "No, re-enter":
                                        continue

                                config["data_leakage_prevention"][
                                    "test_subjects_paths"
                                ] = valid_test_paths
                                break

                            except ValueError as e:
                                print(f"[ERROR] {e}")
                                continue

                    elif (
                        "Automatically split"
                        in config["data_leakage_prevention"]["single_split_method"]
                    ):
                        # Ask for number of test subjects
                        while True:
                            num_groups = len(config["data_input"]["groups"])
                            test_subjects_count = questionary.text(
                                f"5.2.2 Enter number of subjects for test set (e.g., 4) (recommended: at least {num_groups} for balanced group representation):"
                            ).ask()
                            try:
                                count = int(test_subjects_count)
                                if count > 0:
                                    config["data_leakage_prevention"][
                                        "test_subjects_count"
                                    ] = count
                                    break
                                else:
                                    print("[ERROR] Please enter a positive number.")
                            except ValueError:
                                print("[ERROR] Please enter a valid integer.")
                        
                        # Automatically select test subjects and add them to config for reproducibility
                        # This makes the split reproducible and explicit, avoiding the need for the Ray container
                        # to re-implement the same random selection logic
                        test_count = config["data_leakage_prevention"]["test_subjects_count"]
                        if test_count >= 1:
                            
                            # Check if we have enough test subjects for balanced group representation
                            num_groups = len(config["data_input"]["groups"])
                            if test_count < num_groups:
                                print(f"\n⚠️  WARNING: You selected {test_count} test subject(s) but have {num_groups} groups.")
                                print(f"   This means not all groups will have test subjects, which may bias your results.")
                                print(f"   Recommended: Select at least {num_groups} test subjects for balanced representation.")
                                
                                proceed = questionary.select(
                                    "Do you want to proceed anyway?",
                                    choices=["Yes, proceed with current selection", "No, let me change the count"]
                                ).ask()
                                
                                if proceed == "No, let me change the count":
                                    # Go back to asking for test count
                                    while True:
                                        new_test_count = questionary.text(
                                            f"5.2.2 Enter number of subjects for test set (recommended: at least {num_groups} for balanced groups):"
                                        ).ask()
                                        try:
                                            new_count = int(new_test_count)
                                            if new_count > 0:
                                                config["data_leakage_prevention"]["test_subjects_count"] = new_count
                                                test_count = new_count
                                                break
                                            else:
                                                print("[ERROR] Please enter a positive number.")
                                        except ValueError:
                                            print("[ERROR] Please enter a valid integer.")
                            
                            print(f"\n🎯 Automatically selecting {test_count} test subject(s) for reproducibility...")
                            
                            try:
                                # Use the dedicated function for automatic selection
                                selected_test_subjects, metadata = select_test_subjects_automatically(
                                    config["data_input"]["groups"], 
                                    test_count, 
                                    random_seed=42
                                )
                                
                                # Add the selected subjects to config as if they were manually selected
                                config["data_leakage_prevention"]["test_subjects_paths"] = selected_test_subjects
                                
                                # Display results
                                print(f"✅ Automatically selected test subjects: {', '.join(metadata['selected_subject_ids'])}")
                                print(f"   Paths: {', '.join(selected_test_subjects)}")
                                print(f"   Random seed: {metadata['random_seed']} (for reproducibility)")
                                
                                # Show group representation
                                if metadata['missing_groups']:
                                    print(f"   ⚠️  Groups represented: {', '.join(sorted(metadata['selected_groups']))}")
                                    print(f"   ⚠️  Groups missing: {', '.join(sorted(metadata['missing_groups']))}")
                                else:
                                    print(f"   ✅ All groups represented: {', '.join(sorted(metadata['selected_groups']))}")
                                
                                # Also add the random seed to config for transparency
                                config["data_leakage_prevention"]["random_seed"] = metadata['random_seed']
                                
                            except ValueError as e:
                                print(f"❌ ERROR: {e}")
                                exit(1)

                # Question 2: No split needed (if transform all data is selected)
                elif (
                    "Transform all data together"
                    in config["data_leakage_prevention"]["strategy"]
                ):
                    print("⚠️  WARNING: You selected to transform all data together.")
                    print(
                        "   This may cause data leakage as test data will influence training transforms."
                    )
                    print(
                        "   No additional configuration needed - all data will be transformed together."
                    )

    else:
        print(
            "\nSkipping [1] Data Input [2] Preprocessing [3] Feature Extraction [4] Feature Transformation, and [5] Data Leakage Prevention as we are not using PySpark"
        )

    # 6. Deployment Configuration
    print("\n[6] Deployment Configuration")
    config["project"]["deployment_method"] = questionary.select(
        "6.1 Deployment Method:",
        choices=["Docker", "Singularity with Slurm", "Singularity without Slurm"],
    ).ask()

    # 6.2 PySpark Resource Configuration
    if target == "pyspark" or target == "pyspark-only" or target == "full":
        print("\n[6.2] PySpark Resource Configuration")
        print("For example, for a 8-core CPU with 16GB memory, we can safely allocate:")
        print("  - 6 cores for the driver (master)")
        print("  - 6GB memory for the driver")
        print("  - 6GB memory for executors")
        print("  - 2 cores per executor")
        print("  - 8 shuffle partitions")
        print("This is the default and lightweight for testing.")

        edit_spark_config = questionary.select(
            "6.2.1 Do you want to edit the PySpark resource configuration?",
            choices=["Yes", "No (use defaults)"],
        ).ask()

        if edit_spark_config == "Yes":
            config["pyspark"] = {}
            config["pyspark"]["master"] = validate_integer_input(
                "6.2.2 Enter number of cores/threads to allocate (master):", default="6"
            )
            config["pyspark"]["driver_memory"] = validate_integer_input(
                "6.2.3 Enter driver memory in GB (e.g., 6):", default="6"
            )
            config["pyspark"]["executor_memory"] = validate_integer_input(
                "6.2.4 Enter executor memory in GB (e.g., 6):", default="6"
            )
            config["pyspark"]["executor_cores"] = validate_integer_input(
                "6.2.5 Enter executor cores/threads:", default="2"
            )
            config["pyspark"]["shuffle_partitions"] = validate_integer_input(
                "6.2.6 Enter shuffle partitions:", default="8"
            )
        else:
            # Use defaults
            config["pyspark"] = {
                "master": "6",
                "driver_memory": "6",
                "executor_memory": "6",
                "executor_cores": "2",
                "shuffle_partitions": "8",
            }

    # 6.3 SLURM Configuration (if Singularity with Slurm is selected)
    if config["project"]["deployment_method"] == "Singularity with Slurm":
        print("\n[6.3] SLURM Configuration")

        # Always ask for build options when using SLURM
        print("Recommended build options (10 minutes, 8GB RAM, 2 CPUs):")
        print("  --time=00:10:00 --mem=8G --cpus-per-task=2")
        build_slurm_options = questionary.text(
            "6.3.1 Enter SLURM options for building .sif containers:",
            default="--time=00:10:00 --mem=8G --cpus-per-task=2",
        ).ask()
        config["project"]["slurm_options_build"] = (
            sanitize_slurm_options(build_slurm_options) if build_slurm_options else ""
        )

        if target == "full":
            # Ask if user wants same or different SLURM options for PySpark and Ray
            slurm_choice = questionary.select(
                "6.3.2 SLURM options for PySpark and Ray:",
                choices=["Same options for both", "Different options for each"],
            ).ask()

            if slurm_choice == "Same options for both":
                slurm_options = questionary.text(
                    "6.3.3 Enter SLURM options for both PySpark and Ray:",
                    default="--time=24:00:00 --mem=16G --cpus-per-task=4",
                ).ask()
                config["project"]["slurm_options_pyspark"] = (
                    sanitize_slurm_options(slurm_options) if slurm_options else ""
                )
                config["project"]["slurm_options_ray"] = (
                    sanitize_slurm_options(slurm_options) if slurm_options else ""
                )
            else:  # Different options
                pyspark_slurm = questionary.text(
                    "6.3.3 Enter SLURM options for PySpark:",
                    default="--time=12:00:00 --mem=8G --cpus-per-task=2",
                ).ask()
                ray_slurm = questionary.text(
                    "6.3.4 Enter SLURM options for Ray:",
                    default="--time=24:00:00 --mem=16G --cpus-per-task=4",
                ).ask()
                config["project"]["slurm_options_pyspark"] = (
                    sanitize_slurm_options(pyspark_slurm) if pyspark_slurm else ""
                )
                config["project"]["slurm_options_ray"] = (
                    sanitize_slurm_options(ray_slurm) if ray_slurm else ""
                )

        elif target == "pyspark-only":
            slurm_options = questionary.text(
                "6.3.2 Enter SLURM options for PySpark:",
                default="--time=12:00:00 --mem=8G --cpus-per-task=2",
            ).ask()
            config["project"]["slurm_options_pyspark"] = (
                sanitize_slurm_options(slurm_options) if slurm_options else ""
            )

        elif target == "ray-only":
            slurm_options = questionary.text(
                "6.3.2 Enter SLURM options for Ray:",
                default="--time=24:00:00 --mem=16G --cpus-per-task=4",
            ).ask()
            config["project"]["slurm_options_ray"] = (
                sanitize_slurm_options(slurm_options) if slurm_options else ""
            )

    # 7. Ray Configuration (only if target is ray-only or full AND experiment type is ML)
    if (target == "ray-only" or target == "full") and config["project"][
        "experiment_type"
    ] in ["ML (Classification)", "ML (Clustering)"]:
        print("\n[7] Ray Configuration")
        config["ray"] = {}

        # TODO: make it such that we can choose distributed or sklearn (where distributed is ray and pyspark with raydp)
        # Machine Learning Models Selection
        config["ray"]["models"] = questionary.checkbox(
            "7.1 Select machine learning models to test:",
            choices=[
                "Random Forest",
                "XGBoost",
                "MLP (Neural Network)",
                "KNN",
                "SVM",
                "Linear Regression",
                "Logistic Regression",
                "Decision Tree",
                "Gradient Boosting",
                "AdaBoost",
            ],
        ).ask()

        config["ray"]["num_trials"] = validate_integer_input(
            "7.2 Enter number of trials for hyperparameter optimization:", default="10"
        )

        config["ray"]["max_concurrent"] = validate_integer_input(
            "7.3 Enter maximum concurrent trials:", default="2"
        )

        config["ray"]["metric"] = questionary.select(
            "7.4 Select optimization metric:",
            choices=[
                "accuracy",
                "f1",
                "precision",
                "recall",
                "auc",
                "mse",
                "mae",
                "r2",
            ],
        ).ask()

        config["ray"]["mode"] = questionary.select(
            "7.5 Select optimization mode:", choices=["max", "min"]
        ).ask()

        config["ray"]["cv_folds"] = validate_integer_input(
            "7.6 Enter number of cross-validation folds:", default="5"
        )

        config["ray"]["random_state"] = validate_integer_input(
            "7.7 Enter random state for reproducibility:", default="42"
        )
    else:
        # Skip Ray configuration for Analysis mode
        if target == "ray-only" or target == "full":
            print("\n[7] Ray Configuration - SKIPPED")
            print(
                "   ℹ️  Ray ML configuration skipped because you selected 'Analysis (No Ray ML)'"
            )
            print("   📊 Your data will be processed and saved for manual analysis")
            print("   🔧 You can run your own ML analysis on the processed data")
            print(
                "   📁 Output: Parquet files ready for pandas, R, or other analysis tools"
            )

    # Configuration summary
    print("\n" + "=" * 60)
    print("📋 CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"🎯 Experiment Type: {config['project']['experiment_type']}")
    print(
        f"📊 Output Format: {config.get('feature_extraction', {}).get('output_format', 'N/A')}"
    )
    print(f"🔧 Deployment: {config['project']['deployment_method']}")

    if "ML" in config["project"]["experiment_type"]:
        print(f"🤖 ML Pipeline: PySpark + Ray (automated)")
    else:
        print(f"📈 Analysis Pipeline: PySpark only (manual ML)")

    # Show test subject selection info if applicable
    if (config.get("data_leakage_prevention", {}).get("test_subjects_paths")):
        test_subject_paths = config["data_leakage_prevention"]["test_subjects_paths"]
        test_count = len(test_subject_paths)
        
        # Extract subject IDs from paths
        selected_subject_ids = []
        for test_subject_path in test_subject_paths:
            path_parts = test_subject_path.split('/')
            filename = path_parts[-1]
            subject_id = filename.replace('_task-eyesclosed_eeg.set', '').replace('_eeg.set', '').replace('.set', '').replace('.fif', '')
            selected_subject_ids.append(subject_id)
        
        if test_count == 1:
            print(f"🎯 Test Subject: {selected_subject_ids[0]} (automatically selected)")
            print(f"   📍 Path: {test_subject_paths[0]}")
        else:
            print(f"🎯 Test Subjects: {', '.join(selected_subject_ids)} (automatically selected)")
            print(f"   📍 Count: {test_count} subjects")
            for i, (subject_id, path) in enumerate(zip(selected_subject_ids, test_subject_paths), 1):
                print(f"      {i}. {subject_id}: {path}")

    print("=" * 60)

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
    return " ".join(options.split())


def validate_eeg_paths(paths: List[str]) -> List[str]:
    """Validate EEG file paths - check they exist and don't contain spaces."""
    valid_paths = []
    for path in paths:
        path = path.strip()
        if not path:
            continue

        # Check for spaces in path
        if " " in path:
            raise ValueError(
                f"Path contains spaces: '{path}'. Please use paths without spaces."
            )

        # Check if file exists
        if not Path(path).exists():
            raise ValueError(f"File does not exist: '{path}'")

        # Check if it's a valid EEG file (optional - basic check)
        if not (path.endswith(".set") or path.endswith(".fif")):
            print(f"⚠️ Warning: '{path}' doesn't end with .set or .fif")

        valid_paths.append(path)

    return valid_paths


def check_paths_in_groups(
    paths: List[str], groups: Dict[str, List[str]]
) -> Tuple[List[str], List[str]]:
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


def select_test_subjects_automatically(
    groups: Dict[str, List[str]], 
    test_count: int, 
    random_seed: int = 42
) -> Tuple[List[str], Dict[str, Any]]:
    """
    Automatically select test subjects with balanced group representation when possible.
    
    Args:
        groups: Dictionary of group names to subject paths
        test_count: Number of test subjects to select
        random_seed: Random seed for reproducibility (default: 42)
        
    Returns:
        Tuple of (selected_subject_paths, metadata_dict)
    """
    num_groups = len(groups)
    
    # Collect all available subjects from groups
    all_subject_paths = []
    for group_name, paths in groups.items():
        all_subject_paths.extend(paths)
    
    if not all_subject_paths:
        raise ValueError("No subjects found in groups. Please check your data input configuration.")
    
    if test_count > len(all_subject_paths):
        raise ValueError(f"Requested {test_count} test subjects but only {len(all_subject_paths)} subjects available.")
    
    # Use fixed seed for reproducibility
    random.seed(random_seed)
    
    # Select test subjects with balanced group representation when possible
    if test_count >= num_groups:
        # Try to select at least one subject from each group
        selected_test_subjects = []
        remaining_subjects = all_subject_paths.copy()
        
        # First, select one subject from each group
        for group_name, group_paths in groups.items():
            if remaining_subjects and any(path in remaining_subjects for path in group_paths):
                # Find subjects from this group that are still available
                available_from_group = [path for path in group_paths if path in remaining_subjects]
                if available_from_group:
                    selected = random.choice(available_from_group)
                    selected_test_subjects.append(selected)
                    remaining_subjects.remove(selected)
        
        # Fill remaining slots with random selection from all remaining subjects
        remaining_needed = test_count - len(selected_test_subjects)
        if remaining_needed > 0 and remaining_subjects:
            additional_subjects = random.sample(remaining_subjects, min(remaining_needed, len(remaining_subjects)))
            selected_test_subjects.extend(additional_subjects)
        
        # If we still don't have enough, add more from any available subjects
        if len(selected_test_subjects) < test_count:
            all_available = [path for path in all_subject_paths if path not in selected_test_subjects]
            if all_available:
                additional_needed = test_count - len(selected_test_subjects)
                additional = random.sample(all_available, min(additional_needed, len(all_available)))
                selected_test_subjects.extend(additional)
    else:
        # Simple random selection when we can't guarantee balance
        selected_test_subjects = random.sample(all_subject_paths, test_count)
    
    # Extract subject IDs from paths for display
    selected_subject_ids = []
    for subject_path in selected_test_subjects:
        path_parts = subject_path.split('/')
        filename = path_parts[-1]
        # Remove common EEG file extensions and task suffixes
        subject_id = filename.replace('_task-eyesclosed_eeg.set', '').replace('_eeg.set', '').replace('.set', '').replace('.fif', '')
        selected_subject_ids.append(subject_id)
    
    # Show group representation
    selected_groups = set()
    for subject_path in selected_test_subjects:
        for group_name, group_paths in groups.items():
            if subject_path in group_paths:
                selected_groups.add(group_name)
                break
    
    all_groups = set(groups.keys())
    missing_groups = all_groups - selected_groups
    
    # Create metadata
    metadata = {
        "selected_subject_paths": selected_test_subjects,
        "selected_subject_ids": selected_subject_ids,
        "selected_groups": list(selected_groups),
        "missing_groups": list(missing_groups),
        "all_groups_represented": len(missing_groups) == 0,
        "random_seed": random_seed,
        "test_count": test_count,
        "num_groups": num_groups
    }
    
    return selected_test_subjects, metadata


if __name__ == "__main__":
    target: str = infer_target()
    print(f"Generating config for target: {target}")
    config, config_name = build_config(target=target)
    save_config(config, config_name)
