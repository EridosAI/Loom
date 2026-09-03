"""exp19_g5a.py — G5a STRATUM VIABILITY (Jason ruling 4, ledger 36). Runs FIRST; nothing before it.

THE GATE (prereg EXP19 §4.3 / §7): does exp12_shuffle certify on its OWN zero-preceding stratum at
FULL stratum N (~14,156), with the detector (band, N) RE-CUT FRESH on the stratum via _provisional_cut
(calibrate-in-regime transports the PROCEDURE, never the constant — the committed full-READ 0.64x5 over
ALL onsets does NOT transport; consec=5 cannot be inherited, the timescale changed)?
  NO -> HALT -> Jason: the stratified detector has no baseline, wp-strat is unaskable, the arm's entire
  recency defence is DECORATIVE. Structural shatter risk: a 36-90 window episode, thinned to ~30% of
  onsets per window, may be unable to form runs at ANY N.

MECHANISM (why a replay): committed columns store per-WINDOW exam_acc (evolving-weight mean); the stratum
is per-ONSET. exp19_replay recovers the per-onset series by deterministic replay, anchor-certified
(A1 bit-exact ckpt / A2 columns / A3 re-bin). See exp19_replay.py header.

TWO-PHASE:
  --replay SEED   deterministic replay + per-onset capture + anchor verify + write. (parallelizable)
  --score         stratify every captured seed, re-cut (band,N) on the stratum null, census -> certify?

NULL SOURCE (documented, non-gameable): the prereg names _provisional_cut. Primary = _provisional_cut on
the 8 verdict seeds' OWN stratified post-acq null (it episode-excludes s0-class conversions, so the cut
is honest, not circular). SENSITIVITY = Ruling-B _between_episode_null (the committed cell used Ruling B).
BOTH bands are reported; if the certify verdict agrees under both, the choice is moot. None-windows (a
window with zero in-stratum onsets) BREAK runs in the census (conservative — never manufactures a run)
and are excluded from the null pool; their count is reported.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp19_score as S19
import exp19_replay as R

EVAL = XA.EVAL
READ_AT = R.READ_AT
H_MAX = R.H_MAX
ARM = "exp12_shuffle"
VERDICT_SEEDS = list(range(8))
CONVERTERS = [0, 2, 4, 5, 6]          # committed X15_REPRO["C_shuffle"]
NONCONVERTERS = [1, 3, 7]
REPLAY_TAG = "g5a_replay"


# ---------------------------------------------------------------- phase 1: replay + anchor + capture
def replay_seed(seed: int) -> dict:
    rec, per_onset = R.capture_run(ARM, seed, read_at=READ_AT, h_max=H_MAX, out_tag=REPLAY_TAG)
    anchors = R.verify_anchors(ARM, seed, REPLAY_TAG, per_onset, rec, verdict_tag="verdict")
    R.write_capture(ARM, seed, per_onset, REPLAY_TAG)
    rep = dict(seed=seed, acquisition_onset=rec["acquisition_onset"], anchors=anchors)
    (XA.OUTDIR / f"exp14_{ARM}_s{seed}_{REPLAY_TAG}_anchors.json").write_text(json.dumps(rep, indent=2))
    tag = "ALL-GREEN" if anchors["all_green"] else "!!! ANCHOR RED !!!"
    print(f"s{seed}: {tag}  A1={anchors['A1_bitexact']} A2={anchors['A2_columns']} "
          f"A3={anchors['A3_consistency']}  n_onset={anchors['n_onset_captured']}  "
          f"acq_onset={rec['acquisition_onset']}")
    if not anchors["all_green"]:
        for k in ("A1_div", "A2_div", "A3_div"):
            if anchors[k]:
                print(f"    {k}: {anchors[k]}")
    return rep


# ---------------------------------------------------------------- phase 2: stratify + re-cut + census
def _max_run_nonesafe(vals, band: float) -> int:
    best = cur = 0
    for a in vals:
        cur = cur + 1 if (a is not None and a >= band) else 0
        best = max(best, cur)
    return best


def stratify(seed: int, acquisition_onset) -> dict:
    """Restrict the captured per-onset series to the zero-preceding stratum, re-bin to 300-step windows
    -> stratified per-window exam_acc. Returns the full window series + post-acq series (with None) +
    stratum size + None count."""
    cap = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{seed}_{REPLAY_TAG}_peronset.json").read_text())
    per_onset = cap["per_onset"]                      # [wave, dwell_id, pos, acc]
    # rebuild the deployed fabric (index-list only, no training) for the stratum mask over [0, read_at)
    loop, spec, cfg = X12.build_exp12(ARM, seed, H_MAX)
    fab = loop.stream
    zpm = S19._zero_preceding(fab.dwell_id[:READ_AT], fab.is_exam[:READ_AT])   # per-wave, read-window-sliced

    n_onset_total = len(per_onset)
    win_all: dict = {}                                # col_t -> [acc] over ALL onsets (A-check)
    win_strat: dict = {}                              # col_t -> [acc] over IN-STRATUM onsets
    n_strat = 0
    for (wave, _dw, _pos, acc) in per_onset:
        col_t = (wave // EVAL + 1) * EVAL
        if col_t > READ_AT:
            continue
        win_all.setdefault(col_t, []).append(acc)
        if bool(zpm[wave]):
            win_strat.setdefault(col_t, []).append(acc)
            n_strat += 1

    cols_t = sorted(win_all)                          # the committed window grid (300..499800)
    series, n_none_postacq = [], 0
    strat_cols = []
    for t in cols_t:
        accs = win_strat.get(t)
        val = statistics.mean(accs) if accs else None
        strat_cols.append(dict(t=t, exam_acc=val, exam_n_strat=(len(accs) if accs else 0)))
        if t >= acquisition_onset:
            series.append(val)
            if val is None:
                n_none_postacq += 1
    return dict(seed=seed, n_onset_total=n_onset_total, n_stratum=n_strat,
                frac_stratum=round(n_strat / max(1, n_onset_total), 5),
                acquisition_onset=acquisition_onset, n_postacq_windows=len(series),
                n_none_postacq=n_none_postacq, post_acq_series=series, strat_cols=strat_cols)


def score() -> dict:
    # gather anchors + stratify every seed
    strat, anchors_all_green = {}, True
    for s in VERDICT_SEEDS:
        rep = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_{REPLAY_TAG}_anchors.json").read_text())
        if not rep["anchors"]["all_green"]:
            anchors_all_green = False
            print(f"s{s}: ANCHOR NOT GREEN — cannot trust the replay. {rep['anchors']}")
        strat[s] = stratify(s, rep["acquisition_onset"])

    if not anchors_all_green:
        return dict(HALT="anchors not all green — replay unfaithful; G5a cannot be read", ok=False)

    # per-seed post-acq stratified series (None = window with no in-stratum onset)
    series = {s: strat[s]["post_acq_series"] for s in VERDICT_SEEDS}
    series_nonone = {s: [x for x in series[s] if x is not None] for s in VERDICT_SEEDS}

    # --- re-cut (band, N) on the stratum null. PRIMARY = _provisional_cut (prereg-named); pooled over
    #     the verdict seeds' own stratified null (episode-excluded inside _provisional_cut).
    band_p, N_p, pooled_p = XA._provisional_cut(series_nonone)
    # SENSITIVITY = Ruling-B between-episode null (the committed cell used Ruling B)
    between = XA._between_episode_null(series_nonone)
    band_b, N_b = XA._joint_band_cut(between)

    def census(band, N):
        per_seed = {}
        for s in VERDICT_SEEDS:
            longest = _max_run_nonesafe(series[s], band)     # None breaks runs (conservative)
            per_seed[s] = dict(longest_run=longest, certifies=bool(longest >= N))
        cert = [s for s in VERDICT_SEEDS if per_seed[s]["certifies"]]
        return dict(band=round(band, 4), N=N, per_seed=per_seed,
                    certified_seeds=cert, n_certified=len(cert),
                    converters_certified=[s for s in cert if s in CONVERTERS],
                    nonconverters_certified=[s for s in cert if s in NONCONVERTERS])

    prov = census(band_p, N_p)
    rulingB = census(band_b, N_b)

    # the committed full-READ reproduction, for context ONLY (does NOT transport — reported to show the
    # contrast the stratum is being asked about)
    fullread = {}
    for s in VERDICT_SEEDS:
        rec = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_verdict.json").read_text())
        o = rec["acquisition_onset"]
        full = [c["exam_acc"] for c in rec["columns"]
                if c["t"] >= o and c.get("exam_acc") is not None]
        fullread[s] = dict(longest_run_064=_max_run_nonesafe(full, 0.64),
                           certifies_064x5=bool(_max_run_nonesafe(full, 0.64) >= 5))

    # -------- the G5a verdict. The gate is about the CONVERTERS: do the seeds that certified on the
    #          full read still certify on their recency-free stratum? Reported under BOTH null sources.
    conv_prov = prov["converters_certified"]
    conv_b = rulingB["converters_certified"]
    both_agree = set(conv_prov) == set(conv_b)
    # HALT trigger (ruling 4): if C_shuffle CANNOT certify on its own recency-free stratum at full N.
    # Read conservatively: viable iff at least one committed converter still certifies under BOTH nulls.
    viable = bool(conv_prov) and bool(conv_b)

    out = dict(
        gate="G5a — STRATUM VIABILITY (full N)", arm=ARM,
        committed_converters=CONVERTERS, committed_nonconverters=NONCONVERTERS,
        stratum_sizes={s: dict(n_stratum=strat[s]["n_stratum"], n_onset=strat[s]["n_onset_total"],
                               frac=strat[s]["frac_stratum"],
                               n_none_postacq=strat[s]["n_none_postacq"],
                               n_postacq_windows=strat[s]["n_postacq_windows"]) for s in VERDICT_SEEDS},
        recut_PRIMARY_provisional=dict(band=round(band_p, 4), N=N_p, n_null=len(pooled_p)),
        recut_SENSITIVITY_rulingB=dict(band=round(band_b, 4), N=N_b, n_null=len(between)),
        census_PRIMARY_provisional=prov,
        census_SENSITIVITY_rulingB=rulingB,
        fullread_reproduction_CONTEXT_ONLY=fullread,
        converters_certified_on_stratum=dict(provisional=conv_prov, rulingB=conv_b,
                                             agree=both_agree),
        VERDICT=("VIABLE — a committed converter still certifies on the recency-free stratum under both "
                 "null sources" if viable else
                 "HALT -> JASON: NO committed converter certifies on its own recency-free stratum at "
                 "full N -> the recency defence is DECORATIVE"),
        viable=viable, ok=True)
    (XA.OUTDIR / "exp19_g5a_verdict.json").write_text(json.dumps(out, indent=2))
    return out


def _print_score(out: dict):
    if not out.get("ok"):
        print("G5a HALT:", out.get("HALT"))
        return
    print("\n===== G5a — STRATUM VIABILITY (full N) =====")
    print(f"  re-cut PRIMARY (_provisional_cut): band={out['recut_PRIMARY_provisional']['band']} "
          f"N={out['recut_PRIMARY_provisional']['N']}  (n_null={out['recut_PRIMARY_provisional']['n_null']})")
    print(f"  re-cut SENSITIVITY (Ruling-B):     band={out['recut_SENSITIVITY_rulingB']['band']} "
          f"N={out['recut_SENSITIVITY_rulingB']['N']}  (n_null={out['recut_SENSITIVITY_rulingB']['n_null']})")
    print(f"  {'seed':>4} {'class':>5} {'n_strat':>8} {'frac':>7} {'none':>5} "
          f"{'full 0.64x5':>11} {'strat(prov)':>12} {'strat(RulB)':>12}")
    for s in VERDICT_SEEDS:
        cl = "CONV" if s in CONVERTERS else "non"
        ss = out["stratum_sizes"][s]
        fr = out["fullread_reproduction_CONTEXT_ONLY"][s]
        pp = out["census_PRIMARY_provisional"]["per_seed"][str(s)] if str(s) in out["census_PRIMARY_provisional"]["per_seed"] else out["census_PRIMARY_provisional"]["per_seed"][s]
        bb = out["census_SENSITIVITY_rulingB"]["per_seed"][str(s)] if str(s) in out["census_SENSITIVITY_rulingB"]["per_seed"] else out["census_SENSITIVITY_rulingB"]["per_seed"][s]
        print(f"  {s:>4} {cl:>5} {ss['n_stratum']:>8} {ss['frac']:>7.4f} {ss['n_none_postacq']:>5} "
              f"{('Y' if fr['certifies_064x5'] else '·')+' (run '+str(fr['longest_run_064'])+')':>11} "
              f"{('Y' if pp['certifies'] else '·')+' (run '+str(pp['longest_run'])+')':>12} "
              f"{('Y' if bb['certifies'] else '·')+' (run '+str(bb['longest_run'])+')':>12}")
    cc = out["converters_certified_on_stratum"]
    print(f"  converters certifying on stratum: provisional={cc['provisional']}  rulingB={cc['rulingB']}  "
          f"agree={cc['agree']}")
    print(f"\n  VERDICT: {out['VERDICT']}\n")


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--replay" in sys.argv:
        seed = int(sys.argv[sys.argv.index("--replay") + 1])
        replay_seed(seed)
    elif "--score" in sys.argv:
        _print_score(score())
    else:
        print("usage: exp19_g5a.py --replay SEED   |   --score")
