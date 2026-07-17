# EXP19 W-PERM — PRE-FLIGHT PACKAGE (the G8 object, touch 2)

**Assembled 2026-07-17 at HEAD `c64a2b4`.** Read against the ratified criteria: every falsifier
observed-red · every constant computed-not-asserted · wp-strat passed (+ the per-B ≥width-floor law) —
plus the riders ruled in since: **the B4 flag verbatim · flag-3 · ratified v5 (ten amendments,
`EXP19_PREREG_V5_DRAFT.md`) · the decay finding with its sensitivity companion.**

## Gate table (executor → outcome; every gate re-run at HEAD, never assumed)
| gate | executor | outcome |
|---|---|---|
| G0b generator scope + content | `exp19_diffscope.py` (structural, whitelist = W-PERM blast radius) | **PASS at HEAD**; red-team fires on planted self.centre perturbation |
| Learner fence (B11, L47) | `exp19_diffscope.learner_fence()` — live `EXP12Loop.step` == baseline `Stage0Loop.step` (loop.py:208) via MRO | **PASS at HEAD**; planted override FIRES + clean restore |
| wp-strat G5a (viability) | `exp19_floor.py --audit` | **PASS** (floor audit; α-transport catch L38); re-run bit-identical at `1a33096` |
| wp-strat G5b (matched-N power) | `exp19_g5b_rebin.py` | **PASS** (window artifact L40/41; argmax rule L42). **B4 FLAG, VERBATIM (never summarized away): s6 matched-N at the final op 550: q10 12 vs floor q99 8 (1.5×), `s6_clears_robust: false` (min 6 dips under the floor q99 in the subsample-draw tail).** |
| B7 calibration law | `exp19_cal.py` (argmax separation per B, per read; underpower gate; robustness field `da7bbb6`) | validate/smoke/redteam-borrow **green at HEAD** |
| B8 dual-detector scorer | `exp19_scorer.py` (band 0.64 one-family assert; outcome-blind sim floor) | validate/smoke **green**; dec_cat coverage 8/8 (`323568c`) |
| B9 matched-bar tabs | `exp19_tabs.py` (L45; paired stats; floor columns) | validate/smoke **green** |
| B10 smokes wp1/wpT/wp-parity/wp-posassert/wp-delta/wp-strat-label | `exp19_smokes.py` | **ALL PASS** (`c64a2b4`): wp1 + wpT bit-identical at FABRIC and WEIGHT level; naive stratifier shown RED at every B>1 |
| wp-multiset | committed twin-rebuild + checksum assert (`exp12_arms:444`) | passes by construction (shuffled=True on wperm arms) |

## Computed pre-flight constants (deployed [0,500k) of the 1M fabric — `exp19_preflight_measures.json`)
| B | ρ(B) | stratum (zero-preceding) | n_stratum |
|---|---|---|---|
| 1 | 0.90860 | 100% (structural) | 45,702 |
| 32 | 0.39444 | 22.66% | 10,358 |
| 128 | 0.12723 | 18.39% | 8,405 |
| **512 (anchor)** | **0.03370 (≤0.05 ✓)** | **17.72%** | **8,097** |
| 2048 (esc.) | 0.00857 | 17.54% | 8,015 |
| T | 0.00001 | 30.75% | 14,156 |
Non-monotone stratum ⇒ **STRATUM-POWER-SHAPE** (v5 A9) governs any stratified non-monotone read.
Per-B operating widths + ≥width floors: cut IN-CORRIDOR on each B's own null (`exp19_cal`, L42) with the
**G7 separation-curve surface** (v5 A7: full curve reported; integer-tie argmax ⇒ HALT → Jason).

## Endpoints — single instrument end to end (v5 A5), zero replays, computed
- **B=1** (A_dwell): **0/8** under the floor audit (`exp19_endpoint_B1_flooraudit.json` — blind column-based
  read from committed records; runs 2–3 vs own nulls 5–6). The α-era 0/8 reproduced under the one family.
- **B=T** (C_shuffle): **full 5/8 @op300, stratified 5/8 @op550** = the committed set {0,2,4,5,6}
  (B8 committed validation), recency-carried [].

## The B\* estimator (v5 A8, blind, pre-data)
Bracket rule on certified counts c(B); B\* ∈ (B\*_lo, B\*_hi]; full c(B) curve always; degenerate routes
pre-named. No point estimate; fits reported-never-gating.

## Open items riding into the read
- **flag-3 / LATE-RESCUE-IN-TAIL (v5 A10):** latest committed onset 427.5k/500k; tail-only cell, never in
  the estimator. **Decay finding (regime-bound):** 4/5 converters LOCKSTEP-EROSION + sensitivity companion
  (co-decay 5/5 significant; material 4/5; s2 complete-to-dead-band; erosion horizon-truncated) — the
  category representation erodes post-episode; bears on flag-3's direction.
- Cost: **39 paid runs** (3 paid B × 13; +13 conditional at B=2048), per §8.

## HARD STOP — the corridor-open word
The ratified protocol places Jason's G8 read HERE, on this assembled package. His 2026-07-17 word
"G8 ratified. Go." arrived BEFORE assembly (sequence: …pre-flight → G8) — under the standing rule "a
contradiction between two rules is a HALT," the corridor does NOT self-open on the advance word: **this
package is the object his ratification must attach to.** If the advance word stands as-is, one word on this
package opens the corridor (39 runs; auto-push at every closed gate; checkpoint contract standing).
