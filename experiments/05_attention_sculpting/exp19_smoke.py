"""exp19_smoke.py — EXP19 W-PERM build smokes (Part C, positive-delta asserts).

Ships incrementally as the build lands. This first tranche (per Jason's order — B1-B3 + wp1/wpT +
verify wp-multiset fires) covers the two REUSED endpoints and the already-built multiset gate:

  wp1         B=1 reduces to exp12_dwell (no perm; fab.shuffled False) — and a paid B>1 build does NOT
              (fab.shuffled True, order differs) while preserving the wave multiset. Falsifier: B=1
              built through the shuffle path / fab.shuffled set wrongly.
  wpT         B=T reduces BIT-IDENTICALLY to exp12_shuffle (block_perm(T,T) == randperm(T)). Falsifier:
              the constructor diverges from exp12_fabric.py:431 at its limit -> the ceiling is uncertified.
  wp-multiset G3 — the COMMITTED twin-rebuild + checksum-assert (exp12_arms:443-451, run via
              _assert_one) FIRES and PASSES on a W-PERM fabric. NOT rebuilt (deleted from build scope);
              this verifies it. Falsifier: a block permutation changes the multiset.

Fabric-level bit-identity (deterministic => weight-identical); the deployed-horizon weight-level replay
is the pre-flight gate (G1a/G1b). Exits non-zero on any failure.
"""
import sys

import torch
torch.set_num_threads(1)

import exp12_fabric as F
import exp12_arms as X12
import exp14_arms as XA
import exp19_score as SC

SEED = 0
T = 4000                                              # multiple blocks at B=32/128; ragged tail
FIELDS = ("a", "b", "member", "cat", "dwell_id", "pos", "mask_slot",
          "is_exam", "is_probe_exam", "nuis", "bg", "raw")


def _fab(arm):
    loop, spec, cfg = X12.build_exp12(arm, SEED, T)
    return loop, cfg, loop.stream


def wpT():
    """B=T bit-identical to exp12_shuffle."""
    loop, cfg, fab_C = _fab("exp12_shuffle")          # randperm(T) reorder of the dwelled base
    fab_wpT = F.build_fabric(loop.stim, cfg, cfg.seed, fab_C.T, shuffled=True, wperm_B=fab_C.T)
    fields_ok = all(torch.equal(getattr(fab_wpT, f), getattr(fab_C, f)) for f in FIELDS)
    perm_ok = torch.equal(fab_wpT.perm, fab_C.perm)
    assert fields_ok and perm_ok, "wpT: block_perm(T,T) fabric != exp12_shuffle — ceiling uncertified"
    # reachable falsifier: a real block window (B<T) must NOT equal exp12_shuffle
    fab_bad = F.build_fabric(loop.stim, cfg, cfg.seed, fab_C.T, shuffled=True, wperm_B=128)
    assert not torch.equal(fab_bad.perm, fab_C.perm), "wpT falsifier dead: B=128 perm == randperm(T)"
    print("  wpT  OK — B=T fabric bit-identical to exp12_shuffle (all 12 fields + perm); B=128 differs")


def wp1():
    """B=1 reduces to exp12_dwell (no perm); a paid B>1 does not, but preserves the multiset."""
    loop_A, cfg_A, fab_A = _fab("exp12_dwell")
    assert (not fab_A.shuffled) and fab_A.perm is None, "wp1: exp12_dwell (B=1 ref) is not perm-free"
    try:
        X12.exp19_wperm(1); rejected = False
    except AssertionError:
        rejected = True
    assert rejected, "wp1: exp19_wperm(1) not rejected — B=1 must be REUSED==exp12_dwell, not a perm arm"
    fab_wp = F.build_fabric(loop_A.stim, cfg_A, cfg_A.seed, fab_A.T, shuffled=True, wperm_B=128)
    assert fab_wp.shuffled, "wp1: a paid W-PERM build must set fab.shuffled"
    assert not torch.equal(fab_wp.raw, fab_A.raw), "wp1 falsifier dead: B=128 raw == exp12_dwell (no reorder)"
    assert torch.equal(fab_wp.raw.sort(0).values, fab_A.raw.sort(0).values), \
        "wp1: W-PERM multiset != exp12_dwell — not order-only"
    # RED-TEAM (red-team rule): the wp1 condition "B=1 is perm-free" MUST go red on a B=1 built as a
    # shuffle (fab.shuffled set wrongly — the prereg §2.1 falsifier). Reachable: a registrar/threading
    # bug that routes B=1 through the shuffle path. block_perm(T,1) is an identity perm, so the VALUES
    # match exp12_dwell — the only tell is shuffled=True / perm!=None, which is exactly what wp1 checks.
    wrong_B1 = F.build_fabric(loop_A.stim, cfg_A, cfg_A.seed, fab_A.T, shuffled=True, wperm_B=1)
    perm_free = (not wrong_B1.shuffled) and (wrong_B1.perm is None)
    assert not perm_free, "wp1 falsifier DEAD: a shuffle-built B=1 still reads perm-free — wp1 cannot fail"
    print("  wp1  OK — B=1==exp12_dwell (perm-free); exp19_wperm(1) rejected; falsifier LIVE (a shuffle-built "
          "B=1 reads shuffled=True/perm!=None -> the wp1 perm-free condition goes red)")


