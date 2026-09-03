# Handoff — How to Work on This Project

**What this is.** The procedural document for the associative-memory project (Weft / PAM
lineage). It says *how to work*, not *what's been decided* — that's the companion,
`PROJECT_STATE_AND_MVP.md`. Read this first, that second.

---

## The one thing that matters most

The recurring failure mode of this project (≈10 prior restarts) is **drift from the
paradigm into familiar ML machinery** — most often a forward-in-time / next-window
predictor — which quietly substitutes a conventional system for the novel one. Every
discipline below exists to prevent that one thing.

Familiarity is the drift vector. The more productive a familiar technique looks, the more
scrutiny before adopting it. Long elaboration that feels like progress is itself a drift
risk.

---

## What changed about the discipline (read carefully)

The project has moved through three stages, and the discipline shifts at each:

- **Stage 1 — pure paradigm.** Drift looked like "jump to architecture." Discipline: stay at
  paradigm, refuse mechanism.
- **Stage 2 — first mechanism commitments** (pooling substrate, PAM as the masked-completion
  operation, the encode/decode codec). Drift stopped looking like picking an architecture and
  started looking like **forward-prediction re-entering through the *details* of the chosen
  mechanism** — masking scheme (causal vs non-causal), tracing (stepped vs whole-surfaced),
  recall (generate-next vs complete-whole), the temptation to bolt a planner onto tracing.
- **Stage 3 (current) — first mechanisms validated in isolation; now at the integration
  frontier** (the Stage-0 MVP). Two standalone bets are tested and green (pooling substrate,
  non-causal masked completion). The remaining load-bearing claims (gap-3 fusion,
  order-as-content in a latent, confidence-as-currency, the recall loop) are **not**
  isolation-testable — they only appear in the loop. So drift now *also* hides in
  **integration**: an MVP that "works" by quietly violating a characteristic (a fixed-capacity
  v0; a shared-space fusion that never exercises char 10) teaches nothing about whether the
  real design works. Watch for the loop succeeding for the wrong reason.

The through-line across all three: **test the mechanism's *realisation* against the paradigm's
*functions*, not its vocabulary.** A JEPA encoder is sanctioned; a JEPA *predictor becoming the
association operation* is the drift. Same words, opposite outcomes.

---

## Live drift vectors (specific to current state)

1. **Causal masking.** PAM learns by *non-causal* masked completion (predict an interior
   span from *both* sides). The instant masking becomes causal (past-predicts-future),
   PAM is a forward predictor wearing a mask. Hold this line explicitly. *(Exp02 showed this
   directly: the causal control fails end-cues-beginning by construction — 0.062 vs 1.000.
   The random-access sweep plot is the standing anti-drift artifact; point at it when forward
   prediction tempts its way back.)*
2. **Stepped recall.** Within a stored span, material is surfaced *whole* (sideways,
   random-access). Only *across* spans is there a trace, and that trace is the
   already-accepted confidence-gated char-4 mechanism. "Generate each step from the last"
   is the drift. **Within = whole; across = trace.**
3. **Planner-bolt.** When confidence-gated tracing hits its reach ceiling, the temptation
   is to add a value/planner model to push past it (this is what Dreamer does, and the
   mechanism map names it as the canonical silent architecture swap). Reach grows because
   *the space is better-shaped* (familiarity shrinks per-step error), **not** because a
   planner is added.
4. **Separate store as overseer.** The store feeds PAM but is *passive*; PAM associates,
   the store does not. "A predictor that sees over a stored sequence" is the rejected
   framing-1. The store holds *past bundles* (perception-derived), never PAM's own
   outputs.
5. **Efficiency as objective.** Efficiency must stay *emergent* (a consequence of local
   re-pool). The moment "minimise weights / be efficient" becomes a global target, a
   global loss is back — which violates the no-external-objective commitment.

---

## Working principles (these are load-bearing, treat as near-canon)

**Reference-and-relaxation.** No plastic component without a slower-changing reference to
converge against; the reference is itself on a relaxation schedule — stiff early when the
system is chaotic, loosening as the rough configuration settles. Co-development loops
without a stable reference do not converge. Recurs everywhere (parent→encoder, fixed
wave→convergence, cortex-spaces→PAM). Jason has independently re-derived this across
multiple sessions — that recurrence is the signal it's load-bearing.

