"""12b block scorer — the S reads at the IN-FORCE coin-policy constants (prereg §15 as
amended + the chat ratification 2026-07-05). Constants are READ from
exp08/exp12_12b_stage2_constants.json — never re-derived here.

Per seed (per block): onset_p = the PRESENT twin's num-floor onset; UNREAD taxonomy
(unacquired | window-truncated at onset_p > horizon − W) — never a no-fire; READ: the
S series over the aligned window [onset_p, onset_p + W] from the twin pair's BOUNDED
sep columns; **FIRE := S > band_p99 for N consecutive windows** (the registered
criterion). Block outcome = the standing seed machinery: majority over read seeds;
3–2 margin or <3 read fires the +2 extension {5,6} (guard-fires-THEN-extension);
<3 read post-extension = UNREAD-AT-HORIZON → horizon re-pin returns to chat as a
recorded amendment (pre-acknowledged for the dwelled block).

Falsifier companion (never the verdict): word-re-accelerates-collapse — present-twin
routing health vs absent (asg_cat window means, den sub-floor fractions). The
post-onset-S preview lean is FENCED (logged, cal-only, constants are preview-
independent). Speed companion: onset contrasts.
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

import exp09_arms as X9                                       # noqa: E402
import exp12_arms as X12                                      # noqa: E402

OUTDIR = X12.OUTDIR
K = json.loads((OUTDIR / "exp12_12b_stage2_constants.json").read_text())
W = K["W_common"]
VERDICT_SEEDS = [0, 1, 2, 3, 4]
EXT_POOL = [5, 6]
BLOCKS = dict(sh=dict(arms=("exp12_12bc_shp", "exp12_12bc_sha")),
              dw=dict(arms=("exp12_12bc_dwp", "exp12_12bc_dwa")))


def _s_window(rp, ra, lo, hi):
    out = []
    for cp, ca in zip(rp["columns"], ra["columns"]):
        assert cp["t"] == ca["t"], "twin columns misaligned"   # hygiene (verification note)
        if not (lo <= cp["t"] <= hi):
            continue
        ok = all(cp.get(k) is not None and ca.get(k) is not None
                 for k in ("sep_cat", "sep_dist", "sep_a"))
        if not ok:
            out.append(None)
            continue
        d = {k: cp[k] - ca[k] for k in ("sep_cat", "sep_dist", "sep_a")}
        out.append(d["sep_cat"] - 0.5 * (d["sep_dist"] + d["sep_a"]))
    return out


def seed_read(block: str, seed: int) -> dict:
    armP, armA = BLOCKS[block]["arms"]
    pP, pA = OUTDIR / f"{armP}_s{seed}.json", OUTDIR / f"{armA}_s{seed}.json"
    if not (pP.exists() and pA.exists()):
        return dict(block=block, seed=seed, status="NOT RUN")
    rp, ra = json.loads(pP.read_text()), json.loads(pA.read_text())
    kb = K[block]
    horizon, band, n_sust = kb["horizon"], kb["band_p99"], kb["sustained_N"]
    onset = rp["acquisition_onset"]
    out = dict(block=block, seed=seed, onset_present=onset,
               onset_absent=ra["acquisition_onset"])
    if onset is None:
        out["status"] = "UNREAD (unacquired)"
        return out
    if onset > horizon - W:
        out["status"] = f"UNREAD (window-truncated: onset {onset} > {horizon - W})"
        return out
    S = _s_window(rp, ra, onset, onset + W)
    run = best = 0
    fire_t = None
    for i, v in enumerate(S):
        run = run + 1 if (v is not None and v > band) else 0
        best = max(best, run)
        if run >= n_sust and fire_t is None:
            fire_t = onset + (i - n_sust + 1) * X12.EVAL
    vals = [v for v in S if v is not None]
    # falsifier companion: routing health, present vs absent, same window
    def _health(r):
        win = [c for c in r["columns"] if onset <= c["t"] <= onset + W]
        return dict(asg_cat_mean=round(statistics.mean(c["asg_cat"] for c in win), 5),
                    den_subfloor=round(sum(1 for c in win if c["den"] < X9.FLOOR) / len(win), 3))
    out.update(status="READ",
               fired=bool(fire_t is not None), fire_t=fire_t,
               band=band, sustained_N=n_sust,
               S_mean=round(statistics.mean(vals), 5), S_max=round(max(vals), 5),
               S_frac_above_band=round(sum(1 for v in vals if v > band) / len(vals), 4),
               longest_run=best, n_windows=len(vals),
               collapse_falsifier=dict(present=_health(rp), absent=_health(ra)))
    return out


def block_outcome(block: str) -> dict:
    def tally(seeds):
        reads = [seed_read(block, s) for s in seeds]
        reads = [r for r in reads if r["status"] != "NOT RUN"]
        read = [r for r in reads if r["status"] == "READ"]
        f = sum(1 for r in read if r["fired"])
        return reads, read, f, len(read) - f
    reads, read, fired, nofire = tally(VERDICT_SEEDS)
    margin = (fired, nofire) in ((3, 2), (2, 3))
    shortfall = len(read) < 3
    ext = False
    if (margin or shortfall) and any(
            (OUTDIR / f"{BLOCKS[block]['arms'][0]}_s{s}.json").exists() for s in EXT_POOL):
        reads, read, fired, nofire = tally(VERDICT_SEEDS + EXT_POOL)
        ext = True
        margin = (fired, nofire) in ((3, 2), (2, 3))
        shortfall = len(read) < 3
    out = dict(block=block, per_seed=reads, n_read=len(read), fired=fired,
               nofire=nofire, extension_included=ext)
    if shortfall:
        out["outcome"] = "READ-COUNT SHORTFALL"
        out["action"] = ("fire +2 extension {5,6}" if not ext else
                         "UNREAD-AT-HORIZON (pin ii) — horizon re-pin returns to chat "
                         "as a recorded amendment (pre-acknowledged for dwelled)")
    elif margin:
        out["outcome"] = f"MARGIN {fired}-{nofire}"
        out["action"] = ("fire +2 extension {5,6} BEFORE interpretation" if not ext
                         else "extension exhausted — outcome stands at majority")
    elif fired == nofire:
        out["outcome"] = f"TIE {fired}-{nofire} (unregistered state)"
        out["action"] = "SURFACE — ruling required"
    else:
        out["outcome"] = "S-FIRES" if fired > nofire else "S-NULL"
        out["action"] = None
        out["registered_mapping"] = (
            "word-tied SELECTIVITY demonstrated in this block (the re-cut registration)"
            if fired > nofire else
            "S in the null band — falsifier (b): channel inert/unselective on this fabric")
    return out


SW_SEEDS = [5, 6, 7, 8, 9]          # §10.20.5 fresh-seed discipline
SW_EXT = [10, 11]                   # natural continuation pool (fires only on a guard)


def seed_read_w(block: str, seed: int) -> dict:
    """The §10.20.5 S_w read: FIRE := Δsep_cat(present−absent) > Sw_band_p99 for
    Sw_sustained_N consecutive windows. Companions: the untied contrasts (the
    dose-visibility check — generic dose predicts comparable positive untied contrasts;
    word-tied selectivity predicts Δcat ≫ untied), the retired composite S, and the
    health falsifier."""
    armP, armA = BLOCKS[block]["arms"]
    pP, pA = OUTDIR / f"{armP}_s{seed}.json", OUTDIR / f"{armA}_s{seed}.json"
    if not (pP.exists() and pA.exists()):
        return dict(block=block, seed=seed, status="NOT RUN")
    rp, ra = json.loads(pP.read_text()), json.loads(pA.read_text())
    kb = K[block]
    horizon, band, n_sust = kb["horizon"], kb["Sw_band_p99"], kb["Sw_sustained_N"]
    onset = rp["acquisition_onset"]
    out = dict(block=block, seed=seed, onset_present=onset,
               onset_absent=ra["acquisition_onset"])
    if onset is None:
        out["status"] = "UNREAD (unacquired)"
        return out
    if onset > horizon - W:
        out["status"] = f"UNREAD (window-truncated: onset {onset} > {horizon - W})"
        return out
    rows = []
    for cp, ca in zip(rp["columns"], ra["columns"]):
        assert cp["t"] == ca["t"], "twin columns misaligned"
        if not (onset <= cp["t"] <= onset + W):
            continue
        ok = all(cp.get(k) is not None and ca.get(k) is not None
                 for k in ("sep_cat", "sep_dist", "sep_a"))
        rows.append(None if not ok else
                    dict(sw=cp["sep_cat"] - ca["sep_cat"],
                         da=cp["sep_a"] - ca["sep_a"],
                         dd=cp["sep_dist"] - ca["sep_dist"]))
    sw = [r["sw"] for r in rows if r is not None]
    run = best = 0
    fire_t = None
    for i, r in enumerate(rows):
        run = run + 1 if (r is not None and r["sw"] > band) else 0
        best = max(best, run)
        if run >= n_sust and fire_t is None:
            fire_t = onset + (i - n_sust + 1) * X12.EVAL
    def _health(r):
        win = [c for c in r["columns"] if onset <= c["t"] <= onset + W]
        return dict(asg_cat_mean=round(statistics.mean(c["asg_cat"] for c in win), 5),
                    den_subfloor=round(sum(1 for c in win if c["den"] < X9.FLOOR) / len(win), 3))
    out.update(
        status="READ", fired=bool(fire_t is not None), fire_t=fire_t,
        band=band, sustained_N=n_sust,
        Sw_mean=round(statistics.mean(sw), 5), Sw_max=round(max(sw), 5),
        Sw_frac_above=round(sum(1 for v in sw if v > band) / len(sw), 4),
        longest_run=best, n_windows=len(sw),
        dose_visibility=dict(               # companions, never criteria
            d_a_mean=round(statistics.mean(r["da"] for r in rows if r), 5),
            d_dist_mean=round(statistics.mean(r["dd"] for r in rows if r), 5),
            composite_S_mean=round(statistics.mean(
                r["sw"] - 0.5 * (r["da"] + r["dd"]) for r in rows if r), 5)),
        collapse_falsifier=dict(present=_health(rp), absent=_health(ra)))
    return out


def block_outcome_w(block: str) -> dict:
    def tally(seeds):
        reads = [seed_read_w(block, s) for s in seeds]
        reads = [r for r in reads if r["status"] != "NOT RUN"]
        read = [r for r in reads if r["status"] == "READ"]
        f = sum(1 for r in read if r["fired"])
        return reads, read, f, len(read) - f
    reads, read, fired, nofire = tally(SW_SEEDS)
    margin = (fired, nofire) in ((3, 2), (2, 3))
    shortfall = len(read) < 3
    ext = False
    if (margin or shortfall) and any(
            (OUTDIR / f"{BLOCKS[block]['arms'][0]}_s{s}.json").exists() for s in SW_EXT):
        reads, read, fired, nofire = tally(SW_SEEDS + SW_EXT)
        ext = True
        margin = (fired, nofire) in ((3, 2), (2, 3))
        shortfall = len(read) < 3
    out = dict(block=block, ruler="S_w (§10.20.5)", per_seed=reads, n_read=len(read),
               fired=fired, nofire=nofire, extension_included=ext)
    if shortfall:
        out["outcome"] = "READ-COUNT SHORTFALL"
        out["action"] = ("fire {10,11} continuation" if not ext else
                         "UNREAD-AT-HORIZON (pin ii) — horizon re-pin returns to chat")
    elif margin:
        out["outcome"] = f"MARGIN {fired}-{nofire}"
        out["action"] = ("fire {10,11} continuation BEFORE interpretation" if not ext
                         else "continuation exhausted — outcome stands at majority")
    elif fired == nofire:
        out["outcome"] = f"TIE {fired}-{nofire} (unregistered state)"
        out["action"] = "SURFACE — ruling required"
    else:
        out["outcome"] = "S_w-FIRES" if fired > nofire else "S_w-NULL"
        out["action"] = None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sw", action="store_true", help="the §10.20.5 S_w read on {5–9}")
    args = ap.parse_args()
    if args.sw:
        res = {b: block_outcome_w(b) for b in BLOCKS}
        (OUTDIR / "exp12_12b_sw_verdicts.json").write_text(json.dumps(res, indent=2))
        for b, r in res.items():
            print(f"[{b}] {r['outcome']} (read {r['n_read']}: {r['fired']}F/{r['nofire']}N)"
                  f"{'  ACTION: ' + r['action'] if r['action'] else ''}")
            for p in r["per_seed"]:
                if p["status"] == "READ":
                    dv = p["dose_visibility"]
                    print(f"  s{p['seed']}: READ fired={p['fired']} Sw_mean={p['Sw_mean']} "
                          f"Sw_max={p['Sw_max']} frac>band={p['Sw_frac_above']} "
                          f"run={p['longest_run']}/{p['sustained_N']} onset={p['onset_present']} "
                          f"| dose-vis dA={dv['d_a_mean']} dDist={dv['d_dist_mean']}")
                else:
                    print(f"  s{p['seed']}: {p['status']} onset_p={p.get('onset_present')}")
        return
    res = {b: block_outcome(b) for b in BLOCKS}
    (OUTDIR / "exp12_12b_verdicts.json").write_text(json.dumps(res, indent=2))
    for b, r in res.items():
        print(f"[{b}] {r['outcome']} (read {r['n_read']}: {r['fired']}F/{r['nofire']}N)"
              f"{'  ACTION: ' + r['action'] if r['action'] else ''}")
        for p in r["per_seed"]:
            if p["status"] == "READ":
                print(f"  s{p['seed']}: READ fired={p['fired']} S_mean={p['S_mean']} "
                      f"S_max={p['S_max']} frac>band={p['S_frac_above_band']} "
                      f"run={p['longest_run']}/{p['sustained_N']} onset={p['onset_present']}")
            else:
                print(f"  s{p['seed']}: {p['status']} onset_p={p.get('onset_present')}")


if __name__ == "__main__":
    main()
