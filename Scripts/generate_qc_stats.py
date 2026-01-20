# 08_generate_qc_stats.py
# Description: Integrates raw data from FastQC, MultiQC, and QUAST to produce a 
# comprehensive summary table of the genomic quality of 372 A. baumannii isolates.
# Output corresponds to Table 4.1 in the thesis.

import pandas as pd
import numpy as np
import os

# --- Configuration ---
# Paths relative to the 'scripts' folder
MULTIQC_FILE = "../results/multiqc/multiqc_data/multiqc_general_stats.txt"
QUAST_FILE = "../results/quast_results/transposed_report.txt"
PHRED_FILE = "../results/multiqc/multiqc_data/fastqc_per_sequence_quality_scores_plot.txt"
OUTPUT_FILE = "../results/Table_4_1_Summary_Stats.csv"

pd.options.display.float_format = '{:,.2f}'.format

def numeric_summary(series):
    """Calculates summary statistics for a given data series."""
    return {
        'Mean': series.mean(),
        'Median': series.median(),
        'Q1 (25%)': series.quantile(0.25),
        'Q3 (75%)': series.quantile(0.75),
        'Min': series.min(),
        'Max': series.max()
    }

def main():
    print("Loading Quality Control data...")
    rows = []

    # 1. Load Data Sources
    try:
        # Load MultiQC stats
        general_df = pd.read_csv(MULTIQC_FILE, sep='\t')
        # Load QUAST stats (skiprows=2 handles the specific QUAST header format)
        quast_df = pd.read_csv(QUAST_FILE, sep=r'\s{2,}', skiprows=2, engine='python')
    except FileNotFoundError as e:
        print(f"Error: Required input file not found: {e.filename}")
        exit()

    # 2. Calculate Weighted Phred Scores
    try:
        phred_dist = pd.read_csv(PHRED_FILE, sep='\t')
        
        def calculate_weighted_phred(row):
            total_score = 0
            total_reads = 0
            for col in phred_dist.columns[1:]:
                val = row[col]
                if isinstance(val, str) and '(' in val:
                    # Parse 'Score(Count)' format often found in MultiQC plots
                    score, count = eval(val)
                    total_score += (score * count)
                    total_reads += count
            return total_score / total_reads if total_reads > 0 else np.nan

        phred_dist['weighted_mean'] = phred_dist.apply(calculate_weighted_phred, axis=1)
        phred_stats = numeric_summary(phred_dist['weighted_mean'])
        phred_stats.update({'Metric': 'Mean Phred Score (Q)', 'Category': 'Raw Reads'})
        rows.append(phred_stats)
        
    except FileNotFoundError:
        print("Warning: Phred distribution file not found. Skipping Weighted Phred calculation.")

    # 3. Process Numeric Metrics
    metrics_to_process = {
        # Category: Raw Reads
        'Total Sequences (Millions)': (general_df['fastqc-total_sequences'], 'Raw Reads'),
        'Sequence Duplication (%)': (general_df['fastqc-percent_duplicates'], 'Raw Reads'),
        'Read GC Content (%)': (general_df['fastqc-percent_gc'], 'Raw Reads'),
        
        # Category: Assembly
        'Genome Size (Mbp)': (quast_df['Total length'] / 1e6, 'Assembly'),
        'Assembly GC Content (%)': (quast_df['GC (%)'], 'Assembly'),
        'N50 Value (bp)': (quast_df['N50'], 'Assembly'),
        'N90 Value (bp)': (quast_df['N90'], 'Assembly'), 
        'L50 (Contig Count)': (quast_df['L50'], 'Assembly'),
        'L90 (Contig Count)': (quast_df['L90'], 'Assembly')
    }

    for metric, (series, category) in metrics_to_process.items():
        stats = numeric_summary(series)
        stats.update({'Metric': metric, 'Category': category})
        rows.append(stats)

    # 4. Consolidate and Export
    raw_reads_qc_df = pd.DataFrame(rows)
    
    # Reorder columns for readability
    cols_order = ['Category', 'Metric', 'Mean', 'Median', 'Q1 (25%)', 'Q3 (75%)', 'Min', 'Max']
    raw_reads_qc_df = raw_reads_qc_df[cols_order]

    # Save to CSV
    raw_reads_qc_df.round(2).to_csv(OUTPUT_FILE, index=False)
    print(f"Success. Quality statistics saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()