"""EXP12 verdict scorer — the four-cell read at the IN-FORCE stage-two constants
(exp08/exp12_stage2_constants.json, ratified 2026-07-05; NOTHING here is re-derived —
every constant is READ from the artifact).

Per-seed read (the ratified criteria + taxonomy):
  * onset = num-floor acquisition (§13.4, pinned form).
  * UNREAD taxonomy (never a dies): unacquired (onset never fires) | window-truncated
    (onset > horizon − W_post; pin i).
  * SURVIVES := mean asg_cat over [onset, onset + W_post] >= theta (window MEAN,
    pinned form); frac-alive companion logged.
Arm outcome: majority over READ seeds; MARGIN GUARD: a 3–2 split among read seeds, or a
read-count shortfall (<3 read), fires the +2 extension {5,6} BEFORE any table
interpretation; <3 read POST-extension = UNREAD-AT-HORIZON (pin ii; escalation =
horizon re-pin as recorded amendment).

Companions (never cell-deciders): exam-conversion onset (chance-band form, Ruling 2:
the sensitivity-without-conversion dissociation); exam lift window mean; 16-member
asg_dist / argmax_k / entropy window means; den tripwire fraction; the §13.10 monitor
(scheduled vs probe exam lift at matched acquisition — registered divergence fires
fallback (c), report-only); earned-salience early-vs-late background divergence.

The four-cell mapping runs ONLY after the margin guard clears, and the printed cell is
a DRAFT — it goes behind the verification pass before it reaches the table (one review).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp09_arms as X9                                       # noqa: E402  (FLOOR tripwire)
import exp12_arms as X12                                      # noqa: E402

OUTDIR = X12.OUTDIR
K = json.loads((OUTDIR / "exp12_stage2_constants.json").read_text())
THETA = K["survival"]["theta"]
W_POST = K["w_post"]["value"]
HORIZON = K["verdict_horizon"]["value"]
CONV_THR = K["exam_conversion"]["threshold"]
CONV_CONSEC = K["exam_conversion"]["consec"]
READ_CUTOFF = HORIZON - W_POST


def _conv_onset(cols):
    run = 0
    for c in cols:
        ok = c.get("exam_acc") is not None and c["exam_acc"] >= CONV_THR
        run = run + 1 if ok else 0
        if run >= CONV_CONSEC:
            return c["t"] - (CONV_CONSEC - 1) * X12.EVAL
    return None


def seed_read(arm: str, seed: int) -> dict:
    rec = json.loads((OUTDIR / f"{arm}_s{seed}.json").read_text())
    cols = rec["columns"]
    onset = rec["acquisition_onset"]
    out = dict(arm=arm, seed=seed, onset=onset,
               exam_conversion_onset=_conv_onset(cols))
    if onset is None:
        out["status"] = "UNREAD (unacquired)"
        return out
    if onset > READ_CUTOFF:
        out["status"] = f"UNREAD (window-truncated: onset {onset} > {READ_CUTOFF})"
        return out
    win = [c for c in cols if onset <= c["t"] <= onset + W_POST]
    asg = [c["asg_cat"] for c in win]
    m = statistics.mean(asg)
    out.update(
        status="READ",
        survives=bool(m >= THETA),
        asg_cat_mean=round(m, 6), theta=THETA,
        asg_cat_frac_above=round(sum(1 for a in asg if a >= THETA) / len(asg), 4),
        n_windows=len(win),
        companions=dict(
            asg_dist_mean=round(statistics.mean(c["asg_dist"] for c in win), 4),
            argmax_k_med=statistics.median(c["asg_argmax_k"] for c in win),
            asg_entropy_mean=round(statistics.mean(c["asg_entropy"] for c in win), 4),
            den_subfloor_frac=round(sum(1 for c in win if c["den"] < X9.FLOOR) / len(win), 4),
            exam_lift_mean=round(statistics.mean(
                c["exam_lift"] for c in win if c.get("exam_lift") is not None), 4),
            exam_acc_mean=round(statistics.mean(
                c["exam_acc"] for c in win if c.get("exam_acc") is not None), 4),
            mid_word_lift_mean=round(statistics.mean(
                c["mid_word_lift"] for c in win if c.get("mid_word_lift") is not None), 4),
            monitor_13_10=dict(
                scheduled_lift=round(statistics.mean(
                    c["exam_lift"] for c in win if c.get("exam_lift") is not None), 4),
                probe_lift=(round(statistics.mean(
                    c["probe_exam_lift"] for c in win
                    if c.get("probe_exam_lift") is not None), 4)
                    if any(c.get("probe_exam_lift") is not None for c in win) else None)),
            earned_salience=dict(
                div_bg_first5=round(statistics.mean(
                    [c["div_bg"] for c in cols if c.get("div_bg") is not None][:5]), 4),
                div_bg_last5=round(statistics.mean(
                    [c["div_bg"] for c in cols if c.get("div_bg") is not None][-5:]), 4),
                div_id_last5=round(statistics.mean(
                    [c["div_id"] for c in cols if c.get("div_id") is not None][-5:]), 4))))
    return out


def arm_outcome(arm: str, seeds: list[int]) -> dict:
    reads = [seed_read(arm, s) for s in seeds
             if (OUTDIR / f"{arm}_s{s}.json").exists()]
    read = [r for r in reads if r["status"] == "READ"]
    surv = sum(1 for r in read if r["survives"])
    dies = len(read) - surv
    out = dict(arm=arm, seeds_run=[r["seed"] for r in reads], per_seed=reads,
               n_read=len(read), survives=surv, dies=dies)
    if len(read) < 3:
        out["outcome"] = "READ-COUNT SHORTFALL"
        out["action"] = ("fire +2 extension {5,6}" if not set(X12.EXT_POOL) <=
                         set(r["seed"] for r in reads) else
                         "UNREAD-AT-HORIZON (pin ii) — horizon re-pin as recorded amendment")
    elif min(surv, dies) > 0 and abs(surv - dies) <= 1:
        out["outcome"] = f"MARGIN {surv}-{dies}"
        out["action"] = ("fire +2 extension {5,6} BEFORE table interpretation"
                         if not set(X12.EXT_POOL) <= set(r["seed"] for r in reads)
                         else "extension exhausted — outcome stands at majority")
    else:
        out["outcome"] = "SURVIVES" if surv > dies else "DIES"
        out["action"] = None
    return out


CELLS = {
    ("SURVIVES", "DIES"): "PROMOTE-THE-ROOT (dwell survives / shuffled dies)",
    ("SURVIVES", "SURVIVES"): "BOTH-SURVIVE (variation + exam-scheduling jointly suffice; "
                              "splitting arm fires)",
    ("DIES", "DIES"): "BOTH-DIE (ordering alone insufficient — NOT root-refutation; "
                      "§8 escalation ladder)",
    ("DIES", "SURVIVES"): "ANOMALY (inversion — Fork 1.5 geometry audit + recency-channel "
                          "check; named finding only)",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=X12.VERDICT_SEEDS)
    args = ap.parse_args()
    res = {a: arm_outcome(a, args.seeds + X12.EXT_POOL) for a in X12.ARMS12}
    d, s = res["exp12_dwell"], res["exp12_shuffle"]
    pending = [a for a, r in res.items() if r["action"]]
    table = None
    if not pending and d["outcome"] in ("SURVIVES", "DIES") and s["outcome"] in ("SURVIVES", "DIES"):
        table = CELLS[(d["outcome"], s["outcome"])]
    out = dict(constants_in_force=dict(theta=THETA, w_post=W_POST, horizon=HORIZON,
                                       read_cutoff=READ_CUTOFF, conv=CONV_THR),
               arms=res, guards_pending=pending,
               draft_cell=(table if table else "TABLE NOT INTERPRETABLE YET (guards pending)"),
               note="DRAFT — goes behind the verification pass before the table (one review)")
    (OUTDIR / "exp12_verdicts.json").write_text(json.dumps(out, indent=2))
    for a, r in res.items():
        print(f"{a}: {r['outcome']}  (read {r['n_read']}: {r['survives']}S/{r['dies']}D)"
              f"{'  ACTION: ' + r['action'] if r['action'] else ''}")
        for p in r["per_seed"]:
            line = (f"  s{p['seed']}: {p['status']}"
                    + (f"  asg_cat={p['asg_cat_mean']} vs θ={THETA:.5f} -> "
                       f"{'SURVIVES' if p.get('survives') else 'DIES'}"
                       if p["status"] == "READ" else "")
                    + f"  onset={p['onset']} conv={p['exam_conversion_onset']}")
            print(line)
    print("DRAFT CELL:", out["draft_cell"])


if __name__ == "__main__":
    main()
