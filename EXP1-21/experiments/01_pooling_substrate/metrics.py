"""Instrumentation for the pooling rig (SPEC sec. 3).

Everything the tests need, logged at near-zero cost:

* coarse / fine accuracy (separately),
* per-level residual norms (pooling state),
* within-group weight spread (differentiation happening),
* intra-group gradient signal -- two facets of "are members being pulled apart?":
    - ``cos_disagreement`` : mean pairwise cosine of per-member Delta2 gradients.
      Low (toward -1) = members pull in different directions = high disagreement =
      "want to differentiate". This is the SPEC sec.3 named quantity (Test D).
    - ``pull_apart``       : mean magnitude of the per-member differentiation force
      (member gradient minus its group mean). This is the *magnitude* form of
      "members no longer pulled apart", and is what Test C's re-pool controller
      triggers on -- it stays robust when gradients vanish (signal removed) or when
      the fine head is not trained, cases where a pure cosine is ill-defined.
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


def intra_group_grad_stats(model, X, y_coarse, y_fine, train_fine: bool) -> dict:
    """Per-member Delta2 gradient signal on the current task loss.

    Computes a fresh task-loss backward (coarse + optionally fine) w.r.t. Delta2 and
    summarises, per group, how members are being pulled apart. Does not touch the
    optimiser state (uses ``autograd.grad``). Returns ``cos_disagreement`` and
    ``pull_apart`` (see module docstring).
    """
    cl, fl = model(X)
    loss = F.cross_entropy(cl, y_coarse)
    if train_fine:
        loss = loss + F.cross_entropy(fl, y_fine)
    (grad,) = torch.autograd.grad(loss, model.delta2)  # (U, D)

    cos_list, pull_list = [], []
    for j in range(model.G):
        gb = grad[j * model.M:(j + 1) * model.M]  # (M, D)
        if model.M < 2:
            continue
        # Directional disagreement (mean pairwise cosine).
        gn = F.normalize(gb, dim=1, eps=1e-12)
        sim = gn @ gn.t()
        off = ~torch.eye(model.M, dtype=torch.bool, device=grad.device)
        cos_list.append(sim[off].mean())
        # Pull-apart force: deviation of each member from its group mean.
        diff = gb - gb.mean(dim=0, keepdim=True)
        pull_list.append(diff.norm(dim=1).mean())

    return dict(
        cos_disagreement=(torch.stack(cos_list).mean().item() if cos_list else float("nan")),
        pull_apart=(torch.stack(pull_list).mean().item() if pull_list else 0.0),
    )
