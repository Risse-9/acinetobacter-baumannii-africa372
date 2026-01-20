# 04_filter_amr_matrix.py
# Description: Filters AMR hits by Identity/Coverage and converts to binary matrix.

import pandas as pd
import sys

# --- CONFIGURATION ---
INPUT_FILE = '../results/merged_amrfinder.csv' 
OUTPUT_FILE = '../results/amr_results_wide_filtered.csv'

# Quality Thresholds
MIN_IDENTITY = 90.0
MIN_COVERAGE = 80.0  

def main():
    print(f"Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"ERROR: File not found at {INPUT_FILE}")
        sys.exit(1)

    original_rows = len(df)
    print(f"Loaded {original_rows} total gene hits.")

    # --- FILTERING ---
    print(f"Filtering hits: Identity >= {MIN_IDENTITY}% AND Coverage >= {MIN_COVERAGE}%")
    
    # Ensure columns exist
    id_col = '% Identity to reference sequence'
    cov_col = '% Coverage of reference sequence'
    
    if id_col not in df.columns or cov_col not in df.columns:
        print("ERROR: Missing required Identity/Coverage columns in CSV.")
        sys.exit(1)

    df_filtered = df[
        (df[id_col] >= MIN_IDENTITY) &
        (df[cov_col] >= MIN_COVERAGE)
    ]

    print(f"Filtered. Kept {len(df_filtered)} of {original_rows} hits.")

    # --- PIVOTING (Long to Wide) ---
    print("Pivoting to wide format (Presence/Absence matrix)...")
    
    # Pivot: Index=Sample, Columns=Gene Symbol
    amr_wide = df_filtered.pivot_table(
        index='Name', 
        columns='Gene symbol', 
        aggfunc='size', 
        fill_value=0
    )

    # Convert counts (1, 2, 3...) to binary (1/0)
    amr_wide[amr_wide > 0] = 1
    
    # Reset index to make 'Name' a regular column
    amr_wide = amr_wide.reset_index()

    # Save
    print(f"Saving to {OUTPUT_FILE}...")
    amr_wide.to_csv(OUTPUT_FILE, index=False)
    print("Success!")

if __name__ == "__main__":
    main()