"""exp19_cal.py — B7: the ONE FLOOR-AUDIT LAW, per-B, both reads (Jason 2026-07-15, ratified).

The α-cut is DROPPED entirely. The floor audit is the certification at every B, both reads (full-read AND
stratified) — it makes no i.i.d. assumption, agrees with α where α is valid, and is right where α fails
(α transported once and was wrong by 667×). One detector family across the arm ⇒ every cross-B / cross-read
comparison uses the same instrument. Borrow-gate SURVIVES (C_shuffle's shifted-floor referent, orthogonal to
α-vs-floor-audit; it rides the full-read floor audit unchanged).

PER-B, cut on the NULL, outcome-blind (ledger 41): each B gets its own width SWEEP, its own operating point at
that B/read's native density, and its own ≥ WIDTH FLOOR (min width where a known converter clears the phantom
floor). Below that width the granularity floor swamps the signal. The per-B width floors go in G8 beside ρ(B).

PER-B UNDERPOWER GATE (built as a GATE, not a cal step — = wp-strat generalized across the ladder): if any B's
stratified detector cannot clear its own floor for a KNOWN signal at that B's density, that B's stratified
read is underpowered and its null is uninterpretable ⇒ STRATUM-UNDERPOWER, per-B. The arm is only as strong as
its weakest-powered B (the anchor, B=512). The matched-N power test (thinning to that B's density) is the
underpower gate's teeth — it reuses the G5b machinery per-B.

STATUS: core + B=T (exp12_shuffle) validation here. Treatment arms exp19_wperm_B{32,128,512,2048} have no
records until the corridor (nothing trains until G8) — exp19_cal runs per-B there. B=T reproduces G5a/G5b:
stratified operating point 550, ≥ width floor 400 (`exp19_g5b_rebin_sweep.json`).
"""
from __future__ import annotations

import json
import statistics
import sys

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp19_score as S19
import exp19_g5b_rebin as RB

BAND = RB.BAND                          # 0.64 — the committed X15_REPRO C_shuffle detector band
READ_AT, H_MAX, EVAL = RB.READ_AT, RB.H_MAX, RB.EVAL_INHERITED
REPLAY_TAG = "g5a_replay"
FULL_READ_NATIVE = 27.0                 # full-read onsets/window at EVAL=300 (~46034/1666, ~B-independent)
# The stratified CHARACTERIZATION density (ledger 41): C_shuffle's full-N zero-preceding stratum density
# (14156 onsets / 1666 windows at EVAL=300 ≈ 8.5). It is UNIVERSAL across the ladder — "one detector family"
# (Jason): every B's stratified window is cut to RESTORE this density on that B's stratum (so a smaller
# stratum ⇒ a wider window; B=512's 8097 restores 8.5 at ~width 540, matching the G5b proxy's 550). NOT each
# arm's own sparse density (that was the width-300 granularity artifact).
STRATUM_NATIVE_DENSITY = round(14156 / (READ_AT / EVAL), 1)   # ≈ 8.5


def _onsets(arm: str, seed: int, read: str) -> tuple[int, list]:
    """Per-onset [wave, acc] for the read over [0, read_at). read='full' = ALL onset exams (already in the
    per-onset capture); read='stratified' = the zero-preceding stratum (needs the arm's dwell_id/is_exam)."""
    rep = json.loads((XA.OUTDIR / f"exp14_{arm}_s{seed}_{REPLAY_TAG}_anchors.json").read_text())
    acq = rep["acquisition_onset"]
    cap = json.loads((XA.OUTDIR / f"exp14_{arm}_s{seed}_{REPLAY_TAG}_peronset.json").read_text())
    if read == "full":
        ons = [[int(w), float(a)] for (w, _d, _p, a) in cap["per_onset"] if w < READ_AT]
    else:                                                    # stratified (zero-preceding)
        wc = json.loads(RB.WAVECACHE.read_text()) if (arm == "exp12_shuffle" and RB.WAVECACHE.exists()) else {}
        if str(seed) in wc:                                  # fast path: the committed wave-cache (no rebuild)
            return wc[str(seed)]["acquisition_onset"], [list(o) for o in wc[str(seed)]["onsets"]]
        loop, _spec, _cfg = X12.build_exp12(arm, seed, H_MAX)   # per-B: rebuild the arm's fabric for the stratum
        zpm = S19._zero_preceding(loop.stream.dwell_id[:READ_AT], loop.stream.is_exam[:READ_AT])
        ons = [[int(w), float(a)] for (w, _d, _p, a) in cap["per_onset"] if w < READ_AT and bool(zpm[w])]
    return acq, ons


