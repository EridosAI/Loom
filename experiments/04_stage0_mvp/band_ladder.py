"""Band ladder (Characterisation-Sweep) — probe-bracketed, built AFTER Step 0.

Varies **r_fine↓ at fixed σ_stim** (R6: single-variable; σ↑ would mechanically depress the raw
oracle). Probe-only (no deployed sweep run). Endpoints bracketed by **probe representability**:
  top    = just below the trivial r/σ≈12.5, raw `ceiling_B` near-clean + substrate oracle near its
           ceiling (so density isn't wasted in the trivial region; autonomous *plausibly* succeeds);
  bottom = lowest cell whose **substrate oracle** is still ≥ `oracle_threshold` + margin (admissible;
           the F3 cap is enforced just below).
Then ≥10 uniform steps in r/σ between them. **Admissibility is gated on the SUBSTRATE oracle**
(the re-pre-registered F3 line) + A-salience + floor_B — NOT on raw `ceiling_B`/confusion (those are
raw-based and fail in the very interior where raw is weak but the substrate still represents B; they
are recorded for F3-diagnosis only). `autonomous_resolution_frequency` (whether the no-word arm
acquires B) is a SWEEP OUTPUT, not a ladder input.

Reuses `oracle_probe.oracle_b_rec` (substrate oracle + ablation guard) and
`validity_probe.run_validity_probe` (raw `ceiling_B`, `floor_B`, `A_salience`, confusion — diagnostics).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import constants                                          # noqa: E402
from oracle_probe import _commit_hash, oracle_b_rec       # noqa: E402
from validity_probe import run_validity_probe             # noqa: E402

LADDER_PARAMS = dict(
    sigma_stim=0.20,
    r_over_sigma_top=7.5,        # just below trivial r/σ≈12.5 (raw near-clean, oracle≈ceiling)
    r_over_sigma_bottom=1.30,    # candidate bottom near the oracle→threshold approach
    n_cells=12,                  # candidates; ≥10 must remain admissible after the F3 trim
    seeds=[0, 1, 2],
    oracle_steps=600,
    bottom_margin=0.05,          # admissible bottom: oracle ≥ threshold + this (just above F3)
    raw_clean_bar=0.90,          # top diagnostic: raw ceiling_B ≥ this (autonomous plausible)
    floor_eps=0.10,              # floor_B must stay ≤ chance + this (B not coarse-trivial)
    f3_bracket_r_over_sigma=[1.15, 1.0, 0.85],   # probes below the ladder: confirm F3 can fire
)


def build_ladder(calib_path="calibration.json", out_path="band_ladder.json", verbose=True) -> dict:
    calib = json.loads(Path(calib_path).read_text())
    commit = _commit_hash()
    if calib.get("commit_hash") != commit:
        raise SystemExit(f"calibration commit {calib.get('commit_hash')} != HEAD {commit}; re-run Step 0")
    pin = constants.PinnedConstants()
    base = constants.Stage0Config()
    thr = calib["oracle_threshold"]
    chance = calib["chance"]
    oracle_easy_ceiling = calib["oracle_easy_ceiling"]
    sig = LADDER_PARAMS["sigma_stim"]
    seeds = LADDER_PARAMS["seeds"]
    lo, hi, n = (LADDER_PARAMS["r_over_sigma_bottom"], LADDER_PARAMS["r_over_sigma_top"],
                 LADDER_PARAMS["n_cells"])
    grid = [hi - (hi - lo) * i / (n - 1) for i in range(n)]   # descending r/σ

    cells = []
    for ros in grid:
        r_fine = ros * sig
        A_s, floors, raws, confs, ors, abls = [], [], [], [], [], []
        for s in seeds:
            cfg = replace(base, r_fine=r_fine, sigma_stim=sig, seed=s)
            vp = run_validity_probe(cfg, pin)
            A_s.append(vp["A_salience"]); floors.append(vp["floor_B"])
            raws.append(vp["ceiling_B"]); confs.append(vp["cross_axis_confusion"])
            orc = oracle_b_rec(cfg, pin, steps=LADDER_PARAMS["oracle_steps"])
            ors.append(orc["oracle_B_rec"]); abls.append(orc["ablation_collapsed"])
        cell = dict(
            r_fine=round(r_fine, 4), r_over_sigma=round(ros, 3), sigma_stim=sig,
            oracle_substrate=statistics.mean(ors), oracle_per_seed=[round(x, 3) for x in ors],
            ablation_ok=bool(all(abls)),
            ceiling_B_raw=statistics.mean(raws), A_salience=statistics.mean(A_s),
            floor_B=statistics.mean(floors), confusion=statistics.mean(confs))
        cell["F3_prone"] = bool(cell["oracle_substrate"] < thr)
        cell["admissible"] = bool(
            cell["oracle_substrate"] >= thr + LADDER_PARAMS["bottom_margin"]
            and cell["ablation_ok"] and cell["A_salience"] >= 0.8
            and cell["floor_B"] <= chance + LADDER_PARAMS["floor_eps"])
        cells.append(cell)
        if verbose:
            print(f"  r/σ={ros:>5.2f} r_fine={r_fine:>5.3f}  oracle={cell['oracle_substrate']:.3f}"
                  f"  raw={cell['ceiling_B_raw']:.3f}  floor_B={cell['floor_B']:.3f}"
                  f"  A_sal={cell['A_salience']:.3f}  abl={cell['ablation_ok']}"
                  f"  {'ADMISSIBLE' if cell['admissible'] else ('F3' if cell['F3_prone'] else '--')}")

    admissible = [c for c in cells if c["admissible"]]
    top = admissible[0] if admissible else None
    bot = admissible[-1] if admissible else None

    # F3-bracket probes below the ladder bottom — confirm the cap can actually fire (tight bracket).
    f3_bracket = []
    for ros in LADDER_PARAMS["f3_bracket_r_over_sigma"]:
        r_fine = ros * sig
        ors, abls = [], []
        for s in seeds:
            orc = oracle_b_rec(replace(base, r_fine=r_fine, sigma_stim=sig, seed=s),
                               pin, steps=LADDER_PARAMS["oracle_steps"])
            ors.append(orc["oracle_B_rec"]); abls.append(orc["ablation_collapsed"])
        m = statistics.mean(ors)
        f3_bracket.append(dict(r_over_sigma=round(ros, 3), r_fine=round(r_fine, 4),
                               oracle_substrate=m, breaches=bool(m < thr)))
        if verbose:
            print(f"  [F3-bracket] r/σ={ros:>4.2f} r_fine={r_fine:.3f}  oracle={m:.3f}  "
                  f"breaches(<{thr:.3f})={m < thr}")

    checks = dict(
        n_admissible=len(admissible),
        ten_dense_ok=len(admissible) >= 10,
        top_not_oracle_depressed=bool(top and top["ceiling_B_raw"] >= LADDER_PARAMS["raw_clean_bar"]
                                      and top["oracle_substrate"] >= oracle_easy_ceiling - 0.10),
        bottom_brackets_F3=bool(any(c["breaches"] for c in f3_bracket)),
    )
    rec = dict(commit_hash=commit, spec_hash=calib["spec_hash"], oracle_threshold=thr,
               chance=chance, oracle_easy_ceiling=oracle_easy_ceiling,
               params=LADDER_PARAMS, cells=cells, admissible_cells=admissible,
               f3_bracket=f3_bracket, top=top, bottom=bot, checks=checks,
               LADDER_OK=bool(checks["ten_dense_ok"] and checks["top_not_oracle_depressed"]
                              and checks["bottom_brackets_F3"]))
    Path(out_path).write_text(json.dumps(rec, indent=2))
    if verbose:
        print(f"\n  admissible cells: {len(admissible)} (need ≥10)")
        if top and bot:
            print(f"  ladder span: r/σ {top['r_over_sigma']} → {bot['r_over_sigma']}  "
                  f"(oracle {top['oracle_substrate']:.3f} → {bot['oracle_substrate']:.3f})")
        print("  checks:", checks, " LADDER_OK:", rec["LADDER_OK"])
        print(f"  (record -> {out_path})")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--calib", default="calibration.json")
    ap.add_argument("--out", default="band_ladder.json")
    args = ap.parse_args()
    res = build_ladder(calib_path=args.calib, out_path=args.out)
    sys.exit(0 if res["LADDER_OK"] else 1)
