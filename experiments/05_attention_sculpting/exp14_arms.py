"""EXP14 — CONVERSION DYNAMICS (horizon-extension arm).

Pre-registration: docs/EXP14_CONVERSION_DYNAMICS_PREREG.md (FINALIZED, fork (i) screen-first,
panel-folded 2026-07-07). Forward axis of EXP13 fork (a): does the operator LEAVE THE MARGINAL
(conversion) in a healthy existing regime at long horizon, and what orders it — horizon / dose /
seed? Split s0 is the sole existence proof (coin/shuffled, converted late).

ONE CODE PATH (discipline §0): the DYNAMICS (step/losses/optimizer in EXP12Loop/Stage0Loop) are
reused VERBATIM. `run_exp14_arm` REPLICATES `exp12_arms.run_exp12_arm`'s runner body in exact
read order (the interleaved dc_track/grad_geometry_split/eval reads couple into the near-floor
trajectory, §10.21.4 — a bare step-loop would diverge), adding ONLY: (a) fabric pre-built at
`h_max` (one fixed shuffled perm so the coin rung is faithfully extendable — panel F1), (b) read
+ `.pt` checkpoint at `read_at` and at the online conversion-onset trigger (the checkpoint
contract, PROJECT_STATE §12.E), (c) the density-matched conversion read (post-hoc). No new loss,
no new force. Faithfulness is PROVEN, not asserted: `smoke()` requires run_exp14_arm at a matched
horizon to reproduce run_exp12_arm's columns DIGIT-IDENTICALLY.

Screen rungs (fork (i)): scheduled = exp12_dwell (dwelled), coin = exp12_split (shuffled, s0
lineage). Cal seeds {20-24} != verdict {0-7}.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp07_config as C                                        # noqa: E402
import exp08_arms as A                                         # noqa: E402
import exp09_arms as X9                                        # noqa: E402
import exp10_arms as X10                                       # noqa: E402
import exp12_arms as X12                                       # noqa: E402
import exp12_fabric as F                                       # noqa: E402
from revival import dynamics_panel                             # noqa: E402

OUTDIR = X12.OUTDIR
EVAL, BLOCK = X12.EVAL, X12.BLOCK

# --- fork (i) screen rungs (prereg §3) ---
RUNGS = {"scheduled": "exp12_dwell", "coin": "exp12_split"}

# --- 2x2 conversion-deconfound CELLS (EXP14_2x2_DECONFOUND_PREREG §2) -----------------------
# The FABRIC x DOSE factorial. A,D reuse the screen's committed cal/verdict runs; B,C are new.
# Per-cell cal_tag: reused cells read the screen cal ("cal"); new cells cut fresh ("cal2").
CELLS = {
    "A_dwell":    dict(arm="exp12_dwell",    fabric="dwelled",  dose="scheduled",
                       cal_tag="cal",  reused=True),   # double-negative baseline (screen 0/8)
    "B_12bc_dwp": dict(arm="exp12_12bc_dwp", fabric="dwelled",  dose="coin",
                       cal_tag="cal2", reused=False),  # DOSE-only carrier (NEW; liveness-gated)
    "C_shuffle":  dict(arm="exp12_shuffle",  fabric="shuffled", dose="scheduled",
                       cal_tag="cal2", reused=False),  # FABRIC-only carrier (NEW)
    "D_split":    dict(arm="exp12_split",    fabric="shuffled", dose="coin",
                       cal_tag="cal",  reused=True),   # the corner (screen 4/8 +cal s20)
}
NEW_ARMS = ["exp12_shuffle", "exp12_12bc_dwp"]   # step-1 pre-check + step-2 fresh cal

CAL_SEEDS = [20, 21, 22, 24, 25]   # s23 -> s25 swap (Jason 2026-07-07): under the T-independent
#                                    fabric-independence bar (instrument re-pin), s23 GENUINELY
#                                    exceeds (per-lag nuisance 0.1346 > 0.1344 at every horizon) =
#                                    a real seed defect -> "swap, don't tune"; s25 clears cleanly.
VERDICT_SEEDS = list(range(8))
EXT_POOL = [8, 9]

# --- horizons (prereg §5; panel F1) ---
READ_AT = 500_000
H_MAX = 1_000_000

# --- online conversion-onset TRIGGER (checkpoint placement ONLY; never the verdict) (§6) ---
PROPOSED_BAND, PROPOSED_CONSEC = 0.6, 2

# --- density-matched band + cell constants (prereg §4/§7; cut/pinned at stage-two) ---
ALPHA = 1e-3                       # target pre-conversion false-conversion rate
N_NULL_MIN = 200                   # min pooled post-acq pre-conversion windows (panel F3)
S0_LEVEL, S0_N = 0.704, 16         # committed s0 anchor (FRONTIER §10.20.1); band must admit it
EPISODE_BAND, EPISODE_MIN = S0_LEVEL, 8    # honest-null episode-exclusion (band re-pin, Jason 2026-07-07)
COUNT_CUTS = dict(across_seeds=5, lottery=(1, 2), none=0, ambiguous=(3, 4))  # per 8 (panel F4)
N_MIN_READ = 3                     # READ-floor (panel F5; EXP12 §13.9 pin ii)
MIN_CONV_BUDGET = 130_000          # F6 budget gate: min post-acq conversion-onset budget on the
#                                    reference converter (split, ~130k). A READ seed with
#                                    (READ_AT - acquisition_onset) < this = UNREAD(budget-truncated)
#                                    — re-derived from D's reused split verdict runs at verdict.

# --- Ruling B (Jason 2026-07-08): a cell whose OWN cal seeds convert has no clean marginal null.
# Only C_shuffle is broken (A/B/D self-calibrate: A 5/5, B 5/5, D 4/5 clean cal seeds). C borrows
# the density-matched A_dwell marginal (both scheduled) IFF the borrow-validity gate passes; else
# it uses its OWN between-episode null. Gate: A's provisional band must control the false-rate on
# C's between-episode (non-converting) windows within BORROW_ALPHA_MULT x ALPHA — else the fabric
# has MOVED the baseline (a weaker finding than "enables conversion") and A is not C's null. ---
CONV_LOW, CONV_MIN = PROPOSED_BAND, EPISODE_MIN   # between-episode exclusion: sustained >=0.6 x >=8
BORROW_ALPHA_MULT = 2.0            # borrow valid iff fr(A_band on C_between) <= 2*ALPHA (density-matched)
BORROW_CELL, BORROW_FROM = "C_shuffle", "A_dwell"

# =============================================================================================
# EXP15 — DURABILITY BY DOSE (docs/EXP15_DURABILITY_BY_DOSE_PREREG.md; ratified Jason 2026-07-10)
# ---------------------------------------------------------------------------------------------
# SCORING-ONLY constants. These MUST NOT enter C.spec_hash()'s payload: the runs are
# `run_exp14_arm` VERBATIM, so a reused EXP14 run and a fresh EXP15 run must carry the SAME
# run-level spec_hash (41d6f0d5e7da) or the F2 parity assert breaks by construction. Hashed
# separately by exp15_spec_hash() for provenance on the durability artifacts.
# =============================================================================================
X15_RULER_BAND, X15_RULER_N = 0.6875, 5   # COMMON RULER, both cells: converter classification
X15_T_DUR = 200_000                # runway censoring: converter w/ < T_DUR post-onset runway =
#                                    DUR-CENSORED (reported, out of primary, NEVER "decayed").
#                                    RULING 1 re-scope: T_DUR now ALSO guards the OPPOSITE confound
#                                    — a late converter trivially populates the final quartile.
X15_CELLS = ["C_shuffle", "D_split"]          # within-shuffled contrast only
X15_CONV_FLOOR = 12                           # A1: eligible converters required per cell
X15_RESERVE_POOL = [40, 41, 42, 43, 44, 45, 46, 47]   # paired top-up, by rule only, cap +8/cell
X15_RESERVE_CAP = 8
X15_H_MAX = 1_000_000              # A2: new seeds run to 1M unconditionally...
X15_PRIMARY_AT = 500_000           # ...but the PRIMARY is frozen at 500k on ALL seeds
X15_ALPHA_P = 0.05

# --- RULING 2 (Jason 2026-07-10): seed-pool repair. -------------------------------------------
# The ratified {8-27} re-admitted the EXP14 cal seeds {20,21,22,24,25}. Concrete, not theoretical:
# C's cal2 ran at h_max=1M, so re-running those seeds would be BIT-IDENTICAL REPLAYS of the runs
# that cut C's band. New pool is cal-disjoint, s23-free, reserve-disjoint.
X15_NEW_SEEDS = list(range(8, 20)) + list(range(28, 36))   # {8-19} u {28-35} = 20/cell
X15_SUBST_POOL = [36, 37, 38, 39]             # pre-check substitution, lowest-unused-first
X15_PRECHECKED_CARRY = [28]                   # s28 passed pre-check as the s23 replacement

# --- RULING 1 (Jason 2026-07-10): locked-state sustain RETIRED; primary re-posed. --------------
# FINDING (recorded, prereg §6): LOCKED-STATE SUSTAIN DOES NOT EXIST AT 500k IN THIS REGIME.
# `mean(last K=10) >= band` returns 0/16 on the committed verdict seeds, and NO bar both controls
# alpha and produces sustainers (the alpha-calibrated K=10 bar is 0.79, HIGHER than the ruler).
# It is the WRONG CATEGORY: conversion here is EPISODIC (verified: 2-27 recurring episodes per
# committed converter at the ruler, median 9; 2-23 at each cell's own band. NOT '8-23' -- the
# ruling text's lower bound does not reproduce; see the prereg fact-check note),
# so "held above band at horizon" measures a state the phenomenon does not occupy.
#
# RE-POSED PRIMARY: exact Mann-Whitney one-sided (D > C) on FINAL-QUARTILE TIME-ABOVE-BAND =
# fraction of eval windows in (375k, 500k] with exam_acc >= the common ruler, among ELIGIBLE
# converters, NEW SEEDS ONLY.
#   * already a REGISTERED §7 companion (named before any peek);
#   * continuous -> no threshold to alpha-calibrate (the null is between-cell EXCHANGEABILITY);
#   * operationalizes durability for an EPISODIC phenomenon (does the regime persist late);
#   * new-seeds-only QUARANTINES every disclosed peek (CC's MW on last-10 means; Jason's
#     verification computations). The committed 16 are CONTEXT/SENSITIVITY, never primary.
X15_FINAL_Q_FROM = 375_000         # primary window is (X15_FINAL_Q_FROM, X15_PRIMARY_AT]
X15_PRIMARY_SCOPE = "new_seeds_only"
X15_K_LAST = 10                    # RETIRED as primary (Ruling 1). Kept for the SENSITIVITY only.

# --- RULING 3 (Jason 2026-07-10): converter definition UNCHANGED; pool protected by a -----------
# PRECEDENTED gate, not a new constant. Converter classification stays >=5-consec->=ruler (keeps
# comparability with §10.24 and the §5a reproduction check). DURABILITY-POOL eligibility
# additionally requires longest-run >= EPISODE_MIN (=8, the existing s0-class house constant):
# set-preserving on committed data (census: converters start at 21) and it structurally excludes
# bare-N phantoms when the tails get sampled 5x harder.
X15_DUR_MIN_RUN = EPISODE_MIN      # =8; durability-pool eligibility (NOT a new constant)

# EXP14 per-cell bands, retained ONLY for the reproduction check (prereg §5a):
X15_REPRO = {"C_shuffle": dict(band=0.64, N=5, converters=[0, 2, 4, 5, 6]),
             "D_split":   dict(band=0.6875, N=5, converters=[0, 1, 3, 6])}

PANEL_KEYS = ("num", "den", "ratio", "proto", "d2_depth", "d2_spread",
              "asg_dist", "asg_argmax_k", "asg_entropy", "asg_cat",
              "exam_lift", "exam_acc", "mid_word_lift", "mid_vis_err",
              "div_bg", "div_id", "div_nuis")


# ------------------------------------------------------------------ checkpoint (contract §12.E)
@torch.no_grad()
def save_checkpoint(loop, path: Path, **meta) -> None:
    """End-state `.pt` — trajectory-inert (no RNG draw, no param touch). Sufficient to
    re-probe the operator READ-ONLY (the exact thing the §10.21.6 retro probe could not do)
    and to resume (faithful on the pre-built h_max fabric — panel F1)."""
    ckpt = dict(
        vision=loop.vision.state_dict(), word=loop.word.state_dict(),
        op=loop.op.state_dict(), opt=loop.opt.state_dict(),
        gen_state=loop.gen.get_state(), t=loop._t,
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), **meta)
    torch.save(ckpt, path)


# ------------------------------------------------------------------ the runner (faithful replica)
def run_exp14_arm(arm_name: str, seed: int, *, read_at: int = READ_AT, h_max: int | None = None,
                  probe_rate: float = X12.PROBE_RATE_STAGE1, out_tag: str | None = None,
                  checkpoint: bool = True, mid_ckpt_at: int | None = None) -> dict:
    """Faithful replica of exp12_arms.run_exp12_arm (verified digit-identical in smoke), with
    the fabric pre-built at `h_max` and reads/checkpoints at `read_at`.

    `mid_ckpt_at` (EXP15 A2): drop an EXTRA `.pt` mid-run at step `mid_ckpt_at` without stopping.
    `save_checkpoint` is trajectory-inert (no RNG draw, no param touch), so the dynamics are
    byte-for-byte unchanged; smoke (9) asserts the run-to-2N/read-at-N prefix is digit-exact and
    that this checkpoint equals the state a read_at=N run reaches. EXP15 runs to 1M with
    mid_ckpt_at=500k so the primary can be read at 500k on every seed."""
    h_max = h_max or read_at
    assert read_at <= h_max, "read_at must be <= h_max (fabric is pre-built to h_max)"
    assert mid_ckpt_at is None or 0 < mid_ckpt_at <= read_at, \
        f"mid_ckpt_at {mid_ckpt_at} must lie in (0, read_at={read_at}]"
    loop, spec, cfg = X12.build_exp12(arm_name, seed, h_max, probe_rate)   # fabric -> h_max+8
    fab = loop.stream

    OUTDIR.mkdir(exist_ok=True)
    # asserts on the UNSHUFFLED wave order (identical multiset by construction)
    if fab.shuffled:
        fab_plain = F.build_fabric(loop.stim, cfg, seed, fab.T, probe_rate=probe_rate,
                                   shuffled=False,
                                   uniform_mask=spec.get("uniform_mask", False),
                                   word_ref=spec.get("word_ref", False))
        assert torch.equal(fab.raw.sort(0).values, fab_plain.raw.sort(0).values), \
            "A-SHUFFLE waves are not the identical multiset"
        assert int(fab.is_exam.sum()) == int(fab_plain.is_exam.sum()), "exam count differs"
        asserts = F.fabric_asserts(fab_plain, cfg)
    else:
        asserts = F.fabric_asserts(fab, cfg)
    man = F.fabric_manifest(fab, loop.stim, cfg, asserts)
    man.update(arm=arm_name, seed=seed, read_at=read_at, h_max=h_max, vocab=cfg.n_category,
               exp="exp14_conversion_dynamics",
               geometry="wave-local (W=1); no u-carrier; L_JEPA inert by construction",
               members=A._members(cfg),
               anchor=dict(embeddings=[[round(float(x), 6) for x in r]
                                       for r in loop.word.emit(torch.arange(cfg.n_category))],
                           construction="WordCortex(D, n_category, seed=seed+1) — deployed v2"))
    base = OUTDIR / (f"exp14_{arm_name}_s{seed}" + (f"_{out_tag}" if out_tag else ""))
    base.with_suffix(".manifest.json").write_text(json.dumps(man, indent=2, default=str))
    try:
        A.render_scatter(loop, base.with_suffix(".scatter.png"))
    except Exception as e:                                    # illustrative-only: never blocks
        man["scatter_note"] = f"render skipped: {e}"

    members_a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    members_b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    labels = loop._word_label(members_b, members_a)

    no_word = bool(spec.get("no_word", False))
    buf = X12._fresh_buf()
    cols, occ, gsplit, mixes = [], {}, {}, {}
    onset_saved = False
    for t in range(1, read_at + 1):
        # §13.10 probe read PRE-update (matched to the scheduled exam's timing)
        pl = X12._probe_exam_read(loop, t - 1) if bool(fab.is_probe_exam[t - 1]) else None
        loop.step(no_word=no_word)
        X12._buffer_wave(loop, t - 1, buf, probe_lift=pl)
        if t % EVAL == 0:
            cols.append(X12._eval_column(loop, t, buf, members_a, members_b, labels,
                                         no_word=no_word))
            buf = X12._fresh_buf()
            # online conversion-onset TRIGGER (PROPOSED band) -> checkpoint placement only
            if checkpoint and not onset_saved and _proposed_conversion(cols):
                save_checkpoint(loop, base.with_suffix(".ckpt_onset.pt"),
                                arm=arm_name, seed=seed, event="proposed_conversion_onset",
                                onset_t=cols[-1]["t"])
                onset_saved = True
        # EXP15 A2: mid-horizon checkpoint. Trajectory-inert; the loop does NOT stop.
        if checkpoint and mid_ckpt_at is not None and t == mid_ckpt_at:
            save_checkpoint(loop, base.with_suffix(".ckpt_mid.pt"),
                            arm=arm_name, seed=seed, event="mid_horizon", mid_t=t)
        if t % BLOCK == 0:
            occ[str(t)] = loop.dc_track(cfg.n_eval)
            gsplit[str(t)] = X12.grad_geometry_split(loop, no_word)
            mixes[str(t)] = loop.mix_snapshot()

    if checkpoint:
        save_checkpoint(loop, base.with_suffix(".ckpt_read.pt"),
                        arm=arm_name, seed=seed, event="read_horizon", read_at=read_at)

    ts = [c["t"] for c in cols]
    panels = {k: dynamics_panel(ts, [c.get(k) for c in cols]) for k in PANEL_KEYS}
    onset = X10.acquisition_onset(cols)                       # §13.4: num >= 0.01, 2 consec
    rec = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), exp="exp14",
        arm=arm_name, seed=seed, read_at=read_at, h_max=h_max, vocab=int(cfg.n_category),
        shuffled=bool(spec["shuffled"]), probe_rate=probe_rate,
        word_ref=bool(spec.get("word_ref", False)), no_word=no_word,
        eval_cadence=EVAL, block_cadence=BLOCK, mid_ckpt_at=mid_ckpt_at,
        torch_num_threads=torch.get_num_threads(),
        acquisition_onset=onset, dynamics_panel=panels,
        conversion_onset_PROPOSED=_proposed_conversion_onset(cols),
        columns=[{k: ((round(v, 6) if k in A._STANDING_COLS else float(f"{v:.6g}"))
                      if isinstance(v, float) else v) for k, v in c.items()}
                 for c in cols],
        occupancy=occ, grad_split=gsplit, masking_mix=mixes,
    )
    base.with_suffix(".json").write_text(json.dumps(rec, indent=2))
    print(f"exp14 {arm_name} s{seed}: onset={onset}  conv_PROPOSED={rec['conversion_onset_PROPOSED']}  "
          f"exam_acc_end={cols[-1].get('exam_acc')}  asg_cat_end={cols[-1]['asg_cat']:.4f}")
    return rec


def _proposed_conversion(cols) -> bool:
    """PROPOSED-band trigger (0.6/2 consec) — checkpoint placement ONLY, never the verdict."""
    if len(cols) < PROPOSED_CONSEC:
        return False
    tail = cols[-PROPOSED_CONSEC:]
    return all(c.get("exam_acc") is not None and c["exam_acc"] >= PROPOSED_BAND for c in tail)


def _proposed_conversion_onset(cols):
    run = 0
    for c in cols:
        run = run + 1 if (c.get("exam_acc") is not None and c["exam_acc"] >= PROPOSED_BAND) else 0
        if run >= PROPOSED_CONSEC:
            return c["t"] - (PROPOSED_CONSEC - 1) * EVAL
    return None


# ------------------------------------------------------------------ step-1 fabric pre-check (§7.1)
def _assert_one(arm: str, seed: int, T: int) -> dict:
    """Build the fabric at T and run the T-independent fabric-asserts (the §10.22 re-pin) —
    OUTCOME-BLIND: pure fabric construction + independence asserts, NO loop step, NO dynamics,
    NO exam/conversion read. Runs the assert on the UNSHUFFLED wave order (for a shuffled arm,
    rebuild the unshuffled twin and checksum the multiset — the exact path in run_exp14_arm).
    T>=15k so the fixed n_sample=12000 window is fully populated (the assert reads min(T,12000),
    so T=15k == the 500k run's assert bit-for-bit)."""
    try:
        loop, spec, cfg = X12.build_exp12(arm, seed, T)          # fabric -> T+8; no stepping
        fab = loop.stream
        if fab.shuffled:
            fab_plain = F.build_fabric(loop.stim, cfg, seed, fab.T,
                                       probe_rate=X12.PROBE_RATE_STAGE1, shuffled=False,
                                       uniform_mask=spec.get("uniform_mask", False),
                                       word_ref=spec.get("word_ref", False))
            assert torch.equal(fab.raw.sort(0).values, fab_plain.raw.sort(0).values), \
                "A-SHUFFLE waves are not the identical multiset"
            assert int(fab.is_exam.sum()) == int(fab_plain.is_exam.sum()), "exam count differs"
            asr = F.fabric_asserts(fab_plain, cfg)
        else:
            asr = F.fabric_asserts(fab, cfg)
        return dict(ok=True, arm=arm, seed=seed, spec_hash=C.spec_hash(),
                    perlag_nuis=asr["perlag_nuis"], k_indep=asr["k_indep"],
                    schedule_indep=asr["schedule_indep"], bg_indep=asr["bg_indep"],
                    cap_hit=asr["cap_hit"])
    except AssertionError as e:
        return dict(ok=False, arm=arm, seed=seed, spec_hash=C.spec_hash(), err=str(e))


def precheck_fabric(arm: str, seeds=None, T: int = 15_000, out_tag: str = "precheck",
                    swap_pool=None) -> dict:
    """STEP 1 (§7.1): fabric-assert the verdict seeds OUTCOME-BLIND; swap any defective from the
    EXT_POOL-then-higher pool (the ruled cal-s23->s25 substitution rule), recording each swap.

    `swap_pool` pins the substitution pool explicitly (EXP15 §3: {28-39}, lowest-unused-first,
    disjoint from the reserve {40-47}). Default preserves the EXP14 behaviour."""
    seeds = list(seeds if seeds is not None else VERDICT_SEEDS)
    if swap_pool is None:
        swap_pool = [s for s in (EXT_POOL + list(range(10, 40))) if s not in seeds]
    else:
        swap_pool = [s for s in swap_pool if s not in seeds]
    results = {s: _assert_one(arm, s, T) for s in seeds}
    accepted, swaps, used = [], [], set()
    for s in seeds:
        if results[s]["ok"]:
            accepted.append(s)
            continue
        repl = None                                              # find a clean replacement
        for cand in swap_pool:
            if cand in used or cand in accepted:
                continue
            used.add(cand)
            r = _assert_one(arm, cand, T)
            results[cand] = r
            if r["ok"]:
                repl = cand
                accepted.append(cand)
                break
        swaps.append(dict(defective=s, err=results[s].get("err"), replacement=repl))
    out = dict(arm=arm, T=T, seeds_requested=seeds, seeds_accepted=sorted(accepted),
               n_pass=sum(1 for s in seeds if results[s]["ok"]), n_total=len(seeds),
               swaps=swaps, spec_hash=C.spec_hash(),
               per_seed={str(s): results[s] for s in results})
    (OUTDIR / f"exp14_{arm}_{out_tag}.json").write_text(json.dumps(out, indent=2))
    tag = "ALL PASS" if not swaps else f"{len(swaps)} SWAP(S)"
    print(f"[precheck {arm}] {out['n_pass']}/{out['n_total']} pass ({tag}); "
          f"accepted={out['seeds_accepted']}")
    for s in seeds:
        r = results[s]
        if r["ok"]:
            print(f"    s{s}: OK  perlag obs={r['perlag_nuis']['obs']}/n99={r['perlag_nuis']['null99']}"
                  f"  k chi2={r['k_indep']['chi2']}/n99={r['k_indep']['null99']}")
        else:
            print(f"    s{s}: FAIL -> {r.get('err')}")
    for sw in swaps:
        print(f"    SWAP: s{sw['defective']} defective ({sw['err']}) -> s{sw['replacement']}")
    return out


# ------------------------------------------------------------------ stage-two band cut (§4)
def _acc_series(rec) -> list[tuple[int, float, int]]:
    """(t, exam_acc, exam_n) for windows that HAVE an exam_acc, post-acquisition-onset."""
    onset = rec["acquisition_onset"]
    if onset is None:
        return []
    out = []
    for c in rec["columns"]:
        if c["t"] >= onset and c.get("exam_acc") is not None:
            out.append((c["t"], float(c["exam_acc"]), int(c.get("exam_n", 0))))
    return out


def _honest_null(series: list[tuple[int, float, int]]) -> list[float]:
    """HONEST NULL (band re-pin, Jason's ruling 2026-07-07): keep the FULL post-acquisition
    marginal — INCLUDING its high tail — as the null, excluding ONLY windows inside a SUSTAINED
    conversion episode (>= EPISODE_MIN consecutive windows >= EPISODE_BAND = s0-class). The prior
    form excluded EVERY window >= 0.6, stripping the marginal high tail, so false_rate came out
    0.0 (artifact) and the sustained-N was cut too low (0.5625x4 -> honest false-rate 2.9% on the
    coin rung). Panel-validated (wf_9677edf3): full-null n = 6837/8252, honest band coin 0.704x16
    / sched 0.611x4, verdict coin {0,1,3,6} / sched 0/8. For the ~marginal cal seeds the
    episode-exclusion removes ~nothing; it guards against a cal seed that genuinely converts."""
    accs = [a for (_, a, _) in series]
    n = len(accs)
    in_ep = [False] * n
    i = 0
    while i < n:
        if accs[i] >= EPISODE_BAND:
            j = i
            while j < n and accs[j] >= EPISODE_BAND:
                j += 1
            if j - i >= EPISODE_MIN:                # a sustained s0-class run -> exclude
                for k in range(i, j):
                    in_ep[k] = True
            i = j
        else:
            i += 1
    return [a for a, ie in zip(accs, in_ep) if not ie]


def _joint_band_cut(null_accs: list[float]) -> tuple[float, int]:
    """Joint (band, N) cut over the post-acq pre-conversion null span (§4). Choose the LOWEST
    band that admits s0 (band <= S0_LEVEL) and the SMALLEST N (>=3) whose empirical rate of
    N-consecutive windows >= band over the null span is <= ALPHA. This keeps s0 (0.704 x 16)
    detectable while controlling the false-conversion rate — the per-window own-density p99
    alone is ABOVE s0 for the low-exam-rate coin rung (panel F2)."""
    if not null_accs:
        return (S0_LEVEL, 3)
    # candidate bands: quantiles of the null, capped at the s0 anchor so s0 stays admissible
    xs = sorted(null_accs)
    cand = sorted({round(min(S0_LEVEL, q), 4)
                   for q in (_quantile(xs, p) for p in (0.90, 0.95, 0.975, 0.99))} | {S0_LEVEL})
    for band in cand:                                        # lowest -> highest
        for N in range(3, S0_N + 1):
            if _consec_rate(null_accs, band, N) <= ALPHA and band <= S0_LEVEL and N <= S0_N:
                return (band, N)
    return (min(S0_LEVEL, cand[-1]), S0_N)


def _consec_rate(accs: list[float], band: float, N: int) -> float:
    """Fraction of length-N windows over the null series that are all >= band (empirical
    false-conversion rate of the (band, N) detector on marginal data)."""
    if len(accs) < N:
        return 0.0
    hits = sum(1 for i in range(len(accs) - N + 1)
               if all(accs[i + j] >= band for j in range(N)))
    return hits / (len(accs) - N + 1)


def _quantile(sorted_xs: list[float], p: float) -> float:
    if not sorted_xs:
        return 0.0
    i = min(len(sorted_xs) - 1, max(0, int(round(p * (len(sorted_xs) - 1)))))
    return sorted_xs[i]


def cut_conv_band(cal_seeds=None, out_tag: str = "cal") -> dict:
    """Stage-two per-rung density-matched band from the POST-ACQUISITION, PRE-CONVERSION span
    (panel F2/F3). Reports per-rung n_null; flags cal-pool widening if thin; checks the
    s0-admission anchor. SURFACED for Jason's read before any verdict interpretation (§4)."""
    cal_seeds = cal_seeds or CAL_SEEDS
    out = dict(rungs={}, count_cuts=COUNT_CUTS, n_min_read=N_MIN_READ, alpha=ALPHA,
               s0_anchor=dict(level=S0_LEVEL, n=S0_N), cal_seeds=cal_seeds)
    for rung, arm in RUNGS.items():
        null_accs, n_seed_null, onsets = [], {}, {}
        for s in cal_seeds:
            p = OUTDIR / f"exp14_{arm}_s{s}_{out_tag}.json"
            if not p.exists():
                continue
            rec = json.loads(p.read_text())
            onsets[s] = rec["acquisition_onset"]
            series = _acc_series(rec)
            accs = _honest_null(series)              # full marginal high tail; drop s0-class episodes only
            null_accs += accs
            n_seed_null[s] = len(accs)
        n_null = len(null_accs)
        band, N = _joint_band_cut(null_accs)
        s0_admitted = bool(band <= S0_LEVEL and N <= S0_N)
        out["rungs"][rung] = dict(
            arm=arm, n_null=n_null, n_null_per_seed=n_seed_null,
            acquisition_onsets=onsets,
            conv_band=round(band, 4), conv_consec=N,
            null_p99=round(_quantile(sorted(null_accs), 0.99), 4) if null_accs else None,
            null_mean=round(statistics.mean(null_accs), 4) if null_accs else None,
            widen_needed=bool(n_null < N_NULL_MIN),
            s0_admitted=s0_admitted,
            false_rate_at_cut=round(_consec_rate(null_accs, band, N), 6) if null_accs else None,
        )
    (OUTDIR / f"exp14_band_{out_tag}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


# ------------------------------------------------------------------ two-pass fixpoint null (§4 F1)
# SUPERSEDED (Ruling A, Jason 2026-07-08): the literal two-pass ratchets N on the self-thinned null
# and VIOLATES alpha on the honest (un-thinned) marginal (A/C/D fixpoints measured 1.3x-6.8x alpha;
# D fired 5/5 cal seeds where only s20 truly converts). Its protective scenario (a hidden dampened
# sub-s0 conversion inflating a band -> under-detection) did NOT materialize where it mattered (B,
# the dose-only cell, is clean at provisional). Reverted to the provisional (§10.22 honest-null) cut
# (`_provisional_cut`). `_twopass_cut` + `_episode_mask` are RETAINED (record + still used by the
# per-cal-seed converter diagnostic and the between-episode null); `_twopass_cut` is NO LONGER the
# band method. See smoke (5) for the deflation-mechanism demonstration that motivated F1.
def _episode_mask(accs: list[float], band: float, N: int) -> list[bool]:
    """Windows inside a RUN of >= N consecutive `accs` >= band (what the (band,N) detector would
    call a conversion episode). Only sustained runs are marked — isolated high blips STAY (so the
    marginal texture / honest false-rate is preserved; this is the guard against the over-stripping
    the blanket >=0.6 exclusion caused, §4)."""
    n = len(accs)
    m = [False] * n
    i = 0
    while i < n:
        if accs[i] >= band:
            j = i
            while j < n and accs[j] >= band:
                j += 1
            if j - i >= N:
                for k in range(i, j):
                    m[k] = True
            i = j
        else:
            i += 1
    return m


def _null_excluding(per_seed_accs: dict, provisional) -> tuple[list[float], dict]:
    """Pool the post-acq null across cal seeds, excluding (a) s0-class episodes
    (EPISODE_MIN=8 consec >= EPISODE_BAND=0.704 — the honest-null base) AND (b), if `provisional`
    = (band,N) is given, any run the PROVISIONAL detector would fire. Returns (pooled, per_seed_kept)."""
    pooled, kept = [], {}
    for s, accs in per_seed_accs.items():
        excl = _episode_mask(accs, EPISODE_BAND, EPISODE_MIN)     # s0-class base exclusion
        if provisional is not None:
            band, N = provisional
            pm = _episode_mask(accs, band, N)
            excl = [a or b for a, b in zip(excl, pm)]
        keep = [a for a, e in zip(accs, excl) if not e]
        pooled += keep
        kept[s] = len(keep)
    return pooled, kept


def _twopass_cut(per_seed_accs: dict, max_iters: int = 12) -> dict:
    """TWO-PASS ITERATIVE FIXPOINT NULL (panel F1). Pass 0: provisional (band,N) on the
    s0-class-excluded null. Then iterate: exclude the cal episodes the CURRENT provisional detector
    would fire, re-cut, until (band,N) is a fixpoint. Exclusion tracks the DETECTION band (not the
    fixed 0.704x8 anchor) so a sub-s0-class conversion in a cal seed (e.g. a dwelled-coin dampened
    s20) is removed from the null before it inflates the band and makes a true DOSE read as
    INTERACTION. Contractive in practice (removing high tail lowers the quantiles -> band drops or
    holds; once no new episode fires it is stable). A non-converging cycle is SURFACED, never
    silently accepted."""
    if not any(per_seed_accs.values()):
        return dict(provisional=(S0_LEVEL, 3), fixpoint=(S0_LEVEL, 3), converged=True, iters=0,
                    trace=[], final_null=[], final_kept={s: 0 for s in per_seed_accs},
                    prov_null=[], prov_kept={s: 0 for s in per_seed_accs})
    null0, kept0 = _null_excluding(per_seed_accs, None)
    prov = _joint_band_cut(null0)
    trace = [dict(iter=0, band=round(prov[0], 4), N=prov[1], n_null=len(null0), excl="s0-class")]
    cur, seen = prov, {prov}
    for it in range(1, max_iters + 1):
        nulli, kepti = _null_excluding(per_seed_accs, cur)
        nxt = _joint_band_cut(nulli)
        trace.append(dict(iter=it, band=round(nxt[0], 4), N=nxt[1], n_null=len(nulli),
                          excl=f"s0-class + provisional {round(cur[0], 4)}x{cur[1]}"))
        if nxt == cur:                                           # FIXPOINT
            return dict(provisional=prov, fixpoint=nxt, converged=True, iters=it, trace=trace,
                        final_null=nulli, final_kept=kepti, prov_null=null0, prov_kept=kept0)
        if nxt in seen:                                         # CYCLE -> surface, don't accept
            conservative = max([cur, nxt], key=lambda bn: (bn[0], bn[1]))
            ncons, kcons = _null_excluding(per_seed_accs, conservative)
            return dict(provisional=prov, fixpoint=conservative, converged=False, cycle=True,
                        iters=it, trace=trace, final_null=ncons, final_kept=kcons,
                        prov_null=null0, prov_kept=kept0)
        seen.add(nxt)
        cur = nxt
    ncons, kcons = _null_excluding(per_seed_accs, cur)          # ran out of iters -> surface
    return dict(provisional=prov, fixpoint=cur, converged=False, iters=max_iters, trace=trace,
                final_null=ncons, final_kept=kcons, prov_null=null0, prov_kept=kept0)


# ------------------------------------------------------- provisional cut + borrow gate (Rulings A/B)
def _provisional_cut(per_seed_accs: dict):
    """RULING A band method — the §10.22 honest-null cut: pool the post-acq windows across cal
    seeds, exclude ONLY s0-class episodes (>= EPISODE_MIN consec >= EPISODE_BAND), joint (band,N).
    Returns (band, N, pooled_null). Honest false-rate <= ALPHA on the true marginal (unlike the
    dropped two-pass, which ratcheted below alpha on the self-thinned null)."""
    pooled = []
    for accs in per_seed_accs.values():
        m = _episode_mask(accs, EPISODE_BAND, EPISODE_MIN)
        pooled += [a for a, e in zip(accs, m) if not e]
    (band, N) = _joint_band_cut(pooled)
    return band, N, pooled


def _between_episode_null(per_seed_accs: dict) -> list[float]:
    """RULING B — a cell's NON-CONVERTING baseline: pool post-acq windows, exclude sustained
    conversions + shoulders (>= CONV_MIN consec >= CONV_LOW). For a cell whose OWN cal seeds convert
    (C_shuffle) this is the residual marginal after removing its conversions."""
    pooled = []
    for accs in per_seed_accs.values():
        m = _episode_mask(accs, CONV_LOW, CONV_MIN)
        pooled += [a for a, e in zip(accs, m) if not e]
    return pooled


def _borrow_gate(donor_band, donor_null: list[float], cell_between: list[float]) -> dict:
    """RULING B borrow-validity gate. Is the density-matched donor (A_dwell) marginal a valid null
    for the broken cell (C_shuffle)? PASS iff the donor's provisional band controls the false-rate
    on the cell's between-episode (non-converting) windows within BORROW_ALPHA_MULT x ALPHA (the
    operational meaning of "A's marginal == C's baseline"). Reports the mean/p99 shift too.
      same  -> BORROW (dataset marginal order-invariant; C leaving A's marginal = genuine fabric conversion)
      shift -> fabric MOVED the baseline (weaker finding); C uses its own between-episode null."""
    db, dN = donor_band
    fr = _consec_rate(cell_between, db, dN)
    ok = fr <= BORROW_ALPHA_MULT * ALPHA
    dm = statistics.mean(donor_null) if donor_null else None
    cm = statistics.mean(cell_between) if cell_between else None
    return dict(
        donor=BORROW_FROM, cell=BORROW_CELL, donor_band=dict(band=round(db, 4), N=dN),
        donor_mean=round(dm, 4) if dm is not None else None,
        donor_p99=round(_quantile(sorted(donor_null), 0.99), 4) if donor_null else None,
        cell_between_mean=round(cm, 4) if cm is not None else None,
        cell_between_p99=round(_quantile(sorted(cell_between), 0.99), 4) if cell_between else None,
        cell_between_n=len(cell_between),
        mean_shift=round(cm - dm, 4) if (cm is not None and dm is not None) else None,
        fr_donorband_on_cell=round(fr, 5), alpha=ALPHA, alpha_mult=BORROW_ALPHA_MULT, borrow_ok=bool(ok),
        decision=("BORROW — marginal order-invariant; C leaving A's marginal = genuine fabric conversion"
                  if ok else
                  "SHIFTED — fabric moves the baseline (weaker finding); C uses OWN between-episode null"))


def cut_conv_band_2x2(cal_seeds=None, out_tag: str = "2x2_cal") -> dict:
    """STEP 2 band cut under RULINGS A + B (Jason 2026-07-08):
      * RULING A — band method = the PROVISIONAL (§10.22 honest-null) cut for A/B/D (the two-pass is
        DROPPED: it ratcheted N on the self-thinned null and violated alpha on the true marginal).
        D keeps its committed 0.6875x5 -> F7's D-reproduces check preserved.
      * RULING B — C_shuffle's OWN cal seeds convert (4/5 s0-class) so it has no clean marginal;
        it BORROWS the density-matched A_dwell marginal (both scheduled) IFF the borrow-gate passes,
        else uses its OWN between-episode null (fabric-moves-baseline = the weaker finding).
    Records per cell: final (band,N) + method + honest false-rate + per-cal converters (s20 explicit)
    + acquisition/liveness (B) + spec_hash parity (F2). score_2x2 NOT run (verdict withheld)."""
    cal_seeds = cal_seeds or CAL_SEEDS
    out = dict(cells={}, cal_seeds=cal_seeds, alpha=ALPHA, count_cuts=COUNT_CUTS,
               n_min_read=N_MIN_READ, s0_anchor=dict(level=S0_LEVEL, n=S0_N),
               episode_min=EPISODE_MIN, episode_band=EPISODE_BAND, n_null_min=N_NULL_MIN,
               conv_low=CONV_LOW, conv_min=CONV_MIN,
               ruling=dict(A="two-pass DROPPED -> provisional §10.22 honest-null (A/B/D; D committed, F7-preserved)",
                           B=f"{BORROW_CELL} borrows {BORROW_FROM} marginal iff borrow-gate passes, else own between-episode null"))
    # --- gather per-cell cal traces ---
    data, spec_by_cell = {}, {}
    for cell, meta in CELLS.items():
        arm, ctag = meta["arm"], meta["cal_tag"]
        per_seed_accs, onsets, acquired, h_maxes, specs = {}, {}, {}, set(), []
        for s in cal_seeds:
            p = OUTDIR / f"exp14_{arm}_s{s}_{ctag}.json"
            if not p.exists():
                onsets[s], acquired[s] = "MISSING", False
                continue
            rec = json.loads(p.read_text())
            specs.append(rec.get("spec_hash"))
            h_maxes.add(rec.get("h_max"))
            onsets[s] = rec["acquisition_onset"]
            acquired[s] = rec["acquisition_onset"] is not None
            per_seed_accs[s] = [a for (_, a, _) in _acc_series(rec)]
        spec_by_cell[cell] = sorted(set(x for x in specs if x is not None))
        data[cell] = dict(meta=meta, per_seed_accs=per_seed_accs, onsets=onsets,
                          acquired=acquired, h_maxes=sorted(h_maxes))
    # --- provisional (§10.22) cut for every cell; also the donor + broken cell's between-episode ---
    prov = {cell: _provisional_cut(d["per_seed_accs"]) for cell, d in data.items()}   # (band,N,null)
    donor_band = (prov[BORROW_FROM][0], prov[BORROW_FROM][1])
    c_between = _between_episode_null(data[BORROW_CELL]["per_seed_accs"])
    gate = _borrow_gate(donor_band, prov[BORROW_FROM][2], c_between)
    out["borrow_gate"] = gate
    # --- assign each cell's FINAL band ---
    for cell, d in data.items():
        pb, pN, pnull = prov[cell]
        if cell == BORROW_CELL and gate["borrow_ok"]:
            band, N, cell_null = donor_band[0], donor_band[1], prov[BORROW_FROM][2]
            method = f"BORROW {BORROW_FROM} marginal (borrow-gate PASS)"
            referent = (f"borrowed {BORROW_FROM} dwelled marginal -> a conversion means 'leaves the SHARED "
                        "dwelled marginal' (SAME referent as A/B/D)")
        elif cell == BORROW_CELL:
            band, N = _joint_band_cut(c_between)
            cell_null = c_between
            method = "OWN between-episode null (borrow-gate SHIFTED)"
            referent = (f"C's OWN between-episode floor, which CONTAINS the +{gate['mean_shift']} shifted "
                        "baseline (borrow-gate SHIFTED; C has NO clean marginal). fr controls false-alarms "
                        "relative to C's ELEVATED floor -> a C conversion means 'leaves C's SHIFTED baseline', "
                        "a DIFFERENT referent than A/B/D. SAME alpha, DIFFERENT null: do NOT read C's fr as "
                        "marginal-honest or as equal-guarantee to A/B/D. This referent asymmetry IS the fabric finding.")
        else:
            band, N, cell_null = pb, pN, pnull
            method = "provisional §10.22 honest-null" + (" (committed, F7-preserved)" if cell == "D_split" else "")
            referent = ("clean dwelled/coin marginal (§10.22 honest-null; this cell does NOT convert at cal) "
                        "-> a conversion means 'leaves the dwelled marginal'")
        converters = {s: bool(any(_episode_mask(accs, band, N))) for s, accs in d["per_seed_accs"].items()}
        out["cells"][cell] = dict(
            arm=d["meta"]["arm"], fabric=d["meta"]["fabric"], dose=d["meta"]["dose"],
            reused=d["meta"]["reused"], cal_tag=d["meta"]["cal_tag"], cal_h_max=d["h_maxes"],
            method=method, conv_band=round(band, 4), conv_consec=N,
            provisional_self_cut=dict(band=round(pb, 4), N=pN),   # what the cell WOULD self-cut
            n_null=len(cell_null),
            null_p99=round(_quantile(sorted(cell_null), 0.99), 4) if cell_null else None,
            null_mean=round(statistics.mean(cell_null), 4) if cell_null else None,
            false_rate_at_cut=round(_consec_rate(cell_null, band, N), 6) if cell_null else None,
            false_rate_referent=referent,                         # canon-precision (Jason 2026-07-08): SAME alpha, DIFFERENT null for C
            s0_admitted=bool(band <= S0_LEVEL and N <= S0_N), widen_needed=bool(len(cell_null) < N_NULL_MIN),
            acquisition_onsets=d["onsets"], n_acquired=sum(d["acquired"].values()), n_cal=len(cal_seeds),
            per_cal_seed_converters=converters)
    # --- 12bc_dwp acquisition-liveness (pin 2; UNREAD-never-none) ---
    b = out["cells"]["B_12bc_dwp"]
    live = b["n_acquired"] >= N_MIN_READ
    b["liveness"] = dict(n_acquired=b["n_acquired"], n_cal=b["n_cal"], n_min=N_MIN_READ, live=bool(live),
                         s20_converter=b["per_cal_seed_converters"].get(20, "MISSING"),
                         status="LIVE" if live else "UNREAD-AT-HORIZON (dose/fabric partial)")
    # --- spec_hash parity (F2) ---
    all_specs = sorted({h for hs in spec_by_cell.values() for h in hs})
    out["spec_hash_parity"] = dict(per_cell=spec_by_cell, unique=all_specs, ok=bool(len(all_specs) == 1))
    (OUTDIR / f"exp14_band_{out_tag}.json").write_text(json.dumps(out, indent=2))
    if len(all_specs) != 1:                                      # FAIL LOUD, name the divergent cell(s)
        div = {c: hs for c, hs in spec_by_cell.items() if hs and hs != [all_specs[0]]}
        raise AssertionError(f"F2 SPEC_HASH PARITY BREACH across cells: {all_specs}; divergent cells={div}")
    _print_band_2x2(out)
    return out


def _print_band_2x2(out: dict) -> None:
    print(f"\n=== 2x2 BAND CUT (Rulings A+B) — spec_hash parity "
          f"{'OK ' + out['spec_hash_parity']['unique'][0] if out['spec_hash_parity']['ok'] else 'BREACH'} ===")
    for cell, c in out["cells"].items():
        conv = [s for s, v in c["per_cal_seed_converters"].items() if v]
        print(f"\n{cell} [{c['fabric']}x{c['dose']}] {c['arm']} ({'REUSED' if c['reused'] else 'NEW'}, "
              f"tag={c['cal_tag']}, cal_h_max={c['cal_h_max']})")
        print(f"    FINAL band {c['conv_band']}x{c['conv_consec']}  [{c['method']}]  "
              f"(self-cut would be {c['provisional_self_cut']['band']}x{c['provisional_self_cut']['N']})")
        print(f"    n_null {c['n_null']}  p99={c['null_p99']}  mean={c['null_mean']}  "
              f"honest_false_rate@cut={c['false_rate_at_cut']}  s0_admitted={c['s0_admitted']}  widen={c['widen_needed']}")
        print(f"    acq_onsets={c['acquisition_onsets']}  n_acq={c['n_acquired']}/{c['n_cal']}")
        print(f"    per-cal-seed converters (final band): "
              f"{ {s: v for s, v in c['per_cal_seed_converters'].items()} }  -> fired: {conv}")
    g = out["borrow_gate"]
    print(f"\nBORROW-GATE ({g['cell']} <- {g['donor']}): {g['decision']}")
    print(f"    donor {g['donor']} mean {g['donor_mean']} p99 {g['donor_p99']} band {g['donor_band']['band']}x{g['donor_band']['N']}"
          f"  |  {g['cell']} between-ep mean {g['cell_between_mean']} p99 {g['cell_between_p99']} (n={g['cell_between_n']})")
    print(f"    mean_shift +{g['mean_shift']}  fr(donor-band on cell-between) {g['fr_donorband_on_cell']} "
          f"vs {g['alpha_mult']}xalpha={g['alpha_mult']*g['alpha']}  -> borrow_ok={g['borrow_ok']}")
    lv = out["cells"]["B_12bc_dwp"]["liveness"]
    print(f"\nB_12bc_dwp LIVENESS: {lv['status']}  (acquired {lv['n_acquired']}/{lv['n_cal']}, "
          f"n_min={lv['n_min']}); s20 converter = {lv['s20_converter']}")


# ------------------------------------------------------------------ verdict scoring (§7)
def _density_conversion_onset(rec: dict, band: float, consec: int):
    """First t where exam_acc >= band for `consec` consecutive POST-acquisition windows
    (the density-matched detector). None = acquired-but-no-conversion. Requires acquisition
    (the operator-at-chance marginal is only readable post-onset)."""
    onset = rec["acquisition_onset"]
    if onset is None:
        return None
    run = 0
    for c in rec["columns"]:
        if c["t"] < onset:
            continue
        ea = c.get("exam_acc")
        run = run + 1 if (ea is not None and ea >= band) else 0
        if run >= consec:
            return c["t"] - (consec - 1) * EVAL
    return None


def _classify_count(k: int) -> str:
    lo, hi = COUNT_CUTS["lottery"]
    alo, ahi = COUNT_CUTS["ambiguous"]
    if k >= COUNT_CUTS["across_seeds"]:
        return "across-seeds"
    if alo <= k <= ahi:
        return "AMBIGUOUS"
    if lo <= k <= hi:
        return "s0-class-lottery"
    if k == COUNT_CUTS["none"]:
        return "none"
    return "UNMAPPED"


def score_exp14(cal_tag: str = "cal", verdict_tag: str = "verdict", seeds=None) -> dict:
    """The DRAFT four-cell read (§7) — pre-gate A (READ-floor: acquired) -> pre-gate B (count
    partition) -> cell. DRAFT: any conversion goes behind the adversarial verification pass
    before the cell reaches the table. Screen-grade: dose-ordered is NAMED, never CLAIMED;
    ANY conversion in EITHER rung fires the 2x2 (§3.1 pins)."""
    seeds = seeds or VERDICT_SEEDS
    band = json.loads((OUTDIR / f"exp14_band_{cal_tag}.json").read_text())
    out = dict(cal_tag=cal_tag, verdict_tag=verdict_tag, seeds=seeds, rungs={})
    for rung, arm in RUNGS.items():
        b = band["rungs"][rung]["conv_band"]
        N = band["rungs"][rung]["conv_consec"]
        read_cutoff = READ_AT - N * EVAL          # onset past this -> window-truncated (pin i)
        per_seed = []
        for s in seeds:
            p = OUTDIR / f"exp14_{arm}_s{s}_{verdict_tag}.json"
            if not p.exists():
                per_seed.append(dict(seed=s, status="MISSING"))
                continue
            rec = json.loads(p.read_text())
            onset = rec["acquisition_onset"]
            if onset is None:
                status, conv = "UNREAD(unacquired)", None
            elif onset > read_cutoff:
                status, conv = "UNREAD(window-truncated)", None
            else:
                status = "READ"
                conv = _density_conversion_onset(rec, b, N)
            per_seed.append(dict(
                seed=s, status=status, acquisition_onset=onset,
                conversion_onset=conv, converted=bool(conv is not None),
                exam_acc_end=(rec["columns"][-1].get("exam_acc") if rec["columns"] else None)))
        read = [x for x in per_seed if x["status"] == "READ"]
        conv = [x for x in read if x["converted"]]
        if len(read) < N_MIN_READ:
            cell = f"UNREAD-AT-HORIZON (<{N_MIN_READ} READ) — horizon re-pin, NOT none"
        else:
            cell = _classify_count(len(conv))
        out["rungs"][rung] = dict(
            arm=arm, conv_band=b, conv_consec=N, band_gt_s0_admitted=bool(b <= S0_LEVEL),
            n_read=len(read), n_converted=len(conv),
            converter_seeds=[x["seed"] for x in conv], draft_cell=cell, per_seed=per_seed)
    sc, co = out["rungs"]["scheduled"], out["rungs"]["coin"]
    any_conv = (sc["n_converted"] + co["n_converted"]) > 0
    out["any_conversion"] = any_conv
    out["fires_2x2"] = any_conv                    # §3.1 pin 2: ANY conversion, either rung
    out["dose_ordered_SCREEN_GRADE"] = dict(
        scheduled_converts=sc["n_converted"], coin_converts=co["n_converted"],
        note="SCREEN-GRADE — NAMED not CLAIMED (fabric-confounded); license = fire the 2x2 only")
    out["headline"] = (
        "NO CONVERSION at 500k on either rung -> cell 'none' pending READ-floor + adversarial pass"
        if not any_conv else
        f"CONVERSION SEEN (sched {sc['n_converted']}/{sc['n_read']}, coin {co['n_converted']}/"
        f"{co['n_read']}) -> DRAFT behind the adversarial pass; fires 2x2")
    (OUTDIR / f"exp14_verdict_{verdict_tag}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: v for k, v in out.items() if k != "rungs"}, indent=2))
    for rung, r in out["rungs"].items():
        print(f"\n{rung} ({r['arm']}): band {r['conv_band']}x{r['conv_consec']}  "
              f"READ {r['n_read']}/{len(seeds)}  CONVERTED {r['n_converted']} "
              f"{r['converter_seeds']}  -> DRAFT CELL: {r['draft_cell']}")
        for x in r["per_seed"]:
            print(f"    s{x['seed']}: {x['status']}"
                  + (f"  onset={x.get('acquisition_onset')}  conv={x.get('conversion_onset')}"
                     f"  acc_end={x.get('exam_acc_end')}" if x['status'] != 'MISSING' else ""))
    return out


# ------------------------------------------------------------------ 2x2 attribution scorer (§5)
# BUILT, NOT EXERCISED until verdict release (brief scope: steps 1->2 only). The 4-cell scorer
# reads verdict runs; it is guarded in _main behind --release-verdict.
def _attribution_from_convertset(cv: set) -> dict:
    """The exhaustive + exclusive §5 table, structured on the corner D then B/C. `cv` = the set of
    converting cell letters among {A,B,C,D} (post READ/budget/liveness gates)."""
    A_, B_, C_, D_ = ("A" in cv), ("B" in cv), ("C" in cv), ("D" in cv)
    if A_:
        return dict(attribution="ANOMALY",
                    note="double-negative A converted; baseline (screen dwell 0/8) contradicted "
                         "-> Fork-1.5-style audit, do NOT force an attribution")
    if not D_:
        return dict(attribution="INSTRUMENT_REGRESSION",
                    note="D (reused committed split) MUST reproduce {0,1,3,6}; D-silent => the "
                         "generalized scorer/band diverged from the screen -> fix pipeline, NOT a "
                         "regime finding (F7)")
    if not B_ and not C_:
        return dict(attribution="INTERACTION",
                    note="corner-only (screen prior); needs BOTH coin dose AND shuffled fabric")
    if B_ and not C_:
        return dict(attribution="DOSE_MAIN_EFFECT",
                    note="coin enables on either fabric; shuffled-scheduled (C) alone insufficient")
    if C_ and not B_:
        return dict(attribution="FABRIC_MAIN_EFFECT",
                    note="shuffled enables at either dose; dwelled-coin (B) alone insufficient")
    return dict(attribution="BOTH_MAIN_EFFECTS_ADDITIVE",
                note="dose AND fabric each independently enable; double-negative A silent; no "
                     "interaction (F3)")


def _stability_of_seed(rec: dict, band: float, N: int) -> dict:
    """STABILITY COMPANION (prereg §3): for a converting seed, the LONGEST sustained-episode length
    (>= N consec >= band), its within-episode mean, the endpoint exam_acc, and whether the episode
    SUSTAINS TO THE HORIZON (endpoint window >= band) vs decays. Post-acquisition windows only."""
    onset = rec["acquisition_onset"]
    vals = [c["exam_acc"] for c in rec["columns"]
            if onset is not None and c["t"] >= onset and c.get("exam_acc") is not None]
    n, i, longest, longest_mean = len(vals), 0, 0, None
    while i < n:
        if vals[i] >= band:
            j = i
            while j < n and vals[j] >= band:
                j += 1
            if j - i >= N and (j - i) > longest:
                longest, longest_mean = j - i, sum(vals[i:j]) / (j - i)
            i = j
        else:
            i += 1
    endpoint = vals[-1] if vals else None
    return dict(longest_episode=longest,
                within_episode_mean=round(longest_mean, 4) if longest_mean is not None else None,
                endpoint_acc=round(endpoint, 4) if endpoint is not None else None,
                sustains_to_horizon=bool(endpoint is not None and endpoint >= band))


# ------------------------------------------------------------ EXP15 §5a: coded reproduction check
def reproduction_check(verdict_tag: str = "verdict", strict: bool = True) -> dict:
    """EXP15 prereg §5a. The reused C/D verdict runs, scored at their EXP14 bands through the
    standing gates, MUST yield exactly C {0,2,4,5,6} / D {0,1,3,6}. Mismatch = INSTRUMENT
    REGRESSION -> fix the pipeline, NO read (fail loud; never a regime finding).

    Also reports whether the EXP15 COMMON RULER (0.6875x5) is SET-PRESERVING on each cell. For
    D this is tautological (the ruler IS D's committed band). For C it is a real check: the ruler
    RAISES C's band 0.64 -> 0.6875 at fixed N, so a converter could have been lost."""
    out = dict(verdict_tag=verdict_tag, cells={}, ok=True,
               ruler=dict(band=X15_RULER_BAND, N=X15_RULER_N))
    for cell in X15_CELLS:
        arm = CELLS[cell]["arm"]
        exp = X15_REPRO[cell]
        own, ruler, per_seed = [], [], []
        for s in VERDICT_SEEDS:
            p = OUTDIR / f"exp14_{arm}_s{s}_{verdict_tag}.json"
            if not p.exists():
                per_seed.append(dict(seed=s, status="MISSING"))
                out["ok"] = False
                continue
            rec = json.loads(p.read_text())
            onset = rec["acquisition_onset"]
            if onset is None:
                st = "UNREAD(unacquired)"
            elif (READ_AT - onset) < MIN_CONV_BUDGET:
                st = "UNREAD(budget-truncated)"                  # F6, same gate as score_2x2
            else:
                st = "READ"
            c_own = _density_conversion_onset(rec, exp["band"], exp["N"]) if st == "READ" else None
            c_rul = _density_conversion_onset(rec, X15_RULER_BAND, X15_RULER_N) if st == "READ" else None
            if c_own is not None:
                own.append(s)
            if c_rul is not None:
                ruler.append(s)
            per_seed.append(dict(seed=s, status=st, own_band_onset=c_own, ruler_onset=c_rul))
        matches = (own == exp["converters"])
        tautological = (exp["band"], exp["N"]) == (X15_RULER_BAND, X15_RULER_N)
        out["cells"][cell] = dict(
            arm=arm, own_band=dict(band=exp["band"], N=exp["N"]),
            expected=exp["converters"], own_band_converters=own,
            reproduces=bool(matches),
            ruler_converters=ruler, ruler_set_preserving=bool(ruler == own),
            ruler_check_tautological=bool(tautological),
            ruler_note=("TAUTOLOGICAL — the common ruler IS this cell's committed band"
                        if tautological else
                        f"NON-TRIVIAL — ruler raises the band {exp['band']} -> {X15_RULER_BAND} "
                        f"at fixed N={X15_RULER_N}; converters could have been LOST"),
            per_seed=per_seed)
        if not matches:
            out["ok"] = False
    out["headline"] = ("REPRODUCTION OK — pipeline validated"
                       if out["ok"] else "INSTRUMENT REGRESSION — pipeline diverged; NO READ")
    (OUTDIR / "exp15_reproduction_check.json").write_text(json.dumps(out, indent=2))
    print(f"\n=== EXP15 §5a REPRODUCTION CHECK — {out['headline']} ===")
    for cell, c in out["cells"].items():
        print(f"  {cell:12s} own band {c['own_band']['band']}x{c['own_band']['N']} -> "
              f"{c['own_band_converters']}  expected {c['expected']}  "
              f"{'REPRODUCES' if c['reproduces'] else 'MISMATCH'}")
        print(f"  {'':12s} common ruler {X15_RULER_BAND}x{X15_RULER_N} -> {c['ruler_converters']}  "
              f"set-preserving={c['ruler_set_preserving']}  [{c['ruler_note']}]")
    if strict and not out["ok"]:
        bad = {k: v["own_band_converters"] for k, v in out["cells"].items() if not v["reproduces"]}
        raise AssertionError(
            f"EXP15 §5a INSTRUMENT REGRESSION: reused verdict runs do not reproduce the committed "
            f"converter sets. got={bad}  expected={{c: X15_REPRO[c]['converters'] for c in bad}}. "
            f"FIX THE PIPELINE — do not read.")
    return out


def score_2x2(cal_tag: str = "2x2_cal", verdict_tag: str = "verdict", write: bool = True) -> dict:
    """DRAFT 4-cell attribution (§5) — VERDICT-STAGE. pre-gate A (READ=acquired) -> pre-gate B
    (F6 budget) -> conversion (per-cell fixpoint band, sustained-episode) -> F5 power gate ->
    attribution + factorial. DRAFT: routes behind the adversarial pass before the table reaches
    Jason. NOT run in the cal phase (verdict withheld).

    `write=False` = DRY. The committed `exp14_2x2_verdict_verdict.json` is a canon artifact
    (commit 19616d4); re-scoring it under the EXP15 §5b D-row fix must NOT overwrite it. Records
    stand and get superseded — they do not get regenerated in place."""
    band = json.loads((OUTDIR / f"exp14_band_{cal_tag}.json").read_text())
    if not band["spec_hash_parity"]["ok"]:
        raise AssertionError(f"F2 spec_hash parity breach in {cal_tag}; refusing to score")
    out = dict(cal_tag=cal_tag, verdict_tag=verdict_tag, cells={}, min_conv_budget=MIN_CONV_BUDGET)
    letter = {"A_dwell": "A", "B_12bc_dwp": "B", "C_shuffle": "C", "D_split": "D"}
    converts, ext_needed = set(), []
    for cell, meta in CELLS.items():
        c = band["cells"][cell]
        b, N = c["conv_band"], c["conv_consec"]                 # final band (provisional / C own-null)
        vtag = "verdict"                                        # A,D reuse committed screen verdict
        per_seed = []
        for s in VERDICT_SEEDS:
            p = OUTDIR / f"exp14_{meta['arm']}_s{s}_{vtag}.json"
            if not p.exists():
                per_seed.append(dict(seed=s, status="MISSING"))
                continue
            rec = json.loads(p.read_text())
            onset = rec["acquisition_onset"]
            if onset is None:
                st, conv = "UNREAD(unacquired)", None
            elif (READ_AT - onset) < MIN_CONV_BUDGET:
                st, conv = "UNREAD(budget-truncated)", None      # F6
            else:
                st = "READ"
                conv = _density_conversion_onset(rec, b, N)
            entry = dict(seed=s, status=st, acquisition_onset=onset,
                         conversion_onset=conv, converted=bool(conv is not None))
            if conv is not None:
                entry["stability"] = _stability_of_seed(rec, b, N)   # §3 companion
            per_seed.append(entry)
        read = [x for x in per_seed if x["status"] == "READ"]
        conv = [x for x in read if x["converted"]]
        # STABILITY COMPANION (prereg §3): sustain-to-horizon vs decay, per cell
        stab = [x["stability"] for x in conv]
        wem = [st["within_episode_mean"] for st in stab if st["within_episode_mean"] is not None]
        stability = dict(
            n_convert=len(conv),
            n_sustain_to_horizon=sum(1 for st in stab if st["sustains_to_horizon"]),
            sustainer_seeds=[x["seed"] for x in conv if x["stability"]["sustains_to_horizon"]],
            longest_episode=max([st["longest_episode"] for st in stab], default=0),
            within_episode_mean=round(sum(wem) / len(wem), 4) if wem else None)
        # pin-2 liveness (B only): a non-acquiring 12bc_dwp cell is UNREAD, never "no conversion"
        liveness_ok = True
        if cell == "B_12bc_dwp":
            liveness_ok = band["cells"][cell]["liveness"]["live"] and len(read) >= N_MIN_READ
        kcls = _classify_count(len(conv))
        if cell in ("B_12bc_dwp", "C_shuffle") and kcls in ("s0-class-lottery", "AMBIGUOUS"):
            ext_needed.append(cell)                              # F5 power gate -> EXT_POOL
        # --- D-ROW WIRING (EXP15 §5b fix, Jason 2026-07-10) --------------------------------
        # SUPERSEDED:  cell_converts = (len(conv) >= COUNT_CUTS["across_seeds"])
        # The count-cut is a SCREEN classifier (>=5 of 8 = "converts across seeds"). Applying it
        # to D — the reused committed corner whose job is F7 instrument-regression — mislabels it:
        # D converts 4/8 -> AMBIGUOUS -> excluded from `converts` -> _attribution_from_convertset
        # sees "not D_" and returns INSTRUMENT_REGRESSION *despite* D reproducing {0,1,3,6}
        # EXACTLY. In the committed EXP14 verdict this latent defect was masked only by the Pin-3
        # c_gt_d override firing first. The D row must key on the REPRODUCTION CHECK, not a count.
        # Old logic retained above, in-code, per report-don't-patch; committed artifacts stand.
        if cell == "D_split":
            cell_converts = (sorted(x["seed"] for x in conv) == X15_REPRO["D_split"]["converters"])
        else:
            cell_converts = (len(conv) >= COUNT_CUTS["across_seeds"])
        if cell == "B_12bc_dwp" and not liveness_ok:
            cell_status = "UNREAD-AT-HORIZON"
        elif len(read) < N_MIN_READ:
            cell_status = "UNREAD(<N_MIN READ)"
        else:
            cell_status = "converts" if cell_converts else ("ambiguous/lottery" if kcls in
                          ("s0-class-lottery", "AMBIGUOUS") else "silent")
        if cell_converts and cell_status == "converts":
            converts.add(letter[cell])
        out["cells"][cell] = dict(arm=meta["arm"], fabric=meta["fabric"], dose=meta["dose"],
                                  conv_band=b, conv_consec=N, n_read=len(read), n_converted=len(conv),
                                  converter_seeds=[x["seed"] for x in conv], count_class=kcls,
                                  cell_status=cell_status, liveness_ok=liveness_ok,
                                  false_rate_referent=band["cells"][cell].get("false_rate_referent"),
                                  stability=stability, per_seed=per_seed)
    attrib = _attribution_from_convertset(converts)
    # PIN 3 (Jason 2026-07-08) — C>D routes to OPEN-ATTRIBUTION, NOT the tidy row. If scheduled-
    # shuffled (C) converts MORE than coin-shuffled (D), on the shuffled fabric adding coin REDUCED
    # conversion = dose-inverted / coin×shuffled-interacting; held OPEN, do NOT collapse to a row.
    cc, dd = out["cells"]["C_shuffle"], out["cells"]["D_split"]
    c_readable = not cc["cell_status"].startswith("UNREAD")
    d_readable = not dd["cell_status"].startswith("UNREAD")
    c_gt_d = bool(c_readable and d_readable and cc["n_converted"] > dd["n_converted"])
    out["c_gt_d"] = dict(n_convert_C=cc["n_converted"], n_convert_D=dd["n_converted"], fired=c_gt_d)
    if c_gt_d:
        attrib = dict(
            attribution="OPEN_ATTRIBUTION — C>D dose-inversion/interaction (Pin 3)",
            note=(f"scheduled-shuffled C converts MORE than coin-shuffled D ({cc['n_converted']}>"
                  f"{dd['n_converted']}): on the shuffled fabric adding coin REDUCED conversion. This is "
                  "NOT the tidy fabric-main-effect / both-main-effects row — the dose-inverted / "
                  "coin×shuffled-interacting reading is held OPEN alongside the convert-set reading. The "
                  "panel separates them; do NOT collapse to a clean row."),
            convert_set_reading=attrib)
    # factorial companion (PARTIAL if any cell UNREAD)
    def rate(cell):
        cc = out["cells"][cell]
        return None if cc["cell_status"].startswith("UNREAD") else cc["n_converted"] / max(1, cc["n_read"])
    rA, rB, rC, rD = (rate(k) for k in ("A_dwell", "B_12bc_dwp", "C_shuffle", "D_split"))
    partial = any(r is None for r in (rA, rB, rC, rD))
    out["converts"] = sorted(converts)
    out["ext_pool_needed"] = ext_needed                         # F5: extend these before finalizing
    out["attribution_DRAFT"] = attrib
    out["factorial"] = (dict(status="PARTIAL — a cell is UNREAD; interaction undefined")
                        if partial else dict(
                        dose=round((rB + rD) / 2 - (rA + rC) / 2, 4),
                        fabric=round((rC + rD) / 2 - (rA + rB) / 2, 4),
                        interaction=round((rD - rB) - (rC - rA), 4)))
    out["DRAFT_note"] = ("DRAFT — behind the adversarial refute-default pass before the table; "
                         "counts NOT claimed robust at n=8 (F5); pattern is the verdict")
    out["pin2_panel_posture"] = (                               # Pin 2 — cal is NOT a prior
        "REFUTE-DEFAULT. Cal previewed fabric-on + C>D; the verdict TESTS it, does NOT inherit it. "
        "The adversarial panel's job is to REFUTE these conversions on their own bands+gates; any lens "
        "that assumes 'we expect fabric' is DISQUALIFIED. Attribution routes to Jason AFTER the panel.")
    out["referent_reminder"] = ("SAME alpha, DIFFERENT null: a C conversion means 'leaves C's SHIFTED "
                                "baseline' (own between-episode null 0.64x5); A/B/D mean 'leaves the "
                                "dwelled marginal'. Do not read the fr's as one equal-guarantee column.")
    out["d_row_wiring"] = ("EXP15 §5b: D keys on the REPRODUCTION CHECK (exact committed set), not "
                           "on count_class>=5. The count-cut mislabelled the reused corner (4/8 -> "
                           "AMBIGUOUS -> INSTRUMENT_REGRESSION despite exact reproduction).")
    if write:
        (OUTDIR / f"exp14_2x2_verdict_{verdict_tag}.json").write_text(json.dumps(out, indent=2))
    else:
        print("[DRY] score_2x2: committed artifact NOT overwritten (records stand).")
    print(json.dumps({k: v for k, v in out.items() if k != "cells"}, indent=2))
    for cell, c in out["cells"].items():
        st = c["stability"]
        print(f"\n{cell} [{c['fabric']}x{c['dose']}] {c['arm']}: band {c['conv_band']}x{c['conv_consec']}  "
              f"READ {c['n_read']}/8  CONVERTED {c['n_converted']} {c['converter_seeds']}  [{c['cell_status']}]")
        print(f"    stability: n_sustain-to-horizon {st['n_sustain_to_horizon']}/{st['n_convert']} "
              f"{st['sustainer_seeds']}  longest_episode {st['longest_episode']}  within-ep mean {st['within_episode_mean']}")
    return out


# =============================================================================================
# EXP15 — DURABILITY BY DOSE (prereg §4/§7). BUILT; the 40 runs are WITHHELD behind Jason's GO.
# `score_durability` is guarded in _main behind --release-durability and refuses a primary read
# unless the {8-27} records exist.
# =============================================================================================
def seed_pool_audit() -> dict:
    """EXP15 build-gate seed-pool audit. REPORT-DON'T-PATCH: it names collisions and lets
    `score_durability` refuse; it never silently edits a constant.

    HISTORY (keep — a successor must not re-introduce the pool it repairs): the originally ratified
    pool {8-27} (A1) SILENTLY RE-ADMITTED the EXP14 cal seeds {20,21,22,24,25}. Because a run is
    fully determined by (arm, seed, h_max) and both cal and EXP15 build the fabric at h_max=1M, an
    EXP15 run at s20 would be the SAME TRAJECTORY as the committed cal run at s20 -- a bit-identical
    replay of the runs that CUT the bands the primary scores against, whose conversion outcomes are
    already recorded. That is an outcome-blindness break, not merely a circularity.
    RULING 2 (Jason 2026-07-10) repaired the pool to {8-19} u {28-35}."""
    new, cal = set(X15_NEW_SEEDS), set(CAL_SEEDS)
    verdict, reserve, subst = set(VERDICT_SEEDS), set(X15_RESERVE_POOL), set(X15_SUBST_POOL)
    cal_collision = sorted(new & cal)
    known_defect = sorted(new & {23})            # s23: real fabric defect, swapped out at EXP14 cal
    blockers, warnings = [], []
    if cal_collision:
        blockers.append(dict(
            id="CAL_SEEDS_IN_VERDICT_POOL", seeds=cal_collision,
            detail=("EXP14 cal seeds are inside the EXP15 new-seed pool. Same (arm,seed,h_max) => "
                    "identical trajectory => bit-identical replays of the traces that CUT the "
                    "bands, with outcomes already recorded. Outcome-blindness broken on "
                    f"{len(cal_collision)}/{len(X15_NEW_SEEDS)} of each cell's sample."),
            routes_to="Jason — a ratified constant. Do not change it here."))
    if known_defect:
        blockers.append(dict(
            id="KNOWN_DEFECTIVE_SEED_IN_POOL", seeds=known_defect,
            detail=("s23 was REJECTED at EXP14 cal as a genuine fabric defect (per-lag nuisance "
                    "0.1346 > 0.1344 at every horizon) -> 'swap, don't tune'. It must not be in "
                    "the pool. (The EXP15 pre-check independently reproduced this failure on BOTH "
                    "shuffled arms: 0.13464194536209106 > 0.13435383141040802.)"),
            routes_to="Jason — repair the pool"))
    assert not (subst & reserve), "substitution pool must not intersect the reserve"
    assert not (new & verdict), "new seeds must not intersect the committed verdict seeds"
    assert not (new & reserve), "new seeds must not intersect the reserve"
    assert len(X15_NEW_SEEDS) == len(new) == 20, "the new-seed pool must be 20 distinct seeds"
    audit = dict(
        new_seeds=sorted(new), cal_seeds=sorted(cal), verdict_seeds=sorted(verdict),
        reserve_pool=sorted(reserve), substitution_pool=sorted(subst),
        prechecked_carry=list(X15_PRECHECKED_CARRY),
        cal_collision=cal_collision, known_defective_in_pool=known_defect,
        blockers=blockers, warnings=warnings, clean=not blockers)
    return audit


# ---------------------------------------------------- exact rank-sum / Mann-Whitney (Ruling 1)
def _midranks_doubled(pooled_sorted: list[float]) -> list[int]:
    """2 x midrank for each element of a SORTED pool (doubled to stay integral under ties)."""
    n, out, i = len(pooled_sorted), [0] * len(pooled_sorted), 0
    while i < n:
        j = i
        while j < n and pooled_sorted[j] == pooled_sorted[i]:
            j += 1
        m2 = (i + 1) + j                     # 2 * mean(rank_{i+1} .. rank_j), 1-based
        for k in range(i, j):
            out[k] = m2
        i = j
    return out


def _exact_rank_sum_p(x: list[float], y: list[float]) -> float:
    """EXACT one-sided permutation p for "x stochastically GREATER than y", conditional on the
    observed pooled multiset -- i.e. the exact Mann-Whitney/Wilcoxon rank-sum test, TIE-AWARE and
    fully deterministic (no RNG, no normal approximation, pure stdlib).

    The null is exactly the one Ruling 1 names: BETWEEN-CELL EXCHANGEABILITY. Under it every
    assignment of n1 of the N pooled midranks to x is equally likely, so
        p = #{subsets S, |S|=n1 : sum(midranks in S) >= W_obs} / C(N, n1).
    Counted by a 0/1 knapsack DP over doubled midranks (integral => no float drift)."""
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return 1.0
    pooled = sorted(list(x) + list(y))
    dbl = _midranks_doubled(pooled)
    rank_of = {}
    for v, r in zip(pooled, dbl):
        rank_of[v] = r                        # ties share a midrank, so this map is well-defined
    w_obs = sum(rank_of[v] for v in x)
    N, maxs = n1 + n2, sum(dbl)
    dp = [[0] * (maxs + 1) for _ in range(n1 + 1)]
    dp[0][0] = 1
    for r in dbl:                             # 0/1 knapsack: each midrank used at most once
        for k in range(min(n1, N), 0, -1):
            row_k, row_p = dp[k], dp[k - 1]
            for s in range(maxs, r - 1, -1):
                if row_p[s - r]:
                    row_k[s] += row_p[s - r]
    ge = sum(dp[n1][s] for s in range(w_obs, maxs + 1))
    return ge / math.comb(N, n1)


def _fmt_seeds(xs) -> str:
    """Collapse to ranges — the EXP15 pool is NON-CONTIGUOUS ({8-19} u {28-35}); printing
    'first-last' would misrepresent it as spanning the cal seeds it was repaired to exclude."""
    if not xs:
        return "{}"
    xs, parts, i = sorted(xs), [], 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[j + 1] == xs[j] + 1:
            j += 1
        parts.append(str(xs[i]) if i == j else f"{xs[i]}-{xs[j]}")
        i = j + 1
    return "{" + ",".join(parts) + "}"


def _print_seed_audit(a: dict) -> None:
    print("\n=== EXP15 SEED-POOL AUDIT ===")
    print(f"  new {_fmt_seeds(a['new_seeds'])} (n={len(a['new_seeds'])})   "
          f"cal {_fmt_seeds(a['cal_seeds'])}   verdict {_fmt_seeds(a['verdict_seeds'])}")
    print(f"  reserve {_fmt_seeds(a['reserve_pool'])}   subst {_fmt_seeds(a['substitution_pool'])}"
          f"   pre-checked carry {a.get('prechecked_carry')}")
    for b in a["blockers"]:
        print(f"  ** BLOCKER {b['id']}: seeds {b['seeds']}\n     {b['detail']}\n     -> {b['routes_to']}")
    for w in a["warnings"]:
        print(f"  *  WARNING {w['id']}: seeds {w['seeds']}\n     {w['detail']}\n     -> {w['routes_to']}")
    if a["clean"]:
        print("  clean — no collisions")


def _fisher_one_sided(a: int, b: int, c: int, d: int) -> float:
    """SUPERSEDED as the EXP15 primary by RULING 1 (retained, not deleted — records stand).

    Fisher tested a BINARY sustain rate. The binary is degenerate here (locked-state sustain is 0/16
    at 500k), so the primary is now an exact rank-sum on a CONTINUOUS statistic (`_exact_rank_sum_p`).
    Kept for reference and for any future genuinely-binary 2x2.

    One-sided Fisher exact, P(X >= a) on the 2x2  [[a, b], [c, d]]. Pure stdlib (math.comb)."""
    n1, n2 = a + b, c + d                       # row totals (D converters, C converters)
    k = a + c                                   # col total (sustainers)
    n = n1 + n2
    if n1 == 0 or n2 == 0 or k == 0 or k == n:
        return 1.0
    lo, hi = max(0, k - n2), min(k, n1)
    denom = math.comb(n, k)
    return sum(math.comb(n1, x) * math.comb(n2, k - x) for x in range(a, hi + 1)) / denom


def _truncate(rec: dict, t_max: int) -> dict:
    """A2: the PRIMARY is frozen at 500k on ALL seeds. New seeds run to 1M; read them at 500k by
    dropping columns past t_max. Reused seeds already end at 500k (no-op). Returns a shallow copy;
    the on-disk record is never mutated."""
    r = dict(rec)
    r["columns"] = [c for c in rec["columns"] if c["t"] <= t_max]
    return r


def _post_acq(rec: dict):
    o = rec["acquisition_onset"]
    if o is None:
        return []
    return [c["exam_acc"] for c in rec["columns"]
            if c["t"] >= o and c.get("exam_acc") is not None]


def _longest_episode(vals, band: float, N: int) -> int:
    best, i, n = 0, 0, len(vals)
    while i < n:
        if vals[i] >= band:
            j = i
            while j < n and vals[j] >= band:
                j += 1
            if j - i >= N:
                best = max(best, j - i)
            i = j
        else:
            i += 1
    return best


def _max_run(vals, band: float) -> int:
    """Longest run of consecutive windows >= band (NO N threshold). The bare-N census statistic."""
    best, cur = 0, 0
    for a in vals:
        cur = cur + 1 if a >= band else 0
        best = max(best, cur)
    return best


def _durability_of_seed(rec: dict, band: float, N: int, k_last: int,
                        q_from: int = None, q_to: int = None) -> dict:
    """PRIMARY measure (Ruling 1): FINAL-QUARTILE TIME-ABOVE-BAND = fraction of eval windows in
    the ABSOLUTE interval (q_from, q_to] with exam_acc >= band. Continuous; no threshold to
    alpha-calibrate. The locked-state `mean(last k_last) >= band` and the single-endpoint form are
    RETIRED as primaries and retained as SENSITIVITIES ONLY."""
    q_from = X15_FINAL_Q_FROM if q_from is None else q_from
    q_to = X15_PRIMARY_AT if q_to is None else q_to
    vals = _post_acq(rec)
    o = rec["acquisition_onset"]
    post = [c for c in rec["columns"]
            if o is not None and c["t"] >= o and c.get("exam_acc") is not None]

    # --- PRIMARY: absolute final-quartile window, NOT a fraction of the post-acq span ---
    q = [c for c in post if q_from < c["t"] <= q_to]
    frac_q4 = (sum(1 for c in q if c["exam_acc"] >= band) / len(q)) if q else None

    # --- retired forms, kept for the registered sensitivities ---
    tail = vals[-k_last:] if len(vals) >= k_last else vals
    last_mean = (sum(tail) / len(tail)) if tail else None
    endpoint = vals[-1] if vals else None

    longest = _longest_episode(vals, band, N)     # longest run of length >= N (0 if none)
    maxrun = _max_run(vals, band)                 # longest run at all (census)

    # companions (read-only, no claims)
    n_ep, last_end_t, i, n = 0, None, 0, len(post)
    while i < n:
        if post[i]["exam_acc"] >= band:
            j = i
            while j < n and post[j]["exam_acc"] >= band:
                j += 1
            if j - i >= N:
                n_ep += 1
                last_end_t = post[j - 1]["t"]
            i = j
        else:
            i += 1
    return dict(
        # PRIMARY
        frac_above_band_final_quartile=round(frac_q4, 6) if frac_q4 is not None else None,
        final_quartile_windows=len(q), final_quartile=[q_from, q_to],
        # RULING 3 eligibility input
        longest_episode=longest, max_run=maxrun,
        dur_pool_ok=bool(longest >= X15_DUR_MIN_RUN),
        bare_ruler=bool(0 < longest < X15_DUR_MIN_RUN),   # phantom signature (band lesson)
        # SENSITIVITIES (never primary)
        last_k_mean=round(last_mean, 4) if last_mean is not None else None,
        sustains_lockedstate=bool(last_mean is not None and last_mean >= band),
        endpoint_acc=round(endpoint, 4) if endpoint is not None else None,
        sustains_endpoint=bool(endpoint is not None and endpoint >= band),
        # companions
        episode_recurrence=n_ep, last_episode_end_t=last_end_t)


# ------------------------------------------- coded loose-N floor gate (Ruling 3; the band lesson)
def _episodes_ge(vals, band: float, N: int) -> list[int]:
    out, i, n = [], 0, len(vals)
    while i < n:
        if vals[i] >= band:
            j = i
            while j < n and vals[j] >= band:
                j += 1
            if j - i >= N:
                out.append(j - i)
            i = j
        else:
            i += 1
    return out


def phantom_floor_gate(cell: str, seeds, tag_of, band: float, N: int, cal_seeds=None) -> dict:
    """RULING 3 — the loose-N carry becomes a CODED GATE. Per cell, compute the false-alarm
    EXPECTATION at the common ruler on the cell's OWN honest null, and compare it to the observed
    converter count. A cell AT its floor is FLAGGED before its count means anything.

    UNIT (per [[feedback_loose_N_false_alarm]]): count EPISODES, not hit-positions. A `_consec_rate`
    position-rate overcounts by the mean cluster size; at N=3 (cell B) episodes are almost all
    exactly length 3 so the shortcut was safe, but at N=5 it is NOT. Both units are reported; the
    EPISODE unit is the gate. Contiguity is respected (a pooled null spliced across excluded
    windows manufactures runs).

    The null is the cell's BETWEEN-EPISODE pool (conversions + shoulders excluded) -- the honest
    non-converting baseline. NOTE it is an inflated UPPER BOUND for C, whose cal pool converted 4/5.
    """
    cal_seeds = cal_seeds or CAL_SEEDS
    arm, cal_tag = CELLS[cell]["arm"], CELLS[cell]["cal_tag"]
    per_seed_accs = {}
    for s in cal_seeds:
        p = OUTDIR / f"exp14_{arm}_s{s}_{cal_tag}.json"
        if p.exists():
            per_seed_accs[s] = _post_acq(json.loads(p.read_text()))
    segs = _null_segments(per_seed_accs, CONV_LOW, CONV_MIN)
    n_pos = sum(max(0, len(sg) - N + 1) for sg in segs)
    ep_lens = [L for sg in segs for L in _episodes_ge(sg, band, N)]
    n_ep = len(ep_lens)
    n_hitpos = sum(L - N + 1 for L in ep_lens)
    ep_rate = (n_ep / n_pos) if n_pos else 0.0
    pos_rate = (n_hitpos / n_pos) if n_pos else 0.0

    # per-seed phantom probability over each scored seed's own post-onset span
    ps_ep, ps_pos, census, observed = [], [], [], []
    for s in seeds:
        p = OUTDIR / f"exp14_{arm}_s{s}_{tag_of(s)}.json"
        if not p.exists():
            continue
        rec = _truncate(json.loads(p.read_text()), X15_PRIMARY_AT)
        vals = _post_acq(rec)
        m = max(0, len(vals) - N + 1)
        ps_ep.append(1 - (1 - ep_rate) ** m)
        ps_pos.append(1 - (1 - pos_rate) ** m)
        census.append(dict(seed=s, max_run=_max_run(vals, band),
                           longest_episode=_longest_episode(vals, band, N)))
        if _longest_episode(vals, band, N) > 0:
            observed.append(s)
    exp_ep, exp_pos = sum(ps_ep), sum(ps_pos)
    p_ge_obs = _poisson_binomial_ge(ps_ep, len(observed)) if ps_ep else None
    at_floor = bool(p_ge_obs is not None and p_ge_obs > 0.10)
    return dict(
        cell=cell, band=band, N=N, null="between-episode (conversions + shoulders excluded)",
        n_null_positions=n_pos, n_null_episodes=n_ep, null_episode_lengths=sorted(ep_lens, reverse=True),
        mean_cluster_size=round(n_hitpos / n_ep, 3) if n_ep else None,
        episode_rate=round(ep_rate, 8), position_rate=round(pos_rate, 8),
        expected_phantom_converters_EPISODE_UNIT=round(exp_ep, 3),
        expected_phantom_converters_position_unit=round(exp_pos, 3),
        observed_converters=len(observed), converter_seeds=observed,
        P_observed_or_more_under_floor=round(p_ge_obs, 5) if p_ge_obs is not None else None,
        at_floor=at_floor,
        verdict=("AT-FLOOR — the crossing count carries NO signal; the cell must be carried by "
                 "episode QUALITY (run length), not by n/N converted"
                 if at_floor else
                 "ABOVE-FLOOR — the crossing count exceeds the false-alarm expectation"),
        bare_N_census=census,
        census_note=("max_run per seed at the ruler. A bimodal census (noise ceiling << N << "
                     "converter floor) is what protects a loose-N rule; a populated [N, 2N] band "
                     "means phantoms have arrived."),
        null_caveat=("This floor is an inflated UPPER BOUND where the cal pool itself converted "
                     "(C: 4/5 cal seeds are s0-class converters, so residual shoulders survive the "
                     "CONV_MIN=8 exclusion). Under-, not over-, state the risk."))


def _poisson_binomial_ge(ps: list[float], k: int) -> float:
    """Exact P(X >= k), X = sum of independent Bernoulli(ps). DP convolution, no RNG."""
    dist = [1.0]
    for p in ps:
        nxt = [0.0] * (len(dist) + 1)
        for i, d in enumerate(dist):
            nxt[i] += d * (1 - p)
            nxt[i + 1] += d * p
        dist = nxt
    return sum(dist[k:]) if k <= len(dist) - 1 else 0.0


def _cell_durability(cell: str, seeds, tag_of, band: float, N: int, k_last: int,
                     t_primary: int, t_dur: int, q_from: int = None) -> dict:
    """Eligibility (Ruling 3) = CONVERTED (>=N consec >= band) AND longest-run >= X15_DUR_MIN_RUN (8)
    AND runway >= T_DUR. The three exclusions are reported SEPARATELY and never conflated:
      DUR-CENSORED   -> too little runway to read durability at all (never "decayed")
      BARE-N         -> a phantom-shaped converter; excluded from the durability POOL, not from the
                        converter count (the converter definition is unchanged, per Ruling 3)."""
    arm = CELLS[cell]["arm"]
    per_seed, missing = [], []
    for s in seeds:
        p = OUTDIR / f"exp14_{arm}_s{s}_{tag_of(s)}.json"
        if not p.exists():
            missing.append(s)
            per_seed.append(dict(seed=s, status="MISSING"))
            continue
        rec = _truncate(json.loads(p.read_text()), t_primary)   # A2: frozen at 500k
        onset = rec["acquisition_onset"]
        if onset is None:
            per_seed.append(dict(seed=s, status="UNREAD(unacquired)"))
            continue
        conv = _density_conversion_onset(rec, band, N)
        d = _durability_of_seed(rec, band, N, k_last, q_from=q_from, q_to=t_primary)
        if conv is None:
            per_seed.append(dict(seed=s, status="READ", converted=False,
                                 acquisition_onset=onset, max_run=d["max_run"]))
            continue
        runway = t_primary - conv
        censored = runway < t_dur
        if censored:
            elig = "DUR-CENSORED"
        elif not d["dur_pool_ok"]:
            elig = f"BARE-N (longest episode {d['longest_episode']} < {X15_DUR_MIN_RUN})"
        else:
            elig = "ELIGIBLE"
        per_seed.append(dict(seed=s, status="READ", converted=True, acquisition_onset=onset,
                             conversion_onset=conv, runway=runway, censored=bool(censored),
                             eligibility=elig, **d))
    conv = [x for x in per_seed if x.get("converted")]
    cens = [x for x in conv if x["censored"]]
    bare = [x for x in conv if not x["censored"] and not x["dur_pool_ok"]]
    elig = [x for x in conv if not x["censored"] and x["dur_pool_ok"]]
    vals = [x["frac_above_band_final_quartile"] for x in elig
            if x["frac_above_band_final_quartile"] is not None]
    return dict(
        cell=cell, arm=arm, fabric=CELLS[cell]["fabric"], dose=CELLS[cell]["dose"],
        n_seeds=len(seeds), n_missing=len(missing), missing=missing,
        n_read=sum(1 for x in per_seed if x["status"] == "READ"),
        n_converted=len(conv), converter_seeds=[x["seed"] for x in conv],
        n_censored=len(cens), censored_seeds=[x["seed"] for x in cens],
        n_bare_N=len(bare), bare_N_seeds=[x["seed"] for x in bare],
        n_eligible=len(elig), eligible_seeds=[x["seed"] for x in elig],
        # PRIMARY statistic, per eligible converter
        final_quartile_frac=[round(v, 6) for v in vals],
        final_quartile_frac_mean=round(sum(vals) / len(vals), 6) if vals else None,
        # retired forms (sensitivity inputs only)
        n_sustain_lockedstate=sum(1 for x in elig if x["sustains_lockedstate"]),
        n_sustain_endpoint=sum(1 for x in elig if x["sustains_endpoint"]),
        last_k_means=[x["last_k_mean"] for x in elig],
        max_run_census=[dict(seed=x["seed"], max_run=x.get("max_run")) for x in per_seed
                        if x["status"] == "READ"],
        per_seed=per_seed)


def score_durability(verdict_tag: str = "verdict", new_tag: str = "exp15",
                     seeds_new=None, band: float = None, N: int = None,
                     k_last: int = None, out_tag: str = "exp15", require_new: bool = True) -> dict:
    """EXP15 DRAFT durability read (prereg §7, as re-posed by Ruling 1).

    PRIMARY: exact Mann-Whitney one-sided (D > C) on FINAL-QUARTILE TIME-ABOVE-BAND -- the fraction
    of eval windows in (375k, 500k] with exam_acc >= the common ruler -- among ELIGIBLE converters,
    NEW SEEDS ONLY. The committed 16 are CONTEXT/SENSITIVITY, never primary (peek quarantine).

    DRAFT — halts here. Routes behind the adversarial refute-default pass (NO LENS ASSUMES D>C).
    Attribution routes to Jason. Sensitivities are REPORTED, never verdict-deciding."""
    band = X15_RULER_BAND if band is None else band
    N = X15_RULER_N if N is None else N
    k_last = X15_K_LAST if k_last is None else k_last
    seeds_new = X15_NEW_SEEDS if seeds_new is None else seeds_new

    # gate: the reused corner must still reproduce (F7 / §5a) before ANY durability read
    repro = reproduction_check(verdict_tag=verdict_tag, strict=True)

    # gate: seed-pool integrity (outcome-blindness). Routes to Jason; never auto-resolved here.
    audit = seed_pool_audit()
    if audit["blockers"]:
        _print_seed_audit(audit)
        raise AssertionError(
            f"EXP15 REFUSED: seed-pool BLOCKER(s) {[b['id'] for b in audit['blockers']]}. "
            "Surface to Jason; do not patch.")

    all_seeds = list(VERDICT_SEEDS) + list(seeds_new)

    def tag_of(s):
        return verdict_tag if s in VERDICT_SEEDS else new_tag

    if require_new:
        have = [s for s in seeds_new
                if (OUTDIR / f"exp14_{CELLS['D_split']['arm']}_s{s}_{new_tag}.json").exists()]
        if len(have) < len(seeds_new):
            raise AssertionError(
                f"EXP15 primary REFUSED: {len(seeds_new)-len(have)} of {len(seeds_new)} new-seed "
                f"records missing (tag='{new_tag}'). The 40 runs are WITHHELD until Jason's GO. "
                f"Pass require_new=False only for smoke/synthetic exercise.")

    out = dict(exp="exp15_durability_by_dose", verdict_tag=verdict_tag, new_tag=new_tag,
               ruler=dict(band=band, N=N), t_dur=X15_T_DUR, dur_min_run=X15_DUR_MIN_RUN,
               primary_at=X15_PRIMARY_AT, final_quartile=[X15_FINAL_Q_FROM, X15_PRIMARY_AT],
               primary_scope=X15_PRIMARY_SCOPE,
               seeds=dict(committed=list(VERDICT_SEEDS), new=list(seeds_new)),
               reproduction_check=dict(ok=repro["ok"],
                                       cells={k: v["reproduces"] for k, v in repro["cells"].items()}),
               cells={}, context_committed={})

    # ---- PRIMARY: new seeds only ----
    for cell in X15_CELLS:
        out["cells"][cell] = _cell_durability(cell, seeds_new, tag_of, band, N, k_last,
                                              X15_PRIMARY_AT, X15_T_DUR)
    D, C = out["cells"]["D_split"], out["cells"]["C_shuffle"]
    xD, xC = D["final_quartile_frac"], C["final_quartile_frac"]
    p_dgtc = _exact_rank_sum_p(xD, xC)
    p_cgtd = _exact_rank_sum_p(xC, xD)
    floor_met = (D["n_eligible"] >= X15_CONV_FLOOR and C["n_eligible"] >= X15_CONV_FLOOR)

    # ---- RULING 3: coded loose-N floor gate, per cell (before any count means anything) ----
    out["phantom_floor_gate"] = {c: phantom_floor_gate(c, seeds_new, tag_of, band, N)
                                 for c in X15_CELLS}
    flagged = [c for c, g in out["phantom_floor_gate"].items() if g["at_floor"]]

    # ---- §7 outcome cells (exhaustive, pre-registered; unchanged by Ruling 1) ----
    if not floor_met:
        cellname = "UNDERPOWERED"
        note = (f"eligible converters D {D['n_eligible']} / C {C['n_eligible']} vs floor "
                f"{X15_CONV_FLOOR}. TOP-UP RULE: pairs from reserve {X15_RESERVE_POOL} "
                f"(lowest-first, BOTH cells, cap +{X15_RESERVE_CAP}/cell). Floor still unmet after "
                f"the capped top-up -> routes to Jason, named.")
    elif p_cgtd <= X15_ALPHA_P:
        cellname = "INVERTED"
        note = ("C > D significant — ANOMALY-CLASS. Surface, audit, NEVER force.")
    elif p_dgtc <= X15_ALPHA_P:
        cellname = "PROMOTED"
        note = ("p <= 0.05 AND floor met -> the §10.24 companion is PROMOTED: within the shuffled "
                "fabric, dose gates durability. Scope-fenced: this power, this horizon, no onset "
                "re-litigation.")
    else:
        cellname = "NOT-PROMOTED-AT-POWER"
        note = ("floor met, p > 0.05 -> the companion is RETIRED AT THIS POWER, recorded. Not a "
                "refutation of durability-by-dose in principle; a null at n=20/cell.")

    out["primary"] = dict(
        test="EXACT Mann-Whitney / rank-sum, one-sided (D > C), tie-aware, deterministic",
        statistic="final-quartile time-above-band = frac windows in (375k,500k] with exam_acc >= ruler",
        null="between-cell exchangeability of the eligible-converter values",
        scope="NEW SEEDS ONLY (peek quarantine)",
        D=dict(n_eligible=D["n_eligible"], values=xD, mean=D["final_quartile_frac_mean"]),
        C=dict(n_eligible=C["n_eligible"], values=xC, mean=C["final_quartile_frac_mean"]),
        p_one_sided_D_gt_C=round(p_dgtc, 6), p_one_sided_C_gt_D=round(p_cgtd, 6),
        alpha=X15_ALPHA_P, converter_floor=X15_CONV_FLOOR, floor_met=bool(floor_met))
    out["outcome_cell"] = dict(cell=cellname, note=note)
    if flagged:
        out["outcome_cell"]["floor_flag"] = (
            f"CELL(S) AT FLOOR: {flagged}. Their converter COUNT carries no signal (observed ~ "
            "false-alarm expectation). The durability pool is protected by the longest-run>=8 gate, "
            "but any statement about how MANY seeds converted in a flagged cell must not be made.")

    # ---- sensitivities: REPORTED, never verdict-deciding ----
    sens = {}
    #  (i) the PEEKED statistic: locked-state last-K mean, as a LEVEL (continuous), not a threshold
    lkD = [x["last_k_mean"] for x in D["per_seed"]
           if x.get("eligibility") == "ELIGIBLE" and x.get("last_k_mean") is not None]
    lkC = [x["last_k_mean"] for x in C["per_seed"]
           if x.get("eligibility") == "ELIGIBLE" and x.get("last_k_mean") is not None]
    sens["last_k_mean_LEVEL_peeked"] = dict(
        D=lkD, C=lkC, p_one_sided_D_gt_C=round(_exact_rank_sum_p(lkD, lkC), 6),
        note="THE PEEKED STATISTIC (CC's MW; Jason's verification). SENSITIVITY ONLY, never primary.")
    #  (ii) the 0.64 ruler variant (C's own EXP14 band applied to BOTH cells)
    D64 = _cell_durability("D_split", seeds_new, tag_of, 0.64, N, k_last, X15_PRIMARY_AT, X15_T_DUR)
    C64 = _cell_durability("C_shuffle", seeds_new, tag_of, 0.64, N, k_last, X15_PRIMARY_AT, X15_T_DUR)
    sens["ruler_0.64_variant"] = dict(
        D=D64["final_quartile_frac"], C=C64["final_quartile_frac"],
        p_one_sided_D_gt_C=round(_exact_rank_sum_p(D64["final_quartile_frac"],
                                                   C64["final_quartile_frac"]), 6))
    #  (iii) committed-16-included variant (context; NOT the primary scope)
    Da = _cell_durability("D_split", all_seeds, tag_of, band, N, k_last, X15_PRIMARY_AT, X15_T_DUR)
    Ca = _cell_durability("C_shuffle", all_seeds, tag_of, band, N, k_last, X15_PRIMARY_AT, X15_T_DUR)
    sens["committed_16_included"] = dict(
        D=Da["final_quartile_frac"], C=Ca["final_quartile_frac"],
        n_eligible=dict(D=Da["n_eligible"], C=Ca["n_eligible"]),
        p_one_sided_D_gt_C=round(_exact_rank_sum_p(Da["final_quartile_frac"],
                                                   Ca["final_quartile_frac"]), 6),
        note="CONTEXT. The committed 16 are peek-contaminated; never primary.")
    flips = [k for k, v in sens.items()
             if v.get("p_one_sided_D_gt_C") is not None
             and (v["p_one_sided_D_gt_C"] <= X15_ALPHA_P) != (p_dgtc <= X15_ALPHA_P)]
    out["sensitivities"] = sens

    # ---- CENSORING DEPENDENCY (diagnostic, NOT a sensitivity, NEVER an alternative primary) ----
    # Pre-declared because it is load-bearing on the committed context: the single DUR-CENSORED
    # committed seed is C-s6 (conversion onset 427.5k, runway 72.5k), whose 90-window episode lies
    # almost wholly INSIDE the final quartile. Its frac would be 0.4688 -- second-highest overall --
    # and including it moves the committed-context p from 0.028571 to 0.095238.
    #
    # Censoring it is CORRECT: with only 72.5k of runway, `time-above-band in the final quartile`
    # measures RECENCY (it just converted), not DURABILITY (it persisted). That is precisely the
    # confound T_DUR was re-scoped to guard (Ruling 1). So this is REPORTED, never scored:
    # "include the censored seeds" is NOT a valid alternative primary, and must not be run as one.
    def _censored_vals(cellname, seeds):
        cc = _cell_durability(cellname, seeds, tag_of, band, N, k_last, X15_PRIMARY_AT, X15_T_DUR)
        return [dict(seed=x["seed"], conversion_onset=x["conversion_onset"], runway=x["runway"],
                     frac_if_included=x["frac_above_band_final_quartile"])
                for x in cc["per_seed"] if x.get("censored")]
    out["censoring_dependency"] = dict(
        censored_new={c: _censored_vals(c, seeds_new) for c in X15_CELLS},
        censored_committed={c: _censored_vals(c, VERDICT_SEEDS) for c in X15_CELLS},
        note=("DIAGNOSTIC ONLY. A censored converter has too little runway for the final-quartile "
              "fraction to mean durability -- it measures RECENCY. Do NOT re-score with censored "
              "seeds included; that reinstates the exact confound T_DUR excludes. Reported so that "
              "a result which depends on a single censoring decision is VISIBLE, not so that the "
              "decision can be reversed after seeing the outcome."),
        committed_context_warning=(
            "On the COMMITTED 16 the sole censored seed is C-s6 (onset 427500, runway 72500, frac "
            "0.4688 if included). Censoring it is what makes the committed context significant "
            "(p 0.028571 -> 0.095238 if included). The committed 16 are CONTEXT, never primary; "
            "this is exactly why the primary is quarantined to the new seeds."))
    out["definition_sensitive"] = bool(flips)
    out["sensitivity_note"] = (
        (f"DEFINITION-SENSITIVE — a sensitivity flips significance: {flips}. The PRIMARY still "
         "decides; promotion (if any) carries this caveat VISIBLY.")
        if flips else "Sensitivities agree with the primary (reported, never verdict-deciding).")

    # ---- context: the committed 16 (never primary) ----
    for cell in X15_CELLS:
        cc = _cell_durability(cell, VERDICT_SEEDS, tag_of, band, N, k_last,
                              X15_PRIMARY_AT, X15_T_DUR)
        out["context_committed"][cell] = dict(
            n_converted=cc["n_converted"], n_censored=cc["n_censored"], n_bare_N=cc["n_bare_N"],
            n_eligible=cc["n_eligible"], final_quartile_frac=cc["final_quartile_frac"],
            n_sustain_lockedstate=cc["n_sustain_lockedstate"],
            n_sustain_endpoint=cc["n_sustain_endpoint"])
    out["locked_state_finding"] = (
        "LOCKED-STATE SUSTAIN DOES NOT EXIST AT 500k IN THIS REGIME (recorded, prereg §6). "
        "mean(last 10) >= ruler returns 0/16 on the committed verdict seeds; no bar both controls "
        "alpha and produces sustainers (the alpha-calibrated K=10 bar is 0.79 > the ruler). "
        "Conversion is EPISODIC (2-27 recurring episodes per committed converter at the ruler, "
        "median 9), so a locked-state read "
        "measures a state the phenomenon does not occupy. Hence the re-posed continuous primary.")

    # ---- companions: read-only, no claims ----
    out["companions"] = {
        cell: dict(
            episode_recurrence=[x.get("episode_recurrence") for x in out["cells"][cell]["per_seed"]
                                if x.get("converted")],
            last_episode_end_t=[x.get("last_episode_end_t") for x in out["cells"][cell]["per_seed"]
                                if x.get("converted")],
            max_run_census=out["cells"][cell]["max_run_census"],
            note="READ-ONLY. No claims. The 500k->1M tail is scored separately (descriptive).")
        for cell in X15_CELLS}
    out["DRAFT_note"] = ("DRAFT — halts here. Routes behind the adversarial refute-default pass; "
                         "NO LENS ASSUMES D>C. Attribution routes to Jason after the panel.")
    out["scope_fence"] = ("No onset re-litigation (EXP14 §10.24 stands regardless). No claim beyond "
                          "durability-by-dose WITHIN the shuffled fabric, at this power and horizon.")
    (OUTDIR / f"exp15_durability_{out_tag}.json").write_text(json.dumps(out, indent=2))
    _print_durability(out)
    return out


def _last_k_false_rate(null_segments, band: float, k: int) -> dict:
    """False rate of the LAST-K-MEAN detector on a null pool. A position counts only if all k
    windows lie inside ONE contiguous null segment — a pooled null built by concatenating masked
    subsequences would otherwise splice non-adjacent windows and manufacture a passing mean."""
    pos, hits = 0, 0
    for seg in null_segments:
        for i in range(len(seg) - k + 1):
            pos += 1
            if sum(seg[i:i + k]) / k >= band:
                hits += 1
    return dict(n_positions=pos, n_hits=hits, false_rate=(hits / pos) if pos else None)


def _null_segments(per_seed_accs: dict, band: float, N: int):
    """Contiguous runs of windows NOT inside an excluded episode (>= N consec >= band)."""
    segs = []
    for accs in per_seed_accs.values():
        m = _episode_mask(accs, band, N)
        cur = []
        for a, e in zip(accs, m):
            if e:
                if cur:
                    segs.append(cur)
                    cur = []
            else:
                cur.append(a)
        if cur:
            segs.append(cur)
    return segs


def sustain_cal(cal_seeds=None, band: float = None, k: int = None, out_tag: str = "exp15") -> dict:
    """EXP15 §6 stage-one sustain-cal — FROM EXISTING TRACES ONLY, no new runs.

    False rate of the last-K-mean sustain detector at the common ruler on
      (i)  the D-null cal pool      (s0-class exclusion: >= EPISODE_BAND for >= EPISODE_MIN)
      (ii) the C-between cal pool   (conversion+shoulder exclusion: >= CONV_LOW for >= CONV_MIN)
    reported against ALPHA. Plus its DESCRIPTIVE behaviour on the committed converter pool
    (last-K-mean vs the old single-endpoint `sustains_to_horizon`) — the B-s6 fragility check."""
    cal_seeds = cal_seeds or CAL_SEEDS
    band = X15_RULER_BAND if band is None else band
    k = X15_K_LAST if k is None else k
    out = dict(band=band, k_last=k, alpha=ALPHA, cal_seeds=cal_seeds, nulls={}, committed={})

    pools = {
        "D_null(s0-class excl)": ("D_split", "cal", EPISODE_BAND, EPISODE_MIN),
        "C_between(conv+shoulder excl)": ("C_shuffle", "cal2", CONV_LOW, CONV_MIN),
    }
    for name, (cell, tag, xb, xn) in pools.items():
        arm = CELLS[cell]["arm"]
        per_seed_accs = {}
        for s in cal_seeds:
            p = OUTDIR / f"exp14_{arm}_s{s}_{tag}.json"
            if not p.exists():
                continue
            per_seed_accs[s] = _post_acq(json.loads(p.read_text()))
        segs = _null_segments(per_seed_accs, xb, xn)
        fr = _last_k_false_rate(segs, band, k)
        fr.update(cell=cell, n_segments=len(segs),
                  n_null_windows=sum(len(x) for x in segs),
                  within_alpha=bool(fr["false_rate"] is not None and fr["false_rate"] <= ALPHA),
                  exclusion=f">= {xb} for >= {xn} consec")
        out["nulls"][name] = fr
    out["locked_state_finding"] = (
        "RULING 1 (Jason 2026-07-10): the locked-state sustain detector is RETIRED as primary. "
        "It returns 0/16 on the committed verdict seeds, and NO bar both controls alpha and "
        "produces sustainers (the alpha-calibrated K=10 bar is 0.79, ABOVE the ruler). That is "
        "itself the finding: LOCKED-STATE SUSTAIN DOES NOT EXIST AT 500k IN THIS REGIME. "
        "Conversion is EPISODIC, so 'held above band at horizon' measures a state the phenomenon "
        "does not occupy. Retained below as a SENSITIVITY level only.")

    # descriptive: the committed converters, last-K-mean vs single-endpoint
    for cell in X15_CELLS:
        arm = CELLS[cell]["arm"]
        b14, n14 = X15_REPRO[cell]["band"], X15_REPRO[cell]["N"]
        rows = []
        for s in X15_REPRO[cell]["converters"]:
            p = OUTDIR / f"exp14_{arm}_s{s}_{verdict_tag_default()}.json"
            if not p.exists():
                continue
            rec = json.loads(p.read_text())
            d = _durability_of_seed(rec, band, X15_RULER_N, k)
            conv = _density_conversion_onset(rec, band, X15_RULER_N)
            runway = (X15_PRIMARY_AT - conv) if conv is not None else None
            rows.append(dict(seed=s, conversion_onset_at_ruler=conv, runway=runway,
                             censored=bool(runway is not None and runway < X15_T_DUR),
                             last_k_mean=d["last_k_mean"], sustains_lastK=d["sustains_lockedstate"],
                             endpoint_acc=d["endpoint_acc"],
                             sustains_endpoint=d["sustains_endpoint"],
                             longest_episode=d["longest_episode"], max_run=d["max_run"],
                             bare_ruler=d["bare_ruler"],
                             frac_q4=d["frac_above_band_final_quartile"]))
        agree = sum(1 for r in rows if r["sustains_lastK"] == r["sustains_endpoint"])
        out["committed"][cell] = dict(
            exp14_band=dict(band=b14, N=n14), rows=rows,
            n_converters=len(rows), n_censored=sum(1 for r in rows if r["censored"]),
            n_sustain_lastK=sum(1 for r in rows if r["sustains_lastK"] and not r["censored"]),
            n_sustain_endpoint=sum(1 for r in rows if r["sustains_endpoint"] and not r["censored"]),
            detectors_agree=f"{agree}/{len(rows)}")
    (OUTDIR / f"exp15_sustain_cal_{out_tag}.json").write_text(json.dumps(out, indent=2))
    print(f"\n=== EXP15 §6 SUSTAIN-CAL (existing traces only) — detector: mean(last {k}) >= {band} ===")
    for name, r in out["nulls"].items():
        print(f"  {name:32s} n_null={r['n_null_windows']:5d} segs={r['n_segments']:3d} "
              f"positions={r['n_positions']:5d} hits={r['n_hits']:3d} "
              f"false_rate={r['false_rate']}  <= alpha({ALPHA})? {r['within_alpha']}")
    for cell, cc in out["committed"].items():
        print(f"\n  {cell} committed converters (n={cc['n_converters']}, censored {cc['n_censored']}): "
              f"sustain lastK {cc['n_sustain_lastK']} vs endpoint {cc['n_sustain_endpoint']}  "
              f"(agree {cc['detectors_agree']})")
        for r in cc["rows"]:
            print(f"     s{r['seed']}: conv@{r['conversion_onset_at_ruler']} runway={r['runway']} "
                  f"{'CENSORED' if r['censored'] else 'eligible'}  last{k}mean={r['last_k_mean']} "
                  f"-> {r['sustains_lastK']}   endpoint={r['endpoint_acc']} -> {r['sustains_endpoint']}"
                  f"   longest_ep={r['longest_episode']}{'  [BARE-RULER]' if r['bare_ruler'] else ''}")
    return out


def verdict_tag_default() -> str:
    return "verdict"


def _print_durability(out: dict) -> None:
    p = out["primary"]
    q0, q1 = out["final_quartile"]
    print(f"\n=== EXP15 DURABILITY-BY-DOSE (DRAFT) — ruler {out['ruler']['band']}x{out['ruler']['N']}, "
          f"T_DUR={out['t_dur']}, dur_min_run={out['dur_min_run']}, primary@{out['primary_at']} ===")
    print(f"    PRIMARY statistic: frac of windows in ({q0},{q1}] with exam_acc >= ruler  "
          f"[scope: {out['primary_scope']}]")
    for cell in X15_CELLS:
        c = out["cells"][cell]
        print(f"\n{cell} [{c['fabric']}x{c['dose']}] {c['arm']}  seeds={c['n_seeds']} READ={c['n_read']}")
        print(f"    converted {c['n_converted']} {c['converter_seeds']}")
        print(f"    DUR-CENSORED {c['n_censored']} {c['censored_seeds']}   "
              f"BARE-N(<{out['dur_min_run']}) {c['n_bare_N']} {c['bare_N_seeds']}   "
              f"ELIGIBLE {c['n_eligible']} {c['eligible_seeds']}")
        print(f"    final-quartile frac: {c['final_quartile_frac']}  mean={c['final_quartile_frac_mean']}")
        g = out["phantom_floor_gate"][cell]
        print(f"    FLOOR GATE: observed {g['observed_converters']} vs expected "
              f"{g['expected_phantom_converters_EPISODE_UNIT']} (episode unit; position unit "
              f"{g['expected_phantom_converters_position_unit']})  P(>=obs)={g['P_observed_or_more_under_floor']}"
              f"  -> {'AT-FLOOR' if g['at_floor'] else 'ABOVE-FLOOR'}")
        print(f"    max-run census: {[(x['seed'], x['max_run']) for x in c['max_run_census']]}")
    print(f"\nPRIMARY  exact MW one-sided (D>C): p={p['p_one_sided_D_gt_C']}   "
          f"(C>D: p={p['p_one_sided_C_gt_D']})   floor_met={p['floor_met']} "
          f"(>= {p['converter_floor']}/cell)")
    print(f"    D mean {p['D']['mean']} (n={p['D']['n_eligible']})   "
          f"C mean {p['C']['mean']} (n={p['C']['n_eligible']})")
    print(f"OUTCOME CELL: {out['outcome_cell']['cell']}")
    print(f"    {out['outcome_cell']['note']}")
    if out["outcome_cell"].get("floor_flag"):
        print(f"    ** {out['outcome_cell']['floor_flag']}")
    print(f"\nSENSITIVITIES (reported, never deciding): {out['sensitivity_note']}")
    for k, v in out["sensitivities"].items():
        print(f"    {k}: p(D>C)={v.get('p_one_sided_D_gt_C')}")
    print(f"\nCONTEXT (committed 16, never primary): {json.dumps(out['context_committed'], indent=6)}")
    print(f"\n{out['locked_state_finding']}")
    print(f"\n{out['DRAFT_note']}")


# ------------------------------------------------------------------ smoke (faithfulness proof)
def smoke():
    torch.set_num_threads(1)
    N = 1200
    arm, seed = "exp12_dwell", 0
    # (1) one code path: step is the inherited Stage0Loop.step (never overridden in exp14)
    assert "run_exp14_arm" in globals()
    # (2) FAITHFUL REPLICA: exp14 at matched horizon reproduces exp12 columns DIGIT-IDENTICALLY
    ref = X12.run_exp12_arm(arm, seed, N, out_tag="exp14smoke_ref")
    got = run_exp14_arm(arm, seed, read_at=N, h_max=N, out_tag="exp14smoke", checkpoint=True)
    assert len(ref["columns"]) == len(got["columns"]), "column count differs from run_exp12_arm"
    for cr, cg in zip(ref["columns"], got["columns"]):
        for k, v in cr.items():
            assert cg.get(k) == v, f"DIVERGENCE at t={cr['t']} key={k}: {cg.get(k)} != {v}"
    assert ref["acquisition_onset"] == got["acquisition_onset"]
    print("SMOKE (1)+(2): run_exp14_arm reproduces run_exp12_arm DIGIT-IDENTICALLY over", N, "steps")
    # (3) checkpoint round-trips: save -> load -> identical operator read
    ckpt_path = OUTDIR / f"exp14_{arm}_s{seed}_exp14smoke.ckpt_read.pt"
    assert ckpt_path.exists(), "read checkpoint not written"
    ck = torch.load(ckpt_path, weights_only=False)
    loop2, _, cfg2 = X12.build_exp12(arm, seed, N)
    loop2.vision.load_state_dict(ck["vision"]); loop2.op.load_state_dict(ck["op"])
    loop2.word.load_state_dict(ck["word"])
    ma, mb = X9._member_set(cfg2)
    r_reload = X12.asg_reads(loop2)["asg_cat"]
    # the live loop from the reproduced run (rebuild + step to N) for comparison
    loop3, _, _ = X12.build_exp12(arm, seed, N)
    for _ in range(N):
        loop3.step(no_word=False)
    r_live = X12.asg_reads(loop3)["asg_cat"]
    assert abs(r_reload - r_live) < 1e-9, f"checkpoint reload asg_cat {r_reload} != live {r_live}"
    assert ck["t"] == N
    print(f"SMOKE (3): checkpoint round-trips (asg_cat reload={r_reload:.6f} == live={r_live:.6f})")
    # (4) coin rung faithfully extendable: build at h_max, step PAST read_at on the SAME perm
    lc, sc, cc = X12.build_exp12("exp12_split", 1, 800)       # h_max fabric = 800
    fc = lc.stream
    assert fc.shuffled and fc.T >= 808
    for _ in range(600):                                     # read_at=600 < h_max=800
        lc.step(no_word=False)
    # extension continues on the SAME pre-built perm (no rebuild, no reshuffle)
    t_before = lc._t
    for _ in range(150):                                    # 600 -> 750, still < fab.T
        lc.step(no_word=False)
    assert lc._t == t_before + 150, "coin rung could not step past read_at on the h_max fabric"
    print("SMOKE (4): coin (shuffled) rung steps past read_at on the pre-built h_max perm")
    # (5) TWO-PASS FIXPOINT NULL (F1) — SUPERSEDED by Ruling A (kept as the mechanism record):
    # 3 clean marginal seeds ~U(0.30,0.62) + 1 seed carrying ONE sub-s0-class conversion (0.66 x 15:
    # value 0.66 in (band, 0.704) and length 15 < ... but ABOVE 0.704x8 in NEITHER value NOR the
    # s0-class run test, so the honest-null BASE misses it). Small-fraction contamination (15/~4000
    # < 1%) so the provisional lands BELOW 0.66 and inflates its N; the fixpoint fires the detector on
    # the episode, excludes it, and TIGHTENS the cut back to the clean marginal. Isolated blips stay.
    import random as _r
    _rng = _r.Random(0)
    def _marg(n):
        return [round(0.30 + 0.32 * _rng.random(), 3) for _ in range(n)]   # U(0.30,0.62)
    per_seed = {i: _marg(1200) for i in range(3)}                          # 3600 clean marginal
    contam = _marg(600)
    contam = contam[:300] + [0.66] * 15 + contam[300:]                     # sub-s0 conversion 0.66x15
    per_seed[3] = contam
    res = _twopass_cut(per_seed)
    assert res["converged"], f"two-pass did not converge: {res['trace']}"
    pb, pN = res["provisional"]; fb, fN = res["fixpoint"]
    # the episode fires the FIXPOINT detector (contamination made legible) ...
    assert any(_episode_mask(contam, fb, fN)), "fixpoint detector fails to fire on the planted episode"
    # ... and the fixpoint null DROPPED it (the honest-null base did not) — strict shrink
    assert len(res["final_null"]) < len(res["prov_null"]), "fixpoint null did not shrink"
    # ... and the fixpoint is no LOOSER than the provisional (deflation/hold, never inflation)
    assert fb <= pb and fN <= pN, f"two-pass loosened the cut: {(pb, pN)} -> {(fb, fN)}"
    clean = _twopass_cut({0: _marg(1200)})                                 # pure marginal control
    assert clean["converged"], "two-pass diverged on a clean marginal null"
    print(f"SMOKE (5): two-pass fixpoint null [SUPERSEDED] — provisional {pb}x{pN} -> fixpoint {fb}x{fN} "
          f"(null {len(res['prov_null'])}->{len(res['final_null'])}); planted 0.66x15 caught + deflated")
    # (5b) RULING B borrow-gate: donor marginal ~U(0.30,0.62); a MATCHED cell (same law) borrows;
    # a SHIFTED cell (law bumped +0.05) does not. The band is a high-tail statistic, so a small
    # baseline shift trips the gate (fr of donor band on the shifted cell's between-episode > 2*alpha).
    donor = {i: _marg(1200) for i in range(3)}
    _, _, donor_null = _provisional_cut(donor)
    donor_band = _joint_band_cut(donor_null)
    matched_between = _marg(1600)                                         # same law -> should borrow
    shifted_between = [round(a + 0.05, 3) for a in _marg(1600)]           # baseline bumped -> should not
    g_match = _borrow_gate(donor_band, donor_null, matched_between)
    g_shift = _borrow_gate(donor_band, donor_null, shifted_between)
    assert g_match["borrow_ok"], f"borrow-gate rejected a matched cell: {g_match}"
    assert not g_shift["borrow_ok"], f"borrow-gate accepted a shifted cell: {g_shift}"
    print(f"SMOKE (5b): borrow-gate — matched cell borrow_ok={g_match['borrow_ok']} (shift {g_match['mean_shift']}), "
          f"shifted cell borrow_ok={g_shift['borrow_ok']} (shift {g_shift['mean_shift']})")
    # (6) attribution table is exhaustive + exclusive over all 16 convert-subsets (pure fn)
    seen_attr = {}
    for mask in range(16):
        cv = {L for i, L in enumerate("ABCD") if mask & (1 << i)}
        a = _attribution_from_convertset(cv)["attribution"]
        seen_attr[frozenset(cv)] = a
    assert seen_attr[frozenset()] == "INSTRUMENT_REGRESSION"
    assert seen_attr[frozenset({"D"})] == "INTERACTION"
    assert seen_attr[frozenset({"D", "B"})] == "DOSE_MAIN_EFFECT"
    assert seen_attr[frozenset({"D", "C"})] == "FABRIC_MAIN_EFFECT"
    assert seen_attr[frozenset({"D", "B", "C"})] == "BOTH_MAIN_EFFECTS_ADDITIVE"
    assert all(seen_attr[k] == "ANOMALY" for k in seen_attr if "A" in k)
    assert len(seen_attr) == 16 and all(v for v in seen_attr.values())
    print("SMOKE (6): 2x2 attribution table exhaustive+exclusive over 16 subsets (scorer NOT run)")

    # ================= EXP15 additions (7)-(11) =================
    # (7) spec_hash DRIFT ASSERT — the new `mid_ckpt_at` parameter must NOT enter the hashed
    #     payload, or F2 parity across reused (EXP14) + new (EXP15) runs breaks by construction.
    #     Catch payload drift NOW, not post-GO with 40 runs already carrying it.
    COMMITTED_SPEC_HASH = "41d6f0d5e7da"
    assert C.spec_hash() == COMMITTED_SPEC_HASH, \
        (f"SPEC_HASH DRIFT: {C.spec_hash()} != committed {COMMITTED_SPEC_HASH}. The EXP15 scoring "
         f"constants or mid_ckpt_at leaked into the hashed payload -> F2 parity would break "
         f"across reused+new cells. Fix the payload, do NOT re-pin the hash.")
    got_a2 = run_exp14_arm(arm, seed, read_at=N, h_max=2 * N, out_tag="exp15smoke_a2",
                           checkpoint=True, mid_ckpt_at=N // 2)
    assert got_a2["spec_hash"] == COMMITTED_SPEC_HASH, \
        f"a mid_ckpt_at run emits spec_hash {got_a2['spec_hash']} != {COMMITTED_SPEC_HASH}"
    print(f"SMOKE (7): spec_hash stable at {COMMITTED_SPEC_HASH} with mid_ckpt_at set (no payload drift)")

    # (8) D-row logic: exact-reproduction at 4/8 must NOT read as INSTRUMENT_REGRESSION.
    d_exact = sorted(X15_REPRO["D_split"]["converters"])
    assert (sorted(d_exact) == d_exact) and len(d_exact) == 4 < COUNT_CUTS["across_seeds"], \
        "the committed D set is 4/8 — below the count-cut — which is exactly the mislabel"
    assert _classify_count(len(d_exact)) == "AMBIGUOUS", "D at 4/8 classifies AMBIGUOUS (the trap)"
    #  old wiring would have excluded D -> convert-set {B,C} -> INSTRUMENT_REGRESSION
    assert _attribution_from_convertset({"B", "C"})["attribution"] == "INSTRUMENT_REGRESSION"
    #  fixed wiring keys on the reproduction check: D enters -> the real row is reachable
    assert _attribution_from_convertset({"C", "D"})["attribution"] == "FABRIC_MAIN_EFFECT"
    assert _attribution_from_convertset({"B", "C", "D"})["attribution"] == "BOTH_MAIN_EFFECTS_ADDITIVE"
    print("SMOKE (8): D-row keys on reproduction, not count_class (old 4/8->AMBIGUOUS mislabel caught)")

    # (9) A2 round-trip: run-to-2N with mid_ckpt_at=N  ==  run-to-N, digit-exact on the prefix.
    base_a2 = OUTDIR / f"exp14_{arm}_s{seed}_exp15smoke_a2"
    got_short = run_exp14_arm(arm, seed, read_at=N // 2, h_max=2 * N, out_tag="exp15smoke_short",
                              checkpoint=True)
    npref = len(got_short["columns"])
    for i in range(npref):
        assert got_a2["columns"][i] == got_short["columns"][i], \
            f"A2 prefix diverges at column {i}: mid_ckpt_at changed the trajectory"
    mid = torch.load(base_a2.with_suffix(".ckpt_mid.pt"), weights_only=False)
    shortckpt = torch.load(
        (OUTDIR / f"exp14_{arm}_s{seed}_exp15smoke_short").with_suffix(".ckpt_read.pt"),
        weights_only=False)
    assert mid["t"] == shortckpt["t"] == N // 2, "mid checkpoint is not at the requested step"
    for k in ("vision", "word", "op"):
        for pk in mid[k]:
            assert torch.equal(mid[k][pk], shortckpt[k][pk]), \
                f"mid-horizon checkpoint state[{k}][{pk}] != the read-at-N state (A2 not inert)"
    assert torch.equal(mid["gen_state"], shortckpt["gen_state"]), "RNG state diverged"
    print(f"SMOKE (9): run-to-2N/mid-ckpt-at-N == run-to-N, digit-exact ({npref} cols + RNG + params)")

    # (10) score_durability under RULINGS 1-3, on SYNTHETIC records. No files, no runs — pure logic.
    def _rec(onset, series, t0=None):
        t0 = onset if t0 is None else t0
        return dict(acquisition_onset=onset,
                    columns=[dict(t=t0 + i * EVAL, exam_acc=a) for i, a in enumerate(series)])
    B_, K_, RN_ = X15_RULER_BAND, X15_K_LAST, X15_RULER_N
    lo, hi = 0.30, 0.95

    # (10a) EXACT Mann-Whitney: verified against hand-computed exact tails.
    #   fully separated 2v2: only 1 of C(4,2)=6 assignments reaches W_obs -> p = 1/6
    assert abs(_exact_rank_sum_p([3, 4], [1, 2]) - 1 / 6) < 1e-12
    assert abs(_exact_rank_sum_p([1, 2], [3, 4]) - 1.0) < 1e-12       # fully reversed -> p=1
    assert abs(_exact_rank_sum_p([1, 2, 3], [1, 2, 3]) - _exact_rank_sum_p([1, 2, 3], [1, 2, 3])) < 1e-15
    assert _exact_rank_sum_p([], [1, 2]) == 1.0 and _exact_rank_sum_p([1], []) == 1.0
    #   all ties -> every assignment gives the same rank-sum -> p = 1
    assert abs(_exact_rank_sum_p([5, 5, 5], [5, 5, 5]) - 1.0) < 1e-12
    #   tie-aware midranks: [2,2] pooled with [1,3] -> midranks 1,2.5,2.5,4
    assert _midranks_doubled([1, 2, 2, 3]) == [2, 5, 5, 8]
    #   brute-force cross-check on a random-ish tied sample (deterministic literals, no RNG)
    from itertools import combinations as _combs
    _x, _y = [0.5, 0.5, 0.9, 0.2], [0.1, 0.5, 0.3]
    _pool = _x + _y
    _srt = sorted(_pool)
    _dbl = _midranks_doubled(_srt)
    _rk = {v: r for v, r in zip(_srt, _dbl)}
    _w = sum(_rk[v] for v in _x)
    _tot = _ge = 0
    for _idx in _combs(range(len(_pool)), len(_x)):
        _tot += 1
        if sum(_rk[_pool[i]] for i in _idx) >= _w:
            _ge += 1
    assert abs(_exact_rank_sum_p(_x, _y) - _ge / _tot) < 1e-12, "exact MW != brute-force enumeration"
    #   the 4v4 committed-context shape must be reachable and match a hand tail
    assert 0.0 < _exact_rank_sum_p([0.9, 0.8, 0.7, 0.6], [0.5, 0.4, 0.3, 0.2]) <= 1 / 70 + 1e-12

    # (10b) PRIMARY statistic = ABSOLUTE final-quartile window, not a fraction of the post-acq span.
    #   Build a run whose post-acq span starts at 3000 and reaches 500000 (EVAL=300).
    n_win = (X15_PRIMARY_AT - 3000) // EVAL + 1
    #   all-low then all-high over exactly the final quartile
    ser = []
    for i in range(n_win):
        t = 3000 + i * EVAL
        ser.append(hi if t > X15_FINAL_Q_FROM else lo)
    r_late = _rec(3000, ser)
    d = _durability_of_seed(r_late, B_, RN_, K_)
    assert d["frac_above_band_final_quartile"] == 1.0, d["frac_above_band_final_quartile"]
    assert d["final_quartile_windows"] == sum(1 for i in range(n_win)
                                              if X15_FINAL_Q_FROM < 3000 + i * EVAL <= X15_PRIMARY_AT)
    #   the mirror: high early, floor late -> primary reads 0 even though it converted hard
    ser2 = [hi if 3000 + i * EVAL <= X15_FINAL_Q_FROM else lo for i in range(n_win)]
    d2 = _durability_of_seed(_rec(3000, ser2), B_, RN_, K_)
    assert d2["frac_above_band_final_quartile"] == 0.0 and d2["longest_episode"] > 100
    assert d2["dur_pool_ok"], "a long-episode decayer is ELIGIBLE (it decayed; it is not a phantom)"

    # (10c) RULING 3 eligibility: longest-run >= 8 gates the DURABILITY POOL, not the converter count.
    ph = _rec(3000, [lo] * 20 + [hi] * 5 + [lo] * 75)          # bare-N phantom: run of exactly 5
    d = _durability_of_seed(ph, B_, RN_, K_)
    assert d["longest_episode"] == 5 and d["max_run"] == 5
    assert (not d["dur_pool_ok"]) and d["bare_ruler"], "a 5-run must be BARE-N, out of the pool"
    real = _rec(3000, [lo] * 20 + [hi] * 8 + [lo] * 72)        # exactly at the gate
    d = _durability_of_seed(real, B_, RN_, K_)
    assert d["longest_episode"] == 8 and d["dur_pool_ok"] and not d["bare_ruler"], \
        "longest-run == EPISODE_MIN must ENTER the pool (>=, not >)"
    assert X15_DUR_MIN_RUN == EPISODE_MIN == 8, "the gate must reuse the house constant, not a new one"
    #   set-preserving on committed data: every committed converter's longest run >= 8 (census 21..90)
    for cell, meta in (("C_shuffle", X15_REPRO["C_shuffle"]), ("D_split", X15_REPRO["D_split"])):
        for s in meta["converters"]:
            p = OUTDIR / f"exp14_{CELLS[cell]['arm']}_s{s}_verdict.json"
            if p.exists():
                v = _post_acq(json.loads(p.read_text()))
                assert _longest_episode(v, B_, RN_) >= X15_DUR_MIN_RUN, \
                    f"{cell} s{s}: the Ruling-3 gate is NOT set-preserving on committed data"

    # (10d) censoring boundary: runway exactly T_DUR enters; one step less is censored
    assert ("DUR-CENSORED" if X15_T_DUR - 1 < X15_T_DUR else "ELIGIBLE") == "DUR-CENSORED"
    assert ("DUR-CENSORED" if X15_T_DUR < X15_T_DUR else "ELIGIBLE") == "ELIGIBLE"

    # (10e) retired forms still computable as SENSITIVITIES, and the B-s6 fragility still exposed
    frag = _rec(3000, [lo] * 10 + [hi] * 40 + [lo] * 49 + [hi])
    d = _durability_of_seed(frag, B_, RN_, K_)
    assert d["sustains_endpoint"] and not d["sustains_lockedstate"], \
        "single-endpoint calls a decayed run sustained; locked-state must not"

    # (10f) outcome cells: reachable, mutually exclusive, floor checked FIRST
    def _cellof(xd, xc, floor=X15_CONV_FLOOR):
        if not (len(xd) >= floor and len(xc) >= floor):
            return "UNDERPOWERED"
        if _exact_rank_sum_p(xc, xd) <= X15_ALPHA_P:
            return "INVERTED"
        if _exact_rank_sum_p(xd, xc) <= X15_ALPHA_P:
            return "PROMOTED"
        return "NOT-PROMOTED-AT-POWER"
    hi12 = [0.60 + 0.01 * i for i in range(12)]
    lo12 = [0.10 + 0.01 * i for i in range(12)]
    assert _cellof(hi12, lo12) == "PROMOTED"
    assert _cellof(lo12, hi12) == "INVERTED"
    mid12 = [0.30 + 0.01 * i for i in range(12)]
    assert _cellof(mid12, list(mid12)) == "NOT-PROMOTED-AT-POWER"
    assert _cellof(hi12[:4], lo12[:4]) == "UNDERPOWERED"          # floor unmet dominates
    assert _cellof(hi12, lo12, floor=99) == "UNDERPOWERED"        # floor is checked FIRST

    # (10g) seed pool: RULING 2 repair -> audit is CLEAN
    assert X15_RESERVE_POOL[:2] == [40, 41] and len(X15_RESERVE_POOL) == X15_RESERVE_CAP
    audit = seed_pool_audit()
    _print_seed_audit(audit)
    assert audit["clean"] and not audit["blockers"], f"seed pool must be clean: {audit['blockers']}"
    assert audit["cal_collision"] == [] and audit["known_defective_in_pool"] == []
    assert X15_NEW_SEEDS == list(range(8, 20)) + list(range(28, 36))
    assert X15_SUBST_POOL == [36, 37, 38, 39]
    assert set(X15_NEW_SEEDS).isdisjoint(CAL_SEEDS) and 23 not in X15_NEW_SEEDS
    #  and the primary still REFUSES while the 40 runs do not exist (they are WITHHELD)
    try:
        score_durability(require_new=True)
        raise SystemExit("score_durability did NOT refuse with the 40 runs absent")
    except AssertionError as e:
        assert "REFUSED" in str(e) and "WITHHELD" in str(e), f"unexpected assertion: {e}"
    print("SMOKE (10): score_durability — exact MW (vs brute force + hand tails), absolute "
          "final-quartile window, Ruling-3 pool gate (set-preserving on committed data), censor "
          "boundary, 4 outcome cells; seed pool CLEAN; primary refuses (runs withheld)")

    # (11) sustain-cal unit: planted null vs planted sustainer; contiguity respected.
    seg_null = [[0.30 + 0.02 * (i % 5) for i in range(200)]]
    r = _last_k_false_rate(seg_null, B_, K_)
    assert r["n_hits"] == 0 and r["n_positions"] == 200 - K_ + 1
    seg_sust = [[0.95] * 40]
    r = _last_k_false_rate(seg_sust, B_, K_)
    assert r["n_hits"] == 40 - K_ + 1 and r["false_rate"] == 1.0
    #  splice guard: two short segments that would pass ONLY if concatenated
    spliced = [[0.95] * 5, [0.95] * 5]
    r = _last_k_false_rate(spliced, B_, K_)
    assert r["n_positions"] == 0 and r["n_hits"] == 0, \
        "last-K must never span a null-segment boundary (splicing manufactures sustain)"
    segs = _null_segments({0: [0.9] * 10 + [0.3] * 5 + [0.9] * 10}, 0.704, 8)
    assert [len(s) for s in segs] == [5], "episode-exclusion must leave only the between-episode run"
    print("SMOKE (11): sustain-cal — null/sustainer detectors, splice guard, segment exclusion")

    # (12) RULING 3 coded floor gate: episode unit != position unit; census is bimodal on committed
    #      data; the gate runs on real artifacts and its verdict is derivable by hand.
    def _tag_committed(_s):
        return "verdict"
    gates = {c: phantom_floor_gate(c, VERDICT_SEEDS, _tag_committed, X15_RULER_BAND, X15_RULER_N)
             for c in X15_CELLS}
    for c, g in gates.items():
        assert g["expected_phantom_converters_EPISODE_UNIT"] <= \
               g["expected_phantom_converters_position_unit"] + 1e-9, \
            "the position unit must never UNDER-count episodes (it overcounts by cluster size)"
        assert g["converter_seeds"] == sorted(X15_REPRO[c]["converters"]), \
            f"{c}: floor gate must see the committed converter set, got {g['converter_seeds']}"
        assert g["observed_converters"] == len(X15_REPRO[c]["converters"])
        runs = sorted(x["max_run"] for x in g["bare_N_census"])
        noise = [r for r in runs if r < X15_RULER_N]
        conv = [r for r in runs if r >= X15_DUR_MIN_RUN]
        assert not [r for r in runs if X15_RULER_N <= r < X15_DUR_MIN_RUN], \
            f"{c}: committed census must have an EMPTY [N, EPISODE_MIN) band, got {runs}"
        assert max(noise) < X15_RULER_N <= min(conv), f"{c}: census not bimodal: {runs}"
    #  the whole point of the gate: D is ABOVE its floor, C is AT its floor (count carries no signal)
    assert not gates["D_split"]["at_floor"], "D's crossing count should clear its floor"
    assert gates["C_shuffle"]["at_floor"], \
        "C's crossing count sits AT its floor — the gate must flag it (C is carried by run length)"
    print(f"SMOKE (12): floor gate — D obs {gates['D_split']['observed_converters']} vs floor "
          f"{gates['D_split']['expected_phantom_converters_EPISODE_UNIT']} ABOVE; "
          f"C obs {gates['C_shuffle']['observed_converters']} vs floor "
          f"{gates['C_shuffle']['expected_phantom_converters_EPISODE_UNIT']} AT-FLOOR (flagged); "
          f"census bimodal, [5,8) empty")
    print("SMOKE OK (12/12)")


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ARM", "SEED"))
    ap.add_argument("--read-at", type=int, default=READ_AT)
    ap.add_argument("--h-max", type=int, default=None)
    ap.add_argument("--out-tag", type=str, default=None)
    ap.add_argument("--cut-band", action="store_true")
    ap.add_argument("--cal-tag", type=str, default="cal")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--verdict-tag", type=str, default="verdict")
    # --- 2x2 deconfound (steps 1->2) ---
    ap.add_argument("--precheck", type=str, metavar="ARM", help="step 1: fabric pre-check an arm")
    ap.add_argument("--precheck-t", type=int, default=15_000)
    ap.add_argument("--cut-band-2x2", action="store_true", help="step 2: two-pass 4-cell band cut")
    ap.add_argument("--band-2x2-tag", type=str, default="2x2_cal")
    ap.add_argument("--score-2x2", action="store_true", help="VERDICT-STAGE (guarded; withheld)")
    ap.add_argument("--release-verdict", action="store_true", help="override the verdict-withhold")
    ap.add_argument("--dry", action="store_true", help="score without overwriting committed artifacts")
    # --- EXP15 durability-by-dose (build stage; the 40 runs are WITHHELD) ---
    ap.add_argument("--mid-ckpt-at", type=int, default=None, help="A2: extra .pt mid-run (inert)")
    ap.add_argument("--repro-check", action="store_true", help="EXP15 §5a reproduction check")
    ap.add_argument("--sustain-cal", action="store_true", help="EXP15 §6 (existing traces only)")
    ap.add_argument("--score-durability", action="store_true", help="EXP15 primary (guarded)")
    ap.add_argument("--release-durability", action="store_true",
                    help="override the EXP15 run-withhold (only after Jason's GO)")
    ap.add_argument("--new-tag", type=str, default="exp15")
    args = ap.parse_args()
    torch.set_num_threads(1)                                  # the determinism contract
    if args.smoke:
        smoke()
    elif args.precheck:
        precheck_fabric(args.precheck, T=args.precheck_t)
    elif args.run:
        run_exp14_arm(args.run[0], int(args.run[1]),
                      read_at=args.read_at, h_max=args.h_max, out_tag=args.out_tag,
                      mid_ckpt_at=args.mid_ckpt_at)
    elif args.repro_check:
        reproduction_check(verdict_tag=args.verdict_tag)
    elif args.sustain_cal:
        sustain_cal()
    elif args.score_durability:
        if not args.release_durability:                        # brief scope: build stage ONLY
            print("EXP15 RUNS WITHHELD (brief scope: build + pre-check + cal). score_durability is "
                  "BUILT but not exercised until Jason's GO. Pass --release-durability to override.")
        else:
            score_durability(verdict_tag=args.verdict_tag, new_tag=args.new_tag)
    elif args.cut_band:
        cut_conv_band(out_tag=args.cal_tag)
    elif args.cut_band_2x2:
        cut_conv_band_2x2(out_tag=args.band_2x2_tag)
    elif args.score:
        score_exp14(cal_tag=args.cal_tag, verdict_tag=args.verdict_tag)
    elif args.score_2x2:
        if not args.release_verdict:                          # brief scope: steps 1->2 ONLY
            print("VERDICT WITHHELD (brief scope: steps 1->2). score_2x2 is BUILT but not exercised "
                  "until Jason releases the verdict. Pass --release-verdict to override.")
        else:
            score_2x2(cal_tag=args.band_2x2_tag, verdict_tag=args.verdict_tag,
                      write=not args.dry)


if __name__ == "__main__":
    _main()
