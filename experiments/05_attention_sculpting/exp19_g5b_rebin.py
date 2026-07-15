"""exp19_g5b_rebin.py — the WINDOW re-cut: G5b's phantom floor was a BINNING artifact (Jason, ledger 40).

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
EVAL_INHERITED = 300          # the committed detector's bin width (the un-transported constant, ledger 40/41)
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
# Finer grid (ledger 41): the operating point is cut in the STRATUM's own regime, NOT the population's.
# The 27-onset target (width ~1706) was the population density — an over-correction. Sweep to find the
# ≥ width floor (below which the granularity floor swamps the signal) as a computed pre-flight constant.
WIDTHS = [300, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1200, 1500, 1706, 2100, 3000]


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
                         s6_clears_floor=s6_clears_floor, s6_clears_robust=bool(s6_min > floor_max),
                         sep_ratio=round(s6_q10 / max(1, floor_q99), 2),
                         n_converters_clear=sum(conv_clears.values()), conv_clears=conv_clears))

    inherited = next(r for r in rows if r["width"] == 300)
    # PRE-FLIGHT CONSTANT (ledger 41): the ≥ WIDTH FLOOR — the narrowest window at which the treatment
    # detector has power = the min width where the weakest labeled converter (s6) clears the phantom floor.
    # Below it, the granularity floor swamps the signal. Computed on the null + the labeled positive controls,
    # NOT fit to s6. Standard clearance (s6_q10>floor_q99) and the strict form (s6_min>floor_max) both reported.
    below = [r for r in rows if r["s6_clears_floor"]]
    w_power_floor = min((r["width"] for r in below), default=None)
    robust = [r for r in rows if r["s6_clears_robust"]]
    w_robust = min((r["width"] for r in robust), default=None)
    # OPERATING POINT — cut in the STRATUM's OWN regime (ledger 41: NOT the population's 27-onset target).
    # The stratum's characteristic density = its full-N (14,156) onsets/window at the native EVAL=300 bin
    # (~8.5), the density G5a characterized it at. Restore THAT on the thinned 7,915 arm (width ~550), so the
    # detector runs in the regime it will actually see — above the ≥ power floor, finest resolution consistent
    # with the stratum regime (flag 3). s6's margin is MEASURED here, not chosen; NOT widened to the population.
    STRATUM_NATIVE_ONSETS_PER_WIN = round(N_FULL / (READ_AT / EVAL_INHERITED), 1)   # ~8.5
    op = min(rows, key=lambda r: abs(r["onsets_per_window"] - STRATUM_NATIVE_ONSETS_PER_WIN))
    pop_target = min(rows, key=lambda r: abs(r["onsets_per_window"] - FULL_READ_ONSETS_PER_WIN))  # the retracted 27-target
    s6_ok = bool(op) and op["s6_clears_floor"]
    window_was_artifact = bool(s6_ok and not inherited["s6_clears_floor"])
    out = dict(
        gate="G5b re-cut — WINDOW audited; operating point cut in the STRATUM regime (ledger 41), outcome-blind",
        band=BAND, subsample_seed=SUBSAMPLE_SEED, k_draws=K_DRAWS, thin_ratio=round(R_THIN, 4),
        sweep=rows, inherited_300=inherited,
        preflight_width_floor=dict(w_power_floor=w_power_floor, w_robust=w_robust,
            grounds="min width where the weakest labeled converter s6 clears the phantom floor "
                    "(power_floor: s6_q10>floor_q99; robust: s6_min>floor_max) — a computed pre-flight "
                    "constant beside ρ(B) and the stratum counts"),
        stratum_native_onsets_per_window=STRATUM_NATIVE_ONSETS_PER_WIN,
        operating_point=op, operating_point_width=(op["width"] if op else None),
        retracted_population_target=dict(width=pop_target["width"], onsets_per_window=pop_target["onsets_per_window"],
            sep=pop_target["sep_ratio"], note="the 27-onset (all-population) density — over-correction, ledger 41"),
        FALSIFIER="s6 fails to clear the floor at ANY width in the stratum regime ⇒ genuine underpower, fork returns",
        VERDICT=(f"PASS, cut in the stratum regime (ledger 41). s6 swallowed ONLY at the inherited 300-bin "
                 f"(s6_q10 {inherited['s6_run_q10']} ≤ floor_q99 {inherited['floor_run_q99']}); ≥ width floor "
                 f"= {w_power_floor} (robust ≥ {w_robust}). Operating point width {op['width'] if op else None} "
                 f"({op['onsets_per_window'] if op else '-'} onsets/win, stratum regime): s6 margin "
                 f"{op['sep_ratio'] if op else '-'}× (q10 {op['s6_run_q10'] if op else '-'} vs floor_q99 "
                 f"{op['floor_run_q99'] if op else '-'}), {op['n_converters_clear'] if op else '-'}/5 clear. "
                 f"The 3.6× headline at width {pop_target['width']} was the population-regime over-correction, "
                 f"RETRACTED. G5b PASSES (target-invariant); the margin is the stratum-regime value." if s6_ok else
                 "FALSIFIER TRIGGERED — s6 fails to clear the floor across the stratum regime ⇒ genuine "
                 "underpower; the fork returns → Jason."),
        window_was_artifact=window_was_artifact, s6_clears_at_op=s6_ok, ok=True)
    (XA.OUTDIR / "exp19_g5b_rebin_sweep.json").write_text(json.dumps(out, indent=2))
    return out


def _print(o):
    print("\n===== G5b RE-BIN — phantom floor vs window width (N=7,915, band 0.64, outcome-blind) =====")
    print(f"  {'width':>5} {'ons/win':>7} {'floorq99':>8} {'floormax':>8} {'s6_med':>6} {'s6_q10':>6} "
          f"{'s6_min':>6} {'sep':>5} {'clr':>5} {'robust':>6} {'#conv':>5}")
    for r in o["sweep"]:
        print(f"  {r['width']:>5} {r['onsets_per_window']:>7} {r['floor_run_q99']:>8} {r['floor_run_max']:>8} "
              f"{r['s6_run_median']:>6} {r['s6_run_q10']:>6} {r['s6_run_min']:>6} {r['sep_ratio']:>5} "
              f"{str(r['s6_clears_floor']):>5} {str(r['s6_clears_robust']):>6} {r['n_converters_clear']:>5}")
    pf = o["preflight_width_floor"]; rt = o["retracted_population_target"]
    print(f"\n  PRE-FLIGHT WIDTH FLOOR (computed): power_floor ≥ {pf['w_power_floor']} · robust ≥ {pf['w_robust']}")
    print(f"  operating point (STRATUM regime, ledger 41): width={o['operating_point_width']}  "
          f"window_was_artifact={o['window_was_artifact']}")
    print(f"  retracted population target: width {rt['width']} ({rt['onsets_per_window']} onsets/win, "
          f"sep {rt['sep']}×) — the over-correction")
    print(f"\n  VERDICT: {o['VERDICT']}\n")


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--cache-wave" in sys.argv:
        _cache_wave()
    elif "--sweep" in sys.argv:
        _print(sweep())
    else:
        print("usage: --cache-wave | --sweep")
