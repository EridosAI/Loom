"""Training, shuffled-set reconstruction, and the alpha=1 information probe (SPEC 5-7).

* ``train`` -- masked-completion on content cells, sampling the FULL cue-shape
  distribution (sparse / one-sided / endpoint-only / interior) so the operator learns
  random access rather than gap-filling (the exp02 lesson). Context is never masked; the
  bundle set is re-shuffled with an independent permutation every batch.
* ``reconstruct`` -- single forward pass (or k-pass iterative refinement for the F3
  at-once check), returning predicted symbol ids in canonical order so recall can be
  scored at true positions.
* ``info_probe`` -- trains a tiny probe to recover the drift value from the alpha=1
  mixture, proving position is still present there (so an F4 collapse is operator
  separability-dependence, not a data ceiling -- the critique's critical guard).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from data import inject, make_drift


# ---------------------------------------------------------------------------
# shuffle helpers
# ---------------------------------------------------------------------------
def _perm(K, L, shuffle, gen):
    if not shuffle:
        return torch.arange(L).unsqueeze(0).expand(K, L).contiguous()
    return torch.stack([torch.randperm(L, generator=gen) for _ in range(K)])


def _gather_rows(x, perm):
    """x: (K, L, D) or (K, L); returns rows permuted so slot s holds canonical perm[s]."""
    if x.dim() == 3:
        return torch.gather(x, 1, perm.unsqueeze(-1).expand(-1, -1, x.shape[-1]))
    return torch.gather(x, 1, perm)


def _scatter_to_canonical(ids_shuf, perm):
    """Inverse of the gather: canonical[i, perm[i,s]] = shuffled[i, s]."""
    out = torch.empty_like(ids_shuf)
    out.scatter_(1, perm, ids_shuf)
    return out


@torch.no_grad()
def _decode(pred, cb):
    """Nearest frozen codeword (cosine) -> predicted symbol ids (K, L)."""
    pn = F.normalize(pred, dim=-1)
    sims = pn @ F.normalize(cb.E[: cb.V], dim=-1).t()   # (K, L, V)
    return sims.argmax(-1)


# ---------------------------------------------------------------------------
# masking (full cue-shape distribution)
# ---------------------------------------------------------------------------
def _sample_keep(K, L, gen):
    """Per-row content-visible mask covering the full cue-shape distribution.

    Modes: uniform-k, sparse-1, endpoint-only, one-sided run, interior-only. The
    endpoint-only mode guarantees the cue-end -> recover-begin pathway is trained.
    """
    keep = torch.zeros(K, L, dtype=torch.bool)
    modes = torch.randint(0, 5, (K,), generator=gen)
    for i in range(K):
        m = int(modes[i])
        if m == 0:                                  # uniform-k
            nk = int(torch.randint(1, L, (1,), generator=gen))
            sel = torch.randperm(L, generator=gen)[:nk]
        elif m == 1:                                # sparse-1
            sel = torch.randperm(L, generator=gen)[:1]
        elif m == 2:                                # endpoint-only ({0},{L-1},{0,L-1})
            opts = [[0], [L - 1], [0, L - 1]]
            sel = torch.tensor(opts[int(torch.randint(0, 3, (1,), generator=gen))])
        elif m == 3:                                # one-sided prefix/suffix run
            r = int(torch.randint(1, L, (1,), generator=gen))
            sel = torch.arange(r) if int(torch.randint(0, 2, (1,), generator=gen)) else torch.arange(L - r, L)
        else:                                       # interior-only
            interior = torch.arange(1, L - 1)
            k = int(torch.randint(1, len(interior) + 1, (1,), generator=gen))
            sel = interior[torch.randperm(len(interior), generator=gen)[:k]]
        keep[i, sel] = True
    return keep


# ---------------------------------------------------------------------------
# training
# ---------------------------------------------------------------------------
def train(model, fam, cb, sigma, alpha, *, clean=False, shuffle=True, steps=3000,
          lr=1e-3, tau=0.1, n_draw=4, seed=0):
    """Masked-completion training. Each step stacks ``n_draw`` independent drift draws of
    the (fixed) K-sequence family -> effective batch K*n_draw, which the continuous
    context-ranking task needs to learn from."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    X, K, L = fam.X, fam.K, fam.L
    B = K * n_draw
    Xb = X.repeat(n_draw, 1)                                 # (B, L)
    Ecand = F.normalize(cb.E[: cb.V], dim=-1)
    for _ in range(steps):
        d = make_drift(B, L, sigma, g, clean=clean)
        keep = _sample_keep(B, L, g)
        sym_ids = torch.where(keep, Xb, torch.full_like(Xb, cb.mask_id))
        content = inject(cb.E[sym_ids], d, alpha, cb)
        context = ((1.0 - alpha) * d).unsqueeze(-1)
        x = torch.cat([content, context], dim=-1)
        perm = _perm(B, L, shuffle, g)
        xs, Xs, keeps = _gather_rows(x, perm), _gather_rows(Xb, perm), _gather_rows(keep, perm)
        pred = model(xs)
        logits = F.normalize(pred, dim=-1) @ Ecand.t() / tau   # (B, L, V)
        m = ~keeps
        loss = F.cross_entropy(logits[m], Xs[m])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return model


