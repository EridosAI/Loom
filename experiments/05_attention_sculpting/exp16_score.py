"""EXP16 CAPTURE-FEED — cal-read (G4) + guarded §4-partition DRAFT scorer (G6).

BUILT under AMD-12 (Jason 2026-07-11). The prereg §6 build scope enumerated the arm flag + the
read-only probe but never the SCORER; both EXP14 (`score_2x2`) and EXP15 (`score_durability`)
carried an explicit build-the-guarded-scorer step and EXP16's §6 scoped it out — the omission
survived five review layers and was caught by the corridor's gate-executor audit ("executable by
what?"). This module is that missing step. It implements ONLY pre-named routes (prereg §2 gate /
§4 partition / §5 rows); it adds no route, constant, or definition of its own beyond the ratified
participation bar (corridor G2 / AMD-11) and the read-time observables the routes require.

Executors (corridor gate-executor audit — every gate names its function + positive-delta smoke ID):
  G4  band / liveness / participation / gradient / cal-converts  -> cal_read_exp16   (smoke sc-G4-*)
  G6  §4-partition DRAFT (WORD-SIDE / VISION-SIDE / DOSE-STARV /  -> score_exp16      (smoke sc-G6-*)
      EXT-fire / UNDERPOWERED / cal-converts-SHIFTED direction-only)

Reuses `exp14_arms` as the helper LIBRARY (band cut, borrow-gate, one-sided Fisher, floor-audit
primitives, density converter detector, §13.4 acquisition detector, _truncate) so the run-level
machinery + constants are SHARED, not re-implemented. Reads only; no dynamics, no new loss/force;
threads=1 determinism inherited. GUARDED: `score_exp16` refuses a verdict read until the {0-7}
records exist, and __main__ withholds it behind --release (the score_2x2 build-not-run pattern).
Primary frozen at 500k on all seeds (XA._truncate); the 1M tail is descriptive only.
"""
import sys
import json
import statistics
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import torch                                                      # noqa: E402
torch.set_num_threads(1)
import exp14_arms as XA                                           # noqa: E402  (helper library)

X10 = XA.X10
OUTDIR = XA.OUTDIR
EVAL = XA.EVAL

# ============================================================================================
# EXP16 SCORING-ONLY constants. These MUST NOT enter C.spec_hash()'s payload — the runs are
# `run_exp14_arm` VERBATIM, so a reused EXP14 record and a fresh EXP16 record carry the SAME
# run-level spec_hash. These are read-side classifiers, identical discipline to the EXP15 block.
# ============================================================================================
X16_ARM           = "exp12_dwell_expomid"
X16_CAL_SEEDS     = [20, 21, 22, 24, 25]
X16_VERDICT_SEEDS = list(range(8))                 # {0-7}, n=8 base
X16_EXT_POOL      = [8, 9]                          # count-extension pool (AMD-3/9)
X16_SUBST_POOL    = list(range(10, 20))            # {10-19} FRESH pre-check substitution (AMD-7/10)
X16_READ_FLOOR    = 8                               # AMD-9/D1: READ n>=8 for ANY certifiable cell
#                                                    (NOT XA.N_MIN_READ=3 — that is EXP14's floor)
X16_CAL_LIVE_MIN  = 3                               # corridor G4: cal liveness >= 3/5 acquired
X16_ACT_FLOOR     = 0.01                            # activity observable == §13.4 acquisition floor
X16_PRIMARY_AT    = XA.READ_AT                      # 500k; primary frozen here, 1M tail descriptive

# --- participation bar: RATIFIED before cal, X-blind (corridor G2 / AMD-11); frozen constant ---
X16_PARTICIP_RHO    = 0.167869                      # X:A word-target occasion ratio (exp08/exp16_rho_bar.json)
X16_PARTICIP_ANCHOR = 0.776                         # committed A-arm exp12_dwell {0-7} activity-frac median
X16_PARTICIP_HALF   = 0.5
X16_PARTICIP_BAR    = 0.065133                      # = 0.5 * 0.776 * 0.167869
assert abs(X16_PARTICIP_BAR - X16_PARTICIP_HALF * X16_PARTICIP_ANCHOR * X16_PARTICIP_RHO) < 1e-6, \
    "X16 participation bar drift vs 0.5*0.776*rho (amend-path rule: fail loudly on numeric drift)"

# --- recency-gradient referent: A's verdict-pooled POST-ACQUISITION gradient (AMD-2; verified 4x;
#     docs/EXP16_FORENSIC_FACTCHECK.md). Δ = p1 - p13-48 = 0.6915 - 0.5499 = +0.1416. REPORTED, not gated.
X16_GRAD_REF_A    = dict(p1=0.6915, p13_48=0.5499, delta=0.1416)
X16_GRAD_P1       = "p1"                            # POS_BUCKETS onset bucket (pos 1)
X16_GRAD_TAIL     = "p13-48"                        # POS_BUCKETS tail bucket (pos 13-48)

# --- cal-converts borrow-gate donor: A_dwell scheduled dwelled marginal (prereg §4). Recomputed
#     live from A_dwell's committed cal; the prereg-stated band is drift-checked, never hard-trusted.
X16_BORROW_DONOR    = "exp12_dwell"
X16_A_BAND_PREREG   = (0.6111, 4)                  # prereg §4 stated A_dwell band; asserted vs recompute
X16_BASELINE_A_0OF8 = 8                            # A's committed 0/8 (Fisher companion 2x2 [[k,n-k],[0,8]])


# --------------------------------------------------------------------------- record IO (disk)
def _rec_path(seed: int, tag: str, arm: str = X16_ARM) -> Path:
    return OUTDIR / f"exp14_{arm}_s{seed}_{tag}.json"


def _load(seed: int, tag: str, arm: str = X16_ARM, primary_at: int = X16_PRIMARY_AT):
    """Load a run record and freeze it to the primary horizon (drop columns past primary_at).
    Returns None if absent — the guard on missing records lives in the callers."""
    p = _rec_path(seed, tag, arm)
    if not p.exists():
        return None
    return XA._truncate(json.loads(p.read_text()), primary_at)


