"""exp19_g0b_genregress.py — G0b GENERATOR REGRESSION (REUSED-class, deterministic replay).

Ruled by Jason 2026-07-13 (ledger 29). Runs BEFORE any W-PERM code (B1) lands. The wperm_B kwarg
edits the shared generator (exp12_fabric/exp12_arms); ~15 files import it. wp1/wpT cover only
W-PERM's two endpoints — this gate covers the other campaigns.

--- v1 VOID (ledger 31, CC), superseded in place ---------------------------------------------------
v1 compared ONLY F.fabric_manifest — PERMUTATION-INVARIANT summary stats (order-blind counts; asserts
on the unshuffled twin). It was blind to any change in the realized permutation of the one shuffled
arm — the exact failure it exists to catch. Ruled VOID. "A gate passed for an unverifiable reason is
a HALT, not a pass."

--- v2 hardening (ledger 31 fixes, Jason panel MUST-FIXes 2026-07-14) -------------------------------
THE GATE = CONTENT DIGEST. content_digest(): sha256 over the 12 permuted fields + dwell_k + perm,
fixed field order / dtype / little-endian bytes. ORDER- and CONTENT-sensitive. Red-teamed in
exp19_g0b_redteam.py (fires on flip, on seed-bump, on a raw-content perturbation; manifest blind to
all three; the red-team fabric is bound == the real loop.stream).

COMPANION (kept, NOT the gate) = F.fabric_manifest `fabric` + `independence_asserts` vs the committed
.manifest.json. Order-invariant, so genuinely sensitive only for the UNSHUFFLED arms; ties the current
generator to the committed order-invariant content.

FAIL-CLOSED + ANCHOR-PROVENANCE (panel MUST-FIXes):
  * A non-baseline run REQUIRES a complete baseline reference (a content_digest for every cell). If it
    is absent or incomplete, HALT(setup, exit 2) — NEVER pass on the companion alone (that is v1).
  * Each artifact stamps gen_source_sha = sha256 of the generator SOURCE (exp12_fabric.py +
    exp12_arms.py). The edited run asserts ref.gen_source_sha != this run's — else the baseline was
    computed from the SAME source and digest==baseline is vacuous (HALT). Committed-code provenance.

SCOPE (honest, panel should-fix): the gate proves the wperm_B edit INERT vs the immediately-pre-edit
generator (the baseline is a worktree at the pre-B1 commit; digest(baseline)==digest(edited)). It does
NOT re-anchor the shuffled arm's realized ORDER to the original certification commit (no committed
content_digest exists there; the committed manifest is order-blind). It fingerprints the FABRIC; the
eval-path (EXP12Stimulus.raw_clean / self.centre) and spread-loss raw() generator behaviour are NOT
fingerprinted by the digest — their integrity is carried STRUCTURALLY by the generator diff-scope
(`exp19_diffscope.py`, Jason ruling 1b): every generator symbol outside the wperm_B blast radius must
be byte-identical to the pre-edit baseline. DIGEST = fabric; DIFF-SCOPE = generator-source confinement
(a sampled behavioural probe would catch only what it sampled — G0b v1's species). Both stand at every
generator edit.

PASSES.
  baseline (UNEDITED generator, git worktree at the pre-B1 commit) — reference digests + companion.
  edited   (this tree) — digest == baseline (GATE), manifest == committed (companion), provenance bound.

Any divergence (digest OR companion) => HALT. Writes exp08/exp19_g0b_genregress_<tag>.json.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import torch
torch.set_num_threads(1)

import exp12_fabric as F
import exp12_arms as X12
import exp14_arms as XA

OUT = XA.OUTDIR
HERE = Path(__file__).resolve().parent
FAB_PAD = 8
PERM_FIELDS = ("a", "b", "member", "cat", "dwell_id", "pos", "mask_slot",
               "is_exam", "is_probe_exam", "nuis", "bg", "raw")     # the 12 permuted fields
DIGEST_FIELDS = PERM_FIELDS + ("dwell_k", "perm")
GEN_SOURCES = ("exp12_fabric.py", "exp12_arms.py")                  # the shared generator source

CELLS = [
    ("exp12_dwell",         "exp14_exp12_dwell_s{s}_verdict",                [0]),
    ("exp12_shuffle",       "exp14_exp12_shuffle_s{s}_verdict",             [0]),
    ("exp12_dwell_scatter", "exp14_exp12_dwell_scatter_s{s}_scatterverdict", [0]),
    ("exp12_dwell_orbit",   "exp14_exp12_dwell_orbit_s{s}_exp17verdict",    [0]),
    ("exp12_dwell_expomid", "exp14_exp12_dwell_expomid_s{s}_exp16verdict",  [0]),
]


def content_digest(fab) -> str:
    """sha256 over the 12 permuted fields + dwell_k + perm, fixed order, tagged by field/dtype/shape,
    bytes forced little-endian. ORDER- and CONTENT-sensitive; fires on any permutation OR wave-content
    change — the manifest's blind spot. Reused by the red-team and bound == the real loop.stream."""
    h = hashlib.sha256()
    for name in DIGEST_FIELDS:
        t = getattr(fab, name, None)
        if t is None:
            h.update(f"|{name}=None".encode())
            continue
        a = t.detach().cpu().contiguous().numpy()
        a = a.astype(a.dtype.newbyteorder("<"), copy=False)
        h.update(f"|{name}:{a.dtype.str}:{tuple(a.shape)}=".encode())
        h.update(a.tobytes())
    return h.hexdigest()


