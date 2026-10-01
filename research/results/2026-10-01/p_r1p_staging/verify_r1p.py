"""Second corrective pass, new exclusive evidence paths; no prehistory generator."""
import argparse,copy,gzip,hashlib,inspect,json,subprocess,sys
from pathlib import Path
import numpy as np
from loom_p.records import code_identity,strict_bytes,view,state_hash
from loom_p.schema import Config
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'artifacts/r1p-correction-20260923-01a0c405'
OLD='f7eb6f27c661e3db193a4225b56a825d7e41739d'
def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def save(name,value):
    with (OUT/name).open('xb') as f: f.write(strict_bytes(view(value)))
def preflight():
    from loom_p.prehistory import load
    baseline=json.loads((OUT/'BASELINE_FILE_HASHES.json').read_text())
    changed=[name for name,h in baseline.items() if sha(ROOT/name)!=h]
    assert changed==['loom_p/physics.py'],changed
    fields,phase,rng,m=load(Config(),ROOT/'artifacts/prehistory-attempt-001')
    save('PREHISTORY_AND_SCOPE.json',dict(changed_baseline_files=changed,all_existing_tests_byte_identical=True,configuration_sha256=Config().identity(),configuration_file_sha256=sha(ROOT/'configuration.json'),unchanged_dependencies={n:h for n,h in baseline.items() if n not in changed},field_sha256=hashlib.sha256(fields.tobytes()).hexdigest(),phase=phase,cache_validation=m,prehistory_steps_executed=0,code=code_identity()))
    print('Scope verified: physics only; all prior tests and field dependencies unchanged.',flush=True)
def smokes():
    from loom_p.smokes import CASES,execute
    assert (OUT/'PREHISTORY_AND_SCOPE.json').exists()
    for case in CASES:
        print('START',case,'attempt-004',flush=True)
        m=execute(case,ROOT/'configuration.json',4,'Authorized second R1-P correction: oblique release and swept-search termination; same configuration, seed, life, fixtures and caps.')
        save(case+'-004.json',m)
        print('DONE',case,m['status'],m['records'],flush=True)
def rows(path,kind):
    with gzip.open(path/(kind+'.jsonl.gz'),'rt',encoding='utf-8') as f:
        for line in f: yield json.loads(line)
