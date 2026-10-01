"""Read-only provenance and saved-stage compatibility; writes only new review receipts."""
from pathlib import Path
from fractions import Fraction
import ast,gzip,hashlib,json,os,subprocess,sys
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
T=W/'worktrees/loom-p-clock-correction-20260926'; D=T/'developmental_ecology'
O=W/'exports/2026-09-26-p-clock-final-review-68db2c58/provenance'
Z=O.parent/'portable'; B=W/'exports/2026-09-26-A5-clock-correction'
OLD=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'; BEFORE='5f07748102cb5eaa302569c87efbae095050e9fe'; HEAD='68db2c581f07200966d699a4f55a65f9b96df1e9'
def read(p):return json.loads(Path(p).read_bytes())
def ident(p):
    with Path(p).open('rb') as f:return {'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'bytes':Path(p).stat().st_size}
def save(n,d):
    (O/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(n, 'written',flush=True)
def git(*args,root=T):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+root.as_posix(),'-C',str(root),*args],cwd=root,env=env)
def check_map(mapping):
    out={'count':len(mapping),'matched':0,'failures':{},'files':{}}
    for p,v in mapping.items():
        try:
            actual=ident(p); out['files'][p]=actual
            if actual==v:out['matched']+=1
            else:out['failures'][p]={'expected':v,'actual':actual}
        except Exception as e:out['failures'][p]=repr(e)
    return out
patch=git('diff','--binary',BEFORE,HEAD)
files=git('diff','--name-status',BEFORE,HEAD).decode().splitlines()
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','HEAD^').decode().strip()==BEFORE
assert git('merge-base',P,HEAD).decode().strip()==P
assert patch==(Z/'CLOCK_SCHEDULING_CORRECTION.patch').read_bytes()
unchanged={n: not git('diff','--name-only',P,HEAD,'--','developmental_ecology/'+n).strip() for n in ['loom_p','tests','configuration.json','requirements-lock.txt']}
unchanged['adapter_from_5f']=not git('diff','--name-only',BEFORE,HEAD,'--','developmental_ecology/loom_commissioning/adapter.py').strip()
exp={rev:git('rev-parse',rev+':EXP1-21').decode().strip() for rev in [P,BEFORE,HEAD]}
assert len(set(exp.values()))==1
blobs={p.relative_to(T).as_posix():git('show',HEAD+':'+p.relative_to(T).as_posix())==p.read_bytes() for p in (D/'loom_commissioning').glob('*.py')}
save('GIT.json',{'HEAD':HEAD,'parent':BEFORE,'P_ancestor':P,'branch':git('branch','--show-current').decode().strip(),'old_HEAD':git('rev-parse','HEAD',root=OLD).decode().strip(),'target_status':git('status','--porcelain').decode(),'old_status':git('status','--porcelain',root=OLD).decode(),'changed_files':files,'stat':git('diff','--stat',BEFORE,HEAD).decode(),'patch':{'bytes':len(patch),'sha256':hashlib.sha256(patch).hexdigest(),'matches_package':True},'P_unchanged':unchanged,'EXP1-21_trees':exp,'apparatus_committed_blob_matches':blobs})
package_files=read(Z/'ARTIFACT_MANIFEST.json')['files']
matches={}
for n,v in package_files.items():
    if n.startswith(('developmental_ecology/','docs/')) and (T/n).is_file():matches[n]={'package':ident(Z/n),'target':ident(T/n),'match':ident(Z/n)==ident(T/n)}
