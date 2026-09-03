"""exp06 INTERIOR READ (post-gate; runs only after TRIAD_PASS and review). Deterministic computation
of the spec §4/§5 primary read over the surfaced cube cell values — NEUTRAL, no penalty-primary lens.

HARDENED (2026-06-29): the joint-vs-conjunction fork hung on the deciding cell [1,0,0], which was
unconverged at the 4000-step gate budget. `exp06_reconfirm.py` finished it (plateau, 16 seeds): the
verdict below is NO LONGER conditional — member-count is RESOLVED as tolerated-deployed (degrader, not
killer), the joint lever {cue-diffuseness, pam-pool-penalty} is LOCKED. See exp06_reconfirm.json and
FRONTIER §10.7 / PROJECT_STATE §12.E.

Computes, exactly per spec §4:
  * lifts over the dead corner for the 3 single-toggles-from-dead (undo ONE factor) and the 3
    pairs-from-dead (undo TWO factors);
  * from-dead super-additivity per pair: pair_lift > (sum of its two constituent single lifts) +
    margin, margin = K * combined within-cell seed-noise (the revival-variance calibration);
  * the §4 decision (single-factor lever / joint / irreducible-conjunction), BINARY at live_bar;
    grades are evidence only;
  * §5 redesign direction;
  * the soft-cell ROUTING check: which cell + constituents are the DECIDING measurement, and whether
    the soft (near-collapse + seed-residual) diffOnly cell lands in it. If it does -> STOP flag.

Kill-texture (penalty point-collapse vs diffuseness near-collapse) is reported as CHARACTERISATION
only; it never enters the lever arithmetic (which uses d_diff means).
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
GATE = json.load(open(_HERE / "anchor_gate.json"))
CUBE = GATE["cube_cells_RAW_DO_NOT_INTERPRET"]
BARS = GATE["calibrated_bars"]
LIVE_BAR = BARS["live_bar"]          # 0.867
ABL_FLOOR = BARS["ablation_floor"]   # 0.10
K = BARS["traverse_K"]               # 3.0
MIN_MARGIN = BARS["min_floor_margin"]  # 0.10

FACTORS = ("member-count", "cue-diffuseness", "pam-pool-penalty")
DEAD = (1, 1, 1)
CLEAN = (0, 0, 0)


def cell(code):
    return CUBE[",".join(map(str, code))]


def d(code):
    return cell(code)["d_diff"]["mean"]


def dstd(code):
    return cell(code)["d_diff"]["std"]


def revived(code):
    """§4 binary: d_diff >= live_bar AND ablation collapses (d_ablated <= ablation_floor)."""
    c = cell(code)
    return bool(c["d_diff"]["mean"] >= LIVE_BAR and c["d_ablated"]["max"] <= ABL_FLOOR)


def flip(code, idxs):
    """Return code with the given factor indices set to clean (0)."""
    out = list(code)
    for i in idxs:
        out[i] = 0
    return tuple(out)


def main():
    dead_d = d(DEAD)

    # ---- single-toggles FROM DEAD: undo exactly one factor (set it clean) ----
    singles = {}
    for i in range(3):
        code = flip(DEAD, [i])
        singles[i] = dict(code=code, d=d(code), std=dstd(code), lift=d(code) - dead_d,
                          revived=revived(code), undone_factor=FACTORS[i])

    # ---- pairs FROM DEAD: undo exactly two factors ----
    pairs = {}
    for i, j in itertools.combinations(range(3), 2):
        code = flip(DEAD, [i, j])
        s_i, s_j = singles[i], singles[j]
        lift = d(code) - dead_d
        sum_singles = s_i["lift"] + s_j["lift"]
        # margin = K * combined within-cell seed-noise of the pair cell + its two constituents
        noise = (dstd(code) ** 2 + s_i["std"] ** 2 + s_j["std"] ** 2) ** 0.5
        margin = max(K * noise, MIN_MARGIN)
        pairs[(i, j)] = dict(
            code=code, d=d(code), std=dstd(code), lift=lift, revived=revived(code),
            undone_factors=[FACTORS[i], FACTORS[j]],
            constituent_codes=[s_i["code"], s_j["code"]],
            sum_constituent_lifts=sum_singles,
            superadditive=bool(lift - sum_singles > margin),
            superadd_margin=margin, superadd_excess=lift - sum_singles)

    clean_revived = revived(CLEAN)

    # ---- §4 decision ----
    n_single_rev = [i for i in singles if singles[i]["revived"]]
    rev_pairs = [k for k in pairs if pairs[k]["revived"]]
    if n_single_rev:
        verdict = "single-factor lever"
        lever = [FACTORS[i] for i in n_single_rev]
    elif rev_pairs:
        verdict = "joint lever (pair)"
        lever = [pairs[k]["undone_factors"] for k in rev_pairs]
    elif clean_revived:
        verdict = "irreducible conjunction"
        lever = ["all three (only the full clean conjunction revives)"]
    else:
        verdict = "look-outside (nothing revived)"
        lever = []

    # ---- §5 direction ----
    DIRECTION_MAP = {
        "pam-pool-penalty": "drop/reshape the λ2-tie on PAM's own prototypes (proto-spread collapse)",
        "member-count": "redesign the multi-member completion STRUCTURE",
        "cue-diffuseness": "redesign how the CUE is posed",
    }
    if verdict == "single-factor lever":
        direction = "; ".join(DIRECTION_MAP[f] for f in lever)
    elif verdict in ("joint lever (pair)", "irreducible conjunction"):
        direction = ("re-pose PAM's COMPLETION TASK (the under-decomposed clean-2-member vs "
                     "diffuse-multi-member gap) — addresses the joint lever, not a single-factor tweak")
    else:
        direction = "look outside the three factors (carrier-even-bounded / training / task-posing)"

    # ---- soft-cell ROUTING check ----
    SOFT_CELL = (0, 1, 0)   # diffOnly: near-collapse + faint seed residual (Q3)
    deciding_pairs = rev_pairs if rev_pairs else []
    deciding_cells, deciding_constituents = set(), set()
    for k in deciding_pairs:
        deciding_cells.add(pairs[k]["code"])
        for cc in pairs[k]["constituent_codes"]:
            deciding_constituents.add(cc)
    soft_in_deciding = bool(SOFT_CELL in deciding_cells or SOFT_CELL in deciding_constituents)

    # cells sharing the diffuse near-collapse TEXTURE (diffuse=1) whose d_diff is load-bearing here
    diffuse_textured_in_deciding = [
        list(c) for c in (deciding_cells | deciding_constituents) if c[1] == 1]

    out = dict(
        commit_hash=GATE["commit_hash"], spec_hash=GATE["spec_hash"],
        live_bar=LIVE_BAR, dead_d=dead_d, clean_d=d(CLEAN), clean_revived=clean_revived,
        singles_from_dead={FACTORS[i]: {**singles[i], "code": list(singles[i]["code"])}
                           for i in singles},
        pairs_from_dead={"+".join(p["undone_factors"]):
                         {**p, "code": list(p["code"]),
                          "constituent_codes": [list(x) for x in p["constituent_codes"]]}
                         for p in pairs.values()},
        VERDICT=verdict, LEVER=lever, DIRECTION_exp07=direction,
        soft_cell_routing=dict(
            soft_cell=list(SOFT_CELL), deciding_pair_cells=[list(c) for c in deciding_cells],
            deciding_constituents=[list(c) for c in deciding_constituents],
            soft_cell_in_deciding_measurement=soft_in_deciding,
            diffuse_textured_cells_in_deciding=diffuse_textured_in_deciding),
    )
    print(json.dumps(out, indent=2))
    Path(_HERE / "exp06_interior_read.json").write_text(json.dumps(out, indent=2))

    # human-readable
    print("\n" + "=" * 78)
    print(f"§4/§5 INTERIOR READ  (live_bar={LIVE_BAR}, dead={dead_d}, clean={d(CLEAN)})")
    print("=" * 78)
    print("\nSingle-toggles FROM DEAD (undo one factor; revived = d>=live_bar & ablation collapses):")
    for i in singles:
        s = singles[i]
        print(f"  undo {s['undone_factor']:16s} {list(s['code'])} -> d={s['d']:.3f} lift={s['lift']:+.3f} "
              f"{'REVIVED' if s['revived'] else 'dead'}")
    print("\nPairs FROM DEAD (undo two factors) + super-additivity:")
    for p in pairs.values():
        print(f"  undo {'+'.join(p['undone_factors']):33s} {list(p['code'])} -> d={p['d']:.3f}±{p['std']:.2f} "
              f"lift={p['lift']:+.3f} vs Σsingles={p['sum_constituent_lifts']:+.3f} "
              f"(margin {p['superadd_margin']:.3f}) "
              f"{'SUPER-ADDITIVE' if p['superadditive'] else 'additive/none'} "
              f"{'[REVIVED]' if p['revived'] else ''}")
    print(f"\n  clean corner revived: {clean_revived}")
    print(f"\n  VERDICT: {verdict}   LEVER: {lever}")
    print(f"  exp07 DIRECTION: {direction}")
    r = out["soft_cell_routing"]
    print(f"\n  soft-cell routing: diffOnly{list(SOFT_CELL)} in deciding measurement? "
          f"{r['soft_cell_in_deciding_measurement']}")
    print(f"    deciding pair cell(s): {r['deciding_pair_cells']}  "
          f"constituents: {r['deciding_constituents']}")
    print(f"    diffuse-textured cells whose d_diff is load-bearing in the deciding pair: "
          f"{r['diffuse_textured_cells_in_deciding']}")


if __name__ == "__main__":
    main()
