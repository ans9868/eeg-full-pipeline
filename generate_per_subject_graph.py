#!/usr/bin/env python3
"""
Generate per-subject analysis graph for fingerPrintWithin data.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up environment
os.environ['RAY_DISABLE_IMPORT_WARNING'] = '1'

def generate_per_subject_graph():
    """Generate the per-subject analysis graph."""
    try:
        print("🧪 Generating per-subject analysis graph...")
        
        # Import the graph class
        sys.path.insert(0, str(project_root / "eeg-ray-tuner"))
        from eeg_ray_tuner.visualization.multi_fold_graphs import PerSubjectAnalysisGraph
        from config_handler import UnifiedConfigHandler
        
        # Load the config
        config_path = "data/fingerPrintWithin/config_20250929_030648.yaml"
        config_handler = UnifiedConfigHandler(config_path)
        
        # Set up paths
        ml_results_path = Path("data/fingerPrintWithin/ml_results")
        output_dir = ml_results_path / "graphs"
        output_dir.mkdir(exist_ok=True)
        
        print(f"📊 ML results path: {ml_results_path}")
        print(f"📊 Output directory: {output_dir}")
        
        # Create the graph
        per_subject_graph = PerSubjectAnalysisGraph(
            config_handler=config_handler,
            output_dir=output_dir
        )
        
        # Generate the graph
        per_subject_graph.generate_and_save(ml_results_path)
        
        print("✅ Per-subject analysis graph generated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error generating per-subject analysis graph: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = generate_per_subject_graph()
    sys.exit(0 if success else 1)
