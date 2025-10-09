#!/usr/bin/env python3
"""
Launcher script for graph generation from the main project directory.
"""

import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_graphs.py <graph_type> <ml_results_path>")
        print("")
        print("Graph types available:")
        print("  all          - Generate all types of graphs")
        print("  per-subject  - Generate per-subject analysis graphs only")
        print("  boxplots     - Generate hyperparameter box plots only")
        print("")
        print("Examples:")
        print("  python run_graphs.py all /path/to/ml_results")
        print("  python run_graphs.py per-subject /path/to/ml_results")
        print("  python run_graphs.py boxplots /path/to/ml_results")
        sys.exit(1)
    
    graph_type = sys.argv[1].lower()
    ml_results_path = sys.argv[2]
    
    # Determine which script to run
    if graph_type == "all":
        script_name = "generate_all_graphs.py"
    elif graph_type == "per-subject":
        script_name = "simple_graph_generator_no_config.py"
    elif graph_type == "boxplots":
        script_name = "hyperparameter_boxplot_generator.py"
    else:
        print(f"❌ Unknown graph type: {graph_type}")
        print("Available types: all, per-subject, boxplots")
        sys.exit(1)
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        sys.exit(1)
    
    # Run the script
    try:
        print(f"🚀 Running {script_name} from {script_dir}")
        result = subprocess.run([
            sys.executable, str(script_path), ml_results_path
        ], cwd=str(script_dir), check=True)
        
        print("✅ Graph generation completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running graph generation: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
