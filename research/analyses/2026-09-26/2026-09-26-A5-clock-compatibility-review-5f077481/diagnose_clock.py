"""Diagnosis only: scalars, inert records and detached predicates. No world evolution."""
import ast,copy,gzip,hashlib,json,math,os,pathlib,subprocess,sys,time,traceback
from decimal import Decimal,localcontext
from fractions import Fraction
from types import SimpleNamespace
O=pathlib.Path(__file__).resolve().parent;ROOT=O.parents[1]
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405');D=W/'developmental_ecology'
PACK=ROOT/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f';APP='5f07748102cb5eaa302569c87efbae095050e9fe'
HELD='88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
COUNTS={'world_steps':0,'field_steps':0,'neural_steps':0,'RNG_draws':0,'world_constructors':0,'Run_constructors':0,'A5_controller_calls':0,'detached_legacy_controller_calls':0}
BLOCKED=[];ALLOW_LEGACY_CONTROLLER=False

def guard(frame,event,arg):
    if event!='call':return
    f=frame.f_code;p=f.co_filename.replace('\\','/');name=f.co_name
    if '/loom_p/' in p or '/loom_commissioning/' in p:
        bad=name in {'step','advance','account','prepare','native','handoff','draw','coupled','_coupled','begin_command','hold','resume','from_verified_cache','load_snapshot','load_restart','transduce','free_velocity','actuator_forces','verify_history','load','privileged_input'}
        bad|=name=='__init__' and (p.endswith(('/engine.py','/runner.py','/neural.py','/chemistry.py')) or type(frame.f_locals.get('self')).__name__=='Streams')
        if name=='waypoint_command':
            if ALLOW_LEGACY_CONTROLLER:COUNTS['detached_legacy_controller_calls']+=1
            else:bad=True
        if bad:BLOCKED.append(p+':'+name);raise AssertionError('Diagnosis forbids '+BLOCKED[-1])
sys.setprofile(guard);sys.path[:0]=[str(D),str(D/'tests_apparatus')]
from loom_commissioning import authority,contract,controllers,pending,runner,validators
from loom_p.records import code_identity

def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def write(n,v):(O/n).write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_packet_staging_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env).decode()
def outcome(fn):
    try:fn();return {'accepted':True}
    except ValueError as error:
        frames=[{'file':pathlib.Path(x.filename).name,'function':x.name,'line':x.lineno} for x in traceback.extract_tb(error.__traceback__)]
        return {'accepted':False,'exception':type(error).__name__,'message':str(error),'traceback':frames}
def decfloat(v):return str(Decimal.from_float(v))
def native_deadlines(manifest):
    with localcontext() as c:
        c.prec=70
        result=[]
        for s in manifest['execution']['procedure']['stages']:
            q=(Decimal(str(s['until']))-Decimal(str(manifest['initial_time'])))/Decimal('0.01')
            assert q==q.to_integral_value()
            result.append(manifest['initial_index']+int(q))
        return result
