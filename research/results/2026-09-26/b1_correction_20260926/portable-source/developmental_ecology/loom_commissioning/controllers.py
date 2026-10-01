"""Capability boundaries: controllers receive copied data, never an Engine."""
import copy
import math
import numpy as np
from loom_p.geometry import fixtures, mover
from loom_p.records import view, state_hash
from .contract import require

# Same reviewed literals, now explicit approval-bearing controller configuration.
WAYPOINT_SETTINGS={'heading_gain':.8,'angular_damping':.2,'distance_gain':.5,
    'speed_damping':.4,'force_gain':.4,'turn_bound':.5,'drive_bound':.5,
    'maximum_target_force':.25,'heading_distance_epsilon':1e-12}

def time_due(now, deadline):
    """Exact native-index ownership; physical timestamps never select a stage."""
    require(type(now) is int and type(deadline) is int, 'deadline comparison requires native indices')
    return now >= deadline

def validate_plan(plan):
    require(isinstance(plan,list) and bool(plan), 'invalid prescribed route')
    previous=-float('inf')
    for p in plan:
        require(set(p)=={'point','until','press_force'} and len(p['point'])==2
                and all(math.isfinite(float(v)) for v in (*p['point'],p['until'],p['press_force']))
                and 0<=p['press_force']<=WAYPOINT_SETTINGS['maximum_target_force']
                and p['until']>previous, 'invalid prescribed route')
        previous=p['until']

PRIVILEGED_KEYS={'position','angle','velocity','omega','reserves','commands','geometry',
                 'mover_phase','mover_velocity','stocks','contacts','time'}
SENSOR_KEYS={'schema','raw_labels','history','own_commands','annotations','availability'}
ROW_KEYS={'native_index','time','raw','actual_EI','EI_sample_time'}
LABELS=[f'{name}_{i}' for name,width in [('light',10),('chemistry',4),('contact',8),('proprioception',7)] for i in range(width)]

def validate_privileged(data):
    require(set(data)==PRIVILEGED_KEYS, 'forbidden controller input')
    base={'id','kind','velocity'}
    for f in data['geometry']:
        specific={'wall':{'axis','sign','boundary'},'disk':{'centre','radius'},'rect':{'rect'}}
        require(f.get('kind') in specific and set(f)==base|specific[f['kind']], 'forbidden geometry input')
    for x in data['contacts']:
        require(set(x)=={'normal','force','impulse'}, 'forbidden contact input')
    return True

def privileged_input(e):
    scene=[]
    for f in fixtures(e.c,e.time,e.phase):
        scene.append({k:copy.deepcopy(v) for k,v in f.items() if k not in ('material','source')})
    contacts=[{k:copy.deepcopy(x.get(k,0.)) for k in ('normal','force','impulse')}
              for event in e.last_events for x in event.get('contacts',[])]
    result=view(dict(position=e.body.position.copy(),angle=e.body.angle,velocity=e.body.velocity.copy(),
        omega=e.body.omega,reserves=e.body.reserves,commands=e.body.command.copy(),geometry=scene,
        mover_phase=e.phase,mover_velocity=mover(e.c,e.time,e.phase)[1],stocks=e.stocks.copy(),
        contacts=contacts,time=e.time))
    validate_privileged(result)
    return result

def command_pair(command):
    values=np.asarray(command,dtype=float)
    require(values.shape==(2,) and np.isfinite(values).all() and np.all(abs(values)<=1), 'invalid actuator command')
    return values.copy()

def waypoint_stage(decision, count):
    """Pure stage ownership, also usable on saved metadata without actuation."""
    require(type(decision) is tuple and len(decision)==2, 'native decision clock required')
    native_index,deadlines=decision
    require(type(native_index) is int and native_index>=0 and type(deadlines) is tuple
            and len(deadlines)==count and count>0
            and all(type(i) is int for i in deadlines)
            and all(a<b for a,b in zip(deadlines,deadlines[1:])), 'invalid native route boundaries')
    cursor=0
    while cursor<count-1 and time_due(native_index,deadlines[cursor]):
        cursor+=1
    return cursor


