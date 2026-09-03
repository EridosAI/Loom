"""exp19_g5b.py — G5b MATCHED-N POWER, re-specified as a PHANTOM-FLOOR measurement (Jason, 2026-07-14).

THE RE-SPECIFIED QUESTION (not "does a converter certify at 7,915?"):
    what is the PHANTOM FLOOR at 7,915, and does the converter SIGNAL still clear it?
The floor RISES as the stratum thins: sparser windows (fewer in-stratum onsets/window) -> granular accuracy
-> longer chance runs. At full N=14,156 the phantom floor tops at 6 (non-converters) and the nearest
converter is 12. At the treatment's density (B=512, N=7,915) the floor may reach 12 and swallow s6. This is
the underpower risk at the rho<=0.05 anchor, MEASURABLE before anything trains.

METHOD (house discipline, ledger 18 / ledger 38 — floor audit, never a raw-count / alpha bar):
  * AMONG-KEPT uniform thinning of each seed's OWN zero-preceding stratum to the treatment's density
    (ratio r = 7915/14156 of the post-acq stratum), K draws, pinned SUBSAMPLE_SEED. Faithful to the
    treatment: same [0,500k) window grid, sparser stratum; thinning cannot MERGE runs (onsets never move
    windows), it can only coarsen per-window means -> the floor it raises is real granularity, not an artifact.
  * PHANTOM FLOOR at 7,915 = the run-length distribution of the NON-converters {1,3,7} under thinning (they
    carry the regime's granularity AND autocorrelation). Ceiling = its upper tail.
  * SIGNAL at 7,915 = the run-length distribution of the converters {0,2,4,5,6} under thinning (shrinks as
    episodes lose onsets). s6 (12 at full N) is the marginal converter.
  * The finding is the SEPARATION (or overlap): does the converter signal sit above the risen floor, or is
    it swallowed? Reported as distributions + a paired per-draw excess, NOT a >=90%/<=1% binary (retired).

  --run   measure the phantom floor + signal at N_TARGET and report the separation
"""
from __future__ import annotations

import json
import statistics
import sys

import torch

import exp14_arms as XA
import exp19_floor as FL

VERDICT_SEEDS = FL.VERDICT_SEEDS
CONVERTERS = FL.CONVERTERS
NONCONVERTERS = FL.NONCONVERTERS
FLOOR_BAND = FL.FLOOR_BAND
CACHE = FL.CACHE

N_FULL = 14156            # control full zero-preceding stratum (preflight B=T, read [0,500k))
N_TARGET = 7915           # treatment B=512 stratum (prereg; the rho<=0.05 anchor, worst per-seed seed 4)
R_THIN = N_TARGET / N_FULL  # density-matched among-kept thinning ratio (0.5591)
SUBSAMPLE_SEED = 719_150   # pinned
K_DRAWS = 2000


def _q(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    i = min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))
    return xs[i]


def _subsample_run(strat_onsets, keep, post_acq_windows, gen) -> int:
    """Among-kept uniform thinning: keep `keep` of the in-stratum onsets (random, no replacement), re-bin to
    the post-acq window grid (per-window mean; empty windows break runs), return longest run >= FLOOR_BAND."""
    n = len(strat_onsets)
    idx = torch.randperm(n, generator=gen)[:keep].tolist()
    win: dict = {}
    for i in idx:
        t, acc = strat_onsets[i]
        win.setdefault(t, []).append(acc)
    best = cur = 0
    for t in post_acq_windows:
        a = win.get(t)
        cur = cur + 1 if (a and statistics.mean(a) >= FLOOR_BAND) else 0
        best = max(best, cur)
    return best


