# PROJECT OPS & POSITIONING — CONTINUITY, PRIOR ART, AND THE REPLAY DIAGNOSTIC

**Status: BANKED OPS/DESIGN MEMO (design seat + Jason, 2026-07-12). Three sections, three audiences: §1 is a checklist (Jason + CC, this week); §2 is scientific positioning (the future paper, and honesty about novelty); §3 is one new banked arm (mechanism-class, fenced). Rides with the shelf.**

---

## §1 Continuity register (cheap now, expensive to retrofit)

1. **The truly irreplaceable assets are NOT the .pt files** — determinism + committed fabric configs make every run recomputable from seeds. The irreplaceables: **CC's local memory directory** (`~/.claude/.../memory/` — loom_*.md, MEMORY.md — exists on Equinox only), **Jason's Obsidian vault**, and **the design-chat transcripts** (rulings' grounds live there; canon carries verdicts, not full reasoning). Action: CC memory into a private repo or synced backup; vault backup confirmed; export the key transcript(s) to the vault.
2. **Environment lock:** commit a lockfile (pip freeze / conda env) + CUDA/driver/torch versions + the `threads=1` convention, so Equinox is rebuildable and "digit-identical" survives a hardware death. One CC task.
3. **Release tag + priority:** tag HEAD (e.g. `v0.17-orbit-prereg`) at the shelf commit; consider a Zenodo snapshot for a timestamped DOI — the order-only result and the capture-not-collapse forensic are priority-worthy findings sitting in a public repo with no timestamp stronger than git.
4. **Public-vs-private is currently an accident.** The repo went public for a verification pass. Decide deliberately: public → add a LICENSE (public-with-no-license is all-rights-reserved plus confusion) and accept scooping exposure with the DOI as the mitigation; private → flip it back and note that the design seat's clone-verification then needs a token workflow.
5. **Verification independence:** `verify_toolkit.py` (committed with the shelf) is the second implementation of every load-bearing read, self-testing against four analytic anchors and live-verified against canon figures. Any seat — or Jason directly — can now run terminal verification mechanically. The Fable-dependency of that function ends with this file.
6. **Free CC task, no trigger needed:** run the committed EXP17 kinematics measurer over EXP13's lawful fabric (read-only). Answers "was the wall kinematic?" this week.

## §2 Positioning & prior art (what is genuinely novel, and what isn't)

**Adjacent literatures, named so nobody reinvents or overclaims:**
- **Experience replay (Lin 1992; DQN, Mnih et al. 2015):** exists because temporally correlated streams break online SGD — the fabric effect is its supervised-completion cousin. Their remedy is architectural; our finding is *environmental and causally isolated*.
- **Blocked vs interleaved practice** (human category learning; interleaving effect): the cognitive-science twin of the fabric effect — convergent, supportive, but never with an order-only control.
- **Catastrophic interference** (McCloskey & Cohen) — M2's ancestry; **collapse in self-supervised siamese/JEPA systems** and the EMA-teacher remedy — the cascading-stability ancestry; **curriculum learning** (Bengio et al.) — the growing-world's ancestry, though stationarity-of-old + expansion-of-new is a different law than easy-to-hard.
- Follow-up owed (next seat, web pass): recent work 2024–26 on temporally correlated data in SSL/online learning — the in-context knowledge here ends at the classics.

**Defensible novelty claims (each with its evidence chain in canon):**
1. **Order-only causal isolation** — identical example multiset, one permutation, conversion flips. Replay/interleaving literatures assume this; the identical-multiset control demonstrates it.
2. **Capture, not collapse** — the "failed" learner is shown to be *succeeding at a cheaper task* (adjacency-caused gradient, flat under permutation), with the drift then causally tied to reward (delete the loss occasions, drift dies at full visibility).
3. **Surgical shortcut deletion as method** — EXP16's loss-occasion deletion holds the stimulus stream bit-identical while removing one reward pathway; the rung taxonomy generalizes it.
4. **The conversion/acquisition dissociation** — massing blocks conditional readout, not representation formation; localizes the pathology in a way the interference literature typically cannot.

## §3 The replay diagnostic (new, banked, fenced)

**The arm:** dwelled fabric + a small uniform replay buffer in the update pipeline — no loss change, no fabric change; the gradient *stream* is artificially interleaved. **Reads:** converts → the ordering-at-SGD account is confirmed at the mechanism level, directly; **buffer-size titration = a direct measurement of the effective window** (M3's constant, from a knob instead of an experiment series); stays dead with the stream demonstrably decorrelated → the block is deeper than update ordering and the map's ladder needs surgery below rung 3.

**Fences and placement:** mechanism-class — behind the reality ladder, same sequencing rule as CWP (added earlier, it confounds every regime finding). **And it sets CWP's honest bar:** the elegant surprise-gated mechanism must beat or match dumb uniform replay to justify itself — biological resonance (hippocampal replay vs novelty-gated plasticity) is available to both, so the contest is decided on regime coverage and cost, not romance. Fold-note: this section cross-references into MECHANISM_MAP v1.2 §5 and FUTURES §4 as a marked amendment at the shelf commit.

---

**Plain language.** Three housekeeping truths and one idea. Housekeeping: the project's real memory lives in three places that aren't backed up (fix this week); the code environment should be frozen in writing so a dead GPU box costs a day, not the project; and the repo being public was a side effect — make it a decision, with a license and a timestamp if yes. The idea: the machine-learning world already met a version of our problem — agents learning from life-as-it-comes kept failing until someone gave them a small notebook of shuffled memories to study from. Giving our learner that notebook is a one-knob experiment that would confirm our whole story and *measure* its key constant — and it becomes the fair rival that Jason's more elegant surprise-gating idea has to beat.
