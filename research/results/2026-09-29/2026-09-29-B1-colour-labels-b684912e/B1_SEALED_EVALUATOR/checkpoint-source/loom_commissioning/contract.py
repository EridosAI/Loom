"""Closed manifests, identity checks and interpretation firewall."""
from pathlib import Path
import hashlib
import math
import numpy as np
from loom_p.records import code_identity, strict_bytes, state_hash

BASELINE = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
P_CODE = '63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9'
CONFIG = 'a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a'
FIXED = 'FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC'
INTACT = 'intact_P'
EXTERNAL = 'external_controller'
SELECTION = {'wave': 'every_handoff', 'native': 'native_index % 100 == 0', 'native_stride': 100}
ROSTER = {'birth_ids': [1, 2, 3, 4], 'birth_ceiling_seconds': 600,
          'zero_witness_interpretation': 'unresolved opportunity at that coverage',
          'execution_authorized': False}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def apparatus_identity():
    files = {p.name: digest(p.read_bytes()) for p in sorted(Path(__file__).parent.iterdir())
             if p.suffix in ('.py', '.html')}
    return {'sha256': digest(strict_bytes(files)), 'files': files}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def make_manifest(engine, case_id, mode, controller, seconds, *, purpose='manufactured_fixture',
                  initialization=None, plan=None, protocol=None, storage_limit=1_000_000_000, wall_limit=3600,display='none'):
    """Explicit constructor; it does not grant permission to execute a manifest."""
    from .authority import make_execution
    return dict(schema=2, baseline=BASELINE, p_code=P_CODE, configuration=CONFIG,
                apparatus=apparatus_identity(), case_id=case_id, purpose=purpose,
                mode=mode, controller=controller, initial_state=state_hash(engine),
                initial_time=engine.time, initial_index=engine.native_index,
                initial_fields=digest(engine.fields.tobytes()), phase=engine.phase,
                initialization=initialization or {'kind': 'manufactured', 'lawful_birth': False},
                duration_seconds=seconds, hard_stop_time=engine.time+seconds,
                command_hold_seconds=.1, selection=SELECTION.copy(), roster=ROSTER.copy(),
                execution=make_execution(mode,controller,plan=plan,protocol=protocol,
                                         storage_limit=storage_limit,wall_limit=wall_limit,display=display),
                execution_authority=None)

def validate_manifest(m, engine, *, initial=True):
    required = set(make_manifest(engine, 'unused', INTACT, 'none', 0))
    require(set(m) == required, 'manifest schema mismatch')
    require(m['schema'] == 2 and m['baseline'] == BASELINE and m['p_code'] == P_CODE
            and code_identity()['sha256'] == P_CODE, 'manifest/code identity mismatch')
    require(m['configuration'] == CONFIG == engine.c.identity(), 'configuration identity mismatch')
    require(m['apparatus'] == apparatus_identity(), 'apparatus identity mismatch')
    require(m['mode'] in (INTACT, FIXED, EXTERNAL), 'trajectory label invalid')
    require(m['controller'] in ('none', 'waypoint', 'sensor_human', 'manual_privileged'), 'controller kind invalid')
    require((m['controller'] == 'none') == (m['mode'] != EXTERNAL), 'external controller incorrectly labelled intact P')
    duration = m['duration_seconds']
    require(type(duration) in (int, float) and math.isfinite(duration) and 0 < duration <= 1200,
            'duration cap invalid')
    require(abs(duration/.01-round(duration/.01)) < 1e-8
            and abs(m['hard_stop_time']-m['initial_time']-duration) < 1e-9, 'duration cap identity mismatch')
    require(m['command_hold_seconds'] == .1 and m['selection'] == SELECTION and m['roster'] == ROSTER,
            'fixed sampling/hold/roster contract mismatch')
    require(engine.phase == m['phase'], 'wrong field/mover phase')
    if initial:
        require(engine.native_index == m['initial_index'] and engine.time == m['initial_time'], 'initial clock mismatch')
        require(digest(engine.fields.tobytes()) == m['initial_fields'], 'wrong initial field')
        require(state_hash(engine) == m['initial_state'], 'initial state identity mismatch')
    if m['purpose'] == 'manufactured_fixture':
        require(m['case_id'].startswith('fixture-') and duration <= .6
                and m['initialization'] == {'kind': 'manufactured', 'lawful_birth': False},
                'manufactured fixture cap/provenance invalid')
    else:
        require(m['purpose'] == 'commissioning', 'unknown run purpose')
        init = m['initialization']
        require(init.get('kind') == 'verified_phase_history'
                and init.get('phase') == engine.phase
                and init.get('field_sha256') == m['initial_fields']
                and bool(init.get('cache_receipt_sha256')), 'lawful phase-specific prehistory required')
        from .initialization import verify_history
        verify_history(init,engine.c,m['initial_fields'],m['phase'])
        if m['case_id'] in ('C1', 'C2'):
            require(init.get('birth_id') in (1,2,3,4) and duration == 600, 'birth roster/ceiling mismatch')
    from .authority import validate_execution
    validate_execution(m)
    return True

def authorize_execution(m):
    # Future executions require an explicit separately supplied local grant.
    # No such grant is delivered or synthesized by the apparatus build. This is
    # an auditable workflow boundary, not security against the machine owner.
    if m['purpose']=='manufactured_fixture':
        require(m['execution_authority'] is None,'fixture is not a commissioning grant')
        return
    authority=m['execution_authority']
    require(isinstance(authority,dict) and set(authority)=={'request_path','request_sha256','approved_case','approved_initial_state','approved_duration','approved_execution_sha256'},
            'commissioning execution is not authorized')
    require(authority['approved_case']==m['case_id'] and authority['approved_initial_state']==m['initial_state']
            and authority['approved_duration']==m['duration_seconds'], 'execution grant scope mismatch')
    from .authority import verify_approval_binding, validate_execution
    verify_approval_binding(m,authority)
    validate_execution(m,complete=True)

CLASSES = {'V1':'AV','V2':'AV','V3':'AV','A0':'AV','A1':'AV','A2':'AV','A3':'AV','A4':'AV','A5':'AV',
           'B1':'AV','B2':'AV','B3':'AV','B4':'CO','C1':'CO','C2':'CO',
           **{f'D{i}':'CO' for i in range(1,8)}, 'S1':'SO','S2':'SO'}

def classify(row_id, observation):
    require(row_id in CLASSES, 'unknown evidence class')
    return {'row':row_id, 'class':CLASSES[row_id], 'observation':observation,
            'interpretation_status':'preserved_not_a_configuration_ground' if CLASSES[row_id]=='SO' else 'commissioning_review_only'}

def configuration_grounds(evidence):
    require(all(x['class'] == CLASSES.get(x['row']) for x in evidence), 'evidence class mismatch')
    require(all(x['class'] in ('AV','CO') for x in evidence), 'SO cannot ground a configuration adjustment before freeze')
    return {'automatic_adjustment':False, 'requires':'Jason defect-specific ruling', 'evidence':evidence}
