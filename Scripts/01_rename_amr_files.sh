#!/usr/bin/env bash
# 01_rename_amr_files.sh
# Description: Maps messy Galaxy output files to clean Sample Accessions.
# Requires: 'mapping.csv' (Accession,DataID) and 'datasets/' folder.

set -euo pipefail

# Configuration
MAPPING="../data/mapping.csv"       # Path to your mapping file
INPUT_DIR="../data/datasets"        # Path to the raw Galaxy download folder
OUTPUT_DIR="../data/renamed_outputs" # Where valid renamed files go

# Set DRYRUN to false to actually move files
# Run as: DRYRUN=false ./01_rename_amr_files.sh
DRYRUN="${DRYRUN:-true}"

mkdir -p "$OUTPUT_DIR"
shopt -s nullglob

echo "Starting renaming process..."
echo "Mode: Dry Run = $DRYRUN"

# Read mapping file, skipping header
while IFS=, read -r accession dataid; do
    # Trim whitespace
    accession="${accession//[[:space:]]/}"
    dataid="${dataid//[[:space:]]/}"

    # Skip invalid rows
    if [[ -z "$accession" ]] || [[ "$accession" =~ ^(Accession|accession|#) ]]; then
        continue
    fi

    # Find files matching the DataID pattern
    for f in "$INPUT_DIR"/*"${dataid}"__*; do
        [ -f "$f" ] || continue
        
        base=$(basename "$f")
        newname="${accession}__${base}"
        dest="$OUTPUT_DIR/$newname"

        if [[ "$DRYRUN" == "true" ]]; then
            echo "DRYRUN: $f -> $dest"
        else
            mv -- "$f" "$dest"
            echo "Moved: $f -> $dest"
        fi
    done
done < <(tail -n +2 "$MAPPING")

echo "Renaming complete."