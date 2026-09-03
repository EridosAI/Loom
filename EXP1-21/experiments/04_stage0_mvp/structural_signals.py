"""Two structural live signals (Stage-0 §9, Phase 1).

#1 char-7: use(complete) + adjust(step) in ONE pass, no train/run branch anywhere — a static
   scan of the wave-loop source plus a runtime single-step assertion. PASS = no phase split.
#2 pooling visibly does something: under the fixed unpool clock, capacity opens AND members
   differentiate (substrate live, not inert) — distinct from whether the word taught it.
"""

from __future__ import annotations

from pathlib import Path

from verdict import Verdict, Outcome

# Tokens that would indicate a train/run phase split governing the wave loop's behaviour.
_FORBIDDEN = (".eval()", ".train()", "self.training", "if train", "is_train",
              "phase ==", "mode ==")


def char7_no_phase_split(loop) -> Verdict:
    src = (Path(__file__).resolve().parent / "loop.py").read_text()
    # restrict to the wave-loop critical path: build_cells, _l_pam, step
    hits = [tok for tok in _FORBIDDEN if tok in src]
    # runtime single-step assertion: one optimiser step per wave (the loop calls opt.step once)
    n0 = _opt_step_count(loop)
    loop.step()
    one_step = (_opt_step_count(loop) - n0) == 1
    ok = (not hits) and one_step
    return Verdict(
        Outcome.PASS if ok else "FAIL-PHASE_SPLIT",
        dict(forbidden_tokens=hits, one_step_per_wave=one_step),
        notes=("char-7 holds: single code path, one complete-then-step per wave"
               if ok else f"phase split detected: {hits or 'multiple steps per wave'}"),
    )


def _opt_step_count(loop):
    # Adam stores per-parameter state after the first step; count global steps via the
    # optimiser's state_dict step counter on the first parameter.
    st = loop.opt.state_dict()["state"]
    return int(next(iter(st.values()))["step"].item()) if st else 0


def pooling_does_something(depth_history, spread_history, pin) -> Verdict:
    """Members differentiate = the per-member residual (Delta2, i.e. ``pooling_depth``) opens
    from the pooled state. ``pooling_depth`` is the faithful signal; ``within_group_spread``
    (pairwise member-WEIGHT distance) is confounded by the §5 isotropy term, so a flat/falling
    spread while depth opens is the SPREAD_FIGHTS_POOLING observation, not substrate inertia."""
    opened = depth_history[-1] >= pin.L_capacity
    differentiated = depth_history[-1] > depth_history[0] * 3.0       # Delta2 opened from pooled
    spread_fights_pooling = spread_history[-1] <= spread_history[0] and opened
    ok = opened and differentiated
    notes = ("substrate live: capacity opened (Delta2 grew %.0fx from pooled)"
             % (depth_history[-1] / max(depth_history[0], 1e-6))) if ok else \
            "substrate inert: Delta2 did not open from the pooled state"
    if spread_fights_pooling:
        notes += " | OBSERVATION: SPREAD_FIGHTS_POOLING (within-group spread flat/falling while"
        notes += " capacity opens — §5 attribution-watch; interpose a throwaway projector in a follow-up)"
    return Verdict(
        Outcome.PASS if ok else "FAIL-SUBSTRATE_INERT",
        dict(depth_start=round(depth_history[0], 5), depth_end=round(depth_history[-1], 5),
             L_capacity=pin.L_capacity, spread_start=round(spread_history[0], 5),
             spread_end=round(spread_history[-1], 5), spread_fights_pooling=spread_fights_pooling),
        notes=notes,
    )
