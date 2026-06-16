# Experiment 02 — Non-Causal Masked Completion (order-as-content)

**Purpose.** Demonstrate, minimally, the claim the recall design rests on: **non-causal masked
completion gives random-access fill-in** — you can cue with *any* fragment (including the
*end*) and reconstruct the *whole* sequence, order included, **in one pass**. And demonstrate
that the **forward predictor (causal) fails** the property recall needs. This is the project's
"sideways, not forward" claim, isolated.

**Scope: deliberately minimal.** This claim is lower-risk than the pooling claim (it's close to
the established masked-LM property). The genuinely at-risk version — order-as-*content* in a
learned latent over *bundles*, with position-as-content, under drift — is **not** tested here;
it can only be tested once PAM exists. This rig's value is (a) a runnable artifact showing the
*forward* control failing the random-access property (directly useful to the anti-drift
purpose), and (b) the smallest possible confirmation before the property is built into PAM.
**Do not build for transfer or generality.** Smallest thing that fires the discriminator.

Context: `docs/PROJECT_STATE_AND_MVP.md` §6 (order-as-content vs order-as-operation).

> **Pre-registered failure conditions** below state what means the claim is wrong. Do not
> soften after seeing results.

---

## The one property that makes this test valid

**The cue must require order-information to complete.** If every sequence is unique, any
fragment trivially identifies its sequence and even dumb lookup passes — hiding whether order
is actually content. So:

- **Shared interior fragments.** Sequences that share an interior span but differ at the ends,
  e.g. `[A,B,C,D,E]` and `[F,B,C,D,G]` share `[B,C,D]`. Now the **end carries the information
  needed to reconstruct the beginning** — making end-cues-beginning a real test, not a lookup.
- **Same symbol at different positions** across sequences, so the model must encode *where* a
  symbol is, not just *which* symbols are present.

Without this structure the rig is invalid (the §0-analog trap).

---

## Data

- Small vocabulary (e.g. 8–16 symbols), fixed sequence length (e.g. 5–7).
- A constructed set with **shared interior fragments** and **position-varied symbols** as above.
- Enough sequences that the shared fragments genuinely create ambiguity that only the ends
  resolve (hand-construct or generate a family with controlled overlap).

## Model

- The **smallest masked-completion backbone** that trains (a tiny transformer encoder is
  appropriate *here* — this rig is specifically about attention *direction*; using one is not
  architectural drift because it is **not** being built into the system, only used to test a
  property).
- Train by masking positions and reconstructing them (masked-LM objective).
- **The only variable is attention direction:**
  - **Non-causal** — masked positions attend both left and right.
  - **Causal** — masked positions attend left only (this literally instantiates the forbidden
    forward / next-window predictor; it is the control).
- Everything else identical between the two (data, masking objective, size, training).

> **Simplification flagged (this is the deferred part):** the toy uses **explicit position
> encodings / sequence indices**. The real architecture's claim is **position-as-content** (order
> riding in the embedding, not explicit indices). This rig does **not** test position-as-content.
> State this in the README so a toy pass is not mistaken for the real claim.

## Tests (masking patterns at eval; #3 is the headline)

1. **Prefix-cued** (cue the start, mask the rest) — *control that both learned the sequences.*
   Both causal and non-causal should pass. (If a model fails here, a later failure is just
   undertraining, not the property.)
2. **Interior-cued** (cue the middle, mask both ends) — non-causal uses both sides; causal
   underperforms on the right-side gaps.
3. **Suffix-cued / end-cues-beginning** (cue the END, mask the BEGINNING) — **THE
   DISCRIMINATOR.** Non-causal should reconstruct the beginning; causal **cannot by
   construction** (start positions have no left context and it cannot attend right).
4. **Sparse-fragment** (cue 1–2 non-adjacent positions) — random access / whole-from-fragment
   in one pass.

## Metrics

- Per-position reconstruction accuracy, broken out by **cued region vs masked region**, for
  each masking pattern, for both models.
- For the headline test specifically: **accuracy on the masked *beginning* positions**, causal
  vs non-causal.
- A check that completion is **single-pass** (one forward call), not iterative.

## Pre-registered failure conditions

> **Order-as-content (random access) FAILS** if **non-causal** suffix-cued accuracy on the
> *beginning* positions is ≈ chance while its prefix-cued accuracy is high. → Masked completion
> does not give random access; the recall design needs rethinking.
>
> **Discriminator INVALID** if the **causal** control *also* passes suffix-cued beginning
> reconstruction. → The control is not isolating attention direction (should be impossible);
> investigate before trusting any result.
>
> **At-once FAILS** if reconstruction needs a decoding *order* or iterative refinement to
> converge — i.e. it is secretly autoregressive. → Not whole-completion; the compounding-error
> doom is not actually escaped. (Single forward pass must suffice.)

## Deliverables

- Data constructor (shared-fragment family), tiny model with a causal/non-causal switch, eval
  over the four masking patterns, `RESULTS.md` with per-test pass/fail against the conditions
  above and the causal-vs-non-causal beginning-reconstruction numbers.

## Explicit non-goals

No position-as-content, no bundles/latent, no drift, no transfer harness, no
difficulty/capacity sweep, no integration with anything. The property in isolation, smallest
form. The at-risk version is deferred to the PAM-setting test.
