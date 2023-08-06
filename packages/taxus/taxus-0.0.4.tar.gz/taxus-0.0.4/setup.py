# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taxus']

package_data = \
{'': ['*']}

install_requires = \
['gpytorch>=1.6.0,<2.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'patsy>=0.5.2,<0.6.0',
 'torch>=1.11.0,<2.0.0',
 'tqdm>=4.63.1,<5.0.0']

setup_kwargs = {
    'name': 'taxus',
    'version': '0.0.4',
    'description': 'Gaussian Process models for transcriptome data',
    'long_description': "# _taxus_\n\n### Gaussian Process models for transcriptome data\n\n[![PyPI version](https://badge.fury.io/py/taxus.svg)](https://badge.fury.io/py/taxus)\n[![CI](https://github.com/holmrenser/taxus/actions/workflows/ci.yml/badge.svg)](https://github.com/holmrenser/taxus/actions/workflows/ci.yml)\n[![Coverage Status](https://coveralls.io/repos/github/holmrenser/taxus/badge.svg?branch=main)](https://coveralls.io/github/holmrenser/taxus?branch=main)\n\n```\npip install taxus\n```\n\n```python\nimport taxus as tx\n\n# at the moment importing data has to be handled by the user\ncovariates, counts = get_mock_data()\ngp = tx.GP('~ time + treatment', covariates, counts, kernel='rbf', likelihood='poisson')\nelbo = gp.fit()\n\nlikelihood_ratio_rbf = tx.LRT(\n    full_formula='~ time + treatment',\n    reduced_formula='~ time',\n    covariates=covariates,\n    expression=counts,\n    kernel='rbf',\n    likelihood='nb'\n)\n\nlikelihood_ratio_linear = tx.LRT(\n    full_formula='~ C(time) + C(treatment) + C(time) : C(treatment)',\n    reduced_formula='~ C(time) + C(treatment)',\n    covariates=covariates,\n    expression=counts,\n    kernel='linear',\n    likelihood='nb'\n)\n```\n",
    'author': 'Rens Holmer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/holmrenser/taxus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
