# EXP15 — DURABILITY BY DOSE (within the shuffled fabric) — PRE-REGISTRATION

**Status: FINALIZED — ratified (Jason, 2026-07-10); amendments A1/A2 folded; RULINGS 1–3 folded at the
build gate (2026-07-10).** Build stage complete. **The 40 runs are WITHHELD** behind the §8 surface;
GO releases them. Scoring runs behind the adversarial refute-default pass — **no lens assumes D > C.**
Attribution routes to Jason.

**Lineage.** The §10.24 held-open companion: *"fabric gates ONSET; dose MAY gate DURABILITY."*
§10.24 recorded it as **NOT POWERED** — "a NEXT QUESTION, not a finding" — and set the promotion bar:
a *powered durability read, on a parity-matched referent.* **EXP15 is that gate.**

**Onset is NOT at stake.** EXP14's verdict — FABRIC main effect ON ONSET — stands regardless of this
experiment's outcome. A NOT-PROMOTED outcome retires the companion at this power; it does not touch
§10.24.

> **BUILD-GATE CORRECTION (2026-07-10, ratified).** The companion's motivating numbers — **D 2/4
> sustain vs C 0/5** — were a **single-endpoint artifact** (`endpoint ≥ band`, one window per seed).
> Under the ratified `mean(last 10) ≥ band` they become **D 0/4, C 0/4**. See §6 and the §10.24
> annotation. The *question* survives — corrected, weaker, and exactly what this powered read is for.

---

## 0. Discipline traps (carried)

- **No new loss, no new force, no new mechanism, one code path.** Runs are `run_exp14_arm` **verbatim**
  (digit-identical to `run_exp12_arm`). Both arms are existing EXP12 arms. The only additions are
  observation/scoring and a trajectory-inert mid-horizon checkpoint.
- **Manufacturing-class FENCED.** Nothing is engineered to make D persist or C decay. Loss-engineering
  stays fenced. EXP13 stays PAUSED.
- **Determinism:** seed + construction order + `threads=1` + faithful runner. Fabric pre-built at
  `H_MAX = 1M` — **ONE fixed permutation per arm, no rebuild** (F1). Both arms are shuffled-fabric.
- **Checkpoint contract:** `.pt` at 500k, at 1M, and at the online conversion-onset trigger.
- **Report-don't-patch.** Records stand and get superseded, never overwritten.
- **Refute-default at scoring.** Cal is not a prior the verdict confirms (Pin-2 posture, carried).

---

## 1. The question

**Within the shuffled fabric, does DOSE gate DURABILITY?** Conditional on conversion: does the
converted regime **persist late** under coin (D_split) more than under scheduled (C_shuffle)?

Nothing about onset. Fabric already gates that.

---

## 2. Arms

| cell | arm | fabric | dose | EXP14 status (committed) |
|---|---|---|---|---|
| **C_shuffle** | `exp12_shuffle` | shuffled | scheduled | 5/8 convert |
| **D_split** | `exp12_split` | shuffled | coin | 4/8 convert |

Dwelled cells are **out of scope** — they do not convert, so durability is undefined there. The
contrast is *within* the permitting regime.

---

## 3. Ratified constants

