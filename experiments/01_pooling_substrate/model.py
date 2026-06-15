"""Hierarchical additive-residual pooling model (SPEC sec. 2).

The feature layer carries the fixed nested tree (1 -> G -> G*M) as additive
residuals with per-level penalties. Each unit ``i`` is a **prototype** in input
space::

    W_i = base_root + Delta1_{g1(i)} + Delta2_i          (i = 0 .. G*M-1)

    L_pool = lambda1 * sum_j ||Delta1_j||^2 + lambda2 * sum_i ||Delta2_i||^2

Large ``lambda`` drives the matching residuals toward zero -- a *soft* tie, never a
hard equality. Fully pooled (both lambda large) -> every prototype collapses to
``base_root`` (one detector). Drop ``lambda1`` -> G distinct group prototypes (the
coarse level). Drop ``lambda2`` -> G*M distinct prototypes (full resolution, the
fine level). Raising a lambda again shrinks those residuals back toward zero while
the coarser prototypes survive -- graceful re-pool ("shed detail, keep coarse
value").

Readout is a **soft nearest-prototype** classifier, NOT a free linear head::

    fine_logit_i   = -||x - W_i||^2 / temp
    coarse_logit_c = logsumexp_{i in group c} fine_logit_i        (soft OR over members)

This tying is what makes capacity track the pooling state. A free linear head can
separate clusters that differ along any single shared direction, so it *leaks* the
fine distinction through the shared (pooled) weights -- the SPEC sec.0 false
negative. With a prototype readout, the four members of a pooled group are the same
prototype, so they produce identical fine logits and genuinely cannot resolve the
four fine sub-clusters until Delta2 opens (members move apart). Negative-distance
logits also give non-vanishing gradients that pull prototypes toward the data, so
training is robust from any initialisation.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class HierarchicalPoolingModel(nn.Module):
    def __init__(
        self,
        D: int,
        n_groups: int,
        members_per_group: int,
        temp: float = 1.0,
        init_scale: float = 1e-3,
        init_center: torch.Tensor | None = None,
        seed: int = 0,
    ):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        self.D = D
        self.G = n_groups
        self.M = members_per_group
        self.U = n_groups * members_per_group
        self.temp = temp

        base = init_scale * torch.randn(D, generator=g)
        if init_center is not None:
            base = base + init_center.detach().clone()
        self.base_root = nn.Parameter(base)
        self.delta1 = nn.Parameter(init_scale * torch.randn(n_groups, D, generator=g))
        # Tiny *independent* per-unit perturbations: without them, soft-tied members
        # under identical gradients can never break symmetry (the Test A failure mode).
        self.delta2 = nn.Parameter(init_scale * torch.randn(self.U, D, generator=g))

        # g1(i): which level-1 group unit i belongs to.
        self.register_buffer("g1", torch.arange(self.U) // members_per_group)

    def weights(self) -> torch.Tensor:
        """The (U, D) per-unit prototypes W_i."""
        return self.base_root.unsqueeze(0) + self.delta1[self.g1] + self.delta2

    def forward(self, X: torch.Tensor):
        W = self.weights()                                  # (U, D)
        dist2 = torch.cdist(X, W).pow(2)                    # (N, U)
        fine_logits = -dist2 / self.temp                   # (N, U)
        # coarse logit = soft-OR (logsumexp) over a group's member logits.
        fl = fine_logits.view(X.shape[0], self.G, self.M)
        coarse_logits = torch.logsumexp(fl, dim=2)         # (N, G)
        return coarse_logits, fine_logits

    def pool_penalty(self, lam1: float, lam2: float) -> torch.Tensor:
        return lam1 * self.delta1.pow(2).sum() + lam2 * self.delta2.pow(2).sum()

    @torch.no_grad()
    def residual_norms(self):
        """Per-level residual norms: (||Delta1_j||)_j, (||Delta2_i||)_i."""
        return self.delta1.norm(dim=1).cpu(), self.delta2.norm(dim=1).cpu()
