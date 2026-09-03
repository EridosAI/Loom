# Experiment 01 — Pooling Substrate Validation Rig

**Purpose.** Validate, in isolation, the core mechanism of the project's growth substrate:
**soft-tied weight pooling** that opens resolution (unpool) and reclaims it (re-pool) under
local signals. This rig tests the *mechanism's mechanics and central claims* on a fully
controlled toy task — **before** any integration with the wider architecture. It exists to
**fail loudly if the substrate is inert**, so the project doesn't build on a mechanism that
doesn't work.

Context (not required reading to implement, but orienting): `docs/substrate_description.md`,
`docs/PROJECT_STATE_AND_MVP.md`.

> **Discipline — pre-registered failure conditions.** Each test below states what result
> means **the theory is wrong**. An isolation test with no failure condition becomes a demo
> that always "works." These conditions are the point. Do not soften them after seeing
> results.

---

## 0. The one property that makes this test valid

**Capacity must track the hierarchy.** The *coarse* distinction must be learnable in the
*pooled* (low-resolution) state; the *fine* distinction must genuinely *require* unpooling.
If fine is already learnable while pooled, unpooling buys nothing and the test shows nothing
(false negative). If coarse needs high capacity, the pooled baseline fails and you can't
separate "pooling broken" from "task too hard."

This is why the data is **synthetic hierarchical Gaussians** — the capacity gradient is built
*by construction* via two knobs (`R_coarse`, `r_fine`), not hoped for. (Note: the literal
"red ball / green ball" framing is a *bad* test, because colour is a cheap low-level feature —
fine would be easier than coarse, inverting the gradient. The synthetic data avoids this.)

---

## 1. Data — hierarchical Gaussian clusters (4 → 16)

Generate a tree-structured clustering in `R^D`:

- **4 coarse centres** `μ_c`, drawn far apart on a sphere of radius `R_coarse` in `R^D`.
- For each coarse `c`, **4 fine centres** `μ_{c,f} = μ_c + offset`, where `offset` has norm
  `r_fine` (with `r_fine << R_coarse`). 16 fine centres total, **nested inside** their coarse
  parent.
- **Samples**: `x ~ Normal(μ_{c,f}, σ² I)`.
- **Labels**: coarse `c ∈ {0..3}` and fine `(c,f) ∈ {0..15}`.