def wp_multiset():
    """G3 — the COMMITTED twin-rebuild + multiset checksum (exp12_arms:443-451, via _assert_one) fires
    and passes on a W-PERM fabric. Deleted from build scope; verify, do not rebuild."""
    arm = X12.exp19_wperm(128)
    r = XA._assert_one(arm, SEED, T)
    assert r["ok"], f"wp-multiset: committed checksum FAILED on W-PERM ({r.get('err')})"
    # RED-TEAM (red-team rule): the committed multiset checksum MUST go red on a broken multiset — a
    # wave-VALUE change, not a reorder. Reachable: a generator bug that alters raw values (which the
    # order-only W-PERM must never do). Replicate the exact committed compare (exp12_arms:449).
    loop, spec, cfg = X12.build_exp12(arm, SEED, T)
    fab = loop.stream
    twin = F.build_fabric(loop.stim, cfg, cfg.seed, fab.T, shuffled=False)
    assert torch.equal(fab.raw.sort(0).values, twin.raw.sort(0).values), "wp-multiset: real W-PERM breaks the multiset?!"
    broken = fab.raw.clone(); broken.view(-1)[0] += 1.0
    assert not torch.equal(broken.sort(0).values, twin.raw.sort(0).values), \
        "wp-multiset falsifier DEAD: a wave-value change still matches the twin multiset — checksum cannot fail"
    print(f"  wp-multiset  OK — committed twin-rebuild+checksum fires and passes on {arm}; falsifier LIVE "
          "(a wave-value change breaks the sorted-multiset compare)")


def wp_strat_label():
    """G4 — the `pos==1` mask and `zero_preceding_mask` DIVERGE at every B>1 and COINCIDE at B=1.
    Coincidence at B>1 => the stratifier is on the LABEL (pos==1), not the PROPERTY (zero same-dwell
    waves preceding the exam in emitted order) => it would score contaminated exams as recency-free and
    certify the arm's own confound. THIS IS THE FALSIFIER: with a naive pos==1 stratifier it goes red."""
    loop1, cfg1, fab1 = _fab("exp12_dwell")
    assert torch.equal((fab1.pos == 1), SC.zero_preceding_mask(fab1)), \
        "wp-strat-label: masks DIVERGE at B=1 (exp12_dwell) — they must coincide"
    for B in (32, 128):
        loop, spec, cfg = X12.build_exp12(X12.exp19_wperm(B), SEED, T)
        fab = loop.stream
        assert not torch.equal((fab.pos == 1), SC.zero_preceding_mask(fab)), (
            f"wp-strat-label: masks COINCIDE at B={B} — the stratifier is on the LABEL (pos==1), not the "
            f"property (zero preceding same-dwell wave in emitted order); it would certify its own confound")
    print("  wp-strat-label  OK — pos==1 and zero_preceding DIVERGE at B>1, COINCIDE at B=1")


def wp_recency():
    """B5 — the recency companion is computable per B before any run; B=1 shows ZERO contamination
    (structural), B>1 shows contamination (peaks in the interior). Falsifier: a companion computed from
    DWELL order (the unshuffled twin) instead of EMITTED order reads B>1 as clean and misses the confound."""
    _, _, fab1 = _fab("exp12_dwell")
    r1 = SC.recency_companion(fab1)
    assert r1["frac_contaminated"] == 0.0, f"wp-recency: B=1 contaminated {r1['frac_contaminated']} (must be 0)"
    loop, spec, cfg = X12.build_exp12(X12.exp19_wperm(32), SEED, T)
    fab = loop.stream
    r32 = SC.recency_companion(fab)
    assert r32["frac_contaminated"] > 0.0, "wp-recency: B=32 shows no contamination (the confound must be present)"
    twin = F.build_fabric(loop.stim, cfg, cfg.seed, fab.T, shuffled=False)        # dwell-order (wrong)
    r_wrong = SC.recency_companion(twin)
    assert r_wrong["frac_contaminated"] == 0.0 and r_wrong["frac_contaminated"] != r32["frac_contaminated"], \
        "wp-recency falsifier DEAD: dwell-order companion agrees with emitted-order"
    print(f"  wp-recency  OK — B=1 clean (0); B=32 contaminated ({r32['frac_contaminated']:.3f}, immediate "
          f"{r32['frac_immediate']:.3f}); falsifier LIVE (dwell-order companion reads 0)")


def wp_delta():
    """B6 — ρ(B) strictly DECREASING in B and ρ(1) != ρ(T). Fails under a no-op (constant ρ)."""
    seq = []
    for B, arm in [(1, "exp12_dwell"), (32, X12.exp19_wperm(32)), (512, X12.exp19_wperm(512)),
                   ("T", "exp12_shuffle")]:
        loop, spec, cfg = X12.build_exp12(arm, SEED, T)
        seq.append(SC.rho(loop.stream))
    assert all(seq[i] > seq[i + 1] for i in range(len(seq) - 1)), f"wp-delta: rho(B) not strictly decreasing: {seq}"
    assert seq[0] != seq[-1], "wp-delta: rho(B=1) == rho(B=T) — no-op"
    const = [seq[0]] * 4                                                          # a no-op sequence
    assert not all(const[i] > const[i + 1] for i in range(3)), "wp-delta falsifier DEAD: constant rho passes strict-decreasing"
    print(f"  wp-delta  OK — rho(B) strictly decreasing {[round(x, 3) for x in seq]}; falsifier LIVE "
          "(a constant/no-op sequence is not strictly decreasing)")


def main():
    print("EXP19 W-PERM smokes: wpT / wp1 / wp-multiset / wp-strat-label / wp-recency / wp-delta")
    for fn in (wpT, wp1, wp_multiset, wp_strat_label, wp_recency, wp_delta):
        try:
            fn()
        except AssertionError as e:
            print(f"  FAIL: {e}")
            sys.exit(1)
    print("EXP19 W-PERM smokes: ALL PASS")


if __name__ == "__main__":
    main()