def _gen_source_sha() -> str:
    """sha256 of the generator SOURCE as it exists at gate-run time — the anchor-provenance binding.
    Baseline and edited MUST hash differently, else the digest comparison is vacuous."""
    h = hashlib.sha256()
    for name in GEN_SOURCES:
        h.update(f"|{name}=".encode())
        h.update((HERE / name).read_bytes())
    return h.hexdigest()


def _git_head():
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE,
                           capture_output=True, text=True, timeout=10)
        return (r.stdout.strip() or None)
    except Exception:
        return None


def _canon(d):
    return json.dumps(d, sort_keys=True, default=str)


def _build(arm, seed, target_T):
    loop, spec, cfg = X12.build_exp12(arm, seed, target_T - FAB_PAD)
    fab = loop.stream
    if fab.T != target_T:
        raise RuntimeError(f"T-setup: rebuilt fabric.T {fab.T} != committed {target_T} for {arm}")
    if fab.shuffled:
        twin = F.build_fabric(loop.stim, cfg, seed, fab.T, probe_rate=X12.PROBE_RATE_STAGE1,
                              shuffled=False, uniform_mask=spec.get("uniform_mask", False),
                              word_ref=spec.get("word_ref", False))
        asr = F.fabric_asserts(twin, cfg)
    else:
        asr = F.fabric_asserts(fab, cfg)
    return fab, F.fabric_manifest(fab, loop.stim, cfg, asr)


def _load_reference(src_sha):
    """FAIL-CLOSED: a non-baseline run MUST have a complete, provenance-distinct reference, else the
    content-digest gate is disabled and only the order-blind companion remains (the v1 VOID). Returns
    (ref_map, ref_meta) or exits 2 with a distinct SETUP message (never a false pass, never a
    misattributed regression HALT)."""
    ref_path = OUT / "exp19_g0b_genregress_baseline.json"
    if not ref_path.exists():
        print(f"HALT(setup, exit 2) — no baseline reference at {ref_path}. The content-digest gate "
              f"cannot run without the UNEDITED-generator reference. Refusing to pass on the companion "
              f"alone — that is the v1 order-blind VOID. Run 'baseline' in a git worktree at the pre-edit "
              f"commit and place its exp19_g0b_genregress_baseline.json here.")
        sys.exit(2)
    doc = json.loads(ref_path.read_text())
    ref = {(c["arm"], c["seed"]): c["content_digest"] for c in doc["cells"] if "content_digest" in c}
    need = [(a, s) for a, _, ss in CELLS for s in ss]
    missing = [k for k in need if k not in ref]
    if missing:
        print(f"HALT(setup, exit 2) — baseline reference incomplete/wrong-schema: no content_digest for "
              f"{missing} (a stale v1 baseline yields an EMPTY reference). This is NOT a regression; "
              f"regenerate the baseline. Refusing companion-only pass.")
        sys.exit(2)
    ref_src = doc.get("gen_source_sha")
    if ref_src is None:
        print("HALT(setup, exit 2) — baseline has no gen_source_sha; cannot bind the anchor to a "
              "committed generator source (anchor-provenance rule).")
        sys.exit(2)
    if ref_src == src_sha:
        print("HALT(setup, exit 2) — VACUOUS baseline: its gen_source_sha == this run's, i.e. the "
              "reference was computed from the SAME generator source (a baseline generated from the "
              "edited tree). digest==baseline would prove nothing. Regenerate from the UNEDITED "
              "(pre-edit) generator.")
        sys.exit(2)
    return ref, dict(gen_source_sha=ref_src, git_head=doc.get("git_head"), tag=doc.get("tag"))


