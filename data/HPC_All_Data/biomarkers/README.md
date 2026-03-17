# Biomarker Analysis

This folder contains all biomarker-related analysis, scripts, visualizations, and summaries.

## Overview

Analysis of EEG biomarkers distinguishing Alzheimer's from Control groups using 95 features extracted from processed EEG data. Focus on relative bandpower features.

## Key Findings

### Top 3 Biomarkers (Highest Effect Size)

1. **feature_38 = O2 × Alpha** (Cohen's d = 0.797)
   - Control: 0.106 vs Alzheimer's: 0.040
   - **90.7% relative difference** - Control has 2.7x higher values
   - Strongly **reduced** in Alzheimer's patients

2. **feature_58 = T5 × Alpha** (Cohen's d = 0.715)
   - Control: 0.092 vs Alzheimer's: 0.036
   - **86.2% relative difference** - Control has 2.5x higher values
   - Strongly **reduced** in Alzheimer's patients

3. **feature_34 = O1 × Alpha** (Cohen's d = 0.704)
   - Control: 0.095 vs Alzheimer's: 0.039
   - **83.9% relative difference** - Control has 2.4x higher values
   - Strongly **reduced** in Alzheimer's patients

### Pattern Analysis

**Alpha Band Reduction:**
- Multiple occipital and temporal channels show significant Alpha band reduction
- O1, O2, T5, T6, P3, P4, Pz all show reduced Alpha relative power
- Consistent with known Alzheimer's EEG patterns (posterior Alpha reduction)

**Delta Band Elevation:**
- Some channels show elevated Delta relative power in Alzheimer's
- May represent compensatory increases or pathological patterns

## Files

### Scripts

- **`explore_biomarkers.py`**: Initial biomarker exploration - loads parquet files, identifies relative bandpower features, calculates statistics
- **`map_features_to_channels_bands.py`**: Maps feature indices to channel×band combinations using real EEG processing pipeline
- **`visualize_biomarkers.py`**: Creates distribution plots, effect size plots, correlation heatmaps, and boxplots
- **`cluster_biomarkers.py`**: Performs clustering analysis on subjects using top biomarkers

### Data Files

- **`full_data_with_features.csv`**: Complete dataset with all 95 features extracted
- **`feature_statistics_by_group.csv`**: Statistical summary by group (Alzheimer's vs Control)
- **`interesting_features.csv`**: Features ranked by effect size (Cohen's d)
- **`interesting_features_mapped.csv`**: Top features with channel×band mapping
- **`feature_mapping.csv`**: Complete mapping of all 95 features to channel×band combinations
- **`subject_clusters.csv`**: Cluster assignments for each subject (from clustering analysis)
- **`exploration_summary.csv`**: Overall summary statistics

### Visualizations

- **`top_10_biomarkers_distributions.png`**: Distribution plots for top 10 biomarkers
- **`biomarker_effect_sizes.png`**: Effect size (Cohen's d) visualization
- **`biomarker_correlation_heatmap.png`**: Correlation matrix of top biomarkers
- **`biomarker_boxplots.png`**: Boxplots comparing groups for top biomarkers
- **`clustering_elbow_curve.png`**: Elbow curve and silhouette scores for optimal cluster selection
- **`clustering_analysis.png`**: Comprehensive clustering visualization (PCA, dendrogram, silhouette analysis)

### Documentation

- **`BIOMARKER_ANALYSIS.md`**: Detailed analysis report
- **`FEATURE_MAPPING_RESULTS.md`**: Feature mapping validation results
- **`BIOMARKER_EXPLORATION_SUMMARY.md`**: Executive summary

## Channel Mapping

The analysis uses 19 EEG channels in the following order (from MNE):
```
Fp1, Fp2, F3, F4, C3, C4, P3, P4, O1, O2, 
F7, F8, T3, T4, T5, T6, Fz, Cz, Pz
```

Frequency bands (in order):
```
Delta (0.5-4 Hz), Theta (4-8 Hz), Alpha (8-12 Hz), Beta (12-30 Hz)
```

Feature ordering:
1. **per_channel_per_band** features first (76 features = 19 channels × 4 bands × 1 feature)
   - Order: channel 0, band 0; channel 0, band 1; ... channel N, band M
2. **per_channel_across_bands** features second (19 features = 19 channels × 1 feature)
   - Order: channel 0; channel 1; ... channel 18

Total: 95 features

## Usage

### Run biomarker exploration:
```bash
python explore_biomarkers.py
```

### Map features to channels/bands:
```bash
python map_features_to_channels_bands.py
```

### Generate visualizations:
```bash
python visualize_biomarkers.py
```

### Perform clustering analysis:
```bash
python cluster_biomarkers.py
```

## Data Summary

- **Total epochs**: 33,014
- **Total subjects**: 65
- **Total features**: 95
- **Relative bandpower features**: 76 (values in [0,1] range)
- **Top biomarkers identified**: 95 features with significant group differences

## Key Insights

1. **Alpha band reduction** is the strongest biomarker pattern, particularly in posterior channels (O1, O2, P3, P4, Pz)
2. **Temporal channels** (T5, T6) also show significant Alpha reduction
3. **Delta band elevation** in some channels may indicate compensatory mechanisms
4. **Clustering analysis** reveals distinct subject groups based on biomarker profiles

---

*Analysis Date: December 2025*




