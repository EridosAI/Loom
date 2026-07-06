"""EXP13 — lawful dynamics: the W=3 interior-mask loop (A-LAWFUL / A-LAWSCRAM), the
law-participation probe, the window-blinded discriminator, the runner, and the stage-one
calibrator (τ re-derivation + participation band).

Pre-registration: docs/EXP13_LAWFUL_DYNAMICS_PREREG.md (RATIFIED AT CHECKPOINT 2026-07-06).
NOTHING verdict-grade runs until the participation-gate ruling AND the stage-two constants
are recorded; this module runs stage-one only.

THE GEOMETRY (Fork 2b, ratified): W = 3 sliding window, stride 1, masked slots
INTERIOR-ONLY. At loop time t the window is waves [t, t+1, t+2]; the INTERIOR wave t+1
(window-local index 1) has exactly ONE slot masked (per the fabric's schedule / coin); the
two flanks are fully visible. The completer reads the interior slot FROM BOTH SIDES.
Terminal-position masking (a flank) never happens — forward-prediction-in-costume is
excluded by construction. This is the structural pass of the recorded W>1 guard.

THE FORWARD GUARD (§0/§2, binding): the next-wave-prediction term L_JEPA STAYS DELETED at
W>1. The base SculptLoop._l_jepa loops over within-window pairs (inert at W=1, the empty
range; it WOULD fire at W=3) — EXP13Loop overrides it to a hard zero. No component
acquires a next-step objective; the W=3 window is purely two-sided completion (L_PAM).

One code path: step/optimizer/losses inherited from EXP12Loop -> EXP08Loop -> SculptLoop
UNCHANGED except (a) _l_jepa -> 0 (the guard), (b) build_cells assembles the W=3 window,
(c) _l_pam stashes the reshaped window prediction for the reads. No new loss, no new force.
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

import constants                                              # noqa: E402
import exp07_config as C                                      # noqa: E402
import exp08_arms as A                                        # noqa: E402
import exp09_arms as X9                                       # noqa: E402
import exp10_arms as X10                                      # noqa: E402
import exp12_arms as X12                                      # noqa: E402
import exp13_fabric as F13                                    # noqa: E402
from loom import poolmetrics                                  # noqa: E402
from loom.completion import apply_slice_mask                  # noqa: E402
from revival import partition_read, dynamics_panel            # noqa: E402
from sculpt_config import SculptConfig                        # noqa: E402

OUTDIR = X12.OUTDIR
EVAL, BLOCK = X12.EVAL, X12.BLOCK

# --- §9.8 seeds / horizons (carried forms; stage-two horizon from re-cal onsets) ---
CAL_SEEDS = [20, 21, 22, 23, 24]
VERDICT_SEEDS = [0, 1, 2, 3, 4]
EXT_POOL = [5, 6]
SUB_POOL = [7, 8]                    # continuation pool (prospective substitution, §10.20.7-AMEND)
CAL_HORIZON = 160000
PROBE_RATE_STAGE1 = 0.0
W = 3                                # the interior-mask window (Fork 2b)
INTERIOR = 1                         # window-local index of the masked wave

ARMS13 = {
    "exp13_lawful":   dict(shuffled=False),
    "exp13_lawscram": dict(shuffled=True),
    # 12b TWINS ride along on the LAWFUL fabric (coin policy; present / absent-exposure)
    "exp13_12bc_lp":  dict(shuffled=False, uniform_mask=True, no_word=False),
    "exp13_12bc_la":  dict(shuffled=False, uniform_mask=True, no_word=True, expo_word=True),
}
CORE_ARMS = ("exp13_lawful", "exp13_lawscram")


# ------------------------------------------------------------------ the loop
class EXP13Loop(X12.EXP12Loop):
    """EXP12Loop with the W=3 interior-mask geometry. step()/optimizer inherited; the ONLY
    dynamics changes are the forward-guard (_l_jepa -> 0), the windowed build_cells, and
    the reshaped-prediction stash. build_cells consumes ZERO loop.gen draws (waves are
    pre-generated), so loop.gen stays bit-identical across arms at a seed."""

    def _make_stream(self):
        cfg = self.cfg
        v = getattr(cfg, "_exp13", None)
        assert v is not None, "EXP13Loop needs cfg._exp13 before factories"
        if v.get("uniform_mask") or v.get("word_ref"):
            assert v.get("probe_rate", 0.0) == 0.0, "uniform/word-ref arm: probe machinery N/A"
        return F13.build_fabric13(self.stim, cfg, cfg.seed, v["T"],
                                  probe_rate=v.get("probe_rate", 0.0),
                                  shuffled=v.get("shuffled", False),
                                  uniform_mask=v.get("uniform_mask", False),
                                  word_ref=v.get("word_ref", False),
                                  expo_word=v.get("expo_word", False))

    def _l_jepa(self, bc):
        # THE W>1 FORWARD GUARD (§0/§2): the next-wave-prediction term stays DELETED at
        # W=3. The base loops over within-window pairs; here it is a hard zero — asserted.
        return torch.zeros(())

    def build_cells(self, t, *, no_word, gen, ablate="none", force_mask=None):
        """t = the window's LEFT edge; window = waves [t, t+1, t+2]; INTERIOR = wave t+1.
        Only the interior wave is masked (one slot); the flanks are fully visible."""
        cfg = self.cfg
        fab = self.stream
        ti = t + INTERIOR                                     # the interior (masked) wave
        assert ti + 1 < fab.T, f"window right edge past fabric (t={t}, T={fab.T})"
        idx = torch.arange(t, t + cfg.W)                     # (W,)
        raw = fab.raw[idx]                                   # (W, D) precomputed waves
        e_vis = self.vision.emit(raw)                        # (W, D) plastic, grad
        wl = fab.cat[idx]
        tokens = torch.tensor([self.curric.word_token(int(wl[w]), no_word=no_word)
                               for w in range(cfg.W)])
        e_word = self._vary_word(self.word.emit(tokens), tokens)
        content = torch.stack([e_vis, e_word], dim=1)        # (W, n_slots, D)
        v13 = getattr(cfg, "_exp13", {})
        word_ref = bool(v13.get("word_ref", False))
        expo_word = bool(v13.get("expo_word", False))
        if force_mask is None:
            mask = torch.zeros(cfg.W, cfg.n_slots, dtype=torch.bool)
            slot = int(fab.mask_slot[ti])                    # interior wave's assigned slot
            if (word_ref or expo_word) and slot == 1:
                fam_name = "exposure"                        # no cell masked; loss skips
            else:
                mask[INTERIOR, slot] = True
                fam_name = ("exam" if bool(fab.is_exam[ti])
                            else ("mid_word" if slot == 1 else "mid_vis"))
            self.mix["n"] += 1
            self.mix["vis_masked"] += int(slot == 0 and fam_name != "exposure")
            self.mix["word_visible"] += int(slot == 0 and fam_name != "exposure")
            self.mix["sib_visible"] += 1                     # interior has same-window flanks
            self.mix["both"] += 0
        else:
            mask, fam_name = force_mask, "forced"
        masked = apply_slice_mask(self._pose_pam_input(content), mask, self.op.mask_emb)
        # NO u-carrier (order enters via the fabric's lawful dynamics only, §2)
        Ccells = cfg.W * cfg.n_slots
        return dict(
            cells=masked.reshape(Ccells, cfg.D),
            target=self._pam_target(content).reshape(Ccells, cfg.D),
            mask=mask.reshape(Ccells), visible=(~mask).reshape(Ccells),
            fam=fam_name, raw=raw, drift_w=torch.zeros(cfg.W),
            dwell=fab.dwell_id[idx], e_vis=e_vis[INTERIOR:INTERIOR + 1],
            t_int=ti,
        )

    def _l_pam(self, bc):
        if not bool(bc["mask"].any()):
            # EXPOSURE-ONLY (coin policy absent twin): completion loss SKIPS (constant 0)
            pred = self.op(bc["cells"].unsqueeze(0), self.slot_ids, bc["visible"])[0]
            if bc["fam"] != "forced":
                self._stash = dict(pred=pred.reshape(self.cfg.W, self.cfg.n_slots, -1).detach(),
                                   e_vis=bc["e_vis"].detach(), mask=bc["mask"].clone(),
                                   fam=bc["fam"], raw=bc["raw"], t_int=bc["t_int"])
            return torch.zeros(()), pred
        pred = self.op(bc["cells"].unsqueeze(0), self.slot_ids, bc["visible"])[0]
        m = bc["mask"]
        l = torch.nn.functional.mse_loss(pred[m], bc["target"][m])
        if bc["fam"] != "forced":
            self._stash = dict(pred=pred.reshape(self.cfg.W, self.cfg.n_slots, -1).detach(),
                               e_vis=bc["e_vis"].detach(), mask=bc["mask"].clone(),
                               fam=bc["fam"], raw=bc["raw"], t_int=bc["t_int"])
        return l, pred


# ------------------------------------------------------------------ windowed reads
@torch.no_grad()
def _window_complete(loop, ti: int, mask_slot: int, *, blind_flanks: bool = False,
                     decoy_left: int | None = None, decoy_right: int | None = None):
    """Read-only two-sided completion of the interior wave ti's `mask_slot`. RNG-free.
    - blind_flanks: replace BOTH flanks' cells with mask_emb (the window-blinded read: only
      the interior wave's OTHER slot remains — kills the copyable same-dwell trace).
    - decoy_left/right: replace a flank wave with wave j from ANOTHER dwell (the
      law-participation probe's law-broken window). Returns (pred_slot, e_true_slot)."""
    cfg = loop.cfg
    fab = loop.stream
    t = ti - INTERIOR
    idx = [t + w for w in range(cfg.W)]
    if decoy_left is not None:
        idx[0] = decoy_left
    if decoy_right is not None:
        idx[cfg.W - 1] = decoy_right
    idx = torch.tensor(idx)
    raw = fab.raw[idx]
    e_vis = loop.vision.emit(raw)
    e_word = loop.word.emit(fab.cat[idx])
    content = torch.stack([e_vis, e_word], dim=1)
    mask = torch.zeros(cfg.W, cfg.n_slots, dtype=torch.bool)
    mask[INTERIOR, mask_slot] = True
    posed = loop._pose_pam_input(content)
    if blind_flanks:
        for w in range(cfg.W):
            if w != INTERIOR:
                mask[w, :] = True                            # blind both flanks entirely
    masked = apply_slice_mask(posed, mask, loop.op.mask_emb)
    cells = masked.reshape(cfg.W * cfg.n_slots, cfg.D)
    pred = loop.op(cells.unsqueeze(0), loop.slot_ids, (~mask).reshape(-1))[0]
    pred = pred.reshape(cfg.W, cfg.n_slots, cfg.D)
    # the interior true slot (vision emission or word emission of the interior wave)
    e_true = e_vis[INTERIOR] if mask_slot == 0 else e_word[INTERIOR]
    return pred[INTERIOR, mask_slot], e_true


@torch.no_grad()
def onset_divergence13(loop, ti: int) -> dict:
    """Earned-salience leg-2 read (Amendment A; expectation, not a gate) — now W=3 and
    mechanically posable. Two-sided vision-masked completion of the interior wave; residual
    vs the actual vision emission, energy split over the pre-rotation axis blocks."""
    st = X9._rng_guard(loop)
    pred_slot, e_true = _window_complete(loop, ti, 0)
    r = (pred_slot - e_true) @ loop.stim.Q
    n_id = loop.cfg.n_A + loop.cfg.n_distractor + loop.cfg.n_category
    out = dict(div_id=float(r[:n_id].pow(2).sum()),
               div_nuis=float(r[n_id:n_id + F13.K_AXES].pow(2).sum()),
               div_bg=float(r[n_id + F13.K_AXES:n_id + F13.K_AXES + F13.BG_AXES].pow(2).sum()))
    X9._rng_check(loop, st, "onset_divergence13")
    return out


@torch.no_grad()
def window_blinded_read(loop, ti: int, mask_slot: int) -> dict:
    """The shortcut-through-trace discriminator (§2/§5): completion error of the interior
    slot WITH the same-window flanks blinded vs the full-window completion. A completer
    that COPIES a same-dwell neighbor collapses when the neighbor is blinded; one that
    reads the LAW (or the interior's other slot) survives. Read-only, RNG-free."""
    st = X9._rng_guard(loop)
    full_pred, e_true = _window_complete(loop, ti, mask_slot)
    blind_pred, _ = _window_complete(loop, ti, mask_slot, blind_flanks=True)
    err_full = float((full_pred - e_true).norm())
    err_blind = float((blind_pred - e_true).norm())
    X9._rng_check(loop, st, "window_blinded_read")
    return dict(err_full=err_full, err_blind=err_blind,
                blind_penalty=err_blind - err_full)


@torch.no_grad()
def participation_probe(loop, *, n: int = 64, panel_seed: int = 0) -> dict | None:
    """The LAW-PARTICIPATION GATE (Fork 3C, read-only, panel cadence). Completion error on
    TRUE lawful windows vs LAW-BROKEN DECOYS (a flank swapped for a wave from ANOTHER
    dwell, |Δt|- and residual-magnitude-matched, §9.5). If completion reads the law,
    breaking it HURTS: decoy error > true error. The gap is the participation statistic;
    the band + sustained-N are stage-two. Runs on the UNSHUFFLED (lawful) order only
    (decoys need dwell identity); returns None on a shuffled arm."""
    fab = loop.stream
    if fab.shuffled:
        return None
    st = X9._rng_guard(loop)
    lawful = F13.lawful_window_mask(fab)                      # interior waves with same-dwell flanks
    cand = torch.nonzero(lawful).flatten()
    cand = cand[(cand >= INTERIOR) & (cand + 1 < fab.T)]
    if len(cand) == 0:
        X9._rng_check(loop, st, "participation_probe")
        return None
    g = torch.Generator().manual_seed(90007 + panel_seed)
    sel = cand[torch.randperm(len(cand), generator=g)[:min(n, len(cand))]]
    true_err, decoy_err, n_used = [], [], 0
    resid = (fab.nuis - fab.law_mu)
    for ti in sel.tolist():
        slot = int(fab.mask_slot[ti])
        # residual-magnitude-matched cross-dwell donor for the RIGHT flank (|Δt| kept: the
        # donor sits at the same within-window offset). Match on the donor wave's residual
        # magnitude to the true right flank's, so the swap breaks LAW not noise-scale.
        tgt_flank = ti + 1
        rmag = float(resid[tgt_flank].norm())
        donors = torch.nonzero(fab.dwell_id != int(fab.dwell_id[ti])).flatten()
        donors = donors[(donors >= INTERIOR) & (donors + 1 < fab.T)]
        if len(donors) == 0:
            continue
        dres = resid[donors].norm(dim=1)
        donor = int(donors[(dres - rmag).abs().argmin()])
        tp, e_true = _window_complete(loop, ti, slot)
        dp, _ = _window_complete(loop, ti, slot, decoy_right=donor)
        true_err.append(float((tp - e_true).norm()))
        decoy_err.append(float((dp - e_true).norm()))
        n_used += 1
    X9._rng_check(loop, st, "participation_probe")
    if n_used == 0:
        return None
    te, de = statistics.mean(true_err), statistics.mean(decoy_err)
    return dict(true_err=round(te, 5), decoy_err=round(de, 5),
                participation_gap=round(de - te, 5), n=n_used,
                note="gap>0 = law-broken window completes WORSE = participation; band at stage-two")


def grad_geometry_split13(loop, no_word: bool = False) -> dict:
    """Teaching (interior vision-masked) vs exam (interior word-masked) gradient norms at
    W=3 — the EXP12 split with the interior-only force mask."""
    cfg = loop.cfg
    out = {}
    for name, slot in (("teach_geom", 0), ("exam_geom", 1)):
        m = torch.zeros(cfg.W, cfg.n_slots, dtype=torch.bool)
        m[INTERIOR, slot] = True
        bc = loop.build_cells(loop._t, no_word=no_word, gen=loop.gen, force_mask=m)
        l_pam, _ = loop._l_pam(bc)
        g = torch.autograd.grad(l_pam, loop.vision.pool.delta2, retain_graph=False,
                                allow_unused=True)[0]
        out[name] = 0.0 if g is None else float(g.norm())
    return out


# ------------------------------------------------------------------ τ re-derivation (§9.2)
def tau_rederivation(fab: F13.Fabric13, *, max_lag: int = 8) -> dict:
    """Stage-one: residual-about-law decorrelation vs drift scale (the Fork-1/2 coupling,
    EXP13 edition). Reports the residual autocorrelation at lags 1..max_lag (within-dwell,
    per axis, averaged) and the drift-per-wave scale vs the residual sd — so the τ ordering
    (residual decorrelates fast; drift is the slow cross-wave order signal) is a MEASURED
    number before stage-two, never assumed."""
    resid = fab.nuis - fab.law_mu                            # (T, K)
    # within-dwell residual autocorrelation (only consecutive same-dwell pairs count)
    d = fab.dwell_id
    acf = []
    r0 = float((resid ** 2).mean())
    for L in range(1, max_lag + 1):
        same = d[L:] == d[:-L]
        if not bool(same.any()):
            acf.append(None)
            continue
        x, y = resid[:-L][same], resid[L:][same]
        cov = float((x * y).mean())
        acf.append(round(cov / max(1e-12, r0), 4))
    # empirical decorrelation lag = first lag whose acf drops below 1/e
    thr = math.exp(-1.0)
    decor = next((L for L, v in enumerate(acf, 1) if v is not None and v < thr), None)
    drift_per_wave = float(fab.dwell_velocity.abs().mean())
    resid_sd = float(resid.std())
    return dict(residual_acf=acf, decorrelation_lag_1_over_e=decor, tau_pin=F13.TAU,
                drift_per_wave=round(drift_per_wave, 4), residual_sd=round(resid_sd, 4),
                drift_over_residual=round(drift_per_wave / max(1e-9, resid_sd), 4),
                note="residual decorrelates within a few waves; drift is the slow ordering "
                     "signal — the tau<E[k] ordering, re-derived on residuals-about-law")


# ------------------------------------------------------------------ the runner
def build_exp13(arm_name: str, seed: int, steps: int, probe_rate: float = PROBE_RATE_STAGE1):
    spec = ARMS13[arm_name]
    pin = constants.PinnedConstants()
    cfg = SculptConfig(seed=seed)
    cfg.W = W                                                # the interior-mask window (Fork 2b)
    cfg.T = steps + W + 8                                    # continual: window needs t+2 < T
    cfg._exp13 = dict(T=cfg.T, shuffled=spec["shuffled"], probe_rate=probe_rate,
                      uniform_mask=spec.get("uniform_mask", False),
                      word_ref=spec.get("word_ref", False),
                      expo_word=spec.get("expo_word", False))
    loop = EXP13Loop(cfg, pin)
    return loop, spec, cfg


def run_exp13_arm(arm_name: str, seed: int, steps: int, *,
                  probe_rate: float = PROBE_RATE_STAGE1, out_tag: str | None = None) -> dict:
    loop, spec, cfg = build_exp13(arm_name, seed, steps, probe_rate)
    fab = loop.stream
    OUTDIR.mkdir(exist_ok=True)
    if fab.shuffled:
        fab_plain = F13.build_fabric13(loop.stim, cfg, seed, fab.T, probe_rate=probe_rate,
                                       shuffled=False,
                                       uniform_mask=spec.get("uniform_mask", False),
                                       word_ref=spec.get("word_ref", False),
                                       expo_word=spec.get("expo_word", False))
        assert torch.equal(fab.raw.sort(0).values, fab_plain.raw.sort(0).values), \
            "A-LAWSCRAM waves are not the identical multiset"
        assert int(fab.is_exam.sum()) == int(fab_plain.is_exam.sum()), "exam count differs"
        asserts = F13.fabric_asserts13(fab_plain, cfg)
        tau = tau_rederivation(fab_plain)
    else:
        asserts = F13.fabric_asserts13(fab, cfg)
        tau = tau_rederivation(fab)
    man = F13.fabric_manifest13(fab, loop.stim, cfg, asserts)
    man.update(arm=arm_name, seed=seed, steps=steps, vocab=cfg.n_category,
               geometry="W=3 interior-mask; L_JEPA deleted (W>1 forward guard); no u-carrier",
               tau_rederivation=tau, members=A._members(cfg))
    base = OUTDIR / (f"{arm_name}_s{seed}" + (f"_{out_tag}" if out_tag else ""))
    base.with_suffix(".manifest.json").write_text(json.dumps(man, indent=2, default=str))

    members_a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    members_b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    labels = loop._word_label(members_b, members_a)
    no_word = bool(spec.get("no_word", False))
    buf = _fresh_buf13()
    cols, occ, gsplit, part = [], {}, {}, {}
    for t in range(1, steps + 1):
        loop.step(no_word=no_word)
        _buffer_wave13(loop, buf)
        if t % EVAL == 0:
            cols.append(_eval_column13(loop, t, buf, members_a, members_b, labels, no_word=no_word))
            buf = _fresh_buf13()
        if t % BLOCK == 0:
            occ[str(t)] = loop.dc_track(cfg.n_eval)
            gsplit[str(t)] = grad_geometry_split13(loop, no_word)
            pp = participation_probe(loop, panel_seed=t)
            if pp is not None:
                part[str(t)] = pp

    ts = [c["t"] for c in cols]
    panel_keys = ("num", "den", "ratio", "proto", "d2_depth", "d2_spread",
                  "asg_dist", "asg_cat", "exam_lift", "exam_acc", "mid_vis_err",
                  "div_bg", "div_id", "div_nuis", "blind_penalty")
    panels = {k: dynamics_panel(ts, [c.get(k) for c in cols]) for k in panel_keys}
    onset = X10.acquisition_onset(cols)
    rec = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(),
        arm=arm_name, seed=seed, steps=steps, vocab=int(cfg.n_category),
        shuffled=bool(spec["shuffled"]), probe_rate=probe_rate, no_word=no_word,
        W=W, eval_cadence=EVAL, block_cadence=BLOCK,
        torch_num_threads=torch.get_num_threads(),
        acquisition_onset=onset, tau_rederivation=tau,
        lawful_window=asserts.get("lawful_window"),
        participation_probe=part, dynamics_panel=panels,
        columns=[{k: ((round(v, 6) if k in A._STANDING_COLS else float(f"{v:.6g}"))
                      if isinstance(v, float) else v) for k, v in c.items()}
                 for c in cols],
        occupancy=occ, grad_split=gsplit,
    )
    base.with_suffix(".json").write_text(json.dumps(rec, indent=2))
    pg = (statistics.mean(p["participation_gap"] for p in part.values()) if part else None)
    print(f"{arm_name} s{seed}: onset={onset}  asg_cat_end={cols[-1]['asg_cat']:.4f}  "
          f"lawful_frac={asserts['lawful_window']['fraction']}  "
          f"part_gap_mean={pg}  den_panel={panels['den']}")
    return rec


