#!/usr/bin/env python3

import sys
import os
sys.path.append('.')
sys.path.append('eeg-ray-tuner')

# Write debug output to file
with open('debug_detection_output.txt', 'w') as f:
    f.write("Starting detection debug...\n")
    
    try:
        from config_handler import UnifiedConfigHandler
        f.write("Config handler imported\n")
        
        from eeg_ray_tuner.visualization import GraphGenerator
        f.write("Graph generator imported\n")
        
        # Test detection logic
        config_handler = UnifiedConfigHandler('data/demo1/config_20250929_014424.yaml')
        f.write("Config loaded\n")
        
        graph_generator = GraphGenerator(config_handler, 'data/demo1/ml_results')
        f.write("Graph generator created\n")
        
        # Test detection
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

print("Debug output written to debug_detection_output.txt")
