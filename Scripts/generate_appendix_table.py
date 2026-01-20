# 16_generate_appendix_table.py
# Description: Merges the final metadata with the full list of resistance genes detected per isolate.
# Generates the comprehensive Appendix 1 table.

import pandas as pd
import os

# --- Configuration ---
# Inputs
METADATA_FILE = "../data/microreact_metadata_final_Copy.xlsx"
AMR_MATRIX_FILE = "../results/amr_results_wide_filtered.csv"

# Output
OUTPUT_FILE = "../results/Appendix_Metadata_Final.csv"

def main():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    print("Loading datasets...")
    try:
        metadata_df = pd.read_excel(METADATA_FILE)
        amr_df = pd.read_csv(AMR_MATRIX_FILE)
    except FileNotFoundError as e:
        print(f"Error: Required file not found: {e.filename}")
        exit()

    # 1. Create the Resistance Genes Column
    # Collapses all binary columns (1s) into a single comma-separated string
    print("Consolidating resistance genes...")
    resistance_gene_columns = amr_df.columns.drop('Name')

    def get_resistance_genes(row):
        genes = []
        for gene_col in resistance_gene_columns:
            if row[gene_col] == 1:
                genes.append(gene_col)
        return ", ".join(genes)

    amr_df['Resistance Genes Detected'] = amr_df.apply(get_resistance_genes, axis=1)

    # 2. Fix the Year Column
    # Remove decimals (e.g., 2021.0 -> 2021) and handle missing values
    if 'Date (Year)' in metadata_df.columns:
        metadata_df['Date (Year)'] = pd.to_numeric(metadata_df['Date (Year)'], errors='coerce').astype('Int64')

    # 3. Select Metadata Columns
    # Adjust these column names if your metadata headers differ slightly
    cols_to_keep = ['id', 'Date (Year)', 'Study Accessions', 'Isolation source', 'Country', 'ST']
    # Check if all columns exist
    existing_cols = [c for c in cols_to_keep if c in metadata_df.columns]
    metadata_subset = metadata_df[existing_cols]

    # 4. Merge Data
    # Join Metadata (id) with AMR Data (Name)
    print("Merging metadata with AMR genotypes...")
    final_df = pd.merge(metadata_subset, amr_df[['Name', 'Resistance Genes Detected']], 
                        left_on='id', right_on='Name', how='left')

    # 5. Rename for Appendix
    final_df = final_df.rename(columns={
        'id': 'Run Accession',
        'Date (Year)': 'Year',
        'Study Accessions': 'Study Accession',
        'Isolation source': 'Isolation Source'
    })

    # 6. Clean up
    if 'Name' in final_df.columns:
        final_df = final_df.drop(columns=['Name'])

    # 7. Output
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Success! Appendix table saved to {OUTPUT_FILE}")
    print("\nFirst 5 rows:")
    print(final_df.head())

if __name__ == "__main__":
    main()