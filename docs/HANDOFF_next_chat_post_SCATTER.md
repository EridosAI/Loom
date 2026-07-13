# HANDOFF — Next Design Chat: post-SCATTER. The novelty axis is closed. One fork is open.

**What this is.** Orientation for the next design seat. Read this, then **confirm state from canon** — clone the repo (PRIVATE: `github.com/EridosAI/Loom`, Jason will issue a fresh read-only PAT) and read FRONTIER §10.27–§10.28 + `MECHANISM_MAP_v1_2_RECONCILED.md` §2–§3 at HEAD. **Do not trust the Claude-project snapshot for anything numeric** — it went eight files stale during this session alone. The repo is the only current source. Standing discipline: `CORRIDOR_PROTOCOL.md`, `docs/Guiding List.md`.

**Working mode.** Design seat (the chat) rules and verifies; **CC implements** on Equinox; **docs are canon**; Jason relays and ratifies. One fork at a time — surface, recommend, **stop**. Corridor cadence: Jason touches each experiment three times (ratify design → read pre-flight → rule on the verified terminal). **The seat has a clone: pull it and verify every claim digit-exact from raw committed artifacts, independently of CC.** That is the seat's whole power, and this session it caught the biggest error twice.

---

## The one-line state

**The novelty axis is closed negative, end to end. Interleaving is the gate. The mechanism is [PROPOSED] and untested — and the arm that tests it is the fork below.**

## What is settled (carry, do not re-derive)

- **EXP14 (§10.24):** FABRIC main effect on onset. Shuffled converts, dwelled suppresses — **identical wave multiset, order-only** (checksum-asserted). C_shuffle certifies 5/8 (62.5%, longest episodes 36–90).
- **EXP16 (§10.26):** recency drift is reward-caused; removing the shortcut does not free content learning. Certified VISION-SIDE. Its **UNDERPOWERED terminal is a count-rung verdict and does not transport** to two-axis regimes.
- **EXP17 / ORBIT (§10.27):** smooth, directed, predictable motion — **DIRECTION-ONLY**, certified 0/8. Closed with **F6-A**: the matched-bar companion re-base.
- **SCATTER (§10.28):** maximal per-frame novelty, zero path, zero predictability — **DEAD**. Certified 0/8; no matched-bar excess at *any* of three detectors (scatter/orbit/A = 2/1/0 at 0.6129×4, 2/1/0 at 0.6111×4, 6/5/3 at 0.6129×3); max episode 4 vs a converter reference of ≥36; raw=2 sits **inside** the floor audit's phantom bracket [0, 3.13]; acq-guard passes (scatter `sep_cat` 0.4733 ≈ A's 0.4732 — **identity was fully recoverable and it still did not bind**).
- **The collapse:** at matched bars the three novelty arms are **indistinguishable from each other**. Not "more novelty is worse," not "less is worse" — **inert**. v1.2 §2's three-way ambiguity (dose / predictability / interleaving) is dead: scatter maxed dose AND killed predictability, and neither moved the needle. **Ordering, not content, moves conversion.**
- **Power of the negative:** certified 0/8 against a paradigm that converts at 58.3%/seed when it converts (14/24, pooled B/C/D) → **p = 0.0009**; conservative certified-vs-certified form (9/24 = 37.5%) → p = 0.023. Both significant.

**The firewall, verbatim from §10.28 — do not let the strength of the negative smuggle the mechanism through.** "Interleaving is the gate" is a claim about *this completer under this fabric*. **Why** it gates — whether interleaving denies the local-satisfiability shortcut (v1.2 §5) or does something else — is **[PROPOSED] and untested**. The replay arm is what tests it.

---

## THE OPEN FORK — rule this first, before any prereg

§4's DEAD branch pre-named **dwell-length titration**, and CC's close states the pivot as titration → replay → CWP. **The seat argued replay-first and Jason has not ruled.** Both cases, honestly:

**Titration (the pre-named order).** Turns the onset-rate knob and measures the *interleaving dose* — how much is needed. Cheap, safe, and it is a **quantity** on a gate we have already established.

