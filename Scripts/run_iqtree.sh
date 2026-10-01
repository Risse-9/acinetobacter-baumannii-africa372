#!/bin/bash
# Infers a maximum-likelihood phylogeny from a core SNP alignment using IQ-TREE.
#
# Usage: bash Scripts/run_iqtree.sh   (from the repository root, after 00_run_snippy.sh)

set -e

# --- Configuration ----------------------------------------------------------
ALIGNMENT="results/snippy_final_core_362/core.aln"
OUTPUT_PREFIX="results/iqtree_out_362/core_362"

# --- Checks -----------------------------------------------------------------
if [ ! -f "$ALIGNMENT" ]; then
  echo "ERROR: alignment not found: $ALIGNMENT (run 00_run_snippy.sh first)"
  exit 1
fi
command -v iqtree >/dev/null || { echo "ERROR: iqtree not found. Activate the conda environment."; exit 1; }

mkdir -p "$(dirname "$OUTPUT_PREFIX")"

echo "Alignment: $ALIGNMENT ($(grep -c '^>' "$ALIGNMENT") sequences)"
iqtree --version | head -1

# --- Tree -------------------------------------------------------------------
iqtree -s "$ALIGNMENT" \
       -pre "$OUTPUT_PREFIX" \
       -m GTR+ASC \
       -B 1000 \
       -T AUTO

echo
echo "Tree: ${OUTPUT_PREFIX}.treefile"
grep -m1 "IQ-TREE version" "${OUTPUT_PREFIX}.log"
grep -m1 "columns" "${OUTPUT_PREFIX}.log"