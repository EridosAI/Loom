"""EXP21 — G3b calibration and dynamic range (prereg §3.6/§4; gate G3b).

Runs AFTER the 10 calibration runs (2 arms x cal seeds {20,21,22,24,25} x 1M waves, from
scratch, primary+shadow banks scored at every planned read) exist on disk. Cuts EVERY
constant fresh, in-regime, outcome-blind (no verdict data exists), with formula + measured
inputs + resulting value + provenance committed to exp21_constants.json (§4.2/§4.4/§4.7).

THE LAWS (deployed FUNCTIONS below — the observed-red fixtures exercise these same
functions, never inline restatements; the build-review panel's dead-fixture findings are
the reason for this structure):
  * assert_grid_complete — every probe artifact's read grid must equal the planned grid
    (t=0, every 3,000, exactly read_at); silent truncation is a HALT, not a shorter series.
  * t_eligible = first planned read at or after cfg.t2 — COMPUTED (== 3,000 asserted).
  * episode_start — first N_ACQ=5-consecutive-read episode >= theta from t_eligible.
  * initial_state_law — theta_cat must leave every calibration t=0 read below theta_cat;
    failure is a HALT, never a threshold adjustment.
  * The 4,096-stream null: fixed class-balance-preserving label permutations, one per
    stream across the full series, evaluated over BOTH arms and all 10 cal runs;
    theta_cat = smallest attainable k/2048 with k/2048 >= 0.5 + delta_point_cat AND
    <= 4/4,096 streams producing any five-read episode. ALL law applications use
    full-precision series (rounding lives only in display artifacts — the panel's
    exact-grid-point >=/< finding).
  * Q4 = (750,000, read_at], 84 planned reads at the 1M horizon; FQ occupancy; the
    familywise bound = smallest attainable k/84 reached by <= 4/4,096 streams (the §4.2
    count applied to §4.3 — the only in-document referent, surfaced for Touch 2).
  * Repeatability envelopes (§4.4): 99th-pct primary-vs-shadow differences, pointwise and
    run-level, with pointwise companions and maxima reported.
  * viability_fails — chance-referenced broad-guard law (common bars, both arms).
  * dynamic_range_route — §3.6 mechanical: BOTH-QUESTIONS-LIVE /
    PRESERVATION-ONLY-RESTRICTION / HALT-UNSUPPORTED; OFF collapse recorded, never tuned.
  * verify_constants — the row-56 recompute-verify guard: a committed theta that does not
    reproduce from its inputs is a HALT (the null_threshold_injection fixture fires THIS).
"""

from __future__ import annotations

import argparse
import itertools
import json
import statistics
import sys
import time
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp21_probe as P21                                      # noqa: E402
import exp21_teaching as T21                                   # noqa: E402
from sculpt_config import SculptConfig                         # noqa: E402

OUTDIR21 = T21.OUTDIR21
CAL_TAG = "cal"
N_NULL = 4096
NULL_KEY = 410000 * 1_000_003      # offline scorer-side permutation seed (recorded; never a
#                                    live generator — the audit families are live-RNG only)
FAMILYWISE_COUNT = 4               # §4.2's "at most 4/4,096" (applied identically to §4.3)
GRID = 2048                        # attainable bacc grid: k/2048 (balanced 1024/class)
GUARD_AXES = ("coarse_a", "distractor", "member")
CHANCE = dict(category=0.5, coarse_a=0.25, distractor=0.5, member=1.0 / 16)
INTERNAL_METRICS = ("exam_acc", "asg_cat")                     # pre-named, direction ON > OFF


# ------------------------------------------------------------------ loading
def probe_path(arm: str, seed: int, tag: str, bank: str) -> Path:
    return OUTDIR21 / f"exp21_{arm}_s{seed}_{tag}.probe_{bank}.pt"


def record_path(arm: str, seed: int, tag: str) -> Path:
    return OUTDIR21 / f"exp21_{arm}_s{seed}_{tag}.json"


def load_probe(arm: str, seed: int, tag: str, bank: str) -> dict:
    p = torch.load(probe_path(arm, seed, tag, bank), weights_only=False)
    js = json.loads(probe_path(arm, seed, tag, bank).with_suffix(".json").read_text())
    p["summaries"] = js["reads"]
    return p


