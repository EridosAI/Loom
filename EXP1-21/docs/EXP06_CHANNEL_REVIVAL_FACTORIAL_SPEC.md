# Exp06 — Channel-Revival Factorial — CC Implementation Spec

**What this is.** A pre-registered **diagnostic factorial** that locates the load-bearing lever behind
the dead evocation channel (`FRONTIER_attention_sculpting.md` §10 / `PROJECT_STATE_AND_MVP.md` §12.E).
It is **not the redesign** — it is the decomposition that *names* the redesign direction. Decompose-first,
in factorial form so interaction is **in the design**, not a post-hoc caveat. exp03-style: failure and
outcome conditions are pre-registered *here*, before any run.

**Status.** `[PROPOSED]` diagnostic. Reuses the built exp05 apparatus
(`experiments/05_attention_sculpting/`) and its neutral `(d)`-gate; adds **no new operator, no store, no
gain sweep**. Does **not** touch the `[SETTLED]` empty-gap (`PROJECT_STATE` §9).

**What it decides.** The contained operator-side fix was exhausted; the candidate levers are *jointly
movable but causally undecomposed* (§10.2). exp06 isolates which of three — **member-count ×
cue-diffuseness × PAM pool-penalty** — is load-bearing, with the **carrier bounded throughout** (the
adopted necessary-not-sufficient baseline). The surviving cell names the redesign direction: the B-step
(redesign) falls out of A's (diagnosis's) output instead of being guessed. exp07 (the redesign build) is
scoped *from* this result, not instead of it.

---

## `[RECONCILE]` convention

Every value tagged `[RECONCILE]` is set from the **live exp05 rig on the run commit** (Step-0
calibration), **not pinned by feel** — exp03 discipline. Round numbers are illustrative. Consolidated
register in §7.

---

## 0. Scope-lock — what is new, what is reused unchanged

**New (exactly three things):**
1. The **2×2×2 factorial harness** over the three factors (§1).
2. The **dual-anchor hard gate** + the **traverse validity check (V3)** + the **independent-toggle Step-0
   construction** (§2).
3. **Per-cell continuous `(d)`-grade logging** with a pre-registered interaction-evidence pattern (§4).

**Reused unchanged (binding):** the exp05 `PrototypeResonanceOperator`; **non-causal** masking; **no
stop-grad**; the neutral `(d)`-gate machinery (associated-different vs associated-same on random content +
content-ablation guard); **carrier bounding** (the within-window-relative bound, exp03-validated, adopted
as baseline). One code path. **Anything not in the "new" list above is out of scope** — in particular no
operator-form change, no carrier-as-a-factor, no completion-task change (those are exp07, *informed by
this result*).

---

## 1. The factors and their levels (carrier bounded in all cells)

| factor | clean level | deployed level |
|---|---|---|
| member-count | 2 | `many` `[RECONCILE]` (deployed multi-member value, from exp05 commit) |
| cue-diffuseness | sharp | `diffuse` `[RECONCILE]` (deployed cue-spread, from exp05 commit) |
| PAM pool-penalty | off (`pam_lam = 0`) | on `[RECONCILE]` (deployed `pam_lam`, from exp05 commit) |

- **Carrier is NOT a factor.** The within-window-relative bound is applied **identically in all 8 cells**
  as a standing baseline correctness fix (necessary-not-sufficient per §10.3). The factorial holds the
  carrier fixed-bounded and varies only the three factors above.
- **Clean corner** = `(2, sharp, off)` — the all-clean conjunction; the positive-control anchor (§2).
- **Dead corner** = `(many, diffuse, on)` — the deployed regime; the negative-control anchor (§2).

---

## 2. Step-0 — separability construction + dual-anchor hard gate (runs FIRST; surfaced for review)

Two Step-0 resolutions. **Neither the cube nor any interior cell is read until both resolve.**

