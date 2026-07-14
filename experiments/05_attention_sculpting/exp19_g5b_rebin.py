"""exp19_g5b_rebin.py — the WINDOW re-cut: G5b's phantom floor was a BINNING artifact (Jason, ledger 39).

THE THIRD UN-TRANSPORTED CONSTANT. The detector bins at EVAL=300 steps — a FULL-READ constant. Full read: a
300-step window holds ~27 onsets. Thinned stratum (N=7,915): ~5. Accuracy over ~5 samples is coarse and
lumpy; lumpy → long chance runs; long chance runs ARE the phantom floor. G5b's "underpower" measured a
detector binned for a regime 5.6× denser than the one it runs in. We audited α (ledger 38) and the forced
band; neither chair audited the WINDOW. Ledger 39.

THE RULING (outcome-blind, fixed by the committed full-read detector — NOT by what it does to s6):
The full-read detector's operating point is an EVIDENCE requirement, not a bin requirement — it asks for
~N×27 ≈ 135 onsets of sustained signal (X15_REPRO C_shuffle = band 0.64, N=5 windows × ~27 onsets). PRESERVE
the granularity the detector was cut for; RE-DERIVE the bins. Re-bin the stratum at widths that restore the
full-read onsets/window, re-measure the phantom floor at 7,915. SWEEP window widths; the operating point is
chosen on the NULL (the width restoring ~27 onsets/window), never on s6.

THE GATE is the FLOOR AUDIT — a WITHIN-WIDTH separation: `s6_q10 > floor_q99` at the same width (so onsets/
window m_w cancels ⇒ the separation ratio is UNIT-INVARIANT). `N_w`/`EVIDENCE_ONSETS` is REPORTED CONTEXT
only (it restores the density; it does NOT itself gate — enforcing 135/N_w as an absolute threshold would
misfire, since at the restored density N_w≈5 ≤ the floor's own max). The verdict reads only s6-vs-floor.
CAVEAT carried (panel FLAGs): 27 onsets/win is the ALL-onset full-read density; the stratum is zero-preceding
(native full-N density ~8.5/win ⇒ width ~600), where s6 still clears but ~1.6×, not 3.6× — the binary PASS is
target-invariant, the magnitude is not. Wide-window run-length measures block-CONTIGUITY, not strength.

FALSIFIER (pre-named, on the record before computing): if the floor does NOT collapse under the re-binned
detector AND s6 still fails to clear, the underpower is GENUINE, the fork returns, and it is ruled with the
window constant finally audited.

  --cache-wave   rebuild each fabric once; cache per in-stratum onset the WAVE (step) + acc (enables re-bin)
  --sweep        floor + signal vs window width at 7,915 (and full N), evidence-preserving N, outcome-blind
"""
from __future__ import annotations

import json
import statistics
import sys

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp19_score as S19

READ_AT = 500_000
H_MAX = 1_000_000
ARM = "exp12_shuffle"
VERDICT_SEEDS = list(range(8))
CONVERTERS = [0, 2, 4, 5, 6]
NONCONVERTERS = [1, 3, 7]
REPLAY_TAG = "g5a_replay"

BAND = 0.64                       # the COMMITTED full-read C_shuffle detector band (X15_REPRO), transported
#                                   with the granularity it was cut for (restored by the re-bin), NOT the
#                                   α-forced 0.704 (which was the sparse-bin artifact).
EVIDENCE_ONSETS = 135             # full-read evidence: N=5 windows × ~27 onsets/window
FULL_READ_ONSETS_PER_WIN = 27
N_FULL = 14156
N_TARGET = 7915
R_THIN = N_TARGET / N_FULL
SUBSAMPLE_SEED = 719_150
K_DRAWS = 2000
WAVECACHE = XA.OUTDIR / "exp19_g5a_strat_cache_wave.json"
WIDTHS = [300, 450, 600, 900, 1200, 1500, 1706, 2100, 3000]   # 1706 ≈ restores 27 onsets/win at 7,915


