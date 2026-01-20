# 11_plot_heatmap_by_country.py
# Description: Visualizes the geographic distribution of the Top 20 resistance genes
# using a heatmap. Prevalence is calculated per country.
# Corresponds to Figure 4.3 in the thesis.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Configuration ---
WIDE_FILE = "../results/amr_results_wide_filtered.csv"
# Note: Using the Excel file as specified in your setup
META_FILE = "../data/microreact_metadata_final_Copy.xlsx"
OUTPUT_IMAGE = "../results/figures/Figure_4_3_Country_Heatmap.png"

os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

# 1. Load Data
print("Loading data...")
try:
    wide = pd.read_csv(WIDE_FILE, index_col=0)
    # Use 'id' as index to match the wide matrix index
    meta = pd.read_excel(META_FILE, index_col='id')
except FileNotFoundError as e:
    print(f"Error: Required file not found: {e.filename}")
    exit()

# 2. Align and Merge
# Ensure we only use samples that exist in both datasets
common_samples = wide.index.intersection(meta.index)
combined_df = wide.loc[common_samples].copy()

# Add Country column to the gene matrix
combined_df['Country'] = meta.loc[common_samples, 'Country']

# 3. Calculate Prevalence per Country
print("Calculating prevalence by country...")
country_prevalence = combined_df.groupby('Country').mean() * 100

# Select Top 20 genes (based on overall global prevalence)
top_20_genes = wide.mean().sort_values(ascending=False).head(20).index
country_prevalence_top20 = country_prevalence[top_20_genes]

# 4. Plot Heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(country_prevalence_top20, 
            annot=False,         # Clean look without numbers in cells
            cmap="YlGnBu",       # Yellow to Blue gradient
            linewidths=.5, 
            cbar_kws={'label': 'Prevalence (%)'})

plt.xlabel('Resistance Gene', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig(OUTPUT_IMAGE, dpi=300)
print(f"Heatmap saved to {OUTPUT_IMAGE}")