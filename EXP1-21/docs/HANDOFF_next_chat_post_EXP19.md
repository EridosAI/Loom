# HANDOFF — Next Design Chat: post-EXP19. The ordering window is bracketed. U-BUF is the open fork.

**What this is.** Orientation for the next design seat. Read this, then **confirm state from canon** — clone
the repo (PRIVATE: `github.com/EridosAI/Loom`; **Jason issues a fresh read-only PAT — the prior one is
burned in a chat transcript; rotation is move zero**) and read **FRONTIER §10.29**, the ratified
**EXP19 prereg (v5, ten amendments)**, the **session-audit pair** (`EXP19_SESSION_AUDIT.md` +
`_VERIFICATION.md` — read together; the audit's own headline error is part of the record), and
`CORRIDOR_PROTOCOL.md` at HEAD. **Do not trust any chat-side restatement for anything numeric.** Verify the
tail past `0d6b102` first — it is owed, and it includes the post-close §2.4 patch + row 54.

**Working mode (unchanged).** Design seat rules and verifies from its own clone; **CC implements** on
Equinox; docs are canon; Jason relays and ratifies. One fork at a time — surface, recommend, **stop**.
Three touches per experiment. The seat asserts nothing it has not computed in-session or read from a
committed artifact — **and its own grounds get fact-checked like anyone's numbers** (ledger rows 46, 51 are
this seat's; expect the same).

---

## The one-line state

**EXP19 closed (§10.29): the ordering window is bracketed — B\* ∈ (128, 512], stratified headline, stream-
stable 200/200. RESCUE-MONOTONE fired → U-BUF is UNLOCKED at bar B\*. The mechanism (why interleaving
gates) remains [PROPOSED]. W-PERM is non-causal; realizability is U-BUF's question — and U-BUF is the fork.**

## What is settled (carry, do not re-derive)

- **The bracket:** c_strat(B) = 0, 0, 0, 4, 5 over B ∈ {1, 32, 128, 512, T}; B\* ∈ (128, 512] on both reads;
  survived 200/200 independent simulator streams. Full read rides as qualified companion — s3 QUALIFIED
  (0.110 stream-stability; the ledger-52 law-bound violation), s0 at 0.860. The emphatic four {4,5,6,7} are
  the stratified-surviving, stream-stable core.
- **Matched-bar:** no evidence-grade cross-arm excess at any matched bar; the "6v5" dissolves at 450 (6v6).
- **RECENCY-CARRIED fired per-seed on {0,3}** — and the descriptive tails then showed both are **late
  conversions truncated by the 500k read** (s0: 97-window episode in the tail, dec_cat 0.789; s3: 128
  windows, 0.556). **B=128's tails stayed at noise through 1M** — the lower edge holds at double the
  horizon. Descriptive only; enters no bracket.
- **D2 canon line (§10.29):** recency is neither necessary (G5a) nor sufficient (EXP16) for conversion.
- **The decay finding:** conversion is transient in this regime — the category representation itself erodes
  after the episode (LOCKSTEP-EROSION 4/5; READOUT-DRIFT disfavored). Acquisition and retention are
  separate problems. Interference-vs-rotation left fused by design; the axis-tracking follow-on is banked.
- **The certification law is amended (ratified, standing):** the tail bound is computed **marginally over
  simulator streams**; a certification violating its own advertised bound rides **QUALIFIED**, never
  headline-unqualified.

## THE OPEN FORK — U-BUF touch 1. Two rulings before any prereg exists.

U-BUF: a **causal, past-only uniform FIFO buffer in the update pipeline**, fabric held at the certified-dead
dwelled regime. The question: **can a realizable mechanism reach B\*?** Bar = B\* ∈ (128, 512], read on the
stratified floor-audit law **with the stream-marginal amendment**.

**Ruling (i) — the ~~C2~~ C3 rider, first.** *[annotated fix at commit (Jason's order, 2026-07-25): the
seat's audit-internal numbering leaked; the canon referent is C3, `MECHANISM_MAP_v1_1_addendum.md:40` —
consistent with the body below, which already reads C3.]* v1.2 §5.3's ratified rider says replay "does not
enter the default learner while any regime arm remains unrun" — read literally it blocks U-BUF (a buffer IS
in the learner) while L3 stays banked. The pre-flagged fork: **refine the rider to its C3 purpose**
(fabric-vs-gating attribution must stay decidable — U-BUF holds the fabric, so attribution IS decidable)
**or declare the regime map closed-enough**. Prior seat's lean: refine-to-purpose. **Do not inherit the lean
silently — rule it with the origin text (C3, `MECHANISM_MAP_v1_1_addendum.md:40`) in hand.**

**Ruling (ii) — the §12.1 instrument audit at open.** Arms are priced when they open. Known before any
drafting:
- **U-BUF touches `SculptLoop.step` — the one path unchanged since EXP08, resolved via MRO to
  `Stage0Loop.step` (`experiments/04_stage0_mvp/loop.py:208`). Ten restarts died to a forward predictor
  entering exactly here.** The anti-forward fence is at its maximum: architectural, symbol-scoped,
  red-teamed, pre-flight blocker.
- **Update-parity is an ASSERT, not a property:** substitution, never addition — one optimizer step per
  wave (`n_optimizer_steps == T`). A buffer that adds replayed-wave updates confounds with compute.
- **Multiplicity is the known confound:** uniform-with-replacement ⇒ Poisson(1) ⇒ **36.8% of waves (and
  their onset exams) never receive an update**. The realized multiplicity distribution rides as a
  **reported companion, never assumed**. The wave multiset is NOT preserved — there is no wpT-style
  certified ceiling; W-PERM's B=T is the *reference*, not U-BUF's limit case.
- **The horizon question is now demonstrated, not hypothesized:** the 500k read truncated two real late
  conversions at the anchor. U-BUF's prereg must rule its read horizon (inherit 500k + LATE-RESCUE-IN-TAIL,
  or re-rule) **before** data exists.
