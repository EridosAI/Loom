"""exp19_g5a_fork.py — the G5a-fork TRIGGER + the (0.704,7) false-rate sensitivities (Jason, 2026-07-14).

THE FORK IS A TEST, NOT A CHOICE. Ruling-B exists because C_shuffle's CAL seeds convert, leaving no clean
marginal to build a null from (committed: 4/5 s0-class on the full read). That is a fact about a REGIME. The
stratum is a DIFFERENT regime. Compute whether the trigger fires there:
  cal seeds CONVERT on the zero-preceding stratum  -> Ruling-B FORCED (no clean marginal; provisional's null
                                                       is contaminated).
  cal seeds DO NOT convert on the stratum           -> _provisional_cut CORRECT; importing Ruling-B is a
                                                       TRANSPORT VIOLATION (calibrate-in-regime, nothing
                                                       transports).
The procedure follows from the trigger. The leak evidence rides as CONFIRMATION, never as grounds.

Also (before G5b): the cut landed at band=0.704=S0_LEVEL=EPISODE_BAND, N=7 = one below the exclusion length
EPISODE_MIN=8. Report the false-rate at (0.704, {6,7,8}), the cut's ALPHA-sensitivity, and whether
band=EPISODE_BAND is forced (null quantiles all exceed the cap) or coincidental.

  --replay-cal SEED   deterministic replay + capture + anchor (vs committed *_cal2.*) for a cal seed
  --trigger           s0-class conversion of each cal seed ON THE STRATUM -> fires / doesn't
  --sensitivity       (0.704,N) false-rates, ALPHA sweep, band-forced check on the verdict stratum null
"""
from __future__ import annotations

import json
import statistics
import sys

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp19_score as S19
import exp19_replay as R

EVAL = XA.EVAL
READ_AT = R.READ_AT
H_MAX = R.H_MAX
ARM = "exp12_shuffle"
CAL_SEEDS = [20, 21, 22, 24, 25]
VERDICT_SEEDS = list(range(8))
CAL_TAG = "g5a_cal_replay"
VERDICT_TAG = "g5a_replay"
S0_BAND, S0_MIN = XA.EPISODE_BAND, XA.EPISODE_MIN     # 0.704, 8 — the honest-null exclusion criterion


