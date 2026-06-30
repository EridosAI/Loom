# Exp07 (Phase 0) — Cue-Floor × Penalty-Surface Decompose — CC Implementation Spec

**What this is.** The **measured opening phase** of exp07 (the joint re-pose). It does **not** build the
redesign — it measures the surface the redesign is scoped from: **the cue floor as a function of the
penalty regime**, read through the committed neutral (d)-gate. Two outputs:
1. the **intrinsic/inflated split** of the deployed cue-diffuseness — how much is posing-inflated
   (recoverable by content-blind re-organization) vs an irreducible floor (must be built-robust-to) —
   **measured, not argued**;
2. an **empirical adjudication of the penalty-legitimacy call** the design pass settled by argument
   (preserve/reshape vs correct/drop).

Pre-registered, exp03/exp06-style: failure and outcome conditions fixed here, before any run.

**Status.** `[PROPOSED]` diagnostic. Reuses `dgate.py` (committed, gate `335f36d`) as the read
instrument and the exp06 deployed knobs. **No new operator, no store.** Touches no settled mechanics.

**Why 2D, not 1D (locked reasoning).** exp06 established the two levers interact **super-additively**.
A cue floor read at one pinned penalty is therefore a *slice through an unknown surface*, assuming a
separability the exp06 finding directly contradicts. The penalty level exp07 *reshapes to* determines the
cue floor exp07 *faces* — so the floor must be read **against** the penalty axis. The 1D version returns a
confidently-wrong floor because it cannot see the interaction already known to exist.

---

## The two legitimacy locks this phase carries (framing — do not flatten)

1. **Penalty = preserve/reshape** (the open-and-stay-open envelope discipline), with **fixed-PAM as a
   *pinnable* simplification** kept on the radar. The distinction is **three points** —
   **developmental → fixed-but-emergent → store** — and "correct it" lands PAM at the **middle**
   (fixed-resolution prototypes, content still gradient-shaped), **not** a store. Preserve's argument is
   **architectural uniformity with the cortices** (same machinery everywhere), **not** store-avoidance.

2. **Cue = partial-preserve**, split **measured not argued**. The cue fix is intrinsically **two-part** —
   *preserve the irreducible floor* (build robust to real diffuseness) **AND** *correct the inflation*
   (re-organize away fake diffuseness) — **symmetric in weight to the penalty, different in shape**
   (penalty fix = one clean reshape; cue fix = two-parter). **Guard: never flatten the cue fix to "make
   the cue sharp"** — sharp is the toy, diffuse-but-structured is the native substrate.

These are not penalty-primary. The penalty got the richer design treatment because **λ2 is documented**,
not because it is the bigger lever — a property of what is written down, not of which lever matters more.

---

## `[RECONCILE]` convention

Values tagged `[RECONCILE]` are read from the **exp06 commit** (the reconfirmed cube), not set by feel.
Consolidated register in §6.

---

## 0. Scope-lock

**New (exactly four things):**
1. the **content-preserving cue re-posing sweep** (§1, constructed in Step-0a);
2. the **3-regime penalty axis** `{off, reshaped, deployed}` (§1);
3. the **2D read + floor/ceiling extraction + topology classification** (§3);
4. the **penalty-legitimacy adjudication** (off vs reshaped column, §3).

**Member-count — explicit decision (resolved toward a measured call, not an assumption).** The **full
surface is read at deployed cardinality (16)** — exp06 resolved member-count as a non-load-bearing ~22%
degrader and a single-factor non-lever, and the surface must be read at the cardinality exp07 works in. So
member-count is **not a full third axis.** **But** exp06's super-additivity finding genuinely leaves open
whether the *cue/penalty topology itself* is a cardinality effect (member-count not killing the channel ≠
member-count not modulating the cue×penalty interaction shape). So a **bounded cardinality corner-probe**
(§1, six corner cells at one lower cardinality, no content-preserving sweep) converts "16-only is fine"
from an assumption into a measurement. The untested stone is thereby *closed by measurement*, not recorded
as a caveat.

**Operator-form NOT committed.** The `reshaped` column instantiates the open-tie regime via the **settled
λ2 envelope discipline** — a *concrete open-tie point to read the surface against*, **NOT** a commitment
of exp07's final reshape to that form (kept open, carried to analysis; §5).

