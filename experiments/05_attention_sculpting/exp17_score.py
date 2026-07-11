"""EXP17 TREMBLE-vs-SWEEP (orbit) — measurer/selector + cal-read + guarded scorer.

The prereg (docs/EXP17_TREMBLE_VS_SWEEP_PREREG.md, RATIFIED 52a4d7a) §6/F2 names this FILE as the
build deliverable; the gate-executor table (CORRIDOR_PROTOCOL.md:94):

    G2  measure_tremble_baselines / select_orbit    smoke: sm-G2-lex (lexicographic incl. the
        (the (r,omega)-freeze; §9 R3, RB-2)           min-r*omega DECOY that must FAIL under the
                                                      retired objective, tie-break, empty->HALT)
                                                      + the --anchor digit-exact bind (F4/F4-A:
                                                      the measurer's OWN frozen outputs; forensic
                                                      = documented cross-check w/ residual table)
    G4  cal_read_exp17                              smoke: sm-G4-* (band/liveness/geometry
                                                      HALT flags, gradient FALLBACK path)
    G6  score_exp17 (GUARDED build-not-run)         smoke: sm-G6-* (partition grid incl.
                                                      SWEEP-CONVERTS/DEAD/SIGNATURE-DIVERGENT,
                                                      census F7 off-diagonals + F12 SELF-AUDIT
                                                      positive-delta, EXT under D1, Fisher)

House rules carried (prereg §8/§9): every null pool, band cut, and borrow DIAGNOSTIC on the
[0,500k] column prefix (F13 — enforced here by loading every cal/verdict record through
XA._truncate at X17_PRIMARY_AT); census DEPTH-decisive, RECUR-corroborative (F7) + census
SELF-AUDIT (F12: a POSITIVE certified count must EXCEED the dual-null >=SIG_DEPTH expectation
bracket high end, else NOT-CERTIFIABLE-by-census); SWEEP-DEAD = raw 0 (F5); scoring constants
NEVER enter C.spec_hash() (run-level spec_hash parity across reused+fresh records); primary
frozen at 500k, 1M tail descriptive. Baselines are MEASURED, never assumed (the TRB=0.096
lesson): no floor carries a load-bearing literal — sim expectations are recorded for sanity only.
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import torch

torch.set_num_threads(1)                      # the determinism contract (inherited)

import exp14_arms as XA                       # helper library (band, census, fisher, truncate)
import exp12_arms as X12                      # build_exp12 (fabric access for the measurer)

X10 = XA.X10
OUTDIR = XA.OUTDIR
EVAL = XA.EVAL

# ---- constants (NONE of these enter C.spec_hash(); see header) -------------------------- #
X17_ARM = "exp12_dwell_orbit"                 # §9 R2 (the live arm; registered by the 3b delta)
X17_TREMBLE_ARM = "exp12_dwell"               # A_dwell — the contrast + baseline source
X17_CAL_SEEDS = [20, 21, 22, 24, 25]
X17_VERDICT_SEEDS = list(range(8))
X17_EXT_POOL = [8, 9]
X17_SUBST_POOL = list(range(10, 20))          # provenance (pre-check substitution, G1b)
X17_READ_FLOOR = 8                            # certifiable cells need READ n>=8 (NOT XA.N_MIN_READ)
X17_CAL_LIVE_MIN = 3                          # liveness gate: >=3/5 acquired else HALT
X17_PRIMARY_AT = XA.READ_AT                   # 500_000 — the frozen primary (F13 prefix everywhere)

# gradient-persistence internal control (§5.1): EXPECT ~ A's referent; collapse = instrument alarm
X17_GRAD_REF_A = dict(p1=0.6915, p13_48=0.5499, delta=0.1416)   # AMD-2, verified 4x (EXP16)
X17_GRAD_ALARM = 0.0708                       # flag iff median delta < half the referent (F10)
X17_GRAD_P1, X17_GRAD_TAIL = "p1", "p13-48"

# signature census (F7 DEPTH-decisive; SIG_DEPTH re-affirmed = 8 against EXP17's own band
# geometry via the G4 bare-N check below — §10.25.3, never silently inherited)
X17_SIG_DEPTH = XA.EPISODE_MIN                # 8 — longest episode >= DEPTH certifies ALONE
X17_SIG_RECUR = 2                             # reported as corroboration; NEVER gates (F7)
X17_FLOOR_P = 0.10                            # floor-audit clean rule (AMD-13, self-excluded null)
X17_NULL_POOL_ADVISORY = 6532                 # min committed precedent n_null — ADVISORY tripwire
                                              # ONLY (F14: routes-to-human, never gates; the §0
                                              # nothing-transports exemption is explicit)

# selection (§9 R3, RB-2 LEXICOGRAPHIC) — grid PINNED at ratification
X17_R_GRID = [0.85, 0.90, 0.95, 1.00, 1.05, 1.10]
X17_W_GRID_DEG = [12, 14, 16, 18, 20, 22]
X17_NP_MULT = 4.0                             # floor 1: net/path@11 >= 4x measured tremble
X17_TR_MULT = 2.5                             # floor 2: traverse@11 >= 2.5x measured tremble
X17_TR_CEIL = 0.50                            # floor 2 ceiling (absolute; per-seed MAX applies)
X17_SELECT_T = 100_000                        # selection scale (fabric-only, X-blind)
X17_MEAN_K = 11                               # the mean-dwell restriction for @11 statistics
X17_STAT_SD = 0.125                           # stationary deviation sd (exp12_fabric derivation)
X17_BOUND = 1.5                               # family bound (per-axis support = 3.0)

# F4-A anchor bind (RULED 2026-07-12, ratification-class — supersedes the forensic-target bind,
# which FIRED at build as designed): the anchors are THIS measurer's OWN outputs on unmodified A
# fabric at the recipe windows (BUILD_T=1,000,008, measure [0,500k), seeds {0..7}) — the committed
# code is the executable recipe definition, frozen digit-exact at re-base into
# exp08/exp17_anchor_rebase.json. Loud fail, NO tolerance; future measurer drift breaks the bind.
# Forensic originals ride below as X17_FORENSIC_* (documented cross-check; residual table in the
# artifact — every residual an averaging/summation step of the unported design-chat script, none
# recipe-class). Rider: an anchor is only as exact as its provenance — digit-exact binds require
# committed-code provenance.
X17_ANCHOR_STAT2 = 0.07887529612359336        # mean over seeds of per-seed mean per-dwell
                                              #   net/path over contained k in [13,48]
X17_ANCHOR_STAT3 = 0.05558072403073311        # mean over seeds of per-seed LOWER-median
                                              #   (sorted[(m-1)//2]) over the flattened
                                              #   contained-dwell x axis f32 radius pool /3.0
X17_ANCHOR_STAT1 = 0.15955481071937405        # mean over seeds of per-seed within-step norm
                                              #   median (per-frame pools incl. straddler, f64
                                              #   norms) — feeds floor-3's confusion bound (R4)
X17_FORENSIC_STAT2 = 0.07887529612359337      # F4-A cross-check originals ('from-scratch numpy,
X17_FORENSIC_STAT3 = 0.05558072434117397      #   matched to 6 decimals' provenance — never
X17_FORENSIC_STAT1 = 0.15955464218495066      #   ULP-validated; see the re-base artifact)
X17_ANCHOR_SEEDS = list(range(8))
X17_ANCHOR_BUILD_STEPS = 1_000_000            # cfg.T = steps+8 = 1,000,008 (the committed build)
X17_ANCHOR_WINDOW = 500_000
X17_ANCHOR_ARTIFACT = "exp17_anchor_rebase.json"

# sim expectations (sanity display ONLY — never load-bearing; measured values govern)
X17_SIM_EXPECT = dict(np11=0.1448, tr11=0.0902, path11=1.636, confusion=1.311,
                      landing=(0.85, 18))

FISHER_BASELINE_A = 8                         # A_dwell committed 0/8 (companion, never gated)
C_SHUFFLE_CONTEXT = "C_shuffle 5/8 {0,2,4,5,6} @ 0.64x5 (own shifted null; descriptive context)"


# ======================================================================================== #
#  Fabric kinematics measurer (G2; also §5.5/§5.7 companion reader). Pure fabric; X-blind.
# ======================================================================================== #
def _fabric(arm: str, seed: int, steps: int):
    """Fabric ONLY (loop constructed, never stepped) — the pre-check pattern
    ('fabric -> T+8; no stepping', exp14_arms._assert_one)."""
    loop, _spec, _cfg = X12.build_exp12(arm, seed, steps)
    return loop.stream


def measure_kinematics(arm: str, seed: int, steps: int, window: int) -> dict:
    """All EXP17 per-seed fabric statistics over frames [0, window), CONTAINED dwells only
    (a dwell truncated by the window boundary is dropped — the forensic recipe).

    np11 / tr11 / path11: per-dwell net-over-path, per-axis (max-min)/(2*BOUND) axis-mean, and
    path length — each restricted to realized k == X17_MEAN_K, pooled mean (tr11_max = per-dwell
    max, for the ceiling). perstep/cross: within-dwell and cross-boundary step norms (stat1
    recipe; cross = the F11 'different-object' jump -> the CONFUSION bound). stat2_1348 /
    stat3_med: the forensic anchor recipes (F4). anchor_over / pose_clips: orbit-arm telemetry
    (None on other arms)."""
    fab = _fabric(arm, seed, steps)
    nuis = fab.nuis                            # float32 (the fabric dtype; radii stay f32 —
    pos = fab.pos.tolist()                     # the forensic's stored per-axis medians are f32)
    T_full = nuis.shape[0]
    n = min(window, T_full)
    # CONTAINED dwells (forensic recipe, recovered): every dwell with onset < window and
    # onset + k <= window — including the final in-window dwell (whose successor may start
    # at/after the window). The single boundary-straddler is excluded from per-dwell stats.
    starts_full = [i for i in range(T_full) if pos[i] == 1]
    ends_full = starts_full[1:] + [T_full]
    bounds = [(s, e) for s, e in zip(starts_full, ends_full) if s < n and e <= n]
    # stat1 pools (review C12): PER-FRAME over [0,n) — within = steps at pos[t] > 1, cross =
    # steps at pos[t] == 1 (t > 0) — INCLUDING the boundary-straddler's in-window frames (the
    # forensic recipe: the straddler is excluded from per-DWELL metrics only). Float64 norms.
    nu64 = nuis[:n].double()
    dstep = nu64[1:] - nu64[:-1]
    step_norm = torch.linalg.vector_norm(dstep, dim=1)
    within = [float(step_norm[t - 1]) for t in range(1, n) if pos[t] > 1]
    cross = [float(step_norm[t - 1]) for t in range(1, n) if pos[t] == 1]
    np11, tr11, path11, ratios_1348 = [], [], [], []
    exc32 = []                                  # per-dwell per-axis radii, FLOAT32 (recovered)
    for (s, e) in bounds:
        seg = nuis[s:e]
        seg64 = seg.double()                    # per-dwell net/path in FLOAT64 (recovered)
        k = e - s
        d64 = seg64[1:] - seg64[:-1]
        step_norms = torch.linalg.vector_norm(d64, dim=1) if k > 1 else seg64.new_zeros(0)
        path = float(step_norms.sum())
        net = float(torch.linalg.vector_norm(seg64[-1] - seg64[0]))
        ratio = (net / path) if path > 0 else 0.0
        if k == X17_MEAN_K:
            np11.append(ratio)
            ext = (seg64.max(dim=0).values - seg64.min(dim=0).values) / (2 * X17_BOUND)
            tr11.append(float(ext.mean()))
            path11.append(path)
        if 13 <= k <= 48:
            ratios_1348.append(ratio)
        exc32.append((seg - seg[0]).abs().amax(dim=0))       # FLOAT32 radii
    # stat3 (forensic construction, RECOVERED from the stored artifact): the LOWER-MEDIAN
    # (sorted[(m-1)//2]) of the flattened dwell x axis float32 radius pool, divided by the
    # per-axis support (3.0) in float64 — verified element-exact on seed 0 (rank 91401 of
    # 182,804). NOT numpy's midpoint median.
    stat3 = None
    if exc32:
        flat = torch.stack(exc32).flatten()
        low_med = float(flat.sort().values[(flat.numel() - 1) // 2])
        stat3 = low_med / (2 * X17_BOUND)
    # R5 REQUIRED companion (review C21): driven-plane vs undriven-complement extents — any
    # SWEEP-DEAD read is posed against the DRIVEN contrast, never the diluted 4-axis average.
    driven = undriven = None
    planes = getattr(fab, "orbit_planes", None)
    if planes is not None and len(bounds) and planes.shape[0] >= len(bounds):
        dr, ud = [], []
        for di, (s, e) in enumerate(bounds):
            seg64 = nuis[s:e].double()
            dev = seg64 - seg64[0]
            P = planes[di].double()                          # (2, K) orthonormal
            in_plane = dev @ P.T                             # (k, 2)
            out_plane = dev - in_plane @ P
            dr.append(float(torch.linalg.vector_norm(in_plane, dim=1).amax()) / (2 * X17_BOUND))
            ud.append(float(torch.linalg.vector_norm(out_plane, dim=1).amax()) / (2 * X17_BOUND))
        driven = statistics.mean(dr)
        undriven = statistics.mean(ud)
    return dict(
        arm=arm, seed=seed, steps=steps, window=window,
        n_dwells=len(bounds), n11=len(np11),
        np11=(statistics.mean(np11) if np11 else None),
        tr11=(statistics.mean(tr11) if tr11 else None),
        tr11_max=(max(tr11) if tr11 else None),
        path11=(statistics.mean(path11) if path11 else None),
        perstep_med=(statistics.median(within) if within else None),
        perstep_max=(max(within) if within else None),
        cross_med=(statistics.median(cross) if cross else None),
        stat2_1348=(statistics.mean(ratios_1348) if ratios_1348 else None),
        stat3_med=stat3,
        anchor_over=getattr(fab, "orbit_anchor_over", None),
        pose_clips=getattr(fab, "orbit_pose_clips", None),
        driven_extent=driven, undriven_extent=undriven,
        stat1_within_med=(statistics.median(within) if within else None),
    )


def _forensic_residuals(per: dict, pooled: dict) -> dict:
    """F4-A clause 2: the original forensic values as documented cross-check — the residual
    table is computed MECHANICALLY vs the committed docs/EXP17_DWELL_KINEMATICS_FORENSIC.json
    (per-seed + pooled diffs and ULP distances; stat3's stored-value inconsistency — s0 =
    LOWER element, s2 = MIDPOINT on float32-identical pools — named as the cause)."""
    fj = json.loads((Path(__file__).resolve().parents[2] / "docs" /
                     "EXP17_DWELL_KINEMATICS_FORENSIC.json").read_text())
    fper = {str(e["seed"]): dict(
        stat1=e["stat1_perstep"]["within"]["norm"]["median"],
        stat2=e["stat2_netpath"]["p13-48"]["ratio_mean"],
        stat3=e["stat3_radius"]["per_axis_radius_frac_pooled_median"],
        n_within=e["stat1_perstep"]["within"]["norm"]["n"]) for e in fj["per_seed"]}
    fpool = dict(stat1=fj["pooled"]["stat1_within_norm_median"],
                 stat2=fj["pooled"]["stat2_ratio_by_bucket_mean"]["p13-48"],
                 stat3=fj["pooled"]["stat3_per_axis_radius_frac_pooled"])

    def row(mine, theirs):
        d = mine - theirs
        return dict(mine=mine, forensic=theirs, diff=d,
                    ulp=(abs(d) / math.ulp(theirs) if d else 0.0), exact=(d == 0.0))

    return dict(
        pooled={st: row(pooled[st], fpool[st]) for st in ("stat1", "stat2", "stat3")},
        per_seed={sd: {st: row(per[sd][st], fper[sd][st]) for st in ("stat1", "stat2", "stat3")}
                  for sd in per},
        n_within={sd: fper[sd]["n_within"] for sd in fper},
        residual_classes="stat2: summation-order (<=1 ULP all 8 seeds; 3 exact); stat3: 7/8 "
                         "exact, s2 = MIDPOINT-vs-LOWER-element (mutually inconsistent with s0 "
                         "on identical pools); stat1: BIT-EXACT on all four odd-n_within seeds "
                         "(single-element medians — frame-set and element identity proven), "
                         "even-n seeds off <=5.71e-7 at the two-middle averaging step",
        provenance="original measure script untracked (design-chat side), environment reset; "
                   "the history records validation 'from-scratch numpy, matched to 6 decimals' "
                   "— the anchors were never ULP-validated (F4-A grounds). Design-seat catch "
                   "NINE rides the amendment record.")


def anchor_assert(write: bool = True) -> dict:
    """F4-A anchor bind (2026-07-12, supersedes the forensic-target bind that FIRED at build):
    the measurer's OWN frozen outputs, digit-exact — this committed code is the executable
    recipe definition, so drift in any of the three recipes breaks the bind loudly. Forensic
    originals = documented cross-check (X17_FORENSIC_*); on green the re-base artifact
    (frozen values + mechanical residual table) is written. NO tolerance (amend-path rule)."""
    per, s1, s2, s3 = {}, [], [], []
    for sd in X17_ANCHOR_SEEDS:
        m = measure_kinematics(X17_TREMBLE_ARM, sd, X17_ANCHOR_BUILD_STEPS, X17_ANCHOR_WINDOW)
        s1.append(m["stat1_within_med"])
        s2.append(m["stat2_1348"])
        s3.append(m["stat3_med"])
        per[str(sd)] = dict(stat1=m["stat1_within_med"], stat2=m["stat2_1348"],
                            stat3=m["stat3_med"])
    got1, got2, got3 = statistics.mean(s1), statistics.mean(s2), statistics.mean(s3)
    assert got1 == X17_ANCHOR_STAT1, \
        f"ANCHOR stat1 drift: measurer {got1!r} != frozen {X17_ANCHOR_STAT1!r} (F4-A digit-exact bind)"
    assert got2 == X17_ANCHOR_STAT2, \
        f"ANCHOR stat2 drift: measurer {got2!r} != frozen {X17_ANCHOR_STAT2!r} (F4-A digit-exact bind)"
    assert got3 == X17_ANCHOR_STAT3, \
        f"ANCHOR stat3 drift: measurer {got3!r} != frozen {X17_ANCHOR_STAT3!r} (F4-A digit-exact bind)"
    out = dict(stat1=got1, stat2=got2, stat3=got3, seeds=X17_ANCHOR_SEEDS, ok=True)
    if write:
        _dump(OUTDIR / X17_ANCHOR_ARTIFACT, dict(
            ruling="F4-A (Jason, 2026-07-12; ratification-class): anchors re-based on "
                   "exp17_score.py's own outputs as the executable recipe definition; frozen "
                   "digit-exact; NO tolerance anywhere — future measurer drift breaks the bind. "
                   "Original forensic values retained as documented cross-check with residuals "
                   "stated. Rider: an anchor is only as exact as its provenance — digit-exact "
                   "binds require committed-code provenance.",
            recipe=dict(arm=X17_TREMBLE_ARM, seeds=X17_ANCHOR_SEEDS,
                        build_steps=X17_ANCHOR_BUILD_STEPS, window=X17_ANCHOR_WINDOW,
                        conventions="contained dwells = onset+k <= W incl. the final in-window "
                                    "dwell; per-dwell net/path FLOAT64; radii FLOAT32; stat3 = "
                                    "LOWER-median sorted[(m-1)//2] of the flattened radius pool "
                                    "/3.0 in f64 (method-named per F4-A); stat1 = per-frame "
                                    "pools over [0,n) incl. straddler frames, f64 norms, "
                                    "per-seed median; pooled = mean over seeds"),
            frozen=dict(stat1=X17_ANCHOR_STAT1, stat2=X17_ANCHOR_STAT2,
                        stat3=X17_ANCHOR_STAT3, per_seed=per),
            forensic_cross_check=_forensic_residuals(
                per, dict(stat1=got1, stat2=got2, stat3=got3))))
    return out


def measure_tremble_baselines(seeds=None, steps=X17_SELECT_T, window=None) -> dict:
    """The FOUR measured floor references (§9 R6) on real A fabric — pinned in the freeze
    artifact with this recipe; no load-bearing literal anywhere."""
    seeds = list(seeds if seeds is not None else X17_VERDICT_SEEDS)
    window = window or steps
    per = [measure_kinematics(X17_TREMBLE_ARM, sd, steps, window) for sd in seeds]
    return dict(
        recipe=dict(arm=X17_TREMBLE_ARM, seeds=seeds, steps=steps, window=window,
                    stats="np11/tr11/path11: pooled mean of per-seed means (k==11 contained "
                          "dwells); confusion: mean of per-seed MEDIAN cross-boundary step norms "
                          "(F11 'different-object' jump)"),
        np11=statistics.mean([m["np11"] for m in per]),
        tr11=statistics.mean([m["tr11"] for m in per]),
        path11=statistics.mean([m["path11"] for m in per]),
        # F11 names two candidate 'different-object' jumps (shuffled-adjacent 1.326 /
        # cross-boundary 1.311); PINNED here = CROSS-BOUNDARY (the actual adjacent
        # different-object step in the delivered stream) — review m13; surfaced at pre-flight.
        confusion=statistics.mean([m["cross_med"] for m in per]),
        per_seed={str(m["seed"]): {k: m[k] for k in ("np11", "tr11", "path11", "cross_med")}
                  for m in per},
        sim_expect=X17_SIM_EXPECT)


# ======================================================================================== #
#  (r, omega) selector — the G2 executor (§9 R3, RB-2 LEXICOGRAPHIC)
# ======================================================================================== #
def _clip_halfwidth(r: float) -> float:
    return X17_BOUND - r - 3 * X17_STAT_SD


def _lexicographic_pick(cells: list) -> dict | None:
    """RB-2: among FEASIBLE cells, maximize clip half-width, tie-break minimal r*omega.
    Returns the winner or None (empty region -> geometry-conflict HALT in the caller)."""
    feas = [c for c in cells if c["feasible"]]
    if not feas:
        return None
    feas.sort(key=lambda c: (-c["clip"], c["r"] * math.radians(c["w_deg"])))
    return feas[0]


def _cell_feasible(per_seed: list, base: dict, r: float, w_deg: int) -> dict:
    """All three floors, pooled AND per-seed-WORST (MIN for lower bounds, MAX for ceilings)."""
    np_pool = statistics.mean([m["np11"] for m in per_seed])
    tr_pool = statistics.mean([m["tr11"] for m in per_seed])
    np_min = min(m["np11"] for m in per_seed)
    tr_min = min(m["tr11"] for m in per_seed)
    # per-seed-WORST = worst SEED STATISTIC (R3, review C16): ceilings gate on the max over
    # seeds of the per-seed AGGREGATE (tr11 seed-mean; perstep seed-median) — symmetric with
    # the lower floors' min-over-seeds-of-means. Raw per-dwell/per-step maxima are REPORTED
    # companions only, never gated on.
    tr_seed_max = max(m["tr11"] for m in per_seed)
    ps_med = statistics.mean([m["perstep_med"] for m in per_seed])
    ps_seed_max = max(m["perstep_med"] for m in per_seed)
    tr_dwell_max = max((m["tr11_max"] if m["tr11_max"] is not None else m["tr11"])
                       for m in per_seed)                      # reported only
    ps_step_max = max(m["perstep_max"] for m in per_seed)      # reported only
    anchor_over = sum(int(m["anchor_over"] or 0) for m in per_seed)
    arc = r * math.radians(w_deg) * (X17_MEAN_K - 1)
    f1 = np_pool >= X17_NP_MULT * base["np11"] and np_min >= X17_NP_MULT * base["np11"]
    f2 = (tr_pool >= X17_TR_MULT * base["tr11"] and tr_min >= X17_TR_MULT * base["tr11"]
          and tr_pool <= X17_TR_CEIL and tr_seed_max <= X17_TR_CEIL)
    f3 = (arc >= base["path11"] and ps_med <= base["confusion"]
          and ps_seed_max <= base["confusion"])
    return dict(r=r, w_deg=w_deg, clip=round(_clip_halfwidth(r), 4), arc=round(arc, 3),
                np_pool=round(np_pool, 4), np_min=round(np_min, 4),
                tr_pool=round(tr_pool, 4), tr_min=round(tr_min, 4),
                tr_seed_max=round(tr_seed_max, 4), perstep_med=round(ps_med, 4),
                perstep_seed_max=round(ps_seed_max, 4),
                tr_dwell_max=round(tr_dwell_max, 4), perstep_step_max=round(ps_step_max, 4),
                anchor_over=anchor_over, floor1=f1, floor2=f2, floor3=f3,
                feasible=bool(f1 and f2 and f3 and anchor_over == 0))


def select_orbit(write: bool = True) -> dict:
    """G2: grid per §9 R3 on real orbit fabrics at T=100k seeds {0-7}; LEXICOGRAPHIC pick;
    freeze artifact exp08/exp17_orbit_select.json. Empty region -> geometry-conflict HALT."""
    base = measure_tremble_baselines()
    cells = []
    for r in X17_R_GRID:
        for w in X17_W_GRID_DEG:
            per = [measure_kinematics(X12.orbit_arm(r, w), sd, X17_SELECT_T, X17_SELECT_T)
                   for sd in X17_VERDICT_SEEDS]
            cells.append(_cell_feasible(per, base, r, w))
    pick = _lexicographic_pick(cells)
    out = dict(gate="G2-select", arm=X17_ARM, grid_r=X17_R_GRID, grid_w_deg=X17_W_GRID_DEG,
               objective="lexicographic: feasible(all floors, pooled AND per-seed-WORST) -> "
                         "max clip half-width -> tie-break min r*omega (RB-2)",
               baselines=base, cells=cells, selected=pick, spec_hash=XA.C.spec_hash())
    if pick is None:
        out["verdict"] = ("GEOMETRY-CONFLICT HALT: no (r,omega) clears all floors "
                          "(routes to design)")
    if write:
        _dump(OUTDIR / "exp17_orbit_select.json", out)
    if pick is None:
        raise AssertionError(out["verdict"])
    return out


def _dump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=1))


def onset_marginal_delta(arm: str = X17_ARM, steps: int = 1_000_000,
                         window: int = X17_PRIMARY_AT) -> dict:
    """RB-2 rider (a), REQUIRED touch-2 read: mean per-axis Wasserstein-1 distance between the
    realized first-pose (p=1) marginal of the frozen arm and A's, seeds {0-7} pooled, [0,window).
    Reported trade, NEVER an envelope-halt."""
    def _onsets(a):
        pools = []
        for sd in X17_VERDICT_SEEDS:
            fab = _fabric(a, sd, steps)
            m = min(window, fab.nuis.shape[0])
            sel = fab.pos[:m] == 1
            pools.append(fab.nuis[:m][sel])
        return torch.cat(pools).double()
    xa, xo = _onsets(X17_TREMBLE_ARM), _onsets(arm)
    w1 = []
    for ax in range(xa.shape[1]):
        a_s, o_s = xa[:, ax].sort().values, xo[:, ax].sort().values
        m = min(len(a_s), len(o_s))                     # counts differ by <= a few dwells
        qa = a_s[torch.linspace(0, len(a_s) - 1, m).long()]
        qo = o_s[torch.linspace(0, len(o_s) - 1, m).long()]
        w1.append(float((qa - qo).abs().mean()))
    return dict(statistic="mean per-axis W1 (quantile coupling), p=1 poses, seeds {0-7}, "
                          f"[0,{window})", per_axis=w1, mean_w1=statistics.mean(w1),
                gated=False, note="RB-2 rider (a): reported trade at touch 2")


def g2_verify(steps: int = 1_000_000) -> dict:
    """The G2 verification half (F3, review C8/C14/C18): (1) deterministic REPLAY of the
    lexicographic selection at T=100k — assert == the frozen pair; (2) verify ALL THREE floors +
    the zero-anchor-reflection assert on the deployed 1M fabrics of all 15 planned seeds
    (window [0,500k)); (3) write exp17_orbit_freeze.json carrying the frozen pair, all FOUR
    measured floor references + recipes, per-seed deployed kinematics, and the onset-marginal
    W1 rider. Targets fail at 1M -> geometry-conflict HALT (raise)."""
    art = json.loads((OUTDIR / "exp17_orbit_select.json").read_text())
    frozen = art["selected"]
    assert frozen is not None, "select artifact records a geometry-conflict HALT - nothing to verify"
    replay = select_orbit(write=False)
    rp = replay["selected"]
    assert (rp["r"], rp["w_deg"]) == (frozen["r"], frozen["w_deg"]), \
        f"G2 replay drift: {rp['r'], rp['w_deg']} != frozen {frozen['r'], frozen['w_deg']}"
    base = measure_tremble_baselines(steps=steps, window=X17_PRIMARY_AT)
    arm = X12.orbit_arm(frozen["r"], frozen["w_deg"])
    seeds = X17_VERDICT_SEEDS + X17_EXT_POOL + X17_CAL_SEEDS      # all 15 planned (F3)
    per = []
    for sd in seeds:
        m = measure_kinematics(arm, sd, steps, X17_PRIMARY_AT)
        m["_r"], m["_w_deg"] = frozen["r"], frozen["w_deg"]
        per.append(m)
    cell = _cell_feasible(per, base, frozen["r"], frozen["w_deg"])
    out = dict(gate="G2-verify", frozen=frozen, replay_ok=True,
               deployed=dict(steps=steps, window=X17_PRIMARY_AT, seeds=seeds, cell=cell,
                             per_seed={str(m["seed"]): {k: m[k] for k in
                                       ("np11", "tr11", "perstep_med", "anchor_over",
                                        "pose_clips", "driven_extent", "undriven_extent")}
                                       for m in per}),
               baselines_1M=base,
               onset_marginal=onset_marginal_delta(arm, steps, X17_PRIMARY_AT),
               spec_hash=XA.C.spec_hash())
    _dump(OUTDIR / "exp17_orbit_freeze.json", out)
    assert cell["anchor_over"] == 0, "zero-anchor-reflection assert failed at deployed 1M"
    assert cell["feasible"], (f"frozen ({frozen['r']},{frozen['w_deg']}) FAILS the floors at "
                              "deployed 1M - geometry-conflict HALT (routes to design)")
    return out


# ======================================================================================== #
#  Record loading (F13: [0,500k] prefix EVERYWHERE except the 1M tail)
# ======================================================================================== #
def _rec_path(seed: int, tag: str, arm: str = X17_ARM) -> Path:
    return OUTDIR / f"exp14_{arm}_s{seed}_{tag}.json"


def _load(seed, tag, arm=X17_ARM, primary_at=X17_PRIMARY_AT):
    p = _rec_path(seed, tag, arm)
    if not p.exists():
        return None
    return XA._truncate(json.loads(p.read_text()), primary_at)


def _recency_gradient(rec) -> dict:
    """§5.1 persistence control — EXP16's recipe verbatim; EXP17 keeps mid-dwell grading so the
    tail arrives via the pos_err_word FALLBACK (tail_from_probe expected False)."""
    onset = rec.get("acquisition_onset")
    p1s, tails = [], []
    for c in rec["columns"]:
        if onset is not None and c["t"] < onset:
            continue
        pw = c.get("pos_err_word") or {}
        pp = c.get("probe_pos_err_word") or {}
        if X17_GRAD_P1 in pw:
            p1s.append(pw[X17_GRAD_P1])
        if X17_GRAD_TAIL in pp:
            tails.append(pp[X17_GRAD_TAIL])
        elif X17_GRAD_TAIL in pw:
            tails.append(pw[X17_GRAD_TAIL])
    p1 = statistics.mean(p1s) if p1s else None
    tail = statistics.mean(tails) if tails else None
    delta = (p1 - tail) if (p1 is not None and tail is not None) else None
    return dict(p1=round(p1, 5) if p1 is not None else None,
                p13_48=round(tail, 5) if tail is not None else None,
                delta=round(delta, 5) if delta is not None else None,
                p1_n=len(p1s), tail_n=len(tails),
                tail_from_probe=bool(tails and any(
                    X17_GRAD_TAIL in (c.get("probe_pos_err_word") or {})
                    for c in rec["columns"])))


def _score_one(rec, band: float, N: int, primary_at: int = X17_PRIMARY_AT) -> dict:
    """READ/UNREAD + conversion — EXP16's _score_one verbatim (F9: the F6 budget gate)."""
    onset = rec.get("acquisition_onset")
    if onset is None:
        return dict(status="UNREAD(unacquired)", acquisition_onset=None,
                    conversion_onset=None, converted=False)
    if (primary_at - onset) < XA.MIN_CONV_BUDGET:
        return dict(status="UNREAD(budget-truncated)", acquisition_onset=onset,
                    conversion_onset=None, converted=False)
    conv = XA._density_conversion_onset(rec, band, N)
    return dict(status="READ", acquisition_onset=onset, conversion_onset=conv,
                converted=bool(conv is not None))


