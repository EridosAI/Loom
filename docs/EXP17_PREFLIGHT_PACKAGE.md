# EXP17 — PRE-FLIGHT PACKAGE (touch 2)

**Assembled 2026-07-12. G2 (select + deployed verify), G1a (reused-A audit), G1b (fresh pre-checks)
ALL CLOSED — outcomes in (c). This is the HARD STOP: the corridor does NOT open until Jason reads
this package and gives the word. On ratification: the pre-flight commit (this package + the two G1
records, currently untracked by design) pushes, and the corridor opens G3→G8 unattended
(CORRIDOR_PROTOCOL.md:96-98). Build + amendment already committed+pushed: `93b22b4` (F4-A docs),
`0fb3e4c` (build + select/freeze/anchor artifacts).**

**Advisory annex rides this commit: `docs/EXP17_PREFLIGHT_ANNEX.md`** (Jason-requested touch-2
kinematics sweep, fabric-only, corridor-shut). Neither halt-class condition trips — deployed walls
are *wider* than the 100k read (ω-window [15.81,19.40] vs [16.0,18.9]; slopes scale-stable), and
W1(r) is smooth/monotone with the pin at its low-confound end (no knee); the onset shift is 2.36×
the within-tremble baseline. The freeze (0.85,18°) is corroborated at the deployed window; no
re-selection is motivated. Generator `exp17_annex_sweep.py` + data `exp08/exp17_preflight_annex.json`
ride too.

---

## (a) Operational texts — verbatim, where they bite

**§4 outcome cells (counts route, signatures certify):**
- "**SWEEP CONVERTS** — ≥5 of READ (n≥8) AND floor-clean AND signature-decisive: PER-FRAME NOVELTY
  SUFFICES — interleaving is not required; *temporally coherent experience can convert*." RB-2
  rider b (pre-named): this cell "TRIGGERS the interior-concentration control — a tremble arm at
  the sweep arm's realized center distribution — BEFORE any paradigm-positive certifies"; scope:
  "a post-corridor FOLLOW-UP experiment (own prereg/ratification); it gates canon entry of the
  paradigm-level positive claim at touch 3 only."
- "**SWEEP DEAD** — 0 real after signature census: INTERLEAVING IS THE GATE — novelty-within-
  identity insufficient." F5 trigger pin: "Formal SWEEP-DEAD = raw k = 0 (certified-0 then holds
  and is asserted)."
- "Count {1–4}/8 → EXT {8,9} fires before any row (D1 priorities: UNREAD substitution first;
  certifiable cells need READ n≥8); post-extension ≥5 certifies, else UNDERPOWERED, routes."
- "Raw ≥5 with certified <5 → **SIGNATURE-DIVERGENT, routes**." Raw>0/certified-0 → "formal-
  UNDERPOWERED + certified-SWEEP-DEAD — the interleaving-is-the-gate claim then belongs to
  attribution, not the formal cell."
- "**Cal-converts** → Ruling-B machinery (own between-episode null, referent recorded); counts
  non-loadable vs A; direction-only + §5 companions; attribution routes."
- "**Liveness < 3/5** → HALT (experiment unposed). **Floor-flagged** → bracket + census ride to
  terminal, NOT-CERTIFIABLE-by-count." Precedence: "loadable → floor_clean → n≥8 → count", with
  the formal/certified divergence guard ("routes forced on disagreement") kept.

**F7 census:** "Certification = longest post-acquisition episode ≥ SIG_DEPTH = 8, decisive on its
own. Episode count (referent SIG_RECUR = 2) is REPORTED as corroboration — never disqualifying,
never certifying alone." G4 geometry check (§10.25.3): "the own band's N must be < SIG_DEPTH
(bare-N regime — the census discriminates); N ≥ 8 → judgment-class HALT."

