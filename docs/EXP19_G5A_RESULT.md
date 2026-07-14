# EXP19 W-PERM — G5a STRATUM VIABILITY: **PASS by floor audit** (2026-07-14)

**Gate (prereg §4.3/§7):** does `exp12_shuffle` (C_shuffle) certify conversion on its OWN zero-preceding
(recency-free) stratum? **Result: PASS.** Certified in the house's form — **excess over a measured phantom
floor** (ledger 18: raw counts never gate; they sit inside the floor), NOT an α-cut binary. The arm's
recency defence is **not decorative**: conversion survives removal of the recency channel, and it clears the
granularity floor the sparse stratum produces.

## The certification — FLOOR AUDIT (excess over the measured floor, in-regime, blind)
The non-converters {1,3,7} do not "leak" — **they are the phantom floor, measured** (they carry the real
granularity and autocorrelation of the regime). Certification = the converters clearing that floor.

| seed | class | stratum run (≥0.704) | in-regime sim null (max / q99.9) | p(null ≥ obs) | clears floor? |
|------|-------|----------------------|----------------------------------|---------------|---------------|
| 0 | CONV | **37** | 16 / 14 | <1/5000 | ✅ |
| 2 | CONV | **20** | 10 / 9 | <1/5000 | ✅ |
| 4 | CONV | **17** | 11 / 10 | <1/5000 | ✅ |
| 5 | CONV | **71** | 10 / 10 | <1/5000 | ✅ |
| 6 | CONV | **12** | 10 / 10 | <1/5000 | ✅ (marginal) |
| 1 | non | 4 | 10 / 9 | 0.806 | — (floor) |
| 3 | non | 5 | 9 / 9 | 0.333 | — (floor) |
| 7 | non | 6 | 10 / 9 | 0.107 | — (floor) |

- **Empirical floor** = the non-converters' own longest runs, ceiling **6**. **Nearest converter = 12 = 2×
  the ceiling** — a clean separation outside the bracket, the SCATTER-terminal form ("raw sits inside/outside
  the phantom bracket").
- **Simulated floor** (pinned `SIM_SEED=20260714`, 5000 draws, per-window in-stratum onset counts preserved,
  Bernoulli at each seed's post-acq p̂): every converter's observed run exceeds its own null max (p<1/5000);
  every non-converter sits within its null (p 0.11–0.81).
- **s6 is the marginal converter** (carried forward, not buried): 12 clears the empirical ceiling (6) 2×, but
  clears the *simulated* non-converter tail (max ~9–10) by only +2. This is precisely the seed G5b tests — at
  the thinner treatment stratum the floor rises toward 12.

## The real finding — **ALPHA does not transport** (the instrument-assumption audit; ledger 38)
The α-cut binary was the wrong instrument, and its failure is the finding. `ALPHA=1e-3` is cut against an
**i.i.d.** false-rate model (`_consec_rate`). On the stratum, per-window accuracy is **granular** (5–13
onsets/window) and **autocorrelated** — the i.i.d. model does not hold. A detector nominally at 1e-3
delivered an **actual false rate of 2/3** (the α-cut selected N=5; 2/3 non-converters clear N=5). A **~667×
miss** — a calibrate-in-regime violation hiding inside a constant. **Ruling-B didn't fail; α did.** Neither
the seat nor Jason audited whether α survived the regime change; that instrument-assumption audit is the
hardest and most valuable thing here. **Ruling 4 (standing): nothing transports into the stratum regime —
band, N, α, cadence are all suspect until re-measured red.** (Band=0.704=`EPISODE_BAND` is *forced* here, not
transported: the stratum-null quantiles q90=0.83/q95–99=1.0 blow past the S0 cap — `exp19_g5a_fork_sensitivity.json`.)

## How the fork was resolved — a TEST, not a choice (ledger 37)
The seat first recommended `_provisional_cut` "because it's clean and Ruling-B leaks" — selecting an
instrument by its outcome, forbidden. The fork is a computable trigger: **do C_shuffle's cal seeds convert
on the zero-preceding stratum?** They do — **4/5** (s21/22/24/25 s0-class runs 22/37/37/13 on the stratum;
s20 no) = **exactly the full-read 4/5**, same seeds. Conversions persist recency-free ⇒ no clean marginal ⇒
Ruling-B regime forced (`exp19_g5a_fork_trigger.json`). But the deeper lesson overtook the fork: the
α-cut — the shared machinery of *both* provisional and Ruling-B — doesn't transport. The floor audit sidesteps
it (no α, no N-threshold; pure excess over the measured floor).

## The mechanism — deterministic replay, anchor-certified (why, and that it's faithful)
The committed conversion signal is an **evolving-weight trajectory** (per-window mean of live per-onset
`exam_acc`); the read-checkpoint at 500k has **reverted toward chance** (decay companion), so a frozen-eval
returns ~chance for all seeds. The faithful per-onset signal is recovered by **deterministic replay**
(`exp19_replay.py`, read-only monkeypatch on `_buffer_wave`), certified by three anchors, **all green on all
8 verdict + 5 cal seeds**:
- **A1 bit-exact** — replay `.ckpt_read.pt` == committed (every tensor incl. `gen_state`; `t==500000`).
  Committed @`396c0a7` (verdict) / `510f23b` (cal) == replay @HEAD ⇒ A1 also certifies B1's shuffle-path
  refactor did not perturb the arm.
- **A2 columns** — replay per-window `exam_acc` == committed (digit-exact).
- **A3 consistency** — re-binned captured per-onset → windows == committed columns.
- **RED-TEAM** (`exp19_replay.py --redteam`): a capture that shifts one draw reddens A1; a corrupted capture
  reddens A3; clean is green. The anchors are reachable falsifiers.

## Decay companion (ruling 4 — carried for G8; `docs/EXP19_G5A_DECAY_COMPANION.md`)
Conversion here is a **transient episode, not a stable end-state**: every converter's episode ends before
500k (peak 0.87–0.91, 36–90 windows), then decays toward chance. The 500k checkpoint is **not converged** —
which is why the frozen-eval was wrong. Any future read treating it as converged is wrong.

## G5b — the re-specified question (Jason)
Not "does a converter certify at N=7,915?" but **"what is the phantom floor at 7,915, and does the converter
signal still clear it?"** The floor RISES as the stratum thins (sparser windows ⇒ granular accuracy ⇒ longer
chance runs). Nearest converter 12 vs a floor ceiling 6 at 14,156 onsets; at 7,915 the floor may reach 12 and
swallow s6. That is the underpower risk at the ρ≤0.05 anchor (B=512), and it is **measurable before anything
trains** — subsample the actual non-converters (autocorrelation-carrying) to the treatment's density, measure
the phantom floor, check whether the converter signal clears it.

## Provenance / reproduction
- Replay + anchors: `exp19_g5a.py --replay {0..7}`, `exp19_g5a_fork.py --replay-cal {20,21,22,24,25}` (13
  captures, sha256 in `exp08/exp19_g5a_capture_digests.json`; captures themselves out of git, regenerable).
- Floor audit: `exp19_floor.py --cache` (one rebuild pass → `exp19_g5a_strat_cache.json`) then `--audit` →
  `exp19_g5a_floor_audit.json`. Trigger/sensitivity: `exp19_g5a_fork.py --trigger|--sensitivity`.
- All numbers COMPUTED (pinned SIM_SEED; deterministic `torch.set_num_threads(1)`); committed
  `exp12_arms.py`/`exp14_arms.py` behaviour untouched (capture monkeypatch-scoped; runs use `out_tag`).
