# TWO FREE READS — TERMINAL PACKAGE (assembled by CC, 2026-07-25)

**Route: design-seat verification FIRST, then Jason for the rule.** Base at order receipt: `9510e4e`.
Commit trail: texts `2ac1480` → pre-flight `c2fc3f5` → pin read `204feb9` → this package. The ratified
texts are `docs/OPTIMIZER_PIN.md` and `docs/STEP0_CWP_PREMISE_READ_PREREG.md`, committed verbatim as
attached (canon-as-attached rule; no edits, typos included).

---

## READ 1 — OPTIMIZER PIN: **COMPLETE, all gates green, every red observed first**

**Artifact `outputs/optimizer_pin.json`** (committed; HEAD-at-emit recorded inside):
torch.optim.Adam · lr **3e-3** (parsed from `constants.py:87`, == cfg.lr == live group) · betas
**(0.9, 0.999)** / eps **1e-8** / weight_decay **0** — read off the LIVE param group (by-omission
defaults), cross-checked against the installed-torch signature · scheduler **none** · torch
**2.10.0+cu128** (Equinox, timestamped; env-lock PATHWAY item stays open) · **τ₁ = 10 waves, τ₂ = 1000
waves** (computed from the read betas — stored as the raw floats 10.000000000000002 /
999.9999999999991; equality to §2's integers is float representation only, rel 1e-12) · param census:
**20 tensors held (vision + op), 1 excluded (word — the frozen exclusion of `loop.py:8`, mechanism =
never enters the optimizer, `loop.py:67`)**, one param group, census via constructor-only instantiation
(exp12_dwell s0, T=2000, zero optimizer steps — mechanics field in the artifact).

**Gate log `outputs/optimizer_pin_gatelog.json`:** P0 — 3 citations byte-verified at HEAD (`loop.py:68`,
`constants.py:87`, `loop.py:8`; actual line text recorded). P1 — 14 `torch.optim.` constructor calls in
the tracked tree, **all lr-only**; zero scheduler references; zero lr mutations via param_groups (all
param_groups lines enumerated in the log). P2 — artifact complete per the §4 field list. **Observed
red first, all three fixtures:** P0 edited-line, P1 `betas=` kwarg, P2 field-drop.

**§4 landing applied:** `MECHANISM_MAP_conversion_gating.md:71` and `MECHANISM_MAP_v1_2_RECONCILED.md:68`
annotated in place — "[PINNED 2026-07-24 → optimizer_pin.json: τ₁=10, τ₂=1000]". The §3 flag commentary
stands verbatim in the ratified doc; per §6 it is commentary, not evidence, and this package adds no
sentence to it.

## READ 2 — STEP-0 CWP PREMISE: **G0/G1 green (reds observed), G2 HELD on a census-surfaced HALT**

**G0 census (`exp08/step0_census.json`):** 100 candidates enumerated from the committed (git-tracked)
OUTDIR, every exclusion reasoned. **Admissible: the 8 verdict records of the certified-dead cell** —
`exp14_exp12_dwell_s{0..7}_verdict.json`, arm field verified `exp12_dwell` (provenance computed, not
filename-trusted), 1666 columns each, both required fields present in every column. Companion census:
8 `exp14_exp12_shuffle_s{0..7}_verdict.json`. Fixture: one-good-one-field-missing dir → exactly one
exclusion (PASS). **G1 reader red-team:** FAILS and CONFIRMED synthetics land correctly; **the broken
≥-variant was observed red on the tie fixture before the strict version's pass** (gate log); an
empty-denominator fixture HALTs rather than judges.

**THE HALT (G2 HELD — surfaced, no workaround taken):**
> STRUCTURAL: `pos_err_vis` lacks the `p1` bucket in **every column of every admissible record**
> (measured 0/1666 × 8 seeds; the `_buffer_wave` training-stash routing stashes no vision-side error at
> onset — `exp12_arms.py:725-727` assembly, `:536` `_buffer_wave`). The §4 vis-channel onset-dominance
> denominator is EMPTY for the whole cell; §5 defines no cell for an undefined dominance.

The **word channel is complete everywhere** (all six buckets in 1666/1666 columns, every seed; late
quartile = 417 columns per seed, denominator ready). No cell was computed on either channel and no
companion was run — a word-only read is a judgment the prereg does not license, so the whole compute is
HELD. **The fork this surfaces (Jason rules; no recommendation made):** treat the read as word-channel
(a cited fold to §3/§4), or add a ratified vis-channel convention — either is a text change, which is
why it routes rather than executes.

## Deviations & notes for the verifying seat (all in-envelope, all recorded)

1. **`outputs/` is gitignored** (pre-existing rule, `.gitignore:23`); the doc-named §4 artifact paths
   were force-added by file so the committed form exists. No ignore-rule edit.
2. **P1 self-scan exclusion** (instrument fix, reported): once committed, the sweep flagged its own
   detector strings and red-fixture literal; `exp_opt_pin.py` excludes itself from its own sweep. The
   pre-flight P1 PASS was re-run on the post-commit tree before P2 emitted.
3. **G2's full cell/companion emission is unbuilt beyond the HALT** — deliberately: the primitives it
   would compose (census, quartiles, dominance, cells) are the G1-fixture-verified functions, but the
   emission path is gated on the ruling and was not drafted ahead of it.
4. Executor locations follow house convention (`experiments/05_attention_sculpting/`); step-0 artifacts
   in `exp08/` (house), pin artifacts at the doc-named `outputs/` path.

**Scope fence honored:** nothing else was built; U-BUF stands ratified-but-unopened; no learner-adjacent
code was touched.

---

## ADDENDUM — AMD-1 resolution and the step-0 read (2026-07-25)

**AMD-1 folded** (`2c33bf0`), grounds byte-verified at fold: `exp12_fabric.py:27` — "position-1
word-mask GUARANTEED (the onset exam)"; the 0/13,328 vs 13,328/13,328 counts are the census's own
measurements. G1 re-run green after the compute-path build (broken ≥-variant red observed again); G2 run
under AMD-1 with the census's structural surface recorded as resolved-by-AMD-1.

**RESULT — PREMISE-FAILS on the word channel, all 8 seeds agree** (`exp08/step0_read.json`):

| seed | late dominance (417 cols, 0 dropped) | early |
|---|---|---|
| s0 | 0.16547 | 0.29808 |
| s1 | 0.23501 | 0.30048 |
| s2 | 0.14868 | 0.35817 |
| s3 | 0.30456 | 0.30288 |
| s4 | 0.15108 | 0.34135 |
| s5 | 0.12950 | 0.32212 |
| s6 | 0.19664 | 0.30048 |
| s7 | 0.15827 | 0.33413 |

Every seed ≤ 0.50 (the FAILS bar); none within reach of 0.90. **The licensed sentence (§8 + AMD-1, the
only sentence this buys):** *"5.1's premise fails in-substrate; the CWP program closes before it opens"*
— **on the word channel.**

**Descriptive companions (no cells):** the MEAN word curve is monotone decreasing p1 → p13-48 in both
quartiles (late s0: 0.711 → 0.627) — an average onset gradient exists, but the per-column strict spike
the premise requires fires in only 13–30% of late columns; the gap between "average gradient" and
"reliable per-column spike" is what the estimator prices. Vis (recovery-shape only): p2 → p13-48 gently
decreasing (late s0: 0.163 → 0.145). Shuffle contrast (flagged, context only): word dominance
0.137–0.173 — the label-conditioned curve does not differ materially from the dwell cell's late read.

**HELD FOR THE RULE (after seat verification):** the §5 FAILS route's map annotation (the v1.2 §6
falsifier) is a canon act — not fired by CC. No rescue drafting, per the route. **OPEN on Jason's word:**
the seat's offered protocol rider ("estimator-support check at pre-flight"), and any ledger row for the
seat-owned miss — both ratification acts, neither applied.
