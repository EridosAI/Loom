# Experiment 03 — Order-as-Content: Falsification Rig (SPEC)

**Lineage.** exp01 = pooling substrate (validated). exp02 = non-causal masked
completion under *explicit position indices* — i.e. order-as-**index** (validated, but
flagged: the explicit index is the unvalidated crutch). exp03 removes that crutch and
tests order-as-**content** while staying in isolation. It is the bridge rung between
exp02 (index, isolation) and the MVP (content, full loop).

---

## 0. Status & scope — read first

- **This is a falsification gate, not a validation.** A pass *licenses proceeding* to the
  Stage-0 MVP. It does **not** validate the full claim. The full claim — order-as-content
  under *co-developing encoders + pooling + convergence-driven drift* — is only meaningful
  in the loop and is the MVP's job, not this rig's.
- **Isolation rig.** Fixed synthetic generators. **No** learned encoders, **no** pooling,
  **no** collapse-control. The *only* learned component is the completion operator. Those
  other mechanisms are integration concerns; folding them in here would make a failure
  un-attributable.
- **Train-then-eval is fine here.** The no-train/run-split commitment is an MVP-level
  architectural constraint; an isolation rig that trains a completer then probes a property
  is sanctioned (exp02 did exactly this). We are *testing a property of* a completion
  operator, not *adopting* the operator into PAM.

---

## 1. The claim under test

> Position carried as ordinary content by an internal **drifting** signal supports
> random-access masked completion — specifically **cue-the-end → recover-the-beginning** —
> and this survives (a) **shuffling** the bundle set (no array axis to read), (b) the carrier
> having **no clean fixed coordinate** underneath (σ>0 genuine drift), and (c) the position
> signal being **entangled with content** rather than a separable side-channel (α→1; see §3).

**Two orthogonal "easy way out" axes, each with a degenerate corner that must be swept past
(not pinned):** **σ** (drift magnitude — σ=0 collapses position to an *index*) and **α**
(entanglement fraction — α=0 lets position be read from a clean *separable channel*). The
faithful deployed corner is **high-σ ∧ α=1**.

**Contrast (the thing it must beat):** order-as-**index** — a clean, fixed, invertible
position→state map. By the project's settled criterion, the *only* axis separating index
from content is **clean-and-fixed vs drifting-and-stochastic** (waveform/curvature/
periodicity/scalar-vs-population are all irrelevant — a clean phase angle is still an
index). So the discriminator must remove the clean coordinate, not merely the array axis.

