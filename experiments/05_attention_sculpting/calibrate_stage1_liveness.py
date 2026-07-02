"""§L deployed-loop liveness — CALIBRATION (STAGE1 rig spec §L; pinned gate sequence step 1).

Runs the NEUTRAL (d)-gate at the rig's EXACT revival config to produce the
`healthy-reference-at-config`, and emits `liveness_calibration.json` for REVIEW GATE 1.

SCOPE (gate step 1 ONLY): this does NOT run the deployed SculptLoop, NOT Step-0 (a)/(b)/(c),
NOT the entry read / window count k, and NOT read/interpret any interior surface. It only
re-measures the neutral (d)-gate reference at >=20 seeds and computes the pinned membership bar.

ONE CODE PATH (reuse-only): the operator training + measurement is exp07_core.cell_trajectory
verbatim (which itself reuses dgate.make_op/_task_tensors/_companion/_sep). No reimplementation.

THE RIG CELL (all knobs [RECONCILE]'d from exp07_config, base commit ac7ea57):
  * member cardinality  = C.M_DEPLOYED (16)
  * completion cue      = CueSpec("repose", 1.0)  -- content-blind GLOBAL mean-centre
                          (comp - 1.0*mu; the validated common-mode remover). NOT flat/0.0
                          (that is the collapsed/un-reorganized deployed BASELINE = the disease).
  * PAM prototype tie   = PenaltySpec("reshaped", **PENALTY_REGIMES["reshaped"])
                          -- preserve-style two-clock StepSchedule, ABSOLUTE onsets 900/3600.
  * shared_mag / cue_mag = C.DIFFUSE_SHARED (5.831) / C.DIFFUSE_CUE (0.5)
This is EXACTLY the exp07 converge cell "16/reshaped@0.3/repose@1.0" (exp07_converge_off16.py),
so seeds 0..9 reproduce that run's per-seed d_diff bit-for-bit (a built-in correctness check).

READ BUDGET = 36000 (converged), NOT 12000. reshaped/repose@1.0 is a SLOW-REVIVER: at the
12000 plateau_budget it is still BIMODAL (surface: per_seed [0.182,1.118,0.011,0.992,1.177],
2 seeds not yet revived). Only by ~30000 does it plateau (converge: 1.0234 +/- 0.0793, all
seeds alive, plateaued=True). The healthy-reference-at-config is the MATURE ceiling, so we read
at the converged budget with the converge's [30000,33000,36000] plateau spot-check. Reading at
12000 would measure the half-revived regime and yield a meaningless (negative) bar.

MARGIN RULE (pinned pre-run, STAGE1 §L): bar = reference - 2*(per-seed std).
  reference = mean over per-seed d_diff at the read budget
  spread    = statistics.stdev(per_seed_d)   # sample (n-1) PER-SEED std, NOT SEM
  margin    = 2*spread ;  bar = reference - margin
Per-seed std (not SEM) because the entry gate is a MEMBERSHIP test (does one deployed read
belong to the healthy-at-config family), not a mean-clears-threshold test; SEM would shrink
with seed count -> stricter gate the better the reference is measured (backwards).

Orchestration only (in-scope: "compute buys seed-count"): --smoke for a fast end-to-end check;
--shard-index/--shard-count for process-parallel seeds; --merge to fold shards into the final
artifact + bar. The rig cell and read budget come solely from exp07_config / this file's pins.
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
OUT = _HERE / "liveness_calibration.json"

# --- pinned rig cell (single source of truth = exp07_config; only the read schedule + seed floor
#     are local pins, matching the exp07 converge precedent for this exact cell) ---
CUE = CueSpec("repose", 1.0)                                       # global mean-centre (alpha=1.0)
PEN = PenaltySpec(name="reshaped", **dict(C.PENALTY_REGIMES["reshaped"]))  # two-clock, abs 900/3600
ANCHORS = [30000, 33000, 36000]                                   # coarse plateau anchors (converge x-check)
WINDOW_STEP = 100                                                  # deployed eval cadence (Stage0Config.eval_every)
PLATEAU_ONSET = 30000                                             # converge-confirmed plateau onset
READ_STEP = 36000                                                  # reference read budget (bar from single window @36000)
# fine eval-cadence grid over the plateau, used ONLY to pin k in true deployed-read units:
CHECKPOINTS = sorted(set(list(range(PLATEAU_ONSET, READ_STEP + 1, WINDOW_STEP)) + ANCHORS))
PLATEAU_EPS = 0.05                                                 # matches exp07 converge
SEED_FLOOR = 20                                                    # STAGE1 §L frequency floor (>=20)

# the exp07 converge (10-seed) per-seed d_diff @36000 for this exact cell — seeds 0..9 must match
CONVERGE_SEED0_9 = [1.0147, 1.0366, 0.9218, 1.0162, 1.0743, 1.0553, 1.0517, 1.1427, 1.059, 0.8619]


def _config_dict() -> dict:
    """Full knob set + provenance, serialized into the artifact (audit at REVIEW GATE 1)."""
    return dict(
        reconcile_base_commit="ac7ea57",
        member_count=C.M_DEPLOYED,                                 # 16   [RECONCILE]
        cue_seg=CUE.seg, cue_alpha=CUE.alpha,                      # repose / 1.0  [rig: global mean-centre]
        penalty_name=PEN.name,                                     # reshaped (preserve tie)
        penalty=dict(C.PENALTY_REGIMES["reshaped"]),              # {lam1_hi:10,lam1_lo:0,t1:900,lam2_hi:10,lam2_lo:0,t2:3600}
        onset_is_absolute=C.KNOBS["onset_is_absolute"],           # True
        t1_step_abs=C.RESHAPED_T1_STEP, t2_step_abs=C.RESHAPED_T2_STEP,   # 900 / 3600
        reshaped_t1_fraction=round(C.RESHAPED_T1_FRACTION, 4),     # 0.075
        reshaped_clock_fraction=round(C.RESHAPED_CLOCK_FRACTION, 4),  # 0.30
        reshaped_lam_hi=C.CORTEX_LAM_HI, reshaped_lam_lo=C.CORTEX_LAM_LO,  # 10 / 0
        shared_mag=C.DIFFUSE_SHARED, cue_mag=C.DIFFUSE_CUE,        # 5.831 / 0.5  [RECONCILE]
        diffuse_snr=round(C.DIFFUSE_SNR, 4),                       # 0.0857
        read_step=READ_STEP, anchors=list(ANCHORS),              # 36000 converged; 30k/33k/36k anchors
        window_step=WINDOW_STEP, plateau_onset=PLATEAU_ONSET,     # deployed eval cadence; k-pin plateau start
        n_fine_windows=len(CHECKPOINTS),                         # eval-cadence grid size for k-pin
        canonical_budget=C.CANONICAL_BUDGET,                      # 12000 (onset pin ref; NOT the read budget)
        plateau_eps=PLATEAU_EPS,
        seed_streams=dict(op_init="seed*131+3", task="seed*101+17", train_rng="seed*911+7"),
        # anchors carried for reviewer CONTEXT ONLY — this run re-measures the reference; NOT the bar:
        anchor_reshaped_converge_10seed=1.0234,                    # exp07 conv_reshaped @36000 (context)
        anchor_off_sharp_ref=C.OFF_SHARP_REF,                     # 1.1064 (context)
        anchor_healthy_clean2=C.HEALTHY,                          # 1.4122 (context; superseded per §L)
        anchor_live_bar_exp06=C.LIVE_BAR,                         # 0.8672 (SUPERSEDED canon bar; context)
    )


def _run_seeds(seeds: list[int]) -> list[dict]:
    """Per seed: fresh op inside cell_trajectory (make_op(seed) + fresh task tensors -> no leak).
    Returns one record per seed: {seed, d_diff@each ckpt, d_ablated@each ckpt}."""
    recs = []
    for s in seeds:
        traj = cell_trajectory(C.M_DEPLOYED, CUE, PEN, s, CHECKPOINTS,
                               shared_mag=C.DIFFUSE_SHARED, cue_mag=C.DIFFUSE_CUE)
        by_step = {t["step"]: t for t in traj}
        recs.append(dict(
            seed=s,
            d_diff={str(k): round(by_step[k]["d_diff"], 6) for k in CHECKPOINTS},
            d_ablated={str(k): round(by_step[k]["d_ablated"], 6) for k in CHECKPOINTS},
        ))
    return recs


def _kpin(recs: list[dict], bar: float) -> dict:
    """Pin k = #eval-windows the entry read must average, in TRUE deployed-read units (WINDOW_STEP),
    measured over the converge-confirmed plateau [PLATEAU_ONSET, READ_STEP]. Amendment 2: single
    windows dip below the -2sigma bar (that is what -2sigma means); the k-window mean must clear it.
    Reports two criteria + the binding seed; k is pinned on the CONSERVATIVE sliding one (the entry
    read may land anywhere in the plateau) when achievable, else on the full-plateau-mean fallback."""
    steps = CHECKPOINTS
    n = len(steps)
    fine = {r["seed"]: [r["d_diff"][str(s)] for s in steps] for r in recs}
    plateau_mean = {s: statistics.mean(v) for s, v in fine.items()}       # each seed's true value (large-k limit)
    binding = min(plateau_mean, key=plateau_mean.get)                     # lowest = the -2sigma-tail seed
    firstk_min = lambda k: min(statistics.mean(v[:k]) for v in fine.values())          # first k from onset
    sliding_min = lambda k: min(min(statistics.mean(v[i:i + k]) for i in range(0, n - k + 1))
                                for v in fine.values())                                # worst position, all seeds
    k_first = next((k for k in range(1, n + 1) if firstk_min(k) >= bar), None)
    k_slide = next((k for k in range(1, n + 1) if sliding_min(k) >= bar), None)
    pinned = k_slide if k_slide is not None else k_first
    return dict(
        window_step=WINDOW_STEP, plateau_span=[PLATEAU_ONSET, READ_STEP], n_windows=n,
        k_pinned=pinned, k_pinned_span_steps=(pinned * WINDOW_STEP if pinned else None),
        k_pinned_criterion=("sliding-worst-position" if k_slide is not None else "first-k-from-onset"),
        k_firstk=k_first, k_sliding=k_slide,
        single_window_min=round(min(min(v) for v in fine.values()), 4),
        plateau_mean_min=round(min(plateau_mean.values()), 4),
        binding_seed=binding, binding_seed_plateau_mean=round(plateau_mean[binding], 4),
    )


def _aggregate(recs: list[dict]) -> dict:
    """Compute the pinned bar + coarse-anchor trajectory + eval-cadence k-pin from per-seed records."""
    recs = sorted(recs, key=lambda r: r["seed"])
    seeds = [r["seed"] for r in recs]
    traj = {}
    for k in ANCHORS:
        dv = [r["d_diff"][str(k)] for r in recs]
        av = [r["d_ablated"][str(k)] for r in recs]
        traj[str(k)] = dict(
            d_mean=round(statistics.mean(dv), 6),
            d_std=round(statistics.stdev(dv) if len(dv) > 1 else 0.0, 6),
            d_min=round(min(dv), 6), d_max=round(max(dv), 6),
            ablated_max=round(max(av), 6),
        )
    per_seed_d = [r["d_diff"][str(READ_STEP)] for r in recs]
    reference = statistics.mean(per_seed_d)
    spread = statistics.stdev(per_seed_d) if len(per_seed_d) > 1 else 0.0   # per-seed sample std
    margin = 2.0 * spread
    bar = reference - margin
    plateaued = abs(traj[str(READ_STEP)]["d_mean"] - traj[str(ANCHORS[-2])]["d_mean"]) <= PLATEAU_EPS
    # per-seed coarse-anchor trajectory (auditable plateau, not only the mean)
    per_seed_trajectory = {str(r["seed"]): {str(k): r["d_diff"][str(k)] for k in ANCHORS}
                           for r in recs}
    per_seed_swing = {str(r["seed"]): round(abs(r["d_diff"][str(READ_STEP)]
                                               - r["d_diff"][str(ANCHORS[-2])]), 6) for r in recs}
    per_seed_plateaued = sum(1 for v in per_seed_swing.values() if v <= PLATEAU_EPS)
    per_seed_min = round(min(per_seed_d), 6)   # lowest seed at read step: all alive if >> collapse floor
    kpin = _kpin(recs, bar)
    # correctness cross-check: seeds 0..9 must match the exp07 converge per-seed values
    xcheck = None
    d_by_seed = {r["seed"]: r["d_diff"][str(READ_STEP)] for r in recs}
    if all(s in d_by_seed for s in range(10)):
        mine = [round(d_by_seed[s], 4) for s in range(10)]
        max_abs = max(abs(a - b) for a, b in zip(mine, CONVERGE_SEED0_9))
        xcheck = dict(seeds0_9_mine=mine, seeds0_9_converge=CONVERGE_SEED0_9,
                      max_abs_dev=round(max_abs, 4), matches=max_abs <= 0.001)
    return dict(
        reference=round(reference, 4), spread=round(spread, 4),
        margin=round(margin, 4), bar=round(bar, 4),
        per_seed_d=[round(x, 4) for x in per_seed_d],
        seed_count=len(recs), seeds=seeds,
        read_step=READ_STEP, plateaued=bool(plateaued),
        per_seed_plateaued=per_seed_plateaued, per_seed_swing_max=max(per_seed_swing.values()),
        per_seed_min=per_seed_min, k_pin=kpin,
        ablated_max=traj[str(READ_STEP)]["ablated_max"],
        trajectory=traj, per_seed_trajectory=per_seed_trajectory, converge_xcheck=xcheck,
    )


def _write_final(recs: list[dict]):
    agg = _aggregate(recs)
    payload = dict(commit_hash=C.commit_hash(), spec_hash=C.spec_hash(),
                   config=_config_dict(), **agg)
    OUT.write_text(json.dumps(payload, indent=2))
    x = agg["converge_xcheck"]
    print(f"reference={agg['reference']:.4f}  spread={agg['spread']:.4f}  margin={agg['margin']:.4f}  "
          f"bar={agg['bar']:.4f}  n={agg['seed_count']}  plateaued={agg['plateaued']}  "
          f"per_seed_plateaued={agg['per_seed_plateaued']}/{agg['seed_count']}  "
          f"per_seed_min={agg['per_seed_min']:.4f}  swing_max={agg['per_seed_swing_max']:.4g}  "
          f"ablated_max={agg['ablated_max']:.4g}")
    kp = agg["k_pin"]
    print(f"k_pin: k={kp['k_pinned']} ({kp['k_pinned_span_steps']} steps, {kp['k_pinned_criterion']})  "
          f"k_firstk={kp['k_firstk']} k_sliding={kp['k_sliding']}  single_win_min={kp['single_window_min']:.4f}  "
          f"plateau_mean_min={kp['plateau_mean_min']:.4f} (binding seed {kp['binding_seed']})")
    print(f"per_seed_d={agg['per_seed_d']}")
    if x is not None:
        print(f"converge x-check (seeds0-9): matches={x['matches']}  max_abs_dev={x['max_abs_dev']}")
    print(f"-> {OUT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=SEED_FLOOR, help="total seed count (>=20 floor)")
    ap.add_argument("--shard-index", type=int, default=None)
    ap.add_argument("--shard-count", type=int, default=None)
    ap.add_argument("--merge", action="store_true", help="fold shard files into the final artifact")
    ap.add_argument("--smoke", action="store_true", help="fast end-to-end check (2 seeds, tiny budget)")
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))

    if args.smoke:
        global CHECKPOINTS, READ_STEP, ANCHORS, PLATEAU_ONSET
        PLATEAU_ONSET, READ_STEP = 500, 1000
        ANCHORS, CHECKPOINTS = [500, 1000], [500, 600, 700, 800, 900, 1000]
        recs = _run_seeds([0, 1])
        agg = _aggregate(recs)
        print("SMOKE:", json.dumps({k: agg[k] for k in
              ("reference", "spread", "bar", "seed_count", "plateaued", "ablated_max")}, default=str))
        print("SMOKE per-seed d_diff:", [(r["seed"], r["d_diff"]) for r in recs])
        return

    if args.merge:
        recs = []
        for p in sorted(_HERE.glob("liveness_calibration.shard*.json")):
            recs += json.loads(p.read_text())["records"]
        # dedupe by seed (last wins), require >= floor
        by_seed = {r["seed"]: r for r in recs}
        recs = list(by_seed.values())
        if len(recs) < SEED_FLOOR:
            raise SystemExit(f"merge: only {len(recs)} seeds < floor {SEED_FLOOR}")
        _write_final(recs)
        return

    all_seeds = list(range(max(args.seeds, SEED_FLOOR)))
    if args.shard_count:
        seeds = [s for s in all_seeds if s % args.shard_count == args.shard_index]
        recs = _run_seeds(seeds)
        shard = _HERE / f"liveness_calibration.shard{args.shard_index}.json"
        shard.write_text(json.dumps(dict(records=recs), indent=2))
        print(f"shard {args.shard_index}/{args.shard_count}: seeds={seeds} -> {shard}")
        return

    _write_final(_run_seeds(all_seeds))


if __name__ == "__main__":
    main()
