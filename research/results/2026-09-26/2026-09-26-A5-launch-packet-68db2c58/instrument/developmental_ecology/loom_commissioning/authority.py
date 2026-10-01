"""Canonical, inspectable execution identities. No authority is created here."""
import copy
from functools import lru_cache
import importlib.metadata
import json
import marshal
import math
from pathlib import Path
import platform
import sys
import types
from .contract import require, digest, INTACT, FIXED

def canonical(value):
    """UTF-8 JSON; sorted string keys, compact separators, finite numbers only."""
    def unique_json(x):
        if type(x) is dict:
            require(all(type(k) is str for k in x), 'canonical object keys must be strings')
            for v in x.values(): unique_json(v)
        elif type(x) is list:
            for v in x: unique_json(v)
        else:
            require(x is None or type(x) in (str,int,float,bool), 'non-JSON canonical value')
    unique_json(value)
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')

def strict_loads(raw):
    """Reject even identical duplicate keys at every nesting level."""
    def object_pairs(pairs):
        result={}
        for key,value in pairs:
            require(key not in result, 'duplicate JSON field: '+key)
            result[key]=value
        return result
    def invalid_constant(value): raise ValueError('nonfinite JSON number: '+value)
    result=json.loads(raw,object_pairs_hook=object_pairs,parse_constant=invalid_constant)
    canonical(result)
    return result

def validate_dispatch(m,namespace):
    """Check the very aliases the runner invokes, not another namespace."""
    from . import controllers as c
    names=('waypoint_command','privileged_input','command_pair','time_due','observe_without_interference')
    bound={name:namespace[name] for name in (*names,'SensorHistory')}
    for name in names:
        actual=bound[name]
        require(type(actual) is types.FunctionType and actual is getattr(c,name)
                and actual.__globals__ is vars(c) and actual.__closure__ is None
                and actual.__defaults__ is None and actual.__kwdefaults__ is None,
                'executed controller dispatch mismatch: '+name)
    require(bound['SensorHistory'] is c.SensorHistory, 'executed sensor history dispatch mismatch')
    require(controller_identity(m['controller'])==m['execution']['controller'], 'controller execution identity mismatch')
    return types.MappingProxyType(bound)

def execution_object(manifest):
    # Only the self-referential grant is excluded. Future manifest fields are
    # therefore bound automatically rather than accidentally omitted.
    return copy.deepcopy({k:v for k,v in manifest.items() if k!='execution_authority'})

def execution_sha256(manifest):
    return digest(canonical(execution_object(manifest)))

def file_identity(name):
    return digest((Path(__file__).parent/name).read_bytes())

def callable_identity(fn):
    # Bind live Python implementations as well as source bytes. Normalize only
    # the location, so a byte-identical portable copy has the same code identity.
    def portable(code):
        constants=tuple(portable(c) if isinstance(c,types.CodeType) else c for c in code.co_consts)
        return code.replace(co_filename=Path(code.co_filename).name,co_consts=constants)
    return digest(marshal.dumps(portable(fn.__code__)))

@lru_cache(maxsize=1)
def _runtime_identity():
    packages={}
    for name in ('numpy','scipy'):
        dist=importlib.metadata.distribution(name)
        files={str(p).replace('\\','/'):digest(Path(dist.locate_file(p)).read_bytes())
               for p in sorted(dist.files,key=str) if str(p).endswith(('.py','.pyd','.dll','.so','/METADATA','/RECORD'))}
        packages[name]={'version':dist.version,'content_sha256':digest(canonical(files)),
                        'file_count':len(files),'coverage':'installed .py/.pyd/.dll/.so plus METADATA/RECORD; excludes bytecode'}
    dlls={p.name:digest(p.read_bytes()) for p in sorted(Path(sys.base_prefix).glob('python*.dll'))}
    return {'python':sys.version,'implementation':platform.python_implementation(),
            'executable_sha256':digest(Path(sys.executable).read_bytes()),'python_dlls':dlls,
            'platform':platform.platform(),'packages':packages}

def runtime_identity():
    # A fresh process inventories its installed runtime once. This is an
    # approval/workflow identity, not defense against hot patching native DLLs.
    return copy.deepcopy(_runtime_identity())

def controller_identity(kind):
    from . import controllers as c
    from . import clock
    names=('waypoint_command','waypoint_stage','validate_plan','time_due','command_pair','privileged_input','validate_privileged','observe_without_interference') if kind=='waypoint' else (
        ('privileged_input','validate_privileged','command_pair','observe_without_interference') if kind=='manual_privileged' else ('validate_sensor_payload','command_pair') if kind=='sensor_human' else ())
    implementation={'controllers.py':file_identity('controllers.py'),
                    'live_functions':{n:callable_identity(getattr(c,n)) for n in names},
                    'clock.py':file_identity('clock.py'),
                    'live_clock_functions':{n:callable_identity(getattr(clock,n)) for n in
                        ('grid_steps','case_end','stage_ends','decision_clock','hold_steps',
                         'expected_time','clock_allowance','validate_physical_time')}}
    if kind=='sensor_human':
        implementation.update({'sensor_ui.py':file_identity('sensor_ui.py'),'sensor.html':file_identity('sensor.html')})
    interface={'none':'P-native','waypoint':'privileged-closed-input','manual_privileged':'privileged-manual-fallback',
               'sensor_human':'29-raw-native-history-held-EI-own-commands'}[kind]
    settings=copy.deepcopy(c.WAYPOINT_SETTINGS) if kind=='waypoint' else {}
    return {'kind':kind,'implementation':implementation,'configuration':settings,'interface':interface}

