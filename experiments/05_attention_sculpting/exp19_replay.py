"""exp19_replay.py — EXP19 per-onset capture harness (FOUNDATIONAL; serves G5a AND the treatment).

WHY A REPLAY, NOT A FROZEN-CHECKPOINT EVAL (Jason ruling, 2026-07-14 — the trap CC stopped in front of):
  The committed conversion signal is an EVOLVING-WEIGHT trajectory — each committed column's exam_acc
  is the per-window MEAN of live per-onset exam_acc computed from the SAME training forward that step()
  ran (exp12_arms._buffer_wave: `lift, acc = exam_lift(...)` -> buf["exam_acc"].append(acc), then
  _eval_column means it). The read-checkpoint at read_at=500k is a snapshot that has REVERTED toward
  chance (tail-50 mean acc ~= 0.48-0.62 on EVERY seed incl. the converters); a frozen-weight eval from
  it returns ~chance for all seeds -> nothing certifies -> a WRONG-REASON all-seeds-fail. The faithful
  per-onset signal is only recoverable by a DETERMINISTIC REPLAY of the committed run, capturing the
  per-onset exam_acc the run averaged away.

WHAT THE CAPTURE IS (non-perturbing by construction):
  A read-only wrapper on X12._buffer_wave. It records the value _buffer_wave ITSELF appends to
  buf["exam_acc"] (the committed per-onset acc), tagged with (wave, dwell_id, pos). It draws no RNG,
  touches no parameter, mutates no run state -> the trajectory is byte-identical. That claim is PROVEN,
  not asserted, by the checkpoint anchor (Jason ruling 2 — "bit-exact reproduction of .ckpt_read.pt
  including gen_state proves the harness is non-perturbing; it comes free"):
    A1 bit-exact:   replay .ckpt_read.pt == committed verdict .ckpt_read.pt  (every tensor incl.
                    gen_state; t == read_at). Cross-commit (committed @396c0a7, replay @HEAD) so A1 ALSO
                    certifies B1's shuffle-path refactor did not perturb exp12_shuffle.
    A2 columns:     replay per-window exam_acc == committed columns  (digit-exact)
    A3 consistency: re-bin captured per-onset -> 300-step windows -> means == committed columns
                    (digit-exact) — proves the CAPTURE recovered exactly the averaged values.

RED-TEAM (Jason ruling 2 — an anchor that has never failed is G0b v1 again): _redteam() proves both
  anchors are reachable falsifiers — a capture that SHIFTS A DRAW reddens A1; a CORRUPTED capture
  reddens A3; the clean capture is green.

Report-don't-patch / supersede-don't-overwrite: this file edits NO committed code. run_exp14_arm is
called verbatim with an out_tag, so every artifact lands under a *_<tag>.* basename and the committed
*_verdict.* records/checkpoints are never touched.
"""
from __future__ import annotations

import json
from pathlib import Path

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp19_score as S19

EVAL = XA.EVAL                       # 300 — the committed eval cadence
READ_AT = 500_000
H_MAX = 1_000_000

# ---------------------------------------------------------------- the read-only capture wrapper
_CAPTURE: list = []                  # per-run: (wave, dwell_id, pos, acc)
_PERTURB = None                      # None | "shift_draw" — RED-TEAM only
_orig_buffer_wave = X12._buffer_wave


def _capturing_buffer_wave(loop, t, buf, probe_lift=None, probe_midword=None):
    """Byte-inert wrapper: call the committed _buffer_wave unchanged, then read the value it just
    appended to buf["exam_acc"] (if any). Pure read of buf + fab -> no RNG, no param, no state touch.

    _PERTURB == "shift_draw" is the RED-TEAM saboteur ONLY: it consumes one draw from loop.gen (the
    checkpointed training generator), which desyncs the trajectory and MUST redden A1 — the proof the
    anchor can catch a perturbing capture."""
    if _PERTURB == "shift_draw":
        torch.rand((), generator=loop.gen)               # deliberate sabotage — reddens A1
    n_before = len(buf["exam_acc"])
    _orig_buffer_wave(loop, t, buf, probe_lift=probe_lift, probe_midword=probe_midword)
    if len(buf["exam_acc"]) > n_before:                  # this wave contributed an onset exam_acc
        fab = loop.stream
        _CAPTURE.append((int(t), int(fab.dwell_id[t]), int(fab.pos[t]), float(buf["exam_acc"][-1])))


