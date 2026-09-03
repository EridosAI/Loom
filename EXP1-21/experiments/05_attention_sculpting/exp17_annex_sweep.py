"""EXP17 touch-2 ADVISORY kinematics annex sweep (Jason-requested, 2026-07-12; scope-fenced).

FENCE: fabric kinematics + onset marginals ONLY. No learner, no loss, no outcome statistic;
the corridor stays shut; NO new constant is pinned. Committed-measurer recipes verbatim:
  - np11/tr11  -> exp17_score.measure_kinematics (called unchanged)
  - W1         -> exp17_score.onset_marginal_delta's per-axis quantile-coupled estimator,
                  REPLICATED here (byte-faithful) only because the committed fn hard-codes
                  X17_VERDICT_SEEDS and Jason pinned seeds {0,1,2,3} for this sweep.
Deployed bars = 4x / 2.5x baselines_1M from exp17_orbit_freeze.json (method-named).
Off-grid probe arms (odd omega; r=0.80) are fabric-only PROBE arms (X12.orbit_arm) — never
experiment arms; they read the slope, they are not candidates. Results are an advisory ANNEX.
"""
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import torch

torch.set_num_threads(1)                       # determinism contract (inherited)

import exp17_score as S
import exp12_arms as X12

SEEDS = [0, 1, 2, 3]
DEPLOY_WINDOW = 500_000
TREMBLE = S.X17_TREMBLE_ARM                     # "exp12_dwell"
OUT = Path(__file__).parent / "exp08" / "exp17_preflight_annex.json"

_frz = json.loads((Path(__file__).parent / "exp08" / "exp17_orbit_freeze.json").read_text())
BASE_NP = _frz["baselines_1M"]["np11"]
BASE_TR = _frz["baselines_1M"]["tr11"]
NP_BAR = S.X17_NP_MULT * BASE_NP                # 4 x 0.14489
TR_BAR = S.X17_TR_MULT * BASE_TR               # 2.5 x 0.09019
FREEZE_W1_0_7 = _frz["onset_marginal"]["mean_w1"]


def _sd(xs):
    return statistics.stdev(xs) if len(xs) >= 2 else 0.0


# ---- committed-recipe np11/tr11 (measure_kinematics unchanged), pooled over SEEDS ---------- #
def kin(arm, steps, window):
    per = [S.measure_kinematics(arm, sd, steps, window) for sd in SEEDS]
    np_ = [m["np11"] for m in per]
    tr_ = [m["tr11"] for m in per]
    return dict(
        np11=statistics.mean(np_), np11_sd=_sd(np_),
        tr11=statistics.mean(tr_), tr11_sd=_sd(tr_),
        per_seed={str(sd): dict(np11=m["np11"], tr11=m["tr11"]) for sd, m in zip(SEEDS, per)},
        n11_per_seed={str(sd): m["n11"] for sd, m in zip(SEEDS, per)})


# ---- onset_marginal_delta's W1 estimator, replicated byte-faithful ------------------------- #
def _pool(arm, seeds, steps, window, onsets_only=True):
    pools = []
    for sd in seeds:
        fab = S._fabric(arm, sd, steps)
        m = min(window, fab.nuis.shape[0])
        if onsets_only:
            pools.append(fab.nuis[:m][fab.pos[:m] == 1])
        else:
            pools.append(fab.nuis[:m])
    return torch.cat(pools).double()


def _w1(pool_a, pool_b):
    w = []
    for ax in range(pool_a.shape[1]):
        a_s, o_s = pool_a[:, ax].sort().values, pool_b[:, ax].sort().values
        m = min(len(a_s), len(o_s))
        qa = a_s[torch.linspace(0, len(a_s) - 1, m).long()]
        qo = o_s[torch.linspace(0, len(o_s) - 1, m).long()]
        w.append(float((qa - qo).abs().mean()))
    return statistics.mean(w), w


def w1_arm_vs_tremble(arm, steps, window):
    """Pooled W1 (committed pooling: cat over seeds then couple) + per-seed W1 for the sd bar."""
    pooled, per_axis = _w1(_pool(TREMBLE, SEEDS, steps, window),
                           _pool(arm, SEEDS, steps, window))
    per_seed = [_w1(_pool(TREMBLE, [sd], steps, window),
                    _pool(arm, [sd], steps, window))[0] for sd in SEEDS]
    return dict(w1_pooled=pooled, per_axis=per_axis,
                w1_per_seed_mean=statistics.mean(per_seed), w1_per_seed_sd=_sd(per_seed),
                per_seed={str(sd): v for sd, v in zip(SEEDS, per_seed)})


def _interp_cross(xs, ys, bar):
    """Linear omega/r at which y crosses `bar`, using the bracket that spans it; extrapolate
    from the nearest segment (flagged) if unbracketed. Returns (x_at_bar, extrapolated?)."""
    pts = sorted(zip(xs, ys))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if (y0 - bar) * (y1 - bar) <= 0 and y1 != y0:
            return x0 + (bar - y0) * (x1 - x0) / (y1 - y0), False
    (x0, y0), (x1, y1) = pts[0], pts[-1]        # extrapolate on the full-range slope
    if y1 == y0:
        return None, True
    return x0 + (bar - y0) * (x1 - x0) / (y1 - y0), True


