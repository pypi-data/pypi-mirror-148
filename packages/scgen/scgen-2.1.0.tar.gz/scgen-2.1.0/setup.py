# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scgen']

package_data = \
{'': ['*']}

install_requires = \
['adjustText',
 'anndata>=0.7.5',
 'scanpy>=1.6',
 'scvi-tools>=0.15.0',
 'seaborn>=0.11']

extras_require = \
{':(python_version < "3.8") and (extra == "docs")': ['typing_extensions'],
 ':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'dev': ['black>=20.8b1',
         'codecov>=2.0.8',
         'flake8>=3.7.7',
         'isort>=5.7',
         'jupyter>=1.0',
         'loompy>=3.0.6',
         'nbconvert>=5.4.0',
         'nbformat>=4.4.0',
         'pre-commit>=2.7.1',
         'pytest>=4.4'],
 'docs': ['ipython>=7.1.1',
          'nbsphinx',
          'nbsphinx-link',
          'pydata-sphinx-theme>=0.4.0',
          'scanpydoc>=0.5',
          'sphinx>=4.1,<4.4',
          'sphinx-autodoc-typehints',
          'sphinx-material'],
 'tutorials': ['leidenalg',
               'loompy>=3.0.6',
               'python-igraph',
               'scikit-misc>=0.1.3']}

setup_kwargs = {
    'name': 'scgen',
    'version': '2.1.0',
    'description': 'ScGen - Predicting single cell perturbations.',
    'long_description': '# scGen [![PyPI version](https://badge.fury.io/py/scgen.svg)](https://badge.fury.io/py/scgen) [![Build Status](https://travis-ci.com/theislab/scGen.svg?branch=master)](https://travis-ci.com/theislab/scGen) [![Documentation Status](https://readthedocs.org/projects/scgen/badge/?version=latest)](https://scgen.readthedocs.io/en/latest/?badge=latest) [![Downloads](https://pepy.tech/badge/scgen)](https://pepy.tech/project/scgen)\n\n\n\n\n<img align="center" src="./sketch/sketch.png?raw=true">\n\n## Introduction\nscGen is a generative model to predict single-cell perturbation response across cell types, studies and species\n  [(Nature Methods, 2019)](https://www.nature.com/articles/s41592-019-0494-8). scGen is implemented using the [scvi-tools framework](https://scvi-tools.org/).\n\n## Getting Started\nWhat you can do with scGen:\n\n* Train on a dataset with multiple cell types and conditions and predict the perturbation effect on the cell type\nwhich you only have in one condition. This scenario can be extended to multiple species where you want to predict\nthe effect of a specific species using another or all the species.\n\n* Train on a dataset where you have two conditions (e.g. control and perturbed) and predict on second dataset\nwith similar genes.\n\n* Remove batch effect on labeled data. In this scenario you need to provide cell_type and batch labels to\nthe method. Note that `batch_removal` does not require all cell types to be present in all datasets (batches). If\nyou have dataset specific cell type it will preserved as before.\n\n* We assume there exist two conditions in you dataset (e.g. control and perturbed). You can train the model and with\nyour data and predict the perturbation for the cell type/species of interest.\n\n* We recommend to use normalized data for the training. A simple example for normalization pipeline using scanpy:\n\n``` python\nimport scanpy as sc\nadata = sc.read(data)\nsc.pp.normalize_total(adata)\nsc.pp.log1p(adata)\n```\n* We further recommend to use highly variable genes (HVG). For the most examples in the paper we used top ~7000\nHVG. However, this is optional and highly depend on your application and computational power.\n\n\n\n\n## Installation\n\n### Installation with pip\nTo install the latest version scGen via pip:\n```bash\npip install scgen\n```\n\nor install the development version via pip:\n```bash\npip install git+https://github.com/theislab/scgen.git\n```\n\n## Examples\n\nSee examples at our [documentation site](https://scgen.readthedocs.io/).\n\n## Reproducing paper results\nIn order to reproduce paper results visit [here](https://github.com/M0hammadL/scGen_reproducibility).\n\n## References\n\nLotfollahi, Mohammad and Wolf, F. Alexander and Theis, Fabian J.\n**"scGen predicts single-cell perturbation responses."**\nNature Methods, 2019. [pdf](https://rdcu.be/bMlbD)\n',
    'author': 'Mohammad lotfollahi',
    'author_email': 'mohammad.lotfollahi@helmholtz-muenchen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theislab/scgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
