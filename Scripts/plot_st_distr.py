# 13_plot_st_distribution.py
# Description:Visualizes the distribution of Pasteur Sequence Types (STs) across different countries.
# Countries with fewer than 5 isolates are filtered out.
# Corresponds to Figure 4.4 in the thesis.

import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
INPUT_FILE = "../data/microreact_metadata_final_Copy.xlsx"
OUTPUT_IMAGE = "../results/figures/Figure_4_4_ST_Distribution.png"

os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

# 1. LOAD DATA
print(f"Loading metadata from {INPUT_FILE}...")
meta = pd.read_excel(INPUT_FILE, index_col='id')

# 2. CALCULATE COUNTS AND PERCENTAGES
# Get raw counts of ST per country
st_counts = pd.crosstab(meta['Country'], meta['ST'])

# Get total n for each country to add to the labels
country_totals = st_counts.sum(axis=1)

# --- FILTER COUNTRIES WITH N < 5 ---
# Only keep countries where the total count is 5 or more
countries_to_keep = country_totals[country_totals >= 5].index
st_counts = st_counts.loc[countries_to_keep]
country_totals = country_totals.loc[countries_to_keep]

# Create labels: "Country Name (n=X)"
new_labels = {country: f"{country}\n(n={int(total)})" 
              for country, total in country_totals.items()}

# 3. ORGANIZE PLOT DATA
# Sort countries by total size (largest n first)
sorted_countries = country_totals.sort_values(ascending=False).index
st_counts = st_counts.loc[sorted_countries]

# Identify Top STs across the whole study to keep legend clean
# Selecting top 10 most frequent STs
top_st_names = st_counts.sum(axis=0).sort_values(ascending=False).head(10).index
plot_data = st_counts[top_st_names].copy()
plot_data['Others'] = st_counts.drop(columns=top_st_names).sum(axis=1)

# Convert to percentage for the stacked bar view
plot_data_pct = plot_data.div(plot_data.sum(axis=1), axis=0) * 100

# Rename the index with our "n=X" labels
plot_data_pct.index = [new_labels[c] for c in plot_data_pct.index]

# 4. PLOT
print("Generating stacked bar chart...")
ax = plot_data_pct.plot(kind='bar', 
                        stacked=True, 
                        figsize=(16, 8), 
                        colormap='tab20c', 
                        width=0.8)

# 5. FORMATTING
plt.ylabel('Percentage of Isolates (%)', fontsize=12)
plt.xlabel('Country of Origin (Sample Size)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Pasteur ST', bbox_to_anchor=(1.02, 1), loc='upper left')

# Add a horizontal line at 50% for visual guide
plt.axhline(y=50, color='gray', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_IMAGE, dpi=300)
print(f"Plot saved to {OUTPUT_IMAGE}")