"""Pre-registered readouts (Stage-0 §9). Phase-1 live: Readout G (gap-3 fusion) and
Readout D (order-as-content in loop). Each shares the exp03 format — a logged primary vs an
independent weaker baseline, an ablation gate that defeats the confound, and named pass/fail
shapes encoded as a data table. A clean primary with the baseline-gap absent is a wrong-reason
pass and is FLAGGED, never celebrated.
"""

from __future__ import annotations

from verdict import Verdict, Outcome, score_against_table


# ----------------------------------------------------------------- conditioning helpers
def b_success(b_track_history, floor_B, ceiling_B, pin) -> bool:
    """B_track >= floor_B + k*(ceiling_B-floor_B) for N consecutive eval windows."""
    bar = floor_B + pin.k * (ceiling_B - floor_B)
    recent = b_track_history[-pin.N:]
    return len(recent) >= pin.N and all(v >= bar for v in recent)


def in_floor_band(b_track, floor_B, pin) -> bool:
    return b_track <= floor_B + pin.eps_band


# ----------------------------------------------------------------- Readout G (gap-3 fusion)
def _clean_gap3_window(b_hist, no_word_hist, bar, floor_hi, sustain=2):
    """Time-qualified gap-3 signature: a SUSTAINED run (>= ``sustain`` consecutive eval
    windows) where the word arm cleared the success bar WHILE the matched no-word arm stayed
    in the floor-band — read PAIRED and sustained (a single-window unpaired gap flips on the
    no-word arm's eval noise, e.g. seed 1's inversion). The clean signature is time-qualified
    because autonomous B-resolution is LATE: it can appear early then be caught up."""
    clean = [bool(w >= bar and nw <= floor_hi) for w, nw in zip(b_hist, no_word_hist)]
    run = best = best_end = 0
    for i, c in enumerate(clean):
        run = run + 1 if c else 0
        if run > best:
            best, best_end = run, i
    if best >= sustain:
        return dict(found=True, start=best_end - best + 1, end=best_end, length=best)
    return dict(found=False, start=None, end=None, length=best)


def readout_G(b_track_history, no_word_b_track_history, A_track, floor_B, ceiling_B,
              capacity_open: bool, contrast_available: bool, separable: bool, pin) -> Verdict:
    bar = floor_B + pin.k * (ceiling_B - floor_B)
    floor_hi = floor_B + pin.eps_band
    gap3 = _clean_gap3_window(b_track_history, no_word_b_track_history, bar, floor_hi)
    cond = dict(
        capacity_open=capacity_open, contrast_available=contrast_available, word_present=True,
        separable=separable,
        clean_gap3_window=gap3["found"], gap3_window=(gap3["start"], gap3["end"]),
        B_success=b_success(b_track_history, floor_B, ceiling_B, pin),
        B_in_floor_band=in_floor_band(b_track_history[-1], floor_B, pin),
        no_word_in_floor_band=in_floor_band(no_word_b_track_history[-1], floor_B, pin),
        A_high=A_track >= 0.8,
        B_bar=round(bar, 3),
        B_track=round(b_track_history[-1], 3),
        no_word_B_track=round(no_word_b_track_history[-1], 3),
        floor_B=round(floor_B, 3), ceiling_B=round(ceiling_B, 3),
    )
    rows = [
        ("INVALID", lambda c: not c["separable"],
         "A/B not separable — B-rise unattributable, re-gate the stimulus"),
        ("PASS-TIME-QUALIFIED", lambda c: c["clean_gap3_window"],
         "gap-3 ISOLATED in a sustained window: the word arm cleared the bar while the matched "
         "no-word arm stayed in the floor-band (before autonomous resolution caught up). "
         "Time-qualified — autonomous B-discovery is late"),
        (Outcome.BOUNDARY, lambda c: not c["capacity_open"] or not c["contrast_available"],
         "preconditions for gap-3 not yet met (capacity/contrast pending) — data/maturation floor"),
        (Outcome.PASS, lambda c: c["B_success"],
         "gap-3 working: vision acquired a distinction it cannot find autonomously"),
        ("FAIL-capture-instead-of-acquisition",
         lambda c: c["B_in_floor_band"] and c["A_high"],
         "freed capacity captured by A instead of acquiring B"),
        (Outcome.NORMAL, lambda c: not c["B_in_floor_band"],
         "B rising above floor but not yet sustained B_success — acquisition underway"),
        (Outcome.BOUNDARY, lambda c: True,
         "B in floor-band with capacity+contrast present — not (yet) acquired"),
    ]
    # Stage-3 guard: at the ENDPOINT B rose in the intact arm BUT the matched no-word arm ALSO
    # rose — word didn't cleanly teach it. Does NOT fire if a clean time-qualified window exists
    # (an early clean isolation is real even if endpoint attribution later muddies).
    def wrong(c):
        return (not c["clean_gap3_window"] and c["capacity_open"] and c["contrast_available"]
                and c["word_present"] and not c["B_in_floor_band"] and not c["no_word_in_floor_band"])
    return score_against_table(rows, cond, wrong_reason_predicate=wrong)