# ======================================================================================== #
#  Census (F7 DEPTH-decisive) + floor audit (AMD-13) + census SELF-AUDIT (F12)
# ======================================================================================== #
def _floor_audit(verdict_recs: dict, band: float, N: int, cal_per_seed_accs: dict) -> dict:
    """AMD-13 dual-null bracket at band-N + the F7 census + the F12 SELF-AUDIT at SIG_DEPTH.

    Census (F7, marked delta from EXP16's OR-rule): a seed is CERTIFIED iff its longest
    post-acq episode >= X17_SIG_DEPTH — decisive ALONE; episode count (>= X17_SIG_RECUR) is
    REPORTED as corroboration, never disqualifying, never certifying.
    Self-audit (F12): the expected COUNT of >=SIG_DEPTH runs under BOTH null constructions is
    bracketed; a POSITIVE certified count must EXCEED the bracket's high end, else
    NOT-CERTIFIABLE-by-census (occupies the floor_clean precedence rung; covers own-band
    N in {6,7}). All pools = [0,500k] prefix (F13; the records arrive truncated)."""
    def _null(excl_band, excl_N, run_len):
        segs = XA._null_segments(cal_per_seed_accs, excl_band, excl_N)
        n_pos = sum(max(0, len(sg) - run_len + 1) for sg in segs)
        ep = [L for sg in segs for L in XA._episodes_ge(sg, band, run_len)]
        rate = (len(ep) / n_pos) if n_pos else 0.0
        ps = [1 - (1 - rate) ** max(0, len(XA._post_acq(r)) - run_len + 1)
              for r in verdict_recs.values()]
        return dict(exclusion=f"{round(excl_band, 4)}x{excl_N}", run_len=run_len,
                    n_null_positions=n_pos, n_null_episodes=len(ep),
                    episode_rate=round(rate, 8), expected=sum(ps),
                    expected_display=round(sum(ps), 4), _ps=ps)

    self_N = _null(band, N, N)
    cont_N = _null(XA.CONV_LOW, XA.CONV_MIN, N)
    self_D = _null(band, N, X17_SIG_DEPTH)
    cont_D = _null(XA.CONV_LOW, XA.CONV_MIN, X17_SIG_DEPTH)

    census, observed = [], []
    for s, rec in verdict_recs.items():
        vals = XA._post_acq(rec)
        le = XA._longest_episode(vals, band, N)
        if le <= 0:
            continue
        observed.append(s)
        ne = len(XA._episodes_ge(vals, band, N))
        certified = bool(le >= X17_SIG_DEPTH)                 # F7: DEPTH alone decides
        census.append(dict(seed=s, longest_episode=le, n_episodes=ne,
                           max_run=XA._max_run(vals, band),
                           signature=("conversion-signature (depth)" if certified else
                                      ("recurrence-only (corroborative, non-certifying)"
                                       if ne >= X17_SIG_RECUR else "bare-N-isolated")),
                           certified=certified))
    certified = [c["seed"] for c in census if c["certified"]]
    P_self = (XA._poisson_binomial_ge(self_N["_ps"], len(observed))
              if (self_N["_ps"] and observed) else None)
    P_cont = (XA._poisson_binomial_ge(cont_N["_ps"], len(observed))
              if (cont_N["_ps"] and observed) else None)
    for d in (self_N, cont_N, self_D, cont_D):
        d.pop("_ps")
    census_bar = max(self_D["expected"], cont_D["expected"])
    n_null_prefix = sum(len(sg) for sg in
                        XA._null_segments(cal_per_seed_accs, band, N))
    return dict(
        band=round(band, 4), N=N, sig_depth=X17_SIG_DEPTH, sig_recur=X17_SIG_RECUR,
        expected_phantom_bracket=[self_N["expected"], cont_N["expected"]],
        self_excluded_null=self_N, contaminated_null=cont_N,
        P_self_excluded=round(P_self, 5) if P_self is not None else None,
        P_contaminated=round(P_cont, 5) if P_cont is not None else None,
        floor_clean=not bool(P_self is not None and P_self > X17_FLOOR_P),
        observed_converters=len(observed), observed_seeds=observed,
        signature_census=census, certified_converters=certified,
        certified_count=len(certified),
        census_selfaudit=dict(
            expected_depth_runs_bracket=[self_D["expected"], cont_D["expected"]],
            bar=census_bar,
            certified_exceeds_bar=bool(len(certified) > census_bar),
            census_ok=bool(len(certified) == 0 or len(certified) > census_bar),
            rule="F12: a POSITIVE certified count must EXCEED the dual-null >=SIG_DEPTH "
                 "expectation bracket high end, else NOT-CERTIFIABLE-by-census (the AMD-13 "
                 "observed-must-clear-expectation logic applied to the census itself)"),
        n_null_prefix=n_null_prefix,
        null_pool_advisory=bool(n_null_prefix < X17_NULL_POOL_ADVISORY),
        null_caveat=("AMD-13: self-excluded UNDER-states / contaminated (>=0.6x8) OVER-states "
                     "the phantom rate; truth between; the census (F7 DEPTH-decisive + F12 "
                     "self-audit) is decisive, never the floor arithmetic. Pools = [0,500k] "
                     "prefix (F13)."))


