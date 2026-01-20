#!/bin/bash
# Rename Reference back to 'ERR10710700' and remove snippy prefix from sample names

# Input: The raw tree file from IQ-TREE
INPUT_TREE="../results/snippy_final_core/core.aln.treefile"
# Output: The clean tree file for Microreact
OUTPUT_TREE="../results/snippy_final_core/final_core.tre"


sed -e 's/Reference/ERR10710700/g' \
    -e 's/snippy_//g' \
    "$INPUT_TREE" > "$OUTPUT_TREE"

echo "Tree formatted successfully."