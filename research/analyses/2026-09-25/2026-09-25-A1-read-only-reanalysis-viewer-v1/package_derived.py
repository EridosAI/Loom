"""Verify custody and deliver a distinct derived artifact, never replace A1."""
import datetime,os,shutil,subprocess,sys,zipfile
from evidence import *
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
B=W/'developmental_ecology/artifacts/first-commissioning-A1-20260925-5f077481'
V=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
DELIVERY=ROOT.parent/(ROOT.name+'-delivery')
INBOX=V/'INBOX'/ROOT.name
NAME='A1_READ_ONLY_REANALYSIS_VIEWER_v1'
def row(p):return {'bytes':p.stat().st_size,'sha256':filehash(p)}
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-C',str(W),*args],env=env).decode().strip()
e=Evidence();before=json.loads((ROOT/'HASH_BEFORE.json').read_bytes());after=e.proof()
assert before==after,'Input archive changed'
assert not DELIVERY.exists() and not INBOX.exists(),'Do not replace an existing delivery'
nav={n:row(V/n) for n in ['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md']}
live={}
for name,expected in e.manifest['files'].items():
    if name.startswith('evidence/'):
        p=B/name[len('evidence/'):];actual=row(p);assert actual==expected,name;live[name]=actual
ids=e.launch_json('CODE_AND_RUNTIME_IDENTITIES.json')
for path,h in ids['original_file_inventory'].items():assert filehash(path)==h,path
assert git('rev-parse','HEAD')=='5f07748102cb5eaa302569c87efbae095050e9fe' and not git('status','--porcelain')
refs=ROOT/'references';refs.mkdir(exist_ok=True)
historical=refs/'FIRST_A1_COMMISSIONING_RESULT.zip'
if not historical.exists():shutil.copyfile(e.path,historical)
assert filehash(historical)==EXPECTED
subprocess.run([sys.executable,'-B','v3_checker_v1_1.py','--evidence','references/FIRST_A1_COMMISSIONING_RESULT.zip','--output','V3_REPRODUCED.json'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
assert (ROOT/'V3_REPRODUCED.json').read_bytes()==(ROOT/'V3_RESULT_v1_1.json').read_bytes()
write(ROOT/'REPRODUCTION_CHECK.json',{'command':'python -B v3_checker_v1_1.py --evidence references/FIRST_A1_COMMISSIONING_RESULT.zip --output V3_REPRODUCED.json','result_byte_identical':True,'sha256':filehash(ROOT/'V3_REPRODUCED.json'),'world_steps':0})
old=refs/'historical-v3';old.mkdir(exist_ok=True)
preserved={}
for name in ['read_results.py','V3_BOUNDARY_ERROR.json','V3_POST_CHECK_LIMITATION.md','V3_COUNT_FINDING.json','A1_RESULT_SUMMARY.json']:
    b=e.z.read('evidence/read-only-review/'+name);(old/name).write_bytes(b);preserved[name]=digest(b)
(refs/'FIRST_A1_COMMISSIONING_REPORT.md').write_bytes(e.z.read('FIRST_A1_COMMISSIONING_REPORT.md'))
source_dir=refs/'reviewed-runtime';source_dir.mkdir(exist_ok=True)
for name in ['loom_commissioning/runner.py','loom_commissioning/controllers.py','loom_commissioning/diagnostics.py','loom_commissioning/adapter.py','loom_p/records.py','loom_p/geometry.py','loom_p/physics.py','configuration.json']:
    target=source_dir/name;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(e.launch.read(PREFIX+'instrument/developmental_ecology/'+name))
for name in ['PROCEDURES.md','references/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md']:
    (refs/pathlib.Path(name).name).write_bytes(e.launch.read(PREFIX+name))
write(ROOT/'HASH_AFTER.json',after)
proof={'status':'UNCHANGED','input_before_equals_after':before==after,'canonical_A1_zip_sha256':EXPECTED,
    'local_original_evidence_files_checked':len(live),'local_original_files':live,'preserved_failed_V3_artifacts':preserved,
    'original_runtime_configuration_cache_files_unchanged':len(ids['original_file_inventory']),
    'apparatus_checkpoint':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'git_clean':True,
    'P_checkpoint':'6bc9683b54e4fa80136fe8534d7713e2a250a95f','workbench_navigation_before_delivery':nav,
    'code_world_configuration_controller_mutations':0,'physical_replays':0,'simulation_steps':0,
    'scope':'New derived folder and new Workbench intake only. No original evidence, original failure record, code repository or canonical navigation rewritten.'}
write(ROOT/'CUSTODY_PROOF.json',proof)
write(ROOT/'ANALYSIS_RUNTIME.json',{'python':sys.version,'executable':sys.executable,'executable_sha256':filehash(sys.executable),
    'dependencies':'Python standard library only for new checker/extractor/server; browser HTML/JS/Canvas without external dependencies',
    'original_instrument_runtime':'Retained in the original A1 launch packet; never loaded or executed by this analysis.'})
vr=json.loads((ROOT/'V3_RESULT_v1_1.json').read_bytes());vt=json.loads((ROOT/'V3_TEST_RESULTS.json').read_bytes());vd=json.loads((ROOT/'VIEWER_DATA_TEST_RESULTS.json').read_bytes());bv=json.loads((ROOT/'BROWSER_VERIFICATION.json').read_bytes())
assert vr['checker_sha256']==filehash(ROOT/'v3_checker_v1_1.py')==vt['checker_sha256']
assert vd['viewer_js_sha256']==filehash(ROOT/'viewer.js') and vd['viewer_data_sha256']==filehash(ROOT/'viewer_data.js')
(ROOT/'VIEWER_VERIFICATION.md').write_text(f'''# Passive viewer verification

The viewer was opened and operated through the Codex in-app browser using the loopback HTTP preview. Native stepping, scrubber Home/End, restart, play/pause, 1× and 20× playback, automatic stopping at the recorded end, all named event jumps, 29-coordinate sensor panel and accounting panel were checked. No browser JavaScript errors were reported. `BROWSER_VERIFICATION.json` and `screenshots/browser-control-checks.json` retain the checks.

Four exact displayed states are recorded in `screenshots/browser-states.json`: t=0; first impact at 6.31019048650431 s (event 632, prior native sample 631); the first complete positive-net window at native 640 / 6.4 s; and the administrative stop at native 9183 / 91.83 s. Three capture passes reflect layout/label verification; the four final screenshot files and static validation page use the last pass. The force/integrity screenshot shows the recorded peak at 6.4 s (event 641). No transient intermediate animation state is presented as a physical sample.

The viewer-data checker passed {vd['passed']} checks, comparing all {vd['native_rows_compared']} native rows to immutable evidence, all event ledgers, all fixed windows and all 919 recorded mover samples. V3's separate copied-record test suite passed {vt['passed']} tests. These are analysis/display checks, not additional commissioning cases. The passive server returned the expected page and rejected POST/PUT/DELETE with 405 and non-allowlisted paths/archive access with 404.

The direct file URL was blocked by the in-app browser's URL policy and was not bypassed. The supported double-click launcher therefore starts the verified loopback HTTP server. Its path/arguments and Python availability were inspected; OS double-click/default-browser dispatch itself was not automated. The helper is local-only, standard-library-only, read-only, has a 30-minute default lifetime, and may be closed using the launch window. No service installation or auto-start exists.

Display limitations are explicit: mover geometry is held from its latest recorded 0.1-second decision sample, with timestamp/age; exact-event pose/reserves may be between native sensor/velocity/actuator samples, which retain their own times. No interpolation, reconstructed mover motion, live control or neural-development display is used. High-speed display can skip intermediate screen frames; all recorded rows remain individually inspectable.

The original record is still the same 91.83-second wall-limit pause. It is not extended, retuned or reinterpreted as a P learning/survival result. The original failed V3 files remain unchanged; the new versioned analysis closes their previously unreached record comparisons.
''',encoding='utf-8')
# Only final/reproducible artifacts are delivered; authoring previews remain outside the package.
exclude={'inspect_records.py','finish_documents.py','write_v3_report.py','screenshots/01-initial.png','FILE_MANIFEST.json','V3_REPRODUCED.json'}
payload={p.relative_to(ROOT).as_posix():p for p in sorted(ROOT.rglob('*')) if p.is_file() and p.relative_to(ROOT).as_posix() not in exclude and '__pycache__' not in p.parts}
manifest={'artifact_kind':'DERIVED READ-ONLY V3 REANALYSIS AND PASSIVE VIEWER; not a replacement commissioning result',
    'version':'1.0','original_A1_sha256':EXPECTED,'V3_checker_version':'1.1.0','files':{n:row(p) for n,p in payload.items()}}
write(ROOT/'FILE_MANIFEST.json',manifest);payload['FILE_MANIFEST.json']=ROOT/'FILE_MANIFEST.json'
DELIVERY.mkdir();archive=DELIVERY/(NAME+'.zip')
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,p in payload.items():z.write(p,NAME+'/'+n)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and len(z.namelist())==len(payload)
    for n,p in payload.items():assert digest(z.read(NAME+'/'+n))==filehash(p),n
INBOX.mkdir(parents=True);extracted=INBOX/NAME;extracted.mkdir()
for n,p in payload.items():
    target=extracted/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target);assert row(target)==row(p),n
shutil.copyfile(archive,INBOX/archive.name);assert row(archive)==row(INBOX/archive.name)
assert e.proof()==before and filehash(e.path)==EXPECTED
for n,expected in live.items():assert row(B/n[len('evidence/'):])==expected,n
for path,h in ids['original_file_inventory'].items():assert filehash(path)==h,path
nav_after={n:row(V/n) for n in nav};assert nav_after==nav
assert git('rev-parse','HEAD')==proof['apparatus_checkpoint'] and not git('status','--porcelain')
receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifact_kind':manifest['artifact_kind'],
    'zip':row(archive),'payload_count_excluding_manifest':len(payload)-1,'every_payload_hash_and_zip_crc_verified':True,
    'project_delivery':str(archive),'workbench_delivery':str(INBOX/archive.name),'double_click_launcher':str(extracted/'OPEN_A1_VIEWER.cmd'),
    'original_A1_evidence_unchanged':True,'historical_failed_V3_unchanged':True,'code_configuration_cache_git_unchanged':True,
    'workbench_navigation_before':nav,'workbench_navigation_after':nav_after,'new_simulation_steps':0,'retries_resumes_physical_replays':0}
write(DELIVERY/'DELIVERY_RECEIPT.json',receipt);write(INBOX/'DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,indent=2))
