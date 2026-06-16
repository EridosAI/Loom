# Experiment 02 — Non-Causal Masked Completion (order-as-content)

Minimal, falsifiable test of the claim recall rests on: **non-causal masked completion
gives random-access fill-in** — cue *any* fragment (including the end) and reconstruct
the *whole* sequence, order included, **in one pass** — and the **causal (forward)
control fails** the property. This is the project's "sideways, not forward" claim,
isolated. Full design + pre-registered failure conditions: [`SPEC.md`](SPEC.md);
measured outcomes: [`RESULTS.md`](RESULTS.md).

## Run it

```bash
pip install -r requirements.txt
python run_tests.py            # full suite, writes RESULTS.md + figures/
python run_tests.py --quick    # fewer training steps (smoke test)
```

CPU-only, deterministic. Figures land in `figures/` (gitignored); `RESULTS.md` is
committed. Exits non-zero if a pre-registered failure condition trips.

## What makes the test valid

The cue must *require order information* to complete (otherwise any fragment is a
lookup key and even dumb retrieval passes). The data (`data.py`) enforces:

- **begin⇄end bijection** — the end *determines* the beginning (end-cues-beginning is
  a real inference), over a shared symbol set so the same symbol appears at different
  positions across sequences;
- **interior = h(begin), non-injective** — several begins share one interior fragment,
  so the interior alone is ambiguous; only the endpoints resolve identity.

Either endpoint therefore determines the whole sequence; the interior does not.
`run_tests.py` asserts these properties before trusting any result.

## The single variable: attention direction

Two otherwise-identical models (`model.py`): **non-causal** (masked positions attend
both ways) vs **causal** (left only — this literally instantiates the forbidden
forward / next-window predictor). Using a transformer here is *not* architectural
drift: it is not built into the system, only used to isolate attention direction.

## The discriminator

Cue the **end**, mask the **beginning**. Non-causal reconstructs the beginning
(attends right to the cue); causal **cannot by construction** — beginning positions
have no left context and it cannot attend right. See `RESULTS.md` for the
non-causal-vs-causal beginning-reconstruction numbers and the random-access sweep
(cue one position → recover the whole).

## ⚠ Flagged simplification (the deferred part)

This rig uses **explicit position embeddings** — order-as-*index*. The real
architecture's claim is order/position-**as-content** (order riding in the embedding,
in a learned latent over bundles, under drift). **This rig does not test that.** A
pass here is the (near-established) masked-LM property, not the at-risk claim, which
can only be tested once PAM exists.

## Non-goals (SPEC)

No position-as-content, no bundles/latent, no drift, no transfer, no capacity sweep,
no integration. The property in isolation, smallest form.
