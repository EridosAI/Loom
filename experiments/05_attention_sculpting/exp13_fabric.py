"""EXP13 — lawful-dynamics fabric (harness-side world data; prereg §1, §9.1/.2/.6).

EXP13 = the EXP12 scene-persistence fabric with ONE change to the world's physics: the
nuisance anchor MOVES under a per-dwell LAW (Fork 1B, ratified). Everything else — the
member draw, the dwell law, the fixed background, the mask schedule, the substreams, the
independence machinery — is EXP12 VERBATIM (imported, never re-implemented; "one code
path"). The mask schedule is untouched: EXP13's W=3 interior-mask lives entirely in the
LOOP (exp13_arms.py), not the fabric — the fabric still assigns one masked slot per wave.

The law (Fork 1B, §9.1 ratified):
  * Per dwell, at onset: draw an onset pose c0 ~ family marginal (EXP12) AND a per-axis
    VELOCITY v from a dedicated law-params substream (SEED_LAW): |v| ~ U[VMIN, VMAX]·σ_f,
    independent random sign per axis. Velocity ⟂ member by construction (its own stream,
    drawn on the dwell counter, never keyed on identity) — asserted.
  * The LAW position drifts at constant velocity: mu_p = mu_{p-1} + v, with ELASTIC
    reflection at the family bounds ±3σ_f (the drift bounces; speed preserved, sign flips
    per axis on a fold). mu_1 = c0.
  * An OU RESIDUAL rides the law: dev_1 = 0; dev_p = (1-θ)·dev_{p-1} + σ_step·noise
    (reverting to 0 — i.e. to the MOVING law), reflected into its own ±3·(0.25σ_f)
    support. Same τ=4 / stationary-0.25σ_f pin as EXP12, now the residual-ABOUT-LAW
    spread. The PRESENTED nuisance is c_p = mu_p + dev_p.
  * Residual-about-law = c_p − mu_p = dev_p (clean; the OU residual, bounded). The per-lag
    ⟂ member machinery runs on THIS, not on the drift-laden c_p (§9 verify item).
  * sideways-beats-forward BY CONSTRUCTION: two-sided interpolation of the interior wave
    reads mu from both flanks; forward extrapolation must also pay the OU residual it
    cannot see. Internalizing the law is paid through completion geometry, never forecast.

Mechanical choices SURFACED (not silent; recorded in the manifest, reported at the pause):
  * SEED_LAW = 90000 — a NEW dedicated substream, disjoint from all EXP12 keys
    (91000..99000); law-params never share a stream with member/nuisance/bg/mask.
  * Velocity magnitude U[0.05, 0.2]·σ_f per axis (§9.1); sign ±1 each axis (fair coin on
    the same law stream). Drawn ONCE per dwell (at onset), constant within the dwell.
  * Residual reflected at ±3·(0.25σ_f) (its stationary ±3σ support) — the dev analog of
    EXP12's total-coeff reflection; keeps residual-about-law bounded and member-clean.
  * The background is UNCHANGED (pin-to-constant + OU jitter, no drift — the standing
    world; §1 "carries: fixed background").
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

import exp12_fabric as F12                                      # noqa: E402  one code path

OUTDIR = F12.OUTDIR

# --- carried EXP12 constants (imported, never re-typed) ---
P_GEOM, K_MIN, K_MAX = F12.P_GEOM, F12.K_MIN, F12.K_MAX
CAP_CEILING = F12.CAP_CEILING
TAU, THETA, STATIONARY_FRAC = F12.TAU, F12.THETA, F12.STATIONARY_FRAC
FAMILY_BOUND_SIG = F12.FAMILY_BOUND_SIG
K_AXES, BG_AXES = F12.K_AXES, F12.BG_AXES

# --- §9.1 the law (velocity family) ---
SEED_LAW = 90000                 # NEW dedicated law-params substream (disjoint from EXP12)
V_MIN, V_MAX = 0.05, 0.20        # |velocity| ~ U[V_MIN, V_MAX] * family sigma, per axis/wave
# --- §9.6 dose pin ---
LAWFUL_WINDOW_FLOOR = 0.75       # manifest assert; ~0.818 = 1 - 2/E[k] expected at W=3
W_WINDOW = 3                     # the completer window (the fabric records tags for it)

# EXP12 stimulus is reused verbatim (identity axes + nuisance axes + bg axes + bg const).
EXP13Stimulus = F12.EXP12Stimulus


def _bounce(x: torch.Tensor, v: torch.Tensor, bound: float):
    """Elastic reflection of a constant-velocity point at ±bound: fold position, flip the
    corresponding velocity component's sign (a couple of folds suffice for bounded steps)."""
    for _ in range(4):
        hi, lo = x > bound, x < -bound
        if not bool(hi.any() or lo.any()):
            break
        x = torch.where(hi, 2 * bound - x, x)
        v = torch.where(hi, -v, v)
        x = torch.where(lo, -2 * bound - x, x)
        v = torch.where(lo, -v, v)
    return x.clamp(-bound, bound), v


