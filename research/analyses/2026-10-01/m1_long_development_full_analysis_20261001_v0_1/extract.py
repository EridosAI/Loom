"""Read sealed arrays once. Write only derivative data beneath this directory."""
from common import *
import gzip,time

def main():
    (OUT/'cache').mkdir(exist_ok=True);(OUT/'raw').mkdir(exist_ok=True)
    records=[]
    for number in range(1,13):
        life=f'RS-M1-{number:03d}';dest=OUT/'cache'/life
        if dest.with_suffix('.json').exists():
            records.append(json.loads(dest.with_suffix('.json').read_bytes()));continue
        store=EX/'lives'/life;details=json.loads((OLD/(life+'_DETAILS.json')).read_bytes())
        initial=attrs(rd(next(store.glob('pilot-*-pilot-initial.ld')))['engine'])
        b=attrs(initial['body']);n=details['kinematics']['native_steps']
        native=np.lib.format.open_memmap(str(dest)+'_native.npy',mode='w+',dtype=np.float64,shape=(n,WIDTH))
        lists={};t=0.;idx=0;eventsum=np.zeros(4);ledger_error=0.;eventcount=0;bins={};impacts=[]
        event_columns=['time','duration','expenditure','damage','repair','energy_before','energy_after','integrity_before','integrity_after']+[f'transfer_{s}' for s in range(8)]
        with gzip.open(OUT/'raw'/(life+'_physical_events.csv.gz'),'wt',newline='',encoding='utf8') as ef:
            ew=csv.writer(ef);ew.writerow(event_columns)
            for file in sorted(store.glob('chunk-*.ld')):
                v=rd(file);assert v['first_index']==idx+1 and v['start_time']==t
                a=v['native'];native[idx:idx+len(a)]=a
                for row in a:t+=float(row[1]);assert t==row[0]
                idx+=len(a);assert idx==v['last_index']
                for w in v['waves']:
                    d=w['motor_coupling'];m=w['map_update_use'];wd=w['map_write_decay']
                    x={k:w[k] for k in ('time','index','wave','q','psi','packets','controls','learned','exploration','need','credit_trend','pool_opening','regulator_bank_norm','regulator_reference_norm','regulator_eligibility_norm','regulator_learning_norm','regulator_reference_force_norm','sensory_shared_norm','sensory_fine_norm','sensory_reference_norm','sensory_activity_norm','body_mean')}
                    x.update({k:d[k] for k in ('oscillator','direct_feedback','evoked','current','target','tendency','command','attenuation_used')})
                    x.update(H_norm=norm(m[:,:4]),H_branch_norm=m[:,:4],use_branch=m[:,4:],write_branch=wd[:,:4],decay_branch=wd[:,4:],H_use_mean=m[:,4:].mean(),H_use_max=m[:,4:].max(),write_norm=norm(wd[:,:4]),decay_norm=norm(wd[:,4:]))
                    for k,val in x.items():lists.setdefault(k,[]).append(val)
                for e in v['events']:
                    eventcount+=1;tr=np.asarray(e['transfer']);ew.writerow([e[k] for k in event_columns[:9]]+tr.tolist())
                    eventsum+=np.array([tr.sum(),e['expenditure'],e['damage'],e['repair']])
                    errs=[e['energy_after']-e['energy_before']-tr.sum()+e['expenditure'],e['integrity_after']-e['integrity_before']+e['damage']-e['repair'],np.max(abs(np.array(e['stock_after'])-e['stock_before']-e['renewal_first']-e['renewal_second']+tr))]
                    ledger_error=max(ledger_error,*map(abs,errs))
                    for c in e['contacts']:
                        if e['impact'] and c['impulse']>0:
                            impacts.append(dict(life=life,time=e['time'],collider=c['collider'],impulse=c['impulse'],damage=cfg['damage_per_impulse']*c['impulse'],isolated_normal_closing_speed=c['impulse']/cfg['body_mass'] if len(e['contacts'])==1 else None,relative_surface_speed=c['relative_speed'],x=e['body_position'][0],y=e['body_position'][1],angle=e['body_angle'],normal_x=c['normal'][0],normal_y=c['normal'][1]))
        native.flush();assert idx==n and t==details['age']
        assert ledger_error<cfg['arithmetic_tol']
        physical=details['physical'];assert np.max(abs(eventsum-[physical['source_transfer'],physical['expenditure'],physical['damage'],physical['repair']]))<1e-9
        waves={k:np.asarray(v) for k,v in lists.items()};np.savez_compressed(str(dest)+'_waves.npz',**waves)
        assert np.max(abs(controls(waves['learned'],waves['exploration'],waves['need'])-waves['controls']))<1e-14
        assert np.max(abs(np.tanh(waves['oscillator']+waves['direct_feedback']+waves['evoked']+waves['current'])-waves['target']))<1e-14
        cutoff=details['last_complete_checkpoint_age'] if number==8 else t
        # Exact neural values are wave-end measurements; add the known zero birth banks/maps.
        keep=waves['time']<=cutoff
        learned=waves['learned'];withoutE=learned.copy();withoutE[:,0]=0;withoutI=learned.copy();withoutI[:,1]=0
        de=waves['controls']-controls(withoutE,waves['exploration'],waves['need'])
        di=waves['controls']-controls(withoutI,waves['exploration'],waves['need'])
        columns=['age','native_index','wave','H_norm','regulator_theta_E_norm','regulator_theta_I_norm','H_use_mean','H_use_max','q_norm','learned_E_current_delta_left','learned_E_current_delta_right','learned_I_current_delta_left','learned_I_current_delta_right','learned_E_current_delta_rms','learned_I_current_delta_rms','M1_spontaneous_rms','direct_feedback_rms','motor_evocation_rms','learned_E_attenuation_delta_left','learned_E_attenuation_delta_right','learned_I_attenuation_delta_left','learned_I_attenuation_delta_right']
        raw=np.column_stack((waves['time'],waves['index'],waves['wave'],waves['H_norm'],waves['regulator_bank_norm'],waves['H_use_mean'],waves['H_use_max'],np.linalg.norm(waves['q'],axis=1),de[:,8:10],di[:,8:10],np.sqrt(np.mean(de[:,8:10]**2,axis=1)),np.sqrt(np.mean(di[:,8:10]**2,axis=1)),np.sqrt(np.mean(waves['oscillator']**2,axis=1)),np.sqrt(np.mean(waves['direct_feedback']**2,axis=1)),np.sqrt(np.mean(waves['evoked']**2,axis=1)),de[:,10:12],di[:,10:12]))
        with gzip.open(OUT/'raw'/(life+'_H_E_I_WAVES.csv.gz'),'wt',newline='',encoding='utf8') as f:
            wr=csv.writer(f);wr.writerow(columns);wr.writerows(raw[keep])
        with gzip.open(OUT/'raw'/(life+'_BODY_NATIVE.csv.gz'),'wt',newline='',encoding='utf8') as f:
            wr=csv.writer(f);wr.writerow(['age','native_index','E','I']);wr.writerow([0,0,b['energy'],b['integrity']]);mask=native[:,0]<=cutoff
            wr.writerows(np.column_stack((native[mask,0],np.arange(1,n+1)[mask],native[mask,SL['reserves']])))
        # Plot inputs preserve every wave, every native reserve and both sides of support.
        bt=np.r_[0,native[mask,0]];body=np.vstack(([b['energy'],b['integrity']],native[mask,SL['reserves']]))
        interventions=[v for v in details['resurrections'] if v['time']<=cutoff]
        extraT=[];extraB=[]
        for e in interventions:
            extraT.extend([e['time'],e['time']]);extraB.extend([e['before_reserves'],e['after_reserves']])
        np.savez_compressed(OUT/'cache'/(life+'_curves.npz'),wave=raw[keep],wave_columns=np.array(columns),body_time=bt,body=body,support_time=np.array(extraT),support_body=np.array(extraB).reshape(-1,2))
        table('tables/'+life+'_IMPACTS.csv',impacts)
        record=dict(life=life,physical_age=t,curve_cutoff=cutoff,last_complete_checkpoint_age=details['last_complete_checkpoint_age'],native_rows=n,waves=len(waves['time']),curve_waves=int(keep.sum()),event_rows=eventcount,ledger_max=ledger_error,physical_totals=eventsum,birth_position=b['position'],birth_angle=b['angle'],interventions=interventions,source_hashes=[dict(file=p.name,sha256=HASHES[p.relative_to(EX).as_posix()]) for p in checkpoint_paths(life)])
        save('cache/'+life+'.json',record);records.append(record)
        print(json.dumps(dict(event='PASSIVE_EXTRACTED',life=life,age=t,curve_cutoff=cutoff,native_rows=n,waves=len(waves['time']))),flush=True)
    save('EXTRACTION_VERIFICATION.json',dict(status='PASS',new_simulation_steps=0,model_imports=0,lives=records,original_seal_sha256=sha(OLD/'EXECUTION_CUSTODY_SEAL.json')))
if __name__=='__main__':main()
