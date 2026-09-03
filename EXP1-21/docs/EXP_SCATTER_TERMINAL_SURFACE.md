# SCATTER-DWELL — TERMINAL SURFACE (G8, DRAFT — no attribution)

**Status: TERMINAL DRAFT (corridor G8, 2026-07-13). NO ATTRIBUTION — attribution is touch 3 (Jason's),
from an independent verification of the pushed artifacts.** Prereg `docs/EXP_SCATTER_DWELL_PREREG.md`;
build `24dd0e3`; pre-flight `b443a6e`; corridor commits `3b9627f` (G3/G4) · `ec8121a` (§3 horizon
amendment) · `9b08558` (G5/G6) · this CLOSE. Author: Jason Dury, no co-author.

> **G7 judgment-class RULED (Jason, 2026-07-13): terminal = SCATTER DEAD.** The refute-panel surfaced a
> real DEAD-vs-UNDERPOWERED label tension (raw=2/10 bare-N); Jason ruled **DEAD** on grounds: (1) the
> committed scorer returned DEAD and smoke **sc4 (committed pre-data) asserts DEAD is raw-agnostic** —
> **F4-A gives committed code precedence over the conflicting §4 prose**; (2) **raw=2 sits INSIDE the
> floor-audit's own phantom bracket [0, 3.13]**, so a raw≥5 gate is a floor on NOISE; (3) EXP16's
> UNDERPOWERED is a **count-rung** terminal that does NOT transport to the two-axis regime
> (calibrate-in-regime; nothing transports). The raw≥5 restriction is STRUCK as a marked §4 amendment
> (catch-15 species: raw-gating; **ledger catch 18**). The negative's strength is stated quantitatively
> below (the claim rests on numbers, not a one-word cell).

## Finding: **SCATTER DEAD** *(G7 judgment-class ruled by Jason 2026-07-13; DRAFT — no attribution, touch 3)*

**Strength of the negative (quantitative):** certified **0/8** on the decisive axis, against a
converting-fabric paradigm (EXP14 B/C/D) that converts **58% of seeds** (14/24) → **p(0/8) = 0.0009**
(binomial); the conservative certified-vs-certified companion (paradigm certifies 9/24 = 37.5%) gives
**p = 0.023** — both significant. The two brief crossers sit **inside the floor-audit phantom bracket
[0, 3.13]** (raw=2 is noise-floor, not signal). **No matched-bar excess at any of three detectors**
(below). Max episode **4 vs ≥36** for a real converter. The negative is a *powered* null, not an absence
of data.

At the **far end of the novelty axis** — maximal per-frame novelty, zero path structure, zero
predictability, identity held (R\*=0.50 uniform-in-ball resample) — the learner **did not convert**. The
two PRIMARY axes (matched-bar excess + certified census, [0,500k) for every arm) both read null:
- **Axis-1 — matched-bar excess: DOES NOT SURVIVE.** Both detectors × both arms: common detector
  **0.6129×4 → scatter 2/8 [1,6] vs A_dwell 0/8, Fisher p=0.2333**; A-bar **0.6111×4 → scatter 2/8 vs
  A 0/8, p=0.2333**. No excess over tremble at any common detector.
- **Axis-2 — certified census: 0.** Per-seed longest post-acq ≥band run: **[2,4,3,3,2,3,4,3,3,3]**,
  **max = 4 < SIG_DEPTH 8** — nothing sustains. Crossers (longest ≥ N=4): {1,6}.

No surviving excess ∧ census 0 → **SCATTER DEAD**. This is the orbit's outcome (§10.27) reproduced at the
*opposite* extreme of the novelty axis. **At MATCHED geometry (F6-A / catch-16 — no unlike-bar gloss):**
at every arm's own detector scatter **≥** orbit **≥** A in brief crossers (0.6129×4: **2/1/0**; 0.6111×4:
**2/1/0**; 0.6129×3: **6/5/3** = scatter/orbit/A), and all three are **identical on the decisive axis —
certified 0, max episode 4 (scatter) / 4 (orbit) / 3 (A) vs ≥36 for a real converter.** The three arms
are indistinguishable on brief crossings (low-N band geometry) and equally null on conversion: **the
novelty axis is inert end to end.**

*[Correction, seat catch pre-panel 2026-07-13 — catch-ledger: the earlier draft's "deader than the orbit
— fewer brief crossers (2/8) than the orbit (5/8)" was an UNLIKE-BAR comparison (scatter@N=4 vs
orbit@N=3, catch-16 species) and is struck; at matched geometry scatter ≥ orbit at every detector.]*

**Reading frame (v1.2 §3, reserved for touch 3):** SCATTER DEAD brackets — novelty-within-identity is
insufficient at *both* ends of the axis (smooth orbit and jumping scatter), which points to
**interleaving as the gate**, with the **dwell-length titration** the pre-named next knob (onset-rate).
*Attribution is Jason's at touch 3; the draft records the shape only.*

## Gate log

