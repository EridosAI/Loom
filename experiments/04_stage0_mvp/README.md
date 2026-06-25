# Experiment 04 — Stage-0 MVP (Phase-1 core)

The first **integration** in the Loom program: the smallest system that runs the one PAM
operation end-to-end — **vision cortex + word cortex + a non-causal masked-completion
associator** — under continuous experience. It fuses the three validated isolation rigs
(exp01 pooling substrate, exp02 non-causal completion, exp03 order-as-content) in one loop.

Built from `docs/STAGE0_MVP_SPEC.md`. Purpose is **observability, not capability**: every
choice is judged by whether it keeps *gap-3 fusion* and the *anchor decomposition* readable,
never by "does it perform." This pass implements **Phase-1 core**; Phase 2 (Readout A collapse
ladders), the gain-rate sweep, and Readout O are deferred per the spec's Phase 1 → Phase 2
staging.

## Run

```bash
python run_stage0.py --selftest          # cue-shape coverage (6 families) + verdict-table self-tests
python run_stage0.py --quick             # CPU-deterministic smoke, single seed (~1-2 min)
python run_stage0.py --quick --seeds 3   # 3-seed headline Readout G verdict
python run_stage0.py                     # full config (longer)
```
Writes `RESULTS.md`. Shared primitives live in `../../src/loom/` (imported as `loom`).

## Layout

| File | Role |
|---|---|
| `encoders.py` | Vision = plastic pooling embedder + `L_JEPA` (within-dwell next-wave prediction); Word = frozen lookup (the anchor, lr=0) |
| `pam_operator.py` | The operator: prototype-resonance over a 2nd pooling population, **no softmax** (inverse-distance/Shepard kernels), no free head, at-once, no PAM latent |
| `stream.py` | Continuous single-object stream: A decoy / B probe, A/B **dwell-stable** while the entangled order-drift varies within-dwell; α=1 carrier + nuisance confound (no clean slot) |
| `loop.py` | The single PAM wave loop: one at-once completion + one step, **no detach** (gap-3 target-side gradient on the masked vision slot), asymmetric plasticity, `L_total = gain·L_PAM + α_spread·L_spread + L_JEPA` |
| `controllers.py` | The three separate rates: unpool clock (gate=1), gain ramp (gates off), curriculum (contrast-not-rename) |
| `validity_probe.py` | Pre-loop 4-check admissibility gate (A-salience, floor_B, ceiling_B different-regime oracle, separability) — never a success signal |
| `readouts.py` | Readout G (gap-3 fusion) + Readout D (order-as-content), pre-registered tables-as-data |
| `structural_signals.py` | char-7 (no phase split) + pooling-does-something |
| `logging_block.py`, `constants.py`, `verdict.py` | §10 logging block, pinned constants, verdict primitives + Stage-3 wrong-reason guard |
| `run_stage0.py` | Phased Phase-1 runner; build-failure invariants every eval window; auto-writes `RESULTS.md` |

## What "green" means here

The **build** is correct iff: cue-shape coverage hits all six families; the verdict-table
self-tests pass; the validity probe locks; and every eval window passes the build-failure
invariants — `word_param_delta == 0` (anchor frozen), `vision_grad_from_{PAM,JEPA} > 0` (gap-3
path alive, no detach), `max_coord_r2 < tau_entangle` (carrier stays entangled, no clean slot),
operator has no softmax-attention, one step per wave (char-7).

The **readouts** then report the science honestly. A clean gap-3 PASS (Readout G) is **not**
expected from the `--quick` smoke and is a follow-up (full config + suppressing autonomous
B-resolution so the no-word arm stays in the floor-band). The Stage-3 discipline flags
`WRONG_REASON`/seed-instability rather than declaring a false PASS.

## Discipline held (spec §12)

Non-causal masking; block-level whole-slice masks; distance/prototype readout (no free head);
**no softmax-attention** (operator is inverse-distance resonance, not a masked transformer);
order-as-content never order-as-index (`max_coord_r2` gate every window); three rates kept
separate; one code path (no train/run branch).
