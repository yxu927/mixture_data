# mixture_data

Companion data archive for the manuscript:

> A hierarchical clock-mixture model for Bayesian phylogenetic dating

This repository contains analysis-ready empirical alignments, BEAST XML
configuration files, LinguaPhylo simulation inputs, processed MCMC outputs, and
posterior summaries for the hierarchical clock-mixture study.

## Files in this archive

- `README_mixture_data.md` - this file.
- `real.zip` - the `real/` directory: the four empirical benchmark datasets
  (alignments and BEAST XML).
- `simulation_short.zip` - the `simulation/short/` directory.
- `simulation_long.zip` - the `simulation/long/` directory.


## Layout

- `real/D4/` - DENV-4 serially sampled benchmark.
- `real/RSV2/` - RSV-A G-gene benchmark.
- `real/H3N2/` - H3N2 structured-coalescent subset.
- `real/rbcl/` - 31-taxon chloroplast rbcL historical benchmark.
- `simulation/short/` - lower-information simulation condition:
  `nchar = 600`, `clockRate ~ LogNormal(meanlog=-5, sdlog=0.5)`.
- `simulation/long/` - main simulation condition:
  `nchar = 1500`, `clockRate ~ LogNormal(meanlog=-3.4, sdlog=0.5)`.
- `analysis_scripts/` - not included in this Dryad archive; the post-processing
  and figure scripts are on the linked Zenodo deposit (see Contents and
  Licensing above).

Each simulation condition contains:

- `lphy_scripts/` - LinguaPhylo simulation scripts for the strict, UCLN, and
  autocorrelated generating strata.
- `{strict,ucln,auto}/data/data.zip` - 100 replicate input bundles per stratum:
  simulated alignments, true tree files, true-value logs, and generated BEAST
  XML files.
- `{strict,ucln,auto}/beast/beast.zip` - BEAST MCMC trace outputs for the 100
  replicates in that stratum.
- `{strict,ucln,auto}/stats/stats.zip` - posterior-summary tables generated
  from the BEAST trace outputs.
- `{strict,ucln,auto}/figures/` - coverage and recovery figures generated from
  the corresponding `data/` and `stats/` files.

## How to Reproduce

The archived files are intended to make the reported analyses reproducible
without relying on local absolute paths.

1. Install the RelaxClockAveraging software release from Zenodo
   (`10.5281/zenodo.20684860`) or the matching GitHub release.
2. For simulation inputs, start from
   `simulation/{short,long}/lphy_scripts/*.lphy`.
3. Convert each LPhy script to BEAST XML using the RelaxClockAveraging
   LPhy/LPhyBEAST workflow, or use the generated XML files already stored in
   each `data.zip`.
4. Run the BEAST XML files to produce `.log` and `.trees` outputs.


Example after extracting the zip files inside one simulation stratum:

```bash
python analysis_scripts/calc_tree_stats.py simulation/short/auto
python analysis_scripts/plot_parameter_coverage.py simulation/short/auto
python analysis_scripts/plot_model_recovery.py simulation/short
```

The scripts use paths relative to the supplied simulation folder and write
outputs under its `figures/` directory by default.

## Software Versions

The empirical XML files archived here were run under the analysis environment
used for the manuscript, primarily BEAST 2.7.8. Individual XML headers provide
the package requirements for each analysis:

- `BEAST.base` 2.7.8
- `ORC` 1.2.1 for the DENV-4 mixture analysis
- `BEASTLabs` 2.0.3 for the DENV-4 mixture analysis
- `MultiTypeTree` 8.3.0 for the H3N2 structured-coalescent analysis
- `bModelTest` 1.3.3 and `OBAMA` 1.1.1 for the rbcL OBAMA sensitivity analysis

The current GitHub release
targets BEAST.base 2.8.0-beta5 / BEAST3-compatible builds, JDK 25, LPhy
1.8.0-beta1, and LPhyBEAST 2.0.0-SNAPSHOT for LPhy-to-BEAST conversion.

Some archived empirical XML files were generated before the BEAST3 migration.
Their scientific model specification is unchanged in this archive; only the
custom `CategoricalDistribution` class path has been updated to the current
RelaxClockAveraging package namespace.

## Dataset Provenance

### DENV-4 (`real/D4/Dengue4.nex`)

17-taxon serially sampled dengue virus serotype 4 envelope-gene alignment
(1485 bp), sampled 1956-1994. The alignment was compiled by Rambaut 2000,
Bioinformatics 16(4):395-399, doi:10.1093/bioinformatics/16.4.395, and shipped
as the example dataset with TipDate. Underlying envelope-gene sequences are
from Lanciotti, Gubler & Trent 1997, J. Gen. Virol. 78(9):2279-2286; one
sequence identified as recombinant by Worobey, Rambaut & Holmes 1999, PNAS
96(13):7352-7357 was omitted, leaving the 17 taxa here.

Taxon labels: Thailand63, Philippines56/64/84, SriLanka78, Thailand78/84,
Indonesia76/77, Tahiti79/85, PuertoRico86, ElSalvador83/94, NewCaledonia84,
Mexico84, Brazil82.

### RSV2 (`real/RSV2/`)

RSV-A G-gene alignment, 129 sequences (629 nt) collected between 1956 and 2002.
Source: Zlateva et al. 2004, J. Virol. 78(9):4675-4683,
doi:10.1128/jvi.78.9.4675-4683.2004. The dataset contains 81 Belgian isolates
generated in that study plus 48 previously published sequences retrieved from
GenBank; see Table 1 of the paper for the full accession list.

### H3N2 (`real/H3N2/`)

245-taxon stratified subset of the 980-taxon H3N2 HA alignment of Vaughan et
al. 2014, Bioinformatics 30(16):2272-2279. Samples come from Hong Kong, New
York, and New Zealand between 2000 and 2006. Subset composition: 55 Hong Kong,
79 New York, 111 New Zealand sequences, drawn by proportional largest-remainder
sampling across region by calendar-year strata; accessions and decimal sampling
times are preserved from the original 980-taxon alignment.

### rbcL (`real/rbcl/`)

31-taxon chloroplast rbcL amino-acid alignment, reconstructed from the GenBank
accessions of Chase et al. 1993, Ann. Mo. Bot. Gard. 80(3):528-580. Used here
as the historical benchmark for autocorrelated rate evolution of Thorne et al.
1998, Mol. Biol. Evol. 15(12):1647-1657. Marchantia paleacea is retained as the
outgroup, following Thorne et al.

## Citation

When using these files, please cite the associated manuscript and the original
data sources listed under Dataset Provenance.