**Out of scope:** any redesign build; **member-count promoted to a deliverable axis only if the corner-gate
fires** (the lower-cardinality surface may be *pre-computed* as overnight insurance — see Run plan — but is
*interpreted* as a third axis only on a qualitative corner mismatch, §1/§4); pinning exp07's final reshape
operator; adopting "sharp cue" as a fix (it appears only as a labeled reference, §1).

---

## Run plan (overnight — compute-unconstrained)

Compute is not a barrier and the run is unattended overnight, so **everything runs straight up — no
compute-staging, no probe-as-gate-before-investing.** The probe-early ordering was purely a compute hedge
and is moot. Two contingency branches are **pre-computed up front** — *pre-computed, not pre-promoted*: the
decision rules in §1/§3/§4 are unchanged; this only runs the data ahead so a fired branch does not cost a
second night.
- **Cardinality:** run the **full lower-cardinality surface**, not just the 6 corners. The 6 corners remain
  the *gate* (read first, §1); the rest is *interpreted* only if they mismatch — but it is already computed
  if member-count is promoted.
- **Phasing:** run the **`reshaped` column across the full clock-onset phasing sweep** (3–5 onsets) from the
  start. The reversal decision rule is unchanged (§3: locks only if reshaped stays worse across *all*
  phasings); the sweep is simply already in hand if the reversal branch triggers.

**What does NOT collapse — compute-staging ≠ interpretation-staging.** Running all cells at once buys speed,
**not** permission to skip a gate. CC still **surfaces Step-0 artifacts before reading any interior** (the
standing gate). The morning read still respects, in order: Step-0a/0b/0c (a sanity-gate failure blocks
interpretation **even though the cells were computed**), the cardinality corner-gate (read first), the
training-plateau invariant (every cell read at its d_diff plateau), and the binary bar with the ablation
guard. The night produces *all the numbers*; the gates still decide *which get read and in what order*.

---

## 1. The surface — cue ceiling-sweep × penalty axis

### Penalty axis — 3 qualitatively distinct regimes
| regime | meaning | exp06 anchor |
|---|---|---|
| `off` | no tie; fixed-resolution PAM — the **correct-it** endpoint | penalty-clean |
| `reshaped` | tie present, **open-on-clock, stays open** — the **preserve** endpoint (λ2 envelope discipline; PAM clock-onset pinned `[RECONCILE]`, §5) | new |
| `deployed` | tie **collapses** prototypes — the broken status quo | penalty-deployed (`pam_lam` `[RECONCILE]`) |

### Cue axis — per column, three segments
Each penalty column sweeps the **same** cue axis:
1. **flat-diffuse** (the deployed status-quo presentation: relevant association faint under coarse
   structure + distractors, snr `[RECONCILE]` ≈ 0.086) — the baseline.
2. **content-preserving re-posings**, swept toward maximal content-blind structure — the **candidates**
   for the actual fix. Concrete re-posings are a **Step-0a construction**, validated content-blind. The
   sweep parameter = degree/kind of structural re-organization; swept **to a (d)-plateau** (§3).
3. **sharp** (the high-snr stimulus, `[RECONCILE]` ≈ 5.83) — included **only as the column's labeled
   alive-reference / toy ceiling.** Sharp is **not** content-preserving and is **never** a candidate fix.
   **Why it is in the floor formula at all:** sharp is the *unreachable ruler* — it quantifies the
   *uncloseable gap* (how far honest, content-preserving re-organization falls short of a cheated signal),
   so the irreducible floor is computable per column. It is a measuring stick, not a destination. Anyone
   reading this later: sharp's presence in `floor = sharp − C` is **not** a latent "make-it-sharp" target —
   sharpening the deployed cue is forbidden (§7); sharp appears solely to *measure* what build-robust must
   survive.

**Read:** neutral (d) via `dgate.py`, member-count 16, at every (cue-segment × penalty-regime) cell.

**Deliverable:** the **cue-floor-as-f(penalty) topology** (§3) — `separable` / `monotonic` / `sweet-spot`
— **not** a scalar floor.

