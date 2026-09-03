# EXP17 — TERMINAL SURFACE (orbit; DRAFT, no attribution)

**Status: corridor CLOSED clean (G1→G8, 2026-07-12). This is the DRAFT terminal — it routes FIRST
to the independent design-seat verification from raw committed artifacts (touch-3 prep, not
optional), THEN to Jason for attribution + canon §10.27 (touch 3). No attribution is asserted here.**
Arm `exp12_dwell_orbit`, frozen (r,ω)=(0.85, 18°). Author Jason Dury, no co-author. One code path,
spec_hash `41d6f0d5e7da` across all 20 scored records.

---

## ⚠ SUPERSEDED IN PART BY F6-A (Jason ratified, 2026-07-12) — matched-bar correction

The formal cell (DIRECTION-ONLY) is **unchanged**. But the "excess over A" framing below was an
**unlike-bar comparison** and is corrected here (supersede-don't-overwrite; the original text is
struck in place with a `[→F6-A]` pointer, retained not deleted).

**The error.** The Fisher row (k=5/8 vs A 0/8, p=0.013) compared the orbit at *its* detector
(0.6129, N=3) against A at *A's* detector (0.6111, N=4) — a **detector mismatch** (N=3 vs N=4; false
rates 0.000964 vs 0.000439, a 2.2× difference). Counts at different detectors are not comparable.
The Fisher row is **SUPERSEDED** and replaced by:

**Both detectors × both arms** (verdict {0–7}, post-acq, [0,500k); fresh-code reproduction,
fact-check clean — the harness was not ported):

| detector (band × N) | false rate | ORBIT | A_dwell | Fisher (orbit ≥ A) |
|---|---|---|---|---|
| A-bar 0.6111 × 4 | 0.000439 | 1/8 [1] | 0/8 | p = 0.50 |
| orbit-bar 0.6129 × 3 | 0.000964 | 5/8 [1,2,5,6,7] | **3/8 [3,5,6]** | p = 0.31 |

Longest runs (identical at both bars): orbit [2,4,3,2,2,3,3,3], A [2,2,2,3,2,3,3,2].

**What survives, what does not.** The **unshifted onset marginal survives** (Δ0.0011, borrow-diag —
lens-4 was right about that). The **"genuine excess over A" does NOT survive bar-matching**: at a
common bar the orbit is statistically indistinguishable from tremble in brief-excursion rate
(p=0.50 / 0.31), and A_dwell itself crosses 3/8 at the orbit bar. **Every "well above A's 0/8"
phrase in this document is struck.**

**Neutral summary** (replaces the "not a null" framing): *at a common bar the orbit is
indistinguishable from tremble in brief-excursion rate, and neither arm sustains anything — max run
4 vs 3 against a converter reference of ≥36.*

**Reading-frame reconciliation (v1.2 §2).** The "ORBIT-DEAD three-way-ambiguous" ambiguity
**collapses toward orbit ≈ tremble at a common bar** — there is no matched-bar signal to attribute
to dose or to predictability. What remains open is the pre-registered question itself: per-frame
novelty within a persistent identity did not convert *as tested*; whether a different regime would
is the banked next step (dwell-length titration; the disambiguation ladder).

**Asymmetry (to canon §10.27).** A_dwell self-converts **3/5 at its own detector [20,21,24]**
(committed `per_cal_seed_converters`), exactly as the orbit self-converts 3/5 at its own. Under
EXP17's symmetric cal-converts rule A would be non-loadable too — so **DIRECTION-ONLY is a property
of low-N band geometry + the rule, not of the orbit.**

---

## The result — DIRECTION-ONLY (routes)

The moving-anchor orbit produced ~~**alpha-significant brief band-crossings well above A**~~
`[→F6-A: struck — no matched-bar excess; orbit ≈ tremble at a common bar]`, at an
essentially unshifted onset marginal, with ZERO sustained/certified conversions — under
self-converting calibration that blocks a clean count vs A. In the pre-registered cells this is
the **ORBIT-DEAD direction** (0 certified after the signature census), delivered **direction-only**
because the calibration seeds themselves cross (Ruling-B → non-loadable).

