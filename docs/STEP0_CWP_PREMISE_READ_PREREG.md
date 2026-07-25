STEP-0 — CWP premise read (per-dwell-position update pressure)
Status: TOUCH-1 TEXT FOR RATIFICATION. Content ratified in-chat 2026-07-24 (Jason) against the seat's sketch; this document is the committed form — ratification to be confirmed against THIS text. Seat/session: design chat, post-EXP19 / U-BUF thread, 2026-07-24. Provenance: v1.2 §5.2 (pre-registerable now, read-only); falsifier pre-named at v1.2 §6. Read-gates rule: this text commits before the read executes; the data (committed run records) already exists — the RULES for reading it are fixed here, before any look.
§1 Question
Does the certified-dead dwelled learner exhibit the structure CWP's premise requires — loss spikes at dwell boundaries with massed low-surprise within-dwell updates (v1.2 §5.1)? If the premise fails in-substrate, the CWP program closes before it opens (v1.2 §6, verbatim route).
§2 Sources — records only
Committed exp12_dwell run records in OUTDIR. CC enumerates the certified-dead cell's record set at pre-flight (the census is part of the pre-flight surface; the prereg does not assert filenames from recollection).
Fields per eval column: pos_err_word, pos_err_vis (training-stash meaning, per the committed _buffer_wave division-of-labor routing).
No checkpoint loads (row 53: resume UNFAITHFUL, root cause open — untriggered here). No new forwards. Pure record read.
A record missing a required field is excluded and reported (record name + missing field), never patched. Zero admissible records ⇒ HALT.
§3 Definitions (mechanical conventions — corridor-readiness additions, flagged)
Buckets: verbatim from committed POS_BUCKETS = ((1,1),(2,2),(3,3),(4,6),(7,12),(13,48)) (exp12_arms.py:160): p1, p2, p3, p4-6, p7-12, p13-48. p1 = onset; the other five = mid buckets.
Late quartile: for a record with N columns, the last N − floor(0.75·N) columns by t. Early quartile: the first floor(0.25·N) columns. Convention named per the even-count-median rule's spirit. N < 8 columns ⇒ HALT (too few to quartile).
Channels never pool (word-cell and vision-cell errors live on different scales — committed docstring). All statistics are per seed × per channel.
§4 Estimator (pre-named)
Per seed, per channel: onset-dominance fraction = the fraction of late-quartile columns in which err(p1) strictly exceeds every mid bucket's value in that same column. A column missing any bucket key is dropped from the fraction's denominator and counted in a reported columns_dropped companion. Strict inequality; no ties forgiven.
§5 Outcome cells (per channel, per seed) and routes
PREMISE-CONFIRMED: dominance ≥ 0.90. Route: record; map annotation per §8 claim ceiling; proceeds to inform the LR-probe trigger (banked, per the ratified sequencing).
PREMISE-FAILS: dominance ≤ 0.50. Route: the v1.2 §6 falsifier fires — "5.1's premise fails in-substrate; the CWP program closes before it opens." Map annotated; no rescue drafting.
PREMISE-WEAK: dominance ∈ (0.50, 0.90). Route: HALT — surface to Jason. No auto-route.
CHANNEL-SPLIT: the two channels of one seed land in different cells. Route: HALT — surfaced as its own outcome, never averaged.
Cross-seed: cells are reported per seed; no pooling across seeds. Any seed disagreement on cell ⇒ the disagreement IS the surfaced result (HALT-class, Jason rules attribution).
§6 Companions (descriptive, no cells, no gates)
The full mean per-position curve (all six buckets), per channel, late and early quartiles.
Early-quartile dominance fraction (the steady-state cell is judged on late only).
The same read on committed exp12_shuffle records, flagged: pos labels ride the permutation, so bucket membership no longer implies delivery adjacency — reported as contrast, licensed for no sentence beyond "the label-conditioned curve differs/does not differ."
§7 Corridor rows (gate · condition · executor · smoke · fail action)
gate	pre-named condition	executor	positive-delta smoke	fail action
G0 census	≥1 admissible exp12_dwell record; fields present	exp_step0_read.py --census	census on a fixture dir with one good + one field-missing record → exactly one exclusion reported	exclusions reported; zero admissible ⇒ HALT
G1 reader red-team	synthetic record with onset < every mid bucket lands PREMISE-FAILS; synthetic onset > all mids at every column lands PREMISE-CONFIRMED	exp_step0_read.py --smoke	observed red required: the naive/broken variant (≥ instead of >) must fail the tie fixture before the strict version passes	HALT
G2 compute	§4 estimator over the census	exp_step0_read.py	covered by G1 fixtures	any judgment ⇒ HALT
G3 terminal	one package: per-seed × per-channel cells + companions + census + gate log	assembled by CC	—	routes to seat verification, then Jason
Every gate names its executor and must have failed once (observed red) before its pass counts.
§8 Claim ceiling (licensed sentences, written before the run)
CONFIRMED buys: "the dwelled learner's committed error curves show a reliable onset spike in steady state — CWP's premise survives in-substrate." No mechanism claim; no gating claim.
FAILS buys the §6 route sentence only. Neither outcome touches B*, U-BUF, or the ordering finding. The read is premise-level, strictly.
