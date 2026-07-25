# EXP20 U-BUF — PRE-FLIGHT PACKAGE (touch 2; assembled by CC)

**Status: COMPLETE — routes to the design seat for verification, then Jason for touch-2
ratification. HARD HOLD at G4 — no verdict run launches until ratified. The cal table licenses no
prose: constants are constants; nothing here is a dose-response sentence (the EXP19 corridor rule).**
Prereg: `docs/EXP20_UBUF_PREREG.md` (`0741717`, canon as attached). Build: `f45939a`. G2+cal
executor: `a333c45`. Protocol instance: `docs/CORRIDOR_PROTOCOL.md` at HEAD, contents (a)–(e).

---

## (a) Operational definitions, VERBATIM where they bite

### EXP19 §2.4 non-causality (prereg :123-129, byte-extracted)

### 2.4 **W-PERM is NOT causally realizable** *(quote VERBATIM in the terminal)*

> *"Permuting a window of B requires having already seen all B waves before emitting the first — a B-wave
> lookahead. No agent has that. W-PERM **measures the ordering window B\***; it does **not** show that any
> realizable mechanism can produce it. **U-BUF tests realizability, and its bar is B\*.** A W-PERM positive
> reported as 'a path to reality' is a pre-named overclaim, not a finding."*

**Three tiers:** W-PERM measures B\* → U-BUF must reach B\* **causally** → CWP must beat or match U-BUF.
*(Context change, prereg header: CWP CLOSED at step-0 — the third tier is vacated; U-BUF's question
stands alone: realizability.)*

### The certification law (exp19_floor.py:16-21, byte-extracted)

CERTIFICATION = the FLOOR AUDIT, blind and in-regime:
  (i)  EMPIRICAL floor — the non-converters' own longest stratum runs (they carry the real granularity AND
       autocorrelation). Ceiling = max over {1,3,7}. Converter excess over it, with margin.
  (ii) SIMULATED floor — per seed, N_SIMS draws preserving each window's ACTUAL in-stratum onset count,
       Bernoulli at the seed's post-acq stratum mean p_hat (conservative: for converters p_hat is inflated
       by their own episode), longest run >= FLOOR_BAND. Converter observed run vs its null max -> p-value.

*(EXP20 instantiation: N_SIMS = 5000, SIM_SEED = 20260714 — the committed simulator constants; the
BAND is the fresh in-regime cut of §(b), injected into the law's module globals by `exp20_cal._band`,
never edited in the committed law.)*

### The stream-marginal amendment (canon §10.29, byte-extracted; ledger 52, standing)

**LEDGER-52 STANDING AMENDMENT (ratified):** *The floor-audit certification law's advertised tail bound is
computed marginally over simulator streams, not conditionally on the pinned stream. A certification whose
stream-marginal tail exceeds the law's own advertised bound rides QUALIFIED and never enters a headline
count unqualified.*

Scheme (exp19_stream_stability.py:27): gseed = SIM_SEED + 1_000_003·(k+1) + seed, k ∈ 0..199.

### The committed EXP19 stratified cutter (exp19_score.py:46, byte-extracted)

def _zero_preceding(dwell_id, is_exam):
    return is_exam & _first_occ(dwell_id)

**EXP20 transport derivation (prereg §3 assigns this to pre-flight; ratified AT touch 2, not before):**
the committed form reads "no contaminating wave before the exam", where contamination is the channel the
shortcut lives in. On W-PERM's emitted stream that channel was same-DWELL waves emitted ahead of their
onset. On U-BUF's DELIVERED stream, same-dwell pre-delivery is impossible by causality (a dwell's waves
do not exist before its onset; deliver[t'] ≤ t' < t) — the shortcut channel is same-MEMBER replay within
the buffer's reach. Transported form (`exp20_ubuf.delivered_zero_preceding`, fixtures hand-verified):
onset exam at t is delivered-zero-preceding iff NO same-member wave was DELIVERED in the trailing window
**W = K** (the buffer's own reach — a wave leaves the buffer permanently after K steps, so K bounds the
replay-recency channel exactly). Measured support at W = K, W = 2K, W = ∞ rides in
`exp08/exp20_g2_maps.json` (§(c)); the W = K choice is **the touch-2 ratification's to confirm**.

### RESCUE-MONOTONE, committed form (EXP19 prereg :325, byte-extracted)

| **RESCUE-MONOTONE** | conversion rises with B; knee at B\*, **surviving the stratified read** | Ordering is the gate; **U-BUF unlocks, bar = B\*.** *(flattering)* |

*(EXP20 §5 instantiates: certified count non-decreasing in K with ≥1 strict rise, surviving the
delivered-stratum read.)*

### The §5 outcome cells — as committed in the prereg (`0741717`), read from there at verdict; the
routes table is NOT restated here (carry-verbatim applies to the prereg itself, which is the committed
gate object).

## (b) Constants — formula · measured inputs · value · provenance

