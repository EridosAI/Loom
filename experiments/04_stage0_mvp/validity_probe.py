"""Pre-loop stimulus-admissibility gate (Stage-0 §8). Run ONCE, before the loop. It gates
whether the factorial is admissible — it is NEVER a success signal (a passing probe says
nothing about whether the loop works).

Four checks, all must hold:
  1. A-salience    : a coarse-autonomous encoder differentiates A (high)        -> real decoy
  2. floor_B       : a coarse-autonomous encoder does NOT differentiate B (~chance)
  3. ceiling_B     : a capacity-open / raw-feature ORACLE recovers B (high), a DIFFERENT
                     regime, externally supervised on ground-truth B, no PAM / no live word
  4. separability  : cross-axis confusion (A<->B leakage) via prototype/centroid margins
                     (NOT a free linear head) < tau_sep

floor_B and ceiling_B are DIFFERENT regimes by design; their gap is the room gap-3 drives.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from encoders import VisionCortex                # noqa: E402
from stream import Stimulus                       # noqa: E402


def _nc_acc(emit, lab, n_cls, *, support, labels_support):
    """Nearest-centroid accuracy (no free head). Centroids from a disjoint support set."""
    cen = torch.stack([support[labels_support == c].mean(0) for c in range(n_cls)])
    return (torch.cdist(emit, cen).argmin(1) == lab).float().mean().item()


def _train_coarse_encoder(stim: Stimulus, cfg, *, steps=300, lr=0.05):
    """A coarse-AUTONOMOUS encoder: trained on the A (coarse) task with Delta2 frozen at 0
    -> resolves A but has NO B-resolution (the init regime that cannot find the subtle B)."""
    g = torch.Generator().manual_seed(cfg.seed + 555)
    init_center = stim.centre.reshape(-1, cfg.D).mean(0)
    enc = VisionCortex(cfg.D, cfg.n_A, cfg.n_B, init_center=init_center, seed=cfg.seed + 5)
    with torch.no_grad():
        enc.pool.delta2.zero_()
    params = [p for n, p in enc.named_parameters() if "delta2" not in n]
    opt = torch.optim.Adam(params, lr=lr)
    for _ in range(steps):
        a = torch.randint(0, cfg.n_A, (256,), generator=g)
        b = torch.randint(0, cfg.n_B, (256,), generator=g)
        raw = stim.raw(a, b, g)
        coarse_logits, _ = enc.pool(raw)
        loss = F.cross_entropy(coarse_logits, a)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        with torch.no_grad():
            enc.pool.delta2.zero_()                # keep B-resolution shut
        opt.step()
    return enc


def run_validity_probe(cfg, pin) -> dict:
    g = torch.Generator().manual_seed(cfg.seed + 4242)
    stim = Stimulus(cfg.D, cfg.n_A, cfg.n_B, R_coarse=cfg.R_coarse, r_fine=cfg.r_fine,
                    sigma=cfg.sigma_stim, seed=cfg.seed)
    coarse = _train_coarse_encoder(stim, cfg)

    def sample(K):
        a = torch.randint(0, cfg.n_A, (K,), generator=g)
        b = torch.randint(0, cfg.n_B, (K,), generator=g)
        return stim.raw(a, b, g), a, b

    raw_s, a_s, b_s = sample(cfg.n_A * cfg.n_B * 64)
    raw_e, a_e, b_e = sample(1024)
    with torch.no_grad():
        ec_s, ec_e = coarse.emit(raw_s), coarse.emit(raw_e)

    # checks 1 & 2: coarse-autonomous regime
    A_salience = _nc_acc(ec_e, a_e, cfg.n_A, support=ec_s, labels_support=a_s)
    floor_B = _nc_acc(ec_e, b_e, cfg.n_B, support=ec_s, labels_support=b_s)
    # check 3: capacity-open / RAW oracle (different regime; GT-supervised; no PAM/word)
    ceiling_B = _nc_acc(raw_e, b_e, cfg.n_B, support=raw_s, labels_support=b_s)
    A_oracle = _nc_acc(raw_e, a_e, cfg.n_A, support=raw_s, labels_support=a_s)
    # check 4: cross-axis confusion. A and B sit on disjoint subspaces, so a clean oracle
    # resolves BOTH; if either axis is NOT cleanly recoverable they are confounded. Confusion
    # = how far the worse axis falls short of clean recovery (prototype/margin, no free head).
    confusion = 1.0 - min(A_oracle, ceiling_B)

    gap = ceiling_B - floor_B
    checks = dict(
        A_salience=A_salience, floor_B=floor_B, ceiling_B=ceiling_B, A_oracle=A_oracle,
        floor_ceiling_gap=gap, cross_axis_confusion=confusion,
    )
    locked = bool(
        A_salience >= 0.8 and
        floor_B <= 1.0 / cfg.n_B + 0.10 and
        ceiling_B >= 0.8 and
        gap >= 0.25 and
        confusion < pin.tau_sep
    )
    checks["locked"] = locked
    checks["note"] = ("VALIDITY_OK (admissibility only — NOT loop success)" if locked
                      else "VALIDITY_GATE_FAILED")
    return checks
