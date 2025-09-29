#!/usr/bin/env python3

import sys
import os
sys.path.append('.')
sys.path.append('eeg-ray-tuner')

# Write debug output to file
with open('debug_best_models.txt', 'w') as f:
    f.write("Starting best models graph debug...\n")
    
    try:
        from config_handler import UnifiedConfigHandler
        f.write("Config handler imported\n")
        
        from eeg_ray_tuner.visualization.single_split_graphs import BestModelsGraph
        f.write("BestModelsGraph imported\n")
        
        # Load config
        config_handler = UnifiedConfigHandler('data/fingerPrintWithin/config_20250928_193856.yaml')
        f.write("Config loaded\n")
        
        # Check settings
        f.write(f"Best models graph enabled: {config_handler.best_models_graph}\n")
        
        if config_handler.best_models_graph:
            f.write("Best models graph is enabled - proceeding\n")
            
            # Create output directory
            from pathlib import Path
            output_dir = Path('data/fingerPrintWithin/ml_results/graphs')
            output_dir.mkdir(exist_ok=True)
            f.write(f"Output directory created: {output_dir}\n")
            
            # Create best models graph
            best_models_graph = BestModelsGraph(
                config_handler=config_handler,
                output_dir=output_dir
            )
            f.write("BestModelsGraph instance created\n")
            
            # Generate and save
            ml_results_path = Path('data/fingerPrintWithin/ml_results')
            best_models_graph.generate_and_save(ml_results_path)
            f.write("Best models graph generated and saved\n")
            
            # Check if file was created
            best_models_file = output_dir / 'best_models_comparison.png'
            if best_models_file.exists():
                f.write(f"Best models graph file exists: {best_models_file}\n")
            else:
                f.write("Best models graph file was not created\n")
        else:
            f.write("Best models graph is not enabled\n")
            
    except Exception as e:
        f.write(f"Error: {e}\n")
        import traceback
        f.write(traceback.format_exc())
    
    f.write("Debug completed\n")

print("Debug output written to debug_best_models.txt")
