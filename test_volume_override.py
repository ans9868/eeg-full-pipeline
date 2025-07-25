#!/usr/bin/env python3
"""Test the volume override logic."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from start_pipelines import CONTAINER_CONFIG, build_user_mounts, get_all_mount_mappings

def test_volume_override():
    """Test that user config can override default ./data volume."""
    
    # Test config with user output_dir
    test_config_with_output = {
        'project': {
            'output_dir': './my_custom_output'
        },
        'data_input': {
            'groups': {
                'test_group': ['/path/to/file1.txt', '/path/to/file2.txt']
            }
        }
    }
    
    # Test config without user output_dir
    test_config_no_output = {
        'data_input': {
            'groups': {
                'test_group': ['/path/to/file1.txt', '/path/to/file2.txt']
            }
        }
    }
    
    print('✅ Testing volume override logic...')
    
    print('\n1. With user output_dir:')
    mounts_with_output = get_all_mount_mappings('pyspark', './config.yaml', test_config_with_output)
    data_volumes = [m for m in mounts_with_output if '/app/data' in m[1]]
    print(f'   Data volumes: {data_volumes}')
    
    print('\n2. Without user output_dir:')
    mounts_without_output = get_all_mount_mappings('pyspark', './config.yaml', test_config_no_output)
    data_volumes = [m for m in mounts_without_output if '/app/data' in m[1]]
    print(f'   Data volumes: {data_volumes}')
    
    # Verify the logic
    has_default_data = any('./data' in m[0] for m in mounts_without_output)
    has_custom_output = any('my_custom_output' in m[0] for m in mounts_with_output)
    
    print(f'\n✅ Default ./data volume present when no user output: {has_default_data}')
    print(f'✅ Custom output volume present when user specifies output: {has_custom_output}')
    
    return has_default_data and has_custom_output

if __name__ == "__main__":
    test_volume_override() 