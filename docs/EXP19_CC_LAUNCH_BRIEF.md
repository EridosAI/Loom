# CC LAUNCH BRIEF v2 — EXP19 ORDERING WINDOW (W-PERM)

**From:** design seat · **To:** CC (Equinox) · **Authority:** Jason, 2026-07-13 · **HEAD at brief:** `caa212e`

**v1 → v2 (your halt was correct; it is folded).** The arm is re-anchored from **`exp13_fabric`** to
**`exp12_fabric`** — the lineage the certified endpoints actually live in. Three consequences you did not
scope, all in your favour:

1. **The claim-ceiling narrowing is STRUCK** (Jason ratified). exp13 *disables* on `fab.shuffled`; **exp12
   rebuilds the unshuffled twin and checksums the multiset** (`exp12_arms:442–450`). **Nothing is unavailable
   at B > 1.** Your "re-citation, not redesign" read was too generous — a ratified clause was false.
2. **`wp-multiset` is ALREADY BUILT.** That committed checksum-assert *is* the order-only certification, and a
   block permutation passes it by construction. **One build item deleted, not added.**
3. **A fifth `fab.shuffled` site your census missed:** `exp14_arms:1969` — `assert fc.shuffled and fc.T >= 808`,
   a **positive** assert in the coin-rung smoke. New smoke `wp-posassert`.

**Two numbers, one each way.** Yours: exp12's permuted field list is **12**, not 13. Mine: brief v1's G9 said
*"3 B × 8 seeds = 39"* — 3 × 8 = **24**; 39 = 3 × (5 cal + 8 verdict). Both are §12.2 species. Both are ledgered.

**Model line.** Design seat rules and verifies; **CC implements**; docs are canon; Jason relays and ratifies.
**Jason authors all commits** (`jason@eridos.ai`, no co-author). Append-only, auto-push at every closed gate.
**Report-don't-patch. When uncertain, STOP.** Anything whose honest next sentence is *"I recommend…"* is a HALT.

**The spec is `EXP19_ORDERING_WINDOW_PREREG.md`.** This brief is the execution wrapper. **Where they differ, the
prereg governs and the difference is a HALT.**

---

## PART A — CANON WRITES (ratified; mechanical; BEFORE the corridor opens)

| # | file | change | class |
|---|---|---|---|
| A1 | `FRONTIER_attention_sculpting.md` §10.28 | **Annotate-in-place**: pivot (titration → replay → CWP) **SUPERSEDED** → **replay-first**, Jason 2026-07-13. Quote grounds; **do not rewrite** the original. | supersede-in-place |
| A2 | `MECHANISM_MAP_v1_2_RECONCILED.md` §5.3 | **Marked amendment**: fold back the two clauses v1.2's compression dropped from `MECHANISM_MAP_v1_1_addendum.md:40` (C3) — *"(conversion attributable to fabric or to gating — undecidable)"* and *"Regime map first; gating mechanism second, with the regime map as its baseline."* Then record **§5.3 SATISFIED** (Jason, 2026-07-13) **with the isolated-diagnostic rider**: the arm holds the fabric; it does **not** enter the default learner while any regime arm remains unrun. | amendment |
| A3 | `PROJECT_OPS_POSITIONING.md` §3 | **Re-spec, ratified**: "a small uniform replay buffer" → **W-PERM (windowed permutation)**. Record the three tiers: **W-PERM measures B\* → U-BUF must reach B\* causally → CWP must beat or match U-BUF.** U-BUF banked behind, bar = B\*. | amendment |
| A4 | `CORRIDOR_PROTOCOL.md` | **+ three standing rules** (verbatim, below). | append |
| A5 | `progress_log.md` §ledger | **+ rows 19–28** (below). Numbering yours; content fixed. | append |
| A6 | `docs/EXP19_ORDERING_WINDOW_PREREG.md` | **New.** The prereg, verbatim. | new |
| **A7** | `docs/EXP19_CC_LAUNCH_BRIEF.md` | **New — this document.** *(v1 omitted this; briefs are canon, cf. `EXP15_CC_LAUNCH_BRIEF.md`.)* | new |

### A4 — the three rules, verbatim

> **Raw counts never gate a finding.** Raw counts scale with the detector's false rate and sit inside the
> floor-audit phantom bracket; a raw-count power floor is a floor on *noise*. **Certified counts only.**
> *(Ledger 18, a catch-15-species regression. The instance was recorded; the forward-binding rule was not.)*

