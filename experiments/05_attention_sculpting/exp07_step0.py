"""exp07 STEP-0 — runs FIRST; surfaces artifacts for review BEFORE any interior surface is interpreted.

Standing gate (spec §2 + Run plan): the night may compute every cell, but the morning read still
respects order — Step-0a/0b/0c sanity gates and the cardinality corner-gate are surfaced here, and a
sanity-gate failure blocks interpretation even though the interior was computed.

  Step-0a — content-preserving re-posing construction + ablation-invariance proof (no training).
  Step-0b — cue-LOCATABILITY at the `off` column (does ANY re-posing lift (d) above flat-diffuse?),
            read at the training plateau (the under-re-organization trap). Lever-separability is
            answered by the surface itself (the topology) and is NOT decided here.
  Step-0c — predicted-column SANITY gates: deployed column ~0 across the whole cue sweep;
            off flat-diffuse ~0; off sharp ~1.106 at its 12000-step plateau (equal-training).
  Corner-gate — six corners at one lower cardinality (recommend 2): does the OR-kill structure
            (alive iff sharp & ~penalty) and the reshaped-vs-off relationship reproduce at the new
            cardinality? (read FIRST in the morning; promotes member-count only on a qualitative
            mismatch.)

STOPS at the review gate. Writes cue_reposing_construction.json, exp07_step0.json,
exp07_corner_gate.json. Nothing interpreted past the gate; nothing committed.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import torch

import exp07_config as C
from exp07_core import CueSpec, PenaltySpec, cell, cell_trajectory, reposing_validation

_HERE = Path(__file__).resolve().parent


def _pen(name: str) -> PenaltySpec:
    return PenaltySpec(name=name, **C.PENALTY_REGIMES[name])


def _agg(vals):
    return dict(mean=statistics.mean(vals), std=(statistics.stdev(vals) if len(vals) > 1 else 0.0),
                min=min(vals), max=max(vals), per_seed=[round(v, 5) for v in vals])


def _read_cells(member_count, cue_specs, pen_name, seeds, budget):
    """Read a column (one penalty regime) across the cue axis -> {cue_label: agg-rec}."""
    pen = _pen(pen_name)
    out = {}
    for cs in cue_specs:
        recs = [cell(member_count, cs, pen, s, shared_mag=C.DIFFUSE_SHARED, cue_mag=C.DIFFUSE_CUE,
                     budget=budget) for s in seeds]
        label = cs.seg if cs.seg != "repose" else f"repose@{cs.alpha:g}"
        out[label] = dict(seg=cs.seg, alpha=cs.alpha,
                          d_diff=_agg([r["d_diff"] for r in recs]),
                          d_same=_agg([r["d_same"] for r in recs]),
                          d_ablated=_agg([r["d_ablated"] for r in recs]),
                          proto_spread=_agg([r["proto_spread"] for r in recs]))
    return out


# ------------------------------------------------------------------ Step-0a
def step0a_construction(member_count, alphas):
    val = reposing_validation(member_count, C.DIFFUSE_SHARED, C.DIFFUSE_CUE, alphas)
    pairdiff_max = max(r["pairwise_diff_deviation"] for r in val)
    abl_max = max(r["ablated_max_separation"] for r in val)
    ill_posed = bool(len(alphas) <= 1)   # no structural variation constructible -> sweep ill-posed
    rec = dict(
        construction=("content-blind common-mode centering: comp_reposed[m] = comp[m] - alpha*mu, "
                      "mu = population-mean cue (cls-independent constant). alpha=0 flat-diffuse, "
                      "alpha=1 fully centered. Sharp = pure unit cue (diffuse=False), alpha=0, "
                      "labeled alive-reference only."),
        alphas=list(alphas),
        ablation_invariance=dict(
            rows=val,
            pairwise_diff_deviation_max=round(pairdiff_max, 8),
            ablated_max_separation_max=round(abl_max, 8),
            adds_no_signal=bool(pairdiff_max < 1e-5),       # (A) pairwise diffs invariant
            cannot_manufacture_floor=bool(abl_max < 1e-4),  # (B) ablated cue -> no (d) at any alpha
        ),
        sweep_ill_posed=ill_posed,
        **C.reconcile_register(),
    )
    Path(_HERE / "cue_reposing_construction.json").write_text(json.dumps(rec, indent=2))
    return rec


# ------------------------------------------------------------------ Step-0b / 0c
def step0bc(seeds, budget, checkpoints):
    cue_specs = [CueSpec(**d) for d in C.cue_axis()]

    off = _read_cells(C.M_DEPLOYED, cue_specs, "off", seeds, budget)
    deployed = _read_cells(C.M_DEPLOYED, cue_specs, "deployed", seeds, budget)

    # plateau spot-check on the off-column ceiling cells (sharp + top re-posing): d_diff flat?
    plateau = {}
    for cs in (CueSpec("sharp", 0.0), CueSpec("repose", max(C.REPOSING_ALPHAS))):
        trajs = [cell_trajectory(C.M_DEPLOYED, cs, _pen("off"), s, checkpoints,
                                 shared_mag=C.DIFFUSE_SHARED, cue_mag=C.DIFFUSE_CUE) for s in seeds]
        per_ckpt = {}
        for i, step in enumerate(sorted(set(checkpoints))):
            vals = [t[i]["d_diff"] for t in trajs]
            per_ckpt[step] = dict(d_mean=round(statistics.mean(vals), 4),
                                  d_std=round((statistics.stdev(vals) if len(vals) > 1 else 0.0), 4))
        label = cs.seg if cs.seg != "repose" else f"repose@{cs.alpha:g}"
        steps = sorted(set(checkpoints))
        flat = all(abs(per_ckpt[steps[j]]["d_mean"] - per_ckpt[steps[j - 1]]["d_mean"]) <= 0.05
                   for j in range(1, len(steps)))
        plateau[label] = dict(per_checkpoint=per_ckpt, plateaued=bool(flat))

    # ---- Step-0b: cue-locatability (off column) ----
    flat_base = off["flat"]["d_diff"]["mean"]
    margin = C.CUE_PLATEAU_MARGIN
    lifts = {k: round(v["d_diff"]["mean"] - flat_base, 4) for k, v in off.items()
             if v["seg"] == "repose"}
    any_lift = bool(any(l > margin for l in lifts.values()))
    locatability = dict(
        off_flat_baseline=round(flat_base, 5), lift_margin=margin, reposing_lifts=lifts,
        any_reposing_lifts=any_lift,
        interpretation=("locatable -> run full sweep (correction-part may be non-empty)" if any_lift
                        else "NOT locatable -> diffuseness fully intrinsic; floor = deployed snr; "
                             "cue-fix = build-robust-only (NOT 'make it sharp')"))

    # ---- Step-0c: sanity gates ----
    off_flat = off["flat"]["d_diff"]
    off_sharp = off["sharp"]["d_diff"]
    deployed_max = max(v["d_diff"]["max"] for v in deployed.values())
    off_sharp_plat = plateau["sharp"]["per_checkpoint"][max(checkpoints)]["d_mean"]
    sane_deployed = bool(deployed_max <= C.COLLAPSE_CEILING)
    sane_off_flat = bool(off_flat["max"] <= C.COLLAPSE_CEILING)
    # off-sharp must reproduce ~1.106 at plateau (band around the reconciled ref)
    sharp_lo, sharp_hi = C.OFF_SHARP_REF - 0.20, C.OFF_SHARP_REF + 0.30
    sane_off_sharp = bool(sharp_lo <= off_sharp_plat <= sharp_hi)
    sanity = dict(
        deployed_column_max=round(deployed_max, 5), deployed_collapsed=sane_deployed,
        off_flat_max=round(off_flat["max"], 5), off_flat_collapsed=sane_off_flat,
        off_sharp_plateau=round(off_sharp_plat, 4), off_sharp_ref=round(C.OFF_SHARP_REF, 4),
        off_sharp_band=[round(sharp_lo, 3), round(sharp_hi, 3)], off_sharp_ok=sane_off_sharp,
        all_sane=bool(sane_deployed and sane_off_flat and sane_off_sharp))

    rec = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), seeds=seeds, budget=budget,
        member_count=C.M_DEPLOYED,
        off_column=off, deployed_column=deployed, off_column_plateau_check=plateau,
        STEP0B_locatability=locatability, STEP0C_sanity=sanity,
    )
    Path(_HERE / "exp07_step0.json").write_text(json.dumps(rec, indent=2))
    return rec


# ------------------------------------------------------------------ corner-gate (lower cardinality)
def corner_gate(seeds, budget):
    card = C.CORNER_CARDINALITY
    corners = [CueSpec("flat", 0.0), CueSpec("sharp", 0.0)]
    grid = {}
    for pen_name in ("off", "reshaped", "deployed"):
        col = _read_cells(card, corners, pen_name, seeds, budget)
        grid[pen_name] = {k: dict(d_mean=round(v["d_diff"]["mean"], 4),
                                  d_max=round(v["d_diff"]["max"], 4),
                                  ablated_max=round(v["d_ablated"]["max"], 5),
                                  alive=bool(v["d_diff"]["mean"] >= C.LIVE_BAR
                                             and v["d_ablated"]["max"] <= C.ABLATION_FLOOR))
                          for k, v in col.items()}
    # exp06 structure at 16: alive iff (sharp & ~penalty). i.e. off/reshaped@sharp alive-ish; all else dead.
    # We report the qualitative pattern; the morning read compares it to the 16 surface.
    or_kill_holds = bool(
        grid["off"]["sharp"]["alive"] and not grid["off"]["flat"]["alive"]
        and not grid["deployed"]["sharp"]["alive"] and not grid["deployed"]["flat"]["alive"])
    rec = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), corner_cardinality=card, seeds=seeds,
        budget=budget, grid=grid,
        OR_kill_holds_at_lower_cardinality=or_kill_holds,
        note=("Qualitative gate ONLY. Read first in the morning. Match to 16 -> member-count stays a "
              "non-lever, topology not a cardinality effect. Qualitative mismatch (penalty-kill is "
              "cardinality-dependent, or reshaped helps at one cardinality not the other) -> promote "
              "member-count to a third lever (the pre-computed low-cardinality full surface is "
              "interpreted)."),
    )
    Path(_HERE / "exp07_corner_gate.json").write_text(json.dumps(rec, indent=2))
    return rec


def _print_gate(con, bc, cg):
    print("\n" + "=" * 80)
    print(f"exp07 STEP-0 REVIEW GATE  (commit {con['commit_hash'][:7]}, spec {con['spec_hash']})")
    print("=" * 80)
    ai = con["ablation_invariance"]
    print("\nStep-0a — content-preserving re-posing construction:")
    print(f"  {con['construction']}")
    print(f"  alphas = {con['alphas']}")
    print(f"  (A) adds no signal (pairwise-diff invariant): {ai['adds_no_signal']} "
          f"(max dev {ai['pairwise_diff_deviation_max']:.2e})")
    print(f"  (B) cannot manufacture floor (ablated -> no d): {ai['cannot_manufacture_floor']} "
          f"(max ablated sep {ai['ablated_max_separation_max']:.2e})")
    print(f"  sweep ill-posed: {con['sweep_ill_posed']}")

    s = bc["STEP0C_sanity"]
    print("\nStep-0c — predicted-column sanity gates:")
    print(f"  deployed column max d={s['deployed_column_max']:.4f} (<= {C.COLLAPSE_CEILING}) "
          f"-> collapsed={s['deployed_collapsed']}")
    print(f"  off flat-diffuse max d={s['off_flat_max']:.4f} (<= {C.COLLAPSE_CEILING}) "
          f"-> collapsed={s['off_flat_collapsed']}")
    print(f"  off sharp @plateau d={s['off_sharp_plateau']:.4f} vs ref {s['off_sharp_ref']:.4f} "
          f"band {s['off_sharp_band']} -> ok={s['off_sharp_ok']}")
    print(f"  ALL SANE = {s['all_sane']}")

    b = bc["STEP0B_locatability"]
    print("\nStep-0b — cue-locatability (off column; under-re-organization trap guarded by plateau):")
    print(f"  off flat baseline d={b['off_flat_baseline']:.5f}; reposing lifts (vs baseline): "
          f"{b['reposing_lifts']}")
    print(f"  any re-posing lifts (> {b['lift_margin']}): {b['any_reposing_lifts']}")
    print(f"  -> {b['interpretation']}")
    pc = bc["off_column_plateau_check"]
    for k, v in pc.items():
        print(f"  plateau[{k}]: {[ (st, c['d_mean']) for st, c in v['per_checkpoint'].items() ]} "
              f"plateaued={v['plateaued']}")

    print(f"\nCorner-gate (cardinality {cg['corner_cardinality']}; read FIRST):")
    for pen_name, col in cg["grid"].items():
        cells = "  ".join(f"{k}:{v['d_mean']:.3f}{'(alive)' if v['alive'] else ''}"
                          for k, v in col.items())
        print(f"  [{pen_name:8s}] {cells}")
    print(f"  OR-kill (alive iff sharp & ~penalty) holds at lower cardinality: "
          f"{cg['OR_kill_holds_at_lower_cardinality']}")

    print("\n  >>> STOP. Interior surface (topology / floor / legitimacy) is POST-GATE — read only")
    print("      after this review. Surface artifacts written; nothing interpreted; nothing committed. <<<")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="tiny budget/seeds/alphas for pipeline test")
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))

    if args.smoke:
        seeds, budget = [0, 1], 400
        checkpoints = [200, 400]
        alphas = [0.0, 0.5, 1.0]
    else:
        seeds, budget = C.SEEDS, C.PLATEAU_BUDGET
        checkpoints = C.KNOBS["plateau_checkpoints"]
        alphas = C.REPOSING_ALPHAS

    # Step-0a uses the actual alpha grid (smoke shrinks it)
    if args.smoke:
        C.REPOSING_ALPHAS[:] = alphas  # type: ignore  (shrink the module grid for the smoke pipeline)

    con = step0a_construction(C.M_DEPLOYED, alphas)
    bc = step0bc(seeds, budget, checkpoints)
    cg = corner_gate(seeds, budget)
    _print_gate(con, bc, cg)


if __name__ == "__main__":
    main()