| gate | outcome |
|---|---|
| G-select | R\*=0.50 (sole feasible; coverage floor 2.0×tr11 binds); frozen, drift-asserted, deterministic double-run |
| G1a/G1b/G2 | deployed-1M pre-check ALL PASS, no substitutions (perlag/k/schedule/bg/cap + zero-box-exit; A no replay divergence; F5 floors hold @1M) |
| G3 | cal ×5 @1M, liveness **5/5** |
| G4 | `cal_read_scatter`: band **0.6129×4**, fr 0.000287 ≤ α; cal-converts **{20,21}** → Ruling-B non-loadable → **DIRECTION-ONLY** (expected formal label); N=4<8 census discriminates |
| G5 | verdict ×8 + EXT ×2 @1M, all acquired (onset min 3k / median 130.2k / max 183k) |
| G6 | `score_scatter` DRAFT → **SCATTER DEAD** (axes above; raw_k=2 SECONDARY) |
| G7 | refute-default panel: stats + fact-check CLEAN, f6a MUST-FIX refuted (three-arm tab present); **1 judgment-class RULED by Jason → SCATTER DEAD** (raw≥5 restriction struck, F4-A code-precedence). `exp08/scatter_g7_panel.json` |

## Matched-bar cross-tabs (F6-A rule i; ALL THREE arms read through each own-detector; [0,500k))

| detector (owner) | fr | scatter k/8 | orbit k/8 | A_dwell k/8 | Fisher(sc≥A) |
|---|---|---|---|---|---|
| 0.6129×4 (scatter) | 0.000287 | **2** [1,6] | 1 | 0 | 0.2333 |
| 0.6111×4 (A_dwell) | 0.000439 | **2** [1,6] | 1 | 0 | 0.2333 |
| 0.6129×3 (orbit) | 0.000964 | **6** | 5 | 3 | — |

**Decisive axis (certified census, DEPTH-decisive SIG_DEPTH=8):** certified(≥8) = **0 / 0 / 0**
(scatter / orbit / A); max episode = **4 / 4 / 3** — vs **≥36** for a real committed converter.

**No surviving excess at any common detector** (scatter 2/8 vs A 0/8 → Fisher p=0.23 ≫ 0.05). At matched
geometry the three arms are **indistinguishable on brief crossings** (scatter ≥ orbit ≥ A is low-N band
geometry, not a novelty gradient) and **equally null on conversion**. Every count above fixes ONE detector
and reads all three arms through it; unlike-bar counts are never evidence (catch-16).

## Bare-N census (DEPTH-decisive; SIG_DEPTH=8)

Per-seed longest post-acq ≥0.6129 run, [0,500k): s0..s9 = **[2,4,3,3,2,3,4,3,3,3]**. Certified (≥8): **0**.
The two crossers {1,6} reach exactly N=4 and go no further — bare-N, nothing approaches sustained.

## Companions (reported, never gated)

- **Gradient-persistence** Δ(p1−p13-48) = **0.1112** (A referent +0.1416; alarm threshold 0.0708) — the
  recency shortcut **persists**, no instrument alarm: kinematics was the only change (valid regime probe).
- **acq-guard (capacity check) — RE-ANCHORED (§10.28 catch 19, CC 2026-07-14):** the original rule
  (scatter sep_cat **0.4733** ≥ 0.90 × A_dwell **0.4732**) compared two values at the **undifferentiated
  floor** — sep_cat ≈ 0.5 is category-**blindness** (`_sep_ratio` docstring; FRONTIER "≈0.47–0.50
  (undifferentiated)"), so passing it shows scatter is as undifferentiated as A, **not** that identity is
  recoverable. **Correct evidence:** the same 608-param cortex reaches **sep_cat max 0.86–0.96 / asg_cat
  max 0.66–0.95** in the shuffle converters ⇒ the capacity to represent the category exists. **Conclusion
  UNCHANGED:** DEAD is a real non-conversion, not a confusion-ceiling/capacity artifact.
- **Acquisition-onset** (n=10): min 3k / median 130.2k / max 183k — all ≪ 500k.
- **Tail (500k,1M], DESCRIPTIVE-ONLY — never cross-arm, F6-A tail-hazard pin §3):** one band-touch (s9,
  an EXT seed, longest 4, does not sustain); **blind-tail {0,1,2,3}: none touch → no escalation trigger.**
  The tail is flat; nothing converts past 500k either.

## Execution note (§3 horizon amendment, ride-it-out)

The §3 amendment (read_at split) landed with cal done @1M and G5 ~60% into its 1M runs; by
prefix-invariance [0,500k) is bit-identical at any read_at and restarting would cost more, so the
in-flight runs finished at 1M and the finding uses **[0,500k) for every cross-arm read** (Jason ruled
ride-it-out). Horizon-independence confirmed at code level and empirically (gain(t)/lam1lam2(t)/pam/Adam-LR
key on absolute step; h_max=N vs 2N → bit-identical trajectory). Primary untouched.

---
*Terminal verification (touch 3): the design seat re-derives these numbers from the pushed raw records,
independently, then Jason rules the attribution. SCATTER-CONVERTS would have triggered the pre-named
interior-concentration control before any paradigm-positive certified — not reached (DEAD).*
