# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apav',
 'apav.analysis',
 'apav.core',
 'apav.qtwidgets',
 'apav.tests',
 'apav.utils',
 'apav.visualization']

package_data = \
{'': ['*'], 'apav': ['resources/icons/*', 'resources/testdata/*']}

install_requires = \
['PyQt5>=5.11',
 'fast-histogram',
 'lmfit>=1.0',
 'numba',
 'numpy>=1.17',
 'periodictable',
 'pyqtgraph>=0.11.0',
 'pytest',
 'pytest-qt>=3',
 'tabulate']

setup_kwargs = {
    'name': 'apav',
    'version': '1.2.2',
    'description': 'A Python library for Atom Probe Tomography analysis',
    'long_description': '# APAV: Python analysis for atom probe tomography\n[![Documentation Status](https://readthedocs.org/projects/apav/badge/?version=latest)](https://apav.readthedocs.io/en/latest/?badge=latest)\n[![coverage report](https://gitlab.com/jesseds/apav/badges/master/coverage.svg)](https://gitlab.com/jesseds/apav/commits/master)\n[![pipeline status](https://gitlab.com/jesseds/apav/badges/master/pipeline.svg)](https://gitlab.com/jesseds/apav/-/commits/master)\n\nAPAV (Atom Probe Analysis and Visualization) is a Python library for the analysis and\nvisualization of atom probe tomography experiments, for example:\n\n* Disambiguation of multiple detector events in mass or time-of-flight histograms\n* Correlation histograms and molecular dissociation\n* Calculation of molecular isotopic distributions\n* Read/write common file formats (*.pos, *.epos, *.ato, *.apt, and *.rrng) or simulated data\n* Roi primitives for localized analysis\n* Interactive visualizations\n* Build analyses in the compositional domain (i.e. compositional "grids" with 1st + 2nd pass delocalization)\n* Quantify mass spectra using various levels of fitting/background correction\n\nAPAV is open source (GPLv2_ or greater) and is platform independent. It is written in Python 3\nusing NumPy to accelerate mathematical computations, and other mathematical tools for more niche calculations.\nVisualizations leverage pyqtgraph and other custom Qt widgets.\n\n# Support\nPost discussion to the [GitLab issue tracker](https://gitlab.com/jesseds/apav/-/issues)\n\n# Documentation\nDocumentation is found at: https://apav.readthedocs.io/\n\n# FAQ\n**Why use this over IVAS or program X?**\n\nAPAV was never intended to be used as an IVAS substitute or replacement. While much of the \nfunctionality may overlap, APAV fills feature gaps in IVAS deemed lacking (or otherwise non-existent).\nSpecifically:\n1. Multiple-event analysis (correlation histograms, multiple event histograms, multiple event mass quantifications.\n2. Explicit control over mass spectrum analysis (background models, fitting, binning).\n3. Provide an interface for the development of custom analyses--a common need in the academic community.\n\n**Why is there no GUI for APAV?**\n\nAPAV is a python *library*, there is no plan for a graphical user interface for APAV. It does, however, include\nsome custom interactive GUI visualizations using pyqtgraph and Qt.\n\n\n',
    'author': 'Jesse Smith',
    'author_email': 'jesseds@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://apav.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
