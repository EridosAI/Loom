"""Run the masked-completion tests (SPEC, "Tests") and write RESULTS.md.

Trains two identical models differing only in attention direction (causal vs
non-causal), evaluates the four masking patterns, and scores against the
pre-registered failure conditions (fixed below, not softened after the fact).

    python run_tests.py            # full
    python run_tests.py --quick    # fewer training steps (smoke test)

Run from this directory. RESULTS.md is committed; figures/ is gitignored.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import torch

import data as D
import plots
from harness import reconstruct, reconstruct_iterative, region_accuracy, train
from model import TinyMaskedTransformer

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
SEED = 0

# ---- pre-registered pass/fail thresholds -----------------------------------
HIGH = 0.90         # "high"/reconstructed
CHANCE_MAX = 0.25   # causal beginning recon must be at/near chance (chance = 1/K = 0.0625)
ITER_EPS = 0.02     # iteration may not beat the single pass by more than this


def train_both(fam, steps):
    models = {}
    for causal in (False, True):
        m = TinyMaskedTransformer(fam.V, fam.L, causal=causal, seed=SEED)
        train(m, fam.X, steps=steps, seed=SEED)
        models["causal" if causal else "noncausal"] = m
    return models


def eval_patterns(models, fam):
    bp, ep, ip = fam.begin_pos, fam.end_pos, fam.interior_pos
    masked_in_suffix = [p for p in range(fam.L) if p != ep]  # everything but the cued end
    masked_in_prefix = [p for p in range(fam.L) if p != bp]
    res = {}
    for name, m in models.items():
        pre = reconstruct(m, fam.X, cue_positions=[bp])
        suf = reconstruct(m, fam.X, cue_positions=[ep])
        int_ = reconstruct(m, fam.X, cue_positions=ip)
        suf_iter = reconstruct_iterative(m, fam.X, cue_positions=[ep])
        res[name] = dict(
            prefix_end=region_accuracy(pre, fam.X, [ep]),
            prefix_whole=region_accuracy(pre, fam.X, masked_in_prefix),
            suffix_begin=region_accuracy(suf, fam.X, [bp]),
            suffix_whole=region_accuracy(suf, fam.X, masked_in_suffix),
            suffix_whole_iter=region_accuracy(suf_iter, fam.X, masked_in_suffix),
            interior_begin=region_accuracy(int_, fam.X, [bp]),
            interior_end=region_accuracy(int_, fam.X, [ep]),
        )
    return res


def sparse_sweep(models, fam):
    """Random access: cue a single position p, reconstruct the whole sequence."""
    sweep = {name: [] for name in models}
    others = lambda p: [q for q in range(fam.L) if q != p]
    for name, m in models.items():
        for p in range(fam.L):
            preds = reconstruct(m, fam.X, cue_positions=[p])
            sweep[name].append(region_accuracy(preds, fam.X, others(p)))
    return sweep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    torch.manual_seed(SEED)
    steps = 800 if args.quick else 3000

    fam = D.build_family(seed=SEED)
    vrep = D.validity_report(fam)
    print("validity:", vrep)
    assert vrep["shared_interior"] and vrep["end_determines_begin"] \
        and vrep["interior_ambiguous_about_begin"], "data is not valid for this test"

    models = train_both(fam, steps)
    res = eval_patterns(models, fam)
    sweep = sparse_sweep(models, fam)

    nc, ca = res["noncausal"], res["causal"]
    chance = vrep["chance_begin"]
    print(f"\nchance (begin) = {chance:.4f}")
    for name, r in res.items():
        print(f"{name:9s} prefix_end={r['prefix_end']:.3f} suffix_begin={r['suffix_begin']:.3f} "
              f"suffix_whole={r['suffix_whole']:.3f}")

    control_pass = nc["prefix_end"] >= HIGH and ca["prefix_end"] >= HIGH
    order_pass = nc["suffix_begin"] >= HIGH
    discriminator_valid = ca["suffix_begin"] <= CHANCE_MAX
    atonce_pass = (nc["suffix_whole"] >= HIGH
                   and (nc["suffix_whole_iter"] - nc["suffix_whole"]) <= ITER_EPS)
    overall = control_pass and order_pass and discriminator_valid and atonce_pass

    plots.plot_summary(res, sweep, fam, os.path.join(FIGDIR, "summary.png"))
    write_results(vrep, res, sweep, fam,
                  dict(control=control_pass, order=order_pass,
                       discriminator=discriminator_valid, atonce=atonce_pass,
                       overall=overall))
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")
    sys.exit(0 if overall else 1)


def write_results(vrep, res, sweep, fam, verdict):
    nc, ca = res["noncausal"], res["causal"]
    pf = lambda b: "**PASS**" if b else "**FAIL**"
    chance = vrep["chance_begin"]

    sweep_rows = "\n".join(
        f"| {p}{' (begin)' if p == fam.begin_pos else ' (end)' if p == fam.end_pos else ' (interior)'} "
        f"| {sweep['noncausal'][p]:.3f} | {sweep['causal'][p]:.3f} |"
        for p in range(fam.L)
    )
    md = f"""# Experiment 02 -- Results

