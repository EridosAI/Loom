"""FREE-READ (i) — RENDER-GAIN AUDIT (runs FIRST; gates SCATTER's F5; qualifies §10.27 'as tested').

Memo: docs/FREE_READS_MEMO.md §(i).  Recipe (verbatim): MECHANISM_MAP_v1_2_RECONCILED.md §4 —
"per-dwell mean render-step / pose-step ratio along the realized [L1] trajectory vs the same ratio
over random pose pairs." Anisotropy of the pose->render appearance gains.

In this substrate the pose is the K=4 nuisance-coefficient vector and the "render" (a pose's vision
contribution) is pose @ nuis_axes (the fabric's committed pose->stimulus map, exp12_fabric.py:139/353).
The nuisance axes are orthonormal rows (basis @ Q.t(), Q orthogonal) so the map is a linear isometry —
this read MEASURES that (per-axis gains, cross-axis leakage, directional-gain anisotropy over random
unit directions, realized within-dwell ratio, random-pose-pair ratio); it does not assume it.

Read-only. Builds the frozen L1 (orbit) fabric deterministically (torch threads=1). One JSON out.
"""
import json, statistics
from pathlib import Path

import torch
torch.set_num_threads(1)                          # determinism contract

import exp12_arms as X12                           # build_exp12 (committed fabric access)
import exp17_score as S                            # committed constants (X17_ARM, X17_SELECT_T)

HERE = Path(__file__).resolve().parent
OUT = HERE / "exp08"
ARM = S.X17_ARM                                    # "exp12_dwell_orbit" — the pinned L1 arm
SEEDS = list(range(8))                             # X17 verdict seeds {0..7}
WINDOW = S.X17_SELECT_T                            # 100_000 (committed selection scale; the ratio is
                                                   #   T-invariant under the isometry — representative)
N_DIR = 20000                                      # random unit-direction / pose-pair probes
RNG_BASE = 17                                      # fixed sampling seed (determinism)


def _render(pose, axes):
    """pose (.,K) -> render (.,D): pose @ nuis_axes (the committed pose->stimulus contribution)."""
    return pose @ axes


def per_seed(seed):
    loop, _spec, _cfg = X12.build_exp12(ARM, seed, WINDOW)
    fab = loop.stream
    axes = loop.stim.nuis_axes.double()            # (K, D) the render map
    K = axes.shape[0]
    nuis = fab.nuis.double()
    pos = fab.pos.tolist()
    n = min(WINDOW, nuis.shape[0])

    # per-axis render gain = ||e_k @ axes|| ; cross-axis leakage = max_{i!=j} |axes_i . axes_j|
    per_axis_gain = [float(axes[k].norm()) for k in range(K)]
    cross_axis_max = max(abs(float(axes[i] @ axes[j]))
                         for i in range(K) for j in range(K) if i != j)

    # directional anisotropy: gain(u) = ||u @ axes|| over random unit u in R^K (isometry -> all 1)
    gd = torch.Generator().manual_seed(RNG_BASE + seed)
    U = torch.randn(N_DIR, K, generator=gd, dtype=torch.float64)
    U = U / U.norm(dim=1, keepdim=True)
    dgain = (U @ axes).norm(dim=1)
    dg_min, dg_max = float(dgain.min()), float(dgain.max())
    anisotropy_ratio = dg_max / dg_min

    # realized within-dwell step ratio ||d_render|| / ||d_pose|| (consecutive frames, pos>1)
    dpose = nuis[1:n] - nuis[:n - 1]
    drender = _render(nuis[1:n], axes) - _render(nuis[:n - 1], axes)
    pn = dpose.norm(dim=1); rn = drender.norm(dim=1)
    within = [float(rn[t - 1] / pn[t - 1]) for t in range(1, n) if pos[t] > 1 and pn[t - 1] > 0]

    # random pose pairs from the family marginal (same sigma + clamp as the committed onset draw)
    sig = float(loop.stim.coeff_std)
    bound = X12.F.FAMILY_BOUND_SIG * sig
    gp = torch.Generator().manual_seed(RNG_BASE * 7 + seed)
    A = (sig * torch.randn(N_DIR, K, generator=gp, dtype=torch.float64)).clamp(-bound, bound)
    B = (sig * torch.randn(N_DIR, K, generator=gp, dtype=torch.float64)).clamp(-bound, bound)
    dpn = (A - B).norm(dim=1)
    drn = (_render(A, axes) - _render(B, axes)).norm(dim=1)
    rpair = [float(drn[i] / dpn[i]) for i in range(N_DIR) if float(dpn[i]) > 0]

    return dict(
        seed=seed, n_within_steps=len(within),
        per_axis_gain=[round(g, 12) for g in per_axis_gain],
        cross_axis_leakage_max=cross_axis_max,
        directional_gain_min=dg_min, directional_gain_max=dg_max,
        anisotropy_ratio=anisotropy_ratio,
        realized_ratio_mean=statistics.mean(within),
        realized_ratio_sd=statistics.pstdev(within),
        realized_ratio_min=min(within), realized_ratio_max=max(within),
        randompair_ratio_mean=statistics.mean(rpair),
        randompair_ratio_sd=statistics.pstdev(rpair))


