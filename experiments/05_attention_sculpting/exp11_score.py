"""EXP11 scoring — the coverage-on-routing-survival read (one-review prep).

Per §9 pins: BOTH axes acquisition-aligned; the routing verdict = asg_dist
(input-sensitivity, NOT argmax_k count) over a MATCHED POST-ONSET WINDOW of W_post=3
collapse periods IN EACH RUNG'S OWN REGIME. Per-rung period + the asg_dist survival
threshold are IN-REGIME stage-two constants derived from the ladder's OWN acquired
verdict seeds (not the thin n=2 cal periods, and never static constants).

Reads:
  - acquisition (≥3 acquired/rung gate; ACQUISITION-STARVED if not);
  - the natural ladder: does asg_dist survival rise with coverage;
  - the GEOMETRY FORK (a/b/c): does it run uphill or downhill against the ~min-sep drop;
  - the MATCHED-SEPARATION control: does the coverage effect survive equalized min-sep;
  - the CRUTCH screen: asg_dist survival vs argmax_k count (Form 1); Form-2 residual named.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp09_arms as X9                                       # noqa: E402
import exp11_arms as X11                                      # noqa: E402

OUTDIR = X11.OUTDIR
RUNGS = X11.RUNGS
SEEDS = X11.VERDICT_SEEDS
W = X11.W_POST_PERIODS


def _load(vocab, seed, matched):
    return json.loads((OUTDIR / f"{X11._arm_name(vocab, matched)}_s{seed}.json").read_text())


def _rung_period(recs):
    """IN-REGIME per-rung collapse period: median dominant den-period over the rung's own
    acquired verdict seeds, post-onset healthy segment (robust vs the n=2 cal estimate)."""
    ps = []
    for r in recs:
        on = r["acquisition_onset"]
        if on is None:
            continue
        post = [c for c in r["columns"] if c["t"] >= on]
        if len(post) >= 8:
            p = X9.dynamics_panel([c["t"] for c in post], [c["den"] for c in post])["dominant_period_steps"]
            ps.append(p or X9.PERIOD_WORD)
    return int(statistics.median(ps)) if ps else X9.PERIOD_WORD


def _survival(rec, period):
    """asg_dist survival over the matched post-onset window + argmax_k companion (crutch)."""
    on = rec["acquisition_onset"]
    if on is None:
        return None
    hi = on + W * period
    win = [c for c in rec["columns"] if on <= c["t"] <= hi]
    if not win or win[-1]["t"] < hi - X11.EVAL:
        return dict(short=True, have=len(win))
    asg = [c["asg_dist"] for c in win]
    return dict(short=False, n=len(win),
                asg_mean=statistics.mean(asg), asg_min=min(asg),
                asg_frac_alive=sum(1 for a in asg if a > 0.1) / len(asg),
                argmax_k_med=statistics.median(c["asg_argmax_k"] for c in win))


def score_ladder(matched: bool):
    out = {}
    for v in RUNGS:
        recs = [_load(v, s, matched) for s in SEEDS]
        acq = [r for r in recs if r["acquisition_onset"] is not None]
        period = _rung_period(recs)
        survs = [(_survival(r, period), r) for r in acq]
        read = [(s, r) for s, r in survs if s and not s.get("short")]
        starved = len(acq) < 3
        out[v] = dict(
            acquired=len(acq), starved=bool(starved), period=period,
            min_sep=round(statistics.mean(r["anchor_min_sep"] for r in recs), 4),
            mean_sep=round(statistics.mean(r["anchor_mean_sep"] for r in recs), 4),
            n_read=len(read),
            asg_mean=round(statistics.mean(s["asg_mean"] for s, _ in read), 4) if read else None,
            asg_mean_sd=round(statistics.pstdev([s["asg_mean"] for s, _ in read]), 4) if len(read) > 1 else None,
            asg_frac_alive=round(statistics.mean(s["asg_frac_alive"] for s, _ in read), 3) if read else None,
            argmax_k_med=round(statistics.mean(s["argmax_k_med"] for s, _ in read), 2) if read else None,
            per_seed_asg=[round(s["asg_mean"], 4) for s, _ in read],
        )
    return out


def monotone(vals):
    v = [x for x in vals if x is not None]
    if len(v) < 2:
        return None
    ups = sum(1 for i in range(len(v) - 1) if v[i + 1] > v[i])
    return dict(values=v, up_steps=ups, of=len(v) - 1,
                spearman_dir=("increasing" if v[-1] > v[0] else "flat/decreasing"),
                endpoint_ratio=round(v[-1] / v[0], 2) if v[0] else None)


def _asg_full(rec):
    """Estimator-free verdict read: mean asg_dist over the WHOLE post-onset run. The
    period-normalized window is RETRACTED (verification: the per-rung den-period is
    fallback-dominated — 3/5 estimator failures on some rungs, 6x cal-vs-in-regime swing
    — so 'W_post = 3 periods in the rung's own regime' is effectively arbitrary-length)."""
    on = rec["acquisition_onset"]
    if on is None:
        return None
    w = [c["asg_dist"] for c in rec["columns"] if c["t"] >= on]
    return statistics.mean(w) if w else None


def _honest():
    """The verification-corrected read: estimator-free full-post-onset window; within-rung
    nat-vs-ms (coverage fixed); pooled min-sep dose."""
    out = dict(full_window={}, within_rung={})
    for v in RUNGS:
        nat = [x for x in (_asg_full(_load(v, s, False)) for s in SEEDS) if x is not None]
        ms = [x for x in (_asg_full(_load(v, s, True)) for s in SEEDS) if x is not None]
        out["full_window"][f"v{v}"] = dict(
            nat_mean=round(statistics.mean(nat), 4), nat_sd=round(statistics.pstdev(nat), 4),
            ms_mean=round(statistics.mean(ms), 4), ms_sd=round(statistics.pstdev(ms), 4),
            min_sep=round(statistics.mean(_load(v, s, False)["anchor_min_sep"] for s in SEEDS), 4))
        out["within_rung"][f"v{v}"] = round(statistics.mean(ms) - statistics.mean(nat), 4)
    xs, ys = [], []
    for v in RUNGS:
        for m in (False, True):
            for s in SEEDS:
                r = _load(v, s, m); a = _asg_full(r)
                if a is not None:
                    xs.append(r["anchor_min_sep"]); ys.append(a)
    n = len(xs); mx = statistics.mean(xs); my = statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    out["pooled_minsep_corr"] = round(cov / (statistics.pstdev(xs) * statistics.pstdev(ys)), 3)
    nat_full = [out["full_window"][f"v{v}"]["nat_mean"] for v in RUNGS]
    out["nat_full_trend"] = monotone(nat_full)
    out["verdict"] = "INCONCLUSIVE"
    out["reading"] = (
        "Natural ladder rises ~monotonically with coverage on the estimator-free window "
        f"({'/'.join(str(x) for x in nat_full)}) BUT coverage is collinear with anchor "
        "min-sep AND onset; the matched-sep control meant to separate them is CONFOUNDED "
        "(non-uniform closest-pair perturbation — heavy at v2, ~zero at v16 — lifts ONLY "
        "v2 (within-rung " + str(out["within_rung"]) + "), so its flatness is a "
        "construction artifact, not clean coverage-null); pooled min-sep corr "
        f"{out['pooled_minsep_corr']} is coverage/perturbation collinearity, NOT a "
        "within-rung dose (v4/v8/v16 flat-or-negative). Neither COVERAGE-SCAFFOLD nor "
        "COVERAGE-NULL established; underpowered n=5. Loose thread (named, not a "
        "mechanism): heavily re-perturbing the v2 category-only anchor lifts survival ~4x "
        "via an UNIDENTIFIED channel. Clean redo needs a UNIFORM matched-min-sep control "
        "(or D-scaling), a fixed common window, and more seeds.")
    return out


def main():
    nat = score_ladder(False)
    ms = score_ladder(True)
    honest = _honest()
    # geometry fork on the NATURAL ladder
    nat_asg = [nat[v]["asg_mean"] for v in RUNGS]
    nat_minsep = [nat[v]["min_sep"] for v in RUNGS]
    survives_more = (nat_asg[-1] or 0) > (nat_asg[0] or 0)
    sep_degrades = nat_minsep[-1] < nat_minsep[0]
    fork = ("(a) survives-more DESPITE degrading min-sep — coverage dominates (uphill)"
            if survives_more and sep_degrades else
            "(c) survives-more AND sep holds" if survives_more and not sep_degrades else
            "(b) survives-less AND sep degrades — CONFOUNDED" if not survives_more and sep_degrades else
            "survives-less, sep holds — density-null-ish")
    # matched-sep: does the coverage trend survive equalized min-sep?
    ms_asg = [ms[v]["asg_mean"] for v in RUNGS]
    # crutch: asg_dist trend vs argmax_k trend (Form 1)
    result = dict(
        HONEST_READ=honest,                                # verification-corrected primary
        period_normalized_RETRACTED=dict(
            natural=nat, matched_sep=ms,
            note="RETRACTED window (period fallback-dominated); kept for provenance only"),
        acquisition=dict((f"v{v}", dict(nat=nat[v]["acquired"], ms=ms[v]["acquired"],
                                        starved=nat[v]["starved"] or ms[v]["starved"]))
                         for v in RUNGS),
    )
    (OUTDIR / "exp11_verdicts.json").write_text(json.dumps(result, indent=2))
    print("VERDICT:", honest["verdict"])
    print("full-window nat trend:", honest["nat_full_trend"])
    print("within-rung (coverage fixed, ms-nat):", honest["within_rung"])
    print("pooled min-sep corr:", honest["pooled_minsep_corr"])
    print(f"{'rung':>5} {'acq':>4} {'period':>7} {'min_sep':>8} | "
          f"{'NATURAL asg':>12} {'frac_alive':>10} {'argmax_k':>9} | {'MATCHED-SEP asg':>15}")
    for v in RUNGS:
        n, m = nat[v], ms[v]
        print(f"{'v'+str(v):>5} {n['acquired']}/{m['acquired']:<2} {n['period']:>7} "
              f"{n['min_sep']:>8.3f} | {str(n['asg_mean']):>12} {str(n['asg_frac_alive']):>10} "
              f"{str(n['argmax_k_med']):>9} | {str(m['asg_mean']):>15}")
    print("-> exp11_verdicts.json")


if __name__ == "__main__":
    main()
