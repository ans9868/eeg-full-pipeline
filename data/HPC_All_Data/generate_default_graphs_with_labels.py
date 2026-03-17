#!/usr/bin/env python
"""
Generate default graphs with experiment labels (Anova/PCA) in titles.

This script creates the same graphs as GraphGenerator but:
1. Adds experiment label (Anova/PCA) to graph titles (Anova -> F-test)
2. Saves to custom directories
3. Orders models: MLP, SVM, XGBoost, KNN
4. Uses 3 decimal places for accuracy values
"""

import sys
from pathlib import Path
import os
from unittest.mock import MagicMock

# Mock ray and xgboost before any imports that might need them
sys.modules['ray'] = MagicMock()
sys.modules['ray.tune'] = MagicMock()
sys.modules['xgboost'] = MagicMock()
sys.modules['xgboost.sklearn'] = MagicMock()

# Add eeg-ray-tuner to path
project_root = Path(__file__).parent.parent.parent
eeg_ray_tuner_path = project_root / 'eeg-ray-tuner'
sys.path.insert(0, str(eeg_ray_tuner_path))
sys.path.insert(0, str(project_root))

import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Import base graph classes
from eeg_ray_tuner.visualization.single_split_graphs import (
    BestModelsGraph as BaseBestModelsGraph,
    HyperparameterGraph as BaseHyperparameterGraph,
    BaseGraph
)


class LabeledGraphMixin:
    """Mixin to add experiment label to graph titles."""
    
    def __init__(self, *args, experiment_label: str = "", **kwargs):
        """Initialize with experiment label."""
        self.experiment_label = experiment_label
        super().__init__(*args, **kwargs)
    
    def _add_label_to_title(self, title: str) -> str:
        """Add experiment label to title if not already present."""
        if self.experiment_label and self.experiment_label not in title:
            # Replace "Anova" with "F-test" in the display label
            display_label = "F-test" if self.experiment_label.lower() == "anova" else self.experiment_label
            return f"{display_label} - {title}"
        return title


# Model ordering: MLP, XGBoost, SVM, KNN
# Handle both naming variations: with underscores and with spaces
MODEL_ORDER = [
    'MLP_(Neural_Network)', 'MLP (Neural Network)',
    'XGBoost',
    'SVM',
    'KNN'
]


def order_models_custom(df: pd.DataFrame, model_col: str = 'model_name') -> pd.DataFrame:
    """Order models in custom order: MLP, XGBoost, SVM, KNN."""
    # Create a mapping for custom order - normalize model names
    order_map = {}
    for i, model in enumerate(MODEL_ORDER):
        order_map[model] = i
        # Also map normalized versions
        if 'MLP' in model:
            order_map['MLP_(Neural_Network)'] = i
            order_map['MLP (Neural Network)'] = i
    
    # Add order column - normalize model names for matching
    def get_order(model_name):
        # Direct match
        if model_name in order_map:
            return order_map[model_name]
        # Try normalized matching
        normalized = model_name.replace('_', ' ').replace('(', ' (').strip()
        for key in order_map:
            if normalized == key.replace('_', ' ').replace('(', ' (').strip():
                return order_map[key]
        return 999
    
    df['_model_order'] = df[model_col].map(get_order)
    
    # Sort by order
    df_sorted = df.sort_values('_model_order')
    
    # Drop the temporary order column
    df_sorted = df_sorted.drop(columns=['_model_order'])
    
    return df_sorted


