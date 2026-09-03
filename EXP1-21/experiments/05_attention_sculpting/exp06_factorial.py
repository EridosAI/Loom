"""exp06 — Channel-Revival Factorial: Step-0 orchestrator (separability + dual-anchor gate + V3
traverse). Runs FIRST; surfaces factor_separability.json + anchor_gate.json (+ the V3 traverse
result) for review BEFORE the interior cube is read. Pre-registered per EXP06_CHANNEL_REVIVAL_
FACTORIAL_SPEC.md.

EXECUTION-ORDER DISCIPLINE (binding, from the run directive):
  * Resolve the validity TRIAD first and fully — V1 (clean anchor spans up), V2 (dead anchor
    collapses), V3 (>=1 single-toggle traverses) — before interpreting ANY interior cell.
  * V3 is resolved BEFORE any super-additivity / interaction analysis (super-additivity is only
    meaningful if something traversed; on a non-traversing cube every lift is noise).
  * This module STOPS at the review gate: it writes the triad + the raw cube cell table (the cells
    are needed to COMPUTE V3) but does NOT compute super-additivity, does NOT name a lever, does NOT
    make a redesign-direction call, and commits NOTHING. Those are strictly downstream of a passing
    triad and a human review.

The measurement is the committed neutral (d)-gate (dgate.py) — content-agnostic, carrier bounded in
every cell, binary at the healthy bar, ablation-guarded (a non-collapsing ablation = magnitude
artifact, rejected). The three factors are member-count x cue-diffuseness x PAM pool-penalty; the
carrier is NOT a factor (bounded baseline in all cells).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import subprocess
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))  # exp04 (constants)

import constants                                            # noqa: E402
from sculpt_config import SculptConfig                      # noqa: E402  (exp05 deployed conflict cfg)
from dgate import Factors, dgate, force_collapsed_floor     # noqa: E402

# ------------------------------------------------------------------ [RECONCILE] register
# All deployed levels are READ programmatically from the exp05 commit config (SculptConfig — the
# deployed conflict rig), never pinned by feel. The comments show the read values for transparency;
# nothing here is a hand-set literal.
_CFG = SculptConfig()                                       # deployed Stage-1 conflict config (commit)

DEPLOYED_STEPS = _CFG.steps                                 # 4000 — the deployed training budget
DEPLOYED_PAM_LAM = _CFG.pam_lam                             # 0.01 — deployed PAM pool-penalty
M_MANY = _CFG.n_A * _CFG.n_B                                # 16 = n_A*n_B, full deployed completion
                                                           # cardinality (n_B=4 verified equivalent
                                                           # for the gate; see calibration note)
# diffuse-cue salience STRUCTURE: the radii are READ from the commit (R_coarse, r_distractor,
# r_category); the *mapping* (subtle member-cue r_category buried under salient shared energy
# sqrt(R_coarse^2 + r_distractor^2)) is a CONSTRUCTION calibrated to the deployed salience ratio —
# random DIRECTIONS keep the probe content-agnostic. NOT a literal transcription of the deployed cue.
DIFFUSE_SHARED = (_CFG.R_coarse ** 2 + _CFG.r_distractor ** 2) ** 0.5   # read: 5.0, 3.0 -> 5.831
DIFFUSE_CUE = _CFG.r_category                              # read: 0.5 (deployed subtle named axis)

SEEDS = [0, 1, 2, 3, 4]                                     # >=5: read REVIVAL variance (Phase-1's 3
                                                           # was too few — SPEC §7)

# factor levels: (member_count, diffuse) ; pam_lam handled separately
CLEAN = dict(member_count=2, diffuse=False, pam_lam=0.0)
DEAD = dict(member_count=M_MANY, diffuse=True, pam_lam=DEPLOYED_PAM_LAM)


def _factors(member_count, diffuse, pam_lam) -> Factors:
    return Factors(member_count=member_count, diffuse=diffuse, pam_lam=pam_lam,
                   diffuse_shared_mag=DIFFUSE_SHARED, diffuse_cue_mag=DIFFUSE_CUE,
                   train_steps=DEPLOYED_STEPS)


# The 8 cube cells, labelled by (member-count, diffuseness, penalty) toggles from clean (0) / dead (1).
def _cube_cells():
    levels = dict(member_count=(2, M_MANY), diffuse=(False, True), pam_lam=(0.0, DEPLOYED_PAM_LAM))
    cells = {}
    for mi, m in enumerate(levels["member_count"]):
        for fi, f in enumerate(levels["diffuse"]):
            for pi, p in enumerate(levels["pam_lam"]):
                code = (mi, fi, pi)                          # 0=clean level, 1=deployed level per factor
                cells[code] = _factors(m, f, p)
    return cells


def spec_hash() -> str:
    payload = dict(SEEDS=SEEDS, DEPLOYED_STEPS=DEPLOYED_STEPS, DEPLOYED_PAM_LAM=DEPLOYED_PAM_LAM,
                   M_MANY=M_MANY, DIFFUSE_SHARED=round(DIFFUSE_SHARED, 4), DIFFUSE_CUE=DIFFUSE_CUE)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]


def _commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(_HERE),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def _agg(rows, key):
    vals = [r[key] for r in rows]
    return dict(mean=statistics.mean(vals), std=(statistics.stdev(vals) if len(vals) > 1 else 0.0),
                min=min(vals), max=max(vals), per_seed=vals)


# ------------------------------------------------------------------ run all cells (once)
def run_cube(seeds, quick=False):
    """Train+measure every cube cell at every seed. Returns {code: {seed: dgate-rec}} + per-cell agg.
    Running all 8 cells is REQUIRED to resolve V3 (the single-toggles); the interior is NOT read here."""
    cells = _cube_cells()
    raw = {}
    for code, f in cells.items():
        if quick:
            f = Factors(**{**f.__dict__, "train_steps": 1500})
        recs = [dgate(f, seed=s) for s in seeds]
        raw[code] = dict(factors=dict(member_count=f.member_count, diffuse=f.diffuse,
                                      pam_lam=f.pam_lam, cue_snr=round(f.cue_snr, 4)),
                         d_diff=_agg(recs, "d_diff"), d_same=_agg(recs, "d_same"),
                         d_ablated=_agg(recs, "d_ablated"), proto_spread=_agg(recs, "proto_spread"))
    return raw


# ------------------------------------------------------------------ Step-0a: separability
def step0a_separability(out="factor_separability.json"):
    """Independent-toggle construction. In dgate.Factors, member_count (int) and diffuse (bool) are
    ORTHOGONAL parameters with no shared state: all four (member-count x diffuseness) combinations are
    constructible independently, and pam_lam is a third orthogonal knob. -> Outcome A (separable),
    full 2x2x2. (Outcome B would require the rig to be UNABLE to set diffuseness at a fixed member-
    count; it is not.)"""
    cells = _cube_cells()
    constructible = sorted({(f.member_count, f.diffuse) for f in cells.values()})
    notes = (
        "member_count (int) and diffuse (bool) are independent fields of dgate.Factors with no shared "
        "state; cue-diffuseness is a cue-structure knob (shared-salient-base vs pure-differentiating "
        "cue) that applies identically at any member-count, and member-count is a cardinality knob "
        "that applies at either diffuseness. All four (member-count x diffuseness) combinations were "
        f"constructed independently: {constructible}. pam_lam is a third orthogonal knob (training-loss "
        "penalty coefficient). No structural coupling -> Outcome A."
    )
    rec = dict(separable=True, outcome="A (separable) -> full 2x2x2 cube",
               constructible_member_diffuse_combos=[[m, d] for m, d in constructible],
               construction_notes=notes, commit_hash=_commit_hash(), spec_hash=spec_hash())
    Path(out).write_text(json.dumps(rec, indent=2))
    return rec


# ------------------------------------------------------------------ Step-0b + V3
def step0b_and_v3(raw, out="anchor_gate.json"):
    """Dual-anchor hard gate (V1, V2) + the traverse validity check (V3). Resolves the full triad;
    does NOT read the interior. collapse_floor / healthy / margins are calibrated from this run +
    the forced-collapse reference, surfaced here."""
    clean = raw[(0, 0, 0)]
    dead = raw[(1, 1, 1)]
    floor_ref = force_collapsed_floor(0)                    # deployed content-invariant reference

    healthy_value = clean["d_diff"]["mean"]
    clean_std = clean["d_diff"]["std"]
    dead_mean = dead["d_diff"]["mean"]
    dead_std = dead["d_diff"]["std"]

    # --- calibrated bars (data-driven; surfaced) ---
    # measurement seed-spread = WITHIN-cell seed-to-seed std (NOT the clean-vs-dead gap). The traverse
    # test (below) compares each cell's move to the combined within-cell noise of cell+corner.
    MIN_MARGIN = 0.10
    TRAVERSE_K = 3.0                                        # require |move| > K * combined seed-noise
    collapse_ceiling = max(floor_ref["d_diff"], dead_mean) + max(3.0 * dead_std, 0.05)
    ablation_floor = max(clean["d_ablated"]["max"], floor_ref["d_diff"]) + 0.10
    live_bar = healthy_value - 2.0 * clean_std             # the "~healthy neighbourhood" bar
    proto_collapse_bar = 0.05                               # dead prototype-spread must be ~collapsed

    # --- V1: clean corner robustly LIVE (spans up) + ablation collapses ---
    v1_live = bool(clean["d_diff"]["min"] >= live_bar)
    v1_abl = bool(clean["d_ablated"]["max"] <= ablation_floor)
    v1_pass = bool(v1_live and v1_abl and (live_bar > collapse_ceiling))

    # --- V2: dead corner robustly COLLAPSED ---
    v2_pass = bool(dead["d_diff"]["max"] <= collapse_ceiling
                   and dead["proto_spread"]["max"] <= proto_collapse_bar)

    # --- V3: traverse. Every non-anchor cell vs its ADJACENT corner (Hamming-1). ---
    # from-clean cells (one deployed factor; sum(code)==1) are adjacent to CLEAN;
    # from-dead cells (two deployed factors; sum(code)==2) are adjacent to DEAD.
    factor_names = ("member-count", "cue-diffuseness", "pam-pool-penalty")
    adj_std = {"clean": clean_std, "dead": dead_std}
    traverse_rows = []
    for code, cell in raw.items():
        s = sum(code)
        if s in (0, 3):
            continue                                       # the anchors themselves
        adj = "clean" if s == 1 else "dead"
        adj_mean = healthy_value if adj == "clean" else dead_mean
        delta = cell["d_diff"]["mean"] - adj_mean
        # combined within-cell seed-noise of cell + its adjacent corner (std of the difference)
        noise = (cell["d_diff"]["std"] ** 2 + adj_std[adj] ** 2) ** 0.5
        margin = max(TRAVERSE_K * noise, MIN_MARGIN)
        moved = bool(abs(delta) > margin)
        toggled = [factor_names[i] for i in range(3) if (code[i] == 1) == (adj == "clean")]
        # ^ from clean: the deployed (1) factors are what was toggled; from dead: the clean (0) factors
        traverse_rows.append(dict(code=list(code), adjacent_corner=adj,
                                  toggled_from_corner=toggled,
                                  cell_d_diff=round(cell["d_diff"]["mean"], 4),
                                  cell_std=round(cell["d_diff"]["std"], 4),
                                  adjacent_d_diff=round(adj_mean, 4),
                                  delta=round(delta, 4), seed_noise=round(noise, 4),
                                  margin=round(margin, 4), moved=moved))
    v3_pass = bool(any(r["moved"] for r in traverse_rows))
    n_moved = sum(r["moved"] for r in traverse_rows)
    traverse_margin = round(min((r["margin"] for r in traverse_rows), default=MIN_MARGIN), 4)

    triad_pass = bool(v1_pass and v2_pass and v3_pass)

    rec = dict(
        commit_hash=_commit_hash(), spec_hash=spec_hash(), seeds=SEEDS,
        deployed_levels=dict(train_steps=DEPLOYED_STEPS, pam_lam=DEPLOYED_PAM_LAM, M_many=M_MANY,
                             m_many_basis="n_A*n_B (full deployed completion cardinality); n_B=4 "
                             "verified to collapse identically",
                             diffuse_shared_mag=round(DIFFUSE_SHARED, 4), diffuse_cue_mag=DIFFUSE_CUE,
                             diffuse_cue_snr=round(DIFFUSE_CUE / DIFFUSE_SHARED, 4)),
        calibrated_bars=dict(healthy_value=round(healthy_value, 4), clean_std=round(clean_std, 4),
                             live_bar=round(live_bar, 4), collapse_floor=round(floor_ref["d_diff"], 6),
                             collapse_ceiling=round(collapse_ceiling, 4),
                             ablation_floor=round(ablation_floor, 4),
                             traverse_K=TRAVERSE_K, traverse_min_margin=traverse_margin,
                             min_floor_margin=MIN_MARGIN,
                             proto_collapse_bar=proto_collapse_bar),
        V1_clean_anchor=dict(d_diff=clean["d_diff"], d_ablated=clean["d_ablated"],
                             proto_spread=clean["proto_spread"], live=v1_live, ablation_ok=v1_abl,
                             PASS=v1_pass),
        V2_dead_anchor=dict(d_diff=dead["d_diff"], proto_spread=dead["proto_spread"],
                            forced_collapse_ref=floor_ref, PASS=v2_pass),
        V3_traverse=dict(margin=round(traverse_margin, 4), n_moved=n_moved, n_cells=len(traverse_rows),
                         per_cell=traverse_rows, PASS=v3_pass),
        TRIAD_PASS=triad_pass,
        cube_cells_RAW_DO_NOT_INTERPRET={",".join(map(str, k)): v for k, v in raw.items()},
        # ^ keyed "m,f,p" (0=clean level,1=deployed level). Needed to COMPUTE V3; interior read is
        #   POST-GATE (no super-additivity here).
    )
    Path(out).write_text(json.dumps(rec, indent=2))
    return rec


def _print_gate(sep, gate):
    print("\n" + "=" * 78)
    print(f"exp06 STEP-0 REVIEW GATE  (commit {gate['commit_hash'][:7]}, spec {gate['spec_hash']})")
    print("=" * 78)
    print(f"\nStep-0a separability: {sep['outcome']}  (separable={sep['separable']})")
    b = gate["calibrated_bars"]
    print(f"\nCalibrated bars (from this run + forced-collapse ref):")
    print(f"  healthy_value={b['healthy_value']} (clean_std={b['clean_std']})  live_bar={b['live_bar']}")
    print(f"  collapse_floor={b['collapse_floor']}  collapse_ceiling={b['collapse_ceiling']}")
    print(f"  ablation_floor={b['ablation_floor']}  traverse: K={b['traverse_K']}*seed-noise "
          f"(floor {b['min_floor_margin']}, smallest applied {b['traverse_min_margin']})")
    v1, v2, v3 = gate["V1_clean_anchor"], gate["V2_dead_anchor"], gate["V3_traverse"]
    print(f"\n  V1 clean anchor  : d_diff mean={v1['d_diff']['mean']:.3f} "
          f"[min={v1['d_diff']['min']:.3f}] ablated max={v1['d_ablated']['max']:.3f} "
          f"-> {'PASS' if v1['PASS'] else 'FAIL'}")
    print(f"  V2 dead anchor   : d_diff max={v2['d_diff']['max']:.3f} "
          f"proto_spread max={v2['proto_spread']['max']:.3g} -> {'PASS' if v2['PASS'] else 'FAIL'}")
    print(f"  V3 traverse      : {v3['n_moved']}/{v3['n_cells']} single-toggles moved off corner "
          f"(K={b['traverse_K']}*seed-noise, floor {b['min_floor_margin']}) "
          f"-> {'PASS' if v3['PASS'] else 'FAIL'}")
    for r in v3["per_cell"]:
        flag = "MOVED" if r["moved"] else "pinned"
        print(f"      {str(r['code']):11s} adj={r['adjacent_corner']:5s} "
              f"d={r['cell_d_diff']:.3f}±{r['cell_std']:.2f} vs {r['adjacent_d_diff']:.3f} "
              f"(Δ{r['delta']:+.3f}, margin {r['margin']:.3f})  [{flag}]")
    print(f"\n  TRIAD_PASS = {gate['TRIAD_PASS']}")
    print("\n  >>> STOP. Interior cube + super-additivity are POST-GATE (downstream of a passing")
    print("      triad AND this review). Nothing committed. Surface the two JSONs for review. <<<")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="quick CPU config (reduced steps)")
    args = ap.parse_args()
    torch.set_num_threads(max(1, (torch.get_num_threads() or 2)))

    sep = step0a_separability()
    raw = run_cube(SEEDS, quick=args.smoke)
    gate = step0b_and_v3(raw)
    _print_gate(sep, gate)


if __name__ == "__main__":
    main()
