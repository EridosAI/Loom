"""exp19_g0b_redteam.py — reachable-falsifier proof for G0b's content-digest gate (ledger 31).

Jason 2026-07-14: "Until it has failed once, it is dead code." Same discipline as wp-strat-label and
wpT's live B=128 falsifier. This proves the content digest FIRES on a permutation change that the
demoted manifest companion CANNOT see — i.e., it catches exactly G0b v1's blind spot.

Self-contained and cheap (small T, exp12_shuffle only; no worktree/reference). Build the unshuffled
base once, apply the real shuffle perm and two perturbations of it:

  flip : perm.flip(0) — a PURE reorder. Manifest fabric-fingerprint IDENTICAL (order-invariant
         counts/means/keys), content digest DIFFERENT. This is the v1 blind spot, now caught.
  bump : a perm drawn from keys["shuffle"] + 1 — a different realized order. Digest DIFFERENT.

Exit 1 if the digest fails to fire (dead code) OR if the manifest is NOT blind to the flip (then the
flip is not a clean isolation of the blind spot).
"""
import copy
import json
import sys

import torch
torch.set_num_threads(1)

import exp12_fabric as F
import exp12_arms as X12
from exp19_g0b_genregress import content_digest, PERM_FIELDS

SEED, T = 0, 4000


def _apply_perm(base, p):
    f2 = copy.copy(base)                              # shallow: dwell-level arrays shared (unpermuted)
    for name in PERM_FIELDS:
        setattr(f2, name, getattr(base, name)[p])
    f2.perm, f2.shuffled = p, True
    return f2


def _manifest_fabric(loop, cfg, fab):
    twin = F.build_fabric(loop.stim, cfg, cfg.seed, fab.T, shuffled=False)
    asr = F.fabric_asserts(twin, cfg)
    return json.dumps(F.fabric_manifest(fab, loop.stim, cfg, asr)["fabric"], sort_keys=True, default=str)


def main():
    loop, spec, cfg = X12.build_exp12("exp12_shuffle", SEED, T)
    Tf = loop.stream.T
    twin = F.build_fabric(loop.stim, cfg, cfg.seed, Tf, shuffled=False)   # unshuffled base

    perm = torch.randperm(Tf, generator=torch.Generator().manual_seed(F.SEED_SHUFFLE + SEED))
    perm_bump = torch.randperm(Tf, generator=torch.Generator().manual_seed(F.SEED_SHUFFLE + SEED + 1))

    fab_real = _apply_perm(twin, perm)                # reconstruction of exp12_shuffle's certified order
    fab_flip = _apply_perm(twin, perm.flip(0))        # pure REORDER
    fab_bump = _apply_perm(twin, perm_bump)           # different realized order

    # CONTENT-only perturbation: shift one raw wave (no order/perm/dwell_k/nuis/bg change). The manifest
    # never reads raw, so its fabric fingerprint stays identical; the digest hashes raw, so it must fire.
    fab_content = copy.copy(fab_real)
    raw2 = fab_real.raw.clone(); raw2.view(-1)[0] += 1.0
    fab_content.raw = raw2

    d_real = content_digest(fab_real)
    d_stream = content_digest(loop.stream)            # bind the proxy to the REAL certified build
    d_flip, d_bump = content_digest(fab_flip), content_digest(fab_bump)
    d_content = content_digest(fab_content)
    d_real2 = content_digest(_apply_perm(twin, perm))                     # stability
    m_real = _manifest_fabric(loop, cfg, fab_real)
    m_flip = _manifest_fabric(loop, cfg, fab_flip)
    m_content = _manifest_fabric(loop, cfg, fab_content)

    checks = {
        "red-team fabric BOUND to real build (reconstruction == loop.stream)": d_real == d_stream,
        "digest stable (real == real2)": d_real == d_real2,
        "digest FIRES on ORDER flip (real != flip)": d_real != d_flip,
        "digest FIRES on ORDER seed-bump (real != bump)": d_real != d_bump,
        "digest FIRES on CONTENT raw-perturb (real != content)": d_real != d_content,
        "manifest BLIND to flip (real == flip) — the v1 ORDER blind spot": m_real == m_flip,
        "manifest BLIND to content raw-perturb (real == content) — the CONTENT blind spot": m_real == m_content,
    }
    ok = True
    for k, v in checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        ok &= v
    print()
    if not ok:
        print("RED-TEAM FAILED — the gate is not falsifiable as claimed.")
        sys.exit(1)
    print("RED-TEAM PASS — on a fabric BOUND to the real build, the content digest fires on ORDER and "
          "CONTENT perturbations the manifest is blind to. The gate has failed on planted blind-spot "
          "perturbations — it is not dead code.")


if __name__ == "__main__":
    main()
