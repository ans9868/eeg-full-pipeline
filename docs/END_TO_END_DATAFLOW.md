# End-to-End Data Flow Diagram

## Complete Data Journey Through the Pipeline

```mermaid
graph TB
    %% Input Layer
    subgraph "1. Input Data Sources"
        A1[EEG .set Files<br/>Patient Group]
        A2[EEG .set Files<br/>Control Group]
        A3[Subject Metadata]
        A4[Event Annotations]
    end
    
    %% Configuration Layer
    subgraph "2. Configuration"
        B1[config-maker.py<br/>Interactive Setup]
        B2[config.yaml<br/>Complete Configuration]
        B3[UnifiedConfigHandler<br/>Validation & Parsing]
    end
    
    %% PySpark Processing Layer
    subgraph "3. PySpark Processing Pipeline"
        C1[Load Raw EEG Files<br/>MNE/EEGLAB]
        C2[Preprocessing<br/>Filter, Artifact Removal]
        C3[Epoching<br/>Time Windows]
        C4[Feature Extraction<br/>72 Features per Epoch]
        C5[Subject Aggregation<br/>Union All Subjects]
        C6[Data Leakage Prevention<br/>LPSO/Train-Test Split]
        C7[Feature Transformations<br/>Scalers, PCA, SVD]
        C8[Save Processed Data<br/>Parquet Format]
    end
    
    %% Intermediate Storage
    subgraph "4. Intermediate Storage"
        D1[processed_subjects/<br/>Parquet Files]
        D2[transformed/<br/>Parquet Files]
        D3[Hash Validation<br/>Data Reuse Checking]
    end
    
    %% Ray ML Layer
    subgraph "5. Ray ML Pipeline"
        E1[Load Transformed Features<br/>Parquet Files]
        E2[Data Split<br/>Train/Test or LPSO Folds]
        E3[Search Strategy<br/>Grid Search or Ax]
        E4[Hyperparameter Tuning<br/>Ray Tune]
        E5[Model Training<br/>Parallel Trials]
        E6[Model Evaluation<br/>Metrics Calculation]
        E7[Best Model Selection]
        E8[Save Model Artifacts]
    end
    
    %% Output Layer
    subgraph "6. Output & Results"
        F1[Trained Models<br/>Pickle Files]
        F2[Performance Metrics<br/>CSV/JSON]
        F3[Hyperparameter Results<br/>Ray Tune Results]
        F4[Configuration Backups<br/>Hash-based Storage]
        F5[Logs & Debug Info<br/>Spark & Ray Logs]
    end
    
    %% Data Flow Connections
    A1 --> C1
    A2 --> C1
    A3 --> C1
    A4 --> C1
    
    B1 --> B2
    B2 --> B3
    B3 --> C1
    
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> C5
    C5 --> C6
    C6 --> C7
    C7 --> C8
    
    C8 --> D1
    C7 --> D2
    D1 --> D3
    D2 --> D3
    
    D2 --> E1
    B3 --> E1
    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 --> E5
    E5 --> E6
    E6 --> E7
    E7 --> E8
    
    E8 --> F1
    E6 --> F2
    E4 --> F3
    B2 --> F4
    C8 --> F5
    E8 --> F5
    
    %% Styling
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef config fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef process fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef storage fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef ml fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef output fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class A1,A2,A3,A4 input
    class B1,B2,B3 config
    class C1,C2,C3,C4,C5,C6,C7,C8 process
    class D1,D2,D3 storage
    class E1,E2,E3,E4,E5,E6,E7,E8 ml
    class F1,F2,F3,F4,F5 output
```

## Detailed Processing Stages

### Stage 1: Data Loading & Preprocessing

```mermaid
flowchart LR
    A[EEG File<br/>sub-001_eeg.set] --> B[Load with MNE<br/>or EEGLAB]
    B --> C[Raw Data<br/>Multi-channel Time Series]
    C --> D[Apply Filters<br/>Bandpass, Notch]
    D --> E[Remove Artifacts<br/>ICA, Annotations]
    E --> F[Create Epochs<br/>1-2 second windows]
    F --> G[Epoch Data<br/>Ready for Features]
    
    %% Styling
    classDef file fill:#e3f2fd
    classDef raw fill:#e8f5e9
    classDef process fill:#fff3e0
    classDef output fill:#f3e5f5
    
    class A file
    class B,C raw
    class D,E,F process
    class G output
```

### Stage 2: Feature Extraction

```mermaid
flowchart TD
    A[Single Epoch<br/>Time Window] --> B[Extract Frequency Bands]
    B --> C[Delta: 1-4 Hz]
    B --> D[Theta: 4-8 Hz]
    B --> E[Alpha: 8-13 Hz]
    B --> F[Beta: 13-30 Hz]
    B --> G[Gamma: 30-100 Hz]
    
    C --> H[Compute Features]
    D --> H
    E --> H
    F --> H
    G --> H
    
    H --> I[Band Power]
    H --> J[Mean Amplitude]
    H --> K[Standard Deviation]
    H --> L[Variance]
    H --> M[RMS]
    H --> N[Hjorth Parameters]
    H --> O[PSD Features]
    
    I --> P[Feature Vector<br/>72 Features Total]
    J --> P
    K --> P
    L --> P
    M --> P
    N --> P
    O --> P
    
    P --> Q[6 Electrodes × 4 Bands × 3 Features<br/>= 72 Features per Epoch]
    
    %% Styling
    classDef epoch fill:#e3f2fd
    classDef band fill:#e8f5e9
    classDef feature fill:#fff3e0
    classDef vector fill:#f3e5f5
    
    class A epoch
    class B,C,D,E,F,G band
    class H,I,J,K,L,M,N,O feature
    class P,Q vector
```

