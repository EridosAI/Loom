"""Bounded native scheduler, append-only segments and exact all-state restart."""
import copy
import gzip
import json
import os
from pathlib import Path
import time
import numpy as np
from loom_p.records import Recorder, pack, unpack, strict_bytes, state_hash, view
from . import adapter, diagnostics
from .contract import (INTACT, FIXED, EXTERNAL, validate_manifest, authorize_execution,
                       apparatus_identity, digest, require)
from .controllers import SensorHistory, privileged_input, waypoint_command, command_pair, observe_without_interference

def save_restart(path, engine, session, manifest):
    payload=pack({'engine':engine,'session':session})
    wrapper={'manifest':manifest,'state':payload,'sha256':digest(strict_bytes(payload))}
    data=gzip.compress(strict_bytes(wrapper),mtime=0)
    path=Path(path); temporary=path.with_suffix(path.suffix+'.partial')
    with temporary.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(temporary,path)
    return digest(data)

def load_restart(path):
    wrapper=json.loads(gzip.decompress(Path(path).read_bytes()))
    require(digest(strict_bytes(wrapper['state']))==wrapper['sha256'], 'restart checksum mismatch')
    restored=unpack(wrapper['state']); e=restored['engine']; s=restored['session']; m=wrapper['manifest']
    e.validate_state(); validate_manifest(m,e,initial=False); authorize_execution(m)
    require(s['contract_sha256']==digest(strict_bytes(m)), 'restart manifest identity mismatch')
    require(e.time<=m['hard_stop_time']+1e-9, 'duration cap bypass')
    if m['mode']==FIXED: adapter.validate_frozen(e.organism,s['frozen'])
    return e,s,m

