# Genomic Epidemiology of *Acinetobacter baumannii* in Africa

This repository contains the bioinformatics pipeline, data processing scripts, and downstream analysis used to investigate the antimicrobial resistance (AMR) profiles and phylogenetic relationships of *Acinetobacter baumannii* genomes collected from across Africa.

The analysis dataset comprises **362 genomes**. An earlier version used 372; ten genomes were excluded following metadata and assembly-quality verification. See [CHANGELOG.md](CHANGELOG.md) for the list and the reason for each. The earlier state is preserved under the `v1` tag.

## Project Overview

The goal of this study is to characterize the genomic population structure of African *A. baumannii* isolates, identifying dominant Sequence Types (STs), analyzing the prevalence of resistance genes, and determining plasmid-borne resistance mechanisms.

**Key Analysis Steps:**

1. **Quality Control:** Assessment of raw reads (FastQC + MultiQC) and assembly quality (QUAST).
2. **Core SNP Alignment & Phylogeny:** Using Snippy and IQ-TREE.
3. **Genomic Typing:** MLST (Pasteur scheme) and Plasmid reconstruction (MOB-suite).
4. **AMR Analytics:** Statistical analysis of gene burden and resistance prevalence.
5. **Visualization:** Generating figures (heatmaps, stacked bar charts, histograms).

## Dataset and directory layout

The analysis uses 362 genomes.

* `data/metadata_clean_362.csv` — the analysis metadata: one row per genome, 26 metadata columns
  followed by resistance gene presence/absence.
* `data/excluded_genomes.csv` — the ten excluded genomes and the reason for each.
* `data/fasta_372/` — all 372 assemblies, including the ten excluded. Retained so that the earlier
  results remain reproducible.
* `data/362/` and `results/362/` — inputs and outputs for the 362-genome analysis.
* `results/` — outputs from the 372-genome version, kept unchanged.

`Scripts/11_filter_inputs_362.py` produces the contents of `data/362/` and the pipeline inputs in
`results/362/`. Run it before any other script.

---

## Repository Structure

* **`data/`**: Contains metadata, reference genomes, and intermediate mapping files.
  * *Note: Raw sequencing reads are excluded due to size constraints. The 372 assembled genome FASTA files (`data/fasta_372/`) are included.*


* **`results/`**: Output tables (CSV/Excel) and Figures (`.png`). The 362-genome outputs are in `results/362/`.
* **`Scripts/`**: All computational scripts.

---

## Installation & Dependencies

The analysis runs on a Linux/WSL environment using **Conda/Mamba**. You can recreate the necessary environments using the commands below.


```bash
# Phylogenetics (Snippy + IQ-TREE)
conda env create -f environment_phylo.yml

# Data analysis, statistics and plotting
conda env create -f environment_analysis.yml

# Typing (MLST)
conda create -n mlst_env -c bioconda -c conda-forge mlst

```

---

## Usage / Workflow

The scripts in the `Scripts/` folder.

### Phase 1: Quality Control & Bioinformatics Pipeline

* **Pre-processing:**
* **FastQC & MultiQC** were run on raw FASTQ reads to assess sequencing quality.
* **QUAST** was run on assembled FASTA genomes to assess assembly metrics (N50, Contigs).
* *Note: These outputs are processed in `generate_qc_stats.py`.*


* `00_run_snippy.sh`: Generates core SNP alignment against reference **ERR10710700**.
* `run_iqtree.sh`: Builds Maximum Likelihood tree (GTR+ASC model, 1000 bootstraps).
* `run_mlst.sh`: Assigns Sequence Types (Pasteur scheme).
* `clean_tree.sh`: Formats tree labels for Microreact visualization.

### Phase 2: Data Processing & Cleaning (Python/Bash)

*Note: AMRFinderPlus was run via the Galaxy web platform rather than locally,
which exports results under long filenames tied to Galaxy's internal history
IDs rather than sample accessions. `01`–`03` convert that into a clean,
mergeable dataset: `01` maps each file to its real sample accession using
`data/mapping.csv`, `02` shortens filenames to a standard format, and `03`
merges everything into one CSV.*

Cleaning raw reports and integrating MOB-suite plasmid data.

