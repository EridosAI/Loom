"""exp_scatter_preflight.py — SCATTER deployed-horizon pre-check (G1a / G1b / G2).

Runs BEFORE the pre-flight commit (CORRIDOR_PROTOCOL touch 2). OUTCOME-BLIND: fabric construction +
independence asserts + F5-floor re-verification at the DEPLOYED 1M horizon (AMD-1: the k-independence /
cap-hit asserts are T-dependent, so the pre-check must run at 1M, never 15k). Reuses the committed
executors exp14_arms._assert_one (G1) and exp17_score.measure_kinematics + cell_feasible_scatter (G2).
Writes exp08/scatter_preflight_gates.json. Zero-box-exit is asserted inside build_fabric, so a clean
build IS the box check over the full 1M.
"""
import statistics
from pathlib import Path

import torch
torch.set_num_threads(1)

import exp14_arms as XA
import exp12_arms as X12
import exp17_score as S17
import exp_scatter_score as SS

OUT = XA.OUTDIR
DEPLOY, WIN = 1_000_000, S17.X17_PRIMARY_AT          # build @1M, read window [0,500k)


def _g1(arm, seeds):
    rows = []
    for s in seeds:
        r = XA._assert_one(arm, s, DEPLOY)           # builds @1M (zero-box-exit implicit); asserts
        rows.append(dict(seed=s, ok=bool(r["ok"]),
                         perlag=bool(r["perlag_nuis"]["ok"]), k=bool(r["k_indep"]["ok"]),
                         sched=bool(r["schedule_indep"]["ok"]), bg=bool(r["bg_indep"]["ok"]),
                         cap=bool(r["cap_hit"]["ok"])))
        print(f"  G1 {arm} s{s}: ok={rows[-1]['ok']} perlag={rows[-1]['perlag']} "
              f"k={rows[-1]['k']} sched={rows[-1]['sched']} bg={rows[-1]['bg']} cap={rows[-1]['cap']}")
    return rows


def _g2():
    """R-verify at deployed 1M: re-measure tremble + scatter kinematics (window [0,500k)) and assert
    the F5 floors hold; R must equal the frozen 0.50."""
    tb = [S17.measure_kinematics(SS.TREMBLE_ARM, s, DEPLOY, WIN) for s in SS.VERDICT_SEEDS]
    base = dict(perstep=statistics.mean(m["perstep_med"] for m in tb),
                tr11=statistics.mean(m["tr11"] for m in tb),
                confusion=statistics.mean(m["cross_med"] for m in tb))
    sc = [S17.measure_kinematics(SS.ARM, s, DEPLOY, WIN) for s in SS.VERDICT_SEEDS]
    cell = SS.cell_feasible_scatter(sc, base, 0.50)
    return dict(deployed_window=WIN, baselines=base, cell=cell,
                r_frozen=X12.X_SCATTER_R, r_matches=bool(X12.X_SCATTER_R == 0.50),
                floors_hold=bool(cell["feasible"]))


def main():
    print("G1b — FRESH scatter cal/verdict/EXT @1M")
    g1b = _g1(SS.ARM, SS.CAL_SEEDS + SS.VERDICT_SEEDS + SS.EXT_POOL)
    print("G1a — REUSED A_dwell {0-7} @1M (replay divergence class)")
    g1a = _g1(SS.TREMBLE_ARM, SS.VERDICT_SEEDS)
    print("G2 — R-verify + F5 floors at deployed 1M")
    g2 = _g2()
    g1_ok = all(r["ok"] and r["perlag"] and r["k"] and r["sched"] and r["bg"] and r["cap"]
                for r in g1b + g1a)
    out = dict(gate="scatter pre-flight (G1a/G1b/G2)", deploy=DEPLOY, window=WIN,
               g1b_scatter=g1b, g1a_reused_A=g1a, g2=g2, spec_hash=XA.C.spec_hash(),
               all_pass=bool(g1_ok and g2["floors_hold"] and g2["r_matches"]))
    S17._dump(OUT / "scatter_preflight_gates.json", out)
    print(f"G2: floors_hold={g2['floors_hold']} r_matches={g2['r_matches']} "
          f"(perstep {g2['cell']['perstep_pool']} >= {SS.CONTRAST_MULT}x{round(g2['baselines']['perstep'],4)}; "
          f"cov {g2['cell']['coverage_pool']} >= {SS.COVERAGE_MULT}x{round(g2['baselines']['tr11'],4)})")
    print("SCATTER PRE-FLIGHT GATES all_pass:", out["all_pass"])


if __name__ == "__main__":
    main()
