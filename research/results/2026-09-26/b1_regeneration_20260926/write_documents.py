"""Operator-safe document authoring only; standard-library file operations."""
import json,pathlib
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
E=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
OLD=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02/B1_OPERATOR_REVIEW'
index=json.loads((PUB/'CASE_AND_AUTHORITY_INDEX.json').read_bytes());rows=index['cases']
resources=json.loads((PUB/'RESOURCE_PROJECTION.json').read_bytes())
def put(name,text): (PUB/name).write_text(text.strip()+'\n',encoding='utf-8',newline='\n')
instructions=(OLD/'OPERATOR_INSTRUCTIONS.md').read_text(encoding='utf-8')
replacements={
 '# Operator instructions — review only; do not launch':'# Operator instructions — prepared, awaiting separate case authorization',
 'The packet is on HOLD. The current inert sensor launcher opens saved records only and is not a live-trial launcher.':'This packet has been regenerated against the corrected operator apparatus. No case is authorized or started. The next decision is authorization of the four positive controls only; B1 needs separate later authorization. The prior positive-control disclosure is retained only for those controls, as Jason clarified.',
 'After a separately reviewed live apparatus and exact packet are authorized, the intended interaction is:':'Only after Jason authorizes the exact case, the interaction is as follows. A newly prepared case starts in PREPARED / NOT STARTED. Explicit Start changes it to PAUSED without advancing the world:',
 'These steps describe the required reviewed behavior, not a claim that the present page meets its live lifecycle requirements. In particular, its current label stays “paused” during a request and it leaves the button enabled. That is a HOLD finding, not an instruction to work around it.':'The corrected page shows PREPARED, PAUSED, RUNNING and ENDED. It disables command controls before sending and accepts one current decision token only. A delayed or duplicate request cannot become a second hold. Refresh/reconnect reads permitted history without advancement. During RUNNING the displayed sensor history is the last complete history. An uncertain response locks action controls: inspect the permitted state by explicit refresh, never automatically resubmit. Closing a paused page does not advance the body. A command already accepted remains bounded even if the connection is lost. ENDED is irreversible: do not resume, retry, replace or extend the case. Private stop details remain evaluator-only.',
 'In FULL-RAW, all 29 native coordinates are real. In CHEMISTRY-HIDDEN, the four chemistry coordinates and their entire history must be withheld at the display boundary. They must be marked hidden rather than shown as real zeros. The physical field, actual sensors and the remaining 25 coordinates stay unchanged. The current checkpoint does not implement this condition.':'In FULL-RAW, all 29 native coordinates are real. In CHEMISTRY-HIDDEN, all four chemistry coordinates are omitted from the current and every historical operator row, leaving 25 actual coordinates. The page states CHEMISTRY UNAVAILABLE IN THIS CONDITION. There are no zero/null numeric substitutes. The physical field, real chemistry transduction and complete private 29-coordinate record remain intact. All other permitted channels, E/I cadence, paired actuators and 0.1-second holds are unchanged.'
}
for a,b in replacements.items():assert instructions.count(a)==1;instructions=instructions.replace(a,b)
put('OPERATOR_INSTRUCTIONS.md',instructions)

pc_table='\n'.join(f"| {i} | {r['case']} | {r['duration_seconds']} s | `{r['canonical_authority_sha256']}` |" for i,r in enumerate(rows[:4],1))
put('POSITIVE_CONTROL_AUTHORIZATION.md',f'''
# Positive controls: the next authorization decision only

All four are NOT EXECUTED / NOT DEMONSTRATED. No grant or live session exists. Jason may authorize the following four independent canonical authority objects, explicitly and in this order. Each covers one attempt at its exact preserved fixture, duration, interface and resource limits. It does not authorize another case.

| Order | Case | Ceiling | Canonical case authority SHA-256 |
|---:|---|---:|---|
{pc_table}

These hashes identify the complete canonical execution objects retained in sealed evaluator custody. They are not hashes of summaries and are not the historical held review identity. `PC_AUTHORITY_IDENTITIES.json` provides the opaque initial-state/snapshot bindings and exact current case identities. The authority objects are prepared specifications; the actual manifests still have `execution_authority: null`. No approval record has been manufactured.

The four disclosed cards assess directional sensory reading, command versus achieved movement, contact onset and gentle contact hold. Their criteria are unchanged and do not use B1 outcomes. Review the actual operator explanation, displayed record and evaluator observation after each control. Preserve a miss, damage or administrative stop. One attempt each; no automatic retry, extension, substitution or policy assistance.

**Authorizing these four objects authorizes no B1 trial.** Successful controls do not automatically authorize or launch B1. After the controls, stop for their recorded gate review and a separate B1 decision. The two B1 authority identities are listed separately as sealed, unexecuted cases.
''')

