"""FREE-READ (iv) — EXP13 KINEMATICS: "was the wall kinematic?"

Memo: docs/FREE_READS_MEMO.md §(iv).  Recipe: PROJECT_OPS_POSITIONING.md §1 item 6 (the user's
"OPS §6.5") — run the committed EXP17 kinematics measurer over EXP13's lawful fabric (read-only).

Implementation: the COMMITTED measurer exp17_score.measure_kinematics is run UNCHANGED; only its
fabric source (exp17_score._fabric) is redirected to exp13_arms.build_exp13 so the identical
per-dwell net/path (f64), per-axis traverse (f32 radii), path, and per-step (stat1) recipe applies to
EXP13's lawful fabric. Both EXP13 core arms are measured at a MATCHED window (lawful vs lawscram) so
the directedness comparison is like-for-like; the "kinematic?" judgment routes to the seat.

Deterministic build (torch threads=1). One JSON.
"""
import json, statistics
from pathlib import Path

import exp17_score as S                              # committed measurer (threads=1 set on import)
import exp13_arms as XA13                            # committed EXP13 fabric builder

HERE = Path(__file__).resolve().parent
OUT = HERE / "exp08"
ARMS = ["exp13_lawful", "exp13_lawscram"]            # CORE_ARMS (exp13_arms)
SEEDS = list(range(8))
WINDOW = 100_000
FIELDS = ["np11", "tr11", "tr11_max", "path11", "perstep_med", "cross_med", "n_dwells", "n11"]


def measure(arm, seed, steps, window):
    """Committed exp17_score.measure_kinematics, fabric-source redirected to EXP13's lawful fabric."""
    orig = S._fabric
    S._fabric = lambda a, sd, st: XA13.build_exp13(arm, sd, st)[0].stream
    try:
        return S.measure_kinematics(arm, seed, steps, window)
    finally:
        S._fabric = orig


def _pooled(rows, f):
    xs = [r[f] for r in rows if r.get(f) is not None]
    return round(statistics.mean(xs), 6) if xs else None


def main():
    arms_out = {}
    for arm in ARMS:
        per = []
        for s in SEEDS:
            r = measure(arm, s, WINDOW, WINDOW)
            per.append({k: r[k] for k in (["arm", "seed"] + FIELDS)})
        arms_out[arm] = dict(pooled={f: _pooled(per, f) for f in FIELDS}, per_seed=per)
    law = arms_out["exp13_lawful"]["pooled"]
    scr = arms_out["exp13_lawscram"]["pooled"]
    contrast = dict(
        np11_lawful=law["np11"], np11_lawscram=scr["np11"],
        np11_lawful_minus_scram=(round(law["np11"] - scr["np11"], 6)
                                 if law["np11"] is not None and scr["np11"] is not None else None),
        tr11_lawful=law["tr11"], tr11_lawscram=scr["tr11"])
    out = dict(
        read="(iv) EXP13 kinematics — was the wall kinematic?",
        memo_section="docs/FREE_READS_MEMO.md §(iv)",
        recipe="PROJECT_OPS_POSITIONING.md §1 item 6",
        method=("exp17_score.measure_kinematics (committed) UNCHANGED, fabric source redirected to "
                "exp13_arms.build_exp13(<arm>). np11/tr11/path11 restricted to realized k==11 dwells, "
                "contained-dwell recipe; net/path f64, traverse f32 radii, per-step stat1 f64."),
        inputs=dict(arms=ARMS, seeds=SEEDS, window=WINDOW, steps=WINDOW,
                    code_modules=["exp17_score.py", "exp13_arms.py", "exp13_fabric.py",
                                  "exp12_fabric.py"]),
        consequence=dict(
            memo_condition="a kinematic EXP13 wall bridges the lawful-dynamics line to the "
                           "SCATTER/ladder kinematics reading; a non-kinematic wall keeps EXP13 a "
                           "separate paused coordinate. Either way routes to the seat; EXP13's paused "
                           "status changes only by ruling.",
            matched_window_contrast=contrast,
            triggered="ROUTES (judgment): lawful-vs-lawscram np11/tr11 reported at a matched window; "
                      "the seat rules 'kinematic?'."),
        matched_window_contrast=contrast,
        arms=arms_out)
    OUT.mkdir(exist_ok=True)
    (OUT / "freeread_4_exp13_kinematics.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print("exp13 lawful np11=%.4f tr11=%.4f | lawscram np11=%.4f tr11=%.4f | dnp11=%s"
          % (law["np11"], law["tr11"], scr["np11"], scr["tr11"], contrast["np11_lawful_minus_scram"]))
    print("-> exp08/freeread_4_exp13_kinematics.json")


if __name__ == "__main__":
    main()
