"""exp19_tabs.py — B9: the matched-bar tabs ×2 (full read + stratified read), EXP19's cross-B instrument.

THE MATCHED-BAR LAW (EXP17 F6-A / catch 16 / canon §10.27; standing rule): a cross-cell COUNT comparison is
evidence ONLY at a fixed detector — read BOTH cells through BOTH bars, like-for-like. The unlike-bar
comparison (cell A at A's bar vs cell B at B's bar) is exactly the 5-lens-missed error F6-A caught; this tab
never emits it, and its own validation/smoke derive every cross-cell quantity from SAME-bar reads (the B9
panel caught the first validation print doing an unlike-bar subtraction — the module now practices what its
header claims). What transports from the committed `verify_toolkit.matched_bar_tab` is the PROCEDURE — both
cells through both detectors — never the constants: EXP19's detector family is (BAND=0.64, window WIDTH,
outcome-blind simulated-floor certification), not EXP17's (band, N-consecutive). Every certification here
goes through B8's `_certify_seed` — one law, one instrument, everywhere.

TWO TABS, NEVER MIXED (prereg §8): the stratified read has ITS OWN tab, never the full-read bar — a cell
carries its `read` tag and the tab refuses cells whose reads differ. Cross-READ comparison is not a tab row
anywhere. When the two cells' bars COINCIDE (equal widths — per-B native cutting can land there), the tab
emits ONE matched row and flags `bars_coincide` so prose can never claim two-detector robustness from one
detector.

STATISTICS, MODEL-ANNOTATED (B9 panel): the per-row Fisher is INDEPENDENT-GROUPS exact (hypergeometric
margins). When the two cells share seeds (thinned proxies, same-arm re-reads — the ledger-42/43 companion
constructions are same-seed BY DESIGN), that model is invalid for evidence: the row then carries the exact
PAIRED companion (McNemar-exact one-sided on discordant per-seed certifications) and the paired column is
the evidence-grade p; the independent-groups Fisher is context-only there. `seed_overlap` is COMPUTED from
the cells' own seed lists, never asserted.

FLOOR COLUMNS (ledger 43 + B9 panel): each matched row reports, per cell, the per-seed simulated null maxima
with their p_hats. A seed's null is simulated at ITS OWN post-acq mean, which an episode INFLATES — so the
per-seed height is conservative for certifying THAT seed, and `floor_ceiling` (the max, with its realizing
seed named in `ceiling_carrier`) is a CERTIFICATION ENVELOPE, explicitly NOT the cell's phantom floor.
Cross-cell floor ordering reads on `floor_median` / per-seed heights with p_hats visible; the evidence-grade
PHANTOM-floor ordering (non-converter-labeled seeds) is computed downstream where labels are lawful
(calibration/validation side), never inside the outcome-blind tab. Never read one cell's separation against
another cell's floor.

DIVISION OF LAW: exp19_cal CUTS each cell's operating width on its own null (per-B native, ledger 42);
exp19_scorer CERTIFIES at the inherited width (ledger 44: at CAL.BAND, one family); this tab TABULATES —
it accepts widths already resolved upstream and never re-selects a bar on outcome. A cell's width must have
PROVENANCE on the exact data the cell contains (the panel caught the first validation handing a committed
op to a different draw — provenance is computed here, never asserted).

STATUS: machinery + validation on committed captures (B=T full-N stratum vs the ledger-42 thinned-7915
B=512-proxy, reproduced draw-exactly). The deployed cross-B tabs (paid arms exp19_wperm_B*) and the
cross-ARM floor ordering (C vs donor A et al.) run when those captures exist (corridor / pre-flight);
nothing trains until G8.
"""
from __future__ import annotations

import json
import statistics
import sys
from math import comb
from pathlib import Path

import torch

import exp14_arms as XA
import exp19_cal as CAL
import exp19_floor as FL
import exp19_scorer as SC

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from verify_toolkit import fisher_one_sided          # the committed instrument (exact hypergeometric)