put('README.md',f'''
# B1 perceptual ceiling — regenerated, unexecuted

**Next decision: Jason's authorization of the four positive controls only. No execution is authorized by this packet.**

P: `{index['P']}`  
Corrected operator apparatus: `{index['apparatus']}`  
Historical held review identity: `{index['historical_held_review_identity']}` — preserved, not reused.

Jason supplied the independent disposition **FIT FOR B1 LAUNCH-PACKET REGENERATION** and authorized this static regeneration. This packet does not claim a new independent review or a demonstrated human result. The older workbench HOLD entry remains historical; this task does not edit canon or shared navigation.

Read [the positive-control authorization sheet](POSITIVE_CONTROL_AUTHORIZATION.md), [operator instructions](OPERATOR_INSTRUCTIONS.md), [unchanged practice cards](POSITIVE_CONTROL_CARDS.md), [semantic diff](SEMANTIC_DIFF.md), [resource plan](RESOURCE_PLAN.md) and [static report](STATIC_COMPATIBILITY_REPORT.md). All controls remain NOT DEMONSTRATED / NOT EXECUTED.

The fixed order is PC-LR (4 s), PC-MOTION (4 s), PC-CONTACT (6 s), PC-HOLD (10 s). Each has a new separate exact authority. Existing practice geometry is disclosed for those controls only, following Jason's clarification. No positive-control authorization includes either B1 case.

The separately sealed B1-FULL-RAW and B1-CHEMISTRY-HIDDEN cases each retain a 30-second ceiling and the exact same complete physical starting state. FULL-RAW supplies 29 actual coordinates; CHEMISTRY-HIDDEN supplies 25, with an explicit unavailable label and full actual chemistry privately recorded. B1 remains unexecuted and needs separate later authorization plus the preserved control/integrity gates. No evaluator result from FULL-RAW may inform the second trial before both end or the pair is explicitly abandoned.

This operator bundle contains opaque state/snapshot hashes, not B1 pose, hidden geometry, source identity/stock/position, mover truth, initial readings or evaluator records. The separately sealed evaluator archive is not linked here and must remain closed to Jason while he is the blinded operator. This is workflow separation, not an OS security barrier against the machine owner.

Static checks invoked no world construction, snapshot deserialization, transduction, controller command, simulation step, prehistory, test suite, replay or live service. See `ZERO_EXECUTION_RECORD.json`. Source code/configuration and the old held packet remain unchanged. Six pure execution specifications were accepted; all six null grants were rejected. New authority objects identify scope for a future decision and confer no permission by themselves.

`CASE_AND_AUTHORITY_INDEX.json` holds all six opaque identity records. `PC_AUTHORITY_IDENTITIES.json` and `B1_SEALED_AUTHORITY_IDENTITIES.json` keep authorization scopes separate. `PACKET_CUSTODY_IDENTITY.json` and `FILE_MANIFEST.json` identify this document delivery; their hashes are custody identities, never a combined execution authority. Stop for positive-control authorization only.
''')

put('APPARATUS_DISPOSITION.md',f'''
# Apparatus disposition and provenance

Jason's current instruction names `{index['apparatus']}` and supplies the independent disposition **FIT FOR B1 LAUNCH-PACKET REGENERATION**. That is the decision basis used here. The implementation checkpoint and clean local worktree were verified. No independent review or engineering regression was rerun in this task.

The historical `OPEN_ISSUE_B1_INTERFACE.md` described absent chemistry masking and a misleading/queued live lifecycle at 68db. It remains unchanged in the historical held packet. The selected correction implements omission at the server projection boundary, typed authority binding, explicit lifecycle, single-use decisions and irreversible end. This regeneration updates its exact source/runtime/interface identities and representation; it does not change physical chemistry, P, body/world laws, actuation or the prepared design.

The history-growth resource concern remains: full permitted histories are copied into human decision records and validated. Resource estimates retain conservative bounds and add the new lifecycle audit stream. This is not a measured interactive benchmark. Human competence and both B1 outcomes remain untested.

Jason also clarified the disclosure question with **“Retain existing positive-control disclosure only.”** The four practice cards therefore remain byte-identical. No practice disclosure is permission to expose the held-out B1 state or either evaluator record.

No execution was authorized. Subsequent positive-control authorization must name their four independent objects; B1 authorization remains a separate decision after the preserved gates.
''')

