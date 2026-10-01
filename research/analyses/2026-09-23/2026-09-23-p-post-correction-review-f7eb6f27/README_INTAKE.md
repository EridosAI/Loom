# Loom P independent post-correction review — intake

**HOLD BEFORE COUPLING COMMISSIONING** at `f7eb6f27c661e3db193a4225b56a825d7e41739d`.

Read `LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md` first. It contains the complete delta review, R1–R3 table, exact identities, observed results and reproduction commands.

R2 and R3 are closed. The original R1 counterexample passes, but a resolvable oblique release/return still receives full-duration contact accounting. `reproduce_remaining_r1.py` deliberately exits 1 on the current unmodified checkpoint. This failure is the single remaining engineering closure requirement.

The evidence folders contain independent executions, not copies of the builder's logs. `reviewed_delivery/Loom_P_corrective_review_20260923.zip` is the exact audited 83,421,895-byte builder delivery, included without alteration so the code, sources and existing attempt-003 records accompany the review. Its SHA-256 is `7e33da1b05646c5af352a4114e99082c52b51b2b5966911f30816fb2911091da`.

`review_inputs/` contains the prior independent review, the current user request and the exact correction patch. `REVIEW_RECEIPT.json` identifies this review. `FILE_MANIFEST.json` provides sizes and SHA-256 for all other package members; the adjacent `ZIP_SHA256.txt` identifies the outer independent-review ZIP.

Review utilities use the reviewed Windows paths; reproduction on another host requires directing those read-only paths to an identity-verified extracted delivery and choosing a new output directory. The full report's commands preserve source/artifact bytes and run only components or saved-record reconstruction. No installation is needed on the reviewed host. Do not execute smoke/prehistory generators or mutating builder verification stages as part of intake.

Temporary test snapshots and poisoned ambient fixtures are excluded. Their result logs and all consequential RED/GREEN evidence are included. Initial review-harness setup/parser failures are retained and labelled separately from completed successful checks.

No source, target artifact, Git state or Workbench content was changed. This export was created outside the Workbench and does not perform intake, fixes, or commissioning.
