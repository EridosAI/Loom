"""exp20_diffscope.py — per-edit diff-scope config for the EXP20 U-BUF seam (prereg §2/§7; the
per-edit-config rule born at exp19_diffscope).

Reuses exp19_diffscope's machinery (symbols / blast_radius / learner_fence — construction, not
judgment) with THIS edit's config injected: fresh BASELINE_COMMIT = the prereg commit (the last
committed generator before the U-BUF seam), WHITELIST = U-BUF's own symbols only, learner chain
EMPTY-SET (B11 both layers unchanged and re-asserted here, planted-red per invocation).

Whitelist notes:
- exp12_fabric.py <module-level> is whitelisted ONLY for the SEED_UBUF constant (the conditional-
  registration seed, house style puts substream seeds at module level); the red-team below proves
  out-of-scope symbol changes in the same file still fire.
- exp14_arms.py joins the scanned set for this edit (run_exp14_arm gained the E-B onset read);
  everything else in it must be byte-identical to baseline.
"""
import sys

import exp19_diffscope as D

BASELINE_COMMIT = "0741717"          # the EXP20 prereg commit — last committed tree before the seam
WHITELIST = {
    "exp12_fabric.py": dict(added={"ubuf_map"}, changed={"build_fabric", "<module-level>"}),
    "exp12_arms.py":   dict(added={"exp20_ubuf"},
                            changed={"build_exp12", "EXP12Loop._make_stream",
                                     "EXP12Loop.build_cells"}),
    "exp14_arms.py":   dict(added=set(), changed={"run_exp14_arm"}),
    # B11 REPO layer — the learner chain is OUTSIDE the U-BUF blast radius entirely (5.3-SAT-2's
    # enforcement consequence: the buffer lives in the wave-delivery path, never in step)
    "sculpt_loop.py":  dict(added=set(), changed=set()),
    "exp08_arms.py":   dict(added=set(), changed=set()),
    "../04_stage0_mvp/loop.py": dict(added=set(), changed=set()),
}


def _inject():
    D.BASELINE_COMMIT = BASELINE_COMMIT
    D.WHITELIST = WHITELIST


def run(perturb=None):
    _inject()
    return D.run(perturb=perturb)


def learner_fence(planted_override=None):
    _inject()
    return D.learner_fence(planted_override=planted_override)


def main():
    _inject()
    print(f"EXP20 diff-scope vs baseline {BASELINE_COMMIT} (whitelist = the U-BUF blast radius)")
    any_viol = False
    for name, r in run().items():
        print(f"  {name}: added={r['added']} changed={r['changed']} removed={r['removed']}")
        for kind, sym in r["violations"]:
            print(f"    VIOLATION {kind} {sym} — OUT OF BLAST RADIUS"); any_viol = True
    if any_viol:
        print("HALT — the U-BUF edit is NOT confined to its blast radius.")
        sys.exit(1)
    print("  PASS — every symbol outside the U-BUF whitelist is byte-identical to baseline.\n")

    print("RED-TEAM 1 — out-of-scope generator change (the eval-path perturbation) must fire:")
    rt = run(perturb=("exp12_fabric.py",
                      "self.centre = self.centre_id + (self.bg_const @ self.bg_axes)",
                      "self.centre = self.centre_id + 2 * (self.bg_const @ self.bg_axes)"))
    if not rt["exp12_fabric.py"]["violations"]:
        print("RED-TEAM FAILED — out-of-scope generator change not flagged. Dead code."); sys.exit(1)
    print(f"    fires: {rt['exp12_fabric.py']['violations']}")

    print("RED-TEAM 2 — out-of-scope exp14_arms change (scorer-side perturbation) must fire:")
    rt2 = run(perturb=("exp14_arms.py",
                       "def _proposed_conversion(cols) -> bool:",
                       "def _proposed_conversion(cols, _x=0) -> bool:"))
    if not rt2["exp14_arms.py"]["violations"]:
        print("RED-TEAM FAILED — out-of-scope exp14_arms change not flagged. Dead code."); sys.exit(1)
    print(f"    fires: {rt2['exp14_arms.py']['violations']}")

    print("\nB11 LEARNER FENCE (runtime) — live EXP12Loop.step vs baseline Stage0Loop.step:")
    v = learner_fence()
    if v:
        for kind, msg in v:
            print(f"    VIOLATION {kind}: {msg}")
        print("HALT — the LIVE learner is not the baseline learner."); sys.exit(1)
    print("    PASS — live step IS baseline Stage0Loop.step (byte-for-byte, MRO clean).")

    def _planted(self, *a, **k):
        return None
    rtv = learner_fence(planted_override=_planted)
    if not rtv:
        print("RED-TEAM FAILED — planted runtime step override not flagged. Dead code."); sys.exit(1)
    post = learner_fence()
    if post:
        print(f"RED-TEAM RESTORE FAILED: {post}"); sys.exit(1)
    print(f"    RED-TEAM PASS — planted override fires ({[k for k, _ in rtv]}), clean after restore.")


if __name__ == "__main__":
    main()