class Run:
    """One continuing trajectory. Resumes retain the original hard ceiling.

    No constructor evolves a world. Each explicit call advances native steps,
    not a succession of Engine.run_bounded calls. An external decision owns ten
    native steps, including across a pause/restart in the middle of its hold.
    """
    def __init__(self, engine, manifest, output, *, session=None, parent=None, plan=None,
                 observer=diagnostics.passive, storage_limit=1_000_000_000, wall_limit=3600):
        validate_manifest(manifest,engine,initial=session is None); authorize_execution(manifest)
        require(engine.status not in ('failure','terminal','budget_complete'), 'stopped state cannot resume')
        self.engine=engine; self.manifest=copy.deepcopy(manifest); self.observer=observer
        self.closed=False; self.started=time.perf_counter(); self.wall_limit=wall_limit
        self.storage_limit=storage_limit
        if session is None:
            require(np.isfinite(wall_limit) and wall_limit>0 and type(storage_limit)==int and storage_limit>0, 'explicit finite resource limits required')
            if manifest['mode']==FIXED:
                o=engine.organism
                require(o.native_count==o.wave_count==0 and not np.any(o.regulator.theta)
                        and not np.any(o.regulator.reference)
                        and all(not np.any(v) for v in o.association.H.values())
                        and all(not np.any(v) for v in o.association.use.values()), 'fixed diagnostic must start from newborn structure')
            history=SensorHistory(engine)
            self.session={'contract_sha256':digest(strict_bytes(manifest)), 'frozen':adapter.structure(engine.organism) if manifest['mode']==FIXED else None,
                'sensor':vars(history),'hold_remaining':0,'held_command':[0.,0.], 'route':copy.deepcopy(plan),
                'cursor':0,'advanced':0,'field_updates':0,'body_wave_samples':0,
                'wall_seconds_used':0.,'bytes_used':0,'wall_limit':wall_limit,'storage_limit':storage_limit,
                'stop_reason':'administrative_pause'}
        else:
            self.session=copy.deepcopy(session)
            self.wall_limit=self.session['wall_limit']; self.storage_limit=self.session['storage_limit']
        self.sensor=SensorHistory.__new__(SensorHistory); self.sensor.__dict__=self.session['sensor']
        self.recorder=Recorder(output,dict(contract=self.manifest,parent=parent,mode=manifest['mode']),storage_limit=self.storage_limit-self.session['bytes_used'])
        for name in ('diagnostics','controller','sensor','scientific_observations'):
            self.recorder.streams[name]=gzip.open(self.recorder.path/(name+'.jsonl.gz'),'wb')
        save_restart(self.recorder.path/'initial.restart.json.gz',engine,self.session,self.manifest)
        self.recorder.append('sensor',self.sensor.display())

    @classmethod
    def resume(cls, previous, output, **kwargs):
        previous=Path(previous)
        receipt=json.loads((previous/'manifest.json').read_bytes())
        require(receipt['complete'] and receipt['status']=='administrative_pause', 'only complete pauses can resume')
        for filename,identity in receipt['files'].items():
            require(digest((previous/filename).read_bytes())==identity['sha256'], 'resume record checksum mismatch')
        e,s,m=load_restart(previous/'final.restart.json.gz')
        require(receipt['contract']==m, 'resume contract mismatch')
        return cls(e,m,output,session=s,parent={'manifest_sha256':digest((previous/'manifest.json').read_bytes())},**kwargs)

    def _guard(self):
        require(not self.closed, 'closed segment')
        require(digest(strict_bytes(self.manifest))==self.session['contract_sha256'], 'manifest changed during run')
        require(self.engine.phase==self.manifest['phase'], 'wrong field/mover phase')
        require(self.engine.c.identity()==self.manifest['configuration'], 'configuration identity mismatch')
        require(self.engine.time<=self.manifest['hard_stop_time']+1e-9, 'duration cap bypass')

    def remaining(self):
        return max(0,round((self.manifest['hard_stop_time']-self.engine.time)/self.engine.c.native_dt))

    def begin_command(self, command=None, annotation=''):
        self._guard()
        require(self.manifest['mode']==EXTERNAL and self.session['hold_remaining']==0, 'command hold already active or no external controller')
        require(self.remaining()>0, 'duration cap reached')
        kind=self.manifest['controller']; inputs=None
        if kind=='waypoint':
            require(command is None, 'manual override of deterministic controller')
            inputs=observe_without_interference(self.engine,privileged_input)
            command,cursor=waypoint_command(copy.deepcopy(inputs),self.session['route'],self.session['cursor'])
            self.session['cursor']=cursor
        elif kind=='manual_privileged':
            inputs=observe_without_interference(self.engine,privileged_input)
        elif kind=='sensor_human':
            inputs=self.sensor.display()
        command=command_pair(command)
        self.session['held_command']=command.tolist(); self.session['hold_remaining']=min(10,self.remaining())
        action={'time':self.engine.time,'actor':EXTERNAL,'controller':kind,'inputs':inputs,
                'command':command.tolist(),'hold_native_steps':self.session['hold_remaining'],'annotation':str(annotation)}
        self.recorder.append('controller',action)
        self.sensor.payload['own_commands'].append({'time':self.engine.time,'command':command.tolist()})
        if annotation: self.sensor.payload['annotations'].append({'time':self.engine.time,'text':str(annotation)})

    def advance(self, native_steps):
        self._guard()
        require(type(native_steps)==int and 0<=native_steps<=self.remaining(), 'duration cap bypass')
        if self.manifest['mode']==EXTERNAL:
            require(native_steps<=self.session['hold_remaining'], 'controller hold cannot insert extra steps')
        try:
            for _ in range(native_steps):
                self._guard()
                if self.session['wall_seconds_used']+time.perf_counter()-self.started>=self.wall_limit:
                    self.close('administrative_pause',cause='wall_time_limit'); break
                # Clean soft storage stop BEFORE stepping; I/O errors below are failures.
                reserve=max(16_000_000,2*self.recorder.widths.get('diagnostics',{}).get('max',0)*30)
                if self.session['bytes_used']+self.recorder.bytes_uncompressed+reserve>self.storage_limit:
                    self.close('administrative_pause',cause='storage_reserve'); break
                before=copy.deepcopy(self.engine)
                n,w,events,discarded=adapter.step(self.engine,self.manifest['mode'],
                    self.session['held_command'],self.session['frozen'])
                self.session['advanced']+=1; self.session['field_updates']+=1
                if self.manifest['mode']==EXTERNAL:
                    self.session['hold_remaining']-=1
                    n={k:v for k,v in n.items() if k not in ('sensory','motor','controls','organism_sha256')}
                    n['neural_state']='inactive_newborn_not_P'
                n=dict(n,mode=self.manifest['mode'],field_phase=self.engine.phase,
                       field_sha256=digest(self.engine.fields.tobytes()))
                self.recorder.append('native',n)
                if w is not None: self.recorder.append('wave',dict(time=self.engine.time,mode=self.manifest['mode'],**w))
                for event in events: self.recorder.append('events',dict(event,mode=self.manifest['mode']))
                if self.engine.native_index%20==0 and self.engine.status!='terminal': self.session['body_wave_samples']+=1
                before_hash=state_hash(self.engine)
                diagnostic=self.observer(before,self.engine,w,self.manifest['mode'],discarded)
                require(before_hash==state_hash(self.engine), 'observer RNG/state interference')
                self.recorder.append('diagnostics',diagnostic)
                self.sensor.observe(self.engine)
                self.recorder.append('sensor',self.sensor.payload['history'][-1])
                if self.engine.native_index%1000==0:
                    save_restart(self.recorder.path/f'native-{self.engine.native_index}.restart.json.gz',self.engine,self.session,self.manifest)
                if self.engine.status=='terminal': self.close('terminal'); break
                if self.remaining()==0: self.close('administrative_cutoff'); break
        except Exception as error:
            self.engine.status='failure'; self.engine.failure=f'{type(error).__name__}: {error}'
            if not self.closed: self.close('apparatus_failure',error=self.engine.failure)
            raise

    def hold(self, command=None, annotation=''):
        if self.session['hold_remaining']==0: self.begin_command(command,annotation)
        else: require(command is None, 'cannot replace an interrupted held command')
        self.advance(self.session['hold_remaining'])

    def display(self):
        return self.sensor.display()  # no time/RNG/field update

    def preserve_scientific_observation(self, observation):
        from .contract import classify
        self.recorder.append('scientific_observations',classify('S1',observation))

    def close(self, reason='administrative_pause', cause=None, error=None):
        require(not self.closed, 'segment already closed')
        from .validators import validate_stop
        validate_stop(reason,self.engine,self.manifest)
        if reason not in ('terminal','apparatus_failure'): self.engine.status='paused'
        self.session['stop_reason']=reason
        self.session['wall_seconds_used']+=time.perf_counter()-self.started
        self.session['bytes_used']+=self.recorder.bytes_uncompressed
        try:
            save_restart(self.recorder.path/'final.restart.json.gz',self.engine,self.session,self.manifest)
            (self.recorder.path/'sensor-display.json').write_bytes(strict_bytes(self.display()))
            self.recorder.manifest.update(stop_cause=cause,final_state=state_hash(self.engine),
                final_time=self.engine.time,terminal_dimension=self.engine.terminal_dimension,
                session_counters={k:self.session[k] for k in ('advanced','field_updates','body_wave_samples')})
            self.recorder.close(reason,reason!='apparatus_failure',error)
        except Exception as failure:
            self.recorder.close('apparatus_failure',False,str(failure))
            raise
        finally: self.closed=True
