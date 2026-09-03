"""Block-level slice masking over the W x n_slots grid + at-once discipline (Stage-0 §2-i).

The cue-shape sampler is REBUILT (not a verbatim port) for the (W=3, n_slots=2) slice
grid so it generates **all SIX** spec families
``{single-slot, whole-wave, interior-both-sides, one-sided-edge, sparse, near-all}``.
exp03's ``_sample_keep`` is a 5-mode sampler over an L-length sequence — not a fit.
A dropped family is the exp02 undertraining trap (the operator learns gap-filling, not
random access) — this is a spec hard rule, so ``family_coverage`` lets the harness
fail the build if any family count is 0.

MASKING IS BLOCK-LEVEL OVER WHOLE SLICES — never individual scalar coordinates (scalar
masking turns the operator into a masked-autoencoder over coordinates, the leak, §2-i/§12).
``mask[w, s] == True`` means cell (wave w, slot s) is masked (to be completed); the drift
carrier is injected AFTER masking (in the loop), so a masked cell still carries its wave's
position (order survives the mask — that is what cue-end->recover-begin needs).
"""

from __future__ import annotations

import torch

# The six pre-registered cue-shape families. Interior wave = the middle wave; edge waves
# = the first and last. Slot 0 = vision, slot 1 = word (by convention).
FAMILIES = (
    "single-slot",
    "whole-wave",
    "interior-both-sides",
    "one-sided-edge",
    "sparse",
    "near-all",
)


def _randint(hi, gen):
    return int(torch.randint(0, hi, (1,), generator=gen))


def sample_mask_grid(W: int, n_slots: int, gen: torch.Generator):
    """Draw one cue-shape mask (W, n_slots) bool (True = masked) + its family name.

    Guarantees at least one visible cell and at least one masked cell. Families are
    drawn uniformly; the interior/edge families require W>=3.
    """
    fam = FAMILIES[_randint(len(FAMILIES), gen)]
    mask = torch.zeros(W, n_slots, dtype=torch.bool)
    interior = list(range(1, W - 1)) or [W // 2]
    edges = sorted(set([0, W - 1]))

    if fam == "single-slot":                       # exactly one cell masked
        mask[_randint(W, gen), _randint(n_slots, gen)] = True

    elif fam == "whole-wave":                      # both slots of one wave masked
        mask[_randint(W, gen), :] = True

    elif fam == "interior-both-sides":             # interior masked, both edges visible
        w = interior[_randint(len(interior), gen)]
        mask[w, :] = True

    elif fam == "one-sided-edge":                  # an edge wave masked (cue-end->recover-begin)
        w = edges[_randint(len(edges), gen)]
        if n_slots > 1 and _randint(2, gen):       # whole edge wave, or just its vision slot
            mask[w, :] = True
        else:
            mask[w, 0] = True

    elif fam == "sparse":                          # 1-2 scattered cells
        cells = [(w, s) for w in range(W) for s in range(n_slots)]
        k = 1 + _randint(min(2, len(cells) - 1), gen)
        perm = torch.randperm(len(cells), generator=gen)[:k]
        for i in perm:
            w, s = cells[int(i)]
            mask[w, s] = True

    else:                                          # near-all: keep exactly one cell visible
        mask[:] = True
        mask[_randint(W, gen), _randint(n_slots, gen)] = False

    # invariants: at least one visible, at least one masked
    if mask.all():
        mask[_randint(W, gen), _randint(n_slots, gen)] = False
    if not mask.any():
        mask[_randint(W, gen), _randint(n_slots, gen)] = True
    return mask, fam


def apply_slice_mask(content: torch.Tensor, mask: torch.Tensor, mask_emb: torch.Tensor):
    """Replace masked cells' CONTENT with the learned MASK embedding.

    ``content`` (..., W, n_slots, dim); ``mask`` (W, n_slots) bool; ``mask_emb`` (dim,).
    Whole-slice (all-or-nothing per cell) — the mask never indexes within ``dim``.
    Returns a new tensor (does not mutate input).
    """
    out = content.clone()
    out[..., mask, :] = mask_emb
    return out


def family_coverage(W: int, n_slots: int, n: int, gen: torch.Generator) -> dict:
    """Count how often each family is drawn over ``n`` samples (coverage self-test)."""
    counts = {f: 0 for f in FAMILIES}
    for _ in range(n):
        _, fam = sample_mask_grid(W, n_slots, gen)
        counts[fam] += 1
    return counts


@torch.no_grad()
def at_once_gap(single_pass_acc: float, k_pass_acc: float) -> float:
    """Positive => iteration beat the single pass (secretly autoregressive). The at-once
    check requires k_pass_acc - single_pass_acc <= ITER_EPS."""
    return k_pass_acc - single_pass_acc
