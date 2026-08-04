"""EXP21 — per-edit diff-scope + actual-arm B11 (prereg §2.5, gate G1).

Reuses the committed exp19_diffscope machinery (symbols / blast_radius / baseline reads) via
module-attribute injection — the EXP20 precedent — with THIS experiment's per-edit config:

  BASELINE = commit 19a8fbf (the ratified-prereg commit, containing NO EXP21 implementation —
  prereg §2.5: "not an earlier experiment's baseline and not an uncommitted working tree").

  WHITELIST = the §9.2 shared-file fence with EMPTY added/changed sets on every file: the EXP21
  blast radius touches NOTHING in the learner/generator chain; every symbol must be
  byte-identical to baseline. The new exp21_* files are additive and are checked by the
  repo-layer path scan (only enumerated EXP21 paths may differ from baseline).

  B11 RUNTIME layer, BOTH actual arms (§2.5): EXP12Loop (ON) and EXP21TeachingOffLoop (OFF)
  must each resolve `step` through the MRO to the committed `Stage0Loop.step`, byte-for-byte
  vs baseline; no class below Stage0Loop may own a `step` override. Red-teamed with planted
  overrides on BOTH classes; restoration must return the fence to green.
"""

from __future__ import annotations

import inspect
import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import exp19_diffscope as DS                                   # noqa: E402  (committed machinery)

BASELINE21 = "19a8fbf"             # the ratified-prereg commit (§2.5)

WHITELIST21 = {
    "../04_stage0_mvp/loop.py": dict(added=set(), changed=set()),
    "sculpt_loop.py":           dict(added=set(), changed=set()),
    "exp08_arms.py":            dict(added=set(), changed=set()),
    "exp12_arms.py":            dict(added=set(), changed=set()),
    "exp12_fabric.py":          dict(added=set(), changed=set()),
    "exp14_arms.py":            dict(added=set(), changed=set()),
}

# repo-layer blast radius: the ONLY paths that may differ from the baseline commit
ALLOWED_PREFIXES = (
    "docs/EXP21_",
    "docs/FABLE_EXP21_",
    "experiments/05_attention_sculpting/exp21_",
    "experiments/05_attention_sculpting/exp08/exp21/",
)


def _inject():
    saved = (DS.BASELINE_COMMIT, DS.WHITELIST)
    DS.BASELINE_COMMIT, DS.WHITELIST = BASELINE21, WHITELIST21
    return saved


def _restore(saved):
    DS.BASELINE_COMMIT, DS.WHITELIST = saved


def shared_chain_scan(perturb=None) -> dict:
    """Symbol-scoped byte-identity of every fenced file vs the prereg baseline."""
    saved = _inject()
    try:
        return DS.run(perturb=perturb)
    finally:
        _restore(saved)


def repo_blast_radius() -> dict:
    """Every tracked path changed since the baseline must be an enumerated EXP21 path."""
    r = subprocess.run(["git", "diff", "--name-only", BASELINE21], cwd=_HERE,
                       capture_output=True, text=True, timeout=20)
    r2 = subprocess.run(["git", "diff", "--name-only", "--cached", BASELINE21], cwd=_HERE,
                        capture_output=True, text=True, timeout=20)
    changed = sorted(set(filter(None, r.stdout.splitlines() + r2.stdout.splitlines())))
    out_of_scope = [p for p in changed if not any(p.startswith(a) for a in ALLOWED_PREFIXES)]
    return dict(changed=changed, out_of_scope=out_of_scope, ok=not out_of_scope)


def fence21(cls, planted_override=None) -> list:
    """B11 runtime fence on ONE actual arm class (mirrors the committed learner_fence, ledger
    32, parameterized to the class): step must be the baseline Stage0Loop.step through the MRO."""
    saved = _inject()
    violations = []
    if planted_override is not None:
        cls.step = planted_override
    try:
        base = [c for c in cls.__mro__ if c.__name__ == "Stage0Loop"]
        if not base:
            violations.append(("MRO", f"Stage0Loop missing from {cls.__name__}.__mro__"))
        else:
            for c in cls.__mro__:
                if c is base[0]:
                    break
                if "step" in vars(c):
                    violations.append(("OVERRIDE", f"{c.__name__} defines its own step — the "
                                                   "learner is no longer Stage0Loop.step"))
        try:
            live = inspect.getsource(cls.step)
        except (OSError, TypeError):
            live = "<unreadable planted object>"
        want = DS.symbols(DS._baseline_src("../04_stage0_mvp/loop.py"),
                          "loop.py")["Stage0Loop.step"] + "\n"
        if live != want:
            violations.append(("CHANGED", f"live {cls.__name__}.step source != baseline "
                                          f"Stage0Loop.step ({BASELINE21})"))
    finally:
        if planted_override is not None:
            del cls.step
        _restore(saved)
    return violations


