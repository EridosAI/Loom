# EXP16 PRE-FLIGHT PACKAGE — Jason's single read before the corridor opens

**Cadence touch 2 of 3** (ratify design → **read pre-flight** → rule on verified result). Assembled per
the EXP16 corridor brief §2. Every §1 immediate action is done; on your ratification of this package the
ratification commit lands + pushes and the corridor OPENS — from that moment the next human touch is the
terminal surface (§7 of the brief), unless a fence trips.

---

## 0. §1 immediate actions — executed

| # | action | outcome |
|---|--------|---------|
| §1.1 | **Push** `3a26fef` + `366ffd3` → origin | done — `53d27f5..366ffd3 main→main`; **origin sync 0/0** |
| §1.2 | Complete class-aware pre-check (G1 semantics) | done — see §1 below |
| §1.3 | **Compute participation bar, X-blind** (G2) | done — see §2 below; **ρ in envelope, no halt** |
| §1.5 | Draft `docs/CORRIDOR_PROTOCOL.md` | done — experiment-agnostic standing form |
| §1.4 | Assemble this package | this document |

---

## 1. (c) PRE-CHECK OUTCOME — G1, clean

**Deployed T=1M decides; 15k advisory.** Scope cal {20,21,22,24,25} + verdict {0–7} + EXT {8,9}, all
up front. Classes (AMD-10): **REUSED = {0–7}** (committed same-(fabric,seed,h_max=1M) assert → a 1M
failure is a deterministic replay divergence → HALT-AND-AUDIT); **FRESH = cal + EXT** (no committed 1M
assert → substitute from {10–19}). Record: `exp08/exp16_precheck_full.json`.

**15/15 ACCEPTED at 1M · 0 swaps · 0 halts · 15k advisory 0 disagreements.** REUSED {0–7} all passed
(no instrument regression on the committed dwell corner). FRESH cal+EXT all passed (substitution pool
{10–19} untouched). Worst k-independence margin comfortable (s6: χ² 70.0 vs threshold 86.9). 34 min.

## 2. (b) THE PARTICIPATION BAR — formula, ρ, constant, X-blind provenance — G2, in envelope

**Formula (corridor brief §5, your ruling):** `bar = ½ × 0.776 × ρ`, where **ρ = X:A word-target
occasion ratio** = `n_exam / N(slot==1)`, counted from the pre-built cal fabric flags — deterministic,
**no X run, no dynamics.** Envelope: **ρ ∈ [0.10, 0.25]**, else HALT. Anchor 0.776 = committed A-arm
`exp12_dwell` {0–7} post-onset activity-fraction median. Record: `exp08/exp16_rho_bar.json`.

| quantity | value |
|---|---|
| **ρ (pooled, primary window [0, 500k])** | **0.167869** |
| ρ per-seed spread (cal {20,21,22,24,25}) | [0.167083, 0.168430] — range 0.0014 |
| ρ pooled at [0, 1M] (structural-invariance check) | 0.167721 (agrees to the 4th decimal) |
| ρ ∈ [0.10, 0.25]? | **YES** (0.168, mid-envelope) → **no G2 halt** |
| word-target dose cut = 1/ρ | **5.96×** (onsets only; mid-dwell word-loss deleted) |
| **BAR = ½ × 0.776 × 0.167869** | **0.065133** |

**Interpretation.** If X participated at exactly the *dose-scaled* reference rate it would show activity
fraction 0.776 × 0.1679 = 0.1303; the bar is **half of that**, 0.0651. So Gate 2 asks: *is X at least
half as active as the designed 5.96×-starved reference would predict?* This is the dose-aware form of the
"X is starved-by-design" concern raised at the prior surface — resolved by formula, not by a chosen knob.

