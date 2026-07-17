"""exp19_smokes.py — B10: the W-PERM pre-flight smokes (prereg §7, v5-governed).

  wp1        B=1 ⇒ bit-identical to exp12_dwell — FABRIC (every permuted field) AND WEIGHTS (vision/op/word
             state_dicts after a smoke-horizon run). block_perm(T,1,g) is the identity permutation applied
             through the shuffled branch; divergence ⇒ added/dropped update, shifted draw, or fab.shuffled
             set wrongly. Registry refuses B=1 by design (REUSED) ⇒ a TEST-ONLY ARMS12 entry, deleted after.
  wpT        B=T ⇒ bit-identical to exp12_shuffle — same two levels. block_perm(T,T,g) is documented
             bit-exact randperm(T,g) (exp12_fabric:222); divergence ⇒ the ceiling is uncertified.
  wp-parity  n_optimizer_steps (loop._t) equal across every arm at the same horizon — compute confound fence.
  wp-posassert  the exp14_arms:1969-pattern positive assert (`fc.shuffled`) must NOT fire for W-PERM arms
             (wperm arms set shuffled=True).
  wp-delta   fails under a no-op: B=1 weights ≠ B=T weights at the same horizon; ρ(B) strictly decreasing.
  wp-strat-label  (§4.2, naive-first): the naive pos==1 stratifier and the PROPERTY (zero_preceding_mask)
             COINCIDE at B=1 and DIVERGE at every B>1 — and at every B>1 the naive mask contains
             CONTAMINATED onsets (naive & ~property nonempty): the gate would certify its own confound.
             The naive version is written first and shown RED, per the pin.

All smoke-horizon (S=2000 run / 50k index-list); trains nothing that persists; test-only registry entries
are removed in `finally`. Every assert is a reachable falsifier (wp-delta is the no-op killer).
"""
from __future__ import annotations

import sys

import torch

import exp12_arms as X12
import exp12_fabric as F
import exp19_score as S19

S_RUN = 2000                # weight-level smoke horizon
S_IDX = 50_000              # index-list horizon for rho / strat-label (build-only, no training)
B_LADDER = (32, 128, 512, 2048)


def _run(name: str, seed: int, steps: int):
    loop, _spec, _cfg = X12.build_exp12(name, seed, steps)
    for _ in range(steps):
        loop.step(no_word=False)
    return loop


def _weights(loop) -> dict:
    out = {}
    for m in ("vision", "op", "word"):
        for k, v in getattr(loop, m).state_dict().items():
            out[f"{m}.{k}"] = v
    return out


def _w_equal(a: dict, b: dict) -> bool:
    return set(a) == set(b) and all(torch.equal(a[k], b[k]) for k in a)


FAB_FIELDS = ("a", "b", "member", "cat", "dwell_id", "pos", "mask_slot",
              "is_exam", "is_probe_exam", "nuis", "bg", "raw")


def _fab_equal(fa, fb) -> tuple[bool, str]:
    for f in FAB_FIELDS:
        if not torch.equal(getattr(fa, f), getattr(fb, f)):
            return False, f
    return True, ""


