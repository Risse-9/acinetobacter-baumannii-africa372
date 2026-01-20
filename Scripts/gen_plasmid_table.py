# 17_generate_plasmid_table.py
# Description:
#   Analyzes the genomic location (Plasmid vs. Chromosome) of resistance genes.
#   Calculates the count and percentage of each gene found on mobile elements.
#   Output corresponds to Table 4.5 in the thesis.

import pandas as pd
import os

# --- Configuration ---
# Input: The "Super-Table" created in Script 06
INPUT_FILE = "../results/amr_plus_mob_merged.csv"
OUTPUT_FILE = "../results/Table_4_5_Plasmid_Association.csv"

# Genes of interest to highlight (Top 20 or specific ones from your Jottings)
KEY_GENES = [
    "blaOXA-23", "blaNDM-1", "armA", "ant(3'')-IIa", "mph(E)", 
    "sul2", "tet(B)", "aph(3'')-Ib", "msr(E)"
]

def format_cell(count, total):
    """Formats as: Count (Percentage%)"""
    if total == 0:
        return "0 (0.0%)"
    pct = (count / total) * 100
    return f"{count} ({pct:.1f}%)"

def main():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    print(f"Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print("Error: Input file not found. Please run Script 06 first.")
        exit()

    # 1. Pivot the Data
    # We want to count occurrences of each gene on 'chromosome' vs 'plasmid'
    print("Analyzing genomic locations...")
    
    # Create a crosstab (contingency table)
    location_counts = pd.crosstab(df['Gene symbol'], df['molecule_type'])
    
    # Ensure both columns exist (fill with 0 if missing)
    if 'chromosome' not in location_counts.columns:
        location_counts['chromosome'] = 0
    if 'plasmid' not in location_counts.columns:
        location_counts['plasmid'] = 0

    # 2. Calculate Statistics
    location_counts['Total Hits'] = location_counts['chromosome'] + location_counts['plasmid']
    
    # Filter for genes with at least 5 occurrences to keep the table manageable
    # (Or filter for your KEY_GENES list)
    # Using KEY_GENES for the specific Table 4.5 focus:
    # If you prefer ALL genes, comment out the next line.
    location_counts = location_counts[location_counts.index.isin(KEY_GENES)].sort_values('Total Hits', ascending=False)

    # 3. Format the Table
    results = []
    for gene in location_counts.index:
        row = location_counts.loc[gene]
        chrom_n = row['chromosome']
        plas_n = row['plasmid']
        total = row['Total Hits']
        
        results.append({
            'Gene Symbol': gene,
            'Total Detected': total,
            'Chromosome (n (%))': format_cell(chrom_n, total),
            'Plasmid (n (%))': format_cell(plas_n, total)
        })

    final_table = pd.DataFrame(results)

    # 4. Save
    final_table.to_csv(OUTPUT_FILE, index=False)
    print(f"Table 4.5 saved to {OUTPUT_FILE}")
    print("\nPreview:")
    print(final_table)

if __name__ == "__main__":
    main()