def cat_labels(ev_member: torch.Tensor) -> torch.Tensor:
    cfg = SculptConfig(seed=0)
    return (ev_member % cfg.n_B) % cfg.n_category


def bacc_series(pred: torch.Tensor, lab: torch.Tensor) -> torch.Tensor:
    """(n_reads, N) int8 predictions + (N,) labels -> (n_reads,) balanced accuracy.
    FULL PRECISION — every law application uses this; rounding is display-only."""
    counts = [int((lab == c).sum()) for c in (0, 1)]
    assert counts[0] == counts[1], f"category labels not balanced: {counts}"
    out = []
    for c in (0, 1):
        m = lab == c
        out.append((pred[:, m] == c).float().mean(1))
    return (out[0] + out[1]) / 2


# ------------------------------------------------------------------ deployed law functions
def assert_summary_integrity(series: torch.Tensor, summaries: list, where: str):
    """From-raw integrity: the recomputed category series must equal the in-run summaries
    digit-exactly (deployed on every cal/verdict/verify load; the raw_column_mutation
    fixture fires THIS)."""
    for i, rd in enumerate(summaries):
        assert abs(rd["axes"]["category"]["bacc"] - round(float(series[i]), 6)) < 5e-7, \
            f"probe summary/prediction mismatch at {where} read {i}"


def assert_grid_complete(ts: list[int], read_at: int):
    """The read grid MUST be the planned grid for its horizon (§3.3) — silent truncation
    or an off-plan grid is a HALT. Deployed on every cal AND verdict scoring path."""
    want = T21.planned_reads(read_at)
    assert list(ts) == want, \
        (f"read grid incomplete/off-plan: {len(ts)} reads ending {ts[-1] if ts else None} "
         f"!= planned {len(want)} ending {want[-1]} for read_at={read_at}")


def assert_record_complete(rec: dict, read_at: int):
    """Run-record completeness: the horizon and the final eval column must match the
    planned horizon (last column at read_at - read_at % EVAL)."""
    assert rec["read_at"] == read_at, \
        f"record read_at {rec['read_at']} != required horizon {read_at}"
    want_last = read_at - (read_at % T21.EVAL)
    got_last = rec["columns"][-1]["t"] if rec["columns"] else None
    assert got_last == want_last, \
        f"record truncated: last eval column t={got_last} != planned {want_last}"


def eligible_index(ts: list[int], t2: int) -> int:
    """§4.2: the first planned read at or after cfg.t2 — computed, then asserted == 3000."""
    for i, t in enumerate(ts):
        if t >= t2:
            return i
    raise AssertionError("no eligible read on the planned grid")


def episode_start(series: torch.Tensor, ts: list[int], theta: float, i_elig: int,
                  n_acq: int = T21.N_ACQ):
    """First qualifying N_ACQ-read episode start time (or None). >= theta, consecutive
    PLANNED reads, window start at or after t_eligible."""
    ok = (series >= theta).tolist()
    for i in range(i_elig, len(ok) - n_acq + 1):
        if all(ok[i:i + n_acq]):
            return ts[i]
    return None


def initial_state_law(t0s: dict, theta: float):
    """§4.2: theta must leave EVERY calibration initial state below the acquisition law —
    failure is a HALT, never a threshold adjustment. (The t0_acquisition fixture feeds a
    hot t=0 through THIS function.)"""
    hot = {k: v for k, v in t0s.items() if not (v < theta)}
    assert not hot, f"calibration initial state at/above theta_cat — HALT: {hot}"


def acq_area(series: torch.Tensor, ts: list[int], theta: float, i_elig: int,
             upto: int = T21.Q4_FROM) -> float:
    """§4.5 acquisition summary: normalized area above theta from t_eligible through 750k."""
    sel = [i for i, t in enumerate(ts) if ts[i_elig] <= t <= upto]
    vals = (series[sel] - theta).clamp_min(0)
    return float(vals.mean())


def q4_indices(ts: list[int], upto: int) -> list[int]:
    """§4.3: Q4 = (750,000, read_at] — the upper bound is the ratified horizon, passed
    explicitly (never inferred from whatever the artifact happens to end at)."""
    return [i for i, t in enumerate(ts) if T21.Q4_FROM < t <= upto]


