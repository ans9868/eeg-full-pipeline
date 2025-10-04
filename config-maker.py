import random
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import questionary
import yaml


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


def get_target_with_ray_option() -> str:
    """Get target with option to include Ray configuration for ML experiments."""
    base_target = infer_target()

    # If we're in eeg-pyspark-pipeline and user wants ML, offer Ray option
    if base_target == "pyspark-only":
        print("\n🎯 Target Configuration")
        print("   You're running from eeg-pyspark-pipeline (PySpark processing)")
        print("   For ML experiments, you can optionally include Ray configuration")

        include_ray = questionary.select(
            "Do you want to include Ray ML configuration?",
            choices=[
                "No - PySpark only (data processing)",
                "Yes - Include Ray ML (data processing + ML)",
            ],
        ).ask()

        if "Yes" in include_ray:
            return "full"  # This will include both PySpark and Ray
        else:
            return "pyspark-only"

    return base_target


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


def metadataPart0() -> Tuple[Dict[str, Any], str]:
    """
    Section 0: Project Metadata
    Returns: Tuple of (project_config_dict, config_filename)
    """
    print("\n[0] Project Metadata")
    config = {}
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
            "ML Fingerprinting - Predict EEG subject ID's from EEG data (only intra subject splits are supported)",
            "ML Classification - Predict categories (e.g., patient vs control, disease stages)",
            "ML Clustering - Find patterns/groups in data with labels",
            "Analysis (No Ray ML) - Process data for manual analysis, no automated ML",
        ],
    ).ask()

    # Extract simplified experiment type from the choice
    if experiment_type_choice and "ML Classification" in experiment_type_choice:
        config["project"]["experiment_type"] = "ML Classification"
    elif "ML Clustering" in experiment_type_choice:
        config["project"]["experiment_type"] = "ML Clustering"
    elif "ML Fingerprinting" in experiment_type_choice:
        config["project"]["experiment_type"] = "ML Fingerprinting"
    elif "Analysis (No Ray ML)" in experiment_type_choice:
        config["project"]["experiment_type"] = "Analysis (No Ray ML)"
    else:
        config["project"]["experiment_type"] = "ML Classification"  # Default fallback

    config["project"]["subjects_or_events"] = questionary.select(
        "0.4 Are we analyzing subjects or events: (events are not currently supported)",
        choices=["subjects", "events"],
    ).ask()

    # if select events raise error_message
    if config["project"]["subjects_or_events"] == "events":
        raise ValueError(
            "Unfortunatly support for events has not been created yet."
        )

    # 0.4.1 Event selection (only if analyzing events) (currently not supported)
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

    # # 0.4.2 Artifact removal method (fundamental metadata)
    # config["project"]["artifact_removal"] = questionary.select(
    #     "0.4.2 Artifact removal method (defines how data was processed):",
    #     choices=[
    #         # "ICA",
    #         "None",
    #     ],  # costum list of events to remove
    # ).ask()

    # 0.5 Deployment method (fundamental project metadata)
    config["project"]["deployment_method"] = questionary.select(
        "0.5 Deployment Method:",
        choices=["Docker", "Singularity with Slurm", "Singularity without Slurm"],
    ).ask()

    # 0.6 Global random seed (used throughout the pipeline for reproducibility)
    while True:
        random_seed_input = questionary.text(
            "0.6 Enter global random seed for reproducibility (used for data splitting, ML training, etc.):",
            default="42"
        ).ask()
        try:
            random_seed = int(random_seed_input)
            config["project"]["random_seed"] = random_seed
            print(f"   ✅ Global random seed: {random_seed}")
            break
        except ValueError:
            print("[ERROR] Please enter a valid integer.")

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

    return config, config_name


def dataInputPart1() -> Dict[str, Any]:
    """
    Section 1: Data Input
    Returns: Dictionary containing data_input configuration
    """
    print("\n[1] Data Input")
    config = {}
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
                    [path.strip() for path in group_input.split(",") if path.strip()]
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

    return config


