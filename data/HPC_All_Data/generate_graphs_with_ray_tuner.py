#!/usr/bin/env python
"""
Generate graphs using the actual eeg-ray-tuner GraphGenerator.

This script uses the GraphGenerator from eeg_ray_tuner.visualization
to generate the standard graphs that would normally be created
at the end of a Ray Tuner experiment.
"""

import sys
from pathlib import Path

# Add eeg-ray-tuner to path
project_root = Path(__file__).parent.parent.parent
eeg_ray_tuner_path = project_root / 'eeg-ray-tuner'
sys.path.insert(0, str(eeg_ray_tuner_path))

# Also add project root for config_handler
sys.path.insert(0, str(project_root))

import os
from typing import Any, Dict, Optional

# Import GraphGenerator from eeg-ray-tuner
from eeg_ray_tuner.visualization import GraphGenerator

# Try to import config_handler
try:
    from config_handler import UnifiedConfigHandler
except ImportError:
    print("⚠️ Warning: Could not import UnifiedConfigHandler")
    print("   Creating minimal config handler for graph generation")
    UnifiedConfigHandler = None


class MinimalConfigHandler:
    """
    Minimal config handler that enables all graphs.
    This is used when we don't have the full config file.
    """
    
    def __init__(self):
        # Enable all graphs
        self.best_models_graph = True
        self.per_model_across_hyperparameters_graph = True
        self.per_model_per_hyperparameter_across_folds_graph = True
        self.per_subject_analysis_graph = True
        
        # Default values for graph generation
        self.data_leakage_strategy = "LPSO"  # Assume LPSO for multi-fold graphs
        self.project_name = "hpc_analysis"
    
    def get_ray_config(self) -> Dict[str, Any]:
        """Return ray config with use_lpso enabled."""
        return {'use_lpso': True}


def load_config_if_available(config_path: Optional[Path]) -> Any:
    """
    Try to load config file, otherwise return minimal config handler.
    
    Args:
        config_path: Path to config file (optional)
        
    Returns:
        UnifiedConfigHandler or MinimalConfigHandler
    """
    if config_path and config_path.exists() and UnifiedConfigHandler:
        try:
            print(f"📋 Loading config from: {config_path}")
            config_handler = UnifiedConfigHandler(str(config_path))
            print("✅ Config loaded successfully")
            return config_handler
        except Exception as e:
            print(f"⚠️ Warning: Could not load config file: {e}")
            print("   Using minimal config handler instead")
            return MinimalConfigHandler()
    else:
        print("📋 No config file provided, using minimal config handler")
        print("   (All graphs will be enabled)")
        return MinimalConfigHandler()


def find_config_file(ml_results_dir: Path) -> Optional[Path]:
    """Try to find config file in ml_results directory or parent directories."""
    # Check common locations
    possible_configs = [
        ml_results_dir / "config.yaml",
        ml_results_dir / "config.yml",
        ml_results_dir.parent / "config.yaml",
        ml_results_dir.parent / "config.yml",
    ]
    
    for config_path in possible_configs:
        if config_path.exists():
            return config_path
    
    # Search for any yaml file with "config" in name
    for yaml_file in ml_results_dir.rglob("config*.yaml"):
        return yaml_file
    for yaml_file in ml_results_dir.rglob("config*.yml"):
        return yaml_file
    
    return None


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate graphs using eeg-ray-tuner GraphGenerator'
    )
    parser.add_argument(
        'ml_results_dir', 
        type=str, 
        help='Path to ml_results directory'
    )
    parser.add_argument(
        '--config', 
        type=str, 
        default=None,
        help='Path to config file (optional - will search if not provided)'
    )
    
    args = parser.parse_args()
    
    ml_results_dir = Path(args.ml_results_dir).resolve()
    
    if not ml_results_dir.exists():
        print(f"❌ ML results directory not found: {ml_results_dir}")
        sys.exit(1)
    
    print("="*70)
    print("GRAPH GENERATION USING EEG-RAY-TUNER")
    print("="*70)
    print(f"📁 ML Results Directory: {ml_results_dir}")
    
    # Try to find config file
    if args.config:
        config_path = Path(args.config).resolve()
    else:
        config_path = find_config_file(ml_results_dir)
    
    # Load config handler
    config_handler = load_config_if_available(config_path)
    
    # Create GraphGenerator
    print("\n📊 Initializing GraphGenerator...")
    try:
        graph_generator = GraphGenerator(
            config_handler=config_handler,
            ml_results_path=str(ml_results_dir)
        )
        print("✅ GraphGenerator initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing GraphGenerator: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generate graphs
    print("\n📊 Generating graphs...")
    print("="*70)
    try:
        graph_generator.generate_graphs()
        print("\n✅ Graph generation completed successfully!")
    except Exception as e:
        print(f"\n❌ Error generating graphs: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # List generated graphs
    graphs_dir = ml_results_dir / "graphs"
    if graphs_dir.exists():
        graph_files = list(graphs_dir.glob("*.png"))
        print("\n" + "="*70)
        print(f"📊 Generated {len(graph_files)} graph files:")
        print("="*70)
        for graph_file in sorted(graph_files):
            size_kb = graph_file.stat().st_size / 1024
            print(f"   ✅ {graph_file.name} ({size_kb:.1f} KB)")
        
        # Check for subdirectories
        subdirs = [d for d in graphs_dir.iterdir() if d.is_dir()]
        if subdirs:
            print(f"\n   📁 Generated {len(subdirs)} subdirectories:")
            for subdir in sorted(subdirs):
                subdir_files = list(subdir.glob("*.png"))
                print(f"      • {subdir.name}/ ({len(subdir_files)} files)")
    
    print("\n" + "="*70)
    print("GRAPH GENERATION COMPLETE")
    print("="*70)
    print(f"\n📁 Generated graphs in: {graphs_dir}")
    print("="*70)


if __name__ == '__main__':
    main()