def fq_of(series: torch.Tensor, ts: list[int], theta: float, upto: int) -> float:
    q4 = q4_indices(ts, upto)
    assert q4, "empty Q4 — the retention law has no reads (grid must reach past 750k)"
    return float((series[q4] >= theta).float().mean())


def viability_fails(guards_q4: dict, pr_q4: float, bars: dict) -> list:
    """§4.7 broad-viability law (deployed; used by the cal OFF-collapse record, the verdict
    scorer, and the nonbiting_guard fixture): guard q FAILS iff its Q4-mean <= bar(q)."""
    fails = [q for q in GUARD_AXES if guards_q4[q] <= bars[q]]
    if pr_q4 <= bars["participation_ratio"]:
        fails.append("participation_ratio")
    return fails


def dynamic_range_route(on_runs: list[dict], ts: list[int], i_elig: int,
                        floor: float) -> dict:
    """§3.6 mechanical dynamic-range route over the ON-calibration summaries.
    Each entry: dict(series_max, acq_onset, fq). Returns the route + inputs.
    (The ceilinged_on fixture drives THIS function, never a hardcoded string.)"""
    on_max = max(r["series_max"] for r in on_runs)
    unsupported = on_max < floor                               # never resolvable above floor
    imm = [r["acq_onset"] == ts[i_elig] for r in on_runs]
    acq_ceilinged = all(imm)                                   # every ON cal acquires at once
    ret_ceilinged = all(r["fq"] == 1.0 for r in on_runs)
    if unsupported or (acq_ceilinged and ret_ceilinged):
        route = "HALT-UNSUPPORTED"                             # §3.6: no answerable question
    elif acq_ceilinged:
        route = "PRESERVATION-ONLY-RESTRICTION"
    else:
        route = "BOTH-QUESTIONS-LIVE"
    return dict(route=route, on_max_bacc=round(on_max, 6), floor=round(floor, 6),
                acq_immediate_flags=imm, ret_ceilinged=ret_ceilinged)


def verify_constants(committed: dict, recomputed_theta: float):
    """The row-56 recompute-verify guard: the committed theta must reproduce exactly from
    the committed inputs. (The null_threshold_injection fixture fires THIS function.)"""
    got = committed["theta_cat"]["value"]
    assert got == recomputed_theta, \
        f"theta_cat does not reproduce: committed {got} != recomputed {recomputed_theta} — HALT"


def null_perms(n: int = N_NULL, n_ev: int = 2048) -> torch.Tensor:
    g = torch.Generator().manual_seed(NULL_KEY)
    return torch.stack([torch.randperm(n_ev, generator=g) for _ in range(n)])


def null_bacc_matrix(pred: torch.Tensor, lab: torch.Tensor, perms: torch.Tensor) -> torch.Tensor:
    """(n_reads, N) predictions x (P, N) permutations -> (P, n_reads) null balanced accuracy.
    One permutation fixed across the full series per stream (temporal correlation preserved).
    Exact balance asserted (the formula divides by N/2 per class)."""
    labp = lab[perms]                                          # (P, N)
    A0 = (labp == 0).float()                                   # (P, N)
    assert int(A0.sum(1).min()) == int(A0.sum(1).max()) == pred.shape[1] // 2, \
        "permuted labels not exactly balanced"
    A1 = (labp == 1).float()
    out = torch.empty(perms.shape[0], pred.shape[0])
    for r in range(pred.shape[0]):
        p0 = (pred[r] == 0).float()
        p1 = (pred[r] == 1).float()
        out[:, r] = (A0 @ p0 + A1 @ p1) / pred.shape[1]
    return out


def stream_episode_max(B: torch.Tensor, i_elig: int, n_acq: int = T21.N_ACQ) -> torch.Tensor:
    """(P, n_reads) null series -> (P,) max over eligible windows of the window MIN."""
    win = B.unfold(1, n_acq, 1)                                # (P, n_windows, n_acq)
    mins = win.min(-1).values
    return mins[:, i_elig:].max(1).values if mins.shape[1] > i_elig else mins.max(1).values


