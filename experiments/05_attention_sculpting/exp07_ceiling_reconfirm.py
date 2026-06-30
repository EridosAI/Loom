"""exp07 CEILING RECONFIRM (post-gate, pre-interior-read; pre-registered). The surface ceiling cells
(alpha>=0.9 on the off + reshaped columns) read SEED-UNSTABLE at 5 seeds / 12000 steps (std 0.47-0.55
-> likely bimodal: some seeds revive, some don't) and possibly UNDER-PLATEAUED (the off alpha=1.0 cell
climbed 0.78->1.04 over 6k-12k). Under the standing plateau-before-read rule and the user's directive,
this finishes them: extend to a longer budget with checkpoints (confirm TAIL-plateau) AND bump seeds
(seed-stable ceilings + uncertainty + per-seed distribution to expose bimodality), for the cells the
interior read hangs the floor/topology/legitimacy on.

PRE-REGISTERED (pinned before running):
  * SEEDS_HI = 10 (up from the surface's 5).
  * CHECKPOINTS = [12000, 15000, 18000]; PLATEAU = mean d_diff flat over the LAST TWO (|Δ|<=0.05).
    Not flat by 18000 -> flagged not-plateaued (read top, honest flag).
  * cells: the alive ceiling region (alpha in {0.9,1.0}) on off + reshaped@0.3 (pinned) + reshaped@0.1
    (the phasing recovery candidate) at member=16, the off/reshaped sharp refs, and the off/reshaped
    ceilings at member=2 (topology-invariance). Grouped for process-parallel running.
  * Ceiling C is read at the alpha=1.0 endpoint (maximal content-blind re-organization); alpha=0.9
    reported for the trace. Per-seed values reported (bimodality is a first-class observation).
"""

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
# ABSOLUTE-onset convention (PenaltySpec fixed): extending the budget = more post-clock differentiation
# from a FIXED 3600-step closed phase, so the plateau is well-defined. Read each cell at its tail-flat.
CHECKPOINTS = [12000, 18000, 24000, 30000]
PLATEAU_EPS = 0.05


def _pen(name, clock_fraction=None):
    r = dict(C.PENALTY_REGIMES[name])
    if clock_fraction is not None:
        r["t2_step"] = C.onset_step(clock_fraction)   # absolute λ2 onset (budget-independent)
    return PenaltySpec(name=name, **r)


# cell = (label, member, CueSpec, penalty-name, clock_fraction). clock_fraction sets the ABSOLUTE
# onset = onset_step(fraction) (= fraction*12000); budget-independent (PenaltySpec fixed).
def _cells(group):
    A = [  # member=16: off ceilings + sharp ref (no onset)
        ("16/off/repose@0.9", 16, CueSpec("repose", 0.9), "off", None),
        ("16/off/repose@1.0", 16, CueSpec("repose", 1.0), "off", None),
        ("16/off/sharp",      16, CueSpec("sharp", 0.0),  "off", None),
    ]
    B = [  # member=16: reshaped@0.3 (pinned, abs onset 3600) ceilings + sharp ref
        ("16/reshaped@0.3/repose@0.9", 16, CueSpec("repose", 0.9), "reshaped", 0.3),
        ("16/reshaped@0.3/repose@1.0", 16, CueSpec("repose", 1.0), "reshaped", 0.3),
        ("16/reshaped@0.3/sharp",      16, CueSpec("sharp", 0.0),  "reshaped", 0.3),
    ]
    Cc = [  # member=2: topology-invariance ceilings (off + reshaped@0.3) + sharp refs
        ("2/off/repose@0.9", 2, CueSpec("repose", 0.9), "off", None),
        ("2/off/repose@1.0", 2, CueSpec("repose", 1.0), "off", None),
        ("2/off/sharp",      2, CueSpec("sharp", 0.0),  "off", None),
        ("2/reshaped@0.3/repose@0.9", 2, CueSpec("repose", 0.9), "reshaped", 0.3),
        ("2/reshaped@0.3/repose@1.0", 2, CueSpec("repose", 1.0), "reshaped", 0.3),
        ("2/reshaped@0.3/sharp",      2, CueSpec("sharp", 0.0),  "reshaped", 0.3),
    ]
    # phasing-onset reconfirm (the armed phasing re-check; clean 10-seed/30000/abs-onset values for the
    # off-vs-reshaped recovery check). Labels MUST match the interior read's lookup key.
    P1 = [
        ("16/reshaped@0.1/repose@1.0", 16, CueSpec("repose", 1.0), "reshaped", 0.1),
        ("16/reshaped@0.5/repose@1.0", 16, CueSpec("repose", 1.0), "reshaped", 0.5),
    ]
    P2 = [
        ("16/reshaped@0.7/repose@1.0", 16, CueSpec("repose", 1.0), "reshaped", 0.7),
        ("16/reshaped@0.9/repose@1.0", 16, CueSpec("repose", 1.0), "reshaped", 0.9),
    ]
    return {"A": A, "B": B, "C": Cc, "P1": P1, "P2": P2}[group]


def _run_cell(member, cue, pen_name, clock_fraction):
    pen = _pen(pen_name, clock_fraction)
    per_seed = [cell_trajectory(member, cue, pen, s, CHECKPOINTS,
                                shared_mag=C.DIFFUSE_SHARED, cue_mag=C.DIFFUSE_CUE) for s in SEEDS_HI]
    out = {}
    for i, step in enumerate(CHECKPOINTS):
        dvals = [ps[i]["d_diff"] for ps in per_seed]
        avals = [ps[i]["d_ablated"] for ps in per_seed]
        out[step] = dict(d_mean=statistics.mean(dvals),
                         d_std=(statistics.stdev(dvals) if len(dvals) > 1 else 0.0),
                         d_sem=((statistics.stdev(dvals) / len(dvals) ** 0.5) if len(dvals) > 1 else 0.0),
                         d_min=min(dvals), d_max=max(dvals),
                         d_per_seed=[round(x, 4) for x in dvals],
                         ablated_max=max(avals))
    last2 = CHECKPOINTS[-2:]
    plateaued = abs(out[last2[1]]["d_mean"] - out[last2[0]]["d_mean"]) <= PLATEAU_EPS
    cval_step = CHECKPOINTS[-1]
    return dict(trajectory=out, plateaued=bool(plateaued), ceiling_step=cval_step,
                ceiling_mean=out[cval_step]["d_mean"], ceiling_std=out[cval_step]["d_std"],
                ceiling_sem=out[cval_step]["d_sem"], ceiling_per_seed=out[cval_step]["d_per_seed"],
                ablated_max=out[cval_step]["ablated_max"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", choices=["A", "B", "C", "P1", "P2"], required=True)
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))

    results = {}
    for label, member, cue, pen_name, cf in _cells(args.group):
        r = _run_cell(member, cue, pen_name, cf)
        results[label] = r
        print(f"{label:32s} C@{r['ceiling_step']}={r['ceiling_mean']:.3f}±{r['ceiling_std']:.2f} "
              f"(sem {r['ceiling_sem']:.3f}) plateaued={r['plateaued']} "
              f"per_seed={r['ceiling_per_seed']}")
    payload = dict(commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), group=args.group,
                   seeds_hi=len(SEEDS_HI), checkpoints=CHECKPOINTS, plateau_eps=PLATEAU_EPS,
                   cells=results)
    Path(_HERE / f"exp07_ceiling_{args.group}.json").write_text(json.dumps(payload, indent=2))
    print(f"\n(record -> exp07_ceiling_{args.group}.json)")


if __name__ == "__main__":
    main()
