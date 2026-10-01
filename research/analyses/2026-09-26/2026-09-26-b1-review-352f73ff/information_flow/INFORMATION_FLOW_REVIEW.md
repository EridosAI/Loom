# B1 operator information-flow review

Checkpoint `352f73fffa6d9781eae8aa38e708a9a05669588f`, compared with `68db2c581f07200966d699a4f55a65f9b96df1e9`. No material defect was exposed in this bounded information-flow review. The evidence supports the display-only chemistry intervention and preservation of the full raw record. It does not independently establish the complete lifecycle disposition or authorize B1 execution.

## Scope and source identity

Read the current request, correction report, chemistry information-flow map, lifecycle description, relevant production changes, `test_b1_operator.py`, and `b1_dom_fixture.cjs`. Only the delivered generic manufactured component and invented canary data were executed. No held B1 case, prepared positive control, sealed geometry, evaluator result, or launch authority was opened or executed. Target source, Git, earlier exports, and Workbench were not modified. All new evidence is under this directory.

`SOURCE_FLOW.json` verifies exact committed bytes for eleven relevant source/test files. The diff from the parent is empty for `loom_p`, `configuration.json`, `adapter.py`, `clock.py`, `evaluation.py`, and `diagnostics.py`. AST comparisons also confirm unchanged `SensorHistory`, `command_pair`, `waypoint_command`, `waypoint_stage`, `time_due`, and `privileged_input`. This is preservation evidence for the reviewed change, not a fresh general audit of those components.

## Projection and physical fidelity

References below are relative to `developmental_ecology/loom_commissioning` in the pinned target.

`operator_view.py:7` excludes exactly raw indices 10–13. Lines 26–34 validate the complete source, copy it, and select the remaining coordinates in every history row. Hidden data use schema 2 and 25 labels; FULL-RAW retains schema 1 and 29 labels. Lines 16–24 reject inconsistent intervention identities and payload schemas. There is no numeric chemistry replacement or chemistry-derived summary.

The unchanged physical `SensorHistory` remains at `controllers.py:129`; the common closed-schema validator at lines 105–127 enforces row fields, dimensions, finite values, history ordering, and actual E/I availability. `runner.py:125` records the full initial sensor history, while `runner.py:249` projects only the operator view; line 276 saves that view. `validators.py:97–105` distinguish operator payloads from full raw streams, and lines 135–136 compare replayed full data and their projected history separately.

The independent `check_operator_egress.py` used the delivered two-condition generic 0.2-second fixture, with actual loopback HTTP start/command requests and command pairs `(0.13, 0.07)` and `(-0.1, 0.04)`. Both conditions completed 20 native steps and retained 21 raw rows of width 29, with nonzero real chemistry in every row. Every exposed value equalled its corresponding complete raw coordinate; hidden rows contained exactly the selected 25 coordinates. Operator histories had lengths 1, 1, 11, and 21 across prepared/start/two command responses. Recorded human inputs exactly matched the preceding HTTP operator payloads. Saved operator histories matched HTTP and offline-display histories.

Both replay validators passed. Final physical state and complete native, event, wave, and raw sensor streams were identical across conditions. Final physical hash: `d65a1e46413a4eba0df55bcfa512056a6c0b9d94c33261004a49eda6bcb1d14d`. The wave stream is empty in this short fixture; unchanged wave implementation is separately covered by the source comparison. Evidence: `generic-fixtures-evl0r32q/RESULT.json`, both `*-HTTP.json` files, and retained component records.

## Operator-facing boundary

| Surface | Source boundary and independent evidence |
|---|---|
| Current values, complete history, API responses | `sensor_ui.py:18–26` validates the closed envelope; lines 155–184 validate before serialization. Actual HTTP returned exactly 25/29 channels in the paired fixture. Invented chemistry canary was absent from `/`, `/sensors`, and `/session`. |
| DOM, labels, attributes, plots and statistics | `sensor.html:23–33` validates condition/schema/dimensions before `accept` at line 66. Lines 50–60 build channels, text, and plot ranges only from permitted rows and labels; chemistry-unavailable text is nonnumeric. Actual production JavaScript was exercised in the delivered detached DOM harness. |
| Downloads and saved display | `sensor.html:94` exports only `session.sensors`; the generic filename discloses no case path. Paired fixture saved display equals HTTP. Detached DOM evidence confirms hidden export has 25 values and FULL-RAW has 29. |
| Errors and logs | `sensor_ui.py:16` supplies a fixed generic error; lines 30 and 149 suppress handler/access diagnostics. An invented private exception containing the canary returned exactly the generic 400 body. Captured server stdout/stderr were empty. |
| Debug, evaluator, state, filesystem and socket routes | GET/POST dispatch is an explicit small allowlist (`sensor_ui.py:155–184`); no evaluator, WebSocket, debug, or arbitrary-file handler exists. Nine representative denied paths returned 404 and exactly `Unavailable`, including `/evaluation`, `/state`, `/debug`, `/socket`, and `/../configuration.json`. The private recording directory is not a web root. |
| Extra hidden data or summaries | Independent HTTP injections of a chemistry coordinate and an extra chemistry-mean envelope key both produced generic 400 responses. The projection left its full source object unchanged. |

These checks cover the declared operator interface, not secrecy against an owner with direct filesystem or interpreter access. Permitted physical channels retain their lawful correlations; no claim of statistical independence from chemistry is made.

## Consequential falsifier and evidence limits

The delivered C fault bypasses the actual HTML JavaScript envelope validator in memory. Direct C RED exited 1 at `CSS-ONLY MASK EXPORTED CHEMISTRY`; restored GREEN exited 0. The original RED stops at the export assertion, so its later DOM assertion is not reached. Independent observation inserted immediately before that first assertion recorded both an exported canary and rendered numeric chemistry, with controls enabled. Restored code rejected the invalid hidden response before either exposure and kept controls disabled. Valid hidden and full responses then showed the expected 25/29 dimensions and canary absence/presence. See `DOM-C-*.log` and `OBSERVED-DOM-C-*.log`.

This is execution of production JavaScript with detached DOM/transport stubs, not a full browser appearance audit. Delivered B, D, and L faults mutate/select detached fixture inputs; they establish their respective invariants but are not production pipeline patches. The separate paired HTTP/physical reproduction above establishes the actual connected data path. The root reviewer owns the complete A–L matrix and full-suite results; they are not re-counted as independent executions here.

All bounded independent checks described above passed. No information-flow HOLD item was identified within the authorized scope.