- **Row 53: `save_checkpoint` resume is UNFAITHFUL** (diverges from from-scratch; root cause open). No
  run resumes from checkpoints until it is root-caused. Tails/extensions run from scratch.

**First move next session:** rotate the PAT, clone, verify the tail past `0d6b102`, read §10.29 + v5 + the
audit pair, **then open Ruling (i) and stop for Jason.** Do not draft the U-BUF prereg before the rider is
ruled.

## Standing rules born or ratified this session (all in canon; cite, don't re-derive)

- **Every gate must have failed at least once before it can pass** (observed red under a deliberately broken
  input; a never-failed gate is asserted, not tested). — `CORRIDOR_PROTOCOL`
- **Arms are priced when they open, not when banked** (instrument audit at prereg: knob range, confounds,
  endpoints re-derived from code, **on the lineage the certified records actually live in**).
- **Prose figures carry the recipe-naming burden — from any chair** (seat, CC, and design authority alike).
- **The stream-marginal tail bound / QUALIFIED rule** (ledger 52).
- **Read-gates commit before the data they gate exists** — content that governs how data will be *read* has
  the same commit-before-data requirement as content that governs runs.
- Raw counts never gate; provenance computed never asserted; matched-bar covers prose; calibrate-in-regime —
  all pre-existing, all load-bearing this session (five un-transported constants caught: α, the window, the
  density target, the band default, the titration's exam-lock).

## The traps, for this seat specifically

- **The dominant error species, all chairs, all session: convenient claims about comfortable cases.**
  "Both rules agree at B=T," "at chance for every seed," "elevated vs A/B/D," "universal 8.5," "zero
  additional runs" — every one false, every one caught by the machinery, none self-caught. B=T and
  favorable framings are where scrutiny relaxes. The largest stratum is the worst validator.
- **The relay is half-duplex and crossed five times.** Nothing broke — because every gate lived in a
  committed document. Keep it that way, and use the handshake: **CC echoes any multi-item order back before
  executing.** A superseding message re-carries live content; it never references it.
- **The seat's own audit committed the species it was auditing** (row 46: asserted canon from spoken
  numbering with the clone sitting there). Read canon. Then rule.

## Banked after U-BUF (priced when opened, in this order)

1. **Bracket refinement** — whether an interior point (B=256) is worth a prereg; the B=128-at-noise-to-1M
   tail is the standing input.
2. **Decay follow-on** — the axis-tracking read separating interference from rotation (ISOTROPY-line
   instruments; DECCAT-REGIME-BOUND governs).
3. **Round-robin massing-vs-dispersal arm** (from Jason's question): stratified interleave at B=32 —
   adjacency →0 with dispersal fixed — splits the two candidate mechanisms. Same `fab.perm` family.
4. **Dwell-length titration** (re-priced: exam density ≡ onset rate, per-dose band re-cut, K_MIN=2 floor).
5. D3/D4 (titration reframing; phantom-floor scaling law) — nice-to-haves.

## Housekeeping

- **PAT: burned — rotate before anything else** (fresh, read-only, fine-grained, this repo, short expiry).
- PATHWAY Step 4 ops tail still open (backups of the three irreplaceables, env-lock, release tag, Zenodo).
- Verify the §2.4 post-close patch + row 54 landed (ordered at close; part of the owed tail).
- Ledger through **row 54** at handoff; HEAD at handoff-write was `0d6b102` + the post-close order in flight.
