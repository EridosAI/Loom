# EXP19 W-PERM — G5A CRITICAL-PATH HANDOFF (pre-compaction, 2026-07-14)

**Read this + the ratified spec `EXP19_ORDERING_WINDOW_PREREG.md` + `EXP19_CC_LAUNCH_BRIEF.md` at HEAD.**
Author every commit `Jason Dury <jason@eridos.ai>`, NO co-author, on Jason's word. HEAD = `c710ecf`.

## The one line
Build **B1–B6 landed** (six smokes green, each falsifier observed-red). **wp-strat is now the whole
frontier**, split by Jason into **G5a (stratum viability) → G5b (matched-N power)**. **G5a runs FIRST,
nothing else before it** — and the recon below shows G5a is NOT a trivial "re-score the committed
columns": it needs a **per-onset forward-eval recomputation from the read-checkpoint**.

## THE G5a RECON FINDING (the thing that would be lost) — the committed signal is per-WINDOW, the stratum is per-ONSET
- Committed C_shuffle records (`exp08/exp14_exp12_shuffle_s{0..7}_verdict.json`) store `columns` = **1666
  eval-windows @ eval_cadence=300**, each with `exam_acc` + `exam_n` (17–42 onset-exams **aggregated** per
  window). The census (`_longest_episode`, `exp14_arms.py:1327`) runs on that per-window `exam_acc`; the
  conversion detector `_density_conversion_onset(rec, band=0.64, consec=5)` (`exp14_arms.py:801`) too.
- The **zero-preceding stratum is per-ONSET** (`exp19_score.zero_preceding_mask` — onset exam that is the
  emitted-first wave of its dwell). Restricting to it needs **per-onset exam accuracy, which is NOT in the
  committed columns** (only the per-window mean survives).
- **BUT it is recomputable (zero training, a forward eval):** `exp12_arms.py:576–578` computes accuracy
  **per onset** (`if bool(fab.is_exam[t]): buf["exam_acc"].append(acc)`) then means it per window at
  `:685`. The read-checkpoint `exp08/…_verdict.ckpt_read.pt` carries `{vision, word, op}` weights +
  `gen_state` + `t` + `read_at=500000`. So **G5a = load the read-checkpoint, rebuild the exp12_shuffle
  fabric, forward-eval per-onset exam accuracy over [0,500k), restrict to the zero-preceding stratum,
  re-cut (band,N) on the stratum null via `_provisional_cut`, run the census, ask: does it certify?**
- This changes the §4.3 "ZERO runs / re-score committed records" framing to **zero TRAINING but a forward
  re-eval** — surface this to Jason with the G5a result (it is a real wrinkle, not just a computation).

## G5a — the pre-registered gate (Jason ruling 4, ledger 36; committed §4.3/§7 at c710ecf)
> **G5a — STRATUM VIABILITY (full N).** Does `exp12_shuffle` certify on its own zero-preceding stratum at
> **full stratum N (~14,156/seed)** with the detector **(band,N) re-cut fresh on the stratum** via
> `_provisional_cut` (calibrate-in-regime transports the PROCEDURE, never the constant; `consec=5` cannot be
> inherited — the timescale changed)? **NO → HALT → Jason** — the stratified detector has no baseline,
> wp-strat is unaskable, the arm's entire recency defence is **decorative**.
> **The shattering risk is STRUCTURAL:** a 36-onset episode yields ~6 in-stratum onsets — the detector may
> be unable to form runs at ANY N. **If C_shuffle cannot certify on its own recency-free stratum, STOP and
> tell Jason before anything else is built** — that outcome ends the recency defence and he must see it.

## G5b — matched-N power (only if G5a passes)
Subsample each seed's stratum to **N = 7,915** (worst per-seed paid stratum = seed 4; per-seed B=512 strata
= {0:8097,1:8038,2:8191,3:8248,4:7915,5:8036,6:8126,7:8091}, panel-computed — VERIFY at build) by
**AMONG-KEPT uniform thinning** (faithful to the treatment: same [0,500k) window, sparser stratum). K draws,
**pin `SUBSAMPLE_SEED`**. **PASS iff each of the 5 committed converters {0,2,4,5,6} certifies in ≥90% of
draws** (derived: read is k/8; require q·k<0.5 ⇒ q<0.10 ⇒ retention ≥90%). **MARGINAL (any converter <90%
while others above) → Jason** (seed-dependent detector can't report a null). **NEGATIVE CONTROL gates the
METHOD:** the 3 non-converters {1,3,7} must certify ≤1% of draws, else among-kept is manufacturing
conversions (run-merging) → method void → HALT. Contiguous-block subsampling rides only as a reported
sensitivity (window-placement confound). Full distribution reported regardless. (50% bar REJECTED — certifies
a coin-flip detector ⇒ spurious RECENCY-CARRIED, the mirror of the trap that bit twice this cycle.)

## Key code refs (verify at HEAD before building on them — re-derive-recon rule)
- `exp14_arms.py`: `_provisional_cut`:630 (joint band,N on the between-episode null), `_between_episode_null`:643,
  `_density_conversion_onset`:801, `_longest_episode`:1327, `_episode_mask`~446/461, `EPISODE_BAND/EPISODE_MIN=8`:84.
- `exp12_arms.py`: per-onset exam acc `:576–578`, per-window mean `_eval_column`:656/685, `exam_lift`:287.
- `exp19_score.py` (built this cycle): `zero_preceding_mask` (B4), `recency_companion` (B5), `rho` (B6),
  `preflight_measures` (deployed 500k). `exp19_smoke.py`: wp1/wpT/wp-multiset/wp-strat-label/wp-recency/wp-delta
  (6 green, falsifiers red). `exp19_g0b_genregress.py` (G0b v2 content-digest+diffscope), `exp19_diffscope.py`
  (generator blast-radius, symbol-scoped; B11's learner check goes here too, ledger 32), `exp19_g0b_redteam.py`.
- Committed C_shuffle: read_at=500000, h_max=1000000, fabric.T=1000008, converters {0,2,4,5,6}, non {1,3,7},
  full-read conv 0.64×5, longest episodes {0:85,2:60,4:36,5:77,6:90}. B=T stratum over [0,500k)=30.75% (14,156).

## After G5a/G5b: remaining build (do NOT start before G5a result)
B7 `exp19_cal` (per-B band, both detectors, borrow-gate) · B8 `exp19_score` (dual detector + gradient, the
matched-N wp-strat) · B9 matched-bar tabs ×2 · B10 smokes · B11 `exp19_diffscope` **learner** check
(symbol-scoped `inspect.getsource(EXP12Loop.step)`, ledger 32) · pre-flight G0/G0b/G1a-b/G2/G3/G3b/G4/G6/G7 →
**G8 package to Jason** (touch 2). Jason reads it against 3 things ONLY: every falsifier observed-red; every
constant computed-not-asserted; **wp-strat passed**. Nothing trains until Jason ratifies G8.

## Ledger this cycle (progress_log §ledger): 29 G0b-REUSED-omission · 30 seat bit-identity-no-committed-record ·
31 G0b permutation-invariant comparator (CC) · 32 B11 file-vs-symbol · 33 §4.3 straddle sign (CC) · 34 B=T
horizon/read-window (CC) · 35 CC dismissed wp-strat power-transfer · 36 wp-strat presumed a non-existent
stratum baseline + non-transporting constants (CC panel → Jason). **The recurring trap: the favorable/
unflattering number goes uninterrogated — it bit at ledger 34 and 35.**
