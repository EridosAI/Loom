"""Reconstruct only the three recorded 0.2-second fixtures; no new trajectory."""
from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
import numpy as np
REPO=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=REPO/'developmental_ecology';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(D));os.environ['GIT_OPTIONAL_LOCKS']='0'
from loom_commissioning import adapter,diagnostics
from loom_commissioning.contract import EXTERNAL,FIXED
from loom_commissioning.runner import load_restart
from loom_commissioning.validators import read_stream
from loom_p.records import state_hash,strict_bytes,view
results=[]
for mode in sorted((D/'artifacts/apparatus-20260924-01a0c405/review-evidence/records').iterdir()):
 path=mode/'continuous';e,s,m=load_restart(path/'initial.restart.json.gz')
 native=read_stream(path/'native.jsonl.gz');saved=read_stream(path/'diagnostics.jsonl.gz')
 actions={round(a['time'],10):a for a in read_stream(path/'controller.jsonl.gz')}
 remaining=s['hold_remaining'];command=s['held_command'];different_raw=0;waves=0;nativeprobes=0;checked_cortices=0
 for n,d in zip(native,saved):
  before=copy.deepcopy(e)
  if m['mode']==EXTERNAL:
   if remaining==0:
    action=actions[round(e.time,10)];command=action['command'];remaining=action['hold_native_steps']
   remaining-=1
  actual,w,ev,discarded=adapter.step(e,m['mode'],command,s['frozen'])
  old_hash=state_hash(before);new_hash=state_hash(e)
  observed=diagnostics.passive(before,e,w,m['mode'],discarded)
  assert strict_bytes(view(observed))==strict_bytes(d),(mode.name,n['native_index'])
  assert state_hash(before)==old_hash and state_hash(e)==new_hash
  assert d['input_time']==before.time and d['endpoint_time']==e.time
  assert d['raw_step_start']==view(before.raw) and d['raw_endpoint']==n['raw']==view(e.raw)
  if d['raw_step_start']!=d['raw_endpoint']:different_raw+=1
  if m['mode']!=EXTERNAL:
   for i,cd in enumerate(d['cortices']):
    old=before.organism.cortices[i];new=e.organism.cortices[i]
    raw=np.array(d['raw_step_start'][i]);residual=raw-old.mean
    assert np.array_equal(residual,np.array(cd['residual_used']))
    assert np.array_equal(new.mean,old.mean+(-np.expm1(-n['elapsed']/e.c.tau_receptor))*(raw-old.mean))
    assert np.array_equal(np.array(cd['shared_reference']),old.shared_ref) and np.array_equal(np.array(cd['fine_reference']),old.fine_ref)
    assert np.array_equal(np.array(cd['shared_applied_delta']),new.shared-old.shared)
    assert np.array_equal(np.array(cd['fine_applied_delta']),new.fine-old.fine)
    assert view(new.diagnostic['groups'])==cd['pressures']
    if m['mode']==FIXED:assert not np.any(cd['shared_applied_delta']) and not np.any(cd['fine_applied_delta'])
    checked_cortices+=1
  if w is not None:
   waves+=1
   for p,mean,beta in zip(d['wave_alignment']['packets'],d['wave_alignment']['old_means'],d['wave_alignment']['beta']):
    assert np.array_equal(np.array(p)-mean,np.array(beta))
   credit=d['credit_separate_E_I']
   assert np.array_equal(np.array(credit['old_eligibility']),before.organism.regulator.eligibility)
   assert np.array_equal(np.array(credit['applied_theta_delta']),e.organism.regulator.theta-before.organism.regulator.theta)
   assert len(credit['actual_reserves'])==2
   assert 'D5_wave' in d
  if 'D5_native' in d:nativeprobes+=1
 final,_,_=load_restart(path/'final.restart.json.gz');assert state_hash(e)==state_hash(final)
 results.append({'mode':m['mode'],'native_rows':len(native),'diagnostic_rows_bit_exact':len(saved),'cortical_rows_with_independent_operand_checks':checked_cortices,'input_endpoint_raw_different_rows':different_raw,'wave_rows':waves,'D5_native_rows':nativeprobes,'final_state':state_hash(e),'observer_pre_post_hashes_unchanged_at_every_row':True})
with (OUT/'DIAGNOSTIC_RECONSTRUCTION.json').open('x',encoding='utf-8') as f:json.dump(results,f,indent=2)
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+str(REPO),'-C',str(REPO),*args],cwd=REPO).decode().strip()
refs=['d5f7efbe67193f215e52d95ca912db131a79f31c','f7eb6f27c661e3db193a4225b56a825d7e41739d','6bc9683b54e4fa80136fe8534d7713e2a250a95f','05abf60401d08f38750bca589b1c040e10513d7b']
trees={ref:git('rev-parse',ref+':EXP1-21') for ref in refs};assert len(set(trees.values()))==1
ancestry={ref:subprocess.run(['git','-c','safe.directory='+str(REPO),'-C',str(REPO),'merge-base','--is-ancestor',ref,refs[-1]],cwd=REPO).returncode==0 for ref in refs[:-1]};assert all(ancestry.values())
extra={'EXP1_21_trees':trees,'ancestor_checks':ancestry,'all_prior_tracked_files_unchanged':not git('diff','--name-only','--diff-filter=DMRTUXB',refs[-2],refs[-1])}
with (OUT/'ANCESTRY.json').open('x',encoding='utf-8') as f:json.dump(extra,f,indent=2)
print(json.dumps({'diagnostics':results,'ancestry':extra},indent=2))