@torch.no_grad()
def reconstruct(model, fam, cb, sigma, alpha, cue_positions, *, clean=False,
                shuffle=True, iters=1, ablate="none", gen=None):
    """Predict masked content; return predicted symbol ids in canonical order (K, L).

    Masked cells stay e_MASK across passes (no clean-codeword feedback -- that would be
    out-of-distribution and confound the at-once check); ``iters`` re-runs only re-shuffle,
    testing single-pass stability. ``ablate``: 'zero' kills the drift carrier (position
    gone -> begin-recon must collapse: the carrier-necessary gate); 'flip' reverses it.
    """
    X, K, L = fam.X, fam.K, fam.L
    gen = gen or torch.Generator().manual_seed(999)
    d = make_drift(K, L, sigma, gen, clean=clean)
    if ablate == "zero":
        d = torch.zeros_like(d)
    elif ablate == "flip":
        d = d.flip(1)
    keep = torch.zeros(K, L, dtype=torch.bool)
    keep[:, cue_positions] = True
    fill_ids = torch.where(keep, X, torch.full_like(X, cb.mask_id))
    ids_canon = X.clone()
    for _ in range(iters):
        content = inject(cb.E[fill_ids], d, alpha, cb)
        context = ((1.0 - alpha) * d).unsqueeze(-1)
        x = torch.cat([content, context], dim=-1)
        perm = _perm(K, L, shuffle, gen)
        pred = model(_gather_rows(x, perm))
        ids_canon = _scatter_to_canonical(_decode(pred, cb), perm)
    return ids_canon


@torch.no_grad()
def region_accuracy(ids_canon, X, positions):
    if not positions:
        return float("nan")
    return (ids_canon[:, positions] == X[:, positions]).float().mean().item()


# ---------------------------------------------------------------------------
# alpha=1 information-preservation probe
# ---------------------------------------------------------------------------
def info_probe(fam, cb, sigma, alpha=1.0, *, steps=800, lr=1e-2, n_draw=16, seed=0):
    """Train a tiny probe to recover the drift value from the (entangled) mixture, then
    measure order recoverability of the probe's estimate on a LARGE held-out sample. A
    probe that recovers the order as well as the oracle does => position is still present
    in x(alpha) (so an F4 collapse would be separability-dependence, not a data ceiling).
    Reported alongside the oracle order-recoverability on the SAME large sample.
    """
    g = torch.Generator().manual_seed(seed)
    X, K, L = fam.X, fam.K, fam.L
    Xb = X.repeat(n_draw, 1)
    probe = nn.Sequential(nn.Linear(cb.dc, 64), nn.GELU(), nn.Linear(64, 1))
    opt = torch.optim.Adam(probe.parameters(), lr=lr)
    for _ in range(steps):
        d = make_drift(K * n_draw, L, sigma, g)
        content = inject(cb.E[Xb], d, alpha, cb)
        loss = F.mse_loss(probe(content).squeeze(-1), d)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    with torch.no_grad():
        d = make_drift(K * 200, L, sigma, torch.Generator().manual_seed(seed + 1))
        content = inject(cb.E[X.repeat(200, 1)], d, alpha, cb)
        dhat = probe(content).squeeze(-1)
        probe_begin = (dhat.argmin(1) == 0).float().mean().item()
        oracle_begin = (d.argmin(1) == 0).float().mean().item()
    return dict(probe_begin_is_argmin=probe_begin, oracle_begin_is_argmin=oracle_begin)
