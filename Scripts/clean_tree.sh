#!/bin/bash
# Description: Removes 'snippy_' prefixes from the IQ-TREE output 
# to make labels clean for Microreact (e.g., "snippy_SRR123" -> "SRR123").

set -e

# --- CONFIGURATION ---
INPUT_TREE="../results/iqtree_out/final_core.treefile"
OUTPUT_TREE="../results/iqtree_out/final_core.tre"

# 1. Check if file exists
if [ ! -f "$INPUT_TREE" ]; then
    echo "Error: Cannot find tree file at $INPUT_TREE"
    exit 1
fi

echo "Cleaning tree labels..."

# 2. Rename Reference and remove snippy_ prefix
sed -e 's/Reference/ERR10710700/g' \
    -e 's/snippy_//g' \
    "$INPUT_TREE" > "$OUTPUT_TREE"

echo "------------------------------------------------"
echo "Success! Clean tree saved to:"
echo "$OUTPUT_TREE"
echo "------------------------------------------------"