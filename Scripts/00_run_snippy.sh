#!/bin/bash
# Description: Runs Snippy on all genomes in a folder.
# Uses conservative resource limits (4GB RAM) to prevent crashing.

set -e 

# --- CONFIGURATION ---
# Point to the reference file inside the main folder
REF_GENOME="../data/fasta_372/ERR10710700.fasta"
# Point to the folder containing ALL 372 fastas
GENOME_DIR="../data/fasta_372"

# Output directories
FINAL_OUTPUT_DIR="../results/snippy_final_core"
INTERMEDIATE_DIR="../results/snippy_out"

# --- RESOURCE LIMITS ---
CPUS_TO_USE=4
RAM_IN_GB=4

# 1. Setup
mkdir -p "$FINAL_OUTPUT_DIR"
mkdir -p "$INTERMEDIATE_DIR"

# Extract just the filename of the reference (e.g., "ERR10710700.fasta")
# Use to compare inside the loop.
REF_FILENAME=$(basename "$REF_GENOME")

echo "Starting Snippy pipeline..."
echo "Reference: $REF_FILENAME"
echo "Input Folder: $GENOME_DIR"

SNIPPY_DIRS=()

# 2. Loop through every fasta file in the folder
for genome_file in "$GENOME_DIR"/*.fasta; do
  
  # Get the current file's name
  current_file=$(basename "$genome_file")

  # --- LOGIC CHECK ---
  if [ "$current_file" == "$REF_FILENAME" ]; then
      echo "Skipping reference genome ($current_file) to avoid self-mapping."
      continue
  fi
  # -------------------------------------------

  # Prepare output name
  sample_name=$(basename "$genome_file" .fasta)
  output_dir="$INTERMEDIATE_DIR/snippy_$sample_name"

  echo "Processing: $sample_name"

  # Run Snippy
  snippy --outdir "$output_dir" \
         --ref "$REF_GENOME" \
         --ctgs "$genome_file" \
         --cpus $CPUS_TO_USE \
         --ram $RAM_IN_GB \
         --force

  # Add to list
  SNIPPY_DIRS+=("$output_dir")
done

echo "------------------------------------------------"
echo "Individual runs complete. Starting Core Alignment..."

# 3. Run snippy-core
# Note: The reference is automatically included in the final alignment by snippy-core
snippy-core --outdir "$FINAL_OUTPUT_DIR" \
            --ref "$REF_GENOME" \
            "${SNIPPY_DIRS[@]}"

echo "------------------------------------------------"
echo "PIPELINE COMPLETE!"
echo "Final alignment: $FINAL_OUTPUT_DIR/core.aln"