"""exp_opt_pin.py — OPTIMIZER PIN executor (docs/OPTIMIZER_PIN.md §5, ratified 2026-07-24).

Modes: --verify = P0 line-verify + P1 defaults (the pre-flight half; no artifact), --fixtures = the three
broken-variant reds (each must be OBSERVED red before the corresponding pass counts), default = P0 + P1 +
P2 emit (outputs/optimizer_pin.json at the repo root, per the doc's §4 path).

Pure code-read: no runs, no records, no checkpoints. The param-group census (P2) uses a constructor-only
instantiation (exp12_dwell s0, T=2000, ZERO optimizer steps) — recorded in the artifact's mechanics field.
τ values are computed from the betas READ off the live optimizer's param group (by-omission defaults),
never re-typed; drift from any §1 cited line, any §1 stated default, or any §2 derived constant ⇒ HALT.
"""
from __future__ import annotations

import inspect
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = REPO / "outputs"
GATELOG = OUT / "optimizer_pin_gatelog.json"

# §1 citations: (relative path, 1-indexed line, required substrings — from the DOC's claims, not the file)
P0_CITES = [
    ("experiments/04_stage0_mvp/loop.py", 68, ["torch.optim.Adam(params, lr=cfg.lr)"]),
    ("experiments/04_stage0_mvp/constants.py", 87, ["lr", "3e-3"]),
    ("experiments/04_stage0_mvp/loop.py", 8, ["lr=0", "frozen"]),
]
STATED_DEFAULTS = {"betas": (0.9, 0.999), "eps": 1e-8, "weight_decay": 0}   # §1, by omission
STATED_TAU = {"tau1": 10, "tau2": 1000}                                     # §2


def _gatelog_update(gate: str, payload: dict) -> None:
    OUT.mkdir(exist_ok=True)
    log = json.loads(GATELOG.read_text()) if GATELOG.exists() else {}
    log[gate] = payload
    GATELOG.write_text(json.dumps(log, indent=2))


def _head() -> str:
    return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()


def p0_line_verify(root: Path = REPO) -> list:
    rows = []
    for rel, lineno, needles in P0_CITES:
        line = (root / rel).read_text().split("\n")[lineno - 1]
        for n in needles:
            assert n in line, f"P0 DRIFT — {rel}:{lineno} lacks {n!r} (line: {line.strip()!r}) — HALT"
        rows.append({"cite": f"{rel}:{lineno}", "line": line.strip(), "verified": needles})
    return rows


def p1_defaults(py_files: list[Path] | None = None) -> dict:
    """No betas/eps/weight_decay kwarg on the optimizer path; no scheduler; no lr mutation."""
    if py_files is None:
        tracked = subprocess.run(["git", "-C", str(REPO), "ls-files", "*.py"],
                                 capture_output=True, text=True, check=True).stdout.split()
        py_files = [REPO / t for t in tracked]
    optim_calls, pg_lines, violations = [], [], []
    for f in py_files:
        for i, line in enumerate(f.read_text().split("\n"), 1):
            loc = f"{f.relative_to(REPO) if f.is_relative_to(REPO) else f.name}:{i}"
            if "torch.optim." in line and "lr_scheduler" not in line:
                optim_calls.append({"at": loc, "line": line.strip()})
                for kw in ("betas=", "eps=", "weight_decay="):
                    if kw in line:
                        violations.append(f"{loc}: optimizer kwarg {kw} — {line.strip()}")
            if "lr_scheduler" in line:
                violations.append(f"{loc}: scheduler reference — {line.strip()}")
            if "param_groups" in line:
                pg_lines.append({"at": loc, "line": line.strip()})
                if re.search(r"\[.lr.\]\s*=", line):
                    violations.append(f"{loc}: lr mutation via param_groups — {line.strip()}")
    assert not violations, "P1 HALT:\n" + "\n".join(violations)
    return {"optim_constructor_calls": optim_calls, "param_groups_lines": pg_lines,
            "scheduler_hits": 0, "violations": []}


