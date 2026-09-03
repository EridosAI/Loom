"""exp19_corridor.py — the EXP19 W-PERM corridor (G8 RATIFIED against a9adb12; Jason 2026-07-18).

39 runs, order: ALL cal (3 paid B x 5) -> per-B ops (G7: FULL separation curves, integer-tie => HALT,
underpower => HALT) -> ALL verdict (3 x 8) -> B8 dual-detector scoring + B* bracket. Capture harness on
every run (capture_run: per-onset + checkpoints). Auto-push at every closed gate. All halt fences live —
any HALT stops the batch with the state pushed; never substitute, never proceed past a fence.

Cal labeling (the one-family instrument, outcome-blind): a cal seed is a converter iff its FULL-read
longest run at the EVAL-native width 300 clears its own simulated null (B8 _certify_seed, band 0.64).
The per-B ops are then cut by the committed law (exp19_cal.cal_floor_audit) on that B's OWN cal data,
threaded via data= (no tag coupling). Derived series per run committed (v5 item e).
"""
from __future__ import annotations

import json
import subprocess
import sys
import time

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp16_score as X16
import exp19_cal as CAL
import exp19_floor as FL
import exp19_replay as REP
import exp19_score as S19
import exp19_scorer as SC

ROOT = XA.OUTDIR.parent.parent.parent            # repo root (exp08 -> 05_attention -> experiments -> root)
ARMS = {B: X12.exp19_wperm(B) for B in (32, 128, 512)}
CAL_SEEDS = [20, 21, 22, 24, 25]
VERDICT_SEEDS = list(range(8))
READ_AT, H_MAX, TAG = 500_000, 1_000_000, "g9"
LOG = XA.OUTDIR / "exp19_corridor_log.json"
STATE: dict = dict(runs=[], ops={}, verdicts={}, halts=[])


def _save():
    LOG.write_text(json.dumps(STATE, indent=2))


def _halt(msg: str):
    STATE["halts"].append(msg); _save()
    _push(f"EXP19 corridor HALT — {msg[:60]}")
    print(f"HALT: {msg}", flush=True); sys.exit(1)


def _push(msg: str):
    subprocess.run(["git", "add", "exp08/exp19_corridor_log.json"] +
                   [str(p.relative_to(ROOT / "experiments/05_attention_sculpting"))
                    for p in XA.OUTDIR.glob(f"*_{TAG}*.json")] +
                   [str(p.relative_to(ROOT / "experiments/05_attention_sculpting"))
                    for p in XA.OUTDIR.glob("exp19_g9_*.json")],
                   cwd=ROOT / "experiments/05_attention_sculpting", capture_output=True)
    subprocess.run(["git", "commit", "--author=Jason Dury <jason@eridos.ai>", "-m", msg],
                   cwd=ROOT, capture_output=True)
    r = subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
    print(f"[push] {msg} ({'ok' if r.returncode == 0 else 'PUSH FAIL'})", flush=True)


