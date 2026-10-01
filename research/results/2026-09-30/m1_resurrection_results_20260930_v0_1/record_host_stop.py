"""NON-CANONICAL RESURRECTION SANDBOX. Preserve abrupt host-stop disposition; no replay."""
from pathlib import Path
from datetime import datetime,timezone
import json
import analyse_passive as m

def main():
    assert not (m.EX/'DENOMINATOR.json').exists()
    observed=json.loads((m.OUT/'HOST_FAILURE_OBSERVATION.json').read_text(encoding='utf-8-sig'))
    assert observed['kind']=='HOST_NATIVE_APPLICATION_ERROR'
    files=[dict(path=p.relative_to(m.EX).as_posix(),bytes=p.stat().st_size,sha256=m.h(p)) for p in sorted(m.EX.rglob('*')) if p.is_file()]
    hashes={r['path']:r['sha256'] for r in files}
    rd=lambda p:m.read_data(p,hashes[p.relative_to(m.EX).as_posix()])
    rows=[];interrupted=None
    for j in range(1,13):
        name=f'RS-M1-{j:03d}';store=m.EX/'lives'/name
        pilot=json.loads((store/'pilot-RECEIPT.json').read_bytes())
        assert pilot['complete'] and pilot['end_age']==600
        row=dict(life_id=name,pilot='AGE_TARGET_COMPLETE',overnight='UNSTARTED',last_age=600.,last_full_checkpoint=pilot['final_checkpoint']['file'])
        if (store/'overnight-RECEIPT.json').exists():
            receipt=json.loads((store/'overnight-RECEIPT.json').read_bytes())
            assert receipt['complete'] and receipt['end_age']==4500
            row.update(overnight='AGE_TARGET_COMPLETE',last_age=4500.,last_full_checkpoint=receipt['final_checkpoint']['file'])
        elif (store/'overnight-START.json').exists():
            assert interrupted is None
            cp=[]
            for p in store.glob('overnight-*.ld'):
                if any(word in p.name for word in ('periodic','initial','resurrection-')):
                    e=m.attrs(rd(p)['engine']);cp.append((e['native_index'],p.name,e['time']))
            ni,filename,age=max(cp)
            last=sorted(store.glob('chunk-*.ld'))[-1];v=rd(last);n=v['native'][-1]
            row.update(overnight='HOST_NATIVE_CRASH_DURABLE_PREFIX',last_age=float(n[0]),last_durable_native_index=v['last_index'],
                last_full_checkpoint=filename,last_full_checkpoint_index=ni,last_full_checkpoint_age=age,
                last_chunk=last.name,full_state_at_durable_endpoint_available=False)
            interrupted=row
        rows.append(row)
    assert interrupted and interrupted['life_id']=='RS-M1-008'
    reason='Windows native Python memory-read access violation; process remained in Application Error wait and was terminated without retry.'
    start=datetime.fromtimestamp((m.EX/'SINGLE_USE_START.json').stat().st_mtime,timezone.utc)
    stopped=datetime.fromisoformat(observed['observed_utc'].replace('Z','+00:00'))
    elapsed=(stopped-start).total_seconds()
    primary=sum(p.stat().st_size for p in m.PREP.rglob('*') if p.is_file())
    den=dict(label=m.LABEL,kind='EXTERNAL_POST_STOP_DISPOSITION_NOT_EXECUTOR_RECEIPT',rows=rows,stop=reason,common_target=4500.,
        active_wall_seconds=elapsed,active_wall_estimated_from_file_timestamp=True,primary_bytes=primary,
        new_simulation_steps=0,exact_inflight_state_available=False,canonical_P_world_untouched=True)
    m.save('HOST_STOP_DENOMINATOR.json',den)
    m.save('HOST_STOP.json',dict(label=m.LABEL,reason=reason,stage='overnight',life=interrupted['life_id'],
        age=interrupted['last_age'],native_index=interrupted['last_durable_native_index'],boundary_kind='LAST_DURABLE_NATIVE_PREFIX_NOT_EXACT_CRASH_CALL',
        exact_inflight_state_available=False,last_full_checkpoint=interrupted['last_full_checkpoint'],
        last_full_checkpoint_age=interrupted['last_full_checkpoint_age'],last_full_checkpoint_index=interrupted['last_full_checkpoint_index'],
        no_retry=True,no_reconstruction=True,no_simulation_after_host_failure=True))
    m.save('EXECUTION_CUSTODY_SEAL.json',dict(label=m.LABEL,utc=datetime.now(timezone.utc).isoformat(),files=files,
        bytes=sum(r['bytes'] for r in files),denominator_source='HOST_STOP_DENOMINATOR.json',denominator_sha256=m.h(m.OUT/'HOST_STOP_DENOMINATOR.json')))
    print(json.dumps(dict(label=m.LABEL,rows=rows,primary_bytes=primary,estimated_wall_seconds=elapsed,execution_files=len(files))))
if __name__=='__main__':main()
