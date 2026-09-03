"""exp19_tails.py — Phase-2 of the ratified EXP19 close-out (Jason 2026-07-20): the descriptive tails.

Resume the §3-designated blind tail seeds — verdict {0,1,2,3}, rule-drawn, never by hand (the ec8121a
horizon amendment's designation) — from their 500k `.ckpt_read.pt` checkpoints to 1M, for exp19_wperm_B128
and exp19_wperm_B512 (8 tails). B=32 is WAIVED with record (Jason's word; grounds: three certified-dead
decades below the knee, lowest information per run). Capture harness ON (per-onset tail via the replay
monkeypatch); checkpoint contract: `.ckpt_1M.pt` at the horizon.

FIDELITY OUTCOME (the anchor discipline did its job): `--smoke` CAUGHT the ruled resume as UNFAITHFUL —
resumed weights diverge from a from-scratch run, and three targeted state transplants did not close the
gap. The committed save_checkpoint docstring's "sufficient to resume" claim is thereby FALSIFIED (standing
instrument flag for the close). The _resume/_smoke code is RETAINED as the evidence instrument; run() uses
the committed ec8121a mechanics instead ("Full runs from the start; no checkpoint-resume anywhere"):
from-scratch read_at=1M runs, PREFIX-ANCHORED digit-exact against the committed g9 records. Deviation from
the Phase-2 instruction's stated mechanics recorded for Jason's Phase-3 word.

READ (LATE-RESCUE-IN-TAIL, the ONLY cell — v5 A10): descriptive per-seed tail numbers at the committed
detector (band 0.64; the arm's own tail column grid): longest tail run, band touches, exam_acc / dec_cat
tail means. Enters NO bracket, NO estimator, NO cross-arm sentence.
"""
from __future__ import annotations

import json
import sys
import time

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp19_replay as REP

EVAL, BLOCK = XA.EVAL, XA.BLOCK
READ_AT, H_MAX, BAND = 500_000, 1_000_000, 0.64
ARMS = ["exp19_wperm_B128", "exp19_wperm_B512"]
TAIL_SEEDS = [0, 1, 2, 3]                     # §3-designated (ec8121a): verdict {0,1,2,3} — rule-drawn
WAIVER = ("B=32 WAIVED (Jason 2026-07-20, with record): three certified-dead decades below the knee "
          "(c=0 at 32/128 both reads; B* > 128), lowest information per run.")
for _a in ARMS:
    X12.exp19_wperm(int(_a.split("_B")[1]))   # register arms