| Constant | Value | Note |
|---|---|---|
| **Common ruler** | **0.6875 × 5** | converter classification, BOTH cells. Per-cell EXP14 bands retained ONLY for the reproduction check (§5a). Verified **set-preserving**: tautological for D (the ruler *is* D's band); **non-trivial for C** (raises 0.64 → 0.6875; all 5 converters survive, min longest-run 21). |
| **Durability-pool gate (Ruling 3)** | **longest-run ≥ `EPISODE_MIN` = 8** | an **existing house constant** (the s0-class bound), not a new one. Set-preserving on committed data (census: converters start at 21). Structurally excludes bare-N phantoms when the tails get sampled 5× harder. **Converter classification is unchanged** — this gates the *durability pool* only. |
| **Runway censoring** | **`T_DUR` = 200k** | converter with **< 200k** post-conversion-onset runway = **DUR-CENSORED**: reported, excluded from the primary, **never scored as "decayed."** Under Ruling 1 it now guards the **opposite** confound: a late converter trivially populates the final quartile. |
| **Primary window** | **(375k, 500k]** | the final quartile, **absolute** — not a fraction of the post-acquisition span. 416 eval windows at `EVAL = 300`. |
| **New seeds (Ruling 2)** | **{8–19} ∪ {28–35}** = 20/cell | 40 runs. **Cal-disjoint, s23-free, reserve-disjoint.** |
| **Converter floor** | **12 eligible converters per cell** | |
| **Reserve pool** | **{40–47}** | tops up **BOTH** cells in pairs, **by rule only**, cap **+8/cell**. |
| **Substitution pool (Ruling 2)** | **{36–39}**, lowest-unused first | disjoint from the reserve; decided at rejection, recorded. |
| **Horizon (A2)** | run to **1M** unconditionally; **primary frozen at 500k on ALL seeds** | the 500k→1M tail is a descriptive companion, no claim. |

### 3.1 Why the seed pool was repaired (Ruling 2 — keep, so it is not re-introduced)

The originally ratified `{8–27}` **re-admitted the EXP14 cal seeds `{20,21,22,24,25}`**. A run is fully
determined by `(arm, seed, h_max)`, and C's cal2 ran at `h_max = 1M` — so re-running those seeds would
have been **bit-identical replays of the very runs that cut C's band.** Their conversion outcomes are
already recorded. That is an **outcome-blindness break on 25% of each cell's sample**, not merely a
circularity; EXP14 prereg §0 pinned *"verdict-seeds ≠ cal-seeds."* `{8–27}` also contained **s23**, the
seed EXP14 rejected as a genuine fabric defect. The EXP15 pre-check reproduced that defect
independently on both shuffled arms (per-lag nuisance `0.13464194536209106 > 0.13435383141040802`).

---

## 4. Primary (RULING 1 — locked-state sustain RETIRED)

**PRIMARY: exact one-sided Mann-Whitney (D > C) on FINAL-QUARTILE TIME-ABOVE-BAND** — the fraction of
eval windows in **(375k, 500k]** with `exam_acc ≥ 0.6875` — among **ELIGIBLE converters**, **NEW SEEDS
ONLY.**

**Eligible** = converted (≥ 5 consecutive windows ≥ ruler) **AND** longest-run ≥ 8 **AND** runway
≥ 200k. The three exclusions are reported separately and never conflated.

**Grounds (all four ratified):**
1. It is already a **registered §7 companion** — named before any peek.
2. It is **continuous**, so there is no threshold to α-calibrate. The null is exactly **between-cell
   exchangeability**, which the exact rank-sum test conditions on. Tie-aware, deterministic, no RNG,
   no normal approximation.
3. It **operationalizes durability for an episodic phenomenon**: does the regime persist late?
4. **New-seeds-only quarantines every disclosed peek** — CC's Mann-Whitney on last-10 means, and
   Jason's verification computations alike. The **committed 16 are CONTEXT/SENSITIVITY, never primary.**

**Why the locked state was retired.** See §6. It is not merely degenerate; it is the **wrong category.**

---

## 5. Instrument fixes (build gate — precede everything else) — **DONE**

**(a) Coded reproduction check.** Reused C/D verdict runs at their EXP14 bands must yield exactly
**C {0,2,4,5,6} / D {0,1,3,6}**. Assert; fail loud. Mismatch = **INSTRUMENT REGRESSION** → fix the
pipeline, **no read.** *(Passes; robust to ±1e-9 band perturbation.)*

**(b) `score_2x2` D-row wiring fixed.** The D row keys on the **reproduction check**, not on
`count_class ≥ 5`. (Latent EXP14 mislabel: D at 4/8 → `AMBIGUOUS` → excluded from `converts` → the
draft read `INSTRUMENT_REGRESSION` despite exact reproduction; only the Pin-3 override masked it.) Old
logic marked **SUPERSEDED in-code.** The committed `exp14_2x2_verdict_verdict.json` is **not**
regenerated — records stand. *(Dry-verified: on the post-refutation set {C,D} the fixed scorer emits
`FABRIC_MAIN_EFFECT` — the committed verdict — directly.)*

**(c) `score_durability`** implements §4/§7.

**(d) Coded loose-N floor gate (Ruling 3).** The cross-experiment carry becomes machinery, not a note.
Per cell, at the common ruler: the **false-alarm EXPECTATION** on the cell's own honest null vs the
observed converter count, plus a **bare-N census** (max-run per seed) in **every** surface. **A cell at
its floor is flagged before its count means anything.**
- **Unit: EPISODES, not hit-positions** (per `feedback_loose_N_false_alarm.md`). A position-rate
  overcounts by the mean cluster size; at N = 3 (cell B) episodes are almost all exactly length 3, so
  the shortcut was safe — at N = 5 it is **not.** Both units are reported; the **episode unit is the
  gate.** Contiguity respected (a spliced pooled null manufactures runs).
- On committed data: **D observed 4 vs floor 1.48 → ABOVE-FLOOR.
  C observed 5 vs floor 3.83 → AT-FLOOR, flagged.** C's crossing count carries no signal; **C is
  carried by episode quality (runs of 21–90), exactly as §10.24 already states.**

---

## 6. Stage-one cal + the locked-state finding — **DONE, from existing traces only**

- **Fabric pre-check**, outcome-blind, T = 15k: `{8–19}` and `{28–35}` both arms; s28 carried from the
  s23 swap. Substitution pool `{36–39}`. Every rejection and replacement recorded.
- **`spec_hash` parity (F2):** one hash across reused (cal + cal2 + verdict) and new manifests. Fail
  loud, naming any divergent cell.
- **Sustain-cal (no new runs):** false rate of the last-K-mean detector at the ruler on the D-null and
  C-between cal pools, against α = 1e-3.

### FINDING (recorded): **LOCKED-STATE SUSTAIN DOES NOT EXIST AT 500k IN THIS REGIME**

| definition | D | C | note |
|---|---|---|---|
| `endpoint ≥ ruler` (the §10.24 basis) | 2/4 | 0/4 | **single-window artifact** |
| **`mean(last 10) ≥ 0.6875`** (was to be the primary) | **0/4** | **0/4** | |
| `mean(last 5)` / `mean(last 20)` | 1/4 / 0/4 | 0/4 / 0/4 | |
| `mean(last 10) ≥ 0.79` (α-calibrated) | 0/4 | 0/4 | |

**0 of all 16 committed verdict seeds sustain**; best is C-s6 at **0.6873**, one thousandth short. The
detector's false rate **exceeds α on every null pool** (D-null 0.00433, C-between 0.00174, D-between
0.00137), and the α-calibrated K = 10 bar is **0.79 — higher than the ruler**, making sustain rarer
still. **No bar both controls α and produces sustainers.**

