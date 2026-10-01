"""Write explanatory review wrappers and preparation history; no Loom imports."""
import hashlib,json,pathlib,shutil
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
P=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481'
FAILED=ROOT/'exports/2026-09-25-A3-preparation-incomplete-serialization'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):(P/n).write_text(s,encoding='utf-8')
h=(P/'AUTHORITY_SHA256.txt').read_text().split()[0]
summary=json.loads((P/'INITIAL_STATE_SUMMARY.json').read_bytes())
evidence=json.loads((P/'PLANNING_EVIDENCE.json').read_bytes())
a2=json.loads((P/'references/A2_OBSERVATIONS.json').read_bytes())
assert evidence['A2_reported_final_EI']==a2['whole_case']['final_EI']
assert evidence['A2_total_damage']==a2['whole_case']['damage'] and evidence['A2_repair']==a2['whole_case']['repair']
assert evidence['A2_first_source_contact_s']==a2['sources']['0']['first_certified_contact']['time']
assert evidence['A2_second_source_contact_s']==a2['sources']['1']['first_certified_contact']['time']
assert sha(FAILED/'INITIAL_A3.snapshot.json.gz')==sha(P/'INITIAL_A3.snapshot.json.gz')
(P/'preparation-history').mkdir(exist_ok=False)
for n in ('build_packet.py','INITIAL_A3.snapshot.json.gz'):
    shutil.copyfile(FAILED/n,P/'preparation-history'/('incomplete-'+n))