def cal_floor_audit(arm: str, read: str, conv: list, nonconv: list, widths=None, data=None) -> dict:
    """The one floor-audit law for (arm, read): sweep window width; per width the phantom floor is the
    NON-converters' longest-run distribution and the signal is each converter's longest run; the operating
    point is cut at the native density (outcome-blind); the ≥ width floor is the narrowest width where every
    converter clears the floor (q99). Underpowered iff no width clears — STRATUM-UNDERPOWER for that B/read.
    `data` (optional) = {seed: (acq, [[wave,acc],...])} in-memory (the smoke plants it); else read from files."""
    widths = widths or RB.WIDTHS
    if data is None:
        data = {s: _onsets(arm, s, read) for s in conv + nonconv}
    native = FULL_READ_NATIVE if read == "full" else STRATUM_NATIVE_DENSITY   # UNIVERSAL (ledger 41), not arm-own
    rows = []
    for w in widths:
        runs = {}
        for s in conv + nonconv:
            acq, ons = data[s]
            r, _m = RB._longest_run_binned([o[0] for o in ons], [o[1] for o in ons], w, acq)
            runs[s] = r
        m_w = statistics.mean(len(data[s][1]) / (READ_AT / w) for s in conv + nonconv)
        floor = [runs[s] for s in nonconv]
        fq99, fmax = RB._q(floor, 0.99), max(floor)
        conv_runs = {s: runs[s] for s in conv}
        clears = {s: bool(runs[s] > fq99) for s in conv}
        rows.append(dict(width=w, onsets_per_window=round(m_w, 1), floor_q99=fq99, floor_max=fmax,
                         conv_runs=conv_runs, nonconv_runs={s: runs[s] for s in nonconv},
                         n_clear=sum(clears.values()), nearest_conv=min(conv_runs.values()),
                         all_clear=bool(sum(clears.values()) == len(conv))))
    op = min(rows, key=lambda r: abs(r["onsets_per_window"] - native))
    w_floor = min((r["width"] for r in rows if r["all_clear"]), default=None)
    underpowered = w_floor is None
    out = dict(gate="B7 exp19_cal — floor-audit law", arm=arm, read=read, band=BAND,
               converters=conv, nonconverters=nonconv, native_density=native,
               sweep=rows, operating_point=op, operating_point_width=op["width"],
               w_width_floor=w_floor, underpowered=underpowered,
               VERDICT=(f"STRATUM-UNDERPOWER ({arm}/{read}) — no window width lets all converters clear the "
                        "phantom floor ⇒ null uninterpretable ⇒ HALT → Jason" if underpowered else
                        f"powered ({arm}/{read}): ≥ width floor = {w_floor}; operating point width "
                        f"{op['width']} ({op['onsets_per_window']} onsets/win, native {native}); "
                        f"{op['n_clear']}/{len(conv)} converters clear (nearest run {op['nearest_conv']} vs "
                        f"floor q99 {op['floor_q99']})"), ok=True)
    return out


def _validate_BT():
    """B=T (exp12_shuffle): stratified must reproduce G5b (op 550, ≥ width floor 400); full-read separates
    converters from the non-converting floor at the dense native ~27/win."""
    conv, nonconv = [0, 2, 4, 5, 6], [1, 3, 7]
    for read in ("stratified", "full"):
        o = cal_floor_audit("exp12_shuffle", read, conv, nonconv)
        print(f"\n=== exp19_cal  exp12_shuffle / {read} ===")
        print(f"  native density {o['native_density']} onsets/win · ≥ width floor {o['w_width_floor']} · "
              f"operating point width {o['operating_point_width']}")
        print(f"  {'width':>5} {'ons/win':>7} {'floorq99':>8} {'nearest_conv':>12} {'n_clear':>7} {'all':>4}")
        for r in o["sweep"]:
            print(f"  {r['width']:>5} {r['onsets_per_window']:>7} {r['floor_q99']:>8} "
                  f"{r['nearest_conv']:>12} {r['n_clear']:>7} {str(r['all_clear']):>4}")
        print(f"  VERDICT: {o['VERDICT']}")
        (XA.OUTDIR / f"exp19_cal_exp12_shuffle_{read}.json").write_text(json.dumps(o, indent=2))


def _plant(with_episode: bool, epi=(100000, 130000), n_per_win=8) -> tuple[int, list]:
    """Deterministic planted per-onset series (no RNG). Chance windows: 4/8 correct (mean 0.5) with a lucky
    6/8 (0.75) every 40th window ⇒ a realistic short-run floor. `with_episode`: windows in `epi` are all-1.0
    (a sustained ≥0.64 episode ⇒ a long run)."""
    acq, ons = 3000, []
    for wi, w0 in enumerate(range(3000, READ_AT, 300)):
        for j in range(n_per_win):
            acc = 1.0 if (with_episode and epi[0] <= w0 < epi[1]) else \
                  (1.0 if (j < 6 if wi % 40 == 0 else j < 4) else 0.0)   # lucky 6/8 every 40th else 4/8
            ons.append([w0 + j * 30 + 1, acc])
    return acq, ons


def _smoke():
    print("exp19_cal SMOKE — the per-B UNDERPOWER gate is a reachable falsifier:")
    nonconv = {1: _plant(False), 3: _plant(False), 7: _plant(False)}       # chance = the floor
    # (a) POWERED: converters carry a real episode -> clear the floor -> NOT underpowered.
    powered = cal_floor_audit("PLANT", "stratified", [0, 2, 4], [1, 3, 7],
                              data={**{s: _plant(True) for s in (0, 2, 4)}, **nonconv})
    assert not powered["underpowered"], "SMOKE FAIL: planted real converters read as underpowered"
    assert powered["w_width_floor"] is not None
    print(f"  (a) real converters clear (≥ width floor {powered['w_width_floor']}) -> POWERED  [green]")
    # (b) UNDERPOWERED red-test: 'converters' are ALSO chance (no episode) -> cannot clear -> gate FIRES.
    under = cal_floor_audit("PLANT", "stratified", [0, 2, 4], [1, 3, 7],
                            data={**{s: _plant(False) for s in (0, 2, 4)}, **nonconv})
    assert under["underpowered"], "SMOKE FAIL: chance 'converters' did NOT trip the underpower gate"
    assert under["w_width_floor"] is None and "STRATUM-UNDERPOWER" in under["VERDICT"]
    print(f"  (b) chance 'converters' cannot clear the floor -> STRATUM-UNDERPOWER fires  [RED, as required]")
    print("SMOKE PASS: the underpower gate observed RED on a known-underpowered plant, GREEN on a real signal.")


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--validate" in sys.argv:
        _validate_BT()
    elif "--smoke" in sys.argv:
        _smoke()
    else:
        print("usage: --validate | --smoke   (B=T reproduction / gate red-test; per-B runs in the corridor)")