def _fresh_buf13() -> dict:
    return dict(exam=[], exam_acc=[], mid_vis=[], div=[], blind=[], pos_word={}, pos_vis={})


def _buffer_wave13(loop, buf: dict):
    """Consume the stashed W=3 training forward (interior wave). Division of labor as EXP12:
    scheduled onset exams -> exam buffers + earned-salience + window-blinded reads;
    mid-dwell vision-masks -> teaching companion."""
    st = getattr(loop, "_stash", None)
    if st is None:
        return
    loop._stash = None
    if not bool(st["mask"].any()):
        return                                               # exposure-only wave
    fab = loop.stream
    ti = st["t_int"]
    cat = int(fab.cat[ti])
    pred = st["pred"]                                        # (W, n_slots, D)
    mask = st["mask"].reshape(loop.cfg.W, loop.cfg.n_slots)
    masked_word = bool(mask[INTERIOR, 1])
    pslot = pred[INTERIOR, 1] if masked_word else pred[INTERIOR, 0]
    tgt = loop.word.emit(torch.tensor([cat]))[0] if masked_word else st["e_vis"][0]
    err = float((pslot - tgt).norm())
    pb = X12._pos_bucket(int(fab.pos[ti]))
    buf["pos_word" if masked_word else "pos_vis"].setdefault(pb, []).append(err)
    mid = int(fab.pos[ti]) > 1
    if masked_word:
        lift, acc = X12.exam_lift(loop, pslot, cat)
        if bool(fab.is_exam[ti]):
            buf["exam"].append(lift)
            buf["exam_acc"].append(acc)
            buf["div"].append(onset_divergence13(loop, ti))
            buf["blind"].append(window_blinded_read(loop, ti, 1)["blind_penalty"])
    elif mid:
        buf["mid_vis"].append(err)
        buf["blind"].append(window_blinded_read(loop, ti, 0)["blind_penalty"])


