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
                  checkpoint: bool = True) -> dict:
    """Faithful replica of exp12_arms.run_exp12_arm (verified digit-identical in smoke), with
    the fabric pre-built at `h_max` and reads/checkpoints at `read_at`."""
    h_max = h_max or read_at
    assert read_at <= h_max, "read_at must be <= h_max (fabric is pre-built to h_max)"
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
        eval_cadence=EVAL, block_cadence=BLOCK,
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


def precheck_fabric(arm: str, seeds=None, T: int = 15_000, out_tag: str = "precheck") -> dict:
    """STEP 1 (§7.1): fabric-assert the verdict seeds OUTCOME-BLIND; swap any defective from the
    EXT_POOL-then-higher pool (the ruled cal-s23->s25 substitution rule), recording each swap."""
    seeds = list(seeds if seeds is not None else VERDICT_SEEDS)
    swap_pool = [s for s in (EXT_POOL + list(range(10, 40))) if s not in seeds]
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


def score_2x2(cal_tag: str = "2x2_cal", verdict_tag: str = "verdict") -> dict:
    """DRAFT 4-cell attribution (§5) — VERDICT-STAGE. pre-gate A (READ=acquired) -> pre-gate B
    (F6 budget) -> conversion (per-cell fixpoint band, sustained-episode) -> F5 power gate ->
    attribution + factorial. DRAFT: routes behind the adversarial pass before the table reaches
    Jason. NOT run in the cal phase (verdict withheld)."""
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
            per_seed.append(dict(seed=s, status=st, acquisition_onset=onset,
                                 conversion_onset=conv, converted=bool(conv is not None)))
        read = [x for x in per_seed if x["status"] == "READ"]
        conv = [x for x in read if x["converted"]]
        # pin-2 liveness (B only): a non-acquiring 12bc_dwp cell is UNREAD, never "no conversion"
        liveness_ok = True
        if cell == "B_12bc_dwp":
            liveness_ok = band["cells"][cell]["liveness"]["live"] and len(read) >= N_MIN_READ
        kcls = _classify_count(len(conv))
        if cell in ("B_12bc_dwp", "C_shuffle") and kcls in ("s0-class-lottery", "AMBIGUOUS"):
            ext_needed.append(cell)                              # F5 power gate -> EXT_POOL
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
                                  cell_status=cell_status, liveness_ok=liveness_ok, per_seed=per_seed)
    attrib = _attribution_from_convertset(converts)
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
    (OUTDIR / f"exp14_2x2_verdict_{verdict_tag}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: v for k, v in out.items() if k != "cells"}, indent=2))
    return out


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
    print("SMOKE OK")


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
    args = ap.parse_args()
    torch.set_num_threads(1)                                  # the determinism contract
    if args.smoke:
        smoke()
    elif args.precheck:
        precheck_fabric(args.precheck, T=args.precheck_t)
    elif args.run:
        run_exp14_arm(args.run[0], int(args.run[1]),
                      read_at=args.read_at, h_max=args.h_max, out_tag=args.out_tag)
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
            score_2x2(cal_tag=args.band_2x2_tag, verdict_tag=args.verdict_tag)


if __name__ == "__main__":
    _main()
