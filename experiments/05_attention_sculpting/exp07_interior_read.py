"""exp07 INTERIOR READ (POST-GATE; Step-0 reviewed + signed off 2026-06-30). Deterministic §3 read
over the raw surface, using the SEED-STABLE, plateau-confirmed ceilings from exp07_ceiling_*.json
(the surface's 5-seed/12000 ceilings were unstable: std 0.47-0.55, bimodal). NEUTRAL — no
penalty-primary lens; liveness binary at live_bar + ablation; floors/topology are characterisation.

Per the user's directives (2026-06-30):
  * extend alive ceiling cells -> use exp07_ceiling_*.json (10 seeds, to 18000, tail-plateau checked);
  * floors reported WITH UNCERTAINTY and CLAMPED at 0 (>=0 = fully recoverable, never negative);
  * full card-2 surface for TOPOLOGY-INVARIANCE (compare the card-2 topology to card-16);
  * SEED-RECONFIRM a marginal legitimacy call (the reconfirm IS the seed-bump; a difference within
    2*combined-sem after that is reported as not-significant -> lean preserve, flagged honestly);
  * PHASING re-check ARMED on reshaped < off (reads reshaped @ all onsets; preserve holds if it
    recovers to ~/better than off at any onset, else the reversal locks).

irreducible floor = (column's own sharp alive-reference) - C ; recoverable/inflated = C - flat baseline.
"""

from __future__ import annotations

import json
from pathlib import Path

import exp07_config as C

_HERE = Path(__file__).resolve().parent
LIVE_BAR = C.LIVE_BAR
ABL_FLOOR = C.ABLATION_FLOOR
MARGIN = C.CUE_PLATEAU_MARGIN          # 0.10
SEM_K = 2.0                            # significance band for the legitimacy call


def _load(name, required=True):
    p = _HERE / name
    if not p.exists():
        if required:
            raise SystemExit(f"missing {name} — run exp07_surface.py / exp07_ceiling_reconfirm.py first.")
        return None
    return json.load(open(p))


# ---- merged reconfirmed-ceiling lookup (absolute-onset reconfirm; 10 seeds; to 30000) ----
# conv_* (off/reshaped card-16 ceilings converged to 36000) override A/B for the deciding cells.
_RECON = {}
for g in ("A", "B", "C", "P1", "P2", "conv_off", "conv_reshaped"):
    d = _load(f"exp07_ceiling_{g}.json", required=False)
    if d:
        _RECON.update(d["cells"])


def _surface_cell(columns, col, label):
    v = columns[col][label]
    dd = v["d_diff"]
    return dict(mean=dd["mean"], std=dd["std"], sem=dd["std"] / max(1, len(dd["per_seed"])) ** 0.5,
                per_seed=dd["per_seed"], ablated_max=v["d_ablated"]["max"], plateaued=None,
                source="surface")


def _recon_cell(key):
    r = _RECON[key]
    return dict(mean=r["ceiling_mean"], std=r["ceiling_std"], sem=r["ceiling_sem"],
                per_seed=r["ceiling_per_seed"], ablated_max=r["ablated_max"],
                plateaued=r["plateaued"], source=f"reconfirm@{r['ceiling_step']}")


def _ceiling(card, col, recon_key, columns):
    """Prefer the reconfirmed (extended, seed-stable) ceiling; fall back to the surface alpha=1.0 cell."""
    if recon_key and recon_key in _RECON:
        return _recon_cell(recon_key)
    return _surface_cell(columns, col, "repose@1")


def _sharp(card, col, recon_key, columns):
    if recon_key and recon_key in _RECON:
        return _recon_cell(recon_key)
    return _surface_cell(columns, col, "sharp")


def _floor(ruler_mean, ruler_sem, ceil):
    """irreducible floor = max(0, RULER - C), with uncertainty; clamped at 0 (>=0 = fully recoverable,
    never negative). RULER = the off-column sharp alive-reference (the §1 'unreachable ruler'), common
    to all columns so the uniformly-dead deployed column reads a MAXIMAL floor (own-sharp=0 would read
    a degenerate 0)."""
    raw = ruler_mean - ceil["mean"]
    sem = (ruler_sem ** 2 + ceil["sem"] ** 2) ** 0.5
    return dict(value=round(max(0.0, raw), 4), raw=round(raw, 4), uncertainty=round(sem, 4),
                fully_recoverable=bool(raw <= MARGIN))


