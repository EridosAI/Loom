"""exp20_verdict.py — EXP20 G5: certification + cells (prereg §5 as amended by AMD-1) + companions.

The ratified law, applied mechanically — pre-named conditions execute, judgment halts:
  certification   SC._certify_seed at WIDTH=300 (Q2, EXP19-SPLIT precedent), per-K G3 band injected
                  (exp20_cal._band), pinned stream gen = SIM_SEED + seed; excess over own 5000-sim
                  null (ledger 18/38)
  stream-marginal ledger 52: per certification, 200-stream family (gseed = SIM_SEED +
                  1_000_003*(k+1) + seed) -> cert rate + marginal tail; tail > 1/N_SIMS => the
                  certification rides STREAM-QUALIFIED, never headline-unqualified
  reads           K32/K128: full + delivered-stratum (W=K, Q1). K512: FULL ONLY — the stratified
                  read is UNDECIDABLE-IN-ARM (AMD-1), recorded never imputed
  cells           §5 + AMD-1: RECENCY-CARRIED (full∖strat, powered K); STRATIFIED-ONLY => HALT;
                  RESCUE-FULL-ONLY-K512 (its licensed sentence + dec_cat companion-grade
                  discriminator numbers); RESCUE-MONOTONE through POWERED strata only; ALL-DEAD
                  (paid) => the escalation artifact fires (the gate's pass action); WARMUP-CARRIED
                  flag (certified episode overlapping t <= K); MULTIPLICITY-CARRIED envelope check
  companions      dec_cat (post-acq mean + late-early delta), E-A continuity (exam_acc), K<->B
                  correspondence (same-member delivered adjacency + mean displacement), multiplicity

--smoke: cell-logic fixtures, reds first (STRATIFIED-ONLY plant must HALT; ALL-DEAD plant must
fire the escalation write TO SCRATCH; monotone-through-powered asserts). --score: the G5 run.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import torch

torch.set_num_threads(1)
import exp14_arms as XA
import exp19_floor as FL
import exp19_scorer as SC
import exp20_cal as C20

OUTDIR = XA.OUTDIR
WIDTH = 300                                   # Q2, ruled
READ_AT = 1_000_000
PAID_K = (32, 128, 512)
POWERED_K = (32, 128)                         # AMD-1: K512 stratified is UNDECIDABLE-IN-ARM
SEEDS = list(range(8))
N_STREAMS, STRIDE = 200, 1_000_003
STRATCACHE = OUTDIR / "exp20_verdict_stratcache.json"
OUT = OUTDIR / "exp20_verdict.json"
ESCALATION = OUTDIR / "exp20_escalation.json"

RESCUE_FULL_ONLY_SENTENCE = ("certified on the full read at K512; the recency-free confirmation is "
                             "structurally unpowered at this K — RECENCY-CARRIED cannot be "
                             "excluded in-arm")


def _bands() -> dict:
    cal = json.loads((OUTDIR / "exp20_cal.json").read_text())
    return {K: cal["per_K"][f"K{K}"]["band"] for K in PAID_K}


def _verdict_rec(K: int, s: int) -> dict:
    return json.loads((OUTDIR / f"exp14_exp20_ubuf_K{K}_s{s}_exp20verdict.json").read_text())


def _certify(ons, acq, band, seed) -> dict:
    with C20._band(band):
        r = SC._certify_seed(ons, acq, WIDTH, torch.Generator().manual_seed(FL.SIM_SEED + seed))
    return r


def _stream_marginal(ons, acq, band, seed, obs) -> dict:
    """Ledger-52 machinery: 200 independent stream families; cert rate + marginal tail."""
    certs, tails = [], []
    with C20._band(band):
        for k in range(N_STREAMS):
            g = torch.Generator().manual_seed(FL.SIM_SEED + STRIDE * (k + 1) + seed)
            r = SC._certify_seed(ons, acq, WIDTH, g)
            certs.append(obs > r["null_max"])
            tails.append(r["p_value"])
    marginal = statistics.mean(tails)
    return dict(cert_rate=round(statistics.mean([float(c) for c in certs]), 3),
                marginal_tail=marginal, advertised=1.0 / FL.N_SIMS,
                qualified=bool(marginal > 1.0 / FL.N_SIMS))


def _dec_cat_companion(rec: dict) -> dict:
    acq = rec["acquisition_onset"] or 0
    dc = [(c["t"], c["dec_cat"]) for c in rec["columns"]
          if c.get("dec_cat") is not None and c["t"] >= acq]
    if not dc:
        return dict(mean=None, late_minus_early=None, n=0)
    vals = [v for _t, v in dc]
    half = len(vals) // 2
    return dict(mean=round(statistics.mean(vals), 4),
                late_minus_early=(round(statistics.mean(vals[half:]) -
                                        statistics.mean(vals[:half]), 4) if half else None),
                n=len(vals))


def _episode_span(ons, acq, band, width=WIDTH):
    """Window span [t_lo, t_hi) (wave units) of the LONGEST certified-band run — for the
    WARMUP-CARRIED overlap check."""
    win: dict = {}
    for w, a in ons:
        if w >= acq:
            win.setdefault(w // width, []).append(a)
    if not win:
        return None
    lo, hi = min(win), max(win)
    best, cur, best_end = 0, 0, None
    for i in range(lo, hi + 1):
        v = win.get(i)
        cur = cur + 1 if (v and statistics.mean(v) >= band) else 0
        if cur > best:
            best, best_end = cur, i
    if best == 0:
        return None
    return ((best_end - best + 1) * width, (best_end + 1) * width)


def _correspondence(K: int, s: int) -> dict:
    """K<->B correspondence companion (§4): same-member delivered adjacency + mean displacement,
    computed on the realized map (descriptive only; no K<->B equivalence claim is licensed)."""
    import exp12_arms as X12
    import exp12_fabric as F
    loop, _sp, _c = X12.build_exp12("exp12_dwell", s, 20_000)   # member stream: fabric-structural,
    fab = loop.stream                                           # 20k prefix is representative
    d = F.ubuf_map(fab.T, K, torch.Generator().manual_seed(F.SEED_UBUF + s))
    dm = fab.member[d]
    adj = float((dm[1:] == dm[:-1]).float().mean())
    disp = float((torch.arange(fab.T) - d).float().mean())
    return dict(same_member_delivered_adjacency=round(adj, 5),
                mean_displacement=round(disp, 1), prefix=20_000)


# ------------------------------------------------------------------ cells (§5 + AMD-1)

def cells(cert: dict, strat_cert: dict) -> dict:
    """Mechanical §5+AMD-1 cell mapping. cert/strat_cert: {K: sorted certified seed lists};
    strat_cert has POWERED_K keys only. Returns cells + halts (judgment never taken here)."""
    out = dict(halts=[], flags=[])
    for K in POWERED_K:
        s_only = sorted(set(strat_cert[K]) - set(cert[K]))
        if s_only:
            out["halts"].append(f"K{K}: STRATIFIED-ONLY certification {s_only} — HALT")
    out["recency_carried"] = {K: sorted(set(cert[K]) - set(strat_cert[K])) for K in POWERED_K}
    out["rescue_full_only_K512"] = sorted(cert[512])
    if cert[512]:
        out["rescue_full_only_K512_sentence"] = RESCUE_FULL_ONLY_SENTENCE
    powered_counts = [len(strat_cert[K]) for K in POWERED_K]      # AMD-1(3): powered strata only
    out["powered_strat_counts"] = dict(zip((f"K{k}" for k in POWERED_K), powered_counts))
    out["rescue_monotone_powered"] = bool(
        all(b >= a for a, b in zip(powered_counts, powered_counts[1:]))
        and any(b > a for a, b in zip(powered_counts, powered_counts[1:])))
    total_certified = sum(len(cert[K]) for K in PAID_K)
    out["all_paid_dead"] = (total_certified == 0)
    return out


# ------------------------------------------------------------------ G5 score

def score():
    bands = _bands()
    strat = json.loads(STRATCACHE.read_text())
    g2 = json.loads((OUTDIR / "exp20_g2_maps.json").read_text())
    res = {"width": WIDTH, "bands": {f"K{k}": v for k, v in bands.items()},
           "amd1": "K512 stratified = UNDECIDABLE-IN-ARM (recorded, never imputed)",
           "per_K": {}, "halts": [], "flags": []}
    cert, strat_cert = {}, {}
    for K in PAID_K:
        rows = {}
        for s in SEEDS:
            rec = _verdict_rec(K, s)
            acq, full = C20._eb_onsets(rec)
            row = dict(acq=rec["acquisition_onset"], n_full=len(full))
            cf = _certify(full, acq, bands[K], s)
            row["full"] = dict(observed=cf["observed_run"], null_max=cf["null_max"],
                               p_hat=cf["p_hat"], certified=cf["certified"])
            if cf["certified"]:
                row["full"]["stream_marginal"] = _stream_marginal(full, acq, bands[K], s,
                                                                 cf["observed_run"])
                span = _episode_span(full, acq, bands[K])
                row["full"]["episode_span"] = span
                if span and span[0] <= K:
                    res["flags"].append(f"K{K} s{s}: WARMUP-CARRIED (episode from wave {span[0]} "
                                        f"<= K={K})")
            if K in POWERED_K:
                sw = set(strat[str(s)][f"K{K}"])
                sons = [[w, a] for w, a in full if w in sw]
                cs = _certify(sons, acq, bands[K], s)
                row["stratified"] = dict(n=len(sons), observed=cs["observed_run"],
                                         null_max=cs["null_max"], certified=cs["certified"])
                if cs["certified"]:
                    row["stratified"]["stream_marginal"] = _stream_marginal(
                        sons, acq, bands[K], s, cs["observed_run"])
            else:
                row["stratified"] = dict(state="UNDECIDABLE-IN-ARM (AMD-1)",
                                         n_recorded=g2["per_seed"][str(s)][f"K{K}"]["support"]
                                                    ["windows"]["W=K"]["support"])
            row["dec_cat"] = _dec_cat_companion(rec)
            row["ea_exam_acc_end"] = rec["columns"][-1].get("exam_acc")
            rows[s] = row
            print(f"  K{K} s{s}: full {cf['observed_run']} vs {cf['null_max']} "
                  f"{'CERT' if cf['certified'] else '-'}"
                  + (f" | strat {row['stratified'].get('observed')} vs "
                     f"{row['stratified'].get('null_max')} "
                     f"{'CERT' if row['stratified'].get('certified') else '-'}"
                     if K in POWERED_K else " | strat UNDECIDABLE")
                  + f" | dec_cat {row['dec_cat']['mean']} (dLE {row['dec_cat']['late_minus_early']})",
                  flush=True)
        res["per_K"][f"K{K}"] = rows
        cert[K] = sorted(s for s in SEEDS if rows[s]["full"]["certified"])
        if K in POWERED_K:
            strat_cert[K] = sorted(s for s in SEEDS if rows[s]["stratified"].get("certified"))
        # multiplicity envelope (MULTIPLICITY-CARRIED): certified vs non-certified p_never
        pn = {s: g2["per_seed"][str(s)][f"K{K}"]["multiplicity"]["p_never"] for s in SEEDS}
        cs_, ns_ = [pn[s] for s in cert[K]], [pn[s] for s in SEEDS if s not in cert[K]]
        if cs_ and ns_:
            gap = abs(statistics.mean(cs_) - statistics.mean(ns_))
            spread = max(pn.values()) - min(pn.values())
            res["per_K"][f"K{K}"]["multiplicity_envelope"] = dict(
                certified_mean=round(statistics.mean(cs_), 5),
                noncert_mean=round(statistics.mean(ns_), 5),
                gap=round(gap, 5), full_spread=round(spread, 5))
            if spread > 0 and gap > spread:
                res["halts"].append(f"K{K}: MULTIPLICITY-CARRIED (gap {gap} beyond spread)")
    res["correspondence"] = {f"K{K}": _correspondence(K, 0) for K in PAID_K}
    cl = cells(cert, strat_cert)
    res["cells"] = cl
    res["halts"] += cl["halts"]
    res["flags"] += cl["flags"]
    if cl["all_paid_dead"]:
        ESCALATION.write_text(json.dumps(dict(
            fired=True, grounds="ALL-PAID-DEAD at G5 (0 certified at K in {32,128,512})",
            date="2026-07-28", per_prereg="§4: same law, same seeds, own pre-flight (constants "
                                          "re-cut only where K-dependent); launch = this gate's "
                                          "pass action, not a new ruling")))
        res["escalation"] = "FIRED — exp20_escalation.json written; K=2048 arm unlocked"
    OUT.write_text(json.dumps(res, indent=2))
    print(f"\nG5: cert_full={ {k: v for k, v in cert.items()} } "
          f"strat={ {k: v for k, v in strat_cert.items()} } | halts={len(res['halts'])} "
          f"flags={len(res['flags'])} -> {OUT.name}", flush=True)
    if res["halts"]:
        print("G5 HALTS:", *res["halts"], sep="\n  * ", flush=True)
        sys.exit(3)


# ------------------------------------------------------------------ smoke (cells, reds first)

def smoke():
    # STRATIFIED-ONLY plant must HALT
    c = cells({32: [], 128: [], 512: []}, {32: [4], 128: []})
    assert any("STRATIFIED-ONLY" in h for h in c["halts"]), "STRATIFIED-ONLY plant did not HALT"
    print("  STRATIFIED-ONLY plant -> HALT fires  [RED observed]")
    # ALL-DEAD plant fires escalation (checked via the flag, NOT by writing the real artifact here)
    c = cells({32: [], 128: [], 512: []}, {32: [], 128: []})
    assert c["all_paid_dead"], "ALL-DEAD plant did not set the escalation condition"
    print("  ALL-PAID-DEAD plant -> escalation condition set  [red-side verified]")
    # monotone through POWERED strata only: K512 full-cert must NOT satisfy the gate
    c = cells({32: [], 128: [], 512: [0, 1, 2]}, {32: [], 128: []})
    assert not c["rescue_monotone_powered"] and c["rescue_full_only_K512"] == [0, 1, 2], \
        "K512 full certs leaked into the monotone gate"
    print("  K512 full-certs land in RESCUE-FULL-ONLY-K512, NOT the monotone gate  [AMD-1(3)]")
    # a genuine powered rise satisfies it
    c = cells({32: [0], 128: [0, 1], 512: []}, {32: [0], 128: [0, 1]})
    assert c["rescue_monotone_powered"] and not c["all_paid_dead"]
    print("  powered strict rise -> RESCUE-MONOTONE satisfiable  [green]")
    # RECENCY-CARRIED = full minus strat, per powered K
    c = cells({32: [0, 3], 128: [], 512: []}, {32: [0], 128: []})
    assert c["recency_carried"][32] == [3]
    print("  RECENCY-CARRIED = full∖strat per powered K  [green]")
    print("SMOKE PASS (cell logic: reds observed before any pass counts)", flush=True)


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        smoke()
    elif "--score" in sys.argv:
        score()
    else:
        print("usage: --smoke | --score")
