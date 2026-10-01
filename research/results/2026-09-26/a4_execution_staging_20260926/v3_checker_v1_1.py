"""V3 v1.1: immutable record analysis. No Loom imports, Engine or control calls."""
import argparse,math
from evidence import *
VERSION='1.1.0'
SENSOR_KEYS={'schema','raw_labels','history','own_commands','annotations','availability'}
ROW_KEYS={'native_index','time','raw','actual_EI','EI_sample_time'}
PRIVILEGED_KEYS={'position','angle','velocity','omega','reserves','commands','geometry','mover_phase','mover_velocity','stocks','contacts','time'}
LABELS=[f'{k}_{i}' for k,n in [('light',10),('chemistry',4),('contact',8),('proprioception',7)] for i in range(n)]
def require(ok,message):
    if not ok:raise AssertionError(message)
def flatten(raw):return [v for group in raw for v in group]
def align(native,sensors,diagnostics,initial):
    require(bool(sensors),'Missing initial sensor envelope')
    envelope=sensors[0]
    require(set(envelope)==SENSOR_KEYS and envelope['schema']==1,'First sensor entry is not the reviewed display envelope')
    require(envelope['raw_labels']==LABELS and envelope['availability']=='paused','Initial display labels/availability differ')
    require(envelope['own_commands']==envelope['annotations']==[],'Initial display contains unexplained commands/annotations')
    require(len(envelope['history'])==1,'Initial display must contain exactly the initial record')
    first=envelope['history'][0]
    require(set(first)==ROW_KEYS,'Initial history row schema')
    require(first['native_index']==initial['native_index']==0 and first['time']==initial['time']==0,'Initial time/index anchor')
    require(first['raw']==flatten(initial['raw']),'Initial raw/snapshot mismatch')
    reserves=[initial['body']['energy'],initial['body']['integrity']]
    require(first['actual_EI']==reserves and first['EI_sample_time']==0,'Initial E/I anchor')
    rows=sensors[1:]
    # Identified above by schema, contents and initial snapshot, not discarded by position alone.
    require(len(rows)==len(native)==len(diagnostics),'Per-step counts differ after explicit envelope identification')
    lookup={r['native_index']:r for r in rows}
    require(len(lookup)==len(rows),'Duplicate sensor native index')
    require(set(lookup)=={n['native_index'] for n in native},'Index-set mismatch')
    previous_time=0.;previous_raw=list(initial['raw']);held=reserves;sampled=0.;mapping=[]
    cumulative=0.
    for ordinal,(n,d,r) in enumerate(zip(native,diagnostics,rows),1):
        require(set(r)==ROW_KEYS,'Per-step sensor schema leak')
        require(n['native_index']==r['native_index']==d['native_index']==ordinal,'Index progression/mapping mismatch')
        require(lookup[n['native_index']]==r,'Independent index join differs from sequence join')
        require(n['time']==r['time']==d['endpoint_time'] and n['time']>previous_time,'Endpoint time mismatch')
        cumulative+=n['elapsed']
        require(abs(cumulative-n['time'])<=1e-10,'Independent elapsed-time progression mismatch')
        require(0<n['elapsed']<=initial['c']['native_dt']+1e-12,'Invalid native elapsed')
        require(d['input_time']==previous_time,'Diagnostic start time mismatch')
        require(d['raw_step_start']==previous_raw and d['raw_endpoint']==n['raw'],'Diagnostic start/endpoint raw mismatch')
        require(flatten(n['raw'])==r['raw'] and len(r['raw'])==29 and all(math.isfinite(v) for v in r['raw']),'Raw sensor/native mismatch')
        if ordinal%20==0 and n['status']!='terminal':held=n['reserves'];sampled=n['time']
        require(r['actual_EI']==held and r['EI_sample_time']==sampled,'E/I hold cadence mismatch')
        require(n['mode']==d['mode']=='external_controller' and n['neural_state']=='inactive_newborn_not_P','External mode label mismatch')
        require(set(d)=={'class','native_index','input_time','endpoint_time','raw_step_start','raw_endpoint','mode','selection','neural_scope'},'External diagnostics contain extra neural information')
        mapping.append({'sensor_stream_entry':ordinal,'native_stream_row':ordinal-1,'diagnostic_stream_row':ordinal-1,
            'native_index':ordinal,'start_time':previous_time,'endpoint_time':n['time'],'EI_sample_time':sampled})
        previous_time=n['time'];previous_raw=n['raw']
    return envelope,rows,mapping

