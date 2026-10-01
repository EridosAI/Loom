"""Observed R1-P faults in isolated subprocesses; no production-file mutations."""
import argparse,hashlib,json,subprocess,sys,types
from pathlib import Path
OLD='f7eb6f27c661e3db193a4225b56a825d7e41739d'
EXACT='tests/test_r1p_oblique.py::test_oblique_release_free_return_and_accounting[review-exact]'
CASES={
 'unmodified_f7':(EXACT,'R1-P: resolvable free flight was charged as contact'),
 'class_search_disabled':(EXACT,'R1-P: resolvable free flight was charged as contact'),
 'old_swept_search':(EXACT,'Swept contact search iteration limit'),
 'duplicate_field_update':('tests/test_r1p_oblique.py::test_oblique_event_subdivision_keeps_native_noise_and_field_cadence',"assert calls=="),
}
def archived():
    root=Path(__file__).resolve().parent.parent
    source=subprocess.check_output(['git','-C',str(root),'show',OLD+':developmental_ecology/loom_p/physics.py'])
    name='loom_p._archived_f7_physics'; m=types.ModuleType(name); m.__package__='loom_p'; sys.modules[name]=m
    exec(compile(source,'<unmodified f7eb6f27 physics>','exec'),m.__dict__)
    return m,hashlib.sha256(source).hexdigest()
def install(name):
    import loom_p.physics as p
    import loom_p.engine as e
    if name=='unmodified_f7':
        m,_=archived(); p.advance=m.advance; e.advance=m.advance
    elif name=='class_search_disabled': p.clear_excursion=lambda *args:None
    elif name=='old_swept_search':
        m,_=archived(); p.first_collision=m.first_collision
    elif name=='duplicate_field_update':
        original=e.Engine._coupled
        def broken(self,dt,refresh,allow_terminal=False):
            result=original(self,dt,refresh,allow_terminal)
            self.solver.step(self.fields,self.stocks,self.time,self.phase,dt,self.body.position)
            return result
        e.Engine._coupled=broken
    else: raise ValueError(name)
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--child'); parser.add_argument('--output',type=Path); args=parser.parse_args()
    if args.child:
        import pytest
        install(args.child)
        raise SystemExit(pytest.main([CASES[args.child][0],'-q','-p','no:cacheprovider','--tb=short']))
    args.output.mkdir(exist_ok=False); receipts=[]
    for name,(test,expected) in CASES.items():
        r=subprocess.run([sys.executable,'-B','-X','utf8',__file__,'--child',name],capture_output=True,text=True,encoding='utf-8')
        output=r.stdout+r.stderr; (args.output/(name+'-RED.txt')).write_bytes(output.encode())
        assert r.returncode==1 and expected in output and '1 failed' in output,(name,output)
        g=subprocess.run([sys.executable,'-B','-X','utf8','-m','pytest',test,'-q','-p','no:cacheprovider'],capture_output=True,text=True,encoding='utf-8')
        (args.output/(name+'-GREEN.txt')).write_bytes((g.stdout+g.stderr).encode())
        assert g.returncode==0,(name,g.stdout,g.stderr)
        receipts.append(dict(fault=name,test=test,expected_assertion=expected,red_exit=r.returncode,green_exit=g.returncode))
        print(name,'RED 1 -> GREEN 0',flush=True)
    _,oldsha=archived()
    (args.output/'SUMMARY.json').write_text(json.dumps(dict(old_checkpoint=OLD,old_physics_sha256=oldsha,harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),pairs=receipts),indent=2),encoding='utf-8')
if __name__=='__main__': main()