def waypoint_command(data, plan, decision):
    """Deterministic geometry-specified route, not an optimized policy.

    A plan consists of fixed point/wait/press entries, provided before execution.
    Contact servo uses measured normal force; it cannot set the body's force.
    """
    validate_privileged(data)
    validate_plan(plan)
    cursor=waypoint_stage(decision,len(plan))
    native_index,deadlines=decision
    k=WAYPOINT_SETTINGS
    p=plan[cursor]; delta=np.array(p['point'])-data['position']
    distance=float(np.linalg.norm(delta))
    heading=math.atan2(delta[1],delta[0]) if distance>k['heading_distance_epsilon'] else data['angle']
    error=math.atan2(math.sin(heading-data['angle']),math.cos(heading-data['angle']))
    turn=float(np.clip(k['heading_gain']*error-k['angular_damping']*data['omega'],-k['turn_bound'],k['turn_bound']))
    forward=np.array([math.cos(data['angle']),math.sin(data['angle'])])
    speed=float(forward@np.array(data['velocity']))
    drive=float(np.clip(k['distance_gain']*distance-k['speed_damping']*speed,0,k['drive_bound']))*max(0,math.cos(error))
    if data['contacts'] and p['press_force']>0:
        measured=sum(x['force'] for x in data['contacts'])
        drive=float(np.clip(float(np.mean(data['commands']))+k['force_gain']*(p['press_force']-measured),0,k['drive_bound']))
    if time_due(native_index,deadlines[cursor]): drive=0.; turn=0.
    return command_pair([drive-turn,drive+turn]),cursor

def validate_sensor_payload(payload):
    return validate_history(payload,LABELS,1)

def validate_history(payload,labels,schema):
    """Closed coordinate schema; physical history always uses the 29-label wrapper."""
    require(set(payload)==SENSOR_KEYS and payload['schema']==schema and payload['raw_labels']==labels,
            'privileged data leakage into sensor-only interface')
    require(payload['availability'] in ('paused','offline_record','unavailable'), 'privileged status leak')
    previous=-1; previous_time=-float('inf'); held=None; sampled=None
    for row in payload['history']:
        require(set(row)==ROW_KEYS, 'privileged data leakage into sensor-only interface')
        require(type(row['native_index'])==int and row['native_index']>previous and row['time']>previous_time,
                'sensor history time/order mismatch')
        raw=np.asarray(row['raw'],dtype=float); ei=np.asarray(row['actual_EI'],dtype=float)
        require(raw.shape==(len(labels),) and ei.shape==(2,) and np.isfinite(raw).all() and np.isfinite(ei).all(), 'raw/actual EI schema mismatch')
        require(row['EI_sample_time']<=row['time']+1e-12, 'future EI leak')
        if sampled is not None and row['EI_sample_time']==sampled:
            require(row['actual_EI']==held, 'EI cadence leak')
        if sampled is not None and row['EI_sample_time']!=sampled:
            require(row['native_index']%20==0 and abs(row['EI_sample_time']-row['time'])<1e-12, 'EI cadence leak')
        previous=row['native_index']; previous_time=row['time']; sampled=row['EI_sample_time']; held=row['actual_EI']
    for item in payload['own_commands']:
        require(set(item)=={'time','command'}, 'privileged command record leak'); command_pair(item['command'])
    for item in payload['annotations']:
        require(set(item)=={'time','text'} and isinstance(item['text'],str), 'privileged annotation leak')
    return True

class SensorHistory:
    def __init__(self, engine):
        self.payload={'schema':1,'raw_labels':LABELS.copy(),'history':[],'own_commands':[],
                      'annotations':[],'availability':'paused'}
        self.held=engine.body.reserves.tolist(); self.sample_time=engine.time
        self.observe(engine, initial=True)

    def observe(self,e,initial=False):
        if not initial and e.native_index%20==0 and e.status!='terminal':
            self.held=e.body.reserves.tolist(); self.sample_time=e.time
        self.payload['history'].append(dict(native_index=e.native_index,time=e.time,
            raw=np.concatenate(e.raw).tolist(),actual_EI=self.held.copy(),EI_sample_time=self.sample_time))

    def display(self):
        result=copy.deepcopy(self.payload)
        validate_sensor_payload(result)
        return result

def observe_without_interference(engine, observer):
    before=state_hash(engine)
    result=observer(engine)
    require(state_hash(engine)==before, 'observer RNG/state interference')
    return result