def main(tag):
    src_sha = _gen_source_sha()
    head = _git_head()
    ref, ref_meta = (None, None) if tag == "baseline" else _load_reference(src_sha)

    results, gate_fail, companion_fail, setup_err = [], False, False, False
    for arm, tmpl, seeds in CELLS:
        for s in seeds:
            base = tmpl.format(s=s)
            mpath = OUT / (base + ".manifest.json")
            if not mpath.exists():
                results.append(dict(arm=arm, seed=s, status="NO_COMMITTED_MANIFEST", file=base))
                setup_err = True
                continue
            committed = json.loads(mpath.read_text())
            try:
                fab, man = _build(arm, s, committed["fabric"]["T"])
            except RuntimeError as e:
                results.append(dict(arm=arm, seed=s, status="SETUP_ERROR", err=str(e)))
                setup_err = True
                continue
            dig = content_digest(fab)
            fab_ok = _canon(man["fabric"]) == _canon(committed["fabric"])
            asr_ok = _canon(man["independence_asserts"]) == _canon(committed["independence_asserts"])
            companion_ok = fab_ok and asr_ok
            companion_fail |= not companion_ok
            row = dict(arm=arm, seed=s, T=committed["fabric"]["T"], content_digest=dig,
                       manifest_fabric_match=fab_ok, manifest_asserts_match=asr_ok,
                       companion_ok=companion_ok, shuffled=bool(fab.shuffled))
            if ref is not None:
                dig_ok = ref.get((arm, s)) == dig            # THE GATE (ref guaranteed complete)
                gate_fail |= not dig_ok
                row["digest_match"] = dig_ok
                verdict = "OK" if (dig_ok and companion_ok) else \
                          ("DIGEST-DIVERGENCE" if not dig_ok else "companion-only-divergence")
            else:
                row["digest_match"] = None
                verdict = "REF" if companion_ok else "companion-divergence"
            results.append(row)
            print(f"  G0b {arm} s{s} (shuffled={bool(fab.shuffled)}): digest={dig[:16]}.. "
                  f"digest_match={row['digest_match']} companion={companion_ok} -> {verdict}")

    all_pass = (not setup_err and not companion_fail and (tag == "baseline" or not gate_fail))
    out = dict(gate="G0b generator regression v2 (content-digest GATE + manifest companion, fail-closed)",
               tag=tag, spec_hash=XA.C.spec_hash(), gen_source_sha=src_sha, git_head=head,
               reference=ref_meta, reference_used=bool(ref is not None),
               supersedes="v1 manifest-only comparator (VOID, ledger 31 — permutation-invariant)",
               cells=results, all_pass=bool(all_pass),
               gate_divergence=bool(gate_fail), companion_divergence=bool(companion_fail),
               setup_error=bool(setup_err))
    (OUT / f"exp19_g0b_genregress_{tag}.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"\nG0b [{tag}] all_pass={all_pass} gate_div={gate_fail} companion_div={companion_fail} "
          f"setup_err={setup_err} src_sha={src_sha[:12]}.. head={head[:8] if head else None} "
          f"(reference={'yes' if ref is not None else 'NONE (baseline)'})")
    if ref is not None and gate_fail:
        print("HALT — GENERATOR REGRESSION: a certified fabric's CONTENT/ORDER changed (digest).")
        sys.exit(1)
    if companion_fail:
        print("HALT — companion divergence: a fabric fingerprint no longer matches the committed manifest.")
        sys.exit(1)
    if setup_err:
        print("SETUP INCOMPLETE — fix the harness before trusting the gate.")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "baseline")