| constant | formula / recipe | inputs | value | provenance |
|---|---|---|---|---|
| SEED_UBUF | dedicated substream base, conditional registration (K≥2 only) | collision audit vs 61000-64199, 91000-99047, 100000-100025, loop-side seeds | **101000** | `exp12_fabric.py` (build `f45939a`); tree grep clean at build |
| delivery law | deliver[t] ~ Uniform{max(0,t−K+1)..t}, one f64 rand/wave, K=1 short-circuit | — | `ubuf_map()` | prereg §2; fixtures: causality t+1 plant RED, length plant RED |
| cutter window W | W = K (derivation in §(a)); alternatives measured | G2 maps, 8 seeds × 3 K | support: K32 ≈ 66.6–67.2k · K128 ≈ 24.6–24.9k · K512 ≈ 470–530 of ~90k onsets | `exp08/exp20_g2_maps.json`; **W = K to be confirmed at touch 2** |
| multiplicity envelope | measured per K per seed, never assumed | same | p_never 0.362–0.368, K-invariant (≈ Poisson(1) 0.368, re-measured) | same artifact |
| band + N ("conv band, θ") | `XA._provisional_cut` (§10.22 joint honest-null cut) on pooled post-acq per-window E-B accs, 5 cal seeds, per K | 15,342 / 16,366 / 16,278 pooled windows (K32/K128/K512); no acq=None anywhere | **K32: 0.6154 × N4 · K128: 0.6190 × N4 · K512: 0.6333 × N12** | `exp08/exp20_cal.json`; formula committed pre-EXP20, constants cut in-regime |
| cal-seed split (width 300, in-regime band) | `SC._certify_seed` per cal seed (obs vs own 5000-sim null max) | cal records | K32: 0/5 certify (runs 2–4 vs null max 6–8) · K128: 0/5 (2–3 vs 6–8) · **K512: 3/5 — s22 (8 > 7), s24 (46 > 7), s25 (16 > 11); s20/s21 at 3–4** | same; the corridor's :86 split precedent |
| operating points / width floors | argmax converter/floor separation on the (K, read)'s own null (ledger 42) | cal records | **K512/full: op 500, width floor 300.** K512/delivered-stratum: NONE — in-arm STRATUM-UNDERPOWER (HALT below). K32/K128: no in-arm converter — no op cut; the SPLIT-precedent width question rides to touch 2 | same |
| powercert (K32/K128, both reads) | G5b machinery: C's committed converters thinned to target density, 20 draws, certify vs own null; bar ≥ 0.90 | committed C wavecache + cal densities | **K32: 1.00 / 1.00 (full / delivered-stratum) · K128: 1.00 / 0.94 — ALL PASS** | EXP19-SPLIT precedent; 1M-grid null-inflation companion: null_max 24–25, q999 20–22 at p_hat_ref ≈ 0.621–0.622 (REPORTED, never bridged) |
| 200-stream marginal nulls | gseed scheme above, per K per cal seed, width 300 | cal records | pinned null_max within the 200-family [min,max] in 14/15 cells; exception K512 s25: pinned 11 > family max 10 (conservative pinned stream, recorded) | same |
| horizon | read_at = 1M primary (LATE-RESCUE-IN-TAIL absorbed); from-scratch only (row 53) | prereg §4 ruling | 1,000,000 | prereg `0741717` |
| seeds | verdict {0..7}, cal {20,21,22,24,25} | registry | pinned | `exp19_corridor.py:33-34` |

## (c) Pre-check outcomes (rule citations; no substitutions anywhere)

- **G0 (fabric-hash + K=1 REUSED):** PASS, red observed first. All 10 fabric fields `torch.equal`
  dwell-vs-ubuf_K32; substream keys == the committed verdict manifest s0 (fabric block); the broken
  variant (ONE consumed draw from `loop.gen`) diverged the record — observed RED — then the proper
  short-circuit ran **digit-exact on every shared field** vs a fresh exp12_dwell (N=2000, 6 columns),
  E-B additive (166 onset reads, zero draws). Committed pre-delta ref carries a different config
  (exp12-era, read_at=None) — the manifest-key anchor covers the regression fence instead; recorded.
- **G1 (B11 + diff-scope):** PASS per invocation. Blast radius confined to the whitelist; learner
  chain EMPTY-SET byte-identical; live `EXP12Loop.step` == baseline `Stage0Loop.step` byte-for-byte;
  red-teams: eval-path perturbation FIRES, out-of-scope exp14_arms perturbation FIRES, planted
  runtime step override FIRES and restores clean. Baseline commit `0741717` (fresh, this edit).