BAND = SC.BAND                                       # 0.64 — family-wide (asserted == RB.BAND at SC import)
ROW_KEYS = {"bar", "a", "b", "fisher_a_ge_b", "fisher_model", "seed_overlap", "paired_exact_a_ge_b"}
TAB_KEYS = {"tab", "read", "cells", "bars", "bars_coincide", "evidence_rule", "floor_rule"}


def cell(name: str, read: str, width: int, data: dict) -> dict:
    """A tab cell: `data` = {seed: (acq, [[wave, acc], ...])} resolved UPSTREAM (CAL._onsets for committed
    captures, plants for smokes); `width` = the cell's own operating bar, cut upstream by exp19_cal on THIS
    data's own null (provenance is the caller's obligation — checked, not assumed, in _validate). The data is
    SNAPSHOTTED here (deep-copied) so later caller mutation cannot break the tab's determinism."""
    snap = {s: (int(acq), [[int(w), float(a)] for (w, a) in ons]) for s, (acq, ons) in data.items()}
    return dict(name=name, read=read, width=int(width), data=snap, seeds=sorted(snap))


def cell_from_records(name: str, arm: str, seeds: list, read: str, width: int) -> dict:
    """Convenience: build a cell from an arm's committed per-onset captures."""
    return cell(name, read, width, {s: CAL._onsets(arm, s, read) for s in seeds})


def _mcnemar_exact_one_sided(b_disc: int, c_disc: int) -> float:
    """Exact paired one-sided test on discordant pairs: P(X >= b_disc), X ~ Binomial(b_disc+c_disc, 1/2).
    b_disc = pairs certified in A only; c_disc = in B only (over the shared seeds)."""
    n = b_disc + c_disc
    return sum(comb(n, k) for k in range(b_disc, n + 1)) / 2 ** n if n else 1.0


def _bar_read(c: dict, width: int) -> dict:
    """Read one cell at one bar: certify every seed at (BAND, width) via B8's outcome-blind law. Per-seed
    simulated null max = that seed's floor height at this bar, simulated at ITS OWN p_hat (episode-inflated
    for converters — conservative per-seed, NOT the phantom floor; see the header's FLOOR COLUMNS)."""
    per = {}
    for s in c["seeds"]:
        acq, ons = c["data"][s]
        per[s] = SC._certify_seed(ons, acq, width, torch.Generator().manual_seed(FL.SIM_SEED + int(s)))
    certified = [s for s in c["seeds"] if per[s]["certified"]]
    heights = {s: per[s]["null_max"] for s in c["seeds"]}
    carrier = max(heights, key=lambda s: heights[s])
    return dict(name=c["name"], k=len(certified), n=len(c["seeds"]), certified=certified,
                runs={s: per[s]["observed_run"] for s in c["seeds"]},
                floor_heights=heights,                                              # per-seed OWN sim floor
                p_hats={s: per[s]["p_hat"] for s in c["seeds"]},                    # what drives each height
                floor_median=statistics.median(heights.values()),                   # the cross-cell floor read
                floor_ceiling=heights[carrier],                                     # certification ENVELOPE (max)
                ceiling_carrier=carrier,                                            # which seed realizes it
                separations={s: per[s]["observed_run"] - heights[s] for s in c["seeds"]})


