"""Consequential AV validators. No useful behavior or survival requirement."""
import gzip
import json
from pathlib import Path
import numpy as np
from loom_p.records import strict_bytes, view, state_hash
from .contract import require, digest, EXTERNAL, FIXED
from .controllers import validate_sensor_payload, validate_privileged, SensorHistory
from . import adapter, clock
from .authority import strict_loads, canonical
from .pending import validate_journal

def validate_stop(reason,e,m):
    require(reason in ('terminal','administrative_cutoff','administrative_pause','apparatus_failure'), 'mislabelled stop reason')
    if reason=='terminal':
        require(e.status=='terminal' and e.terminal_dimension in ('energy','integrity') and min(e.body.reserves)<=1e-9,
                'mislabelled stop reason')
    elif reason=='apparatus_failure':
        require(e.status=='failure' and bool(e.failure), 'mislabelled stop reason')
    else:
        require(e.terminal_dimension is None and e.status not in ('failure','terminal'), 'mislabelled stop reason')
        if reason=='administrative_cutoff':
            require(e.native_index==clock.case_end(m), 'mislabelled stop reason')
        else: require(e.native_index<clock.case_end(m), 'mislabelled stop reason')
    if reason!='apparatus_failure':
        clock.validate_physical_time(m,e.native_index,e.time,e.status=='terminal')

def validate_ledger(records, tolerance=1e-12):
    maximum=0.
    for r in records:
        # Release markers also carry complete zero-duration accounting.
        transfer=np.asarray(r['transfer']); renew=np.asarray(r['renewal_first'])+r['renewal_second']
        energy=(r['energy_after']-r['energy_before'])-(float(transfer.sum())-r['expenditure'])
        stock=np.asarray(r['stock_after'])-r['stock_before']-renew+transfer
        integrity=r['integrity_after']-r['integrity_before']-(r['repair']-r['damage'])
        maximum=max(maximum,abs(energy),float(np.max(abs(stock))),abs(integrity))
        require(maximum<=tolerance, 'source debit/body credit mismatch')
        if r['duration']==0:
            require(not np.any(transfer) and r['expenditure']==r['repair']==0, 'zero-duration exchange')
    return maximum

def validate_native_sequence(native,initial,final,m):
    require(len(native)==final.native_index-initial.native_index, 'missing native record')
    t=initial.time
    for i,n in enumerate(native,initial.native_index+1):
        require(n['native_index']==i and 0<n['elapsed']<=initial.c.native_dt+1e-12, 'missing native record')
        t+=n['elapsed']
        require(abs(n['time']-t)<1e-10, 'missing native record')
        require(n['field_phase']==m['phase'], 'wrong field/mover phase')
        require(n['mode']==m['mode'], 'external controller incorrectly labelled intact P')
    require(abs(t-final.time)<1e-10 and final.native_index<=clock.case_end(m), 'duration cap bypass')
    clock.validate_physical_time(m,final.native_index,final.time,final.status=='terminal')

def read_stream(path):
    with gzip.open(path,'rt',encoding='utf-8') as f: return [strict_loads(line) for line in f]

