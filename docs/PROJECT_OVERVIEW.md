# EEG Full Pipeline - Project Overview

## 🎯 Project Purpose

The **EEG Full Pipeline** is a comprehensive, production-ready system for processing electroencephalography (EEG) data and running machine learning experiments. It's designed for researchers studying brain activity, particularly for tasks like:

- **Alzheimer's Disease Classification**: Distinguishing between patients and healthy controls
- **EEG Fingerprinting**: Identifying individual subjects from EEG patterns
- **Clustering Analysis**: Finding patterns and groups in EEG data
- **General Analysis**: Processing EEG data for manual analysis

## 🏗️ System Architecture Overview

```mermaid
graph TB
    %% User Layer
    subgraph "User Interface"
        A[config-maker.py<br/>Interactive Configuration]
        B[Configuration YAML Files]
    end
    
    %% Core Components
    subgraph "Core Pipeline Components"
        C[eeg-pyspark-pipeline<br/>Data Processing]
        D[eeg-ray-tuner<br/>ML Training & Tuning]
    end
    
    %% Data Flow
    subgraph "Data Flow"
        E[Raw EEG .set Files]
        F[Processed Features<br/>Parquet Format]
        G[Transformed Features]
        H[ML Models & Results]
    end
    
    %% Deployment
    subgraph "Deployment Options"
        I[Docker<br/>Local Development]
        J[Singularity<br/>HPC Systems]
        K[SLURM<br/>Job Scheduling]
    end
    
    %% Storage
    subgraph "Storage & Output"
        L[Processed Data<br/>Parquet Files]
        M[Model Artifacts]
        N[Configuration Backups]
        O[Logs & Metrics]
    end
    
    A --> B
    B --> C
    B --> D
    E --> C
    C --> F
    F --> G
    G --> D
    D --> H
    
    C --> I
    C --> J
    D --> I
    D --> J
    J --> K
    
    F --> L
    H --> M
    B --> N
    C --> O
    D --> O
    
    %% Styling
    classDef user fill:#e3f2fd
    classDef core fill:#e8f5e9
    classDef data fill:#fff3e0
    classDef deploy fill:#f3e5f5
    classDef storage fill:#fce4ec
    
    class A,B user
    class C,D core
    class E,F,G,H data
    class I,J,K deploy
    class L,M,N,O storage
```

## 📊 Complete Pipeline Flow

