# EXP21 — TERMINAL SURFACE (G6; assembled mechanically; attribution and canon are Jason's — Touch 3)

**No attribution below. SEED-SPLIT licenses NO pooled causal sentence (§4.6): seeds are reported
separately.** Law: theta_cat 0.5380859375, frozen AMD-1 scorer (commit 520a51d),
restriction False (dynamic range BOTH-QUESTIONS-LIVE).

## The result (per-seed, the committed law; bare N = 8 paired seeds)

**Cohort: SEED-SPLIT** — counts {'CATEGORY-COLLAPSE-IN-COSTUME': 5, 'NO-EFFECT': 3}; grounds: top 5 < 7, no opposite-signed
route, no heterogeneous-causal pair. TEACHING-ADDED's extra law not reached.

| seed | route | ON acq | ON area | ON FQ | OFF acq | OFF area | OFF FQ | adv_cat | OFF viable |
|---|---|---|---|---|---|---|---|---|---|
| s0 | CATEGORY-COLLAPSE-IN-COSTUME | 207000 | 0.002770 | 0.0952 | None | 0.000000 | 0.0000 | +0.0128 | Y |
| s1 | NO-EFFECT | None | 0.002615 | 0.0476 | None | 0.000383 | 0.0000 | -0.0043 | Y |
| s2 | CATEGORY-COLLAPSE-IN-COSTUME | 663000 | 0.002824 | 0.2976 | None | 0.000000 | 0.0000 | +0.0412 | Y |
| s3 | NO-EFFECT | None | 0.001949 | 0.0357 | None | 0.000000 | 0.0000 | -0.0099 | Y |
| s4 | CATEGORY-COLLAPSE-IN-COSTUME | 390000 | 0.003166 | 0.1667 | None | 0.000053 | 0.0000 | +0.0181 | Y |
| s5 | CATEGORY-COLLAPSE-IN-COSTUME | 657000 | 0.003910 | 0.0833 | None | 0.000023 | 0.0119 | -0.0051 | Y |
| s6 | NO-EFFECT | None | 0.000486 | 0.0238 | None | 0.000000 | 0.0000 | -0.0046 | Y |
| s7 | CATEGORY-COLLAPSE-IN-COSTUME | 417000 | 0.002338 | 0.2381 | None | 0.000000 | 0.0000 | +0.0195 | Y |

5/8 ON seeds certify category acquisition (onsets 207k-663k); 0/8 OFF seeds certify; 8/8 OFF
viable. Every certifying ON seed trips the pre-registered wrong-reason compression guard.

## Collapse-leg census (from raw; the committed verdict artifact alone cannot show this — panel FLAG)

- **s0**: PR-floor (adv_dist +0.1620, adv_member +0.0117, ON PR_q4 1.000001)
- **s2**: distractor, member, PR-floor (adv_dist -0.1710, adv_member -0.0879, ON PR_q4 1.0)
- **s4**: distractor, member, PR-floor (adv_dist -0.2358, adv_member -0.1145, ON PR_q4 1.0)
- **s5**: distractor, member (adv_dist -0.3196, adv_member -0.2728, ON PR_q4 1.06148)
- **s7**: distractor, member, PR-floor (adv_dist -0.3235, adv_member -0.3456, ON PR_q4 1.00005)

s0 is qualitatively unlike the others: PR-floor ONLY (ON collapses to rank ~1.000) while its
distractor/member baccs IMPROVE. s2/s4/s7 fire all three legs; s5 fires distractor+member with
PR above floor — and s5's certified category episode (onset 657k) had washed out by Q4
(adv_cat -0.005): the '5/8' count must not be glossed as five terminal category gains.

## G6 verification

Core: 16/16 from-raw series digit-exact; 8/8 verdict bank
rebuilds; gradient-census replay vs the committed record: MATCH; all 8 routes + cohort
recomputed exactly. Refute-default panel (5 lenses + adversarial verify): **substance NOT
REFUTED** — independent code reproduced the full verdict bit-exactly; every constant
(theta, delta_point_cat, null exceedance = 4, FQ bound 12/84, guard bars) reproduces exactly.
One confirmed MUST-FIX, record-level only: the gate log lacked G3a/G4 execution events
(both gates' evidence was committed all along: exp21_probe_audit.json at 12f6818; the 16
verdict runs at 38ecf64 behind the ratification artifact). Folded append-only per the
panel's named fix; no number, route, or definition touched.

## Flags riding into the read (all panel-verified; details in exp21_panel.json)

1. s5 composition (mid-run episode, negative terminal adv_cat) — stated above.
2. s0's PR-floor-only fire + the leg census's absence from the verdict artifact — stated above.
3. ON s3 pr_q4 = NaN from ONE degenerate probe read (t=921,000; unique across all 36
   artifacts; training side fully finite; route proven invariant under ANY pr substitution —
   the panel's structural proof supersedes the session-side sensitivity artifact, whose
   ad-hoc provenance is itself flagged). The bare NaN token in exp21_verdict.json is
   strict-JSON invalid; adv_pr for s3 is undefined. Scorer NaN semantics are fail-open —
   inert in this cohort; queued as a next-gate fix with a fired fixture.
4. Reproduction contract is thread-pinned (torch threads = 1, as recorded in every record).
5. delta_acq/delta_ret carry float32 arithmetic at the 1e-10 digit; margins are >= 4 orders
   above. delta_ret's exact-grid hazard (6/84 boundary, s5's paired FQ diff) was latent and
   non-biting (ret_adv never decided any route). q99 = order-statistic convention; provably
   zero effect on theta.
6. The ratification freeze surface omitted the law-bearing modules (exp21_cal/probe/teaching)
   — no drift occurred (git provenance + bit-exact re-scoring); pin the full set next gate.
7. exp21_constants.json's guard_law.general string is the SUPERSEDED pre-AMD-1 text
   (append-only artifact, cut before AMD-1): the deployed law is AMD-1
   (exp21_score.py:177; exp21_touch2_ratified.json ruling 5).

## Sequence from here

**Jason: attribution, canon, close — Touch 3, on his word.** The claim ceiling until then:
the §4.6 SEED-SPLIT letter — seeds reported separately; no pooled causal sentence; nothing
licenses a teaching, preservation, stabilisation, or impedance sentence at cohort level.
