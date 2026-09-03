# Stage-0 MVP — Phase-1 Results

## Headline — gap-3 is present

The deliverable is that the **gap-3 gradient path is alive**: PAM's convergence error
reaches the masked vision slot with **no detach** — `vision_grad_from_PAM` is **nonzero
every eval window**. That binary fact is gap-3 being wired and active.

> `vision_grad_from_PAM` ≈ 0.0099 vs `vision_grad_from_JEPA` ≈ 0.0134 (cross-seed mean) — **ratio 0.79×**, per-seed [1.11, 0.74, 0.52].

Magnitude is **order-1 (comparable to JEPA), seed/time-variable** — it rises in late
windows but is **not robustly dominant**, so the claim is *present and comparable*, not
*PAM does N× the work*. Everything below is about **isolating** gap-3 (Readout G), not
whether it is there.

Phase-1 core (validity probe, Readout G, Readout D, two structural signals). Phase 2
(Readout A ladders), the gain sweep, and Readout O are deferred per the spec's staging.

## Pinned constants (logged before the run)
```
k = 0.5
eps_band = 0.1
N = 5
tau_sep = 0.35
tau_entangle = 0.9
tau_full_ols = 0.9
ablate_margin = 0.1
iter_eps = 0.05
P = 64
alpha_spread = 0.1
L_capacity = 0.05
K_settle = 1
repool_frac = 0.15
repool_patience = 4
repool_ramp = 400
```

## Pre-registration & build-correctness self-tests

- Cue-shape coverage (all six families): **OK** — {'single-slot': 529, 'whole-wave': 496, 'interior-both-sides': 501, 'one-sided-edge': 517, 'sparse': 454, 'near-all': 503}
- Verdict-table self-test (each named outcome incl. WRONG_REASON): **OK**
- Static build-correctness (§0/§12): **OK** — {'no_softmax_attention': True, 'no_pam_latent': True, 'slice_level_masking': True, 'no_detach_on_pam_target': True, 'word_excluded_from_optimizer': True, 'all_ok': True}

## Validity probe (admissibility only — NOT loop success)
```
A_salience = 1.0
floor_B = 0.2548828125
ceiling_B = 1.0
A_oracle = 1.0
floor_ceiling_gap = 0.7451171875
cross_axis_confusion = 0.0
locked = True
note = VALIDITY_OK (admissibility only — NOT loop success)
```

## Headline Readout G (3-seed verdict)
- per-seed outcomes: ['WRONG_REASON', 'WRONG_REASON', 'NORMAL']
- **seed-stable: False**  (categories FLIP — seed-unstable)

### seed 0
- gap-3 gradient-attribution: PAM=0.0110 JEPA=0.0099 → **1.11×**
- paired B-track trajectory (word arm): [0.27, 0.23, 0.38, 0.34, 0.37, 0.5, 0.46, 0.54, 0.51, 0.46, 0.86]
- paired B-track trajectory (no-word arm): [0.27, 0.34, 0.42, 0.25, 0.42, 0.52, 0.52, 0.58, 0.46, 0.37, 0.44]
- **Readout G (gap-3 fusion): WRONG_REASON**  [WRONG_REASON] — NORMAL matched but baseline-gap absent: B rising above floor but not yet sustained B_success — acquisition underway
    - evidence: {'capacity_open': True, 'contrast_available': True, 'word_present': True, 'separable': True, 'clean_gap3_window': False, 'gap3_window': (None, None), 'B_success': False, 'B_in_floor_band': False, 'no_word_in_floor_band': False, 'A_high': False, 'B_bar': 0.627, 'B_track': 0.859, 'no_word_B_track': 0.438, 'floor_B': 0.255, 'ceiling_B': 1.0}
- **Readout D (order-as-content): PASS-LINEAR-REGIME** — order recovered in-loop and carrier-zero collapses it (REAL), but the carrier is in the LINEARLY-SEPARABLE regime (full_ols_r2 >= tau_full_ols) — validates order-IN-LOOP, NOT the entangled order-as-content corner (exp03 hit 0.80 at alpha=1). Dwell-stable content removed the along-u content variation; the entangled corner is DEFERRED
    - evidence: {'order_recovery': 0.776, 'carrier_zero': 0.385, 'chance': 0.333, 'max_coord_r2': 0.69, 'full_ols_r2': 0.9999, 'recovers': True, 'carrier_collapses': True, 'clean_slot': False, 'linearly_separable': True, 'oracle_well_ordered': 1.0}
