"""Three predeclared cases only. Refuses unresolved configuration or repeat overwrite."""
import argparse
import copy
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
from .schema import Config,radial
from .prehistory import load
from .engine import Engine,run_bounded
from .records import Recorder,save_snapshot,load_snapshot,state_hash,strict_bytes
from .geometry import transduce

CASES={'birth_30s':30.,'nonzero_resume_1s':1.,'contact_ui_1s':1.}

def make_case(c,name,prehistory):
    fields,phase,rng,history=load(c,prehistory)
    e=Engine(c,fields,phase,rng,history)
    if name=='nonzero_resume_1s':
        for cortex in e.organism.cortices:
            cortex.x[:]=np.linspace(-.08,.08,len(cortex.x)); cortex.C[:]=.002
            cortex.shared_ref*=.95; cortex.fine_ref*=.9; cortex.opening[:]=.2
        a=e.organism.association
        for (m,n),maps in a.H.items():
            for j in range(4): maps[j]=radial(np.ones_like(maps[j])*(-1 if (m+n+j)%2 else 1),.04)
        for use in a.use.values(): use[:]=.1
        a.a[:]=np.linspace(-.1,.1,c.central_width); a.q[:]=.001
        for mu,z in zip(a.means,a.traces): mu[:]=.02; z[:]=.01
        r=e.organism.regulator; r.theta[:]=.001; r.reference[:]=.0005; r.eligibility[:]=.002
        r.body_mean[:]=[.69,.99]
        e.organism.motor.tendency[:]=[.08,-.04]
    elif name=='contact_ui_1s':
        e.body.position=np.array([2.,3.]); e.body.angle=0.; e.body.velocity=np.array([.01,0.]); e.body.integrity=.8
        e.raw=transduce(c,e.body,e.fields,e.time,e.phase)
        # Manufactured physical state; original newborn filters deliberately retained and disclosed.
    e.fixture=dict(name=name,duration=CASES[name],seed=c.master_seed,life=0,manufactured=name!='birth_30s',definition='loom_p.smokes.make_case; field is unchanged lawful prehistory; no outcome selection')
    return e

def execute(case,config_path,attempt,reason=None):
    c=Config(**json.loads(Path(config_path).read_text())).validate()
    if c.illumination_boundary is None: raise RuntimeError('Baseline illumination ruling required before complete-loop execution')
    if case not in CASES: raise ValueError('Case is outside declared budget')
    if attempt>1 and not reason: raise ValueError('Correction reason required for fixed-case rerun')
    root=Path(__file__).resolve().parents[1]; e=make_case(c,case,root/'artifacts'/'prehistory-attempt-001')
    directory=root/'artifacts'/f'smoke-{case}-attempt-{attempt:03d}'
    recorder=Recorder(directory,dict(case=case,simulated_seconds_cap=CASES[case],seed=c.master_seed,life=0,configuration=asdict(c),configuration_sha256=c.identity(),attempt=attempt,correction_reason=reason,initial_state_sha256=state_hash(e),fixture=e.fixture,units=dict(time='seconds',length='body_diameters',reserves='dimensionless [0,1]',stocks='reserve units',force='body_mass * body_diameter / second^2'),coordinate_order=dict(channels=['light','chemistry','contact','proprioception','energy','integrity','motor','regulation'],raw_widths=[10,4,8,7],packet_widths=c.packet_widths,central_widths=c.central_widths,pools=c.pools,packet='mean coordinates followed by endpoint coordinates',context='beta coordinates followed by trace coordinates, channel by channel')))
    if case!='nonzero_resume_1s':
        run_bounded(e,recorder,CASES[case]); return recorder.manifest
    # Same named case, two deterministic continuations for all-state verification.
    from .inspector import Inspector
    observer=Inspector(); observer.engine=e
    try:
        save_snapshot(recorder.path/'initial.snapshot.json.gz',e)
        birth_copy=load_snapshot(recorder.path/'initial.snapshot.json.gz')
        assert state_hash(e)==state_hash(birth_copy)
        for _ in range(7):
            n,w,events=e.step(); recorder.append('native',n)
            if w: recorder.append('wave',dict(time=e.time,**w))
            for ev in events: recorder.append('events',ev)
        save_snapshot(recorder.path/'midwave.snapshot.json.gz',e)
        resumed=load_snapshot(recorder.path/'midwave.snapshot.json.gz')
        assert state_hash(e)==state_hash(resumed)
        for _ in range(93):
            before=state_hash(e); observer.observation()
            assert state_hash(e)==before
            n,w,events=e.step(); resumed.step()
            recorder.append('native',n)
            if w: recorder.append('wave',dict(time=e.time,**w))
            for ev in events: recorder.append('events',ev)
            if state_hash(e)!=state_hash(resumed): raise AssertionError('Nonzero resumed trajectory mismatch')
        save_snapshot(recorder.path/'final.snapshot.json.gz',e)
        recorder.manifest.update(resume_identical=True,observer_noninterference=True,comparison_trajectory_seconds=.93)
        recorder.close('administrative_pause',True)
    except Exception as error:
        e.status='failure'; e.failure=f'{type(error).__name__}: {error}'
        try: save_snapshot(recorder.path/'failure.snapshot.json.gz',e)
        except OSError: pass
        try: recorder.close('apparatus_failure',False,e.failure)
        except OSError: pass
        raise
    return recorder.manifest

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('case',choices=CASES); p.add_argument('--config',default='configuration.json'); p.add_argument('--attempt',type=int,default=1); p.add_argument('--correction-reason'); a=p.parse_args()
    print(json.dumps(execute(a.case,a.config,a.attempt,a.correction_reason)))
