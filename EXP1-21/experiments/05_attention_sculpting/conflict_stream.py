"""The 4->8 CONFLICT stimulus (Stage-1 attention-sculpting, SPEC §2).

Drop-in replacement for ``stream.Stimulus`` (same ``centre``/``raw``/``raw_clean``/``Q``
interface, so the existing ``Stage0Loop`` consumes it unchanged), with the one new structure
the empty-gap sweep entirely lacked: **two crossed FINE member axes** pulling in opposite
directions.

  * A  — coarse DECOY groups (n_A), salient (R_coarse), word-irrelevant. Resolved by the
    lam1 clock (Delta1), not the Delta2 battleground. As in Stage-0.
  * DISTRACTOR — a fine axis, HIGH visual salience (r_distractor), freely splittable by vision
    alone, but **associatively inert** (the word does not name it). The "colour" role.
  * CATEGORY — a fine axis, LOWER visual salience (r_category), **associatively load-bearing**
    (the word names it). The "handle/hole" role.

Member index ``b in [0, n_distractor*n_category)`` decodes to ``(distractor, category) =
divmod(b, n_category)`` (so ``category = b % n_category``, ``distractor = b // n_category``).
The 8 leaves of a group therefore contain BOTH "same category / different appearance"
(different distractor, same category — the word must pull together) AND "different category /
similar appearance" (same distractor, different category — the word must push apart), which is
exactly the conflict the rig needs (SPEC §2). Disjoint subspaces, rotated to a generic frame.

Conflict-strength is set by the salience GAP (how far r_distractor exceeds r_category); the
ladder sweeps it (SPEC §2, the dense axis). Vision-alone provably occupies the salient distractor
(Step-0 check (a)); the word's job is to redirect occupancy to the category (the test).
"""

from __future__ import annotations

import torch


class ConflictStimulus:
    """4->8 conflict geometry. Interface-compatible with ``stream.Stimulus``."""

    def __init__(self, D: int, n_A: int, n_distractor: int, n_category: int, *,
                 R_coarse: float = 5.0, r_distractor: float = 3.0, r_category: float = 1.0,
                 sigma: float = 0.20, seed: int = 0,
                 ablate_distractor: bool = False, ablate_category: bool = False):
        n_B = n_distractor * n_category
        need = n_A + n_distractor + n_category
        if need > D:
            raise ValueError(f"need n_A+n_distractor+n_category <= D; got {need} > {D}")
        g = torch.Generator().manual_seed(seed)
        self.D, self.n_A, self.n_B = D, n_A, n_B
        self.n_distractor, self.n_category = n_distractor, n_category
        self.sigma = sigma
        self.r_distractor = 0.0 if ablate_distractor else r_distractor
        self.r_category = 0.0 if ablate_category else r_category

        centre = torch.zeros(n_A, n_B, D)
        for a in range(n_A):
            for b in range(n_B):
                d, c = divmod(b, n_category)              # distractor, category
                v = torch.zeros(D)
                v[a] = R_coarse                           # coarse decoy (salient)
                v[n_A + d] = self.r_distractor            # distractor fine axis (salient, inert)
                v[n_A + n_distractor + c] = self.r_category  # category fine axis (subtle, named)
                centre[a, b] = v
        Q, _ = torch.linalg.qr(torch.randn(D, D, generator=g))
        self.centre = centre @ Q.t()                      # (n_A, n_B, D), rotated
        self.Q = Q

    # -- stream.Stimulus interface --------------------------------------------------------------
    def raw(self, a: torch.Tensor, b: torch.Tensor, gen: torch.Generator) -> torch.Tensor:
        mu = self.centre[a, b]
        return mu + self.sigma * torch.randn(mu.shape, generator=gen)

    def raw_clean(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return self.centre[a, b]

    # -- (distractor, category) <-> member-index helpers ----------------------------------------
    def category_of(self, b):
        return b % self.n_category

    def distractor_of(self, b):
        return b // self.n_category

    def member_index(self, d, c):
        return d * self.n_category + c
