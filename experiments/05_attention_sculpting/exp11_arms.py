"""EXP11 — the anchor-COVERAGE ladder (acquisition-aligned, both axes): does a wider
frozen reference keep routing input-sensitive?

Pre-registration: docs/EXP11_ANCHOR_DENSITY_PREREG.md (all §9 pins ratified 2026-07-04).
Sequence: build → pre-flight (per-rung acquisition onset + collapse period on cal seeds)
→ arms (verdict seeds, both the natural ladder and the matched-separation control) → one
review. Gate steps 5–6 BLOCKED; the ladder measures the lever, adoption = separate ruling.

Both axes acquisition-aligned (the EXP10 blocker fix): the verdict (routing survival) is
read over a MATCHED POST-ONSET WINDOW (W_post = 3 collapse periods in the rung's OWN
regime), never at a fixed absolute horizon — else denser-acquires-later manufactures
"survives better". Variable = COVERAGE (cardinality/coverage collinear in the nested
ladder; the coarse-first discriminator is parked). Verdict quantity = asg_dist
(input-sensitivity), NOT argmax_k count (the crutch screen). The matched-separation
control isolates coverage from the ~26% MIN-separation degradation (unit norm preserved).

Determinism: threads = 1, recorded.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import constants                                              # noqa: E402
import exp08_arms as A                                        # noqa: E402
import exp09_arms as X9                                       # noqa: E402
import exp10_arms as X10                                      # noqa: E402
from encoders import WordCortex                               # noqa: E402
from sculpt_config import SculptConfig                        # noqa: E402

OUTDIR = A.OUTDIR
EVAL = A.EVAL
RUNGS = [2, 4, 8, 16]
CAL_SEEDS = [20, 21]                    # distinct from verdict seeds (pin 1)
VERDICT_SEEDS = [0, 1, 2, 3, 4]         # >=5/rung
EXTENSION_SEEDS = [5, 6]               # the ONE +2 extension pool (pin 1)
FLOOR = X9.FLOOR
W_POST_PERIODS = 3                      # matched post-onset window (pin 3)
PREFLIGHT_CEILING = 130000             # long enough to catch v16 onset on cal seeds
MARGIN = 12000                         # horizon margin (pin 2)


# ------------------------------------------------------------------ matched-separation anchor
@torch.no_grad()
def _match_min_sep(wc: WordCortex, target: float) -> dict:
    """Rotate the CLOSEST anchor pair together in its plane until their separation =
    target, UNIT NORM PRESERVED (pin 4). Only acts if the natural min > target (sparse
    rungs); the densest rung is already at ~target. Minimal perturbation (one pair)."""
    w = wc.embed.weight
    n = w.shape[0]
    off = ~torch.eye(n, dtype=torch.bool)
    pair = torch.cdist(w, w)
    cur = float(pair[off].min())
    if cur <= target + 1e-6:
        return dict(acted=False, achieved_min=cur)
    flat = pair.clone(); flat[~off] = float("inf")
    i, j = [int(x) for x in divmod(int(flat.argmin()), n)]
    u, v = w[i].clone(), w[j].clone()
    # current half-angle; target half-angle from dist = 2 sin(theta/2)
    cos = float((u * v).sum().clamp(-1, 1))
    theta = torch.acos(torch.tensor(cos))
    theta_t = 2 * torch.asin(torch.tensor(target / 2).clamp(-1, 1))
    # rotate both toward the bisector by (theta - theta_t)/2 each
    mid = (u + v); mid = mid / mid.norm()
    for vec in (i, j):
        x = w[vec]
        # component along mid and perpendicular
        a = (x * mid).sum()
        perp = x - a * mid
        pn = perp.norm()
        if float(pn) < 1e-9:
            continue
        perp = perp / pn
        half = float(theta) / 2
        new_half = float(theta_t) / 2
        w[vec].copy_(torch.cos(torch.tensor(new_half)) * mid
                     + torch.sin(torch.tensor(new_half)) * perp)
    wc._w0.copy_(w)                                        # keep the frozen-snapshot invariant
    pair2 = torch.cdist(w, w)
    return dict(acted=True, achieved_min=float(pair2[off].min()),
                achieved_mean=float(pair2[off].mean()), pair=(i, j))


class MatchedSepVocabLoop(A.VocabLoop):
    """VocabLoop whose frozen anchor has its MIN separation matched to a common target
    (the control that isolates coverage from geometry degradation)."""

    _MATCH_TARGET = None                                   # set per-build (class attr injection)

    def _make_word(self):
        wc = super()._make_word()
        if self._MATCH_TARGET is not None:
            self._match_record = _match_min_sep(wc, self._MATCH_TARGET)
        return wc


def _natural_min_sep(vocab: int, seed: int) -> float:
    wc = WordCortex(16, vocab, seed=seed + 1)
    emb = wc.embed.weight.detach()
    off = ~torch.eye(emb.shape[0], dtype=torch.bool)
    return float(torch.cdist(emb, emb)[off].min())


def match_target() -> float:
    """Common target = the densest rung's mean natural MIN over the verdict seeds."""
    return statistics.mean(_natural_min_sep(16, s) for s in VERDICT_SEEDS)


# ------------------------------------------------------------------ per-rung run
def _arm_name(vocab: int, matched: bool) -> str:
    return f"cov{vocab}{'_ms' if matched else ''}"


