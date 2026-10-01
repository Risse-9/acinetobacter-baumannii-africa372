"""Writes 362-genome versions of the pipeline input files by removing the
accessions listed in data/excluded_genomes.csv.

Each output keeps the schema of its source file. Outputs are written to
results/362/ and data/362/. Source files are not modified.

The wide gene matrix is not produced here. It is rebuilt from
results/merged_amrfinder_362.csv by 04_filter_amr_matrix.py, which drops genes
that no remaining genome carries.

Usage: python Scripts/11_filter_inputs_362.py   (from the repository root)
"""

import os

import pandas as pd

EXCLUDED = 'data/excluded_genomes.csv'
ANALYSIS_SET = 'data/metadata_clean_362.csv'
N_EXPECTED = 362

# (source, output, identifier column, reader)
TABLES = [
    ('data/microreact_metadata_final_Copy.xlsx',
     'data/362/microreact_metadata.xlsx', 'id', 'excel'),
    ('results/merged_amrfinder.csv',
     'results/362/merged_amrfinder.csv', 'Name', 'csv'),
    ('results/amr_plus_mob_merged.csv',
     'results/362/amr_plus_mob_merged.csv', 'Name', 'csv'),
    ('results/master_mob_report.csv',
     'results/362/master_mob_report.csv', 'sample_id', 'csv'),
    ('results/amr_location_summary.csv',
     'results/362/amr_location_summary.csv', 'Name', 'csv'),
    ('results/quast_results/transposed_report.tsv',
     'results/362/transposed_report.tsv', 'Assembly', 'tsv'),
]

# MultiQC reports one row per read file, named <accession>_1 and <accession>_2. Its
# accession set is not identical to the analysis set, so rows are selected by
# membership of the analysis set rather than by removing the excluded list.
MULTIQC = [
    ('results/multiqc/multiqc_data/multiqc_general_stats.txt',
     'results/362/multiqc_general_stats.txt'),
    ('results/multiqc/multiqc_data/fastqc_per_sequence_quality_scores_plot.txt',
     'results/362/fastqc_per_sequence_quality_scores_plot.txt'),
]

for folder in ('data/362', 'results/362'):
    os.makedirs(folder, exist_ok=True)

excluded = set(pd.read_csv(EXCLUDED).iloc[:, 0].astype(str))
analysis_set = set(pd.read_csv(ANALYSIS_SET)['run_accession'].astype(str))
print(f'{len(excluded)} accessions excluded, {len(analysis_set)} in the analysis set')

for src, out, id_col, kind in TABLES:
    if kind == 'excel':
        df = pd.read_excel(src)
    elif kind == 'tsv':
        df = pd.read_csv(src, sep='\t', low_memory=False)
    else:
        df = pd.read_csv(src, low_memory=False)

    kept = df[~df[id_col].astype(str).isin(excluded)]

    n_before = df[id_col].nunique()
    n_after = kept[id_col].nunique()
    assert n_after == N_EXPECTED, f'{src}: {n_after} accessions after filtering, expected {N_EXPECTED}'

    if out.endswith('.xlsx'):
        kept.to_excel(out, index=False)
    elif out.endswith('.tsv'):
        kept.to_csv(out, sep='\t', index=False)
    else:
        kept.to_csv(out, index=False)

    print(f'{out}  rows {len(df)} -> {len(kept)}  accessions {n_before} -> {n_after}')

for src, out in MULTIQC:
    df = pd.read_csv(src, sep='\t')
    id_col = df.columns[0]
    accession = df[id_col].astype(str).str.rsplit('_', n=1).str[0]

    keep = accession.isin(analysis_set)
    kept = df[keep]

    n_after = accession[keep].nunique()
    missing = sorted(analysis_set - set(accession))
    extra = sorted(set(accession) - analysis_set - excluded)

    kept.to_csv(out, sep='\t', index=False)
    print(f'{out}  rows {len(df)} -> {len(kept)}  accessions {n_after} of {N_EXPECTED}')
    if missing:
        print(f'  not present in this report: {", ".join(missing)}')
    if extra:
        print(f'  present but not in the analysis set, removed: {", ".join(extra)}')