write('preparation-history/PREPARATION_HISTORY.md',f'''# Preparation history — no execution

Three invocations of the packet authoring helper occurred. None instantiated Run, calculated a controller command, stepped a body/field/neural system, drew simulation randomness, regenerated prehistory or replayed a trajectory.

1. The first stopped before creating an output folder: `KeyError: There is no item named 'FILE_MANIFEST.json' in the archive`. The nested A1 launch archive has the prefix `FIRST_COMMISSIONING_LAUNCH_PACKET/`; the archive reader was corrected to use its actual existing prefix. No input archive was changed.
2. The second wrote the proposed healthy zero-time snapshot and then stopped while serializing its provenance summary: `TypeError: Object of type ndarray is not JSON serializable`. A general JSON observation conversion was added to the preparation writer. The incomplete folder remains at `{FAILED}`. Its helper and snapshot are preserved here for portable audit.
3. The third completed the same selected fixture and route, with successful identity, hash, geometry and null-grant checks. Its snapshot is byte-identical to the second invocation: `{sha(P/'INITIAL_A3.snapshot.json.gz')}`.

`PREPARATION_CHECKS.json` counts the final successful builder invocation: two snapshot loads, one deterministic instantaneous time-zero transduction and one snapshot save. Across the entire preparation task there were two such time-zero transductions (one in the incomplete authoring attempt, one in the completed attempt), four snapshot loads and two saves. These are duplicate static fixture authoring/roundtrip operations, not trial routes, impacts, lifetimes or trajectory replays. The healthy pose, E/I, plan, controller constants and horizon were not changed in response to either helper error.

The first helper revision differs from the preserved incomplete helper by only the nested archive prefix. Errors above are preparatory tooling errors, not A3 case failures. They do not authorize any execution or additional case.
''')
write('NOT_EXECUTED.md',f'''# No A3 execution occurred

Authority status: **PROPOSED / NOT AUTHORIZED**. Exact object SHA-256: `{h}`.

The complete manifest has `execution_authority: null`; the original production authorization validator rejects it with `commissioning execution is not authorized`. The dormant birth roster also remains unauthorized. No grant file or approval envelope for A3 was created. A1/A2 grants remain historical objects tied to their own exact executions.

Preparation performed source/custody hashing, read-only Git/runtime checks, nominal geometry calculations, complete saved-state loading and healthy time-zero fixture authoring, instantaneous deterministic sensor evaluation, snapshot roundtrip, static manifest/dispatch validation, arithmetic projections and documentation/packaging. All dynamic calls were guarded. No Engine constructor, Run constructor, controller-command computation, world/native/field/neural step, simulation RNG draw, prehistory preparation, replay, inspector/server or background process was performed for A3.

The final helper counts are in `PREPARATION_CHECKS.json`; the two earlier authoring errors and whole-task static-operation counts are disclosed in `preparation-history/PREPARATION_HISTORY.md`. No code, configuration, cache or prior evidence was changed. `HASH_BEFORE.json` and `HASH_AFTER.json` cover 286 original files.

The prospective run directory was absent at preparation and is checked again at sealing. All A3 physical observations remain unobserved. No claim of actual injury, repair, departure, source arrival, controller competence or A3 performance is made.
''')
write('A3_LAUNCH_PACKET.md',f'''# A3: one proposed damage → repair → energy witness

**Prepared for Jason's review. NOT AUTHORIZED. NOT EXECUTED.**

The body would begin healthy at (2.5,6), facing the existing left wall. The controller would drive it into that ordinary wall below the repair strip, allowing the unchanged mechanics to determine any injury. It would then turn away, travel up the left corridor, press gently against the existing repair strip, leave, and approach the nearby energy source at (3,10). All actual energy, integrity, stocks and world state would continue throughout. Nothing is reset between those encounters.

This asks whether that complete physical recovery sequence can be witnessed with one prescribed external controller. P is inactive; this is no test of learning, discovery or survival skill. Small real injury is acceptable evidence. No target damage value, exact full restoration, or useful-learning pass gate is imposed.

| Proposed interval | Intended action |
|---|---|
| 0–15 s | One approach/impact at ordinary wall-0 around (0,6) |
| 15–40 s | Turn away toward (1.5,6) |
| 40–75 s | Travel to (1.5,10) |
| 75–155 s | Approach repair-0 and seek gentle eligible contact/restoration |
| 155–180 s | Leave repair toward (1.5,10) |
| 180–210 s | Reach source-3 and seek actual transfer |

The existing controller uses fixed deadlines. It does not wait for a specified injury or restoration before switching stages. **If positive repair is absent before departure, the complete A3 witness is absent**, even if the body later reaches energy. This is a disclosed review choice; no new event-triggered controller is hidden in the packet. Any timing change would require a revised object before approval.

The 210-second horizon includes 80 seconds for repair approach/contact and explicit turn/departure allowances. Maximum-effort expenditure gives a no-intake arithmetic reserve floor of E≈0.175 at the horizon; it does not prove successful travel or recovery. Actual A1/A2 throughput projects approximately **41–47 minutes** of wall time. Proposed hard limits: **70 minutes runner time**, **1.5 GB uncompressed streams**, **3 GB disk budget** for primary/analysis/delivery, plus at most **one hour of read-only reporting** with zero extra world steps. Costs may differ from these projections; ordinary wall/storage checks operate between native steps.

## The ten requested deliverables

| Item | Exact record |
|---|---|
| 1. Healthy initial state | `INITIAL_A3.snapshot.json.gz`, `INITIAL_STATE_SUMMARY.json`: E=0.7, I=1, t=0, all stocks=0.2, no initial motion/contact |
| 2. Actual damage interaction | `PROCEDURES.md`: ordinary left-wall approach below strip; no integrity assignment or exact-I target |
| 3. Repair and energy destinations | Existing repair-0 at x=[0,0.25], y=[8,12]; existing source-3 at (3,10) |
| 4. Stages/constants | Typed `A3_MANIFEST.json`, full unchanged controller source and identity; six fixed stages |
| 5. Phase/prehistory | Phase 3.558411277237072, exact original cache/receipt/field hashes; no new prehistory |
| 6. Duration/resources | `BUDGET.json`, projections from actual A1/A2 long runs; 210 simulated seconds |
| 7. Event/interpretation table | `INTERPRETATION.md`, all eight reserve milestones, separate damage/repair/intake/cost/control/cutoff findings |
| 8. Canonical object/hash | `AUTHORITY_OBJECT.canonical.json`, `AUTHORITY_OBJECT.json`, `AUTHORITY_SHA256.txt` |
| 9. Plain-language story | This document and the detailed `PROCEDURES.md` |
| 10. No-execution confirmation | `NOT_EXECUTED.md`, `PREPARATION_CHECKS.json`, preparation history and delivery receipt |

Canonical authority SHA-256:

`{h}`

Initial complete state SHA-256: `{summary['state_sha256']}`. Initial snapshot file SHA-256: `{summary['snapshot_sha256']}`.

P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus remains `5f07748102cb5eaa302569c87efbae095050e9fe` on `build/p-commissioning-apparatus-20260924-01a0c405`, worktree `C:\\Users\\Jason\\Desktop\\Eridos\\Loom-p-apparatus-20260924-01a0c405`. Clean read-only status verified. No new commit or Git writes.

## Remaining uncertainties and review boundary

Actual A3 wall damage, turning/release, strip arrival, force/slip, positive restoration, departure reserve and source transfer are all untested. Straight finite-body path clearance is verified; the controller may deviate from those segments. The force servo responds to any contact and may overshoot. Repair-arrival impact can add injury. No actual I value or time of arrival is promised. The existing external recording lacks labelled mover ray hits; pose/mover/contact and raw sensory evidence remain available.

The exact fixture is a labelled manufactured healthy start, not a sampled newborn. It reuses the original inactive neural/RNG state and lawful field history; only body position, instantaneous raw sensors and fixture provenance differ from the old zero-time fixture. Static fixture authoring occurred twice because of a documented JSON helper error, producing identical snapshots; no route was rehearsed. Historical source files and both helper errors are preserved.

The workbench navigation still ends at A1/V3. This packet instead cites the later verified A2 result and current request, without rewriting that navigation. The full immutable A2 result archive is included; it contains the prior approved A2 packet and A1 evidence chain. Its existing nominal-boundary reporting limitation is preserved and explicitly distinguished from missing physical time.

No low-E/I A3 arm, other commissioning case, dynamic test, learning run, sweep, tuning, continuation, viewer launch, new prehistory or mechanism/configuration change was performed. The second A3 arm remains only in the historical design. This task ends with the proposal; genuine Jason approval of this exact object and scoped output permission are still required before any future execution.
''')
write('README.md',f'''# A3 launch packet — review only

Start with [the plain-language launch packet](A3_LAUNCH_PACKET.md), then [the exact procedure](PROCEDURES.md) and [parallel event interpretations](INTERPRETATION.md).

**NOT AUTHORIZED / NOT EXECUTED.** Canonical authority SHA-256: `{h}`.

`A3_MANIFEST.json` contains a null execution grant. The canonical object excludes only that grant and binds the healthy snapshot, procedure/interpretation documents, controller stages/constants/implementation, code/runtime/configuration, source identities and budgets. `FILE_MANIFEST.json` inventories every payload; `DELIVERY_RECEIPT.json` beside the ZIP reports its independent hash and verification.

The standard-library `validate_packet.py` can check this folder or its ZIP without importing Loom or evolving a world. It is a saved-byte validator, not a launch script. `build_packet.py` and `finish_review.py` are audit sources whose authoring paths refer to the original local workspace; they are not portable launchers. No A3 launcher, approval object or double-click execution action is supplied.

Full unchanged instrument/configuration/lockfile are under `instrument/`; reused history under `verified-cache/`; exact source documents and full A2 evidence chain under `references/`. Historical scripts/grants inside those reference archives are historical data, not instructions to execute.

Read [no-execution evidence](NOT_EXECUTED.md) and [preparation helper history](preparation-history/PREPARATION_HISTORY.md). Separate approval is required for any run, retry, route change, continuation, other arm or correction. Stop at Jason's review.
''')
write('SESSION_RECORD.md',f'''# Durable task record — 2026-09-25

Read the exact latest A3 preparation attachment, project instructions, current workbench AGENTS/map/status, historical 00_LOOM_CURRENT_STATE, applicable design/matrix/change rules and apparatus scope/closure records. Inspected unchanged controller, adapter, runner, snapshot, geometry/accounting configuration and prior A1 preparation. Verified A2 result (60 payloads), nested A2 launch (75), A1 result (49) and A1 launch (65), plus current local source/runtime identities. Source provenance is in SOURCE_IDENTITIES.json.

Created one prospective A3 healthy initial fixture, fixed six-stage plan, event definitions, reserve/resource arithmetic and null-grant authority object `{h}`. Actual outcomes remain unknown. The fixed-clock versus event-triggered sequencing choice is explicitly disclosed for review. No mechanism/law ambiguity was resolved by changing code or world. No shared workbench map, source, repository or Git state was edited.

Static geometry, snapshot identity/roundtrip, inactive-organism/RNG preservation, exact runtime/dispatch/schema and null-grant rejection checks passed. Two preparation-helper errors were corrected and disclosed without any trajectory or command. No commissioning execution, test suite, replay, dynamic diagnostic, tuning, prehistory or visualization server ran. Final folder/ZIP/copy verification is recorded separately by the seal/delivery receipts.

Remaining work belongs to a separate authorization: if Jason approves the exact object, revalidate live prerequisites, obtain scoped output access and execute that one case under its fixed limits. This task stops here and grants nothing.
''')
shutil.copyfile(S/'finish_review.py',P/'finish_review.py')
print(json.dumps({'review_written':True,'authority_sha256':h,'prior_failed_fixture_identical':True,'new_execution':False}))
