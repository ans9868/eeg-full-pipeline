#!/bin/bash
# Run comprehensive analysis on all ML results directories

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANALYSIS_SCRIPT="$SCRIPT_DIR/generate_comprehensive_analysis.py"

echo "=============================================================="
echo "BATCH ANALYSIS - ALL HPC RESULTS"
echo "=============================================================="
echo ""

# Activate virtual environment
if command -v py-neuro-env &> /dev/null; then
    source "$(which py-neuro-env)"
fi

# Find all ml_results directories
find "$SCRIPT_DIR" -type d -name "*ml_results*" | while read -r dir; do
    echo ""
    echo "=============================================================="
    echo "Processing: $dir"
    echo "=============================================================="
    
    # Check if directory has results.json files
    result_count=$(find "$dir" -name "results.json" | wc -l | xargs)
    
    if [ "$result_count" -gt 0 ]; then
        echo "  Found $result_count results.json files"
        echo "  Running analysis..."
        
        # Run analysis script
        python "$ANALYSIS_SCRIPT" "$dir"
        
        if [ $? -eq 0 ]; then
            echo "  ✅ Analysis complete for: $dir"
        else
            echo "  ⚠️  Analysis failed for: $dir"
        fi
    else
        echo "  ⚠️  No results.json files found, skipping..."
    fi
done

echo ""
echo "=============================================================="
echo "BATCH ANALYSIS COMPLETE"
echo "=============================================================="