@dataclass
class Fabric13(F12.Fabric):
    law_mu: torch.Tensor | None = None       # (T, K) the LAW position (drift), per wave
    dwell_velocity: torch.Tensor | None = None   # (n_dwell, K) per-dwell velocity (⟂ member)


def build_fabric13(stim, cfg, seed: int, T: int, *,
                   probe_rate: float = 0.0, shuffled: bool = False,
                   uniform_mask: bool = False, word_ref: bool = False,
                   expo_word: bool = False) -> Fabric13:
    """EXP12 build_fabric with the lawful-drift nuisance (Fork 1B). The dwell law, member
    draw, mask schedule, background, noise and substream keys are EXP12 VERBATIM; only the
    nuisance trajectory changes (fixed onset-revert OU -> drifting law + OU residual) and a
    new law-params stream + per-wave law_mu / per-dwell velocity records are added."""
    sig = stim.coeff_std
    bound = FAMILY_BOUND_SIG * sig
    dev_bound = FAMILY_BOUND_SIG * STATIONARY_FRAC * sig       # residual's own ±3σ support
    s_step = F12.sigma_step(sig)
    keys = dict(dwell=F12.SEED_DWELL + seed, member=F12.SEED_MEMBER + seed,
                nuis=F12.SEED_NUIS + seed, bg_const=F12.SEED_BG_CONST,
                bg_jit=F12.SEED_BG_JIT + seed, mask=F12.SEED_MASK + seed,
                noise=F12.SEED_NOISE + seed, shuffle=F12.SEED_SHUFFLE + seed,
                probe_raw=F12.SEED_PROBE_RAW + seed, law=SEED_LAW + seed)
    g_dwell = torch.Generator().manual_seed(keys["dwell"])
    g_member = torch.Generator().manual_seed(keys["member"])
    g_nuis = torch.Generator().manual_seed(keys["nuis"])       # OU residual noise
    g_bgj = torch.Generator().manual_seed(keys["bg_jit"])
    g_mask = torch.Generator().manual_seed(keys["mask"])
    g_noise = torch.Generator().manual_seed(keys["noise"])
    g_law = torch.Generator().manual_seed(keys["law"])         # velocity draws

    n_members = cfg.n_A * cfg.n_B
    rows = dict(member=[], dwell_id=[], pos=[], mask_slot=[], is_exam=[],
                is_probe=[], nuis=[], law_mu=[])
    dwell_member, dwell_k, dwell_velocity = [], [], []
    cap_hits = 0
    prev_m = -1
    did = 0
    while len(rows["member"]) < T:
        k, cap = F12._geom_k(g_dwell)
        cap_hits += int(cap)
        if prev_m < 0:
            m = int(torch.randint(0, n_members, (1,), generator=g_member))
        else:
            r = int(torch.randint(0, n_members - 1, (1,), generator=g_member))
            m = r + (1 if r >= prev_m else 0)
        prev_m = m
        dwell_member.append(m)
        dwell_k.append(k)
        # §13.10 mask coins (EXP12 verbatim: BOTH drawn every dwell, draw parity)
        probe_dwell = bool(torch.rand((), generator=g_mask).item() < probe_rate)
        onset_coin = int(torch.rand((), generator=g_mask).item() < 0.5)
        # --- the law (§9.1): onset pose + per-axis velocity, this dwell ---
        c0 = (sig * torch.randn(K_AXES, generator=g_nuis)).clamp(-bound, bound)
        vmag = (V_MIN + (V_MAX - V_MIN) * torch.rand(K_AXES, generator=g_law)) * sig
        vsign = torch.where(torch.rand(K_AXES, generator=g_law) < 0.5,
                            torch.tensor(1.0), torch.tensor(-1.0))
        v = vmag * vsign
        dwell_velocity.append(v.clone())
        mu = c0.clone()
        vel = v.clone()
        dev = torch.zeros(K_AXES)
        for p in range(1, k + 1):
            if p > 1:
                mu, vel = _bounce(mu + vel, vel, bound)        # drift, elastic reflect
                dev = F12._reflect(dev + THETA * (0.0 - dev)
                                   + s_step * torch.randn(K_AXES, generator=g_nuis),
                                   dev_bound)                  # OU residual about the law
            c = mu + dev                                       # presented nuisance
            if p == 1:
                if word_ref:
                    slot, exam, probe = onset_coin, False, False
                elif uniform_mask:
                    slot, exam, probe = onset_coin, onset_coin == 1, False
                elif probe_dwell:
                    slot, exam, probe = onset_coin, False, True
                else:
                    slot, exam, probe = 1, True, False         # guaranteed onset exam
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
            rows["law_mu"].append(mu.clone())
        did += 1
    truncated = len(rows["member"]) > T

    member = torch.tensor(rows["member"][:T])
    a, b = member // cfg.n_B, member % cfg.n_B
    nuis = torch.stack(rows["nuis"][:T])
    law_mu = torch.stack(rows["law_mu"][:T])
    # background: EXP12 verbatim (pin-to-constant + OU jitter, no drift)
    bg = torch.empty(T, BG_AXES)
    bcur = stim.bg_const.clone()
    for t in range(T):
        if t > 0:
            bcur = F12._reflect(bcur + THETA * (stim.bg_const - bcur)
                                + s_step * torch.randn(BG_AXES, generator=g_bgj), bound)
        bg[t] = bcur
    noise = cfg.sigma_stim * torch.randn(T, cfg.D, generator=g_noise)
    raw = (stim.centre_id[a, b] + noise
           + nuis @ stim.nuis_axes + bg @ stim.bg_axes)

    fab = Fabric13(
        a=a, b=b, member=member, cat=b % cfg.n_category,
        dwell_id=torch.tensor(rows["dwell_id"][:T]),
        pos=torch.tensor(rows["pos"][:T]),
        mask_slot=torch.tensor(rows["mask_slot"][:T]),
        is_exam=torch.tensor(rows["is_exam"][:T], dtype=torch.bool),
        is_probe_exam=torch.tensor(rows["is_probe"][:T], dtype=torch.bool),
        nuis=nuis, bg=bg, raw=raw,
        dwell_member=torch.tensor(dwell_member), dwell_k=torch.tensor(dwell_k),
        cap_hits=cap_hits, truncated_last=truncated, shuffled=False, perm=None,
        substreams=keys,
        law_mu=law_mu, dwell_velocity=torch.stack(dwell_velocity))
    if shuffled:
        perm = torch.randperm(T, generator=torch.Generator().manual_seed(keys["shuffle"]))
        for f in ("a", "b", "member", "cat", "dwell_id", "pos", "mask_slot",
                  "is_exam", "is_probe_exam", "nuis", "bg", "raw", "law_mu"):
            setattr(fab, f, getattr(fab, f)[perm])
        fab.shuffled, fab.perm = True, perm
    return fab


