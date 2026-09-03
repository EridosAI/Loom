"""Earned-salience read — the registered Amendment-A observable (prereg §Amendment A =
FRONTIER §10.19), read form recorded in §10.20.7 BEFORE this read produced a number.
EXPECTATION, NOT A GATE: a non-landing changes no committed verdict; the read feeds only
the second leg of the Guiding-List promotion trigger.

Registered sentence: "PAM divergence on background axes FALLS with exposure while
member-onset divergence STAYS HIGH." Rig-1 readout, existing verdict artifacts {0-4},
both arms (A-DWELL, A-SHUFFLE), no new runs. Columns are the registered ones: the pos-1
member-onset exam prediction-divergence components div_bg / div_id (div_nuis companion);
exposure axis = wave t (fixed background from wave 0).

Read form (§10.20.7): per seed, EARLY = mean over the first decile of div-bearing
columns, LATE = mean over the last decile; full-series least-squares slope as trend
companion. FALLS(bg) := late/early < 0.7 AND slope < 0. STAYS_HIGH(id) := late/early
> 0.7 (symmetric knob, declared illustrative — full ratios/slopes reported so the
letter can be re-cut by ruling without re-measurement). LANDS := FALLS(bg) AND
STAYS_HIGH(id); arm letter = majority of 5, borderlines surfaced not force-lettered.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

_HERE = Path(__file__).resolve().parent
OUTDIR = _HERE / "exp08"

ARMS = {"dwell": "exp12_dwell", "shuffle": "exp12_shuffle"}
SEEDS = [0, 1, 2, 3, 4]                 # rig-1 verdict seeds
KNOB = 0.7                              # §10.20.7 symmetric ratio knob (illustrative)


def _ls_slope(ts, vs):
    n = len(ts)
    mt, mv = statistics.mean(ts), statistics.mean(vs)
    den = sum((t - mt) ** 2 for t in ts)
    return sum((t - mt) * (v - mv) for t, v in zip(ts, vs)) / den if den else 0.0


def seed_read(arm: str, seed: int) -> dict:
    path = OUTDIR / f"{ARMS[arm]}_s{seed}.json"
    cols = json.load(open(path))["columns"]
    rows = [c for c in cols if c.get("div_bg") is not None]
    n = len(rows)
    dec = max(1, n // 10)
    out = dict(arm=arm, seed=seed, n_div_rows=n, decile=dec,
               t_first=rows[0]["t"], t_last=rows[-1]["t"])
    for k in ("div_bg", "div_id", "div_nuis"):
        early = statistics.mean(r[k] for r in rows[:dec])
        late = statistics.mean(r[k] for r in rows[-dec:])
        slope = _ls_slope([r["t"] for r in rows], [r[k] for r in rows])
        out[k] = dict(early=round(early, 6), late=round(late, 6),
                      ratio=round(late / early, 4) if early else None,
                      slope_per_100k=round(slope * 1e5, 6))
    falls_bg = out["div_bg"]["ratio"] is not None and \
        out["div_bg"]["ratio"] < KNOB and out["div_bg"]["slope_per_100k"] < 0
    stays_id = out["div_id"]["ratio"] is not None and out["div_id"]["ratio"] > KNOB
    out.update(falls_bg=falls_bg, stays_high_id=stays_id,
               lands=bool(falls_bg and stays_id))
    return out


def main():
    res = {}
    for arm in ARMS:
        reads = [seed_read(arm, s) for s in SEEDS]
        lands = sum(1 for r in reads if r["lands"])
        res[arm] = dict(per_seed=reads, lands=lands, n=len(reads),
                        letter="LANDS" if lands > len(reads) / 2 else "DOES-NOT-LAND")
    out = dict(read="earned-salience (Amendment A; §10.20.7 form)",
               expectation_not_a_gate=True, knob=KNOB, arms=res)
    (OUTDIR / "exp12_salience_read.json").write_text(json.dumps(out, indent=1))
    for arm, r in res.items():
        print(f"[{arm}] {r['letter']} ({r['lands']}/{r['n']})")
        for s in r["per_seed"]:
            print(f"  s{s['seed']}: bg {s['div_bg']['early']:.4f}->"
                  f"{s['div_bg']['late']:.4f} r={s['div_bg']['ratio']} "
                  f"sl={s['div_bg']['slope_per_100k']:+.4f} | "
                  f"id {s['div_id']['early']:.4f}->{s['div_id']['late']:.4f} "
                  f"r={s['div_id']['ratio']} | nuis r={s['div_nuis']['ratio']} "
                  f"| {'LANDS' if s['lands'] else ('no-fall' if not s['falls_bg'] else 'id-fell')}")


if __name__ == "__main__":
    main()
