"""Fisher's exact tests of ST lineage against resistance gene carriage.

Usage: python Scripts/08_fisher_tests_362.py  (from the repository root)
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
from scipy.stats.contingency import odds_ratio as cond_odds_ratio

OUT = 'results/fisher_test_results_362.csv'

COMPARISONS = [
    ('ST2', 'blaOXA-23'),
    ('ST2', 'armA'),
    ('ST85', 'blaNDM-1'),
]


def run_fisher(data, group_val, gene_col):
    in_group = (data['st_group'] == group_val).astype(int)

    # reindex keeps the table 2x2 when a level is absent
    table = (pd.crosstab(in_group, data[gene_col])
               .reindex(index=[0, 1], columns=[0, 1], fill_value=0))

    _, p_value = stats.fisher_exact(table.values)
    res = cond_odds_ratio(table.values)
    lo, hi = res.confidence_interval(confidence_level=0.95)

    print(f'\n{group_val} vs {gene_col}')
    print(table.to_string())
    print(f'OR {res.statistic:.2f} (95% CI {lo:.2f}-{hi:.2f}), p = {p_value:.4e}')

    return {
        'st_group': group_val,
        'gene': gene_col,
        'other_absent': table.loc[0, 0],
        'other_present': table.loc[0, 1],
        'target_absent': table.loc[1, 0],
        'target_present': table.loc[1, 1],
        'odds_ratio': res.statistic,
        'ci_lower': lo,
        'ci_upper': hi,
        'p_value': p_value,
    }


results = pd.DataFrame([run_fisher(df, g, c) for g, c in COMPARISONS])
results['bonferroni_threshold'] = 0.05 / len(results)

results.to_csv(OUT, index=False)
print(f'\nWritten to {OUT}')