### Step-0a — independent-toggle construction (two-outcome)
**Construct cue-diffuseness and member-count as *independent* knobs on the rig — independent-toggle
first.** Collapse only on **demonstrated structural coupling**.
- **Outcome A — separable:** diffuseness toggles at fixed member-count and vice-versa → the full **2×2×2**
  cube proceeds.
- **Outcome B — structurally coupled:** the rig cannot vary diffuseness independently of member-count →
  collapse to a **2×2** cube (member-count × pool-penalty); **report diffuseness as confounded-with-
  member-count**; proceed on the reduced cube. This is a first-class outcome, not a failure.

Output: `factor_separability.json` = {separable: bool, construction notes, commit_hash, spec_hash}.

### Step-0b — dual-anchor hard gate (both anchors evaluated BEFORE any cell `(d)` is read)
Both anchors are **hard gates**. Both must pass or the cube is **invalid** and no interior, single-toggle,
or pair cell is interpreted:
- **Clean corner must reach healthy capacity** — neutral-`(d)` ≥ `healthy` `[RECONCILE]` (~1.27 neighbourhood,
  the fresh-op clean-task capacity on the commit), ablation-guarded.
  **Clean-corner shortfall ⇒ the three named factors do not span the gap ⇒ the WHOLE cube is invalid ⇒
  mandate look-outside** (carrier-even-bounded / training dynamics / completion-task-posing). **First-class
  pre-registered outcome — NOT a cube expansion** (expanding mid-experiment would be drift).
- **Dead corner must collapse** — reproduce the deployed content-invariance (within-group prototype spread
  ~1e-9, random-input `(d)` ≈ `collapse_floor` `[RECONCILE]`).
  **Dead-corner-not-collapsing is equally invalidating ⇒ the harness does not reproduce the deployed regime
  ⇒ the cube is invalid; debug the harness, do not read cells.** Not a result.

Output: `anchor_gate.json` = {clean_corner_d, clean_corner_ablation, dead_corner_d, healthy_threshold,
collapse_floor, both_pass: bool, commit_hash, spec_hash}.

**REVIEW GATE:** surface `factor_separability.json` + `anchor_gate.json` **before** the cube is read.

### Cube validity — three conditions (anchors + traverse)
The dual-anchor gate proves the cube's **endpoints differ**; it does **not** prove the three factors are
the **axis the channel lives on**. The clean corner can reach healthy merely because it is a near-replica
of the already-known-healthy fresh-op clean task — so **"both anchors pass" can co-occur with "the factors
are not the lever,"** and reading the interior then would over-confidently name a factor (or land on
"irreducible conjunction") for unsound reasons. The likeliest real result, given the prior session, is
exactly this ambiguous **"anchors pass, interior muddled"** case. Three conditions, **all required before
any factor is named:**

- **(V1) Clean corner ~healthy** (Step-0b anchor).
- **(V2) Dead corner ~collapsed** (Step-0b anchor).
- **(V3) Traverse — ≥1 single-toggle measurably moves the channel off its adjacent corner**, by more than
  the measurement seed-spread `[RECONCILE]` (§7). Computed on the single-toggle cells (which the §4 primary
  read reads anyway), **and logged before any lever is named.** If **every** single-toggle is **pinned at
  its adjacent corner** (all toggles-from-dead stay ~dead, all toggles-from-clean stay ~healthy, nothing
  moves in between), the three factors **do not span the gap** → **look-outside fires as a measured
  result** — not inferred only from a clean-corner shortfall that may never occur.

**Validity = (anchors span the gap) AND (≥1 toggle traverses it).** Only then is the §4 interior read
valid. V3 is precisely what separates a **true** irreducible conjunction (singles/pairs *move*, super-
additively; only the triple reaches healthy) from **factors-not-the-lever** (nothing moves; the clean
corner is healthy for replica reasons): the discriminator is whether anything traversed.

---

## 3. The measurement — neutral `(d)`-gate, per cell

