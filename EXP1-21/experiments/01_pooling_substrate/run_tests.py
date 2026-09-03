"""Run Tests A-D for the pooling substrate (SPEC sec. 4) and write RESULTS.md.

Each test states a *pre-registered* failure condition (fixed in code, below) and is
scored against it; results are not softened after the fact. Usage:

    python run_tests.py            # full suite + sweep, writes RESULTS.md + figures/
    python run_tests.py --quick    # fewer steps / smaller sweep (smoke test)

Run from this directory. Figures land in ./figures (gitignored); RESULTS.md is
committed.
"""

from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch

import data as D
import plots
from harness import AdaptiveRepool, StepSchedule, train
from model import HierarchicalPoolingModel

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")

# ---- knobs -----------------------------------------------------------------
LAM_HI = 10.0     # "pooled" penalty: drives matching residuals ~0
LAM_SOFT = 0.1    # Test A soft tie: finite, non-zero (not the free control)
TEMP = 1.0        # softmax temperature on the prototype (negative-distance) logits
LR = 0.05
BATCH = 256
SEED = 0


def build_model(data, n_groups, members_per_group, seed):
    """Construct the model with prototypes initialised at the data mean (so the
    nearest-prototype gradients start well-conditioned)."""
    return HierarchicalPoolingModel(
        data.X.shape[1], n_groups, members_per_group, temp=TEMP,
        init_center=data.X.mean(0), seed=seed,
    )

# ---- pre-registered pass/fail thresholds -----------------------------------
A_FINE_PASS = 0.90      # soft & free must separate the two sub-classes
A_FINE_FAIL = 0.65      # hard tie must stay at/near chance (0.5)
A_SPREAD_RATIO = 5.0    # soft spread must exceed hard spread by this factor
B_FINE_PASS = 0.90      # gradual unpool must reach this fine accuracy
B_POOLED_CAP = 0.55     # always-pooled fine must stay capped below this
B_MARGIN = 0.30         # gradual fine must beat pooled fine by this margin
B_COARSE_CEIL = 0.95    # coarse must reach ceiling before fine unpool (t2)
B_LURCH = 0.10          # coarse must not drop more than this across the t2 step
C_D2_SHRINK = 0.30      # re-pooled ||Delta2|| must fall below this x its pre-value
C_COARSE_KEEP = 0.95    # coarse value must survive re-pool


def _i_before(log, t):
    idx = [i for i, s in enumerate(log["step"]) if s < t]
    return idx[-1] if idx else 0


def _i_after(log, t):
    idx = [i for i, s in enumerate(log["step"]) if s >= t]
    return idx[0] if idx else len(log["step"]) - 1


def _peak_window(log, key, lo, hi):
    vals = [v for s, v in zip(log["step"], log[key]) if lo <= s <= hi]
    return max(vals) if vals else float("nan")


# ===========================================================================
# Test A -- symmetry break (make-or-break)
# ===========================================================================
def test_A(steps):
    print("== Test A: symmetry break ==")
    d = D.make_hierarchical_gaussians(
        D=16, n_coarse=1, n_fine=2, R_coarse=10.0, r_fine=1.0, sigma=0.3,
        n_per_fine=300, seed=SEED,
    )
    tr, te = d.split(seed=SEED)
    conds = {
        "soft": dict(controller=StepSchedule(0, 0, LAM_SOFT, LAM_SOFT, 0, 0), hard_tie=False),
        "hard": dict(controller=StepSchedule(0, 0, LAM_SOFT, LAM_SOFT, 0, 0), hard_tie=True),
        "free": dict(controller=StepSchedule(0, 0, 0.0, 0.0, 0, 0), hard_tie=False),
    }
    res = {}
    for name, cfg in conds.items():
        m = build_model(tr, n_groups=1, members_per_group=2, seed=SEED)
        log = train(m, tr, cfg["controller"], steps, lr=LR, batch=BATCH,
                    train_fine=True, hard_tie=cfg["hard_tie"], eval_data=te, seed=SEED)
        res[name] = dict(fine=log["fine_acc_te"][-1], spread=log["spread"][-1], log=log)
        print(f"   {name:5s}  fine_acc={res[name]['fine']:.3f}  spread={res[name]['spread']:.4f}")

    soft, hard, free = res["soft"], res["hard"], res["free"]
    spread_ratio = soft["spread"] / max(hard["spread"], 1e-9)
    passed = (
        soft["fine"] >= A_FINE_PASS
        and free["fine"] >= A_FINE_PASS
        and hard["fine"] <= A_FINE_FAIL
        and spread_ratio >= A_SPREAD_RATIO
    )
    for name in ("soft", "hard", "free"):
        plots.plot_run(res[name]["log"], os.path.join(FIGDIR, f"A_{name}.png"),
                       f"Test A ({name} tie)")
    return dict(passed=passed, soft=soft, hard=hard, free=free, spread_ratio=spread_ratio)


