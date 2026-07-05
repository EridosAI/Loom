"""12b stage-two DERIVATION (prereg §15 — PROPOSAL; constants surface in chat before any
verdict twin).

Derives, from the cal twins ({20–24} × {present, absent} × {shuffled, dwelled}, 160k):

  1. Per-partition S NULL BANDS. S per seed per window = Δsep_cat − mean(Δsep_dist,
     Δsep_a), Δ = present − absent (twin contrast at the same window t on bit-identical
     fabric). NULL SOURCES (registered): (a) PRE-ACQUISITION windows — before the
     PRESENT twin's num-floor onset the word channel is unacquired, so no selective
     effect exists; S there is pure instrument noise (primary band source, one-sided
     p99); (b) the UNTIED-UNTIED companion Δsep_dist − Δsep_a over the whole run
     (null if the word treats untied partitions equally — reported alongside). The cal
     twins' POST-onset S is NOT a null (it would absorb a real effect) and never enters
     the band.
  2. Sustained-N: smallest N with zero empirical false-fires of "S > band-p99 for N
     consecutive windows" on the pooled null segments.
  3. Per-fabric horizons: shuffled-12b = max measured present-twin cal onset + W +
     margin (short); dwelled-12b carries the 303,400 form + the UNREAD/truncation
     machinery. W = the in-force 131,400 common window (comparability with the rig-1
     ruler) unless ratified otherwise.
  4. Aligned-window form (PROPOSED): per seed, [onset_present, onset_present + W] — the
     present twin's num onset anchors BOTH twins (the absent twin's word channel may
     never acquire; its num onset is a companion, never an anchor).
  5. Dead-reference regime check: the dead-signature asg_cat distribution under the new
     mask policy vs the in-force theta's provenance (dead p50 ~4e-5 / p95 0.00566).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp09_arms as X9                                       # noqa: E402
import exp12_arms as X12                                      # noqa: E402

OUTDIR = X12.OUTDIR
CAL = X12.CAL_SEEDS
MARGIN = 12000
W_COMMON = 131400
FABRICS = dict(sh=("exp12_12bc_shp", "exp12_12bc_sha"), dw=("exp12_12bc_dwp", "exp12_12bc_dwa"))
# (the struck-(iii) arms exp12_12b_* stay on disk for the record; this derivation reads
# the COIN-POLICY twins per §15 as amended — bounded sep columns, nothing transported)


def _load(arm, seed):
    return json.loads((OUTDIR / f"{arm}_s{seed}.json").read_text())


def _s_series(rp, ra):
    """Per-window S + untied-untied companion from a twin pair (matched t; None-guarded)."""
    out = []
    for cp, ca in zip(rp["columns"], ra["columns"]):
        assert cp["t"] == ca["t"]
        vals = {}
        for k in ("sep_cat", "sep_dist", "sep_a"):
            if cp.get(k) is None or ca.get(k) is None:
                vals = None
                break
            vals[k] = cp[k] - ca[k]
        if vals is None:
            out.append(dict(t=cp["t"], S=None, uu=None))
            continue
        out.append(dict(t=cp["t"],
                        S=vals["sep_cat"] - 0.5 * (vals["sep_dist"] + vals["sep_a"]),
                        uu=vals["sep_dist"] - vals["sep_a"]))
    return out


def _fires(vals, thr, n):
    run = 0
    for v in vals:
        run = run + 1 if (v is not None and v > thr) else 0
        if run >= n:
            return True
    return False


def propose12b():
    out = dict(status="PROPOSED — surfaces in chat before any verdict twin",
               W_common=W_COMMON, margin=MARGIN)
    for fkey, (armP, armA) in FABRICS.items():
        null_S, null_uu, onsets_p, onsets_a, degen = [], [], [], [], 0
        series_by_seed = {}
        for s in CAL:
            rp, ra = _load(armP, s), _load(armA, s)
            onset_p = rp["acquisition_onset"]
            onsets_p.append(onset_p)
            onsets_a.append(ra["acquisition_onset"])
            ser = _s_series(rp, ra)
            series_by_seed[s] = (ser, onset_p)
            degen += sum(1 for x in ser if x["S"] is None)
            for x in ser:
                if x["uu"] is not None:
                    null_uu.append(x["uu"])
                if x["S"] is not None and (onset_p is None or x["t"] < onset_p):
                    null_S.append(x["S"])
        ns = sorted(null_S)
        band = ns[int(0.99 * len(ns))] if ns else None
        # sustained-N: smallest N with zero false-fires on the pooled null segments
        n_sust = None
        if band is not None:
            for n in range(2, 12):
                ff = 0
                for s in CAL:
                    ser, onset_p = series_by_seed[s]
                    seg = [x["S"] for x in ser if onset_p is None or x["t"] < onset_p]
                    ff += int(_fires(seg, band, n))
                if ff == 0:
                    n_sust = n
                    break
        uu = sorted(null_uu)
        # post-onset S preview (NEVER a band input; surfaced so the ratification sees
        # what the cal twins actually show)
        post_preview = {}
        for s in CAL:
            ser, onset_p = series_by_seed[s]
            if onset_p is None:
                post_preview[f"s{s}"] = None
                continue
            seg = [x["S"] for x in ser if x["t"] >= onset_p and x["S"] is not None]
            post_preview[f"s{s}"] = round(statistics.mean(seg), 4) if seg else None
        censored = sum(1 for o in onsets_p if o is None)
        max_on = max((o for o in onsets_p if o is not None), default=None)
        horizon = (dict(value=303400, form="dwelled carries the 303,400 form + full "
                                           "UNREAD/truncation machinery")
                   if fkey == "dw" else
                   dict(value=(max_on + W_COMMON + MARGIN) if max_on and not censored
                        else None,
                        form=f"max present-twin cal onset ({max_on}"
                             f"{' — CENSORED SEED PRESENT, bound is a >=' if censored else ''})"
                             f" + W({W_COMMON}) + margin({MARGIN})"))
        out[fkey] = dict(
            arms=[armP, armA],
            onsets_present=onsets_p, onsets_absent=onsets_a,
            null_band=dict(n_windows=len(ns),
                           p50=(round(ns[len(ns) // 2], 5) if ns else None),
                           p99=(round(band, 5) if band is not None else None),
                           max=(round(ns[-1], 5) if ns else None),
                           source="pre-acquisition (present-twin num onset) windows, "
                                  "pooled over cal twin pairs"),
            sustained_N=n_sust,
            untied_untied=dict(n=len(uu),
                               p50=round(uu[len(uu) // 2], 5) if uu else None,
                               p99=round(uu[int(0.99 * len(uu))], 5) if uu else None),
            degenerate_windows=degen,
            post_onset_S_preview_NOT_A_BAND_INPUT=post_preview,
            aligned_window="per seed: [onset_present, onset_present + W_common]; the "
                           "absent twin anchored to the PRESENT twin's onset",
            horizon=horizon)
    # CHANNEL-ALIVE CHECK (the coin policy's precondition — the (iii) regime finding
    # that forced the re-pose is the RECORD in git history / §10.20.3, not this block)
    num_max_p = num_max_a = 0.0
    for arms in FABRICS.values():
        for s in CAL:
            num_max_p = max(num_max_p, max(c["num"] for c in _load(arms[0], s)["columns"]))
            num_max_a = max(num_max_a, max(c["num"] for c in _load(arms[1], s)["columns"]))
    out["channel_alive_check"] = dict(
        num_max_present=round(num_max_p, 4), num_max_absent=round(num_max_a, 6),
        note="present twins acquire under the coin policy (the dose carries the "
             "channel); absent twins never do — BY CONSTRUCTION (no word to bind), "
             "which is why the aligned window anchors on the PRESENT twin's onset")
    # fresh dead reference at the coin policy (companion bar only — never the S verdict;
    # pooled dead-signature windows, whole-run: absent twins have no onsets to gate on)
    dead = []
    for arms in FABRICS.values():
        for a in arms:
            for s in CAL:
                rec = _load(a, s)
                dead += [c["asg_cat"] for c in rec["columns"]
                         if c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR]
    ds = sorted(dead)
    q = lambda f: round(ds[int(f * len(ds))], 6) if ds else None
    out["dead_reference_coin_policy"] = dict(
        n_dead_windows=len(ds), gating="whole-run pooled (absent twins have no onset)",
        p50=q(0.50), p95=q(0.95), p99=q(0.99),
        theta_companion_proposed=q(0.95),
        note="FRESH-CUT at the coin policy per the nothing-transports ruling; companion "
             "bar for asg_cat routing-health context only — never an S-verdict input")
    (OUTDIR / "exp12_12b_stage2.PROPOSED.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))
    return out


def record_sw():
    """§10.20.5: register the S_w constants from the EXISTING cal twins (no new cal).
    S_w per window = sep_cat(present) − sep_cat(absent), bounded form. Null band =
    pre-onset pooled Δsep_cat per fabric (same source/construction as the S band: sh
    over the widened {20–29} pool, dw over {20–24}); sustained-N re-checked for zero
    false-fires. Everything else carries in force. Updates the constants artifact in
    place (the composite-S bands stay recorded as companions-of-record)."""
    K = json.loads((OUTDIR / "exp12_12b_stage2_constants.json").read_text())
    for fkey, (armP, armA) in FABRICS.items():
        seeds = CAL + ([25, 26, 27, 28, 29] if fkey == "sh" else [])
        null_w = []
        series = {}
        for s in seeds:
            rp, ra = _load(armP, s), _load(armA, s)
            onset_p = rp["acquisition_onset"]
            ser = []
            for cp, ca in zip(rp["columns"], ra["columns"]):
                assert cp["t"] == ca["t"]
                v = (cp["sep_cat"] - ca["sep_cat"]
                     if cp.get("sep_cat") is not None and ca.get("sep_cat") is not None
                     else None)
                ser.append(dict(t=cp["t"], Sw=v))
            series[s] = (ser, onset_p)
            null_w += [x["Sw"] for x in ser
                       if x["Sw"] is not None and (onset_p is None or x["t"] < onset_p)]
        ns = sorted(null_w)
        band = ns[int(0.99 * len(ns))]
        n_sust = None
        for n in range(2, 12):
            ff = 0
            for s in seeds:
                ser, onset_p = series[s]
                seg = [x["Sw"] for x in ser if onset_p is None or x["t"] < onset_p]
                ff += int(_fires(seg, band, n))
            if ff == 0:
                n_sust = n
                break
        K[fkey]["Sw_band_p99"] = round(band, 6)
        K[fkey]["Sw_band_n_windows"] = len(ns)
        K[fkey]["Sw_sustained_N"] = n_sust
        K[fkey]["Sw_note"] = ("S_w = dsep_cat alone (§10.20.5 re-cut; untied legs + "
                              "composite S demoted to reported companions); band from "
                              "the SAME pre-onset null source, existing cal only")
    K["status"] = (K["status"] + " | S_w REGISTERED 2026-07-05 (§10.20.5): primary = "
                   "word-tied contrast alone; fresh-seed discipline — verdict {5–9}, "
                   "never the {0–4} that motivated the re-cut")
    (OUTDIR / "exp12_12b_stage2_constants.json").write_text(json.dumps(K, indent=2))
    print(json.dumps({f: {k: K[f][k] for k in ("Sw_band_p99", "Sw_band_n_windows",
                                               "Sw_sustained_N")} for f in FABRICS},
                     indent=1))
    return K


def record_inforce12b():
    """Record the 12b coin-policy constants IN FORCE (chat ratification 2026-07-05:
    the widen amendment + two fences + rest-as-proposed). The shuffled band is RE-CUT
    over the fattened pool (cal {20–29}, 10 twin pairs — grounds recorded before the
    wider numbers existed: p99 from n=89 is essentially the pool max, unstable as a
    primary-axis ruler); N re-checked for zero false-fires on the fatter pool. The
    dwelled band stands from {20–24} (n=1414, not thin). Nothing transported."""
    out = dict(status="IN FORCE (ratified in chat 2026-07-05; widen amendment + "
                      "preview fence + dwelled-lottery pre-acknowledgement)",
               W_common=W_COMMON, margin=MARGIN,
               fences=dict(
                   preview="the post-onset S preview is a LOGGED LEAN: cal-only, "
                           "sustained-ness unchecked, never touches constants (all "
                           "derive from pre-onset nulls and dead pools — "
                           "preview-independent grounds); verdict seeds {0–4} are the test",
                   dwelled_lottery="pre-acknowledged, no improvisation: <3 dwelled reads "
                                   "post-extension → UNREAD-AT-HORIZON → horizon re-pin "
                                   "returns to chat as a recorded amendment"))
    for fkey, (armP, armA) in FABRICS.items():
        seeds = CAL + ([25, 26, 27, 28, 29] if fkey == "sh" else [])
        null_S, onsets_p = [], []
        series = {}
        for s in seeds:
            rp, ra = _load(armP, s), _load(armA, s)
            onset_p = rp["acquisition_onset"]
            onsets_p.append(onset_p)
            ser = _s_series(rp, ra)
            series[s] = (ser, onset_p)
            null_S += [x["S"] for x in ser
                       if x["S"] is not None and (onset_p is None or x["t"] < onset_p)]
        ns = sorted(null_S)
        band = ns[int(0.99 * len(ns))]
        n_sust = None
        for n in range(2, 12):
            ff = 0
            for s in seeds:
                ser, onset_p = series[s]
                seg = [x["S"] for x in ser if onset_p is None or x["t"] < onset_p]
                ff += int(_fires(seg, band, n))
            if ff == 0:
                n_sust = n
                break
        max_on = max((o for o in onsets_p if o is not None), default=None)
        censored = sum(1 for o in onsets_p if o is None)
        horizon = 303400 if fkey == "dw" else 152400
        out[fkey] = dict(
            arms=[armP, armA], cal_seeds=seeds,
            band_p99=round(band, 6), band_n_windows=len(ns),
            sustained_N=n_sust,
            onsets_present=onsets_p, censored_cal=censored,
            horizon=horizon, read_cutoff=horizon - W_COMMON,
            aligned_window="[onset_present, onset_present + W_common]",
            note=("band RE-CUT over the widened pool per the ratified amendment; "
                  "replaces the thin-pool 0.0414 whichever direction it moved"
                  if fkey == "sh" else "band stands from {20–24} (n=1414, not thin)"))
    # theta companion (ratified as proposed, companion only)
    out["theta_companion"] = dict(value=0.007751, role="asg_cat routing-health context "
                                                       "ONLY — never an S-verdict input")
    (OUTDIR / "exp12_12b_stage2_constants.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: (v if k in ("sh", "dw") else v)
                      for k, v in out.items() if k in ("sh", "dw")}, indent=1))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--record-inforce", action="store_true")
    ap.add_argument("--record-sw", action="store_true")
    args = ap.parse_args()
    if args.record_inforce:
        record_inforce12b()
    elif args.record_sw:
        record_sw()
    else:
        propose12b()
