"""Bounded corrective evidence; stages never silently rerun or replace artifacts."""
import argparse
import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from loom_p.records import code_identity,strict_bytes,view,state_hash
from loom_p.schema import Config

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'artifacts/correction-20260923-01a0c405'
OLD='d5f7efbe67193f215e52d95ca912db131a79f31c'

def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def save(name,value):
    with (OUT/name).open('xb') as f: f.write(strict_bytes(view(value)))

def preflight():
    from loom_p.prehistory import load
    before=json.loads((OUT/'BASELINE_CODE_HASHES.json').read_text())
    current=code_identity()['files']
    changed=[n for n in current if current[n]!=before[n]]
    assert changed==['physics.py'], changed
    old_config=subprocess.check_output(['git','-C',str(ROOT.parent),'show',OLD+':developmental_ecology/configuration.json'])
    # Git normalizes this JSON's CRLF checkout; the original runtime receipt
    # records actual file bytes. Require both that byte identity and JSON law.
    original_runtime=json.loads((ROOT.parent/'docs/developmental_ecology/p_engineering_20260921/RUNTIME_RECORD.json').read_text())
    assert sha(ROOT/'configuration.json')==original_runtime['configuration_file_sha256']
    assert json.loads(old_config)==json.loads((ROOT/'configuration.json').read_bytes())
    fields,phase,rng,m=load(Config(),ROOT/'artifacts/prehistory-attempt-001')
    save('PREHISTORY_REUSE.json',dict(changed_runtime_modules=changed,unchanged_dependencies={n:current[n] for n in current if n!='physics.py'},configuration_byte_identical=True,configuration_sha256=Config().identity(),phase=phase,field_sha256=hashlib.sha256(fields.tobytes()).hexdigest(),cached_manifest=m,prehistory_executions=0,decision='Reuse unchanged lawful field cache. No field/prehistory dependency changed.'))
    print('Prehistory dependencies unchanged; cache verified; no regeneration.',flush=True)

def smokes():
    from loom_p.smokes import CASES,execute
    assert (OUT/'PREHISTORY_REUSE.json').exists()
    for case in CASES:
        print('START',case,'attempt-003',flush=True)
        result=execute(case,ROOT/'configuration.json',3,'Authorized R1 release/recontact correction and R2/R3 reverification; same configuration, seed, life and duration.')
        save(case+'-attempt-003-result.json',result)
        print('DONE',case,result['status'],result['records'],flush=True)

def rows(root,kind):
    with gzip.open(root/(kind+'.jsonl.gz'),'rt',encoding='utf-8') as f:
        for line in f: yield json.loads(line)

