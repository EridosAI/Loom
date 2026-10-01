"""Read-only bounded review of this batch's saved evidence; no trajectory replay.

Only runs after EXECUTION_RESULT exists. Does not call a controller, Engine.step,
adapter.step, prehistory generation, Run or load_restart. Scalar algebra checks
the recorded commands against the frozen law, without producing actuator work.
"""
from pathlib import Path
import csv
import datetime
import gzip
import hashlib
import json
import math
import sys
import time

S=Path(__file__).resolve().parent
ROOT=S.parent
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
R=ROOT/'exports/2026-09-29-B1-minimal-apparatus-a8cdd75'
OUT=S/'run-001'
REPORT=S/'review'
sys.path.insert(0,str(D))
from loom_p.records import unpack,strict_bytes,state_hash
from loom_commissioning.authority import strict_loads,execution_sha256
from loom_commissioning.validators import validate_ledger,validate_native_sequence,validate_stop
from loom_commissioning.controllers import LABELS,ROW_KEYS

def read(p):return strict_loads(Path(p).read_bytes())
def check(ok,why):
    if not ok:raise ValueError(why)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def stream(p):
    with gzip.open(p,'rt',encoding='utf-8') as f:
        for line in f:yield strict_loads(line)
def write(p,value):
    with Path(p).open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
def restart(p):
    data=strict_loads(gzip.decompress(Path(p).read_bytes()))
    check(hashlib.sha256(strict_bytes(data['state'])).hexdigest()==data['sha256'],'restart internal checksum')
    state=unpack(data['state']);e=state['engine'];e.validate_state()
    return e,state['session'],data['manifest']
def deadline():check(time.perf_counter()-START<1800,'read-only reporting time limit')

