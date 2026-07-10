# Loose-N detectors: verify against the false-alarm EXPECTATION, not the crossing-count

**Cross-experiment carry.** Canon-linked from FRONTIER §10.24 as `[[feedback_loose_N_false_alarm]]`.
Origin: the EXP14 2×2 verdict, 2026-07-09.

---

## The rule

A "conversion" scored as **a sustained episode (≥ N consecutive windows ≥ band) appearing ANYWHERE
post-onset** over a long horizon has a per-seed false-positive probability that a **correctly-calibrated
per-window α does NOT bound.** The episode-anywhere criterion multiplies the per-window rate by the
number of post-onset windows.

**So: when a cell's band lands at a loose N (N = 3, or near the N-floor), its crossing-count (n/8
converted) is not a signal. Compute the false-alarm EXPECTATION and compare.**

---

## The arithmetic

Let a cell's honest per-position false-rate at its band be `fr` (the empirical rate of length-N windows
entirely ≥ band, over its honest null). For seed *i* with `n_i` post-onset windows there are
`m_i = n_i − N + 1` length-N positions, so under an independent-position floor

```
p_i  = 1 − (1 − fr)^m_i            # P(seed i shows >= 1 phantom episode)
E[phantom converters] = Σ p_i
P(X ≥ k)              = Poisson-binomial tail over {p_i}     # exact, deterministic
```

Use the **deterministic** Poisson-binomial. A clustered block bootstrap over the honest-null sequences
(circular blocks, resampled to each seed's `m_i`) is a legitimate cross-check and will read **lower**,
because real episodes cluster; but the deterministic number is reproducible and belongs in canon.

**Episodes, not positions.** `_consec_rate`-style estimators count hit *positions*: one episode of length
L ≥ N contributes `L − N + 1` of them. Converting a position-rate into an episode-rate by `λ = fr × m`
overcounts by the mean cluster size. At **N = 3** the null's episodes are almost all exactly length 3, so
position-rate ≈ episode-rate and the shortcut is safe. At larger N, **count episodes**, and count them
only within contiguous unmasked segments — a pooled null built by concatenating masked subsequences will
splice non-adjacent windows and manufacture runs.

---

## The case (EXP14 cell B — dwelled × coin, the dose-only carrier)

B's honest band came out **0.6667 × N = 3** — N at the floor, the loosest cell. B "converted" **5/8** at
verdict. The crossing-count read said *dose enables*. **It was a calibrated false-alarm artifact:**

- `fr = 0.000613` (honest, per-position, ≤ α = 1e-3 — **B's band did its job**).
- Post-onset window counts {1041, 752, 1592, 1450, 1585, 1543, 1591, 1472}; mean ≈ 1400.
- **E[phantom converters] = 4.50.** **Observed 5.** Dead on the null mode.
- Exact Poisson-binomial **P(X ≥ 5) ≈ 0.51** under the independent-position floor. (A clustered block
  bootstrap on B's honest-null sequences reads ≈ 0.37 — agrees in kind.)
- Per-seed false-conversion probability ≈ **0.56** at N = 3 over a 500k horizon, *at a correctly
  calibrated per-window α*.
- **Every B "conversion" is longest-episode exactly 3** — bare N. Across **all 13 B runs** (verdict
  {0–7} + cal {20,21,22,24,25}) there is **not one episode longer than 3.**
- The same detector fires on **3/5 of B's own cal seeds** — the very seeds used to *define* B's null
  (floor expectation 2.67, observed 3).

**B was refuted 5 → 0. The dose row went empty.**

---

## How to apply

1. **Compute the floor before reading the count.** `E[phantoms] = Σ p_i` over the actual per-seed window
   counts. If observed ≈ expected, the cell is **empty** (floor, not conversion).
2. **Corroborate with episode QUALITY, not presence.** Bare-N length + shallow depth (mean barely above
   band) + decay = artifact. Deep + long (≫ N) + high within-episode mean = real. (In EXP14 the real
   cells' longest episodes ran 36–90; the artifact's were flat 3.)
3. **Beware exposure-ranking as a *ground*.** "The firing seeds are the highest-window-count seeds" is
   **non-diagnostic** — a genuinely slow conversion predicts the same ranking (more post-onset time = more
   chance to convert). Record it as a descriptive note. The decisive grounds are the bare-N signature, the
   floor comparison, and the absence of any longer episode.
4. **Beware selection-forced zeros.** A pool of "non-converting" seeds has zero episodes ≥ N *by
   definition*. Such a pool cannot estimate the phantom rate at N; only the run-length statistics **below**
   the threshold are free. Extrapolate the hazard, and say when the answer is unestimable.
5. **This is report-don't-patch.** The band was honestly cut (per-window α held) — **do NOT re-cut it.**
   The floor-check rescues the READ; the band stands.

---

## Why this keeps mattering

Same discipline family as the draft-flip catches (the EXP14 screen's 15/16 false positives; the EXP11 and
EXP10 verdict flips): **a surprising count goes through adversarial verification — a refute-default panel
plus an independent floor-check — before it reaches an attribution table.** The count is the trap; the
floor is the instrument.

Related: FRONTIER §10.22 (band re-pin), §10.24 (the B refutation), EXP15's common-ruler floor analysis.
