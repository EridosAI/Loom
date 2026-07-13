# SCATTER-DWELL — PRE-REGISTRATION (the bracketing arm)

**Status: DRAFT (CC, 2026-07-13) — refute-default panel RAN (4 lenses): 3 MUST-FIX + 9 CONCERN, ALL
FOLDED in place (record: `exp08/scatter_prereg_panel.json`). → one commit → touch 1 (Jason ratifies).**
The three MUST-FIX were: the CONVERTS cell gated on a raw count unreachable under the expected
cal-self-converts state (catch-15 re-committed) → §4 restructured to decide on matched-bar excess +
census; a missing SIGNATURE-DIVERGENT cell → added; an unpinned R grid/sampling method breaking the G2
`==R*` bind → pinned in §2. Numeric pins (R grid, 2.0× multipliers) are candidate values Jason ratifies
at touch 1.
Promoted from the fenced scatter skeleton (scratchpad, retired) after the free-reads batch was
seat-verified PASS (`docs/FREE_READS_SURFACE.md`, 2026-07-13). This is the next arm after ORBIT-DEAD
(§10.27), per `MECHANISM_MAP_v1_2_RECONCILED.md` §3 — the **bracketing** ruling. Author: Jason Dury,
no co-author; commits on Jason's word. Nothing builds or runs before the panel and touch-1 ratification.

**Lineage.** EXP16 killed the word-side shortcut account (VISION-SIDE, §10.26). EXP17/L1 (orbit): a real
sweep — novel, smooth, **predictable** — did NOT convert *as tested*; **DIRECTION-ONLY**, no matched-bar
excess, no sustained episode (§10.27, F6-A). F6-A made ORBIT-DEAD three-way *symmetric* (A self-converts
at its own bar exactly as the orbit does) → the interleaving-is-the-gate reading is unproven. **SCATTER
tests the far end of the novelty axis: maximal per-frame novelty · zero path structure · zero
predictability · identity held.** It **brackets** (v1.2 §3): if scatter converts, the gate lives between
orbit and scatter (smoothness/predictability was protective); if scatter dies, interleaving is confirmed
with input novelty maximal and the intermediate arm is skipped.

## §0 Discipline traps (verbatim standing machinery)

**Anti-forward audit — at FULL strength, doubly on this unpredictable arm:** the operator remains masked
completion over co-present structure; no forward loss, no temporal target, no next-frame anything at any
layer. A jump-world is where a forward-predictor import is most seductive — that import is the fenced
move. **Manufacturing fence:** scatter is fabric structure (a regime probe, same class as shuffling/orbit),
never a force toward conversion; no loss/schedule/signal engineering; any target adjustment under
feasibility pressure routes to Jason with the flag stated (the EXP17 traverse-correction precedent).
**σ>0 load-bearing:** the jitter is not deleted — the pose is *resampled*. **New fabric = new regime:**
own cal, own band, calibrate-in-regime, **nothing transports — not even A's or the orbit's band.**

## §1 The arm — `exp12_dwell_scatter` (draw-parity)

Per `MECHANISM_MAP_v1_2_RECONCILED.md` §3. Generator change, minimal and single: the within-dwell pose
is **resampled per frame inside a dwell-local ball**, no path.

- **Ball center per dwell** = the repurposed onset `g_nuis` draw (the draw-parity architecture, exactly
  as the orbit repurposed it), clipped so `|center|∞ + R ≤ bound − 3·stationary_sd` (the same centering
  rule that gives the orbit zero anchor reflections; keeps every frame in the family box by construction).
- **Per frame** p∈{1..k}: `pose_p = center + uniform-in-ball(radius R)` drawn from the dedicated
  `g_sweep` substream — each frame an **independent** draw (zero path structure, zero interleaving,
  maximal per-frame novelty within the identity).