### Cardinality corner-probe (bounded — converts the 16-only assumption to a measurement)
At **one lower cardinality** `[RECONCILE]` (recommend the **2-member** point — anchored to the dgate
clean-2 value ~1.41 *and* maximum contrast against 16, so a cardinality effect shows most strongly there;
4-member is the alternative if monotonic detection is preferred), read the **six corner cells**:
`{off, reshaped, deployed} × {flat-diffuse, sharp}` — **no content-preserving sweep** (corners only; this
is the cheap probe, not a second full surface). These six reproduce, at the new cardinality, exp06's
OR-kill structure (alive iff sharp ∧ ¬penalty) **and** the reshaped-vs-off relationship.
- **Qualitative structure matches 16** (OR-kill holds; reshaped-vs-off relationship holds) → **16-only
  validated as a measured call**; member-count stays a non-lever; topology is not a cardinality effect.
- **Structure differs qualitatively** (e.g. penalty-kill is cardinality-dependent, or reshaped helps at
  one cardinality but not the other) → **member-count promoted to a third exp07 lever**; the full surface
  is re-read with cardinality as an axis (the controlled expansion, §4).

This is the cardinality analog of the measured-not-argued discipline: exp06's super-additivity does not
license assuming the interaction shape is cardinality-invariant, and the probe is cheap enough to settle
it.

---

## 2. Step-0 (runs first; surfaced for review before the surface is interpreted)

### Step-0a — content-preserving re-posing construction
Construct the cue re-posing sweep so each re-posing is a **content-blind structural transform**:
reorganizes *presentation* identically regardless of which association is masked, so it **cannot inject
discriminating signal.** Validation (cue-side analog of the ablation guard): a re-posing applied to a
**content-ablated** cue must **not** create (d) — re-organization cannot manufacture a floor. If no
re-posing can be constructed that varies structure at all without adding information → **flag; the sweep
is ill-posed.** Output: `cue_reposing_construction.json` (the sweep definition + the ablation-invariance
check + commit/spec hashes).

### Step-0b — two-sense separability gate
- **Cue-locatability** — read at the **`off` column** (no collapse confound): does *any* content-
  preserving re-posing lift (d) above the flat-diffuse baseline? **No → the relevant signal is not
  locatable in the concatenation → diffuseness is fully intrinsic → floor = deployed snr, cue-fix is
  *build-robust-only* (still NOT "make it sharp" — it is *accept-and-build-for*, the opposite).** Yes →
  run the full sweep.
- **Lever-separability** — read across columns: is the cue floor penalty-dependent? Answered by the
  surface itself (the topology, §3).

### Step-0c — predicted-column sanity gates (must hold, or the surface is suspect)
- **`deployed` column ≈ 0.000 across the entire cue sweep** (including its sharp segment) — the collapsing
  tie kills regardless of cue posing (exp06 OR-logic: penalty-on dead at every cue). If the deployed
  column lifts under re-posing or at sharp, the harness **contradicts exp06 — stop, debug. Not a result.**
- **`off` column, flat-diffuse segment ≈ 0.000** (= exp06 `[1,1,0]`: 16-member, diffuse, penalty-off,
  dead) — the sweep must start from the known-dead point.
- **`off` column, sharp segment ≈ 1.106** `[RECONCILE]`, **read at its training plateau** (= exp06
  reconfirmed `[1,0,0]`, 12000-step plateau — equal-training comparison, the exp06 reconfirm lesson; a
  sharp cell read at a shorter budget would be compared unfairly against a plateau-derived 1.106) — the
  column's alive-reference reproduces the known value. If not, the harness or stimulus scaling is off —
  **debug before interpreting floors.**

**REVIEW GATE:** surface `cue_reposing_construction.json` + the Step-0b/0c reads **before** the full
surface is interpreted.

---

## 3. The reading — ceiling-at-plateau → floor; topology; legitimacy

### Training-plateau invariant (every cell, the exp06 convergence lesson)
**Every cell is read at its training plateau, not at a fixed budget.** "Plateau" = the functional metric
**d_diff is flat** (consecutive-budget changes within seed-spread); **proto-spread growth is benign** and
is *not* a non-convergence signal (it is the live-regime substrate differentiating — the clean reference
does the same; proto-flat is a *death* certificate, not a *life* one — exp06's reconfirm finding, carried
here so it survives compaction). This is distinct from the cue-sweep plateau below: one is convergence
*within* a cell over training, the other is the cue-axis ceiling *across* re-posings.

