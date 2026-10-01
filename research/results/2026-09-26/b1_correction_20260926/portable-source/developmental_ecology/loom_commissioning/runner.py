"""Bounded native scheduler, append-only segments and exact all-state restart."""
import copy
import gzip
import json
import os
from pathlib import Path
import time
import numpy as np
from loom_p.records import Recorder, pack, unpack, strict_bytes, state_hash, view
from . import adapter, diagnostics, clock
from .contract import (INTACT, FIXED, EXTERNAL, validate_manifest, authorize_execution,
                       apparatus_identity, digest, require)
from .controllers import SensorHistory, privileged_input, waypoint_command, command_pair, observe_without_interference
from .controllers import time_due
from .authority import execution_sha256, validate_execution, validate_session, canonical, strict_loads, validate_dispatch
from .pending import RestoredSession, validate_restored, validate_pending, validate_decision, decision_stage

def save_restart(path, engine, session, manifest):
    if engine.status!='failure': validate_pending(manifest,session,engine)
    payload=pack({'engine':engine,'session':session})
    wrapper={'manifest':manifest,'state':payload,'sha256':digest(strict_bytes(payload))}
    data=gzip.compress(strict_bytes(wrapper),mtime=0)
    path=Path(path); temporary=path.with_suffix(path.suffix+'.partial')
    with temporary.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(temporary,path)
    return digest(data)

def load_restart(path):
    wrapper=strict_loads(gzip.decompress(Path(path).read_bytes()))
    require(digest(strict_bytes(wrapper['state']))==wrapper['sha256'], 'restart checksum mismatch')
    # P's packed dictionary representation is a pair list. Reject duplicate
    # semantic keys before its unchanged unpacker could collapse them.
    def packed_keys(value):
        if isinstance(value,list):
            for item in value: packed_keys(item)
        elif isinstance(value,dict):
            if '$dict' in value:
                seen=set()
                for key,item in value['$dict']:
                    unpacked=unpack(key)
                    require(unpacked not in seen,'duplicate packed state key')
                    seen.add(unpacked); packed_keys(item)
            else:
                for item in value.values(): packed_keys(item)
    packed_keys(wrapper['state'])
    restored=unpack(wrapper['state']); e=restored['engine']; s=restored['session']; m=wrapper['manifest']
    e.validate_state(); validate_manifest(m,e,initial=False); authorize_execution(m)
    require(s['contract_sha256']==digest(strict_bytes(m)), 'restart manifest identity mismatch')
    validate_session(m,s)
    validate_pending(m,s,e)
    require(e.native_index<=clock.case_end(m), 'duration cap bypass')
    if m['mode']==FIXED: adapter.validate_frozen(e.organism,s['frozen'])
    return e,RestoredSession(s,e,m,path),m

