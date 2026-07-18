"""exp19_corridor_resume.py — SPLIT ruling (Jason 2026-07-18). B=512 resumes under the ratified law
unchanged; B=32/128 verdicts run at width 300 IFF the small-B detector-power certification PASSED
(exp19_g9_smallB_powercert.json — G5b machinery on committed C data), else HALT -> Jason.
Cal recaptures for B512 are deterministic re-runs (full per-onset was not persisted by the first driver;
series now persist full_onsets too). Fences live; auto-push per closed gate; cal table -> no prose."""
from __future__ import annotations
import json, subprocess, sys, time
import torch
import exp12_arms as X12, exp14_arms as XA, exp16_score as X16
import exp19_cal as CAL, exp19_floor as FL, exp19_replay as REP, exp19_score as S19, exp19_scorer as SC

ROOT = XA.OUTDIR.parent.parent.parent
ARM512, SMALL = X12.exp19_wperm(512), [X12.exp19_wperm(32), X12.exp19_wperm(128)]
CAL_SEEDS, V_SEEDS = [20, 21, 22, 24, 25], list(range(8))
READ_AT, H_MAX, TAG = 500_000, 1_000_000, "g9"
LOG = XA.OUTDIR / "exp19_corridor_log.json"
STATE = json.loads(LOG.read_text())


def _save(): LOG.write_text(json.dumps(STATE, indent=2))


def _push(msg):
    subprocess.run(["git", "add", "-A", "experiments/05_attention_sculpting/exp08"], cwd=ROOT, capture_output=True)
    subprocess.run(["git", "commit", "--author=Jason Dury <jason@eridos.ai>", "-m", msg], cwd=ROOT, capture_output=True)
    r = subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
    print(f"[push] {msg} ({'ok' if r.returncode == 0 else 'FAIL'})", flush=True)


def _halt(msg):
    STATE.setdefault("halts", []).append(msg); _save(); _push(f"EXP19 corridor HALT — {msg[:60]}")
    print("HALT: " + msg, flush=True); sys.exit(1)


def _run_one(arm, seed):
    t0 = time.time()
    rec, po = REP.capture_run(arm, seed, read_at=READ_AT, h_max=H_MAX, out_tag=TAG)
    loop, _s, _c = X12.build_exp12(arm, seed, H_MAX)
    zpm = S19._zero_preceding(loop.stream.dwell_id[:READ_AT], loop.stream.is_exam[:READ_AT])
    acq = rec["acquisition_onset"]
    full = [[int(w), float(a)] for (w, _d, _p, a) in po if w < READ_AT]
    strat = [[w, a] for (w, a) in full if bool(zpm[w])]
    cols = [[c["t"], c.get("dec_cat"), c.get("exam_acc")] for c in rec["columns"]]
    (XA.OUTDIR / f"exp19_g9_{arm}_s{seed}_series.json").write_text(json.dumps(
        dict(arm=arm, seed=seed, acq=acq, full_onsets=full, strat_onsets=strat, cols=cols)))
    print(f"  run {arm} s{seed}: acq={acq} nf={len(full)} ns={len(strat)} {round(time.time()-t0,1)}s", flush=True)
    return dict(acq=acq, full=full, strat=strat)


def _cert300(d, s):
    return SC._certify_seed(d["full"], d["acq"], 300, torch.Generator().manual_seed(FL.SIM_SEED + s))["certified"]


def _verdict(arm, wf, ws, data):
    df = {s: (data[s]["acq"], data[s]["full"]) for s in V_SEEDS}
    ds = {s: (data[s]["acq"], data[s]["strat"]) for s in V_SEEDS}
    full = SC.score_arm(arm, "full", V_SEEDS, wf, data=df)
    strat = SC.score_arm(arm, "stratified", V_SEEDS, ws, data=ds)
    carried, survives, so = SC._recency_test(full["certified_seeds"], strat["certified_seeds"])
    if so: _halt(f"{arm}: STRATIFIED-ONLY certification {so} -> Jason")
    comp = {}
    for s in V_SEEDS:
        rec = XA._truncate(json.loads((XA.OUTDIR / f"exp14_{arm}_s{s}_{TAG}.json").read_text()), READ_AT)
        g = X16._recency_gradient(rec)
        dc = [c["dec_cat"] for c in rec["columns"] if c.get("dec_cat") is not None and c["t"] >= rec["acquisition_onset"]]
        comp[s] = dict(grad=g["delta"], dec_cat=round(sum(dc) / len(dc), 4) if dc else None)
    v = dict(arm=arm, full=dict(k=full["k"], certified=full["certified_seeds"], op=wf),
             stratified=dict(k=strat["k"], certified=strat["certified_seeds"], op=ws),
             recency_carried=carried, survives_stratified=survives, companions=comp)
    STATE.setdefault("verdicts", {})[arm] = v; _save()
    (XA.OUTDIR / f"exp19_g9_{arm}_verdict.json").write_text(json.dumps(
        dict(**v, full_per_seed=full["per_seed"], strat_per_seed=strat["per_seed"]), indent=2))
    print(f"  VERDICT {arm}: full {full['k']}/8 {full['certified_seeds']} | strat {strat['k']}/8 "
          f"{strat['certified_seeds']} | carried {carried}", flush=True)