**F12 census self-audit:** "Certification requires the observed certified count to **exceed the
bracket's high end**; else **NOT-CERTIFIABLE-by-census, routes**… it covers the own-band N∈{6,7}
zone the geometry HALT (N≥8) waves through, in any regime." Occupies the floor_clean precedence
rung; folded INTO the definition of "certified" (F5's "certified ≥5" presupposes it cleared).

**F13 single referent:** "The cal-marginal band cut, the borrow diagnostic, AND all null pools
(floor audit + census self-audit bracket) are computed on the [0,500k] column prefix
(t ≤ 499,800) — one referent everywhere… The (500k,1M] cal tail is descriptive only."

**F9 READ/UNREAD cutoff:** "the F6 budget gate (500k − acquisition_onset ≥ 130k), EXP16's
`_score_one` verbatim."

**F10 gradient alarm:** "flag iff pooled Δ < 0.0708 (half of A's +0.1416). Reported/flagged only,
never gated."

**F11 correspondence window:** frozen kinematics' per-step displacement "must sit strictly inside
(floor, bound)" = (tremble within-step norm, confusion bound); "position within the window is
reported at pre-flight" — reported in (b).

**F4-A anchor bind (2026-07-12):** "Anchors re-base on `exp17_score.py` outputs as the executable
recipe definition, frozen digit-exact into the anchor artifact. No tolerance anywhere; future
measurer drift breaks the bind." Rider: "an anchor is only as exact as its provenance —
digit-exact binds require committed-code provenance."

**F14 cross-regime advisory:** the 6,532 null-pool floor is an "ADVISORY tripwire only (routes to
a human, never gates/certifies; the regime-native α-uncuttable fallback is the sole decisive
HALT-equivalent."

**F8 borrow diagnostic:** label-corrected wrapper output only; "can never source the band."

---

## (b) Constants — formula, measured inputs, value, provenance

Blinded-constant statement: every constant below was fixed from A-fabric measurements, fabric-only
X-blind orbit probes, or ratified text **before any orbit-arm RUN (treatment data) existed**; no
orbit run has ever been stepped. Scoring constants never enter `C.spec_hash()` (run-record parity
`41d6f0d5e7da`, all 41 committed records + G1 checks).

| constant | formula / recipe | value | provenance |
|---|---|---|---|
| (r, ω) | lexicographic: feasible(all floors, pooled AND per-seed-worst) → max clip → min r·ω | **(0.85, 18°)** | `exp17_orbit_select.json` (36-cell grid, 8 seeds @100k; sole feasible r=0.85 cell; 24/36 feasible) |
| clip half-width | 1.5 − r − 3·0.125 | ±0.275 | derived; max over feasible set |
| anchor stat1/2/3 | committed measurer, A fabric {0–7}, T=1,000,008, [0,500k) | 0.15955481071937405 / 0.07887529612359336 / 0.05558072403073311 | F4-A re-base; `exp17_anchor_rebase.json` (forensic cross-check + residual table inside); `--anchor` GREEN digit-exact ×3 |
| baselines @100k (selection) | pooled mean of per-seed means, k==11 contained; confusion = mean of per-seed cross-boundary medians | np11 0.14399, tr11 0.09060, path11 1.6449, confusion 1.3104 | measured at `--select` (F4-A clause 3: re-measured before selection; no chat literal consumed) |
| baselines @1M/[0,500k) (deployed floors) | same recipe at deployed scale | np11 0.14489, tr11 0.09019, path11 1.6380, confusion 1.3112 | `exp17_orbit_freeze.json` |
| floor bars (deployed) | 4× / 2.5× / ceiling / arc / per-step | ≥0.57956, ≥0.22548 & ≤0.50, arc 2.67 ≥ 1.6380, per-step ≤ 1.3112 | ratios ratified (R3/RB-1); references measured |
| F11 window position | deployed per-step median vs (noise floor, confusion) | 0.2261 ∈ (0.1596, 1.3112) = 1.42× floor, 0.17× bound | freeze artifact; INSIDE, floor end |
| census | SIG_DEPTH = XA.EPISODE_MIN; SIG_RECUR corroborative | 8; 2 | F7 (DEPTH-decisive) |
| floor-audit clean rule | AMD-13 self-excluded dual-null bracket | p = 0.10 | inherited, re-affirmed vs own band at G4 |
| null-pool advisory | committed precedent minimum | 6,532 | F14 — advisory only |
| cal fences | fr ≤ α; live ≥ 3/5; band N < 8 | α = 1e-3 (XA.ALPHA) | §4 / F7 geometry |
| READ floor | certifiable cells need READ n | ≥ 8 | F5 (NOT XA.N_MIN_READ=3) |
| budget gate | 500k − onset ≥ 130k | F9 | EXP16 `_score_one` verbatim |
| gradient alarm | pooled Δ < half A's referent | 0.0708 (ref +0.1416) | F10; report-only |
| seeds / horizons | cal {20,21,22,24,25}; verdict {0–7}; EXT {8,9} unconditional; subst {10–19}; primary 500k; h_max 1M; mid-ckpt 500k | — | §3 / F3 |
| SEED_SWEEP | dedicated substream base | 100000 | collision-audited (§8 minors) |
| onset-marginal W1 (RB-2 rider a, REQUIRED touch-2 read) | mean per-axis W1, p=1 poses, {0–7} pooled, [0,500k) | **0.0228** (per-axis 0.0235/0.0230/0.0226/0.0220) | freeze artifact; reported trade, never a fence |

Deployed kinematics at the frozen pair (15 seeds, [0,500k)): np11 0.5853–0.5889 (bar 0.57956),
tr11 0.2373–0.2391, per-step seed-max 0.2267, anchor reflections 0, pose_clips 0 across 15×1M,
driven/undriven extents ≈ 0.31 / 0.075 (the 2-plane structure visible — RB-1's undiluted
driven-plane contrast for any SWEEP-DEAD read).

---

## (c) Pre-check outcomes (F3 order: G2 → G1a → G1b; all closed before this stop)

- **G2 — CLOSED, PASS.** Deterministic replay of the lexicographic selection == frozen (0.85, 18°);
  all three floors + zero-anchor-reflection verified on ALL 15 deployed 1M fabrics at [0,500k);
  freeze artifact `exp08/exp17_orbit_freeze.json` (committed `0fb3e4c`). Feasibility at deployed
  scale re-derived against the 1M-measured baselines, not the 100k selection values.
- **G1a — CLOSED, 8/8 PASS, no halts.** REUSED A comparator {0–7} @ T=1M, halt-and-audit class
  (§10.25.2: failure = replay divergence, never substituted). Record:
  `exp08/exp14_exp12_dwell_exp17_g1a.json` (rides the pre-flight commit).
- **G1b — CLOSED, 15/15 PASS, ZERO substitutions.** FRESH orbit cal/verdict/EXT @ T=1M, swap pool
  {10–19} lowest-unused (unused). No substitution ⇒ no mechanical G2 re-verification owed. perlag
  margins wider than A's (obs ~0.055–0.075 vs n99 ~0.085–0.099; expected false-alarm ~1%/fabric —
  none fired). Record: `exp08/exp14_exp12_dwell_orbit_exp17_g1b.json` (rides the pre-flight commit).

