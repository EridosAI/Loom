"""Saved-byte documentation, projection-unit clarification, binding and sealing; no Loom imports."""
import hashlib,json,pathlib,shutil,sys,time,zipfile
from validate_packet import verify,canonical
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent;O=ROOT/'exports/2026-09-26-A4-launch-packet-5f077481'
DEL=ROOT/'exports/2026-09-26-A4-launch-delivery-5f077481'
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(n,v):(O/n).write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def read(n):return json.loads((O/n).read_bytes())
def text(n,v):(O/n).write_text(v,encoding='utf-8')
def main():
    assert not (O/'FILE_MANIFEST.json').exists() and not DEL.exists()
    # Only unit labels were corrected after the first unsealed review. No input,
    # number, fixture, case, stage, controller or horizon is reselected or executed.
    oldhash=read('AUTHORITY_OBJECT.json')
    budget=read('RESOURCE_PROJECTION.json')
    names={'recorder_wall_seconds_per_sim_second':'recorder_wall_seconds','whole_process_wall_seconds_per_sim_second':'whole_process_wall_seconds','uncompressed_bytes_per_sim_second':'uncompressed_stream_bytes','stored_bytes_per_sim_second':'stored_trajectory_bytes'}
    for row in list(budget['per_case'].values())+[{'by_measured_case':budget['total_by_measured_case']}]:
        row['by_measured_case']={k:{names.get(kk,kk):vv for kk,vv in v.items()} for k,v in row['by_measured_case'].items()}
    budget['total_by_measured_case']={k:{names.get(kk,kk):vv for kk,vv in v.items()} for k,v in budget['total_by_measured_case'].items()}
    write('RESOURCE_PROJECTION.json',budget)
    shutil.copyfile(S/'build_packet.py',O/'build_packet.py')
    shutil.copyfile(__file__,O/'finish_packet.py')
    rows=[]
    for cid,r in budget['per_case'].items():
        a=r['by_measured_case']['A2'];b=r['by_measured_case']['A3']
        rows.append(f"| {cid} | {r['simulated_seconds']:g} s | {a['recorder_wall_seconds']/60:.2f}–{b['recorder_wall_seconds']/60:.2f} min | {a['stored_trajectory_bytes']/1e6:.2f}–{b['stored_trajectory_bytes']/1e6:.2f} MB | {r['wall_cap_seconds']/60:g} min |")
    text('RESOURCE_PLAN.md',"""# A4 resource projection — no new benchmark

The source measurements are the complete A2 180 s and A3 210 s records. A2 used 2,116.03 recorder wall seconds, 105.66 MB uncompressed and 62.74 MB stored. A3 used 2,506.23 recorder wall seconds, 119.34 MB uncompressed and 81.73 MB stored. Exact receipts and calculations are in `RESOURCE_PROJECTION.json`, with unchanged originals under `references/` and inside the sealed A3 result archive.

| Case | Simulated ceiling | Projected recorder time | Projected stored trajectory | Runner wall cap |
|---|---:|---:|---:|---:|
"""+'\n'.join(rows)+"""

Total: **76 simulated seconds, 7,600 native steps, 760 controller decisions** at full recording fidelity. The two measured rates project **14.89–15.12 minutes** of recorder time and **26.49–29.58 MB stored**, or **43.19–44.61 MB uncompressed**. Whole-process linear extrapolation is 14.90–15.22 minutes. Allow roughly **15–16 minutes plus saved-data reporting**; three fresh starts and mover-specific contacts may cost differently. No completion guarantee or throughput benchmark was run.

The fixed administrative runner caps total **35 minutes**, plus **10 minutes total for read-only validation/reporting/packaging**. Each case has a 100 MB uncompressed-stream cap; these are distinct from the combined 3 GB disk cap for primary records, analysis and delivery copies. Require 3 GB free before launch and before each subsequent case. A clean resource pause ends the batch without resume or substitution. The unchanged native-step guard and final flushing can add a small overrun; an I/O fault is an apparatus failure, not a clean cutoff.

The portable launch packet also carries about **155 MB of immutable nested A0–A3 review evidence**, which dominates its size. Budget about **160 MB for the launch packet** and **200 MB per final review bundle** including launch evidence and new records. Preserve raw originals and copied packages within the same 3 GB allowance. The delivery receipt gives actual preparation package bytes.

No thinning of native records, sensors, events, controller samples or snapshots is allowed. Snapshot/history overhead is not perfectly linear; short independent cases differ from A2/A3. Do not reclaim space by deleting historical evidence. The basal/max-command conservative energy floors at the ceilings are CROSS 0.66, WAIT 0.63 and DETOUR 0.62 in the absence of intake; this is an accounting bound, not a survival or learning gate.
""")
    notes={'preparation_only':True,'authoring_failures':[],'executed_build_helpers':1,'static_fixture_authorings':3,'proposal_review_changes':['Before sealing, scaled resource projection keys were corrected from rate-unit names to total-unit names. Numeric projections, states, phase, routes, controllers and horizons unchanged. The guarded authoring helper was updated for reproducibility; it was not rerun.'],'discarded_or_trial_simulations':0,'request_provenance':'A4_PREPARATION_REQUEST.txt is a transcription of the current user message with separator formatting normalized; it is not an original attachment or an execution approval.','not_tested':['Actual A4 commands or trajectories','Actual waiting/crossing/detour success','Contact/damage outcomes or exact continuous-time clearance minimum','P neural learning, perception, prediction or efficacy','All phases, reserves or starts','Any lifetime, cohort, additional case, retry or continuation']}
    write('PREPARATION_REVIEW_NOTE.json',notes)
    obj=read('AUTHORITY_OBJECT.json')
    additional=['RESOURCE_PLAN.md','PREPARATION_REVIEW_NOTE.json','finish_packet.py']
    # Rebind the unsealed proposal's documentation, preserving exact trajectory identities.
    for n in additional:obj['bound_documents'][n]=sha(O/n)
    for n in obj['bound_documents']:obj['bound_documents'][n]=sha(O/n)
    for member in obj['cases']:
        m=read(member['manifest_file']);bf=m['execution']['procedure']['protocol']['bound_files']
        for n in additional:bf[n]=sha(O/n)
        for n in bf:bf[n]=sha(O/n)
        write(member['manifest_file'],m)
        member['manifest_file_sha256']=sha(O/member['manifest_file'])
        child={k:v for k,v in m.items() if k!='execution_authority'}
        (O/member['execution_object_file']).write_bytes(canonical(child))
        member['execution_object']=child;member['execution_sha256']=sha(O/member['execution_object_file'])
    write('AUTHORITY_OBJECT.json',obj);(O/'AUTHORITY_OBJECT.canonical.json').write_bytes(canonical(obj));h=sha(O/'AUTHORITY_OBJECT.canonical.json')
    text('AUTHORITY_SHA256.txt',h+'  AUTHORITY_OBJECT.canonical.json\n')
    text('README.md',f"""# A4 launch packet — prepared, not executed

One proposal, three independent predetermined physical witnesses. **Jason's separate authorization is required before any case runs.**

| Case | Start → destination | Prescription | Ceiling |
|---|---|---|---:|
| A4-CROSS | (10,8.8) → (10,12) | Cross during the initial clear window | 16 s |
| A4-WAIT | (6,8.8) → (6,12) | Hold own position through t=12, then cross | 28 s |
| A4-DETOUR | (1.5,6) → (1.5,14) | Exact A0 always-clear left bypass | 32 s |

All start healthy and stationary, facing north, E=0.7/I=1, with the same lawful phase-matched field history. No mover, body, reserve, sensor, controller-gain or P-law change. Starts are explicitly manufactured external fixtures, not sampled newborns. The wait is expressed through the existing paired-actuator waypoint interface. Static geometry and analytic timing make each strategy a meaningful proposed test; actual outcomes remain unobserved.

Read [the plain-language plan](PROCEDURES.md), [interpretation table](INTERPRETATION.md), [resource plan](RESOURCE_PLAN.md), [batch approval workflow](BATCH_EXECUTION_RULES.md), and [passive replay record contract](VIEWER_RECORD_CONTRACT.md). Exact manifest/snapshot/object files are in [A4-CROSS](cases/A4-CROSS/MANIFEST.json), [A4-WAIT](cases/A4-WAIT/MANIFEST.json) and [A4-DETOUR](cases/A4-DETOUR/MANIFEST.json).

The projected new trajectory total is about **15–16 wall minutes and 26.5–29.6 MB stored** (43.2–44.7 MB uncompressed), from actual A2/A3 receipts. Full native fidelity is retained. Hard administrative allowances are **35 runner minutes + 10 reporting minutes**, and **3 GB combined disk**. Prior review evidence adds about 155 MB to this portable packet; no simulation is needed to inspect it.

**Canonical batch authority SHA-256:**

`{h}`

[Readable authority object](AUTHORITY_OBJECT.json) · [exact canonical bytes](AUTHORITY_OBJECT.canonical.json). The outer object binds all three complete constituent objects. The unchanged apparatus is single-case; its future exact constituent approval envelopes must retain the genuine parent approval as described in the workflow. All current manifest grants are null; all three were rejected by the existing authorization gate. This is not an execution grant.

Preparation verification: **0 world/field/neural steps, 0 controller command calls, 0 simulation RNG draws, 0 new prehistory, 0 replay or candidate trials**. Three instantaneous t=0 sensor evaluations authored the three fixed snapshots; all inactive organism/RNG/field/body attributes except declared position, heading, raw sensors and provenance are unchanged. [Guarded preparation record](PREPARATION_CHECKS.json), [preservation record](PRESERVATION.json), and [review note](PREPARATION_REVIEW_NOTE.json). All **435 scoped original files** retained their hashes; the actual code worktree remains clean at the pinned apparatus commit. No Git writes or new commit.

The portable validator uses only saved bytes and the Python standard library. `python -B validate_packet.py` verifies this extracted directory; pass the ZIP path to verify the archive. It does not import Loom, compute commands or launch a world. The included authoring helper is provenance, not a launch command; it refuses an existing output directory and is tied to the original local references. No execution helper, live viewer, server or scheduler is included.

Remaining limitations: A4 performance, actual contact/timing, destination arrival and controller competence are untested; analytic nominal clearance is not a measured continuous-time clearance certificate. The detour uses its already-declared independent endpoints, so it is not an equal-endpoint efficiency comparison. P learning/perception, all-phase safety, lifetimes and every other commissioning row remain outside this packet. Full production launch preflight is deferred until genuine authorization. Stop here for Jason's review.
""")
    result=verify(lambda n:(O/n).read_bytes(),[p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()],False)
    write('STATIC_VALIDATION.json',result)
    before=read('HASH_BEFORE.json');assert all(sha(path)==v for path,v in before.items())
    assert not pathlib.Path(obj['cases'][0]['execution_object']['execution']['procedure']['protocol']['record_destination']).parents[1].exists()
    files={p.relative_to(O).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(O.rglob('*')) if p.is_file()}
    write('FILE_MANIFEST.json',{'schema':1,'authority_sha256':h,'files':files})
    sealed=verify(lambda n:(O/n).read_bytes(),[p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()])
    DEL.mkdir(parents=True);zp=DEL/'A4_LAUNCH_PACKET.zip'
    with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(O.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(O).as_posix())
    with zipfile.ZipFile(zp) as z:archive=verify(z.read,z.namelist())
    receipt={'packet_directory':str(O),'zip':str(zp),'zip_sha256':sha(zp),'zip_bytes':zp.stat().st_size,'payload_count':len(files),'authority_sha256':h,'directory_verification':sealed,'archive_verification':archive,'no_execution':True}
    (DEL/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
