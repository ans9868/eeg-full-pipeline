#!/usr/bin/env python3
"""
Apply fixes to biomarker analysis:
1. FDR correction on 95 tests
2. Create Top 10 clean table
3. Fix percent math, use ratios
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

def apply_fdr_correction(interesting_df):
    """Apply FDR correction to p-values."""
    print("🔬 Applying FDR correction...")
    
    # Calculate p-values from Cohen's d (approximate)
    # Using t-test approximation: t = d * sqrt(n/2), then p from t
    # For large samples, we can approximate
    
    # We need actual p-values - let's calculate from the data
    # For now, we'll use a conservative approach: assume all tests were done
    # and use Benjamini-Hochberg FDR
    
    # Since we don't have raw p-values, we'll estimate from effect sizes
    # This is approximate - ideally we'd have the actual test results
    
    # Load full data to calculate actual p-values
    print("   Loading full data to calculate p-values...")
    df = pd.read_csv('full_data_with_features.csv')
    
    # Calculate p-values for each feature
    p_values = []
    feature_names = []
    
    for _, row in interesting_df.iterrows():
        feature = row['feature']
        alz_data = df[df['Group'] == 'alz'][feature]
        cntrl_data = df[df['Group'] == 'cntrl'][feature]
        
        # Welch's t-test (unequal variances)
        t_stat, p_val = stats.ttest_ind(alz_data, cntrl_data, equal_var=False)
        p_values.append(p_val)
        feature_names.append(feature)
    
    # Apply FDR correction
    rejected, p_corrected, _, _ = multipletests(
        p_values, 
        alpha=0.05, 
        method='fdr_bh'
    )
    
    # Add to dataframe
    interesting_df['p_value'] = p_values
    interesting_df['p_corrected'] = p_corrected
    interesting_df['fdr_significant'] = rejected
    
    n_significant = rejected.sum()
    print(f"   ✅ {n_significant}/{len(interesting_df)} features significant after FDR correction (q=0.05)")
    
    return interesting_df

def create_top10_table(interesting_df):
    """Create clean Top 10 table with means, ratios, Cohen's d."""
    print("\n📊 Creating Top 10 reference table...")
    
    top10 = interesting_df.head(10).copy()
    
    # Calculate ratios (Control / Alzheimer's for Alpha, Alzheimer's / Control for Delta)
    ratios = []
    for _, row in top10.iterrows():
        if 'Alpha' in str(row.get('band_name', '')) or 'Beta' in str(row.get('band_name', '')):
            # For Alpha/Beta: Control / Alzheimer's (higher in control)
            ratio = row['group2_mean'] / row['group1_mean'] if row['group1_mean'] > 0 else np.nan
        else:
            # For Delta: Alzheimer's / Control (higher in Alzheimer's)
            ratio = row['group1_mean'] / row['group2_mean'] if row['group2_mean'] > 0 else np.nan
        ratios.append(ratio)
    
    top10['ratio'] = ratios
    
    # Create clean table
    table_data = []
    for _, row in top10.iterrows():
        feature_name = f"{row['channel_name']} × {row['band_name']}"
        table_data.append({
            'Feature': feature_name,
            'Mean_AD': f"{row['group1_mean']:.4f}",
            'Mean_Control': f"{row['group2_mean']:.4f}",
            'Ratio': f"{row['ratio']:.2f}",
            "Cohen's_d": f"{row['cohens_d']:.3f}",
            'FDR_Sig': '✓' if row.get('fdr_significant', False) else ''
        })
    
    table_df = pd.DataFrame(table_data)
    
    return table_df

def main():
    """Apply fixes to analysis."""
    print("="*60)
    print("🔧 Applying Analysis Fixes")
    print("="*60)
    
    # Load data
    interesting_df = pd.read_csv('interesting_features_mapped.csv')
    
    # Apply FDR correction
    interesting_df = apply_fdr_correction(interesting_df)
    
    # Save updated file
    interesting_df.to_csv('interesting_features_mapped_fdr.csv', index=False)
    print("\n💾 Saved interesting_features_mapped_fdr.csv")
    
    # Create Top 10 table
    top10_table = create_top10_table(interesting_df)
    top10_table.to_csv('top10_biomarkers_table.csv', index=False)
    print("💾 Saved top10_biomarkers_table.csv")
    
    # Print table
    print("\n📋 Top 10 Biomarkers Reference Table:")
    print("="*80)
    print(top10_table.to_string(index=False))
    
    print("\n✅ Analysis fixes complete!")

if __name__ == '__main__':
    main()




