"""The §10 minimum-logging block: one record per eval window, consumed by every readout.

Includes the build-failure checks (word-encoder parameter-delta ~ 0; gradient attribution
split with both vision-from-JEPA and vision-from-PAM nonzero = gap-3 alive) and the live
carrier-entanglement check (max single-coordinate R^2 must stay below tau_entangle).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from loom import order  # noqa: E402


@dataclass
class LoggedWindow:
    step: int
    gain: float
    lam2: float
    # losses
    l_pam: float = 0.0
    l_jepa: float = 0.0
    l_spread: float = 0.0
    spread_completion_ratio: float = 0.0
    loss_by_mask_family: dict = field(default_factory=dict)
    # build-failure invariants
    word_param_delta: float = 0.0
    vision_grad_from_PAM: float = 0.0
    vision_grad_from_JEPA: float = 0.0
    # substrate
    pooling_depth: float = 0.0
    within_group_spread: float = 0.0
    pull_apart: float = 0.0
    # tracks
    A_track: float = 0.0
    B_track: float = 0.0
    A_chance: float = 0.0
    B_chance: float = 0.0
    no_word_B_track: float = float("nan")
    # order diagnostics
    max_coord_r2: float = 0.0
    full_ols_r2: float = 0.0
    adjacent_overlap: float = 0.0
    sigma_drift: float = 0.0
    order_recovery: float = 0.0
    carrier_zero: float = 0.0
    order_chance: float = 0.0
    # operator settling
    relaxation_residual: float = float("nan")  # N/A if K_settle <= 1
    # curriculum
    curriculum_state: list = field(default_factory=list)
    contrast_available: bool = False

    def as_dict(self):
        return asdict(self)


def assemble(loop, step_result: dict, family_losses: dict, *, n_eval: int) -> LoggedWindow:
    """Compute the full logging block from a loop at the current step (eval cadence)."""
    cfg, pin = loop.cfg, loop.pin
    tr = loop.b_a_track(n_eval)
    ga = loop.grad_attribution()
    ent = loop.entanglement_r2(min(64, n_eval))
    ps = loop.pooling_stats()
    pb = loop.position_begin_id(min(160, n_eval))
    dv = order.drift_validity(cfg.sigma_drift, L=cfg.W)
    sc_ratio = (step_result["l_spread"] / step_result["l_pam"]
                if step_result["l_pam"] > 1e-9 else float("inf"))
    return LoggedWindow(
        step=loop._t, gain=step_result["gain"], lam2=step_result["lam2"],
        l_pam=step_result["l_pam"], l_jepa=step_result["l_jepa"],
        l_spread=step_result["l_spread"], spread_completion_ratio=sc_ratio,
        loss_by_mask_family=dict(family_losses),
        word_param_delta=loop.word.param_delta(),
        vision_grad_from_PAM=ga["vision_grad_from_PAM"],
        vision_grad_from_JEPA=ga["vision_grad_from_JEPA"],
        pooling_depth=ps["pooling_depth"], within_group_spread=ps["within_group_spread"],
        pull_apart=ps["pull_apart"],
        A_track=tr["A_track"], B_track=tr["B_track"],
        A_chance=tr["A_chance"], B_chance=tr["B_chance"],
        max_coord_r2=ent["max_coord_r2"], full_ols_r2=ent["full_ols_r2"],
        adjacent_overlap=dv["adjacent_overlap"], sigma_drift=cfg.sigma_drift,
        order_recovery=pb["intact_begin"], carrier_zero=pb["carrier_zero_begin"],
        order_chance=pb["chance_floor"],
        relaxation_residual=(float("nan") if pin.K_settle <= 1 else 0.0),
        curriculum_state=loop.curric.state(), contrast_available=loop.curric.contrast_available,
    )
