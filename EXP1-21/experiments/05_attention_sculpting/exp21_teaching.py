"""EXP21 — PAM-TEACHING CONTRAST: arms, faithful runner, G0 parity, G2 gradient/compute census.

Pre-registration: docs/EXP21_PAM_TEACHING_CONTRAST_PREREG.md (Touch-1 RATIFIED 2026-08-04;
build authorized through G3 only; HARD HOLD before G4). Diff-scope baseline: commit 19a8fbf
(the prereg commit, §2.5).

ARMS (§2):
  * Teaching ON  = the deployed `EXP12Loop` on `exp12_dwell` — semantically REUSED, constructed
    through the committed `exp12_arms.build_exp12` path itself (G0 additionally proves this
    module's own constructor is bit-equal to it).
  * Teaching OFF = `EXP21TeachingOffLoop(EXP12Loop)` below — overrides EXACTLY the two
    identity-default hooks `_pose_pam_input` / `_pam_target` (loop.py:115/:121), `super()` first,
    clone, detach ONLY vision slot [..., 0, :]. Blocks cue-side AND target-side raw L_PAM
    gradients into every visual-cortex parameter; PAM forwards, raw L_PAM, PAM parameters,
    optimiser membership, and actual PAM updates stay alive; vision stays plastic under its
    non-PAM forces (spread + pool penalty; L_JEPA is inert at W=1, loop.py:192).

RUNNER (§3.5/§2.3): `run_exp21_arm` REPLICATES `exp14_arms.run_exp14_arm`'s body in exact read
order (the interleaved dc_track/grad_geometry_split/eval reads couple into the trajectory through
the live stimulus counter — §10.21.4; the house precedent is exp14 replicating exp12's runner).
The ONLY addition is the trajectory-inert external probe read (exp21_probe.probe_read: zero RNG,
zero live-state mutation, guarded) at t=0, every 3,000 waves, and exactly `read_at`. Probe results
live in SEPARATE artifacts; the run record and manifest carry no probe field, so probe-enabled and
probe-disabled records are comparable by FULL equality (G0 parity check 3).

Shared-file fence (§9.2): this module imports the committed learner/generator chain and changes
nothing in it — asserted structurally by exp21_diffscope (G1, both layers).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import constants                                               # noqa: E402
import exp07_config as C                                       # noqa: E402
import exp08_arms as A                                         # noqa: E402
import exp10_arms as X10                                       # noqa: E402
import exp12_arms as X12                                       # noqa: E402
import exp12_fabric as F                                       # noqa: E402
import exp14_arms as X14                                       # noqa: E402
import exp21_probe as P21                                      # noqa: E402
from revival import dynamics_panel                             # noqa: E402
from sculpt_config import SculptConfig                         # noqa: E402

OUTDIR21 = _HERE / "exp08" / "exp21"
EVAL, BLOCK = X12.EVAL, X12.BLOCK

# --- §4.1 horizons / seeds (fixed by ratification; no transported constant) ---
BASE_ARM = "exp12_dwell"
CAL_SEEDS21 = [20, 21, 22, 24, 25]
VERDICT_SEEDS21 = list(range(8))
H21 = 1_000_000
PROBE_EVERY = 3_000                # §3.3 read cadence == the existing block cadence
N_ACQ = 5                          # §4.2 five-read sustained-acquisition form (design constant)
Q4_FROM = 750_000                  # §4.3 final quarter (750k, 1M]

assert PROBE_EVERY == BLOCK, "§3.3: the probe cadence IS the existing block cadence"


def gatelog_append(event: dict):
    """exp21_gatelog.json — append-only gate event log (§9.3)."""
    OUTDIR21.mkdir(parents=True, exist_ok=True)
    p = OUTDIR21 / "exp21_gatelog.json"
    log = json.loads(p.read_text()) if p.exists() else dict(exp="exp21", events=[])
    log["events"].append(event)
    p.write_text(json.dumps(log, indent=2))


def planned_reads(read_at: int) -> list[int]:
    """§3.3: t=0, every 3,000 waves, and exactly `read_at` (off-grid when read_at % 3000 != 0)."""
    ts = [0] + list(range(PROBE_EVERY, read_at + 1, PROBE_EVERY))
    if ts[-1] != read_at:
        ts.append(read_at)
    return ts


# ------------------------------------------------------------------ the OFF arm (§2.2, binding)
class EXP21TeachingOffLoop(X12.EXP12Loop):
    """Teaching OFF: the deployed loop with BOTH L_PAM->vision gradient edges structurally cut.
    Overrides exactly two existing hooks and no other learner method; `super()` first is
    mandatory (OFF retains the deployed cue presentation including the reposing transformation
    and changes only autograd connectivity — §2.2). Forward values match ON exactly before
    optimisation divergence (G2 check 1)."""

    def _pose_pam_input(self, content):
        posed = super()._pose_pam_input(content)
        out = posed.clone()
        out[..., 0, :] = posed[..., 0, :].detach()
        return out

    def _pam_target(self, content):
        target = super()._pam_target(content)
        out = target.clone()
        out[..., 0, :] = target[..., 0, :].detach()
        return out


def build_exp21(teaching: str, seed: int, steps: int,
                probe_rate: float = X12.PROBE_RATE_STAGE1):
    """Construct one arm. ON goes through the committed `build_exp12` path VERBATIM; OFF
    replicates that construction byte-equally (proven at G0) with the loop class swapped —
    `build_exp12` hardcodes EXP12Loop and the shared files are fenced (§9.2), so the swap
    lives here, experiment-scoped."""
    assert teaching in ("on", "off"), f"unknown arm {teaching}"
    if teaching == "on":
        return X12.build_exp12(BASE_ARM, seed, steps, probe_rate)
    spec = X12.ARMS12[BASE_ARM]
    pin = constants.PinnedConstants()
    cfg = SculptConfig(seed=seed)
    cfg.W = 1                                                  # the wave-local pin (EXP12 §3)
    cfg.T = steps + 8
    cfg._exp12 = dict(T=cfg.T, shuffled=spec["shuffled"], probe_rate=probe_rate,
                      uniform_mask=spec.get("uniform_mask", False),
                      word_ref=spec.get("word_ref", False),
                      expo_word=spec.get("expo_word", False),
                      expo_midword=spec.get("expo_midword", False),
                      dwell_orbit=spec.get("dwell_orbit", False),
                      orbit_r=spec.get("orbit_r"), orbit_w_deg=spec.get("orbit_w_deg"),
                      dwell_scatter=spec.get("dwell_scatter", False),
                      scatter_r=spec.get("scatter_r"),
                      wperm_B=spec.get("wperm_B"), ubuf_K=spec.get("ubuf_K"))
    loop = EXP21TeachingOffLoop(cfg, pin)
    return loop, spec, cfg


def state_digest(loop) -> str:
    """Canonical state digest (§3.5: raw serialization bytes are NOT the criterion): SHA-256
    over every model/optimizer tensor in sorted key order + the generator state + counters."""
    h = hashlib.sha256()
    for name, mod in (("vision", loop.vision), ("word", loop.word), ("op", loop.op)):
        sd = mod.state_dict()
        for k in sorted(sd):
            h.update(f"{name}.{k}".encode())
            h.update(sd[k].detach().to(torch.float64).numpy().tobytes())
    ost = loop.opt.state_dict()
    for gi, g in enumerate(ost["param_groups"]):
        h.update(json.dumps({k: v for k, v in g.items() if k != "params"},
                            sort_keys=True, default=str).encode())
    for pid in sorted(ost["state"]):
        for k in sorted(ost["state"][pid]):
            v = ost["state"][pid][k]
            h.update(f"opt.{pid}.{k}".encode())
            h.update(v.detach().to(torch.float64).numpy().tobytes()
                     if torch.is_tensor(v) else str(v).encode())
    h.update(loop.gen.get_state().numpy().tobytes())
    h.update(torch.get_rng_state().numpy().tobytes())          # global RNG: a probe consuming
    #                                                            it must break the digest
    h.update(str((loop._t, loop.stim._calls)).encode())
    return h.hexdigest()


# ------------------------------------------------------------------ the runner (faithful replica)
def run_exp21_arm(teaching: str, seed: int, *, read_at: int, h_max: int | None = None,
                  probe_rate: float = X12.PROBE_RATE_STAGE1, out_tag: str | None = None,
                  checkpoint: bool = True, mid_ckpt_at: int | None = None,
                  probe: tuple = ("primary",), _red: str | None = None,
                  return_loop: bool = False):
    """Faithful replica of exp14_arms.run_exp14_arm (digit-identity proven at G0), on the
    EXP21 arms, writing under exp08/exp21/. The external probe is the ONLY addition; `_red`
    exists solely for the G0 observed-red fixtures (live_stim/gen_consume/read_order_swap)
    and never rides a cal or verdict run (asserted below)."""
    h_max = h_max or read_at
    assert read_at <= h_max, "read_at must be <= h_max (fabric is pre-built to h_max)"
    assert mid_ckpt_at is None or 0 < mid_ckpt_at <= read_at
    assert _red in (None, "live_stim", "gen_consume", "read_order_swap")
    assert _red is None or (out_tag and "broken" in out_tag), \
        "_red fixtures must carry a 'broken' tag — they never ride a real run"
    OUTDIR21.mkdir(parents=True, exist_ok=True)
    base = OUTDIR21 / (f"exp21_{teaching}_s{seed}" + (f"_{out_tag}" if out_tag else ""))
    stale = [s for s in (".json", ".manifest.json", ".ckpt_read.pt", ".ckpt_onset.pt",
                         ".ckpt_mid.pt")
             if base.with_suffix(s).exists()]
    assert not stale, (f"stale artifacts for this cell {stale} — from-scratch only: "
                       "no resume, no re-run, no overwrite (append-only)")
    loop, spec, cfg = build_exp21(teaching, seed, h_max, probe_rate)
    fab = loop.stream

    if fab.shuffled:
        fab_plain = F.build_fabric(loop.stim, cfg, seed, fab.T, probe_rate=probe_rate,
                                   shuffled=False,
                                   uniform_mask=spec.get("uniform_mask", False),
                                   word_ref=spec.get("word_ref", False))
        assert torch.equal(fab.raw.sort(0).values, fab_plain.raw.sort(0).values)
        assert int(fab.is_exam.sum()) == int(fab_plain.is_exam.sum())
        asserts = F.fabric_asserts(fab_plain, cfg)
    else:
        asserts = F.fabric_asserts(fab, cfg)
    man = F.fabric_manifest(fab, loop.stim, cfg, asserts)
    man.update(arm=f"exp21_teach_{teaching}", base_arm=BASE_ARM, seed=seed,
               read_at=read_at, h_max=h_max, vocab=cfg.n_category,
               exp="exp21_pam_teaching",
               geometry="wave-local (W=1); no u-carrier; L_JEPA inert by construction",
               members=A._members(cfg),
               anchor=dict(embeddings=[[round(float(x), 6) for x in r]
                                       for r in loop.word.emit(torch.arange(cfg.n_category))],
                           construction="WordCortex(D, n_category, seed=seed+1) — deployed v2"))
    base.with_suffix(".manifest.json").write_text(json.dumps(man, indent=2, default=str))
    try:
        A.render_scatter(loop, base.with_suffix(".scatter.png"))
    except Exception as e:                                    # illustrative-only: never blocks
        man["scatter_note"] = f"render skipped: {e}"

    members_a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    members_b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    labels = loop._word_label(members_b, members_a)

    no_word = bool(spec.get("no_word", False))
    ubuf_eb = spec.get("ubuf_K") is not None                  # structurally False on exp12_dwell
    eb_onsets = []
    expo_midword = bool(spec.get("expo_midword", False))      # structurally False on exp12_dwell
    session = None
    if probe:
        banks = {k: P21.write_bank(seed, k) for k in probe}
        session = P21.ProbeSession(banks)
        session.read(loop, 0)                                 # §3.3: t=0, BEFORE the first step
    buf = X12._fresh_buf()
    cols, occ, gsplit, mixes = [], {}, {}, {}
    onset_saved = False
    for t in range(1, read_at + 1):
        prev = t - 1
        if _red == "read_order_swap" and t % BLOCK == 0:
            # G0 red fixture: the BLOCK reads moved BEFORE the step — dc_track's live-stimulus
            # counter consumption lands at the wrong point and the trajectory must diverge.
            occ[str(t)] = loop.dc_track(cfg.n_eval)
            gsplit[str(t)] = X12.grad_geometry_split(loop, no_word)
            mixes[str(t)] = loop.mix_snapshot()
        pl = X12._probe_exam_read(loop, prev) if bool(fab.is_probe_exam[prev]) else None
        if ubuf_eb and bool(fab.is_exam[prev]):
            eb_onsets.append([prev, round(X12._probe_exam_read(loop, prev), 6)])
        pmw = (X12._probe_midword_read(loop, prev)
               if (expo_midword and int(fab.mask_slot[prev]) == 1 and not bool(fab.is_exam[prev]))
               else None)
        loop.step(no_word=no_word)
        X12._buffer_wave(loop, prev, buf, probe_lift=pl, probe_midword=pmw)
        if t % EVAL == 0:
            cols.append(X12._eval_column(loop, t, buf, members_a, members_b, labels,
                                         no_word=no_word))
            buf = X12._fresh_buf()
            if checkpoint and not onset_saved and X14._proposed_conversion(cols):
                X14.save_checkpoint(loop, base.with_suffix(".ckpt_onset.pt"),
                                    arm=f"exp21_teach_{teaching}", seed=seed,
                                    event="proposed_conversion_onset", onset_t=cols[-1]["t"])
                onset_saved = True
        if checkpoint and mid_ckpt_at is not None and t == mid_ckpt_at:
            X14.save_checkpoint(loop, base.with_suffix(".ckpt_mid.pt"),
                                arm=f"exp21_teach_{teaching}", seed=seed,
                                event="mid_horizon", mid_t=t)
        if t % BLOCK == 0:
            if _red != "read_order_swap":
                occ[str(t)] = loop.dc_track(cfg.n_eval)
                gsplit[str(t)] = X12.grad_geometry_split(loop, no_word)
                mixes[str(t)] = loop.mix_snapshot()
            if session is not None:
                session.read(loop, t)                         # §3.3: the block-cadence read
            if _red == "live_stim":
                # G0 red fixture: a broken probe touching the LIVE training stimulus once per
                # read — its counter advances and later spread samples shift (§3.5 check 3).
                loop.stim.raw(torch.tensor([0]), torch.tensor([0]),
                              torch.Generator().manual_seed(1))
            elif _red == "gen_consume":
                torch.rand((), generator=loop.gen)            # broken probe consuming loop.gen

    if session is not None and read_at % PROBE_EVERY != 0:
        session.read(loop, read_at)                           # §3.3: exactly the horizon read
    if checkpoint:
        X14.save_checkpoint(loop, base.with_suffix(".ckpt_read.pt"),
                            arm=f"exp21_teach_{teaching}", seed=seed,
                            event="read_horizon", read_at=read_at)

    ts = [c["t"] for c in cols]
    panels = {k: dynamics_panel(ts, [c.get(k) for c in cols]) for k in X14.PANEL_KEYS}
    onset = X10.acquisition_onset(cols)
    rec = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), exp="exp21",
        arm=f"exp21_teach_{teaching}", base_arm=BASE_ARM, seed=seed,
        read_at=read_at, h_max=h_max, vocab=int(cfg.n_category),
        shuffled=bool(spec["shuffled"]), probe_rate=probe_rate,
        word_ref=bool(spec.get("word_ref", False)), no_word=no_word,
        eval_cadence=EVAL, block_cadence=BLOCK, mid_ckpt_at=mid_ckpt_at,
        torch_num_threads=torch.get_num_threads(),
        acquisition_onset=onset, dynamics_panel=panels,
        conversion_onset_PROPOSED=X14._proposed_conversion_onset(cols),
        columns=[{k: ((round(v, 6) if k in A._STANDING_COLS else float(f"{v:.6g}"))
                      if isinstance(v, float) else v) for k, v in c.items()}
                 for c in cols],
        occupancy=occ, grad_split=gsplit, masking_mix=mixes,
        **({"eb_onsets": eb_onsets} if ubuf_eb else {}),
    )
    base.with_suffix(".json").write_text(json.dumps(rec, indent=2))
    if session is not None:
        session.write(base)
    print(f"exp21 {teaching} s{seed}: onset={onset}  "
          f"conv_PROPOSED={rec['conversion_onset_PROPOSED']}  "
          f"exam_acc_end={cols[-1].get('exam_acc')}  asg_cat_end={cols[-1]['asg_cat']:.4f}")
    return (rec, loop) if return_loop else rec


# ------------------------------------------------------------------ G0 — REUSED / trajectory parity
FABRIC_FIELDS = ("a", "b", "member", "cat", "dwell_id", "pos", "mask_slot",
                 "is_exam", "is_probe_exam", "nuis", "bg", "raw")
SHARED_REC_FIELDS = ("columns", "occupancy", "grad_split", "masking_mix", "dynamics_panel",
                     "acquisition_onset", "conversion_onset_PROPOSED", "vocab", "shuffled",
                     "probe_rate", "no_word", "eval_cadence", "block_cadence")


def _fabric_equal(fa, fb) -> list[str]:
    bad = [f for f in FABRIC_FIELDS if not torch.equal(getattr(fa, f), getattr(fb, f))]
    if getattr(fa, "deliver", None) is not None or getattr(fb, "deliver", None) is not None:
        bad.append("deliver-present")
    if fa.substreams != fb.substreams:
        bad.append("substreams")
    return bad


def _shared_fields_equal(ra: dict, rb: dict) -> list[str]:
    ja, jb = json.loads(json.dumps(ra)), json.loads(json.dumps(rb))
    return [k for k in SHARED_REC_FIELDS if ja.get(k) != jb.get(k)]


def _is_tracked(p: Path) -> bool:
    """Git-tracked check with the pathspec resolved against the SAME cwd git runs in (the
    build-review panel's dead-guard finding: a repo-root-relative pathspec under cwd=_HERE
    never matches, so the refusal could never fire)."""
    import subprocess
    rel = str(p.resolve().relative_to(_HERE))
    return subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=_HERE,
                          capture_output=True).returncode == 0


def _clean_untracked_scratch(patterns: list[str]):
    """Remove this executor's own UNCOMMITTED by-products from a prior invocation so a re-run
    does not trip the append-only assert. Tracked files are never touched (committed records
    are append-only; this guard refuses them)."""
    for pat in patterns:
        for p in OUTDIR21.glob(pat):
            assert not _is_tracked(p), f"refusing to remove COMMITTED artifact {p.name}"
            p.unlink()


def write_gate_artifact(path: Path, obj: dict):
    """Gate-artifact writer: a COMMITTED artifact is append-only (overwrite refused unless
    byte-identical); an uncommitted working file may be replaced (pre-close iteration)."""
    text = json.dumps(obj, indent=2, default=str)
    if path.exists() and _is_tracked(path):
        assert path.read_text() == text, \
            f"refusing to overwrite COMMITTED gate artifact {path.name} with different content"
        return
    path.write_text(text)


def g0_parity(short: int = 6000) -> dict:
    """G0 executor (§7): constructor/fabric/init parity, faithful-runner digit-identity,
    probe-inertness, repeat-run determinism — every named fixture observed red FIRST."""
    torch.set_num_threads(1)
    OUTDIR21.mkdir(parents=True, exist_ok=True)
    _clean_untracked_scratch(["exp21_on_s0_g0*", "exp21_off_s0_g0*"])
    out = dict(gate="G0", executor="exp21_teaching.g0_parity", short=short,
               observed_red={}, checks={})

    # --- red 1: fabric_bit_flip — the comparator must FAIL on a planted bit flip ---
    on_a, _, _ = build_exp21("on", 0, steps=256)
    on_b, _, _ = build_exp21("on", 0, steps=256)
    assert _fabric_equal(on_a.stream, on_b.stream) == []
    on_b.stream.raw[0, 0] += 1e-3
    bad = _fabric_equal(on_a.stream, on_b.stream)
    assert bad, "G0 fabric comparator blind to a planted bit flip — dead gate, HALT"
    out["observed_red"]["fabric_bit_flip"] = dict(red=True, fields=bad)

    # --- check 1: constructor/fabric/init parity (mine-ON vs committed build path; OFF vs ON) ---
    ref_loop, ref_spec, ref_cfg = X12.build_exp12(BASE_ARM, 0, 256)
    mine_on, _, _ = build_exp21("on", 0, 256)
    off, _, _ = build_exp21("off", 0, 256)
    assert type(mine_on) is X12.EXP12Loop, "ON must be the deployed class itself"
    assert _fabric_equal(ref_loop.stream, mine_on.stream) == []
    assert _fabric_equal(ref_loop.stream, off.stream) == []
    assert torch.equal(ref_loop.stim.bg_const, off.stim.bg_const)
    d_ref, d_on, d_off = state_digest(ref_loop), state_digest(mine_on), state_digest(off)
    assert d_ref == d_on == d_off, "initial state digests diverge across constructors"
    overrides = {k for k in vars(EXP21TeachingOffLoop)
                 if not k.startswith("__") or k == "__init__"}
    assert overrides == {"_pose_pam_input", "_pam_target"}, \
        f"OFF class overrides more than the two ratified hooks: {overrides}"
    out["checks"]["constructor_parity"] = dict(ok=True, init_digest=d_ref,
                                               off_overrides=sorted(overrides))

    # --- check 2: faithful runner vs the designated current ON runner (digit-identical,
    #     shared fields AND checkpoint state — prereg §3.5 parity 1) ---
    x14 = X14.run_exp14_arm(BASE_ARM, 0, read_at=short, h_max=short, checkpoint=True,
                            out_tag="g21fchk")
    rec_on, loop_on = run_exp21_arm("on", 0, read_at=short, checkpoint=False, probe=(),
                                    out_tag="g0onchk", return_loop=True)
    bad = _shared_fields_equal(x14, rec_on)
    assert not bad, f"faithful-runner divergence on shared fields: {bad}"
    ck = torch.load(X14.OUTDIR / f"exp14_{BASE_ARM}_s0_g21fchk.ckpt_read.pt",
                    weights_only=False)
    for mod, sd in (("vision", loop_on.vision.state_dict()),
                    ("word", loop_on.word.state_dict()), ("op", loop_on.op.state_dict())):
        for k in sd:
            assert torch.equal(ck[mod][k], sd[k]), f"ckpt-state divergence {mod}.{k}"
    assert torch.equal(ck["gen_state"], loop_on.gen.get_state()) and ck["t"] == loop_on._t
    out["checks"]["faithful_runner"] = dict(ok=True, fields=list(SHARED_REC_FIELDS),
                                            checkpoint_state="tensor-equal (vision/word/op"
                                            "/gen/t vs the designated runner's .ckpt_read)")

    # --- check 2b: repeat-run determinism (separate-process scheduling justification) ---
    rec_on2, loop_on2 = run_exp21_arm("on", 0, read_at=short, checkpoint=False, probe=(),
                                      out_tag="g0onchk2", return_loop=True)
    assert json.loads(json.dumps(rec_on)) == json.loads(json.dumps(rec_on2))
    assert state_digest(loop_on) == state_digest(loop_on2)
    out["checks"]["repeat_determinism"] = dict(ok=True)

    # --- check 3: probe-enabled == probe-disabled on EVERY record field + full state ---
    rec_p, loop_p = run_exp21_arm("on", 0, read_at=short, checkpoint=False,
                                  probe=("primary",), out_tag="g0onprobe", return_loop=True)
    assert json.loads(json.dumps(rec_on)) == json.loads(json.dumps(rec_p)), \
        "probe-enabled record differs from probe-disabled"
    assert state_digest(loop_on) == state_digest(loop_p), \
        "probe-enabled terminal state differs (model/opt/gen/counters)"
    assert torch.equal(loop_on.gen.get_state(), loop_p.gen.get_state())
    assert loop_on.stim._calls == loop_p.stim._calls
    out["checks"]["probe_inertness"] = dict(ok=True, state_digest=state_digest(loop_p))

    # --- check 3b: the DEPLOYED cal probe shape — dual banks + off-grid horizon read
    #     (panel flag: check 3 alone never exercised primary+shadow or the exact-read_at
    #     off-grid read the 1M runs perform) ---
    short2 = 4200                                              # reads at 0, 3000, 4200
    rec_q, loop_q = run_exp21_arm("on", 0, read_at=short2, checkpoint=False, probe=(),
                                  out_tag="g0onchk2b", return_loop=True)
    rec_q2, loop_q2 = run_exp21_arm("on", 0, read_at=short2, checkpoint=False,
                                    probe=("primary", "shadow"), out_tag="g0onprobe2b",
                                    return_loop=True)
    assert json.loads(json.dumps(rec_q)) == json.loads(json.dumps(rec_q2)), \
        "dual-bank probe run record differs from probe-disabled at an off-grid horizon"
    assert state_digest(loop_q) == state_digest(loop_q2), \
        "dual-bank probe terminal state differs at an off-grid horizon"
    pt = json.loads((OUTDIR21 / "exp21_on_s0_g0onprobe2b.probe_primary.json").read_text())
    assert pt["ts"] == [0, 3000, 4200], f"off-grid read grid wrong: {pt['ts']}"
    out["checks"]["probe_inertness_dualbank_offgrid"] = dict(ok=True, ts=pt["ts"])

    # --- reds 2-4: broken probes / swapped read order MUST diverge from the faithful record ---
    for red, tag in (("live_stim", "g0broken_stim"), ("gen_consume", "g0broken_gen"),
                     ("read_order_swap", "g0broken_order")):
        rec_r = run_exp21_arm("on", 0, read_at=short, checkpoint=False,
                              probe=(("primary",) if red != "read_order_swap" else ()),
                              out_tag=tag, _red=red)
        diff = _shared_fields_equal(rec_on, rec_r)
        assert diff, f"G0 parity BLIND to {red} — the broken condition left the record " \
                     "identical; dead gate, HALT"
        out["observed_red"][{"live_stim": "live_stim_probe_call",
                             "gen_consume": "probe_gen_consumption",
                             "read_order_swap": "read_order_swap"}[red]] = \
            dict(red=True, diverged_fields=diff[:6])

    write_gate_artifact(OUTDIR21 / "exp21_g0_parity.json", out)
    gatelog_append(dict(gate="G0", outcome="PASS", executor="exp21_teaching.g0_parity",
                        reds=sorted(out["observed_red"]), checks=sorted(out["checks"])))
    print("G0 PASS:", sorted(out["checks"]), "reds:", sorted(out["observed_red"]))
    return out


# ------------------------------------------------------------------ G2 — gradient/compute census
def _mask_paths(fab, t0: int) -> dict:
    """First REAL scheduled wave of each mask path at or after t0 (§7 G2: both live paths)."""
    tv = tw = None
    t = t0
    while tv is None or tw is None:
        if int(fab.mask_slot[t]) == 0 and tv is None:
            tv = t
        if int(fab.mask_slot[t]) == 1 and tw is None:
            tw = t
        t += 1
    return dict(vision_masked=tv, word_masked=tw)


def _raw_lpam_grads(loop, t: int):
    """Raw UNSCALED L_PAM at real wave t; per-parameter grads over EVERY visual-cortex
    parameter and every PAM parameter (allow_unused: None == structurally unused)."""
    bc = loop.build_cells(t, no_word=False, gen=loop.gen)     # zero loop.gen draws at W=1
    l_pam, _ = loop._l_pam(bc)
    vis = [p for p in loop.vision.parameters() if p.requires_grad]
    ops = [p for p in loop.op.parameters() if p.requires_grad]
    if not l_pam.requires_grad:                               # fully severed (pam_dead plant):
        gv, go = [None] * len(vis), [None] * len(ops)         # every edge structurally unused
    else:
        gv = (torch.autograd.grad(l_pam, vis, retain_graph=True, allow_unused=True)
              if vis else [])
        go = (torch.autograd.grad(l_pam, ops, retain_graph=False, allow_unused=True)
              if ops else [])
    nv = [0.0 if g is None else float(g.norm()) for g in gv]
    no_ = [0.0 if g is None else float(g.norm()) for g in go]
    return dict(l_pam=float(l_pam.detach()), vis_norms=nv, vis_total=sum(nv),
                op_norms=no_, op_total=sum(no_),
                vis_all_unused=all(g is None or float(g.abs().max()) == 0.0 for g in gv))


def gradient_census(on_loop, off_loop, warm: int = 10,
                    paths: tuple = ("vision_masked", "word_masked")) -> dict:
    """The G2 measurement (§7): forward equality at init; raw L_PAM edge census on BOTH real
    scheduled mask paths; PAM liveness + actual gain-positive update in OFF; autonomous vision
    liveness in OFF; matched counts. Returns named checks; the executor asserts."""
    cks = {}
    fab = on_loop.stream
    mp0 = _mask_paths(fab, 0)
    # (1) forward equality at identical initial state
    eq = {}
    for name, t in mp0.items():
        bo = on_loop.build_cells(t, no_word=False, gen=on_loop.gen)
        bf = off_loop.build_cells(t, no_word=False, gen=off_loop.gen)
        lo, po = on_loop._l_pam(bo)
        lf, pf = off_loop._l_pam(bf)
        eq[name] = bool(torch.equal(bo["cells"].detach(), bf["cells"].detach())
                        and torch.equal(bo["target"].detach(), bf["target"].detach())
                        and torch.equal(po.detach(), pf.detach())
                        and float(lo.detach()) == float(lf.detach()))
    cks["forward_equal_at_init"] = dict(ok=all(eq.values()), detail=eq)
    # (2) warm both arms on the REAL path (gain(t) > 0 for t >= 1; ramp 0->1 over 400)
    n_fwd = dict(on=0, off=0)
    for lname, lp in (("on", on_loop), ("off", off_loop)):
        orig = lp.op.forward
        lp.op.forward = (lambda o, nm: lambda *a, **k:
                         (n_fwd.__setitem__(nm, n_fwd[nm] + 1), o(*a, **k))[1])(orig, lname)
        for _ in range(warm):
            lp.step(no_word=False)
        del lp.op.forward
    cks["matched_counts"] = dict(
        ok=(n_fwd["on"] == n_fwd["off"] and on_loop._t == off_loop._t
            and [tuple(p.shape) for p in on_loop.vision.parameters()]
            == [tuple(p.shape) for p in off_loop.vision.parameters()]
            and [tuple(p.shape) for p in on_loop.op.parameters()]
            == [tuple(p.shape) for p in off_loop.op.parameters()]
            and len(on_loop.opt.param_groups[0]["params"])
            == len(off_loop.opt.param_groups[0]["params"])),
        pam_forwards=n_fwd, steps=dict(on=on_loop._t, off=off_loop._t),
        params=dict(vision=sum(p.numel() for p in on_loop.vision.parameters()),
                    op=sum(p.numel() for p in on_loop.op.parameters()),
                    optimizer_members=len(on_loop.opt.param_groups[0]["params"])))
    # (3) the raw L_PAM edge census on both REAL post-warm scheduled paths
    mp = _mask_paths(fab, on_loop._t)
    census = {}
    for name in paths:
        t = mp[name]
        g_on = _raw_lpam_grads(on_loop, t)
        g_off = _raw_lpam_grads(off_loop, t)
        census[name] = dict(t=t, on=g_on, off=g_off)
    cks["on_lpam_to_vision_pos"] = dict(
        ok=all(census[p]["on"]["vis_total"] > 0 for p in paths),
        totals={p: census[p]["on"]["vis_total"] for p in paths})
    cks["off_lpam_to_vision_zero"] = dict(
        ok=all(census[p]["off"]["vis_all_unused"] for p in paths),
        totals={p: census[p]["off"]["vis_total"] for p in paths})
    cks["off_lpam_to_pam_pos"] = dict(
        ok=all(census[p]["off"]["op_total"] > 0 for p in paths),
        totals={p: census[p]["off"]["op_total"] for p in paths})
    # (4) OFF autonomous-vision force (spread + pool penalty), measured without touching loop.gen
    g2 = torch.Generator()
    g2.set_state(off_loop.gen.get_state())
    l_sp = off_loop._l_spread(g2)
    vis = [p for p in off_loop.vision.parameters() if p.requires_grad]
    gs = torch.autograd.grad(off_loop.pin.alpha_spread * l_sp
                             + off_loop.vision.pool.pool_penalty(
                                 off_loop.unpool.lam1(off_loop._t),
                                 off_loop.unpool.lam2(off_loop._t)),
                             vis, allow_unused=True) if vis else []
    sp_total = sum(0.0 if g is None else float(g.norm()) for g in gs)
    cks["off_vision_nonpam_grad_pos"] = dict(ok=sp_total > 0, total=sp_total)
    # (5) one actual gain-positive OFF step: PAM params AND vision params both move
    gain_now = off_loop.gain.gain(off_loop._t)
    snap_op = [p.detach().clone() for p in off_loop.op.parameters()]
    snap_vis = [p.detach().clone() for p in off_loop.vision.parameters()]
    off_loop.step(no_word=False)
    d_op = sum(float((p.detach() - s).norm()) for p, s in zip(off_loop.op.parameters(), snap_op))
    d_vis = sum(float((p.detach() - s).norm())
                for p, s in zip(off_loop.vision.parameters(), snap_vis))
    cks["off_gain_positive_pam_update"] = dict(ok=(gain_now > 0 and d_op > 0),
                                               gain=gain_now, op_delta=d_op)
    cks["off_vision_nonpam_update_pos"] = dict(ok=d_vis > 0, vision_delta=d_vis)
    return dict(checks=cks, census=census, warm=warm, paths=list(paths))


# --- G2 observed-red plants (§2.4 rejected controls, as fixtures ONLY) ---
class _PlantTargetOnly(X12.EXP12Loop):
    def _pam_target(self, content):
        tgt = content.clone()
        tgt[..., 0, :] = content[..., 0, :].detach()
        return tgt


class _PlantCueOnly(X12.EXP12Loop):
    def _pose_pam_input(self, content):
        posed = super()._pose_pam_input(content)
        out = posed.clone()
        out[..., 0, :] = posed[..., 0, :].detach()
        return out


class _PlantNoopHooks(X12.EXP12Loop):
    def _pose_pam_input(self, content):
        return super()._pose_pam_input(content).clone()        # clone WITHOUT detach

    def _pam_target(self, content):
        return super()._pam_target(content).clone()            # clone WITHOUT detach


def _build_plant(cls, seed: int, steps: int):
    spec = X12.ARMS12[BASE_ARM]
    pin = constants.PinnedConstants()
    cfg = SculptConfig(seed=seed)
    cfg.W = 1
    cfg.T = steps + 8
    cfg._exp12 = dict(T=cfg.T, shuffled=False, probe_rate=0.0, uniform_mask=False,
                      word_ref=False, expo_word=False, expo_midword=False, dwell_orbit=False,
                      orbit_r=None, orbit_w_deg=None, dwell_scatter=False, scatter_r=None,
                      wperm_B=None, ubuf_K=None)
    return cls(cfg, pin)


def g2_gradient_census(seed: int = 20, steps: int = 2000) -> dict:
    """G2 executor (§7): every named fixture observed red FIRST, then the real pair green."""
    torch.set_num_threads(1)
    OUTDIR21.mkdir(parents=True, exist_ok=True)
    reds = {}

    def fresh_pair(off_cls=EXP21TeachingOffLoop):
        on, _, _ = build_exp21("on", seed, steps)
        off = _build_plant(off_cls, seed, steps) if off_cls is not EXP21TeachingOffLoop \
            else build_exp21("off", seed, steps)[0]
        return on, off

    def expect_red(name, off_cls, failing_checks, mutate=None):
        on, off = fresh_pair(off_cls)
        if mutate:
            mutate(off)
        r = gradient_census(on, off)
        bad = [k for k in failing_checks if not r["checks"][k]["ok"]]
        assert bad, (f"G2 fixture {name}: census stayed GREEN under the broken condition "
                     f"(expected {failing_checks} to fail) — dead gate, HALT")
        reds[name] = dict(red=True, failed_checks=bad)

    expect_red("baseline_no_detach", X12.EXP12Loop, ["off_lpam_to_vision_zero"])
    expect_red("target_only", _PlantTargetOnly, ["off_lpam_to_vision_zero"])
    expect_red("cue_only", _PlantCueOnly, ["off_lpam_to_vision_zero"])
    expect_red("noop_hooks", _PlantNoopHooks, ["off_lpam_to_vision_zero"])
    expect_red("pam_dead", EXP21TeachingOffLoop,
               ["off_lpam_to_pam_pos", "off_gain_positive_pam_update"],
               mutate=lambda off: [p.requires_grad_(False) for p in off.op.parameters()])
    expect_red("vision_frozen", EXP21TeachingOffLoop,
               ["off_vision_nonpam_grad_pos", "off_vision_nonpam_update_pos"],
               mutate=lambda off: [p.requires_grad_(False) for p in off.vision.parameters()])
    # single_mask_path_only: a census restricted to ONE path is BLIND to the partial detach
    on, off_t = fresh_pair(_PlantTargetOnly)
    blind = gradient_census(on, off_t, paths=("vision_masked",))
    assert blind["checks"]["off_lpam_to_vision_zero"]["ok"], \
        "expected the single-path census to (wrongly) pass the target-only plant"
    on2, off_t2 = fresh_pair(_PlantTargetOnly)
    full = gradient_census(on2, off_t2)
    assert not full["checks"]["off_lpam_to_vision_zero"]["ok"]
    reds["single_mask_path_only"] = dict(
        red=True, blind_single_path_passed=True, full_census_caught=True,
        leak_path="word_masked (cue side)",
        leak_norm=full["census"]["word_masked"]["off"]["vis_total"])

    # --- the REAL pair, all checks green ---
    on, off = fresh_pair()
    real = gradient_census(on, off)
    bad = [k for k, v in real["checks"].items() if not v["ok"]]
    assert not bad, f"G2 REAL census failed: {bad} — HALT"
    out = dict(gate="G2", executor="exp21_teaching.g2_gradient_census", seed=seed,
               steps=steps, observed_red=reds, real=real)
    write_gate_artifact(OUTDIR21 / "exp21_g2_gradient_census.json", out)
    gatelog_append(dict(gate="G2", outcome="PASS", executor="exp21_teaching.g2_gradient_census",
                        reds=sorted(reds), checks=sorted(real["checks"])))
    print("G2 PASS:", {k: v["ok"] for k, v in real["checks"].items()}, "reds:", sorted(reds))
    return out


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--g0", action="store_true")
    ap.add_argument("--g2", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ARM", "SEED"))
    ap.add_argument("--read-at", type=int, default=H21)
    ap.add_argument("--tag", type=str, default=None)
    ap.add_argument("--shadow", action="store_true",
                    help="score the shadow bank too (calibration runs)")
    args = ap.parse_args()
    torch.set_num_threads(1)                                   # the determinism contract
    if args.g0:
        g0_parity()
    elif args.g2:
        g2_gradient_census()
    elif args.run:
        teaching, seed = args.run[0], int(args.run[1])
        banks = ("primary", "shadow") if args.shadow else ("primary",)
        run_exp21_arm(teaching, seed, read_at=args.read_at, out_tag=args.tag, probe=banks)


if __name__ == "__main__":
    _main()
