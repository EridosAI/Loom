"""Extended-length confirmation at the prime clean-G candidate bands (interior: autonomous≈0,
oracle high). Tests whether the gap-3 lift (intact_B − noword_B) emerges with much MORE capacity
than the main sweep used — ruling out under-convergence as the reason the clean-G window was empty.
Matched intact + no-word arms, MODERATE clock, long runs, several seeds."""

from __future__ import annotations

import json
import statistics
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import constants                                  # noqa: E402
from loop import Stage0Loop                       # noqa: E402

HERE = Path(__file__).resolve().parent
LONG_STEPS = 48000          # ~3.4× the MODERATE sweep length
LONG_T = 52000
EVAL_EVERY = 1000
SEEDS = [0, 1, 2, 3]
calib = json.loads((HERE / "calibration.json").read_text())
ladder = json.loads((HERE / "band_ladder.json").read_text())
cells = {i: c for i, c in enumerate(ladder["admissible_cells"])}   # band_index = list position
TEST_BANDS = [7, 8]         # interior: autonomous≈0, oracle high (prime clean-G candidates)
ib = calib["intact_bar"]; nlo, nhi = calib["noword_floor_band"]

print(f"intact_bar={ib:.3f} noword_floor=[{nlo:.3f},{nhi:.3f}] | LONG_STEPS={LONG_STEPS}")
for bi in TEST_BANDS:
    cell = cells[bi]
    pin = constants.PinnedConstants()
    lifts, iBs, nBs, depths_end, cleanG_any = [], [], [], [], 0
    for seed in SEEDS:
        cfg = replace(constants.Stage0Config(), r_fine=cell["r_fine"], sigma_stim=cell["sigma_stim"],
                      seed=seed, steps=LONG_STEPS, T=LONG_T, eval_every=EVAL_EVERY)
        intact = Stage0Loop(cfg, pin); noword = Stage0Loop(cfg, pin)
        tail_i, tail_n, dtraj = [], [], []
        for i in range(cfg.steps):
            intact.step(no_word=False); noword.step(no_word=True)
            if i % cfg.eval_every == 0 or i == cfg.steps - 1:
                bi_ = intact.b_a_track(cfg.n_eval)["B_track"]
                bn_ = noword.b_a_track(cfg.n_eval)["B_track"]
                dtraj.append((i, intact.vision.pooling_depth))
                if i >= 0.8 * cfg.steps:
                    tail_i.append(bi_); tail_n.append(bn_)
                if bi_ >= ib and nlo <= bn_ <= nhi:
                    cleanG_any += 1
        mi, mn = statistics.mean(tail_i), statistics.mean(tail_n)
        iBs.append(mi); nBs.append(mn); lifts.append(mi - mn); depths_end.append(dtraj[-1][1])
    print(f"\n  band b{bi} r/σ={cell['r_over_sigma']:.2f} oracle={cell['oracle_substrate']:.2f}")
    print(f"    per-seed lift: {[round(x,3) for x in lifts]}")
    print(f"    intact_B(tail) mean={statistics.mean(iBs):.3f}  noword_B(tail) mean={statistics.mean(nBs):.3f}"
          f"  LIFT mean={statistics.mean(lifts):+.3f} (sd={statistics.pstdev(lifts):.3f})")
    print(f"    depth@end mean={statistics.mean(depths_end):.2f} (sweep MOD reached ~0.73)  "
          f"cleanG windows hit (any seed/win): {cleanG_any}")
    print(f"    -> intact clears bar {ib:.3f}? {statistics.mean(iBs) >= ib} ; "
          f"lift > 2*sd_noise(~0.03)? {statistics.mean(lifts) > 0.03}")