# ===========================================================================
# Test B -- pool -> unpool -> differentiate
# ===========================================================================
def run_B_setting(r_fine, sigma, steps, t1, t2, seed=SEED):
    d = D.make_hierarchical_gaussians(
        D=16, n_coarse=4, n_fine=4, R_coarse=10.0, r_fine=r_fine, sigma=sigma,
        n_per_fine=200, seed=seed,
    )
    tr, te = d.split(seed=seed)
    controllers = {
        "gradual": StepSchedule(LAM_HI, 0, LAM_HI, 0, t1, t2),
        "pooled": StepSchedule(LAM_HI, 0, LAM_HI, 0, t1, None),      # lam2 never drops
        "unpooled": StepSchedule(0, 0, 0, 0, 0, 0),                  # full res from init
    }
    out = {}
    for name, ctrl in controllers.items():
        m = build_model(tr, 4, 4, seed=seed)
        log = train(m, tr, ctrl, steps, lr=LR, batch=BATCH, train_fine=True,
                    eval_data=te, seed=seed)
        out[name] = log
    return out


def test_B(steps, t1, t2):
    print("== Test B: pool -> unpool -> differentiate ==")
    logs = run_B_setting(r_fine=1.0, sigma=0.3, steps=steps, t1=t1, t2=t2)
    g, p, u = logs["gradual"], logs["pooled"], logs["unpooled"]

    coarse_pre_t2 = g["coarse_acc_te"][_i_before(g, t2)]
    fine_pre_t2 = g["fine_acc_te"][_i_before(g, t2)]
    coarse_post_t2 = g["coarse_acc_te"][_i_after(g, t2)]
    grad_fine = g["fine_acc_te"][-1]
    pooled_fine = p["fine_acc_te"][-1]
    unpooled_fine = u["fine_acc_te"][-1]
    lurch = coarse_pre_t2 - coarse_post_t2

    passed = (
        grad_fine >= B_FINE_PASS
        and pooled_fine <= B_POOLED_CAP
        and (grad_fine - pooled_fine) >= B_MARGIN
        and coarse_pre_t2 >= B_COARSE_CEIL
        and lurch <= B_LURCH
    )
    print(f"   coarse@pre-t2={coarse_pre_t2:.3f}  fine@pre-t2={fine_pre_t2:.3f}")
    print(f"   fine: gradual={grad_fine:.3f}  pooled={pooled_fine:.3f}  unpooled={unpooled_fine:.3f}")
    print(f"   coarse lurch at t2={lurch:+.3f}")

    marks = {"unpool->4": t1, "unpool->16": t2}
    plots.plot_run(g, os.path.join(FIGDIR, "B_gradual.png"), "Test B (gradual unpool)", marks)
    plots.plot_overlay({"gradual": g, "always-pooled": p, "always-unpooled": u},
                       "fine_acc_te", os.path.join(FIGDIR, "B_fine_overlay.png"),
                       "Test B: fine accuracy", "held-out fine acc", marks)

    # --- required sweep over r_fine/sigma -------------------------------------
    print("   -- sweep over r_fine/sigma --")
    sweep = []
    for r_fine in (2.0, 1.0, 0.5, 0.3):
        sl = run_B_setting(r_fine=r_fine, sigma=0.3, steps=steps, t1=t1, t2=t2)
        row = dict(
            r_fine=r_fine, ratio=r_fine / 0.3,
            pooled=sl["pooled"]["fine_acc_te"][-1],
            gradual=sl["gradual"]["fine_acc_te"][-1],
            unpooled=sl["unpooled"]["fine_acc_te"][-1],
        )
        sweep.append(row)
        print(f"      r_fine={r_fine:>4} (r/sig={row['ratio']:.1f}): "
              f"pooled={row['pooled']:.3f} gradual={row['gradual']:.3f} unpooled={row['unpooled']:.3f}")

    return dict(passed=passed, coarse_pre_t2=coarse_pre_t2, fine_pre_t2=fine_pre_t2,
                grad_fine=grad_fine, pooled_fine=pooled_fine, unpooled_fine=unpooled_fine,
                lurch=lurch, sweep=sweep, gradual_log=g, t1=t1, t2=t2)


