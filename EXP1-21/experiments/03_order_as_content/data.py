"""Data for the order-as-content rig (SPEC sec. 3-4).

Three pieces, kept deliberately separate so a failure is attributable:

1. **Content family** (exp02-shaped, unchanged): a fixed family of length-L symbol
   sequences with a begin<->end bijection and a non-injective interior, so cue-end ->
   recover-begin is well-posed and content alone never reveals position.

2. **Drift carrier `d`** (the load-bearing part): a per-sequence-stochastic cumulative
   walk with a *random start* AND a *random positive slope* plus sigma noise. Random
   start + slope mean the same context value occurs at different positions across
   sequences -> there is no fixed value->position table (defeats the soft-index / F2
   easy-out). Positive slope keeps within-window order recoverable (begin/end are robust
   cumulative extremes); sigma tunes adjacent-position overlap. `d` is standardized to
   unit scale so the entanglement injection is *comparable* to content (not swamping).

3. **Entanglement** `x(alpha) = [E[sym] + alpha*d*u ; (1-alpha)*d]`: a single fixed
   direction `u` relocates the drift from a dedicated context dim (alpha=0, separable)
   into the content coordinates (alpha=1, dead context dim). Masking swaps only the
   *symbol codeword* (c -> e_MASK); the drift injection `alpha*d*u` and the context are
   kept, so the position-query survives even at alpha=1 where the context dim is dead.

All sec.4 validity checks are computed on `d` (and the symbol family) -- never on the
mixture `x(alpha)` -- so they are alpha-invariant by construction.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import torch


# ---------------------------------------------------------------------------
# 1. Content family (exp02 shape)
# ---------------------------------------------------------------------------
@dataclass
class Family:
    X: torch.Tensor          # (K, L) symbol ids
    K: int
    L: int
    V: int
    begin_pos: int
    end_pos: int
    interior_pos: list


def build_family(K: int = 16, n_interior: int = 4, pool: int = 4, V: int = 20,
                 seed: int = 0) -> Family:
    g = torch.Generator().manual_seed(seed)
    L = n_interior + 2
    begins = list(range(K))
    ends = torch.randperm(K, generator=g).tolist()          # begin<->end bijection
    frags = [torch.randint(0, V, (n_interior,), generator=g).tolist() for _ in range(pool)]
    seqs = [[begins[k]] + frags[k % pool] + [ends[k]] for k in range(K)]
    X = torch.tensor(seqs, dtype=torch.long)
    return Family(X=X, K=K, L=L, V=V, begin_pos=0, end_pos=L - 1,
                  interior_pos=list(range(1, L - 1)))


def family_validity(fam: Family) -> dict:
    """The exp02 content-structure checks (computed on X)."""
    X, bp, ep, ip = fam.X, fam.begin_pos, fam.end_pos, fam.interior_pos
    end_to_begin, ok = {}, True
    for row in X:
        e, b = int(row[ep]), int(row[bp])
        if end_to_begin.setdefault(e, b) != b:
            ok = False
    interiors = [tuple(r[ip].tolist()) for r in X]
    pos_of = defaultdict(set)
    for r in X:
        for p, s in enumerate(r.tolist()):
            pos_of[s].add(p)
    int_to_b = defaultdict(set)
    for r in X:
        int_to_b[tuple(r[ip].tolist())].add(int(r[bp]))
    return dict(
        end_determines_begin=ok,
        position_varied_symbols=sum(1 for ps in pos_of.values() if len(ps) >= 2),
        shared_interior=len(set(interiors)) < len(interiors),
        interior_ambiguous_about_begin=any(len(b) > 1 for b in int_to_b.values()),
        chance=1.0 / fam.K,
    )


# ---------------------------------------------------------------------------
# 2. Drift carrier
# ---------------------------------------------------------------------------
def make_drift(K: int, L: int, sigma: float, gen: torch.Generator, *,
               clean: bool = False, s0: float = 2.0, m_lo: float = 0.6,
               m_hi: float = 1.4, standardize: bool = True) -> torch.Tensor:
    """Per-sequence random-walk-with-drift, shape (K, L).

    ``clean=True`` returns a fixed position ramp ``d[:,p]=p`` (no random start, no
    noise) -- a clean fixed coordinate (an index in costume) used by Control A; it
    fails the map-non-fixedness check, confirming the checks discriminate index from
    content.
    """
    if clean:
        d = torch.arange(L, dtype=torch.float32).expand(K, L).clone()
    else:
        start = s0 * torch.randn(K, 1, generator=gen)
        slope = m_lo + (m_hi - m_lo) * torch.rand(K, 1, generator=gen)   # per-seq, positive
        steps = slope + sigma * torch.randn(K, L - 1, generator=gen)
        d = torch.cat([torch.zeros(K, 1), steps.cumsum(dim=1)], dim=1) + start
    if standardize:
        d = (d - d.mean()) / (d.std() + 1e-8)
    return d


def drift_validity(sigma: float, L: int = 6, *, clean: bool = False, n_mc: int = 4000,
                   seed: int = 12345, bin_w: float = 0.25) -> dict:
    """SPEC sec.4 checks on the drift signal `d` (Monte-Carlo over many trajectories).

    Returns adjacent-overlap, the oracle extreme-identifiabilities (begin=argmin,
    end=argmax -- the ceiling for cue-end->begin recall), positionwise order
    recoverability, and map-non-fixedness. Computed on `d` only => alpha-invariant.
    """
    g = torch.Generator().manual_seed(seed)
    d = make_drift(n_mc, L, sigma, g, clean=clean)
    overlap = (d[:, 1:] < d[:, :-1]).float().mean().item()
    begin_is_argmin = (d.argmin(1) == 0).float().mean().item()
    end_is_argmax = (d.argmax(1) == L - 1).float().mean().item()
    ranks = d.argsort(1).argsort(1)
    rank_acc = (ranks == torch.arange(L)).float().mean().item()
    exact_order = (d.argsort(1) == torch.arange(L)).all(1).float().mean().item()
    # map non-fixedness: bin values; fraction of occupied bins seen at >=2 positions.
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
# 3. Entanglement / bundles
# ---------------------------------------------------------------------------
@dataclass
class Codebook:
    E: torch.Tensor   # (V+1, dc) frozen unit codewords; row V == [MASK]
    u: torch.Tensor   # (dc,) fixed unit injection direction (top-PC of the codewords)
    kappa: float      # injection scale, matched to content variance along u
    V: int
    dc: int

    @property
    def mask_id(self) -> int:
        return self.V


def make_codebook(V: int = 20, dc: int = 16, seed: int = 0) -> Codebook:
    """Frozen unit codebook. The injection direction ``u`` is the **top principal
    component of the real codewords** -- the direction the content *actually occupies*,
    so injecting drift there genuinely confounds it with content (a content-free axis
    would let drift be read off by a single clean projection, making the alpha=1 corner
    separable and F4 vacuous). ``kappa`` matches the injection magnitude to the codewords'
    spread along u, so at alpha=1 a naive linear read of the drift is confounded by the
    symbol offset (recoverable only by first disentangling content -- hard but solvable).
    """
    g = torch.Generator().manual_seed(seed)
    E = torch.randn(V + 1, dc, generator=g)
    E = E / E.norm(dim=1, keepdim=True)
    Ev = E[:V]
    _, _, Vh = torch.linalg.svd(Ev - Ev.mean(0, keepdim=True), full_matrices=False)
    u = Vh[0]                                           # top-PC, unit
    kappa = (Ev @ u).std().item()                      # match drift injection to content spread on u
    return Codebook(E=E, u=u, kappa=kappa, V=V, dc=dc)


def inject(content_sym: torch.Tensor, d: torch.Tensor, alpha: float, cb: Codebook):
    """content_sym (..., dc) + alpha*kappa*d*u along the content direction u."""
    return content_sym + alpha * cb.kappa * d.unsqueeze(-1) * cb.u


def make_bundles(X: torch.Tensor, d: torch.Tensor, alpha: float, keep: torch.Tensor,
                 cb: Codebook):
    """Assemble bundles ``x(alpha)`` and the clean reconstruction targets.

    ``keep`` (K,L) bool: content visible (symbol shown) where True, masked (e_MASK)
    where False. The drift injection and the context ``(1-alpha)*d`` are kept regardless
    of the mask (they carry position, not symbol identity).
    """
    sym_ids = torch.where(keep, X, torch.full_like(X, cb.mask_id))
    content = inject(cb.E[sym_ids], d, alpha, cb)       # (K, L, dc)
    context = ((1.0 - alpha) * d).unsqueeze(-1)         # (K, L, 1)
    x = torch.cat([content, context], dim=-1)           # (K, L, dc+1)
    target = cb.E[X]                                    # clean codewords (K, L, dc)
    return x, target


def linear_separability_r2(fam, cb, sigma: float, alpha: float, *, n_draw: int = 200,
                           seed: int = 7) -> float:
    """Best-linear-read R^2 of the drift `d` from the (entangled) mixture content at
    `alpha`, over a large Monte-Carlo sample. R^2 ~ 1 => drift sits in a clean separable
    subspace (alpha=1 not really entangled -> F4 would be vacuous); R^2 well below 1 =>
    genuinely confounded with content (the validity gate for F4)."""
    g = torch.Generator().manual_seed(seed)
    B = fam.K * n_draw
    Xb = fam.X.repeat(n_draw, 1)
    d = make_drift(B, fam.L, sigma, g)
    content = inject(cb.E[Xb], d, alpha, cb).reshape(-1, cb.dc)
    dflat = d.reshape(-1, 1)
    A = torch.cat([content, torch.ones(content.shape[0], 1)], dim=1)
    sol = torch.linalg.lstsq(A, dflat).solution
    resid = dflat - A @ sol
    ss_res = (resid ** 2).sum()
    ss_tot = ((dflat - dflat.mean()) ** 2).sum()
    return (1.0 - ss_res / ss_tot).item()


def ols_order_recovery(fam, cb, sigma: float, alpha: float, *, n_train: int = 200,
                       n_eval: int = 200, seed: int = 7) -> dict:
    """A FIXED, non-learned (closed-form OLS) ceiling probe, independent of the operator.
    Fit a linear read of the drift from the mixture content on a train MC, then on a fresh
    eval MC report begin=argmin of the OLS-predicted drift vs the oracle. If even this weak
    fixed probe recovers order ~ the oracle, the order is extractable at this (sigma,alpha)
    cell -> an operator collapse there is a real F4 failure, not a data ceiling."""
    g = torch.Generator().manual_seed(seed)
    Xtr = fam.X.repeat(n_train, 1)
    dtr = make_drift(fam.K * n_train, fam.L, sigma, g)
    Ctr = inject(cb.E[Xtr], dtr, alpha, cb).reshape(-1, cb.dc)
    A = torch.cat([Ctr, torch.ones(Ctr.shape[0], 1)], dim=1)
    w = torch.linalg.lstsq(A, dtr.reshape(-1, 1)).solution            # (dc+1, 1)
    Xte = fam.X.repeat(n_eval, 1)
    dte = make_drift(fam.K * n_eval, fam.L, sigma, torch.Generator().manual_seed(seed + 1))
    Cte = inject(cb.E[Xte], dte, alpha, cb)
    pred = (Cte @ w[:-1] + w[-1]).squeeze(-1)                         # (B, L)
    return dict(
        probe_begin_is_argmin=(pred.argmin(1) == 0).float().mean().item(),
        oracle_begin_is_argmin=(dte.argmin(1) == 0).float().mean().item(),
    )