Reused from exp05, unchanged and content-agnostic by construction:
- **Neutral 2-member probe:** associated-different vs associated-same on **random content** (unrelated to
  any conflict stimulus). Revives liveness on the *neutral* probe — **never** on a conflict stimulus (the
  manufacturing discriminator).
- **Content-ablation guard:** ablate the differentiating association → `(d)` must collapse to ~chance
  (`ablation_floor` `[RECONCILE]`). A revival whose ablation does **not** collapse is a magnitude artifact
  (the init=1.0 `clamp_min` false positive, §10 provenance) — **rejected, never counted.**

Log the **full continuous `(d)`-grade per cell** (all 8, or 4 if collapsed), each with its ablation value
and seed spread.

---

## 4. The reading rule — binary decision at the healthy bar; grades as interaction evidence

### Decision rule — BINARY, at the healthy bar
A cell is `revived` **iff** neutral-`(d)` ≥ `healthy` **AND** ablation collapses. Below `healthy` =
**not revived** — the ~15%-capacity stack (§10.2) is below bar: a contaminated hint, **never a pass.**

**Primary read (only when validity V1–V3 holds, §2):** the three single-toggles *from the dead corner*
(main levers) + the three pair cells + the clean corner (the all-clean conjunction):
- **one single-toggle revived** → that factor is **load-bearing** → names the redesign (§5).
- **only a pair revived** → **joint lever** → redesign addresses both.
- **all singles below bar, all pairs below bar, only the clean corner revived — AND V3 holds (singles/
  pairs measurably moved, super-additively)** → **irreducible conjunction** → redesign **re-poses PAM's
  completion task** (not a single-factor operator tweak). *(If instead nothing moved — V3 fails — this is
  **not** a conjunction but factors-not-the-lever → look-outside, §2/§6.)*

### Graded `(d)` — interaction EVIDENCE, never a decision input
Log the continuous gradient across the cube. **Pre-registered interaction pattern:** *super-additivity
with a margin* — a pair's `(d)`-lift over the dead corner **exceeding the sum** of its two constituent
single-toggle lifts **by more than the measurement seed-spread** (`[RECONCILE]`, the revival-variance
calibration of §7) indicates the factors interact (the lever is the combination, not either alone). Near
the dead corner every lift is tiny and noisy, so the bare arithmetic comparison would fire on noise alone
— the margin is the same "don't read structure in noise" discipline as the binary decision, applied to the
graded read. The grades **enrich the
characterisation** of an interaction; they **never move** the binary lever-decision. This keeps the
manufacturing trap shut: **no tuning to a graded target — the decision is the bar crossing.**

---

## 5. Revival → redesign direction (the payoff; exp07 scoped from this)

| revived outcome | redesign direction it names |
|---|---|
| pool-penalty toggle | drop / reshape the λ2-tie on PAM's own prototypes (the proto-spread collapse, §10.1) |
| member-count | the multi-member completion **structure** |
| cue-diffuseness | how the **cue is posed** |
| pair / conjunction | **re-pose PAM's completion task** (the under-decomposed clean-2-member vs diffuse-multi-member gap, §10.2) |

**Reduced-cube caveat (Step-0a Outcome B).** On a collapsed 2×2, "member-count" is a **compound** factor
(member-count *and its entailed diffuseness*). A member-count revival on the reduced cube therefore maps to
the **completion-task** redesign direction, **not** the narrow multi-member-structure one — the factor is
compound, so the redesign cannot be attributed to member-count alone.

The surviving cell **is** the redesign-direction selection. exp07 (the channel-revival redesign build) is
scoped from it; it must clear the same neutral `(d)`-gate at the **healthy** bar (not a hint) before
Stage-1 (§8 of the rig spec) is re-attempted.

---

## 6. Pre-registered outcomes & failure conditions (all first-class)

