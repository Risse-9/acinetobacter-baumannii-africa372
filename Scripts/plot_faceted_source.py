# 14_plot_faceted_source_st.py
# Description: Creates a faceted bar chart showing Sequence Type (ST) distribution
# separated by Isolation Source (e.g., Blood, Respiratory, Wound).
# Corresponds to Figure 4.5 in the thesis.

import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
INPUT_FILE = "../data/microreact_metadata_final_Copy.xlsx"
OUTPUT_IMAGE = "../results/figures/Figure_4_5_Faceted_ST_By_Source.png"

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
# Standardizing diverse source names into broad categories
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
# Define consistent categories for all facets
global_country_counts = meta['Country'].value_counts()
top_countries = global_country_counts[global_country_counts >= 5].nlargest(5).index
top_st_global = meta['ST'].value_counts().nlargest(10).index

# 6. FACET PLOTTING
print("Generating faceted plot...")
sources = priority_sources
ncols = 2
nrows = (len(sources) + 1) // ncols

fig, axes = plt.subplots(nrows, ncols, figsize=(18, 6 * nrows), sharey=True)
axes = axes.flatten()

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

    # Formatting
    ax.set_xticklabels(plot_data_pct.index, rotation=45, ha='right', rotation_mode='anchor', fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    n_source = subset.shape[0]
    ax.set_title(f"{source.capitalize()} (n={n_source})", fontsize=14, fontweight='bold')
    ax.set_ylabel('Percentage (%)')
    ax.set_xlabel('')
    ax.set_ylim(0, 100)
    ax.axhline(50, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.2)

# 7. GLOBAL LEGEND FIX
for a in axes:
    handles, labels = a.get_legend_handles_labels()
    if handles:
        break

fig.legend(
    handles, labels, title='Pasteur ST',
    bbox_to_anchor=(1.02, 0.5), loc='center left',
    fontsize=14, title_fontsize=16, markerscale=2.0
)

plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.savefig(OUTPUT_IMAGE, dpi=300)
print(f"Faceted plot saved to {OUTPUT_IMAGE}")