- **Draw-parity invariant (pinned, carries its own positive-delta smoke):** `g_nuis` consumption stays
  **byte-identical to A_dwell** — 1 onset draw + (k−1) step draws are still drawn (parity), the realized
  pose is the `g_sweep` ball sample; all other streams (member, mask, bg, dwell, noise) untouched →
  existing arms digit-identical, asserted.
- **Held to A_dwell:** dwell law (Geom0, mean 11), member-per-dwell (no immediate repeat), word channel,
  **mask policy including mid-dwell word grading** (EXP16 proved the shortcut isn't the gate; leaving it
  makes kinematics the only change, and its gradient stays an internal control, §5). Background pin held
  (lifts only at L3).
- **Guards:** `dwell_scatter` × {shuffled / uniform_mask / word_ref / dwell_orbit / expo_*} assert-fail.

## §2 Selection statistics — the F5 fill (NOT net/path; NO render-gain floor)

Scatter has no path; net/path is a path-only anti-revisit statistic, **explicitly not imposed** (RED_TEAM
**F5**, the floor-vacuum it flagged, filled here). Selection is on scatter's own statistics.
**Manufacturing-fence discipline (panel fix): the multipliers are PRE-NAMED here; only the baselines are
measured** — a gate-picked stringency would be a target adjustment under feasibility pressure (§0) and is
forbidden (the EXP17 pattern: pre-named 4×/2.5× contrast floors, measured baselines only). Lower walls AND
the confusion ceiling are **fabric-only, X-blind, T=100k** (the ceiling reuses the committed `cross_med`
different-object-jump bound, §2.3); the acquisition read enters ONLY as a deployment-time GUARD on the
geometric ceiling (§2.3 / §6 `acq-guard`), never a selection-time input — the fence holds because
acquisition ≠ conversion.

**Pinned candidate grid + sampling method (touch-1 ratification pins; deterministic G-select/G2 require
them, per the committed `X17_R_GRID` precedent, [[feedback_anchor_provenance]]):**
- **Ball-radius grid** `R ∈ {0.20, 0.30, 0.40, 0.50}` (pose-coordinate units; family bound 1.5, tremble
  per-step ≈0.16). *(Candidate grid — Jason ratifies/adjusts at touch 1.)*
- **Uniform-in-ball sampling (pinned method):** per frame from `g_sweep` — direction `u =
  randn(K)/‖randn(K)‖`, magnitude `R·U^(1/K)` with `U~Uniform(0,1)`, `pose = center + R·U^(1/K)·u`;
  independent per frame; fixed draw count per frame → the G2 `==R*` bind has committed-code provenance.

**Statistics (pooled AND per-seed-worst, RB-2 discipline):**
1. **Per-step displacement contrast** — median within-dwell step norm **≥ 2.0× the measured tremble
   per-step baseline** (`measure_kinematics.perstep_med` on A_dwell): the lower wall — defeats local
   satisfiability (rung 3). *(2.0× pre-named; touch-1 ratifiable.)*
2. **Distinct-pose coverage per dwell** — per-dwell realized pose spread (per-axis extent / support)
   **≥ 2.0× the tremble traverse baseline**; the read the orbit's traverse played for a path arm.
   *(2.0× pre-named; touch-1 ratifiable.)*