def _revives(ceil):
    return bool(ceil["mean"] >= LIVE_BAR and ceil["ablated_max"] <= ABL_FLOOR)


def _column_read(card, col, columns, ceil_key, sharp_key, ruler_mean, ruler_sem):
    flat = columns[col]["flat"]["d_diff"]["mean"]
    ceil = _ceiling(card, col, ceil_key, columns)
    own_sharp = _sharp(card, col, sharp_key, columns)        # column's own sharp (deployed's is dead)
    floor = _floor(ruler_mean, ruler_sem, ceil)              # vs the common off-sharp ruler
    own_raw = own_sharp["mean"] - ceil["mean"]
    return dict(
        flat_baseline=round(flat, 4),
        ceiling_C=round(ceil["mean"], 4), ceiling_std=round(ceil["std"], 4),
        ceiling_sem=round(ceil["sem"], 4), ceiling_per_seed=ceil["per_seed"],
        ceiling_plateaued=ceil["plateaued"], ceiling_source=ceil["source"],
        own_sharp=round(own_sharp["mean"], 4), own_sharp_source=own_sharp["source"],
        own_sharp_floor=round(max(0.0, own_raw), 4),
        recoverable_inflated=round(ceil["mean"] - flat, 4),
        irreducible_floor=floor, revives=_revives(ceil),
        ablation_collapses=bool(ceil["ablated_max"] <= ABL_FLOOR))


def _topology(floors):
    fo, fr, fd = floors["off"], floors["reshaped"], floors["deployed"]
    vals = [fo, fr, fd]
    spread = max(vals) - min(vals)
    order = {"off": fo, "reshaped": fr, "deployed": fd}
    mn = min(order, key=order.get)
    if spread <= MARGIN:
        return dict(klass="separable", min_regime=mn, spread=round(spread, 4))
    if fo >= fr >= fd or fo <= fr <= fd:
        return dict(klass="monotonic", min_regime=mn, spread=round(spread, 4))
    return dict(klass=f"sweet-spot@{mn}", min_regime=mn, spread=round(spread, 4))


