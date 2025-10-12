"""
Single Split Graph Generation for EEG Ray Tuner

This module handles graph generation for single split scenarios (transform all data,
within subject, 1 test/1 train split).
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np


class BaseGraph:
    """Base class for all graph types."""
    
    def __init__(self, config_handler, output_dir: Path):
        """
        Initialize base graph.
        
        Args:
            config_handler: UnifiedConfigHandler instance
            output_dir: Directory to save graphs
        """
        self.config_handler = config_handler
        self.output_dir = output_dir
        self.logger = logging.getLogger('ray_driver')
        
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
            "XGBoost": "#9467bd",
            "Decision Tree": "#8c564b",
            "Gradient Boosting": "#e377c2",
            "AdaBoost": "#7f7f7f",
            "Logistic Regression": "#bcbd22",
            "Logistic Regression": "#17becf"
        }
    
    def save_graph(self, figure: plt.Figure, filename: str) -> None:
        """Save graph to file with consistent styling."""
        output_path = self.output_dir / f"{filename}.{self.format}"
        figure.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        self.logger.info(f"💾 Graph saved: {output_path}")
        plt.close(figure)


class BestModelsGraph(BaseGraph):
    """Creates best model comparison graph."""
    
    def __init__(self, config_handler, output_dir: Path):
        super().__init__(config_handler, output_dir)
        self.primary_metric = "best_test_accuracy"  # Default metric
    
    def generate_and_save(self, ml_results_path: Path) -> None:
        """Generate and save the best models graph."""
        try:
            self.logger.info(f"📊 Loading model comparison data from: {ml_results_path}")
            
            # Load data
            data = self._load_model_comparison_data(ml_results_path)
            
            if data is None or data.empty:
                raise ValueError("No model comparison data found or data is empty")
            
            self.logger.info(f"📊 Loaded {len(data)} models for best models graph")
            
            # Create graph
            figure = self._create_best_models_graph(data)
            if figure is None:
                raise ValueError("Failed to create best models graph figure")
            
            # Save graph
            self.save_graph(figure, "best_models_comparison")
            
            self.logger.info("✅ Best models graph generated and saved successfully")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR generating best models graph: {e}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise  # Hard fail
    
    def _load_model_comparison_data(self, ml_results_path: Path) -> pd.DataFrame:
        """Load model comparison data."""
        model_comparison_file = ml_results_path / "model_comparison.csv"
        
        if not model_comparison_file.exists():
            raise FileNotFoundError(f"Model comparison file not found: {model_comparison_file}")
        
        df = pd.read_csv(model_comparison_file)
        self.logger.info(f"📊 Loaded model comparison data: {len(df)} models")
        
        return df
    
    def _create_best_models_graph(self, data: pd.DataFrame) -> plt.Figure:
        """Create the best models comparison graph."""
        # Sort by primary metric
        data_sorted = data.sort_values(self.primary_metric, ascending=False)
        
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
        ax.set_title('Best Model Performance Comparison', fontsize=16, fontweight='bold')
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, data_sorted[self.primary_metric])):
            ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
                   f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
        
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


class HyperparameterGraph(BaseGraph):
    """Creates per-model hyperparameter comparison graphs."""
    
    def __init__(self, config_handler, model_name: str, output_dir: Path):
        super().__init__(config_handler, output_dir)
        self.model_name = model_name
        self.primary_metric = "mean_test_accuracy"  # Default metric
    
    def generate_and_save(self, ml_results_path: Path) -> None:
        """Generate and save the hyperparameter comparison graph for this model."""
        try:
            self.logger.info(f"📊 Loading hyperparameter data for {self.model_name} from: {ml_results_path}")
            
            # Load data
            data = self._load_hyperparameter_data(ml_results_path)
            
            if data is None or data.empty:
                raise ValueError(f"No hyperparameter data found for {self.model_name}")
            
            self.logger.info(f"📊 Loaded {len(data)} hyperparameter combinations for {self.model_name}")
            
            # Create graph
            figure = self._create_hyperparameter_graph(data)
            if figure is None:
                raise ValueError(f"Failed to create hyperparameter graph figure for {self.model_name}")
            
            # Save graph
            filename = f"{self.model_name.lower()}_hyperparameter_comparison"
            self.save_graph(figure, filename)
            
            self.logger.info(f"✅ Hyperparameter graph for {self.model_name} generated and saved successfully")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR generating hyperparameter graph for {self.model_name}: {e}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise  # Hard fail
    
    def _load_hyperparameter_data(self, ml_results_path: Path) -> pd.DataFrame:
        """Load hyperparameter comparison data for this model."""
        model_dir = ml_results_path / self.model_name
        hyperparam_file = model_dir / "hyperparameter_comparison.csv"
        
        if not hyperparam_file.exists():
            raise FileNotFoundError(f"Hyperparameter comparison file not found: {hyperparam_file}")
        
        df = pd.read_csv(hyperparam_file)
        self.logger.info(f"📊 Loaded hyperparameter data for {self.model_name}: {len(df)} combinations")
        
        return df
    
    def _create_hyperparameter_graph(self, data: pd.DataFrame) -> plt.Figure:
        """Create the hyperparameter comparison graph."""
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
        ax.set_title(f'{self.model_name} - Hyperparameter Performance Comparison', 
                    fontsize=16, fontweight='bold')
        
        # Add value labels on bars (removed for cleaner visualization)
        # for i, (bar, value) in enumerate(zip(bars, data_sorted[self.primary_metric])):
        #     ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
        #            f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
        
        # Improve layout
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, min(1.0, data_sorted[self.primary_metric].max() * 1.1))
        
        plt.tight_layout()
        return fig
    
    def _create_hyperparameter_name(self, row: pd.Series) -> str:
        """Create a readable name for hyperparameter combination."""
        if self.model_name == "KNN":
            n_neighbors = row.get('hyperparam_n_neighbors', '?')
            weights = row.get('hyperparam_weights', '?')
            metric = row.get('hyperparam_metric', '?').capitalize()
            return f"KNN_{metric}_n={n_neighbors}_{weights}"
        
        elif self.model_name == "MLP":
            # Handle MLP hyperparameters
            hidden_layers = row.get('hyperparam_hidden_layer_sizes', '?')
            activation = row.get('hyperparam_activation', '?')
            solver = row.get('hyperparam_solver', '?')
            return f"MLP_{activation}_{solver}_layers={hidden_layers}"
        
        elif self.model_name == "SVM":
            # Handle SVM hyperparameters
            kernel = row.get('hyperparam_kernel', '?')
            c = row.get('hyperparam_C', '?')
            gamma = row.get('hyperparam_gamma', '?')
            return f"SVM_{kernel}_C={c}_gamma={gamma}"
        
        elif self.model_name == "Random Forest":
            # Handle Random Forest hyperparameters
            n_estimators = row.get('hyperparam_n_estimators', '?')
            max_depth = row.get('hyperparam_max_depth', '?')
            return f"RF_estimators={n_estimators}_depth={max_depth}"
        
        elif self.model_name == "XGBoost":
            # Handle XGBoost hyperparameters
            n_estimators = row.get('hyperparam_n_estimators', '?')
            max_depth = row.get('hyperparam_max_depth', '?')
            learning_rate = row.get('hyperparam_learning_rate', '?')
            return f"XGB_estimators={n_estimators}_depth={max_depth}_lr={learning_rate}"
        
        else:
            # Generic fallback
            # todo: do teh rest of the models for the fallback here 
            hyperparams = []
            for col in row.index:
                if col.startswith('hyperparam_'):
                    param_name = col.replace('hyperparam_', '')
                    param_value = row[col]
                    hyperparams.append(f"{param_name}={param_value}")
            
            if hyperparams:
                return f"{self.model_name}_{'_'.join(hyperparams[:3])}"  # Limit to first 3 params
            else:
                return f"{self.model_name}_config"