def main():
    torch.set_num_threads(1)
    print("=== CORRIDOR RESUME (SPLIT): B512 under the ratified law; small-B gated on powercert ===", flush=True)
    # B512 cal recapture (deterministic; full per-onset regained)
    cd = {s: _run_one(ARM512, s) for s in CAL_SEEDS}
    conv = [s for s in CAL_SEEDS if _cert300(cd[s], s)]
    nonconv = [s for s in CAL_SEEDS if s not in conv]
    if not conv or not nonconv: _halt(f"{ARM512}: cal label edge state {conv}/{nonconv} -> Jason")
    ops = {}
    for read in ("full", "stratified"):
        dd = {s: (cd[s]["acq"], cd[s]["full" if read == "full" else "strat"]) for s in CAL_SEEDS}
        cal = CAL.cal_floor_audit(ARM512, read, conv, nonconv, data=dd)
        if cal["underpowered"]: _halt(f"{ARM512}/{read}: STRATUM-UNDERPOWER -> Jason")
        usable = [r for r in cal["sweep"] if r["all_clear"]]
        top = max(r["separation"] for r in usable)
        if sum(1 for r in usable if r["separation"] == top) > 1:
            _halt(f"{ARM512}/{read}: G7 INTEGER-TIE at {top} -> Jason rules the tie-break")
        ops[read] = cal
        print(f"  G7 {ARM512}/{read}: conv={conv} op={cal['operating_point_width']} "
              f"robust={cal['operating_point']['all_clear_robust']}", flush=True)
    STATE.setdefault("ops", {})[ARM512] = {r: dict(op=ops[r]["operating_point_width"],
                                                   w_floor=ops[r]["w_width_floor"], conv=conv, nonconv=nonconv)
                                           for r in ops}
    (XA.OUTDIR / f"exp19_g9_{ARM512}_ops.json").write_text(json.dumps(
        dict(arm=ARM512, conv=conv, nonconv=nonconv, full=ops["full"], stratified=ops["stratified"]), indent=2))
    _save(); _push("EXP19 corridor — B512 G7 ops closed (own null; full curves; no tie)")
    vd = {s: _run_one(ARM512, s) for s in V_SEEDS}
    _verdict(ARM512, STATE["ops"][ARM512]["full"]["op"], STATE["ops"][ARM512]["stratified"]["op"], vd)
    _push(f"EXP19 corridor — B512 verdict closed")
    # small-B: gated on the power certification
    cert = json.loads((XA.OUTDIR / "exp19_g9_smallB_powercert.json").read_text())
    if not all(v["all_ge_90"] for v in cert["results"].values()):
        _halt(f"small-B detector-power certification FAILED ({cert['results']}) — the small-B design is in question -> Jason")
    print("  small-B powercert PASS — B32/B128 verdicts at width 300 (committed instrument width)", flush=True)
    for arm in SMALL:
        vd = {s: _run_one(arm, s) for s in V_SEEDS}
        _verdict(arm, 300, 300, vd)
        _push(f"EXP19 corridor — {arm} verdict closed (width 300 per SPLIT ruling)")
    for read in ("full", "stratified"):
        STATE.setdefault("bstar", {})[read] = {1: 0, **{a.split("_B")[1]: STATE["verdicts"][a][read]["k"]
                                               for a in STATE["verdicts"]}, "T": 5}
    _save(); _push("EXP19 corridor — CLOSED (SPLIT executed): verdicts + B* curves. Terminal -> Jason")
    print("=== CORRIDOR COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
