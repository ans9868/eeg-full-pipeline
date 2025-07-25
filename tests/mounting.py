#!/usr/bin/env python3
"""
Test script to verify data directory mounting functionality.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple

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
    
    # Add output directory
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
        mount_mappings.append((output_dir, output_dir))
    
    return mount_mappings

def test_mounting():
    """Test the mounting functionality with the sample config."""
    
    # Change to project root directory (parent of tests directory)
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Changed working directory to: {os.getcwd()}")
    
    # Load the sample config
    config_path = "eeg-pyspark-pipeline/config/config_pathstest_22-07-2025_1439.yaml"
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Get mount mappings
    mount_mappings = get_data_directories_to_mount(config)
    
    print("🔍 Testing data directory mounting functionality...")
    print(f"📁 Found {len(mount_mappings)} directories to mount:")
    
    # Show first few directories (including output directory which is first)
    show_count = min(5, len(mount_mappings))
    for i, (host_path, container_path) in enumerate(mount_mappings[:show_count], 1):
        print(f"   {i}. {host_path} -> {container_path}")
    
    if len(mount_mappings) > show_count:
        print(f"   ... and {len(mount_mappings) - show_count} more directories")
    
    # Verify that we found the expected directories
    expected_data_dir = "/Users/user/bigData/ds004504-download"
    found_expected_data = any(expected_data_dir in host_path for host_path, _ in mount_mappings)
    
    if found_expected_data:
        print(f"✅ Successfully found expected data directory pattern: {expected_data_dir}")
    else:
        print(f"❌ Expected data directory pattern not found: {expected_data_dir}")
    
    # Check output directory (should be first in the list)
    expected_output_dir = str(Path.cwd() / "data")
    found_expected_output = mount_mappings and mount_mappings[0][0] == expected_output_dir
    
    if found_expected_output:
        print(f"✅ Successfully found expected output directory (first): {expected_output_dir}")
    else:
        print(f"❌ Expected output directory not found at first position: {expected_output_dir}")
    
    # Show what the Docker command would look like
    print("\n🐳 Example Docker command would be:")
    docker_cmd = ["docker", "run", "--rm", "-v", f"{config_path}:/app/config.yaml"]
    for host_path, container_path in mount_mappings:
        docker_cmd.extend(["-v", f"{host_path}:{container_path}"])
    docker_cmd.extend(["your-image", "your-command"])
    
    print(" ".join(docker_cmd))
    
    # Show what the Singularity command would look like
    print("\n🔒 Example Singularity command would be:")
    bind_mounts = [f"{config_path}:/app/config.yaml"]
    for host_path, container_path in mount_mappings:
        bind_mounts.append(f"{host_path}:{container_path}")
    bind_mount_string = ",".join(bind_mounts)
    
    singularity_cmd = f"singularity run --bind {bind_mount_string} your-image.sif your-command"
    print(singularity_cmd)

if __name__ == "__main__":
    test_mounting() 