"""EXP12 — the scene-persistence fabric (harness-side world data; prereg §1–§5, §13.1–3).

The fabric is PURE DATA, generated before wave 0 on dedicated seeded substreams (never
loop.gen, never probe generators; §5): per-wave member, nuisance pose, background pose,
stimulus noise, mask slot, and the harness-side role flags (dwell id / position / exam)
that exist for SCORING ONLY — the system sees stimulus + mask, nothing else ("time is
felt, not coded": no timestamps, no dwell indices, no boundary flags as signal).

Construction (§13, ratified 2026-07-04; §13.2 AMENDED IN PLACE per Ruling 1, 2026-07-05):
  * Dwell law: k = K_MIN + Geom0(P_GEOM) — support-{0,1,...} geometric, so k_min = 2 is
    REALIZABLE (support {2..48}, E[k] = 11, cap-hit ~0.7%). The as-ratified arithmetic
    embedded a support error (Geom support >=1 made k=2 unreachable); the pin's grounds
    outrank the constants' letter. Cap-hit ceiling ASSERT at 1% (§2 pin 2).
  * Member draw: uniform over the 16 members with NO immediate same-member repeat.
  * Walk (§13.1): the EXP10 pinned nuisance family VERBATIM (K=4 complement-block
    orthonormal axes @ Q^T, per-axis coeff_std READ from exp10_calibration.json — never a
    re-typed literal). Onset pose ~ family marginal; within dwell per-axis OU reverting
    to the onset pose, tau = 4 waves, STATIONARY deviation sd = 0.25 * family sigma
    (per-step sigma DERIVED: sd * sqrt(1-(1-1/tau)^2), never pinned directly).
    Reflection at the family bounds = |total coeff| <= 3 * family sigma (CC mechanical
    choice, surfaced: the family marginal's ±3σ support proxy; onset draws clamped to the
    same bounds so a fresh pose never starts outside them).
  * Background (§1 amendment): ONE fixed configuration (pin-to-constant — drawn once on a
    FIXED dedicated key, identical across seeds and arms, recorded in the manifest) on 4
    further complement axes + continuous OU jitter around it (same walk law, per-seed
    stream), reflected at the same ±3σ bounds.
  * Mask schedule (§3, §13.3): one slot masked per wave; position-1 word-mask GUARANTEED
    (the onset exam) unless the dwell is a PROBE dwell (§13.10). BOTH per-dwell coins
    (suppression + onset slot) are drawn for EVERY dwell regardless of rate, so per-dwell
    g_mask consumption is constant: a stage-two rate change flips only which dwells are
    suppressed (nested across rates), never the downstream draw alignment. Mid-dwell =
    50:50 coin. The schedule leaks boundary, never identity — asserted numerically below.
  * A-SHUFFLE: the IDENTICAL waves and the IDENTICAL mask schedule, order-shuffled
    (one permutation from a dedicated substream). Same exams, different order. Role
    flags travel with the waves for scoring only.

Independence asserts (§5/§13.8 — the EXP10 §7.1 machinery extended; epsilon form
inherited = shuffle-null 99th percentile, here with the exchangeability-correct null =
permuting the dwell->member assignment, which preserves the dwell/lag structure):
per-lag nuisance ⟂ member over lags <= K_MAX (multiplicity-controlled: the null is of
the MAX over lags); k ⟂ member (chi-square statistic vs permutation null); mid-dwell
schedule ⟂ member (chi-square vs permutation null; the exam is structural at position 1
by construction, recorded not tested); background ⟂ member (lag-0 corr vs the same
null). All HARD asserts at manifest time.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

from conflict_stream import ConflictStimulus                  # noqa: E402

OUTDIR = _HERE / "exp08"

# --- §13.2 dwell law (AMENDED Ruling 1: Geom0 support, k_min realizable) ---
P_GEOM = 0.1                     # E[k] = K_MIN + (1-p)/p = 11
K_MIN = 2
K_MAX = 48                       # cap-hit = 0.9^47 ~ 0.707% theoretical; ceiling assert 1%
CAP_CEILING = 0.01
# --- §13.1 walk (ratified) ---
TAU = 4.0                        # OU decorrelation time (waves); ordering ~2 < 4 < E[k]=12
THETA = 1.0 / TAU
STATIONARY_FRAC = 0.25           # stationary deviation sd = 0.25 * family sigma (PIN)
FAMILY_BOUND_SIG = 3.0           # reflect |total coeff| at 3 * family sigma (CC choice, surfaced)
K_AXES = 4                       # EXP10 pinned family (verified vs exp10_calibration.json)
BG_AXES = 4                      # background block: the remaining complement axes
# --- substream key bases (§5; recorded in every manifest) ---
SEED_DWELL = 91000
SEED_MEMBER = 92000
SEED_NUIS = 93000
SEED_BG_CONST = 94000            # FIXED key — pin-to-constant, no per-seed offset
SEED_BG_JIT = 95000
SEED_MASK = 96000
SEED_NOISE = 97000
SEED_SHUFFLE = 98000
SEED_PROBE_RAW = 99000           # EXP12Stimulus.raw() marginal draws (probes/spread only)


def family() -> dict:
    """The EXP10 pinned nuisance family, READ from the committed calibration artifact
    (never a re-typed literal). CC-VERIFIED 2026-07-05: k_axes=4, coeff_std=0.5
    (rung x2.0 = total RMS 2x r_category / sqrt(K))."""
    art = json.loads((OUTDIR / "exp10_calibration.json").read_text())
    p = art["proposed"]
    assert p["k_axes"] == K_AXES, "EXP10 family k_axes changed under us"
    return dict(coeff_std=float(p["coeff_std"]), k_axes=int(p["k_axes"]))


def sigma_step(coeff_std: float) -> float:
    """Per-step OU sigma DERIVED from the stationary pin (never pinned directly):
    stationary var of the deviation = sigma_step^2 / (1 - (1-theta)^2)."""
    return STATIONARY_FRAC * coeff_std * math.sqrt(1.0 - (1.0 - THETA) ** 2)


# ------------------------------------------------------------------ the stimulus
class EXP12Stimulus(ConflictStimulus):
    """ConflictStimulus + the nuisance axes (EXP10 family, complement indices
    [n_id, n_id+K)) + the background axes (complement indices [n_id+K, n_id+K+BG)) +
    the FIXED background configuration folded into `centre` (probes and the vision
    init-center see the standing world: member centre + background at rest).

    `centre_id` keeps the identity-only centres (the fabric composes raw waves from
    them so background is added exactly once). `raw()` (probe/spread path only — the
    TRAINING waves come precomputed from the fabric) adds marginal draws from a
    dedicated counter-keyed stream: nuisance at the OU stationary TOTAL sd
    (= family sigma * sqrt(1 + 0.25^2)), background jitter at the stationary deviation
    sd around the constant — so probe batches sample the distribution the system
    actually lives in. Counter caveat (EXP10, carried): raw() advances the counter per
    call; call order is deterministic, so replays are exact, but inserting/removing a
    probe shifts subsequent keys."""

    def __init__(self, *args, coeff_std: float, probe_seed: int, **kw):
        super().__init__(*args, **kw)
        self.coeff_std = float(coeff_std)
        self.probe_seed = int(probe_seed)
        self._calls = 0
        n_id = self.n_A + self.n_distractor + self.n_category
        if n_id + K_AXES + BG_AXES > self.D:
            raise ValueError("complement block too small for nuisance + background")
        basis = torch.zeros(K_AXES + BG_AXES, self.D)
        for i in range(K_AXES + BG_AXES):
            basis[i, n_id + i] = 1.0
        rot = basis @ self.Q.t()
        self.nuis_axes = rot[:K_AXES]                      # (K, D) ⟂ identity axes
        self.bg_axes = rot[K_AXES:]                        # (BG, D) ⟂ identity + nuisance
        # the fixed background configuration (pin-to-constant): FIXED key, all seeds/arms
        gb = torch.Generator().manual_seed(SEED_BG_CONST)
        bound = FAMILY_BOUND_SIG * self.coeff_std
        self.bg_const = (self.coeff_std * torch.randn(BG_AXES, generator=gb)
                         ).clamp(-bound, bound)            # (BG,)
        self.centre_id = self.centre                       # identity-only centres
        self.centre = self.centre_id + (self.bg_const @ self.bg_axes)  # standing world

    def raw(self, a, b, gen):
        base = self.centre[a, b] + self.sigma * torch.randn(
            self.centre[a, b].shape, generator=gen)
        g = torch.Generator().manual_seed(self.probe_seed * 1_000_003 + self._calls)
        self._calls += 1
        n = base.shape[0] if base.dim() > 1 else 1
        tot_sd = self.coeff_std * math.sqrt(1.0 + STATIONARY_FRAC ** 2)
        nuis = (tot_sd * torch.randn(n, K_AXES, generator=g)) @ self.nuis_axes
        bgj = (STATIONARY_FRAC * self.coeff_std
               * torch.randn(n, BG_AXES, generator=g)) @ self.bg_axes
        return base + nuis.reshape(base.shape) + bgj.reshape(base.shape)


# ------------------------------------------------------------------ the fabric
@dataclass
class Fabric:
    # per-wave (all length T; A-SHUFFLE = the same tensors, one permutation applied)
    a: torch.Tensor              # coarse index
    b: torch.Tensor              # fine index (distractor*n_cat + category)
    member: torch.Tensor         # a*4 + b
    cat: torch.Tensor            # word label = b % n_category
    dwell_id: torch.Tensor       # scoring only — never presented
    pos: torch.Tensor            # 1-based dwell position — scoring only
    mask_slot: torch.Tensor      # 0 = vision masked, 1 = word masked
    is_exam: torch.Tensor        # scheduled onset exam (bool)
    is_probe_exam: torch.Tensor  # suppressed-exam probe dwell onset (bool, §13.10)
    nuis: torch.Tensor           # (T, K) realized nuisance coefficients
    bg: torch.Tensor             # (T, BG) realized TOTAL background coefficients
    raw: torch.Tensor            # (T, D) the presented stimulus (noise included)
    # dwell-level (scoring/asserts)
    dwell_member: torch.Tensor
    dwell_k: torch.Tensor
    cap_hits: int
    truncated_last: bool
    shuffled: bool
    perm: torch.Tensor | None
    substreams: dict

    @property
    def T(self) -> int:
        return int(self.a.shape[0])


def _geom_k(gen) -> tuple[int, bool]:
    """k = K_MIN + Geom0(p): support-{0,1,...} geometric (Ruling 1) — P(k = K_MIN) = p,
    constant hazard above the floor, E[k] = K_MIN + (1-p)/p."""
    u = torch.rand((), generator=gen).item()
    g = int(math.floor(math.log(max(1e-12, 1.0 - u)) / math.log(1.0 - P_GEOM)))
    k_raw = K_MIN + g
    return min(k_raw, K_MAX), k_raw > K_MAX


def _reflect(x: torch.Tensor, bound: float) -> torch.Tensor:
    """Reflect into [-bound, bound] (bounded steps -> at most a couple of folds)."""
    for _ in range(4):
        over = x.abs() > bound
        if not bool(over.any()):
            break
        x = torch.where(x > bound, 2 * bound - x, x)
        x = torch.where(x < -bound, -2 * bound - x, x)
    return x.clamp(-bound, bound)


def build_fabric(stim: EXP12Stimulus, cfg, seed: int, T: int, *,
                 probe_rate: float = 0.0, shuffled: bool = False,
                 uniform_mask: bool = False, word_ref: bool = False) -> Fabric:
    """uniform_mask (the SPLITTING ARM, prereg §14): the mask POLICY at position-1 waves
    becomes the same 50:50 coin as mid-dwell — the scheduling structure is removed and
    NOTHING else. Draw parity is free: both per-dwell coins are always drawn; the uniform
    arm USES the onset coin instead of ignoring it, so stimulus streams and mid-dwell
    masks are bit-identical to the scheduled fabric at the same seed. Scoring flag:
    is_exam := (pos 1 AND coin drew word) — recency-free onset word-masks that arrive by
    coin. Probe machinery is N/A (no schedule to anticipate); probe_rate must be 0.

    word_ref (the 12b mask policy (iii), prereg §15): uniform-coin layout with the SAME
    draws, REINTERPRETED by the loop — a word-coin wave becomes EXPOSURE-ONLY (no cell
    masked; the loss skips), a vision-coin wave stays a vision-mask teaching wave. NO
    word-masks anywhere: the word is a reference, never a target. is_exam ≡ False (no
    exams exist); mask_slot keeps the raw coin (0 = vision-mask, 1 = exposure-only)."""
    fam = dict(coeff_std=stim.coeff_std, k_axes=K_AXES)
    sig = fam["coeff_std"]
    bound = FAMILY_BOUND_SIG * sig
    s_step = sigma_step(sig)
    keys = dict(dwell=SEED_DWELL + seed, member=SEED_MEMBER + seed,
                nuis=SEED_NUIS + seed, bg_const=SEED_BG_CONST,
                bg_jit=SEED_BG_JIT + seed, mask=SEED_MASK + seed,
                noise=SEED_NOISE + seed, shuffle=SEED_SHUFFLE + seed,
                probe_raw=SEED_PROBE_RAW + seed)
    g_dwell = torch.Generator().manual_seed(keys["dwell"])
    g_member = torch.Generator().manual_seed(keys["member"])
    g_nuis = torch.Generator().manual_seed(keys["nuis"])
    g_bgj = torch.Generator().manual_seed(keys["bg_jit"])
    g_mask = torch.Generator().manual_seed(keys["mask"])
    g_noise = torch.Generator().manual_seed(keys["noise"])

    n_members = cfg.n_A * cfg.n_B
    rows = dict(member=[], dwell_id=[], pos=[], mask_slot=[], is_exam=[],
                is_probe=[], nuis=[])
    dwell_member, dwell_k = [], []
    cap_hits = 0
    prev_m = -1
    did = 0
    while len(rows["member"]) < T:
        k, cap = _geom_k(g_dwell)
        cap_hits += int(cap)
        # uniform, no immediate same-member repeat
        if prev_m < 0:
            m = int(torch.randint(0, n_members, (1,), generator=g_member))
        else:
            r = int(torch.randint(0, n_members - 1, (1,), generator=g_member))
            m = r + (1 if r >= prev_m else 0)
        prev_m = m
        dwell_member.append(m)
        dwell_k.append(k)
        # §13.10: BOTH per-dwell coins (suppression + onset slot) are drawn for EVERY
        # dwell so per-dwell g_mask consumption is constant — a stage-two rate change
        # flips only which dwells are suppressed (nested sets), never the downstream
        # draw alignment. (Review catch 2026-07-05: the onset coin was conditional,
        # which shifted every later draw on a rate change.)
        probe_dwell = bool(torch.rand((), generator=g_mask).item() < probe_rate)
        onset_coin = int(torch.rand((), generator=g_mask).item() < 0.5)
        # onset pose from the family marginal, clamped to the family bounds
        c = (sig * torch.randn(K_AXES, generator=g_nuis)).clamp(-bound, bound)
        c0 = c.clone()
        for p in range(1, k + 1):
            if p > 1:
                c = _reflect(c + THETA * (c0 - c)
                             + s_step * torch.randn(K_AXES, generator=g_nuis), bound)
            if p == 1:
                if word_ref:
                    slot, exam, probe = onset_coin, False, False   # no exams exist (§15)
                elif uniform_mask:
                    slot, exam, probe = onset_coin, onset_coin == 1, False
                elif probe_dwell:
                    slot, exam, probe = onset_coin, False, True
                else:
                    slot, exam, probe = 1, True, False   # the guaranteed onset exam
            else:
                slot = int(torch.rand((), generator=g_mask).item() < 0.5)
                exam, probe = False, False
            rows["member"].append(m)
            rows["dwell_id"].append(did)
            rows["pos"].append(p)
            rows["mask_slot"].append(slot)
            rows["is_exam"].append(exam)
            rows["is_probe"].append(probe)
            rows["nuis"].append(c.clone())
        did += 1
    truncated = len(rows["member"]) > T

    member = torch.tensor(rows["member"][:T])
    a, b = member // cfg.n_B, member % cfg.n_B
    nuis = torch.stack(rows["nuis"][:T])
    # background: continuous OU around the fixed constant, whole stream, per-seed jitter
    bg = torch.empty(T, BG_AXES)
    bcur = stim.bg_const.clone()
    for t in range(T):
        if t > 0:
            bcur = _reflect(bcur + THETA * (stim.bg_const - bcur)
                            + s_step * torch.randn(BG_AXES, generator=g_bgj), bound)
        bg[t] = bcur
    noise = cfg.sigma_stim * torch.randn(T, cfg.D, generator=g_noise)
    raw = (stim.centre_id[a, b] + noise
           + nuis @ stim.nuis_axes + bg @ stim.bg_axes)

    fab = Fabric(
        a=a, b=b, member=member, cat=b % cfg.n_category,
        dwell_id=torch.tensor(rows["dwell_id"][:T]),
        pos=torch.tensor(rows["pos"][:T]),
        mask_slot=torch.tensor(rows["mask_slot"][:T]),
        is_exam=torch.tensor(rows["is_exam"][:T], dtype=torch.bool),
        is_probe_exam=torch.tensor(rows["is_probe"][:T], dtype=torch.bool),
        nuis=nuis, bg=bg, raw=raw,
        dwell_member=torch.tensor(dwell_member), dwell_k=torch.tensor(dwell_k),
        cap_hits=cap_hits, truncated_last=truncated, shuffled=False, perm=None,
        substreams=keys)
    if shuffled:
        perm = torch.randperm(T, generator=torch.Generator().manual_seed(keys["shuffle"]))
        for f in ("a", "b", "member", "cat", "dwell_id", "pos", "mask_slot",
                  "is_exam", "is_probe_exam", "nuis", "bg", "raw"):
            setattr(fab, f, getattr(fab, f)[perm])
        fab.shuffled, fab.perm = True, perm
    return fab


# ------------------------------------------------------------------ asserts (§5 / §13.8)
def _labels_of(a: torch.Tensor, b: torch.Tensor, n_category: int) -> torch.Tensor:
    """The EXP10 label triple: coarse a / distractor / category."""
    return torch.stack([a.float(), (b // n_category).float(),
                        (b % n_category).float()], dim=1)


def _max_abs_corr(x, y):
    xc = (x - x.mean(0)) / (x.std(0) + 1e-12)
    yc = (y - y.mean(0)) / (y.std(0) + 1e-12)
    return float((xc.t() @ yc / len(x)).abs().max())


def _dwell_perm_labels(fab: Fabric, gen, n_category: int, upto: int) -> torch.Tensor:
    """The exchangeability null: permute the dwell->member ASSIGNMENT (dwell lengths and
    the nuisance/bg series stay put), rebuild the per-wave label triple.

    T-INDEPENDENT NULL (instrument-validity re-pin, Jason's ruling 2026-07-07): the
    permutation universe is the dwells WITHIN the sampled window `[:upto]` — the same fixed
    window on which `obs` is computed — NOT the full `len(fab.dwell_member)` array (which grows
    with the run length T). The old full-array form made randperm(N) T-dependent, so the null's
    99th-pct moved with horizon and the SAME observed correlation flipped PASS->FAIL at longer T
    (a leak guard whose bar moves with run length fails its own matched-bar principle). With the
    window-local permutation the null is byte-identical at every horizon (K, dwell_member[:K],
    dwell_id[:upto] and randperm(K,seed) are all prefix-stable). Recorded, not a threshold-skip:
    at a fixed horizon this is a MORE-matched exchangeability test (null universe == obs universe);
    EXP12/EXP13 are closed and are not re-run, so their committed results are unaffected."""
    K = int(fab.dwell_id[upto - 1]) + 1                      # dwells inside the sampled window
    perm = torch.randperm(K, generator=gen)                 # T-independent (window-local)
    pm = fab.dwell_member[:K][perm]
    m = pm[fab.dwell_id[:upto]]
    a, b = m // 4, m % 4
    return _labels_of(a, b, n_category)


def fabric_asserts(fab: Fabric, cfg, *, n_sample: int = 12000, n_null: int = 200,
                   lag_stride: int = 1) -> dict:
    """HARD manifest-time asserts. Runs on the UNSHUFFLED wave order (pass the A-DWELL
    fabric; A-SHUFFLE is the same waves by construction, asserted via checksum)."""
    assert not fab.shuffled, "asserts run on the unshuffled fabric (same waves by construction)"
    S = min(fab.T, n_sample)
    labels = _labels_of(fab.a[:S], fab.b[:S], cfg.n_category)
    out = dict(n_sample=S, n_null=n_null)

    # cap-hit ceiling (§2 pin 2): the pin governs the LAW's rate (breach = re-pin k_max)
    # — asserted EXACTLY on the design — plus a realized-count binomial-consistency
    # guard (z=4 upper bound) that catches construction bugs without firing on the
    # small-sample noise of a short fabric.
    n_dwell = len(fab.dwell_k)
    cap_rate = fab.cap_hits / max(1, n_dwell)
    p_theory = (1.0 - P_GEOM) ** (K_MAX - K_MIN + 1)          # P(Geom0 > K_MAX - K_MIN)
    cap_bound = n_dwell * p_theory + 4.0 * math.sqrt(n_dwell * p_theory * (1 - p_theory)) + 1
    out["cap_hit"] = dict(rate=round(cap_rate, 5), rate_theory=round(p_theory, 5),
                          ceiling=CAP_CEILING, n_dwells=n_dwell, count=fab.cap_hits,
                          count_bound=round(cap_bound, 1),
                          ok=bool(p_theory < CAP_CEILING and fab.cap_hits <= cap_bound))
    assert p_theory < CAP_CEILING, \
        f"CAP-HIT CEILING BREACH (design): {p_theory:.4f} >= {CAP_CEILING} — re-pin k_max, surfaced"
    assert fab.cap_hits <= cap_bound, \
        f"CAP-HIT REALIZED INCONSISTENT WITH LAW: {fab.cap_hits} > bound {cap_bound:.1f}"
    rep = int((fab.dwell_member[1:] == fab.dwell_member[:-1]).sum())
    out["immediate_repeats"] = rep
    assert rep == 0, "immediate same-member repeat"
    # realized stationary fraction (the derived-sigma sanity, logged):
    # deviation from onset pose, reconstructed via per-dwell onset
    onset_by_dwell = {}
    for t in range(min(fab.T, S)):
        d = int(fab.dwell_id[t])
        if d not in onset_by_dwell:
            onset_by_dwell[d] = fab.nuis[t]
    devs = torch.stack([fab.nuis[t] - onset_by_dwell[int(fab.dwell_id[t])]
                        for t in range(min(fab.T, S)) if int(fab.pos[t]) > 1])
    fam_sig = float(torch.std(torch.stack(list(onset_by_dwell.values()))))
    out["walk_realized"] = dict(deviation_sd=round(float(devs.std()), 4),
                                onset_sd=round(fam_sig, 4),
                                target_frac=STATIONARY_FRAC,
                                realized_frac=round(float(devs.std()) / max(1e-9, fam_sig), 4))

    # (1) per-lag nuisance ⟂ member over lags <= K_MAX (multiplicity-controlled max)
    lags = list(range(0, K_MAX + 1, lag_stride))
    def max_over_lags(lab):
        best = 0.0
        for L in lags:
            n = S - L
            best = max(best, _max_abs_corr(fab.nuis[:n], lab[L:L + n]))
        return best
    obs = max_over_lags(labels)
    null = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(61000 + i)
        null.append(max_over_lags(_dwell_perm_labels(fab, gp, cfg.n_category, S)))
    thr = sorted(null)[int(0.99 * n_null)]
    out["perlag_nuis"] = dict(obs=round(obs, 4), null99=round(thr, 4),
                              lags=f"0..{K_MAX} stride {lag_stride}", ok=bool(obs <= thr))
    assert obs <= thr, f"PER-LAG NUISANCE LEAK: {obs} > {thr}"

    # (2) k ⟂ member: chi-square statistic vs permutation null (epsilon form inherited:
    # the null IS the calibrator; scipy-free). Bins: {2}, {3-4}, {5-8}, {9-16}, {17-48}.
    kb = ((fab.dwell_k >= 3).long() + (fab.dwell_k >= 5).long()
          + (fab.dwell_k >= 9).long() + (fab.dwell_k >= 17).long())
    bins = torch.tensor([2, 3, 5, 9, 17, K_MAX + 1])          # recorded bin edges
    def chi2(mem, kbin):
        tab = torch.zeros(16, len(bins) - 1)
        for m_, k_ in zip(mem.tolist(), kbin.tolist()):
            tab[m_, k_] += 1
        exp = tab.sum(1, keepdim=True) @ tab.sum(0, keepdim=True) / tab.sum()
        sel = exp > 0
        return float(((tab - exp).pow(2)[sel] / exp[sel]).sum())
    obs_k = chi2(fab.dwell_member, kb)
    null_k = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(62000 + i)
        null_k.append(chi2(fab.dwell_member[torch.randperm(n_dwell, generator=gp)], kb))
    thr_k = sorted(null_k)[int(0.99 * n_null)]
    out["k_indep"] = dict(chi2=round(obs_k, 2), null99=round(thr_k, 2), ok=bool(obs_k <= thr_k))
    assert obs_k <= thr_k, f"k CODES IDENTITY: chi2 {obs_k} > {thr_k}"

    # (3) mid-dwell schedule ⟂ member (the exam is structural at position 1: recorded)
    mid = fab.pos[:S] > 1
    mm, ms = fab.member[:S][mid], fab.mask_slot[:S][mid]
    def chi2m(mem, slot):
        tab = torch.zeros(16, 2)
        for m_, s_ in zip(mem.tolist(), slot.tolist()):
            tab[m_, s_] += 1
        exp = tab.sum(1, keepdim=True) @ tab.sum(0, keepdim=True) / tab.sum()
        sel = exp > 0
        return float(((tab - exp).pow(2)[sel] / exp[sel]).sum())
    obs_s = chi2m(mm, ms)
    null_s = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(63000 + i)
        null_s.append(chi2m(mm, ms[torch.randperm(len(ms), generator=gp)]))
    thr_s = sorted(null_s)[int(0.99 * n_null)]
    out["schedule_indep"] = dict(chi2=round(obs_s, 2), null99=round(thr_s, 2),
                                 note="exam@pos1 structural by construction (recorded, not tested)",
                                 ok=bool(obs_s <= thr_s))
    assert obs_s <= thr_s, f"SCHEDULE CODES IDENTITY: chi2 {obs_s} > {thr_s}"

    # (4) background ⟂ member (lag-0; same exchangeability null)
    obs_b = _max_abs_corr(fab.bg[:S], labels)
    null_b = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(64000 + i)
        null_b.append(_max_abs_corr(fab.bg[:S], _dwell_perm_labels(fab, gp, cfg.n_category, S)))
    thr_b = sorted(null_b)[int(0.99 * n_null)]
    out["bg_indep"] = dict(obs=round(obs_b, 4), null99=round(thr_b, 4), ok=bool(obs_b <= thr_b))
    assert obs_b <= thr_b, f"BACKGROUND LEAK: {obs_b} > {thr_b}"
    return out


def fabric_manifest(fab: Fabric, stim: EXP12Stimulus, cfg, asserts: dict) -> dict:
    mid = fab.pos > 1
    return dict(
        fabric=dict(
            T=fab.T, dwell_law=f"k = {K_MIN} + Geom0({P_GEOM}), cap {K_MAX} (Ruling 1)",
            e_k_target=K_MIN + (1.0 - P_GEOM) / P_GEOM,
            k_min_realized_frac_target=P_GEOM,
            k_min_realized_frac=round(float((fab.dwell_k == K_MIN).float().mean()), 4),
            realized_mean_k=round(float(fab.dwell_k.float().mean()), 3),
            n_dwells=len(fab.dwell_k), cap_hits=fab.cap_hits,
            truncated_last_dwell=fab.truncated_last,
            walk=dict(tau=TAU, theta=THETA, stationary_frac=STATIONARY_FRAC,
                      family_coeff_std=stim.coeff_std,
                      sigma_step_derived=round(sigma_step(stim.coeff_std), 5),
                      reflect_bound=FAMILY_BOUND_SIG * stim.coeff_std,
                      k_axes=K_AXES, bg_axes=BG_AXES),
            background_const=[round(float(x), 6) for x in stim.bg_const],
            member_hist=torch.bincount(fab.dwell_member, minlength=16).tolist(),
            mask_mix=dict(exam=int(fab.is_exam.sum()),
                          probe_exam=int(fab.is_probe_exam.sum()),
                          mid_vis=int(((~fab.is_exam) & mid & (fab.mask_slot == 0)).sum()),
                          mid_word=int(((~fab.is_exam) & mid & (fab.mask_slot == 1)).sum())),
            shuffled=fab.shuffled,
            substream_keys=fab.substreams),
        independence_asserts=asserts,
    )
