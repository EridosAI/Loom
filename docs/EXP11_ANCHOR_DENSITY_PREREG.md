# EXP11 — The anchor-coverage ladder (acquisition-aligned, both axes): does a denser/wider frozen reference keep routing input-sensitive?

**STATUS: DRAFT AT CHECKPOINT (2026-07-04, REVISED after pre-commit verification — two
BLOCKERS fixed: the verdict axis is now acquisition-aligned, and the horizon is set from
a measured per-rung onset pre-flight, not a conflated pin clock). Nothing is built;
nothing runs until Jason ratifies the [RECONCILE] items in §9. Gate steps 5–6 stay
BLOCKED. The ladder measures the lever — adoption of any rung is a separate ruling; no
arm is a fix.**

The ruling (FRONTIER §10.16): after two regimes hit the same wall (EXP09 slow-reference,
EXP10 variation — the detach-null matches or beats every target-side / input-side
intervention because nothing touches what keeps ROUTING differential), the next move is
the denser/wider ANCHOR, before any counter-force. The anchor is stimulus-side, no new
machinery, and its lever is genuinely UNMEASURED — the EXP08 ladder read it at a fixed
30k budget and got only a **seed lottery** (below). EXP10 built the instrument that fixes
the alignment problem — the acquisition-aligned read.

