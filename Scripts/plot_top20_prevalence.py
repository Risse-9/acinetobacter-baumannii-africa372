# 10_plot_top20_prevalence.py
# Description: Calculates the prevalence of each AMR gene across the dataset and plots
# the Top 20 most frequent genes, colored by antibiotic class. 
# Corresponds to Figure 4.2 in the thesis.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Configuration ---
WIDE_FILE = "../results/amr_results_wide_filtered.csv"
RAW_AMR_FILE = "../results/merged_amrfinder.csv"
OUTPUT_IMAGE = "../results/figures/Figure_4_2_Top20_Prevalence.png"

os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

# 1. Load Data
print("Loading datasets...")
try:
    wide = pd.read_csv(WIDE_FILE, index_col=0)
    raw_amr = pd.read_csv(RAW_AMR_FILE, sep=',')
except FileNotFoundError as e:
    print(f"Error: Required file not found: {e.filename}")
    exit()

# Clean column names (remove potential leading/trailing spaces)
raw_amr.columns = raw_amr.columns.str.strip()

# 2. Calculate Prevalence
# Calculate the percentage of isolates carrying each gene
gene_prevalence = (wide.mean() * 100).sort_values(ascending=False).reset_index()
gene_prevalence.columns = ['Gene symbol', 'Prevalence (%)']

# 3. Map Genes to Classes
# Extract a unique mapping of Gene -> Class from the raw AMRFinder output
gene_map = raw_amr[['Gene symbol', 'Class']].drop_duplicates('Gene symbol')

# Merge prevalence data with class information
plot_df = pd.merge(gene_prevalence, gene_map, on='Gene symbol')

# Filter for the Top 20 genes
top_20_df = plot_df.head(20)

# 4. Plotting
print("Generating plot...")
plt.figure(figsize=(12, 10))
sns.set_style("whitegrid")

# Create horizontal bar plot
plot = sns.barplot(
    data=top_20_df, 
    x='Prevalence (%)', 
    y='Gene symbol', 
    hue='Class', 
    dodge=False, 
    palette='viridis'
)

# 5. Add Percentage Labels
for p in plot.patches:
    width = p.get_width()
    if width > 0: 
        plt.text(
            width + 1, 
            p.get_y() + p.get_height()/2, 
            f'{width:.1f}%', 
            va='center', fontsize=10
        )

# 6. Final formatting and saving
plt.xlabel('Prevalence (%)', fontsize=12)
plt.ylabel('Resistance Gene', fontsize=12)
plt.legend(title='Antibiotic Class', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

plt.savefig(OUTPUT_IMAGE, dpi=300)
print(f"Plot saved to {OUTPUT_IMAGE}")