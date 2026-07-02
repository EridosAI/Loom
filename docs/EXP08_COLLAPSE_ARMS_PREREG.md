# EXP08 — Collapse Diagnostic Arms: PRE-REGISTRATION (before any arm launches)

**What this is.** The pre-registered prediction table for the §10.12 collapse finding's
diagnostic arms (Gate-4 ruling, 2026-07-02). Written BEFORE any arm exists or runs; the
predictions below do not move after results. **All arms are DIAGNOSTIC — no arm is a fix**:
detach amputates the teaching channel, ties>0 is Tier-2-adjacent, re-weight is a knob.
Design revision happens after verdicts, at its own gate, in the frontier docs.

**The composed hypothesis under test** (FRONTIER §10.12, PLAUSIBLE): **engine** = the gap-3
no-detach TARGET-side pull via the vision-SELF reconstruction path (a contraction on
emissions); **permitting conditions** = sparse anchor (2 named targets / 16 members) +
spread 10× under-weighted (α=0.1 vs gain 1.0) + all L2 ties → 0 after t=1200. The word
path is a failed 2-point anchor, refuted as the engine.

**Base:** run commit lineage `ad23fc6`/`6768dfd`; deployed rig = SculptConfig defaults
(revival config); the entry-run artifact is the reference trajectory.

---

## The arms and their pre-registered predictions

| # | arm | single variable | prediction under the composed hypothesis | what refutes what |
|---|---|---|---|---|
| 1 | **No-word marathon** (the discriminator) | `no_word=True`, full horizon, cap 112500, seed 0 | **THE SHARPEST LINE: collapse NO SLOWER than the word-arm** (the engine is the self path; no-word removes only the failed anchor — if anything, onset earlier/equal; envelope no healthier) | No-word does NOT collapse by cap, or collapses materially slower → the word path is implicated as engine after all → the composed hypothesis's engine assignment REVISES |
| 2 | **Detached-target** | `detach()` on the PAM target (vision cells only), everything else deployed | **No collapse by 30k signature** (engine amputated): denominator envelope healthy, assessable fraction high, occupancy oscillation persists as in the no-word diagnostic | Collapse persists under detach → the engine is NOT the target-side pull → hypothesis engine REFUTED, suspect moves to remaining paths (cue-side/spread interaction) |
| 3 | **Spread re-weight** | `alpha_spread` 0.1 → 1.0 (parity with gain) | **Collapse prevented or strongly delayed** (counter-force restored): later onset if any, healthier envelope, assessable fraction ↑ | No effect on the signature → spread-under-weight was not a permitting condition; drop it from the composed hypothesis |
| 4 | **Ties > 0** | vision `lam2_lo` 0 → small ε (single knob; PAM tie untouched) | **Collapse prevented/delayed at a capacity cost** (the substrate tie resists emission drift; occupancy ceiling may drop — Tier-2-adjacent, diagnostic only) | No effect → ties-at-zero was not a permitting condition; drop it |
| 5 | **Vocab ladder** (anchor density) | word vocab 2 → 4 → 8 → 16 (construction below) | **Collapse onset / envelope / assessable-fraction ease MONOTONICALLY with vocab** (a denser frozen anchor holds more of the space open) | **Flat in vocab ⇒ the anchor is irrelevant to the collapse ⇒ the permitting-condition story revises** (the anchor-sparsity leg falls) |

**Seeds:** ≥3 per arm at 30k horizon (the early-signature readout below), EXCEPT arm 1
(full-horizon marathon, seed 0 — matched to the reference trajectory). Word-arm seed
extension (the n=1 gap on the reference itself) staged separately as compute allows, with
the word/no-word split pre-registered here.

---

## Arm-5 ladder construction (surfaced for the checkpoint read — the one open construction)

The word's vocab is raised by naming FINER partitions of the same 16-member space; the
stimulus geometry never changes (single variable = the label map, `_word_label(b)` + vocab):

| vocab | label map (member (a,b) → token) | what the anchor names |
|---|---|---|
| 2 | `b % n_category` *(the deployed rig — the reference cell)* | category only |
| 4 | `b` | both fine axes (distractor × category) |
| 8 | `(a % 2) * 4 + b` | half the coarse axis + both fine axes |
| 16 | `a * 4 + b` | full member identity (the Phase-1 Stage-0 word) |

**Named consequence (pre-registered, not a bug):** at vocab ≥ 4 the distractor becomes
word-NAMED, so the conflict premise (distractor associatively inert) no longer holds —
these cells are NOT the teaching rig and are never read for a teaching verdict. They are
anchor-density diagnostics only. The monotone-easing prediction is about the COLLAPSE
signature, not about redirect/lift.

---

## New columns (wired everywhere before any arm runs — both split what one lens read twice)

