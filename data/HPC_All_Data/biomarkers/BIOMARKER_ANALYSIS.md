# Biomarker Analysis: Relative Bandpower Features

## Overview
Analysis of 95 features extracted from processed EEG data to identify biomarkers distinguishing Alzheimer's (alz) from Control (cntrl) groups.

**Data Summary:**
- Total rows: 33,014 epochs
- Total features: 95
- Unique subjects: 65
- Unique epochs: 857
- Groups: alz (Alzheimer's), cntrl (Control)

---

## Key Findings

### Top Biomarkers by Effect Size (Cohen's d)

#### 1. **feature_38** ⭐⭐⭐ (d=0.797, 90.7% relative difference)
- **Alzheimer's mean**: 0.040
- **Control mean**: 0.106
- **Difference**: Control has **2.7x higher** values
- **Interpretation**: This feature is significantly **reduced** in Alzheimer's patients
- **Potential**: Strong biomarker candidate

#### 2. **feature_58** ⭐⭐⭐ (d=0.715, 86.2% relative difference)
- **Alzheimer's mean**: 0.036
- **Control mean**: 0.092
- **Difference**: Control has **2.5x higher** values
- **Interpretation**: Also **reduced** in Alzheimer's patients
- **Potential**: Strong biomarker candidate

#### 3. **feature_34** ⭐⭐⭐ (d=0.704, 83.9% relative difference)
- **Alzheimer's mean**: 0.039
- **Control mean**: 0.095
- **Difference**: Control has **2.4x higher** values
- **Interpretation**: Also **reduced** in Alzheimer's patients
- **Potential**: Strong biomarker candidate

#### 4. **feature_36** ⭐⭐ (d=0.603, 7.3% relative difference)
- **Alzheimer's mean**: 0.889
- **Control mean**: 0.826
- **Difference**: Alzheimer's has **7.5% higher** values
- **Interpretation**: This feature is **elevated** in Alzheimer's patients
- **Potential**: Moderate biomarker candidate

#### 5. **feature_62** ⭐⭐ (d=0.602, 68.2% relative difference)
- **Alzheimer's mean**: 0.038
- **Control mean**: 0.077
- **Difference**: Control has **2.0x higher** values
- **Interpretation**: **Reduced** in Alzheimer's patients
- **Potential**: Moderate biomarker candidate

---

## Pattern Analysis

### Features Reduced in Alzheimer's (Control > Alzheimer's)
These features show **lower values** in Alzheimer's patients:
- feature_38, feature_58, feature_34, feature_62, feature_26, feature_74, feature_30
- **Pattern**: Multiple features showing similar reduction pattern
- **Clinical significance**: May represent loss of specific frequency bands or channels

### Features Elevated in Alzheimer's (Alzheimer's > Control)
These features show **higher values** in Alzheimer's patients:
- feature_36, feature_32, feature_56, feature_60
- **Pattern**: These features have high baseline values (0.82-0.89)
- **Clinical significance**: May represent compensatory increases or pathological patterns

---

## Statistical Summary

### Effect Size Distribution
- **Large effect (d > 0.5)**: 8 features
- **Medium effect (0.3 < d < 0.5)**: ~15 features
- **Small effect (d < 0.3)**: Remaining features

### Feature Characteristics
- **76/95 features** are in [0,1] range (potential relative bandpower)
- **19/95 features** are outside [0,1] range (may be absolute power or other features)
- **Mean row sum**: 19.0 (suggests mixed feature types, not all relative bandpower)

---

## Recommendations

### High Priority Biomarkers
1. **feature_38**: Highest effect size, 90.7% relative difference
2. **feature_58**: Second highest, 86.2% relative difference
3. **feature_34**: Third highest, 83.9% relative difference

### Next Steps
1. **Identify feature names**: Map feature indices to actual channel×band combinations
2. **Biological interpretation**: Determine which frequency bands/channels these represent
3. **Validation**: Test these biomarkers on independent dataset
4. **Clinical correlation**: Link to known Alzheimer's EEG patterns (e.g., alpha reduction, delta increase)

---

## Notes

- Features are currently labeled as `feature_0` through `feature_94`
- Need to map these to actual channel×band×feature_type combinations
- 76 features appear to be relative bandpower (values in [0,1])
- 19 features may be absolute power or other feature types
- All 95 features show some group difference (Cohen's d > 0)

---

*Analysis Date: December 12, 2025*  
*Data Source: processed_subjects parquet files*  
*Analysis Script: explore_biomarkers.py*

