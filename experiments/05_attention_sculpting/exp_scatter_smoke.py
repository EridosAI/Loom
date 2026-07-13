"""exp_scatter_smoke.py — scorer-side smoke for SCATTER (prereg §6, the sm-G* row falsifiers).

Covers the scatter-SPECIFIC logic + every reachable falsifier the prereg names; the REUSED
exp17_score machinery (cal_read structure, _score_one/_ext_resolve/_floor_audit/_partition17) is
already smoke-tested in exp17_score.smoke(). Each assert is a POSITIVE delta — dies under a no-op.
"""
import exp_scatter_score as SS


def _cell(pslist, covlist):
    """cell_feasible on explicit per-seed perstep/coverage lists (lets a smoke exercise the
    per-seed-WORST gating, not just the pool)."""
    per = [dict(perstep_med=ps, tr11=cov) for ps, cov in zip(pslist, covlist)]
    return SS.cell_feasible_scatter(per, base, 0.50)


base = dict(perstep=0.1597, tr11=0.0906, confusion=1.3104)          # the real A_dwell baselines


def smoke_scatter_scorer():
    eight = lambda x: [x] * 8

    # (sc1) F5 floors — reachable falsifiers incl. the per-seed-WORST (RB-2) gating
    ok = _cell(eight(0.5576), eight(0.2087))
    assert ok["feasible"] and ok["floor1_contrast"] and ok["floor2_coverage"] and ok["floor3_ceiling"], \
        "the ratified R=0.50 cell must be feasible"
    assert not _cell(eight(0.0), eight(0.2087))["floor1_contrast"], "R=0 must FAIL the contrast floor"
    assert not _cell(eight(0.5576), eight(0.05))["floor2_coverage"], "low coverage must FAIL floor2"
    # confusion-ceiling reachable falsifier: planted per-step > C_ceil -> floor3 False (non-tautology)
    assert not _cell(eight(2.0), eight(0.2087))["floor3_ceiling"], "perstep > C_ceil must FAIL the ceiling"
    assert _cell(eight(1.20), eight(0.2087))["floor3_ceiling"], "perstep < C_ceil must PASS the ceiling"
    # per-seed-WORST: pool clears floor1 but ONE seed is below -> per-seed-min gates it out
    worst = _cell([0.56] * 7 + [0.20], eight(0.2087))
    assert worst["perstep_pool"] >= SS.CONTRAST_MULT * base["perstep"] \
        and not worst["floor1_contrast"], "per-seed-worst must gate a below-floor seed the pool hides"
    print("SMOKE_SCATTER_SCORER (sc1): F5 floors — contrast/coverage/ceiling + per-seed-worst falsifiers")

    # (sc2) lexicographic pick via the REAL SS._pick (not an inline re-implementation)
    cells = [dict(r=0.40, perstep_pool=0.446, confusion_margin=0.86, feasible=True),
             dict(r=0.50, perstep_pool=0.558, confusion_margin=0.75, feasible=True),
             dict(r=0.20, perstep_pool=0.223, confusion_margin=1.09, feasible=False)]
    assert SS._pick(cells)["r"] == 0.50, "SS._pick must take max-contrast feasible R (0.50)"
    assert SS._pick([c for c in cells if not c["feasible"]]) is None, "no feasible -> None (geometry HALT)"
    print("SMOKE_SCATTER_SCORER (sc2): real SS._pick -> R=0.50 (max contrast); empty -> None")

    # (sc3) matched-bar EXCESS predicate (F6-A rule i) — BOTH clauses independently falsified
    surviving = [dict(detector="0.62x4", a_k=6, b_k=2, fisher_a_ge_b=0.03)]
    fisher_fail = [dict(detector="0.62x4", a_k=5, b_k=3, fisher_a_ge_b=0.31)]          # p>0.05
    count_fail = [dict(detector="0.62x4", a_k=2, b_k=5, fisher_a_ge_b=0.01)]           # a_k<=b_k
    assert SS._excess_survives(surviving), "common-detector a_k>b_k with p<=0.05 must survive"
    assert not SS._excess_survives(fisher_fail), "p=0.31 (EXP17-orbit-shaped) must NOT survive"
    assert not SS._excess_survives(count_fail), "a_k<=b_k must NOT survive even at p<=0.05"
    print("SMOKE_SCATTER_SCORER (sc3): excess predicate — Fisher AND count clauses both falsifiable")

    # (sc4) primary-finding decision (the MUST-FIX: CONVERTS carries the n>=8 READ power floor)
    F = SS._primary_finding
    assert F(True, 5, 8, 6) == "SCATTER CONVERTS", "excess + cert>=5 + n_read>=8 -> CONVERTS"
    assert F(True, 5, 7, 6) != "SCATTER CONVERTS", "n_read=7 (<8) must NOT be CONVERTS (power floor)"
    assert F(True, 4, 8, 6) != "SCATTER CONVERTS", "cert=4 (<5) must NOT be CONVERTS"
    assert F(False, 0, 8, 0) == "SCATTER DEAD", "no excess + census 0 -> DEAD"
    assert F(False, 0, 8, 3) == "SCATTER DEAD", "no excess + census 0 -> DEAD regardless of raw_k (context)"
    assert F(True, 0, 8, 0).startswith("ROUTES"), "excess but census 0 -> ROUTES (divergence)"
    print("SMOKE_SCATTER_SCORER (sc4): _primary_finding — CONVERTS needs n>=8; DEAD raw-agnostic")

    # (sc5) guards (sm-G6-guard): both scorer entry points refuse when records are absent
    for fn, kw in ((SS.cal_read_scatter, dict(cal_tag="__nope__", write=False)),
                   (SS.score_scatter, dict(cal_read_tag="__nope__", write=False))):
        try:
            fn(**kw); raise RuntimeError(f"{fn.__name__} did not refuse on absent records")
        except AssertionError:
            pass
    print("SMOKE_SCATTER_SCORER (sc5): cal_read_scatter + score_scatter REFUSE when records absent")
    print("SMOKE_SCATTER_SCORER OK (sc1-sc5)")


if __name__ == "__main__":
    smoke_scatter_scorer()