def evidence():
    from verify_engineering_records import verify
    from loom_p.smokes import CASES
    from loom_p.inspector import Inspector
    import loom_p.physics as p
    from verify_r1p_mutants import archived
    reconstruction=[]; comparison=[]
    for case in CASES:
        previous=ROOT/'artifacts'/f'smoke-{case}-attempt-003'; current=ROOT/'artifacts'/f'smoke-{case}-attempt-004'
        reconstruction.append(verify(current))
        pm=json.loads((previous/'manifest.json').read_text()); cm=json.loads((current/'manifest.json').read_text())
        assert all(pm[k]==cm[k] for k in ('configuration_sha256','seed','life','fixture','simulated_seconds_cap'))
        delta={key:0. for key in ('reserves','position','angle','velocity','omega','commands','stocks','contact_rates')}; neural=raw=count=0
        for a,b in zip(rows(previous,'native'),rows(current,'native'),strict=True):
            count+=1; neural+=a['organism_sha256']!=b['organism_sha256']; raw+=a['raw']!=b['raw']
            for key in delta: delta[key]=max(delta[key],float(np.max(abs(np.asarray(a[key])-np.asarray(b[key])))))
        comparison.append(dict(case=case,native=count,max_absolute_difference=delta,different_neural_hashes=neural,different_raw_rows=raw,old_events=pm['records']['events'],new_events=cm['records']['events'],configuration_seed_life_fixture_caps_identical=True))
        print('RECONSTRUCTED',case,flush=True)
    save('RECONSTRUCTION.json',dict(cases=reconstruction,method='Detached neural/field replay; no new complete loop.'))
    save('ATTEMPT_COMPARISON.json',comparison)
    app=Inspector(); assert app.error is None and app.record_path.endswith('contact_ui_1s-attempt-004')
    before=state_hash(app.engine); counters=copy.deepcopy(app.engine.organism.rng.counters)
    app.observation(); app.command('pause'); app.command('replay',39); app.command('reconstruct'); obs=app.observation()
    assert state_hash(app.engine)==before and app.engine.organism.rng.counters==counters
    assert app.session_steps==0 and app.engine.time==0 and app.recorder is None
    save('OBSERVER.json',dict(paused_time=0,session_steps=0,before=before,after=state_hash(app.engine),counters_unchanged=True,record=app.record_path,reconstruction=obs['parameters']['provenance'],server_started=False))
    old,oldsha=archived(); cases=[]
    loop_lines={n+1 for n,line in enumerate(Path(p.__file__).read_text().splitlines()) if line.strip()=='for _ in range(500):'}
    for label,normal,speed,side in [('review-exact',.01,1e-5,1.),('different-normal-force',.02,1e-5,1.),('reflected-longer-flight',.01,2e-5,-1.),('radial-original',.76,.001,1.)]:
        variants={}
        for version,fn,body_class in [('f7',old.advance,old.Body),('corrected',p.advance,p.Body)]:
            b=body_class(np.array([2.,3.]),float(side*np.arccos(normal/.76)),velocity=np.array([-speed,0.])); stocks=np.full(8,.2)
            frames={}; completed=[]
            def trace(frame,event,arg):
                if frame.f_code.co_filename!=p.__file__: return trace
                if event=='call' and frame.f_code.co_name in ('search','first_collision'): frames[id(frame)]=dict(function=frame.f_code.co_name,loop_passes=0)
                if event=='line' and frame.f_lineno in loop_lines and id(frame) in frames: frames[id(frame)]['loop_passes']+=1
                if event=='return' and id(frame) in frames: completed.append(frames.pop(id(frame)))
                return trace
            try:
                if version=='corrected': sys.settrace(trace)
                events,elapsed,terminal=fn(Config(),b,stocks,0,0,np.ones(2),.01)
                variants[version]=dict(events=events,elapsed=elapsed,terminal=terminal,reserves=b.reserves,position=b.position,stocks=stocks,search_frames=completed)
            except ArithmeticError as error: variants[version]=dict(error=str(error),search_frames=completed)
            finally: sys.settrace(None)
        assert 'error' not in variants['corrected']
        assert all(s['loop_passes']<=500 for s in variants['corrected']['search_frames'])
        cases.append(dict(case=label,normal_force=normal,outward_speed=speed,orientation_sign=side,comparison=variants))
    save('PHYSICAL_COMPONENT_EVIDENCE.json',dict(old_checkpoint=OLD,old_physics_sha256=oldsha,cases=cases,trace_method='Read-only Python line tracing of existing 500-pass loops, in component arithmetic only.'))
def final():
    assert (OUT/'RECONSTRUCTION.json').exists()
    command=[sys.executable,'-B','-X','utf8','-m','pytest','tests','-q','-p','no:cacheprovider','--basetemp',str(OUT/'final-test-temp')]
    r=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    with (OUT/'FINAL_SUITE.txt').open('xb') as f: f.write((r.stdout+r.stderr).encode())
    save('FINAL_SUITE_RECEIPT.json',dict(exit_code=r.returncode,command=command,code=code_identity(),after_all_attempt_004_artifacts=True))
    print(r.stdout+r.stderr,flush=True)
    if r.returncode: raise SystemExit(r.returncode)
    expected=json.loads((OUT/'PRESERVED_ARTIFACTS_BEFORE.json').read_text())
    assert all((ROOT/'artifacts'/n).stat().st_size==r['bytes'] and sha(ROOT/'artifacts'/n)==r['sha256'] for n,r in expected.items())
    save('PRESERVATION.json',dict(files=len(expected),all_sizes_and_hashes_unchanged=True,checkpoints=['d5f7efbe67193f215e52d95ca912db131a79f31c',OLD]))
    print('Preserved',len(expected),'old artifact files.',flush=True)
if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('stage',choices=['preflight','smokes','evidence','final']); globals()[a.parse_args().stage]()
