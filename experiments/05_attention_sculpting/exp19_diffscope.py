"""exp19_diffscope.py — structural GENERATOR diff-scope (Jason ruling 1, 2026-07-14).

The wperm_B edit touches the SHARED generator (exp12_fabric.py / exp12_arms.py). G0b's content digest
is scoped to the FABRIC; the eval-path (EXP12Stimulus.self.centre / raw_clean) and the spread-loss
raw() generator behaviour are NOT fingerprinted by the digest. Their integrity is carried HERE,
STRUCTURALLY: every top-level symbol and class method of the generator OUTSIDE a per-edit whitelist
MUST be byte-identical to the pre-edit baseline. This catches ANY out-of-blast-radius change — including
ones nobody enumerated — where a sampled behavioural probe (G0b v1's species) catches only what it
looked at. Construction, not judgment.

B11 LIVES HERE (ledger 32; prereg §6 item 1) — the LEARNER fence, two layers:
  REPO layer: the learner chain (loop.py / sculpt_loop.py / exp08_arms.py) enters the WHITELIST with EMPTY
    added/changed sets = the W-PERM blast radius touches NOTHING there; every symbol must be byte-identical
    to baseline. (§6 names sculpt_loop.py / EXP08Loop / EXP12Loop.step; the effective `step` actually
    resolves through the MRO to Stage0Loop.step in exp04's loop.py — a file-hash on the three NAMED files
    would fence the wrong file, which is exactly why ledger 32 demanded symbol-scoped.)
  RUNTIME layer: learner_fence() asserts inspect.getsource(EXP12Loop.step) on the LIVE class equals the
    BASELINE_COMMIT source of Stage0Loop.step, and that no class below Stage0Loop in the MRO grew its own
    `step` override. Catches loaded-module drift / monkeypatching that a repo diff cannot see.
  Red-teamed like the generator scope: a planted runtime `step` override must FIRE the fence.

Red-teamed (the red-team rule, CORRIDOR Conduct): a synthetic out-of-scope change — the review panel's
own self.centre eval-path perturbation — is shown to trip a CHANGED violation. A diff-scope that has
never flagged an out-of-scope change is asserted, not tested.

Per-edit config: BASELINE_COMMIT (the last committed generator before this edit) + WHITELIST.
"""
import ast
import inspect
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE_COMMIT = "9429792"          # pre-B1: the unedited generator this edit is measured against

# Symbols the W-PERM edit is ALLOWED to add or change. EVERYTHING ELSE must be byte-identical.
WHITELIST = {
    "exp12_fabric.py": dict(added={"block_perm"}, changed={"build_fabric"}),
    # `_dec_cat` (added) + `_eval_column` (changed) = the ratified EXP19 free SCORER field `dec_cat`
    # (Jason 2026-07-15): a col-only nearest-centroid category decode — NO generator/learner touch, no
    # RNG/loss/optimizer/gen_state (anchor re-verified: .ckpt_read.pt bit-identical). Learner integrity
    # is separately fenced by the symbol-scoped EXP12Loop.step check.
    "exp12_arms.py":   dict(added={"exp19_wperm", "_dec_cat"},
                            changed={"build_exp12", "EXP12Loop._make_stream", "_eval_column"}),
    # B11 REPO layer — the learner chain is OUTSIDE the W-PERM blast radius entirely: zero additions, zero
    # changes; every symbol byte-identical to baseline. loop.py is exp04's foundation (Stage0Loop.step = the
    # effective optimizer step of every arm); a legitimate future edit there updates this whitelist AT that
    # edit, per the per-edit-config rule.
    "sculpt_loop.py":  dict(added=set(), changed=set()),
    "exp08_arms.py":   dict(added=set(), changed=set()),
    "../04_stage0_mvp/loop.py": dict(added=set(), changed=set()),
}


def symbols(src, filename):
    """qualified_name -> exact source segment (decorators included), for every top-level function, each
    class method, each class's <header> (decl line) and <body> (non-method statements), and one
    <module-level> bucket (imports / constants). Whitespace BETWEEN symbols is ignored; symbol bodies
    are byte-exact."""
    tree = ast.parse(src, filename=filename)
    lines = src.splitlines()

    def seg(node):
        start = node.decorator_list[0].lineno if getattr(node, "decorator_list", None) else node.lineno
        return "\n".join(lines[start - 1:node.end_lineno])

    out, modlevel = {}, []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out[node.name] = seg(node)
        elif isinstance(node, ast.ClassDef):
            hstart = node.decorator_list[0].lineno if node.decorator_list else node.lineno
            out[f"{node.name}.<header>"] = "\n".join(lines[hstart - 1:node.body[0].lineno - 1])
            nonmethod = []
            for m in node.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    out[f"{node.name}.{m.name}"] = seg(m)
                else:
                    nonmethod.append(seg(m))
            out[f"{node.name}.<body>"] = "\n".join(nonmethod)
        else:
            modlevel.append(seg(node))
    out["<module-level>"] = "\n".join(modlevel)
    return out


def blast_radius(baseline_src, edited_src, filename):
    wl = WHITELIST[filename]
    b, e = symbols(baseline_src, filename), symbols(edited_src, filename)
    added = set(e) - set(b)
    removed = set(b) - set(e)
    changed = {k for k in (set(b) & set(e)) if b[k] != e[k]}
    violations = ([("ADDED", k) for k in sorted(added) if k not in wl["added"]] +
                  [("REMOVED", k) for k in sorted(removed)] +
                  [("CHANGED", k) for k in sorted(changed) if k not in wl["changed"]])
    return dict(added=sorted(added), removed=sorted(removed), changed=sorted(changed),
                violations=violations)


