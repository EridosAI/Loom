# A5 clock diagnosis — review only

Read [A5_CLOCK_COMPATIBILITY_REVIEW.md](A5_CLOCK_COMPATIBILITY_REVIEW.md).

Finding: **APPARATUS DEFECT — correction required to pose approved longer horizons.**
The pinned apparatus falsely rejects the nominal 269.5-second command when
accumulated addition error exceeds its fixed clock allowance. The separate
270-second stage comparator also needs a coherent correction.

This package records diagnosis and alternatives, not an implemented correction.
A5 is still held. No world was evolved, no production code or existing test was
edited, and no authority object or Git checkpoint was created.

## Contents and custody

- The review explains the exact branch, arithmetic, timing domains, prior tests,
  proposed closures, required future tests and bounded effect on A1–A4 evidence.
- DIAGNOSTIC_RESULTS.json is the original detached-check result; ARITHMETIC_DETAIL.json
  preserves a scalar supplement including the explicit-addition/built-in-sum distinction.
- diagnose_clock.py is the new, already-executed detached diagnostic source. It
  depends on the original local paths and pinned runtime; it is not a launcher.
  Do not execute reference scripts merely because they are included here.
- references/ contains byte-identical copies of the pinned source, clock tests,
  prior reviews and selected held-proposal documents. The held manifest is an
  unchanged reference with no grant, not a replacement launch proposal.
- REFERENCE_MANIFEST.json binds those copies to original paths and hashes.
- SOURCE_IDENTITIES_BEFORE/AFTER.json and PRESERVATION.json record the diagnostic
  preservation checks. FINAL_VERIFICATION.json repeats preservation after packaging.
- FILE_MANIFEST.json binds each payload by path, byte count and SHA-256. The archive
  checksum is provided beside the ZIP; neither is an execution authority.

Only six pre-existing detached clock test cases, inert pending predicates, scalar
calculations and saved-record metadata reads were executed. Physical pause/resume,
world component tests, replay, A5 commands against a world, fields, RNG, prehistory
and ecological trajectories were not executed. The 5,579 saved A1–A4 decisions
checked here all retained their expected stage; earlier claim limits remain.

## Unchanged identities and open decision

P: 6bc9683b54e4fa80136fe8534d7713e2a250a95f

Apparatus: 5f07748102cb5eaa302569c87efbae095050e9fe

Held A5: 88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6

The recommendation is an apparatus-only correction using native indices for
scheduling and the unchanged physical recurrence for timestamp provenance.
Jason's decision and separate correction scope remain pending. Shared workbench
navigation, canon, old reviews and commissioning records were not edited.