**Build-full / pin-to-constant / release** (the implementation face of the above). Build
the developmental mechanism in full, pin its variable part to a constant for v1, release
later. Appears at least three times (the activity-gate pinned to 1; the relaxation
schedule generally; what was the "frozen router" before it dissolved). This is how you get
the principled version on paper and the predictable version in the first run — *no debt*,
because the simple case is a special case of the real one, not a stand-in to rip out.

**Provisional before canon.** New resolutions are held as `[PROPOSED]` bets and sit before
promotion. The next session may challenge them and must **not** inherit them as settled.
Mark this-session bets clearly.

**Test against functions, not vocabulary.** A candidate mechanism is a good fit only if it
satisfies the *behaviour*, not if it shares a name with the system.

**Confidence is the universal currency.** Credit-assignment, trace-halt, the pooling
trigger, hop-looseness, vividness, and segmentation are all *one* signal (inverse
prediction error) wearing different hats. When a new mechanism needs a control signal,
check whether confidence already supplies it before adding a knob.

**Isolate and pre-register.** Where a mechanism's success criterion is *local* (doesn't depend
on the rest of the loop), test it standalone before integrating — and write the **failure
condition first**. An isolation test with no pre-registered failure becomes a demo that always
"works." This has earned its keep: exp01's rig caught a validity bug in its own spec (a leaky
readout) *because* the failure condition was explicit, before it could produce a false pass.
Mechanisms whose criterion is only meaningful *in the loop* (fusion, confidence, recall) are
integration tests, not isolation tests — don't fake a standalone version.

**Testing a property of a mechanism ≠ adopting it.** Using a transformer (or any familiar
architecture) in an *isolation rig to test a property of it* is not drift — it is not being
built into the system. Adoption is when the mechanism becomes load-bearing in the
architecture. Keep the two separate: exp02 used a tiny transformer to *demonstrate* that
non-causal beats causal for random-access recall; that does **not** put a transformer in PAM.
Expect this to recur (trigger words like "transformer"/"attention" will flag during builds) —
the question is always *adopting* vs *testing a property of*.

---

## Tone / process preferences

- **Concise, load-bearing outputs.** Trim scope. Short labeled moves over elaborated
  analysis. Claude's fluency and length are themselves flagged drift vectors — long
  elaboration that feels like progress often is drift.
- **Correct compressions.** When Claude's elaboration compresses or drifts from the
  original vision, say so. Jason values the correction.
- **One question at a time** at decision forks; surface the fork, recommend, then stop for
  the read.

---

## How to use the companion docs

The docs are **three tiers by lifespan** — keep them in their lanes:
- **This doc (`HANDOFF.md`)** — *how to work*. Stable; rarely changes.
- **`PROJECT_STATE_AND_MVP.md`** — *what's true now*. Full architecture, every decision,
  status (settled / proposed / deferred), open gaps, and the suggested MVP. **The base for the
  MVP build chat** — §9 is the validation status, §10 the open blockers, §11 the MVP; those
  are the live frontier. Rewritten as decisions move; keeps no history.
- **`progress_log.md`** — *what happened when*. Append-only; the trail behind the state doc.

**The rule:** a *decision* edits the state doc; an *event* (experiment run, fork resolved,
thing learned) appends to the log. Most sessions touch both.

Reference docs (don't edit lightly):
- `substrate_description.md` — the detailed pooling-substrate spec (summarised into state §4).
- `association_cortex_operation_spec.md` — the twelve characteristics. **Stable. Do not
  re-litigate.** Its open-questions framing predates the current architecture; the state doc
  supersedes it.
- The **mechanism map** (latest version) — a map of the *possibility space*, not a design.
  Trust its tension map and `[CONFIRMED]` items; treat its *recommendations* and staged build
  with caution (they lean conservative — they trade away the novel part, drift, first).

**Implementation lives in the repo, not the chat.** Design happens in chat; Claude Code (CC)
implements in `github.com/EridosAI/Loom`; the docs are the bridge. The validated build-time
constraints from the experiments — re-pool trigger = force magnitude; adaptive-λ scales with
signal strength; PAM's loss must sample the full cue-shape distribution; readouts
distance/similarity-based — live in state doc §9; carry them into any build. **Doc-sync
caveat:** commit refs and the README layout recorded in the docs come from CC's reports and are
unverified against the actual repo — reconcile them in CC's next pass so docs and code stay in
step.
