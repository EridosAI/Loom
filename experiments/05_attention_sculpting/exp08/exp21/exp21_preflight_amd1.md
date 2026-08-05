# EXP21 — TOUCH-2 AMD-1 SUPERSEDING PRE-FLIGHT (2026-08-05)

Supersedes `exp21_preflight.md` (commit `eae40d5`) in exactly ONE semantic respect; everything
else stands as committed.

- **G0–G3b remain CLOSED and are NOT rerun.** Calibration and every constant remain valid:
  `cut_constants` recomputed from the committed calibration artifacts reproduces
  `exp21_constants.json` EXACTLY (theta_cat 0.5380859375);
  all 19 bank rebuilds hash-identical; all 10 calibration series from-raw digit-exact;
  shared learner/generator chain byte-identical to the prereg baseline (G1 rerun, zero
  violations, B11 both arms green).
- **The only semantic change:** the GENERAL-STABILISATION competing-axis set —
  `max(adv["coarse_a"], adv["distractor"], adv["member"]) >= adv_cat` → `max(adv["coarse_a"], adv["distractor"]) >= adv_cat`
  (Jason-ratified AMD-1; §4.7 governs over the §5 shorthand; member and participation ratio
  remain broad-viability guards, category-collapse/compression guards, and reported
  companions).
- **AMD-1 fixtures all passed after their observed-red forms:** member-only improvement
  (TEACHING-ADDED and PRESERVATION-ONLY setups) — pre-AMD-1 three-axis expression shown to
  misclassify both as GENERAL-STABILISATION (observed red), deployed scorer routes the
  causal cells; coarse-A breadth fires; distractor breadth fires; rank-only movement does
  not fire (companion reported). Full pre-existing suite (13 cells + 3 reds) green through
  the AMD-1 scorer: `exp21_score_fixtures_amd1.json` (the old fixture artifact is
  preserved, not overwritten).
- **Verdict seeds remain untouched:** G4 NOT RUN; zero verdict artifacts at amendment time.

Hashes: constants `59ede2ff84d6bcc0…`, calibration
`974cb495d2abb91f…`, scorer `f0db8ab63d3ce9d0…`
(full values in `exp21_preflight_amd1.json`).