**The question, stated once: does naming more of the space keep routing input-sensitive —
the anchor shifting from ACCELERANT (2 tokens; the collapse's pin-deepener) to SCAFFOLD
(coverage of the axes that die first)?** Mechanism hypothesis: at v2 the word names only
the category axis, so its frozen target set is 2 points — it cannot hold the distractor /
A axes that die (§10.12: "a failed 2-point anchor"). At v16 the word names full member
identity, so the reference offers 16-target diversity covering every axis — the §5
"target-diversity removes collapse as a global optimum" mechanism, scaled up. Does the
routing collapse (input-sensitivity → floor) get prevented or delayed as coverage rises?

**VARIABLE NAME — COVERAGE, not "density" (verification correction).** The nested ladder
steps CARDINALITY (2→4→8→16 tokens) and AXIS-COVERAGE (which of {A, distractor, category}
the word names) TOGETHER — they are perfectly collinear here, so an effect cannot be
attributed to count vs named-axes within this ladder. The mechanism hypothesis rests on
COVERAGE (naming the dying axes); the primary variable is named accordingly. The
cardinality-vs-coverage discriminator (the coarse-first / coverage-matched ladder) is
PARKED (§8), triggered by a positive result.

---

## 1. Arms — the nested ladder (ratified)

Fixed label maps, geometry untouched (the EXP08 LADDER, verbatim; verified against
`exp08_arms.py`): `v2 = b%2` (category only — the deployed reference) · `v4 = b`
(distractor × category) · `v8 = (a%2)·4+b` (half the coarse axis + both fine) ·
`v16 = a·4+b` (full member identity). Static environment (EXP08 comparability — NO
variation; the varied ladder is parked, §8).

**Teaching-fence intact (binding, from the EXP08 prereg):** v≥4 cells are NEVER teaching
evidence — at v4+ the word names the distractor too, so the conflict premise (word
redirects occupancy from the salient-inert distractor to the subtle-named category) is
broken. **EXP11 reads COVERAGE-ON-ROUTING-SURVIVAL only, never "the word teaches the
right distinction."**

**Seed budget — sized against the acquisition lottery (verification blocker fix).** The
EXP08 3-seed read was an ACQUISITION SEED LOTTERY, not a clean signal (§ below), so
**≥5 verdict seeds per rung** `[RECONCILE]`, chosen so every rung reaches **≥3 ACQUIRED
seeds** (§3 censoring); if a rung falls short, seeds are added to THAT rung before any
verdict (pre-committed, not improvised). Plus a dedicated **calibration seed set (never
verdict seeds)** for the §2 pre-flight and §7 in-regime constants.

## 2. Horizon — set from a MEASURED per-rung onset pre-flight (verification blocker fix)

The first draft justified 160k from the word_terminal PIN onset (75.3k — a deployed-v2,
n=1 COLLAPSE clock), conflating it with a v16 ACQUISITION onset it never measured. Fixed:

- **PRE-FLIGHT (stage-one calibration):** run each rung on the calibration seeds, measure
  the per-rung ACQUISITION-ONSET distribution (num-floor crossing, §3). This is the only
  way to size the horizon for the slowest rung.
- **HORIZON = max(measured acquisition onset across rungs) + W_post + margin**, where
  W_post = the matched post-onset verdict window (§3), so EVERY acquired rung gets a full
  W_post of post-acquisition run inside the horizon. `[RECONCILE: W_post + margin at the
  stage-two read]`. If the pre-flight shows a rung's onset so late that HORIZON is
  infeasible, that rung is reported ACQUISITION-CENSORED and the ladder is read on the
  rungs that fit — surfaced, never forced.

## 3. The two axes — BOTH acquisition-aligned (verification blocker fix)

The first draft aligned the PRIMARY read to onset but took the VERDICT at a fixed absolute
horizon — which reintroduces the confound: a denser rung acquires later, so at a fixed
horizon it has undergone FEWER post-acquisition collapse periods, and would look
"survives better" purely from having less time to die. Fixed — both axes align to each
rung's own onset:

- **Acquisition onset (per rung, per seed):** num ≥ 0.01 in ≥2 consecutive windows (the
  EXP10 harness verbatim). Never-crossed by horizon = **ACQUISITION-CENSORED** (unread,
  never a null — the EXP08 lesson made a rig outcome).
- **PRIMARY axis — acquisition quality, aligned:** k-window means from each rung's own
  onset (the matched-bar idiom) — num/den/asg at matched acquisition STATE.
- **VERDICT axis — routing survival over a MATCHED POST-ONSET WINDOW:** read routing
  input-sensitivity across `[onset, onset + W_post]` for every rung, the SAME W_post in
  collapse-periods (not absolute time). This compares rungs at matched collapse-phase, so
  "denser survives more" cannot be an artifact of later acquisition. `W_post` spans ≥ N
  collapse periods so survival-vs-collapse is observable `[RECONCILE at stage-two]`.
- **The verdict quantity is asg_dist (input-sensitivity), NOT asg_argmax_k count** (the §6
  crutch screen): does assignment DIFFER across inputs over the matched post-onset window,
  and does that survival rise with coverage.

## 4. THE CENTRAL CONFOUND — anchor-geometry degradation (pre-registered, measured over the PER-RUN anchors)

Denser rungs pack more frozen tokens into fixed D=16, so per-token separation degrades.
**Measured over the ACTUAL per-run anchor seeds (WordCortex seed = cfg.seed+1; verdict
seeds → word seeds {1,2,3}), incl. null token:** pairwise MIN separation (mean over
seeds) **1.208 (v2) → 1.120 (v4) → 1.046 (v8) → 0.889 (v16) — a ~26% MIN drop across the
ladder** (single-anchor-seed=1 gives 41%; the per-run mean is the representative figure),
while the MEAN holds ~1.39–1.43. So "denser survives less" could be COVERAGE or DEGRADED
per-token separation — inseparable at fixed D.

**Guards + the pre-registered reading fork** (anchor pairwise min+mean logged per run —
verified the EXP08 manifest already emits `pairwise_separation`; the §9-item-3 tolerance
is calibrated against the PER-RUN anchor distribution, not the seed-1 outlier):
- **(a) denser survives MORE despite degrading min-separation → the coverage-scaffold
  effect DOMINATES** (clean positive — ran uphill against the confound).
- **(b) denser survives LESS AND min-separation degrades → CONFOUNDED**; ambiguous,
  routes to the matched-separation follow-up (§8), NOT a null on coverage.
- **(c) denser survives MORE AND min-separation holds within tolerance → cleanest.**
The matched-separation control (hold min-separation constant across rungs) is a geometry
change → its own checkpoint, PARKED, triggered by fork (b).

## 5. Pre-registered outcomes + wrong-reason candidates

The EXP08 acquisition record, stated straight (verification): at fixed 30k the ladder is
an **ACQUISITION SEED LOTTERY** — acquired-seed counts v2 **1/3** (the SPARSEST rung is
the WORST), v4 3/3, v8 2/3, v16 2/3; num finals medians 0.00/0.63/0.19/0.36; the means
(2.26/2.30/0.19/0.77) are each dominated by ONE spiking seed. This is NOT a monotone
"dense under-acquired" curriculum lag — it is noise at a fixed budget, which is exactly
why the lever is unmeasured and EXP11 re-reads acquisition-aligned with a lottery-sized
seed budget.

- **ACQUISITION-CENSORED** (per rung/seed): onset never crossed → no routing verdict;
  reported, never a coverage null.
- **COVERAGE-SCAFFOLD (the sought positive):** matched-post-onset asg_dist survival rises
  monotonically with coverage across ACQUIRED rungs, clearing the §4 geometry fork toward
  (a)/(c) and the §6 crutch screen.
- **COVERAGE-NULL:** aligned-acquired rungs show no monotone coverage effect on routing
  survival → the lever is measured-and-flat (the honest negative EXP08 could not deliver).
- **Wrong-reason candidates (pinned, each with route):** (1) GEOMETRY-NOT-COVERAGE (§4
  fork b → matched-separation follow-up); (2) ACQUISITION-CENSORED (§3 → unread, not a
  null); (3) ANCHOR-AS-CRUTCH (§6); (4) CARDINALITY-NOT-COVERAGE (the count/named-axes
  collinearity → the coarse-first control, §8).

## 6. The ANCHOR-AS-CRUTCH screen (the load-bearing wrong-reason) — with its residual named

A denser anchor could raise routing survival not because routing stays INPUT-SENSITIVE but
because the larger frozen target set mechanically resists collapse. **Form 1 (screened):**
argmax_k held up (many prototypes used) WHILE asg_dist floors — a crutch of prototype
count with input-insensitive assignment. The verdict quantity is asg_dist not argmax_k
count, so Form 1 is caught. (The assignment simplex is over PAM prototypes, not word
tokens — verified: a denser WORD does not mechanically bound asg_argmax_k.)

**Form 2 (RESIDUAL, named — verification catch, NOT fully screened):** a frozen
16-distinct-target reference makes each member's reconstruction target MANDATORILY
distinct, so the MSE loss can mechanically force asg_dist HIGH (target-diversity-forced
assignment) — consistent with BOTH a genuine scaffold AND mechanically-forced input-
sensitivity. asg_dist survival therefore does not by itself *prove* scaffold. **The
discriminating control (PARKED, §8): a matched-diversity anchor that is assignment-
COLLAPSIBLE** (same target cardinality/diversity, but arranged so a collapsed assignment
is still loss-optimal) — if asg_dist survives there too, it was target-diversity forcing,
not coverage-scaffold. Until that control runs, a positive asg_dist result is
COVERAGE-SCAFFOLD-CONSISTENT, not COVERAGE-SCAFFOLD-DEMONSTRATED. This is the same
manufacturing-class concern the counter-force carries, in a milder stimulus-side form —
named here so it is not mistaken for a clean scaffold.

## 7. Readouts + instruments

Standing columns + dynamics panels (the EXP08/09 set): num/den/ratio (den = one-sided
collapse-floor tripwire only), asg_dist / asg_argmax_k / asg_entropy, occupancy dc_track,
proto_spread, grad_split, masking-mix. Acquisition-aligned per-rung reads (§3) both axes.
Anchor pairwise separation per run (§4) logged. **In-regime calibration mandate (§10.14
lesson):** the ladder regime differs from both the EXP09 detach set-point and the static
word-terminal regime — any verdict-taxonomy constant (collapse period, W_post, asg_dist
survival threshold) calibrates on the LADDER's own healthy spans (the dedicated
calibration seeds, never verdict seeds; two-stage as in EXP10). The guarded-v2 scorer
(period-substitution gated, force_period disclosure, mechanical floor checks — the EXP10
fixes) is the scoring instrument. Determinism: threads = 1, recorded. Manifests re-cut
live-derived; illustrative scatter per rung (standing request).

