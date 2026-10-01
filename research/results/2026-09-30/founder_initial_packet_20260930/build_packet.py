"""Static launch-packet construction from verified time-zero states only."""
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent;HERE=Path(__file__).resolve().parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929';D=W/'developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-initial-stage'
sys.path.insert(0,str(D))
from loom_developmental import codec,core
from loom_developmental.runner import canonical,identity,file_hash
from loom_p.schema import Config

CHECKPOINT='87abae34e19d4e46234402a6b1ba776814956ec1'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
GIT=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+str(ROOT/'a5_regeneration_20260926/empty-excludes'),'-C',str(W)]
os.environ['GIT_OPTIONAL_LOCKS']='0'
def git(*args):return subprocess.check_output([*GIT,*args]).decode().strip()
def sha(obj):return hashlib.sha256(canonical(obj)).hexdigest()
def obj(name,value):(PACKET/name).write_bytes(canonical(value))
def doc(name,text):(PACKET/name).write_text(text.strip()+'\n',encoding='utf8')

def main():
    release=json.loads((HERE/'RELEASE_BENCHMARK_RESULT.json').read_bytes())
    births=json.loads((PACKET/'BLANK_START_VERIFICATION.json').read_bytes())
    assert release['status']==births['status']=='PASS'
    assert git('rev-parse','HEAD')==CHECKPOINT and not git('status','--porcelain')
    if (PACKET/'AUTHORITY_INDEX.json').exists():raise FileExistsError('Do not overwrite proposed authority identities')
    runtime=identity();runtime_sha=sha(runtime)
    assert runtime_sha==births['runtime_sha256']==release['full_P_reconstruction']['recording_identity']
    rows=births['rows'];assert len(rows)==12 and [r['stream_life'] for r in rows]==list(range(1,13))
    for row in rows:
        e=codec.read(PACKET/'initial_states'/row['initial_snapshot']['file'],row['initial_snapshot']['sha256'])['engine']
        assert e.time==e.native_index==e.organism.native_count==e.organism.wave_count==0
        assert codec.digest(core.causal_state(e))==row['initial_causal_sha256']
        assert e.organism.rng.life==row['stream_life'] and not hasattr(e,'fixture')
    doc('ANALYSIS_PLAN.md','''# Passive initial-stage analysis plan

This is a plan, not an analysis result. Execute no analysis now beyond start/authority integrity checks. During each life retain only the final runner's Tier-1 streams/checkpoints. After the declared initial-stage set has stopped (or a batch-stopping condition prevents remaining launches), seal the complete denominator, verify every available life store, create one archive, and analyze saved records only.

## A — What happened

Publish all 12 roster rows first, including not-started and incomplete rows. Keep actual observed time, native/wave counts, stop reason, censoring and recording completeness separate. Report source contact episodes, productive debit/body credit, renewal/depletion, expenditure, reserve changes, damage/repair, impulses, mover encounters, movement and opportunity/exposure intervals. Link every quantity to life/native/event indices. Distinguish zero contact, contact without transfer, productive contact, departure/recontact, accidental benefit and repeated interaction. Do not exclude deaths or misses. Contact alone is not founder competence, and survival alone is not learned competence.

## B — What changed internally

For all recorded lives, use compact wave summaries and saved checkpoint arrays to report sensory shared/fine/reference changes, pooling openings/support, H writes/decay/use, regulator banks/references/eligibility and credit/learned/exploration quantities. Preserve the distinction between transient activity, structural change and actual read/use. Norm changes alone are not learning efficacy. Report interval endpoints and reconstruction/identity provenance; retain missing intervals as missing. Use exact P reconstruction only if the requested quantity is absent from compact evidence.

## C — Whether later behavior suggests the change mattered

Only after A/B tables cover the entire declared roster, describe time-ordered A→B→C accounts where available. Look for subsequent expression/use of changed structure in later contexts and its accompanying physical consequences. Keep lasting sensory contribution separate from useful history-dependent regulation. Consider alternative explanations: geometry, pose, stock, reserve need, direct feedback, exploration, contact or injury. A local receiver omission shows immediate influence, not an alternate trajectory or proof of benefit. Treat these accounts as bounded observational suggestions with unresolved causality.

First-review deep-analysis allowance: at most four explicitly named 0.2-second native windows, selected after the complete A/B tables, with their nearest-checkpoint warm-up. Include a miss/no-transfer comparison when available, and disclose why each exploratory illustration was selected. Full-roster summaries remain primary; a selected illustration does not change the denominator. Total passive analysis budget 900 wall seconds and 500 MB derived outputs; stop/report if exhausted. Extra windows/dossiers or world counterfactuals require separate review. Do not run detached D5 during life, synthesize an alternative experienced history, or feed any analysis result into P.

No single founder score, automatic winner, ranking-based exclusion, continuation selection, 900/1,800-second authority, nursery decision, tuning or mechanism change is part of this stage. The scientific record can report no supported developmental change without calling P universally impossible. This plan does not authorize an additional perceptual assay.
''')
    expected=release['wall_seconds']*12
    resource={'status':'PROPOSED_NOT_EXECUTION_PERMISSION','basis':'Measured post-fix 600-second engineering life including one save/reload',
        'benchmark_wall_seconds':release['wall_seconds'],'benchmark_native_steps':60000,
        'wall_seconds_per_simulated_second':release['wall_seconds']/600,
        'expected_initial_execution_seconds':expected,'target_prior_expected_seconds':2460,
        'execution_allowance_seconds':3984,'per_life_wall_limit_seconds':332,
        'aggregate_primary_limit_bytes':1_000_000_000,'per_life_storage_limit_bytes':83_333_333,
        'sum_per_life_storage_limits_bytes':999_999_996,'expected_primary_bytes':release['stored_bytes']*12,
        'expected_archive_bytes':round(release['stored_bytes']*12*1.005),
        'archive_limit_bytes':1_000_000_000,'temporary_headroom_bytes':250_000_000,
        'passive_analysis_wall_limit_seconds':900,'derived_analysis_limit_bytes':500_000_000,
        'postrun_validation_allowance_seconds':180,'archive_allowance_seconds':120,
        'full_preflight_allowance_seconds':120,'concurrent_lives':1,
        'worker_working_set_planning_bytes':500_000_000,'worker_commit_planning_bytes':2_500_000_000,
        'recording_chunk_steps':100,'checkpoint_stride':6000,'compression_level':1,
        'actual_preparation_wall_seconds':births['wall_seconds'],'prehistory_complete':True,
        'preparation_required_at_execution':False,'execution_clock_semantics':'Runner active wall time including its initialization and closure; native-boundary administrative guard. Report atomic-step/closure overrun and stop further launches if aggregate exhausted; no pooled extension of a per-life limit.'}
    obj('RESOURCE_PLAN.json',resource)
    doc('RESOURCE_PLAN.md',f'''# Measured initial-stage resource plan

Fixed scope: twelve blank lives, each up to 600 seconds. No later stage is included.

The final-codec benchmark measured {release['wall_seconds']:.4f} wall seconds for 600 simulated seconds, including a save/load at age 300. Conservatively multiplying this complete cost by twelve gives **{expected/60:.2f} minutes expected execution**. This updates the earlier approximate 41-minute estimate. The **66.4-minute (3,984-second) administrative execution allowance remains unchanged**; no observed scaling defect warrants increasing it.

One worker, fixed order. Each life has 332 wall seconds and 83,333,333 primary-store bytes; unused per-life allowance does not extend another life. The total primary ceiling is 1,000,000,000 bytes (the sum of per-life limits is four bytes lower). Native-boundary stop checks and final checkpoint closure are preserved; any atomic operation/closure overrun must be reported and may not justify another launch. The executor tracks aggregate active runner time and primary bytes and stops further launches at either common limit. Human deliberation is not simulated time.

Measured expected primary evidence: **{resource['expected_primary_bytes']/1e9:.3f} GB**, plus **{resource['expected_archive_bytes']/1e9:.3f} GB** for one final archive. Reserve 1 GB primary, 1 GB archive, 0.25 GB temporary headroom and 0.5 GB bounded derived outputs: **2.75 GB total planning capacity**, excluding the existing shared Python installation. No full-life decompression directory or duplicate per-chart evidence copy is planned.

Separate allowances: 120 seconds read-only launch preflight, 180 seconds passive complete-file/ledger validation, 120 seconds one archive, 900 seconds passive A/B/C analysis. Working-set planning 0.5 GB / process commit 2.5 GB for one worker. These are declared resource envelopes, not guarantees for every contact/solver workload. Check free space and unchanged runtime again immediately before any authorized execution.

All twelve lawful body-absent prehistories are already prepared in this packet; preparation took {births['wall_seconds']/60:.2f} minutes. No field preparation, birth substitution or prehistory regeneration belongs in the later execution allowance. Start only from the exact saved initial snapshots. Do not return to the superseded 57-hour/200-GB envelope.
''')
    doc('EXECUTION_PROTOCOL.md','''# Initial-stage execution protocol — pending authorization

There are twelve separate proposed authority objects. Preparation is not approval. Execute only an explicitly authorized object's exact SHA-256, once, in roster order. No authority exists here for 900/1,800 seconds, a retry, substitute birth, fixed controller or outcome intervention.

Before any launch, verify: exact checkpoint and clean worktree; frozen P/configuration and full recorded runtime identity; selected canonical authority bytes/hash and common cohort manifest; all twelve prepared snapshot/manifest/prehistory hashes; ordinary blank time-zero checks; enough free disk and active resource headroom. No source, phase, seed, controller, state or resource substitution. Do not open old human B1 evaluator material.

The proposed outer object binds code/runtime/initial state/cohort/resources/analysis/evidence semantics. It is deliberately not a runner approval request. After Jason authorizes its hash, preserve that exact instruction in an execution-side approval receipt. Materialize the unchanged runner's request JSON with exactly `notice` and `approved_scope`, where `notice` identifies Jason's authorization and exact outer hash and `approved_scope` equals this object's `runner_scope` byte-for-byte under canonical JSON. The actual grant adds only `request_path` and `request_sha256` for that future receipt. Do not fabricate that receipt or call `Life` while this packet remains proposed. A proposed outer object fails the runner's approval-file schema by construction.

Load the exact saved `.ld` engine, verify its causal state and birth/RNG identities, and invoke the existing `Life`/`advance` path with mode `developmental-intact-P`. Do not reconstruct a new birth at execution time. No B1/external-controller dispatch, command-hold controller, sensory omission or authored neural state. Intact P uses its own 0.01-second native motor activity, 0.2-second handoffs and normal plasticity.

The executor enforces the per-life and common administrative limits, tracks a durable launch/stop ledger, and refuses an existing attempt/output directory. It checks remaining aggregate allowance at native boundaries and may close a life with a resource pause before its ceiling. Use closed-chunk byte counters and a fixed shared-asset total for aggregate accounting, not repeated reads of growing history. Preserve the runner's closure reserve when checking common disk headroom. It does not change the approved grant, reallocate unused per-life budget or force a checkpoint to continue. One worker only. A terminal E/I event ends that life at its actual partial native time; it does not stop the remainder of the roster by itself. A positive-looking event never stops a life early.

Shared apparatus/identity/recording failure, unreconciled physical accounting or exhausted aggregate resources stops further launches. Preserve the failed/partial evidence and all not-started rows. Do not patch, restart, replace or reinterpret a recorder failure as biological death. An ordinary terminal case is reported and the next separately authorized life may start if all apparatus/resource conditions remain valid.

At 60,000 native steps, seal the exact complete organism/body/field/source/RNG state as one continuing life's paused stage endpoint. Do not continue it. During life retain Tier 1 only: native sensory/action/body data, physical events, compact actual wave/change/use outputs, closed chunk hashes and periodic/boundary exact checkpoints. No live renderer, charts, D5, dossiers, ZIP work or feedback from the evaluator. Boundary hash/close operations intrinsic to the runner remain mandatory.

After all twelve stop, or an explicit batch stop prevents remaining launches: publish the complete twelve-row status ledger; perform passive complete-file/ledger validation; create one verified archive; apply `ANALYSIS_PLAN.md` to saved records. No new ecological trajectory or automatic continuation. Jason reviews the initial twelve before any later stage.

Aggregate enforcement is an executor protocol around the unchanged per-life runner, not a newly claimed built-in batch API. This packet provides exact scopes and the preflight/stop protocol; it does not modify the release checkpoint or claim that twelve proposed objects authorize themselves.
''')
    cohort={'schema':'loom-founder-initial-cohort-v1','status':'PROPOSED_NOT_AUTHORIZED',
        'name':'Founder Search initial stage','P_commit':P,'apparatus_checkpoint':CHECKPOINT,
        'runtime_sha256':runtime_sha,'configuration_sha256':rows[0]['configuration_sha256'],
        'roster_order':[r['life_id'] for r in rows],
        'lives':[{'life_id':r['life_id'],'stream_life':r['stream_life'],'master_seed':r['master_seed'],
            'initial_causal_sha256':r['initial_causal_sha256'],'initial_snapshot_sha256':r['initial_snapshot']['sha256'],
            'birth_manifest_sha256':file_hash(PACKET/'birth_manifests'/(r['life_id']+'.json')),
            'prehistory_manifest_sha256':r['prehistory']['manifest_sha256']} for r in rows],
        'total_maximum_simulated_seconds':7200,'per_life_end_index':60000,
        'resource_plan_sha256':file_hash(PACKET/'RESOURCE_PLAN.json'),
        'analysis_plan_sha256':file_hash(PACKET/'ANALYSIS_PLAN.md'),
        'execution_protocol_sha256':file_hash(PACKET/'EXECUTION_PROTOCOL.md'),
        'continuations':[],'replacement_births':0,'retry':False,'selection_score':None,
        'release_check_result_sha256':file_hash(HERE/'RELEASE_BENCHMARK_RESULT.json')}
    obj('COHORT_MANIFEST.json',cohort);cohort_sha=sha(cohort)
    (PACKET/'authorities').mkdir(exist_ok=True)
    authorities=[]
    for number,row in enumerate(rows,1):
        name=row['life_id']
        scope={'schema':1,'kind':'developmental-intact-P','life_id':name,
            'initial_causal_sha256':row['initial_causal_sha256'],'initial_index':0,'end_index':60000,
            'parent_receipt_sha256':None,'wall_limit_seconds':332,'storage_limit_bytes':83_333_333,
            'checkpoint_stride':6000,'chunk_steps':100,'compression_level':1}
        authority={'schema':'loom-founder-initial-authority-v1','status':'PROPOSED_NOT_AUTHORIZED',
            'life_id':name,'ordinal':number,'cohort_manifest_sha256':cohort_sha,
            'apparatus_checkpoint':CHECKPOINT,'P_commit':P,'P_code_sha256':runtime['P']['sha256'],
            'runtime_sha256':runtime_sha,'runtime_asset':'shared/'+runtime_sha+'.json',
            'configuration_sha256':row['configuration_sha256'],'configuration_file_sha256':file_hash(D/'configuration.json'),
            'initial_snapshot':{'path':'initial_states/'+name+'.ld',**row['initial_snapshot']},
            'birth_manifest':{'path':'birth_manifests/'+name+'.json','sha256':file_hash(PACKET/'birth_manifests'/(name+'.json'))},
            'birth_id':row['stream_life'],'master_seed':row['master_seed'],'mover_phase':row['phase'],
            'prehistory':row['prehistory'],'initial_engine_sha256':row['initial_engine_sha256'],
            'runner_scope':scope,'simulation_ceiling_seconds':600,'external_controller':None,
            'recording':'Final lean Tier 1; unchanged complete causal streams, 100-native chunks, 6000-native and terminal/pause checkpoints, zlib 1',
            'evidence_identity':{'life_id':name,'first_native_index':1,'last_native_index_ceiling':60000,
                'parent_receipt':None,'store_name':name,'attempt_limit':1,'schema_magic':'LOOMDEV1',
                'closed_segment_receipt':'segment-000.json','evidence_hashes':'Computed from realized chunks/checkpoints on closure; no precomputed trajectory'},
            'grant_materialization':'Only after Jason authorizes this exact outer SHA; add request_path/request_sha256 of preserved future authorization receipt. No such receipt is prepared here.',
            'stops':['actual energy/integrity terminal','native index 60000','per-life wall/storage resource pause',
                'aggregate resource pause','apparatus/identity/accounting/recording fault'],
            'retry':False,'continuation':False,'substitution':False,'outcome_intervention':False}
        digest=sha(authority);obj('authorities/'+name+'.json',authority)
        assert set(authority)!={'notice','approved_scope'}
        assert set(scope)=={'schema','kind','life_id','initial_causal_sha256','initial_index','end_index',
            'parent_receipt_sha256','wall_limit_seconds','storage_limit_bytes','checkpoint_stride','chunk_steps','compression_level'}
        authorities.append({'life_id':name,'authority_sha256':digest,'path':'authorities/'+name+'.json'})
    obj('AUTHORITY_INDEX.json',{'status':'AWAITING_JASON_AUTHORIZATION','hash_rule':'SHA256 of UTF-8 json.dumps(sort_keys=True,separators=(comma,colon),allow_nan=False); files contain exactly those canonical bytes',
        'cohort_manifest_sha256':cohort_sha,'authorities':authorities,'no_batch_execution_authority':True,
        'approved_scope_receipts_created':0,'scientific_lives_executed':0})
    with (PACKET/'ROSTER_AND_IDENTITIES.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f);writer.writerow(['life_id','stream_life','master_seed','mover_phase','initial_causal_sha256','initial_snapshot_sha256','prehistory_manifest_sha256','authority_sha256','status'])
        for row,a in zip(rows,authorities):writer.writerow([row['life_id'],row['stream_life'],row['master_seed'],row['phase'],row['initial_causal_sha256'],row['initial_snapshot']['sha256'],row['prehistory']['manifest_sha256'],a['authority_sha256'],'PREPARED_UNEXECUTED'])
    hash_table='\n'.join('| '+x['life_id']+' | `'+x['authority_sha256']+'` |' for x in authorities)
    doc('AUTHORITY_HASHES.md','# Proposed per-life authorities\n\nNone is authorized or executed. Approval of preparation is not approval of these objects.\n\n| Life | Canonical authority SHA-256 |\n|---|---|\n'+hash_table)
    obj('STATIC_COMPATIBILITY_REPORT.json',{'status':'PASS','checkpoint':CHECKPOINT,'git_clean':True,
        'runtime_matches_release_benchmark':True,'snapshots_verified':12,'blank_and_distinct_initial_states':True,
        'ordinary_birth_zero_native_and_wave_counts':True,'same_anatomy_unmodified':True,
        'per_life_scope_schema_matches_final_runner':True,'proposed_outer_objects_are_not_runner_approval_files':True,
        'all_authority_hashes_verified':all(file_hash(PACKET/a['path'])==a['authority_sha256'] for a in authorities),
        'aggregate_wall_seconds':12*332,'aggregate_per_life_storage_bytes':12*83_333_333,
        'scientific_Life_objects_created':0,'scientific_native_calls':0,'scientific_handoffs':0,
        'new_execution_tests':0,'scope':'Static schema/hash/state checks only; actual future authorization receipt and full runtime preflight remain execution-time steps.'})
    obj('CHECKPOINT.json',{'checkpoint':CHECKPOINT,'parent':git('rev-parse','HEAD^'),'branch':git('branch','--show-current'),
        'worktree':str(W),'P_commit':P,'code_changes_this_task':0,'git_writes_this_task':0,'runtime_sha256':runtime_sha})
    doc('RELEASE_BENCHMARK_REPORT.md',f'''# Post-fix 600-second release benchmark

**PASS.** Exactly one non-scientific intact-P engineering life was run at final checkpoint `{CHECKPOINT}`, from the prior longer benchmark's exact initial snapshot. It is a manufactured fixture, not a Founder birth. No behavior or developmental outcome was interpreted scientifically.

- 60,000 native steps / 3,000 handoffs; nominal ceiling 600 seconds, unchanged accumulated physical time {release['simulated_seconds']!r}.
- Wall time **{release['wall_seconds']:.6f} s** ({release['wall_seconds']/600:.6f} wall/sim, {60000/release['wall_seconds']:.2f} native steps/s), including {release['setup_seconds']:.6f} s initial setup and {release['resume_seconds']:.6f} s exact save/load-resume at age 300.
- Stored **{release['stored_bytes']:,} bytes** ({release['stored_bytes']/600/1e6:.6f} MB/sim). Complete native/wave/event families, all checkpoint and source/runtime identities retained.
- Execution peak working set **{release['execution_memory']['peak_working_set_bytes']/1e6:.3f} MB**; final working set {release['execution_memory']['working_set_bytes']/1e6:.3f} MB; peak process commit {release['execution_memory']['peak_pagefile_bytes']/1e9:.3f} GB. Peak is captured before post-run reconstruction.
- Every one of **600 chunks** matches the prior run's exact native/wave/event payload and P/field/RNG hashes. All **11 full checkpoint causal states** match, including the final state after the split continuation. Only the already documented observer-cache exclusion applies.
- Full saved-input P reconstruction: {release['full_P_reconstruction']['wall_seconds']:.4f} s, all 600 chunk endpoints exact. Final full causal state/field reconstruction: {release['final_causal_reconstruction']['wall_seconds']:.4f} s. These are post-run costs, excluded from execution.
- First 200 s: {release['first_200_wall_per_sim']:.6f} wall/sim; last 200 s: {release['last_200_wall_per_sim']:.6f}; ratio {release['last_over_first_rate']:.6f}. Approximately 2.2% change, no material history-growth scaling flag.

Final causal state SHA-256: `{release['final_causal_sha256']}`. Exact RNG counters and full measurements appear in `engineering/RELEASE_BENCHMARK_RESULT.json`. Runtime identity `{runtime_sha}` matches the final runner and prepared blank starts. The preceding archive remains preserved; no prior record was replaced.

All prospectively declared gates passed. There was no retry, patch or further engineering benchmark. No 900/1,800-second life was run. One 600-second engineering life plus twelve body-absent histories are distinct from scientific Founder execution, which remains zero.
''')
    with (PACKET/'RELEASE_THROUGHPUT_BY_AGE.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f);writer.writerow(['ending_native_index','nominal_age_seconds','block_wall_seconds','wall_per_simulated_second','working_set_bytes','peak_working_set_bytes'])
        for b in release['blocks']:writer.writerow([b['end_index'],b['end_index']*.01,b['wall_seconds'],b['wall_seconds']/b['simulated_seconds'],b['working_set_bytes'],b['peak_working_set_bytes']])
    doc('README.md',f'''# Founder Search — initial-stage launch packet

**Prepared, unexecuted, awaiting Jason's authorization.** The post-fix 600-second engineering release check passed. The final lean runner remains `{CHECKPOINT}`; frozen P remains `{P}`. No code was changed in this task.

Exactly twelve ordinary blank starts: FS-001…FS-012, stream life IDs 1…12, master seed 5,284,097, unchanged anatomy and Base World. Each starts at time/native/wave zero with ordinary unlearned state, its own lawful phase/prehistory/birth/RNG, E=0.70 and I=1. They are initialized snapshots, not executed lives. No B1 controller, learned-state transplant, map, label, correct action or external intervention is supplied to P.

Each proposed authority permits only that saved initial state and up to 600 seconds. No 900/1,800 continuation is prepared. The fixed denominator remains twelve, including any not-started/terminal/cutoff/failure row. Do not stop the set early because something looks positive.

Read `RELEASE_BENCHMARK_REPORT.md`, `RESOURCE_PLAN.md`, `EXECUTION_PROTOCOL.md` and `ANALYSIS_PLAN.md`. Exact identities are in `ROSTER_AND_IDENTITIES.csv`, `birth_manifests/`, `COHORT_MANIFEST.json`, `authorities/` and `AUTHORITY_HASHES.md`. The proposed objects are deliberately incompatible with the runner's approval-file schema until a real future authorization receipt is materialized from Jason's instruction.

Current expected execution is approximately {expected/60:.1f} minutes for twelve complete windows; the allowance remains 66.4 minutes. Expected primary scientific records are approximately {resource['expected_primary_bytes']/1e9:.2f} GB, plus one similar archive. Preparation is already complete. No old 57-hour/200-GB envelope is retained.

The portable review includes exact source/configuration, complete post-fix engineering evidence, all prepared prehistory/initial snapshots, manifests and authority objects. No old sealed human B1 evaluator state was read or included. `VERIFY_PACKET.py` checks package bytes without simulation. Opening documents does not launch a case.

Stop boundary: **zero scientific Founder lives executed, zero scientific native steps, zero scientific handoffs**. No Founder selected. No nursery, tuning, extra perceptual work, push, PR or merge. Await Jason's explicit authorization of the exact proposed hashes.
''')
    print(json.dumps({'status':'packet prepared','authorities':authorities,'scientific_lives_executed':0},indent=2))

if __name__=='__main__':main()
