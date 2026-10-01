"""Operator-safe documents; no held-out B1 scalar is received or printed."""
import pathlib

def put(p,s):
    with pathlib.Path(p).open('x',encoding='utf-8',newline='\n') as f:f.write(s.strip()+'\n')

def documents(pub,private,cases,resources,locations):
    put(pub/'README.md',r'''
# First B1 perceptual-ceiling packet — PREPARED / HOLD

**Do not execute. No execution grant or live launcher is supplied.**

Prepared scope: four disclosed operator positive controls, one 30-second B1 FULL-RAW trial, and one 30-second B1 CHEMISTRY-HIDDEN trial from the same complete initial state. The four control ceilings are 4, 4, 6 and 10 seconds. These are proposals for review; every operator/result status is NOT DEMONSTRATED / NOT EXECUTED.

Read `OPERATOR_INSTRUCTIONS.md`, `POSITIVE_CONTROL_CARDS.md`, `RESOURCE_PLAN.md`, `INTERPRETATION_TABLE.md` and `OPEN_ISSUE_B1_INTERFACE.md`. `CASE_AND_AUTHORITY_INDEX.json` binds opaque state and case hashes without revealing the B1 test state. `HELD_REVIEW_IDENTITY.json` identifies this held preparation; its hash is **not launch authority**.

P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The pinned apparatus is `68db2c581f07200966d699a4f55a65f9b96df1e9`.

The exact checkpoint explicitly rejects chemistry deprivation. Its reviewed full-raw boundary is retained, but the present live page lacks an honest in-flight/ended indication and protection against repeated queued submissions. A later narrow apparatus decision and independent review are required. This packet does not implement a replacement interface, mask, controller or command cadence.

The evaluator-only archive contains complete snapshots, raw initial B1 readings, world state, exact case manifests and candidate authority objects. **Jason must not inspect it before both trials end if he is the sensor-only operator.** These files are separated for custody; this is not an OS security boundary against the machine owner. No hidden B1 state appears in this operator bundle. General source-state subtleties and body/sensor laws may be known.

Preparation made five zero-time copies of an existing lawful snapshot and calculated each initial raw tuple once. It performed no native step, field update, new prehistory, controller command, human trial, RNG draw or simulation Run construction. Nothing here is a P learning/perception result.
''')
    put(pub/'OPERATOR_INSTRUCTIONS.md',r'''
# Operator instructions — review only; do not launch

This task asks whether a person can use the body's permitted information. You are the external human reference. P is inactive. Your trial objective is to use the raw history and paired actuator controls to attempt an interaction with an energy source. An incomplete or unsuccessful attempt remains informative about this operator/controller attempt; it does not establish that the information is absent.

The packet is on HOLD. The current inert sensor launcher opens saved records only and is not a live-trial launcher. Do not use the world inspector, privileged review, a prior trajectory, developer console, source files, or evaluator archive to discover the B1 start. Do not ask an assistant to choose commands from hidden state. No source identifier, target marker, direction arrow, distance, stock, material label, gain notification or semantic hint belongs on the live display.

After a separately reviewed live apparatus and exact packet are authorized, the intended interaction is:

1. Read the current raw values and the state indicator. While paused, inspect history and deliberate freely: this must consume no bodily time, field step, energy, or RNG. The separate administrative wall clock continues.
2. Enter one left/right pair, each between −1 and +1. These are commands, not guaranteed forces, velocities or distances. Click once. One decision holds that pair for ten 0.01-second native steps: 0.1 bodily seconds, unless an earlier stop occurs. No autoplay, batching, repeat button, cadence change, or queued second request is permitted.
3. Wait for that hold to finish and the paused indicator to return. The latest row now reflects the achieved response. A zero pair still advances the world for one hold and costs bodily time/energy; it is not the pause operation.
4. Move the history slider to study earlier native rows. The chart displays up to the last 1,000 rows before the selected endpoint; the complete ordered history must remain available. Actuation always concerns the current state, never the selected historical row. Return to the latest endpoint before entering another command.
5. Use your own notes. The existing text limit is 1,000 characters per submitted annotation. Keep external private notes during deliberation if useful, then retain them with their wall/time context; no external note may contain privileged feedback. The permitted export must contain only the channels allowed in the current display condition.
6. At the fixed ceiling or another stop, do not retry or resume. Preserve the transcript, displayed histories and stop receipt. In an error, stop requesting commands and report it; no alternate route, phase, start or controller is silently substituted.

These steps describe the required reviewed behavior, not a claim that the present page meets its live lifecycle requirements. In particular, its current label stays “paused” during a request and it leaves the button enabled. That is a HOLD finding, not an instruction to work around it.

## Reading the coordinates

The coordinate labels identify anatomy, not external objects. No light or chemistry value is a direct source label.

| Display group | Meaning allowed from the general laws |
|---|---|
| `light_0` … `light_9` | Two bands at each of five visual sectors. Pair order is right to left, at body-relative −48°, −24°, 0°, +24°, +48°. Values combine actual surface response, light, occlusion and attenuation. |
| `chemistry_0`, `chemistry_1` | Two mixed chemical receptor coordinates at the body-right/front site (−45°). |
| `chemistry_2`, `chemistry_3` | Corresponding coordinates at the body-left/front site (+45°). Compare like indices across sites; this is your inference, not an analytic gradient supplied by the display. |
| `contact_0` … `contact_7` | Eight body-relative sectors starting at forward, increasing toward the left in 45° increments. Contacts distribute across neighboring sectors. The bounded values transform recent impulse per native time; a transient impact spike is not itself a stable contact force. |
| `proprioception_0`, `_1` | The body's current left/right command values. |
| `proprioception_2`, `_3`, `_4` | Bounded forward, lateral and angular motion readings. These report achieved motion; they are not global pose. |
| `proprioception_5`, `_6` | Bounded discrepancies between each command and its corresponding body-motion combination. |
| Actual E / I | Separate real bodily reserves, released only at the existing 5 Hz handoff and held between samples. Read the sample timestamp. They are not updated every native sensor row. |

The current table formats raw values to seven significant digits, E/I to six decimals, and the selected time to three decimals. Exact delivered numeric values must also remain in the operator-view record; rendering precision is not measurement precision. The charts use a shared automatic vertical range within each modality panel. Do not compare apparent plot heights across different panels as though their scales were identical.

## Fixed sequence and the gate

First complete the four disclosed cards: left/right reading, command versus motion, contact onset, then gentle hold. They check operator/interface use, not ecological success. Save your descriptions and the actual command transcript. All four must be documented as demonstrated before B1 can be interpreted. No completion launches B1 automatically. If any is not demonstrated, B1 remains unexecuted/uninterpretable pending a separate decision.

Then, only under a later genuine grant and passed integrity gate, use the fixed order **FULL-RAW first; CHEMISTRY-HIDDEN second**. Each trial has a 30-second ceiling. The pair starts from the same complete physical state, restored only between separate trials. You retain ordinary human memory of the first trial; this is an explicit carryover limitation for the chemistry-hidden comparison. No privileged evaluation of the first trial is shown before the second ends or is explicitly abandoned.

In FULL-RAW, all 29 native coordinates are real. In CHEMISTRY-HIDDEN, the four chemistry coordinates and their entire history must be withheld at the display boundary. They must be marked hidden rather than shown as real zeros. The physical field, actual sensors and the remaining 25 coordinates stay unchanged. The current checkpoint does not implement this condition.

Before starting, complete `OPERATOR_INTEGRITY_FORM.md`. General knowledge of sensor/body laws is allowed. Any prior or accidental knowledge of this fixture's hidden state must be declared. Do not silently replace the case to repair exposure.

## What can be concluded

A successful held-out interaction is a positive information-availability witness for this human and case. A miss is not proof of absence. Source appearance does not directly announce stock. Chemistry depends on stock and also transport, history, position and occlusion. Depleted sources remain chemically present; there is no EMPTY flag. There is no required percentage, recognizer accuracy, P success/failure, or learning-efficacy score.
''')
    put(pub/'POSITIVE_CONTROL_CARDS.md',r'''
# Four disclosed operator controls — all NOT DEMONSTRATED / NOT EXECUTED

Each is an independent predetermined manufactured zero-time fixture in the existing world, with unchanged laws and an ordinary paired-actuator interface. The fixtures are not ecological evidence or sampled newborn lives. They are shown/described openly to teach the interface; they reveal no B1 test state. E/I begin at 0.7 / 1.0, stationary, with zero commands, forces and contact rates. Exact snapshots are sealed in the evaluator package. No command sequence has been executed or optimized.

| Control | Disclosed fixture | Ceiling | Human task and separate evaluator check |
|---|---|---:|---|
| PC-LR | Body at (4.2, 3.8), facing east; the disclosed nearby round source is at (3, 3). | 4 s / 40 holds | Before any action, identify a left/right difference using paired raw channels and name the channel indices and observed sign. The evaluator checks the statement against exactly displayed values. If no resolved difference is present or the operator cannot identify it, record NOT DEMONSTRATED; do not replace the fixture. Turning is optional human action within the same ceiling, never an automatic search. |
| PC-MOTION | Body at (6, 5), facing east in open space. | 4 s / 40 holds | Apply a self-chosen bounded nonzero pair and distinguish the command coordinates from the achieved motion and discrepancy coordinates. Record your explanation and the actual response. No requirement that the numerical readings match the commands. |
| PC-CONTACT | Body at (0.65, 6), facing west, near the plain boundary wall. | 6 s / 60 holds | Use small paired entries to approach, and identify contact onset from raw contact/proprioceptive history. The evaluator checks actual onset/impact/support and preserves any missed onset or damage. No event popup is supplied. |
| PC-HOLD | Body at (0.52, 6), facing west, close to the same plain wall. | 10 s / 100 holds | Establish a gentle contact hold using the raw readings and achieved-motion discrepancy. The disclosed practice target is 1.0 s of continuous positive-duration support below the existing 0.25 stress threshold, with no sustained stress damage during that interval. This is an operator practice task, not a biological utility threshold. Initial impacts, interruptions and all damage remain recorded. If the target is not demonstrated, preserve that outcome. |

Use your own bounded entries; no automatic servo or privileged suggestion is supplied. The evaluator records the achieved body response after each disclosed control ends. A nonzero contact spike alone does not demonstrate a hold. Before interpreting gentle contact, distinguish the brief impulse reading from persistent positive-duration support; the actual force check is evaluator-only and appears after the control.

Record separately for every control: exact display fields/values and timestamps, user commands and annotations, achieved physical response, the operator's explanation, evaluator observation, exposure/record integrity, stop reason, and DEMONSTRATED / NOT DEMONSTRATED. Numeric signs must be resolved beyond the existing accounting/arithmetic uncertainty; no success percentage is added.

This packet prescribes one attempt per control and no retry. If familiarization is inadequate, request a separately scoped decision; do not run B1 automatically, change the body, or adapt the held-out start.
''')
    put(pub/'OPERATOR_INTEGRITY_FORM.md',r'''
# Operator integrity record — blank form, not an attestation

Operator: Jason. Date/time: NOT RECORDED. All case statuses: NOT EXECUTED.

- General sensor/body/world-law knowledge before the session: NOT RECORDED.
- Any prior access to this pair's exact hidden pose, field/phase, world image, source state, initial readings, privileged manifest, or trajectory: NOT RECORDED.
- Familiarization material seen: NOT RECORDED.
- Positive-control evidence references and demonstrated/not-demonstrated status: NOT RECORDED.
- Accidental exposure, content, timing and affected cases: NOT RECORDED.
- Assistance received during live decisions, and information available to the assistant: NOT RECORDED.
- FULL-RAW trial start/end and stop reason: NOT RECORDED.
- CHEMISTRY-HIDDEN trial start/end and stop reason: NOT RECORDED.
- Human memory/carryover from the first trial: NOT RECORDED.
- Confirmation that privileged evaluation was withheld through the pair: NOT RECORDED.

An unknown entry is not a passed integrity check. Prior phase/world knowledge may limit blinding even when no live endpoint leaks state. If exposure occurs, preserve it; qualify or withhold the held-out interpretation. Do not erase the evidence, reset the human, or substitute another fixture without a separate decision.
''')
    put(pub/'INTERPRETATION_TABLE.md',r'''
# Predeclared interpretation

| Record | Label / interpretation |
|---|---|
| All four operator controls documented | OPERATOR POSITIVE CONTROL PASSED. An interface/operator demonstration only. |
| Any control not demonstrated, missing, or record-invalid | OPERATOR POSITIVE CONTROL NOT DEMONSTRATED. B1 does not automatically run and remains uninterpretable if the gate was not established. |
| FULL-RAW source interaction with valid boundary and operator integrity | FULL-RAW HELD-OUT INTERACTION WITNESSED. A bounded positive witness that the permitted sensory history supported meaningful interaction for this human in this case. |
| No valid FULL-RAW interaction | FULL-RAW HELD-OUT INTERACTION NOT WITNESSED. Preserve approach, contact, intake, cost, damage and stop. This alone does not establish absent information. |
| Valid chemistry-hidden interaction | CHEMISTRY-HIDDEN INTERACTION WITNESSED. This trial used the retained real channels and human memory; full-first carryover prevents a necessity claim. |
| No chemistry-hidden interaction | CHEMISTRY-HIDDEN INTERACTION NOT WITNESSED. Bounded dependence/ambiguity or operator/control limitation; no proof chemistry is necessary or that other information is absent. |
| Early terminal, failure, resource or operator stop | Report the observed prefix and exact cause, leave later events unobserved. No replacement, automatic retry or continuation. |
| Forbidden live signal or prior test-state exposure | Apparatus/operator-integrity limitation. Preserve the physical records but withhold or qualify a blinded sensory-only interpretation. |
| Preparation or unsupported mask | NOT EXECUTED / APPARATUS HOLD. Not a perceptual, ecological or P failure. |

The descriptive interaction witness requires actual source contact with positive-duration support and resolved positive source-debit/body-credit transfer. Report a contact-only witness separately if transfer is absent. Do not require positive net E for the contact/transfer witness: actual gross transfer, expenditure and net E remain separate. Report every complete 0.2-second contact window's net E and any partial terminal window separately. A net-positive interval is its own scoped observation, not a requirement for P or sensory-learning success.

The evaluator records opportunity geometry, approach and its limits, all contacts, transfer, net E, all source stocks, and trajectory. A geometric approach alone is not a source interaction; a touch is not necessarily positive-duration support; positive intake is not necessarily net gain. Preserve uncertainty at every boundary.

The paired trials share only their complete initial state and unchanged physical laws. Human command divergence produces different future trajectories and fields. They are not matched sensory streams after divergence, a randomized comparison, a policy benchmark or a chemistry-necessity proof. Human memory and fixed order are explicit limitations. No source-recognition accuracy or required success percentage is defined.

All conclusions concern the external human reference. P learning, preservation, regulation, autonomous discovery, scientific efficacy and indefinite survival are untested. B2/B3/B4/C1/C2 are not prepared or authorized.
''')
    proxy=resources['A5_compute_proxy_total_seconds']/60
    rows='\n'.join(f"| {r['case']} | {r['seconds']} | {r['holds']} | {r['A5_compute_proxy_seconds']/60:.2f} | {r['full_history_row_copies_in_controller_stream']:,} | {r['stream_planning_bound_bytes']/1e6:.1f} |" for r in resources['cases'])
    examples='; '.join(f"{x['seconds_per_decision']} s per decision → {x['total_wall_minutes']:.1f} min total" for x in resources['deliberation_examples'])
    put(pub/'RESOURCE_PLAN.md',f'''
# Resource and time proposal — no execution permission

The corrected A5 recorder measured **7,714.9715165 wall seconds for 630 simulated seconds**, or **{resources['A5_seconds_wall_per_simulated_second']:.6f} wall seconds per simulated second**. Its stored trajectory was 448,657,204 bytes and its uncompressed streams were 376,284,429 bytes. This is the actual corrected-apparatus long-run basis, not the original short engineering-smoke rate.

| Case | Simulated ceiling (s) | Decisions | A5 compute proxy (min) | Repeated history rows | Stream planning bound (MB) |
|---|---:|---:|---:|---:|---:|
{rows}

Total ceiling: **84 simulated seconds / 8,400 native steps / 840 human decisions**. The base A5 proxy is **{proxy:.2f} minutes**, before human deliberation and human-interface overhead. Illustrative deliberation allowances: {examples}. These are arithmetic illustrations, not measured interactive throughput. Existing whole-history validation, serialization, HTTP response and browser rendering add unmeasured work.

The B1 horizon is **30 s per condition**, below the reviewed 180 s ceiling. The evaluator-only static geometry places a finite-body opportunity within an ordinary short approach, while retaining time for contact and some stock change. Prior A1/A2 physical access shows that such short approaches can fit well inside this ceiling; this is not a forecast for Jason's sensor-only choices. The fixed 30 s budget poses approach/contact/transfer and possible stock-linked sensory change, without requiring exhaustive discovery, depletion, adaptation over 180 s, or negative information conclusions. This is a selected short witness horizon, not a proof of the mathematically shortest sufficient trial. A miss does not authorize extension or a second start.

The current sensor-human recorder copies the full history into every decision input. For N complete holds starting at time zero, that is `N + 5*N*(N−1)` raw rows, plus cumulative past commands and notes. A 30-second trial has **448,800 repeated raw rows**, rather than only its 3,001 displayed history entries. Storage/validation cannot be projected simply by multiplying A5's constant-sized waypoint input rate. `RESOURCE_PROJECTION.json` accounts for this and records the equations.

The conservative stream envelope uses 1,200 bytes per raw row, 128 per historical command, 6,200 per historical 1,000-character note including escaping, and 10,000 bytes per decision for surrounding metadata/current note, plus the measured A5 physical-stream proxy. It gives each B1 case a **1.5 GB uncompressed-stream cap**, each operator control **256 MB**, and separate snapshot/display allowances. No compression saving is needed for that planning calculation. The byte envelope is a conservative schema calculation, not a new measured throughput result; actual caps can still terminate a case early.

Proposed wall limits: **20 minutes per control**, **2 hours per B1 trial**, including deliberation because the existing recorder's wall timer continues while bodily time is paused. No automatic extension, continuation or retry. Proposed reporting allowance after the pair: **1 hour**, saved records only. No automatic trial advances; positive-control and integrity gates are explicit human review steps.

Proposed combined-new-artifact ceiling: **12 GB**, including primary records, operator/evaluator outputs, retained packages and delivery copies. Require **12 GB free before any future launch**, request a clean administrative stop at **11 GB**, retain **1 GB** for final flush/receipt. Count disjoint directories and all copies, including snapshots; do not count the same path twice. At most four complete equivalent retentions are budgeted (primary, review copy, portable archive, delivered archive); the conservative primary-copy estimate is **{resources['combined_primary_copy_planning_bytes']/1e9:.3f} GB**. Native recording fidelity and all mask-separated evidence remain intact. No test, benchmark, prehistory, trial or background process was run to estimate these costs.

These resource numbers do not close the interface HOLD. A reviewed deprivation/lifecycle implementation must retain the same cadences and record contract, and a regenerated packet must bind its actual identities before Jason considers execution.
''')
    put(pub/'OPEN_ISSUE_B1_INTERFACE.md',r'''
# B1 apparatus compatibility — HOLD BEFORE EXECUTION

P and the pinned apparatus are unchanged. The independent review verified the existing full-raw information boundary and inert inspection within its tested scope; it did not verify a chemistry-hidden adapter or fresh browser appearance. The later correction explicitly bound `display_intervention = {"kind":"none"}` and rejected unimplemented alternatives. A5's corrected long clock does not add perceptual-display capabilities.

| Finding | Exact present surface | Consequence |
|---|---|---|
| B1-H1 — chemistry-hidden unavailable | `loom_commissioning/authority.py::validate_execution` requires `display_intervention == {'kind':'none'}` and raises `unsupported display intervention`. `controllers.py::SensorHistory`, `Run.display`, and `HumanGateway.display` supply full raw history. | The exact chemistry-hidden candidate is rejected by pure validation. It has a custody digest, not a valid launch authority. No masking implementation hash exists. |
| B1-H2 — misleading in-flight state and queued submissions | `sensor.html::render` shows `Paused between decisions` for every live payload. The click handler awaits `/command` without first changing state or disabling submission. | During an authorized future hold, the page would still look paused, and further clicks could queue commands. This does not meet the requested obvious paused/running interaction. |
| B1-H3 — live lifecycle not supplied | `sensor_ui.main` constructs `OfflineGateway` only. `HumanGateway` exists for explicit later integration. `Run.close` does not change the sensor payload's `availability`, and `HumanGateway.display` does not translate closed state. | The inert launcher is not a live launch workflow, and a finished run can retain a paused/submit-ready payload. A reviewed integration must end input cleanly without revealing privileged stop details live. |
| B1-R1 — growing record/validation work | `Run.begin_command` obtains the entire `sensor.display()` history, records it in each action, and pending-command validation revisits it. | Use the explicit history-growth estimate; A5 physics throughput alone is insufficient. No performance claim or recording-fidelity reduction is substituted. |

`STATIC_COMPATIBILITY_FINDINGS.json` gives exact checked source hashes and line anchors. The code was read, not modified. The hidden candidate was passed only to the pure execution-specification validator and produced the expected rejection. No Run, controller, live gateway or world was invoked.

## Smallest proposed closure for Jason's separate decision

Authorize a narrowly scoped **apparatus-only** implementation and independent review of:

1. A server-side chemistry-display deprivation, bound by exact implementation/specification identity. Withhold all four chemistry coordinates from every operator-visible route/history/export and record what was actually shown. Retain the original real sensor values separately for the evaluator. No physical-field, sensor-law, P, world, body or actuator change.
2. Honest client-side in-flight/paused/ended indication and rejection of concurrent/queued extra submissions. Preserve exactly one 0.1-second hold per explicit decision and the existing native/5 Hz cadence. No control macro, batching or automatic repeat.
3. Explicit authorized live gateway lifecycle, no evaluator endpoints, safe closed-state handling, and complete display/command/annotation audit. No hidden control assistance.

Exact affected surfaces likely include `authority.py`, condition-specific sensor egress/recording in `controllers.py`/`runner.py`/`pending.py` as required, and `sensor_ui.py`/`sensor.html`. The final minimal diff must be established by the separate engineering task, not inferred as authorized here.

Required review evidence: real versus shown channel equality; complete chemistry suppression including all prior rows/downloads; poison/canary leak rejection; unchanged physical state/RNG across repeated reads and display deprivation; unchanged commands/hold remainder/deadlines; one-decision handling during slow requests/double clicks; honest terminal/failure/cutoff state; separated operator/evaluator records and same full initial-state identity; null grants fail closed; canonical authority binds the actual mask implementation; pause/inspection costs no bodily time or RNG. Any manufactured execution used for that review needs separate explicit scope. No such tests were run here.

Existing full-display case objects and all prepared initial snapshots remain preserved. A new reviewed apparatus changes identities, so regenerate the exact manifests and approval hashes; do not edit the held objects, relabel the unsupported candidate as valid, mask by CSS only, substitute fake zero chemistry, or bypass validation. Do not launch FULL-RAW alone to work around the held pair. No B2/B3/B4/C1/C2 work is included.
''')
    put(pub/'REVIEW_AND_AUTHORITY_BOUNDARY.md',r'''
# Review and authority boundary

The preparation request authorizes this packet, not a trial. Every manifest has `execution_authority: null`. No approval record, grant, live launcher, request to an actuator endpoint, or execution batch was created.

The four positive-control and FULL-RAW case specifications use the existing schema-2 `sensor_human` external arm and pass pure execution-specification validation. This is not full live execution approval: no Run was constructed, and this packet's lifecycle HOLD applies to them. Each object is canonically hashed over every manifest field except the null/self-referential grant, using the reviewed sorted-key compact UTF-8 JSON procedure.

The CHEMISTRY-HIDDEN file is an **exact rejected candidate**, carrying the proposed display contract and a null implementation identity. Its digest identifies those bytes for review. It cannot truthfully be called an executable authority under the current checkpoint: the validator rejects the intervention. The overall `HELD_REVIEW_OBJECT` binds all cases, initial states, documents, order, interface/recording contracts and unresolved implementation status as a custody object. It is **not** a new runner authority schema and cannot be used to bypass the reviewed apparatus.

The order is PC-LR, PC-MOTION, PC-CONTACT, PC-HOLD, FULL-RAW, CHEMISTRY-HIDDEN. No case substitutes for another. There is one predetermined held-out B1 state, used identically for both conditions, and no candidate route/phase trial or outcome selection. Human commands remain unknown until actual decisions; the bound manual protocol and exact UI define that interface, not a precomputed policy.

The requested operator test-state secrecy means Jason should review the operator bundle and opaque hashes, leaving state/geometry inspection to a separate evaluator/reviewer if he intends to operate. Reading a privileged manifest defeats that condition even if the HTTP interface is clean. No claim of blinding is made merely because files have different directory names. Exposure is recorded, never repaired by an unapproved new fixture.

All commissioning results remain NOT EXECUTED here. B1 cannot proceed until the apparatus holds are closed under separate authority, the new exact packet is generated and reviewed, Jason explicitly authorizes it, positive controls are actually demonstrated, and the operator-integrity gate is addressed. This paragraph grants none of those actions. Stop for Jason's review.
''')
    put(pub/'SESSION_RECORD.md',r'''
# Preparation session record — 2026-09-26

Read the exact new request, project instructions and Current State orientation, current Workbench instructions/map/status, accepted apparatus-construction scope, reviewed B1 design/matrix/change rules, independent full-raw boundary review, correction reports, exact pinned source, and the corrected A5 resource/result records.

The Workbench's latest navigation still says A5 NOT EXECUTED. That is a dated pre-execution status. The newer sealed A5 result and Jason's present instruction control this task; the older files were preserved rather than silently reconciled or edited. A0–A5 remain bounded physical commissioning evidence, not P learning/perception or scientific efficacy.

Produced only a held perceptual preparation: operator instructions/cards/forms, static resource and interpretation contracts, five exact zero-time fixture snapshots, six separately identified case specifications, canonical hashes and a separate privileged evaluator package. The paired B1 conditions share one identical complete initial state. Initial raw transduction is fixture authoring, not an executed command or trajectory; it is explicitly counted in PREPARATION_CHECKS.json.

No simulation/controller execution, Run construction, native/field/prehistory step, simulation RNG draw, benchmark, component test, live UI server, trajectory replay, new dependency, production change, configuration change, Git write, canon/status-map change, push, PR, merge or background run occurred. Existing snapshots, code, reviews and A1–A5 evidence were preserved. File access to some historical test-temporary directories was denied during a cache inventory; no bypass was attempted and no assertion of exhaustive cache coverage is made. The packet uses the known verified cache and records prior-knowledge limits privately.

Remaining: chemistry deprivation implementation, truthful live lifecycle and submission handling, independent apparatus review, regenerated valid execution authorities, operator positive controls, and actual B1 evidence. No test outcome or operator competence is inferred from preparing a fixture. Stop for Jason's decision.
''')
    put(private/'README.md',r'''
# PRIVILEGED EVALUATOR PACKAGE — DO NOT SHOW THE B1 OPERATOR

This archive contains the hidden B1 initial state, phase, field/history provenance, source geometry and raw initial readings inside complete snapshots. Jason should not inspect it before both paired trials end if he is the sensor-only operator. Use a separate reviewer for privileged prelaunch checks. Same-machine file separation is not owner-resistant security.

Status: PREPARED / HOLD / NOT LAUNCH-READY. There are no execution grants. Read PRIVILEGED_EVALUATOR_MANIFEST.json, PREDECLARED_INITIAL_FIXTURES.json, INITIAL_STATE_CHECKS.json, case-manifests/, authority-objects/ and the operator-safe HOLD documents in the companion bundle. The exact chemistry-hidden candidate is intentionally rejected, because the pinned apparatus implements no deprivation adapter. Its null implementation identity is not a wildcard or deferred permission.

Complete snapshots are generated by copying the previously verified zero-time manufactured external state, changing only the predetermined body pose, recomputing its actual initial raw sensors once, and saving lossless all-state snapshots. World/configuration/fields/stocks/reserves/forces/RNG/neural state are retained. The inactive neural object's old provenance and means are deliberately preserved as in the prior external fixture; these are not sampled newborns or P runs. No organism or Engine constructor, world advance or random draw was called. The snapshots preserve the original birth provenance; PREDECLARED_INITIAL_FIXTURES.json is the explicit new manufactured-pose provenance.

The held-out start was chosen once by the recorded deterministic static rule, before its initial sensor tuple was calculated. It was not chosen from successful trajectories or screened phases/routes. The body pose is new to this packet. The existing prehistory/phase is reused, so do not claim a novel phase or erase earlier phase knowledge; require the operator's exposure declaration and qualify blinding as needed. No alternate phase/history is silently prepared.

Full and hidden conditions start from exactly the same snapshot bytes and state hash. No restoration is allowed within a trial. The fixed order is FULL-RAW then CHEMISTRY-HIDDEN; memory can carry into the second trial. Show neither privileged B1 evaluation between them. Separate actual raw chemistry from condition-specific operator-visible records; the hidden-display implementation remains absent.

The included source files and AUTHORING_SOURCE.py are custody material, not an executable launch environment or permission to rerun preparation. No trial runner is included. Canonical objects exclude only execution_authority; all grants remain null. A later corrected apparatus requires new exact identities/objects and explicit authorization.
''')
