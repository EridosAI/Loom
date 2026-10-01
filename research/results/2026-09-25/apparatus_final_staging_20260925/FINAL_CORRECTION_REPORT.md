# Loom P apparatus — final three-finding corrective pass

Date: 2026-09-25. **Builder verification complete; stop for final mechanical closure review.** This is not a declaration of commissioning fitness or execution authority.

Previous apparatus checkpoint: `9d31e7902658b15762052a2a6a3d161d64338524`. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The new checkpoint is recorded in the portable `CHECKPOINT.json`, alongside its exact `FINAL_CORRECTION.patch`. Worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`; branch: `build/p-commissioning-apparatus-20260924-01a0c405`.

## Authority, scope and environment

The exact user request and complete `LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md` are preserved under `developmental_ecology/artifacts/apparatus-final-correction-20260925-01a0c405/references`. Only its three reproduced HOLD findings A-R1a, A-R1b and A-R1c were corrected. The already accepted numerical deadline comparison was not modified. Current Workbench orientation remains a historical navigation record; no canonical Workbench document or scientific sequence was rewritten.

Execution was Windows desktop-local, using the existing Python 3.13.5 environment, NumPy 2.3.3, SciPy 1.16.2, pytest 8.4.2 and Git 2.50.0.windows.1. A scoped temporary create/read/delete check passed in the new evidence directory. No dependency installation, cloud execution substitute, new worktree, remote operation or background scientific run occurred. Local writes/commit used the authorized existing apparatus worktree; no vault Git write occurred.

## A-R1a: one unambiguous approval object

The exact two review files were accepted by unchanged 9d31e790 before edits: conflicting duplicate `approved_execution`, and conflicting nested route `point`. Their raw bytes were independently preserved and the original acceptance is recorded in `old-duplicates-RED.log` and `old-9d31-duplicates/RESULT.json`. No world step or commissioning constructor was used.

The new `strict_loads` rejects duplicate JSON names at every nesting level, including identical duplicates and names that decode to the same string. Canonical input must use actual string dictionary keys and JSON-native values; integer-key coercion is rejected. Sorted keys and whitespace still do not alter an unambiguous semantic object. Non-finite values remain invalid. No first/last-value selection is performed.

Approval documents have a closed envelope: `notice`, `approved_execution_sha256`, `approved_execution`. An additional alias such as `approved_manifest`, `route` or `controller` is rejected rather than silently ignored as a second prescription. The existing manifest and nested execution schemas remain closed; their required mirrored case/controller/mode/adapter/resource identities must agree. The apparatus supports no alternative alias spelling for those fields. The descriptive protocol is checked recursively and cannot contain a second typed execution field such as controller, route, stage or intervention, even inside a descriptive step. Protocol descriptions are not an override or a second configuration source; no natural-language interpreter is claimed.

The same parser guards restart wrappers, record/receipt input and sensor command JSON. Packed restart dictionaries use pair lists, so a separate pre-unpack uniqueness check prevents repeated semantic keys in that representation from being collapsed by P's unchanged decoder. Sensor gateway changes are limited to these parser calls: a duplicated actuator field is rejected before gateway submission. The sensor interface, information boundary and command policy were not redesigned.

Human-readable material contains the exact unique object used for the existing full execution digest. Raw request-byte identity, the readable object/digest match, and all former case/state/duration checks remain active.

## A-R1b: bind the actual causal dispatch

The exact original alias failure was reproduced on unchanged 9d31e790. A same-display-name replacement at `runner.waypoint_command` delivered `[-0.5,0.5]` in one native step while the checked controller would have produced `[0.717668244562803,0.237668244562803]`. Original replay accepted that record. See `old-dispatch-RED.log` and `old-9d31-dispatch/`.

The runner now checks its actual invocation references and captures them in a read-only dispatch mapping. The callable captured and checked is the callable invoked. It verifies agreement with the approved module's function identity/configuration and disallows an alternate function/proxy, unexpected function globals, defaults or closure state in this supported dispatch. The same rule covers the other direct command-path aliases (`privileged_input`, `command_pair`, `time_due`, `observe_without_interference`) and the sensor-history class reference. Module implementation/constants still must match the manifest.

Commands are computed from a detached approved route copy. The runner rechecks dispatch/specification and route/session integrity before accepting the result. A targeted check swaps the global runner reference immediately after validation: the captured approved callable is used, the substituted callable is never invoked, and the later check rejects the changed dispatch before command recording or world advancement.

For physical advancement, the actuator pair comes from the independently retained serialized issued decision, rather than a second read of the exposed mutable `held_command` after validation. This binds the command actually passed into unchanged physical advancement. Matching implementations can be reconstructed in another process from the same approved specification; Python memory addresses are not portable approval identities.

## A-R1c: issued decisions and legal pending remainders

The exact original persistence failure was reproduced before edits: begin a ten-step first-stage command, advance seven steps, alter the pair and change remainder three to four, use ordinary close/resume, then reach native index 11 at `0.10999999999999999`, beyond the `.1` first-stage deadline. Both original segments passed the old verifier. No record checksum was forged in that reproduction. See `old-pending-RED.log` and `old-9d31-pending/`.

Each newly issued action now retains its native index/time, controller identity and full execution digest, exact inputs and command, issued hold length, selected stage identity/start/absolute deadline, case deadline and annotation. The public session carries the decision for inspection; a separate immutable byte representation records what the segment actually issued. A public edit to the decision, pair, cursor or remainder cannot update that retained representation.

Before advancement and normal save, the apparatus checks the decision against the approved controller/route; derives native progress from actual index minus issued index; requires the remaining count to equal issued steps minus progress; checks elapsed time against native cadence, including the existing partial-terminal exception; and verifies the remaining interval lies within stage and case authority. A changed pair, enlarged remainder, coherent replacement decision, stale completed-stage hold or inconsistent clock is rejected before another native step. The original numerical tolerance, native dt, full-hold rule and global-case shortening remain unchanged.

Restart loading returns values with a separate read receipt over the complete losslessly serialized session, engine and manifest. Direct session edits fail before recorder creation. A resumed constructor also compares these values with the verified source snapshot, validates the source segment's issued-action journal, and accepts only a complete administrative pause. It records a relative parent-segment link and manifest identity. Source origin, body state, complete session and pending decision must remain continuous across segments.

Record validation now checks issued actions, derived remainders and final pending state even when physical replay is disabled. For a resumed segment, it also verifies the parent and exact initial/final state/session continuity. A separate coherent saved-payload corruption with honest recomputed checksums is rejected because it disagrees with the original action journal. The old practice of trusting a resumed initial command merely because replay reproduces its later arithmetic is closed for the reproduced class.

Invalid pending state is rejected, not silently shortened or used as a rescue. Continue from its intact verified state/checkpoint. Once the legitimate first-stage remainder is zero at its deadline, the next stage generates its own new command. The test returns a deliberately corrupted boundary remainder to its intact issued-decision value and confirms that only the newly generated next-stage command advances. No stale pair leaks forward.

## Results and evidence

| Verification | Result |
|---|---|
| Original 9d31e790 counterexamples | Three observed RED failures before edits; duplicate approval, actual dispatch, ordinary saved pending overrun |
| Previous original apparatus matrix | 16 RED→GREEN pairs; original script/test bytes unchanged |
| Previous correction matrix | 20 RED→GREEN pairs; original script/test bytes unchanged |
| New narrowly scoped matrix | 18 RED→GREEN pairs |
| Final worktree suite | **143 passed**: all 113 existing + 30 new |
| Final assembled portable suite | **143 passed**; log packaged after the run |

New pairs exercise five duplicate cases, non-string canonical keys, approval aliases, nested protocol shadows, five actual dispatch references, four pending mutations, and saved decision-journal disagreement. Faults remove the named production guard or restore the old parser/unchecked dispatch while leaving the rest active; each reaches its explicit breach assertion, followed by its clean control. They are not a new broad adversarial campaign. All prior failed and successful evidence is retained in separate directories. Final results are the `*-002` suite logs and `*-final-002/FAULT_MATRIX.json` files; earlier successful attempts remain labelled as intermediate evidence.

Additional positive/negative checks cover the exact review raw files, required semantic mirrors, post-approval constants/route edits, a same-name proxy, replacement between check and use, mismatching reconstructed dispatch on resume, exact approved resume, duplicate packed pending keys and a duplicate command request rejected before submission.

A real seven-step pause retains three steps. Its valid resume ends the first hold at index 10, then runs ten fresh second-stage steps to index 20. The resumed segment has exactly thirteen .01 field calls; the inactive external neural/RNG state is unchanged and there are no neural waves. At rejection points, complete engine hashes and causal-call sentinels show no advancement. The original unchanged tests supply further intact/fixed/external cadence, field, noise, terminal and complete-state reconstruction controls.

Detached saved-state boundary inputs cover a valid `.07`/index-7/remainder-3 state, a crossing `.09`/index-9/remainder-2 state, exact `.1`, `.1-5e-11`, and `nextafter(.1,+infinity)`. Stale positive remainders are rejected. At nominal native index 10, the intact zero remainder is accepted and route selection proceeds to stage 1. Injected nearby clock values are explicitly manufactured preflight inputs, not asserted to be reconstructed physical trajectories. These checks use actual native-index progress; they do not enlarge timing tolerance or round world time.

The initial unchanged regression attempt passed 112 and failed one fixed-structure restart because the new read receipt attempted ordinary JSON encoding of frozen NumPy arrays. The receipt now uses P's existing lossless state hash; approval JSON remains strict. That failed log is preserved. No P serializer, frozen-state law or existing test was changed. The first 27 new checks then passed; two targeted dispatch/gateway checks brought the additions to 29 and both intermediate suites to 142 passes. The final nested-protocol shadow rejection added one targeted check and one fault/control pair, bringing the final suite to 143 and the new matrix to 18 pairs. Intermediate apparatus sources are retained under `attempt-001-source`; its saved records retain that runtime identity. Final saved examples are under `review-evidence/final-suite-002`, with their parent chains.

All final suites use the pinned local environment, disabled bytecode/plugin autoload/pytest cache, and fresh temporary roots. The portable run removes ambient `PYTHONPATH` and uses the assembled code and explicitly packaged verified life-0 cache. No prehistory preparation occurred. Test wall times are reported in logs, not extrapolated into a commissioning budget.

## P, runtime and preservation

All thirteen P modules remain byte-identical to their `6bc9683b` Git blobs, aggregate SHA-256 `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`. Configuration retains its baseline Windows checkout bytes, SHA-256 `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`, and semantic identity `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. The unchanged LF Git / CRLF checkout representations are disclosed separately; no normalization was performed.

