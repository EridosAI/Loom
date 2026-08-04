"""EXP21 — frozen seed/cohort route logic + all-cell fixtures (prereg §4.5-§4.7/§5; gate G5).

COMMITTED BEFORE G4 (the row-56/§8 discipline: no scorer change after verdict data exists).
Routes are assigned PER SEED FIRST by the §5 binding precedence, then by the §4.6 cohort law;
no averaging may erase a route split. An observed pattern that cannot be assigned mechanically
is a HALT (`Unrouted`), never a new in-corridor interpretation.

Seed-level precedence (§5, binding): (1) CONTROL-NONVIABLE; (2) CATEGORY-COLLAPSE-IN-COSTUME;
(3) GENERAL-STABILISATION / WRONG-REASON; (4) OFF-BETTER; (5) TEACHING-ADDED;
(6) PRESERVATION-ONLY; (7) INTERNAL-ONLY / SELF-EASING; (8) NO-EFFECT. First satisfied row
wins. ACQUISITION-SPEEDUP is a reported companion under NO-EFFECT, never a tenth cell.

Deployed laws folded from the build-review panel (all exercised by real-path fixtures):
  * grid/record completeness on the VERDICT path (exp21_cal.assert_grid_complete /
    assert_record_complete at the ratified 1M horizon) — a truncated record HALTs, never
    scores silently;
  * bank binding: each run's probe payload hash must equal the seed's canonical primary-bank
    manifest hash (exp21_probe.assert_bank_binding) AND the ON/OFF pair must share it
    (assert_pair_share);
  * the §3.6 dynamic-range restriction: when calibration routed
    PRESERVATION-ONLY-RESTRICTION, the acquisition question is DEAD — TEACHING-ADDED (and
    the acquisition leg of OFF-BETTER) cannot fire at verdict;
  * wrong-reason compression is tested on the IMPROVING arm in BOTH directions (the §5 cell
    is arm-neutral): an OFF category gain with OFF-side collapse is
    CATEGORY-COLLAPSE-IN-COSTUME, and OFF-BETTER requires the OFF-side guards clear;
  * t_eligible is COMPUTED from the run config (cfg.t2), never a literal;
  * pre-Q4 certified acquisition = the full five-read certification COMPLETES at or before
    750,000 (onset + 4 reads <= Q4_FROM);
  * cohort SEED-SPLIT additionally fires when a second CAUSAL-claim cell (TEACHING-ADDED /
    PRESERVATION-ONLY / OFF-BETTER) appears beside the 7/8 route — the §4.6 "materially
    different causal routes" leg, mechanical form surfaced for the Touch-2 read.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

import exp21_cal as CAL                                        # noqa: E402
import exp21_probe as P21                                      # noqa: E402
import exp21_teaching as T21                                   # noqa: E402
from sculpt_config import SculptConfig                         # noqa: E402

OUTDIR21 = T21.OUTDIR21
CAUSAL_CELLS = {"TEACHING-ADDED", "PRESERVATION-ONLY", "OFF-BETTER"}
OPPOSED = {"TEACHING-ADDED": "OFF-BETTER", "PRESERVATION-ONLY": "OFF-BETTER",
           "OFF-BETTER": "TEACHING-ADDED"}


class Unrouted(Exception):
    """§5: an outcome no cell covers mechanically — a HALT, never an interpretation."""


def load_constants() -> dict:
    return json.loads((OUTDIR21 / "exp21_constants.json").read_text())


def load_restriction() -> bool:
    """§3.6: the calibration dynamic-range route, read from the committed artifact."""
    cal = json.loads((OUTDIR21 / "exp21_calibration.json").read_text())
    return cal["dynamic_range"]["route"] == "PRESERVATION-ONLY-RESTRICTION"


def assert_pair_share(on_sum: dict, off_sum: dict):
    """§3.2: the primary bank is shared byte-for-byte by the paired ON/OFF runs."""
    assert on_sum["bank_sha256"] == off_sum["bank_sha256"], \
        (f"s{on_sum.get('seed')}: paired runs used different primary banks "
         f"({on_sum['bank_sha256'][:12]} != {off_sum['bank_sha256'][:12]}) — HALT")


def summarize_seed(arm: str, seed: int, k: dict, tag: str = "verdict",
                   *, horizon: int = T21.H21) -> dict:
    """Per-arm seed summary under the frozen constants (verdict form; also usable on cal
    tags for fixtures). Primary bank ONLY (§4.4: shadow never enters a verdict record)."""
    rec = json.loads(CAL.record_path(arm, seed, tag).read_text())
    CAL.assert_record_complete(rec, horizon)
    p = CAL.load_probe(arm, seed, tag, "primary")
    CAL.assert_grid_complete(p["ts"], horizon)
    P21.assert_bank_binding(seed, p["bank_sha256"])
    lab = CAL.cat_labels(p["ev_member"])
    s = CAL.bacc_series(p["predictions"], lab)                 # full precision
    ts = p["ts"]
    theta = k["theta_cat"]["value"]
    t2 = SculptConfig(seed=seed).t2                            # computed, never a literal
    i_elig = CAL.eligible_index(ts, t2)
    q4 = set(CAL.q4_indices(ts, horizon))
    onset = CAL.episode_start(s, ts, theta, i_elig)
    fq = CAL.fq_of(s, ts, theta, horizon)
    # pre-Q4 certified acquisition: the five-read certification COMPLETES by 750k
    acq_pre_q4 = (onset is not None
                  and onset + (T21.N_ACQ - 1) * T21.PROBE_EVERY <= T21.Q4_FROM)
    q4c = [c for c in rec["columns"] if T21.Q4_FROM < c["t"] <= horizon]
    return dict(
        arm=arm, seed=seed, bank_sha256=p["bank_sha256"],
        acq_onset=onset,
        acq_pre_q4=acq_pre_q4,
        acq_area=CAL.acq_area(s, ts, theta, i_elig),
        fq=fq,
        ret=bool(fq > k["fq_null_bound"]["value"] and acq_pre_q4),
        cat_q4_mean=float(s[sorted(q4)].mean()),
        guards_q4={q: statistics.mean(rd["axes"][q]["bacc"]
                                      for i, rd in enumerate(p["summaries"]) if i in q4)
                   for q in CAL.GUARD_AXES},
        pr_q4=statistics.mean(rd["geom"]["participation_ratio"]
                              for i, rd in enumerate(p["summaries"]) if i in q4),
        internal_q4={m: (statistics.mean(c[m] for c in q4c if c.get(m) is not None)
                         if any(c.get(m) is not None for c in q4c) else None)
                     for m in CAL.INTERNAL_METRICS})


def _viability(off: dict, k: dict) -> tuple[bool, list]:
    fails = CAL.viability_fails(off["guards_q4"], off["pr_q4"], k["guard_bars"])
    return len(fails) < 2, fails


def seed_route(on: dict, off: dict, k: dict, *, restriction: bool = False) -> dict:
    """The §5 mechanical seed route. Raises Unrouted on any missing input.
    `restriction` = the committed §3.6 PRESERVATION-ONLY-RESTRICTION: the acquisition
    question is dead — no acquisition-based cell may fire in either direction."""
    need = ("acq_onset", "acq_pre_q4", "acq_area", "fq", "ret", "cat_q4_mean",
            "guards_q4", "pr_q4", "internal_q4")
    for d, nm in ((on, "on"), (off, "off")):
        missing = [f for f in need if f not in d or (d[f] is None and f in
                   ("acq_area", "fq", "cat_q4_mean", "guards_q4", "pr_q4"))]
        if missing:
            raise Unrouted(f"seed summary [{nm}] missing {missing} — HALT")
    dg4, bars = k["delta_guard_q4"], k["guard_bars"]
    d_acq, d_ret = k["delta_acq"], k["delta_ret"]
    viable, fails = _viability(off, k)
    adv_cat = on["cat_q4_mean"] - off["cat_q4_mean"]           # common axis-advantage form
    adv = {q: on["guards_q4"][q] - off["guards_q4"][q] for q in CAL.GUARD_AXES}
    acq_adv = (not restriction
               and on["acq_onset"] is not None and off["acq_onset"] is None
               and (on["acq_area"] - off["acq_area"]) > d_acq)
    ret_adv = (on["acq_pre_q4"] and off["acq_pre_q4"] and on["ret"] and not off["ret"]
               and (on["fq"] - off["fq"]) > d_ret)
    off_acq_adv = (not restriction
                   and off["acq_onset"] is not None and on["acq_onset"] is None
                   and (off["acq_area"] - on["acq_area"]) > d_acq)
    off_ret_adv = (on["acq_pre_q4"] and off["acq_pre_q4"] and off["ret"] and not on["ret"]
                   and (off["fq"] - on["fq"]) > d_ret)
    cat_improves_on = acq_adv or ret_adv or (adv_cat > k["delta_point_cat"])
    cat_improves_off = off_acq_adv or off_ret_adv or (-adv_cat > k["delta_point_cat"])
    selective = (adv_cat > adv["coarse_a"] + dg4["coarse_a"]
                 and adv_cat > adv["distractor"] + dg4["distractor"])
    # wrong-reason compression, tested on the IMPROVING arm (the §5 cell is arm-neutral)
    collapse_on = (adv["distractor"] < -dg4["distractor"]
                   or adv["member"] < -dg4["member"]
                   or on["pr_q4"] <= bars["participation_ratio"])
    collapse_off = (adv["distractor"] > dg4["distractor"]
                    or adv["member"] > dg4["member"]
                    or off["pr_q4"] <= bars["participation_ratio"])
    detail = dict(off_viable=viable, off_guard_fails=fails, adv_cat=round(adv_cat, 6),
                  adv_guards={q: round(v, 6) for q, v in adv.items()},
                  adv_pr=round(on["pr_q4"] - off["pr_q4"], 6),
                  acq_adv=acq_adv, ret_adv=ret_adv, selective=selective,
                  collapse_on=collapse_on, collapse_off=collapse_off,
                  restriction=restriction,
                  on=dict(acq=on["acq_onset"], area=round(on["acq_area"], 6),
                          fq=round(on["fq"], 6), ret=on["ret"]),
                  off=dict(acq=off["acq_onset"], area=round(off["acq_area"], 6),
                           fq=round(off["fq"], 6), ret=off["ret"]))
    # --- the binding precedence ---
    if not viable:
        return dict(route="CONTROL-NONVIABLE", **detail)
    if (cat_improves_on and collapse_on) or (cat_improves_off and collapse_off):
        return dict(route="CATEGORY-COLLAPSE-IN-COSTUME", **detail)
    if cat_improves_on and max(adv["coarse_a"], adv["distractor"], adv["member"]) >= adv_cat:
        return dict(route="GENERAL-STABILISATION", **detail)
    if (off_acq_adv or off_ret_adv) and not collapse_off:
        return dict(route="OFF-BETTER", **detail)
    if acq_adv and viable and selective and not collapse_on:
        return dict(route="TEACHING-ADDED", **detail)
    if ret_adv and viable and selective and not collapse_on:
        return dict(route="PRESERVATION-ONLY", **detail)
    internal = {m: (on["internal_q4"][m] - off["internal_q4"][m]
                    if (on["internal_q4"][m] is not None and off["internal_q4"][m] is not None)
                    else None) for m in CAL.INTERNAL_METRICS}
    if any(v is not None and v > k["delta_internal"][m] for m, v in internal.items()):
        return dict(route="INTERNAL-ONLY", internal={m: (round(v, 6) if v is not None else None)
                                                     for m, v in internal.items()}, **detail)
    speedup = (on["acq_onset"] is not None and off["acq_onset"] is not None
               and on["acq_onset"] < off["acq_onset"])
    return dict(route="NO-EFFECT", acquisition_speedup_companion=speedup, **detail)


def cohort(routes: dict) -> dict:
    """§4.6 cohort law over the 8-row seed table."""
    if len(routes) != 8:
        raise Unrouted(f"cohort needs the full 8-row seed table; got {sorted(routes)}")
    counts = {}
    for r in routes.values():
        counts[r["route"]] = counts.get(r["route"], 0) + 1
    top = max(counts, key=counts.get)
    opposite = any(OPPOSED.get(a) in counts for a in counts)
    hetero = len(CAUSAL_CELLS & set(counts)) >= 2              # §4.6 "materially different
    #                                                            causal routes" (mechanical)
    out = dict(counts=counts, sign_test="7/8 minimum (9/256 = 0.03515625 one-sided)")
    if counts[top] < 7 or opposite or hetero:
        out["cohort"] = "SEED-SPLIT"
        out["split_grounds"] = dict(top_count=counts[top], opposite_signed=opposite,
                                    heterogeneous_causal=hetero)
        return out
    if top == "TEACHING-ADDED":
        all_viable = all(r["off_viable"] for r in routes.values())
        off_acq = sum(1 for r in routes.values() if r["off"]["acq"] is not None)
        if not (all_viable and off_acq == 0):
            out["cohort"] = "SEED-SPLIT"
            out["teaching_added_extra_law"] = dict(off_viable_8of8=all_viable,
                                                   off_certified_acq=off_acq)
            return out
        out["teaching_added_extra_law"] = dict(off_viable_8of8=True, off_certified_acq=0)
    out["cohort"] = top
    return out


def main(tag: str = "verdict") -> dict:
    """G5 executor — refuses until every verdict record exists (and G4 was ratified-opened)."""
    torch.set_num_threads(1)
    k = load_constants()
    restriction = load_restriction()
    missing = [(a, s) for a in ("on", "off") for s in T21.VERDICT_SEEDS21
               if not CAL.record_path(a, s, tag).exists()]
    assert not missing, f"G5 refused: verdict records missing {missing}"
    routes, table = {}, []
    for s in T21.VERDICT_SEEDS21:
        on = summarize_seed("on", s, k, tag)
        off = summarize_seed("off", s, k, tag)
        assert_pair_share(on, off)
        routes[s] = seed_route(on, off, k, restriction=restriction)
        table.append(dict(seed=s, **routes[s]))
    out = dict(exp="exp21", tag=tag, constants_theta=k["theta_cat"]["value"],
               restriction=restriction, seed_table=table, cohort=cohort(routes),
               bare_n=len(routes))
    p = OUTDIR21 / "exp21_verdict.json"
    assert not p.exists(), "verdict artifact exists — append-only"
    p.write_text(json.dumps(out, indent=2))
    return out


# ------------------------------------------------------------------ all-cell fixtures (§7 G5)
def _syn(route_shape: str) -> tuple[dict, dict]:
    """Synthetic (on, off) seed summaries driving one §5 cell (fixture-only)."""
    base = dict(acq_onset=None, acq_pre_q4=False, acq_area=0.0, fq=0.0, ret=False,
                cat_q4_mean=0.5, guards_q4=dict(coarse_a=0.6, distractor=0.8, member=0.4),
                pr_q4=6.0, internal_q4=dict(exam_acc=0.5, asg_cat=0.2),
                bank_sha256="fix", arm="x", seed=-1)
    on, off = dict(base), dict(base)
    on["guards_q4"], off["guards_q4"] = dict(base["guards_q4"]), dict(base["guards_q4"])
    on["internal_q4"], off["internal_q4"] = dict(base["internal_q4"]), dict(base["internal_q4"])
    if route_shape == "TEACHING-ADDED":
        on.update(acq_onset=90_000, acq_pre_q4=True, acq_area=0.05, cat_q4_mean=0.75)
    elif route_shape == "PRESERVATION-ONLY":
        on.update(acq_onset=90_000, acq_pre_q4=True, fq=0.6, ret=True, cat_q4_mean=0.72)
        off.update(acq_onset=95_000, acq_pre_q4=True, fq=0.02, ret=False, cat_q4_mean=0.55)
    elif route_shape == "GENERAL-STABILISATION":
        on.update(cat_q4_mean=0.62)
        on["guards_q4"].update(coarse_a=0.85, distractor=0.95)   # broader-than-category lift
    elif route_shape == "INTERNAL-ONLY":
        on["internal_q4"].update(exam_acc=0.9)
    elif route_shape == "CATEGORY-COLLAPSE-IN-COSTUME":
        on.update(acq_onset=90_000, acq_pre_q4=True, acq_area=0.05, cat_q4_mean=0.8)
        on["guards_q4"].update(member=0.07)                      # member info collapses
    elif route_shape == "CATEGORY-COLLAPSE-OFF-SIDE":
        off.update(acq_onset=90_000, acq_pre_q4=True, acq_area=0.05, cat_q4_mean=0.8)
        off["guards_q4"].update(member=0.07)                     # OFF's member info collapses
    elif route_shape == "NO-EFFECT":
        pass
    elif route_shape == "OFF-BETTER":
        off.update(acq_onset=90_000, acq_pre_q4=True, acq_area=0.05, cat_q4_mean=0.75)
    elif route_shape == "CONTROL-NONVIABLE":
        off["guards_q4"].update(coarse_a=0.25, distractor=0.5)   # two broad guards at chance
    elif route_shape == "SPEEDUP":
        on.update(acq_onset=60_000, acq_pre_q4=True, acq_area=0.03, cat_q4_mean=0.7)
        off.update(acq_onset=200_000, acq_pre_q4=True, acq_area=0.028, cat_q4_mean=0.69)
    return on, off


FIX_K = dict(theta_cat=dict(value=0.66), fq_null_bound=dict(value=0.1),
             delta_point_cat=0.01, delta_acq=0.005, delta_ret=0.05,
             delta_guard_q4=dict(coarse_a=0.02, distractor=0.02, member=0.02,
                                 participation_ratio=0.2),
             guard_bars=dict(coarse_a=0.27, distractor=0.52, member=0.0825,
                             participation_ratio=1.2),
             delta_internal=dict(exam_acc=0.05, asg_cat=0.05))


def _pool_summaries(sums: list[dict]) -> dict:
    """The BROKEN pooled scorer (plant only): field means across seeds, one route."""
    out = dict(sums[0])
    for f in ("acq_area", "fq", "cat_q4_mean", "pr_q4"):
        out[f] = statistics.mean(s[f] for s in sums)
    out["guards_q4"] = {q: statistics.mean(s["guards_q4"][q] for s in sums)
                        for q in CAL.GUARD_AXES}
    out["internal_q4"] = {m: statistics.mean(s["internal_q4"][m] for s in sums)
                          for m in CAL.INTERNAL_METRICS}
    out["acq_onset"] = min((s["acq_onset"] for s in sums if s["acq_onset"] is not None),
                           default=None)
    out["acq_pre_q4"] = any(s["acq_pre_q4"] for s in sums)
    out["ret"] = any(s["ret"] for s in sums)
    return out


def fixtures() -> dict:
    """Every §5 cell reached from a synthetic input THROUGH the real scorer + the broken-
    scorer reds (each executed, never narrated)."""
    torch.set_num_threads(1)
    got = {}
    for cell, expect in (
            ("CONTROL-NONVIABLE", "CONTROL-NONVIABLE"),
            ("CATEGORY-COLLAPSE-IN-COSTUME", "CATEGORY-COLLAPSE-IN-COSTUME"),
            ("CATEGORY-COLLAPSE-OFF-SIDE", "CATEGORY-COLLAPSE-IN-COSTUME"),
            ("GENERAL-STABILISATION", "GENERAL-STABILISATION"),
            ("OFF-BETTER", "OFF-BETTER"),
            ("TEACHING-ADDED", "TEACHING-ADDED"),
            ("PRESERVATION-ONLY", "PRESERVATION-ONLY"),
            ("INTERNAL-ONLY", "INTERNAL-ONLY"),
            ("NO-EFFECT", "NO-EFFECT")):
        on, off = _syn(cell)
        r = seed_route(on, off, FIX_K)
        assert r["route"] == expect, f"fixture {cell} routed to {r['route']} — scorer broken"
        got[cell] = r["route"]
    on, off = _syn("SPEEDUP")
    r = seed_route(on, off, FIX_K)
    assert r["route"] == "NO-EFFECT" and r["acquisition_speedup_companion"] is True, \
        "SPEEDUP must ride as a NO-EFFECT companion, never a cell"
    got["ACQUISITION-SPEEDUP-companion"] = "NO-EFFECT"
    # §3.6 restriction: a TEACHING-ADDED-shaped seed must NOT fire it under restriction
    on, off = _syn("TEACHING-ADDED")
    r = seed_route(on, off, FIX_K, restriction=True)
    assert r["route"] != "TEACHING-ADDED", \
        f"restriction failed to disable TEACHING-ADDED: {r['route']}"
    got["RESTRICTION-DISABLES-TEACHING-ADDED"] = r["route"]
    # SEED-SPLIT at cohort: 5 TEACHING-ADDED + 3 OFF-BETTER (opposite-signed present)
    routes = {}
    for s in range(8):
        on, off = _syn("TEACHING-ADDED" if s < 5 else "OFF-BETTER")
        routes[s] = seed_route(on, off, FIX_K)
    c = cohort(routes)
    assert c["cohort"] == "SEED-SPLIT", f"opposite-signed cohort not SEED-SPLIT: {c}"
    got["SEED-SPLIT"] = "SEED-SPLIT"
    # heterogeneous-causal leg: 7 TEACHING-ADDED + 1 PRESERVATION-ONLY -> SEED-SPLIT
    routes_h = {}
    for s in range(8):
        on, off = _syn("TEACHING-ADDED" if s < 7 else "PRESERVATION-ONLY")
        routes_h[s] = seed_route(on, off, FIX_K)
    ch = cohort(routes_h)
    assert ch["cohort"] == "SEED-SPLIT" and ch["split_grounds"]["heterogeneous_causal"], \
        f"heterogeneous causal cohort not SEED-SPLIT: {ch}"
    got["SEED-SPLIT-heterogeneous"] = "SEED-SPLIT"

    reds = {}
    # unrouted_pattern: missing inputs must HALT, never default
    try:
        broken_on, off2 = _syn("NO-EFFECT")
        del broken_on["guards_q4"]
        seed_route(broken_on, off2, FIX_K)
        raise SystemExit("unrouted_pattern: scorer defaulted on missing inputs — HALT")
    except Unrouted as e:
        reds["unrouted_pattern"] = dict(red=True, message=str(e)[:120])
    # seed_pooling_plant: EXECUTE the broken pooled scorer on the 5v3 split — it returns ONE
    # flattering route where the real §4.6 law returns SEED-SPLIT
    ons = [_syn("TEACHING-ADDED" if s < 5 else "OFF-BETTER")[0] for s in range(8)]
    offs = [_syn("TEACHING-ADDED" if s < 5 else "OFF-BETTER")[1] for s in range(8)]
    pooled = seed_route(_pool_summaries(ons), _pool_summaries(offs), FIX_K)
    real_cohort = cohort({s: seed_route(ons[s], offs[s], FIX_K) for s in range(8)})
    assert pooled["route"] != "SEED-SPLIT" and real_cohort["cohort"] == "SEED-SPLIT", \
        f"pooling plant inconclusive: pooled={pooled['route']} real={real_cohort['cohort']}"
    reds["seed_pooling_plant"] = dict(red=True, pooled_single_route=pooled["route"],
                                      real_cohort=real_cohort["cohort"])
    # guard_bypass_plant: a scorer variant that SKIPS the guard checks mis-routes
    # collapse-in-costume as TEACHING-ADDED; the real scorer routes it correctly
    def _route_no_guards(on_, off_, k_):                       # the broken scorer (plant only)
        acq_adv = (on_["acq_onset"] is not None and off_["acq_onset"] is None
                   and (on_["acq_area"] - off_["acq_area"]) > k_["delta_acq"])
        return "TEACHING-ADDED" if acq_adv else "NO-EFFECT"
    on, off = _syn("CATEGORY-COLLAPSE-IN-COSTUME")
    r_bypass = _route_no_guards(on, off, FIX_K)
    assert r_bypass == "TEACHING-ADDED", \
        "expected the guard-bypassed scorer to mis-route the collapse plant"
    r_real = seed_route(on, off, FIX_K)
    assert r_real["route"] == "CATEGORY-COLLAPSE-IN-COSTUME"
    reds["guard_bypass_plant"] = dict(red=True, bypassed_route=r_bypass,
                                      real_route=r_real["route"])
    out = dict(cells=got, observed_red=reds)
    OUTDIR21.mkdir(parents=True, exist_ok=True)
    T21.write_gate_artifact(OUTDIR21 / "exp21_score_fixtures.json", out)
    T21.gatelog_append(dict(gate="G5-fixtures", outcome="ALL CELLS + OBSERVED-RED "
                            "(fixture-only)", executor="exp21_score.fixtures",
                            cells=sorted(got), reds=sorted(reds)))
    print("G5 fixtures:", sorted(got), "reds:", sorted(reds))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", action="store_true")
    ap.add_argument("--score", action="store_true")
    args = ap.parse_args()
    if args.fixtures:
        fixtures()
    elif args.score:
        main()
