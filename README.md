# Plotting macros for Higgs to Invisible NLO k-factors

## Introduction

This repository contains several macros to produce k-factor plots for the CMS Higgs to Invisible analysis note, as well as macros to correct the k-factor files for missing uncertainty information in some samples (`extrapolate.py` and `extrapolate2D.py`).

The `version-0.9` branch contains an older version, not fully described, but has more features and studies. The output for the functions common to `master` will be the same though.

## Making plots for the note

The code is contained within `mkplots.py` Run like:

-  `python3 mkplots.py path_to_input_directory path_to_output_directory`

There are also `plot_wz.py` and `plot_wz2D.py` which plots the uncertainty on the ratio of W/Z for the 1D and 2D k-factors

## Correcting the k-factors

In order to produce working k-factor files for input to `CHIP` the 2D k-factor files created in the https://github.com/snwebb/higgsinvisible respository need to have some post-processing run on them to correct for missing uncertainty information and to remove 0 values in some bins (to avoid crashes in `FAST`).
For the VBF analysis, which now uses the NLO samples directly the program now also sets the nominal scale factors to 1 and divides the uncertainty histogram by the (old) nominal values.

This is run like:
-  `python3 extrapolate2D.py path_to_input_directory`

Note that the input k-factor files are overwritten when running `extrapolate2D`, so do not run the code over the same input files twice.

There is also a 1D equivalent `extrapolate.py`, but this is no longer necessary to run as 2D k-factors are used in the analysis (and also has not been brought up to date very recently).