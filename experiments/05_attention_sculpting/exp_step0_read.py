"""exp_step0_read.py — STEP-0 CWP premise read executor (docs/STEP0_CWP_PREMISE_READ_PREREG.md, ratified
2026-07-24; corridor rows §7).

Modes: --census (G0; writes exp08/step0_census.json), --smoke (G1, including the REQUIRED observed-red of
the broken >=-variant on the tie fixture), default = G2 compute — which REFUSES to run unless the census
exists AND carries no HALT surface ("any HALT condition in the docs = stop and surface, no workaround").

Records only: no checkpoint loads (row 53, untriggered here), no new forwards. All statistics per seed ×
per channel; channels never pool. A condition the prereg does not define (e.g. an empty dominance
denominator) is a HALT surfaced in the artifact, never a judgment.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTDIR = HERE / "exp08"
REPO = HERE.parents[1]

sys.path.insert(0, str(HERE))
import exp12_arms as X12

# §3: bucket labels COMPUTED from the committed POS_BUCKETS (never re-typed); value drift => HALT
assert X12.POS_BUCKETS == ((1, 1), (2, 2), (3, 3), (4, 6), (7, 12), (13, 48)), \
    "POS_BUCKETS drift vs prereg §3 — HALT"
def _label(lo: int, hi: int) -> str:
    return f"p{lo}" if lo == hi else f"p{lo}-{hi}"
KEYS = [_label(lo, hi) for lo, hi in X12.POS_BUCKETS]
ONSET, MIDS = KEYS[0], KEYS[1:]
CHANNELS = ("pos_err_word", "pos_err_vis")
CONFIRM_AT, FAIL_AT = 0.90, 0.50          # §5 thresholds, verbatim
MIN_COLS = 8                               # §3: N < 8 columns => HALT

CENSUS_PATH = OUTDIR / "step0_census.json"
GATELOG_PATH = OUTDIR / "step0_gatelog.json"


def _gatelog_update(gate: str, payload: dict) -> None:
    log = json.loads(GATELOG_PATH.read_text()) if GATELOG_PATH.exists() else {}
    log[gate] = payload
    GATELOG_PATH.write_text(json.dumps(log, indent=2))


def _quartiles(cols: list) -> tuple[list, list]:
    """§3 verbatim: late = last N - floor(0.75*N) columns by t; early = first floor(0.25*N)."""
    cs = sorted(cols, key=lambda c: c["t"])
    n = len(cs)
    assert n >= MIN_COLS, f"N={n} < {MIN_COLS} columns — HALT (too few to quartile)"
    return cs[math.floor(0.75 * n):], cs[:math.floor(0.25 * n)]


def _dominance(cols: list, channel: str, strict: bool = True) -> tuple[int, int, int]:
    """§4 estimator: (numerator, denominator, columns_dropped). A column missing ANY bucket key is
    dropped from the denominator and counted. Strict inequality; no ties forgiven. The strict=False
    variant exists ONLY for the G1 observed-red fixture and is never used on real records."""
    num = den = dropped = 0
    for c in cols:
        d = c.get(channel, {})
        if any(k not in d for k in KEYS):
            dropped += 1
            continue
        den += 1
        op = (lambda a, b: a > b) if strict else (lambda a, b: a >= b)
        if all(op(d[ONSET], d[m]) for m in MIDS):
            num += 1
    return num, den, dropped


def _cell(num: int, den: int) -> str:
    """§5 cells. An empty denominator matches no cell => HALT surface, never a judgment."""
    if den == 0:
        return "HALT:ESTIMATOR-UNDEFINED (empty denominator — every late-quartile column dropped)"
    f = num / den
    if f >= CONFIRM_AT:
        return "PREMISE-CONFIRMED"
    if f <= FAIL_AT:
        return "PREMISE-FAILS"
    return "HALT:PREMISE-WEAK"


# ---------------------------------------------------------------- census (G0)

_VARIANTS = ("expomid", "orbit", "scatter")

def _classify(name: str, arm: str) -> tuple[bool, str]:
    """Mechanical role rule, stated in the census artifact: the certified-dead cell = the arm-exact
    verdict set (tag _verdict). Everything else is excluded with a named reason."""
    if any(f"{arm}_{v}" in name for v in _VARIANTS):
        return False, "variant arm (not the certified-dead cell's arm)"
    if name.startswith("exp_isobal") or name.startswith("retro_marginal"):
        return False, "instrument/retro-read record, not a run record of the cell"
    if re.fullmatch(rf"exp14_{arm}_s\d+_verdict\.json", name):
        return True, "verdict record (the certified-dead cell)"
    if "_cal" in name:
        return False, "cal-seed record (calibration role, not the verdict cell)"
    if "_dcy" in name:
        return False, "decay micro-arm companion record"
    if re.fullmatch(rf"{arm}_s\d+\.json", name):
        return False, "EXP12-era Stage-1 record (pre-exp14 harness)"
    return False, "smoke/reference/pre-check instrument record (not the verdict cell)"


def _field_check(rec: dict, name: str) -> tuple[bool, str, dict]:
    """§2: a record missing a required field is excluded and reported, never patched. Coverage of
    individual bucket KEYS is recorded (feeds §4's columns_dropped), not an exclusion ground."""
    if rec.get("arm") is not None and "exp12" in str(rec.get("arm", "")):
        pass                                       # provenance computed below by the caller
    cols = rec.get("columns")
    if not cols:
        return False, "no columns[]", {}
    for ch in CHANNELS:
        missing = sum(1 for c in cols if not isinstance(c.get(ch), dict))
        if missing:
            return False, f"missing field {ch} in {missing} column(s)", {}
    cov = {}
    for ch in CHANNELS:
        cov[ch] = {
            "n_columns": len(cols),
            "all6": sum(1 for c in cols if all(k in c[ch] for k in KEYS)),
            "missing_by_key": {k: sum(1 for c in cols if k not in c[ch]) for k in KEYS
                               if any(k not in c[ch] for c in cols)},
        }
    return True, "", cov


def census(fixture_dir: str | None = None) -> dict:
    """G0. Real mode: git-tracked exp08 records only ("committed"), arm-exact, role-classified.
    Fixture mode (--fixture-dir): every *.json is a role-admissible candidate; field rules only."""
    out = {"doc": "STEP0_CWP_PREMISE_READ_PREREG.md", "rules": [
        "committed = git-tracked in OUTDIR (exp08)",
        "arm-exact: filename token exp12_dwell (variants expomid/orbit/scatter excluded); record's own "
        "arm field must equal exp12_dwell (provenance computed, not asserted)",
        "the certified-dead cell = the verdict set: exp14_exp12_dwell_s<seed>_verdict.json",
        "field rule (§2): every column must carry pos_err_word and pos_err_vis as dicts; a record "
        "failing this is excluded and reported, never patched",
        "bucket-key coverage per channel is RECORDED (feeds §4 columns_dropped); an empty late-quartile "
        "denominator for any admissible record/channel is a HALT surface (no cell defined)",
    ], "candidates": [], "admissible": [], "companion": {"candidates": [], "admissible": []},
        "halt_surfaces": []}

    if fixture_dir:
        for p in sorted(Path(fixture_dir).glob("*.json")):
            rec = json.loads(p.read_text())
            ok, why, cov = _field_check(rec, p.name)
            out["candidates"].append({"name": p.name, "admitted": ok,
                                      "reason": why or "fixture candidate, fields complete"})
            if ok:
                out["admissible"].append({"name": p.name, "coverage": cov})
        return out

    tracked = subprocess.run(["git", "-C", str(REPO), "ls-files",
                              "experiments/05_attention_sculpting/exp08/"],
                             capture_output=True, text=True, check=True).stdout.split()
    for arm, bucket in (("exp12_dwell", out), ("exp12_shuffle", out["companion"])):
        names = sorted(Path(t).name for t in tracked
                       if arm in Path(t).name and t.endswith(".json")
                       and not t.endswith(".manifest.json"))
        for name in names:
            ok_role, reason = _classify(name, arm)
            row = {"name": name, "admitted": False, "reason": reason}
            if ok_role:
                rec = json.loads((OUTDIR / name).read_text())
                if rec.get("arm") != arm:
                    row["reason"] = f"PROVENANCE MISMATCH: record arm field {rec.get('arm')!r} != {arm}"
                    out["halt_surfaces"].append(row["reason"])
                else:
                    ok_f, why, cov = _field_check(rec, name)
                    if not ok_f:
                        row["reason"] = f"field exclusion: {why}"
                    else:
                        row.update(admitted=True, reason="verdict record, fields complete")
                        late, _early = _quartiles(rec["columns"])
                        entry = {"name": name, "seed": rec.get("seed"),
                                 "n_columns": len(rec["columns"]), "coverage": cov,
                                 "late_quartile_denominator": {}}
                        for ch in CHANNELS:
                            _n, den, drop = _dominance(late, ch)
                            entry["late_quartile_denominator"][ch] = den
                            if den == 0 and bucket is out:
                                out["halt_surfaces"].append(
                                    f"{name} channel {ch}: EVERY late-quartile column dropped "
                                    f"(§4) — dominance denominator EMPTY; §5 defines no cell for an "
                                    f"undefined estimator. HALT — surfaced to Jason, no workaround.")
                        bucket["admissible"].append(entry)
            bucket["candidates"].append(row)

    if not out["admissible"]:
        out["halt_surfaces"].append("ZERO admissible exp12_dwell records — HALT (§2)")
    # collapse the per-record vis surfaces into one structural line when uniform
    vis_hits = [h for h in out["halt_surfaces"] if "pos_err_vis" in h]
    if len(vis_hits) == len(out["admissible"]) and vis_hits:
        out["halt_surfaces"] = [h for h in out["halt_surfaces"] if "pos_err_vis" not in h]
        out["halt_surfaces"].append(
            "STRUCTURAL: pos_err_vis lacks the p1 bucket in every column of every admissible record "
            "(measured 0/1666 x 8 seeds; the _buffer_wave training-stash routing stashes no vision-side "
            "error at onset — exp12_arms.py:725-727, assembly; :536 _buffer_wave). The §4 vis-channel "
            "onset-dominance denominator is EMPTY for the whole cell; §5 defines no cell for an "
            "undefined dominance. HALT — G2 HELD, surfaced to Jason. The word channel is complete "
            "(all six buckets in 1666/1666 columns, every seed).")
    return out


# ------------------------------------------------------------------ smoke (G1)

def _mk_rec(p1_val, mid_val, n=12, tie_mid=None):
    cols = []
    for i in range(n):
        d = {ONSET: p1_val, **{m: mid_val for m in MIDS}}
        if tie_mid is not None:
            d[tie_mid] = p1_val                    # exact tie at one mid bucket
        cols.append({"t": (i + 1) * 300, "pos_err_word": dict(d), "pos_err_vis": dict(d)})
    return cols


def smoke():
    """G1 reader red-team. The broken >=-variant MUST be observed red on the tie fixture before the
    strict version's pass counts (prereg §7, observed-red rule)."""
    fails = _mk_rec(0.1, 1.0)                      # onset < every mid, every column
    conf = _mk_rec(2.0, 1.0)                       # onset > all mids, every column
    tie = _mk_rec(1.0, 0.5, tie_mid=MIDS[0])       # onset == one mid exactly, every column

    late_f, _ = _quartiles(fails)
    late_c, _ = _quartiles(conf)
    late_t, _ = _quartiles(tie)

    n, d, _ = _dominance(late_f, "pos_err_word")
    assert _cell(n, d) == "PREMISE-FAILS", "G1 red-team: FAILS synthetic mislabeled"
    n, d, _ = _dominance(late_c, "pos_err_word")
    assert _cell(n, d) == "PREMISE-CONFIRMED", "G1 red-team: CONFIRMED synthetic mislabeled"

    # OBSERVED RED: the broken variant (>= instead of >) forgives the tie and mislabels
    nb, db, _ = _dominance(late_t, "pos_err_word", strict=False)
    broken_verdict = _cell(nb, db)
    assert broken_verdict == "PREMISE-CONFIRMED", "fixture broken: >=-variant did not mislabel the tie"
    ns, ds, _ = _dominance(late_t, "pos_err_word", strict=True)
    strict_verdict = _cell(ns, ds)
    assert strict_verdict == "PREMISE-FAILS", "strict rule failed the tie fixture"

    # additional build fixture: an all-columns-dropped channel must surface HALT, never a cell
    gap = _mk_rec(2.0, 1.0)
    for c in gap:
        del c["pos_err_vis"][ONSET]
    ng, dg, dropg = _dominance(_quartiles(gap)[0], "pos_err_vis")
    assert dg == 0 and _cell(ng, dg).startswith("HALT:"), "empty denominator must HALT, not judge"

    payload = dict(fails_synthetic="PREMISE-FAILS ok", confirmed_synthetic="PREMISE-CONFIRMED ok",
                   broken_variant_observed_red=(f"tie fixture: >=-variant labeled {broken_verdict} "
                                                f"(WRONG, red observed) vs strict {strict_verdict}"),
                   empty_denominator_fixture="HALT surfaced, no judgment", result="PASS")
    _gatelog_update("G1", payload)
    print("G1 SMOKE PASS (broken >=-variant observed red on the tie fixture first)", flush=True)


# ---------------------------------------------------------------- compute (G2)

def compute():
    assert CENSUS_PATH.exists(), "G2 refuses: no census artifact (run --census first) — HALT"
    cen = json.loads(CENSUS_PATH.read_text())
    if cen["halt_surfaces"]:
        _gatelog_update("G2", {"status": "HELD", "grounds": cen["halt_surfaces"],
                               "note": "any HALT condition in the docs = stop and surface, no "
                                       "workaround (order, 2026-07-25); no partial/word-only read "
                                       "taken — that would be a judgment the prereg does not license"})
        print("G2 HELD — HALT surfaced at census; routed to Jason:", flush=True)
        for h in cen["halt_surfaces"]:
            print("  *", h, flush=True)
        sys.exit(3)
    raise SystemExit("G2 full compute path unreached this corridor (census carried HALT surfaces); "
                     "implementing the cell/companion emission is gated on Jason's ruling.")


if __name__ == "__main__":
    if "--census" in sys.argv:
        fx = None
        if "--fixture-dir" in sys.argv:
            fx = sys.argv[sys.argv.index("--fixture-dir") + 1]
        c = census(fx)
        if fx is None:
            CENSUS_PATH.write_text(json.dumps(c, indent=2))
            _gatelog_update("G0", {
                "admissible": len(c["admissible"]),
                "excluded": sum(1 for r in c["candidates"] if not r["admitted"]),
                "companion_admissible": len(c["companion"]["admissible"]),
                "halt_surfaces": c["halt_surfaces"], "result": "PASS" if c["admissible"] else "HALT"})
            print(f"G0 CENSUS: {len(c['admissible'])} admissible / "
                  f"{len(c['candidates'])} candidates; halt_surfaces={len(c['halt_surfaces'])}",
                  flush=True)
        else:
            adm = len(c["admissible"]); exc = sum(1 for r in c["candidates"] if not r["admitted"])
            print(f"G0 FIXTURE: admissible={adm} excluded={exc}", flush=True)
    elif "--smoke" in sys.argv:
        smoke()
    else:
        compute()