*Supporting fragment, direction-only (verification: method-pinned):* the EXP08 occupancy
category-step (last-block minus first-block `category_track`, mean over seeds) is largest
at v4 (+0.095 by this aggregate; ~+0.07 by others — the number is aggregation-sensitive,
the DIRECTION "largest at v4, where the dead axis first gets named" is robust). Kept as a
directional pointer, not evidence (canon rates the EXP08 ladder statistically flat).

## 8. Parked (with triggers)

- **Cardinality-vs-coverage discriminator** (the coarse-first / coverage-matched ladder) —
  trigger: a positive COVERAGE-SCAFFOLD result, to attribute it to named-axes vs count.
- **Matched-diversity assignment-collapsible control** (§6 Form-2) — trigger: asg_dist
  survives; distinguishes scaffold from target-diversity forcing.
- **Matched-separation control** (§4 fork b) — trigger: denser survives less AND
  separation degrades; its own checkpoint (geometry change).
- **Varied-environment ladder** — trigger: coverage holds routing open in static; tests
  whether coverage + variation compose.

## 9. Checkpoint list — ALL RATIFIED (Jason, 2026-07-04)

1. **Seeds: ≥5 verdict/rung; decisive rungs MUST reach ≥3 ACQUIRED — if a rung can't
   after ONE +2 extension, it is reported ACQUISITION-STARVED, not extended again. Cal
   seeds DISTINCT from verdict seeds.** (verdict {0–4}, +2 pool {5,6}; cal {20,21}.)
