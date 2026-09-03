"""Distributional-spread collapse-control term (Stage-0 §5, kinetic half).

Specified by FUNCTION, not citation (a provenance correction — LeJEPA / SIGReg / a
VJEPA-variant — must not destabilise the build): push the vision marginal toward
isotropy over P random 1-D projections, with **NO stop-gradient and NO EMA** (the
gradient flows live into the vision emissions). Coefficient ``alpha_spread`` is applied
by the loop; this returns the raw, differentiable L_spread.

Anchor (structural, the frozen word encoder) + this spread term (kinetic) together
remove collapse as a global optimum without cutting the gap-3 gradient (no stop-grad).
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def spread_loss(emissions: torch.Tensor, P: int, gen: torch.Generator) -> torch.Tensor:
    """Isotropy penalty over P random 1-D projections of ``emissions`` (B, D).

    For each random unit direction v, project the batch and penalise deviation of the
    1-D marginal from a standard reference: mean^2 (centring) + (var - 1)^2 (unit scale).
    Summing over many random directions pushes the whole covariance toward isotropic,
    which is what prevents dimensional collapse. No stop-grad, no EMA, no detach — the
    gradient is meant to reach the vision emissions.
    """
    B, D = emissions.shape
    V = F.normalize(torch.randn(D, P, generator=gen, device=emissions.device), dim=0)
    proj = emissions @ V                                  # (B, P)
    mean = proj.mean(dim=0)                               # (P,)
    var = proj.var(dim=0, unbiased=False)                # (P,)
    return (mean.pow(2) + (var - 1.0).pow(2)).mean()


@torch.no_grad()
def covariance_spectrum(emissions: torch.Tensor) -> torch.Tensor:
    """Eigenvalues of the (centred) emission covariance — the diversity statistic
    Readout A scores per half (a collapsing half loses spectral mass). Eval-only."""
    X = emissions - emissions.mean(dim=0, keepdim=True)
    cov = (X.t() @ X) / max(1, X.shape[0] - 1)
    return torch.linalg.eigvalsh(cov).flip(0)            # descending


@torch.no_grad()
def effective_rank(emissions: torch.Tensor) -> float:
    """Participation-ratio effective rank of the emissions (collapse -> 1.0). Eval-only."""
    ev = covariance_spectrum(emissions).clamp(min=0)
    s = ev.sum()
    if s <= 0:
        return 1.0
    p = ev / s
    return float(torch.exp(-(p * (p + 1e-12).log()).sum()))
