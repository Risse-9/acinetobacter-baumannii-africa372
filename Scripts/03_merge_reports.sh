#!/usr/bin/env bash
# 03_merge_reports.sh
# Description: Merges all individual tabular reports into a single CSV file.

INPUT_DIR="../data/renamed_outputs"
OUTPUT_FILE="../results/merged_amrfinder.csv"

# Ensure output directory exists
mkdir -p ../results

echo "Merging reports into $OUTPUT_FILE"

# Initialize file: Clear it if it exists
> "$OUTPUT_FILE"

# 1. Create Header
# Take header from the first found report, replace tabs with commas, and add "Name" as the first column
first_file=$(ls "$INPUT_DIR"/*report*tabular | head -n 1)
echo "Name,$(head -n 1 "$first_file" | tr '\t' ',')" > "$OUTPUT_FILE"

# 2. Loop and Append Data
# Iterate over each report file
for file in "$INPUT_DIR"/*report*tabular; do
    # Extract Accession from filename (the part before the first underscore
    accession=$(basename "$file" | cut -d'_' -f1)

    # Read file, skip header (tail -n +2), convert tab to comma, prepend Accession
    tail -n +2 "$file" | tr '\t' ',' | sed "s/^/$accession,/" >> "$OUTPUT_FILE"
done

echo "Merge complete. Output saved to $OUTPUT_FILE"