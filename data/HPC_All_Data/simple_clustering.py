#!/usr/bin/env python3
"""
Simple Clustering Analysis for EEG Alzheimer's Classification Data
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

# Create a log file to track execution
import logging
logging.basicConfig(filename='clustering_debug.log', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

print("🧠 Starting Simple EEG Clustering Analysis...")
logging.info("🧠 Starting Simple EEG Clustering Analysis...")

def load_and_cluster_subjects():
    """Simple subject clustering"""
    print("📊 Loading subject performance data...")
    logging.info("📊 Loading subject performance data...")

    try:
        df = pd.read_csv('analysis_1/ANOVA_L_6_Random_per_subject_summary.csv')
        print(f"✅ Loaded {len(df)} subjects")

        # Prepare data for clustering
        features = ['Median_Accuracy', 'Mean_Accuracy']
        X = df[features].values

        # Remove NaN values
        mask = ~np.isnan(X).any(axis=1)
        X_clean = X[mask]
        subjects_clean = df['Subject'][mask]

        print(f"✅ After cleaning: {len(X_clean)} subjects")

        if len(X_clean) < 3:
            print("❌ Not enough data for clustering")
            return

        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_clean)

        # K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        print(f"✅ Clustered into {len(np.unique(clusters))} groups")

        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Scatter plot
        scatter = ax1.scatter(X_clean[:, 0], X_clean[:, 1], c=clusters, cmap='viridis', alpha=0.7)
        ax1.set_xlabel('Median Accuracy')
        ax1.set_ylabel('Mean Accuracy')
        ax1.set_title('Subject Clusters (ANOVA_L_6_Random)')
        plt.colorbar(scatter, ax=ax1)

        # Cluster statistics
        df_clean = df.iloc[mask].copy()
        df_clean['cluster'] = clusters

        cluster_stats = df_clean.groupby('cluster')[features].mean()
        cluster_stats.plot(kind='bar', ax=ax2)
        ax2.set_title('Cluster Characteristics')
        ax2.set_ylabel('Accuracy')

        plt.tight_layout()
        plt.savefig('simple_subject_clusters.png', dpi=150, bbox_inches='tight')
        plt.close()

        print("✅ Saved visualization as 'simple_subject_clusters.png'")

        # Print cluster summary
        print("\n📈 CLUSTER SUMMARY:")
        for cluster_id in np.unique(clusters):
            cluster_data = df_clean[df_clean['cluster'] == cluster_id]
            print(f"Cluster {cluster_id}: {len(cluster_data)} subjects, "
                  f"Mean Acc: {cluster_data['Mean_Accuracy'].mean():.3f}")

        return df_clean

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def cluster_cross_model_swings():
    """Cluster subjects by performance variability"""
    print("\n📈 Analyzing cross-model performance swings...")

    try:
        df = pd.read_csv('cross_model_swings_summary.csv')
        print(f"✅ Loaded {len(df)} swing records")

        # Group by subject
        subject_swings = df.groupby('Subject').agg({
            'Swing': ['mean', 'max', 'std'],
            'Mean_Accuracy': 'mean'
        }).fillna(0)

        subject_swings.columns = ['mean_swing', 'max_swing', 'std_swing', 'mean_accuracy']

        print(f"✅ Aggregated {len(subject_swings)} subjects")

        # Prepare for clustering
        features = ['mean_swing', 'max_swing', 'std_swing', 'mean_accuracy']
        X = subject_swings[features].values

        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-means
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        print(f"✅ Clustered subjects by variability into {len(np.unique(clusters))} groups")

        # Visualization
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        scatter = ax.scatter(subject_swings['mean_swing'], subject_swings['mean_accuracy'],
                           c=clusters, cmap='plasma', alpha=0.7)
        ax.set_xlabel('Mean Performance Swing')
        ax.set_ylabel('Mean Accuracy')
        ax.set_title('Subject Clusters by Performance Variability')
        plt.colorbar(scatter, ax=ax)

        plt.tight_layout()
        plt.savefig('subject_variability_simple.png', dpi=150, bbox_inches='tight')
        plt.close()

        print("✅ Saved visualization as 'subject_variability_simple.png'")

        # Print summary
        print("\n📊 VARIABILITY CLUSTER SUMMARY:")
        subject_swings['cluster'] = clusters
        for cluster_id in np.unique(clusters):
            cluster_data = subject_swings[subject_swings['cluster'] == cluster_id]
            print(f"Cluster {cluster_id}: {len(cluster_data)} subjects, "
                  f"Avg Swing: {cluster_data['mean_swing'].mean():.3f}, "
                  f"Avg Acc: {cluster_data['mean_accuracy'].mean():.3f}")

        return subject_swings

    except Exception as e:
        print(f"❌ Error in swing analysis: {e}")
        return None

def main():
    print("🧠 EEG Alzheimer's Classification - Simple Clustering Analysis")
    print("=" * 60)

    # Run clustering analyses
    subject_clusters = load_and_cluster_subjects()
    swing_clusters = cluster_cross_model_swings()

    print("\n🎉 SIMPLE CLUSTERING ANALYSIS COMPLETE!")
    print("📁 Check the generated PNG files")

if __name__ == "__main__":
    main()