def main():
    global ALLOW_LEGACY_CONTROLLER
    start=time.perf_counter();assert not (O/'DIAGNOSTIC_RESULTS.json').exists()
    assert git('rev-parse','HEAD').strip()==APP and not git('status','--porcelain').strip()
    m=authority.strict_loads((PACK/'A5_MANIFEST.json').read_bytes());assert sha(PACK/'AUTHORITY_OBJECT.canonical.json')==HELD
    assert authority.execution_sha256(m)==HELD and m['execution_authority'] is None
    fm=json.loads((PACK/'FILE_MANIFEST.json').read_bytes())
    assert all(sha(PACK/n)==v['sha256'] and (PACK/n).stat().st_size==v['bytes'] for n,v in fm['files'].items())
    assert contract.apparatus_identity()==m['apparatus'] and code_identity()['sha256']==m['p_code']
    assert authority.runtime_identity()==m['execution']['runtime']
    sources=[p for name in ('loom_p','loom_commissioning','tests_apparatus') for p in (D/name).rglob('*') if p.is_file() and p.suffix in ('.py','.html','.json')]
    sources += [D/'configuration.json',D/'requirements-lock.txt',
      W/'docs/developmental_ecology/p_apparatus_correction_20260924/CORRECTION_REPORT.md',W/'docs/developmental_ecology/p_apparatus_final_correction_20260925/FINAL_CORRECTION_REPORT.md',
      ROOT/'exports/2026-09-24-p-apparatus-review-05abf604/physical/RUNNER_AUTHORITY_CONTROLLER_REVIEW.md',
      ROOT/'exports/2026-09-25-p-apparatus-correction-review-9d31e790/physical/INDEPENDENT_CLOCK_REVIEW.md',
      ROOT/'exports/2026-09-25-p-apparatus-correction-review-9d31e790/LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md',
      ROOT/'exports/2026-09-25-p-final-mechanical-closure-5f077481/LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md']
    sources += [p for p in PACK.rglob('*') if p.is_file()]
    paths={'A1':D/'artifacts/first-commissioning-A1-20260925-5f077481/trajectory-001',
      'A2':D/'artifacts/commissioning-A2-20260925-5f077481/trajectory-001','A3':D/'artifacts/commissioning-A3-20260925-5f077481/trajectory-001'}
    paths.update({n:D/'artifacts/commissioning-A4-20260926-5f077481'/n/'trajectory-001' for n in ('A4-CROSS','A4-WAIT','A4-DETOUR')})
    sources += [p for folder in paths.values() for p in folder.iterdir() if p.is_file()]
    sources=list(sorted(set(sources)));before={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sources};write('SOURCE_IDENTITIES_BEFORE.json',before)
    history={'log':git('log','-5','--format=%H %s','--','developmental_ecology/loom_commissioning/pending.py','developmental_ecology/loom_commissioning/controllers.py'),
      'clock_guard_blame':git('blame','-L','37,62','--','developmental_ecology/loom_commissioning/pending.py')}
    write('CLOCK_HISTORY.json',history)
    # Scalar recurrence only. No body, field or controller state accompanies it.
    times=[0.]
    for _ in range(120000):times.append(times[-1]+.01)
    def detail(i):
        t=times[i];nominal=i*.01
        return {'index':i,'accumulated':t,'accumulated_hex':t.hex(),'accumulated_exact_decimal':decfloat(t),'index_product':nominal,'index_product_hex':nominal.hex(),
          'difference':t-nominal,'difference_exact_decimal':decfloat(t-nominal),'ulp':math.ulp(t),'absolute_guard_passes':abs(t-nominal)<=1e-10}
    first_native=next(i for i in range(120001) if abs(times[i]-i*.01)>1e-10)
    first_decision=next(i for i in range(0,120001,10) if abs(times[i]-i*.01)>1e-10)
    assert first_native==26941 and first_decision==26950
    checkpoints={str(i):detail(i) for i in (10,20,9000,12000,12800,18000,21000,25600,26940,26941,26950,27000,30000,45000,48000,51200,60000,63000,102400,120000)}
    scalar_ranges={}
    for top in (63000,120000):
        localmax=(0,None);roundmax=(0,None);ierr=(0,None);spacingmax=0;elapsed=0.;waves=0
        for j in range(top):
            q=abs(round((top*.01-times[j])/.01)-(top-j));roundmax=max(roundmax,(q,j)) if q>roundmax[0] else roundmax
            exact_error=float(abs(Fraction.from_float(j*.01)-Fraction(j,100)))
            if exact_error>ierr[0]:ierr=(exact_error,j)
            spacingmax=max(spacingmax,math.ulp(times[j]))
            if j%10==0:
                for progress in range(1,min(10,top-j)+1):
                    err=abs(times[j+progress]-(times[j]+progress*.01))
                    if err>localmax[0]:localmax=(err,[j,progress])
            elapsed+=.01
            if (j+1)%20==0:
                assert abs(elapsed-.2)<=1e-10;waves+=1;elapsed=0.
        assert roundmax[0]==0 and waves==top//20
        scalar_ranges[str(top)]={'max_absolute_accumulated_minus_index_product':max(abs(times[j]-j*.01) for j in range(top+1)),
          'max_index_product_error_vs_exact_decimal':ierr,'max_local_ten_step_elapsed_error':localmax,'max_remaining_native_count_error':roundmax[0],
          'max_ulp':max(spacingmax,math.ulp(times[top])),'scalar_native_count':top,'scalar_command_hold_count':top//10,'scalar_wave_boundaries':waves,
          'scalar_wave_elapsed_after20':sum([.01]*20),'field_cadence':'Source specifies one .01 call per full native step; no FieldSolver called in this diagnostic',
          'case_cutoff_predicate':abs(times[top]-top*.01)<1e-9,'minimum_recorded_clock_increment':min(times[j+1]-times[j] for j in range(top))}
    increments={}
    for t in (.1,90.,120.,128.,200.,256.,269.5,512.,630.,1024.,1200.):
        inc=(t+.01)-t
        increments[str(t)]={'ulp':math.ulp(t),'represented_increment':inc,'increment_minus_exact_point01':str(Fraction.from_float(inc)-Fraction(1,100)),
          'increment_error_float':float(Fraction.from_float(inc)-Fraction(1,100)),'one_e_minus10_in_ulps':1e-10/math.ulp(t),
          'added_1e_minus12_resolved':(t+1e-12)>t,'added_1e_minus14_resolved':(t+1e-14)>t}
    stages=m['execution']['procedure']['stages'];bounds=native_deadlines(m)
    def trace(i):
        t=times[i];cursor=0
        while cursor<len(stages)-1 and controllers.time_due(t,stages[cursor]['until']):cursor+=1
        deadline=stages[cursor]['until'];clock=SimpleNamespace(engine=SimpleNamespace(time=t,c=SimpleNamespace(native_dt=.01)),manifest=m)
        remaining=runner.Run.remaining(clock);steps=min(10,remaining);end=t+steps*.01
        return {'index':i,'time':t,'stage_from_existing_scalar_comparator':cursor,'stage_deadline':deadline,
          'route_complete_predicate':controllers.time_due(t,deadline),'remaining_expression':(m['hard_stop_time']-t)/.01,'remaining_native_steps':remaining,
          'held_steps':steps,'end_expression':end,'new_hold_stage_check':end<=deadline or controllers.time_due(deadline,end),
          'absolute_clock_check':abs(t-i*.01)<=1e-10,'case_guard_time_le_deadline_plus_1e_minus9':t<=630+1e-9,
          'integer_expected_stage':min(sum(i>=b for b in bounds),len(stages)-1),'integer_route_done':i>=bounds[-1],
          'integer_hold_end_within_expected_stage':i+steps<=bounds[min(sum(i>=b for b in bounds),len(stages)-1)]}
    traces={str(i):trace(i) for i in (26940,26950,26990,27000,30000,45000,48000,62990,63000)}
    # The exact A5 object is read unchanged. No grant, command or state is produced.
    # Sentinel inputs prove the clock rejection happens before any controller/input validation.
    direct=[]
    for i in (26940,26950,27000):
        d={'time':times[i],'native_index':i,'actor':contract.EXTERNAL,'controller':m['controller'],'inputs':{},'command':[0.,0.],
           'hold_native_steps':10,'annotation':'DETACHED CLOCK PREFIX ONLY; NOT AN ISSUED COMMAND','execution_sha256':HELD,'stage':None,'case_deadline':630.}
        got=outcome(lambda:pending.validate_decision(m,d))
        expected='forbidden controller input' if i==26940 else 'issued decision clock mismatch'
        assert got.get('message')==expected
        direct.append({'index':i,'scope':'Schema/authority/clock prefix only. Deliberately invalid downstream input sentinel; not a valid physical command.',**got})
    # Minimal dictionaries exercise complete manual pending predicates, not a launch
    # manifest/authority. They omit required commissioning fields and are never saved as grants.
    toy={'mode':contract.EXTERNAL,'controller':'manual_privileged','initial_time':0.,'initial_index':0,'hard_stop_time':630.}
    toyhash=authority.execution_sha256(toy)
    template=json.loads((D/'tests_apparatus/fixtures/review-boundary-input.json').read_bytes())
    pending_results=[]
    for start_index in (26940,26950,30000,62990):
        inputs=copy.deepcopy(template);inputs['time']=times[start_index]
        d={'time':times[start_index],'native_index':start_index,'actor':contract.EXTERNAL,'controller':'manual_privileged','inputs':inputs,'command':[0.,0.],
          'hold_native_steps':10,'annotation':'DETACHED NONEXECUTABLE CLOCK TEST','execution_sha256':toyhash,'stage':None,'case_deadline':630.}
        for progress in (0,7,9,10):
            s={'decision':d,'hold_remaining':10-progress,'held_command':[0.,0.],'cursor':0}
            e=SimpleNamespace(time=times[start_index+progress],native_index=start_index+progress,c=SimpleNamespace(native_dt=.01,event_time_tol=1e-10),status='paused')
            got=outcome(lambda:pending.validate_pending(toy,s,e))
            assert got['accepted'] is (start_index==26940)
            if start_index!=26940:assert got['message']=='issued decision clock mismatch'
            encoded=json.dumps({'time':e.time,'index':e.native_index,'session':s});decoded=json.loads(encoded)
            assert decoded['time']==e.time and decoded['session']==s
            pending_results.append({'issued_index':start_index,'progress':progress,'json_scalar_roundtrip_exact':True,'local_elapsed_error':e.time-(d['time']+progress*.01),**got})
        if start_index==26940:
            s['hold_remaining']=1
            bad=outcome(lambda:pending.validate_pending(toy,s,e));assert bad['message']=='pending remainder differs from issued native progress'
            pending_results.append({'issued_index':start_index,'negative':'stale positive remainder at completed hold',**bad})
    # Six pre-existing detached controller test cases only. All other test bodies,
    # including real short-world restart and large-clock one-step fixtures, are not run.
    assert not os.environ.get('CORRECTION_FAULT') and not os.environ.get('APPARATUS_FAULT') and not os.environ.get('FINAL_FAULT')
    import test_corrections as legacy
    legacy_results=[];ALLOW_LEGACY_CONTROLLER=True
    for t in (0.09999999999999999,math.nextafter(.1,-math.inf),.1,math.nextafter(.1,math.inf),.1+5e-11):
        legacy.test_exact_review_boundary(t);legacy_results.append({'test':'test_exact_review_boundary','time':t,'passed':True})
    legacy.test_final_stage_and_not_due_control();legacy_results.append({'test':'test_final_stage_and_not_due_control','passed':True})
    ALLOW_LEGACY_CONTROLLER=False
    # Read saved A1-A4 action metadata without a controller call or replay.
    prior=[]
    for label,folder in paths.items():
        rec=json.loads((folder/'manifest.json').read_bytes());mold=rec['contract'];deadlines=native_deadlines(mold)
        for n in ('controller.jsonl.gz','native.jsonl.gz'):
            assert sha(folder/n)==rec['files'][n]['sha256']
        with gzip.open(folder/'controller.jsonl.gz','rt',encoding='utf-8') as f:actions=[json.loads(l) for l in f]
        mismatch=[];maximum=0.
        for a in actions:
            expected=min(sum(a['native_index']>=b for b in deadlines),len(deadlines)-1)
            if a['stage']['index']!=expected:mismatch.append(a['native_index'])
            maximum=max(maximum,abs(a['time']-(mold['initial_time']+(a['native_index']-mold['initial_index'])*.01)))
        assert not mismatch and maximum<=1e-10
        prior.append({'case':label,'receipt_sha256':sha(folder/'manifest.json'),'controller_stream_sha256':sha(folder/'controller.jsonl.gz'),'action_count':len(actions),
          'maximum_saved_action_clock_error':maximum,'integer_stage_mismatches':mismatch,'final_time':rec['final_time'],'status':rec['status'],'replayed':False})
    # Integer-only schedule oracle covers the selected A5 bounds and preserved
    # seven-step global versus incompatible five-step interior examples.
    integer={'A5_deadline_native_indices':bounds,'A5_native_count':63000,'A5_command_count':6300,'A5_wave_boundaries':3150,
      'case_seven_native_steps':{'hold_length':min(10,7),'legal_global_shortening':True},
      'interior_five_native_steps':{'requested_hold_length':10,'deadline_native_index':5,'must_reject':10>5},
      'all_A5_holds_fit_their_index_stage':all(i+10<=bounds[min(sum(i>=b for b in bounds),len(bounds)-1)] for i in range(0,63000,10)),
      'no_world_time_overwrite':True,'no_controller_invocation':True}
    assert integer['all_A5_holds_fit_their_index_stage']
    uniform={'scope':'Detached scalar candidate comparison only; no production tolerance altered',
      'one_e_minus9_would_admit_zero_origin_clock_to1200':all(abs(times[i]-i*.01)<=1e-9 for i in range(0,120001,10)),
      'existing_early_control_time':.1-2e-10,'existing_due_result':controllers.time_due(.1-2e-10,.1),
      'uniform_one_e_minus9_due_result':math.isclose(.1-2e-10,.1,rel_tol=0.,abs_tol=1e-9),
      'only_guard_increase_leaves_t270_stage_rejection':not traces['27000']['new_hold_stage_check']}
    results={'diagnosis_only':True,'p_commit':P,'apparatus_commit':APP,'held_A5_sha256':HELD,'runtime':m['execution']['runtime'],
      'first_native_exceedance':detail(first_native),'first_decision_rejection':detail(first_decision),'checkpoints':checkpoints,'scalar_ranges':scalar_ranges,'float_increment_bins':increments,
      'binary_point01_exact_decimal':decfloat(.01),'binary_point01_minus_exact_decimal':str(Fraction.from_float(.01)-Fraction(1,100)),
      'A5_causal_scalar_traces':traces,'direct_production_prefix_results':direct,'detached_pending_predicate_results':pending_results,'existing_detached_test_results':legacy_results,
      'prior_saved_action_metadata':prior,'integer_schedule_oracle':integer,'uniform_tolerance_comparison':uniform,
      'max_mover_position_difference_bound_if_replacing_physical_time_at630':4*(2*math.pi/30)*abs(times[63000]-630),
      'counts':COUNTS,'forbidden_calls':BLOCKED,'tests_not_run':['All existing tests that create/advance/replay any world, including short pause/resume and one-step-at-1199.99 tests','Ecological trajectories','A5 controller against world','New prehistory','Physical convergence or throughput'],
      'no_production_edits':True,'no_replacement_authority':True,'elapsed_wall_seconds':time.perf_counter()-start}
    after={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sources}
    assert before==after and not BLOCKED and authority.execution_sha256(m)==HELD and not git('status','--porcelain').strip()
    write('SOURCE_IDENTITIES_AFTER.json',after);write('DIAGNOSTIC_RESULTS.json',results)
    write('PRESERVATION.json',{'source_count':len(before),'all_hashes_unchanged':before==after,'held_A5_hash_unchanged':HELD,'head':APP,'branch':git('branch','--show-current').strip(),'git_clean':True,'Git_writes':0,'production_code_edits':0,'new_authority_objects':0,'world_steps':0,'forbidden_calls':BLOCKED})
    print(json.dumps({'first_rejection':results['first_decision_rejection'],'scalar_ranges':scalar_ranges,'direct_prefix_results':direct,'legacy_test_cases':len(legacy_results),'prior_actions_checked':sum(v['action_count'] for v in prior),'counts':COUNTS,'preserved_sources':len(before),'output':str(O/'DIAGNOSTIC_RESULTS.json')},indent=2))
if __name__=='__main__':main()
