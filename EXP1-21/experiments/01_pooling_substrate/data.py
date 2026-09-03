"""Hierarchical Gaussian data for the pooling-substrate rig (SPEC sec. 1).

A tree-structured clustering in R^D: ``n_coarse`` coarse centres placed far apart,
each carrying ``n_fine`` fine centres nested at a small radius ``r_fine`` inside the
parent. Samples are ``Normal(mu_fine, sigma^2 I)``.

The one property that makes the test valid (SPEC sec. 0) is *built by construction*:
coarse centres occupy the first ``n_coarse`` axes of a structured frame and fine
offsets occupy a *disjoint* set of axes (``n_coarse .. n_coarse+n_fine``). So a
low-rank (pooled) feature map can capture the coarse distinction while being blind
to the fine one -- the fine distinction genuinely *requires* opening extra
resolution. A random rotation maps the structured frame to a generic (non
axis-aligned) one so nothing reads the raw coordinates.

Setting ``fine_structure=False`` collapses every fine centre onto its coarse parent
(the "signal removed" regime used by Test C1): the coarse problem is byte-for-byte
identical, the fine sub-structure is simply gone.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import torch


@dataclass
class HGData:
    X: torch.Tensor          # (N, D) samples
    y_coarse: torch.Tensor   # (N,) coarse labels in [0, n_coarse)
    y_fine: torch.Tensor     # (N,) fine labels in [0, n_coarse*n_fine)
    mu_coarse: torch.Tensor  # (n_coarse, D)
    mu_fine: torch.Tensor    # (n_coarse*n_fine, D)
    n_coarse: int
    n_fine: int
    meta: dict = field(default_factory=dict)

    def __len__(self) -> int:
        return self.X.shape[0]

    def subset(self, idx: torch.Tensor) -> "HGData":
        return HGData(
            self.X[idx], self.y_coarse[idx], self.y_fine[idx],
            self.mu_coarse, self.mu_fine, self.n_coarse, self.n_fine, dict(self.meta),
        )

    def split(self, train_frac: float = 0.5, seed: int = 0):
        """Deterministic train/held-out split."""
        g = torch.Generator().manual_seed(seed)
        perm = torch.randperm(len(self), generator=g)
        k = int(len(self) * train_frac)
        return self.subset(perm[:k]), self.subset(perm[k:])


def make_hierarchical_gaussians(
    D: int = 16,
    n_coarse: int = 4,
    n_fine: int = 4,
    R_coarse: float = 10.0,
    r_fine: float = 1.0,
    sigma: float = 0.3,
    n_per_fine: int = 200,
    fine_structure: bool = True,
    rotate: bool = True,
    seed: int = 0,
) -> HGData:
    """Generate nested Gaussian clusters. See module docstring and SPEC sec. 1.

    Coarse centres sit on axes ``0 .. n_coarse-1`` at radius ``R_coarse``; fine
    offsets use the disjoint axes ``n_coarse .. n_coarse+n_fine-1`` at radius
    ``r_fine`` (so fine variation is orthogonal to the coarse subspace). Requires
    ``n_coarse + n_fine <= D``.
    """
    if n_coarse + n_fine > D:
        raise ValueError(
            f"need n_coarse + n_fine <= D for orthogonal nesting; "
            f"got {n_coarse}+{n_fine} > {D}"
        )
    g = torch.Generator().manual_seed(seed)

    # Structured (axis-aligned) centres.
    mu_coarse = torch.zeros(n_coarse, D)
    for c in range(n_coarse):
        mu_coarse[c, c] = R_coarse
    fine_dir = torch.zeros(n_fine, D)
    for f in range(n_fine):
        fine_dir[f, n_coarse + f] = 1.0

    mu_fine = torch.zeros(n_coarse * n_fine, D)
    for c in range(n_coarse):
        for f in range(n_fine):
            off = r_fine * fine_dir[f] if fine_structure else torch.zeros(D)
            mu_fine[c * n_fine + f] = mu_coarse[c] + off

    # Rotate the whole space to a generic frame (preserves all distances/ranks).
    if rotate:
        Q, _ = torch.linalg.qr(torch.randn(D, D, generator=g))
        mu_coarse = mu_coarse @ Q.t()
        mu_fine = mu_fine @ Q.t()

    Xs, yc, yf = [], [], []
    for c in range(n_coarse):
        for f in range(n_fine):
            idx = c * n_fine + f
            centre = mu_fine[idx] if fine_structure else mu_coarse[c]
            samples = centre.unsqueeze(0) + sigma * torch.randn(n_per_fine, D, generator=g)
            Xs.append(samples)
            yc.append(torch.full((n_per_fine,), c, dtype=torch.long))
            yf.append(torch.full((n_per_fine,), idx, dtype=torch.long))

    X = torch.cat(Xs)
    y_coarse = torch.cat(yc)
    y_fine = torch.cat(yf)
    perm = torch.randperm(len(X), generator=g)

    meta = dict(
        D=D, n_coarse=n_coarse, n_fine=n_fine, R_coarse=R_coarse, r_fine=r_fine,
        sigma=sigma, n_per_fine=n_per_fine, fine_structure=fine_structure,
        rotate=rotate, seed=seed,
    )
    return HGData(X[perm], y_coarse[perm], y_fine[perm], mu_coarse, mu_fine,
                  n_coarse, n_fine, meta)


def nesting_report(data: HGData) -> dict:
    """Confirm fine sub-clusters sit *inside* their coarse parent (SPEC sec. 1).

    Returns the min inter-coarse centre distance, the mean fine->parent distance,
    the min inter-fine distance within a parent, and a ``nested`` flag (every fine
    centre is closer to its own parent than the parent's nearest neighbour).
    """
    mu_c, mu_f = data.mu_coarse, data.mu_fine
    nc, nf = data.n_coarse, data.n_fine

    if nc > 1:
        dc = torch.cdist(mu_c, mu_c)
        inter_coarse = dc[~torch.eye(nc, dtype=torch.bool)].min().item()
    else:
        inter_coarse = float("inf")

    parent_dist, intra_fine = [], []
    for c in range(nc):
        block = mu_f[c * nf:(c + 1) * nf]
        parent_dist.append((block - mu_c[c]).norm(dim=1))
        if nf > 1:
            d = torch.cdist(block, block)
            intra_fine.append(d[~torch.eye(nf, dtype=torch.bool)].min())
    parent_dist = torch.cat(parent_dist)

    return dict(
        inter_coarse_min=inter_coarse,
        fine_to_parent_mean=parent_dist.mean().item(),
        fine_to_parent_max=parent_dist.max().item(),
        intra_fine_min=(torch.stack(intra_fine).min().item() if intra_fine else float("nan")),
        nested=bool(parent_dist.max().item() < inter_coarse),
    )