def _eval_column13(loop, t, buf, ma, mb, labels, no_word=False) -> dict:
    cfg = loop.cfg
    with torch.no_grad():
        raw_c = loop.stim.raw_clean(ma, mb)
        e = loop.evoke_vision(ma, mb, associative=True)
        content = loop.vision.emit(raw_c)
        p = loop.vision.pool.assign(raw_c)
        off = ~torch.eye(p.shape[0], dtype=torch.bool)
        asg_dist = float(torch.cdist(p, p, p=1)[off].mean())
        asg_argmax_k = int(len(set(p.argmax(1).tolist())))
    r = partition_read(e, labels, content)
    col = dict(t=t, num=r["cross_dist_raw"], den=r["content_denom"], ratio=r["d_diff"],
               proto=loop.pam_proto_spread(),
               d2_depth=loop.vision.pool.pooling_depth(),
               d2_spread=float(poolmetrics.within_group_spread(loop.vision.pool)),
               asg_dist=asg_dist, asg_argmax_k=asg_argmax_k)
    col.update(X12.asg_reads(loop))
    col["sep_cat"] = X12._sep_ratio(content, mb % cfg.n_category)
    col["sep_dist"] = X12._sep_ratio(content, mb // cfg.n_category)
    col["sep_a"] = X12._sep_ratio(content, ma)

    def _m(xs):
        return statistics.mean(xs) if xs else None
    col["exam_lift"] = _m(buf["exam"])
    col["exam_acc"] = _m(buf["exam_acc"])
    col["exam_n"] = len(buf["exam"])
    col["mid_vis_err"] = _m(buf["mid_vis"])
    col["blind_penalty"] = _m(buf["blind"])
    if buf["div"]:
        for k in ("div_id", "div_nuis", "div_bg"):
            col[k] = statistics.mean(d[k] for d in buf["div"])
    col["pos_err_word"] = {k: round(statistics.mean(v), 5) for k, v in sorted(buf["pos_word"].items())}
    col["pos_err_vis"] = {k: round(statistics.mean(v), 5) for k, v in sorted(buf["pos_vis"].items())}
    return col


# ------------------------------------------------------------------ stage one
def stage_one_read13(rec: dict) -> dict:
    """Per-run stage-one numbers: onset + in-regime den period + asg_cat/exam trajectory +
    the EXP13 additions (τ re-derivation, lawful-window fraction, participation-gap series,
    window-blinded penalty). In-regime discipline carried (no static-line constants)."""
    cols = rec["columns"]
    onset = rec["acquisition_onset"]
    out = dict(arm=rec["arm"], seed=rec["seed"], onset=onset,
               lawful_window=rec.get("lawful_window"),
               tau_rederivation=rec.get("tau_rederivation"))
    part = rec.get("participation_probe", {})
    if part:
        gaps = [p["participation_gap"] for p in part.values()]
        out["participation"] = dict(
            gap_mean=round(statistics.mean(gaps), 5), gap_min=round(min(gaps), 5),
            gap_max=round(max(gaps), 5), n_panels=len(gaps),
            true_err_mean=round(statistics.mean(p["true_err"] for p in part.values()), 5),
            decoy_err_mean=round(statistics.mean(p["decoy_err"] for p in part.values()), 5))
        # THE PRE-REGISTERED DISCRIMINATOR (§4, ruled at GO 2026-07-06, recorded before
        # cal): the gap-vs-acquisition curve, aligned to the num-floor onset. Pre-onset
        # panels = the noise reference; the read is "acquired AND flat" vs "gap opens
        # post-onset". Band/N are stage-two; stage-one reports raw aligned numbers.
        curve = sorted(((int(t), p["participation_gap"]) for t, p in part.items()),
                       key=lambda kv: kv[0])
        pre = [g for t, g in curve if onset is None or t < onset]
        post = [g for t, g in curve if onset is not None and t >= onset]
        pc = dict(panels=curve, onset=onset,
                  pre_onset=(dict(n=len(pre), mean=round(statistics.mean(pre), 5),
                                  sd=round(statistics.stdev(pre), 5) if len(pre) > 1 else None,
                                  max_abs=round(max(abs(g) for g in pre), 5))
                             if pre else None))
        if post:
            pre_max = max(abs(g) for g in pre) if pre else None
            pc["post_onset"] = dict(
                n=len(post), mean=round(statistics.mean(post), 5),
                max=round(max(post), 5), end=round(post[-1], 5),
                frac_above_pre_max_abs=(round(sum(1 for g in post
                                                  if pre_max is not None and g > pre_max)
                                              / len(post), 4) if pre_max is not None else None))
        pc["discrimination"] = ("PRE-ACQUISITION ONLY — licenses nothing" if not post else
                                "post-onset read available (benign = opens; structural = "
                                "acquired-and-flat; band at stage-two)")
        out["participation_curve"] = pc
    if onset is None:
        out["note"] = "NEVER ACQUIRED at stage-one horizon (acquisition-censored: unread, never a null)"
        return out
    post = [c for c in cols if c["t"] >= onset]
    den_panel = dynamics_panel([c["t"] for c in post], [c["den"] for c in post])
    any_cycle = any(c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR for c in post)
    out.update(
        den_dominant_period=den_panel["dominant_period_steps"], den_panel=den_panel,
        collapse_cycle_present=bool(any_cycle),
        asg_cat_post=dict(mean=round(statistics.mean(c["asg_cat"] for c in post), 4),
                          end=round(post[-1]["asg_cat"], 4),
                          min=round(min(c["asg_cat"] for c in post), 4)),
        asg_dist_post_mean=round(statistics.mean(c["asg_dist"] for c in post), 4),
        exam_lift_post=dict(
            mean=round(statistics.mean(c["exam_lift"] for c in post
                                       if c.get("exam_lift") is not None), 4),
            end=round(post[-1]["exam_lift"], 4) if post[-1].get("exam_lift") is not None else None),
        blind_penalty_post_mean=round(statistics.mean(c["blind_penalty"] for c in post
                                                      if c.get("blind_penalty") is not None), 5),
        den_end=post[-1]["den"], argmax_k_end=post[-1]["asg_argmax_k"])
    return out


def stage_one_collect13():
    reads = []
    for arm in ARMS13:
        for s in CAL_SEEDS:
            p = OUTDIR / f"{arm}_s{s}.json"
            if p.exists():
                reads.append(stage_one_read13(json.loads(p.read_text())))
    out = dict(cal_seeds=CAL_SEEDS, horizon=CAL_HORIZON, reads=reads,
               note="STAGE-ONE ONLY: constants NOT set here; stage-two (θ, S_w bands, N, "
                    "horizons, dead reference, participation band+N) + the participation-gate "
                    "ruling wait on the chat read of these numbers.")
    (OUTDIR / "exp13_stage1.json").write_text(json.dumps(out, indent=2))
    for r in reads:
        print(json.dumps(r))
    return out


# ------------------------------------------------------------------ smoke
def smoke():
    torch.manual_seed(0)
    loop, spec, cfg = build_exp13("exp13_lawful", 0, steps=1200)
    # one code path: step() is still the inherited SculptLoop.step
    assert "step" not in EXP13Loop.__dict__ and "step" not in X12.EXP12Loop.__dict__
    assert cfg.W == 3
    fab = loop.stream
    assert fab.T >= 1211 and int(fab.pos.min()) == 1
    assert fab.law_mu is not None and fab.dwell_velocity is not None
    # the guaranteed onset exam (core arm, rate 0): pos-1 waves are word-masked exams
    onset_rows = fab.pos == 1
    assert bool((fab.mask_slot[onset_rows] == 1).all()) and bool(fab.is_exam[onset_rows].all())
    # background pin-to-constant across seeds
    loop2, _, _ = build_exp13("exp13_lawful", 3, steps=64)
    assert torch.equal(loop.stim.bg_const, loop2.stim.bg_const)
    # A-LAWSCRAM: identical wave multiset + exam count, different order
    ls, _, cfgs = build_exp13("exp13_lawscram", 0, steps=1200)
    fs = ls.stream
    assert torch.equal(fs.raw.sort(0).values, fab.raw.sort(0).values)
    assert int(fs.is_exam.sum()) == int(fab.is_exam.sum())
    assert not torch.equal(fs.member, fab.member)
    # THE W>1 FORWARD GUARD: L_JEPA is a hard zero at W=3 (the base would fire here)
    g0 = loop.gen.get_state()
    out = loop.step(no_word=False)
    assert out["l_jepa"] == 0.0, "L_JEPA not deleted at W=3 — forward guard breached"
    # interior-only masking: only the interior wave is ever masked (terminals never)
    bc = loop.build_cells(loop._t, no_word=False, gen=loop.gen)
    mgrid = bc["mask"].reshape(cfg.W, cfg.n_slots)
    assert not bool(mgrid[0].any()) and not bool(mgrid[2].any()), "a flank was masked (forward-in-costume)"
    assert int(mgrid[INTERIOR].sum()) == 1, "interior must have exactly one masked slot"
    for _ in range(2, 301):
        loop.step(no_word=False)
    assert loop.word.param_delta() == 0.0, "anchor not frozen"
    # loop.gen parity across arms (build_cells consumes zero draws)
    for _ in range(1, 301):
        ls.step(no_word=False)
    assert torch.equal(loop.gen.get_state(), ls.gen.get_state()), "loop.gen diverged across arms"
    # reads present
    buf = _fresh_buf13()
    loop.step(no_word=False)
    _buffer_wave13(loop, buf)
    ma, mb = X9._member_set(cfg)
    labels = loop._word_label(mb, ma)
    col = _eval_column13(loop, loop._t, buf, ma, mb, labels)
    need = {"num", "den", "asg_cat", "sep_cat", "blind_penalty", "pos_err_vis"}
    assert need <= set(col), f"missing columns: {need - set(col)}"
    # participation probe fires on the lawful arm, None on scrambled
    pp = participation_probe(loop, n=32)
    assert pp is not None and "participation_gap" in pp
    assert participation_probe(ls, n=32) is None, "probe must be None on A-LAWSCRAM"
    # window-blinded read + earned-salience read
    ti = int(torch.nonzero(fab.is_exam)[3])
    wb = window_blinded_read(loop, ti, 1)
    assert "blind_penalty" in wb
    div = onset_divergence13(loop, ti)
    assert {"div_id", "div_nuis", "div_bg"} <= set(div)
    # τ re-derivation
    tau = tau_rederivation(fab)
    assert tau["decorrelation_lag_1_over_e"] is not None or tau["residual_acf"][0] is not None
    # fabric asserts end-to-end (incl. residual-about-law, law-params ⟂ member, lawful frac)
    a = F13.fabric_asserts13(fab, cfg, n_sample=1211, n_null=60)
    lw = a["lawful_window"]
    print("SMOKE OK:", json.dumps(dict(
        cap=a["cap_hit"]["ok"], perlag_resid=a["perlag_residual"],
        law_params=a["law_params_indep"], k=a["k_indep"]["ok"], sched=a["schedule_indep"]["ok"],
        bg=a["bg_indep"]["ok"], lawful_window=lw, law_realized=a["law_realized"],
        participation=pp, tau=tau, col_keys=sorted(col.keys()))))


def _main13():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ARM", "SEED"))
    ap.add_argument("--steps", type=int, default=CAL_HORIZON)
    ap.add_argument("--stage1-collect", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(1)
    if args.smoke:
        smoke()
    elif args.run:
        run_exp13_arm(args.run[0], int(args.run[1]), args.steps)
    elif args.stage1_collect:
        stage_one_collect13()


if __name__ == "__main__":
    _main13()
