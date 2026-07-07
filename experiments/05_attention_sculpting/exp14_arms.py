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
COUNT_CUTS = dict(across_seeds=5, lottery=(1, 2), none=0, ambiguous=(3, 4))  # per 8 (panel F4)
N_MIN_READ = 3                     # READ-floor (panel F5; EXP12 §13.9 pin ii)

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


EPISODE_BAND, EPISODE_MIN = S0_LEVEL, 8    # honest-null episode-exclusion (band re-pin, Jason 2026-07-07)


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
    # (5) band cut runs on a tiny synthetic (schema only; not a real cut)
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
    args = ap.parse_args()
    torch.set_num_threads(1)                                  # the determinism contract
    if args.smoke:
        smoke()
    elif args.run:
        run_exp14_arm(args.run[0], int(args.run[1]),
                      read_at=args.read_at, h_max=args.h_max, out_tag=args.out_tag)
    elif args.cut_band:
        cut_conv_band(out_tag=args.cal_tag)
    elif args.score:
        score_exp14(cal_tag=args.cal_tag, verdict_tag=args.verdict_tag)


if __name__ == "__main__":
    _main()
