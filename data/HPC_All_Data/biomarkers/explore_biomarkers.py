#!/usr/bin/env python3
"""
Explore biomarkers in processed_subjects parquet files.
Focus on relative bandpower features and identify interesting columns.
"""

import pandas as pd
import numpy as np
import glob
from pathlib import Path
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

def load_all_parquet_files(data_dir: str) -> pd.DataFrame:
    """Load all parquet files and combine into single DataFrame."""
    parquet_files = sorted(glob.glob(str(Path(data_dir) / 'part-*.snappy.parquet')))
    print(f"📂 Found {len(parquet_files)} parquet files")
    
    dfs = []
    for i, file in enumerate(parquet_files):
        print(f"   Loading {i+1}/{len(parquet_files)}: {Path(file).name}")
        df = pd.read_parquet(file)
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"✅ Loaded {len(combined_df):,} total rows")
    return combined_df

def extract_features_to_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Extract features from dict structure to individual columns."""
    print("\n🔍 Extracting features from dict structure...")
    
    # Get feature vector from first row
    first_features = df['features'].iloc[0]
    if isinstance(first_features, dict) and 'values' in first_features:
        n_features = len(first_features['values'])
        print(f"   Feature vector length: {n_features}")
        
        # Extract all feature vectors
        feature_vectors = []
        for idx, row in df.iterrows():
            feat = row['features']
            if isinstance(feat, dict) and 'values' in feat:
                feature_vectors.append(feat['values'])
            else:
                feature_vectors.append(np.zeros(n_features))
        
        # Create feature matrix
        feature_matrix = np.array(feature_vectors)
        print(f"   Feature matrix shape: {feature_matrix.shape}")
        
        # Create feature column names (we'll try to infer or use generic names)
        # Since we don't have explicit feature names, we'll use generic names
        # and try to identify relative bandpower patterns
        feature_cols = [f'feature_{i}' for i in range(n_features)]
        
        # Create DataFrame with features as columns
        feature_df = pd.DataFrame(feature_matrix, columns=feature_cols)
        
        # Combine with metadata
        result_df = pd.concat([
            df[['SubjectID', 'EpochID', 'Group', 'label']].reset_index(drop=True),
            feature_df
        ], axis=1)
        
        return result_df, feature_cols
    else:
        raise ValueError("Features structure not recognized")

def identify_relative_bandpower_features(df: pd.DataFrame, feature_cols: List[str]) -> List[str]:
    """
    Identify relative bandpower features based on characteristics:
    - Values between 0 and 1
    - Sum to approximately 1 (within tolerance)
    - Multiple features per subject/epoch that sum to 1
    """
    print("\n🔬 Identifying relative bandpower features...")
    
    # Sample a few rows to check patterns
    sample_size = min(1000, len(df))
    sample_df = df[feature_cols].iloc[:sample_size]
    
    # Check which features are between 0 and 1
    in_range = (sample_df >= 0).all(axis=0) & (sample_df <= 1).all(axis=0)
    potential_rbp = [col for col, val in zip(feature_cols, in_range) if val]
    print(f"   Features in [0,1] range: {len(potential_rbp)}/{len(feature_cols)}")
    
    # Check which groups of features sum to ~1
    # This is trickier - we need to identify groups
    # Let's check if all features sum to 1 (suggesting they're all relative bandpower)
    row_sums = sample_df.sum(axis=1)
    mean_sum = row_sums.mean()
    std_sum = row_sums.std()
    
    print(f"   Mean row sum: {mean_sum:.4f} ± {std_sum:.4f}")
    
    if abs(mean_sum - 1.0) < 0.1:
        print("   ✅ All features appear to be relative bandpower (sum ≈ 1)")
        return potential_rbp
    else:
        print("   ⚠️  Features don't sum to 1 - may be mixed feature types")
        # Try to find subsets that sum to 1
        # This is more complex - for now, return all potential features
        return potential_rbp

def analyze_feature_statistics(df: pd.DataFrame, feature_cols: List[str], group_col: str = 'Group') -> pd.DataFrame:
    """Calculate statistics for each feature by group."""
    print("\n📊 Calculating feature statistics by group...")
    
    stats_list = []
    for col in feature_cols:
        for group in df[group_col].unique():
            group_data = df[df[group_col] == group][col]
            stats_list.append({
                'feature': col,
                'group': group,
                'mean': group_data.mean(),
                'std': group_data.std(),
                'median': group_data.median(),
                'min': group_data.min(),
                'max': group_data.max(),
                'q25': group_data.quantile(0.25),
                'q75': group_data.quantile(0.75),
            })
    
    stats_df = pd.DataFrame(stats_list)
    return stats_df

def find_interesting_features(stats_df: pd.DataFrame, min_effect_size: float = 0.1) -> pd.DataFrame:
    """
    Find features with interesting differences between groups.
    Uses Cohen's d as effect size measure.
    """
    print("\n🎯 Finding interesting features (features with group differences)...")
    
    interesting = []
    groups = stats_df['group'].unique()
    
    if len(groups) < 2:
        print("   ⚠️  Only one group found - cannot compare")
        return pd.DataFrame()
    
    for feature in stats_df['feature'].unique():
        feature_stats = stats_df[stats_df['feature'] == feature]
        
        if len(feature_stats) >= 2:
            group1_stats = feature_stats.iloc[0]
            group2_stats = feature_stats.iloc[1]
            
            # Calculate Cohen's d
            mean_diff = abs(group1_stats['mean'] - group2_stats['mean'])
            pooled_std = np.sqrt((group1_stats['std']**2 + group2_stats['std']**2) / 2)
            
            if pooled_std > 0:
                cohens_d = mean_diff / pooled_std
            else:
                cohens_d = 0
            
            # Calculate relative difference
            mean_avg = (group1_stats['mean'] + group2_stats['mean']) / 2
            if mean_avg > 0:
                rel_diff = mean_diff / mean_avg
            else:
                rel_diff = 0
            
            interesting.append({
                'feature': feature,
                'group1': group1_stats['group'],
                'group1_mean': group1_stats['mean'],
                'group2': group2_stats['group'],
                'group2_mean': group2_stats['mean'],
                'mean_diff': mean_diff,
                'cohens_d': cohens_d,
                'rel_diff_pct': rel_diff * 100,
                'group1_std': group1_stats['std'],
                'group2_std': group2_stats['std'],
            })
    
    interesting_df = pd.DataFrame(interesting)
    
    if len(interesting_df) > 0:
        # Sort by effect size
        interesting_df = interesting_df.sort_values('cohens_d', ascending=False)
        print(f"   Found {len(interesting_df)} features with group differences")
        print(f"   Top 10 by effect size (Cohen's d):")
        for idx, row in interesting_df.head(10).iterrows():
            print(f"      {row['feature']}: d={row['cohens_d']:.3f}, diff={row['mean_diff']:.4f} ({row['rel_diff_pct']:.1f}%)")
    
    return interesting_df

def save_results(df: pd.DataFrame, stats_df: pd.DataFrame, interesting_df: pd.DataFrame, 
                 output_dir: str):
    """Save results to CSV files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Saving results to {output_dir}...")
    
    # Save full data with features
    df.to_csv(output_path / 'full_data_with_features.csv', index=False)
    print(f"   ✅ Saved full_data_with_features.csv ({len(df):,} rows)")
    
    # Save statistics
    stats_df.to_csv(output_path / 'feature_statistics_by_group.csv', index=False)
    print(f"   ✅ Saved feature_statistics_by_group.csv")
    
    # Save interesting features
    if len(interesting_df) > 0:
        interesting_df.to_csv(output_path / 'interesting_features.csv', index=False)
        print(f"   ✅ Saved interesting_features.csv ({len(interesting_df)} features)")
    
    # Save summary
    summary = {
        'total_rows': len(df),
        'total_features': len([c for c in df.columns if c.startswith('feature_')]),
        'unique_subjects': df['SubjectID'].nunique(),
        'unique_epochs': df['EpochID'].nunique(),
        'groups': df['Group'].unique().tolist(),
        'top_10_features': interesting_df.head(10)['feature'].tolist() if len(interesting_df) > 0 else []
    }
    
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(output_path / 'exploration_summary.csv', index=False)
    print(f"   ✅ Saved exploration_summary.csv")