```mermaid
flowchart TD
    Start([Start: User Runs Pipeline]) --> Config[Create Configuration<br/>via config-maker.py]
    Config --> Deploy{Deployment Method}
    
    Deploy -->|Docker| Docker[Run Docker Containers]
    Deploy -->|Singularity| Singularity[Run Singularity Containers]
    Deploy -->|SLURM| SLURM[Submit SLURM Jobs]
    
    Docker --> SparkInit[Initialize PySpark Session]
    Singularity --> SparkInit
    SLURM --> SparkInit
    
    SparkInit --> LoadData[Load Raw EEG Data<br/>.set or .fif files]
    LoadData --> Preprocess[Preprocess Data<br/>- Filtering<br/>- Artifact Removal<br/>- Epoching]
    
    Preprocess --> ExtractFeatures[Extract Features<br/>- Band Power<br/>- Frequency Analysis<br/>- Statistical Features]
    
    ExtractFeatures --> CheckReuse{Reuse<br/>Transformed?}
    CheckReuse -->|Yes| LoadTransformed[Load Existing<br/>Transformed Data]
    CheckReuse -->|No| Transform[Apply Transformations<br/>- StandardScaler<br/>- PCA<br/>- SVD<br/>- etc.]
    
    LoadTransformed --> SaveFeatures[Save Processed Features<br/>Parquet Format]
    Transform --> SaveFeatures
    
    SaveFeatures --> MLCheck{ML Experiment?}
    MLCheck -->|No| Analysis[Analysis Output]
    MLCheck -->|Yes| RayInit[Initialize Ray Cluster]
    
    RayInit --> LoadML[Load Transformed Features]
    LoadML --> SplitData[Data Split<br/>LPSO or Train/Test]
    
    SplitData --> Tune{Search Strategy}
    Tune -->|Grid Search| GridSearch[Grid Search<br/>Hyperparameter Tuning]
    Tune -->|Ax Search| AxSearch[Bayesian Optimization<br/>Ax Framework]
    
    GridSearch --> TrainModels[Train ML Models<br/>- Random Forest<br/>- SVM<br/>- Neural Networks]
    AxSearch --> TrainModels
    
    TrainModels --> Evaluate[Evaluate Models<br/>- Accuracy<br/>- Precision/Recall<br/>- F1-Score]
    
    Evaluate --> SelectBest[Select Best Model]
    SelectBest --> SaveResults[Save Results<br/>- Models<br/>- Metrics<br/>- Configurations]
    
    SaveResults --> End([End: Results Available])
    Analysis --> End
    
    %% Styling
    classDef startEnd fill:#4caf50,color:#fff
    classDef process fill:#2196f3,color:#fff
    classDef decision fill:#ff9800,color:#fff
    classDef ml fill:#9c27b0,color:#fff
    classDef storage fill:#f44336,color:#fff
    
    class Start,End startEnd
    class Config,SparkInit,LoadData,Preprocess,ExtractFeatures,Transform,SaveFeatures process
    class Deploy,CheckReuse,MLCheck,Tune decision
    class RayInit,LoadML,SplitData,GridSearch,AxSearch,TrainModels,Evaluate,SelectBest ml
    class LoadTransformed,SaveResults,Analysis storage
```

## 🔄 Component Interaction Sequence

```mermaid
sequenceDiagram
    participant User
    participant ConfigMaker
    participant StartScript
    participant PySpark
    participant RayTuner
    participant Storage
    participant HPC
    
    User->>ConfigMaker: Run config-maker.py
    ConfigMaker->>User: Interactive Q&A
    User->>ConfigMaker: Provide configuration
    ConfigMaker->>Storage: Save config.yaml
    
    User->>StartScript: Run start-pipelines.py
    StartScript->>StartScript: Determine deployment method
    StartScript->>Storage: Load config.yaml
    
    alt Docker Deployment
        StartScript->>PySpark: Start Docker container
        PySpark->>Storage: Load EEG data
        PySpark->>PySpark: Process subjects
        PySpark->>PySpark: Extract features
        PySpark->>Storage: Save processed features
        PySpark->>StartScript: Complete
        
        StartScript->>RayTuner: Start Docker container
        RayTuner->>Storage: Load processed features
        RayTuner->>RayTuner: Train models
        RayTuner->>RayTuner: Tune hyperparameters
        RayTuner->>Storage: Save models & results
        RayTuner->>StartScript: Complete
    else Singularity + SLURM
        StartScript->>HPC: Submit PySpark SLURM job
        HPC->>PySpark: Run Singularity container
        PySpark->>Storage: Process & save data
        PySpark->>HPC: Job complete
        
        StartScript->>HPC: Submit Ray SLURM job (depends on PySpark)
        HPC->>RayTuner: Run Singularity container
        RayTuner->>Storage: Train & save models
        RayTuner->>HPC: Job complete
    end
    
    StartScript->>User: Pipeline complete
```

## 🧩 Component Architecture Details

### 1. PySpark Pipeline Component