2. **Pre-flight + horizon RATIFIED as drafted:** stage-one measures per-rung
   acquisition-onset (+ collapse period); HORIZON = max measured onset + W_post + margin;
   infeasible rung → CENSORED, ladder read on the rungs that fit.
3. **W_post = ≥3 collapse periods in the RUNG'S OWN regime** (per-rung period from
   stage-two, not a shared constant); the asg_dist survival threshold from IN-REGIME
   stage-two calibration, NEVER static constants.
4. **Geometry fork: tolerance from the PER-RUN distribution; the matched-separation
   control RUNS ALONGSIDE** (cheap, and the confound is live at ~26%). Construction
   (ratified): match each rung's MIN pairwise separation to a common target (the densest
   rung's natural min ≈ 0.889) by rotating the closest anchor pair together in its plane
   — UNIT NORM PRESERVED EXACTLY (no magnitude confound); achieved min-sep + mean logged.
5. **Crutch/Form-2 (matched-diversity assignment-collapsible) control: PARKED-UNTIL-
   POSITIVE** — it disambiguates a positive; spending it pre-positive buys nothing. A
   positive asg_dist result stands as COVERAGE-SCAFFOLD-CONSISTENT until it runs.
6. **Adoption clause RATIFIED VERBATIM:** a scaffold rung is a FINDING; adoption is a
   SEPARATE ruling (the deployed word names category only by design).
7. **Probes: ride along READ-ONLY if zero marginal runs; else DROP.** (The EXP09/EXP10
   decomposition probes are read-only per-eval on the same run — zero marginal runs — so
   they ride; the slow-reference columns are dropped, no slow copy here.)

**Sequence: build → pre-flight → arms → one review. Steps 5–6 blocked.**