def adapter_identity(mode):
    return {'mode':mode,'implementation_sha256':file_identity('adapter.py'),
            'intervention':'freeze-reviewed-structure-at-reviewed-restoration-points' if mode==FIXED else 'inactive-neural-external-actuation' if mode!=INTACT else 'none'}

def make_execution(mode,controller,*,plan=None,protocol=None,storage_limit=1_000_000_000,wall_limit=3600):
    kind={'waypoint':'prescribed_waypoints','manual_privileged':'privileged_manual_procedure',
          'sensor_human':'sensor_only_human_procedure','none':'native_autonomous_procedure'}[controller]
    return {'runtime':runtime_identity(),'controller':controller_identity(controller),'adapter':adapter_identity(mode),
            'procedure':{'kind':kind,'stages':copy.deepcopy(plan),'protocol':copy.deepcopy(protocol)},
            'display_intervention':{'kind':'none'},
            'resources':{'storage_limit_bytes':storage_limit,'wall_limit_seconds':wall_limit}}

def validate_protocol_fields(protocol):
    # Protocol descriptions cannot supply second values for the typed execution
    # fields. There is no alias/override channel hidden inside free-form data.
    reserved={'schema','baseline','p_code','configuration','apparatus','runtime','case_id','mode','controller',
        'controller_kind','controller_config','implementation','interface','command_interface','adapter',
        'route','plan','stages','stage','point','until','press_force','intervention','display_intervention','deprivation',
        'initial_state','initial_time','initial_index','initial_fields','initialization','phase','duration','duration_seconds',
        'deadline','hard_stop_time','command_hold_seconds','resources','storage_limit_bytes','wall_limit_seconds',
        'selection','roster','execution','execution_authority'}
    def visit(value):
        if isinstance(value,dict):
            require(not reserved.intersection(value),'protocol shadows a bound execution field')
            for item in value.values():visit(item)
        elif isinstance(value,list):
            for item in value:visit(item)
    visit(protocol)

def validate_execution(m,*,complete=False):
    x=m['execution']; expected=make_execution(m['mode'],m['controller'])
    require(set(x)==set(expected), 'execution specification schema mismatch')
    for k in ('runtime','controller','adapter'):
        require(x[k]==expected[k],f'{k} execution identity mismatch')
    # This correction binds existing full-display behavior; it does not build
    # a new deprivation adapter or silently treat its label as an implementation.
    require(x['display_intervention']=={'kind':'none'}, 'unsupported display intervention')
    r=x['resources']
    require(set(r)=={'storage_limit_bytes','wall_limit_seconds'} and type(r['storage_limit_bytes'])==int
            and r['storage_limit_bytes']>0 and type(r['wall_limit_seconds']) in (int,float)
            and math.isfinite(r['wall_limit_seconds']) and r['wall_limit_seconds']>0, 'explicit finite resource limits required')
    p=x['procedure']
    require(set(p)=={'kind','stages','protocol'} and p['kind']==expected['procedure']['kind'], 'procedure kind mismatch')
    require(p['protocol'] is None or isinstance(p['protocol'],dict), 'structured procedure required')
    validate_protocol_fields(p['protocol'])
    if m['controller']=='waypoint':
        if complete or p['stages'] is not None:
            from .controllers import validate_plan
            validate_plan(p['stages'])
    else:
        require(p['stages'] is None,'route supplied to another controller')
        if complete and m['purpose']=='commissioning':
            require(bool(p['protocol']),'explicit structured arm procedure required')
    from . import clock
    clock.stage_ends(m)  # Compile/validate declared boundaries before any output.
    clock.clock_allowance(m,clock.case_end(m))  # Reject unsupported clock origins early.
    canonical(x)  # Reject non-finite or non-JSON procedure content.

def validate_session(m,s):
    x=m['execution']
    require(s['route']==x['procedure']['stages'], 'session route differs from approved procedure')
    require(s['wall_limit']==x['resources']['wall_limit_seconds']
            and s['storage_limit']==x['resources']['storage_limit_bytes'], 'session resources differ from approved scope')
    require(s['execution_sha256']==execution_sha256(m), 'session execution identity mismatch')

def read_approval(raw):
    request=strict_loads(raw)
    require(set(request)=={'notice','approved_execution_sha256','approved_execution'}
            and type(request['notice']) is str, 'unknown/aliased approval field or missing notice')
    return request

def verify_approval_binding(m,authority):
    raw=Path(authority['request_path']).read_bytes()
    request=read_approval(raw)
    expected=execution_sha256(m)
    require(authority['approved_execution_sha256']==expected,'approved execution identity mismatch')
    require(digest(raw)==authority['request_sha256'],'execution authority identity mismatch')
    require(request.get('approved_execution_sha256')==expected
            and canonical(request.get('approved_execution'))==canonical(execution_object(m)),
            'request does not approve exact execution specification')