def main():
    per = [per_seed(s) for s in SEEDS]
    aniso = [p["anisotropy_ratio"] for p in per]
    gains = [g for p in per for g in p["per_axis_gain"]]
    pooled = dict(
        anisotropy_ratio_max=max(aniso),
        anisotropy_ratio_mean=statistics.mean(aniso),
        per_axis_gain_min=min(gains), per_axis_gain_max=max(gains),
        cross_axis_leakage_max=max(p["cross_axis_leakage_max"] for p in per),
        realized_ratio_mean=statistics.mean(p["realized_ratio_mean"] for p in per),
        randompair_ratio_mean=statistics.mean(p["randompair_ratio_mean"] for p in per))
    out = dict(
        read="(i) render-gain audit",
        memo_section="docs/FREE_READS_MEMO.md §(i)",
        recipe="MECHANISM_MAP_v1_2_RECONCILED.md §4 (verbatim)",
        method=("pose = K=4 nuisance coeffs; render(pose) = pose @ nuis_axes (exp12_fabric.py:139,353). "
                "per_axis_gain = ||axes_k||; cross_axis_leakage = max_{i!=j}|axes_i.axes_j|; "
                "anisotropy_ratio = max/min of ||u@axes|| over 20000 random unit u in R^K; "
                "realized_ratio = ||d_render||/||d_pose|| over within-dwell consecutive frames; "
                "randompair_ratio = same over 20000 random family-marginal pose pairs. float64."),
        inputs=dict(arm=ARM, seeds=SEEDS, window=WINDOW,
                    built_by="exp12_arms.build_exp12 (committed); axes from loop.stim.nuis_axes",
                    code_modules=["exp12_arms.py", "exp12_fabric.py", "exp17_score.py"]),
        consequence=dict(
            memo_condition="severe anisotropy -> ratification-class gain floor in SCATTER's F5 ball "
                           "sampling; and it qualifies §10.27's 'as tested'",
            measured_anisotropy_ratio_max=max(aniso),
            per_axis_gain_range=[min(gains), max(gains)],
            triggered="N (routes: 'severe' threshold is unpinned in the memo -> seat rules; the map is "
                      "isotropic to float precision by orthonormal construction, so no gain floor is "
                      "indicated and 'as tested' is NOT qualified on perceptual-weakness grounds)"),
        pooled=pooled,
        per_seed=per)
    OUT.mkdir(exist_ok=True)
    (OUT / "freeread_1_render_gain.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print("render-gain: anisotropy_max=%.3e  per_axis_gain in [%.8f, %.8f]  realized_ratio_mean=%.8f"
          % (max(aniso), min(gains), max(gains), pooled["realized_ratio_mean"]))
    print("-> exp08/freeread_1_render_gain.json")


if __name__ == "__main__":
    main()
