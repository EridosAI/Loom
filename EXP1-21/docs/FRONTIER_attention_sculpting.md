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

### FORK RESOLVED — Reading A: occupancy is the existing gap-3 gradient's intra-group disagreement
The capacity/occupancy split (§5/§6b) resolved this. Once divergence only has to **fill and hold**
capacity the clock already opened — never *open* it — the occupancy force is exactly exp01's
validated mechanism: intra-group gradient disagreement drives members of an already-loosened tie to
differentiate.

**The load-bearing identity:** *per-distinction divergence = per-instance convergence error
aggregated across the group's members* — the same signal at two descriptions. Trace it: mask a
member's vision slot, PAM evokes it from co-present context, backprop convergence error into the
(still-shared) tied weights. If the two members are associated with the **same** PAM successors
(colour → same word/context), PAM evokes the same target for both → gradient pulls both the same way
→ **consistent → no pull-apart → intrinsic re-pool keeps them merged** (inert distinction, correctly
not occupied). If associated with **different** successors (handle → different word/context), PAM
evokes different targets → gradient pulls them apart → **contradictory → pull-apart → they occupy
the opened capacity** (productive distinction, correctly occupied). "Do the two sides evoke different
bundles" *is* "do the members receive contradictory convergence-error gradients." No separate
divergence computation needed.

**So the unpool/occupy side is mostly already built** (the gap-3 gradient, validated alive in
Phase-1). Genuinely new: only (1) **constant intrinsic re-pool** (the substrate currently has
*disuse-triggered* re-pool; this needs constant-force decay) and (2) depth-grading (release stage).

**The one line the rig must assert (or A collapses into a predictor):** convergence error must come
from **non-causal** evocation (mask evoked from *all co-present context*, not from predecessors —
HANDOFF live-vector 1 / exp02). Causal masking would make the occupancy gradient a *next-step
prediction error*, silently converting "maintain associatively-productive distinctions" into
"maintain temporally-predictive distinctions" — a different, wrong objective. A holds *only* under
non-causal masking.

**Bootstrap (broken by the anchor):** occupancy can't begin until PAM has *learned* enough
association to evoke differentially — but the word distinction is *given* (the anchored word cortex
emits distinct words from t=0), so PAM acquires word↔context association first, *then* its
differential evocation drives vision's occupancy. Occupancy **lags** PAM's word-association
acquisition — a clean signature that the split is driven by association, not by vision splitting
alone. (This lag is the manipulated variable in §8.)

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

## 8. The rig (fork closed — now specifiable; build spec is the companion doc)

**Mechanism under test:** Reading A (§7) — occupancy = gap-3 intra-group gradient disagreement,
sourced from PAM's **anchored-word-seeded** associations, **non-causal masking asserted**. New
substrate piece: **constant intrinsic re-pool** (depth-grading deferred to release).

**Stimulus — the 4→8 conflict** (the structure the empty-gap sweep entirely lacked). Objects
*mostly visually dissimilar, sharing a few characteristics*, engineered so **vision-alone provably
occupies the wrong (salient) axis**. Two axes: a **distractor axis** (high-salience, freely
splittable, associatively *inert* — colour) and a **category axis** (less salient, associatively
load-bearing — handle). 4→8 gives both "same category, different appearance" and "different category,
similar appearance." *Control that makes the whole thing valid:* the timing sweep must run on **this
conflict stimulus, not a visually-resolvable one** — else vision succeeds alone, lift is null across
all conditions for the wrong reason, and timing looks irrelevant when really the stimulus didn't need
the word.

**Primary manipulation — word-vs-capacity timing.** The variable that "leads or lags" is **not** two
onsets but two *confidence trajectories*: when capacity has opened enough to host the distinction
(a point on the unpool ramp) vs when PAM's word-association is confident enough to evoke
differentially (a learning curve built over repetition). Operationalized as a single scalar:
**unpool-onset delay** relative to word-exposure (word channel active and PAM associating from t=0;
the *clock onset* is delayed by a swept offset). Negative offset = words-before; zero = same;
positive = words-after. *Experimental instrument only* — deployment-realism is the **rate-ratio**
(how fast association builds vs how fast capacity opens), not a delay; do **not** read a timing
result as a developmental-pacing finding (same caution as §12-B's rate-is-a-locator line).

**Readout — two timescales** (richer than a single reversed-lift number):
- **Fast (first-growth-phase efficiency):** does the word redirect occupancy from distractor to
  category *before* vision commits to the distractor? Measured as reversed lift — intact arm
  *fails to occupy / re-pools* the distractor where the no-word arm occupies it (calibration-
  independent difference-of-arms, as in the sweep). Expected strong at words-before, weak/absent at
  words-after.
- **Slow (does the cycle provide rate-flexibility):** does occupancy *eventually* reach the category
  axis and shed the distractor across re-pool/unpool cycles, **regardless of timing**? Requires the
  run to cover **≥1 full distractor re-pool/re-unpool cycle** (esp. words-after — run it Phase-1-short
  and recovery is missed, mis-read as permanent failure; the empty-gap run-length finding says cycles
  are ~3× longer than first assumed).

**Words-after = a structured OPEN QUESTION, not a prediction** (confident in the paradigm, unsure of
the architecture's behaviour):
- *Soft prior (not a gate):* words-after recovers at the **occupancy** level (the cycle cleans up and
  covers over) but **scars at the envelope level** — this rig has **no envelope re-pool** (Tier 2,
  §6b deferred), so the first allocation literally lasts; the cycle redirects occupancy *within the
  branch the first impression opened* but cannot reclaim/reallocate the branch.
- *What the rig measures:* the **asymptotic words-before vs words-after gap** (after both have cycled
  fully) = the size of the **envelope-level scar** = a lower bound on what envelope re-pool (Tier 2)
  would recover. **A deferral paying rent:** the first rig *sizes the deferred mechanism's value*.
  Small gap → Tier 2 is minor, deferral was cheap. Large gap → Tier 2 is doing real work, its
  re-entry trigger should fire sooner.
- *Genuinely open:* how large the scar is. Full recovery → "first impressions last" was wrong and the
  occupancy cycle is stronger than expected (a finding). Heavy scar → Tier 2 earns priority.

**Disambiguation control — pretrained-PAM** (run only if the online result is ambiguous on
learning-vs-gradient). If occupancy lags, is it because PAM hasn't *learned* the association, or
because the *gradient* is weak? Enter PAM with the word-association already confident → any remaining
lag is the gradient's doing. The analog of the oracle's forced-open/read-only trick (hold one
variable to attribute the other). **The one admissible train/run split** — as an *isolation control*,
not the deployed mechanism (exp02 logic: testing a property ≠ adopting it).

**Build path (three stages; pin/sweep/release):**
1. Fixed wide ratio, depth-independent, slow constant re-pool. Get the equilibrium-with-PAM-unpool
   **stable at all**. Pre-register: intermittently-predictive distinction finds a stable depth vs
   oscillates (§7 dynamics question).
2. Sweep the rate ratio inward; characterise where it oscillates — the response surface (as the
   unpool-clock rate was handled).
3. Release the depth-grading, using the surface as the reference for the force law.

Two cortices, **no store needed** — a targeted addition on the current Stage-0 rig. Stays
Stage-0-shaped in components; new in *stimulus*, *timing manipulation*, *two-timescale readout*, and
the *constant-intrinsic-re-pool + evocation-driven-occupancy* mechanism.

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

**Status of the next step:** the A-vs-B fork is **closed** (Reading A, §7) and the §8 rig is
**specified** — see the companion build doc `STAGE1_ATTENTION_SCULPTING_RIG_SPEC.md` (exp03-style,
CC-ready). The rate-gap stability reference is pinned for the first rig (fixed + slow constant
re-pool) and swept as stage 2. Remaining genuinely-open items (envelope-scar magnitude; intermittent-
load stability; depth-grading) are what the rig *measures* or are deferred-with-triggers — none
blocks the build. **[SUPERSEDED by §10, 2026-06-29: the build proceeded and surfaced a GATING
PRECONDITION that blocks the rig — a dead evocation channel. Read §10 before acting on §8.]**

---

## 10. The gating precondition — a live evocation channel (design-table brief, 2026-06-29)

**Status:** `[BLOCKER — design-table decision]`. The Stage-1 rig of §8 was built faithfully (the
constant Δ2 re-pool of §5/G3; the 4→8 conflict stimulus of §2; the category oracle; Step-0 (a)/(b)/(c);
the conflict-strength ladder — `experiments/05_attention_sculpting/`, with only behavior-preserving
hooks added to the `[SETTLED]` exp04 + `src/loom/constant_repool_delta2`). Building it surfaced a
prerequisite the whole program rests on and does not yet have: **the operator's evocation channel is
content-dead in the deployed regime.** Everything below is **verified** (4-lens adversarial panel,
unanimous; content-agnostic neutral (d)-gate); the redesign that fixes it is **the design table's to
scope**, not a CC patch.

### 10.1 What is dead, and why it blocks §8
The mechanism under test (Reading A, §7) routes occupancy through PAM's evocation: a distinction is
maintained iff its sides **evoke different bundles**. Empirically, in the deployed Stage-0/Stage-1 rig
the `PrototypeResonanceOperator`'s PAM substrate **collapses to a single point** (prototype within-group
spread 6.8e-3 init → ~1e-9…1e-11 by a few k steps, all 3 seeds, present from ~t=300), so `z = pa @ Wp`
is **content-invariant** (random-input output std ~1e-9; on-manifold member/word/drift evocation differs
by ~1e-7). The gap-3 gradient still reaches the masked vision **target** (so "gap-3 alive" / grad>0
passes), but it is a **member-invariant constant pull**, carrying no word/member information — vision's
above-chance B_track (0.34–0.84) comes from the spread/JEPA terms, **not** PAM evocation. **A
reversed-lift run on this channel would be a WRONG-REASON null** ("the word doesn't teach" is
indistinguishable from "the channel was too dead to carry the signal"). So §8 cannot be run until the
channel is live. (The operator's *form* is fine: a fresh operator trained on a clean neutral 2-member
association routes at (d)≈1.27 even at init 1e-3 — the collapse is purely the **deployed regime**.)

### 10.2 The candidate levers (causal structure UNDETERMINED — do not read as a solved diagnosis)
> **[SUPERSEDED 2026-06-29 by §10.7 — exp06 determined the lever: JOINT {cue-diffuseness, PAM
> pool-penalty}; member-count tolerated-deployed. The "undetermined" framing below is the
> pre-decomposition state, kept for the record.]**

The contained fix authorised by the design table (operator-side, scale-robust, minimal-DOF,
no tuned dial, validated content-agnostically) was **pursued to exhaustion**; every candidate was
**insufficient alone**, and only a *stack* moved the needle — which establishes the factors are
**jointly movable, NOT their causal structure**:

| candidate change | revival (neutral (d)-gate) | note |
|---|---|---|
| prototype-init rescale 0.3 / 0.5 / 1.0 | none (≈0) | init=1.0's on-stimulus 0.23 was a `clamp_min` magnitude **artifact**, rejected by (d) |
| window-center the cells (parameter-free) | none | within-dwell **content is itself window-constant** → centering removes content with the carrier |
| remove carrier-DC along `u` | none | prototypes don't lift under the diffuse multi-member task |
| **stimulus-side: bound carrier to within-window-relative** | none | so it is **not** just the absolute carrier scale |
| cosine (scale-invariant) resonance + pam_lam=0 + init=1.0 + 2× training | ~0.197 (~15% of clean capacity) | only the *stack* revives, and weakly |

Three named candidate levers — **carrier scale × PAM pool penalty × the diffuse multi-member completion
signal** — were each shown insufficient and jointly movable. **The load-bearing lever is undetermined.**
The most under-decomposed gap is **clean-2-member (d≈1.27) vs diffuse-multi-member deployed (dead)**:
the real lever may be **how PAM's completion task is posed** (task structure) rather than the operator
or the carrier at all. The redesign must decompose this before committing to a mechanism.

### 10.3 The exp03 residue — verified, come-due, necessary-not-sufficient
exp03 pre-registered (`experiments/03_order_as_content/RESULTS.md:120-126`; echoed PROJECT_STATE §6) that
the operator is a **within-window comparator, not scale-invariant — "retains some absolute-scale
sensitivity (large out-of-distribution per-sequence offsets degrade it)."** Stage-0 then made the order
carrier **one continuous unbounded walk** ("never reset per window", loop.py), feeding the comparator
OOD-large absolute offsets (deployed `ctx` on real cells ≈ **333**: `in_proj(cells)`≈1348,
`pos_extract(cells)`≈252; prototypes ≈ **0.03** → ~4-order mismatch → uniform soft-assignment). So the
residue has **come due**, and it correctly points at the harness's uncontrolled carrier scale — **but
bounding the carrier alone does not revive the channel** (row 4 above). The residue is therefore
**real-but-partial / necessary-not-sufficient**: a genuine contributing cause, not the whole cause.

### 10.4 What this does to the empty-gap reading (a sharpening, not a retraction)
The empty-gap `lift ≈ 0` headline **stands** — it is calibration-independent of *why* evocation fails.
But because the evocation channel was **content-dead throughout Phase-1 and every contained fix failed**,
the channel was **never close to live in any Stage-0 configuration.** Consequently:
- The entire Stage-0 program provides **ZERO bearing on the (i)-impoverished vs (ii)-inert fork, in
  *either* direction.** (i)/(ii) asks what happens *when the channel works*; the channel never worked, so
  the question was never posed. (i)/(ii) becomes answerable **only on a redesigned, channel-live rig** —
  it is not "(ii) gains weight," it is "unasked." *(This supersedes the §9 "discriminating test" bullet
  and the earlier "strengthens (i)" note.)*
- The empty-gap's scope **collapses to its channel-independent part**: *"vision does not need the word
  for a visually-resolvable distinction"* (Step-0 (a) reconfirms this: no-word vision occupies the
  salient distractor at 0.95, neglects the subtle category at ≈chance). That much is solid and useful.
- **Plainly: the central paradigm bet — evocation-as-teacher — is wholly untested**, because evocation
  has never carried information end-to-end in a deployed loop.

### 10.5 The blocker, framed as a design problem (not a bug)
> **[RESOLVED 2026-06-29 — see §10.7. exp06 was designed from this brief, decomposed the levers, and
> named the direction: re-pose PAM's completion task over the JOINT {cue-diffuseness, pool-penalty}
> lever. The "lever unknown" caution below is discharged.]**

**A live evocation channel in the deployed regime is the prerequisite for the entire attention-sculpting
program** (and, in retrospect, for any evocation-as-teacher claim). Producing one is an **open
operator/PAM-substrate (and possibly completion-task) redesign decision** — the design table's to scope,
informed by §10.2's undecomposed levers. exp06 (a channel-revival experiment) should be designed *from*
this brief once a direction is chosen, **not instead of it** — the load-bearing lever is unknown, so a
premature exp06 would test the wrong thing. The neutral (d)-gate (associated-different vs
associated-same on random content + content-ablation) is the **pre-registered liveness pass** any
redesign must clear before Stage-1 is re-attempted; order recovery and the no-clean-slot ceiling are
guards (both were **unchanged** across every operator patch — operator-side levers don't disturb the
order paradigm).

### 10.6 The Stage-1 rig's status, and why this is the apparatus working
The Stage-1 rig is **built, faithful, and not wrong** — Step-0 (a)/(b) pass (salience→distractor;
category representable+ablation-guarded), (c) is blocked on the dead channel. It **waits on the channel
redesign**; it does not need rebuilding.

**Process provenance (why the escalation is trustworthy).** The contained fix was pursued to
exhaustion before escalating; the neutral (d)-gate **rejected the init=1.0 `clamp` artifact** — a
manufacturing-shaped false positive (apparent on-stimulus divergence with a still-dead channel) caught
**before it entered canon**. That is the apparatus doing its job: this is **not the project failing
twice.** It is the instrumentation refusing to let an **untested** bet masquerade as a tested one — two
apparent "the word doesn't teach" nulls (the empty-gap interpretation; the Stage-1 preview), **both
dead-channel artifacts, both caught, both kept out of canon.** The central claim is **exactly as alive
as it ever was** — it has simply **never been tested**, and now we know precisely what must exist before
it can be: an evocation channel that carries information in the deployed loop.

### 10.7 exp06 resolves the lever — JOINT {cue-diffuseness, pool-penalty} → re-pose completion (2026-06-29)
**Status:** `[RESOLVED → exp07 scoped]`. The channel-revival factorial (`EXP06_CHANNEL_REVIVAL_FACTORIAL_SPEC.md`;
`experiments/05_attention_sculpting/`) decomposed §10.2's jointly-movable candidates in **factorial form**,
so interaction was *in the design*, not a post-hoc caveat. Decompose-first over **member-count ×
cue-diffuseness × PAM pool-penalty**, **carrier bounded as the necessary-not-sufficient baseline in every
cell** (§10.3), measured by the now-committed neutral content-agnostic **(d)-gate** (`dgate.py`, promoted
from the exp05 design — the §10.5 pre-registered liveness pass).

**Method discipline.** Step-0 validity **triad resolved first and fully, gate committed standalone**
(`335f36d`, no direction-finding): **V1** clean anchor live (d 1.41, d_same 0 → genuine differential
separation), **V2** dead anchor collapsed (d 0.000, proto 4e-7), **V3** ≥1 single-toggle traverses. Four
gate-validity probes confirmed the 0.000's are **genuine death, not under-training or magnitude artifacts**
(`exp06_gate_validation.py`): collapse cells reach d=0 **and** proto=0 by step 200 and stay flat; raw
un-normalised member separation ≈0 with normal output norm; chance-level noise-decodability. The interior
read was **adversarially verified** (5 independent lenses — arithmetic, §4/§5 rule, soft-cell routing,
neutrality, steelman-the-alternative — unanimous SURVIVES, no overturning alternative).

**Verdict (binary at the healthy bar; super-additivity = interaction evidence only).** From the dead
corner, undoing **any single factor** stays dead (d 0.000); undoing **cue-diffuseness AND pool-penalty
together** revives (d≈1.1) — **super-additive** (1.005 vs Σ-singles 0, margin 0.477). So the **JOINT LEVER
= {cue-diffuseness, PAM pool-penalty}**. **Member-count is tolerated-deployed for LIVENESS — a ~22%
degrader that does NOT flip whether the channel revives (NOT a killer; manyOnly plateaus d≈1.11 vs clean
1.42, above the live bar) — but it is a non-lever ONLY for liveness: exp07 (2026-06-30) measured a channel
exp06 did not and found member-count DOES modulate the reshaped (preserve) tie's capacity cost (seed-paired,
scale-growing: ~0 @card-2 → +0.103 @card-16, paired t=2.84). The liveness non-lever finding stands; "non-lever"
without qualification does not.** The **3-way irreducible-conjunction alternative is rejected** at convergence. The penalty/diffuseness **kill-texture
asymmetry** (penalty = perfect point-collapse proto=0; diffuseness = near-collapse proto>0 + faint seed
residual) is **characterisation only** — kept out of the lever arithmetic (which used d_diff means).

**Why convergence was accepted on the d-mean (load-bearing — written here so it survives compaction).**
The whole joint-vs-conjunction fork hung on the deciding cell [1,0,0], unconverged at the 4000-step gate
budget. It was **re-confirmed to plateau** (`exp06_reconfirm.py`, 16 seeds, to 12000): **d_diff plateaus
flat ~1.09–1.11 from step 6000** (mean 1.106, sem 0.033, **mean−2·SEM 1.040 ≥ threshold 0.967**). The
pre-registered "(d) flat **AND** proto stable" criterion's proto-clause never fires because **prototype
spread keeps growing monotonically — but the clean cell does exactly the same** (clean proto 1.71→2.23
while clean d is rock-flat 1.418). **Proto-flat is a DEATH certificate (dead cells: proto→0 and stay 0),
not a LIFE one**: for a live cell the substrate keeps differentiating, which can only sustain/raise d. So
**(d) is the convergence signal for a live cell**, it has plateaued, any residual creep is *upward*
(safer), and the §4 decision rests on the converged d-mean. Routing held under the longer budget (both
deciding-pair constituents stay hard-zero; the soft diffOnly cell stays out of the deciding arithmetic).

**exp07 direction (scoped from this).** **Re-pose PAM's COMPLETION TASK** as a **joint, symmetric**
redesign over the two lever factors — (a) **how the cue is posed**; (b) **drop/reshape the λ2-tie on PAM's
own prototypes** — pursued together, with **NO penalty-first ordering** (the texture asymmetry stays out).
exp07 must clear the same neutral (d)-gate at the **healthy** bar **in the deployed loop** before Stage-1
(§8) is re-attempted. **The empty-gap (i)/(ii) fork stays unasked** until exp07 revives the *deployed*
loop — exp06 revives the *neutral probe* and names the lever; it does not by itself make the deployed
channel live.

## §10.8 — exp07 (Phase 0): the cue-floor × penalty surface (measured, not built)

**What it is.** The measured opening phase of exp07 (`EXP07_CUE_FLOOR_PENALTY_SURFACE_SPEC.md`;
`experiments/05_attention_sculpting/exp07_{config,core,step0,surface,ceiling_reconfirm,converge_off16,interior_read}.py`).
It does **not** build the redesign — it measures the surface the redesign is scoped from, read through the
committed neutral **(d)-gate** (`dgate.py`), **no new operator, no store**. Cue axis = flat-diffuse →
content-blind re-posings → sharp-reference; penalty axis = `{off (drop), reshaped (preserve), deployed
(collapse)}`; member-count held deployed (16) with a card-2 corner/surface probe. All knobs `[RECONCILE]`d
from the exp06 commit. Step-0 gate (re-posing construction + separability/sanity + corner-gate) was
**surfaced and signed off before any interior read** (the standing gate).

**The `reshaped` (preserve) regime = the settled cortex StepSchedule applied to PAM's tie** (the spec's
preserve argument: *architectural uniformity with the cortices*). Groups open at t1, capacity/λ2 at t2,
strength 10→0. **Two methodological traps were caught and fixed before any verdict** (both would have
manufactured a wrong-reason dead/penalised reshaped column): (1) a naive single-clock `pool_penalty(lam,lam)`
that penalised δ1 too → annihilated the group symmetry-breakers → **irreversible collapse trap** (oracle
test: reshaped-sharp could not revive); fixed to the cortex two-clock that keeps groups alive. (2) a
**fractional clock-onset** that drifted later when the budget was extended for plateau (3600→9000),
lengthening the closed phase and making "more training" look *worse*; fixed to an **absolute** two-clock
onset (900/3600, budget-independent). With the faithful schedule, reshaped revives across **all 10 seeds**
at both cardinalities — the bimodality seen earlier was the onset-drift artifact, not intrinsic.

**The three measured findings (adversarially verified — 4 named-blind-spot lenses; survives directionally,
no high-severity / false-PASS; every confirmed error understates the reshaped cost, so no spurious
"preserve" can be manufactured; two framings that failed *as worded* were corrected in the artifact):**

1. **Cue diffuseness recoverability is STRUCTURALLY FORCED and construction-scoped (not a general result).**
   The re-posing (`comp − α·μ`) is exactly **global mean-centering**, and the deployed diffuse cue puts ~100%
   of masking energy in a single cls-independent common-mode (5.831·base) over a tiny differentiating part
   (0.5·Cd) → at α=1 mean-centering removes the common-mode exactly, so floor≈0 (off cue-floor 0.01–0.05,
   own-sharp) follows from the construction independent of training (near tautology). **Generalization to
   structured (non-common-mode) diffuseness — the spec's stated native substrate, i.e. the build-robust half
   of the two-part cue fix — is UNMEASURED.** Common-mode-dominance is itself a probe simplification of the
   deployed rig (R_coarse per-coarse-class, r_distractor possibly per-member), so the deployed substrate's
   true floor may be >0 (unverified).

2. **Penalty legitimacy → PRESERVE on the uniformity argument, at a measured cost — NOT "validated."** Both
   drop(off) and preserve(reshaped) **revive** the channel (binary liveness does not select). The robust
   deliverable is a **seed-paired, SCALE-GROWING CEILING capacity cost**: off−reshaped = **+0.103 @card-16
   (paired t=2.84; off 1.126 vs reshaped 1.023, both converged at 36000), ~0 @card-2 (t=0.43)**. "Floor-
   equivalent with drop" is **ruler-dependent** (holds under each column's own sharp, Δ0.027; **FAILS** under
   the common off-sharp ruler that this artifact's own `CARD16.floors`+topology use, Δ0.103 > margin), and the
   sharp-gap that would license calling the cost a separable "uniform offset" is **NOT significant** (t=1.48).
   So the cost is booked as a **ceiling/capacity cost**, not laundered out of the floor. Preserve is chosen on
   uniformity grounds, paying this cost; drop avoids it. Onset modulates but does not erase it (best reshaped
   recovers to *within margin* of off, ~0.05 below, not better).

3. **Topology: klass-invariant but trivially so; the discriminating relationship is NOT cardinality-invariant.**
   The "monotonic, invariant 16↔2" klass-match is **deployed-dead-driven** (deployed C=0 pins the floor spread
   to maximum, making `separable` unreachable). The non-trivial off-vs-reshaped relationship is a **dead tie
   @card-2 (t=0.43) but significant @card-16 (t=2.84)** → **member-count does NOT flip liveness (the exp06
   non-lever stands for liveness) but DOES modulate the reshaped tie's capacity cost** (scope-narrowing applied
   in place to §10.7 / PROJECT_STATE §12.E / memory). Two cardinalities cannot anchor invariance of a
   relationship that changes between them.

**exp07 design implication (scoped, not built).** Re-pose PAM's completion with **content-blind cue
re-organization** (the dominant lever for common-mode diffuseness; the structured-diffuseness/build-robust
floor remains untested) **+ the preserve-style open-and-stay-open tie** (legitimate on uniformity grounds,
but carrying a real scale-growing capacity cost — weigh it against the uniformity benefit, especially at high
cardinality; it converges slower than drop). **Still unmeasured / unasked:** the build-robust cue floor under
structured diffuseness; revival of the *deployed* loop (exp07 Phase-0 revives only the neutral probe surface);
the empty-gap (i)/(ii) fork. Numbers in `exp07_interior_read.json` (LEGITIMACY / CUE_RECOVERABILITY_SCOPE /
CONVERGENCE_FLAGS / TOPOLOGY_INVARIANT_16_vs_2); adversarial record in the workflow output.

## §10.9 — Cue-floor / structured-diffuseness (the build-robust half) — SHELVED with trigger

