# EXP16 CORRIDOR — G7 HALT SURFACE (routes to Jason)

**Status: HALTED at G7.** The corridor ran clean G1→G6; the G7 refute-default panel returned **0
MUST-FIX** but **2 CONFIRMED judgment-class findings** (+1 nit). Per the G7 fail action ("any MUST-FIX
*or judgment-class finding* → HALT") and the wrong-reason rule ("a gate passed for a flawed reason is a
halt, not a pass"), the corridor halts and surfaces. **Nothing pushed; G8 held.**

## The material result (holds under every treatment)

**NO WORD-SIDE CAPTURE.** X (`exp12_dwell_expomid`, mid-dwell word-reward deleted) shows a count of
**2/10** at the borrowed band 0.6111×4 — below the ≥5 bar under any treatment, and both crossings are
**bare-N** (episode length exactly 4 = N). Fisher 2/10 vs A's 0/8 = p 0.294 (NS). Whatever the floor
label, the primary does not certify word-side capture and routes to Jason.

## Gate log

| gate | outcome |
|---|---|
| G1 pre-check @1M | 15/15 accepted, 0 swaps/halts, advisory agrees |
| G2 participation bar (X-blind) | ρ=0.167869 → **bar 0.065133** (in [0.10,0.25]) |
| G3 cal {20,21,22,24,25}@1M | 5/5 records, **all acquired** |
| G4 cal_read | liveness **5/5** · band **0.6111×4** loadable (CAL-CONVERTS/NOT-SHIFTED; own cut 0.6154×4 coincides) · participation **ALIVE** (median act 0.696 vs 0.065) · gradient **Δ 0.031 vs A +0.142 (collapsed)** — no fence |
| G5 verdict {0–9}@1M | 10/10 records, all READ |
| G6 DRAFT | k=**2** (s6,s7 bare-N), floor-audit AT-FLOOR → **NOT-CERTIFIABLE** |
| G7 refute panel | **0 MUST-FIX, 2 judgment-class SHOULD-FIX → HALT** |

## The two judgment-class findings (both independently reproduced digit-exact by the verify pass)

### 1. Floor-audit null is CONTAMINATED — the AT-FLOOR verdict is an artifact
The floor-audit null claims to exclude "conversions + shoulders" via a **≥0.6 × ≥8-consecutive**
exclusion (the EXP15 `phantom_floor_gate` band I reused). But EXP16 detects conversion at **0.6111 × 4**
(bare-N). **No cal seed has an 8-long run**, so the exclusion removes **zero** windows — while two cal
seeds genuinely convert at the audit band (**s21 @294300, s24 @288300**, bare-N length-4 episodes) and
are **left in the null**. Those two converters ARE the null's 3 "phantom episodes" → they manufacture the
`expected_phantom = 4.748` that produced AT-FLOOR (observed 2 < 4.748, P=0.984).
**Honest null** (exclude the cal converters) → n_ep=0 → floor_clean=**True** →
`_partition(k=2, n_read=10, floor_clean=True, ALIVE, loadable)` → **UNDERPOWERED** (k=2 < 5), *not*
NOT-CERTIFIABLE. Also: my `_floor_audit` **omits the `null_caveat`** its sibling `phantom_floor_gate`
carries (exp14_arms.py:1485), so the DRAFT never flags the contamination itself.
**Material terminal unchanged** (routes to Jason, no WORD-SIDE) — but the *reason* (AT-FLOOR) is wrong,
and the correct label is UNDERPOWERED.

### 2. §5 companion mislabels toward the WRONG side of the 2×2
`convert_status = "convert"` is set from the raw crossing count k=2 with no floor discount
(`exp16_score.py:386`). Combined with the collapsed gradient (Δ 0.031 vs +0.142), that selects the
**"collapse + convert = full causal chain" (WORD-SIDE) row** of the §5 2×2. But the honest,
phantom-discounted read — 2 bare-N crossings (identical in shape to the cal null's [4,4,4]), ~0 real
conversions, **participation ALIVE**, gradient **collapsed** — is the **"collapse + dead → VISION-SIDE
MASSING (participation ALIVE)" row**. The companion currently points Jason's attribution at the OPPOSITE
side from where the evidence lands. (Reported/not-gated, so the terminal is unaffected — but it is the
mechanism read the experiment exists to resolve, so the label matters.)

*Nit (terminal unchanged):* the gradient aggregation averages per-column bucket-means rather than pooling
raw errors — a minor asymmetry, does not move Δ materially.

## The honest scientific read (for your attribution)

The reward-drift was **removed** (gradient collapsed 0.031 vs 0.142 — mechanically confirmed) and the
word channel stayed **alive** (participation 0.696), yet **no robust conversion followed** (2 bare-N
crossings below the bar). Under H1 (word-side capture drives conversion), deleting the mid-dwell
word-reward should have *enabled* consolidation → conversion. **It did not.** That **leans VISION-SIDE
MASSING** — the mid-dwell word-reward was not the gate; the vision side feeds the capture — but it is
formally **UNDERPOWERED** (2/10, honest floor clean) and rests on a floor-audit whose exclusion band
needs fixing before the label is trustworthy.

## Decisions for you (all judgment-class — not mine to fold in-corridor)

1. **Floor-audit exclusion band.** The ≥0.6×8 exclusion (EXP15) doesn't fit EXP16's bare-N (0.6111×4)
   converter band → contaminated null. Fix = match the exclusion to the audit band (exclude the same
   ≥band×N the count uses) and restore the `null_caveat`? Trade-off: matching risks the over-stripping
   the ≥8 exclusion was designed to avoid ([[feedback_loose_N_false_alarm]] / the EXP14 honest-null
   re-pin). This is a scorer **definition** change → canon-amendment-routing.
2. **Companion label.** Phantom-discount `convert_status` (2 observed < 4.748 expected; bare-N) so the §5
   read lands on the VISION-SIDE row, not the WORD-SIDE row?
3. **Is 0.6111×4 (N=4) even the right EXP16 converter band?** It is looser (N=4) than the EXP14 N=5
   bands; the whole bare-N floor problem flows from it. (Borrowed from A_dwell via the NOT-SHIFTED gate,
   as pre-named — but you may want to reconsider N for EXP16.)
4. **Attribution** + whether to re-score with the fixed floor-audit and **resume** the corridor
   (re-run G7 → G8 → terminal) once you rule.

**Held:** the raw run records (cal + verdict JSONs, deterministic) and the DRAFT are local, unpushed;
G8 waits for the corrected DRAFT on your ruling. The scorer fix is judgment-class and routes to you —
I will not modify the floor-audit definition in-corridor.