def validate_inputs(actions,native,initial):
    held=None;offset=0;delivered=0
    for a in actions:
        p=a['inputs'];require(set(p)==PRIVILEGED_KEYS,'Controller input schema leak')
        require(a['actor']=='external_controller' and a['controller']=='waypoint','Wrong controller label')
        require(a['hold_native_steps']==10 and len(a['command'])==2 and all(math.isfinite(v) and abs(v)<=1 for v in a['command']),'Invalid issued command record')
        i=a['native_index'];require(i%10==0 and p['time']==a['time'],'Decision timestamp/index')
        old=native[i-1] if i else {'position':initial['body']['position'],'angle':initial['body']['angle'],
            'velocity':initial['body']['velocity'],'omega':initial['body']['omega'],
            'reserves':[initial['body']['energy'],initial['body']['integrity']],
            'commands':initial['body']['command'],'stocks':initial['stocks'],'time':initial['time']}
        for k in ('position','angle','velocity','omega','reserves','commands','stocks','time'):
            require(p[k]==old[k],f'Controller input does not match recorded decision-boundary {k}')
        require(p['mover_phase']==initial['phase'],'Controller phase mismatch')
        for f in p['geometry']:
            specific={'wall':{'axis','sign','boundary'},'disk':{'centre','radius'},'rect':{'rect'}}
            require(f.get('kind') in specific and set(f)=={'id','kind','velocity'}|specific[f['kind']],'Controller geometry schema leak')
        for c in p['contacts']:require(set(c)=={'normal','force','impulse'},'Controller contact schema leak')
    require([a['native_index'] for a in actions]==list(range(0,len(native),10)),'Decision cadence mismatch')
    for n in native:
        while offset<len(actions) and actions[offset]['native_index']<n['native_index']:
            held=actions[offset];offset+=1
        require(held is not None and 1<=n['native_index']-held['native_index']<=10,'No unique command ownership')
        require(n['commands']==held['command'],'Issued/delivered command differs')
        delivered+=1
    return {'closed_controller_inputs':len(actions),'delivered_command_rows':delivered,
        'controller_command_function_calls':0,'last_hold_consumed_steps':len(native)-actions[-1]['native_index'],
        'last_hold_pending_steps':10-(len(native)-actions[-1]['native_index'])}

