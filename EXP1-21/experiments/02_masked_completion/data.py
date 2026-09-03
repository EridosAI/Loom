"""Shared-interior sequence family for the masked-completion rig (SPEC, "Data").

The one property that makes the test valid (SPEC sec. "The one property..."): the cue
must *require order information* to complete. We build sequences::

    seq_k = [begin_k] + interior_{h(k)} + [end_k]

with three deliberate structures:

* **begin <-> end bijection.** ``end_k = perm(begin_k)`` over a *shared* symbol set, so
  a symbol that is a begin in one sequence is an end in another (position-varied
  symbols), and knowing the end uniquely determines the begin (end-cues-beginning is
  a real inference, not lookup).
* **interior = h(begin), non-injective.** Several begins map to the *same* interior
  fragment, so the interior alone is ambiguous about which sequence it is -- only the
  endpoints resolve it (shared interior fragments).
* Because interior and end are both functions of begin (and begin of end), **either
  endpoint determines the whole sequence**, while the interior does not.

This is a tiny, fully-determined family (one sequence per begin); the rig tests
whether attention *direction* permits end->beginning recall, not generalisation.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class Family:
    X: torch.Tensor          # (K, L) the sequences
    V: int                   # vocab size (symbol ids 0..V-1; MASK is a separate id V)
    L: int
    begin_pos: int
    end_pos: int
    interior_pos: list
    n_begins: int            # distinct symbols at the begin position (for chance)


def build_family(K: int = 16, n_interior: int = 4, pool: int = 4, V: int = 20,
                 seed: int = 0) -> Family:
    g = torch.Generator().manual_seed(seed)
    L = n_interior + 2
    assert K <= V, "begin/end symbols are drawn from the shared vocab 0..V-1"

    begins = list(range(K))                      # begin_k = k
    end_perm = torch.randperm(K, generator=g)    # bijection over the SAME K symbols
    ends = end_perm.tolist()                      # end_k = perm(k), also in 0..K-1

    # Interior fragment pool; assigned non-injectively so begins share interiors.
    frags = [torch.randint(0, V, (n_interior,), generator=g).tolist() for _ in range(pool)]

    seqs = [[begins[k]] + frags[k % pool] + [ends[k]] for k in range(K)]
    X = torch.tensor(seqs, dtype=torch.long)

    return Family(X=X, V=V, L=L, begin_pos=0, end_pos=L - 1,
                  interior_pos=list(range(1, L - 1)), n_begins=K)


def validity_report(fam: Family) -> dict:
    """Confirm the structure that makes the test valid (see module docstring)."""
    X, L = fam.X, fam.L
    bp, ep, ip = fam.begin_pos, fam.end_pos, fam.interior_pos

    # Shared interior: at least two sequences with an identical interior block.
    interiors = [tuple(row[ip].tolist()) for row in X]
    shared_interior = len(set(interiors)) < len(interiors)
    max_share = max(interiors.count(t) for t in set(interiors))

    # Position-varied symbols: a symbol appearing at >= 2 distinct positions.
    pos_of = {}
    for row in X:
        for p, s in enumerate(row.tolist()):
            pos_of.setdefault(int(s), set()).add(p)
    position_varied = sum(1 for s, ps in pos_of.items() if len(ps) >= 2)

    # End determines begin (function end_symbol -> begin_symbol is single-valued).
    end_to_begin = {}
    end_det_begin = True
    for row in X:
        e, b = int(row[ep]), int(row[bp])
        if end_to_begin.setdefault(e, b) != b:
            end_det_begin = False

    # Interior is ambiguous about begin (some interior maps to >1 begin).
    interior_to_begins = {}
    for row in X:
        interior_to_begins.setdefault(tuple(row[ip].tolist()), set()).add(int(row[bp]))
    interior_ambiguous = any(len(bs) > 1 for bs in interior_to_begins.values())

    return dict(
        n_sequences=len(X), seq_len=L,
        shared_interior=shared_interior, max_sequences_sharing_an_interior=max_share,
        position_varied_symbols=position_varied,
        end_determines_begin=end_det_begin,
        interior_ambiguous_about_begin=interior_ambiguous,
        chance_begin=1.0 / fam.n_begins,
    )
