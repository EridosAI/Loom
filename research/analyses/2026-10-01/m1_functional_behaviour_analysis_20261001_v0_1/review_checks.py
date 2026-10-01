"""Independent algebra and accounting checks on preserved records; no model execution."""
from common import *
import ast
def f(r,k):return float(r[k]) if r.get(k,'')!='' else None
def main():
    # Allocate contact duration from fine solver fragments, not a uniform grouped-bout span.
    corrections=[]
    for filename in ('BEHAVIOURAL_AGE_BANDS','BEHAVIOURAL_60S'):
        rows=readcsv('tables/'+filename+'.csv')
        for n in range(1,13):
            life=f'RS-M1-{n:03d}';episodes=[e for e in details(life)['physical']['episodes'] if e['collider'].startswith('source')]
            for r in rows:
                if r['life']!=life:continue
                lo,hi=f(r,'start'),f(r,'end');seconds=sum(max(0,min(hi,e['end'])-max(lo,e['start']))*e['duration']/max(e['end']-e['start'],1e-30) for e in episodes)
                corrections.append(abs(seconds-f(r,'source_contact_seconds')));r['source_contact_seconds']=seconds;r['source_transfer_per_contact_second']=div(f(r,'source_energy'),seconds)
        table('tables/'+filename+'.csv',rows)
    audit=[];inputs=[]
    bands=readcsv('tables/BEHAVIOURAL_AGE_BANDS.csv');intervals=readcsv('tables/RESURRECTION_INTERVALS.csv');sens=readcsv('tables/DEFINITION_SENSITIVITY.csv');pairs=readcsv('tables/CONTEXT_PAIRS.csv')
    for n in range(1,13):
        life=f'RS-M1-{n:03d}';d=details(life);F=np.load(OUT/'series'/(life+'_FUNCTIONAL.npz'));w=np.load(PRIOR/'cache'/(life+'_waves.npz'));count=len(F['age']);t=F['age'];a=native(life)
        initial=attrs(rd(next((EX/'lives'/life).glob('pilot-*-pilot-initial.ld')))['engine']);r=attrs(attrs(initial['organism'])['regulator']);birth=r['output_diagnostic']
        L=np.concatenate((np.asarray(birth['learned'])[None],w['learned'][:count-1]));X=np.concatenate((np.asarray(birth['exploration'])[None],w['exploration'][:count-1]));N=np.concatenate((np.asarray(birth['need'])[None],w['need'][:count-1]));alpha=-np.expm1(-F['native_elapsed']/cfg['tau_motor'])[:,None]
        z=w['oscillator'][:count]+w['direct_feedback'][:count]+w['evoked'][:count]+w['current'][:count];error=0.
        for bank,label in ((0,'E'),(1,'I')):
            # Closed bankwise identity, independent of the omitted full-controls implementation.
            dc=cfg['current_max']/2*(np.tanh(N[:,bank,None]*(L[:,bank,8:10]+X[:,bank,8:10]))-np.tanh(N[:,bank,None]*X[:,bank,8:10]))
            du=(1-w['attenuation_used'][:count])*alpha*(np.tanh(z)-np.tanh(z-dc));error=max(error,float(np.max(abs(dc-F[label+'_current_delta']))),float(np.max(abs(du-F[label+'_command_delta']))))
            assert error<1e-14
        my=[r for r in bands if r['life']==life];ii=[r for r in intervals if r['life']==life]
        for key,original in [('source_energy','source_transfer'),('damage','damage'),('repair','repair'),('expenditure','expenditure')]:assert abs(sum(f(r,key) for r in my)-d['physical'][original])<1e-8,(life,key)
        for key in ('source_energy','expenditure','path'):assert abs(sum(f(r,key) for r in my)-sum(f(r,key) for r in ii))<1e-8,(life,key)
        ss=[r for r in sens if r['life']==life and r['kind']=='source_bout'];assert len(ss)==9
        for key in ('transfer','contact_seconds'):assert np.ptp([f(r,key) for r in ss])<1e-8
        assert abs(sum(f(r,'source_contact_seconds') for r in my)-f(ss[0],'contact_seconds'))<1e-8
        pp=[r for r in pairs if r['life']==life]
        for q in pp:
            assert f(q,'normalized_distance')<=1+1e-12 and f(q,'later_age')>=f(q,'early_age')+60-1e-8
            assert abs(f(q,'early_E')-f(q,'later_E'))<=.1+1e-12 and abs(f(q,'early_I')-f(q,'later_I'))<=.05+1e-12
            assert abs(f(q,'early_speed')-f(q,'later_speed'))<=.03+1e-12
            assert f(q,'later_age')+10<=a[-1,0]+1e-7
            if q['kind']!='post_impact':assert q['query_contact_free']==q['later_contact_free']=='True'
        for qid in set(r['query'] for r in pp):
            ts=sorted(f(r,'later_age') for r in pp if r['query']==qid);assert len(ts)<=3
            if len(ts)>1:assert min(np.diff(ts))>=10-1e-8
        feat=np.load(OUT/'cache'/(life+'_PERMITTED_CONTEXTS.npz'));assert set(feat.files)=={'age','features','contact_free','normalized'} and feat['features'].shape[1]==48
        assert all(np.all(np.isfinite(feat[k])) for k in ('age','features','normalized'))
        if n==10:assert np.all(F['I_command_effect']==0) and np.all(np.isnan(F['command_per_theta_I']))
        audit.append(dict(life=life,independent_receiver_max_error=error,waves=count,context_pairs_checked=len(pp),ledger_age_interval_conservation=True,bout_sensitivity_preserves_totals=True,feature_allowlist=True))
        for q in [PRIOR/'cache'/(life+'_native.npy'),PRIOR/'cache'/(life+'_waves.npz'),PRIOR/'raw'/(life+'_physical_events.csv.gz'),OLD/(life+'_DETAILS.json')]:inputs.append(dict(path=str(q),bytes=q.stat().st_size,sha256=sha(q)))
        print(life+' independent checks and input hashes complete',flush=True)
    # Recheck every preserved execution file against the original custody seal.
    seal=json.loads((OLD/'EXECUTION_CUSTODY_SEAL.json').read_bytes());bad=[]
    for r in seal['files']:
        pth=EX/r['path']
        if not pth.is_file() or pth.stat().st_size!=r['bytes'] or sha(pth)!=r['sha256']:bad.append(r['path'])
    assert not bad,bad
    prior=json.loads((PRIOR/'INPUT_PROVENANCE.json').read_bytes());changed=[]
    for r in prior['sources']:
        pth=Path(r['path'])
        if sha(pth)!=r['sha256']:changed.append(r['path'])
    assert not changed,changed
    archive=ROOT/'M1_RESURRECTION_SANDBOX_20260930_v0_1.zip';assert sha(archive)==prior['archive']['sha256']
    save('REVIEW_VERIFICATION.json',dict(status='PASS',checks=audit,execution_files_rehashed=len(seal['files']),execution_files_changed=bad,source_files_changed=changed,original_archive_sha256=prior['archive']['sha256'],analysis_contact_allocation_max_corrected_seconds=max(corrections),methods='same analyst; independently rearranged bankwise equations, ledger and custody checks; no independent human review',world_steps=0,RNG_draws=0,alternate_trajectories=0,production_edits=0))
    save('ANALYSIS_INPUT_HASHES.json',dict(inputs=inputs,source_provenance=prior,original_custody_seal_sha256=sha(OLD/'EXECUTION_CUSTODY_SEAL.json')))
    print('All source custody, arithmetic, denominators and allowlist checks PASS',flush=True)
if __name__=='__main__':main()
