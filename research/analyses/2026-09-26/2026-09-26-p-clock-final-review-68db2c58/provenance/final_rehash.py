"""Post-regression rehash and derived-fixture semantic proof; no simulation."""
from pathlib import Path
import json,hashlib,sys,os,subprocess,gzip
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
T=W/'worktrees/loom-p-clock-correction-20260926';D=T/'developmental_ecology'
O=W/'exports/2026-09-26-p-clock-final-review-68db2c58/provenance';Z=O.parent/'portable'
OLD=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
def read(p):return json.loads(p.read_bytes())
def ident(p):
    with p.open('rb') as f:return {'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'bytes':p.stat().st_size}
def save(n,d):(O/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
checks={}; baseline={}
for n in ['HISTORICAL_PRESERVATION','ORIGINAL_STAGE_SOURCES','ALL_SAVED_PAYLOADS_PRESERVATION']:
    before=read(O/(n+'.json'));assert not before['failures']; baseline.update(before['files'])
    failures={p:ident(Path(p)) for p,v in before['files'].items() if ident(Path(p))!=v}
    checks[n]={'checked':len(before['files']),'changed':failures}
held=read(O/'HELD_PRESERVATION.json')
for n in ['original','delivered']:
    before=held[n]; assert not before['failures']; baseline.update(before['files'])
    failures={p:ident(Path(p)) for p,v in before['files'].items() if ident(Path(p))!=v}
    checks['held_'+n]={'checked':len(before['files']),'changed':failures}
package=read(Z/'ARTIFACT_MANIFEST.json')['files']; baseline.update({str(Z/n):v for n,v in package.items()})
checks['portable_payloads']={'checked':len(package),'changed':{n:ident(Z/n) for n,v in package.items() if ident(Z/n)!=v}}
source=read(O/'PACKAGE_SOURCE_MATCH.json')['files'];baseline.update({str(T/n):v['target'] for n,v in source.items()})
checks['target_package_sources']={'checked':len(source),'changed':{n:ident(T/n) for n,v in source.items() if ident(T/n)!=v['target']}}
assert not any(r['changed'] for r in checks.values())
save('BEFORE_FILE_IDENTITIES.json',baseline)
sys.path.insert(0,str(D))
from loom_p.records import code_identity
from loom_p.schema import Config
from loom_commissioning.contract import apparatus_identity
from loom_commissioning.authority import runtime_identity
current={'P':code_identity(),'apparatus':apparatus_identity(),'configuration_semantic':Config().identity(),'configuration_file':ident(D/'configuration.json'),'runtime':runtime_identity()}
held_path=W/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481/A5_MANIFEST.json'; hm=read(held_path)
assert current['P']['sha256']==hm['p_code']; assert current['configuration_semantic']==hm['configuration']; assert current['runtime']==hm['execution']['runtime']
assert current['apparatus']!=hm['apparatus']
current['held_runtime_equal']=True;current['old_apparatus_differs']=True
save('CURRENT_IDENTITIES.json',current)
# The changed one-line fixture is independently matched to original receipt fields
# and every row of original compressed records, not to builder summary/copy.
fixture_path=D/'tests_apparatus/fixtures/clock_retrospective.json'; fixture=read(fixture_path)
results=read(O/'RETROSPECTIVE.json'); comparisons=[]
assert len(fixture['cases'])==len(results['cases'])==6
for saved,new in zip(results['cases'],fixture['cases']):
    folder=Path(saved['folder']);m=read(folder/'manifest.json')['contract']
    fields={k:m[k] for k in ['initial_time','initial_index','duration_seconds','hard_stop_time']}
    fields['execution']={'procedure':{'stages':m['execution']['procedure']['stages']}}
    with gzip.open(folder/'controller.jsonl.gz','rt',encoding='utf8') as f:rows=[[a['native_index'],a['time'],a['stage']['index']] for a in map(json.loads,f)]
    expected={'case':saved['case'],'scheduling_fields':fields,'decisions':rows}
    assert new==expected
    assert rows==[r[:3] for r in saved['rows']]
    comparisons.append({'case':saved['case'],'rows':len(rows),'complete_case_object_equal':True})
save('FIXTURE_SEMANTICS.json',{'fixture':str(fixture_path),'identity':ident(fixture_path),'entire_six_case_objects_equal_to_original_saved_sources':True,'rows_total':sum(c['rows'] for c in comparisons),'cases':comparisons,'scope_text':fixture['scope']})
# Only bounded evidence census, not a claim about unrecorded activity elsewhere.
records=[]
for name in package:
    if name.endswith('manifest.json') and 'late_pause_resume_records' in name:
        data=read(Z/name)
        if 'contract' in data:
            records.append({'path':name,'case_id':data['contract']['case_id'],'purpose':data['contract']['purpose'],'duration_seconds':data['contract']['duration_seconds'],'records':data.get('records'),'final_time':data.get('final_time')})
assert all(r['purpose']=='manufactured_fixture' for r in records)
checks['A5_evidence_limits']={'held_execution_authority':hm['execution_authority'],'held_hash':ident(held_path.parent/'AUTHORITY_OBJECT.canonical.json'),'known_A5_destinations':{str(r/'developmental_ecology/artifacts/commissioning-A5-20260926-5f077481'):(r/'developmental_ecology/artifacts/commissioning-A5-20260926-5f077481').exists() for r in [OLD,T]},'packaged_late_pause_resume_records':records,'scope':'Enumerated original held packet, original saved historical receipts, complete correction ZIP, and the two declared A5 output paths. No universal negative claim about unrecorded files/processes elsewhere.'}
# Avoid inaccessible global excludes while reading status; new empty file only.
(O/'empty-excludes').write_bytes(b'')
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
checks['final_git']={}
for root in [T,OLD]:
    base=['git','-c','safe.directory='+root.as_posix(),'-c','core.excludesFile='+(O/'empty-excludes').as_posix(),'-C',str(root)]
    checks['final_git'][str(root)]={'HEAD':subprocess.check_output(base+['rev-parse','HEAD'],cwd=root,env=env).decode().strip(),'status':subprocess.check_output(base+['status','--porcelain'],cwd=root,env=env).decode()}
checks['all_rehashed_unchanged']=True
save('FINAL_PRESERVATION.json',checks)
print(json.dumps({'checks':{n:len(v['changed']) if 'changed' in v else 'recorded' for n,v in checks.items() if isinstance(v,dict)},'P':current['P']['sha256'],'apparatus':current['apparatus']['sha256'],'configuration':current['configuration_semantic'],'fixture_rows':5579,'late_record_manifests':len(records)},indent=2))
