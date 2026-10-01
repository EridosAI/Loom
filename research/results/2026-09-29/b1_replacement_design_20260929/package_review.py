"""Package and verify design-only documents; never import Loom or decode trajectories."""
import datetime,hashlib,json,os,pathlib,shutil,subprocess,zipfile
S=pathlib.Path(__file__).resolve().parent;R=S.parent
W=R/'worktrees/loom-p-b1-coordinate-colours-20260929';D=W/'developmental_ecology'
E=R/'exports/2026-09-29-B1-automated-reference-design-v0-1'
B=R/'b1_hidden_execution_20260929_01';F=R/'b1_execution_20260929_colours_01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(R/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()=='b684912eaf7811cd318ee94c77172aca790f3a0d'
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
assert js(B/'STATE.json')['live_services']==0 and js(B/'STATE.json')['execution_authorization_withdrawn']
assert js(B/'WITHDRAWAL_RECEIPT.json')['prior_lifecycle']=='prepared'
assert js(B/'WITHDRAWAL_RECEIPT.json')['native_steps']==js(B/'WITHDRAWAL_RECEIPT.json')['commands']==0
for root,manifest in ((F,'COMPLETED_ATTEMPT_FILE_MANIFEST.json'),(B,'WITHDRAWN_FILE_MANIFEST.json')):
    for n,v in js(root/'private'/manifest)['files'].items():
        p=root/'private'/n
        assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes']
op=R/'exports/2026-09-29-B1-colour-labels-b684912e/B1_OPERATOR_PACKET'
for n,v in js(op/'FILE_MANIFEST.json')['files'].items():assert sha(op/n)==v['sha256']
assert not E.exists();E.mkdir(parents=True)
for name in ('README.md','B1_AUTOMATED_REFERENCE_DESIGN_v0_1.md','REQUEST.md'):cp(S/name,E/name)
for name in ('WITHDRAWAL_RECEIPT.json','WITHDRAWAL_PRESERVATION.json','WITHDRAWN_SERVICE_STOP_RECEIPT.json'):
    cp(B/name,E/'closure'/name)
cp(R/'research_direction_20260929/JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md',E/'references/JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md')
sources=[
 R/'AGENTS.md',W/'00_LOOM_CURRENT_STATE.md',
 R/'exports/2026-09-23-p-commissioning-design-2fb3ff84/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md',
 op/'B1_SEALED_AUTHORITY_IDENTITIES.json',op/'DISPLAY_CONTRACT.json',op/'PROTOCOL_CONTRACT.json',op/'INTERPRETATION_TABLE.md',op/'RESOURCE_PROJECTION.json',
 R/'research_direction_20260929/JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md',
 F/'FULL_RAW_OPERATOR_COMPLETION.json',B/'WITHDRAWAL_RECEIPT.json',
 R/'exports/2026-09-26-A4-launch-packet-5f077481/references/A2_RESOURCE_RESULT.json',
 R/'exports/2026-09-26-A4-launch-packet-5f077481/references/A3_RESOURCE_RESULT.json',
 R/'exports/2026-09-26-A5-commissioning-result-68db2c58/A5_COMMISSIONING_RESULT/RESOURCE_RESULT.json',
 *[D/'loom_commissioning'/name for name in ('controllers.py','operator_view.py','authority.py','runner.py','sensor_ui.py','evaluation.py')],
 D/'configuration.json',S/'REQUEST.md']
write(E/'SOURCE_RECORDS.json',dict(local=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in sources],
 authority_order='Current user withdrawal/replacement instruction supersedes the human-pair continuation instruction; current checkpoint and verified artifacts govern interface facts; older design is context.',
 external=[dict(title='Designing and Interpreting Probes with Control Tasks',authors='John Hewitt; Percy Liang',year=2019,url='https://aclanthology.org/D19-1275/',scope='Methodological rationale for probe controls; NLP evidence, not Loom validation.'),
 dict(title='A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning',authors='Stephane Ross; Geoffrey Gordon; Drew Bagnell',year=2011,url='https://proceedings.mlr.press/v15/ross11a.html',scope='Imitation distribution-shift limitation; no DAgger implementation or additional training rounds proposed.')],
 sealed_state_access='No B1 snapshots, trajectory streams or evaluator state decoded. Prior run manifests were consulted only for completion/counters/file identities during preservation.'))
