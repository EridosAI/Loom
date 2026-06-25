"""The two cortices (Stage-0 §1, §6).

Vision = a PLASTIC pooling-substrate embedder (weights ARE the soft-tied pool, loom.pooling)
with its own intrinsic L_JEPA. Word = a FROZEN near-trivial lookup (the anchor / parent).

Asymmetric plasticity (§0.2): the vision cortex updates; the word cortex is frozen —
``requires_grad=False`` AND excluded from the optimiser AND no weight-decay/EMA/optimizer
state. A nonzero word-encoder parameter-delta is a BUILD FAILURE (the anchor went plastic).

L_JEPA (§7) is defined concretely: within-dwell **next-wave vision-content prediction** in
vision's own space. Its stop-grad is on the JEPA *target* (internal to the vision cortex,
the J in JEPA) — that is NOT the PAM completion target, so it does not touch the gap-3
no-detach rule (which governs the PAM convergence target path in loop.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from loom.pooling import HierarchicalPoolingModel  # noqa: E402


class VisionCortex(nn.Module):
    """Plastic pooling embedder. G groups = A-levels (coarse/salient), M members =
    B-levels (subtle/fine). Pooled -> emission cannot carry B (floor_B ~ chance);
    Delta2 open -> emission carries B (ceiling). The PAM convergence error reaching this
    emission's gradient drives Delta2 to differentiate along B (gap-3)."""

    def __init__(self, D: int, n_A: int, n_B: int, *, temp: float = 1.0,
                 init_center: torch.Tensor | None = None, seed: int = 0):
        super().__init__()
        self.pool = HierarchicalPoolingModel(
            D=D, n_groups=n_A, members_per_group=n_B, temp=temp,
            init_center=init_center, seed=seed,
        )
        self.D, self.n_A, self.n_B = D, n_A, n_B
        # JEPA predictor: next-wave vision embedding from the current one (vision's own loop).
        self.jepa_pred = nn.Linear(D, D)

    def emit(self, raw: torch.Tensor) -> torch.Tensor:
        """raw (..., D) stimulus -> vision slice (..., D) (plastic, grad flows)."""
        return self.pool.emit(raw)

    def l_jepa(self, raw_t: torch.Tensor, raw_tp1: torch.Tensor) -> torch.Tensor:
        """Within-dwell next-wave content prediction. Target is stop-grad (the J in JEPA),
        internal to the vision cortex — distinct from the PAM no-detach target."""
        e_t = self.emit(raw_t)
        with torch.no_grad():
            tgt = self.emit(raw_tp1)
        return F.mse_loss(self.jepa_pred(e_t), tgt)

    @property
    def pooling_depth(self) -> float:
        return self.pool.pooling_depth()


class WordCortex(nn.Module):
    """Frozen near-trivial lookup. Vocab = n_B probe labels + 1 null token. Distinct
    tokens -> distinct (frozen) embeddings = trivially high-accuracy. The structural
    anchor (§5): its target-diversity removes collapse as a global optimum without any
    stop-grad. Frozen = lr=0 (params excluded from optimiser), NOT detached."""

    def __init__(self, D: int, n_B: int, *, seed: int = 1):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        self.n_B = n_B
        self.null_token = n_B
        emb = F.normalize(torch.randn(n_B + 1, D, generator=g), dim=1)
        self.embed = nn.Embedding(n_B + 1, D)
        with torch.no_grad():
            self.embed.weight.copy_(emb)
        # FREEZE: no grad, no optimiser, no wd/EMA. (loop.py also excludes from optimiser.)
        self.embed.weight.requires_grad_(False)
        self.register_buffer("_w0", emb.clone())   # t0 snapshot for the build-failure check

    def emit(self, token: torch.Tensor) -> torch.Tensor:
        return self.embed(token)

    @torch.no_grad()
    def param_delta(self) -> float:
        """Max |w - w_t0| — MUST be 0.0 (else ANCHOR_WENT_PLASTIC build failure)."""
        return (self.embed.weight - self._w0).abs().max().item()

    def frozen_parameters(self):
        return [self.embed.weight]
