#!/usr/bin/env python3
"""Basic tutorial for exploring normalized FIF and BIDS EDF EEG files with MNE."""

from __future__ import annotations

from pathlib import Path
import json
import re

import mne


DATASET_ROOT = Path("/Volumes/CrucialX6/Home/bigData/4244171_normalized")
NORMALIZED_FILE = DATASET_ROOT / "healthy_controls" / "H_S01" / "EC_raw.fif"
BIDS_FILE = DATASET_ROOT / "BIDS" / "sub-001" / "eeg" / "sub-001_task-eyesclosed_eeg.edf"
BIDS_JSON = DATASET_ROOT / "BIDS" / "sub-001" / "eeg" / "sub-001_task-eyesclosed_eeg.json"


def load_raw(file_path: Path):
    suffix = file_path.suffix.lower()
    if suffix == ".fif":
        return mne.io.read_raw_fif(file_path, preload=False, verbose=False)
    if suffix == ".edf":
        return mne.io.read_raw_edf(file_path, preload=False, verbose=False)
    if suffix == ".set":
        return mne.io.read_raw_eeglab(file_path, preload=False, verbose=False)
    raise ValueError(f"Unsupported EEG file type: {file_path}")


def infer_task(file_path: Path) -> str:
    name = file_path.name.lower()
    if "eyesclosed" in name or name.startswith("ec_") or "_ec" in name:
        return "eyesclosed"
    if "eyesopen" in name or name.startswith("eo_") or "_eo" in name:
        return "eyesopen"
    return "unknown"


def infer_subject(file_path: Path) -> str:
    for part in file_path.parts:
        if part.startswith("sub-"):
            return part
        if re.match(r"^[HM]_[SM]\d+$", part):
            return part
    return file_path.parent.name


def print_summary(label: str, file_path: Path) -> None:
    raw = load_raw(file_path)
    print(f"\n=== {label} ===")
    print(f"path: {file_path}")
    print(f"subject: {infer_subject(file_path)}")
    print(f"task: {infer_task(file_path)}")
    print(f"loader: {type(raw).__name__}")
    print(f"sampling_frequency_hz: {raw.info['sfreq']}")
    print(f"channel_count: {raw.info['nchan']}")
    print(f"first_five_channels: {raw.info['ch_names'][:5]}")
    print(f"duration_seconds: {round(raw.times[-1], 3)}")
    print(f"annotation_count: {len(raw.annotations)}")
    data = raw.get_data(start=0, stop=min(5, raw.n_times))
    print(f"data_preview_shape: {data.shape}")
    print(f"first_channel_first_five_samples: {data[0].tolist()}")


def print_bids_json(json_path: Path) -> None:
    print("\n=== bids_json_sidecar ===")
    payload = json.loads(json_path.read_text())
    for key in [
        "TaskName",
        "SamplingFrequency",
        "PowerLineFrequency",
        "EEGReference",
        "RecordingDuration",
    ]:
        if key in payload:
            print(f"{key}: {payload[key]}")


def main() -> None:
    print("Basic EEG exploration tutorial")
    print(f"dataset_root: {DATASET_ROOT}")
    print_summary("normalized_source_file", NORMALIZED_FILE)
    print_summary("bids_export_file", BIDS_FILE)
    print_bids_json(BIDS_JSON)


if __name__ == "__main__":
    main()