assert all(v['match'] for v in matches.values())
save('PACKAGE_SOURCE_MATCH.json',{'count':len(matches),'files':matches})
protected=read(B/'PROTECTED_BEFORE.json')
prot={n:{'expected':h,'target':ident(D/n)['sha256'],'old':ident(OLD/'developmental_ecology'/n)['sha256'],'portable':ident(Z/'developmental_ecology'/n)['sha256']} for n,h in protected.items()}
assert all(len(set(v.values()))==1 for v in prot.values())
save('PROTECTED.json',{'count':len(prot),'all_match':True,'files':prot})
# Historical inventory pinned before diagnosis, original held packet, delivered held packet.
history=read(W/'exports/2026-09-26-A5-clock-compatibility-review-5f077481/SOURCE_IDENTITIES_BEFORE.json')
save('HISTORICAL_PRESERVATION.json',check_map(history))
held=W/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'; hm=read(held/'FILE_MANIFEST.json')['files']
delivered=WB/'INBOX/2026-09-26-A5-launch-packet-HOLD-5f077481/A5_LAUNCH_PACKET_HOLD'
save('HELD_PRESERVATION.json',{'original':check_map({str(held/n):v for n,v in hm.items()}),'delivered':check_map({str(delivered/n):v for n,v in hm.items()}),'authority':ident(held/'AUTHORITY_OBJECT.canonical.json'),'execution_authority':read(held/'A5_MANIFEST.json')['execution_authority'],'held_manifest':ident(held/'A5_MANIFEST.json'),'known_A5_destination_exists':{str(r/'developmental_ecology/artifacts/commissioning-A5-20260926-5f077481'):(r/'developmental_ecology/artifacts/commissioning-A5-20260926-5f077481').exists() for r in (OLD,T)}})
# Import only the inspected side-effect-free stage helper. Never invoke waypoint_command,
# make_manifest, approval, Engine, Run, adapter, initialization, or any physical verifier.
sys.path.insert(0,str(D))
from loom_commissioning.clock import decision_clock
from loom_commissioning.controllers import waypoint_stage, WAYPOINT_SETTINGS
source_refs=read(B/'RETROSPECTIVE_SOURCES.json')
save('ORIGINAL_STAGE_SOURCES.json',check_map(source_refs))
folders={'A1':OLD/'developmental_ecology/artifacts/first-commissioning-A1-20260925-5f077481/trajectory-001','A2':OLD/'developmental_ecology/artifacts/commissioning-A2-20260925-5f077481/trajectory-001','A3':OLD/'developmental_ecology/artifacts/commissioning-A3-20260925-5f077481/trajectory-001'}
folders.update({n:OLD/'developmental_ecology/artifacts/commissioning-A4-20260926-5f077481'/n/'trajectory-001' for n in ['A4-CROSS','A4-WAIT','A4-DETOUR']})
results=[]; payloads={}; gains={}
for name,folder in folders.items():
    receipt=read(folder/'manifest.json'); m=receipt['contract']; stages=m['execution']['procedure']['stages']
    assert m['baseline']==P and m['apparatus']['sha256']=='d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a'
    for filename,v in receipt['files'].items():payloads[str(folder/filename)]=v
    assert ident(folder/'controller.jsonl.gz')==receipt['files']['controller.jsonl.gz']
    deadlines=[]
    for s in stages:
        offset=(Fraction(str(s['until']))-Fraction(str(m['initial_time'])))*100
        assert offset.denominator==1
        deadlines.append(m['initial_index']+int(offset))
    with gzip.open(folder/'controller.jsonl.gz','rt',encoding='utf8') as f:actions=[json.loads(line) for line in f]
    discrepancies=[]; rows=[]
    for a in actions:
        index=a['native_index']; expected=min(sum(index>=end for end in deadlines),len(deadlines)-1)
        actual=waypoint_stage(decision_clock(m,index),len(stages)); saved=a['stage']['index']
        if expected!=saved or actual!=saved:discrepancies.append({'index':index,'saved':saved,'integer_oracle':expected,'selector':actual})
        rows.append([index,a['time'],saved,actual,expected])
    gains[name]=m['execution']['controller']['configuration']==WAYPOINT_SETTINGS
    results.append({'case':name,'folder':str(folder),'manifest':ident(folder/'manifest.json'),'controller_stream':ident(folder/'controller.jsonl.gz'),'historical_apparatus':m['apparatus']['sha256'],'saved_decisions':len(actions),'receipt_controller_count':receipt['records']['controller'],'stage_deadlines':deadlines,'disagreements':discrepancies,'max_abs_command_clock_discrepancy':max(abs(a['time']-(m['initial_time']+(a['native_index']-m['initial_index'])*.01)) for a in actions),'first_index':actions[0]['native_index'],'last_index':actions[-1]['native_index'],'rows':rows})
assert [r['saved_decisions'] for r in results]==[919,1800,2100,160,280,320]
assert not any(r['disagreements'] for r in results)
save('RETROSPECTIVE.json',{'scope':'Original saved A1-A4 receipts and compressed controller streams. Metadata-only pure selector and independent integer oracle; no replay/controller commands/world/authority construction. A1-A4 were executed with old apparatus, not corrected checkpoint.','selector_source':ident(D/'loom_commissioning/controllers.py'),'clock_source':ident(D/'loom_commissioning/clock.py'),'total':sum(r['saved_decisions'] for r in results),'disagreements':0,'controller_gains_match_all_six':gains,'cases':results})
save('ALL_SAVED_PAYLOADS_PRESERVATION.json',check_map(payloads))
# Compare old/new gain literal without executing either controller.
def gain_literal(p):
    tree=ast.parse(p.read_text(encoding='utf8'))
    return next(ast.literal_eval(node.value) for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='WAYPOINT_SETTINGS' for t in node.targets))
assert gain_literal(OLD/'developmental_ecology/loom_commissioning/controllers.py')==gain_literal(D/'loom_commissioning/controllers.py')
save('GAINS.json',{'unchanged':True,'gains':WAYPOINT_SETTINGS})
print('Done: original 5579 decisions, zero disagreements; preservation details saved.')
