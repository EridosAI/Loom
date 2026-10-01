"""Read the one closed A1 attempt. No replay, continuation or code correction."""
import copy,hashlib,json,math,pathlib,shutil,sys,time,traceback
from contextlib import ExitStack
from unittest.mock import patch
import numpy as np
S=pathlib.Path(__file__).resolve().parent
R=S.parent/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology';BASE=D/'artifacts/first-commissioning-A1-20260925-5f077481'
OUT=BASE/'read-only-review';TRAJ=BASE/'trajectory-001'
sys.path[:0]=[str(D),str(R)]
from loom_commissioning import authority,validators,runner,adapter,controllers
from loom_p import physics,prehistory
from loom_p.records import load_snapshot,state_hash,view
from loom_p.engine import Engine
from loom_p.chemistry import FieldSolver
import packet_checks
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(view(obj),f,indent=2,ensure_ascii=False,allow_nan=False)
def forbidden(*a,**k):raise AssertionError('Read-only results cannot advance a world')

def main():
    started=time.perf_counter()
    assert (BASE/'EXECUTION_RESULT.json').is_file(),'Wait for the sole attempt to stop'
    execution=authority.strict_loads((BASE/'EXECUTION_RESULT.json').read_bytes())
    assert execution['run_constructors_attempted']<=1
    shutil.copyfile(S/'read_results.py',OUT/'read_results.py')
    raw={str(p.relative_to(BASE)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in BASE.rglob('*') if p.is_file() and not p.is_relative_to(OUT)}
    write('RAW_EVIDENCE_BEFORE_ANALYSIS.json',raw)
    if not TRAJ.is_dir():
        write('NO_TRAJECTORY_REPORT.json',execution);return
    receipt=authority.strict_loads((TRAJ/'manifest.json').read_bytes())
    initial=load_snapshot(R/'INITIAL_A1.snapshot.json.gz')
    m=authority.strict_loads((BASE/'LAUNCHED_MANIFEST.json').read_bytes())
    assert authority.execution_sha256(m)=='a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc'
    authority.verify_approval_binding(m,m['execution_authority'])
    errors={};result={};final=None
    def attempt(name,fn):
        try:
            value=fn();result[name]=value;write(name+'.json',value);return value
        except Exception as error:
            errors[name]={'exception':repr(error),'traceback':traceback.format_exc()}
            write(name+'_ERROR.json',errors[name]);return None
    with ExitStack() as stack:
        for obj,name in ((Engine,'step'),(FieldSolver,'step'),(physics,'advance'),(physics,'account'),(prehistory,'prepare'),(runner.Run,'__init__'),(adapter,'step')):
            stack.enter_context(patch.object(obj,name,forbidden))
        verification=attempt('V1_POST_RECORD_VALIDATION',lambda:validators.verify_segment(TRAJ,replay=False))
        # Exact committed data only, even if its validity check reports a failure.
        native=validators.read_stream(TRAJ/'native.jsonl.gz')
        events=validators.read_stream(TRAJ/'events.jsonl.gz')
        actions=validators.read_stream(TRAJ/'controller.jsonl.gz')
        sensors=validators.read_stream(TRAJ/'sensor.jsonl.gz')
        waves=validators.read_stream(TRAJ/'wave.jsonl.gz')
        diagnostic=validators.read_stream(TRAJ/'diagnostics.jsonl.gz')
        accounting=attempt('V2_ACCOUNTING',lambda:packet_checks.v2(events,initial.c))
        observations=attempt('A1_OBSERVATIONS',lambda:packet_checks.a1_interpret(initial,native,events,initial.c))
        try:final,session,final_manifest=runner.load_restart(TRAJ/'final.restart.json.gz')
        except Exception as error:
            errors['final_restart']={'exception':repr(error),'traceback':traceback.format_exc()}
            write('FINAL_RESTART_READ_ERROR.json',errors['final_restart'])
        def v3():
            assert final is not None,'Final state not independently loadable'
            assert final_manifest==m==receipt['contract']
            assert state_hash(initial.organism)==state_hash(final.organism),'External inactive neural state changed'
            assert initial.organism.rng.counters==final.organism.rng.counters
            payload=authority.strict_loads((TRAJ/'sensor-display.json').read_bytes())
            controllers.validate_sensor_payload(payload)
            assert len(native)==len(sensors)==len(diagnostic)
            assert payload['history'][1:]==sensors
            assert len(waves)==0
            for action in actions:controllers.validate_privileged(action['inputs'])
            current=None;offset=0;held=initial.body.reserves.tolist();sampled=initial.time
            for n,s in zip(native,sensors):
                while offset<len(actions) and actions[offset]['native_index']<n['native_index']:
                    current=actions[offset];offset+=1
                assert current is not None and n['commands']==current['command'],'Delivered command differs from issued decision'
                assert n['native_index']==s['native_index'] and n['time']==s['time']
                assert np.concatenate(n['raw']).tolist()==s['raw']
                if n['native_index']%20==0 and n['status']!='terminal':held=n['reserves'];sampled=n['time']
                assert s['actual_EI']==held and s['EI_sample_time']==sampled
                assert n['mode']=='external_controller' and n['neural_state']=='inactive_newborn_not_P'
            assert session['field_updates']==session['advanced']==len(native)
            assert final.native_index==len(native) and state_hash(final)==receipt['final_state']
            return {'all_actual_controller_inputs_closed':True,'actual_native_commands_match_issued':True,
                'raw_sensor_rows_match_native':True,'held_EI_cadence_matches':True,'inactive_neural_RNG_unchanged':True,
                'initial_and_final_organism_sha256':state_hash(final.organism),'rng_counters':final.organism.rng.counters,
                'native_records':len(native),'controller_decisions':len(actions),'sensor_records':len(sensors),
                'wave_records':len(waves),'field_updates':session['field_updates'],'body_wave_samples':session['body_wave_samples'],
                'new_trajectories_or_replays':0}
        boundary=attempt('V3_BOUNDARY',v3)
    contact=[];intervals=[]
    for i,e in enumerate(events):
        matched=[x for x in e['contacts'] if x.get('source')==0 and x.get('collider')=='source-0']
        if not matched:continue
        contact.append((i,e,matched))
        if e['duration']>0:
            start=e['time']-e['duration'];end=e['time']
            if intervals and start<=intervals[-1]['end']+initial.c.event_time_tol:
                intervals[-1]['end']=end;intervals[-1]['supported_duration']+=e['duration'];intervals[-1]['last_event']=i
            else:intervals.append({'start':start,'end':end,'supported_duration':e['duration'],'first_event':i,'last_event':i})
    write('SOURCE_0_CONTACT_INTERVALS.json',{'intervals':intervals,'scope':'Existing event-time tolerance only; no minimum residence gate; all source contact events retained in A1_OBSERVATIONS.'})
    transfer=math.fsum(e['transfer'][0] for e in events)
    total_transfer=math.fsum(math.fsum(e['transfer']) for e in events)
    cost=math.fsum(e['expenditure'] for e in events)
    renewal=[math.fsum(e['renewal_first'][j]+e['renewal_second'][j] for e in events) for j in range(8)]
    windows=[] if observations is None else observations['all_fixed_windows']
    positives=[x for x in windows if x['positive_net_contact_interval']]
    negative_contact=[x for x in windows if x['complete_0_2_second_interval'] and x['source_0_positive_duration_contact'] and x['net_energy_sign']=='negative_resolved']
    forces=[float(x['force']) for _,e,xs in contact if e['duration']>0 for x in xs if 'force' in x]
    last_energy=(final.body.energy if final is not None else native[-1]['reserves'][0] if native else initial.body.energy)
    last_integrity=(final.body.integrity if final is not None else native[-1]['reserves'][1] if native else initial.body.integrity)
    last_stocks=(final.stocks.tolist() if final is not None else native[-1]['stocks'] if native else initial.stocks.tolist())
    source_debit=initial.stocks[0]+renewal[0]-last_stocks[0]
    credit=last_energy-initial.body.energy+cost
    transfer_allowance=(len(events)+1)*initial.c.arithmetic_tol+abs(source_debit-transfer)
    summary={'authority_sha256':execution['approved_execution_sha256'],'apparatus_checkpoint':execution['apparatus_checkpoint'],
        'attempts':execution['run_constructors_attempted'],'stop_reason':receipt['status'],'stop_cause':receipt.get('stop_cause'),
        'record_complete':receipt['complete'],'simulated_seconds':receipt.get('final_time',execution['time']),
        'native_records':len(native),'event_records':len(events),'command_decisions':len(actions),'wave_records':len(waves),
        'geometric_approach_achieved':None if observations is None else observations['geometric_contact_locus_reached'],
        'minimum_source_surface_gap':None if observations is None else observations['minimum_source_surface_gap'],
        'certified_source_contact':bool(contact),'first_contact_time':None if not contact else contact[0][1]['time'],
        'positive_duration_contact_seconds':math.fsum(e['duration'] for _,e,_ in contact if e['duration']>0),
        'contact_interval_count':len(intervals),'sustained_force_min':min(forces) if forces else None,'sustained_force_max':max(forces) if forces else None,
        'source_0_transfer':transfer,'source_0_debit_from_stock_and_renewal':float(source_debit),'source_0_debit_minus_transfer':float(source_debit-transfer),
        'all_source_transfer':total_transfer,'body_credit_from_energy_and_cost':credit,'body_credit_minus_transfer':credit-total_transfer,
        'transfer_sign_allowance':transfer_allowance,'transfer_interpretation':'positive_resolved' if transfer>transfer_allowance else 'exact_zero' if transfer==0 else 'unresolved',
        'total_expenditure':cost,'initial_energy':initial.body.energy,'final_energy':last_energy,'whole_attempt_energy_delta':last_energy-initial.body.energy,
        'initial_integrity':initial.body.integrity,'final_integrity':last_integrity,'source_0_final_stock':last_stocks[0],'source_0_renewal':renewal[0],
        'complete_fixed_windows':sum(x['complete_0_2_second_interval'] for x in windows),'partial_windows':sum(not x['complete_0_2_second_interval'] for x in windows),
        'positive_net_contact_window_count':len(positives),'first_positive_net_contact_window':positives[0] if positives else None,
        'negative_net_contact_window_count':len(negative_contact),
        'maximum_accounting_residual':None if accounting is None else accounting['maximum_ledger_residual'],
        'V1_record_validation':verification,'V3':boundary,'analysis_errors':errors,'trajectory_failure':execution['failure'],
        'physical_nonviability':receipt['status']=='terminal','terminal_dimension':receipt.get('terminal_dimension'),
        'recorder_wall_seconds':receipt.get('wall_seconds'),'whole_process_wall_seconds':execution['wall_seconds_including_preflight'],
        'recorded_uncompressed_bytes':receipt.get('uncompressed_bytes'),'trajectory_file_bytes':sum(p.stat().st_size for p in TRAJ.iterdir() if p.is_file()),
        'read_only_analysis_wall_seconds':time.perf_counter()-started,
        'claim':'One external physical witness only. No P pass/fail, learning/survival efficacy or universal physical-impossibility conclusion.'}
    for name,row in raw.items():
        p=BASE/name;assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Raw evidence altered during analysis'
    summary['raw_evidence_unchanged_during_analysis']=True
    write('A1_RESULT_SUMMARY.json',summary)
    print(json.dumps(view(summary),indent=2),flush=True)

if __name__=='__main__':main()
