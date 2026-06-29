"""Step 0 — conflict-validity pre-flight (Stage-1, SPEC §0). Gates the rig; runs FIRST; surfaced
for review BEFORE any timing-sweep run.

The conflict stimulus tests the mechanism ONLY IF salience and association point in OPPOSITE
directions. Three checks, on the live commit, thresholds [RECONCILE] (set from measured headroom):

  (a) Salience -> distractor.  A no-word, capacity-open arm (vision alone) occupies the DISTRACTOR
      axis, NOT the category axis. (Else the word is redundant = empty-gap repeat; redesign.)
  (b) Category representable.  The capacity-open, CATEGORY-supervised substrate oracle recovers the
      category axis >= threshold, content-ablation-guarded. (Else words-can't-teach-unrepresentable
      = F3-analog; stop.) This is the "reachable-in-principle by the alternative path" oracle test:
      the category is representable by vision; the word only REDIRECTS, never supplies it (G1).
  (c) Conflict confirmed.  PAM's evocation diverges MORE across category than across distractor
      (the word makes category associatively productive despite the distractor being more salient).
      (If the distractor is just as divergent, the conflict is not clean.)

Output: conflict_validity.json. The conflict-strength ladder + timing sweep are committed ONLY after
all three pass. REVIEW GATE: surface conflict_validity.json before any timing-sweep run.

NOTE the discipline carried from Stage-0/exp03: this gate is admissibility ONLY — passing says nothing
about whether the word actually redirects occupancy (that is the rig's job, measured later). A flat
reversed-lift at a valid conflict is a legitimate (deep-negative) RESULT, pre-registered in the SPEC.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "src"))
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

import constants                                             # noqa: E402  (exp04)
from oracle_probe import _commit_hash                        # noqa: E402  (exp04)

from sculpt_config import SculptConfig, quick_sculpt         # noqa: E402  (exp05)
from sculpt_loop import SculptLoop                           # noqa: E402  (exp05)
from category_oracle import category_oracle_rec, raw_axis_recovery  # noqa: E402  (exp05)

# --- pre-registered Step-0 parameters (hashed into spec_hash) ---------------------------------
CONFLICT_PARAMS = dict(
    seeds=[0, 1, 2],
    run_steps=4000,                  # deployed-length arms for (a) occupancy + (c) divergence warmup
    oracle_steps=600,                # category-oracle training steps (mirrors Stage-0)
    # (a) salience: vision-alone must occupy distractor over category
    occupancy_sep=0.15,              # distractor_track - category_track must exceed this
    distractor_floor=0.60,           # vision must actually split the distractor (>= this)
    # (b) representability: category-oracle bar = chance + frac*(easy_ceiling - chance)
    margin_oracle_frac=0.25,
    easy_ref="r_category=r_distractor",   # the mild-conflict reference for the oracle ceiling
    # (c) conflict: PAM evokes more divergently across category than distractor
    divergence_sep=0.10,             # category_share = cat/(cat+dist) must exceed 0.5 + this
    # default deployed conflict cell (the timing sweep's reference cell)
    cell=dict(n_A=4, n_distractor=2, n_category=2,
              R_coarse=5.0, r_distractor=3.0, r_category=0.5, sigma_stim=0.20),
)


def spec_hash() -> str:
    return hashlib.sha256(json.dumps(CONFLICT_PARAMS, sort_keys=True).encode()).hexdigest()[:12]


def _cfg(seed, *, quick=False, **over):
    cell = dict(CONFLICT_PARAMS["cell"])
    cell.update(over)
    base = quick_sculpt(seed=seed, **cell) if quick else SculptConfig(seed=seed, **cell)
    return base


def _mean_pairwise(vs):                                    # vs: (k, D) -> mean pairwise L2
    if vs.shape[0] < 2:
        return 0.0
    dm = torch.cdist(vs, vs)
    off = ~torch.eye(vs.shape[0], dtype=torch.bool)
    return dm[off].mean().item()


def _evocation_divergence(loop: SculptLoop, *, associative: bool) -> dict:
    """Evocation-divergence across category vs distractor, on a warmed (intact) operator.

    associative=True: the word channel is isolated (all vision masked), so the read is PAM's
    word->vision evocation. distractor_divergence is then ~0 BY CONSTRUCTION (the word names
    category only) = the cleanest "associatively inert"; category_divergence>0 iff PAM learned a
    productive word->category association. Normalised by the evoke scale. associative=False is the
    full-context evocation (dominated by the salient distractor via vision) — a diagnostic showing
    how hard the redirect is. Read-only."""
    cfg = loop.cfg
    nA, nd, nc = cfg.n_A, cfg.n_distractor, cfg.n_category
    a_list, b_list = [], []
    for a in range(nA):
        for d in range(nd):
            for c in range(nc):
                a_list.append(a); b_list.append(d * nc + c)
    ev = loop.evoke_vision(a_list, b_list, associative=associative).view(nA, nd, nc, -1)
    scale = ev.reshape(-1, ev.shape[-1]).norm(dim=1).mean().item() + 1e-9

    cat_terms, dist_terms = [], []
    for a in range(nA):
        for d in range(nd):
            cat_terms.append(_mean_pairwise(ev[a, d]))           # across category (fix a, distractor)
        for c in range(nc):
            dist_terms.append(_mean_pairwise(ev[a, :, c]))       # across distractor (fix a, category)
    cat = statistics.mean(cat_terms) if cat_terms else 0.0
    dist = statistics.mean(dist_terms) if dist_terms else 0.0
    return dict(category_divergence=cat, distractor_divergence=dist, evoke_scale=scale,
                category_divergence_norm=cat / scale, distractor_divergence_norm=dist / scale)


def _axis_divergence(loop: SculptLoop) -> dict:
    """Step-0 check (c): associative (gate) + full-context (diagnostic) evocation divergence."""
    assoc = _evocation_divergence(loop, associative=True)
    full = _evocation_divergence(loop, associative=False)
    return dict(category_divergence=assoc["category_divergence"],
                distractor_divergence=assoc["distractor_divergence"],
                category_divergence_norm=assoc["category_divergence_norm"],
                distractor_divergence_norm=assoc["distractor_divergence_norm"],
                full_context=full)


def _run_arms(cfg, pin):
    """Matched intact + no-word SculptLoops (Phase-1 order); step both; return (intact, noword)."""
    intact = SculptLoop(cfg, pin)
    noword = SculptLoop(cfg, pin)
    for _ in range(cfg.steps):
        intact.step(no_word=False)
        noword.step(no_word=True)
    return intact, noword


def validate(verbose=True, out_path="conflict_validity.json", quick=False) -> dict:
    pin = constants.PinnedConstants()
    P = CONFLICT_PARAMS
    seeds = P["seeds"]
    run_steps = 1500 if quick else P["run_steps"]

    # ---- (a) salience + (c) divergence: matched arms per seed -------------------------------
    occ_rows, div_rows = [], []
    for s in seeds:
        cfg = _cfg(s, quick=quick, steps=run_steps)
        intact, noword = _run_arms(cfg, pin)
        occ = noword.dc_track(cfg.n_eval)                  # vision-alone occupancy (no word)
        div = _axis_divergence(intact)                     # warmed-operator evocation divergence
        occ_rows.append(occ); div_rows.append(div)
        # build-failure guards carried from Phase-1
        wpd = intact.word.param_delta()
        ga = intact.grad_attribution()
        if verbose:
            print(f"  seed {s}: [a] distractor_track={occ['distractor_track']:.3f} "
                  f"category_track={occ['category_track']:.3f} | "
                  f"[c] cat_div={div['category_divergence']:.3f} dist_div={div['distractor_divergence']:.3f} "
                  f"share={div['category_share']:.3f} | word_delta={wpd:.2g} "
                  f"gap3(PAM={ga['vision_grad_from_PAM']:.2g},JEPA={ga['vision_grad_from_JEPA']:.2g})")

    distractor_track = statistics.mean(r["distractor_track"] for r in occ_rows)
    category_track_va = statistics.mean(r["category_track"] for r in occ_rows)
    cat_div = statistics.mean(r["category_divergence"] for r in div_rows)
    dist_div = statistics.mean(r["distractor_divergence"] for r in div_rows)
    cat_share = statistics.mean(r["category_share"] for r in div_rows)

    # ---- (b) category representability: oracle at deployed cell + easy reference ceiling -----
    oracle_recs, abls = [], []
    easy_recs = []
    for s in seeds:
        cfg = _cfg(s, quick=quick)
        orc = category_oracle_rec(cfg, pin, steps=(200 if quick else P["oracle_steps"]))
        oracle_recs.append(orc["oracle_category_rec"]); abls.append(orc["ablation_collapsed"])
        # easy reference: mild conflict (category as salient as distractor) = the oracle ceiling
        easy = _cfg(s, quick=quick, r_category=cfg.r_distractor)
        eo = category_oracle_rec(easy, pin, steps=(200 if quick else P["oracle_steps"]))
        easy_recs.append(eo["oracle_category_rec"])
    oracle_category = statistics.mean(oracle_recs)
    easy_ceiling = statistics.mean(easy_recs)
    chance_c = 1.0 / P["cell"]["n_category"]
    oracle_threshold = chance_c + P["margin_oracle_frac"] * (easy_ceiling - chance_c)

    # raw salience bracket (cheap, capacity-open raw NC)
    raw_dist = statistics.mean(raw_axis_recovery(_cfg(s, quick=quick), axis="distractor") for s in seeds)
    raw_cat = statistics.mean(raw_axis_recovery(_cfg(s, quick=quick), axis="category") for s in seeds)

    # ---- verdicts (pre-registered) ----------------------------------------------------------
    a_pass = bool(distractor_track - category_track_va >= P["occupancy_sep"]
                  and distractor_track >= P["distractor_floor"])
    b_pass = bool(oracle_category >= oracle_threshold and all(abls))
    c_pass = bool(cat_share >= 0.5 + P["divergence_sep"] and cat_div > dist_div)

    rec = dict(
        commit_hash=_commit_hash(), spec_hash=spec_hash(), seeds=seeds, quick=quick,
        cell=P["cell"], chance_category=chance_c,
        check_a_salience=dict(distractor_track=distractor_track, category_track=category_track_va,
                              occupancy_sep=P["occupancy_sep"], distractor_floor=P["distractor_floor"],
                              per_seed=occ_rows, PASS=a_pass),
        check_b_representable=dict(oracle_category=oracle_category, easy_ceiling=easy_ceiling,
                                   oracle_threshold=oracle_threshold, margin_oracle_frac=P["margin_oracle_frac"],
                                   ablation_collapsed_all=bool(all(abls)),
                                   oracle_per_seed=oracle_recs, raw_distractor=raw_dist, raw_category=raw_cat,
                                   PASS=b_pass),
        check_c_conflict=dict(category_divergence=cat_div, distractor_divergence=dist_div,
                              category_share=cat_share, divergence_sep=P["divergence_sep"],
                              per_seed=div_rows, PASS=c_pass),
        conflict_params=CONFLICT_PARAMS,
    )

    problems = []
    if not a_pass:
        problems.append("(a) vision-alone does NOT occupy distractor over category -> word may be "
                        "redundant (empty-gap repeat); redesign the stimulus.")
    if not b_pass:
        problems.append("(b) category NOT representable by the substrate oracle (or ablation guard "
                        "failed) -> words-can't-teach-unrepresentable (F3-analog); stop.")
    if not c_pass:
        problems.append("(c) PAM does not evoke more divergently across category than distractor -> "
                        "conflict not clean (distractor not associatively inert).")
    rec["problems"] = problems
    rec["CONFLICT_VALIDITY_OK"] = not problems

    Path(out_path).write_text(json.dumps(rec, indent=2))
    if verbose:
        print(f"\n=== Step 0 conflict-validity (commit {rec['commit_hash'][:7]}, "
              f"spec {rec['spec_hash']}{' QUICK' if quick else ''}) ===")
        print(f"  (a) salience  : distractor_track={distractor_track:.3f} > "
              f"category_track={category_track_va:.3f}  -> {'PASS' if a_pass else 'FAIL'}")
        print(f"  (b) represent : oracle_category={oracle_category:.3f} (>= thr {oracle_threshold:.3f}; "
              f"easy_ceiling={easy_ceiling:.3f}; ablation_ok={all(abls)})  -> {'PASS' if b_pass else 'FAIL'}")
        print(f"      raw bracket: raw_distractor={raw_dist:.3f}  raw_category={raw_cat:.3f}")
        print(f"  (c) conflict  : category_div={cat_div:.3f} vs distractor_div={dist_div:.3f}  "
              f"share={cat_share:.3f} (>= {0.5 + P['divergence_sep']:.2f})  -> {'PASS' if c_pass else 'FAIL'}")
        print(f"  CONFLICT_VALIDITY_OK = {rec['CONFLICT_VALIDITY_OK']}")
        if problems:
            for p in problems:
                print("   PROBLEM:", p)
        print(f"  (record -> {out_path})")
        print("  >>> REVIEW GATE: surface this before any timing-sweep run. <<<")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="conflict_validity.json")
    ap.add_argument("--smoke", action="store_true", help="quick CPU config (minutes)")
    args = ap.parse_args()
    res = validate(out_path=args.out, quick=args.smoke)
    sys.exit(0 if res["CONFLICT_VALIDITY_OK"] else 1)