### Plateau-before-read on the cue sweep (the new under-training trap)
Read each column's content-preserving ceiling **at a plateau**, not after one arbitrary re-posing.
**Under-re-organization fakes the floor too high** — quitting the sweep before (d) plateaus over-estimates
intrinsic-ness, exactly as under-training faked collapse in exp06. Sweep until consecutive re-posing steps
lift (d) by less than the seed-spread `[RECONCILE]`, then read the ceiling.

### Per-column extraction
- **content-preserving ceiling** `C` = the plateau (d) of the content-preserving segment.
- **recoverable / inflated part** = `C − flat-diffuse baseline` (recovered by content-blind re-organization
  — the *correctable inflation*).
- **irreducible floor** = `sharp-reference − C` (the gap honest re-organization cannot close — what
  *build-robust* must survive). Well-defined per column because each column carries its own sharp segment.
- **revives?** (binary) = `C ≥ live_bar` 0.867 `[RECONCILE]` **and** ablation collapses.

### Topology classification (the deliverable)
Over the three columns' floors:
- **`separable`** — floor ~constant across penalty regimes (cue and penalty independent; the rare clean
  case, *contra* the exp06 super-additivity prior).
- **`monotonic`** — floor rises/falls with penalty regime.
- **`sweet-spot`** — floor minimised at one regime. If that regime is `reshaped`, it is the **exp07
  target** (the reshaped tie + re-organized cue jointly minimise irreducible diffuseness).

### Penalty-legitimacy adjudication (off vs reshaped column — the measured replacement for the argued call)
- `reshaped` **≈** `off` (floor/ceiling/revival comparable) → reshaping preserves function at no cue-floor
  cost → **preserve validated.**
- `reshaped` **better** than `off` (lower floor / higher ceiling / revives where off does not) → the open
  tie *actively helps* the cue floor → **strong preserve.**
- `reshaped` **worse** than `off` → **does NOT lock the reversal on the spot.** This outcome would
  *reverse a settled design call* (preserve) on the basis of **one pinned clock-onset phasing** (§5) — so
  it gets the **higher bar**, exactly as a single-seed sub-bar reading did not flip exp06. **Trigger: a
  bounded, pre-registered clock-onset phasing re-check** (a coarse phasing sweep, `[RECONCILE]` 3–5 onsets
  spanning early→late, **not** an open-ended hunt). Then:
  - reshaped recovers to **≈/better than `off` at some phasing** → the original phasing was suboptimal →
    **preserve holds**; the reshaped column is re-read at the recovering phasing.
  - reshaped stays **worse than `off` across the whole phasing sweep** → the reversal **locks**: even
    well-phased, the tie suppresses the cue floor → **correct-it (drop) is the cleaner call**, and the
    **fixed-PAM** simplification kept on the radar is promoted. (This is the entire point of measuring the
    argued call — but a settled call only flips on the higher bar, not one phasing.)

**Liveness stays binary at the bar throughout.** The ceiling/floor magnitudes and the topology shape are
the **characterisation** output; the intrinsic/inflated split and the legitimacy call are read off them,
but every "revives" judgment is binary at `live_bar` with the ablation guard. Grades characterise; they
do not become the decision variable. **Effective-SNR is logged as a descriptor only — never the decision
variable** (re-organize *to* raise SNR and it rises by however hard you tried; the honest readout is the
channel via (d), not the SNR).

---

## 4. Pre-registered outcomes (all first-class)

