"""exp_scatter_score.py — SCATTER-DWELL selector + scorer (prereg docs/EXP_SCATTER_DWELL_PREREG.md).

Mirrors exp17_score's structure and REUSES its arm-agnostic machinery: measure_kinematics (fabric
stats), _score_one / _ext_resolve / _floor_audit / _partition17 (the §4 cells, unchanged), and the
exp14_arms scoring primitives (XA._provisional_cut / census / nulls). The genuinely new pieces are the
R-selector (select_scatter = G-select) and the matched-bar EXCESS axis (F6-A rule (i)) promoted to
PRIMARY in score_scatter.

F5 floors (NOT net/path; NO gain floor): per-step displacement contrast >= 2.0x tremble perstep;
distinct-pose coverage >= 2.0x tremble traverse; confusion-bound CEILING per-step <= committed
cross_med (exp17_score.measure_tremble_baselines["confusion"]). The box wall cl>0 (R<1.125) is the
binding upper wall (generator assert). Decision: matched-bar excess + census PRIMARY; counts SECONDARY;
cal-self-converts EXPECTED -> DIRECTION-ONLY expected formal label. Determinism: threads=1.
"""
import json, math, statistics
from pathlib import Path

import torch
torch.set_num_threads(1)

import exp14_arms as XA
import exp12_arms as X12
import exp17_score as S17
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import verify_toolkit as VT                          # matched_bar_tab (record-anchored)

OUTDIR = XA.OUTDIR
ARM = "exp12_dwell_scatter"
TREMBLE_ARM = "exp12_dwell"                           # A_dwell — the contrast + baseline source
CAL_SEEDS = [20, 21, 22, 24, 25]
VERDICT_SEEDS = list(range(8))
EXT_POOL = [8, 9]
SELECT_T = 100_000
R_GRID = [0.20, 0.30, 0.40, 0.50]                    # RATIFIED (Jason, 2026-07-13, touch 1)
CONTRAST_MULT = 2.0                                  # floor1 (RATIFIED)
COVERAGE_MULT = 2.0                                  # floor2 (RATIFIED)
ACQ_MARGIN = 0.10                                    # acq-guard margin (MECHANISM_MAP §4 l.57)
SIG_DEPTH = S17.X17_SIG_DEPTH                        # 8, DEPTH-decisive
READ_FLOOR = S17.X17_READ_FLOOR                      # 8, the pre-registered n>=8 power floor


def _a_detector():
    """A_dwell's committed detector (band, N, fr) — READ from exp08/exp14_band_2x2_cal.json, never
    hardcoded (F6-A rule (ii): provenance COMPUTED from the record it describes, not asserted)."""
    a = json.loads((OUTDIR / "exp14_band_2x2_cal.json").read_text())["cells"]["A_dwell"]
    return dict(band=float(a["conv_band"]), N=int(a["conv_consec"]),
                fr=float(a["false_rate_at_cut"]), owner="A_dwell")


# ------------------------------------------------------------------ G-select (R freeze)
def scatter_baselines():
    """Tremble (A_dwell) baselines for the F5 floors. The confusion CEILING and the coverage baseline
    are the COMMITTED exp17_score.measure_tremble_baselines outputs (reused VERBATIM — bound to the
    committed recipe, not merely coincident); only perstep_med (absent from that recipe) is measured
    here on the same seeds/steps."""
    b17 = S17.measure_tremble_baselines(seeds=VERDICT_SEEDS, steps=SELECT_T, window=SELECT_T)
    per = [S17.measure_kinematics(TREMBLE_ARM, s, SELECT_T, SELECT_T) for s in VERDICT_SEEDS]
    return dict(perstep=statistics.mean(m["perstep_med"] for m in per),
                tr11=b17["tr11"], confusion=b17["confusion"],
                per_seed={str(m["seed"]): {k: m[k] for k in ("perstep_med", "tr11", "cross_med")}
                          for m in per})