def main():
    main_raw = _load("exp07_surface_raw.json")
    low_raw = _load("exp07_lowcard_raw.json")
    phas_raw = _load("exp07_phasing_raw.json")
    cols16, cols2 = main_raw["columns"], low_raw["columns"]

    # ---------- card-16 read ----------
    ruler16 = _sharp(16, "off", "16/off/sharp", cols16)       # the off-sharp alive-reference ruler
    reads16 = {
        "off":      _column_read(16, "off", cols16, "16/off/repose@1.0", "16/off/sharp",
                                 ruler16["mean"], ruler16["sem"]),
        "reshaped": _column_read(16, "reshaped", cols16, "16/reshaped@0.3/repose@1.0",
                                 "16/reshaped@0.3/sharp", ruler16["mean"], ruler16["sem"]),
        "deployed": _column_read(16, "deployed", cols16, None, None, ruler16["mean"], ruler16["sem"]),
    }
    floors16 = {k: reads16[k]["irreducible_floor"]["value"] for k in reads16}
    topo16 = _topology(floors16)

    # ---------- card-2 read (topology-invariance) ----------
    ruler2 = _sharp(2, "off", "2/off/sharp", cols2)          # off-sharp@2 (reconfirmed; lowcard fallback)
    reads2 = {
        "off":      _column_read(2, "off", cols2, "2/off/repose@1.0", "2/off/sharp",
                                 ruler2["mean"], ruler2["sem"]),
        "reshaped": _column_read(2, "reshaped", cols2, "2/reshaped@0.3/repose@1.0",
                                 "2/reshaped@0.3/sharp", ruler2["mean"], ruler2["sem"]),
        "deployed": _column_read(2, "deployed", cols2, None, None, ruler2["mean"], ruler2["sem"]),
    }
    floors2 = {k: reads2[k]["irreducible_floor"]["value"] for k in reads2}
    topo2 = _topology(floors2)
    topology_invariant = bool(topo16["klass"].split("@")[0] == topo2["klass"].split("@")[0])

    # ---------- penalty-legitimacy adjudication: preserve(reshaped) vs drop/correct-it(off) ----------
    # Two SEPARATE quantities (user reframe 2026-06-30):
    #   * cue-FLOOR equivalence (the deliverable): own-sharp - C per column. If off ~= reshaped on the
    #     floor, the floor does NOT decide preserve-vs-drop -- they are FLOOR-EQUIVALENT.
    #   * UNIFORM capacity cost of the tie: sharp_off - sharp_reshaped (a uniform offset, NOT a cue-floor
    #     cost). This is FOLDED INTO the legitimacy call (preserve-vs-drop), NOT into the cue-floor number.
    #     Measured at both cards to expose SCALE-dependence.
    # Verdict is therefore "preserve on the UNIFORMITY argument (architectural uniformity with the
    # cortices, spec 0 lock 1); floor-equivalent with drop; small scale-growing capacity cost" -- NOT
    # "validated" (the floor doesn't select preserve; uniformity does, at a measured price).
    off_c, resh_c = reads16["off"], reads16["reshaped"]
    Co, Cr = off_c["ceiling_C"], resh_c["ceiling_C"]
    Fo, Fr = off_c["own_sharp_floor"], resh_c["own_sharp_floor"]   # own-sharp ruler
    Fo_common = off_c["irreducible_floor"]["value"]               # common off-sharp ruler (top-level)
    Fr_common = resh_c["irreducible_floor"]["value"]
    delta = Co - Cr

    # paired significance (same seed indices -> paired). The robust deliverable is the CEILING gap;
    # the sharp-gap that would justify calling the cost a 'separable uniform offset' is checked too.
    def _paired(a, b):
        if not a or not b or len(a) != len(b):
            return None
        diffs = [x - y for x, y in zip(a, b)]
        n = len(diffs); m = sum(diffs) / n
        sd = (sum((x - m) ** 2 for x in diffs) / (n - 1)) ** 0.5 if n > 1 else 0.0
        t = (m / (sd / n ** 0.5)) if sd > 0 else float("inf")
        npos = sum(1 for x in diffs if x > 0)
        return dict(mean_diff=round(m, 4), t=round(t, 3), n=n, sign_split=f"{npos}/{n - npos}",
                    significant=bool(abs(t) >= 2.0))
    ceil_paired_16 = _paired(off_c["ceiling_per_seed"], resh_c["ceiling_per_seed"])
    ceil_paired_2 = _paired(reads2["off"]["ceiling_per_seed"], reads2["reshaped"]["ceiling_per_seed"])
    sharp_paired_16 = _paired(_RECON.get("16/off/sharp", {}).get("ceiling_per_seed"),
                              _RECON.get("16/reshaped@0.3/sharp", {}).get("ceiling_per_seed"))

    cap_cost_16 = round(delta, 4)                                  # ROBUST cost = the ceiling gap
    cap_cost_2 = round(reads2["off"]["ceiling_C"] - reads2["reshaped"]["ceiling_C"], 4)
    scale_growing = bool((ceil_paired_16 and ceil_paired_16["significant"]) and
                         not (ceil_paired_2 and ceil_paired_2["significant"]) and cap_cost_16 > cap_cost_2 + 0.02)
    sharp_gap_significant = bool(sharp_paired_16 and sharp_paired_16["significant"])

    # RULER-DEPENDENT floor-equivalence (disclosed, not asserted as the headline)
    floor_equiv_own = bool(abs(Fr - Fo) <= MARGIN)               # own-sharp ruler
    floor_equiv_common = bool(abs(Fr_common - Fo_common) <= MARGIN)  # common ruler (artifact's primary)
    ceiling_cost_robust = bool(ceil_paired_16 and ceil_paired_16["significant"])

    # Headline books the cost as a CEILING/capacity cost (robust), NOT 'floor-equivalent' (ruler-dependent).
    both_revive = bool(off_c["revives"] and resh_c["revives"])
    legitimacy = (
        "PRESERVE on the uniformity argument (same machinery as the cortices). Both drop(off) and "
        "preserve(reshaped) REVIVE the channel (binary liveness), so liveness does not select. Reshaped "
        f"carries a ROBUST seed-paired {'SCALE-GROWING ' if scale_growing else ''}CEILING capacity cost "
        f"(off-reshaped = {cap_cost_16:+.3f} @card-16, paired t={ceil_paired_16['t'] if ceil_paired_16 else 'NA'}, "
        f"{ceil_paired_16['sign_split'] if ceil_paired_16 else 'NA'}; ~{cap_cost_2:+.3f} @card-2) that drop "
        "avoids -- the measured price of the tie, chosen on uniformity grounds. NOT 'validated'. "
        "'Floor-equivalent' is RULER-DEPENDENT (holds own-sharp Δ%.3f; FAILS common off-sharp Δ%.3f>margin, "
        "the ruler this artifact's own CARD16.floors+topology use) and the subtracted sharp-gap is "
        "%sSIGNIFICANT -- so the cost is booked as a ceiling cost, not laundered out of the floor."
        % (abs(Fr - Fo), abs(Fr_common - Fo_common), "" if sharp_gap_significant else "NOT "))
    phasing_armed = ceiling_cost_robust          # show onset-modulation of the (robust) ceiling cost
    marginal = False

    # ---------- phasing re-check (armed on reshaped < off) ----------
    phasing = None
    if phasing_armed:
        rec = {}
        # reconfirmed @0.1 ceiling if present; else surface phasing repose@1 per onset
        for key, colcells in phas_raw["columns"].items():           # key e.g. "reshaped@0.1"
            onset = key.split("@")[1]
            rkey = f"16/reshaped@{onset}/repose@1.0"
            if rkey in _RECON:
                rec[key] = round(_RECON[rkey]["ceiling_mean"], 4)
            else:
                rec[key] = round(colcells["repose@1"]["d_diff"]["mean"], 4)
        best_key = max(rec, key=rec.get); best = rec[best_key]
        cushion = round(best - (Co - MARGIN), 4)
        if best >= Co - MARGIN:
            phasing = dict(outcome=f"reversal NOT locked — reshaped recovers to WITHIN MARGIN of off (NOT "
                                   f"better) at {best_key}: best C={best} is {round(Co-best,4)} BELOW off "
                                   f"C={round(Co,4)}, clearing only the off-margin bar (cushion {cushion}). "
                                   "Onset modulates the ceiling cost but does not erase it; preserve holds "
                                   "as a uniformity choice, not because reshaped matches off.",
                           per_onset_ceiling=rec, best_onset=best_key, best_C=best, off_C=round(Co, 4),
                           below_off_by=round(Co - best, 4), margin_cushion=cushion, reversal_locked=False,
                           caveat="thin cushion vs the off-creep (off@16 still rising); a converged off "
                                  "would widen the gap and could erode this cushion")
        else:
            phasing = dict(outcome="reversal LOCKS — reshaped stays worse than off across ALL onsets "
                                   "-> correct-it (drop) cleaner; fixed-PAM promoted",
                           per_onset_ceiling=rec, best_onset=best_key, best_C=best, off_C=round(Co, 4),
                           reversal_locked=True)

    out = dict(
        commit_hash=main_raw["commit_hash"], spec_hash=main_raw["spec_hash"],
        live_bar=LIVE_BAR, significance_band_k=SEM_K,
        ceilings_from=("reconfirm (10 seeds, plateau-checked) where available; surface fallback"),
        CARD16=dict(columns=reads16, floors=floors16, topology=topo16),
        CARD2=dict(columns=reads2, floors=floors2, topology=topo2),
        TOPOLOGY_INVARIANT_16_vs_2=dict(
            klass_match=topology_invariant,
            klass_match_note="coarse klass-string match; near-FORCED because deployed-dead pins the floor "
                             "spread to maximum at both cards (separable unreachable) -> reduces to the "
                             "single bit 'reshaped did not undershoot off'. Not a strong structural result.",
            discriminating_relationship_invariant=bool(
                (ceil_paired_2 is None or not ceil_paired_2["significant"]) and
                (ceil_paired_16 is None or not ceil_paired_16["significant"])),
            discriminating_note="The off-vs-reshaped CEILING gap (the spec's 2nd invariance gate / only "
                                "non-trivial content) is NOT cardinality-invariant: dead tie @card-2 "
                                f"(t={ceil_paired_2['t'] if ceil_paired_2 else 'NA'}) vs significant "
                                f"@card-16 (t={ceil_paired_16['t'] if ceil_paired_16 else 'NA'}). So "
                                "member-count DOES modulate the reshaped capacity cost.",
            member_count_claim="member-count does not FLIP liveness (OR-kill + off<=reshaped ordering "
                               "replicate at cards 2 and 16); it is NOT a clean non-lever -- it modulates "
                               "the scale-growing capacity cost. Two cardinalities cannot anchor invariance "
                               "of a relationship that changes between them."),
        intrinsic_inflated_split_16={k: dict(inflated=reads16[k]["recoverable_inflated"],
                                             irreducible=reads16[k]["irreducible_floor"]) for k in reads16},
        CUE_RECOVERABILITY_SCOPE=(
            "floor~0 (cue diffuseness fully recoverable by content-blind re-organization) is STRUCTURALLY "
            "FORCED, not discovered: the re-posing (comp - alpha*mu) is exactly global mean-centering, and "
            "the tested diffuse cue puts ~100% of masking energy in a SINGLE cls-independent common-mode "
            "(5.831*base) with a tiny differentiating part (0.5*Cd) -> at alpha=1 mean-centering removes the "
            "common-mode EXACTLY, so floor~0 follows from the construction independent of training (near "
            "tautology). The fully_recoverable=true booleans below MUST be quoted with this scope. Two "
            "further limits: (i) common-mode-dominance is itself a PROBE SIMPLIFICATION of the deployed rig "
            "(R_coarse is per-coarse-class, r_distractor possibly per-member; a single global mean-centering "
            "would NOT remove those) -> the deployed substrate's true floor may be >0, UNVERIFIED; (ii) the "
            "spec's stated native substrate is 'diffuse-but-structured' -- the tested cue is the LEAST "
            "structured case (a constant offset), so the structured-diffuseness floor (the build-robust part "
            "of the two-part cue fix) remains UNMEASURED. The ablation-invariance guard proves 'injects no "
            "new signal' (a tautology of constant subtraction), NOT 'recovers diffuseness in general'."),
        CONVERGENCE_FLAGS=dict(
            off_card16_plateau="RESOLVED by converge to 36000 (exp07_converge_off16): 16/off/repose@1.0 "
                               "PLATEAUS at ~1.126 (flat 30k/33k/36k = 1.133/1.129/1.126; the 24k->30k creep "
                               "stopped). The +0.103 card-16 ceiling gap is now a CONVERGED number (paired "
                               "t=2.84, equal-training at 36000), NOT a lower bound. [At the 30000 snapshot "
                               "off was still creeping -> earlier reported as a lower bound; the converge "
                               "confirms the plateau and the gap held ~constant 0.108->0.103.]",
            reshaped_plateau="reshaped ceilings flat by ~18-24k, confirmed at 36000 (1.024/1.042/1.023) -> converged.",
            equal_convergence="both off and reshaped now read at 36000, both plateaued -> equal-TRAINING and "
                              "equal-CONVERGENCE."),
        LEGITIMACY=dict(
            verdict=legitimacy,
            basis="uniformity argument; both columns revive (liveness does not select); cost booked as CEILING",
            both_revive=both_revive,
            robust_deliverable="seed-paired CEILING capacity cost (off-reshaped); floor-equivalence is ruler-dependent",
            ceiling_cost_card16=dict(delta=cap_cost_16, paired=ceil_paired_16, robust=ceiling_cost_robust),
            ceiling_cost_card2=dict(delta=cap_cost_2, paired=ceil_paired_2),
            scale_growing=scale_growing,
            sharp_gap_card16=dict(delta=round(off_c["own_sharp"] - resh_c["own_sharp"], 4),
                                  paired=sharp_paired_16, significant=sharp_gap_significant,
                                  note="NOT significant -> cannot be cleanly booked as a separable uniform "
                                       "offset; the robust cost is the ceiling gap" if not sharp_gap_significant
                                       else "significant"),
            floor_equivalence=dict(
                own_sharp_ruler=dict(off=round(Fo, 4), reshaped=round(Fr, 4), delta=round(Fr - Fo, 4),
                                     equivalent=floor_equiv_own),
                common_offsharp_ruler=dict(off=round(Fo_common, 4), reshaped=round(Fr_common, 4),
                                           delta=round(Fr_common - Fo_common, 4), equivalent=floor_equiv_common),
                ruler_dependent=bool(floor_equiv_own != floor_equiv_common),
                note="floor-equivalence holds under own-sharp but FAILS under the common off-sharp ruler "
                     "(the ruler this artifact's CARD16.floors + topology use). The robust deliverable is "
                     "the ceiling cost. Spec is ambiguous (own-sharp: 'each column carries its own sharp'; "
                     "common: 'unreachable ruler'); both reported."),
            off_C=round(Co, 4), reshaped_C=round(Cr, 4),
            off_per_seed=off_c["ceiling_per_seed"], reshaped_per_seed=resh_c["ceiling_per_seed"]),
        PHASING_RECHECK=phasing,
    )
    print(json.dumps(out, indent=2))
    Path(_HERE / "exp07_interior_read.json").write_text(json.dumps(out, indent=2))

    # human summary
    print("\n" + "=" * 80)
    print("exp07 INTERIOR READ — SUMMARY")
    print("=" * 80)
    for card, reads, topo in (("16", reads16, topo16), ("2", reads2, topo2)):
        print(f"\ncard-{card}:")
        for col, r in reads.items():
            fl = r["irreducible_floor"]
            print(f"  [{col:8s}] C={r['ceiling_C']:.3f}±{r['ceiling_sem']:.3f} "
                  f"floor={fl['value']:.3f}±{fl['uncertainty']:.3f} "
                  f"revives={r['revives']} plateaued={r['ceiling_plateaued']} ({r['ceiling_source']})")
        print(f"  topology: {topo['klass']} (spread {topo['spread']})")
    _disc_inv = bool((ceil_paired_2 is None or not ceil_paired_2["significant"]) and
                     (ceil_paired_16 is None or not ceil_paired_16["significant"]))
    print(f"\ntopology klass-match 16 vs 2: {topology_invariant} (deployed-dead-driven; coarse)  |  "
          f"discriminating off-vs-reshaped relationship invariant: {_disc_inv} "
          f"(dead tie @card-2 t={ceil_paired_2['t'] if ceil_paired_2 else 'NA'} vs significant @card-16 "
          f"t={ceil_paired_16['t'] if ceil_paired_16 else 'NA'}) -> member-count does NOT flip liveness "
          f"but DOES modulate the capacity cost")
    print(f"\nLEGITIMACY: {legitimacy}")
    print(f"  ROBUST ceiling cost: card-16 Δ={cap_cost_16:+.3f} (paired t="
          f"{ceil_paired_16['t'] if ceil_paired_16 else 'NA'}, {ceil_paired_16['sign_split'] if ceil_paired_16 else ''}, "
          f"sig={ceil_paired_16['significant'] if ceil_paired_16 else 'NA'})  |  card-2 Δ={cap_cost_2:+.3f} "
          f"(t={ceil_paired_2['t'] if ceil_paired_2 else 'NA'}, sig={ceil_paired_2['significant'] if ceil_paired_2 else 'NA'})  "
          f"scale_growing={scale_growing}")
    print(f"  floor-equivalence RULER-DEPENDENT: own-sharp Δ={Fr-Fo:+.3f} (equiv={floor_equiv_own})  "
          f"common-ruler Δ={Fr_common-Fo_common:+.3f} (equiv={floor_equiv_common})")
    print(f"  sharp-gap (would-be uniform offset) significant={sharp_gap_significant} "
          f"(t={sharp_paired_16['t'] if sharp_paired_16 else 'NA'})")
    if phasing:
        print(f"\nPHASING RE-CHECK: {phasing['outcome']}")
        print(f"  per-onset C: {phasing['per_onset_ceiling']}")


if __name__ == "__main__":
    main()