# ======================================================================================== #
#  cal_read_exp17 (G4)
# ======================================================================================== #
def cal_read_exp17(cal_tag: str = "exp17cal", out_tag: str = "exp17_cal_read",
                   write: bool = True) -> dict:
    recs = {s: _load(s, cal_tag) for s in X17_CAL_SEEDS}
    missing = [s for s, r in recs.items() if r is None]
    assert not missing, f"EXP17 cal records missing for seeds {missing} (tag={cal_tag})"
    per_seed_accs = {s: [a for (_, a, _) in XA._acc_series(r)] for s, r in recs.items()}
    band, N, pooled = XA._provisional_cut(per_seed_accs)      # §10.22 own honest band, no borrow
    fr = XA._consec_rate(pooled, band, N)
    alpha_ok = fr <= XA.ALPHA

    acq = {s: recs[s].get("acquisition_onset") is not None for s in X17_CAL_SEEDS}
    n_acq = sum(acq.values())
    live = n_acq >= X17_CAL_LIVE_MIN

    cal_conv = {s: (XA._density_conversion_onset(recs[s], band, N) is not None)
                for s in X17_CAL_SEEDS}
    converts = [s for s, c in cal_conv.items() if c]
    loadable, method = True, "OWN provisional §10.22 honest-null (cal does not convert)"
    if converts:                                              # §4 cal-converts: Ruling-B recut,
        between = XA._between_episode_null(per_seed_accs)     # NO borrow (prereg §2) — counts
        band, N = XA._joint_band_cut(between)                 # NON-loadable, direction-only
        loadable = False
        method = ("OWN between-episode null (cal-converts, Ruling-B); counts NON-loadable -> "
                  "primary DIRECTION-ONLY; attribution routes")
        # review m8/m14/m23: the reported diagnostics belong to the RECUT band on ITS pool
        pooled = between
        fr = XA._consec_rate(between, band, N)
        alpha_ok = fr <= XA.ALPHA

    # borrow-gate DIAGNOSTIC only (never sources the band; F8 label-corrected wrapper)
    diag = None
    donor_accs = {}
    for s in X17_CAL_SEEDS:
        r = _load(s, "cal", arm=X17_TREMBLE_ARM)
        if r is not None:
            donor_accs[s] = [a for (_, a, _) in XA._acc_series(r)]
    if donor_accs:
        d_band, d_N, d_null = XA._provisional_cut(donor_accs)
        raw = XA._borrow_gate((d_band, d_N), d_null,
                              XA._between_episode_null(per_seed_accs))
        diag = {**raw, "cell": X17_ARM, "donor": X17_TREMBLE_ARM,
                "note": ("DIAGNOSTIC ONLY (prereg §2: the baseline-shift question; the band is "
                         "NEVER borrowed; F8 labels corrected — exp14_arms stamps C_shuffle)")}

    grads = {s: _recency_gradient(recs[s]) for s in X17_CAL_SEEDS}
    gdeltas = [g["delta"] for g in grads.values() if g["delta"] is not None]
    grad_med = statistics.median(gdeltas) if gdeltas else None
    # F10: 'flag iff POOLED delta < 0.0708' - pool post-acq columns across cal seeds (AMD-2
    # apples-to-apples basis); the per-seed median stays REPORTED (review m9/m25)
    merged_cols = [c for s2 in X17_CAL_SEEDS
                   if recs[s2].get("acquisition_onset") is not None
                   for c in recs[s2]["columns"] if c["t"] >= recs[s2]["acquisition_onset"]]
    g_pool = _recency_gradient(dict(acquisition_onset=0, columns=merged_cols)) \
        if merged_cols else dict(delta=None)
    grad_pooled = g_pool.get("delta")
    grad_alarm = bool(grad_pooled is not None and grad_pooled < X17_GRAD_ALARM)
    geometry_bare_N = N < X17_SIG_DEPTH                       # F7 census bare-N check

    out = dict(
        exp="exp17_cal_read", gate="G4", arm=X17_ARM, cal_seeds=X17_CAL_SEEDS,
        primary_at=X17_PRIMARY_AT,
        verdict_band=dict(band=round(band, 4), N=N, loadable=loadable, method=method,
                          false_rate=round(fr, 6), alpha=XA.ALPHA, alpha_ok=bool(alpha_ok),
                          n_null=len(pooled), prefix="[0,500k] (F13)"),
        liveness=dict(n_acquired=n_acq, n_cal=len(X17_CAL_SEEDS), n_min=X17_CAL_LIVE_MIN,
                      live=bool(live),
                      onsets={str(s): recs[s].get("acquisition_onset") for s in recs}),
        cal_converters=converts,
        band_geometry=dict(N=N, sig_depth=X17_SIG_DEPTH, bare_N=bool(geometry_bare_N),
                           note="N >= SIG_DEPTH -> judgment-class HALT (F7: the census must "
                                "discriminate above the crossing length)"),
        null_pool=dict(n_null=len(pooled), advisory_floor=X17_NULL_POOL_ADVISORY,
                       advisory_flag=bool(len(pooled) < X17_NULL_POOL_ADVISORY),
                       note="ADVISORY tripwire only (F14); the alpha-uncuttable fallback is "
                            "the decisive HALT-equivalent"),
        gradient=dict(per_seed={str(s): g for s, g in grads.items()}, median_delta=grad_med,
                      pooled_delta=grad_pooled,
                      referent_A=X17_GRAD_REF_A, alarm_threshold=X17_GRAD_ALARM,
                      alarm=bool(grad_alarm),
                      note="persistence EXPECTED (~+0.1416); collapse = instrument alarm — "
                           "flagged, never gated (§5.1/F10)"),
        borrow_diag=diag, spec_hash=XA.C.spec_hash())
    halts = []
    if not live:
        halts.append(f"liveness {n_acq}/{len(X17_CAL_SEEDS)} < {X17_CAL_LIVE_MIN} — "
                     "experiment unposed")
    if not alpha_ok:
        halts.append(f"no alpha-compliant cut (fr {fr:.6f} > {XA.ALPHA})")
    if not geometry_bare_N:
        halts.append(f"band N={N} >= SIG_DEPTH={X17_SIG_DEPTH} — census non-discriminating "
                     "(judgment-class)")
    if halts:
        out["HALT"] = halts
    if write:
        _dump(OUTDIR / f"exp14_{out_tag}.json", out)
    return out