- **G2 (map asserts + multiplicity + support):** PASS, 8/8 verdict seeds. Causality/length asserts
  green on every (K, seed); fixtures: planted deliver[t]=t+1 RED, length plant RED, cutter
  hand-fixture exact, empty-support fixture FLAGGED (the rider's red). Support (W=K) non-empty
  everywhere; **K512 thin (470–530 per seed) — STRATUM-POWER-SHAPE flag, sensitivity lowest at the
  K nearest the EXP19 bracket's upper edge.**
- **G3 (cal):** COMPLETE — constants in §(b), full curves + per-seed detail in
  `exp08/exp20_cal.json`. **One pre-named HALT surfaced: K512/delivered-stratum is
  STRATUM-UNDERPOWER (in-arm)** — with three in-arm cal converters available as known signal, no
  swept width lets them clear the phantom floor on the ~480–560-onset stratum; the null is
  uninterpretable there, per the committed gate. No workaround taken; routed to touch 2.

## (d) Gate table — executor · positive-delta smoke · observed-red evidence

| gate | executor | smoke / red evidence |
|---|---|---|
| G0 | `exp20_ubuf.py --g0` | consumed-draw broken variant RED (gatelog `G0.k1_broken_observed_red`) |
| G1 | `exp20_diffscope.py` (main) | 3 red-teams fire per invocation (gatelog via stdout, committed) |
| G2 | `exp20_ubuf.py --g2` | `--fixtures`: causality t+1 RED, length RED, empty-support FLAG |
| G3 | `exp20_cal.py --cut` | `--smoke`: band-injection bites (0.7-episode: band 0.60 certifies, 0.90 not), chance-converters → STRATUM-UNDERPOWER RED, planted converters green |
| G4 verdict | `XA.run_exp14_arm` ×24 (from scratch, checkpoint contract on) | **HARD HOLD — launches only on touch-2 ratification** |
| G5 certify + cells | `exp19_scorer` machinery at the G3 constants (band-injected), stream-marginal per ledger 52 | inherits G3 smoke + the committed law's fixtures |
| G6 terminal | assembled by CC → refute panel → seat → Jason | — |

**Halt list (live):** fence violations (B11/diff-scope) · fabric-hash divergence (never substitute) ·
causality/length assert · empty delivered-stratum support · STRATUM-UNDERPOWER · G7-style integer tie
at op selection · STRATIFIED-ONLY certification (not a §5 cell) · any outcome landing in no named §5
route · MULTIPLICITY-CARRIED envelope breach.

## (e) Protocol instance note

CORRIDOR_PROTOCOL at HEAD governs; the estimator-support rider (row 55) is WIRED (G2's support check
+ its empty-support red fixture). Every gate above has failed at least once before its pass counts.

## Flags & envelopes riding into the read (recorded now, before any verdict data exists)

1. **K512 delivered-stratum thinness** (470–530 onsets/seed at W=K) — the underpower gate's teeth
   land exactly where the EXP19 bracket predicts rescue; a K512 null that cannot be powered is
   uninterpretable, per the committed gate.
2. **E-B ≡ E-A on the identity arm — measured 6/6 columns EXACT** (acc and n, under the record's
   own 6-digit rounding; K=1 smoke, N=2000). An earlier 4/6 reading was CC's comparison artifact
   (raw float vs stored rounding), caught in-session and corrected — erratum recorded at the G3
   commit. The probe read reproduces the exam channel exactly where they coexist, so the K=1 seam
   reduces to **unlike-horizon** (the committed E-A certification is 0/8 dead at 500k; paid arms
   read E-B at 1M). Licensed as the arm's zero point by BAR-1 (existence, per-K vs own null); any
   cross-K evidence sentence stays matched-bar-scoped and none is licensed by §1.
3. **Grid asymmetry in powercert**: the committed G5b machinery certifies on C's 500k grid; EXP20
   reads at 1M (≈2× windows → longer nulls). The 1M-grid null-inflation companion rides beside every
   powercert number; the asymmetry is reported, never bridged.
4. **acq on cal seeds**: any None acquisition_onset is treated as 0 (whole-read window grid) and
   listed in the G3 artifact (`band_inputs.acq_none_treated_as_0`).
5. **Warm-up**: t ≤ K ≤ 512 of 1M — WARMUP-CARRIED (§5) is descriptive at these scales.
6. **Costing (§8, itemized so it is chosen)**: paid 24 verdict runs × 1M ≈ 24 × ~36 min CPU-class +
   15 cal runs (spent at G3) + conditional K=2048 (8 × same class, fires only on ALL-PAID-DEAD).

## The touch-2 questions (Jason rules; surfaced, not recommended)

1. **W = K** for the delivered-stratum cutter (derivation §(a); alternatives measured in G2 maps).
2. **K32/K128 verdict width** — no in-arm cal converter at either K (powercert PASSES all four
   cells): the EXP19-SPLIT precedent ran verdicts at the committed instrument width 300; the
   sweep's alternatives are in the artifact. Fires: yes.
3. **K512/delivered-stratum STRATUM-UNDERPOWER (the HALT)** — §5 makes the stratified read the
   headline, and the stratified read is unpowered at exactly the K where the full read has an op
   (500) and the cal split shows in-arm signal. The §5 cell logic (RECENCY-CARRIED requires the
   stratum read; RESCUE-MONOTONE requires "surviving the stratified read") cannot evaluate at K512
   as ratified. Committed-machinery facts for the rule: support ≈ 480–560 onsets/seed (W = K);
   W = 2K support ≈ 130–160; W = ∞ ≈ 0 — wider windows only thin it further. This is the wp-strat
   species, pre-named by the underpower gate; it needs your text, not a workaround.
4. Ratification of the G3 constants table (§(b)) and the envelopes above.
