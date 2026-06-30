"""exp07 SURFACE SWEEP — computes every interior cell + BOTH pre-computed contingencies (Run plan:
compute-unconstrained overnight, everything runs straight up). Writes RAW cube cells ONLY; performs
NO interpretation (no topology, no floor extraction, no legitimacy call — those live in
exp07_interior_read.py and run only AFTER the Step-0 review gate clears).

Three parts (each a separate durable JSON):
  main    — member=16: full cue axis x {off, reshaped@0.30, deployed}              -> exp07_surface_raw.json
  phasing — member=16: full cue axis x reshaped@{0.1,0.3,0.5,0.7,0.9} (contingency) -> exp07_phasing_raw.json
  lowcard — member=2:  full cue axis x {off, reshaped, deployed} (contingency)      -> exp07_lowcard_raw.json

Every cell is read at the reconciled plateau budget (equal-training; exp06 lesson). Each part writes
incrementally (per column) so a background run is durable.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

import torch

import exp07_config as C
from exp07_core import CueSpec, PenaltySpec, cell

_HERE = Path(__file__).resolve().parent


def _pen(name: str, clock_fraction: float | None = None) -> PenaltySpec:
    r = dict(C.PENALTY_REGIMES[name])
    if clock_fraction is not None:
        r["t2_step"] = C.onset_step(clock_fraction)   # phasing: sweep λ2 onset (abs); t1_step fixed
    return PenaltySpec(name=name, **r)


def _agg(vals):
    return dict(mean=statistics.mean(vals), std=(statistics.stdev(vals) if len(vals) > 1 else 0.0),
                min=min(vals), max=max(vals), per_seed=[round(v, 5) for v in vals])


def _column(member_count, cue_specs, pen, seeds, budget):
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


def _write(name, payload):
    Path(_HERE / name).write_text(json.dumps(payload, indent=2))


def _provenance(extra):
    return dict(commit_hash=C.commit_hash(), spec_hash=C.spec_hash(),
                seeds=C.SEEDS, budget=C.PLATEAU_BUDGET, knobs=C.KNOBS,
                DO_NOT_INTERPRET="raw cube cells; topology/floor/legitimacy are post-gate", **extra)


def run_main(seeds, budget):
    cue_specs = [CueSpec(**d) for d in C.cue_axis()]
    payload = _provenance(dict(part="main", member_count=C.M_DEPLOYED)); payload["columns"] = {}
    for pen_name in ("off", "reshaped", "deployed"):
        t0 = time.time()
        payload["columns"][pen_name] = _column(C.M_DEPLOYED, cue_specs, _pen(pen_name), seeds, budget)
        payload["columns"][pen_name]["_secs"] = round(time.time() - t0, 1)
        _write("exp07_surface_raw.json", payload)            # durable after each column
        print(f"[main] column {pen_name} done ({payload['columns'][pen_name]['_secs']}s)")
    return payload


def run_phasing(seeds, budget):
    cue_specs = [CueSpec(**d) for d in C.cue_axis()]
    payload = _provenance(dict(part="phasing", member_count=C.M_DEPLOYED,
                               phasing_fractions=C.PHASING_FRACTIONS)); payload["columns"] = {}
    for phi in C.PHASING_FRACTIONS:
        t0 = time.time()
        key = f"reshaped@{phi:g}"
        payload["columns"][key] = _column(C.M_DEPLOYED, cue_specs, _pen("reshaped", phi), seeds, budget)
        payload["columns"][key]["_secs"] = round(time.time() - t0, 1)
        _write("exp07_phasing_raw.json", payload)
        print(f"[phasing] {key} done ({payload['columns'][key]['_secs']}s)")
    return payload


def run_lowcard(seeds, budget):
    cue_specs = [CueSpec(**d) for d in C.cue_axis()]
    card = C.CORNER_CARDINALITY
    payload = _provenance(dict(part="lowcard", member_count=card)); payload["columns"] = {}
    for pen_name in ("off", "reshaped", "deployed"):
        t0 = time.time()
        payload["columns"][pen_name] = _column(card, cue_specs, _pen(pen_name), seeds, budget)
        payload["columns"][pen_name]["_secs"] = round(time.time() - t0, 1)
        _write("exp07_lowcard_raw.json", payload)
        print(f"[lowcard] column {pen_name} done ({payload['columns'][pen_name]['_secs']}s)")
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=["main", "phasing", "lowcard", "all"], default="all")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))

    if args.smoke:
        seeds, budget = [0, 1], 400
        C.REPOSING_ALPHAS[:] = [0.0, 0.5, 1.0]            # type: ignore
        C.PHASING_FRACTIONS[:] = [0.3, 0.6]               # type: ignore
    else:
        seeds, budget = C.SEEDS, C.PLATEAU_BUDGET

    runners = dict(main=run_main, phasing=run_phasing, lowcard=run_lowcard)
    parts = list(runners) if args.part == "all" else [args.part]
    for p in parts:
        print(f"=== exp07 surface part: {p} (seeds={seeds}, budget={budget}) ===")
        runners[p](seeds, budget)
    print("\n(raw cube cells written; interior read is POST-GATE)")


if __name__ == "__main__":
    main()
