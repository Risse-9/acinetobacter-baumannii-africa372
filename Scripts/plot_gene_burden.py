# 09_plot_gene_burden.py
# Description: Calculates the 'Gene Burden' (Total Resistance Genes per Genome) and visualizes
# the dispersion using a histogram. Corresponds to Figure 4.1.

import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
INPUT_FILE = "../results/amr_results_wide_filtered.csv"
OUTPUT_IMAGE = "../results/figures/Figure_4_1_Gene_Burden.png"

# Ensure figure directory exists
os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

print(f"Loading {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)

# 1. Count genes per genome
# Excluding the 'Name' column to sum only the binary gene columns
df['Total_Genes'] = df.drop(columns=['Name']).sum(axis=1)

# 2. Calculate Statistics (Measures of Dispersion)
stats = {
    'Mean': df['Total_Genes'].mean(),
    'Standard Deviation (SD)': df['Total_Genes'].std(),
    'Minimum': df['Total_Genes'].min(),
    'Maximum': df['Total_Genes'].max(),
    'Median': df['Total_Genes'].median(),
    'IQR': df['Total_Genes'].quantile(0.75) - df['Total_Genes'].quantile(0.25)
}

print("Gene Burden Statistics:")
print(pd.DataFrame([stats]))

# 3. Generate Histogram
plt.figure(figsize=(10, 6))
plt.hist(df['Total_Genes'], bins=15, color='skyblue', edgecolor='black')
# plt.title('Distribution of Resistance Genes per Genome')
plt.xlabel('Number of Genes')
plt.ylabel('Number of Genomes')
plt.grid(axis='y', alpha=0.5)

# 4. Save
plt.savefig(OUTPUT_IMAGE, dpi=300)
print(f"Histogram saved to {OUTPUT_IMAGE}")