def preprocessingPart2() -> Dict[str, Any]:
    """
    Section 2: Preprocessing
    Returns: Dictionary containing preprocessing configuration
    """
    print("\n[2] Preprocessing")
    config = {}
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

    # TODO: Better division between preprocessing and feature extraction needed
    # Currently normalize_psd is in preprocessing for pipeline compatibility,
    # but logically it belongs to feature extraction. Need to refactor this properly.
    # Ask for PSD normalization (stored in preprocessing for pipeline compatibility)
    config["preprocessing"]["normalize_psd"] = questionary.select(
        "2.5 Normalize PSD values? (Highly recommended, is the default on almost all EEG software)",
        choices=["Yes", "No"],
    ).ask()

    # Ask for epoch rejection settings
    print("\n📊 Epoch Rejection Settings")
    print(
        "   This will reject individual epochs based on peak-to-peak amplitude thresholds."
    )
    print("   - Reject threshold: Maximum acceptable peak-to-peak amplitude per epoch")
    print("   - Flat threshold: Minimum acceptable peak-to-peak amplitude per epoch")
    print("   - Applied during epoch creation (more efficient than annotation)")
    print(
        "   - Note: Values are entered in μV but automatically converted to V for MNE"
    )

    # Enable/disable epoch rejection
    config["preprocessing"]["use_epoch_rejection"] = questionary.select(
        "2.6 Enable epoch rejection based on amplitude?",
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
        # print(f"   🔄 Will be converted to {reject*1e-6:.6f}V and {flat*1e-6:.6f}V for MNE processing")
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

    return config


def featureCreationPart3(experiment_type: str) -> Dict[str, Any]:
    """
    Section 3: Feature Extraction
    Args:
        experiment_type: The experiment type from project metadata
    Returns: Dictionary containing feature_extraction configuration
    """
    print("\n[3] Feature Extraction")
    config = {}
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
    print(
        "   ⚠️  WARNING!!!: spectral_entropy may produce NA values, especially for per_channel_across_bands"
    )
    print("\nComputationally Expensive (Use Sparingly):")
    print("hjorth_complexity: 3/5 - More complex but valuable")
    print("skewness: 4/5 - Very expensive, consider carefully")
    print("kurtosis: 4/5 - Very expensive, use only if needed")
    print("spectral_entropy: 4/5 - Most expensive, use only if needed")
    print(
        "   ⚠️  WARNING!!!: spectral_entropy may produce NA values, especially for per_channel_across_bands"
    )
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
            f"   ├─ PSD Features (spectral):\n  ",
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
                config["feature_extraction"]["features"][config_key] = selected_features
                break
            else:
                print(error_message)
                print("Please try again.\n")

    get_psd_only_feature_selection(
        "3.2.4 Which features to compute (per channel per band)? *recommended",
        psd_feature_choices,
        "per_channel_per_band",
    )

    # Ask for intermediate results display
    config["feature_extraction"]["show_intermediate_results"] = questionary.select(
        "3.3 Show intermediate results (DataFrame previews)? (Not recommended for large datasets)",
        choices=["No", "Yes"],
    ).ask()

    # Ask for intermediate counts display
    config["feature_extraction"]["show_intermediate_counts"] = questionary.select(
        "3.4 Show intermediate counts (row counts during processing)? (Not recommended for large datasets)",
        choices=["No", "Yes"],
    ).ask()

    # Automatically set output format based on experiment type
    if "ML" in experiment_type:
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
        print("      📊 Each row contains one feature for one channel/band combination")
        print("      🔍 Perfect for exploratory data analysis")

    return config


def featureTransformationsPart4() -> Dict[str, Any]:
    """
    Section 4: Feature Transformation
    Returns: Dictionary containing feature_transformation configuration
    """
    print("\n[4] Feature Transformation")
    print("📊 Available Transformers:")
    print("   • Dummy (+1): Simple test transformer (adds +1 to all features)")
    print("   • PCA: Dimensionality reduction (retain variance or manual count)")
    print("   • SVD: Singular Value Decomposition for dimensionality reduction")
    print("   • MinMax scaler: Scale features to [0,1] or [-1,1] range")
    print("   • Z-score/Standard scaler: Standardize features (mean=0, std=1)")
    print("   • Robust scaler: Scale using median and IQR (outlier-resistant)")
    print("   • Normalizer: Lp normalization (L1, L2, L∞) for unit norm vectors")
    print("   • Log transform (log1p): Apply log(1+x) transformation")
    # print("   • Polynomial expansion: Polynomial expansion (coming soon)")
    # print("   • Cohen test: Statistical feature selection")
    print()

    config = {}
    config["feature_transformation"] = {}

    # Define available transformations
    available_transformations = [
        "Dummy (+1)",
        "PCA (retain 95% variance)",
        "PCA (manual count)",
        "SVD (k components)",
        "MinMax scaler",
        "Z-score standardization",
        "Standard scaler",
        "Robust scaler",
        "Normalizer",
        "Log transform (log1p)",
        # "Polynomial expansion", # coming soon
        # "Cohen test (manual count)", # not implemented (can be done with logistic regression)
        # "Cohen test (limit to % for example 0.05)", # not implemented (can be done with logistic regression)
        # "SPCA (manual count)", # not in spark
        # "ICA", # not in spark
        # "ICA (manual count)", # not in spark
    ]

    # Initialize transformations list
    selected_transformations = []

    print(
        "4.1 Select transformations to apply (one by one, select 'done' when finished):"
    )
    print("   Transformations will be applied in the order you select them")
    print()

    while True:
        # Show current selections
        if selected_transformations:
            print(f"   Current selections: {', '.join(selected_transformations)}")
            print()

        # Create choices list with all transformations plus 'done' (allow duplicates)
        choices = available_transformations + ["done"]

        # Ask for next transformation
        next_transformation = questionary.select(
            f"4.1.{len(selected_transformations) + 1} Select next transformation (or 'done' to finish):",
            choices=choices,
        ).ask()

        if next_transformation == "done":
            break

        selected_transformations.append(next_transformation)
        print(f"   ✅ Added: {next_transformation}")
        print()

    # Set transformations (empty list becomes ["None"])
    if not selected_transformations:
        config["feature_transformation"]["transformations"] = ["None"]
    else:
        config["feature_transformation"]["transformations"] = selected_transformations

    config["feature_transformation"]["synthetic"] = questionary.select(
        "4.2 Synthetic data generation method:",
        choices=[
            # "SMOTE",
            # "Random over-sampling",
            # "Class weights only",
            "None"
        ],
    ).ask()

    # 4.3 Transformer-specific configuration
    if config["feature_transformation"]["transformations"] != ["None"]:
        print("\n📊 Transformer Configuration")
        print(
            f"   Selected transformations: {', '.join(config['feature_transformation']['transformations'])}"
        )
        print("   Transformations will be applied in the order selected above")
        print()

        # PCA configuration
        if "PCA (manual count)" in config["feature_transformation"]["transformations"]:
            while True:
                pca_components = questionary.text(
                    "4.3.1 Enter number of PCA components (e.g., 10):"
                ).ask()
                try:
                    count = int(pca_components)
                    if count > 0:
                        config["feature_transformation"]["pca_components"] = count
                        break
                    else:
                        print("[ERROR] Please enter a positive number.")
                except ValueError:
                    print("[ERROR] Please enter a valid integer.")

        # SVD configuration
        if "SVD (k components)" in config["feature_transformation"]["transformations"]:
            while True:
                svd_components = questionary.text(
                    "4.3.2 Enter number of SVD components (e.g., 10):"
                ).ask()
                try:
                    count = int(svd_components)
                    if count > 0:
                        config["feature_transformation"]["svd_components"] = count
                        break
                    else:
                        print("[ERROR] Please enter a positive number.")
                except ValueError:
                    print("[ERROR] Please enter a valid integer.")

        # MinMax scaler configuration
        if "MinMax scaler" in config["feature_transformation"]["transformations"]:
            minmax_range = questionary.select(
                "4.3.3 MinMax scaler range:", choices=["[0, 1]", "[-1, 1]"]
            ).ask()
            if minmax_range == "[0, 1]":
                config["feature_transformation"]["minmax_range"] = [0.0, 1.0]
            else:
                config["feature_transformation"]["minmax_range"] = [-1.0, 1.0]

        # Robust scaler configuration
        if "Robust scaler" in config["feature_transformation"]["transformations"]:
            robust_centering = questionary.select(
                "4.3.4 Robust scaler centering:",
                choices=["Yes (center with median)", "No (no centering)"],
            ).ask()
            config["feature_transformation"]["robust_scaler_with_centering"] = (
                robust_centering == "Yes (center with median)"
            )

            robust_scaling = questionary.select(
                "4.3.5 Robust scaler scaling:",
                choices=["Yes (scale with IQR)", "No (no scaling)"],
            ).ask()
            config["feature_transformation"]["robust_scaler_with_scaling"] = (
                robust_scaling == "Yes (scale with IQR)"
            )

        # Normalizer configuration
        if "Normalizer" in config["feature_transformation"]["transformations"]:
            p_norm = questionary.select(
                "4.3.6 Normalizer p-norm:",
                choices=[
                    "L1 (Manhattan norm)",
                    "L2 (Euclidean norm)",
                    "L∞ (Maximum norm)",
                ],
            ).ask()
            if p_norm == "L1 (Manhattan norm)":
                config["feature_transformation"]["normalizer_p"] = 1.0
            elif p_norm == "L2 (Euclidean norm)":
                config["feature_transformation"]["normalizer_p"] = 2.0
            else:  # L∞
                config["feature_transformation"]["normalizer_p"] = float("inf")

        # Cohen test configuration
        if "Cohen test" in config["feature_transformation"]["transformations"]:
            if "manual count" in config["feature_transformation"]["transformations"]:
                while True:
                    cohen_components = questionary.text(
                        "4.3.7 Enter number of Cohen test components (e.g., 10):"
                    ).ask()
                    try:
                        count = int(cohen_components)
                        if count > 0:
                            config["feature_transformation"]["cohen_components"] = count
                            break
                        else:
                            print("[ERROR] Please enter a positive number.")
                    except ValueError:
                        print("[ERROR] Please enter a valid integer.")
            elif "limit to %" in config["feature_transformation"]["transformations"]:
                while True:
                    cohen_limit = questionary.text(
                        "4.3.8 Enter Cohen test limit percentage (e.g., 0.05 for 5%):"
                    ).ask()
                    try:
                        limit = float(cohen_limit)
                        if 0 < limit < 1:
                            config["feature_transformation"]["cohen_limit"] = limit
                            break
                        else:
                            print("[ERROR] Please enter a value between 0 and 1.")
                    except ValueError:
                        print("[ERROR] Please enter a valid decimal number.")

    return config


def dataLeakagePreventionPart5(
    experiment_type: str,
    feature_transformations: List[str],
    data_input_groups: Dict[str, List[str]],
    project_config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Section 5: Data Leakage Prevention
    Args:
        experiment_type: The experiment type from project metadata
        feature_transformations: List of selected feature transformations
        data_input_groups: Dictionary of data input groups
        project_config: Dictionary containing project configuration (including random_seed)
    Returns: Dictionary containing data_leakage_prevention configuration
    """
    print("\n[5] Data Leakage Prevention")
    print(f"⚠️  WARNING: You selected {experiment_type} with Feature Transformation.")
    print("   This can cause data leakage if test data influences training transforms.")

    config = {}
    config["data_leakage_prevention"] = {}

    # Question 1: Data leakage prevention strategy
    # For ML Fingerprinting, only allow intra-subject splits (same subjects in train/test)
    if experiment_type == "ML Fingerprinting":
        print("ML Fingerprinting detected - only intra-subject splits are allowed")
        print("   This is because fingerprinting predicts subject IDs, requiring same subjects in train/test")
        
        data_leakage_prevention_choice = questionary.select(
            "5.1 How would you like to handle data leakage during feature transformation?",
            choices=[
                "Transform all data together (intra subject) (no split - fastest, and potential data leakage)",
                "Within-subject (intra subject) train/test split (example: 80/20 per subject) - each subject contributes to both train and test",
            ],
        ).ask()
    else:
        data_leakage_prevention_choice = questionary.select(
        "5.1 How would you like to handle data leakage during feature transformation?",
        choices=[
            "Transform all data together (intra subject) (no split - fastest, and potential data leakage)",
            "Within-subject (intra subject) train/test split (example: 80/20 per subject) - each subject contributes to both train and test",
            "1 test/1 train split (inter subject) with transforms applied to training set only (faster, single split)",
            "LPSO (Leave-P-Subjects-Out) (inter subject) - systematic cross-validation (recommended for small datasets)",
        ],
    ).ask()
    
    
    # Map the choice to the full strategy string expected by config_handler.py
    data_leakage_prevention_mapping = {
        "Transform all data together (intra subject) (no split - fastest, and potential data leakage)": "Transform all data together (intra subject split) (no split - fastest, and potential data leakage)",
        "Within-subject (intra subject) train/test split (example: 80/20 per subject) - each subject contributes to both train and test": "Within-subject (intra subject split) train/test split (80/20 per subject) - each subject contributes to both train and test",
        "1 test/1 train split (inter subject) with transforms applied to training set only (faster, single split)": "1 test/1 train split (inter subject split) with transforms applied to training set only (faster, single split)",
        "LPSO (Leave-P-Subjects-Out) (inter subject) - systematic cross-validation (recommended for small datasets)": "LPSO (Leave-P-Subjects-Out) (inter subject split) - systematic cross-validation (recommended for small datasets)"
    }
    
    config["data_leakage_prevention"]["strategy"] = data_leakage_prevention_mapping[data_leakage_prevention_choice]

    # Question 2: Test subject definition (if rotation is selected)
    if "Rotate test subjects" in config["data_leakage_prevention"]["strategy"]:
        config["data_leakage_prevention"]["test_subject_method"] = questionary.select(
            "5.2.1 How would you like to define test subjects for rotation?",
            choices=[
                "Manually select X test subjects per fold and provide full paths",
                "Automatically rotate all subjects (leave-X-out cross-validation)",
            ],
        ).ask()

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
            available_groups = list(data_input_groups.keys())
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
                        path.strip() for path in fold_input.split(",") if path.strip()
                    ]
                    valid_fold_paths = validate_eeg_paths(fold_paths)

                    # Check if paths exist in groups from part 1
                    found_paths, missing_paths = check_paths_in_groups(
                        valid_fold_paths, data_input_groups
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
                        != config["data_leakage_prevention"]["test_subjects_per_fold"]
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
                        config["data_leakage_prevention"]["leave_out_count"] = count
                        break
                    else:
                        print("[ERROR] Please enter a positive number.")
                except ValueError:
                    print("[ERROR] Please enter a valid integer.")

    # Question 2: LPSO configuration (if LPSO is selected)
    elif (
        "LPSO (Leave-P-Subjects-Out)" in config["data_leakage_prevention"]["strategy"]
    ):
        print("\n📊 LPSO (Leave-P-Subjects-Out) Configuration")
        print("   This will systematically leave out subjects for cross-validation.")
        print("   Each subject will be used as test data exactly once.")

        # Calculate total subjects and show group distribution
        total_subjects = sum(len(paths) for paths in data_input_groups.values())
        print(f"   📈 Total subjects: {total_subjects}")
        for group_name, paths in data_input_groups.items():
            print(f"      {group_name}: {len(paths)} subjects")

        # Ask for default or custom number of subjects per group
        num_groups = len(data_input_groups)
        default_subjects = num_groups  # Default is 1 subject per group per fold

        lpso_choice = questionary.select(
            "5.2.1 LPSO configuration:",
            choices=[
                f"Default ({default_subjects} subjects - 1 per group per fold)",
                f"Custom number of subjects",
                "Leave-One-Subject-Out (Individual) - each subject as test",
            ],
        ).ask()

        if "Default" in lpso_choice:
            # Use default (1 subject per group per fold)
            count = default_subjects
            subjects_per_group_per_fold = 1
            print(
                f"   ✅ Using default: {count} subjects ({subjects_per_group_per_fold} per group per fold)"
            )

            # Calculate how many folds can be generated
            min_subjects_per_group = min(
                len(paths) for paths in data_input_groups.values()
            )
            max_folds = min_subjects_per_group // subjects_per_group_per_fold
            print(f"   📈 You can generate {max_folds} folds with this configuration")

            # Validate that each group has enough subjects
            insufficient_groups = []
            for group_name, paths in data_input_groups.items():
                if len(paths) < subjects_per_group_per_fold:
                    insufficient_groups.append(f"{group_name} ({len(paths)} subjects)")

            if insufficient_groups:
                print(
                    f"❌ ERROR: The following groups don't have enough subjects for default LPSO:"
                )
                for group in insufficient_groups:
                    print(f"   {group}")
                print(f"   Each group needs at least 1 subject for default LPSO.")
                raise ValueError("Insufficient subjects for default LPSO")

            config["data_leakage_prevention"]["lpso_subjects_per_group"] = count

        elif "Leave-P-Subjects-Out (Individual)" in lpso_choice:
            # Individual LPSO - each subject gets its own test fold
            print(f"   ✅ Using Individual LPSO: each subject as test")

            # Collect all subjects from all groups
            all_subjects = []
            for group_name, paths in data_input_groups.items():
                for path in paths:
                    all_subjects.append(path)

            total_subjects = len(all_subjects)
            print(f"   📊 Total subjects: {total_subjects}")
            print(f"   📈 You can generate {total_subjects} folds (one per subject)")

            # Set up for individual SO
            count = total_subjects  # Each subject gets its own fold
            subjects_per_group_per_fold = 1  # Each fold has exactly 1 subject

            config["data_leakage_prevention"]["lpso_subjects_per_group"] = count
            config["data_leakage_prevention"]["individual_lpso"] = True

        else:
            # Ask for custom number of subjects per group
            while True:
                subjects_per_group = questionary.text(
                    f"5.2.2 Enter custom number of subjects to leave out per group (e.g., {num_groups*2} for 2 per group, {num_groups*3} for 3 per group):"
                ).ask()
                try:
                    count = int(subjects_per_group)
                    if count > 0:
                        # Validate that count is evenly divisible by number of groups
                        if count % num_groups != 0:
                            print(
                                f"❌ ERROR: {count} is not evenly divisible by {num_groups} groups"
                            )
                            print(
                                f"   Valid options: {num_groups}, {num_groups*2}, {num_groups*3}, etc."
                            )
                            continue

                        # Calculate subjects per group per fold
                        subjects_per_group_per_fold = count // num_groups
                        print(
                            f"   📊 This will leave out {subjects_per_group_per_fold} subjects per group per fold"
                        )

                        # Calculate how many folds can be generated
                        min_subjects_per_group = min(
                            len(paths) for paths in data_input_groups.values()
                        )
                        max_folds = (
                            min_subjects_per_group // subjects_per_group_per_fold
                        )
                        print(
                            f"   📈 You can generate {max_folds} folds with this configuration"
                        )

                        # Validate that each group has enough subjects
                        insufficient_groups = []
                        for group_name, paths in data_input_groups.items():
                            if len(paths) < subjects_per_group_per_fold:
                                insufficient_groups.append(
                                    f"{group_name} ({len(paths)} subjects)"
                                )

                        if insufficient_groups:
                            print(
                                f"❌ ERROR: The following groups don't have enough subjects:"
                            )
                            for group in insufficient_groups:
                                print(f"   {group}")
                            print(
                                f"   Each group needs at least {subjects_per_group_per_fold} subjects per fold for this configuration."
                            )
                            print(
                                f"   With {subjects_per_group_per_fold} subjects per fold, you can generate {min(len(paths) // subjects_per_group_per_fold for paths in data_input_groups.values())} folds."
                            )
                            continue

                        config["data_leakage_prevention"][
                            "lpso_subjects_per_group"
                        ] = count
                        break
                    else:
                        print("[ERROR] Please enter a positive number.")
                except ValueError:
                    print("[ERROR] Please enter a valid integer.")

        # Check for uneven group sizes and ask for handling strategy
        group_sizes = {
            group_name: len(paths) for group_name, paths in data_input_groups.items()
        }
        min_group_size = min(group_sizes.values())
        max_group_size = max(group_sizes.values())

        if min_group_size != max_group_size:
            print(f"   ⚠️  Uneven group sizes detected:")
            for group_name, size in group_sizes.items():
                print(f"      📊 {group_name}: {size} subjects")

            # Ask for uneven handling strategy
            uneven_handling_choice = questionary.select(
                "5.2.3 How should we handle uneven group sizes?",
                choices=[
                    "Cutoff - Stop when any group runs out of subjects",
                    "Wrap-around - Reuse subjects from beginning when group runs out",
                ],
            ).ask()

            if "Cutoff" in uneven_handling_choice:
                uneven_handling = "cutoff"
                print(
                    f"   ✅ Using cutoff strategy: will stop when any group runs out of subjects"
                )
            else:
                uneven_handling = "wrap_around"
                print(
                    f"   ✅ Using wrap-around strategy: will reuse subjects when group runs out"
                )

            config["data_leakage_prevention"]["uneven_handling"] = uneven_handling
        else:
            # All groups have the same size, use default
            uneven_handling = "cutoff"
            config["data_leakage_prevention"]["uneven_handling"] = uneven_handling

        # Generate LPSO folds
        print(f"   🔄 Generating LPSO folds...")
        try:
            # Check if individual LPSO is enabled
            individual_lpso = config["data_leakage_prevention"].get(
                "individual_lpso", False
            )

            lpso_folds, fold_metadata = generate_lpso_folds(
                data_input_groups,
                count,
                individual_lpso=individual_lpso,
                uneven_handling=uneven_handling,
                # random_seed=42
            )

            # Store the folds in config
            config["data_leakage_prevention"]["lpso_folds"] = lpso_folds
            config["data_leakage_prevention"]["lpso_metadata"] = fold_metadata

            print(f"   ✅ Generated {len(lpso_folds)} LPSO folds")
            print(f"   📊 Each fold leaves out {count} subjects per group")
            print(f"   🎯 Total unique test combinations: {len(lpso_folds)}")

            # Show example of first few folds
            if len(lpso_folds) > 0:
                print(f"   📋 Example fold 1: {len(lpso_folds[0])} subjects")
                if len(lpso_folds) > 1:
                    print(f"   📋 Example fold 2: {len(lpso_folds[1])} subjects")

        except ValueError as e:
            print(f"❌ ERROR generating LPSO folds: {e}")
            exit(1)

        # Set LPSO flag
        config["data_leakage_prevention"]["use_lpso"] = True

    # Question 2: Single train/test set definition (if single split is selected)
    elif "1 test/1 train split" in config["data_leakage_prevention"]["strategy"]:
        config["data_leakage_prevention"]["single_split_method"] = questionary.select(
            "5.2.1 How would you like to define this 1 training/testing set?",
            choices=[
                "Manually select test subjects and provide full paths",
                "Automatically split subjects (e.g., 5 test subjects)",
            ],
        ).ask()

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
                        config["data_leakage_prevention"]["test_subjects_count"] = count
                        break
                    else:
                        print("[ERROR] Please enter a positive number.")
                except ValueError:
                    print("[ERROR] Please enter a valid integer.")

            # Ask for test subject paths with validation
            # Get available group names for reference
            available_groups = list(data_input_groups.keys())
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
                        valid_test_paths, data_input_groups
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
                        != config["data_leakage_prevention"]["test_subjects_count"]
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
                num_groups = len(data_input_groups)
                test_subjects_count = questionary.text(
                    f"5.2.2 Enter number of subjects for test set (e.g., 4) (recommended: at least {num_groups} for balanced group representation):"
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

            # Automatically select test subjects and add them to config for reproducibility
            # This makes the split reproducible and explicit, avoiding the need for the Ray container
            # to re-implement the same random selection logic
            test_count = config["data_leakage_prevention"]["test_subjects_count"]
            if test_count >= 1:

                # Check if we have enough test subjects for balanced group representation
                num_groups = len(data_input_groups)
                if test_count < num_groups:
                    print(
                        f"\n⚠️  WARNING: You selected {test_count} test subject(s) but have {num_groups} groups."
                    )
                    print(
                        f"   This means not all groups will have test subjects, which may bias your results."
                    )
                    print(
                        f"   Recommended: Select at least {num_groups} test subjects for balanced representation."
                    )

                    proceed = questionary.select(
                        "Do you want to proceed anyway?",
                        choices=[
                            "Yes, proceed with current selection",
                            "No, let me change the count",
                        ],
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
                                    config["data_leakage_prevention"][
                                        "test_subjects_count"
                                    ] = new_count
                                    test_count = new_count
                                    break
                                else:
                                    print("[ERROR] Please enter a positive number.")
                            except ValueError:
                                print("[ERROR] Please enter a valid integer.")

                print(
                    f"\n🎯 Automatically selecting {test_count} test subject(s) for reproducibility..."
                )

                try:
                    # Use the dedicated function for automatic selection
                    selected_test_subjects, metadata = (
                        select_test_subjects_automatically(
                            data_input_groups, test_count, random_seed=42
                        )
                    )

                    # Add the selected subjects to config as if they were manually selected
                    config["data_leakage_prevention"][
                        "test_subjects_paths"
                    ] = selected_test_subjects

                    # Display results
                    print(
                        f"✅ Automatically selected test subjects: {', '.join(metadata['selected_subject_ids'])}"
                    )
                    print(f"   Paths: {', '.join(selected_test_subjects)}")
                    print(
                        f"   Random seed: {metadata['random_seed']} (for reproducibility)"
                    )

                    # Show group representation
                    if metadata["missing_groups"]:
                        print(
                            f"   ⚠️  Groups represented: {', '.join(sorted(metadata['selected_groups']))}"
                        )
                        print(
                            f"   ⚠️  Groups missing: {', '.join(sorted(metadata['missing_groups']))}"
                        )
                    else:
                        print(
                            f"   ✅ All groups represented: {', '.join(sorted(metadata['selected_groups']))}"
                        )

                    # Also add the random seed to config for transparency
                    config["data_leakage_prevention"]["random_seed"] = metadata[
                        "random_seed"
                    ]

                except ValueError as e:
                    print(f"❌ ERROR: {e}")
                    exit(1)

    # Question 2: Intra-test-train split configuration (for both strategies)
    elif ("Within-subject" in config["data_leakage_prevention"]["strategy"] and "train/test split" in config["data_leakage_prevention"]["strategy"]) or "Transform all data together" in config["data_leakage_prevention"]["strategy"]:
        
        # Determine strategy type for messaging
        is_within_subject = "Within-subject" in config["data_leakage_prevention"]["strategy"] and "train/test split" in config["data_leakage_prevention"]["strategy"]
        is_transform_all = "Transform all data together" in config["data_leakage_prevention"]["strategy"]
        
        if is_within_subject:
            print("\n📊 Within-Subject Train/Test Split Configuration")
            print("   This will split each subject's data 80/20 for train/test.")
            print("   Each subject contributes to both training and testing sets.")
            print("   This prevents data leakage while maximizing training data usage.")
            print("   Transformations will be fitted on training data only, then applied to both train and test.")
            should_ask_for_split = True
        elif is_transform_all:
            print("\n📊 Transform All Data Together Configuration")
            print("⚠️  WARNING: You selected to transform all data together.")
            print("   This may cause data leakage as test data will influence training transforms.")
            print("   However, you can optionally add an intra-test-train split AFTER transformation.")
            
            # Ask if user wants to add optional split after transformation
            add_split = questionary.select(
                "5.2.1 Do you want to add an optional intra-test-train split after transformation?",
                choices=[
                    "No - Transform all data together (no split - fastest, and potential data leakage)",
                    "Yes - Add split after transformation (prevents data leakage, slower)",
                ],
            ).ask()
            
            should_ask_for_split = "Yes" in add_split
            
            if should_ask_for_split:
                print("   ✅ Adding intra-test-train split after transformation")
            else:
                print("   ⚠️  No split configured - all data will be transformed together (potential data leakage)")
                print("   📊 Transform all data together configuration completed!")
        
        # Ask for split parameters if needed
        if should_ask_for_split:
            # Ask for train/test ratio
            ratio_prompt = "5.2.1 Enter train ratio (e.g., 0.8 for 80% train, 20% test):" if is_within_subject else "5.2.2 Enter train ratio (e.g., 0.8 for 80% train, 20% test):"
            while True:
                train_ratio_input = questionary.text(ratio_prompt).ask()
                try:
                    train_ratio = float(train_ratio_input)
                    if 0.1 <= train_ratio <= 0.9:
                        config["data_leakage_prevention"]["intra_test_train_split"] = {
                            "train_ratio": train_ratio,
                            "random_seed": project_config["random_seed"]
                        }
                        print(f"   ✅ Train ratio: {train_ratio:.1%}, Test ratio: {1.0-train_ratio:.1%}")
                        break
                    else:
                        print("[ERROR] Train ratio must be between 0.1 and 0.9.")
                except ValueError:
                    print("[ERROR] Please enter a valid decimal number (e.g., 0.8).")

            # Use global random seed from project configuration
            global_seed = project_config["random_seed"]
            config["data_leakage_prevention"]["intra_test_train_split"]["random_seed"] = global_seed
            print(f"   ✅ Using global random seed: {global_seed}")

            # Ask for split method
            method_prompt = "5.2.2 Select split method:" if is_within_subject else "5.2.3 Select split method:"
            split_method = questionary.select(
                method_prompt,
                choices=[
                    "random - Random split within each subject",
                    "start - First portion of epochs for training",
                    "middle - Middle portion of epochs for training", 
                    "end - Last portion of epochs for training",
                ],
            ).ask()
            
            # Map selection to config value
            if "random" in split_method:
                config["data_leakage_prevention"]["intra_test_train_split"]["split_method"] = "random"
                print("   ✅ Using random split method")
            elif "start" in split_method:
                config["data_leakage_prevention"]["intra_test_train_split"]["split_method"] = "start"
                print("   ✅ Using start split method (first portion for training)")
            elif "middle" in split_method:
                config["data_leakage_prevention"]["intra_test_train_split"]["split_method"] = "middle"
                print("   ✅ Using middle split method (middle portion for training)")
            elif "end" in split_method:
                config["data_leakage_prevention"]["intra_test_train_split"]["split_method"] = "end"
                print("   ✅ Using end split method (last portion for training)")
            
            # Final completion message
            if is_within_subject:
                print("   📊 Within-subject split configuration completed!")
            elif is_transform_all:
                print("   📊 Transform all data together with post-transformation split configuration completed!")

    return config


def deploymentMethodPart6(target: str, deployment_method: str) -> Dict[str, Any]:
    """
    Section 6: Deployment Configuration
    Args:
        target: The target type (pyspark-only, ray-only, or full)
        deployment_method: The deployment method selected in section 0
    Returns: Dictionary containing deployment configuration
    """
    config = {}

    # 6.1 PySpark Resource Configuration
    if target == "pyspark" or target == "pyspark-only" or target == "full":
        print("\n[6.1] PySpark Resource Configuration")
        print("For example, for a 8-core CPU with 16GB memory, we can safely allocate:")
        print("  - 6 cores for the driver (master)")
        print("  - 6GB memory for the driver")
        print("  - 6GB memory for executors")
        print("  - 2 cores per executor")
        print("  - 8 shuffle partitions")
        print("This is the default and lightweight for testing.")

        edit_spark_config = questionary.select(
            "6.1.1 Do you want to edit the PySpark resource configuration?",
            choices=["Yes", "No (use defaults)"],
        ).ask()

        if edit_spark_config == "Yes":
            config["pyspark"] = {}
            config["pyspark"]["master"] = validate_integer_input(
                "6.1.2 Enter number of cores/threads to allocate (master):", default="6"
            )
            config["pyspark"]["driver_memory"] = validate_integer_input(
                "6.1.3 Enter driver memory in GB (e.g., 6):", default="6"
            )
            config["pyspark"]["executor_memory"] = validate_integer_input(
                "6.1.4 Enter executor memory in GB (e.g., 6):", default="6"
            )
            config["pyspark"]["executor_cores"] = validate_integer_input(
                "6.1.5 Enter executor cores/threads:", default="2"
            )
            config["pyspark"]["shuffle_partitions"] = validate_integer_input(
                "6.1.6 Enter shuffle partitions:", default="8"
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

    # 6.2 SLURM Configuration (if Singularity with Slurm is selected)
    if deployment_method == "Singularity with Slurm":
        print("\n[6.2] SLURM Configuration")

        # Always ask for build options when using SLURM
        print("Recommended build options (10 minutes, 8GB RAM, 2 CPUs):")
        print("  --time=00:10:00 --mem=8G --cpus-per-task=2")
        build_slurm_options = questionary.text(
            "6.2.1 Enter SLURM options for building .sif containers:",
            default="--time=00:10:00 --mem=8G --cpus-per-task=2",
        ).ask()
        # Store SLURM options in a separate section to avoid overwriting project metadata
        config["slurm_options"] = {}
        config["slurm_options"]["build"] = (
            sanitize_slurm_options(build_slurm_options) if build_slurm_options else ""
        )

        if target == "full":
            # Ask if user wants same or different SLURM options for PySpark and Ray
            slurm_choice = questionary.select(
                "6.2.2 SLURM options for PySpark and Ray:",
                choices=["Same options for both", "Different options for each"],
            ).ask()

            if slurm_choice == "Same options for both":
                slurm_options = questionary.text(
                    "6.2.3 Enter SLURM options for both PySpark and Ray:",
                    default="--time=24:00:00 --mem=16G --cpus-per-task=4",
                ).ask()
                config["slurm_options"]["pyspark"] = (
                    sanitize_slurm_options(slurm_options) if slurm_options else ""
                )
                config["slurm_options"]["ray"] = (
                    sanitize_slurm_options(slurm_options) if slurm_options else ""
                )
            else:  # Different options
                pyspark_slurm = questionary.text(
                    "6.2.3 Enter SLURM options for PySpark:",
                    default="--time=12:00:00 --mem=8G --cpus-per-task=2",
                ).ask()
                ray_slurm = questionary.text(
                    "6.2.4 Enter SLURM options for Ray:",
                    default="--time=24:00:00 --mem=16G --cpus-per-task=4",
                ).ask()
                config["slurm_options"]["pyspark"] = (
                    sanitize_slurm_options(pyspark_slurm) if pyspark_slurm else ""
                )
                config["slurm_options"]["ray"] = (
                    sanitize_slurm_options(ray_slurm) if ray_slurm else ""
                )

        elif target == "pyspark-only":
            slurm_options = questionary.text(
                "6.3.2 Enter SLURM options for PySpark:",
                default="--time=12:00:00 --mem=8G --cpus-per-task=2",
            ).ask()
            config["slurm_options"]["pyspark"] = (
                sanitize_slurm_options(slurm_options) if slurm_options else ""
            )

        elif target == "ray-only":
            slurm_options = questionary.text(
                "6.3.2 Enter SLURM options for Ray:",
                default="--time=24:00:00 --mem=16G --cpus-per-task=4",
            ).ask()
            config["slurm_options"]["ray"] = (
                sanitize_slurm_options(slurm_options) if slurm_options else ""
            )

    return config


def rayConfigurationPart7(project_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Section 7: Ray Configuration
    Args:
        project_config: Dictionary containing project configuration (including random_seed)
    Returns: Dictionary containing ray configuration
    """
    print("\n[7] Ray Configuration")
    config = {}
    config["ray"] = {}

    # far in the future todo: make it such that we can choose distributed or sklearn (where distributed is ray and pyspark with raydp)
    # Machine Learning Models Selection
    selected_models = questionary.checkbox(
        "7.1 Select machine learning models to test:",
        choices=[
            "Random Forest",
            "XGBoost",
            "MLP (Neural Network)",
            "KNN",
            "SVM",
            "Logistic Regression",
            "Logistic Regression",
            "Decision Tree",
            "Gradient Boosting",
            "AdaBoost",
        ],
    ).ask()

    config["ray"]["models"] = selected_models

    # 7.2 Individual Model Hyperparameter Configuration
    if selected_models:
        print("\n[7.2] Individual Model Hyperparameter Configuration")
        print("Configure hyperparameter search spaces for each selected model.")
        print("You can customize the search ranges for better optimization.")

        config["ray"]["model_configs"] = {}

        for model in selected_models:
            print(f"\n--- Configuring {model} ---")

            # Ask if user wants to customize hyperparameters for this model
            customize = questionary.select(
                f"7.2.{selected_models.index(model)+1} Customize hyperparameters for {model}?",
                choices=["Use default grid", "Customize hyperparameters"],
            ).ask()

            if customize == "Use default grid":
                config["ray"]["model_configs"][model] = {"use_default": True}
            else:
                # Model-specific hyperparameter configuration
                config["ray"]["model_configs"][model] = configure_model_hyperparameters(
                    model
                )

    config["ray"]["num_trials"] = validate_integer_input(
        "7.3 Enter number of trials for hyperparameter optimization:", default="10"
    )

    config["ray"]["max_concurrent"] = validate_integer_input(
        "7.4 Enter maximum concurrent trials:", default="2"
    )

    config["ray"]["metric"] = questionary.select(
        "7.5 Select optimization metric:",
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
        "7.6 Select optimization mode:", choices=["max", "min"]
    ).ask()

    config["ray"]["cv_folds"] = validate_integer_input(
        "7.7 Enter number of cross-validation folds:", default="5"
    )

    # Use global random seed from project configuration
    global_seed = project_config["random_seed"]
    config["ray"]["random_state"] = str(global_seed)
    print(f"   ✅ Using global random seed: {global_seed}")

    print("\n[7.8] Graph Data Visualization")
    
    # Initialize graph_data_visualization dictionary
    config["ray"]["graph_data_visualization"] = {}
    
    config["ray"]["graph_data_visualization"]["save_prediction_outputs"] = questionary.select(
        "7.8.1 Do you want to save the training and testing final ml predictions for each hyper-parameter combination as pandas dataframes? (required for automatic graph generation)",
        choices=["Yes", "No"],
    ).ask()

    # 7.8 graph data visualization
    if config["ray"]["graph_data_visualization"]["save_prediction_outputs"] == "Yes":
   

       config["ray"]["graph_data_visualization"]["best_models_graph"] = questionary.select(
           "7.8.2 Do you want to get a graph of best model of each machine learning model (best KNN, best SVM, etc.)?",
           choices=["Yes", "No"],
       ).ask()

       config["ray"]["graph_data_visualization"]["per_model_accross_hyperparameters_graph"] = questionary.select(
           "7.8.3 Do you want to get a graph of per model accross hyperparameters (KNN euclidean, KNN manhattan, etc.)?",
           choices=["Yes", "No"],
       ).ask()

       config["ray"]["graph_data_visualization"]["per_model_per_hyperparameter_across_folds_graph"] = questionary.select(
           "7.8.4 Do you want to get a graph of per model per hyperparameter across folds (KNN euclidean fold 1, KNN manhattan, etc.)?",
           choices=["Yes", "No"],
       ).ask()

       config["ray"]["graph_data_visualization"]["per_subject_analysis_graph"] = questionary.select(
           "7.8.5 Do you want to get a per-subject analysis graph showing accuracy for each subject (e.g., sub-001, sub-002, etc.)?",
           choices=["Yes", "No"],
       ).ask()
       
       # If per-subject analysis is enabled, ask for number of top models
       if config["ray"]["graph_data_visualization"]["per_subject_analysis_graph"] == "Yes":
           config["ray"]["graph_data_visualization"]["per_subject_top_n_models"] = validate_integer_input(
               "7.8.6 How many top-performing models should be included in per-subject analysis? (default: 3)",
               default="3",
               min_value=1
           )

    # 7.9 Ray Resource Configuration
    print("\n[7.9] Ray Resource Configuration")
    print(
        "Ray resource configuration helps optimize performance for hyperparameter tuning."
    )
    print("If not configured, Ray will fall back to PySpark resource settings.")

    configure_ray_resources = questionary.select(
        "7.9.1 Do you want to configure Ray-specific resources?",
        choices=["Yes", "No (use approximatley the same settings as PySpark)"],
    ).ask()

    if configure_ray_resources == "Yes":
        print("\nRay Resource Configuration:")
        print("For example, for a 8-core CPU with 16GB memory, we can safely allocate:")
        print("  - 4-6 CPUs for Ray cluster")
        print("  - 8-12GB memory for Ray")
        print("  - 2-4 concurrent trials")
        print("This is optimized for ML workloads.")

        config["ray"]["resources"] = {}
        config["ray"]["resources"]["num_cpus"] = validate_integer_input(
            "7.9.2 Enter number of CPUs for Ray cluster:", default="4"
        )
        config["ray"]["resources"]["memory_gb"] = validate_integer_input(
            "7.9.3 Enter memory in GB for Ray:", default="8"
        )
        config["ray"]["resources"]["object_store_memory_gb"] = validate_integer_input(
            "7.9.4 Enter object store memory in GB (for data caching):", default="4"
        )

        # Ask for GPU configuration if needed
        use_gpu = questionary.select(
            "7.9.5 Do you want to use GPU acceleration (if available)?",
            choices=["No", "Yes"],
        ).ask()

        if use_gpu == "Yes":
            config["ray"]["resources"]["num_gpus"] = validate_integer_input(
                "7.9.6 Enter number of GPUs to use:", default="0"
            )
        else:
            config["ray"]["resources"]["num_gpus"] = 0

        # # Ask for Ray dashboard port
        # config["ray"]["resources"]["dashboard_port"] = validate_integer_input(
        #     "7.9.7 Enter Ray dashboard port (for monitoring):", default="8265"
        # )

        print("✅ Ray resource configuration completed")
    else:  # 'No (use approximatley the same settings as PySpark)'
        print("ℹ️  Ray will use PySpark resource settings as fallback")

        # Get PySpark settings to use as base for Ray resources
        pyspark_master = int(config.get("pyspark", {}).get("master", "6"))
        pyspark_driver_memory = int(config.get("pyspark", {}).get("driver_memory", "6"))
        pyspark_executor_memory = int(
            config.get("pyspark", {}).get("executor_memory", "6")
        )

        # Calculate Ray resources based on PySpark settings
        ray_cpus = max(2, pyspark_master - 2)  # Leave some cores for system
        ray_memory = max(
            4, pyspark_driver_memory + pyspark_executor_memory - 4
        )  # Leave some memory for system
        ray_object_store = max(
            2, ray_memory // 2
        )  # Object store is typically half of total memory

        # Set Ray resources based on PySpark fallback
        config["ray"]["resources"] = {
            "num_cpus": str(ray_cpus),
            "memory_gb": str(ray_memory),
            "object_store_memory_gb": str(ray_object_store),
            "num_gpus": 0,
            "dashboard_port": "8265",
        }

    return config


def get_hyperparameter_with_custom(
    parameter_name: str, choices: List[str], custom_prompt: str = None
) -> List[str]:
    """
    Get hyperparameter selection with custom option.

    Args:
        parameter_name: Name of the parameter for display
        choices: List of predefined choices
        custom_prompt: Custom prompt for custom value input (optional)

    Returns:
        List of selected values including any custom values
    """
    # Add custom option to choices
    choices_with_custom = choices + ["custom"]

    # Get user selection
    selected = questionary.checkbox(
        f"{parameter_name}:", choices=choices_with_custom
    ).ask()

    # Handle custom values
    if "custom" in selected:
        selected.remove("custom")
        if custom_prompt is None:
            custom_prompt = f"Enter custom {parameter_name.lower()} value:"

        custom_value = questionary.text(custom_prompt).ask()
        if custom_value.strip():
            selected.append(custom_value.strip())

    return selected


def configure_model_hyperparameters(model_name: str) -> dict:
    """
    Configure hyperparameters for a specific model.

    Args:
        model_name: Name of the model to configure

    Returns:
        Dictionary with hyperparameter configuration
    """
    config = {"use_default": False, "hyperparameters": {}}

    if model_name == "Random Forest":
        print("\nRandom Forest Hyperparameters:")
        config["hyperparameters"]["n_estimators"] = get_hyperparameter_with_custom(
            "n_estimators (number of trees)", ["50", "100", "200", "300", "500"]
        )

        config["hyperparameters"]["max_depth"] = get_hyperparameter_with_custom(
            "max_depth (max tree depth)",
            ["None", "10", "20", "30", "50"],
            "Enter custom max_depth value (or 'None'):",
        )

        config["hyperparameters"]["min_samples_split"] = get_hyperparameter_with_custom(
            "min_samples_split", ["2", "5", "10", "20"]
        )

        config["hyperparameters"]["max_features"] = get_hyperparameter_with_custom(
            "max_features",
            ["sqrt", "log2", "None"],
            "Enter custom max_features value (sqrt, log2, None, or number):",
        )

    elif model_name == "XGBoost":
        print("\nXGBoost Hyperparameters:")
        config["hyperparameters"]["n_estimators"] = get_hyperparameter_with_custom(
            "n_estimators (number of trees)", ["50", "100", "200", "300", "500"]
        )

        config["hyperparameters"]["max_depth"] = get_hyperparameter_with_custom(
            "max_depth (max tree depth)", ["3", "6", "9", "12", "15"]
        )

        config["hyperparameters"]["learning_rate"] = get_hyperparameter_with_custom(
            "learning_rate", ["0.01", "0.05", "0.1", "0.2", "0.3"]
        )

        config["hyperparameters"]["subsample"] = get_hyperparameter_with_custom(
            "subsample (fraction of samples)", ["0.6", "0.7", "0.8", "0.9", "1.0"]
        )

    elif model_name == "SVM":
        print("\nSVM Hyperparameters:")
        config["hyperparameters"]["C"] = get_hyperparameter_with_custom(
            "C (regularization parameter)", ["0.1", "0.5", "1.0", "5.0", "10.0", "50.0"]
        )

        config["hyperparameters"]["kernel"] = get_hyperparameter_with_custom(
            "kernel", ["rbf", "linear", "poly", "sigmoid"]
        )

        config["hyperparameters"]["gamma"] = get_hyperparameter_with_custom(
            "gamma", ["scale", "auto", "0.001", "0.01", "0.1"]
        )

    elif model_name == "KNN":
        print("\nKNN Hyperparameters:")
        config["hyperparameters"]["n_neighbors"] = get_hyperparameter_with_custom(
            "n_neighbors", ["1", "2", "3", "5", "7", "9", "11", "15", "21"]
        )

        config["hyperparameters"]["weights"] = get_hyperparameter_with_custom(
            "weights", ["uniform", "distance"]
        )

        config["hyperparameters"]["metric"] = get_hyperparameter_with_custom(
            "metric", ["euclidean", "manhattan", "minkowski", "cosine"]
        )

    elif model_name == "Gradient Boosting":
        print("\nGradient Boosting Hyperparameters:")
        config["hyperparameters"]["n_estimators"] = get_hyperparameter_with_custom(
            "n_estimators", ["50", "100", "200", "300"]
        )

        config["hyperparameters"]["max_depth"] = get_hyperparameter_with_custom(
            "max_depth", ["3", "6", "9", "12"]
        )

        config["hyperparameters"]["learning_rate"] = get_hyperparameter_with_custom(
            "learning_rate", ["0.01", "0.05", "0.1", "0.2", "0.3"]
        )

        config["hyperparameters"]["subsample"] = get_hyperparameter_with_custom(
            "subsample", ["0.6", "0.7", "0.8", "0.9", "1.0"]
        )

    elif model_name == "MLP (Neural Network)":
        print("\nMLP (Neural Network) Hyperparameters:")

        # Ask for number of different MLP architectures
        while True:
            num_mlps = validate_integer_input(
                "How many different MLP architectures do you want to test? (1-3)",
                default="3",
            )
            if 1 <= int(num_mlps) <= 3:
                break
            print("⚠️  Please enter a number between 1 and 3")

        mlp_architectures = []
        for mlp_idx in range(int(num_mlps)):
            print(f"\n--- Configuring MLP Architecture {mlp_idx + 1} ---")

            # Ask for number of hidden layers
            while True:
                num_layers = validate_integer_input(
                    f"MLP {mlp_idx + 1}: How many hidden layers? (1-10)", default="1"
                )
                if 1 <= int(num_layers) <= 10:
                    break
                print("⚠️  Please enter a number between 1 and 10")

            layer_sizes = []
            for layer_idx in range(int(num_layers)):
                while True:
                    neurons = validate_integer_input(
                        f"MLP {mlp_idx + 1}, Layer {layer_idx + 1}: How many neurons? (5-500)",
                        default="50",
                    )
                    if 5 <= int(neurons) <= 500:
                        layer_sizes.append(int(neurons))
                        break
                    print("⚠️  Please enter a number between 5 and 500")

            # Convert to tuple format for sklearn
            architecture = tuple(layer_sizes)
            mlp_architectures.append(str(architecture))
            print(f"✅ MLP {mlp_idx + 1} architecture: {architecture}")

        config["hyperparameters"]["hidden_layer_sizes"] = mlp_architectures

        # Show summary of created architectures
        print(f"\n📊 MLP Architecture Summary:")
        for i, arch in enumerate(mlp_architectures):
            print(f"   🧠 MLP {i+1}: {arch}")

        config["hyperparameters"]["activation"] = questionary.checkbox(
            "activation:", choices=["relu", "tanh", "logistic"]
        ).ask()

        config["hyperparameters"]["alpha"] = questionary.checkbox(
            "alpha (regularization):", choices=["0.0001", "0.001", "0.01", "0.1"]
        ).ask()

    elif model_name == "Decision Tree":
        print("\nDecision Tree Hyperparameters:")
        config["hyperparameters"]["max_depth"] = get_hyperparameter_with_custom(
            "max_depth",
            ["None", "5", "10", "15", "20", "30"],
            "Enter custom max_depth value (or 'None'):",
        )

        config["hyperparameters"]["min_samples_split"] = get_hyperparameter_with_custom(
            "min_samples_split", ["2", "5", "10", "20"]
        )

        config["hyperparameters"]["max_features"] = get_hyperparameter_with_custom(
            "max_features",
            ["sqrt", "log2", "None"],
            "Enter custom max_features value (sqrt, log2, None, or number):",
        )

    elif model_name == "AdaBoost":
        print("\nAdaBoost Hyperparameters:")
        config["hyperparameters"]["n_estimators"] = get_hyperparameter_with_custom(
            "n_estimators", ["50", "100", "200", "300"]
        )

        config["hyperparameters"]["learning_rate"] = get_hyperparameter_with_custom(
            "learning_rate", ["0.01", "0.05", "0.1", "0.2", "0.5", "1.0"]
        )

        config["hyperparameters"]["algorithm"] = get_hyperparameter_with_custom(
            "algorithm", ["SAMME", "SAMME.R"]
        )

    elif model_name in ["Logistic Regression", "Logistic Regression"]:
        print(f"\n{model_name} Hyperparameters:")
        config["hyperparameters"]["C"] = get_hyperparameter_with_custom(
            "C (inverse regularization strength)",
            ["0.1", "0.5", "1.0", "5.0", "10.0", "50.0"],
        )

        config["hyperparameters"]["solver"] = get_hyperparameter_with_custom(
            "solver", ["lbfgs", "liblinear", "newton-cg", "sag", "saga"]
        )

        config["hyperparameters"]["max_iter"] = get_hyperparameter_with_custom(
            "max_iter", ["100", "200", "500", "1000"]
        )

    return config

    # 7.9 Ray Resource Configuration
    print("\n[7.9] Ray Resource Configuration")
    print(
        "Ray resource configuration helps optimize performance for hyperparameter tuning."
    )
    print("If not configured, Ray will fall back to PySpark resource settings.")

    # configure_ray_resources = questionary.select(
    #     "7.9.1 Do you want to configure Ray-specific resources?",
    #     choices=["Yes", "No (use PySpark settings as fallback)"],
    # ).ask()

    # if configure_ray_resources == "Yes":
    if True:
        print("\nRay Resource Configuration:")
        print("For example, for a 8-core CPU with 16GB memory, we can safely allocate:")
        print("  - 4-6 CPUs for Ray cluster")
        print("  - 8-12GB memory for Ray")
        print("  - 2-4 concurrent trials")
        print("This is optimized for ML workloads.")

        config["ray"]["resources"] = {}
        config["ray"]["resources"]["num_cpus"] = validate_integer_input(
            "7.9.2 Enter number of CPUs for Ray cluster:", default="4"
        )
        config["ray"]["resources"]["memory_gb"] = validate_integer_input(
            "7.9.3 Enter memory in GB for Ray:", default="8"
        )
        config["ray"]["resources"]["object_store_memory_gb"] = validate_integer_input(
            "7.9.4 Enter object store memory in GB (for data caching):", default="4"
        )

        # Ask for GPU configuration if needed
        use_gpu = questionary.select(
            "7.9.5 Do you want to use GPU acceleration (if available)?",
            choices=["No", "Yes"],
        ).ask()

        if use_gpu == "Yes":
            config["ray"]["resources"]["num_gpus"] = validate_integer_input(
                "7.9.6 Enter number of GPUs to use:", default="1"
            )
        else:
            config["ray"]["resources"]["num_gpus"] = 0

        # Ask for Ray dashboard port
        config["ray"]["resources"]["dashboard_port"] = validate_integer_input(
            "7.9.7 Enter Ray dashboard port (for monitoring):", default="8265"
        )

        print("✅ Ray resource configuration completed")

    return config


def build_config(target: str) -> Tuple[Dict[str, Any], str]:
    config: Dict[str, Any] = {}

    # 0. Metadata
    project_config, config_name = run_section_with_confirmation(
        "Project Metadata", metadataPart0
    )
    config.update(project_config)

    if target == "pyspark-only" or target == "full":
        # 1. Data Input
        data_input_config = run_section_with_confirmation("Data Input", dataInputPart1)
        config.update(data_input_config)

        # 2. Preprocessing
        preprocessing_config = run_section_with_confirmation(
            "Preprocessing", preprocessingPart2
        )
        config.update(preprocessing_config)

        # 3. Feature Extraction
        feature_extraction_config = run_section_with_confirmation(
            "Feature Extraction",
            featureCreationPart3,
            config["project"]["experiment_type"],
        )
        config.update(feature_extraction_config)

        # 4. Feature Transformation
        feature_transformation_config = run_section_with_confirmation(
            "Feature Transformation", featureTransformationsPart4
        )
        config.update(feature_transformation_config)

        # 5. Data Leakage Prevention (only if ML experiment type and Feature Transformation are enabled)
        if config["project"]["experiment_type"] in ["ML Classification", "ML Fingerprinting"] and config[
            "feature_transformation"
        ]["transformations"] != ["None"]:
            data_leakage_prevention_config = run_section_with_confirmation(
                "Data Leakage Prevention",
                dataLeakagePreventionPart5,
                config["project"]["experiment_type"],
                config["feature_transformation"]["transformations"],
                config["data_input"]["groups"],
                config["project"],
            )
            config.update(data_leakage_prevention_config)

    else:
        print(
            "\nSkipping [1] Data Input [2] Preprocessing [3] Feature Extraction [4] Feature Transformation, and [5] Data Leakage Prevention as we are not using PySpark"
        )

    # 6. Deployment Configuration
    print("\n[6] Deployment Configuration")
    deployment_method_config = run_section_with_confirmation(
        "Deployment Configuration",
        deploymentMethodPart6,
        target,
        config["project"]["deployment_method"],
    )
    config.update(deployment_method_config)

    # Move SLURM options to project section if they exist
    if "slurm_options" in config:
        if "project" not in config:
            config["project"] = {}
        # Create slurm_options subsection in project
        config["project"]["slurm_options"] = {}
        slurm_options = config["slurm_options"]
        if "build" in slurm_options:
            config["project"]["slurm_options"]["build"] = slurm_options["build"]
        if "pyspark" in slurm_options:
            config["project"]["slurm_options"]["pyspark"] = slurm_options["pyspark"]
        if "ray" in slurm_options:
            config["project"]["slurm_options"]["ray"] = slurm_options["ray"]
        del config["slurm_options"]  # Remove the temporary section

    # 7. Ray Configuration (only if target is ray-only or full AND experiment type is ML)
    if (target == "ray-only" or target == "full") and config["project"][
        "experiment_type"
    ] in ["ML Classification", "ML Clustering", "ML Fingerprinting"]:
        ray_config = run_section_with_confirmation(
            "Ray Configuration", rayConfigurationPart7, config["project"]
        )
        config.update(ray_config)
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
    if config.get("data_leakage_prevention", {}).get("test_subjects_paths"):
        test_subject_paths = config["data_leakage_prevention"]["test_subjects_paths"]
        test_count = len(test_subject_paths)

        # Extract subject IDs from paths
        selected_subject_ids = []
        for test_subject_path in test_subject_paths:
            path_parts = test_subject_path.split("/")
            filename = path_parts[-1]
            subject_id = (
                filename.replace("_task-eyesclosed_eeg.set", "")
                .replace("_eeg.set", "")
                .replace(".set", "")
                .replace(".fif", "")
            )
            selected_subject_ids.append(subject_id)

        if test_count == 1:
            print(
                f"🎯 Test Subject: {selected_subject_ids[0]} (automatically selected)"
            )
            print(f"   📍 Path: {test_subject_paths[0]}")
        else:
            print(
                f"🎯 Test Subjects: {', '.join(selected_subject_ids)} (automatically selected)"
            )
            print(f"   📍 Count: {test_count} subjects")
            for i, (subject_id, path) in enumerate(
                zip(selected_subject_ids, test_subject_paths), 1
            ):
                print(f"      {i}. {subject_id}: {path}")

    # Show LPSO information if applicable
    elif config.get("data_leakage_prevention", {}).get("use_lpso"):
        lpso_metadata = config["data_leakage_prevention"]["lpso_metadata"]
        total_folds = lpso_metadata.get("total_folds", "unknown")
        subjects_per_group = lpso_metadata.get("subjects_per_group", "unknown")
        total_subjects = lpso_metadata.get("total_subjects", "unknown")

        print(f"🎯 LPSO Cross-Validation: {total_folds} folds")
        print(f"   📊 Leave out {subjects_per_group} subjects per group per fold")
        print(f"   📈 Total subjects: {total_subjects}")
        print(f"   🔄 Each subject used as test data exactly once")

        # Show example of first fold if available
        if config.get("data_leakage_prevention", {}).get("lpso_folds"):
            first_fold = config["data_leakage_prevention"]["lpso_folds"][0]
            if first_fold:
                # Extract subject IDs from first fold
                first_fold_subject_ids = []
                for test_path in first_fold:
                    path_parts = test_path.split("/")
                    filename = path_parts[-1]
                    subject_id = (
                        filename.replace("_task-eyesclosed_eeg.set", "")
                        .replace("_eeg.set", "")
                        .replace(".set", "")
                        .replace(".fif", "")
                    )
                    first_fold_subject_ids.append(subject_id)

                print(f"   📋 Example fold 1: {', '.join(first_fold_subject_ids)}")

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


def confirm_config_section(section_name: str, section_config: Dict[str, Any]) -> bool:
    """
    Display a configuration section and ask user to confirm.

    Args:
        section_name: Name of the configuration section
        section_config: Dictionary containing the section configuration

    Returns:
        True if user confirms, False if user wants to redo the section
    """
    print(f"\n" + "=" * 60)
    print(f"📋 {section_name.upper()} CONFIGURATION REVIEW")
    print("=" * 60)

    # Pretty print the configuration
    yaml_str = yaml.dump(section_config, default_flow_style=False, sort_keys=False)
    print(yaml_str)

    # Ask for confirmation
    confirm = questionary.select(
        f"✅ Does this {section_name.lower()} configuration look correct?",
        choices=["Yes, continue to next section", "No, let me redo this section"],
    ).ask()

    return confirm == "Yes, continue to next section"


def run_section_with_confirmation(section_name: str, section_function, *args, **kwargs):
    """
    Run a configuration section function with confirmation loop.

    Args:
        section_name: Name of the section for display
        section_function: Function to run for the section
        *args, **kwargs: Arguments to pass to the section function

    Returns:
        The configuration dictionary from the section
    """
    while True:
        section_config = section_function(*args, **kwargs)
        if confirm_config_section(section_name, section_config):
            return section_config


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


def generate_lpso_folds(
    groups: Dict[str, List[str]],
    subjects_per_group: int,
    random_seed: int = 42,
    individual_lpso: bool = False,
    uneven_handling: str = "cutoff",
) -> Tuple[List[List[str]], Dict[str, Any]]:
    """
    Generate LPSO (Leave-P-Subjects-Out) folds with systematic, ordered selection.

    Args:
        groups: Dictionary of group names to subject paths
        subjects_per_group: Number of subjects to leave out per group per fold
        random_seed: Random seed for reproducibility (default: 42) - not used for ordering
        individual_lpso: If True, each subject gets its own test fold regardless of group
        uneven_handling: How to handle uneven group sizes - "cutoff" (stop when any group runs out)
                        or "wrap_around" (reuse subjects from beginning when group runs out)

    Returns:
        Tuple of (list_of_test_subject_lists, metadata_dict)
    """

    if individual_lpso:
        # Individual LPSO: each subject gets its own test fold
        print(f"   🎯 Generating Individual LPSO folds (one per subject)")

        # Collect all subjects from all groups
        all_subjects = []
        for group_name, paths in groups.items():
            for path in paths:
                all_subjects.append(path)

        # Create one fold per subject
        all_folds = []
        for subject_path in all_subjects:
            all_folds.append([subject_path])  # Each fold contains exactly one subject

        # Create metadata for individual LPSO
        metadata = {
            "total_folds": len(all_folds),
            "subjects_per_group": len(all_subjects),
            "subjects_per_group_per_fold": 1,
            "total_subjects": len(all_subjects),
            "groups": list(groups.keys()),
            "num_groups": len(groups),
            "fold_generation_method": "individual_lpso",
        }

        return all_folds, metadata

    else:
        # Standard LPSO: systematic selection per group
        num_groups = len(groups)

        # Check if subjects_per_group is evenly divisible by number of groups
        if subjects_per_group % num_groups != 0:
            print(
                f"   ⚠️  WARNING: Subjects per group ({subjects_per_group}) is not evenly divisible by number of groups ({num_groups})"
            )
            print(
                f"   📊 This will result in uneven subject distribution across groups"
            )

        # Calculate subjects per group per fold
        subjects_per_group_per_fold = subjects_per_group // num_groups

        # Collect all subjects with their group information, maintaining order
        subjects_by_group = {}
        for group_name, paths in groups.items():
            subjects_by_group[group_name] = paths.copy()  # Keep original order

        # Check for uneven group sizes and provide warning
        group_sizes = {
            group_name: len(subjects)
            for group_name, subjects in subjects_by_group.items()
        }
        min_group_size = min(group_sizes.values())
        max_group_size = max(group_sizes.values())

        if min_group_size != max_group_size:
            print(f"   ⚠️  WARNING: Uneven group sizes detected:")
            for group_name, size in group_sizes.items():
                print(f"      📊 {group_name}: {size} subjects")
            print(f"   🎯 Using '{uneven_handling}' strategy for uneven groups")

            if uneven_handling == "cutoff":
                print(
                    f"   📋 Strategy: Stop creating folds when any group runs out of subjects"
                )
            elif uneven_handling == "wrap_around":
                print(
                    f"   📋 Strategy: Reuse subjects from beginning when group runs out (wrap-around)"
                )
            else:
                raise ValueError(
                    f"Invalid uneven_handling option: {uneven_handling}. Use 'cutoff' or 'wrap_around'"
                )

        # Validate that each group has enough subjects for at least one fold
        for group_name, subjects in subjects_by_group.items():
            if len(subjects) < subjects_per_group_per_fold:
                raise ValueError(
                    f"Group {group_name} has only {len(subjects)} subjects, but {subjects_per_group_per_fold} are needed per fold"
                )

        # Validate that we don't leave out all subjects (which would leave no training data)
        total_subjects = sum(len(subjects) for subjects in subjects_by_group.values())
        if subjects_per_group >= total_subjects:
            raise ValueError(
                f"❌ Invalid LPSO configuration: {subjects_per_group} subjects per group >= {total_subjects} total subjects. "
                f"This would leave no training subjects, preventing transformers from fitting. "
                f"Please ensure at least one subject remains for training."
            )

        # Generate systematic folds
        all_folds = []
        group_names = list(subjects_by_group.keys())

        # Calculate how many folds we can generate based on strategy
        if uneven_handling == "cutoff":
            # Stop when any group runs out of subjects
            max_folds = min_group_size // subjects_per_group_per_fold
            print(
                f"   📊 Generating {max_folds} folds with {subjects_per_group_per_fold} subjects per group per fold (cutoff strategy)"
            )
        else:  # wrap_around
            # Can generate more folds by reusing subjects
            max_folds = max_group_size // subjects_per_group_per_fold
            print(
                f"   📊 Generating {max_folds} folds with {subjects_per_group_per_fold} subjects per group per fold (wrap-around strategy)"
            )

        for fold_idx in range(max_folds):
            fold_subjects = []

            for group_name in group_names:
                # Get subjects for this group for this fold
                start_idx = fold_idx * subjects_per_group_per_fold
                end_idx = start_idx + subjects_per_group_per_fold

                if uneven_handling == "cutoff":
                    # Stop if we run out of subjects in this group
                    if start_idx >= len(subjects_by_group[group_name]):
                        print(
                            f"   ⏹️  Stopping at fold {fold_idx + 1}: Group {group_name} ran out of subjects"
                        )
                        break

                    # Take available subjects (might be fewer than requested)
                    available_subjects = subjects_by_group[group_name][start_idx:]
                    if len(available_subjects) < subjects_per_group_per_fold:
                        print(
                            f"   ⚠️  Fold {fold_idx + 1}: Group {group_name} only has {len(available_subjects)} subjects available (requested {subjects_per_group_per_fold})"
                        )
                        group_subjects = available_subjects
                    else:
                        group_subjects = available_subjects[
                            :subjects_per_group_per_fold
                        ]

                else:  # wrap_around
                    # Use modulo to wrap around when we run out of subjects
                    group_subjects = []
                    for i in range(subjects_per_group_per_fold):
                        subject_idx = (start_idx + i) % len(
                            subjects_by_group[group_name]
                        )
                        group_subjects.append(
                            subjects_by_group[group_name][subject_idx]
                        )

                    # Check if we're reusing subjects
                    if start_idx + subjects_per_group_per_fold > len(
                        subjects_by_group[group_name]
                    ):
                        print(
                            f"   🔄 Fold {fold_idx + 1}: Group {group_name} using wrap-around (reusing subjects)"
                        )

                fold_subjects.extend(group_subjects)

            # If we broke out of the loop due to cutoff, stop creating more folds
            if uneven_handling == "cutoff" and len(fold_subjects) < subjects_per_group:
                print(
                    f"   ⏹️  Stopping fold generation: insufficient subjects for complete fold"
                )
                break

            all_folds.append(fold_subjects)

        # Create metadata
        metadata = {
            "total_folds": len(all_folds),
            "subjects_per_group": subjects_per_group,
            "subjects_per_group_per_fold": subjects_per_group_per_fold,
            "total_subjects": sum(
                len(subjects) for subjects in subjects_by_group.values()
            ),
            "groups": list(groups.keys()),
            "num_groups": num_groups,
            "fold_generation_method": "systematic_ordered",
        }

        return all_folds, metadata


def select_test_subjects_automatically(
    groups: Dict[str, List[str]], test_count: int, random_seed: int = 42
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
        raise ValueError(
            "No subjects found in groups. Please check your data input configuration."
        )

    if test_count > len(all_subject_paths):
        raise ValueError(
            f"Requested {test_count} test subjects but only {len(all_subject_paths)} subjects available."
        )

    # Use fixed seed for reproducibility
    random.seed(random_seed)

    # Select test subjects with balanced group representation when possible
    if test_count >= num_groups:
        # Try to select at least one subject from each group
        selected_test_subjects = []
        remaining_subjects = all_subject_paths.copy()

        # First, select one subject from each group
        for group_name, group_paths in groups.items():
            if remaining_subjects and any(
                path in remaining_subjects for path in group_paths
            ):
                # Find subjects from this group that are still available
                available_from_group = [
                    path for path in group_paths if path in remaining_subjects
                ]
                if available_from_group:
                    selected = random.choice(available_from_group)
                    selected_test_subjects.append(selected)
                    remaining_subjects.remove(selected)

        # Fill remaining slots with random selection from all remaining subjects
        remaining_needed = test_count - len(selected_test_subjects)
        if remaining_needed > 0 and remaining_subjects:
            additional_subjects = random.sample(
                remaining_subjects, min(remaining_needed, len(remaining_subjects))
            )
            selected_test_subjects.extend(additional_subjects)

        # If we still don't have enough, add more from any available subjects
        if len(selected_test_subjects) < test_count:
            all_available = [
                path for path in all_subject_paths if path not in selected_test_subjects
            ]
            if all_available:
                additional_needed = test_count - len(selected_test_subjects)
                additional = random.sample(
                    all_available, min(additional_needed, len(all_available))
                )
                selected_test_subjects.extend(additional)
    else:
        # Simple random selection when we can't guarantee balance
        selected_test_subjects = random.sample(all_subject_paths, test_count)

    # Extract subject IDs from paths for display
    selected_subject_ids = []
    for subject_path in selected_test_subjects:
        path_parts = subject_path.split("/")
        filename = path_parts[-1]
        # Remove common EEG file extensions and task suffixes
        subject_id = (
            filename.replace("_task-eyesclosed_eeg.set", "")
            .replace("_eeg.set", "")
            .replace(".set", "")
            .replace(".fif", "")
        )
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
        "num_groups": num_groups,
    }

    return selected_test_subjects, metadata


if __name__ == "__main__":
    target: str = get_target_with_ray_option()
    print(f"Generating config for target: {target}")

    config, config_name = build_config(target=target)
    save_config(config, config_name)

