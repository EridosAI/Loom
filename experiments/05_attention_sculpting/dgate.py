"""The neutral operator-liveness gate — the (d)-gate — promoted to a committed module (exp06 §3).

This is the **content-agnostic** liveness measurement the design table pre-registered as the pass any
channel revival must clear (FRONTIER §10.5 / PROJECT_STATE §12.E). It was scratchpad-prototyped while
building exp05 and produced the two canon anchors:
  * fresh op trained on a clean neutral 2-member task  -> d_diff = 1.275   (the HEALTHY capacity)
  * op trained via the full deployed SculptLoop          -> d_diff = 0.000   (the dead channel)
exp06 promotes it here, unchanged in spirit, and imposes the three named factors (member-count ×
cue-diffuseness × PAM pool-penalty) ON this protocol so the clean->dead gap is decomposed (decompose-
first). The CONTENT is always random/neutral (unrelated to any conflict stimulus); only the regime
factors vary. The carrier is the within-window-relative bounded drift in EVERY cell (the necessary-not-
sufficient baseline of FRONTIER §10.3) — never an axis here.

The measurement (exp05 prototype, generalised to M members):
  * neutral task: M members, each a random unit ITEM vector V[m]; each member associated with a
    differentiating companion direction Cd[assoc[m]]. The companion (cue) slot is VISIBLE; the item
    slot is MASKED. The operator must complete the masked item from the visible cue.
  * d_diff = associated-DIFFERENT: assoc[m] = m (each member -> its own cue) -> a live channel evokes
    DISTINCT items -> large mean-pairwise-normalised separation.
  * d_same = associated-SAME: assoc[m] = 0 (all members -> one cue) -> the cue carries no member info
    -> a sound channel does NOT differentiate (sep ~0). Guards against the op leaking masked-item info.
  * d_ablated = differentiating-cue zeroed (the base/shared part kept) -> sep MUST collapse to ~chance.
    A revival whose ablation does NOT collapse is a magnitude artifact (the init=1.0 clamp_min false
    positive of FRONTIER §10 provenance) -> rejected, never counted.

Decision (exp06 §4): a cell is REVIVED iff d_diff >= healthy AND ablation collapses. Binary at the
healthy bar (~1.275); the graded d is logged for interaction evidence only, never tuned to.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))  # exp04 (op, constants)

from pam_operator import PrototypeResonanceOperator  # noqa: E402

# Fixed, non-factor structural constants of the neutral probe (carry the exp05 prototype verbatim).
D = 16                  # slice dim (= Stage0Config.D)
D_MODEL = 64            # operator hidden (= Stage0Config.d_model)
PAM_GROUPS = 8          # (= Stage0Config.pam_groups)
PAM_MEMBERS = 4         # (= Stage0Config.pam_members)
N_SLOTS = 2             # item slot + cue slot
W = 2                   # 2-wave within-dwell window (the exp05 neutral probe)
KAPPA = 0.3             # bounded carrier scale: drift in [-0.5, +0.5] (within-window-relative). BASELINE.
EPS = 1e-9


@dataclass
class Factors:
    """One cube cell = one assignment of the three factors (carrier bounded in all, never a factor)."""
    member_count: int        # M: clean=2, deployed='many' [RECONCILE]
    diffuse: bool            # cue-diffuseness: False=sharp (pure unit cue), True=deployed salience structure
    pam_lam: float           # PAM pool-penalty during training: clean=0.0, deployed [RECONCILE]
    # diffuse-cue magnitudes (imported from the exp05 conflict salience structure; random DIRECTIONS,
    # so the probe stays content-agnostic). sharp ignores these.
    diffuse_shared_mag: float = 5.831     # sqrt(R_coarse^2 + r_distractor^2) = sqrt(25+9), the salient
                                          # shared/uninformative cue energy (deployed)
    diffuse_cue_mag: float = 0.5          # r_category, the subtle member-differentiating cue (deployed)
    train_steps: int = 3000
    lr: float = 3e-3

    @property
    def cue_snr(self) -> float:
        """Differentiating fraction of the cue magnitude (sharp=1.0; diffuse=deployed subtle ratio)."""
        if not self.diffuse:
            return 1.0
        import math
        return self.diffuse_cue_mag / math.sqrt(self.diffuse_shared_mag ** 2 + self.diffuse_cue_mag ** 2)


def _task_tensors(f: Factors, seed: int):
    """Random neutral content for an M-member task. Returns (V, Cd, base, u)."""
    g = torch.Generator().manual_seed(seed * 101 + 17)
    M = f.member_count
    V = F.normalize(torch.randn(M, D, generator=g), dim=1)        # masked ITEM targets (one per member)
    Cd = F.normalize(torch.randn(M, D, generator=g), dim=1)       # differentiating cue dirs (one per assoc class)
    base = F.normalize(torch.randn(D, generator=g), dim=0)        # shared salient cue dir (diffuse only)
    u = F.normalize(torch.randn(D, generator=g), dim=0)           # bounded carrier direction
    return V, Cd, base, u


def _companion(f: Factors, Cd, base, cls: int, *, ablate: bool) -> torch.Tensor:
    """The visible cue for association class ``cls``. sharp = pure unit differentiating dir; diffuse =
    deployed salience structure (large shared base + subtle differentiating cue). Ablation zeroes the
    DIFFERENTIATING part only (keeps the shared base) -> the member-distinguishing signal is removed."""
    if not f.diffuse:
        return torch.zeros(D) if ablate else Cd[cls]
    diff = torch.zeros(D) if ablate else f.diffuse_cue_mag * Cd[cls]
    return f.diffuse_shared_mag * base + diff


def _window(f: Factors, V, Cd, base, u, m: int, cls: int, op, *, ablate: bool):
    """Build the (masked-item, visible-cue) W=2 window for member m / assoc class cls + bounded carrier."""
    item = V[m]
    comp = _companion(f, Cd, base, cls, ablate=ablate)
    content = torch.zeros(W, N_SLOTS, D)
    content[:, 0, :] = item
    content[:, 1, :] = comp
    mask = torch.zeros(W, N_SLOTS, dtype=torch.bool)
    mask[:, 0] = True                                            # mask items; cue visible
    masked = content.clone()
    masked[mask] = op.mask_emb
    drift = torch.arange(W, dtype=torch.float32) - (W - 1) / 2.0  # [-0.5, +0.5] : bounded, within-window
    cells = (masked + KAPPA * drift.view(W, 1, 1) * u).reshape(W * N_SLOTS, D)
    return content.reshape(W * N_SLOTS, D), mask.reshape(-1), cells


def make_op(seed: int) -> PrototypeResonanceOperator:
    """Fresh operator at the DEPLOYED form/init (no init rescale — init is not a factor; the clean
    corner already reaches 1.275 at default init, exp05 line-1057)."""
    return PrototypeResonanceOperator(
        D_slice=D, n_slots=N_SLOTS, d_model=D_MODEL,
        pam_groups=PAM_GROUPS, pam_members=PAM_MEMBERS, seed=seed * 131 + 3)


def train_neutral_op(f: Factors, seed: int) -> PrototypeResonanceOperator:
    """Train a fresh op on the neutral associated-DIFFERENT task under this cell's factors. The PAM
    pool-penalty (factor) is the ONLY thing added to the MSE completion loss; carrier bounded; content
    random. This is the exp05 line-1057 protocol generalised to M members + the two regime knobs."""
    op = make_op(seed)
    V, Cd, base, u = _task_tensors(f, seed)
    slot_ids = torch.tensor([s for _ in range(W) for s in range(N_SLOTS)])
    opt = torch.optim.Adam(op.parameters(), lr=f.lr)
    g = torch.Generator().manual_seed(seed * 911 + 7)
    M = f.member_count
    for _ in range(f.train_steps):
        m = int(torch.randint(0, M, (1,), generator=g))
        target, mask, cells = _window(f, V, Cd, base, u, m, m, op, ablate=False)  # assoc-different: cls=m
        pred = op(cells.unsqueeze(0), slot_ids, (~mask))[0]
        loss = F.mse_loss(pred[mask], target[mask])
        if f.pam_lam > 0.0:
            loss = loss + op.pam.pool_penalty(f.pam_lam, f.pam_lam)               # the deployed penalty
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return op


def _sep(evoked: torch.Tensor) -> float:
    """Mean pairwise L2 over evoked items, normalised by mean item norm. ~1.27 if members map to
    distinct items (live), ~0 if all collapse to one point (dead). Roughly member-count invariant."""
    M = evoked.shape[0]
    if M < 2:
        return 0.0
    dm = torch.cdist(evoked, evoked)
    off = ~torch.eye(M, dtype=torch.bool)
    scale = evoked.norm(dim=1).mean().item() + EPS
    return dm[off].mean().item() / scale


@torch.no_grad()
def measure_d(op: PrototypeResonanceOperator, f: Factors, seed: int) -> dict:
    """Probe the trained op's evocation: d_diff (assoc-different), d_same (assoc-same), d_ablated
    (differentiating cue zeroed). Read-only; generic resonance (no retraining)."""
    V, Cd, base, u = _task_tensors(f, seed)
    slot_ids = torch.tensor([s for _ in range(W) for s in range(N_SLOTS)])
    M = f.member_count

    def evoke(cls_of, *, ablate=False):
        outs = []
        for m in range(M):
            _, mask, cells = _window(f, V, Cd, base, u, m, cls_of(m), op, ablate=ablate)
            pred = op(cells.unsqueeze(0), slot_ids, (~mask))[0]
            outs.append(pred[0])                                   # masked item slot, wave 0
        return torch.stack(outs)

    e_diff = evoke(lambda m: m)                                    # each member -> its own cue
    e_same = evoke(lambda m: 0)                                    # all members -> cue class 0
    e_abl = evoke(lambda m: m, ablate=True)                        # differentiating cue removed
    Wp = op.pam.weights()
    proto_spread = (Wp - Wp.mean(0)).norm(dim=1).mean().item()
    return dict(d_diff=_sep(e_diff), d_same=_sep(e_same), d_ablated=_sep(e_abl),
                proto_spread=proto_spread)


def dgate(f: Factors, seed: int) -> dict:
    """Train + measure one cell at one seed. The atomic (d)-gate reading."""
    op = train_neutral_op(f, seed)
    rec = measure_d(op, f, seed)
    rec.update(member_count=f.member_count, diffuse=f.diffuse, pam_lam=f.pam_lam,
               cue_snr=f.cue_snr, seed=seed)
    return rec


@torch.no_grad()
def force_collapsed_floor(seed: int = 0) -> dict:
    """collapse_floor reference: an op whose PAM prototypes are forced identical (the deployed
    content-invariant regime, FRONTIER §10.1). d_diff here is the floor a dead corner must reach."""
    f = Factors(member_count=2, diffuse=False, pam_lam=0.0)
    op = make_op(seed)
    with torch.no_grad():
        Wp = op.pam.weights()
        mean = Wp.mean(0)
        # drive every prototype to the mean -> z = pa @ Wp = mean for any input (content-invariant)
        op.pam.base_root.copy_(mean)
        op.pam.delta1.zero_()
        op.pam.delta2.zero_()
    return measure_d(op, f, seed)
