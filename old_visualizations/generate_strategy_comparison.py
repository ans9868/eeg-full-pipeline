#!/usr/bin/env python
"""
Generate comprehensive strategy comparison visualizations (AX vs Grid Search).

Usage:
    python generate_strategy_comparison.py

This will generate ALL 11 comparison graphs analyzing AX vs Grid Search strategies.
"""

import sys
from pathlib import Path

# Add eeg-ray-tuner to path
sys.path.insert(0, str(Path(__file__).parent / "eeg-ray-tuner"))

from eeg_ray_tuner.visualization import StrategyComparisonGenerator
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
    output_dir = data_dir / "ml_strategies_comparison"
    
    print("=" * 80)
    print("🔍 STRATEGY COMPARISON GENERATOR: AX vs Grid Search")
    print("=" * 80)
    print(f"📂 AX Results: {ax_results}")
    print(f"📂 Grid Results: {grid_results}")
    print(f"📂 Output Directory: {output_dir}")
    print()
    
    # Check paths exist
    if not ax_results.exists():
        print(f"❌ ERROR: AX results not found at {ax_results}")
        return 1
    
    if not grid_results.exists():
        print(f"❌ ERROR: Grid results not found at {grid_results}")
        return 1
    
    # Initialize generator
    print("🔧 Initializing comparison generator...")
    generator = StrategyComparisonGenerator(
        ax_results_path=ax_results,
        grid_results_path=grid_results,
        output_path=output_dir
    )
    
    # Generate all comparisons
    print("\n🎨 Generating ALL comparison graphs...")
    print("   This will create 11 different visualizations:")
    print("   1. Performance Distribution (Box/Violin)")
    print("   2. Win/Loss/Tie Heatmap")
    print("   3. Statistical Comparison Table")
    print("   4. Head-to-Head Comparison")
    print("   5. Consistency Analysis")
    print("   6. Computational Efficiency")
    print("   7. Hyperparameter Stability")
    print("   8. Radar Chart (Multi-metric)")
    print("   9. Model Recommendations")
    print("   10. Fold Difficulty Analysis")
    print("   11. Summary Dashboard")
    print()
    
    generator.generate_all_comparisons()
    
    print()
    print("=" * 80)
    print(f"✅ SUCCESS! All comparison graphs saved to:")
    print(f"   {output_dir}")
    print("=" * 80)
    print()
    print("📊 Graphs generated:")
    
    if output_dir.exists():
        graphs = sorted(output_dir.glob("*.png"))
        for i, graph in enumerate(graphs, 1):
            print(f"   {i}. {graph.name}")
        
        # Also list CSV files
        csvs = sorted(output_dir.glob("*.csv"))
        if csvs:
            print()
            print("📄 Data files:")
            for csv in csvs:
                print(f"   - {csv.name}")
    
    print()
    print(f"🎉 Total: {len(list(output_dir.glob('*.png')))} graphs + {len(list(output_dir.glob('*.csv')))} data files created!")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