class LabeledBestModelsGraph(LabeledGraphMixin, BaseBestModelsGraph):
    """Best models graph with experiment label in title and custom model ordering."""
    
    def _create_best_models_graph(self, data: pd.DataFrame) -> plt.Figure:
        """Create the best models comparison graph with labeled title and custom ordering."""
        # Order models in custom order: MLP, SVM, XGBoost, KNN
        data_sorted = order_models_custom(data)
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Create vertical bar chart
        x_pos = np.arange(len(data_sorted))
        bars = ax.bar(x_pos, data_sorted[self.primary_metric], 
                     color=[self.model_colors.get(model, '#666666') for model in data_sorted['model_name']])
        
        # Add error bars if available
        if f'std_{self.primary_metric}' in data_sorted.columns:
            ax.errorbar(x_pos, data_sorted[self.primary_metric], 
                       yerr=data_sorted[f'std_{self.primary_metric}'], 
                       fmt='none', color='black', capsize=3)
        
        # Customize the plot
        ax.set_xticks(x_pos)
        ax.set_xticklabels(data_sorted['model_name'], rotation=45, ha='right')
        ax.set_ylabel(f'{self.primary_metric.replace("_", " ").title()}')
        
        # Add experiment label to title
        title = self._add_label_to_title('Best Model Performance Comparison')
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        # Add value labels on bars (3 decimal places)
        for i, (bar, value) in enumerate(zip(bars, data_sorted[self.primary_metric])):
            ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
                   f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Add legend for model colors
        legend_elements = [mpatches.Patch(color=color, label=model) 
                          for model, color in self.model_colors.items() 
                          if model in data_sorted['model_name'].values]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Improve layout
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, min(1.0, data_sorted[self.primary_metric].max() * 1.1))
        
        plt.tight_layout()
        return fig


class LabeledHyperparameterGraph(LabeledGraphMixin, BaseHyperparameterGraph):
    """Hyperparameter graph with experiment label in title."""
    
    def _create_hyperparameter_graph(self, data: pd.DataFrame) -> plt.Figure:
        """Create the hyperparameter comparison graph with labeled title."""
        # Create hyperparameter names
        data = data.copy()
        data['hyperparameter_name'] = data.apply(self._create_hyperparameter_name, axis=1)
        
        # Sort by primary metric
        data_sorted = data.sort_values(self.primary_metric, ascending=False)
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Create vertical bar chart
        x_pos = np.arange(len(data_sorted))
        color = self.model_colors.get(self.model_name, '#666666')
        bars = ax.bar(x_pos, data_sorted[self.primary_metric], color=color, alpha=0.8)
        
        # Add error bars if available
        std_col = f'std_{self.primary_metric.replace("mean_", "")}'
        if std_col in data_sorted.columns:
            ax.errorbar(x_pos, data_sorted[self.primary_metric], 
                       yerr=data_sorted[std_col], 
                       fmt='none', color='black', capsize=3)
        
        # Customize the plot
        ax.set_xticks(x_pos)
        ax.set_xticklabels(data_sorted['hyperparameter_name'], rotation=45, ha='right', fontsize=10)
        ax.set_ylabel(f'{self.primary_metric.replace("_", " ").title()}')
        
        # Add experiment label to title
        title = self._add_label_to_title(f'{self.model_name} - Hyperparameter Performance Comparison')
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        # Improve layout
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, min(1.0, data_sorted[self.primary_metric].max() * 1.1))
        
        plt.tight_layout()
        return fig


class MinimalConfigHandler:
    """Minimal config handler that enables all graphs."""
    
    def __init__(self):
        self.best_models_graph = True
        self.per_model_across_hyperparameters_graph = True
        self.per_model_per_hyperparameter_across_folds_graph = True
        self.per_subject_analysis_graph = True
        self.data_leakage_strategy = "LPSO"
        self.project_name = "hpc_analysis"
    
    def get_ray_config(self) -> Dict[str, Any]:
        return {'use_lpso': True}


