# Deployment Architecture - Container Orchestration

## Deployment Options Overview

```mermaid
graph TB
    %% Deployment Methods
    subgraph "Deployment Methods"
        A[Docker Local]
        B[Singularity Local]
        C[Singularity + SLURM]
        D[Multi-node Cluster]
    end
    
    %% Environment Types
    subgraph "Environment Types"
        E[Development]
        F[Testing]
        G[Production]
        H[HPC/Research]
    end
    
    %% Container Types
    subgraph "Container Types"
        I[eeg-pyspark-pipeline]
        J[eeg-ray-tuner]
        K[Shared Data Volume]
        L[Configuration Mounts]
    end
    
    %% Orchestration
    subgraph "Orchestration"
        M[Docker Compose]
        N[SLURM Job Scheduler]
        O[Ray Cluster]
        P[Manual Execution]
    end
    
    %% Connections
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    %% Styling
    classDef deployment fill:#e1f5fe
    classDef environment fill:#e8f5e8
    classDef container fill:#fff3e0
    classDef orchestration fill:#fce4ec
    
    class A,B,C,D deployment
    class E,F,G,H environment
    class I,J,K,L container
    class M,N,O,P orchestration
```

## Docker Deployment Architecture

```mermaid
graph TB
    %% Docker Components
    subgraph "Docker Environment"
        A[Docker Engine]
        B[Docker Compose]
        C[Docker Images]
        D[Volume Mounts]
    end
    
    %% Container Services
    subgraph "Container Services"
        E[eeg-pyspark-pipeline:latest]
        F[eeg-ray-tuner:latest]
        G[Shared Data Volume]
        H[Configuration Files]
    end
    
    %% Network
    subgraph "Network"
        I[Docker Network]
        J[Port Mapping]
        K[Service Discovery]
        L[Load Balancing]
    end
    
    %% Resources
    subgraph "Resource Allocation"
        M[CPU Limits]
        N[Memory Limits]
        O[Storage Limits]
        P[Network Limits]
    end
    
    %% Connections
    A --> B
    B --> C
    C --> D
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    %% Styling
    classDef docker fill:#e1f5fe
    classDef services fill:#e8f5e8
    classDef network fill:#fff3e0
    classDef resources fill:#fce4ec
    
    class A,B,C,D docker
    class E,F,G,H services
    class I,J,K,L network
    class M,N,O,P resources
```

## Singularity Deployment Architecture

```mermaid
graph TB
    %% Singularity Components
    subgraph "Singularity Environment"
        A[Singularity Runtime]
        B[SIF Files]
        C[Bind Mounts]
        D[Environment Variables]
    end
    
    %% Container Images
    subgraph "Container Images"
        E[eeg-pyspark.sif]
        F[eeg-ray-tuner.sif]
        G[Base Images]
        H[Custom Images]
    end
    
    %% HPC Integration
    subgraph "HPC Integration"
        I[SLURM Scheduler]
        J[Resource Allocation]
        K[Job Submission]
        L[Job Monitoring]
    end
    
    %% File System
    subgraph "File System"
        M[Shared Storage]
        N[Scratch Directory]
        O[Archive Storage]
        P[User Home]
    end
    
    %% Connections
    A --> B
    B --> C
    C --> D
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    %% Styling
    classDef singularity fill:#e1f5fe
    classDef images fill:#e8f5e8
    classDef hpc fill:#fff3e0
    classDef filesystem fill:#fce4ec
    
    class A,B,C,D singularity
    class E,F,G,H images
    class I,J,K,L hpc
    class M,N,O,P filesystem
```

## SLURM Job Scheduling

```mermaid
flowchart TD
    %% SLURM Workflow
    A[Submit Job] --> B[SLURM Scheduler]
    B --> C[Resource Allocation]
    C --> D[Job Execution]
    D --> E[Job Completion]
    E --> F[Results Collection]
    
    %% Job Types
    subgraph "Job Types"
        G[PySpark Job]
        H[Ray Tuner Job]
        I[Dependency Job]
        J[Cleanup Job]
    end
    
    %% Resource Requirements
    subgraph "Resource Requirements"
        K[CPU: 4 cores]
        L[Memory: 6GB]
        M[Time: 2 hours]
        N[Partition: compute]
    end
    
    %% Job Dependencies
    subgraph "Job Dependencies"
        O[After: PySpark Job]
        P[Before: Ray Tuner Job]
        Q[Parallel: Independent Jobs]
        R[Sequential: Dependent Jobs]
    end
    
    %% Job States
    subgraph "Job States"
        S[PENDING]
        T[RUNNING]
        U[COMPLETED]
        V[FAILED]
    end
    
    A --> G
    B --> H
    C --> I
    D --> J
    
    G --> K
    H --> L
    I --> M
    J --> N
    
    K --> O
    L --> P
    M --> Q
    N --> R
    
    O --> S
    P --> T
    Q --> U
    R --> V
    
    %% Styling
    classDef workflow fill:#e1f5fe
    classDef jobs fill:#e8f5e8
    classDef resources fill:#fff3e0
    classDef dependencies fill:#fce4ec
    classDef states fill:#f3e5f5
    
    class A,B,C,D,E,F workflow
    class G,H,I,J jobs
    class K,L,M,N resources
    class O,P,Q,R dependencies
    class S,T,U,V states
```