def stream_fq(B: torch.Tensor, ts: list[int], theta: float, upto: int) -> torch.Tensor:
    q4 = q4_indices(ts, upto)
    return (B[:, q4] >= theta).float().mean(1)


def q99(xs: list[float]) -> float:
    s = sorted(xs)
    return s[min(len(s) - 1, int(0.99 * len(s)))]


# ------------------------------------------------------------------ per-run summaries
def run_summary(arm: str, seed: int, tag: str = CAL_TAG, *, horizon: int = T21.H21) -> dict:
    rec = json.loads(record_path(arm, seed, tag).read_text())
    assert_record_complete(rec, horizon)
    out = dict(arm=arm, seed=seed, banks={})
    for bank in ("primary", "shadow"):
        if not probe_path(arm, seed, tag, bank).exists():
            continue
        p = load_probe(arm, seed, tag, bank)
        assert_grid_complete(p["ts"], horizon)
        lab = cat_labels(p["ev_member"])
        s = bacc_series(p["predictions"], lab)                 # FULL precision
        assert_summary_integrity(s, p["summaries"], f"{arm} s{seed} {bank}")
        q4 = set(q4_indices(p["ts"], horizon))
        out["banks"][bank] = dict(
            ts=p["ts"], series_t=s,                            # tensor, full precision (laws)
            t0=float(s[0]),
            series_max=float(s.max()),
            guards_q4={q: statistics.mean(rd["axes"][q]["bacc"]
                                          for i, rd in enumerate(p["summaries"])
                                          if i in q4) for q in GUARD_AXES},
            pr_q4=statistics.mean(rd["geom"]["participation_ratio"]
                                  for i, rd in enumerate(p["summaries"]) if i in q4),
            guards_series={q: [rd["axes"][q]["bacc"] for rd in p["summaries"]]
                           for q in GUARD_AXES},
            pr_series=[rd["geom"]["participation_ratio"] for rd in p["summaries"]])
    cols = rec["columns"]
    q4c = [c for c in cols if T21.Q4_FROM < c["t"] <= horizon]
    out["internal_q4"] = {
        "exam_acc": (statistics.mean(c["exam_acc"] for c in q4c
                                     if c.get("exam_acc") is not None)
                     if any(c.get("exam_acc") is not None for c in q4c) else None),
        "asg_cat": statistics.mean(c["asg_cat"] for c in q4c) if q4c else None}
    return out


