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
= {cue-diffuseness, PAM pool-penalty}**. **Member-count is tolerated-deployed — a ~22% degrader, NOT a
killer** (manyOnly plateaus d≈1.11 vs clean 1.42, comfortably above the live bar); the **3-way
irreducible-conjunction alternative is rejected** at convergence. The penalty/diffuseness **kill-texture
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