# ======================================================================================== #
#  score_exp17 (G6) — GUARDED build-not-run
# ======================================================================================== #
def _ext_resolve(base: dict, ext: dict) -> dict:
    """D1 EXT logic — EXP16's pattern verbatim (substitution-first toward the n>=8 floor;
    remainder count-extension; no-fire EXCLUDES EXT from the counted cell)."""
    base_read = [s for s, v in base.items() if v["status"] == "READ"]
    base_unread = [s for s, v in base.items() if v["status"] != "READ"]
    k_base = sum(v["converted"] for v in base.values())
    fires = (len(base_read) < X17_READ_FLOOR) or (1 <= k_base <= 4)
    if not fires:
        return dict(fired=False, n_read=len(base_read), k=k_base, read_seeds=base_read,
                    substituted=0, extended=0, ext_used=[])
    ext_read = [s for s, v in ext.items() if v is not None and v["status"] == "READ"]
    ext_missing = [s for s, v in ext.items() if v is None]
    n_sub = min(len(base_unread), len(ext_read))
    k = k_base + sum(ext[s]["converted"] for s in ext_read)
    return dict(fired=True, n_read=len(base_read) + len(ext_read), k=k,
                read_seeds=base_read + ext_read, substituted=n_sub,
                extended=len(ext_read) - n_sub, ext_used=ext_read,
                ext_missing=ext_missing,
                ext_missing_note=("EXT fired but records absent — §3 plans EXT as unconditional "
                                  "compute; run them before the DRAFT stands (review m22)"
                                  if ext_missing else None))


