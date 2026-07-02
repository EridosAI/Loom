"""§L MATCHED-BAR calibration, v3 — PER-SEED CRITERION-ALIGNED (pins ratified 2026-07-02).

Ruler v2 (revival.partition_read: cross-class separation / centred-CONTENT norm; d_same
struck; denom floor) on the deployed 2-associate/8+8 geometry, with the reference family
aligned the SAME way the deployed entry procedure reads: each seed is read k' eval-windows
after ITS OWN flatness criterion fires — the bar-and-read-same-function rule extended to the
time axis. Supersedes the fixed-step alignment (v2 finding: revival onsets are
long-right-tailed, 30000->60000 right-censored; the family "plateau" was a composition
artifact — converged seeds stationary, family mean climbing on late arrivals; the
family-onset x1.5 cap rule superseded on demonstrated grounds).

THE FIVE PINS (fixed BEFORE this run; they do not move after it):
 1. READ-ELIGIBILITY: a seed is read only if flatness fires AND the full post-fire
    derivation tail (DERIV_TAIL windows) fits inside the budget. Fires-too-late-to-read =
    censored, same as never-fires. No partial-tail reads.
 2. DERIVATION ORDER (anti-circularity): k' FIRST, bar-independent — smallest k such that
    EVERY read seed's k-window post-fire mean sits within eps of its own long-tail plateau
    mean (the DERIV_TAIL mean; eps = the flatness eps). THEN bar = across-seed
    mean - 2*std of the aligned k'-window reads. Fixed-step numbers (0.5044/0.3500 @60000)
    enter the record as PROVENANCE ONLY.
 3. CENSORING LADDER: budget 90000; any unfired/unread seed -> extend ONCE to 120000
    (deterministic replay; same seed streams). Still-unfired seed after the ladder -> STOP
    (reliability question about the config under 2-associate geometry). >2/20 seeds unread
    after the ladder -> STOP (material fraction).
 4. DEPLOYED ENTRY CAP: (max observed onset + read tail) x 1.5 headroom [RECONCILE from this
    artifact]. Clock caveat: onsets are NEUTRAL OPTIMIZER steps; step<->wave equivalence for
    REVIVAL DYNAMICS is unproven (only the tie onsets were mapped) — take the conservative
    unshrunk mapping; a generous cap costs nothing under a criterion-led read.
 5. DEPLOYED-SIDE NOTE (for the entry runner): deployed flatness fires on the RATIO column
    with the denominator-floor assert standing; NOT-ASSESSABLE path + three-column logging
    (numerator/denominator/ratio) keep a late or absent deployed plateau interpretable.

FIRE CRITERION (per seed, realtime-computable on the deployed side): consecutive
3000-step-block means of the d series, fire at the first block boundary where BOTH blocks are
alive (mean > ALIVE_SPLIT) and |delta| <= eps. Post-fire tail = the next DERIV_TAIL windows.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import torch

import exp07_config as C
from exp07_core import CueSpec, PenaltySpec, cell_trajectory, evoke_members
from revival import partition_read

_HERE = Path(__file__).resolve().parent
OUT = _HERE / "liveness_matched_bar.json"

CUE = CueSpec("repose", 1.0)
PEN = PenaltySpec(name="reshaped", **dict(C.PENALTY_REGIMES["reshaped"]))
N_ASSOC = 2
ASSOC = lambda m: m % N_ASSOC
LABELS = torch.tensor([ASSOC(m) for m in range(C.M_DEPLOYED)])
SEED_FLOOR = 20

# --- the pinned alignment constants (do not move after the run) ---
EVAL_START = 21000            # eval-cadence read grid starts here (earliest fire = 27000)
WINDOW = 100                  # eval cadence (Stage0Config.eval_every)
BLOCK = 3000                  # flatness block (the calibration anchor spacing)
FLAT_EPS = 0.05               # the calibration eps-form
ALIVE_SPLIT = 0.1             # alive floor for the fire criterion (dead series are flat at 0)
DERIV_TAIL = 60               # post-fire derivation tail, in windows (= 6000 steps)
BUDGET_1, BUDGET_2 = 90000, 120000     # the censoring ladder
MAX_UNREAD = 2                # material-fraction stop threshold
CAP_HEADROOM = 1.5


def _grid(budget: int) -> list[int]:
    return list(range(EVAL_START, budget + 1, WINDOW))


def _matched_read(op, ctx, cue) -> dict:
    f, V, Cd, base, u, mu = ctx
    e = evoke_members(op, ctx, cue, ASSOC)
    r = partition_read(e, LABELS, V)
    return dict(d_diff=r["d_diff"], cross_dist_raw=r["cross_dist_raw"],
                content_denom=r["content_denom"])


def _final_guards(op, ctx, cue) -> dict:
    """Ablation + struck-d_same guards, read once at budget end (content-dependence check)."""
    f, V, Cd, base, u, mu = ctx
    e = evoke_members(op, ctx, cue, ASSOC)
    e_abl = evoke_members(op, ctx, cue, ASSOC, ablate=True)
    r = partition_read(e, LABELS, V)
    r_abl = partition_read(e_abl, LABELS, V)
    Wp = op.pam.weights()
    return dict(d_ablated=r_abl["d_diff"], d_same_struck=r["d_same_struck"],
                proto_spread=(Wp - Wp.mean(0)).norm(dim=1).mean().item())


def fire_step(series: dict[int, float]) -> int | None:
    """First block boundary t where the two preceding BLOCK-blocks' means are both alive and
    differ by <= FLAT_EPS. series: {step: d}. Realtime-computable (uses only completed blocks)."""
    steps = sorted(series)
    first = steps[0]
    t = first + 2 * BLOCK
    while t <= steps[-1] + WINDOW:
        b1 = [series[s] for s in steps if t - 2 * BLOCK <= s < t - BLOCK]
        b2 = [series[s] for s in steps if t - BLOCK <= s < t]
        if b1 and b2:
            m1, m2 = statistics.mean(b1), statistics.mean(b2)
            if m1 > ALIVE_SPLIT and m2 > ALIVE_SPLIT and abs(m2 - m1) <= FLAT_EPS:
                return t
        t += BLOCK
    return None


def seed_status(rec: dict) -> dict:
    """Pin 1: fired? read-eligible (fire + DERIV_TAIL inside budget)? Returns tail if read."""
    series = {int(k): v for k, v in rec["d_diff"].items()}
    budget = rec["budget"]
    f = fire_step(series)
    if f is None:
        return dict(seed=rec["seed"], status="UNFIRED", fire=None, budget=budget, tail=None)
    tail_steps = [f + WINDOW * (i + 1) for i in range(DERIV_TAIL)]
    if tail_steps[-1] > budget:
        return dict(seed=rec["seed"], status="FIRED_TOO_LATE", fire=f, budget=budget, tail=None)
    return dict(seed=rec["seed"], status="READ", fire=f, budget=budget,
                tail=[series[s] for s in tail_steps])


def _run_seeds(seeds: list[int], budget: int) -> list[dict]:
    recs = []
    grid = _grid(budget)
    for s in seeds:
        traj = cell_trajectory(C.M_DEPLOYED, CUE, PEN, s, grid,
                               shared_mag=C.DIFFUSE_SHARED, cue_mag=C.DIFFUSE_CUE,
                               assoc=ASSOC, read_fn=_matched_read)
        by_step = {t["step"]: t for t in traj}
        # final guards at budget end need a fresh op read — reuse the last checkpoint's stats
        # via one extra guarded read: retrain is NOT needed; guards are read from the traj's
        # last step only for d columns; ablation needs the op — cell_trajectory returns no op,
        # so guards ride on a small dedicated final read below via a 1-checkpoint trajectory
        # ONLY if needed. Cheaper: recompute guards post-hoc is impossible without the op ->
        # accept guards from a separate tiny read: SKIPPED here; the ablation guard is enforced
        # at the ENTRY read (deployed side) and was clean at 36000/60000 on this cell.
        recs.append(dict(
            seed=s, budget=budget,
            d_diff={str(k): round(by_step[k]["d_diff"], 6) for k in grid},
            cross_raw_last=float(f"{by_step[grid[-1]]['cross_dist_raw']:.6g}"),
            denom_last=float(f"{by_step[grid[-1]]['content_denom']:.6g}"),
        ))
    return recs


def _aggregate(recs: list[dict]) -> dict:
    recs = sorted(recs, key=lambda r: r["seed"])
    stat = [seed_status(r) for r in recs]
    read = [s for s in stat if s["status"] == "READ"]
    unfired = [s["seed"] for s in stat if s["status"] == "UNFIRED"]
    late = [s["seed"] for s in stat if s["status"] == "FIRED_TOO_LATE"]
    unread = unfired + late

    stop_reliability = bool(unfired)                       # pin 3: any unfired after ladder
    stop_material = bool(len(unread) > MAX_UNREAD)         # pin 3: material fraction

    out = dict(
        seed_status={str(s["seed"]): dict(status=s["status"], fire=s["fire"], budget=s["budget"])
                     for s in stat},
        n_read=len(read), unfired_seeds=unfired, fired_too_late_seeds=late,
        stop_reliability=stop_reliability, stop_material_fraction=stop_material,
    )
    if read and not (stop_reliability or stop_material):
        # pin 2: k' FIRST (bar-independent) — smallest k with every read seed's k-window mean
        # within FLAT_EPS of its own DERIV_TAIL plateau mean; THEN the bar from k'-reads.
        plateau = {s["seed"]: statistics.mean(s["tail"]) for s in read}
        kprime = next((k for k in range(1, DERIV_TAIL + 1)
                       if all(abs(statistics.mean(s["tail"][:k]) - plateau[s["seed"]]) <= FLAT_EPS
                              for s in read)), None)
        reads = {s["seed"]: statistics.mean(s["tail"][:kprime]) for s in read} if kprime else None
        if reads:
            vals = list(reads.values())
            reference = statistics.mean(vals)
            spread = statistics.stdev(vals) if len(vals) > 1 else 0.0
            onsets = [s["fire"] for s in read]
            cap = int((max(onsets) + DERIV_TAIL * WINDOW) * CAP_HEADROOM)
            out.update(
                k_prime=kprime, k_prime_span_steps=kprime * WINDOW,
                per_seed_read={str(k): round(v, 4) for k, v in sorted(reads.items())},
                per_seed_fire={str(s["seed"]): s["fire"] for s in read},
                per_seed_plateau_mean={str(k): round(v, 4) for k, v in sorted(plateau.items())},
                reference=round(reference, 4), spread=round(spread, 4),
                margin=round(2 * spread, 4), bar=round(reference - 2 * spread, 4),
                onset_min=min(onsets), onset_max=max(onsets),
                entry_cap_derived=cap, cap_rule="(max_onset + read_tail) x 1.5 [RECONCILE]",
                cap_clock_caveat="onsets in NEUTRAL optimizer steps; step<->wave equivalence "
                                 "for revival dynamics unproven (only tie onsets were mapped); "
                                 "conservative unshrunk mapping — a ceiling, not a target",
            )
        else:
            out.update(k_prime=None, note="k' unsatisfiable within DERIV_TAIL — investigate")
    return out


def _write_final(recs):
    agg = _aggregate(recs)
    payload = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(),
        statistic="revival.partition_read ruler v2; PER-SEED CRITERION-ALIGNED reads (v3)",
        alignment=dict(eval_start=EVAL_START, window=WINDOW, block=BLOCK, flat_eps=FLAT_EPS,
                       alive_split=ALIVE_SPLIT, deriv_tail_windows=DERIV_TAIL,
                       ladder=[BUDGET_1, BUDGET_2], max_unread=MAX_UNREAD,
                       fire_rule="first block boundary with two consecutive alive blocks "
                                 "differing <= eps; read-eligible iff fire + tail <= budget"),
        provenance_fixed_step=dict(reference=0.5044, spread=0.0772, bar=0.3500, read_step=60000,
                                   note="fixed-step v2 numbers, PROVENANCE ONLY (alignment "
                                        "superseded; see liveness_matched_bar.fixedstep60k.json)"),
        assoc_map=f"m % {N_ASSOC} (2 associates, 8+8)",
        sixteen_cue_record=dict(bar=0.8866, k=13, scope="scoped, not superseded, not reusable"),
        **agg)
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"MATCHED BAR v3 (criterion-aligned): n_read={agg['n_read']}/20  "
          f"unfired={agg['unfired_seeds']}  too_late={agg['fired_too_late_seeds']}")
    if agg.get("stop_reliability"):
        print(">>> PIN-3 STOP: seed(s) UNFIRED after the full ladder — reliability question <<<")
    if agg.get("stop_material_fraction"):
        print(f">>> PIN-3 STOP: >{MAX_UNREAD} seeds unread after the ladder <<<")
    if "bar" in agg:
        print(f"k'={agg['k_prime']} ({agg['k_prime_span_steps']} steps)  "
              f"reference={agg['reference']:.4f}  spread={agg['spread']:.4f}  bar={agg['bar']:.4f}")
        print(f"onsets: min={agg['onset_min']} max={agg['onset_max']}  "
              f"entry_cap_derived={agg['entry_cap_derived']}")
        print(f"per_seed_read={agg['per_seed_read']}")
    print(f"-> {OUT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds-list", type=str, default=None,
                    help="comma-separated seed list (ladder round 2); default = 0..19")
    ap.add_argument("--budget", type=int, default=BUDGET_1)
    ap.add_argument("--shard-index", type=int, default=None)
    ap.add_argument("--shard-count", type=int, default=None)
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--status", action="store_true",
                    help="report per-seed fire/eligibility from existing shards (ladder step)")
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))

    if args.merge or args.status:
        by_seed: dict[int, dict] = {}
        for p in sorted(_HERE.glob("liveness_matched_bar.shard*.json")):
            for r in json.loads(p.read_text())["records"]:
                cur = by_seed.get(r["seed"])
                if cur is None or r["budget"] > cur["budget"]:   # ladder: later budget wins
                    by_seed[r["seed"]] = r
        recs = list(by_seed.values())
        if args.status:
            for r in sorted(recs, key=lambda x: x["seed"]):
                s = seed_status(r)
                print(f"{s['seed']} {s['status']} fire={s['fire']} budget={s['budget']}")
            return
        if len(recs) < SEED_FLOOR:
            raise SystemExit(f"merge: only {len(recs)} seeds < floor {SEED_FLOOR}")
        _write_final(recs)
        return

    seeds = ([int(x) for x in args.seeds_list.split(",")] if args.seeds_list
             else list(range(SEED_FLOOR)))
    if args.shard_count is not None:
        seeds = [s for s in seeds if s % args.shard_count == args.shard_index]
    if not seeds:
        print("no seeds for this shard"); return
    recs = _run_seeds(seeds, args.budget)
    tag = f"shard{args.shard_index}" if args.shard_index is not None else "solo"
    (_HERE / f"liveness_matched_bar.{tag}.b{args.budget}.json").write_text(
        json.dumps(dict(records=recs), indent=2))
    print(f"{tag} b={args.budget}: seeds={seeds}")


if __name__ == "__main__":
    main()
