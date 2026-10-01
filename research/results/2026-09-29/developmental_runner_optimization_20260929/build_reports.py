"""Read measured engineering results; write review documents, never run a world."""
import csv
import hashlib
import json
import pstats
from pathlib import Path
import statistics
ROOT=Path(__file__).resolve().parent.parent
OPT=Path(__file__).resolve().parent
M=OPT/'measurements'
OUT=ROOT/'exports/2026-09-29-developmental-runner-optimization'
OUT.mkdir(parents=True,exist_ok=True)
def read(name):return json.loads((M/(name+'.json')).read_bytes())
def write(name,content):(OUT/name).write_text(content.strip()+'\n',encoding='utf8')
old=read('old-short');lean=read('lean-short-release');medium=read('medium-final');long=read('long')
life=read('lifecycle-final');scale=read('codec-scaling');neural=read('long-neural')
oldprof=read('old-profile-corrected-attribution')['profile'];leanprof=read('lean-profile-final')['profile']
oldbytes=sum(old['bytes_by_file'].values());leanbytes=lean['stored_bytes'];longbytes=long['stored_bytes']
rate=long['execution_wall_seconds']/600
fixed=life['lean']['setup_seconds']
cpmean=statistics.mean(x['seconds'] for x in long['checkpoint_measurements'][1:])
cpbytes=statistics.mean(x['bytes'] for x in long['checkpoint_measurements'][1:])
projection={}
for label,sim,segments,extra_boundary in [('initial',7200,12,0),('continuation_1',1200,4,4),('continuation_2',1800,2,2),('maximum_total',10200,18,6)]:
    expected=rate*sim+fixed*segments
    storage=longbytes/600*sim+extra_boundary*cpbytes
    projection[label]={'simulated_seconds':sim,'segments':segments,'expected_execution_seconds':expected,
        'proposed_execution_cap_seconds':.55*sim+2*segments,'expected_primary_bytes':round(storage),
        'expected_archive_bytes':round(storage*1.005),'expected_full_verification_seconds':long['verification']['verification_wall_seconds']/600*sim,
        'proposed_primary_cap_bytes':1_000_000_000 if label=='initial' else 1_500_000_000 if label=='maximum_total' else round(storage*1.6),
        'proposed_archive_cap_bytes':1_000_000_000 if label=='initial' else 1_500_000_000 if label=='maximum_total' else round(storage*1.6),
        'temporary_workspace_allowance_bytes':250_000_000}
write('RESOURCE_PROJECTION.json',json.dumps({'status':'engineering estimate and proposed reserves; no scientific execution authority',
    'basis':{'execution_wall_seconds_per_simulated_second':rate,'measured_long_seconds':600,
        'fixed_final_setup_seconds':fixed,'proposed_wall_rate':.55,'MB_unit':'decimal 1000000',
        'same_fixture_only':True,'runtime_worker_count':1},'stages':projection,
    'possible_twelve_missing_prehistories':{'new_preparation_occurred':False,'historical_per_phase_seconds':65.17840160000014,
        'projected_seconds':12*65.17840160000014,'proposed_separate_reserve_seconds':1200},
    'analysis_proposal':{'up_to_four_selected_60_second_deep_intervals':True,'wall_reserve_seconds':900,'output_reserve_bytes':500_000_000},
    'verification_cap_seconds':{'initial':180,'maximum_total':300},
    'archive_wall_allowance_seconds':120,'RAM_working_set_allowance_bytes':500_000_000,
    'RAM_commit_allowance_bytes':2_500_000_000},indent=2))

rows=[]
for label,data in [('old-0.6',old),('lean-0.6-release',lean),('lean-30-memory-fix',medium),('lean-600-pre-memory-fix',long)]:
    size=sum(data['bytes_by_file'].values()) if 'bytes_by_file' in data else data['stored_bytes']
    seconds=data['simulated_seconds'];wall=data['wall_seconds']
    rows.append(f"| {label} | {wall:.4f} | {wall/seconds:.4f} | {data['native_steps']/wall:.2f} | {data['waves']/wall:.2f} | {size/seconds/1e6:.5f} | {data['memory']['peak_working_set_bytes']/1e6:.2f} |")
profile_rows=[]
for key in dict.fromkeys([*oldprof['exclusive_seconds'],*leanprof['exclusive_seconds']]):
    profile_rows.append(f"| {key} | {oldprof['exclusive_seconds'].get(key,0):.6f} | {leanprof['exclusive_seconds'].get(key,0):.6f} |")
stats=pstats.Stats(str(OPT/'baseline/OLD_PROFILE.pstats'))
inclusive=[]
for (file,line,name),(primitive,calls,own,total,callers) in stats.stats.items():
    if name in ('passive','motor_receiver','wave_receiver','observe_native','validate_state','save_restart'):
        inclusive.append({'file':file,'line':line,'function':name,'calls':calls,'inclusive_seconds':total})
