# Experiment 03 — Order-as-Content: Falsification Rig

A **falsification gate** for the claim recall rests on: *position carried as ordinary
content by an internal **drifting** signal supports random-access masked completion
(cue-the-end → recover-the-beginning), and this survives (a) **shuffling** the bundle set,
(b) the carrier having **no clean fixed coordinate** (σ>0 drift), and (c) the position
signal being **entangled** with content (α→1).* A pass *licenses* proceeding to the
Stage-0 MVP with order-as-content rather than order-as-index; it does **not** validate the
full claim under co-developing encoders/pooling/drift (that's the MVP). Full design and
pre-registered failure conditions: [`SPEC.md`](SPEC.md); measured outcomes:
[`RESULTS.md`](RESULTS.md) (single-seed core gate) and [`RESULTS_stacked.md`](RESULTS_stacked.md)
(the faithful **high-σ ∧ high-α** corner + multi-seed verification, via
[`stacked_corner.py`](stacked_corner.py)).

This is the bridge rung between **exp02** (order-as-*index*, the explicit position index
was the unvalidated crutch) and the MVP (order-as-content, full loop). exp02's crutch is
removed here.

## Run it

```bash
pip install -r requirements.txt
python run_tests.py            # full suite, writes RESULTS.md + figures/
python run_tests.py --quick    # fewer steps (smoke test)
```

CPU-only, deterministic. Figures in `figures/` (gitignored); `RESULTS.md` committed.
Exits non-zero if a pre-registered failure condition trips or the rig is invalid (no band).

## The two easy-way-out axes (each a degenerate corner to sweep *past*, not pin)

- **σ — drift magnitude.** σ=0 collapses position to a clean *index*. The carrier is a
  per-sequence random-walk-with-drift (**random start + random positive slope** + σ noise),
  so the same context value occurs at different positions across sequences — **no fixed
  value→position table** (defeats the soft-index / **F2** easy-out). σ tunes adjacent-position
  overlap; begin/end are robust cumulative extremes, so a real testable band exists.
- **α — entanglement.** `x(α) = [E[sym] + α·d·u ; (1−α)·d]`. α=0 = drift in a dedicated
  separable channel; α=1 = drift displaced into the content coordinates, dead side-channel
  ("time felt, not coded"). The faithful deployed corner is **high-σ ∧ α=1**.

All §4 validity checks are computed on the drift signal `d` (never the mixture), so they
are **α-invariant**: the σ-axis certifies the signal is content-like; the α-axis asks
whether recall needs it *separable*.

## How each failure condition is adjudicated

| | what it catches | how |
|---|---|---|
| **F1** | array-axis reliance | shuffle (independent permutation every batch) must not break Primary in-band; Control B (unshuffled) shows the axis *is* exploitable at the ceiling, so the ablation is real |
| **F2** | index-in-costume | Primary begin-recon must *track the recoverable oracle* across the overlap band, not collapse where order is still recoverable |
| **F3** | not at-once | k-pass iterative refinement must not beat the single pass |
| **F4** | separability-dependence | begin-recon must survive to α=1, **and** an α=1 information-preservation probe must confirm position is still recoverable from the mixture (so a collapse would be separability, not a data ceiling) |

**Boundary, not failure:** at very high σ the aggregate order is itself unrecoverable
(data ceiling); the order-recoverability validity check marks the upper band edge and
excludes that region from F2/F4 adjudication.

## Design choices worth knowing (and why)

These came out of a design panel + two adversarial validity reviews, mirroring the lessons
of exp01/exp02:

1. **Nearest-prototype readout, no free linear head** (exp01 leak).
2. **Full cue-shape masking distribution** incl. endpoint-only (exp02 gap-filling lesson),
   masking only the *symbol codeword* while keeping the drift injection + context, so the
   position-query survives even at α=1 where the context dim is dead.
3. **Context-derived Fourier position key** in the operator: it extracts a scalar position
   cue from the bundle (context dim at α=0, content·u at α=1) and Fourier-encodes it so
   attention can rank a *continuous* carrier — position read from content, never the axis.
   (Without this the operator could only read the array slot, and even the clean positive
   control failed under shuffle — an operator-capability bug, caught and fixed.)
4. **Genuinely non-separable entanglement** (post-review fix): the drift is injected along the
   **top principal component of the codebook** at a content-matched scale, so at α=1 the
   best-linear-read R² of the drift is ~0.80 (not ~1.0) — reading position requires
   disentangling the symbol first. A reported R² gate *fails the rig* if the α=1 corner is a
   clean separable axis (which would make F4 vacuous); the info-probe checks recovery against
   the oracle so a collapse can't be a data-ceiling masquerade.
5. **Carrier-ablation gate** (post-review fix): because end→begin is a bijection, begin is
   content-solvable from the end cue — so the rig pre-registers that **zeroing the carrier
   must collapse begin-recon** (measured ~0.01–0.10), structurally forcing position-reading
   rather than content-memorization.
6. **At-once = single-pass whole-recon** (post-review fix): the OOD clean-codeword
   iterative-feedback was dropped; the whole window recovered in one forward pass is the
   evidence. See `RESULTS.md` "Caveats and scope" for honest limitations.

## ⚠ Deferred / non-goals (SPEC §0, §8)

Isolation rig: fixed synthetic generators, **no** learned encoders, **no** pooling, **no**
collapse-control — the only learned component is the completion operator. A pass removes the
cheap ways the resolution could be wrong (index-in-costume **and** separable-easy-out); it
does **not** certify order-as-content inside the loop. That is the MVP integration test.
