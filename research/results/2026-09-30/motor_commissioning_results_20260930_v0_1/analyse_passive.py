"""Sealed-record observer only. No Loom imports, object constructors or replay."""
from pathlib import Path
import ast,csv,hashlib,json,math,struct,time,zlib
from datetime import datetime,timezone
import numpy as np

OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
PREP=ROOT/'motor_commissioning_preparation_20260930_v0_1';EX=PREP/'execution'
BASE=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
began=time.perf_counter()
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plain(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    return x
def save(name,obj):
    (OUT/name).write_text(json.dumps(plain(obj),indent=2,allow_nan=False)+'\n',encoding='utf8')
def csvsave(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(plain(rows))

# Read just the existing passive decoder definition, not its enclosing script.
decoder_file=ROOT/'nursery_0_design_20260930_v0_1/audit_exploration.py'
node=next(n for n in ast.parse(decoder_file.read_text(encoding='utf8')).body if isinstance(n,ast.FunctionDef) and n.name=='read_data')
U=struct.Struct('<Q');F=struct.Struct('<d')
exec(compile(ast.Module(body=[node],type_ignores=[]),str(decoder_file),'exec'))
schema_file=BASE/'loom_developmental/evidence.py'
schema=next(n.value for n in ast.parse(schema_file.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='NATIVE_FIELDS' for v in n.targets))
SL={};WIDTH=0
for name,width in ast.literal_eval(schema):SL[name]=slice(WIDTH,WIDTH+width);WIDTH+=width
cfg=json.loads((BASE/'configuration.json').read_bytes())
matrix=json.loads((PREP/'MATRIX.json').read_bytes())['cases']
raw_denominator=json.loads((EX/'DENOMINATOR.json').read_bytes())
assert raw_denominator['stop'] and not (EX/'lives/MC-FS-002-CURRENT').exists()
assert len(list((EX/'lives').iterdir()))==3

# Seal every available execution byte BEFORE metrics. Never edit the raw executor denominator.
files=[dict(path=p.relative_to(EX).as_posix(),bytes=p.stat().st_size,sha256=h(p),mtime_ns=p.stat().st_mtime_ns)
       for p in sorted(EX.rglob('*')) if p.is_file()]
assert not any(x['path'].endswith('.partial') for x in files)
custody=dict(utc=datetime.now(timezone.utc).isoformat(),kind='POST_STOP_AVAILABLE_EXECUTION_CUSTODY',
    files=files,bytes=sum(x['bytes'] for x in files),raw_denominator_sha256=h(EX/'DENOMINATOR.json'),
    authorization_sha256=h(EX/'JASON_AUTHORIZATION.json'),new_simulation=False)
save('EXECUTION_CUSTODY_SEAL.json',custody)
hashes={x['path']:x['sha256'] for x in files}
def rd(p):return read_data(p,hashes[p.relative_to(EX).as_posix()])
def stats(a):
    a=np.asarray(a,dtype=float)
    return dict(count=int(a.size),minimum=float(a.min()),p05=float(np.quantile(a,.05)),median=float(np.median(a)),
        mean=float(a.mean()),p95=float(np.quantile(a,.95)),maximum=float(a.max())) if a.size else None
def runs(mask,dt):
    z=np.r_[False,mask,False];s=np.flatnonzero(z[1:]&~z[:-1]);e=np.flatnonzero(~z[1:]&z[:-1]);t=np.r_[0,np.cumsum(dt)]
    return [dict(start_s=float(t[i]),end_s=float(t[j]),duration_s=float(t[j]-t[i]),end_censored=bool(j==len(dt))) for i,j in zip(s,e)]
def bouts(vf,dt,threshold):
    fw=runs(vf>threshold,dt);rv=runs(vf< -threshold,dt)
    fs=[r for r in fw if r['duration_s']>=.1-1e-9];rs=[r for r in rv if r['duration_s']>=.1-1e-9]
    seq=sorted([(r['start_s'],1) for r in fs]+[(r['start_s'],-1) for r in rs])
    return dict(threshold=threshold,forward=fw,reverse=rv,forward_qualifying_summary=stats([r['duration_s'] for r in fs]),
        reverse_qualifying_summary=stats([r['duration_s'] for r in rs]),forward_all_count=len(fw),reverse_all_count=len(rv),
        switches=sum(a[1]!=b[1] for a,b in zip(seq,seq[1:])),endpoint_bouts_are_right_censored=True)
def grid(p,size,offset=0.):
    cells=np.floor((p+offset)/size).astype(int);seen=set();previous=None;transitions=returns=0;growth=[]
    for point in cells:
        cell=tuple(map(int,point))
        if cell!=previous:
            if previous is not None:transitions+=1;returns+=cell in seen
            seen.add(cell);previous=cell
        growth.append(len(seen))
    return dict(cell_side=size,offset=offset,visited_cells=len(seen),cell_transitions=transitions,
        previously_visited_reentries=returns,reentry_fraction=returns/transitions if transitions else None),np.array(growth)
def correlations(angle,velocity):
    # Born state plus native rows. Exact 0.1-s indices, not resimulation.
    a=angle[::10];v=velocity[::10];speed=np.linalg.norm(v,axis=1);unit=v/np.maximum(speed[:,None],1e-300)
    out=[]
    for lag in (.1,.5,1,2,4,8,16):
        k=round(lag/.1)
        if k>=len(a):out.append(dict(lag_seconds=lag,heading_correlation=None,direction_correlation=None,valid_direction_pairs=0));continue
        ok=(speed[k:]>.01)&(speed[:-k]>.01)
        out.append(dict(lag_seconds=lag,heading_correlation=float(np.cos(a[k:]-a[:-k]).mean()),
            direction_correlation=float(np.einsum('ij,ij->i',unit[k:][ok],unit[:-k][ok]).mean()) if ok.any() else None,
            valid_direction_pairs=int(ok.sum())))
    return out

def kinematics(native,body):
    dt=native[:,SL['elapsed']][:,0];dur=float(dt.sum());q=native[:,SL['position']]
    p=np.vstack((body['position'],q));angle=np.r_[body['angle'],native[:,SL['angle']][:,0]]
    vv=native[:,SL['velocity']];velocity=np.vstack((body['velocity'],vv));omega=native[:,SL['omega']][:,0]
    speed=np.linalg.norm(vv,axis=1);vf=np.sum(vv*np.column_stack((np.cos(angle[1:]),np.sin(angle[1:]))),axis=1)
    length=np.cumsum(np.r_[0,np.linalg.norm(np.diff(p,axis=0),axis=1)])
    excursion=np.maximum.accumulate(np.linalg.norm(p-p[0],axis=1));displacement=float(np.linalg.norm(p[-1]-p[0]))
    grids={};growth={}
    for name,size,off in [('025',.25,0.),('100',1.,0.),('025_offset',.25,.125)]:
        grids[name],growth[name]=grid(p,size,off)
    ages=[]
    for age in sorted(set([x for x in (0.,10.,30.,60.,90.) if x<=dur+1e-8]+[round(dur,10)])):
        k=min(len(native),round(age/.01));d=float(np.linalg.norm(p[k]-p[0]))
        ages.append(dict(age_seconds=age,native_index=k,path_length=float(length[k]),maximum_excursion=float(excursion[k]),
            displacement=d,displacement_path_ratio=d/length[k] if length[k]>0 else None,
            coverage025=int(growth['025'][k]),coverage100=int(growth['100'][k]),coverage025_offset=int(growth['025_offset'][k])))
    u=native[:,SL['commands']];common=(u[:,0]+u[:,1])/2;diff=(u[:,1]-u[:,0])/2
    rms=lambda v:float(np.sqrt(np.sum(dt*v*v)/dur))
    avg=lambda v:float(np.sum(dt*v)/dur)
    rotate=cfg['body_radius']*abs(omega);active=(speed>.005)|(rotate>.005)
    summary=dict(duration_s=dur,native_steps=len(native),path_length=float(length[-1]),maximum_excursion=float(excursion[-1]),
        displacement=displacement,displacement_path_ratio=displacement/length[-1] if length[-1] else None,
        path_displacement_ratio=length[-1]/displacement if displacement else None,
        mean_speed=avg(speed),rms_speed=rms(speed),mean_abs_angular_speed=avg(abs(omega)),rms_angular_speed=rms(omega),
        heading_initial_radians=float(angle[0]),heading_final_radians=float(angle[-1]),
        heading_net_change_degrees=float(np.degrees(angle[-1]-angle[0])),heading_span_degrees=float(np.degrees(np.ptp(angle))),
        heading_total_absolute_rotation_degrees=float(np.degrees(np.abs(np.diff(angle)).sum())),
        forward_time_fraction=avg(vf>.01),reverse_time_fraction=avg(vf< -.01),
        predominantly_rotating_fraction=avg(active&(rotate>2*speed)),predominantly_translating_fraction=avg(active&(speed>2*rotate)),
        inactive_fraction=avg(~active),common_command_mean=avg(common),differential_command_mean=avg(diff),
        common_command_rms=rms(common),differential_command_rms=rms(diff),
        left_command_rms=rms(u[:,0]),right_command_rms=rms(u[:,1]),
        left_right_correlation=float(np.corrcoef(u.T)[0,1]),opposed_command_fraction=avg(u[:,0]*u[:,1]<0),
        mean_absolute_command=avg(np.abs(u).mean(axis=1)),grids=grids,
        bouts={str(t):bouts(vf,dt,t) for t in (.005,.01,.02)},persistence=correlations(angle,velocity),ages=ages)
    plot=dict(position=p,angle=angle,velocity=velocity,time=np.arange(len(p))*.01,path=length,excursion=excursion,
        coverage025=growth['025'],coverage100=growth['100'],commands=np.vstack((body['command'],u)),forward_velocity=np.r_[0,vf],
        reserves=np.vstack(([body['energy'],body['integrity']],native[:,SL['reserves']])),mover_rectangle=native[:,SL['mover_rectangle']])
    return summary,plot

def check_ledger(events):
    maximum=0.
    for r in events:
        tr=np.asarray(r['transfer']);renew=np.asarray(r['renewal_first'])+r['renewal_second']
        errors=((r['energy_after']-r['energy_before'])-(tr.sum()-r['expenditure']),
            np.max(abs(np.asarray(r['stock_after'])-r['stock_before']-renew+tr)),
            r['integrity_after']-r['integrity_before']-(r['repair']-r['damage']))
        maximum=max(maximum,*map(abs,errors));assert maximum<=cfg['arithmetic_tol']
    return maximum

def contacts(events,native):
    categories={name:dict(contact_records=0,impulse=0.,impact_impulse=0.,sustained_impulse=0.,damage=0.,
        contact_duration_s=0.,first_contact_time=None,last_contact_time=None,peak_instantaneous_impulse=0.,peak_sustained_force=0.) for name in ('wall','mover','source','repair','other')}
    by_collider={};compact=[]
    for r in events:
        seen=set()
        for c in r['contacts']:
            cid=c['collider'];kind=next((k for k in ('wall','mover','source','repair') if cid.startswith(k)),'other')
            seen.add(kind);x=categories[kind];imp=c['impulse'];duration=r['duration']
            damage=cfg['damage_per_impulse']*(imp if r['impact'] else max(0,imp-cfg['stress_threshold']*duration))
            x['contact_records']+=1;x['impulse']+=imp;x['damage']+=damage
            x['impact_impulse' if r['impact'] else 'sustained_impulse']+=imp
            if r['impact']:x['peak_instantaneous_impulse']=max(x['peak_instantaneous_impulse'],imp)
            else:x['peak_sustained_force']=max(x['peak_sustained_force'],imp/duration)
            begin=r['time']-duration
            if x['first_contact_time'] is None:x['first_contact_time']=begin
            x['last_contact_time']=r['time']
            by_collider[cid]=by_collider.get(cid,0.)+imp
            compact.append(dict(time=r['time'],duration=duration,collider=cid,impact=r['impact'],impulse=imp,damage=damage,
                position=r['body_position'],relative_speed=c['relative_speed']))
        for kind in seen:categories[kind]['contact_duration_s']+=r['duration']
    expense=sum(r['expenditure'] for r in events);damage=sum(r['damage'] for r in events);repair=sum(r['repair'] for r in events)
    transfer=np.sum([r['transfer'] for r in events],axis=0)
    dt=native[:,SL['elapsed']][:,0];basal=cfg['basal_cost']*float(dt.sum())
    effort=cfg['effort_cost']*float(np.sum(dt*np.abs(native[:,SL['commands']]).mean(axis=1)))
    assert abs(expense-basal-effort)<1e-11
    assert abs(sum(x['damage'] for x in categories.values())-damage)<1e-11
    return dict(categories=categories,impulse_by_collider=by_collider,total_impulse=sum(x['impulse'] for x in categories.values()),
        expenditure=expense,basal_expenditure=basal,effort_expenditure=effort,damage=damage,repair=repair,
        transfer_by_source=transfer,source_transfer=float(transfer.sum()),contact_event_rows=compact)

def coupling(waves,native):
    items=[]
    for wave in waves:
        d=wave['motor_coupling'];z=d['oscillator']+d['direct_feedback']+d['evoked']+d['current']
        tanh_gain=1-np.tanh(z)**2;att=d['attenuation_used'];gain=(1-att)*tanh_gain
        assert np.allclose(np.tanh(z),d['target'],rtol=0,atol=1e-14)
        assert np.array_equal(d['command'],native[wave['index']-1,SL['commands']])
        items.append(dict(index=wave['index'],age=wave['index']*.01,oscillator=d['oscillator'],direct=d['direct_feedback'],
            evoked=d['evoked'],current=d['current'],attenuation=att,total=z,tanh_gain=tanh_gain,
            gain_before_relaxation=gain,gain_next_native=(1-math.exp(-.1))*gain,command=d['command']))
    arrays={k:np.array([r[k] for r in items]) for k in ('oscillator','direct','evoked','current','attenuation','total','tanh_gain','gain_before_relaxation','gain_next_native')}
    summary={}
    for k,v in arrays.items():summary[k]=dict(distribution=stats(v),rms=float(np.sqrt(np.mean(v*v))))
    summary.update(recorded_wave_count=len(items),fraction_tanh_gain_below_point1=float(np.mean(arrays['tanh_gain']<.1)),
        fraction_attenuation_above_point95=float(np.mean(arrays['attenuation']>.95)),
        interpretation='recorded local sensitivity only; no perturbation, causal attribution or evidence of useful learning')
    return summary,items

results=[];boundary=[];age_rows=[];table=[];input_verifications=[]
for item in matrix:
    name=item['case_id'];store=EX/'lives'/name;process=name.split('-')[-1]
    if not store.exists():
        boundary.append(dict(case_id=name,status='NOT_STARTED_BATCH_STOP',native_steps=0,duration_s=0,metrics=None))
        results.append(dict(case_id=name,status='NOT_STARTED_BATCH_STOP',metrics=None));continue
    initial=rd(next(store.glob('*-initial.ld')))['engine']['attributes'];body=initial['body']['attributes']
    chunks=[];waves=[];events=[];t=0.;index=0;wave_index=0
    receipt=None
    if (store/'segment-000.json').exists():
        receipt=json.loads((store/'segment-000.json').read_bytes())
        assert receipt['complete'] and receipt['status']=='stage_complete'
        for r in receipt['files']:assert h(store/r['file'])==r['sha256']
        final=rd(store/receipt['final_checkpoint']['file'])['engine']['attributes']
        status='COMPLETE_90_SECONDS';chunk_paths=[store/r['file'] for r in receipt['chunks']]
    else:
        fault=json.loads((store/'failure-s000.json').read_bytes());tail=rd(store/'failure-tail-s000.ld')
        final=tail['engine']['attributes'];status='APPARATUS_FAILURE_PREFIX'
        assert final['native_index']==fault['native_index']==fault['last_recorded_index']==1025
        assert final['status']=='failure'
        chunk_paths=sorted(store.glob('chunk-*.ld'))
    for path in chunk_paths:
        d=rd(path);a=d['native'];assert d['first_index']==index+1 and d['last_index']==index+len(a) and d['start_time']==t
        for row in a:t+=float(row[SL['elapsed']][0]);index+=1;assert t==row[0]
        chunks.append(a);waves.extend(d['waves']);events.extend(d['events'])
    tail_count=0
    if receipt is None:
        a=tail['unclosed_native'];tail_count=len(a)
        for row in a:t+=float(row[SL['elapsed']][0]);index+=1;assert t==row[0]
        chunks.append(a);waves.extend(tail['unclosed_waves']);events.extend(tail['unclosed_events'])
    native=np.concatenate(chunks);assert native.shape==(index,WIDTH) and np.isfinite(native).all()
    assert index==final['native_index'] and t==final['time'] and len(waves)==final['organism']['attributes']['wave_count']
    for w in waves:wave_index+=1;assert w['wave']==wave_index and w['index']==wave_index*20
    assert int(native[:,SL['event_count']].sum())==len(events)
    assert np.array_equal(native[-1,SL['position']],final['body']['attributes']['position'])
    assert np.array_equal(native[-1,SL['reserves']],np.array([final['body']['attributes']['energy'],final['body']['attributes']['integrity']]))
    max_ledger=check_ledger(events)
    metric,plot=kinematics(native,body);physical=contacts(events,native);influence,detail=coupling(waves,native)
    physical.update(initial_reserves=[body['energy'],body['integrity']],final_reserves=native[-1,SL['reserves']])
    assert abs(physical['final_reserves'][0]-body['energy']-physical['source_transfer']+physical['expenditure'])<1e-11
    assert abs(physical['final_reserves'][1]-body['integrity']+physical['damage']-physical['repair'])<1e-11
    equal10,unused=kinematics(native[:1000],body)
    phys10=contacts([r for r in events if r['time']<=10+1e-8],native[:1000])
    result=dict(case_id=name,process=process,status=status,kinematics=metric,physical=physical,coupling=influence,
        common_predeclared_10_second_window=dict(kinematics=equal10,physical=phys10),
        verified_native_steps=index,verified_wave_count=len(waves),verified_event_count=len(events),
        ledger_max_error=max_ledger,raw_float_clock=t,nominal_age_seconds=index*.01,
        ordinary_stop_cause=None if receipt else fault['error'],has_closed_receipt=receipt is not None,
        closed_chunks_native_steps=index-tail_count,verified_failure_tail_native_steps=tail_count,
        active_wall_seconds=None if receipt is None else receipt['wall_seconds'])
    if process=='CURRENT':
        old_store=ROOT/'founder_initial_execution_20260930/lives/FS-001'
        old_receipt=json.loads((old_store/'segment-000.json').read_bytes())
        old=[]
        for r in old_receipt['chunks']:
            if r['last_index']>9000:break
            old.append(read_data(old_store/r['file'],r['sha256'])['native'])
        result['CURRENT_matches_preserved_FS001_all_9000_native_rows']=bool(np.array_equal(native,np.concatenate(old)))
        assert result['CURRENT_matches_preserved_FS001_all_9000_native_rows']
    results.append(result)
    boundary.append(dict(case_id=name,status=status,native_steps=index,duration_s=index*.01,has_closed_receipt=receipt is not None))
    for row in metric['ages']:age_rows.append(dict(case_id=name,**row))
    np.savez_compressed(OUT/(name+'_PASSIVE_PLOT_DATA.npz'),**plot)
    save(name+'_DETAILS.json',result);save(name+'_WAVE_COUPLING.json',detail)
    table.append(dict(case_id=name,status=status,duration_s=index*.01,path_length=metric['path_length'],maximum_excursion=metric['maximum_excursion'],
        displacement=metric['displacement'],displacement_path_ratio=metric['displacement_path_ratio'],coverage025=metric['grids']['025']['visited_cells'],
        reentry025_fraction=metric['grids']['025']['reentry_fraction'],forward_bout_median=(metric['bouts']['0.01']['forward_qualifying_summary'] or {}).get('median'),
        reverse_bout_median=(metric['bouts']['0.01']['reverse_qualifying_summary'] or {}).get('median'),switches=metric['bouts']['0.01']['switches'],
        common_command_rms=metric['common_command_rms'],differential_command_rms=metric['differential_command_rms'],
        energy_expenditure=physical['expenditure'],effort_expenditure=physical['effort_expenditure'],impulse=physical['total_impulse'],damage=physical['damage'],
        source_transfer=physical['source_transfer'],final_E=float(physical['final_reserves'][0]),final_I=float(physical['final_reserves'][1]),
        minimum_motor_local_gain=influence['gain_before_relaxation']['distribution']['minimum']))
    input_verifications.append(dict(case_id=name,native_rows=index,waves=len(waves),events=len(events),ledger_max_error=max_ledger,
        final_clock_matches=True,final_body_matches=True,tail_rows_verified=tail_count,closed_receipt=receipt is not None))

save('DENOMINATOR_RECONCILIATION.json',dict(raw_denominator=raw_denominator,cases=boundary,
    reason='Immutable executor row for failed case remains STARTED/0; reconciled from failure receipt and verified tail without editing it.',
    attempted_next_native_step=1026,complete_cases=2,interrupted_prefixes=1,unstarted_cases=6,no_retry=True,no_continuation=True))
save('PASSIVE_RESULTS.json',results);csvsave('AVAILABLE_CASE_METRICS.csv',table);csvsave('COVERAGE_AND_EXCURSION_GROWTH.csv',age_rows)
save('PASSIVE_VALIDATION.json',dict(status='PASS',checks=input_verifications,total_native_rows=sum(x['native_rows'] for x in input_verifications),
    execution_source_modified=False,new_simulation_steps=0,all_execution_file_hashes_still_match=all(h(EX/r['path'])==r['sha256'] for r in files),
    decoder_source_sha256=h(decoder_file),native_schema_source_sha256=h(schema_file),
    observer_seconds=time.perf_counter()-began,method='passive typed decoder returns class attributes as plain data; no Loom import/replay'))
print(json.dumps(plain(dict(boundary=boundary,metrics=table,observer_seconds=time.perf_counter()-began)),indent=2))