3. **Confusion-bound ceiling — DETERMINISTIC, committed recipe (the build gate Jason named).** The
   within-dwell per-step displacement (`perstep_med`, pooled AND per-seed-worst = max over seeds) must be
   **≤ `base["confusion"]` = the tremble cross-boundary "different-object" jump norm** (mean of per-seed
   median `cross_med` on A_dwell) — the **committed EXP17 floor-3 / R4 confusion bound**
   (`exp17_score.measure_kinematics.cross_med` → `measure_tremble_baselines["confusion"]`, reused
   VERBATIM: fabric-only, X-blind, deterministic, threads=1). Rationale: a within-dwell step as large as
   a between-object jump lets a frame be confused with a different member → correspondence breaks.
   Feasibility (measured, `exp08/scatter_select.json`): `cross_med` = **1.310** (`baselines.confusion`)
   and the grid `perstep_med` spans **0.223 (R=0.20) → 0.558 (R\*=0.50)** (`cells[].perstep_pool`), all
   ≪ the ceiling — identity-safe across the whole grid (non-binding but PINNED). ~~[superseded
   2026-07-13, method-named-figures: the pre-measurement prose literals "perstep ≈ 0.2–0.45" and
   "cross_med ≈ 1.65" were both wrong; the recipe-named measured values above govern — every gate
   consumed the measured values, so nothing operational was touched.]~~ **Acquisition contingency
   (`MECHANISM_MAP_v1_2_RECONCILED.md` §4 line 57 — the §6 `acq-guard`):** the geometric ceiling is a
   rendering-distance bound; §4 requires that IF the DEPLOYED arm degrades member acquisition, the wall
   was too loose → re-derive from the acquisition read. So the deployed-horizon pre-check / G2 carries an
   acquisition-degradation guard: if scatter's member acquisition falls below the tremble baseline by
   more than a **pre-named 10% margin**, HALT + re-derive the ceiling from the acquisition read. The
   acquisition read is thus the FALSIFIER of the geometric ceiling, not a selection-time input — exactly
   as §4 specifies. **Reachability (recon fix):** the ceiling is non-binding because the box-containment
   rule `cl = bound − R − 3·stat_sd > 0` (⇒ R < 1.125) already caps in-box per-step below `C_ceil`; that
   `cl>0` assert (generator, fires at R ≥ 1.125) is the actual binding upper wall. The confusion-ceiling
   predicate (`perstep_med ≤ C_ceil`) is kept as the identity-correspondence check, and its reachable,
   non-tautological falsifier is a **planted `perstep > C_ceil`** driven through `_cell_feasible_scatter`
   (scorer smoke; a smaller planted value passes). The `acq-guard` metric is **`sep_cat`**
   (member-category separation) COMPUTED from the deployed verdict columns, read on the SAME seeds/window
   as the tremble baseline (matched-bar companion — F6-A rule (i)); scatter `sep_cat` < 0.90 × A_dwell
   `sep_cat` → HALT + re-derive.
4. **NO render-gain floor.** Free-read **(i)** measured the pose→render map an isometry (isotropic to f32
   precision; `nuis_axes ← basis @ Q.t()`, Q QR-orthogonal, `conflict_stream.py:59`) — a random ball
   direction is not perceptually weak, so ball sampling carries **no** gain floor. *(Source: read (i) /
   seat ruling 2026-07-13 — NOT RED_TEAM F5, which is silent on render-gain.)*

**Selection (lexicographic over the pinned grid, committed-measurer-computed at G-select):** measure the
tremble baselines; over `R ∈ grid` keep those clearing walls 1+2 under ceiling 3 (pooled AND
per-seed-worst); pick **max per-step contrast**, tie-break toward the **confusion margin** (identity
safety outranks extra displacement — attribution stakes). R FROZEN + recorded with measured kinematics.
Envelope: no R clears the walls under the ceiling → **HALT** (geometry conflict routes to design).

## §3 Seeds / horizon (verbatim)

Cal {20,21,22,24,25}; verdict {0–7}; EXT {8,9}; substitution {10–19}. `h_max=1M` (fabric build, probe
windows [0, stream.T−W], G1a/G1b) for **every** run — unchanged. mid-ckpt 500k.
**Single referent everywhere: the [0,500k) column prefix** (F13) — primary frozen at 500k; the tail is
descriptive only. Determinism: `torch.set_num_threads(1)`.

