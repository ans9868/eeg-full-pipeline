#!/usr/bin/env python3
"""
Simple graph generator that directly imports only what's needed.
"""

import sys
import os
from pathlib import Path

# Add paths
sys.path.append('.')
sys.path.append('./eeg-ray-tuner')

# Direct imports to avoid ray tuner initialization issues
from eeg_ray_tuner.visualization.multi_fold_graphs import PerSubjectAnalysisGraph
from eeg_ray_tuner.visualization.single_split_graphs import BestModelsGraph, HyperparameterGraph
from config_handler import UnifiedConfigHandler

def main():
    print("🚀 Starting simple_graph_generator.py")
    print(f"📋 Arguments: {sys.argv}")
    
    if len(sys.argv) < 2:
        print("Usage: python simple_graph_generator.py <ml_results_path>")
        print("Example: python simple_graph_generator.py data/fingerPrintAllTogether/ml_results")
        sys.exit(1)
    
    ml_results_path = sys.argv[1]
    
    try:
        # Find config file
        config_files = list(Path(ml_results_path).parent.glob("config_*.yaml"))
        if not config_files:
            print("❌ No config file found in parent directory")
            sys.exit(1)
        
        print(f"📁 Using config: {config_files[0]}")
        config_handler = UnifiedConfigHandler(str(config_files[0]))
        
        # Create output directory
        output_dir = Path(ml_results_path) / "graphs"
        output_dir.mkdir(exist_ok=True)
        
        print(f"📊 Output directory: {output_dir}")
        
        # Generate per-subject analysis graph
        if hasattr(config_handler, 'per_subject_analysis_graph') and config_handler.per_subject_analysis_graph:
            print("🎨 Generating per-subject analysis graph...")
            per_subject_graph = PerSubjectAnalysisGraph(
                config_handler=config_handler,
                output_dir=output_dir
            )
            per_subject_graph.generate_and_save(Path(ml_results_path))
            print("✅ Per-subject analysis graph completed!")
        else:
            print("📊 Per-subject analysis graph not enabled in config")
        
        print("✅ Graph generation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
