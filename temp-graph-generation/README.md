# Graph Generation Scripts

This directory contains standalone graph generation scripts for EEG ML results analysis.

## Scripts Available

### 1. `simple_graph_generator_no_config.py`
- **Purpose**: Generates per-subject analysis graphs
- **Features**: 
  - Overall per-subject accuracy graph (averaged across all models/hyperparameters)
  - Individual per-subject graphs for each model×hyperparameter combination
  - Color-coded by subject groups
- **Usage**: `python simple_graph_generator_no_config.py <ml_results_path>`

### 2. `hyperparameter_boxplot_generator.py`
- **Purpose**: Generates hyperparameter performance box plots
- **Features**:
  - Individual box plots for each model's hyperparameter combinations
  - Overall comparison box plot across all models
  - 50% accuracy reference line
  - Best and worst performance indicators (green/red dots)
- **Usage**: `python hyperparameter_boxplot_generator.py <ml_results_path>`

### 3. `generate_all_graphs.py`
- **Purpose**: Comprehensive graph generator that creates all types of graphs
- **Features**:
  - Per-subject analysis graphs
  - Hyperparameter box plots
  - Best models comparison graph
  - All features from individual scripts combined
- **Usage**: `python generate_all_graphs.py <ml_results_path>`

## Setup

All scripts are configured to work from this directory with `sys.path.append('..')` to access the parent directory's modules.

## Dependencies

The scripts require the following Python packages:
- pandas
- matplotlib
- seaborn
- numpy
- pathlib (built-in)
- json (built-in)

## Output

All graphs are saved to `<ml_results_path>/graphs/` directory in PNG format with 300 DPI.

## Example Usage

```bash
# Generate all types of graphs
python generate_all_graphs.py /path/to/ml_results

# Generate only per-subject graphs
python simple_graph_generator_no_config.py /path/to/ml_results

# Generate only hyperparameter box plots
python hyperparameter_boxplot_generator.py /path/to/ml_results
```

## Graph Types Generated

1. **Per-Subject Analysis**: Bar charts showing accuracy for each subject
2. **Hyperparameter Box Plots**: Box plots showing performance distribution across hyperparameter combinations
3. **Best Models Comparison**: Bar chart comparing the best performance of each model
4. **Individual Per-Subject Graphs**: Separate graphs for each model×hyperparameter combination

All graphs include proper legends, reference lines, and performance indicators for comprehensive analysis.
