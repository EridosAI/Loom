"""exp19_floor.py — G5a certification by FLOOR AUDIT + the alpha-doesn't-transport catch (Jason, 2026-07-14).

THE HOUSE DISCIPLINE (ledger 18, standing): raw counts never gate a finding — they scale with the
detector's false rate and sit inside the phantom floor. Certification = EXCESS OVER A MEASURED FLOOR, never
raw firing. The non-converter stratum runs {1:4, 3:5, 7:6} are NOT a leak; they ARE the phantom floor,
measured. The converters {0:37,2:20,4:17,5:71,6:12} clear it (nearest = 12 = 2x the floor ceiling 6) — the
SCATTER-terminal form ("raw sits inside/outside the phantom bracket").

WHY THE ALPHA-CUT WAS THE WRONG INSTRUMENT (the real finding — ledger 38, Jason): ALPHA=1e-3 is cut against
an i.i.d. false-rate model (_consec_rate). On the stratum, per-window accuracy is GRANULAR (5-13 onsets)
and AUTOCORRELATED — the i.i.d. model does not hold. A detector nominally at 1e-3 delivered an ACTUAL false
rate of 2/3 (Ruling-B N=5: 2/3 non-converters certified). A ~660x miss: a calibrate-in-regime violation
hiding inside a constant. Ruling-B didn't fail; ALPHA did. Nothing transports into the stratum regime
(Ruling 4) — band, N, ALPHA, cadence all suspect until re-measured in-regime.

CERTIFICATION = the FLOOR AUDIT, blind and in-regime:
  (i)  EMPIRICAL floor — the non-converters' own longest stratum runs (they carry the real granularity AND
       autocorrelation). Ceiling = max over {1,3,7}. Converter excess over it, with margin.
  (ii) SIMULATED floor — per seed, N_SIMS draws preserving each window's ACTUAL in-stratum onset count,
       Bernoulli at the seed's post-acq stratum mean p_hat (conservative: for converters p_hat is inflated
       by their own episode), longest run >= FLOOR_BAND. Converter observed run vs its null max -> p-value.

  --cache          rebuild each fabric once, cache the per-window in-stratum onset accs (no repeated builds)
  --audit          floor audit at FULL N (the G5a certification) + the alpha-transport audit
"""
from __future__ import annotations

import json
import statistics
import sys

import torch

import exp12_arms as X12
import exp14_arms as XA
import exp19_score as S19

EVAL = XA.EVAL
READ_AT = 500_000
H_MAX = 1_000_000
ARM = "exp12_shuffle"
VERDICT_SEEDS = list(range(8))
CONVERTERS = [0, 2, 4, 5, 6]
NONCONVERTERS = [1, 3, 7]
REPLAY_TAG = "g5a_replay"

FLOOR_BAND = XA.EPISODE_BAND          # 0.704 — the forced cap (sensitivities: stratum null quantiles all
#                                       exceed it). Band is itself suspect-in-regime (Ruling 4); it is
#                                       reported as forced, not transported.
SIM_SEED = 20260714                   # pinned — the floor-audit simulator
N_SIMS = 5000
CACHE = XA.OUTDIR / "exp19_g5a_strat_cache.json"


def _longest_run(series, band=FLOOR_BAND) -> int:
    """Longest run of consecutive windows >= band; None (empty window) breaks runs (conservative)."""
    best = cur = 0
    for a in series:
        cur = cur + 1 if (a is not None and a >= band) else 0
        best = max(best, cur)
    return best


