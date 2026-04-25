# mixture_data

Companion data repository for the hierarchical clock-mixture manuscript (`clock-paper`).
Contains the analysis-ready input files (alignments, BEAST XML configurations) and processed outputs for the simulation study and the four empirical benchmarks.

## Layout

- `simulation/{auto,strict,ucln}/` — stratified simulation study (100 replicates per stratum).
- `real/D4/` — DENV-4 serially sampled benchmark.
- `real/RSV2/` — RSV-A G-gene benchmark.
- `real/H3N2/` — H3N2 structured-coalescent subset.
- `real/rbcl/` — 31-taxon chloroplast *rbcL* historical benchmark.

## Dataset provenance

### DENV-4 (`real/D4/Dengue4.nex`)
17-taxon serially sampled dengue virus serotype 4 envelope-gene alignment (1485 bp), sampled 1956–1994.
The alignment was compiled by Rambaut 2000, *Bioinformatics* 16(4):395–399, doi:10.1093/bioinformatics/16.4.395, and shipped as the example dataset with TipDate (hence the `BEGIN RHINO` block in the Nexus file).
Underlying envelope-gene sequences are from Lanciotti, Gubler & Trent 1997, *J. Gen. Virol.* 78(9):2279–2286; one sequence identified as recombinant by Worobey, Rambaut & Holmes 1999, *PNAS* 96(13):7352–7357 was omitted, leaving the 17 taxa here.
Taxon labels: Thailand63, Philippines56/64/84, SriLanka78, Thailand78/84, Indonesia76/77, Tahiti79/85, PuertoRico86, ElSalvador83/94, NewCaledonia84, Mexico84, Brazil82.

### RSV2 (`real/RSV2/`)
RSV-A G-gene alignment, 129 sequences (629 nt) collected between 1956 and 2002.
Source: Zlateva et al. 2004, *J. Virol.* 78(9):4675–4683, doi:10.1128/jvi.78.9.4675-4683.2004.
Composition: 81 Belgian isolates generated in that study, plus 48 previously published sequences retrieved from GenBank; see Table 1 of the paper for the full accession list.

### H3N2 (`real/H3N2/`)
245-taxon stratified subset of the 980-taxon H3N2 HA alignment of Vaughan et al. 2014, *Bioinformatics* 30(16):2272–2279.
Sampled from Hong Kong, New York, and New Zealand between 2000 and 2006.
Subset composition: 55 Hong Kong, 79 New York, 111 New Zealand sequences, drawn by proportional largest-remainder sampling across region × calendar-year strata; accessions and decimal sampling times preserved from the original 980-taxon alignment.

### rbcL (`real/rbcl/`)
31-taxon chloroplast *rbcL* amino-acid alignment, reconstructed from the GenBank accessions of Chase et al. 1993, *Ann. Mo. Bot. Gard.* 80(3):528–580.
Used here as the historical benchmark for autocorrelated rate evolution of Thorne et al. 1998, *Mol. Biol. Evol.* 15(12):1647–1657.
*Marchantia paleacea* retained as the outgroup, following Thorne et al.

## Software versions

XMLs target BEAST 2 with the following package pins (see individual XML headers):
- `BEAST.base` 2.7.8
- `ORC` 1.2.1
- `BEASTLabs` 2.0.3

## Citation

If you use these files, please cite the manuscript (in preparation) and the original data sources listed above.