All 59 P engineering checks remain unchanged and green. All 113 existing tests, their old fault scripts and the previous saved clock fixture remain unchanged. Controller arithmetic/comparator source, contract, adapter, diagnostics, initialization and evaluator retain their 9d31e790 bytes. Python/NumPy/SciPy runtime identities and dependency membership remain unchanged; individual dependency hashes and current apparatus identities are packaged.

The pass checks 3,902 pre-existing apparatus/review files against its new before inventory; separately rechecks the prior 792 P artifacts and 1,908 prior apparatus/review/design files. These inventories overlap and are not summed as unique files. All sizes/hashes match. Historical EXP1–21 remains `f1b884a7ada4c806786d1530d76d446aac5d37b1`. Both previous apparatus checkpoints, their packages, earlier P checkpoints, all previous RED evidence and commissioning design records are preserved. The byte-identical 9d31e790 builder ZIP and its independent review ZIP are included as historical archives.

Runtime edits are confined to `authority.py`, `runner.py`, `validators.py`, the two parser uses in `sensor_ui.py`, and new `pending.py`. New targeted tests, exact duplicate fixtures, fault runner and documentation accompany them. Full changes are in `FINAL_CORRECTION.patch`. Prior records require their original apparatus runtime; no historical snapshot is rewritten or silently upgraded.

