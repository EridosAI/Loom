"""Fixed B1 v0.2 external reference. No Engine, file I/O, RNG or world access."""
import copy
import math
from .contract import require
from .controllers import LABELS, validate_sensor_payload, validate_history

KIND='automated_raw_reference'
ARMS=('FULL','CHEMISTRY-HIDDEN','SENSORY-FREE')
DESIGN='8f0437aaa53bb192dad36f5337340a2cc8a4b7060660445d573f9c5ca473cbe6'
SETTINGS={'window_rows':10,'receptor_scale':.05,'contrast_epsilon':1e-12,
          'drive':.30,'drive_imbalance':4.,'turn_gain':2.,'angular_damping':.20,
          'turn_bound':.40,'contact_sectors':[7,0,1],'hold_on':.05,
          'release_below':.02,'release_windows':3,'hold_drive':.05,'null_pair':[.30,.30]}
KEPT=tuple(i for i in range(29) if i not in (10,11,12,13))
HIDDEN_LABELS=[LABELS[i] for i in KEPT]


def arm_from_manifest(m):
    p=m['execution']['procedure']['protocol']
    require(type(p) is dict and set(p)=={'reference_arm','design_sha256'}
            and p['reference_arm'] in ARMS and p['design_sha256']==DESIGN,
            'fixed reference procedure mismatch')
    return p['reference_arm']


def initial_state():
    return {'mode':'SEEK','release_count':0}


def validate_state(state):
    require(type(state) is dict and set(state)=={'mode','release_count'}
            and state['mode'] in ('SEEK','HOLD') and type(state['release_count']) is int
            and 0<=state['release_count']<SETTINGS['release_windows']
            and (state['mode']=='HOLD' or state['release_count']==0), 'invalid reference memory')


def validate_input(payload,arm):
    require(arm in ARMS,'unknown reference arm')
    if arm=='SENSORY-FREE':
        require(payload is None,'sensory-free controller must receive no input')
        return
    require(type(payload) is dict and set(payload)=={'raw_labels','history','own_commands'},
            'forbidden reference input')
    labels=LABELS if arm=='FULL' else HIDDEN_LABELS
    validate_history(dict(payload,schema=1 if arm=='FULL' else 2,annotations=[],availability='paused'),
                     labels,1 if arm=='FULL' else 2)
    rows=payload['history']
    require(bool(rows) and all(row['native_index']==i for i,row in enumerate(rows)),
            'reference history must be a complete causal birth prefix')
    require((len(rows)-1)%10==0,'reference decision outside hold boundary')
    for row in rows:
        require(abs(row['time']-row['native_index']*.01)<1e-10,'reference history clock mismatch')
        require(abs(row['EI_sample_time']-(row['native_index']//20)*.2)<1e-10,
                'reference EI cadence mismatch')
    for item in payload['own_commands']:
        require(item['time']<rows[-1]['time'],'future own command')


def project(payload,arm):
    if arm=='SENSORY-FREE':
        validate_input(payload,arm)
        return None
    require(arm in ARMS,'unknown reference arm')
    validate_sensor_payload(payload)
    require(payload['annotations']==[],'annotations forbidden for automated reference')
    result=copy.deepcopy({k:payload[k] for k in ('raw_labels','history','own_commands')})
    if arm=='CHEMISTRY-HIDDEN':
        result['raw_labels']=HIDDEN_LABELS.copy()
        for row in result['history']:row['raw']=[row['raw'][i] for i in KEPT]
    validate_input(result,arm)
    return result


def command(payload,state,arm):
    """Pure decision: return a pair and fresh memory; no input is mutated."""
    validate_input(payload,arm);validate_state(state)
    if arm=='SENSORY-FREE':
        require(state==initial_state(),'sensory-free reference cannot carry feedback memory')
        return SETTINGS['null_pair'].copy(),initial_state()
    labels=payload['raw_labels'];rows=payload['history'][-SETTINGS['window_rows']:]
    b=0.
    if arm=='FULL':
        ids=[labels.index('chemistry_'+str(j)) for j in range(4)]
        require(all(0<=row['raw'][j]<1 for row in payload['history'] for j in ids),
                'chemical receptor outside invertible range')
        q=[math.fsum(SETTINGS['receptor_scale']*row['raw'][j]/(1-row['raw'][j])
                     for row in rows)/len(rows) for j in ids]
        R=(q[0]+q[1])/2;L=(q[2]+q[3])/2
        b=(L-R)/(L+R+SETTINGS['contrast_epsilon'])
    C=max(row['raw'][labels.index('contact_'+str(j))] for row in rows for j in SETTINGS['contact_sectors'])
    next_state=copy.deepcopy(state)
    if state['mode']=='SEEK' and C>=SETTINGS['hold_on']:
        next_state={'mode':'HOLD','release_count':0}
    elif state['mode']=='HOLD':
        count=state['release_count']+1 if C<SETTINGS['release_below'] else 0
        next_state=initial_state() if count==SETTINGS['release_windows'] else {'mode':'HOLD','release_count':count}
    if next_state['mode']=='HOLD':return [SETTINGS['hold_drive']]*2,next_state
    p4=rows[-1]['raw'][labels.index('proprioception_4')]
    d=SETTINGS['drive']/(1+SETTINGS['drive_imbalance']*abs(b))
    a=max(-SETTINGS['turn_bound'],min(SETTINGS['turn_bound'],SETTINGS['turn_gain']*b-SETTINGS['angular_damping']*p4))
    return [d-a,d+a],next_state
