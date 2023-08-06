# _taxus_

### Gaussian Process models for transcriptome data

[![PyPI version](https://badge.fury.io/py/taxus.svg)](https://badge.fury.io/py/taxus)
[![CI](https://github.com/holmrenser/taxus/actions/workflows/ci.yml/badge.svg)](https://github.com/holmrenser/taxus/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/holmrenser/taxus/badge.svg?branch=main)](https://coveralls.io/github/holmrenser/taxus?branch=main)

```
pip install taxus
```

```python
import taxus as tx

# at the moment importing data has to be handled by the user
covariates, counts = get_mock_data()
gp = tx.GP('~ time + treatment', covariates, counts, kernel='rbf', likelihood='poisson')
elbo = gp.fit()

likelihood_ratio_rbf = tx.LRT(
    full_formula='~ time + treatment',
    reduced_formula='~ time',
    covariates=covariates,
    expression=counts,
    kernel='rbf',
    likelihood='nb'
)

likelihood_ratio_linear = tx.LRT(
    full_formula='~ C(time) + C(treatment) + C(time) : C(treatment)',
    reduced_formula='~ C(time) + C(treatment)',
    covariates=covariates,
    expression=counts,
    kernel='linear',
    likelihood='nb'
)
```
