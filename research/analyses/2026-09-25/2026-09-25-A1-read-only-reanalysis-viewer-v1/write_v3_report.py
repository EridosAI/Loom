from evidence import *
r=json.loads((ROOT/'V3_RESULT_v1_1.json').read_bytes());t=json.loads((ROOT/'V3_TEST_RESULTS.json').read_bytes())
text=f'''# V3 read-only reanalysis — version 1.1.0

**{r['status']}**

This is a new analysis of the original first-A1 evidence, not a new trajectory result. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus remains `5f07748102cb5eaa302569c87efbae095050e9fe`; executed authority remains `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`. No simulation, physical replay, controller command calculation, RNG draw or Engine construction was used.

## Custody and exact analysis identity

Input: `FIRST_A1_COMMISSIONING_RESULT.zip`, SHA-256 `{r['evidence_sha256']}`. All 49 outer payload identities and all 65 nested launch payload identities were checked before analysis. `HASH_BEFORE.json` retains the inventory. The original report, checker, AssertionError, V3_BOUNDARY_ERROR.json, V3_POST_CHECK_LIMITATION.md and V3_COUNT_FINDING.json remain unchanged in that archive. The new analysis supersedes only the incomplete V3 conclusion, not any historical file or trajectory observation.

Checker: `v3_checker_v1_1.py`, version `{r['version']}`, SHA-256 `{r['checker_sha256']}`. `evidence.py` is a standard-library-only archive and numeric JSON decoder. Serialized class tags become ordinary dictionaries; production unpack/load_restart functions are not called. Snapshot tuple-of-array raw values are compared as lists of numeric groups, matching the recorder's JSON view conversion; their values and order are unchanged.

## Derived alignment rule

The implementation inspected is the hash-verified packaged `loom_commissioning/runner.py`, `controllers.py`, `diagnostics.py`, `adapter.py` and `loom_p/records.py`. The sensor-reference contract is the packaged design draft §5.1 (29 raw coordinates, held 5 Hz actual E/I, own commands, no privileged fields), with the A1 procedure's separate privileged-control/observer distinction. These are source semantics; no controller was executed during analysis.

1. `SensorHistory.__init__` creates one history row from the initial Engine data. `Run.__init__` writes its complete display envelope to the sensor stream before any command or native step. Entry 0 must have exactly the six display-envelope keys, expected 29 labels, one history row, zero-time/index anchor, initial snapshot raw/E/I, and empty own-command/annotation arrays. The checker validates these contents before treating it as an envelope.
2. After `adapter.step`, `Run.advance` records native data, obtains `diagnostics.passive(before, after, ...)`, observes the new endpoint and writes the last sensor history row. Thus sensor stream entry k (k≥1) maps to native row k−1 and diagnostic row k−1, all with native index k and the same endpoint time. It is not simply “drop the first row.”
3. Diagnostic `input_time` and `raw_step_start` belong to the preceding endpoint (or the initial snapshot for step 1); `endpoint_time` and `raw_endpoint` belong to the current native/sensor endpoint. Every one of these values was checked. An independent index-key join and cumulative native elapsed-time progression support the same unique mapping; duplicate, missing and shifted rows are rejected.
4. Sensor actual E/I start at the initial values, update only at nonterminal native indices divisible by 20, and are held unchanged otherwise. `EI_sample_time` identifies the handoff; it is not the current physical reserve timestamp between handoffs. The final display history equals the explicit initial row plus every mapped endpoint row.
5. A controller decision at native index j uses the recorded state at j and owns native indices j+1 through j+10, shortened by the observed pause. The 919th decision at index 9180 supplied the three recorded steps 9181–9183; seven held steps remain unexecuted. Commands were compared, never recalculated. Recorded realized actuator forces are separate physical quantities, not an additional controller output.

## Results

- 9,184 sensor stream entries = one identified initial display envelope + 9,183 endpoint rows.
- All 9,183 native/sensor/diagnostic mappings, start/endpoint raw comparisons and E/I holds agree; 459 body handoff samples.
- All 919 controller inputs obey the exact closed privileged schema, including nested geometry/contact keys. Recorded pose, velocity, reserves, prior commands, stocks, time and phase match the corresponding decision boundary. All 9,183 delivered commands match their recorded issued decision. No neural object is supplied in these input records. This A1 used privileged control; the separate sensor display is an observer record, not a sensory-only human trial.
- The final display's own-command list, history, annotations and snapshot payload agree. Final body/raw/stocks/reserves, update counters, pending decision and packed-engine hash agree with the receipt and final native record.
- Complete inactive organism state and complete RNG state agree at all 11 saved checkpoints; all 9,183 native RNG counters agree. The organism hash is `{r['inactive_organism_sha256']}`. Neural wave rows: zero.
- {t['passed']} copied-record tests passed. Negative controls reject missing/wrong envelopes, swapped/duplicate/shifted rows, start/endpoint confusion, raw drift, premature/missed E/I release, elapsed-time mismatch, privileged/neural leakage, command/start-state substitution, RNG-counter change and an injected neural wave record. Tests never write to the original records.

`V3_RESULT_v1_1.json` retains every aligned index/start/endpoint/sample-time mapping. `V3_TEST_RESULTS.json` retains test identities and rejection messages.

## Limits

This closes the intended record-level V3 comparisons. It does not prove arbitrary unlogged transient memory states: complete neural/RNG state is available at 11 checkpoints, while RNG counters are available at every native endpoint. No physical replay, new instrumentation, scientific claim, learning trace, efficacy tuning or new commissioning execution was performed. The historical 91.83-second administrative pause and its unobserved 28.17-second remainder remain unchanged.

## Reproduction

Use Python 3.13 (standard library only) in this derived folder. The portable package includes the exact original archive under `references/`; no executable grant is relocated or activated.

```powershell
python -B v3_checker_v1_1.py --evidence references/FIRST_A1_COMMISSIONING_RESULT.zip --output V3_REPRODUCED.json
python -B test_v3_v1_1.py
```

The default archive lookup also supports the original sibling delivery. Tests use the same immutable evidence and detached copies. Reproduction writes only new derived analysis outputs.
'''
(ROOT/'V3_READ_ONLY_REANALYSIS_REPORT.md').write_text(text,encoding='utf-8')
print(r['status'])
