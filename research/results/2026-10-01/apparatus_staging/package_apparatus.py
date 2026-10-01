"""Package existing manufactured evidence; never start or continue a world."""
import argparse,hashlib,json,platform,shutil,subprocess,sys,zipfile
from pathlib import Path
import numpy,scipy,pytest
from loom_p.records import code_identity,strict_bytes
from loom_commissioning.contract import apparatus_identity,BASELINE,CONFIG,FIXED,INTACT,EXTERNAL,ROSTER

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
EVIDENCE=ROOT/'artifacts/apparatus-20260924-01a0c405'
DOCS=REPO/'docs/developmental_ecology/p_apparatus_20260924'

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_json(path,data): Path(path).write_bytes(json.dumps(data,indent=2,ensure_ascii=False).encode('utf-8'))

def prepare():
    from loom_commissioning.evaluation import write_review
    review=EVIDENCE/'review-evidence'; review.mkdir(exist_ok=True)
    modes={INTACT:'intact-manufactured',FIXED:'fixed-manufactured',EXTERNAL:'external-manufactured'}
    rates=[]
    for p in (EVIDENCE/'tests-attempt-003').glob('test_pause_resume_and_reconstr*/continuous/manifest.json'):
        m=json.loads(p.read_bytes()); name=modes[m['contract']['mode']]
        dest=review/'records'/name
        for segment in ('first','second','continuous'):
            shutil.copytree(p.parent.parent/segment,dest/segment)
        duration=m['final_time']-m['contract']['initial_time']
        stored=sum(x.stat().st_size for x in p.parent.iterdir() if x.is_file())
        rates.append({'mode':m['contract']['mode'],'duration_seconds':duration,'wall_seconds':m['wall_seconds'],
            'stored_bytes':stored,'uncompressed_record_bytes':m['uncompressed_bytes'],
            'wall_seconds_per_simulated_second':m['wall_seconds']/duration,
            'stored_bytes_per_simulated_second':stored/duration,
            'scope':'0.2 s manufactured component including snapshot/diagnostic overhead; not steady-state throughput'})
    assert len(rates)==3
    write_review(review/'records/intact-manufactured/continuous',review/'privileged')
    sensor=json.loads((review/'records/external-manufactured/continuous/sensor-display.json').read_bytes())
    sensor['availability']='offline_record'
    template=(ROOT/'loom_commissioning/sensor.html').read_text(encoding='utf-8')
    offline=template.replace("fetch('/sensors').then(r=>r.json()).then(accept);",
        'accept('+strict_bytes(sensor).decode().replace('<','\\u003c')+');')
    assert "fetch('/sensors')" not in offline
    (review/'SENSOR_ONLY_REVIEW.html').write_bytes(offline.encode('utf-8'))
    (review/'sensor-display.json').write_bytes(strict_bytes(sensor))
    for filename,target in [('Open Paused Sensor Reference.cmd','artifacts\\apparatus-20260924-01a0c405\\review-evidence\\SENSOR_ONLY_REVIEW.html'),
                            ('Open Privileged Apparatus Review.cmd','artifacts\\apparatus-20260924-01a0c405\\review-evidence\\privileged\\PRIVILEGED_REVIEW.html')]:
        (ROOT/filename).write_bytes(('@echo off\r\nstart "" "%~dp0'+target+'"\r\n').encode('utf-8'))
    runtime={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'numpy':numpy.__version__,
             'scipy':scipy.__version__,'pytest':pytest.__version__,'p_code':code_identity(),
             'apparatus_code':apparatus_identity(),'configuration_semantic':CONFIG,
             'configuration_file_sha256':digest(ROOT/'configuration.json'),
             'local_execution':'Windows desktop host; existing local venv; no new dependencies installed'}
    write_json(EVIDENCE/'RUNTIME_RECORD.json',runtime)
    write_json(EVIDENCE/'RUNTIME_STORAGE_ESTIMATE.json',{'measured_components':rates,
        'historical_30s_rate':{'wall_seconds_per_simulated_second':4.6905,'stored_MB_per_simulated_second':1.9709},
        'future_world_ceiling_seconds':8960,'prior_planning_machine_hours':11.67,
        'prior_planning_compressed_GB':17.66,'status':'commissioning unexecuted; no long-run overhead measured',
        'conservative_component_rate_extrapolation':{'machine_hours':max(x['wall_seconds_per_simulated_second'] for x in rates)*8960/3600,
            'stored_GB':max(x['stored_bytes_per_simulated_second'] for x in rates)*8960/1e9,
            'warning':'planning envelope only, dominated by short-fixture and restart overhead; not an approved budget'},
        'source_of_extra_cost':'full aligned native operands, all-wave D5 detached reads, receiver records and full restart state',
        'native_evidence_downsampled':False,'prehistory_preparations_executed':0})
    write_json(EVIDENCE/'EVENTUAL_ROSTER_NOT_AUTHORIZED.json',ROSTER)
    print('Prepared three complete manufactured record sets and separate paused review pages')

