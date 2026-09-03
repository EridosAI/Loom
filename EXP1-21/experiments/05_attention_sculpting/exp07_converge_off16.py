"""exp07 CONVERGE off@card-16 (and reshaped@card-16, for an equal-training paired comparison) to 36000.
The +0.108 card-16 ceiling gap was a LOWER BOUND: off/repose@1.0 was still creeping at 30000 (reshaped
flat). This converges both ceiling cells at the SAME 36000 budget so the gap is a real converged number,
not a lower bound. Absolute onset (900/3600) unchanged -> extending the budget only lengthens the
post-maturation tail. Writes exp07_ceiling_conv_{cell}.json (same keys as the reconfirm; interior read
prefers these). Direction won't change (off creeps UP while reshaped is flat -> gap can only grow)."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import torch

import exp07_config as C
from exp07_core import CueSpec, PenaltySpec, cell_trajectory

_HERE = Path(__file__).resolve().parent
SEEDS_HI = list(range(10))
CHECKPOINTS = [30000, 33000, 36000]
PLATEAU_EPS = 0.05


def _pen(name, clock_fraction=None):
    r = dict(C.PENALTY_REGIMES[name])
    if clock_fraction is not None:
        r["t2_step"] = C.onset_step(clock_fraction)
    return PenaltySpec(name=name, **r)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cell", choices=["off", "reshaped"], required=True)
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))

    if args.cell == "off":
        label, pen = "16/off/repose@1.0", _pen("off")
    else:
        label, pen = "16/reshaped@0.3/repose@1.0", _pen("reshaped", 0.3)
    cue = CueSpec("repose", 1.0)

    per_seed = [cell_trajectory(16, cue, pen, s, CHECKPOINTS,
                                shared_mag=C.DIFFUSE_SHARED, cue_mag=C.DIFFUSE_CUE) for s in SEEDS_HI]
    traj = {}
    for i, step in enumerate(CHECKPOINTS):
        dv = [ps[i]["d_diff"] for ps in per_seed]; av = [ps[i]["d_ablated"] for ps in per_seed]
        traj[step] = dict(d_mean=statistics.mean(dv),
                          d_std=(statistics.stdev(dv) if len(dv) > 1 else 0.0),
                          d_sem=((statistics.stdev(dv) / len(dv) ** 0.5) if len(dv) > 1 else 0.0),
                          d_per_seed=[round(x, 4) for x in dv], ablated_max=max(av))
    plateaued = abs(traj[36000]["d_mean"] - traj[33000]["d_mean"]) <= PLATEAU_EPS
    s = 36000
    rec = dict(trajectory={str(k): v for k, v in traj.items()}, plateaued=bool(plateaued),
               ceiling_step=s, ceiling_mean=traj[s]["d_mean"], ceiling_std=traj[s]["d_std"],
               ceiling_sem=traj[s]["d_sem"], ceiling_per_seed=traj[s]["d_per_seed"],
               ablated_max=traj[s]["ablated_max"])
    Path(_HERE / f"exp07_ceiling_conv_{args.cell}.json").write_text(json.dumps(
        dict(commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), seeds_hi=len(SEEDS_HI),
             checkpoints=CHECKPOINTS, cells={label: rec}), indent=2))
    print(f"{label}: " + "  ".join(f"{k}:{traj[k]['d_mean']:.3f}" for k in CHECKPOINTS)
          + f"  C@36000={rec['ceiling_mean']:.4f}±{rec['ceiling_std']:.2f} plateaued={rec['plateaued']}")
    print(f"per_seed={rec['ceiling_per_seed']}")


if __name__ == "__main__":
    main()
