"""exp20_cal.py — EXP20 G3: the in-regime cal at 1M (prereg §6 G3; touch-2 constants).

EVERY constant cut FRESH in-regime on the K arms' OWN E-B cal data at read_at = 1M — committed
FORMULAS, re-cut CONSTANTS, nothing transported unshown-red:
  band + N ("conv band, θ")   XA._provisional_cut (§10.22 honest-null joint cut) on per-window
                              post-acq E-B accs pooled across the 5 cal seeds, per K
  floor / phantom bracket     the one floor-audit law (exp19_cal.cal_floor_audit), band INJECTED
                              per K (RB.BAND / SC.BAND module override, restored after)
  operating points            argmax converter/floor separation on each (K, read)'s own null —
                              IF the arm has in-arm cal converters; else the EXP19-SPLIT precedent
                              route (powercert + the width question to Jason at touch 2)
  200-stream marginal nulls   gseed = SIM_SEED + 1_000_003*(k+1) + seed (the ledger-52 machinery)
  underpower gate             per (K, read): known signal = C_shuffle's committed converters
                              thinned to the target density (the G5b machinery, cited) — with a
                              1M-grid null-inflation companion (the 500k->1M window-count asymmetry
                              is REPORTED, never silently bridged)

E-B channel: per-onset acc = (lift > 0), the exam_acc semantics. K=1 REUSED rides the committed
E-A instrument; measured E-B/E-A identity on the K=1 smoke = 6/6 columns EXACT under the record's
own 6-digit rounding (an earlier 4/6 reading was CC's comparison artifact — raw float vs stored
rounding — corrected here; erratum noted at the G3 commit). On the identity arm the probe read
reproduces the exam channel exactly; the residual K=1 seam is unlike-HORIZON (500k committed
certification vs 1M paid reads), matched-bar-scoped. Cells per seed; delivered-stratum
onsets from exp20_ubuf.delivered_zero_preceding at W = K (the pre-flight derivation; W=2K and
W=inf support ride in exp20_g2_maps.json).

Modes: --stratcache (cal-seed maps) · --smoke (observed-red set) · --cut (the G3 emission)
"""
from __future__ import annotations

import json
import statistics
import sys
import time

import torch

torch.set_num_threads(1)
import exp12_arms as X12
import exp12_fabric as F
import exp14_arms as XA
import exp19_cal as CAL
import exp19_floor as FL
import exp19_g5b_rebin as RB
import exp19_scorer as SC
import exp20_ubuf as U20

OUTDIR = XA.OUTDIR
EVAL = XA.EVAL
READ_AT = 1_000_000
PAID_K = (32, 128, 512)
CAL_SEEDS = [20, 21, 22, 24, 25]          # pinned from the registry: exp19_corridor.py:33
SPLIT_WIDTH = 300                         # the conv/nonconv bootstrap split width (corridor :86)
STRIDE = 1_000_003                        # the 200-stream scheme (exp19_stream_stability.py:27)
N_STREAMS = 200
POWER_BAR = 0.90                          # the committed powercert bar (exp19_g9_smallB_powercert)
STRATCACHE = OUTDIR / "exp20_cal_stratcache.json"
CAL_OUT = OUTDIR / "exp20_cal.json"


def _load_rec(K: int, s: int) -> dict:
    return json.loads((OUTDIR / f"exp14_exp20_ubuf_K{K}_s{s}_exp20cal.json").read_text())


def _eb_onsets(rec: dict) -> tuple[int, list]:
    """acq (None -> 0, recorded by the caller) + per-onset [wave, acc] on the E-B channel."""
    acq = rec["acquisition_onset"] or 0
    ons = [[int(w), 1.0 if l > 0 else 0.0] for (w, l) in rec["eb_onsets"] if w < READ_AT]
    return acq, ons


# ------------------------------------------------------------- strat cache (cal seeds)

def stratcache():
    """Delivered-stratum onset membership for the CAL seeds (W = K), from the real data path —
    fabric structure + the deterministic map; no training involved."""
    out = {}
    for s in CAL_SEEDS:
        t0 = time.time()
        loop, _sp, _c = X12.build_exp12("exp12_dwell", s, READ_AT)
        fab = loop.stream
        row = {}
        for K in PAID_K:
            deliver = F.ubuf_map(fab.T, K, torch.Generator().manual_seed(F.SEED_UBUF + s))
            U20.causality_assert(deliver, fab.T)
            zpm = U20.delivered_zero_preceding(fab.member, deliver, fab.is_exam, K, READ_AT)
            row[f"K{K}"] = torch.nonzero(zpm, as_tuple=True)[0].tolist()
        out[str(s)] = row
        print(f"  stratcache s{s}: " + " ".join(f"K{K}:{len(row[f'K{K}'])}" for K in PAID_K) +
              f" ({round(time.time()-t0, 1)}s)", flush=True)
    STRATCACHE.write_text(json.dumps(out))
    print(f"wrote {STRATCACHE.name}", flush=True)


