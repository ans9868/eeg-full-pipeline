# EEG Full Pipeline - Documentation

## 📋 Overview

This documentation provides comprehensive diagrams and architectural details for the EEG Full Pipeline project. The project is a sophisticated EEG data processing and machine learning pipeline designed for large-scale neuroscience studies.

## 🏗️ Architecture Diagrams

### 1. [Overall Architecture](overall_architecture.md)
- **System Overview**: High-level system architecture showing all components
- **Pipeline Flow**: End-to-end data processing workflow
- **Component Interaction**: Sequence diagram showing component interactions
- **Data Flow Architecture**: Detailed data flow between components

### 2. [PySpark Pipeline](pyspark_pipeline_diagram.md)
- **Data Processing Flow**: Detailed PySpark processing pipeline
- **Subject Processing Flow**: How individual subjects are processed
- **Feature Schema Architecture**: Data structure and schema design
- **Spark Configuration**: Performance and resource configuration
- **Data Processing Stages**: Sequence diagram of processing steps

### 3. [Ray Tuner](ray_tuner_diagram.md)
- **ML Training Flow**: Machine learning pipeline architecture
- **Hyperparameter Tuning Process**: Detailed tuning workflow
- **Distributed Training Architecture**: Multi-node training setup
- **Model Training Sequence**: Training process sequence diagram
- **Experiment Configuration**: ML experiment setup
- **Ray Tune Configuration**: Hyperparameter optimization settings

### 4. [Configuration System](configuration_system_diagram.md)
- **Configuration Flow**: How configuration system works
- **Interactive Configuration Process**: Step-by-step configuration
- **Configuration File Structure**: YAML structure breakdown
- **Configuration Validation Process**: Input validation workflow
- **Configuration File Naming Convention**: File naming standards
- **Configuration Reuse System**: Caching and reuse mechanisms

### 5. [Deployment Architecture](deployment_diagram.md)
- **Deployment Options Overview**: All deployment methods
- **Docker Deployment Architecture**: Local Docker setup
- **Singularity Deployment Architecture**: HPC deployment
- **SLURM Job Scheduling**: Job scheduling workflow
- **Multi-node Deployment**: Cluster deployment
- **Container Build Process**: Image building process
- **Volume Mount Configuration**: Storage and mounting
- **Deployment Configuration**: Resource allocation

## 🎯 Key Features

### Data Processing
- **Scalable PySpark Processing**: Handles large EEG datasets
- **Feature Extraction**: Extracts power, frequency, and amplitude features
- **Multi-electrode Support**: Processes 6 electrodes (Fp1, Fp2, F3, F4, C3, C4)
- **Frequency Band Analysis**: Delta, Theta, Alpha, Beta bands
- **Epoch-based Processing**: 5 epochs per subject with 72 features each

### Machine Learning
- **Distributed Training**: Ray-based distributed ML training
- **Hyperparameter Tuning**: Automated hyperparameter optimization
- **Multiple Model Types**: Random Forest, SVM, Neural Networks, etc.
- **Data Leakage Prevention**: Proper train/test splitting
- **Performance Metrics**: Accuracy, Precision, Recall, F1-Score, AUC-ROC

### Deployment
- **Multi-platform Support**: Docker, Singularity, HPC
- **Container Orchestration**: Docker Compose, SLURM
- **Resource Management**: CPU, Memory, Storage allocation
- **Scalability**: Single-node to multi-node cluster support

### Configuration
- **Interactive Setup**: User-friendly configuration wizard
- **Validation System**: Comprehensive input validation
- **Caching System**: Hash-based result caching
- **Version Control**: Configuration file versioning

## 📊 Current Status

