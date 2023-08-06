import numpy as np

from .models import GP


class LRT:
    def __init__(self, *, full_formula, reduced_formula, covariates, expression,
                 kernel, likelihood):
        self.full_model = GP(full_formula, covariates, expression,
                             kernel=kernel, likelihood=likelihood)
        self.reduced_model = GP(reduced_formula, covariates, expression,
                                kernel=kernel, likelihood=likelihood)

    def fit(self, n_steps=1000, combine_terms=False):
        full_elbo = self.full_model.fit(n_steps=n_steps, show_progress_bar=False)
        if not full_elbo:
            full_elbo = np.inf
        reduced_elbo = self.reduced_model.fit(n_steps=n_steps, show_progress_bar=False)
        if not reduced_elbo:
            reduced_elbo = -np.inf
        if combine_terms:
            return full_elbo - reduced_elbo
        else:
            return (full_elbo, reduced_elbo)