write('BASELINE_INCLUSIVE_PROFILE.json',json.dumps(inclusive,indent=2))
inclusive_rows='\n'.join(f"| {x['function']} | {x['calls']} | {x['inclusive_seconds']:.6f} |" for x in inclusive)
family_old='\n'.join(f'| {k} | {v:,} |' for k,v in old['bytes_by_file'].items())
family_long='\n'.join(f'| {k} | {v:,} |' for k,v in long['verification']['family_bytes'].items())
age_rows=[]
for start in range(0,60,10):
    b=long['blocks'][start:start+10];wall=sum(x['wall_seconds'] for x in b);seconds=sum(x['simulated_seconds'] for x in b)
    age_rows.append(f'| {start*10}–{(start+10)*10} | {wall:.4f} | {wall/seconds:.6f} |')
with (OUT/'THROUGHPUT_BY_AGE.csv').open('w',newline='',encoding='utf8') as f:
    writer=csv.writer(f);writer.writerow(['case','end_native_index','end_nominal_age_s','block_simulated_seconds','block_wall_seconds','wall_per_simulated_second','working_set_bytes','peak_working_set_bytes'])
    for label,data in [('old-short',old),('medium-final',medium),('long',long)]:
        for b in data['blocks']:
            writer.writerow([label,b['ending_native_index'],b['ending_native_index']*.01,b['simulated_seconds'],b['wall_seconds'],b['wall_seconds']/b['simulated_seconds'],b.get('working_set_bytes'),b.get('peak_working_set_bytes')])
