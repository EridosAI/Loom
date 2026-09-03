"""exp07 (Phase 0) — Cue-Floor x Penalty-Surface: the [RECONCILE] register + grid.

EVERY tunable here is either (a) READ programmatically from the exp06 commit (SculptConfig — the
deployed conflict rig; anchor_gate.json / exp06_reconfirm.json — the reconfirmed cube), or (b) a
KNOB CHOICE the spec leaves to this phase (the reshaped clock-onset, the phasing onsets, the
re-posing alpha grid, the corner-probe cardinality, the plateau budget). The knob choices are
flagged KNOB and surfaced at the Step-0 review gate (standing rule: surface knob choices before
changing anything) — they are NOT silently pinned by feel.

Nothing here reads/interprets the interior surface; it only declares the grid and the bars.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))  # exp04 (constants)

import constants                                            # noqa: E402
from sculpt_config import SculptConfig                      # noqa: E402

# ----------------------------------------------------------------- read the exp06 commit
_CFG = SculptConfig()                                       # deployed Stage-1 conflict config (commit)
_STAGE0 = constants.Stage0Config()                          # deployed cortex clock (t1,t2,steps)


def _read_json(name: str) -> dict:
    p = _HERE / name
    return json.load(open(p)) if p.exists() else {}


_ANCHOR = _read_json("anchor_gate.json")                    # committed gate (335f36d/1a9e8ba)
_RECONFIRM = _read_json("exp06_reconfirm.json")             # committed reconfirm (43e03c0)


# ============================ [RECONCILE] — values READ from the exp06 commit ============
DEPLOYED_PAM_LAM = _CFG.pam_lam                             # 0.01  deployed PAM pool-penalty
M_DEPLOYED = _CFG.n_A * _CFG.n_B                            # 16    deployed completion cardinality
DIFFUSE_SHARED = (_CFG.R_coarse ** 2 + _CFG.r_distractor ** 2) ** 0.5  # 5.831 salient shared cue energy
DIFFUSE_CUE = _CFG.r_category                               # 0.5   subtle differentiating cue
DIFFUSE_SNR = DIFFUSE_CUE / DIFFUSE_SHARED                  # 0.0857 deployed flat-diffuse snr

# bars (calibrated + reconfirmed in exp06; read, never re-derived by feel)
HEALTHY = _ANCHOR.get("calibrated_bars", {}).get("healthy_value", 1.4122)   # clean-2 corner
LIVE_BAR = _ANCHOR.get("calibrated_bars", {}).get("live_bar", 0.8672)       # ~healthy-neighbourhood bar
COLLAPSE_CEILING = _ANCHOR.get("calibrated_bars", {}).get("collapse_ceiling", 0.05)
ABLATION_FLOOR = _ANCHOR.get("calibrated_bars", {}).get("ablation_floor", 0.10)
# off-sharp alive reference: exp06 [1,0,0] read at its 12000-step / 16-seed plateau (NOT the 4000 gate
# value 1.005 — the equal-training-comparison lesson from the reconfirm).
OFF_SHARP_REF = _RECONFIRM.get("deciding_at_bstar", {}).get("mean", 1.1064)

# deployed cortex capacity clock + tie strength (the reshaped tie = the settled cortex StepSchedule
# applied to PAM: same machinery as the cortices, the spec's preserve argument). Read from Stage0Config.
DEPLOYED_T1, DEPLOYED_T2 = _STAGE0.t1, _STAGE0.t2          # 300, 1200
DEPLOYED_STREAM_STEPS = _STAGE0.steps                      # 4000
RESHAPED_T1_FRACTION = DEPLOYED_T1 / DEPLOYED_STREAM_STEPS     # 300/4000  = 0.075 (group/coarse onset)
RESHAPED_CLOCK_FRACTION = DEPLOYED_T2 / DEPLOYED_STREAM_STEPS  # 1200/4000 = 0.30  (capacity/λ2 onset; the swept knob)
CORTEX_LAM_HI = _STAGE0.lam2_hi                            # 10.0  cortex pooling tie strength (hi)
CORTEX_LAM_LO = _STAGE0.lam2_lo                            # 0.0   open

# revival-variance / seeds (exp06 surface used 5; reconfirm used 16 only for the deciding cell)
SEEDS = [0, 1, 2, 3, 4]


# ============================ KNOB CHOICES (spec leaves to this phase; SURFACED for review) =====
# Each is the spec's recommended/principled default, recorded as a knob (not feel) for the gate.
KNOBS = {
    # plateau budget: exp06 reconfirm read live cells at their 12000-step plateau (bstar_effective).
    # every exp07 cell is read here at the SAME budget for the equal-training comparison.
    "plateau_budget": 12000,
    "plateau_checkpoints": [6000, 8000, 10000, 12000],   # spot-check d_diff flatness on ceiling cells
    # cue re-posing alpha grid: content-blind common-mode centering fraction (0=flat-diffuse,
    # 1=fully centered). Swept to a (d)-plateau (read stops when consecutive lift < seed-spread).
    "reposing_alphas": [0.0, 0.25, 0.5, 0.75, 0.9, 1.0],
    # reshaped = the cortex StepSchedule on PAM's tie (same machinery as the cortices). lam1 (groups)
    # opens at t1/steps; lam2 (capacity/members) opens at t2/steps = the swept clock-onset; tie
    # strength = cortex lam_hi (10) -> lam_lo (0). The ONE coarse knob = the λ2/capacity onset; t1 is
    # reconciled-fixed. (The naive single-clock pool_penalty(lam,lam) -- penalising delta1 too --
    # was REJECTED: it annihilates the group symmetry-breakers -> irreversible collapse trap; the
    # reshaped column would be DEAD on every cue regardless of phasing -> a manufactured wrong-reason
    # dead column. The cortex two-clock keeps groups as symmetry-breakers; reshaped-sharp REVIVES
    # at plateau (oracle test passes). See exp07 Step-0 surface for the trap evidence + B/C/D oracle test.)
    "reshaped_clock_fraction": round(RESHAPED_CLOCK_FRACTION, 4),   # λ2/capacity onset (swept knob)
    "reshaped_t1_fraction": round(RESHAPED_T1_FRACTION, 4),         # λ1/group onset (reconciled-fixed)
    "reshaped_t1_step_abs": int(round(RESHAPED_T1_FRACTION * 12000)),    # 900  (absolute, budget-indep)
    "reshaped_t2_step_abs": int(round(RESHAPED_CLOCK_FRACTION * 12000)),  # 3600 (absolute, budget-indep)
    "onset_is_absolute": True,   # pinned to fraction*12000; extending training does NOT move the onset
    "reshaped_lam_hi": CORTEX_LAM_HI, "reshaped_lam_lo": CORTEX_LAM_LO,
    # phasing sweep (reversal re-check only; spec §3 3-5 onsets early->late, bounded). Sweeps the
    # λ2/capacity onset; λ1 onset stays at reshaped_t1_fraction.
    "phasing_fractions": [0.1, 0.3, 0.5, 0.7, 0.9],
    # cardinality corner-probe point (spec §1 recommends 2-member, anchored to dgate clean-2 ~1.41,
    # max contrast vs 16). The full lower-cardinality surface is the pre-computed contingency.
    "corner_cardinality": 2,
    # plateau-on-cue-sweep margin: a re-posing step "lifts" iff it raises mean d_diff by more than
    # this; tied to exp06 within-cell seed-spread (~0.16 at the live off-sharp cell). KNOB.
    "cue_plateau_margin": 0.10,
    # decision margin above live_bar for "revives" headroom (mirrors exp06 reconfirm DECISION_MARGIN);
    # liveness itself is binary at live_bar + ablation — this is only a reporting headroom.
    "decision_margin": 0.10,
}

# convenience handles
PLATEAU_BUDGET = KNOBS["plateau_budget"]
# canonical budget the reshaped onsets are pinned to (ABSOLUTE; see PenaltySpec). Surface/phasing ran
# at exactly this budget, so fraction*budget == absolute onset there; extensions keep the onset fixed.
CANONICAL_BUDGET = KNOBS["plateau_budget"]   # 12000


def onset_step(fraction: float) -> int:
    """Absolute clock-onset step = fraction * canonical budget (pinned; budget-independent)."""
    return int(round(fraction * CANONICAL_BUDGET))


REPOSING_ALPHAS = KNOBS["reposing_alphas"]
PHASING_FRACTIONS = KNOBS["phasing_fractions"]
CORNER_CARDINALITY = KNOBS["corner_cardinality"]
CUE_PLATEAU_MARGIN = KNOBS["cue_plateau_margin"]

# ---- penalty axis (3 qualitatively distinct regimes) ----
# Each regime drives PAM's pool penalty  lam1*||delta1||^2 + lam2*||delta2||^2  during training.
# lam1 (delta1 = groups/coarse) and lam2 (delta2 = members/fine = the "λ2 tie") each follow a step
# schedule: lamX = lamX_hi before tXf*budget, lamX_lo after.
#   off      — no tie (fixed full resolution).
#   deployed — exp06 deployed: lam1=lam2=0.01 CONSTANT (the collapsing tie; the broken status quo).
#   reshaped — the settled cortex StepSchedule on PAM (preserve = same machinery as the cortices):
#              groups open at t1f, capacity/λ2 opens at t2f (the swept clock-onset), tie strength
#              hi=10 -> lo=0. Opens on a clock, stays open; groups survive as symmetry-breakers.
RESHAPED_T1_STEP = int(round(RESHAPED_T1_FRACTION * PLATEAU_BUDGET))      # 900  (groups onset, abs)
RESHAPED_T2_STEP = int(round(RESHAPED_CLOCK_FRACTION * PLATEAU_BUDGET))   # 3600 (λ2/capacity onset, abs)
PENALTY_REGIMES = {
    "off":      dict(lam1_hi=0.0, lam1_lo=0.0, t1_step=0,
                     lam2_hi=0.0, lam2_lo=0.0, t2_step=0),
    "deployed": dict(lam1_hi=DEPLOYED_PAM_LAM, lam1_lo=DEPLOYED_PAM_LAM, t1_step=0,
                     lam2_hi=DEPLOYED_PAM_LAM, lam2_lo=DEPLOYED_PAM_LAM, t2_step=0),
    "reshaped": dict(lam1_hi=CORTEX_LAM_HI, lam1_lo=CORTEX_LAM_LO, t1_step=RESHAPED_T1_STEP,
                     lam2_hi=CORTEX_LAM_HI, lam2_lo=CORTEX_LAM_LO, t2_step=RESHAPED_T2_STEP),
}

# ---- cue axis (per column, three segments) ----
# represented as a list of cue specs: each dict {seg, alpha}. seg in {flat, repose, sharp}.
#   flat   = deployed flat-diffuse (diffuse structure, alpha=0)            -> baseline
#   repose = flat-diffuse with content-blind common-mode centering alpha   -> candidates
#   sharp  = pure unit differentiating cue (dgate diffuse=False)           -> alive-reference ONLY
def cue_axis():
    axis = [dict(seg="flat", alpha=0.0)]
    axis += [dict(seg="repose", alpha=a) for a in REPOSING_ALPHAS if a > 0.0]
    axis += [dict(seg="sharp", alpha=0.0)]
    return axis


def commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(_HERE),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def spec_hash() -> str:
    payload = dict(
        DEPLOYED_PAM_LAM=DEPLOYED_PAM_LAM, M_DEPLOYED=M_DEPLOYED,
        DIFFUSE_SHARED=round(DIFFUSE_SHARED, 4), DIFFUSE_CUE=DIFFUSE_CUE,
        HEALTHY=round(HEALTHY, 4), LIVE_BAR=round(LIVE_BAR, 4),
        OFF_SHARP_REF=round(OFF_SHARP_REF, 4), SEEDS=SEEDS, KNOBS=KNOBS,
        PENALTY_REGIMES=PENALTY_REGIMES)
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:12]


def reconcile_register() -> dict:
    """The full surfaced register: READ values + KNOB choices, with provenance. Written into every
    Step-0 artifact so the review gate sees exactly what was reconciled vs chosen."""
    return dict(
        commit_hash=commit_hash(), spec_hash=spec_hash(),
        READ_from_exp06_commit=dict(
            deployed_pam_lam=DEPLOYED_PAM_LAM, m_deployed=M_DEPLOYED,
            diffuse_shared_mag=round(DIFFUSE_SHARED, 4), diffuse_cue_mag=DIFFUSE_CUE,
            diffuse_snr=round(DIFFUSE_SNR, 4),
            healthy=round(HEALTHY, 4), live_bar=round(LIVE_BAR, 4),
            collapse_ceiling=COLLAPSE_CEILING, ablation_floor=ABLATION_FLOOR,
            off_sharp_ref_1106=round(OFF_SHARP_REF, 4),
            off_sharp_ref_source="exp06_reconfirm [1,0,0] @ bstar=12000, 16 seeds (equal-training)",
            deployed_cortex_clock=dict(t1=DEPLOYED_T1, t2=DEPLOYED_T2,
                                       stream_steps=DEPLOYED_STREAM_STEPS,
                                       t1_fraction=round(RESHAPED_T1_FRACTION, 4),
                                       t2_fraction=round(RESHAPED_CLOCK_FRACTION, 4),
                                       lam_hi=CORTEX_LAM_HI, lam_lo=CORTEX_LAM_LO),
            seeds=SEEDS,
            anchor_commit=_ANCHOR.get("commit_hash", "unknown"),
        ),
        KNOB_choices=KNOBS,
        notes=[
            "SHARP segment = dgate diffuse=False (pure UNIT differentiating cue). The spec's '~5.83' "
            "for sharp is the salient-magnitude descriptor; the BINDING reconcile is the Step-0c "
            "anchor off-sharp ~= 1.106 = exp06 [1,0,0], which is the unit-cue diffuse=False cell. "
            "Implemented to reproduce 1.106, NOT a 5.83-magnitude cue.",
            "RESHAPED = the settled cortex StepSchedule applied to PAM's tie (the spec's preserve "
            "argument: architectural uniformity with the cortices). lam1 (groups) opens at t1/steps=0.075, "
            "lam2 (capacity) at t2/steps=0.30 (the swept clock-onset), strength 10->0. The naive "
            "single-clock pool_penalty(lam,lam) was REJECTED: penalising delta1 too annihilates the group "
            "symmetry-breakers -> irreversible collapse trap -> a manufactured dead reshaped column. The "
            "two-clock keeps groups alive; reshaped-sharp REVIVES at plateau (oracle test passes).",
            "Surface corners reproduce exp06: off-flat=[1,1,0]=0.000, off-sharp=[1,0,0]=1.106, "
            "deployed-*=[1,*,1]=0.000. NEW content = the re-posing segment + the reshaped column.",
        ],
    )


if __name__ == "__main__":
    print(json.dumps(reconcile_register(), indent=2))