def matched_bar_tab19(cell_a: dict, cell_b: dict) -> dict:
    """BOTH cells through BOTH bars. Each matched row fixes ONE detector (BAND, width) and reads both cells
    through it; every statistic lives INSIDE a matched row (group-1 = cell_a). Equal widths collapse to ONE
    row with `bars_coincide` set. Same-seed cells get the exact paired companion (evidence-grade there)."""
    assert cell_a["read"] == cell_b["read"], (
        f"READ MIX REFUSED: {cell_a['name']}={cell_a['read']} vs {cell_b['name']}={cell_b['read']} — the "
        "stratified read has its own tab, never the full-read bar (prereg §8); cross-read rows do not exist")
    coincide = cell_a["width"] == cell_b["width"]
    bars = ([(f"{cell_a['name']}+{cell_b['name']}", cell_a["width"])] if coincide else
            [(cell_a["name"], cell_a["width"]), (cell_b["name"], cell_b["width"])])
    overlap = sorted(set(cell_a["seeds"]) & set(cell_b["seeds"]))                   # COMPUTED, never asserted
    rows = []
    for owner, W in bars:
        a, b = _bar_read(cell_a, W), _bar_read(cell_b, W)
        paired = None
        if overlap:
            b_disc = len((set(a["certified"]) - set(b["certified"])) & set(overlap))
            c_disc = len((set(b["certified"]) - set(a["certified"])) & set(overlap))
            paired = _mcnemar_exact_one_sided(b_disc, c_disc)
        rows.append(dict(bar=dict(band=BAND, width=W, owner=owner),
                         a=a, b=b,
                         fisher_a_ge_b=fisher_one_sided(a["k"], a["n"], b["k"], b["n"]),
                         fisher_model=("independent-groups exact (hypergeometric margins)" +
                                       ("; CONTEXT-ONLY — cells share seeds, paired column is evidence-grade"
                                        if overlap else "")),
                         seed_overlap=overlap,
                         paired_exact_a_ge_b=paired))
    return dict(
        tab="B9 matched-bar tab (EXP19 floor-audit family: band 0.64 × width × sim-floor certification)",
        read=cell_a["read"], cells=[cell_a["name"], cell_b["name"]],
        bars=rows, bars_coincide=coincide,
        evidence_rule=("cross-cell counts are evidence ONLY inside a matched row (one bar, both cells); "
                       "own-bar counts across DIFFERENT bars are context-only and carry no statistic — "
                       "unlike-bar comparison is the F6-A error and is structurally absent here. For cells "
                       "with a nonempty seed_overlap the PAIRED exact column is the evidence-grade p and the "
                       "independent-groups Fisher is context-only. bars_coincide=True means ONE detector — "
                       "never quote it as two-bar robustness."),
        floor_rule=("separations are per-seed observed_run − OWN sim null max at that bar; each seed's null "
                    "is simulated at ITS OWN p_hat, which an episode INFLATES — floor_ceiling (max, with "
                    "ceiling_carrier named) is a certification ENVELOPE, not the phantom floor; cross-cell "
                    "floor ordering reads on floor_median / per-seed heights with p_hats visible, and the "
                    "evidence-grade phantom-floor ordering (non-converter-labeled) is computed downstream "
                    "where labels are lawful. Never read one cell's separation against another cell's floor "
                    "(ledger 43)."))


# ---------------------------------------------------------------- validation (committed captures, no compute)
REDTEAM_ORDER = [0, 2, 4, 5, 6, 1, 3, 7]     # exp19_cal._redteam's conv+nonconv insertion order — the
#                                              committed ledger-42 construction. ONE shared generator binds
#                                              the k-th randperm draw to the k-th seed VISITED, so iteration
#                                              order IS part of the draw's identity (the B9 panel caught the
#                                              first version iterating range(8): a DIFFERENT draw wearing the
#                                              committed op — provenance asserted, not computed).


def _thinned_proxy(full: dict, n_target: int = 7915, n_full: int = 14156, seed: int = 719150) -> dict:
    """The ledger-42 red-team draw, reproduced construction-exactly: shared pinned generator, seeds visited
    in REDTEAM_ORDER, among-kept uniform thinning to the B=512 stratum size. Inner lists copied (no aliasing
    with the full cell)."""
    gen = torch.Generator().manual_seed(seed)
    r = n_target / n_full
    out = {}
    for s in REDTEAM_ORDER:
        acq, ons = full[s]
        idx = torch.randperm(len(ons), generator=gen)[:round(r * len(ons))].tolist()
        out[s] = (acq, [list(ons[i]) for i in idx])
    return out


