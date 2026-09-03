"""Revival-config WIRING ASSERTS (Guard 4 of the build brief; run BEFORE any entry read).

Three cheap invariants so an entry-gate fail can never be a silent wiring bug, plus two
equivalence/mechanism checks. This is NOT the entry read (quick config, no verdict): with
these green, a later dead-pattern read is genuine, not plumbing.

  A. PenaltySpec == deployed tie_schedule equivalence (the shared-implementation proof).
  B. Mean-centre exactness: population mean of the re-posed vision-cue population == 0
     by construction (content-blind common-mode removal is exact at alpha=1).
  C. Tie values at the onsets match the two-clock schedule ((10,10)->(0,10)->(0,0)),
     and the penalty term is exactly 0 once both clocks are open.
  D. Prototype-spread live column from t=0 (the death-certificate watch) + the posed frame
     asserts B on the LIVE loop at several points along training.
  E. Channel-alive mechanism evidence (reported, not gated): does word->vision evocation
     divergence come off the floor under the revival config where the disease config sat
     at ~1e-8? Read via conflict_validity._evocation_divergence (one code path).
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

import constants                                             # noqa: E402  (exp04)
import exp07_config as C                                     # noqa: E402
from exp07_core import PenaltySpec                           # noqa: E402
from revival import tie_schedule                             # noqa: E402
from sculpt_config import quick_sculpt                       # noqa: E402
from sculpt_loop import SculptLoop                           # noqa: E402
from conflict_validity import _evocation_divergence          # noqa: E402


def _inline_lam12(reg: dict, t: int):
    """INDEPENDENT reference: the pre-refactor PenaltySpec.lam12_at inline form, verbatim.
    (PenaltySpec now delegates to tie_schedule, so comparing those two alone would be
    self-referential; this inline form is the third, independent implementation.)"""
    lam1 = reg["lam1_lo"] if t >= reg["t1_step"] else reg["lam1_hi"]
    lam2 = reg["lam2_lo"] if t >= reg["t2_step"] else reg["lam2_hi"]
    return lam1, lam2


def check_A_equivalence():
    for name in ("off", "deployed", "reshaped"):
        reg = C.PENALTY_REGIMES[name]
        spec = PenaltySpec(name=name, **reg)
        sched = tie_schedule(**{k: reg[k]
                                for k in ("lam1_hi", "lam1_lo", "t1_step", "lam2_hi", "lam2_lo", "t2_step")})
        for t in list(range(0, 40001, 7)) + [899, 900, 901, 3599, 3600, 3601]:
            ref = _inline_lam12(reg, t)
            assert (sched.lam1(t), sched.lam2(t)) == ref, ("sched", name, t)
            assert spec.lam12_at(t) == ref, ("spec", name, t)
    print("A. tie_schedule == pre-refactor inline form == PenaltySpec (independent reference): "
          "OK (3 regimes, dense t incl. onsets)")


def _posed_population_residual(loop) -> float:
    """|| population mean of the re-posed vision-cue population || (must be ~0 at alpha=1)."""
    cfg = loop.cfg
    a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    e = loop.vision.emit(loop.stim.raw_clean(a, b))                     # (M, D) the cue population
    content = torch.zeros(e.shape[0], 1, cfg.n_slots, cfg.D)
    content[:, 0, 0, :] = e
    posed = loop._pose_pam_input(content)[:, 0, 0, :]
    return posed.mean(0).norm().item()


def check_B_meancentre(loop):
    r = _posed_population_residual(loop)
    assert r < 1e-5, f"mean-centre residual {r}"
    print(f"B. mean-centre exactness (posed population mean ~0): OK (residual {r:.2e})")


def check_B2_ablation_analogue(loop):
    """Deployed analogue of exp07's reposing_validation guard (B): a member-information-free
    (identical) vision-cue population must remain IDENTICAL after posing — mu cannot manufacture
    separation (it is subtracted equally from every member)."""
    cfg = loop.cfg
    M = cfg.n_A * cfg.n_B
    same = torch.ones(M, 1, cfg.n_slots, cfg.D)
    posed = loop._pose_pam_input(same)[:, 0, 0, :]
    sep = torch.cdist(posed, posed).max().item()
    assert sep == 0.0, f"identical (ablated-analogue) population separated after posing: {sep}"
    print(f"B2. ablation analogue (identical population poses identical; mu manufactures nothing): "
          f"OK (max sep {sep})")


def check_C_tie(loop):
    cfg = loop.cfg
    t1 = cfg.pam_t1 if cfg.pam_t1 is not None else cfg.t1
    t2 = cfg.pam_t2 if cfg.pam_t2 is not None else cfg.t2
    expect = {0: (cfg.lam1_hi, cfg.lam2_hi), t1 - 1: (cfg.lam1_hi, cfg.lam2_hi),
              t1: (cfg.lam1_lo, cfg.lam2_hi), t2 - 1: (cfg.lam1_lo, cfg.lam2_hi),
              t2: (cfg.lam1_lo, cfg.lam2_lo), cfg.steps - 1: (cfg.lam1_lo, cfg.lam2_lo)}
    for t, e in expect.items():
        got = (loop.pam_tie_sched.lam1(t), loop.pam_tie_sched.lam2(t))
        assert got == e, (t, got, e)
    pen_open = float(loop._pam_penalty(t2).detach())
    assert pen_open == 0.0, f"penalty at open clocks should be exactly 0, got {pen_open}"
    print(f"C. two-clock tie at onsets ({t1}/{t2}: (10,10)->(0,10)->(0,0)), penalty==0 when open: OK")


def run_D_E(loop, steps: int):
    cfg = loop.cfg
    rows = []
    for t in range(steps):
        loop.step(no_word=False)
        if t % cfg.eval_every == 0 or t == steps - 1:
            div = _evocation_divergence(loop, associative=True)
            r = _posed_population_residual(loop)
            assert r < 1e-5, f"mean-centre residual drifted to {r} at t={t}"
            ps = loop.pam_proto_spread()
            assert ps == ps and ps != float("inf"), "proto_spread not finite"
            rows.append((t + 1, ps, div["category_divergence"], div["distractor_divergence"]))
    print("D. live columns from t=0 (proto_spread + posed-frame residual re-asserted along training): OK")
    print(f"   t={'':>6} proto_spread  cat_div     dist_div")
    for t, ps, cd, dd in rows:
        print(f"   {t:>7} {ps:>12.4f} {cd:>10.4g} {dd:>10.4g}")
    return rows


def main():
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))
    check_A_equivalence()

    pin = constants.PinnedConstants()
    cfg = quick_sculpt(seed=0)                                # revival config = the defaults
    loop = SculptLoop(cfg, pin)
    check_B_meancentre(loop)
    check_B2_ablation_analogue(loop)
    check_C_tie(loop)
    rows = run_D_E(loop, cfg.steps)

    # E: mechanism evidence (not a gate): the disease config for contrast
    dis_cfg = quick_sculpt(seed=0, reposing_alpha=0.0, pam_tie="constant")
    dis = SculptLoop(dis_cfg, pin)
    for _ in range(dis_cfg.steps):
        dis.step(no_word=False)
    d_rev = rows[-1][2]
    d_dis = _evocation_divergence(dis, associative=True)["category_divergence"]
    print(f"E. channel evidence (quick config, NOT the entry read): revival cat_div={d_rev:.4g} "
          f"vs disease cat_div={d_dis:.4g}  (revival proto_spread={rows[-1][1]:.4f}, "
          f"disease proto_spread={dis.pam_proto_spread():.4f})")
    print("\nWIRING ASSERTS: ALL GREEN")


if __name__ == "__main__":
    main()
