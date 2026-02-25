#!/bin/bash

# Script to create PDF booklet from markdown files
# Uses pandoc to convert markdown to PDF

set -e

BOOKLET_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_PDF="$BOOKLET_DIR/EEG_Analysis_Booklet.pdf"
TEMP_MD="$BOOKLET_DIR/temp_combined_booklet.md"

# Function to clean markdown (remove YAML frontmatter and emojis from headers)
clean_markdown() {
    local file="$1"
    # Remove YAML frontmatter (lines between --- at start)
    awk '/^---$/{if(++c==2) exit} c<2{next} 1' "$file" | \
    # Remove emojis from headers (common ones)
    sed -E 's/#+ [🎯👥🔍📈📊📋📑✅❌⚠️⭐🔬]+\s*//g' | \
    # Remove empty lines at start
    sed '/./,$!d'
}

echo "📚 Creating PDF Booklet..."
echo ""

# Start with title
echo "# EEG Analysis Booklet - Complete Documentation" > "$TEMP_MD"
echo "" >> "$TEMP_MD"
echo "**Generated:** January 13, 2025" >> "$TEMP_MD"
echo "**Total Files:** 82 markdown files" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"
echo "---" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Add main index (clean it)
echo "## Table of Contents" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"
clean_markdown "$BOOKLET_DIR/00_BOOKLET_INDEX.md" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"
echo "\\newpage" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Add threshold analysis files (most important)
echo "# Threshold Analysis" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Main report first
if [ -f "$BOOKLET_DIR/01_threshold_analysis/anova_pca_L6_L2_threshold_analysis.md" ]; then
    echo "## Main Comprehensive Report" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    clean_markdown "$BOOKLET_DIR/01_threshold_analysis/anova_pca_L6_L2_threshold_analysis.md" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    echo "\\newpage" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
fi

# Uniform vs Random Summary
if [ -f "$BOOKLET_DIR/01_threshold_analysis/UNIFORM_VS_RANDOM_SUMMARY.md" ]; then
    echo "## Uniform vs Random Summary" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    clean_markdown "$BOOKLET_DIR/01_threshold_analysis/UNIFORM_VS_RANDOM_SUMMARY.md" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    echo "\\newpage" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
fi

# Uncertainty and Effect Size Analysis
if [ -f "$BOOKLET_DIR/01_threshold_analysis/UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md" ]; then
    echo "## Uncertainty and Effect Size Analysis" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    clean_markdown "$BOOKLET_DIR/01_threshold_analysis/UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    echo "\\newpage" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
fi

# Same Subjects Control Flowchart
if [ -f "$BOOKLET_DIR/01_threshold_analysis/SAME_SUBJECTS_CONTROL_FLOWCHART.md" ]; then
    echo "## Same Subjects Control Flowchart" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    clean_markdown "$BOOKLET_DIR/01_threshold_analysis/SAME_SUBJECTS_CONTROL_FLOWCHART.md" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    echo "\\newpage" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
fi