```mermaid
graph TB
    subgraph "PySpark Pipeline Architecture"
        A[Main Entry Point<br/>main.py] --> B[UnifiedConfigHandler<br/>Configuration Validation]
        B --> C[Session Builder<br/>Spark Session Creation]
        C --> D[Process Subjects<br/>Subject-Level Processing]
        
        D --> E[Process Subject UDTF<br/>User-Defined Table Function]
        E --> F[Process Epoch<br/>Epoch-Level Processing]
        
        F --> G[Feature Extraction<br/>- Band Power<br/>- Frequency Analysis<br/>- Statistical Features]
        
        G --> H[Feature Transformations<br/>Transformer Pipeline]
        H --> I[StandardScaler]
        H --> J[PCA]
        H --> K[SVD]
        H --> L[Other Transformers]
        
        I --> M[Data I/O<br/>Parquet Read/Write]
        J --> M
        K --> M
        L --> M
        
        M --> N[Hash Validation<br/>Data Reuse Checking]
        N --> O[Output Storage<br/>Parquet Files]
    end
    
    %% Styling
    classDef entry fill:#e3f2fd
    classDef core fill:#e8f5e9
    classDef process fill:#fff3e0
    classDef transform fill:#f3e5f5
    classDef storage fill:#fce4ec
    
    class A entry
    class B,C core
    class D,E,F,G process
    class H,I,J,K,L transform
    class M,N,O storage
```

### 2. Ray Tuner Component

```mermaid
graph TB
    subgraph "Ray Tuner Architecture"
        A[Main Entry Point<br/>main.py] --> B[Config Handler<br/>Load Configuration]
        B --> C[Ray Cluster Init<br/>Initialize Ray]
        C --> D[Data Loader<br/>Load Processed Features]
        
        D --> E[Data Split<br/>LPSO or Train/Test]
        E --> F[Search Strategy Selection]
        
        F --> G[Grid Search<br/>Exhaustive Search]
        F --> H[Ax Search<br/>Bayesian Optimization]
        
        G --> I[Ray Tune<br/>Hyperparameter Tuning]
        H --> I
        
        I --> J[Model Training<br/>Parallel Trials]
        J --> K[Random Forest]
        J --> L[SVM]
        J --> M[Neural Network]
        J --> N[Other Models]
        
        K --> O[Model Evaluation<br/>Metrics Calculation]
        L --> O
        M --> O
        N --> O
        
        O --> P[Best Model Selection]
        P --> Q[Model Artifacts<br/>Save Results]
    end
    
    %% Styling
    classDef entry fill:#e3f2fd
    classDef core fill:#e8f5e9
    classDef strategy fill:#fff3e0
    classDef model fill:#f3e5f5
    classDef output fill:#fce4ec
    
    class A entry
    class B,C,D core
    class E,F,G,H strategy
    class I,J,K,L,M,N model
    class O,P,Q output
```

## 🔐 Data Leakage Prevention

```mermaid
graph LR
    subgraph "Data Leakage Prevention Strategies"
        A[LPSO Strategy<br/>Leave-P-Subjects-Out]
        B[Train/Test Split<br/>Single Split Method]
    end
    
    subgraph "LPSO Process"
        C[Fold 1: Subjects 1-10 Test<br/>Subjects 11-40 Train]
        D[Fold 2: Subjects 11-20 Test<br/>Subjects 1-10, 21-40 Train]
        E[Fold N: ...]
    end
    
    subgraph "Train/Test Split Process"
        F[Test Subjects: 1-2]
        G[Train Subjects: 3-40]
    end
    
    subgraph "Transformation Safety"
        H[Fit on Training Set Only]
        I[Transform Both Sets]
        J[No Information Leakage]
    end
    
    A --> C
    A --> D
    A --> E
    
    B --> F
    B --> G
    
    C --> H
    D --> H
    E --> H
    F --> H
    G --> H
    
    H --> I
    I --> J
    
    %% Styling
    classDef strategy fill:#e3f2fd
    classDef lpso fill:#e8f5e9
    classDef split fill:#fff3e0
    classDef safety fill:#f3e5f5
    
    class A,B strategy
    class C,D,E lpso
    class F,G split
    class H,I,J safety
```

## 📦 Data Formats & Schemas

