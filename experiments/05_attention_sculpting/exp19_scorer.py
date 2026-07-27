"""exp19_scorer.py — B8: the deployed DUAL-DETECTOR stratified scorer (Jason 2026-07-15, against the
corrected exp19_cal).

ONE FLOOR-AUDIT LAW, per-B, BOTH reads. For an arm/B the scorer inherits that B/read's operating-point WIDTH
from exp19_cal (the calibration cuts it on the null; the scorer FREEZES and applies it — it never re-selects a
width on its own data), then certifies each seed at that width on BOTH reads:
  - FULL read       (all onsets)          -> the raw conversion count
  - STRATIFIED read  (zero-preceding)      -> the recency-FREE count
    The stratifier is the PROPERTY (S19._zero_preceding: emitted-first same-dwell wave), NEVER the label
    `pos==1` (§4.2 trap / RECENCY-BY-LABEL — that would certify its own confound).
The two reads together are the recency test (§7 outcome cells): RESCUE survives the STRATIFIED read;
RECENCY-CARRIED is FULL-only (certified raw, absent stratified).

CERTIFICATION is OUTCOME-BLIND — a seed certifies iff its observed longest run at the inherited width EXCEEDS
its own in-regime SIMULATED phantom floor (exp19_floor._sim_null_runs at that width, p<1/N_SIMS). No
known-non-converter labels enter the score; the empirical-non-converter floor is a CALIBRATION device (it
selects the op and is the matched-bar referent), not a scoring input. The BORROW-GATE is gone (ledger 43):
every arm self-calibrates on its OWN measured null — C_shuffle's elevated floor is reproduced as its measured
phantom null. Cross-arm floor ORDERING (per-arm floor height, all arms one instrument) is B9's matched-bar
tab, NOT here.

COMPANIONS (both REPORTED, never gated):
  - gradient : EXP16's Δ = p1 − p13-48 per B vs A's committed referent +0.1416 (exp16_score._recency_gradient).
               Shuffled fabric removes recency ⇒ Δ collapses toward 0 (§10.26); the dwelled B=1 pole is A.
  - dec_cat  : the free LOO nearest-centroid category-decode field (col-only; DECCAT-REGIME-BOUND, §10). The
               rescue cells' MECHANISTIC falsifier — flat=RECENCY-CARRIED/artifact, climbing-onto-category=real
               — read at ATTRIBUTION, never a gate here (a post-hoc "dwell solved" read is forbidden).

STATUS: built + validated on B=T (exp12_shuffle) + smoked. Treatment arms exp19_wperm_B{32,128,512,2048} have
NO records until the corridor (nothing trains until G8); the scorer runs per-B there against the inherited op.
"""
from __future__ import annotations

import json
import statistics
import sys

import torch

import exp14_arms as XA
import exp16_score as X16
import exp19_cal as CAL
import exp19_floor as FL
import exp19_g5b_rebin as RB

OUTDIR = XA.OUTDIR
READ_AT, H_MAX = CAL.READ_AT, CAL.H_MAX
REPLAY_TAG = CAL.REPLAY_TAG                       # "g5a_replay" — the verdict-seed replay records (with columns)
VERDICT_SEEDS = list(range(8))
CONVERTERS, NONCONVERTERS = [0, 2, 4, 5, 6], [1, 3, 7]     # committed C_shuffle labels (B=T validation only)

# ONE DETECTOR FAMILY (ledger 44): the scorer CERTIFIES at the SAME band its op WIDTH was cut on. The width
# comes from exp19_cal, which selects it via RB._longest_run_binned at RB.BAND=0.64 (the committed C_shuffle
# detector band, ledger 40/41). exp19_floor's default FLOOR_BAND=0.704 is the α-forced sparse-bin artifact the
# re-bin RETRACTED — it must NOT leak back into the score. BAND is passed explicitly to every certification call.
BAND = CAL.BAND
assert BAND == RB.BAND, f"one-detector-family broken: certification band {BAND} != calibration band {RB.BAND}"


