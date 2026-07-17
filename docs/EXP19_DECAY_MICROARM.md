# EXP19 decay-mechanism micro-arm + dec_cat endpoints — doc-with-cells (D1 + C1, shared compute)

**Status:** RATIFIED (Jason 2026-07-17; cells as written + the two ratification sentences below). Phase C GREEN (launched under the cleared gate). Formerly: DRAFT / PENDING RATIFICATION — committed to the record on the seat's instruction (2026-07-17):
pre-registration is only provably pre-registration once committed; the cells must be canon BEFORE the
C-decay data they route exists. **Phase C is GATED on (i) this doc committed and (ii) the Phase-A noise
band cut and recorded, blind, per §Noise-band below.** Phase A running against the uncommitted draft was
ruled tolerable (A carries no category signal by hypothesis and feeds only the blind noise band). Opened on
Jason's ruling ("doc-with-cells first; A before C; GPU check first"); status flips on ratification.
**Trains nothing, touches no gate** — all compute is deterministic replay of committed trajectories with
the committed (dec_cat-bearing) column instrument.

## Question (audit D1)
G5a showed conversion is a TRANSIENT EPISODE: converters un-convert under continued shuffled training
(committed `EXP19_G5A_DECAY_COMPANION.md`; peaks 0.87–0.91, then decay; only s6's episode is recent enough
to leave tail-50 = 0.616). WHY? Three mechanisms, different implications:
(i) representational interference — later waves overwrite the category axis;
(ii) axis rotation — dynamically unstable axis-selection (the ISOTROPY line's view);
(iii) readout drift — the representation persists; the exam readout's operating point moves.
`dec_cat` (LOO nearest-centroid category decode, col-only, DECCAT-REGIME-BOUND) through the decay window
discriminates (iii) from (i)/(ii).

## Compute (priced at open; C1's endpoints ride the same replays)
- **Phase A (first): 8 × A_dwell (`exp12_dwell` s0–7) replays** at the committed verdict params, HEAD code
  (columns now carry dec_cat). Fills the **B=1 dec_cat endpoint** (C1: currently 0/8). A_dwell has no
  converters — no decay read here; this is the endpoint baseline.
- **Phase C (second): 7 × C_shuffle (`exp12_shuffle` s1–7) re-replays** (s0 already carries dec_cat from
  the anchor-verification re-replay, `9f5aa7c`). Fills the **B=T dec_cat endpoint** (C1: 1/8 → 8/8) AND the
  decay read (5 converters).
- ~30-min-wall class each (audit estimate); run sequentially, GPU checked free before start; checkpoint
  contract applies (`.pt` at read horizon — standing).

## Anchor discipline (before any cell is read)
Every replay must reproduce its committed record on the PRE-EXISTING fields (columns digit-exact; dec_cat
rides as the additive field exactly as proven on C_shuffle s0 — anchor bit-identical there). A replay that
does not reproduce its committed record is a HALT-and-audit (REUSED-class; never substitute). Params
(read_at/h_max/spec_hash) are read from each committed record, never assumed.

## Pre-named cells (read on C_shuffle's 5 converters, episode window [t0..t1] from the committed decay
companion vs the post-episode tail; per-column dec_cat vs exam_acc; REPORTED, never gated)
- **READOUT-DRIFT:** dec_cat holds through the post-episode tail (stays in its episode band) while windowed
  exam_acc decays to chance ⇒ mechanism (iii): the representation persists, the readout moved. (Bears on
  the detector: "un-conversion" would be partly instrumental.)
- **LOCKSTEP-EROSION:** dec_cat falls with exam_acc through the tail ⇒ (i) interference OR (ii) axis
  rotation — **this read does NOT separate (i) from (ii)**; pre-named honestly as a pair. (Separating them
  = an axis-tracking read, out of scope here; bank.)
- **MIXED/AMBIGUOUS:** converters split across the two shapes, or dec_cat's move is within its own
  between-window noise band (measured per seed from the pre-onset segment) ⇒ report the split; no
  mechanism sentence.
- **INSTRUMENT-NULL (control, pre-named):** on the 3 non-converters (no episode), dec_cat through the same
  windows must show NO episode-locked structure — if it does, the read is picking up something other than
  the episode and the mechanism cells are uninterpretable (report → Jason).
Direction words only — no thresholds invented here; every number in the eventual read is computed from the
replayed columns with its noise band stated. DECCAT-REGIME-BOUND stands: whatever the cell, no
"dwell solved" / generalization sentence — mechanism attribution within THIS regime only.

## Ratification sentences (Jason 2026-07-17, text supplied)
(i) **The null statement:** No analytic chance level is used or cited. The Phase-A empirical band is the
null: LOO nearest-centroid carries small-sample bias (dead-arm pooled mean 0.238, p95 0.563 — well below
nominal 1/n_category = 0.5), so citing 0.5 as "chance" would overstate the null and misread moderate dec_cat
values as below-chance.
(ii) **The self-containment statement (CONFIRMED at HEAD before stating — `exp12_arms._dec_cat`):** dec_cat
is within-window self-contained (LOO centroids from that window's 16 probes only; no cross-window centroid
pooling), so encoder drift between windows cannot contaminate a single window's decode; trajectory
comparisons compare self-contained reads.

## Noise band (the Phase-C gate's second condition — cut BLIND, before any C-decay data exists)
The **blind instrument-noise band for dec_cat** is cut from **Phase A's replayed series** (A_dwell is the
dead arm: no episodes, no category signal by hypothesis — its between-window dec_cat variability IS the
instrument's noise, uncontaminated by any decay signal). Recorded per seed (between-window spread over the
post-acquisition segment) and pooled, BEFORE Phase C launches; committed with the Phase-A result. The
C-converters' own PRE-ONSET segments ride as per-seed companions (same statistic, same code path). A
dec_cat move inside this band is the MIXED/AMBIGUOUS cell's "within noise" arm; every cell read states its
distance from the band.

## Outputs
Per replay: the standard record (+ manifest), per-onset capture + digest, and the derived per-window
stratified series per seed (the v5 item-(e) standard, committed like `a72ea3c`). Endpoint dec_cat coverage
updates B8's ledger-48 tripwire WITH the data (the assert names this obligation).
