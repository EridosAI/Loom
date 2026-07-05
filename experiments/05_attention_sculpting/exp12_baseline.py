"""EXP12 — the conventional trainability baseline (Fork 4; prereg §9, §13.6).

THERMOMETER, NOT DONOR (binding fence): this learner shares the STIMULUS (the identical
pre-generated vector waves + the identical mask schedule) and the OBJECTIVE FAMILY
(masked completion) with the rig — and NOTHING else. No shared modules, no shared code
paths into the PAM/vision/word stack, no design flowback. Its reads are trainability
context, never PAM bars; the generality read is ONE-DIRECTIONAL (its failure where PAM
passed is context, never a PAM-superiority claim — param-scale and family confounds are
unresolved by construction).

Family/impl ([RECONCILE: family/impl] resolved at build, surfaced for the checkpoint
record): a V-JEPA-class NON-CAUSAL masked-completion MLP — input = the wave's two slots
[vision-vec ; word-vec] with the masked slot replaced by a LEARNED mask token; output =
the full two-slot reconstruction; MSE on the masked slot only. No forward-in-time
objective (wave-local, like the rig — the anti-forward guard binds the baseline too).
Word-slot targets are the anchor's embedding VECTORS handed over as stimulus-side data
(the environment's labels), not the WordCortex module.

Sizing (§13.6): params within ~2x of PAM's plastic side (11,281 — CC-counted 2026-07-05:
vision 608 + operator 10,673). Hidden width 80 -> 11,728 params (1.04x; mask_token 16 +
f1 2,640 + f2 6,480 + out 2,592 — runtime-verified in smoke).

Its own bars, form registered in the prereg (constants at stage-two, from its own
calibration seeds, same two-stage):
  (B1) latent CATEGORY-separability: windowed between/within-category separation ratio
       in ITS OWN representation space (second hidden layer), read at the exam geometry
       (vision visible, word slot = mask token) over the 16 clean member inputs;
       member-separability rides as companion. "Mean-collapse" = separability -> floor
       while outputs -> category-/deck-mean.
  (B2) onset-exam analog lift: masked word-slot completion on onset waves vs the
       CATEGORY-PRIOR floor (0 by symmetric construction), acquisition-aligned.

BUILT-WHEN-FIRED discipline: this module exists and is smoke-tested (build order item
5); its ARMS run only on a pre-registered trigger (both-die | promote cell).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as Fn

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp12_fabric as F                                      # noqa: E402  (fabric data only)

OUTDIR = _HERE / "exp08"
EVAL = 300
HIDDEN = 80
LR = 3e-3                                                     # the rig's Adam lr class; own knob
PAM_PLASTIC_PARAMS = 11281                                    # CC count, 2026-07-05


class BaselineCompleter(nn.Module):
    """Masked-completion MLP over one wave's two slots. Latent = the second hidden."""

    def __init__(self, D: int, hidden: int = HIDDEN, seed: int = 0):
        super().__init__()
        torch.manual_seed(seed + 51)
        self.D = D
        self.mask_token = nn.Parameter(0.02 * torch.randn(D))
        self.f1 = nn.Linear(2 * D, hidden)
        self.f2 = nn.Linear(hidden, hidden)
        self.out = nn.Linear(hidden, 2 * D)

    def latent(self, x: torch.Tensor) -> torch.Tensor:
        return Fn.gelu(self.f2(Fn.gelu(self.f1(x))))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.out(self.latent(x))

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