# ------------------------------------------------------------- band injection wrapper

class _band:
    """Inject the in-regime band into the committed law's module globals; ALWAYS restored."""
    def __init__(self, band: float):
        self.band = band
    def __enter__(self):
        self.saved = (RB.BAND, SC.BAND, CAL.BAND)
        RB.BAND = SC.BAND = CAL.BAND = self.band
    def __exit__(self, *a):
        RB.BAND, SC.BAND, CAL.BAND = self.saved


def _win_series(ons: list, acq: int) -> list:
    """Per-EVAL-window E-B acc series (post-acq), the _provisional_cut input grid."""
    win: dict = {}
    for w, a in ons:
        if w >= acq:
            win.setdefault((w // EVAL + 1) * EVAL, []).append(a)
    return [statistics.mean(v) for _t, v in sorted(win.items())]


# ------------------------------------------------------------- powercert (per K, per read)

def _powercert(band: float, target_counts: list, thin_to: float, width: int,
               gen: torch.Generator, k_draws: int = 20) -> dict:
    """The G5b machinery, cited: C_shuffle's committed converters thinned to the target density,
    certified per draw at `width`/`band` against their own sim null (500k grid). COMPANION: the
    same p_hat on the TARGET arm's real 1M per-window counts -> null max (the grid-length
    asymmetry, reported never bridged)."""
    conv = FL.CONVERTERS
    wave = json.loads(RB.WAVECACHE.read_text())
    per_conv = {}
    for s in conv:
        acq, ons = wave[str(s)]["acquisition_onset"], [list(o) for o in wave[str(s)]["onsets"]]
        n = len(ons)
        keep = max(2, round(thin_to * n))
        certs = []
        p_hats = []
        for _ in range(k_draws):
            idx = torch.randperm(n, generator=gen)[:keep].tolist()
            sub = [ons[i] for i in idx]
            with _band(band):
                r = SC._certify_seed(sub, acq, width, torch.Generator().manual_seed(
                    FL.SIM_SEED + s))
            certs.append(r["certified"])
            p_hats.append(r["p_hat"])
        per_conv[s] = dict(kept=keep, of=n, cert_rate=round(sum(certs) / k_draws, 3),
                           p_hat_med=round(statistics.median(p_hats), 4))
    rate = statistics.mean(v["cert_rate"] for v in per_conv.values())
    # 1M-grid null-inflation companion: same conservative p_hat on the TARGET's real counts
    p_ref = max(v["p_hat_med"] for v in per_conv.values())
    null_1m = FL._sim_null_runs(target_counts, p_ref, FL.N_SIMS,
                                torch.Generator().manual_seed(FL.SIM_SEED), band=band)
    return dict(per_converter=per_conv, mean_cert_rate=round(rate, 3),
                bar=POWER_BAR, passes=bool(rate >= POWER_BAR),
                grid_note=("committed machinery certifies on C's 500k grid; the target reads at "
                           "1M — the companion below is the same p_hat on the target's REAL 1M "
                           "counts (null inflation reported, not bridged)"),
                null_1m_grid=dict(p_hat_ref=p_ref, null_max=int(null_1m.max()),
                                  null_q999=int(torch.quantile(null_1m.float(), 0.999))))


# ------------------------------------------------------------- the G3 cut

def cut():
    strat = json.loads(STRATCACHE.read_text())
    out = {"doc": "EXP20_UBUF_PREREG.md §6 G3 — in-regime cal at 1M", "read_at": READ_AT,
           "cal_seeds": CAL_SEEDS, "registry": "exp19_corridor.py:33-34",
           "per_K": {}, "halt_surfaces": [], "notes": []}
    for K in PAID_K:
        recs = {s: _load_rec(K, s) for s in CAL_SEEDS}
        acq_none = [s for s in CAL_SEEDS if recs[s]["acquisition_onset"] is None]
        data_full, data_strat, win_accs = {}, {}, {}
        for s in CAL_SEEDS:
            acq, full = _eb_onsets(recs[s])
            sw = set(strat[str(s)][f"K{K}"])
            data_full[s] = (acq, full)
            data_strat[s] = (acq, [[w, a] for w, a in full if w in sw])
            win_accs[s] = _win_series(full, acq)
        # (1) band + N — §10.22 joint cut on the pooled post-acq E-B windows (formula committed)
        band, N, pooled = XA._provisional_cut(win_accs)
        row = dict(band=round(band, 4), N=int(N),
                   band_formula="XA._provisional_cut(§10.22): joint (band,N) on pooled post-acq "
                                "per-window E-B accs, cal seeds, episodes excluded",
                   band_inputs=dict(n_windows_pooled=len(pooled),
                                    per_seed_windows={s: len(win_accs[s]) for s in CAL_SEEDS},
                                    acq_none_treated_as_0=acq_none))
        # (2) conv/nonconv split at the bootstrap width (corridor :86 precedent), in-regime band
        with _band(band):
            certs = {s: SC._certify_seed(data_full[s][1], data_full[s][0], SPLIT_WIDTH,
                                         torch.Generator().manual_seed(FL.SIM_SEED + s))
                     for s in CAL_SEEDS}
        conv = [s for s in CAL_SEEDS if certs[s]["certified"]]
        nonconv = [s for s in CAL_SEEDS if s not in conv]
        row["split"] = {s: dict(observed=certs[s]["observed_run"], null_max=certs[s]["null_max"],
                                certified=certs[s]["certified"]) for s in CAL_SEEDS}
        row["cal_converters"], row["cal_nonconverters"] = conv, nonconv
        # (3) per read: the one floor-audit law, or the EXP19-SPLIT precedent route
        for read, data in (("full", data_full), ("delivered_stratum", data_strat)):
            n_ons = {s: len(data[s][1]) for s in CAL_SEEDS}
            counts_1m = None
            if read == "delivered_stratum":
                s0 = CAL_SEEDS[0]
                acq0, ons0 = data[s0]
                w0: dict = {}
                for w, _a in ons0:
                    if w >= acq0:
                        w0.setdefault(w // SPLIT_WIDTH, 0)
                        w0[w // SPLIT_WIDTH] += 1
                lo, hi = (min(w0), max(w0)) if w0 else (0, 0)
                counts_1m = [w0.get(i, 0) for i in range(lo, hi + 1)]
            else:
                acq0, ons0 = data[CAL_SEEDS[0]]
                counts_1m = [len(v) for v in _win_counts(ons0, acq0, SPLIT_WIDTH)]
            if conv and nonconv:
                with _band(band):
                    cal = CAL.cal_floor_audit(f"exp20_ubuf_K{K}", read, conv, nonconv, data=data)
                row[read] = dict(mode="in-arm floor audit", n_onsets=n_ons,
                                 op=cal["operating_point_width"], w_floor=cal["w_width_floor"],
                                 underpowered=cal["underpowered"],
                                 curve=[[r["width"], r["separation"], r["all_clear"]]
                                        for r in cal["sweep"]],
                                 verdict=cal["VERDICT"])
                if cal["underpowered"]:
                    out["halt_surfaces"].append(f"K{K}/{read}: STRATUM-UNDERPOWER (in-arm)")
            else:
                dens = statistics.mean(n_ons.values())
                wave = json.loads(RB.WAVECACHE.read_text())
                c_mean_n = statistics.mean(len(wave[str(s)]["onsets"]) for s in FL.CONVERTERS)
                thin_to = min(1.0, (dens * (500_000 / READ_AT)) / c_mean_n)
                pc = _powercert(band, counts_1m, thin_to, SPLIT_WIDTH,
                                torch.Generator().manual_seed(FL.SIM_SEED + 20260725))
                row[read] = dict(mode="NO in-arm cal converter — EXP19-SPLIT precedent route "
                                      "(powercert; op width = touch-2 question)",
                                 n_onsets=n_ons, powercert=pc)
                if not pc["passes"]:
                    out["halt_surfaces"].append(
                        f"K{K}/{read}: powercert FAILS ({pc['mean_cert_rate']} < {POWER_BAR}) — "
                        f"STRATUM-UNDERPOWER, null uninterpretable")
        # (4) 200-stream marginal nulls at the split width (the ledger-52 machinery, cal-time)
        with _band(band):
            sm = {}
            for s in CAL_SEEDS:
                acq, ons = data_full[s]
                nm = []
                for k in range(N_STREAMS):
                    g = torch.Generator().manual_seed(FL.SIM_SEED + STRIDE * (k + 1) + s)
                    r = SC._certify_seed(ons, acq, SPLIT_WIDTH, g)
                    nm.append(r["null_max"])
                sm[s] = dict(null_max_min=min(nm), null_max_med=int(statistics.median(nm)),
                             null_max_max=max(nm),
                             pinned=certs[s]["null_max"])
            row["stream_marginal_nulls"] = dict(
                scheme=f"gseed = SIM_SEED + {STRIDE}*(k+1) + seed, k in 0..{N_STREAMS-1} "
                       f"(exp19_stream_stability.py:27)", width=SPLIT_WIDTH, per_seed=sm)
        out["per_K"][f"K{K}"] = row
        print(f"K{K}: band {row['band']}xN{row['N']} | conv {conv} | " +
              " | ".join(f"{rd}: {row[rd].get('op', row[rd]['mode'][:20])}"
                         for rd in ("full", "delivered_stratum")), flush=True)
    out["notes"].append("E-B/E-A identity anchor (K=1 smoke, N=2000): 6/6 columns EXACT under "
                        "record rounding (the 4/6 first reading was a comparison artifact, "
                        "corrected). K=1 REUSED rides the committed E-A certification at 500k; "
                        "paid arms ride E-B at 1M — the seam is unlike-horizon, matched-bar-"
                        "scoped for any cross-K sentence")
    CAL_OUT.write_text(json.dumps(out, indent=2))
    print(("G3 HALT SURFACES: " + "; ".join(out["halt_surfaces"])) if out["halt_surfaces"]
          else "G3 cut complete, no halt surfaces", flush=True)
    print(f"wrote {CAL_OUT.name}", flush=True)


def _win_counts(ons: list, acq: int, w: int) -> list:
    win: dict = {}
    for wv, _a in ons:
        if wv >= acq:
            win.setdefault(wv // w, []).append(1)
    if not win:
        return []
    lo, hi = min(win), max(win)
    return [win.get(i, []) for i in range(lo, hi + 1)]


# ------------------------------------------------------------- smoke (observed red)

def smoke():
    """G3 executor red-team: (a) the injected band BITES (same plant certifies at a low band,
    fails at a high one); (b) chance 'converters' trip STRATUM-UNDERPOWER (reachable falsifier,
    the exp19_cal pattern on THIS wrapper's path); (c) powercert red on an impossible density."""
    # a MID-LEVEL (0.7) episode: clears a 0.5 band (long run, certifies) but sits UNDER a 0.9
    # band (no window clears, run 0). An all-1.0 plant clears any band — the first draft of this
    # fixture used one and the smoke correctly refused it (a band no plant can fail is untested).
    acq, ons = 3000, []
    for wi, w0 in enumerate(range(3000, 500_000, 300)):
        in_epi = 100_000 <= w0 < 130_000
        for j in range(10):
            acc = (1.0 if j < 7 else 0.0) if in_epi else (1.0 if j < 5 else 0.0)
            ons.append([w0 + j * 30 + 1, acc])
    with _band(0.60):
        lo = SC._certify_seed(ons, acq, 300, torch.Generator().manual_seed(1))
    with _band(0.90):
        hi = SC._certify_seed(ons, acq, 300, torch.Generator().manual_seed(1))
    assert lo["certified"] and not hi["certified"], \
        f"band injection does not bite — dead knob (lo {lo['certified']}, hi {hi['certified']})"
    print("  (a) band injection bites: 0.7-episode certifies at band 0.60, NOT at 0.90  [red observed]")
    nonconv = {1: CAL._plant(False), 3: CAL._plant(False), 7: CAL._plant(False)}
    with _band(0.64):
        under = CAL.cal_floor_audit("PLANT", "delivered_stratum", [0, 2, 4], [1, 3, 7],
                                    data={**{s: CAL._plant(False) for s in (0, 2, 4)}, **nonconv})
    assert under["underpowered"], "chance converters did NOT trip underpower on the exp20 path"
    print("  (b) chance 'converters' -> STRATUM-UNDERPOWER fires on this wrapper's path  [RED]")
    with _band(0.64):
        ok = CAL.cal_floor_audit("PLANT", "delivered_stratum", [0, 2, 4], [1, 3, 7],
                                 data={**{s: CAL._plant(True) for s in (0, 2, 4)}, **nonconv})
    assert not ok["underpowered"], "real planted converters read underpowered"
    print("  (c) real planted converters clear -> powered  [green]")
    print("SMOKE PASS (G3 executor: reds observed before any pass counts)", flush=True)


if __name__ == "__main__":
    if "--stratcache" in sys.argv:
        stratcache()
    elif "--smoke" in sys.argv:
        smoke()
    elif "--cut" in sys.argv:
        cut()
    else:
        print("usage: --stratcache | --smoke | --cut")