def capture_run(arm: str, seed: int, *, read_at: int = READ_AT, h_max: int = H_MAX,
                out_tag: str, perturb: str | None = None) -> tuple[dict, list]:
    """Deterministic replay of run_exp14_arm(arm, seed) with the per-onset capture installed.
    Returns (record, per_onset_list). out_tag redirects ALL artifacts away from *_verdict.*."""
    global _CAPTURE, _PERTURB
    torch.set_num_threads(1)                             # determinism (committed runs: torch_num_threads=1)
    _CAPTURE, _PERTURB = [], perturb
    X12._buffer_wave = _capturing_buffer_wave
    try:
        rec = XA.run_exp14_arm(arm, seed, read_at=read_at, h_max=h_max,
                               out_tag=out_tag, checkpoint=True, mid_ckpt_at=None)
    finally:
        X12._buffer_wave = _orig_buffer_wave
        _PERTURB = None
    return rec, list(_CAPTURE)


# ---------------------------------------------------------------- anchors (the safety argument)
def _tensors_equal(a, b, path=""):
    """Deep bit-exact compare of checkpoint state-dicts / tensors / nested dicts. First divergence."""
    if isinstance(a, torch.Tensor) and isinstance(b, torch.Tensor):
        if a.shape != b.shape or a.dtype != b.dtype:
            return f"{path}: shape/dtype {tuple(a.shape)}/{a.dtype} != {tuple(b.shape)}/{b.dtype}"
        return None if torch.equal(a, b) else f"{path}: tensor values differ"
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return f"{path}: dict keys differ ({set(a) ^ set(b)})"
        for k in a:
            d = _tensors_equal(a[k], b[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return f"{path}: len {len(a)} != {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = _tensors_equal(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{path}: {a!r} != {b!r}"


def _bin_windows(per_onset: list, read_at: int = READ_AT) -> dict:
    """Re-bin captured per-onset acc into the committed 300-step windows. window(wave) = the column t
    that flushes the buffer holding it = (wave//EVAL + 1)*EVAL. Returns {col_t: [acc, ...]}."""
    win: dict = {}
    for (wave, _dw, _pos, acc) in per_onset:
        col_t = (wave // EVAL + 1) * EVAL
        if col_t <= read_at:
            win.setdefault(col_t, []).append(acc)
    return win


def _fmt6g(x: float) -> float:
    return float(f"{x:.6g}")


def verify_anchors(arm: str, seed: int, replay_tag: str, per_onset: list,
                   replay_rec: dict, verdict_tag: str = "verdict") -> dict:
    """A1 bit-exact ckpt vs committed; A2 replay columns == committed columns; A3 re-binned capture ==
    committed columns. All keyed to the COMMITTED *_verdict.* record. Returns a pass/fail report."""
    import statistics
    base_r = XA.OUTDIR / f"exp14_{arm}_s{seed}_{replay_tag}"
    base_c = XA.OUTDIR / f"exp14_{arm}_s{seed}_{verdict_tag}"

    # A1 — bit-exact checkpoint (weights + opt + gen_state + t)
    ck_r = torch.load(base_r.with_suffix(".ckpt_read.pt"), map_location="cpu", weights_only=False)
    ck_c = torch.load(base_c.with_suffix(".ckpt_read.pt"), map_location="cpu", weights_only=False)
    a1_div = None
    for key in ("vision", "word", "op", "opt", "gen_state"):
        a1_div = _tensors_equal(ck_r[key], ck_c[key], key)
        if a1_div:
            break
    if a1_div is None and int(ck_r["t"]) != int(ck_c["t"]):
        a1_div = f"t {ck_r['t']} != {ck_c['t']}"
    a1 = a1_div is None

    # A2 — replay per-window exam_acc == committed columns (digit-exact)
    com = json.loads(base_c.with_suffix(".json").read_text())
    ccols = {c["t"]: c.get("exam_acc") for c in com["columns"]}
    a2_div = None
    for c in replay_rec["columns"]:
        if ccols.get(c["t"]) != c.get("exam_acc"):
            a2_div = f"col t={c['t']}: replay {c.get('exam_acc')} != committed {ccols.get(c['t'])}"
            break
    a2 = a2_div is None

    # A3 — re-binned capture means == committed columns (proves the CAPTURE, not just the run)
    win = _bin_windows(per_onset)
    a3_div = None
    n_checked = 0
    for c in com["columns"]:
        t, cval = c["t"], c.get("exam_acc")
        accs = win.get(t)
        rebin = _fmt6g(statistics.mean(accs)) if accs else None
        if rebin != cval:
            a3_div = f"col t={t}: re-bin {rebin} (n={len(accs) if accs else 0}) != committed {cval}"
            break
        n_checked += 1
    a3 = a3_div is None

    return dict(seed=seed, A1_bitexact=a1, A1_div=a1_div, A2_columns=a2, A2_div=a2_div,
                A3_consistency=a3, A3_div=a3_div, n_columns_checked=n_checked,
                n_onset_captured=len(per_onset), all_green=bool(a1 and a2 and a3))


def write_capture(arm: str, seed: int, per_onset: list, tag: str) -> Path:
    p = XA.OUTDIR / f"exp14_{arm}_s{seed}_{tag}_peronset.json"
    p.write_text(json.dumps(dict(arm=arm, seed=seed, read_at=READ_AT, h_max=H_MAX,
                                 n_onset=len(per_onset),
                                 per_onset=[list(x) for x in per_onset]), indent=1))
    return p


# ---------------------------------------------------------------- red-team (reachable falsifiers)
def _redteam() -> dict:
    """Prove BOTH anchors are reachable falsifiers on a SHORT run (Jason ruling 2):
       (i)  clean twice           -> determinism: ckpts bit-identical (sanity)
       (ii) shift_draw capture    -> A1 (ckpt) DIVERGES from clean          [observed RED]
       (iii) corrupt one capture  -> A3 (re-bin) DIVERGES from its columns   [observed RED]
       (iv) clean capture         -> A3 GREEN
    No committed reference needed: the red-team compares clean vs perturbed of the SAME short run."""
    import statistics
    N = 1500
    arm = "exp12_shuffle"
    print("RED-TEAM (short read_at=%d):" % N)

    rec_a, cap_a = capture_run(arm, 0, read_at=N, h_max=2 * N, out_tag="rt_cleanA")
    rec_b, cap_b = capture_run(arm, 0, read_at=N, h_max=2 * N, out_tag="rt_cleanB")
    ck = lambda tag: torch.load((XA.OUTDIR / f"exp14_{arm}_s0_{tag}").with_suffix(".ckpt_read.pt"),
                                map_location="cpu", weights_only=False)
    det = all(_tensors_equal(ck("rt_cleanA")[k], ck("rt_cleanB")[k], k) is None
              for k in ("vision", "word", "op", "opt", "gen_state"))
    assert det, "RED-TEAM sanity FAILED: two clean replays are not bit-identical (non-determinism)"
    print("  (i)  determinism: two clean replays bit-identical  -> GREEN")

    rec_p, cap_p = capture_run(arm, 0, read_at=N, h_max=2 * N, out_tag="rt_shift", perturb="shift_draw")
    a1_shift_div = None
    for k in ("vision", "word", "op", "opt", "gen_state"):
        a1_shift_div = _tensors_equal(ck("rt_cleanA")[k], ck("rt_shift")[k], k)
        if a1_shift_div:
            break
    assert a1_shift_div is not None, \
        "RED-TEAM FAILED: shift_draw did NOT redden A1 — the bit-exact anchor is decorative (G0b v1)"
    print(f"  (ii) shift_draw capture -> A1 bit-exact DIVERGES ({a1_shift_div})  -> RED (as required)")

    win_clean = _bin_windows(cap_a, read_at=N)
    com_clean = {c["t"]: c.get("exam_acc") for c in rec_a["columns"]}
    a3_clean_ok = all(
        (_fmt6g(statistics.mean(win_clean[t])) if win_clean.get(t) else None) == com_clean[t]
        for t in com_clean)
    assert a3_clean_ok, "RED-TEAM FAILED: clean capture A3 not green (capture is already unfaithful)"
    print("  (iv) clean capture -> A3 consistency GREEN")

    cap_corrupt = list(cap_a)
    assert cap_corrupt, "RED-TEAM FAILED: no onsets captured in the short run"
    w, d, p, a = cap_corrupt[0]
    cap_corrupt[0] = (w, d, p, 1.0 - a)                  # flip one captured acc
    win_corrupt = _bin_windows(cap_corrupt, read_at=N)
    a3_corrupt_div = any(
        (_fmt6g(statistics.mean(win_corrupt[t])) if win_corrupt.get(t) else None) != com_clean[t]
        for t in com_clean)
    assert a3_corrupt_div, \
        "RED-TEAM FAILED: corrupting a capture did NOT redden A3 — the consistency anchor is decorative"
    print("  (iii) corrupted capture -> A3 consistency DIVERGES  -> RED (as required)")
    print("RED-TEAM PASS: both anchors observed RED under a deliberately broken capture, GREEN when clean.")
    return dict(determinism=det, a1_reddens_on_shift=True, a3_reddens_on_corrupt=True,
                a3_green_on_clean=True)


if __name__ == "__main__":
    import sys
    if "--redteam" in sys.argv:
        _redteam()
