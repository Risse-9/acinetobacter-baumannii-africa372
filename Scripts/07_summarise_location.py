# 07_summarize_location.py
# Description: This script subsets the merged dataset to retain only the essential columns
# required for the final manuscript tables. It produces a clean CSV containing
# Sample ID, Contig ID, Gene Symbol, and Molecule Type.

import pandas as pd

# --- Configuration ---
INPUT_FILE = "../results/amr_plus_mob_merged.csv"
OUTPUT_FILE = "../results/amr_location_summary.csv"

# Define the columns to be extracted for the final report
COLUMNS_TO_KEEP = [
    'Name',          # Sample Accession ID
    'Contig id',     # Contig Identifier
    'Gene symbol',   # Antimicrobial Resistance Gene
    'molecule_type'  # Genomic Location (plasmid/chromosome)
]

print(f"Loading merged dataset: {INPUT_FILE}...")

# 1. Load the merged dataset
try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    print(f"Error: Input file '{INPUT_FILE}' not found.")
    exit()

# 2. Extract selected columns
print("Extracting summary columns...")
try:
    clean_df = df[COLUMNS_TO_KEEP]
except KeyError as e:
    print(f"Error: Missing expected column in dataset: {e}")
    exit()

# 3. Save the summary table
clean_df.to_csv(OUTPUT_FILE, index=False)
print(f"Processing complete. Summary table saved to: {OUTPUT_FILE}")

# Display the first 5 rows for verification
print("\nFirst 5 rows of output:")
print(clean_df.head())