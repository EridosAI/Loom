"""Static held-proposal representation and existing-record compatibility only."""
import hashlib,json,pathlib,sys
R=pathlib.Path(__file__).resolve().parents[1]
D=R/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
O=R/'exports/2026-09-26-A5-clock-correction'
sys.path.insert(0,str(D))
from loom_commissioning import clock,controllers,authority,contract
from loom_p.records import code_identity
HELD=R/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
m=json.loads((HELD/'A5_MANIFEST.json').read_bytes())
held_hash=hashlib.sha256((HELD/'AUTHORITY_OBJECT.canonical.json').read_bytes()).hexdigest()
assert held_hash=='88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
assert m['execution_authority'] is None
ends=clock.stage_ends(m);assert ends==(9000,12000,27000,30000,45000,48000,63000)
assert m['apparatus']!=contract.apparatus_identity()
# No make_manifest, authority grant, initialization, engine or command call.
runtime=authority.runtime_identity();assert runtime==m['execution']['runtime']
assert code_identity()['sha256']==m['p_code']
times=[0.]
for _ in range(120000):times.append(times[-1]+.01)
rows=[]
for i in (26949,26950,26951,26999,27000,27001,30000,45000,48000,63000):
    clock.validate_physical_time(m,i,times[i])
    stage=controllers.waypoint_stage(clock.decision_clock(m,i),len(ends))
    rows.append({'native_index':i,'physical_time':times[i],'expected_time':clock.expected_time(m,i),
                 'allowance':clock.clock_allowance(m,i),'stage':stage,'case_complete':i==63000,
                 'new_command_permitted_by_cadence':i<63000 and i%10==0})
cases=[]
records=json.loads((D/'tests_apparatus/fixtures/clock_retrospective.json').read_bytes())
for case in records['cases']:
    old=case['scheduling_fields'];mismatches=[]
    for index,t,expected in case['decisions']:
        stage=controllers.waypoint_stage(clock.decision_clock(old,index),len(old['execution']['procedure']['stages']))
        clock.validate_physical_time(old,index,t)
        if stage!=expected:mismatches.append(index)
    assert not mismatches
    cases.append({'case':case['case'],'decisions':len(case['decisions']),'stage_disagreements':mismatches})
result={'status':'CORRECTION EVIDENCE ONLY; NOT A5 LAUNCH FITNESS','held_hash_unchanged':held_hash,
 'held_manifest_written':False,'held_authority_remains_null':True,'old_apparatus_identity_differs':True,
 'stage_end_indices':ends,'case_end_index':clock.case_end(m),'boundary_rows':rows,
 'retrospective':cases,'total_saved_decisions':sum(c['decisions'] for c in cases),'replayed':False,
 'A5_runs':0,'A5_world_controller_calls':0,'new_authority_objects':0,
 'P':code_identity(),'apparatus':contract.apparatus_identity(),'runtime_unchanged':runtime,
 'configuration_file_sha256':hashlib.sha256((D/'configuration.json').read_bytes()).hexdigest(),
 'controller_gains':controllers.WAYPOINT_SETTINGS}
(O/'CORRECTION_DETAILS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'old_A_preserved':'RED at step 26950','new_A':'GREEN','old_B_preserved':'RED at step 27000','new_B':'GREEN',
                  'retrospective':cases,'static_A5_only':True},indent=2))