def main():
    torch.set_num_threads(1)
    print("=== B10 W-PERM smokes (S_run=%d, S_idx=%d) ===" % (S_RUN, S_IDX))
    tmp = []
    try:
        # ---- wp1: identity-window ⇒ exp12_dwell, fabric AND weights
        X12.ARMS12["exp19_wp1s"] = dict(shuffled=True, wperm_B=1); tmp.append("exp19_wp1s")
        ld = _run("exp12_dwell", 0, S_RUN)
        l1 = _run("exp19_wp1s", 0, S_RUN)
        ok, f = _fab_equal(ld.stream, l1.stream)
        assert ok, f"wp1 FABRIC diverged at field {f!r}"
        assert l1.stream.shuffled, "wp-posassert: wperm fabric must set shuffled=True (exp14_arms:1969 pattern)"
        assert _w_equal(_weights(ld), _weights(l1)), "wp1 WEIGHTS diverged (B=1 != exp12_dwell)"
        print("  wp1  PASS — B=1 fabric AND weights bit-identical to exp12_dwell "
              "(identity perm through the shuffled branch)")
        # ---- wpT: single-block ⇒ exp12_shuffle, fabric AND weights
        ls = _run("exp12_shuffle", 0, S_RUN)
        T = ls.stream.T
        X12.ARMS12["exp19_wpTs"] = dict(shuffled=True, wperm_B=int(T)); tmp.append("exp19_wpTs")
        lt = _run("exp19_wpTs", 0, S_RUN)
        ok, f = _fab_equal(ls.stream, lt.stream)
        assert ok, f"wpT FABRIC diverged at field {f!r} (block_perm(T,T) != randperm)"
        assert _w_equal(_weights(ls), _weights(lt)), "wpT WEIGHTS diverged (B=T != exp12_shuffle)"
        print(f"  wpT  PASS — B=T (T={T}) fabric AND weights bit-identical to exp12_shuffle")
        # ---- wp-parity: optimizer steps equal across arms at one horizon (paid-B arm included)
        paid = X12.exp19_wperm(32)
        lp = _run(paid, 0, S_RUN)
        ts = {n: l._t for n, l in (("dwell", ld), ("wp1", l1), ("shuffle", ls), ("wpT", lt), (paid, lp))}
        assert len(set(ts.values())) == 1, f"wp-parity FAIL: optimizer steps differ {ts}"
        assert lp.stream.shuffled, "wp-posassert: paid wperm arm must set shuffled=True"
        print(f"  wp-parity PASS — n_optimizer_steps identical across 5 arms ({set(ts.values())}); "
              "wp-posassert PASS (shuffled=True on wperm fabrics — the 1969-pattern assert cannot fire)")
        # ---- wp-delta: the no-op killer
        assert not _w_equal(_weights(l1), _weights(lt)), "wp-delta FAIL: B=1 == B=T (smoke is a no-op)"
        # rho(B) strictly decreasing + wp-strat-label on the index-list fabric
        loop_idx, _s, _c = X12.build_exp12("exp12_dwell", 0, S_IDX)
        fab = loop_idx.stream
        d0, p0, e0 = fab.dwell_id, fab.pos, fab.is_exam
        Tf = fab.T
        rhos = [S19._rho(d0)]
        labels = ["1"]
        for B in B_LADDER + (Tf,):
            g = torch.Generator().manual_seed(F.SEED_SHUFFLE + 0)
            perm = F.block_perm(Tf, B, g)
            d_em, p_em, e_em = d0[perm], p0[perm], e0[perm]
            rhos.append(S19._rho(d_em))
            labels.append("T" if B == Tf else str(B))
            naive = e_em & (p_em == 1)                      # the §4.2 TRAP, written first
            zpm = S19._zero_preceding(d_em, e_em)           # the PROPERTY
            contaminated = int((naive & ~zpm).sum())
            assert contaminated > 0 and not torch.equal(naive, zpm), \
                f"wp-strat-label FAIL at B={B}: masks coincide (naive stratifier would NOT be caught)"
        naive1 = e0 & (p0 == 1)
        assert torch.equal(naive1, S19._zero_preceding(d0, e0)), \
            "wp-strat-label FAIL at B=1: masks must COINCIDE (stratified read IS the full read)"
        assert all(rhos[i] > rhos[i + 1] for i in range(len(rhos) - 1)), \
            f"wp-delta FAIL: rho(B) not strictly decreasing: {dict(zip(labels, [round(r,4) for r in rhos]))}"
        print(f"  wp-delta PASS — B=1 != B=T weights; rho strictly decreasing "
              f"{ {l: round(r, 4) for l, r in zip(labels, rhos)} }")
        print("  wp-strat-label PASS — naive pos==1 vs zero_preceding: COINCIDE at B=1, DIVERGE at every "
              "B>1 with contaminated onsets present (the naive gate shown RED, per §4.2)")
        print("B10 SMOKES: ALL PASS")
    finally:
        for n in tmp:
            X12.ARMS12.pop(n, None)


if __name__ == "__main__":
    main()
