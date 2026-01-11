# Biomarker Exploration Summary

## Overview
Explored 95 features from processed EEG data to identify biomarkers distinguishing Alzheimer's from Control groups. Analysis focused on relative bandpower features.

## Key Findings

### Top 3 Biomarkers (Highest Effect Size)

1. **feature_38** (Cohen's d = 0.797)
   - Control: 0.106 vs Alzheimer's: 0.040
   - **90.7% relative difference** - Control has 2.7x higher values
   - Strongly **reduced** in Alzheimer's patients

2. **feature_58** (Cohen's d = 0.715)
   - Control: 0.092 vs Alzheimer's: 0.036
   - **86.2% relative difference** - Control has 2.5x higher values
   - Strongly **reduced** in Alzheimer's patients

3. **feature_34** (Cohen's d = 0.704)
   - Control: 0.095 vs Alzheimer's: 0.039
   - **83.9% relative difference** - Control has 2.4x higher values
   - Strongly **reduced** in Alzheimer's patients

### Pattern Analysis

**Features Reduced in Alzheimer's:**
- Multiple features (38, 58, 34, 62, 26, 74, 30) show significant reduction
- May represent loss of specific frequency bands or channels

**Features Elevated in Alzheimer's:**
- Features 36, 32, 56, 60 show elevation (high baseline values ~0.82-0.89)
- May represent compensatory increases or pathological patterns

## Data Summary

- **Total epochs**: 33,014
- **Total features**: 95
- **Unique subjects**: 65
- **Potential RBP features**: 76 (values in [0,1] range)
- **Features with group differences**: All 95 features

## Next Steps

1. **Map feature indices to channel×band combinations** to identify which EEG channels/frequency bands these represent
2. **Biological interpretation** - link to known Alzheimer's EEG patterns
3. **Validation** on independent dataset
4. **Clinical correlation** with disease severity/progression

## Files Generated

- `full_data_with_features.csv` - Complete dataset with extracted features
- `feature_statistics_by_group.csv` - Statistical summary by group
- `interesting_features.csv` - Features ranked by effect size
- `exploration_summary.csv` - Overall summary
- Visualization plots (PNG files)

## Location

All analysis files in: `data/HPC_All_Data/biomarker_exploration/`

---

*Analysis Date: December 12, 2025*



