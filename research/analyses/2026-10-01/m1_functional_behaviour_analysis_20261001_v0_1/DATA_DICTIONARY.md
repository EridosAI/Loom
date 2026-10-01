# Review package data dictionary

All ages are actual bodily seconds. Length, speed, impulse, expenditure and reserves use the unchanged Loom world units. All products are **NON-CANONICAL RESURRECTION SANDBOX — PASSIVE ANALYSIS**. There is no controller, launch authority or live model in the viewer.

## Reports, figures and numerical series

- `FUNCTIONAL_EXPRESSION_OVER_TIME_v0_1.md`: primary findings, six functional and eight behavioural questions, biographies, limits and required ending sections.
- `BEHAVIOURAL_DEVELOPMENT_WATCHLIST_v0_1.md`: reusable ten-family observer watchlist; not canon or a score.
- `REVIEW.html`: local, self-contained image browser. Open directly; no server required. Its JavaScript switches images only.
- `figures/`: twelve ten-panel functional figures, twelve six-panel coupling figures, four population overlays and one behavioural dashboard, each PNG and SVG. **29 figures / 58 files.** Pilot and censor status is visible. SVG provides scalable export.
- `series/*_FUNCTIONAL.npz` and `.csv.gz`: measured-wave operands and exact one-operation receiver algebra. Signed `*_current_delta`, `*_command_delta`, `*_full_delta` retain two coordinates in NPZ; CSV expands left/right. `*_effect` denotes paired RMS. `*_over_M1` uses trailing-60-s RMS ratios; `*_over_M1_same_receiver` compares to a local M1 omission. Bank-zero ratios are NaN/undefined, not zero. No infinities are allowed. H/q/use are same-wave stored quantities; motor diagnostics use previous-wave controls, explicitly aligned.

## Functional tables

| Table | Contents / limits |
| --- | --- |
| `FUNCTIONAL_AGE_BANDS.csv` | Early/middle/late, final1000 and fixed300/600 windows; raw means/RMS and incoming/current-command ratios |
| `FUNCTIONAL_LOCAL_SLOPES.csv` | Theil–Sen and OLS slopes from five-second medians; `predicted_change` = slope × window duration, not a future prediction; no significance test |
| `FUNCTIONAL_SCALE_COMPARISON.csv` | Early/late learned current, one-operation current-only command, full attenuation-inclusive receiver effect; input and same-receiver M1 denominators |
| `STRUCTURE_EXPRESSION_ASSOCIATIONS.csv` | 300-s level, first-difference and linear-age-detrended correlations; descriptive, serially dependent |
| `SPARSE_ASSOCIATIVE_FEATURE_EFFECT.csv` | 807 exact checkpoints: q-feature input/phi/current/support/attenuation effects, separate current/support/attenuation row norms, learned logits and bias terms; preserves stored feature body operands |

## Physical tables

| Table | Contents / denominators |
| --- | --- |
| `BEHAVIOURAL_AGE_BANDS.csv` | 35 fixed-seven rows plus five unequal whole-history rows; physical time/path, events, exposure, E/I, motion and spatial metrics |
| `FIXED_SEVEN_BAND_TOTALS.csv` | Pooled sums/rates for the same seven lives in all five bands; no changing-denominator population curve |
| `AGE_BAND_STATUS_ANNOTATIONS.csv` | Descriptive direction against preceding band; no opportunity, mixed and unresolved labels; no composite score |
| `BEHAVIOURAL_60S.csv` | Same quantities in 60-s windows; final partial window retained but excluded from phase search |
| `SOURCE_BOUTS.csv` | Every grouped bout, physical transfer/contact, E/I, source stock, actual positions used only externally, true departure/revisit flags, latency/path and retention proxies |
| `COLLISION_BOUTS.csv` | Positive instantaneous impulses grouped within one second on the same collider; sum/peak and isolated closing-speed information |
| `HAZARD_APPROACHES.csv` | Gap-entering closing episodes with exact observer geometry, collision/contact flags, censor status and E/I/speed/family strata |
| `DEFINITION_SENSITIVITY.csv` | Two alternate hazard thresholds; nine source contact-gap/clearance grouping definitions; conserved total time/transfer |
| `CAPABILITY_SHARED_STRATA.csv` | Actual early/late same-life/family/E/I/speed overlap, weights and outcomes; only three approaches in each period overlap |
| `CAPABILITY_STANDARDIZED_HAZARD_COMPARISON.csv` | Standardization restricted to common support; no extrapolation to unmatched hazards |
| `SOURCE_NEIGHBORHOOD_RETURNS.csv` | Entry gap≤1, exit>1.5, birth-near/return/consequence/censor flags, return time/path |
| `RETURN_AND_REPAIR_OPPORTUNITIES.csv` | Per-life distinct sources, true returns, switchbacks, neighbourhood departure counts and observed return fractions, damaged restorative approaches and global repair |
| `REPAIR_AFTER_DAMAGE.csv` | First new subsequent repair, latency/path, repair before next damage, available repair opportunities and right-censoring; not an independent sample per row |
| `RESURRECTION_INTERVALS.csv` | Every birth/support-to-support interval plus administrative or host-censored tail; environmental fraction = source/expenditure; no external E counted as source |
| `ENERGY_EPOCH_TRENDS.csv` | Completed energy-ended epochs only, duration and intake trends; administrative tails separate |
| `SUPPORT_MARGIN_SENSITIVITY.csv` | Early/late observed-state summaries excluding ±0/5/30/60 s around actual support; not a no-support counterfactual |
| `SELECTED_BIOGRAPHICAL_EVENTS.csv` | Explicitly retrospective per-life maximum source transfer and maximum total contact damage, with time/collider/force context |