def cell_feasible_scatter(per_seed, base, r):
    """F5 floors, pooled AND per-seed-worst (MIN lower bounds, MAX ceilings). Box-exit is
    guaranteed 0 by the generator's cl>0 assert (not re-checked here)."""
    ps_pool = statistics.mean(m["perstep_med"] for m in per_seed)
    ps_min = min(m["perstep_med"] for m in per_seed)
    ps_max = max(m["perstep_med"] for m in per_seed)
    covs = [m["tr11"] for m in per_seed if m["tr11"] is not None]
    cov_pool = statistics.mean(covs); cov_min = min(covs)
    f1 = ps_pool >= CONTRAST_MULT * base["perstep"] and ps_min >= CONTRAST_MULT * base["perstep"]
    f2 = cov_pool >= COVERAGE_MULT * base["tr11"] and cov_min >= COVERAGE_MULT * base["tr11"]
    f3 = ps_pool <= base["confusion"] and ps_max <= base["confusion"]     # confusion ceiling
    return dict(r=r, perstep_pool=round(ps_pool, 4), perstep_min=round(ps_min, 4),
                perstep_max=round(ps_max, 4), coverage_pool=round(cov_pool, 4),
                coverage_min=round(cov_min, 4),
                confusion_margin=round(base["confusion"] - ps_max, 4),
                floor1_contrast=f1, floor2_coverage=f2, floor3_ceiling=f3,
                feasible=bool(f1 and f2 and f3))


def _pick(cells):
    """Lexicographic pick (the committed rule, extracted so the smoke tests the REAL selector):
    among feasible cells -> MAX per-step contrast -> tie-break MAX confusion margin."""
    feas = sorted([c for c in cells if c["feasible"]],
                  key=lambda c: (-c["perstep_pool"], -c["confusion_margin"]))
    return feas[0] if feas else None


def select_scatter(write: bool = True) -> dict:
    """G-select: lexicographic pick over R_GRID on real scatter fabrics (T=100k, seeds {0-7}).
    Objective: feasible(contrast + coverage under the confusion ceiling, pooled AND per-seed-worst)
    -> MAX per-step contrast -> tie-break MAX confusion margin. Empty region -> geometry HALT."""
    base = scatter_baselines()
    cells = [cell_feasible_scatter(
        [S17.measure_kinematics(X12.scatter_arm(r), s, SELECT_T, SELECT_T) for s in VERDICT_SEEDS],
        base, r) for r in R_GRID]
    pick = _pick(cells)
    out = dict(gate="G-select", arm=ARM, grid_r=R_GRID, baselines=base,
               multipliers=dict(contrast=CONTRAST_MULT, coverage=COVERAGE_MULT),
               ceiling="committed cross_med (measure_tremble_baselines['confusion'])",
               objective="feasible(F5 floors, pooled AND per-seed-worst) -> max perstep contrast -> "
                         "tie-break max confusion margin",
               cells=cells, selected=pick, spec_hash=XA.C.spec_hash())
    if pick is None:
        out["verdict"] = ("GEOMETRY-CONFLICT HALT: no grid R clears the walls under the confusion "
                          "ceiling (routes to design)")
    if write:
        S17._dump(OUTDIR / "scatter_select.json", out)
    if pick is None:
        raise AssertionError(out["verdict"])
    return out