def run_rung(vocab: int, seed: int, steps: int, matched: bool):
    name = _arm_name(vocab, matched)
    loop_cls = MatchedSepVocabLoop if matched else A.VocabLoop
    if matched:
        MatchedSepVocabLoop._MATCH_TARGET = match_target()
    A.ARMS[name] = dict(loop=loop_cls, vocab=vocab, no_word=False, steps=steps, seeds=[seed])
    rec = A.run_arm(name, seed, steps_override=steps, probes=X10.probes10(False))
    rec["acquisition_onset"] = X10.acquisition_onset(rec["columns"])
    rec["acquisition_aligned"] = X10.acquisition_aligned_read(rec["columns"],
                                                              rec["acquisition_onset"])
    rec["vocab"] = vocab
    rec["matched_sep"] = matched
    # anchor geometry (per-run, from the manifest's own construction)
    wc = WordCortex(16, vocab, seed=seed + 1)
    if matched:
        _match_min_sep(wc, MatchedSepVocabLoop._MATCH_TARGET)
    emb = wc.embed.weight.detach(); off = ~torch.eye(emb.shape[0], dtype=torch.bool)
    pair = torch.cdist(emb, emb)
    rec["anchor_min_sep"] = float(pair[off].min())
    rec["anchor_mean_sep"] = float(pair[off].mean())
    (OUTDIR / f"{name}_s{seed}.json").write_text(json.dumps(rec, indent=2))
    print(f"{name} s{seed}: onset={rec['acquisition_onset']} "
          f"min_sep={rec['anchor_min_sep']:.3f} "
          f"aligned={rec['acquisition_aligned']}")
    return rec


# ------------------------------------------------------------------ pre-flight (stage one)
def preflight():
    """Cal seeds → per-rung acquisition onset + collapse (den) period → horizon."""
    out = dict(target_min_sep=round(match_target(), 4), rungs={})
    for v in RUNGS:
        onsets, periods = [], []
        for s in CAL_SEEDS:
            rec = run_rung(v, s, PREFLIGHT_CEILING, matched=False)
            on = rec["acquisition_onset"]
            onsets.append(on)
            if on is not None:
                post = [c for c in rec["columns"] if c["t"] >= on]
                if len(post) >= 8:
                    p = X9.dynamics_panel([c["t"] for c in post],
                                          [c["den"] for c in post])["dominant_period_steps"]
                    periods.append(p or X9.PERIOD_WORD)
        acq = [o for o in onsets if o is not None]
        out["rungs"][str(v)] = dict(onsets=onsets, acquired=len(acq),
                                    max_onset=(max(acq) if acq else None),
                                    periods=periods,
                                    period=(max(periods) if periods else X9.PERIOD_WORD))
    feasible = [r for r in out["rungs"].values() if r["max_onset"] is not None]
    max_onset = max((r["max_onset"] for r in feasible), default=0)
    max_period = max((r["period"] for r in feasible), default=X9.PERIOD_WORD)
    out["max_onset"] = max_onset
    out["max_period"] = max_period
    out["horizon"] = int(max_onset + W_POST_PERIODS * max_period + MARGIN)
    (OUTDIR / "exp11_preflight.json").write_text(json.dumps(out, indent=2))
    print("\nPRE-FLIGHT:", json.dumps({k: out[k] for k in
          ("target_min_sep", "max_onset", "max_period", "horizon")}))
    for v in RUNGS:
        r = out["rungs"][str(v)]
        print(f"  v{v}: acquired {r['acquired']}/{len(CAL_SEEDS)} max_onset {r['max_onset']} "
              f"period {r['period']}")
    return out


# ------------------------------------------------------------------ verdict read (matched post-onset)
def verdict_read(rec, period):
    """asg_dist survival over [onset, onset + W_post periods] — the matched-collapse-phase
    read (pin 3). Returns None if unacquired or the window doesn't fit."""
    on = rec["acquisition_onset"]
    if on is None:
        return dict(status="ACQUISITION-CENSORED")
    hi = on + W_POST_PERIODS * period
    win = [c for c in rec["columns"] if on <= c["t"] <= hi]
    if not win or win[-1]["t"] < hi - EVAL:
        return dict(status="WINDOW-SHORT", have=len(win))
    asg = [c["asg_dist"] for c in win]
    k1 = sum(1 for c in win if c["asg_argmax_k"] == 1)
    return dict(status="READ", n=len(win), window=[on, hi],
                asg_mean=round(statistics.mean(asg), 4),
                asg_min=round(min(asg), 4),
                asg_frac_alive=round(sum(1 for a in asg if a > 0.1) / len(asg), 3),
                argmax_k_median=int(statistics.median(c["asg_argmax_k"] for c in win)),
                k1_frac=round(k1 / len(win), 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--run", nargs=3, metavar=("VOCAB", "SEED", "MATCHED"))
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(1)
    if args.smoke:
        tgt = match_target()
        print(f"match target (v16 mean natural min): {tgt:.4f}")
        for v in RUNGS:
            MatchedSepVocabLoop._MATCH_TARGET = tgt
            pin = constants.PinnedConstants()
            cfg = SculptConfig(seed=0)
            loop = MatchedSepVocabLoop(cfg, pin, v)
            assert loop.word.param_delta() == 0.0, "anchor plastic"
            emb = loop.word.embed.weight.detach(); off = ~torch.eye(emb.shape[0], dtype=torch.bool)
            mn = float(torch.cdist(emb, emb)[off].min())
            for _ in range(5):
                loop.step(no_word=False)
            print(f"  v{v}: matched min_sep {mn:.3f} (target {tgt:.3f}) "
                  f"nat {_natural_min_sep(v,0):.3f} | steps OK")
    elif args.preflight:
        preflight()
    elif args.run:
        run_rung(int(args.run[0]), int(args.run[1]), args.steps or PREFLIGHT_CEILING,
                 matched=(args.run[2] == "1"))


if __name__ == "__main__":
    main()