a2=js(sources[11]);a3=js(sources[12]);a5=js(sources[13])
total=56*30
ratios=dict(A2=a2['recorder_wall_seconds']/a2['simulated_seconds_recorded'],A3=a3['recorder_wall_seconds']/a3['simulated_seconds_recorded'],A5=a5['recorder_wall_seconds']/a5['simulated_seconds'])
per=js(op/'RESOURCE_PROJECTION.json')['cases'][0]['retained_primary_planning_bytes']
write(E/'RESOURCE_ARITHMETIC.json',dict(status='PROPOSAL ONLY / NO EXECUTION BUDGET SET',
 proposed_training_starts=16,proposed_development_starts=4,proposed_held_out_starts=12,
 proposed_primary_test_conditions=2,proposed_sensory_free_control_conditions=1,
 proposed_trajectory_ceiling_seconds=30,proposed_total_trajectories=56,proposed_maximum_simulated_seconds=total,
 proposed_maximum_native_steps=168000,proposed_maximum_command_holds=16800,
 recorded_wall_per_simulated_second=ratios,base_simulation_hours={k:total*v/3600 for k,v in ratios.items()},
 proposed_fitting_wall_ceiling_hours=3,fit_and_inference_throughput_measured=False,
 excluded_costs=['lawful prehistory construction','new model inference and sensory-history overhead','dataset construction and packaging'],
 conservative_existing_human_record_allowance_per_case_bytes=per,
 conservative_primary_case_bytes=56*per,conservative_primary_plus_one_archive_copy_bytes=112*per,
 old_human_batch_storage_cap_bytes=12_000_000_000,old_cap_not_reused_or_raised=True,
 native_fidelity_reduction=False,benchmark_runs=0))
write(E/'VERIFICATION.json',dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 hidden_case_status='AUTHORIZED-BUT-NOT-EXECUTED / WITHDRAWN AT JASON DIRECTION',
 withdrawn_from='prepared',hidden_native_steps=0,hidden_commands=0,hidden_simulated_seconds=0,
 prior_preparation_world_and_wall_timer_preserved_in_audit=True,withdrawn_service_stopped=True,
 full_raw_files_unchanged=True,full_raw_reinterpreted=False,old_operator_packet_unchanged=True,
 current_apparatus_checkpoint='b684912eaf7811cd318ee94c77172aca790f3a0d',current_worktree_clean=True,
 P='6bc9683b54e4fa80136fe8534d7713e2a250a95f',production_code_changes=0,configuration_changes=0,
 new_simulation_steps=0,new_worlds_loaded=0,new_prehistory_generation=0,model_training_runs=0,
 evaluator_state_inspected=False,trajectory_streams_decoded=False,execution_authorities_created=0,
 proposed_numbers_are_unapproved=True,no_new_independent_review_claim=True,
 founder_or_nursery_design_started=False,pushes=0,PRs=0,merges=0,vault_git_writes=0))
files={p.relative_to(E).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(E.rglob('*')) if p.is_file()}
write(E/'FILE_MANIFEST.json',dict(files=files,excludes_self=True,not_an_execution_authority=True))
archive=E.with_suffix('.zip')
assert not archive.exists()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(E))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(files)|{'FILE_MANIFEST.json'}
    for n in z.namelist():assert hashlib.sha256(z.read(n)).hexdigest()==sha(E/n)
    assert not any(s in n.lower() for n in z.namelist() for s in ('snapshot','native.jsonl','sensor.jsonl','controller.jsonl','case-manifests','authority-objects','private/'))
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
write(S/'DELIVERY_RECEIPT.json',dict(package=str(E),archive=str(archive),archive_sha256=sha(archive),
 design_sha256=sha(E/'B1_AUTOMATED_REFERENCE_DESIGN_v0_1.md'),files=len(files)+1,design_only=True,
 hidden_withdrawn_at_zero=True,full_raw_preserved=True,new_execution=0))
print(json.dumps(dict(package=str(E),archive_sha256=sha(archive),base_simulation_hours={k:round(total*v/3600,3) for k,v in ratios.items()},
 design_word_count=len((E/'B1_AUTOMATED_REFERENCE_DESIGN_v0_1.md').read_text(encoding='utf-8').split()),new_execution=0,verification='passed')))