def _partition17(raw_k: int, n_read: int, loadable: bool, floor_clean: bool,
                 census_ok: bool, certified: int) -> dict:
    """F5 + F12 precedence: loadable -> floor -> census self-audit -> n>=8 -> count.
    SWEEP-DEAD = raw 0 (F5); SWEEP-CONVERTS needs raw>=5 AND certified>=5."""
    if not loadable:
        return dict(terminal="DIRECTION-ONLY", routes=True,
                    why="cal-converts Ruling-B recut — counts non-loadable vs A")
    if not floor_clean:
        return dict(terminal="NOT-CERTIFIABLE-by-count", routes=True,
                    why="floor-audit dirty (self-excluded null P > 0.10)")
    if not census_ok:
        return dict(terminal="NOT-CERTIFIABLE-by-census", routes=True,
                    why="positive certified count does not exceed the dual-null >=SIG_DEPTH "
                        "expectation bracket (F12)")
    if n_read < X17_READ_FLOOR:
        return dict(terminal="UNDERPOWERED", routes=True,
                    why=f"READ n={n_read} < {X17_READ_FLOOR} post-EXT")
    if raw_k == 0:
        assert certified == 0, (f"raw 0 with certified {certified} - census/count "
                                "inconsistency (F5's 'certified-0 then holds' is ASSERTED)")
        return dict(terminal="SWEEP-DEAD", routes=False,
                    why="raw 0 (certified-0 asserted): INTERLEAVING IS THE GATE")
    if raw_k >= XA.COUNT_CUTS["across_seeds"]:
        if certified >= XA.COUNT_CUTS["across_seeds"]:
            return dict(terminal="SWEEP-CONVERTS", routes=False,
                        why="raw>=5 AND certified>=5: PER-FRAME NOVELTY SUFFICES — triggers "
                            "the pre-named interior-concentration control (§4 rider) before "
                            "any paradigm-positive certifies")
        return dict(terminal="SIGNATURE-DIVERGENT", routes=True,
                    why=f"raw {raw_k}>=5 but certified {certified}<5 (EDGE-5, pre-named)")
    return dict(terminal="UNDERPOWERED", routes=True,
                why=f"raw {raw_k} in 1..4 post-EXT — below the >=5 bar")