# ===================================== PURE read-time observables (smoke-tested in-memory) ====
def _activity_fraction(rec) -> float | None:
    """Gate-2 statistic (§2): fraction of POST-ONSET eval windows with num >= X16_ACT_FLOOR.
    None if unacquired (Gate 1 handles that case) or no post-onset windows."""
    onset = rec.get("acquisition_onset")
    if onset is None:
        return None
    post = [c for c in rec["columns"] if c["t"] >= onset]
    if not post:
        return None
    return sum(1 for c in post if c.get("num", 0.0) >= X16_ACT_FLOOR) / len(post)


def _recency_gradient(rec) -> dict:
    """§5 companion (REPORTED, not gated): X's recency gradient Δ = p1 - p13-48, pooled over
    post-onset columns. p1 from `pos_err_word` (onset-exam training stash); p13-48 from
    `probe_pos_err_word` (the read-only mid-dwell probe — X's mid-dwell word loss is deleted, so
    pos_err_word is structurally empty at the tail). Falls back to pos_err_word for the tail when
    no probe field exists (so the reader also reproduces A's gradient from committed records)."""
    onset = rec.get("acquisition_onset")
    p1s, tails = [], []
    for c in rec["columns"]:
        if onset is not None and c["t"] < onset:
            continue
        pw = c.get("pos_err_word") or {}
        pp = c.get("probe_pos_err_word") or {}
        if X16_GRAD_P1 in pw:
            p1s.append(pw[X16_GRAD_P1])
        if X16_GRAD_TAIL in pp:                       # X: the probe carries the tail
            tails.append(pp[X16_GRAD_TAIL])
        elif X16_GRAD_TAIL in pw:                     # A / any real-loss arm: tail from training stash
            tails.append(pw[X16_GRAD_TAIL])
    p1 = statistics.mean(p1s) if p1s else None
    tail = statistics.mean(tails) if tails else None
    delta = (p1 - tail) if (p1 is not None and tail is not None) else None
    return dict(p1=round(p1, 5) if p1 is not None else None,
                p13_48=round(tail, 5) if tail is not None else None,
                delta=round(delta, 5) if delta is not None else None,
                p1_n=len(p1s), tail_n=len(tails), tail_from_probe=bool(tails and any(
                    X16_GRAD_TAIL in (c.get("probe_pos_err_word") or {}) for c in rec["columns"])))


def _participation_gate(cal_recs: dict) -> dict:
    """§2 word-participation gate (bar form AMD-11). Two levels, EXTERNAL anchor fixed before cal:
      Gate 1 — acquired at all: acquisition fires on EVERY READ cal seed. Fail -> DEAD (12b-inert).
      Gate 2 — reference scale: MEDIAN across READ cal seeds of the activity fraction >= X16_PARTICIP_BAR.
    Gate1 pass + Gate2 fail = the STARVED middle -> DOSE-STARVATION-CONFOUNDED (routes, no attribution)."""
    acq = {s: (r.get("acquisition_onset") is not None) for s, r in cal_recs.items()}
    # Gate 1 fails ONLY when participation is DEAD — the 12b-inert class where onset NEVER fires
    # (NO cal seed acquires). "fires on every READ cal seed" is over the acquired subset (READ ==
    # acquired here), so the gate tests non-emptiness of that subset, not all-acquire; the >=3/5
    # liveness pre-gate separately HALTs the mostly-inert case. Review MAJOR catch (all -> any).
    gate1 = bool(acq) and any(acq.values())
    afs = {s: _activity_fraction(r) for s, r in cal_recs.items() if acq[s]}
    af_vals = [v for v in afs.values() if v is not None]
    med = statistics.median(af_vals) if af_vals else None
    gate2 = bool(med is not None and med >= X16_PARTICIP_BAR)
    status = "ALIVE" if (gate1 and gate2) else ("STARVED" if gate1 else "DEAD")
    return dict(gate1_not_inert=gate1, per_seed_acquired=acq,
                per_seed_activity={s: round(v, 5) for s, v in afs.items() if v is not None},
                gate2_median_activity=round(med, 5) if med is not None else None,
                bar=X16_PARTICIP_BAR, gate2_pass=gate2, status=status)


def _score_one(rec, band: float, N: int, primary_at: int = X16_PRIMARY_AT) -> dict:
    """Per-seed READ/UNREAD + conversion (density-matched detector at the cal band). READ requires
    acquisition AND the F6 budget (>= MIN_CONV_BUDGET post-acq runway to the primary horizon)."""
    onset = rec.get("acquisition_onset")
    if onset is None:
        return dict(status="UNREAD(unacquired)", acquisition_onset=None, conversion_onset=None, converted=False)
    if (primary_at - onset) < XA.MIN_CONV_BUDGET:
        return dict(status="UNREAD(budget-truncated)", acquisition_onset=onset, conversion_onset=None, converted=False)
    conv = XA._density_conversion_onset(rec, band, N)
    return dict(status="READ", acquisition_onset=onset, conversion_onset=conv, converted=bool(conv is not None))


