# 15_generate_st_prevalence_table.py
# Description: Calculates the prevalence (count and percentage) of selected resistance genes
# within the major Sequence Types (STs).
# Output corresponds to Table 4.4 in the thesis.

import pandas as pd
import os

# --- Configuration ---
# Inputs
WIDE_MATRIX_FILE = "../results/amr_results_wide_filtered.csv"
METADATA_FILE = "../data/microreact_metadata_final_Copy.xlsx"

# Output
OUTPUT_FILE = "../results/Table_4_4_ST_Prevalence.csv"

# Parameters
MAJOR_STS = [1, 2, 10, 25, 85, 164]
KEY_GENES = ["ant(3'')-IIa", "blaOXA-23", "sul2", "msr(E)", "tet(B)", "blaNDM-1", "armA"]

def format_cell(series):
    """
    Helper function to format the output as 'Count (Percentage%)'.
    """
    count = series.sum()
    total = len(series)
    percent = (count / total) * 100 if total > 0 else 0
    return f"{int(count)} ({percent:.1f}%)"

def main():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    print("Loading datasets...")
    try:
        # Load AMR matrix (Index 0 is usually 'Name' or 'id')
        wide = pd.read_csv(WIDE_MATRIX_FILE, index_col=0)
        # Load Metadata
        meta = pd.read_excel(METADATA_FILE, index_col='id')
    except FileNotFoundError as e:
        print(f"Error: Input file not found: {e.filename}")
        exit()

    print("Merging ST information...")
    # Prepare DataFrame: Start with the AMR matrix
    df = wide.copy()
    
    # Map Sequence Type (ST) from metadata to the AMR matrix
    # Align indices (Sample IDs) to ensure correct mapping
    common_indices = df.index.intersection(meta.index)
    df.loc[common_indices, 'ST'] = meta.loc[common_indices, 'ST']

    # Filter for the specified Major STs
    print(f"Filtering for Major STs: {MAJOR_STS}...")
    df_filtered = df[df['ST'].isin(MAJOR_STS)]

    # Check if we have data after filtering
    if df_filtered.empty:
        print("Warning: No isolates found for the specified STs.")
    
    # Check if all key genes exist in the dataset
    missing_genes = [g for g in KEY_GENES if g not in df.columns]
    if missing_genes:
        print(f"Warning: The following genes were not found in the dataset: {missing_genes}")
        # Proceed only with existing genes
        available_genes = [g for g in KEY_GENES if g in df.columns]
    else:
        available_genes = KEY_GENES

    print("Calculating prevalence statistics...")
    # Group by ST and apply the formatting function to each key gene
    st_table = df_filtered.groupby('ST')[available_genes].agg(format_cell)

    # Add an 'N' column (Total number of isolates per ST)
    st_counts = df_filtered.groupby('ST').size()
    st_table.insert(0, 'Total (n)', st_counts)

    # Save to CSV
    st_table.to_csv(OUTPUT_FILE)
    print(f"Table saved to {OUTPUT_FILE}")
    
    # Display preview
    print("\nTable Preview:")
    print(st_table)

if __name__ == "__main__":
    main()