"""Static construction only, after all 48 newborn snapshots are verified."""
import ast
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile
import prepare_expansion as q
from loom_developmental import codec,core
from loom_developmental.runner import identity,canonical,file_hash,atomic_json
from loom_p.records import state_hash,code_identity
from loom_p.prehistory import load
from prepare_blank_starts import verify_blank

HERE=q.HERE;ROOT=q.ROOT;PACKET=q.PACKET;D=q.D;PRIOR=q.PRIOR

def sha(value):return hashlib.sha256(canonical(value)).hexdigest()
def write(name,value):atomic_json(PACKET/name,value)
def doc(name,value):
    with (PACKET/name).open('x',encoding='utf8') as f:f.write(value.strip()+'\n')

def main():
    resolution=None
    if (HERE/'PREPARATION_HOLD.json').exists():
        if not (HERE/'PREPARATION_BOUNDARY_RESOLUTION.json').exists():raise RuntimeError('Unresolved preparation boundary; no authority construction')
        resolution=json.loads((HERE/'PREPARATION_BOUNDARY_RESOLUTION.json').read_bytes())
        assert resolution['status']=='PASS' and resolution['original_hold_sha256']==file_hash(HERE/'PREPARATION_HOLD.json')
        assert resolution['original_log_sha256']==file_hash(HERE/'PREPARATION_LOG.jsonl')
        assert resolution['blank_verification_sha256']==file_hash(PACKET/'BLANK_START_VERIFICATION.json')
        assert resolution['all_48_time_zero'] and resolution['field_histories_repeated']==0
        assert not (HERE/'REMAINING_PREPARATION_HOLD.json').exists()
    if (PACKET/'AUTHORITY_INDEX.json').exists():raise FileExistsError('No authority overwrite')
    births=json.loads((PACKET/'BLANK_START_VERIFICATION.json').read_bytes())
    assert births['status']=='PASS' and births['lives']==48 and births['scientific_lives_executed']==0
    q.source_gate();runtime=identity();assert sha(runtime)==q.RUNTIME==births['runtime_sha256']
    rows=births['rows'];assert [r['stream_life'] for r in rows]==list(range(13,61))
    grant_parser=next(n for n in ast.parse((D/'loom_developmental/runner.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='validate_grant')
    grant_keys=ast.literal_eval(next(n.value for n in grant_parser.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='keys' for t in n.targets)))
    current=[]
    for row in rows:
        name=row['life_id'];snap=row['initial_snapshot'];e=codec.read(PACKET/'initial_states'/snap['file'],snap['sha256'])['engine']
        e.validate_state();assert verify_blank(e)==row['blank']
        assert codec.digest(core.causal_state(e))==row['initial_causal_sha256'] and state_hash(e)==row['initial_engine_sha256']
        assert e.time==e.native_index==e.organism.native_count==e.organism.wave_count==0
        assert e.organism.rng.life==row['stream_life'] and e.organism.rng.counters==row['initial_rng_counters']
        assert e.phase==row['phase'] and e.c.identity()==row['configuration_sha256']
        pre=row['prehistory'];cache=PACKET/pre['path']
        assert file_hash(cache/'manifest.json')==pre['manifest_sha256'] and file_hash(cache/'fields.npz')==pre['field_file_sha256']
        assert hashlib.sha256(e.fields.tobytes()).hexdigest()==pre['field_array_sha256']
        fields,phase,_,pm=load(e.c,cache,life=row['stream_life'])
        assert phase==e.phase and codec.encode(fields)==codec.encode(e.fields)
        current.append(dict(life_id=name,time=e.time,native_index=e.native_index,wave_index=e.organism.wave_count,
            initial_causal_sha256=row['initial_causal_sha256'],snapshot_sha256=snap['sha256'],stream_life=row['stream_life']))
    for name in ('ANALYSIS_PLAN.md','EXECUTION_PROTOCOL.md'):shutil.copyfile(HERE/name,PACKET/name)
    projection=json.loads((PACKET/'RESOURCE_PROJECTION_BEFORE_AUTHORITY.json').read_bytes())
    resource=dict(projection,status='PROPOSED_NOT_AUTHORIZED',prehistory_complete=True,preparation_required_at_execution=False,
        preparation_aggregate_wall_guard_seconds=births.get('preparation_aggregate_wall_guard_seconds',projection['preparation_aggregate_wall_guard_seconds']),
        preparation_clock_basis=births.get('clock_basis','Single measured preparation segment'),
        preparation_boundary_resolution_sha256=file_hash(HERE/'PREPARATION_BOUNDARY_RESOLUTION.json') if resolution else None,
        per_life_wall_limit_seconds=900,execution_allowance_seconds=43200,
        archive_limit_bytes=4100000000,total_additional_planning_bytes=11600000000,
        archive_headroom_revision='4.1 GB archive ceiling includes overhead above a 4 GB primary cap; initial projection retained separately. No scientific recording change.',
        original_projection_sha256=file_hash(PACKET/'RESOURCE_PROJECTION_BEFORE_AUTHORITY.json'),
        administrative_proposal_revision='Before authority creation: 900 wall seconds per life instead of the initial 332-second proposal; allow for current slower body-absent preparation. Not a change to the 600-second simulated ceiling or a measured new-life throughput result.',
        slowdown_sensitivity_factor=3,slowdown_sensitivity_full_48_wall_seconds=3*projection['full_600_all_48_slowest_observed_rate_wall_seconds'],
        slowdown_sensitivity_per_600_life_wall_seconds=3*projection['worst_observed_life_wall_per_sim']*600,
        actual_field_history_mean_wall_seconds=sum(r['prehistory']['wall_seconds'] for r in rows)/48,
        actual_field_history_max_wall_seconds=max(r['prehistory']['wall_seconds'] for r in rows),
        actual_preparation_wall_seconds=births['wall_seconds'],sum_per_life_storage_limits_bytes=48*83333333,
        expected_archive_bytes=round(projection['full_600_all_48_primary_bytes']*1.005)+20000000,
        expected_archive_worst_observed_rate_bytes=round(projection['full_600_all_48_largest_observed_rate_primary_bytes']*1.005)+20000000,
        prior_evidence_not_duplicated=True,
        execution_clock_semantics='One worker active runner wall time including init/closure; native-boundary guard; no unused per-life budget redistribution.',
        resource_limits_are_administrative_not_physical=True,deep_window_proposal_cap=196,deep_window_native_width=20,
        original_12_deep_windows_reused_not_rerun=True)
    write('RESOURCE_PLAN.json',resource)
    if resolution:
        doc('PREPARATION_BOUNDARY_NOTE.md',f'''# Preparation resource boundary

The initial preparation segment reached its 4,800-second wall guard and stopped between completed field histories. Its original hold record and log are preserved. It completed {len(resolution['completed_preserved'])} starts at time zero.

Only the {len(resolution['newly_prepared'])} still-unprepared streams from the roster declared before preparation were then prepared, under an 8,000-second total preparation allowance. This completed Jason's requested preparation of 48; it did not start or continue a Founder life, repeat a field history, replace a birth or change production code. The completed first-segment assets were checked byte-for-byte unchanged. The original field solver and its per-history guard were unchanged.

Measured preparation segments total {births['wall_seconds']/60:.2f} minutes; the intervening review gap is excluded. BLANK_START_VERIFICATION.json also records elapsed wall time from the initial preparation marker. The initial resource estimate, original administrative stop, revised preparation notice and completion checks are all included in preparation/. Every new organism remains at time/native/wave zero.
''')
    priorseal=json.loads((PRIOR/'DENOMINATOR_SEALED.json').read_bytes())
    priordelivery=json.loads((PRIOR/'DELIVERY_VERIFICATION.json').read_bytes())
    priorarchive=json.loads((PRIOR/'ARCHIVE_VERIFICATION.json').read_bytes())
    for filename in ('DENOMINATOR_SEALED.json','DELIVERY_VERIFICATION.json','ARCHIVE_VERIFICATION.json','FOUNDER_SEARCH_INITIAL_STAGE_REPORT.md'):
        shutil.copyfile(PRIOR/filename,PACKET/'references'/('FIRST_12_'+filename))
    prior_entries=[]
    for old in priorseal['roster']:
        p=PRIOR/'lives'/old['life_id']/'segment-000.json';r=json.loads(p.read_bytes())
        assert file_hash(p)==old['receipt_sha256'] and r['status']=='terminal'
        prior_entries.append(dict(life_id=old['life_id'],status='PRESERVED_TERMINAL',authority_sha256=old['authority_sha256'],
            receipt_sha256=old['receipt_sha256'],final_causal_sha256=r['final_causal_sha256'],final_time=r['final_time'],
            native_steps=r['native_steps'],archive_member='execution/lives/'+old['life_id']+'/segment-000.json',
            continuation=False,new_execution=False))
    cohort=dict(schema='loom-founder-expansion-cohort-v1',status='PROPOSED_NOT_AUTHORIZED',name='Founder Search current-world expansion by 48',
        P_commit=q.P,apparatus_checkpoint=q.CHECKPOINT,configuration_sha256=rows[0]['configuration_sha256'],
        runtime_sha256=q.RUNTIME,new_lives=48,preserved_prior_lives=12,combined_roster_size=60,
        roster_order=[r['life_id'] for r in rows],stream_lives=list(range(13,61)),master_seed=5284097,
        first_twelve=prior_entries,first_twelve_archive_sha256=priorarchive['sha256'],
        first_twelve_archive_name=Path(priorarchive['path']).name,first_twelve_report_sha256=file_hash(PRIOR/'FOUNDER_SEARCH_INITIAL_STAGE_REPORT.md'),
        request_sha256=file_hash(PACKET/'references/JASON_EXPANSION_REQUEST.txt'),
        lives=[dict(life_id=r['life_id'],stream_life=r['stream_life'],master_seed=r['master_seed'],
            initial_causal_sha256=r['initial_causal_sha256'],initial_snapshot_sha256=r['initial_snapshot']['sha256'],
            birth_manifest_sha256=file_hash(PACKET/'birth_manifests'/(r['life_id']+'.json')),
            prehistory_manifest_sha256=r['prehistory']['manifest_sha256']) for r in rows],
        each_simulated_ceiling_seconds=600,per_life_end_index=60000,total_maximum_new_simulated_seconds=28800,
        resource_plan_sha256=file_hash(PACKET/'RESOURCE_PLAN.json'),analysis_plan_sha256=file_hash(PACKET/'ANALYSIS_PLAN.md'),
        execution_protocol_sha256=file_hash(PACKET/'EXECUTION_PROTOCOL.md'),retry=False,replacement_births=0,
        continuations=[],selection_score=None,nursery_authorized=False)
    write('COHORT_MANIFEST.json',cohort);cohort_sha=sha(cohort)
    authority_rows=[]
    for ordinal,row in enumerate(rows,1):
        name=row['life_id'];scope=dict(schema=1,kind='developmental-intact-P',life_id=name,
            initial_causal_sha256=row['initial_causal_sha256'],initial_index=0,end_index=60000,parent_receipt_sha256=None,
            wall_limit_seconds=resource['per_life_wall_limit_seconds'],storage_limit_bytes=83333333,checkpoint_stride=6000,chunk_steps=100,compression_level=1)
        assert set(scope)==grant_keys-{'request_path','request_sha256'}
        assert scope['initial_index']==0 and scope['end_index']==60000 and scope['parent_receipt_sha256'] is None
        assert scope['storage_limit_bytes']>=16000000 and scope['checkpoint_stride']%scope['chunk_steps']==0
        authority=dict(schema='loom-founder-expansion-authority-v1',status='PROPOSED_NOT_AUTHORIZED',
            life_id=name,ordinal=ordinal,birth_id=row['stream_life'],master_seed=row['master_seed'],mover_phase=row['phase'],
            P_commit=q.P,P_code_sha256=code_identity()['sha256'],apparatus_checkpoint=q.CHECKPOINT,
            runtime_sha256=q.RUNTIME,runtime_asset='shared/'+q.RUNTIME+'.json',cohort_manifest_sha256=cohort_sha,
            configuration_sha256=row['configuration_sha256'],configuration_file_sha256=file_hash(D/'configuration.json'),
            initial_snapshot=dict(path='initial_states/'+name+'.ld',**row['initial_snapshot']),
            birth_manifest=dict(path='birth_manifests/'+name+'.json',sha256=file_hash(PACKET/'birth_manifests'/(name+'.json'))),
            initial_engine_sha256=row['initial_engine_sha256'],prehistory=row['prehistory'],runner_scope=scope,
            simulation_ceiling_seconds=600,external_controller=None,
            evidence_identity=dict(life_id=name,first_native_index=1,last_native_index_ceiling=60000,parent_receipt=None,
                store_name=name,attempt_limit=1,schema_magic='LOOMDEV1',closed_segment_receipt='segment-000.json',
                evidence_hashes='Realized only on closure; no precomputed trajectory'),
            recording='Unchanged lean Tier 1; complete native/event and compact wave evidence; 100-native chunks; 6000-native/terminal/pause checkpoints; zlib 1',
            grant_materialization='Only after Jason authorizes this exact outer hash; add request_path/request_sha256 of preserved actual approval receipt. None exists in this packet.',
            stops=['actual energy/integrity terminal','native index 60000','per-life wall/storage resource pause',
                   'aggregate resource pause','apparatus/identity/accounting/recording fault'],
            retry=False,continuation=False,substitution=False,outcome_intervention=False,
            first_cohort_death_age_is_not_deadline=True,positive_witness_does_not_end_case=True)
        write('authorities/'+name+'.json',authority)
        authority_rows.append(dict(life_id=name,authority_sha256=sha(authority),path='authorities/'+name+'.json'))
    write('AUTHORITY_INDEX.json',dict(status='AWAITING_JASON_AUTHORIZATION',authorities=authority_rows,
        cohort_manifest_sha256=cohort_sha,canonical_rule='SHA256 of UTF-8 json.dumps(sort_keys=True,separators=(comma,colon),allow_nan=False); exact file bytes',
        runner_approval_requests_created=0,scientific_lives_executed=0,index_is_not_batch_execution_authority=True))
    finish(rows,current,authority_rows,cohort,resource,prior_entries,priorarchive)

def finish(rows,current,authorities,cohort,resource,prior_entries,priorarchive):
    with (PACKET/'ROSTER_AND_IDENTITIES.csv').open('x',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['life_id','stream_life','master_seed','mover_phase','initial_causal_sha256','snapshot_sha256','prehistory_manifest_sha256','authority_sha256','status'])
        for r,a in zip(rows,authorities):w.writerow([r['life_id'],r['stream_life'],r['master_seed'],r['phase'],r['initial_causal_sha256'],r['initial_snapshot']['sha256'],r['prehistory']['manifest_sha256'],a['authority_sha256'],'PREPARED_UNEXECUTED'])
    combined=[dict(x,cohort='original_12') for x in prior_entries]+[
        dict(life_id=r['life_id'],cohort='expansion_48',status='PREPARED_UNEXECUTED',stream_life=r['stream_life'],
            initial_causal_sha256=r['initial_causal_sha256'],authority_sha256=a['authority_sha256'],new_execution=False,
            observed_age=0,continuation=False) for r,a in zip(rows,authorities)]
    write('COMBINED_60_ROSTER.json',dict(status='12_PRESERVED_TERMINAL_48_PREPARED_UNEXECUTED',rows=combined,
        all_60_not_claimed_executed=True,cohort_manifest_sha256=sha(cohort),prior_archive_sha256=priorarchive['sha256']))
    doc('AUTHORITY_HASHES.md','# Proposed 48 independent authorities\n\nPrepared only. Jason must authorize exact hashes before any life executes. The index hash is not a batch execution authority.\n\n| Order | Life | Canonical SHA-256 |\n|---|---|---|\n'+
        '\n'.join(f"| {i} | {a['life_id']} | `{a['authority_sha256']}` |" for i,a in enumerate(authorities,1)))
    doc('RESOURCE_PLAN.md',f'''# Expansion resource plan — proposed

Measured first-cohort basis: twelve lives, {resource['measured_simulated_seconds']:.9f} simulated seconds, {resource['measured_wall_seconds']:.6f} active wall seconds and {resource['measured_primary_bytes']:,} primary bytes. The measured weighted rates are {resource['weighted_wall_per_sim']:.9f} wall seconds/simulated second and {resource['weighted_bytes_per_sim']:.3f} bytes/simulated second. The slowest and largest per-life rates were {resource['worst_observed_life_wall_per_sim']:.9f} and {resource['worst_observed_life_bytes_per_sim']:.3f}, respectively. These projections were saved before any expansion authority was created.

For **48 full 600-second windows**, the weighted projection is **{resource['full_600_all_48_wall_seconds']/60:.2f} minutes** and **{resource['full_600_all_48_primary_bytes']/1e9:.3f} GB** primary evidence. Using the slowest/largest observed per-life rates gives **{resource['full_600_all_48_slowest_observed_rate_wall_seconds']/60:.2f} minutes** and **{resource['full_600_all_48_largest_observed_rate_primary_bytes']/1e9:.3f} GB**. These are linear projections, not guarantees for contact-rich workloads. The preserved complete 600-second release benchmark remains a consistency reference; no new benchmark or recorder optimization was run.

If actual ages happened to match the first cohort, four times its measured cost would be {resource['historical_duration_scenario_only_wall_seconds']/60:.2f} minutes and {resource['historical_duration_scenario_only_primary_bytes']/1e9:.3f} GB. **This is only a historical-duration scenario, never the execution ceiling.** Positive intake may permit longer life, and every case retains its 600-second / native-index 60000 limit.

One worker. Proposed per-life resource allowance: **900 active wall seconds and 83,333,333 bytes**. Aggregate: **43,200 active wall seconds (12 hours), 4 GB primary**, with fixed shared/input/metadata totals included; no unused per-life resource redistribution. This is an administrative proposal awaiting approval, not a 900-second developmental stage: the simulated age ceiling remains exactly 600 seconds. Unchanged Tier 1, 100-native chunks, 6000-native checkpoints and compression level 1. Preserve the existing 16 MB per-life closure reserve. Actual atomic-step/closure overrun must be reported, and shared resource exhaustion prevents further launches.

The initial projection retained the first cohort's 332-second wall allowance. Before creating these authorities, the proposal was increased to 900 wall seconds for all 48, because current body-absent histories have shown materially slower throughput. Their actual mean/max preparation cost is {resource['actual_field_history_mean_wall_seconds']:.2f}/{resource['actual_field_history_max_wall_seconds']:.2f} seconds, versus a first-cohort mean of approximately 50.61 seconds. This is evidence of preparation cost, **not a new-life benchmark**. As a disclosed sensitivity calculation, three times the slowest first-cohort life rate gives {resource['slowdown_sensitivity_per_600_life_wall_seconds']:.2f} wall seconds per full life and {resource['slowdown_sensitivity_full_48_wall_seconds']/3600:.2f} hours for 48. Adding 25% per-life headroom gives approximately 883 seconds, rounded to the proposed 900. The original measured projections above remain unchanged; actual future execution costs may differ. No recorder optimization, scientific tuning or new organism step was used to obtain this proposal. RESOURCE_PROJECTION_BEFORE_AUTHORITY.json preserves the initial estimate; RESOURCE_PLAN.json records this pre-authorization revision.

Budget **4.1 GB** for the sole future expansion results archive, **1 GB** temporary headroom and **2.5 GB** bounded derived analysis: **11.6 GB additional planning capacity**, including 4 GB primary. The archive allowance includes 100 MB above the primary cap for packet/container overhead; this refines the initial 4 GB archive estimate before authority creation. Keep the original cohort evidence/archive unchanged; reference its hashes rather than duplicating its complete records. Expected archive at weighted rates is approximately {resource['expected_archive_bytes']/1e9:.3f} GB, or {resource['expected_archive_worst_observed_rate_bytes']/1e9:.3f} GB using the largest observed primary rate.

Separate proposed allowances: preflight 480 s; passive complete-record validation 720 s; one archive 480 s; passive combined A/B/C 4500 s. The analysis cap includes any detached missing-operand reconstruction, receiver windows and report production. Up to four 0.2-second receiver windows per consequential expansion life plus four comparisons are proposed (hard maximum 196; not a quota). All are post-run only and share that budget. Unanalysed intervals remain pending if a ceiling is reached. These expanded analysis limits are proposals bound into the new authorities, not work executed now.

Working-set planning remains 500 MB and process-commit planning 2.5 GB for one scientific worker. No contact-rich scaling measurement is invented. Do not optimize the recorder merely because this population is larger.

The 48 ordinary starts and phase-matched body-absent prehistories are now complete. Measured preparation took **{resource['actual_preparation_wall_seconds']/60:.2f} minutes** ({resource['preparation_clock_basis']}). The total preparation allowance was {resource['preparation_aggregate_wall_guard_seconds']} seconds. See BLANK_START_VERIFICATION.json, the preparation logs and PREPARATION_BOUNDARY_NOTE.md when present for the exact boundary records. This task advanced fields from −600 to 0 with no body, then initialized each ordinary newborn. **No Founder organism time advanced.** Do not repeat field preparation or substitute a birth at launch.
''')
    doc('PRIOR_EVIDENCE_AND_INTERPRETATION.md','''# Preserved first-cohort evidence and Jason's review

Observed, verified FS-001–FS-012 facts remain: all twelve executed exactly once; all ended through energy depletion at approximately 429.219–429.948 seconds; zero source contact/transfer; three lives entered the descriptive source surface-gap band at most 1 world unit; FS-006 reached gap 0.0303067685 without contact; internal structure changed and later expression occurred; useful developmental benefit was not established. Exact prior reports, denominator and custody receipts are copied into references without modifying their originals.

Jason's accepted interpretation, recorded in references/JASON_EXPANSION_REQUEST.txt: the initial cohort provided no useful positive-energy encounter from which to assess accumulation of beneficial source-related experience. Twelve lives are insufficient to conclude the current ecology is too sparse. No founder is selected from those twelve, and no terminal life is continued.

This packet proposes 48 additional ordinary blank starts under the same scientific configuration, bringing the roster to 60. It does not claim 60 executed lives, new observations of opportunity or a solution to a mechanism problem. The combined analysis plan separates scarcity, internal change/use and possible benefit. Nursery, tuning and next-population decisions remain Jason's later review decisions.
''')
    write('CHECKPOINT.json',dict(checkpoint=q.CHECKPOINT,parent=q.git('rev-parse','HEAD^'),branch=q.git('branch','--show-current'),
        worktree=str(q.W),P_commit=q.P,runtime_sha256=q.RUNTIME,git_clean=True,source_changes=0,git_writes=0))
    assert all(file_hash(PACKET/a['path'])==a['authority_sha256'] for a in authorities)
    write('STATIC_COMPATIBILITY_REPORT.json',dict(status='PASS',checkpoint=q.CHECKPOINT,runtime_sha256=q.RUNTIME,
        authority_count=48,authority_hashes_match=all(file_hash(PACKET/a['path'])==a['authority_sha256'] for a in authorities),
        clean_frozen_source=True,scientific_configuration_identical_to_first_cohort=True,
        new_life_streams=list(range(13,61)),same_ordinary_anatomy=True,all_48_blank_time_zero=current,
        prepared_initial_state_reuse=0,extra_source_proximity_filter=False,controller=None,
        each_ceiling_seconds=600,each_deadline_native=60000,initial_scope_parent=None,
        request_schema_not_materialized=True,runner_approval_requests_created=0,
        runner_scope_keys_checked_against_unchanged_parser_AST=True,
        scientific_Life_objects_created=0,scientific_native_calls=0,scientific_handoffs=0,scientific_lives_executed=0,
        body_absent_field_steps=2880000,prior_lives_untouched=True,combined_roster_size=60,
        source_or_configuration_modifications=0,new_engineering_tests_or_benchmarks=0,
        no_old_sealed_human_B1_access=True,scope='Read-only state/hash/schema/law checks after authorized body-absent preparation; future exact approval and execution preflight still required.'))
    doc('README.md',f'''# Founder Search expansion — 48 prepared blank lives

**Prepared, all at time zero, unexecuted, awaiting Jason's authorization.**

FS-013–FS-060 use the next consecutive independent life streams 13–60, master seed 5284097, unchanged ordinary anatomy/birth law and exact Base World/configuration. Frozen P `{q.P}`; lean runner `{q.CHECKPOINT}`; full runtime `{q.RUNTIME}`. No source-distance filtering, authored competence, initial-state reuse, learned transplant or external controller. The 48 stream IDs and order were declared before generating any of their starts.

Each separate authority proposes only its exact saved blank snapshot through biological nonviability, a valid apparatus/resource stop or **600 total simulated seconds**, whichever first. The first cohort's death ages are not a shortened ceiling. No retry, replacement, continuation, tuning, new world, nursery or 900/1800-second stage is prepared. All 48 must finish or meet a shared-stop boundary before outcome-dependent analysis/selection. No founder selection is automatic after completion either.

Read RESOURCE_PLAN.md, EXECUTION_PROTOCOL.md and ANALYSIS_PLAN.md. AUTHORITY_HASHES.md lists all **48 new independent canonical identities**; AUTHORITY_INDEX.json is their machine-readable index, not an execution approval. Exact starts, birth/RNG identities and field-history provenance are in ROSTER_AND_IDENTITIES.csv, birth_manifests, initial_states and prehistory. COHORT_MANIFEST.json binds these with the preserved twelve and all common plans. COMBINED_60_ROSTER.json explicitly distinguishes **12 terminal prior lives + 48 unexecuted newborns**.

Future full-window projection: **{resource['full_600_all_48_wall_seconds']/60:.1f}–{resource['full_600_all_48_slowest_observed_rate_wall_seconds']/60:.1f} minutes**, **{resource['full_600_all_48_primary_bytes']/1e9:.2f}–{resource['full_600_all_48_largest_observed_rate_primary_bytes']/1e9:.2f} GB** of primary records at observed first-cohort rates. Current slower field preparation motivates a disclosed three-times-throughput sensitivity of {resource['slowdown_sensitivity_full_48_wall_seconds']/3600:.2f} hours; it is not a new-life benchmark. Proposed administrative execution ceiling: **12 hours / 4 GB primary**, individual limits **900 wall seconds / 83,333,333 bytes**. Simulated age remains **600 seconds**, never 900. See the resource plan for the initial 332-second proposal, the pre-authorization revision and all separate allowances.

The passive combined plan covers all 60 opportunity/physical histories, source event timing and transfer, E/I, contraction and sensory/association/regulator histories, and bounded later-expression checks. Zero contacts in 60 fully observed valid lives would imply a rough 95% upper frequency bound near 5% under the stated binomial assumptions; that would be a candidate opportunity bottleneck, not automatic nursery permission.

This preparation computed **48 body-absent field histories** (2,880,000 field steps over −600 to 0), then initialized ordinary newborns. **Zero scientific lives, native organism steps or P handoffs executed.** The distinction is explicit; this is not a claim of zero field computation. STATIC_COMPATIBILITY_REPORT.json and BLANK_START_VERIFICATION.json verify all time/native/wave indices are zero.

The portable packet includes exact frozen source/configuration, runtime identity hashes, all 48 starts/history files, authorities and current instructions. The original results archive remains separate and unchanged, SHA256 `{priorarchive['sha256']}`. No old sealed human B1 material was read or packaged. Opening this packet does not start a life.

Stop boundary: await Jason's approval of exact new authority objects. No expansion life has execution permission yet.
''')
    package()

def package():
    # Package portable frozen sources once; no dependency installation or source editing.
    target=PACKET/'source/developmental_ecology'
    for name in ('loom_p','loom_developmental','loom_commissioning'):
        (target/name).mkdir(parents=True)
        for p in sorted((D/name).glob('*.py')):shutil.copyfile(p,target/name/p.name)
    shutil.copyfile(D/'configuration.json',target/'configuration.json')
    (PACKET/'preparation').mkdir()
    for name in ('prepare_expansion.py','build_expansion_packet.py','PREPARATION_STARTED.json','PREPARATION_LOG.jsonl'):
        shutil.copyfile(HERE/name,PACKET/'preparation'/name)
    for name in ('finish_remaining_preparation.py','PREPARATION_HOLD.json','REMAINING_PREPARATION_STARTED.json',
                 'REMAINING_PREPARATION_LOG.jsonl','PREPARATION_BOUNDARY_RESOLUTION.json'):
        if (HERE/name).exists():shutil.copyfile(HERE/name,PACKET/'preparation'/name)
    # Historical helper source is provenance; its main is never invoked here.
    shutil.copyfile(ROOT/'founder_initial_packet_20260930/prepare_blank_starts.py',PACKET/'preparation/first_cohort_blank_check_source.py')
    doc('VERIFY_PACKET.py','''"""Read-only standard-library packet/ZIP verification; never starts a life."""
import hashlib,json,pathlib,sys,zipfile
p=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
if p.is_file():
    with zipfile.ZipFile(p) as z:
        m=json.loads(z.read('PACKAGE_MANIFEST.json'))
        for r in m['files']:
            b=z.read(r['path']);assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
else:
    m=json.loads((p/'PACKAGE_MANIFEST.json').read_bytes())
    for r in m['files']:
        b=(p/r['path']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
print(json.dumps({'status':'PASS','files':len(m['files']),'new_lives_executed':0,'scope':'byte custody only'}))
''')
    q.source_gate();assert sha(identity())==q.RUNTIME
    files=[dict(path=p.relative_to(PACKET).as_posix(),bytes=p.stat().st_size,sha256=file_hash(p)) for p in sorted(PACKET.rglob('*')) if p.is_file()]
    write('PACKAGE_MANIFEST.json',dict(schema=1,files=files,checkpoint=q.CHECKPOINT,P_commit=q.P,
        authority_count=48,new_lives_executed=0,manifest_excludes_itself_and_external_delivery_receipt=True))
    archive=PACKET.with_suffix('.zip')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
        for p in sorted(PACKET.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(PACKET).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(files)+1
        for r in files:
            data=z.read(r['path']);assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
    report=dict(status='PASS',archive=str(archive),archive_sha256=file_hash(archive),archive_bytes=archive.stat().st_size,
        verified_packet_files=len(files),manifest_sha256=file_hash(PACKET/'PACKAGE_MANIFEST.json'),
        authority_index_sha256=file_hash(PACKET/'AUTHORITY_INDEX.json'),cohort_manifest_sha256=file_hash(PACKET/'COHORT_MANIFEST.json'),
        all_new_lives_time_zero=True,new_lives_prepared=48,new_lives_executed=0,organism_native_calls=0,P_handoffs=0,
        body_absent_field_steps=2880000,code_configuration_unchanged=True,git_clean=True,git_writes=0,
        preparation_boundary_resolution_sha256=file_hash(HERE/'PREPARATION_BOUNDARY_RESOLUTION.json') if (HERE/'PREPARATION_BOUNDARY_RESOLUTION.json').exists() else None,
        field_histories_repeated=0,
        new_runner_approvals=0,stop='AWAIT_JASON_EXACT_AUTHORITY_APPROVAL')
    atomic_json(HERE/'DELIVERY_VERIFICATION.json',report)
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
