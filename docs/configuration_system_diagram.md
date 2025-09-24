# Configuration System - Detailed Architecture

## Configuration Flow

```mermaid
graph TB
    %% User Interface
    subgraph "User Interface"
        A[config-maker.py] --> B[Interactive CLI]
        B --> C[Questionary Library]
        C --> D[User Input Validation]
    end
    
    %% Configuration Sections
    subgraph "Configuration Sections"
        E[Project Metadata]
        F[Data Input]
        G[Preprocessing]
        H[Feature Extraction]
        I[Feature Transformation]
        J[Data Leakage Prevention]
        K[PySpark Settings]
    end
    
    %% Output
    subgraph "Output"
        L[config_<project>_<date>_<time>.yaml]
        M[Configuration Backup]
        N[Validation Report]
    end
    
    %% Validation
    subgraph "Validation"
        O[Path Validation]
        P[Parameter Validation]
        Q[Format Validation]
        R[Cross-reference Check]
    end
    
    %% Connections
    A --> E
    A --> F
    A --> G
    A --> H
    A --> I
    A --> J
    A --> K
    
    E --> O
    F --> P
    G --> Q
    H --> R
    
    O --> L
    P --> M
    Q --> N
    R --> L
    
    %% Styling
    classDef ui fill:#e1f5fe
    classDef config fill:#e8f5e8
    classDef output fill:#fff3e0
    classDef validation fill:#fce4ec
    
    class A,B,C,D ui
    class E,F,G,H,I,J,K config
    class L,M,N output
    class O,P,Q,R validation
```

## Interactive Configuration Process

```mermaid
flowchart TD
    %% Configuration Steps
    A[Start config-maker.py] --> B[Project Metadata]
    B --> C[Data Input Configuration]
    C --> D[Preprocessing Settings]
    D --> E[Feature Extraction]
    E --> F[Feature Transformation]
    F --> G[Data Leakage Prevention]
    G --> H[PySpark Configuration]
    H --> I[Save Configuration]
    
    %% Project Metadata Details
    subgraph "Project Metadata"
        J[Project Name: testMacMini]
        K[Output Directory: ./data]
        L[Experiment Type: Classification]
        M[Subjects or Events: subjects]
        N[Artifact Removal: Auto-reject]
    end
    
    %% Data Input Details
    subgraph "Data Input"
        O[Groups: alz, control]
        P[File Paths: .set files]
        Q[Reuse Settings: Yes/No]
        R[Save Settings: Yes/No]
    end
    
    %% Preprocessing Details
    subgraph "Preprocessing"
        S[Frequency Bands: Delta, Theta, Alpha, Beta]
        T[Window Size: 3.0s]
        U[Sliding Window: 0.5s]
        V[Downsampling: null]
    end
    
    %% Feature Extraction Details
    subgraph "Feature Extraction"
        W[Method: Welch]
        X[Features: Band Power]
        Y[Per Channel: Yes/No]
        Z[Per Band: Yes/No]
    end
    
    B --> J
    B --> K
    B --> L
    B --> M
    B --> N
    
    C --> O
    C --> P
    C --> Q
    C --> R
    
    D --> S
    D --> T
    D --> U
    D --> V
    
    E --> W
    E --> X
    E --> Y
    E --> Z
    
    %% Styling
    classDef steps fill:#e1f5fe
    classDef metadata fill:#e8f5e8
    classDef data fill:#fff3e0
    classDef preprocessing fill:#fce4ec
    classDef features fill:#f3e5f5
    
    class A,B,C,D,E,F,G,H,I steps
    class J,K,L,M,N metadata
    class O,P,Q,R data
    class S,T,U,V preprocessing
    class W,X,Y,Z features
```

## Configuration File Structure