def main() -> dict:
    import torch
    torch.set_num_threads(1)
    import exp12_arms as X12
    import exp21_teaching as T21

    out = dict(gate="G1", executor="exp21_diffscope.main", baseline=BASELINE21,
               observed_red={}, checks={})

    # --- observed reds FIRST (§7 row G1) ---
    def _planted(self, *a, **k):                              # the anti-forward nightmare
        return None

    v_off = fence21(T21.EXP21TeachingOffLoop, planted_override=_planted)
    assert v_off, "G1 fixture off_planted_step_override: fence blind — dead gate, HALT"
    post = fence21(T21.EXP21TeachingOffLoop)
    assert not post, f"OFF fence still firing after plant removal: {post}"
    out["observed_red"]["off_planted_step_override"] = dict(
        red=True, kinds=[k for k, _ in v_off], restored_green=True)

    v_on = fence21(X12.EXP12Loop, planted_override=_planted)
    assert v_on, "G1 fixture on_planted_step_override: fence blind — dead gate, HALT"
    post = fence21(X12.EXP12Loop)
    assert not post, f"ON fence still firing after plant removal: {post}"
    out["observed_red"]["on_planted_step_override"] = dict(
        red=True, kinds=[k for k, _ in v_on], restored_green=True)

    rt = shared_chain_scan(perturb=(
        "../04_stage0_mvp/loop.py",
        "L = gain * l_pam + self.pin.alpha_spread * l_spread + l_jepa + vis_pen + pam_pen",
        "L = gain * l_pam + self.pin.alpha_spread * l_spread + l_jepa + vis_pen + 2 * pam_pen"))
    viols = rt["../04_stage0_mvp/loop.py"]["violations"]
    assert viols, "G1 fixture shared_loop_edit: diff-scope blind to a loss-chain edit — HALT"
    out["observed_red"]["shared_loop_edit"] = dict(red=True, violations=viols[:4])

    rt2 = shared_chain_scan(perturb=(
        "exp12_arms.py",
        "raw = fab.raw[dt:dt + 1]",
        "raw = fab.raw[dt:dt + 1] * 1.0000001"))
    viols2 = rt2["exp12_arms.py"]["violations"]
    assert viols2, "G1 fixture shared_exp12_edit: diff-scope blind to a delivery edit — HALT"
    out["observed_red"]["shared_exp12_edit"] = dict(red=True, violations=viols2[:4])

    # --- the real fence, green ---
    scan = shared_chain_scan()
    bad = {n: r["violations"] for n, r in scan.items() if r["violations"]}
    assert not bad, f"G1 SHARED-CHAIN VIOLATIONS: {bad} — HALT"
    out["checks"]["shared_chain_byte_identical"] = dict(
        ok=True, files={n: dict(added=r["added"], changed=r["changed"], removed=r["removed"])
                        for n, r in scan.items()})

    radius = repo_blast_radius()
    assert radius["ok"], f"G1 OUT-OF-SCOPE tracked changes: {radius['out_of_scope']} — HALT"
    out["checks"]["repo_blast_radius"] = radius

    for label, cls in (("on", X12.EXP12Loop), ("off", T21.EXP21TeachingOffLoop)):
        v = fence21(cls)
        assert not v, f"G1 B11 fence ({label}): {v} — HALT"
        mro = [c.__name__ for c in cls.__mro__]
        step_owner = next(c.__name__ for c in cls.__mro__ if "step" in vars(c))
        assert step_owner == "Stage0Loop"
        out["checks"][f"b11_{label}"] = dict(ok=True, mro=mro, step_owner=step_owner)

    outdir = _HERE / "exp08" / "exp21"
    outdir.mkdir(parents=True, exist_ok=True)
    T21.write_gate_artifact(outdir / "exp21_g1_diffscope.json", out)
    T21.gatelog_append(dict(gate="G1", outcome="PASS", executor="exp21_diffscope.main",
                            reds=sorted(out["observed_red"]), checks=sorted(out["checks"])))
    print("G1 PASS:", sorted(out["checks"]), "reds:", sorted(out["observed_red"]))
    return out


if __name__ == "__main__":
    main()