def main():
    """Main exploration function."""
    data_dir = Path(__file__).parent / 'processed_subjects'
    output_dir = Path(__file__).parent / 'biomarker_exploration'
    
    print("="*60)
    print("🔬 Biomarker Exploration: Relative Bandpower Analysis")
    print("="*60)
    
    # Load data
    df = load_all_parquet_files(str(data_dir))
    
    # Extract features
    df_with_features, feature_cols = extract_features_to_columns(df)
    
    # Identify relative bandpower features
    rbp_features = identify_relative_bandpower_features(df_with_features, feature_cols)
    print(f"\n📋 Identified {len(rbp_features)} potential relative bandpower features")
    
    # Calculate statistics
    stats_df = analyze_feature_statistics(df_with_features, feature_cols)
    
    # Find interesting features
    interesting_df = find_interesting_features(stats_df)
    
    # Save results
    save_results(df_with_features, stats_df, interesting_df, str(output_dir))
    
    print("\n" + "="*60)
    print("✅ Exploration complete!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Total rows: {len(df_with_features):,}")
    print(f"   Total features: {len(feature_cols)}")
    print(f"   Potential RBP features: {len(rbp_features)}")
    print(f"   Interesting features (group differences): {len(interesting_df)}")
    print(f"\n📁 Results saved to: {output_dir}")

if __name__ == '__main__':
    main()