def _validate():
    """Two REAL cells with different native bars, zero new compute: B=T stratified full-N (op 550, committed
    G5b) vs the ledger-42 thinned-7915 B=512-proxy (op 600 — PROVENANCE RECOMPUTED on the exact draw below).
    Labels (committed converters {0,2,4,5,6} / non-converters {1,3,7}) are lawful HERE (validation side) and
    are used only for anchors and the phantom-floor disaggregation — the tab itself never sees them."""
    conv, nonconv = [0, 2, 4, 5, 6], [1, 3, 7]
    seeds = list(range(8))
    full_data = {s: CAL._onsets("exp12_shuffle", s, "stratified") for s in seeds}
    thin_data = _thinned_proxy(full_data)
    # PROVENANCE, COMPUTED NOT ASSERTED: the proxy's bar (600) must be the argmax-separation op of THIS draw's
    # own null — recomputed via the committed calibration law on the exact data the cell will contain.
    prov = CAL.cal_floor_audit("exp12_shuffle", "stratified", conv, nonconv, data=thin_data)
    assert prov["operating_point_width"] == 600, (
        f"PROVENANCE FAIL: the constructed thin draw's own-null op is {prov['operating_point_width']}, not "
        "the committed ledger-42 op 600 — this is NOT the committed red-team draw")
    ca = cell("BT_full14156", "stratified", 550, full_data)
    cb = cell("proxy_thin7915", "stratified", 600, thin_data)
    tab1 = matched_bar_tab19(ca, cb)
    tab2 = matched_bar_tab19(ca, cb)
    assert tab1 == tab2, "tab not deterministic across identical calls"
    print("=== B9 matched-bar tab — stratified: B=T full-N (op 550) vs thinned B=512-proxy (op 600) ===")
    for r in tab1["bars"]:
        a, b, bar = r["a"], r["b"], r["bar"]
        print(f"  bar {bar['band']}×{bar['width']} (owner {bar['owner']}):")
        for cc in (a, b):
            print(f"    {cc['name']:>15}: k={cc['k']}/{cc['n']} certified={cc['certified']} "
                  f"floor_median={cc['floor_median']} ceiling={cc['floor_ceiling']}@s{cc['ceiling_carrier']} "
                  f"runs={ {s: cc['runs'][s] for s in sorted(cc['runs'])} }")
        print(f"    fisher(a>=b) = {r['fisher_a_ge_b']:.4f}  [{r['fisher_model']}]")
        print(f"    paired exact (a>=b, shared seeds {len(r['seed_overlap'])}) = {r['paired_exact_a_ge_b']:.4f}")
    # LIKE-FOR-LIKE anchor: at its OWN bar (550) the full-N cell must reproduce B8's committed B=T stratified
    # read exactly — same instrument, same bar, same answer (5/8 {0,2,4,5,6}).
    own = next(r for r in tab1["bars"] if r["bar"]["width"] == 550)
    assert own["a"]["k"] == 5 and own["a"]["certified"] == conv, \
        f"full-N cell at its own bar diverged from the B8 committed read: {own['a']}"
    # CROSS-READ live anchor (the smoke's mutation-killer, on real data): each cell's read must actually
    # move with the bar — a _bar_read that ignores W (the silent unlike-bar tab) dies here.
    r550 = next(r for r in tab1["bars"] if r["bar"]["width"] == 550)
    r600 = next(r for r in tab1["bars"] if r["bar"]["width"] == 600)
    assert r550["a"]["runs"] != r600["a"]["runs"] and r550["b"]["runs"] != r600["b"]["runs"], \
        "a cell's read did not move across bars — _bar_read is ignoring the passed width"
    # DROPS, SAME-BAR ONLY (the panel caught the first version subtracting across bars): per matched row,
    # full-N certified minus proxy certified AT THAT ROW'S BAR.
    drops = {r["bar"]["width"]: sorted(set(r["a"]["certified"]) - set(r["b"]["certified"]))
             for r in tab1["bars"]}
    print(f"  proxy drops vs full-N AT THE SAME BAR (matched, per row): {drops}")
    # FLOORS: REPORTED, not asserted ('thinner ⇒ higher floor' is an EXPECTATION, not owed per-realization —
    # the loose-N lesson). The ceiling is a converter-inflated certification envelope (carrier printed above);
    # the PHANTOM-floor disaggregation below uses the committed non-converter labels — lawful on the
    # validation side only — where the granularity law can be read without episode inflation.
    fm_a = {r["bar"]["width"]: r["a"]["floor_median"] for r in tab1["bars"]}
    fm_b = {r["bar"]["width"]: r["b"]["floor_median"] for r in tab1["bars"]}
    print(f"  floor MEDIANS by bar (the cross-cell read): full-N {fm_a} vs thinned {fm_b}")
    phantom = {r["bar"]["width"]: sum(r["b"]["floor_heights"][s] >= r["a"]["floor_heights"][s] for s in nonconv)
               for r in tab1["bars"]}
    allw = {r["bar"]["width"]: sum(r["b"]["floor_heights"][s] >= r["a"]["floor_heights"][s] for s in seeds)
            for r in tab1["bars"]}
    print(f"  PHANTOM floor (non-converters {nonconv}, labels lawful here): thinned >= full at "
          f"{phantom} of {len(nonconv)} per bar; all-seed (episode-inflated mixed in): {allw} of {len(seeds)}")
    (XA.OUTDIR / "exp19_tabs_validate_BT_vs_proxy.json").write_text(json.dumps(tab1, indent=2))
    print("VALIDATE PASS: draw provenance recomputed (op 600 on THIS draw); deterministic; both cells read "
          "through both bars (cross-read live); full-N reproduces the committed B8 read at its own bar; "
          "drops matched-bar only; floors surfaced with the phantom/envelope distinction (ledger 43).")