- **Both anchors pass, one single-toggle revived (validity V1–V3 holds)** → clean lever named (§5). Proceed to exp07.
- **Both anchors pass, only pair/conjunction revived (V3 holds — singles/pairs moved)** → interaction / re-pose completion (§5). Proceed.
- **Traverse fails (V1, V2 pass; every single-toggle pinned at its corner — nothing traverses)** → the three
  factors **do not span the gap**; **measured** look-outside (carrier-even-bounded / training / completion-
  task-posing). This is the likeliest ambiguous case made decidable — **not** read as a conjunction.
- **Clean-corner shortfall (V1 fails)** → **cube invalid**; lever is **outside the three factors**;
  deliverable = "levers insufficient — look outside (carrier-even-bounded / training / task-posing)."
  **Do not expand the cube.** *(Second of the two look-outside triggers; V3-failure is the first and does
  not require V1 to fail.)*
- **Dead-corner-not-collapsing (V2 fails)** → **cube invalid**; harness does not reproduce the deployed
  regime; **debug harness; not a result.**
- **Factor coupling (Step-0a, Outcome B)** → reduced **2×2** cube; diffuseness reported confounded.
- **Any revival with non-collapsing ablation** → magnitude artifact (the `clamp` false-positive shape);
  **rejected, never counted** — the (d)-gate already earned this rejection once (§10 provenance).

---

## 7. Parameter block & `[RECONCILE]` register

### Pinned (structural)
| parameter | value |
|---|---|
| Cube | 2×2×2 (or 2×2 if Step-0a Outcome B): member-count × cue-diffuseness × PAM pool-penalty |
| Carrier | within-window-relative bound, **identical in all cells** (baseline, **not a factor**) |
| Measurement | neutral `(d)`-gate (associated-diff vs associated-same on random content + content-ablation), reused from exp05 |
| Decision | **binary** at the `healthy` bar; graded `(d)` logged as interaction evidence only |
| Anchors | clean corner (positive) + dead corner (negative) = **dual hard gate, read first** |
| Operator / masking / anchor | exp05 unchanged; non-causal asserted; no stop-grad; one code path |
| Every output row carries | `commit_hash`, `spec_hash` |

### `[RECONCILE]` (calibrate from the live exp05 commit)
| value | source |
|---|---|
| member-count `many` | deployed multi-member value (exp05) |
| cue-diffuseness `diffuse` (+ the Step-0a independent-toggle construction) | deployed cue-spread (exp05) |
| pool-penalty `on` (`pam_lam`) | deployed value (exp05) |
| `healthy` threshold | fresh-op clean-task capacity on the commit (~1.27 neighbourhood) |
| `collapse_floor` | deployed content-invariance floor (random-input `(d)`, ~1e-9 regime) |
| `ablation_floor` | ~chance under content-ablation |
| seed count | `[RECONCILE]` — dead signal is sharp (1e-9, all seeds, from ~t=300), but set ≥ enough to read **revival** variance (Phase-1's 3 was too few for characterisation) |

---

## 8. The line to hold

This is **decompose-first in factorial form**: the conjunction cell and the dual-anchor gate put
interaction *in the design*, not in a post-hoc rescue. The decision stays **binary at the healthy bar** —
graded `(d)` characterises, never tunes; nothing here moves the operator toward a wanted result. The
**surviving cell names the redesign** (B from A's output). The validity triad — **anchors span the gap AND
a toggle traverses it** — refuses to read a muddled interior over-confidently: a clean corner that is
healthy for replica reasons does not license naming a factor, and "factors don't span the gap" surfaces as
a **measured** result, not an inference. And if the cube is invalid — an anchor failing, or nothing
traversing — that is itself the **honest finding** (the lever is outside the three factors, or the harness
doesn't reproduce the regime), **not** a failure to be patched. The neutral `(d)`-gate at the healthy bar
is the liveness pass exp07 must clear before Stage-1 is re-attempted.