```mermaid
graph TB
    subgraph "Input Data Format"
        A[EEG .set Files<br/>EEGLAB Format]
        B[EEG .fif Files<br/>MNE Format]
        C[Subject Metadata]
    end
    
    subgraph "Processing Formats"
        D[Raw EEG Data<br/>Multi-channel Time Series]
        E[Epochs<br/>Time-windowed Segments]
        F[Feature Vectors<br/>Per Epoch Features]
    end
    
    subgraph "Output Formats"
        G[Analysis Format<br/>Long-form DataFrame]
        H[ML Format<br/>Wide-form with DenseVectors]
    end
    
    subgraph "Analysis Format Schema"
        I[SubjectID: String]
        J[EpochID: String]
        K[Electrode: String]
        L[WaveBand: String]
        M[FeatureName: String]
        N[FeatureValue: Float]
        O[table_type: String]
    end
    
    subgraph "ML Format Schema"
        P[SubjectID: String]
        Q[features: DenseVector]
        R[table_type: String]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    F --> H
    
    G --> I
    G --> J
    G --> K
    G --> L
    G --> M
    G --> N
    G --> O
    
    H --> P
    H --> Q
    H --> R
    
    %% Styling
    classDef input fill:#e3f2fd
    classDef process fill:#e8f5e9
    classDef output fill:#fff3e0
    classDef analysis fill:#f3e5f5
    classDef ml fill:#fce4ec
    
    class A,B,C input
    class D,E,F process
    class G,H output
    class I,J,K,L,M,N,O analysis
    class P,Q,R ml
```

## 🚀 Deployment Architecture

```mermaid
graph TB
    subgraph "Deployment Methods"
        A[Docker<br/>Local Development]
        B[Singularity<br/>Local Execution]
        C[Singularity + SLURM<br/>HPC Systems]
    end
    
    subgraph "Container Images"
        D[eeg-pyspark-pipeline<br/>Docker Image]
        E[eeg-ray-tuner<br/>Docker Image]
        F[eeg-pyspark-pipeline.sif<br/>Singularity Image]
        G[eeg-ray-tuner.sif<br/>Singularity Image]
    end
    
    subgraph "Volume Mounts"
        H[Config Files<br/>YAML Configuration]
        I[Data Directory<br/>EEG Files & Results]
        J[Logs Directory<br/>Processing Logs]
        K[Spark Config<br/>Spark-specific Settings]
    end
    
    subgraph "Network & Ports"
        L[Spark UI<br/>Port 4040]
        M[Ray Dashboard<br/>Port 8265]
    end
    
    A --> D
    A --> E
    B --> F
    B --> G
    C --> F
    C --> G
    
    D --> H
    D --> I
    D --> J
    D --> K
    E --> H
    E --> I
    E --> J
    
    F --> H
    F --> I
    F --> J
    F --> K
    G --> H
    G --> I
    G --> J
    
    D --> L
    E --> M
    
    %% Styling
    classDef deploy fill:#e3f2fd
    classDef container fill:#e8f5e9
    classDef mount fill:#fff3e0
    classDef network fill:#f3e5f5
    
    class A,B,C deploy
    class D,E,F,G container
    class H,I,J,K mount
    class L,M network
```

## 🔧 Configuration System

