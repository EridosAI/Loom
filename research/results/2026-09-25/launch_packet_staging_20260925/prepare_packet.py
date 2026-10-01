"""Construct one zero-time proposed A1 state/manifest. NEVER launch a Run."""
import copy,hashlib,json,math,os,pathlib,shutil,subprocess,sys,time
from contextlib import ExitStack
from unittest.mock import patch
import numpy as np
S=pathlib.Path(__file__).resolve().parent
PROJECT=S.parent
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'
OUT=PROJECT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
CACHE=D/'artifacts/prehistory-attempt-001'
APP='5f07748102cb5eaa302569c87efbae095050e9fe';P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
sys.path.insert(0,str(D))
from loom_p.engine import Engine
from loom_p.chemistry import FieldSolver
from loom_p.physics import Body
from loom_p.neural import Organism
from loom_p import prehistory,physics
from loom_p.geometry import transduce
from loom_p.records import state_hash,save_snapshot,load_snapshot,view,code_identity
from loom_commissioning import adapter,runner,diagnostics,authority
from loom_commissioning.initialization import from_verified_cache
from loom_commissioning.contract import make_manifest,authorize_execution,apparatus_identity,EXTERNAL
import packet_checks

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(view(value),ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf-8')
def copy_file(p,name):
    q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-C',str(W),*args],env=env)
def forbidden(*a,**k):raise AssertionError('PREPARATION CANNOT ADVANCE OR CONSTRUCT A RUN')

def main():
    started=time.perf_counter()
    assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
    assert code_identity()['sha256']=='63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9'
    assert apparatus_identity()['sha256']=='d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a'
    for p in (D/'loom_p').glob('*.py'):assert p.read_bytes()==git('show',P+':developmental_ecology/loom_p/'+p.name)
    assert (D/'configuration.json').read_bytes()==git('cat-file','--filters',P+':developmental_ecology/configuration.json')
    original_files=[p for directory in ('loom_p','loom_commissioning') for p in (D/directory).iterdir() if p.suffix in ('.py','.html')]
    original_files += [D/'configuration.json',D/'requirements-lock.txt']+[p for p in CACHE.rglob('*') if p.is_file()]
    before={str(p):sha(p) for p in original_files}
    OUT.mkdir(parents=True,exist_ok=False)
    probe=OUT/'access-check.tmp';probe.write_bytes(b'launch-packet read/write check');assert probe.read_bytes()==b'launch-packet read/write check';probe.unlink()
    wb=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
    design=PROJECT/'exports/2026-09-23-p-commissioning-design-2fb3ff84'
    sources={
      'FIRST_LAUNCH_REQUEST.txt':pathlib.Path(r'C:\Users\Jason\.codex\attachments\1ba1efef-8a8f-4a55-8b6e-c664af4fde2a\Pasted text.txt'),
      'LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md':PROJECT/'exports/2026-09-25-p-final-mechanical-closure-5f077481/LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md',
      'P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md':design/'P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md',
      'P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md':design/'P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md',
      'COMPUTE_ESTIMATE.json':design/'PACKAGE/COMPUTE_ESTIMATE.json',
      'P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md':design/'P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md',
      'DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md':PROJECT/'exports/2026-09-24-p-apparatus-intake-73c9ad61/NEW/40_DECISIONS/DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md',
      'independent-r1p-evidence.json':PROJECT/'exports/2026-09-23-p-final-r1p-review-6bc9683b/physics/independent-r1p-evidence.json',
      '00_LOOM_CURRENT_STATE.md':PROJECT/'sources/00_LOOM_CURRENT_STATE(2).md',
      'WORKBENCH_AGENTS.md':wb/'AGENTS.md','WORKBENCH_MAP.md':wb/'00_RESEARCH_MAP.md','WORKBENCH_STATUS.md':wb/'01_WORKSPACE_STATUS.md'}
    source_records={}
    for name,p in sources.items():
        copy_file(p,'references/'+name)
        source_records[name]={'original_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
    write('SOURCE_IDENTITIES.json',source_records)
    for name in ('PROCEDURES.md','packet_checks.py','prepare_packet.py'):copy_file(S/name,name)
    for p in original_files:
        if p.is_relative_to(CACHE):copy_file(p,'verified-cache/'+p.relative_to(CACHE).as_posix())
        else:copy_file(p,'instrument/developmental_ecology/'+p.relative_to(D).as_posix())
    with ExitStack() as guards:
        for obj,name in ((Engine,'step'),(FieldSolver,'step'),(prehistory,'prepare'),(physics,'advance'),
                         (physics,'account'),(adapter,'step'),(runner.Run,'__init__'),(Organism,'native'),(Organism,'handoff')):
            guards.enter_context(patch.object(obj,name,forbidden))
        e,initialization=from_verified_cache(CACHE,0)
        constructor_origin=copy.deepcopy(e.birth_provenance)
        inactive_before=state_hash(e.organism);rng_before=copy.deepcopy(e.organism.rng.counters)
        e.body=Body(np.array([6.,3.]),math.pi,energy=e.c.birth_energy,integrity=1.)
        e.raw=transduce(e.c,e.body,e.fields,0.,e.phase)
        e.birth_provenance={'kind':'manufactured_external_geometry_start','lawful_newborn_sample':False,
            'position':[6.,3.],'angle':math.pi,'phase':e.phase,'constructor_origin_retained':constructor_origin,
            'description':'Body selected by geometry at time zero. Original inactive neural object/RNG retained; not a newborn life.'}
        e.validate_state();assert e.time==0 and e.native_index==0 and state_hash(e.organism)==inactive_before
        assert e.organism.rng.counters==rng_before
        snap=save_snapshot(OUT/'INITIAL_A1.snapshot.json.gz',e)
        assert state_hash(load_snapshot(OUT/'INITIAL_A1.snapshot.json.gz'))==state_hash(e)
        summary={'label':'prospective manufactured external initial state; unexecuted','body':view(vars(e.body)),
            'stocks':e.stocks.tolist(),'time':e.time,'native_index':e.native_index,'mover_phase':e.phase,
            'field_sha256':initialization['field_sha256'],'initialization':initialization,
            'state_sha256':state_hash(e),'snapshot_sha256':snap['sha256'],'inactive_organism_sha256':inactive_before,
            'initialization_rng_counters':rng_before,'original_constructor_provenance':constructor_origin,
            'neural_evolution':0,'field_steps':0,'new_prehistory_steps':0,'physical_steps':0}
        write('INITIAL_STATE_SUMMARY.json',summary)
        plan=[{'point':[3.,3.],'until':120.,'press_force':.1}]
        destination=D/'artifacts/first-commissioning-A1-20260925-5f077481/trajectory-001'
        assert not destination.exists()
        protocol={'packet_label':'FIRST_COMMISSIONING_LAUNCH_PACKET / proposed, awaiting Jason',
            'reviewed_checkpoints':{'p_git_sha':P,'apparatus_git_sha':APP},
            'case_count':1,'prechecks':['V1','V2','V3','A0'],
            'bound_files':{name:sha(OUT/name) for name in ('PROCEDURES.md','packet_checks.py','prepare_packet.py','SOURCE_IDENTITIES.json','INITIAL_STATE_SUMMARY.json')},
            'initial_snapshot_file':{'name':'INITIAL_A1.snapshot.json.gz','sha256':snap['sha256']},
            'read_only_callable_identities':{name:authority.callable_identity(getattr(packet_checks,name)) for name in ('v1','v2','v3','a0','a1_interpret')},
            'recording_contract':{'observer_symbol':'loom_commissioning.diagnostics.passive',
                'observer_file_sha256':sha(D/'loom_commissioning/diagnostics.py'),
                'recorder_symbol':'loom_p.records.Recorder','recorder_file_sha256':sha(D/'loom_p/records.py'),
                'streams':['native','wave','events','controller','diagnostics','sensor','scientific_observations'],
                'snapshots':'initial/final and every native 1000; unchanged runner',
                'post_read':'verify_segment(replay=False); packet_checks.v2/a1_interpret; no trajectory replay'},
            'record_destination':str(destination),'analysis_destination':str(destination.parent/'read-only-review'),
            'launch_operations':['load exact snapshot','validate exact object plus later genuine grant','construct one Run with diagnostics.passive','Run.hold with no manual commands until closed','preserve all stops; no retry or automatic resume'],
            'stop_names':['terminal','apparatus_failure','administrative_pause','administrative_cutoff'],
            'failure_rule':'Stop, preserve; no substituted route, controller, settings, state, phase or deadline.',
            'extra_changes':'No deprivation, no sensory hiding, no physical/P modification. External actuation/inactive neural object is the explicit reviewed A1 arm, not intact P.',
            'component_allowance':{'machine_seconds':3600,'recorded_bytes':1000000000,'world_steps':0},
            'disk_bytes_for_primary_and_copy':3000000000,
            'excluded_cases':['A2','A3','A4','A5','B1','B2','B3','B4','C1','C2','newborn lives','fixed-structure diagnostics','perceptual trials','scientific tests'],
            'legacy_roster_note':'The mandatory apparatus roster field is preserved with execution_authorized=false. It grants no birth, C1 or C2 execution.'}
        m=make_manifest(e,'A1',EXTERNAL,'waypoint',120.,purpose='commissioning',initialization=initialization,
                        plan=plan,protocol=protocol,storage_limit=1500000000,wall_limit=1200)
        v1=packet_checks.v1(e,m);v3=packet_checks.v3(e);geom=packet_checks.a0(e.c,e.phase)
        try:authorize_execution(m)
        except ValueError as ex:
            assert str(ex)=='commissioning execution is not authorized';denial=str(ex)
        else:raise AssertionError('Null authority unexpectedly accepted')
        old=json.loads(sources['independent-r1p-evidence.json'].read_bytes())
        archived={case['case']:packet_checks.v2(case['events'],e.c) for case in old['cases']}
        write('V2_ARCHIVED_ACCOUNTING_CHECK.json',{'scope':'Read-only checks of historical R1-P events; not a new regression run or A1 witness. Contact/transfer outcomes were not used to select this A1.', 'cases':archived})
        write('A0_GEOMETRY.json',geom)
        write('PREPARATION_CHECKS.json',{'V1':v1,'V3_initial_read':v3,'null_grant_rejected':denial,
            'snapshot_roundtrip_identical':True,'initial_state_unchanged_after_checks':state_hash(e)==summary['state_sha256'],
            'commissioning_trajectories_executed':0,'controller_commands_computed':0,'new_prehistory_preparations':0,
            'engine_native_field_wave_account_replay_calls':0,'future_live_V2_V3':'pending A1 evidence, not asserted complete',
            'preparation_wall_seconds':time.perf_counter()-started})
        write('A1_MANIFEST.json',m)
        obj=authority.execution_object(m);canonical=authority.canonical(obj);h=authority.execution_sha256(m)
        write('AUTHORITY_OBJECT.json',obj)
        (OUT/'AUTHORITY_OBJECT.canonical.json').write_bytes(canonical)
        (OUT/'AUTHORITY_SHA256.txt').write_text(h+'  AUTHORITY_OBJECT.canonical.json\n',encoding='utf-8')
        assert authority.strict_loads(canonical)==authority.strict_loads((OUT/'AUTHORITY_OBJECT.json').read_bytes())
        assert hashlib.sha256(canonical).hexdigest()==h and m['execution_authority'] is None
        ids={'P_commit':P,'apparatus_commit':APP,'branch':git('branch','--show-current').decode().strip(),
            'P':code_identity(),'apparatus':apparatus_identity(),'configuration_semantic':e.c.identity(),
            'configuration_file_sha256':sha(D/'configuration.json'),'runtime':authority.runtime_identity(),
            'controller':authority.controller_identity('waypoint'),'original_file_inventory':before,
            'scope':'Original reviewed runtime/config/cache bytes only read; copied bytes exact.'}
        write('CODE_AND_RUNTIME_IDENTITIES.json',ids)
        budget=json.loads(sources['COMPUTE_ESTIMATE.json'].read_bytes())['rates']
        write('BUDGET.json',{'maximum_simulated_seconds':120,'maximum_full_native_steps':12000,'maximum_command_decisions':1200,
            'projected_wall_seconds':120*budget['wall_seconds_per_simulated_second'],
            'projected_stored_bytes':120*budget['stored_bytes_per_simulated_second'],
            'projected_uncompressed_bytes':120*budget['uncompressed_bytes_per_simulated_second'],
            'bound_run_wall_seconds':1200,'bound_uncompressed_stream_bytes':1500000000,
            'disk_allowance_primary_and_copy_bytes':3000000000,'component_machine_seconds_ceiling':3600,'component_bytes_ceiling':1000000000,
            'assumption':'Historical full-P 30-second engineering rate as proxy; external commissioning overhead unmeasured; no benchmark run.'})
    assert all(sha(pathlib.Path(p))==h0 for p,h0 in before.items())
    assert not git('status','--porcelain').strip() and git('rev-parse','HEAD').decode().strip()==APP
    write('PRESERVATION.json',{'original_runtime_config_cache_files':len(before),'all_hashes_unchanged':True,
            'git_status_clean':True,'git_writes':0,'code_changes':0,'current_source_files_unchanged':all(sha(p)==source_records[n]['sha256'] for n,p in sources.items()),
            'commissioning_execution_occurred':False,'authority_status':'PROPOSED / NOT AUTHORIZED'})
    print(json.dumps({'output':str(OUT),'canonical_sha256':h,'initial_state_sha256':m['initial_state'],
                      'phase':m['phase'],'time':e.time,'native_index':e.native_index,'status':'PROPOSED / NOT AUTHORIZED'},indent=2))

if __name__=='__main__':main()
