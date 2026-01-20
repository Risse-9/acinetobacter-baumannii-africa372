#!/bin/bash
# Run MLST (Pasteur scheme)on all fastas, strip extension immediately

INPUT_DIR="../data/fasta_372"
OUTPUT_DIR="../results/mlst"
OUTPUT_FILE="$OUTPUT_DIR/mlst_results.tsv"

mkdir -p "$OUTPUT_DIR"

# Activate environment if needed
# conda activate mlst_env 

echo "Input: $INPUT_DIR"

# Use | as the delimiter in sed because INPUT_DIR contains slashes (/)
mlst "$INPUT_DIR"/*.fasta | sed -e "s|$INPUT_DIR/||g" -e 's/\.fasta//g' > "$OUTPUT_FILE"

echo "MLST results saved to $OUTPUT_FILE"