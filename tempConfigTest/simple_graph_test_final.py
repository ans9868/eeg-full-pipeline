#!/usr/bin/env python3

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os

print("🎨 Testing simple graph generation on demo1...")

# Load the model comparison data
try:
    df = pd.read_csv('data/demo1/ml_results/model_comparison.csv')
    print(f"✅ Loaded model comparison data: {len(df)} models")
    print(f"📊 Data columns: {list(df.columns)}")
    print(f"📊 Data:\n{df}")
    
    # Create a simple best models graph
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create vertical bar chart
    x_pos = np.arange(len(df))
    bars = ax.bar(x_pos, df['best_test_accuracy'], color='skyblue', alpha=0.8)
    
    # Customize the plot
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df['model_name'])
    ax.set_ylabel('Test Accuracy')
    ax.set_title('Best Model Performance Comparison')
    ax.set_ylim(0, 1.0)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, df['best_test_accuracy'])):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
               f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save the graph
    output_path = 'data/demo1/ml_results/graphs/best_models_comparison.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Best models graph saved to: {output_path}")
    
    # Check if file was created
    if os.path.exists(output_path):
        print("✅ Best models graph created successfully!")
        print(f"📊 File size: {os.path.getsize(output_path)} bytes")
    else:
        print("❌ Best models graph was not created")
        
    # Now test hyperparameter graph
    hyperparam_df = pd.read_csv('data/demo1/ml_results/KNN/hyperparameter_comparison.csv')
    print(f"✅ Loaded hyperparameter data: {len(hyperparam_df)} combinations")
    print(f"📊 Hyperparameter columns: {list(hyperparam_df.columns)}")
    
    # Create hyperparameter graph
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create hyperparameter names
    hyperparam_names = []
    for _, row in hyperparam_df.iterrows():
        n_neighbors = row.get('hyperparam_n_neighbors', '?')
        weights = row.get('hyperparam_weights', '?')
        metric = row.get('hyperparam_metric', '?')
        name = f"KNN_{metric}_n={n_neighbors}_w={weights}"
        hyperparam_names.append(name)
    
    # Create vertical bar chart
    x_pos = np.arange(len(hyperparam_df))
    bars = ax.bar(x_pos, hyperparam_df['mean_test_accuracy'], color='lightcoral', alpha=0.8)
    
    # Customize the plot
    ax.set_xticks(x_pos)
    ax.set_xticklabels(hyperparam_names, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Test Accuracy')
    ax.set_title('KNN Hyperparameter Performance Comparison')
    ax.set_ylim(0, 1.0)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, hyperparam_df['mean_test_accuracy'])):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
               f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save the graph
    output_path = 'data/demo1/ml_results/graphs/knn_hyperparameter_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Hyperparameter graph saved to: {output_path}")
    
    # Check if file was created
    if os.path.exists(output_path):
        print("✅ Hyperparameter graph created successfully!")
        print(f"📊 File size: {os.path.getsize(output_path)} bytes")
    else:
        print("❌ Hyperparameter graph was not created")
        
    # Check final results
    graphs_dir = 'data/demo1/ml_results/graphs'
    if os.path.exists(graphs_dir):
        print(f"📊 Final graphs directory contents: {os.listdir(graphs_dir)}")
    else:
        print("❌ No graphs directory created")
        
except Exception as e:
    print(f"💥 Error: {e}")
    import traceback
    traceback.print_exc()