1. **Substrate-side weight-space Δ2** — `vision.pool` residuals (`pooling_depth` = mean
   ‖Δ2‖, `within_group_spread`) logged per eval window beside the emission-side columns.
   Splits **substrate-remerge** (Δ2 → 0: the weights themselves re-pool) from
   **emission-contraction** (Δ2 alive while emissions merge downstream) — the fix for the
   one-lens-read-twice caveat (`vision.emit` was the only eye on the collapse).
2. **Gradient-norm split on vision weights, word-path vs self-path, + masking-mix
   fraction** — at block cadence, ‖∂L_PAM/∂Δ2‖ measured under two controlled mask classes:
   (i) masked-vision-with-visible-WORD windows (the word path), (ii)
   masked-vision-with-visible-sibling-VISION windows (the self path); plus the empirical
   fraction of training windows in each class (the masking mix). Converts "anchor too
   sparse" from an inference into a measured ratio (how much of the pull vision actually
   receives is word-anchored vs self-referential).

Dynamics panels remain standing on every axis (an average never ships alone).

---

## Early-signature readout (what a 30k arm reads, pre-registered)

The reference trajectory's collapse signature at 30k horizon is the **collapse-and-regrow
oscillation**, not the terminal event: denominator envelope + dominant period (reference ≈
4800), envelope trend (reference: shrinking toward terminal failure), and **assessable
fraction** (reference: 394/1125 ≈ 35%). An arm "eases" the collapse iff (envelope trend ↑
or flat) ∧ (assessable fraction ↑) relative to the reference columns at matched horizon;
an arm "prevents" it if the denominator never sustains sub-floor blocks. All three are
windowed panel quantities; no point reads.

---

## Checkpoint ratifications + additions (Jason, 2026-07-02 — pinned pre-launch)

**Table RATIFIED arm-for-arm; ladder RATIFIED in the nested-refinement form** (four
properties confirmed: deterministic fixed maps identical across seeds, with the word event
riding its member at Δt_assoc=0 at every rung; proper nested refinement b%2 → b → (a%2,b)
→ (a,b); geometry untouched — density the only mover; clean density schedule 8→4→2→1
members-per-word). The coarse-first alternative DECLINED, reason recorded: the ratified
ladder anchors the observed dead axes in sequence (distractor at 4, coarse across 8→16) —
per-rung signal exactly where the collapse bit; coarse-first defers the first-implicated
axis to the weakest rung, and its sole benefit (conflict premise intact longer) is void
since arm-5 cells are fenced as never-teaching-reads.

**Shape signatures (pinned now — every rung halves members-per-word AND names a new axis
segment, so "monotone easing" alone cannot separate density from axis-coverage):**
- **(i) roughly uniform per-rung easing** → density-as-such (the sparsity leg in its
  general form);
- **(ii) easing concentrated at the rungs where a dead axis first gets named** — step at 4
  (distractor), further movement at 8/16 (coarse) — → **localized anchoring**: the anchor
  matters where collapse bites, not density per se;
- **(iii) flat in vocab** → anchor irrelevant; the leg falls.
Ambiguous between (i) and (ii) → the **coarse-first ladder is the pre-named follow-up
discriminator** — parked now, launched only after the one review.

**Anchor-side geometry — log, don't engineer:** same word-embedding construction rule at
every rung (2 = the deployed reference; 16 = the Phase-1 word; 4/8 from the same
generator, `WordCortex(D, vocab, seed=cfg.seed+1)`); pairwise separations logged in every
artifact. If the generator's pairwise geometry shifts materially across rungs → surface as
a CAVEAT, never fix mid-arm.

**Stimulus manifest (provenance, logging-only, one code path, written before wave 0;
derived LIVE from the constructors — never re-typed):** per run — member→word table across
all rungs + anchor embedding vectors + pairwise matrix; the visual construction as data
(axis roles, block geometry, magnitudes 5.831/0.5, σ); the staging timeline (t1/t2,
Δt_offset, Δt_assoc=0 riding its member, sampling rule + seed); and a STREAM-CONSISTENCY
ASSERT (first 200 sampled waves checked against the manifest's map at runtime — the
manifest is verified against the live stream, not a parallel claim). JSON + human-readable
MD + a per-rung assignment picture labeled **ILLUSTRATIVE-ONLY** (generative-coordinate
grid; a variance projection was rejected — 16 members = 4×4, any PCA overplots 4-into-1).

**Knob choice logged (not tuned):** arm-4 ε = `lam2_lo` 0 → **0.1** (1% of `lam_hi`=10 —
small enough not to re-close capacity, nonzero to resist drift).

## Sequence (pinned)

Checkpoint read of THIS table + the arm-5 construction (Jason — DONE, ratified above) →
arms build (new columns first, wired into the shared runner path) → arms run → **ALL
verdicts return to ONE review** — no arm's result is acted on alone; steps 5–6 of the gate
sequence stay BLOCKED throughout; the design revision (if any) happens after that review,
at its own gate, in the frontier docs.