That is a fact about the **regime**, not only the instrument: conversion here is **episodic**, so a
locked-state read measures a state the phenomenon does not occupy. Hence the re-posed continuous
primary (§4).

**Episode recurrence, verified** (committed converters; episodes = runs ≥ 5 consecutive windows at or
above the band):

| counting rule | per-converter range | median |
|---|---|---|
| at the **common ruler** (0.6875) | **2 – 27** | 9 |
| at each cell's **own EXP14 band** (C 0.64 / D 0.6875) | **2 – 23** | 12 |

Eight of nine converters show **≥ 4** distinct episodes; only D-s3 (2 episodes) is close to a single
excursion. Per-converter, at the ruler: C {0:27, 2:5, 4:9, 5:6, 6:7}, D {0:13, 1:12, 3:2, 6:22}.

> **FACT-CHECK NOTE (2026-07-10).** The ruling text gave this as "8–23 recurring episodes per
> converter." The **upper bound 23 reproduces exactly** under own-band counting; the **lower bound
> does not** — the minimum is **2** (D-s3) under every counting rule tried (ruler/own-band × N ≥ 5 /
> N ≥ 8 × all-converters/eligible-only). Verified figures are written above; "8–23" is **not**
> propagated. The qualitative claim — conversion is episodic, not a locked state — **stands and is
> strongly supported.**