resource_rows='\n'.join(f"| {r['case']} | {r['seconds']} | {r['holds']} | {r['A5_compute_proxy_seconds']/60:.2f} | {r['operator_lifecycle_audit_planning_bytes']:,} | {r['stream_planning_bound_bytes']/1e6:.3f} |" for r in resources['cases'])
pc=resources['pc_only_totals']
put('RESOURCE_PLAN.md',f'''
# Resource projection — unchanged ceilings, no execution permission

The measured basis remains the completed A5 record: 7,714.9715165 recorder wall seconds for 630 nominal simulated seconds, or 12.2459865 wall seconds per simulated second. A5 stored 448,657,204 trajectory bytes and 376,284,429 uncompressed stream bytes. Its privileged waypoint inputs differ from human histories; this is a physical-compute/recording proxy, not measured interactive throughput. No benchmark was executed.

| Case | Simulated ceiling (s) | Maximum decisions | A5 compute proxy (min) | Added lifecycle audit allowance (bytes) | Revised stream planning bound (MB) |
|---|---:|---:|---:|---:|---:|
{resource_rows}

The **positive controls alone** total 24 simulated seconds, 2,400 native steps and at most 240 decisions. Their A5 base-compute proxy is {pc['A5_compute_proxy_seconds']/60:.2f} minutes. At 5 / 10 / 20 wall seconds of human deliberation per decision, illustrative total times are 24.9 / 44.9 / 84.9 minutes, before unmeasured interactive overhead.

The sealed pair adds 60 simulated seconds and at most 600 decisions, only if separately authorized later. All six ceilings total 84 simulated seconds / 8,400 native steps / 840 decisions. The preserved A5 base proxy is 17.14 minutes; 5 / 10 / 20 seconds of deliberation per decision give 87.1 / 157.1 / 297.1 minutes before unmeasured interactive work. These are arithmetic illustrations, not forecasts or resource extensions.

The held history bound is preserved: for N holds from time zero, controller inputs repeat `N + 5*N*(N-1)` native rows. A 30-second case repeats 448,800 rows. The original allowances remain 1,200 bytes per raw row, 128 per prior command, 6,200 per prior 1,000-character note including escaping, 10,000 per decision for metadata/current note, plus A5's physical-stream proxy. No storage saving is credited for omission of four chemistry values; private physical chemistry remains complete.

The sole necessary estimate increment is the corrected private lifecycle stream: at most `2*N + 3` normal lifecycle rows, budgeted at 1,024 uncompressed bytes each. This covers preparation/start, accepted-command and completed-pause transitions, and end. Existing snapshot/display allowances remain 50 MB per control and 150 MB per B1 case. Extraordinary failure tails remain covered by the existing flush reserve; this is a planning envelope, not a promise that failure cannot exhaust storage.

**All hard limits are unchanged:** 256 MB uncompressed streams and 1,200 wall seconds per control; 1.5 GB and 7,200 wall seconds per B1 case. Deliberation advances no simulated bodily time, but the administrative wall timer continues. No automatic extension, continuation or retry follows a resource stop. Reporting allowance remains one hour, saved evidence only.

The combined-new-artifact cap remains 12 GB, with a stop request at 11 GB and 1 GB reserved for final flush/receipt. Require 12 GB free before any future launch; count all disjoint output directories and retained copies. At most four equivalent retentions remain budgeted. The revised conservative combined primary-copy estimate is **{resources['combined_primary_copy_planning_bytes']:,} bytes ({resources['combined_primary_copy_planning_bytes']/1e9:.6f} GB)**. No horizon or native recording fidelity was reduced.

Corrected projection, validation, history hashing, polling, HTTP serialization and browser rendering add unmeasured cost. Read-only polling creates no physical steps and no trajectory stream by itself. Actual disk or wall limits can still end a case early. No performance guarantee, human policy, useful-learning gate or B1 outcome criterion is introduced.
''')

