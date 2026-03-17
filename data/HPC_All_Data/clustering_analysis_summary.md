
    THREE TYPES OF CLUSTERING PERFORMED:

    1. SUBJECT PERFORMANCE CLUSTERING
       - Groups subjects by their accuracy patterns across experiments
       - Reveals subject types: consistently good/bad performers, ANOVA/PCA specialists
       - Uses K-means with optimal cluster determination

    2. HYPERPARAMETER PERFORMANCE CLUSTERING
       - Groups hyperparameter combinations by their performance characteristics
       - Identifies "winning" hyperparameter profiles across models
       - Shows which parameter combinations work well together

    3. SUBJECT VARIABILITY CLUSTERING
       - Groups subjects by how much their performance varies across models
       - Identifies stable vs. unstable subjects
       - Uses both DBSCAN (density-based) and K-means approaches

    KEY INSIGHTS:
    - Some subjects are consistently classifiable regardless of model/params
    - Others show massive performance swings (up to 74% accuracy difference)
    - Certain hyperparameter combinations consistently outperform others
    - Performance variability may indicate biological heterogeneity in Alzheimer's

    FILES GENERATED:
    - subject_performance_clusters.png
    - hyperparameter_clusters.png
    - subject_variability_clusters.png
    