# Changelog

All notable changes to this repository are recorded here.

## [v2.0] — 362-genome dataset

Prepared for manuscript submission. The previous state is preserved under the `thesis-v1` tag, and its
outputs remain in place unchanged.

### Changed

- **Dataset reduced from 372 to 362 genomes** after a verification pass over every accession's
  archive metadata and assembly statistics. See *Removed*.
- **Core SNP alignment rebuilt.** `snippy-core` retains only positions called in every sample, so
  the alignment is a property of the sample set and cannot be corrected by deleting sequences from
  it. It was regenerated from the 362 genomes.

  | | 372 genomes | 362 genomes |
  |---|---|---|
  | Alignment columns | 55,522 | 117,452 |
  | Parsimony-informative sites | 41,914 | 96,820 |

- **Phylogeny rebuilt** with IQ-TREE 3 v3.1.2 (GTR+ASC, 1,000 ultrafast bootstrap replicates).
  Of 359 internal nodes, 229 (63.8%) have ≥95% support and 251 (69.9%) ≥70%.
- **All tables and figures regenerated** from the 362-genome dataset. Outputs are written to
  `results/362/` and keep their original filenames; the 372-genome outputs remain in `results/`.
- **Distinct resistance genes detected falls from 140 to 133.** Seven genes were carried only by
  excluded genomes: `blaADC-150`, `blaI`, `blaR1`, `blaZ`, `dfrA40`, `dfrS1`, `fosB`.
- **Assembly quality range narrowed.** Genome size now 3.44–4.31 Mbp (was 3.44–7.95) and GC content
  38.70–39.80% (was 36.14–43.76).
- **Metadata consolidated** into `data/metadata_clean_362.csv`: country names corrected,
  macro-region added as a column, sequence types stored as numbers with blanks where unassigned.
- **Installation instructions corrected.** Environment names now match those in use, and `scipy`
  and `statsmodels` added — the statistics scripts cannot run without them.
- **IQ-TREE reference updated** from IQ-TREE 2 to IQ-TREE 3.

### Added

- `Scripts/08_fisher_tests_362.py` — Fisher's exact tests of lineage against gene carriage.
- `Scripts/09_kruskal_wallis_resistome_burden_362.py` — resistance gene count across ST groups.
- `Scripts/10_logistic_regression_hallmark_genes_362.py` — logistic regression adjusted for
  macro-region.
- `Scripts/11_filter_inputs_362.py` — writes 362-genome versions of the pipeline input files.
- `data/excluded_genomes.csv` — the ten excluded genomes with a reason for each.
- `data/metadata_clean_362.csv` — the analysis metadata file.
- `environment_phylo.yml`, `environment_analysis.yml` — conda environment definitions.
- `SCRIPTS_DOCUMENTATION.md` — what each script produces and how to read its output.

### Removed

- `Scripts/count_percent_full.ipynb` — duplicated `generate_st_prevalence_table.py` without its
  sequence-type filter.

Ten genomes were excluded from the analysis. Their assemblies remain in `data/fasta_372/`, which is
unchanged.

| Accession | Reason |
|---|---|
| SRR28824822 | Collected in Viet Nam; outside the study region |
| ERR4783167, ERR4783385, ERR4783394, ERR4783413, ERR4783415, ERR4783417, ERR6938738, ERR7226588, SRR25445093 | Assembly length or GC content outside the range expected for *A. baumannii*, indicating contamination |

### Notes

- `data/fasta_372/` retains all 372 assemblies. The directory name refers to its contents, not to
  the analysis dataset.
- Results in `results/` without a `362/` path were generated from the 372-genome dataset and
  correspond to the `v1` tag.
- FastQC and MultiQC outputs cover one genome (`ERR6938737`) that was never assembled or included
  in the dataset. It is removed by `Scripts/11_filter_inputs_362.py`.

## [thesis-v1.0] — 372-genome dataset

The state of the repository as originally submitted.
