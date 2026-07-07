# HANDOFF → next context: EXP14 2×2 conversion-deconfound (build after GO)

**Written 2026-07-07. HEAD `9ea9e54` (github.com/EridosAI/Loom, main, pushed, in sync).** This is the fork seam: the EXP14 screen closed with the program's sharpest result, the 2×2 deconfound is fully pre-registered + committed, and the build executes here after Jason's GO on the sequence.

## Where we are (the one-paragraph state)

**CONVERSION IS REACHABLE.** The operator ("completer") that rides a near-constant marginal on word-completion program-wide (EXP13 §10.21) **CAN leave the marginal** — the EXP14 horizon-extension screen (fork (i)) found sustained conversion on the coin/shuffled arm: **5 coin seeds** (verdict {0,1,3,6}=4/8 + cal s20), scheduled/dwelled **0/8**. Reframe updated (scoped): sensitivity-without-conversion is **regime-specific, not universal**. The screen is fabric-confounded (coin=shuffled, scheduled=dwelled), so the **2×2 deconfound** (`docs/EXP14_2x2_DECONFOUND_PREREG.md`) attributes conversion to **dose / fabric / interaction**. Screen prior = interaction (only the corner has ever converted).

## Commit chain (all pushed)
- `5d2817e` EXP14 prereg (fork i) · `5d9603c` stage-one (build `exp14_arms.py` + fabric-assert T-independent re-pin + cal band) · `f039ccd` **screen CLOSED** (band honest-null re-pin, 16 verdict runs, canon §10.22) · `9ea9e54` **2×2 prereg finalized** (ratified + 2 pins + panel-folded).
- Canon: FRONTIER **§10.22**; PROJECT_STATE + progress_log dated 2026-07-07. Memory: `loom_exp14.md`.

## NEXT = build the 2×2 (after Jason's GO — the sequence is pre-ratified, prereg §7)
1. **Pre-check** verdict {0–7} fabric-assert for the 2 NEW arms (`exp12_shuffle`, `exp12_12bc_dwp`) — T-independent assert, build at T=15k (fast). Outcome-blind swap any defective from {8,9,…} (recorded), same rule as cal s23→s25.
2. **Stage-one cal** the 2 new arms × {20,21,22,24,25} @ 500k → cut their honest bands + **establish `12bc_dwp` acquisition-liveness**. **SURFACE all 4 per-cell bands + n_null + per-cal-seed converters + liveness FOR JASON'S READ before any verdict.**
3. **Verdict:** the 2 new arms × {0–7} @ read 500k / h_max 1M, checkpoints on (dwell & split REUSE the committed screen verdict runs — do NOT re-run them).
4. **Score:** per-cell conversion (sustained-episode) + stability → `score_2x2` attribution DRAFT → **behind an adversarial refute-default panel** → route to Jason. STOP at the attribution.

## Build work the code needs (all in `experiments/05_attention_sculpting/exp14_arms.py`; one code path — dynamics reused verbatim)
- Extend `RUNGS` (currently `{scheduled: exp12_dwell, coin: exp12_split}`) to the 4-cell map: **A** `exp12_dwell` (dwelled-scheduled), **B** `exp12_12bc_dwp` (dwelled-coin), **C** `exp12_shuffle` (shuffled-scheduled), **D** `exp12_split` (shuffled-coin). All exist in `exp12_arms.ARMS12`.
- **F1 — two-pass fixpoint null** in `cut_conv_band`/`_honest_null`: cut a provisional (band,N) on the s0-class-excluded null, then also exclude cal episodes that fire the *provisional* detector, re-cut to a fixpoint. Add a per-cal-seed converter diagnostic to the surfaced output. (Current `_honest_null` excludes only s0-class ≥0.704×8 — too strict vs the ~0.61–0.69 verdict bands; this protects the decision-relevant `12bc_dwp` cell from reading DOSE as INTERACTION.)
- **F2 — spec_hash parity assert** across all 4 cells (reused + fresh, cal + verdict) in `cut_conv_band`/`score_2x2`; fail loudly on mismatch (reused-vs-fresh = one interaction diagonal, so a build skew loads onto the interaction contrast).
- **F5 power gate** (a B/C cell in lottery{1,2}/ambiguous{3,4} fires EXT_POOL {8,9}, n→10, before attribution; report interaction CI) and **F6 budget gate** (READ seed with post-onset budget `500k−onset` < ~130k = UNREAD budget-truncated) in `score_2x2`.
- `score_2x2` = the exhaustive/exclusive attribution table (prereg §5), structured on corner-D → B/C.

## Disciplines to carry (binding — this is a doctrine-heavy program)
- **Conversion = sustained-EPISODE** (≥N consecutive windows ≥band, anywhere post-onset), NOT endpoint. **Stability** (sustains-to-horizon vs decays) = registered companion (screen: only s0 sustained; s1/s3/s6 decayed).
- **Pre-gate A (READ = acquired on num/den/asg_cat, not exam_acc) + pin-2 (liveness = acquisition):** a non-acquiring `12bc_dwp` cell is UNREAD, never a "no-conversion" dose/fabric point (F5-EXP14 / UNREAD-never-none).
- **Instrument re-pins recorded this arc** (both EXP12/13-safe, those are closed): (1) `exp12_fabric._dwell_perm_labels` T-independent (permute only in-window dwells); (2) band honest-null (`_honest_null`, EPISODE_MIN=8) — now being sharpened to the two-pass form (F1).
- **Checkpoint contract** [[feedback_checkpoint_every_run]]: `.pt` at horizon + conversion-onset, every run.
- **Determinism:** seed + construction order + `torch.set_num_threads(1)`; faithful runner (interleaved reads couple); `run_exp14_arm` proven digit-identical to `run_exp12_arm` — keep it so.
- **Process:** pre-register before build; adversarially verify surprising results BEFORE the table (the draft-flip pattern held all session — the screen's 15/16 draft flipped to 4 real via sustain-check + panel); surface-recommend-stop; no silent patches (surface discrepancies); commit at each gate (don't pool); author `Jason Dury <jason@eridos.ai>`, no co-author, **commit on Jason's word only**; loss-engineering stays manufacturing-class FENCED.
- **Compute:** 32 cores / ~50GB; 500k run ≈ 25 min, ~16 parallel (1 thread each); use the nohup+disown launch + a background until-loop waiter with crash coverage (grep Traceback|Error|assert|Killed). OUTDIR = `experiments/05_attention_sculpting/exp08/`.

## Key numbers (carried)
- Cal seeds {20,21,22,24,25} (s23→s25 swap); verdict {0–7}; EXT_POOL {8,9}.
- Carried bands (re-verify under two-pass before reuse): dwell 0.6111×4, split 0.6875×5. s0 anchor 0.704×16. α=1e-3. EPISODE_MIN=8. READ_AT=500k, H_MAX=1M, EVAL=300, BLOCK=3000.
- Screen verdict: coin {0,1,3,6}=4/8 (s0: 63 windows ≥0.704, dwarfs committed 16); scheduled 0/8; +cal s20.

EXP13 holds PAUSED (gate UNPOSABLE-AT-CURRENT-COMPLETER). Nothing verdict-grade before the 4 bands + liveness are surfaced for Jason's read.