def _resume(arm: str, seed: int, from_t: int, to_t: int, ckpt_path, out_tag: str) -> dict:
    """Faithful continuation of run_exp14_arm's loop body from a checkpoint, capture installed."""
    loop, spec, cfg = X12.build_exp12(arm, seed, to_t)
    ck = torch.load(ckpt_path, weights_only=False)
    loop.vision.load_state_dict(ck["vision"]); loop.word.load_state_dict(ck["word"])
    loop.op.load_state_dict(ck["op"]); loop.opt.load_state_dict(ck["opt"])
    loop.gen.set_state(ck["gen_state"]); loop._t = ck["t"]
    assert ck["t"] == from_t, f"checkpoint t {ck['t']} != expected {from_t}"
    fab = loop.stream
    members_a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    members_b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    labels = loop._word_label(members_b, members_a)
    no_word = bool(spec.get("no_word", False))
    REP._CAPTURE, REP._PERTURB = [], None
    X12._buffer_wave = REP._capturing_buffer_wave
    buf = X12._fresh_buf()
    cols = []
    first_eval = ((from_t // EVAL) + 1) * EVAL
    try:
        for t in range(from_t + 1, to_t + 1):
            prev = t - 1
            pl = X12._probe_exam_read(loop, prev) if bool(fab.is_probe_exam[prev]) else None
            loop.step(no_word=no_word)
            X12._buffer_wave(loop, prev, buf, probe_lift=pl, probe_midword=None)
            if t % EVAL == 0:
                c = X12._eval_column(loop, t, buf, members_a, members_b, labels, no_word=no_word)
                if t == first_eval and from_t % EVAL != 0:
                    c["seam"] = True                          # partial buffer (from_t not on the EVAL grid)
                cols.append(c)
                buf = X12._fresh_buf()
        per_onset = list(REP._CAPTURE)
    finally:
        X12._buffer_wave = REP._orig_buffer_wave
    base = XA.OUTDIR / f"exp14_{arm}_s{seed}_{out_tag}"
    XA.save_checkpoint(loop, base.with_suffix(".ckpt_1M.pt"), arm=arm, seed=seed,
                       event="tail_horizon", read_at=to_t)    # the checkpoint contract, at horizon
    return dict(cols=cols, per_onset=per_onset, final_w={m: getattr(loop, m).state_dict()
                                                         for m in ("vision", "op", "word")})


def _tail_read(cols: list) -> dict:
    """Descriptive-only (LATE-RESCUE-IN-TAIL). Tail = post-seam columns in (500k, 1M]."""
    tail = [c for c in cols if not c.get("seam")]
    accs = [c.get("exam_acc") for c in tail]
    run = best = 0
    touches = 0
    for a in accs:
        hit = a is not None and a >= BAND
        touches += int(hit)
        run = run + 1 if hit else 0
        best = max(best, run)
    dc = [c["dec_cat"] for c in tail if c.get("dec_cat") is not None]
    ea = [a for a in accs if a is not None]
    return dict(n_tail_cols=len(tail), longest_band_run=best, band_touch_cols=touches,
                exam_acc_tail_mean=(round(sum(ea) / len(ea), 4) if ea else None),
                dec_cat_tail_mean=(round(sum(dc) / len(dc), 4) if dc else None))


def smoke():
    """Full-vs-resume fidelity at short horizon, seam INCLUDED (N=3100 not on the EVAL grid)."""
    torch.set_num_threads(1)
    N, M = 3100, 6200
    arm = ARMS[0]
    print("tail-resume SMOKE: full run to %d vs ckpt@%d resume -> %d" % (M, N, M), flush=True)
    rec, po_full = REP.capture_run(arm, 0, read_at=M, h_max=M, out_tag="tsmk_full")
    rec2, _ = REP.capture_run(arm, 0, read_at=N, h_max=M, out_tag="tsmk_half")
    r = _resume(arm, 0, N, M, XA.OUTDIR / f"exp14_{arm}_s0_tsmk_half.ckpt_read.pt", "tsmk_res")
    lf, _s, _c = X12.build_exp12(arm, 0, M)                  # fresh loop to load full-run final weights
    ckf = torch.load(XA.OUTDIR / f"exp14_{arm}_s0_tsmk_full.ckpt_read.pt", weights_only=False)
    for m in ("vision", "op", "word"):
        a, b = ckf[m], r["final_w"][m]
        assert set(a) == set(b) and all(torch.equal(a[k], b[k]) for k in a), f"WEIGHTS diverge in {m}"
    tail_full = [(w, a) for (w, _d, _p, a) in po_full if w >= N]
    tail_res = [(w, a) for (w, _d, _p, a) in r["per_onset"]]
    assert tail_full == tail_res, f"per-onset tails differ ({len(tail_full)} vs {len(tail_res)})"
    full_cols = {c["t"]: c for c in rec["columns"] if c["t"] > N}
    seam_t = ((N // EVAL) + 1) * EVAL
    for c in r["cols"]:
        if c.get("seam"):
            assert c["t"] == seam_t
            continue                                          # the seam column is EXCLUDED from fidelity
        fc = full_cols[c["t"]]
        assert all(fc.get(k) == c.get(k) or (isinstance(fc.get(k), float) and
                   abs(fc[k] - c[k]) < 1e-12) for k in fc if k != "seam"), f"column {c['t']} differs"
    print("SMOKE PASS: resumed trajectory bit-identical (weights + per-onset tail + all post-seam "
          "columns); the single seam column is marked and excluded, as designed.", flush=True)


def run():
    """MECHANICS DEVIATION, recorded for Jason's Phase-3 word: the ruled resume-from-checkpoint FAILED its
    own fidelity smoke (resumed weights diverge from a from-scratch run; three targeted state transplants
    did not close it — the committed save_checkpoint's "sufficient to resume" claim is FALSIFIED by this
    smoke; forensics recorded in the close-out report, not resolved here). The COMMITTED ec8121a rule
    governs instead: "Full runs from the start; no checkpoint-resume anywhere." Each tail is a from-scratch
    deterministic read_at=1M run, PREFIX-ANCHORED: its [0,500k) columns must be digit-exact against the
    committed g9 record (a STRONGER anchor than resume). No seam exists on this path."""
    torch.set_num_threads(1)
    out = dict(cell="LATE-RESCUE-IN-TAIL (descriptive-only; v5 A10; enters no bracket/estimator/"
                    "cross-arm sentence)", designation="§3 blind tail seeds {0,1,2,3} (ec8121a rule)",
               waiver=WAIVER, band=BAND,
               mechanics="from-scratch read_at=1M per ec8121a (resume failed its fidelity smoke; "
                         "prefix-anchored to the committed g9 records)", per_arm={})
    for arm in ARMS:
        out["per_arm"][arm] = {}
        for s in TAIL_SEEDS:
            t0 = time.time()
            rec, po = REP.capture_run(arm, s, read_at=H_MAX, h_max=H_MAX, out_tag="g9tail")
            com = json.loads((XA.OUTDIR / f"exp14_{arm}_s{s}_g9.json").read_text())
            cc = {c["t"]: c for c in com["columns"]}
            for c in rec["columns"]:
                if c["t"] > READ_AT:
                    break
                ref = cc[c["t"]]
                for k, v in ref.items():
                    assert c.get(k) == v, (f"PREFIX ANCHOR FAIL {arm} s{s} col {c['t']} field {k}: "
                                           f"tail-run {c.get(k)!r} != committed {v!r} — HALT")
            tail_cols = [c for c in rec["columns"] if c["t"] > READ_AT]
            (XA.OUTDIR / f"exp19_g9tail_{arm}_s{s}_series.json").write_text(json.dumps(
                dict(arm=arm, seed=s, mechanics="from-scratch 1M, prefix-anchored",
                     cols=[[c["t"], c.get("dec_cat"), c.get("exam_acc"), False] for c in tail_cols],
                     tail_onsets=[[int(w), float(a)] for (w, _d, _p, a) in po if w >= READ_AT])))
            rd = _tail_read(tail_cols)
            out["per_arm"][arm][s] = dict(**rd, prefix_anchor="digit-exact vs committed g9 record")
            print(f"  {arm} s{s}: PREFIX-ANCHOR OK | run {rd['longest_band_run']} touches "
                  f"{rd['band_touch_cols']} exam_tail {rd['exam_acc_tail_mean']} dec_cat "
                  f"{rd['dec_cat_tail_mean']} ({round(time.time()-t0, 1)}s)", flush=True)
    (XA.OUTDIR / "exp19_g9_tails.json").write_text(json.dumps(out, indent=2))
    print("TAILS COMPLETE -> exp19_g9_tails.json", flush=True)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        smoke()
    else:
        run()
