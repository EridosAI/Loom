"""Issued-command provenance and native progress; no world advancement."""
import copy
from pathlib import Path
from types import SimpleNamespace
from .authority import canonical, execution_sha256
from .contract import require, digest, EXTERNAL
from . import controllers as c
from . import clock
from loom_p.records import state_hash
from . import raw_reference as reference

class RestoredSession(dict):
    """Loaded values plus a separate immutable-by-value read receipt.

    Public dictionary edits do not update the read receipt. This is workflow
    integrity, not a security boundary against arbitrary Python object surgery.
    """
    def __init__(self,values,engine,manifest,path):
        super().__init__(values)
        self._seal=state_hash(values)  # frozen diagnostic structures include NumPy arrays
        self._engine_hash=state_hash(engine)
        self._manifest=canonical(manifest)
        self._origin=Path(path).resolve()

def validate_restored(s,e,m):
    require(type(s) is RestoredSession, 'resume requires a verified loaded session')
    require(state_hash(dict(s))==s._seal and state_hash(e)==s._engine_hash
            and canonical(m)==s._manifest, 'loaded pending/session state changed before resume')

def decision_stage(m,inputs,native_index):
    if m['controller']!='waypoint': return None
    plan=copy.deepcopy(m['execution']['procedure']['stages'])
    command,index=c.waypoint_command(copy.deepcopy(inputs),plan,clock.decision_clock(m,native_index))
    stage=plan[index]
    return {'index':index,'identity':digest(canonical(stage)),
            'start_time':m['initial_time'] if index==0 else plan[index-1]['until'],
            'deadline':stage['until']}

def validate_decision(m,d):
    keys={'time','native_index','actor','controller','inputs','command','hold_native_steps','annotation',
          'execution_sha256','stage','case_deadline'}
    if m['controller']==reference.KIND:keys|={'reference_state_before','reference_state_after'}
    require(type(d) is dict and set(d)==keys, 'issued decision schema mismatch')
    require(d['execution_sha256']==execution_sha256(m) and d['case_deadline']==m['hard_stop_time']
            and d['actor']==EXTERNAL and m['mode']==EXTERNAL and d['controller']==m['controller'],
            'issued decision authority mismatch')
    clock.validate_physical_time(m,d['native_index'],d['time'])
    command=c.command_pair(d['command'])
    steps=clock.hold_steps(m,d['native_index'])
    require(type(d['hold_native_steps']) is int and d['hold_native_steps']==steps and steps>0,
            'issued hold length mismatch')
    if m['controller']=='waypoint':
        c.validate_privileged(d['inputs'])
        require(d['inputs']['time']==d['time'], 'issued controller input clock mismatch')
        expected,_=c.waypoint_command(copy.deepcopy(d['inputs']),copy.deepcopy(m['execution']['procedure']['stages']),
                                     clock.decision_clock(m,d['native_index']))
        require(command.tolist()==expected.tolist(), 'issued command differs from approved controller')
    elif m['controller']=='manual_privileged': c.validate_privileged(d['inputs'])
    elif m['controller']==reference.KIND:
        arm=reference.arm_from_manifest(m)
        expected,after=reference.command(d['inputs'],d['reference_state_before'],arm)
        require(d['command']==expected and d['reference_state_after']==after and d['annotation']=='',
                'issued reference decision differs from fixed law')
        if d['inputs'] is not None:
            last=d['inputs']['history'][-1]
            require(last['native_index']==d['native_index'] and last['time']==d['time'],
                    'issued reference input clock mismatch')
    else:
        from .operator_view import validate_operator_payload
        validate_operator_payload(d['inputs'],m['execution']['display_intervention'])
    require(d['stage']==decision_stage(m,d['inputs'],d['native_index']), 'issued stage identity mismatch')
    if d['stage'] is not None:
        until=clock.stage_ends(m)[d['stage']['index']]; end=d['native_index']+steps
        require(d['native_index']<until and end<=until,
                'issued hold crosses stage authority')

def validate_pending(m,s,e,seal=None):
    clock.validate_physical_time(m,e.native_index,e.time,e.status=='terminal')
    d=s.get('decision')
    if m['controller']==reference.KIND:
        reference.validate_state(s['reference_state'])
        require(s['reference_state']==(reference.initial_state() if d is None else d['reference_state_after']),
                'reference memory differs from issued decision')
    if seal is not None:
        require(canonical(d)==seal, 'issued decision changed during segment')
    if d is None:
        require(s['hold_remaining']==0 and s['held_command']==[0.,0.], 'pending command has no issued decision')
        return
    validate_decision(m,d)
    progress=e.native_index-d['native_index']
    require(type(s['hold_remaining']) is int and 0<=progress<=d['hold_native_steps']
            and s['hold_remaining']==d['hold_native_steps']-progress, 'pending remainder differs from issued native progress')
    require(s['held_command']==d['command'], 'pending command differs from issued decision')
    require(s['cursor']==(d['stage']['index'] if d['stage'] is not None else 0), 'pending stage cursor mismatch')
    expected_time=d['time']+progress*e.c.native_dt
    if e.status!='terminal':
        require(abs(e.time-expected_time)<=e.c.event_time_tol, 'pending command elapsed time mismatch')
    else:
        require(expected_time-e.c.native_dt-e.c.event_time_tol<=e.time<=expected_time+e.c.event_time_tol,
                'terminal pending elapsed time mismatch')
    if s['hold_remaining']:
        end=e.native_index+s['hold_remaining']
        require(end<=clock.case_end(m), 'pending hold crosses case authority')
        if d['stage'] is not None:
            until=clock.stage_ends(m)[d['stage']['index']]
            require(e.native_index<until and end<=until,
                    'pending hold crosses stage authority')

def validate_journal(initial,session,final,finish,m,actions,native):
    """Tie both snapshots to issued action records, independently of replay."""
    working={'decision':copy.deepcopy(session['decision']),'held_command':session['held_command'].copy(),
             'hold_remaining':session['hold_remaining'],'cursor':session['cursor']}
    if m['controller']==reference.KIND:working['reference_state']=copy.deepcopy(session['reference_state'])
    index=initial.native_index; now=initial.time; offset=0
    def issue_at_current_clock():
        nonlocal offset
        while offset<len(actions) and actions[offset]['native_index']==index:
            d=actions[offset]
            require(working['hold_remaining']==0,'new decision interrupts pending hold')
            validate_decision(m,d)
            if m['controller']==reference.KIND:
                require(d['reference_state_before']==working['reference_state'],'reference journal memory discontinuity')
                working['reference_state']=copy.deepcopy(d['reference_state_after'])
            require(abs(d['time']-now)<=initial.c.event_time_tol, 'recorded decision clock mismatch')
            working.update(decision=copy.deepcopy(d),held_command=d['command'].copy(),
                           hold_remaining=d['hold_native_steps'],cursor=d['stage']['index'] if d['stage'] else 0)
            offset+=1
    for row in native:
        issue_at_current_clock()
        clock=SimpleNamespace(native_index=index,time=now,c=initial.c,status='active')
        validate_pending(m,working,clock)
        if m['mode']==EXTERNAL:
            require(working['hold_remaining']>0,'native record lacks authorized pending command')
            working['hold_remaining']-=1
        index=row['native_index']; now=row['time']
    issue_at_current_clock()
    require(offset==len(actions),'unconsumed or out-of-order controller decision')
    for key in ('decision','held_command','hold_remaining','cursor')+ (('reference_state',) if m['controller']==reference.KIND else ()):
        require(canonical(finish[key])==canonical(working[key]),'pending decision journal continuity mismatch: '+key)
    validate_pending(m,finish,final)
