"""
Pytest configuration and fixtures for EEG Full Pipeline integration tests.
"""

import pytest
import tempfile
import shutil
import subprocess
import time
from pathlib import Path
import yaml
import sys
import os
import mne
from mne.datasets import sample

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_handler import UnifiedConfigHandler


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent


@pytest.fixture(scope="session")
def mne_sample_data():
    """
    Load MNE sample dataset for testing.
    This fixture is session-scoped to avoid reloading data for each test.
    """
    # Download sample data if not already present
    data_path = sample.data_path()
    
    # Load the sample raw data
    raw_fname = data_path / 'MEG' / 'sample' / 'sample_audvis_raw.fif'
    raw = mne.io.read_raw_fif(raw_fname, preload=True)
    
    # Create epochs for testing
    events = mne.find_events(raw, stim_channel='STI 014')
    event_id = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3, 'visual/right': 4}
    tmin, tmax = -0.2, 0.5
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, preload=True)
    
    return {
        'raw': raw,
        'epochs': epochs,
        'events': events,
        'data_path': data_path
    }


@pytest.fixture(scope="session")
def pyspark_pipeline_dir(project_root):
    """Get the PySpark pipeline directory."""
    return project_root / "eeg-pyspark-pipeline"


@pytest.fixture(scope="session")
def ray_tuner_dir(project_root):
    """Get the Ray tuner directory."""
    return project_root / "eeg-ray-tuner"


@pytest.fixture(scope="session")
def config_dir(project_root):
    """Get the config directory."""
    return project_root / "config"


@pytest.fixture
def temp_config_file(project_root):
    """Create a temporary config file for testing using actual test data files."""
    test_config = {
        'project': {
            'name': 'test_integration',
            'experiment_type': 'ML (Classification)',
            'deployment_method': 'Docker'
        },
        'data_input': {
            'groups': {
                'control': [
                    str(project_root / 'tests' / 'test_data' / 'sub-001_task-eyesclosed_eeg.set'),
                    str(project_root / 'tests' / 'test_data' / 'sub-002_task-eyesclosed_eeg.set')
                ],
                'patient': [
                    str(project_root / 'tests' / 'test_data' / 'sub-003_task-eyesclosed_eeg.set'),
                    str(project_root / 'tests' / 'test_data' / 'sub-004_task-eyesclosed_eeg.set')
                ]
            },
            'reuse_processed_subjects': 'Yes'
        },
        'preprocessing': {
            'window_size': 6.0,
            'sliding_window': 0.0,
            'normalize_psd': 'Yes',
            'reject_by_annotation': 'Yes'
        },
        'feature_extraction': {
            'method': 'welch',
            'output_format': 'ml',
            'features': {
                'per_channel_across_bands': ['band_power'],
                'per_channel_per_band': ['band_power']
            }
        },
        'feature_transformation': {
            'transformations': ['MinMax scaler'],
            'synthetic': 'None',
            'minmax_range': [-1.0, 1.0]
        },
        'ray': {
            'models': ['KNN'],
            'metric': 'accuracy'
        },
        'pyspark': {
            'master': 'local[2]',
            'driver_memory': '2g',
            'executor_memory': '2g',
            'executor_cores': 2,
            'shuffle_partitions': 200
        }
    }
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(test_config, f)
        temp_config_path = f.name
    
    try:
        yield temp_config_path
    finally:
        # Clean up temporary file
        os.unlink(temp_config_path)


@pytest.fixture
def sample_config_handler(temp_config_file):
    """Create a sample UnifiedConfigHandler for testing."""
    return UnifiedConfigHandler(temp_config_file)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def pyspark_container():
    """Build and return PySpark test container."""
    container_name = "eeg-pyspark-test"
    
    # Build the container
    build_cmd = [
        "docker", "build", 
        "-t", container_name,
        str(Path(__file__).parent / "eeg-pyspark-pipeline")
    ]
    
    print(f"Building PySpark container: {' '.join(build_cmd)}")
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        pytest.skip(f"Failed to build PySpark container: {result.stderr}")
    
    yield container_name
    
    # Cleanup
    subprocess.run(["docker", "rmi", container_name], capture_output=True)


@pytest.fixture(scope="session")
def ray_container():
    """Build and return Ray test container."""
    container_name = "eeg-ray-test"
    
    # Build the container
    build_cmd = [
        "docker", "build", 
        "-t", container_name,
        str(Path(__file__).parent / "eeg-ray-tuner")
    ]
    
    print(f"Building Ray container: {' '.join(build_cmd)}")
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        pytest.skip(f"Failed to build Ray container: {result.stderr}")
    
    yield container_name
    
    # Cleanup
    subprocess.run(["docker", "rmi", container_name], capture_output=True)


@pytest.fixture
def run_pyspark_container(pyspark_container):
    """Run a command in the PySpark container."""
    def _run_command(command, timeout=300):
        """Run a command in the PySpark container."""
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path(__file__).parent}:/workspace",
            "-w", "/workspace",
            pyspark_container,
            "bash", "-c", command
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result
    
    return _run_command


@pytest.fixture
def run_ray_container(ray_container):
    """Run a command in the Ray container."""
    def _run_command(command, timeout=300):
        """Run a command in the Ray container."""
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{Path(__file__).parent}:/workspace",
            "-w", "/workspace",
            ray_container,
            "bash", "-c", command
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result
    
    return _run_command


@pytest.fixture
def wait_for_container_ready():
    """Wait for container to be ready."""
    def _wait(container_name, max_wait=60):
        """Wait for container to be ready."""
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                result = subprocess.run(
                    ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Status}}"],
                    capture_output=True, text=True, timeout=10
                )
                if "Up" in result.stdout:
                    return True
            except subprocess.TimeoutExpired:
                pass
            time.sleep(2)
        return False
    
    return _wait


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "config: mark test as configuration related"
    )
    config.addinivalue_line(
        "markers", "container: mark test as requiring containers"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add container marker to tests that use container fixtures
        if any(fixture in item.fixturenames for fixture in ['pyspark_container', 'ray_container', 'run_pyspark_container', 'run_ray_container']):
            item.add_marker(pytest.mark.container)
        
        # Add slow marker to tests that might be slow
        if any(keyword in item.name.lower() for keyword in ['slow', 'integration', 'e2e', 'container']):
            item.add_marker(pytest.mark.slow)
        
        # Add config marker to config-related tests
        if any(keyword in item.name.lower() for keyword in ['config', 'handler']):
            item.add_marker(pytest.mark.config)
        
        # Add unit marker to tests that don't require external dependencies
        if not any(fixture in item.fixturenames for fixture in ['pyspark_container', 'ray_container', 'run_pyspark_container', 'run_ray_container']):
            if 'integration' not in item.name.lower() and 'e2e' not in item.name.lower():
                item.add_marker(pytest.mark.unit)