def _tail_of(rec_full, band: float, N: int, tail_from: int = X17_PRIMARY_AT) -> dict:
    conv_full = XA._density_conversion_onset(rec_full, band, N)
    tail_vals = [c["exam_acc"] for c in rec_full["columns"]
                 if c["t"] > tail_from and c.get("exam_acc") is not None]
    le = XA._longest_episode(tail_vals, band, N)
    return dict(conv_onset_full=conv_full,
                first_converts_in_tail=bool(conv_full is not None and conv_full > tail_from),
                tail_longest_episode=le,
                tail_signature=("conversion" if le >= X17_SIG_DEPTH
                                else ("bare-N" if le > 0 else "none")))


def _tail_read(verdict_tag: str, band: float, N: int) -> dict:
    """1M descriptive tail (never gated). FULL untruncated records."""
    per = {}
    for s in X17_VERDICT_SEEDS + X17_EXT_POOL:
        p = _rec_path(s, verdict_tag)
        if p.exists():
            per[str(s)] = _tail_of(json.loads(p.read_text()), band, N)
    n_new = sum(1 for v in per.values() if v["first_converts_in_tail"])
    return dict(window=f"({X17_PRIMARY_AT}, 1000000]", per_seed=per,
                n_first_convert_in_tail=n_new,
                read=("FLAT" if n_new == 0 else f"{n_new} first-convert in the tail"))


def score_exp17(cal_read_tag: str = "exp17_cal_read", verdict_tag: str = "exp17verdict",
                cal_tag: str = "exp17cal", write: bool = True) -> dict:
    cal_read_p = OUTDIR / f"exp14_{cal_read_tag}.json"
    assert cal_read_p.exists(), "run cal_read_exp17 first (G4)"
    cr = json.loads(cal_read_p.read_text())
    assert "HALT" not in cr, f"cal read carries HALT {cr['HALT']} — the corridor is halted"
    band, N = cr["verdict_band"]["band"], cr["verdict_band"]["N"]
    loadable = cr["verdict_band"]["loadable"]

    base, ext = {}, {}
    for s in X17_VERDICT_SEEDS:
        r = _load(s, verdict_tag)
        assert r is not None, (f"verdict record s{s} missing — score_exp17 is BUILT, not run "
                               "(release only after the {0-7} records exist)")
        base[s] = _score_one(r, band, N)
    for s in X17_EXT_POOL:
        r = _load(s, verdict_tag)
        ext[s] = _score_one(r, band, N) if r is not None else None

    res = _ext_resolve(base, ext)
    read_recs = {s: _load(s, verdict_tag) for s in res["read_seeds"]}
    cal_accs = {}
    for s in X17_CAL_SEEDS:
        r = _load(s, cal_tag)
        assert r is not None, (f"cal record s{s} missing at score time - the floor audit/census "
                               "would FAIL OPEN on a partial pool (review C5); loud fail")
        cal_accs[s] = [a for (_, a, _) in XA._acc_series(r)]
    audit = _floor_audit(read_recs, band, N, cal_accs)
    assert audit["n_null_prefix"] > 0, "empty audit null pool - fail loud, never open (C5)" 
    census_ok = audit["census_selfaudit"]["census_ok"]

    formal = _partition17(res["k"], res["n_read"], loadable, audit["floor_clean"],
                          census_ok, audit["certified_count"])
    certified_read = _partition17(audit["certified_count"], res["n_read"], loadable,
                                  audit["floor_clean"], census_ok, audit["certified_count"])
    disagree = formal["terminal"] != certified_read["terminal"]
    routes = bool(formal["routes"] or disagree)

    fisher = XA._fisher_one_sided(res["k"], res["n_read"] - res["k"], 0, FISHER_BASELINE_A)
    grads = {str(s): _recency_gradient(read_recs[s]) for s in read_recs}
    tail = _tail_read(verdict_tag, band, N)

    out = dict(
        exp="exp17_verdict_DRAFT", gate="G6", arm=X17_ARM,
        verdict_band=cr["verdict_band"], ext=res, floor_audit=audit,
        TERMINAL=formal, certified_read=certified_read,
        formal_vs_certified_disagree=bool(disagree), routes_to_jason=routes,
        fisher_vs_A_0of8=dict(k=res["k"], n=res["n_read"], p=round(fisher, 5),
                              label=("conditional-on-extension" if res["fired"]
                                     else "design-fixed"), gated=False),
        c_shuffle_context=C_SHUFFLE_CONTEXT,
        companions=dict(gradient_persistence=grads, tail_1M=tail),
        DRAFT_note="G7 refute-default panel next: no lens assumes conversion or the orbit "
                   "story; attribution is Jason's (touch 3)",
        spec_hash=XA.C.spec_hash())
    if write:
        _dump(OUTDIR / f"exp14_exp17_verdict_{verdict_tag}.json", out)
    return out


# ======================================================================================== #
#  Smoke — composes the REAL functions on planted records/grids (§10.25.1 positive-delta)
# ======================================================================================== #
def _plant(onset=3000, run_len=0, n_runs=1, run_at=60, gap=15, band_val=0.67,
           n_cols=1400, p1=0.68, tail=0.54):
    """Synthetic record: EVAL-spaced columns; n_runs sustained >=band runs of run_len planted
    post-onset so the REAL detectors (XA._density_conversion_onset / _longest_episode /
    _episodes_ge) fire; gradient buckets ride pos_err_word (the EXP17 fallback path)."""
    cols = []
    starts = [run_at + i * (run_len + gap) for i in range(n_runs)] if run_len else []
    for i in range(n_cols):
        t = (i + 1) * EVAL
        v = 0.45
        for st in starts:
            if st <= i < st + run_len:
                v = band_val
        cols.append(dict(t=t, exam_acc=v, exam_n=8,
                         pos_err_word={X17_GRAD_P1: p1, X17_GRAD_TAIL: tail}))
    return dict(acquisition_onset=onset, columns=cols)


