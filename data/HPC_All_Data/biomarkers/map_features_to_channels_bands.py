#!/usr/bin/env python3
"""
Map feature indices to channel×band combinations based on the pipeline code structure.

From process_epoch_ml in eeg_spark_etl/processing/process_epoch.py:
1. First: per_channel_per_band features (relative_band_power)
   - Loop: channels (in order), then bands (in order from freq_bands.items()), then feature names
2. Second: per_channel_across_bands features (band_power)
   - Loop: channels (in order), then feature names

Config:
- Bands: Delta (0.5-4), Theta (4-8), Alpha (8-12), Beta (12-30) - 4 bands
- per_channel_per_band: relative_band_power (1 feature)
- per_channel_across_bands: band_power (1 feature)
- Total: 95 features = 19 channels * 4 bands * 1 feature + 19 channels * 1 feature
"""

import pandas as pd
import sys
import numpy as np
from pathlib import Path

# Add path to import processing functions
base_path = Path(__file__).parent.parent.parent.parent
sys.path.append(str(base_path / 'eeg-pyspark-pipeline'))

try:
    import mne
    from eeg_spark_etl.processing.process_epoch import process_epoch_ml, pre_calculate_all_band_powers
    PROCESSING_AVAILABLE = True
except ImportError as e:
    PROCESSING_AVAILABLE = False
    print(f"⚠️  Warning: Could not import processing functions: {e}")

def get_real_channel_names_from_processing():
    """
    Get real channel names by loading an actual EEG file with the full electrode set.
    Uses MNE to extract channel names directly from the EEG file.
    """
    if not PROCESSING_AVAILABLE:
        raise ImportError("Cannot get real channel names - processing functions not available")
    
    # Use the real EEG file with full electrode set
    real_eeg_path = '/Users/user/bigData/ds004504-download/sub-001/eeg/sub-001_task-eyesclosed_eeg.set'
    
    if not Path(real_eeg_path).exists():
        raise FileNotFoundError(f"Real EEG file not found: {real_eeg_path}")
    
    print(f"   📂 Loading real EEG file with full electrode set: {Path(real_eeg_path).name}")
    
    # Load raw EEG file and get channel names directly from MNE
    raw = mne.io.read_raw_eeglab(real_eeg_path, preload=False, verbose=False)
    channel_names = raw.ch_names
    
    print(f"   ✅ Extracted {len(channel_names)} channel names from MNE: {', '.join(channel_names[:5])}...")
    
    # Validate processing pipeline works with these channel names
    print(f"   🔍 Validating processing pipeline...")
    
    # Load full data for processing validation
    raw = mne.io.read_raw_eeglab(real_eeg_path, preload=True, verbose=False)
    
    # Create epochs (matching the config: window_size=3.0, sliding_window=0.5)
    epochs = mne.make_fixed_length_epochs(
        raw,
        duration=3.0,
        overlap=2.5,  # sliding_window=0.5 means 0.5s overlap, so 3.0-0.5=2.5s step
        preload=True,
        verbose=False
    )
    epochs.drop_bad(verbose=False)
    
    if len(epochs) == 0:
        raise ValueError("No epochs created from EEG file")
    
    # Use first epoch
    epoch = epochs[0]
    
    # Process with exact same config as biomarker analysis
    freq_bands = {
        'Delta': [0.5, 4],
        'Theta': [4, 8],
        'Alpha': [8, 12],
        'Beta': [12, 30]
    }
    
    # Get epoch data
    epoch_data = epoch.get_data()[0]  # (channels, time_points)
    
    # Calculate PSD (matching config: method='welch', normalize_psd='Yes')
    fmin = min(band_range[0] for band_range in freq_bands.values())
    fmax = max(band_range[1] for band_range in freq_bands.values())
    epoch_psd = epoch.compute_psd(fmin=fmin, fmax=fmax, verbose=False, method='welch', n_jobs=1)
    epoch_psd_data = epoch_psd.get_data()[0]  # (channels, frequencies)
    freqs = epoch_psd.freqs
    
    # Normalize PSD (matching config: normalize_psd='Yes')
    epoch_psd_data = epoch_psd_data / np.sum(epoch_psd_data, axis=-1, keepdims=True)
    
    # Process with exact config
    selected_features = {
        'per_channel_per_band': ['relative_band_power'],
        'per_channel_across_bands': ['band_power']
    }
    
    # Process epoch to validate pipeline works
    rows = list(process_epoch_ml(
        epoch_id=0,
        subject_id='test',
        epoch_data=epoch_data,
        epoch_psd_data=epoch_psd_data,
        freqs=freqs,
        freq_bands=freq_bands,
        channel_names=channel_names,
        selected_features=selected_features,
        group='test'
    ))
    
    # Verify processing works
    row = rows[0]
    features_vector = row.features
    if hasattr(features_vector, 'values'):
        feature_values = features_vector.values
    else:
        feature_values = np.array(features_vector)
    
    print(f"   ✅ Processing pipeline validated: {len(feature_values)} features from {len(channel_names)} channels")
    
    # Validate channel order by checking known feature positions
    # Feature order: channel 0, band 0; channel 0, band 1; ... channel N, band M
    # Known biomarker: feature_38 = O2 × Alpha (from biomarker analysis)
    # O2 should be at channel index 9, Alpha is band index 2 (Delta=0, Theta=1, Alpha=2, Beta=3)
    # Expected: feature_38 = 9 * 4 + 2 = 38
    n_bands = len(freq_bands)
    bands_list = list(freq_bands.keys())  # ['Delta', 'Theta', 'Alpha', 'Beta']
    
    if 'O2' in channel_names and 'Alpha' in bands_list:
        o2_idx = channel_names.index('O2')
        alpha_idx = bands_list.index('Alpha')
        expected_o2_alpha_idx = o2_idx * n_bands + alpha_idx
        print(f"   🔍 Validating channel order: O2 (idx={o2_idx}) × Alpha (idx={alpha_idx}) = feature_{expected_o2_alpha_idx}")
        
        if expected_o2_alpha_idx < len(feature_values):
            print(f"   ✅ Channel order validated: feature_{expected_o2_alpha_idx} = O2 × Alpha")
        else:
            print(f"   ⚠️  Warning: Expected feature_{expected_o2_alpha_idx} but only {len(feature_values)} features")
    
    print(f"   ✅ Channel order: {', '.join(channel_names[:5])}... ({len(channel_names)} total)")
    
    return channel_names

