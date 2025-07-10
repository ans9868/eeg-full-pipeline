import os
import subprocess
import sys
import yaml
from pathlib import Path
from datetime import datetime

def check_config(specific_config=None):
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
    config_files = list(config_dir.glob("config_*.yaml"))
    if not config_files:
        print(f"❌ No config files found in {config_dir}")
        print("Run config-maker.py first to create a configuration file.")
        sys.exit(1)
    
    # Sort by modification time (most recent first)
    config_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    most_recent = config_files[0]
    
    print(f"📁 Using most recent config: {most_recent.name}")
    if len(config_files) > 1:
        print(f"📋 Available configs: {[f.name for f in config_files]}")
    
    return str(most_recent.resolve())

def load_config(config_path):
    """Load the configuration file to determine deployment method."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def run_docker(config_path):
    print("\n🐳 Running PySpark container...")
    subprocess.run([
        "docker", "run", "--rm",
        "-v", f"{config_path}:/app/config.yaml",
        "nour333/eeg-spark-pipeline:latest"
    ], check=True)

    print("\n🐳 Running Ray tuner container...")
    subprocess.run([
        "docker", "run", "--rm",
        "-v", f"{config_path}:/app/config.yaml",
        "nour333/eeg-ray-tuner:latest"
    ], check=True)

def run_singularity_without_slurm(config_path):
    print("\n🔒 Running PySpark Singularity container...")
    subprocess.run([
        "singularity", "run",
        "--bind", f"{config_path}:/app/config.yaml",
        "eeg-pyspark.sif",
        "--config", "/app/config.yaml"
    ], check=True)

    print("\n🔒 Running Ray tuner Singularity container...")
    subprocess.run([
        "singularity", "run",
        "--bind", f"{config_path}:/app/config.yaml",
        "eeg-ray-tuner.sif",
        "--config", "/app/config.yaml"
    ], check=True)

def run_singularity_with_slurm(config_path, slurm_options=""):
    print("\n🧬 Submitting PySpark SLURM job...")
    
    # Create temporary SLURM script with custom options
    pyspark_slurm_content = f"""#!/bin/bash
#SBATCH {slurm_options}
#SBATCH --job-name=eeg-pyspark
#SBATCH --output=pyspark_%j.out
#SBATCH --error=pyspark_%j.err

singularity run --bind {config_path}:/app/config.yaml eeg-pyspark.sif --config /app/config.yaml
"""
    
    # Create temporary SLURM script with custom options (overwrite if exists)
    with open("temp_pyspark.slurm", "w") as f:
        f.write(pyspark_slurm_content)
    
    pyspark_submit = subprocess.run(["sbatch", "temp_pyspark.slurm"], capture_output=True, text=True)
    print(pyspark_submit.stdout.strip())

    # Extract job ID
    try:
        job_id = pyspark_submit.stdout.strip().split()[-1]
    except IndexError:
        print("❌ Failed to get job ID from sbatch output.")
        sys.exit(1)

    # Create temporary SLURM script for Ray with dependency (overwrite if exists)
    ray_slurm_content = f"""#!/bin/bash
#SBATCH {slurm_options}
#SBATCH --job-name=eeg-ray-tuner
#SBATCH --output=ray_%j.out
#SBATCH --error=ray_%j.err
#SBATCH --dependency=afterok:{job_id}

singularity run --bind {config_path}:/app/config.yaml eeg-ray-tuner.sif --config /app/config.yaml
"""
    
    with open("temp_ray.slurm", "w") as f:
        f.write(ray_slurm_content)

    print(f"\n🧬 Submitting Ray tuner SLURM job (after PySpark job {job_id})...")
    subprocess.run(["sbatch", "temp_ray.slurm"], check=True)
    
    # Clean up temporary files
    os.remove("temp_pyspark.slurm")
    os.remove("temp_ray.slurm")

def main():
    # Check if a specific config file was provided as command line argument
    specific_config = sys.argv[1] if len(sys.argv) > 1 else None
    
    config_path = check_config(specific_config)
    config = load_config(config_path)
    
    # Get deployment method from config
    deployment_method = config.get("project", {}).get("deployment_method", "Docker")
    
    print(f"🚀 Starting pipeline with deployment method: {deployment_method}")
    
    if deployment_method == "Docker":
        run_docker(config_path)
    elif deployment_method == "Singularity without Slurm":
        run_singularity_without_slurm(config_path)
    elif deployment_method == "Singularity with Slurm":
        slurm_options = config.get("project", {}).get("slurm_options", "")
        run_singularity_with_slurm(config_path, slurm_options)
    else:
        print(f"❌ Unknown deployment method: {deployment_method}")
        print("Supported methods: Docker, Singularity with Slurm, Singularity without Slurm")
        sys.exit(1)

if __name__ == "__main__":
    main()
