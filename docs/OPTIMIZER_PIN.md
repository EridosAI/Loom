OPTIMIZER PIN — M2/M3's timescale constants, read from code
Status: TOUCH-1 TEXT FOR RATIFICATION. Content ratified in-chat 2026-07-24 (Jason); this document is the committed form — ratification to be confirmed against THIS text. Seat/session: design chat, post-EXP19 / U-BUF thread, 2026-07-24. Provenance: banked as "the optimizer pin (code-read, cheap) — M2/M3's timescale constant" (MECHANISM_MAP_conversion_gating.md:71; v1.2 §7 rank 2). Pure code-read: no runs, no records, no checkpoints.
§1 Reads (each verified against the cited line at HEAD; drift from any cited line ⇒ HALT)
Optimizer construction: torch.optim.Adam(params, lr=cfg.lr) — experiments/04_stage0_mvp/loop.py:68.
Learning rate: lr = 3e-3 — experiments/04_stage0_mvp/constants.py:87.
Hyperparameters by omission ⇒ PyTorch defaults: betas (0.9, 0.999), eps 1e-8, weight_decay 0. Gate: CC greps the tree for any betas/eps/weight_decay kwarg on the optimizer path; any hit ⇒ HALT (the derived constants below die with non-default betas).
Scheduler: none (seat grep this session; CC re-verifies — any scheduler/lr mutation on the training path ⇒ HALT).
Param-group census: which parameter tensors the optimizer holds, and the lr=0 frozen exclusion noted at loop.py:8 — enumerated, not summarized.
Installed torch version on Equinox recorded alongside (the env-lock PATHWAY item remains open; this read does not close it, it timestamps one fact).
§2 Derived constants [MEASURED-from-code]
τ₁ = 1/(1−β₁) = 10 waves (first-moment memory).
τ₂ = 1/(1−β₂) = 1000 waves (second-moment memory).
Per-wave step scale = lr = 3e-3 (bias-corrected Adam; order-lr steps).
§3 Flag-level commentary (annotation text, verbatim; commentary is NOT evidence)
Optimizer pin READ 2026-07-24: Adam, lr 3e-3, default betas ⇒ τ₁ = 10 waves, τ₂ = 1000 waves. Flags, not findings: τ₁ ≈ E[k] = 11 — first-moment memory spans one dwell, so massed same-member runs saturate momentum; τ₂ = 1000 sits within 2× of B*'s upper edge (512). These are the timescale constants the M2/M3 slots reference; any LR/betas arm design prices against them.
§4 Landing
Artifact: outputs/optimizer_pin.json — fields: optimizer_class, lr, betas, eps, weight_decay, scheduler (null), torch_version, param_groups (census incl. exclusions), tau1, tau2, source_lines (the §1 citations), read_date, HEAD commit.
Annotate-in-place (stale-pointer style, original text stands): MECHANISM_MAP_conversion_gating.md item 2 and MECHANISM_MAP_v1_2_RECONCILED.md §7 rank 2 — append "[PINNED 2026-07-24 → optimizer_pin.json: τ₁=10, τ₂=1000]".
§5 Corridor rows
gate	pre-named condition	executor	smoke	fail action
P0 line-verify	§1 citations byte-match HEAD	exp_opt_pin.py --verify	fixture with an edited line ⇒ observed red	HALT
P1 defaults	no betas/eps/wd kwargs; no scheduler	exp_opt_pin.py --verify	fixture adding betas= ⇒ observed red	HALT
P2 emit	artifact fields complete; τ values computed from the read betas, never re-typed	exp_opt_pin.py	field-drop fixture ⇒ observed red	HALT
§6 Claim ceiling
The pin buys descriptive constants and the §3 flags, verbatim, nothing more. It licenses no claim about the block's mechanism, no K/B correspondence, and no LR-arm inference; it prices them.
