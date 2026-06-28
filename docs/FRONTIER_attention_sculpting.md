# Frontier — Attention-Sculpting: Evocation-Driven Unpooling Against Intrinsic Decay

**Status.** `[PROPOSED]` · **paradigm-level, not yet mechanism.** This is the forward bet that
emerged from reading the Stage-0 empty-gap result. It is held provisionally per the
sit-with-it-before-canon discipline; the next design pass may challenge it and must not inherit
it as settled. It is kept **strictly separate** from the empty-gap verdict, which is `[SETTLED]`
and closed (PROJECT_STATE §9 / progress_log). One mechanism fork (§7) gates any build spec.

**One line.** The Stage-0 sweep falsified the *weak* reading of evocation-as-teacher (the word
helps vision *acquire* a distinction — redundant, null). The *real* mechanism is **attention-
sculpting**: evocation shapes *which distinctions a cortex bothers to maintain*, by holding
predictively-productive distinctions open against a constant intrinsic decay. This document is
the through-line from the negative to that mechanism.

---

## 1. What the empty-gap actually showed (and its precise scope)

The sweep tested whether naming improves vision's **acquisition** of a distinction (does the word
help vision split a blob into red-ball / green-ball). Result: `lift = intact_B − noword_B ≈ 0` at
every band, rate, and depth. Correctly typed: **not-F3** (the substrate oracle confirms B
representable across the admissible ladder → "word doesn't teach representable B," not "B
unrepresentable"); **not-F2** (autonomous resolution genuinely falls 1.0→0.0 → the opportunity
for the word to matter *existed*, and it still didn't). Plus the methodological catch:
PAM-grad *share* rose through the rapid phase but was **non-discriminating** — identical where the
word is provably inert — so naive trajectory-only instrumentation would have falsely reported a
paradigm-positive S-curve. Acquisition lift, not share, is the load-bearing metric, and it is null.

**The re-scoping (the eyesight metaphor).** Naming does not improve *acuity* — a child doesn't see
edges better because you said "ball." Naming organizes what the sensor already delivers into
*categories*. The sweep tested the **encoder layer** (discrimination — vision's own job); the
paradigm's claim was always about the **cortical-organization layer** (what is *worth*
distinguishing). The two sweep arms were **redundant by construction**: both pushed on acquisition,
the one operation the word is not for. Two visually-distinct things, vision tells apart on its own;
nothing in a predictive visual loss rewards *collapsing* dissimilar things into one category.

**Therefore — the scope, exactly:** the empty-gap bounds the **acquisition** claim only, at the
**encoder** layer, at the **Stage-0 operating point** (two cortices, no store, single scene,
weights-only). It says **nothing** about the development signal's *potency*, because that signal
was never exercised — there was no acquisition to drive; vision was just seeing. (Earlier framings
that read the null as "the teaching signal is too weak" are **withdrawn**: a signal can be
arbitrarily potent and move nothing if there is nothing to move.)

---

## 2. Two teaching mechanisms (the project built and falsified the redundant one)

- **(weak — tested, null) Acquisition.** Word helps vision *acquire* a distinction. Redundant:
  acquisition is vision's job; a co-present label adds nothing vision can't already do (or can't
  be given by a label).
- **(strong — untested, the real one) Attention-sculpting.** Word-association shapes the
  *organization* of representation — which distinctions are worth **maintaining**. This is the
  hunter vs the city kid: **same eyes, different attention.** It is driven by accumulated
  experience, it is intrinsically iterative, and it operates at the cortical-organization layer the
  sweep never touched.

---

## 3. The mechanism — re-pool the associatively-inert

Maturity is **iterative re-sculpting** of pooling state. A distinction vision makes that is
**associatively unproductive** is shed; freed capacity is pushed toward features that **bind**. The
mug: vision, alone, learns the *distinguishing* features (colour, texture — that's what reduces its
prediction error); the *category* feature (handle-and-hole) is less visually salient and carries no
discrimination reward, so vision won't prioritize it. The word is the only signal that says "these
different-looking things are the same kind."

**Why this needs a trigger the project does not yet have.** The existing re-pool trigger is
**disuse-driven** (PROJECT_STATE §4/§5): it sheds *unused* distinctions (low pull-apart + low
recent use). It does **not** shed *used-but-associatively-inert* distinctions — colour is
high-salience, high-use, freely discriminable; under the disuse trigger it would never re-pool. But
that is exactly the distinction attention-sculpting must tear down. The hunter doesn't *stop seeing*
colour; colour gets re-pooled *for categorization* because it doesn't earn associative keep.

---

## 4. The signal — evocation-divergence (goal-free, intrinsic to PAM-as-*predictive*)

"Associatively productive" has a purely local definition, requiring **no new quantity**:

> A distinction is **productive** iff its two sides **evoke different bundles**; **inert** iff PAM
> evokes the same thing across it.

Colour-split → PAM evokes the same companions either side (colour predicts nothing differentially)
→ **zero evocation-divergence**. Handle-split → PAM evokes different successors (mug→drink,
bowl→eat) → **large divergence**. This is read entirely off PAM's *own* evocation — **no downstream
task, no relevance map, no stored score.** It is the same move that resolved confidence:
confidence = a property of the evocation (basin sharpness); **relevance = a property of the
evocation (its divergence across a distinction).** Neither is added on top of the loop.

**The clean/cheat discriminator (binding).** The trigger may measure *whether* the two sides
predict **differently (about anything)** — never *what* they should predict. The moment an
implementation names a target ("re-pool because it fails to predict the word / some loss"), it has
smuggled an external objective and framing-1 returns. No named outcome: the word is just one slice
of the evoked bundle; the test is whole-bundle divergence.

---

## 5. The transport dissolution (the key structural result of this arc)

The hard problem was assumed to be: *how does PAM-space divergence become a re-pool force on a
specific distinction in a specific cortex* — a targeting/addressing problem, and the place a
relevance-controller (smuggled objective) would sneak in. **It dissolves under one inversion:**

> **Re-pool is not PAM-driven. Re-pool is intrinsic, constant, untargeted decay — a property of the
> cortex substrate. PAM drives *only* unpool (hold-this-open).**

Everything is *always* gently re-pooling, everywhere, with no signal. The only thing crossing the
cortex boundary is **maintain-separation** pressure. Consequences:

- **Inertness needs no detection.** It is the *absence of a hold*; the universal slow decay
  collapses whatever isn't held. You never measure "this is unproductive" and route a force to it —
  you only resist decay where divergence is high. Absence-of-signal is free.
- **No addressing.** Unpool force lands where evocation-divergence is high, which is *automatically*
  the right place — the signal **self-localizes** (the productive distinction *is* a place where the
  evoked bundle differs, and that difference *is* the hold, applied right there). Signal and target
  are the same object.
- **No smuggled objective is structurally possible.** PAM can only push maintain-separation; there
  is **no prune channel**. A relevance controller would need to issue *prune* verdicts and there is
  nowhere to issue them. Goal-free **by construction, not by discipline** — the knife-edge is
  removed by removing the knife.
- **Forgetting is non-reinforcement, driven by reality.** No forced forgetting (the wrong name
  isn't told to leave; it just isn't reinforced while the right one is — §2 biology). The system
  learns the world *as experienced* → **"give it a good childhood"** is an engineering statement:
  the environment's statistics are the training signal.

*(Canon promotion: Guiding-List candidate — reality is the teacher; the inner structure mirrors the
world as experienced.)*

---

## 6. The substrate has graceful memory in its physics — depth-graded re-pool force

Re-pool force is **depth-dependent**: steep at the leaves (detail cheap to lose), flat at the root
(structure sticky). For a 1→2→4→8 tree: 8→4 easy, 4→2 harder, **2→1 almost never**. This is not a
parameter choice — it is the mechanism by which **"forget the texture, keep the gist"** falls out of
the substrate, with *no separate consolidation process*:

- A vivid bell (fully unpooled, 8) under long disuse sheds *only at the detail end* → collapses to a
  coarse "brassy shape" (2) → **stops there** (2→1 nearly forceless). The concept survives the loss
  of its texture.
- The coarse node **still associates**: it remains bound in PAM to the bell-sound and the word
  "bell" (association lives on the surviving coarse node). Lost the detail, kept the concept and its
  bindings — exactly human memory of a rarely-seen thing.
- **Relearning is seeded.** Next encounter, unpool *re-elaborates from the surviving coarse node*,
  never from zero. The "learn quicker than forget" ratchet operating along the *depth* axis: the
  system never fully starts over on something seen even once, long ago.

This likely **subsumes** decay mechanisms PROJECT_STATE §5 treated as separate (downsampling/eviction
+ possibly drift) into one substrate property — **check this explicitly.** It coheres with the
nested-tree gating (leaf-first collapse + easy-at-leaves force *agree*; both shed detail before
structure). Connects to Guiding-List #5: **patterns crystallize, instances decay** — patterns are
the slowly-re-pooled coarse nodes; instances are the fast-fading detail; the depth-grading *is* that
distinction made mechanical.

---

## 6b. Later efficiency tiers (deferred — NOT the next pass)

Two reclamation mechanisms beyond occupancy-decay (§5/§6), both real, both out of scope now,
tiered by how settled they are. Logged so they are on record; neither touches the next pass.

**Tier 2 — envelope re-pool `[DEFERRED]`.** Occupancy-decay (§6) empties a distinction to gist but
leaves the *envelope* open — the tree branch stays committed to that concept's lineage, recoverable.
Over a lifetime against a fixed parameter budget (Cap-2, §4) that is a **one-way fill**: childhood
spends the envelope, the adult starves. Envelope re-pool reclaims the *envelope* of branches whose
features are chronically irrelevant — capacity that has sat unoccupied across many pool/unpool
cycles eventually hits envelope re-pool and is freed. This is the **deeper** efficiency (frees
*fresh* capacity, not just clears occupancy) and it is **emergent from envelope re-pool operating
over cycles — NOT a separate "pull-to-centre" force** (correcting an earlier framing). Re-entry
trigger: **observable capacity pressure on long runs** (Stage-0's short runs structurally cannot
reach it).

*Tradeoff it reopens:* envelope reclamation trades **recoverability for budget**. Occupancy-decay-
to-gist was fully recoverable (the coarse seed survived, §6); a reclaimed *envelope* may not be —
**critical-period dynamics**: once a branch is freed, re-committing it to the old concept may be
hard or impossible. Pin the envelope **open** for now (full recoverability while runs are short);
take on the recoverability-vs-budget tradeoff only when the budget actually bites.

**Tier 3 — cross-branch reallocation `[PROPOSED — paradigm-level, FENCED]`.** "Freed capacity
becomes available for *something else*" runs into Cap-2: in the fixed tree (§4), capacity freed at
branch position X is reusable only for whatever maps to X — **not** arbitrarily. True free
reallocation needs capacity to *cross* branches, which is the **migration §4 deliberately excluded**
("freed resolution stays within its own branch… cross-branch migration would dissolve Cap-2,
known-messy, excluded"). Reopening it is **paradigm-level, not a bolt-on**: the fixed tree is what
makes ancestors-gate-descendants, leaf-first collapse, and re-pool/unpool monotonicity
*well-defined*; a movable boundary breaks the gating law **and** the §7 coherence-check, all of
which would need re-deriving. The bar it must clear: *does a system with movable pool boundaries
still have well-defined re-pool/unpool dynamics, or does it thrash?* The distinction the paradigm
pass must draw: **reclaim-within-branch** (a dead branch's envelope freed for a new concept that
maps to the same position — plausibly safe) vs **migrate-across-branch** (true reallocation —
breaks Cap-2).

*Drift tripwire (binding, both tiers):* whatever drives reclamation must be the **existing local
signal** (confidence/divergence) as a *side-effect* — **never** a new force targeting "compact
strong concepts" or "minimise weights," which makes efficiency an **objective** (HANDOFF
drift-vector 5: "the moment 'minimise weights' becomes a global target, a global loss is back").
Efficiency stays emergent or it is not this architecture's.

---

## 7. The stability story — and the one mechanism fork that gates a spec

### Equilibrium (the self-defending structure)
Collapsing a *load-bearing* distinction raises the prediction error its loss would cause → that
raises evocation-divergence → which is **unpool force** → which arrests the collapse. The distinction
**can't fully re-pool because re-pooling it creates the very signal that re-inflates it.** An inert
distinction generates no restoring force as it collapses (PAM predicts the same thing all the way
down) → it fades quietly. **Structure defends itself through the cost of its own absence.** Goal-free
(all evocation-divergence; no external relevance signal).

### Stability condition + the stabilizer
A lagged restoring loop oscillates if the correction arrives only after irreversible damage. **The
stabilizer is the rate asymmetry: re-pool *slower* than unpool** (learn quicker than forget). Slow
collapse keeps the distinction mostly intact until "this is starting to hurt prediction" registers;
fast unpool then snaps it back before damage. The same asymmetry is the **developmental ratchet** —
accumulate structure, fade instances, a direction in time. (A symmetric rate is amnesiac: every lull
erases as fast as exposure builds; nothing accumulates.) This is **reference-and-relaxation** in a
new form — a *rate-asymmetric single mechanism* (slow direction is the reference for the fast),
rather than a two-tier reference; flag that its failure modes may differ (this fails by the *rate gap
being wrong*, not by a reference drifting).

### Depth-graded re-pool force (the variable-force idea, §6) is the *release* form
Build the depth-graded law in full; **pin it to a constant (depth-independent) slow rate for the
first rig**; release the grading once the constant-rate version is stable and characterised.
Constant-rate is the special case → no debt.

### THE OPEN FORK (gates any build spec): how is the unpool force actually computed?
Two readings, **not yet resolved**, and the empty-gap result bears on the choice:

- **Reading A — it is the existing gap-3 gradient, reinterpreted.** A pooling group whose members
  are bound to *different* PAM successors already receives **contradictory intra-group gradients**
  (exp01's pull-apart) → unpools; a group whose members predict the *same* bundle receives
  *consistent* gradients → no pull-apart → intrinsic re-pool collapses it. If so, the unpool side is
  **mostly already built**; what's new is only the *constant intrinsic re-pool* and the
  *depth-grading*. **But:** the empty-gap showed the gap-3 gradient *inert in the redundant case* —
  which either (i) means this signal is too weak, or (ii) doesn't bear on it, because redundancy (both
  members already predicting fine) is not the test. Only a **non-redundant** rig (§8) can tell which.
- **Reading B — a new explicit evocation-divergence computation.** In normal operation PAM is cued
  by the *actual current bundle*, not counterfactually by "member A vs member B" of a pooling group.
  Reading B says divergence-across-a-distinction must be computed explicitly (and integrated over
  some timescale) and coupled to the group's λ. More expressive; more machinery; more surface for
  drift to re-enter.

**This is the design pass that must precede a spec.** It is the analog of pinning gap-3's gradient
path ("backprop through concat, no detach") for Phase-1 — the load-bearing mechanism detail, and
exactly where forward-prediction or a smuggled objective could creep back. Resolve A-vs-B (and, if
B, the divergence definition + integration timescale + coupling to λ) **before** writing a build
spec.

### Genuinely open (the rig measures these; pre-register failure conditions)
- **Stability under *intermittent* predictive load.** Most distinctions matter *sometimes*. Does a
  distinction under fluctuating divergence find a **stable mid-depth**, or **hunt** up and down as
  divergence flickers? Slow re-pool + depth-grading *should* damp it to settle — but this is the
  dynamics question the first rig exists to answer. Pre-register: *stable depth vs oscillation*.
- **The rate gap** (the high-leverage knob). Too small → oscillate / amnesiac; too large → obsolete
  distinctions (a feature that *was* predictive and isn't anymore) never clear → can't re-sculpt to a
  changed world. The **stability-plasticity dilemma**, arriving through the re-pool rate. Possibly the
  gap must *breathe with surprise* (loosen when the world is surprising, stiffen when stable) — which
  is **confidence again**, the same currency; **watch it doesn't smuggle an objective.** Lean (this
  session): pin fixed + slow first, sweep inward, characterise → the surface is the reference for any
  variable law.

### Coherence check for the design session
Depth-graded **force law** × nested-tree **gating law** must cohere at the boundaries: a PAM-held
*descendant* must protect its *ancestor* from collapse (almost certainly correct — holding a
descendant open *is* a reason its ancestor shouldn't collapse — but state it so force-law and
gating-law are known to agree).

---

## 8. The rig this points to (specifiable once §7's fork is closed)

**Stimulus — the 4→8 conflict** (the structure the sweep entirely lacked): objects *mostly visually
dissimilar, sharing a few characteristics*, engineered so that **vision-alone provably keeps
same-category instances apart** (otherwise the word is redundant again — the F2-analog for this
experiment). Must contain both: a **distractor axis** (high-salience, freely splittable, but
associatively inert — the colour) and a **category axis** (less salient, associatively load-bearing —
the handle). 4→8 gives both "same category, different appearance" and "different category, similar
appearance" — the genuine same/different conflict, repeated.

**Readout — reversed lift** (the sharpest test of "the word teaches what to attend to"): does the
**intact arm re-pool the distractor axis** (give up the irrelevant split because the word reveals it
carries no associative weight) **while the no-word arm keeps it**? Same two-arm, calibration-
independent difference-of-arms discipline as the sweep — but the measured quantity is *distractor-axis
resolution*, and the prediction is **intact < no-word** (the word caused vision to shed a distinction
it would otherwise keep). Same eyes, different attention, measured directly.

**Build path (three stages; pin/sweep/release; the established method):**
1. Fixed wide ratio, depth-independent, slow re-pool. Get the equilibrium-with-PAM-unpool **stable at
   all**. Pre-register: intermittently-predictive distinction finds a stable depth vs oscillates.
2. Sweep the ratio inward; characterise where it oscillates — **the response surface** (as the
   unpool-clock rate was handled).
3. Release the depth-grading, using the surface as the reference for the force law.

Two cortices, **no store needed** — a targeted addition on the current Stage-0 rig, cleaner than
dragging in the store. Stays Stage-0-shaped in components; new in *stimulus*, *readout*, and the
*intrinsic-re-pool + evocation-driven-unpool* mechanism.

---

## 9. Where this sits relative to the closed result

- **Empty-gap (PROJECT_STATE §9):** `[SETTLED]`, closed. Acquisition tested, null, correctly scoped.
  Bounds the acquisition claim only; silent on development-signal potency. Untouched by this document.
- **This frontier:** `[PROPOSED]`, paradigm-level. The forward bet — attention-sculpting via
  evocation-driven unpooling against intrinsic decay — is the mechanism the empty-gap *did not* test
  and the human developmental story *requires*. Its purpose is the **inward loop**: environment →
  accumulated experience → internal structure → response → environment. That loop is what converts the
  architecture from "a fixed encoder with an association table" into "a thing that becomes what it has
  experienced" — the line between a tool and a developing mind, and the reason the project exists.

**Immediate next step is a design pass, not a build:** close §7's A-vs-B fork (and find the stability
reference for the rate gap). Then — and only then — the rig in §8 is specifiable, exp03-style.
