"""Step 0 — B00 oracle calibration (Characterisation-Sweep pre-flight; gates the band ladder).

Calibrated on the LIVE commit (never Phase-1's stale numbers). Measures, at the easy band B00,
where the three levels actually sit, then derives the sweep's `[RECONCILE]` bars as fractions of
measured headroom (never round literals). All probes are READ-ONLY / pre-loop; no sweep run happens
here. Reuses: `validity_probe.run_validity_probe` (raw `ceiling_B`, `floor_B`), `oracle_probe`
(the substrate oracle = the G1 line), `Stage0Loop` (intact-arm ceiling).

Outputs `calibration.json` = {chance, intact_easy_ceiling, oracle_easy_ceiling (substrate),
ceiling_B_raw_B00 (bracket), oracle_threshold, margin_oracle, noword_floor_band, intact_bar,
anchor (must-breach r/σ≈1 — proves F3 can fire), commit_hash, spec_hash}.

Derivation rules (the pre-registration that produced the numbers — hashed into spec_hash):
  oracle_threshold = chance + margin_oracle, margin_oracle = frac·(oracle_easy_ceiling − chance);
  intact_bar       = chance + k·(intact_easy_ceiling − chance);
  noword_floor_band= (chance, chance + noword_eps), noword_eps tied to the measured floor spread.
Asserts: B00 ablation guard passes; oracle_threshold < oracle_easy_ceiling; the anchor breaches
(D5 bracket: anchor_oracle + sep ≤ oracle_threshold ≤ oracle_easy_ceiling − sep).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import constants                                          # noqa: E402
from loop import Stage0Loop                               # noqa: E402
from oracle_probe import _commit_hash, oracle_b_rec       # noqa: E402
from validity_probe import run_validity_probe             # noqa: E402

# --- pre-registered calibration parameters (hashed into spec_hash) ----------------------------
# NOTE (2026-06-26): the deployed loop needs ~9k steps to reach the pooling_depth plateau (~0.56 at
# B00); Phase-1's 4000-step runs stopped at depth ~0.156 (~28% of plateau = early-rapid). So the
# intact-arm ceiling and the capacity metrics (full_depth, T95) are measured on a LONG run here.
CALIB_PARAMS = dict(
    B00=dict(r_fine=2.5, sigma_stim=0.20),       # current easy config (r/σ=12.5; clean ceilings)
    seeds=[0, 1, 2, 3, 4],
    margin_oracle_frac=0.25,                     # threshold = chance + 0.25·(ceiling − chance)
    intact_bar_k=0.5,                            # = pin.k
    noword_eps_floor=0.05, noword_eps_k=3.0,     # noword_eps = max(floor, 3·std(floor_B))
    anchor_r_fine=[0.20, 0.15, 0.10],            # r/σ ∈ {1.0, 0.75, 0.5}: must-breach ladder
    bracket_sep=0.05,                            # D5 separation
    oracle_steps=600,
    long_steps=12000, long_T=14000, eval_every=100,
    plateau_frac=0.20,                           # full_depth = mean depth over final 20%
    intact_tail_frac=0.30,                       # ceiling = mean B_track over post-plateau final 30%
    t95_level=0.95,                              # T95 = first wave capacity_fraction >= this
)


def spec_hash() -> str:
    return hashlib.sha256(json.dumps(CALIB_PARAMS, sort_keys=True).encode()).hexdigest()[:12]


def long_intact_run(cfg, pin, *, eval_every=100):
    """A LONG deployed intact (word-present) run. Returns (waves, b_tracks, depths). Read-only
    ceiling/convergence estimate (not loop success)."""
    loop = Stage0Loop(cfg, pin)
    waves, bts, deps = [], [], []
    for i in range(cfg.steps):
        loop.step(no_word=False)
        if i % eval_every == 0 or i == cfg.steps - 1:
            waves.append(i)
            bts.append(loop.b_a_track(cfg.n_eval)["B_track"])
            deps.append(loop.vision.pooling_depth)
    return waves, bts, deps


def capacity_metrics(waves, deps, *, plateau_frac, t95_level):
    """full_depth = mean depth over final `plateau_frac`; capacity_fraction = clip(cummax(
    (depth-baseline)/(plateau-baseline)),0,1); T95 = first wave capacity_fraction >= t95_level."""
    n = len(deps)
    k = max(1, int(n * plateau_frac))
    baseline = deps[0]
    plateau = statistics.mean(deps[-k:])
    denom = max(1e-9, plateau - baseline)
    cap, m = [], -1e9
    for d in deps:
        m = max(m, (d - baseline) / denom)
        cap.append(min(1.0, max(0.0, m)))
    t95_wave = next((waves[i] for i, c in enumerate(cap) if c >= t95_level), waves[-1])
    return dict(full_depth=plateau, pooled_baseline=baseline, t95_wave=t95_wave)


def calibrate(verbose=True, out_path="calibration.json") -> dict:
    pin = constants.PinnedConstants()
    base = constants.Stage0Config()
    chance = 1.0 / base.n_B
    seeds = CALIB_PARAMS["seeds"]
    b00 = CALIB_PARAMS["B00"]

    oracle_recs, raw_ceils, floor_Bs, intact_recs, abls = [], [], [], [], []
    full_depths, t95s = [], []
    ev = CALIB_PARAMS["eval_every"]
    for s in seeds:
        cfg = replace(base, r_fine=b00["r_fine"], sigma_stim=b00["sigma_stim"], seed=s)
        vp = run_validity_probe(cfg, pin)
        raw_ceils.append(vp["ceiling_B"]); floor_Bs.append(vp["floor_B"])
        orc = oracle_b_rec(cfg, pin, steps=CALIB_PARAMS["oracle_steps"])
        oracle_recs.append(orc["oracle_B_rec"]); abls.append(orc["ablation_collapsed"])
        # LONG intact run for a converged, post-plateau ceiling + capacity metrics.
        lcfg = replace(cfg, steps=CALIB_PARAMS["long_steps"], T=CALIB_PARAMS["long_T"])
        waves, bts, deps = long_intact_run(lcfg, pin, eval_every=ev)
        cap = capacity_metrics(waves, deps, plateau_frac=CALIB_PARAMS["plateau_frac"],
                               t95_level=CALIB_PARAMS["t95_level"])
        ktail = max(1, int(len(bts) * CALIB_PARAMS["intact_tail_frac"]))
        intact_recs.append(statistics.mean(bts[-ktail:]))
        full_depths.append(cap["full_depth"]); t95s.append(cap["t95_wave"])
        if verbose:
            print(f"  seed {s}: raw={vp['ceiling_B']:.3f} floor_B={vp['floor_B']:.3f} "
                  f"oracle={orc['oracle_B_rec']:.3f} abl_ok={orc['ablation_collapsed']} "
                  f"intact(post-plateau)={intact_recs[-1]:.3f} full_depth={cap['full_depth']:.3f} "
                  f"T95={cap['t95_wave']}")

    oracle_easy_ceiling = statistics.mean(oracle_recs)
    ceiling_B_raw_B00 = statistics.mean(raw_ceils)
    intact_easy_ceiling = statistics.mean(intact_recs)
    floor_mean = statistics.mean(floor_Bs)
    floor_std = statistics.pstdev(floor_Bs) if len(floor_Bs) > 1 else 0.0
    B00_full_depth = statistics.mean(full_depths)
    B00_T95 = statistics.mean(t95s)
    B00_T_run = 1.25 * B00_T95

    margin_oracle = CALIB_PARAMS["margin_oracle_frac"] * (oracle_easy_ceiling - chance)
    oracle_threshold = chance + margin_oracle
    noword_eps = max(CALIB_PARAMS["noword_eps_floor"], CALIB_PARAMS["noword_eps_k"] * floor_std)
    noword_floor_band = [chance, chance + noword_eps]
    intact_bar = chance + CALIB_PARAMS["intact_bar_k"] * (intact_easy_ceiling - chance)

    # --- must-breach anchor sweep (D5): prove F3 can fire ---------------------------------------
    anchor_sweep = []
    anchor_breach_at = None
    for r_fine in CALIB_PARAMS["anchor_r_fine"]:
        recs = [oracle_b_rec(replace(base, r_fine=r_fine, sigma_stim=b00["sigma_stim"], seed=s),
                             pin, steps=CALIB_PARAMS["oracle_steps"])["oracle_B_rec"] for s in seeds]
        m = statistics.mean(recs)
        row = dict(r_fine=r_fine, r_over_sigma=r_fine / b00["sigma_stim"], oracle_mean=m,
                   breaches=bool(m < oracle_threshold))
        anchor_sweep.append(row)
        if verbose:
            print(f"  anchor r/σ={row['r_over_sigma']:.2f}: oracle={m:.3f} "
                  f"(< thr {oracle_threshold:.3f}? {row['breaches']})")
        if anchor_breach_at is None and row["breaches"]:
            anchor_breach_at = row

    sep = CALIB_PARAMS["bracket_sep"]
    bracket_ok = (anchor_breach_at is not None
                  and anchor_breach_at["oracle_mean"] + sep <= oracle_threshold <= oracle_easy_ceiling - sep)

    rec = dict(
        commit_hash=_commit_hash(), spec_hash=spec_hash(), seeds=seeds, B00=b00,
        chance=chance, empirical_floor_B=floor_mean, floor_B_std=floor_std,
        ceiling_B_raw_B00=ceiling_B_raw_B00,
        oracle_easy_ceiling=oracle_easy_ceiling, oracle_easy_ceiling_per_seed=oracle_recs,
        intact_easy_ceiling=intact_easy_ceiling, intact_per_seed=intact_recs,
        B00_full_depth=B00_full_depth, B00_full_depth_per_seed=full_depths,
        B00_T95=B00_T95, B00_T95_per_seed=t95s, B00_T_run=B00_T_run,
        margin_oracle=margin_oracle, oracle_threshold=oracle_threshold,
        noword_eps=noword_eps, noword_floor_band=noword_floor_band, intact_bar=intact_bar,
        anchor_sweep=anchor_sweep, anchor_breach_at=anchor_breach_at,
        b00_ablation_ok=bool(all(abls)), bracket_ok=bool(bracket_ok),
        calib_params=CALIB_PARAMS,
    )

    # --- pre-registered assertions -------------------------------------------------------------
    problems = []
    if not all(abls):
        problems.append("B00 substrate-oracle ablation guard FAILED (content-memorization).")
    if not (oracle_threshold < oracle_easy_ceiling):
        problems.append("oracle_threshold not below oracle_easy_ceiling.")
    if anchor_breach_at is None:
        problems.append("NO anchor band breaches oracle_threshold -> F3 may never fire (too lax).")
    if not bracket_ok:
        problems.append("D5 bracket failed: need anchor+sep <= threshold <= ceiling-sep.")
    rec["problems"] = problems
    rec["STEP0_OK"] = not problems

    Path(out_path).write_text(json.dumps(rec, indent=2))
    if verbose:
        print("\n=== Step 0 calibration (commit {}) ===".format(rec["commit_hash"][:7]))
        for k in ("chance", "ceiling_B_raw_B00", "oracle_easy_ceiling", "intact_easy_ceiling",
                  "margin_oracle", "oracle_threshold", "noword_floor_band", "intact_bar",
                  "B00_full_depth", "B00_T95", "B00_T_run"):
            print(f"  {k:>20}: {rec[k]}")
        print("  anchor_breach_at:", anchor_breach_at)
        print("  bracket_ok:", bracket_ok, " STEP0_OK:", rec["STEP0_OK"])
        if problems:
            print("  PROBLEMS:", problems)
        print(f"  (record -> {out_path})")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="calibration.json")
    args = ap.parse_args()
    res = calibrate(out_path=args.out)
    sys.exit(0 if res["STEP0_OK"] else 1)
