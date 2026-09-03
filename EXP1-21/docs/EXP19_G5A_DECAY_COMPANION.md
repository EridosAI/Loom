# EXP19 G8 COMPANION — conversion is a TRANSIENT EPISODE, not a stable end-state (Jason ruling, 2026-07-14)

Verified from committed `exp08/exp14_exp12_shuffle_s{0..7}_verdict.json` (per-window `exam_acc`, band 0.64,
post-acq). A REPORTED companion for the G8 package (Jason: "may be the most interesting thing"; "your
numbers, not verified by me" — these are now computed, provenance = the committed columns).

## The numbers (5 converters {0,2,4,5,6}; band 0.64; read_at=500000, last window t=499800)
| seed | class | longest episode [t0..t1] | len(win) | episode mean | peak win t | post-episode mean | tail-50 mean |
|------|-------|--------------------------|----------|--------------|-----------|-------------------|--------------|
| 0 | CONV | [97200..122400]   | 85 | 0.879 | 103800 | 0.615 | 0.479 |
| 2 | CONV | [101400..119100]  | 60 | 0.869 | 105900 | 0.504 | 0.518 |
| 4 | CONV | [45300..55800]    | 36 | 0.868 |  51300 | 0.514 | 0.498 |
| 5 | CONV | [120600..143400]  | 77 | 0.907 | 123000 | 0.519 | 0.496 |
| 6 | CONV | [429600..456300]  | 90 | 0.910 | 434100 | 0.732 | 0.616 |
(non-converters {1,3,7}: longest run len 3 — never a sustained episode.)

## What it says
- Every converter's episode ENDS well before 500k (latest t1 = 456300, seed 6). Peak 0.87–0.91 for 36–90
  windows (~11k–27k steps), then decays toward chance.
- The 500k read-checkpoint sits POST-episode, in the DECAYED regime, for all 5 converters (seed 6 least
  decayed — episode most recent, tail 0.616; the other 4 at ~0.48–0.52 = chance).
- Consequences:
  1. Validates the HALT that produced the G5a replay: a frozen-500k-checkpoint eval is a REVERTED model →
     ~chance for all seeds → wrong-reason all-fail. The per-onset REPLAY is mandatory.
  2. Conversion in this paradigm = a TRANSIENT EPISODE, not a stable end-state.
  3. The §3 horizon amendment was grounded on ONSET ("all 14 converted by 427.5k") — says NOTHING about
     PERSISTENCE. Onset ≠ durability. The detector is episode-based, so nothing in the arm breaks; but any
     future read that treats the 500k checkpoint as a converged model is WRONG.
- Ties to EXP15 durability-by-dose (the increment mean-reverted; 2/9 carriers) — decay is the same
  phenomenon seen window-resolved here.

## Provenance
- Recipe: longest run of consecutive post-acq windows with `exam_acc` ≥ 0.64; episode mean over that run;
  post-episode mean over windows after t1; tail-50 = mean of the last 50 windows. All figures COMPUTED from
  committed columns (not asserted).