**X-blind provenance (the statement that matters):** ρ is counted from `mask_slot`/`is_exam` flags that
are **bit-identical between A (`exp12_dwell`) and X (`exp12_dwell_expomid`)** — the build smoke asserts
`expo_midword` does not perturb the fabric (`exp14_arms.py` ~L2270). ρ therefore depends only on the
*shared* fabric and on *which flagged waves carry loss in each arm* (a loss-application rule), never on
any X activity value. The counting expression is the committed smoke's own
(`n_exam=((mask_slot==1)&is_exam).sum()`, `n_mid=((mask_slot==1)&~is_exam).sum()`; `exp14_arms.py`
~L2279). **The constant is fixed before any X activity datum exists.**

**AMD-11 (supersession, marked — nothing silent).** The committed prereg §2 (line 39) still carries the
**PROPOSED** bar `≥ 0.259 = ⅓ × 0.776`, explicitly deferred ("RATIFY BEFORE CAL… exact constant
ratified at the pre-check→cal gate"). The corridor brief §5 **is** that ratification and re-specifies the
construction to the dose-scaled `½ × 0.776 × ρ = 0.065133` (≈4× more permissive, crediting the designed
dose cut). On your ratification, **AMD-11** marks this in the prereg header + at §2 line 39
(supersede-don't-overwrite; the "a third as often" grounds text is corrected to the dose-scaled form),
pointing to the corridor brief + `CORRIDOR_PROTOCOL.md`. The *statistic* (post-onset activity fraction),
the *two-level structure* (Gate 1 acquisition / Gate 2 scale), the *ambiguous-middle route*
(DOSE-STARVATION-CONFOUNDED), and the *X-blind-before-cal discipline* are all unchanged.

## 3. (a) THE THREE VERBATIM TEXTS — read where they bite

### 3a. Word-participation gate operationalization (prereg §2)
> **Gate 1 — acquired at all:** the standing acquisition detector (num ≥ 0.01, 2 consecutive — §13.4)
> fires on every READ cal seed. Fails → participation DEAD (12b-inert class: onset never fires; referent
> max num 2.6e-5, §10.20.3).
> **Gate 2 — acquired at the reference scale:** the participation STATISTIC is the **post-onset activity
> fraction** = fraction of post-onset eval windows with num ≥ 0.01 (chosen over median-num because the
> word channel is episodic — median sits in the between-episode troughs and understates a spiky-but-live
> channel; activity fraction separates cleanly: committed A-arm `exp12_dwell` {0–7} ∈ [0.223, 0.878],
> median 0.776, vs 12b-inert exactly 0.000). **Bar [AMD-11]: median across READ cal seeds of the
> post-onset activity fraction ≥ 0.065133 = ½ × 0.776 × ρ (ρ = 0.167869).**
> **The ambiguous middle** — onset fires (Gate 1 pass) but activity fraction < the bar (Gate 2 fail) →
> **DOSE-STARVATION-CONFOUNDED**, routes, no attribution forced. Closes the hazard: a barely-acquired X
> channel cannot launder a dead conversion into clean VISION-SIDE MASSING. Feeds attribution only; never
> a GO criterion, never gates the §5 companion.

### 3b. Probe field / coverage choice (prereg §5 + §6 delta 2)
> Exposure waves never fill `pos_err_word` (`_buffer_wave` early-returns; proof: the expo_word twin
> carries `pos_err_word = {}` on 1,011/1,011 columns) — so **X's gradient is measured via the read-only
> pre-update mid-dwell word-mask probe.** Sources: X's p1 = onset-exam training stash (pre-update);
> X's p2–p48 = the probe (`probe_pos_err_word` buckets; the probe read ≡ the training forward's masked
> pred, pre-update, comparable by construction); A's referent = the AMD-2 verdict-pooled gradient
> (Δ ≈ +0.1416, all-post-acq recipe).
> **Delta 2 (§6):** at every mid-dwell slot-1 non-exam wave on an `expo_midword` arm, a pre-update,
> `no_grad`, forced-word-mask read — **coverage exactly matches the deleted loss occasions = A's
> mid-dwell word-mask coverage**; `build_cells` consumes no RNG (draw-free by construction). Errors land
> in `probe_pos_err_word` position buckets (a NEW field; `pos_err_word` keeps its training-stash meaning,
> structurally empty at p2–p48 on X). Inertness ASSERTED: probe-on/off digit-identity of X's full
> trajectory in smoke.

### 3c. The four §5 mechanism-companion 2×2 rows (reported, not gated)
> **collapse + convert** = full causal chain. · **collapse + dead** = drift removed yet content still
> unlearned → conditional on the §2 word-participation gate exactly as §4: participation-ALIVE →
> vision-side confirmed twice; participation-DEAD (or the starved middle) → DOSE-STARVATION-CONFOUNDED,
> routes, no attribution forced. · **no-collapse + convert** = MECHANISM ANOMALY (conversion without
> drift removal — routes, never forced). · **no-collapse + dead** = the probe contradicts the capture
> model's drift premise — routes.
> **Fence:** the cal gradient is instrument-sanity ONLY — not a GO criterion, not a prior the verdict
> confirms. Reported, not gated.

## 4. (d) GATE TABLE · HALT FENCES · ENVELOPES (EXP16 instance)

**Gates** (each = condition + pass/fail action, all pre-named): **G1** pre-check @1M (done, PASS) ·
**G2** participation bar X-blind (done, ρ in envelope, PASS) · **G3** cal exec {20,21,22,24,25} @1M
mid-ckpt 500k (exit clean · single spec_hash parity · checkpoints per contract) · **G4** cal reads @500k
(band: provisional §10.22 cut, fr ≤ ALPHA · liveness ≥ 3/5 · borrow-branch: cal-clean→own band /
cal-converts→borrow-gate [NOT-SHIFTED borrow A 0.6111×4 loadable · SHIFTED own null, non-loadable,
primary→direction-only] · participation vs 0.065133 recorded · recency gradient recorded) → launches
verdict automatically · **G5** verdict {0–7} @1M mid-ckpt 500k read@500k · **G6** score→DRAFT (§4
partition verbatim: ≥5 AND floor-clean AND READ n≥8 → WORD-SIDE CAPTURE; {1–4}→EXT{8,9} fires, D1
priorities; 0/8 → participation-conditional) · **G7** refute-default panel (MUST-FIX=0) · **G8**
consolidate + push all artifacts incl. raw run JSONs.

**Halt fences (exhaustive):** any REUSED pre-check failure · any run-time fabric-assert · any
smoke/spec_hash/parity/checkpoint/contract failure · liveness < 3/5 · no α-compliant band cut · any
value outside its envelope · any outcome with no named route · panel MUST-FIX or judgment-class ·
rule-vs-rule contradiction · substitution-pool exhaustion · any "I recommend…" · anything uncovered by a
written rule.

**Envelopes & constants (all fixed before their data):** **ρ ∈ [0.10, 0.25]** (measured 0.1679 ✓) ·
**bar = 0.065133** · liveness ≥ 3/5 · standing harness ALPHA (band cut) · budget gate 130k · count cuts
≥5 certify / {1–4} EXT / 0 dead-conditional · READ floor n ≥ 8 · EXT priority substitution-first ·
EXT {8,9} · substitution pool {10–19} · 1M tail descriptive only, primary frozen at 500k.

## 5. (e) PROTOCOL — `docs/CORRIDOR_PROTOCOL.md` (drafted, rides this commit)

Experiment-agnostic standing form: the one principle (pre-named executes / judgment halts), the
three-touch cadence, the gate-table form, the standing halt fences, envelope discipline, in-corridor
conduct (report-don't-patch; mechanical folds only; wrong-reason taxonomy applies to the corridor
itself), the pre-flight + terminal-surface contracts, and the invariant (clean corridor necessary, never
sufficient).

## 6. RATIFICATION COMMIT — exact file set (lands + pushes on your word; corridor opens)

1. `docs/CORRIDOR_PROTOCOL.md` — new (standing form).
2. `docs/EXP16_CORRIDOR_BRIEF.md` — new (the EXP16 instance; currently untracked).
3. `docs/EXP16_PREFLIGHT_PACKAGE.md` — new (this surface).
4. `experiments/05_attention_sculpting/exp08/exp16_rho_bar.json` — new (the bar record; reproducible
   from the committed smoke's counting expression).
5. `experiments/05_attention_sculpting/exp08/exp16_precheck_full.json` — new (the pre-check record).
6. `docs/EXP16_CAPTURE_FEED_PREREG.md` — **AMD-11 marked amendment** (bar constant re-specified to
   `½ × 0.776 × ρ = 0.065133`; supersede-don't-overwrite).

## 7. WHAT OPENS ON RATIFICATION

The corridor runs G3→G8 unattended under the pre-named conditions: cal {20,21,22,24,25} @1M
(mid-ckpt 500k) → G4 reads @500k (band, liveness, participation vs 0.065133, recency gradient) →
auto-launch verdict {0–7} @1M → G6 DRAFT under the §4 partition → G7 refute-default panel → G8
consolidate + push. Any fence trips = stop + surface. Otherwise the next human touch is the **terminal
surface**: DRAFT + full gate log + companions → routes first to the design-chat terminal verification
pass, then to you for the one decision the corridor never contains — **attribution + canon.**

---

## 8. ADDENDUM — AMD-12 (gate-executor audit; folded before the commit, 2026-07-11)

**The corridor was found code-incomplete at open.** Before launching, the corridor's own gate-executor
audit ("§4 is *executable by what?*") exposed that the gates in §4 above named routes with **no
executor**: the G4 cal-read observables (participation activity-fraction, recency-gradient-from-probe)
and the entire **G6 §4-partition DRAFT scorer** were never built — the prereg's §6 build scope
enumerated only the arm flag + the probe (366ffd3 built exactly those). Both EXP14 (`score_2x2`) and
EXP15 (`score_durability`) had carried an explicit build-the-guarded-scorer step; EXP16 skipped it, and
the omission survived five review layers. This was surfaced, ruled (**AMD-12**), and the scoring layer
built + verified **before** the corridor opens — so the corridor that opens is genuinely code-complete.

- **Built:** `experiments/05_attention_sculpting/exp16_score.py` — `cal_read_exp16` (G4) + guarded
  `score_exp16` (G6), reusing `exp14_arms` as the helper library; implements only pre-named routes.
- **Verified:** positive-delta smoke, 9 checks (Jason's {0,3,5}×{alive,dead} grid; the
  cal-converts-SHIFTED → DIRECTION-ONLY demotion; D1 substitution-first + the n≥8 floor → UNDERPOWERED;
  floor-audit AT-FLOOR → NOT-CERTIFIABLE; the Fisher companions to 4dp) — **and the activity-fraction
  reader reproduces the committed A-arm anchor exactly (median 0.776, range [0.223, 0.878])**. The
  existing `exp14_arms` smoke re-confirmed green (helpers untouched). Adversarial code review before commit.
- **Generalized fix (to `CORRIDOR_PROTOCOL.md`):** the pre-flight package now carries a **mandatory
  gate-executor audit** — every gate names its executing function + positive-delta smoke ID; a gate
  without a smoke-tested executor is a pre-flight blocker — plus the **canon-amendment-routing** line
  (amending a committed prereg's build scope routes to ratification even when the code is uncontroversial).

**Updated ratification commit file set** (supersedes §6 above): the six files of §6 **plus**
(7) `experiments/05_attention_sculpting/exp16_score.py` — the scoring layer (AMD-12); and the prereg
in item 6 now carries **both** AMD-11 (bar) **and** AMD-12 (scoring-layer build scope), marked.
