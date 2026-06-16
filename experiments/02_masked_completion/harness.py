"""Masked-LM training and reconstruction eval (SPEC, "Metrics").

``train`` learns the family with random masking. ``reconstruct`` does a *single*
forward pass: mask everything except the cue positions, fill all masked positions at
once. ``reconstruct_iterative`` feeds predictions back over several passes -- used only
to check that iteration does NOT improve on the single pass (the "at-once" condition).
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def _apply_mask(X, keep_mask, mask_id):
    """Return a copy of X with positions where keep_mask is False set to mask_id."""
    out = X.clone()
    out[~keep_mask] = mask_id
    return out


def train(model, X, steps=3000, lr=1e-3, seed=0):
    """Masked-LM trained for random access: each step, each sequence keeps a *random
    number* of visible positions (1..L-1) and predicts the rest. Sampling the number
    of cues uniformly (rather than a fixed mask rate) guarantees coverage of sparse,
    single-cue configurations -- exactly the random-access property under test, so the
    end->beginning pathway is learned robustly rather than incidentally. Full-batch."""
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    K, L = X.shape
    losses = []
    for _ in range(steps):
        # per-row number of visible (cued) positions in [1, L-1]
        n_keep = torch.randint(1, L, (K,), generator=g)
        scores = torch.rand(K, L, generator=g)
        ranks = scores.argsort(dim=1).argsort(dim=1)  # 0..L-1 ranking per row
        keep = ranks < n_keep.unsqueeze(1)            # keep the n_keep lowest-scoring
        masked = ~keep
        inp = _apply_mask(X, keep, model.mask_id)
        logits = model(inp)
        loss = F.cross_entropy(logits[masked], X[masked])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        losses.append(loss.item())
    return losses


@torch.no_grad()
def reconstruct(model, X, cue_positions):
    """Single forward pass. Cue = positions kept visible; everything else masked and
    filled simultaneously. Returns predicted token ids (K, L)."""
    K, L = X.shape
    keep = torch.zeros(K, L, dtype=torch.bool)
    keep[:, cue_positions] = True
    inp = _apply_mask(X, keep, model.mask_id)
    preds = model(inp).argmax(dim=-1)
    # keep the cued positions as given (they are observed, not predicted)
    preds[keep] = X[keep]
    return preds


@torch.no_grad()
def reconstruct_iterative(model, X, cue_positions, n_iter=4):
    """Iterative refinement: re-feed predictions for n_iter passes. Used to show that
    extra passes do not beat the single pass (i.e. completion is genuinely at-once)."""
    K, L = X.shape
    keep = torch.zeros(K, L, dtype=torch.bool)
    keep[:, cue_positions] = True
    cur = _apply_mask(X, keep, model.mask_id)
    for _ in range(n_iter):
        preds = model(cur).argmax(dim=-1)
        cur = X.clone()
        cur[~keep] = preds[~keep]   # write predictions back into masked slots
    cur[keep] = X[keep]
    return cur


@torch.no_grad()
def region_accuracy(preds, X, positions):
    """Mean per-position reconstruction accuracy over the given positions."""
    if not positions:
        return float("nan")
    sel = preds[:, positions] == X[:, positions]
    return sel.float().mean().item()
