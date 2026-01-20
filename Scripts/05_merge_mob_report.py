# 05_merge_mob_reports.py
# Description: This script recursively searches the 'mobsuite_results' directory for
# 'contig_report.txt' files. It concatenates them into a single master CSV
# file to facilitate downstream analysis of plasmid/chromosomal locations.

import pandas as pd
import glob
import os
# --- Configuration ---
SEARCH_DIR = "../data/mobsuite_results"
OUTPUT_FILE = "../results/master_mob_report.csv"

print(f"Initiating search for contig reports in: {SEARCH_DIR}...")

# 1. Search for all 'contig_report.txt' files
search_pattern = os.path.join(SEARCH_DIR, "**", "contig_report.txt")
all_files = glob.glob(search_pattern, recursive=True)

if not all_files:
    print("Error: No 'contig_report.txt' files found. Please verify the SEARCH_DIR path.")
    exit()

print(f"Found {len(all_files)} report files. Beginning merge process...")

# 2. Read each file into a list of DataFrames
all_data_list = []
for f in all_files:
    try:
        df = pd.read_csv(f, sep='\t')
        all_data_list.append(df)
    except pd.errors.EmptyDataError:
        print(f"Warning: Skipped empty file: {f}")

# 3. Concatenate all DataFrames and save to CSV
if all_data_list:
    master_df = pd.concat(all_data_list, ignore_index=True)
    master_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Processing complete. Master report saved to: {OUTPUT_FILE}")
    print(f"Total rows merged: {len(master_df)}")
else:
    print("Error: No valid data found to merge.")