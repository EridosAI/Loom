# CC LAUNCH — EXP15 DURABILITY-BY-DOSE — BUILD STAGE ONLY

**Date:** 2026-07-10 · **Authority:** ratified by Jason (design chat) · **Scope: build + pre-check + cal ONLY. THE 40 RUNS ARE WITHHELD** behind the surfacing gate. GO comes after Jason's read.

**Repo:** `EridosAI/Loom`, `main` @ `19616d4`. Author of all commits: Jason Dury, no co-author. Docs are canon — nothing builds before the prereg is on disk. Report-don't-patch; surface anomalies, never silently fix. No new loss / force / mechanism; loss-engineering FENCED; EXP13 PAUSED.

---

## 1. Commit the prereg + two docs riders (one commit, first action)

**(a) `docs/EXP15_DURABILITY_BY_DOSE_PREREG.md`** — the ratified draft, status: **FINALIZED — ratified (Jason, 2026-07-10) + amendments A1/A2 folded.** Lineage: the §10.24 held-open companion ("fabric gates ONSET; dose MAY gate durability"; D 2/4 sustain vs C 0/5). Onset is NOT at stake — EXP14's verdict stands regardless of outcome here.

**(b) Docs rider 1 — §10.24 exposure-ground demotion (one line).** In FRONTIER §10.24's B-refutation bullet, demote "the 5 firing seeds are the 5 highest post-onset window-count seeds → B tracks exposure, not dose" from a refutation *ground* to a descriptive note: exposure-ranking is **non-diagnostic** (a real slow conversion predicts the same ranking — more post-onset time = more chance to convert). The decisive grounds stand unchanged: all-bare-N=3, obs 5 ≈ floor 4.50 (bootstrap-confirmed P(≥5)=0.37), zero length->3 episodes across all 13 B seeds. Verdict untouched; the entry becomes airtight.

**(c) Docs rider 2 — commit `docs/feedback_loose_N_false_alarm.md`.** The cross-experiment carry ("a loose-N cell is verified against its false-alarm EXPECTATION, not its crossing-count") is canon-linked from FRONTIER as `[[feedback_loose_N_false_alarm]]` but the note lives vault-only. Cross-experiment carries belong in `docs/`; commit the note (content = the band-lesson paragraph expanded: the N=3 per-seed ~0.56 false-conversion arithmetic, the 4.50 floor method, the carry-forward rule).

---

## 2. Ratified constants (verbatim into prereg + code)

| Constant | Value | Note |
|---|---|---|
| Common ruler (this contrast) | **0.6875 × 5** | converter classification for the durability contrast + sustain threshold, BOTH cells. Per-cell EXP14 bands retained ONLY for the reproduction check (§3a). |
| Sustain-to-horizon | **mean(exam_acc, last K=10 windows) ≥ band** | kills the single-endpoint fragility (B-s6). |
| Runway censoring | **T_DUR = 200k** | converter with < 200k post-onset runway = **DUR-CENSORED**: reported, excluded from primary, never a "decayed" point. (Against committed data: all 4 D converters enter, runway 282–365k; C-s6 onset 427k censored.) |
| New seeds (A1) | **N_new = 20/cell, seeds {8–27}** | 40 runs total. |
| Converter floor (A1) | **12 per cell** | |
| Reserve pool | **{40–47}** | top-up BOTH cells in pairs, by rule only, cap +8/cell. Should never fire at N=20. |
| Horizon (A2) | **new seeds run to 1M unconditionally; primary frozen at 500k on ALL seeds** | see §4. |

---

## 3. Instrument fixes (build gate — precede everything else)

1. **Coded reproduction check:** reused C/D verdict runs at their EXP14 bands (C 0.64×5, D 0.6875×5) must yield exactly **C {0,2,4,5,6} / D {0,1,3,6}**. Assert, fail loud. Mismatch = INSTRUMENT REGRESSION → fix pipeline, no read.
2. **Fix `score_2x2`'s convert-set / D-row wiring:** the D row keys on the **reproduction check**, not `count_class ≥ 5` (the EXP14 latent mislabel: D at 4/8 → AMBIGUOUS → `converts` excluded D → draft said INSTRUMENT_REGRESSION despite exact reproduction). Mark old logic **SUPERSEDED in-code**; do not silently rewrite.
3. **New `score_durability`** implementing §4/§5 below.

---

## 4. Runs spec (BUILD NOW, EXECUTE ONLY AFTER GO)

- Arms: `C_shuffle` + `D_split` only. Committed {0–7} verdict runs **reused untouched** (screen-provenance verified: `5d9603c`/`396c0a7`).
- NEW: **{8–27} × 2 cells = 40 runs**, fabric pre-built at `h_max = 1M` (ONE fixed perm per arm, no rebuild — the F1 rule; both arms are shuffled-fabric), threads=1, faithful runner (`run_exp14_arm` verbatim).
- **A2:** new seeds run to **1M unconditionally**. This is NOT the EXP14 extension rule — the rising-criterion gate is **not in force** here. **The primary read is frozen at 500k on all seeds** (comparability with the committed 16). The 500k→1M tail is a **descriptive companion only, no claim**: do D's sustainers hold; do C's decayed converters recur.
- `.pt` checkpoints at 500k, at 1M, and at the online onset trigger (standing contract).

---

## 5. Pre-check + stage-one cal (cheap — RUN NOW, these are not the 40)

- **Fabric-assert** seeds {8–27}, both arms, T=15k, outcome-blind; substitution rule carried (lowest unused pool seed, decided at rejection, recorded).
- **spec_hash parity** across reused + new (cal + verdict), fail loud naming any divergent cell.
- **Stage-one sustain-cal from EXISTING traces only** (no new runs): false rate of the last-10-mean detector at 0.6875 on the C-between and D-null cal pools — report ≤ α — plus its descriptive behavior on the committed converter pool.

---

## 6. Outcome cells (named now; execute as written in the committed prereg)

Primary: sustain rate among **eligible** (non-censored) converters at the common ruler, **D vs C, Fisher one-sided (D>C)**.

- **PROMOTED:** p ≤ 0.05 AND ≥ 12 eligible converters per cell.
- **NOT-PROMOTED-AT-POWER:** floor met, p > 0.05 → companion retired at this power, recorded.
- **INVERTED:** C>D significant → anomaly-class; surface, audit, never force.
- **UNDERPOWERED:** floor unmet after capped top-up → routes to Jason, named.

**Sensitivities (reported, never verdict-deciding):** endpoint-window definition; 0.64×5 band; new-seeds-only {8–27}. A direction-flip under sensitivity → promotion carries a visible DEFINITION-SENSITIVE caveat; the primary still decides.

**Companions (read-only, no claims):** episode recurrence counts, last-episode-end times, time-above-band in final quartile, the 1M tail.

**Scope fences:** no onset re-litigation; no claim beyond durability-by-dose within shuffled at this power/horizon.

---

## 7. HARD STOP → surface for Jason's read

Surface together: prereg + riders committed (hashes) · reproduction-check result · sustain-cal false rates · pre-check results · spec_hash parity · smoke (incl. the fixed D-row logic + a run-to-1M/read-at-500k round-trip).

**Do NOT launch the 40 runs.** GO releases them after the read. Scoring runs behind the adversarial refute-default pass — **no lens assumes D>C**. Attribution routes to Jason.