def _baseline_src(name):
    rel = subprocess.run(["git", "ls-files", "--full-name", name], cwd=HERE,
                         capture_output=True, text=True, timeout=10).stdout.strip()
    r = subprocess.run(["git", "show", f"{BASELINE_COMMIT}:{rel}"], cwd=HERE,
                       capture_output=True, text=True, timeout=10)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(f"cannot read baseline {BASELINE_COMMIT}:{rel}: {r.stderr}")
    return r.stdout


def run(perturb=None):
    """perturb=(filename, old, new): inject an out-of-scope change into the edited source (red-team)."""
    results = {}
    for name in WHITELIST:
        edited = (HERE / name).read_text()
        if perturb and perturb[0] == name:
            assert perturb[1] in edited, f"red-team anchor not found in {name}"
            edited = edited.replace(perturb[1], perturb[2], 1)
        results[name] = blast_radius(_baseline_src(name), edited, name)
    return results


def learner_fence(planted_override=None) -> list:
    """B11 RUNTIME layer (ledger 32): the LIVE learner step must be the baseline's, byte-for-byte, resolved
    through the MRO. Returns a list of violations (empty = fence holds). `planted_override` (red-team only):
    a function planted as EXP12Loop.step before the check — the fence must FIRE on it."""
    import torch
    torch.set_num_threads(1)
    import exp12_arms as X12
    cls = X12.EXP12Loop
    violations = []
    if planted_override is not None:
        cls.step = planted_override                     # red-team plant (caller restores)
    try:
        # (a) no class below Stage0Loop in the MRO may own a `step` override
        base = [c for c in cls.__mro__ if c.__name__ == "Stage0Loop"]
        if not base:
            violations.append(("MRO", "Stage0Loop missing from EXP12Loop.__mro__ — learner chain rewired"))
        else:
            for c in cls.__mro__:
                if c is base[0]:
                    break
                if "step" in vars(c):
                    violations.append(("OVERRIDE", f"{c.__name__} defines its own step — the learner is "
                                                   "no longer Stage0Loop.step"))
        # (b) the effective live source must equal the BASELINE Stage0Loop.step source, byte-for-byte
        live = inspect.getsource(cls.step)
        want = symbols(_baseline_src("../04_stage0_mvp/loop.py"), "loop.py")["Stage0Loop.step"] + "\n"
        if live != want:
            violations.append(("CHANGED", "live EXP12Loop.step source != baseline Stage0Loop.step "
                                          f"({BASELINE_COMMIT})"))
    finally:
        if planted_override is not None:
            del cls.step                                # restore inheritance (the plant lived on the subclass)
    return violations


def main():
    print(f"generator diff-scope vs baseline {BASELINE_COMMIT} (whitelist = the W-PERM blast radius)")
    any_viol = False
    for name, r in run().items():
        print(f"  {name}: added={r['added']} changed={r['changed']} removed={r['removed']}")
        for kind, sym in r["violations"]:
            print(f"    VIOLATION {kind} {sym} — OUT OF BLAST RADIUS"); any_viol = True
    if any_viol:
        print("HALT — the generator edit is NOT confined to its blast radius.")
        sys.exit(1)
    print("  PASS — every generator symbol outside the W-PERM whitelist is byte-identical to baseline.\n")

    print("RED-TEAM — inject the review panel's eval-path perturbation (self.centre) into exp12_fabric:")
    rt = run(perturb=("exp12_fabric.py",
                      "self.centre = self.centre_id + (self.bg_const @ self.bg_axes)",
                      "self.centre = self.centre_id + 2 * (self.bg_const @ self.bg_axes)"))
    viols = rt["exp12_fabric.py"]["violations"]
    print(f"    violations now: {viols}")
    if not viols:
        print("RED-TEAM FAILED — the diff-scope did NOT flag an out-of-scope generator change. Dead code.")
        sys.exit(1)
    print("RED-TEAM PASS — the diff-scope flags the eval-path perturbation (self.centre) that G0b's fabric "
          "digest is blind to. It has failed on a planted out-of-scope change — construction, not sampling.")

    print("\nB11 LEARNER FENCE (runtime, ledger 32) — live EXP12Loop.step vs baseline Stage0Loop.step:")
    v = learner_fence()
    if v:
        for kind, msg in v:
            print(f"    VIOLATION {kind}: {msg}")
        print("HALT — the LIVE learner is not the baseline learner.")
        sys.exit(1)
    print("    PASS — the live step IS the baseline Stage0Loop.step (byte-for-byte, MRO clean).")
    print("  RED-TEAM — plant a runtime step override on EXP12Loop; the fence must FIRE:")

    def _planted(self, *a, **k):                       # a wrapped/no-op learner — the anti-forward nightmare
        return None
    rtv = learner_fence(planted_override=_planted)
    print(f"    violations now: {[k for k, _ in rtv]}")
    if not rtv:
        print("RED-TEAM FAILED — the learner fence did NOT flag a planted runtime step override. Dead code.")
        sys.exit(1)
    post = learner_fence()
    if post:
        print(f"RED-TEAM RESTORE FAILED — fence still firing after plant removal: {post}")
        sys.exit(1)
    print("  RED-TEAM PASS — the fence fires on a planted live override and is clean after restore.")


if __name__ == "__main__":
    main()
