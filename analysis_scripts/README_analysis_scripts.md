# Analysis Scripts

Python scripts for post-processing BEAST outputs and generating the coverage
and model-recovery figures for the hierarchical clock-mixture study. The
scripts take paths relative to the simulation folder passed on the command line
and contain no absolute paths. Licensed under MIT (see `LICENSE`).

Expected simulation layout after extracting the archives:

```text
simulation/short/auto/
  data/mixture-0_true.log
  data/mixture-0_true_psi.trees
  stats/mixture-0_stats.log
  figures/
```

Example:

```bash
python analysis_scripts/calc_tree_stats.py simulation/short/auto
python analysis_scripts/plot_parameter_coverage.py simulation/short/auto
python analysis_scripts/plot_model_recovery.py simulation/short
```

Dependencies:

- Python 3.9+
- matplotlib
- numpy
- dendropy, only for `calc_tree_stats.py`