def _floor_audit(verdict_recs: dict, band: float, N: int, cal_per_seed_accs: dict) -> dict:
    """Floor-audit (§4 "floor-clean"), the [[feedback_loose_N_false_alarm]] carry as a coded gate
    (mirrors phantom_floor_gate — EPISODE unit, contiguity-respected, upper-bound null). The null is
    X's OWN cal between-episode pool. at_floor = P(observed-or-more | floor) > 0.10 -> NOT-CERTIFIABLE.
    verdict_recs: {seed: truncated record} for the READ seeds being counted."""
    segs = XA._null_segments(cal_per_seed_accs, XA.CONV_LOW, XA.CONV_MIN)
    n_pos = sum(max(0, len(sg) - N + 1) for sg in segs)
    ep_lens = [L for sg in segs for L in XA._episodes_ge(sg, band, N)]
    n_ep = len(ep_lens)
    ep_rate = (n_ep / n_pos) if n_pos else 0.0
    ps_ep, observed = [], []
    for s, rec in verdict_recs.items():
        vals = XA._post_acq(rec)
        m = max(0, len(vals) - N + 1)
        ps_ep.append(1 - (1 - ep_rate) ** m)
        # `observed` uses _longest_episode (gap-collapsed) while the count k uses
        # _density_conversion_onset (a run resets on a None-exam gap), so observed ⊇ density-converters
        # — this only makes the floor MORE lenient (smaller P(X>=observed)), never manufactures a
        # headline (WORD-SIDE is driven by k); identical to the ratified EXP15 phantom_floor_gate.
        if XA._longest_episode(vals, band, N) > 0:
            observed.append(s)
    # A cell with ZERO observed crossings has no phantom to flag -> vacuously floor-clean. Else
    # _poisson_binomial_ge(ps, 0) == 1.0 would force at_floor=True and make VISION-SIDE MASSING /
    # DOSE-STARVATION-CONFOUNDED unreachable — the review's blocking catch; k=0 is the headline case.
    p_ge = XA._poisson_binomial_ge(ps_ep, len(observed)) if (ps_ep and observed) else None
    at_floor = bool(p_ge is not None and p_ge > 0.10)
    return dict(band=round(band, 4), N=N, null="X cal between-episode (conversions+shoulders excluded)",
                n_null_positions=n_pos, n_null_episodes=n_ep, episode_rate=round(ep_rate, 8),
                expected_phantom_EPISODE=round(sum(ps_ep), 3), observed_converters=len(observed),
                observed_seeds=observed, P_observed_or_more_under_floor=round(p_ge, 5) if p_ge is not None else None,
                at_floor=at_floor, floor_clean=not at_floor)


def _donor_band(cal_seeds=None):
    """A_dwell provisional band + null (borrow-gate donor). Recomputed from committed A_dwell cal;
    the prereg-stated X16_A_BAND_PREREG is drift-checked (surfaced, never silently trusted)."""
    cal_seeds = cal_seeds or X16_CAL_SEEDS
    accs = {}
    for s in cal_seeds:
        p = _rec_path(s, "cal", arm=X16_BORROW_DONOR)
        if p.exists():
            accs[s] = [a for (_, a, _) in XA._acc_series(XA._truncate(json.loads(p.read_text()), X16_PRIMARY_AT))]
    band, N, null = XA._provisional_cut(accs)
    drift = (round(band, 4) != X16_A_BAND_PREREG[0]) or (N != X16_A_BAND_PREREG[1])
    return (band, N), null, dict(recomputed=(round(band, 4), N), prereg=X16_A_BAND_PREREG, drift=bool(drift))


def _cal_converts_branch(x_per_seed_accs: dict, n_cal_conv: int, own_band, own_N) -> dict:
    """§4 cal-converts fallback (Jason ruling 1). If X's cal seeds convert, the own marginal is
    contaminated -> the borrow-gate decides loadability:
      NOT-SHIFTED -> borrow A_dwell's band; counts LOADABLE; the partition applies unchanged.
      SHIFTED     -> own between-episode null; counts NON-LOADABLE; primary DEMOTES to direction-only.
    No cal conversion -> CAL-CLEAN, own provisional band, loadable."""
    if n_cal_conv < 1:
        return dict(kind="CAL-CLEAN", loadable=True, band=round(own_band, 4), N=own_N,
                    method="OWN provisional §10.22 honest-null (cal does not convert)")
    (a_band, a_N), a_null, drift = _donor_band()
    x_between = XA._between_episode_null(x_per_seed_accs)
    gate = XA._borrow_gate((a_band, a_N), a_null, x_between)
    if gate["borrow_ok"]:
        return dict(kind="CAL-CONVERTS / NOT-SHIFTED", loadable=True, band=round(a_band, 4), N=a_N,
                    method="BORROW A_dwell marginal (borrow-gate PASS); counts loadable",
                    donor_band_drift=drift, borrow_gate=gate)
    own_b, own_N2 = XA._joint_band_cut(x_between)
    return dict(kind="CAL-CONVERTS / SHIFTED", loadable=False, band=round(own_b, 4), N=own_N2,
                method="OWN between-episode null (borrow-gate SHIFTED); counts NON-loadable -> "
                       "primary DIRECTION-ONLY + §5 companion; attribution routes to Jason",
                donor_band_drift=drift, borrow_gate=gate)


def _partition(k: int, n_read: int, floor_clean: bool, particip_status: str, loadable: bool) -> dict:
    """The §4 count-primary partition — every path terminates at a NAMED route (AMD-3/9/10).
    Precedence: loadability (cal-converts SHIFTED) -> floor-audit -> certifiability floor n>=8 ->
    count. A path matching two route labels still resolves to a single 'route to Jason' destination."""
    if not loadable:
        return dict(terminal="DIRECTION-ONLY", routes=True,
                    why="cal-converts SHIFTED — counts non-loadable vs A (§10.24 C precedent)")
    if not floor_clean:
        return dict(terminal="NOT-CERTIFIABLE", routes=True,
                    why="floor-audit AT-FLOOR — crossing count carries no signal")
    if n_read < X16_READ_FLOOR:
        return dict(terminal="UNDERPOWERED", routes=True,
                    why=f"READ n={n_read} < {X16_READ_FLOOR} (certifiability floor; EXT exhausted or unspent)")
    if k >= XA.COUNT_CUTS["across_seeds"]:            # >= 5
        return dict(terminal="WORD-SIDE CAPTURE", routes=False,
                    why=f"count {k} >= 5, floor-clean, READ n={n_read} >= 8")
    if k == 0:
        if particip_status == "ALIVE":
            return dict(terminal="VISION-SIDE MASSING", routes=False,
                        why="count 0, floor-clean, READ n>=8, participation ALIVE (both gates)")
        return dict(terminal="DOSE-STARVATION-CONFOUNDED", routes=True,
                    why=f"count 0 but participation {particip_status} (dead or starved middle) — "
                        "massing vs dose-starvation not separable")
    return dict(terminal="UNDERPOWERED", routes=True,
                why=f"count {k} in {{1..4}} after extension at READ n={n_read} — below the >=5 bar")


