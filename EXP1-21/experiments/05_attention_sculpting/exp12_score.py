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


def _tally(arm: str, seeds: list[int]) -> tuple[list, list, int, int]:
    reads = [seed_read(arm, s) for s in seeds
             if (OUTDIR / f"{arm}_s{s}.json").exists()]
    read = [r for r in reads if r["status"] == "READ"]
    surv = sum(1 for r in read if r["survives"])
    return reads, read, surv, len(read) - surv


def arm_outcome(arm: str) -> dict:
    """Guard letters EXACTLY as ratified (verification catch 2026-07-05, two latent
    defects fixed unexercised): (a) the margin guard fires on a 3–2 split ONLY (not
    2–1/2–2/ties — those are not registered guard states); (b) extension seeds {5,6}
    enter the read ONLY when a guard actually fired on the base read (guard-fires-THEN-
    extension; stray artifacts never contaminate the majority silently)."""
    reads, read, surv, dies = _tally(arm, X12.VERDICT_SEEDS)
    shortfall = len(read) < 3
    margin = (surv, dies) in ((3, 2), (2, 3))
    ext_used = False
    if (shortfall or margin) and any(
            (OUTDIR / f"{arm}_s{s}.json").exists() for s in X12.EXT_POOL):
        reads, read, surv, dies = _tally(arm, X12.VERDICT_SEEDS + X12.EXT_POOL)
        ext_used = True
        shortfall = len(read) < 3
        margin = (surv, dies) in ((3, 2), (2, 3))
    out = dict(arm=arm, seeds_run=[r["seed"] for r in reads], per_seed=reads,
               n_read=len(read), survives=surv, dies=dies,
               extension_included=ext_used)
    if shortfall:
        out["outcome"] = "READ-COUNT SHORTFALL"
        out["action"] = ("fire +2 extension {5,6}" if not ext_used else
                         "UNREAD-AT-HORIZON (pin ii) — horizon re-pin as recorded amendment")
    elif margin:
        out["outcome"] = f"MARGIN {surv}-{dies}"
        out["action"] = ("fire +2 extension {5,6} BEFORE table interpretation"
                         if not ext_used else
                         "extension exhausted — outcome stands at majority")
    elif surv == dies:
        out["outcome"] = f"TIE {surv}-{dies} (unregistered state)"
        out["action"] = "SURFACE — no registered guard covers a tie; ruling required"
    else:
        out["outcome"] = "SURVIVES" if surv > dies else "DIES"
        out["action"] = None
    return out


def split_outcome() -> dict:
    """The SPLITTING-ARM read at the §14 registered letter (committed producer —
    verification catch 2026-07-05: the discriminator-scale guard letter had no
    implementation on record). Seeds {0,1,2}; a 2–1 split among read seeds, or <3 read,
    fires the {3,4} backfill BEFORE interpretation; <3 read post-backfill =
    UNREAD-AT-HORIZON."""
    def tally(seeds):
        reads = [seed_read("exp12_split", s) for s in seeds
                 if (OUTDIR / f"exp12_split_s{s}.json").exists()]
        read = [r for r in reads if r["status"] == "READ"]
        surv = sum(1 for r in read if r["survives"])
        return reads, read, surv, len(read) - surv
    reads, read, surv, dies = tally([0, 1, 2])
    margin = (surv, dies) in ((2, 1), (1, 2))
    shortfall = len(read) < 3
    backfilled = False
    if (margin or shortfall) and any(
            (OUTDIR / f"exp12_split_s{s}.json").exists() for s in (3, 4)):
        reads, read, surv, dies = tally([0, 1, 2, 3, 4])
        backfilled = True
        margin = (surv, dies) in ((2, 1), (1, 2))
        shortfall = len(read) < 3
    out = dict(arm="exp12_split", per_seed=reads, n_read=len(read),
               survives=surv, dies=dies, backfilled=backfilled)
    if shortfall:
        out["outcome"] = "READ-COUNT SHORTFALL"
        out["action"] = ("fire {3,4} backfill" if not backfilled else
                         "UNREAD-AT-HORIZON — horizon re-pin as recorded amendment")
    elif margin:
        out["outcome"] = f"MARGIN {surv}-{dies}"
        out["action"] = ("fire {3,4} backfill BEFORE interpretation" if not backfilled
                         else "backfill exhausted — outcome stands at majority")
    elif surv == dies:
        out["outcome"] = f"TIE {surv}-{dies} (unregistered state)"
        out["action"] = "SURFACE — ruling required"
    else:
        out["outcome"] = "SURVIVES" if surv > dies else "DIES"
        out["action"] = None
        out["registered_mapping"] = (
            "VARIATION ALONE SUFFICES on the registered ruler (W_post-mean survival)"
            if surv > dies else "EXAM SCHEDULING LOAD-BEARING")
    (OUTDIR / "exp12_split_read.json").write_text(json.dumps(out, indent=2))
    print(f"A-SPLIT: {out['outcome']} (read {out['n_read']}: {surv}S/{dies}D)"
          f"{'  ACTION: ' + out['action'] if out['action'] else ''}")
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
    ap.add_argument("--split", action="store_true", help="score the §14 splitting arm")
    args = ap.parse_args()
    if args.split:
        split_outcome()
        return
    res = {a: arm_outcome(a) for a in X12.RIG1_ARMS}
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