**HORIZON AMENDMENT (Jason ratified, 2026-07-13, ratification-class, pre-data; F13-primary UNTOUCHED).**
The 1M *training* horizon is not load-bearing: F13 already freezes the primary at [0,500k), and the 14
committed EXP14 B/C/D converters all converted well before 500k. Only the **training** horizon moves,
via the existing `read_at` parameter (no new flag/code/smoke — smoke (9) already proves the
run-to-2N/read-at-N prefix digit-exact). **Intended training horizons:** cal {20,21,22,24,25} · verdict
{4,5,6,7} · EXT {8,9} → **`read_at=500k`**; the pre-named **blind tail** seeds verdict {0,1,2,3} →
`read_at=1M`. Full runs from the start; **no checkpoint-resume anywhere** (so the resume-exactness
question is moot and drops). **Escalation (pre-named, outcome-blind):** if any tail band-touch fires at
the committed detector in (500k,1M] on {0,1,2,3}, the remaining eleven re-run at `read_at=1M` before the
terminal.

**Tail hazard pin (F6-A species — §4/terminal template):** the tail (500k,1M] is **descriptive-only and
NEVER enters a cross-arm comparison**; scatter's tail n differs from A's / the orbit's (n=8–10 at 1M).
**Every cross-arm read is [0,500k) for every arm** (matched-bar, census, Fisher) — the tail is reported
per-arm, never like-barred across arms.

**Grounds (fact-checked 2026-07-13 by CC from `exp08/exp14_2x2_verdict_verdict.json`, field
`cells[B_12bc_dwp,C_shuffle,D_split].per_seed[].conversion_onset`, non-null):** 14 converters
(B 2,4,5,6,7 · C 0,2,4,5,6 · D 0,1,3,6; A 0/8) with conversion-onset **min 19,200 / median 161,250 /
max 427,500 — 14/14 < 500k**. *[Method-named median (provenance ratified by Jason 2026-07-13): the two
middle sorted onsets are **150,300** and **172,200**, so the even-n median (**two-middle mean**) is
**161,250 exactly** — an
exact half-step, because onsets sit on the 300-step eval grid. Prior canon "161.2k" was NOT an error but
an UNDER-display: `f"{161.25:.1f}"` → `161.2` (round-half-even on the exact .25). The relay's earlier
"172.2k" was the UPPER median (sorted[7]), a distinct statistic. min/max/n/all-<500k reproduce exactly.]* Horizon-independence of the step path
confirmed at code level AND empirically (h_max=N vs 2N → bit-identical params + Adam optimizer state +
trajectory): gain(t), lam1/lam2(t), `_pam_penalty`, and the Adam LR all key on the **absolute step index**
with fixed breakpoints — none on total horizon.

**Execution reconciliation (corridor, 2026-07-13):** this amendment landed while cal (G3) had already
completed at 1M and G5 (verdict/EXT) was ~60% into its 1M runs. By prefix-invariance the [0,500k) content
is identical at any `read_at`, and **restarting the in-flight runs at 500k would cost MORE compute than
finishing** (≈7M vs ≈4M remaining steps) — defeating the amendment's own savings. So the in-flight runs
were allowed to **finish at 1M**; the **finding uses [0,500k) for every cross-arm read** (fully
amendment-compliant), all seeds carry a descriptive tail (the blind-on-4 + escalation is thereby moot),
and the primary is untouched. The `read_at` split stands as the ratified design for any re-run.

## §4 Outcome cells — matched-bar excess + certified census DECIDE; counts are context; cal-self-converts EXPECTED

**The F6-A discipline is the spine** (the two standing rules born at the EXP17 close, verbatim): **(i)
cross-arm companions/context rows must be MATCHED-BAR — one detector (band, N) read through both arms;
unlike-bar counts are context-only, never evidence, never gated or attributed on (catch-ledger 16); (ii)
provenance/referent strings are COMPUTED from the data they describe, never asserted in a branch
(catch-ledger 15/16 family).**

**The decision runs on two PRIMARY axes, NOT on the raw count** (the catch-15 lesson, folded from the
panel: under the *expected* cal-self-converts → non-loadable state the formal count rung is UNREACHABLE —
F5 precedence loadable→floor_clean→n≥8→count — so the finding must not hang off it):
- **Axis 1 — matched-bar excess.** A scatter-vs-A (and scatter-vs-orbit) excess that SURVIVES at a
  **common detector** (`tools/verify_toolkit.py:matched_bar_tab`, per-detector fr stated; record-anchored
  + perturbation falsifier). *The exact test the orbit FAILED.*
