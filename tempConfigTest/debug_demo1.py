#!/usr/bin/env python3

import sys
import os
sys.path.append('.')
sys.path.append('eeg-ray-tuner')

# Write debug output to file
with open('debug_demo1_output.txt', 'w') as f:
    f.write("Starting demo1 graph generation debug...\n")
    
    try:
        from config_handler import UnifiedConfigHandler
        f.write("Config handler imported\n")
        
        from eeg_ray_tuner.visualization import GraphGenerator
        f.write("Graph generator imported\n")
        
        # Load config
        config_path = 'data/demo1/config_20250929_014424.yaml'
        ml_results_path = 'data/demo1/ml_results'
        
        f.write(f"Loading config: {config_path}\n")
        config_handler = UnifiedConfigHandler(config_path)
        f.write("Config loaded\n")
        
        # Check graph settings
        f.write(f"Graphs wanted: {config_handler.graphs_wanted}\n")
        f.write(f"Best models graph: {config_handler.best_models_graph}\n")
        f.write(f"Hyperparameter graph: {config_handler.per_model_across_hyperparameters_graph}\n")
        
        # Check paths
        f.write(f"ML results path: {ml_results_path}\n")
        f.write(f"Path exists: {os.path.exists(ml_results_path)}\n")
        
        if os.path.exists(ml_results_path):
            f.write(f"Contents: {os.listdir(ml_results_path)}\n")
        
        if config_handler.graphs_wanted:
            f.write("Graphs are wanted - creating generator\n")
            
            # Create graph generator
            graph_generator = GraphGenerator(config_handler, ml_results_path)
            f.write("Graph generator created\n")
            
            # Generate graphs
            f.write("Generating graphs...\n")
            graph_generator.generate_graphs()
            f.write("Graph generation completed\n")
            
            # Check results
            graphs_dir = os.path.join(ml_results_path, 'graphs')
            if os.path.exists(graphs_dir):
                f.write(f"Graphs created: {os.listdir(graphs_dir)}\n")
            else:
                f.write("No graphs directory created\n")
        else:
            f.write("Graphs are not wanted\n")
            
    except Exception as e:
        f.write(f"Error: {e}\n")
        import traceback
        f.write(traceback.format_exc())
    
    f.write("Debug completed\n")

print("Debug output written to debug_demo1_output.txt")
