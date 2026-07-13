# SCATTER-DWELL — PRE-FLIGHT PACKAGE (touch 2)

**Status: PRE-FLIGHT (CC, 2026-07-13). Assembled once, read once, before the terminal opens
(`CORRIDOR_PROTOCOL.md`). On ratification of this package (Jason's word), committing + pushing it OPENS
the corridor; from that moment the next human touch is the terminal surface (touch 3). Author: Jason
Dury, no co-author.** Prereg = `docs/EXP_SCATTER_DWELL_PREREG.md` (touch-1 ratified: R grid, 2.0×/2.0×,
confusion-ceiling). Build = commit `24dd0e3`. This package folds the method-named-figures prose fix
(§2.3 feasibility literals → recipe-named measured values).

## (a) Ratified texts (verbatim pointers)

- **§4 outcome cells** — matched-bar excess + certified census DECIDE; counts SECONDARY; cal-self-converts
  EXPECTED → DIRECTION-ONLY expected formal label. Cells: **SCATTER CONVERTS** (excess survives at a
  common detector ∧ certified ≥5 ∧ **READ n≥8**), **SCATTER DEAD** (no surviving excess ∧ census 0),
  **SIGNATURE-DIVERGENT** (raw≥5 ∧ certified∈{1..4} or axis disagreement → routes), **DIRECTION-ONLY**
  (cal-converts formal label), raw{1..4}→EXT-first.
- **The two F6-A standing rules** (verbatim): (i) matched-bar companions — one detector through both
  arms, unlike-bar is context-only; (ii) provenance strings COMPUTED, never asserted-in-branch.
- **Interior-concentration control** (pre-named, EXP16 precedent): SCATTER-CONVERTS triggers a tremble
  arm at scatter's realized center distribution before any paradigm-positive certifies at touch 3.
- **R recipe / ball law**: per-frame `pose = center + R·U^(1/K)·(randn(K)/‖randn(K)‖)` from `g_sweep`;
  center = clip(onset g_nuis draw); draw-parity to A_dwell.

## (b) Constants (formula + value; measured values govern)

| constant | value | source / formula |
|---|---|---|
| ARM / tremble | `exp12_dwell_scatter` / `exp12_dwell` | prereg §1 |
| seeds | cal {20,21,22,24,25} · verdict {0–7} · EXT {8,9} · subst {10–19} | §3 |
| horizon | build 1M, mid-ckpt 500k, **primary [0,500k)** (F13) | §3 |
| **R\*** | **0.50** | `select_scatter` → `exp08/scatter_select.json` (sole feasible; drift-asserted) |
| R grid | {0.20, 0.30, 0.40, 0.50} | ratified touch 1 |
| clip half-width | `cl = 1.5 − 0.50 − 3·0.125 = 0.625 > 0` | box upper wall (generator assert) |
| contrast floor | perstep ≥ **2.0× 0.1597 = 0.319** | `measure_kinematics.perstep_med` on A_dwell |
| coverage floor | tr11 ≥ **2.0× 0.0906 = 0.181** | `measure_tremble_baselines["tr11"]` |
| confusion ceiling `C_ceil` | perstep ≤ **1.310** | `measure_tremble_baselines["confusion"]` (committed cross_med, VERBATIM) |
| R\* margins | perstep **0.558** ≪ 1.310; coverage **0.209** | `scatter_select.json` cells |
| SIG_DEPTH / READ_FLOOR / CAL_LIVE_MIN | 8 / 8 / 3 | census DEPTH-decisive; n≥8 power floor; liveness |
| α (fr ceiling) | 0.001 | own honest band (§10.22) |
| acq-guard margin | scatter sep_cat ≥ **0.90 ×** A_dwell sep_cat | MECHANISM_MAP §4 l.57 deployment falsifier |
| determinism | `torch.set_num_threads(1)` | standing |
| spec_hash | `41d6f0d5e7da` | unchanged by the delta (verified) |

## (c) Pre-check outcomes (G-select / G1a / G1b / G2)

- **G-select** CLOSED: `select_scatter` → R\*=0.50 (sole feasible cell; coverage floor binds), frozen +
  pinned (`X_SCATTER_R=0.50`), deterministic (byte-identical double-run), drift-asserted.
- **G1a / G1b / G2** CLOSED (deployed-horizon 1M, `exp_scatter_preflight.py` →
  `exp08/scatter_preflight_gates.json`): **all_pass = True, NO substitutions.**
  **G1b** (scatter cal {20,21,22,24,25} + verdict {0–7} + EXT {8,9} — 15 seeds): independence
  (per-lag / k / schedule / bg / cap) + zero-box-exit all PASS @1M.
  **G1a** (REUSED A_dwell {0–7}): PASS, no replay divergence.
  **G2**: F5 floors HOLD at deployed 1M — perstep **0.557 ≥ 2.0×0.1596 = 0.319** (contrast),
  coverage **0.209 ≥ 2.0×0.0902 = 0.180** (coverage), confusion margin **0.753** (perstep ≪ C_ceil
  1.311); R matches **0.50**. spec_hash `41d6f0d5e7da`.

## (d) Gate-executor table (every gate → executor + positive-delta smoke ID) + halt list

| gate | executor | smoke ID · falsifier |
|---|---|---|
| G-select | `exp_scatter_score.select_scatter` | sm-select-R0 (R=0 → floor1 fails); box sm-box (R≥1.125 → cl≤0) |
| build invariants | generator delta / `exp14_arms.smoke_scatter` | sm-parity (g_nuis byte-identical; nuis differs); (26) uncentered; (29) drift |
| ceiling | `exp_scatter_score.cell_feasible_scatter` | sm-ceiling (planted perstep > C_ceil → infeasible) |
| acq-guard | `exp_scatter_score.acq_guard` | deployed sep_cat ≥ 0.90× A_dwell → else HALT + re-derive (§4 l.57) |
| G1a / G1b | `exp14_arms._assert_one` (@1M, `exp_scatter_preflight`) | independence + zero-box-exit; REUSED-A = replay divergence HALT |
| G2 | `measure_kinematics` + `cell_feasible_scatter` | F5 floors hold @1M; R==R\* |
| G3 / G5 | `exp14_arms.run_exp14_arm` (@1M, mid-ckpt 500k) | cal ×5, verdict ×8 + EXT ×2 |
| G4 | `exp_scatter_score.cal_read_scatter` | liveness ≥3/5; α-uncuttable; band N<SIG_DEPTH; cal-converts→non-loadable |
| G6 | `exp_scatter_score.score_scatter` | matched-bar excess + census PRIMARY (n≥8 floor); sm-G6-guard (refuses w/o records) |
| G7 | refute-default panel | no lens assumes conversion / the scatter story |
| G8 | consolidate + push | terminal surface = DRAFT + gate log + matched-bar tabs + census + companions |

**Halt list:** liveness <3/5 → HALT (unposed); no α-compliant cut → HALT; band N≥SIG_DEPTH → judgment-class
HALT; G1b independence fail → substitute; G1a divergence → HALT-and-audit; G2 floors fail @1M → geometry
HALT; acq-guard fail → HALT + re-derive ceiling; G7 MUST-FIX/judgment-class → HALT.

## (e) Protocol instance note

`CORRIDOR_PROTOCOL.md` governs. Three touches: touch 1 (design ratified), **touch 2 = this package
(read once)**, touch 3 (terminal attribution). Between touch 2 and touch 3 is corridor: pre-named
conditions, halt fences, append-only auto-pushed commits, terminal verification. A clean corridor is
necessary, never sufficient. Cost: ~15 training runs @1M ≈ 54 min each (measured). SWEEP-CONVERTS triggers
the interior-concentration control before any paradigm-positive certifies.
