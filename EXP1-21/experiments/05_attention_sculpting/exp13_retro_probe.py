"""Retro marginal-map probe (§10.21.5, Jason's ruling 2026-07-06) — READ-ONLY.

The question: was the OPERATOR marginal on the prior EXP12 runs too, or did it leave the
marginal where sensitivity-without-conversion CONVERTED? Applies the EXP13 controlled
category-conditioned completion test (the marginal-map probe) retrospectively to committed
EXP12 end-states. NO new training / no new regime: each committed run is REPRODUCED
deterministically (seed + construction order + torch threads=1; the runner's dc_track@BLOCK
read is replicated — the verification found dc_track is the read that couples into the
trajectory, and DC_ONLY reproduces the artifact digit-exact), then the operator is read
read-only at the requested checkpoints. No .pt end-states are saved for these runs, hence
deterministic reproduction rather than a load.

Probe (EXP12 wave-local W=1 geometry, the native completer face): over the 16 clean members,
complete the WORD slot from the visible vision slot; category accuracy (0.5 = context-blind
marginal, ->1 = contextual), completed-word spread across members and across random inputs
(near-0 = constant function), and distance-to-marginal vs distance-to-correct-token.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp09_arms as X9                                        # noqa: E402
import exp12_arms as X12                                       # noqa: E402
from loom.completion import apply_slice_mask                   # noqa: E402

OUTDIR = X12.OUTDIR
BLOCK = X12.BLOCK


@torch.no_grad()
def marginal_map_probe(loop, cfg) -> dict:
    ma, mb = X9._member_set(cfg)
    cat = mb % cfg.n_category
    raw_clean = loop.stim.raw_clean(ma, mb)
    e_vis = loop.vision.emit(raw_clean)                       # (16, D)
    wtok = loop.word.emit(torch.tensor([0, 1]))              # (2, D)
    sl2 = loop.slot_ids[:2]

    def complete_word(ev):                                   # word from a given vision emission
        content = torch.stack([ev.unsqueeze(0), loop.word.emit(torch.tensor([0]))], 1)
        mask = torch.zeros(1, 2, dtype=torch.bool); mask[0, 1] = True
        cells = apply_slice_mask(loop._pose_pam_input(content), mask, loop.op.mask_emb).reshape(2, cfg.D)
        return loop.op(cells.unsqueeze(0), sl2, (~mask).reshape(-1))[0].reshape(1, 2, cfg.D)[0, 1]

    def complete_vision(tok):                                # vision from a given word token
        content = torch.stack([e_vis.mean(0, keepdim=True), loop.word.emit(torch.tensor([tok]))], 1)
        mask = torch.zeros(1, 2, dtype=torch.bool); mask[0, 0] = True
        cells = apply_slice_mask(loop._pose_pam_input(content), mask, loop.op.mask_emb).reshape(2, cfg.D)
        return loop.op(cells.unsqueeze(0), sl2, (~mask).reshape(-1))[0].reshape(1, 2, cfg.D)[0, 0]

    preds = torch.stack([complete_word(e_vis[i]) for i in range(16)])   # (16, D)
    d0 = (preds - wtok[0]).norm(dim=1); d1 = (preds - wtok[1]).norm(dim=1)
    cat_acc = float(((d1 < d0).long() == cat).float().mean())
    outs_rand = torch.stack([complete_word(torch.randn(cfg.D)) for _ in range(20)])
    marg = preds.mean(0)
    correct = wtok[cat]
    word_sep = float((wtok[0] - wtok[1]).norm())
    pv0, pv1 = complete_vision(0), complete_vision(1)
    return dict(
        cat_acc=round(cat_acc, 3),
        completed_word_spread_members=round(float(torch.cdist(preds, preds).max()), 6),
        completed_word_spread_random=round(float(torch.cdist(outs_rand, outs_rand).max()), 6),
        d_to_marginal=round(float((preds - marg).norm(dim=1).mean()), 5),
        d_to_correct_token=round(float((preds - correct).norm(dim=1).mean()), 5),
        word_token_sep=round(word_sep, 4),
        vision_from_word_shift=round(float((pv0 - pv1).norm()), 6),
        vision_from_word_frac_of_wordsep=round(float((pv0 - pv1).norm()) / max(1e-9, word_sep), 5),
        interpretation=("MARGINAL (context-blind: cat_acc~0.5, output~constant, sits at marginal)"
                        if cat_acc < 0.66 else "CONTEXTUAL (cat_acc>0.66)"))


def run_probe(arm: str, seed: int, checkpoints: list[int], no_word: bool = False) -> dict:
    max_steps = max(checkpoints)
    loop, spec, cfg = X12.build_exp12(arm, seed, max_steps)
    nw = bool(spec.get("no_word", no_word))
    reads, done = [], 0
    for cp in sorted(checkpoints):
        while done < cp:
            done += 1
            loop.step(no_word=nw)
            if done % BLOCK == 0:
                loop.dc_track(cfg.n_eval)                     # the runner's coupling read (exact repro)
        rec = marginal_map_probe(loop, cfg)
        rec["t"] = done
        with torch.no_grad():
            ma, mb = X9._member_set(cfg)
            p = loop.vision.pool.assign(loop.stim.raw_clean(ma, mb))
            cat = mb % cfg.n_category
            rec["asg_cat"] = round(float((p[cat == 0].mean(0) - p[cat == 1].mean(0)).abs().sum()), 4)
        reads.append(rec)
        print(f"{arm} s{seed} t={done}: cat_acc={rec['cat_acc']} "
              f"spread_mem={rec['completed_word_spread_members']} "
              f"d_marg={rec['d_to_marginal']} d_corr={rec['d_to_correct_token']} "
              f"vfw={rec['vision_from_word_frac_of_wordsep']} asg_cat={rec['asg_cat']} "
              f"-> {rec['interpretation']}", flush=True)
    out = dict(arm=arm, seed=seed, no_word=nw, checkpoints=sorted(checkpoints), reads=reads,
               note="retro marginal-map probe; deterministic reproduction + dc_track@BLOCK; read-only")
    (OUTDIR / f"retro_marginal_{arm}_s{seed}.json").write_text(json.dumps(out, indent=2))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", nargs="+", metavar=("ARM", "SEED"))   # ARM SEED cp1,cp2,...
    args = ap.parse_args()
    torch.set_num_threads(1)
    arm, seed, cps = args.run[0], int(args.run[1]), [int(x) for x in args.run[2].split(",")]
    run_probe(arm, seed, cps)


if __name__ == "__main__":
    main()
