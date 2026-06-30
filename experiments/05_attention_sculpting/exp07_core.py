"""exp07 core — the two NEW mechanisms (everything else reuses dgate verbatim):

  1. CONTENT-PRESERVING CUE RE-POSING (Step-0a construction).
     The deployed flat-diffuse cue is  comp[m] = shared*base + cue_mag*Cd[m]  — a tiny per-member
     differentiating part (cue_mag*Cd[m]) buried under a large content-blind common-mode (shared*base),
     snr ~0.086. The re-posing subtracts a fraction alpha of the CONTENT-BLIND POPULATION MEAN
     mu = mean_m comp[m] (a single constant vector, cls-independent):

         comp_reposed[m] = comp[m] - alpha * mu

     This is a pure RE-ORGANIZATION of the presentation, provably:
       * it cannot inject discriminating signal — subtracting a constant preserves every pairwise
         member difference exactly: comp_reposed[m] - comp_reposed[m'] == comp[m] - comp[m'].
         (So the differentiating information is UNTOUCHED; alpha only removes the masking offset.)
       * it is content-blind — mu does not depend on which association is masked, so applied to a
         content-ablated cue (differentiating part zeroed -> all members identical) it yields identical
         cues -> NO (d). This is the spec's ablation-invariance guard.
     It is NOT sharpening: the differentiating magnitude stays cue_mag (~0.5), never raised to the
     sharp unit cue. alpha=0 -> flat-diffuse (deployed status quo); alpha=1 -> common-mode centered.
     Why it helps the operator at all (despite preserving info): the prototype-resonance distance
     (cdist) is offset-sensitive — a huge common-mode makes all members cluster, drowning the 0.5-scale
     differences; removing the offset re-centers so those differences become locally resolvable.

  2. CLOCK-GATED PENALTY (the reshaped regime, §5). lam follows the settled lambda2 envelope: present
     (deployed strength) before the clock-onset, then DROPS to 0 and STAYS OPEN. off = lam 0 always;
     deployed = lam 0.01 always; reshaped = 0.01 -> 0 at onset = clock_fraction * budget.

Sharp segment = dgate diffuse=False (pure unit cue), read at alpha=0 — the labeled alive-reference.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

# reuse the committed dgate primitives unchanged
from dgate import (Factors, make_op, _task_tensors, _companion, _sep,   # noqa: E402
                   W, N_SLOTS, KAPPA, D)


# ----------------------------------------------------------------- penalty regime spec
@dataclass
class PenaltySpec:
    """PAM pool penalty as a two-clock step schedule (the settled cortex StepSchedule applied to PAM).
    lam1 (delta1 = groups) and lam2 (delta2 = members/the λ2-tie) each step from hi->lo at an ABSOLUTE
    onset step (NOT a fraction of the training budget — a fractional onset drifts when the budget is
    extended for plateau, lengthening the closed phase and confounding the read; the onset is pinned to
    fraction*CANONICAL_BUDGET so extending training = more post-clock differentiation from a FIXED
    closed phase).
      off      -> all zero (no tie).
      deployed -> lam1=lam2=0.01 constant (collapsing tie).
      reshaped -> lam1 opens at t1_step, lam2/capacity opens at t2_step (the swept onset), hi=10->lo=0.
    Penalising delta1 too (the rejected single-clock pool_penalty(lam,lam)) annihilates the group
    symmetry-breakers and the collapse becomes IRREVERSIBLE; the cortex schedule keeps groups alive."""
    name: str
    lam1_hi: float
    lam1_lo: float
    t1_step: int
    lam2_hi: float
    lam2_lo: float
    t2_step: int

    def lam12_at(self, step: int) -> tuple[float, float]:
        lam1 = self.lam1_lo if step >= self.t1_step else self.lam1_hi
        lam2 = self.lam2_lo if step >= self.t2_step else self.lam2_hi
        return lam1, lam2


# ----------------------------------------------------------------- cue spec + re-posing
@dataclass
class CueSpec:
    seg: str         # "flat" | "repose" | "sharp"
    alpha: float     # common-mode centering fraction (flat=0, sharp=0; repose in (0,1])

    @property
    def diffuse(self) -> bool:
        return self.seg in ("flat", "repose")        # sharp = pure unit cue (diffuse=False)


def _factors(member_count: int, cue: CueSpec, *, shared_mag: float, cue_mag: float,
             train_steps: int) -> Factors:
    return Factors(member_count=member_count, diffuse=cue.diffuse, pam_lam=0.0,
                   diffuse_shared_mag=shared_mag, diffuse_cue_mag=cue_mag, train_steps=train_steps)


def _population_mean_cue(f: Factors, Cd, base, *, ablate: bool) -> torch.Tensor:
    """mu = content-blind population mean of the cue over all M members (cls-independent constant)."""
    comps = torch.stack([_companion(f, Cd, base, cls, ablate=ablate) for cls in range(f.member_count)])
    return comps.mean(dim=0)


def reposed_companion(f: Factors, Cd, base, cls: int, alpha: float, mu: torch.Tensor,
                      *, ablate: bool) -> torch.Tensor:
    """comp_reposed[cls] = comp[cls] - alpha*mu. mu is the FIXED (non-ablated) population mean — the
    deployed transform; the ablation guard applies the SAME mu to the ablated cue."""
    return _companion(f, Cd, base, cls, ablate=ablate) - alpha * mu


def _reposed_window(f: Factors, V, u, m: int, comp: torch.Tensor, op):
    """dgate._window, but the (already re-posed) companion vector is injected directly."""
    item = V[m]
    content = torch.zeros(W, N_SLOTS, D)
    content[:, 0, :] = item
    content[:, 1, :] = comp
    mask = torch.zeros(W, N_SLOTS, dtype=torch.bool)
    mask[:, 0] = True                                            # mask items; cue visible
    masked = content.clone()
    masked[mask] = op.mask_emb
    drift = torch.arange(W, dtype=torch.float32) - (W - 1) / 2.0  # [-0.5,+0.5] bounded carrier
    cells = (masked + KAPPA * drift.view(W, 1, 1) * u).reshape(W * N_SLOTS, D)
    return content.reshape(W * N_SLOTS, D), mask.reshape(-1), cells


# ----------------------------------------------------------------- train + measure one cell
def _slot_ids():
    return torch.tensor([s for _ in range(W) for s in range(N_SLOTS)])


def train_op(member_count: int, cue: CueSpec, pen: PenaltySpec, seed: int, *,
             shared_mag: float, cue_mag: float, budget: int):
    """Train a fresh op on the re-posed neutral task under the clock-gated penalty. Mirrors
    dgate.train_neutral_op exactly except (a) re-posed companion, (b) lam follows the regime envelope."""
    f = _factors(member_count, cue, shared_mag=shared_mag, cue_mag=cue_mag, train_steps=budget)
    op = make_op(seed)
    V, Cd, base, u = _task_tensors(f, seed)
    mu = _population_mean_cue(f, Cd, base, ablate=False)
    sid = _slot_ids()
    opt = torch.optim.Adam(op.parameters(), lr=f.lr)
    g = torch.Generator().manual_seed(seed * 911 + 7)
    M = member_count
    for step in range(budget):
        m = int(torch.randint(0, M, (1,), generator=g))
        comp = reposed_companion(f, Cd, base, m, cue.alpha, mu, ablate=False)  # assoc-different cls=m
        target, mask, cells = _reposed_window(f, V, u, m, comp, op)
        pred = op(cells.unsqueeze(0), sid, (~mask))[0]
        loss = F.mse_loss(pred[mask], target[mask])
        lam1, lam2 = pen.lam12_at(step)
        if lam1 > 0.0 or lam2 > 0.0:
            loss = loss + op.pam.pool_penalty(lam1, lam2)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return op, (f, V, Cd, base, u, mu)


@torch.no_grad()
def measure_d(op, ctx, cue: CueSpec) -> dict:
    """d_diff (assoc-different), d_same (assoc-same), d_ablated (differentiating cue zeroed), proto."""
    f, V, Cd, base, u, mu = ctx
    sid = _slot_ids()
    M = f.member_count

    def evoke(cls_of, *, ablate=False):
        outs = []
        for m in range(M):
            comp = reposed_companion(f, Cd, base, cls_of(m), cue.alpha, mu, ablate=ablate)
            _, mask, cells = _reposed_window(f, V, u, m, comp, op)
            outs.append(op(cells.unsqueeze(0), sid, (~mask))[0][0])
        return torch.stack(outs)

    e_diff = evoke(lambda m: m)
    e_same = evoke(lambda m: 0)
    e_abl = evoke(lambda m: m, ablate=True)
    Wp = op.pam.weights()
    proto_spread = (Wp - Wp.mean(0)).norm(dim=1).mean().item()
    return dict(d_diff=_sep(e_diff), d_same=_sep(e_same), d_ablated=_sep(e_abl),
                proto_spread=proto_spread)


def cell(member_count: int, cue: CueSpec, pen: PenaltySpec, seed: int, *,
         shared_mag: float, cue_mag: float, budget: int) -> dict:
    """Atomic exp07 reading: train + measure one (cue x penalty x cardinality) cell at one seed."""
    op, ctx = train_op(member_count, cue, pen, seed, shared_mag=shared_mag, cue_mag=cue_mag,
                       budget=budget)
    rec = measure_d(op, ctx, cue)
    rec.update(seg=cue.seg, alpha=cue.alpha, penalty=pen.name, member_count=member_count, seed=seed)
    return rec


def cell_trajectory(member_count: int, cue: CueSpec, pen: PenaltySpec, seed: int, checkpoints, *,
                    shared_mag: float, cue_mag: float) -> list:
    """As train_op but snapshot d_diff/proto at each checkpoint (plateau spot-check). budget=max(ckpts).
    Identical optimisation path; only adds read-only measurement."""
    budget = max(checkpoints)
    f = _factors(member_count, cue, shared_mag=shared_mag, cue_mag=cue_mag, train_steps=budget)
    op = make_op(seed)
    V, Cd, base, u = _task_tensors(f, seed)
    mu = _population_mean_cue(f, Cd, base, ablate=False)
    sid = _slot_ids()
    opt = torch.optim.Adam(op.parameters(), lr=f.lr)
    g = torch.Generator().manual_seed(seed * 911 + 7)
    M = member_count
    cps = sorted(set(checkpoints))
    traj = []
    for step in range(max(cps) + 1):
        if step in cps:
            traj.append(dict(step=step, **measure_d(op, (f, V, Cd, base, u, mu), cue)))
        if step == max(cps):
            break
        m = int(torch.randint(0, M, (1,), generator=g))
        comp = reposed_companion(f, Cd, base, m, cue.alpha, mu, ablate=False)
        target, mask, cells = _reposed_window(f, V, u, m, comp, op)
        pred = op(cells.unsqueeze(0), sid, (~mask))[0]
        loss = F.mse_loss(pred[mask], target[mask])
        lam1, lam2 = pen.lam12_at(step)
        if lam1 > 0.0 or lam2 > 0.0:
            loss = loss + op.pam.pool_penalty(lam1, lam2)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return traj


# ----------------------------------------------------------------- Step-0a content-blindness checks
@torch.no_grad()
def reposing_validation(member_count: int, shared_mag: float, cue_mag: float, alphas, seed: int = 0):
    """Two exact/numeric proofs the re-posing is content-preserving (Step-0a):
      (A) pairwise-difference invariance: comp_reposed[m]-comp_reposed[m'] == comp[m]-comp[m'] for all
          alpha (=> re-organization adds NO discriminating signal). Reported as max abs deviation.
      (B) ablation-invariance: applied to a content-ablated cue, all members' cues are identical
          => max pairwise separation ~ 0 at every alpha (=> cannot manufacture a floor)."""
    f = _factors(member_count, CueSpec("flat", 0.0), shared_mag=shared_mag, cue_mag=cue_mag,
                 train_steps=1)
    _, Cd, base, _ = _task_tensors(f, seed)
    mu = _population_mean_cue(f, Cd, base, ablate=False)
    base_comps = torch.stack([_companion(f, Cd, base, m, ablate=False) for m in range(member_count)])
    base_diffs = base_comps.unsqueeze(0) - base_comps.unsqueeze(1)     # (M,M,D) pairwise diffs at alpha=0
    rows = []
    for a in alphas:
        rep = torch.stack([reposed_companion(f, Cd, base, m, a, mu, ablate=False)
                           for m in range(member_count)])
        rep_diffs = rep.unsqueeze(0) - rep.unsqueeze(1)
        pairdiff_dev = (rep_diffs - base_diffs).abs().max().item()      # (A) must be ~0
        abl = torch.stack([reposed_companion(f, Cd, base, m, a, mu, ablate=True)
                           for m in range(member_count)])
        off = ~torch.eye(member_count, dtype=torch.bool)
        abl_sep = torch.cdist(abl, abl)[off].max().item()              # (B) must be ~0
        rows.append(dict(alpha=a, pairwise_diff_deviation=pairdiff_dev, ablated_max_separation=abl_sep))
    return rows