def verify():
    from verify_engineering_records import verify as reconstruct_case
    from loom_p.smokes import CASES
    from loom_p.inspector import Inspector
    from loom_p.physics import Body,advance
    results=[]; comparisons=[]
    for case in CASES:
        old=ROOT/'artifacts'/f'smoke-{case}-attempt-002'; new=ROOT/'artifacts'/f'smoke-{case}-attempt-003'
        result=reconstruct_case(new); results.append(result)
        delta={key:0. for key in ('reserves','position','angle','velocity','omega','commands','stocks','contact_rates')}
        different_neural=0; first=None; count=0
        for a,b in zip(rows(old,'native'),rows(new,'native'),strict=True):
            count+=1
            if a['organism_sha256']!=b['organism_sha256']: different_neural+=1
            for key in delta:
                d=float(np.max(np.abs(np.asarray(a[key])-np.asarray(b[key])))); delta[key]=max(delta[key],d)
                if d and first is None: first=b['native_index']
        old_m=json.loads((old/'manifest.json').read_text()); new_m=json.loads((new/'manifest.json').read_text())
        assert all(old_m[k]==new_m[k] for k in ('configuration_sha256','seed','life','simulated_seconds_cap','fixture'))
        comparisons.append(dict(case=case,native_compared=count,max_absolute_difference=delta,first_body_difference_native=first,different_organism_hashes=different_neural,old_events=old_m['records']['events'],new_events=new_m['records']['events'],same_configuration_seed_life_fixture_and_cap=True))
        print('RECONSTRUCTED',case,'neural, field, clocks, source/body accounting',flush=True)
    save('RECONSTRUCTION.json',dict(cases=results,method='Detached neural and field arithmetic on saved records; no new complete-loop execution.'))
    save('TRAJECTORY_COMPARISON.json',comparisons)
    app=Inspector(); assert app.engine is not None and app.error is None
    assert app.record_path.endswith('smoke-contact_ui_1s-attempt-003')
    before=state_hash(app.engine); before_counts=copy.deepcopy(app.engine.organism.rng.counters)
    app.observation(); app.command('pause'); app.command('replay',39); app.command('reconstruct'); result=app.observation()
    assert state_hash(app.engine)==before and app.engine.organism.rng.counters==before_counts
    assert app.engine.time==0. and app.session_steps==0 and app.recorder is None
    save('OBSERVER_ISOLATION.json',dict(paused=True,initial_engine_time=app.engine.time,session_steps=app.session_steps,record=result['record_path'],cursor=39,live_before=before,live_after=state_hash(app.engine),counters_identical=True,detached_reconstruction=result['parameters']['provenance'],server_launched=False,simulation_steps=0))
    # Exact old/new R1 component comparison, running archived physics in its own
    # module namespace. Only this arithmetic fixture, never the old full loop.
    source=subprocess.check_output(['git','-C',str(ROOT.parent),'show',OLD+':developmental_ecology/loom_p/physics.py'])
    import types
    module=types.ModuleType('loom_p._preserved_r1_physics'); module.__package__='loom_p'; sys.modules[module.__name__]=module
    exec(compile(source,'<preserved d5f7efbe physics>','exec'),module.__dict__)
    observations={}
    for label,bodyclass,fn in [('old',module.Body,module.advance),('corrected',Body,advance)]:
        b=bodyclass(np.array([2.,3.]),0.,velocity=np.array([-.001,0.])); stocks=np.full(8,.2)
        events,elapsed,terminal=fn(Config(),b,stocks,0.,0.,np.ones(2),.01)
        observations[label]=dict(events=events,elapsed=elapsed,terminal=terminal,position=b.position,reserves=b.reserves,stocks=stocks,transfer=sum(r['transfer'].sum() for r in events),damage=sum(r['damage'] for r in events))
    save('R1_COUNTEREXAMPLE.json',dict(old_source_sha256=hashlib.sha256(source).hexdigest(),comparison=observations))

def suite():
    # Run only after all new smoke artifacts and reconstruction fixtures exist.
    assert (OUT/'RECONSTRUCTION.json').exists() and (OUT/'OBSERVER_ISOLATION.json').exists()
    result=subprocess.run([sys.executable,'-B','-X','utf8','-m','pytest','tests','-q','-p','no:cacheprovider'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    with (OUT/'FINAL_COMPONENT_SUITE.txt').open('xb') as f: f.write((result.stdout+result.stderr).encode('utf-8'))
    save('FINAL_COMPONENT_RECEIPT.json',dict(exit_code=result.returncode,code=code_identity(),all_three_attempt_003_manifests_present=True,command='python -B -X utf8 -m pytest tests -q -p no:cacheprovider',cwd=str(ROOT)))
    print(result.stdout+result.stderr,flush=True)
    if result.returncode: raise SystemExit(result.returncode)

def preserve():
    expected=json.loads((OUT/'PRESERVED_ARTIFACTS_BEFORE.json').read_text())
    mismatches=[p for p,r in expected.items() if not (ROOT/'artifacts'/p).exists() or (ROOT/'artifacts'/p).stat().st_size!=r['bytes'] or sha(ROOT/'artifacts'/p)!=r['sha256']]
    assert not mismatches,mismatches
    save('PRESERVATION_VERIFIED.json',dict(preexisting_files=len(expected),all_bytes_and_sha256_unchanged=True,old_checkpoint=OLD))
    print('All',len(expected),'preserved artifact files unchanged.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('stage',choices=['preflight','smokes','verify','suite','preserve']); args=parser.parse_args()
    globals()[args.stage]()