def _strat_post_acq_series(seed: int, tag: str, acquisition_onset) -> tuple[list, int, int]:
    """Rebuild the fabric, restrict the captured per-onset series to the zero-preceding stratum, re-bin to
    300-step windows, return the POST-ACQ per-window series (None = window with no in-stratum onset)."""
    cap = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{seed}_{tag}_peronset.json").read_text())
    loop, spec, cfg = X12.build_exp12(ARM, seed, H_MAX)
    fab = loop.stream
    zpm = S19._zero_preceding(fab.dwell_id[:READ_AT], fab.is_exam[:READ_AT])
    win: dict = {}
    n_strat = 0
    for (wave, _dw, _pos, acc) in cap["per_onset"]:
        col = (wave // EVAL + 1) * EVAL
        if col > READ_AT:
            continue
        if bool(zpm[wave]):
            win.setdefault(col, []).append(acc)
            n_strat += 1
    cols_t = [t for t in range(EVAL, READ_AT + 1, EVAL)]
    series = []
    for t in cols_t:
        if t >= acquisition_onset:
            accs = win.get(t)
            series.append(statistics.mean(accs) if accs else None)
    return series, n_strat, sum(1 for x in series if x is None)


def _s0class_run(series, band=S0_BAND) -> int:
    """Longest run of consecutive windows >= band (None breaks runs — conservative)."""
    best = cur = 0
    for a in series:
        cur = cur + 1 if (a is not None and a >= band) else 0
        best = max(best, cur)
    return best


# ---------------------------------------------------------------- --replay-cal
def replay_cal(seed: int):
    rec, per = R.capture_run(ARM, seed, out_tag=CAL_TAG)
    anch = R.verify_anchors(ARM, seed, CAL_TAG, per, rec, verdict_tag="cal2")
    R.write_capture(ARM, seed, per, CAL_TAG)
    rep = dict(seed=seed, acquisition_onset=rec["acquisition_onset"], anchors=anch)
    (XA.OUTDIR / f"exp14_{ARM}_s{seed}_{CAL_TAG}_anchors.json").write_text(json.dumps(rep, indent=2))
    tag = "ALL-GREEN" if anch["all_green"] else "!!! ANCHOR RED !!!"
    print(f"cal s{seed}: {tag}  A1={anch['A1_bitexact']} A2={anch['A2_columns']} A3={anch['A3_consistency']}"
          f"  n_onset={anch['n_onset_captured']}  acq={rec['acquisition_onset']}")
    if not anch["all_green"]:
        for k in ("A1_div", "A2_div", "A3_div"):
            if anch[k]:
                print(f"    {k}: {anch[k]}")


# ---------------------------------------------------------------- --trigger
def trigger() -> dict:
    rows, any_red = {}, False
    for s in CAL_SEEDS:
        rep = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_{CAL_TAG}_anchors.json").read_text())
        if not rep["anchors"]["all_green"]:
            any_red = True
            print(f"cal s{s}: ANCHOR NOT GREEN — {rep['anchors']}")
        series, n_strat, n_none = _strat_post_acq_series(s, CAL_TAG, rep["acquisition_onset"])
        # committed full-read s0-class run for the same seed (context)
        crec = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_cal2.json").read_text())
        o = crec["acquisition_onset"]
        full = [c["exam_acc"] for c in crec["columns"] if c.get("exam_acc") is not None and c["t"] >= o]
        rows[s] = dict(n_stratum=n_strat, n_none=n_none,
                       full_s0class_run=_s0class_run(full),
                       strat_s0class_run=_s0class_run(series),                  # >=0.704 x ? (s0-class = >=8)
                       strat_run_060=_s0class_run(series, 0.60),                # Ruling-B exclusion band
                       strat_run_064=_s0class_run(series, 0.64),               # full-read cert band
                       converts_stratum_s0class=bool(_s0class_run(series) >= S0_MIN))
    if any_red:
        return dict(HALT="cal anchors not green", ok=False)
    n_full = sum(1 for s in CAL_SEEDS if rows[s]["full_s0class_run"] >= S0_MIN)
    n_strat_conv = sum(1 for s in CAL_SEEDS if rows[s]["converts_stratum_s0class"])
    fires = n_strat_conv > 0
    out = dict(gate="G5a-fork TRIGGER (do C_shuffle CAL seeds convert on the zero-preceding stratum?)",
               cal_seeds=CAL_SEEDS, s0class_criterion=f">= {S0_BAND} x {S0_MIN} consec windows",
               per_seed=rows, n_convert_fullread=n_full, n_convert_stratum=n_strat_conv,
               trigger_fires=fires,
               RULING=("Ruling-B FORCED — cal seeds convert on the stratum -> no clean marginal; "
                       "_provisional_cut's null is contaminated" if fires else
                       "_provisional_cut CORRECT — cal seeds do NOT convert on the stratum -> clean marginal; "
                       "importing Ruling-B would be a transport violation"),
               ok=True)
    (XA.OUTDIR / "exp19_g5a_fork_trigger.json").write_text(json.dumps(out, indent=2))
    return out


# ---------------------------------------------------------------- --sensitivity
def sensitivity() -> dict:
    # rebuild the verdict-seed stratum post-acq null (s0-class excluded, exactly _provisional_cut's pool)
    per_seed = {}
    for s in VERDICT_SEEDS:
        rep = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_{VERDICT_TAG}_anchors.json").read_text())
        series, _n, _none = _strat_post_acq_series(s, VERDICT_TAG, rep["acquisition_onset"])
        per_seed[s] = [x for x in series if x is not None]
    band, N, pooled = XA._provisional_cut(per_seed)               # the committed cut on the stratum null
    xs = sorted(pooled)
    quant = {p: round(XA._quantile(xs, p), 4) for p in (0.90, 0.95, 0.975, 0.99)}
    fr = {n: XA._consec_rate(pooled, S0_BAND, n) for n in (5, 6, 7, 8)}
    # ALPHA sweep: smallest N (>=3) with false-rate <= alpha at band 0.704
    def smallest_N(alpha):
        for n in range(3, XA.S0_N + 1):
            if XA._consec_rate(pooled, S0_BAND, n) <= alpha:
                return n
        return None
    alphas = [3e-4, 5e-4, 7.13e-4, 1e-3, 1.5e-3, 2.06e-3, 2.5e-3, 3e-3, 5e-3]
    alpha_sweep = {f"{a:.2e}": smallest_N(a) for a in alphas}
    band_forced = all(q > S0_BAND for q in quant.values())        # every quantile above the cap => forced
    out = dict(gate="G5a re-cut sensitivities (band=0.704=EPISODE_BAND, N=7 vs exclusion 8)",
               n_null=len(pooled), cut_band=round(band, 4), cut_N=N, alpha_house=XA.ALPHA,
               null_quantiles=quant, band_is_EPISODE_BAND_forced=band_forced,
               false_rate_at_0704={str(n): fr[n] for n in fr},
               alpha_to_smallest_N=alpha_sweep,
               note=("band=0.704 is forced: every null quantile exceeds the S0_LEVEL cap, so _joint_band_cut "
                     "can only return the cap. N=7 is the smallest N with false-rate<=ALPHA=1e-3; "
                     "N=6 fails, N=8 is the exclusion length. The margin: fr(N=6) vs ALPHA."
                     if band_forced else
                     "band=0.704 is NOT forced by the cap — a lower band is admissible; investigate."),
               ok=True)
    (XA.OUTDIR / "exp19_g5a_fork_sensitivity.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--replay-cal" in sys.argv:
        replay_cal(int(sys.argv[sys.argv.index("--replay-cal") + 1]))
    elif "--trigger" in sys.argv:
        print(json.dumps(trigger(), indent=2))
    elif "--sensitivity" in sys.argv:
        print(json.dumps(sensitivity(), indent=2))
    else:
        print("usage: --replay-cal SEED | --trigger | --sensitivity")