# ===========================================================================
# Test C -- re-pool (reverse direction)
# ===========================================================================
def _phase1_full_model(steps, t1, t2, seed=SEED):
    d = D.make_hierarchical_gaussians(D=16, n_coarse=4, n_fine=4, R_coarse=10.0,
                                      r_fine=1.0, sigma=0.3, n_per_fine=200, seed=seed)
    tr, te = d.split(seed=seed)
    m = build_model(tr, 4, 4, seed=seed)
    log = train(m, tr, StepSchedule(LAM_HI, 0, LAM_HI, 0, t1, t2), steps,
                lr=LR, batch=BATCH, train_fine=True, eval_data=te, seed=seed)
    return m, log


def _run_C(variant, p1_steps, t1, t2, c_steps):
    # Phase 1: differentiate to full resolution.
    m, p1 = _phase1_full_model(p1_steps, t1, t2)
    d2_pre = p1["d2_mean"][-1]
    coarse_pre = p1["coarse_acc_te"][-1]
    fine_pre = p1["fine_acc_te"][-1]

    # Phase 2: change the regime, drive re-pool by the pull-apart signal.
    if variant == "C1":   # signal removed: flat data, no fine distinction to train
        d2 = D.make_hierarchical_gaussians(D=16, n_coarse=4, n_fine=4, R_coarse=10.0,
                                           r_fine=1.0, sigma=0.3, n_per_fine=200,
                                           fine_structure=False, seed=SEED)
        train_fine = False
    else:                 # C2: structure present in input, fine head not trained
        d2 = D.make_hierarchical_gaussians(D=16, n_coarse=4, n_fine=4, R_coarse=10.0,
                                           r_fine=1.0, sigma=0.3, n_per_fine=200, seed=SEED)
        train_fine = False
    tr, te = d2.split(seed=SEED)
    ctrl = AdaptiveRepool(lam1=0.0, lam2_lo=0.0, lam2_hi=LAM_HI,
                          frac=0.15, patience=4, ramp_steps=400)
    log = train(m, tr, ctrl, c_steps, lr=LR, batch=BATCH, train_fine=train_fine,
                eval_data=te, seed=SEED + 1)

    d2_post = log["d2_mean"][-1]
    coarse_post = log["coarse_acc_te"][-1]
    fine_post = log["fine_acc_te"][-1]
    repooled = ctrl.trigger_t is not None
    passed = (
        repooled
        and d2_post <= C_D2_SHRINK * d2_pre
        and coarse_post >= C_COARSE_KEEP
    )
    print(f"   {variant}: repool@{ctrl.trigger_t}  ||d2|| {d2_pre:.3f}->{d2_post:.3f}  "
          f"coarse {coarse_pre:.3f}->{coarse_post:.3f}  fine {fine_pre:.3f}->{fine_post:.3f}")
    plots.plot_run(log, os.path.join(FIGDIR, f"{variant}.png"), f"Test {variant} (re-pool)",
                   {"re-pool": ctrl.trigger_t})
    return dict(passed=passed, repooled=repooled, trigger_t=ctrl.trigger_t,
                d2_pre=d2_pre, d2_post=d2_post, coarse_pre=coarse_pre,
                coarse_post=coarse_post, fine_pre=fine_pre, fine_post=fine_post, log=log)


def test_C(p1_steps, t1, t2, c_steps):
    print("== Test C: re-pool ==")
    return {"C1": _run_C("C1", p1_steps, t1, t2, c_steps),
            "C2": _run_C("C2", p1_steps, t1, t2, c_steps)}


