# HPC Results Analysis Scripts

This directory contains scripts for generating comprehensive analysis (graphs and CSV files) from HPC compiled ML results.

## Quick Start

### For a Single Directory

```bash
cd /Users/user/projects/eeg-full-pipeline/data/HPC_All_Data/grid_50_random_folds/PCA_L_2_ml_results
py-neuro-env
python /Users/user/projects/eeg-full-pipeline/data/HPC_All_Data/generate_comprehensive_analysis.py .
```

### For All Directories

```bash
cd /Users/user/projects/eeg-full-pipeline/data/HPC_All_Data
./run_all_analysis.sh
```

## Generated Files

For each `ml_results` directory, the script generates:

### 1. **model_comparison.csv**
   - Model-by-model performance comparison
   - Best test accuracy, std, train accuracy
   - F1, precision, recall metrics
   - Best hyperparameters for each model
   - Sorted by best test accuracy

### 2. **graphs/** Directory
   - **model_comparison_boxplot.png** - Box plots comparing all models
   - **accuracy_distributions_by_model.png** - Histograms showing accuracy distributions per model
   - **fold_performance.png** - Scatter plot showing performance across folds
   - **model_metrics_comparison.png** - Bar charts comparing accuracy, F1, precision, recall

### 3. **detailed_statistics.json**
   - Overall statistics (mean, median, std, min, max)
   - Per-model detailed statistics
   - JSON format for programmatic access

### 4. **detailed_summary.txt**
   - Human-readable summary of all statistics
   - Same information as JSON but formatted for reading

## Script Details

### `generate_comprehensive_analysis.py`

**Purpose**: Generate comprehensive analysis (graphs + CSV) from ML results directory

**Usage**:
```bash
python generate_comprehensive_analysis.py <ml_results_directory>
```

**What it does**:
1. Loads all `results.json` files from the directory (recursively)
2. Aggregates results by model and hyperparameters
3. Finds best hyperparameters for each model
4. Generates model comparison CSV
5. Creates multiple graphs for visualization
6. Generates detailed statistics files

**Requirements**:
- Python with pandas, matplotlib, seaborn, numpy
- Virtual environment with `py-neuro-env` (or activate manually)

### `run_all_analysis.sh`

**Purpose**: Batch script to run analysis on all `ml_results` directories

**Usage**:
```bash
./run_all_analysis.sh
```

**What it does**:
1. Finds all directories named `*ml_results*` in `HPC_All_Data`
2. For each directory:
   - Checks if it has `results.json` files
   - Runs `generate_comprehensive_analysis.py` on it
   - Reports success/failure

## Example Output

### PCA_L_2_ml_results

**Model Comparison Summary:**
```
SVM                       | Accuracy: 0.6045 ± 0.1229 | Folds: 50 | Tasks: 50
KNN                       | Accuracy: 0.5726 ± 0.0985 | Folds: 50 | Tasks: 50
MLP (Neural Network)      | Accuracy: 0.5542 ± 0.1272 | Folds: 50 | Tasks: 50
XGBoost                   | Accuracy: 0.5500 ± 0.0832 | Folds: 50 | Tasks: 50
```

**Overall Statistics:**
- Total results: 600
- Total models: 4
- Total folds: 50
- Mean accuracy: 0.5433 ± 0.0971
- Range: 0.2557 - 0.9044

## Notes

- The scripts work independently of the Ray Tuner pipeline
- They only require `results.json` files (no config file needed for basic analysis)
- Graph generation uses matplotlib with seaborn style
- All graphs are saved as PNG files with 150 DPI
- CSV files are sorted by best test accuracy (descending)

## Troubleshooting

**Issue**: "No results found"
- **Solution**: Make sure the directory contains `results.json` files (check with `find . -name "results.json" | wc -l`)

**Issue**: Import errors
- **Solution**: Make sure you're in the correct virtual environment (`py-neuro-env`) and all dependencies are installed

**Issue**: Graph generation fails
- **Solution**: Check that matplotlib/seaborn are installed. The script will skip graph generation if it fails but will still generate CSV files.

## Future Enhancements

Potential additions:
- Hyperparameter importance analysis
- Cross-model comparison across different configs
- Performance trend analysis over time
- Statistical significance testing between models
- Correlation analysis between hyperparameters and performance


