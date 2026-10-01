# Loom P apparatus independent review — intake

**HOLD BEFORE COUPLING COMMISSIONING**

Read `LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md` first. It contains the complete independent review, concise closure table, exact reviewed identities and smallest required closure. `REPRODUCTION_COMMANDS.md` supplies the commands.

Two apparatus corrections are required at `05abf60401d08f38750bca589b1c040e10513d7b`:

1. Bind execution approval to the complete case, arm/controller and prescribed route contract.
2. Correct the deterministic controller's floating-clock deadline comparison so a nominal due boundary does not add another ten-step command hold.

P remains at unchanged scientific checkpoint `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Both 83-test suites and all 16 delivered fault/control pairs reproduced; the HOLD is based on independently demonstrated gaps outside those tests.

The `neural`, `physical`, `provenance`, boundary and fault files contain independent evidence. `reviewed-inputs/Loom_P_Commissioning_Apparatus_Review_20260924.zip` is the byte-identical original builder delivery located by Jason in the Workbench inbox. It is not a rebuilt or corrected delivery. Its own older claims remain builder claims; this review determines the independent disposition.

`physical/MANUFACTURED-AUTHORITY-NO-EXECUTION.json` is intentionally synthetic test data, explicitly marked not Jason authorization. It was used only for guard validation and must never be treated as a commissioning grant. No commissioning case was run or chosen. No target or Workbench content was changed, and no fix was made.

This archive is prepared for later Workbench intake. It does not perform intake, launch work, grant execution, or freeze the coupling. Complete the two narrow corrections and their independent closure before seeking a separate commissioning execution decision.

The inventory covers all included files except the inventory itself. The separate ZIP checksum and package-verification receipt cover the sealed archive. Fresh pytest temporary trees and the extracted duplicate portable payload are omitted; substantive logs, scripts, results and manufactured evidence remain included.
