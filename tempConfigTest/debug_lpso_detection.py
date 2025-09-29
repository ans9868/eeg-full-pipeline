#!/usr/bin/env python3

import sys
import os
sys.path.append('.')
sys.path.append('eeg-ray-tuner')

# Write debug output to file
with open('debug_lpso_detection.txt', 'w') as f:
    f.write("Starting LPSO detection debug...\n")
    
    try:
        from config_handler import UnifiedConfigHandler
        f.write("Config handler imported\n")
        
        from eeg_ray_tuner.visualization import GraphGenerator
        f.write("Graph generator imported\n")
        
        # Test detection logic
        config_handler = UnifiedConfigHandler('data/demo1/config_20250929_021918.yaml')
        f.write("Config loaded\n")
        
        # Check config properties
        f.write(f"Data leakage strategy: {getattr(config_handler, 'data_leakage_strategy', 'NOT_FOUND')}\n")
        
        # Check ray config
        ray_config = config_handler.get_ray_config()
        f.write(f"Ray config: {ray_config}\n")
        f.write(f"Use LPSO: {ray_config.get('use_lpso', 'NOT_FOUND')}\n")
        
        # Test detection
        graph_generator = GraphGenerator(config_handler, 'data/demo1/ml_results')
        f.write("Graph generator created\n")
        
        split_type = graph_generator._detect_split_type()
        f.write(f"Detected split type: {split_type}\n")
        
        # Test graph generation
        f.write("Testing graph generation...\n")
        graph_generator.generate_graphs()
        f.write("Graph generation completed!\n")
        
        # Check results
        graphs_dir = 'data/demo1/ml_results/graphs'
        if os.path.exists(graphs_dir):
            f.write(f"Graphs created: {os.listdir(graphs_dir)}\n")
        else:
            f.write("No graphs directory created\n")
            
    except Exception as e:
        f.write(f"Error: {e}\n")
        import traceback
        f.write(traceback.format_exc())
    
    f.write("Debug completed\n")

print("Debug output written to debug_lpso_detection.txt")
