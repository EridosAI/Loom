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


def dynamics_panel(steps, values) -> dict:
    """The standing dynamics panel (ruled 2026-07-02): every gate artifact / run deliverable
    surfaces, per logged axis, {mean, amplitude, envelope, dominant period, trend} ALONGSIDE its
    windowed scalar — an average never ships alone. Pure summary over existing trajectories."""
    import statistics as _st
    pairs = [(s, v) for s, v in zip(steps, values) if v is not None]
    if not pairs:
        return dict(mean=None, amplitude=None, envelope=None, dominant_period_steps=None,
                    trend_per_1000=None, n=0)
    xs, vals = [p[0] for p in pairs], [p[1] for p in pairs]
    n = len(vals)
    mean = _st.mean(vals)
    lo, hi = min(vals), max(vals)
    trend = 0.0
    if n > 1:
        mx = _st.mean(xs)
        den = sum((x - mx) ** 2 for x in xs)
        if den:
            trend = sum((x - mx) * (v - mean) for x, v in zip(xs, vals)) / den * 1000.0
    period = None
    if n >= 8 and n > 1:
        c = [v - mean for v in vals]
        var = sum(x * x for x in c)
        if var > 0:
            ac = [sum(c[i] * c[i + l] for i in range(n - l)) / var for l in range(1, n // 2 + 1)]
            for l in range(1, len(ac) - 1):
                if ac[l] > ac[l - 1] and ac[l] >= ac[l + 1] and ac[l] > 0.2:
                    period = (l + 1) * (xs[1] - xs[0])
                    break
    return dict(mean=round(mean, 4), amplitude=round(hi - lo, 4),
                envelope=[round(lo, 4), round(hi, 4)],
                dominant_period_steps=period, trend_per_1000=round(trend, 4), n=n)


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


EPS = 1e-9    # matches dgate.EPS (the (d)-instrument's norm-guard)


def partition_read(evocations: torch.Tensor, labels: torch.Tensor, content: torch.Tensor,
                   *, denom_floor: float = 1e-3) -> dict:
    """THE pinned deployed-read statistic, ruler v2 (§L entry read; knob-register row 5).

    RULER SUPERSESSION (2026-07-02, pre-read, instrument-validity grounds — the convention's
    clean branch): v1's mean-centred-EVOCATION denominator is DEGENERATE on 2-associate
    geometry — within-class evocations are identical by construction, so the centred evocation
    set is {±d/2} and d_diff ≡ 2 at ANY scale (demonstrated: liveness_matched_bar v1, six
    orders of magnitude of raw separation all reading 1.995–2.000). Replaced pre-read.

    BINDING PROPERTIES (future variants [RECONCILE] against these, not the recipe):
      * numerator   = cross-class evoked separation (centring-invariant — common shifts cancel
        in differences; one less knob).
      * denominator = mean centred-CONTENT norm over the 16-item content population (neutral:
        the harness items; deployed: vision's LIVE emissions at read time), DETACHED, this one
        shared code path. Scale from a population with real spread (16 points, not 2):
        non-degenerate BY CONSTRUCTION, content-side, class-blind, self-normalizing across
        rigs; reduces ≈ to the neutral instrument at 16-cue (unit items, mean ≈ 0), so the
        0.8866/k=13 record stays consistent as the SCOPED 16-cue instrument — untouched, and
        not reusable.
      * d_same is STRUCK as a discriminator on 2-associate geometry (within-class evocations
        identical by construction → ≡ 0 for dead and healthy alike — never read zero as
        health). Reported for the record only; the ablation guard carries content-dependence
        alone (d_ablated = this function's d_diff on ablated-cue evocations).
      * denominator floor: sub-floor centred-content norm (early development, vision still
        undifferentiated) → status NOT_ASSESSABLE, d_diff None — never a number off a wild
        ratio. Callers log numerator / denominator / ratio as SEPARATE columns so the
        developmental regime stays interpretable.
    """
    labels = torch.as_tensor(labels, dtype=torch.long)
    M = evocations.shape[0]
    dm = torch.cdist(evocations, evocations)
    same = labels.unsqueeze(0) == labels.unsqueeze(1)
    off = ~torch.eye(M, dtype=torch.bool)
    cross_mask, within_mask = (~same) & off, same & off
    cross = dm[cross_mask].mean().item() if cross_mask.any() else 0.0
    within = dm[within_mask].mean().item() if within_mask.any() else 0.0
    c = content.detach()
    denom = (c - c.mean(dim=0)).norm(dim=1).mean().item()
    assessable = bool(denom >= denom_floor)
    return dict(
        d_diff=(cross / denom if assessable else None),
        status=("assessed" if assessable else "NOT_ASSESSABLE_DENOM_FLOOR"),
        d_same_struck=((within / denom) if assessable else None),
        cross_dist_raw=cross, within_dist_raw=within,
        content_denom=denom, denom_floor=denom_floor,
    )