# ---------------------------------------------------------------- smoke (positive-delta falsifiers)
def _smoke():
    print("exp19_tabs SMOKE — every guard is a reachable falsifier:")
    conv = {s: CAL._plant(True) for s in (0, 1, 2)}
    chance = {s: CAL._plant(False) for s in (0, 1, 2)}
    # (a) CROSS-READ half of the law (the panel's mutation-killer): cells at DIFFERENT widths — each cell's
    # runs must differ between the two matched rows. Both cells carry EPISODES (an episode's run scales
    # deterministically as ~len/width, 100 windows @300 vs ~43 @700 — a chance cell's short runs owe no such
    # movement, so it can't power this check). A _bar_read that ignores the passed W (the silent unlike-bar
    # tab: each cell quietly at its own bar) dies on both asserts.
    conv2 = {s: CAL._plant(True, epi=(200000, 230000)) for s in (0, 1, 2)}     # distinct episode placement
    t = matched_bar_tab19(cell("A", "stratified", 300, conv), cell("B", "stratified", 700, conv2))
    rA, rB = t["bars"][0], t["bars"][1]
    assert rA["a"]["runs"] != rB["a"]["runs"], \
        "SMOKE FAIL: cell A's read did not move across bars (width ignored — unlike-bar tab)"
    assert rA["b"]["runs"] != rB["b"]["runs"], \
        "SMOKE FAIL: cell B's read did not move across bars (width ignored — unlike-bar tab)"
    print(f"  (a) A@300/B@700, both episodic: both cells' runs move across the two bars "
          f"(A run {rA['a']['runs'][0]}→{rB['a']['runs'][0]}, B run {rA['b']['runs'][0]}→{rB['b']['runs'][0]}) "
          f"— the cross-read half is live  [mutation-killer]")
    # (b) equal widths COLLAPSE to one row, flagged — and the Fisher there is exact and directional
    te = matched_bar_tab19(cell("A", "stratified", 300, conv), cell("B", "stratified", 300, chance))
    assert te["bars_coincide"] and len(te["bars"]) == 1, \
        f"SMOKE FAIL: equal widths must emit ONE flagged row, got {len(te['bars'])} coincide={te['bars_coincide']}"
    p_fwd = te["bars"][0]["fisher_a_ge_b"]
    p_rev = matched_bar_tab19(cell("B", "stratified", 300, chance),
                              cell("A", "stratified", 300, conv))["bars"][0]["fisher_a_ge_b"]
    assert p_fwd == fisher_one_sided(3, 3, 0, 3) and p_rev == 1.0, \
        f"SMOKE FAIL: fisher direction wrong (fwd {p_fwd}, rev {p_rev})"
    print(f"  (b) equal widths → ONE row, bars_coincide=True; fisher fwd p={p_fwd:.4f}, rev p={p_rev:.1f}")
    # (c) PAIRED companion: same-seed cells get the McNemar-exact column (3 discordant, one-sided 1/8);
    # disjoint-seed cells get None + no context-only marker.
    assert te["bars"][0]["seed_overlap"] == [0, 1, 2] and te["bars"][0]["paired_exact_a_ge_b"] == 0.125, \
        f"SMOKE FAIL: paired-exact wrong for same-seed cells: {te['bars'][0]['paired_exact_a_ge_b']}"
    assert "CONTEXT-ONLY" in te["bars"][0]["fisher_model"]
    td = matched_bar_tab19(cell("A", "stratified", 300, conv),
                           cell("B", "stratified", 700, {s + 10: CAL._plant(False) for s in (0, 1, 2)}))
    assert td["bars"][0]["seed_overlap"] == [] and td["bars"][0]["paired_exact_a_ge_b"] is None \
        and "CONTEXT-ONLY" not in td["bars"][0]["fisher_model"], \
        "SMOKE FAIL: disjoint-seed cells mis-annotated"
    print(f"  (c) same-seed pair → paired exact 0.125 + Fisher marked context-only; disjoint pair → no paired col")
    # (d) EXACT schema (the panel killed the old superset/substring check): every row carries exactly the
    # matched-row keys; the tab exactly the tab keys — an ADDED comparison anywhere is a schema violation.
    assert all(set(r) == ROW_KEYS for r in t["bars"] + te["bars"] + td["bars"]), \
        f"SMOKE FAIL: row schema drift — {[sorted(set(r) ^ ROW_KEYS) for r in t['bars']]}"
    assert set(t) == TAB_KEYS and set(te) == TAB_KEYS, f"SMOKE FAIL: tab schema drift — {sorted(set(t) ^ TAB_KEYS)}"
    print(f"  (d) exact schema: rows == {sorted(ROW_KEYS)}; an added comparison anywhere violates it")
    # (e) READ-MIX guard fires
    try:
        matched_bar_tab19(cell("A", "full", 300, conv), cell("B", "stratified", 300, chance))
        raise SystemExit("SMOKE FAIL: read-mix was ACCEPTED — the two tabs collapsed into one")
    except AssertionError as e:
        assert "READ MIX REFUSED" in str(e)
        print("  (e) full-vs-stratified cell pair REFUSED — two tabs, never mixed  [guard fires]")
    print("SMOKE PASS: cross-read live (unlike-bar mutation dies), coincide collapsed+flagged, paired stats "
          "model-annotated, exact schema, read-mix refused.")


if __name__ == "__main__":
    torch.set_num_threads(1)
    if "--validate" in sys.argv:
        _validate()
    elif "--smoke" in sys.argv:
        _smoke()
    else:
        print("usage: --validate | --smoke   (B=T vs thinned-proxy two-cell tab / positive-delta falsifiers)")