put('SEMANTIC_DIFF.md',f'''
# Semantic comparison with the preserved held packet

Compared to historical held identity `{index['historical_held_review_identity']}`, all six complete initial-state identities, five snapshot byte sequences, case names, 4/4/6/10/30/30-second ceilings, physical laws, cadence, command semantics, resource hard limits, human actions, admission/completion rules, gate and interpretation are preserved. No candidate fixture, phase, route or outcome was tried or selected.

`SEMANTIC_DIFF.json` enumerates changed manifest and contract paths without exposing values from private physical fields. `DOCUMENT_CHANGE_CLASSIFICATION.json` covers document replacements/additions as well as unchanged controlling documents. **UNEXPECTED SEMANTIC CHANGE: none.** An unlisted manifest field change causes preparation to stop.

| Classification | Changes and grounds |
|---|---|
| IDENTITY-ONLY / REQUIRED BY APPARATUS CORRECTION | Exact apparatus/controller/runtime/interface identities, hashes of corrected display/recording contracts, newly canonicalized independent case objects, hashes/indexes/custody records, and static validation/provenance status. Actual unchanged runtime values are retained rather than fabricated. |
| IDENTITY-ONLY / REQUIRED BY APPARATUS CORRECTION | The rejected chemistry proposal becomes the implemented typed omission identity, including its exact implementation hash; full-raw remains `none`. This realizes the previously selected display condition, with no physical/raw chemistry change. |
| OPERATOR-LIFECYCLE REPRESENTATION CHANGE REQUIRED BY CORRECTION | Document and explain PREPARED → PAUSED → RUNNING → PAUSED/ENDED; explicit Start, consumed decision token, in-flight controls, generic errors and irreversible end. These realize the held pause/hold/no-resume contract without changing it. |
| IDENTITY-ONLY / REQUIRED BY APPARATUS CORRECTION | Resource planning adds only the new audit-record allowance, retaining all ceilings, caps, history fidelity and actual A5 basis. No new benchmark or cap adjustment. |
| UNEXPECTED SEMANTIC CHANGE | Zero. No law, P/configuration, fixture, initial state, phase, body mechanics, command policy, interpretation, order or success criterion changed. |

The five controlling public files `POSITIVE_CONTROL_CARDS.md`, `OPERATOR_INTEGRITY_FORM.md`, `INTERPRETATION_TABLE.md`, `CONTROL_GATE.json` and `PROTOCOL_CONTRACT.json` are byte-identical. The positive-control geometry disclosure is retained only under Jason's clarification, never generalized to B1. The protocol's original admission text continues to say the packet is held until genuine authorization and gates; the corrected source and regenerated objects now fulfill its technical prerequisites, not its ungranted execution permission.

The operator instruction rewrite updates only obsolete apparatus status, implemented omission and lifecycle guidance. Sensor meanings, plots/precision guidance, actuator ranges, holds, human task, fixed order/carryover, blind integrity rules and interpretation remain. Historical preparation reports and the rejected candidate remain preserved under their old identity; they are not relabeled as executable objects.

Full and hidden current manifests differ only in case identity and the typed operator display intervention. Initial-state, snapshot, field/prehistory identities and every physical/timing field match. The same starting state does not imply matched future trajectories after different human commands, nor a chemistry-necessity inference. Those limitations remain unchanged.
''')

put('STATIC_COMPATIBILITY_REPORT.md','''
# Static compatibility — six cases representable, none executed

All six new execution specifications pass the corrected apparatus's pure identity/procedure/display validation. Integer clock arithmetic represents their unchanged native ceilings and ten-step command holds. All six null execution grants are rejected. The checks do not construct a Run, issue a human command, open a service or deserialize a snapshot.

The original five snapshot files are copied byte for byte. Both B1 manifests bind the same complete state hash and shared snapshot hash; only case name and operator display intervention differ. Their 30-second ceilings remain identical. This is custody equivalence to the previously prepared complete states, not a new physical-state round trip or a new initial sensor calculation.

PC-LR retains directional sensory reading; PC-MOTION retains command versus actual motion; PC-CONTACT retains onset detection; PC-HOLD retains the disclosed gentle-support criterion. All four fixtures/cards/criteria are unchanged, and all remain NOT DEMONSTRATED / NOT EXECUTED. No B1 outcome defines a control pass.

The exact P/configuration files and the corrected clock are unchanged. FULL-RAW binds schema 1 with 29 actual coordinates. CHEMISTRY-HIDDEN binds the implemented schema-2 omission with 25 actual coordinates and the explicit unavailable label. Physical raw chemistry is retained privately. The UI/runner/projection source identities are part of the exact authority and also recorded for review.

The file-level and canonical audits confirm the new objects are distinct from all old case digests and from the held review identity; the six new identities are distinct from one another. There is no combined launch authority, no grant, no approval record and no automatic transition from positive controls to B1.

This regeneration does not repeat the independent engineering review, component suite, physical snapshot validation, live browser review or human demonstration. The independent disposition is supplied by Jason. Source identities and static checks establish that the prepared cases are represented by the specified corrected apparatus; they do not establish perceptual success or authorize execution.
''')