class Run:
    """One continuing trajectory. Resumes retain the original hard ceiling.

    No constructor evolves a world. Each explicit call advances native steps,
    not a succession of Engine.run_bounded calls. An external decision owns ten
    native steps, including across a pause/restart in the middle of its hold.
    """
    def __init__(self, engine, manifest, output, *, session=None, parent=None, plan=None,
                 observer=diagnostics.passive, storage_limit=None, wall_limit=None):
        validate_manifest(manifest,engine,initial=session is None); authorize_execution(manifest)
        validate_execution(manifest,complete=True)
        dispatch=validate_dispatch(manifest,globals())
        require(observer is diagnostics.passive, 'unapproved observer implementation')
        scope=manifest['execution']; resources=scope['resources']
        require(plan is None or plan==scope['procedure']['stages'], 'supplied route differs from approved procedure')
        storage_limit=resources['storage_limit_bytes'] if storage_limit is None else storage_limit
        wall_limit=resources['wall_limit_seconds'] if wall_limit is None else wall_limit
        require(storage_limit==resources['storage_limit_bytes'] and wall_limit==resources['wall_limit_seconds'],
                'supplied resources differ from approved scope')
        if session is not None:
            require('operator_lifecycle' not in session,'interactive cases cannot resume')
            validate_session(manifest,session); validate_restored(session,engine,manifest)
            validate_pending(manifest,session,engine)
            previous=session._origin.parent
            receipt=strict_loads((previous/'manifest.json').read_bytes())
            require(session._origin.name=='final.restart.json.gz' and receipt['complete']
                    and receipt['status']=='administrative_pause','only complete pauses can resume')
            from .validators import verify_segment
            verify_segment(previous,replay=False)
            require(digest(session._origin.read_bytes())==receipt['files']['final.restart.json.gz']['sha256'],
                    'resume origin checksum mismatch')
            original,original_session,original_manifest=load_restart(session._origin)
            require(state_hash(engine)==state_hash(original) and manifest==original_manifest
                    and state_hash(dict(session))==state_hash(dict(original_session)), 'resume differs from verified origin')
            expected_parent={'manifest_sha256':digest((previous/'manifest.json').read_bytes()),
                             'segment':os.path.relpath(previous,Path(output).resolve())}
            require(parent is None or parent==expected_parent,'resume parent continuity mismatch')
            parent=expected_parent
        else: require(parent is None,'parent supplied without loaded session')
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
            history=dispatch['SensorHistory'](engine)
            self.session={'contract_sha256':digest(strict_bytes(manifest)), 'frozen':adapter.structure(engine.organism) if manifest['mode']==FIXED else None,
                'execution_sha256':execution_sha256(manifest),
                'decision':None,
                'sensor':vars(history),'hold_remaining':0,'held_command':[0.,0.], 'route':copy.deepcopy(scope['procedure']['stages']),
                'cursor':0,'advanced':0,'field_updates':0,'body_wave_samples':0,
                'wall_seconds_used':0.,'bytes_used':0,'wall_limit':wall_limit,'storage_limit':storage_limit,
                'stop_reason':'administrative_pause'}
        else:
            self.session=copy.deepcopy(dict(session))
            self.wall_limit=self.session['wall_limit']; self.storage_limit=self.session['storage_limit']
        self._decision_seal=canonical(self.session['decision'])
        history_type=dispatch['SensorHistory']
        self.sensor=history_type.__new__(history_type); self.sensor.__dict__=self.session['sensor']
        self.recorder=Recorder(output,dict(contract=self.manifest,parent=parent,mode=manifest['mode']),storage_limit=self.storage_limit-self.session['bytes_used'])
        for name in ('diagnostics','controller','sensor','scientific_observations'):
            self.recorder.streams[name]=gzip.open(self.recorder.path/(name+'.jsonl.gz'),'wb')
        save_restart(self.recorder.path/'initial.restart.json.gz',engine,self.session,self.manifest)
        self.recorder.append('sensor',self.sensor.display())

    @classmethod
    def resume(cls, previous, output, **kwargs):
        previous=Path(previous)
        receipt=strict_loads((previous/'manifest.json').read_bytes())
        require(receipt['complete'] and receipt['status']=='administrative_pause', 'only complete pauses can resume')
        for filename,identity in receipt['files'].items():
            require(digest((previous/filename).read_bytes())==identity['sha256'], 'resume record checksum mismatch')
        e,s,m=load_restart(previous/'final.restart.json.gz')
        require(receipt['contract']==m, 'resume contract mismatch')
        return cls(e,m,output,session=s,**kwargs)

    def _guard(self):
        require(not self.closed, 'closed segment')
        require(digest(strict_bytes(self.manifest))==self.session['contract_sha256'], 'manifest changed during run')
        validate_session(self.manifest,self.session)
        validate_execution(self.manifest,complete=True)
        dispatch=validate_dispatch(self.manifest,globals())
        validate_pending(self.manifest,self.session,self.engine,self._decision_seal)
        require(self.wall_limit==self.session['wall_limit'] and self.storage_limit==self.session['storage_limit'],
                'live resources differ from approved scope')
        require(self.engine.phase==self.manifest['phase'], 'wrong field/mover phase')
        require(self.engine.c.identity()==self.manifest['configuration'], 'configuration identity mismatch')
        require(self.engine.native_index<=clock.case_end(self.manifest), 'duration cap bypass')
        return dispatch

    def remaining(self):
        return max(0,clock.case_end(self.manifest)-self.engine.native_index)

    def begin_command(self, command=None, annotation=''):
        dispatch=self._guard()
        require(self.session.get('operator_lifecycle','running')=='running','operator case is not running')
        require(self.manifest['mode']==EXTERNAL and self.session['hold_remaining']==0, 'command hold already active or no external controller')
        require(self.remaining()>0, 'duration cap reached')
        kind=self.manifest['controller']; inputs=None
        cursor=0
        if kind=='waypoint':
            require(command is None, 'manual override of deterministic controller')
            inputs=dispatch['observe_without_interference'](self.engine,dispatch['privileged_input'])
            # Clock/approved stages determine the decision; a mutable saved
            # cursor cannot skip a prescribed stage on restart.
            approved_plan=copy.deepcopy(self.manifest['execution']['procedure']['stages'])
            command,cursor=dispatch['waypoint_command'](copy.deepcopy(inputs),approved_plan,
                clock.decision_clock(self.manifest,self.engine.native_index))
            require(approved_plan==self.manifest['execution']['procedure']['stages'], 'controller mutated its approved route input')
            until=clock.stage_ends(self.manifest)[cursor]
            require(not dispatch['time_due'](self.engine.native_index,until), 'route complete; no command hold authorized')
            end=self.engine.native_index+clock.hold_steps(self.manifest,self.engine.native_index)
            # Preserve the reviewed full ten-step hold (and existing global cap).
            # An incompatible prescription is rejected; no partial stage hold,
            # early transition, time extension or compensating later cut is invented.
            require(end<=until, 'command hold would cross prescribed stage boundary')
        elif kind=='manual_privileged':
            inputs=dispatch['observe_without_interference'](self.engine,dispatch['privileged_input'])
        elif kind=='sensor_human':
            inputs=self.display()
        command=dispatch['command_pair'](command)
        self._guard()  # Revalidate the actual dispatch/configuration before accepting its result.
        action={'time':self.engine.time,'native_index':self.engine.native_index,'actor':EXTERNAL,'controller':kind,'inputs':inputs,
                'command':command.tolist(),'hold_native_steps':clock.hold_steps(self.manifest,self.engine.native_index),'annotation':str(annotation),
                'execution_sha256':execution_sha256(self.manifest),'stage':decision_stage(self.manifest,inputs,self.engine.native_index),
                'case_deadline':self.manifest['hard_stop_time']}
        validate_decision(self.manifest,action)
        self.session['decision']=copy.deepcopy(action); self._decision_seal=canonical(action)
        self.session['held_command']=command.tolist(); self.session['hold_remaining']=action['hold_native_steps']
        self.session['cursor']=cursor
        self.recorder.append('controller',action)
        self.sensor.payload['own_commands'].append({'time':self.engine.time,'command':command.tolist()})
        if annotation: self.sensor.payload['annotations'].append({'time':self.engine.time,'text':str(annotation)})

    def advance(self, native_steps):
        self._guard()
        require(self.session.get('operator_lifecycle','running')=='running','operator case is not running')
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
                # Actuation consumes the sealed issued command, never a second
                # lookup of an exposed mutable pair after its validation.
                issued=strict_loads(self._decision_seal)
                held=issued['command'] if issued is not None else [0.,0.]
                n,w,events,discarded=adapter.step(self.engine,self.manifest['mode'],
                    held,self.session['frozen'])
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
        from .operator_view import project
        result=project(self.sensor.display(),self.manifest['execution']['display_intervention'])
        if self.closed or self.session.get('operator_lifecycle')=='ended':result['availability']='unavailable'
        return result  # no time/RNG/field update; raw SensorHistory stays complete

    def preserve_scientific_observation(self, observation):
        from .contract import classify
        self.recorder.append('scientific_observations',classify('S1',observation))

    def close(self, reason='administrative_pause', cause=None, error=None):
        require(not self.closed, 'segment already closed')
        if reason!='apparatus_failure': self._guard()
        from .validators import validate_stop
        validate_stop(reason,self.engine,self.manifest)
        if reason not in ('terminal','apparatus_failure'): self.engine.status='paused'
        self.session['stop_reason']=reason
        if 'operator_lifecycle' in self.session:self.session['operator_lifecycle']='ended'
        self.session['wall_seconds_used']+=time.perf_counter()-self.started
        try:
            if 'operator' in self.recorder.streams:
                self.recorder.append('operator',dict(event='ended',lifecycle='ended',
                    wall_seconds=self.session['wall_seconds_used'],
                    display_condition=self.manifest['execution']['display_intervention']['kind'],
                    display_sha256=digest(strict_bytes(self.display()))))
            self.session['bytes_used']+=self.recorder.bytes_uncompressed
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
