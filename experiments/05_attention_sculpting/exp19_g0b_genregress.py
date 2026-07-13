"""exp19_g0b_genregress.py — G0b GENERATOR REGRESSION (REUSED-class, deterministic replay).

Ruled by Jason 2026-07-13 (ledger 29). Runs BEFORE any W-PERM code (B1) lands. The wperm_B kwarg
edits the shared generator (exp12_fabric); fifteen files import it. wp1/wpT cover only W-PERM's two
endpoints — this gate covers the other campaigns. A perturbed generator silently invalidates every
certified record in the campaign and nothing else would tell us.

WHAT IT DOES. Through the original fabric-build entry point (X12.build_exp12 — the exact path
_assert_one / run_exp14_arm build on), rebuild the fabric for one representative arm of every campaign
that imports exp12_fabric/exp12_arms, recompute F.fabric_manifest, and assert its deterministic
fingerprint (the `fabric` sub-dict + `independence_asserts`) is BYTE-IDENTICAL to the committed
.manifest.json. Replay only; NO training; no new science; near-zero cost.

  exp12_dwell   (EXP14 A, certified 0/8) — the house's own G1a form
  exp12_shuffle (EXP14 C, certified 5/8)
  exp12_dwell_scatter (SCATTER) · exp12_dwell_orbit (EXP17) · exp12_dwell_expomid (EXP16)

TWO PASSES.
  baseline (this file, UNEDITED generator) — proves the committed manifests still reproduce at HEAD;
           a false-HALT guard. If baseline itself diverges, that is a pre-existing determinism/env
           issue, surfaced separately — NOT a W-PERM matter.
  edited   (after the wperm_B kwarg lands) — must STILL match => the edit is inert.
  baseline == committed  AND  edited == committed  =>  the edit is inert (transitively).

Any divergence => HALT. Writes exp08/exp19_g0b_genregress_<tag>.json; exit 1 on any divergence.
"""
import json
import sys
from pathlib import Path

import torch
torch.set_num_threads(1)

import exp12_fabric as F
import exp12_arms as X12
import exp14_arms as XA

OUT = XA.OUTDIR
FAB_PAD = 8                                           # fabric.T = build_exp12 steps + 8 (house standard)

# (registry arm, committed-manifest basename template, seeds) — one representative per campaign;
# the two certified endpoints get their full committed seed set.
CELLS = [
    ("exp12_dwell",         "exp14_exp12_dwell_s{s}_verdict",                [0]),
    ("exp12_shuffle",       "exp14_exp12_shuffle_s{s}_verdict",             [0]),
    ("exp12_dwell_scatter", "exp14_exp12_dwell_scatter_s{s}_scatterverdict", [0]),
    ("exp12_dwell_orbit",   "exp14_exp12_dwell_orbit_s{s}_exp17verdict",    [0]),
    ("exp12_dwell_expomid", "exp14_exp12_dwell_expomid_s{s}_exp16verdict",  [0]),
]


def _canon(d):
    return json.dumps(d, sort_keys=True, default=str)


def _fingerprint(arm, seed, target_T):
    """Rebuild the fabric via the original entry point; return F.fabric_manifest (fabric + asserts).
    Shuffled arms assert on the unshuffled twin — the exact run_exp14_arm / _assert_one path."""
    loop, spec, cfg = X12.build_exp12(arm, seed, target_T - FAB_PAD)   # no stepping
    fab = loop.stream
    if fab.T != target_T:
        raise RuntimeError(f"T-setup: rebuilt fabric.T {fab.T} != committed {target_T} "
                           f"(pad assumption wrong for {arm}) — reproduction bug, not a generator divergence")
    if fab.shuffled:
        twin = F.build_fabric(loop.stim, cfg, seed, fab.T, probe_rate=X12.PROBE_RATE_STAGE1,
                              shuffled=False, uniform_mask=spec.get("uniform_mask", False),
                              word_ref=spec.get("word_ref", False))
        asr = F.fabric_asserts(twin, cfg)
    else:
        asr = F.fabric_asserts(fab, cfg)
    return F.fabric_manifest(fab, loop.stim, cfg, asr)


def main(tag):
    results, divergence, setup_err = [], False, False
    for arm, tmpl, seeds in CELLS:
        for s in seeds:
            base = tmpl.format(s=s)
            mpath = OUT / (base + ".manifest.json")
            if not mpath.exists():
                results.append(dict(arm=arm, seed=s, status="NO_COMMITTED_MANIFEST", file=base))
                setup_err = True
                print(f"  G0b {arm} s{s}: NO_COMMITTED_MANIFEST ({base})")
                continue
            committed = json.loads(mpath.read_text())
            try:
                got = _fingerprint(arm, s, committed["fabric"]["T"])
            except RuntimeError as e:
                results.append(dict(arm=arm, seed=s, status="SETUP_ERROR", err=str(e)))
                setup_err = True
                print(f"  G0b {arm} s{s}: SETUP_ERROR — {e}")
                continue
            fab_ok = _canon(got["fabric"]) == _canon(committed["fabric"])
            asr_ok = _canon(got["independence_asserts"]) == _canon(committed["independence_asserts"])
            ok = fab_ok and asr_ok
            divergence |= not ok
            results.append(dict(arm=arm, seed=s, T=committed["fabric"]["T"],
                                fabric_match=fab_ok, asserts_match=asr_ok, ok=ok))
            print(f"  G0b {arm} s{s} (T={committed['fabric']['T']}): "
                  f"fabric={fab_ok} asserts={asr_ok} -> {'OK' if ok else 'DIVERGENCE'}")
    out = dict(gate="G0b generator regression (REUSED-class, deterministic replay)", tag=tag,
               spec_hash=XA.C.spec_hash(), cells=results,
               all_pass=bool(not divergence and not setup_err),
               divergence=bool(divergence), setup_error=bool(setup_err))
    (OUT / f"exp19_g0b_genregress_{tag}.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"\nG0b [{tag}] all_pass={out['all_pass']} divergence={divergence} setup_error={setup_err}")
    if divergence:
        print("HALT — GENERATOR REGRESSION: a certified fabric no longer reproduces.")
        sys.exit(1)
    if setup_err:
        print("SETUP INCOMPLETE — fix the harness (not a generator divergence) before trusting the gate.")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "baseline")