## Multi-node Deployment

```mermaid
graph LR
    %% Cluster Architecture
    subgraph "Cluster Nodes"
        A[Head Node]
        B[Compute Node 1]
        C[Compute Node 2]
        D[Compute Node N]
    end
    
    %% Services Distribution
    subgraph "Service Distribution"
        E[Spark Master]
        F[Spark Workers]
        G[Ray Head]
        H[Ray Workers]
    end
    
    %% Data Distribution
    subgraph "Data Distribution"
        I[Shared File System]
        J[Data Partitioning]
        K[Load Balancing]
        L[Fault Tolerance]
    end
    
    %% Communication
    subgraph "Communication"
        M[Network Fabric]
        N[Message Passing]
        O[Synchronization]
        P[Coordination]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    %% Styling
    classDef nodes fill:#e1f5fe
    classDef services fill:#e8f5e8
    classDef data fill:#fff3e0
    classDef communication fill:#fce4ec
    
    class A,B,C,D nodes
    class E,F,G,H services
    class I,J,K,L data
    class M,N,O,P communication
```

## Container Build Process

```mermaid
sequenceDiagram
    participant User
    participant BuildSystem
    participant DockerHub
    participant Registry
    participant HPC
    
    User->>BuildSystem: Build Docker images
    BuildSystem->>DockerHub: Pull base images
    DockerHub->>BuildSystem: Base images
    BuildSystem->>BuildSystem: Build custom images
    BuildSystem->>Registry: Push images
    
    User->>HPC: Build SIF files
    HPC->>Registry: Pull Docker images
    Registry->>HPC: Docker images
    HPC->>HPC: Convert to SIF
    HPC->>HPC: Store SIF files
    
    Note over BuildSystem: Docker build process<br/>- Multi-stage builds<br/>- Layer optimization<br/>- Security scanning
    Note over HPC: Singularity build process<br/>- SIF conversion<br/>- HPC optimization<br/>- Security validation
```

## Volume Mount Configuration

```mermaid
graph TB
    %% Volume Mounts
    subgraph "Volume Mounts"
        A[Host Paths]
        B[Container Paths]
        C[Mount Types]
        D[Permissions]
    end
    
    %% PySpark Mounts
    subgraph "PySpark Container"
        E[./config/spark → /opt/bitnami/spark/conf]
        F[./data → /app/data]
        G[./logs/spark-events → /opt/bitnami/spark/logs]
        H[./config → /app/config]
    end
    
    %% Ray Tuner Mounts
    subgraph "Ray Tuner Container"
        I[./data → /app/data]
        J[./config → /app/config]
        K[./logs → /app/logs]
        L[./models → /app/models]
    end
    
    %% Shared Volumes
    subgraph "Shared Volumes"
        M[Data Volume]
        N[Config Volume]
        O[Logs Volume]
        P[Results Volume]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    %% Styling
    classDef mounts fill:#e1f5fe
    classDef pyspark fill:#e8f5e8
    classDef ray fill:#fff3e0
    classDef shared fill:#fce4ec
    
    class A,B,C,D mounts
    class E,F,G,H pyspark
    class I,J,K,L ray
    class M,N,O,P shared
```

## Deployment Configuration

```mermaid
graph LR
    %% Configuration Sections
    subgraph "Deployment Configuration"
        A[Deployment Method]
        B[Resource Allocation]
        C[Network Settings]
        D[Storage Settings]
    end
    
    %% Deployment Methods
    subgraph "Available Methods"
        E[Docker Local]
        F[Singularity Local]
        G[Singularity + SLURM]
        H[Multi-node]
    end
    
    %% Resource Settings
    subgraph "Resource Settings"
        I[CPU: 4 cores]
        J[Memory: 6GB]
        K[Storage: 10GB]
        L[Network: 1Gbps]
    end
    
    %% SLURM Options
    subgraph "SLURM Options"
        M[--nodes=1]
        N[--cpus-per-task=4]
        O[--mem=6G]
        P[--time=02:00:00]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> J
    G --> K
    H --> L
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    %% Styling
    classDef config fill:#e1f5fe
    classDef methods fill:#e8f5e8
    classDef resources fill:#fff3e0
    classDef slurm fill:#fce4ec
    
    class A,B,C,D config
    class E,F,G,H methods
    class I,J,K,L resources
    class M,N,O,P slurm
``` 