def smoke():
    ok = 0
    B, N = 0.62, 4

    # (sm-G6-census) F7 off-diagonals: DEPTH certifies alone; recurrence-only must NOT certify.
    # The second assert FAILS under EXP16's OR-rule (le>=8 OR ne>=2) — the F7 positive-delta.
    deep = _plant(run_len=X17_SIG_DEPTH + 2)                    # one long episode
    rec_only = _plant(run_len=4, n_runs=3)                      # 3 short episodes
    vals_d, vals_r = XA._post_acq(deep), XA._post_acq(rec_only)
    le_d = XA._longest_episode(vals_d, B, N)
    le_r = XA._longest_episode(vals_r, B, N)
    ne_r = len(XA._episodes_ge(vals_r, B, N))
    assert le_d >= X17_SIG_DEPTH, "single-long must certify (F7 depth-decisive)"
    assert le_r < X17_SIG_DEPTH and ne_r >= X17_SIG_RECUR, \
        "recurrence-only case malformed"
    or_rule_would_certify = (le_r >= X17_SIG_DEPTH or ne_r >= X17_SIG_RECUR)
    assert or_rule_would_certify, "the discriminating case must separate F7 from the OR-rule"
    audit = _floor_audit({0: deep, 1: rec_only},
                         B, N, {s: [0.45] * 900 for s in X17_CAL_SEEDS})
    cert = {c["seed"]: c["certified"] for c in audit["signature_census"]}
    assert cert[0] is True and cert[1] is False, \
        "F7: depth certifies, recurrence-only must NOT (fails under the EXP16 OR-rule)"
    print("SMOKE sm-G6-census: F7 off-diagonals — single-long certifies; recurrence-only does "
          "NOT (would certify under the superseded OR-rule)")
    ok += 1

    # (sm-G6-selfaudit) F12: a positive certified count must EXCEED the >=SIG_DEPTH bracket.
    # The phantom-depth zone is a LOW band (< 0.6): the contaminated null (>=0.6x8 exclusion)
    # RETAINS sub-0.6 depth-runs the self-excluded null removes — the own-band N in {6,7} case
    # the panel demonstrated (N=7 cut at band 0.52 on A's null). Stub falsifier: the bar must be
    # the >=SIG_DEPTH expectation, never the band-N bracket.
    B2 = 0.55
    hot_cal = {s: ([0.45] * 40 + [0.58] * 9 + [0.45] * 40 + [0.58] * 5 + [0.45] * 40) * 6
               for s in X17_CAL_SEEDS}                       # 9-runs AND 5-runs: band-N episodes
                                                             # outnumber depth episodes 2:1
    reads_1cert = {0: _plant(run_len=X17_SIG_DEPTH + 1, band_val=0.67, n_cols=120, run_at=20)}
    a2 = _floor_audit(reads_1cert, B2, N, hot_cal)
    sa = a2["census_selfaudit"]
    assert sa["expected_depth_runs_bracket"][0] == 0.0, \
        "self-excluded null cannot host depth-runs (everything >=N is excluded)"
    assert 0 < sa["bar"] < 1.0, \
        "contaminated null must retain the planted sub-0.6 depth-runs (sub-saturated)"
    assert sa["bar"] != a2["expected_phantom_bracket"][1], \
        "F12 falsifier: the bar must be the >=SIG_DEPTH expectation, not the band-N bracket " \
        "(band-N episodes outnumber depth episodes 2:1 in the planted null)"
    assert (a2["certified_count"] == 1 and
            sa["certified_exceeds_bar"] is bool(1 > sa["bar"])), "self-audit comparison wrong"
    quiet_cal = {s: [0.45] * 5400 for s in X17_CAL_SEEDS}
    reads_dead = {s: _plant() for s in range(8)}
    a3 = _floor_audit(reads_dead, B, N, quiet_cal)
    assert a3["census_selfaudit"]["census_ok"] is True and a3["certified_count"] == 0, \
        "certified 0 claims nothing — census_ok must hold (SWEEP-DEAD stays reachable)"
    print("SMOKE sm-G6-selfaudit: F12 bar = contaminated-null SIG_DEPTH-run expectation "
          "(low-band zone; not the band-N bracket); certified-0 passes through")
    ok += 1

    # (sm-G6-grid) partition terminals — all 8, the F5+F12 precedence
    assert _partition17(0, 8, True, True, True, 0)["terminal"] == "SWEEP-DEAD"
    assert _partition17(5, 8, True, True, True, 5)["terminal"] == "SWEEP-CONVERTS"
    assert _partition17(5, 8, True, True, True, 2)["terminal"] == "SIGNATURE-DIVERGENT"
    assert _partition17(2, 8, True, True, True, 0)["terminal"] == "UNDERPOWERED"
    assert _partition17(5, 7, True, True, True, 5)["terminal"] == "UNDERPOWERED"
    assert _partition17(5, 8, False, True, True, 5)["terminal"] == "DIRECTION-ONLY"
    assert _partition17(5, 8, True, False, True, 5)["terminal"] == "NOT-CERTIFIABLE-by-count"
    assert _partition17(5, 8, True, True, False, 5)["terminal"] == "NOT-CERTIFIABLE-by-census"
    print("SMOKE sm-G6-grid: 8 terminals, precedence loadable -> floor -> census -> n>=8 -> count")
    ok += 1

    # (sm-G2-lex) RB-2 lexicographic: the min-r*omega DECOY must LOSE (fails under the retired
    # objective), infeasible-higher-clip rejected, tie-break, empty -> None (HALT in caller)
    cells = [
        dict(r=1.05, w_deg=12, clip=_clip_halfwidth(1.05), feasible=True),   # min-r*omega decoy
        dict(r=0.85, w_deg=18, clip=_clip_halfwidth(0.85), feasible=True),   # max clip -> winner
        dict(r=0.80, w_deg=12, clip=_clip_halfwidth(0.80), feasible=False),  # higher clip, infeasible
        dict(r=0.85, w_deg=20, clip=_clip_halfwidth(0.85), feasible=True),   # tie-break loser
    ]
    w = _lexicographic_pick(cells)
    assert (w["r"], w["w_deg"]) == (0.85, 18), f"lexicographic winner wrong: {w}"
    decoy = min([c for c in cells if c["feasible"]],
                key=lambda c: c["r"] * math.radians(c["w_deg"]))
    assert (decoy["r"], decoy["w_deg"]) == (1.05, 12) and \
        (decoy["r"], decoy["w_deg"]) != (w["r"], w["w_deg"]), \
        "grid must separate the objectives — a min-r*omega selector FAILS this smoke (RB-2)"
    assert _lexicographic_pick([dict(r=1.0, w_deg=12, clip=0.1, feasible=False)]) is None
    print("SMOKE sm-G2-lex: lexicographic freeze (0.85,18); min-r*omega decoy loses; "
          "infeasible-higher-clip rejected; tie-break min omega; empty -> HALT")
    ok += 1

    # (sm-G4-grad) gradient FALLBACK path (EXP17 keeps grading: tail from pos_err_word)
    g = _recency_gradient(_plant(p1=0.69, tail=0.55))
    assert g["tail_from_probe"] is False and abs(g["delta"] - 0.14) < 0.011
    flat = _recency_gradient(_plant(p1=0.55, tail=0.545))
    assert flat["delta"] < X17_GRAD_ALARM, "collapse case must sit under the alarm threshold"
    print("SMOKE sm-G4-grad: fallback path (tail_from_probe=False); persistence vs collapse split")
    ok += 1

    # (sm-G6-score-one) F6 budget + conversion via the REAL detector on a planted run
    sc = _score_one(_plant(run_len=6), B, N)
    assert sc["status"] == "READ" and sc["converted"] and sc["conversion_onset"] is not None
    sc2 = _score_one(_plant(onset=X17_PRIMARY_AT - 10_000), B, N)
    assert sc2["status"] == "UNREAD(budget-truncated)"
    sc3 = _score_one(dict(acquisition_onset=None, columns=[]), B, N)
    assert sc3["status"] == "UNREAD(unacquired)"
    print("SMOKE sm-G6-score-one: READ+convert on planted run; budget + unacquired gates fire")
    ok += 1

    # (sm-G6-ext) D1: substitution-first toward n>=8; no-fire EXCLUDES EXT
    base = {s: dict(status=("READ" if s < 7 else "UNREAD(unacquired)"), converted=False)
            for s in range(8)}
    ext = {8: dict(status="READ", converted=False), 9: None}
    res = _ext_resolve(base, ext)
    assert res["fired"] and res["substituted"] == 1 and res["n_read"] == 8
    base8 = {s: dict(status="READ", converted=(s < 5)) for s in range(8)}
    res2 = _ext_resolve(base8, ext)
    assert not res2["fired"] and 8 not in res2["read_seeds"], "no-fire must exclude EXT"
    print("SMOKE sm-G6-ext: substitution-first to the floor; no-fire excludes EXT")
    ok += 1

    # (sm-G2-feas) R6 item (i) + review C2/C25: _cell_feasible COMPUTED on planted per-seed
    # measurement dicts — a pooled-only-clearing cell (one seed below a floor) must be
    # INFEASIBLE; per-seed-worst ceilings gate on the SEED STATISTIC; arc + anchor_over cases.
    base = dict(np11=0.145, tr11=0.090, path11=1.636, confusion=1.311)
    def _m(np11, tr11, ps=0.20, ps_max=0.5, tr_max=None, over=0):
        return dict(np11=np11, tr11=tr11, tr11_max=(tr_max if tr_max is not None else tr11),
                    perstep_med=ps, perstep_max=ps_max, anchor_over=over)
    good = [_m(0.62, 0.24) for _ in range(8)]
    c = _cell_feasible(good, base, 0.85, 18)
    assert c["feasible"], f"all-clear cell must be feasible: {c}"
    pooled_only = [_m(0.62, 0.24) for _ in range(7)] + [_m(0.40, 0.24)]   # one seed below 4x
    c = _cell_feasible(pooled_only, base, 0.85, 18)
    assert not c["feasible"] and c["np_min"] < 4 * base["np11"], \
        "pooled-only-clearing cell must be REJECTED (per-seed-worst, R6 item i)"
    ceil_seed = [_m(0.62, 0.24) for _ in range(7)] + [_m(0.62, 0.52)]     # one SEED over 0.50
    assert not _cell_feasible(ceil_seed, base, 0.85, 18)["feasible"], \
        "ceiling gates on the per-seed statistic (seed mean over 0.50)"
    dwell_tail = [_m(0.62, 0.24, tr_max=0.9) for _ in range(8)]           # raw dwell max only
    assert _cell_feasible(dwell_tail, base, 0.85, 18)["feasible"], \
        "raw per-dwell maxima are REPORTED companions, never gated (review C16)"
    arc_fail = [_m(0.62, 0.24) for _ in range(8)]
    assert not _cell_feasible(arc_fail, base, 0.85, 8)["feasible"], \
        "arc lower edge must reject (r*w*(k-1) < tremble path)"
    over = [_m(0.62, 0.24, over=1)] + [_m(0.62, 0.24) for _ in range(7)]
    assert not _cell_feasible(over, base, 0.85, 18)["feasible"], "anchor_over must reject"
    print("SMOKE sm-G2-feas: _cell_feasible computed — pooled-only rejected; per-seed-statistic "
          "ceilings; raw maxima ungated; arc + anchor_over reject")
    ok += 1

    # (sm-G6-trunc) F13 positive-delta (review C4/C24): a full-1M record loaded through _load
    # must truncate to the 500k prefix and CHANGE the null pool vs the full record
    import tempfile
    full = _plant(n_cols=3000)                       # columns to t=900,000
    tmp = Path(tempfile.gettempdir()) / "exp14_exp12_dwell_orbit_s99_smoketrunc.json"
    tmp.write_text(json.dumps(full))
    try:
        loaded = XA._truncate(json.loads(tmp.read_text()), X17_PRIMARY_AT)
        n_pre = len(loaded["columns"])
        assert n_pre < 3000 and loaded["columns"][-1]["t"] <= X17_PRIMARY_AT, \
            "truncation must clip the 500k prefix"
        accs_full = {0: [c["exam_acc"] for c in full["columns"]]}
        accs_pre = {0: [c["exam_acc"] for c in loaded["columns"]]}
        n_full = sum(len(sg) for sg in XA._null_segments(accs_full, B, N))
        n_prefix = sum(len(sg) for sg in XA._null_segments(accs_pre, B, N))
        assert n_prefix < n_full, "the falsifier: a full-record pool MUST differ (F13)"
    finally:
        tmp.unlink(missing_ok=True)
    print("SMOKE sm-G6-trunc: F13 — 500k-prefix truncation live; full-record pool differs "
          "(the failing falsifier)")
    ok += 1

    # (sm-G4-halts) review C10/C23: every G4 HALT branch fires through the REAL cal_read path
    # (records planted on disk under a scratch tag, removed after)
    scratch = []
    def _put(seed, rec):
        pp = _rec_path(seed, "smokeg4")
        pp.write_text(json.dumps(rec)); scratch.append(pp)
    try:
        for i, sd in enumerate(X17_CAL_SEEDS):       # liveness: only 2/5 acquired
            _put(sd, _plant() if i < 2 else dict(acquisition_onset=None, columns=[]))
        out = cal_read_exp17(cal_tag="smokeg4", write=False)
        assert any("liveness" in h for h in out.get("HALT", [])), "liveness HALT must fire"
        for sd in X17_CAL_SEEDS:                     # cal-converts -> Ruling-B recut
            # s0-class runs (>= EPISODE_BAND 0.704 x >= 8): excluded from the honest null,
            # so the provisional band cuts BELOW them and they read as cal conversions
            _put(sd, _plant(run_len=12, band_val=0.72))
        out2 = cal_read_exp17(cal_tag="smokeg4", write=False)
        assert out2["verdict_band"]["loadable"] is False and "between-episode" in \
            out2["verdict_band"]["method"], "cal-converts must recut own null, non-loadable"
    finally:
        for pp in scratch:
            pp.unlink(missing_ok=True)
    print("SMOKE sm-G4-halts: liveness HALT + cal-converts Ruling-B recut fire through the "
          "real cal_read path")
    ok += 1

    # (sm-G2-noop) review C17: the omega=0 no-op falsifier — a static-anchor orbit reads
    # tremble-like on net/path while the live orbit separates (contrast form)
    tr_m = measure_kinematics(X17_TREMBLE_ARM, 3, 12_000, 12_000)
    live = measure_kinematics(X12.orbit_arm(0.85, 18), 3, 12_000, 12_000)
    dead = measure_kinematics(X12.orbit_arm(0.85, 0), 3, 12_000, 12_000)
    assert live["np11"] >= 3.5 * tr_m["np11"], "live orbit must separate on net/path"
    assert dead["np11"] < 2.0 * tr_m["np11"], \
        f"omega=0 must read tremble-like (got {dead['np11']:.3f} vs tremble {tr_m['np11']:.3f})"
    print("SMOKE sm-G2-noop: omega=0 falsifier — static anchor reads tremble-like; live orbit "
          "separates (the no-op cannot pass the contrast floor)")
    ok += 1

    # (sm-G6-selfaudit-refuse) review m19: a POSITIVE certified count at-or-below the bar must
    # refuse THROUGH the real audit (census_ok False -> NOT-CERTIFIABLE-by-census)
    hot9 = {s2: ([0.45] * 20 + [0.58] * 9 + [0.45] * 20) * 40 for s2 in X17_CAL_SEEDS}
    # TWO read seeds so the expected >=SIG_DEPTH count can exceed 1 (per-seed p saturates at 1);
    # certified = 1 (one deep converter) <= bar (~2) -> the F12 REFUSAL fires via the REAL audit
    reads_low = {0: _plant(run_len=X17_SIG_DEPTH + 1, band_val=0.67, n_cols=1400),
                 1: _plant(n_cols=1400)}
    a4 = _floor_audit(reads_low, 0.55, N, hot9)
    bar4 = a4["census_selfaudit"]["bar"]
    assert bar4 > 1.0, f"planted null too cold (bar {bar4}) — refusal branch not exercised"
    assert a4["census_selfaudit"]["census_ok"] is False and a4["certified_count"] == 1
    t = _partition17(5, 8, True, True, a4["census_selfaudit"]["census_ok"], 5)
    assert t["terminal"] == "NOT-CERTIFIABLE-by-census"
    print("SMOKE sm-G6-selfaudit-refuse: certified 1 <= bar (~2, two reads) refuses through "
          "the REAL audit")
    ok += 1

    # (sm-G6-fisher) exact Fisher companions reproduce the committed table
    for (k, n), want in {(5, 8): 0.0128, (5, 9): 0.0204, (5, 10): 0.0294,
                         (3, 8): 0.1002, (4, 9): 0.0529, (4, 10): 0.0686}.items():
        got = XA._fisher_one_sided(k, n - k, 0, 8)
        assert abs(got - want) < 5e-4, f"fisher ({k},{n}) {got} != {want}"
    print("SMOKE sm-G6-fisher: Fisher-vs-A-0/8 table reproduces to 4dp")
    ok += 1

    print(f"\nexp17_score smoke: {ok} checks PASS")
    return ok