| quantity | value | recipe / note |
|---|---|---|
| terminal | **DIRECTION-ONLY**, routes | `loadable=False` (cal-converts Ruling-B) dominates F5 precedence |
| raw band-crossers | **5 / 8** verdict seeds [1,2,5,6,7] | own recut band 0.6129, N=3, [0,500k); all 8 READ |
| **certified conversions** | **0 / 8** | signature census: longest post-acq episode ≥ SIG_DEPTH=8; observed longest {s1:4, s2:3, s5:3, s6:3, s7:3} — all bare-N-isolated |
| ~~Fisher vs A (0/8)~~ `[→F6-A: SUPERSEDED, detector mismatch]` | ~~k=5/8, p=0.01282~~ → matched-bar 0.6129×3: orbit 5/8 vs **A 3/8**, p=0.31 | see the F6-A both-bars table above |
| onset marginal shift | band 0.6129 vs A's 0.6111, **mean-shift 0.0011** | marginal did NOT shift up (not a band-shift artifact); this survives F6-A. The crossing COUNT is not matched-bar excess — see the F6-A block |
| calibration | **3 / 5 converters** [20,21,25] | brief N=3 crossings (none sustained s0-class) → Ruling-B recut, non-loadable |
| α-uncuttable | fr **0.000964** ≤ α 1e-3 | on the recut band; cleared (see caveat 2) |
| floor-clean | TRUE | structural (see caveat 3); census is the decisive guard |
| EXT {8,9} | not fired (k=5 ≥ 5); both READ | D1 substitution had nothing to act on (all 8 READ) |

**Implementation-independent.** Two separate implementations agree digit-exact: the harness scorer
(`exp17_score.py`) and the design seat's `tools/verify_toolkit.py` (stdlib, written from the prereg,
never importing the harness) both return raw [1,2,5,6,7]/k=5, certified 0, cal [20,21,25], Fisher
p=0.01282.

---

## Reading frame (pre-named — `MECHANISM_MAP_v1_2_RECONCILED.md` §2)

The banked v1.2 map amends the old v1.0 "ORBIT DEAD → interleaving is the gate" reading. **ORBIT DEAD
is THREE-WAY AMBIGUOUS** and the interleaving reading is provisional pending the §3 disambiguation:

- **(a) dose insufficient** — per-frame novelty at the orbit is only ~1.4× the noise floor (deployed
  per-step median 0.2261 = 1.42× the 0.1596 floor; freeze artifact), a regime a weight-drift learner
  may still exploit;
- **(b) predictability protective** — a constant-ω orbit is a linear recurrence (exactly
  extrapolable, rung 3′);
- **(c) identity-interleaving required** — the M3-pair reading.

~~This terminal adds texture the clean "DEAD" cell does not carry: the orbit is **not a null** — it
raises brief crossings to alpha-significance over A (5/8 vs 0/8, p=0.013) at an unshifted marginal —
but **nothing sustains**.~~ `[→F6-A: struck. At a common bar there is NO excess over A (p=0.50/0.31;
A crosses 3/8 at the orbit bar); the ambiguity collapses toward orbit ≈ tremble. What survives:
unshifted marginal, and nothing sustains in either arm.]` Which reading the (unchanged) formal cell
supports is **Jason's attribution at touch 3**, ratified below, not asserted by the corridor. The pre-named disambiguator is **SCATTER-DWELL first** (v1.2 §3: brackets the gate
— maximal per-frame novelty, zero path, zero interleaving), with the interior-concentration control
pre-named on any positive (RB-2 rider b).

---

## Gate log (full; every gate + executor + outcome)

| gate | executor | outcome |
|---|---|---|
| F4-A anchor | `anchor_assert` | re-based on the committed measurer (ratification-class amendment); `--anchor` digit-exact ×3; `exp17_anchor_rebase.json` |
| G2-select | `select_orbit` | lexicographic → **(0.85, 18°)** clip ±0.275; 24/36 feasible; sole feasible r=0.85 cell |
| G2-verify | `g2_verify` | replay == frozen; all 3 floors + zero-anchor on 15 deployed 1M fabrics [0,500k); W1 rider 0.0228; `exp17_orbit_freeze.json` |
| G1a | `precheck_fabric` (reused A {0–7} @1M) | **8/8 PASS**, halt-and-audit class, no divergence |
| G1b | `precheck_fabric` (fresh orbit 15 @1M) | **15/15 PASS**, 0 substitutions |
| (touch-2 annex) | `exp17_annex_sweep.py` | fabric-only kinematics sweep — both halt-class clean; see `EXP17_PREFLIGHT_ANNEX.md` (+ G8 supersede annotation) |
| G3 | `run_exp14_arm` ×5 cal @1M | done; spec_hash parity |
| G4 | `cal_read_exp17` | **PROCEED** (no fence): liveness 5/5; α-uncuttable fr 0.000964 ≤ α on recut band 0.6129; band N=3 < 8 (census discriminates); gradient median Δ 0.154, no alarm. Riders: cal-converts 3/5 → Ruling-B non-loadable; null-pool advisory (n_null 6225 < 6532) |
| G5 | `run_exp14_arm` ×8 verdict + ×2 EXT @1M | done; spec_hash parity; all 8 verdict READ |
| G6 | `score_exp17` | DIRECTION-ONLY DRAFT (above) |
| G7 | refute-default panel (5 lenses) | **4 CLEAN + 1 CONCERN; no MUST-FIX** — DRAFT survives; `exp17_g7_panel.json` |
| G8 | consolidate + push | this surface + panel + raw records + DRAFT artifact |