put('REVIEW_AND_AUTHORITY_BOUNDARY.md','''
# Review and authority boundary

Every manifest still has `execution_authority: null`. Six new independent authority objects are canonical execution objects: every manifest field except the null/self-referential grant, encoded as sorted-key compact UTF-8 JSON with finite values. Their SHA-256 values are the case authority identities to quote. No signed/approved request or grant was created, and no runtime authorization was accepted.

Exact objects and manifests remain in sealed evaluator custody because they carry phase, initialization and other privileged bindings. Public indexes expose only the case name, scope, ceiling and opaque digests. The operator need not inspect private contents to approve an exact object by its digest. No private archive or evaluator viewer is linked from the operator packet.

The next requested authorization is PC-LR, PC-MOTION, PC-CONTACT and PC-HOLD only, individually identified and in that order. Their execution, if later authorized, would still be manually driven by Jason through the corrected interface. One attempt each; no retry, extension, substitution, gain change or assistance from hidden state. A positive-control grant cannot match either B1 execution digest.

Both B1 trials remain sealed, unexecuted and separately unauthorized. The preserved positive-control and exposure gates, separate Jason authorization, and fixed FULL-RAW-then-hidden order apply. No result feedback from the first B1 trial is released before both trials end or the pair is explicitly abandoned. Misses, costs, damage, limitations and early stops are preserved under the existing interpretation.

The packet custody identity binds delivered documents and opaque archive/case identities; it is NOT a seventh case, a batch launch object or execution permission. The historical held hash remains an immutable historical custody identity, never reused as an authority for this apparatus.

This task stops for Jason's authorization of the positive controls only. No pre-authorized B1 step, trial, service or command is waiting in the background.
''')

put('SESSION_RECORD.md',f'''
# Regeneration session record — 2026-09-26

Jason authorized static regeneration after supplying independent disposition FIT FOR B1 LAUNCH-PACKET REGENERATION for apparatus `{index['apparatus']}`. The historical prepared design under `{index['historical_held_review_identity']}` controls fixture/interpretation preservation. Jason clarified: “Retain existing positive-control disclosure only.” The new packet preserves those cards byte for byte and keeps B1 truth sealed.

Read current project instructions/orientation, workbench status, held operator contracts, opaque/sealed manifests as inert data, corrected authority/contract/clock/interface identities and prior correction preservation evidence. Current workbench navigation still contains the dated B1 apparatus HOLD. The later supplied disposition controls this regeneration; no shared map, canon, source archive or instruction file was edited.

Actual Windows local Git and Python identities were checked. The corrected worktree is clean and exact; a harmless preparation-directory read/write probe passed. File-only generation and pure schema/clock arithmetic created six new independent authority objects. No code, configuration, initial snapshot, resource hard limit, case horizon or physical parameter was changed.

One initial static allowlist stop occurred at a Python Recorder class-definition body, before any constructor or state operation. Inspection identified it as method definition only; the guard was made precise and static preparation repeated. This was not a fixture/controller retry. `STATIC_PREPARATION_NOTE.json` preserves that distinction. No private scalar was printed.

The prepared case objects contain no grants. Static null-grant checks reject all six. Zero simulation/controller execution, snapshot deserialization, transduction, prehistory, replay, component test or live service occurred. Call-inventory and custody audits are included. No P learning/perception/survival or human competence claim follows. Stop at the positive-control authorization boundary.
''')

(PRIV/'README.md').write_text('''# SEALED EVALUATOR CUSTODY — do not open to the B1 operator

Current manifests and independent canonical authority objects are under `case-manifests` and `authority-objects`. All grants are null. The five exact preserved initial snapshots are under `initial-states`; the B1 pair references the same one. Prepared fixtures/evaluator design remain unchanged under `preserved-design`. The original sealed archive is retained byte-identically under `historical-held` and retains its old, non-launchable provenance; do not mistake its historical objects for current ones.

The current source/runtime identities bind corrected apparatus 352f73fffa6d9781eae8aa38e708a9a05669588f. New public documents bind its implemented omission/lifecycle contract. No launch is authorized, no approval record or execution batch is supplied, and no simulation occurred. PC authorization cannot authorize B1. Keep both B1 evaluator views closed to Jason through the pair or explicit abandonment.
''',encoding='utf-8')
(PRIV/'DOCUMENT_AUTHORING_SOURCE.py').write_bytes(pathlib.Path(__file__).read_bytes())
print('Operator documents written; existing practice disclosure retained; B1 hidden contents not used in public authoring.')