def _run_one(arm: str, seed: int) -> dict:
    t0 = time.time()
    rec, po = REP.capture_run(arm, seed, read_at=READ_AT, h_max=H_MAX, out_tag=TAG)
    loop, _s, _c = X12.build_exp12(arm, seed, H_MAX)     # fabric rebuild for the stratifier (deterministic)
    zpm = S19._zero_preceding(loop.stream.dwell_id[:READ_AT], loop.stream.is_exam[:READ_AT])
    acq = rec["acquisition_onset"]
    full = [[int(w), float(a)] for (w, _d, _p, a) in po if w < READ_AT]
    strat = [[w, a] for (w, a) in full if bool(zpm[w])]
    win: dict = {}
    for w, a in full:
        if w >= acq:
            win.setdefault((w // 300 + 1) * 300, []).append(a)
    cols = [[c["t"], c.get("dec_cat"), c.get("exam_acc")] for c in rec["columns"]]
    (XA.OUTDIR / f"exp19_g9_{arm}_s{seed}_series.json").write_text(json.dumps(
        dict(arm=arm, seed=seed, acq=acq, strat_onsets=strat, cols=cols,
             full_win300={str(t): [len(v), round(sum(v) / len(v), 6)] for t, v in win.items()})))
    row = dict(arm=arm, seed=seed, acq=acq, n_full=len(full), n_strat=len(strat),
               wall_s=round(time.time() - t0, 1))
    STATE["runs"].append(row); _save()
    print(f"  run {arm} s{seed}: acq={acq} n_full={len(full)} n_strat={len(strat)} {row['wall_s']}s", flush=True)
    return dict(acq=acq, full=full, strat=strat)


def _certify_full300(d: dict, seed: int) -> bool:
    r = SC._certify_seed(d["full"], d["acq"], 300, torch.Generator().manual_seed(FL.SIM_SEED + int(seed)))
    return r["certified"]


def main():
    torch.set_num_threads(1)
    print("=== EXP19 CORRIDOR OPEN (G8 ratified against a9adb12) — 39 runs ===", flush=True)
    data: dict = {}
    # ---- PHASE CAL (15 runs)
    for B, arm in ARMS.items():
        for s in CAL_SEEDS:
            data[(arm, s)] = _run_one(arm, s)
    _push("EXP19 corridor — CAL phase closed (15 runs, capture + derived series)")
    # ---- PHASE OPS (G7 per B, both reads)
    for B, arm in ARMS.items():
        conv = [s for s in CAL_SEEDS if _certify_full300(data[(arm, s)], s)]
        nonconv = [s for s in CAL_SEEDS if s not in conv]
        if not conv:
            _halt(f"{arm}: NO cal converter at width 300 — no known signal; underpower gate unevaluable -> Jason")
        if not nonconv:
            _halt(f"{arm}: ALL cal seeds convert — no phantom floor exists; Ruling-B-class state -> Jason")
        ops = {}
        for read in ("full", "stratified"):
            cd = {s: (data[(arm, s)]["acq"], data[(arm, s)]["full" if read == "full" else "strat"])
                  for s in CAL_SEEDS}
            cal = CAL.cal_floor_audit(arm, read, conv, nonconv, data=cd)
            if cal["underpowered"]:
                _halt(f"{arm}/{read}: STRATUM-UNDERPOWER — {cal['VERDICT']}")
            usable = [r for r in cal["sweep"] if r["all_clear"]]
            top = max(r["separation"] for r in usable)
            if sum(1 for r in usable if r["separation"] == top) > 1:
                _halt(f"{arm}/{read}: G7 INTEGER-TIE at max separation {top} "
                      f"(widths {[r['width'] for r in usable if r['separation'] == top]}) -> Jason rules the tie-break")
            ops[read] = cal
            print(f"  G7 {arm}/{read}: conv={conv} op={cal['operating_point_width']} "
                  f"wfloor={cal['w_width_floor']} robust={cal['operating_point']['all_clear_robust']}", flush=True)
        STATE["ops"][arm] = {r: dict(op=ops[r]["operating_point_width"], w_floor=ops[r]["w_width_floor"],
                                     conv=conv, nonconv=nonconv,
                                     curve=[[x["width"], x["separation"], x["all_clear"]] for x in ops[r]["sweep"]])
                             for r in ops}
        (XA.OUTDIR / f"exp19_g9_{arm}_ops.json").write_text(json.dumps(
            dict(arm=arm, conv=conv, nonconv=nonconv, full=ops["full"], stratified=ops["stratified"]), indent=2))
        _save()
    _push("EXP19 corridor — G7 ops closed (per-B widths cut on own nulls; full curves; no ties)")
    # ---- PHASE VERDICT (24 runs) + scoring per B
    for B, arm in ARMS.items():
        for s in VERDICT_SEEDS:
            data[(arm, s)] = _run_one(arm, s)
        wf, ws = STATE["ops"][arm]["full"]["op"], STATE["ops"][arm]["stratified"]["op"]
        df = {s: (data[(arm, s)]["acq"], data[(arm, s)]["full"]) for s in VERDICT_SEEDS}
        ds = {s: (data[(arm, s)]["acq"], data[(arm, s)]["strat"]) for s in VERDICT_SEEDS}
        full = SC.score_arm(arm, "full", VERDICT_SEEDS, wf, data=df)
        strat = SC.score_arm(arm, "stratified", VERDICT_SEEDS, ws, data=ds)
        carried, survives, strat_only = SC._recency_test(full["certified_seeds"], strat["certified_seeds"])
        if strat_only:
            _halt(f"{arm}: STRATIFIED-ONLY certification {strat_only} — not a modeled §7 cell -> Jason")
        comp = {}
        for s in VERDICT_SEEDS:
            rec = XA._truncate(json.loads((XA.OUTDIR / f"exp14_{arm}_s{s}_{TAG}.json").read_text()), READ_AT)
            g = X16._recency_gradient(rec)
            dc = [c["dec_cat"] for c in rec["columns"]
                  if c.get("dec_cat") is not None and c["t"] >= (rec["acquisition_onset"] or 0)]
            comp[s] = dict(grad=g["delta"], dec_cat=round(sum(dc) / len(dc), 4) if dc else None)
        v = dict(arm=arm, B=B, full=dict(k=full["k"], certified=full["certified_seeds"], op=wf),
                 stratified=dict(k=strat["k"], certified=strat["certified_seeds"], op=ws),
                 recency_carried=carried, survives_stratified=survives, companions=comp)
        STATE["verdicts"][arm] = v; _save()
        (XA.OUTDIR / f"exp19_g9_{arm}_verdict.json").write_text(json.dumps(
            dict(**v, full_per_seed=full["per_seed"], strat_per_seed=strat["per_seed"]), indent=2))
        print(f"  VERDICT {arm}: full {full['k']}/8 {full['certified_seeds']} | strat {strat['k']}/8 "
              f"{strat['certified_seeds']} | carried {carried}", flush=True)
        _push(f"EXP19 corridor — {arm} verdict closed (full {full['k']}/8, strat {strat['k']}/8)")
    # ---- B* bracket (v5 A8; both reads reported, read-choice -> Jason at terminal)
    for read in ("full", "stratified"):
        c = {1: 0, **{B: STATE["verdicts"][ARMS[B]][read if read == "full" else "stratified"]["k"]
                      for B in ARMS}, "T": 5}
        STATE.setdefault("bstar", {})[read] = c
    _save()
    _push("EXP19 corridor — CLOSED: 39 runs, ops, verdicts, B* curves. Terminal read -> Jason")
    print("=== CORRIDOR COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
