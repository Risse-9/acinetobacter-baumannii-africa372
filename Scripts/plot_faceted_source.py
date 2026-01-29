# 14_plot_faceted_source_st_bold.py
# Description: Creates a faceted bar chart showing Sequence Type (ST) distribution
# separated by Isolation Source with BOLD AXIS TEXT and MEGA LEGEND.
# Corresponds to Figure 4.5 in the thesis.

import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
INPUT_FILE = "data/microreact_metadata_final_Copy.xlsx"
OUTPUT_IMAGE = "results/figures/Figure_4_5_Faceted_ST_By_Source.png"

os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

# 1. LOAD DATA
print(f"Loading metadata from {INPUT_FILE}...")
meta = pd.read_excel(INPUT_FILE, index_col='id')

# 2. BASIC CLEANING
meta = meta.dropna(subset=['Country', 'ST'])
meta['Country'] = meta['Country'].str.strip()
meta['Isolation source'] = meta['Isolation source'].str.lower().str.strip()
meta['Isolation source'] = meta['Isolation source'].fillna('unknown')
meta['ST'] = pd.to_numeric(meta['ST'], errors='coerce')
meta = meta.dropna(subset=['ST'])
meta['ST'] = meta['ST'].astype(int)

# 3. ISOLATION SOURCE MAPPING
source_map = {
    # PATIENT SAMPLES
    'blood': 'blood', 'cvp blood': 'blood', 'cerebrospinal fluid (csf)': 'csf',
    'urine': 'urine',
    'wound': 'wound', 'surgical wound': 'wound', 'surgical site infection': 'wound', 'w/s': 'wound',
    'respiratory': 'respiratory', 'respiratory tract': 'respiratory', 'bal': 'respiratory',
    'protected specimen brushing (psb)': 'respiratory', 'throat/s': 'respiratory',
    'pleural aspirate': 'respiratory', 'pleural': 'respiratory',

    # MEDICAL DEVICES / EQUIPMENT
    'endotracheal tube': 'clinical device', 'syringe driver': 'clinical device',
    'dial device': 'clinical device', 'respiratory assistance device': 'clinical device',
    'defibrilator': 'clinical device', 'ecg device': 'clinical device',
    'iv pole': 'clinical device', 'stethoscope': 'clinical device',

    # HOSPITAL ENVIRONMENT
    'hospital surface': 'environmental', 'environmental swab': 'environmental',
    'hospital wastewater': 'environmental', 'sink basin': 'environmental',
    'sink plumbing trap': 'environmental', 'bed': 'environmental',
    'care cart': 'environmental', 'refrigerator handle': 'environmental',
    'soap dispenser': 'environmental', 'disinfectant dispenser': 'environmental',
    'furniture surface': 'environmental',

    # SCREENING
    'screening swab': 'screening/personnel', 'hand swab': 'screening/personnel',
    'medical personnel': 'screening/personnel', 'paramedical personnel': 'screening/personnel',

    # UNKNOWN / UNSPECIFIED
    'patient': 'unknown', 'unknown': 'unknown'
}

meta['Isolation source'] = meta['Isolation source'].replace(source_map)

# 4. FIXED FACET CATEGORIES
priority_sources = [
    'blood', 'respiratory', 'wound',
    'clinical device', 'environmental', 'unknown'
]
meta = meta[meta['Isolation source'].isin(priority_sources)]

# 5. GLOBAL COUNTRY + ST SELECTION
global_country_counts = meta['Country'].value_counts()
top_countries = global_country_counts[global_country_counts >= 5].nlargest(5).index
top_st_global = meta['ST'].value_counts().nlargest(10).index

# 6. FACET PLOTTING
print("Generating faceted plot...")
sources = priority_sources
ncols = 2
nrows = (len(sources) + 1) // ncols

# Wide figure
fig, axes = plt.subplots(nrows, ncols, figsize=(24, 11 * nrows), sharey=True)
axes = axes.flatten()

# We need to capture handles for the legend from a valid plot
legend_handles = None
legend_labels = None

for ax, source in zip(axes, sources):
    subset = meta[meta['Isolation source'] == source]
    st_counts = pd.crosstab(subset['Country'], subset['ST'])
    country_totals = st_counts.sum(axis=1)

    # Force consistent countries
    st_counts = st_counts.reindex(top_countries, fill_value=0)
    country_totals = country_totals.reindex(top_countries, fill_value=0)

    if st_counts.sum().sum() == 0:
        ax.set_visible(False)
        continue

    labels = {country: f"{country}\n(n={int(country_totals[country])})"
              for country in top_countries}

    # Force consistent STs
    plot_data = st_counts.reindex(columns=top_st_global, fill_value=0)
    plot_data['Others'] = st_counts.drop(columns=top_st_global, errors='ignore').sum(axis=1)

    # Convert to percentage
    plot_data_pct = plot_data.div(plot_data.sum(axis=1), axis=0) * 100
    plot_data_pct.index = [labels[c] for c in plot_data_pct.index]

    plot_data_pct.plot(
        kind='bar', stacked=True, ax=ax, colormap='tab20',
        width=0.8, legend=False
    )

    # Capture handles/labels from the first successful plot
    if legend_handles is None:
        legend_handles, legend_labels = ax.get_legend_handles_labels()

    # --- STYLE UPDATES (BOLD EVERYWHERE) ---
    n_source = subset.shape[0]
    ax.set_title(f"{source.capitalize()} (n={n_source})", fontsize=20, fontweight='bold')
    
    ax.set_ylabel('Percentage (%)', fontsize=18, fontweight='bold')
    ax.set_xlabel('')
    
    # 1. BOLD X-AXIS LABELS (Countries)
    ax.set_xticklabels(
        plot_data_pct.index, 
        rotation=45, 
        ha='right', 
        rotation_mode='anchor', 
        fontsize=16, 
        fontweight='bold'  # <--- BOLD ADDED HERE
    )

    # 2. BOLD Y-AXIS TICKS (Numbers)
    # We have to iterate to force them bold
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    ax.tick_params(axis='y', labelsize=16)
    
    ax.set_ylim(0, 100)
    ax.axhline(50, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.2)

# Hide unused axes
for i in range(len(sources), len(axes)):
    axes[i].set_visible(False)

# 7. GLOBAL LEGEND FIX (MEGA SIZE)
if legend_handles:
    fig.legend(
        legend_handles, legend_labels, 
        title='Pasteur ST',
        bbox_to_anchor=(0.99, 0.5), 
        loc='center right',         
        fontsize=22,           
        title_fontsize=24,     
        markerscale=3.0        
    )

# --- LAYOUT ADJUSTMENT ---
plt.tight_layout(rect=[0, 0, 0.78, 1]) 

plt.savefig(OUTPUT_IMAGE, dpi=300) 
print(f"Faceted plot saved to {OUTPUT_IMAGE}")