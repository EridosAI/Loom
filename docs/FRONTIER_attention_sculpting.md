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