# ---------------------------------------------------------------- the floor audit AT THE INHERITED WIDTH
def _bin(onsets: list, acq: int, width: int, read_at: int = READ_AT) -> tuple[list, dict]:
    """Per POST-ACQ window (right-edge = (wave//width+1)*width) at the inherited op width: the in-window onset
    accs, emitted order. The acq filter is on the ONSET WAVE (`wave < acq`), IDENTICAL to the width-selection
    instrument RB._longest_run_binned (exp19_g5b_rebin) — so the scoring windows and the width-selection windows
    are composed of the same onsets at the acq boundary (ledger 44 companion). The grid is the FULL contiguous
    post-acq window grid — a window with no onset is None and BREAKS runs (conservative)."""
    win: dict = {}
    for wave, acc in onsets:
        if wave < acq:                              # match RB: exclude PRE-acquisition onsets (by wave, not edge)
            continue
        col = (wave // width + 1) * width
        if col > read_at:
            continue
        win.setdefault(col, []).append(acc)
    grid = [t for t in range(width, read_at + 1, width) if t >= acq]
    return grid, win


def _certify_seed(onsets: list, acq: int, width: int, gen: torch.Generator,
                  read_at: int = READ_AT) -> dict:
    """Outcome-blind certification: observed longest run at `width` vs the seed's OWN in-regime simulated
    phantom floor (Binomial-per-window at the seed's post-acq mean; p<1/N_SIMS). Certified at BAND=CAL.BAND
    (0.64) — the SAME band the op width was cut on (ledger 44), NOT exp19_floor's retracted 0.704 default.
    `read_at` (EXP20, ledger row 56): the window-grid horizon. The DEFAULT stays READ_AT=500,000 so every
    EXP19 result is byte-preserved; a caller whose ratified law reads at another horizon MUST pass it —
    the def-time default silently truncated EXP20's 1M certification to the first 500k waves (the 6th
    un-transported constant; caught by the G6 refute panel, 8/8 adversarial confirms)."""
    grid, win = _bin(onsets, acq, width, read_at)
    series = FL._series_from_win({str(t): v for t, v in win.items()}, grid)
    obs = FL._longest_run(series, band=BAND)
    counts = [len(win.get(t, [])) for t in grid]
    vals = [a for a in series if a is not None]
    p_hat = statistics.mean(vals) if vals else 0.5
    null = FL._sim_null_runs(counts, p_hat, FL.N_SIMS, gen, band=BAND)
    null_max = int(null.max())
    return dict(observed_run=obs, p_hat=round(p_hat, 4), null_max=null_max,
                p_value=round(float((null >= obs).float().mean()), 5),
                certified=bool(obs > null_max))                 # excess over the measured floor (ledger 18/38)


def _recency_test(full_certified: list, strat_certified: list) -> tuple[list, list, list]:
    """The §7 recency composition, ONE definition shared by score_dual and the smoke (so the smoke exercises the
    deployed path, not a copy). Returns (recency_carried = FULL∖STRAT, survives = STRAT, stratified_only =
    STRAT∖FULL). stratified_only is an ANOMALY: a recency-free certification with no floor-audited raw
    correlate — not a modeled §7 cell (§7 assumes STRAT ⊆ FULL) ⇒ HALT → Jason."""
    fc, sc = set(full_certified), set(strat_certified)
    return sorted(fc - sc), sorted(sc), sorted(sc - fc)


def _op_width(arm: str, read: str, conv: list, nonconv: list, data: dict | None = None) -> tuple[int | None, dict]:
    """INHERIT the operating-point width from exp19_cal for (arm, read) — the calibration cuts it on the null
    (argmax separation, ledger 42). Underpowered ⇒ (None, cal): STRATUM-UNDERPOWER, the null is uninterpretable
    and this read cannot report a count → HALT → Jason. The scorer NEVER selects a width on its own outcome.
    `data` threads in-memory planted onsets to the calibration (the underpower smoke); else cal reads files."""
    cal = CAL.cal_floor_audit(arm, read, conv, nonconv, data=data)
    return (None if cal["underpowered"] else cal["operating_point_width"]), cal


def score_arm(arm: str, read: str, seeds: list, op_width: int, data: dict | None = None) -> dict:
    """Certify every seed at the FROZEN inherited `op_width` on `read`. `data` (optional) = {seed:(acq,onsets)}
    in-memory (the smoke plants it); else read the arm's per-onset captures via exp19_cal._onsets. Per-seed
    deterministic simulator gen (SIM_SEED+seed) ⇒ the score is independent of seed iteration order."""
    if data is None:
        data = {s: CAL._onsets(arm, s, read) for s in seeds}
    per_seed = {}
    for s in seeds:
        acq, ons = data[s]
        gen = torch.Generator().manual_seed(FL.SIM_SEED + int(s))
        per_seed[s] = _certify_seed(ons, acq, op_width, gen)
    certified = [s for s in seeds if per_seed[s]["certified"]]
    return dict(arm=arm, read=read, op_width=op_width, per_seed=per_seed,
                certified_seeds=certified, k=len(certified), n=len(seeds))


def _companions(arm: str, seeds: list, read_at: int = READ_AT) -> dict:
    """REPORTED, never gated. Per seed: EXP16 gradient Δ = p1 − p13-48 (vs A +0.1416) and dec_cat mean, from
    the committed column records (the replay rec carries pos_err_word + dec_cat). DECCAT-REGIME-BOUND: dec_cat
    is a mechanistic falsifier read at attribution, NOT a gate; a post-hoc 'dwell solved' read is forbidden."""
    per = {}
    for s in seeds:
        # dec_cat endpoint replays (tag "dcy", ledger 48 / decay micro-arm) supersede the g5a records for
        # companions when present — same committed trajectory, anchor-proven digit-exact, dec_cat-bearing.
        p_dcy = OUTDIR / f"exp14_{arm}_s{s}_dcy.json"
        p = p_dcy if p_dcy.exists() else (OUTDIR / f"exp14_{arm}_s{s}_{REPLAY_TAG}.json")
        rec = XA._truncate(json.loads(p.read_text()), read_at)
        g = X16._recency_gradient(rec)
        onset = rec.get("acquisition_onset")        # POST-ONSET only, matching the gradient sibling (X16 skips t<onset)
        dc = [c["dec_cat"] for c in rec["columns"]
              if c.get("dec_cat") is not None and (onset is None or c["t"] >= onset)]
        per[s] = dict(gradient_delta=g["delta"], p1=g["p1"], p13_48=g["p13_48"],
                      dec_cat_mean=round(statistics.mean(dc), 4) if dc else None, dec_cat_n=len(dc))
    deltas = [per[s]["gradient_delta"] for s in seeds if per[s]["gradient_delta"] is not None]
    dcs = {s: per[s]["dec_cat_mean"] for s in seeds if per[s]["dec_cat_n"] > 0}
    # COVERAGE-HONEST dec_cat (ledger 48, N1 — Jason 2026-07-17): only records replayed AFTER the dec_cat
    # rider carry the field (at B=T that is s0, the anchor-verification re-replay; 1/8). NO bare "median"
    # over n=1 — the summary states its coverage or withholds itself; the per-seed dec_cat_n is the truth.
    return dict(per_seed=per, referent_A_gradient_delta=X16.X16_GRAD_REF_A["delta"],
                gradient_median_delta=round(statistics.median(deltas), 5) if deltas else None,
                dec_cat_covered=len(dcs), dec_cat_total=len(seeds),
                dec_cat_values={s: dcs[s] for s in sorted(dcs)},
                dec_cat_median=(round(statistics.median(dcs.values()), 4) if len(dcs) >= 2 else None),
                note="REPORTED not gated; dec_cat is DECCAT-REGIME-BOUND (attribution-only falsifier); "
                     "dec_cat_median withheld below 2-seed coverage — read dec_cat_values with dec_cat_covered")


def score_dual(arm: str, seeds: list, conv: list, nonconv: list, data: dict | None = None) -> dict:
    """The dual-detector read for one arm/B: FULL vs STRATIFIED at each read's OWN inherited op width, plus the
    recency test (§7) and the reported companions. UNDERPOWER on either read → STRATUM-UNDERPOWER (HALT). A
    STRATIFIED-ONLY certification (a seed certified recency-free but not in the raw read) → HALT (anomaly, §7
    assumes STRAT ⊆ FULL). `data` threads in-memory planted onsets (the smoke) to both cal and the scorer."""
    wf, cal_f = _op_width(arm, "full", conv, nonconv, data=data)
    ws, cal_s = _op_width(arm, "stratified", conv, nonconv, data=data)
    if wf is None or ws is None:
        under = [r for r, w in (("full", wf), ("stratified", ws)) if w is None]
        return dict(arm=arm, underpowered=True, underpowered_reads=under,
                    VERDICT=f"STRATUM-UNDERPOWER ({arm}, reads {under}) — inherited op has no usable width ⇒ "
                            "null uninterpretable ⇒ HALT → Jason", ok=True)
    full = score_arm(arm, "full", seeds, wf, data=data)
    strat = score_arm(arm, "stratified", seeds, ws, data=data)
    recency_carried, survives, stratified_only = _recency_test(full["certified_seeds"], strat["certified_seeds"])
    anomaly = bool(stratified_only)
    comp = None if data is not None else _companions(arm, seeds)   # companions read files; skip for planted data
    verdict = (f"{arm}: full {full['k']}/{full['n']} (op {wf}), stratified {strat['k']}/{strat['n']} (op {ws}); "
               f"recency-carried {recency_carried}; survives-stratified {survives}")
    if anomaly:
        verdict = (f"STRATIFIED-ONLY certification ({arm}, seeds {stratified_only}) — the recency-free read "
                   f"certified a seed the FULL/raw read did not: no floor-audited raw correlate, NOT a modeled "
                   f"§7 cell ⇒ HALT → Jason. [{verdict}]")
    elif comp is not None:
        verdict += (f"; gradient median Δ {comp['gradient_median_delta']} vs A "
                    f"+{comp['referent_A_gradient_delta']}; dec_cat coverage "
                    f"{comp['dec_cat_covered']}/{comp['dec_cat_total']} "
                    f"(values {comp['dec_cat_values']}; median "
                    f"{comp['dec_cat_median'] if comp['dec_cat_median'] is not None else 'withheld <2 seeds'})")
    return dict(
        gate="B8 exp19_scorer — dual-detector floor-audit (inherited op per read, outcome-blind sim floor)",
        arm=arm, seeds=seeds, underpowered=False,
        full=full, stratified=strat,
        recency_carried_seeds=recency_carried,      # FULL-certified, absent STRATIFIED = the recency channel
        survives_stratified=survives,               # the recency-free count (the finding, if any)
        stratified_only_seeds=stratified_only,      # STRAT-certified, absent FULL = ANOMALY (HALT if non-empty)
        anomaly_stratified_only=anomaly,
        companions=comp,
        VERDICT=verdict, ok=not anomaly)


# ---------------------------------------------------------------- B=T validation (exp12_shuffle)
def _validate_BT():
    out = score_dual("exp12_shuffle", VERDICT_SEEDS, CONVERTERS, NONCONVERTERS)
    print("=== exp19_scorer  B=T (exp12_shuffle) dual-detector ===")
    for read in ("full", "stratified"):
        r = out[read]
        print(f"  {read:>10} (op {r['op_width']}): k={r['k']}/{r['n']}  certified={r['certified_seeds']}")
        for s in VERDICT_SEEDS:
            ps = r["per_seed"][s]
            tag = "conv" if s in CONVERTERS else "non "
            print(f"      s{s} [{tag}] run {ps['observed_run']:>3}  null_max {ps['null_max']:>2}  "
                  f"p {ps['p_value']:.4f}  {'CERT' if ps['certified'] else '----'}")
    print(f"  recency-carried (full∖stratified): {out['recency_carried_seeds']}")
    print(f"  survives-stratified: {out['survives_stratified']}")
    c = out["companions"]
    print(f"  companions: gradient median Δ={c['gradient_median_delta']} vs A +{c['referent_A_gradient_delta']} "
          f"(shuffled ⇒ recency removed ⇒ Δ→0); dec_cat coverage {c['dec_cat_covered']}/{c['dec_cat_total']} "
          f"values={c['dec_cat_values']} (median {'withheld — <2 seeds carry the field (ledger 48)' if c['dec_cat_median'] is None else c['dec_cat_median']})")
    print(f"  VERDICT: {out['VERDICT']}")
    (OUTDIR / "exp19_scorer_exp12_shuffle_dual.json").write_text(json.dumps(out, indent=2))
    # invariants (self-testing contracts — the B=T coincidence full==strat==CONVERTERS makes each falsifiable):
    assert set(out["full"]["certified_seeds"]) == set(CONVERTERS), \
        f"B=T full read must certify the committed converters {CONVERTERS}, got {out['full']['certified_seeds']}"
    assert set(out["stratified"]["certified_seeds"]) == set(CONVERTERS), \
        f"B=T stratified read must certify the committed converters {CONVERTERS} (all SURVIVE the stratum), " \
        f"got {out['stratified']['certified_seeds']}"                      # == not issubset (empty passes issubset)
    assert set(out["stratified"]["certified_seeds"]).issubset(set(out["full"]["certified_seeds"])), \
        "STRATIFIED-ONLY certification at B=T — a recency-free cert with no raw correlate (§7 assumes STRAT⊆FULL)"
    assert out["recency_carried_seeds"] == [] and not out["anomaly_stratified_only"], \
        f"B=T recency-carried must be empty / no anomaly, got carried={out['recency_carried_seeds']} " \
        f"anomaly={out['anomaly_stratified_only']}"
    # companion regression tripwires (validation-reference ONLY; the corridor companions stay REPORTED-not-gated)
    assert c["gradient_median_delta"] is not None and abs(c["gradient_median_delta"]) < 0.05, \
        f"B=T gradient companion drifted: median Δ={c['gradient_median_delta']} (want ~0, far below A "\
        f"+{c['referent_A_gradient_delta']})"
    # dec_cat coverage tripwire (ledger 48): at HEAD only s0 carries the field (1/8 — the anchor re-replay);
    # the median must be WITHHELD at this coverage and s0's value guards the reference band. When the C1/D1
    # replays land, coverage rises and this assert is updated WITH them (a coverage change is a data change).
    assert c["dec_cat_covered"] == 8 and c["dec_cat_median"] is not None, \
        f"dec_cat coverage changed ({c['dec_cat_covered']}/{c['dec_cat_total']}, median {c['dec_cat_median']})" \
        " — update this tripwire WITH the replays that changed it (ledger 48; 8/8 since the Phase-C batch afeeb71)"
    assert abs(c["dec_cat_values"][0] - 0.662) < 0.02, \
        f"s0 dec_cat drifted: {c['dec_cat_values'].get(0)} (want ~0.662)"
    print("  [invariants OK] full & stratified both reproduce the committed converters (all survive the "
          "stratum); STRAT⊆FULL; recency-carried empty; gradient≈0; dec_cat coverage-honest (8/8 since "
          "the Phase-C batch, median reported, s0≈0.662)")


# ---------------------------------------------------------------- smoke (positive-delta falsifiers)
def _smoke():
    print("exp19_scorer SMOKE — certification, recency test, stratified-only anomaly, underpower HALT (reachable):")
    W = 300
    # (a) CERTIFICATION reachable falsifier: a real episode certifies; pure chance does not.
    acq, real = CAL._plant(True)
    _acq, chance = CAL._plant(False)
    r_real = _certify_seed(real, acq, W, torch.Generator().manual_seed(FL.SIM_SEED))
    r_chance = _certify_seed(chance, _acq, W, torch.Generator().manual_seed(FL.SIM_SEED + 1))
    assert r_real["certified"] and not r_chance["certified"], \
        f"SMOKE FAIL: certification not a reachable falsifier (real={r_real['certified']} chance={r_chance['certified']})"
    print(f"  (a) real episode run {r_real['observed_run']} > null_max {r_real['null_max']} -> CERT; "
          f"chance run {r_chance['observed_run']} <= null_max {r_chance['null_max']} -> not  [reachable]")
    # (b) DUAL-DETECTOR recency test through the DEPLOYED path (score_arm + _recency_test, NOT an inline copy):
    #     s0 FULL episode + CHANCE stratified -> RECENCY-CARRIED; s1 real on BOTH -> survives; s2 chance -> neither.
    full = score_arm("PLANT", "full", [0, 1, 2], W,
                     data={0: CAL._plant(True), 1: CAL._plant(True), 2: CAL._plant(False)})
    strat = score_arm("PLANT", "stratified", [0, 1, 2], W,
                      data={0: CAL._plant(False), 1: CAL._plant(True), 2: CAL._plant(False)})
    carried, survives, strat_only = _recency_test(full["certified_seeds"], strat["certified_seeds"])
    assert carried == [0] and survives == [1] and strat_only == [], \
        f"SMOKE FAIL: recency test wrong (carried={carried}, survives={survives}, strat_only={strat_only})"
    print(f"  (b) s0 full-only -> RECENCY-CARRIED {carried}; s1 both -> survives {survives}; strat-only {strat_only}"
          f"  [deployed helper, reachable]")
    # (c) STRATIFIED-ONLY anomaly is reachable: a recency-free cert with NO raw correlate -> the HALT key is set.
    _c, _s, so = _recency_test([2], [2, 0])
    assert so == [0], f"SMOKE FAIL: stratified-only anomaly not detected ({so})"
    print(f"  (c) full=[2], strat=[2,0] -> stratified-only anomaly {so} (HALT key)  [reachable]")
    # (d) UNDERPOWER HALT: an arm whose inherited op is None (all-chance cal) -> STRATUM-UNDERPOWER, NO count.
    chance_data = {s: CAL._plant(False) for s in (0, 1, 2, 3)}
    halt = score_dual("PLANT", [0, 1, 2, 3], [0, 2], [1, 3], data=chance_data)
    assert halt["underpowered"] and "STRATUM-UNDERPOWER" in halt["VERDICT"] and "full" not in halt, \
        f"SMOKE FAIL: underpower HALT path not driven ({halt.get('VERDICT')})"
    print(f"  (d) all-chance arm -> underpowered={halt['underpowered']}, reads {halt['underpowered_reads']}, "
          f"no count reported  [HALT path driven]")
    print("SMOKE PASS: certification fires only on real excess; the deployed dual-detector separates recency-"
          "carried / survives-stratified / stratified-only-anomaly; the underpower HALT is driven end-to-end.")


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--validate" in sys.argv:
        _validate_BT()
    elif "--smoke" in sys.argv:
        _smoke()
    else:
        print("usage: --validate | --smoke   (B=T dual-detector reproduction / reachable-falsifier smoke)")
