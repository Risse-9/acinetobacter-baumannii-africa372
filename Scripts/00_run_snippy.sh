#!/bin/bash
# Description: Runs Snippy pipeline.
# FIX: Uses --prefix to direct output since --outdir is not supported.

set -e 

# --- CONFIGURATION ---
REF_GENOME="../data/fasta_372/ERR10710700.fasta"
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
REF_FILENAME=$(basename "$REF_GENOME")

echo "Starting Snippy pipeline..."
echo "Reference: $REF_FILENAME"

# 2. Loop through every fasta file
for genome_file in "$GENOME_DIR"/*.fasta; do
  
  current_file=$(basename "$genome_file")

  # Skip reference genome
  if [ "$current_file" == "$REF_FILENAME" ]; then
      continue
  fi

  sample_name=$(basename "$genome_file" .fasta)
  output_dir="$INTERMEDIATE_DIR/snippy_$sample_name"

  # Skip if already done
  if [ -f "$output_dir/snps.tab" ]; then
      echo "Skipping $sample_name (Already completed)"
      continue
  fi

  echo "Processing: $sample_name"

  # Run Snippy
  snippy --outdir "$output_dir" \
         --ref "$REF_GENOME" \
         --ctgs "$genome_file" \
         --cpus $CPUS_TO_USE \
         --ram $RAM_IN_GB \
         --force
done

echo "------------------------------------------------"
echo "Individual runs complete. Starting Core Alignment..."

# 3. Run snippy-core
# FIX: We use --prefix to specify the folder AND the filename start.
# This forces the files (core.aln, core.txt) to land in FINAL_OUTPUT_DIR.

snippy-core --prefix "$FINAL_OUTPUT_DIR/core" \
            --ref "$REF_GENOME" \
            "$INTERMEDIATE_DIR"/snippy_*

echo "------------------------------------------------"
echo "PIPELINE COMPLETE!"
echo "Final alignment: $FINAL_OUTPUT_DIR/core.aln"