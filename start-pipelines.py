import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import yaml

# Configuration constants - edit these to change paths/commands
CONTAINER_CONFIG = {
    "pyspark": {
        "docker_image": "nour333/eeg-spark-pipeline:latest",
        "singularity_image": "./containers/eeg-pyspark.sif",
        "entrypoint": "/app/main.py",
        # "entrypoint": "/app/src/test_config_access.py",
        "command": "spark-submit",
        "job_name": "pyspark-pipeline",
        # Spark-submit specific configurations (most Spark configs are in session_builder.py)
        "spark_configs": ["--conf", "spark.jars.ivy=/tmp/.ivy2"],
        "mounts": [
            # (f"./config/{user_config_namec}", "/app/config"),   # User YAML configs (editable)
            ("./config/spark", "/opt/bitnami/spark/conf"),  # Spark configs (editable)
            ("./data", "/app/data"),  # Output / intermediate features
            # entrypoint.sh --> export LOG_FILE_PATH="/opt/bitnami/spark/logs/spark-driver-$(date +%Y-%m-%d_%H-%M).log"
            ("./logs/spark-events", "/opt/bitnami/spark/logs/"),  # Spark event logs
            # Future additions (e.g., user EEG data, model output, results)
            # ("./user_data", "/app/user_data"),
            # ("./output", "/app/output"),
        ],
        "ports": [
            "4040:4040"
        ],
    },
    "ray": {
        "docker_image": "nour333/eeg-ray-tuner:latest",
        "singularity_image": "./containers/eeg-ray-pipeline.sif",
        "entrypoint": "/app/test-ray.py",
        "command": "python",
        "job_name": "ray-tuner",
        "mounts": [
            # Editable + persistent (bind mount everything explicitly)
            # Add any additional mounts here if needed for Ray
            # Example: ("./ray_config", "/app/ray_config"),
        ],
    },
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def check_config(specific_config: Optional[str] = None) -> str:
    """Check for config file and return the path to the most recent one or specified one."""
    config_dir = Path("config")

    if not config_dir.exists():
        print(f"❌ Config directory not found at {config_dir}")
        sys.exit(1)

    if specific_config:
        # Use the specified config file
        config_path = config_dir / specific_config
        if not config_path.exists():
            print(f"❌ Specified config file not found: {config_path}")
            sys.exit(1)
        print(f"📁 Using specified config: {config_path}")
        return str(config_path.resolve())

    # Find the most recent config file
    # Config files are now named as config_<projectname>_<day-month-year>_<HHMM>.yaml
    config_files = list(config_dir.glob("config_*.yaml"))
    if not config_files:
        print(f"❌ No config files found in {config_dir}")
        print(
            "Run config-maker.py first to create a configuration file (format: config_<projectname>_<day-month-year>_<HHMM>.yaml)."
        )
        sys.exit(1)

    # Sort by modification time (most recent first)
    config_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    most_recent = config_files[0]

    print(f"📁 Using most recent config: {most_recent.name}")
    if len(config_files) > 1:
        print(
            f"📋 Available configs: {[f.name for f in config_files]} (format: config_<projectname>_<day-month-year>_<HHMM>.yaml)"
        )

    return str(most_recent.resolve())


def load_config(config_path: str) -> Dict[str, Any]:
    """Load the configuration file to determine deployment method."""
    with open(config_path, "r") as f:
        config = cast(
            Dict[str, Any], yaml.safe_load(f)
        )  # cast to Dict[str, Any] to avoid type errors
    return config


def infer_pipeline_mode() -> str:
    """Infer which pipeline mode to run based on repository name."""
    this_path = Path(
        __file__
    )  # .resolve() # since soft link, if resolved then would get eeg-full-pipeline directory and would get incorrect parent directory
    repo = this_path.parent.name

    if repo == "eeg-pyspark-pipeline":
        return "pyspark-only"
    elif repo == "eeg-ray-pipeline":
        return "ray-only"
    else:
        return "full"


def create_required_directories() -> None:
    """Create required directories for the pipeline."""
    directories = [
        "config",
        "config/spark",
        "logs",
        "logs/spark-events",
        "data",  # we can override this with the user config , need implement logic for this
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created/verified directory: {directory}")


def copy_data_to_scratch(config: Dict[str, Any]) -> None:
    """Copy data files to /scratch/ for compute node access."""
    if "data_input" in config and "groups" in config["data_input"]:
        scratch_dir = "/scratch/ans9868/eeg-data"
        Path(scratch_dir).mkdir(parents=True, exist_ok=True)

        print(f"📁 Copying data files to {scratch_dir}...")

        for group_name, file_list in config["data_input"]["groups"].items():
            if isinstance(file_list, list):
                for file_path in file_list:
                    if isinstance(file_path, str):
                        # Get just the filename
                        filename = Path(file_path).name
                        dest_path = f"{scratch_dir}/{filename}"

                        # Copy if not already there
                        if not Path(dest_path).exists():
                            print(f"   Copying {file_path} -> {dest_path}")
                            import shutil

                            shutil.copy2(file_path, dest_path)
                        else:
                            print(f"   Skipping {filename} (already exists)")

        print(f"✅ Data files copied to {scratch_dir}")

        # Update the config to use scratch paths
        for group_name, file_list in config["data_input"]["groups"].items():
            if isinstance(file_list, list):
                for i, file_path in enumerate(file_list):
                    if isinstance(file_path, str):
                        filename = Path(file_path).name
                        config["data_input"]["groups"][group_name][
                            i
                        ] = f"{scratch_dir}/{filename}"


# =============================================================================
# CORE CONTAINER EXECUTION FUNCTIONS
# =============================================================================


def get_container_command(container_type: str, config_path: str) -> str:
    """Get the command to run inside the container."""
    config = CONTAINER_CONFIG[container_type]

    # Build command parts
    command_parts = [config["command"]]

    # Add spark-submit specific configs for pyspark
    if container_type == "pyspark":
        spark_configs = config.get("spark_configs", [])
        command_parts.extend(spark_configs)

    # Add entrypoint and config
    command_parts.extend([config["entrypoint"], "--config", "/app/config.yaml"])

    return " ".join(command_parts)


def build_user_mounts(config: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Build user-specific mounts from config."""
    user_mounts = []

    # Add data directories from config
    if "data_input" in config and "groups" in config["data_input"]:
        seen_dirs = set()
        for group_name, file_list in config["data_input"]["groups"].items():
            if isinstance(file_list, list):
                for file_path in file_list:
                    if isinstance(file_path, str):
                        # Bind individual files directly
                        # This is more precise and avoids directory permission issues
                        if file_path not in seen_dirs:
                            seen_dirs.add(file_path)
                            # Mount the individual file to the same path inside the container
                            user_mounts.append((file_path, file_path))
                            print(f"🔗 Adding mount: {file_path} -> {file_path}")

    # Add output directory (this can override the default ./data mount)
    if "project" in config and "output_dir" in config["project"]:
        output_dir = config["project"]["output_dir"]

        # Convert relative path to absolute path
        if output_dir.startswith("./"):
            output_dir = str(Path.cwd() / output_dir[2:])
        elif output_dir.startswith("."):
            output_dir = str(Path.cwd() / output_dir[1:])

        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Mount output directory to /app/data (overriding default ./data)
        user_mounts.append((output_dir, "/app/data"))
        print(
            f"🔧 User config overrides default ./data mount with: {config['project']['output_dir']}"
        )

    return user_mounts


def get_all_mount_mappings(
    container_type: str, config_path: str, config_data: Dict[str, Any]
) -> List[Tuple[str, str]]:
    """Get all mount mappings for a container type based on CONTAINER_CONFIG."""
    container_config = CONTAINER_CONFIG[container_type]
    mount_mappings = []

    # Add specific config file mount
    mount_mappings.append((config_path, "/app/config.yaml"))

    # Add static mounts from configuration (but check for user overrides)
    static_mounts = container_config["mounts"].copy()

    # Check if user config has output_dir that would override ./data
    user_has_output_dir = (
        "project" in config_data and "output_dir" in config_data["project"]
    )

    # If user specified output_dir, filter out the default ./data mount to avoid conflicts
    if user_has_output_dir:
        static_mounts = [
            (host_path, container_path)
            for host_path, container_path in static_mounts
            if not (host_path == "./data" and container_path == "/app/data")
        ]
        print(
            f"🔧 User config overrides default ./data mount with: {config_data['project']['output_dir']}"
        )

    mount_mappings.extend(static_mounts)

    # Add dynamic mounts (built from user config)
    dynamic_mounts = build_user_mounts(config_data)
    mount_mappings.extend(dynamic_mounts)

    return mount_mappings


def run_docker_container(container_type: str, config_path: str) -> None:
    """Run a single Docker container."""
    config = CONTAINER_CONFIG[container_type]
    command_parts = get_container_command(container_type, config_path).split()

    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_all_mount_mappings(container_type, config_path, config_data)

    # Build docker run command with volume mounts
    docker_cmd = ["docker", "run", "--rm"]

    # All Spark and Hadoop configurations are now centralized in session_builder.py
    # But LD_PRELOAD is still needed for nss_wrapper in Docker
    docker_cmd.extend(["-e", "LD_PRELOAD=/opt/bitnami/common/lib/libnss_wrapper.so"])

    # Add port mappings for pyspark container
    if container_type == "pyspark":
        ports = config.get("ports", [])
        for port_mapping in ports:
            docker_cmd.extend(["-p", port_mapping])

    # Add volume mounts
    for host_path, container_path in mount_mappings:
        docker_cmd.extend(["-v", f"{host_path}:{container_path}"])

    # Add image and command
    docker_cmd.extend([config["docker_image"]] + command_parts)

    print(f"🔗 Mounting {len(mount_mappings)} directories:")

    # Show first few directories
    show_count = min(5, len(mount_mappings))
    for i, (host_path, container_path) in enumerate(mount_mappings[:show_count], 1):
        print(f"   {i}. {host_path} -> {container_path}")

    if len(mount_mappings) > show_count:
        print(f"   ... and {len(mount_mappings) - show_count} more directories")

    print(f"🔗 Running command: {docker_cmd}")

    try:
        subprocess.run(docker_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Docker command failed with exit code {e.returncode}")

        # Check for common Docker mount errors
        if "operation not permitted" in str(e).lower() or "mkdir" in str(e).lower():
            print("\n🔍 Most likely causes:")
            print("   1. Docker doesn't have full disk access")
            print(
                "   2. Docker doesn't have permission to access the specified files/directories"
            )
            print("   3. The files/directories don't exist")
            print("\n💡 Solutions:")
            print(
                "   • On macOS: Go to System Preferences > Security & Privacy > Privacy > Full Disk Access"
            )
            print("     and add Docker to the list")
            print(
                "   • Check that all paths in your config file exist and are accessible"
            )
            print("   • Ensure Docker has permission to access the mounted directories")
            print(
                "   • Try running with sudo if on Linux (not recommended for production)"
            )
        if "no such file or directory" in str(e).lower():
            print("\n🔍 Most likely cause: One or more files/directories don't exist")
            print("\n💡 Solution: Check that all paths in your config file exist")
        if "permission denied" in str(e).lower():
            print(
                "\n🔍 Most likely cause: Permission denied accessing files/directories"
            )
            print("\n💡 Solutions:")
            print("   • Check file permissions on the mounted directories")
            print("   • Ensure Docker has permission to access the files")
            print("   • On macOS: Check Docker's Full Disk Access permissions")

        print(f"\n🔍 Error details: {e}")

        print(f"\n📋 Full error output:")
        if e.stdout:
            print(f"STDOUT: {e.stdout.decode()}")
        if e.stderr:
            print(f"STDERR: {e.stderr.decode()}")

        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Docker command not found")
        print("💡 Please ensure Docker is installed and available in your PATH")
        sys.exit(1)


def run_singularity_container(container_type: str, config_path: str) -> None:
    """Run a single Singularity container."""
    config = CONTAINER_CONFIG[container_type]
    command_parts = get_container_command(container_type, config_path).split()

    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_all_mount_mappings(container_type, config_path, config_data)

    # Build singularity run command with bind mounts
    singularity_cmd = ["singularity", "run"]

    # Add bind mounts
    for host_path, container_path in mount_mappings:
        singularity_cmd.extend(["--bind", f"{host_path}:{container_path}"])

    # Add image and command
    singularity_cmd.extend([config["singularity_image"]] + command_parts)

    print(f"🔗 Mounting {len(mount_mappings)} directories:")

    # Show first few directories
    show_count = min(5, len(mount_mappings))
    for i, (host_path, container_path) in enumerate(mount_mappings[:show_count], 1):
        print(f"   {i}. {host_path} -> {container_path}")

    if len(mount_mappings) > show_count:
        print(f"   ... and {len(mount_mappings) - show_count} more directories")

    print(f"🔗 Running command: {singularity_cmd}")

    try:
        subprocess.run(singularity_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Singularity command failed with exit code {e.returncode}")

        # Check for common Singularity mount errors
        if "operation not permitted" in str(e).lower() or "mkdir" in str(e).lower():
            print("\n🔍 Most likely causes:")
            print(
                "   1. Singularity doesn't have permission to access the specified files/directories"
            )
            print("   2. The files/directories don't exist")
            print("   3. Insufficient permissions to bind mount directories")
            print("\n💡 Solutions:")
            print(
                "   • Check that all paths in your config file exist and are accessible"
            )
            print(
                "   • Ensure Singularity has permission to access the mounted directories"
            )
            print(
                "   • Check file permissions on the directories you're trying to mount"
            )
            print(
                "   • Try running with sudo if on Linux (not recommended for production)"
            )
        elif "no such file or directory" in str(e).lower():
            print("\n🔍 Most likely cause: One or more files/directories don't exist")
            print("\n💡 Solution: Check that all paths in your config file exist")
        elif "permission denied" in str(e).lower():
            print(
                "\n🔍 Most likely cause: Permission denied accessing files/directories"
            )
            print("\n💡 Solutions:")
            print("   • Check file permissions on the mounted directories")
            print("   • Ensure Singularity has permission to access the files")
            print("   • Check if the .sif file exists and is accessible")
        else:
            print(f"\n🔍 Error details: {e}")

        print(f"\n📋 Full error output:")
        if e.stdout:
            print(f"STDOUT: {e.stdout.decode()}")
        if e.stderr:
            print(f"STDERR: {e.stderr.decode()}")

        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Singularity command not found")
        print("💡 Please ensure Singularity is installed and available in your PATH")
        sys.exit(1)


# =============================================================================
# DOCKER EXECUTION FUNCTIONS
# =============================================================================


def run_docker_pyspark_only(config_path: str) -> None:
    print("\n🐳 Running PySpark container only...")
    run_docker_container("pyspark", config_path)


def run_docker_ray_only(config_path: str) -> None:
    print("\n🐳 Running Ray pipeline container only...")
    run_docker_container("ray", config_path)


def run_docker(config_path: str) -> None:
    print("\n🐳 Running PySpark container...")
    run_docker_container("pyspark", config_path)

    print("\n🐳 Running Ray pipeline container...")
    run_docker_container("ray", config_path)


# =============================================================================
# SINGULARITY EXECUTION FUNCTIONS
# =============================================================================


def run_singularity_pyspark_only(config_path: str) -> None:
    print("\n🔒 Running PySpark Singularity container only...")
    run_singularity_container("pyspark", config_path)


def run_singularity_ray_only(config_path: str) -> None:
    print("\n🔒 Running Ray pipeline Singularity container only...")
    run_singularity_container("ray", config_path)


def run_singularity_without_slurm(config_path: str) -> None:
    print("\n🔒 Running PySpark Singularity container...")
    run_singularity_container("pyspark", config_path)

    print("\n🔒 Running Ray pipeline Singularity container...")
    run_singularity_container("ray", config_path)


# =============================================================================
# SLURM EXECUTION FUNCTIONS
# =============================================================================


def create_slurm_script(
    container_type: str,
    config_path: str,
    slurm_options: str = "",
    dependency_job_id: Optional[str] = None,
) -> str:
    """Create a SLURM script for a container."""
    config = CONTAINER_CONFIG[container_type]
    command = get_container_command(container_type, config_path)

    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_all_mount_mappings(container_type, config_path, config_data)

    dependency_line = (
        f"#SBATCH --dependency=afterok:{dependency_job_id}\n"
        if dependency_job_id
        else ""
    )

    # Build bind mount arguments for singularity (separate --bind flags)
    bind_args = []
    for host_path, container_path in mount_mappings:
        bind_args.extend(["--bind", f"{host_path}:{container_path}"])

    # Create the full singularity command for debugging
    singularity_cmd = (
        f"singularity run {' '.join(bind_args)} {config['singularity_image']} {command}"
    )

    # Debug: print the bind_args to see if there are any issues
    print(f"🔍 Debug - bind_args: {bind_args}")

    print(f"🔗 SLURM will execute this Singularity command:")

    # Print the command in a readable single-line format
    bind_parts = []
    for host_path, container_path in mount_mappings:
        bind_parts.append(f"--bind {host_path}:{container_path}")
    print(
        f"   singularity run {' '.join(bind_parts)} {config['singularity_image']} {command}"
    )

    print(f"🔗 With {len(mount_mappings)} bind mounts:")
    for i, (host_path, container_path) in enumerate(mount_mappings, 1):
        print(f"   {i}. {host_path} -> {container_path}")

    slurm_content = f"""#!/bin/bash
#SBATCH {slurm_options}
#SBATCH --job-name={config['job_name']}
#SBATCH --output=./containers/{container_type}_%j.out
#SBATCH --error=./containers/{container_type}_%j.err
{dependency_line}{singularity_cmd}
"""
    print("\nHere is the SLURM script: \n")
    print(slurm_content)
    print("\n")
    return slurm_content


def run_singularity_with_slurm_shared_options(
    config_path: str, slurm_options: str = ""
) -> None:
    """Convenience function: run with same SLURM options for both containers."""
    return run_singularity_with_slurm_separate_options(
        config_path, slurm_options, slurm_options
    )


def run_singularity_with_slurm_separate_options(
    config_path: str, pyspark_slurm_options: str = "", ray_slurm_options: str = ""
) -> None:
    """Run full pipeline with separate SLURM options for each container."""
    print("\n🧬 Submitting PySpark SLURM job...")

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
        print("❌ Failed to get job ID from sbatch output.")
        sys.exit(1)

    # Create temporary SLURM script for Ray with dependency
    ray_slurm_content = create_slurm_script(
        "ray", config_path, ray_slurm_options, job_id
    )

    with open("./containers/temp_ray.slurm", "w") as f:
        f.write(ray_slurm_content)

    print(f"\n🧬 Submitting Ray pipeline SLURM job (after PySpark job {job_id})...")
    subprocess.run(["sbatch", "./containers/temp_ray.slurm"], check=True)

    # Clean up temporary files
    os.remove("./containers/temp_pyspark.slurm")
    os.remove("./containers/temp_ray.slurm")


def run_singularity_slurm_pyspark_only(
    config_path: str, slurm_options: str = ""
) -> None:
    print("\n🧬 Submitting PySpark SLURM job only...")

    pyspark_slurm_content = create_slurm_script("pyspark", config_path, slurm_options)

    with open("./containers/temp_pyspark.slurm", "w") as f:
        f.write(pyspark_slurm_content)

    subprocess.run(["sbatch", "./containers/temp_pyspark.slurm"], check=True)

    # Clean up temporary file
    os.remove("./containers/temp_pyspark.slurm")


def run_singularity_slurm_ray_only(config_path: str, slurm_options: str = "") -> None:
    print("\n�� Submitting Ray pipeline SLURM job only...")

    ray_slurm_content = create_slurm_script("ray", config_path, slurm_options)

    with open("./containers/temp_ray.slurm", "w") as f:
        f.write(ray_slurm_content)

    subprocess.run(["sbatch", "./containers/temp_ray.slurm"], check=True)

    # Clean up temporary file
    os.remove("./containers/temp_ray.slurm")


# =============================================================================
# CONTAINER BUILDING FUNCTIONS
# =============================================================================


def check_and_build_sif_files(
    config: Dict[str, Any], pipeline_mode: str, use_slurm: bool = False
) -> None:
    """Check if .sif files exist and build them if they don't.

    Args:
        config: The loaded configuration
        pipeline_mode: "pyspark-only", "ray-only", or "full"
        use_slurm: Whether to use SLURM for building (default: False)
    """
    # Create containers directory if it doesn't exist
    containers_dir = Path("./containers")
    containers_dir.mkdir(exist_ok=True)

    builds_submitted = False

    # Determine which containers to check based on pipeline mode
    containers_to_check = []
    if pipeline_mode in ["pyspark-only", "full"]:
        containers_to_check.append(
            (
                "eeg-pyspark-pipeline.sif",
                CONTAINER_CONFIG["pyspark"]["singularity_image"],
                "pyspark",
            )
        )
    if pipeline_mode in ["ray-only", "full"]:
        containers_to_check.append(
            (
                "eeg-ray-pipeline.sif",
                CONTAINER_CONFIG["ray"]["singularity_image"],
                "ray",
            )
        )

    # Check and build each required container
    for sif_name, docker_uri, build_type in containers_to_check:
        sif_path = Path(f"./containers/{sif_name}")
        if not sif_path.exists():
            print(f"🔨 {build_type.capitalize()} .sif file not found: {sif_name}")
            if use_slurm:
                slurm_options = config.get("project", {}).get("slurm_options_build", "")
                build_sif_with_slurm(
                    sif_name, docker_uri, f"{build_type}_build", slurm_options
                )
                builds_submitted = True
            else:
                build_sif_locally(sif_name, docker_uri, build_type)

    # If builds were submitted via SLURM, wait for them to complete
    if builds_submitted:
        print("\n⏳ Waiting for container builds to complete...")
        print("💡 You can check build status with: squeue -u $USER")
        print("💡 Build logs are in ./containers/ directory")

        # Wait for .sif files to appear
        max_wait_time = 1800  # 30 minutes
        wait_interval = 10  # 30 seconds
        waited_time = 0

        while waited_time < max_wait_time:
            all_built = all(
                Path(f"./containers/{sif_name}").exists()
                for sif_name, _, _ in containers_to_check
            )
            if all_built:
                print("✅ All container builds completed!")
                break
            time.sleep(wait_interval)
            waited_time += wait_interval
            print(f"⏳ Still waiting for builds... ({waited_time}s elapsed)")

        if not all(
            Path(f"./containers/{sif_name}").exists()
            for sif_name, _, _ in containers_to_check
        ):
            print("❌ Timeout waiting for container builds to complete")
            print("💡 Check build logs in ./containers/ directory")
            sys.exit(1)


def build_sif_with_slurm(
    sif_name: str, docker_uri: str, job_prefix: str, slurm_options: str = ""
) -> None:
    """Build .sif file using SLURM job."""
    print(f"🧬 Submitting SLURM job to build {sif_name}...")

    # Create SLURM script for building
    build_slurm_content = f"""#!/bin/bash
#SBATCH {slurm_options}
#SBATCH --job-name={job_prefix}
#SBATCH --output=./containers/{job_prefix}_%j.out
#SBATCH --error=./containers/{job_prefix}_%j.err

echo "Building {sif_name} from {docker_uri}"
singularity build ./containers/{sif_name} {docker_uri}
echo "Build completed for {sif_name}"
"""

    # Write SLURM script to containers directory
    slurm_script_path = f"./containers/{job_prefix}.slurm"
    with open(slurm_script_path, "w") as f:
        f.write(build_slurm_content)

    # Submit SLURM job
    subprocess.run(["sbatch", slurm_script_path], check=True)
    print(f"✅ SLURM build job submitted for {sif_name}")
    print(f"📁 Logs will be saved in ./containers/")
    print(f"⏳ Please wait for the build to complete before running the pipeline.")


def build_sif_locally(sif_name: str, docker_uri: str, build_type: str) -> None:
    """Build .sif file locally."""
    print(f"🔨 Building {sif_name} locally from {docker_uri}...")

    # Create log file
    log_file = f"./containers/{build_type}_build.log"

    try:
        # Build the .sif file and redirect output to log
        with open(log_file, "w") as log:
            result = subprocess.run(
                ["singularity", "build", f"./containers/{sif_name}", docker_uri],
                stdout=log,
                stderr=log,
                text=True,
            )

        if result.returncode == 0:
            print(f"✅ Successfully built {sif_name}")
            print(f"📁 Build log saved to {log_file}")
        else:
            print(f"❌ Failed to build {sif_name}")
            print(f"📁 Check build log at {log_file}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error building {sif_name}: {e}")
        sys.exit(1)


# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================


def main() -> None:
    # Check if a specific config file was provided as command line argument
    specific_config = sys.argv[1] if len(sys.argv) > 1 else None

    config_path = check_config(specific_config)
    config = load_config(config_path)

    # Get deployment method from config
    deployment_method = config.get("project", {}).get("deployment_method", "Docker")
    pipeline_mode = infer_pipeline_mode()

    print(f"🚀 Starting pipeline with deployment method: {deployment_method}")
    print(f"🎯 Pipeline mode: {pipeline_mode}")

    # Create required directories
    print("\n📁 Setting up required directories...")
    create_required_directories()

    # Copy data to scratch if using SLURM (for compute node access)
    if deployment_method == "Singularity with Slurm":
        print("\n📁 Copying data files to /scratch/ for compute node access...")
        copy_data_to_scratch(config)

    if deployment_method == "Docker":
        if pipeline_mode == "pyspark-only":
            run_docker_pyspark_only(config_path)
        elif pipeline_mode == "ray-only":
            run_docker_ray_only(config_path)
        else:  # full
            run_docker(config_path)
    elif deployment_method == "Singularity without Slurm":
        check_and_build_sif_files(config, pipeline_mode, use_slurm=False)
        if pipeline_mode == "pyspark-only":
            run_singularity_pyspark_only(config_path)
        elif pipeline_mode == "ray-only":
            run_singularity_ray_only(config_path)
        else:  # full
            run_singularity_without_slurm(config_path)
    elif deployment_method == "Singularity with Slurm":
        check_and_build_sif_files(config, pipeline_mode, use_slurm=True)
        if pipeline_mode == "pyspark-only":
            slurm_options = config.get("project", {}).get("slurm_options_pyspark", "")
            run_singularity_slurm_pyspark_only(config_path, slurm_options)
        elif pipeline_mode == "ray-only":
            slurm_options = config.get("project", {}).get("slurm_options_ray", "")
            run_singularity_slurm_ray_only(config_path, slurm_options)
        else:  # full
            pyspark_slurm = config.get("project", {}).get("slurm_options_pyspark", "")
            ray_slurm = config.get("project", {}).get("slurm_options_ray", "")
            run_singularity_with_slurm_separate_options(
                config_path, pyspark_slurm, ray_slurm
            )
    else:
        print(f"❌ Unknown deployment method: {deployment_method}")
        print(
            "Supported methods: Docker, Singularity with Slurm, Singularity without Slurm"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