```mermaid
graph TB
    subgraph "Configuration Creation"
        A[config-maker.py<br/>Interactive CLI]
        B[Question-Based Setup]
        C[Configuration Sections]
    end
    
    subgraph "Configuration Sections"
        D[Project Metadata<br/>Name, Type, Output]
        E[Data Input<br/>EEG Files, Groups]
        F[Preprocessing<br/>Filtering, Epoching]
        G[Feature Extraction<br/>Bands, Features]
        H[Transformations<br/>Scalers, PCA, SVD]
        I[Data Leakage Prevention<br/>LPSO, Train/Test]
        J[Deployment Method<br/>Docker, Singularity]
        K[Ray Configuration<br/>ML Models, Tuning]
        L[SLURM Options<br/>Resources, Time]
    end
    
    subgraph "Configuration Validation"
        M[UnifiedConfigHandler<br/>Validation Engine]
        N[Type Checking]
        O[Path Validation]
        P[Value Range Checks]
        Q[Cross-Section Validation]
    end
    
    subgraph "Configuration Usage"
        R[PySpark Pipeline<br/>Reads Config]
        S[Ray Tuner<br/>Reads Config]
        T[Hash Generation<br/>Reproducibility]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    C --> G
    C --> H
    C --> I
    C --> J
    C --> K
    C --> L
    
    D --> M
    E --> M
    F --> M
    G --> M
    H --> M
    I --> M
    J --> M
    K --> M
    L --> M
    
    M --> N
    M --> O
    M --> P
    M --> Q
    
    N --> R
    O --> R
    P --> S
    Q --> S
    
    R --> T
    S --> T
    
    %% Styling
    classDef create fill:#e3f2fd
    classDef sections fill:#e8f5e9
    classDef validate fill:#fff3e0
    classDef usage fill:#f3e5f5
    
    class A,B,C create
    class D,E,F,G,H,I,J,K,L sections
    class M,N,O,P,Q validate
    class R,S,T usage
```

## 📈 Processing Pipeline Detail

```mermaid
flowchart TD
    A[Load EEG File] --> B[Apply Preprocessing]
    B --> C[Filter Noise]
    C --> D[Remove Artifacts<br/>ICA/Annotations]
    D --> E[Create Epochs<br/>Time Windows]
    
    E --> F[For Each Epoch]
    F --> G[Extract Frequency Bands<br/>Delta, Theta, Alpha, Beta, Gamma]
    G --> H[Compute Features<br/>Power, Mean, Std, Variance, RMS]
    H --> I[Extract PSD<br/>Welch or Multitaper]
    I --> J[Calculate Hjorth Parameters]
    
    J --> K{More Epochs?}
    K -->|Yes| F
    K -->|No| L[Union All Epochs]
    
    L --> M[For Each Subject]
    M --> N{More Subjects?}
    N -->|Yes| M
    N -->|No| O[Union All Subjects]
    
    O --> P[Apply Data Leakage Prevention]
    P --> Q[Split Train/Test]
    Q --> R[Fit Transformers on Train]
    R --> S[Transform Both Sets]
    S --> T[Save Processed Data]
    
    %% Styling
    classDef load fill:#e3f2fd
    classDef preprocess fill:#e8f5e9
    classDef feature fill:#fff3e0
    classDef process fill:#f3e5f5
    classDef output fill:#fce4ec
    
    class A load
    class B,C,D,E preprocess
    class F,G,H,I,J feature
    class K,L,M,N,O,P,Q,R,S process
    class T output
```

## 🎓 Key Features

### Data Processing Features
- ✅ Multi-format EEG support (.set, .fif)
- ✅ Distributed processing with PySpark
- ✅ Flexible epoching and windowing
- ✅ Multiple feature extraction methods
- ✅ Comprehensive artifact removal
- ✅ Frequency band analysis

### Machine Learning Features
- ✅ Multiple ML models (RF, SVM, NN, etc.)
- ✅ Hyperparameter tuning (Grid Search, Ax)
- ✅ Data leakage prevention (LPSO, Train/Test)
- ✅ Distributed training with Ray
- ✅ Comprehensive evaluation metrics
- ✅ Model persistence and versioning

### Production Features
- ✅ Container-based deployment
- ✅ HPC integration (Singularity, SLURM)
- ✅ Configuration management
- ✅ Data reuse and caching
- ✅ Comprehensive logging
- ✅ Error handling and validation

## 📚 Additional Documentation

For more detailed information, see:
- [Overall Architecture](./overall_architecture.md)
- [PySpark Pipeline Details](./pyspark_pipeline_diagram.md)
- [Ray Tuner Details](./ray_tuner_diagram.md)
- [Deployment Architecture](./deployment_diagram.md)
- [Configuration System](./configuration_system_diagram.md)