write('OLD_VS_LEAN_PROFILE.md',f'''# Measured old versus lean execution

Actual Windows-local Python 3.13.5 engineering measurements, 29 September 2026. No scientific lives or outcome comparisons. P and physical laws are frozen. Decimal MB throughout; RAM means process peak working set, not total system RAM.

## Unprofiled execution

| Path / simulated duration | Total wall s | Wall s / sim s | Native steps / wall s | Waves / wall s | Stored MB / sim s | Peak RAM MB |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

These totals include boundary setup/checkpoint closure and exclude post-run verification, analysis and archive creation. The matched 0.6-second comparison is **{old['wall_seconds']/lean['wall_seconds']:.2f}× faster** and **{oldbytes/leanbytes:.2f}× smaller**, including small-run boundary costs. Same fixture and exact complete causal endpoint. Old stored {oldbytes:,} bytes; release lean stored {leanbytes:,} bytes.

For sustained lean execution, the single 600-second benchmark took {long['wall_seconds']:.4f} s including {long['setup_wall_seconds']:.4f} s setup; {long['execution_wall_seconds']:.4f} s for the native loop and closure ({rate:.6f} wall/sim; {60000/long['execution_wall_seconds']:.2f} native steps/s). This is about {old['wall_seconds']/.6/rate:.1f}× the old short-run rate, **not** a matched 600-second old/lean trial. No 600-second old run was needed or performed.

The 600-second run used the original lean codec before its memory-retention correction. It is retained unchanged. Its 463.99 MB peak is an observed engineering defect, not the release memory claim. Final memory correction: same encoded bytes, zero retained recursive codec closures; final 30-second benchmark peak {medium['memory']['peak_working_set_bytes']/1e6:.2f} MB. Processing 180,000 saved native rows (no simulation) remained approximately 65–67 MB. The release adds Python DLL binding at boundaries and avoids deep copies during Tier-2 warm-up; neither changes the causal scheduler. The release 0.6-second and split runs/test suite exercise the exact delivered source.

## Measured subsystem attribution

Both context profiles cover setup, 0.2 simulated seconds and closure. Values are exclusive wall seconds attributed to the active subsystem, excluding measured profiler callback time. They are measured, but profiling perturbs execution. Use the unprofiled table for speed. Nested JSON/hash/copy/I/O work is assigned to those categories, not charged again to the parent diagnostic/checkpoint category.

| Subsystem | Old seconds | Lean seconds |
|---|---:|---:|
{chr(10).join(profile_rows)}

Old attributed execution totals {sum(oldprof['exclusive_seconds'].values()):.6f} s, of which serialization is {100*oldprof['exclusive_seconds']['serialization']/sum(oldprof['exclusive_seconds'].values()):.1f}%. Callback overhead was {oldprof['callback_seconds']:.6f} s. Lean attributed execution totals {sum(leanprof['exclusive_seconds'].values()):.6f} s, plus {leanprof['callback_seconds']:.6f} s callback overhead. Lean boundary hashing appears large at 0.2 seconds because it hashes the installed numerical runtime once; it does not repeat per step.

The first pre-optimization cProfile independently recorded JSON encoding, recursive state packing and base64 conversion as dominant functions. Its full `.pstats` and raw JSON are preserved. Context attribution was subsequently added to separate shared kernels from callers. Inclusive values below are from that first profile; they overlap and must **not** be added to the exclusive table or one another.

| Baseline operation | Calls | Inclusive s |
|---|---:|---:|
{inclusive_rows}

The expensive observer path includes repeated hashes of before/after complete engines, duplicate neural operands and detached receivers. D5 arithmetic itself is small on this fixture; the surrounding copying/encoding/interference proofs are expensive. The unchanged P computations themselves are retained, including their internal diagnostic construction. No mathematical simplification was made to improve these timings.

Filesystem writes/fsync and compression are measured separately above. Packaging during a life is zero in both measured benchmark drivers; the final review archive is made only after all execution stops. No live charts or browser were launched.

## Checkpoints, pause/resume and verification

| Cost | Old | Lean |
|---|---:|---:|
| Standalone/final short checkpoint bytes | {life['old']['standalone_final_checkpoint_bytes']:,} | {lean['checkpoint_measurements'][-1]['bytes']:,} |
| Short checkpoint seconds | {life['old']['standalone_final_checkpoint_seconds']:.6f} | {lean['checkpoint_measurements'][-1]['seconds']:.6f} |
| Pause at native index 7, including checkpoint | {life['old']['pause_including_checkpoint_seconds']:.6f} | {life['lean']['pause_including_checkpoint_seconds']:.6f} |
| Exact reload/resume, including custody checks | {life['old']['resume_seconds']:.6f} | {life['lean']['resume_seconds']:.6f} |
| Post-run verification | {life['old']['continuous_record_verification_seconds']:.6f} s, one 0.6 s segment | {lean['verification']['verification_wall_seconds']:.6f} s, one 0.6 s segment |

The lean two-segment split verification took {life['lean']['split_record_verification_seconds']:.6f} s. Strong lean reload binding can cost more than the old short reload; this is a boundary cost and is intentionally retained. The long run stored {len(long['checkpoint_measurements'])} checkpoints totaling {long['verification']['family_bytes']['checkpoint']:,} bytes, took {long['recording_timings']['checkpoint']:.6f} s in checkpoint writes, and {long['recording_timings']['chunk_write']:.6f} s in chunk closure. Mean noninitial checkpoint: {cpbytes:,.0f} bytes / {cpmean:.6f} s. Full 600-second post-run verification took {long['verification']['verification_wall_seconds']:.6f} s; no physical replay or P execution in that check.

Whole-600-second neural reconstruction from saved sensory input took {neural['wall_seconds']:.4f} s (600 exact chunk-end P/RNG checks). Selected final 20-step deep analysis including a 60-second checkpoint warm-up and exact realized-field reconstruction took {life['selected_deep_final']['wall_seconds']:.4f} s in the release. These are post-run analysis costs, excluded from execution throughput.

## Bytes by record family

Old actual on-disk files, 0.6 seconds:

| Family | Stored bytes |
|---|---:|
{family_old}

Old native plus diagnostics streams alone used {old['bytes_by_file']['native.jsonl.gz']+old['bytes_by_file']['diagnostics.jsonl.gz']:,} bytes ({100*(old['bytes_by_file']['native.jsonl.gz']+old['bytes_by_file']['diagnostics.jsonl.gz'])/oldbytes:.1f}% of all short-run storage). They contain overlapping sensory/neural structures and detailed operands. Full restarts are the next major short-run cost.

Lean 600-second family accounting:

| Family | Bytes |
|---|---:|
{family_long}

`native`, `waves` and `events` are exact encoded **uncompressed family payload** sizes. They are compressed together per chunk: `chunks_stored` is their actual combined stored size, not an additional raw family. `checkpoint` and `metadata` are stored sizes. Do not add raw and compressed columns. Total actual primary store = {longbytes:,} bytes, or {longbytes/600/1e6:.6f} MB/simulated second. One shared identity asset is around 0.3 MB per apparatus/runtime and is reused, not added per life.

Lossless representative chunk comparison (raw 223,464 bytes): level 1 about 67.6 kB, level 3 about 66.9 kB, level 6 about 66.7 kB. Level 6 saved only about 1.4% against level 1 while taking roughly 50% more compression CPU. Level 1 is retained. Actual measurements for every tested level and exact byte round-trip checks are in `measurements/long.json`. A final archive stores already-compressed `.ld` members without recompressing them.

## Throughput versus age

Single longer engineering trajectory, grouped into 100 simulated-second blocks:

| Nominal age interval s | Wall s | Wall / sim |
|---|---:|---:|
{chr(10).join(age_rows)}

All individual 10-second blocks, and old/medium blocks, are in `THROUGHPUT_BY_AGE.csv`. No increasing time-per-step trend large enough to indicate whole-history copying appeared over this fixture's 600 seconds. This is not a claim covering every possible contact load or 1,800-second developmental history. The small receipt list is O(chunks); full native history is neither recopied nor re-encoded each step. The separate 180,000-row codec test is a storage scaling check, explicitly not a life.
''')