# ------------------------------------------------------------------ G4 cal read (own band; Ruling-B)
def cal_read_scatter(cal_tag: str = "scattercal", out_tag: str = "scatter_cal_read",
                     write: bool = True) -> dict:
    """SCATTER cal read: own provisional band (§10.22, NO borrow); borrow-gate DIAGNOSTIC only;
    cal-converts -> Ruling-B own between-episode recut -> NON-loadable (the EXPECTED cell). Arm label
    stamped = ARM (F6-A rule (ii): provenance COMPUTED, never a wrong branch label). Structure mirrors
    exp17_score.cal_read_exp17; primitives are XA's arm-agnostic helpers."""
    recs = {s: S17._load(s, cal_tag, arm=ARM) for s in CAL_SEEDS}
    missing = [s for s, r in recs.items() if r is None]
    assert not missing, f"SCATTER cal records missing for seeds {missing} (tag={cal_tag})"
    per_accs = {s: [a for (_, a, _) in XA._acc_series(r)] for s, r in recs.items()}
    band, N, pooled = XA._provisional_cut(per_accs)
    fr = XA._consec_rate(pooled, band, N)
    alpha_ok = fr <= XA.ALPHA
    n_acq = sum(recs[s].get("acquisition_onset") is not None for s in CAL_SEEDS)
    live = n_acq >= S17.X17_CAL_LIVE_MIN
    converts = [s for s in CAL_SEEDS
                if XA._density_conversion_onset(recs[s], band, N) is not None]
    loadable, method = True, "OWN provisional §10.22 honest-null (cal does not convert)"
    if converts:                                      # the EXPECTED cell (pre-named §4)
        between = XA._between_episode_null(per_accs)
        band, N = XA._joint_band_cut(between)
        loadable, pooled = False, between
        fr = XA._consec_rate(between, band, N); alpha_ok = fr <= XA.ALPHA
        method = ("OWN between-episode null (cal-converts EXPECTED, Ruling-B); counts NON-loadable "
                  "-> DIRECTION-ONLY is the expected formal LABEL; the finding is the matched-bar "
                  "excess + census, not this label")
    # borrow-gate DIAGNOSTIC only (never sources the band)
    donor = {s: [a for (_, a, _) in XA._acc_series(S17._load(s, "cal", arm=TREMBLE_ARM))]
             for s in CAL_SEEDS if S17._load(s, "cal", arm=TREMBLE_ARM) is not None}
    diag = None
    if donor:
        d_band, d_N, d_null = XA._provisional_cut(donor)
        diag = {**XA._borrow_gate((d_band, d_N), d_null, XA._between_episode_null(per_accs)),
                "cell": ARM, "donor": TREMBLE_ARM,
                "note": "DIAGNOSTIC ONLY (§2: baseline-shift; the band is NEVER borrowed)"}
    geometry_bare_N = N < SIG_DEPTH
    out = dict(exp="scatter_cal_read", gate="G4", arm=ARM, cal_seeds=CAL_SEEDS,
               primary_at=S17.X17_PRIMARY_AT,
               verdict_band=dict(band=round(band, 4), N=N, loadable=loadable, method=method,
                                 false_rate=round(fr, 6), alpha=XA.ALPHA, alpha_ok=bool(alpha_ok),
                                 n_null=len(pooled), prefix="[0,500k] (F13)"),
               liveness=dict(n_acquired=n_acq, n_cal=len(CAL_SEEDS), n_min=S17.X17_CAL_LIVE_MIN,
                             live=bool(live)),
               cal_converters=converts, cal_converts_expected=True,
               band_geometry=dict(N=N, sig_depth=SIG_DEPTH, bare_N=bool(geometry_bare_N)),
               borrow_diag=diag, spec_hash=XA.C.spec_hash())
    halts = []
    if not live:
        halts.append(f"liveness {n_acq}/{len(CAL_SEEDS)} < {S17.X17_CAL_LIVE_MIN} — unposed")
    if not alpha_ok:
        halts.append(f"no alpha-compliant cut (fr {fr:.6f} > {XA.ALPHA})")
    if not geometry_bare_N:
        halts.append(f"band N={N} >= SIG_DEPTH={SIG_DEPTH} — census non-discriminating")
    if halts:
        out["HALT"] = halts
    if write:
        S17._dump(OUTDIR / f"exp14_{out_tag}.json", out)
    return out


# ------------------------------------------------------------------ matched-bar EXCESS (PRIMARY axis 1)
def _excess_survives(both_bars) -> bool:
    """A surviving excess = scatter (group-1, a_k) exceeds A_dwell (b_k) at a COMMON detector with a
    one-sided Fisher <= 0.05. Unlike-bar rows never count (both arms read through each detector)."""
    return any(row["a_k"] > row["b_k"] and row["fisher_a_ge_b"] <= 0.05 for row in both_bars)


