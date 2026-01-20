#!/bin/bash
# Description: Generates a Maximum Likelihood tree from Snippy core alignment.
# Tool: IQ-TREE
# Model: GTR+ASC (Standard for SNP-only alignments)
# Bootstrap: 1000 Ultrafast Bootstraps

set -e

INPUT_ALIGNMENT="../results/snippy_final_core/core.aln"
OUTPUT_DIR="../results/iqtree_out"
OUTPUT_PREFIX="final_core"

# --- RESOURCES ---
# 'AUTO' allows IQ-TREE to choose the best number of CPU cores automatically
THREADS="AUTO"

# 1. Setup Output Directory
mkdir -p "$OUTPUT_DIR"

echo "------------------------------------------------"
echo "Starting IQ-TREE Phylogeny Pipeline"
echo "Input Alignment: $INPUT_ALIGNMENT"
echo "Output Directory: $OUTPUT_DIR"
echo "------------------------------------------------"

# 2. Check if alignment exists before starting
if [ ! -f "$INPUT_ALIGNMENT" ]; then
    echo "ERROR: Could not find $INPUT_ALIGNMENT"
    echo "Please wait for snippy-core to finish running!"
    exit 1
fi

# 3. Run IQ-TREE
# -s  : Input alignment
# -m  : Model (GTR+ASC is crucial for SNP data)
# -B  : 1000 Ultrafast bootstraps (standard for high reliability)
# -T  : Threads (CPU cores)
# -pre: Output prefix (folder/filename_start)

iqtree -s "$INPUT_ALIGNMENT" \
        -pre "$OUTPUT_DIR/$OUTPUT_PREFIX" \
        -m GTR+ASC \
        -B 1000 \
        -T $THREADS

echo "------------------------------------------------"
echo "TREE GENERATION COMPLETE!"
echo "Newick Tree file: $OUTPUT_DIR/${OUTPUT_PREFIX}.treefile"
echo "------------------------------------------------"