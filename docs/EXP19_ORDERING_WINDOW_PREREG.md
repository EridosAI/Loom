# EXP19 — ORDERING WINDOW (W-PERM). PREREG v4 — FOR RATIFICATION

**Status:** RATIFIED (Jason, touch 1, 2026-07-13). Commit as `docs/EXP19_ORDERING_WINDOW_PREREG.md`.

**v3 → v4 — the fabric re-anchoring (CC's fact-check gate, pre-canon; ledger 26).**
v3 anchored its shuffle construction, exam lock, and `fab.shuffled` evidence to **`exp13_fabric`** — the
lawful-dynamics derivative (adds `law_mu`, `w3`; its shuffle arm is the uncertified `exp13_lawscram` from the
closed EXP13). **Both certified endpoints live in the exp12 lineage** (`exp14_arms.py:55,59` →
`exp12_dwell` / `exp12_shuffle`; `exp14_arms.py:42` → `import exp12_fabric as F`). A W-PERM built on exp13
could not satisfy `wpT` or `wp-strat` — there are no certified exp13 endpoints to reduce to.

**RATIFIED STRIKE (Jason, 2026-07-13) — it removes a clause he had previously ratified:**

> **The claim ceiling's read-regime narrowing is FALSE on the correct fabric and is STRUCK.** exp13 and exp12
> handle `fab.shuffled` in **opposite** ways. exp13 *disables* (participation candidates → `None`; window tags
> `assert not`). **exp12 REBUILDS THE UNSHUFFLED TWIN AND CHECKSUMS THE MULTISET** (`exp12_arms:444`,
> `exp14_arms:213,337`). **Nothing is unavailable at B > 1.**
>
> **And that gate was already built.** The committed checksum-assert **is `wp-multiset`** — it runs on every
> shuffled arm build, and a block permutation passes it by construction. **One build item deleted, not added.**

Everything else in v3 survives: every §0/§3/§4 number (the dwell law was read from `exp12_fabric.py:66–68`
all along), the bracket logic, the entire recency analysis, and `fab.shuffled = (B > 1)`.

**Ratified upstream (Jason, 2026-07-13):** replay-first · v1.2 §5.3 SATISFIED + isolated-diagnostic rider ·
U-BUF → W-PERM re-spec · §2.4 non-causality, load-bearing · ρ ≤ 0.05 as a **ladder-span requirement** ·
`SEED_REPLAY ≡ keys["shuffle"]` · `fab.shuffled = (B > 1)` · endpoints REUSED-class · the stratum authorized as
a second detector · `wp-strat-label` in build scope, first commit · §12 canon rules.

---

## §0 — Provenance (RE-ANCHORED to the exp12 lineage)

Every number computed in-session by the design seat from committed artifacts/code at HEAD `caa212e`.

| quantity | value | source (**corrected**) |
|---|---|---|
| **certified endpoints' arms** | `A_dwell` → **`exp12_dwell`** · `C_shuffle` → **`exp12_shuffle`** | `exp14_arms.py:55, 59` |
| **fabric module** | `import exp12_fabric as F` | `exp14_arms.py:42` |
| dwell law | `k = K_MIN + Geom0(P_GEOM)`; P_GEOM=0.1, K_MIN=2, K_MAX=48 | `exp12_fabric.py:66–68` *(correct in v3)* |
| E[k] · E[k²] · E[k²]/E[k] · E[1/k] | **10.9293** · **202.87** · **18.56** · **0.1732** | computed |
| *cap statistics (definitional note)* | **mass-at-cap** 0.9⁴⁶ = **0.786%**; **cap-hit (clipped)** 0.9⁴⁷ = **0.707%** — different statistics, both correct. E[k] uses the pmf and is unaffected. | code comment cites the clipped fraction |
| A_dwell certified | **0/8** | FRONTIER §10.28 |
| C_shuffle certified | **5/8**, seeds {0,2,4,5,6}, longest 90 | FRONTIER §10.24 |
| **shuffle construction** | `perm = randperm(T, generator=Generator().manual_seed(keys["shuffle"]))`; **12** permuted fields — `a, b, member, cat, dwell_id, pos, mask_slot, is_exam, is_probe_exam, nuis, bg, raw` — **`pos` travels with the perm** ✓ | **`exp12_fabric.py:430–435`** |
| **exam lock** | `is_exam = True` iff `p == 1` — *"the guaranteed onset exam"* | **`exp12_fabric.py:357–365`** |
| **`fab.shuffled` sites (exp12 lineage — 5, not 5-as-v3-described)** | **1 `assert not`** inside `fabric_asserts()` (`exp12_fabric:478`) — *runs on the unshuffled twin* · **3 `if fab.shuffled:`** that **rebuild the twin + checksum the multiset** (`exp12_arms:444`, `exp14_arms:213`, `exp14_arms:337`) · **1 POSITIVE `assert fc.shuffled`** in the coin-rung smoke (`exp14_arms:1969`) — **must not fire for W-PERM; check at build** | as cited |
| **"the exam wave has no recency channel"** | canon, verbatim | `FRONTIER:1476` |
| same-member-repeat ban, and why | *"else the prior dwell contaminates the onset exam via recency"* | `FRONTIER:1481` |
| **EXP16 recency instrument** | `X16_GRAD_REF_A = dict(p1=0.6915, p13_48=0.5499, delta=+0.1416)` — REPORTED, not gated; verified 4× | `exp16_score.py:63–67` |
| SCATTER cost | 5 cal + 8 verdict = **13 runs** | `exp_scatter_score.py:31–32` |

---

## §1 — The question, and the claim ceiling

**Question.** Is ordering the gate — and **what ordering window does the gradient stream need**?

**The arm.** Hold the fabric at the certified-dead dwelled regime (`exp12_dwell`). Change **nothing** in the
model, loss, or optimizer. Reorder the pre-generated wave list by a **block permutation of window B**. Sweep B.

### CLAIM CEILING — quoted VERBATIM in the terminal surface, never cited

> *"Interleaving the update stream at window B, with the fabric held and the wave multiset preserved,
> rescues / does not rescue conversion; the ordering window is B\*.*
>
> *It is made **on the recency-free stratum** (§4) wherever the recency companion shows contamination.*
>
> *W-PERM is **not causally realizable** (§2.4). It measures B\*; it does not show that any realizable
> mechanism can produce it."*

> **~~STRUCK (Jason ratified, 2026-07-13):~~** ~~"This claim is made under C_shuffle's read regime: at
> every B > 1 window tags and participation candidates are unavailable."~~ **FALSE on `exp12_fabric`.** The
> exp12 lineage does not disable those reads when shuffled — it **rebuilds the unshuffled twin** and
> checksum-asserts the identical multiset (`exp12_arms:442–450`). The narrowing was derived from **exp13**'s
> disabling branches, which are not in this arm's lineage. Nothing is unavailable at B > 1.

**Does NOT license:** "brains replay" · "a path to reality" · any claim about *why* interleaving gates
(v1.2 §5 — stays **[PROPOSED]**) · anything about Isaac.

---

## §2 — The instrument

### 2.1 W-PERM, and its definitions (fixed before data)
Block permutation of the wave index list, window B. **A fabric-index reorder only** — the existing `fab.perm`
machinery in **`exp12_fabric.py:430–435`**.

- Blocks tile from index 0. **Ragged tail:** if `T mod B ≠ 0`, the final short block is permuted at its actual size.
- **One generator, seeded once:** `g = Generator().manual_seed(keys["shuffle"])`; perm = concat of
  `randperm(b, generator=g) + offset` over blocks. **`SEED_REPLAY ≡ keys["shuffle"]`** — no new seed constant.
- **Permute exactly the 12 committed fields** — `a, b, member, cat, dwell_id, pos, mask_slot, is_exam,
  is_probe_exam, nuis, bg, raw`. Not exp13's 14 (no `law_mu`, no `w3`).
- **`fab.shuffled = (B > 1)`** — load-bearing, and **re-grounded on exp12**:
  - **B = 1** → no permutation constructed → **`exp12_dwell`'s exact code path**.
  - **B > 1** → **`exp12_shuffle`'s exact code path** — which **triggers the unshuffled-twin rebuild and the
    multiset checksum-assert**. That is the order-only certification, and **a block permutation passes it by
    construction.**
  - **Check at build:** `exp14_arms:1969`'s *positive* `assert fc.shuffled` is a coin-rung-smoke assert. It
    must not fire for W-PERM. If it does → **HALT**.

**Consequence — the opposite of v3's:** the committed checksum-assert **IS `wp-multiset`.** It is already
built, already runs, and W-PERM passes it. **No new multiset smoke is needed.**

### 2.2 The bracket: both endpoints already certified
| B | reduces to | status |
|---|---|---|
| **B = 1** | no perm ⇒ **`exp12_dwell`**, bit-identical | **certified 0/8** |
| **B = T** | one block ⇒ `randperm(T, generator=g)` ⇒ **`exp12_shuffle`**, bit-identical | **certified 5/8** |

The block constructor **must reduce bit-exactly** to `exp12_fabric.py:431` at B=T (`wpT`).

### 2.3 Why not the uniform buffer (ratified re-spec)
| | W-PERM | U-BUF (as banked) |
|---|---|---|
| wave multiset | **preserved at every B — and the committed assert already certifies it** | broken — Poisson(1) multiplicity |
| waves never updated | 0% | **36.8%** |
| certified ceiling at B=T | **yes — is `exp12_shuffle`** | **no** |
| update-parity | **structural** | must be **asserted** |
| touches `SculptLoop.step` | **no** | **yes** — the path inherited unchanged since EXP08 |
| exam density across B | **identical** | varies with multiplicity |

### 2.4 **W-PERM is NOT causally realizable** *(quote VERBATIM in the terminal)*

> *"Permuting a window of B requires having already seen all B waves before emitting the first — a B-wave
> lookahead. No agent has that. W-PERM **measures the ordering window B\***; it does **not** show that any
> realizable mechanism can produce it. **U-BUF tests realizability, and its bar is B\*.** A W-PERM positive
> reported as 'a path to reality' is a pre-named overclaim, not a finding."*

**Three tiers:** W-PERM measures B\* → U-BUF must reach B\* **causally** → CWP must beat or match U-BUF.

---

## §3 — The dose axis and the ladder-span floor

ρ(B) = P(two consecutive *emitted* waves share a dwell). A uniformly-drawn **wave** is **length-biased** toward
long dwells, so the governing constant is **E[k²]/E[k] = 18.56**, not E[k] = 10.93. ρ(B) ≈ 17.56 / B.

| regime | ρ |
|---|---|
| A_dwell (B=1) | 0.909 |
| B = 32 | **0.549** |
| B = 128 | 0.137 |
| B = 512 | 0.034 |
| C_shuffle (B=T) | ~3.5e-5 |

### THE FLOOR — a **ladder-span requirement**, NOT a DEAD warrant

> **This arm cannot return a general DEAD.** B=T **is** `exp12_shuffle`, certified 5/8 — **ordering already
> converts.** The arm locates *where* it starts working; it cannot conclude that it doesn't.
>
> The floor is a **span requirement**: the paid ladder must reach **ρ ≤ 0.05**, or B\* is unbounded above within
> any realizable range. An arm stopping at B=32 (**ρ = 0.549 — 55% same-dwell**) never delivered its own
> treatment. **The unflattering outcomes are RESCUE-AT-CEILING-ONLY, NO-KNEE-IN-LADDER, and RECENCY-CARRIED.**

**Ladder:** `B ∈ {1, 32, 128, 512, T}`. Endpoints REUSED. Paid: 32, 128, 512 → ρ spans 0.549 → **0.034** ✓.
**B = 2048 is a pre-named conditional escalation** (a *realizability* probe) firing only on RESCUE-AT-CEILING-ONLY.

Every B is its own regime → its own band cut. **But the wave multiset — hence exam density — is identical at
every B.** The exam-density confound that prices the dwell-length titration is **structurally absent here.**

---

## §4 — RECENCY-AT-EXAM (unchanged from v3 — the math is fabric-agnostic; the citations are now exp12)

### 4.1 What W-PERM destroys — already named in canon
`FRONTIER:1476`: *"the exam wave has **no recency channel**."* `FRONTIER:1481`: the same-member-repeat ban
exists *"else the prior dwell contaminates the onset exam via recency."*

`is_exam` is locked to `p == 1` (**`exp12_fabric.py:357–365`**) — so in `exp12_dwell` **all** of a dwell's waves
come *after* its exam. Zero preceding dwell-mates, structurally. **W-PERM scatters a dwell's waves inside the
block, placing same-object waves BEFORE the exam** — worse than the contamination the fabric guards against:
not the *prior* dwell, the exam's **own**.

| B | E[dist to nearest preceding dwell-mate] ≈ B/E[k] | P(dwell-mate **immediately** before) = (E[k]−1)/(B−1) |
|---|---|---|
| **1 (A_dwell)** | — (exam is first in dwell) | **0.000 — structural** |
| 32 | 2.9 | **0.320** |
| 128 | 11.7 | 0.078 |
| 512 | 46.8 | 0.019 |
| **T (C_shuffle)** | ~45,700 | ~2e-5 |

> **Zero at both certified endpoints, PEAKS in the interior. Every FREE point is clean; every PAID point is
> contaminated.** At B=32, **32% of onset exams have a same-dwell wave immediately before them.**

### 4.2 **THE BAR IS ZERO — and the scorer trap**

**EXP16 commits no distance timescale.** It commits a two-bucket contrast whose **recency-free pole is `p1`,
the onset exam**. So `d*` is not measured, not derived, and **not invented**: the bar is **zero preceding
same-dwell waves** — EXP16's own committed operational definition.

> ### PIN — BUILD SCOPE, FIRST COMMIT (ratified)
> **In `exp12_dwell`, `pos == 1` and "zero preceding same-dwell waves" are THE SAME SET. W-PERM DISSOCIATES
> THEM.** `pos` travels with the permutation (it is in the 12-field list), so `is_exam`/`p1` still mark the
> dwell onsets — **but those onsets now have same-dwell predecessors in the emitted order.**
>
> **A scorer stratifying on `pos == 1` — the obvious thing, and what inherited EXP16 code does — would score
> contaminated exams as recency-free, and the gate would certify its own confound.**
>
> **Stratify on the PROPERTY (zero preceding same-dwell waves in EMITTED order), never the LABEL (`pos == 1`).**
> `wp-strat-label` asserts the two masks **diverge at every B > 1** and **coincide at B = 1**.
> **Write the naive version first and confirm the smoke goes red.**

### 4.3 The stratum, and its free positive control
| B | zero-preceding stratum | note |
|---|---|---|
| **1** (A_dwell) | **100%** — structural | the stratified read **is** the full read ⇒ **A's certified 0/8 carries**, free |
| interior | **E[1/k]=17.3% + a straddle BOOST, approached FROM ABOVE, monotone** — measured (500k, index-list exact): B=32 **22.7%** · B=128 **18.4%** · B=512 **17.7%** · B=2048 17.5% | exact count from the index list, pre-flight |
| **T** (C_shuffle) | **30.75%** (14156/46034) over the deployed read [0,500k) — **NOT ~17.3%, NOT matched to the treatment** (17.7%). C_shuffle is `randperm(1M)` read at 500k: the single block spans [0,1M), the read slices ~half, per-dwell competitors halve ⇒ P(emitted-first) ≈ 2/k. | **records committed → wp-strat runs on this 30.75% stratum** |

> *[Amendment 2026-07-14, ledger 33 — the interior row read "minus straddle"; the SIGN was backwards. The onset is `pos==1`, so on a straddling dwell it sits in the **earlier** block and its mates pushed into the next block **cannot precede it** ⇒ fewer local competitors ⇒ P(emitted-first) = 1/k₁ ≥ 1/k. Straddle **RAISES** the interior stratum, monotone from above toward the block-level asymptote E[1/k]=17.3% (B=32→2048: 22.7 → 18.4 → 17.7 → 17.5%). Interior blocks fit within the read window, so no slicing. Caught by CC from the exact index-list computation; the smoke-horizon (T=4000) figures first reported (23.8/20.2/16.7%) were small-sample noise (SE≈2pp).]*
>
> *[Amendment 2026-07-14, ledger 34 — the B=T figure was ALSO wrong: first written 17.29% from a 500k-**build** (`randperm(500k)`, no slicing), not the deployed `randperm(1M)` **read at [0,500k)**. Deployed B=T stratum = **30.75%** — the giant block (the whole 1M fabric) is halved by the 500k read window, competitors halve, stratum ≈ 2×E[1/k]. So B=T's stratum is **LARGER** than the treatment (17.7%), **not matched** — §4.3's "exactly matched" is retired. Consequence for **wp-strat** (Jason's #3): the positive control (C_shuffle) certifies on a 30.75% stratum, larger than the treatment's 17.7% — FAVORABLE (more power for the control); §8 calibrates each stratum in-regime (per-stratum cut, not a shared detector), so the size difference is accommodated, and the treatment retains ample onsets (8097 at B=512). Flagged for Jason's G8 read. Caught by CC from the deployed pre-flight measure. **SUPERSEDED IN PART by ledger 35 (Jason 2026-07-14): the "FAVORABLE / §8-accommodated / ample onsets" reasoning here was WRONG — certification at 14,156 is NOT evidence about 8,097. wp-strat is now MATCHED-N: subsample C_shuffle to N=8,097 (the smallest paid stratum) over draws, report the distribution; if the subsampled control fails, HALT → Jason.**]*

> **`wp-strat` — SPLIT into G5a + G5b (Jason 2026-07-14, ledger 36). Pre-flight, ZERO training runs.** The
> detector is **RE-CUT on the stratum** — calibrate-in-regime transports the PROCEDURE, never the constant:
> cut **(band, N) JOINTLY, fresh, at the house α on the stratum null** (`_provisional_cut`), because a run of
> the committed `consec=5` spans ~28 original onsets — the timescale changed, so N cannot be inherited. The
> committed full-READ 5/8 (conv `0.64×5` over ALL onsets) is **NOT a stratum baseline and does not transport.**
>
> - **G5a — STRATUM VIABILITY (full N).** Does `exp12_shuffle` certify on its own zero-preceding stratum at
>   **full stratum N (~14,156)**, with the re-cut (band, N) detector? **This is the baseline.** If **NO →
>   HALT → Jason**: the stratified detector has no baseline, wp-strat is unaskable, and the arm's entire
>   recency defence is decorative. *(The shattering risk is STRUCTURAL, not statistical: a 36-onset episode
>   yields ~6 in-stratum onsets — the detector may be incapable of forming runs at ANY N. G5a costs one
>   re-score and answers it. **Nothing else runs first.**)*
> - **G5b — MATCHED-N POWER.** Given G5a, subsample each seed's stratum to **N = 7,915** (the worst per-seed
>   paid stratum, seed 4 — the control must be at least as hard as the hardest treatment cell) by **AMONG-KEPT
>   uniform thinning** (a faithful model of the treatment: same [0,500k) window, sparser stratum — the
>   treatment's own detector also sees only stratum onsets and asks for consecutive ones among them). K draws,
>   pinned **`SUBSAMPLE_SEED`**. **PASS iff each of the 5 committed converters certifies in ≥ 90 % of draws**
>   (derived, outcome-independent: the read is k/8; a per-seed false-negative rate q distorts a true k=5 by
>   q·k; require q·k < 0.5 ⇒ q < 0.10 ⇒ retention ≥ 90 %). **MARGINAL — any converter < 90 % while others are
>   above → Jason, not into the package** (heterogeneous retention ⇒ a seed-dependent detector, which cannot
>   report a null). Full distribution reported regardless.
> - **NEGATIVE CONTROL — gates the subsampling METHOD.** Run the identical G5b procedure on the 3 committed
>   **non-converters {1,3,7}**; they must certify in **≤ 1 % of draws** (the detector's own α regime, with
>   slack). If they don't, among-kept thinning is **manufacturing conversions via run-merging** ⇒ the method
>   is **void → HALT.** **Contiguous-block** subsampling rides only as a **reported sensitivity** (window-
>   placement confounds power: a random-start block of 7,915/14,156 spans ~56 % of the run, so a late converter
>   — onsets to 427.5k — fails for the WRONG reason) — never primary.
> - **Why not a 50 % bar:** it certifies a coin-flip detector as healthy (STRATUM-UNDERPOWER wearing a PASS),
>   and the failure it lets through is **spurious RECENCY-CARRIED** — a weak stratified detector manufactures
>   the unflattering cell, which we'd believe *because* it's unflattering. The mirror of the trap that bit
>   twice this cycle.

> **[Amendment 2026-07-14, ledger 37–38 — G5a EXECUTED and PASSED; the detector question resolved by a
> TEST, and the α-cut retired.** Per-onset signal recovered by deterministic replay (`exp19_replay.py`; the
> read-checkpoint at 500k is a REVERTED-to-chance model, so a frozen eval is wrong — decay companion), all 13
> anchors bit-exact incl. cross-commit. **Fork (which null?) resolved as a computable trigger, not a choice
> (ledger 37):** C_shuffle's CAL seeds convert **4/5** on the zero-preceding stratum (= full-read 4/5) ⇒
> Ruling-B regime; provisional's null contaminated. **But the deeper finding retired the whole α-cut (ledger
> 38): ALPHA=1e-3 does NOT transport** — cut against an i.i.d. false-rate model, applied to a granular
> (5–13 onsets/window) autocorrelated stratum, it delivered an ACTUAL 2/3 false rate (~667× miss). **G5a is
> certified by a FLOOR AUDIT, not an α-cut binary** (canon ledger-18: raw counts sit inside the phantom
> floor): the non-converter runs {4,5,6} ARE the measured floor; converters {12,17,20,37,71} clear it
> (nearest 12 = 2× the ceiling 6; each exceeds its in-regime 5000-sim null, p<1/5000). **G5a = PASS**
> (`docs/EXP19_G5A_RESULT.md`, `exp19_floor.py`). **G5b RE-SPECIFIED (supersedes the N=7,915 "≥90% certifies"
> wording above):** the question is not "does a converter certify at 7,915?" but **"what is the PHANTOM FLOOR
> at 7,915, and does the converter signal still clear it?"** The floor RISES as the stratum thins (sparser ⇒
> granular ⇒ longer chance runs); s6 (run 12) is the marginal converter and the floor may reach it.
> Measured by subsampling the ACTUAL non-converters (autocorrelation-carrying) to the treatment's density —
> pre-training. **Standing (ruling 4): nothing transports into the stratum regime unshown-red — band, N, α,
> cadence all suspect.]**

### 4.4 Two independent recency instruments — neither invents a constant
1. **Structural** — the realized recency companion per B, **from the permuted index list alone**: no training,
   no model, blinded, before treatment data.
2. **Measured** — EXP16's gradient **Δ = p1 − p13-48** at every B vs A's committed referent **+0.1416**
   (REPORTED, not gated).

### 4.5 EXP16 as the partial control
EXP16 certified that **removing** the recency shortcut does not free content learning (§10.26). So a rescue at
large B — where recency is *removed* — **cannot be attributed to recency-removal.** *The uncovered direction is
recency being **added** at small B. That is the live risk.*

---

## §5 — Cheapest-shortcut analysis

Nothing in the model, loss, or optimizer changes; **the learner cannot detect B.** No quantity indexed by
*next*; no clock, schedule, coded time, or position carrier; no per-member asymmetry.

Only two things change with B: (i) local satisfiability within a dwell **falls** — the manipulation; (ii)
**recency-at-exam** — the confound, measured and stratified.

**Burden-reversal.** "Replay" rides in on nothing. It enters **only** as a fabric-index reorder on the existing
`exp12_fabric` perm machinery. **Any version touching `SculptLoop.step`, adding a loss term, adding a gradient
step, or re-using a wave is a DIFFERENT arm, out of scope.**

---

## §6 — Anti-forward fence: ARCHITECTURAL, pre-flight blocker

1. **Diff-scope assert (hash, not review).** Permitted: `exp12_fabric`'s permutation constructor · the arm
   registry · the stratified scorer (§4.2). **`sculpt_loop.py`, `EXP08Loop`, `EXP12Loop.step` bit-unchanged**,
   asserted by hash.
2. **`_l_jepa == 0`** guard retained and asserted (inherited).
3. **Zero `loop.gen` draws** (inherited).
4. **Update-parity is structural** — T entries ⇒ T optimizer steps. *Assert anyway:* `n_optimizer_steps == T`,
   identical at every B.
5. **Draw-parity.** The perm consumes only from `keys["shuffle"]`.

---

## §7 — Smokes and outcome cells

### Smokes (pre-flight blockers)
| id | assert | falsifier |
|---|---|---|
| **wp1** | B=1 ⇒ **bit-identical to `exp12_dwell`** (weight level) | divergence ⇒ added/dropped update, shifted draw, **or `fab.shuffled` set wrongly** |
| **wpT** | B=T ⇒ **bit-identical to `exp12_shuffle`** (weight level) | divergence ⇒ constructor ≠ `exp12_fabric:431` at its limit ⇒ **the ceiling is uncertified** |
| **wp-parity** | `n_optimizer_steps == T`, identical across all B | inequality ⇒ compute confound |
| **~~wp-multiset~~** | **ALREADY BUILT** — the committed twin-rebuild + checksum-assert (`exp12_arms:444`, `exp14_arms:213`). W-PERM passes it by construction. | *(no new smoke)* |
| **wp-strat-label** | `pos==1` mask and `zero_preceding_mask` **DIVERGE at every B>1**, **COINCIDE at B=1** | coincidence at B>1 ⇒ **the scorer would certify its own confound** |
| **wp-strat-viability (G5a)** | **[amended 2026-07-14, ledger 37–38 — PASS]** `exp12_shuffle` clears the measured phantom floor on its zero-preceding stratum at FULL N — **FLOOR AUDIT, not an α-cut** (α doesn't transport): non-converter runs {4,5,6} = the floor, converters {12,17,20,37,71} exceed it (nearest 12 = 2× ceiling; each p<1/5000 vs its in-regime sim null) | NO ⇒ recency defence decorative ⇒ HALT. **Observed: PASS** (`exp19_g5a_floor_audit.json`) |
| **wp-strat-power (G5b)** | **[re-specified 2026-07-14, ledger 38]** measure the **phantom floor at 7,915** (subsample the actual non-converters to the treatment's density, K draws, pinned SUBSAMPLE_SEED — the floor RISES as the stratum thins) and ask whether the converter signal still clears it (s6=12 the marginal) | floor reaches/exceeds the converter signal ⇒ STRATUM-UNDERPOWER at ρ≤0.05 anchor B=512 ⇒ HALT → Jason; among-kept must not merge runs (method check) |
| **wp-recency** | structural recency companion computed per B **before any run** | absent ⇒ §4 unenforceable |
| **wp-posassert** | `exp14_arms:1969`'s positive `assert fc.shuffled` does **not** fire for W-PERM | fires ⇒ HALT |
| **wp-delta** | **fails under a no-op**: B=1 ≠ B=T; ρ(B) strictly decreasing in B | guards against an invariance-only smoke |

### Outcome cells
| cell | condition | route |
|---|---|---|
| **RESCUE-MONOTONE** | conversion rises with B; knee at B\*, **surviving the stratified read** | Ordering is the gate; **U-BUF unlocks, bar = B\*.** *(flattering)* |
| **RESCUE-AT-CEILING-ONLY** | converts only at B ≈ T | **Fire the B=2048 escalation** (+13). If 2048 also fails: **B\* > 2048 ⇒ no causal mechanism can hold the window.** *(unflattering)* |
| **NO-KNEE-IN-LADDER** | B=T converts; no paid point does | **UNDERPOWERED-BY-LADDER, not DEAD.** Escalate. |
| **NON-MONOTONE** | converts at some middle B, not higher | **ROUTES FIRST TO §4.** The predicted artifact **is** an interior peak. Only if the **stratified** read reproduces it does it refute the account. **A raw non-monotone read as refutation is a pre-named wrong reason, not a finding.** |
| **RECENCY-CARRIED** | conversion in the raw read, **absent** in the stratified read | The rescue is the recency channel. **Report; do not patch.** *(unflattering)* |
| **CEILING-FAILURE** | B=T does not convert | **INSTRUMENT FAILURE — B=T *is* `exp12_shuffle` (5/8). HALT.** |
| **FLOOR-FAILURE** | B=1 converts | **INSTRUMENT FAILURE — B=1 *is* `exp12_dwell` (0/8). HALT.** |

---

## §8 — Cost

**Recipe named.** SCATTER = `CAL_SEEDS` (5) + `VERDICT_SEEDS` (8) = **13 runs** (`exp_scatter_score.py:31–32`).

| ladder point | class | runs |
|---|---|---|
| **B = 1** | **REUSED** (≡ `exp12_dwell`) — pre-check `wp1` | **0** |
| B = 32 / 128 / 512 | paid | **5 cal + 8 verdict = 13 each** |
| **B = T** | **REUSED** (≡ `exp12_shuffle`) — pre-check `wpT` | **0** |
| **COMMITTED TOTAL** | **3 paid B × 13 = 39 runs** (= **24 verdict + 15 cal**) = **3.0× SCATTER** | **39** |
| *B = 2048* | *conditional, RESCUE-AT-CEILING-ONLY only* | *+13 → 52 = 4.0×* |

*(v3's brief mislabelled this as "3 B × 8 seeds = 39". 3 × 8 = 24 verdict. The total was right; the formula was
not — §12.2 species, ledger 27.)*

The stratified read and `wp-strat` cost **zero additional runs** — they re-score committed records and the same
treatment runs. They cost **scorer code and a stratified band cut**.

**Constants: grounds now, values at pre-flight.**

| constant | grounds | fixed when |
|---|---|---|
| B-ladder | span ρ(B) 0.549 → ≤0.05; both certified endpoints pinned | pre-flight, against **measured** ρ(B) |
| ρ(B) · recency companion | measured on the committed fabric + permutation | pre-flight, **blinded** |
| **recency stratum bar** | **ZERO preceding same-dwell waves — EXP16's committed `p1` referent.** Not invented. | **fixed here** |
| per-B band, full read | calibrate-in-regime; **borrow-gate applies** (C's floor was SHIFTED) | cal seeds, pre-treatment |
| per-B band, **stratified** | stratum is 100% at B=1, ~17% at B>1 ⇒ **its own exam density, its own cut, its own matched-bar tab**, never the full-read bar | cal seeds, pre-treatment |
| read_at / h_max | §3 horizon, ratified `ec8121a` | fixed |

---

## §9 — Halt fences (standing set applies in full)

`wp1`/`wpT` failure (REUSED-class — deterministic replay, **never substitute**) · `wp-strat-label` masks
coincide at B>1 · **`wp-strat` failure → Jason, not a finding** · `wp-posassert` fires · **CEILING-FAILURE** ·
**FLOOR-FAILURE** · any diff outside build scope · ρ(B) or the recency companion outside its analytic bracket
by >2× · any outcome in **no named route** · a contradiction between two rules · **anything not covered by a
written rule** · anything whose honest next sentence is *"I recommend…"*.

---

## §10 — Wrong-reason taxonomy (named BEFORE the run)

**RECENCY-AT-EXAM** (the one real confound; its shape *is* a spurious NON-MONOTONE) · **RECENCY-BY-LABEL**
(stratifying on `pos == 1`; the gate certifies its own confound) · **STRATUM-UNDERPOWER** · **FALSE-SPAN**
(ρ ≥ 0.10 yields no usable B\*; *not* a DEAD warrant) · **COMPUTE-CONFOUND** (absent by construction) ·
**EXAM-DENSITY** (absent by construction — *the confound that prices the titration*) · **MULTIPLICITY**
(absent by construction; returns under U-BUF) · **CEILING-BORROW** (C's band was cut against a SHIFTED floor;
every cross-B claim from a matched-bar tab, **prose included** — ledger 17) · **RAW-GATING** (ledger 18) ·
**WRONG-FABRIC** *(new — ledger 26: an arm spec'd against a parallel-looking but uncertified fabric lineage.
The instrument audit of §12.1 is the standing guard.)*

---

## §11 — Banked behind this arm

**U-BUF** (causal FIFO; bar = B\*; update-parity becomes an assert; realized multiplicity a reported companion)
· **CWP** (must beat or match U-BUF) · **Dwell-length titration** (RE-PRICED: `K_MIN=2` floor · multiset not
preserved · **exam density ≡ onset rate** ⇒ per-dose band re-cut + an exam-density-matched control. A
calibration series, not a knob-turn).

---

## §12 — Canon rules (route to `CORRIDOR_PROTOCOL`)

### 12.1 Arms are priced when they open, not when they are banked
> A banked arm's cost, instrument, and dose range are **[ESTIMATE]** until its prereg is written against
> committed code and constants. **Pre-registration fixes bars against post-hoc movement; it does not certify an
> arm nobody has opened.** Every banked arm gets an **instrument audit at prereg** — knob's reachable range,
> confounds, **and endpoints re-derived from code, on the lineage the certified records actually live in** —
> before it is scheduled or costed.
>
> *Instances: the dwell-length titration (exam density ≡ onset rate; K_MIN=2 floor). The replay diagnostic,
> banked as a "small" buffer (55% same-dwell at B=32). **This arm's own v1** (a bit-identity its seed spec
> forbade). **This arm's own v3** (spec'd against `exp13_fabric`, where its certified endpoints do not exist).*

### 12.2 Prose figures carry the same recipe-naming burden as canon figures — **from any chair**
> Every number in relay text, chat, a handoff, **or a launch brief** names the recipe that produced it and is
> **computed in-session or read from a committed artifact** — never restated from recollection. Binds the design
> seat, CC, **and the design authority**.
>
> *Instances, one per chair: an upper-median quoted as a median (seat) · a pooled 58% attached to a specific
> 62.5% (seat) · "~2.7× SCATTER" for a ladder computing to 4.0× (design authority) · "3 B × 8 seeds = 39"
> where 3×8=24 (seat, **in the brief carrying this very rule**) · "13 permuted fields" where there are 12 (CC).*
>
> **The weak point is not the seat. It is prose, and prose is written by everyone.**

---

## §13 — Terminal surface requirements

Carry **verbatim, not by citation**: §1's **claim ceiling** · §2.4's **non-causality paragraph** · **both** §4
recency companions alongside **every** conversion figure · the **recency-free stratified read** wherever the
companion shows contamination.

Plus the standing package: DRAFT · verification/refute panel record · full gate log · companions ·
sensitivities · riding flags · bare-N census · **independent terminal verification pass before the result
reaches Jason** for attribution + canon.
