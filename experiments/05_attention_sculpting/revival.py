"""revival — the exp06/07 revival config's two primitives as ONE shared implementation
(STAGE1 spec Edit-3 binding; wired 2026-07-02, Gate-1/2 lineage 34fa8c4/fb9a27d).

Both the neutral (d)-gate path (exp07_core) and the deployed loop (SculptLoop) import THESE
functions — no parallel implementation whose equivalence would need its own proof (Guard 1).

  1. CONTENT-BLIND CUE RE-ORGANIZATION (global mean-centre form — the validated common-mode
     remover; the structured half is shelved, FRONTIER §10.9):
         reposed = cue - alpha * mu ,   mu = population mean over the member set (cls-independent
     constant at presentation). Provably adds no signal (pairwise diffs invariant) and cannot
     manufacture a floor (applied to a content-ablated cue population it yields identical cues).

  2. TWO-CLOCK PRESERVE TIE = the settled cortex StepSchedule (loom.pooling.StepSchedule)
     applied to PAM's pool penalty. lam1 (groups) and lam2 (capacity) each step hi->lo at an
     ABSOLUTE onset (t >= onset; budget-invariant). tie_schedule() constructs the cortex
     machinery from PENALTY_REGIMES-style fields, so the neutral rig's PenaltySpec and the
     deployed loop share the SAME step function by construction (same >= boundary semantics).

ONSET UNITS ([RECONCILE] — a named mapping, never a copied literal): onsets are steps of the
clock the consuming loop actually runs. The neutral rig's canonical budget is 12000 optimizer
steps -> 900/3600 (= 0.075/0.30 x 12000). The deployed loop's clock is the 4000-wave stream,
where the SAME fractions are the cortex's own onsets t1=300 / t2=1200 (they were derived from
it: 300/4000, 1200/4000). The PATTERN (absolute, two-clock, budget-invariant) is binding; the
literals do not transfer across clocks.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "src"))

from loom.pooling import StepSchedule                        # noqa: E402  (the settled machinery)


def population_mean(cues: torch.Tensor) -> torch.Tensor:
    """mu = content-blind population mean over the member set: (M, D) -> (D,). A single constant
    vector, independent of which member/association is masked (the content-blindness guard)."""
    return cues.mean(dim=0)


def repose(x: torch.Tensor, mu: torch.Tensor, alpha: float) -> torch.Tensor:
    """Global mean-centre re-organization: x - alpha*mu. alpha=0 -> untouched (the flat-diffuse
    disease baseline); alpha=1 -> fully common-mode centered (the validated revival form)."""
    return x - alpha * mu


def tie_schedule(*, lam1_hi: float, lam1_lo: float, t1_step: int,
                 lam2_hi: float, lam2_lo: float, t2_step: int) -> StepSchedule:
    """The preserve tie as the cortex StepSchedule (same class, same >= onset semantics).
    NOTE StepSchedule's positional order is (lam1_hi, lam1_lo, lam2_hi, lam2_lo, t1, t2)."""
    return StepSchedule(lam1_hi, lam1_lo, lam2_hi, lam2_lo, t1_step, t2_step, activity_gate=1.0)