---

## (d) Gate table (executor + positive-delta smoke ID), halt list, envelopes

| gate | executes | executor (committed) | positive-delta smoke |
|---|---|---|---|
| G3 | cal runs ×5 @1M, mid-ckpt 500k, `out_tag="exp17cal"` | `XA.run_exp14_arm("exp12_dwell_orbit", s, read_at=1_000_000, h_max=1_000_000, mid_ckpt_at=500_000)` | smoke17 (19)/(20) delta-live + (23) drift fence; PROBE-arm refusal guard (22) |
| G4 | cal read: own band, fences, gradient, census geometry | `cal_read_exp17` | sm-G4-halts (liveness + Ruling-B recut fire through the real path), sm-G4-grad (fallback tail) |
| G5 | verdict runs ×8 (+EXT {8,9} unconditional), same invocation `out_tag="exp17verdict"` | `XA.run_exp14_arm` | as G3 |
| G6 | guarded score: F5 partition, F7/F12 census+self-audit, F13 pools, D1 EXT, Fisher, companions | `score_exp17` (refuses until cal_read ∧ ¬HALT ∧ {0–7}+{8,9} records) | sm-G6-grid, sm-G6-census, sm-G6-selfaudit + sm-G6-selfaudit-refuse, sm-G6-score-one, sm-G6-ext, sm-G6-trunc (F13 falsifier), sm-G6-fisher |
| G7 | refute-default panel on the DRAFT — no lens assumes conversion; no lens assumes the sweep story | workflow panel (human-auditable record) | n/a (adversarial layer) |
| G8 | consolidate + push all artifacts (raw JSONs incl.) → `docs/EXP17_TERMINAL_SURFACE.md` | git, enumerated scope | `git show --stat` vs list |

**Halt / route list (in-corridor):** cal liveness <3/5 (HALT); α-uncuttable band (HALT); band
geometry N≥8 (judgment HALT); census self-audit refuse (NOT-CERTIFIABLE-by-census, routes);
formal/certified divergence (routes); SIGNATURE-DIVERGENT (routes); SWEEP-DEAD certified-0 assert
failure (HALT); EXT target-verify failure (HALT); any replay/reproduction divergence
(halt-and-audit); §5.5 realized-kinematics assert on rebuilt run fabrics vs frozen targets
(instrument-integrity, HALTS on mismatch); F4-A anchor bind drift at any measurer re-run (loud
fail); instrument/NM STOP → **disclose the tripped instrument ONLY** (standing rule; sealed
verdicts stay sealed).

**Envelopes / annotations:** gradient-persistence flag (F10, report-only); `walk_realized`
manifest field reads inflated under the orbit (logged-not-asserted — annotation, not a defect);
checkpoints `.pt` at 500k + 1M + any pre-registered event (standing contract, gitignored);
`torch.set_num_threads(1)` on every path; auto-push at every closed gate.

---

## (e) Protocol instance

CORRIDOR_PROTOCOL.md governs (committed). Instance brief: after ratification of this package the
corridor runs **G3 → G4 → G5 → G6 → DRAFT (no attribution) → G7 → G8** unattended; every fence
above halts to Jason; the terminal surface routes FIRST to independent design-chat verification
from pushed artifacts, THEN to Jason for attribution + canon §10.27 (touch 3) — the close commit is
separate and on his word only. Descriptive context rows ride the DRAFT: Fisher vs A's committed
0/8; "C_shuffle 5/8 {0,2,4,5,6} @ 0.64×5 (own shifted null; descriptive context)". The 1M tail is
read from untruncated records, descriptive only. Cost note: 15 runs @1M CPU (~40 min each,
parallelizable); no GPU.

**HARD STOP. Awaiting Jason's read + word to open the corridor.**