### Stage 3: Data Transformation

```mermaid
flowchart TD
    A[All Subjects Features<br/>Analysis Format DataFrame] --> B[Data Leakage Prevention]
    
    B --> C{LPSO Strategy}
    B --> D{Train/Test Split}
    
    C --> E[Fold 1: Train on Subjects 11-40<br/>Test on Subjects 1-10]
    C --> F[Fold 2: Train on Subjects 1-10, 21-40<br/>Test on Subjects 11-20]
    C --> G[Fold N: ...]
    
    D --> H[Train: Subjects 3-40<br/>Test: Subjects 1-2]
    
    E --> I[Fit Transformers<br/>on Training Set Only]
    F --> I
    G --> I
    H --> I
    
    I --> J[StandardScaler<br/>Mean=0, Std=1]
    I --> K[PCA<br/>Dimensionality Reduction]
    I --> L[SVD<br/>Singular Value Decomposition]
    I --> M[Other Transformers]
    
    J --> N[Transform Both<br/>Train & Test Sets]
    K --> N
    L --> N
    M --> N
    
    N --> O[ML Format<br/>DenseVector Features]
    
    %% Styling
    classDef input fill:#e3f2fd
    classDef strategy fill:#e8f5e9
    classDef split fill:#fff3e0
    classDef transform fill:#f3e5f5
    classDef output fill:#fce4ec
    
    class A input
    class B,C,D strategy
    class E,F,G,H split
    class I,J,K,L,M transform
    class N,O output
```

### Stage 4: Machine Learning Training

```mermaid
flowchart TD
    A[Transformed Features<br/>Parquet Files] --> B[Load into Ray]
    B --> C[Split Data<br/>Train/Test]
    
    C --> D[Select Search Strategy]
    D --> E[Grid Search<br/>Exhaustive]
    D --> F[Ax Search<br/>Bayesian]
    
    E --> G[Define Hyperparameter Grid]
    F --> H[Define Search Space]
    
    G --> I[Ray Tune<br/>Launch Trials]
    H --> I
    
    I --> J[Trial 1<br/>Random Forest]
    I --> K[Trial 2<br/>SVM]
    I --> L[Trial 3<br/>Neural Network]
    I --> M[Trial N<br/>...]
    
    J --> N[Train Model]
    K --> N
    L --> N
    M --> N
    
    N --> O[Evaluate on Test Set]
    O --> P[Calculate Metrics<br/>Accuracy, F1, AUC]
    
    P --> Q[Report to Ray Tune]
    Q --> R{More Trials?}
    R -->|Yes| I
    R -->|No| S[Select Best Model]
    
    S --> T[Save Best Model<br/>Pickle File]
    S --> U[Save Metrics<br/>CSV/JSON]
    S --> V[Save Ray Results<br/>Ray Tune Format]
    
    %% Styling
    classDef input fill:#e3f2fd
    classDef strategy fill:#e8f5e9
    classDef tune fill:#fff3e0
    classDef train fill:#f3e5f5
    classDef output fill:#fce4ec
    
    class A input
    class B,C,D,E,F strategy
    class G,H,I,J,K,L,M tune
    class N,O,P,Q,R train
    class S,T,U,V output
```

## Data Volume Flow

```mermaid
graph LR
    A[Raw EEG Files<br/>~100 MB per subject] --> B[Preprocessed Data<br/>~150 MB per subject]
    B --> C[Extracted Features<br/>~5 MB per subject]
    C --> D[Transformed Features<br/>~5 MB per subject]
    D --> E[ML Training Data<br/>~50 MB total]
    E --> F[Model Artifacts<br/>~10-50 MB per model]
    
    %% Styling
    classDef raw fill:#e3f2fd
    classDef process fill:#e8f5e9
    classDef feature fill:#fff3e0
    classDef ml fill:#f3e5f5
    classDef model fill:#fce4ec
    
    class A raw
    class B process
    class C,D feature
    class E ml
    class F model
```

## Time Flow Through Pipeline

```mermaid
gantt
    title Pipeline Execution Timeline
    dateFormat X
    axisFormat %s
    
    section Configuration
    Create Config           :0, 60
    
    section PySpark Processing
    Load Data              :60, 120
    Preprocess             :120, 300
    Extract Features       :300, 600
    Transform Features     :600, 900
    Save Data              :900, 960
    
    section Ray ML Training
    Initialize Ray         :960, 1020
    Load Features          :1020, 1080
    Hyperparameter Tuning  :1080, 3600
    Model Evaluation       :3600, 3660
    Save Results           :3660, 3720
```

## Resource Usage Flow

```mermaid
graph TB
    subgraph "PySpark Phase"
        A[CPU: 4-8 cores<br/>Memory: 6-12 GB<br/>Time: 10-30 min]
    end
    
    subgraph "Ray Phase"
        B[CPU: 2-4 cores per trial<br/>Memory: 4-8 GB per trial<br/>Parallel Trials: 4-8<br/>Time: 30-120 min]
    end
    
    subgraph "Storage"
        C[Input: 100 MB/subject<br/>Processed: 5 MB/subject<br/>Models: 10-50 MB/model<br/>Logs: 50-200 MB]
    end
    
    A --> B
    A --> C
    B --> C
    
    %% Styling
    classDef pyspark fill:#e3f2fd
    classDef ray fill:#e8f5e9
    classDef storage fill:#fff3e0
    
    class A pyspark
    class B ray
    class C storage
```