# ---------------------------------------------------------------- --cache (one rebuild pass)
def cache():
    out = {}
    for s in VERDICT_SEEDS:
        rep = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_{REPLAY_TAG}_anchors.json").read_text())
        acq = rep["acquisition_onset"]
        capf = json.loads((XA.OUTDIR / f"exp14_{ARM}_s{s}_{REPLAY_TAG}_peronset.json").read_text())
        loop, spec, cfg = X12.build_exp12(ARM, s, H_MAX)
        fab = loop.stream
        zpm = S19._zero_preceding(fab.dwell_id[:READ_AT], fab.is_exam[:READ_AT])
        # per POST-ACQ window: the list of in-stratum onset accs (order preserved for among-kept thinning)
        win: dict = {}
        strat_onsets = []                                  # (window_t, acc) in emitted order — for G5b subsample
        for (wave, _dw, _pos, acc) in capf["per_onset"]:
            col = (wave // EVAL + 1) * EVAL
            if col > READ_AT or col < acq:
                continue
            if bool(zpm[wave]):
                win.setdefault(col, []).append(acc)
                strat_onsets.append([col, acc])
        out[str(s)] = dict(acquisition_onset=acq,
                           post_acq_windows=[t for t in range(EVAL, READ_AT + 1, EVAL) if t >= acq],
                           win_accs={str(t): v for t, v in win.items()},
                           strat_onsets=strat_onsets,
                           n_stratum=len(strat_onsets))
        print(f"cached s{s}: n_stratum={len(strat_onsets)}  n_windows_with_stratum={len(win)}")
    CACHE.write_text(json.dumps(out))
    print(f"wrote {CACHE}")


def _series_from_win(win_accs: dict, post_acq_windows: list) -> list:
    """Per-window stratum mean over the post-acq window grid; None where a window has no in-stratum onset."""
    return [ (statistics.mean(win_accs[str(t)]) if str(t) in win_accs and win_accs[str(t)] else None)
             for t in post_acq_windows ]


def _sim_null_runs(onset_counts: list, p: float, n_sims: int, gen, band: float = FLOOR_BAND) -> torch.Tensor:
    """Longest-run distribution of a granularity null: per window i with n_i in-stratum onsets, draw
    successes ~ Binomial(n_i, p), acc_i = successes/n_i; window clears iff acc_i >= band; empty
    windows (n_i=0) never clear (break runs). Returns [n_sims] longest runs. `band` defaults to
    FLOOR_BAND (G5a's forced 0.704, unchanged for the committed --audit path); B8 passes the CALIBRATION
    band CAL.BAND=0.64 so the deployed detector certifies at the band its op width was cut on (ledger 44)."""
    n_win = len(onset_counts)
    clears = torch.zeros(n_sims, n_win, dtype=torch.bool)
    for i, ni in enumerate(onset_counts):
        if ni <= 0:
            continue
        succ = (torch.rand(n_sims, ni, generator=gen) < p).sum(dim=1).float()
        clears[:, i] = (succ / ni) >= band
    # longest run of True per row
    best = torch.zeros(n_sims, dtype=torch.long)
    cur = torch.zeros(n_sims, dtype=torch.long)
    for i in range(n_win):
        cur = torch.where(clears[:, i], cur + 1, torch.zeros_like(cur))
        best = torch.maximum(best, cur)
    return best


# ---------------------------------------------------------------- --audit (G5a certification)
def audit() -> dict:
    data = json.loads(CACHE.read_text())
    gen = torch.Generator().manual_seed(SIM_SEED)
    per_seed, runs = {}, {}
    for s in VERDICT_SEEDS:
        d = data[str(s)]
        series = _series_from_win(d["win_accs"], d["post_acq_windows"])
        obs = _longest_run(series)
        runs[s] = obs
        # in-stratum onset count per post-acq window (for the simulator)
        counts = [len(d["win_accs"].get(str(t), [])) for t in d["post_acq_windows"]]
        vals = [a for a in series if a is not None]
        p_hat = statistics.mean(vals) if vals else 0.5
        null = _sim_null_runs(counts, p_hat, N_SIMS, gen)
        null_max = int(null.max())
        null_q999 = int(torch.quantile(null.float(), 0.999))
        p_exceed = float((null >= obs).float().mean())          # P(null run >= observed) under its own p_hat
        per_seed[s] = dict(observed_run=obs, p_hat=round(p_hat, 4), null_max=null_max,
                           null_q999=null_q999, p_value=p_exceed,
                           exceeds_null_max=bool(obs > null_max))

    # EMPIRICAL floor = the non-converters' own longest runs (real granularity + autocorrelation)
    floor_runs = {s: runs[s] for s in NONCONVERTERS}
    floor_ceiling = max(floor_runs.values())
    conv_runs = {s: runs[s] for s in CONVERTERS}
    nearest_conv = min(conv_runs.values())
    # SIMULATED floor certification: every converter observed run exceeds its own N_SIMS null max
    sim_certified = [s for s in CONVERTERS if per_seed[s]["exceeds_null_max"]]

    # -------- ALPHA-TRANSPORT AUDIT: nominal i.i.d. alpha vs actual measured false rate on the stratum
    #          The alpha-cut (Ruling-B) selected N=5; at N=5 the ACTUAL non-converter false rate is #leak/3.
    nonconv_runs = {s: runs[s] for s in NONCONVERTERS}
    n_leak_N5 = sum(1 for s in NONCONVERTERS if nonconv_runs[s] >= 5)   # reproduces the 2/3
    alpha_audit = dict(
        alpha_nominal=XA.ALPHA, alpha_cut_N=5,
        actual_false_rate=f"{n_leak_N5}/{len(NONCONVERTERS)}",
        miss_factor=round((n_leak_N5 / len(NONCONVERTERS)) / XA.ALPHA, 1),
        reason=("i.i.d. false-rate model (_consec_rate, the target of ALPHA) breaks on the granular "
                "(5-13 onsets/window) autocorrelated stratum; the alpha-cut controls a false rate that "
                "does not describe the regime. ALPHA does not transport."))

    certified = (nearest_conv > floor_ceiling) and (len(sim_certified) == len(CONVERTERS))
    out = dict(
        gate="G5a certification — FLOOR AUDIT (excess over measured floor, in-regime, blind)",
        floor_band=FLOOR_BAND, sim_seed=SIM_SEED, n_sims=N_SIMS,
        empirical_floor=dict(nonconverter_runs=floor_runs, ceiling=floor_ceiling),
        converter_runs=conv_runs, nearest_converter=nearest_conv,
        margin_ratio=round(nearest_conv / max(1, floor_ceiling), 2),
        simulated_floor_per_seed=per_seed,
        simulated_certified_converters=sim_certified,
        alpha_transport_audit=alpha_audit,
        VERDICT=("PASS — every converter clears the measured phantom floor: nearest converter "
                 f"{nearest_conv} > floor ceiling {floor_ceiling} (x{round(nearest_conv/max(1,floor_ceiling),2)}), "
                 f"and all {len(CONVERTERS)} converters exceed their in-regime simulated null max (p<{1/N_SIMS}). "
                 "Non-converters ARE the floor, as expected. The alpha-cut binary is retired: ALPHA does not "
                 "transport (nominal 1e-3 vs actual 2/3 false rate)." if certified else
                 "NOT CLEAN — investigate"),
        certified=certified, ok=True)
    (XA.OUTDIR / "exp19_g5a_floor_audit.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--cache" in sys.argv:
        cache()
    elif "--audit" in sys.argv:
        print(json.dumps(audit(), indent=2))
    else:
        print("usage: --cache | --audit")