def _primary_finding(excess_survives: bool, certified: int, n_read: int, raw_k: int) -> str:
    """§4 PRIMARY decision on matched-bar excess + census (counts SECONDARY). CONVERTS carries the
    pre-registered READ n>=8 POWER floor (prereg §4: 'census certifies >=5 of READ n>=8'; the
    positive is independent of the raw-count rung per catch-15, but NEVER of the power floor). DEAD
    = no surviving excess AND census 0 (raw is SECONDARY context, does not gate — the orbit texture)."""
    if excess_survives and certified >= 5 and n_read >= READ_FLOOR:
        return "SCATTER CONVERTS"
    if (not excess_survives) and certified == 0:
        return "SCATTER DEAD"
    return "ROUTES (matched-bar/census disagree, intermediate, or underpowered n_read<8)"


def matched_bar_excess(band: float, N: int, fr_scatter=None,
                       verdict_tag: str = "scatterverdict") -> dict:
    """F6-A rule (i): read BOTH arms through BOTH detectors (scatter's own (band,N,fr) and A_dwell's
    committed detector, READ from the artifact). A CONVERTS finding needs an excess that SURVIVES at
    a common detector. Per-detector fr is passed and REPORTED (matched_bar_tab contract)."""
    op = [str(S17._rec_path(s, verdict_tag, arm=ARM)) for s in VERDICT_SEEDS]
    ap = [str(OUTDIR / f"exp14_exp12_dwell_s{s}_verdict.json") for s in VERDICT_SEEDS]
    det_s = dict(band=round(band, 4), N=N, fr=fr_scatter, owner="scatter")
    det_a = _a_detector()
    tab = VT.matched_bar_tab(op, ap, det_s, det_a)     # scatter = group-1 (a_k in the tab)
    return dict(both_bars=tab["both_bars"], excess_survives=_excess_survives(tab["both_bars"]),
                det_scatter=det_s, det_a=det_a,
                note="unlike-bar counts are context-only (catch-16); the surviving-at-a-common-"
                     "detector excess is the load-bearing read")


# ------------------------------------------------------------------ acq-guard (§4 l.57 falsifier)
def acq_guard(verdict_tag: str = "scatterverdict") -> dict:
    """MECHANISM_MAP_v1_2 §4 l.57 DEPLOYMENT-time falsifier of the geometric confusion ceiling:
    scatter member-category separation (sep_cat, post-acq mean [0,500k), matched seeds/window) must
    be >= (1 - ACQ_MARGIN) * A_dwell sep_cat. FAIL -> HALT + re-derive the ceiling from the
    acquisition read. Built-not-run (a_sep uses the committed A_dwell verdict records)."""
    def _sepcat(arm, tag):
        vals = []
        for s in VERDICT_SEEDS:
            r = S17._load(s, tag, arm=arm)
            if r is None:
                continue
            on = r.get("acquisition_onset")
            vals += [c["sep_cat"] for c in r["columns"]
                     if c.get("sep_cat") is not None and (on is None or c["t"] >= on)
                     and c["t"] <= S17.X17_PRIMARY_AT]
        return statistics.mean(vals) if vals else None
    s_sep, a_sep = _sepcat(ARM, verdict_tag), _sepcat(TREMBLE_ARM, "verdict")
    ok = s_sep is not None and a_sep is not None and s_sep >= (1 - ACQ_MARGIN) * a_sep
    return dict(scatter_sep_cat=s_sep, a_dwell_sep_cat=a_sep, margin=ACQ_MARGIN,
                floor=(round((1 - ACQ_MARGIN) * a_sep, 6) if a_sep is not None else None),
                passes=bool(ok),
                halt=(None if ok else "acq-guard: scatter sep_cat degraded > 10% vs A_dwell -> "
                      "re-derive the confusion ceiling from the acquisition read (§4 l.57)"))