**The knobs that create the test condition (call these out; they're load-bearing):**
- `R_coarse` — inter-coarse distance. Large → coarse trivially separable while pooled.
- `r_fine` — inter-fine distance *within* a coarse cluster. Small → fine requires resolution.
- `σ` — noise. Set so coarse is comfortably separable (`σ` well below `R_coarse`) but fine is
  *hard but learnable* (`σ` comparable to or modestly below `r_fine`).

**Starting values** (tune from here): `D = 16`, `R_coarse = 10`, `r_fine = 1.0`, `σ = 0.3`.
**Required sweep:** vary `r_fine/σ` (e.g. fine-separability from easy to near-impossible) and
confirm the qualitative results below are not artifacts of one setting. The *ratio*
`r_fine : R_coarse : σ` is what matters, not absolute scale.

**Nesting check:** confirm fine sub-clusters sit *inside* their coarse parent (fine offsets
are small perturbations of the coarse centre), not independent dimensions. The
ancestors-gate-descendants structure depends on this.

---

## 2. Model — hierarchical additive-residual pooling

A small classifier whose feature layer carries the **fixed nested tree (1 → 4 → 16)** as
**additive residuals with per-level penalties**. This is the recommended formulation because
it maps the tree directly and makes graceful re-pool *literal* (drive fine residuals to zero,
coarse base survives). CC may implement an equivalent if cleaner.

**Feature layer — 16 units**, unit `i` has weight vector:

```
W_i = base_root  +  Δ1_{g1(i)}  +  Δ2_i
```

- `base_root` — **1** shared vector (the 1×1 / fully-pooled level).
- `Δ1_j` — **4** vectors, one per level-1 group `j` (the 4×4 increments). `g1(i)` maps unit
  `i` to its level-1 group.
- `Δ2_i` — **16** per-unit vectors (the 16×16 increments).

**Pooling penalty (the soft tie):**

```
L_pool = λ1 · Σ_j ||Δ1_j||²  +  λ2 · Σ_i ||Δ2_i||²
```

- **Fully pooled:** `λ1, λ2` large → all Δ ≈ 0 → all `W_i ≈ base_root` → **1 effective
  feature** (low resolution).
- **Unpool to level 1:** `λ1 → small`, `λ2` large → **4 effective features**.
- **Unpool to level 2:** `λ1, λ2 → small` → **16 features** (full resolution).
- **Re-pool:** raise the relevant `λ` again → those Δ shrink toward 0, coarser bases survive
  ("shed detail, keep coarse value").

**Tie is soft, never hard.** `λ` is a finite penalty, not a hard equality constraint. Hard
tying (Δ ≡ 0 enforced) is used only as a *control* (Test A).

**Heads:** a 4-way **coarse** head and a 16-way **fine** head, both from the feature layer.
(Two heads so coarse and fine accuracy are measured separately — the tests need both.)

**Maturational clock (unpool schedule):** `λ1(t)`, `λ2(t)` as **step schedules** over training
steps — start both high (pooled), drop `λ1` at `t1` (unpool to 4), drop `λ2` at `t2` (unpool
to 16). This is the **clock-led, pinned-constant** design (capacity opens on a schedule, not
pulled by error). Keep it a simple, fixed schedule for v1.

**Keep it tiny and CPU-fast.** Small `D`, small network, fast iteration. This validates a
mechanism, not performance. PyTorch.

---

## 3. Instrumentation (log throughout, all tests)

- **Coarse accuracy** and **fine accuracy** (separately), train and held-out.
- **Per-level residual norms**: `||Δ1_j||`, `||Δ2_i||` over training (shows pooling state).
- **Within-group weight spread**: for each level-1 group, the pairwise distance between member
  `W_i` vectors (shows differentiation happening).
- **Intra-group gradient disagreement** — for members of a group, the alignment (mean pairwise
  cosine) of the gradients on their `Δ2_i`. **Low cosine / high variance = members "want" to
  differentiate.** This is the project's consumption/re-pool signal; logging it tests a
  separate claim (does disagreement behave as predicted: high during differentiation, low once
  settled) at near-zero cost, and Test C uses it as the trigger.

---

## 4. The tests

### Test A — Symmetry break **(make-or-break; run first)**

The load-bearing claim and the one most likely to fail. Two soft-tied members under identical
gradients stay identical forever; the substrate is inert unless something breaks the symmetry.

**Setup.** Minimal: 2 units in one level-1 group, data with 2 nested sub-classes they should
each come to detect. Initialise members with **tiny independent perturbations**. Relax `λ2`
(allow Δ2 to move).

**Procedure.** Train; track within-group weight spread and the two `Δ2` vectors.

**Pass:** with the **soft** tie, the two members **diverge** (Δ2 grow apart, distinct, tracking
the two sub-classes) once the data demands it.
**Controls:** (i) **hard-tie** (Δ2 ≡ 0) — must **fail** to differentiate (confirms soft-vs-hard
matters). (ii) **free** (no tie) — differentiates freely (upper reference).

> **FAILS IF:** with the soft tie, members do **not** diverge even though sub-structure is
> present and the free control diverges. → The substrate cannot differentiate from a pooled
> state. **Stop and rethink the substrate before anything else.**

### Test B — Pool → unpool → differentiate (the headline claim)

**Setup.** Full 4→16 model and data. Run the clock schedule: pooled → unpool to 4 → unpool to
16.

**Procedure.** Track coarse and fine accuracy against unpool depth.

**Pass:** coarse accuracy reaches ceiling **while still pooled / at level 1**; **fine accuracy
lifts specifically when depth crosses to level 2** (capacity opening *enables* the fine
distinction).
**Baselines (required — the test is meaningless without them):**
- **Always-pooled** (`λ2` stays high): upper bound on coarse; should **cap below** on fine.
- **Always-fully-unpooled from init** (`λ1=λ2=0`): standard model; fine should reach ceiling.
  Tests whether **gradual unpool matches this (no cost) or differs** — informative either way.

> **FAILS IF:** fine accuracy under gradual unpool does **not** exceed the always-pooled
> baseline. → Unpooling does not buy usable capacity; the core claim is wrong.
>
> **ALSO CHECK (function preservation):** at the unpool *step*, is there a large discontinuity
> in loss/accuracy? A clean mechanism should transition smoothly (newly-freed residuals start
> at ~0). A large lurch means the tie/relaxation mechanics are wrong even if accuracy
> eventually recovers.

### Test C — Re-pool (the reverse direction)

Two variants — run both; they test different real properties.

**C1 — signal removed (cleaner).** After B reaches full resolution, switch the data so fine
sub-structure **disappears** (samples for coarse `c` now drawn from `Normal(μ_c, σ²)`, no
sub-clusters). The fine distinction is no longer *present*.

**C2 — signal present but not rewarded (more realistic).** Keep the sub-clusters in the data,
but **stop training the fine head** (only coarse loss). The distinction is still *in the input*
but stops *earning its keep* — which is what the running system actually faces (distinctions
don't vanish from perception; they stop being useful).

**Procedure (both).** Drive re-pool by the **intra-group gradient disagreement** signal: when
it is **sustained low** (members no longer pulled apart) **and** use is low, raise `λ2`
(re-tighten). Track within-group spread, `||Δ2||`, and *both* coarse and fine accuracy.

**Pass:** members **re-converge** (Δ2 shrink toward 0) under sustained low disagreement; **coarse
accuracy survives** while fine degrades **gracefully** (coarsening, not collapse). The coarse
base is retained.

> **FAILS IF:** members do **not** re-converge under sustained low-disagreement+low-use, **or**
> coarse value is **destroyed** (re-pool is not graceful — it erases rather than coarsens).
> → The reverse direction is broken.

### Test D (observational, free) — does the disagreement signal behave as theorised?

No separate run. Across A–C, check the logged **intra-group gradient disagreement**:

**Expected:** high while a group is actively differentiating (Test B, level-2 phase), falling to
low once members have settled into distinct stable detectors, low when there is no sub-structure
to find (Test C1). If it behaves this way, the project's central control signal (the
consumption/re-pool trigger) is validated cheaply.

> **FLAG IF:** disagreement is uninformative (e.g. stays high after settling, or low during
> active differentiation). → The signal we plan to use as the universal pooling control may not
> carry the information we assumed. Note it; it affects the re-pool trigger design.

---

## 5. Deliverables

- The data generator (parameterised by `D, R_coarse, r_fine, σ`).
- The model (hierarchical additive-residual pooling, per-level `λ`, step schedule).
- A run harness producing, per test: the instrumented metrics (§3) as logged series + plots,
  and a **pass/fail line against the pre-registered condition**.
- A short results note per test: pass/fail, the plots, and (if failed) what the failure implies
  for the substrate.

## 6. Explicit non-goals

Not testing: integration with cortices/PAM, the convergence loop, confidence-as-currency,
tracing, the store, any real perceptual data. This rig is the substrate **alone**. Resist
adding scope — the value is a clean, falsifiable mechanism test.

## 7. Notes / freedoms for the implementer

- The additive-residual formulation is recommended for clarity; an equivalent soft-tie (e.g.
  penalty toward a running group mean) is acceptable if it preserves: soft (not hard) tie,
  per-level relaxation, and graceful re-pool (coarse survives).
- `λ` schedules are pinned constants for v1 (clock-led). Do **not** make unpooling
  error-triggered — the design claim is that the clock *leads* and error *consumes*. (Driving
  re-pool by the disagreement signal in Test C is the reverse direction and is intended.)
- Favour many fast small runs over few large ones; the sweep over `r_fine/σ` matters more than
  scale.