def run_baseline(fab, word_vecs: torch.Tensor, steps: int, seed: int,
                 n_category: int = 2) -> dict:
    """Train on the IDENTICAL waves + IDENTICAL mask schedule; emit (B1)/(B2) columns.
    `fab` = the same Fabric object the rig arm consumed (stimulus-side data only);
    `word_vecs` (n_tokens, D) = the anchor embedding vectors as environment data."""
    D = fab.raw.shape[1]
    net = BaselineCompleter(D, seed=seed)
    ratio = net.n_params() / PAM_PLASTIC_PARAMS
    assert 0.5 <= ratio <= 2.0, f"baseline sizing out of the ~2x band: {ratio:.2f}"
    opt = torch.optim.Adam(net.parameters(), lr=LR)

    # the 16 clean member inputs at exam geometry, for B1 (vision visible, word masked)
    mem = torch.arange(16)
    a, b = mem // 4, mem % 4
    # clean member vision vectors = the standing world at rest pose (centre incl. bg)
    # handed over as data; rebuilt here from the fabric's own realized waves is noisy,
    # so the caller passes probe_vis explicitly if wanted; default = per-member mean of
    # realized waves (stimulus-side, no rig components)
    probe_vis = torch.stack([fab.raw[fab.member == m].mean(0) if bool((fab.member == m).any())
                             else torch.zeros(D) for m in range(16)])
    cat = b % n_category

    cols, buf_exam, buf_examacc = [], [], []
    for t in range(steps):
        x = torch.cat([fab.raw[t], word_vecs[int(fab.cat[t])]], dim=0)
        m_slot = int(fab.mask_slot[t])
        x_in = x.clone()
        sl = slice(0, D) if m_slot == 0 else slice(D, 2 * D)
        x_in[sl] = net.mask_token
        pred = net(x_in.unsqueeze(0))[0]
        loss = Fn.mse_loss(pred[sl], x[sl])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if m_slot == 1 and bool(fab.is_exam[t]):              # B2 buffer (scheduled exams)
            with torch.no_grad():
                pw = pred[D:2 * D]
                d = torch.cdist(pw.unsqueeze(0), word_vecs[:n_category])[0]
                c = int(fab.cat[t])
                lift = float(d[1 - c] - d[c])
                buf_exam.append(lift)
                buf_examacc.append(float(lift > 0))
        if (t + 1) % EVAL == 0:
            with torch.no_grad():
                # B1: latent category-separability at exam geometry
                xin = torch.cat([probe_vis,
                                 net.mask_token.unsqueeze(0).expand(16, D)], dim=1)
                z = net.latent(xin)
                dm = torch.cdist(z, z)
                same = cat.unsqueeze(0) == cat.unsqueeze(1)
                off = ~torch.eye(16, dtype=torch.bool)
                between = float(dm[(~same) & off].mean())
                within = float(dm[same & off].mean())
                # member separability companion
                mem_sep = float(dm[off].mean())
            cols.append(dict(
                t=t + 1,
                b1_between=between, b1_within=within,
                b1_ratio=(between / within) if within > 1e-9 else None,
                b1_member_sep=mem_sep,
                b2_exam_lift=(statistics.mean(buf_exam) if buf_exam else None),
                b2_exam_acc=(statistics.mean(buf_examacc) if buf_examacc else None),
                b2_exam_n=len(buf_exam)))
            buf_exam, buf_examacc = [], []
    return dict(n_params=net.n_params(), param_ratio_vs_pam=round(ratio, 3),
                hidden=HIDDEN, lr=LR, columns=cols)


def run_baseline_cal(arm: str, seed: int, steps: int):
    """Stage-two B1/B2 calibration run (§13.6: constants from the baseline's OWN cal
    seeds, same two-stage). Builds the rig loop ONLY to hand over the environment data
    (the fabric + the anchor's embedding vectors); the learner shares no component."""
    import exp12_arms as X12
    torch.set_num_threads(1)
    lp, _, cfg = X12.build_exp12(arm, seed, steps=steps)
    fab = lp.stream
    wv = lp.word.emit(torch.arange(cfg.n_category)).detach().clone()
    del lp                                                    # environment handed over; rig discarded
    rec = run_baseline(fab, wv, steps=steps, seed=seed, n_category=cfg.n_category)
    rec.update(arm=arm, seed=seed, steps=steps,
               torch_num_threads=torch.get_num_threads())
    out = OUTDIR / f"exp12_baseline_{arm.replace('exp12_', '')}_s{seed}.json"
    out.write_text(json.dumps(rec, indent=2))
    c = rec["columns"][-1]
    r1 = c["b1_ratio"]
    print(f"baseline {arm} s{seed}: b1_ratio_end={r1 if r1 is None else round(r1, 3)} "
          f"(between={c['b1_between']:.4f} within={c['b1_within']:.4f}) "
          f"b2_lift_end={c['b2_exam_lift']} b2_acc_end={c['b2_exam_acc']}")
    return rec


def smoke():
    """Build-order item 5 smoke: sizing in band; trains on a real fabric; B1/B2 emit;
    NO component of the rig imported (the fence — asserted by module inspection)."""
    import exp12_arms as X12
    banned = ("sculpt_loop", "loop", "pam_operator", "encoders")
    src = Path(__file__).read_text()
    for mod in banned:
        assert f"import {mod}" not in src, f"FENCE BREACH: baseline imports {mod}"
    torch.set_num_threads(1)
    lp, _, cfg = X12.build_exp12("exp12_dwell", 0, steps=900)
    fab = lp.stream
    wv = lp.word.emit(torch.arange(cfg.n_category)).detach().clone()  # env data handoff
    rec = run_baseline(fab, wv, steps=900, seed=0, n_category=cfg.n_category)
    assert 0.5 <= rec["param_ratio_vs_pam"] <= 2.0
    assert rec["columns"] and rec["columns"][-1]["b1_ratio"] is not None
    print("BASELINE SMOKE OK:", json.dumps(dict(
        n_params=rec["n_params"], ratio=rec["param_ratio_vs_pam"],
        last_col=rec["columns"][-1])))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cal", nargs=2, metavar=("ARM", "SEED"))
    ap.add_argument("--steps", type=int, default=160000)
    args = ap.parse_args()
    if args.smoke:
        smoke()
    elif args.cal:
        run_baseline_cal(args.cal[0], int(args.cal[1]), args.steps)