# Other threshold analysis files
for file in "$BOOKLET_DIR/01_threshold_analysis"/*.md; do
    if [ -f "$file" ] && [ "$(basename "$file")" != "anova_pca_L6_L2_threshold_analysis.md" ] && \
       [ "$(basename "$file")" != "UNIFORM_VS_RANDOM_SUMMARY.md" ] && \
       [ "$(basename "$file")" != "UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md" ] && \
       [ "$(basename "$file")" != "SAME_SUBJECTS_CONTROL_FLOWCHART.md" ]; then
        echo "## $(basename "$file" .md)" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$file" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
done

# Add per-subject analysis summary
echo "# Per-Subject Classification Analysis" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"

# Main per-subject files
for file in "$BOOKLET_DIR/02_per_subject_analysis"/SUBJECT_SUCCESS_RATE_VARIANCE_SUMMARY.md \
            "$BOOKLET_DIR/02_per_subject_analysis"/CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md \
            "$BOOKLET_DIR/02_per_subject_analysis"/SUMMARY_ALL_EXPERIMENTS.md \
            "$BOOKLET_DIR/02_per_subject_analysis"/analysis_summary.md; do
    if [ -f "$file" ]; then
        echo "## $(basename "$file" .md)" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$file" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
done

# Add clustering
echo "# Clustering Analysis" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"
for file in "$BOOKLET_DIR/03_clustering"/*.md; do
    if [ -f "$file" ]; then
        echo "## $(basename "$file" .md)" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$file" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
done

# Add biomarker analysis
if [ -d "$BOOKLET_DIR/07_biomarkers" ]; then
    echo "# Biomarker Analysis" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    for file in "$BOOKLET_DIR/07_biomarkers"/*.md; do
        if [ -f "$file" ]; then
            echo "## $(basename "$file" .md)" >> "$TEMP_MD"
            echo "" >> "$TEMP_MD"
            clean_markdown "$file" >> "$TEMP_MD"
            echo "" >> "$TEMP_MD"
            echo "\\newpage" >> "$TEMP_MD"
            echo "" >> "$TEMP_MD"
        fi
    done
fi

# Add variance analysis
if [ -d "$BOOKLET_DIR/08_variance_analysis" ]; then
    echo "# Variance Analysis" >> "$TEMP_MD"
    echo "" >> "$TEMP_MD"
    
    # Main comparison first
    if [ -f "$BOOKLET_DIR/08_variance_analysis/ANOVA_PCA_VARIANCE_COMPARISON.md" ]; then
        echo "## ANOVA vs PCA Variance Comparison" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$BOOKLET_DIR/08_variance_analysis/ANOVA_PCA_VARIANCE_COMPARISON.md" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
    
    # PCA analysis
    if [ -f "$BOOKLET_DIR/08_variance_analysis/PCA_VARIANCE_ANALYSIS_SUMMARY.md" ]; then
        echo "## PCA Variance Analysis Summary" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$BOOKLET_DIR/08_variance_analysis/PCA_VARIANCE_ANALYSIS_SUMMARY.md" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
    
    # ANOVA analysis
    if [ -f "$BOOKLET_DIR/08_variance_analysis/ANOVA_VARIANCE_ANALYSIS_SUMMARY.md" ]; then
        echo "## ANOVA Variance Analysis Summary" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$BOOKLET_DIR/08_variance_analysis/ANOVA_VARIANCE_ANALYSIS_SUMMARY.md" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
    
    # Intra-Subject vs LPSO comparison
    if [ -f "$BOOKLET_DIR/08_variance_analysis/INTRASUBJECT_VS_LPSO_COMPARISON.md" ]; then
        echo "## Intra-Subject vs LPSO: Accuracy and Variance Comparison" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$BOOKLET_DIR/08_variance_analysis/INTRASUBJECT_VS_LPSO_COMPARISON.md" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
    
    # LPSO Convergence Analysis
    if [ -f "$BOOKLET_DIR/08_variance_analysis/LPSO_CONVERGENCE_ANALYSIS.md" ]; then
        echo "## LPSO Convergence Analysis: 12-Fold Systematic vs 50-Fold Random" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$BOOKLET_DIR/08_variance_analysis/LPSO_CONVERGENCE_ANALYSIS.md" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
    
    # Intra-Subject Convergence Analysis
    if [ -f "$BOOKLET_DIR/08_variance_analysis/INTRASUBJECT_CONVERGENCE_ANALYSIS.md" ]; then
        echo "## Intra-Subject Convergence Analysis: W_F and W_C Across Random Seeds" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$BOOKLET_DIR/08_variance_analysis/INTRASUBJECT_CONVERGENCE_ANALYSIS.md" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
    
    # LPSO vs Intra-Subject Convergence Comparison
    if [ -f "$BOOKLET_DIR/08_variance_analysis/LPSO_VS_INTRASUBJECT_CONVERGENCE_COMPARISON.md" ]; then
        echo "## LPSO vs Intra-Subject Convergence Comparison" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$BOOKLET_DIR/08_variance_analysis/LPSO_VS_INTRASUBJECT_CONVERGENCE_COMPARISON.md" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
fi

# Add other analyses
echo "# Other Analyses" >> "$TEMP_MD"
echo "" >> "$TEMP_MD"
for file in "$BOOKLET_DIR/05_other_analyses"/*.md; do
    if [ -f "$file" ]; then
        echo "## $(basename "$file" .md)" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        clean_markdown "$file" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
        echo "\\newpage" >> "$TEMP_MD"
        echo "" >> "$TEMP_MD"
    fi
done

# Convert to PDF
echo "📄 Converting to PDF (this may take a minute)..."
pandoc "$TEMP_MD" \
    -o "$OUTPUT_PDF" \
    --pdf-engine=pdflatex \
    -V geometry:margin=1in \
    -V fontsize=10pt \
    -V documentclass=article \
    --toc \
    --toc-depth=2 \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    --syntax-highlighting=tango \
    --wrap=none \
    -V lang=en \
    2>&1 | grep -v "Overfull\|Underfull\|Package\|LaTeX\|Font" || true

# Clean up temp file
rm -f "$TEMP_MD"

if [ -f "$OUTPUT_PDF" ]; then
    echo ""
    echo "✅ PDF created successfully!"
    echo "📄 Output: $OUTPUT_PDF"
    echo "📊 Size: $(du -h "$OUTPUT_PDF" | cut -f1)"
    echo ""
    echo "You can open it with: open $OUTPUT_PDF"
else
    echo ""
    echo "❌ PDF creation failed. Check pandoc and LaTeX installation."
    exit 1
fi