**Replay (the seat's recommendation).** Tests the **why** — §10.28's own firewall names replay as the arm that tests the mechanism. It also asks whether interleaving can be *manufactured* from coherent, dwelled experience, which is the question that decides whether this architecture has **any path to reality**. A rescue opens the road; a DEAD closes the paradigm honestly and cheaply. Titration is cheap and does not expire; replay is load-bearing and everything downstream waits on it.

**Seat's recommendation: replay-first.** But this is Jason's ruling, and it should be taken with the terminal in hand.

### The Isaac question — asked, answered, and worth carrying

Jason raised it directly: *are we over-engineering a toy environment to test a model meant for reality? Should we put it in Isaac / a 3D sim and walk it around?* The seat pushed back and Jason accepted the reasoning. **Do not re-litigate from scratch; inherit it:**

1. **Isaac is the hardest regime, not a fresh one.** A walkthrough is *maximally dwelled* — the exact regime now shown DEAD across four arms.
2. **It is a forward-prediction paradise.** Continuous ego-motion means the next frame is the current frame, warped. The failure that killed ten restarts — a forward predictor quietly substituting for the associative mechanism — gets a rocket. In the toy the anti-forward fences are *checkable* (`l_jepa == 0` asserts, zero `loop.gen` draws). In Isaac they are aspirational.
3. **It trades a sharp negative for unfalsifiable mush.** Everything that makes these findings trustworthy — matched-bar detectors, calibration bands, census, digit-exact replication — rests on determinism and cheap replication.
4. **The result already predicts Isaac would fail** — and tells you why brains don't: reality is coherent, and biology doesn't learn from coherent experience directly. **It replays it, interleaved and decontextualized.** The campaign has walked into the reason replay exists.

**The gate for Isaac, pinned:** an architecture that converts under coherent, dwelled, temporally-continuous experience **in the toy**. Before that gate, Isaac cannot distinguish "it works in reality" from "it failed and we can't tell why."

**Cheap middle path if a reality-check is wanted sooner:** enrich the fabric along the axis actually suspected — richer visual basis, occlusion, more co-present objects, ego-motion-like continuity — **while keeping determinism**. Tests "is it the poverty?" at a fraction of Isaac's cost with the whole verification apparatus intact.

---

## Standing rules born this session (all load-bearing, all earned)

- **Matched-bar covers PROSE.** Any cross-arm claim — including descriptive and narrative glosses — must come from a matched-bar tab (`tools/verify_toolkit.py:matched_bar_tab`). The tool existed and the sentence bypassed it. *(Ledger catch 17.)*
- **A gate's falsifier must be reachable from the real data path**, not only from hand-fed smoke. (Born from `floor_clean ≡ True`, a structural tautology whose NOT-CERTIFIABLE branch is dead code.)
- **Provenance strings are COMPUTED from the data they describe, never asserted in a branch.** (`exp14_arms.py:743` asserted "this cell does NOT convert at cal" while the cell's own committed field showed 3/5 converters.)
- **Raw counts never gate a finding.** They scale with the detector's false rate (N=3 → fr 0.000964; N=4 → fr 0.000287) and sit inside the phantom floor. A "raw ≥ 5 power floor" is a floor on *noise*. *(Ledger catch 18 — struck from SCATTER §4.)*
- **F4-A code precedence:** when committed prose and committed code disagree, **the code is the executable definition.** This is what resolved the SCATTER DEAD/UNDERPOWERED judgment call — smoke `sc4`, green *before any run*, asserts DEAD is raw-agnostic.
- **The ledger lives in one pointer** (`progress_log.md §ledger`), never in prose integers.
- **§3 horizon (ratified, applies to every future arm):** default training `read_at = 500_000`; `h_max` stays 1M (fabric, probes, G1a/G1b unchanged); descriptive tail on 4 pre-named blind seeds, with an outcome-blind escalation trigger. Grounds: F13 already freezes the primary at [0,500k), and **all 14 committed converters converted by 427.5k** (median 161.25k). **~37% compute saved per arm.** The tail is descriptive-only and **never enters a cross-arm comparison.**
- **CANDIDATE, needs Jason's ratification: the seat's prose figures carry the same recipe-naming burden as canon figures.** The seat's *computed* numbers have never failed a verification; its *restated* numbers slipped twice this session (an upper-median quoted as a median; a pooled 58% attached to the shuffled arm's specific 62.5%). Both caught by CC's fact-check. Name the recipe next to the number, in relay text too.

## The trap specific to this seat

**Every catch this session was the same species: a number or claim asserted from recollection or an implicit convention, not computed in-session.** The machinery caught all of them — CC's fact-check gate, the refute-default panels, and the seat's own clone-verification. **The next instance inherits the rule in its strongest form: the design seat asserts nothing it has not computed in-session or verified from committed artifacts — and its own rulings' grounds get fact-checked like anyone's numbers.**

Two specific tensions at maximum for the next arm:
- **The anti-forward fence.** Replay is where a forward predictor is most seductive — a replayed sequence is a sequence. The fence must be architectural, not aspirational.
- **The manufacturing fence.** Every target adjustment under feasibility pressure routes to Jason **with the flag stated**. The EXP17 traverse correction is the precedent for doing it honestly.

## Provenance / first move

- **Verified HEAD at handoff: `4588263`** (SCATTER CLOSE, §10.28). Corridor trail: build `24dd0e3` → pre-flight `b443a6e` → G3/G4 `3b9627f` → §3 amendment `ec8121a` → G5/G6 `9b08558` → G8 terminal `ceef0d8` → close `4588263`.
- **Ledger through catch 18** in `progress_log.md §ledger`.
- **Banked with triggers:** dwell-length titration (fires now), replay diagnostic (fires now — see fork), CWP-vs-replay-bar (behind replay), rung-3.5 → L3 generalization arm (free-read (iii)), EXP13 lawful-line bridge (free-read (iv), kinematic-indicated). Loss-engineering FENCED; EXP13 PAUSED.
- **Free-reads standing:** render-gain = **isometry, no gain floor** (pose→render is orthonormal by construction, `conflict_stream.py:59`); CWP step-0 premise-consistent, kill not fired; background carries no member info (rung 3.5 latent).

**First move next session:** clone the repo, read FRONTIER §10.27–§10.28 and v1.2 §2–§3 at HEAD, confirm the ledger, then **open the fork above and stop for Jason's ruling.** Do not draft a prereg before the fork is ruled — titration and replay are different experiments and the wrong one costs a week.

**Housekeeping, still open:** PAT rotation (Jason: fresh read-only, fine-grained, this repo, short expiry); PATHWAY Step 4's ops tail (backups of the three irreplaceables, env-lock commit, release tag, Zenodo).
