"""exp06 Step-0 GATE-VALIDITY probes (pre-review). Answers three diagnostic questions about whether
the gate's numbers are real, BEFORE the interior cube is read. NOT interior interpretation — these
test the validity of the gate itself.

Q1 (plateau): do the many-member / collapse cells PLATEAU by the deployed budget (flat d/loss), or are
    they still moving (under-training masquerading as collapse)? -> trajectory to 2x the budget.
Q3 (genuine death vs magnitude artifact): for the single-toggle COLLAPSE cells, is d_diff=0 a real
    content-invariant death, or a magnitude artifact hiding a live channel under a large common-mode?
    The (d) metric normalises by output norm, so a huge-norm/small-member-signal output could read
    ~0 spuriously (the dual of the canon clamp_min false-POSITIVE). -> measure ABSOLUTE member
    separation + a noise-decodability SNR (between-member vs within-member), independent of (d)'s
    normalisation. Genuine death => members are NOT recoverable by ANY measure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

from dgate import (Factors, make_op, _task_tensors, _window, measure_d, _sep,  # noqa: E402
                   W, N_SLOTS, KAPPA, D)


def _slot_ids():
    return torch.tensor([s for _ in range(W) for s in range(N_SLOTS)])


def train_with_trajectory(f: Factors, seed: int, checkpoints):
    """Train as dgate.train_neutral_op but snapshot (loss, d_diff, proto_spread) at each checkpoint.
    Identical optimisation path; the only addition is read-only measurement."""
    op = make_op(seed)
    V, Cd, base, u = _task_tensors(f, seed)
    sid = _slot_ids()
    opt = torch.optim.Adam(op.parameters(), lr=f.lr)
    g = torch.Generator().manual_seed(seed * 911 + 7)
    M = f.member_count
    traj = []
    cps = sorted(set(checkpoints))
    last_loss = None
    for step in range(max(cps) + 1):
        if step in cps:
            rec = measure_d(op, f, seed)
            traj.append(dict(step=step, loss=last_loss, d_diff=rec["d_diff"],
                             proto_spread=rec["proto_spread"]))
        m = int(torch.randint(0, M, (1,), generator=g))
        target, mask, cells = _window(f, V, Cd, base, u, m, m, op, ablate=False)
        pred = op(cells.unsqueeze(0), sid, (~mask))[0]
        loss = F.mse_loss(pred[mask], target[mask])
        if f.pam_lam > 0.0:
            loss = loss + op.pam.pool_penalty(f.pam_lam, f.pam_lam)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        last_loss = float(loss.detach())
    return traj


@torch.no_grad()
def _noisy_evoke(op, f, V, Cd, base, u, m, cls, sigma, K, gen):
    """Evoke member m's masked item K times with gaussian noise added to the visible CUE (sigma).
    The op never sees the item (masked); within-member spread comes from cue noise. Returns (K, D)."""
    sid = _slot_ids()
    outs = []
    for _ in range(K):
        _, mask, cells = _window(f, V, Cd, base, u, m, cls, op, ablate=False)
        # re-inject cue noise on the visible companion cells (slot 1)
        noise = sigma * torch.randn(cells.shape, generator=gen)
        cue_cells = torch.tensor([w * N_SLOTS + 1 for w in range(W)])
        cells = cells.clone()
        cells[cue_cells] = cells[cue_cells] + noise[cue_cells]
        pred = op(cells.unsqueeze(0), sid, (~mask))[0]
        outs.append(pred[0])
    return torch.stack(outs)


def genuineness(f: Factors, seed: int, *, sigma=0.20, K=64) -> dict:
    """Train the cell (needs grad), then test whether member identity is recoverable from evocations
    by ANY measure independent of (d)'s norm-normalisation. Genuine death => no recovery."""
    from dgate import train_neutral_op
    op = train_neutral_op(f, seed)                            # training: grad ON
    V, Cd, base, u = _task_tensors(f, seed)
    M = f.member_count
    sid = _slot_ids()

    with torch.no_grad():
        # deterministic clean evocations (the (d)-gate's own inputs)
        outs = []
        for m in range(M):
            _, mask, cells = _window(f, V, Cd, base, u, m, m, op, ablate=False)
            outs.append(op(cells.unsqueeze(0), sid, (~mask))[0][0])
        clean = torch.stack(outs)
        out_norm = clean.norm(dim=1).mean().item()
        off = ~torch.eye(M, dtype=torch.bool)
        abs_pairwise = torch.cdist(clean, clean)[off].mean().item()   # UN-normalised member separation
        d_diff_norm = _sep(clean)                            # the (d) metric (norm-normalised)

        # noise-decodability SNR: per-member centroid distance vs within-member spread
        gen = torch.Generator().manual_seed(seed * 53 + 11)
        cents, withins, samples, labels = [], [], [], []
        for m in range(M):
            e = _noisy_evoke(op, f, V, Cd, base, u, m, m, sigma, K, gen)   # (K, D)
            cents.append(e.mean(0))
            withins.append((e - e.mean(0)).norm(dim=1).mean().item())
            samples.append(e); labels += [m] * K
        cents = torch.stack(cents)
        within_spread = sum(withins) / len(withins) + 1e-9
        between = torch.cdist(cents, cents)[off].mean().item()
        snr = between / within_spread                         # >>1 => members separable (live/artifact);
                                                             # ~0 => genuine death
        # nearest-centroid member-recovery accuracy on the noisy samples (chance = 1/M)
        X = torch.cat(samples); y = torch.tensor(labels)
        acc = (torch.cdist(X, cents).argmin(1) == y).float().mean().item()

        Wp = op.pam.weights()
        proto_spread = (Wp - Wp.mean(0)).norm(dim=1).mean().item()
    return dict(member_count=M, diffuse=f.diffuse, pam_lam=f.pam_lam,
                d_diff_norm=round(d_diff_norm, 5), abs_pairwise=round(abs_pairwise, 5),
                out_norm=round(out_norm, 4), proto_spread=round(proto_spread, 5),
                decode_snr=round(snr, 4), decode_acc=round(acc, 4), chance=round(1.0 / M, 4),
                within_spread=round(within_spread, 5), between_spread=round(between, 5))


