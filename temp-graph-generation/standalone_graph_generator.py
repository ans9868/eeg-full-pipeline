#!/usr/bin/env python3
"""
Standalone graph generator that doesn't import the full ray tuner.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np

# Add paths
sys.path.append('.')
from config_handler import UnifiedConfigHandler

class BaseGraph:
    """Base class for all graph types."""
    
    def __init__(self, config_handler, output_dir: Path):
        self.config_handler = config_handler
        self.output_dir = output_dir
        self.logger = logging.getLogger('standalone_graph')
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Graph configuration
        self.figure_size = (12, 8)
        self.dpi = 300
        self.format = "png"
        
        # Model colors
        self.model_colors = {
            "KNN": "#1f77b4",
            "MLP": "#ff7f0e", 
            "SVM": "#2ca02c",
            "Random Forest": "#d62728",
            "Logistic Regression": "#9467bd"
        }
    
    def save_graph(self, figure: plt.Figure, filename: str) -> None:
        """Save the graph to the output directory."""
        output_path = self.output_dir / f"{filename}.{self.format}"
        figure.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        self.logger.info(f"💾 Graph saved: {output_path}")
        plt.close(figure)

class PerSubjectAnalysisGraph(BaseGraph):
    """Creates per-subject analysis graphs showing accuracy for each subject."""
    
    def __init__(self, config_handler, output_dir: Path):
        super().__init__(config_handler, output_dir)
        self.graph_name = "per_subject_analysis"
        # Create subdirectory for individual per-subject graphs
        self.per_subject_dir = output_dir / "per_subject_individual"
        print(f"Initialized PerSubjectAnalysisGraph")
    
    def generate_and_save(self, ml_results_path: Path) -> None:
        """Generate and save per-subject analysis graphs."""
        try:
            print(f"📊 Loading per-subject data from: {ml_results_path}")
            
            # Load and process per-subject data
            all_data = self._load_per_subject_data(ml_results_path)
            if all_data is None or all_data.empty:
                raise ValueError("No per-subject data found or data is empty")
            
            print(f"📊 Loaded {len(all_data)} subjects for per-subject analysis")
            
            # 1. Create overall per-subject graph (average across all models/hyperparams)
            overall_data = self._create_overall_per_subject_data(all_data)
            if overall_data is not None and not overall_data.empty:
                figure = self._create_per_subject_graph(overall_data, "Per-Subject Test Accuracy (Overall)")
                if figure is not None:
                    self.save_graph(figure, self.graph_name)
                    print("✅ Overall per-subject analysis graph generated and saved successfully")
            
            # 2. Create individual graphs for each model×hyperparameter combination
            self._create_individual_per_subject_graphs(all_data)
            
            print("✅ All per-subject analysis graphs generated and saved successfully")
            
        except Exception as e:
            print(f"💥 CRITICAL ERROR generating per-subject analysis graph: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _load_per_subject_data(self, ml_results_path: Path) -> pd.DataFrame:
        """Load per-subject data by reading prediction parquet files."""
        model_dirs = [d for d in ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if not model_dirs:
            raise ValueError("No model directories found")
        
        all_subject_data = []
        
        for model_dir in model_dirs:
            model_name = model_dir.name
            print(f"📊 Processing model: {model_name}")
            
            # Get all hyperparameter directories for this model
            hyperparam_dirs = [d for d in model_dir.iterdir() 
                             if d.is_dir() and "_" in d.name]
            
            if not hyperparam_dirs:
                print(f"No hyperparameter directories found for model {model_name}")
                continue
            
            # Collect data from all hyperparameter directories
            for hyperparam_dir in hyperparam_dirs:
                test_parquet_file = hyperparam_dir / "test_predictions.parquet"
                results_json_file = hyperparam_dir / "results.json"
                
                if test_parquet_file.exists():
                    try:
                        # Read the parquet file
                        df = pd.read_parquet(test_parquet_file)
                        
                        # Calculate per-subject accuracy
                        if 'SubjectID' in df.columns and 'label' in df.columns and 'prediction' in df.columns:
                            # Check if Group column exists
                            if 'Group' in df.columns:
                                # Group by SubjectID and calculate accuracy and get group info
                                per_subject = df.groupby('SubjectID').apply(
                                    lambda x: pd.Series({
                                        'accuracy': (x['label'] == x['prediction']).mean(),
                                        'group': x['Group'].iloc[0]  # Get the group for each subject
                                    })
                                ).reset_index()
                            else:
                                print(f"❌ Group column not found in {test_parquet_file.name}")
                                print(f"   Available columns: {df.columns.tolist()}")
                                raise ValueError(f"Group column missing from {test_parquet_file.name}")
                            
                            # Add model and hyperparameter info
                            per_subject['model_name'] = model_name
                            per_subject['hyperparam_dir'] = hyperparam_dir.name
                            
                            # Try to load hyperparameter information from results.json
                            hyperparam_info = self._load_hyperparameter_info(results_json_file)
                            per_subject['hyperparam_info'] = hyperparam_info
                            
                            all_subject_data.append(per_subject)
                            
                    except Exception as e:
                        print(f"Error reading parquet file {test_parquet_file}: {e}")
        
        if not all_subject_data:
            raise ValueError("No per-subject data found in any parquet files")
        
        # Combine all data
        combined_data = pd.concat(all_subject_data, ignore_index=True)
        return combined_data
    
    def _create_overall_per_subject_data(self, all_data: pd.DataFrame) -> pd.DataFrame:
        """Create overall per-subject data by averaging across all models/hyperparameters."""
        # Calculate average accuracy per subject across all models/hyperparameters
        if 'group' in all_data.columns:
            # Include group information if available
            per_subject_avg = all_data.groupby('SubjectID').agg({
                'accuracy': 'mean',
                'group': 'first'  # Get the group for each subject (should be consistent)
            }).reset_index()
        else:
            print(f"❌ Group column not found in overall data")
            print(f"   Available columns: {all_data.columns.tolist()}")
            raise ValueError(f"Group column missing from overall data")
        
        per_subject_avg = per_subject_avg.sort_values('SubjectID', ascending=True)
        return per_subject_avg
    
    def _create_individual_per_subject_graphs(self, all_data: pd.DataFrame) -> None:
        """Create individual per-subject graphs for each model×hyperparameter combination."""
        # Create the subdirectory if it doesn't exist
        self.per_subject_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created individual per-subject graphs directory: {self.per_subject_dir}")
        
        # Group by model and hyperparameter
        grouped = all_data.groupby(['model_name', 'hyperparam_dir'])
        
        for (model_name, hyperparam_dir), group_data in grouped:
            # Create a clean filename
            clean_model = model_name.replace(' ', '_').lower()
            clean_hyperparam = hyperparam_dir.replace(' ', '_').replace('=', '_').lower()
            filename = f"per_subject_{clean_model}_{clean_hyperparam}"
            
            # Sort by subject ID
            sorted_data = group_data.sort_values('SubjectID')
            
            # Create a readable title
            readable_title = self._create_readable_title(model_name, hyperparam_dir, all_data)
            
            # Create graph
            figure = self._create_per_subject_graph(sorted_data, readable_title)
            
            if figure is not None:
                # Save in the subdirectory
                self.save_graph_in_subdir(figure, filename)
    
    def _create_per_subject_graph(self, data: pd.DataFrame, title: str = "Per-Subject Test Accuracy") -> plt.Figure:
        """Create the per-subject analysis graph with bar chart."""
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Create bar chart with color coding by group
        x_pos = np.arange(len(data))
        
        # Generate colors dynamically based on unique groups
        if 'group' in data.columns:
            unique_groups = data['group'].unique()
        elif 'Group' in data.columns:
            unique_groups = data['Group'].unique()
        else:
            print(f"❌ No group column found in data for graph creation")
            print(f"   Available columns: {data.columns.tolist()}")
            raise ValueError(f"No group column found in data")
        
        # Generate distinct colors for each group
        if len(unique_groups) <= 10:
            color_palette = ['#2E8B57', '#DC143C', '#FF8C00', '#4169E1', '#8B0000', 
                           '#9370DB', '#20B2AA', '#FF6347', '#32CD32', '#FF1493']
        else:
            color_palette = cm.Set3(np.linspace(0, 1, len(unique_groups)))
        
        # Create mapping from group names to colors
        group_colors = {group: color_palette[i % len(color_palette)] 
                       for i, group in enumerate(unique_groups)}
        
        # Get colors for each bar based on group
        colors = [group_colors[group] for group in data['group']]
        
        bars = ax.bar(x_pos, data['accuracy'], color=colors, alpha=0.8)
        
        # Customize the plot
        ax.set_xticks(x_pos)
        ax.set_xticklabels(data['SubjectID'], rotation=45, ha='right', fontsize=12)
        ax.set_ylabel('Test Accuracy')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add legend for groups
        legend_elements = []
        for group in unique_groups:
            color = group_colors[group]
            legend_elements.append(plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8, label=group.title()))
        
        if len(unique_groups) > 1:
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))
        
        plt.tight_layout()
        return fig
    
    def save_graph_in_subdir(self, figure: plt.Figure, filename: str) -> None:
        """Save graph to the per_subject_individual subdirectory."""
        output_path = self.per_subject_dir / f"{filename}.{self.format}"
        figure.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        print(f"💾 Individual per-subject graph saved: {output_path}")
        plt.close(figure)
    
    def _load_hyperparameter_info(self, results_json_file: Path) -> str:
        """Load hyperparameter information from results.json file."""
        try:
            if not results_json_file.exists():
                return "Unknown hyperparameters"
            
            with open(results_json_file, 'r') as f:
                results = json.load(f)
            
            # Extract hyperparameters from the results
            hyperparams = results.get('hyperparameters', {})
            if not hyperparams:
                hyperparams = results.get('detailed_results', {}).get('hyperparams', {})
            if not hyperparams:
                hyperparams = results.get('hyperparams', {})
            
            if not hyperparams:
                return "Unknown hyperparameters"
            
            # Create a readable string of hyperparameters
            param_strings = []
            for key, value in hyperparams.items():
                if key.lower() in ['n_neighbors', 'n_neigh', 'k']:
                    param_strings.append(f"n_neighbors={value}")
                elif key.lower() in ['metric', 'distance_metric']:
                    param_strings.append(f"metric={value}")
                elif key.lower() in ['weights', 'weight']:
                    param_strings.append(f"weights={value}")
                else:
                    param_strings.append(f"{key}={value}")
            
            return ", ".join(param_strings)
            
        except Exception as e:
            print(f"Could not load hyperparameters from {results_json_file}: {e}")
            return "Unknown hyperparameters"
    
    def _create_readable_title(self, model_name: str, hyperparam_dir: str, all_data: pd.DataFrame) -> str:
        """Create a readable title by extracting hyperparameters from the loaded data."""
        try:
            # Find the first row with this model and hyperparam_dir to get the hyperparam info
            sample_row = all_data[(all_data['model_name'] == model_name) & 
                                (all_data['hyperparam_dir'] == hyperparam_dir)].iloc[0]
            
            hyperparam_info = sample_row.get('hyperparam_info', 'Unknown hyperparameters')
            
            if hyperparam_info and hyperparam_info != "Unknown hyperparameters":
                return f"Per-Subject Test Accuracy: {model_name} - {hyperparam_info}"
            else:
                return f"Per-Subject Test Accuracy: {model_name} - {hyperparam_dir}"
                
        except Exception as e:
            print(f"Could not create readable title for {model_name} - {hyperparam_dir}: {e}")
            return f"Per-Subject Test Accuracy: {model_name} - {hyperparam_dir}"

def main():
    print("🚀 Starting standalone_graph_generator.py")
    print(f"📋 Arguments: {sys.argv}")
    
    if len(sys.argv) < 2:
        print("Usage: python standalone_graph_generator.py <ml_results_path>")
        print("Example: python standalone_graph_generator.py data/fingerPrintAllTogether/ml_results")
        sys.exit(1)
    
    print("✅ Arguments check passed")
    
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
