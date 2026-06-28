"""Pure metric functions for the characterisation sweep (no model state / no I/O).

`capacity_fraction` (self-normalized to the run's own plateau) is the cross-rate developmental axis;
`pam_grad_share` is the bounded [0,1] plateau-read; the S-curve signature and clean-G sustainedness
are computed inequalities over the seed distribution. See plan R2/§5/§6.
"""

from __future__ import annotations

import statistics


def pam_grad_share(gp, gj):
    s = gp + gj
    return (gp / s) if s > 0 else None


def capacity_fraction_series(depths, *, plateau_frac=0.20):
    """floor-subtracted, self-normalized, cummax-clamped capacity_fraction (plan R2).
    Returns (cap_list, full_depth, pooled_baseline)."""
    n = len(depths)
    k = max(1, int(n * plateau_frac))
    baseline = depths[0]
    plateau = statistics.mean(depths[-k:])
    denom = max(1e-9, plateau - baseline)
    cap, m = [], -1e18
    for d in depths:
        m = max(m, (d - baseline) / denom)
        cap.append(min(1.0, max(0.0, m)))
    return cap, plateau, baseline


def t95_trun(waves, cap, *, level=0.95, factor=1.25):
    t95 = next((waves[i] for i, c in enumerate(cap) if c >= level), waves[-1])
    return t95, factor * t95


def _phase_indices(waves, cap, t_run, *, toe, rapid, plateau_band_frac):
    """Indices (into the per-run row list) for toe / rapid / plateau bands, restricted to
    waves ≤ t_run. toe & rapid by capacity_fraction; plateau = final `plateau_band_frac` of the
    ≤t_run rows (by wave)."""
    inrun = [i for i, w in enumerate(waves) if w <= t_run]
    if not inrun:
        inrun = list(range(len(waves)))
    toe_i = [i for i in inrun if toe[0] <= cap[i] < toe[1]]
    rapid_i = [i for i in inrun if rapid[0] <= cap[i] < rapid[1]]
    kk = max(1, int(len(inrun) * plateau_band_frac))
    plateau_i = inrun[-kk:]
    return toe_i, rapid_i, plateau_i, inrun


def _quantile(xs, q):
    if not xs:
        return None
    s = sorted(xs)
    i = min(len(s) - 1, max(0, int(round(q * (len(s) - 1)))))
    return s[i]


def per_seed_share_stats(waves, shares, cap, t_run, spec, *, toe=None, rapid=None):
    """Per-seed toe/rapid/plateau shares + S-curve deltas + signature. `shares` may contain None
    (both grads ~0); those rows are dropped per band. toe/rapid override SPEC defaults (robustness)."""
    toe = toe or spec["toe"]; rapid = rapid or spec["rapid"]
    toe_i, rapid_i, plateau_i, _ = _phase_indices(
        waves, cap, t_run, toe=toe, rapid=rapid, plateau_band_frac=spec["plateau_band_frac"])

    def vals(idx):
        return [shares[i] for i in idx if shares[i] is not None]
    toe_v, rapid_v, plateau_v = vals(toe_i), vals(rapid_i), vals(plateau_i)
    toe_share = statistics.mean(toe_v) if toe_v else None
    rapid_peak = _quantile(rapid_v, spec["rapid_quantile"]) if rapid_v else None
    plateau_share = statistics.mean(plateau_v) if plateau_v else None
    d_rapid = (rapid_peak - toe_share) if (rapid_peak is not None and toe_share is not None) else None
    d_plateau = (plateau_share - rapid_peak) if (plateau_share is not None and rapid_peak is not None) else None
    s_curve = bool(d_rapid is not None and d_plateau is not None
                   and d_rapid > 0 and d_plateau <= spec["tol_plateau"])
    return dict(toe_share=toe_share, rapid_peak_share=rapid_peak, plateau_share=plateau_share,
                delta_rapid=d_rapid, delta_plateau=d_plateau, s_curve_signature=s_curve)


def sustained(flags, waves, t_run, *, n_consec, x_pct):
    """clean-G / autonomous sustainedness: holds for ≥ n_consec consecutive eval windows OR ≥ x_pct
    of the ≤t_run rows — whichever STRICTER (both required). Returns (sustained_bool, longest_run,
    frac)."""
    idx = [i for i, w in enumerate(waves) if w <= t_run]
    seq = [bool(flags[i]) for i in idx]
    longest, cur = 0, 0
    for f in seq:
        cur = cur + 1 if f else 0
        longest = max(longest, cur)
    frac = (sum(seq) / len(seq)) if seq else 0.0
    return bool(longest >= n_consec and frac >= x_pct), longest, frac


def agg(xs):
    """exp03 stacked_corner idiom."""
    xs = [x for x in xs if x is not None]
    return dict(mean=(statistics.mean(xs) if xs else None),
                sd=(statistics.pstdev(xs) if len(xs) > 1 else 0.0), n=len(xs))


def frac_true(bools):
    bools = [b for b in bools if b is not None]
    return (sum(1 for b in bools if b) / len(bools)) if bools else 0.0
