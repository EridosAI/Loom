"""exp19_score.py — EXP19 W-PERM scorer (B4/B5/B6 landed; B7/B8 grow here).

Every pre-flight measure is INDEX-LIST ONLY (no training) and computed at the DEPLOYED read window
read_at=500,000 of the h_max=1,000,000 fabric — never the smoke horizon (Jason 2026-07-14; SE≈0.18pp
at 500k vs ≈2pp at 4k). The B=T stratum count is folded into the pre-flight record.

  B4 zero_preceding_mask — THE STRATIFIER: onset exam with NO same-dwell wave preceding it in the
                           EMITTED order (the emitted-first wave of its dwell). From the realized
                           permutation (dwell_id), NEVER from pos. (Naive pos==1 red-teamed first.)
  B5 recency_companion   — per-B distribution: onset exams contaminated (a same-dwell wave precedes),
                           the immediately-before fraction, and the zero-preceding stratum count.
  B6 rho                 — per-B ρ(B) = P(two consecutive emitted waves share a dwell).
"""
import torch


# ---------------------------------------------------------------- index-list cores (dwell_id/is_exam)
def _first_occ(dwell_id):
    """bool[T]: True at the EMITTED-FIRST occurrence of each dwell_id (no same-dwell wave precedes)."""
    T = dwell_id.shape[0]
    order = torch.argsort(dwell_id, stable=True)          # positions grouped by dwell; stable = emitted order
    sd = dwell_id[order]
    isf = torch.ones(T, dtype=torch.bool)
    isf[1:] = sd[1:] != sd[:-1]                           # first element of each dwell group
    fo = torch.zeros(T, dtype=torch.bool)
    fo[order[isf]] = True
    return fo


def _nearest_preceding_same_dwell(dwell_id):
    """long[T]: emitted index of the nearest PRECEDING same-dwell wave, or -1 if none. The in-group
    (emitted-sorted) predecessor is the nearest same-dwell wave below each position."""
    T = dwell_id.shape[0]
    order = torch.argsort(dwell_id, stable=True)
    sd = dwell_id[order]
    same_prev = torch.zeros(T, dtype=torch.bool)
    same_prev[1:] = sd[1:] == sd[:-1]
    prev = torch.full((T,), -1, dtype=torch.long)
    prev[1:] = order[:-1]
    prev = torch.where(same_prev, prev, torch.full_like(prev, -1))
    out = torch.full((T,), -1, dtype=torch.long)
    out[order] = prev
    return out


def _zero_preceding(dwell_id, is_exam):
    return is_exam & _first_occ(dwell_id)


def _rho(dwell_id):
    if dwell_id.shape[0] < 2:
        return 0.0
    return float((dwell_id[1:] == dwell_id[:-1]).float().mean())


def _recency(dwell_id, is_exam):
    """B5 core. For each onset exam, the emitted distance to its nearest preceding same-dwell wave."""
    onset = torch.nonzero(is_exam, as_tuple=True)[0]
    n = int(onset.shape[0])
    ls = _nearest_preceding_same_dwell(dwell_id)[onset]
    contaminated = ls >= 0
    nc = int(contaminated.sum())
    dist = (onset - ls)[contaminated]
    immediate = int((dist == 1).sum())
    zpm = _zero_preceding(dwell_id, is_exam)
    return dict(n_onset=n, n_contaminated=nc,
                frac_contaminated=round(nc / max(1, n), 5),
                frac_immediate=round(immediate / max(1, n), 5),
                n_zero_preceding=int(zpm.sum()),
                frac_zero_preceding=round(int(zpm.sum()) / max(1, n), 5),
                median_dist=(int(dist.median()) if nc else None))


# ---------------------------------------------------------------- fab wrappers (B4/B5/B6)
def zero_preceding_mask(fab):
    return _zero_preceding(fab.dwell_id, fab.is_exam)


def rho(fab):
    return _rho(fab.dwell_id)


def recency_companion(fab):
    return _recency(fab.dwell_id, fab.is_exam)


# ---------------------------------------------------------------- pre-flight measure (index-list, 500k)
def preflight_measures(seed=0, h_max=1_000_000, read_at=500_000, B_paid=(32, 128, 512), B_esc=2048):
    """Build the DEPLOYED fabric (h_max), block-permute per B, and compute ρ(B) + the recency companion
    + the zero-preceding stratum over the read window [0, read_at) — the exact deployed slice. B=1
    (exp12_dwell) and B=T (exp12_shuffle, folded per Jason) are included. INDEX-LIST ONLY; no training."""
    import exp12_fabric as F
    import exp12_arms as X12
    loop, spec, cfg = X12.build_exp12("exp12_dwell", seed, h_max)
    fab = loop.stream
    Tf = fab.T
    d0, ex0 = fab.dwell_id, fab.is_exam
    W = read_at
    rows = {}
    for B in (1,) + tuple(B_paid) + (B_esc, Tf):
        if B == 1:
            d_em, ex_em = d0[:W], ex0[:W]
        else:
            g = torch.Generator().manual_seed(F.SEED_SHUFFLE + seed)
            perm = F.block_perm(Tf, B, g)
            d_em, ex_em = d0[perm][:W], ex0[perm][:W]
        rec = _recency(d_em, ex_em)
        rec["rho"] = round(_rho(d_em), 6)
        rows["T" if B == Tf else str(B)] = rec
    return dict(measure="EXP19 pre-flight (index-list, no training)", seed=seed, h_max=Tf,
                read_window=W, n_dwell_full=len(fab.dwell_k), by_B=rows)


if __name__ == "__main__":
    import json
    import sys
    out = preflight_measures()
    from pathlib import Path
    import exp14_arms as XA
    (XA.OUTDIR / "exp19_preflight_measures.json").write_text(json.dumps(out, indent=2, default=str))
    for B, r in out["by_B"].items():
        print(f"  B={B:>7}  rho={r['rho']:.5f}  frac_contaminated={r['frac_contaminated']:.4f}  "
              f"frac_immediate={r['frac_immediate']:.4f}  stratum={r['frac_zero_preceding']:.4f} "
              f"({r['n_zero_preceding']}/{r['n_onset']})")
    print(f"read window [0,{out['read_window']}) of h_max={out['h_max']} fabric")