def run(e):
    initial_wrapper=e.snapshot('initial');final_wrapper=e.snapshot('final')
    start=snapshot_data(initial_wrapper);finish=snapshot_data(final_wrapper)
    initial=start['engine'];final=finish['engine'];session=finish['session']
    native=e.stream('native');sensors=e.stream('sensor');diagnostics=e.stream('diagnostics');actions=e.stream('controller')
    envelope,rows,mapping=align(native,sensors,diagnostics,initial)
    inputs=validate_inputs(actions,native,initial)
    display=e.json('evidence/trajectory-001/sensor-display.json')
    require(set(display)==SENSOR_KEYS and display['raw_labels']==LABELS and display['schema']==1,'Final display schema')
    require(display['history']==envelope['history']+rows,'Final display/full sensor history differs')
    require(display['own_commands']==[{'time':a['time'],'command':a['command']} for a in actions],'Display own-command journal differs')
    require(display['annotations']==[] and display['availability']=='paused','Unexpected display annotations/status')
    require(display==session['sensor']['payload'],'Final snapshot sensor payload differs')
    organism=packed_attr(dict(initial_wrapper['state']['$dict'])['engine'],'organism')
    organism_hash=digest(canonical(organism));rng=initial['organism']['rng']
    checked=[]
    for name in sorted(n for n in e.z.namelist() if n.startswith('evidence/trajectory-001/') and n.endswith('.restart.json.gz')):
        snap=json.loads(gzip.decompress(e.z.read(name)));data=snapshot_data(snap)
        engine_packed=dict(snap['state']['$dict'])['engine']
        require(packed_attr(engine_packed,'organism')==organism,'Inactive organism changed at checkpoint')
        require(data['engine']['organism']['rng']==rng,'Full RNG checkpoint state differs')
        require(snap['manifest']==initial_wrapper['manifest']==final_wrapper['manifest'],'Manifest differs across checkpoints')
        checked.append({'file':name,'native_index':data['engine']['native_index'],'time':data['engine']['time'],'organism_sha256':organism_hash})
    for n in native:require(n['random_counters']==rng['counters'],'Native RNG counters changed')
    require(not e.stream('wave') and not e.stream('scientific_observations'),'Unexpected neural/scientific rows')
    require(session['advanced']==session['field_updates']==len(native)==final['native_index'],'Final update counters differ')
    require(session['body_wave_samples']==sum(n['native_index']%20==0 and n['status']!='terminal' for n in native),'Body handoff counter differs')
    require(session['hold_remaining']==inputs['last_hold_pending_steps'] and session['decision']==actions[-1],'Pending issued hold differs')
    receipt=e.json('evidence/trajectory-001/manifest.json')
    final_engine=dict(final_wrapper['state']['$dict'])['engine']
    require(digest(canonical(final_engine))==receipt['final_state'],'Final packed-engine hash differs')
    for k,field in [('position','position'),('angle','angle'),('velocity','velocity'),('omega','omega'),('commands','command'),('forces','force')]:
        require(native[-1][k]==final['body'][field],'Final body/native differs: '+k)
    require(native[-1]['reserves']==[final['body']['energy'],final['body']['integrity']] and native[-1]['stocks']==final['stocks'],'Final reserves/stocks differ')
    require(native[-1]['raw']==list(final['raw']),'Final raw differs')
    return {'version':VERSION,'status':'V3 COMPLETED — checks support the reviewed boundary claim',
        'analysis_of':'Original A1 only; not a new trajectory result','evidence_sha256':e.zip_sha256,
        'checker_sha256':filehash(__file__),'alignment':'Explicit initial display envelope anchored to snapshot at index/time 0; subsequent sensor entry k joins native/diagnostic index k at endpoint time. Diagnostic input_time/raw_step_start join index k-1. Independent index-set and cumulative-elapsed checks agree.',
        'native_records':len(native),'sensor_entries':len(sensors),'diagnostic_records':len(diagnostics),
        'initial_envelopes':1,'mapped_endpoint_rows':len(mapping),'EI_updates':session['body_wave_samples'],
        'controller':inputs,'inactive_organism_sha256':organism_hash,'checkpoints':checked,
        'native_rng_counter_comparisons':len(native),'neural_wave_rows':0,'simulation_steps':0,
        'engine_instances':0,'research_module_imports':0,'physical_replays':0,
        'limitations':['Evidence-level validation with source semantics; no physical replay or new runtime instrumentation.',
            'Full neural/RNG state compared at all 11 saved checkpoints; native RNG counters compared on every row. No assertion of observing unrecorded transient memory states.'],
        'old_analysis_relationship':'Supersedes only the incomplete V3 analysis conclusion; old checker, error and finding files remain byte-identical inside the original ZIP.',
        'mapping':mapping}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=pathlib.Path,default=DEFAULT);p.add_argument('--output',type=pathlib.Path,default=ROOT/'V3_RESULT_v1_1.json');a=p.parse_args()
    evidence=Evidence(a.evidence)
    try:result=run(evidence)
    except Exception as error:
        result={'version':VERSION,'status':'V3 REMAINS UNRESOLVED — '+str(error),'checker_sha256':filehash(__file__),'evidence_sha256':evidence.zip_sha256}
        write(a.output,result);raise
    write(a.output,result);print(json.dumps({k:v for k,v in result.items() if k!='mapping'},indent=2))