def _ext_resolve(base: dict, ext: dict) -> dict:
    """D1 EXT logic (AMD-9). base/ext: {seed: _score_one(...)}. EXT_POOL {8,9} serves TWO jobs;
    when both fire, SUBSTITUTION (cover UNREAD base seeds to reach the n>=8 floor) takes priority
    over count-extension. Both jobs add the EXT seed to the READ pool; the accounting is recorded."""
    base_read = [s for s, v in base.items() if v["status"] == "READ"]
    base_unread = [s for s, v in base.items() if v["status"] != "READ"]
    base_k = sum(v["converted"] for v in base.values())
    n_read_base = len(base_read)
    k_base = base_k
    # decide whether EXT fires: base is non-terminal if n_read<8 (needs substitution) OR 1<=k<=4
    fires = (n_read_base < X16_READ_FLOOR) or (1 <= k_base <= 4)
    if not fires:
        return dict(fired=False, n_read=n_read_base, k=k_base, read_seeds=base_read,
                    substituted=0, extended=0, ext_used=[])
    ext_read = [s for s, v in ext.items() if v["status"] == "READ"]
    n_sub = min(len(base_unread), len(ext_read))            # substitution first
    n_ext = len(ext_read) - n_sub                           # remainder extends the count
    n_read_final = n_read_base + len(ext_read)
    k_final = k_base + sum(v["converted"] for v in ext.values() if v["status"] == "READ")
    return dict(fired=True, n_read=n_read_final, k=k_final, read_seeds=base_read + ext_read,
                substituted=n_sub, extended=n_ext, ext_used=sorted(ext.keys()),
                note=f"EXT fired: {n_sub} to substitution (cover UNREAD base), {n_ext} to count-extension")


