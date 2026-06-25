"""Order-as-content carrier + entanglement + ceiling probes (Stage-0 §3, §6).

Ported from experiments/03_order_as_content (data.py + info_probe from harness.py).
The Stage-0 live path uses ``make_drift`` (driven ONCE as a continuous stream, never
reset per window) and ``inject`` at **alpha=1** along the codebook top-PC ``u`` — drift
entangled into content-bearing dims with NO separable carrier (§3). ``make_codebook``
gives the content-matched injection so entanglement is non-vacuous
(``linear_separability_r2`` < 1). ``ols_order_recovery`` / ``info_probe`` are the
independent, fixed/weak ceiling probes Readout D scores the operator against.

CARRIER DISCIPLINE: the drift carrier and the operator's position-read must stay
entangled, never a clean separable slot, or order-as-content silently becomes
order-as-index in the first build.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Drift carrier (the order signal)
# ---------------------------------------------------------------------------
def make_drift(K: int, L: int, sigma: float, gen: torch.Generator, *,
               clean: bool = False, s0: float = 2.0, m_lo: float = 0.6,
               m_hi: float = 1.4, standardize: bool = True) -> torch.Tensor:
    """Per-sequence random-walk-with-drift, shape (K, L).

    Random start + positive slope -> the same value occurs at different positions
    across sequences (no fixed value->position table; defeats soft-index / order-as-
    index). ``sigma`` tunes adjacent-position overlap. ``clean=True`` returns a fixed
    position ramp d[:,p]=p (an index in costume) used by controls.
    """
    if clean:
        d = torch.arange(L, dtype=torch.float32).expand(K, L).clone()
    else:
        start = s0 * torch.randn(K, 1, generator=gen)
        slope = m_lo + (m_hi - m_lo) * torch.rand(K, 1, generator=gen)
        steps = slope + sigma * torch.randn(K, L - 1, generator=gen)
        d = torch.cat([torch.zeros(K, 1), steps.cumsum(dim=1)], dim=1) + start
    if standardize:
        d = (d - d.mean()) / (d.std() + 1e-8)
    return d


def drift_validity(sigma: float, L: int = 3, *, clean: bool = False, n_mc: int = 4000,
                   seed: int = 12345, bin_w: float = 0.25) -> dict:
    """SPEC §4-style checks on the drift signal `d` (Monte-Carlo). Returns adjacent
    overlap, oracle extreme-identifiabilities (begin=argmin, end=argmax — the ceiling
    for cue-end->begin recall), order recoverability, and map-non-fixedness. Computed
    on `d` only => alpha-invariant. Used to select the sigma-band before the loop.
    """
    g = torch.Generator().manual_seed(seed)
    d = make_drift(n_mc, L, sigma, g, clean=clean)
    overlap = (d[:, 1:] < d[:, :-1]).float().mean().item()
    begin_is_argmin = (d.argmin(1) == 0).float().mean().item()
    end_is_argmax = (d.argmax(1) == L - 1).float().mean().item()
    ranks = d.argsort(1).argsort(1)
    rank_acc = (ranks == torch.arange(L)).float().mean().item()
    exact_order = (d.argsort(1) == torch.arange(L)).all(1).float().mean().item()
    binpos = defaultdict(set)
    b = (d / bin_w).round().long()
    for i in range(min(n_mc, 2000)):
        for p in range(L):
            binpos[int(b[i, p])].add(p)
    occ = list(binpos.values())
    map_nonfixed = sum(1 for s in occ if len(s) >= 2) / max(1, len(occ))
    return dict(
        adjacent_overlap=overlap, begin_is_argmin=begin_is_argmin,
        end_is_argmax=end_is_argmax, rank_acc=rank_acc, exact_order=exact_order,
        map_nonfixed_frac=map_nonfixed,
    )


# ---------------------------------------------------------------------------
# Entanglement codebook (fixed injection direction, content-matched scale)
# ---------------------------------------------------------------------------
@dataclass
class Codebook:
    u: torch.Tensor   # (dc,) fixed unit injection direction (top-PC of the content)
    kappa: float      # injection scale, matched to content variance along u
    dc: int


def make_codebook_from_content(content: torch.Tensor) -> Codebook:
    """Fixed entanglement direction from a sample of CONTENT vectors (dc-dim).

    ``u`` = top principal component of the content (the direction content actually
    occupies). Injecting drift there genuinely confounds it with content (a content-free
    axis would let a single clean projection read the drift off — separable -> order-as-
    index). ``kappa`` matches the injection magnitude to the content's spread along u, so
    a naive linear read of the drift is confounded by the content offset (recoverable
    only by first disentangling content — hard but solvable; linear_separability_r2 < 1).
    """
    C = content.reshape(-1, content.shape[-1])
    Cc = C - C.mean(0, keepdim=True)
    _, _, Vh = torch.linalg.svd(Cc, full_matrices=False)
    u = Vh[0]                                    # top-PC, unit
    kappa = (Cc @ u).std().item()
    return Codebook(u=u, kappa=kappa, dc=content.shape[-1])


def inject(content: torch.Tensor, d: torch.Tensor, alpha: float, cb: Codebook):
    """content (..., dc) + alpha*kappa*d*u along the content direction u (entangled).

    At alpha=1 there is NO separable context coordinate: the position rides entirely in
    the content dims along u. ``d`` broadcasts over the last (dc) axis.
    """
    return content + alpha * cb.kappa * d.unsqueeze(-1) * cb.u


def linear_separability_r2(content: torch.Tensor, d: torch.Tensor, cb: Codebook,
                           alpha: float = 1.0) -> float:
    """Best-linear-read R^2 of the drift `d` from the entangled mixture content.

    R^2 ~ 1 => drift sits in a clean separable subspace (NOT entangled -> order became
    index, the §3 failure). R^2 well below 1 => genuinely confounded with content. This
    is the live-path entanglement gate, logged every window (CARRIER_SEPARABLE if it
    rises toward 1).
    """
    mix = inject(content, d, alpha, cb).reshape(-1, cb.dc)
    dflat = d.reshape(-1, 1)
    A = torch.cat([mix, torch.ones(mix.shape[0], 1)], dim=1)
    sol = torch.linalg.lstsq(A, dflat).solution
    resid = dflat - A @ sol
    ss_res = (resid ** 2).sum()
    ss_tot = ((dflat - dflat.mean()) ** 2).sum()
    return (1.0 - ss_res / ss_tot).item()


def max_coordinate_r2(content: torch.Tensor, d: torch.Tensor, cb: Codebook,
                      alpha: float = 1.0, center_within: bool = False) -> float:
    """Max single-COORDINATE R^2 of the drift `d` from the entangled mixture.

    The direct §3 test: a clean separable *slot* (order-as-index) is a single coordinate
    that recovers d (R^2 ~ 1). Because d is injected along a DENSE direction u and confounded
    by a content nuisance on the same direction, no single coordinate carries it cleanly ->
    max single-coord R^2 < 1 (entangled). ``center_within=True`` removes the per-window mean
    (dim=1) first, so the test is on the WITHIN-window order the operator actually reads (not
    the absolute drift trend across the stream). The live-path guard gates on THIS.
    """
    mix = inject(content, d, alpha, cb)                  # (..., C, dc)
    dd = d
    if center_within and mix.dim() >= 2:
        mix = mix - mix.mean(dim=-2, keepdim=True)
        dd = d - d.mean(dim=-1, keepdim=True)
    mix = mix.reshape(-1, cb.dc)
    dflat = dd.reshape(-1)
    dc = dflat - dflat.mean()
    mc = mix - mix.mean(0, keepdim=True)
    cov = (dc.unsqueeze(1) * mc).mean(0)                 # (dc,)
    denom = dc.var(unbiased=False) * mc.var(0, unbiased=False) + 1e-12
    r2 = (cov.pow(2) / denom)
    return float(r2.max())


def ols_order_recovery(content_train: torch.Tensor, d_train: torch.Tensor,
                       content_eval: torch.Tensor, d_eval: torch.Tensor,
                       cb: Codebook, alpha: float = 1.0) -> dict:
    """FIXED, non-learned (closed-form OLS) ceiling probe, independent of the operator.

    Fit a linear read of the drift from the entangled mixture on a train sample, then on
    a fresh eval sample report begin=argmin of the OLS-predicted drift vs the oracle. If
    even this weak fixed probe recovers order ~ the oracle, order is extractable here ->
    an operator collapse is a real failure, not a data ceiling. (Readout D baseline.)
    """
    Mtr = inject(content_train, d_train, alpha, cb).reshape(-1, cb.dc)
    A = torch.cat([Mtr, torch.ones(Mtr.shape[0], 1)], dim=1)
    w = torch.linalg.lstsq(A, d_train.reshape(-1, 1)).solution        # (dc+1, 1)
    Mte = inject(content_eval, d_eval, alpha, cb)
    pred = (Mte @ w[:-1] + w[-1]).squeeze(-1)                         # (B, L)
    return dict(
        probe_begin_is_argmin=(pred.argmin(1) == 0).float().mean().item(),
        oracle_begin_is_argmin=(d_eval.argmin(1) == 0).float().mean().item(),
    )


def info_probe(content_sampler, cb: Codebook, *, dc: int, L: int, steps=600, lr=1e-2,
               n_draw=16, seed=0) -> dict:
    """Train a tiny MLP probe to recover the drift from the entangled mixture, then
    measure order recoverability of the probe's estimate on a fresh sample. A probe that
    recovers order ~ the oracle => position is still present in the alpha=1 mixture (so a
    collapse is operator separability-dependence, not a data ceiling). ``content_sampler``
    is a callable (B, gen) -> (content (B,L,dc), d (B,L)).
    """
    g = torch.Generator().manual_seed(seed)
    probe = nn.Sequential(nn.Linear(dc, 64), nn.GELU(), nn.Linear(64, 1))
    opt = torch.optim.Adam(probe.parameters(), lr=lr)
    for _ in range(steps):
        content, d = content_sampler(n_draw, g)
        mix = inject(content, d, 1.0, cb)
        loss = F.mse_loss(probe(mix).squeeze(-1), d)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    with torch.no_grad():
        content, d = content_sampler(200, torch.Generator().manual_seed(seed + 1))
        mix = inject(content, d, 1.0, cb)
        dhat = probe(mix).squeeze(-1)
        probe_begin = (dhat.argmin(1) == 0).float().mean().item()
        oracle_begin = (d.argmin(1) == 0).float().mean().item()
    return dict(probe_begin_is_argmin=probe_begin, oracle_begin_is_argmin=oracle_begin)
