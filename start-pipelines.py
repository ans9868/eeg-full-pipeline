import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple, Union, cast
import yaml

# Configuration constants - edit these to change paths/commands
CONTAINER_CONFIG = {
    "pyspark": {
        "docker_image": "nour333/eeg-spark-pipeline:latest",
        "singularity_image": "./containers/eeg-pyspark.sif",
        "entrypoint": "/app/src/main.py",
        # "entrypoint": "/app/src/test_config_access.py",
        "command": "spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --master local[*]",
        "job_name": "eeg-pyspark",
    },
    "ray": {
        "docker_image": "nour333/eeg-ray-tuner:latest",
        "singularity_image": "./containers/eeg-ray-tuner.sif",
        "entrypoint": "/app/test-ray.py",
        "command": "python",
        "job_name": "eeg-ray-tuner",
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
        print("Run config-maker.py first to create a configuration file (format: config_<projectname>_<day-month-year>_<HHMM>.yaml).")
        sys.exit(1)

    # Sort by modification time (most recent first)
    config_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    most_recent = config_files[0]

    print(f"📁 Using most recent config: {most_recent.name}")
    if len(config_files) > 1:
        print(f"📋 Available configs: {[f.name for f in config_files]} (format: config_<projectname>_<day-month-year>_<HHMM>.yaml)")

    return str(most_recent.resolve())


def load_config(config_path: str) -> Dict[str, Any]:
    """Load the configuration file to determine deployment method."""
    with open(config_path, "r") as f:
        config = cast(Dict[str, Any], yaml.safe_load(f)) # cast to Dict[str, Any] to avoid type errors
    return config


def infer_pipeline_mode() -> str:
    """Infer which pipeline mode to run based on repository name."""
    this_path = Path(
        __file__
    )  # .resolve() # since soft link, if resolved then would get eeg-full-pipeline directory and would get incorrect parent directory
    repo = this_path.parent.name

    if repo == "eeg-pyspark-pipeline":
        return "pyspark-only"
    elif repo == "eeg-ray-tuner":
        return "ray-only"
    else:
        return "full"


# =============================================================================
# CORE CONTAINER EXECUTION FUNCTIONS
# =============================================================================


def get_container_command(container_type: str, config_path: str) -> str:
    """Generate the command for a specific container type."""
    config = CONTAINER_CONFIG[container_type]
    if container_type == "pyspark":
        return f"{config['command']} {config['entrypoint']} --config /app/config.yaml"
    else:  # ray
        return f"{config['command']} {config['entrypoint']} --config /app/config.yaml"


def get_data_directories_to_mount(config: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Extract unique directories from file paths in config and return mount mappings."""
    mount_mappings = []
    seen_dirs = set()
    
    # Extract all file paths from the config
    all_file_paths = []
    if "data_input" in config and "groups" in config["data_input"]:
        for group_name, file_list in config["data_input"]["groups"].items():
            if isinstance(file_list, list):
                all_file_paths.extend(file_list)
    
    # Extract unique directories
    for file_path in all_file_paths:
        if isinstance(file_path, str):
            # Get the directory containing the file
            dir_path = str(Path(file_path).parent)
            if dir_path not in seen_dirs:
                seen_dirs.add(dir_path)
                # Mount the directory to the same path inside the container
                mount_mappings.append((dir_path, dir_path))
    
    # Add output directory FIRST (so it appears in the top few)
    output_mount = None
    if "project" in config and "output_dir" in config["project"]:
        output_dir = config["project"]["output_dir"]
        # Convert relative path to absolute path
        if output_dir.startswith("./"):
            output_dir = str(Path.cwd() / output_dir[2:])
        elif output_dir.startswith("."):
            output_dir = str(Path.cwd() / output_dir[1:])
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Mount output directory to the same path inside container
        output_mount = (output_dir, output_dir)
    
    # Put output directory first, then data directories
    if output_mount:
        mount_mappings.insert(0, output_mount)
    
    return mount_mappings


def run_docker_container(container_type: str, config_path: str) -> None:
    """Run a single Docker container."""
    config = CONTAINER_CONFIG[container_type]
    command_parts = get_container_command(container_type, config_path).split()
    
    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_data_directories_to_mount(config_data)
    
    # Build docker run command with volume mounts
    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{config_path}:/app/config.yaml",
    ]
    
    # Add data directory mounts
    for host_path, container_path in mount_mappings:
        docker_cmd.extend(["-v", f"{host_path}:{container_path}"])
    
    # Add image and command
    docker_cmd.extend([config["docker_image"]] + command_parts)
    
    print(f"🔗 Mounting {len(mount_mappings)} directories:")
    
    # Show first few directories (including output directory which is first)
    show_count = min(5, len(mount_mappings))
    for i, (host_path, container_path) in enumerate(mount_mappings[:show_count], 1):
        print(f"   {i}. {host_path} -> {container_path}")
    
    if len(mount_mappings) > show_count:
        print(f"   ... and {len(mount_mappings) - show_count} more directories")
    
    subprocess.run(docker_cmd, check=True)


def run_singularity_container(container_type: str, config_path: str) -> None:
    """Run a single Singularity container."""
    config = CONTAINER_CONFIG[container_type]
    command_parts = get_container_command(container_type, config_path).split()
    
    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_data_directories_to_mount(config_data)
    
    # Build singularity run command with bind mounts
    singularity_cmd = [
        "singularity",
        "run",
        "--bind",
        f"{config_path}:/app/config.yaml",
    ]
    
    # Add data directory bind mounts
    for host_path, container_path in mount_mappings:
        singularity_cmd.extend(["--bind", f"{host_path}:{container_path}"])
    
    # Add image and command
    singularity_cmd.extend([config["singularity_image"]] + command_parts)
    
    print(f"🔗 Mounting {len(mount_mappings)} directories:")
    
    # Show first few directories (including output directory which is first)
    show_count = min(5, len(mount_mappings))
    for i, (host_path, container_path) in enumerate(mount_mappings[:show_count], 1):
        print(f"   {i}. {host_path} -> {container_path}")
    
    if len(mount_mappings) > show_count:
        print(f"   ... and {len(mount_mappings) - show_count} more directories")
    
    subprocess.run(singularity_cmd, check=True)


# =============================================================================
# DOCKER EXECUTION FUNCTIONS
# =============================================================================


def run_docker_pyspark_only(config_path: str) -> None:
    print("\n🐳 Running PySpark container only...")
    run_docker_container("pyspark", config_path)


def run_docker_ray_only(config_path: str) -> None:
    print("\n🐳 Running Ray tuner container only...")
    run_docker_container("ray", config_path)


def run_docker(config_path: str) -> None:
    print("\n🐳 Running PySpark container...")
    run_docker_container("pyspark", config_path)

    print("\n🐳 Running Ray tuner container...")
    run_docker_container("ray", config_path)


# =============================================================================
# SINGULARITY EXECUTION FUNCTIONS
# =============================================================================


def run_singularity_pyspark_only(config_path: str) -> None:
    print("\n🔒 Running PySpark Singularity container only...")
    run_singularity_container("pyspark", config_path)


def run_singularity_ray_only(config_path: str) -> None:
    print("\n🔒 Running Ray tuner Singularity container only...")
    run_singularity_container("ray", config_path)


def run_singularity_without_slurm(config_path: str) -> None:
    print("\n🔒 Running PySpark Singularity container...")
    run_singularity_container("pyspark", config_path)

    print("\n🔒 Running Ray tuner Singularity container...")
    run_singularity_container("ray", config_path)


# =============================================================================
# SLURM EXECUTION FUNCTIONS
# =============================================================================


def create_slurm_script(
    container_type: str,
    config_path: str,
    slurm_options: str = "",
    dependency_job_id: Optional[str] = None
) -> str:
    """Create a SLURM script for a container."""
    config = CONTAINER_CONFIG[container_type]
    command = get_container_command(container_type, config_path)

    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_data_directories_to_mount(config_data)

    dependency_line = (
        f"#SBATCH --dependency=afterok:{dependency_job_id}\n"
        if dependency_job_id
        else ""
    )

    # Build bind mount string for singularity
    bind_mounts = [f"{config_path}:/app/config.yaml"]
    for host_path, container_path in mount_mappings:
        bind_mounts.append(f"{host_path}:{container_path}")
    
    bind_mount_string = ",".join(bind_mounts)

    slurm_content = f"""#!/bin/bash
#SBATCH {slurm_options}
#SBATCH --job-name={config['job_name']}
#SBATCH --output=./containers/{container_type}_%j.out
#SBATCH --error=./containers/{container_type}_%j.err
{dependency_line}singularity run --bind {bind_mount_string} {config['singularity_image']} {command}
"""
    return slurm_content


def run_singularity_with_slurm_shared_options(config_path: str, slurm_options: str = "") -> None:
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

    print(f"\n🧬 Submitting Ray tuner SLURM job (after PySpark job {job_id})...")
    subprocess.run(["sbatch", "./containers/temp_ray.slurm"], check=True)

    # Clean up temporary files
    os.remove("./containers/temp_pyspark.slurm")
    os.remove("./containers/temp_ray.slurm")


def run_singularity_slurm_pyspark_only(config_path: str, slurm_options: str = "") -> None:
    print("\n🧬 Submitting PySpark SLURM job only...")

    pyspark_slurm_content = create_slurm_script("pyspark", config_path, slurm_options)

    with open("./containers/temp_pyspark.slurm", "w") as f:
        f.write(pyspark_slurm_content)

    subprocess.run(["sbatch", "./containers/temp_pyspark.slurm"], check=True)

    # Clean up temporary file
    os.remove("./containers/temp_pyspark.slurm")


def run_singularity_slurm_ray_only(config_path: str, slurm_options: str = "") -> None:
    print("\n�� Submitting Ray tuner SLURM job only...")

    ray_slurm_content = create_slurm_script("ray", config_path, slurm_options)

    with open("./containers/temp_ray.slurm", "w") as f:
        f.write(ray_slurm_content)

    subprocess.run(["sbatch", "./containers/temp_ray.slurm"], check=True)

    # Clean up temporary file
    os.remove("./containers/temp_ray.slurm")


# =============================================================================
# CONTAINER BUILDING FUNCTIONS
# =============================================================================


def check_and_build_sif_files(config: Dict[str, Any], pipeline_mode: str, use_slurm: bool = False) -> None:
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
            ("eeg-pyspark.sif", "docker://nour333/eeg-spark-pipeline:latest", "pyspark")
        )
    if pipeline_mode in ["ray-only", "full"]:
        containers_to_check.append(
            ("eeg-ray-tuner.sif", "docker://nour333/eeg-ray-tuner:latest", "ray")
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


def build_sif_with_slurm(sif_name: str, docker_uri: str, job_prefix: str, slurm_options: str = "") -> None:
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
