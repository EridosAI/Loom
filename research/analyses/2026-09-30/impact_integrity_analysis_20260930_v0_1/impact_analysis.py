"""Read-only recorded physics and detached immediate receivers; never world stepping."""
import csv, hashlib, json, math, sys, time
from pathlib import Path
import numpy as np
from scipy.special import expit

HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
PREV=ROOT/'founder_expansion_execution_20260930'; OLD=ROOT/'founder_initial_execution_20260930'
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
sys.path.insert(0,str(D));sys.path.insert(0,str(PREV))
from loom_developmental import codec,evidence
from loom_developmental.runner import identity,canonical,file_hash
from loom_developmental.replay import reconstruct
from loom_p.geometry import fixtures,gap_normal,mover
import execute_authorized_expansion as execution

def read(p): return json.loads(Path(p).read_bytes())
def plain(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [plain(x) for x in v]
    return v
def write(p,v):
    with (HERE/p).open('x',encoding='utf-8') as f:json.dump(plain(v),f,separators=(',',':'),allow_nan=False)
def table(p,rows):
    if not rows:return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (HERE/p).open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        for r in rows:w.writerow({k:json.dumps(plain(v),separators=(',',':')) if isinstance(v,(list,dict,np.ndarray)) else v for k,v in r.items()})
def norm(x):return float(np.linalg.norm(x))
def base(name):return OLD if int(name[3:])<13 else PREV
def receipt(name):
    store=base(name)/'lives'/name
    if name!='FS-060':return store,read(store/'segment-000.json')
    f=read(PREV/'INTERRUPTION_CUSTODY_SEAL.json')['files']
    cps=sorted((r for r in f if r['file'].startswith('checkpoint-')),key=lambda r:r['file'])
    return store,dict(initial_checkpoint=next(r for r in cps if r['file'].endswith('-initial.ld')),
        chunks=sorted((r for r in f if r['file'].startswith('chunk-')),key=lambda r:r['file']))
def initial(name):
    store,r=receipt(name);q=r['initial_checkpoint'];return codec.read(store/q['file'],q['sha256'])['engine']
def fixture(e,key,t):return next(f for f in fixtures(e.c,t,e.phase) if f['id']==key)
def gap_series(e,key,data):
    p=data['position'];c=e.c
    if key.startswith('wall-'):
        f=fixture(e,key,0);a=f['axis'];out=f['sign']*(p[:,a]-f['boundary'])-c.body_radius
        normal=np.zeros_like(p);normal[:,a]=f['sign'];return out,normal
    if key.startswith('source-'):
        f=fixture(e,key,0);delta=p-f['centre'];length=np.linalg.norm(delta,axis=1)
        return length-c.body_radius-f['radius'],delta/length[:,None]
    rect=data['mover_rectangle'] if key=='mover' else np.tile(fixture(e,key,0)['rect'],(len(p),1))
    near=np.column_stack((np.clip(p[:,0],rect[:,0],rect[:,1]),np.clip(p[:,1],rect[:,2],rect[:,3])))
    delta=p-near;length=np.linalg.norm(delta,axis=1)
    assert np.all(length>0),'Recorded body centre inside solid: do not guess normals'
    return length-c.body_radius,delta/length[:,None]
def idx(data,t,side='left'):return int(np.searchsorted(data['time'].ravel(),t,side=side))
def path_at(data,t):return 0. if t<=0 else float(np.interp(t,data['time'].ravel(),data['path']))

def contact_rows(name,e,native,event_groups):
    c=e.c;rows=[];damaged=[];event_id=0;checks=[];prior=e.body
    previous_pos=prior.position.copy();previous_angle=prior.angle;velocity=prior.velocity.copy();omega=prior.omega
    for n,events in zip(native,event_groups):
        native_index=len(checks)+1;err=0.
        for ev in events:
            event_id+=1;dt=float(ev['duration']);t=float(ev['time']);pos=np.asarray(ev['body_position']);angle=float(ev['body_angle'])
            pre_v=velocity.copy();pre_o=omega;pre_pos=previous_pos.copy();pre_a=previous_angle
            pre_err=err
            if dt>0:
                velocity=(pos-previous_pos)/dt;omega=(angle-previous_angle)/dt
                err=8*np.finfo(float).eps*max(1.,norm(pos),norm(previous_pos),abs(angle),abs(previous_angle))/dt
            else:
                velocity=velocity+sum((float(ct['impulse'])*np.asarray(ct['normal'])/c.body_mass for ct in ev['contacts']),np.zeros(2))
            if ev['damage']>0 or ev['repair']>0:
                damaged.append(dict(life_id=name,event_index=event_id,native_index=native_index,time=t,duration=dt,
                    damage=ev['damage'],restoration=ev['repair'],integrity_before=ev['integrity_before'],integrity_after=ev['integrity_after'],
                    energy_before=ev['energy_before'],energy_after=ev['energy_after'],colliders=[z['collider'] for z in ev['contacts']]))
            allocations=[]
            for ct in ev['contacts']:
                key=ct['collider'];normal=np.asarray(ct['normal']);tangent=np.array([-normal[1],normal[0]])
                f=fixture(e,key,t-dt);fv=f['velocity'];arm=-c.body_radius*normal
                vrel=pre_v-fv;surf_rel=pre_v+pre_o*np.array([-arm[1],arm[0]])-fv
                j=float(ct['impulse']);damage=c.damage_per_impulse*(j if ev['impact'] else max(j-c.stress_threshold*dt,0.))
                allocations.append(damage)
                precise=pre_err<=1e-6
                r=dict(life_id=name,collider=key,collider_type=f['kind'],material=int(ct['material']),native_index=native_index,event_index=event_id,
                    onset=t-dt,end=t,duration=dt,instant=bool(ev['impact']),event_kind=ev.get('event_kind','sustained_or_free'),
                    position_start=pre_pos,position_end=pos.copy(),orientation=pre_a,omega=pre_o if precise else None,
                    velocity_before=pre_v if precise else None,velocity_after=velocity.copy() if err<=1e-6 else None,
                    velocity_uncertainty=pre_err,normal=normal,tangent=tangent,collider_velocity=fv,
                    closing_normal_velocity=-float(vrel@normal) if precise else None,
                    tangential_centre_velocity=float(vrel@tangent) if precise else None,
                    tangential_surface_velocity=float(surf_rel@tangent) if precise else None,
                    command=n[evidence.SLICES['commands']].copy(),impulse=j,force=float(ct['force']) if 'force' in ct else None,
                    damage=damage,event_integrity_before=ev['integrity_before'],event_integrity_after=ev['integrity_after'],
                    restoration=float(ev['repair']) if ct['material']==3 and sum(z['material']==3 for z in ev['contacts'])==1 else None,
                    joint_event_restoration=float(ev['repair']),relative_surface_speed_after_recorded=float(ct['relative_speed']))
                rows.append(r)
            assert abs(sum(allocations)-ev['damage'])<1e-12
            previous_pos=pos.copy();previous_angle=angle
        actual=n[evidence.SLICES['velocity']];actual_o=float(n[evidence.SLICES['omega']][0])
        error=max(norm(velocity-actual),abs(omega-actual_o));assert error<=max(1e-7,err*4),(name,native_index,error,err)
        checks.append(error)
        velocity=actual.copy();omega=actual_o;previous_pos=n[evidence.SLICES['position']].copy();previous_angle=float(n[evidence.SLICES['angle']][0])
    return rows,damaged,dict(native_checks=len(checks),maximum_algebra_native_endpoint_error=max(checks),
        no_dynamics_integrated=True,uncertain_contact_velocity_rows=sum(x['velocity_before'] is None for x in rows))

def partition(rows,data,gaps,threshold,temporal_only=False):
    result=[]
    for key in sorted({r['collider'] for r in rows}):
        chosen=[r for r in rows if r['collider']==key and (r['impulse']>0 or r['duration']>0)]
        group=[];end=None
        for r in chosen:
            split=False
            if end is not None and r['onset']-end>=.1-1e-10:
                a=idx(data,end,'right');b=idx(data,r['onset'],'left')
                split=temporal_only or (b>a and float(gaps[key][a:b].max())>threshold)
            if split:result.append(group);group=[]
            group.append(r);end=max(end if end is not None else r['end'],r['end'])
        if group:result.append(group)
    return sorted(result,key=lambda g:(g[0]['onset'],g[0]['collider']))

def summarize_group(name,number,g,data,gaps):
    first,last=g[0],g[-1];key=first['collider'];start=first['onset'];end=max(r['end'] for r in g)
    forces=[r['force'] for r in g if r['force'] is not None];duration=sum(r['duration'] for r in g)
    instant=[r['impulse'] for r in g if r['instant']]
    onset_index=first['native_index'];a=max(0,idx(data,start-.2));b=max(a+1,idx(data,start,'left'))
    speed=data['velocity'][a:b];normal=np.asarray(first['normal']);mvr=first['collider_velocity']
    after=idx(data,end,'right');exitrow=min(after,len(data['time'])-1)
    out=dict(life_id=name,episode=number,collider=key,collider_type=first['collider_type'],onset=start,end=end,
        span=end-start,contact_duration=duration,event_contact_rows=len(g),first_native=onset_index,last_native=last['native_index'],
        first_event=first['event_index'],last_event=last['event_index'],onset_velocity=first['velocity_before'],
        onset_closing_velocity=first['closing_normal_velocity'],onset_tangential_centre=first['tangential_centre_velocity'],
        onset_tangential_surface=first['tangential_surface_velocity'],onset_orientation=first['orientation'],onset_omega=first['omega'],
        onset_commands=first['command'],pre_0_2s_command_mean=np.mean(data['commands'][a:b],axis=0),
        pre_0_2s_closing_velocity_mean=float(np.mean(-(speed-mvr)@normal)),
        pre_0_2s_energy=float(data['reserves'][a:b,0].mean()),pre_0_2s_integrity=float(data['reserves'][a:b,1].mean()),
        impulse=sum(r['impulse'] for r in g),instant_impulse_sum=sum(instant),instant_impulse_peak=max(instant,default=0.),
        sustained_force_peak=max(forces) if forces else None,
        sustained_force_time_mean=sum(r['impulse'] for r in g if not r['instant'])/duration if duration else None,
        damage=sum(r['damage'] for r in g),instant_damage=sum(r['damage'] for r in g if r['instant']),
        sustained_damage=sum(r['damage'] for r in g if not r['instant']),restoration=sum(r['restoration'] or 0 for r in g),
        integrity_before=first['event_integrity_before'],integrity_after=last['event_integrity_after'],
        exit_velocity=last['velocity_after'],exit_native_velocity=data['velocity'][exitrow],exit_native_time=float(data['time'][exitrow,0]),
        exit_direction=math.atan2(last['velocity_after'][1],last['velocity_after'][0]) if last['velocity_after'] is not None and norm(last['velocity_after'])>1e-12 else None)
    for seconds in (1,5,30):
        z=gaps[key][after:idx(data,end+seconds,'right')]
        out[f'clearance_next_{seconds}s_min']=float(z.min()) if len(z) else None
        out[f'clearance_next_{seconds}s_max']=float(z.max()) if len(z) else None
    return out

def physical(name,native,event_groups,e):
    fields=('time','elapsed','position','angle','velocity','omega','commands','forces','reserves','mover_rectangle','mover_velocity')
    data={k:native[:,evidence.SLICES[k]] for k in fields}
    data['path']=np.cumsum(np.linalg.norm(np.diff(np.vstack((e.body.position,data['position'])),axis=0),axis=1))
    rows,consequences,validation=contact_rows(name,e,native,event_groups)
    gaps={};normals={}
    for key in sorted({r['collider'] for r in rows}):gaps[key],normals[key]=gap_series(e,key,data)
    groups=partition(rows,data,gaps,.05);episodes=[summarize_group(name,i+1,g,data,gaps) for i,g in enumerate(groups)]
    bouts=[summarize_group(name,i+1,g,data,gaps) for i,g in enumerate(partition(rows,data,gaps,0,True))]
    for ep in episodes:
        later=[q for q in episodes if q['collider']==ep['collider'] and q['onset']>ep['end']]
        q=later[0] if later else None
        ep['next_same_episode']=q['episode'] if q else None
        ep['next_same_contact_delay']=q['onset']-ep['end'] if q else None
        ep['native_path_until_next_same_contact']=path_at(data,q['onset'])-path_at(data,ep['end']) if q else None
        ep['followup_without_next_same_contact']=float(data['time'][-1,0])-ep['end'] if not q else None
    first_damage=min(r['time']-r['duration'] for r in consequences if r['damage']>0)
    exposure=[];probes=[]
    for kind,collection in [('episode',episodes),('bout',bouts)]:
        for ep in collection:
            end=max(1,idx(data,ep['onset'],'left'));start=max(1,end-19)
            probes.append(dict(life_id=name,name=f'{name}-{kind}-{ep["episode"]:03d}-approach',kind=kind,collider=ep['collider'],
                related_episode=ep['episode'],event_onset=ep['onset'],first_native=start,last_native=end))
    for key in gaps:
        for begin in range(int(first_damage//30)*30,int(float(data['time'][-1,0]))+1,30):
            lo=max(float(begin),first_damage);hi=min(float(begin+30),float(data['time'][-1,0]));a=idx(data,lo);b=idx(data,hi,'right')
            if b<=a:continue
            j=a+int(np.argmin(gaps[key][a:b]));last=j+1
            actual=[r for r in rows if r['collider']==key and r['onset']>=lo and r['end']<=hi]
            exposure.append(dict(life_id=name,collider=key,start=lo,end=hi,minimum_clearance=float(gaps[key][j]),
                closest_native=last,closest_time=float(data['time'][j,0]),maximum_clearance=float(gaps[key][a:b].max()),
                path_length=path_at(data,hi)-path_at(data,lo),time_within_0_25=float(data['elapsed'][a:b,0][gaps[key][a:b]<=.25].sum()),
                time_within_1=float(data['elapsed'][a:b,0][gaps[key][a:b]<=1].sum()),
                damage=sum(r['damage'] for r in actual),contact_duration=sum(r['duration'] for r in actual),
                episode_onsets=sum(ep['collider']==key and lo<=ep['onset']<hi for ep in episodes),
                position_at_closest=data['position'][j],orientation_at_closest=float(data['angle'][j,0]),
                commands_at_closest=data['commands'][j],velocity_at_closest=data['velocity'][j]))
            probes.append(dict(life_id=name,name=f'{name}-{key}-ageblock-{begin:03d}',kind='fixed_ageblock_closest',collider=key,
                age_block_start=lo,age_block_end=hi,first_native=max(1,last-19),last_native=last))
    rates=[]
    for label,lo,hi in [('before_first_injury',0.,first_damage),('after_first_injury',first_damage,float(data['time'][-1,0]))]:
        a=idx(data,lo);b=idx(data,hi,'right');path=path_at(data,hi)-path_at(data,lo)
        for key in gaps:
            count=sum(ep['collider']==key and lo<=ep['onset']<hi for ep in episodes)
            rates.append(dict(life_id=name,period=label,collider=key,start=lo,end=hi,path_length=path,episode_onsets=count,
                episodes_per_second=count/(hi-lo) if hi>lo else None,episodes_per_path=count/path if path>0 else None,
                within_0_25_seconds=float(data['elapsed'][a:b,0][gaps[key][a:b]<=.25].sum()),
                within_1_seconds=float(data['elapsed'][a:b,0][gaps[key][a:b]<=1].sum()),
                minimum_clearance=float(gaps[key][a:b].min()) if b>a else None))
    sensitivity={str(th):len(partition(rows,data,gaps,th)) for th in (.01,.05,.1)}
    write(name+'_CONTACT_RECORDS.json',rows);table(name+'_CONTACT_RECORDS.csv',rows)
    write(name+'_EPISODES.json',episodes);table(name+'_EPISODES.csv',episodes);table(name+'_TEMPORAL_BOUTS.csv',bouts)
    write(name+'_CONSEQUENCES.json',consequences);table(name+'_EXPOSURE_BLOCKS.csv',exposure);write(name+'_EXPOSURE_BLOCKS.json',exposure)
    table(name+'_BEFORE_AFTER_RATES.csv',rates)
    np.savez_compressed(HERE/(name+'_RECORDED_NATIVE.npz'),**data)
    write(name+'_PHYSICAL_SUMMARY.json',dict(life_id=name,first_damage=first_damage,episodes=len(episodes),bouts=len(bouts),
        grouping_sensitivity=sensitivity,validation=validation,damage=sum(r['damage'] for r in rows),
        contact_records=len(rows),zero_impulse_zero_duration_records=sum(r['duration']==0 and r['impulse']==0 for r in rows),
        colliders=sorted(gaps),probes=probes,derived_only=True))
    return episodes,bouts,probes,exposure,rates

def audit():
    started=time.perf_counter();execution.source_gate();runtime=hashlib.sha256(canonical(identity())).hexdigest();assert runtime==execution.RUNTIME
    seal=read(PREV/'COMBINED_DENOMINATOR_SEALED.json');prior=read(PREV/'analysis/ALL_SIXTY_AB.json');lookup={r['life_id']:r for r in prior}
    final=read(PREV/'FINAL_DELIVERY_VERIFICATION.json');ref=next(x for x in final['analysis_files'] if x['path']=='analysis/ALL_SIXTY_AB.json')
    assert file_hash(PREV/ref['path'])==ref['sha256']
    expected={}
    for b in (OLD,PREV):
        for f in read(b/'EVIDENCE_ARCHIVE_MANIFEST.json')['files']:
            if f['path'].startswith(('execution/lives/','execution/shared-assets/')):expected[str(b/f['path'][len('execution/'):])]=f['sha256']
    checked=[]
    for path,sha in expected.items():assert file_hash(path)==sha;checked.append(dict(path=path,sha256=sha))
    write('INPUT_CUSTODY.json',dict(runtime_sha256=runtime,combined_seal_sha256=file_hash(PREV/'COMBINED_DENOMINATOR_SEALED.json'),
        methods_sha256=file_hash(HERE/'METHODS.md'),request_sha256=file_hash(HERE/'JASON_REQUEST.txt'),source_checkpoint=execution.CHECKPOINT,
        P_commit=execution.P,scientific_files=checked))
    allrows=[];allprobes=[];allepisodes=[];allbouts=[];allexposure=[];allrates=[]
    for roster in seal['roster']:
        name=roster['life_id'];store,r=receipt(name)
        if roster['complete']:assert file_hash(store/'segment-000.json')==roster['receipt_sha256']
        retain=lookup[name]['damage']>0;native=[];groups=[];damage=repair=0.;contacts=events=0
        for f in r['chunks']:
            d=codec.read(store/f['file'],f['sha256']);offset=0
            if retain:native.append(d['native'])
            for n in d['native']:
                count=int(n[evidence.SLICES['event_count']][0]);ev=d['events'][offset:offset+count];offset+=count
                damage+=sum(z['damage'] for z in ev);repair+=sum(z['repair'] for z in ev)
                events+=count;contacts+=sum(len(z['contacts']) for z in ev)
                if retain:groups.append(ev)
            assert offset==len(d['events'])
        assert abs(damage-lookup[name]['damage'])<1e-12
        assert bool(damage>0)==retain,'Unlisted damaged life found; stop instead of excluding'
        allrows.append(dict(life_id=name,complete=roster['complete'],damage=damage,restoration=repair,event_count=events,
            contact_records=contacts,native_steps=roster['native_steps'],preserved_prefix_only=not roster['complete']))
        if retain:
            ep,bo,pr,ex,ra=physical(name,np.vstack(native),groups,initial(name));allepisodes+=ep;allbouts+=bo;allprobes+=pr;allexposure+=ex;allrates+=ra
        print(json.dumps(dict(life_id=name,damage=damage,verified=True,physical_analysis=retain)),flush=True)
    write('DAMAGED_LIFE_AUDIT.json',dict(roster=allrows,damaged_lives=[r['life_id'] for r in allrows if r['damage']>0],
        complete_roster=60,FS060_prefix_only=True,wall_seconds=time.perf_counter()-started,world_steps=0))
    table('ALL_BEHAVIORAL_EPISODES.csv',allepisodes);table('ALL_TEMPORAL_BOUTS.csv',allbouts)
    table('ALL_EXPOSURE_BLOCKS.csv',allexposure);table('ALL_BEFORE_AFTER_RATES.csv',allrates)
    write('PROBE_MANIFEST.json',dict(methods_sha256=file_hash(HERE/'METHODS.md'),selection='All predefined physical anchors; no omission result used for selection',
        windows=allprobes,world_steps_authorized=0,not_an_execution_authority=True))

def controls(c,rd,omit=False):
    learned=rd['learned'].copy()
    if omit:learned[1]*=0
    weighted=rd['need'][:,None]*(learned+rd['exploration']);g=c.group_count
    return np.concatenate((expit(weighted[:,:g].sum(axis=0)),c.current_max/2*np.tanh(weighted[:,g:g+2]).sum(axis=0),
        expit(c.attenuation_bias+weighted[:,g+2:g+4].sum(axis=0))))

def receivers():
    started=time.perf_counter();audit=read(HERE/'DAMAGED_LIFE_AUDIT.json');manifest=read(HERE/'PROBE_MANIFEST.json')
    results=[];window_results=[];alignments=[];wave_summary=[]
    for name in audit['damaged_lives']:
        store,r=receipt(name);e0=initial(name);c=e0.c;g=c.group_count
        data=dict(np.load(HERE/(name+'_RECORDED_NATIVE.npz')));probes=[p for p in manifest['windows'] if p['life_id']==name]
        first_damage=read(HERE/(name+'_PHYSICAL_SUMMARY.json'))['first_damage']
        wanted={i for p in probes for i in range(p['first_native'],p['last_native']+1)}
        held=e0.organism.regulator.output_diagnostic;old_theta=e0.organism.regulator.theta[1].copy();old_ref=e0.organism.regulator.reference[1].copy()
        summaries=[];samples={};wave_operands=[];consequences=read(HERE/(name+'_CONSEQUENCES.json'))
        align_native={int(math.ceil(z['native_index']/20))*20 for z in consequences}
        align_native|={max(20,(p['last_native']//20)*20) for p in probes}
        def observe(index,e,diag):
            nonlocal held,old_theta,old_ref
            rd=held;o=e.organism;motor=o.motor.diagnostic
            if index in wanted:
                baseline=controls(c,rd);alternative=controls(c,rd,True)
                assert np.array_equal(baseline,rd['controls'])
                assert np.array_equal(baseline[g:g+2],motor['current'])
                assert np.array_equal((1-baseline[-2:])*motor['tendency'],motor['command'])
                alt_target=np.tanh(motor['oscillator']+motor['direct_feedback']+motor['evoked']+alternative[g:g+2])
                alpha=-np.expm1(-e.last_native['elapsed']/c.tau_motor)
                alt_tendency=motor['tendency']+alpha*(alt_target-motor['target'])
                alt_command=(1-alternative[-2:])*alt_tendency
                j=index-1
                reserves=e0.body.reserves if j==0 else data['reserves'][j-1]
                angle=e0.body.angle if j==0 else float(data['angle'][j-1,0])
                position=e0.body.position if j==0 else data['position'][j-1]
                body_velocity=e0.body.velocity if j==0 else data['velocity'][j-1]
                coefficients=.5*(.2+.8*reserves[0])*np.array([.4+.6*reserves[1],.7+.3*reserves[1]])
                actual_force=coefficients*motor['command'];alt_force=coefficients*alt_command
                samples[index]=dict(native_index=index,time=e.time,input_time=e.time-e.last_native['elapsed'],
                    command=motor['command'].copy(),without_learned_I_command=alt_command,
                    delta_command=motor['command']-alt_command,actual_force=actual_force,without_learned_I_force=alt_force,
                    controls=baseline,without_learned_I_controls=alternative,delta_controls=baseline-alternative,
                    learned_I=rd['learned'][1].copy(),exploration_I=rd['exploration'][1].copy(),I_need=float(rd['need'][1]),
                    actual_body_feature_input=rd['Bv_body'].copy(),associative_feature_input=rd['Bq_q'].copy(),
                    motor_evocation=motor['evoked'].copy(),direct_feedback=motor['direct_feedback'].copy(),oscillator=motor['oscillator'].copy(),
                    position=position.copy(),angle=angle,velocity=body_velocity.copy(),reserves=reserves.copy(),
                    angular_acceleration_delta=c.lever*float((actual_force[1]-alt_force[1])-(actual_force[0]-alt_force[0]))/c.body_inertia)
                if index<math.floor(first_damage/.01):
                    assert np.array_equal(alt_command,motor['command']),'Nonzero learned I before first integrity experience'
            if e.last_wave is not None:
                reg=o.regulator;credit=reg.credit_diagnostic;nr=reg.output_diagnostic
                update=reg.theta[1]-old_theta
                assert np.allclose(update,credit['learning'][1]+credit['reference_force'][1]+credit['projection'][1],rtol=0,atol=1e-16)
                z=dict(life_id=name,native_index=index,time=e.time,actual_integrity=float(e.body.integrity),
                    old_I_mean=float(credit['old_body_mean'][1]),I_trend=float(credit['trend'][1]),
                    eligibility_norm=norm(credit['eligibility'][1]),previous_I_exploration_draw_norm=norm(credit['previous_xi'][1]),
                    previous_features_norm=norm(credit['previous_phi']),I_learning_norm=norm(credit['learning'][1]),
                    I_reference_force_norm=norm(credit['reference_force'][1]),I_projection_norm=norm(credit['projection'][1]),
                    I_bank_before_norm=norm(old_theta),I_bank_after_norm=norm(reg.theta[1]),I_bank_applied_update_norm=norm(update),
                    I_reference_before_norm=norm(old_ref),I_reference_after_norm=norm(reg.reference[1]),
                    learned_I_norm=norm(nr['learned'][1]),exploration_I_norm=norm(nr['exploration'][1]),
                    actual_body_feature_norm=norm(nr['Bv_body']),associative_feature_norm=norm(nr['Bq_q']))
                summaries.append(z)
                if index in align_native:
                    wave_operands.append(dict(summary=z,old_theta=old_theta.copy(),old_reference=old_ref.copy(),
                        eligibility=credit['eligibility'][1].copy(),learning=credit['learning'][1].copy(),reference_force=credit['reference_force'][1].copy(),
                        projection=credit['projection'][1].copy(),theta=reg.theta[1].copy(),reference=reg.reference[1].copy(),
                        previous_xi=credit['previous_xi'][1].copy(),previous_phi=credit['previous_phi'].copy(),
                        learned_I=nr['learned'][1].copy(),regulatory_controls=nr['controls'].copy(),without_learned_I_controls=controls(c,nr,True)))
                old_theta=reg.theta[1].copy();old_ref=reg.reference[1].copy()
            held=o.regulator.output_diagnostic
        start=time.perf_counter();replay=reconstruct(store,fields=False,deep=False,callback=observe);final=replay.pop('engine')
        exact=codec.write(HERE/(name+'_ALIGNED_I_OPERANDS.ld'),wave_operands,level=1)
        records=codec.write(HERE/(name+'_RECEIVER_NATIVE.ld'),list(samples.values()),level=1)
        bywave={z['native_index']:z for z in summaries}
        for event in consequences:
            following=int(math.ceil(event['native_index']/20))*20;prior=following-20
            z=dict(event)
            for label,k in [('prior',prior),('next',following)]:
                z[label+'_handoff_native']=k if k in bywave else None
                if k in bywave:z.update({label+'_'+key:v for key,v in bywave[k].items() if key not in ('life_id','native_index')})
            alignments.append(z)
        for p in probes:
            points=[samples[i] for i in range(p['first_native'],p['last_native']+1)];details=[]
            for z in points:
                f=fixture(e0,p['collider'],z['input_time']);gap,normal=gap_normal(z['position'],c.body_radius,f)
                forward=np.array([np.cos(z['angle']),np.sin(z['angle'])]);left=np.array([-forward[1],forward[0]])
                actual_into=-float(normal@forward)*float(np.sum(z['actual_force']))
                omitted_into=-float(normal@forward)*float(np.sum(z['without_learned_I_force']))
                details.append(dict(native_index=z['native_index'],time=z['time'],gap=gap,
                    actual_into_surface_force=actual_into,without_learned_I_into_surface_force=omitted_into,
                    learned_I_into_force_delta=actual_into-omitted_into,
                    closing_velocity=-float(normal@(z['velocity']-f['velocity'])),
                    heading_outward_projection=float(normal@forward),heading_outward_acceleration_tendency=float(normal@left)*z['angular_acceleration_delta'],
                    attenuation_delta_mean=float(z['delta_controls'][-2:].mean()),command_delta_norm=norm(z['delta_command']),
                    actual_axial_force=float(z['actual_force'].sum()),without_I_axial_force=float(z['without_learned_I_force'].sum())))
            result=dict(p,normal_command_mean=np.mean([z['command'] for z in points],axis=0),
                without_learned_I_command_mean=np.mean([z['without_learned_I_command'] for z in points],axis=0),
                command_delta_mean=np.mean([z['delta_command'] for z in points],axis=0),
                maximum_command_delta_norm=max(z['command_delta_norm'] for z in details),
                learned_I_into_force_delta_mean=float(np.mean([z['learned_I_into_force_delta'] for z in details])),
                learned_I_into_force_delta_min=min(z['learned_I_into_force_delta'] for z in details),
                learned_I_into_force_delta_max=max(z['learned_I_into_force_delta'] for z in details),
                closing_velocity_mean=float(np.mean([z['closing_velocity'] for z in details])),
                attenuation_delta_mean=float(np.mean([z['attenuation_delta_mean'] for z in details])),
                heading_outward_acceleration_tendency_mean=float(np.mean([z['heading_outward_acceleration_tendency'] for z in details])),
                actual_axial_force_mean=float(np.mean([z['actual_axial_force'] for z in details])),
                minimum_clearance=min(z['gap'] for z in details),normal_minus_omission=True,
                scope='Immediate frozen motor receiver only; no body trajectory, support/history propagation or long-horizon benefit')
            window_results.append(result);write(p['name']+'_RECEIVER.json',dict(summary=result,native=details))
        wave_summary+=summaries
        item=dict(life_id=name,reconstruction=replay,endpoint_P_sha256=codec.digest(final.organism),
            native_probes=len(samples),windows=len(probes),aligned_operands=exact,receiver_records=records,wall_seconds=time.perf_counter()-start)
        results.append(item);write(name+'_RECONSTRUCTION_CHECK.json',item)
        table(name+'_I_WAVES.csv',summaries)
        print(json.dumps(dict(life_id=name,receiver_windows=len(probes),reconstruction='PASS',world_steps=0)),flush=True)
    table('I_CREDIT_BANK_EXPRESSION_ALIGNMENT.csv',alignments);write('I_CREDIT_BANK_EXPRESSION_ALIGNMENT.json',alignments)
    table('ALL_I_WAVES.csv',wave_summary);table('PASSIVE_LEARNED_I_OMISSIONS.csv',window_results);write('PASSIVE_LEARNED_I_OMISSIONS.json',window_results)
    write('RECEIVER_CHECK_COMPLETION.json',dict(lives=results,window_count=len(window_results),wall_seconds=time.perf_counter()-started,
        world_steps=0,fields_evolved=False,alternative_trajectories=0,learned_I_omission_only=True))

if __name__=='__main__':
    {'audit':audit,'receivers':receivers}[sys.argv[1]]()
