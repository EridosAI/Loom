# Loom

A novel associative-memory architecture (Weft / PAM lineage). The system learns through
continuous experience rather than discrete training phases: modality-specific **cortices**
(each with its own representation space) feed a central associative operation (**PAM**) that
evokes expected experience from partial cues, every "wave," with no train/run distinction.
Memory is emergent predictive structure in weights, not an archive.

## Status

Architecture design is well-developed; first **mechanism** commitments made (the pooling
substrate, PAM-as-masked-completion, JEPA-pattern cortices). Now entering **isolated
mechanism validation** before integration.

## Repository

```
docs/                              Design documents (read in this order)
  HANDOFF.md                         How to work on this project (anti-drift discipline)
  PROJECT_STATE_AND_MVP.md           Full architecture, all decisions, status, suggested MVP
  substrate_description.md           The pooling-substrate spec (detail)
  association_cortex_operation_spec.md   The twelve characteristics (STABLE — do not re-litigate)

experiments/
  01_pooling_substrate/            First validation rig: does soft-tied weight pooling
                                   actually pool / unpool / re-pool? (see SPEC.md)

src/loom/                          Shared code (grows as experiments are integrated)
```

## Core principles (see HANDOFF.md for the full set)

- **One operation, every wave, never frozen.** No train/run split; development is the only mode.
- **Test mechanisms against functions, not vocabulary.** The recurring failure mode is drift
  into a conventional forward-in-time predictor wearing novel terms.
- **No plastic component without a slower-changing reference** (reference-and-relaxation).
- **Confidence is the universal currency** (credit-assignment, segmentation, decay, recall
  looseness — one signal, many roles).
- **Build the full mechanism, pin its variable part to a constant for v1, release later.**

## Current work

`experiments/01_pooling_substrate/` — validating the growth substrate in isolation, with
pre-registered failure conditions, before integrating it into the loop.