# ------------------------------------------------------------------ window tagging (§2/§3)
def lawful_window_mask(fab: Fabric13) -> torch.Tensor:
    """A W=3 stride-1 window is centred on each interior wave t (window [t-1, t, t+1]).
    LAWFUL := all three waves share a dwell (the drift is continuous across the window, so
    two-sided completion of the interior can read the law). BOUNDARY := crosses a dwell
    edge (t is a dwell onset or a dwell's last wave). Interior waves are t = 1..T-2; the
    two stream-end waves have no full window (tagged False). Runs on the UNSHUFFLED order
    (dwell contiguity is a wave-order property); pass the A-LAWFUL fabric."""
    assert not fab.shuffled, "window tags run on the unshuffled (lawful) wave order"
    d = fab.dwell_id
    T = fab.T
    lawful = torch.zeros(T, dtype=torch.bool)
    same = (d[1:-1] == d[:-2]) & (d[1:-1] == d[2:])            # interior t in [1, T-2]
    lawful[1:-1] = same
    return lawful


def lawful_window_fraction(fab: Fabric13) -> dict:
    """Fraction of interior windows (t=1..T-2) that are lawful. Theory at E[k]=11, W=3:
    a dwell of length k yields (k-2) lawful interior waves -> frac = 1 - 2/E[k] ~ 0.818."""
    lawful = lawful_window_mask(fab)
    n_interior = fab.T - 2
    n_lawful = int(lawful[1:-1].sum())
    frac = n_lawful / max(1, n_interior)
    e_k = K_MIN + (1.0 - P_GEOM) / P_GEOM
    return dict(fraction=round(frac, 4), n_lawful=n_lawful, n_interior=n_interior,
                theory=round(1.0 - 2.0 / e_k, 4), floor=LAWFUL_WINDOW_FLOOR,
                ok=bool(frac >= LAWFUL_WINDOW_FLOOR))


