"""exp06 RE-CONFIRM of the deciding cell [1,0,0] (post-gate; pre-registered). The joint-lever vs
irreducible-conjunction fork hangs entirely on [1,0,0], which was still climbing at the 4000-step
budget (Q1 trajectory) — under the standing plateau-before-read rule (the same one that certified the
dead cells) an unconverged cell is not ready to read. This finishes it.

PRE-REGISTERED (pinned BEFORE running; no new criterion):
  * Train [1,0,0] (deciding) + [0,0,0] (bar guard) to 12000 steps, checkpoints
    [4000,6000,8000,10000,12000], SEEDS_HI=16 (up from 5) to tighten the estimate.
  * PLATEAU = mean d_diff flat (|Δ|<=0.05 between consecutive checkpoints) AND mean proto_spread
    stable (<=5% rel change), sustained to the end. B* = earliest such checkpoint with a flat tail.
    Never flat by 12000 -> NON-CONVERGENT (honest outcome: fork undecidable at this operating point).
  * BAR: live_bar = 0.867 (committed gate value). Recompute at B* ONLY if clean [0,0,0] drifts >0.05
    from its 4000 value (the "clean also still climbing" trigger). Report clean(B*) regardless
    (equal-training comparison).
  * DECISION (unchanged §4 on the converged mean): manyOnly(B*) mean >= live_bar + 0.10 (=0.967)
    -> JOINT {cue-diffuseness, pam-pool-penalty} locked, member-count tolerated-deployed.
    Below -> 3-way IRREDUCIBLE CONJUNCTION, member-count load-bearing. Both pre-registered.
  * ROUTING WATCH: [1,1,0],[1,0,1] (deciding-pair constituents) + [0,1,0] (soft cell) to 12000
    (SEEDS_LO=5) must STAY collapsed (<= collapse_ceiling 0.05). If [1,1,0] lifts off zero, re-check
    the soft diffOnly cell still isn't in the deciding arithmetic.
  * NEUTRALITY: texture asymmetry stays out; symmetric over the two lever factors.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

from dgate import Factors                                   # noqa: E402
from exp06_gate_validation import train_with_trajectory     # noqa: E402
from exp06_factorial import (M_MANY, DEPLOYED_PAM_LAM, DIFFUSE_SHARED, DIFFUSE_CUE)  # noqa: E402

# --- pre-registered pins ---
SEEDS_HI = list(range(16))
SEEDS_LO = list(range(5))
CHECKPOINTS = [4000, 6000, 8000, 10000, 12000]
LIVE_BAR = 0.8672                  # committed gate value
DECISION_MARGIN = 0.10
COLLAPSE_CEILING = 0.05
PLATEAU_D_EPS = 0.05               # |Δ mean d_diff| between consecutive checkpoints
PLATEAU_PROTO_REL = 0.05          # rel change in mean proto_spread
CLEAN_DRIFT_EPS = 0.05            # recompute bar if clean drifts more than this from its 4000 value

CFG = dict(diffuse_shared_mag=DIFFUSE_SHARED, diffuse_cue_mag=DIFFUSE_CUE)


def _factors(member_count, diffuse, pam_lam):
    return Factors(member_count=member_count, diffuse=diffuse, pam_lam=pam_lam,
                   train_steps=max(CHECKPOINTS), **CFG)


def _agg_traj(cell_factors, seeds):
    """Train `seeds` trajectories to max(CHECKPOINTS); return per-checkpoint mean/std of d_diff+proto."""
    per_seed = [train_with_trajectory(cell_factors, s, CHECKPOINTS) for s in seeds]
    out = {}
    for ci, step in enumerate(CHECKPOINTS):
        dvals = [ps[ci]["d_diff"] for ps in per_seed]
        pvals = [ps[ci]["proto_spread"] for ps in per_seed]
        out[step] = dict(
            d_mean=statistics.mean(dvals), d_std=(statistics.stdev(dvals) if len(dvals) > 1 else 0.0),
            d_min=min(dvals), d_max=max(dvals), d_per_seed=[round(x, 4) for x in dvals],
            proto_mean=statistics.mean(pvals), n=len(dvals),
            d_sem=((statistics.stdev(dvals) / len(dvals) ** 0.5) if len(dvals) > 1 else 0.0))
    return out


def _plateau_budget(traj):
    """Earliest checkpoint B where d-mean and proto-mean are flat from B onward (pre-registered)."""
    steps = CHECKPOINTS
    for i in range(1, len(steps)):
        ok = True
        for j in range(i, len(steps)):
            dprev, dcur = traj[steps[j - 1]]["d_mean"], traj[steps[j]]["d_mean"]
            pprev, pcur = traj[steps[j - 1]]["proto_mean"], traj[steps[j]]["proto_mean"]
            if abs(dcur - dprev) > PLATEAU_D_EPS:
                ok = False; break
            if pprev > 1e-6 and abs(pcur - pprev) / pprev > PLATEAU_PROTO_REL:
                ok = False; break
        if ok:
            return steps[i - 1]
    return None


def main():
    print("=== exp06 RE-CONFIRM of deciding cell [1,0,0] (pre-registered) ===")
    print(f"seeds_hi={len(SEEDS_HI)} checkpoints={CHECKPOINTS} live_bar={LIVE_BAR} "
          f"decision_threshold={LIVE_BAR + DECISION_MARGIN:.4f}\n")

    deciding = _factors(M_MANY, False, 0.0)       # [1,0,0] manyOnly
    clean = _factors(2, False, 0.0)               # [0,0,0]
    traj_dec = _agg_traj(deciding, SEEDS_HI)
    traj_cln = _agg_traj(clean, SEEDS_HI)

    print("trajectory (mean d_diff ± std [min,max], proto_mean) over checkpoints:")
    for step in CHECKPOINTS:
        td, tc = traj_dec[step], traj_cln[step]
        print(f"  step {step:6d}: [1,0,0] d={td['d_mean']:.3f}±{td['d_std']:.3f} "
              f"[{td['d_min']:.2f},{td['d_max']:.2f}] sem={td['d_sem']:.3f} proto={td['proto_mean']:.3f}"
              f"  | [0,0,0] d={tc['d_mean']:.3f}±{tc['d_std']:.3f} proto={tc['proto_mean']:.3f}")

    bstar = _plateau_budget(traj_dec)
    converged = bstar is not None
    bstar_eff = bstar if converged else CHECKPOINTS[-1]

    # bar guard: did clean drift past 4000?
    clean_4000 = traj_cln[4000]["d_mean"]
    clean_bstar = traj_cln[bstar_eff]["d_mean"]
    clean_drift = abs(clean_bstar - clean_4000)
    if clean_drift > CLEAN_DRIFT_EPS:
        live_bar_eff = clean_bstar - 2.0 * traj_cln[bstar_eff]["d_std"]
        bar_note = f"clean drifted {clean_drift:.3f} -> recomputed live_bar at B*={live_bar_eff:.4f}"
    else:
        live_bar_eff = LIVE_BAR
        bar_note = f"clean flat (drift {clean_drift:.3f} <= {CLEAN_DRIFT_EPS}) -> live_bar held at {LIVE_BAR}"

    dec_mean = traj_dec[bstar_eff]["d_mean"]
    dec_sem = traj_dec[bstar_eff]["d_sem"]
    threshold = live_bar_eff + DECISION_MARGIN
    clears = dec_mean >= threshold
    verdict = ("JOINT LEVER {cue-diffuseness, pam-pool-penalty}; member-count tolerated-deployed"
               if clears else
               "3-way IRREDUCIBLE CONJUNCTION; member-count ALSO load-bearing")

    # routing watch
    routing = {}
    for name, fc in (("1,1,0", _factors(M_MANY, True, 0.0)),
                     ("1,0,1", _factors(M_MANY, False, DEPLOYED_PAM_LAM)),
                     ("0,1,0", _factors(2, True, 0.0))):
        t = _agg_traj(fc, SEEDS_LO)
        last = t[bstar_eff]
        routing[name] = dict(d_mean=last["d_mean"], d_max=last["d_max"], proto_mean=last["proto_mean"],
                             stays_collapsed=bool(last["d_max"] <= COLLAPSE_CEILING))
    soft_cell_d = routing["0,1,0"]["d_mean"]
    constituent_110_lifted = not routing["1,1,0"]["stays_collapsed"]

    out = dict(
        pre_registered=dict(seeds_hi=len(SEEDS_HI), seeds_lo=len(SEEDS_LO), checkpoints=CHECKPOINTS,
                            live_bar=LIVE_BAR, decision_margin=DECISION_MARGIN,
                            decision_threshold=threshold, plateau_d_eps=PLATEAU_D_EPS,
                            plateau_proto_rel=PLATEAU_PROTO_REL),
        deciding_trajectory=traj_dec, clean_trajectory=traj_cln,
        plateau_budget=bstar, converged=converged, bstar_effective=bstar_eff,
        bar_guard=dict(clean_4000=clean_4000, clean_bstar=clean_bstar, clean_drift=clean_drift,
                       live_bar_effective=live_bar_eff, note=bar_note),
        deciding_at_bstar=dict(mean=dec_mean, sem=dec_sem, mean_minus_2sem=dec_mean - 2 * dec_sem,
                               threshold=threshold, clears=clears),
        VERDICT=verdict, joint_locked=bool(clears),
        routing_watch=dict(cells=routing, soft_cell_0_1_0_d=soft_cell_d,
                           constituent_1_1_0_lifted=constituent_110_lifted,
                           soft_still_out_of_deciding=bool(soft_cell_d <= COLLAPSE_CEILING)),
    )
    Path(_HERE / "exp06_reconfirm.json").write_text(json.dumps(out, indent=2))

    print(f"\nplateau budget B* = {bstar}  (converged={converged}; effective {bstar_eff})")
    print(f"bar guard: {bar_note}")
    print(f"\ndeciding [1,0,0] @ B*={bstar_eff}: mean={dec_mean:.4f} (sem {dec_sem:.4f}, "
          f"mean-2sem {dec_mean - 2 * dec_sem:.4f})  vs threshold {threshold:.4f}  -> "
          f"{'CLEARS' if clears else 'BELOW'}")
    print(f"\nVERDICT: {verdict}")
    print("\nrouting watch @ B* (must stay <= collapse_ceiling 0.05):")
    for name, r in routing.items():
        print(f"  [{name}] d_mean={r['d_mean']:.4f} d_max={r['d_max']:.4f} proto={r['proto_mean']:.4f} "
              f"-> {'collapsed' if r['stays_collapsed'] else 'LIFTED'}")
    print(f"  soft diffOnly [0,1,0] d={soft_cell_d:.4f} -> "
          f"{'still out of deciding arithmetic' if soft_cell_d <= COLLAPSE_CEILING else 'ENTERS arithmetic — re-check routing'}")
    if constituent_110_lifted:
        print("  !! constituent [1,1,0] LIFTED off zero — re-check soft-cell routing per pre-registration")
    print("\n(record -> exp06_reconfirm.json)")


if __name__ == "__main__":
    main()