def create_feature_mapping(channel_names: list = None):
    """Create mapping from feature index to channel×band combination."""
    
    # From config
    bands = ['Delta', 'Theta', 'Alpha', 'Beta']  # 4 bands in order
    n_bands = len(bands)
    
    # Calculate number of channels
    total_features = 95
    # Features = n_channels * n_bands * n_per_channel_per_band_features + n_channels * n_per_channel_across_bands_features
    # 95 = n_channels * 4 * 1 + n_channels * 1
    # 95 = n_channels * 5
    n_channels = total_features // 5  # 19 channels
    
    # Use provided channel names or get real ones from actual processing
    if channel_names is None:
        try:
            channel_names = get_real_channel_names_from_processing()
        except Exception as e:
            print(f"   ❌ Error getting real channel names: {e}")
            raise
    
    # Validate channel count matches
    if len(channel_names) != n_channels:
        raise ValueError(
            f"Channel count mismatch! Expected {n_channels} channels (from 95 features), "
            f"but got {len(channel_names)} channels from EEG file. "
            f"The processed data may have been created with a different number of channels."
        )
    
    # Create mapping
    feature_mapping = []
    
    # Part 1: per_channel_per_band features (relative_band_power)
    # Order: channel 0, band 0; channel 0, band 1; ... channel 0, band 3; channel 1, band 0; ...
    feature_idx = 0
    for channel_idx in range(n_channels):
        for band_idx, band_name in enumerate(bands):
            feature_mapping.append({
                'feature_index': feature_idx,
                'feature_name': f'feature_{feature_idx}',
                'channel_index': channel_idx,
                'channel_name': channel_names[channel_idx],
                'band_index': band_idx,
                'band_name': band_name,
                'feature_type': 'relative_band_power',
                'section': 'per_channel_per_band'
            })
            feature_idx += 1
    
    # Part 2: per_channel_across_bands features (band_power)
    # Order: channel 0; channel 1; ... channel 18
    for channel_idx in range(n_channels):
        feature_mapping.append({
            'feature_index': feature_idx,
            'feature_name': f'feature_{feature_idx}',
            'channel_index': channel_idx,
            'channel_name': channel_names[channel_idx],
            'band_index': None,
            'band_name': 'all_bands',
            'feature_type': 'band_power',
            'section': 'per_channel_across_bands'
        })
        feature_idx += 1
    
    return pd.DataFrame(feature_mapping), channel_names, bands