# ======================================================================================== #
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--anchor", action="store_true",
                    help="F4-A digit-exact anchor bind on A fabric (measurer's own frozen "
                         "outputs; writes the re-base artifact on green; CPU, 8x 1M builds)")
    ap.add_argument("--baselines", action="store_true",
                    help="the four measured floor references (A fabric @100k)")
    ap.add_argument("--select", action="store_true",
                    help="G2 (r,omega) lexicographic selection (needs the orbit arm)")
    ap.add_argument("--g2-verify", action="store_true",
                    help="G2 verification half: replay + deployed-1M floors + freeze artifact")
    ap.add_argument("--onset-marginal", action="store_true")
    ap.add_argument("--cal-read", action="store_true")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--release", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        smoke()
    elif args.anchor:
        print(json.dumps(anchor_assert(), indent=1))
    elif args.baselines:
        print(json.dumps(measure_tremble_baselines(), indent=1))
    elif args.select:
        out = select_orbit()
        print(f"SELECTED: {out['selected']}")
    elif args.g2_verify:
        out = g2_verify()
        print(f"G2 VERIFY OK: frozen {out['frozen']} feasible at deployed 1M; "
              f"onset-marginal W1 {out['onset_marginal']['mean_w1']:.4f}")
    elif args.onset_marginal:
        print(json.dumps(onset_marginal_delta(), indent=1))
    elif args.cal_read:
        out = cal_read_exp17()
        print(json.dumps({k: v for k, v in out.items() if k != "gradient"}, indent=1)[:1800])
    elif args.score:
        if not args.release:
            print("WITHHELD: score_exp17 is BUILT, not run — release requires --release "
                  "(and the {0-7} records)")
        else:
            out = score_exp17()
            print(out["TERMINAL"])
    else:
        ap.print_help()