# ----------------------------------------------------------------- Readout D (order-as-content)
def readout_D(order_recovery, carrier_zero, chance, max_coord_r2, full_ols_r2,
              oracle_well_ordered, pin, *, scale_recovery_trend=None) -> Verdict:
    """Two entanglement gates, BOTH must hold for the strong (entangled) claim:
      * ``max_coord_r2 < tau_entangle``  — no clean axis-aligned SLOT (single-coordinate);
      * ``full_ols_r2  < tau_full_ols``  — no FULL-linear read (exp03's criterion; exp03 hit
        0.80 at alpha=1). Single-coord alone passes a carrier that is spread across coordinates
        yet still linearly trivial — exactly what the dwell-stable fix induces (drift becomes
        the only within-window variation). carrier-zero collapse is necessary-but-NOT-sufficient
        (it fires for a separable index too), so it cannot certify entanglement on its own.
    """
    recovers = order_recovery >= chance + 0.10
    carrier_collapses = carrier_zero <= chance + pin.ablate_margin
    clean_slot = max_coord_r2 >= pin.tau_entangle           # a single coordinate carries it
    linearly_separable = full_ols_r2 >= pin.tau_full_ols    # a full linear read recovers it
    cond = dict(
        order_recovery=round(order_recovery, 3), carrier_zero=round(carrier_zero, 3),
        chance=round(chance, 3), max_coord_r2=round(max_coord_r2, 3),
        full_ols_r2=round(full_ols_r2, 4), recovers=recovers,
        carrier_collapses=carrier_collapses, clean_slot=clean_slot,
        linearly_separable=linearly_separable, oracle_well_ordered=round(oracle_well_ordered, 3),
    )
    rows = [
        ("INVALID-CARRIER_SLOT", lambda c: c["clean_slot"],
         "live carrier has a clean axis-aligned slot (single-coord R^2 >= tau_entangle) — order-as-index"),
        ("FAIL-CONTENT_MEMORIZATION", lambda c: c["recovers"] and not c["carrier_collapses"],
         "order 'recovered' but carrier-zero did not collapse it — operator content-memorized, not reading order"),
        ("PASS-LINEAR-REGIME", lambda c: c["recovers"] and c["carrier_collapses"] and c["linearly_separable"],
         "order recovered in-loop and carrier-zero collapses it (REAL), but the carrier is in the "
         "LINEARLY-SEPARABLE regime (full_ols_r2 >= tau_full_ols) — validates order-IN-LOOP, NOT the "
         "entangled order-as-content corner (exp03 hit 0.80 at alpha=1). Dwell-stable content removed "
         "the along-u content variation; the entangled corner is DEFERRED"),
        (Outcome.PASS, lambda c: c["recovers"] and c["carrier_collapses"],
         "order-as-content recovered in-loop; carrier-zero collapses it AND the carrier is genuinely "
         "entangled (full-linear read < tau_full_ols)"),
        (Outcome.BOUNDARY, lambda c: not c["recovers"],
         "order not recovered above chance — data/maturation floor"),
    ]
    v = score_against_table(rows, cond)
    if scale_recovery_trend is not None and scale_recovery_trend < -0.05:
        v.notes += " | WATCH: scale-sensitivity — order_recovery declines as cumulative drift grows"
    return v
