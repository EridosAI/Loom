# CORRIDOR PROTOCOL — standing execution practice

**Status:** STANDING. · **Authority:** Jason (design chat, 2026-07-11), ratified as canon practice at the
opening of the EXP16 corridor. · **First instance:** EXP16 capture-feed discrimination
(`docs/EXP16_CORRIDOR_BRIEF.md` = the EXP16 gate table, halt fences, and envelopes as instantiated).

This document is the **experiment-agnostic form**. A corridor brief instantiates it per experiment by
filling the gate table, the halt list, and the envelope/constant set — nothing in the mechanics below
is experiment-specific.

---

## The one principle

**Pre-named decisions execute; judgment halts.** Every gate carries its condition and its action,
both written *before its data exists*. If the honest next sentence is "I recommend…", that is a HALT
by definition — surface and stop. **Repeat-compute is authorized; improvisation is not.**

## The standing cadence — three human touches per experiment

1. **Ratify the design** — the prereg, its outcome cells, its routes (the existing design gate).
2. **Read the pre-flight** — one package, one sitting, *before* the terminal opens (§ Pre-flight below).
3. **Rule on the verified result** — attribution + canon, the only decision the corridor can never contain.

Everything between touch 2 and touch 3 is **corridor**: pre-named conditions, halt fences, append-only
commits, auto-push, terminal verification. A clean corridor is **necessary, never sufficient**.

## The gate table (form)

A corridor is a linear sequence of gates. Each gate is a row:

| field | meaning |
|---|---|
| **Gate** | the check being run |
| **Pre-named condition** | the pass/fail test, fixed before the gate's data exists |
| **Pass action** | what executes automatically on pass (proceed / launch next / record) |
| **Fail action** | the pre-named response — either a **named recovery** (e.g. substitute-from-pool, record) or **HALT** |

Every fail action is either a *named, mechanical recovery* or a *halt*. A gate with a fail mode that
routes to neither is not corridor-ready — it must be resolved at design or pre-flight, never in-corridor.

**Auto-push at every closed gate.** Commits are append-only; committed records are never regenerated.

## Halt fences (the exhaustive list is written per instance; the standing members)

Halt = **stop, surface, wait**. Standing fences present in every corridor:

- any **REUSED-class** pre-check failure (a committed same-conditions assert now diverging = instrument
  regression, deterministic replay — never substitute);
- any run-time fabric-assert / smoke / spec-hash / parity / checkpoint / contract failure;
- any measured value **outside its pre-named envelope**;
- any outcome landing in **no named route**;
- a verification/refute panel returning a **MUST-FIX or judgment-class** finding;
- a **contradiction discovered between two rules**;
- **substitution-pool exhaustion**;
- anything for which the honest next sentence is "I recommend…";
- **anything not covered by a written rule.**

## Envelopes & constants

Every constant, definition, route, and envelope is **fixed before its data exists**. A value that lands
inside its envelope is *recorded and the corridor continues*; a value outside it *halts*. No constant,
definition, or route may be modified in-corridor **for any reason**.

## Conduct in the corridor

- **Report-don't-patch.** A surprising-but-in-envelope value is recorded and the corridor continues; an
  out-of-envelope value halts. Surfacing replaces fixing.
- **Mechanical folds only.** A typo-class change, cited, with record, is permitted. Anything touching a
  **number, a route, or a definition is judgment-class** → halt.
