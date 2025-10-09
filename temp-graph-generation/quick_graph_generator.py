#!/usr/bin/env python3
import sys
from pathlib import Path

# Add paths
sys.path.append('.')
sys.path.append('./eeg-ray-tuner')

from eeg_ray_tuner.visualization.graph_generator import GraphGenerator
from config_handler import UnifiedConfigHandler

def main():
    print("🚀 Starting quick_graph_generator.py")
    print(f"📋 Arguments: {sys.argv}")
    
    if len(sys.argv) < 2:
        print("Usage: python quick_graph_generator.py <ml_results_path>")
        print("Example: python quick_graph_generator.py data/fingerPrintAllTogether/ml_results")
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
        
        # Create graph generator
        graph_generator = GraphGenerator(config_handler, ml_results_path)
        
        # Generate graphs
        print(f"🎨 Generating graphs from: {ml_results_path}")
        graph_generator.generate_graphs()
        print("✅ Graph generation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
