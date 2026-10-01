# Loom P — independent post-correction review intake

**HOLD BEFORE COUPLING COMMISSIONING**

Apparatus `9d31e7902658b15762052a2a6a3d161d64338524`; previous HOLD `05abf60401d08f38750bca589b1c040e10513d7b`; unchanged P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Review date 2026-09-25.

Start with `LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md` or `CLOSURE_TABLE.md`. Three remaining approval-integrity defects require closure. The original clock comparison is independently verified, both full suites pass 113 tests, and all 36 delivered fault/control pairs reproduce. Passing counts do not cover the counterexamples.

- `REPRODUCTION_COMMANDS.md`: exact commands, expected RED/GREEN outcomes and fresh-output instructions.
- `REVIEWED_IDENTITIES.json` and `provenance/scoped-complete/`: reviewed identities and complete preservation/reconstruction receipts.
- `canonical-001/`: strict-parser comparisons and 20 independently rejected semantic substitutions.
- `authority_runtime/`: actual-callable and pending-hold counterexamples, replay consequences, neural/firewall regression, and independent audit of all 72 logs.
- `physical/`: independent Decimal clock oracle, manufactured pause/restart proofs, and a fresh original-05ab authority RED.
- `old-pairs-001/` and `new-pairs-001/`: all delivered RED/GREEN logs and command matrices.
- `reviewed_delivery/`: byte-identical corrected builder ZIP, expected SHA-256 `e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81`. Its nested archives preserve the earlier builder/reviewer packages.
- `references/` and `CORRECTION.patch`: latest review request, previous independent HOLD review, builder report and exact correction patch.
- `FILE_MANIFEST.json`: size/hash for every included payload file. The adjacent `INTAKE_RECEIPT.json` identifies the complete ZIP after reopening and verifying it.

All synthetic approval files are manufactured test data, NOT Jason approval. No commissioning case, 600-second life or new prehistory was run. This is an intake artifact only; no Workbench file was changed. Source paths in evidence preserve original execution provenance; see reproduction instructions before repeating elsewhere.

Disposable pytest temporary trees and the redundant extracted builder tree are excluded; full independent counterexample/clock component records, all 72 fault/control logs, reports and receipts are included. Incomplete preliminary provenance receipts are retained transparently and superseded by `scoped-complete/`.