# ------------------------------------------------------------------ asserts (§5/§13.8 + §9)
def fabric_asserts13(fab: Fabric13, cfg, *, n_sample: int = 12000, n_null: int = 200,
                     lag_stride: int = 1) -> dict:
    """The EXP12 independence asserts with TWO EXP13 changes (§9 verify items):
      (a) the per-lag ⟂ member assert runs on RESIDUALS-ABOUT-LAW (nuis - law_mu), not on
          the drift-laden presented nuisance — the drift is member-independent structure,
          so testing residuals is the correct member-leak test;
      (b) a NEW law-params ⟂ member assert (per-dwell velocity vs member; chi-square vs
          the dwell-permutation null, the k ⟂ member form).
    Plus the lawful-window fraction dose assert (§9.6). Runs on the UNSHUFFLED order."""
    assert not fab.shuffled, "asserts run on the unshuffled fabric (same waves by construction)"
    S = min(fab.T, n_sample)
    labels = F12._labels_of(fab.a[:S], fab.b[:S], cfg.n_category)
    residual = fab.nuis - fab.law_mu                           # residual-about-law (§9)
    out = dict(n_sample=S, n_null=n_null)

    # cap-hit + immediate-repeat (EXP12 verbatim)
    n_dwell = len(fab.dwell_k)
    cap_rate = fab.cap_hits / max(1, n_dwell)
    p_theory = (1.0 - P_GEOM) ** (K_MAX - K_MIN + 1)
    cap_bound = n_dwell * p_theory + 4.0 * math.sqrt(n_dwell * p_theory * (1 - p_theory)) + 1
    out["cap_hit"] = dict(rate=round(cap_rate, 5), rate_theory=round(p_theory, 5),
                          ceiling=CAP_CEILING, n_dwells=n_dwell, count=fab.cap_hits,
                          count_bound=round(cap_bound, 1),
                          ok=bool(p_theory < CAP_CEILING and fab.cap_hits <= cap_bound))
    assert p_theory < CAP_CEILING, f"CAP-HIT CEILING (design): {p_theory:.4f} >= {CAP_CEILING}"
    assert fab.cap_hits <= cap_bound, f"CAP-HIT REALIZED: {fab.cap_hits} > {cap_bound:.1f}"
    rep = int((fab.dwell_member[1:] == fab.dwell_member[:-1]).sum())
    out["immediate_repeats"] = rep
    assert rep == 0, "immediate same-member repeat"

    # realized law + residual scales (the derived-sigma + drift sanity, logged)
    onset_by_dwell = {}
    for t in range(min(fab.T, S)):
        dd = int(fab.dwell_id[t])
        if dd not in onset_by_dwell:
            onset_by_dwell[dd] = fab.nuis[t]
    resid_dev = residual[:S][fab.pos[:S] > 1]
    fam_sig = float(torch.std(torch.stack(list(onset_by_dwell.values()))))
    vel = fab.dwell_velocity
    out["law_realized"] = dict(
        residual_sd=round(float(resid_dev.std()), 4), onset_sd=round(fam_sig, 4),
        target_resid_frac=STATIONARY_FRAC,
        realized_resid_frac=round(float(resid_dev.std()) / max(1e-9, fam_sig), 4),
        velocity_abs_mean=round(float(vel.abs().mean()), 4),
        velocity_frac_of_sigma=round(float(vel.abs().mean()) / max(1e-9, fam_sig), 4),
        v_range_target=[V_MIN, V_MAX])

    # (1) per-lag RESIDUAL-ABOUT-LAW ⟂ member (the §9 change: residual, not raw nuis)
    lags = list(range(0, K_MAX + 1, lag_stride))
    def max_over_lags(lab):
        best = 0.0
        for L in lags:
            n = S - L
            best = max(best, F12._max_abs_corr(residual[:n], lab[L:L + n]))
        return best
    obs = max_over_lags(labels)
    null = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(61000 + i)
        null.append(max_over_lags(F12._dwell_perm_labels(fab, gp, cfg.n_category, S)))
    thr = sorted(null)[int(0.99 * n_null)]
    out["perlag_residual"] = dict(obs=round(obs, 4), null99=round(thr, 4),
                                  on="residual-about-law (nuis - law_mu)",
                                  lags=f"0..{K_MAX} stride {lag_stride}", ok=bool(obs <= thr))
    assert obs <= thr, f"PER-LAG RESIDUAL LEAK: {obs} > {thr}"

    # (2) k ⟂ member (EXP12 verbatim)
    kb = ((fab.dwell_k >= 3).long() + (fab.dwell_k >= 5).long()
          + (fab.dwell_k >= 9).long() + (fab.dwell_k >= 17).long())
    def chi2_bin(mem, code, ncode):
        tab = torch.zeros(16, ncode)
        for m_, c_ in zip(mem.tolist(), code.tolist()):
            tab[m_, c_] += 1
        exp = tab.sum(1, keepdim=True) @ tab.sum(0, keepdim=True) / tab.sum()
        sel = exp > 0
        return float(((tab - exp).pow(2)[sel] / exp[sel]).sum())
    obs_k = chi2_bin(fab.dwell_member, kb, 5)
    null_k = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(62000 + i)
        null_k.append(chi2_bin(fab.dwell_member[torch.randperm(n_dwell, generator=gp)], kb, 5))
    thr_k = sorted(null_k)[int(0.99 * n_null)]
    out["k_indep"] = dict(chi2=round(obs_k, 2), null99=round(thr_k, 2), ok=bool(obs_k <= thr_k))
    assert obs_k <= thr_k, f"k CODES IDENTITY: chi2 {obs_k} > {thr_k}"

    # (2b) NEW — law-params (velocity) ⟂ member: bin the velocity ANGLE/MAGNITUDE per axis.
    # Reduce the per-dwell velocity vector to a coarse code (sign pattern over K axes ->
    # 2^K bins) and chi-square vs the dwell-permutation null — velocity must not whisper
    # identity (same coin, elephants and mice, now in motion).
    vsign_code = torch.zeros(n_dwell, dtype=torch.long)
    for j in range(K_AXES):
        vsign_code += (vel[:, j] > 0).long() * (2 ** j)
    obs_v = chi2_bin(fab.dwell_member, vsign_code, 2 ** K_AXES)
    null_v = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(65000 + i)
        null_v.append(chi2_bin(fab.dwell_member[torch.randperm(n_dwell, generator=gp)],
                               vsign_code, 2 ** K_AXES))
    thr_v = sorted(null_v)[int(0.99 * n_null)]
    out["law_params_indep"] = dict(chi2=round(obs_v, 2), null99=round(thr_v, 2),
                                   code="velocity sign-pattern over K axes",
                                   ok=bool(obs_v <= thr_v))
    assert obs_v <= thr_v, f"LAW-PARAMS CODE IDENTITY: chi2 {obs_v} > {thr_v}"

    # (3) mid-dwell schedule ⟂ member (EXP12 verbatim)
    mid = fab.pos[:S] > 1
    mm, ms = fab.member[:S][mid], fab.mask_slot[:S][mid]
    obs_s = chi2_bin(mm, ms, 2)
    null_s = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(63000 + i)
        null_s.append(chi2_bin(mm, ms[torch.randperm(len(ms), generator=gp)], 2))
    thr_s = sorted(null_s)[int(0.99 * n_null)]
    out["schedule_indep"] = dict(chi2=round(obs_s, 2), null99=round(thr_s, 2),
                                 note="exam@pos1 structural by construction (recorded, not tested)",
                                 ok=bool(obs_s <= thr_s))
    assert obs_s <= thr_s, f"SCHEDULE CODES IDENTITY: chi2 {obs_s} > {thr_s}"

    # (4) background ⟂ member (EXP12 verbatim)
    obs_b = F12._max_abs_corr(fab.bg[:S], labels)
    null_b = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(64000 + i)
        null_b.append(F12._max_abs_corr(fab.bg[:S], F12._dwell_perm_labels(fab, gp, cfg.n_category, S)))
    thr_b = sorted(null_b)[int(0.99 * n_null)]
    out["bg_indep"] = dict(obs=round(obs_b, 4), null99=round(thr_b, 4), ok=bool(obs_b <= thr_b))
    assert obs_b <= thr_b, f"BACKGROUND LEAK: {obs_b} > {thr_b}"

    # (5) §9.6 dose: lawful-window fraction >= floor
    lw = lawful_window_fraction(fab)
    out["lawful_window"] = lw
    assert lw["ok"], f"LAWFUL-WINDOW FLOOR BREACH: {lw['fraction']} < {LAWFUL_WINDOW_FLOOR} — raise E[k]"
    return out


def fabric_manifest13(fab: Fabric13, stim, cfg, asserts: dict) -> dict:
    man = F12.fabric_manifest(fab, stim, cfg, asserts)
    vel = fab.dwell_velocity
    man["fabric"]["law"] = dict(
        kind="lawful drift + OU residual (Fork 1B)",
        velocity_family=f"|v| ~ U[{V_MIN},{V_MAX}]*sigma_f per axis, random sign, per dwell",
        velocity_abs_mean=round(float(vel.abs().mean()), 5),
        drift_reflection="elastic (bounce) at +/-3 sigma_f",
        residual="OU about the moving law, tau=4, stationary 0.25 sigma_f, reflected +/-3*(0.25 sigma_f)",
        law_params_stream=SEED_LAW,
        w_window=W_WINDOW)
    man["fabric"]["lawful_window"] = asserts.get("lawful_window")
    return man
