"""exp19_score.py — EXP19 W-PERM scorer (grows as the build lands; B4 first).

B4 — zero_preceding_mask(fab): THE STRATIFIER. An onset exam is in the zero-preceding stratum iff NO
wave of its own dwell precedes it in the EMITTED order (it is the FIRST wave of its dwell in emitted
order). Computed from the REALIZED PERMUTATION (emitted-order dwell_id), NEVER from `pos`.

Part D discipline (red-team rule, CORRIDOR Conduct): this ships NAIVE first — `zero_preceding_mask ==
pos==1` — and wp-strat-label is shown RED (the pos==1 mask and the stratifier coincide at B>1) BEFORE
the property version exists. Stratifying on the LABEL (pos==1) instead of the PROPERTY would score
contaminated exams as recency-free and certify the arm's own confound.
"""
import torch


def zero_preceding_mask(fab):
    """THE STRATIFIER (B4). An onset exam is in the zero-preceding stratum iff NO wave of its own dwell
    precedes it in the EMITTED order — i.e. it is the FIRST wave of its dwell in emitted order AND an
    onset exam. Computed from the realized permutation (emitted-order `dwell_id`), NEVER from `pos`.
    (The naive `pos == 1` version was confirmed RED against wp-strat-label first — Part D / red-team rule.)"""
    dwell_id = fab.dwell_id
    T = dwell_id.shape[0]
    order = torch.argsort(dwell_id, stable=True)           # group positions by dwell; stable = emitted order
    sorted_d = dwell_id[order]
    is_first_in_group = torch.ones(T, dtype=torch.bool)
    is_first_in_group[1:] = sorted_d[1:] != sorted_d[:-1]  # first element of each dwell group (emitted-earliest)
    first_occ = torch.zeros(T, dtype=torch.bool)
    first_occ[order[is_first_in_group]] = True             # emitted-first occurrence of each dwell
    return fab.is_exam & first_occ