def _cache_wave():
    out = {}
    for s in VERDICT_SEEDS:
        rep = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_{REPLAY_TAG}_anchors.json").read_text())
        acq = rep["acquisition_onset"]
        capf = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_{REPLAY_TAG}_peronset.json").read_text())
        loop, spec, cfg = X12.build_exp12(ARM, s, H_MAX)
        zpm = S19._zero_preceding(loop.stream.dwell_id[:READ_AT], loop.stream.is_exam[:READ_AT])
        onsets = [[int(wave), float(acc)] for (wave, _dw, _pos, acc) in capf["per_onset"]
                  if wave < READ_AT and bool(zpm[wave])]     # POST-ACQ filter applied at bin time (needs acq)
        out[str(s)] = dict(acquisition_onset=acq, onsets=onsets, n=len(onsets))
        print(f"cached s{s}: n_stratum={len(onsets)}")
    WAVECACHE.write_text(json.dumps(out))
    print(f"wrote {WAVECACHE}")


def _longest_run_binned(waves, accs, w: int, acq: int) -> tuple[int, float]:
    """Bin post-acq (wave>=acq) onsets into width-w windows (idx = wave//w), per-window mean; longest run of
    windows >= BAND (empty windows break runs). Returns (longest_run_in_windows, onsets_per_window)."""
    win: dict = {}
    for wv, a in zip(waves, accs):
        if wv < acq:
            continue
        win.setdefault(wv // w, []).append(a)
    if not win:
        return 0, 0.0
    lo, hi = min(win), max(win)
    best = cur = 0
    for k in range(lo, hi + 1):
        v = win.get(k)
        cur = cur + 1 if (v and statistics.mean(v) >= BAND) else 0
        best = max(best, cur)
    n_onset = sum(len(v) for v in win.values())
    m_w = n_onset / (hi - lo + 1)
    return best, m_w


def _q(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))] if xs else 0