**Deferred, not abandoned.** The structured-diffuseness floor (the build-robust half of the exp07 two-part
cue fix) is a property of the **static `ConflictStimulus` construction** (R_coarse/r_distractor/r_category
block geometry, σ=0.20 noise), **not of the co-development loop**. It surfaced because Phase-0's floor≈0 was
**construction-bound** (common-mode cue + global-mean-centre remover). Measuring the structured floor
optimizes one static single-frame stimulus — **off the loop's critical path *conditional on the revival
result holding in the regime the loop test runs in*** (the bet; the Trigger below names when it's wrong).

**Why deferred.** Signal/clutter separation becomes structurally easier with the two mechanisms the
architecture already intends and we have **deliberately not built** — **continual time** (earned salience:
background becomes low-surprise through exposure; signal separates because the system *learned* the
environment) and **multiple cortices** (cross-modal association recovers a faint signal through the
co-occurrence PAM exists to build). Forcing a single static frame to separate signal from structured clutter
— with PCA/whitening/block-centre disqualified as **variance-matching-circular**, leaving only global
mean-centring — asks one frame to do in isolation the job the loop's **time-and-association machinery** is
designed for.

**Epistemic status.** "Easier later" is a **prior, not a measured fact** — same status as the temporal floor
we declined to assume. The deferral is a **bet, recorded as one.**

**Trigger to resume.** If the loop test stalls because **evocation cannot carry enough signal to teach** —
i.e. the channel-carries-information result does not hold in the regime the loop test actually runs in — the
within-frame structured floor becomes load-bearing and **Phase-1 resumes with a measured reason.**

**Banked pickup artifact — CC's read-only rig analysis** (resume from this, do not re-derive):
- **Structured decomposition** of the deployed `centre` (read-only, exact): **full-16 = 68% structured /
  31.8% global-common-mode; within-group = 13.5% structured** (coarse becomes the within-group common-mode,
  distractor is the residual). Of the globally-centred residual: coarse 80% / **distractor 19%** / category
  **signal 0.5%**. PCA spectrum `[10,10,10,8.49,1.41,0,0,0]` — **category signal @ s=1.41 vs distractor @
  s=8.49 (6× gap), sitting near the σ=0.20 noise floor.**
- **Circularity ladder:** **global-mean-centre = the ONLY non-circular floor instrument** (removes just the
  single global-mean direction); **PCA / whitening / block-centre = variance-matching-circular** (their basis
  *is* the constructed clutter blocks → forced floor) — usable only as **upper-bound references, never the
  floor**. **The ablation guard does NOT catch variance-matching circularity** (it catches signal-injection
  only). Shared-parameter loci that create the trap: the block layout (`n_A/n_distractor/n_category` + the
  divmod map), the rotation `Q`, the population covariance/variance ordering, the magnitudes.
- **Design (scoped, not written): calibrated-synthetic + deployed-direct-validation.** The (d)-gate is
  rotation-agnostic, so a synthetic construction matching the extractable block energies/counts/assignment
  reproduces the deployed endpoint exactly *and* preserves the Phase-0 floor≈0 anchor at sweep=0;
  deployed-direct (`ConflictStimulus` is standalone-extractable) is the calibration target + validation check.
  Floor measured with global-mean-centre only.
- **Phase-1 spec scoped, NOT written. Resume from the analysis.** No code; `ac7ea57` stands as the last build.

## §10.10 — LIVE FRONTIER: evocation-as-teacher remains UNTESTED

exp06/07 established the **channel revives** — it clears the neutral (d)-gate **above the live bar** (revival
d≈1.0–1.1 vs the clean-2 *healthy* ≈1.41) once **cue and penalty are jointly addressed** (cue re-organization
dominant for common-mode diffuseness **(structured/build-robust half shelved, §10.9)**; preserve-style
open-and-stay-open tie legitimate on uniformity grounds at a measured, scale-growing capacity cost). **The channel carries information; it has NOT been shown to
teach** — to **sculpt cortex representation via evocation-divergence.**

**Next phase: scope the minimal rig that tests whether evocation sculpts cortex representation.** The scoping fork (continual time + second cortex from the start, vs
single-cortex minimal-first) is **RESOLVED → §10.11.** [Bar note: exp06/07 cleared the
*live* bar (0.867), not the full *healthy* value (~1.41); "revives" = above-live-bar, not
healthy-restored.]

## §10.11 — Loop-test scoping fork RESOLVED → the anchored-reference minimal rig

**Status.** Design decision, ratified 2026-07-02. Scopes *how the bet is tested*; the bet
itself — evocation-as-teacher — remains **[PROPOSED] and untested** (§10.10).

**The resolution.** The minimal rig that can pose the question is **one plastic vision
cortex developing against a FROZEN word anchor, under continual time, both present from
t=0.** Rejected: (a) **single-cortex minimal-first** — cannot pose the question at all
(grounds below); (b) **the symmetric co-developing pair** — deferred to release (below).
Minimal-vs-rich was a false economy: below this configuration there is nothing to measure.

**Load-bearing grounds (three):**
1. **§7's discriminating signature requires the word cortex to exist.** The signature is
   occupancy *lagging* PAM's word-association acquisition. Single-stream there is no
   association to acquire and no lag to read — minimal-first cannot exhibit the thing the
   rig is built to detect.
2. **#12 bootstrap-convergence — the anchor IS the stable reference, taken at its frozen
   limit.** No plastic component without a slower-changing reference; the anchored word
   supplies the stable co-occurring stream against which association can form from t=0.
   Single-stream has no reference → the loop doesn't start.
3. **Echo-chamber (structural, premise-free).** With one cortex, PAM's associative content
   is wholly vision-derived: evocation mirrors the vision encoder back at itself, so the
   "teaching signal" is a mirror, not a teacher — **regardless of what vision's own
   objective wants.** This is what makes the second cortex *constitutive* of the test, not
   an enrichment.

**Demoted to supporting (do not cite as load-bearing):** the exogeneity form — "vision's
own predictive objective draws on the same temporal structure as PAM's evocation, so
single-stream lift is confounded" — holds only under the untested premise that vision's own
loss would already split the taught distinction. Echo-chamber supersedes it without the
premise.

**FROZEN means frozen — no relaxation schedule exists in this rig.** The word *encoding* is
pinned constant for the whole run. Build-full / pin-to-constant / release (HANDOFF): frozen
is #12's stiff limit — a special case of the real mechanism, not a stand-in — so **no
debt**. One component supplies both required qualities: **stabilisation** (#12's reference)
and the **associative structure** the whole loop builds off (the exogenous distinction
source). Binding scope check: **fixed encoding ≠ fixed association** — PAM must still
*acquire* vision↔word, so the §7 lag signature is untouched.

**Continual time is constitutive, not enrichment.** Sculpting is a decay-vs-hold
equilibrium (evocation-divergence holding productive distinctions open against constant
intrinsic re-pool; inert ones fade) and the §7 lag is itself temporal. Both are invisible
at a single frame — the same reason Stage-0's static frame could only ever test acquisition
(§1).

**Deferred → release: the mutual-sculpting pair.** Two co-developing cortices (word plastic
too) is the richer loop and **will not converge without a designed relaxation schedule**
(#12: stiff early, loosening as the configuration settles). It enters only after the
anchored-reference rig gives a verdict on the basic mechanism. Re-entry is a design step
(the schedule), not a knob.

**Minimality lives inside this regime:** anchor frozen; intrinsic re-pool constant + slow +
depth-independent (depth-grading deferred, §6); **metric = occupancy-lag LIFT, never
gradient-share** (the settled §1 lesson — share is non-discriminating).

**Next.** *(Forward pointer amended in place, 2026-07-03 — the fork below is resolved and
its successor arc has run.)* The revise-vs-fresh question was **RESOLVED → REVISED in
place** (STAGE1 spec, `eabe08b`) and executed through the §L gate sequence: calibration →
matched bar (three pre-read instrument fixes) → windowed Step-0 PASS → entry run
NON_CONVERGENCE → the **§10.12 collapse finding** → EXP08 arms → **§10.12.2: dead-dictionary
DEMONSTRATED, DESIGN GATE OPEN** → **§10.12.3: kick probe ESCAPABLE stands; fork re-ruled
PREVENTION-PRIMARY; fate shared end-to-end, word = pure accelerant + pin-deepener;
correlate = position (early ≫ late).** Current state: **THE DESIGN TABLE opens from canon
— first deliverable = the force-ledger; constraint = input-sensitivity self-sustaining
under the deployed flow.** Gate steps 5–6 blocked.

## §10.12 — Long-horizon vision-content collapse in the deployed loop (entry run, 2026-07-02)

The §L entry gate's first full-horizon deployed run (seed 0, cap 112500 waves, run commit
`ad23fc6`) returned **NON_CONVERGENCE** — and beneath the non-fire, an adversarially
verified finding. Status-split held strictly; nothing below upgrades a reading into a
claim. Artifacts: `stage1_entry_gate.json` (+ dynamics panels), verification record in the
progress_log Gate-4 entry.

**DEMONSTRATED.** (1) **Total vision-content collapse in the word-present arm at long
horizon:** all 16 member emissions collapse to ONE point (centred-content denominator
1.108 → 2.5e-07, seven orders; pinned for the final ~20k waves; occupancy at chance on
BOTH axes from ~96000; healthy through ~72000; one failed revival transient at 93000).
Real, not instrument — every artifact hypothesis ruled out in source. It is the terminal
failure of a standing collapse-and-regrow oscillation (denominator period ≈4800; 394/1125
windows assessable), not a sudden event. Caveat: the ratio column and the occupancy
covariate both read through `vision.emit` — one collapse read twice, not two confirmations.
(2) **The word→category evocation channel stays alive and DECOUPLED from the dead
content:** numerator declines through discrete plateaus (46→36→10→13→4.97;
prototype-resonance snapping); proto_spread at its run maximum; the ratio correctly
NOT_ASSESSABLE at the tail (the denominator floor doing its job). 30k corroboration:
word-arm channel dead in 2/3 seeds while the no-word arm is healthy in 3/3 — the collapse
is word-present-arm-specific and modal-leaning at config; **n=1 at full horizon** — every
routing decision is under-powered against the ≥20-style seed floor.

**PLAUSIBLE (mechanism — suspected, NOT demonstrated).** The composed hypothesis: **engine
= the gap-3 no-detach TARGET-side pull via the vision-SELF reconstruction path** (a
contraction on emissions — emission → PAM resonance-averaging → target pulled toward it,
no stop-grad), **permitted by** three verifiably weakened counter-forces: the anchor names
only 2 category targets for 16 members (a failed 2-point anchor — REFUTED as the engine:
a 2-target pull floors at two points, cannot name the A/distractor axes that died, and the
axis that died is the word-LESS distractor); spread 10× under-weighted (α=0.1 vs gain
1.0); all L2 ties → 0 after t=1200. The no-detach is deliberate design — the gap-3
teaching channel itself — so any fix is a **design revision at its own gate**, not a bug
patch. Exonerated: JEPA (stop-grad, within-member), constant re-pool (rate 0 — no-op).
Confirmation requires the pre-registered diagnostic arms (`EXP08_COLLAPSE_ARMS_PREREG.md`).

**The §11 stress-test reading (spec §11: "the word does not improve acuity — it teaches
what is worth distinguishing").** This run stress-tests the line's converse: in a loop
with a live no-detach evocation channel and weak restoring forces, the substrate does not
merely fail to learn distinctions — it can UN-distinguish. The line survives only with its
implicit precondition made explicit: teaching-what-to-distinguish presupposes forces that
hold everything else open. The word taught nothing here; the loop forgot everything.

**The potency reading — HELD AS A READING, not a claim.** If the self-path contraction is
confirmed, this run is the first direct observation of evocation *sculpting* the cortex —
in the destructive direction (a homogenizer, not a teacher). That is the §10.11
echo-chamber ground made empirical: a single cortex's evocation mirrors the encoder back
at itself, and the mirror, unopposed, erases. Potency-of-the-channel would be evidence FOR
the paradigm's premise (evocation moves substrate) while being evidence AGAINST deploying
it unanchored. Do not cite this section as either until the arms return.

**The #12 / EMA-as-relaxation-reference note — FLAGGED for the design gate; decides
nothing now.** #12 (§10.11) holds that the anchor is the stable reference at its frozen
limit. This run suggests the reference-stability requirement is QUANTITATIVE, not just
qualitative: 2 frozen points did not hold 16 members open. When the mutual-sculpting
release eventually relaxes the anchor (§10.11 deferred), the relaxation form may need to
be a slow-reference (EMA-style) rather than a scheduled un-freezing — a reference that
moves slower than the thing it anchors, everywhere in the space it anchors. A note for
that design gate, nothing more.

### §10.12.1 — The one review (2026-07-03): verified arm verdicts; NO design revision yet

**Ruling (Jason).** All five arm verdicts ratified AS VERIFIED — including the refuted
sharpest line (Jason's own), kept on the books with all beats. **No design revision yet:**
its target hangs on three claims still at deduced/suspected (driver identity,
dead-dictionary, terminal lock); the converters are each cheaper than the design they'd
steer. Design gate parked; the #12/EMA note parked with it; gate steps 5–6 blocked.

**The verified table (status-split held).**
- **DETACH — CONFIRMED, re-anchored: the gap-3 no-detach TARGET-side pull is NECESSARY
  for the collapse.** Evidence: real word-channel structure in 3/3 seeds (num
  0.26/0.59/1.35), ratio-positive 28–71%, occupancy, the fixed-α detach-vs-baseline
  contrast; gW=0.00 validates the amputation.
- **SPREAD — NOT CONFIRMED AS STATED** (circular readout, the manufacturing class,
  caught: spread_loss forces the very variance the denominator measures; seed-0
  counterexample: den 2.72 with zero word-axis structure). Partial 2/3 on independent
  evidence.
- **MARATHON — the sharpest-line prediction REFUTED; the pre-registered revision branch
  fired, narrow form: word-presence ACCELERATES a shared contraction (~4.8× clock — den
  period 23100 no-word vs 4800 word, same seed). DEMONSTRATED: acceleration. SUSPECTED
  only: a distinct terminality mechanism (the marathon was caught MID-DECAY — window-max
  1.16→0.05, troughs to 1.4× floor, tail num-freeze — PRE-terminal, not non-terminal;
  n=1 vs n=1).** The refuted-prediction record, all beats: prediction (no slower) →
  result (nowhere near terminal at matched cap; ~5× slower clock) → revision (engine
  stays self-path-credible; word = accelerant). *The accelerant is the two-word
  instinct's first measured support — the sparse word adds pull — though density itself
  stays open pending acquisition-aligned reads.*
- **TIES — UNINFORMATIVE** (ε=0.1 overshot: Δ2 never crossed the calibrated 0.05
  capacity-open threshold). Parked; re-dose on-call (ε below threshold), not in the
  leverage path.
- **LADDER — statistically flat, relabeled UNINFORMATIVE on anchor density at 30k**
  (dense anchors under-acquired: num ~4× weaker at v8/16 — curriculum lag). Follow-up
  pre-named, not launched: **acquisition-aligned per-rung reads** (the time-axis lesson's
  third appearance). Generalized caution: **any word-dependent 30k read is
  acquisition-suspect until aligned** (vocab2's own word-axis structure absent in 2/3
  seeds at 30k).

**Mechanism as it survives.** Target-side pull NECESSARY (demonstrated). To-a-point
driver credibly the SELF path (the word-path target is 2-valued/floor-protective and
magnitude-dissociated: the marathon keeps gW/gS≈3.24 without terminal collapse — gradient
magnitude is not contraction causality when the dominant path pulls toward a floor). The
engine yields collapse-regrow with or without the word; word sets the timescale.
**Terminal lock mechanism UNRESOLVED** (zero gradient data at/near terminality;
"2-points-lockable" struck as under-evidenced). **Localization: capacity-open
ASSIGNMENT-collapse (dead-dictionary readout)** — Δ2 depth and within-group spread stay
open in collapsing arms (both substrate metrics non-diagnostic); DEDUCED from
emit = assign@W with fixed inputs and spread weights; column pending.

**Instrument ruling — den demoted, principle generalized.** The centred-content
denominator is a VARIANCE statistic: it cannot certify differentiation at the high end
(the spread term manufactures exactly what it measures; set-point 2.49–3.34 across all
detach+spread runs). **Demoted rig-wide to a one-sided collapse-floor tripwire.** The
principle joins the circularity ladder (§10.9's instrument lesson) as its second
independent instance: **variance statistics cannot certify differentiation — floor
tripwires only.**

**Authorized converters (composed; then ONE follow-up review; then the design gate):**
(1) columns first — assignment-entropy/argmax-concentration + input-sensitivity (the
dead-dictionary measurement) and the gradient split carried to terminality — wired before
any run (no stored weight checkpoints exist from prior runs; forward-wire only);
(2) split by question: no-word marathon EXTENDED to cap 500000 [RECONCILE: ~20 no-word
periods (23100) + headroom] with the pre-registered TERMINAL / ASYMPTOTIC / neither
reads; +1 word-arm full-horizon seed (terminality arrives ~96k, inside the existing cap)
carrying the gradient columns — doubles the n=1 terminal observation;
(3) den demotion as above.

### §10.12.2 — Follow-up verdicts (2026-07-03): dead-dictionary DEMONSTRATED; the DESIGN GATE OPENS

**Run A — no-word marathon to 500000: NEITHER_BY_CAP, earned** (not a criterion artifact:
the run is authentically neither). The no-word regime is named: **METASTABLE INTERMITTENT
COLLAPSE** — deep floor episodes (window troughs e-6…e-8 from ~230k; occupancy ~chance
through ~300–460k) with episodic partial revivals (den regrows to 0.69 at ~470k; occupancy
back to 0.60–0.67 late; final window still flickering).

**Run B — word arm, seed 1: TERMINALITY REPLICATED (n=2),** arriving earlier than seed 0
(argmax collapse ~50k; sub-floor 1.00 from ~80k; den pinned ≤4.5e-5 for the final 30k;
num frozen; occupancy chance; zero regrow).

**Dead-dictionary: DEMONSTRATED** (was deduced). `asg_argmax_k = 1` sustained in BOTH arms
(word ~50k+; no-word ~162k+) while capacity stays open (Δ2 depth 2.54 / 1.14 at end). The
collapse is assignment-side: all 16 probes route to one prototype; the weight dictionary
survives as unused open capacity.

**The pin-depth correlate (measured).** The soft assignment separates the two ends by four
orders of magnitude: word arm pins `asg_dist` ≈ 1e-5 (locked; no regrow ever follows);
no-word floats ≈ 0.08 (regrow-capable, and regrows repeatedly). **Word = accelerant (~5×)
+ pin-deepener.** The self-absorption reading (input-invariant assignment strips gradients
of their input-differential component; the word's 2-target pull then translates the
collapsed point rather than re-spreading it) is COHERENT-DEDUCED, not demonstrated — the
kick probe (prereg below) is its direct test.

**Scope line (SUPERSEDED by measurement, 2026-07-03 — the question it fenced was answered,
not violated; see §10.12.3).** As written it read: engine shared, lock word-conditional, do
not extrapolate no-word terminality. The kick probe's ε=0 control then MEASURED the no-word
terminality it fenced: the 500k state self-pins unkicked within +18k (~518k total). **Fate
is shared end-to-end** (terminality n=1 no-word, n=2 word); **word = pure accelerant** —
two independent estimates converging: **5.4×** (terminal clocks 518k/96k) and **4.8×** (den
periods 23100/4800) — **+ pin-deepener**; the 4-orders pin-depth gap is **position on one
trajectory, not a word-conditional regime** (the no-word state was the same road, earlier).
The t=75000 self-path gradient spike remains a **named observable only** — n=1.

**DESIGN GATE — OPENED (record).** The constraint the data fixes: **any revision must keep
the routing/assignment map INPUT-SENSITIVE under the target-side pull** — the failure
point is neither capacity (open throughout) nor the prototypes (alive throughout) but the
routing function, and the word as-built pushes routing toward absorption. Directions on
the table: **routing-side counter-force / denser anchor / revised target path.** Drift
guards, verbatim: **counter-force = highest risk** (the manufacturing-the-effect class —
building in the property under test); **confidence-first check** (any candidate must fail
the wrong-reason screens before its first run is trusted); **detach stays DIAGNOSTIC**
(it amputates the teaching channel; it is never the fix). The **#12/EMA-as-relaxation-
reference note is PROMOTED to a design-table input** (the reference-stability requirement
is quantitative; a slow-reference form is on the table alongside the three directions).

### §10.12.3 — The kick probe (2026-07-03): ESCAPABLE stands; the fork re-ruled PREVENTION-PRIMARY

**The verdict, with all beats (the falsified-expectation record kept whole):** (1) formal
scoring (final-period mean) → ESCAPABLE both states, ε*=0.01; (2) flagged — the mean-form
did not measure the pre-registered word "sustained" (a single terminal-window flicker
satisfied it); (3) re-score RULED on instrument-validity grounds, pinned literal form (asg
above the control band for EVERY window of the final den period); (4) **re-score:
ESCAPABLE STANDS — both states (word ε*=0.1, no-word ε*=0.01), no third scoring pass.**
Two stated expectations overturned by their own execution, kept on the record: the
expected ABSORBING-in-substance verdict, and the form-robustness ground (ε* is
form-sensitive; the two forms fire on different phenomena). CC's interim "decay-back
universal" trajectory read is also corrected on the record (a 6-of-30-shard downsample
artifact).

**The population structure (all 24 kicked resumes; t=0 null-kick guards passed; ε=0
controls near-zero):** **2 PIN** (exact return to zero) / **8 EMBER** (named third
profile: sustained above-band at 1e-4–3e-3, flat trend — persistent low-grade
input-sensitivity, neither growing nor dying) / **8 FLICKER** (intermittent; two
rising-at-cutoff cases logged as RIGHT-CENSORED — caveat only, no extension) / **6
SUSTAINED at functional scale** (standouts: no-word ε=0.01 k2 — final-period mean 0.232 ≈
4× the pre-kick floating level, max 0.71, positive trend; word ε=0.3 k0 — mean 0.107 ≈
10⁴× the hard pin, decaying). Content-blind kicks CAN rescue — **stochastically (~25%
sustained-functional), non-monotone in ε, seed-dependent.**

**The fork, re-ruled: PREVENTION-PRIMARY, RECOVERY-UNRELIABLE.** Recovery exists but
cannot be load-bearing — a gambler's mechanism, not a design element. The constraint
survives refined: **the flow is mostly-absorbing with stochastic re-amplification
windows**; design still targets making input-sensitivity self-sustaining RELIABLY, and the
kick data proves the flow HAS a re-amplifying regime — **the design question sharpens to
what conditions put the system in it.** The corrected picture: **not a pure drain — a
current with eddies.** Most kicks wash back to the pin; some land in a pocket where
difference re-amplifies and holds. The balance framing survives intact — stronger:
differentiation pressure demonstrably CAN win locally. **Regulation = widening those
pockets by design.**

**Guards (verbatim, now load-bearing):** kick-not-a-candidate stays barred — "noise
sometimes rescues" is exactly the unreviewed counter-force door, and it matters MORE after
this data, not less. Occupancy-column gap in the kick reads logged as caveat (asg/den/num
answered the basin question; no re-run).

**Authorized converter (read-only, no new runs): the CORRELATE HUNT.** The 24 resumes are
a dataset. Pre-registered pass over existing artifacts: what separates SUSTAINED(6) from
PIN/EMBER(10)? Candidates: post-kick t=0 magnitude, state, ε, early-window trend. A found
correlate converts "stochastic" into "conditioned" and feeds the design table directly.
**Then: the design table opens from canon, first deliverable = the force-ledger.**

## §10.13 — THE DESIGN TABLE (2026-07-03): force-ledger v1; Fork 1 RESOLVED → the self-path #12 reference

Opened from canon (§10.12–§10.12.3 + PROJECT_STATE §12.E 07-03 + the EXP08 prereg tail
incl. the position-vs-live-pull confound). First deliverable, ratified as tabled with
every number traced to committed artifacts before this write:

**FORCE-LEDGER v1** — force | direction | surface | measured | status.

*Contraction:*
1. **Self-path target-side pull** (the gap-3 common component, no-detach) | contracts |
   routing/assignment | NECESSARY for collapse (detach arm, fixed-α contrast); active
   from early (the standing collapse-regrow oscillation, den period ≈4800) through
   terminal lock late (word ~96k s0 / sub-floor ~80k s1; no-word ~518k unkicked) |
   demonstrated-necessary; driver identity credibly-the-self-path (magnitude
   dissociation: the marathon holds word/self ≈3.24 with no terminal collapse at
   matched cap).
2. **Word-anchor pull** | contracts | routing → 2 category targets | pure accelerant —
   5.4× (terminal clocks 518k/96k) and 4.8× (den periods 23100/4800) converging — +
   pin-deepener (asg_dist ~1e-5 locked vs ~0.08 floating) | demonstrated; the
   live-pull-during-recovery reading OPEN (the position-vs-live-pull confound;
   discriminator pre-named, unrun). *(A tabled fourth clause — "persists post-death at
   ~4× self magnitude" — was REFUTED in pre-commit verification: the word/self
   grad-split ratio reads the identical ≈4.0 in the word-FREE marathon (probe mask
   geometry: the word-path probe masks all W=3 vision cells, the self-path probe one).
   Post-death word-pull persistence currently has NO valid observable — logged, not
   chased [checkpoint-ratified strike]. Scope: the pre-named word-ablated-resume
   discriminator is unaffected — it reads outcomes, not probe ratios.)*
3. **Constant Δ2 re-pool** | contracts (designed occupancy decay) | occupancy |
   **deployed rate 0 → no-op in every collapse run**; exonerated as engine | settled.
   (Correction from the tabled draft, which read "slow, designed, graceful": the force
   is designed-graceful but was OFF in every run on the books.)

*Differentiation:*
4. **Gap-3 differential component** (intra-group disagreement) | separates | the SAME
   path as row 1 | path potency demonstrated only in the destructive direction
   (AGGREGATE target-side — the detach arm severs word-cued and self-cued maskings
   alike; the self-path/differential attribution is credible-deduced, mirroring row 1's
   status split, never demonstrated); fuel = existing routing differences →
   SELF-CONSUMING at the pin (input-invariant assignment strips gradients of their
   input-differential component — coherent-deduced; the kick data locates the
   CONSEQUENCE: a mostly-absorbing flow with stochastic, position-conditioned
   re-amplification pockets — not the mechanism) | **THE DESIGN TARGET.**
5. **Spread term** | separates | emissions | 10× under-weighted (α=0.1 vs gain 1.0);
   partial preventer 2/3 on independent evidence; readout circularity caught
   (manufactures the variance den measures; seed-0 counterexample: den 2.72 with zero
   word-axis structure) | measured-weak; **surface mismatch: emission variance ≠ routing
   sensitivity** (the failure is assignment-side; spread acts on emissions).
6. **λ2 tie schedule** | separates (early) | capacity envelope | holds early, → 0 after
   t2=1200 by design; ties arm UNINFORMATIVE (ε=0.1 overshot the 0.05 capacity-open
   threshold) | designed-zero late; re-dose parked on-call (ε<0.05).
7. **Anchor as #12 reference** (frozen word) | separates (reference) | word channel |
   channel alive and DECOUPLED from the dead content at full horizon (s0: num declines
   through plateaus 46→…→4.97); 2 frozen points did not hold 16 members open — the
   2-target pull floors at one point (translates the collapsed point rather than
   re-spreading it; coherent-deduced); density lever UNMEASURED at matched acquisition
   (ladder flat at 30k = uninformative; acquisition-aligned reads parked) |
   partially-failed-as-deployed / unmeasured-as-lever.

**Row property (all rows): timing multiplies** — pocket width early ≫ late (the
correlate hunt); the prevention budget concentrates early.

**Named ledger observation (LOG, NO CLAIM — checkpoint, 2026-07-03):** word s1 shows
num = 0.0 in every window through t=45000 while routing collapse is already under way —
**the word's pull is task-structural, present before measurable association.**

**The structural fact the ledger surfaces: rows 1 and 4 are ONE PATH.** The engine and
the teaching force are the same gradient, split into a common component (contracts) and
a differential component (separates). Collapse = the common component winning; the
differential component burns the very differences it feeds on — self-consuming at the
pin (coherent-deduced, §10.12.2; what is LOCATED-demonstrated is the assignment-side
dead-dictionary and, from the kick data, the mostly-absorbing flow — the consequence,
not the stripping mechanism). And the self-path is the one plastic loop THROUGH THE
ASSOCIATIVE OPERATOR (the PAM target path) with no #12 reference — vision predicting
vision, both sides the same weights (JEPA's within-member stop-grad loop sits outside
#12's scope: exonerated, not reference-bearing). The word path had its reference; its
channel survived to the end.

**Fork 1 — what supplies self-sustenance: RESOLVED → (a) the self-path #12 reference**
(ruling, 2026-07-03). Grounds: (1) repairs the diagnosed violation rather than
counter-weighting it — the self-path is the one plastic loop through the associative
operator with no slower reference; (2) no new force, no new objective — the reference
re-times an existing path; (3) **RE-WORDED at checkpoint (Jason, 2026-07-03,
superseding the tabled "gap-3 intact" — his carry, on the record): teaching path
RE-ROUTED, not intact.** The canonical target-side gap-3 pressure is severed at every β
(detached target); the mismatch reaches online vision via the cue/completion side only;
word path untouched. The design is a recorded BET — lagged-content targets re-supply
the teaching function — certified or refuted by the §6 screen + detach-null comparator,
never assumed. *The bet has teeth, pre-registered now: (a) ≈ detach-null on outcomes ⇒
the slow copy is stop-grad in costume — the function test may PASS while the paradigm
bet FAILS; that routes back to the table as a PARTIAL RESULT, never laundered into
PASS*; (4)
SIGReg-class spread stays the row-5 COMPLEMENT, not the fix — the surface mismatch
(emission variance ≠ routing sensitivity; the seed-0 counterexample) rules it out as
primary. **Parked with triggers:** (b) re-weight existing differentiation forces (spread
→ parity) — trigger: (a) FAILs its function test; any use passes the circularity guard
(variance statistics cannot certify differentiation) and the manufacturing-class screen.
(c) denser anchor — triggers: the acquisition-aligned ladder reads (pre-named,
§10.12.1), and/or the word-ablated-resume discriminator resolving the live-pull reading
(if the pull closes pockets, anchor design becomes a direct pocket-width lever). **Drift
guard verbatim: the most-ML-familiar move on the table — it passes on FUNCTION
(input-sensitivity self-sustaining under the deployed flow, kick-free), never on the EMA
vocabulary.**

**The decomposition observable (ruled with the fork): "the common part" becomes a
number.** A standing read-only column pair: the 16-member evocation set split into
population-mean (common) vs residual (differential) energy, and the same split on the
per-member teaching gradient — the contraction/teaching ratio as a TRAJECTORY (where it
sits, when it tips, what (a) does to it). Spec: EXP09 §7.

**Design pins + the pre-registered function test: `EXP09_SELF_REFERENCE_PREREG.md` —
SPEC AT CHECKPOINT.** Nothing is built or run until the checkpoint list (EXP09 §10) is
ratified. The spec's honesty block (EXP09 §3) records the guard interaction faced
directly: the design shares the detach diagnostic's gradient topology (zero target-side
flow into online vision at every β; β=1 degenerates to the detach arm, β=0 to a
frozen-at-birth target; the family never contains the baseline) — so a bare no-pin PASS
proves nothing by itself, and the detach-null wrong-reason screen (EXP09 §6) is
load-bearing before any PASS is trusted. Steps 5–6 stay BLOCKED.

**Pre-commit adversarial verification (2026-07-03; 32 agents, 4 lenses, per-finding
independent verify): 23 confirmed findings applied before this section's first commit.**
The load-bearing catches, on the record: the row-2 "~4× post-death word pull" clause
REFUTED (probe mask geometry — the word-free marathon shows the identical ratio; the
standing word/self grad-split ratio carries that geometry factor as an instrument
caveat); the EXP09 fast bound DEMOTED to unmeasured (no committed acquisition-plateau
clock exists; §10.12.1's 30k caution applies; in word s1 the word-channel association
post-dates routing collapse — num 0.0 through 45k); the function-test literal forms
re-pinned flicker-tolerant and censoring-aware against measured healthy/terminal spans
(healthy phases flicker argmax_k=1 in ~11% of windows; the no-word regime regrows from
epochs up to 5.9 periods); the teaching discriminator's gradient-share candidate STRUCK
as circular (member-distinct targets mechanically produce member-dependent probe
gradients); ground (3) sharpened as above; the baseline-replay cost corrected 3.5h →
~4 minutes (measured timestamps). Full spec: `EXP09_SELF_REFERENCE_PREREG.md`.

## §10.14 — EXP09 verdicts RULED (2026-07-04): the screen fires STOP-GRAD-IN-COSTUME; Fork 1(a) UNRESOLVED-NOT-REFUTED; the fork record → EXP10 structured variation

The four arms (192k waves each, threads=1, from committed pins) — verdicts independently
rescored, all reproduce, no flips: **slowref_word s0 and s1 = PASS_PENDING_SCREEN**
(32/32 argmax_k>1, ZERO k=1 windows across the entire horizon, zero episodes — at 2×
the horizon where the word baseline terminally pinned); **slowref_noword s0 control =
NO_PIN** (no acceleration); **detachnull s1 = PASS_PENDING_SCREEN with IDENTICAL
margins.** Verification: 35 agents, 4 lenses, 29 confirmed findings — all folded into
the record below (progress_log 07-03 review entry = the full verification record).

**The certified scope, NARROWED at ruling (superseding the prereg's pinned PASS
scope, which the null's identical margins made over-broad): PULL-REMOVAL PREVENTS THE
PIN; the reference's contribution is UNDETECTED.** Both beats kept: the prereg pinned
"the reference sustains input-sensitivity"; the null showed pull-removal alone
suffices; the honest certificate is the narrower one.

**The screen: STOP-GRAD-IN-COSTUME — the pre-registered partial outcome FIRED.** No
recorded column separates slowref from the null in kind (asg / den / pairwise /
grad-ratio / occupancy all ≈); two of the three ruled screen axes returned no events
(vacuous — stated, never counted as equal-behavior evidence); the interim "the null's
word channel dies while slowref holds" was struck in verification as cherry-picked
endpoints of a block-oscillating column. **The paradigm bet — lagged-content targets
re-supply the teaching function — is NOT certified. Fork 1(a) is UNRESOLVED-NOT-
REFUTED:** the reference is not shown useless; the test as built cannot detect its
contribution in this regime. The knob is certified separately (no COPY-COLLAPSE — the
3e-4 floor breached only in the birth transient; lag mechanically valid; τ consistent):
the costume verdict is about the FUNCTION, not a broken reference.

**The regime shift, and its instrument lesson.** All four arms live at a spread
set-point (den ~3.3 word / ~3.5 control+null; pairwise ~4–5) that NEITHER baseline ever
inhabited (~200× the word-baseline healthy-span mean den) — produced by cutting the
target-side pull (the null shares it), not by the reference. The PASS constants,
calibrated on the baseline regime's healthy spans, are cleared trivially by everything
including the null. **The lesson, joining the instrument ladder: constants calibrated
in one regime do not discriminate in another — every future verdict taxonomy calibrates
IN-REGIME, on the tested loop's own healthy spans.**

**The HOW columns — demoted (confound analysis), with one surviving observation.** The
dominance flip (baselines common-dominated ~1.4e4/~294 healthy → all four arms
differential-dominated, medians 0.11–0.17) is real in direction but NOT attributable to
removal of the target-side term from the probe — the null's probe RETAINS the
grad-attached target term and flips identically — and its arithmetic co-moves with
emission distinctness (grad_diff up 5–8 orders alongside ~150–400× pairwise): the
decomposition largely RESTATES member-distinctness in gradient units (the circularity
ladder's shadow; no independent support beyond den/pairwise). **What SURVIVES: the two
decompositions DISSOCIATE — every fresh arm is gradient-diff-dominated yet
EVOCATION-common-dominated (evo_ratio medians 12–799; recurring near-copy episodes;
horizon-end decay in three of four arms — slowref s1 the exception, logged no claim).
The associative evocation channel stays common-dominated everywhere the routing stays
open — the teaching axis, not the routing axis, is where the design bet must be
decided.** Trajectory observation, no claim. Rider (verification caveat 4, carried):
the control's evo/grad columns are OOD (its operator never trained on real tokens) and
stay EXCLUDED from cross-arm decomposition comparisons — the dissociation is asserted
on the three token-trained arms; the control's inside-range values are corroborative
only.

**Baseline corrections (measured under the back-filled columns):** word_terminal_s1's
terminal pin ONSET = 75300 (7.81 periods; k-collapse 42600; two regrown dead episodes
before the pin) — not "~80k"; marathon_ext_s0 to 500k has NO pin under the prereg rule
(three REGROWN episodes, max 5.92 no-word periods — the K_c calibration source; den
0.048 at horizon); the ~518k no-word self-pin remains the kick ε=0 RESUME's measurement
(a +48k continuation), not the 500k artifact's. Named observation (logged, no claim):
the num-continuity difference (slowref s1 continuous-weak post-acquisition vs null
intermittent-strong; seed-inconsistent, amplitude-reversed; dedicated seeds required).

**Scorer guards (EXP10 build items, from the verification):** period substitution
requires an actual collapse cycle (the healthy-segment estimator misfires on
non-collapsing runs — 19× down-substitution on the control, silently rescaling the K_c
bar; vacuous here, live trap later); the PASS window scales with the used period; the
COPY-COLLAPSE floor check goes mechanical (the scorer never consulted ref_pairwise).

**THE FORK RECORD (ruled 2026-07-04): the teaching-axis discriminator runs under
STRUCTURED VARIATION; static cells are the existing baselines.** Grounds: (1) **the
empty-gap lesson** — a potent signal moves nothing where nothing needs moving (the
RULED formulation; the citation, stated to what the record licenses: Stage-0 EMPTY-GAP,
PROJECT_STATE §9/§12.C — lift ≈ 0 at every cell; at easy bands the word was provably
inert because autonomous resolution did everything, which is the
where-nothing-needs-moving half; per §12.E the channel was content-dead throughout, so
Stage-0 never fielded a potent signal — the lesson is the ruling's design bet built on
that record, not a §12.C-certified fact); the static rig gives the teaching channel
nothing that needs teaching at long horizon; (2) **exogenous differential fuel is the
one ledger force that is not self-consuming** (ruled verbatim; clarifier: supplied from
OUTSIDE the v1 rows — the fuel source for row 4's design target, whose endogenous fuel
burns up at the pin; an environment that keeps generating differences cannot be
exhausted by the loop). **Governing line: "Reality is the teacher" — the original
Guiding-List entry (`Guiding List.md`), cited, not duplicated.** Prereg:
`EXP10_STRUCTURED_VARIATION_PREREG.md` — **DRAFT AT CHECKPOINT; nothing builds or runs
until ratified. Steps 5–6 stay BLOCKED.**

## §10.15 — EXP10 structured variation RAN (2026-07-04): the direct test is NEGATIVE; the teaching axis is STOP-GRAD-IN-COSTUME AGAIN; the structured-family routing claim FALLS to generic-noise

The campaign ran to plan (cal → Step-0 re-validation → 12 verdict arms {no-detach,
slowref, detachnull, no-detach-isotropic} × 3 seeds, 160k/192k, threads=1; the
rung-fallback guard did NOT fire — both cal seeds acquired, onsets 15k/21k).
Manifest-time asserts passed every arm (realized pairing ≤ shuffle-null; deployed jiggle
residual ⟂ labels and ⟂ token; centroid-only bound; per-arm σ*=0.04 NC = 1.0). **All
numbers independently reproduced (adversarial verification, 48 agents / 4 lenses / 36
confirmed findings, 0 fabrication); the readings below are the CORRECTED ones — three of
my draft verdicts were flipped in verification and are on the record as such.** Honest
labels throughout (`exp10_verdicts.json` regenerated): the static-calibrated epoch
verdict strings are OUT-OF-REGIME and kept only as the labeled artifact they are; reads
are regime-label + both-period terminal-class (a genuine forced-period read, after a
scorer bug was caught — the substituting path did NOT report at the pinned constant when
a collapse cycle exists) + onsets + trajectories.

**Step-0 re-validated under variation (the environment is valid):** (a) distractor
recovery 0.71/0.62/0.76 ≥ 0.60 floor, 3/3; (c) the word→category evocation channel LIVE
3/3 (share 1.000; cat_div 0.075/1.12/12.3, dist 0). The (b) ceiling never bound (oracle
0.955 at every rung). So the varied rig teaches a representable, resolvable environment.

**THE DIRECT TEST — NEGATIVE (verdict-flip from my draft).** Does exogenous variation
alone hold the ORIGINAL (no-detach) loop open? **No.** All three no-detach-varied seeds
die: routing goes assignment-dead in long tails (k=1-only runs 69.3k/33.6k/45.3k waves;
every seed dead at horizon), with the word→content channel decoupled-alive on the dead
routing — the SAME signature as the static collapse, now with extended flicker
(collapse-regrow interior revivals, 12/12 across arms, deepest joint-dead runs ~18k).
Occupancy death arrives at/before the static word clock. **The word is doing something —
accelerating routing death on the static schedule — the no-word-metastable-arriving-
earlier alternative is refuted** (acquisition entry 9–27k vs the marathon's ~141k). **The
pre-registered closure-necessary-too inference DOES NOT FIRE; pull-necessity stands via
the either-way clause only.** Correction on the record: my "terminal lock mostly beaten"
and "onsets earlier than every static word arm" were both wrong — the loop is not held
open (dead tails), and varied onsets beat only the static NO-DETACH word clock (45.3k,
n=1); they tie the static stop-grad arms (detachnull_s1 = 9.3k without any variation).

**THE ANNEALING DISCRIMINATOR — the structured-family ROUTING claim FALLS (route fires
a fortiori, but NOT the way I first read it).** Isotropic noise at matched total power
(which corrupts identity axes by construction) reproduces the open-routing phenomenology
and is WORSE on every honest routing outcome: deeper joint-dead pockets (41.1k/29.7k vs
≤18k) and one horizon-terminal FULL PIN at the matched period (iso s2, 3.5 periods —
which no structured seed reached). So the routing-openness effect of variation is **NOT
structure-specific → the structured-family routing claim falls.** (Correction: my "NEITHER
×3 = holds routing open equally" was a period-substitution artifact — the a-fortiori
conclusion survives, the equality reasoning does not.) **The one structured residue —
earlier acquisition onset (3/3 seeds, 1.3–2.9×, n=3, not significant) — is CONFOUNDED by
cue-corruption** (isotropic damages the identity axes at matched power, so later iso
onsets may be corruption, not lower demand) and cannot be claimed as a structured-teaching
advantage without an off-cue-axes matched-power control. Named, not claimed.

**THE TEACHING AXIS — STOP-GRAD-IN-COSTUME, AGAIN, under variation.** slowref-varied vs
detachnull-varied: **no outcome-level divergence on any measured axis** (both ROUTING-OPEN,
0 k=1 windows in 640, den never sub-floor, asg ~1.6–1.73); all three leans — live-fraction,
acquisition onset, evo_diff — favor the NULL (equal-or-ahead). The churn-in-costume screen
does NOT fire (acquisition is present in all 12 arms), so the teaching bet is UNDECIDED via
NO-DIVERGENCE, not churn. What DID change from the static regime: the differentiation
(evocation) channel is alive-at-horizon in 5/6 varied ref/null seeds (vs static horizon-end
decay) — but common-domination PERSISTS (evo_ratio > 1 in ≥99.6% of windows; the median
actually moved off common-dominance in only 3/6 full-run). Variation kept the channel
firing longer; it did not make the reference detectably teach.

**WHAT EXP10 SETTLES (and does not).** SETTLES: (1) exogenous structured variation, as
operationalized (K=4 orthogonal recurring axes + frozen-centroid jiggle, ×2.0 demand), does
NOT hold the deployed no-detach loop open — the collapse is not fixed by giving the
environment inexhaustible differences; (2) the routing-openness that variation DOES produce
in the detach-topology arms is not structure-specific (generic noise does it, worse); (3)
the self-path reference remains undetectable against its detach-null even under variation —
Fork 1(a) stays UNRESOLVED-NOT-REFUTED, now on a second independent regime. DOES NOT settle:
whether a stronger/among-cue structured environment, or a longer horizon, or a different
teaching-axis instrument would separate the reference — the evocation-channel-alive-longer
change is a thread, not a result. **"Reality is the teacher" is not refuted as a principle;
the specific operationalization did not deliver a detectable teaching effect here.**

**Instrument + process notes (on the record):** a real scorer bug caught and fixed — the
"both-period disclosure" read applied period substitution instead of forcing the pinned
period, hiding iso-s2's terminal PIN (now a `force_period` path); the stage-two constants
note was self-contradictory (claimed a terminal-signature exclusion that isn't implemented)
— corrected, the regime finding (no clean healthy band in the varied regime) survives an
exclusion-honoring recompute; the read-time shuffle screen is low-power BY DESIGN (the
nuisance-riding read sits at 0.52–0.55 vs chance 0.50) — primary-read leakage is carried by
the manifest asserts, as pinned; Step-0 ran concurrently with cal (letter-deviation from the
linear sequence; gate order preserved at verdict launch — process note, pin for future: a
fallback-firing must trigger Step-0 re-run). Steps 5–6 BLOCKED; no arm was a fix.

**THE DESIGN TABLE, where it stands after EXP10.** Two independent regimes now show the
same wall: the failure is assignment-side routing collapse under the target-side pull, and
neither a slow-reference (EXP09) nor an inexhaustible environment (EXP10) makes the
reference's contribution detectable — because in every case the detach-null does as well or
better. The live thread EXP10 adds: variation keeps the differentiation channel firing to
horizon (5/6) where the static regime decays it — the teaching axis stays common-dominated
but no longer dies. The open directions from §10.13 that EXP10 did not touch remain: the
routing-side counter-force (highest-risk, manufacturing class) and the denser anchor
(stimulus-side; its lever still unmeasured at matched acquisition). The next design move is
Jason's ruling.

## §10.16 — EXP10 verdicts RATIFIED + the next-move ruling (2026-07-04): the denser anchor via the acquisition-aligned ladder, before any counter-force

**Ratified (Jason):** §10.15 as stated — EXP10 NEGATIVE; routing-openness not
structure-specific; costume on a second regime; Fork 1(a) unresolved-not-refuted; the
live thread (differentiation channel alive-at-horizon 5/6, common-domination intact) and
the acquisition-onset residue kept named-not-claimed; the three flipped drafts kept as
beats; the a-fortiori isotropic result and the scorer catch are the apparatus earning its
keep. "Reality is the teacher" scoped to *this operationalization undetected* — the
principle untouched.

**THE RULING — next move = the DENSER ANCHOR, via the parked acquisition-aligned ladder,
BEFORE any counter-force.** Grounds: two regimes now show the same shape — every
intervention so far acts on *targets or inputs*, and the detach-null matches or beats all
of them because nothing yet touches what keeps **routing** differential. The two untouched
directions split cleanly on risk: the routing-side counter-force is the named
manufacturing-class drift (a new mechanism with its own objective — LAST RESORT, only on
measured exhaustion of alternatives); the anchor is stimulus-side, no new machinery, and
its lever is genuinely UNMEASURED — the EXP08 ladder read it at a fixed 30k budget and got
only an ACQUISITION SEED LOTTERY (verification-corrected: acquired-seed counts 1/3, 3/3,
2/3, 2/3 across v2/4/8/16 — the SPARSEST rung v2 is the WORST acquirer, not a monotone
"dense under-acquired" lag; num medians 0.00/0.63/0.19/0.36, means each dominated by one
spiking seed), and EXP10 built the instrument that fixes the alignment (the
acquisition-aligned read). The one ns fragment we have — the occupancy category-step
largest at v4 (direction robust; magnitude aggregation-sensitive, +0.095 by last-minus-
first-block mean-over-seeds) — points the same way, as does the standing fact that the
word channel is the sole #12 reference that survived every collapse. **The question the
ladder now asks cleanly: does naming more of the space keep routing input-sensitive — the
anchor shifting from accelerant (2 tokens) to scaffold (COVERAGE of the axes that die
first).**

**Construction (ratified + verification-hardened):** the nested ladder v2→4→8→16 (fixed
maps b%2 / b / (a%2)·4+b / a·4+b, geometry untouched), STATIC environment for EXP08
comparability, **BOTH axes acquisition-aligned** (verification blocker fix — the PRIMARY
acquisition read AND the routing VERDICT read at each rung's own onset over a matched
post-onset window; a fixed-absolute-horizon verdict would re-introduce the very
curriculum confound the aligned read removes, since denser rungs acquire later),
input-sensitivity **asg_dist** as the verdict quantity (NOT argmax_k count — the crutch
screen), the teaching-fence intact (v≥4 cells are NEVER teaching evidence). **Variable =
COVERAGE, not "density"** (verification: cardinality and axis-coverage are collinear in the
nested ladder — the coarse-first control that separates them is PARKED with a
positive-result trigger). Horizon set from a MEASURED per-rung acquisition-onset pre-flight
(not the conflated word-pin clock). Varied-environment ladder PARKED (trigger: coverage
holds routing open in static). **Prereg at checkpoint before build:
`EXP11_ANCHOR_DENSITY_PREREG.md` (REVISED post-verification — two blockers fixed: verdict
alignment + horizon pre-flight). Steps 5–6 stay BLOCKED; the ladder measures the lever —
adoption of any rung is a separate ruling, no arm is a fix.**

## §10.17 — EXP11 anchor-coverage ladder RAN → INCONCLUSIVE (2026-07-04; my two draft verdicts BOTH refuted in verification)

The ladder ran to plan: pre-flight (all 4 rungs acquired 2/2 on cal seeds; horizon 147300
= max onset 45300 + 3×30000 period + 12000 margin) → 40 verdict arms (natural + the
matched-separation control, 5 seeds/rung, all 5/5 acquired — no ACQUISITION-STARVED) →
adversarial verification (37 agents, 4 lenses, 20 confirmed findings; all artifact
arithmetic and construction integrity reproduced clean — threads=1, spec_hash consistent,
teaching fence intact). **My draft claimed a clean COVERAGE-NULL + a new inverse
"tighter-anchor-helps" lever; verification refuted BOTH. The honest verdict is
INCONCLUSIVE.**

**What is real (estimator-free full-post-onset window — see the instrument lesson):** the
NATURAL ladder's routing input-sensitivity (asg_dist survival) rises ~monotonically with
coverage — v2 0.033 → v4 0.137 → v8 0.158 → v16 0.179 (3/3 up-steps, ~5.4×). **But
coverage is COLLINEAR with anchor min-separation (denser = tighter: v2 1.205 → v16 0.896)
AND with acquisition onset**, so the rise cannot be attributed to coverage per se.

**Why COVERAGE-NULL is NOT established — the control is confounded.** The
matched-separation control (closest-anchor-pair rotation to a common min-sep) is
NON-UNIFORM: it perturbs the sparse rungs heavily (v2 min-sep 1.205→0.896, mean-sep
1.379→1.283) and the dense rung ~not at all (v16 0.896→0.863). Its "flatness" is produced
by lifting ONLY v2 — within-rung, coverage-fixed asg change nat→ms is **v2 +0.130, v4
−0.001, v8 −0.040, v16 −0.016** — i.e. the construction raises the sparse end and leaves
the rest, which flattens the ladder as an ARTIFACT, not as evidence that coverage is
inert. And it is underpowered (n=5; matched-sep pairwise |t|<0.7).

**Why the "tighter min-sep lever" is NOT supported — no within-rung dose.** The apparent
inverse lever (pooled corr(min_sep, asg) = −0.38 across 40 runs) is the
coverage/perturbation collinearity wearing a min-sep mask: the within-rung effect
(coverage held fixed) is entirely v2 (the most-perturbed rung); v4/v8/v16 are
flat-or-negative. There is no min-sep dose-response with coverage removed. The claim is
struck.

**What survives — a named LOOSE THREAD, not a mechanism:** heavily re-perturbing the v2
(category-only) anchor lifts its routing-survival ~4× via an UNIDENTIFIED channel
(candidates, all co-varying in the closest-pair construction: min-sep, mean-sep,
acquisition onset, generic anchor re-draw). It is real (persists at matched onset: early-
window means 0.281 vs 0.057) but un-attributed. A residual hint also noted: terminal
asg_dist is weakly coverage-positive in BOTH ladders (window-mean buries it; weak).

**THE INSTRUMENT LESSON (a real scorer correction, canonized like EXP10's force_period).**
The pinned verdict window "W_post = 3 collapse periods in the rung's OWN regime" is
UNUSABLE here: the per-rung den-period estimator is fallback-dominated (3/5 estimation
failures on some rungs → the PERIOD_WORD=4800 fallback) and swings 6× (cal 30000 vs
in-regime 4800), so the window is effectively arbitrary-length and it manufactured the
draft's non-monotone "v8 peak / 5.0× endpoint" (v8's short fallback window caught only its
post-onset plateau). **The estimator-free full-post-onset window is the honest read; the
period-normalized window is RETRACTED** (kept in the artifact for provenance). Pre-registered
fork note: §4 assumed degrading min-sep HURTS; the data came in orthogonal to that
assumption — the machine-written `geometry_fork.verdict` string ("coverage dominates
uphill") is stale/inverted and must not be quoted.

**HONEST ANSWER TO THE RULING'S QUESTION ("does naming more of the space keep routing
input-sensitive?"): EXP11 cannot answer it cleanly.** The natural rise is inseparable from
the min-sep and onset confounds; the control built to separate them is itself confounded by
non-uniform perturbation; the study is underpowered. Neither COVERAGE-SCAFFOLD nor
COVERAGE-NULL is demonstrated. **The anchor lever remains UNMEASURED — EXP11-v1's execution
had a flawed control, not a null.**

**WHAT A CLEAN REDO NEEDS (design inputs, for the ruling):** (1) a UNIFORM
matched-min-separation control — re-draw EVERY rung's anchor to a common min-sep by the
same method (rejection sampling / optimization at unit norm), or the parked D-scaling
control — not the non-uniform closest-pair rotation; (2) a FIXED common post-onset verdict
window (the period-normalized one is retracted); (3) more seeds (n=5 underpowered); (4)
the loose-thread control (perturbed-but-same-min-sep vs tighter) to identify the v2
channel. **The decision — clean-redo the anchor lever vs move to the routing-side
counter-force (the manufacturing-class last resort) — is Jason's ruling.** Steps 5–6 stay
BLOCKED; no arm was a fix.

## §10.18 — THE STATIC-LINE WRAP (2026-07-04): the static-frame line is RETIRED; continual time is the primary frontier

**Ruling (Jason): WRAP, not redo.** EXP11's inconclusive-by-flawed-control (§10.17) is not the
"measured exhaustion" that would trigger the routing-side counter-force, and the anchor lever is
worth measuring — but not in the static frame. The clean-redo design is BANKED as a pickup and the
coverage question RE-POSES inside the continual-time rig (EXP12) where its answer is load-bearing.
The counter-force stays PARKED (manufacturing-class last resort). **Gate steps 5–6 RETIRE with the
static line** (they were static-rig gates; the teaching test re-poses at its own gates in the
continual-time rig).

**THE STATIC-LINE LEDGER — what the exp05–exp11 static-frame program established.**

*Proved (demonstrated, on the record):*
- The evocation channel CARRIES end-to-end — the first live word→category evocation in the deployed
  rig (Step-0(c), seed 2, cat_div 1.423 / dist 0 / share 1.000; §10.12 Gate-4 era).
- The collapse is LOCALIZED: capacity-open ASSIGNMENT-side dead-dictionary (argmax_k=1 sustained,
  Δ2 depth open, prototypes alive) — §10.12.2.
- The ENGINE is the gap-3 no-detach TARGET-side pull (necessity demonstrated by the detach arm) —
  §10.12.1.
- The WORD is a ~5× accelerant + pin-deepener; fate shared end-to-end (no-word self-pins ~518k) —
  §10.12.2/§10.12.3.
- The basin is PREVENTION-PRIMARY / RECOVERY-UNRELIABLE (mostly-absorbing flow with stochastic
  position-conditioned re-amplification pockets) — §10.12.3.
- Two design regimes (EXP09 slow-reference, EXP10 structured variation) both return
  STOP-GRAD-IN-COSTUME — the intervention is indistinguishable from its detach-null; **Fork 1(a)
  UNRESOLVED-NOT-REFUTED** on two independent regimes — §10.14/§10.15.
- The instrument arsenal (windowed estimators; dynamics panels; den = one-sided collapse-floor
  tripwire; the guarded-v2 scorer with force_period; acquisition-aligned reads; in-regime
  calibration; the manifest-time independence asserts) + the DETERMINISM CONTRACT (seed +
  construction order + torch threads=1, recorded).

*Manufactured — the collapse's ROOT, [COHERENT-DEDUCED, NOT DEMONSTRATED — the motivating
hypothesis EXP12 tests, not a proved result]:* **task degeneracy.** The stimulus draws members
i.i.d. uniform, so the deck-average (mean over all members) is nearly optimal for the masked-slot
reconstruction — member-CONDITIONAL routing buys almost nothing against the loss, so it is not
reinforced and collapses to the dead-dictionary mean. On this reading the whole static-frame
collapse is a property of the i.i.d. TASK, not of the operator, the anchor, or the reference —
which is why every target-side / input-side / reference intervention hit the same wall. **Status
tag binding: this is a deduced synthesis; it is the HYPOTHESIS the continual-time discriminator
tests (persistence breaks the i.i.d. degeneracy — if member-conditional routing survives with
dwells but not with shuffled dwells, task degeneracy is confirmed as the root). Do not cite as
demonstrated.**

**NEXT — EXP12 (scene persistence: the minimal temporal fabric).** The continual-time rig makes the
task non-i.i.d. by giving members DWELL (persistence across waves). Pre-committed now: the
**SHUFFLED-DWELL DISCRIMINATOR from day one** (dwelled vs shuffled-dwell i.i.d. control — the direct
test of the task-degeneracy hypothesis).

**The FOUR-CELL inference table — pre-registered WHOLE (Jason, 2026-07-04; the confirming-cell-only
reading was incomplete).** Both arms keep per-frame jitter; shuffling kills only the cross-wave
ORDER (persistence), not the within-frame variation. A both-die result must NOT be misread as "the
pivot was aimed wrong" when it may be a mis-built fabric:
- **Dwell SURVIVES / shuffled DIES** → the temporal fabric is load-bearing; **root PROMOTED to
  demonstrated.**
- **BOTH DIE** → NOT a clean refutation → **Fork 1.5**: persistence-as-built may fail to create
  demand (identity copy-free, or the mask/onset geometry wrong). Routes to a **Fork 1.5 audit BEFORE
  any root re-ruling** — root neither confirmed nor refuted until the fabric is shown to create
  member-conditional demand.
- **BOTH SURVIVE** → the EXP10 prior applies (variation alone opens routing; both arms retain
  per-frame jitter, shuffling removes only order) → **VARIATION-SUFFICES, fabric not needed; root
  REFINED, not confirmed.**
- **Dwell DIES / shuffled SURVIVES** → inversion → **instrument / leakage audit** (a
  wrong-direction result implicates the rig before the hypothesis).

The UNPREDICTABILITY PIN (three clauses) carries; the
ANCHOR arm carries the banked clean-redo design (uniform matched-min-sep, fixed common window, seed
floor, loose-thread disambiguation); acquisition-aligned reads, in-regime calibration, guarded
scorer v2, dynamics panels all carry. **Opening fork for the next session: what within-dwell
evolution IS, mechanically.** Handoff: `docs/HANDOFF_next_chat_continual_time.md`. Steps 5–6 retired;
no arm is a fix.

## §10.19 — EXP12 SCOPING RESOLVED (2026-07-04, design chat): five forks ruled; prereg RATIFIED FOR BUILD

**Live spec: `docs/EXP12_SCENE_PERSISTENCE_PREREG.md` (ratified 2026-07-04 — checkpoint read
complete; Amendments A/B + the B1/B2 propagations applied; §13 constants ratified with
Adjustments 1–2 and the margin guard; arms do not run until the stage-two calibration constants
are recorded).** This unit records the fork RULINGS; the prereg carries the constants.

**Five forks resolved:**
- **F1 — the walk law: stochastic OU jitter.** Member nuisance/pose drawn at dwell onset from
  the family marginal, then bounded per-axis OU steps around the onset pose; one fixed walk law,
  hyperparameters global across members; increments stochastic. **Struck overclaim, on the
  record (do not re-import): "cheapest good completion at all lags is knowing the member" is
  FALSE** — clause 2 (nuisance ⟂ identity) forbids member knowledge improving nuisance
  completion, and identity-copy from any visible same-dwell neighbor is free under every walk
  law. **Routing demand lives in mask geometry + dwell-onset rate, not in the walk.**
- **F1 amendment — background recurrence:** onset poses come from a persistent configuration,
  not fresh family draws. **v1 = ONE fixed background configuration (pin-to-constant) + OU
  jitter around it**; the background library is a later rung. Grounds: familiarity must be
  *earnable*, not just family-robustness; a learned background concentrates completion gradient
  on the member component. Canon language (correction, carried): the familiar background earns
  **LOW** prediction error — that is *why* it is ignorable; the new object is the
  **high-divergence residual**. Binding: background ⟂ member.
- **F1.5 — completion geometry:** **wave-local completion** (the completer sees only the
  current wave [vision ; word-anchor slot]; NO trace machinery in v1 — v1 tests
  persistence-as-GRADIENT-ORDERING only, and **a v1 null is NOT fabric-refutation**) + the
  **GUARANTEED ONSET EXAM** (every dwell's first wave: word slot masked, vision visible —
  route-and-recall through the dictionary is the only completion path). **Division of labor,
  pre-registered: onset waves = ROUTING EXAMS (the verdict axis); mid-dwell vision-masked waves
  = THE TEACHING CHANNEL; onset completion is never teaching evidence, mid-dwell completion is
  never routing evidence.** Wrong-reason outcome pre-registered: completion-good/routing-dead =
  **shortcut-through-recency** — a named finding, never a pass; the onset/mid-dwell split is
  its discriminating read (the exam wave has no recency channel).
- **F2 — the dwell law: shifted-capped geometric, k = k_min + Geom(p), capped.** Constant
  hazard in the bulk = the only clockless law (fixed-k and bounded-uniform EXCLUDED on pin
  clause 1 extended into the time axis). New binding numeric asserts: **k ⟂ member** (duration
  must not code identity) and the cap-hit ceiling. Member draw uniform with **no immediate
  same-member repeat** (else the prior dwell contaminates the onset exam via recency).
- **F3 — 12b (the no-word comparator), gated with TWO pre-registered openers:** (i) the promote
  cell — full seeds, the teaching test at its own gates; (ii) the both-die cell — reduced
  seeds, as the word-culprit discriminator. Construction pin: **absent-word, NOT
  scrambled-word.** Same arm, two triggers; epistemically closed either way.
- **F4 — the baseline (conventional trainability control), banked with two openers** (both-die
  → trainability discriminator | promote cell → generality leg, **context not gate**).
  **Escalation ladder BINDING: baseline → 12b → visibility rung** (world-untrainable moots
  word-attribution, which moots escalation). **Thermometer, not donor:** shares stimulus +
  objective family ONLY — no shared components, no design flowback; **generality read
  ONE-DIRECTIONAL** (baseline-fails-where-PAM-passed = context, NEVER a PAM-superiority claim;
  the flattering direction fenced before any result exists).

**The four-cell inference table is pre-registered WHOLE (prereg §7), all cells named before the
run, including the anomaly cell** (dwell-dies/shuffled-survives → inversion → instrument/leakage
audit; named finding only). **Construction pin: A-SHUFFLE carries the IDENTICAL waves and the
IDENTICAL mask schedule, order-shuffled** — destroys dwell contiguity and nothing else; same
exams, different order; otherwise the table confounds exam rate with persistence.

**Amendment B — THE SURVIVAL-READ GEOMETRY PIN:** the verdict is geometry-matched to what the
task PAYS at rig topology. At v2, wave-local, vision-masked waves give the completer no member
cue (word = category only, background ⟂ member, no trace) — category-mean is optimal by
construction, so no gradient ever pays 16-way routing; onset exams pay exactly the 2-way
partition. **VERDICT AXIS = category-partition input-sensitivity (category-partition asg_dist);
16-member asg_dist rides as companion/characterization ONLY; 16-way survival is the coverage
LADDER's question, never rig-1's.** A 16-member survival bar would demand unpaid structure and
manufacture a wrong-reason both-die — the matched-bar lesson, surfaced before the run instead of
after it. Propagated to the baseline's own bars: **(B1) latent CATEGORY-separability** (windowed
between/within-category separation ratio in its own representation space, in-regime floor);
**(B2) onset-exam analog lift over the CATEGORY-PRIOR floor** (lift over deck-mean IS
category-lift at v2), acquisition-aligned. Never scored on PAM's asg machinery.

**REGISTERED PREDICTION (cross-scene contrast, 12b):** word-present differentiates word-tied
axes FASTER than no-word, on identical fabric/seeds/schedule — measure = acquisition-aligned
differentiation LIFT on word-tied axes (lift, never share). The registration's edge: the same
channel that was the ~5× *collapse* accelerant in the degenerate task is predicted to accelerate
*differentiation* in the live one — same channel, opposite sign, regime-discriminating.
**Falsifiers pre-named:** (a) word re-accelerates collapse on live fabric (fate-shared,
recurring); (b) no contrast (channel inert on healthy fabric).

**REGISTERED OBSERVABLE (earned salience, rig-1; expectation, NOT a gate):** PAM divergence on
background axes FALLS with exposure while member-onset divergence STAYS HIGH.

**Sequence: build → calibration pre-flight (stage-one/two; constants recorded before any
verdict run) → rig-1 arms (A-DWELL, A-SHUFFLE; verdict seeds {0–4}, +2 pool {5,6} reserved for
the margin guard) → four-cell read behind the verification pass → margin guard → ladder-ordered
fires as triggered → one review.** Banked arms (12b, baseline openers, coverage ladder,
splitting arm, coherence-ablation) are built-when-fired, not speculatively. No arm is a fix.

### §10.19.1 — STAGE-ONE ADDENDUM (2026-07-05): built + reviewed + re-calibrated on the corrected law; THE FIRST MEASURED FABRIC FACT

**Build + pre-run review.** Harness committed `a98b45a` (wave-local W=1 rig; fabric on 9
dedicated substreams; one code path — step() inherited). The standing verification pass ran
BEFORE the first run (32 agents; 15 confirmed → 5 distinct, all fixed pre-run): the two §13.10
majors (an extra conditional mask-stream draw that let a probe-rate change reshuffle the whole
downstream schedule → both per-dwell coins now drawn every dwell, rate-nestedness
regression-tested; the probe read taken post-update vs the scheduled exam's pre-update stash →
probe now reads pre-update) and a §10.14-ban violation in the stage-one period read (static-line
4800-pin/1.5×-band/20100-cut estimator → replaced with the estimator-free in-regime read;
cycle-present-period-unmeasured labeled exactly that). Wave-local consequences recorded as CC
choices, not silent patches: **L_JEPA inert by construction** (the §3(a) RECORDED GUARD — W=1
idles the deployed loss's one next-wave-prediction term; the anti-forward guard enforced
structurally); no u-carrier (within-window order does not exist at W=1); the EXP10 word jiggle
not carried (the fabric enumerates member nuisance + background only).

**Ruling 1 executed (dwell law amended in place):** k = 2 + Geom₀(0.1), support {2..48},
E[k]=11, cap 0.9⁴⁷ ≈ 0.707% — k_min = 2 realizable (law verified: min k = 2, P(k=2) = 0.100,
realized cap 0.73%). The stale-law stage-one (support-error law, 120k ceiling; committed
`45a0121`) is SUPERSEDED by the corrected-law re-cal below (160k ceiling, censoring-aware);
records stand in history. §13.8 asserts re-ran green on the new support (per-lag 0–48 stride 1;
k ⟂ member with the k=2 bin populated; schedule; background; dwell-permutation nulls).

**THE FIRST MEASURED FABRIC FACT — the acquisition asymmetry, NAMED so nobody "fixes" it:
the shuffled arm acquires ~10× faster than the dwelled arm, on every seed.** Corrected-law
re-cal (cal {20–24}, 160k, threads=1): A-SHUFFLE num-floor onsets {3.6k, 3.0k, 2.4k, 4.2k,
7.8k} — 5/5, all ≤ 7.8k. A-DWELL onsets {CENSORED, 31.8k, 6.3k, CENSORED, 103.2k} — 3/5
acquired at 160k. Mechanically coherent: interleaved (i.i.d.-like) gradient ordering reaches
the word→vision num floor fast; long same-member runs are bursty and slow to cover the deck.
**The out-of-family baseline REPRODUCES the asymmetry on the identical fabric** (B2 exam acc at
160k: shuffle 0.93–0.96 on 5/5; dwell 0.95/0.93 on 2 seeds, chance on 3) — a TASK property, not
a PAM property (the generality leg's one-directional read, pre-armed). This fact is
ENVIRONMENT-side and is NOT a defect to be tuned away; **the acquisition-aligned machinery is
what keeps it out of the four-cell table** (verdicts read post-onset per arm/seed; a censored
seed is UNREAD, never a dies; the +2 extension fires on read-count shortfall — §13.5 amended).

**Sensitivity-without-conversion is already visible at stage-one** (the §10 registered finding
class doing its job): num-floor acquisition fires while the onset-exam channel sits at chance
in BOTH arms (post-onset exam acc 0.478–0.513; lift ≈ 0 — the deck-mean word completion), and
asg_cat moves independently of the exam. Also measured: the draft conversion form (acc ≥ 0.6
×2 windows) FALSE-FIRES on 60% of chance segments including censored runs — rejected;
the chance-band-calibrated form went into the stage-two proposal.

**Collapse periods (W_post ladder inputs, per arm):** dwell — one measured cycle (18.6k), one
present-unmeasured, one no-cycle; shuffle — measured {43.8k, 9.3k}, one present-unmeasured, one
no-cycle. Period estimates disagree up to 4.7× across seeds within an arm (the §10.17 estimator
instability, present in-regime as expected).

**Stage-two constants PROPOSED (artifact `exp12_stage2_constants.PROPOSED.json`; NOTHING in
force until ratified in chat):** onset bound ≥160k (2 censored cal seeds — censoring-aware §13.9
form); W_post per the precedence ladder (dwell 3×18.6k = 55.8k own-period; shuffle 3×43.8k =
131.4k; sizing pin satisfied; the fixed-COMMON-window alternative 131.4k for both arms is the
EXP11-lesson-consistent recommendation); verdict horizon 303.4k; survival θ recommended =
dead-p95 0.0057 (alternates p90/p99 surfaced; the θ choice is DECISIVE on the cal spans —
exactly why it is ratified, never read off); probe-dwell rate 0.02; baseline B1 floors + B2
(floor 0); conversion form = chance-band p99 (acc ≥ 0.704) ×3 windows, measured false-fire 0.
Verdict arms run only after ratification.

## §10.20 — EXP12 RIG-1 FOUR-CELL VERDICT (2026-07-05, verified 28-agent/18-findings): **BOTH-SURVIVE** at the ratified constants; the splitting arm's trigger fires

**Constants in-force before any verdict run** (`exp12_stage2_constants.json`, commit 3120f54:
Rulings A/B + pins i–iv + the symmetric B2 completion; θ = dead-p95 0.00566 with the
dead-reference span definition written in; W_post = fixed COMMON 131,400 as a recorded ladder
amendment; horizon 303,400; probe rate 0.02 — the §13.10 monitor live).

**THE CELL (verdict seeds {0–4}, both arms, 303,400 waves, threads=1; every read seed
independently recomputed to 6dp in verification):**
- **A-DWELL: SURVIVES (read 4: 3S/1D).** s0 UNREAD window-truncated (onset 192,900 > 172,000 —
  pin i applied correctly); s1 0.00991 S; s2 0.01558 S; s3 0.00315 D; s4 0.01139 S.
- **A-SHUFFLE: SURVIVES (read 5: 5S/0D).** Means 0.0249–0.1443, θ-robust across the whole
  surfaced alternate range (4.4×–25.5× θ).
- No registered guard fires (no 3–2 split; 4 and 5 reads ≥ 3). Two latent scorer defects caught
  in verification and fixed UNEXERCISED (margin predicate was broader than the 3–2 letter;
  extension seeds entered on file-existence rather than guard-fire — both now letter-exact).

**REGISTERED READING (prereg §7, applied as pre-registered): variation + exam-scheduling
jointly suffice; the root is REFINED, not confirmed** (the EXP10 prior applies — both arms
retain per-frame jitter; shuffling removed only cross-wave order, and routing survived
anyway at these constants). **The splitting arm (shuffled + uniform masking) is the
pre-registered trigger that now fires — built-when-fired, awaiting the GO.**

**The verified texture (companions — none of it moves the cell):**
- **Mode asymmetry.** Shuffle survival is SUSTAINED-in-window (frac-above-θ 0.80–1.00); dwell
  survival is an INTERMITTENT, duty-cycled revival mode (frac-above 0.34–0.56, window medians
  mostly below θ, the mean carried by revival episodes). Dwell s1 is a late-REVIVAL seed —
  dead mass in its FIRST third, alive at horizon (run-end 98% above θ, 0% dead-signature): the
  suspected wrong-reason survival was the INVERSE shape.
- **READING-CHANGING instrument fact (to the ledger, no post-hoc re-pin): the ratified
  window-MEAN form certifies W_post-mean input-sensitivity, NOT alive-at-horizon** — the two
  are decoupled in this oscillatory regime. Shuffle s3 passes at 0.0915 yet is 98%
  dead-signature at run end; dwell s2's run-end clears θ by 1.0%; shuffle s1 (the strongest
  window survivor) is marginal at horizon. Collapse is NOT abolished on this fabric at long
  horizons — the fabric/ordering changes when and how routing dies, not whether it can.
- **READING-CHANGING θ-provenance fact (defuses the p99-ANOMALY alternate): the pooled dead
  reference is 85% shuffle windows with a ~32× arm-asymmetric tail.** θ as applied to the dwell
  arm is a shuffle-tail statistic ~24× the dwell arm's own dead reference — CONSERVATIVE
  against dwell survival; dwell cleared a bar dominated by the other arm's transition tail.
  The p99 alternate (which would read dwell 0S/4D) is even more a shuffle-tail artifact.
- **Conversion companion CORRECTED in verification (my draft gloss struck):** the "shuffle
  converts 3/5" read was band-edge flicker (s3's crossing = a 3-window flicker then back to
  0.458; s2 misdated by ~219k; s1 de-converts before horizon). **Sensitivity-without-conversion
  holds ARM-WIDE: both arms are asg-alive / exam-at-floor at horizon** — the §10 registered
  finding class fires for the campaign, not for one arm. The exam channel is paid and
  unconverted everywhere at 303k.
- **Arm-wide ordering inversion (recorded; companions never decide cells):** min shuffle
  window-mean (0.0249) > max dwell (0.0156); onsets 3.3–10.5k vs 16.5–192.9k — the shuffled arm
  both acquires faster AND holds more input-sensitivity. The BOTH-SURVIVE label under-claims
  this structure; it is the fabric fact (§10.19.1) continuing into the verdict regime, now with
  a survival-ordering attached.
- **§13.10 monitor: NO registered divergence bar exists (gap, on record).** Paired
  scheduled-minus-probe deltas: dwell 4/4 positive (max t ≈ +2.3 at s3; the two largest in the
  two weakest seeds), shuffle mixed-negative. Not a registered fire — fallback (c) stays
  unfired — but the direction is the anticipation direction in the dwell arm and the bar's
  absence is a named gap for the next campaign's constants.
- Second acquisition record: verdict-seed onsets replicate the §10.19.1 fabric fact (dwell
  slow/censored-class, shuffle ≤10.5k). **[The ordering-inversion reading is REGIME-BOUND —
  §10.20.2 rider: this fabric's order carries no completable structure by construction.]**

**Ladder state:** both-survive routes to the SPLITTING ARM (shuffled + uniform masking —
attributes between variation and exam-scheduling); the §8 escalation ladder does NOT open
(that is the both-die route); 12b full-seeds does NOT open (that is the promote route). The
coverage ladder stays banked (promote-cell trigger). No arm is a fix.

### §10.20.1 — SPLITTING ARM RAN (2026-07-05, verified 16-agent/12-findings, none verdict-changing): **A-SPLIT SURVIVES 3S/0D → variation alone suffices ON THE REGISTERED RULER — bounded hard by a 2–3× scheduling DOSE effect and 2/3 horizon deaths**

**Registered block prereg §14, recorded before launch; construction pins verified BIT-LEVEL in
verification** (A-SPLIT = the A-SHUFFLE fabric verbatim at each seed — raw/member/nuisance/
background/dwell/perm tensors torch.equal; mid-dwell masks bit-identical; all 13,426 mask
diffs at position 1; is_exam ≡ pos-1 ∧ word-coin; manifests differ only in arm + exam/probe
counts). Constants in-force verbatim; seeds {0,1,2}.

**THE READ (every number independently recomputed): SURVIVES 3S/0D** — window means 0.0348
(6.2× θ) / 0.0469 (8.3×) / 0.0077 (1.35×); onsets 3.3–3.6k; no registered guard fires
(3–0 is not the 2–1 letter). **The pre-named mapping fires: VARIATION ALONE SUFFICES — for
routing survival as registered (W_post-mean input-sensitivity above the dead reference), the
guaranteed onset exam is not necessary.** EXP10's variation thread confirmed on live fabric;
the both-survive joint reading collapses to its variation component ON THIS RULER.

**The verified bounds (all confirmed by recomputation; none moves the registered binary):**
- **Scheduling is a strong DOSE factor: removing the exams cost 40–70% of window-mean
  input-sensitivity on EVERY paired seed** (0.60× / 0.32× / 0.31× of the scheduled twin on
  bit-identical fabric; worst-seed margin fell 4.4× → 1.35× θ). "Not load-bearing" would
  overclaim — the exams are not NECESSARY for registered survival, and they roughly triple it.
- **At HORIZON the split arm dies 2/3 where its scheduled twin lives 3/3** (final-window
  [172k–303.4k] means: split 16.5× / 0.12× / 0.56× θ vs twins 7.2× / 23.2× / 9.7×). On the
  horizon axis — NOT the registered criterion; the §10.20 window-mean≠end-state lesson applies
  in both directions — **the exam scheduling looks load-bearing for PERSISTENCE-to-horizon.**
  Recorded as the natural next question, not a verdict.
- **s2 is DYING-IN-WINDOW** (quartile means 0.0176→0.0089→0.0042→0.00005; the 1.35× margin is
  front-loaded; the estimator-free full-span form reads 0.88× θ = DIES; adjacent forms would
  put the arm at 2S/1D = the backfill letter). The registered read stands — adjacent-form
  fragility is on the record, and the {3,4} backfill fires only on the letter or on a ruling.
- **A second channel moved by construction (registered, now named):** the uniform coin also
  RAISES teaching density (vision-masked fraction 0.456 → 0.500, +9.7% relative, including
  recency-free onset teaching waves the scheduled arm never presents). "Only the mask policy
  changed" is exact wave-wise; its composition shift has two components (fewer exams AND more
  teaching), and the attribution between them is not separable in this arm.
- **Acquisition: unchanged-or-EARLIER** (paired onsets 4800→3300, 10500→3600, 3300→3600) —
  halving onset word-masks delayed num-floor acquisition nowhere; acquisition rides the
  mid-dwell teaching channel, not the exams.
- **Companion corrections:** the FIRST REAL exam-channel conversions of the campaign appear in
  split s0, LATE and sustained (16-consecutive windows ≥ 0.704 at t≈258–262k, accs to 1.0;
  five distinct episodes — unambiguously non-chance), OUTSIDE the verdict window; the
  arm-wide sensitivity-without-conversion statement carries a per-run exception. Instrument
  note: the conversion chance band was calibrated at scheduled exam density (~27/window); the
  split arm halves it (~13.7) → the fixed threshold runs ~4× hot here and the 216.6k
  scorer-reported onset is chance-consistent under the corrected null (the late episodes are
  real regardless). Density-matched band = a constants item for any arm that changes exam
  rate.
- Process: the §14 discriminator guard letter now has a COMMITTED producer
  (`exp12_score.py --split`; the ad-hoc wrapper is superseded).

**Where this leaves the ledger:** the task-degeneracy root stays REFINED — on this fabric,
per-frame variation alone is sufficient for registered routing survival, the guaranteed exam
buys margin (2–3×) and horizon persistence, and dwell-ordering buys neither (the §10.20
inversion) **[REGIME-BOUND — §10.20.2 rider]**. Characterization of the both-survive cell is
complete at discriminator scale; the four-cell table is untouched. No arm is a fix.

### §10.20.2 — POST-SPLIT RULINGS (Jason, 2026-07-05, consolidated order; recorded in order)

1. **12b TRIGGER AMENDED (recorded, not silent):** opener (i) promote-cell →
   **routing-alive-demonstrated-arm-wide**. Grounds quoted from the Fork-3 record: the gate
   existed to run the teaching test "where routing can live"; BOTH-SURVIVE + the split arm
   satisfy the reason on every read arm; the letter assumed the shuffle arm dies. Amended in
   place in prereg §9; the 12b block runs per prereg §15.
2. **REGISTRATION RE-CUT (pre-run):** the 12b cross-scene-contrast prediction's primary axis
   = **SELECTIVITY** (word-tied-partition-selective differentiation contrast vs untied
   controls — the S index), **not speed**. Speed = companion, reported never fired on.
3. **REGIME-BOUND RIDER on §10.20 / §10.20.1:** "dwell-ordering buys nothing" is bounded to
   the NON-GENERATIVE fabric — unpredictability clause 1 makes cross-wave order carry no
   completable structure BY CONSTRUCTION, so the fabric offers ordering nothing to pay for.
   **Lawful-dynamics worlds (order that carries completable structure) = a NAMED FUTURE
   RUNG, under maximal trap-#1 (anti-forward) discipline. Continual motion is DEFERRED, not
   demoted.**
4. **STANDING PRINCIPLE:** compute is not a constraint → the banked-arm posture favors
   **parallel registered blocks** over serial minimalism (hence the two 12b blocks).
5. **s2 BACKFILL FIRED BY RULING:** split seeds {3,4} run as characterization only, AFTER
   verdict-invariance was written into §14 (worst case 3S/2D still passes; the registered
   read cannot flip).
6. **DENSITY-MATCHED CONVERSION BAND:** form registered (prereg §15); the constant is
   recorded at any exam-rate-changing arm's stage-two.

### §10.20.3 — 12b CAL TWINS RAN (2026-07-05): **REGIME FINDING — the zero-prediction-load word is INERT; constants NOT settable; verdict twins DO NOT run pending ruling**

**s2 backfill first (§14, fired by ruling):** seeds {3,4} both READ SURVIVES (0.0663 at 11.7× θ,
frac-above 0.886; 0.0227 at 4.0× θ, 0.834) — **A-SPLIT now 5S/0D**; the registered read stands
per the pre-written verdict invariance and the backfill STRENGTHENED it (the two backfill seeds
sit above all three original margins; s2's 1.35× remains the arm's floor case).

**The 12b cal outcome (cal twins {20–24} × {present, absent} × {shuffled, dwelled}, 160k, mask
policy (iii); twin parity verified `torch.equal` ex-word; exposure-wave loss-skip verified
clean):** **the num channel NEVER forms — max num over ALL 20 runs = 2.6e-5** (vs 0.284 at the
same seed under the scheduled policy); acquisition onsets None 20/20, present twin and absent
twin alike; **present and absent twins are indistinguishable on every panel.** The word,
presented as a pure reference with zero prediction load in either direction, never binds into
completion at these horizons. Mechanically coherent in hindsight: the strong binding force in
every prior arm was the word-PREDICTION gradient (unit-separated token targets); the teaching
direction's own gradient scales with the subtle r_category = 0.5 axis and evidently never
lifts the channel off the floor by itself. **The dose ladder now has three rungs: scheduled
exams (strongest routing + channel), coin exams (split: ~2–3× weaker), zero word-prediction
load (12b-(iii): channel never forms and the world collapses harder — 9/20 runs end
dead-dictionary, 15/20 end den sub-floor; both dwelled twins fully dead on most seeds).**

**Consequences (why constants cannot be set):** the aligned-window anchor (present-twin num
onset) has ZERO support; the S index has no post-onset windows to read; the raw S form is
additionally unbounded (ratio explosion as within→0 — any re-pin should use a bounded form,
e.g. between/(between+within)); the dead-reference regime SHIFTED (new-policy dead p95 0.0086
= 1.5× the in-force provenance — θ not transportable unflagged under (iii)). Artifact:
`exp12_12b_stage2.PROPOSED.json` (the finding + the instrument notes; nothing in force).

**What this is, read plainly: a result about the #12 reference, not a failed experiment.** The
teaching test's vehicle assumed a reference-only word still participates; measured, it does
not — **participation appears to require prediction load somewhere.** The registered
prediction (S-selectivity) is UNTESTED, not falsified: the channel never came alive to test.
**Ruling required before any verdict twin; candidate re-poses surfaced in chat** (e.g., re-pin
the twin policy to the SPLIT arm's coin-exam policy — word carries load at coin rate; twins
{present, absent} on that policy — or rule the inertness finding the block's answer and route
the teaching test elsewhere). No arm is a fix.

**RULED (same day): finding RECORDED + policy (iii) STRUCK; §15 AMENDED to the COIN POLICY;
cal re-runs at the new policy; constants back before verdict twins.** The re-pose pins
(recorded in prereg §15): present twin = the A-SPLIT coin policy verbatim; absent twin = the
same coin, the same draws, word-mask draws → EXPOSURE-ONLY — **the original option (ii),
rejected then as a dose confound, correct now because the dose IS the mechanism**;
vision-teaching density matched across twins by construction; **the dose control is S itself**
(the untied-partition subtraction cancels generic dose — selectivity was registered as the
dose-robust axis, and this is where that earns its keep); **bounded S form ratified**
(between/(between+within); instrument-validity, pre-verdict); **nothing transports** (θ, dead
reference, bands, sustained-N, horizons all fresh-cut at the coin policy's own stage-two —
the 1.5× dead-reference shift under (iii) proves the point); the S registration carries
unchanged.

### §10.20.4 — 12b VERDICT TWINS RAN (2026-07-05, verified 14-agent/10-findings, none verdict-changing, every number reproduced to the digit): **sh S-FIRES 5F/0N · dw S-NULL 0F/3N — with the fire's COMPOSITION decomposed in verification**

**Constants in-force before launch** (`exp12_12b_stage2_constants.json`, 48f0784: sh band
RE-CUT 0.049689 over the widened {20–29} pool per the ratified amendment — the widening
RAISED the bar from the thin-pool 0.0414 and from 0.0348-without-s26, and sh fired 5/5 over
the raised bar anyway; dw band 0.125053; N = 2/4; θ_companion 0.00775; fences recorded
verbatim). Twin parity verified on verdict artifacts; preview fence verified (every constant
derives from pre-onset/dead pools).

**[sh] S-FIRES 5F/0N (letter-valid; mechanically clean).** Onsets 3.0–5.1k; fires with
sustained runs 17–145 vs N=2; S_max 0.23–0.66. **BUT the verified composition changes what
the fire is:** in EVERY fire event the untied term −½(Δdist+Δa) is POSITIVE (+0.048..+0.085)
— **the subtraction built to cancel generic dose ADDED instead**, because Δsep_a runs
NEGATIVE: the ABSENT twin's a-partition separability (0.69–0.79) exceeds the present twin's
(0.53–0.71). **The dying no-word twin collapses ONTO the coarse partition; the word-present
twin does not.** Word-tied Δcat is genuinely positive in every fire event (0.023–0.064) but
carries only 26–48% of S there. Two regimes among the five fires: **s0/s2/s3 = sustained
positive-S** (means 0.115/0.081/0.179; 58–69% of windows above band, <8% below −band);
**s1/s4 = duty-cycled net-≈0** (≈20% above +band vs 15–20% below −band; s1's cat-axis signal
≈ 0 — artifact-compatible, its episodes band-adjacent). **The registered sentence "acting
selectively on what it names" is NOT licensed as-is**; what IS licensed at the verified
numbers: the word RESHAPES the present twin's geometry away from the comparator's
collapse-onto-the-coarse-axis, with a real but minority word-tied component — and the word is
strongly HEALTH-PROTECTIVE (falsifier (a) ANTI-fires: absent twins den-subfloor 0.72–0.89 vs
present 0.0–0.48).
**INSTRUMENT LESSON (the S-form's matched-bar moment): the untied "control" legs are
CONTAMINATED BY THE COMPARATOR'S OWN DEATH** — the dose-cancellation logic assumed a healthy
absent twin whose untied contrasts reflect generic dose; a collapsing absent twin
concentrates on the salient coarse axis and turns the control legs into a signal carrier.
Any S re-cut (Δcat-only companion, per-leg reporting, collapse-conditioned reads) is a
RULING, not a scorer patch.

**[dw] S-NULL 0F/3N — and STRONGER than the draft stated:** the read seeds' S_max values
(0.147–0.162) are the dw null pool's own tail behavior (pool p99.5 = 0.161, max 0.196; null
segments themselves produced runs up to 3 — N=4 is doing exactly its job). s0/s1 UNREAD
window-truncated (onsets 187.8k/274.5k — the pre-acknowledged dwelled lottery); 3 reads =
the minimum; no guard fires by the letter. The word-present dw twins are healthier on
asg_cat everywhere (0.017–0.024 vs 0.004–0.008) — the health effect without word-tied
selectivity.

**Corrections + records from verification:** falsifier-(a) "present healthier on every read
seed" corrected — dw s2's den-subfloor runs WORSE in the present twin (0.153 vs 0.093; the
asg_cat direction still holds there; the (a)-does-not-fire conclusion survives on the
preponderance, 7/8 seeds clean). s26-tail internal-consistency note ON RECORD: the in-force
sh horizon (152,400) is the thin-pool form while the band was re-cut on the widened pool
(the form on the widened pool would read 208,200) — an empirically ~1/10 sh truncation
lottery existed and did not bite (max verdict onset 5,100 vs cutoff 21,000);
verdict-conservative direction. Scorer t-alignment assert added (hygiene; no consequence —
all twin pairs verified aligned).

**Ledger:** the teaching test's first verdict-grade data: the word channel on live fabric is
(1) health-protective (both fabrics), (2) geometry-reshaping vs the no-word collapse
(shuffled fabric, letter-fire), (3) NOT yet demonstrated word-tied-selective in the
registered sense (composition impure on sh; null on dw), (4) inert without prediction load
(§10.20.3). Registered falsifier (a) does not fire; falsifier (b) fires for the DWELLED
block only. Rulings owed: the sh-fire interpretation (letter vs composition), any S re-cut,
and the dw follow-ups. No arm is a fix.

### §10.20.5 — RULED (2026-07-05): **S RE-CUT to S_w (word-tied contrast alone); constants from existing cal; the re-cut ruler grades FRESH seeds {5–9}, both blocks**

**The ruling, recorded in order:** (1) the §10.20.4 composition finding is accepted — the
composite S's untied subtraction is **retired for this regime** (its premise, a healthy
comparator whose untied contrasts reflect generic dose, fails when the comparator collapses
onto the coarse partition; the control legs carried signal). (2) **S_w = Δsep_cat (present −
absent, bounded form) is REGISTERED as the primary axis**; the untied contrasts and the old
composite S are demoted to reported companions — never subtracted, never fire criteria. The
re-opened dose caveat is carried honestly: S_w does not cancel generic dose; **the untied
companions are the dose-visibility check** (generic dose predicts comparable positive
contrasts on untied partitions; word-tied selectivity predicts Δcat ≫ untied). (3)
**Constants from the EXISTING cal twins** — per-fabric S_w null bands from the same
pre-onset null source (sh over the widened {20–29} pool; dw over {20–24}), sustained-N
re-checked; windows/horizons/taxonomy/letters carry in force unchanged. (4) **FRESH-SEED
DISCIPLINE: verdict seeds {5–9}** — the re-cut ruler never grades the {0–4} seeds whose
data motivated the re-cut; their S_w values may be reported post-hoc as labeled companions
after the fresh read exists. One review per block, behind the verification pass.

### §10.20.6 — S_w FRESH-SEED VERDICTS (2026-07-05, verified 18-agent/9-findings, none verdict-changing, mechanics exact): **sh S_w-FIRES 4F/0N ROBUST · dw S_w-FIRES 3F/1N FRAGILE — and the dw flip is a SEED-BATCH effect, not the ruler**

**Constants:** S_w bands from existing cal only — sh 0.006353 (n=348, N=2; null max run 1,
only 3/348 windows above band), dw 0.019755 (n=1414, N=5; null max run 4, once). One
pre-run event: **sh seed 9's fabric was REJECTED by the k⟂member manifest gate** (chi2
85.36 vs null-p99 83.42 — a 2.3% exceedance at a 1% test after ~29 fabrics this session;
verified OUTCOME-BLIND: the gate runs before the manifest write and before wave 0, and
consumes only construction fields; dw s9 passed at its longer dwell sequence). Committed
record `exp12_12bc_sh_s9_REJECTED.json`; the sh block reads on {5–8} (4 ≥ the min-3
letter); **substitution (s10) not improvised — a ruling if wanted.**

**[sh] S_w-FIRES 4F/0N — ROBUST.** Every fire dwarfs the null: the weakest (s6, the
duty-cycle regime again — negative window mean, oscillatory) still has 21.6% of windows
above band (25× the null rate), 24 distinct runs ≥ 2 where the null never produced 2
consecutive anywhere, max 5.6× the null max; s5 is the showcase (mean 0.0453, frac 0.565,
run 77). **Dose-visibility passes on the correct normalization: NO untied leg fires its
own analogous band on any sh seed** (dA +0.010..−0.063, dDist −0.015..+0.003, all quiet
vs their own nulls). INSTRUMENT NOTE (reading-changing, recorded): the registered
"Δcat ≫ untied" wording is SCALE-MISMATCHED in raw units — the untied contrast nulls are
40–60× wider than the S_w null (dA p99 0.38–0.40 vs S_w band 0.006–0.020); the check is
valid ONLY as each-leg-against-its-own-band. Caveat on record: the sh null pool is 62%
one cal seed (s26, the slow acquirer that donated the fattest pre-onset span).

**[dw] S_w-FIRES 3F/1N — LETTER-VALID, EVIDENCE FRAGILE.** The three fires are three
different shapes, none clean: **s5 = persistence-only** (run 59 = 14.8× the null max run,
but amplitude INSIDE the null tail — run mean 0.0252 vs null p99.5 0.0233); **s7 =
mirror-oscillatory** (fires run 15 but runs BELOW −band harder: 20; mean −0.005); **s8 =
band-adjacent AND fails the apples-to-apples check** (exactly-N runs, amplitude never
leaves the null tail, and its untied dA leg WOULD fire the analogous own-band criterion —
the one read where selectivity fails like-for-like). s6 clean null; s9 window-truncated
(onset 281.1k).
**THE CROSS-RULER DECOMPOSITION (labeled post-hoc companions, never verdicts): the dw
S-NULL {0–4} → S_w-FIRES {5–9} flip is a SEED-BATCH effect, not the ruler re-cut — each
batch gives the SAME letter under BOTH rulers** (dw {2,3,4} under S_w: 0F/3N; dw {5–9}
under composite S: 3F/1N). Combined dw evidence over 7 read seeds: 3F/4N. **The dwelled
block's selectivity is a seed lottery at current power** — the letter fires on this
batch; demonstration-grade it is not.

**Health companion, corrected texture:** sh unchanged (absent twins deep in den collapse
0.686–0.838 vs present 0.0–0.221; word-present clearly healthier). **dw INVERTS on the
den channel** (present den-subfloor HIGHER in 3/4 reads: 0.239/0.166/0.257 vs
0.032/0.068/0.159) while asg_cat still favors present everywhere — on the dwelled fabric
the word buys assignment-side category sensitivity at some content-contraction cost. The
health story is fabric-dependent, not universal.

**Registered-prediction status after fresh seeds: word-tied SELECTIVITY is DEMONSTRATED on
the SHUFFLED fabric** (S_w, fresh seeds, robust against a clean null, untied legs quiet on
their own bands, batch-consistent direction with the {0–4} composite fires). **On the
DWELLED fabric it is letter-fired but NOT demonstration-grade** (fragile shapes,
batch-unstable, one like-for-like failure). Falsifier (a) does not fire on the routing
axis anywhere (den-channel inversion on dw noted); falsifier (b) is batch-dependent on dw.
Rulings owed: the dw-block standing (letter vs fragility — more seeds / leave as lottery /
route elsewhere), the s10 substitution, and whether the sh demonstration promotes any
Guiding-List candidate machinery. No arm is a fix.

### §10.20.7 — RULED (2026-07-06): STANDING SUBSTITUTION RULE (applied: sh s9→s10) + the EARNED-SALIENCE READ registered (the Guiding-List second leg). Recorded BEFORE the substitute runs and before the read produces a number.

**(1) STANDING SUBSTITUTION RULE (a ruling, not an improvisation — closes the §10.20.6
open item).** When a seed's fabric fails a §13.8 manifest gate PRE-RUN, the seed is
substituted by the LOWEST unused seed of that block's registered continuation pool, in pool
order. Conditions and consequences, all binding:
- **Validity ground:** the gates run before the manifest write and before wave 0 and consume
  only construction fields (verified outcome-blind in the 18-agent S_w pass) — substitution
  therefore opens no selection channel on outcomes.
- **Twin discipline:** the substitution covers the WHOLE twin pair (twins share fabric draws
  by construction; a split-seed pair is not a twin).
- **Records:** the rejected seed's committed record STANDS (never deleted, never re-rolled);
  the substitution is recorded before the substitute runs.
- **Pool accounting:** the consumed pool seed is no longer available to the margin-guard
  extension — extension draws the next unused pool seed. If the pool is exhausted, the block
  reads on what it has under the min-3 letter; further seeds are a ruling.
- **Standing of the substitute:** a substituted seed is a VERDICT seed under the block's
  registered criteria, letter-equal with the original set. If the substitute's fabric ALSO
  gate-rejects, the rule re-applies (next pool seed), each rejection committed.
**Application recorded now:** sh 12bc twin pair, s9 (committed record
`exp12_12bc_sh_s9_REJECTED.json`) → **s10** (head of pool {10,11}); sh extension pool becomes
{11}. Scorer touch registered with this ruling: `SW_SUB = {"sh": {9: 10}}` applied to
SW_SEEDS in `exp12_score12b.py`; dw untouched (its s9 passed). Recorded before the s10 twins
run.

**(2) EARNED-SALIENCE READ — form recorded before the read.** The observable is already
registered (prereg Amendment A = §10.19: "PAM divergence on background axes FALLS with
exposure while member-onset divergence STAYS HIGH"; a rig-1 readout; **expectation, NOT a
gate**). The read runs off the EXISTING rig-1 verdict artifacts, seeds {0–4}, BOTH arms
(A-DWELL, A-SHUFFLE) — no new runs; the columns are the registered ones (the pos-1
member-onset exam prediction-divergence components `div_bg` / `div_id`, `div_nuis` as
companion; exposure axis = wave t, the fixed background present from wave 0). Read form
(reader `exp12_salience_read.py`, committed with this ruling):
- Per seed: **EARLY** = mean over the first decile of div-bearing columns, **LATE** = mean
  over the last decile; full-series least-squares slope as the trend companion.
- **FALLS(bg)** := div_bg LATE/EARLY < 0.7 AND slope < 0. **STAYS-HIGH(id)** := div_id
  LATE/EARLY > 0.7. The symmetric 0.7 knob is declared here as illustrative strictness —
  the full ratios/slopes are reported per seed so the letter can be re-cut by ruling without
  re-measurement; borderline cases are surfaced, never force-lettered.
- **LANDS per seed** := FALLS(bg) ∧ STAYS-HIGH(id); arm letter = majority of 5.
**Scope fence:** this read feeds ONLY the second leg of the Guiding-List promotion trigger
(the first leg — the cross-scene contrast — is the §10.20.6 sh demonstration). Promotion
itself remains a ruling; landing here licenses nothing else. Expectation-not-a-gate carries:
a non-landing changes no committed verdict.

**(3) Not in this order:** the dw-block standing ruling remains OPEN (§10.20.6). Results of
(1)'s substitute read and (2)'s read are appended below after the standing verification
pass.

**RESULTS (2026-07-06; verified 10-agent — 5 refute-default lenses + 5 per-finding
adjudications; every number digit-exact, verdict artifact byte-reproduced, NO letter moved;
2 reading-changing framing corrections recorded below as written, 3 cosmetic):**

**(R1) Substitution applied — the sh block STRENGTHENS to S_w-FIRES 5F/0N.** *[SUPERSEDED
→ §10.20.7-AMEND below: block letter = 4F/0N on [5,6,7,8]; s10 = out-of-block
confirmation, numbers stand as verified.]* s10's fabric
passed all §13.8 gates; twins verified same-fabric; **s10 FIRES, second-strongest in the
block after s5** (Sw_mean 0.0192, Sw_max 0.32366, 50.3% of windows above band, longest run
46 vs N=2 where the null's max run anywhere is 1; onset 3000). Scorer tally verified
[5,6,7,8,10] — s9 never read (its REJECTED record cannot be picked up), dw block invariant
(3F/1N + s9 window-truncated, substitution=None), sh extension pool = {11}. Dose-visibility
on own-band normalization: dA −0.03892 / dDist +0.00941, NEITHER fires its own analogous
band — consistent with the §10.20.6 pattern (no untied leg has ever fired on sh). Health
companion: word-present healthier (asg_cat_end 0.0274 vs 0.0090; den sub-floor
present-healthier over the aligned window). **The §10.20.6 sh selectivity demonstration
carries at 5F/0N on the full substituted verdict set.**

**(R2) Earned-salience read — DOES-NOT-LAND, 0/5 on BOTH arms** (reader vs fresh
re-implementation: zero mismatches; artifact `exp12_salience_read.json`). Per-seed
(bg-ratio / id-ratio, late-decile over early-decile): dwell s0 0.6372/0.4088, s1
1.1106/2.0794, s2 2.3529/2.6451, s3 0.0493/0.0597, s4 0.3201/0.4123; shuffle s0
1.5381/0.5255, s1 0.1625/0.4338, s2 0.7607/0.4567, s3 0.1648/0.0663, s4 0.0684/0.0550.
Texture, verification-corrected:
- **On the DWELL arm the two components are fate-shared** — co-directional on all 5 seeds
  (id/bg ratio-of-ratios 0.64–1.87): background and member-onset divergence rise and fall
  TOGETHER; no seed shows the differential signature. **The SHUFFLE arm is not universally
  co-directional** (the correction): s0 is anti-directional (bg ROSE 1.54× while id fell to
  0.53 — the wrong direction for the expectation) and s2's div_nuis rose while bg/id fell
  (the "nuis tracks the same way" gloss is dwell-only). Neither exception approaches the
  landing signature.
- **Knob-robustness, exact form:** at the declared 0.7 knob and ANY symmetric knob ≥ 0.5,
  zero seeds land. The full symmetric-K sweep finds THREE formal landings at pathological
  knobs — dwell s3 K∈(0.049,0.060) (id fell 94%), dwell s4 K∈(0.32,0.41) (id fell 59%),
  shuffle s1 K∈(0.16,0.43) (id fell 57%; the widest window and the dataset's largest
  ratio-of-ratios, 2.67, on the CONTROL arm — which strengthens, not weakens, the
  no-differential reading). Max landers at any single K = 1/5 per arm; majority is never
  reached; **both letters are K-invariant.**
- **Borderline surfaced (both blockers, per adjudication):** dwell s0 — bg ratio 0.6372 <
  0.7 but POSITIVE LS slope (+0.0042/100k, non-monotone trajectory) fails FALLS(bg) under
  EVERY threshold choice (the slope-sign conjunct is definitional, not a knob); and its id
  ratio (0.4088) below its bg ratio independently blocks every symmetric re-cut.
- **Reader hygiene notes (cosmetic, recorded not silently patched; reader stands as the
  committed provenance of the artifact):** (i) cuts on rounded values (4dp ratio / 6dp
  slope) vs the raw-value canon text — flip windows 5e-5/5e-7, margins clear by >3 orders,
  flags identical both ways on all 10 seeds; (ii) div-row filter keyed on div_bg alone vs
  "div-bearing columns" — identical row sets on every artifact (all 1011 columns carry all
  three components); latent-only, noted for any future reuse.

**(R3) Consequence for the Guiding-List trigger (plain reading; the promotion call remains
a ruling):** leg 1 (cross-scene contrast) now stands at 5F/0N *[SUPERSEDED →
§10.20.7-AMEND: 4F/0N + out-of-block confirmation at s10]* on sh; leg 2 (the
earned-salience curve) DOES-NOT-LAND — **the registered promotion trigger does NOT fire;
the candidate stays CANDIDATE-HELD.** The Guiding-List entry is untouched (annotating it is
Jason's call). Expectation-not-a-gate carries: no committed verdict moves. Mechanical
texture for any re-pose ruling: the onset-divergence probe's components scale together
(dominated by global acquisition/collapse dynamics — an echo of the static-line fate-shared
ledger item), rather than differentially by axis; a background-selective decline is not
what this fabric produces at this operating point.

**Open after this order: the dw-block standing ruling (§10.20.6) and any
earned-salience re-pose / Guiding-List annotation.** *[Closed by §10.20.7-AMEND below.]*

### §10.20.7-AMEND — QUARANTINE EXECUTION (Path A, RULED 2026-07-06; amended in place under the forward-pointer rule — the R1–R3 text above STANDS as written)

**(A) sh block letter = S_w-FIRES 4F/0N on [5,6,7,8] — the §10.20.6 reviewed verdict
set.** **s10 is RECLASSIFIED: OUT-OF-BLOCK CONFIRMATION** — labeled,
never in the tally; its verified numbers stand exactly as recorded in R1 (fire
second-strongest, mean 0.0192, max 0.324, run 46 vs null-max 1; untied legs quiet on own
bands; present twin healthier). **Extension pool REVERTS to {10, 11}.** Scorer: `SW_SUB`
emptied (prospective-only mechanism retained); s10 carried as a labeled
`out_of_block_confirmation` field; verdict artifact regenerated. **The discrepancy record
STANDS as written: a halt was crossed with execution — the substitution was applied
retroactively to a block whose verdict had already been reviewed (§10.20.6). No fault
assigned; never smoothed.**

**(B) SUBSTITUTION RULE ADOPTED PROSPECTIVELY** — superseding the rescue-only form in (1)
above; grounds recorded: the gate is outcome-blind, and substitution restores the
registered n. **Applies to any block whose verdict has NOT yet been reviewed. First
eligible application = the next block, not sh.**

**(C) GUIDING-LIST ANNOTATED (as ruled):** leg 1 — the cross-scene contrast —
DEMONSTRATED, scope-tagged SHUFFLED FABRIC; leg 2 — the earned-salience curve — re-tagged
**UNPOSABLE-AT-W=1**, re-poses at the visibility/lawful-dynamics rung. Entry stays
**CANDIDATE-HELD**.

**(D) DWELLED BLOCK CLOSED: lottery-at-current-power** (3F/4N combined over 7 reads,
§10.20.6); re-poses at lawful-dynamics.

**(E) HEADLINE (canon):** cross-scene contrast demonstrated on shuffled fabric, 4F/0N,
with out-of-block confirmation at s10 and health-protection at preponderance.

No §10.20.6/§10.20.7 rulings remain open after this amendment.

## §10.21 — EXP13 SCOPING RESOLVED (2026-07-06, checkpoint): four forks ruled + the dose pin; prereg RATIFIED AT CHECKPOINT; frontier → EXP13 build

**The question EXP13 re-asks.** EXP12's regime-bound rider (§10.20/§10.20.1) — "dwell-ordering
buys nothing for routing" — was scoped, by ruling, to a world built WITHOUT physics: an i.i.d.
member draw dressed in a nuisance walk that reverts to a fixed onset pose, so cross-wave order
carried no *logic*. EXP13 gives the world a LAW and re-asks the direct question: **does lawful
cross-wave structure make order load-bearing?** The Guiding-List candidate's leg-2 venue
(earned-salience, re-tagged UNPOSABLE-AT-W=1 at §10.20.7-AMEND) opens here, where W=3 spans time.
Prereg: `docs/EXP13_LAWFUL_DYNAMICS_PREREG.md` (RATIFIED AT CHECKPOINT 2026-07-06; §9.1–.6 ratified
by CC order, §9.7 stage-two surfaces at cal). Assembly of rulings, not new design; NOTHING numeric
transports (proven twice in 12b — every θ/band/N/horizon cut fresh at EXP13's own two-stage cal).

**The learner-not-world doctrine (recorded at Fork 1, carried as the governing line).** The
anti-forward guard lives on the LEARNER, never on the world. v1's illogical world was scaffolding,
not doctrine — a world can have lawful physics without any component acquiring a next-step
objective. The deleted next-wave-prediction term STAYS DELETED; the recorded W>1 guard is passed
STRUCTURALLY by §2's geometry (interior-only masking is two-sided completion, not forecasting), not
by keeping the window at 1. This is the pivot that lets W grow to 3 without re-admitting a forward loss.

**The four forks (ruled), the dose pin, and the wrong-reason class:**
- **Fork 1B — lawful drift + OU residual (the fabric).** The nuisance anchor MOVES:
  constant-velocity drift, velocity drawn per dwell from one fixed family (member-independent),
  dying at the boundary (the throw belongs to the object's appearance — law tied to perception).
  The OU residual RIDES the drift so that **two-sided interpolation strictly beats forward
  extrapolation — sideways-beats-forward BY CONSTRUCTION**: internalizing the law is paid through
  completion geometry, never forecasting. Rejected on record: pure kinematics (world pays
  extrapolation — trap #1 as fabric) and event-grammar (the real destination — a later rung, named).
  Asserts extended: **law-params ⟂ member** (velocity never whispers identity — same coin,
  elephants and mice, now in motion) and the per-lag machinery runs on **RESIDUALS-ABOUT-LAW**;
  k ⟂ member, schedule ⟂ member carry; τ-ordering re-derived against drift scale at stage-one.
- **Clause-1 relocation (recorded, regime-scoped).** "Unpredictable as a sequence" moves from
  within-dwell increments to **LAW-INSTANCE draws across dwells** (params fresh per dwell). The law
  FAMILY is fixed and learnable — clause 3 now carries the load; clause 2 (law-params ⟂ member)
  unchanged and extended. This relocation is *scoped to this regime*: it is what makes order
  carry logic without the world forecasting itself.
- **Fork 2b — symmetric window, interior mask (the completer).** W = 3 sliding window (stride 1);
  masked slots INTERIOR-ONLY, completed from both sides. Terminal-position masking is forward
  prediction in costume — excluded by construction. Windows slide over the RAW stream with no
  boundary alignment (clipping at dwell edges would code the boundary); boundary-crossing windows
  stay in training, honest, and TAGGED. Shortcut-through-trace is now REAL (a mid-dwell mask has a
  same-dwell neighbor in-window) → the banked WINDOW-BLINDED READ goes live as its discriminator.
- **Fork 3C — the law-participation probe + the claim ceiling (the gate).** A read-only
  manipulation check — completion on true windows vs LAW-BROKEN DECOYS (cross-dwell flank-swaps,
  residual-matched) — that MUST fire before any verdict cell is interpretable. No participation →
  cells UNINTERPRETABLE by pre-registration (not dead, not alive — unposed).
- **Named wrong-reason class: MIDPOINT-SHORTCUT** (participation-without-internalization). At
  W=3 / constant-velocity, a neighbor-midpoint solves the interior anchor without internalizing
  anything. Therefore the **CLAIM CEILING is written now**: EXP13 licenses only "order/law
  PARTICIPATES in completion," never "the law family is internalized." Family-internalization
  (generalization probes) is unpayable at this geometry — fenced to a later rung.
- **The dose pin (subtractive curriculum).** Manifest-time floor: lawful-window fraction ≥ 0.75
  (at E[k]=11, W=3, ~82% expected). Breach → raise E[k], recorded, never silent. k=2 dwells
  contribute zero lawful windows (P=0.1), priced in and monitored. Boundary windows are excluded
  from the participation probe by construction, ride as companion columns, and are never verdict
  carriers.
- **Fork 4 — the arm set (parallel blocks, one review each).** CORE: A-LAWFUL vs A-LAWSCRAM
  (identical wave multiset + identical mask schedule, full-stream order-shuffled — the arms differ
  ONLY in whether order carries the law), gated on Fork 3C. 12b TWINS ride along on the lawful
  fabric (does teaching selectivity strengthen where order has logic?). EARNED-SALIENCE leg 2 is
  now mechanically posable (W=3 spans time) — the Guiding-List promotion leg's proper venue,
  expectation-not-gate. Banked (trigger = both-survive): the within-dwell-scramble disambiguation
  arm (attributes law vs dwell-grouping).

**The pre-registered cell table (gate fires first; seeds {0–4}):** lawful-survives / scram-dies →
*order-with-logic is load-bearing — the rider confirmed* (opens dwelled-teaching re-pose +
earned-salience leg 2 as primaries); both-survive → *law participates but is not load-bearing for
routing at these constants* (named finding, rider unconfirmed; the banked disambiguation arm fires);
both-die → world/constants, NOT rider-refutation (thermometer + constants audit); lawful-dies /
scram-survives → ANOMALY (instrument audit, named finding only).

**Future-pointer (canon-explicit, never a training loss here):** forward capability later = reading
the store FORWARD — cued calling-forth (mechanism-map item 3), a downstream use of well-formed
memory. EXP13 builds the well-formed store; it does not forecast.

**Sequence:** checkpoint read → build → cal pre-flight (stage-one incl. τ re-derivation +
participation-probe band → stage-two proposal) → participation-gate ruling → core arms ∥ twins ∥
salience leg → cell read behind verification → one review per block. Nothing verdict-grade runs
before the gate ruling. **Frontier now = EXP13 build.**

### §10.21.1 — RIG BUILT + THE FLANK-INDEPENDENCE FLAG + the pre-registered discriminator (2026-07-06; recorded BEFORE cal)

**Built (`6ec4b94`; canon `7d03d3c`), smoke green end-to-end:** the lawful-drift fabric
(law-params on a NEW dedicated substream, SEED_LAW=90000; residual-about-law recorded per
wave) + the W=3 interior-mask loop (EXP13Loop(EXP12Loop); `_l_jepa` overridden to a hard
zero — the base's within-window pair loop is inert at W=1 but WOULD fire at W=3; the W>1
forward guard is passed structurally). Smoke: per-lag-on-residuals ⟂ member 0.16 < 0.22;
law-params ⟂ member 214 < 278; lawful-window 0.844 > 0.75 (theory 0.818); τ residual
decorrelation at lag-4 = 1/e (matches the τ=4 pin); drift/residual 0.54; interior-only
masking verified; loop.gen parity across arms.

**THE FLAG (surfaced at build, not patched):** a build-diligence probe found the interior
completion FLANK-INDEPENDENT at ≤6k steps — participation gap exactly 0, blinded-read
penalty ~2e-7. Root cause: the operator localizes cells only via `pos_extract` reading the
content-borne drift (the u-carrier was correctly DROPPED — "time is felt, not coded"), and
pre-acquisition the operator substrate is near-collapsed while vision emissions are
near-identical across waves. **Ruled at GO: not patching was right — injecting a position
code to make the gate fire would MANUFACTURE the very participation the gate exists to
measure** (the §10.20-era manufacturing-class line, applied to the instrument itself).

**Pre-registered discriminator (ruled at GO, recorded before any cal number exists):** the
participation-gap-vs-acquisition curve — gap at panel cadence, aligned per seed to the
num-floor onset. BENIGN → the gap OPENS after onset; STRUCTURAL → flat-at-noise through
horizon ON ACQUIRED SEEDS. The distinguishing read is **"acquired AND flat"** — never bare
flatness (pre-acquisition flatness is expected under both readings and licenses nothing).
**Named confound: MIDPOINT-SHORTCUT contaminates the window-blinded read, not the gate**
(flanks→midpoint is cheap where drift is locally linear, even in the benign world) — the
gate's law-breaking decoys are the discriminator; the blinded read is texture; the 2e-7
alarm never rides on the blinded read. **If the gate stays dead on acquired seeds: STOP —
the F3 ruling returns to chat; design space = doctrine-compatible position signal
(content-borne, felt-not-coded) vs W geometry, before any carrier talk.**

### §10.21.2 — STAGE-ONE WALL (2026-07-06, cal {20–24} × both core arms, 160k): **ACQUISITION-CENSORED ON ALL 10 SEEDS — the gate discriminator CANNOT BE READ; stage-two constants CANNOT be cut; STOPPED for the design ruling**

**The letter (pre-registered taxonomy):** all 10 cal runs return onset=None — num_max
1e-6..4.3e-4 vs the 0.01 floor, both arms alike. UNREAD, never a null. The pre-registered
discriminator returns "PRE-ACQUISITION ONLY — licenses nothing" on every seed: neither the
benign nor the structural reading of the flank-flag is licensed, because the "acquired"
half of "acquired AND flat" never arrives. No stage-two constant is derivable (no onsets →
no horizons/θ/W_post; a dead reference without a live one grades nothing).

**The texture (verified numbers, all 10 seeds):** exam_acc = CHANCE (0.482–0.503 over
~14,600 exams per run; exam_lift ~0/negative) — **the visible same-dwell flank word cell is
NOT being copied** (copy would read ~1.0), so the W=3 exam-integrity worry is moot at this
operating point: the completer fails to exploit even the trivial shortcut. mid_vis_err
falls ~10× (1.5 → 0.10–0.22) while **blind_penalty stays ≤1.4e-3 through the full 160k** —
the training loss improves via a FLANK-BLIND path (an unconditional/prior completion),
never via context. Capacity is NOT the gate (d2_depth opens to 2.3–3.0); the assignment
side drifts to collapse (argmax_k 1–3); sep_cat pinned at ~0.47–0.50 throughout. The
FABRIC is healthy: all independence asserts green at full size, lawful-window 0.815–0.817
(capped-theory ~0.817), residual decorrelation lag-4 = the τ=4 pin, drift/residual 0.56.

**CC mechanical diagnosis (texture for the ruling, NOT a canon verdict):** an
operator-architecture × window-geometry interaction. The deployed operator's ONLY
cross-cell addressing is Shepard distance on content-borne position keys; pre-
differentiation those keys are DEGENERATE (same-slot cells indistinguishable — measured:
the masked word cell gathers ~1/3 from EACH of the three vision cells, cross-member at
dwell boundaries, and ~0.0003 from flank word cells). At W=1 the exam context was
single-source full-strength; at W=3 the mix averages the binding signal into a
low-variance mush, the substrate prototypes never differentiate (pa stays uniform), the
completion stays functionally context-constant, and the chicken-and-egg the build flag
named is measured TERMINAL at 160k: the lawful drift IS a content-borne position signal
the operator could in principle feel, but it cannot BOOTSTRAP onto it from the degenerate
start. Both arms identical → not an order effect; this wall sits in front of the rider
question, it does not answer it.

**Standing:** STOPPED per the pre-registered stop. The design ruling returns to chat with
the fenced space — **doctrine-compatible position signal (content-borne, felt-not-coded)
vs W geometry — before any carrier talk.** Nothing verdict-grade ran; the cell table is
untouched; no arm is a fix.

### §10.21.3 — THE WALL AS A NAMED FINDING + PATH B (mixed-W) RULED (2026-07-06)

**NAMED FINDING (canon): W=3 cold-start is acquisition-dead on this operator.** At a pure
W=3 interior-mask geometry the completer never acquires (10/10 cal seeds censored, both
arms; §10.21.2) — not for want of capacity or a healthy fabric, but because of a
**BOOTSTRAP-ORDER fact**: *differentiation requires binding, and cross-wave addressing
requires differentiation.* The operator's only cross-cell channel is Shepard distance on
content-borne position keys; those keys are degenerate until the substrate differentiates;
the substrate differentiates only once a binding signal drives it; and at W=3 the sole
binding context (the masked cell's completion source) is diluted across three
indistinguishable same-slot cells — so the drive never starts. The two requirements are
circular at cold start. This is a property of the operator × window geometry, standing in
FRONT of the rider question, not an answer to it.

**RULED (Jason): Path B — the mixed-W re-pose (§2 amended in place).** The completer
becomes a coin face: per window W=1 (the EXP12 single-source vision↔word completion that
supplies binding and differentiates the substrate — the bootstrap) or W=3 (the interior-
mask two-sided read that consumes differentiation), default 50:50, rate a stage-two
constant. The participation gate and all verdict reads live on W=3 windows exclusively;
acquisition may ride either width. The mixed-W coin breaks the bootstrap circularity by
letting W=1 windows differentiate the substrate first, so the W=3 windows become readable.

**CURRICULUM NOTE (Jason, recorded): this is curriculum's FIRST STRUCTURAL APPEARANCE** —
in its stationary mixed form (a fixed 50:50 coin, no schedule over time). The FULL STAGED
CURRICULUM (non-stationary, W=1-heavy early then widening) stays PARKED as the pre-named
escalation (A): it fires only if Path (B) itself fails to acquire.

**WRONG-REASON CLASS REGISTERED — W1-CRUTCH:** an ACQUIRED seed whose gate stays FLAT on
W=3 windows (instrumented by blind_penalty) learned to complete via the W=1 crutch and
never onto cross-wave context — and THAT outcome licenses the structural reading (the
"acquired AND flat" bar of §10.21.1, now reachable via the bootstrap). Escalation (B fails
to acquire → A developmental widening) pre-named. Verify-list cosmetics ruled: absent-twin
probe words = deliberate (evocation-probe purpose); probe seed-base moved out of the
fabric-key band before cal. Nothing verdict-grade has run; the cell table is untouched.


### §10.21.4 — PATH B STAGE-ONE: acquisition wall PARTIALLY BROKEN, capability wall INTACT — the OPERATOR marginal-collapses at both widths on both arms (2026-07-06, verified 12-agent: 4 lenses + 8 adjudications, every number digit-exact, 2 independent retrains incl. the scrambled arm; NO letter/verdict — stage-one read for the gate ruling)

**Path B moved the num-floor but not the completer.** Cal {20–24} × both core arms at 160k,
mixed-W 50:50. Acquisition (num-floor, 2-consec ≥ 0.01) reproduced digit-exact: **lawful
2/5** {s21 123300, s22 120600}, **lawscram 4/5** {s20 15300, s21 7800, s22 6000, s24 6300},
s23 censored both — vs **0/10 at the pure-W=3 wall**. The W=1 bootstrap DID cross the floor
on some seeds. Asymmetry 13.8× (scram mean onset 8850 vs lawful 121950) = the EXP12
shuffle-fast / order-slow fabric fact, carried.

**But the OPERATOR is a near-CONSTANT MARGINAL map — verified by two independent retrains
(lawful s22 to 130k, scram s22 to 160k), both arms:** controlled category-conditioned
completion gives **category accuracy 0.500 (chance)** at both widths; the completed slot
moves ~1e-4 across inputs spanning 0.1–5.2 in scale (word-token scale 1.08) — a
near-constant function; the output sits at the marginal (scram dist-to-marginal 0.047 vs
dist-to-correct 0.543). The participation gate is therefore FLAT not by a crutch but because
there is **no contextual completion to break**: true_err ≈ decoy_err to 3 decimals,
frac-above-pre-onset-noise 0.0/0.008, blind_penalty negative on every acquired seed.

**W1-CRUTCH does NOT apply (the pre-registered class is retired for this result).** W1-CRUTCH
presupposes the W=1 face completes CONTEXTUALLY (within-wave) and merely fails to transfer to
W=3. The data refute the premise: W=1 is ALSO context-blind (exam_acc_w1 ≈ exam_acc_w3 ≈
chance; W=1 word→vision cross-category shift 1.6e-4). This is a DISTINCT, deeper finding:
**operator marginal-collapse**, order-independent (both arms).

**Framing CORRECTION (verify-driven, recorded): num is OPERATOR-MEDIATED.** `evoke_vision`
(associative) reconstructs vision from the visible word THROUGH the operator, so the num-floor
"acquisition" is the operator's word→vision evocation weakly/transiently crossing 0.01 (s22
median num 0.008 — BELOW floor — with a late transient), NOT a pure vision-cortex read. The
raw vision-emission separability `sep_cat` stays ≈ 0.47–0.50 (undifferentiated) on the lawful
arm throughout; the SCRAM arm's CONTENT does differentiate early and healthily (den peaks
0.72, asg_dist 1.5) yet its operator completion is still marginal — so content differentiation
and operator contextuality are dissociated, and the collapse is on the OPERATOR side.

**INSTRUMENT CAVEAT (recorded, benign): the read schedule couples into the near-floor
trajectory.** A bare `loop.step` training loop diverges from the cal artifacts after ~t=3000
unless the BLOCK-cadence `dc_track` diagnostic read is replicated; dc_track touches no
detectable param / Δ2 / loop.gen yet shifts the near-floor trajectory (within the noise band).
The cal artifacts reproduce EXACTLY only via the faithful runner. Does not affect the
marginal-collapse (holds on clean and read-interleaved trajectories); flagged as a
determinism-contract subtlety (the interleaved reads are part of "order").

**Consequence for the fenced design space.** The wall's earlier axis — "doctrine-compatible
position signal vs W geometry" — is shown to be DOWNSTREAM: with no contextual completion at
ANY width on EITHER fabric, neither a position signal nor a wider window is the operative
lever. The real axis is what pulls the completer OFF the marginal — the contextual-signal
strength / loss regime / operator capacity — or whether this operator can do contextual
completion on this fabric at all. **Stage-two constants are NOT cuttable** (no differentiated
completion regime to calibrate; the gate has no participation to band).

**Standing: STOPPED for the gate ruling + next-move.** The pre-named escalation "(B) fails to
acquire → (A) developmental widening" has an AMBIGUOUS trigger (B weakly acquired the
operator-mediated floor but the completer stayed marginal), and developmental widening is a
W-schedule lever — the wrong axis if the collapse is W-independent (it is). Artifact note: the
mixed-W cal artifacts (`exp13_{lawful,lawscram}_s20-24`, w3_rate + participation_probe +
mixed_w present) SUPERSEDE the pure-W=3 §10.21.2 artifacts at those paths; the pure-W=3 wall
artifacts live at commit 8ffe6f5. Nothing verdict-grade ran; the cell table is untouched; no
arm is a fix.

### §10.21.5 — RATIFIED + THE REFRAME (named hypothesis) + GATE RULED UNPOSABLE-AT-CURRENT-COMPLETER + the retro marginal-map probe (2026-07-06)

**Ratified (Jason):** the draft-flip owned and caught by the pass (the pattern holds);
W1-CRUTCH RETIRED on a refuted premise; escalation (A) developmental widening RETIRED with
it — a W-schedule knob cannot fix a W-INDEPENDENT collapse; num = OPERATOR-MEDIATED evocation
(acquisition is not a content read) recorded; housekeeping (artifact supersession) noted.

**THE REFRAME — entered as a NAMED HYPOTHESIS, not a verdict.** Check the finding against the
ledger before ruling: EXP12's campaign-wide result was **sensitivity-without-conversion** —
assignment alive, exams at floor, everywhere, both arms; 12b showed teaching on CONTENT-side
separability (S_w) while exams sat at chance. **EXP13's gate is the FIRST instrument that
requires contextual COMPLETION; every prior verdict axis lived on the assignment / content
side.** Candidate unification: **operator marginal-collapse is the MECHANISM of
sensitivity-without-conversion** — completion rides the marginal while sensitivity lives
assignment/content-side. The ledger holds ONE existence proof that the operator CAN leave the
marginal: **split s0's late sustained conversions** (§10.20.4).

**GATE RULING: UNPOSABLE-AT-CURRENT-COMPLETER — a PAUSE, not F3-dead.** The wall is UPSTREAM
of EXP13's design; the cell table is untouched; **EXP13 holds** (the lawful-dynamics rig is
faithful — it is the completer that has not yet left the marginal, not the fabric that is
wrong). No F3, because the premise of F3 (the environment cannot represent the target) is not
what failed — the operator does not complete contextually at all, anywhere prior.

**NEXT MOVE — MEASURE, DON'T ARGUE. Trap named: "pull the completer off the marginal" via
LOSS ENGINEERING is MANUFACTURING-CLASS until we know what regime conversion lives in.** So
the move is a READ-ONLY retro probe, on saved/reproduced end-states, NO new training:
- **Retro marginal-map probe** on: (1) the 12b PRESENT twin `exp12_12bc_shp_s23` (num 1.38 —
  the healthiest evocation on record); (2) split s0 PRE- and POST-conversion checkpoints
  (the existence proof); (3) a rig-1 arm. One question: **was the operator marginal there
  too?** (controlled category-conditioned W=1 completion accuracy + output spread = the
  EXP13 probe, applied retrospectively). Determinism note: no `.pt` end-states are saved for
  these runs, so the probe REPRODUCES each committed run deterministically (seed+order+
  threads, exact) and reads the operator read-only — no new regime, no new training.
- **Decision fork:** (a) MARGINAL EVERYWHERE UNTIL CONVERSION → operator marginal-collapse is
  the standing default; the axis is CONVERSION DYNAMICS (dose ladder, horizon — split s0
  converted LATE, and EXP13 cal was 160k vs the 12b dwelled 303k). (b) EXP12 OPERATORS
  CONTEXTUAL → EXP13's regime (lawful drift / mixed-W dilution) broke something specific; the
  axis is the FABRIC. Nothing verdict-grade; the probe decides the axis before any lever.

### §10.21.6 — RETRO MARGINAL-MAP PROBE → FORK (a): the operator marginal-collapse is the PROGRAM-WIDE default; EXP13 revealed it, didn't break it (2026-07-06)

**Obstacle surfaced first (not papered over):** the committed EXP12 runs are NOT reproducible
from current code — no `.pt` end-states were saved, and deterministic reproduction FAILS
because (i) the runs were produced by earlier `exp12_arms.py` versions (CODE DRIFT since the
split/12b/rig-1 commits) and (ii) the runner's interleaved reads couple into the near-floor
trajectory (the §10.21.4 dc_track subtlety, program-wide). A faithful runner-replication still
diverges from committed split_s0 by t≈2100. So the reproduced-state probes cannot CERTIFY the
committed operators. **But the completion question does not need reproduction:** the committed
artifacts' own `exam_acc` columns ARE the operator's word-completion accuracy, recorded at run
time — an authoritative direct read.

**Direct-artifact answer (no reproduction; pooled over all post-onset scheduled exams):**
- **exp12_12bc_shp_s23** (present twin, num_max **1.38** — the healthiest evocation on record):
  operator completion **0.496** over 7,012 exams = **AT CHANCE**. Strong word→vision evocation,
  marginal vision→word completion — sensitivity-without-conversion in a single run.
- **exp12_dwell_s1** (rig-1, num_max **3.87** — the strongest rig-1 evocation): **0.488** over
  12,263 exams = **AT CHANCE**.
- **exp12_split_s0**: **0.530** over 13,746 exams (**7.5 SE** above chance; longest sustained
  run 27 windows > 0.6) = a REAL but SMALL (+3%) departure — the existence proof HOLDS but is
  weak. The reproductions (trajectory-divergent by the obstacle above, yet architecturally
  robust) add that the operator is a near-CONSTANT function (completed-word output spread ~1e-4
  across inputs spanning 0.1–5.2 in scale) — so the chance accuracy is genuine marginal-collapse,
  not a contextual-but-wrong map.

**FORK RESOLVED → (a), and it UNIFIES.** Option (b) is refuted: EXP12 operators are NOT
contextual — they sit at the marginal on completion exactly as EXP13's do, even at the ledger's
strongest evocations (num 1.38, 3.87). So EXP13's lawful-drift / mixed-W regime did NOT break
something specific; **EXP13's gate is simply the FIRST instrument that measured the operator's
completion directly**, and it revealed a program-wide standing default. **This promotes the
reframe from hypothesis toward measured:** operator marginal-collapse IS the mechanism of
sensitivity-without-conversion — assignment/content-side sensitivity is alive (num, asg, S_w),
the completer rides the marginal. The existence proof (split s0, +3% sustained) shows the
operator CAN leave the marginal, but only weakly and rarely across the whole program — so **the
forward axis is CONVERSION DYNAMICS** (what regime lets the completer leave the marginal:
dose / horizon / signal strength), with the standing manufacturing-class trap on loss-engineering.

**Standing:** the answer rests on the committed `exam_acc` columns (authoritative) + the
reproductions (architectural, trajectory-robust). A belt-and-suspenders CERTIFICATION of the
exact committed operator states would require checking out each run's HISTORICAL commit and
reproducing there — offered, not done (the direct reads already answer the fork). Retro probe
artifacts `retro_marginal_*` committed with the reproduction-divergence caveat. Nothing
verdict-grade; EXP13 holds; the gate stays UNPOSABLE-AT-CURRENT-COMPLETER.

### §10.21.7 — RATIFIED (scoped) + HISTORICAL CERTIFICATION DECLINED + STANDING CHECKPOINT CONTRACT + next move = horizon-extension arm (2026-07-06)

**Ratified, WITH A SCOPE TAG (Jason):**
- **MEASURED — `completion-rides-the-marginal`, PROGRAM-WIDE.** The fork resolves to (a) on the
  direct run-time `exam_acc` columns alone (cross-ledger: shp_s23 0.496, dwell_s1 0.488,
  split_s0 0.530). This half is promoted to measured and stands.
- **SUPPORTED-NOT-CERTIFIED — the `near-constant-map` characterization** (output spread ~1e-4).
  It rests on the reproductions, which are trajectory-DIVERGENT (the §10.21.6 obstacle) and
  honestly flagged; architecturally robust but not certified. Held at supported, not measured.
- **Split s0 = the SOLE existence proof of departure** (+3%, 7.5 SE, 27-window sustained) — one
  run, program-wide, that the operator can leave the marginal at all.

**Historical certification — DECLINED (Jason).** No saved `.pt` end-states means it is
*unbuildable*, not merely undone; and the direct reads already answer the fork. The lesson is
retired not by building the probe but by a **standing contract**:

> **CHECKPOINT CONTRACT (binding, all runs from 2026-07-06 forward):** every run saves its
> end-state — `.pt` at the horizon AND at any pre-REGISTERED event (e.g. conversion onset). This
> retro probe was blocked by the absence of exactly this; never again. (See PROJECT_STATE §12.E.)

**Next move — (A) HORIZON-EXTENSION ARM, recommended (Jason); the conversion-dynamics axis, the
cheapest test of "conversion is slow dynamics."** Rationale in-record: split s0 converted LATE
(post-303k-class, under the coin dose) while the EXP13 cal stopped at 160k — so a conversion the
program has seen once may simply live past the horizons run so far. Design in Jason's words, to be
pre-registered before any build:
- Extend **healthy existing-regime runs** — rig-1 / split-class **dwelled** fabric (NOT the
  shuffled control, NOT EXP13's lawful-drift fabric) — to **long horizon**.
- **Seeds across the dose ladder's two LIVE rungs** = **scheduled exams** (rig-1 dwell) and
  **coin exams** (split); the third rung (zero word-prediction load, 12b-(iii)) is STRUCK
  (§10.20.3) and excluded.
- Read with the **density-matched conversion band (the registered form** — §7 EXP13 prereg;
  the naive band ran ~4× hot at halved exam density, so the two rungs' differing exam rates
  MUST be density-matched or the cross-rung conversion read is confounded). **"Now needed for
  real"** = its constant is cut per rung before the verdict read (stage-two discipline).
- **Result cells PRE-NAMED (Jason):** conversions appear ACROSS SEEDS → slow-dynamics confirmed,
  **horizon axis** / **s0-only** → seed lottery, named / **dose-ordered** (coin vs scheduled) →
  **dose axis** promoted.

**Fences carried:** loss-engineering stays **manufacturing-class FENCED** (do not build a loss
term to pull the completer off the marginal until we know what regime conversion lives in).
**EXP13 holds PAUSED** (gate UNPOSABLE-AT-CURRENT-COMPLETER). Knob choices owed to Jason before
build — surfaced in chat, not picked here: horizon length; the seed set; fresh-runs-on-current-code
vs pinned-to-historical-commit (the runs to be extended have no saved end-states, so an "extension"
is a fresh long-horizon run in the same regime under the new checkpoint contract, not a literal
continuation of the committed trajectories); the density-matched band's per-rung constant.

## §10.22 — EXP14 CONVERSION-DYNAMICS SCREEN → **CONVERSION IS REACHABLE** (5 coin seeds); the founding capability is not lost — sensitivity-without-conversion is REGIME-SPECIFIC. 2×2 deconfound GO (2026-07-07)

**THE SHARPEST PROGRAM RESULT TO DATE.** The horizon-extension screen (fork (i), prereg `EXP14_CONVERSION_DYNAMICS_PREREG.md`; build `exp14_arms.py`, one code path proven digit-identical to `run_exp12_arm`) ran fresh seeds {0–7} × {scheduled `exp12_dwell` (dwelled), coin `exp12_split` (shuffled)} @ 500k, checkpoints on. **The operator LEAVES THE MARGINAL** — sustained above-chance word-completion — on the coin rung, across multiple seeds. The founding "operator marginal-collapse" (§10.21.4–.7) is a REGIME-SPECIFIC default, **not a universal incapacity.**

**Verdict (verified, on the re-pinned honest band):**
- **COIN: {0,1,3,6} = 4/8 convert** — each clears a sustained-episode bar; **coin s0 reproduces the sole prior existence proof AND DWARFS it** (63 consecutive windows ≥0.704 vs the committed 16). Plus **cal seed s20 also converted** (36-window ≥0.704 episode) → **5 coin seeds total** show conversion. Far from an s0 lottery.
- **SCHEDULED: 0/8** — all marginal (`frac≥0.5625 ≈ 0.19–0.24` = the exact marginal expectation at ~27 exams/window; mean never leaves chance, even for early-acquirers with ample post-onset room).
- **Cell:** coin 4/8 = the registered **AMBIGUOUS** state ({3,4}); scheduled 0/8 = **none**. Resolved by pin 2: **any-conversion-either-rung fires the 2×2** — the 4+ coin conversions do, so the screen's job is done; the ambiguous COUNT is not load-bearing and no seeds are ground to disambiguate it.

**The draft-flip, caught at the gate (the pattern holding).** The stage-two cal band `0.5625×4` flagged 15/16 "conversions" (scheduled 7/8, coin 8/8) — a FALSE POSITIVE from a too-permissive bar. Caught by a sustain check (scheduled mean stays at chance; "conversions" are 4-window autocorrelated marginal excursions that revert) BEFORE it reached the table, then an adversarial refute-default panel (`wf_9677edf3`, 4 lenses + adjudication, all `read_holds`) **independently re-cut on the honest null and converged on the same {0,1,3,6}.** Root cause: `cut_conv_band` excluded EVERY window ≥0.6 from the null (stripping the marginal's high tail), so `false_rate=0.0` was an artifact and N=4 was cut too low (honest false-rate at 0.5625×4 = **2.9% on coin**).

**BAND RE-PIN (ratified — instrument-validity, same class as the fabric-assert re-pin):** the honest null keeps the FULL post-acquisition marginal (incl. its high tail), excluding ONLY sustained s0-class episodes (`EPISODE_MIN=8` consecutive windows ≥0.704 — half of s0's 16, clear of marginal 2–4 run-lengths). This also caught that **coin cal seed s20 genuinely converted** (a marginal null with a real converter in it is not marginal — its 53 high-tail windows had inflated the panel's full-null p99 to 0.889). Cleaned honest band: **coin 0.6875 × 5** (false-rate 0.0006), **scheduled 0.6111 × 4** (false-rate 0.0004). Verdict IDENTICAL to the panel's contaminated-null 0.704×16 → robust. (`exp14_band_cal.json` re-cut; `_honest_null` in `exp14_arms.py`.)

**STABILITY SUB-FINDING (registered companion, rides into the 2×2):** conversion is reachable but **not always stable** — only **s0 sustains to the horizon** (t≈491700); **s1/s3/s6 convert mid-run** (within-episode mean 0.876–0.916, decisively real) **then DECAY** back toward the marginal before 500k. Conversion definition (2×2 pin): **sustained-EPISODE presence** (EPISODE_MIN form), not endpoint — a seed converts if the episode fires anywhere; **stability logged separately** (endpoint-only would miss the real transient conversions).

**REFRAME UPDATE (ratified, scoped):** the §10.21.5 reframe "operator marginal-collapse = mechanism of sensitivity-without-conversion" was promoted MEASURED program-wide — **now scoped: sensitivity-without-conversion is REGIME-SPECIFIC, not universal.** The completer CAN leave the marginal (verified, 5 coin seeds). **Every conversion the program has ever seen is on the coin/shuffled rung** (s0 originally; now cal-s20 + verdict {0,1,3,6}); never on dwelled/scheduled.

> **[REFINED by §10.24 (2×2 VERDICT): the "coin/shuffled" attribution was the SHUFFLED confound. The 2×2 deconfound shows the gate is the FABRIC (main effect **ON ONSET**), not the coin dose — dwelled+coin (B) is floor-empty, so coin alone enables nothing; dwelled stays in sensitivity-without-conversion at BOTH doses. NB: "fabric main effect" here is **ON ONSET ONLY** — durability by dose within shuffled is a separate, held-OPEN companion (do NOT read this pointer as a global fabric main-effect / do NOT close the durability thread).]**

## §10.23 — EXP14 2×2 DECONFOUND, STAGE-ONE CAL GATE (steps 1→2; **VERDICT WITHHELD**): honest per-cell bands under Rulings A+B; **a cal-grade FABRIC preview with a C>D dose-inversion flag** (2026-07-08)

**Scope.** Prereg `EXP14_2x2_DECONFOUND_PREREG.md`; the 2×2 = {dwelled,shuffled}×{scheduled,coin} = A `exp12_dwell` / B `exp12_12bc_dwp` (NEW) / C `exp12_shuffle` (NEW) / D `exp12_split`. This gate ran **steps 1→2 ONLY** (pre-check + stage-one cal + band cut); the 4-cell scorer (`score_2x2`) is **built but NOT run** — verdict releases from Jason after this read. Cal seeds {20,21,22,24,25} ≠ verdict {0–7}.

**Execution (clean).** Step 1 fabric pre-check (T-independent asserts, T=15k, outcome-blind): **8/8 both new arms, 0 swaps**, verdict {0–7} accepted. Step 2 cal (2 new arms × 5 cal seeds @ 500k, h_max=1M, checkpoints, threads=1): **10/10 clean, no crashes**. **`12bc_dwp` LIVENESS: LIVE — acquires 5/5** (the dose-only cell is readable; the factorial will not be partial; s20 acquires late at 355k, budget 145k>130k). **spec_hash parity OK — single `41d6f0d5e7da`** across all four cells (F2 preserved: constants-payload hash, stable across the reused/fresh diagonal).

**RULING A (Jason 2026-07-08) — the F1 two-pass fixpoint null is DROPPED; revert to the provisional (§10.22 honest-null) cut.** As-built (literal, "implement exactly"), the two-pass ratcheted N to the floor on the *self-thinned* null and **violated α on the true marginal** — honest false-rates (measured on the un-thinned null, the non-circular rate) were **A 0.00132 (1.3×α), C 0.00684 (6.8×), D 0.00379 (3.8×)** while its `false_rate@cut` reported 0.0 (circular). D fired **5/5** cal seeds where only s20 truly converts. The protective scenario F1 guarded (a hidden dampened sub-s0 conversion inflating a band → under-detection) did NOT materialize where it mattered: **B, the dose-only cell, is clean at provisional.** `_twopass_cut` is retained SUPERSEDED (the deflation-mechanism record + the per-cal / between-episode helpers); it is no longer the band method. **Lesson: re-cutting on a self-thinned null degrades the α guarantee — a false-rate must be measured against the marginal that includes its own chance runs.**

**RULING B (Jason 2026-07-08) — a cell whose OWN cal seeds convert has no clean marginal; only C is broken.** A (0/5 s0-class), B (0/5), D (1/5 — the known s20) each self-calibrate on provisional (D keeps its committed **0.6875×5** → **F7's D-reproduces check preserved**). **C_shuffle's cal seeds CONVERT (4/5 s0-class, s24 a 108-window sustained episode)** — no marginal to calibrate. C borrows the density-matched A marginal (both scheduled, exam_n median 27) **iff a borrow-validity gate passes**: A's provisional band must control the false-rate on C's between-episode (non-converting) windows within 2×α. **Gate = SHIFTED** — mean_shift **+0.0203** (A 0.4899 → C-between 0.5102, ~5σ; even C's non-converting s20 sits elevated), and A's band has fr **0.00467** on C's own floor (>2α). So **C uses its OWN between-episode null → 0.64×5** (the Binomial option under-cut, ignoring C's cross-window serial correlation).

**HONEST BANDS (all fr ≤ α; but read the REFERENT column — this is load-bearing):**

| cell | fabric×dose | FINAL band | method | honest fr | **fr referent (SAME α, DIFFERENT null)** |
|---|---|---|---|---|---|
| A_dwell | dwelled×scheduled | 0.6111×4 | provisional §10.22 (=committed) | 0.00044 | clean dwelled marginal → conversion = "leaves the marginal" |
| B_12bc_dwp | dwelled×coin | 0.6667×3 | provisional §10.22 | 0.00061 | clean marginal (B does not convert at cal) → "leaves the marginal" |
| C_shuffle | shuffled×scheduled | **0.64×5** | OWN between-ep (gate SHIFTED) | 0.00091 | **C's own between-ep floor, which CONTAINS the +0.020 shifted baseline — conversion = "leaves C's SHIFTED baseline," NOT the dwelled marginal. Do not read as equal-guarantee to A/B/D.** |
| D_split | shuffled×coin | 0.6875×5 | provisional §10.22 (committed, F7) | 0.00061 | clean marginal (only s20 converts) → "leaves the marginal" |

The referent asymmetry **is** the fabric finding: A/B/D control false-alarms against a genuine chance floor; C's α is relative to an elevated floor. A shared fr column would flatten exactly the distinction the whole C saga hangs on.

**CAL-GRADE FABRIC PREVIEW (verdict WITHHELD — cal seeds {20–25}, behind the adversarial pass at verdict).** s0-class conversions (≥0.704×8) land on the **shuffled row only, dose held fixed**:

| | scheduled | coin |
|---|---|---|
| **dwelled** | A **0/5** | B **0/5** |
| **shuffled** | C **4/5** | D **1/5** |

Two measured effects, both named, both cal-grade: **(1)** shuffled fabric **moves the baseline up +0.020** (the weaker, borrow-gate-SHIFTED finding); **(2)** C fires its own band on **5/5** — conversion *beyond* even the shifted baseline. **GUARD (do not collapse to a tidy "fabric main effect"):** **C > D at cal cuts against the screen's own prior** ("coin converts, scheduled doesn't"). On the shuffled fabric, adding coin dose *reduced* conversion (C 4/5 > D 1/5) — a hint the **dose axis may run backwards on shuffled, or coin×shuffled interact non-additively.** The clean fabric-main-effect reading is ONE hypothesis; the **C>D dose-inversion/interaction** is visible in the same table and is held **open**. The verdict's job is to separate them — canon records both, collapses neither. Screen prior was INTERACTION; this preview neither confirms nor overturns it.

**Held for verdict (Jason's word):** the 2 new arms × {0–7} @ 500k (dwell/split reuse committed screen runs — F7), per-cell conversion (sustained-episode) + stability, then `score_2x2` DRAFT → adversarial refute-default panel → attribution. Nothing verdict-grade run here. Artifacts: `exp14_band_2x2_cal.json` (per-cell band + method + fr referent + borrow-gate + liveness + spec_hash), precheck + cal2 JSONs. Harness: `exp14_arms.py` (CELLS, `precheck_fabric`, `_provisional_cut`/`_between_episode_null`/`_borrow_gate`, `score_2x2` built-not-run, smoke 7/7 incl. borrow-gate unit).

**FORK (i) DISCHARGED → 2×2 GO.** The screen answered "does conversion happen at all beyond s0" = YES, across seeds. dose-ordered (coin»scheduled) stays SCREEN-GRADE (fabric-confounded: coin=shuffled, scheduled=dwelled), license = fire the 2×2 only. **Next: the clean deconfounding 2×2** — {dwelled, shuffled} × {scheduled, coin} — to attribute conversion to **dose, fabric, or their interaction.** Prereg owed for Jason's read before build; conversion = sustained-episode, stability = companion. Loss-engineering stays FENCED; EXP13 holds PAUSED.

> **[REFINED by §10.24 (2×2 VERDICT, 2026-07-09): the screen's dose-ordered "coin converts, scheduled doesn't" was the SHUFFLED CONFOUND — coin rode the shuffled fabric. FABRIC is the gate (main effect ON ONSET; durability held open). "Sensitivity-without-conversion is regime-specific" refines to: the permitting regime is the SHUFFLED FABRIC; dwelled stays in sensitivity-without-conversion at BOTH doses. The founding coin/shuffled observation is not overturned — it is re-attributed from dose to fabric.]**

## §10.24 — EXP14 2×2 DECONFOUND, **VERDICT: FABRIC MAIN EFFECT ON ONSET** (fabric necessary, dose-alone insufficient, dose-inversion refuted). Panel-broken draft; referent-clean core = B↔D + dwelled-emptiness; C corroborates-but-non-loadable; durability held OPEN (2026-07-09)

**Execution.** The 2 new arms × {0–7} @ 500k (h_max 1M, checkpoints, threads=1, faithful runner) ran clean; **dwell/split REUSE the committed screen verdict runs (F7 — not re-run).** All four cells READ 8/8 (no unacquired, no budget-truncation). `score_2x2` produced the DRAFT and halted; an adversarial **refute-default** panel (`wf_1df4cc96`, 6 agents, Pin-2 compliant — any fabric-assuming lens disqualified) broke it; its two load-bearing claims were **independently re-verified** before this write.

**The DRAFT (per-cell honest bands, sustained-episode detector):** A_dwell 0.6111×4 → **0/8**; B_12bc_dwp 0.6667×3 → 5/8 [2,4,5,6,7]; C_shuffle 0.64×5 (own shifted null) → 5/8 [0,2,4,5,6]; D_split 0.6875×5 (committed) → 4/8 **[0,1,3,6]**. Draft fired Pin 3 (C 5>D 4) → OPEN_ATTRIBUTION; draft factorial dose +0.25 / fabric +0.25 / interaction −0.75.

**The panel broke it — verified:**
- **B → REFUTED, 5 → 0 (calibrated false-alarm artifact).** Three decisive grounds, all CC-verified against the committed traces: **(a)** every B "conversion" is longest-episode **exactly 3** (bare N at the loosest band), and across **all 13 B runs** (verdict {0–7} + cal {20,21,22,24,25}) there is **not one episode longer than 3**; **(b)** under B's own honest per-position false-rate (`fr = 0.000613`), EXPECTED phantom-converters = **4.50**, OBSERVED **5** — dead on the null mode (exact **P(X ≥ 5) ≈ 0.51 under the independent-position floor**, deterministic Poisson-binomial; a clustered block bootstrap reads ≈ 0.37 — agrees in kind); **(c)** the same detector fires on **3/5 of B's own cal seeds**, the seeds used to *define* B's null (floor expectation 2.67, observed 3). *Descriptive note — **NON-DIAGNOSTIC**, not a refutation ground: the 5 firing seeds are also the 5 highest post-onset window-count seeds. A genuinely slow conversion predicts the same ranking (more post-onset time = more chance to convert), so exposure-ranking cannot discriminate. Recorded, not relied on.* **The DOSE row is dead: dwelled+coin enables nothing real (A=0, B=0 real).**
- **C → GENUINE but NON-LOADABLE.** C's episodes are real (deep +0.36–0.40 above C's shifted floor, +0.10–0.14 above C's own p99, long 36–90) — clear refute-default. BUT scored on C's **own between-episode SHIFTED null** (band 0.64; borrow-gate SHIFTED, §10.23) → count non-parity vs the A/B/D honest marginal, and **0/5 durable**. C **corroborates** the fabric direction; **C cannot enter a magnitude or interaction contrast.**
- **C>D → REFUTED (Pin 3 CLOSED). The pin WORKED.** Pin 3 held both the tidy-collapse AND the dose-inversion live until a matched-band check could separate them; the check killed the inversion on three counts: (a) the **observed C 5/8 vs D 4/8 gap is a two-proportion z≈0.51 at n=8 = coin-flip** (one seed flips it); (b) at a **matched band the ordering ties-or-inverts** — D ≥ C at every band ≤0.6522 (D 6, C 5 at 0.64), C>D appears only ≥0.6667 and never by more than 1 seed; (c) **durability inverts it** (D 2/4 vs C 0/5). C>D was a **referent-parity artifact** (C at its own 0.64 vs D at the committed 0.6875) — exactly what Pin 3 was written to catch. Trust the machinery: it caught it.
- **D → reproduces {0,1,3,6} EXACTLY. F7 PASS.** The reused committed corner, re-scored at 0.6875×5 through the generalized 4-cell scorer, gives the screen's coin set exactly (A/scheduled 0/8; single spec_hash `41d6f0d5e7da`). **Pipeline validated — this licenses believing the new cells.**

**THE VERDICT — FABRIC MAIN EFFECT ON ONSET (the §5 FABRIC row: D+C convert, A+B silent), on the ENABLING question.** Fabric **necessary**, dose-**alone** insufficient, dose-inversion **refuted**.
- **Referent-clean CORE (does NOT rest on C): B↔D + dwelled-emptiness.** B (dwelled+coin) and D (shuffled+coin) are **both on the honest marginal** — a parity-matched fabric contrast at fixed dose: flip fabric and B is floor-empty while D converts deep+durable+reproduces the screen. Add dwelled-emptiness (A 0/8 scheduled, B floor-empty coin) + shuffled-conversion (C, D real). The pattern is fixed **without C.**
- **Referent SCOPE of the enabling claim:** dose-**general** on the dwelled-empty side — A (scheduled) and B (coin) are BOTH empty, so "dwelled enables nothing" spans both doses — and **referent-cleanest on the B↔D coin diagonal** (both honest marginal). The scheduled-shuffled cell IS C: own-referent, **corroborating-not-loadable**. (Answer, pre-recorded, to "was fabric tested at scheduled on a clean referent?" — no; scheduled-shuffled is C, which cannot carry a magnitude contrast.)
- **C limit (explicit):** real + own-referent (borrow-gate SHIFTED) + direction-corroborating + **magnitude/interaction NON-loadable**. **The fabric call does NOT depend on C.**
- **Factorial is PARTIAL — report the pattern, not the coefficients.** The draft's +.25/+.25/−.75 sit on unrefuted counts (B artifact, C wrong referent) and are meaningless post-refutation.

**BAND LESSON (report-don't-patch — B is NOT re-cut).** An N=3 detector at a 500k horizon carries a per-seed false-conversion probability ~0.56 **even at a correctly-calibrated per-window α** (the sustained-episode-anywhere criterion over the ~1400-window mean post-onset span; the exact 4.50 floor expectation is summed over the actual per-seed window counts). B's honest per-window band did its job; the **crossing-count** read (5/8) was the trap. The **floor-check** (observed vs false-alarm expectation) rescued it. **Carry-forward, cross-experiment: a loose-N cell is verified against its false-alarm EXPECTATION, not its crossing-count.** (See [[feedback_loose_N_false_alarm]] → `docs/feedback_loose_N_false_alarm.md`, which carries the arithmetic, the episodes-not-positions rule, and the selection-forced-zero warning.)

**COMPANION — durability may split by dose within shuffled — HELD OPEN, DO NOT ATTRIBUTE.** Within the shuffled cells, D (coin) 2/4 sustain-to-horizon vs C (scheduled) 0/5. Direction is referent-robust (a stricter band on C only sharpens it) and consistent with the screen (coin s0 was the sole durable sustainer). Reading: **fabric gates ONSET; dose MAY gate DURABILITY.** **NOT POWERED** — durability n is D 2/4 + C 0/5. **Promotion bar (its own gate, disqualification-style like Pin 2):** a *powered durability read* — an experiment designed and seeded to test sustain-to-horizon rate by dose within the shuffled fabric, on a parity-matched referent — must clear before this becomes a claim. Until then it is a NEXT QUESTION, not a finding; a warm restatement a few sessions on does not promote it.

> **[SUPERSEDED IN PART at the EXP15 build gate, 2026-07-10 — the numbers above are a SINGLE-ENDPOINT ARTIFACT. Records stand; this annotates, it does not overwrite.]**
>
> **What died.** The "**D 2/4 sustain vs C 0/5**" table used `sustains_to_horizon = endpoint ≥ band` — **one eval window per seed**. EXP15's ratified re-pin (`mean(last K=10) ≥ band`), built precisely to kill single-endpoint fragility, kills this too: **D 0/4 and C 0/4** (C-s6 DUR-CENSORED). D's two "sustainers" *were* the fragility — D-s0 endpoint **0.9412** but last-10 mean **0.6712** (40% of its final 10 windows clear the ruler); D-s3 endpoint **0.7857**, last-10 mean **0.5729** (30%). CC-verified digit-exact against the committed traces, and independently by an adversarial agent that never saw the diagnostic.
>
> **And it is not rescuable by re-tuning the bar.** Across the committed 16, **0 seeds** sustain under any α-consistent locked-state read; the sustain detector's false rate **exceeds α = 1e-3** on every null pool, and the α-calibrated K=10 bar is **0.79 — *higher* than the ruler**, making sustain rarer still. **FINDING, recorded: LOCKED-STATE SUSTAIN DOES NOT EXIST AT 500k IN THIS REGIME.** Conversion here is **episodic** — committed converters show **2–27 recurring episodes** at the common ruler (median 9; 2–23 at each cell's own band, median 12; 8 of 9 have ≥ 4) — so "held above band at horizon" measures a state the phenomenon does not occupy. That is a fact about the regime, not merely about an instrument.
>
> **What survives — the question, corrected and weaker.** (a) **C decays under every definition tried** (endpoint, last-5, last-10, last-20, α-calibrated). (b) **D's late-run *level* sits higher than C's** — a *disclosed peek*: exact Mann-Whitney on last-10 means, D 0.5967 vs C 0.5100, **p ≈ 0.057** at n = 4 v 4. (c) The screen's **s0** was the sole durable sustainer. So *fabric gates onset; dose MAY gate durability* still stands as a **NEXT QUESTION** — now on a **continuous, episode-appropriate** statistic, not a locked state.
>
> **The promotion bar is unchanged and now precise.** EXP15's re-posed primary: **exact one-sided Mann-Whitney (D > C) on final-quartile time-above-band** — the fraction of windows in (375k, 500k] at or above the common ruler — among eligible converters, **new seeds only** (which quarantines every peek above). See `docs/EXP15_DURABILITY_BY_DOSE_PREREG.md`. **Nothing here promotes the companion; it re-poses the gate.**
>
> **F1 lesson, recurring:** *the re-pin built to kill endpoint fragility revealed that the motivating observation **was** the fragility.* The instrument that was supposed to protect the read deleted the thing being read. Cf. §10.24's B refutation and [[feedback_loose_N_false_alarm]] — a surprising number goes through adversarial verification *before* it becomes a premise, and that applies to the numbers a **verification pass** produces just as much as to a build's.

**Refines / retires (verdict-grade):** (1) screen's "coin converts, scheduled doesn't" → the shuffled confound; **fabric is the gate ON ONSET**. (2) sensitivity-without-conversion → the permitting regime is the **shuffled fabric**; dwelled stays in it at both doses. (3) **Pin 3 → REFUTED** (dose does not invert). (4) **fabric-moves-baseline (+0.0203, §10.23) → STANDS** — it is *why* C requires its own null (borrow-gate SHIFTED) and therefore why C is magnitude-non-loadable. Artifacts: `exp14_2x2_verdict_verdict.json` (draft + stability + Pin-3 check + PARTIAL factorial), panel `wf_1df4cc96`. Loss-engineering FENCED; EXP13 PAUSED.

## §10.25 — EXP15 DURABILITY-BY-DOSE, THE POWERED GATE: **UNDERPOWERED** (per the letter) — no durability claim in EITHER direction; the floor is structurally unreachable for D under this design; the D>C lean weakened at n=28 and is not characterizable; BANKED behind the mechanism campaign (2026-07-10)

**Execution (all gates held).** Prereg + riders committed `6ec2bb9`, harness at its own gate `5e1ff0e` (the EXP14 pattern). The 40 new-seed runs ({8–19}∪{28–35} × C_shuffle/D_split @ 1M, mid-ckpt 500k, threads=1, faithful runner, `.pt` per contract) ran clean — one outcome-blind fabric-assert rejection (s10, both arms) handled by the ruled substitution (s36 failed the then-named 15k screen → **s37**; recorded, `exp15_seed_substitution.json`). DRAFT scored UNDERPOWERED at n=20 (p(D>C)=0.090285, eligible D 6 / C 10) → refute-default panel (`wf_80ee0e95`, no lens assumed D>C) reproduced every load-bearing number → HARD STOP → **Jason's closure rulings (2026-07-10): run the capped top-up per the letter expecting the floor miss (option i); pre-check moves to the deployed horizon (the RE-PIN below); no relabel of the outcome cell.** Top-up: reserve {40–47} pre-checked at T=1M both arms (8/8, no swaps, 15k advisory 16/16 agrees, zero advisory-vs-deployed disagreements; `exp15_topup_precheck.json`) → 16 runs, same contract, 16/16 contract-exact, **zero run-time assert rejections** (the deployed-horizon pre-check guarantees this deterministically) → final score at n=28 (`exp15_durability_exp15_n28.json`; the n=20 draft artifact stands unmodified) → **panel addendum** (`wf_5ec81437`, refute-default, no lens assumed D>C, 4 lenses + synthesis) reproduced every n=28 number from raw records — including a fully independent reimplementation with brute-force enumeration of all C(24,9)=1,307,504 rank subsets for the exact MW.

**THE OUTCOME CELL — UNDERPOWERED, per the letter.** Eligible converters (ruler 0.6875×5, longest-run ≥ 8, runway ≥ 200k; new seeds only): **D 9 / C 15 vs floor 12/cell** (the floor needs BOTH cells). Primary (exact tie-aware one-sided Mann-Whitney on final-quartile time-above-band, (375k,500k], frozen at 500k — the 16 seeds eligible at n=20 carry byte-identical values into n=28): **p(D>C) = 0.096846** (D mean 0.244658, C mean 0.169071; p(C>D) = 0.913141). Ruled annotation (as ratified 2026-07-10 — the direction wording adopts the addendum panel's refute-default label; the provisional "suggestive" was dropped at ratification because the n=28 fill it was waiting on moved the picture): *floor structurally unreachable under this design at feasible n (marginal P(D ≥ 12 | 28 seeds at rate 0.30) ≈ 0.10 at the cap; the audited pre-top-up prediction was the **conditional** P(D reaches ≥ 12 | the 20 observed) = 0.0113 — two framings, named, not to be conflated; observed: D gained 3 of 8, predicted E = 2.4 — the futility call was borne out); direction D>C = **weak unresolved lean** (p = 0.097 at n = 28; weaker than n = 20 on every measure; carried by 2/9 eligibles; new-eligibles-only [top-up increment] contrast mean-reversed) — not characterizable; banked behind the mechanism campaign.* **Panel basis for the adopted label (adjacent, as recorded):** mean gap 0.134→0.076 (−44%); CLES 0.717→0.667; p 0.090285→0.096846; the 8-seed increment itself is mean-REVERSED (new-eligibles-only D 0.099 < C 0.141, p=0.393); the same two pre-top-up carriers s16=0.6587 / s31=0.6058 hold the entire lean — drop them and the order flips (D 0.1339 < C 0.1691, p=0.2907) — while the counter-direction shows nothing at all (p(C>D)=0.913). Gate-variant robustness stands (the registered gate is the most conservative against the lean; every variant NS). No promotion; no refutation; the §10.24 companion neither confirms nor dies here.

**What the reads established (panel-confirmed, both rounds):**
- **The peek-quarantine is correct and conservative.** Including the committed 16 *creates* significance (sensitivity p = 0.009273 at n=20, 0.009641 at n=28 — the sole registered DEFINITION-SENSITIVE flip, visible by construction, and it amplifies exactly the fragile 2-carrier structure: the peeked committed D context contributes 0.8125 and 0.4087) and the registration excludes them; a rule that discards a significant result cannot be manufacturing a favorable one. *(Provenance note, ruled fold at ratification: a circulating figure of 0.008929 for this sensitivity has NO computational source — transcript-traced, it entered as an unverified recollection in a CC scratchpad draft [numerically = 1/112 exactly] and was caught against the artifact before reaching canon; the n=20 panel independently reproduced 0.009273 exactly (U = 110, n = 10 v 14), and no tie convention yields 0.008929 — inclusive-≥ 0.009273, mid-p 0.008520, strict-> 0.007768. The delta had no statistical cause; the fact-check gate was the resolution.)*
- **C's near-zero final-quartile fracs are genuine early-converter decay** — deep 30–88-window episodes that ended before the final quartile. Real durability failure, measured — not padding, not phantoms.
- **Ruling 3's machinery worked, in both directions — and caught the loose-N signature arriving.** The eligible pool is phantom-free at n=28: every eligible converter's longest episode ≥ 19 (D min 21, C min 19), the bare-N shell tops out at 7, and the **empty 8–18 longest-run gap persists**. The [5,10) band is now populated (D s11/s15/s30 at runs 5/6/7; C s13 at 7) — precisely the phantom-shaped converters the gate exists to exclude, and it excluded all four; **raw converter counts must therefore be stated with the run≥8 discount (D 10 / C 17, not 13 / 18).** The floor gate flagged C's count AT-FLOOR at n=20 (12 vs E 9.563, P=0.193 — the count carried no signal) and released it at n=28 (18 vs E 13.374, P=0.05896) — verified rule-genuine (bit-identical null, no denominator change, pure accumulation) but **single-converter fragile**: P(≥17)=0.11843 > 0.10, so losing any one converter restores AT-FLOOR, and the top-up increment alone (6 vs E 3.811, P=0.116) would not clear the rule. Any statement that "C's count is above floor" carries this fragility note; C's converter count still carries little signal. D's count is decisively above floor (13 vs E 5.16, P=0.00065; still P=0.0232 under the run≥8 discount to 10).
- **The gate remains conservative AGAINST D>C.** All looser variants give smaller p (no gate 0.0772; converter+runway 0.0792; converter+longest-run 0.0852; registered 0.0968; all NS) — and the looser variants flatter D partly via the exact recency confound T_DUR exists to remove (D's censored s35 carries frac 0.346 at runway 38.3k, s11 0.139 at 82.7k).
- **Censoring dependency, visible (ROUTED — the 4th decision).** C-45 converted at 309,300 → runway 190,700, censored **9,300 steps = 31 eval windows short of T_DUR** — the tightest boundary case in the experiment (with C-29 6.2k, D-11 82.7k, D-35 38.3k). Its diagnostic-only inclusion is the **largest single mover of the primary** (p 0.096846 → 0.137807) and moves **against** D>C — the registered censoring currently works in the D-direction's favor. The frozen rule was correctly applied and pre-declared (§7.1); no variant flips significance; but this dependency stays visible in any future promotion discussion. (D-11's frac-if-included is a doubly-invalid counterfactual — it also fails the run≥8 gate; the diagnostic reports it only because censoring takes coded precedence.) **Ruled at ratification: the registered rule stands as applied; the diagnostic rides.** And it *independently supports* the adopted direction label — the largest single mover cuts against the lean, which is exactly what "unresolved" means.

**DESIGN-SEAT OWNERSHIP + STANDING RULE (F1-family, instrument-side).** The 12/cell converter floor was ratified BEFORE Ruling 3 added the longest-run ≥ 8 eligibility gate, and the two were never reconciled: the floor priced eligibility at EXP14's converter rate, the gate repriced it at ~0.32 (D eligible 9/28), and the collision surfaced only when the capped top-up was already futile for D (conditional P = 0.0113; ~40 seeds/cell ≈ 80 runs for even odds). The reserve is now consumed in both cells; the floor is unreachable by ruled top-up. Ownership: the design seat. **STANDING RULE: when an eligibility gate changes, every downstream constant that assumed the old eligible rate — floors, caps, reserve sizes, power targets — is re-derived BEFORE GO.**

**PRE-CHECK RE-PIN (STANDING; Ruling 2 of the closure).** Pre-checks run at the **deployed horizon** — the fabric object the run will actually use (T = h_max), decided by the same assert path as the run (`_assert_one` at T = 1M IS the run-time gate; a pass is deterministic across the pre-check/run boundary). The T=15k screen is **advisory only** (recorded, never rejects). Grounds (the s10/s36 instrument finding): the fabric k-independence assert is level-0.01 with per-(seed,T) noisy χ² draws near a T-invariant threshold — s10 PASSES at 15k/100k/500k (χ² 59/47/56) and FAILS only at 1M (92.018 > 89.312, +3.0%; 3-dp values from the deterministic re-run of the gate itself, `_assert_one("exp12_shuffle", 10, 1M)` — the substitution artifact stores 92.02/89.31); s36 is the exact mirror (FAILS 15k at 88.7 > 83.9, PASSES 1M at 61.0). A 15k screen tests a DIFFERENT OBJECT than the deployed fabric. **State the false-alarm expectation with every rejection:** 20 seeds × a level-0.01 assert → E = 0.20 false failures, P(≥1) = 0.182; observed 1 — dead on expectation ([[feedback_loose_N_false_alarm]] turned on the instrument). s10 is NOT s23 (which failed a different test at every horizon and stays out). Thresholds were NOT relaxed. First application: the {40–47} reserve, 8/8 accepted at 1M both arms, 15k advisory 16/16, **zero advisory-vs-deployed disagreements (0/16 — the recorded baseline agreement rate against which future advisory-vs-deployed disagreements are read)**, zero run-time rejections downstream.

**BANKED FORK (trigger required).** Durability-by-dose re-poses ONLY if the mechanism campaign makes durability predictable — a mechanism-level account of what erodes or holds a converted state, such that a durability experiment has a designed effect size instead of a hoped one. Candidate hypothesis, noted for EXP16-successors, not scored here: **C's ~2× exam traffic as post-conversion erosion** (scheduled exams interrogate the converted state roughly twice as often as the coin arm; if each exam event perturbs the converted state, dose-of-interrogation — not dose-of-reinforcement — is the durability variable). A warm restatement does not re-open this; the trigger is the mechanism account. **Pre-pin (ruled at ratification):** any re-pose pre-registers a **censoring-boundary sensitivity — T_DUR ± one window-block, reported-never-deciding** — so a 31-window boundary case (C-45) can never again sit silently load-adjacent; the exact block constant is fixed in the re-pose prereg.

**Known cosmetic issues, reported-not-patched:** (a) the harness attaches C's `null_caveat` string verbatim to D's floor gate (D's own null is far cleaner — 1 episode in 8,095 positions; no numeric consequence); (b) the n=28 `outcome_cell` note reuses the n=20 wording listing reserve {40–47} as the top-up source although that reserve is now consumed (the trailing "floor still unmet after the capped top-up" keeps it accurate). **Disposition (ruled at ratification): both are zero-semantic (prose strings only — no number, no behavior), so the fixes fold into the EXP16 build commit where the harness is already changing, cross-referenced to these notes; if either fix turns out to touch output semantics, it reverts to documented-and-untouched pending its own ruling.**

**Scope fence.** No onset re-litigation — §10.24 stands regardless. No claim beyond durability-by-dose within the shuffled fabric at this power and horizon. The committed 16 remain quarantined context (peeked); the n=20 DRAFT, its panel, the n=28 score, the addendum, the substitution, pre-check, and tail-descriptive records (`exp15_tail_descriptive_n28.json`, descriptive only) are all on disk and commit together with this section.

### §10.25.1 — STANDING RULE (ruled 2026-07-11, at the EXP16 prereg gate): **POSITIVE-DELTA SMOKE** — every new flag's smoke suite includes at least one positive-delta assert that FAILS under a no-op implementation

**Provenance.** The EXP16 prereg panel (`wf_7122fd66`, BD-7) found the registered smoke suite asserted only INVARIANCES (stream bit-identity; existing-arm digit-identity) — a silently no-op `expo_midword` flag (wrong slot test, flipped `is_exam` polarity, spec-key typo) would pass every named assert, leave the new arm digit-identical to `exp12_dwell`, and manufacture a guaranteed 0/8 → a wrong-reason VISION-SIDE MASSING verdict. **This is the wrong-reason taxonomy ([[feedback_manufacturing_the_effect]]) applied to the instrument itself: invariance-only smoke certifies silence.**

**The rule.** A smoke suite for any new flag/arm/policy must contain, alongside its invariance asserts, at least one assert that is TRUE only if the delta is mechanically live — a count that must be nonzero and equal a fabric-derived expectation, a divergence that must appear after the first affected wave, a field that must populate (or must stay empty) precisely because of the delta. If every smoke assert would also pass on a build where the new code path never executes, the suite certifies nothing about the delta. First application: EXP16 §6 asserts (i)–(iv).

### §10.25.2 — STANDING RULES (ruled 2026-07-11, at the EXP16 prereg re-verify): the **pool-second-consumer** rule + **clean panel ≠ sufficient**

**Pool-second-consumer (the §10.25 design-seat rule, generalized).** The EXP15 collision was a floor ratified before the eligibility gate that repriced its input; the EXP16 re-verify hit the same species — EXT_POOL {8,9}, ruled single-consumer (count-ambiguity extension), silently acquired a second consumer (UNREAD-seed substitution), and a bar denominated in that pool's units ("/10") became unrealizable whenever substitution consumed EXT seeds — a whole class of outcome paths left with no reachable route. **The rule: when a shared pool (seeds, budget, a reserve, a check) gains a second consumer, every bar or constant denominated in that pool's units is re-derived — and restated in a pool-invariant unit where one exists — BEFORE GO.** The EXP16 fix restated the "/10" verdict bar as the house *count* (≥ 5, significant at every realized n from 8 to 10), which survives any split of EXT; plus a priority order (substitution first) and a symmetric READ floor (n ≥ 8, so no cell certifies from the n = 7 zone where count and Fisher disagree). Cf. [[feedback_loose_N_false_alarm]] (verify against expectation) and the §10.25 design-seat rule (re-derive on gate change) — one family: *a constant is only as valid as the assumption it was set under; when the assumption moves, the constant is re-derived, not carried.*

**Clean panel ≠ sufficient (standing, promoted from an EXP16 footnote at Jason's word).** An adversarial panel passing — build-gate, prereg, verdict, or re-verify — is **necessary, never sufficient**, to commit or to promote. Commits, canon writes, and pushes each move on Jason's explicit word; a clean panel clears the technical gate, it does not authorize the action. (This is the standing companion to *nothing verdict-grade reaches canon before Jason's read*.)

**Pre-check failure class (standing, ruled at the EXP16 re-verify).** A deployed-horizon pre-check rejection is dispositioned by a **criterion, not a seed list**, so it survives the next experiment without a ruling: **REUSED** = a committed **same-(arm-fabric, seed, h_max)** assert pass already exists → the fresh pre-check is a bit-exact deterministic replay → a failure is a **replay divergence = instrument regression → HALT-AND-AUDIT**, never substitute (`reproduction_check` discipline). **FRESH** = everything else → the **seed-defect class** → read against the stated per-seed false-alarm rate (the §10.25 standing duty), substitute per rule. *"arm-fabric" = the **deployed fabric object** the run trains on (fixed by the fabric flags — shuffled / uniform-mask / word-ref); loop-side reinterpretation flags (expo_word / expo_midword) share their base arm's fabric and do NOT make a distinct arm-fabric. So a committed run of a bit-identical **twin** does not confer REUSED unless it deployed the same object: a shuffled arm's committed run asserts the unshuffled twin but **deploys the shuffled fabric**, a different object.* **The trap it retires (EXP16 AMD-9→AMD-10):** "the seed's fabric was already built here" is *append-faithfulness* (the T-prefix is identical), which is NOT the same property as *horizon-extension stability* (the higher-T assert examines the [T_old, T_new] segment the old assert never saw). A committed 500k pass does NOT make a 1M pre-check a replay — §10.25's own **s10** is precisely a 500k-pass / 1M-fail on the T-dependent k-independence assert (χ² 56 → 92 > 89.3), and the T-dependence is confirmed *in mirror* by **s36** (15k-fail / 1M-pass). REUSED is defined by a same-**horizon** assert; append-faithfulness alone is FRESH. (EXP16: REUSED = verdict {0–7} at h_max 1M; FRESH = cal {20,21,22,24,25} at 500k + EXT {8,9}, whose dwelled fabric object has no committed 1M deployment — only shuffled twins ran at 1M.)

### §10.25.3 — STANDING RULE (ruled 2026-07-11, at the EXP16 G7 halt): **audit constants are re-derived per-experiment against the experiment's own band geometry** — the constant-inheritance rule recurring on the auditing machinery itself

**The instance (EXP16 AMD-13).** The floor-audit (the phantom-crossing check that guards a loose-N count) **inherited EXP15's exclusion constants** — exclude a null episode iff it sustains **≥ 0.6 for ≥ 8 consecutive** windows — into an EXP16 regime whose conversion band is **0.6111 × 4** (bare-N, N = 4). At N = 4 the ≥ 8 exclusion excludes **nothing** (no cal seed has an 8-long run), so the two cal seeds that genuinely convert at the audit band (bare-N length-4 episodes) were left **in** the null they claim to exclude — manufacturing a phantom expectation (4.75) that floored a real count for a fabricated reason. **The §10.25 rule — *a constant is only as valid as the assumption it was set under* — recurred on the AUDITOR:** the machinery that catches inherited-constant errors had itself inherited a constant. The G7 refute-default panel caught it (the auditor needed auditing); it was invisible to five prior review layers because each verified *what exists against its spec*, never *the audit's null against the band it audits*.

**The rule.** Any auditing/exclusion/null-construction constant is **re-derived against the experiment's own band geometry before GO**, never carried from the experiment it was set in; an **inherited exclusion rule is a build-gate check** (does the exclusion band match the audit band?). When a self-matched exclusion carries the mirror risk (self-excluding the very events audited **under-states** the false rate — the EXP14 two-pass laundering, retired in §10.24), **report the bracket** (self-excluded [lower] .. contaminated [upper]) and make a **signature census** — not the floor arithmetic — the decisive discriminator: an isolated bare-N crossing vs a genuine conversion signature (deep: longest run ≥ the s0-class length 8; recurring: ≥ 2 episodes; the C/D reference is 2–27). Companions inherit the **certified** (signature-filtered) read, **never the raw crossing count** (a companion that free-lances raw counts can contradict its own partition — the EXP16 §5 near-miss that would have pointed WORD-SIDE while the honest read is VISION-SIDE).

**Borrow imports N (ruled with it, banked forward — EXP16 ruling 3).** A **borrowed** band imports the lender's N *and its bare-N vulnerability*: EXP16's 0.6111 × 4 arrived via the pre-named NOT-SHIFTED borrow of A_dwell's marginal, and N = 4 (looser than the EXP14 N = 5 converter bands) is the whole source of the bare-N floor problem. The band **stands** — re-cutting N after seeing the result is a bar-move that breaks the baseline comparability the borrow exists to provide (A's committed 0/8). The lesson is **not retroactive**; it banks forward as a build-gate pin: **a borrow pre-names a signature requirement alongside the count**, so the lender's bare-N vulnerability is disarmed before the read, not patched after. Cf. [[feedback_loose_N_false_alarm]] · §10.25.2 (pool-second-consumer) · §10.24 (the two-pass laundering this mirrors) — one family: the constant, the pool, and the auditor are each only as valid as the assumption they were set under.

## §10.26 — EXP16 CAPTURE-FEED DISCRIMINATION: **no word-side capture — VISION-SIDE lean** (UNDERPOWERED by the letter); the reward-drift is caused, but it is not the gate (2026-07-11, ratified after a design-chat verification PASS)

**The question.** Which side of the wave feeds the dwelled-completer capture — the reward/word-target side (H1, word-side capture) or the vision side (H0, vision-side massing)? The arm `exp12_dwell_expomid` **deletes the mid-dwell word-target loss** while holding word *visibility* at 100% and keeping the onset exams — input-side recency maximized, reward-side removed, so a conversion would be unambiguously reward-attributable. Deconfound: exposure waves are gradient- and state-inert (loss skips; stash discarded). Run via the EXP16 corridor (design → pre-flight → verified-result cadence; `docs/CORRIDOR_PROTOCOL.md`), G1→G8, one G7 halt (AMD-13), clean re-run, and an independent design-chat verification pass.

**Verdict (two reads; attribution ratified).** **Formal terminal — UNDERPOWERED by the letter:** raw k = 2/10 converters (s6, s7) at the borrowed band 0.6111 × 4; exact Fisher vs A's committed 0/8 = **p 0.2941** (NS). **Certified read (signature-decisive) — VISION-SIDE MASSING:** both crossings are **bare-N-isolated** (longest episode exactly 4 = N, one episode each), the phantom signature — vs the C/D real-conversion texture (multi-episode, deep, long, 2–27 episodes) — so **certified real conversions = 0**; the other eight seeds show zero episodes anywhere; participation decisively ALIVE; gradient collapsed; 1M tail flat.

**The experiment's yield — TWO mechanism coordinates (the canon result):**
1. **The recency drift is REWARD-caused, not exposure-caused.** Delete the mid-dwell word-loss occasions and the drift dies **at full word visibility** — the gradient collapses to **Δ ≈ 0.025 (verdict-pooled mean) / 0.031 (cal-stage median)** against A's verdict-pooled referent **+0.1416** (a ~5–6× collapse, robust across all four seed-set × aggregation recipes: cal 0.031/0.027, verdict 0.026/0.025). Visibility is not what drives the drift; the reward occasion is.
2. **The shortcut is not the gate.** Drift removed, **content stays unlearned across a doubled horizon** — no seed converts with a real-conversion signature at 500k, and the **1M tail is flat** (zero ≥N runs anywhere in (500k, 1M] across all ten seeds, digit-confirmed): the sparsity confound (X's word-target occasions are ~6× sparser by design, so "enables slowly" was live) is **excluded, not caveated**. Removing the reward-side shortcut did not free the vision-side content learning → the vision side feeds the capture.

**Method-named figures (AMD-2 discipline; a successor must re-derive them).** Participation activity fraction (num ≥ 0.01, post-onset), cal seeds: **median-of-per-seed 0.696** (the ratified §2 bar statistic; 10.7× the X-blind bar 0.065133) / mean-of-per-seed 0.685 / pooled-windows 0.682 — ALIVE under every aggregation. *(Fact-check flag, 2026-07-11: the 0.696 on the terminal surface is **median-of-per-seed**, NOT "pooled windows" — pooled-windows is the distinct 0.682; the label is corrected here, the conclusion unaffected.)* Gradient Δ = p1 − p13-48: **cal-stage median 0.031** (X cal seeds, the surfaced figure) / **verdict-pooled mean 0.0247** (X verdict seeds — the apples-to-apples basis matching A's verdict-pooled referent), both « +0.1416. Floor-audit bracket **[self-excluded 0.00, contaminated 4.748]**, observed 2 — the self-excluded end landing at literally 0.00 is EDGE-5 (over-stripping) made visible, vindicating census-decisive; cal reproduces the same bare-N behavior (s21 [4, 4], s24 [4]).

**Verification-pass record (design chat, PASS).** Every load-bearing number reproduced from the pushed artifacts under an independent detector: converters {6,7} bare-N (length 4, one episode), all other seeds zero episodes, budget gates clear (min 473k), Fisher 0.2941, the bracket, the flat 1M tail. **`spec_hash` single `41d6f0d5e7da` across all 15 X records — and identical to EXP14/15's: the one-code-path claim now spans three experiments.**

**Texture fact (report-don't-attribute; for the campaign, not the verdict).** X acquires **dramatically faster and tighter** than A — acquisition onsets **4.5k–26.4k across all ten seeds** vs A's **14k–300k** spread. Removing the mid-dwell word-loss did not free conversion, but it visibly changed **acquisition dynamics**. Recorded, not attributed.

**Provenance / instrument.** The G7 refute-default panel caught the floor-audit inheriting EXP15's ≥0.6×8 exclusion into EXP16's bare-N (0.6111×4) regime — the §10.25 constant-inheritance rule recurring on the auditing machinery (**§10.25.3**, "the auditor needed auditing"). AMD-13 (prereg): exclusion matched to the audit band, dual-null bracket, signature census decisive, companion inherits the certified read, 1M tail added, band stands. The borrow-imports-N lesson banks forward (§10.25.3). Commit `175e01e` (corridor G8); ratified after the verification pass.

**BANKED (queue behind this verdict):** the **dose-matched discriminator arm** (dead-cell trigger — X's word-target *rate* at mid-dwell recency-satisfiable *placement*, separating dose from placement) and **Fork-next: scene-massing dose-response via dwell-length titration** (the natural next probe of the VISION-SIDE mechanism).

## §10.27 — EXP17 TREMBLE vs SWEEP: **CLOSED 2026-07-12 — ORBIT = DIRECTION-ONLY; per-frame novelty within a persistent identity did NOT convert as tested; no matched-bar excess, no sustained episode (F6-A folded)** (posed 2026-07-11 → closed 2026-07-12)

**CLOSE (Jason ratified, 2026-07-12, touch 3; F6-A folded; supersedes the POSED marker).** The
orbit corridor ran clean G1→G8 (commits `93b22b4` F4-A / `0fb3e4c` build / `e32f005` pre-flight /
`c1a3df5` G8 terminal / this CLOSE). Formal cell: **DIRECTION-ONLY** (unchanged). Attribution reading
(ratified): **per-frame novelty within a persistent identity did NOT convert *as tested*** — a real
sweep (net/path 4.05× tremble, σ>0 and non-degeneracy verified: deployed np11 0.587, driven/undriven
0.307/0.075, zero anchor reflections) produced **no sustained episode** (max run 4 vs a converter
reference ≥36) and **no matched-bar excess** over tremble. The **SWEEP-DEAD cell stays UNCLAIMED**
(raw k≠0). **[Forward-pointer amendment, 2026-07-12 — corrected in place per the forward-pointer
rule (a pointer is operational, not a verdict):** the triggered next arm is **SCATTER-DWELL**
(`MECHANISM_MAP_v1_2_RECONCILED.md` §3 — the bracketing ruling); the ~~banked dwell-length titration
is the triggered next knob (next prereg)~~ **dwell-length titration is repositioned to ride
SCATTER's DEAD branch**. Grounds on the record: the titration-first pointer inherited pre-ladder
language that presumed *interleaving-is-the-gate* — the very attribution this close DECLINED to make;
F6-A made ORBIT-DEAD fully three-way *symmetric* (A self-converts at its own bar exactly as the orbit
does), removing the interleaving presumption and **strengthening the bracketing arm** — scatter
resolves dose+predictability vs interleaving *jointly*, whereas titration only measures the
interleaving dose once scatter has confirmed interleaving is the gate.]** Reading-frame
(`MECHANISM_MAP_v1_2_RECONCILED.md` §2): the "ORBIT-DEAD
three-way-ambiguous" ambiguity **collapses toward orbit ≈ tremble at a common bar** — no matched-bar
signal to attribute to dose or predictability; what remains open is the disambiguation ladder
(SCATTER-DWELL first).

**F6-A — the matched-bar correction (the load-bearing close finding).** The G8 DRAFT's "orbit 5/8
brief crossings *well above* A's 0/8, Fisher p=0.013" was an **UNLIKE-BAR comparison** (orbit at its
detector 0.6129×N3 vs A at A's detector 0.6111×N4 — false rates 0.000964 vs 0.000439, 2.2× apart).
**At a MATCHED bar the excess vanishes** (fresh-code reproduction, both detectors × both arms,
verdict {0–7}, [0,500k)): A-bar 0.6111×4 → orbit 1/8, A 0/8, p=0.50; orbit-bar 0.6129×3 → orbit 5/8,
**A 3/8**, p=0.31. Longest runs orbit [2,4,3,2,2,3,3,3], A [2,2,2,3,2,3,3,2]. The unshifted marginal
survives (Δ0.0011); the "excess over A" does not. **ASYMMETRY FINDING:** A_dwell self-converts
**3/5 at its own committed detector [20,21,24]** (`per_cal_seed_converters`), exactly as the orbit
self-converts 3/5 at its own — so under EXP17's symmetric cal-converts rule A would be non-loadable
too. **DIRECTION-ONLY is a property of low-N band geometry + the rule, not of the orbit.**

**Instrument note (report-don't-patch; EXP14 artifacts untouched).** `exp14_arms.py:743`'s
`false_rate_referent` string is **asserted-in-branch** ("this cell does NOT convert at cal") and is
**contradicted by the same cell's own committed `per_cal_seed_converters`** (A_dwell 3/5 DO convert).
Logged, not patched. Standing rules born this close: **(i) cross-arm companions and context rows must
be MATCHED-BAR — unlike-bar counts are context-only, never evidence; (ii) provenance strings are
COMPUTED from the data they describe, never asserted in a branch** (same family as the
reachable-falsifier rule). **Process fact:** five CLEAN in-corridor panel lenses missed the
bar-matching error (each checked the orbit's numbers against themselves); the outside design-seat
verification pass found it — the two-wall verification (inside panel + outside independent pass) is
exactly why rule (i) exists. Design-seat catch ~~**TEN**~~ **16** (catch-ledger, `progress_log.md`
2026-07-12 — ratified numbering supersedes the "TEN" label in place; never rewritten) = the
unlike-bar comparison.

---

**[HISTORICAL — pre-commit POSED findings, retained below.] Status marker: this section recorded
ratified PRE-COMMIT findings, not a verdict. RB-1/RB-2 ruled 2026-07-11; F4-A 2026-07-12; the CLOSE
above supersedes the POSED status.**

**The question** (the fork EXP16's VISION-SIDE lean opens): shuffling delivers two properties at
once — per-frame NOVELTY and identity-INTERLEAVING. Does conversion require interleaving, or does
novelty within a persistent identity suffice? Arm class: the OU anchor MOVES (kinematics the only
change vs A_dwell; mid-dwell grading kept — EXP16 proved it isn't the gate — so its gradient
becomes an internal control, persistence ≈ +0.1416 expected). The dwell-kinematics forensic
(docs/EXP17_DWELL_KINEMATICS_FORENSIC.{md,json}) quantifies the tremble regime: ~11 near-duplicate
views/dwell, per-step novelty 12% of a random look, net/path 0.079 at k≥13, 5.6% per-axis range.

**FINDING (R1, ratified): a directed LINEAR sweep and wide coverage are jointly impossible in the
±1.5 family box at mean dwell 11.** Pinning §1's anchor-reflection rule on its own words ("moves at
fixed speed v, reflecting") = BILLIARD; under it both faithful sims agree (net/path falls
0.628→0.525 / 0.611→0.515 over v 0.30→0.50) and no v clears the directedness and coverage floors
jointly — 10·v anchor travel folds against the 3.0-wide box while OU jitter (sd 0.125) sets the
path floor. Walls turn fast lines into oscillations. Retired with the finding: (a) the pose-level
unfold argument — a bounce IS partial revisiting in the delivered experience; the FOLDED pose is
the honest statistic; (b) the stalled-anchor model (position-reflect, fixed heading) — violates
"fixed speed v". Method note for the record: the ≥0.8 net/path target and a claimed 0.97-at-v0.4
both traced to an implicit tight-tracking assumption (pose ≈ anchor) that was never computed — at
θ=0.25 (pinned from code, exp12_fabric.py:71-72) the confined pose lags v/θ and cannot follow.
Absolute sim-derived targets were retired for CONTRAST forms (≥ multiples of the MEASURED tremble
baseline) after two validated sims diverged on absolute levels; the real generator adjudicates.

**The re-pose (R2–R7, ratified): ORBITAL anchor, `exp12_dwell_orbit`.** Per dwell from a dedicated
substream: random 2-plane, radius r, angular speed ω, random phase; center = onset pose clipped so
|center|∞ + r + 3·stationary_sd ≤ 1.5 → **zero anchor reflections by construction**. Draw-parity
architecture pinned: the onset g_nuis draw is repurposed as the center source; e1/e2/phase come
only from g_sweep; g_nuis consumption stays byte-identical to A (the single-change invariant now
carries its own positive-delta smoke with a stream-desync falsifier). Selection = minimal r·ω **[superseded — RB-2 amendment below: lexicographic]**
clearing ALL floors (net/path@11 ≥ 4× measured tremble ≈0.58; traverse@11 ≥ 2.5× ≈0.226 — grounds
under RB-1; arc ≥ tremble path 1.636; per-step ≤ confusion bound), pooled AND per-seed-WORST
(MIN floors / MAX ceilings — RB-2 completion), T=100k
seeds {0–7}; (r,ω) frozen; G2 re-verifies at deployed 1M on all 15 fabrics. Feasibility VERIFIED
by sim (r∈[0.85,1.10], ω∈[12°,22°]; region empty on the real fabric → geometry-conflict HALT,
honestly). Census delta from EXP16 (F7, ratified): certification is **DEPTH-decisive** (longest
episode ≥ 8), episode count corroborative only — a conjunctive rule would certify-fake a lone
long-episode sustainer; EXP16's OR-rule let recurrence alone certify; grounds are structural (all
nine committed C/D converters longest ≥36), the s0 example withdrawn (§10.20.1 records five
episodes). Census self-audit added: observed certified count must EXCEED the dual-null ≥SIG_DEPTH
expectation bracket (the AMD-13 logic applied to the census itself; covers the own-band N∈{6,7}
zone). One referent everywhere: band cut, borrow diagnostic, and every null pool on the [0,500k]
column prefix.

**RB-1/RB-2 RULED (Jason, 2026-07-11; marked amendment — the OPEN block above is closed).**
RB-1: the 2.5×-contrast traverse floor is RE-GROUNDED on measured physics (OU-lag caps delivered
traverse ~0.30–0.35 regardless of anchor speed; the 2-plane drives 2 of 4 axes, ~0.38 driven →
~0.24 average); the "teleportation-only" sentence RETIRES as the **eighth design-seat catch**, with
the panel's refutation riding: the absolute form was rejected not as unreachable but as **reachable
only where it's confounded** (the thin feasible band = the maximal-centering corner). RB-2:
selection = **lexicographic** on the pinned grid (r∈[0.85,1.10]×0.05, ω∈[12°,22°]×2°): feasible on
all floors pooled AND per-seed-WORST (MIN floors / MAX ceilings) → maximize clip half-width → tie-break min r·ω; clip-margin
outranks rotation rate because the onset-marginal confound has attribution stakes. Riders: the
onset-marginal delta is a REQUIRED touch-2 read (reported trade, not a fence), and the
**interior-concentration control is pre-named** — SWEEP-CONVERTS triggers a tremble arm at the
sweep arm's realized center distribution BEFORE any paradigm-positive certifies (the EXP16
dose-matched move applied forward). Sim expectation: (0.85, 18°) at clip ±0.275; the real
generator's (r,ω)-freeze decides. Process record: three refute-default panels; both seats caught
and owned errors (design seat: the never-computed 0.97, the s0 recollection, the 0.096 baseline
sketch, the teleportation sentence; CC seat: propagating 0.096 unverified, the stalled-anchor sim);
every correction is marked in the prereg §8/§9, and the three sims ride the commit as the
divergence-and-resolution exhibit. Next: confirmation panel → ratification commit → build →
corridor.

**F4-A RULED (Jason, 2026-07-12; ratification-class — anchor provenance re-base; marked amendment
in the prereg after RB-1/RB-2).** The build landed post-ratification (draw-parity generator delta +
measurer/selector/guarded scorer; 26 adversarial-review findings folded; full suite green), and at
build G2 the F4/R4 digit-exact anchor-assert **FIRED as designed** — no tolerance was minted at any
point. Archaeology from committed artifacts recovered the recipe (contained-dwell set; f64
net/path; f32 radii; **stat3 = LOWER-median**; **stat1 = per-frame pools incl. straddler**): 10/16
per-seed stat2/stat3 values digit-exact; stat1 **bit-exact on all four odd-count seeds**
(single-element medians — frame-set and element identity proven); every residual localizes to an
averaging or summation step of the unported design-chat script. The chat history records that
script's validation as "from-scratch numpy, matched to 6 decimals" — **the anchors were never
ULP-validated; the digit-exact bind as ratified demanded exactness the anchors never had.** Option
1 (recover the script) was dead twice over: unrecoverable (untracked, environment reset) and
structurally incapable (s0/s2 embed mutually inconsistent median conventions on identical pools —
recovery could only pick a side). Amendment: anchors **RE-BASE on the committed measurer's own
outputs as the executable recipe definition** (frozen digit-exact in
`exp08/exp17_anchor_rebase.json`; no tolerance; future measurer drift breaks the bind); forensic
values = documented cross-check with residuals stated; the floor RATIOS stand and the baselines are
re-measured by the committed measurer before selection runs. Incident = **design-seat catch NINE**
(in-session numbers insufficiently externalized), with the standing rider: **an anchor is only as
exact as its provenance — digit-exact binds require committed-code provenance.** Next: lexicographic
(r,ω) selection → pin+freeze → G2 deployed-1M verification → build commit → G1a/G1b → pre-flight
(touch 2).

## §10.28 — SCATTER-DWELL: **CLOSED 2026-07-13 — THE NOVELTY AXIS IS INERT END TO END; ORDERING (NOT CONTENT) MOVES CONVERSION → INTERLEAVING IS THE GATE** (mechanism [PROPOSED]) (posed as the bracketing arm 2026-07-12 → closed 2026-07-13)

**CLOSE (Jason ratified, touch 3, 2026-07-13).** The bracketing arm `exp12_dwell_scatter` (per-frame
uniform-in-ball pose resample at R\*=0.50 — maximal per-frame novelty · zero path · zero predictability ·
identity held) ran the corridor clean G1→G8. Commits: build `24dd0e3` / pre-flight `b443a6e` / G3-G4
`3b9627f` / §3 horizon amendment `ec8121a` / G5-G6 `9b08558` / G8 terminal `ceef0d8` / this CLOSE.

**What is measured.** Across the entire novelty axis — **tremble** (minimal per-frame change), **orbit**
(smooth, directed, predictable), **scatter** (maximal, pathless, unpredictable) — conversion is
**uniformly absent** (certified **0/8** each), and **at matched bars the three arms are
indistinguishable**: scatter / orbit / A_dwell = **2/1/0** (0.6129×4), **2/1/0** (0.6111×4), **6/5/3**
(0.6129×3); all certified 0; max episode **4 / 4 / 3** vs **≥36** for a real converter; **no matched-bar
excess at any common detector**. Not "more novelty is worse," not "less is worse" — **INERT.** Meanwhile
the **shuffled** fabric (`C_shuffle` — the **IDENTICAL wave multiset** as A_dwell, checksum-verified,
merely **reordered**) converts AND certifies **5/8 (62.5%)** with longest episodes 36–90; the pooled
converting-fabric regimes (EXP14 B/C/D) at **58%/seed** (14/24) give **p(scatter certified 0/8) = 0.0009**.
**The variable that moves conversion is ORDERING, not content.**

**What that licenses.** v1.2 §2's three-way ambiguity — **dose / predictability / interleaving** —
**collapses:** scatter maximizes within-dwell dose AND destroys predictability, and **neither moved the
needle.** **INTERLEAVING IS THE GATE.** This is the strongest claim the campaign has earned, and this arm
earned it. The novelty axis (rungs 1–3 of the reality ladder) is closed **NEGATIVE end to end**.

**Where the line holds ([PROPOSED] — do not smuggle the mechanism through the strength of the negative).**
"Interleaving is the gate" is a claim about **this completer under this fabric**. It does **not yet say
WHY** — whether interleaving denies the local-satisfiability shortcut (the mechanism map's prediction) or
does something else. That mechanism claim remains **[PROPOSED]**; the **replay arm** is what tests it
(the dumb uniform buffer, which also measures the effective window and sets CWP's honest bar). The
powered negative earns "interleaving is the gate," not "interleaving is the gate *because* X."

**Corridor texture + rulings.** G4 cal-converts {20,21} → Ruling-B non-loadable → DIRECTION-ONLY formal
(expected). G6 DEAD on the two-axes spine (no surviving matched-bar excess ∧ certified census 0), raw
SECONDARY. **G7 refute-panel** (stats+fact-check CLEAN; f6a MUST-FIX refuted) surfaced ONE judgment-class
— DEAD vs UNDERPOWERED for the raw=2/10 bare-N signature — **ruled DEAD** (F4-A: committed scorer + smoke
sc4 decide DEAD raw-agnostically pre-data, code governs the conflicting §4 prose; raw=2 inside the
floor-audit phantom bracket [0,3.13], so raw≥5 is a floor on noise; EXP16's UNDERPOWERED is a **count-rung**
terminal that does **not transport** to a two-axis regime — nothing transports). The **raw≥5 restriction
STRUCK** (ledger catch 18, catch-15-species raw-gating). **Ledger catch 17:** the terminal's "deader than
the orbit" was an unlike-bar prose gloss (scatter@N4 vs orbit@N3), caught by the **seat pre-panel**
(earlier than §10.27's outside-pass catch) — standing rule reinforced: audit cross-arm PROSE for
bar-matching. Acq-guard PASSED (**capacity exists — re-anchored [catch 19] to the converter arms' sep_cat
max 0.86–0.96 / asg_cat max 0.66–0.95 on the same 608-param cortex, NOT the dead-arm sep_cat 0.4733≈A's
0.4732 which is the undifferentiated floor**; the negative is a real non-conversion, not a confusion-ceiling
artifact). Gradient persisted (0.1112 ≈ A's 0.1416 — valid regime probe). **Ledger catch 19 (CC):** the
acq-guard originally read the undifferentiated-floor sep_cat 0.4733≈0.4732 as "identity recoverable" — but
sep_cat ≈ 0.5 is category-blindness, so the rule proved the OPPOSITE of its claim; re-anchored to the
converter-arm max, conclusion (not capacity-limited) unchanged.

**Pivot fires.** SCATTER-DEAD triggers the **dwell-length titration** (onset-rate is the knob) to measure
the interleaving **dose** (the §10.27 forward-pointer, now realized); then the mechanism-class arms unlock
in order — **replay diagnostic first** (measures the effective window; sets the honest bar), then **CWP vs
the replay bar** (v1.2 §5). Only there does "interleaving is the gate" get its *why*. Standing rules from
this arm: [[feedback_matched_bar_companions]] (prose included), the F4-A code-over-prose precedence, and
calibrate-in-regime (nothing transports). Related: §10.27 (orbit, the smooth end), `MECHANISM_MAP_v1_2_RECONCILED.md`
§2 (ambiguity collapsed), `EXP_SCATTER_TERMINAL_SURFACE.md` (the corridor record).

> **PIVOT SUPERSEDED → REPLAY-FIRST (Jason ratified, 2026-07-13; the paragraph above is preserved, not
> rewritten).** The pivot order (titration → replay → CWP) is superseded: **replay-first.** Grounds: replay
> tests the *why* — §10.28's own firewall names the replay arm as what tests the mechanism — and it is the
> load-bearing question (whether interleaving can be *manufactured* from coherent, dwelled experience, the
> architecture's only path to reality), on which everything downstream waits; titration is cheap and does not
> expire, so it loses nothing riding behind. The replay-first arm is **EXP19 — ORDERING WINDOW (W-PERM)**
> (`EXP19_ORDERING_WINDOW_PREREG.md`, ratified touch-1 2026-07-13): a block-permutation ladder measuring the
> ordering window B\* on the held `exp12_dwell` fabric, with dwell-length titration re-banked behind it
> (RE-PRICED — v1.2 §12.1). Cross-refs: `MECHANISM_MAP_v1_2_RECONCILED.md` §5.3 (SATISFIED, isolated-diagnostic
> rider), `PROJECT_OPS_POSITIONING.md` §3 (U-BUF→W-PERM re-spec).

## §10.29 — EXP19 W-PERM (ordering window): **CLOSED 2026-07-20 — THE ORDERING WINDOW IS BRACKETED: B\* ∈ (128, 512], ON THE RECENCY-FREE STRATUM, STREAM-STABLE** (ratified touch 3; Jason)

**HEADLINE (the stratified bracket — grounds ruled: the claim ceiling's stratum clause + RESCUE-MONOTONE's
own condition + the stable core):** c_strat(B) = 0, 0, 0, **4/8**, 5 across B ∈ {1, 32, 128, 512, T};
**B\* ∈ (128, 512]** (ratified A8 bracket rule; no point estimate), **stream-stable in 200/200 independent
simulator families** (`exp19_stream_stability.json`). Single instrument end to end (floor audit, band 0.64;
per-B widths argmax-cut on each B's own null; per-B underpower gate). Small-B zeros are **arm-truthful on
the PASS-certified instrument** (powercert: C's converters clear at both small-B densities, ≥90% bar).

**Full read, qualified companion:** c_full = 0, 0, 0, 6/8, 5 — **s3 QUALIFIED** (certification = a 0.110
minority-draw event whose stream-marginal tail 4.2e-4 exceeds the law's advertised 2e-4 — ledger 52),
s0 0.860 (modal margin one window); modal family count **5**. The knife-edge pair {0,3} IS the
recency-carried pair (RECENCY-CARRIED fires per-seed on {0,3}); the emphatic four are the stratified core.

**Cross-arm (the matched-bar sentence, tab-governed):** **no evidence-grade excess at any matched bar**
(full @450: 6 v 6, paired-exact 0.6875; @300: 6 v 5, 0.5; stratified: B=T ≥ B512 at every matched bar).

**CELL MAPPING (ratified):** **RESCUE-MONOTONE fires on the stratified primary → U-BUF UNLOCKED, bar =
B\* ∈ (128, 512].**

**THE FIREWALL (verbatim carries in the terminal surface; §1 claim ceiling + §2.4):** W-PERM measures the
window and is **non-causal** — *why* interleaving gates stays **[PROPOSED]**; U-BUF tests realizability and
its bar is B\*. **B4 flag (wherever criterion-3 is stated, never summarized away):** s6 matched-N at the
final op 550: q10 12 vs floor q99 8 (1.5×), `s6_clears_robust: false`.

**§2.4 NON-CAUSALITY, PASTED VERBATIM** *(post-close patch, 2026-07-25 — the seat's post-close
verification pass caught this section carrying §2.4 by citation only, against the prereg's own rule
("carry verbatim, not by citation", `EXP19_ORDERING_WINDOW_PREREG.md:432`); ledger row 54; text =
prereg §2.4, byte-exact)*:

> *"Permuting a window of B requires having already seen all B waves before emitting the first — a B-wave
> lookahead. No agent has that. W-PERM **measures the ordering window B\***; it does **not** show that any
> realizable mechanism can produce it. **U-BUF tests realizability, and its bar is B\*.** A W-PERM positive
> reported as 'a path to reality' is a pre-named overclaim, not a finding."*

**Tail record (descriptive; LATE-RESCUE-IN-TAIL its only cell; B=32 WAIVED with record):** in (500k, 1M]
the two 500k knife-edge seeds become sustained late episodes — B512 s0 run 97 (dec_cat 0.789), s3 run 128
(0.556); B512 s1/s2 + all B128 tails at noise. Enters no bracket, no estimator, no cross-arm sentence.

**D2 CANON LINE:** *Recency is neither necessary (G5a: conversion survives on the zero-preceding stratum)
nor sufficient (EXP16: removing the shortcut does not free content learning) for conversion.*

**LEDGER-52 STANDING AMENDMENT (ratified):** *The floor-audit certification law's advertised tail bound is
computed marginally over simulator streams, not conditionally on the pinned stream. A certification whose
stream-marginal tail exceeds the law's own advertised bound rides QUALIFIED and never enters a headline
count unqualified.*

**ATTRIBUTION (Jason's wording direction, touch 3):** the finding belongs to **the campaign** — the
corridor, its fences, and both chairs; the **s3 qualification to CC's panel**; the catches **as rowed**
(ledgers 37–53). **BANK ORDER:** U-BUF first (the §5.3 rider ruled at its prereg — pre-flagged *[ruled 2026-07-24 → v1.2 §5.3-SAT-2]*) → bracket
refinement (informed by the B=128 tail) → decay follow-on (axis-tracking) → D3/D4. [RE-ANCHORED 2026-07-25 → FRONTIER bench re-anchor: U-BUF = comparator arm]

## §10.30 — BENCH RE-ANCHOR (ratified Jason, 2026-07-25)

The EXP12–20 apparatus — the certified-dead dwelled regime, the in-regime certification law, and the 5.3-SAT-2 arm-scoped entry fence — constitutes the test bench for the founding bet: §5.5's teaching claim ("PAM's convergence error teaches the encoder distinctions it would not acquire autonomously"), maximally testable in a regime certified to not acquire them autonomously. The bench's headline occupant is the evocation-rescue arm (design opens at the seat next; priced at its prereg per §12.1). U-BUF is demoted from "the open fork" to the comparator arm: it prices the ordering channel's causal reachability so an evocation rescue can be dissociated from dumb replay (the 2×2: evocation × replay). U-BUF's original purpose — the bar CWP had to beat — died with CWP at step-0; this re-anchor records the succession explicitly rather than by momentum. Origin: Jason's drift-check, 2026-07-25.

**§10.30 NAMING AND CONTROL AMENDMENT (Jason ratified, 2026-08-04).**
"Evocation-rescue" is retired prospectively as the operational name. The certified-dead baseline already runs with PAM coupling active, so the next bench object is subtractive, not a rescue being added: **PAM-teaching contrast**. The missing comparison is teaching ON versus a structurally verified teaching-OFF control. Historical uses of "evocation-rescue" remain part of the record.

The current bench supplies only the lower-rung contrast against a geometry-only cortex. The full autonomous-objective founding test remains banked per amended §5.5.

## §10.31 — EXP20 U-BUF (causal uniform replay): CLOSED 2026-07-28 — REALIZABILITY ESTABLISHED AT K=128 (ratified touch 3; Jason)

A causal, past-only uniform replay buffer of capacity K=128 rescues certified conversion in the certified-dead dwelled regime — one seed of eight (s2: full 39>7, delivered-stratum 13>10), both reads, stream-emphatic (200/200, tail 0.0, unqualified). RESCUE-FULL-ONLY-K512: 7/8 on the full read (s3: 140>45, the grid-edge episode) — per AMD-1, recency cannot be excluded in-arm at K512; stratified UNDECIDABLE-IN-ARM. K32: 0/8. K=2048 never fired. Comparator status per the bench re-anchor: this prices the replay axis of the evocation × replay 2×2 — the evocation-rescue arm reads against the profile {K32 dead · K128 1/8 both-reads · K512 7/8 full-only}. Row 56 in the open: the first G5 read was refuted in full by the panel (a def-time 500k read_at default truncated every certification; sixth un-transported constant); the fix preserved the default so EXP19 stays byte-anchored, and the corrected read changed decisive outcomes — s2's certification was invisible at 500k. Flags carried, stated not interpreted: the stratified excess is thin at the family extreme (worst single stream's null_max 12 vs observed 13); the powered rise rests on one seed, no other K128 seed within 4 windows on either read; cal display factor (2×, verdict-irrelevant per ledger 42); grid's last ~100 waves unscored by committed behavior. Not claimed: no K↔B equivalence (correspondence companions descriptive); the mechanism WHY stays [PROPOSED]; companions (dec_cat, E-A, correspondence, multiplicity) per the draft, panel-covered. Verification: v2 panel NOT REFUTED zero MUST-FIX from raw; seat recount independent five-for-five including the straddle and the decisive null floor.


## §10.32 — EXP21 PAM-TEACHING CONTRAST: CLOSED 2026-08-06 — SEED-SPLIT; NO CLEAN TEACHING CELL; DIRECT COUPLING NOT VALIDATED (ratified touch 3; Jason)

EXP21 compared the deployed Teaching-ON learner against a structurally verified Teaching-OFF control that blocked both cue-side and target-side L_PAM gradients into vision while leaving PAM present and learning. Eight paired seeds ran from scratch for 1,000,000 waves under a trajectory-inert, vision-only held-out probe.

The frozen cohort route is SEED-SPLIT: {CATEGORY-COLLAPSE-IN-COSTUME 5, NO-EFFECT 3}. Five ON seeds certified category acquisition; zero OFF seeds certified; all eight OFF controls remained broadly viable. Every certifying ON seed failed the pre-registered compression guard. No seed landed TEACHING-ADDED or PRESERVATION-ONLY.

Composition is load-bearing. s2/s4/s7 acquired and retained category while losing distractor/member information and effective rank. s0 fired the rank floor only, with distractor/member accuracy improving, but remained non-selective and low-rank. s5's mid-run acquisition washed out by Q4 and carried negative terminal category advantage. s1/s3/s6 produced no certified category effect. The paired guard companion marks ON-side compression in all eight seeds; this is reported, not promoted into an unregistered cohort route.

Licensed conclusion: the deployed unrestricted L_PAM→vision gradient path did not demonstrate externally useful teaching relative to the viable geometry-only cortex in this regime. No pooled teaching, preservation, stabilisation, or impedance sentence is licensed.

Not claimed: PAM teaching in general is not refuted; the full autonomous-objective founding contrast remains banked; the internal self-easing mechanism is not proven; no slower-reference, pooling-only, residual, or foveated alternative is established.

EXP20/U-BUF retains its closed ordering-realisability result but is no longer the automatic comparator for an evocation×replay continuation. The old 2×2 succession is retired unless a future coupling architecture gives replay a separately ratified role.

Verification: G6 reproduced 16/16 probe series, 8/8 bank rebuilds, the gradient census, all seed routes and the cohort route. The panel returned substance NOT REFUTED. Its one record-level MUST-FIX—the missing G3a/G4 gate-log completion entries—was folded append-only without changing any number, route, or definition. The s3 NaN flag is route-invariant and rides in full.
