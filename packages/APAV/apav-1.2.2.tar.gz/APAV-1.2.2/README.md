# APAV: Python analysis for atom probe tomography
[![Documentation Status](https://readthedocs.org/projects/apav/badge/?version=latest)](https://apav.readthedocs.io/en/latest/?badge=latest)
[![coverage report](https://gitlab.com/jesseds/apav/badges/master/coverage.svg)](https://gitlab.com/jesseds/apav/commits/master)
[![pipeline status](https://gitlab.com/jesseds/apav/badges/master/pipeline.svg)](https://gitlab.com/jesseds/apav/-/commits/master)

APAV (Atom Probe Analysis and Visualization) is a Python library for the analysis and
visualization of atom probe tomography experiments, for example:

* Disambiguation of multiple detector events in mass or time-of-flight histograms
* Correlation histograms and molecular dissociation
* Calculation of molecular isotopic distributions
* Read/write common file formats (*.pos, *.epos, *.ato, *.apt, and *.rrng) or simulated data
* Roi primitives for localized analysis
* Interactive visualizations
* Build analyses in the compositional domain (i.e. compositional "grids" with 1st + 2nd pass delocalization)
* Quantify mass spectra using various levels of fitting/background correction

APAV is open source (GPLv2_ or greater) and is platform independent. It is written in Python 3
using NumPy to accelerate mathematical computations, and other mathematical tools for more niche calculations.
Visualizations leverage pyqtgraph and other custom Qt widgets.

# Support
Post discussion to the [GitLab issue tracker](https://gitlab.com/jesseds/apav/-/issues)

# Documentation
Documentation is found at: https://apav.readthedocs.io/

# FAQ
**Why use this over IVAS or program X?**

APAV was never intended to be used as an IVAS substitute or replacement. While much of the 
functionality may overlap, APAV fills feature gaps in IVAS deemed lacking (or otherwise non-existent).
Specifically:
1. Multiple-event analysis (correlation histograms, multiple event histograms, multiple event mass quantifications.
2. Explicit control over mass spectrum analysis (background models, fitting, binning).
3. Provide an interface for the development of custom analyses--a common need in the academic community.

**Why is there no GUI for APAV?**

APAV is a python *library*, there is no plan for a graphical user interface for APAV. It does, however, include
some custom interactive GUI visualizations using pyqtgraph and Qt.


