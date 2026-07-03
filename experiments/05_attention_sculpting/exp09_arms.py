"""EXP09 — the self-path #12 reference: SlowRefLoop + the function-test arms + the
decomposition observable + the baseline replays.

Pre-registration: docs/EXP09_SELF_REFERENCE_PREREG.md (checkpoint RESOLVED 2026-07-03;
all constants below are the resolved values — never re-derived here). Sequence: wire ->
ONE final pre-run read (resolved prereg + wiring asserts + replayed-baseline
decomposition panels) -> arms run. Gate steps 5-6 BLOCKED.

The design (EXP09 SS1-SS3): a slow copy of the vision cortex supplies the SELF-PATH
reconstruction target only — detached (reference, not co-developer), birth = bit-copy of
online at t=0 (stored), post-optimizer-step fixed-lag update theta_slow += beta *
(theta_online - theta_slow), tau = 1/beta = 9600 waves (RULE: 2x the pinned den period
4800; instrument of record = the cadence-100 entry-run series). Route = the existing
identity-default hooks, one code path: the build_cells WRAP below rewrites the TARGET's
vision rows from the returned window raw under no_grad; word rows untouched (asserted).
Ground (3) as re-worded: teaching path RE-ROUTED, not intact — the canonical target-side
gap-3 pressure is severed at every beta; the design is a recorded BET, certified or
refuted by the detach-null comparator + outcome-level divergence (stop-grad-in-costume =
the pre-registered partial outcome).

Probe hygiene (SS7, asserted): all EXP09 probes are RNG-ISOLATED (clean centres /
private generators; loop.gen never touched — asserted per probe call) and the per-member
gradient probe uses ONE fixed mask geometry across all members (equalized); the standing
word/self grad_split keeps its asymmetric pair with the ~4.0 mechanical geometry factor
RECORDED as an instrument caveat, never compared across probe classes.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import constants                                              # noqa: E402  (exp04)
import exp08_arms as A                                        # noqa: E402  (the shared runner)
from revival import dynamics_panel                            # noqa: E402
from sculpt_config import SculptConfig                        # noqa: E402

OUTDIR = A.OUTDIR
EVAL, BLOCK = A.EVAL, A.BLOCK

# --- resolved constants (EXP09 SS4-SS5; values land HERE from the prereg, nowhere else) ---
TAU = 9600                       # 1/beta = 2 x pinned den period 4800 (rule; resolution executed)
BETA = 1.0 / TAU
PERIOD_WORD = 4800               # instrument of record: entry-run cadence-100 series
PERIOD_NOWORD = 23100
FLOOR = 1e-3                     # den collapse-floor tripwire (one-sided)
K_W = 3                          # word-arm PIN duration (periods)
K_C = 8                          # control PIN duration (periods; > measured 5.9 regrown max)
PASS_WINDOWS = 32                # final 2 word periods at cadence 300
PASS_K_MIN = 27                  # argmax_k>1 in >=27/32 (healthy worst placement = 27)
PASS_RUN_MAX = 2                 # no argmax_k=1 run longer than 2 (healthy max run = 2)
PERIOD_CHANGE_FACTOR = 1.5       # run's own healthy-segment period substitutes only beyond this
HORIZON = 192000                 # 2 x the 96k s0 terminal clock


# ------------------------------------------------------------------ the loop
class SlowRefLoop(A.EXP08Loop):
    """EXP08Loop + the self-path slow reference. ONE new piece of state (the slow copy +
    its stored birth snapshot); dynamics, losses, masking, word path all inherited
    UNCHANGED (wiring assert: step() is the inherited Stage0Loop.step — no new loss
    term, no new force)."""

    def __init__(self, cfg, pin, beta: float = BETA):
        super().__init__(cfg, pin)
        self.slow_beta = float(beta)
        self.vision_slow = copy.deepcopy(self.vision)
        for p in self.vision_slow.parameters():
            p.requires_grad_(False)
        self.vision_birth = copy.deepcopy(self.vision_slow)   # stored t=0 snapshot (SS6.1)
        # wiring assert: identity at t=0
        assert self._ref_param_dist(self.vision_slow, self.vision) == 0.0, "birth != online at t=0"
        assert self._ref_param_dist(self.vision_birth, self.vision_slow) == 0.0

    @staticmethod
    @torch.no_grad()
    def _ref_param_dist(m1, m2) -> float:
        return float(sum((p1 - p2).pow(2).sum() for p1, p2 in
                         zip(m1.parameters(), m2.parameters())).sqrt())

    def build_cells(self, t, *, no_word, gen, ablate="none", force_mask=None):
        bc = super().build_cells(t, no_word=no_word, gen=gen, ablate=ablate,
                                 force_mask=force_mask)
        cfg = self.cfg
        with torch.no_grad():
            slow_vis = self.vision_slow.emit(bc["raw"])        # (W, D), no grad by construction
        tgt = bc["target"].clone()
        vis_rows = torch.arange(cfg.W) * cfg.n_slots           # vision slot = 0 in every wave
        word_rows_before = tgt[vis_rows + 1].detach().clone()
        tgt[vis_rows] = slow_vis                               # the ONLY change: vision-row targets
        if self._t < 5 or self._t % BLOCK == 0:                # sampled wiring asserts
            assert torch.equal(tgt[vis_rows + 1], word_rows_before), "word target rows touched"
            assert not any(p.requires_grad for p in self.vision_slow.parameters())
        bc["target"] = tgt
        return bc

    def _post_step(self):
        super()._post_step()                                   # constant Delta2 re-pool (G3)
        with torch.no_grad():
            for ps, po in zip(self.vision_slow.parameters(), self.vision.parameters()):
                ps.add_(self.slow_beta * (po - ps))


# ------------------------------------------------------------------ RNG-isolated probes
def _member_set(cfg):
    a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    return a, b


def _rng_guard(loop):
    return loop.gen.get_state()


def _rng_check(loop, state, where: str):
    assert torch.equal(loop.gen.get_state(), state), f"probe touched loop.gen: {where}"


@torch.no_grad()
def evo_decomp(loop) -> dict:
    """Evocation split (SS7): common vs differential energy over the 16-member
    associative evocation set. Clean centres; RNG-free (asserted)."""
    st = _rng_guard(loop)
    ma, mb = _member_set(loop.cfg)
    e = loop.evoke_vision(ma, mb, associative=True)            # (16, D)
    mu = e.mean(0)
    common = float(mu.pow(2).sum())
    diff = float((e - mu).pow(2).sum(1).mean())
    _rng_check(loop, st, "evo_decomp")
    return dict(evo_common=common, evo_diff=diff,
                evo_ratio=(common / diff) if diff > 1e-30 else None)


def grad_decomp(loop, no_word: bool) -> dict:
    """Gradient split, same decomposition (SS7): per-member teaching gradient g_i =
    dL_PAM/d(e_vis_i) on a probe frame under the ACTIVE target regime, ONE fixed mask
    geometry for every member (equalized — never the asymmetric word/self pair, which
    carries the ~4.0 mechanical geometry factor). Clean centres; fixed drift carrier;
    RNG-free (asserted); no optimizer step; block-diagonal windows -> grad rows are
    per-member."""
    st = _rng_guard(loop)
    cfg = loop.cfg
    W, K = cfg.W, cfg.n_A * cfg.n_B
    ma, mb = _member_set(cfg)
    e_vis = loop.vision.emit(loop.stim.raw_clean(ma, mb))      # (16, D) grad-attached
    tokens = (torch.full((K,), loop.word.null_token, dtype=torch.long) if no_word
              else loop._word_label(mb, ma))
    e_word = loop.word.emit(tokens)
    content = torch.zeros(K, W, cfg.n_slots, cfg.D)
    content[:, :, 0, :] = e_vis.unsqueeze(1)
    content[:, :, 1, :] = e_word.unsqueeze(1)
    # the ONE fixed geometry: read-slot vision cell masked, everything else visible
    mask = torch.zeros(W, cfg.n_slots, dtype=torch.bool)
    mask[1, 0] = True
    # target under the ACTIVE regime (baseline: online, grad-attached = training-faithful;
    # slow-ref: the slow copy's emissions, no grad — training-faithful likewise)
    if hasattr(loop, "vision_slow"):
        with torch.no_grad():
            tgt_vis = loop.vision_slow.emit(loop.stim.raw_clean(ma, mb))
    else:
        tgt_vis = e_vis
    masked = loop._pose_pam_input(content).clone()
    masked[:, mask] = loop.op.mask_emb
    drift_w = torch.arange(W, dtype=torch.float32) - (W - 1) / 2.0
    cells = (masked + loop.cb.kappa * drift_w.view(1, W, 1, 1) * loop.cb.u
             ).reshape(K, W * cfg.n_slots, cfg.D)
    visible = (~mask).reshape(W * cfg.n_slots)
    pred = loop.op(cells, loop.slot_ids, visible)              # (K, C, D)
    read = pred[:, 1 * cfg.n_slots + 0, :]                     # the masked vision cell
    loss = (read - tgt_vis).pow(2).mean()
    g = torch.autograd.grad(loss, e_vis, retain_graph=False)[0]  # (16, D) per-member rows
    gb = g.mean(0)
    common = float(gb.pow(2).sum())
    diff = float((g - gb).pow(2).sum(1).mean())
    _rng_check(loop, st, "grad_decomp")
    return dict(grad_common=common, grad_diff=diff,
                grad_ratio=(common / diff) if diff > 1e-30 else None)


@torch.no_grad()
def ref_columns(loop) -> dict:
    """SS6.1 reference-distinctness columns (slow arms only): param dist to online,
    param dist to the stored birth snapshot, target-space dist, pairwise slow-target
    distinctness (copy-collapse watch). RNG-free (asserted)."""
    st = _rng_guard(loop)
    ma, mb = _member_set(loop.cfg)
    raw_c = loop.stim.raw_clean(ma, mb)
    slow_t = loop.vision_slow.emit(raw_c)
    online_t = loop.vision.emit(raw_c)
    off = ~torch.eye(slow_t.shape[0], dtype=torch.bool)
    out = dict(
        ref_param_dist=SlowRefLoop._ref_param_dist(loop.vision_slow, loop.vision),
        ref_birth_dist=SlowRefLoop._ref_param_dist(loop.vision_slow, loop.vision_birth),
        ref_target_dist=float((slow_t - online_t).norm(dim=1).mean()),
        ref_pairwise=float(torch.cdist(slow_t, slow_t)[off].mean()))
    _rng_check(loop, st, "ref_columns")
    return out


@torch.no_grad()
def pairwise_emit(loop) -> dict:
    """Baseline analogue of the pairwise column (replays): pairwise distinctness of the
    ONLINE emissions — the quantity the slow copy would have carried; the SS6.1 floor is
    set from its healthy-span value at the final pre-run read."""
    st = _rng_guard(loop)
    ma, mb = _member_set(loop.cfg)
    e = loop.vision.emit(loop.stim.raw_clean(ma, mb))
    off = ~torch.eye(e.shape[0], dtype=torch.bool)
    out = dict(pairwise_emit=float(torch.cdist(e, e)[off].mean()))
    _rng_check(loop, st, "pairwise_emit")
    return out


def probes_for(no_word: bool):
    """The per-EVAL probe callback handed to the shared runner (RNG-isolated; asserted
    inside each probe)."""
    def fn(lp):
        out = {}
        out.update(evo_decomp(lp))
        out.update(grad_decomp(lp, no_word))
        out.update(pairwise_emit(lp))
        if hasattr(lp, "vision_slow"):
            out.update(ref_columns(lp))
        return out
    return fn


# ------------------------------------------------------------------ the function-test read
def _healthy_segment_period(cols, pinned: int) -> dict:
    """SS5 period pin: dynamics_panel on the HEALTHY SEGMENT only (windows before the
    last asg_argmax_k>1 window, excluding the first 20100 waves of ramp); the run's own
    period substitutes for the pinned constant only beyond PERIOD_CHANGE_FACTOR, logged."""
    ts = [c["t"] for c in cols]
    ks = [c["asg_argmax_k"] for c in cols]
    last_alive = max((t for t, k in zip(ts, ks) if k > 1), default=None)
    seg = [(t, c["den"]) for t, c in zip(ts, cols) if t >= 20100 and (last_alive is None or t <= last_alive)]
    if len(seg) < 8:
        return dict(measured=None, used=pinned, substituted=False, note="segment too short")
    p = dynamics_panel([t for t, _ in seg], [v for _, v in seg])["dominant_period_steps"]
    if p is None:
        return dict(measured=None, used=pinned, substituted=False, note="estimator None -> pinned")
    sub = (p > pinned * PERIOD_CHANGE_FACTOR) or (p < pinned / PERIOD_CHANGE_FACTOR)
    return dict(measured=int(p), used=int(p) if sub else pinned, substituted=bool(sub))


def _epochs(cols, period: int):
    """Qualifying epochs: argmax_k==1 AND den<FLOOR in every window, length >= 1 period."""
    runs, cur = [], []
    for c in cols:
        if c["asg_argmax_k"] == 1 and c["den"] < FLOOR:
            cur.append(c)
        else:
            if cur:
                runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    out = []
    for r in runs:
        span = r[-1]["t"] - r[0]["t"] + EVAL
        if span >= period:
            out.append(dict(start=r[0]["t"], end=r[-1]["t"], span=span,
                            periods=round(span / period, 2),
                            at_horizon=r[-1]["t"] == cols[-1]["t"]))
    return out


def function_test_read(cols, *, control: bool) -> dict:
    """The SS5 taxonomy, literal forms, resolved constants. Control arms: PIN/K_C +
    PIN-CENSORED only (never held to PASS)."""
    pinned = PERIOD_NOWORD if control else PERIOD_WORD
    per = _healthy_segment_period(cols, pinned)
    period = per["used"]
    K = K_C if control else K_W
    eps = _epochs(cols, period)
    episodes = [e for e in eps if not e["at_horizon"]]
    verdict_pin = None
    for e in eps:
        if e["at_horizon"]:
            if e["span"] >= K * period:
                verdict_pin = dict(kind="PIN", epoch=e)
            else:
                verdict_pin = dict(kind="PIN_CENSORED" if control else
                                   ("PIN" if e["span"] >= K_W * period else "PIN_CENSORED"),
                                   epoch=e)
    out = dict(period_resolution=per, period=period, K=K,
               metastable_episodes=episodes, horizon_epoch=verdict_pin)
    if control:
        out["verdict"] = (verdict_pin["kind"] if verdict_pin else "NO_PIN")
        return out
    # PASS criteria (word arms): final 32 windows
    fin = cols[-PASS_WINDOWS:]
    k_ok = sum(1 for c in fin if c["asg_argmax_k"] > 1)
    run = best = 0
    for c in fin:
        run = run + 1 if c["asg_argmax_k"] == 1 else 0
        best = max(best, run)
    den_ok = sum(1 for c in fin if c["den"] >= FLOOR)
    num_frozen = (max(c["num"] for c in fin) - min(c["num"] for c in fin)) < 1e-3
    crit = dict(k_gt1_count=k_ok, k_gt1_min=PASS_K_MIN, k1_run_max=best,
                k1_run_limit=PASS_RUN_MAX, den_ok_count=den_ok, den_ok_min=PASS_WINDOWS,
                num_frozen_logged=bool(num_frozen))
    pinned_fail = verdict_pin is not None and verdict_pin["kind"] == "PIN"
    passed = (not pinned_fail and k_ok >= PASS_K_MIN and best <= PASS_RUN_MAX
              and den_ok == PASS_WINDOWS)
    out["pass_criteria"] = crit
    out["verdict"] = ("FAIL_PIN" if pinned_fail else
                      "PASS_PENDING_SCREEN" if passed else
                      verdict_pin["kind"] if verdict_pin else "NEITHER")
    return out


# ------------------------------------------------------------------ arms + replays
ARMS9 = {
    "slowref_word":   dict(loop="slow", no_word=False, steps=HORIZON, seeds=[0, 1]),
    "slowref_noword": dict(loop="slow", no_word=True, steps=HORIZON, seeds=[0]),
    "detachnull":     dict(loop="detach", no_word=False, steps=HORIZON, seeds=[1]),
}
REPLAYS = {"word_terminal": 1, "marathon_ext": 0}


def run_exp09_arm(arm_name: str, seed: int, steps_override: int | None = None):
    spec9 = ARMS9[arm_name]
    steps = steps_override or spec9["steps"]
    no_word = spec9["no_word"]
    # one code path: the shared runner does everything; only the loop class + horizon
    # + probes differ. Register a transient arm spec so build_loop/manifest see it.
    loop_cls = SlowRefLoop if spec9["loop"] == "slow" else A.DetachLoop
    A.ARMS[arm_name] = dict(loop=loop_cls, no_word=no_word, steps=steps, seeds=spec9["seeds"])
    # save_state_at_end=False: A.save_state does not carry vision_slow/vision_birth —
    # an exp09 resume-grade save is its own (small) build item if an arm ever needs one.
    rec = A.run_arm(arm_name, seed, steps_override=steps,
                    probes=probes_for(no_word), save_state_at_end=False)
    read = function_test_read(rec["columns"], control=no_word)
    rec["function_test_read"] = read
    (OUTDIR / f"{arm_name}_s{seed}.json").write_text(json.dumps(rec, indent=2))
    print(f"{arm_name} s{seed}: {read['verdict']}")
    return rec


def run_replay(arm_name: str):
    """Baseline replay carrying the decomposition columns (SS7): bit-faithful standing
    columns asserted against the committed artifact — the end-to-end proof that the new
    probes are RNG-isolated."""
    seed = REPLAYS[arm_name]
    spec = A.ARMS[arm_name]
    rec = A.run_arm(arm_name, seed, probes=probes_for(spec.get("no_word", False)),
                    out_tag="decomp")
    committed = json.loads((OUTDIR / f"{arm_name}_s{seed}.json").read_text())
    mism = []
    for c_new, c_old in zip(rec["columns"], committed["columns"]):
        for k, v in c_old.items():
            if c_new.get(k) != v:
                mism.append((c_new["t"], k, v, c_new.get(k)))
    assert rec["grad_split"] == committed["grad_split"], "grad_split diverged"
    assert rec["occupancy"] == committed["occupancy"], "occupancy diverged"
    assert not mism, f"standing columns diverged: {mism[:5]} (+{len(mism)-5 if len(mism)>5 else 0})"
    print(f"REPLAY {arm_name}_s{seed}: standing columns BIT-IDENTICAL to committed "
          f"({len(rec['columns'])} windows) — RNG isolation proven end-to-end")
    return rec


def smoke():
    """Wiring asserts (SS1) on a short slow-ref run."""
    torch.manual_seed(0)
    pin = constants.PinnedConstants()
    cfg = SculptConfig(seed=0)
    loop = SlowRefLoop(cfg, pin)
    # loss-term structure unchanged: step() is the inherited Stage0Loop.step
    assert "step" not in SlowRefLoop.__dict__ and "step" not in A.EXP08Loop.__dict__
    assert not any(p.grad is not None for p in loop.vision_slow.parameters())
    for t in range(1, 1201):
        loop.step(no_word=False)
    d_on = SlowRefLoop._ref_param_dist(loop.vision_slow, loop.vision)
    d_birth = SlowRefLoop._ref_param_dist(loop.vision_slow, loop.vision_birth)
    assert d_on > 0.0, "no divergence from online after warm-up"
    assert d_birth > 0.0, "slow copy frozen at birth"
    assert all(p.grad is None for p in loop.vision_slow.parameters()), "grad reached the copy"
    cols = probes_for(False)(loop)
    need = {"evo_common", "evo_diff", "grad_common", "grad_diff", "ref_param_dist",
            "ref_birth_dist", "ref_target_dist", "ref_pairwise", "pairwise_emit"}
    assert need <= set(cols), f"missing columns: {need - set(cols)}"
    # the probes must leave training RNG untouched (also asserted inside each probe)
    st = loop.gen.get_state()
    probes_for(False)(loop)
    assert torch.equal(loop.gen.get_state(), st)
    print("SMOKE OK:", json.dumps({k: (round(v, 6) if isinstance(v, float) else v)
                                   for k, v in cols.items()}, indent=1))
    print(f"  d_online={d_on:.4g} d_birth={d_birth:.4g} (t=1200, tau={TAU})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--replay", choices=sorted(REPLAYS))
    ap.add_argument("--arm", choices=sorted(ARMS9))
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--steps", type=int, default=None)
    args = ap.parse_args()
    # DETERMINISM CONTRACT (measured 2026-07-03): seed + construction order + THREADS.
    # At 16 threads, parallel-reduction order perturbs floats ~1e-9 relative — visible
    # only in the ratio column's coarse quantization; at 1-2 threads the replay is
    # byte-identical to the committed artifacts (which came from the kick session's
    # thread-limited parallel phase). Pinned to 1 for every EXP09 run; recorded in rec.
    torch.set_num_threads(1)
    if args.smoke:
        smoke()
    elif args.replay:
        run_replay(args.replay)
    elif args.arm:
        run_exp09_arm(args.arm, args.seed, args.steps)


if __name__ == "__main__":
    main()
