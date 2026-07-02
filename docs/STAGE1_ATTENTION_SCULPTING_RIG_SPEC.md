# Stage-1 Attention-Sculpting Rig — CC Implementation Spec

**What this is.** The build spec for the first rig of the attention-sculpting frontier. Design is
closed (see companion `FRONTIER_attention_sculpting.md`, §7 fork resolved → Reading A); this is the
CC bridge. exp03-style: the conflict-validity pre-flight (Step 0) gates the rig; failure conditions
and the words-after open question are pre-registered *here* before any run.

**Status.** `[PROPOSED]` build of a `[PROPOSED]` paradigm mechanism. Extends the Stage-0 Phase-1 core
(`experiments/04_stage0_mvp/`); does not rebuild it. Separate from — and does not touch — the
`[SETTLED]` empty-gap result (PROJECT_STATE §9). **Revised 2026-07-02** under FRONTIER §10.11
(anchored-reference resolution) + the exp06/07 revival configuration; base `517e61c`.

**Goal.** Test whether **the word teaches what to attend to** — whether evocation drives a cortex to
*occupy* the associatively-productive axis rather than the visually-salient one. Deliverable = a
two-timescale response surface (fast redirect + slow convergence) across a word-vs-capacity timing
sweep, not a PASS. Primary signature = occupancy-lag **LIFT**, never gradient-share (§10.11). The
surface is read only on §L-live runs.

---

## `[RECONCILE]` convention

Every value tagged `[RECONCILE]` is set from the **live rig on the run commit** (Step 0 calibration /
validity probe), **not pinned by feel** — exp03 discipline. Round numbers are illustrative. A
consolidated register is in §11.

---

## 0. Scope-lock — what's new, what is Phase-1 unchanged

**New, relative to Phase-1 (exactly six):**
1. Conflict stimulus — unchanged.
2. Constant intrinsic re-pool on Δ2 — unchanged.
3. Timing manipulation Δt_offset — unchanged in mechanism; availability-staging clarified
   (Temporal terms block).
4. Two-timescale readout — unchanged.
5. **Deployed-loop liveness phase (§L)** — calibration + entry gate + continuous channel column.
6. **Δt_assoc kernel arm (§4b)** — piggyback characterization; does not gate the verdict.
The nothing-new guard now covers exactly these six.

**PAM configuration (binding — the exp06/07 revival config, superseding "Phase-1
unchanged"):** completion cue posed via **content-blind cue re-organization** (global
mean-centre form — the validated common-mode remover; structured half shelved, FRONTIER
§10.9); PAM prototype tie = **preserve-style open-and-stay-open two-clock StepSchedule,
ABSOLUTE onsets** (900/3600-pattern; carries the measured scale-growing capacity cost,
accepted on uniformity grounds — FRONTIER §10.8); operator form unchanged
(prototype-resonance, no softmax); **no stop-grad**; **non-causal** masking over the six
cue-shape families; **frozen word anchor** (§10.11 — no relaxation schedule exists in this
rig); one code path. All revival-config knobs `[RECONCILE]`d from the run commit (base:
`ac7ea57` values), never re-typed. The gap-3 gradient path **is** the occupancy drive (§1)
— **not re-implemented**. Its Phase-1 "validated alive" read is scope-narrowed by the exp05
arc: mechanically alive (gradient reaches the masked target) but content-dead in the old
regime (§12.E); §L is what certifies it carries information in this rig.

**Nothing-new guard.** Compute buys stimulus-conflict-strength resolution, timing-offset resolution,
run-length, seed-count. No new operator, no gain sweep, no store. If a change is not one of the six
above, it is out of scope.

### Temporal terms (binding — three distinct notions; do not conflate)
- **Δt_assoc** (short; waves): offset between a word event and its visual event within the
  stream — the associative-proximity kernel (§4b). Primary runs pin Δt_assoc = 0 (same bundle).
- **Δt_offset** (long; developmental): offset between word-content onset and vision capacity
  opening (unpool onset) — words-before / simultaneous / vision-before. The existing sweep,
  unchanged in mechanism. Both cortices are PRESENT from t=0 (§10.11); Δt_offset stages
  *availability*, never component presence.