---

## 7. Outcome cells (named now; executed as written)

**Primary:** exact one-sided Mann-Whitney (D > C), as in §4.

| cell | condition |
|---|---|
| **PROMOTED** | p ≤ 0.05 **AND** ≥ 12 eligible converters per cell |
| **NOT-PROMOTED-AT-POWER** | floor met, p > 0.05 → the companion is **retired at this power**, recorded |
| **INVERTED** | C > D significant → **anomaly-class**; surface, audit, **never force** |
| **UNDERPOWERED** | floor unmet after capped top-up → routes to Jason, named |

Floor checked **first**. Top-up: pairs from `{40–47}`, lowest-first, **both** cells, cap +8/cell.

**Sensitivities (reported, NEVER verdict-deciding):**
1. **last-10-mean as a LEVEL** — *the peeked statistic* (CC's MW; Jason's verification). Sensitivity only.
2. **the 0.64-ruler variant.**
3. **committed-16-included variant** — context; the committed seeds are peek-contaminated.

A direction-flip under sensitivity → promotion carries a visible **DEFINITION-SENSITIVE** caveat; the
primary still decides.

**Companions (read-only, no claims):** episode recurrence counts; last-episode-end times; the bare-N
max-run census; the 500k→1M tail.

### 7.1 CENSORING DEPENDENCY — declared *before* the runs (diagnostic, not a sensitivity)

On the **committed 16** the sole DUR-CENSORED seed is **C-s6** (conversion onset 427.5k, runway 72.5k).
Its final-quartile fraction *would be* **0.4688** — second-highest overall — and including it moves the
committed-context p from **0.028571 → 0.095238**. **Censoring it is correct**: with 72.5k of runway the
final-quartile fraction measures **recency** (it just converted), not **durability** (it persisted) —
precisely the confound `T_DUR` was re-scoped to guard.

**Therefore: "include the censored seeds" is NOT a valid alternative primary and must not be scored as
one.** The dependency is **reported** so that a result resting on a single censoring decision is
*visible*, **not** so that the decision can be reversed after seeing the outcome. Recorded here in
advance, on committed data, before any new seed is run.

**Scope fences:** no onset re-litigation; **no claim beyond durability-by-dose within the shuffled
fabric, at this power and this horizon.**

---

## 8. Gate sequence

1. **Docs commit** — this prereg + three riders (§10.24 exposure-ground demotion; the loose-N carry into
   `docs/`; the §10.24 companion correction).
2. **Instrument fixes** (§5) — reproduction check, D-row wiring, `score_durability`, floor gate.
3. **Runner extension + smoke** — mid-horizon checkpoint; the existing digit-identical checks stay green;
   plus the D-row logic, the run-to-1M / read-at-500k round-trip, exact-MW unit tests (against
   brute-force enumeration and hand tails), the Ruling-3 pool gate, the floor gate, and a **`spec_hash`
   drift assert** (the new parameter must not enter the hashed payload).
4. **Pre-check + sustain-cal** (§6).
5. **HARD STOP → surface.** Do **NOT** launch the 40 runs. **GO releases them.**
6. (post-GO) 40 runs → `score_durability` DRAFT → **halt** → adversarial refute-default panel →
   attribution routes to Jason.

---

## 9. Known issues in the inputs (records stand; surfaced, not patched)

- **`exp14_band_2x2_cal.json` — `D_split.false_rate_referent` is factually wrong.** The canned string
  *"(this cell does NOT convert at cal)"* is applied to A, B **and D**. It is true for A and B (no
  s0-class episode at cal). **It is false for D:** D's cal **s20 has a 36-window run ≥ 0.704** — a full
  s0-class converter, which canon elsewhere records. **No number moves** (D's provisional cut already
  excludes s0-class episodes); the defect is confined to the annotation. The committed JSON **stands**.
  A successor reading it verbatim would wrongly believe D's cal pool is clean like A/B — hence this note.
