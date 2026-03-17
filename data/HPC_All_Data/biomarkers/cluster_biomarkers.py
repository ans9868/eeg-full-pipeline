#!/usr/bin/env python3
"""
Clustering visualization for biomarker features.
Performs clustering analysis on subjects using top biomarkers.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import umap
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def load_data():
    """Load the biomarker data."""
    data_dir = Path(__file__).parent
    df = pd.read_csv(data_dir / 'full_data_with_features.csv')
    interesting = pd.read_csv(data_dir / 'interesting_features_mapped.csv')
    feature_mapping = pd.read_csv(data_dir / 'feature_mapping.csv')
    return df, interesting, feature_mapping

def get_feature_name(feature_col, feature_mapping_df):
    """Get actual feature name (channel×band) from feature column name."""
    # Extract feature index from column name like "feature_38"
    if feature_col.startswith('feature_'):
        feat_idx = int(feature_col.split('_')[1])
        mapping = feature_mapping_df[feature_mapping_df['feature_index'] == feat_idx]
        if len(mapping) > 0:
            row = mapping.iloc[0]
            if row['feature_type'] == 'relative_band_power':
                return f"{row['channel_name']} × {row['band_name']}"
            elif row['feature_type'] == 'band_power':
                return f"{row['channel_name']} (all bands)"
            else:
                return f"{row['channel_name']} × {row['band_name']}"
    return feature_col

def prepare_clustering_data(df, interesting_df, feature_mapping_df, n_features=20, aggregation='mean'):
    """
    Prepare data for clustering.
    
    Args:
        df: Full data with features
        interesting_df: Mapped interesting features
        feature_mapping_df: Feature mapping with channel×band names
        n_features: Number of top features to use
        aggregation: How to aggregate epochs per subject ('mean', 'median', 'std')
    """
    print(f"📊 Preparing clustering data (using top {n_features} features)...")
    
    # Get top features
    top_features = interesting_df.head(n_features)['feature'].tolist()
    
    # Get actual feature names
    feature_names = [get_feature_name(f, feature_mapping_df) for f in top_features]
    
    # Aggregate by subject
    if aggregation == 'mean':
        subject_data = df.groupby(['SubjectID', 'Group'])[top_features].mean().reset_index()
    elif aggregation == 'median':
        subject_data = df.groupby(['SubjectID', 'Group'])[top_features].median().reset_index()
    elif aggregation == 'std':
        subject_data = df.groupby(['SubjectID', 'Group'])[top_features].std().reset_index()
    else:
        raise ValueError(f"Unknown aggregation: {aggregation}")
    
    # Rename columns to use actual feature names
    rename_dict = {old: new for old, new in zip(top_features, feature_names)}
    subject_data = subject_data.rename(columns=rename_dict)
    
    print(f"   Subjects: {len(subject_data)}")
    print(f"   Features: {len(top_features)}")
    print(f"   Top features: {', '.join(feature_names[:5])}...")
    
    # Separate features and metadata
    X = subject_data[feature_names].values
    subject_ids = subject_data['SubjectID'].values
    groups = subject_data['Group'].values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, subject_ids, groups, feature_names, subject_data

def find_optimal_clusters(X, max_k=8):
    """Find optimal number of clusters using elbow method and silhouette score."""
    print("\n🔍 Finding optimal number of clusters...")
    
    inertias = []
    silhouette_scores = []
    k_range = range(2, max_k + 1)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))
        print(f"   k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={silhouette_scores[-1]:.3f}")
    
    # Find optimal k (highest silhouette score)
    optimal_k = k_range[np.argmax(silhouette_scores)]
    print(f"   ✅ Optimal k={optimal_k} (highest silhouette score)")
    
    return k_range, inertias, silhouette_scores, optimal_k

def plot_cluster_analysis(X, subject_ids, groups, top_features, subject_data, n_clusters=3, use_umap=False):
    """Perform and visualize clustering analysis."""
    print(f"\n🎯 Performing clustering analysis (k={n_clusters})...")
    
    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X)
    
    # Add cluster labels to subject data
    subject_data['Cluster'] = cluster_labels
    
    # Dimensionality reduction for visualization
    if use_umap:
        print("   Computing UMAP embedding...")
        reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.1)
        X_2d = reducer.fit_transform(X)
        x_label = 'UMAP 1'
        y_label = 'UMAP 2'
        title_suffix = 'UMAP Projection'
    else:
        pca = PCA(n_components=2, random_state=42)
        X_2d = pca.fit_transform(X)
        x_label = f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)'
        y_label = f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)'
        title_suffix = 'PCA Projection'
        print(f"   PCA explained variance: {pca.explained_variance_ratio_.sum():.2%}")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    
    # Plot 1: 2D scatter with clusters
    ax1 = plt.subplot(2, 3, 1)
    scatter = ax1.scatter(X_2d[:, 0], X_2d[:, 1], c=cluster_labels, 
                        cmap='viridis', s=100, alpha=0.6, edgecolors='black', linewidth=1)
    ax1.set_xlabel(x_label, fontsize=12)
    ax1.set_ylabel(y_label, fontsize=12)
    ax1.set_title(f'K-Means Clustering (k={n_clusters}) - {title_suffix}', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='Cluster')
    
    # Plot 2: 2D scatter with true groups
    ax2 = plt.subplot(2, 3, 2)
    group_colors = {'alz': 'red', 'cntrl': 'blue'}
    for group in ['alz', 'cntrl']:
        mask = groups == group
        ax2.scatter(X_2d[mask, 0], X_2d[mask, 1], 
                   c=group_colors[group], label=group.upper(), 
                   s=100, alpha=0.6, edgecolors='black', linewidth=1)
    ax2.set_xlabel(x_label, fontsize=12)
    ax2.set_ylabel(y_label, fontsize=12)
    ax2.set_title(f'True Group Labels - {title_suffix}', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Cluster vs Group comparison
    ax3 = plt.subplot(2, 3, 3)
    cluster_group_crosstab = pd.crosstab(subject_data['Cluster'], subject_data['Group'])
    cluster_group_crosstab.plot(kind='bar', ax=ax3, color=['red', 'blue'], alpha=0.7)
    ax3.set_xlabel('Cluster', fontsize=12)
    ax3.set_ylabel('Count', fontsize=12)
    ax3.set_title('Cluster Composition by Group', fontsize=14, fontweight='bold')
    ax3.legend(title='Group')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0)
    
    # Plot 4: Cluster centers in feature space (top 10 features)
    ax4 = plt.subplot(2, 3, 4)
    top_10_features = top_features[:10]
    cluster_centers = kmeans.cluster_centers_[:, :10]
    x_pos = np.arange(len(top_10_features))
    width = 0.25
    
    for i in range(n_clusters):
        offset = (i - n_clusters/2 + 0.5) * width
        ax4.bar(x_pos + offset, cluster_centers[i], width, 
               label=f'Cluster {i}', alpha=0.7)
    
    ax4.set_xlabel('Feature', fontsize=12)
    ax4.set_ylabel('Standardized Feature Value', fontsize=12)
    ax4.set_title('Cluster Centers (Top 10 Features)', fontsize=14, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(top_10_features, rotation=45, ha='right', fontsize=9)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Plot 5: Hierarchical clustering dendrogram (sample)
    ax5 = plt.subplot(2, 3, 5)
    from scipy.cluster.hierarchy import dendrogram, linkage
    # Use a sample for dendrogram (too many points otherwise)
    sample_size = min(30, len(X))
    sample_indices = np.random.choice(len(X), sample_size, replace=False)
    X_sample = X[sample_indices]
    
    linkage_matrix = linkage(X_sample, method='ward')
    dendrogram(linkage_matrix, ax=ax5, leaf_rotation=90, leaf_font_size=8)
    ax5.set_title(f'Hierarchical Clustering (Sample of {sample_size} subjects)', 
                 fontsize=14, fontweight='bold')
    ax5.set_xlabel('Subject (sample)', fontsize=12)
    ax5.set_ylabel('Distance', fontsize=12)
    
    # Plot 6: Silhouette analysis
    ax6 = plt.subplot(2, 3, 6)
    from sklearn.metrics import silhouette_samples
    silhouette_vals = silhouette_samples(X, cluster_labels)
    y_lower = 10
    
    for i in range(n_clusters):
        cluster_silhouette_vals = silhouette_vals[cluster_labels == i]
        cluster_silhouette_vals.sort()
        size_cluster_i = cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i
        
        ax6.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_silhouette_vals,
                         alpha=0.7)
        ax6.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10
    
    ax6.set_xlabel('Silhouette Coefficient', fontsize=12)
    ax6.set_ylabel('Cluster Label', fontsize=12)
    ax6.set_title('Silhouette Analysis', fontsize=14, fontweight='bold')
    ax6.axvline(x=silhouette_score(X, cluster_labels), color='red', 
               linestyle='--', label=f'Avg: {silhouette_score(X, cluster_labels):.3f}')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    projection_type = 'UMAP' if use_umap else 'PCA'
    plt.suptitle(f'Biomarker Clustering Analysis (k={n_clusters}, {projection_type})', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    return fig, subject_data, cluster_labels

def plot_elbow_curve(k_range, inertias, silhouette_scores, optimal_k):
    """Plot elbow curve and silhouette scores."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Elbow curve
    ax1.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
    ax1.axvline(x=optimal_k, color='r', linestyle='--', linewidth=2, label=f'Optimal k={optimal_k}')
    ax1.set_xlabel('Number of Clusters (k)', fontsize=12)
    ax1.set_ylabel('Inertia', fontsize=12)
    ax1.set_title('Elbow Method', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Silhouette scores
    ax2.plot(k_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
    ax2.axvline(x=optimal_k, color='r', linestyle='--', linewidth=2, label=f'Optimal k={optimal_k}')
    ax2.set_xlabel('Number of Clusters (k)', fontsize=12)
    ax2.set_ylabel('Silhouette Score', fontsize=12)
    ax2.set_title('Silhouette Score', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def main():
    """Generate clustering visualizations."""
    print("="*60)
    print("🎯 Biomarker Clustering Analysis")
    print("="*60)
    
    # Load data
    print("\n📂 Loading data...")
    df, interesting_df, feature_mapping_df = load_data()
    
    # Prepare clustering data
    X, subject_ids, groups, top_features, subject_data = prepare_clustering_data(
        df, interesting_df, feature_mapping_df, n_features=20, aggregation='mean'
    )
    
    # Find optimal clusters
    k_range, inertias, silhouette_scores, optimal_k = find_optimal_clusters(X, max_k=6)
    
    # Plot elbow curve
    print("\n📊 Creating elbow curve plot...")
    fig_elbow = plot_elbow_curve(k_range, inertias, silhouette_scores, optimal_k)
    
    # Perform clustering with optimal k (PCA)
    print(f"\n🎯 Performing clustering with k={optimal_k} (PCA)...")
    fig_clusters_pca, subject_data_clustered_pca, cluster_labels_pca = plot_cluster_analysis(
        X, subject_ids, groups, top_features, subject_data.copy(), n_clusters=optimal_k, use_umap=False
    )
    
    # Perform clustering with optimal k (UMAP)
    print(f"\n🎯 Performing clustering with k={optimal_k} (UMAP)...")
    fig_clusters_umap, subject_data_clustered_umap, cluster_labels_umap = plot_cluster_analysis(
        X, subject_ids, groups, top_features, subject_data.copy(), n_clusters=optimal_k, use_umap=True
    )
    
    # Perform clustering with different k values (4, 5, 6, 7) - PCA
    k_values = [4, 5, 6, 7]
    figs_kmeans_pca = []
    figs_kmeans_umap = []
    
    for k in k_values:
        print(f"\n🎯 Performing clustering with k={k} (PCA)...")
        fig_k_pca, subject_data_k_pca, cluster_labels_k_pca = plot_cluster_analysis(
            X, subject_ids, groups, top_features, subject_data.copy(), n_clusters=k, use_umap=False
        )
        figs_kmeans_pca.append((k, fig_k_pca, subject_data_k_pca))
        
        print(f"\n🎯 Performing clustering with k={k} (UMAP)...")
        fig_k_umap, subject_data_k_umap, cluster_labels_k_umap = plot_cluster_analysis(
            X, subject_ids, groups, top_features, subject_data.copy(), n_clusters=k, use_umap=True
        )
        figs_kmeans_umap.append((k, fig_k_umap, subject_data_k_umap))
    
    # Save results
    output_dir = Path(__file__).parent
    print(f"\n💾 Saving results to {output_dir}...")
    
    fig_elbow.savefig(output_dir / 'clustering_elbow_curve.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved clustering_elbow_curve.png")
    
    fig_clusters_pca.savefig(output_dir / 'clustering_analysis_k3_pca.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved clustering_analysis_k3_pca.png")
    
    fig_clusters_umap.savefig(output_dir / 'clustering_analysis_k3_umap.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved clustering_analysis_k3_umap.png")
    
    # Save individual k-means visualizations (PCA)
    for k, fig_k, subject_data_k in figs_kmeans_pca:
        filename = f'clustering_analysis_k{k}_pca.png'
        fig_k.savefig(output_dir / filename, dpi=300, bbox_inches='tight')
        print(f"   ✅ Saved {filename}")
    
    # Save individual k-means visualizations (UMAP)
    for k, fig_k, subject_data_k in figs_kmeans_umap:
        filename = f'clustering_analysis_k{k}_umap.png'
        fig_k.savefig(output_dir / filename, dpi=300, bbox_inches='tight')
        print(f"   ✅ Saved {filename}")
    
    # Save cluster assignments (using optimal k)
    subject_data_clustered_pca.to_csv(output_dir / 'subject_clusters.csv', index=False)
    print("   ✅ Saved subject_clusters.csv")
    
    # Print cluster summaries
    print("\n📊 Cluster Summary (k=3, optimal):")
    print("="*60)
    cluster_summary = subject_data_clustered_pca.groupby(['Cluster', 'Group']).size().unstack(fill_value=0)
    print(cluster_summary)
    
    for k, _, subject_data_k in figs_kmeans_pca:
        print(f"\n📊 Cluster Summary (k={k}):")
        print("="*60)
        cluster_summary_k = subject_data_k.groupby(['Cluster', 'Group']).size().unstack(fill_value=0)
        print(cluster_summary_k)
    
    print("\n✅ Clustering analysis complete!")

if __name__ == '__main__':
    main()