class LabeledGraphGenerator:
    """
    Graph generator that creates graphs with experiment labels in titles.
    Uses the same logic as GraphGenerator but with labeled graph classes.
    """
    
    def __init__(self, config_handler, ml_results_path: str, experiment_label: str, output_dir_name: str):
        """
        Initialize the labeled graph generator.
        
        Args:
            config_handler: UnifiedConfigHandler instance
            ml_results_path: Path to ml_results directory
            experiment_label: Label to add to graph titles (e.g., "Anova", "PCA")
            output_dir_name: Name of output directory
        """
        self.config_handler = config_handler
        self.ml_results_path = Path(ml_results_path)
        self.experiment_label = experiment_label
        self.output_dir_name = output_dir_name
        self.logger = logging.getLogger('ray_driver')
        
        # Verify ml_results directory exists
        if not self.ml_results_path.exists():
            raise FileNotFoundError(f"ML results directory not found: {self.ml_results_path}")
        
        # Create graphs output directory in HPC_All_Data
        current_path = self.ml_results_path
        hpc_all_data_dir = None
        
        # Go up the directory tree to find HPC_All_Data or use parent.parent
        for _ in range(5):
            if current_path.name == "HPC_All_Data" or current_path.name == "HPC_experimentsv2":
                hpc_all_data_dir = current_path
                break
            if current_path.parent == current_path:
                break
            current_path = current_path.parent
        
        # Fallback: use parent.parent (assuming structure: HPC_All_Data/grid_50_random_folds/experiment)
        if hpc_all_data_dir is None:
            hpc_all_data_dir = self.ml_results_path.parent.parent
        
        self.graphs_output_dir = hpc_all_data_dir / output_dir_name
        self.graphs_output_dir.mkdir(exist_ok=True, parents=True)
        
        self.logger.info(f"📊 Labeled graph generator initialized")
        self.logger.info(f"📁 ML results path: {self.ml_results_path}")
        self.logger.info(f"📊 Graphs output: {self.graphs_output_dir}")
        self.logger.info(f"🏷️  Experiment label: {self.experiment_label}")
    
    def generate_graphs(self) -> None:
        """Generate all enabled graphs with experiment labels."""
        try:
            self.logger.info("🎨 Starting labeled graph generation...")
            
            # Check if any graphs are enabled
            if not self._any_graphs_enabled():
                self.logger.info("📊 No graphs enabled in configuration - skipping graph generation")
                return
            
            # Clear existing graphs directory
            self._clear_graphs_directory()
            
            # Detect split type
            split_type = self._detect_split_type()
            self.logger.info(f"🔍 Detected split type: {split_type}")
            
            if split_type == "single_split":
                self._generate_single_split_graphs()
            elif split_type == "multi_fold":
                self._generate_multi_fold_graphs()
            else:
                raise ValueError(f"Unknown split type: {split_type}")
                
            self.logger.info("✅ Labeled graph generation completed successfully!")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR in labeled graph generation: {e}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise
    
    def _any_graphs_enabled(self) -> bool:
        """Check if any graphs are enabled in configuration."""
        return (
            self.config_handler.best_models_graph or
            self.config_handler.per_model_across_hyperparameters_graph or
            self.config_handler.per_model_per_hyperparameter_across_folds_graph or
            self.config_handler.per_subject_analysis_graph
        )
    
    def _detect_split_type(self) -> str:
        """Detect whether this is a single split or multi-fold scenario."""
        # FIRST check the actual directory structure (more reliable than config)
        model_dirs = [d for d in self.ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if model_dirs:
            for model_dir in model_dirs:
                # Check for multi-fold structure: sub-X_sub-Y directories
                fold_dirs = [d for d in model_dir.iterdir() 
                           if d.is_dir() and "sub-" in d.name and "_sub-" in d.name]
                if fold_dirs:
                    return "multi_fold"
                # Check for within_subject_split (single split structure)
                within_split = [d for d in model_dir.iterdir() 
                              if d.is_dir() and "within_subject_split" in d.name]
                if within_split:
                    return "single_split"
        
        # Fallback: Check configuration only if directory structure is unclear
        try:
            if hasattr(self.config_handler, 'data_leakage_strategy'):
                strategy = self.config_handler.data_leakage_strategy
                if 'LPSO' in strategy or 'Leave-P-Subjects-Out' in strategy:
                    return "multi_fold"
            
            ray_config = self.config_handler.get_ray_config()
            if ray_config.get('use_lpso', False):
                return "multi_fold"
        except Exception:
            pass
        
        # Default to single_split
        return "single_split"
    
    def _generate_single_split_graphs(self) -> None:
        """Generate graphs for single split scenarios."""
        self.logger.info("📊 Generating single split graphs with labels...")
        
        if self.config_handler.best_models_graph:
            self.logger.info("📈 Creating labeled best models graph...")
            best_models_graph = LabeledBestModelsGraph(
                config_handler=self.config_handler,
                output_dir=self.graphs_output_dir,
                experiment_label=self.experiment_label
            )
            best_models_graph.generate_and_save(self.ml_results_path)
        
        if self.config_handler.per_model_across_hyperparameters_graph:
            self.logger.info("📈 Creating labeled hyperparameter comparison graphs...")
            models = self._get_available_models()
            for model_name in models:
                hyperparam_graph = LabeledHyperparameterGraph(
                    config_handler=self.config_handler,
                    model_name=model_name,
                    output_dir=self.graphs_output_dir,
                    experiment_label=self.experiment_label
                )
                hyperparam_graph.generate_and_save(self.ml_results_path)
    
    def _generate_multi_fold_graphs(self) -> None:
        """Generate graphs for multi-fold scenarios - not implemented for labeled graphs yet."""
        self.logger.warning("📊 Multi-fold graphs not yet implemented with custom ordering")
        pass
    
    def _get_available_models(self) -> List[str]:
        """Get list of available models from ml_results directory."""
        excluded_dirs = {'graphs', 'debug', 'ml_temp_cache', 'graphs_mega'}
        model_dirs = [d for d in self.ml_results_path.iterdir() 
                     if d.is_dir() and d.name not in excluded_dirs]
        return [d.name for d in model_dirs]
    
    def _clear_graphs_directory(self) -> None:
        """Clear the graphs directory."""
        try:
            if self.graphs_output_dir.exists():
                existing_files = list(self.graphs_output_dir.glob("*"))
                if existing_files:
                    self.logger.info(f"🧹 Clearing {len(existing_files)} existing graph files")
                    for file_path in existing_files:
                        if file_path.is_file():
                            file_path.unlink()
                        elif file_path.is_dir():
                            import shutil
                            shutil.rmtree(file_path)
        except Exception as e:
            self.logger.warning(f"⚠️ Warning: Could not clear graphs directory: {e}")


def main():
    """Main function to generate labeled graphs."""
    import argparse
    import logging
    
    # Configure logging to show output
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    parser = argparse.ArgumentParser(
        description='Generate graphs with experiment labels (Anova/PCA) in titles'
    )
    parser.add_argument(
        'ml_results_dir',
        type=str,
        help='Path to ml_results directory'
    )
    parser.add_argument(
        '--label',
        type=str,
        required=True,
        choices=['Anova', 'PCA'],
        help='Experiment label to add to graph titles'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory name (default: default_{label.lower()}_graphs)'
    )
    
    args = parser.parse_args()
    
    ml_results_path = Path(args.ml_results_dir).resolve()
    if not ml_results_path.exists():
        print(f"❌ ML results directory not found: {ml_results_path}")
        sys.exit(1)
    
    # Determine output directory name
    if args.output_dir:
        output_dir_name = args.output_dir
    else:
        output_dir_name = f"default_{args.label.lower()}_graphs"
    
    # Create minimal config handler
    config_handler = MinimalConfigHandler()
    
    print("="*70)
    print("LABELED GRAPH GENERATION")
    print("="*70)
    print(f"📁 ML Results Directory: {ml_results_path}")
    print(f"🏷️  Experiment Label: {args.label}")
    print(f"📊 Output Directory: {ml_results_path.parent / output_dir_name}")
    print("="*70)
    
    # Create labeled graph generator
    try:
        graph_generator = LabeledGraphGenerator(
            config_handler=config_handler,
            ml_results_path=str(ml_results_path),
            experiment_label=args.label,
            output_dir_name=output_dir_name
        )
        print("✅ Labeled graph generator initialized")
    except Exception as e:
        print(f"❌ Error initializing graph generator: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generate graphs
    try:
        graph_generator.generate_graphs()
        print("\n✅ Labeled graph generation completed successfully!")
    except Exception as e:
        print(f"\n❌ Error generating graphs: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # List generated graphs
    graphs_dir = graph_generator.graphs_output_dir
    if graphs_dir.exists():
        graph_files = list(graphs_dir.glob("*.png"))
        print("\n" + "="*70)
        print(f"📊 Generated {len(graph_files)} graph files:")
        print("="*70)
        for graph_file in sorted(graph_files):
            size_kb = graph_file.stat().st_size / 1024
            print(f"   ✅ {graph_file.name} ({size_kb:.1f} KB)")
        
        subdirs = [d for d in graphs_dir.iterdir() if d.is_dir()]
        if subdirs:
            print(f"\n   📁 Generated {len(subdirs)} subdirectories:")
            for subdir in sorted(subdirs):
                subdir_files = list(subdir.glob("*.png"))
                print(f"      • {subdir.name}/ ({len(subdir_files)} files)")
    
    print("\n" + "="*70)
    print("LABELED GRAPH GENERATION COMPLETE")
    print("="*70)
    print(f"\n📁 Generated graphs in: {graphs_dir}")
    print("="*70)


if __name__ == '__main__':
    main()

