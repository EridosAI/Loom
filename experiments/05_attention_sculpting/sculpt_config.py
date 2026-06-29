"""Stage-1 config: extends Stage0Config with the conflict stimulus + constant Delta2 re-pool.

SculptConfig is a strict superset of Stage0Config (every Phase-1 field inherited unchanged).
The four new things (SPEC §0) live here:
  * conflict stimulus cardinalities + salience (n_distractor/n_category, r_distractor/r_category),
  * ``repool_rate`` — the constant intrinsic Delta2-decay rate (G3; 0 = off; pinned slow for stage-1),
  * timing onset ``t2`` is inherited (the swept knob is the unpool clock; SPEC §3),
and ``n_B`` is DERIVED = n_distractor*n_category in __post_init__ (the crossed member space).

Backward note: with conflict params at their defaults but driven through SculptLoop, the rig is the
conflict rig. Phase-1 Stage0Config/Stage0Loop are untouched and still reproduce the [SETTLED] sweep.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, asdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

import constants  # noqa: E402  (exp04)


@dataclass
class SculptConfig(constants.Stage0Config):
    # --- conflict stimulus (SPEC §2) ---
    # n_A coarse decoy "base objects"; each member = (distractor, category) crossed fine axes.
    n_A: int = 4
    n_distractor: int = 2            # salient, associatively INERT split (vision sees these)
    n_category: int = 2             # subtle, word-NAMED partition (the load-bearing axis)
    r_distractor: float = 3.0       # distractor fine-axis magnitude (HIGH salience; r/sigma=15)
    r_category: float = 0.5         # category fine-axis magnitude (LOWER salience; r/sigma=2.5,
                                    # oracle-representable but subtle to pooled vision); ladder sweeps this
    # --- constant intrinsic re-pool on occupancy (SPEC §5, G3) ---
    repool_rate: float = 0.0        # per-step Delta2 decay-toward-group-mean fraction (0 = off)

    def __post_init__(self):
        # member space = crossed axes; word vocab = category (set in SculptLoop._make_word).
        self.n_B = self.n_distractor * self.n_category

    @property
    def conflict_strength(self) -> float:
        """How far distractor salience exceeds category salience (the swept dense axis)."""
        return self.r_distractor / max(1e-9, self.r_category)

    def logged(self) -> dict:
        d = asdict(self)
        d["conflict_strength"] = self.conflict_strength
        return d


def quick_sculpt(**over) -> SculptConfig:
    """Small CPU-deterministic smoke config (minutes)."""
    cfg = SculptConfig(
        T=2500, t1=120, t2=400, ramp_steps=150, steps=1500,
        eval_every=150, n_eval=128, spread_batch=48,
    )
    for k, v in over.items():
        setattr(cfg, k, v)
    # keep n_B consistent if cardinalities were overridden
    cfg.n_B = cfg.n_distractor * cfg.n_category
    return cfg
