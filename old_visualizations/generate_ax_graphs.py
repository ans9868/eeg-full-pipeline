#!/usr/bin/env python
"""
Quick script to generate AX search visualizations.

Usage:
    python generate_ax_graphs.py

This will generate all AX-specific graphs from the testEdgeCases results.
"""

import sys
from pathlib import Path

# Add eeg-ray-tuner to path
sys.path.insert(0, str(Path(__file__).parent / "eeg-ray-tuner"))

from eeg_ray_tuner.visualization import AxGraphGenerator
import logging

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Paths
    data_dir = Path("data/testEdgeCases")
    ax_results = data_dir / "ml_results_ax"
    grid_results = data_dir / "ml_results_grid_search"
    
    print("=" * 70)
    print("🎨 AX SEARCH VISUALIZATION GENERATOR")
    print("=" * 70)
    print(f"📂 AX Results: {ax_results}")
    print(f"📂 Grid Results: {grid_results}")
    print()
    
    # Check paths exist
    if not ax_results.exists():
        print(f"❌ ERROR: AX results not found at {ax_results}")
        return 1
    
    # Initialize generator
    print("🔧 Initializing graph generator...")
    generator = AxGraphGenerator(ax_results)
    
    # Generate all graphs
    print("\n🎨 Generating ALL graphs...")
    print("   This may take a minute...")
    print()
    
    if grid_results.exists():
        generator.generate_all_graphs(grid_results_path=grid_results)
    else:
        print("⚠️  Grid Search results not found - generating AX-only graphs")
        generator.generate_all_graphs()
    
    print()
    print("=" * 70)
    print(f"✅ SUCCESS! Graphs saved to:")
    print(f"   {ax_results / 'graphs'}")
    print("=" * 70)
    print()
    print("📊 Graphs generated:")
    
    graphs_dir = ax_results / "graphs"
    if graphs_dir.exists():
        graphs = sorted(graphs_dir.glob("*.png"))
        for i, graph in enumerate(graphs, 1):
            print(f"   {i}. {graph.name}")
    
    print()
    print(f"🎉 Total: {len(list(graphs_dir.glob('*.png')))} graphs created!")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

