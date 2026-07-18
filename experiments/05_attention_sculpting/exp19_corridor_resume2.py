"""exp19_corridor_resume2.py — recovery: the resume driver was OOM-killed mid-B32 verdicts (silent SIGKILL,
no traceback; B512 ops+verdict CLOSED and pushed before it). Completed runs reload from their persisted
series (full_onsets present — deterministic, never re-run); only the missing runs execute. Memory-lean:
one seed in flight at a time, per-arm data released after scoring."""
from __future__ import annotations
import gc, json, subprocess, sys, time
import torch
import exp12_arms as X12, exp14_arms as XA, exp16_score as X16
import exp19_floor as FL, exp19_replay as REP, exp19_score as S19, exp19_scorer as SC

ROOT = XA.OUTDIR.parent.parent.parent
SMALL = [X12.exp19_wperm(32), X12.exp19_wperm(128)]
V_SEEDS = list(range(8))
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


def _get(arm, seed):
    p = XA.OUTDIR / f"exp19_g9_{arm}_s{seed}_series.json"
    if p.exists():
        d = json.loads(p.read_text())
        if "full_onsets" in d:
            print(f"  reload {arm} s{seed} (series on disk)", flush=True)
            return dict(acq=d["acq"], full=d["full_onsets"], strat=d["strat_onsets"])
    t0 = time.time()
    rec, po = REP.capture_run(arm, seed, read_at=READ_AT, h_max=H_MAX, out_tag=TAG)
    loop, _s, _c = X12.build_exp12(arm, seed, H_MAX)
    zpm = S19._zero_preceding(loop.stream.dwell_id[:READ_AT], loop.stream.is_exam[:READ_AT])
    del loop
    acq = rec["acquisition_onset"]
    full = [[int(w), float(a)] for (w, _d, _p, a) in po if w < READ_AT]
    strat = [[w, a] for (w, a) in full if bool(zpm[w])]
    cols = [[c["t"], c.get("dec_cat"), c.get("exam_acc")] for c in rec["columns"]]
    p.write_text(json.dumps(dict(arm=arm, seed=seed, acq=acq, full_onsets=full, strat_onsets=strat, cols=cols)))
    del rec, po, zpm
    gc.collect()
    print(f"  run {arm} s{seed}: acq={acq} nf={len(full)} ns={len(strat)} {round(time.time()-t0,1)}s", flush=True)
    return dict(acq=acq, full=full, strat=strat)


def main():
    torch.set_num_threads(1)
    print("=== CORRIDOR RESUME-2 (recovery; small-B verdicts at width 300 per SPLIT + powercert PASS) ===",
          flush=True)
    cert = json.loads((XA.OUTDIR / "exp19_g9_smallB_powercert.json").read_text())
    assert all(v["all_ge_90"] for v in cert["results"].values()), "powercert not PASS — must not be here"
    for arm in SMALL:
        data = {}
        for s in V_SEEDS:
            data[s] = _get(arm, s)
        df = {s: (data[s]["acq"], data[s]["full"]) for s in V_SEEDS}
        ds = {s: (data[s]["acq"], data[s]["strat"]) for s in V_SEEDS}
        full = SC.score_arm(arm, "full", V_SEEDS, 300, data=df)
        strat = SC.score_arm(arm, "stratified", V_SEEDS, 300, data=ds)
        carried, survives, so = SC._recency_test(full["certified_seeds"], strat["certified_seeds"])
        if so: _halt(f"{arm}: STRATIFIED-ONLY certification {so} -> Jason")
        comp = {}
        for s in V_SEEDS:
            rec = XA._truncate(json.loads((XA.OUTDIR / f"exp14_{arm}_s{s}_{TAG}.json").read_text()), READ_AT)
            g = X16._recency_gradient(rec)
            dc = [c["dec_cat"] for c in rec["columns"]
                  if c.get("dec_cat") is not None and c["t"] >= rec["acquisition_onset"]]
            comp[s] = dict(grad=g["delta"], dec_cat=round(sum(dc) / len(dc), 4) if dc else None)
            del rec
        v = dict(arm=arm, full=dict(k=full["k"], certified=full["certified_seeds"], op=300),
                 stratified=dict(k=strat["k"], certified=strat["certified_seeds"], op=300),
                 recency_carried=carried, survives_stratified=survives, companions=comp,
                 width_grounds="width 300 per SPLIT ruling (committed instrument width; powercert PASS)")
        STATE.setdefault("verdicts", {})[arm] = v; _save()
        (XA.OUTDIR / f"exp19_g9_{arm}_verdict.json").write_text(json.dumps(
            dict(**v, full_per_seed=full["per_seed"], strat_per_seed=strat["per_seed"]), indent=2))
        print(f"  VERDICT {arm}: full {full['k']}/8 {full['certified_seeds']} | strat {strat['k']}/8 "
              f"{strat['certified_seeds']} | carried {carried}", flush=True)
        _push(f"EXP19 corridor — {arm} verdict closed (width 300 per SPLIT ruling)")
        del data, df, ds, full, strat
        gc.collect()
    for read in ("full", "stratified"):
        STATE.setdefault("bstar", {})[read] = {"1": 0, **{a.split("_B")[1]: STATE["verdicts"][a][read]["k"]
                                               for a in STATE["verdicts"]}, "T": 5}
    _save(); _push("EXP19 corridor — CLOSED (SPLIT executed): all verdicts + B* curves. Terminal -> Jason")
    print("=== CORRIDOR COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