- **Canon amendments route to ratification, always.** Writing code for an already-ratified route is
  mechanical and may be corridor-prep. But amending a *committed document* — a prereg's build scope, an
  outcome route, a constant — is a canon change even when the code it enables is uncontroversial. The
  code being uncontroversial does not make the scope change silently yours: surface it, route it to
  ratification, then build. (EXP16 AMD-12 is the standing instance — the scorer code was uncontroversial;
  adding it to the committed prereg's build scope was not.)
- **The wrong-reason taxonomy applies to the corridor itself.** A gate passed for an *unverifiable*
  reason is a halt, not a pass. (E.g. an invariance-only smoke that would also pass a dead no-op does not
  certify the delta — a positive-delta assert that fails under the no-op is required.)
- **Provenance-computed, never asserted.** Every provenance, referent, and status string is **computed
  from the data it describes, at the point it is written**. A string asserted in a branch is a claim
  without a measurement, and is treated as a **MUST-FIX at panel**. *(Motivating instance:
  `exp14_arms.py:743` — `false_rate_referent` asserted "this cell does NOT convert at cal" while the same
  cell's committed `per_cal_seed_converters` field showed 3/5. Report-don't-patch: the EXP14 artifacts
  stand; the rule is the fix.)*
- **Even-count medians state their convention.** Any median over an even-count pool **names the
  convention** (lower / upper / two-middle mean) and **reports the two middle values alongside it**.
  *(Motivating instances: EXP17 F4 stat3 two-middle average; the converter-onset median — two middles
  **150,300 / 172,200 → 161,250 exact** — the third of three incidents, with the seat's upper-median slip
  and canon's round-half-even display of the exact .25.)*
- **Raw counts never gate a finding.** Raw counts scale with the detector's false rate and sit inside the
  floor-audit phantom bracket; a raw-count power floor is a floor on *noise*. **Certified counts only.**
  *(Ledger 18, a catch-15-species regression. The instance was recorded; the forward-binding rule was not.)*
- **Prose figures carry the same recipe-naming burden as canon figures — from any chair.** Every number in
  relay text, chat, a handoff, **or a launch brief** names the recipe that produced it and is **computed
  in-session or read from a committed artifact** — never restated from recollection. Binds the design seat,
  **CC**, and the **design authority**. **The weak point is not the seat. It is prose, and prose is written by
  everyone.**

## The pre-flight package (touch 2)

Assembled once, read once, before the terminal opens. Contents:

- **(a)** the verbatim texts of every operational definition the corridor will apply *where it bites*
  (the gate wordings, probe/field choices, outcome-row wordings) — read now, not reconstructed later;
- **(b)** every constant fixed at this gate — **formula, measured inputs, resulting value, and its
  provenance statement** (for a blinded constant: the statement that it was fixed before the treatment
  data existed, and how);
- **(c)** the pre-check outcome, with any substitutions and their rule citations;
- **(d)** the gate table + halt list + envelopes for this instance;
- **(e)** this protocol (or its instance brief).

**Mandatory gate-executor audit (added after the EXP16 corridor was found code-incomplete at open — the AMD-12 instance).** Every gate row in (d) MUST name its **executing function** and its **positive-delta smoke ID**. A gate whose executor does not yet exist — or exists without a smoke-tested positive-delta assert — is a **pre-flight blocker**: the corridor does not open. This is the generalized fix for the motivating failure — EXP16's §4-partition scorer and its cal-read gates were never built (the prereg's build scope enumerated only the arm flag + the probe), and the gap survived five review layers because each verified *what exists against its spec*, never *the gate table against its executors*. It was exposed only when writing the gate table made "executable by what?" a checkable question. A corridor cannot open with an unexecutable gate.

**Reachable-falsifier requirement (extends the gate-executor audit; a pre-flight blocker).** Every gate names not only its executing function and positive-delta smoke, but a **falsifier reachable from the real data path**. A branch that cannot fire on any admissible input is dead code, and a gate whose only failing input is hand-fed to the smoke is **not certified**. *Motivating instance: SCATTER/EXP17 `floor_clean` — the self-excluded null excludes (band,N) episodes then counts (band,N) episodes, so `floor_clean ≡ TRUE` identically and the NOT-CERTIFIABLE-by-count branch is unreachable from the audit; it was exercised only by passing `floor_clean=False` by hand. Five refute-default lenses read it as a pass.*

**Every gate must have failed at least once before it can pass (the red-team rule; extends reachable-falsifier from *reachable* to *observed*).** A gate's positive-delta smoke is not certified until it has been **observed red** under a deliberately broken input — a perturbed seed, a no-op executor, a naive implementation. **A gate that has never failed has been asserted, not tested, and its PASS is unverifiable.** *(Instances: `floor_clean ≡ True`; EXP19 G0b v1 — a permutation-invariant comparator that could not fail on the mode it existed to catch; `wp-strat-label`, certified only by writing the naive `pos == 1` version first and watching it go red.)*

**Estimator-support check at pre-flight: every pre-named estimator's input domain verified non-empty from the real data path.** (Ratified 2026-07-25, ledger row 55 — the motivating instance: STEP-0's §4 per-channel onset-dominance estimator was committed with a structurally empty vis-channel domain — the mask schedule guarantees position-1 word-mask, so `pos_err_vis` carries p1 in 0/13,328 columns; the prereg's own G0 checked fields, not buckets. The census-surfaced HALT held the gate lawfully; this check moves the catch to pre-flight, where it costs nothing.)

**Arms are priced when they open, not when they are banked.** A banked arm's cost, instrument, and dose range are **[ESTIMATE]** until its prereg is written against committed code and constants. **Pre-registration fixes bars against post-hoc movement; it does not certify an arm nobody has opened.** Every banked arm gets an **instrument audit at prereg** — its knob's reachable range, its confounds, **and its endpoints re-derived from code, on the lineage the certified records actually live in** — before it is scheduled or costed. *(Motivating instance: EXP19 v3, spec'd against `exp13_fabric` where its certified endpoints do not exist — ledger 26. The audit is the standing guard.)*

**On ratification of the package:** commit the protocol + the constant record + the pre-flight surface,
push, and the corridor OPENS. From that moment the next human touch is the terminal surface — unless a
fence trips.

## The terminal surface (touch 3)

One package: the DRAFT result + the verification/refute panel record + the **full gate log** (every gate,
its condition, its measured outcome, its action) + companions + sensitivities + any flags riding
(not-certifiable, borrow-branch, participation route) + the bare-N census. It routes **first** to an
independent **terminal verification pass** (re-derived from pushed artifacts, at full review depth),
**then** to the human for **attribution + canon** — the one decision the corridor never contains.

---

**Invariant.** A clean corridor is necessary, never sufficient. Pre-named conditions, halt fences, and
append-only auto-pushed commits carry the mechanical work; **attribution and canon remain human.**


---

## EXP21-derived standing riders (ratified at the EXP21 touch-3 close, Jason, 2026-08-06 — prospective; EXP21's frozen scorer and constants are NOT altered)

**Non-finite law.** Every scalar entering a gate, route, guard, envelope comparison, or reported
route companion must be explicitly checked finite before use. NaN or infinity is a HALT unless the
prereg contains a specific UNREAD/unsupported route for that field. Python's default fail-open NaN
comparison is never an admissible rule. Every scorer must carry an observed-red NaN fixture and an
infinity fixture. Machine-readable verdict and terminal artifacts must be serialized with strict
JSON semantics (`allow_nan=False` or equivalent). A non-finite value may be described in prose or
represented by an explicit tagged/null structure, never a bare JSON NaN token. *(Motivating
instance: EXP21 ON-s3's one degenerate probe read — route-invariant, but only proven so after the
fact; ledger row 59.)*

**Ratification freeze completeness.** A Touch-2 freeze surface must hash every law-bearing module
and every executable named in the gate table — not only constants, scorer, banks, and pre-flight
prose. An omitted law-bearing module is a pre-flight blocker. *(Motivating instance: EXP21's
freeze omitted exp21_cal/probe/teaching; no drift occurred, proven by provenance — ledger row 60.)*

**Discrete-grid arithmetic.** When a statistic is a count over a fixed denominator, gate
comparisons use the integer counts or exact cross-products. They must not be decided by float
representations of equal rational grid points. *(Motivating instance: EXP21's delta_ret vs the
exact 6/84 boundary — latent, non-biting, panel-proven.)*

**Quantile convention.** Every percentile or quantile used as a constant names its estimator:
order-statistic index/interpolation method, indexing convention, and even-count handling. "99th
percentile" without the estimator is incomplete provenance. *(Motivating instance: EXP21's q99
order statistic — provably zero effect on theta, but convention-dependent by construction.)*
