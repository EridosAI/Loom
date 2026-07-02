"""EXP08 KICK PROBE — the self-absorption test (prereg + checkpoint amendments, pinned).

Is the collapsed assignment state ABSORBING or ESCAPABLE? Both measured end-states,
Δ2-only content-blind kicks, per-state clock-matched resumes, ε=0 null-resume controls,
and the t=0 null-kick guard (SURFACE-INVALID if the largest kick doesn't move routing).

States (deterministic replay via exp08_arms --save-state):
  word   = word_terminal seed 1 @112500 (asg_dist ~1e-5, the hard pin);  resume 24000 (5 den periods @4800)
  noword = marathon_ext seed 0 @500000 (asg_dist ~0.08, metastable);     resume 48000 (~2 periods @23100)

Grid: eps in {0 (CONTROL), 0.01, 0.03, 0.1, 0.3} x kick-seeds {0,1,2}. Kick = one-shot
zero-mean Gaussian on vision.pool.delta2 only, std = eps * RMS(delta2) — content-blind
(can re-seed input-SENSITIVITY, cannot implant the member map).

Verdicts (pre-registered, no rescue):
  SURFACE-INVALID — at eps=0.3, no kick seed moves asg_dist >=1.5x pre OR changes argmax_k
                    at t=0 -> stop; never ABSORBING.
  ABSORBING       — every eps rung decays back (final den-period asg_dist within the
                    control band; den back to the state's regime).
  ESCAPABLE       — some rung sustains regrow ABOVE the eps=0 control band through the
                    final den period (>=2/3 kick seeds); depth eps* recorded.
  MIXED-BY-STATE  — word ABSORBING while noword ESCAPABLE (the pin-depth lock confirmed).

The kick is a basin-geometry probe, NOT a candidate design (the counter-force drift door
stays bolted).
"""

from __future__ import annotations

import argparse
import glob
import json
import statistics
from pathlib import Path

import torch

import exp08_arms as A

_HERE = Path(__file__).resolve().parent
OUTDIR = _HERE / "exp08"
OUT = OUTDIR / "kick_probe.json"

STATES = {
    "word":   dict(arm="word_terminal", seed=1, resume=24000, period=4800),
    "noword": dict(arm="marathon_ext", seed=0, resume=48000, period=23100),
}
EPS_LADDER = [0.0, 0.01, 0.03, 0.1, 0.3]         # 0.0 = the null-resume CONTROL rung
KICK_SEEDS = [0, 1, 2]
EVAL = 300
T0_MOVE_FACTOR = 1.5                              # the pinned "measurably move" bar


def _members(loop):
    cfg = loop.cfg
    a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    return a, b, loop._word_label(b, a)


@torch.no_grad()
def read_state(loop) -> dict:
    ma, mb, labels = _members(loop)
    raw_c = loop.stim.raw_clean(ma, mb)
    p = loop.vision.pool.assign(raw_c)
    off = ~torch.eye(p.shape[0], dtype=torch.bool)
    from revival import partition_read
    e = loop.evoke_vision(ma, mb, associative=True)
    content = loop.vision.emit(raw_c)
    r = partition_read(e, labels, content)
    return dict(asg_dist=float(torch.cdist(p, p, p=1)[off].mean()),
                asg_argmax_k=int(len(set(p.argmax(1).tolist()))),
                den=r["content_denom"], num=r["cross_dist_raw"])


def kick(loop, eps: float, kseed: int):
    if eps <= 0:
        return 0.0
    with torch.no_grad():
        d2 = loop.vision.pool.delta2
        g = torch.Generator().manual_seed(9000 + kseed)
        std = eps * float(d2.pow(2).mean().sqrt())
        d2.add_(std * torch.randn(d2.shape, generator=g))
    return std