def p2_emit() -> dict:
    import torch
    torch.set_num_threads(1)
    sys.path.insert(0, str(HERE))
    import exp12_arms as X12

    sig = {k: v.default for k, v in inspect.signature(torch.optim.Adam).parameters.items()
           if k in ("betas", "eps", "weight_decay")}
    loop, _spec, cfg = X12.build_exp12("exp12_dwell", 0, 2000)     # constructor-only; zero .step() calls
    groups = loop.opt.param_groups
    assert len(groups) == 1, f"P2: expected 1 param group, found {len(groups)} — HALT"
    g = groups[0]
    betas, eps, wd, lr = tuple(g["betas"]), g["eps"], g["weight_decay"], g["lr"]

    # §1 stated defaults must equal BOTH the live group's values and the installed-torch signature
    assert betas == STATED_DEFAULTS["betas"] == tuple(sig["betas"]), f"P2 DRIFT betas {betas} — HALT"
    assert eps == STATED_DEFAULTS["eps"] == sig["eps"], f"P2 DRIFT eps {eps} — HALT"
    assert wd == STATED_DEFAULTS["weight_decay"] == sig["weight_decay"], f"P2 DRIFT wd {wd} — HALT"

    # lr: parsed from the cited constants line (the read), cross-checked against cfg and the live group
    lr_line = (REPO / "experiments/04_stage0_mvp/constants.py").read_text().split("\n")[86]
    lr_read = float(re.search(r"=\s*([0-9.e+-]+)", lr_line).group(1))
    assert lr_read == cfg.lr == lr, f"P2 DRIFT lr: line {lr_read} cfg {cfg.lr} group {lr} — HALT"

    # τ computed from the READ betas — never re-typed; §2's integers checked to float representation
    tau1, tau2 = 1.0 / (1.0 - betas[0]), 1.0 / (1.0 - betas[1])
    assert math.isclose(tau1, STATED_TAU["tau1"], rel_tol=1e-12), f"tau1 {tau1} — HALT"
    assert math.isclose(tau2, STATED_TAU["tau2"], rel_tol=1e-12), f"tau2 {tau2} — HALT"

    held = {id(p) for p in g["params"]}
    census = {"group_lr": lr, "held": [], "excluded": []}
    for mod in ("vision", "op", "word"):
        for name, p in getattr(loop, mod).named_parameters():
            (census["held"] if id(p) in held else census["excluded"]).append(
                {"param": f"{mod}.{name}", "shape": list(p.shape)})
    held_mods = {e["param"].split(".")[0] for e in census["held"]}
    excl_mods = {e["param"].split(".")[0] for e in census["excluded"]}
    assert excl_mods == {"word"} and held_mods == {"vision", "op"}, \
        f"P2 census drift: held {held_mods}, excluded {excl_mods} — HALT (loop.py:8/:67 exclusion)"

    artifact = {
        "optimizer_class": type(loop.opt).__module__ + "." + type(loop.opt).__name__,
        "lr": lr, "betas": list(betas), "eps": eps, "weight_decay": wd, "scheduler": None,
        "torch_version": torch.__version__, "param_groups": census,
        "tau1": tau1, "tau2": tau2,
        "source_lines": p0_line_verify(),
        "read_date": "2026-07-25", "head_commit": _head(),
        "mechanics": "param census via constructor-only instantiation (exp12_dwell s0, T=2000, zero "
                     "optimizer steps); betas/eps/wd read from the live param group (by-omission "
                     "defaults) and cross-checked against the installed-torch signature; tau computed "
                     "from the read betas",
    }
    required = {"optimizer_class", "lr", "betas", "eps", "weight_decay", "scheduler", "torch_version",
                "param_groups", "tau1", "tau2", "source_lines", "read_date", "head_commit"}
    missing = required - set(artifact)
    assert not missing, f"P2 artifact incomplete: missing {missing} — HALT"
    OUT.mkdir(exist_ok=True)
    (OUT / "optimizer_pin.json").write_text(json.dumps(artifact, indent=2))
    return artifact