## Remaining limitations and untested work

Final mechanical closure still requires independent review. No commissioning approval has been created or exercised. Hashes/read receipts establish local workflow integrity, not a cryptographic Jason signature or security against an owner replacing arbitrary interpreter/native code or private internals. Runtime dependency inventory remains process-local. Operator compliance with human procedure text is not inferred by software. Serialized external inputs must use the strict apparatus reader; the apparatus cannot recover duplicate source text already discarded by an unrelated caller's earlier parser.

Invalid restart data must return to an intact verified checkpoint. Only complete paused segments can resume through the supported constructor; snapshots from incomplete/failure/cutoff records are not execution authority. Parent segments must accompany resumed segments for continuity validation, so the portable evidence retains each needed chain. Long-chain storage/performance is unmeasured. Cross-stage holds remain rejected rather than shortened, and no new partial-stage policy is introduced.

Not tested: commissioning A1–A5/B1–B4/C1/C2, 600-second lives, long lifetimes/cohorts, efficacy, useful learning/survival, controller competence, parameter tuning/sweeps, new prehistory, new birth caches, new deprivations, fresh dependency installation, other operating systems, long-run throughput/storage, or a new browser appearance review. No mechanism/world-law change, experiment number, preregistration, push, PR, merge or canonical Workbench update occurred.

The unchanged double-click `developmental_ecology/Open Paused Sensor Reference.cmd` opens a static saved view. It cannot advance a world. Stop for one final mechanical closure review.
