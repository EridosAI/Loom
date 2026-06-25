"""Pinned constants (Stage-0 §10) + the run config.

ALL of {k, eps_band, N, tau_sep, tau_entangle, P, alpha_spread, L_capacity, K_settle}
are pinned-and-logged BEFORE the run — none chosen after seeing results (exp03 selected
sigma*/band before training). Nothing here may be mutated once a run begins.

Two distinct separability bars are kept apart (they were folded as one 'tau_sep' in the
plan): ``tau_sep`` = the validity-probe cross-axis confusion bar; ``tau_entangle`` = the
live-carrier entanglement ceiling (linear_separability_r2(mixture) must stay BELOW it,
else CARRIER_SEPARABLE — order regressed to index).
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field


@dataclass(frozen=True)
class PinnedConstants:
    # headline Readout-G bars (confirm before run)
    k: float = 0.5                 # B_success gap fraction: floor + k*(ceiling-floor)
    eps_band: float = 0.10         # floor-band tolerance (no-word arm must stay <= floor+eps)
    N: int = 5                     # consecutive eval windows for sustained B_success
    tau_sep: float = 0.35          # validity check-4 cross-axis confusion bar
    # entanglement / order
    tau_entangle: float = 0.90     # live mixture max single-COORD R^2 must stay below (clean-slot gate)
    tau_full_ols: float = 0.90     # live mixture FULL-linear-read R^2 must stay below (exp03's
                                   # entanglement criterion: exp03 hit 0.80 at alpha=1). Single-coord
                                   # alone only catches an axis-aligned slot; this catches the
                                   # spread-but-linearly-trivial regime the dwell-stable fix induces.
    ablate_margin: float = 0.10    # Readout D: carrier-zero begin-id <= chance_floor + this
    iter_eps: float = 0.05         # at-once: k_pass - 1_pass <= this
    # collapse-control / spread
    P: int = 64                    # random 1-D projections for the spread term
    alpha_spread: float = 0.1      # spread/completion balance in L_total
    # capacity
    L_capacity: float = 0.05       # capacity_open: vision pooling_depth >= this (calibrated to
                                   # post-unpool depth ~0.08; pooled baseline ~0.003 -> ~23x)
    K_settle: int = 1              # operator settle cap (1 = single at-once act, run 1)
    # re-pool (exp01)
    repool_frac: float = 0.15
    repool_patience: int = 4
    repool_ramp: int = 400

    def logged(self) -> dict:
        return asdict(self)


@dataclass
class Stage0Config:
    # stimulus / cortices
    D: int = 16
    n_A: int = 4
    n_B: int = 4
    R_coarse: float = 5.0          # A (decoy) on coarse axes — salient but not so large its
    r_fine: float = 2.5            # centroid sampling-noise swamps the B-signal; B (probe) on
    sigma_stim: float = 0.20       # disjoint fine axes, recoverable by oracle but not by pooling
    # stream
    W: int = 3
    n_slots: int = 2
    sigma_drift: float = 0.8       # the order-carrier band (validity-probe selects/confirms)
    slope: float = 0.7
    dwell_extra: int = 4
    entangle_nuisance_frac: float = 0.6  # kappa_c/kappa: continuous content confound on u
                                         # (guarantees no-clean-slot regardless of content state)
    T: int = 6000                  # total waves in the stream
    # operator
    d_model: int = 64
    pam_groups: int = 8
    pam_members: int = 4
    n_freq: int = 12
    # pooling clock (vision); activity_gate pinned to 1
    lam1_hi: float = 10.0
    lam1_lo: float = 0.0
    lam2_hi: float = 10.0
    lam2_lo: float = 0.0
    t1: int = 300                  # unpool to A-groups
    t2: int = 1200                 # unpool to full (B) resolution -> capacity_open
    pam_lam: float = 0.01          # PAM substrate light fixed penalty (full resolution)
    # gain ramp
    gain_max: float = 1.0
    ramp_steps: int = 400
    # curriculum
    curric_threshold: float = 0.6
    curric_start_active: int = 2
    # optimisation / run
    lr: float = 3e-3
    steps: int = 4000              # total wave steps
    spread_batch: int = 64
    eval_every: int = 100
    n_eval: int = 256
    seed: int = 0

    def logged(self) -> dict:
        return asdict(self)


def quick_config(**over) -> Stage0Config:
    """Small CPU-deterministic smoke config (minutes)."""
    cfg = Stage0Config(
        T=2500, t1=120, t2=400, ramp_steps=150, steps=1500,
        eval_every=150, n_eval=128, spread_batch=48,
    )
    for k, v in over.items():
        setattr(cfg, k, v)
    return cfg
