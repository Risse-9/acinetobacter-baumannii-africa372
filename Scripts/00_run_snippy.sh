#!/bin/bash
# Runs Snippy against a reference for each genome in GENOME_DIR, then builds a
# core SNP alignment with snippy-core.
#
# Usage: bash Scripts/00_run_snippy.sh   (from the repository root)
#
# Completed samples are skipped, so the script can be re-run to resume.

set -e

# --- Configuration ----------------------------------------------------------
REF_GENOME="data/fasta_372/ERR10710700.fasta"
GENOME_DIR="data/fasta_372"

INTERMEDIATE_DIR="results/snippy_out_362"          # one directory per sample
FINAL_OUTPUT_DIR="results/snippy_final_core_362"   # combined alignment

CPUS_TO_USE=4
RAM_IN_GB=4

EXPECTED_SAMPLES=361

# Samples listed here are not aligned. Source: data/excluded_genomes.csv
EXCLUDE="
SRR28824822
ERR4783167
ERR4783385
ERR4783394
ERR4783413
ERR4783415
ERR4783417
ERR6938738
ERR7226588
SRR25445093
"

# --- Checks -----------------------------------------------------------------
if [ ! -f "$REF_GENOME" ]; then
  echo "ERROR: reference not found: $REF_GENOME (run from the repository root)"
  exit 1
fi
command -v snippy >/dev/null || { echo "ERROR: snippy not found. Activate the conda environment."; exit 1; }
command -v snippy-core >/dev/null || { echo "ERROR: snippy-core not found."; exit 1; }

mkdir -p "$INTERMEDIATE_DIR" "$FINAL_OUTPUT_DIR"
REF_FILENAME=$(basename "$REF_GENOME")

done_count=0
skipped_excluded=0

# --- Per-sample Snippy ------------------------------------------------------
for genome_file in "$GENOME_DIR"/*.fasta; do

  sample_name=$(basename "$genome_file" .fasta)

  # Skip the reference
  if [ "$(basename "$genome_file")" == "$REF_FILENAME" ]; then
    continue
  fi

  # Skip excluded samples
  if echo "$EXCLUDE" | grep -qw "$sample_name"; then
    echo "[excluded]  $sample_name"
    skipped_excluded=$((skipped_excluded + 1))
    continue
  fi

  output_dir="$INTERMEDIATE_DIR/snippy_$sample_name"

  # Skip samples completed on an earlier run
  if [ -f "$output_dir/snps.tab" ]; then
    echo "[done]      $sample_name"
    done_count=$((done_count + 1))
    continue
  fi

  echo "[running]   $sample_name"
  snippy --outdir "$output_dir" \
         --ref "$REF_GENOME" \
         --ctgs "$genome_file" \
         --cpus $CPUS_TO_USE \
         --ram $RAM_IN_GB \
         --force

  done_count=$((done_count + 1))
done

echo
echo "Processed: $done_count   Excluded: $skipped_excluded"

# --- Sample count -----------------------------------------------------------
# snippy-core uses whatever directories it is given; require the expected count.
actual=$(ls -d "$INTERMEDIATE_DIR"/snippy_* 2>/dev/null | wc -l)
if [ "$actual" -ne "$EXPECTED_SAMPLES" ]; then
  echo "ERROR: found $actual sample directories, expected $EXPECTED_SAMPLES. Not running snippy-core."
  exit 1
fi

# --- Core alignment ---------------------------------------------------------
echo "Running snippy-core on $actual samples..."
snippy-core --prefix "$FINAL_OUTPUT_DIR/core" \
            --ref "$REF_GENOME" \
            "$INTERMEDIATE_DIR"/snippy_*

echo
echo "Core alignment: $FINAL_OUTPUT_DIR/core.aln"
echo "Sequences (expect $((EXPECTED_SAMPLES + 1))): $(grep -c '^>' "$FINAL_OUTPUT_DIR/core.aln")"