```mermaid
graph TD
    %% Configuration Structure
    subgraph "Configuration File Structure"
        A[project]
        B[data_input]
        C[preprocessing]
        D[feature_extraction]
        E[feature_transformation]
        F[data_leakage_prevention]
        G[pyspark]
    end
    
    %% Project Section
    subgraph "Project Section"
        A1[name: testMacMini]
        A2[output_dir: ./data]
        A3[experiment_type: Classification]
        A4[subjects_or_events: subjects]
        A5[artifact_removal: Auto-reject]
    end
    
    %% Data Input Section
    subgraph "Data Input Section"
        B1[groups]
        B2[reuse_processed_subjects: Yes]
        B3[save_processed_subjects: Yes]
        B6[reuse_transformed: Yes]
        B7[save_transformed: Yes]
    end
    
    %% Groups Subsection
    subgraph "Groups"
        C1[alz: [sub-001, sub-002]]
        C2[control: [sub-037, sub-038]]
    end
    
    %% Preprocessing Section
    subgraph "Preprocessing Section"
        D1[bands]
        D2[window_size: 3.0]
        D3[sliding_window: 0.5]
        D4[downsampling: null]
    end
    
    %% Bands Subsection
    subgraph "Frequency Bands"
        E1[Delta: [0.5, 4]]
        E2[Theta: [4, 8]]
        E3[Alpha: [8, 12]]
        E4[Beta: [12, 30]]
    end
    
    %% Feature Extraction Section
    subgraph "Feature Extraction Section"
        F1[method: Welch]
        F2[features: [Band Power]]
    end
    
    %% PySpark Section
    subgraph "PySpark Section"
        G1[master: 4]
        G2[driver_memory: 6]
        G3[executor_memory: 6]
        G4[executor_cores: 2]
        G5[shuffle_partitions: 8]
    end
    
    %% Connections
    A --> A1
    A --> A2
    A --> A3
    A --> A4
    A --> A5
    
    B --> B1
    B --> B2
    B --> B3
    B --> B4
    B --> B5
    B --> B6
    B --> B7
    
    B1 --> C1
    B1 --> C2
    
    C --> D1
    C --> D2
    C --> D3
    C --> D4
    
    D1 --> E1
    D1 --> E2
    D1 --> E3
    D1 --> E4
    
    D --> F1
    D --> F2
    
    G --> G1
    G --> G2
    G --> G3
    G --> G4
    G --> G5
    
    %% Styling
    classDef main fill:#e1f5fe
    classDef project fill:#e8f5e8
    classDef data fill:#fff3e0
    classDef preprocessing fill:#fce4ec
    classDef pyspark fill:#f3e5f5
    
    class A,B,C,D,E,F,G main
    class A1,A2,A3,A4,A5 project
    class B1,B2,B3,B4,B5,B6,B7,C1,C2 data
    class D1,D2,D3,D4,E1,E2,E3,E4,F1,F2 preprocessing
    class G1,G2,G3,G4,G5 pyspark
```

## Configuration Validation Process

```mermaid
sequenceDiagram
    participant User
    participant ConfigMaker
    participant Validator
    participant FileSystem
    participant YAML
    
    User->>ConfigMaker: Run config-maker.py
    ConfigMaker->>User: Interactive prompts
    
    loop Configuration Sections
        User->>ConfigMaker: Provide input
        ConfigMaker->>Validator: Validate input
        Validator->>FileSystem: Check file paths
        FileSystem->>Validator: Path status
        Validator->>ConfigMaker: Validation result
        ConfigMaker->>User: Confirm or retry
    end
    
    ConfigMaker->>YAML: Generate config file
    YAML->>FileSystem: Save config.yaml
    FileSystem->>ConfigMaker: Save confirmation
    ConfigMaker->>User: Configuration complete
    
    Note over ConfigMaker: Validates:<br/>- File paths exist<br/>- Parameter ranges<br/>- Required fields<br/>- Cross-references
```

## Configuration File Naming Convention

```mermaid
graph LR
    %% File Naming
    subgraph "File Naming Convention"
        A[config_]
        B[project_name]
        C[_]
        D[day-month-year]
        E[_]
        F[HHMM]
        G[.yaml]
    end
    
    %% Example
    subgraph "Example"
        H[config_testMacMini_01-08-2025_1353.yaml]
    end
    
    %% Components
    subgraph "Components"
        I[Prefix: config_]
        J[Project: testMacMini]
        K[Date: 01-08-2025]
        L[Time: 1353]
        M[Extension: .yaml]
    end
    
    A --> I
    B --> J
    C --> K
    D --> L
    E --> M
    F --> H
    G --> H
    
    %% Styling
    classDef naming fill:#e1f5fe
    classDef example fill:#e8f5e8
    classDef components fill:#fff3e0
    
    class A,B,C,D,E,F,G naming
    class H example
    class I,J,K,L,M components
```

## Configuration Reuse System

```mermaid
graph TB
    %% Reuse System
    subgraph "Configuration Reuse"
        A[Load Previous Config]
        B[Modify Parameters]
        C[Save New Config]
        D[Version Control]
    end
    
    %% Hash-based Caching
    subgraph "Hash-based Caching"
        E[Config Hash]
        F[Data Hash]
        G[Output Hash]
        H[Cache Validation]
    end
    
    %% Reuse Options
    subgraph "Reuse Options"
        I[reuse_processed_subjects: Yes/No]
        J[reuse_transformed: Yes/No]
        K[save_processed_subjects: Yes/No]
        L[save_transformed: Yes/No]
    end
    
    %% Cache Files
    subgraph "Cache Files"
        O[.config_hash.txt]
        P[.data_hash.txt]
        Q[.output_hash.txt]
        R[_SUCCESS]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> O
    J --> P
    K --> Q
    L --> R
    
    %% Styling
    classDef reuse fill:#e1f5fe
    classDef cache fill:#e8f5e8
    classDef options fill:#fff3e0
    classDef files fill:#fce4ec
    
    class A,B,C,D reuse
    class E,F,G,H cache
    class I,J,K,L,M,N options
    class O,P,Q,R files
``` 