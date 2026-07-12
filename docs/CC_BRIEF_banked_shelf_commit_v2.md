# CC BRIEF v2 — BANKED-SHELF INTEGRATION + COMMIT (SUPERSEDES v1)

**Date: 2026-07-12 · Authority: Jason (design chat, Fable session close). This brief SUPERSEDES `CC_BRIEF_banked_shelf_commit.md` (v1 was never executed; do not commit v1). Scope: docs + one tools file — no harness changes, no interaction with the EXP17 corridor (fully parallel). Author: Jason Dury, no co-author. Push on Jason's word after the checklist reads clean.**

## 1. Complete file inventory (Jason relays; enumerated adds only, no globs)

**To `docs/`:** `MECHANISM_MAP_conversion_gating.md` (v1.0) · `MECHANISM_MAP_v1_2_RECONCILED.md` · `MECHANISM_MAP_v1_1_addendum.md` + `MECHANISM_MAP_ADDENDUM_v1_1_reality_ladder.md` (superseded forks, retained as provenance — verify both status lines say so) · `EXP18_CONVERTS_BRANCH_PREREG.md` · `EXP_L2_HANDHELD_PREREG.md` · `RED_TEAM_banked_shelf.md` · `FUTURES_after_the_loop.md` · `PROJECT_OPS_POSITIONING.md` · this brief · plus `HANDOFF_next_design_chat_exp17.md` and `EXP17_ORBIT_RULINGS_RELAY.md` **if not already committed** (check first).

**To `tools/`:** `verify_toolkit.py`.

Every status line must carry its tier (BANKED / BANKED-CONDITIONAL / SPECULATION / OPS). Nothing in this commit is canon-verdict material — verify no file reads as one.

## 2. The toolkit's special handling (read carefully — its value is its independence)

`tools/verify_toolkit.py` is a **deliberately independent second implementation** of every load-bearing read, written from the prereg definitions. **Pins:** (a) it must NEVER import from or be refactored to reuse `exp14_arms` / `exp17_score` — convergence-by-construction would destroy its purpose; (b) **divergence between toolkit and harness is a FINDING, never a bug to silently fix on either side** — three recipe-deltas were caught exactly this way; (c) pre-commit verification: `python3 tools/verify_toolkit.py` self-test PASS, **plus** the three live anchors against committed records — EXP16 X s6/s7 = converted, lengths exactly [4]; A-arm `pos_gradient` delta = 0.1416; A-arm `exam_density` = 27.48. Any miss → halt, surface.

## 3. Folds — marked amendments in THIS commit (ruled; none silent)

1. **F3** (v1.2 §5.1): boundary-surprise sentence conditioned — "IF losses spike at boundaries (the step-0 diagnostic checks this)."
2. **F4** (EXP-L2 status + §3): marked supersession — trigger is now *scatter-CONVERTS (post-orbit-DEAD)* per v1.2 §3; scatter-DEAD skips L2.
3. **F7** (v1.2 status block): sim-supersession rider — all sim-derived figures are estimates; freeze artifacts and real-fabric measurements supersede.
4. **CWP-family** (v1.2 §5.1): the map slot belongs to *surprise-gated plasticity as a family*; CWP is the house implementation, advantages named, standing on fit not provenance. Cross-reference FUTURES §4 (already carries the language).
5. **Replay cross-reference** (v1.2 §5 + FUTURES §4): one-line pointers to `PROJECT_OPS_POSITIONING.md` §3 — the replay diagnostic as a banked mechanism-class arm, same sequencing fence as CWP, and **CWP's honest bar** (must beat/match uniform replay).
6. **HANDOFF tally correction:** replace "seven design-seat catches" with — *"the in-line catches (eight by the session's running count, plus the scripts-are-deliverables process gap at the F4-anchor ruling) plus the terminal red-team's five findings — see RED_TEAM_banked_shelf.md; the rule matters more than the tally."*

## 4. Do-NOT-fold (they wait at their named triggers; the red-team doc is the record)

**F1** (EXP18 assert-(i) re-spec) → EXP18 trigger · **F2** (APU estimator pin) → L2 prereg · **F5** (scatter's own selection statistics) → scatter prereg · **F6** (pretrained-arm decision table) → that arm family's prereg.

## 5. Step-0 fact-check, then commit

Faithfulness workflow over the full shelf: every [MEASURED] number re-derived against committed artifacts (use the toolkit — that is its job); every sim figure carries the rider; no load-bearing literal (contrast-form floors reference *measured* baselines everywhere). Surface residuals; report-don't-patch applies to design-seat prose. Then: **one commit** — *"banked design shelf + verification toolkit — conditional/speculative tier, triggers named (Fable session close, 2026-07-12)"* — `git show --stat` verified against §1's list; nothing from the corridor's working set rides; push on Jason's word; origin sync confirmed.

## 6. Follow-on tasks (NOT in this commit; queue after)

1. **Environment lock** (ops §1.2): lockfile + CUDA/driver/torch versions + threads=1 convention → small separate commit.
2. **Release tag** at the shelf commit (e.g. `v0.17-shelf`); Zenodo DOI on Jason's word (ops §1.3).
3. **Backups** (ops §1.1): CC memory dir → private repo/sync; confirm vault backup; transcript export is Jason-side.
4. **License / public-vs-private** → **Jason's decision, blocking nothing** (ops §1.4).
5. **EXP13 kinematics measurement** (free, read-only, no trigger): run the committed EXP17 measurer's forensic-recipe stats over a rebuilt EXP13 lawful fabric; report net/path, traverse, per-step vs the tremble baseline and the orbit envelope; artifact to `scratchpad/`, surface to the design seat — **no canon write without ratification**.

## 7. Standing pins

Seat/session identifier in every new work product's status line; one seat owns reconciliation before anything rides to CC; the EXP17 corridor proceeds untouched and its terminal is read against v1.2 §2's outcome table.
