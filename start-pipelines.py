import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import yaml

# =============================================================================
# EMOJI CONSTANTS - Consistent messaging
# =============================================================================

# Status emojis
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_WARNING = "⚠️"
EMOJI_INFO = "💡"
EMOJI_DEBUG = "🔍"

# Action emojis
EMOJI_RUNNING = "🚀"
EMOJI_BUILDING = "🔨"
EMOJI_WAITING = "⏳"
EMOJI_SUBMITTING = "🧬"
EMOJI_MOUNTING = "🔗"
EMOJI_CREATING = "📁"

# Container emojis
EMOJI_DOCKER = "🐳"
EMOJI_SINGULARITY = "🔒"

# UI emojis
EMOJI_TARGET = "🎯"
EMOJI_LIST = "📋"
EMOJI_CHART = "📊"
EMOJI_SIZE = "📏"
EMOJI_WEB = "🌐"

# =============================================================================

# Configuration constants - edit these to change paths/commands
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
            (
                "./config/spark",
                "/opt/bitnami/spark/conf",
            ),  # Spark configs (editable) - removing this puts spark logs in console
            ("./logs/spark-events", "/opt/bitnami/spark/logs/"),  # Spark event logs
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
        "entrypoint": "/app/test-ray.py",
        "command": "python",
        "job_name": "ray-tuner",
        "mounts": [
            # TODO ray logs and ray config
            # Done through config file
            # (f"./config/{user_config_namec}", "/app/config"),   # User YAML configs (editable)
            # ("./data", "/app/data"),
        ],
        # "ports": [ # TODO: add ray ports if needed]
    },
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def check_config(specific_config: Optional[str] = None) -> str:
    """Check for config file and return the path to the most recent one or specified one."""
    config_dir = Path("config")

    if not config_dir.exists():
        print(f"{EMOJI_ERROR} Config directory not found at {config_dir}")
        sys.exit(1)

    if specific_config:
        # 3-tier lookup: config_dir -> relative path -> absolute path
        for config_path in [
            config_dir / specific_config,
            Path(specific_config),
            Path(specific_config).resolve(),
        ]:
            if config_path.exists():
                print(f"{EMOJI_CREATING} Using specified config: {config_path}")
                return str(config_path.resolve())
        print(f"{EMOJI_ERROR} Specified config file not found: {specific_config}")
        sys.exit(1)

    # Find the most recent config file
    # Config files are named as config_<projectname>_<day-month-year>_<HHMM>.yaml
    config_files = list(config_dir.glob("config_*.yaml"))
    if not config_files:
        print(f"{EMOJI_ERROR} No config files found in {config_dir}")
        print(
            "Run config-maker.py first to create a configuration file (format: config_<projectname>_<day-month-year>_<HHMM>.yaml)."
        )
        sys.exit(1)

    # Sort by modification time (most recent first)
    config_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    most_recent = config_files[0]

    print(f"{EMOJI_CREATING} Using most recent config: {most_recent.name}")
    if len(config_files) > 1:
        print(
            f"{EMOJI_LIST} Available configs: {[f.name for f in config_files]} (format: config_<projectname>_<day-month-year>_<HHMM>.yaml)"
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
    )  # no .resolve() # since soft link, if resolved then would get eeg-full-pipeline directory and would get incorrect parent directory
    repo_name = this_path.parent.name

    if repo_name == "eeg-pyspark-pipeline":
        return "pyspark-only"
    elif repo_name == "eeg-ray-tuner":  # TODO: add ray-only
        return "ray-only"
    elif repo_name == "eeg-full-pipeline":
        return "full"
    else:
        raise ValueError(
            f"Invalid repo name: {repo_name}. Please run this script from the root of the repository who's directory name is one of the following: (eeg-full-pipeline, eeg-ray-tuner, eeg-pyspark-pipeline)."
        )


def create_required_directories(output_dir: str = "./data") -> None:
    """Create required directories for the pipeline."""
    # Convert relative path to absolute if needed
    if output_dir.startswith("./"):
        output_dir = str(Path.cwd() / output_dir[2:])
    elif output_dir.startswith("."):
        output_dir = str(Path.cwd() / output_dir[1:])

    directories = [
        "config",
        "config/spark",
        # config/ray
        "logs",
        "logs/spark-events",
        # logs/ray-events
        output_dir,
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"{EMOJI_CREATING} Created/verified directory: {directory}")