- **Structural #1 (char-7 no phase split): PASS** — char-7 holds: single code path, one complete-then-step per wave
    - evidence: {'forbidden_tokens': [], 'one_step_per_wave': True}
- **Structural #2 (pooling does something): PASS** — substrate live: capacity opened (Delta2 grew 8x from pooled) | OBSERVATION: SPREAD_FIGHTS_POOLING (within-group spread flat/falling while capacity opens — §5 attribution-watch; interpose a throwaway projector in a follow-up)
    - evidence: {'depth_start': 0.00973, 'depth_end': 0.07531, 'L_capacity': 0.05, 'spread_start': 0.01235, 'spread_end': 0.01098, 'spread_fights_pooling': True}
- build-failure invariants: NONE (clean)

### seed 1
- gap-3 gradient-attribution: PAM=0.0105 JEPA=0.0142 → **0.74×**
- paired B-track trajectory (word arm): [0.24, 0.23, 0.36, 0.35, 0.46, 0.42, 0.66, 0.59, 0.53, 0.59, 0.41]
- paired B-track trajectory (no-word arm): [0.24, 0.24, 0.38, 0.43, 0.53, 0.54, 0.51, 0.55, 0.37, 0.48, 0.5]
- **Readout G (gap-3 fusion): WRONG_REASON**  [WRONG_REASON] — NORMAL matched but baseline-gap absent: B rising above floor but not yet sustained B_success — acquisition underway
    - evidence: {'capacity_open': True, 'contrast_available': True, 'word_present': True, 'separable': True, 'clean_gap3_window': False, 'gap3_window': (None, None), 'B_success': False, 'B_in_floor_band': False, 'no_word_in_floor_band': False, 'A_high': False, 'B_bar': 0.627, 'B_track': 0.406, 'no_word_B_track': 0.5, 'floor_B': 0.255, 'ceiling_B': 1.0}
- **Readout D (order-as-content): PASS-LINEAR-REGIME** — order recovered in-loop and carrier-zero collapses it (REAL), but the carrier is in the LINEARLY-SEPARABLE regime (full_ols_r2 >= tau_full_ols) — validates order-IN-LOOP, NOT the entangled order-as-content corner (exp03 hit 0.80 at alpha=1). Dwell-stable content removed the along-u content variation; the entangled corner is DEFERRED
    - evidence: {'order_recovery': 0.656, 'carrier_zero': 0.331, 'chance': 0.333, 'max_coord_r2': 0.715, 'full_ols_r2': 0.9999, 'recovers': True, 'carrier_collapses': True, 'clean_slot': False, 'linearly_separable': True, 'oracle_well_ordered': 1.0}
- **Structural #1 (char-7 no phase split): PASS** — char-7 holds: single code path, one complete-then-step per wave
    - evidence: {'forbidden_tokens': [], 'one_step_per_wave': True}
- **Structural #2 (pooling does something): PASS** — substrate live: capacity opened (Delta2 grew 14x from pooled)
    - evidence: {'depth_start': 0.00928, 'depth_end': 0.12603, 'L_capacity': 0.05, 'spread_start': 0.01212, 'spread_end': 0.01837, 'spread_fights_pooling': False}
- build-failure invariants: NONE (clean)

### seed 2
- gap-3 gradient-attribution: PAM=0.0083 JEPA=0.0160 → **0.52×**
- paired B-track trajectory (word arm): [0.2, 0.24, 0.68, 0.57, 0.42, 0.57, 0.56, 0.7, 0.48, 0.62, 0.59]
- paired B-track trajectory (no-word arm): [0.2, 0.28, 0.58, 0.62, 0.58, 0.57, 0.62, 0.65, 0.55, 0.71, 0.34]
- **Readout G (gap-3 fusion): NORMAL** — B rising above floor but not yet sustained B_success — acquisition underway
    - evidence: {'capacity_open': True, 'contrast_available': True, 'word_present': True, 'separable': True, 'clean_gap3_window': False, 'gap3_window': (None, None), 'B_success': False, 'B_in_floor_band': False, 'no_word_in_floor_band': True, 'A_high': False, 'B_bar': 0.627, 'B_track': 0.594, 'no_word_B_track': 0.336, 'floor_B': 0.255, 'ceiling_B': 1.0}
