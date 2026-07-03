"""EXP10 scoring + screens (one-review prep; NO PASS-form verdicts on varied arms —
the stage-two calibration returned DEGENERATE constants because the varied no-detach
regime is EPISODIC (metastable collapse-regrow), so 'healthy spans' do not exist as a
clean band; the PASS-form question routes to the one review as a regime finding).

Reports, per the prereg readouts:
  - epoch structure (episodes / horizon epoch / PIN vs PIN-CENSORED) via the guarded
    v2 machinery at the pinned word period (substitution per guard (a));
  - the DIRECT TEST: nodetach_varied vs the static death clocks (75.3k pin onset /
    ~96k s0) — licensed inference: closure-necessary-too, pull-necessity stands;
  - the ANNEALING DISCRIMINATOR: nodetach_isotropic vs nodetach_varied;
  - the TEACHING-AXIS screen: slowref_varied vs detachnull_varied outcome divergence;
  - acquisition onsets + aligned reads (SS-L, logged); shuffle-screen quietness;
  - evocation-decomposition trajectory summaries vs the static baseline observation.
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
import exp10_arms as X10                                      # noqa: E402

OUTDIR = X10.OUTDIR
ARMS = ["nodetach_varied", "slowref_varied", "detachnull_varied", "nodetach_isotropic"]
SEEDS = [0, 1, 2]


def _phase_med(cols, key, lo, hi):
    vals = [c[key] for c in cols if lo <= c["t"] < hi and c.get(key) is not None]
    return round(statistics.median(vals), 6) if vals else None


def summarize(rec):
    cols = rec["columns"]
    horizon = cols[-1]["t"]
    read = X10.function_test_read_v2(cols, control=False)
    k1 = sum(1 for c in cols if c["asg_argmax_k"] == 1)
    # longest k=1 & den-subfloor run anywhere (the deep-episode footprint)
    run = best = 0
    for c in cols:
        run = run + 1 if (c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR) else 0
        best = max(best, run)
    krun = kbest = 0                                        # k1-ONLY (assignment-dead) runs
    for c in cols:
        krun = krun + 1 if c["asg_argmax_k"] == 1 else 0
        kbest = max(kbest, krun)
    thirds = [(0, horizon // 3), (horizon // 3, 2 * horizon // 3),
              (2 * horizon // 3, horizon + 1)]
    traj = {k: [_phase_med(cols, k, lo, hi) for lo, hi in thirds]
            for k in ("num", "den", "asg_dist", "evo_diff", "grad_diff", "pairwise_emit")}
    shuf = [c.get("shufscreen_delta") for c in cols if c.get("shufscreen_delta") is not None]
    # both-period disclosure (verification: cross-arm strings must not ride substitution)
    read_pinned = X10.function_test_read_v2(cols, control=False, force_period=X9.PERIOD_WORD)
    # honest regime label (verification: static-calibrated PASS-form is out-of-regime/vacuous)
    if best == 0 and k1 == 0:
        regime = f"ROUTING-OPEN (0 k=1 windows in {len(cols)}; den never sub-floor)"
    else:
        regime = (f"EPISODIC ({best*X10.EVAL}w deepest joint-dead run; {k1} k=1 windows; "
                  f"terminal-class @pinned={read_pinned['verdict']} @measured={read['verdict']})")
    return dict(
        seed=rec["seed"], horizon=horizon,
        regime_label=regime,
        epoch_read=dict(verdict_static_calibrated_OUT_OF_REGIME=read["verdict"],
                        verdict_at_pinned_period=read_pinned["verdict"],
                        episodes=len(read["metastable_episodes"]),
                        horizon_epoch=read["horizon_epoch"],
                        period_measured=read["period"],
                        period_note=read["period_resolution"].get("note", "")),
        k1_windows=k1, k1_frac=round(k1 / len(cols), 4),
        deepest_joint_dead_run_waves=best * X10.EVAL,       # k=1 AND den sub-floor
        deepest_asg_dead_run_waves=kbest * X10.EVAL,        # k=1 only (assignment-dead)
        onset=rec.get("acquisition_onset"), aligned=rec.get("acquisition_aligned"),
        final=dict(num=cols[-1]["num"], den=cols[-1]["den"],
                   asg_dist=cols[-1]["asg_dist"], asg_k=cols[-1]["asg_argmax_k"]),
        thirds_median=traj,
        shufscreen=dict(n=len(shuf),
                        max_abs_delta=(round(max(abs(x) for x in shuf), 4) if shuf else None)),
    )


def main():
    out = {}
    for arm in ARMS:
        out[arm] = []
        for s in SEEDS:
            rec = json.loads((OUTDIR / f"{arm}_s{s}.json").read_text())
            out[arm].append(summarize(rec))
            r = out[arm][-1]
            print(f"{arm} s{s}: {r['regime_label']} | onset {r['onset']} "
                  f"| asg-dead-run {r['deepest_asg_dead_run_waves']}w | shufmax "
                  f"{r['shufscreen']['max_abs_delta']}")

    def col(arm, f):
        return [f(r) for r in out[arm]]

    comparisons = dict(
        direct_test=dict(
            static_death_clocks=dict(word_s1_pin_onset=75300, word_s0_occ_chance=96000,
                                     n_static_clock=2),
            nodetach_varied_horizon=X10.HORIZON_NODETACH,
            regime=col("nodetach_varied", lambda r: r["regime_label"]),
            horizon_epochs=col("nodetach_varied", lambda r: r["epoch_read"]["horizon_epoch"]),
            deepest_asg_dead=col("nodetach_varied", lambda r: r["deepest_asg_dead_run_waves"]),
            onsets=col("nodetach_varied", lambda r: r["onset"]),
            note="DIRECT TEST NEGATIVE: variation does not hold the loop open; word-arm "
                 "routing dies (asg-dead tails), word-channel decoupled-alive; "
                 "closure-necessary-too does NOT fire; pull-necessity via either-way clause"),
        annealing_discriminator=dict(
            structured=dict(regime=col("nodetach_varied", lambda r: r["regime_label"]),
                            onsets=col("nodetach_varied", lambda r: r["onset"]),
                            k1_fracs=col("nodetach_varied", lambda r: r["k1_frac"]),
                            asg_dead=col("nodetach_varied", lambda r: r["deepest_asg_dead_run_waves"])),
            isotropic=dict(regime=col("nodetach_isotropic", lambda r: r["regime_label"]),
                           onsets=col("nodetach_isotropic", lambda r: r["onset"]),
                           k1_fracs=col("nodetach_isotropic", lambda r: r["k1_frac"]),
                           asg_dead=col("nodetach_isotropic", lambda r: r["deepest_asg_dead_run_waves"])),
            note="ROUTE FIRES A FORTIORI: isotropic >= structured on every honest routing "
                 "outcome (deeper joint-dead pockets + one horizon-terminal PIN@pinned) -> "
                 "routing-openness is NOT structure-specific; structured-family ROUTING "
                 "claim FALLS. Onset residue (structured earlier 3/3, 1.3-2.9x, n=3 ns) is "
                 "CONFOUNDED by cue-corruption (iso corrupts identity axes at matched power)"),
        teaching_axis=dict(
            slowref=dict(regime=col("slowref_varied", lambda r: r["regime_label"]),
                         onsets=col("slowref_varied", lambda r: r["onset"]),
                         thirds_num=col("slowref_varied", lambda r: r["thirds_median"]["num"]),
                         thirds_evo=col("slowref_varied", lambda r: r["thirds_median"]["evo_diff"]),
                         thirds_asg=col("slowref_varied", lambda r: r["thirds_median"]["asg_dist"])),
            detachnull=dict(regime=col("detachnull_varied", lambda r: r["regime_label"]),
                            onsets=col("detachnull_varied", lambda r: r["onset"]),
                            thirds_num=col("detachnull_varied", lambda r: r["thirds_median"]["num"]),
                            thirds_evo=col("detachnull_varied", lambda r: r["thirds_median"]["evo_diff"]),
                            thirds_asg=col("detachnull_varied", lambda r: r["thirds_median"]["asg_dist"])),
            note="STOP-GRAD-IN-COSTUME AGAIN under variation: no slowref-vs-null divergence "
                 "on any axis; all 3 leans (live-frac, onset, evo_diff) favor the NULL. "
                 "Churn screen does NOT fire (acquisition present in all 12). Change from "
                 "static: differentiation channel alive-at-horizon in 5/6 varied ref/null "
                 "seeds (vs static decay) BUT common-domination persists (evo_ratio>1 in "
                 ">=99.6% of windows; moved-off-common only 3/6 full-run)."),
    )
    result = dict(per_arm=out, comparisons=comparisons,
                  note="CORRECTED READING (adversarial verification, 36 findings): the "
                       "static-calibrated epoch verdict strings are OUT-OF-REGIME/vacuous "
                       "(kept only as the labeled artifact they are). Honest reads = "
                       "regime_label + both-period terminal-class + onsets + trajectories. "
                       "DIRECT TEST NEGATIVE (variation does not hold the no-detach loop "
                       "open); annealing route fires a fortiori (routing-openness not "
                       "structure-specific); teaching axis = stop-grad-in-costume AGAIN "
                       "(null equal-or-ahead). See FRONTIER 10.15.")
    (OUTDIR / "exp10_verdicts.json").write_text(json.dumps(result, indent=2))
    print("\n-> exp10_verdicts.json")


if __name__ == "__main__":
    main()
