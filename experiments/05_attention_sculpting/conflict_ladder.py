"""Conflict-strength ladder (Stage-1, SPEC §2 — the dense axis). Probe-only (no full training),
committed only after Step-0 conflict-validity passes (reads its oracle_threshold).

Sweeps the category salience r_category DOWN at fixed r_distractor (conflict_strength =
r_distractor/r_category rises): top = mild (category nearly as salient as distractor); bottom ~=
where the category oracle (check b) starts to fail. Each admissible cell has: category
oracle-representable (>= threshold, content-ablation-guarded) AND the distractor more raw-salient
than the category (the salience conflict). >= N dense steps + F3-bracket probes below to confirm
the oracle CAN fail. The conflict_strength is the swept knob; vision-alone occupancy is a sweep
OUTPUT (measured later on the deployed arms), not a ladder input.

Writes conflict_ladder.json {oracle_threshold, cells[...], admissible_cells, bracket, top, bottom,
checks, LADDER_OK}.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

import constants                                             # noqa: E402  (exp04)
from oracle_probe import _commit_hash                        # noqa: E402  (exp04)

from sculpt_config import SculptConfig, quick_sculpt         # noqa: E402  (exp05)
from category_oracle import category_oracle_rec, raw_axis_recovery  # noqa: E402  (exp05)

LADDER_PARAMS = dict(
    seeds=[0, 1, 2],
    n_cells=12,                      # dense steps in r_category
    r_distractor=3.0, sigma_stim=0.20, n_A=4, n_distractor=2, n_category=2, R_coarse=5.0,
    r_category_top=2.7,             # mild conflict (~0.9*r_distractor: category nearly as salient)
    r_category_bottom=0.30,         # near where the binary-category oracle approaches threshold
    f3_bracket=[0.22, 0.16, 0.12],  # below the ladder: confirm the oracle CAN fail (F3-analog)
    oracle_steps=600,
    bottom_margin=0.03,             # admissible needs oracle >= threshold + this
    raw_distractor_bar=0.80,        # distractor must be cleanly raw-salient
    conflict_margin=0.05,           # raw_distractor - raw_category >= this (a real salience gap)
)


def _cfg(seed, r_category, *, quick=False):
    P = LADDER_PARAMS
    cell = dict(n_A=P["n_A"], n_distractor=P["n_distractor"], n_category=P["n_category"],
                R_coarse=P["R_coarse"], r_distractor=P["r_distractor"], r_category=r_category,
                sigma_stim=P["sigma_stim"], seed=seed)
    return quick_sculpt(**cell) if quick else SculptConfig(**cell)


def _probe_cell(r_category, threshold, *, quick=False):
    P = LADDER_PARAMS
    pin = constants.PinnedConstants()
    steps = 150 if quick else P["oracle_steps"]
    oks, recs, raw_d, raw_c = [], [], [], []
    for s in P["seeds"]:
        cfg = _cfg(s, r_category, quick=quick)
        orc = category_oracle_rec(cfg, pin, steps=steps)
        recs.append(orc["oracle_category_rec"]); oks.append(orc["ablation_collapsed"])
        raw_d.append(raw_axis_recovery(cfg, axis="distractor"))
        raw_c.append(raw_axis_recovery(cfg, axis="category"))
    oracle = statistics.mean(recs)
    rd, rc = statistics.mean(raw_d), statistics.mean(raw_c)
    ablation_ok = all(oks)
    admissible = bool(oracle >= threshold + P["bottom_margin"] and ablation_ok
                      and rd >= P["raw_distractor_bar"] and (rd - rc) >= P["conflict_margin"])
    return dict(r_category=r_category, conflict_strength=P["r_distractor"] / r_category,
                oracle_category=oracle, oracle_per_seed=recs, ablation_ok=ablation_ok,
                raw_distractor=rd, raw_category=rc, salience_gap=rd - rc,
                F3_prone=bool(oracle < threshold), admissible=admissible)


def build_ladder(validity_path="conflict_validity.json", out_path="conflict_ladder.json",
                 verbose=True, quick=False) -> dict:
    P = LADDER_PARAMS
    vp = json.loads(Path(validity_path).read_text())
    threshold = vp["check_b_representable"]["oracle_threshold"]
    easy_ceiling = vp["check_b_representable"]["easy_ceiling"]
    chance = vp["chance_category"]

    grid = [P["r_category_top"] - (P["r_category_top"] - P["r_category_bottom"]) * i / (P["n_cells"] - 1)
            for i in range(P["n_cells"])]
    cells = [_probe_cell(r, threshold, quick=quick) for r in grid]
    if verbose:
        for c in cells:
            print(f"  r_cat={c['r_category']:.3f} (strength {c['conflict_strength']:.1f}): "
                  f"oracle={c['oracle_category']:.3f} raw_d={c['raw_distractor']:.3f} "
                  f"raw_c={c['raw_category']:.3f} gap={c['salience_gap']:.3f} "
                  f"adm={c['admissible']}")

    bracket = [dict(r_category=r, conflict_strength=P["r_distractor"] / r,
                    oracle_category=(o := _probe_cell(r, threshold, quick=quick))["oracle_category"],
                    breaches=bool(o["oracle_category"] < threshold))
               for r in P["f3_bracket"]]

    admissible = [c for c in cells if c["admissible"]]
    checks = dict(
        n_admissible=len(admissible),
        ten_dense_ok=len(admissible) >= 10,
        top_representable=bool(cells[0]["oracle_category"] >= easy_ceiling - 0.10
                               and cells[0]["admissible"]),
        bottom_brackets_F3=bool(any(b["breaches"] for b in bracket)),
    )
    ladder_ok = bool(checks["ten_dense_ok"] and checks["top_representable"]
                     and checks["bottom_brackets_F3"])

    rec = dict(commit_hash=_commit_hash(), spec_hash=vp["spec_hash"], quick=quick,
               oracle_threshold=threshold, easy_ceiling=easy_ceiling, chance=chance,
               params=P, cells=cells, admissible_cells=admissible, bracket=bracket,
               top=(admissible[0] if admissible else None),
               bottom=(admissible[-1] if admissible else None),
               checks=checks, LADDER_OK=ladder_ok)
    Path(out_path).write_text(json.dumps(rec, indent=2))
    if verbose:
        print(f"\n=== conflict ladder (commit {rec['commit_hash'][:7]}) ===")
        print(f"  n_admissible={checks['n_admissible']} (>=10? {checks['ten_dense_ok']}) "
              f"top_representable={checks['top_representable']} bracket_F3={checks['bottom_brackets_F3']}")
        print(f"  LADDER_OK={ladder_ok}  (record -> {out_path})")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--validity", default="conflict_validity.json")
    ap.add_argument("--out", default="conflict_ladder.json")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    res = build_ladder(validity_path=args.validity, out_path=args.out, quick=args.smoke)
    sys.exit(0 if res["LADDER_OK"] else 1)