write('SCIENTIFIC_EVIDENCE_INVENTORY.md','''# Evidence retained and reconstructed

Scope: unchanged intact P and Base World. A = causally unique; B = exactly derivable; C = immutable provenance; D = redundant representation. Classification concerns evidence, not whether a biological outcome was desirable. No benchmark outcome is interpreted scientifically.

| Question / information | Class | Retained evidence and recovery |
|---|---|---|
| Actual lived input | A | All 29 raw endpoint channels at every native step; exact initial raw input; exact actual elapsed dt and absolute time/index. Step-start input is the preceding endpoint, including across continuations. No sensory downsampling. |
| Actual action | A | Delivered command pair, forces, body position/orientation/velocity/angular velocity, contact rates at each native endpoint. |
| Bodily consequences | A | E/I/stocks at each endpoint; unchanged full physical event records contain substep timing, source debit/body credit, renewal, expenditure, damage, repair, colliders, impulses and release markers. Incremental and post-run ledger reconciliation. |
| Exposure/world | A + B | Actual sampled mover rectangle/velocity, exact phase and world configuration; field diagnostics per step; exact fields at checkpoints. Intervening realized fields reconstruct from prior fields, saved actual body/stocks/dt/time through the original deterministic solver. Chunk field SHA checks. No simulated alternate body trajectory. |
| Actual handoffs and outputs | A | Every handoff index and compact actual packets/psi/q/control/credit trend/learned/exploration/need outputs, map update/use summaries, sensory norms, pooling openings and regulator bank norms. Native/wave indices retained absolutely. |
| Changes to learned sensory structure, H and regulator banks | A operands + B matrices | Full initial and periodic exact P state; all actual raw input, dt, reserves and original RNG/clock position. Replay original native/handoff functions to recover every matrix, reference, eligibility, trace, control, update operand and motor contribution. Compact use/change summaries also retained during life. No lossy matrix approximation. |
| Was changed structure used? | B with A audit | Actual association-use summaries at handoffs; exact map/bank history and read state recovered from lived inputs. Original D5 immediate receiver queries can run offline. This distinguishes actual and evoked motor/regulatory contributions without making a benefit claim. |
| RNG | A | Full RNG object and stream counter dictionary in every exact checkpoint; dynamic counters per native row; full dictionary plus exact P digest per closed chunk. No reseed on continuation. |
| Terminal/cutoff/failure | A | Exact terminal partial elapsed time/events/state; administrative pause/resource cause separately labelled; incomplete I/O failure/tail retained and automatic continuation rejected. |
| Exact continuing organism | A | All Engine/organism/world/field/source/body/RNG state at each boundary, exact continuous indices and partial-wave state. Initial-state hash + parent receipt + runtime/apparatus agreement required to append a segment. |
| Law/config/code/runtime/authority | C | Frozen P/configuration identities, apparatus file hashes, executable/version/platform, NumPy/SciPy source/native library identities, Python native runtime files in release; exact grant and request hash per segment; shared immutable assets. Verification at boundaries. |
| Chart/UI/history presentation and repeated diagnostic containers | D | Omitted from live execution; reconstruct from immutable evidence when required. They are not additional experiences of the organism. |

No scientifically unique variable identified in the existing intact-P path is intentionally discarded. The replacement is lossless causal data plus exact deterministic reconstruction, not retention of every old representation. This statement is supported by short every-step full-causal-state and D5 comparisons, full-600-second P/RNG reconstruction, selected exact field/full-state reconstruction and full-state checkpoints. It is not an empirical equivalence proof for every possible trajectory or numerical platform.

`Engine.last_native` is the sole state-comparison exception: a duplicate observer cache with no causal reader. All its scientifically relevant quantities are retained natively or derived exactly. All other fields, including internal P diagnostic state, are compared exactly. Historical old evidence and P files remain unchanged.

Tier 2 requires the recorded P and numerical runtime. Unsupported runtime changes are rejected, rather than producing approximate diagnostics presented as exact. A future diagnostic requiring information absent from this inventory must be assessed before claiming it is recoverable. Current original passive/D5 outputs were tested byte-for-byte from saved inputs. Analysis is detached/read-only and has no callback into a living organism.

Physical event dictionaries are intentionally retained in full. Further event-table specialization could save some repeated key bytes, but their compressed cost is small and preserving substep causal/accounting detail was more important than an unverified format shortcut.
''')
write('REMOVED_OR_DEFERRED_OPERATIONS.md','''# Removed or deferred commissioning operations

| Operation | New treatment | Why unique evidence survives |
|---|---|---|
| Per-native full Engine deepcopy for ordinary rollback | Minimal mutable native transaction backup; wave-writing association/regulator backup only on handoff | Unchanged update order; exact rollback/terminal tests. Static config/field geometry and nonwriting structures shared. Rare terminal search still makes complete candidates. |
| Observer before/after Engine copies | Removed from live path | Tier-2 detached reconstruction creates them when requested. |
| Per-native packed/base64/JSON state hash | P digest only at chunk closure; fields SHA at chunk closure; complete checkpoint/receipt hashes | Exact causal stream plus checkpoint and chunk evidence. No repeated state serialization just to hash it. |
| Per-native full recursive state/config/schema validation | Cheap finiteness and ledger/sequence checks live; full validation at boundaries | Frozen shape/law objects cannot structurally change through unchanged numerical updates. Physical accounting is not weakened. Invalid/corrupt saved state is checked before continuation. |
| Repeated immutable code/config/dispatch/authority checks | Bound at segment start; source closure checks at end | No external callback/rebinding in runner; grant frozen by copy and attempt receipt. Complete runtime binding is retained at boundaries. |
| Duplicate aligned raw/diagnostic copies | One native raw stream and compact wave outputs | All old alignments are deterministically reconstructible. |
| Dense full matrix dumps and update operands every wave/native | Periodic exact P checkpoints, compact actual use/update summaries, exact input replay | H/sensory weights/regulator banks reconstructed exactly; actual operands preserved in causal inputs/checkpoint state. |
| Detached receiver/D5 during life | Tier 2 only | Existing diagnostic output equality tested; no alternate trajectory or learning. |
| Full snapshots every 10 seconds | Default 60-second periodic checkpoints plus all meaningful boundaries | Maximum one checkpoint interval of replay; pause/terminal still exact. |
| Cumulative SensorHistory/session copies | Absent in developmental runner | Native records supply chronology; no operator exists in this path. Removes a potential growing-history cost. |
| Browser/UI/display JSON/controller journal/human metadata | Absent | Intact P has no external human/reference controller. Commands and experience remain recorded. |
| Charts during execution | Deferred | Read-only post-run analysis uses saved evidence. |
| Per-life source/config/runtime copies | Shared immutable content-addressed identity asset and preserved source/runtime once | Exact identities remain bound and portable source is included once in review archive. |
| Multiple complete evidence packages while running | One append-only primary per life | One final archive after execution; no transient full unpacked archive copy. |
| ZIP work during execution | None | Final review/archival step only. |
| Dense numerical JSON/list round-trips | Typed binary arrays/scalars and chunk buffering | float64 bytes preserved exactly, shapes/dtypes tagged, no pickle/eval. |
| Expensive complete-file verification every step | Chunk hash at closure; strong full post-run/continuation verification | Incremental sequence/ledger checks remain; corruption tests reject modified evidence. |
| Repeated deep copies during Tier-2 checkpoint warm-up | Only copy the requested deep interval | Warm-up still reconstructs exact P/fields; unrequested diagnostics are not computed. |

Not removed: original P neural computations (including their internal diagnostic construction), terminal event bisection, contact/viability/field solvers, source ledgers, native observations, actual wave boundaries, sparse events, RNG state, exact checkpoints, full launch/continuation validation and closed-file integrity proofs. No physics/learning constant was tuned.

The old commissioner's APIs/files remain available unchanged. This is a separate package, not an in-place rewrite or a renamed commissioning case. No human UI change was made.
''')

