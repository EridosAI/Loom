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
    # THE REGIME FINDING (cal outcome, 2026-07-05): under mask policy (iii) the num
    # channel NEVER forms — max num over all 20 cal runs = 2.6e-5 (vs 0.284 at the same
    # seed under the scheduled policy); onsets None 20/20; present and absent twins
    # indistinguishable on every panel; the (iii)-world also collapses harder (9/20 end
    # argmax_k=1; 15/20 end den < 1e-3; both dwelled twins fully dead-dictionary on
    # most seeds). CONSEQUENCE: the aligned-window anchor has ZERO support, the S index
    # has no post-onset windows to read, and the raw S form is unbounded (ratio
    # explosion as within->0; null-band max 141094) — CONSTANTS ARE NOT SETTABLE for
    # the registered machinery. Surfaced for ruling; verdict twins DO NOT run.
    num_max = 0.0
    for arms in FABRICS.values():
        for a in arms:
            for s in CAL:
                rec = _load(a, s)
                num_max = max(num_max, max(c["num"] for c in rec["columns"]))
    out["REGIME_FINDING"] = dict(
        num_max_over_all_20_runs=num_max,
        onsets="None 20/20 (present AND absent twins, both fabrics)",
        s_form_note="raw ratio-difference S is unbounded (within->0 explosion); any "
                    "re-pin should use a bounded form, e.g. between/(between+within)",
        reading="the zero-prediction-load word is INERT — the channel the teaching "
                "test needs never comes alive to test under policy (iii)")
    # dead-reference regime check — UNGATED (onset gating is vacuous here: no onsets)
    dead = []
    for arms in FABRICS.values():
        for a in arms:
            for s in CAL:
                rec = _load(a, s)
                dead += [c["asg_cat"] for c in rec["columns"]
                         if c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR]
    ds = sorted(dead)
    q = lambda f: round(ds[int(f * len(ds))], 6) if ds else None
    out["dead_reference_regime_check"] = dict(
        n_dead_windows=len(ds), gating="UNGATED whole-run (no onsets exist)",
        p50=q(0.50), p95=q(0.95), p99=q(0.99),
        inforce_reference=dict(p50=3.9e-05, p95=0.00566),
        note="SHIFTED: new-policy dead p95 0.0086 = 1.5x the in-force provenance — the "
             "asg_cat companion must not be read against theta unflagged under (iii)")
    (OUTDIR / "exp12_12b_stage2.PROPOSED.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
    propose12b()