> **Arms are priced when they open, not when they are banked.** A banked arm's cost, instrument, and dose range
> are **[ESTIMATE]** until its prereg is written against committed code and constants. **Pre-registration fixes
> bars against post-hoc movement; it does not certify an arm nobody has opened.** Every banked arm gets an
> **instrument audit at prereg** — its knob's reachable range, its confounds, **and its endpoints re-derived
> from code, on the lineage the certified records actually live in** — before it is scheduled or costed.

> **Prose figures carry the same recipe-naming burden as canon figures — from any chair.** Every number in
> relay text, chat, a handoff, **or a launch brief** names the recipe that produced it and is **computed
> in-session or read from a committed artifact** — never restated from recollection. Binds the design seat,
> **CC**, and the **design authority**. **The weak point is not the seat. It is prose, and prose is written by
> everyone.**

### A5 — ledger rows 19–28

| # | catch | caught by |
|---|---|---|
| 19 | **Previous seat** — post-SCATTER handoff called the titration/replay fork "unruled" against a pivot order **its own touch-3 words had ratified** (FRONTIER §10.28). Assertion from recollection, not read from canon. | fresh seat, from clone |
| 20 | **Previous seat** — "replay fires now," written having read v1.2 §2–§3 and §5.2 but **never §5.1/§5.3**, where replay is fenced behind the reality ladder under CWP's sequencing rule. | fresh seat |
| 21 | **Canon hygiene — a RULING-CLASS fence made unrulable by lossy compression.** v1.2 §5.3 dropped **both** operative clauses of `MECHANISM_MAP_v1_1_addendum.md:40` (C3): the confound's definition and the baseline requirement. **New species: canon compressed past rulability.** Resolved from the origin text; fence ruled SATISFIED **without a supersession**. | fresh seat |
| 22 | **Seat** — "titration interpolates between two certified endpoints." False: `K_MIN = 2` is a constant, not the knob (dwell=1 unreachable); the multiset is not preserved at any `P_GEOM ≠ 0.1`. | **Jason** |
| 23 | **Design authority** — "~2.7× SCATTER." The v1 ladder computes to **52 runs = 4.0×** (SCATTER = 5 cal + 8 verdict = 13, `exp_scatter_score.py:31–32`). | fresh seat |
| 24 | **Seat, prereg v1** — (a) `wpT` asserted bit-identity to C_shuffle while §5 pinned a *new* substream `SEED_REPLAY`; both could not hold *(Jason)*. (b) Pursuing (a): **`fab.shuffled` gates code paths, not labels** — `wp1` would have failed on an assert unrelated to update parity *(seat)*. Resolved: `SEED_REPLAY ≡ keys["shuffle"]`; `fab.shuffled = (B > 1)`. | Jason + seat |
| 25 | **Seat, prereg v1** — **RECENCY-AT-EXAM omitted.** The arm's one real confound absent from the taxonomy; NON-MONOTONE routed straight to *"the account is wrong"* — but the predicted artifact **is** a non-monotone (32% of exams contaminated at B=32, zero at both endpoints). A pre-named wrong reason would have fired as a finding. | **Jason** |
| 26 | **Seat, prereg v3 — WRONG-FABRIC (new species).** Spec'd its shuffle construction, exam lock, and `fab.shuffled` evidence against **`exp13_fabric`** (the lawful-dynamics derivative; its shuffle arm `exp13_lawscram` is uncertified). **Both certified endpoints live in exp12** (`exp14_arms:55,59` → `exp12_dwell`/`exp12_shuffle`; `:42` → `import exp12_fabric as F`). `wpT` and `wp-strat` were unsatisfiable as written. **Consequence: the claim ceiling's read-regime narrowing was FALSE and is struck** — exp12 rebuilds the unshuffled twin and checksums the multiset rather than disabling reads. §12.1's instrument audit catching the document that proposed §12.1. | **CC fact-check gate, pre-canon** |
| 27 | **Seat, CC brief v1** — G9: *"3 B × 8 seeds = 39."* 3 × 8 = **24**. 39 = 3 × (5 cal + 8 verdict). Number right, formula wrong — **§12.2 species, in the brief carrying the §12.2 rule.** | **CC** |
| 28 | **CC** — exp12's permuted field list is **12**, not 13 *(a, b, member, cat, dwell_id, pos, mask_slot, is_exam, is_probe_exam, nuis, bg, raw)*. And the `fab.shuffled` census missed a fifth site: **`exp14_arms:1969` — a *positive* `assert fc.shuffled`** in the coin-rung smoke. | seat |