projection_rows='\n'.join(f"| {k} | {v['simulated_seconds']:,} | {v['expected_execution_seconds']/60:.2f} min | {v['proposed_execution_cap_seconds']/60:.2f} min | {v['expected_primary_bytes']/1e9:.3f} GB | {v['expected_archive_bytes']/1e9:.3f} GB |" for k,v in projection.items())
write('FOUNDER_SEARCH_RESOURCE_REPROJECTION.md',f'''# Resource reprojection — design arithmetic only

Fixed schedule: **12 × 600 seconds**, up to **4 × additional 300 seconds** (900 total age), up to **2 × additional 900 seconds** (1,800 total age). Same continuing lives. This report changes neither those ages/population sizes nor the developmental-selection direction. It creates no execution authority.

Basis: one disclosed 600-second intact-P engineering fixture, {rate:.6f} execution wall seconds per simulated second, {longbytes/600:,.1f} stored bytes per simulated second. Boundary setup from the release split measurement, extra continuation checkpoints included conservatively. Single worker; no assumption of free parallel scaling. The long fixture is not a Founder birth and its outcomes are not assessed.

| Stage | Simulated s | Expected execution | Proposed execution allowance | Expected primary | Expected one archive |
|---|---:|---:|---:|---:|---:|
{projection_rows}

The allowance uses 0.55 wall/sim plus 2 seconds per segment: about 62% above the observed sustained rate, with boundary overhead. It is a proposed administrative envelope, not a guarantee under all collision/solver workloads. A future launch packet must bind actual limits and stop/report rather than change laws if exceeded. Existing phase caches may be reused only lawfully; no new phase was prepared here.

Storage reserves: initial primary **1.0 GB** plus one archive **1.0 GB**; full staged primary **1.5 GB** plus one archive **1.5 GB**. Additional temporary workspace **0.25 GB**, selected Tier-2 outputs **0.5 GB**: total proposed capacities **2.75 GB initial / 3.75 GB full**, without an extra unpacked copy. These are reasonable planning reserves, not measured exact maxima. Runtime/dependency installation is shared and excluded from per-population scientific storage. One worker's observed release peak was about 93 MB working set; allow 0.5 GB working set and 2.5 GB process commit because NumPy/BLAS reserves more committed/virtual memory than resident RAM.

Keep costs separate:

- **Prehistory, if all 12 phases are missing:** historical unchanged field-only preparation measured 65.1784 seconds per phase; 13.04 minutes projected, 20-minute separate planning reserve. This task did not prepare any phase. That work requires the later approved preparation scope.
- **Full record verification:** {projection['initial']['expected_full_verification_seconds']/60:.2f} minutes initial; {projection['maximum_total']['expected_full_verification_seconds']/60:.2f} minutes full at the measured rate. Reserve 3 / 5 minutes, separately from execution.
- **Archive creation:** compressed chunks/checkpoints are copied into one verified archive after the stage, with no recompression and no full unpacked duplicate. Reserve 2 minutes for this modest local volume; the actual review-package write/hash cost is recorded in `DELIVERY_VERIFICATION.json`.
- **Tier 2:** whole-600-second P-only reconstruction measured {neural['wall_seconds']:.2f} seconds. A final 20-step deep interval with a preceding 60-second neural/field warm-up measured {life['selected_deep_final']['wall_seconds']:.2f} seconds. Propose up to four selected 60-second deep windows for an initial review, with 15 minutes of analysis CPU and 0.5 GB derived outputs reserved. This is a bounded analysis proposal, not authorization or a claim about unlimited future dossiers. Human reading time is separate.

Thus the initial execution itself is roughly **41 minutes**, with a **66.4-minute allowance**. With optional missing-prehistory reserve, verification, one archive and the proposed selected analysis, initial machine time planning is about **106 minutes**; the full staged envelope about **136 minutes**. No old 57 h / 200 GB or 82 h / 280 GB allowance is carried forward. Historical design documents remain preserved, with this measured reprojection supplied as a new document.

Uncertainty: the single long fixture does not sample all future contact loads, field-solver demands or machine contention. The reserve is explicit; it does not justify scientific execution, automatic retry, more bugs or altered horizons. No 900/1,800-second lived trajectory was benchmarked. Final-code 1,800-equivalent record-count checks use saved rows only.
''')