**Halt list — none tripped in-corridor.** (Liveness, α-uncuttable, band-geometry N≥8, census-refuse,
formal/certified divergence, SIGNATURE-DIVERGENT, SWEEP-DEAD-assert, EXT-target, replay divergence,
§5.5 kinematics-assert, F4-A anchor drift — all clear.)

---

## Companions (reported, never gated)

- **Gradient-persistence internal control INTACT** — verdict per-seed Δ 0.079–0.236 (pooled ~0.15),
  referent A +0.1416, alarm 0.0708 → no alarm. Confirms the fabric is A_dwell-identical except
  kinematics (the shortcut is present by design, not the driver); empirically decoupled from
  crossing (s4 no-cross Δ0.120 vs s5 cross Δ0.236).
- **σ>0 realized** — deployed np11 0.587 = 4.05× tremble, tr11 0.238, driven/undriven extents
  0.307/0.075, zero anchor reflections, zero pose-clips across 15×1M. The arm is a genuine orbit,
  not a collapsed tremble.
- **1M tail (descriptive)** — 2 seeds (s0, s3) first-cross only in (500k,1M], both bare-N
  (longest ≤3); outside the 500k primary. No sustained conversion emerges in the tail.
- **C_shuffle context** — 5/8 {0,2,4,5,6} @ 0.64×5 (own shifted null; descriptive row).
- **Null-pool advisory** — n_null 6225 < 6532 precedent floor (F14 advisory; routes to human,
  never gates; the α-uncuttable fallback is the decisive HALT-equivalent, and it cleared).

## Bare-N census (required in the terminal package)

| seed | crosses band | longest post-acq episode | n_episodes | signature | certified |
|---:|:--:|---:|---:|---|:--:|
| 0 | no | 0 | 0 | — | — |
| 1 | yes | 4 | 1 | bare-N-isolated | no |
| 2 | yes | 3 | 1 | bare-N-isolated | no |
| 3 | no | 0 | 0 | — | — |
| 4 | no | 0 | 0 | — | — |
| 5 | yes | 3 | 1 | bare-N-isolated | no |
| 6 | yes | 3 | 1 | bare-N-isolated | no |
| 7 | yes | 3 | 1 | bare-N-isolated | no |

Geometry check: recut band N=3 < SIG_DEPTH=8 (bare-N regime — the census discriminates, no
judgment-class HALT). Robustness: the band would have to fall to **0.52** (from 0.6129) before any
seed's longest episode reaches 8 — far into alpha-catastrophic territory.

## Transparency caveats (from the G7 panel — for the touch-3 reader)

1. **`formal_vs_certified_disagree=FALSE` is vacuous** under `loadable=False` (both `_partition17`
   calls short-circuit before reading counts). Do **not** read it as "count and census agree" — the
   real, stark split is **5 raw crossers vs 0 certified**, surfaced above and in `floor_audit`.
2. **α "cleared" is one-hit-fragile at the SELECTED band** (fr 0.000964; a 7th hit → 0.001125 > α).
   The robustness lives in the `_joint_band_cut` fallback ladder (the next band clears at 1.6e-4),
   not in the 3.58% margin — and this band feeds only the non-loadable direction-only counts, so it
   cannot flip the terminal.
3. **`floor_clean=TRUE` is a disclosed structural tautology** (the self-excluded null cannot host a
   ≥N run ≥band by construction). The **census** (depth ≥8), not the floor arithmetic, is the
   decisive phantom guard here; the honest pessimistic read is P_contaminated=0.752 (the 5 crossings
   are fully consistent with phantoms) **plus** the census certifying nothing.
4. **The substance** `[→F6-A corrected]`: the **unshifted marginal survives** (Δ0.0011,
   borrow-diag), but ~~the crossings are genuine excess over A~~ **the "excess over A" does NOT
   survive bar-matching** — at a common bar the orbit matches tremble (p=0.50/0.31) and A crosses
   3/8 at the orbit bar. Direction-only is the honest routing of "no matched-bar excess, no
   sustained conversion, under self-converting calibration that is symmetric with A."

---

## Next (not part of this corridor)

1. **Design-seat verification** (touch-3 prep): re-derive this terminal from the pushed raw
   artifacts at full depth using `tools/verify_toolkit.py` (the toolkit already agrees digit-exact
   on the load-bearing reads). Not optional — it is the seat's contribution.
2. **Jason's attribution + canon §10.27** (touch 3): rule which reading the direction supports
   (dose / predictability / interleaving / transient-non-consolidation), on his word only.
3. **Pre-named follow-ups** (banked, triggered by the reading): SCATTER-DWELL bracket (v1.2 §3);
   the CWP step-0 update-pressure diagnostic and the render-gain audit are now computable from the
   committed checkpoints/fabric.