- **Axis 2 — signature census.** Per-seed longest post-acq episode vs **SIG_DEPTH = 8** (DEPTH-decisive,
  certifies alone; SIG_RECUR=2 corroborative only — the F7 rule). Self-audit: observed certified count
  EXCEEDS the dual-null ≥SIG_DEPTH bracket (AMD-13 on the census). Bare-N geometry check: own band N <
  SIG_DEPTH else judgment-class HALT (§10.25.3).

**The formal count partition is SECONDARY context.** cal-self-converts is the EXPECTED cell (pre-named):
the scatter cal is *expected* non-loadable exactly as A and the orbit were → **DIRECTION-ONLY is the
expected formal LABEL, and it is NOT the finding.** Ruling-B on cal-converts (own between-episode null;
referent COMPUTED from the record, never asserted). Raw crossing counts / Fisher vs A_dwell **0/8**
(committed) and vs orbit are **context-only — matched-bar or nothing, never gated or attributed on.**

**Named cells (every reachable outcome; the two axes decide, counts route):**
- **SCATTER CONVERTS (paradigm positive)** — Axis-1 matched-bar excess SURVIVES at a common detector
  **AND** Axis-2 census certifies (≥5 of READ n≥8 with longest ≥ SIG_DEPTH). **PER-FRAME NOVELTY SUFFICES
  — smoothness/predictability was protective; interleaving exonerated.** *Independent of the formal count
  rung (expected non-loadable) — the positive rides Axes 1–2, never the raw count (catch-15 fix).*
  Triggers the **two-wall window law** [MEASURED-conditional], HAND-HELD (`EXP_L2_HANDHELD_PREREG.md`, F2
  fixed at its prereg), and — before any paradigm-positive certifies at touch 3 — the
  **interior-concentration / centering control** at the scatter arm's realized center distribution
  (EXP16 precedent).
- **SCATTER DEAD** — no surviving matched-bar excess **AND** census 0 (no certified episode): the orbit's
  exact outcome at the novelty far-end → **INTERLEAVING IS THE GATE, hard** → the **dwell-length
  titration** (onset-rate knob) measures the interleaving dose; mechanism-class arms unlock in order
  (replay first, then CWP vs the replay bar).
- **SIGNATURE-DIVERGENT** — a loadable-world split or an Axis-1/Axis-2 disagreement: **raw ≥5 ∧ certified
  ∈ {1..4}**, or matched-bar excess without census (or census without excess) → **routes** (the
  formal/certified divergence guard; EXP17 EDGE-5 made pre-named).
- **DIRECTION-ONLY (expected formal label)** — cal-converts → non-loadable formal cell; the FINDING is
  decided by Axes 1–2, not this label. Direction-only + §5 companions.
- **Raw {1..4}/8 (context)** → EXT {8,9} fires first (D1: UNREAD substitution first; certifiable cells
  need READ n≥8); post-EXT **the two axes re-decide.** ~~The certified-0 route (→ DEAD /
  SIGNATURE-DIVERGENT) is restricted to raw ≥5 post-EXT, so it never collides with the EXT route.~~
  **[STRUCK — marked amendment, Jason ruled 2026-07-13 (G7 judgment-class), ledger catch 18.** The
  "raw ≥5 post-EXT" restriction **contradicts §4's ratified two-axes spine** (DEAD = no surviving
  matched-bar excess ∧ census 0, which carries NO raw condition) and **reintroduces raw-gating — a
  catch-15 species.** Grounds: the committed scorer (`_primary_finding`) decides DEAD raw-agnostically
  and smoke **sc4 asserts it pre-data** (F4-A: committed code is the executable recipe, it governs over
  conflicting prose); **raw sits inside the floor-audit's own phantom bracket [0, 3.13]**, so a raw≥5
  gate is a floor on noise, not signal; and EXP16's UNDERPOWERED is a count-rung terminal that does not
  transport to a two-axis regime (nothing transports). The two axes govern at every raw; raw is SECONDARY
  context only.]**