def assemble():
    destination=ROOT/'artifacts/review-package-apparatus-20260924-01a0c405/assembled'
    destination.mkdir(parents=True,exist_ok=False)
    code=destination/'developmental_ecology'; code.mkdir()
    for name in ('loom_p','loom_commissioning','tests','tests_apparatus'):
        shutil.copytree(ROOT/name,code/name,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
    for name in ('configuration.json','requirements-lock.txt','verify_apparatus.py','package_apparatus.py',
                 'Open Paused Sensor Reference.cmd','Open Privileged Apparatus Review.cmd'):
        source=ROOT/name
        if source.exists(): shutil.copyfile(source,code/name)
    shutil.copytree(ROOT/'artifacts/prehistory-attempt-001',code/'artifacts/prehistory-attempt-001')
    target=code/'artifacts/apparatus-20260924-01a0c405'; target.mkdir()
    shutil.copytree(EVIDENCE/'review-evidence',target/'review-evidence')
    shutil.copytree(EVIDENCE/'references',target/'references')
    for p in EVIDENCE.iterdir():
        if p.is_file(): shutil.copyfile(p,target/p.name)
    faults=target/'faults-attempt-002'; faults.mkdir()
    for p in (EVIDENCE/'faults-attempt-002').iterdir():
        if p.is_file(): shutil.copyfile(p,faults/p.name)
    shutil.copytree(DOCS,destination/'docs/developmental_ecology/p_apparatus_20260924')
    (destination/'START_HERE.md').write_text('''# Loom P apparatus review

Apparatus construction only. P baseline 6bc9683b remains uncommissioned/untested.

Double-click `developmental_ecology/Open Paused Sensor Reference.cmd` for an inert recorded sensor view.
The separately named privileged review is for evaluators; someone who sees it cannot provide a blinded sensory witness for that fixture.
These static pages need no Python and cannot advance a body.

Read `docs/developmental_ecology/p_apparatus_20260924/BUILD_REPORT.md` and `CHECKPOINT.json`.
`SOURCE_IDENTITIES.json`, the unchanged design ZIP, P source/configuration, full manufactured streams/restarts,
fault logs, test logs, exact Git patch and inventories are included. Earlier failed-development logs are retained.

For component reproduction use Python 3.13.5 with the included pinned requirements. Run from `developmental_ecology`:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp C:\\Temp\\loom-apparatus-review-UNIQUE
python -B -X utf8 verify_apparatus.py C:\\Temp\\loom-apparatus-faults-UNIQUE
```

Choose unused paths. These commands execute manufactured component fixtures, not commissioning.
Never run the legacy smoke/prehistory helpers under this apparatus-build authority.
Fresh dependency installation and another operating system were not tested.
''',encoding='utf-8')
    print(destination)

def seal():
    package=ROOT/'artifacts/review-package-apparatus-20260924-01a0c405'; assembled=package/'assembled'
    checkpoint=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
    branch=subprocess.check_output(['git','-C',str(REPO),'branch','--show-current'],text=True).strip()
    status=subprocess.check_output(['git','-C',str(REPO),'status','--porcelain'],text=True)
    assert not status,status
    patch=subprocess.check_output(['git','-C',str(REPO),'diff','--binary',BASELINE,checkpoint])
    (assembled/'APPARATUS.patch').write_bytes(patch)
    write_json(assembled/'CHECKPOINT.json',{'checkpoint':checkpoint,'parent':BASELINE,'branch':branch,'worktree':str(REPO),
        'patch_sha256':hashlib.sha256(patch).hexdigest(),'p_code':code_identity(),'apparatus':apparatus_identity()})
    for name in ('portable-suite.log','PRESERVATION_AFTER.json','UI_REVIEW.json'):
        shutil.copyfile(EVIDENCE/name,assembled/'developmental_ecology/artifacts/apparatus-20260924-01a0c405'/name)
    inventory={p.relative_to(assembled).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(assembled.rglob('*')) if p.is_file()}
    write_json(assembled/'ARTIFACT_MANIFEST.json',{'files':inventory,'checkpoint':checkpoint})
    output=package/'Loom_P_Commissioning_Apparatus_Review_20260924.zip'
    with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(assembled.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(assembled).as_posix())
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for name,row in inventory.items():
            data=z.read(name); assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    receipt={'zip':str(output),'bytes':output.stat().st_size,'sha256':digest(output),
             'checkpoint':checkpoint,'inventoried_files':len(inventory),'all_payload_hashes_verified':True}
    write_json(package/'RECEIPT.json',receipt); print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('stage',choices=('prepare','assemble','seal')); args=parser.parse_args()
    globals()[args.stage]()
