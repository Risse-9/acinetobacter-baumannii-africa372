# 06_link_amr_to_location.py
# Description: This script merges the aggregated AMRFinder results with the master MOB-suite
# report. An inner join is performed on 'Sample Name' and 'Contig ID' to link
# each resistance gene to its specific genomic molecule (plasmid or chromosome).

import pandas as pd

# --- Configuration ---
AMR_FILE = "../results/merged_amrfinder.csv"
MOB_FILE = "../results/master_mob_report.csv"
OUTPUT_FILE = "../results/amr_plus_mob_merged.csv"

print("Loading input datasets...")

# 1. Load the AMR and MOB-suite datasets
try:
    amr_df = pd.read_csv(AMR_FILE)
    mob_df = pd.read_csv(MOB_FILE)
except FileNotFoundError:
    print("Error: One or more input files not found in '../results/'.")
    exit()

print(f"AMR Data Loaded: {len(amr_df)} rows")
print(f"MOB Data Loaded: {len(mob_df)} rows")

# 2. Perform Inner Join
# Matches AMR 'Name' to MOB 'sample_id' AND AMR 'Contig id' to MOB 'contig_id'
print("Merging datasets based on Sample ID and Contig ID...")

merged_df = pd.merge(
    amr_df,
    mob_df,
    left_on=['Name', 'Contig id'],
    right_on=['sample_id', 'contig_id'],
    how='inner'
)

print(f"Merge successful. Linked {len(merged_df)} resistance genes to genomic locations.")

# 3. Save the merged dataset
merged_df.to_csv(OUTPUT_FILE, index=False)
print(f"Merged output saved to: {OUTPUT_FILE}")