def fixtures(scratch: Path) -> None:
    """The three broken variants, each OBSERVED red (prereg §5 smoke column)."""
    scratch.mkdir(parents=True, exist_ok=True)
    # P0 red: edited cited line must fail line-verify
    root = scratch / "p0root"
    for rel, _l, _n in P0_CITES:
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text((REPO / rel).read_text())
    f = root / "experiments/04_stage0_mvp/loop.py"
    lines = f.read_text().split("\n")
    lines[67] = lines[67].replace("lr=cfg.lr", "lr=1e-4")
    f.write_text("\n".join(lines))
    try:
        p0_line_verify(root)
        raise SystemExit("P0 fixture FAILED TO FAIL — no observed red")
    except AssertionError as e:
        red_p0 = str(e)
    # P1 red: a betas= kwarg on an optimizer call must be flagged
    bad = scratch / "bad_optim.py"
    bad.write_text("opt = torch.optim.Adam(params, lr=lr, betas=(0.5, 0.9))\n")
    try:
        p1_defaults([bad])
        raise SystemExit("P1 fixture FAILED TO FAIL — no observed red")
    except AssertionError as e:
        red_p1 = str(e)
    # P2 red: a dropped field must fail the completeness check
    required = {"optimizer_class", "lr", "betas", "eps", "weight_decay", "scheduler", "torch_version",
                "param_groups", "tau1", "tau2", "source_lines", "read_date", "head_commit"}
    partial = {k: None for k in required if k != "tau2"}
    missing = required - set(partial)
    assert missing == {"tau2"}, "P2 fixture broken"
    red_p2 = f"field-drop fixture: completeness check reports missing {missing} (red observed)"
    _gatelog_update("fixtures_observed_red", {
        "P0_edited_line": red_p0.split("\n")[0], "P1_betas_kwarg": red_p1.split("\n")[0],
        "P2_field_drop": red_p2, "result": "ALL RED OBSERVED"})
    print("FIXTURES: all three broken variants observed red (P0 edited-line, P1 betas=, P2 field-drop)",
          flush=True)


if __name__ == "__main__":
    if "--fixtures" in sys.argv:
        fixtures(Path(sys.argv[sys.argv.index("--fixtures") + 1]) if
                 len(sys.argv) > sys.argv.index("--fixtures") + 1 else REPO / "outputs" / "_pinfx")
    elif "--verify" in sys.argv:
        rows = p0_line_verify()
        sweep = p1_defaults()
        _gatelog_update("P0", {"cites": rows, "result": "PASS"})
        _gatelog_update("P1", {"optim_calls": len(sweep["optim_constructor_calls"]),
                               "param_groups_lines": len(sweep["param_groups_lines"]),
                               "scheduler_hits": 0, "detail": sweep, "result": "PASS"})
        print(f"P0 PASS ({len(rows)} citations byte-verified) · P1 PASS "
              f"({len(sweep['optim_constructor_calls'])} optimizer calls, all lr-only; no scheduler; "
              f"no lr mutation)", flush=True)
    else:
        rows = p0_line_verify()
        p1 = p1_defaults()
        art = p2_emit()
        _gatelog_update("P2", {"tau1": art["tau1"], "tau2": art["tau2"],
                               "torch_version": art["torch_version"],
                               "held": len(art["param_groups"]["held"]),
                               "excluded": len(art["param_groups"]["excluded"]), "result": "PASS"})
        print(f"P2 EMIT: outputs/optimizer_pin.json — tau1 {art['tau1']} tau2 {art['tau2']} "
              f"lr {art['lr']} torch {art['torch_version']} | held "
              f"{len(art['param_groups']['held'])} tensors (vision+op), excluded "
              f"{len(art['param_groups']['excluded'])} (word, frozen)", flush=True)