def verify_segment(directory, replay=True, _ancestors=()):
    """Native reconstruction verifies committed field/RNG/update counts too.

    This replays ONLY this existing segment and never auto-continues it. For the
    present build every segment is a manufactured <=0.6 s component fixture.
    """
    from .runner import load_restart
    directory=Path(directory).resolve()
    require(directory not in _ancestors,'cyclic segment ancestry')
    receipt=strict_loads((directory/'manifest.json').read_bytes())
    require(receipt['complete'], 'incomplete apparatus records')
    for name,expected in receipt['files'].items():
        data=(directory/name).read_bytes()
        require(len(data)==expected['bytes'] and digest(data)==expected['sha256'], 'record checksum mismatch')
    initial,session,m=load_restart(directory/'initial.restart.json.gz')
    final,finish,m2=load_restart(directory/'final.restart.json.gz')
    require(m==m2==receipt['contract'], 'manifest identity mismatch')
    parent=receipt.get('parent')
    if parent is None:
        require(state_hash(initial)==m['initial_state'] and initial.native_index==m['initial_index']
                and session['decision'] is None, 'unanchored initial pending decision')
    else:
        require(set(parent)=={'segment','manifest_sha256'}, 'resume parent schema mismatch')
        previous=(directory/parent['segment']).resolve()
        require(digest((previous/'manifest.json').read_bytes())==parent['manifest_sha256'], 'resume parent checksum mismatch')
        verify_segment(previous,replay=False,_ancestors=(*_ancestors,directory))
        old,old_session,old_manifest=load_restart(previous/'final.restart.json.gz')
        require(m==old_manifest and state_hash(initial)==state_hash(old)
                and state_hash(dict(session))==state_hash(dict(old_session)), 'cross-segment pending/state continuity mismatch')
    native=read_stream(directory/'native.jsonl.gz'); waves=read_stream(directory/'wave.jsonl.gz')
    events=read_stream(directory/'events.jsonl.gz'); actions=read_stream(directory/'controller.jsonl.gz')
    diagnostic=read_stream(directory/'diagnostics.jsonl.gz')
    validate_journal(initial,session,final,finish,m,actions,native)
    validate_native_sequence(native,initial,final,m); validate_stop(receipt['status'],final,m)
    require(len(diagnostic)==len(native), 'missing native diagnostic record')
    for kind in ('native','wave','events','controller','diagnostics','sensor','scientific_observations'):
        require(len(read_stream(directory/(kind+'.jsonl.gz')))==receipt['records'].get(kind,0), 'record count mismatch')
    maximum=validate_ledger(events,initial.c.arithmetic_tol)
    payload=strict_loads((directory/'sensor-display.json').read_bytes()); validate_sensor_payload(payload)
    for action in actions:
        require(action['actor']==EXTERNAL and m['mode']==EXTERNAL, 'external controller incorrectly labelled intact P')
        if action['controller']=='sensor_human': validate_sensor_payload(action['inputs'])
        else: validate_privileged(action['inputs'])
    if replay:
        e=initial; wave_index=0; replay_events=[]
        history=SensorHistory.__new__(SensorHistory); history.__dict__=session['sensor']
        commands={x['native_index']:x for x in actions}
        held=session['held_command']; remaining=session['hold_remaining']
        for n in native:
            if m['mode']==EXTERNAL:
                if remaining==0:
                    action=commands.get(e.native_index); require(action is not None,'missing controller decision')
                    held=action['command']; remaining=action['hold_native_steps']
                remaining-=1
            actual,w,ev,discarded=adapter.step(e,m['mode'],held,session['frozen'])
            history.observe(e)
            replay_events.extend(dict(x,mode=m['mode']) for x in ev)
            if m['mode']==EXTERNAL:
                actual={k:v for k,v in actual.items() if k not in ('sensory','motor','controls','organism_sha256')}
                actual['neural_state']='inactive_newborn_not_P'
            actual=dict(actual,mode=m['mode'],field_phase=e.phase,field_sha256=digest(e.fields.tobytes()))
            require(strict_bytes(view(actual))==strict_bytes(n), 'extra native/wave/random/field update or native reconstruction mismatch')
            if w is not None:
                require(wave_index<len(waves) and strict_bytes(view(dict(time=e.time,mode=m['mode'],**w)))==strict_bytes(waves[wave_index]),
                        'wave reconstruction mismatch')
                wave_index+=1
            if m['mode']==FIXED: adapter.validate_frozen(e.organism,session['frozen'])
        require(wave_index==len(waves), 'extra wave record')
        require(strict_bytes(view(replay_events))==strict_bytes(events),'event replay mismatch')
        require(state_hash(e)==state_hash(final)==receipt['final_state'], 'final state reconstruction mismatch')
        require(finish['field_updates']-session['field_updates']==len(native), 'extra field update count')
        require(history.payload['history']==payload['history'], 'privileged raw/EI substitution in sensor interface')
    return {'class':'AV','native_records':len(native),'wave_records':len(waves),'events':len(events),
            'replayed':replay,'maximum_accounting_residual':maximum,'mode':m['mode'],'status':receipt['status']}
