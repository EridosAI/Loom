"""EXP12 — scene persistence: the rig-1 loop (A-DWELL / A-SHUFFLE), reads, runner, and
the stage-one calibrator.

Pre-registration: docs/EXP12_SCENE_PERSISTENCE_PREREG.md (RATIFIED 2026-07-04). Build
handoff: docs/HANDOFF_CC_exp12_build.md. ARMS DO NOT RUN AT VERDICT until the stage-two
calibration constants are recorded (§13.4–5); this module runs stage-one only.

THE GEOMETRY (§3, ratified): WAVE-LOCAL completion — cfg.W = 1, one wave = [vision ;
word-anchor slot], EXACTLY one slot masked per wave by the fabric's harness-side
schedule (via the existing `force_mask`-style path: `sample_mask_grid` is never drawn).
This is what makes A-SHUFFLE a pure gradient-REORDERING control: the multiset of
per-wave training examples (stimulus + mask) is IDENTICAL across arms; only exposure
order differs.

Consequences of the wave-local pin, surfaced (not silent patches):
  * L_JEPA is INERT by construction (the within-window pair loop is empty at W=1) — the
    term stays in the code path, untouched; note this also idles the one next-wave
    prediction component of the deployed loss (consistent with the anti-forward guard).
  * The drift/nuisance u-carrier injection is NOT applied to the presented cells: it
    carried WITHIN-WINDOW order (exp03 order-as-content), which does not exist at W=1;
    cross-wave order enters ONLY through the fabric's stimulus dynamics ("time is felt,
    not coded"). The codebook is still built (construction order untouched).
  * The EXP10 word jiggle is NOT carried: the prereg's fabric (§1) enumerates member
    nuisance + background only; the anchor presents clean (deployed frozen centroids).

Division of labor (§3, binding): onset waves = ROUTING EXAMS (the verdict axis);
mid-dwell vision-masked waves = the TEACHING CHANNEL; mid-dwell word-masked waves =
recency-inflated companion ONLY. Onset completion is never teaching evidence; mid-dwell
completion is never routing evidence.

Columns: the EXP08 standing 16-probe set verbatim (num/den/ratio, proto, d2_*, asg_*)
+ the Amendment-B verdict-designate `asg_cat` (category-partition input-sensitivity:
L1 distance between the two category-conditioned MEAN soft-assignment vectors over the
16 clean probes; 16-member asg_dist rides as companion only) + the per-wave-buffered
window means (exam lift/acc, probe-exam lift, mid-dwell companions, earned-salience
divergence splits, per-dwell-position error curve).

Determinism: seed + construction order + torch threads = 1 (recorded). The fabric is
pre-generated on dedicated substreams; build_cells consumes ZERO loop.gen draws, so the
per-step loop.gen sequence (spread batches) is bit-identical across arms at a seed.
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

import constants                                              # noqa: E402
import exp07_config as C                                      # noqa: E402
import exp08_arms as A                                        # noqa: E402
import exp09_arms as X9                                       # noqa: E402
import exp10_arms as X10                                      # noqa: E402
import exp12_fabric as F                                      # noqa: E402
from loom import poolmetrics                                  # noqa: E402
from loom.completion import apply_slice_mask                  # noqa: E402
from revival import partition_read, dynamics_panel            # noqa: E402
from sculpt_config import SculptConfig                        # noqa: E402

OUTDIR = A.OUTDIR
EVAL, BLOCK = A.EVAL, A.BLOCK

# --- §13.9 seeds / horizons ---
CAL_SEEDS = [20, 21, 22, 23, 24]     # stage-one/two calibration — never verdict
VERDICT_SEEDS = [0, 1, 2, 3, 4]
EXT_POOL = [5, 6]                    # margin-guard +2 extension pool
CAL_HORIZON = 160000                 # corrected-law re-cal ceiling (Ruling 1 cascade: the
                                     # stale-law 120k bound is DISCARDED; ~3x the stale max
                                     # onset, censoring-aware — a censored cal seed makes the
                                     # §13.9 onset bound a >=, never a max). The VERDICT
                                     # horizon comes from the re-cal onsets (§13.9)
PROBE_RATE_STAGE1 = 0.0              # boundary-leak probe-dwell rate is a STAGE-TWO constant;
                                     # machinery smoke-tested at a nonzero rate, run at 0 here

ARMS12 = {
    "exp12_dwell":   dict(shuffled=False),
    "exp12_shuffle": dict(shuffled=True),
}

POS_BUCKETS = ((1, 1), (2, 2), (3, 3), (4, 6), (7, 12), (13, 48))


def _pos_bucket(p: int) -> str:
    for lo, hi in POS_BUCKETS:
        if lo <= p <= hi:
            return f"p{lo}" if lo == hi else f"p{lo}-{hi}"
    return "p?"


# ------------------------------------------------------------------ the loop
class EXP12Loop(A.EXP08Loop):
    """EXP08Loop on the scene-persistence fabric: wave-local build_cells driven by the
    pre-generated wave list; dynamics (step/losses/optimizer) inherited UNCHANGED —
    step() is still Stage0Loop.step (asserted in smoke). The prediction of each training
    forward is stashed (detached) for the per-wave reads; no new loss, no new force."""

    def _make_stream(self):
        cfg = self.cfg
        v = getattr(cfg, "_exp12", None)
        assert v is not None, "EXP12Loop needs cfg._exp12 (fabric params) before factories"
        return F.build_fabric(self.stim, cfg, cfg.seed, v["T"],
                              probe_rate=v.get("probe_rate", 0.0),
                              shuffled=v.get("shuffled", False))

    def _make_stim(self):
        cfg = self.cfg
        fam = F.family()
        return F.EXP12Stimulus(
            cfg.D, cfg.n_A, cfg.n_distractor, cfg.n_category,
            R_coarse=cfg.R_coarse, r_distractor=cfg.r_distractor,
            r_category=cfg.r_category, sigma=cfg.sigma_stim, seed=cfg.seed,
            coeff_std=fam["coeff_std"], probe_seed=F.SEED_PROBE_RAW + cfg.seed)

    def build_cells(self, t, *, no_word, gen, ablate="none", force_mask=None):
        cfg = self.cfg
        fab = self.stream
        assert t < fab.T, f"fabric exhausted at t={t} (T={fab.T}) — no wraparound in continual time"
        raw = fab.raw[t:t + 1]                                # (1, D) precomputed wave
        e_vis = self.vision.emit(raw)                         # (1, D) plastic, grad
        wl = fab.cat[t:t + 1]
        tokens = torch.tensor([self.curric.word_token(int(wl[0]), no_word=no_word)])
        e_word = self._vary_word(self.word.emit(tokens), tokens)   # identity hook (no jiggle)
        content = torch.stack([e_vis, e_word], dim=1)         # (1, n_slots, D)
        if force_mask is None:
            mask = torch.zeros(1, cfg.n_slots, dtype=torch.bool)
            mask[0, int(fab.mask_slot[t])] = True
            fam_name = ("exam" if bool(fab.is_exam[t])
                        else ("mid_word" if int(fab.mask_slot[t]) == 1 else "mid_vis"))
            self.mix["n"] += 1
            self.mix["vis_masked"] += int(int(fab.mask_slot[t]) == 0)
            self.mix["word_visible"] += int(int(fab.mask_slot[t]) == 0)
            self.mix["sib_visible"] += 0                      # no sibling wave at W=1
            self.mix["both"] += 0
        else:
            mask, fam_name = force_mask, "forced"
        masked = apply_slice_mask(self._pose_pam_input(content), mask, self.op.mask_emb)
        # NO u-carrier injection (wave-local; order enters via the fabric's dynamics only)
        Ccells = cfg.W * cfg.n_slots
        return dict(
            cells=masked.reshape(Ccells, cfg.D),
            target=self._pam_target(content).reshape(Ccells, cfg.D),
            mask=mask.reshape(Ccells), visible=(~mask).reshape(Ccells),
            fam=fam_name, raw=raw, drift_w=torch.zeros(cfg.W),
            dwell=fab.dwell_id[t:t + 1], e_vis=e_vis,
        )

    def _l_pam(self, bc):
        l, pred = super()._l_pam(bc)
        if bc["fam"] != "forced":                             # training waves only
            self._stash = dict(pred=pred.detach(), e_vis=bc["e_vis"].detach(),
                               mask=bc["mask"].clone(), fam=bc["fam"], raw=bc["raw"])
        return l, pred

    def evoke_vision(self, a_idx, b_idx, *, mask_wave: int = 0, associative: bool = True,
                     null_word: bool = False) -> torch.Tensor:
        """W=1: the only wave is wave 0 — the inherited default mask_wave=1 would index
        past the window. Same read otherwise (associative = word-channel evocation)."""
        return super().evoke_vision(a_idx, b_idx, mask_wave=0, associative=associative,
                                    null_word=null_word)


# ------------------------------------------------------------------ per-wave reads
@torch.no_grad()
def exam_lift(loop, pred_word: torch.Tensor, cat: int) -> tuple[float, float]:
    """Completion category-lift on the masked word cell: d(pred, wrong) - d(pred,
    correct). The CATEGORY-PRIOR floor is 0 by construction (the deck-mean/word-mean
    prediction is equidistant from the two tokens at symmetric geometry)."""
    emb = loop.word.emit(torch.tensor([0, 1]))
    d = torch.cdist(pred_word.unsqueeze(0), emb)[0]
    lift = float(d[1 - cat] - d[cat])
    return lift, float(lift > 0)


@torch.no_grad()
def onset_divergence(loop, t: int) -> dict:
    """Earned-salience read at a scheduled exam wave (Amendment A; expectation, not a
    gate): read-only vision-masked completion of the SAME wave; residual vs the actual
    vision emission, energy split over the pre-rotation axis blocks (identity /
    nuisance / background). RNG-free (private construction; loop.gen untouched)."""
    st = X9._rng_guard(loop)
    cfg = loop.cfg
    fab = loop.stream
    raw = fab.raw[t:t + 1]
    e_vis = loop.vision.emit(raw)
    tokens = torch.tensor([int(fab.cat[t])])
    e_word = loop.word.emit(tokens)
    content = torch.stack([e_vis, e_word], dim=1)
    mask = torch.zeros(1, cfg.n_slots, dtype=torch.bool)
    mask[0, 0] = True                                         # vision masked, word visible
    masked = apply_slice_mask(loop._pose_pam_input(content), mask, loop.op.mask_emb)
    cells = masked.reshape(cfg.n_slots, cfg.D)
    pred = loop.op(cells.unsqueeze(0), loop.slot_ids, (~mask).reshape(-1))[0]
    r = (pred[0] - e_vis[0]) @ loop.stim.Q                    # residual in pre-rotation coords
    n_id = cfg.n_A + cfg.n_distractor + cfg.n_category
    out = dict(div_id=float(r[:n_id].pow(2).sum()),
               div_nuis=float(r[n_id:n_id + F.K_AXES].pow(2).sum()),
               div_bg=float(r[n_id + F.K_AXES:n_id + F.K_AXES + F.BG_AXES].pow(2).sum()))
    X9._rng_check(loop, st, "onset_divergence")
    return out


@torch.no_grad()
def asg_reads(loop) -> dict:
    """The Amendment-B verdict-designate + companions over the 16 clean probes.
    asg_cat = L1 distance between category-conditioned MEAN soft-assignment vectors
    (the category-partition input-sensitivity; 0 = category-blind assignment)."""
    cfg = loop.cfg
    ma, mb = X9._member_set(cfg)
    p = loop.vision.pool.assign(loop.stim.raw_clean(ma, mb))
    cat = mb % cfg.n_category
    mu0, mu1 = p[cat == 0].mean(0), p[cat == 1].mean(0)
    dm = torch.cdist(p, p, p=1)
    cross = (cat.unsqueeze(0) != cat.unsqueeze(1))
    off = ~torch.eye(p.shape[0], dtype=torch.bool)
    return dict(asg_cat=float((mu0 - mu1).abs().sum()),
                asg_cross_cat=float(dm[cross & off].mean()),
                asg_within_cat=float(dm[(~cross) & off].mean()))


def grad_geometry_split(loop) -> dict:
    """BLOCK-cadence gradient split by SCHEDULED geometry at W=1: teaching geometry
    (vision masked, word visible) vs exam geometry (word masked, vision visible) —
    ||dL_PAM/dDelta2|| each. The wave-local analog of the exp08 word/self split."""
    cfg = loop.cfg
    out = {}
    for name, slot in (("teach_geom", 0), ("exam_geom", 1)):
        m = torch.zeros(1, cfg.n_slots, dtype=torch.bool)
        m[0, slot] = True
        bc = loop.build_cells(loop._t, no_word=False, gen=loop.gen, force_mask=m)
        l_pam, _ = loop._l_pam(bc)
        g = torch.autograd.grad(l_pam, loop.vision.pool.delta2, retain_graph=False,
                                allow_unused=True)[0]
        out[name] = 0.0 if g is None else float(g.norm())
    return out


def grad_decomp_local(loop, no_word: bool) -> dict:
    """Wave-local per-member teaching-gradient decomposition (the EXP09 SS7 observable
    at W=1 geometry): one fixed mask (vision masked, word visible) for every member;
    common vs differential energy of dL/d(e_vis). RNG-free (asserted)."""
    st = X9._rng_guard(loop)
    cfg = loop.cfg
    K = cfg.n_A * cfg.n_B
    ma, mb = X9._member_set(cfg)
    e_vis = loop.vision.emit(loop.stim.raw_clean(ma, mb))
    tokens = (torch.full((K,), loop.word.null_token, dtype=torch.long) if no_word
              else loop._word_label(mb, ma))
    e_word = loop.word.emit(tokens)
    content = torch.zeros(K, cfg.W, cfg.n_slots, cfg.D)
    content[:, :, 0, :] = e_vis.unsqueeze(1)
    content[:, :, 1, :] = e_word.unsqueeze(1)
    mask = torch.zeros(cfg.W, cfg.n_slots, dtype=torch.bool)
    mask[0, 0] = True
    masked = loop._pose_pam_input(content).clone()
    masked[:, mask] = loop.op.mask_emb
    cells = masked.reshape(K, cfg.W * cfg.n_slots, cfg.D)
    pred = loop.op(cells, loop.slot_ids, (~mask).reshape(-1))
    read = pred[:, 0, :]
    loss = (read - e_vis).pow(2).mean()
    g = torch.autograd.grad(loss, e_vis, retain_graph=False)[0]
    gb = g.mean(0)
    common = float(gb.pow(2).sum())
    diff = float((g - gb).pow(2).sum(1).mean())
    X9._rng_check(loop, st, "grad_decomp_local")
    return dict(grad_common=common, grad_diff=diff,
                grad_ratio=(common / diff) if diff > 1e-30 else None)


# ------------------------------------------------------------------ the runner
def build_exp12(arm_name: str, seed: int, steps: int, probe_rate: float = PROBE_RATE_STAGE1):
    spec = ARMS12[arm_name]
    pin = constants.PinnedConstants()
    cfg = SculptConfig(seed=seed)
    cfg.W = 1                                                 # the wave-local pin (§3)
    cfg.T = steps + 8                                         # continual: no wraparound
    cfg._exp12 = dict(T=cfg.T, shuffled=spec["shuffled"], probe_rate=probe_rate)
    loop = EXP12Loop(cfg, pin)
    return loop, spec, cfg


def run_exp12_arm(arm_name: str, seed: int, steps: int, *,
                  probe_rate: float = PROBE_RATE_STAGE1, out_tag: str | None = None) -> dict:
    loop, spec, cfg = build_exp12(arm_name, seed, steps, probe_rate)
    fab = loop.stream

    OUTDIR.mkdir(exist_ok=True)
    # asserts run on the UNSHUFFLED wave order; for A-SHUFFLE rebuild the unshuffled
    # twin (identical waves by construction) and checksum the multisets
    if fab.shuffled:
        fab_plain = F.build_fabric(loop.stim, cfg, seed, fab.T, probe_rate=probe_rate,
                                   shuffled=False)
        assert torch.equal(fab.raw.sort(0).values, fab_plain.raw.sort(0).values), \
            "A-SHUFFLE waves are not the identical multiset"
        assert int(fab.is_exam.sum()) == int(fab_plain.is_exam.sum()), "exam count differs"
        asserts = F.fabric_asserts(fab_plain, cfg)
    else:
        asserts = F.fabric_asserts(fab, cfg)
    man = F.fabric_manifest(fab, loop.stim, cfg, asserts)
    man.update(arm=arm_name, seed=seed, steps=steps, vocab=cfg.n_category,
               geometry="wave-local (W=1); no u-carrier; L_JEPA inert by construction",
               members=A._members(cfg),
               anchor=dict(embeddings=[[round(float(x), 6) for x in r]
                                       for r in loop.word.emit(torch.arange(cfg.n_category))],
                           construction="WordCortex(D, n_category, seed=seed+1) — deployed v2"))
    base = OUTDIR / (f"{arm_name}_s{seed}" + (f"_{out_tag}" if out_tag else ""))
    base.with_suffix(".manifest.json").write_text(json.dumps(man, indent=2, default=str))
    try:
        A.render_scatter(loop, base.with_suffix(".scatter.png"))
    except Exception as e:                                    # illustrative-only: never blocks
        man["scatter_note"] = f"render skipped: {e}"

    members_a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    members_b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    labels = loop._word_label(members_b, members_a)

    buf = _fresh_buf()
    cols, occ, gsplit, mixes = [], {}, {}, {}
    for t in range(1, steps + 1):
        # §13.10 probe read PRE-update (matched to the scheduled exam's timing)
        pl = _probe_exam_read(loop, t - 1) if bool(fab.is_probe_exam[t - 1]) else None
        loop.step(no_word=False)
        _buffer_wave(loop, t - 1, buf, probe_lift=pl)
        if t % EVAL == 0:
            cols.append(_eval_column(loop, t, buf, members_a, members_b, labels))
            buf = _fresh_buf()
        if t % BLOCK == 0:
            occ[str(t)] = loop.dc_track(cfg.n_eval)
            gsplit[str(t)] = grad_geometry_split(loop)
            mixes[str(t)] = loop.mix_snapshot()

    ts = [c["t"] for c in cols]
    panel_keys = ("num", "den", "ratio", "proto", "d2_depth", "d2_spread",
                  "asg_dist", "asg_argmax_k", "asg_entropy", "asg_cat",
                  "exam_lift", "exam_acc", "mid_word_lift", "mid_vis_err",
                  "div_bg", "div_id", "div_nuis")
    panels = {k: dynamics_panel(ts, [c.get(k) for c in cols]) for k in panel_keys}
    onset = X10.acquisition_onset(cols)                       # §13.4: num >= 0.01, 2 consec
    rec = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(),
        arm=arm_name, seed=seed, steps=steps, vocab=int(cfg.n_category),
        shuffled=bool(spec["shuffled"]), probe_rate=probe_rate,
        eval_cadence=EVAL, block_cadence=BLOCK,
        torch_num_threads=torch.get_num_threads(),
        acquisition_onset=onset,
        dynamics_panel=panels,
        columns=[{k: ((round(v, 6) if k in A._STANDING_COLS else float(f"{v:.6g}"))
                      if isinstance(v, float) else v) for k, v in c.items()}
                 for c in cols],
        occupancy=occ, grad_split=gsplit, masking_mix=mixes,
    )
    base.with_suffix(".json").write_text(json.dumps(rec, indent=2))
    print(f"{arm_name} s{seed}: onset={onset}  asg_cat_end={cols[-1]['asg_cat']:.4f}  "
          f"exam_lift_end={cols[-1].get('exam_lift')}  den_panel={panels['den']}")
    return rec


def _fresh_buf() -> dict:
    return dict(exam=[], exam_acc=[], probe_exam=[], mid_word=[], mid_vis=[],
                div=[], pos_word={}, pos_vis={})


def _buffer_wave(loop, t: int, buf: dict, probe_lift: float | None = None):
    """Consume the stashed training forward for wave t (called IMMEDIATELY after
    step(), before any probe overwrites the stash). `probe_lift` is the §13.10
    read-only probe result, computed PRE-update in the runner (matched to the
    scheduled exam's stash timing — review catch 2026-07-05: a post-update probe
    read re-introduces the recency channel the monitor exists to remove).

    Division-of-labor routing (§3): scheduled exams -> exam buffers; MID-DWELL
    (pos > 1) waves -> the recency companions; probe-dwell POSITION-1 waves are
    onset-geometry and are EXCLUDED from the mid-dwell companions (they carry the
    probe read instead). The per-position error curve is split by masked slot —
    word-cell and vision-cell errors live on different scales and never pool."""
    st = getattr(loop, "_stash", None)
    if st is None:
        return
    loop._stash = None
    fab = loop.stream
    cat = int(fab.cat[t])
    pred = st["pred"]                                         # (C=2, D), detached
    masked_word = bool(st["mask"][1])
    err = float((pred[st["mask"]] -
                 (st["e_vis"] if not masked_word else loop.word.emit(
                     torch.tensor([cat])))).norm())
    pb = _pos_bucket(int(fab.pos[t]))
    buf["pos_word" if masked_word else "pos_vis"].setdefault(pb, []).append(err)
    mid = int(fab.pos[t]) > 1
    if masked_word:
        lift, acc = exam_lift(loop, pred[1], cat)
        if bool(fab.is_exam[t]):
            buf["exam"].append(lift)
            buf["exam_acc"].append(acc)
            buf["div"].append(onset_divergence(loop, t))      # earned-salience probe
        elif mid:
            buf["mid_word"].append(lift)
    elif mid:
        buf["mid_vis"].append(err)
    if probe_lift is not None:                                # §13.10, pre-update
        buf["probe_exam"].append(probe_lift)


@torch.no_grad()
def _probe_exam_read(loop, t: int) -> float:
    """Position-matched, schedule-unmatched word-mask probe at a suppressed-exam dwell
    onset (§13.10). Read-only; no gradient; RNG-free."""
    st = X9._rng_guard(loop)
    cfg = loop.cfg
    fab = loop.stream
    raw = fab.raw[t:t + 1]
    e_vis = loop.vision.emit(raw)
    cat = int(fab.cat[t])
    e_word = loop.word.emit(torch.tensor([cat]))
    content = torch.stack([e_vis, e_word], dim=1)
    mask = torch.zeros(1, cfg.n_slots, dtype=torch.bool)
    mask[0, 1] = True
    masked = apply_slice_mask(loop._pose_pam_input(content), mask, loop.op.mask_emb)
    pred = loop.op(masked.reshape(cfg.n_slots, cfg.D).unsqueeze(0), loop.slot_ids,
                   (~mask).reshape(-1))[0]
    lift, _ = exam_lift(loop, pred[1], cat)
    X9._rng_check(loop, st, "probe_exam_read")
    return lift


def _eval_column(loop, t: int, buf: dict, ma, mb, labels) -> dict:
    cfg = loop.cfg
    with torch.no_grad():
        raw_c = loop.stim.raw_clean(ma, mb)
        e = loop.evoke_vision(ma, mb, associative=True)
        content = loop.vision.emit(raw_c)
        p = loop.vision.pool.assign(raw_c)
        off = ~torch.eye(p.shape[0], dtype=torch.bool)
        asg_dist = float(torch.cdist(p, p, p=1)[off].mean())
        asg_argmax_k = int(len(set(p.argmax(1).tolist())))
        asg_entropy = float(-(p * (p + 1e-12).log()).sum(1).mean())
    r = partition_read(e, labels, content)
    col = dict(t=t, num=r["cross_dist_raw"], den=r["content_denom"], ratio=r["d_diff"],
               proto=loop.pam_proto_spread(),
               d2_depth=loop.vision.pool.pooling_depth(),
               d2_spread=float(poolmetrics.within_group_spread(loop.vision.pool)),
               asg_dist=asg_dist, asg_argmax_k=asg_argmax_k, asg_entropy=asg_entropy)
    col.update(asg_reads(loop))
    col.update(X9.evo_decomp(loop))
    col.update(grad_decomp_local(loop, no_word=False))
    col.update(X9.pairwise_emit(loop))
    def _m(xs):
        return statistics.mean(xs) if xs else None
    col["exam_lift"] = _m(buf["exam"])
    col["exam_acc"] = _m(buf["exam_acc"])
    col["exam_n"] = len(buf["exam"])
    col["probe_exam_lift"] = _m(buf["probe_exam"])
    col["probe_exam_n"] = len(buf["probe_exam"])
    col["mid_word_lift"] = _m(buf["mid_word"])
    col["mid_vis_err"] = _m(buf["mid_vis"])
    if buf["div"]:
        for k in ("div_id", "div_nuis", "div_bg"):
            col[k] = statistics.mean(d[k] for d in buf["div"])
    # per-dwell-position curves SPLIT by masked slot (never pooled — different scales)
    col["pos_err_word"] = {k: round(statistics.mean(v), 5)
                           for k, v in sorted(buf["pos_word"].items())}
    col["pos_err_vis"] = {k: round(statistics.mean(v), 5)
                          for k, v in sorted(buf["pos_vis"].items())}
    return col


# ------------------------------------------------------------------ stage one
def stage_one_read(rec: dict) -> dict:
    """Per-run stage-one numbers: acquisition onset (§13.4 num-floor, pinned form) +
    the post-onset collapse-period estimate + the W_post precedence-ladder input + the
    asg_cat / exam_lift trajectory summaries.

    IN-REGIME DISCIPLINE (review catch 2026-07-05; the §10.14 ban + the §10.17
    estimator lesson): NO static-line constants enter this read. The period is the
    ESTIMATOR-FREE dynamics_panel dominant period of the post-onset den series (no
    4800 pin, no substitution band, no 20100 ramp cut — the post-onset slice is the
    in-regime segment by construction). den < X9.FLOOR stays as the standing ONE-SIDED
    collapse-floor tripwire (an instrument constant, not a regime constant). A cycle
    that is PRESENT but UNMEASURED is labeled exactly that — it is a stage-two
    decision input, never silently folded into the no-cycle fallback."""
    cols = rec["columns"]
    onset = rec["acquisition_onset"]
    out = dict(arm=rec["arm"], seed=rec["seed"], onset=onset)
    # the §10 sensitivity-without-conversion dissociation observable: num-floor onset vs
    # exam-CONVERSION onset. Conversion form PROPOSED (surfaced with the stage-two
    # constants, not yet ratified): exam_acc >= 0.6 in 2 consecutive eval windows.
    run = 0
    conv = None
    for c in cols:
        run = run + 1 if (c.get("exam_acc") is not None and c["exam_acc"] >= 0.6) else 0
        if run >= 2:
            conv = c["t"] - EVAL
            break
    out["exam_conversion_onset_PROPOSED_form"] = conv
    if onset is None:
        out["note"] = "NEVER ACQUIRED at stage-one horizon (acquisition-censored: unread, never a null)"
        return out
    post = [c for c in cols if c["t"] >= onset]
    den_panel = dynamics_panel([c["t"] for c in post], [c["den"] for c in post])
    measured = den_panel["dominant_period_steps"]
    any_cycle = any(c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR for c in post)
    out.update(
        den_dominant_period=measured,
        den_panel=den_panel,
        collapse_cycle_present=bool(any_cycle),
        w_post_ladder=(
            "own collapse period (measured in-regime)" if any_cycle and measured else
            "COLLAPSE CYCLE PRESENT, PERIOD UNMEASURED — stage-two must resolve "
            "(precedence-ladder input unresolved; do NOT fold into the no-cycle fallback)"
            if any_cycle else
            "FIXED CALIBRATED ABSOLUTE-WAVE WINDOW (no collapse cycle in-regime — "
            "pre-registered fallback, §13.4)"),
        asg_cat_post=dict(mean=round(statistics.mean(c["asg_cat"] for c in post), 4),
                          end=round(post[-1]["asg_cat"], 4),
                          min=round(min(c["asg_cat"] for c in post), 4)),
        asg_dist_post_mean=round(statistics.mean(c["asg_dist"] for c in post), 4),
        exam_lift_post=dict(
            mean=round(statistics.mean(c["exam_lift"] for c in post
                                       if c.get("exam_lift") is not None), 4),
            end=round(post[-1]["exam_lift"], 4) if post[-1].get("exam_lift") is not None else None),
        exam_acc_post_mean=round(statistics.mean(c["exam_acc"] for c in post
                                                 if c.get("exam_acc") is not None), 4),
        den_end=post[-1]["den"],
        argmax_k_end=post[-1]["asg_argmax_k"],
    )
    return out


def stage_one_collect():
    reads = []
    for arm in ARMS12:
        for s in CAL_SEEDS:
            p = OUTDIR / f"{arm}_s{s}.json"
            if p.exists():
                reads.append(stage_one_read(json.loads(p.read_text())))
    out = dict(cal_seeds=CAL_SEEDS, horizon=CAL_HORIZON, reads=reads,
               note="STAGE-ONE ONLY: constants are NOT set here; stage-two "
                    "(survival threshold, W_post, B1/B2, probe-dwell rate) waits on "
                    "the chat read of these numbers (handoff §'report back').")
    (OUTDIR / "exp12_stage1.json").write_text(json.dumps(out, indent=2))
    for r in reads:
        print(json.dumps(r))
    return out


# ------------------------------------------------------------------ smoke
def smoke():
    torch.manual_seed(0)
    loop, spec, cfg = build_exp12("exp12_dwell", 0, steps=1200)
    # one code path: step() is still the inherited Stage0Loop.step
    assert "step" not in EXP12Loop.__dict__ and "step" not in A.EXP08Loop.__dict__
    fab = loop.stream
    assert fab.T >= 1208 and int(fab.pos.min()) == 1
    # the guaranteed onset exam: every dwell's first wave is word-masked (rate 0)
    onset_rows = fab.pos == 1
    assert bool((fab.mask_slot[onset_rows] == 1).all()) and bool(fab.is_exam[onset_rows].all())
    # exactly one slot masked per wave, by construction of mask_slot
    # background constant identical across seeds (pin-to-constant)
    loop2, _, _ = build_exp12("exp12_dwell", 3, steps=64)
    assert torch.equal(loop.stim.bg_const, loop2.stim.bg_const)
    # A-SHUFFLE: identical wave multiset + identical exam count, different order
    ls, _, cfgs = build_exp12("exp12_shuffle", 0, steps=1200)
    fs = ls.stream
    assert torch.equal(fs.raw.sort(0).values, fab.raw.sort(0).values)
    assert int(fs.is_exam.sum()) == int(fab.is_exam.sum())
    assert not torch.equal(fs.member, fab.member)
    # dynamics: run; JEPA inert at W=1; anchor frozen; loop.gen parity across arms
    g0 = loop.gen.get_state()
    out = loop.step(no_word=False)
    assert out["l_jepa"] == 0.0, "L_JEPA not inert at wave-local geometry"
    for t in range(2, 301):
        loop.step(no_word=False)
    assert loop.word.param_delta() == 0.0
    for t in range(1, 301):
        ls.step(no_word=False)
    assert torch.equal(loop.gen.get_state(), ls.gen.get_state()), \
        "loop.gen diverged across arms (build_cells must consume zero draws)"
    # reads
    buf = _fresh_buf()
    loop.step(no_word=False)
    _buffer_wave(loop, loop._t - 1, buf)
    ma, mb = X9._member_set(cfg)
    labels = loop._word_label(mb, ma)
    col = _eval_column(loop, loop._t, buf, ma, mb, labels)
    need = {"num", "den", "asg_cat", "asg_cross_cat", "evo_common", "grad_common",
            "pairwise_emit", "pos_err_word", "pos_err_vis"}
    assert need <= set(col), f"missing columns: {need - set(col)}"
    gs = grad_geometry_split(loop)
    assert gs["teach_geom"] > 0 or gs["exam_geom"] > 0
    # probe machinery at a nonzero rate (stage-two constant; machinery must work now)
    lp, _, _ = build_exp12("exp12_dwell", 1, steps=600, probe_rate=0.3)
    fp = lp.stream
    assert int(fp.is_probe_exam.sum()) > 0, "probe-dwell machinery produced no probes at rate 0.3"
    sup = fp.pos == 1
    assert bool((fp.is_exam[sup] | fp.is_probe_exam[sup]).all())
    for t in range(1, 61):
        lp.step(no_word=False)
    pe = _probe_exam_read(lp, int(torch.nonzero(fp.is_probe_exam)[0]))
    assert isinstance(pe, float)
    # fabric asserts end-to-end on a real-size sample
    a = F.fabric_asserts(fab, cfg, n_sample=1208, n_null=60)
    print("SMOKE OK:", json.dumps(dict(
        cap=a["cap_hit"], walk=a["walk_realized"],
        perlag=a["perlag_nuis"], k=a["k_indep"], sched=a["schedule_indep"],
        bg=a["bg_indep"], col_keys=sorted(col.keys()))))


def _main12():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ARM", "SEED"))
    ap.add_argument("--steps", type=int, default=CAL_HORIZON)
    ap.add_argument("--stage1-collect", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(1)                                  # the determinism contract
    if args.smoke:
        smoke()
    elif args.run:
        run_exp12_arm(args.run[0], int(args.run[1]), args.steps)
    elif args.stage1_collect:
        stage_one_collect()


if __name__ == "__main__":
    _main12()