# ===================================================================== G4: cal read (executor)
def cal_read_exp16(cal_tag: str = "exp16cal", out_tag: str = "exp16_cal_read") -> dict:
    """G4 (corridor). Single-arm cal read on `exp12_dwell_expomid` {20,21,22,24,25} @ 500k (primary
    frozen; 1M tail descriptive). Produces: own provisional band, liveness (>=3/5), the §2
    participation gate (Gate1/Gate2 vs the ratified bar), the §5 recency gradient (median vs A's
    +0.1416 referent — REPORTED), and the cal-converts borrow branch (loadable / direction-only).
    HALTS the corridor (flag) if liveness < 3/5 (experiment unposed). Records exp14_{out_tag}.json."""
    recs = {s: _load(s, cal_tag) for s in X16_CAL_SEEDS}
    missing = [s for s, r in recs.items() if r is None]
    if missing:
        raise AssertionError(f"EXP16 cal records missing for seeds {missing} (tag={cal_tag})")
    per_seed_accs = {s: [a for (_, a, _) in XA._acc_series(r)] for s, r in recs.items()}
    band, N, pooled = XA._provisional_cut(per_seed_accs)
    cal_conv = {s: (XA._density_conversion_onset(recs[s], band, N) is not None) for s in X16_CAL_SEEDS}
    n_cal_conv = sum(cal_conv.values())
    acq = {s: recs[s].get("acquisition_onset") is not None for s in X16_CAL_SEEDS}
    n_acq = sum(acq.values())
    live = n_acq >= X16_CAL_LIVE_MIN
    particip = _participation_gate(recs)
    grads = {s: _recency_gradient(recs[s]) for s in X16_CAL_SEEDS}
    gdeltas = [g["delta"] for g in grads.values() if g["delta"] is not None]
    grad_med = statistics.median(gdeltas) if gdeltas else None
    branch = _cal_converts_branch(per_seed_accs, n_cal_conv, band, N)
    out = dict(
        exp="exp16_cal_read", arm=X16_ARM, cal_seeds=X16_CAL_SEEDS, primary_at=X16_PRIMARY_AT,
        provisional_own=dict(band=round(band, 4), N=N, n_null=len(pooled)),
        liveness=dict(n_acquired=n_acq, n_cal=len(X16_CAL_SEEDS), n_min=X16_CAL_LIVE_MIN, live=bool(live)),
        cal_converters=cal_conv, n_cal_converters=n_cal_conv,
        participation=particip,
        gradient=dict(per_seed={s: g for s, g in grads.items()}, median_delta=grad_med,
                      referent_A=X16_GRAD_REF_A,
                      note="cross-seed-set: X cal seeds vs A verdict-pool referent (AMD-2); REPORTED, not gated"),
        cal_converts_branch=branch,
        verdict_band=dict(band=branch["band"], N=branch["N"], loadable=branch["loadable"]),
        participation_bar=dict(bar=X16_PARTICIP_BAR, rho=X16_PARTICIP_RHO, anchor=X16_PARTICIP_ANCHOR,
                               formula="0.5 * 0.776 * rho", provenance="corridor G2 / AMD-11 (X-blind); "
                               "exp08/exp16_rho_bar.json"),
        alpha=XA.ALPHA, spec_hash=XA.C.spec_hash())
    if not live:
        out["HALT"] = f"corridor G4: liveness {n_acq}/{len(X16_CAL_SEEDS)} < {X16_CAL_LIVE_MIN} — experiment unposed"
    (OUTDIR / f"exp14_{out_tag}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: v for k, v in out.items() if k not in ("gradient",)}, indent=2))
    print(f"\n[cal_read_exp16] band {branch['band']}x{branch['N']} ({branch['kind']}, loadable={branch['loadable']})  "
          f"liveness {n_acq}/{len(X16_CAL_SEEDS)} live={live}  participation={particip['status']} "
          f"(median act {particip['gate2_median_activity']} vs bar {X16_PARTICIP_BAR})  "
          f"grad median Δ={grad_med} vs A {X16_GRAD_REF_A['delta']}")
    return out


# ===================================================================== G6: DRAFT scorer (executor)
def score_exp16(cal_read_tag: str = "exp16_cal_read", verdict_tag: str = "exp16verdict",
                ext_tag: str = "exp16verdict", ext_seeds=None, write: bool = True) -> dict:
    """G6 (corridor). The §4 count-primary partition DRAFT. GUARDED: refuses until the {0-7} records
    exist (build-not-run). Reads the cal band + loadability from cal_read; scores base {0-7}, fires
    EXT {8,9} under the D1 priority when non-terminal, applies floor-audit + participation gate, and
    routes every landing to a NAMED terminal. Fisher companion vs A's committed 0/8. §5 2x2 companion
    REPORTED (not gated). DRAFT: routes behind the §7.1 refute-default panel before any attribution."""
    calp = OUTDIR / f"exp14_{cal_read_tag}.json"
    if not calp.exists():
        raise AssertionError(f"cal_read record {cal_read_tag} absent — run cal_read_exp16 first")
    cal = json.loads(calp.read_text())
    if cal.get("HALT"):
        raise AssertionError(f"cal_read HALTED ({cal['HALT']}) — score_exp16 refuses (corridor G4 fail)")
    band, N = cal["verdict_band"]["band"], cal["verdict_band"]["N"]
    loadable = cal["verdict_band"]["loadable"]
    ext_seeds = ext_seeds if ext_seeds is not None else X16_EXT_POOL

    base_recs = {s: _load(s, verdict_tag) for s in X16_VERDICT_SEEDS}
    if any(r is None for r in base_recs.values()):
        miss = [s for s, r in base_recs.items() if r is None]
        raise AssertionError(f"EXP16 verdict records {miss} missing — score_exp16 is BUILT, not run "
                             "(the score_2x2 guard). Release only after the {0-7} runs exist.")
    base = {s: _score_one(r, band, N) for s, r in base_recs.items()}

    # EXT fires only if base is non-terminal (n_read<8 or 1<=k<=4)
    ext_recs = {s: _load(s, ext_tag) for s in ext_seeds}
    ext = {s: _score_one(r, band, N) for s, r in ext_recs.items() if r is not None}
    ext_avail = {s: r for s, r in ext_recs.items() if r is not None}
    res = _ext_resolve(base, ext if ext_avail else {})
    k, n_read = res["k"], res["n_read"]

    # floor-audit over the READ seeds that converted, on X's own cal between-episode null
    cal_accs = {s: [a for (_, a, _) in XA._acc_series(_load(s, "exp16cal"))] for s in X16_CAL_SEEDS} \
        if all(_rec_path(s, "exp16cal").exists() for s in X16_CAL_SEEDS) else {}
    # floor-audit population MUST be the authoritative counted cell (res["read_seeds"]) — else when
    # EXT does NOT fire, k/n_read are base-only (8) while READ EXT records would still be audited (up
    # to 10), a denominator mismatch between the count and its floor gate. Review MAJOR catch.
    _all_recs = {**base_recs, **{s: r for s, r in ext_recs.items() if r is not None}}
    read_recs = {s: _all_recs[s] for s in res["read_seeds"] if s in _all_recs}
    floor = _floor_audit(read_recs, band, N, cal_accs) if cal_accs else dict(
        floor_clean=True, note="cal null unavailable — floor-audit skipped (records absent)")
    particip_status = cal["participation"]["status"]

    partition = _partition(k, n_read, floor.get("floor_clean", True), particip_status, loadable)
    fisher = XA._fisher_one_sided(k, max(0, n_read - k), 0, X16_BASELINE_A_0OF8) if n_read else None

    gm = cal["gradient"]["median_delta"]
    companion_2x2 = dict(
        gradient_median_delta_X=gm, referent_A=X16_GRAD_REF_A["delta"],
        convert_status=("convert" if k > 0 else "dead"), participation=particip_status,
        rows="collapse+convert=full causal chain; collapse+dead=VISION-SIDE(if participation ALIVE) "
             "else DOSE-STARVATION-CONFOUNDED; no-collapse+convert=MECHANISM ANOMALY; "
             "no-collapse+dead=probe contradicts the drift premise — routes",
        note="§5 companion REPORTED, not gated (instrument-sanity only). The collapse call vs the "
             f"A referent (+{X16_GRAD_REF_A['delta']}) routes to Jason at attribution.")

    out = dict(
        exp="exp16_capture_feed", arm=X16_ARM, cal_read_tag=cal_read_tag, verdict_tag=verdict_tag,
        conv_band=band, conv_consec=N, loadable=loadable, primary_at=X16_PRIMARY_AT,
        base_seeds=X16_VERDICT_SEEDS, ext_seeds=ext_seeds, ext=res,
        n_read=n_read, n_converted=k, converter_seeds=[s for s in res["read_seeds"]
                                                       if (base.get(s) or ext.get(s, {})).get("converted")],
        floor_audit=floor, participation=cal["participation"],
        TERMINAL=partition["terminal"], routes_to_jason=partition["routes"], terminal_why=partition["why"],
        fisher_vs_A_0of8=dict(k=k, n=n_read, one_sided_p=round(fisher, 5) if fisher is not None else None,
                              note=f"exact Fisher [[{k},{n_read - k}],[0,8]] vs A's committed 0/8"),
        mechanism_companion_2x2=companion_2x2,
        per_seed_base=base, per_seed_ext=ext,
        DRAFT_note="DRAFT — routes behind the §7.1 refute-default panel (no lens assumes conversion or "
                   "the recency story) before any attribution reaches Jason. A clean panel is necessary, "
                   "never sufficient.",
        spec_hash=XA.C.spec_hash())
    if write:
        (OUTDIR / f"exp14_exp16_verdict_{verdict_tag}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k2: v for k2, v in out.items() if k2 not in ("per_seed_base", "per_seed_ext")}, indent=2))
    print(f"\n[score_exp16] band {band}x{N} loadable={loadable}  READ {n_read}  CONVERTED {k} "
          f"{out['converter_seeds']}  floor_clean={floor.get('floor_clean')}  participation={particip_status}"
          f"\n  -> TERMINAL: {partition['terminal']}  ({partition['why']})  [routes={partition['routes']}]")
    return out


# =========================================================================== positive-delta smoke
def _plant(onset, conv_run=None, band=0.6875, N=5, n_cols=60, t0=None, num_active=None,
           p1=None, tail=None, probe_tail=None, base_acc=0.30):
    """Build a synthetic run record. onset=None -> unacquired. conv_run -> a sustained >=band run of
    length >=N placed post-onset (makes _density_conversion_onset fire). num_active in [0,1] sets the
    fraction of post-onset windows with num>=0.01 (the activity fraction). p1/tail/probe_tail plant
    the gradient buckets. EVAL-spaced columns."""
    t0 = t0 if t0 is not None else EVAL
    cols = []
    onset_idx = None
    for i in range(n_cols):
        t = t0 + i * EVAL
        if onset is not None and onset_idx is None and t >= onset:
            onset_idx = i
        post = onset is not None and t >= onset
        # activity: post-onset windows are "active" (num>=0.01) at rate num_active
        if post and num_active is not None:
            k_post = i - onset_idx
            num = 0.05 if ((k_post % 100) < int(round(num_active * 100))) else 0.0
        else:
            num = 0.05 if (onset is not None and t >= onset) else 0.0
        acc = base_acc
        if post and conv_run is not None:
            cstart, clen = conv_run
            if cstart <= (i - onset_idx) < cstart + clen:
                acc = band + 0.02                       # sustained above band
        col = dict(t=t, num=num, exam_acc=acc, exam_n=4)
        if post and p1 is not None:
            col["pos_err_word"] = {X16_GRAD_P1: p1, **({X16_GRAD_TAIL: tail} if (tail is not None and probe_tail is None) else {})}
        if post and probe_tail is not None:
            col["probe_pos_err_word"] = {X16_GRAD_TAIL: probe_tail}
        cols.append(col)
    return dict(arm=X16_ARM, seed=0, acquisition_onset=onset, columns=cols)


def smoke() -> None:
    """Positive-delta smoke (canon §10.25.1 — each assert FAILS under a no-op / wrong route). Jason's
    matrix: {0,3,5} count × participation {alive,dead}; plus the two branch additions (AMD-12):
    cal-converts-SHIFTED demotion, and EXT-fire under D1 (substitution-first + the n>=8 floor)."""
    B, N = 0.6875, 5
    ok = 0

    # sc-G4-af: activity fraction separates live from inert (POSITIVE-DELTA: a no-op returning a
    # constant fails). Live plant ~0.8 active; inert plant 0.0 active.
    live = _plant(onset=EVAL, num_active=0.80, n_cols=80)
    inert = _plant(onset=EVAL, num_active=0.00, n_cols=80)
    af_live, af_inert = _activity_fraction(live), _activity_fraction(inert)
    assert af_live is not None and af_live > 0.5 and af_inert == 0.0, f"sc-G4-af {af_live}/{af_inert}"
    assert _activity_fraction(_plant(onset=None)) is None, "sc-G4-af unacquired must be None"
    print(f"SMOKE sc-G4-af: activity fraction live={af_live:.3f} vs inert={af_inert:.3f} (separates)"); ok += 1

    # sc-G4-part: participation gate — ALIVE (>=bar) / STARVED (acquired, <bar) / DEAD (unacquired)
    alive_recs = {s: _plant(onset=EVAL, num_active=0.80) for s in range(5)}
    starv_recs = {s: _plant(onset=EVAL, num_active=0.02) for s in range(5)}   # ~0.02 < bar 0.065
    dead_recs = {s: _plant(onset=None) for s in range(5)}
    assert _participation_gate(alive_recs)["status"] == "ALIVE", "sc-G4-part ALIVE"
    assert _participation_gate(starv_recs)["status"] == "STARVED", "sc-G4-part STARVED"
    assert _participation_gate(dead_recs)["status"] == "DEAD", "sc-G4-part DEAD"
    # BUG-C positive-delta (review MAJOR): 4/5 acquired with healthy activity is ALIVE, not DEAD
    # (Gate 1 == any-acquired, not all-acquired). FAILS under the pre-fix all() coding.
    partial = {s: _plant(onset=EVAL, num_active=0.80) for s in range(4)}
    partial[4] = _plant(onset=None)
    assert _participation_gate(partial)["status"] == "ALIVE", "sc-G4-part 4/5-acquired must be ALIVE (any, not all)"
    print("SMOKE sc-G4-part: participation ALIVE / STARVED / DEAD fire; 4/5-acquired -> ALIVE (any-not-all)"); ok += 1

    # sc-G4-grad: gradient positive-delta — a real gradient (p1>tail) gives delta>0; flat gives ~0.
    g_real = _recency_gradient(_plant(onset=EVAL, p1=0.69, probe_tail=0.55))
    g_flat = _recency_gradient(_plant(onset=EVAL, p1=0.55, probe_tail=0.55))
    assert g_real["delta"] is not None and g_real["delta"] > 0.1, f"sc-G4-grad real {g_real}"
    assert abs(g_flat["delta"]) < 1e-6, f"sc-G4-grad flat {g_flat}"
    assert g_real["tail_from_probe"], "sc-G4-grad tail must come from the probe on X"
    print(f"SMOKE sc-G4-grad: gradient real Δ={g_real['delta']} vs flat Δ={g_flat['delta']}"); ok += 1

    # sc-G6-grid: the {0,3,5} × {alive,dead} partition grid ------------------------------------
    def base_of(k_conv, n_read=8):
        b = {}
        for s in range(8):
            if s < n_read and s < k_conv:
                b[s] = dict(status="READ", converted=True, acquisition_onset=EVAL, conversion_onset=EVAL * 3)
            elif s < n_read:
                b[s] = dict(status="READ", converted=False, acquisition_onset=EVAL, conversion_onset=None)
            else:
                b[s] = dict(status="UNREAD(unacquired)", converted=False, acquisition_onset=None, conversion_onset=None)
        return b
    # k=5, alive, floor-clean, loadable, n=8 -> WORD-SIDE CAPTURE
    r5 = _ext_resolve(base_of(5), {})
    assert _partition(r5["k"], r5["n_read"], True, "ALIVE", True)["terminal"] == "WORD-SIDE CAPTURE", "sc-G6 k5"
    # k=0, alive -> VISION-SIDE MASSING; k=0, dead/starved -> DOSE-STARVATION-CONFOUNDED
    r0 = _ext_resolve(base_of(0), {})
    assert _partition(r0["k"], r0["n_read"], True, "ALIVE", True)["terminal"] == "VISION-SIDE MASSING", "sc-G6 k0 alive"
    assert _partition(r0["k"], r0["n_read"], True, "STARVED", True)["terminal"] == "DOSE-STARVATION-CONFOUNDED", "sc-G6 k0 starv"
    assert _partition(r0["k"], r0["n_read"], True, "DEAD", True)["terminal"] == "DOSE-STARVATION-CONFOUNDED", "sc-G6 k0 dead"
    # k=3 -> EXT fires; with EXT bringing 2 more converters+read to k=5,n=10 -> WORD-SIDE
    assert _ext_resolve(base_of(3), {})["fired"], "sc-G6 k3 must fire EXT"
    print("SMOKE sc-G6-grid: {0,3,5}×{alive,dead} terminals (WORD-SIDE / VISION-SIDE / DOSE-STARV) all correct"); ok += 1

    # sc-G6-shift: cal-converts-SHIFTED demotes the primary to DIRECTION-ONLY (POSITIVE-DELTA: a
    # loadable=True no-op would wrongly certify). Even k=5/alive/floor-clean must demote when SHIFTED.
    shifted = _partition(5, 8, True, "ALIVE", loadable=False)
    assert shifted["terminal"] == "DIRECTION-ONLY" and shifted["routes"], f"sc-G6-shift {shifted}"
    assert _partition(5, 8, True, "ALIVE", loadable=True)["terminal"] == "WORD-SIDE CAPTURE", "sc-G6-shift control"
    # borrow-gate itself: a shifted between-episode pool is rejected, a matched one borrows
    donor_band = (0.6111, 4)
    donor_null = [0.30] * 400
    matched = [0.30] * 400
    shifted_pool = [0.62] * 400
    assert XA._borrow_gate(donor_band, donor_null, matched)["borrow_ok"], "sc-G6-shift borrow matched"
    assert not XA._borrow_gate(donor_band, donor_null, shifted_pool)["borrow_ok"], "sc-G6-shift borrow shifted"
    print("SMOKE sc-G6-shift: cal-converts SHIFTED -> DIRECTION-ONLY demotion (vs loadable control)"); ok += 1

    # sc-G6-ext: D1 EXT — substitution-first + the n>=8 certifiability floor -----------------
    # base has 2 UNREAD (n_read_base=6), k=3; EXT {8,9} both READ -> 2 substitute -> n_read=8
    base6 = base_of(3, n_read=6)
    ext_both_read = {8: dict(status="READ", converted=False, acquisition_onset=EVAL, conversion_onset=None),
                     9: dict(status="READ", converted=True, acquisition_onset=EVAL, conversion_onset=EVAL * 3)}
    e = _ext_resolve(base6, ext_both_read)
    assert e["fired"] and e["n_read"] == 8 and e["substituted"] == 2 and e["extended"] == 0, f"sc-G6-ext sub {e}"
    # exhaustion: base 2 UNREAD, only 1 EXT READ -> n_read=7 < 8 -> UNDERPOWERED
    ext_one_read = {8: dict(status="READ", converted=False, acquisition_onset=EVAL, conversion_onset=None),
                    9: dict(status="UNREAD(unacquired)", converted=False, acquisition_onset=None, conversion_onset=None)}
    e2 = _ext_resolve(base6, ext_one_read)
    assert e2["n_read"] == 7, f"sc-G6-ext exhaust n {e2}"
    assert _partition(e2["k"], e2["n_read"], True, "ALIVE", True)["terminal"] == "UNDERPOWERED", "sc-G6-ext exhaust->UNDERPOWERED"
    # count-extension: base all 8 READ, k=4 -> EXT extends; 1 EXT converter -> k=5,n=10 -> WORD-SIDE
    base8k4 = base_of(4, n_read=8)
    ext_ext = {8: dict(status="READ", converted=True, acquisition_onset=EVAL, conversion_onset=EVAL * 3),
               9: dict(status="READ", converted=False, acquisition_onset=EVAL, conversion_onset=None)}
    e3 = _ext_resolve(base8k4, ext_ext)
    assert e3["fired"] and e3["substituted"] == 0 and e3["extended"] == 2 and e3["k"] == 5 and e3["n_read"] == 10, f"sc-G6-ext extend {e3}"
    assert _partition(e3["k"], e3["n_read"], True, "ALIVE", True)["terminal"] == "WORD-SIDE CAPTURE", "sc-G6-ext extend->WORD-SIDE"
    # BUG-D positive-delta (review MAJOR): when EXT does NOT fire (base all READ, k>=5), read_seeds
    # excludes EXT -> the floor-audit population matches the counted cell. FAILS if read_seeds ever
    # unconditionally admitted READ EXT seeds.
    nf = _ext_resolve(base_of(5, n_read=8), ext_ext)
    assert (not nf["fired"]) and 8 not in nf["read_seeds"] and 9 not in nf["read_seeds"] and nf["n_read"] == 8, f"sc-G6-ext no-fire {nf}"
    print("SMOKE sc-G6-ext: D1 substitution-first, n>=8 floor->UNDERPOWERED, extend->WORD-SIDE, no-fire excludes EXT"); ok += 1

    # sc-G6-flooraudit: the REAL _floor_audit (not a literal) — the coverage gap the review flagged.
    # (a) k=0 READ set + benign null -> floor_clean=True -> VISION-SIDE. THE positive-delta that FAILS
    #     under the pre-fix bug (observed=[] gave _poisson_binomial_ge(ps,0)=1.0 -> NOT-CERTIFIABLE).
    cal_benign = {s: [0.30] * 300 for s in range(5)}
    zero_read = {s: _plant(onset=EVAL, conv_run=None, base_acc=0.30, n_cols=60) for s in range(8)}
    fa0 = _floor_audit(zero_read, B, N, cal_benign)
    assert fa0["floor_clean"] is True and fa0["observed_converters"] == 0, f"sc-G6-flooraudit k0 {fa0}"
    assert _partition(0, 8, fa0["floor_clean"], "ALIVE", True)["terminal"] == "VISION-SIDE MASSING", "sc-G6-flooraudit k0->VISION"
    assert _partition(0, 8, fa0["floor_clean"], "DEAD", True)["terminal"] == "DOSE-STARVATION-CONFOUNDED", "sc-G6-flooraudit k0 DEAD"
    # (b) phantom converters (bare-N runs) vs a crossing-rich null -> floor_clean=False (FAILS return-True no-op)
    cal_phantom = {0: ([0.70] * 5 + [0.30] * 5) * 25}
    phantom = {s: _plant(onset=EVAL, conv_run=(2, 5), band=B, N=N, base_acc=0.30, n_cols=60) for s in range(5)}
    fa1 = _floor_audit(phantom, B, N, cal_phantom)
    assert fa1["observed_converters"] == 5 and fa1["floor_clean"] is False, f"sc-G6-flooraudit phantom {fa1}"
    assert _partition(5, 8, fa1["floor_clean"], "ALIVE", True)["terminal"] == "NOT-CERTIFIABLE", "sc-G6-flooraudit phantom->NOT-CERT"
    # (c) strong long-episode converters vs benign null -> above floor -> WORD-SIDE
    strong = {s: _plant(onset=EVAL, conv_run=(2, 40), band=B, N=N, base_acc=0.30, n_cols=60) for s in range(5)}
    fa2 = _floor_audit(strong, B, N, cal_benign)
    assert fa2["observed_converters"] == 5 and fa2["floor_clean"] is True, f"sc-G6-flooraudit strong {fa2}"
    assert _partition(5, 8, fa2["floor_clean"], "ALIVE", True)["terminal"] == "WORD-SIDE CAPTURE", "sc-G6-flooraudit strong->WORD-SIDE"
    print("SMOKE sc-G6-flooraudit: REAL _floor_audit — k0->clean->VISION, phantom->AT-FLOOR->NOT-CERT, strong->clean->WORD-SIDE"); ok += 1

    # sc-G6-fisher: Fisher companion reproduces the prereg values vs A's 0/8
    fish = {(5, 8): 0.0128, (5, 9): 0.0204, (5, 10): 0.0294, (3, 8): 0.100, (4, 9): 0.0529, (4, 10): 0.0686}
    for (k, n), exp in fish.items():
        got = XA._fisher_one_sided(k, n - k, 0, 8)
        assert abs(got - exp) < 5e-4, f"sc-G6-fisher {k}/{n}: {got} vs {exp}"
    print("SMOKE sc-G6-fisher: exact Fisher companions {5/8..4/10} reproduce prereg to 4dp"); ok += 1

    # sc-anchor: activity-fraction reader on committed A-arm exp12_dwell {0-7} reproduces the
    # ratified anchor (range within [0.223,0.878], median ~0.776). Ties the bar to committed data.
    a_afs = []
    for s in range(8):
        p = _rec_path(s, "verdict", arm="exp12_dwell")
        if p.exists():
            a_afs.append(_activity_fraction(XA._truncate(json.loads(p.read_text()), X16_PRIMARY_AT)))
    a_afs = [x for x in a_afs if x is not None]
    if len(a_afs) == 8:
        med = statistics.median(a_afs)
        assert 0.70 <= med <= 0.85, f"sc-anchor A-arm median {med} not ~0.776"
        assert min(a_afs) >= 0.15 and max(a_afs) <= 0.95, f"sc-anchor A-arm range {min(a_afs)}-{max(a_afs)}"
        print(f"SMOKE sc-anchor: A-arm activity-fraction reproduces anchor (median {med:.3f}, "
              f"range [{min(a_afs):.3f},{max(a_afs):.3f}]) vs ratified 0.776 [0.223,0.878]"); ok += 1
    else:
        print(f"SMOKE sc-anchor: SKIPPED — only {len(a_afs)}/8 committed A-arm verdict records present")

    print(f"\nexp16_score smoke: {ok} checks PASS")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cal-read", action="store_true", help="G4: cal read (band/liveness/participation/gradient)")
    ap.add_argument("--cal-tag", type=str, default="exp16cal")
    ap.add_argument("--score", action="store_true", help="G6: §4-partition DRAFT (guarded)")
    ap.add_argument("--verdict-tag", type=str, default="exp16verdict")
    ap.add_argument("--release", action="store_true", help="override the verdict-withhold guard")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        smoke()
    elif args.cal_read:
        cal_read_exp16(cal_tag=args.cal_tag)
    elif args.score:
        if not args.release:
            print("EXP16 VERDICT WITHHELD (build-not-run). score_exp16 is BUILT; pass --release after "
                  "the {0-7} runs exist and the cal read is surfaced.")
        else:
            score_exp16(verdict_tag=args.verdict_tag, write=not args.dry)