def review_case(case):
    deadline(); directory=OUT/'cases'/case
    receipt=read(directory/'manifest.json');m=receipt['contract']
    arm=m['execution']['procedure']['protocol']['reference_arm']
    for name,v in receipt.get('files',{}).items():
        p=directory/name
        check(p.stat().st_size==v['bytes'] and sha(p)==v['sha256'],'saved record identity: '+case+'/'+name)
    initial,begin,m0=restart(directory/'initial.restart.json.gz')
    final,finish,m1=restart(directory/'final.restart.json.gz')
    check(m==m0==m1,'snapshot/receipt manifest mismatch')
    prepared=read(R/'cases'/case/'MANIFEST.json')
    check(execution_sha256(m)==execution_sha256(prepared),'saved execution identity mismatch')
    check(state_hash(initial)==m['initial_state'] and state_hash(final)==receipt['final_state'],'state identity mismatch')
    check(begin['reference_state']=={'mode':'SEEK','release_count':0} and begin['decision'] is None,'memory not reset')
    check(state_hash(initial.organism)==state_hash(final.organism),'inactive P state changed')
    n=list(stream(directory/'native.jsonl.gz'))
    events=list(stream(directory/'events.jsonl.gz'))
    physical=finish['sensor']['payload']
    sensor=list(stream(directory/'sensor.jsonl.gz'))
    check(sensor[0]==begin['sensor']['payload'] and sensor[1:]==physical['history'][1:],'physical sensor history mismatch')
    check(physical['raw_labels']==LABELS and physical['annotations']==[],'physical sensory schema')
    check(len(physical['history'])==len(n)+1,'missing physical sensory row')
    validate_native_sequence(n,initial,final,m)
    validate_stop(receipt['status'],final,m)
    maximum=validate_ledger(events,initial.c.arithmetic_tol)
    check(finish['advanced']==finish['field_updates']==len(n),'step/field cadence mismatch')
    for k,row in enumerate(physical['history']):
        check(set(row)==ROW_KEYS and row['native_index']==k,'sensor row schema/index')
        expected_raw=[float(v) for block in (initial.raw if k==0 else n[k-1]['raw']) for v in block]
        check(row['raw']==expected_raw,'saved sensor differs from physical raw')
        sample=(k//20)*20
        if k==final.native_index and final.status=='terminal' and k%20==0:sample-=20
        ei=initial.body.reserves.tolist() if sample==0 else n[sample-1]['reserves']
        sample_time=0.0 if sample==0 else n[sample-1]['time']
        check(row['actual_EI']==ei and row['EI_sample_time']==sample_time,'EI sample/hold mismatch')
    traces=[];prior={'mode':'SEEK','release_count':0};commands=[];boundary=True
    labels=LABELS if arm=='FULL' else [s for s in LABELS if not s.startswith('chemistry_')]
    kept=list(range(29)) if arm=='FULL' else [i for i,s in enumerate(LABELS) if not s.startswith('chemistry_')]
    for number,a in enumerate(stream(directory/'controller.jsonl.gz')):
        deadline();idx=a['native_index']
        check(idx==number*10 and a['hold_native_steps']==10,'command index/hold mismatch')
        check(a['actor']=='external_controller' and a['controller']=='automated_raw_reference','controller identity')
        check(a['execution_sha256']==execution_sha256(m) and a['case_deadline']==30,'command authority/deadline mismatch')
        check(a['annotation']=='' and a['stage'] is None,'unexpected feedback channel')
        check(a['reference_state_before']==prior,'reference state continuity')
        b=0.;p4=None;C=None
        if arm=='SENSORY-FREE':
            check(a['inputs'] is None,'feedback in sensory-free input')
            expected=[.30,.30];after={'mode':'SEEK','release_count':0}
        else:
            payload=a['inputs']
            check(set(payload)=={'raw_labels','history','own_commands'} and payload['raw_labels']==labels,'forbidden reference input')
            check(len(payload['history'])==idx+1,'not complete causal input prefix')
            check(payload['own_commands']==commands,'own-command prefix mismatch')
            for k,row in enumerate(payload['history']):
                source=physical['history'][k]
                expected_row=dict(source,raw=[source['raw'][i] for i in kept])
                check(row==expected_row,'input differs from allowlisted physical prefix')
            rows=payload['history'][-10:]
            if arm=='FULL':
                ids=[labels.index('chemistry_'+str(j)) for j in range(4)]
                check(all(0<=row['raw'][j]<1 for row in rows for j in ids),'invalid receptor inversion')
                q=[math.fsum(.05*row['raw'][j]/(1-row['raw'][j]) for row in rows)/len(rows) for j in ids]
                left=(q[2]+q[3])/2;right=(q[0]+q[1])/2
                b=(left-right)/(left+right+1e-12)
            C=max(row['raw'][labels.index('contact_'+str(j))] for row in rows for j in (7,0,1))
            p4=rows[-1]['raw'][labels.index('proprioception_4')]
            after=dict(prior)
            if prior['mode']=='SEEK' and C>=.05:after={'mode':'HOLD','release_count':0}
            elif prior['mode']=='HOLD':
                count=prior['release_count']+1 if C<.02 else 0
                after={'mode':'SEEK','release_count':0} if count==3 else {'mode':'HOLD','release_count':count}
            d=.30/(1+4*abs(b));turn=max(-.40,min(.40,2*b-.20*p4))
            expected=[.05,.05] if after['mode']=='HOLD' else [d-turn,d+turn]
        check(a['command']==expected and a['reference_state_after']==after,'recorded command/law arithmetic mismatch')
        check(a['time']==physical['history'][idx]['time'],'decision time mismatch')
        for row in n[idx:idx+10]:check(row['commands']==a['command'],'applied hold differs from issued pair')
        commands.append({'time':a['time'],'command':a['command']})
        traces.append(dict(time=a['time'],native_index=idx,left=a['command'][0],right=a['command'][1],
            imbalance=b,p4=p4,front_contact_window=C,mode_before=prior['mode'],mode_after=after['mode'],release_count=after['release_count']))
        prior=after
    check(prior==finish['reference_state'] and commands==physical['own_commands'],'final reference/command history mismatch')
    check(len(traces)==receipt['records'].get('controller',0),'controller record count')
    for kind in ('native','events','diagnostics','sensor','wave','scientific_observations'):
        count=len(n) if kind=='native' else len(events) if kind=='events' else len(sensor) if kind=='sensor' else sum(1 for _ in stream(directory/(kind+'.jsonl.gz')))
        check(count==receipt['records'].get(kind,0),'stream count mismatch: '+kind)
    transfers=[math.fsum(e['transfer']) for e in events]
    gross=math.fsum(transfers);expense=math.fsum(e['expenditure'] for e in events)
    damage=math.fsum(e['damage'] for e in events);repair=math.fsum(e['repair'] for e in events)
    debit=math.fsum(math.fsum(float(x) for x in e['stock_before'])+math.fsum(e['renewal_first'])+math.fsum(e['renewal_second'])-math.fsum(e['stock_after']) for e in events)
    credit=math.fsum((e['energy_after']-e['energy_before'])+e['expenditure'] for e in events)
    tolerance=initial.c.arithmetic_tol
    # Conservative accumulated bound from the already-established per-record tolerance.
    uncertainty=len(events)*tolerance
    source_events=[e for e in events if any('source' in c for c in e['contacts'])]
    productive_events=[e for e in events if math.fsum(e['transfer'])>tolerance]
    for e in productive_events:
        for index,amount in enumerate(e['transfer']):
            if amount>tolerance:check(any(c.get('source')==index for c in e['contacts']),'transfer without actual source contact')
    contact_duration=math.fsum(e['duration'] for e in source_events)
    result={'case_id':case,'start':case.split('-')[2],'arm':arm,'status':receipt['status'],'complete_record':receipt['complete'],
      'stop_cause':receipt.get('stop_cause'),'error':receipt.get('error'),'native_steps':len(n),'commands':len(traces),
      'simulated_seconds':final.time,'completed_30_seconds':final.native_index==3000 and receipt['status']=='administrative_cutoff' and receipt['complete'],
      'terminal_dimension':final.terminal_dimension,'wall_seconds':receipt['wall_seconds'],
      'initial_EI':initial.body.reserves.tolist(),'final_EI':final.body.reserves.tolist(),
      'initial_state_sha256':state_hash(initial),'final_state_sha256':state_hash(final),
      'source_contact':bool(source_events),'source_contact_duration':contact_duration,
      'first_source_contact_time':min((e['time']-e['duration'] for e in source_events),default=None),
      'first_resolved_transfer_event_endpoint':min((e['time'] for e in productive_events),default=None),
      'gross_transfer':gross,'gross_debit_reconstructed':debit,'gross_credit_reconstructed':credit,
      'source_transfer_by_index':[math.fsum(e['transfer'][j] for e in events) for j in range(len(initial.stocks))],
      'expenditure':expense,'damage':damage,'repair':repair,
      'contact_colliders':sorted({c['collider'] for e in events for c in e['contacts']}),
      'total_contact_impulse':math.fsum(c['impulse'] for e in events for c in e['contacts']),
      'ledger_records':len(events),'ledger_max_residual':maximum,'ledger_per_record_tolerance':tolerance,
      'conservative_accumulated_accounting_bound':uncertainty,
      'resolved_productive':bool(source_events and productive_events and min(gross,debit,credit)>uncertainty),
      'feedback_changed_commands':arm!='SENSORY-FREE' and len({(t['left'],t['right']) for t in traces})>1,
      'nonbaseline_commands':sum([t['left'],t['right']]!=[.30,.30] for t in traces),
      'hold_decisions':sum(t['mode_after']=='HOLD' for t in traces),
      'hold_transitions':[t['time'] for t in traces if t['mode_before']!=t['mode_after']],
      'all_checks_passed':True,'physical_replay':False,'controller_execution_during_review':False,
      'controller_boundary_verified':boundary,'P_state_inactive_unchanged':True,
      'native_field_and_EI_cadence_verified':True,'reset_and_recorded_law_verified':True,
      'artifact_bytes':sum(p.stat().st_size for p in directory.iterdir() if p.is_file()),'receipt_sha256':sha(directory/'manifest.json')}
    write(REPORT/(case+'.json'),result)
    with (REPORT/(case+'-command-trace.csv')).open('x',newline='',encoding='utf-8') as f:
        if traces:
            writer=csv.DictWriter(f,fieldnames=list(traces[0]));writer.writeheader();writer.writerows(traces)
    return result

def main():
    execution=read(OUT/'EXECUTION_RESULT.json')
    REPORT.mkdir(exist_ok=False)
    write(REPORT/'REVIEW_START.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'read_only_budget_seconds':1800,'saved_records_only':True,'script_sha256':sha(__file__)})
    rows=[];failures=[]
    for case in execution['authorized_order']:
        if case not in execution['attempted']:
            rows.append({'case_id':case,'disposition':'NOT EXECUTED — declared batch stop'});continue
        try:rows.append(review_case(case))
        except Exception as error:
            import traceback
            failures.append({'case_id':case,'error':repr(error),'traceback':traceback.format_exc()})
            rows.append({'case_id':case,'disposition':'PRESERVED — saved-data verification unresolved','error':repr(error)})
        print(json.dumps({'reviewed':case,'checks_passed':rows[-1].get('all_checks_passed',False)}),flush=True)
    witnesses=[]
    for start in ('S1','S2','S3'):
        f=next(x for x in rows if x['case_id']==f'B1-MINIMAL-{start}-FULL')
        null=next(x for x in rows if x['case_id']==f'B1-MINIMAL-{start}-SENSORY-FREE')
        if (f.get('all_checks_passed') and f.get('resolved_productive') and f.get('feedback_changed_commands')
            and null.get('all_checks_passed') and null.get('completed_30_seconds') and null.get('gross_transfer')==0):
            witnesses.append(start)
    result={'checkpoint':execution['checkpoint'],'cases':rows,'verification_failures':failures,
        'closure_witness_starts':witnesses,'closure':'BOUNDED B1 CLOSURE SATISFIED' if witnesses else 'B1 UNRESOLVED BY THIS EXECUTION',
        'batch_stop':execution['batch_stop'],'review_wall_seconds':time.perf_counter()-START,
        'physical_replay':False,'new_controller_execution':False,'old_human_B1_accessed':False,
        'no_P_or_Base_World_modification':True}
    write(REPORT/'BOUNDED_RESULTS.json',result)
    print(json.dumps({'closure':result['closure'],'witness_starts':witnesses,'verification_failures':len(failures)}),flush=True)

if __name__=='__main__':
    START=time.perf_counter();main()