def run() -> dict:
    data = json.loads(CACHE.read_text())
    gen = torch.Generator().manual_seed(SUBSAMPLE_SEED)
    runs = {s: [] for s in VERDICT_SEEDS}
    keeps = {}
    # draw-major so the pinned generator advances identically regardless of seed order
    seq = []
    for s in VERDICT_SEEDS:
        d = data[str(s)]
        keeps[s] = round(R_THIN * len(d["strat_onsets"]))
    for k in range(K_DRAWS):
        for s in VERDICT_SEEDS:
            d = data[str(s)]
            runs[s].append(_subsample_run(d["strat_onsets"], keeps[s], d["post_acq_windows"], gen))

    # PHANTOM FLOOR at 7,915 = non-converters pooled
    floor_pool = [r for s in NONCONVERTERS for r in runs[s]]
    floor = dict(median=_q(floor_pool, 0.5), q90=_q(floor_pool, 0.90), q99=_q(floor_pool, 0.99),
                 max=max(floor_pool),
                 per_seed={s: dict(median=_q(runs[s], 0.5), q99=_q(runs[s], 0.99), max=max(runs[s]))
                           for s in NONCONVERTERS})
    floor_ceiling = floor["q99"]        # the phantom bracket upper edge (q99 of the granularity floor)

    # SIGNAL at 7,915 = converters; paired per-draw excess over that draw's floor ceiling (max non-conv run)
    per_draw_floor_max = [max(runs[s][k] for s in NONCONVERTERS) for k in range(K_DRAWS)]
    conv = {}
    for s in CONVERTERS:
        rs = runs[s]
        clears_bracket = sum(1 for r in rs if r > floor_ceiling) / K_DRAWS
        clears_paired = sum(1 for k in range(K_DRAWS) if rs[k] > per_draw_floor_max[k]) / K_DRAWS
        conv[s] = dict(median=_q(rs, 0.5), q10=_q(rs, 0.10), min=min(rs),
                       full_N_run=FL._longest_run(  # the full-N run, for the shrink picture
                           FL._series_from_win(data[str(s)]["win_accs"], data[str(s)]["post_acq_windows"])),
                       frac_clears_q99_bracket=round(clears_bracket, 4),
                       frac_exceeds_perdraw_floor_max=round(clears_paired, 4))

    # separation verdict — floor-audit form, NOT a fixed % bar
    nearest = min(CONVERTERS, key=lambda s: conv[s]["median"])
    swallowed = [s for s in CONVERTERS if conv[s]["q10"] <= floor_ceiling]   # lower tail inside the bracket
    clean = [s for s in CONVERTERS if conv[s]["min"] > floor["max"]]         # never overlaps even the floor max
    out = dict(
        gate="G5b — PHANTOM FLOOR at N=7,915 (does the converter signal still clear it?)",
        method=f"among-kept thinning to density r={round(R_THIN,4)} (N_target={N_TARGET}/N_full={N_FULL}), "
               f"K={K_DRAWS} draws, SUBSAMPLE_SEED={SUBSAMPLE_SEED}",
        floor_band=FLOOR_BAND, keeps_per_seed=keeps,
        phantom_floor_7915=floor, floor_ceiling_q99=floor_ceiling,
        converter_signal_7915=conv, marginal_converter=nearest,
        swallowed_converters=swallowed, cleanly_separated_converters=clean,
        floor_at_full_N=dict(nonconverter_runs={s: FL._longest_run(
            FL._series_from_win(data[str(s)]["win_accs"], data[str(s)]["post_acq_windows"]))
            for s in NONCONVERTERS}),
        VERDICT=("SIGNAL CLEARS — every converter's run distribution sits above the risen phantom floor "
                 f"(q99 ceiling {floor_ceiling}); none swallowed" if not swallowed else
                 f"STRATUM-UNDERPOWER at rho<=0.05 (B=512): converter(s) {swallowed} fall INSIDE the phantom "
                 f"floor bracket [0,{floor_ceiling}] at N=7,915 (their lower tail overlaps the granularity "
                 "floor) — the signal is swallowed by thinning. HALT -> Jason."),
        underpowered=bool(swallowed), ok=True)
    (XA.OUTDIR / "exp19_g5b_phantom_floor.json").write_text(json.dumps(out, indent=2))
    return out


def _print(o):
    print("\n===== G5b — PHANTOM FLOOR at N=7,915 =====")
    print(f"  method: {o['method']}")
    fl = o["phantom_floor_7915"]
    print(f"  PHANTOM FLOOR (non-converters pooled): median={fl['median']} q90={fl['q90']} "
          f"q99={fl['q99']} max={fl['max']}   [full-N floor: {o['floor_at_full_N']['nonconverter_runs']}]")
    print(f"  {'conv':>4} {'full_N':>7} {'median':>7} {'q10':>5} {'min':>5} {'>q99_ceil':>10} {'>perdraw_floor':>15}")
    for s in CONVERTERS:
        c = o["converter_signal_7915"][s]
        print(f"  {s:>4} {c['full_N_run']:>7} {c['median']:>7} {c['q10']:>5} {c['min']:>5} "
              f"{c['frac_clears_q99_bracket']:>10} {c['frac_exceeds_perdraw_floor_max']:>15}")
    print(f"\n  marginal converter: s{o['marginal_converter']}   swallowed: {o['swallowed_converters']}   "
          f"cleanly separated: {o['cleanly_separated_converters']}")
    print(f"\n  VERDICT: {o['VERDICT']}\n")


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--run" in sys.argv:
        _print(run())
    else:
        print("usage: --run")
