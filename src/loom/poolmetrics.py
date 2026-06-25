"""Pooling-substrate instrumentation (Stage-0 §4 differentiation signal, §9 structural
signal #2, §10 logging). Ported verbatim from experiments/01_pooling_substrate/metrics.py.

* ``accuracy``            — nearest-prototype / margin accuracy (no free head).
* ``within_group_spread`` — members differentiating (substrate live, not inert).
* ``intra_group_grad_stats`` — the consumption signal:
    - ``pull_apart``      : magnitude of the per-member differentiation force; this is the
      §4/§13 re-pool trigger AND the gap-3 disagreement readout (robust when gradients
      vanish, where a pure cosine is ill-defined).
    - ``cos_disagreement``: mean pairwise cosine of per-member Delta2 gradients —
      DIAGNOSTIC ONLY (never the re-pool trigger).
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


@torch.no_grad()
def accuracy(logits: torch.Tensor, y: torch.Tensor) -> float:
    return (logits.argmax(1) == y).float().mean().item()


@torch.no_grad()
def within_group_spread(model) -> float:
    """Mean pairwise distance between member weight vectors, averaged over groups."""
    W = model.weights()
    spreads = []
    for j in range(model.G):
        block = W[j * model.M:(j + 1) * model.M]
        if model.M > 1:
            d = torch.cdist(block, block)
            spreads.append(d[~torch.eye(model.M, dtype=torch.bool, device=W.device)].mean())
    return torch.stack(spreads).mean().item() if spreads else 0.0


def intra_group_grad_stats(model, loss: torch.Tensor) -> dict:
    """Per-member Delta2 gradient signal on a supplied differentiable ``loss``.

    Uses ``autograd.grad`` (does not touch optimiser state). Summarises, per group, how
    members are being pulled apart by this loss. Generalised from exp01 (which computed
    its own coarse+fine task loss) so any Stage-0 loss term — including the PAM
    convergence loss — can be attributed to substrate differentiation (gap-3).
    """
    (grad,) = torch.autograd.grad(loss, model.delta2, retain_graph=True)  # (U, D)

    cos_list, pull_list = [], []
    for j in range(model.G):
        gb = grad[j * model.M:(j + 1) * model.M]  # (M, D)
        if model.M < 2:
            continue
        gn = F.normalize(gb, dim=1, eps=1e-12)
        sim = gn @ gn.t()
        off = ~torch.eye(model.M, dtype=torch.bool, device=grad.device)
        cos_list.append(sim[off].mean())
        diff = gb - gb.mean(dim=0, keepdim=True)
        pull_list.append(diff.norm(dim=1).mean())

    return dict(
        cos_disagreement=(torch.stack(cos_list).mean().item() if cos_list else float("nan")),
        pull_apart=(torch.stack(pull_list).mean().item() if pull_list else 0.0),
    )
