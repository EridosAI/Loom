"""EXP12 stage-two constant DERIVATION (PROPOSAL — nothing here is in force until
ratified in chat; §13.4–5 'threshold + cell boundaries recorded pre-run at stage-two').

Derives, from the CORRECTED-LAW cal artifacts (cal seeds {20–24}, both arms, never
verdict seeds) + the baseline cal artifacts:

  1. §13.9 verdict horizon: max measured acquisition onset + W_post + margin —
     CENSORING-AWARE (a censored cal seed makes the onset bound a >=, never a max).
  2. §13.4 W_post per arm + the precedence ladder: own collapse period (3x the max
     measured in-regime period for the arm) -> fixed calibrated absolute-wave window for
     no-cycle regimes, subject to the SIZING PIN (fallback >= the max measured in-regime
     period anywhere, so no-cycle / present-unmeasured arms are never under-covered).
  3. §13.5 survival threshold for category-partition asg_dist over matched W_post:
     derived from the cal runs' OWN spans — the DEAD-state asg_cat distribution
     (windows carrying the collapse signature argmax_k==1 AND den < floor-tripwire) vs
     the post-onset healthy distribution; proposed theta = the dead-state 99th
     percentile (survival = staying above what the dead dictionary produces), with the
     healthy-vs-dead separation surfaced so the margin is visible.
  4. §13.10 probe-dwell rate (proposed constant; fabric-thinning guard shown).
  5. §13.6 B1/B2 constants from the baseline's own cal runs: B1 floor = the
     pre-differentiation (early-window) between/within ratio band; B2 floor = 0
     (registered category-prior floor) + its conversion form.
  6. The exam-CONVERSION form (sensitivity-without-conversion observable): PROPOSED
     exam_acc >= 0.6 in 2 consecutive eval windows.

Margin = 12000 (EXP11 §2 form, carried).
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

import exp09_arms as X9                                       # noqa: E402  (FLOOR tripwire)
import exp12_arms as X12                                      # noqa: E402

OUTDIR = X12.OUTDIR
MARGIN = 12000
PROBE_RATE_PROPOSED = 0.02


def _load(arm, seed):
    return json.loads((OUTDIR / f"{arm}_s{seed}.json").read_text())


def propose():
    reads = {a: [X12.stage_one_read(_load(a, s)) for s in X12.CAL_SEEDS]
             for a in X12.ARMS12}
    out = dict(status="PROPOSED — not in force until ratified in chat",
               cal_seeds=X12.CAL_SEEDS, cal_horizon=X12.CAL_HORIZON, margin=MARGIN)

    # --- onset bound (censoring-aware) ---
    onsets, censored = [], 0
    for rs in reads.values():
        for r in rs:
            if r["onset"] is None:
                censored += 1
            else:
                onsets.append(r["onset"])
    onset_bound = max(onsets) if onsets else None
    out["onset_bound"] = dict(
        value=onset_bound, censored_cal_seeds=censored,
        form=(f">= {X12.CAL_HORIZON} (censored seed present — bound is a >=, never a max)"
              if censored else f"max measured onset = {onset_bound}"))

    # --- periods + W_post per arm (precedence ladder + sizing pin) ---
    all_measured = []
    per_arm = {}
    for a, rs in reads.items():
        ms = [r["den_dominant_period"] for r in rs
              if r.get("collapse_cycle_present") and r.get("den_dominant_period")]
        per_arm[a] = ms
        all_measured += ms
    global_max_period = max(all_measured) if all_measured else None
    wpost = {}
    for a, ms in per_arm.items():
        if ms:
            wpost[a] = dict(rung="own collapse period", periods_measured=ms,
                            w_post=3 * max(ms))
        else:
            wpost[a] = dict(rung="fixed calibrated window (no cycle measured)",
                            w_post=3 * global_max_period if global_max_period else None)
        # SIZING PIN: never under-cover vs anything measured in-regime anywhere
        if global_max_period and wpost[a]["w_post"] < global_max_period:
            wpost[a]["w_post"] = global_max_period
            wpost[a]["sizing_pin_applied"] = True
    out["w_post"] = wpost

    # --- verdict horizon ---
    wmax = max(v["w_post"] for v in wpost.values() if v["w_post"])
    base = (X12.CAL_HORIZON if censored else onset_bound)
    out["verdict_horizon"] = dict(
        value=base + wmax + MARGIN,
        form=f"onset_bound({'>=' + str(X12.CAL_HORIZON) if censored else onset_bound}) "
             f"+ max W_post({wmax}) + margin({MARGIN})")

    # --- survival threshold theta (dead-state vs healthy separation) ---
    dead, healthy = [], []
    for a in X12.ARMS12:
        for s in X12.CAL_SEEDS:
            rec = _load(a, s)
            onset = rec["acquisition_onset"]
            if onset is None:
                continue
            for c in rec["columns"]:
                if c["t"] < onset:
                    continue
                if c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR:
                    dead.append(c["asg_cat"])
                else:
                    healthy.append(c["asg_cat"])
    dead_s, healthy_s = sorted(dead), sorted(healthy)
    q = lambda xs, f: xs[int(f * len(xs))] if xs else None
    theta_p99, theta_p95 = q(dead_s, 0.99), q(dead_s, 0.95)
    span_means = {a: [round(statistics.mean(
        c["asg_cat"] for c in _load(a, s)["columns"]
        if _load(a, s)["acquisition_onset"] is not None
        and c["t"] >= _load(a, s)["acquisition_onset"]), 4)
        for s in X12.CAL_SEEDS if _load(a, s)["acquisition_onset"] is not None]
        for a in X12.ARMS12}
    out["survival_threshold"] = dict(
        theta_recommended=theta_p95,
        theta_recommendation_grounds="dead-p95; the dead p95->p99 tail (0.006->0.027) is "
                                     "boundary-TRANSITION windows (argmax_k momentarily 1 "
                                     "while asg_cat still relaxing), and the criterion is a "
                                     "W_post MEAN — a dead arm's window mean sits near "
                                     "dead-p50 ~4e-5, far below either candidate",
        theta_alternates=dict(dead_p90=q(dead_s, 0.90), dead_p95=theta_p95,
                              dead_p99=theta_p99),
        n_dead_windows=len(dead), n_healthy_windows=len(healthy),
        dead=dict(p50=q(dead_s, 0.50), p90=q(dead_s, 0.90), p95=theta_p95,
                  p99=theta_p99, max=dead_s[-1] if dead_s else None),
        healthy=dict(p10=q(healthy_s, 0.10), p50=q(healthy_s, 0.50),
                     p90=q(healthy_s, 0.90)),
        cal_span_means_per_acquired_seed=span_means,
        decisiveness_note="against dead-p99 the cal span means read dwell 1/3, shuffle "
                          "2/5 above; against dead-p95 all 3/3 and 5/5 above — the theta "
                          "choice is DECISIVE, which is why it is ratified, never read off",
        criterion_form="window MEAN of asg_cat over matched W_post >= theta "
                       "(windowed estimator, pinned form; frac-alive companion logged)")

    # --- probe-dwell rate ---
    out["probe_rate"] = dict(
        proposed=PROBE_RATE_PROPOSED,
        fabric_thinning=f"{PROBE_RATE_PROPOSED:.0%} of scheduled exams suppressed; at "
                        f"E[k]=11, ~{PROBE_RATE_PROPOSED / 11:.2%} of waves affected")

    # --- baseline B1/B2 ---
    bl = {}
    for a in X12.ARMS12:
        short = a.replace("exp12_", "")
        rows = []
        for s in X12.CAL_SEEDS:
            p = OUTDIR / f"exp12_baseline_{short}_s{s}.json"
            if p.exists():
                rows.append(json.loads(p.read_text()))
        if not rows:
            continue
        def _m(xs):
            xs = [x for x in xs if x is not None]
            return round(statistics.mean(xs), 5) if xs else None
        early = [c["b1_ratio"] for r in rows for c in r["columns"][:20]
                 if c["b1_ratio"] is not None]
        es = sorted(early)
        # NOTE: b1_ratio is None when b1_within -> 0 with b1_between > 0 = DEGENERATE
        # (maximal category clustering), not missing data — counted, never averaged in
        bl[a] = dict(
            b1_floor_proposed=round(es[int(0.99 * len(es))], 4) if es else None,
            b1_floor_derivation="99th pct of the first-20-window (pre-differentiation) "
                                "between/within ratios pooled over cal seeds",
            b1_early=dict(p50=round(es[len(es) // 2], 4) if es else None,
                          p99=round(es[int(0.99 * len(es))], 4) if es else None),
            b1_late_per_seed=[dict(
                ratio=_m([c["b1_ratio"] for c in r["columns"][-20:]]),
                between=_m([c["b1_between"] for c in r["columns"][-20:]]),
                within=_m([c["b1_within"] for c in r["columns"][-20:]]),
                degenerate_windows=sum(1 for c in r["columns"][-20:]
                                       if c["b1_ratio"] is None)) for r in rows],
            b2_floor=0.0,
            b2_acc_end_per_seed=[_m([c["b2_exam_acc"] for c in r["columns"][-20:]])
                                 for r in rows],
            b2_lift_end_per_seed=[_m([c["b2_exam_lift"] for c in r["columns"][-20:]])
                                  for r in rows])
    out["baseline"] = bl

    # --- exam-CONVERSION form: calibrate against the measured CHANCE BAND ---
    # (the naive acc>=0.6 x2 form FALSE-FIRES on censored cal runs — measured, below;
    # so the form is set from the pooled pre-onset/censored per-window acc distribution)
    chance_accs, chance_runs = [], []
    for a in X12.ARMS12:
        for s in X12.CAL_SEEDS:
            rec = _load(a, s)
            onset = rec["acquisition_onset"]
            seg = [c["exam_acc"] for c in rec["columns"]
                   if c.get("exam_acc") is not None and (onset is None or c["t"] < onset)]
            if seg:
                chance_accs += seg
                chance_runs.append(seg)

    def fires(seg, thr, consec):
        run = 0
        for x in seg:
            run = run + 1 if x >= thr else 0
            if run >= consec:
                return True
        return False

    ca = sorted(chance_accs)
    p99 = ca[int(0.99 * len(ca))]
    naive_rate = sum(fires(s_, 0.6, 2) for s_ in chance_runs) / len(chance_runs)
    cand = dict(thr=round(p99, 4), consec=3)
    cand_rate = sum(fires(s_, cand["thr"], cand["consec"]) for s_ in chance_runs) / len(chance_runs)
    out["exam_conversion_form"] = dict(
        chance_band=dict(n_windows=len(ca), p50=ca[len(ca) // 2], p99=round(p99, 4),
                         max=ca[-1]),
        naive_form_rejected=dict(form="acc >= 0.6 x2 consecutive",
                                 false_fire_rate_per_chance_segment=round(naive_rate, 3),
                                 note="fires on censored runs — too weak; REJECTED"),
        proposed=dict(form=f"exam_acc >= {cand['thr']} in {cand['consec']} consecutive "
                           "eval windows (thr = chance-band p99)",
                      false_fire_rate_per_chance_segment=round(cand_rate, 3)),
        note="the sensitivity-without-conversion dissociation observable; the companion "
             "aligns to this onset if one appears (§10)")

    (OUTDIR / "exp12_stage2_constants.PROPOSED.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
    propose()