def print_spark_ui_instructions() -> None:
    """Print instructions for accessing Spark UI on HPC."""
    # TODO: NECESSARY FOR LATER - Uncomment when Spark UI access is needed
    # print("\n" + "="*60)
    # print("🌐 SPARK UI ACCESS INSTRUCTIONS")
    # print("="*60)
    # print("To access Spark UI from your local machine:")
    # print()
    # print("1. Find your compute node:")
    # print("   squeue -u $USER -o '%.18i %.9P %.20j %.8u %.2t %.10M %.6D %R'")
    # print()
    # print("2. Create SSH tunnel from your local machine:")
    # print("   ssh -L 4040:COMPUTE_NODE:4040 USERNAME@LOGIN_NODE")
    # print()
    # print("3. Access Spark UI in your browser:")
    # print("   http://localhost:4040")
    # print()
    # print("4. Alternative: Use port forwarding in your SLURM script:")
    # print("   Add '--bind 4040:4040' to singularity run command")
    # print("="*60)
    pass  # Placeholder for future use


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
                            print(
                                f"{EMOJI_MOUNTING} Adding mount: {file_path} -> {file_path}"
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

    # Get output directory from config or use default
    output_dir = config_data.get("project", {}).get("output_dir", "./data")

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


def run_docker_container(container_type: str, config_path: str) -> None:
    """Run a single Docker container."""
    config = CONTAINER_CONFIG[container_type]
    command_parts = get_container_command(container_type, config_path).split()

    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_all_mount_mappings(container_type, config_path, config_data)

    # Build docker run command with volume mounts
    docker_cmd = ["docker", "run", "--rm"]

    # !! All Spark and Hadoop configurations are now centralized in session_builder.py

    # But LD_PRELOAD is still needed for nss_wrapper in Docker - moved to Dockerfile
    # docker_cmd.extend(["-e", "LD_PRELOAD=/opt/bitnami/common/lib/libnss_wrapper.so"])

    # Add port mappings for pyspark container

    ports = config.get("ports", [])
    for port_mapping in ports:
        docker_cmd.extend(["-p", port_mapping])

    # Add volume mounts
    for host_path, container_path in mount_mappings:
        docker_cmd.extend(["-v", f"{host_path}:{container_path}"])

    # Add image and command
    docker_cmd.extend([config["docker_image"]] + command_parts)

    print(f"{EMOJI_MOUNTING} Mounting {len(mount_mappings)} directories:")

    print(f"{EMOJI_MOUNTING} Running command: {docker_cmd}")

    try:
        subprocess.run(docker_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n{EMOJI_ERROR} Docker command failed with exit code {e.returncode}")

        # Check for common Docker mount errors
        if "operation not permitted" in str(e).lower() or "mkdir" in str(e).lower():
            print(f"\n{EMOJI_DEBUG} Most likely causes:")
            print("   1. Docker doesn't have full disk access")
            print(
                "   2. Docker doesn't have permission to access the specified files/directories"
            )
            print("   3. The files/directories don't exist")
            print(f"\n{EMOJI_INFO} Solutions:")
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
            print(
                f"\n{EMOJI_DEBUG} Most likely cause: One or more files/directories don't exist"
            )
            print(
                f"\n{EMOJI_INFO} Solution: Check that all paths in your config file exist"
            )
        if "permission denied" in str(e).lower():
            print(
                f"\n{EMOJI_DEBUG} Most likely cause: Permission denied accessing files/directories"
            )
            print(f"\n{EMOJI_INFO} Solutions:")
            print("   • Check file permissions on the mounted directories")
            print("   • Ensure Docker has permission to access the files")
            print("   • On macOS: Check Docker's Full Disk Access permissions")

        print(f"\n{EMOJI_DEBUG} Error details: {e}")

        print(f"\n{EMOJI_LIST} Full error output:")
        if e.stdout:
            print(f"STDOUT: {e.stdout.decode()}")
        if e.stderr:
            print(f"STDERR: {e.stderr.decode()}")

        sys.exit(1)
    except FileNotFoundError:
        print(f"\n{EMOJI_ERROR} Docker command not found")
        print(
            f"{EMOJI_INFO} Please ensure Docker is installed and available in your PATH"
        )
        sys.exit(1)


def run_singularity_container(container_type: str, config_path: str) -> None:
    """Run a single Singularity container."""
    config = CONTAINER_CONFIG[container_type]
    command_parts = get_container_command(container_type, config_path).split()

    # Load config to get data directories
    config_data = load_config(config_path)
    mount_mappings = get_all_mount_mappings(container_type, config_path, config_data)

    # Build singularity run command with bind mounts
    # Fix Singularity auto-mount issues that can hide container files and cause authentication problems
    # --no-mount tmp: prevents host /tmp from hiding container /tmp contents
    # --cleanenv: provides clean environment to avoid host OS conflicts
    # --writable-tmpfs: ensures writable temp space for Spark/Hadoop operations
    # Note: --net disabled because iptables not available on this system
    # Note: --fakeroot not available on this HPC system due to missing /etc/subuid configuration
    singularity_cmd = [
        "singularity",
        "run",
        "--no-mount",
        "tmp",
        "--cleanenv",
        "--writable-tmpfs",
    ]
    # Let the container's entrypoint.sh and session_builder.py handle user detection dynamically
    # Only set essential environment variables that don't conflict with dynamic logic
    singularity_cmd.extend(
        [
            "--env",
            "HADOOP_CONF_DIR=/tmp",
            "--env",
            "HADOOP_HOME=/tmp",
            # Note: We REMOVE -Djava.security.manager= as it enables security manager instead of disabling it
            "--env",
            "JAVA_TOOL_OPTIONS=-Djava.security.auth.login.config= -Dhadoop.security.authentication=simple -Dhadoop.security.authorization=false",
        ]
    )

    # Add user database bind mounts to help resolve Unix user resolution issues
    # Even with --cleanenv, we need the container to know about the current user
    singularity_cmd.extend(
        ["--bind", "/etc/passwd:/etc/passwd:ro", "--bind", "/etc/group:/etc/group:ro"]
    )

    # Add bind mounts
    for host_path, container_path in mount_mappings:
        singularity_cmd.extend(["--bind", f"{host_path}:{container_path}"])

    # Add port mappings - not needed for singularity as done automatically - https://stackoverflow.com/questions/47297645/binding-ports-when-running-docker-images-in-singularity -
    # ports = config.get("ports", [])
    # for port_mapping in ports:
    #     singularity_cmd.extend(["--bind", f"0.0.0.0:{port_mapping.split(':')[0]}:{port_mapping.split(':')[1]}"])

    # Add image and command
    singularity_cmd.extend([config["singularity_image"]] + command_parts)

    print(f"🔗 Mounting {len(mount_mappings)} directories:")

    print(f"🔗 Running command: {singularity_cmd}")
    print(
        f"{EMOJI_RUNNING} Starting {container_type} container... (this may take a while)"
    )

    try:
        # Use real-time output instead of silent execution
        import queue
        import threading

        # Create a queue for capturing output
        output_queue = queue.Queue()

        def capture_output(pipe, queue_obj, prefix=""):
            """Capture output from subprocess and put it in queue"""
            for line in iter(pipe.readline, ""):
                if line:
                    queue_obj.put(f"{prefix}{line}")
            pipe.close()

        # Start the subprocess with real-time output
        process = subprocess.Popen(
            singularity_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Start threads to capture stdout and stderr
        stdout_thread = threading.Thread(
            target=capture_output, args=(process.stdout, output_queue, "")
        )
        stderr_thread = threading.Thread(
            target=capture_output, args=(process.stderr, output_queue, "")
        )

        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()

        # Process output in real-time
        while process.poll() is None or not output_queue.empty():
            try:
                line = output_queue.get(timeout=0.1)
                # Print with appropriate emoji indicators
                if "INFO:" in line:
                    print(f"{EMOJI_INFO} {line.strip()}")
                elif "WARNING:" in line:
                    print(f"{EMOJI_WARNING} {line.strip()}")
                elif "ERROR:" in line or "FATAL:" in line:
                    print(f"{EMOJI_ERROR} {line.strip()}")
                elif "Converting SIF" in line or "Mounting" in line:
                    print(f"{EMOJI_MOUNTING} {line.strip()}")
                elif line.strip():
                    print(f"{EMOJI_RUNNING} {line.strip()}")

            except queue.Empty:
                continue

        # Wait for threads to finish
        stdout_thread.join(timeout=1)
        stderr_thread.join(timeout=1)

        # Check return code
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, singularity_cmd)
        else:
            print(
                f"\n{EMOJI_SUCCESS} {container_type.capitalize()} container completed successfully!"
            )

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
    print(f"\n{EMOJI_DOCKER} Running PySpark container only...")
    run_docker_container("pyspark", config_path)


def run_docker_ray_only(config_path: str) -> None:
    print(f"\n{EMOJI_DOCKER} Running Ray pipeline container only...")
    run_docker_container("ray", config_path)


def run_docker(config_path: str) -> None:
    print(f"\n{EMOJI_DOCKER} Running PySpark container...")
    run_docker_container("pyspark", config_path)

    print(f"\n{EMOJI_DOCKER} Running Ray pipeline container...")
    run_docker_container("ray", config_path)


# =============================================================================
# SINGULARITY EXECUTION FUNCTIONS
# =============================================================================


def run_singularity_pyspark_only(config_path: str) -> None:
    print(f"\n{EMOJI_SINGULARITY} Running PySpark Singularity container only...")
    run_singularity_container("pyspark", config_path)


def run_singularity_ray_only(config_path: str) -> None:
    print(f"\n{EMOJI_SINGULARITY} Running Ray pipeline Singularity container only...")
    run_singularity_container("ray", config_path)


def run_singularity_without_slurm(config_path: str) -> None:
    print(f"\n{EMOJI_SINGULARITY} Running PySpark Singularity container...")
    run_singularity_container("pyspark", config_path)

    print(f"\n{EMOJI_SINGULARITY} Running Ray pipeline Singularity container...")
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


def run_singularity_slurm_pyspark_only(
    config_path: str, slurm_options: str = ""
) -> None:
    print(f"\n{EMOJI_SUBMITTING} Submitting PySpark SLURM job only...")

    pyspark_slurm_content = create_slurm_script("pyspark", config_path, slurm_options)

    with open("./containers/temp_pyspark.slurm", "w") as f:
        f.write(pyspark_slurm_content)

    subprocess.run(["sbatch", "./containers/temp_pyspark.slurm"], check=True)

    # Clean up temporary file
    os.remove("./containers/temp_pyspark.slurm")


def run_singularity_slurm_ray_only(config_path: str, slurm_options: str = "") -> None:
    print(f"\n{EMOJI_SUBMITTING} Submitting Ray pipeline SLURM job only...")

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

    # Define which containers are needed for each pipeline mode
    pipeline_containers = {
        "pyspark-only": ["pyspark"],
        "ray-only": ["ray"],
        "full": ["pyspark", "ray"],
    }

    # Get containers needed for this pipeline mode
    needed_containers = pipeline_containers.get(pipeline_mode, [])

    # Build container list
    for container_type in needed_containers:
        sif_name = f"eeg-{container_type}-{'pipeline' if container_type == 'pyspark' else 'tuner'}.sif"
        containers_to_check.append(
            (
                sif_name,
                CONTAINER_CONFIG[container_type]["docker_image"],
                container_type,
            )
        )

    # Check and build each required container
    print(f"{EMOJI_INFO} Checking for required container images...")
    for sif_name, docker_uri, build_type in containers_to_check:
        sif_path = Path(f"./containers/{sif_name}")
        if sif_path.exists():
            size_mb = sif_path.stat().st_size / (1024 * 1024)
            print(
                f"{EMOJI_SUCCESS} Found {build_type} container: {sif_name} ({size_mb:.1f} MB)"
            )
        else:
            print(
                f"{EMOJI_BUILDING} {build_type.capitalize()} .sif file not found: {sif_name}"
            )
            print(f"{EMOJI_INFO} Will build from: docker://{docker_uri}")
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
        print(f"\n{EMOJI_WAITING} Waiting for container builds to complete...")
        print(f"{EMOJI_INFO} You can check build status with: squeue -u $USER")
        print(f"{EMOJI_INFO} Build logs are in ./containers/ directory")

        # Wait for .sif files to appear
        max_wait_time = 1800  # 30 minutes
        wait_interval = 10  # 10 seconds
        waited_time = 0

        while waited_time < max_wait_time:
            all_built = all(
                Path(f"./containers/{sif_name}").exists()
                for sif_name, _, _ in containers_to_check
            )
            if all_built:
                print(f"{EMOJI_SUCCESS} All container builds completed!")
                break
            time.sleep(wait_interval)
            waited_time += wait_interval
            print(
                f"{EMOJI_WAITING} Still waiting for builds... ({waited_time}s elapsed)"
            )

        if not all(
            Path(f"./containers/{sif_name}").exists()
            for sif_name, _, _ in containers_to_check
        ):
            print(f"{EMOJI_ERROR} Timeout waiting for container builds to complete")
            print(f"{EMOJI_INFO} Check build logs in ./containers/ directory")

            # Show status of each container
            print(f"\n{EMOJI_CHART} Build status:")
            for sif_name, _, build_type in containers_to_check:
                sif_path = Path(f"./containers/{sif_name}")
                if sif_path.exists():
                    size_mb = sif_path.stat().st_size / (1024 * 1024)
                    print(f"   {EMOJI_SUCCESS} {sif_name} ({size_mb:.1f} MB)")
                else:
                    print(f"   {EMOJI_ERROR} {sif_name} (not found)")

                    # Check for log files
                    log_pattern = f"./containers/{build_type}_build_*.err"
                    import glob

                    error_logs = glob.glob(log_pattern)
                    if error_logs:
                        print(f"      {EMOJI_CREATING} Error logs: {error_logs}")

            sys.exit(1)


def build_sif_with_slurm(
    sif_name: str, docker_uri: str, job_prefix: str, slurm_options: str = ""
) -> None:
    """Build .sif file using SLURM job."""
    print(f"{EMOJI_SUBMITTING} Submitting SLURM job to build {sif_name}...")
    print(f"{EMOJI_DEBUG} Source: docker://{docker_uri}")
    print(f"{EMOJI_TARGET} Target: ./containers/{sif_name}")
    print(
        f"{EMOJI_INFO} SLURM options: {slurm_options if slurm_options else 'default'}"
    )

    # Create SLURM script for building
    build_slurm_content = f"""#!/bin/bash
#SBATCH {slurm_options}
#SBATCH --job-name={job_prefix}
#SBATCH --output=./containers/{job_prefix}_%j.out
#SBATCH --error=./containers/{job_prefix}_%j.err

set -e  # Exit on any error
echo "=== Starting build of {sif_name} ==="
echo "Source: docker://{docker_uri}"
echo "Target: ./containers/{sif_name}"
echo "Timestamp: $(date)"

# Check if singularity is available
if ! command -v singularity &> /dev/null; then
    echo "ERROR: singularity command not found"
    exit 1
fi

# Check if we can access the containers directory
if [ ! -d "./containers" ]; then
    echo "ERROR: ./containers directory not found"
    exit 1
fi

echo "Building {sif_name} from docker://{docker_uri}..."
if singularity build ./containers/{sif_name} docker://{docker_uri}; then
    echo "=== SUCCESS: Build completed for {sif_name} ==="
    echo "Timestamp: $(date)"
    ls -la ./containers/{sif_name}
else
    echo "=== FAILED: Build failed for {sif_name} ==="
    echo "Timestamp: $(date)"
    exit 1
fi
"""

    # Write SLURM script to containers directory
    slurm_script_path = f"./containers/{job_prefix}.slurm"
    with open(slurm_script_path, "w") as f:
        f.write(build_slurm_content)

    # Submit SLURM job
    try:
        result = subprocess.run(
            ["sbatch", slurm_script_path], capture_output=True, text=True, check=True
        )
        print(f"{EMOJI_SUCCESS} SLURM build job submitted for {sif_name}")
        print(f"{EMOJI_LIST} Job output: {result.stdout.strip()}")
        print(f"{EMOJI_CREATING} Logs will be saved in ./containers/")
        print(
            f"{EMOJI_INFO} Monitor with: tail -f ./containers/{job_prefix}_*.out ./containers/{job_prefix}_*.err"
        )
        print(
            f"{EMOJI_WAITING} Please wait for the build to complete before running the pipeline."
        )
    except subprocess.CalledProcessError as e:
        print(f"{EMOJI_ERROR} Failed to submit SLURM job for {sif_name}")
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        sys.exit(1)


def build_sif_locally(sif_name: str, docker_uri: str, build_type: str) -> None:
    """Build .sif file locally."""
    print(f"{EMOJI_BUILDING} Building {sif_name} locally from docker://{docker_uri}...")

    # Create log file
    log_file = f"./containers/{build_type}_build.log"

    try:
        # Check if singularity is available
        subprocess.run(["singularity", "--version"], check=True, capture_output=True)

        # Check if containers directory exists
        containers_dir = Path("./containers")
        containers_dir.mkdir(exist_ok=True)

        print(f"{EMOJI_CREATING} Build log will be saved to: {log_file}")
        print(f"{EMOJI_DEBUG} Source: docker://{docker_uri}")
        print(f"{EMOJI_TARGET} Target: ./containers/{sif_name}")
        print(
            f"{EMOJI_BUILDING} Starting build process... (this may take several minutes)"
        )

        # Build the .sif file with real-time output to both console and log
        import queue
        import threading
        from io import StringIO

        # Create a queue for capturing output
        output_queue = queue.Queue()

        def capture_output(pipe, queue_obj, prefix=""):
            """Capture output from subprocess and put it in queue"""
            for line in iter(pipe.readline, ""):
                if line:
                    queue_obj.put(f"{prefix}{line}")
            pipe.close()

        # Start the subprocess
        process = subprocess.Popen(
            [
                "singularity",
                "build",
                f"./containers/{sif_name}",
                f"docker://{docker_uri}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Start threads to capture stdout and stderr
        stdout_thread = threading.Thread(
            target=capture_output, args=(process.stdout, output_queue, "")
        )
        stderr_thread = threading.Thread(
            target=capture_output, args=(process.stderr, output_queue, "")
        )

        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()

        # Open log file for writing
        with open(log_file, "w") as log:
            log.write(f"=== Starting build of {sif_name} ===\n")
            log.write(f"Source: docker://{docker_uri}\n")
            log.write(f"Target: ./containers/{sif_name}\n")
            log.write(f"Timestamp: {datetime.now()}\n\n")
            log.flush()

            # Process output in real-time
            while process.poll() is None or not output_queue.empty():
                try:
                    line = output_queue.get(timeout=0.1)
                    # Print to console with emoji indicators
                    if "INFO:" in line or "Writing" in line:
                        print(f"{EMOJI_INFO} {line.strip()}")
                    elif "ERROR:" in line or "FATAL:" in line:
                        print(f"{EMOJI_ERROR} {line.strip()}")
                    elif "WARNING:" in line:
                        print(f"{EMOJI_WARNING} {line.strip()}")
                    elif line.strip():
                        print(f"{EMOJI_BUILDING} {line.strip()}")

                    # Also write to log file
                    log.write(line)
                    log.flush()

                except queue.Empty:
                    continue

            # Wait for threads to finish
            stdout_thread.join(timeout=1)
            stderr_thread.join(timeout=1)

            # Get the final return code
            result = process

        if result.returncode == 0:
            print(f"{EMOJI_SUCCESS} Successfully built {sif_name}")
            print(f"{EMOJI_CREATING} Build log saved to {log_file}")
            # Show file size
            sif_path = Path(f"./containers/{sif_name}")
            if sif_path.exists():
                size_mb = sif_path.stat().st_size / (1024 * 1024)
                print(f"{EMOJI_SIZE} File size: {size_mb:.1f} MB")
        else:
            print(f"{EMOJI_ERROR} Failed to build {sif_name}")
            print(f"{EMOJI_CREATING} Check build log at {log_file}")
            # Show last few lines of log for debugging
            try:
                with open(log_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        print(f"{EMOJI_LIST} Last 10 lines of build log:")
                        for line in lines[-10:]:
                            print(f"   {line.rstrip()}")
            except Exception as log_e:
                print(f"{EMOJI_WARNING} Could not read log file: {log_e}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"{EMOJI_ERROR} Singularity command failed: {e}")
        print(f"{EMOJI_INFO} Make sure Singularity is installed and available in PATH")
        sys.exit(1)
    except Exception as e:
        print(f"{EMOJI_ERROR} Error building {sif_name}: {e}")
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

    print(
        f"{EMOJI_RUNNING} Starting pipeline with deployment method: {deployment_method}"
    )
    print(f"{EMOJI_TARGET} Pipeline mode: {pipeline_mode}")

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
            # TODO: NECESSARY FOR LATER - Uncomment when Spark UI access is needed
            # print_spark_ui_instructions()
        elif pipeline_mode == "ray-only":
            slurm_options = config.get("project", {}).get("slurm_options_ray", "")
            run_singularity_slurm_ray_only(config_path, slurm_options)
        else:  # full
            pyspark_slurm = config.get("project", {}).get("slurm_options_pyspark", "")
            ray_slurm = config.get("project", {}).get("slurm_options_ray", "")
            run_singularity_with_slurm_separate_options(
                config_path, pyspark_slurm, ray_slurm
            )
            # TODO: NECESSARY FOR LATER - Uncomment when Spark UI access is needed
            # print_spark_ui_instructions()
    else:
        print(f"{EMOJI_ERROR} Unknown deployment method: {deployment_method}")
        print(
            "Supported methods: Docker, Singularity with Slurm, Singularity without Slurm"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
