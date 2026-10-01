"""Coupled physical-time scheduler. UI and saved-record replay never own learning."""
import copy
import numpy as np
from .schema import Config,Streams
from .geometry import fixtures,gap_normal,transduce
from .chemistry import FieldSolver
from .physics import Body,advance,TerminalCrossing
from .neural import Organism

class Engine:
    def __init__(self,c,fields,phase,rng,prehistory_provenance):
        self.c=c.validate(); self.solver=FieldSolver(c); self.fields=fields.copy(); self.phase=float(phase)
        self.stocks=np.full(len(c.source_positions),c.source_capacity); self.time=0.; self.native_index=0
        self.status='paused'; self.failure=None; self.terminal_dimension=None; self.prehistory=prehistory_provenance
        rejected=[]; scene=fixtures(c,0,phase)
        for proposal in range(10000):
            position=c.body_radius+(c.world_side-2*c.body_radius)*rng.draw('world-position',(2,))
            gaps=[gap_normal(position,c.body_radius,f)[0] for f in scene]
            if min(gaps)>=.25: break
            rejected.append({'position':position.copy(),'minimum_gap':min(gaps)})
        else: raise ValueError('Birth rejection limit')
        angle=float(rng.draw('world-orientation',(1,))[0]*2*np.pi)
        self.body=Body(position,angle,energy=c.birth_energy)
        self.birth_provenance=dict(position=position.copy(),angle=angle,phase=phase,rejected=rejected)
        self.raw=transduce(c,self.body,self.fields,0,phase)
        self.organism=Organism(c,rng,self.raw,self.body.reserves)
        self.last_events=[]; self.last_native={}; self.last_wave=None
    def validate_state(self):
        c=self.c.validate()
        required=('solver','fields','phase','stocks','time','native_index','status','failure','terminal_dimension','prehistory','body','birth_provenance','raw','organism','last_events','last_native','last_wave')
        if any(not hasattr(self,key) for key in required): raise ValueError('Incomplete engine snapshot')
        if self.fields.shape!=(2,c.grid_n,c.grid_n) or self.fields.dtype!=np.float64: raise ValueError('Field schema mismatch')
        if self.stocks.shape!=(len(c.source_positions),): raise ValueError('Stock schema mismatch')
        if self.organism.association.a.shape!=(c.central_width,): raise ValueError('Central schema mismatch')
        if self.organism.regulator.theta.shape!=(2,c.outputs,c.feature_width+1): raise ValueError('Bank schema mismatch')
        def shaped(obj,name,shape):
            a=getattr(obj,name,None)
            if not isinstance(a,np.ndarray) or a.shape!=tuple(shape): raise ValueError(f'Snapshot array mismatch: {name}')
        o=self.organism; a=o.association; r=o.regulator; m=o.motor
        if len(o.cortices)!=4 or o.c.identity()!=c.identity() or self.solver.c.identity()!=c.identity(): raise ValueError('Snapshot configuration disagreement')
        if len(self.raw)!=4: raise ValueError('Raw channel schema mismatch')
        from .schema import RAW_WIDTHS
        for m,cortex in enumerate(self.organism.cortices):
            if cortex.x.shape!=(c.widths[m],) or cortex.integral.shape!=cortex.x.shape: raise ValueError('Cortex snapshot mismatch')
            if cortex.index!=m or [g.tolist() for g in cortex.groups]!=c.pools[m]: raise ValueError('Pool snapshot mismatch')
            d=RAW_WIDTHS[m]; w=c.widths[m]; g=len(c.pools[m])
            for name,shape in {'A':(w,w),'shared':(g,d),'fine':(w,d),'shared_ref':(g,d),'fine_ref':(w,d),'opening':(g,),'mean':(d,),'C':(w,w)}.items(): shaped(cortex,name,shape)
            if self.raw[m].shape!=(d,): raise ValueError('Raw width mismatch')
        keys={(i,j) for i in range(8) for j in range(8) if i!=j}
        if set(a.H)!=keys or set(a.use)!=keys: raise ValueError('Map inventory mismatch')
        for i,j in keys:
            if a.H[i,j].shape!=(c.gate_branches,c.central_widths[i],c.central_widths[j]) or a.use[i,j].shape!=(c.gate_branches,): raise ValueError('Map shape mismatch')
        shaped(a,'q',(c.central_width,))
        for collection in (a.means,a.traces):
            if len(collection)!=8 or any(x.shape!=(w,) for x,w in zip(collection,c.packet_widths)): raise ValueError('Packet context schema mismatch')
        for name in ('reference','eligibility'): shaped(r,name,(2,c.outputs,c.feature_width+1))
        for name,shape in {'body_mean':(2,),'Bq':(c.feature_width,c.central_width),'Bv':(c.feature_width,2),'bias':(c.feature_width,),'phi':(c.feature_width+1,),'xi':(2,c.outputs),'h':(c.group_count,),'current':(2,),'attenuation':(2,)}.items(): shaped(r,name,shape)
        for name in ('phase','nu','drive','tendency','command','integral'): shaped(o.motor,name,(2,))
        shaped(o.motor,'feedback',(2,15))
        for name,shape in {'position':(2,),'velocity':(2,),'command':(2,),'force':(2,),'contact_rates':(8,)}.items(): shaped(self.body,name,shape)
        if not 0<=self.organism.wave_elapsed<c.wave_dt+1e-12: raise ValueError('Invalid partial wave')
        from .records import state_bytes
        state_bytes(self)  # recursively rejects non-finite values
        return True
    def _coupled(self,dt,refresh,allow_terminal=False):
        command=self.organism.native(self.raw,dt,refresh_noise=refresh)
        events,actual,terminal=advance(self.c,self.body,self.stocks,self.time,self.phase,command,dt,allow_terminal)
        if actual<dt-self.c.event_time_tol and not allow_terminal: raise ArithmeticError('Short physics without terminal')
        self.fields=self.solver.step(self.fields,self.stocks,self.time+dt,self.phase,dt,self.body.position)
        self.time+=dt; self.last_events=events
        self.raw=transduce(self.c,self.body,self.fields,self.time,self.phase)
        return terminal
    def step(self):
        if self.status in ('failure','terminal','budget_complete'): raise RuntimeError('Stopped state cannot advance')
        old=copy.deepcopy(self); dt=self.c.native_dt
        refresh=self.native_index>0 and self.native_index%round(self.c.noise_refresh/dt)==0
        terminal=None
        try:
            try: terminal=self._coupled(dt,refresh)
            except TerminalCrossing as event:
                low=0.; high=dt; dimension=event.dimension
                for _ in range(80):
                    mid=(low+high)/2
                    candidate=copy.deepcopy(old)
                    try:
                        candidate._coupled(mid,refresh)
                        low=mid
                    except TerminalCrossing: high=mid
                    if high-low<=self.c.event_time_tol: break
                else: raise ArithmeticError('Terminal location did not converge')
                self.__dict__=copy.deepcopy(old.__dict__)
                terminal=self._coupled(high,refresh,True) or dimension
                dt=high
            self.native_index+=1
            self.last_wave=None
            if terminal:
                self.status='terminal'; self.terminal_dimension=terminal
            elif self.native_index%round(self.c.wave_dt/self.c.native_dt)==0:
                self.last_wave=self.organism.handoff(self.body.reserves)
            self.last_native=self.observe_native(dt)
            self.validate_state()
            return self.last_native,self.last_wave,self.last_events
        except Exception as error:
            self.__dict__=old.__dict__; self.status='failure'; self.failure=f'{type(error).__name__}: {error}'
            raise
    def observe_native(self,dt):
        o=self.organism
        import hashlib
        from .records import state_bytes
        return dict(schema_version=1,time=self.time,elapsed=dt,native_index=self.native_index,raw=[x.copy() for x in self.raw],reserves=self.body.reserves,position=self.body.position.copy(),angle=self.body.angle,velocity=self.body.velocity.copy(),omega=self.body.omega,commands=self.body.command.copy(),forces=self.body.force.copy(),contact_rates=self.body.contact_rates.copy(),stocks=self.stocks.copy(),controls=o.regulator.controls.copy(),sensory=[copy.deepcopy(x.diagnostic) for x in o.cortices],motor=copy.deepcopy(o.motor.diagnostic),field=copy.deepcopy(self.solver.last),status=self.status,random_counters=o.rng.counters.copy(),organism_sha256=hashlib.sha256(state_bytes(o)).hexdigest())

