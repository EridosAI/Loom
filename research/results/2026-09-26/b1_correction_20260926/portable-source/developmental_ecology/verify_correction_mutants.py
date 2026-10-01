"""Isolated in-memory faults; each subprocess must fail its designated assertion.
Never edits a production module or runs a complete-loop smoke.
"""
import argparse
import hashlib
import inspect
import json
import subprocess
import sys
import textwrap
from pathlib import Path

CASES={
 'release_disabled':('tests/test_corrective_contracts.py::test_touch_release_return_duration_and_accounting','Touching body must release'),
 'live_branch_missing':('tests/test_records.py::test_live_handoff_observation_has_physical_timestamp','Live handoff branch was not exercised'),
 'bank_reference_frozen':('tests/test_neural.py::test_bank_projection_and_reference_follow_new_value','assert np.allclose(r.reference'),
 'bank_reference_old_target':('tests/test_neural.py::test_bank_projection_and_reference_follow_new_value','Bank reference must follow newly projected theta'),
 'shared_reference_frozen':('tests/test_corrective_contracts.py::test_separate_sensory_reference_following[shared_ref-shared-tau_shared_reference]','shared_ref movement missing'),
 'fine_reference_frozen':('tests/test_corrective_contracts.py::test_separate_sensory_reference_following[fine_ref-fine-tau_fine_reference]','fine_ref movement missing'),
 'terminal_guard_removed':('tests/test_boundary_and_scheduler.py::test_terminal_scheduler_restores_trial_state_and_draws_once[19]','Invented terminal handoff'),
 'body_footprint_missing':('tests/test_physical.py::test_field_flux_mass_and_moving_geometry_continuity','Body footprint must change diffusion'),
 'hidden_pose_injected':('tests/test_corrective_contracts.py::test_hidden_state_cannot_bypass_declared_transductions','Hidden world state entered native learner arithmetic'),
 'hidden_config_read':('tests/test_corrective_contracts.py::test_hidden_state_cannot_bypass_declared_transductions','Forbidden learner configuration read'),
 'evoked_refill':('tests/test_corrective_contracts.py::test_evoked_reserves_have_no_direct_physical_ownership','Evoked reserve bypassed motor/physical ownership'),
 'double_source_debit':('tests/test_corrective_contracts.py::test_touch_release_return_duration_and_accounting',"r['stock_after']-r['stock_before']"),
 'damage_suppressed':('tests/test_corrective_contracts.py::test_touch_release_return_duration_and_accounting',"r['integrity_after']-r['integrity_before']"),
 'native_repeated':('tests/test_corrective_contracts.py::test_release_subdivision_does_not_repeat_native_or_noise',"assert calls=="),
}


def install(name):
    import loom_p.physics as p
    import loom_p.engine as e
    import loom_p.neural as n
    import loom_p.inspector as i
    import loom_p.chemistry as ch
    if name=='release_disabled': p.release_probe=lambda *args:None
    elif name=='live_branch_missing':
        old=i.Inspector.observation
        def broken(self):
            result=old(self); result['wave']=None; return result
        i.Inspector.observation=broken
    elif name=='bank_reference_frozen':
        old=n.Regulator.credit
        def broken(self,*args):
            reference=self.reference.copy(); old(self,*args); self.reference=reference
        n.Regulator.credit=broken
    elif name=='bank_reference_old_target':
        old=n.Regulator.credit
        def broken(self,c,*args):
            theta=self.theta.copy(); reference=self.reference.copy(); old(self,c,*args)
            self.reference=n.follow(reference,theta,c.wave_dt,c.tau_bank_reference)
        n.Regulator.credit=broken
    elif name in ('shared_reference_frozen','fine_reference_frozen'):
        old=n.Cortex.step; attr='shared_ref' if name.startswith('shared') else 'fine_ref'
        def broken(self,*args):
            reference=getattr(self,attr).copy(); old(self,*args); setattr(self,attr,reference)
        n.Cortex.step=broken
    elif name=='terminal_guard_removed':
        source=textwrap.dedent(inspect.getsource(e.Engine.step))
        assert 'elif self.native_index%' in source
        source=source.replace('elif self.native_index%','if self.native_index%')
        namespace=dict(vars(e)); exec(compile(source,'<mutant terminal guard>','exec'),namespace)
        e.Engine.step=namespace['step']
    elif name=='body_footprint_missing':
        old=ch.FieldSolver.coefficients
        ch.FieldSolver.coefficients=lambda self,t,phase,body_position=None:old(self,t,phase,None)
    elif name=='hidden_config_read':
        old=n.Organism.native
        def broken(self,*args,**kwargs):
            hidden=self.c.source_positions
            return old(self,*args,**kwargs)
        n.Organism.native=broken
    elif name in ('hidden_pose_injected','evoked_refill','native_repeated'):
        old=e.Engine._coupled
        def broken(self,dt,refresh,allow_terminal=False):
            if name=='hidden_pose_injected': self.raw[0][0]+=self.body.position[0]
            if name=='native_repeated': self.organism.native(self.raw,dt,refresh_noise=refresh)
            result=old(self,dt,refresh,allow_terminal)
            if name=='evoked_refill': self.body.energy+=.0001*self.organism.association.q[self.c.slices[4]][0]
            return result
        e.Engine._coupled=broken
    elif name in ('double_source_debit','damage_suppressed'):
        old=p.account
        def broken(c,body,stocks,contacts,dt,instant=False):
            result=old(c,body,stocks,contacts,dt,instant)
            if name=='double_source_debit':
                stocks-=result['transfer']; result['stock_after']=stocks.copy()
            else:
                body.integrity+=result['damage']; result['integrity_after']=body.integrity
            return result
        p.account=broken
    else: raise ValueError(name)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--child'); parser.add_argument('--output',type=Path); args=parser.parse_args()
    if args.child:
        import pytest
        install(args.child)
        raise SystemExit(pytest.main([CASES[args.child][0],'-q','-p','no:cacheprovider','--tb=short']))
    args.output.mkdir(parents=True,exist_ok=False)
    receipts=[]
    for name,(test,expected) in CASES.items():
        red=subprocess.run([sys.executable,'-B','-X','utf8',__file__,'--child',name],capture_output=True,text=True,encoding='utf-8')
        output=red.stdout+red.stderr
        (args.output/(name+'-RED.txt')).write_bytes(output.encode('utf-8'))
        valid=red.returncode==1 and expected in output and '1 failed' in output
        receipt=dict(mutant=name,test=test,expected_failure=expected,red_exit=red.returncode,observed_red=valid)
        if not valid:
            print(output,flush=True); raise RuntimeError('Mutant did not fail its intended assertion: '+name)
        green=subprocess.run([sys.executable,'-B','-X','utf8','-m','pytest',test,'-q','-p','no:cacheprovider'],capture_output=True,text=True,encoding='utf-8')
        (args.output/(name+'-GREEN.txt')).write_bytes((green.stdout+green.stderr).encode('utf-8'))
        receipt.update(green_exit=green.returncode,observed_green=green.returncode==0)
        receipts.append(receipt); print(name,receipt['red_exit'],receipt['green_exit'],flush=True)
        if green.returncode: raise RuntimeError('Unmutated test failed: '+name)
    (args.output/'SUMMARY.json').write_bytes(json.dumps(dict(harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),receipts=receipts),indent=2).encode('utf-8'))


if __name__=='__main__': main()