### ✅ Completed
- **PySpark Pipeline**: Successfully processes EEG data
- **Feature Extraction**: 250+ parquet files generated
- **Configuration System**: Interactive setup working
- **Containerization**: Docker and Singularity support
- **Data Processing**: 4 subjects processed (2 Alzheimer's, 2 controls)

### 🔄 In Progress
- **Ray Tuner**: ML training component ready but not executed
- **Model Training**: Hyperparameter tuning setup complete
- **Performance Optimization**: Ongoing optimization efforts

### 📈 Results Achieved
- **Processing Success**: Successfully processed ds004504 dataset
- **Feature Generation**: 72 features per epoch across 6 electrodes
- **Data Integrity**: Hash-based caching and validation working
- **Scalability**: PySpark distributed processing operational

## 🚀 Usage

### Quick Start
1. **Configure**: Run `config-maker.py` to create configuration
2. **Process**: Execute PySpark pipeline for feature extraction
3. **Train**: Run Ray Tuner for machine learning
4. **Deploy**: Choose deployment method (Docker/Singularity/HPC)

### Configuration
```bash
# Interactive configuration
python config-maker.py

# This creates: config_<project>_<date>_<time>.yaml
```

### Processing
```bash
# Run PySpark pipeline
python start-pipelines.py --config config_<project>_<date>_<time>.yaml

# This generates processed features in Parquet format
```

### Machine Learning
```bash
# Run Ray Tuner (when implemented)
python eeg-ray-tuner/start-pipeline.py --config config_<project>_<date>_<time>.yaml

# This will train models and optimize hyperparameters
```

## 📁 Project Structure

```
eeg-full-pipeline/
├── docs/                          # Documentation and diagrams
│   ├── overall_architecture.md    # System overview
│   ├── pyspark_pipeline_diagram.md # Data processing details
│   ├── ray_tuner_diagram.md      # ML training details
│   ├── configuration_system_diagram.md # Config system
│   └── deployment_diagram.md     # Deployment options
├── config/                        # Configuration files
├── data/                          # Processed results
├── eeg-pyspark-pipeline/         # Data processing module
├── eeg-ray-tuner/                # ML training module
├── logs/                          # Execution logs
└── config-maker.py               # Interactive configuration
```

## 🔧 Technical Stack

### Data Processing
- **PySpark**: Distributed data processing
- **Parquet**: Efficient data storage format
- **EEGLAB**: EEG data format support (.set files)

### Machine Learning
- **Ray**: Distributed ML framework
- **Ray Tune**: Hyperparameter optimization
- **Scikit-learn**: Traditional ML algorithms
- **PyTorch/TensorFlow**: Deep learning support

### Deployment
- **Docker**: Containerization
- **Singularity**: HPC containerization
- **SLURM**: Job scheduling
- **Docker Compose**: Multi-container orchestration

### Configuration
- **YAML**: Configuration format
- **Questionary**: Interactive CLI
- **PyYAML**: YAML processing

## 📈 Performance Metrics

### Data Processing
- **Subjects Processed**: 4 (2 Alzheimer's, 2 controls)
- **Features Generated**: 72 per epoch
- **Electrodes**: 6 (Fp1, Fp2, F3, F4, C3, C4)
- **Frequency Bands**: 4 (Delta, Theta, Alpha, Beta)
- **Output Files**: 250+ Parquet partition files

### Resource Usage
- **Spark Configuration**: 4 cores, 6GB memory
- **Processing Time**: Optimized for large datasets
- **Storage**: Efficient Parquet compression
- **Scalability**: Linear scaling with cluster size

## 🎯 Use Cases

### Research Applications
- **Alzheimer's Disease Classification**: Current implementation
- **EEG Biomarker Discovery**: Feature-based analysis
- **Clinical Trial Analysis**: Large-scale data processing
- **Neuroscience Research**: Scalable EEG analysis

### Production Deployment
- **HPC Clusters**: Research institution deployment
- **Cloud Computing**: AWS, Azure, GCP support
- **Local Development**: Docker-based development
- **Multi-site Studies**: Distributed data processing

## 🔮 Future Enhancements

### Planned Features
- **Real-time Processing**: Stream processing capabilities
- **Advanced ML Models**: Deep learning integration
- **Web Interface**: User-friendly web UI
- **API Integration**: RESTful API for external access
- **Advanced Analytics**: Statistical analysis tools

### Scalability Improvements
- **Multi-site Support**: Distributed data collection
- **Real-time Monitoring**: Live processing status
- **Advanced Caching**: Intelligent result caching
- **Auto-scaling**: Dynamic resource allocation

## 📞 Support

For questions, issues, or contributions:
- **Documentation**: Check the diagrams in this folder
- **Configuration**: Use `config-maker.py` for setup
- **Deployment**: Follow deployment diagrams for your environment
- **Troubleshooting**: Check logs and validation reports

---

*This documentation provides comprehensive architectural diagrams and implementation details for the EEG Full Pipeline project. Each diagram is designed to be self-contained while showing the relationships between different components of the system.* 