- **Liveness < 3/5** → HALT (unposed). **Floor-flagged** → bracket + census ride to terminal,
  NOT-CERTIFIABLE-by-count.

## §5 Companions (reported, never gated) — incl. the four free-reads as non-gating pointers

1. **Gradient-persistence internal control:** recency Δ(p1 − p13-48), post-acq method-named recipe;
   shortcut intact → should persist ≈ A's +0.1416; collapse = instrument alarm (flagged).
2. Baseline-shift vs A and vs orbit (the borrow-gate diagnostic; matched-bar only).
3. Acquisition-onset distribution; cortex-side diversity echo (`div_nuis`/`d2_spread`) vs the forensic gap.
4. Realized scatter kinematics from the actual run fabric (must match the frozen-R build targets — assert).
5. 1M tail, descriptive.
6. **Free-reads pointers (seat-verified 2026-07-13, `FREE_READS_SURFACE.md`; non-gating):**
   (i) **render-gain** = isotropic → **no gain floor** (folded into §2.4);
   (ii) **CWP step-0** premise-consistent → the CWP program stays open at its pre-named place *behind the
   ladder* (does not gate scatter);
   (iii) **rung-3.5** latent (background carries no member info) → L3 designs as a generalization-pressure
   arm (does not gate scatter);
   (iv) **EXP13** kinematic-indicated (lawful np11 0.624 vs scramble 0.087), bridge holds (seat ruling);
   EXP13 stays PAUSED behind the ladder. *[CC inference, non-gating: the lawful wall is plausibly the
   same gate ORBIT-DEAD hit and likely priced in by scatter's answer — not a seat ruling.]*

## §6 Build + gate-executor table (every gate names its executor + a reachable falsifier BEFORE the corridor opens)

Deliverables (mirroring the orbit build): the `exp12_dwell_scatter` generator delta in `build_fabric`
(ball-resample, dedicated `g_sweep`, draw-parity) + `cal_read_scatter` (own provisional band §10.22,
borrow-gate diagnostic-only, cal-converts → Ruling-B) + guarded `score_scatter` (refuses until cal-read
exists ∧ not HALTED ∧ all {0–7}+EXT records exist; matched-bar + census PRIMARY, counts SECONDARY) +
the R-selector. Pre-delta smoke refs captured from clean code FIRST.

Every row names its executor + a positive-delta **smoke ID** (CORRIDOR_PROTOCOL:94 makes these mandatory
for the pre-flight gate-executor audit; the EXP17 `sm-G2-lex`/`sm-G4-*`/`sm-G6-*` precedent):

| gate | executor | smoke ID · reachable falsifier (fails under a no-op) |
|------|----------|------------------------------------------------------|
| G-select (R freeze) | R-selector (fabric-only, T=100k) | **sm-select-R0**: F5 floors cleared at frozen R; **FAIL under R=0** (uniform-ball(0) → pose≡center → zero within-dwell displacement → floor-1 fails) |
| build invariants | generator delta | **sm-parity**: scatter vs A same seed — dwell_id/pos/member/mask IDENTICAL, `nuis` DIFFERS; `g_nuis` byte-identical (**FAIL on stream-desync**, incl. "optimizing away" the discarded tremble draw); existing arms digit-identical; guards fire on illegal combos |
| box (upper wall) | generator `cl>0` assert | **sm-box**: `cl = bound − R − 3·stat_sd > 0` (R < 1.125) — the binding upper wall; **FIRES** on a canonical R ≥ 1.125 |
| ceiling | `_cell_feasible_scatter` (reuses `measure_tremble_baselines["confusion"]` = committed `cross_med`) | **sm-ceiling**: `perstep_med` (pooled + per-seed-max) ≤ `C_ceil`; reachable falsifier = a **planted `perstep > C_ceil` → cell infeasible** (a smaller planted value passes; non-tautological); at grid R `perstep_med` **0.223–0.558** ≪ `C_ceil` **1.310** (measured, `scatter_select.json`; non-binding, identity-safe) |
| acq-guard | deployed-horizon pre-check / G2 | **sm-acqguard**: deployed scatter `sep_cat` ≥ 0.90 × A_dwell `sep_cat` (matched seeds/window); **FAIL → HALT + re-derive the ceiling from the acquisition read** (MECHANISM_MAP §4 l.57) — the geometric ceiling's contingent falsifier |
| G1a/G1b | `run_exp14_arm` (class-aware pre-check @1M) | **sm-G1**: REUSED A {0–7} = replay divergence HALT; FRESH scatter cal/verdict/EXT, subst {10–19} |
| G2 | R-verify | **sm-G2-lex**: re-derive R over the pinned grid, assert `==R*` (digit-exact, committed-code provenance), F5 targets hold on deployed 1M all seeds |
| G3/G5 | `run_exp14_arm` | **sm-G3G5**: cal ×5, verdict ×8 + EXT ×2 @1M, mid-ckpt 500k; spec_hash parity |
| G4 | `cal_read_scatter` | **sm-G4-cal**: liveness ≥3/5 else HALT; α-uncuttable; band N<SIG_DEPTH; cal-converts → non-loadable (referent computed) |
| G6 | `score_scatter` | **sm-G6-mb** matched-bar tab (`matched_bar_tab`, record-anchored + perturbation falsifier); **sm-G6-census** DEPTH-decisive + self-audit; **sm-G6-guard** DRAFT refuses with any record absent |
| G7 | refute-default panel | **sm-G7**: no lens assumes conversion; no lens assumes the scatter story; MUST-FIX/judgment-class → HALT |
| G8 | consolidate + push | **sm-G8**: terminal surface = DRAFT + gate log + matched-bar tabs + bare-N census + companions |

The scorer smoke exercises planted terminals: CONVERTS (matched-bar excess + certified census) ×
SIGNATURE-DIVERGENT × DEAD (census 0) × cal-converts branch × EXT-fire under D1 — every assert dies under
a no-op.

Adversarial code review before the build commit (the orbit review caught a blocking bug).

## §7 Corridor

`CORRIDOR_PROTOCOL.md` governs (three touches; gate-executor audit at pre-flight). **Pre-flight package
(touch 2), items (a)–(e):** (a) ratified texts verbatim (§4 cells + the two F6-A rules + the
interior-concentration control + the R recipe/formula); (b) every constant with formula + value (R*,
band α, floors, census constants, the pre-named multipliers 2.0×/2.0×); (c) the **G-select / G1a / G1b /
G2 pre-check outcomes** with any substitutions and rule citations; (d) the gate-executor table (every
gate → executor + smoke ID) + the halt list; (e) the CORRIDOR_PROTOCOL instance note. Then unattended
G1→G8 → terminal → design-seat verification → **Jason's attribution (touch 3)**. SWEEP-CONVERTS triggers
the pre-named interior-concentration control before any paradigm-positive certifies.

---

**Plain language.** The orbit moved smoothly and never surprised the learner, and it didn't convert —
but we couldn't prove *why* (dose, predictability, or interleaving). Scatter is the opposite extreme: the
same object shown in random jumps within arm's reach — maximum newness, no path at all. If it teaches,
smoothness was the trap and the hand-held world tells us which half; if even random jumps fail, the
learner needs alternation between *different things* and we measure how much. Every bar was set before its
data existed, the loads are matched-bar and census (not raw counts), and cal-self-converting is expected,
not a surprise — the real question is whether a matched-bar excess survives at a common detector, which is
exactly the test the orbit failed.