- **Cue-locatability = no (Step-0b)** → intrinsic-only floor; cue-fix = **build-robust-only**; the
  correction-part is **measured empty** — *not* a two-parter. (The two-part lock still holds as "do not
  flatten to sharp"; the decompose simply measures the correction-part to be empty.) Deliverable:
  "diffuseness intrinsic, floor = deployed snr."
- **Locatability = yes, sweep runs** → full surface: topology + intrinsic/inflated split per column +
  legitimacy adjudication (§3).
- **`reshaped` worse than `off`** → **not** an on-the-spot reversal: triggers the bounded clock-onset
  phasing re-check (§3). Reversal **locks only if** reshaped stays worse across the phasing sweep — then
  preserve is overturned and fixed-PAM/correct-it promoted; otherwise preserve holds at the recovering
  phasing. Either resolution carries to the exp07 design write.
- **Cardinality corner-probe matches 16 (§1)** → 16-only validated as a *measured* call; member-count
  stays a non-lever; the full surface generalizes across cardinality.
- **Cardinality corner-probe differs qualitatively (§1)** → **member-count promoted to a third exp07
  lever**; full surface re-read with cardinality as an axis (controlled expansion, not creep — it is a
  pre-registered finding). First-class.
- **`deployed` column lifts (Step-0c fail)** → harness contradicts exp06 OR-logic; **debug, not a result.**
- **`off` sharp ≠ ~1.106 (at plateau budget) or `off` flat ≠ ~0.000 (Step-0c fail)** → sweep/stimulus
  mis-scaled or under-trained; floor reads untrustworthy; fix the harness before interpreting.
- **Any revival with non-collapsing ablation** → magnitude artifact; **rejected, never counted** (the
  guard `dgate.py` already earned).

---

## 5. The `reshaped` column — instantiation (operator-form open)

Instantiated via the **settled λ2 envelope discipline** applied to PAM's tie: opens on a clock,
**stays open.** This is the *preserve direction expressed in already-settled mechanics* — the cheapest
concrete open-tie point to read the surface against. It introduces **one coarse knob — PAM's
clock-onset** — pinned to a **single value** `[RECONCILE]` for the decompose. (Whether PAM shares the
cortex clock is a real paradigm question, but the surface needs the tie *open*, not *optimally phased*.)

**This does NOT commit exp07's final reshape to the λ2 form.** That choice stays open and is carried as an
analysis variable. The reshaped column is a **read point**, not a redesign.

---

## 6. Parameter block & `[RECONCILE]` register

### Pinned (structural)
| parameter | value |
|---|---|
| Surface | cue-sweep (flat-diffuse → content-preserving plateau → sharp-reference) × penalty `{off, reshaped, deployed}` |
| Member-count | held **deployed (16)** — not a third axis (exp06-resolved) |
| Read instrument | `dgate.py` (committed, `335f36d`); non-causal masking; carrier bounded ±0.5 all cells |
| Cue invariant | content-preserving re-posings (content-blind structural transform; ablation-invariant) |
| Decision | binary liveness at `live_bar` + ablation; floor/ceiling/topology are characterisation; SNR descriptor-only |
| Sharp segment | labeled alive-reference only — never a candidate fix |
| Provenance | every output row carries `commit_hash`, `spec_hash` |

### `[RECONCILE]` (from the exp06 commit)
| value | source |
|---|---|
| `live_bar` 0.867 / `healthy` 1.412 | exp06 clean corner |
| `off` sharp-segment reference ~1.106 | exp06 reconfirmed `[1,0,0]` (12000-step, 16-seed plateau) |
| `deployed` `pam_lam` (0.01) | exp06 deployed penalty |
| cue scales (diffuse snr ~0.086: salient ~5.83 / subtle ~0.5; sharp ~5.83) | exp06 cue construction |
| member-count 16 (= n_A·n_B) | exp06 deployed cardinality |
| `reshaped` PAM clock-onset | single pinned value for the decompose (§5) |
| clock-onset phasing sweep (reversal re-check only) | 3–5 onsets early→late, bounded (§3) |
| cardinality corner-probe point | one lower cardinality (recommend 2-member, anchored ~1.41; or 4) (§1) |
| seed count / seed-spread (plateau margin) | exp06 revival-variance calibration |
| collapse / ablation floors | exp06 |

---

## 7. The line to hold

This phase **measures**; it does not build. The cardinal guards:
- **Don't flatten the cue to sharp.** The floor read exists precisely to find what diffuse-but-structured
  must survive; sharp is the labeled cheat-reference, never the fix.
- **Penalty is not the primary lever.** Its richer design treatment reflects what's documented (λ2), not
  what matters more; the cue carries equal weight in its honest two-part shape.
- **Content-blind re-organization** is what keeps the floor from faking downward — re-posing reorganises
  presentation, never adds signal (Step-0a's ablation-invariance enforces it).
- **Operator-form stays open** — the `reshaped` column is a read point, not a commitment; exp07's final
  reshape form is an analysis variable.

The deliverable is a **surface** plus **two measured legitimacy calls**, scoping exp07's joint redesign on
the same empirical footing exp06 earned. Both legitimacy questions — settled in chat by argument — return
here as measurements; if the data overturns a lean (the `reshaped`-worse-than-`off` branch), the
measurement wins.