- **Readout timescales** (within-run): fast redirect vs slow equilibrium — a readout
  distinction inside every cell, not a manipulated axis.

---

## 1. Mechanism under test — Reading A, and the envelope/occupancy decoupling

**Occupancy drive = the existing gap-3 gradient's intra-group disagreement.** Mask a member's vision
slot, PAM evokes it **non-causally** from co-present context, backprop convergence error into the
(still-shared) tied weights. Members associated with the **same** PAM successors get a **consistent**
gradient → no pull-apart → stay merged (inert axis, correctly not occupied). Members associated with
**different** successors get a **contradictory** gradient → pull-apart → occupy the opened capacity
(productive axis, correctly occupied). *Identity:* per-distinction divergence = per-instance
convergence error aggregated across the group's members. No separate divergence computation.

**THE CORE SUBSTRATE CHANGE — decouple envelope from occupancy (do not reuse exp01 re-pool as-is).**
The Stage-0 substrate has two quantities that exp01 **coupled**:
- **λ2 = envelope** (tie strength; the *capacity/ceiling* on resolution). Clock-led; opens (drops) on
  the maturational schedule.
- **Δ2 = occupancy** (member deviation from the mean; *what fills* the opened capacity). Grows under
  gradient pull-apart when λ2 is low.

exp01's re-pool **raised λ2** (re-tightened the tie), which collapsed Δ2 as a side-effect — it moves
*both* at once. **That is envelope re-pool = Tier 2 = DEFERRED** (`FRONTIER` §6b). This rig must
**not** use it. Instead:

- **λ2 (envelope): clock-led, opens on schedule, STAYS OPEN.** No envelope re-pool in this rig.
- **Δ2 (occupancy): grows under the gap-3 gradient (occupy); decays under a NEW constant intrinsic
  re-pool force = a constant decay on Δ2 toward the mean** (§6). Equilibrium = the balance of
  intermittent occupy-pull vs constant decay.

Why this is the right decoupling (and not a detail): λ2 staying open gives the **"seed waiting"**
property — when occupancy decays (Δ2→0) the *room stays open*, so re-occupation is **instant** when
divergence returns (no waiting for the clock to re-open the envelope). That is what makes
words-after *recoverable at the occupancy level* (§5) and what makes the bell→brassy-shape→re-elaborate
cycle work. Building re-pool as a λ2-raise instead would (a) silently introduce the deferred Tier-2
envelope dynamics, (b) re-couple capacity and occupancy — the exact confusion the design pass
untangled. **Constant intrinsic re-pool = Δ2 decay, λ2 untouched. State and assert this.**

**The one line that keeps A from becoming a predictor:** the convergence error must come from
**non-causal** evocation (mask evoked from co-present context, never from predecessors). Causal
masking turns the occupancy gradient into a next-step prediction error → "maintain temporally-
predictive distinctions," a different and wrong objective. Assert non-causal every eval window (the
Phase-1 guard carries forward).

---

## §L. Deployed-loop liveness — calibration, entry gate, continuous channel column
*(gates Step-0(c) and every sweep; the wrong-reason-null protection)*

**Instrument.** The (d)-gate descendant, **read-only on the deployed PAM's evocations**:
associated-different vs associated-same separation (d_diff, d_same) with the
content-ablation guard. No fresh operator; no neutral-task training inside the loop.

**Calibration run (pre-registered, BEFORE the loop run).** The neutral (d)-gate
(`dgate.py`, `335f36d`) at the rig's EXACT configuration — the rig's member cardinality,
re-organized cue, preserve tie, absolute onsets, all knobs `[RECONCILE]`d from the run
commit → **healthy-reference-at-config**. Entry bar = reference − margin (margin
`[RECONCILE]` from calibration seed spread, fixed before any loop run). Output:
`liveness_calibration.json` {reference, spread, margin, bar, config knobs, commit_hash,
spec_hash}. **REVIEW GATE: surface it before the loop run.**