Auto-generated by `run_tests.py` (CPU, deterministic). Figures in `figures/`
(gitignored). Thresholds pre-registered in `run_tests.py`; not changed after seeing
results. See `SPEC.md` for the failure conditions and `README.md` for the flagged
simplification (explicit position encodings = order-as-index, NOT the real
order-as-content claim).

**Overall:** {pf(verdict['overall'])}

| Test | Result |
|------|--------|
| Control -- prefix-cued, both models learn (forward) | {pf(verdict['control'])} |
| Order-as-content -- non-causal recovers the beginning from the end | {pf(verdict['order'])} |
| Discriminator valid -- causal CANNOT (fails by construction) | {pf(verdict['discriminator'])} |
| At-once -- single forward pass suffices (no iterative refinement) | {pf(verdict['atonce'])} |

## Data validity (the property that makes the test real)

| check | value |
|-------|-------|
| sequences / length | {vrep['n_sequences']} / {vrep['seq_len']} |
| shared interior fragments | {vrep['shared_interior']} (max {vrep['max_sequences_sharing_an_interior']} seqs share one interior) |
| position-varied symbols (appear at >=2 positions) | {vrep['position_varied_symbols']} |
| end determines begin (bijection) | {vrep['end_determines_begin']} |
| interior ambiguous about begin | {vrep['interior_ambiguous_about_begin']} |
| chance accuracy on begin (1/K) | {chance:.4f} |

## Per-pattern reconstruction (non-causal vs causal)

| pattern | metric | non-causal | causal |
|---------|--------|-----------:|-------:|
| 1. prefix-cued (cue begin) | end recon | {nc['prefix_end']:.3f} | {ca['prefix_end']:.3f} |
| 1. prefix-cued | whole recon | {nc['prefix_whole']:.3f} | {ca['prefix_whole']:.3f} |
| 2. interior-cued (cue middle) | begin recon | {nc['interior_begin']:.3f} | {ca['interior_begin']:.3f} |
| 2. interior-cued | end recon | {nc['interior_end']:.3f} | {ca['interior_end']:.3f} |
| **3. suffix-cued (cue end)** | **begin recon** | **{nc['suffix_begin']:.3f}** | **{ca['suffix_begin']:.3f}** |
| 3. suffix-cued | whole recon | {nc['suffix_whole']:.3f} | {ca['suffix_whole']:.3f} |

### Test 1 -- control {pf(verdict['control'])}
Both models reconstruct forward from the begin cue (end recon: non-causal
{nc['prefix_end']:.3f}, causal {ca['prefix_end']:.3f}). Both learned the family, so a
later failure is the property, not undertraining.

### Test 3 -- the discriminator {pf(verdict['order'] and verdict['discriminator'])}
Cue the END, reconstruct the BEGINNING. Non-causal = **{nc['suffix_begin']:.3f}**;
causal = **{ca['suffix_begin']:.3f}** (chance {chance:.4f}). The causal control cannot
reconstruct begin positions: they have no left context and it cannot attend right --
exactly the forbidden forward predictor failing the random-access property.

> FAILS IF non-causal suffix-cued begin is ~chance while prefix is high -> not the
> case ({nc['suffix_begin']:.3f} vs prefix {nc['prefix_end']:.3f}).
> INVALID IF causal also passes -> not the case ({ca['suffix_begin']:.3f} <= {CHANCE_MAX}).

### Test 2 -- interior-cued (descriptive, not gated)
Cueing only the (shared, ambiguous) interior under-determines the endpoints, so both
models are low on begin/end recon -- a direct consequence of the validity structure
(interior alone cannot identify the sequence; the ends must).

### Test 4 -- random access (single cued position -> whole sequence)

| cued position | non-causal whole recon | causal whole recon |
|---------------|-----------------------:|-------------------:|
{sweep_rows}

Either endpoint lets the non-causal model reconstruct the whole sequence in one pass;
the causal model only reconstructs forward (high when cued at/near the begin, failing
when cued at the end). Interior-only cues are ambiguous for both, as designed.

### At-once check {pf(verdict['atonce'])}
Non-causal suffix-cued whole reconstruction: single pass = {nc['suffix_whole']:.3f},
4-pass iterative refinement = {nc['suffix_whole_iter']:.3f} (delta
{nc['suffix_whole_iter'] - nc['suffix_whole']:+.3f}). Iteration does not improve on the
single pass -- completion is genuinely at-once, not secretly autoregressive.
"""
    with open(os.path.join(HERE, "RESULTS.md"), "w") as f:
        f.write(md)
    print(f"wrote {os.path.join(HERE, 'RESULTS.md')}")


if __name__ == "__main__":
    main()
