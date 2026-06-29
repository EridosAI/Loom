"""Category-supervised substrate oracle (Stage-1 Step-0 check (b), SPEC §0).

The F3-analog for the conflict rig: can a FRESH substrate, capacity forced open, CATEGORY-supervised,
**with the deployed SIGReg/spread regime active at deployed strength**, recover the CATEGORY axis from
its OWN emissions (p @ W)? If yes, the category is *representable* — so a no-redirect result is "the
word didn't teach a representable category" (the real test), not "category unrepresentable" (F3-analog,
stop). Mirrors ``oracle_probe`` exactly (capacity-open, A+axis-supervised member-marginal CE, SIGReg at
parity, nearest-centroid recovery, content-ablation guard) — only the supervised/recovered axis changes
from member-B to the category-marginal.

The category-marginal logits = logsumexp over the DISTRACTOR index of the member-marginal logits
(member b = distractor*n_category + category), the dual marginalisation to the coarse(=over-members)
and member(=over-groups) logits.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
import torch.nn.functional as F

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "src"))
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

from loom import spread                                     # noqa: E402
from encoders import VisionCortex                           # noqa: E402  (exp04)
from oracle_probe import _member_marginal_logits            # noqa: E402  (exp04, reuse)

from conflict_stream import ConflictStimulus                # noqa: E402  (exp05)

ABLATION_MARGIN = 0.10          # ablated recovery must be <= chance + this (collapse)


def _make_conflict_stim(cfg, *, ablate_category=False, ablate_distractor=False):
    return ConflictStimulus(
        cfg.D, cfg.n_A, cfg.n_distractor, cfg.n_category,
        R_coarse=cfg.R_coarse, r_distractor=cfg.r_distractor, r_category=cfg.r_category,
        sigma=cfg.sigma_stim, seed=cfg.seed,
        ablate_category=ablate_category, ablate_distractor=ablate_distractor)


def _category_marginal_logits(pool, X, n_distractor, n_category):
    """Category-logits = logsumexp over the DISTRACTOR index of the member-marginal. (N, n_category)."""
    m = _member_marginal_logits(pool, X)                    # (N, n_B = n_distractor*n_category)
    m = m.view(X.shape[0], n_distractor, n_category)        # member b = distractor*n_category + category
    return torch.logsumexp(m, dim=1)                        # marginalise distractor -> (N, n_category)


def train_category_oracle(cfg, pin, *, alpha_spread, steps=600, lr=0.05, seed_offset=7000):
    """Fresh, capacity-open, A + CATEGORY-supervised encoder with SIGReg at the given strength.
    READ-ONLY (separate instance). Returns (enc, gen, alpha, P)."""
    g = torch.Generator().manual_seed(cfg.seed + seed_offset)
    stim = _make_conflict_stim(cfg)
    init_center = stim.centre.reshape(-1, cfg.D).mean(0)
    enc = VisionCortex(cfg.D, cfg.n_A, cfg.n_B, init_center=init_center, seed=cfg.seed + seed_offset)
    opt = torch.optim.Adam(enc.pool.parameters(), lr=lr)    # capacity forced open: lam1=lam2=0
    for _ in range(steps):
        a = torch.randint(0, cfg.n_A, (256,), generator=g)
        b = torch.randint(0, cfg.n_B, (256,), generator=g)
        c = b % cfg.n_category
        raw = stim.raw(a, b, g)
        coarse, _ = enc.pool(raw)
        cat_logits = _category_marginal_logits(enc.pool, raw, cfg.n_distractor, cfg.n_category)
        e = enc.emit(raw)                                  # p @ W (downstream of Delta2)
        loss = (F.cross_entropy(coarse, a) + F.cross_entropy(cat_logits, c)
                + alpha_spread * spread.spread_loss(e, pin.P, g))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return enc, g, alpha_spread, pin.P


@torch.no_grad()
def _category_recovery(enc, cfg, g, *, ablate_category: bool) -> float:
    """Nearest-centroid CATEGORY-recovery on the oracle's emissions (no free head). With
    ablate_category the category axis is zeroed (r_category=0) -> recovery must be ~chance."""
    stim = _make_conflict_stim(cfg, ablate_category=ablate_category)

    def emit(K):
        a = torch.randint(0, cfg.n_A, (K,), generator=g)
        b = torch.randint(0, cfg.n_B, (K,), generator=g)
        return enc.emit(stim.raw(a, b, g)), (b % cfg.n_category)

    es, cs = emit(max(512, cfg.n_A * cfg.n_B * 16))
    cen = torch.stack([es[cs == k].mean(0) for k in range(cfg.n_category)])
    ee, ce = emit(512)
    return (torch.cdist(ee, cen).argmin(1) == ce).float().mean().item()


def category_oracle_rec(cfg, pin, *, alpha_spread=None, steps=600) -> dict:
    """Substrate-oracle CATEGORY-recovery + content-ablation guard at the (default deployed)
    SIGReg strength. ``alpha_spread`` defaults to pin.alpha_spread (parity, read not re-specified)."""
    a_s = pin.alpha_spread if alpha_spread is None else alpha_spread
    enc, g, alpha, P = train_category_oracle(cfg, pin, alpha_spread=a_s, steps=steps)
    rec = _category_recovery(enc, cfg, g, ablate_category=False)
    abl = _category_recovery(enc, cfg, g, ablate_category=True)
    chance = 1.0 / cfg.n_category
    return dict(oracle_category_rec=rec, ablation_rec=abl,
                ablation_collapsed=bool(abl <= chance + ABLATION_MARGIN),
                alpha_spread=alpha, P=P, chance=chance,
                r_distractor=cfg.r_distractor, r_category=cfg.r_category,
                sigma_stim=cfg.sigma_stim)


@torch.no_grad()
def raw_axis_recovery(cfg, *, axis: str) -> float:
    """Cheap RAW (capacity-open, no training) nearest-centroid recovery of an axis from the raw
    stimulus — the salience bracket (analogous to validity_probe.ceiling_B). axis in
    {'distractor','category'}."""
    g = torch.Generator().manual_seed(cfg.seed + 4242)
    stim = _make_conflict_stim(cfg)
    n_cls = cfg.n_distractor if axis == "distractor" else cfg.n_category

    def sample(K):
        a = torch.randint(0, cfg.n_A, (K,), generator=g)
        b = torch.randint(0, cfg.n_B, (K,), generator=g)
        lab = (b // cfg.n_category) if axis == "distractor" else (b % cfg.n_category)
        return stim.raw(a, b, g), lab

    rs, ls = sample(max(1024, cfg.n_A * cfg.n_B * 32))
    cen = torch.stack([rs[ls == k].mean(0) for k in range(n_cls)])
    re, le = sample(1024)
    return (torch.cdist(re, cen).argmin(1) == le).float().mean().item()