**Why the bar is calibrated, not the canon literal (recorded supersession).** The exp06
direction line reads "must clear the (d)-gate at the *healthy* bar in the deployed loop."
Healthy ≈1.41 is a **clean-config / card-2 reference-category**; under the revival config
at deployed cardinality the converged neutral ceiling is ≈1.0–1.1 (exp07), and the
deployed loop cannot exceed its neutral-probe ceiling — holding 1.41 pre-commits the gate
to fail on RULER grounds, not liveness grounds. Superseded per the §12.C rule (calibrated
on the live commit, never a guessed literal). This paragraph is the record; the
progress_log entry for this revision carries it.

**Entry gate.** Deployed read ≥ bar at run start (post word-association acquisition
onset), ablation guard passing. Below bar → the run does NOT proceed to Step-0(c); a
teaching verdict is never read off a sub-bar channel.

**Continuous channel column.** The deployed (d)-read is logged **every eval window in
every run** (the logged-oracle-column pattern). The channel is expected to be an ADAPTIVE
quantity in the full system — responding to environment and behaviour — so the deliverable
includes its TRAJECTORY and covariates (occupancy, acquisition, Δt_offset cell), not a
scalar pass. Mid-run sag is a logged observable, not a silent kill.

**§10.9 trigger, wired.** Entry bar unreachable at config, or runs stalling with the
channel column collapsing (evocation cannot carry enough signal to teach) → the cue-floor
build-robust Phase-1 RESUMES with the measured reason (FRONTIER §10.9; CC's banked
analysis is the pickup). A trigger-fire, not a teaching null.

---

## Step 0 — conflict-validity pre-flight (gates the rig; runs FIRST; surfaced for review)

The conflict stimulus tests the mechanism **only if** salience and association point in *opposite*
directions. The empty-gap rig failed partly because they didn't (the salient axis *was* the
resolvable one → word redundant). Step 0 proves the conflict exists, on the live commit, before the
timing sweep. Three checks, thresholds `[RECONCILE]`:

- **(a) Salience → distractor.** No-word arm, capacity-open: vision-alone occupies the **distractor**
  axis (Δ2 grows on distractor), **not** the category axis. *If vision-alone already occupies the
  category, the word is redundant — empty-gap repeat; redesign the stimulus.*