def map_interesting_features(interesting_df, feature_mapping_df):
    """Map interesting features to their channel×band combinations."""
    merged = interesting_df.merge(
        feature_mapping_df,
        left_on='feature',
        right_on='feature_name',
        how='left'
    )
    return merged

def main():
    """Main function to create and save feature mapping."""
    print("="*60)
    print("🗺️  Feature Mapping: Index → Channel×Band")
    print("="*60)
    
    # Get real channel names from actual processing (same as test script)
    print("\n🔍 Getting real channel names from actual EEG processing...")
    real_channel_names = get_real_channel_names_from_processing()
    
    # Create mapping with real channel names
    feature_mapping_df, channel_names, bands = create_feature_mapping(channel_names=real_channel_names)
    
    print(f"\n📊 Mapping Summary:")
    print(f"   Total features: {len(feature_mapping_df)}")
    print(f"   Channels: {len(channel_names)}")
    print(f"   Bands: {len(bands)}")
    print(f"   Channel names: {', '.join(channel_names[:5])}... ({len(channel_names)} total)")
    print(f"   Band names: {', '.join(bands)}")
    
    # Load interesting features
    output_dir = Path(__file__).parent
    interesting_df = pd.read_csv(output_dir / 'interesting_features.csv')
    
    # Map interesting features
    mapped_features = map_interesting_features(interesting_df, feature_mapping_df)
    
    # Save mapping
    feature_mapping_df.to_csv(output_dir / 'feature_mapping.csv', index=False)
    print(f"\n💾 Saved feature_mapping.csv")
    
    # Save mapped interesting features
    mapped_features.to_csv(output_dir / 'interesting_features_mapped.csv', index=False)
    print(f"💾 Saved interesting_features_mapped.csv")
    
    # Print top 10 mapped features
    print(f"\n🔝 Top 10 Biomarkers with Channel×Band Mapping:")
    print("="*80)
    top_10 = mapped_features.head(10)
    for idx, row in top_10.iterrows():
        if row['feature_type'] == 'relative_band_power':
            print(f"   {row['feature_name']:12} | {row['channel_name']:6} × {row['band_name']:6} | "
                  f"Cohen's d={row['cohens_d']:.3f} | Rel diff={row['rel_diff_pct']:.1f}%")
        else:
            print(f"   {row['feature_name']:12} | {row['channel_name']:6} × {row['band_name']:10} | "
                  f"Cohen's d={row['cohens_d']:.3f} | Rel diff={row['rel_diff_pct']:.1f}%")
    
    # Summary by band
    print(f"\n📈 Top Biomarkers by Band (relative_band_power only):")
    print("="*80)
    rbp_features = mapped_features[mapped_features['feature_type'] == 'relative_band_power']
    for band in bands:
        band_features = rbp_features[rbp_features['band_name'] == band].head(3)
        if len(band_features) > 0:
            print(f"\n   {band} Band:")
            for idx, row in band_features.iterrows():
                print(f"      {row['channel_name']:6} | d={row['cohens_d']:.3f} | "
                      f"Alz={row['group1_mean']:.4f} vs Cntrl={row['group2_mean']:.4f}")
    
    # Summary by channel
    print(f"\n📈 Top Biomarkers by Channel (relative_band_power only):")
    print("="*80)
    for channel in channel_names[:10]:  # Top 10 channels
        channel_features = rbp_features[rbp_features['channel_name'] == channel].head(1)
        if len(channel_features) > 0:
            best = channel_features.iloc[0]
            print(f"   {channel:6} | Best: {best['band_name']:6} | d={best['cohens_d']:.3f}")
    
    print("\n" + "="*60)
    print("✅ Feature mapping complete!")
    print("="*60)

if __name__ == '__main__':
    main()