write('EQUIVALENCE_AND_CONTINUATION.md',f'''# Equivalence, reconstruction and continuation evidence

Release result: `COMPONENT_RELEASE.txt` — **14 passed in 29.81 seconds**. No scientific pass gate, learning/survival assessment, Founder start or new prehistory. The suite uses disclosed `loom_p.smokes.make_case` engineering fixtures. All comparisons are exact typed binary equality or `array_equal`, not loose numeric closeness. The only causal-state exclusion is duplicate observer cache `Engine.last_native`.

| Check | Result / scope |
|---|---|
| Old `Engine.step` versus new scheduler, nonzero neural fixture | Every Engine causal field, wave and event identical after each of 60 native steps. |
| Old versus new, contact fixture | Same every-step exact comparison, 60 native steps. |
| Energy terminal | Same exact partial terminal dt and all causal state. |
| Integrity/contact terminal | Same exact terminal result and all causal state. |
| Invalid-field rollback | Same failure and rolled-back causal state. |
| Binary state | Exact round-trip; bit corruption/truncation rejected. |
| Tier-2 full state and D5 | Every native state and original passive/D5 row exactly reconstructed for 60 saved steps, including fields. |
| Continuous versus save/load | Continuous 60 steps equals split at 7 → 20 → 60, preserving partial wave and exact final body/fields/P/RNG. |
| Total-age boundary tests | Manufactured clocks around 600 / 900 / 1,800 seconds: 14 native steps each; split at the named boundary versus continuous old scheduler. No claim these fixtures lived to those ages. |
| Stop/custody/error handling | Terminal continuation, mismatched state/parent, unauthorized science-kind grant and corrupted chunk rejected; storage pause at zero steps; injected I/O failure preserved separately from biology. |

Independent lifecycle timing check: old continuous endpoint equals old split at index 7; release lean split at 7 equals the same old continuous endpoint. No reset/rebirth/refill occurs. Exact final P hash in the matched pre-release comparison: `228602660301c4c58f8784b1a814251c5252e0fbdbd99bb274a0ec2d1a42bfe4`. `lifecycle-final.json` records release results and complete runtime identity.

The longer preserved fixture yielded 60,000 native records / 3,000 handoffs. Reconstructing P from all its saved actual inputs checked every one of 600 P/RNG chunk endpoints ({neural['wall_seconds']:.4f} seconds, zero body/world trajectory steps). Selected last 20 steps plus nearest-checkpoint warm-up regenerated exact realized fields and complete final causal state. The 600-second original record was not re-run or replaced after the memory repair.

Continuation API uses absolute integer native deadlines. A later grant can extend 60,000 → 90,000 → 180,000 while retaining the exact prior checkpoint and receipt, same life identifier and store, full transients/learned structures/phase/RNG. World physical time continues in the unchanged accumulated-float representation; it is never rebased. These capability tests do not authorize such scientific continuations.

Development failures are preserved:

- The first pytest run could not use the global Windows temporary directory. A fresh explicit writable base directory resolved that environment issue.
- `STORE_TESTS_001.txt` exposed a reconstructed raw-container list/tuple mismatch. The baseline uses a tuple. This was corrected in the analysis codec projection and all exact tests then passed; no physical/P law changed.
- The 600-second benchmark exposed temporary encoding/decoding closure retention. With GC disabled in an isolated saved-record component, 100 old codec calls retained 100 `put`/`get` closures and 22,346,400 bytes of encoding parts. The correction retains zero closures/parts, with identical encoded SHA `05ff3d0d00f63b4affee37dd851e5922046860c942c577e0350302aadaf7989d`. A subsequent 30-second benchmark and 180,000-row saved-data scaling check validate stable memory. No longer trajectory was repeated.
- The profiler was refined to attribute neural helpers invoked by D5 to diagnostic context. Earlier raw profiles are preserved and marked superseded for attribution, not erased.

The final source additionally binds Python DLL/native runtime files at segment boundaries and avoids unnecessary deep copies during analysis warm-up. These changes are included in release tests and lifecycle/short benchmarks; the sole long benchmark is explicitly identified as the earlier lean source. Its exact source files and identities accompany the package.

Not tested: scientific founder births/populations, learning efficacy, selection, nursery, adversarial machine-owner tampering, cross-platform bit-exact replay, crash recovery after incomplete I/O, all possible pathological collider/solver states, or a full lived 1,800-second trajectory. Incomplete stores deliberately require review rather than automatic continuation.
''')