---

## PART B — BUILD SCOPE (EXHAUSTIVE. AMD-12: a corridor cannot open with an unexecutable gate.)

**If a gate needs code not listed here, that is a HALT and a scope amendment routed to Jason — never a silent
addition.**

| # | executor | what it is |
|---|---|---|
| B1 | `block_perm(T, B, g)` in **`exp12_fabric`** | The permutation constructor. **Must reduce bit-exactly to `exp12_fabric.py:431` — `randperm(T, generator=g)` — at B=T.** Ragged tail: final short block permuted at its actual size. One generator, seeded once from `keys["shuffle"]`. **Permute exactly the committed 12 fields.** |
| B2 | fabric arm flag | **`fab.shuffled = (B > 1)`. At B = 1 no permutation is constructed at all** — `exp12_dwell`'s exact path. At B > 1 — `exp12_shuffle`'s exact path, which **triggers the twin-rebuild + multiset checksum**. |
| B3 | arm registry entry | `exp19_wperm(B)`. **No loop change. No loss change.** |
| B4 | **`zero_preceding_mask(fab)`** | **THE STRATIFIER. Computed from the REALIZED PERMUTATION. NEVER from `pos`.** An onset exam is in the stratum iff **no wave of its own dwell precedes it in the EMITTED order.** |
| B5 | `recency_companion(fab)` | Per-B distribution of emitted-stream distance from each onset exam to its nearest preceding same-dwell wave. **Index-list only — no training, no model.** |
| B6 | `rho(fab)` | Per-B measured ρ(B). Index-list only. |
| B7 | `exp19_cal(B, detector)` | Per-B band cut, **run twice: full detector and stratified detector.** Cal seeds, before treatment data. **Borrow-gate applies** (C's floor was SHIFTED). |
| B8 | `exp19_score(B)` | Both detectors, certified counts. Plus **EXP16's gradient Δ = p1 − p13-48 vs A's committed referent +0.1416** (`exp16_score.py:63–67`) — **REPORTED, not gated.** |
| B9 | `matched_bar_tab` × 2 | `tools/verify_toolkit.py`. **Two tabs: full-read and stratified.** Every cross-B claim on the stratum comes from the **stratified** tab. **Prose included** (ledger 17). |
| B10 | `exp19_smoke.py` | Part C smokes. |
| B11 | `exp19_diffscope.py` | Hash assert: **`sculpt_loop.py`, `EXP08Loop`, `EXP12Loop.step` bit-unchanged.** |

> **DELETED from v1's scope:** the `wp-multiset` smoke. **It already exists** — the committed twin-rebuild +
> checksum-assert (`exp12_arms:444`, `exp14_arms:213`, `exp14_arms:337`). W-PERM passes it by construction.
> **Do not rebuild it. Verify it fires and passes.**

**Out of scope — any of these is a HALT, not a build decision:** touching `SculptLoop.step` · any loss term ·
any extra gradient step · any wave re-use · any buffer · **any use of `exp13_fabric`.**

---

## PART C — GATE TABLE (every gate names its executor and its positive-delta smoke)

| gate | pre-named condition | executor | smoke | fail |
|---|---|---|---|---|
| **G0 diff-scope** | the three files bit-unchanged (hash) | B11 | `wp-diffscope` | **HALT** |
| **G1a REUSED floor** | **B=1 ⇒ bit-identical to `exp12_dwell`** (weight level) | B1–B3 | **`wp1`** | **HALT** — REUSED-class regression; deterministic replay, **never substitute** |
| **G1b REUSED ceiling** | **B=T ⇒ bit-identical to `exp12_shuffle`** (weight level) | B1–B3 | **`wpT`** | **HALT** — the ceiling is uncertified |
| **G2 parity** | `n_optimizer_steps == T`, identical at every B | B3 | `wp-parity` | **HALT** — compute confound |
| **G3 multiset** | **the COMMITTED checksum-assert fires and passes at every B > 1** | **already built** (`exp12_arms:444`) | *(none — verify, don't rebuild)* | **HALT** — not order-only |
| **G3b positive-assert** | `exp14_arms:1969`'s `assert fc.shuffled` does **not** fire for W-PERM | B3 | **`wp-posassert`** | **HALT** |
| **G4 stratifier label** | the `pos==1` mask and `zero_preceding_mask` **DIVERGE at every B>1** and **COINCIDE at B=1** | B4 | **`wp-strat-label`** | **HALT** — stratifying on the **label**, not the property; **it would certify its own confound** |
| **G5 stratum power** | **`exp12_shuffle`'s COMMITTED records still certify on the zero-preceding stratum** | B4, B7, B8 | **`wp-strat`** | **HALT → Jason.** The stratified detector has no power and the recency defence is decorative. **Not a finding.** |
| **G6 pre-flight measure (BLINDED)** | ρ(B) within 2× of analytic 17.56/B; recency companion within 2× of B/E[k] | B5, B6 | `wp-delta` | **HALT** — the law is not what we read |
| **G7 cal** | per-B bands cut on cal seeds, **both detectors**, before treatment data | B7 | — | **HALT** |
| **G8 PRE-FLIGHT PACKAGE** | assembled, one sitting | — | — | **Jason ratifies → CORRIDOR OPENS** |
| **G9 verdict** | **B ∈ {32, 128, 512} × (5 cal + 8 verdict) = 3 × 13 = 39 runs** *(= 24 verdict + 15 cal)* | B3 | — | **HALT** on any envelope breach |
| **G10 score** | both detectors; both matched-bar tabs; both recency companions | B8, B9 | — | **HALT** on any outcome in **no named route** |
| **G11 refute panel** | adversarial refute-default | — | — | MUST-FIX **or judgment-class** ⇒ **HALT** |
| **G12 TERMINAL (touch 3)** | DRAFT + panel + full gate log + companions + census → **independent terminal verification pass** → Jason | — | — | **attribution + canon: JASON ONLY** |

**Conditional escalation (pre-named, executes automatically):** terminal reads **RESCUE-AT-CEILING-ONLY** ⇒ run
**B = 2048** (+13 runs → 52 total, 4.0× SCATTER). **No other escalation is authorized.**

---

## PART D — THE SMOKES MUST FAIL UNDER THE NAIVE IMPLEMENTATION

**`wp-strat-label` is load-bearing.** It must go **red** if the stratifier is written against `pos == 1`.
Stratifying on `pos` is the *correct* implementation in `exp12_dwell` and the *wrong* one at every paid point —
it passes review, passes spec-check, and certifies the confound it exists to remove. **Write the naive version
first, confirm the smoke goes red, then write the real one.** Same species as `floor_clean ≡ True`; the
reachable-falsifier rule now applies to the arm's own defence.

**`wp-delta`** must fail under a dead no-op: B=1 ≠ B=T, and ρ(B) strictly decreasing in B.

---

## PART E — HALT FENCES (standing set applies in full)

`wp1`/`wpT` bit-identity failure — REUSED-class, **never substitute** · `wp-strat-label` masks coincide at B>1 ·
**`wp-strat` failure — HALT → Jason, not a finding** · `wp-posassert` fires · **CEILING-FAILURE** (B=T does not
convert — it **is** `exp12_shuffle`, certified 5/8) · **FLOOR-FAILURE** (B=1 converts — it **is** `exp12_dwell`,
certified 0/8) · any diff outside Part B · **any use of `exp13_fabric`** · ρ(B) or the recency companion outside
its analytic bracket by >2× · any outcome in **no named route** · a contradiction between two rules ·
**anything not covered by a written rule.**

---

## PART F — WHAT THE TERMINAL MUST CARRY VERBATIM

Not cited — **quoted**: the prereg's **§1 claim ceiling** and its **§2.4 non-causality paragraph** (*W-PERM
measures B\*; it does not show any realizable mechanism can produce it*). **Both** recency companions ride
alongside **every** conversion figure.

---

## HOUSEKEEPING

**PAT: burned** (issued into a chat transcript). Rotate — fresh, read-only, fine-grained, this repo, short
expiry. Still open: PATHWAY Step 4's ops tail (backups of the three irreplaceables, env-lock commit, release
tag, Zenodo).

---

**The one line.** The learner never sees B. Nothing in the model, loss, or optimizer changes. The only things
that move are (i) local satisfiability within a dwell, which falls with B — **the manipulation** — and (ii)
recency-at-exam, which peaks in the interior — **the confound, and it is measured, stratified, and pre-named.**
