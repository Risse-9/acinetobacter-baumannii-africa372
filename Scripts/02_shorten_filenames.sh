#!/usr/bin/env bash
# 02_shorten_filenames.sh
# Description: Shortens long Galaxy filenames to standard format:
# [Accession]_data[ID]_report.tabular or _sequences.fasta
set -euo pipefail

INPUT_DIR="../data/renamed_outputs"
OUTPUT_DIR="../data/renamed_outputs_short"

mkdir -p "$OUTPUT_DIR"
shopt -s nullglob

echo "Shortening filenames..."

for f in "$INPUT_DIR"/*; do
    base=$(basename "$f")

    # Extract accession (everything before first __)
    accession="${base%%__*}"

    # Extract DataID (digits from 'on_data_XX')
    if [[ "$base" =~ on_data_([0-9]+) ]]; then
        dataid="${BASH_REMATCH[1]}"
    else
        dataid="NA"
    fi

    # Rename based on file type
    if [[ "$base" == *"AMRFinderPlus_report"* ]]; then
        newname="${accession}_data${dataid}_report.tabular"
    elif [[ "$base" == *"Nucleotide_identified_sequences"* ]]; then
        newname="${accession}_data${dataid}_sequences.fasta"
    else
        newname="$base"   # Fallback for unexpected files
    fi

    cp -- "$f" "$OUTPUT_DIR/$newname"
    # echo "$base  -->  $newname" # Uncomment for verbose output
done

echo "Shortening complete. Files saved to $OUTPUT_DIR"