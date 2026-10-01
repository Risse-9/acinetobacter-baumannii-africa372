"""Logistic regression of resistance gene carriage on ST group, adjusted for macro-region.

Usage: python Scripts/10_logistic_regression_hallmark_genes_362.py  (from the repository root)
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

import statsmodels.formula.api as smf

MODELS = [
    ('blaOXA-23', 'is_st2', 'ST85', 'results/logistic_blaOXA-23_362.csv'),
    ('armA', 'is_st2', 'ST85', 'results/logistic_armA_362.csv'),
    ('blaNDM-1', 'is_st85', None, 'results/logistic_blaNDM-1_362.csv'),
]


def fit(data, outcome, predictor, out_csv):
    model = smf.logit(f'Q("{outcome}") ~ {predictor} + C(macro_region)', data=data).fit()
    print(model.summary())

    if not model.mle_retvals['converged']:
        print(f'Model did not converge. {out_csv} not written.\n')
        return

    # conf_int() is on the log-odds scale, so both bounds are exponentiated
    table = np.exp(model.conf_int())
    table.columns = ['ci_lower', 'ci_upper']
    table.insert(0, 'adjusted_odds_ratio', np.exp(model.params))
    table['p_value'] = model.pvalues
    table = table.drop(index='Intercept')

    table.to_csv(out_csv)
    print(f'\n{table.to_string()}\nWritten to {out_csv}\n')


for outcome, predictor, drop_group, out_csv in MODELS:
    data = df if drop_group is None else df[df['st_group'] != drop_group]
    data = data.copy()
    data[predictor] = (data['st_group'] == predictor.replace('is_st', 'ST')).astype(int)
    print(f'\n{outcome} ~ {predictor} + C(macro_region)')
    fit(data, outcome, predictor, out_csv)