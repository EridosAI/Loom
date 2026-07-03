"""EXP08 — collapse diagnostic arms: the SHARED runner (one code path for every arm).

Pre-registration: docs/EXP08_COLLAPSE_ARMS_PREREG.md (predictions fixed before this file
existed). All arms are DIAGNOSTIC — no arm is a fix. Verdicts return to ONE review.

Arms (single variable each, vs the deployed reference = SculptConfig defaults):
  marathon   no-word full horizon (cap 112500, seed 0) — THE DISCRIMINATOR
  detach     PAM target's vision slot detached (gap-3 target-side pull amputated)
  spread     alpha_spread 0.1 -> 1.0 (parity with gain)
  ties       vision lam2_lo 0 -> 0.1 (KNOB choice: 1% of lam_hi; logged, not tuned)
  vocab2/4/8/16  the anchor-density ladder (label maps below; geometry untouched)

Columns (every run; dynamics panels on all): three-column channel read (numerator /
denominator / ratio, ruler v2, labels = the rig's own word map) + proto_spread +
SUBSTRATE-side vision Delta2 (pooling_depth, within_group_spread — splits substrate-remerge
from emission-contraction) at EVAL cadence; occupancy (dc_track), the word-path vs
self-path GRADIENT SPLIT (two forced-mask probes) and the MASKING-MIX fractions at BLOCK
cadence.

Stimulus manifest (provenance, logging-only, written before wave 0, derived LIVE from the
constructors — never re-typed): member->word table across ALL rungs, anchor embedding
vectors + pairwise separations, visual construction as data, staging timeline, and a
stream-consistency assert (first N sampled waves checked against the manifest's map).
A per-rung PCA scatter is emitted ILLUSTRATIVE-ONLY (a projection for orientation, not an
instrument).
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

import constants                                             # noqa: E402  (exp04)
from loom import poolmetrics                                 # noqa: E402
import exp07_config as C                                     # noqa: E402
from revival import partition_read, dynamics_panel           # noqa: E402
from sculpt_config import SculptConfig                       # noqa: E402
from sculpt_loop import SculptLoop                           # noqa: E402
from encoders import WordCortex                              # noqa: E402
from controllers import Curriculum                           # noqa: E402

OUTDIR = _HERE / "exp08"
EVAL, BLOCK = 300, 3000
MANIFEST_ASSERT_WAVES = 200

# --- the vocab-ladder label maps (nested refinement; geometry untouched; prereg table) ---
LADDER = {
    2: lambda b, a: b % 2,                    # category only (the deployed reference map)
    4: lambda b, a: b,                        # both fine axes (distractor x category)
    8: lambda b, a: (a % 2) * 4 + b,          # half the coarse axis + both fine axes
    16: lambda b, a: a * 4 + b,               # full member identity (the Phase-1 word)
}


# ------------------------------------------------------------------ loop variants
class EXP08Loop(SculptLoop):
    """SculptLoop + the masking-mix counter (logging only; dynamics untouched)."""

    def __init__(self, cfg, pin):
        super().__init__(cfg, pin)
        self.mix = dict(n=0, vis_masked=0, word_visible=0, sib_visible=0, both=0)

    def build_cells(self, t, *, no_word, gen, ablate="none", force_mask=None):
        bc = super().build_cells(t, no_word=no_word, gen=gen, ablate=ablate,
                                 force_mask=force_mask)
        if force_mask is None:                                # training/eval draws only
            cfg = self.cfg
            m = bc["mask"].view(cfg.W, cfg.n_slots)
            vis_masked = bool(m[:, 0].any())
            if vis_masked:
                word_vis = bool((~m[:, 1]).any())
                sib_vis = bool((~m[:, 0]).any())
                self.mix["vis_masked"] += 1
                self.mix["word_visible"] += int(word_vis)
                self.mix["sib_visible"] += int(sib_vis)
                self.mix["both"] += int(word_vis and sib_vis)
            self.mix["n"] += 1
        return bc

    def mix_snapshot(self):
        s, self.mix = self.mix, dict(n=0, vis_masked=0, word_visible=0, sib_visible=0, both=0)
        return s


class DetachLoop(EXP08Loop):
    """The detached-target arm: gap-3 TARGET-side pull on vision amputated (diagnostic)."""

    def _pam_target(self, content):
        tgt = content.clone()
        tgt[..., 0, :] = content[..., 0, :].detach()          # vision slot detached; word frozen anyway
        return tgt


class VocabLoop(EXP08Loop):
    """The anchor-density ladder: word names a finer partition; geometry untouched."""

    def __init__(self, cfg, pin, vocab: int):
        self._vocab = vocab                                   # set BEFORE factories run
        super().__init__(cfg, pin)

    def _make_word(self):
        return WordCortex(self.cfg.D, self._vocab, seed=self.cfg.seed + 1)

    def _make_curric(self):
        return Curriculum(self._vocab, threshold=self.cfg.curric_threshold,
                          start_active=self.cfg.curric_start_active,
                          null_token=self.word.null_token)

    def _word_label(self, b, a=None):
        return LADDER[self._vocab](b, a)


NOWORD_PERIOD = 23100     # [RECONCILE: marathon_s0 den dominant period — the extension's window]

_STANDING_COLS = ("t", "num", "den", "ratio", "proto", "d2_depth", "d2_spread",
                  "asg_dist", "asg_argmax_k", "asg_entropy")   # committed rounding contract


def extension_read(cols, *, floor=1e-3, period=NOWORD_PERIOD) -> dict:
    """The one-review extension's PRE-REGISTERED terminal-vs-asymptotic read (no rescue):
    TERMINAL = final period-window den all sub-floor AND num-freeze (the reference
    signature); ASYMPTOTIC = >=5 consecutive period-windows with non-shrinking troughs
    (10% tol); neither -> NEITHER_BY_CAP, surfaced as a finding."""
    ws = {}
    for c in cols:
        ws.setdefault((c["t"] - 1) // period, []).append(c)
    windows = [ws[k] for k in sorted(ws)]
    troughs = [min(c["den"] for c in w) for w in windows]
    fin = windows[-1]
    terminal = (all(c["den"] < floor for c in fin)
                and (max(c["num"] for c in fin) - min(c["num"] for c in fin)) < 1e-3)
    asymptotic = any(all(troughs[i + j + 1] >= troughs[i + j] * 0.9 for j in range(4))
                     for i in range(max(0, len(troughs) - 4)))
    verdict = "TERMINAL" if terminal else ("ASYMPTOTIC" if asymptotic else "NEITHER_BY_CAP")
    return dict(period=period, window_troughs=[float(f"{t:.6g}") for t in troughs],
                terminal_check=bool(terminal), asymptotic_check=bool(asymptotic),
                verdict=verdict)


ARMS = {
    "marathon": dict(loop=EXP08Loop, no_word=True, steps=112500, seeds=[0]),
    # the one-review converters (prereg extension, 2026-07-03):
    "marathon_ext": dict(loop=EXP08Loop, no_word=True, steps=500000, seeds=[0],
                         extension_read=True),
    "word_terminal": dict(loop=EXP08Loop, no_word=False, steps=112500, seeds=[1]),
    "detach":   dict(loop=DetachLoop, no_word=False, steps=30000, seeds=[0, 1, 2]),
    "spread":   dict(loop=EXP08Loop, no_word=False, steps=30000, seeds=[0, 1, 2],
                     pin=dict(alpha_spread=1.0)),
    "ties":     dict(loop=EXP08Loop, no_word=False, steps=30000, seeds=[0, 1, 2],
                     cfg=dict(lam2_lo=0.1)),
    "vocab2":   dict(loop=VocabLoop, vocab=2, no_word=False, steps=30000, seeds=[0, 1, 2]),
    "vocab4":   dict(loop=VocabLoop, vocab=4, no_word=False, steps=30000, seeds=[0, 1, 2]),
    "vocab8":   dict(loop=VocabLoop, vocab=8, no_word=False, steps=30000, seeds=[0, 1, 2]),
    "vocab16":  dict(loop=VocabLoop, vocab=16, no_word=False, steps=30000, seeds=[0, 1, 2]),
}


# ------------------------------------------------------------------ manifest (before wave 0)
def _members(cfg):
    rows = []
    for m in range(cfg.n_A * cfg.n_B):
        a, b = m // cfg.n_B, m % cfg.n_B
        d, c = b // cfg.n_category, b % cfg.n_category
        rows.append(dict(member=m, a=a, b=b, distractor=d, category=c,
                         **{f"word_v{v}": int(LADDER[v](b, a)) for v in LADDER}))
    return rows


def build_manifest(loop, arm_name, spec, seed) -> dict:
    cfg = loop.cfg
    vocab = getattr(loop, "_vocab", cfg.n_category)
    toks = torch.arange(vocab)
    emb = loop.word.emit(toks)
    pair = torch.cdist(emb, emb)
    man = dict(
        arm=arm_name, seed=seed, vocab=int(vocab), no_word=bool(spec.get("no_word", False)),
        members=_members(cfg),
        visual_side=dict(
            axis_roles="coarse decoy = a (word-irrelevant); distractor = b//n_category "
                       "(salient, associatively inert at vocab 2); category = b%n_category "
                       "(subtle, word-named at every rung)",
            n_A=cfg.n_A, n_distractor=cfg.n_distractor, n_category=cfg.n_category,
            R_coarse=cfg.R_coarse, r_distractor=cfg.r_distractor, r_category=cfg.r_category,
            shared_mag_reference=C.DIFFUSE_SHARED, cue_mag_reference=C.DIFFUSE_CUE,
            sigma_stim=cfg.sigma_stim,
            block_geometry="disjoint index blocks [a | distractor | category] rotated by Q "
                           "(seeded by cfg.seed; see conflict_stream.ConflictStimulus)"),
        anchor_side=dict(
            construction="WordCortex(D, vocab, seed=cfg.seed+1) — same generator rule at "
                         "every rung (2 = deployed reference; 16 = the Phase-1 word)",
            embeddings=[[round(float(x), 6) for x in row] for row in emb],
            pairwise_separation=[[round(float(x), 4) for x in row] for row in pair],
            pairwise_min=float(pair[~torch.eye(vocab, dtype=torch.bool)].min()) if vocab > 1 else None,
            pairwise_mean=float(pair[~torch.eye(vocab, dtype=torch.bool)].mean()) if vocab > 1 else None,
            geometry_caveat="if pairwise geometry shifts materially across rungs, surface as "
                            "a caveat — do NOT fix mid-arm (Gate-4 pin)"),
        staging=dict(
            capacity_clock=dict(t1=cfg.t1, t2=cfg.t2, lam_hi=cfg.lam2_hi, lam_lo=cfg.lam2_lo),
            pam_tie=dict(regime=cfg.pam_tie, t1=cfg.pam_t1 or cfg.t1, t2=cfg.pam_t2 or cfg.t2),
            reposing_alpha=cfg.reposing_alpha, gain_ramp=cfg.ramp_steps,
            curriculum=dict(vocab=int(vocab), threshold=cfg.curric_threshold,
                            start_active=cfg.curric_start_active),
            dt_offset=0, dt_assoc="0 — the word event rides its member (token computed from "
                                  "the SAME wave's (a,b) in build_cells; every rung)",
            word_available_from=0 if not spec.get("no_word") else None,
            stream=dict(rule="uniform (a,b) via make_stream", seed=cfg.seed + 3, T=cfg.T,
                        W=cfg.W, eval_cadence=EVAL, block_cadence=BLOCK),
        ),
        arm_overrides={k: v for k, v in spec.items() if k in ("pin", "cfg", "vocab", "no_word")},
    )
    return man


def assert_stream_consistency(loop, man, n=MANIFEST_ASSERT_WAVES):
    """The manifest is verified against the LIVE stream, not a parallel claim."""
    table = {r["member"]: r for r in man["members"]}
    cfg = loop.cfg
    for t in range(n):
        win = loop.stream.window(t % (loop.stream.T - cfg.W), cfg.W)
        a, b = win["a"], win["b"]
        wl = loop._word_label(b, a)
        for w in range(cfg.W):
            m = int(a[w]) * cfg.n_B + int(b[w])
            expect = table[m][f"word_v{getattr(loop, '_vocab', cfg.n_category)}"] \
                if f"word_v{getattr(loop, '_vocab', cfg.n_category)}" in table[m] \
                else table[m]["word_v2"]
            assert int(wl[w]) == expect, (t, w, m, int(wl[w]), expect)
    return n


def manifest_md(man) -> str:
    L = [f"# stimulus manifest — arm {man['arm']} seed {man['seed']} (vocab {man['vocab']})",
         "", "ILLUSTRATIVE scatter: see the PNG; a projection for orientation, NOT an instrument.",
         "", "| member | a | b | distractor | category | w@2 | w@4 | w@8 | w@16 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in man["members"]:
        L.append(f"| {r['member']} | {r['a']} | {r['b']} | {r['distractor']} | {r['category']} "
                 f"| {r['word_v2']} | {r['word_v4']} | {r['word_v8']} | {r['word_v16']} |")
    a = man["anchor_side"]
    L += ["", f"anchor pairwise separation: min {a['pairwise_min']}, mean {a['pairwise_mean']}",
          f"staging: {json.dumps(man['staging'], default=str)}"]
    return "\n".join(L)


# ------------------------------------------------------------------ illustrative scatter
PALETTE = ["#2a78d6", "#1baf7a", "#eda100", "#008300",      # validated categorical (light),
           "#4a3aa7", "#e34948", "#e87ba4", "#eb6834"]      # fixed order, never cycled


def render_scatter(loop, path: Path):
    """ILLUSTRATIVE ONLY — the member space laid out in its GENERATIVE coordinates (a × b),
    colored by word class per rung, every cell direct-labeled (identity never color-alone;
    >8 classes fold to color%8 + marker split, labels carry exact identity). A variance
    projection was rejected: 16 members = 4 coarse-groups × 4 fine-positions, so any 2D
    PCA overplots 4-into-1; the generative grid is the construction stated as a picture."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cfg = loop.cfg
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.4))
    for ax, v in zip(axes, LADDER):
        for m in range(cfg.n_A * cfg.n_B):
            a, b = m // cfg.n_B, m % cfg.n_B
            k = int(LADDER[v](b, a))
            ax.scatter(b, a, s=340, color=PALETTE[k % 8],
                       marker="o" if k < 8 else "s", zorder=3)
            ax.annotate(f"m{m}\nw{k}", (b, a), ha="center", va="center",
                        fontsize=6.5, color="#ffffff", zorder=4)
        ax.set_title(f"vocab {v}", fontsize=10, color="#222222")
        ax.set_xticks(range(cfg.n_B))
        ax.set_xticklabels([f"b={b}\nd{b // cfg.n_category},c{b % cfg.n_category}"
                            for b in range(cfg.n_B)], fontsize=7)
        ax.set_yticks(range(cfg.n_A))
        ax.set_yticklabels([f"a={a}" for a in range(cfg.n_A)], fontsize=8)
        ax.set_xlim(-0.6, cfg.n_B - 0.4)
        ax.set_ylim(-0.6, cfg.n_A - 0.4)
        for s_ in ax.spines.values():
            s_.set_color("#dddddd")
        ax.grid(True, color="#eeeeee", lw=0.6, zorder=0)
        ax.tick_params(color="#cccccc")
    fig.suptitle("member (a × b) × word assignment per rung — ILLUSTRATIVE ONLY "
                 "(generative coordinates, not an instrument)", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


# ------------------------------------------------------------------ gradient-split probes
def grad_split(loop, no_word: bool) -> dict:
    """Two forced-mask probes: word-path (all vision masked, word visible) vs self-path
    (one vision cell masked, word masked, sibling vision visible). ||dL_PAM/dDelta2||."""
    cfg = loop.cfg
    out = {}
    masks = dict(
        word_path=torch.zeros(cfg.W, cfg.n_slots, dtype=torch.bool),
        self_path=torch.zeros(cfg.W, cfg.n_slots, dtype=torch.bool))
    masks["word_path"][:, 0] = True
    masks["self_path"][1, 0] = True
    masks["self_path"][:, 1] = True
    for name, m in masks.items():
        bc = loop.build_cells(loop._t, no_word=no_word, gen=loop.gen, force_mask=m)
        l_pam, _ = loop._l_pam(bc)
        g = torch.autograd.grad(l_pam, loop.vision.pool.delta2, retain_graph=False,
                                allow_unused=True)[0]
        out[name] = 0.0 if g is None else float(g.norm())
    return out


# ------------------------------------------------------------------ the run
def build_loop(arm_name: str, seed: int):
    """Construct an arm's loop exactly as run_arm does (ONE code path — the kick probe
    rebuilds states through this same constructor before loading saved weights)."""
    spec = ARMS[arm_name]
    pin = constants.PinnedConstants(**spec.get("pin", {}))
    cfg = SculptConfig(seed=seed)
    for k, v in spec.get("cfg", {}).items():
        setattr(cfg, k, v)
    if spec["loop"] is VocabLoop:
        loop = VocabLoop(cfg, pin, spec["vocab"])
    else:
        loop = spec["loop"](cfg, pin)
    return loop, spec, cfg


def save_state(loop, path: Path):
    """Full continuation state (params + Adam moments + RNG + wave counter) so a resume
    is bit-faithful to having kept running."""
    torch.save(dict(_t=loop._t, vision=loop.vision.state_dict(), op=loop.op.state_dict(),
                    word=loop.word.state_dict(), opt=loop.opt.state_dict(),
                    gen_state=loop.gen.get_state()), path)


def load_state(loop, path: Path):
    st = torch.load(path, weights_only=False)
    loop.vision.load_state_dict(st["vision"])
    loop.op.load_state_dict(st["op"])
    loop.word.load_state_dict(st["word"])
    loop.opt.load_state_dict(st["opt"])
    loop.gen.set_state(st["gen_state"])
    loop._t = st["_t"]
    return loop


def run_arm(arm_name: str, seed: int, steps_override: int | None = None,
            save_state_at_end: bool = False, probes=None, out_tag: str | None = None) -> dict:
    """probes: optional per-EVAL callback loop -> dict of EXTRA columns (exp09; must be
    RNG-isolated — never draws from loop.gen). out_tag: optional artifact suffix so a
    replay never overwrites the committed artifact. Both default to the pre-exp09
    behavior byte-identically."""
    spec = ARMS[arm_name]
    steps = steps_override or spec["steps"]
    no_word = spec.get("no_word", False)
    loop, spec, cfg = build_loop(arm_name, seed)

    OUTDIR.mkdir(exist_ok=True)
    man = build_manifest(loop, arm_name, spec, seed)
    n_checked = assert_stream_consistency(loop, man)
    man["stream_consistency_asserted_waves"] = n_checked
    base = OUTDIR / (f"{arm_name}_s{seed}" + (f"_{out_tag}" if out_tag else ""))
    (base.with_suffix(".manifest.json")).write_text(json.dumps(man, indent=2))
    (base.with_suffix(".manifest.md")).write_text(manifest_md(man))
    try:
        render_scatter(loop, base.with_suffix(".scatter.png"))
    except Exception as e:                                   # illustrative-only: never blocks
        man["scatter_note"] = f"render skipped: {e}"

    vocab = getattr(loop, "_vocab", cfg.n_category)
    members_a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    members_b = torch.arange(cfg.n_B).repeat(cfg.n_A)
    labels = loop._word_label(members_b, members_a)

    cols, occ, gsplit, mixes = [], {}, {}, {}
    for t in range(1, steps + 1):
        loop.step(no_word=no_word)
        if t % EVAL == 0:
            with torch.no_grad():
                raw_c = loop.stim.raw_clean(members_a, members_b)
                e = loop.evoke_vision(members_a, members_b, associative=True)
                content = loop.vision.emit(raw_c)
                # the dead-dictionary measurement (one-review converter b): assignment
                # input-sensitivity + argmax concentration + entropy over the 16 probes
                p = loop.vision.pool.assign(raw_c)
                off = ~torch.eye(p.shape[0], dtype=torch.bool)
                asg_dist = float(torch.cdist(p, p, p=1)[off].mean())
                asg_argmax_k = int(len(set(p.argmax(1).tolist())))
                asg_entropy = float(-(p * (p + 1e-12).log()).sum(1).mean())
            r = partition_read(e, labels, content)
            cols.append(dict(t=t, num=r["cross_dist_raw"], den=r["content_denom"],
                             ratio=r["d_diff"], proto=loop.pam_proto_spread(),
                             d2_depth=loop.vision.pool.pooling_depth(),
                             d2_spread=float(poolmetrics.within_group_spread(loop.vision.pool)),
                             asg_dist=asg_dist, asg_argmax_k=asg_argmax_k,
                             asg_entropy=asg_entropy))
            if probes is not None:                             # exp09 extra columns (RNG-isolated)
                cols[-1].update(probes(loop))
        if t % BLOCK == 0:
            occ[str(t)] = loop.dc_track(cfg.n_eval)
            gsplit[str(t)] = grad_split(loop, no_word)
            mixes[str(t)] = loop.mix_snapshot()

    ts = [c["t"] for c in cols]
    panels = {k: dynamics_panel(ts, [c[k] for c in cols])
              for k in ("num", "den", "ratio", "proto", "d2_depth", "d2_spread",
                        "asg_dist", "asg_argmax_k", "asg_entropy")}
    assessable = sum(1 for c in cols if c["ratio"] is not None)
    rec = dict(
        commit_hash=C.commit_hash(), spec_hash=C.spec_hash(),
        arm=arm_name, seed=seed, steps=steps, vocab=int(vocab), no_word=no_word,
        eval_cadence=EVAL, block_cadence=BLOCK,
        torch_num_threads=torch.get_num_threads(),             # determinism-contract provenance
        early_signature=dict(
            assessable_fraction=round(assessable / max(1, len(cols)), 4),
            denominator_panel=panels["den"], reference_note="reference (entry run): period "
            "~4800, assessable ~35% at cadence 100; envelope trend shrinking to terminal"),
        dynamics_panel=panels,
        # standing keys keep the committed 6-DECIMAL rounding (byte-identical replays);
        # probe keys use 6 SIGNIFICANT digits (gradient energies live at 1e-9)
        columns=[{k: ((round(v, 6) if k in _STANDING_COLS else float(f"{v:.6g}"))
                      if isinstance(v, float) else v) for k, v in c.items()}
                 for c in cols],
        occupancy=occ, grad_split=gsplit, masking_mix=mixes,
    )
    if spec.get("extension_read"):
        rec["extension_read"] = extension_read(cols)
    if save_state_at_end:
        save_state(loop, OUTDIR / f"state_{arm_name}_s{seed}.pt")
        rec["state_saved"] = f"state_{arm_name}_s{seed}.pt"
    base.with_suffix(".json").write_text(json.dumps(rec, indent=2))
    print(f"{arm_name} s{seed}: assessable={rec['early_signature']['assessable_fraction']}  "
          f"den_panel={panels['den']}  d2_depth_end={cols[-1]['d2_depth']:.4f}")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=sorted(ARMS))
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--save-state", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(max(1, torch.get_num_threads() or 2))
    run_arm(args.arm, args.seed, args.steps, save_state_at_end=args.save_state)


if __name__ == "__main__":
    main()