* `01_rename_amr_files.sh` - `03_merge_reports.sh`: Prepares raw AMR data.
* `04_filter_amr_matrix.py`: Creates the binary gene presence/absence matrix.
* `05_merge_mob_report.py`: Aggregates plasmid clustering results.
* `06_link_amr_to_location.py`: Determines if genes are chromosomal or plasmid-borne.
* `07_summarise_location.py`: Produces the gene location summary table.

### Phase 3: Statistical Analysis & Visualization (Python)

Generates the final tables and figures.

* **362-genome inputs:**
* `11_filter_inputs_362.py`: writes 362-genome versions of the pipeline input files. Run before the scripts below.

* **Quality Control Summary:** `generate_qc_stats.py` (Table 4.1 - Integrates FastQC/QUAST data).
* **Figures:**
* `plot_gene_burden.py` (Figure 4.1: Histogram of resistance genes).
* `plot_top20_prevalence.py` (Figure 4.2: Bar chart of common genes).
* `plot_heatmap_by_country.py` (Figure 4.3: Geographic heatmap).
* `plot_st_distr.py` (Figure 4.4: Stacked bar chart of STs).
* `plot_faceted_source.py` (Figure 4.5: Isolation source analysis).


* **Tables:**
* `generate_dominant_st_table.py` (Table 4.7).
* `generate_st_prevalence_table.py` (Table 4.4).
* `gen_plasmid_table.py` (Table 4.5).
* `generate_appendix_table.py` (Appendix 1: per-isolate metadata and resistance genes).


* **Statistical tests:**
* `08_fisher_tests_362.py`: Fisher's exact tests of ST lineage against resistance gene carriage.
* `09_kruskal_wallis_resistome_burden_362.py`: resistance gene count compared across ST groups.
* `10_logistic_regression_hallmark_genes_362.py`: logistic regression adjusted for macro-region.

---

## Key Results

* **Phylogeny:** High-resolution core SNP tree revealing the population structure of African isolates.
* **Resistance Burden:** Analysis of the Gene Burden across different STs.
* **Plasmid Association:** Detailed breakdown of chromosomal vs. plasmid location for genes.

## License

This project is for academic research purposes.

---

## Data Availability

Raw sequencing reads are publicly available from the NCBI Sequence Read Archive (SRA) and European Nucleotide Archive (ENA) under the run accessions listed in `data/metadata_clean_362.csv` (`run_accession` column). Reads are not redistributed here; they can be retrieved using each accession via the SRA/ENA browser, the SRA Toolkit (`prefetch` / `fasterq-dump`), or the ENA Portal API.

Assembled draft genomes (post-QC, FASTA) are included under `data/fasta_372/`. This directory holds all 372 assemblies, including the ten excluded from the analysis dataset.

---

## Software & References

The following bioinformatics tools and platforms were used in this analysis. Please refer to their official documentation for detailed usage instructions.

* **Snippy:** Core genome alignment and SNP calling.
* [https://github.com/tseemann/snippy](https://github.com/tseemann/snippy)


* **IQ-TREE 3:** Maximum Likelihood phylogenetics.
* [http://www.iqtree.org/](http://www.iqtree.org/)


* **MLST:** Multi-Locus Sequence Typing (Pasteur scheme).
* [https://github.com/tseemann/mlst](https://github.com/tseemann/mlst)


* **MOB-suite:** Plasmid reconstruction and typing.
* [https://github.com/phac-nml/mob-suite](https://github.com/phac-nml/mob-suite)


* **AMRFinderPlus:** Identification of antimicrobial resistance genes.
* [https://github.com/ncbi/amr](https://github.com/ncbi/amr)


* **PathogenWatch:** Genomic assembly and surveillance.
* [https://pathogen.watch/](https://pathogen.watch/)


* **Galaxy Platform:** Web-based platform used for running AMRFinderPlus.
* [https://usegalaxy.org/](https://usegalaxy.org/)


* **Microreact:** Phylogeographic visualization.
* [https://microreact.org/](https://microreact.org/)


* **Quality Control:**
* **FastQC:** [https://www.bioinformatics.babraham.ac.uk/projects/fastqc/](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
* **MultiQC:** [https://multiqc.info/](https://multiqc.info/)
* **QUAST:** [https://quast.sourceforge.net/](https://quast.sourceforge.net/)



---