# ------------------------------------------------------------------ the cut
def cut_constants(cal_seeds=None, tag: str = CAL_TAG) -> tuple[dict, dict]:
    cal_seeds = cal_seeds or T21.CAL_SEEDS21
    cfg = SculptConfig(seed=0)
    runs = {(arm, s): run_summary(arm, s, tag)
            for arm, s in itertools.product(("on", "off"), cal_seeds)}
    ts = runs[("on", cal_seeds[0])]["banks"]["primary"]["ts"]
    for r in runs.values():
        assert r["banks"]["primary"]["ts"] == ts, "planned read grids differ across cal runs"
        assert "shadow" in r["banks"], "calibration run missing its shadow bank"
    i_elig = eligible_index(ts, cfg.t2)
    assert ts[i_elig] == 3000, f"t_eligible computed {ts[i_elig]} != 3000 under the current grid"

    # --- delta_point_cat + pointwise guard envelopes (needed before theta) ---
    pt_diffs, guard_pt = [], {q: [] for q in list(GUARD_AXES) + ["participation_ratio"]}
    for r in runs.values():
        sp, ss = r["banks"]["primary"]["series_t"], r["banks"]["shadow"]["series_t"]
        pt_diffs += (sp - ss).abs().tolist()
        for q in GUARD_AXES:
            gp = torch.tensor(r["banks"]["primary"]["guards_series"][q], dtype=torch.float64)
            gs = torch.tensor(r["banks"]["shadow"]["guards_series"][q], dtype=torch.float64)
            guard_pt[q] += (gp - gs).abs().tolist()
        pp = torch.tensor(r["banks"]["primary"]["pr_series"], dtype=torch.float64)
        ps = torch.tensor(r["banks"]["shadow"]["pr_series"], dtype=torch.float64)
        guard_pt["participation_ratio"] += (pp - ps).abs().tolist()
    delta_point_cat = q99(pt_diffs)

    # --- the 4,096-stream null over BOTH arms x all cal runs ---
    perms = null_perms()
    M_p = torch.zeros(N_NULL)
    null_B = {}
    for key, r in runs.items():
        p = load_probe(r["arm"], r["seed"], tag, "primary")
        lab = cat_labels(p["ev_member"])
        B = null_bacc_matrix(p["predictions"], lab, perms)
        null_B[key] = B
        M_p = torch.maximum(M_p, stream_episode_max(B, i_elig))

    # --- theta_cat: smallest attainable value on the k/2048 grid (from k = GRID/2 = 0.5,
    #     letter-faithful: the >= 0.5 + delta floor is applied as written, not pre-clipped) ---
    floor = 0.5 + delta_point_cat
    theta_cat = None
    for k in range(GRID // 2, GRID + 1):
        c = k / GRID
        if c >= floor and int((M_p >= c).sum()) <= FAMILYWISE_COUNT:
            theta_cat = c
            break
    assert theta_cat is not None, "no attainable theta_cat satisfies the joint law — HALT"
    null_exceed = int((M_p >= theta_cat).sum())

    # --- initial-state law (deployed function; HALT, never an adjustment) ---
    t0s = {f"{a}_s{s}": runs[(a, s)]["banks"]["primary"]["t0"] for a, s in runs}
    initial_state_law(t0s, theta_cat)

    # --- retention familywise bound on the k/84 grid ---
    n_q4 = len(q4_indices(ts, T21.H21))
    assert n_q4 == 84, f"Q4 planned-read count {n_q4} != 84"
    FQ_p = torch.zeros(N_NULL)
    for key, B in null_B.items():
        FQ_p = torch.maximum(FQ_p, stream_fq(B, ts, theta_cat, T21.H21))
    fq_bound = None
    for k in range(0, n_q4 + 1):
        c = k / n_q4
        if int((FQ_p >= c).sum()) <= FAMILYWISE_COUNT:
            fq_bound = c
            break
    assert fq_bound is not None, "no attainable FQ bound — HALT"

    # --- per-run real summaries at theta (full-precision laws) ---
    for r in runs.values():
        for bank in ("primary", "shadow"):
            b = r["banks"][bank]
            b["acq_onset"] = episode_start(b["series_t"], ts, theta_cat, i_elig)
            b["acq_area"] = acq_area(b["series_t"], ts, theta_cat, i_elig)
            b["fq"] = fq_of(b["series_t"], ts, theta_cat, T21.H21)

    # --- run-level envelopes ---
    delta_acq = q99([abs(r["banks"]["primary"]["acq_area"] - r["banks"]["shadow"]["acq_area"])
                     for r in runs.values()])
    delta_ret = q99([abs(r["banks"]["primary"]["fq"] - r["banks"]["shadow"]["fq"])
                     for r in runs.values()])
    delta_guard_q4 = {}
    for q in GUARD_AXES:
        delta_guard_q4[q] = q99([abs(r["banks"]["primary"]["guards_q4"][q]
                                     - r["banks"]["shadow"]["guards_q4"][q])
                                 for r in runs.values()])
    delta_guard_q4["participation_ratio"] = q99(
        [abs(r["banks"]["primary"]["pr_q4"] - r["banks"]["shadow"]["pr_q4"])
         for r in runs.values()])
    delta_guard_point = {q: q99(v) for q, v in guard_pt.items()}

    # --- internal-metric envelopes (within-arm cal-seed pairwise spread, outcome-blind) ---
    delta_internal = {}
    for m in INTERNAL_METRICS:
        per_arm = []
        for arm in ("on", "off"):
            vals = [runs[(arm, s)]["internal_q4"][m] for s in cal_seeds]
            assert all(v is not None for v in vals), f"internal metric {m} unsupported in cal"
            diffs = [abs(a - b) for a, b in itertools.combinations(vals, 2)]
            per_arm.append(q99(diffs))
        delta_internal[m] = max(per_arm)

    guard_bars = {q: round(CHANCE[q] + delta_guard_q4[q], 6) for q in GUARD_AXES}
    guard_bars["participation_ratio"] = round(1.0 + delta_guard_q4["participation_ratio"], 6)

    # --- §3.6 dynamic-range route (deployed function) ---
    on_inputs = [dict(series_max=runs[("on", s)]["banks"]["primary"]["series_max"],
                      acq_onset=runs[("on", s)]["banks"]["primary"]["acq_onset"],
                      fq=runs[("on", s)]["banks"]["primary"]["fq"]) for s in cal_seeds]
    dr = dynamic_range_route(on_inputs, ts, i_elig, floor)
    off_collapse = []
    for s in cal_seeds:
        b = runs[("off", s)]["banks"]["primary"]
        fails = viability_fails(b["guards_q4"], b["pr_q4"], guard_bars)
        if len(fails) >= 2:
            off_collapse.append(dict(seed=s, failed=fails))

    constants = dict(
        theta_cat=dict(
            value=theta_cat,
            formula="smallest k/2048 with k/2048 >= 0.5 + delta_point_cat AND "
                    "#(null streams with any 5-read episode across all 10 cal runs) <= 4/4096",
            inputs=dict(delta_point_cat=round(delta_point_cat, 8),
                        floor=round(floor, 8), null_exceed_at_theta=null_exceed,
                        null_M_top8=[round(float(x), 6)
                                     for x in M_p.sort(descending=True).values[:8]]),
            provenance="cut on the 10 calibration runs' committed primary-bank predictions "
                       "before any verdict data exists; null seed "
                       f"{NULL_KEY} (offline scorer-side)"),
        t_eligible=dict(value=ts[i_elig], formula="first planned read >= cfg.t2 (=1200)",
                        asserted=True),
        n_acq=dict(value=T21.N_ACQ, provenance="EXP21 design constant fixed by ratification"),
        q4=dict(from_wave=T21.Q4_FROM, upto=T21.H21, n_reads=n_q4),
        fq_null_bound=dict(
            value=fq_bound,
            formula="smallest k/84 with #(null streams whose max-over-runs Q4 occupancy at "
                    "theta_cat >= k/84) <= 4/4096",
            inputs=dict(null_FQ_top8=[round(float(x), 6)
                                      for x in FQ_p.sort(descending=True).values[:8]]),
            note="the §4.2 familywise count (<=4/4096) applied identically to §4.3's bound — "
                 "the only in-document count referent; surfaced for the Touch-2 read"),
        delta_point_cat=delta_point_cat,
        delta_acq=delta_acq, delta_ret=delta_ret,
        delta_guard_point=delta_guard_point,
        delta_guard_q4=delta_guard_q4,
        delta_internal=delta_internal,
        guard_bars=guard_bars,
        repeatability_companions=dict(
            pointwise_cat_max=max(pt_diffs), pointwise_cat_mean=statistics.mean(pt_diffs),
            pointwise_guard_max={q: max(v) for q, v in guard_pt.items()},
            n_pointwise=len(pt_diffs)),
        guard_law=dict(
            viability="guard q FAILS iff Q4-mean <= chance_q + delta_guard_q4(q); PR FAILS iff "
                      "Q4-mean PR <= 1 + delta_guard_q4(PR); OFF NONVIABLE iff >= 2 broad "
                      "guards fail among {coarse_a, distractor, member, PR}; category excluded",
            selectivity="category advantage selective iff adv_cat > adv_q + delta_guard_q4(q) "
                        "for BOTH q in {coarse_a, distractor}; adv = paired ON-OFF Q4-mean "
                        "margin difference on the axis",
            collapse="the improving arm's category gain is wrong-reason iff that arm's paired "
                     "Q4-mean on distractor OR member falls beyond delta_guard_q4(q), or its "
                     "Q4-mean PR <= floor (applied in BOTH directions by the scorer)",
            general="if the improving arm's benefit on any word-unnamed bacc axis "
                    "{coarse_a, distractor, member} >= its category advantage while that "
                    "advantage clears repeatability -> GENERAL-STABILISATION (rank rides as "
                    "a reported companion; scale-mismatched with bacc, surfaced at Touch 2)"),
        internal_law=dict(metrics=list(INTERNAL_METRICS), direction="ON > OFF",
                          form="Q4-mean; fires iff ON-OFF > delta_internal(m)"),
        familywise_count=FAMILYWISE_COUNT, n_null=N_NULL, null_seed=NULL_KEY,
        grid="k/2048 (balanced 1024/class)")
    calibration = dict(
        cal_seeds=cal_seeds, tag=tag, planned_reads=len(ts), ts_head=ts[:3], ts_tail=ts[-3:],
        runs={f"{a}_s{s}": dict(
            primary={k: (round(v, 6) if isinstance(v, float) else v)
                     for k, v in runs[(a, s)]["banks"]["primary"].items()
                     if k not in ("series_t", "guards_series", "pr_series")},
            primary_series=[round(float(x), 6)
                            for x in runs[(a, s)]["banks"]["primary"]["series_t"]],
            shadow={k: (round(v, 6) if isinstance(v, float) else v)
                    for k, v in runs[(a, s)]["banks"]["shadow"].items()
                    if k not in ("series_t", "guards_series", "pr_series")},
            internal_q4={k: (round(v, 6) if v is not None else None)
                         for k, v in runs[(a, s)]["internal_q4"].items()})
            for a, s in runs},
        dynamic_range=dr,
        off_broad_collapse=off_collapse)
    return constants, calibration


# ------------------------------------------------------------------ observed-red fixtures
def _fixtures(constants: dict, ts: list[int], i_elig: int) -> dict:
    """§7 G3b fixtures — synthetic INPUTS through the DEPLOYED law functions (never inline
    restatements; the build-review panel's dead-fixture findings bind here)."""
    reds = {}
    theta = constants["theta_cat"]["value"]
    n = len(ts)

    # null_threshold_injection: verify_constants must FIRE on an injected theta
    inj = dict(constants, theta_cat=dict(constants["theta_cat"], value=0.6))
    try:
        verify_constants(inj, theta)
        raise SystemExit("verify_constants blind to an injected theta — dead guard, HALT")
    except AssertionError as e:
        reds["null_threshold_injection"] = dict(red=True, message=str(e)[:160])
    verify_constants(constants, theta)                         # restore-green on the real value

    # chance_converter: a chance-level series must certify through the REAL episode law at a
    # BROKEN theta (reachable falsifier) and must NOT certify at the real theta_cat
    chance = torch.full((n,), 0.5)
    broken = episode_start(chance, ts, 0.5, i_elig)
    assert broken is not None, "acquisition law cannot fire even at theta=0.5 — dead law, HALT"
    real = episode_start(chance, ts, theta, i_elig)
    assert real is None, f"chance series certified at theta_cat={theta} — HALT"
    reds["chance_converter"] = dict(red=True, broken_theta_certifies_at=broken,
                                    real_theta_certifies=False)

    # t0_acquisition: a hot t=0 must trip the DEPLOYED initial-state law
    hot_t0 = {"syn_s0": min(1.0, theta + 2.0 / GRID)}
    try:
        initial_state_law(hot_t0, theta)
        raise SystemExit("initial_state_law blind to a hot t=0 — dead law, HALT")
    except AssertionError as e:
        reds["t0_acquisition"] = dict(red=True, message=str(e)[:160])
    initial_state_law({"syn_s0": 0.5}, theta)                  # restore-green

    # ceilinged_on: synthetic ON summaries through the DEPLOYED dynamic-range route
    hot = torch.full((n,), min(1.0, theta + 2.0 / GRID))
    on_syn = [dict(series_max=float(hot.max()),
                   acq_onset=episode_start(hot, ts, theta, i_elig),
                   fq=0.5) for _ in range(5)]
    dr = dynamic_range_route(on_syn, ts, i_elig, floor=0.5)
    assert dr["route"] == "PRESERVATION-ONLY-RESTRICTION", \
        f"dynamic-range route blind to a ceilinged ON: {dr['route']} — dead route, HALT"
    on_syn_dead = [dict(r, fq=1.0) for r in on_syn]
    dr2 = dynamic_range_route(on_syn_dead, ts, i_elig, floor=0.5)
    assert dr2["route"] == "HALT-UNSUPPORTED", \
        f"both-ceilinged must HALT: {dr2['route']}"
    reds["ceilinged_on"] = dict(red=True, restriction_route=dr["route"],
                                both_ceilinged_route=dr2["route"])

    # empty_q4: a truncated grid must make the DEPLOYED laws refuse — both the retention
    # law (empty Q4) and the grid-completeness law (the panel's silent-truncation finding)
    short_ts = [t for t in ts if t <= 600_000]
    try:
        fq_of(torch.zeros(len(short_ts)), short_ts, theta, T21.H21)
        raise SystemExit("retention law accepted an empty Q4 — dead law, HALT")
    except AssertionError as e:
        msg1 = str(e)[:120]
    try:
        assert_grid_complete(short_ts, T21.H21)
        raise SystemExit("assert_grid_complete accepted a truncated grid — dead law, HALT")
    except AssertionError as e:
        reds["empty_q4"] = dict(red=True, fq_message=msg1, grid_message=str(e)[:120])

    # nonbiting_guard: through the DEPLOYED viability law — dead bars catch nothing; the
    # REAL bars must catch a fully collapsed (chance-level, rank-1) input
    collapsed = dict(coarse_a=CHANCE["coarse_a"], distractor=CHANCE["distractor"],
                     member=CHANCE["member"])
    dead_bars = {q: CHANCE[q] - 1.0 for q in GUARD_AXES}
    dead_bars["participation_ratio"] = 0.0
    fails_dead = viability_fails(collapsed, 1.0, dead_bars)
    assert not fails_dead, f"expected the dead-bar guard to be non-biting: {fails_dead}"
    fails_real = viability_fails(collapsed, 1.0, constants["guard_bars"])
    assert len(fails_real) >= 2, \
        f"REAL viability law cannot bite a collapsed input: {fails_real} — HALT"
    reds["nonbiting_guard"] = dict(red=True, dead_bar_fails=fails_dead,
                                   real_bar_fails=fails_real)
    return reds


def probe_cost_profile() -> dict:
    """§10.2: measured (never 'free') runtime cost of one planned read."""
    loop, _, _ = T21.build_exp21("on", 20, steps=64)
    bank = P21.write_bank(20, "primary")
    P21.probe_read(loop, bank)                                 # warm
    t0 = time.perf_counter()
    for _ in range(10):
        P21.probe_read(loop, bank)
    per_read = (time.perf_counter() - t0) / 10
    return dict(seconds_per_read_per_bank=round(per_read, 4),
                emissions_per_read=2560,
                reads_per_full_run=len(T21.planned_reads(T21.H21)),
                projected_seconds_per_run_per_bank=round(
                    per_read * len(T21.planned_reads(T21.H21)), 1))


def main(tag: str = CAL_TAG) -> dict:
    torch.set_num_threads(1)
    missing = [(a, s) for a in ("on", "off") for s in T21.CAL_SEEDS21
               if not record_path(a, s, tag).exists()]
    assert not missing, f"calibration runs missing: {missing}"
    constants, calibration = cut_constants(tag=tag)
    ts = T21.planned_reads(T21.H21)
    i_elig = eligible_index(ts, SculptConfig(seed=0).t2)
    reds = _fixtures(constants, ts, i_elig)
    # the row-56 recompute-verify guard, on the real committed cut
    c2, _ = cut_constants(tag=tag)
    verify_constants(constants, c2["theta_cat"]["value"])
    cost = probe_cost_profile()
    calibration["observed_red"] = reds
    calibration["probe_cost"] = cost
    T21.write_gate_artifact(OUTDIR21 / "exp21_constants.json", constants)
    T21.write_gate_artifact(OUTDIR21 / "exp21_calibration.json", calibration)
    route = calibration["dynamic_range"]["route"]
    assert route != "HALT-UNSUPPORTED", "dynamic range HALT: no answerable question — surfaced"
    T21.gatelog_append(dict(gate="G3b", outcome="PASS", executor="exp21_cal.main",
                            theta_cat=constants["theta_cat"]["value"], route=route,
                            reds=sorted(reds)))
    print(f"G3b: theta_cat={constants['theta_cat']['value']} route={route} "
          f"reds={sorted(reds)}")
    return dict(constants=constants, calibration=calibration)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut", action="store_true")
    args = ap.parse_args()
    if args.cut:
        main()