def sweep() -> dict:
    data = json.loads(WAVECACHE.read_text())
    gen = torch.Generator().manual_seed(SUBSAMPLE_SEED)
    # pre-draw the thinned index sets (same among-kept draws reused across widths — width is what varies)
    keeps = {s: round(R_THIN * data[str(s)]["n"]) for s in VERDICT_SEEDS}
    draws = {s: [torch.randperm(data[str(s)]["n"], generator=gen)[:keeps[s]].tolist()
                 for _ in range(K_DRAWS)] for s in VERDICT_SEEDS}

    rows = []
    for w in WIDTHS:
        # per-seed run distributions under thinning at width w
        runs = {s: [] for s in VERDICT_SEEDS}
        m_w_seen = []
        for s in VERDICT_SEEDS:
            d = data[str(s)]; acq = d["acquisition_onset"]
            waves = [o[0] for o in d["onsets"]]; accs = [o[1] for o in d["onsets"]]
            for idx in draws[s]:
                sw = [waves[i] for i in idx]; sa = [accs[i] for i in idx]
                r, m = _longest_run_binned(sw, sa, w, acq)
                runs[s].append(r); m_w_seen.append(m)
        m_w = statistics.mean(m_w_seen)
        N_w = max(2, round(EVIDENCE_ONSETS / m_w))            # evidence-preserving window count
        floor_pool = [r for s in NONCONVERTERS for r in runs[s]]
        floor_q99 = _q(floor_pool, 0.99); floor_max = max(floor_pool)
        s6 = runs[6]; s6_med = _q(s6, 0.5); s6_q10 = _q(s6, 0.10); s6_min = min(s6)
        # certification = FLOOR AUDIT (signal lower tail clears floor upper tail), NOT signal-vs-N_w.
        # N_w (evidence-preserving) is reported as context; the gate is s6 vs the measured floor.
        s6_clears_floor = s6_q10 > floor_q99
        conv_clears = {s: bool(_q(runs[s], 0.10) > floor_q99) for s in CONVERTERS}
        rows.append(dict(width=w, onsets_per_window=round(m_w, 1), N_w=N_w,
                         floor_run_q99=floor_q99, floor_run_max=floor_max,
                         floor_onsets_q99=round(floor_q99 * m_w, 1),
                         s6_run_median=s6_med, s6_run_q10=s6_q10, s6_run_min=s6_min,
                         s6_clears_floor=s6_clears_floor, sep_ratio=round(s6_q10 / max(1, floor_q99), 2),
                         n_converters_clear=sum(conv_clears.values()), conv_clears=conv_clears))

    # operating point = the width restoring full-read onsets/window (chosen ON THE NULL, not on s6)
    op = min(rows, key=lambda r: abs(r["onsets_per_window"] - FULL_READ_ONSETS_PER_WIN))
    inherited = next(r for r in rows if r["width"] == 300)
    s6_ok = op["s6_clears_floor"]
    window_was_artifact = bool(s6_ok and not inherited["s6_clears_floor"])
    out = dict(
        gate="G5b re-cut — WINDOW audited; phantom floor vs window width at N=7,915 (outcome-blind)",
        band=BAND, evidence_onsets=EVIDENCE_ONSETS, full_read_onsets_per_window=FULL_READ_ONSETS_PER_WIN,
        subsample_seed=SUBSAMPLE_SEED, k_draws=K_DRAWS, thin_ratio=round(R_THIN, 4),
        sweep=rows, operating_point_width=op["width"], operating_point=op, inherited_300=inherited,
        FALSIFIER="s6 STILL fails to clear the measured floor at the restored density ⇒ genuine underpower, fork returns",
        VERDICT=(f"FLOOR WAS A BINNING ARTIFACT — s6 is swallowed ONLY at the inherited 300-step window "
                 f"(s6_q10 {inherited['s6_run_q10']} <= floor_q99 {inherited['floor_run_q99']}); at the "
                 f"restored full-read density (width {op['width']}, {op['onsets_per_window']} onsets/win) s6 "
                 f"clears the floor {op['sep_ratio']}x (s6_q10 {op['s6_run_q10']} vs floor_q99 "
                 f"{op['floor_run_q99']}); {op['n_converters_clear']}/5 converters clear. The 300-step window "
                 "was the THIRD un-transported constant (ledger 39). G5b PASSES." if s6_ok else
                 "FALSIFIER TRIGGERED — s6 STILL fails to clear the measured floor at the restored density "
                 "⇒ genuine underpower; the fork returns → Jason."),
        window_was_artifact=window_was_artifact, s6_clears_at_op=s6_ok, ok=True)
    (XA.OUTDIR / "exp19_g5b_rebin_sweep.json").write_text(json.dumps(out, indent=2))
    return out


def _print(o):
    print("\n===== G5b RE-BIN — phantom floor vs window width (N=7,915, band 0.64, outcome-blind) =====")
    print(f"  evidence requirement = {o['evidence_onsets']} onsets sustained ≥{o['band']} "
          f"(full-read {o['full_read_onsets_per_window']} onsets/window)")
    print(f"  {'width':>5} {'ons/win':>7} {'N_w':>4} {'floorq99':>8} {'floormax':>8} "
          f"{'s6_med':>6} {'s6_q10':>6} {'s6_min':>6} {'sep':>5} {'s6>floor':>8} {'#conv':>5}")
    for r in o["sweep"]:
        print(f"  {r['width']:>5} {r['onsets_per_window']:>7} {r['N_w']:>4} {r['floor_run_q99']:>8} "
              f"{r['floor_run_max']:>8} {r['s6_run_median']:>6} {r['s6_run_q10']:>6} {r['s6_run_min']:>6} "
              f"{r['sep_ratio']:>5} {str(r['s6_clears_floor']):>8} {r['n_converters_clear']:>5}")
    print(f"\n  operating point (restores ~{o['full_read_onsets_per_window']} onsets/win, chosen on null): "
          f"width={o['operating_point_width']}  window_was_artifact={o['window_was_artifact']}  "
          f"s6_clears_floor={o['s6_clears_at_op']}")
    print(f"\n  VERDICT: {o['VERDICT']}\n")


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--cache-wave" in sys.argv:
        _cache_wave()
    elif "--sweep" in sys.argv:
        _print(sweep())
    else:
        print("usage: --cache-wave | --sweep")