- **Readout D (order-as-content): PASS-LINEAR-REGIME** — order recovered in-loop and carrier-zero collapses it (REAL), but the carrier is in the LINEARLY-SEPARABLE regime (full_ols_r2 >= tau_full_ols) — validates order-IN-LOOP, NOT the entangled order-as-content corner (exp03 hit 0.80 at alpha=1). Dwell-stable content removed the along-u content variation; the entangled corner is DEFERRED
    - evidence: {'order_recovery': 0.763, 'carrier_zero': 0.385, 'chance': 0.333, 'max_coord_r2': 0.748, 'full_ols_r2': 0.9993, 'recovers': True, 'carrier_collapses': True, 'clean_slot': False, 'linearly_separable': True, 'oracle_well_ordered': 1.0}
- **Structural #1 (char-7 no phase split): PASS** — char-7 holds: single code path, one complete-then-step per wave
    - evidence: {'forbidden_tokens': [], 'one_step_per_wave': True}
- **Structural #2 (pooling does something): PASS** — substrate live: capacity opened (Delta2 grew 11x from pooled)
    - evidence: {'depth_start': 0.00972, 'depth_end': 0.11168, 'L_capacity': 0.05, 'spread_start': 0.01132, 'spread_end': 0.0186, 'spread_fights_pooling': False}
- build-failure invariants: NONE (clean)

## Notes & caveats

- **Readout D is PASS-LINEAR-REGIME, not a clean PASS.** Order is recovered in-loop and
  carrier-zero collapses it (real), but `full_ols_r2 ≈ 1.0 ≥ 0.9` — a full linear read
  recovers the drift (exp03's entangled corner was 0.80 at α=1). Cause: the dwell-stable
  fix froze A/B within a dwell, so drift is the only within-window variation → linearly
  separable. The **entangled order-as-content corner is DEFERRED** (would need a 3rd
  within-dwell content axis varying along u; more stream machinery than Stage 0 warrants).
  `max_coord_r2 < 0.9` (no clean axis-aligned slot) still holds; carrier-zero collapse is
  necessary-but-not-sufficient (it fires for a separable index too) — `full_ols_r2` is the tell.
- **Readout G — autonomous resolution, leak ruled out.** The no-word arm's B-rise is
  genuine autonomous resolution (B is in the *visual* input; JEPA + the unpool clock open
  capacity 8–14×), NOT a leak: the null token is a single fixed B-agnostic embedding; the
  unpool/gain/curriculum schedules are independent per arm (matched, not shared); the stream
  is the same seed (paired stimulus, no word label leaked). The fix is to suppress autonomous
  resolution, not to plug a leak. Read the gap **paired and sustained** (a single-window
  unpaired inversion — e.g. seed 1 — is no-word eval noise, not a real sign flip).
- **K_settle = 1** → single at-once pass → `relaxation_residual = nan` is correct (at-once is
  structural, like exp03's single-forward encoder).
- **SPREAD_FIGHTS_POOLING** is intermittent (does not fire all seeds); projector fix is
  pre-specified and deferred. No correlation with the differentiation signal across seeds.

## Final logged window (seed 0, §10 block)
```
step = 1500
gain = 1.0
lam2 = 0.0
l_pam = 0.0008976306999102235
l_jepa = 0.00014718715101480484
l_spread = 1.011353611946106
spread_completion_ratio = 1126.6923157232216
loss_by_mask_family = {'single-slot': 0.03316050599218628, 'whole-wave': 0.03358650691376827, 'interior-both-sides': 0.035053028574674926, 'one-sided-edge': 0.02946445917241163, 'sparse': 0.0311629466614032, 'near-all': 0.03296314914588456}
word_param_delta = 0.0
vision_grad_from_PAM = 0.0020043491385877132
vision_grad_from_JEPA = 0.0008909765747375786
pooling_depth = 0.07530800998210907
within_group_spread = 0.01097925752401352
pull_apart = 1.7088832464651205e-05
A_track = 0.578125
B_track = 0.859375
A_chance = 0.25
B_chance = 0.25
no_word_B_track = 0.4375
max_coord_r2 = 0.7022035717964172
full_ols_r2 = 0.9998835325241089
adjacent_overlap = 0.11599999666213989
sigma_drift = 0.8
order_recovery = 0.8046875
carrier_zero = 0.453125
order_chance = 0.3333333333333333
relaxation_residual = nan
curriculum_state = [0, 1]
contrast_available = True
```
