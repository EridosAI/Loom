"""Characterisation-Sweep configuration — the pinned SPEC (hashed) + cfg transforms.

Two axes only (scope-lock): BAND (dense, from `band_ladder.json`) × UNPOOL-RATE (coarse, 2 constant
values). SLOW = schedule time-scaling (t1,t2,ramp_steps,steps,T × 1/slow_fraction) — NOT a
learning-rate change (that would be a scope-lock violation). Everything else is Phase-1 unchanged.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import replace
from pathlib import Path

import constants

HERE = Path(__file__).resolve().parent

SPEC = dict(
    rates={"MODERATE": 1.0, "SLOW": 0.5},     # slow_fraction; FAST dropped (scope-lock)
    n_seeds=20,                               # floor; seeds-as-instrument
    moderate_steps=14000, moderate_T=16000,   # > B00 T_run≈11300 (calibrated); SLOW = ×2
    eval_every=250,                           # ≥40 trajectory rows ≤ T_run (≈45 MOD / ≈90 SLOW)
    n_eval=256,
    ent_n=32,                                 # entanglement_r2 sample (max_coord_r2 build-invariant)
    plateau_frac=0.20, t95_level=0.95, t_run_factor=1.25,
    # phase bands in capacity_fraction — default quartiles; analyze adds a ±1-bin robustness check
    toe=[0.0, 0.25], rapid=[0.25, 0.75], plateau_band_frac=0.20,
    rapid_quantile=0.9,
    tol_plateau=0.05,                         # S-curve plateau-flatness tolerance [RECONCILE]
    n_consec=3, x_pct=0.20,                   # clean-G sustainedness (stricter-of-two)
    tau_entangle=0.90,                        # max_coord_r2 build-invariant (NOT full_ols_r2 — G3)
    # FROZEN verdict-classification thresholds (pre-registered BEFORE the surface exists; hashed
    # into spec_hash). Operationalize §8's qualitative terms over the seed distribution:
    verdict_sig_bar=0.30,        # s_curve_signature_frequency "materially >0" (≥6/20 seeds)
    verdict_f1_cutoff=0.10,      # F1 "flat": s_curve_signature_frequency ≤ this (≤2/20)
    verdict_clean_bar=0.30,      # cleanG_frequency "material" (≥6/20 seeds)
    verdict_auto_high=0.70,      # F2 "autonomous high at all bands"
)


def spec_hash() -> str:
    return hashlib.sha256(json.dumps(SPEC, sort_keys=True).encode()).hexdigest()[:12]


def commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(HERE), text=True).strip()
    except Exception:
        return "unknown"


def base_cfg(*, steps=None, T=None, eval_every=None, seed=0):
    """Stage0Config at the sweep's MODERATE run-length (band/rate applied on top)."""
    return constants.Stage0Config(
        steps=steps or SPEC["moderate_steps"], T=T or SPEC["moderate_T"],
        eval_every=eval_every or SPEC["eval_every"], n_eval=SPEC["n_eval"], seed=seed)


def band_cfg(base, cell):
    return replace(base, r_fine=cell["r_fine"], sigma_stim=cell["sigma_stim"])


def rate_cfg(cfg, rate):
    """SLOW = schedule time-scaling: t1,t2,ramp_steps,steps,T × 1/slow_fraction. ramp_steps scales
    too (keep gain-ramp/capacity-onset relation constant across rates). T stays > steps."""
    sc = 1.0 / SPEC["rates"][rate]
    return replace(cfg,
                   t1=int(round(cfg.t1 * sc)), t2=int(round(cfg.t2 * sc)),
                   ramp_steps=int(round(cfg.ramp_steps * sc)),
                   steps=int(round(cfg.steps * sc)), T=int(round(cfg.T * sc)))
