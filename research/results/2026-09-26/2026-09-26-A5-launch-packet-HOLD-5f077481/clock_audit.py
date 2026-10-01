"""Scalar floating-clock arithmetic only. No Loom import, world, command or RNG."""
import ast, hashlib, json, pathlib, sys

def audit(instrument):
    root=pathlib.Path(instrument)
    names={'loom_commissioning/adapter.py':['coupled','step'],
           'loom_commissioning/pending.py':['validate_decision'],
           'loom_commissioning/runner.py':['begin_command'],
           'loom_commissioning/controllers.py':['time_due']}
    excerpts={}
    for name,functions in names.items():
        raw=(root/name).read_bytes();source=raw.decode('utf-8');lines=source.splitlines()
        found={n.name:{'line':n.lineno,'text':'\n'.join(lines[n.lineno-1:n.end_lineno])}
               for n in ast.walk(ast.parse(source)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in functions}
        assert set(found)==set(functions)
        excerpts[name]={'sha256':hashlib.sha256(raw).hexdigest(),'functions':found}
    config=json.loads((root/'configuration.json').read_bytes())
    assert config['native_dt']==0.01 and config['event_time_tol']==1e-10
    assert 'e.time+=dt' in excerpts['loom_commissioning/adapter.py']['functions']['coupled']['text']
    assert "abs(d['time']-(m['initial_time']+(d['native_index']-m['initial_index'])*.01))<=1e-10" in excerpts['loom_commissioning/pending.py']['functions']['validate_decision']['text']
    now=0.;first_native=None;first_decision=None;points={}
    for i in range(1,63001):
        now+=.01
        v={'native_index':i,'accumulated_time':now,'index_derived_time':i*.01,'difference':now-i*.01,'predicate_passes':abs(now-i*.01)<=1e-10}
        if first_native is None and not v['predicate_passes']:first_native=v
        if first_decision is None and i%10==0 and not v['predicate_passes']:first_decision=v
        if i in (9000,12000,18000,21000,26940,26950,27000,30000,45000,48000,63000):points[str(i)]=v
    assert first_native['native_index']==26941 and first_decision['native_index']==26950
    return {'method':'Scalar additions/comparisons under pinned Python; no Loom imports or production validator invocation. Conditional on uninterrupted nonterminal full native steps.',
            'python':sys.version,'dt':.01,'absolute_decision_tolerance':1e-10,
            'first_native_exceedance':first_native,'first_decision_exceedance':first_decision,'checkpoints':points,
            'source_excerpts':excerpts,'world_steps':0,'controller_calls':0,'rng_draws':0,
            'commissioning_failure_observed':False,'launch_disposition':'HOLD_CLOCK_INCOMPATIBILITY'}

if __name__=='__main__':
    print(json.dumps(audit(pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent/'instrument/developmental_ecology'),indent=2))
