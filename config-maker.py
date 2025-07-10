from datetime import datetime
from pathlib import Path

import questionary
import yaml


def infer_target():
    this_file = Path(
        __file__
    )  # no resolve as it gets absolute path which will be the parent directory as we are simlinking
    repo_name = this_file.parent.name
    print(f"Running config_maker from: {repo_name}")

    if repo_name == "eeg-pyspark-pipeline":
        return "pyspark"
    elif repo_name == "eeg-ray-tuner":
        return "ray"
    else:
        return "full"


def validate_downsampling_rate(rate_str):
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


def build_config(target: str):
    config = {}

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

    # If Singularity with Slurm is selected, ask for Slurm options
    if config["project"]["deployment_method"] == "Singularity with Slurm":
        slurm_options = questionary.text(
            "Enter Slurm options (e.g., --time=24:00:00 --mem=16G --cpus-per-task=4):"
        ).ask()
        config["project"]["slurm_options"] = slurm_options if slurm_options else ""

    # Use timestamp for config name (consistent approach)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    config_name = f"config_{timestamp}.yaml"
    config["project"]["config_name"] = config_name

    # 1. Data Input
    print("\n[1] Data Input")
    config["data_input"] = {}
    config["data_input"]["groups"] = {}
    i = 1
    while True:
        group_input = questionary.text(
            f"Enter comma-separated EEG paths for Group {i} (or 'done'):"
        ).ask()
        if group_input.lower() == "done":
            break
        if not group_input.strip():
            print("[ERROR] Please enter valid paths to the *.set/.fif files or 'done'")
            continue
        config["data_input"]["groups"][f"group_{i}"] = [
            path.strip() for path in group_input.split(",") if path.strip()
        ]
        i += 1

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

    # Ask for split details based on the selected method
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


def save_config(config, config_name):
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


if __name__ == "__main__":
    target = infer_target()
    print(f"Generating config for target: {target}")
    config, config_name = build_config(target=target)
    save_config(config, config_name)