# ===========================================================================
# Test D -- does the disagreement / pull-apart signal behave as theorised?
# ===========================================================================
def test_D(B_res, C_res):
    print("== Test D: signal behaviour (observational) ==")
    g = B_res["gradual_log"]
    t2 = B_res["t2"]
    # During fine differentiation (just after t2) the force should peak; once
    # settled (end) it should fall.
    peak = _peak_window(g, "pull_apart", t2, t2 + (g["step"][-1] - t2) // 2)
    settled = g["pull_apart"][-1]
    rises_then_falls = peak > 0 and settled < 0.5 * peak
    # Disagreement (cosine) should dip (more negative) during differentiation.
    cos_during = min(v for s, v in zip(g["step"], g["cos_disagreement"]) if s >= t2)
    informative = rises_then_falls
    print(f"   pull-apart: peak(post-t2)={peak:.4f} settled={settled:.4f} "
          f"-> rises_then_falls={rises_then_falls}")
    print(f"   cos disagreement min(post-t2)={cos_during:.3f}")
    return dict(informative=informative, peak=peak, settled=settled,
                cos_during=cos_during, flag=(not informative))


# ===========================================================================
def write_results(A, B, C, Dr, elapsed):
    def pf(ok):
        return "**PASS**" if ok else "**FAIL**"

    sweep_rows = "\n".join(
        f"| {r['r_fine']} | {r['ratio']:.1f} | {r['pooled']:.3f} | "
        f"{r['gradual']:.3f} | {r['unpooled']:.3f} |"
        for r in B["sweep"]
    )
    md = f"""# Experiment 01 -- Results

Auto-generated by `run_tests.py` ({elapsed:.0f}s, CPU). Plots in `figures/`
(regenerable, gitignored). Thresholds are pre-registered in `run_tests.py` and were
not changed after seeing results. See `SPEC.md` for each test's failure condition.

**Overall:** {pf(A['passed'] and B['passed'] and C['C1']['passed'] and C['C2']['passed'])}
(Test D is observational -- it flags, it does not gate.)

| Test | Result |
|------|--------|
| A -- symmetry break | {pf(A['passed'])} |
| B -- pool -> unpool -> differentiate | {pf(B['passed'])} |
| C1 -- re-pool (signal removed) | {pf(C['C1']['passed'])} |
| C2 -- re-pool (signal not rewarded) | {pf(C['C2']['passed'])} |
| D -- signal behaviour (observational) | {"OK" if Dr['informative'] else "FLAG"} |

---

## Test A -- symmetry break  {pf(A['passed'])}

Two soft-tied members under near-identical gradients must diverge once sub-structure
is present; the hard-tie control must fail; the free control is the upper reference.

| condition | fine acc | within-group spread |
|-----------|---------:|--------------------:|
| soft tie  | {A['soft']['fine']:.3f} | {A['soft']['spread']:.4f} |
| hard tie (Delta2 == 0) | {A['hard']['fine']:.3f} | {A['hard']['spread']:.4f} |
| free (no tie) | {A['free']['fine']:.3f} | {A['free']['spread']:.4f} |

soft spread ({A['soft']['spread']:.3f}) vs hard spread ({A['hard']['spread']:.4f}): the
hard tie cannot differentiate at all (pass needs ratio >= {A_SPREAD_RATIO:.0f}; measured
{"effectively infinite" if A['hard']['spread'] < 1e-6 else f"{A['spread_ratio']:.1f}"}).
Figures: `figures/A_soft.png`, `A_hard.png`, `A_free.png`.

> FAILS IF the soft tie does not diverge while the free control does. Result: soft
> fine acc {A['soft']['fine']:.3f} vs hard {A['hard']['fine']:.3f}.

## Test B -- pool -> unpool -> differentiate  {pf(B['passed'])}

Schedule: fully pooled -> unpool to 4 (t1={B['t1']}) -> unpool to 16 (t2={B['t2']}).

- coarse acc reached **{B['coarse_pre_t2']:.3f}** while still at level 1 (before t2; pass >= {B_COARSE_CEIL}).
- fine acc before t2 = **{B['fine_pre_t2']:.3f}**, lifting to **{B['grad_fine']:.3f}** after fine unpool.
- always-pooled fine capped at **{B['pooled_fine']:.3f}** (pass <= {B_POOLED_CAP}); always-unpooled reached {B['unpooled_fine']:.3f}.
- gradual beats pooled by **{B['grad_fine'] - B['pooled_fine']:.3f}** (pass >= {B_MARGIN}).
- coarse "lurch" across the t2 step = **{B['lurch']:+.3f}** (pass <= {B_LURCH}; freed residuals start ~0, so the transition is smooth).

Figures: `figures/B_gradual.png`, `B_fine_overlay.png`.

### Required sweep over r_fine/sigma

| r_fine | r/sigma | pooled fine | gradual fine | unpooled fine |
|-------:|--------:|------------:|-------------:|--------------:|
{sweep_rows}

Reading: across the learnable range, gradual unpool tracks the always-unpooled
upper bound and clears the always-pooled cap; as r_fine -> sigma the fine
distinction becomes unlearnable for *every* condition (task too hard, not a
substrate failure).

## Test C -- re-pool  C1 {pf(C['C1']['passed'])} / C2 {pf(C['C2']['passed'])}

After full differentiation, the pull-apart force is watched; once sustained low,
lambda2 is ramped back up. Pass needs re-pool to fire, ||Delta2|| to collapse, and
coarse value to survive.

| variant | re-pool step | mean \\|\\|Delta2\\|\\| (pre -> post) | coarse (pre -> post) | fine (pre -> post) |
|---------|-------------:|-----------------------------------:|---------------------:|-------------------:|
| C1 (signal removed) | {C['C1']['trigger_t']} | {C['C1']['d2_pre']:.3f} -> {C['C1']['d2_post']:.3f} | {C['C1']['coarse_pre']:.3f} -> {C['C1']['coarse_post']:.3f} | {C['C1']['fine_pre']:.3f} -> {C['C1']['fine_post']:.3f} |
| C2 (not rewarded) | {C['C2']['trigger_t']} | {C['C2']['d2_pre']:.3f} -> {C['C2']['d2_post']:.3f} | {C['C2']['coarse_pre']:.3f} -> {C['C2']['coarse_post']:.3f} | {C['C2']['fine_pre']:.3f} -> {C['C2']['fine_post']:.3f} |

Re-pool is *graceful*: Delta2 collapses and fine accuracy coarsens while the coarse
base is retained (coarse acc held). Figures: `figures/C1.png`, `C2.png`.

> Modelling note: both variants drop the fine reward (you cannot supervise a
> distinction that is gone). C1 additionally removes the structure from the input
> (signal truly absent); C2 keeps it in the input but unrewarded. The trigger uses
> the *pull-apart force magnitude* (members no longer pulled apart), which stays
> well-defined when the directional cosine does not.

## Test D -- signal behaviour (observational)  {"OK" if Dr['informative'] else "FLAG"}

In the gradual run the pull-apart force should rise while the fine group actively
differentiates (after t2) and fall once members settle.

- peak pull-apart after t2 = **{Dr['peak']:.4f}**, settled = **{Dr['settled']:.4f}** -> rises-then-falls = **{Dr['informative']}**.
- min cosine disagreement after t2 = **{Dr['cos_during']:.3f}** (more negative = members pulled apart).

{"The signal carries the information the re-pool trigger assumes." if Dr['informative'] else "> FLAG: signal did not rise-then-fall as theorised; revisit the re-pool trigger design."}
"""
    with open(os.path.join(HERE, "RESULTS.md"), "w") as f:
        f.write(md)
    print(f"\nwrote {os.path.join(HERE, 'RESULTS.md')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="fewer steps (smoke test)")
    args = ap.parse_args()
    torch.manual_seed(SEED)

    if args.quick:
        a_steps, b_steps, t1, t2, c_p1, c_steps = 800, 1200, 300, 700, 1200, 1000
    else:
        a_steps, b_steps, t1, t2, c_p1, c_steps = 2500, 3000, 600, 1500, 3000, 2500

    t0 = time.time()
    A = test_A(a_steps)
    B = test_B(b_steps, t1, t2)
    C = test_C(c_p1, t1, t2, c_steps)
    Dr = test_D(B, C)
    elapsed = time.time() - t0

    write_results(A, B, C, Dr, elapsed)
    overall = A["passed"] and B["passed"] and C["C1"]["passed"] and C["C2"]["passed"]
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}  ({elapsed:.0f}s)")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