def run_bounded(engine,recorder,seconds):
    """Only the declared administrative budget; no autonomous continuation."""
    from .records import save_snapshot,load_snapshot,state_hash
    if seconds<0 or seconds>30 or engine.time+seconds>30+1e-10: raise ValueError('30-second engineering cap')
    steps=round(seconds/engine.c.native_dt)
    if abs(steps*engine.c.native_dt-seconds)>1e-10: raise ValueError('Budget must align to native steps')
    try:
        save_snapshot(recorder.path/'initial.snapshot.json.gz',engine)
        if state_hash(load_snapshot(recorder.path/'initial.snapshot.json.gz'))!=state_hash(engine): raise ValueError('Initial all-state restart mismatch')
        recorder.manifest['initial_restart_identical']=True
        for _ in range(steps):
            native,wave,events=engine.step()
            recorder.append('native',native)
            if wave is not None: recorder.append('wave',dict(time=engine.time,**wave))
            for event in events: recorder.append('events',event)
            if engine.native_index%1000==0: save_snapshot(recorder.path/f'native-{engine.native_index}.snapshot.json.gz',engine)
            if engine.status=='terminal': break
        if engine.status!='terminal': engine.status='paused'
        save_snapshot(recorder.path/'final.snapshot.json.gz',engine)
        recorder.close('terminal' if engine.terminal_dimension else 'administrative_pause',True)
    except Exception as error:
        engine.status='failure'; engine.failure=f'{type(error).__name__}: {error}'
        try: save_snapshot(recorder.path/'failure.snapshot.json.gz',engine)
        except OSError: pass
        try: recorder.close('apparatus_failure',False,engine.failure)
        except OSError: pass
        raise
