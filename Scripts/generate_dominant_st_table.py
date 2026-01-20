# 12_generate_dominant_st_table.py
# Description: Calculates the prevalence of Sequence Types (STs) per country.
# Identifies the dominant lineage and the proportion of unassigned STs.
# Corresponds to Table 4.7 in the thesis.

import pandas as pd
import os

# --- Configuration ---
INPUT_FILE = "../data/microreact_metadata_final_Copy.xlsx"
OUTPUT_FILE = "../results/Table_4_7_Dominant_STs.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

print(f"Loading metadata from {INPUT_FILE}...")
# Use pd.read_excel since the input is .xlsx
df = pd.read_excel(INPUT_FILE)

# 1. CLEANING COUNTRY NAMES
country_corrections = {
    'Tunisian': 'Tunisia',
    'Bostwana': 'Botswana',
    'Republic of Djibouti': 'Djibouti'
}
df['Country'] = df['Country'].replace(country_corrections)

# 2. FILTER FOR TOP 5 COUNTRIES
target_countries = ['Nigeria', 'Tunisia', 'Egypt', 'Botswana', 'Libya']
filtered_df = df[df['Country'].isin(target_countries)]

# 3. CALCULATE METRICS
results = []
print("Calculating dominant lineages...")

for country in target_countries:
    country_data = filtered_df[filtered_df['Country'] == country]
    total_isolates = len(country_data)
    
    # A. Calculate Unassigned
    # Treat '-', 'nan', and empty strings as unassigned
    unassigned_mask = country_data['ST'].astype(str).isin(['-', 'nan', ''])
    unassigned_count = unassigned_mask.sum()
    unassigned_pct = (unassigned_count / total_isolates) * 100 if total_isolates > 0 else 0
    unassigned_str = f"{unassigned_count} ({unassigned_pct:.1f}%)"
    
    # B. Calculate Most Frequent ST (Excluding Unassigned)
    valid_sts = country_data[~unassigned_mask]['ST'].astype(str)
    
    if not valid_sts.empty:
        dominant_st_name = valid_sts.value_counts().idxmax()
        dominant_count = valid_sts.value_counts().max()
        dominant_pct = (dominant_count / total_isolates) * 100
        
        # Format the separate columns
        dominant_st_val = f"ST{dominant_st_name}"
        dominant_freq_val = f"{dominant_count} ({dominant_pct:.1f}%)"
    else:
        dominant_st_val = "None"
        dominant_freq_val = "0 (0.0%)"
        
    results.append({
        'Country': country,
        'Total Isolates': total_isolates,
        'Dominant Lineage': dominant_st_val,
        'Prevalence (n (%))': dominant_freq_val,
        'Unassigned / Novel (n (%))': unassigned_str
    })

# 4. DISPLAY AND SAVE RESULT
result_table = pd.DataFrame(results)
print(result_table)

result_table.to_csv(OUTPUT_FILE, index=False)
print(f"Table saved to {OUTPUT_FILE}")