write('DEVELOPMENTAL_RUNNER_OPTIMIZATION_REPORT.md',f'''# Developmental runner engineering report

**Implemented and verified a separate lean intact-P runner.** Matched 0.6-second engineering execution is {old['wall_seconds']/lean['wall_seconds']:.2f}× faster and {oldbytes/leanbytes:.2f}× smaller including boundary costs. The one longer 600-second fixture completed in {long['wall_seconds']:.2f} wall seconds and stored {longbytes/1e6:.2f} MB. The measured projection for **12 × 600 seconds is about 41 minutes execution and 0.63 GB primary evidence**, before separately listed preparation/verification/analysis/archive costs.

This is engineering evidence only. No developmental result from these fixtures has been interpreted. No Founder Search life, selection, nursery, new prehistory or scientific authority was created. The 600 / 900 / 1,800 total-age schedule remains unchanged.

## Identity and actual scope

Frozen P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Parent apparatus: `a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad`. Local branch: `build/p-developmental-runner-20260929`. Exact delivery commit and worktree are in `CHECKPOINT.json`.

Added `developmental_ecology/loom_developmental`, focused component tests and technical documentation. No pre-existing tracked file was edited. `loom_p`, `loom_commissioning` and `configuration.json` are unchanged from the parent. Frozen P file-set identity remains `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`; configuration semantic identity remains `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. The verification and exact Git patch are included. No push/PR/merge or Obsidian Git write occurred.

Authority is Jason's developmental optimization attachment `400b7786-b3fc-4525-b4cb-f23c18150dff`; the disclosed engineering plan preceded measurements. Local Windows Python/Git executed these checks. Synced project sources are read-only. The older `00_LOOM_CURRENT_STATE(2).md` is historical orientation, not permission to replace the later frozen P/checkpoint or current instructions. The prior `FOUNDER_SEARCH_v0_1_DESIGN.md` and `JASON_TIMING_RULING.md` are preserved; only a new measured resource reprojection is supplied here.

## What consumed time and disk?

Repeated full-state JSON/base64 serialization dominated the old intact-P harness. The refined measured old profile attributed {100*oldprof['exclusive_seconds']['serialization']/sum(oldprof['exclusive_seconds'].values()):.1f}% of measured non-callback time to serialization. Copying, compression and repeated state hashing added more. Actual P/physics/field/sensing work was a small fraction of that recorder-heavy path. The old native and diagnostic streams stored overlapping sensory/neural operands and consumed {100*(old['bytes_by_file']['native.jsonl.gz']+old['bytes_by_file']['diagnostics.jsonl.gz'])/oldbytes:.1f}% of short-run disk; restart files contributed most of the remainder.

The replacement uses bounded columnar/binary chunks, exact periodic/boundary checkpoints, compact actual wave/use summaries and shared immutable identities. It removes live D5/observer copies, duplicate aligned diagnostics, cumulative UI/sensory-history state, per-step full serialization/validation and frequent complete snapshots. A complete operation-by-operation rationale is in `REMOVED_OR_DEFERRED_OPERATIONS.md`.

## What remains and is the trajectory identical?

Every actual raw sensory reading, command/body/E/I/stock/mover observation, physical exchange/contact/impulse ledger, handoff, relevant compact developmental output and RNG continuity remains recorded. Full P/world state supports exact continuation. Detailed weights/maps/banks/credits/motor contributions and original D5 outputs reconstruct offline from lived inputs and checkpoints. No intentionally lost scientifically unique evidence was identified; the inventory explains the exact recovery route and its frozen-runtime requirement.

All 14 release component checks pass. Every causal state field was compared exactly in nonzero/contact fixtures, terminal cases and split continuation. The entire saved 600-second P trajectory reconstructed exactly at every chunk boundary. A selected interval reproduced the complete final causal state including fields. The only allowed difference is the duplicate observer cache `Engine.last_native`.

No finite test suite proves every possible future trajectory. The sole longer benchmark preceded a byte-preserving codec memory fix; its observed 463.99 MB peak and full original record are preserved. Final 30-second and 180,000-saved-row checks demonstrate the fix without repeating that long trajectory. Release exact-source short/lifecycle tests also cover added runtime boundary binding. Details and failures are in `EQUIVALENCE_AND_CONTINUATION.md`.

## Practical cost and limits

Initial 12 × 600 s: **~41 min expected execution; 66.4 min proposed execution allowance; ~0.63 GB primary plus ~0.63 GB one archive**. Full permitted staged design (10,200 s total): **~58 min expected execution; 94.1 min proposed allowance; ~0.90 GB primary plus one similar archive**. These are proposed engineering-based resources, not authority to execute. The complete tables separately budget prehistory if needed, verification, temporary workspace and bounded selected deep analysis.

The old 57 h / 200 GB and 82 h / 280 GB allowances are superseded by this measured planning document, not silently retained. Reserve proposals: 2.75 GB initial / 3.75 GB full including primary, one archive, temporary workspace and selected derived outputs. The expected rate is fixture-specific; unknown contact/solver workloads or machine contention may consume the reserve.

No scientific population, 900/1,800-second lived trajectory, biological efficacy test, founder selection or nursery was run. No outcome was used to choose starts, optimize laws or change horizons. No unattended run remains active. Stop at engineering review; a later approved launch packet is still needed for any science.

## Review contents

- `OLD_VS_LEAN_PROFILE.md`: timing/RAM/subsystem/storage/checkpoint/pause/verification measurements.
- `SCIENTIFIC_EVIDENCE_INVENTORY.md`: unique, derivable, immutable and redundant evidence.
- `REMOVED_OR_DEFERRED_OPERATIONS.md`: every removed/deferred operation and rationale.
- `EQUIVALENCE_AND_CONTINUATION.md`: exact checks, limitations and preserved failures.
- `THROUGHPUT_BY_AGE.csv`: all measured time blocks.
- `FOUNDER_SEARCH_RESOURCE_REPROJECTION.md` / `RESOURCE_PROJECTION.json`: explicit estimates/reserves.
- `IMPLEMENTATION.patch`, `CHECKPOINT.json`, `FROZEN_IDENTITY_VERIFICATION.json`: exact code/provenance.
- Portable archive: source once, exact benchmark/component evidence and source versions, profiles, request/plan, cache, manifest and integrity record. It contains no old sealed human B1 evaluator material.
''')
write('README.md','''# Loom developmental runner review

Start with `DEVELOPMENTAL_RUNNER_OPTIMIZATION_REPORT.md`. This is an engineering review, not a launch packet. Nothing in this package automatically runs a life or grants scientific execution.

The adjacent ZIP is the portable complete review: documents, exact source, implementation patch, measured benchmark stores, component logs/evidence, shared runtime identities and the preserved engineering phase cache. The small unpacked review folder intentionally does not duplicate all evidence.

After extraction, the evidence directories retain their relative shared-assets links. Historical request/cache paths inside immutable records are preserved as provenance, not rewritten. Passive validation and reconstruction use the included source and matching Python/numerical environment. `VERIFY_REVIEW.py` verifies package bytes only and does not simulate anything. Component tests, if separately requested, support `LOOM_ENGINEERING_CACHE` and `LOOM_ENGINEERING_REQUEST` overrides for the included copies. Benchmark drivers preserve their original local paths for audit and do not auto-execute on import.

See `CHECKPOINT.json` for the local apparatus commit and `DELIVERY_VERIFICATION.json` beside the ZIP for archive identity/verification. No dependency binaries are redistributed; exact versions/file identities and requirements are recorded. Byte-verification is portable; bit-exact scientific reconstruction requires the recorded numerical runtime.
''')
print(json.dumps({'documents':len(list(OUT.iterdir())),'old_short_bytes':oldbytes,'lean_short_bytes':leanbytes,'short_speedup':old['wall_seconds']/lean['wall_seconds'],'projection':projection},indent=2))
