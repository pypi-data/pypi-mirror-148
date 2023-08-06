from gpytorch.likelihoods import _OneDimensionalLikelihood
from gpytorch.distributions import base_distributions, Distribution
# from gpytorch.constraints import LessThan
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.priors import GammaPrior

# from torch.distributions import Poisson
from torch.distributions.utils import broadcast_all

import torch
from torch import lgamma, log


Poisson = base_distributions.Poisson


class NegativeBinomial(Distribution):
    arg_constraints = {}

    def __init__(self, mu, phi, validate_args=True, debug=False):
        if debug:
            print(mu.shape, phi.shape)
        self.mu, self.phi = broadcast_all(mu, phi)
        super(NegativeBinomial, self).__init__(validate_args=validate_args)

    def log_prob(self, value: torch.tensor) -> torch.tensor:
        return (
            lgamma(value + self.phi) - lgamma(value + 1) - lgamma(self.phi)
            + (self.phi * log(self.phi / (self.phi + self.mu)))
            + (value * log(self.mu / (self.phi + self.mu)))
        )

    def sample(self, sample_shape=torch.Size([]), debug=False):
        shape = self._extended_shape(sample_shape) + self.mu.shape
        p = (self.phi / (self.phi + self.mu)).expand(shape)
        gamma_rate = p / (1 - p)
        gamma_concentration = self.phi.expand(shape)
        if debug:
            print(f'{gamma_rate=} {gamma_rate=}')
        poisson_rate = base_distributions.Gamma(
            concentration=gamma_concentration, rate=gamma_rate).sample()
        if debug:
            print(f'{poisson_rate=}')
        dist = base_distributions.Poisson(poisson_rate, validate_args=False)
        return dist.sample()

    @property
    def mean(self):
        return self.mu

    @property
    def variance(self):
        return self.mu + ((self.mu ** 2) / self.phi)


class NegativeBinomialLikelihood(_OneDimensionalLikelihood):
    def __init__(self, alpha=1.0, invlink=torch.exp):
        super().__init__()
        self.alpha = torch.nn.Parameter(torch.tensor([alpha]))
        self.register_prior('alpha_prior', GammaPrior(0.1, 1.0), 'alpha')
        self.invlink = invlink

    def forward(self, function_samples: torch.tensor) -> NegativeBinomial:
        phi = 1 / self.alpha
        mu = self.invlink(function_samples)
        return NegativeBinomial(mu, phi)


class PoissonLikelihood(_OneDimensionalLikelihood):
    def __init__(self, invlink=torch.exp):
        super().__init__()
        self.invlink = invlink

    def forward(self, function_samples: torch.tensor) -> Poisson:
        rate = self.invlink(function_samples) + 1e-9
        return Poisson(rate=rate, validate_args=False)


LIKELIHOODS = dict(
    poisson=PoissonLikelihood,
    nb=NegativeBinomialLikelihood,
    gaussian=GaussianLikelihood
)
