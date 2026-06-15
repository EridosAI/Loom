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

The project has now crossed from *pure paradigm* into *first mechanism commitments* (the
pooling substrate, PAM-as-JEPA, the encode/decode codec). This **changes where drift
enters**:

- **Before:** drift looked like "stop staying at paradigm level, jump to architecture."
  The discipline was "stay at paradigm, refuse mechanism."
- **Now:** the mechanism is partly chosen. Drift no longer looks like picking an
  architecture — it looks like **forward-prediction re-entering through the *details* of
  the chosen mechanism.** Specifically through: masking scheme (causal vs non-causal),
  tracing (stepped vs whole-surfaced), recall (generate-next vs complete-whole), and the
  temptation to bolt a planner onto tracing to extend reach.

So the new discipline is: **the mechanism is committed; keep testing that its
*realisation* still serves the paradigm's functions.** Test against *functions*, not
vocabulary. A JEPA encoder is sanctioned; a JEPA *predictor becoming the association
operation* is the drift. Same words, opposite outcomes.

---

## Live drift vectors (specific to current state)

1. **Causal masking.** PAM learns by *non-causal* masked completion (predict an interior
   span from *both* sides). The instant masking becomes causal (past-predicts-future),
   PAM is a forward predictor wearing a mask. Hold this line explicitly.
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

- `PROJECT_STATE_AND_MVP.md` — the full architecture, every decision, status (settled /
  proposed / deferred), open gaps, and the suggested MVP. **This is the base for the MVP
  build chat.**
- `substrate_description.md` — the detailed pooling-substrate spec (folded in summary into
  the state doc, but the standalone has the full detail).
- `association_cortex_operation_spec.md` — the twelve characteristics. **Stable. Do not
  re-litigate.** The open-questions framing in it predates the current architecture; the
  state doc supersedes it.
- The **mechanism map** (latest version) — a map of the *possibility space*, not a design.
  Trust its tension map and `[CONFIRMED]` items; treat its *recommendations* and staged
  build with caution (they lean conservative — they trade away the novel part, drift, first).