def run_resume(state: str, eps: float, kseed: int) -> dict:
    S = STATES[state]
    loop, spec, cfg = A.build_loop(S["arm"], S["seed"])
    A.load_state(loop, OUTDIR / f"state_{S['arm']}_s{S['seed']}.pt")
    no_word = spec.get("no_word", False)
    pre = read_state(loop)
    std = kick(loop, eps, kseed)
    t0 = read_state(loop)                          # post-kick, PRE-resume (the guard read)
    cols = []
    for i in range(1, S["resume"] + 1):
        loop.step(no_word=no_word)
        if i % EVAL == 0:
            cols.append(dict(i=i, **read_state(loop)))
    rec = dict(state=state, eps=eps, kseed=kseed, kick_std=std, resume=S["resume"],
               period=S["period"], pre=pre, t0=t0,
               cols=[{k: (round(v, 6) if isinstance(v, float) else v) for k, v in c.items()}
                     for c in cols])
    (OUTDIR / f"kick_{state}_e{eps}_k{kseed}.json").write_text(json.dumps(rec, indent=2))
    print(f"kick {state} eps={eps} k={kseed}: pre asg={pre['asg_dist']:.3g} t0 asg={t0['asg_dist']:.3g} "
          f"final asg={cols[-1]['asg_dist']:.3g} final den={cols[-1]['den']:.3g}")
    return rec


def _final_period_stats(rec):
    n = rec["period"] // EVAL
    tail = rec["cols"][-n:]
    return dict(asg=statistics.mean(c["asg_dist"] for c in tail),
                den=statistics.mean(c["den"] for c in tail),
                den_max=max(c["den"] for c in tail))


def verdict():
    shards = {}
    for p in sorted(glob.glob(str(OUTDIR / "kick_*_e*_k*.json"))):
        r = json.loads(Path(p).read_text())
        shards[(r["state"], r["eps"], r["kseed"])] = r
    out = dict(eps_ladder=EPS_LADDER, kick_seeds=KICK_SEEDS, t0_move_factor=T0_MOVE_FACTOR)
    states_verdicts = {}
    for state in STATES:
        # 1. the t=0 null-kick guard at the largest eps
        big = [shards[(state, EPS_LADDER[-1], k)] for k in KICK_SEEDS]
        moved = [(r["t0"]["asg_dist"] >= T0_MOVE_FACTOR * max(r["pre"]["asg_dist"], 1e-12))
                 or (r["t0"]["asg_argmax_k"] != r["pre"]["asg_argmax_k"]) for r in big]
        if not any(moved):
            states_verdicts[state] = dict(verdict="SURFACE_INVALID",
                                          t0_moved=moved, note="largest kick never touched routing")
            continue
        # 2. the eps=0 control band (final-period stats over 3 unkicked resumes)
        ctrl = [_final_period_stats(shards[(state, 0.0, k)]) for k in KICK_SEEDS]
        band = dict(asg_max=max(c["asg"] for c in ctrl), den_max=max(c["den"] for c in ctrl),
                    denmax_max=max(c["den_max"] for c in ctrl))
        # 3. per-rung escape: >=2/3 kick seeds sustain final-period regrow ABOVE the control band
        rungs = {}
        eps_star = None
        for eps in EPS_LADDER[1:]:
            fins = [_final_period_stats(shards[(state, eps, k)]) for k in KICK_SEEDS]
            esc = [f["asg"] > band["asg_max"] and f["den"] > band["den_max"] for f in fins]
            rungs[str(eps)] = dict(final=fins, escaped=esc, rung_escapable=sum(esc) >= 2)
            if sum(esc) >= 2 and eps_star is None:
                eps_star = eps
        v = "ESCAPABLE" if eps_star is not None else "ABSORBING"
        states_verdicts[state] = dict(verdict=v, eps_star=eps_star, t0_moved=moved,
                                      control_band=band, rungs=rungs)
    out["states"] = states_verdicts
    vs = {s: states_verdicts[s]["verdict"] for s in states_verdicts}
    out["combined"] = ("SURFACE_INVALID" if "SURFACE_INVALID" in vs.values() else
                       "MIXED_BY_STATE" if vs.get("word") == "ABSORBING" and vs.get("noword") == "ESCAPABLE"
                       else f"word={vs.get('word')} noword={vs.get('noword')}")
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps({s: {k: v for k, v in sv.items() if k in ('verdict', 'eps_star')}
                      for s, sv in states_verdicts.items()}, indent=1))
    print("COMBINED:", out["combined"])
    print(f"-> {OUT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", nargs=3, metavar=("STATE", "EPS", "KSEED"), default=None)
    ap.add_argument("--verdict", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))
    if args.verdict:
        verdict()
    elif args.resume:
        run_resume(args.resume[0], float(args.resume[1]), int(args.resume[2]))


if __name__ == "__main__":
    main()