def main():
    result = dict(fence="fabric kinematics + onset marginals ONLY; corridor shut; no constant "
                        "pinned; committed recipes verbatim",
                  seeds=SEEDS, deploy_window=DEPLOY_WINDOW,
                  bars=dict(np_bar=NP_BAR, tr_bar=TR_BAR, base_np=BASE_NP, base_tr=BASE_TR,
                            recipe="4x / 2.5x baselines_1M (exp17_orbit_freeze.json)"),
                  freeze_w1_0_7_1M=FREEZE_W1_0_7)

    # ---- STEP 0: prefix-identity lever (orbit canonical arm, seed 0) ---------------------- #
    f500 = S._fabric("exp12_dwell_orbit", 0, 500_000)
    f1m = S._fabric("exp12_dwell_orbit", 0, 1_000_000)
    nuis_eq = torch.equal(f500.nuis[:DEPLOY_WINDOW], f1m.nuis[:DEPLOY_WINDOW])
    pos_eq = torch.equal(f500.pos[:DEPLOY_WINDOW], f1m.pos[:DEPLOY_WINDOW])
    # orbit_planes/centers for dwells fully inside [0,500k)
    starts = [i for i in range(DEPLOY_WINDOW) if int(f1m.pos[i]) == 1]
    ndw = max(0, len(starts) - 1)               # exclude the straddler at the window edge
    planes_eq = torch.equal(f500.orbit_planes[:ndw], f1m.orbit_planes[:ndw])
    centers_eq = torch.equal(f500.orbit_centers[:ndw], f1m.orbit_centers[:ndw])
    prefix_identical = bool(nuis_eq and pos_eq and planes_eq and centers_eq)
    STEPS = 500_000 if prefix_identical else 1_000_000
    result["step0"] = dict(prefix_identical=prefix_identical, nuis_eq=bool(nuis_eq),
                           pos_eq=bool(pos_eq), planes_eq=bool(planes_eq),
                           centers_eq=bool(centers_eq), dwells_compared=ndw, steps_used=STEPS,
                           seed_class_note="kinematics measures are fabric-only, X-blind; the "
                           "pre-registered seed roles (cal/verdict/EXT/subst) bind LEARNER runs "
                           "and scoring, not fabric kinematics — select_orbit itself measured "
                           "kinematics over verdict seeds with no seed-class restriction; "
                           "{0,1,2,3} (subset of verdict) is admissible for a kinematics-only "
                           "measure")
    print(f"STEP0: prefix_identical={prefix_identical} (nuis={bool(nuis_eq)} pos={bool(pos_eq)} "
          f"planes={bool(planes_eq)} centers={bool(centers_eq)}; {ndw} dwells) -> STEPS={STEPS}",
          flush=True)

    # ---- SWEEP A: deployed omega-slope, r=0.85, omega in {17,18,19} ----------------------- #
    A = {}
    for w in (17, 18, 19):
        arm = X12.orbit_arm(0.85, w)
        A[w] = kin(arm, STEPS, DEPLOY_WINDOW)
        print(f"SWEEP-A r=0.85 w={w}: np11={A[w]['np11']:.4f}+/-{A[w]['np11_sd']:.4f} "
              f"tr11={A[w]['tr11']:.4f}+/-{A[w]['tr11_sd']:.4f}", flush=True)
    ws = [17, 18, 19]
    np_slope = (A[19]["np11"] - A[17]["np11"]) / 2.0
    tr_slope = (A[19]["tr11"] - A[17]["tr11"]) / 2.0
    np_wall, np_ex = _interp_cross(ws, [A[w]["np11"] for w in ws], NP_BAR)
    tr_wall, tr_ex = _interp_cross(ws, [A[w]["tr11"] for w in ws], TR_BAR)
    # 100k grid comparison (r=0.85, from the committed select artifact; seeds {0-7} @100k)
    sel = json.loads((Path(__file__).parent / "exp08" / "exp17_orbit_select.json").read_text())
    g = {c["w_deg"]: c for c in sel["cells"] if c["r"] == 0.85}
    np_slope_100k = (g[20]["np_pool"] - g[16]["np_pool"]) / 4.0
    tr_slope_100k = (g[20]["tr_pool"] - g[16]["tr_pool"]) / 4.0
    result["sweepA"] = dict(
        arm_r=0.85, omega=A,
        np11_slope_per_deg=np_slope, tr11_slope_per_deg=tr_slope,
        np11_wall_omega=np_wall, np11_wall_extrapolated=np_ex,
        tr11_wall_omega=tr_wall, tr11_wall_extrapolated=tr_ex,
        grid_100k=dict(seeds="0-7", window=100_000,
                       cells={str(k): dict(np_pool=g[k]["np_pool"], tr_pool=g[k]["tr_pool"],
                                           floor1=g[k]["floor1"], floor2=g[k]["floor2"])
                              for k in (16, 18, 20)},
                       np11_slope_per_deg=np_slope_100k, tr11_slope_per_deg=tr_slope_100k))

    # ---- SWEEP B: r-trajectory at omega=18, r in {0.80, 0.85, 0.90} (W1 + np11/tr11) ------ #
    B = {}
    for r in (0.80, 0.85, 0.90):
        arm = X12.orbit_arm(r, 18)
        k = kin(arm, STEPS, DEPLOY_WINDOW)
        w1 = w1_arm_vs_tremble(arm, STEPS, DEPLOY_WINDOW)
        clip = round(S.X17_BOUND - r - 3 * S.X17_STAT_SD, 4)
        B[r] = dict(clip=clip, kin=k, w1=w1)
        print(f"SWEEP-B r={r} w=18: np11={k['np11']:.4f} tr11={k['tr11']:.4f} "
              f"W1={w1['w1_pooled']:.4f} (per-seed {w1['w1_per_seed_mean']:.4f}"
              f"+/-{w1['w1_per_seed_sd']:.4f})", flush=True)
    result["sweepB"] = dict(arm_w=18, r={str(r): B[r] for r in (0.80, 0.85, 0.90)})
    W1P = {r: B[r]["w1"]["w1_pooled"] for r in (0.80, 0.85, 0.90)}

    # ---- REFERENCE C: W1 contrast baseline — tremble onsets vs tremble RAW (full) marginal - #
    base_pooled, base_axes = _w1(_pool(TREMBLE, SEEDS, STEPS, DEPLOY_WINDOW, onsets_only=True),
                                 _pool(TREMBLE, SEEDS, STEPS, DEPLOY_WINDOW, onsets_only=False))
    base_per_seed = [_w1(_pool(TREMBLE, [sd], STEPS, DEPLOY_WINDOW, True),
                         _pool(TREMBLE, [sd], STEPS, DEPLOY_WINDOW, False))[0] for sd in SEEDS]
    pin_w1 = W1P[0.85]
    result["referenceC"] = dict(
        definition="W1(tremble onset marginal [pos==1] vs tremble RAW full-frame delivered "
                   "marginal), same per-axis quantile-coupled estimator, seeds {0,1,2,3}, "
                   "[0,500k) — the within-tremble scale that turns the orbit W1 into a ratio",
        w1_pooled=base_pooled, per_axis=base_axes,
        w1_per_seed_mean=statistics.mean(base_per_seed), w1_per_seed_sd=_sd(base_per_seed),
        ratio_pin_over_baseline=(pin_w1 / base_pooled if base_pooled else None),
        ratio_freeze0_7_over_baseline=(FREEZE_W1_0_7 / base_pooled if base_pooled else None),
        pin_w1_0_3=pin_w1)

    # ---- halt-class assessment (qualitative; JASON RULES) --------------------------------- #
    np_margin = A[19]["np11"] - NP_BAR          # high-omega wall probe (np falls with omega)
    tr_margin = A[17]["tr11"] - TR_BAR          # low-omega wall probe (tr falls with omega)
    w1_step_lo = W1P[0.85] - W1P[0.80]
    w1_step_hi = W1P[0.90] - W1P[0.85]
    result["halt_class"] = dict(
        criterion_1_walls=dict(
            np11_at_w19=A[19]["np11"], np_bar=NP_BAR, np_clears_at_w19=bool(A[19]["np11"] >= NP_BAR),
            tr11_at_w17=A[17]["tr11"], tr_bar=TR_BAR, tr_clears_at_w17=bool(A[17]["tr11"] >= TR_BAR),
            note="100k feasible window at r=0.85 is the single cell w=18; {17,19} sit 1 deg "
                 "inside each 100k wall. Deployed walls TIGHTER than 100k iff either probe fails."),
        criterion_2_w1_knee=dict(
            w1_r080=W1P[0.80], w1_r085=W1P[0.85], w1_r090=W1P[0.90],
            step_080_to_085=w1_step_lo, step_085_to_090=w1_step_hi,
            note="a knee = the 0.85->0.90 step markedly steeper than 0.80->0.85 (W1 rising sharply "
                 "into the pin); monotone-smooth => no knee"),
        both_probes_clear=bool(A[19]["np11"] >= NP_BAR and A[17]["tr11"] >= TR_BAR))
    print(f"HALT-CLASS: np11(w19)={A[19]['np11']:.4f} vs {NP_BAR:.4f} "
          f"(margin {np_margin:+.4f}); tr11(w17)={A[17]['tr11']:.4f} vs {TR_BAR:.4f} "
          f"(margin {tr_margin:+.4f}); W1 steps {w1_step_lo:+.4f}/{w1_step_hi:+.4f}", flush=True)

    OUT.write_text(json.dumps(result, indent=1))
    print(f"ANNEX JSON -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
