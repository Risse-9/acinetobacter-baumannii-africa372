#!/bin/bash
# Run MLST (Pasteur scheme)on all fastas, strip extension immediately

INPUT_DIR="../data/fasta_372"
OUTPUT_DIR="../results/mlst"
OUTPUT_FILE="$OUTPUT_DIR/mlst_results.tsv"

mkdir -p "$OUTPUT_DIR"

# Activate environment if needed
# conda activate mlst_env 

echo "Input: $INPUT_DIR"

mlst "$INPUT_DIR"/*.fasta | sed 's/\.fasta//g' > "$OUTPUT_FILE"

echo "MLST results saved to $OUTPUT_FILE"