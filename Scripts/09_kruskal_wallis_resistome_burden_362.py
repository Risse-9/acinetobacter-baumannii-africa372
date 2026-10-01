"""Kruskal-Wallis test of resistance gene count across ST groups.

Usage: python Scripts/09_kruskal_wallis_resistome_burden_362.py  (from the repository root)
"""

import pandas as pd
import numpy as np

DATA = 'data/metadata_clean_362.csv'

METADATA_COLS = [
    'run_accession', 'biosample_accession', 'bioproject_accession', 'country',
    'macro_region', 'city_region', 'latitude', 'longitude', 'collection_date',
    'collection_year', 'isolation_source', 'source_category', 'host',
    'host_disease', 'study_title', 'center_name', 'species_name',
    'mash_reference_id', 'matching_hashes', 'mash_distance', 'st_original',
    'assembly_length', 'contigs', 'n50', 'gc_percent', 'st_oxford',
]
N_EXPECTED = 362
MAJOR_STS = (1, 2, 85)

df = pd.read_csv(DATA)

assert len(df) == N_EXPECTED, f'Expected {N_EXPECTED} rows, found {len(df)}'
assert list(df.columns[:len(METADATA_COLS)]) == METADATA_COLS, 'Unexpected metadata columns'

# Columns after the metadata block are gene presence/absence.
gene_cols = df.columns[len(METADATA_COLS):].tolist()
genes = df[gene_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
df = pd.concat([df[METADATA_COLS], genes], axis=1)


def group_st(value):
    if pd.isna(value):
        return 'Unassigned'
    return f'ST{int(value)}' if int(value) in MAJOR_STS else 'Other STs'


# Int64 keeps ST values as integers and blanks as NA.
df['st_group'] = df['st_original'].astype('Int64').apply(group_st)

assert df['macro_region'].notna().all(), 'macro_region contains blanks'

import scipy.stats as stats

OUT = 'results/resistome_burden_summary_362.csv'

df['total_amr_genes'] = df[gene_cols].sum(axis=1)

summary = (df.groupby('st_group')['total_amr_genes']
             .agg(count='count', median='median',
                  q25=lambda x: x.quantile(0.25),
                  q75=lambda x: x.quantile(0.75),
                  mean='mean', std='std')
             .reset_index())

groups = [g['total_amr_genes'].values for _, g in df.groupby('st_group')]
h_stat, p_val = stats.kruskal(*groups)

print(summary.to_string(index=False))
print(f'\nKruskal-Wallis H = {h_stat:.2f}, p = {p_val:.4e}')

summary.to_csv(OUT, index=False)
print(f'Written to {OUT}')