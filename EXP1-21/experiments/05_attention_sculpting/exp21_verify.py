"""EXP21 — G6 terminal verification machinery + fixtures (prereg §7 row G6).

BUILT NOW because the gate-executor audit requires every executor before Touch 2; EXECUTED in
full only after G5 (not authorized by the build order — the corridor hard-holds before G4).
What runs pre-verdict: the bank rebuild check, the gradient-proof replay vs the COMMITTED G2
census, the probe-series from-raw recompute on CALIBRATION artifacts, and every observed-red
fixture — each fixture fires a DEPLOYED comparison function (the build-review panel's
vacuous-fixture findings bind here), never an inline restatement.

Full G6 (post-G5): independent from-raw recomputation of every verdict series, bank/fabric
rebuild, gradient proof replay vs the committed census, seed-route AND cohort recomputation
vs the committed exp21_verdict.json (8-row completeness enforced), the full gate log, and
zero MUST-FIX — then the terminal surface routes to Touch 3.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import exp21_cal as CAL                                        # noqa: E402
import exp21_probe as P21                                      # noqa: E402
import exp21_score as SC                                       # noqa: E402
import exp21_teaching as T21                                   # noqa: E402

OUTDIR21 = T21.OUTDIR21


# ------------------------------------------------------------------ deployed comparators
def compare_census(replay: dict, committed: dict):
    """The replayed G2 census must agree with the COMMITTED census artifact check-for-check
    (the gradient_record_tamper fixture fires THIS)."""
    want = {k: v["ok"] for k, v in committed["real"]["checks"].items()}
    assert replay == want, \
        (f"gradient census replay disagrees with the committed record: "
         f"{ {k: (replay.get(k), want.get(k)) for k in set(replay) | set(want) if replay.get(k) != want.get(k)} }")


def compare_routes(committed_out: dict, recomputed_rows: dict, recomputed_cohort: dict):
    """Committed verdict vs independent recomputation: full 8-row table, row-wise route
    equality, cohort equality (the route_flip / missing_bare_n fixtures fire THIS)."""
    table = committed_out.get("seed_table", [])
    assert len(table) == 8 and committed_out.get("bare_n") == 8, \
        f"committed verdict lacks the full 8-row seed table (n={len(table)}) — HALT"
    assert sorted(recomputed_rows) == [r["seed"] for r in sorted(table, key=lambda r: r["seed"])], \
        "recomputed seed set differs from the committed table"
    for row in table:
        rec = recomputed_rows[row["seed"]]
        assert rec["route"] == row["route"], \
            f"route recompute mismatch s{row['seed']}: {rec['route']} != committed {row['route']}"
    assert recomputed_cohort["cohort"] == committed_out["cohort"]["cohort"], \
        (f"cohort recompute mismatch: {recomputed_cohort['cohort']} != "
         f"committed {committed_out['cohort']['cohort']}")


# ------------------------------------------------------------------ verification passes
def verify_probe_series(arm: str, seed: int, tag: str, *, horizon: int = T21.H21) -> dict:
    """From-raw: recompute the category series from the committed predictions + labels and
    require digit-identity with the committed per-read summaries (deployed integrity law)."""
    p = CAL.load_probe(arm, seed, tag, "primary")
    CAL.assert_grid_complete(p["ts"], horizon)
    lab = CAL.cat_labels(p["ev_member"])
    s = CAL.bacc_series(p["predictions"], lab)
    CAL.assert_summary_integrity(s, p["summaries"], f"{arm} s{seed} {tag}")
    return dict(arm=arm, seed=seed, tag=tag, reads=len(p["ts"]), ok=True)


def verify_banks(seeds, kinds=("primary",)) -> list:
    out = []
    for s in seeds:
        for kind in kinds:
            stored = P21.load_bank(s, kind)                    # manifest-hash asserted
            rebuilt = P21.build_bank(s, kind)
            P21.check_bank_hash(rebuilt, P21.bank_digest(stored), f"rebuild s{s} {kind}")
            out.append(dict(seed=s, kind=kind, ok=True))
    return out


def replay_gradient_proof(seed: int = 20, steps: int = 2000) -> dict:
    """Independent replay of the G2 census on a fresh real pair; every check must hold."""
    on, _, _ = T21.build_exp21("on", seed, steps)
    off, _, _ = T21.build_exp21("off", seed, steps)
    r = T21.gradient_census(on, off)
    bad = [k for k, v in r["checks"].items() if not v["ok"]]
    assert not bad, f"gradient proof replay failed: {bad}"
    return {k: v["ok"] for k, v in r["checks"].items()}


def recompute_routes(tag: str = "verdict") -> dict:
    """Route + cohort recomputation vs the committed verdict artifact (post-G5 only)."""
    committed = json.loads((OUTDIR21 / "exp21_verdict.json").read_text())
    k = SC.load_constants()
    restriction = SC.load_restriction()
    rows = {}
    for row in committed["seed_table"]:
        s = row["seed"]
        on = SC.summarize_seed("on", s, k, tag)
        off = SC.summarize_seed("off", s, k, tag)
        SC.assert_pair_share(on, off)
        rows[s] = SC.seed_route(on, off, k, restriction=restriction)
    compare_routes(committed, rows, SC.cohort(rows))
    return dict(seeds=len(rows), ok=True)


# ------------------------------------------------------------------ observed-red fixtures
def fixtures() -> dict:
    torch.set_num_threads(1)
    reds = {}

    # raw_column_mutation: a tampered prediction column must fire the DEPLOYED integrity law
    bank = P21.build_bank(20, "primary")
    loop, _, _ = T21.build_exp21("on", 20, steps=64)
    out, pred = P21.probe_read(loop, bank)
    lab = CAL.cat_labels(bank["ev_member"])
    tampered = pred.clone()
    tampered[:64] = 1 - tampered[:64]
    s_tamp = CAL.bacc_series(tampered.unsqueeze(0), lab)
    try:
        CAL.assert_summary_integrity(s_tamp, [out], "tampered")
        raise SystemExit("integrity law blind to a mutated prediction column — HALT")
    except AssertionError as e:
        reds["raw_column_mutation"] = dict(red=True, message=str(e)[:120])
    s_true = CAL.bacc_series(pred.unsqueeze(0), lab)
    CAL.assert_summary_integrity(s_true, [out], "restore-green")

    # bank_swap: the DEPLOYED bank-binding law must refuse a payload carrying another
    # bank's digest (requires the seed-20 primary manifest on disk — write_bank provides)
    P21.write_bank(20, "primary")
    shadow = P21.build_bank(20, "shadow")
    try:
        P21.assert_bank_binding(20, P21.bank_digest(shadow))
        raise SystemExit("bank-binding law blind to a swapped bank — HALT")
    except AssertionError as e:
        reds["bank_swap"] = dict(red=True, message=str(e)[:140])
    P21.assert_bank_binding(20, P21.bank_digest(P21.load_bank(20, "primary")))

    # route_flip / missing_bare_n: DEPLOYED compare_routes on a synthetic committed verdict
    rows = {s: SC.seed_route(*SC._syn("NO-EFFECT"), SC.FIX_K) for s in range(8)}
    coh = SC.cohort(rows)
    committed = dict(seed_table=[dict(seed=s, **rows[s]) for s in range(8)],
                     cohort=coh, bare_n=8)
    flipped = json.loads(json.dumps(committed))
    flipped["seed_table"][3]["route"] = "TEACHING-ADDED"
    try:
        compare_routes(flipped, rows, coh)
        raise SystemExit("compare_routes blind to a flipped committed route — HALT")
    except AssertionError as e:
        reds["route_flip"] = dict(red=True, message=str(e)[:140])
    partial = dict(committed, seed_table=committed["seed_table"][:5], bare_n=5)
    try:
        compare_routes(partial, rows, coh)
        raise SystemExit("compare_routes accepted a partial seed table — HALT")
    except AssertionError as e:
        reds["missing_bare_n"] = dict(red=True, message=str(e)[:140])
    compare_routes(committed, rows, coh)                       # restore-green

    # gradient_record_tamper: DEPLOYED compare_census vs a tampered committed record
    replay = replay_gradient_proof(seed=20, steps=1000)
    committed_census = dict(real=dict(checks={k: dict(ok=v) for k, v in replay.items()}))
    tampered_census = json.loads(json.dumps(committed_census))
    tampered_census["real"]["checks"]["off_lpam_to_vision_zero"]["ok"] = False
    try:
        compare_census(replay, tampered_census)
        raise SystemExit("compare_census blind to a tampered committed census — HALT")
    except AssertionError as e:
        reds["gradient_record_tamper"] = dict(red=True, message=str(e)[:140])
    compare_census(replay, committed_census)                   # restore-green

    OUTDIR21.mkdir(parents=True, exist_ok=True)
    T21.write_gate_artifact(OUTDIR21 / "exp21_verify_fixtures.json", reds)
    T21.gatelog_append(dict(gate="G6-fixtures", outcome="OBSERVED-RED (fixture-only)",
                            executor="exp21_verify.fixtures", reds=sorted(reds)))
    print("G6 fixtures reds:", sorted(reds))
    return reds


def main(tag: str = "verdict") -> dict:
    """Full G6 — refuses until the verdict artifact exists (post-G5; NOT the build order)."""
    torch.set_num_threads(1)
    assert (OUTDIR21 / "exp21_verdict.json").exists(), \
        "G6 refused: no committed verdict artifact (the corridor hard-holds before G4)"
    committed_census = json.loads((OUTDIR21 / "exp21_g2_gradient_census.json").read_text())
    replay = replay_gradient_proof()
    compare_census(replay, committed_census)
    out = dict(
        series=[verify_probe_series(a, s, tag) for a in ("on", "off")
                for s in T21.VERDICT_SEEDS21],
        banks=verify_banks(T21.VERDICT_SEEDS21),
        gradient_replay=replay,
        routes=recompute_routes(tag))
    T21.write_gate_artifact(OUTDIR21 / "exp21_g6_verification.json", out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", action="store_true")
    ap.add_argument("--pre-verdict", action="store_true",
                    help="bank rebuild + gradient replay vs committed census + cal from-raw")
    args = ap.parse_args()
    torch.set_num_threads(1)
    if args.fixtures:
        fixtures()
    elif args.pre_verdict:
        committed_census = json.loads(
            (OUTDIR21 / "exp21_g2_gradient_census.json").read_text())
        replay = replay_gradient_proof()
        compare_census(replay, committed_census)
        print(json.dumps(dict(
            census_vs_committed="MATCH",
            banks=verify_banks(T21.CAL_SEEDS21),
            cal_series=[verify_probe_series(a, s, "cal") for a in ("on", "off")
                        for s in T21.CAL_SEEDS21]), indent=2))