# ------------------------------------------------------------------ G6 score (GUARDED, built-not-run)
def score_scatter(cal_read_tag: str = "scatter_cal_read", verdict_tag: str = "scatterverdict",
                  cal_tag: str = "scattercal", write: bool = True) -> dict:
    cal_read_p = OUTDIR / f"exp14_{cal_read_tag}.json"
    assert cal_read_p.exists(), "run cal_read_scatter first (G4)"
    cr = json.loads(cal_read_p.read_text())
    assert "HALT" not in cr, f"cal read carries HALT {cr['HALT']} — the corridor is halted"
    band, N = cr["verdict_band"]["band"], cr["verdict_band"]["N"]
    loadable = cr["verdict_band"]["loadable"]
    base, ext = {}, {}
    for s in VERDICT_SEEDS:
        r = S17._load(s, verdict_tag, arm=ARM)
        assert r is not None, (f"verdict record s{s} missing — score_scatter is BUILT, not run "
                               "(release only after the {0-7} records exist)")
        base[s] = S17._score_one(r, band, N)
    for s in EXT_POOL:
        r = S17._load(s, verdict_tag, arm=ARM)
        ext[s] = S17._score_one(r, band, N) if r is not None else None
    res = S17._ext_resolve(base, ext)
    read_recs = {s: S17._load(s, verdict_tag, arm=ARM) for s in res["read_seeds"]}
    cal_accs = {}
    for s in CAL_SEEDS:
        r = S17._load(s, cal_tag, arm=ARM)
        assert r is not None, f"cal record s{s} missing at score time — loud fail (C5)"
        cal_accs[s] = [a for (_, a, _) in XA._acc_series(r)]
    audit = S17._floor_audit(read_recs, band, N, cal_accs)
    raw_k = res["k"]
    certified = sum(1 for s in res["read_seeds"]
                    if XA._longest_episode(
                        [c["exam_acc"] for c in read_recs[s]["columns"]
                         if c.get("exam_acc") is not None
                         and c["t"] >= (read_recs[s].get("acquisition_onset") or 0)
                         and c["t"] <= S17.X17_PRIMARY_AT], band, N) >= SIG_DEPTH)
    census_ok = certified > audit["census_selfaudit"]["expected_depth_runs_bracket"][1]
    part = S17._partition17(raw_k, res["n_read"], loadable, audit["floor_clean"],
                            census_ok, certified)
    mb = matched_bar_excess(band, N, fr_scatter=cr["verdict_band"]["false_rate"],
                            verdict_tag=verdict_tag)
    # F6-A: matched-bar excess + census are PRIMARY (with the n>=8 power floor); counts SECONDARY.
    finding = _primary_finding(mb["excess_survives"], certified, res["n_read"], raw_k)
    out = dict(exp="scatter_score", gate="G6", arm=ARM,
               decision_axes=dict(axis1_matched_bar_excess=mb["excess_survives"],
                                  axis2_certified_census=certified,
                                  primary_finding=finding),
               formal_partition_SECONDARY=part, raw_k=raw_k, certified=certified,
               n_read=res["n_read"], loadable=loadable, floor_audit=audit,
               matched_bar=mb, acq_guard=acq_guard(verdict_tag),
               ext=res, cal_converts_expected=cr.get("cal_converts_expected"),
               band=round(band, 4), N=N, spec_hash=XA.C.spec_hash(),
               note="DRAFT — no attribution (touch 3). Matched-bar excess + census DECIDE; the count "
                    "partition is SECONDARY (cal-converts EXPECTED -> DIRECTION-ONLY formal label).")
    if write:
        S17._dump(OUTDIR / "scatter_score.json", out)
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--select", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    if a.smoke:
        import exp_scatter_smoke as SM
        SM.smoke_scatter_scorer()
    if a.select:
        r = select_scatter()
        print("select_scatter:", r["selected"])