**Carrier — a swept axis, not a fixed choice.** Dedicated (α=0, drift in its own dims) and
entangled (α=1, drift displaced into content coordinates) are the endpoints of a **continuous
entanglement fraction α** over the *same* drift signal (§3) — same supplier throughout, α only
relocates where the signal lives. So this passes the continuity test that index→content failed
(there the *source* changed, oracle→generator, unbridgeable; here it does not). Dedicated is
therefore the α=0 *corner* of a continuous family, **not a stand-in** — but for that same reason
it must be **swept past, not pinned** (pinning α=0 over-certifies the separable instance the MVP
won't deploy). Build attribution starts at α=0 (cleanest to read) and the sweep carries to α=1.
**Note α=0 is *less* degenerate than σ=0:** σ=0 makes position an *index* (wrong category);
α=0 keeps position as *content* but separable (easy instance of the right category) — so the
α-sweep de-risks the deployed entangled instance rather than fixing a category error.

---

## 2. Pre-registered failure conditions (WRITE THESE BEFORE RUNNING; do not change after seeing results)

The rig **passes** only if random access (under shuffle) stays high **(i)** across the σ-band
where position is recoverable *including the sub-band where the value→position map is ambiguous*
(no clean coordinate), **and (ii)** across the α-range up to entanglement (α→1, no separable
channel). It **fails** under any of:

- **F1 — array-axis reliance.** Random access drops under **shuffle** even at low σ.
  → the operator was reading the tensor slot index; order was in the axis, not the content.
- **F2 — index-in-costume.** Random access (shuffled) is high only in the **clean-coordinate
  zone** (σ→0) and drops as σ enters the **overlap zone**, *even though aggregate order is
  still recoverable there*. → the operator was reading a (soft) fixed lookup; order-as-content
  is false in the loop. (The σ-axis discriminator.)
- **F3 — not at-once.** k-pass iterative refinement materially beats the single completion
  pass. → completion is secretly autoregressive, not random-access.
- **F4 — separability-dependence.** Random access is high at **α=0** (dedicated side-channel)
  and collapses as **α→1** (drift entangled into content coordinates), *while the drift signal's
  own validity checks (§4) still hold*. → it passed only because the carrier was a clean
  separable channel — the easy way out; faithfulness to the deployed (entangled) mechanism is
  unproven. (The α-axis discriminator — the structural twin of F2.)

**Boundary (NOT a failure of the claim — must be excluded from the falsification window by
the validity checks):** at very high σ, aggregate order itself becomes unrecoverable
(context ≈ noise); recall collapses for *every* method. That is the **data ceiling**
(cf. exp02's "task going unlearnable, not the substrate"), not a falsification. The
order-recoverability validity check (§4) defines the upper edge of the testable band.

---

## 3. Data construction

Synthetic, exp02-shaped, with order moved out of the index and into a drifting carrier.

- **Bundle.** `bundle_i = [content_i ; context_i]` — content dims carry symbol identity;
  context dims carry position via drift. Dedicated (separable) context per the recorded
  carrier choice.
- **Content / sequence family.** A small fixed family of length-`L` sequences over a symbol
  set, constructed so the validity structure in §4 holds — crucially an **end-determines-
  begin bijection** (so cue-end→recover-begin is well-posed) with **position-varied symbols**
  (a symbol appears at ≥2 positions, so content alone never reveals position). Reuse exp02's
  generator shape (e.g. ~16 sequences, `L`≈6) as the starting point.
- **Context carrier — the load-bearing part.** A **per-sequence-stochastic accumulation**
  (OU-type / random-walk-with-drift). Requirements on the *class*, not a fixed formula:
  1. **No fixed position→value map across sequences.** Per-sequence-random start and/or
     drift, so the operator *cannot* learn a fixed `value → position` table. (A clean mean
     ramp `μ_i + noise` is **disqualified**: `μ_i` is fixed across sequences and therefore
     learnable as a soft index — it does not defeat F2.)
  2. **σ controls overlap.** σ is the swept knob. It must be tunable from a near-clean regime
     up into a regime where **adjacent positions' value distributions overlap** (order is not
     perfectly recoverable from context alone).
  3. **Genuine drift, not ramp-plus-removable-noise.** The realized trajectory *is* the
     signal; there must be nothing clean to denoise back to.
- **Entanglement fraction α — the second swept axis.** With drift `d_i` and content `c_i`, and a
  **fixed** injection `P: drift-space → content-space`, the bundle is
  `x_i(α) = [ c_i + α·P(d_i) ; (1−α)·d_i ]`. At **α=0** drift lives in its own dims (dedicated);
  at **α=1** drift is fully displaced into content coordinates and the side-channel dims are dead
  (entangled — position confounded with content in the same coordinates, "time felt not coded").
  α is continuous, the drift signal `d_i` is unchanged across α (same supplier), so dedicated↔
  entangled is a *setting*, not a swap. **`P` fixed is not an index leak:** it maps the
  *per-sequence-stochastic* `d_i` (σ>0, overlapping) to a stochastic displacement — there is still
  no fixed value→position map (the §4 map-non-fixedness check, computed on `d_i`, still holds).
  The faithful corner is **high-σ ∧ α=1**; both degenerate corners (σ=0, α=0) are swept past.

---

## 4. Validity checks (the structure that makes the test real — measured & logged at each σ, exp02-style)

A result is only interpretable if the data has these properties. Log them as a table over σ.

| Check | Requirement | Why |
|---|---|---|
| End-determines-begin (bijection) | holds | random access is well-posed |
| Position-varied symbols | symbols appear at ≥2 positions | content alone cannot give position |
| **Map non-fixedness** | same context *value* occurs at **different positions** across sequences | no fixed `value→position` lookup exists (defeats soft-index / F2) |
| **Adjacent overlap** | P(context out-of-order for adjacent positions) **> 0** in the test band | position is a *noisy* cue, not a clean coordinate — the σ>0 bite |
| **Aggregate order recoverable** | a simple sort/comparator on context recovers order **above threshold** in the test band | task is *solvable* — separates the discriminating band from the data ceiling |
| Chance baseline | `1/K` reported | the floor recall is measured against (cf. exp02 = 0.0625) |

The **testable σ-band** is where *map non-fixedness* + *adjacent overlap* are present (no
clean coordinate) **and** *aggregate order recoverable* is still high (above the data
ceiling). F2 is adjudicated **inside this band**.

**α-invariance of these checks.** All §4 checks are computed on the **drift signal `d_i`
itself**, not on the observed mixture `x_i(α)` — they certify the *signal* is content-like
(non-fixed, overlapping, recoverable), which α does not change (α only relocates `d_i`).
Recall, by contrast, is measured on the observed `x_i(α)` and *is* α-dependent. So the σ-axis
(via these checks) and the α-axis (via recall vs α) probe orthogonal easy-outs and do not
interfere: §4 says "the position signal is content, not index"; the α-sweep says "recall does
not depend on that signal sitting in a separable channel."

---

## 5. Conditions / protocol

Three runs. (Mirrors exp02's control / discriminator / boundary logic.)

- **Primary — DRIFT, shuffled — swept over BOTH σ and α.** Context = drift carrier; **bundle set
  shuffled every batch (train + test)**. *The discriminator.* The operator must read position from
  the context channel because the array axis carries nothing. **Two sweeps cross here** (an
  L-shape, not a full grid, to stay tractable while isolating each axis):
  - **σ-sweep at α=0** — adjudicates **F2** (index-in-costume) on the cleanest-to-attribute carrier.
  - **α-sweep at σ = σ\*** (σ\* chosen *inside* the overlap band, where F2/index is already excluded)
    — adjudicates **F4** (separability-dependence). Carry to **α=1**.
  - **Confirm the faithful corner** (σ in band ∧ α=1) explicitly — this is the regime closest to
    the deployed mechanism.
- **Control A — CLEAN, shuffled (positive control).** Context = clean fixed coordinate
  (σ=0); shuffled. Random access *should* succeed (a coordinate exists; it's just not on the
  axis). Confirms the rig can register success, and confirms CLEAN *fails* the
  map-non-fixedness / overlap validity checks (i.e. the validity checks discriminate
  index from content).
- **Control B — DRIFT, unshuffled (axis-leak check).** Same drift carrier, **not shuffled**
  (array order = true position, a deliberate leak). If the operator exploits the axis it will
  stay high even at **high σ** where context is uninformative. Primary-vs-ControlB at high σ
  reveals whether array order was being used → adjudicates **F1**.

**Operator-capability requirement (so shuffle is a real test, not a no-op).** The completion
operator must be **capable of using array position** (e.g. carries positional encodings, or
is otherwise position-aware) — otherwise shuffle is vacuous and F1 is untestable. A
permutation-invariant operator is **disallowed for this reason**. Within that constraint the
operator's internal form stays **neutral** (this is "test a property of," not "adopt"); a
tiny transformer-with-PE is the natural choice, exactly as exp02 used a tiny transformer to
demonstrate a property without putting one in PAM. Position must come from the **context
channel**, never from a privileged position input the architecture is built to consume.

---

## 6. Completion setup

- **Window.** `W ≥ 3` consecutive bundles (a maskable both-sides interior exists). Latent-out:
  completion runs directly on **concatenated content** (no distinct latent — settled).
- **Masking — non-causal, set-form.** Mask **content** cells; keep their **context** as the
  position-query key ("complete the bundle whose context is lowest" = recover the beginning).
  Because the window is fed as a (shuffled) set, "non-causal" here is the stronger
  permutation-form: there is no order axis to be causal about; the operator completes from
  *both/all* sides by content. (Masking context-from-content is an optional extension; not
  core.)
- **Cue-shape distribution — mandatory (exp02 rule #3).** Training masks must **sample the
  full cue-shape distribution** — sparse, one-sided, **endpoint-only**, interior — not just
  dense centered masking. Otherwise the operator learns **gap-filling**, not random access,
  and the property fails to appear (discovered late in exp02). With only the two channels and
  an all-/near-all-masked draw, completion must come from learned structure or not at all —
  this is the corner where the deferred *cross-cortex / from-weights completion* requirement
  (radar item) incidentally touches Stage 0; keep the distribution wide so it stays
  structurally available.
- **Loss.** **Embedding-distance on masked cells only**, distance/similarity-based —
  **not a free linear head** (exp01: a linear head leaks distinctions through shared weights).
- **At-once check.** Evaluate a **single** completion pass vs k-pass iterative refinement.
  Iteration must **not** materially improve (→ F3 if it does).

---

## 7. Readouts / metrics (report as tables over σ; mirror exp02 RESULTS)

1. **Random access, Primary (DRIFT, shuffled):**
   - cue-end → **begin recon** (the headline discriminator)
   - cue single position → **whole recon**, for each cued position (endpoint cues high;
     interior cues ambiguous by the validity structure)
   - plotted **vs σ** (at α=0) across the band, **and vs α** (at σ\*) up to α=1.
2. **Control A (CLEAN, shuffled)** and **Control B (DRIFT, unshuffled)** on the same metrics
   — A as positive control, B (esp. at high σ) as the F1 adjudicator.
3. **Validity table over σ** (§4) — including map-non-fixedness, adjacent overlap, aggregate
   order recoverability — so the testable band and the data ceiling are explicit.
4. **At-once:** single-pass vs k-pass whole-recon (delta should be ≤ 0).
5. **Chance baseline** `1/K`.

**Headline pass artifact:** Primary cue-end→begin-recon stays high **through the overlap
sub-band** (map non-fixed, adjacent overlap present, aggregate order still recoverable) **and
up to α=1** (entangled, no separable channel), while Control B reveals any axis leak at high σ
and Control A confirms the rig registers success and that the validity checks separate clean
from drifting.

---

## 8. What a pass licenses / what it cannot do

- **Licenses:** proceeding to the Stage-0 MVP with order-as-content as the order mechanism
  (carrier swept to **α=1** / entangled, σ>0 pin), rather than order-as-index.
- **Cannot:** validate order-as-content under co-developing encoders, pooling, and
  convergence-driven representational drift. That is the MVP integration test. A pass here
  removes the *cheap* ways the resolution could have been wrong (index-in-costume **and**
  separable-easy-out); it does not certify the loop.

---

## 9. One-line summary table

| Run | Context | Shuffle | Sweep | Adjudicates | Pass shape |
|---|---|---|---|---|---|
| Primary (σ-axis) | DRIFT (σ>0), α=0 | yes | **σ** | the claim + **F2** | high through the overlap band |
| Primary (α-axis) | DRIFT, σ=σ\* | yes | **α** | **F4** (separability) | high up to **α=1** |
| Control A | CLEAN (σ=0) | yes | — | rig sanity + validity-check discrimination | high; fails non-fixed/overlap checks |
| Control B | DRIFT | **no** | σ | **F1** (axis leak) | high at high σ ⇒ axis was leaking |

**Failures:** F1 (shuffle breaks it at low σ) · F2 (drops as overlap rises despite recoverable
order) · F3 (iteration beats single pass) · **F4 (drops as α→1 despite the drift signal's checks
still holding).** **Boundary, not failure:** collapse where aggregate order is itself
unrecoverable.