Physical energy/damage/repair are assigned by recorded event endpoint. Fine contact fragments allocate contact duration at a boundary; whole-bout means and peak statistics are assigned to onset. Positive-impact damage excludes continuous stress; total physical damage includes it. Contact seconds use native contact indicators for all surfaces; source-contact duration uses fine per-source fragments. Effort is the unchanged command-cost term, not total expenditure. Coverage uses 0.25-unit cells. Occupancy entropy uses native sample occupancy (an approximation to time occupancy where terminal fractional native steps occur). Pinned = contact and speed<0.005. Rotation/path is integrated absolute body angular speed divided by path. Forward/reverse bouts use body-relative speed±0.01 with duration≥0.1 s. A “short bout” lasts<1 s. Empty denominators produce blank cells, not zero success. `max_collision_impulse=0` with no collision denotes a zero observed maximum; consult collision count.

`environment_fraction_of_inputs` in the pooled table means source/(source + resurrection injections), **excluding birth reserve**. `environment_fraction_of_expense` and interval `environment_fraction` mean source/expenditure. Never confuse these ratios or treat injections as learned productive intake.

Neighbourhood observed return fractions are not censor-adjusted survival probabilities. Every completed departure counts; no observed return by the evidence boundary remains censored. Different-source switchback means A→B→A in a source-contact sequence (possibly with intermediate local A/A or B/B contacts), not a claim of a planned route.

## Context and phase tables

| Table | Contents / limits |
| --- | --- |
| `CONTEXT_QUERIES.csv` | All declared collision, productive source, unselected early, chemistry, low-E and post-impact queries, including exclusions/no matches |
| `CONTEXT_PAIRS.csv` | Main k=3/cap1 pairs, distance/calipers and both ten-second outcomes; `*_observer` geometry/identity columns are outcomes, not features |
| `CONTEXT_SENSITIVITY.csv` | Per-query k=1/3/5 × cap0.5/1/2; no-match rows remain |
| `CONTEXT_SUMMARY.csv` | Per-life pair-weighted descriptive summary |
| `FIXED_SEVEN_CONTEXT_COMPARISON.csv` | Equal-query population weighting; all, both-hazard and both-source-near subsets |
| `FIXED_SEVEN_CONTEXT_SENSITIVITY.csv` | Equal-query results for all nine k/cap settings |
| `CONTEXT_EXTENDED_OUTCOMES.csv` | Closing, signed normal-turn proxy, command change, separation/censoring, damage, source-distance change, mean action and persistence; support-free follow-up subset |
| `CONDITIONAL_ACTION_CONSISTENCY.csv` | Outcome-independent early anchors, early and late neighbour sets, counts and paired conditional dispersion; k=3/5 |
| `CONDITIONAL_CONSISTENCY_SUMMARY.csv` | Fixed-seven summaries, only queries with ≥2 matches in both periods for dispersion; count/life denominator retained |
| `EXPLORATORY_PHASE_CANDIDATES.csv` | Every tested two-segment split on complete 60-s windows; missing-opportunity windows retained; no significance claim |
| `INTERNAL_BEHAVIOURAL_COVARIATION.csv` | Concurrent and next-window correlations of internal expression with behaviour; not causal |

Context feature files `cache/*_PERMITTED_CONTEXTS.npz` have only age, 48 permitted features, contact-free mask and normalized feature array. `CONTEXT_FEATURE_AUDIT.json` binds family slices, IQR scales and weights. Observer geometry lives in separate `*_OBSERVER.npz`/`*_EVENTS.json` files and never enters normalized distances. Runtime controller inputs are unchanged because no controller runs.

## Reproduction and custody

Analysis sequence: `functional.py`, `behaviour.py`, `contexts.py`, `coupling_checkpoints.py`, `conditional_consistency.py`, `review_checks.py`, `finish_tables.py`, `postprocess.py`, `plot_results.py`, `write_reports.py`, package verification. Plotting uses a separate installed Python with Pillow/ReportLab; numerical analysis uses the existing NumPy/SciPy environment. No dependency installation occurred. These are local analysis scripts, not production modifications.

The scripts reference the immutable prior extracted native/wave caches and evidence tree by sibling paths. `ANALYSIS_INPUT_HASHES.json` gives exact absolute locations and hashes; the review archive is portable for **review**, not self-contained with the multi-gigabyte raw experiment. It contains series, copied permitted contexts, observer summaries, event tables, methods, verification and source scripts. Original raw evidence remains in its separately sealed archive. A reproduction needs that original evidence and the prior decoder/cache package at the documented paths, or explicitly adjusted analysis-only paths.

The input decoder extracts a single plain-data decoding function from preserved source; it does not instantiate live engine classes. Verification independently rearranges the bankwise readout equation and reconciles ledgers, feature allowlists, timing and custody. `REVIEW_VERIFICATION.json` records zero model steps/RNG draws/alternate trajectories/production edits. Prior code/runtime identities are rechecked rather than silently reconciled. `PACKAGE_MANIFEST.json` and the adjacent archive record bind all delivery files.