def main():
    cfg = dict(diffuse_shared_mag=5.831, diffuse_cue_mag=0.5, train_steps=4000)
    cells = {
        "0,0,0 CLEAN":   Factors(member_count=2,  diffuse=False, pam_lam=0.0,  **cfg),
        "0,0,1 penOnly": Factors(member_count=2,  diffuse=False, pam_lam=0.01, **cfg),
        "0,1,0 diffOnly":Factors(member_count=2,  diffuse=True,  pam_lam=0.0,  **cfg),
        "1,0,0 manyOnly":Factors(member_count=16, diffuse=False, pam_lam=0.0,  **cfg),
        "1,1,1 DEAD":    Factors(member_count=16, diffuse=True,  pam_lam=0.01, **cfg),
    }
    CKPTS = [200, 500, 1000, 2000, 3000, 4000, 6000, 8000]

    print("=" * 78)
    print("Q1 — TRAJECTORY (plateau check; seed 0): d_diff / proto_spread / loss vs step")
    print("=" * 78)
    q1 = {}
    for name, f in cells.items():
        traj = train_with_trajectory(f, 0, CKPTS)
        q1[name] = traj
        print(f"\n{name}:")
        print("  step :  " + "  ".join(f"{t['step']:>6d}" for t in traj))
        print("  d    :  " + "  ".join(f"{t['d_diff']:>6.3f}" for t in traj))
        print("  proto:  " + "  ".join(f"{t['proto_spread']:>6.3f}" for t in traj))
        print("  loss :  " + "  ".join(f"{(t['loss'] if t['loss'] is not None else 0):>6.3f}" for t in traj))

    print("\n" + "=" * 78)
    print("Q3 — GENUINE DEATH vs MAGNITUDE ARTIFACT (collapse cells; 3 seeds)")
    print("    decode_snr/acc are INDEPENDENT of (d)'s norm-normalisation. genuine death => acc~chance")
    print("=" * 78)
    q3 = {}
    for name in ("0,0,0 CLEAN", "0,0,1 penOnly", "0,1,0 diffOnly", "1,1,1 DEAD"):
        f = cells[name]
        rows = [genuineness(f, s) for s in (0, 1, 2)]
        q3[name] = rows
        print(f"\n{name}:")
        for s, r in zip((0, 1, 2), rows):
            print(f"  seed{s}: d_norm={r['d_diff_norm']:.4f} abs_pairwise={r['abs_pairwise']:.4f} "
                  f"out_norm={r['out_norm']:.3f} proto={r['proto_spread']:.4f} | "
                  f"decode_acc={r['decode_acc']:.3f} (chance {r['chance']}) snr={r['decode_snr']:.3f}")

    Path("exp06_gate_validation.json").write_text(json.dumps(dict(Q1_trajectory=q1, Q3_genuineness=q3),
                                                             indent=2))
    print("\n(record -> exp06_gate_validation.json)")


if __name__ == "__main__":
    main()