- **(b) Category representable.** Substrate oracle (capacity-forced-open + **category**-supervised,
  read-only, nearest-centroid, content-ablation-guarded — same machinery as the sweep's oracle)
  recovers the category axis ≥ threshold. *Else words-can't-teach-unrepresentable (the F3-analog);
  stop.*
- **(c) Conflict confirmed — salience and association pull opposite ways.** Evocation-divergence
  **low** across the distractor axis (PAM evokes the same → associatively inert) **and high** across
  the category axis (PAM evokes different → associatively productive). This is what makes "the word
  redirects occupancy from distractor to category" the right prediction. *If divergence is high on
  the distractor too, the distractor is not inert and there is no clean conflict.*

**Output:** `conflict_validity.json` = {distractor_salience, category_salience, category_oracle (+
ablation), distractor_divergence, category_divergence, derived thresholds, commit_hash, spec_hash}.
The stimulus ladder and the timing sweep are committed **only after** Step 0 passes all three.
**REVIEW GATE:** surface `conflict_validity.json` before any timing-sweep run.

---

## 2. Stimulus — the 4→8 conflict

Four base objects, each splitting into two under increased resolution (4→8). Two orthogonal axes:

- **Distractor axis** — high visual salience, freely splittable by vision alone, **associatively
  inert** (does not co-vary with the word/context). Concretely the "colour" role.
- **Category axis** — lower visual salience (vision won't prioritize it alone), **associatively
  load-bearing** (co-varies with the word). Concretely the "handle/hole" role.

The 4→8 structure must contain **both** "same category / different appearance" (different-distractor,
same-category — the instances the word must pull *together*) **and** "different category / similar
appearance" (same-distractor, different-category — the instances the word must push *apart*). The
word channel emits the **category** label (anchored, from t=0).

**Conflict-strength is a swept axis** (the dense axis, like the sweep's band): how far the
distractor's salience exceeds the category's. Validity-probe-bracketed (Step 0): top = conflict mild
(category nearly as salient as distractor); bottom = conflict severe (distractor dominates, category
barely visible) — bounded below by where the category oracle (b) starts to fail. ≥ N `[RECONCILE]`
dense steps.

---

## 3. Timing manipulation — word-vs-capacity offset

**The variable that leads/lags is two confidence trajectories, not two onsets:** when capacity has
opened enough to *host* the split (a point on the λ2 ramp) vs when PAM's word-association is confident
enough to *evoke differentially* (a learning curve built over repetition). Operationalized as a single
scalar:

- Word channel active and PAM associating **from t=0** (physical co-occurrence is continuous —
  preserves char-7, no train/run split).
- **Unpool-onset delay** `Δt_offset` is the swept knob: the λ2 schedule's onset is delayed relative
  to word-exposure. **Negative = words-before** (association climbs while capacity is still closed →
  confident-when-capacity-opens); **zero = same**; **positive = words-after** (capacity opens and
  vision occupies the distractor before association is confident).

**Instrument, not a pacing finding (binding caveat).** `Δt_offset` is an experimental knob.
Deployment-realism is the **rate-ratio** (association-build-rate vs capacity-open-rate), not a delay.
Do **not** read a timing result as a developmental-pacing claim (same discipline as §12-B's
rate-is-a-locator line). The slow-start unpool ramp (§12-B) stays **pinned off** for this rig.

### §4b. Δt_assoc kernel arm  — piggyback, non-gating.
At the simultaneous Δt_offset cell ONLY, sweep the word event's placement k waves from its
visual event: k ∈ {0, ±1, ±2, …} (`[RECONCILE]`, bounded by PAM's completion window).
Read: association strength / evocation-divergence as f(k). Expectation (logged, not a
gate): peak at k=0, fall-off either side. **Honest scope (pre-registered): the kernel is
WINDOW-BOUNDED by construction** — events outside the completion window cannot associate
at all, so the edges are architecture-set; the informative content is the shape INSIDE the
window (same-bundle vs adjacent-wave). Characterization only; shares no cell with the
primary verdict.

---

## 4. Readout — two timescales

Same two-arm, calibration-independent difference-of-arms discipline as the sweep (intact = word
present + gap-3 active; no-word = matched, word withheld).

- **Fast — first-growth-phase efficiency (reversed lift).** Does the word redirect occupancy from
  distractor to category *before* vision commits to the distractor? Measured as **reversed lift**:
  `distractor_occupancy(intact) < distractor_occupancy(no-word)` — the intact arm *fails to occupy /
  decays* the distractor where the no-word arm occupies it. (Equivalently: `category_occupancy(intact)
  > category_occupancy(no-word)`.) Expected strong at words-before, weak/absent at words-after.
- **Slow — does the cycle provide rate-flexibility.** Does occupancy *eventually* reach the category
  axis and shed the distractor across re-pool/unpool cycles, **regardless of timing**? Requires the
  run to cover **≥1 full distractor occupancy decay/re-grow cycle**. **Run-length pre-registration:**
  size `T_run` so the words-after condition covers ≥1 cycle — run it Phase-1-short and recovery is
  missed and mis-read as permanent failure (the empty-gap run-length finding: cycles ~3× longer than
  first assumed). `[RECONCILE]` from the observed Δ2 decay/re-grow timescale.

---

## 5. The new substrate piece — constant intrinsic re-pool on Δ2

A **constant decay force on Δ2** (member deviations relax toward the pooled mean each step), opposed
by the gap-3 gradient's pull-apart. **λ2 (envelope) is NOT touched — clock-led, stays open** (§1).

- **Pinned slow + fixed + depth-independent for stage-1** (`repool_rate` `[RECONCILE]`, set wide-gap
  vs the occupy/unpool rate so the loop is **safe from oscillation** by construction — the "learn
  quicker than forget" asymmetry).
- **Depth-grading deferred to release** (stage 3): the eventual law is `repool_rate` steeper at leaf
  nodes than root (detail decays before gist — bell→brassy-shape, `FRONTIER` §6). Build-full /
  pin-constant (depth-independent) for stage-1 / release later. No debt — constant is the special case.
- **One code path:** a decay term in the existing pooling update, not a reimplementation. Do **not**
  wire the exp01 disuse-triggered λ2-ramp re-pool (that is Tier-2 envelope re-pool, deferred).

---

## 6. Pre-registration (fix before the run)

### Expected shape
- **Words-before:** reversed lift > 0 (fast) — the word redirects occupancy from distractor to
  category as capacity opens. Strongest at higher conflict-strength (where vision-alone most wants the
  distractor).
- **Words-same:** partial / noisy — the race between association-confidence and distractor-commitment.
- **Occupancy LAGS PAM's word-association acquisition** (the §1 bootstrap signature — occupancy driven
  by association, not by vision splitting alone). Verify the ordering.

### Words-after — STRUCTURED OPEN QUESTION, not a prediction
*(Confident in the paradigm; unsure of the architecture's behaviour. Leave open.)*
- **Soft prior (not a gate):** words-after recovers at the **occupancy** level (the cycle cleans up
  and covers over) but **scars at the envelope level** — no envelope re-pool in this rig (Tier 2
  deferred), so the first allocation persists; the cycle redirects occupancy *within the branch the
  first impression opened* but cannot reclaim/reallocate it.
- **The measurement:** the **asymptotic words-before vs words-after gap** (after both have cycled
  fully) = the **envelope-level scar** = a lower bound on what envelope re-pool (Tier 2) would recover.
  *A deferral paying rent:* small gap → Tier 2 minor, deferral cheap; large gap → Tier 2 doing real
  work, re-entry trigger fires sooner.
- **Genuinely open:** scar magnitude. Full recovery → "first impressions last" was wrong, the
  occupancy cycle is stronger than expected (a finding). Heavy scar → Tier 2 earns priority. **Do not
  pre-commit to either; report the asymptotic gap as the result.**

### Failure / boundary conditions
- **No conflict (Step 0 fails (a) or (c)):** stop — stimulus invalid, not a result.
- **Category unrepresentable (Step 0 (b) fails at a conflict cell):** that cell is the cap (F3-analog);
  drop it, never count as a clean redirect.
- **Flat reversed lift at all timing offsets, conflict valid:** the occupancy drive is too weak to
  redirect even with the word's opening — the gap-3 gradient is genuinely inert (the deep negative,
  `FRONTIER` §7 reading-(ii) gaining weight). A real possible result; report it, do not rescue.
- **Oscillation (stage-1 dynamics):** does an intermittently-productive distinction find a **stable
  Δ2 depth**, or **hunt**? Pre-register stable-depth-vs-oscillation (`FRONTIER` §7). Oscillation →
  the rate gap is too small; widen and re-run (stage-2 is the characterisation).

**Bars-amendment convention (binding).** A pre-registered bar may be superseded after
results ONLY on recorded reference-error grounds — the bar measured the wrong quantity —
with the record stating what it should have measured. Never silently; never because a
result missed it.

**Added failure/boundary condition — entry-liveness fail.** Calibration bar unreachable at
config, or deployed read < bar at run start: NOT a teaching null (§L exists to prevent
that wrong-reason read); fires the §10.9 trigger assessment. The real negative remains:
flat reversed lift at all Δt_offset cells, conflict valid (Step-0), AND channel live (§L
column above bar throughout) → the gap-3 drive is genuinely inert; report, do not rescue.

---

## 7. Controls

**Pretrained-PAM — learning-vs-gradient disambiguator (run only if the online result is ambiguous).**
If occupancy lags, is it because PAM hasn't *learned* the association, or because the *gradient* is
weak? Enter PAM with the word-association already confident → any remaining lag is the gradient's
doing. The analog of the oracle's forced-open/read-only trick. **The one admissible train/run split —
as an isolation control only, not the deployed mechanism** (exp02 logic: testing a property ≠
adopting it; char-7 preserved in the deployed rig).

---

## 8. Build path (three stages; pin/sweep/release)

1. **Fixed wide ratio, depth-independent, slow constant Δ2-decay.** Get the equilibrium-with-PAM-occupy
   **stable at all**, on the conflict stimulus, across the timing offsets. Pre-register stable-depth-
   vs-oscillation. Deliverable: the two-timescale surface (reversed-lift vs timing × conflict-strength;
   asymptotic words-before/after gap).
2. **Sweep the rate ratio inward** (occupy vs decay); characterise where it oscillates — the response
   surface (as the unpool-clock rate was handled).
3. **Release depth-grading** on `repool_rate`, using the surface as the reference for the force law.

Two cortices, **no store**. Stays Stage-0-shaped in components.

**Gate sequence (pinned):** (1) §L calibration → bar; (2) Step-0 (a)/(b) RE-CONFIRMED on
the run commit (the old PASS predates the revival config); (3) deployed entry gate ≥ bar;
(4) Step-0 (c); (5) commit stimulus ladder + both sweeps; (6) runs. Review gates at (1)
and (4).

---

## 9. Guardrails

- **G1 (no access-gate / wrong-reason):** Step 0 proves the category is *representable* (oracle) — the
  word *redirects* occupancy, it does not supply a representability vision lacks. No stop-grad.
- **G2 (non-causal):** masking non-causal every window, or the occupancy gradient becomes a predictor
  (§1). The single most load-bearing guard.
- **G3 (envelope ≠ occupancy):** constant re-pool acts on **Δ2 only**; λ2 clock-led and open; the
  exp01 λ2-ramp re-pool (= Tier-2 envelope) stays unused/deferred (§1, §5).
- **G4 (efficiency emergent):** the Δ2 decay is a constant substrate force, not a target; no
  "minimise weights / compact strong concepts" objective (HANDOFF drift-vector 5).
- **G5 (timing = instrument):** `Δt_offset` is an experimental knob, not a pacing finding; §12-B ramp
  pinned off (§3).

---

## 10. Parameter block & `[RECONCILE]` register

### Pinned (structural)
| parameter | value |
|---|---|
| Stimulus | 4→8 conflict (distractor + category axes); word emits category label, anchored |
| Axes | conflict-strength (dense) × timing-offset; asymmetric, not a grid |
| Timing offsets | ≥3 (words-before / same / after); continuous `Δt_offset` |
| Constant re-pool | decay on **Δ2** (occupancy); λ2 (envelope) untouched, clock-led, open |
| Rate asymmetry | re-pool slow vs occupy/unpool (wide gap, oscillation-safe) |
| Operator / masking / anchor | Phase-1 unchanged; non-causal asserted; no stop-grad; one code path |
| Every row carries | `commit_hash`, `spec_hash` |

### `[RECONCILE]` (calibrate from the live rig)
| value | source |
|---|---|
| Step-0 thresholds: distractor-salience, category-oracle floor, distractor/category divergence | Step 0 conflict-validity |
| conflict-strength ladder endpoints + step count | validity probe (top = mild; bottom ≈ category-oracle failure) |
| `Δt_offset` range/steps | rig (span words-before → words-after) |
| `repool_rate` (constant Δ2 decay, slow) | rig (wide gap vs occupy rate; oscillation-safe) |
| `T_run` | ≥1 full distractor decay/re-grow cycle (esp. words-after); from observed Δ2 timescale |
| seed count | ≥ the frequency floor (Phase-1's 3 was too few; ≥20-style) |
| §L reference / margin / bar | §L calibration (neutral (d)-gate at rig config) |
| channel-column eval cadence | rig (every eval window) |
| Δt_assoc k-range | PAM completion window (§4b) |
| revival-config knobs — cue re-org form, tie onsets | run commit (base `ac7ea57`) |

---

## 11. The line to hold

The word does not improve acuity — it teaches what is worth distinguishing. This rig tests whether
evocation redirects a cortex's occupancy from the salient axis to the associatively-productive one;
envelope stays open (Tier-2 deferred), occupancy is the battleground, non-causal masking keeps the
drive associative not predictive, and the words-after scar measures the deferred mechanism's worth.
