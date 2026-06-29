"""Soft-tied hierarchical pooling substrate — the LAW (Stage-0 §4).

Ported verbatim from experiments/01_pooling_substrate (model.py + harness.py
controllers), with one addition: an ``emit`` method so the same substrate can be used
as a plastic *embedder* (the vision cortex), not only as a classifier. The pooling law
and trigger semantics are shared by the encoder population and the PAM population
(Stage-0 §4: same law, **separate weight populations**) — instantiate this class twice.

Each unit ``i`` is a prototype in input space::

    W_i = base_root + Delta1_{g1(i)} + Delta2_i           (i = 0 .. G*M-1)
    L_pool = lambda1 * sum||Delta1||^2 + lambda2 * sum||Delta2||^2

Large lambda -> residuals shrink (pooled, few effective detectors); small lambda ->
residuals grow (unpooled, full resolution). Readout is **soft nearest-prototype**
(negative squared distance), never a free linear head (exp01 §0 capacity-leak).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class HierarchicalPoolingModel(nn.Module):
    def __init__(
        self,
        D: int,
        n_groups: int,
        members_per_group: int,
        temp: float = 1.0,
        init_scale: float = 1e-3,
        init_center: torch.Tensor | None = None,
        seed: int = 0,
    ):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        self.D = D
        self.G = n_groups
        self.M = members_per_group
        self.U = n_groups * members_per_group
        self.temp = temp

        base = init_scale * torch.randn(D, generator=g)
        if init_center is not None:
            base = base + init_center.detach().clone()
        self.base_root = nn.Parameter(base)
        self.delta1 = nn.Parameter(init_scale * torch.randn(n_groups, D, generator=g))
        # Tiny *independent* per-unit perturbations: without them, soft-tied members
        # under identical gradients can never break symmetry (the Test A failure mode).
        self.delta2 = nn.Parameter(init_scale * torch.randn(self.U, D, generator=g))

        self.register_buffer("g1", torch.arange(self.U) // members_per_group)

    def weights(self) -> torch.Tensor:
        """The (U, D) per-unit prototypes W_i."""
        return self.base_root.unsqueeze(0) + self.delta1[self.g1] + self.delta2

    def forward(self, X: torch.Tensor):
        """Return (coarse_logits (N,G), fine_logits (N,U)) = soft nearest-prototype."""
        W = self.weights()
        dist2 = torch.cdist(X, W).pow(2)
        fine_logits = -dist2 / self.temp
        fl = fine_logits.view(X.shape[0], self.G, self.M)
        coarse_logits = torch.logsumexp(fl, dim=2)
        return coarse_logits, fine_logits

    def assign(self, X: torch.Tensor) -> torch.Tensor:
        """Soft assignment p (N, U) = softmax over fine prototypes (no free head)."""
        _, fine_logits = self.forward(X)
        return F.softmax(fine_logits, dim=-1)

    def emit(self, X: torch.Tensor) -> torch.Tensor:
        """Embedder emission (N, D): soft nearest-prototype reconstruction ``p @ W``.

        Under pooling (members identical), B-distinct inputs map to nearly the same
        reconstruction -> the emission CANNOT carry the fine (B) distinction. Once
        Delta2 opens (members move apart), distinct prototypes -> the emission carries
        B. This is exactly the substrate property Stage-0 needs: vision resolution
        gates whether the B-probe is representable. The PAM convergence error reaching
        this emission's gradient drives Delta2 to open along B (gap-3).
        """
        p = self.assign(X)
        return p @ self.weights()

    def pool_penalty(self, lam1: float, lam2: float) -> torch.Tensor:
        return lam1 * self.delta1.pow(2).sum() + lam2 * self.delta2.pow(2).sum()

    @torch.no_grad()
    def residual_norms(self):
        """Per-level residual norms: (||Delta1_j||)_j, (||Delta2_i||)_i."""
        return self.delta1.norm(dim=1).cpu(), self.delta2.norm(dim=1).cpu()

    @torch.no_grad()
    def pooling_depth(self) -> float:
        """A scalar 'how open is fine capacity' = mean ||Delta2_i|| (feeds capacity_open)."""
        return self.delta2.norm(dim=1).mean().item()


class StepSchedule:
    """Clock-led, pinned-constant unpool (§4 / §13 rate-1; activity_gate pinned to 1).

    Capacity opens on a *schedule*, not pulled by error. ``t2=None`` keeps lambda2 high
    forever (the always-pooled baseline).
    """

    def __init__(self, lam1_hi, lam1_lo, lam2_hi, lam2_lo, t1, t2, activity_gate: float = 1.0):
        self.lam1_hi, self.lam1_lo = lam1_hi, lam1_lo
        self.lam2_hi, self.lam2_lo = lam2_hi, lam2_lo
        self.t1, self.t2 = t1, t2
        self.activity_gate = activity_gate  # pinned to 1 for Stage-0 run 1

    def lam1(self, t):
        return self.lam1_lo if (self.t1 is not None and t >= self.t1) else self.lam1_hi

    def lam2(self, t):
        return self.lam2_lo if (self.t2 is not None and t >= self.t2) else self.lam2_hi

    def update(self, t, stats):
        pass


@torch.no_grad()
def constant_repool_delta2(model: "HierarchicalPoolingModel", rate: float) -> None:
    """CONSTANT INTRINSIC RE-POOL on **occupancy** (Stage-1 attention-sculpting, FRONTIER §5).

    Relax each member deviation Delta2_i toward its group's member-mean by a constant fraction
    ``rate`` every step — an untargeted, signal-free decay of *occupancy* opposed only by the
    gap-3 pull-apart gradient. Equilibrium = balance of intermittent occupy-pull vs constant
    decay; whatever isn't held collapses.

    G3 — THIS ACTS ON Delta2 (occupancy) ONLY. lambda2 (the envelope/tie-strength) and Delta1
    (the coarse/group node) are UNTOUCHED, so the opened capacity STAYS OPEN ("seed waiting":
    re-occupation is instant when divergence returns — no waiting on the clock). This is NOT
    ``AdaptiveRepool``: that *raises lambda2* (re-tightens the envelope), collapsing Delta2 only
    as a downstream side-effect — that is **Tier-2 envelope re-pool, DEFERRED** (FRONTIER §6b).
    Do not substitute one for the other.

    Applied under no_grad as a post-optimizer-step substrate force (not a loss term) — efficiency
    stays an emergent property of the substrate, never a global objective (G4).
    Depth-grading (steeper at leaves than root) is the release form (stage 3); pinned constant /
    depth-independent here — the constant rate is the special case, so no debt.
    """
    if rate <= 0.0:
        return
    d2 = model.delta2.data.view(model.G, model.M, model.D)      # (G, M, D) view of the parameter
    member_mean = d2.mean(dim=1, keepdim=True)                  # (G, 1, D) pooled (within-group) mean
    d2.add_(d2 - member_mean, alpha=-rate)                      # in-place: Delta2 -= rate*(Delta2 - mean)


class AdaptiveRepool:
    """Re-pool when the pull-apart FORCE magnitude is sustained below ``frac`` of its
    peak (§4 / §13 re-pool; trigger is pull-apart magnitude, NOT gradient cosine).
    Self-calibrating against the largest force seen; fast-out/slow-in via ``ramp_steps``.

    NOTE (Stage-1): this raises lambda2 = ENVELOPE re-pool (Tier-2, DEFERRED). The Stage-1
    attention-sculpting rig uses ``constant_repool_delta2`` (occupancy decay) instead — see G3.
    """

    def __init__(self, lam1, lam2_lo, lam2_hi, frac=0.15, patience=4, ramp_steps=400):
        self._lam1 = lam1
        self.lam2_lo, self.lam2_hi = lam2_lo, lam2_hi
        self.frac, self.patience, self.ramp_steps = frac, patience, ramp_steps
        self.peak = 0.0
        self.count = 0
        self.trigger_t = None

    def lam1(self, t):
        return self._lam1

    def lam2(self, t):
        if self.trigger_t is None:
            return self.lam2_lo
        frac = min(1.0, (t - self.trigger_t) / max(1, self.ramp_steps))
        return self.lam2_lo + frac * (self.lam2_hi - self.lam2_lo)

    def update(self, t, stats):
        if self.trigger_t is not None:
            return
        pull = stats.get("pull_apart", 0.0)
        self.peak = max(self.peak, pull)
        if self.peak > 0 and pull < self.frac * self.peak:
            self.count += 1
        else:
            self.count = 0
        if self.count >= self.patience:
            self.trigger_t = t
