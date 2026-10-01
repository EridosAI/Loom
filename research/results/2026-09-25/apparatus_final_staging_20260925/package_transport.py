"""Retain final record fixtures and verify copied parent links without replay."""
import json,subprocess,sys
from package_final import S,W,D,E,A,copy,tree,evidence,write
for attempt in ('001','002'):
    source=E/('worktree-suite-'+attempt)/'test_saved_decision_journal_re0'
    target=E/'review-evidence'
    if attempt=='002':target=target/'final-suite-002'
    target=target/source.name
    assert source.is_dir() and not target.exists()
    tree(source,target)
for n in ('commit_final.py','package_transport.py'):copy(S/n,E/n)
subprocess.run([sys.executable,'-B','-X','utf8',str(S/'audit.py')],check=True)
v=json.loads((E/'FINAL_VERIFICATION.json').read_bytes())
v['checkpoint']=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD']).decode().strip()
assert v['checkpoint']=='5f07748102cb5eaa302569c87efbae095050e9fe'
ids=json.loads((E/'IDENTITIES.json').read_bytes())
assert v['apparatus']==ids['apparatus']['sha256'] and v['p_code']==ids['p_code']['sha256']
v['receipt_count']=json.loads((E/'EXECUTION_AUDIT.json').read_bytes())['count']
write(E/'FINAL_VERIFICATION.json',v)
evidence(A/'developmental_ecology/artifacts/apparatus-final-correction-20260925-01a0c405')
sys.path.insert(0,str(A/'developmental_ecology'))
from loom_commissioning.validators import verify_segment
base=A/'developmental_ecology/artifacts/apparatus-final-correction-20260925-01a0c405/review-evidence/final-suite-002'
rows={}
for name in ('first','resumed'):
    p=base/'test_resume_binding_and_stage_0'/name
    result=verify_segment(p,replay=False)
    assert result['native_records']=={'first':7,'resumed':13}[name]
    rows[str(p.relative_to(A))]=result
p=base/'test_saved_decision_journal_re0'
rows[str((p/'good').relative_to(A))]=verify_segment(p/'good',replay=False)
try:verify_segment(p/'bad',replay=False)
except ValueError as ex:
    assert 'pending decision journal continuity mismatch' in str(ex)
    rows[str((p/'bad').relative_to(A))]={'intended_rejection':str(ex)}
else:raise AssertionError('copied negative fixture was accepted')
write(E/'PORTABLE_RECORD_INTEGRITY.json',{'replay':False,'new_world_advancement':0,'copied_records':rows})
print(json.dumps(rows,indent=2))
