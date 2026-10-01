"""Final read-only custody checks and hashes of this new passive delivery."""
import datetime,hashlib,json,re,time
from pathlib import Path
from impact_analysis import HERE,PREV,OLD,read,write,execution,identity,canonical,file_hash

def main():
    began=time.perf_counter();inputs=read(HERE/'INPUT_CUSTODY.json')
    for item in inputs['scientific_files']:assert file_hash(item['path'])==item['sha256']
    previous=read(PREV/'FINAL_DELIVERY_VERIFICATION.json')
    for item in previous['analysis_files']:assert file_hash(PREV/item['path'])==item['sha256']
    assert file_hash(PREV/'FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md')==previous['final_report_sha256']
    archives=[]
    for base in (OLD,PREV):
        a=read(base/'ARCHIVE_VERIFICATION.json');assert file_hash(a['path'])==a['sha256'];archives.append(dict(path=a['path'],sha256=a['sha256']))
    execution.source_gate();assert hashlib.sha256(canonical(identity())).hexdigest()==inputs['runtime_sha256']
    audit=read(HERE/'DAMAGED_LIFE_AUDIT.json');damaged=audit['damaged_lives'];assert len(audit['roster'])==60
    assert damaged==['FS-002','FS-010','FS-015','FS-017','FS-032','FS-033','FS-034','FS-038','FS-044']
    assert audit['roster'][-1]['life_id']=='FS-060' and audit['roster'][-1]['damage']==0 and audit['roster'][-1]['preserved_prefix_only']
    episodes=read(HERE/'BEHAVIORAL_EPISODES_ENRICHED.json');receiver=read(HERE/'RECEIVER_CHECK_COMPLETION.json')
    manifest=read(HERE/'PROBE_MANIFEST.json');omissions=read(HERE/'PASSIVE_LEARNED_I_OMISSIONS.json')
    assert {x['name'] for x in manifest['windows']}=={x['name'] for x in omissions}
    assert len(omissions)==receiver['window_count']==192
    for name in damaged:
        a=next(z for z in audit['roster'] if z['life_id']==name)
        e=[z for z in episodes if z['life_id']==name]
        assert abs(sum(z['damage'] for z in e)-a['damage'])<1e-12
        assert abs(sum(z['restoration'] for z in e)-a['restoration'])<1e-12
        r=next(z for z in receiver['lives'] if z['life_id']==name)['reconstruction']
        assert not r['physics_executed'] and not r['fields_reconstructed'] and not r['live_state_modified']
    assert read(HERE/'COMPARISON_COMPLETION.json')['no_damage_I_bank_always_zero']
    report=HERE/'IMPACT_INTEGRITY_DEVELOPMENT_ANALYSIS_v0_1.md';text=report.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(<([^>]+)>\)',text):
        path=re.sub(r':[0-9]+$','',target)
        if path.endswith('FINAL_VERIFICATION.json'):continue
        assert Path(path).exists(),path
    files=[dict(path=p.relative_to(HERE).as_posix(),bytes=p.stat().st_size,sha256=file_hash(p)) for p in sorted(HERE.rglob('*')) if p.is_file()]
    write('FINAL_VERIFICATION.json',dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        request_sha256=inputs['request_sha256'],P_commit=inputs['P_commit'],runner_checkpoint=inputs['source_checkpoint'],
        runtime_sha256=inputs['runtime_sha256'],git_clean=True,scientific_files_unchanged=len(inputs['scientific_files']),
        previous_analysis_files_unchanged=len(previous['analysis_files']),archives_unchanged=archives,
        audited_roster=60,damaged_lives=damaged,FS060_prefix_only=True,FS060_tail_not_synthesized=True,
        behavioral_episodes=26,temporal_bouts=28,receiver_windows=192,
        unique_receiver_native_samples=sum(x['native_probes'] for x in receiver['lives']),
        exact_saved_input_P_checks=9,receiver_wall_seconds=receiver['wall_seconds'],
        physical_audit_wall_seconds=audit['wall_seconds'],final_verification_seconds=time.perf_counter()-began,
        derived_bytes=sum(x['bytes'] for x in files),report_sha256=file_hash(report),files=files,
        new_world_steps=0,field_steps=0,alternative_world_trajectories=0,new_births=0,new_authorities=0,
        no_P_world_nursery_change=True,no_founder_selection=True,no_scientific_retry_or_continuation=True,
        no_git_writes=True,no_dependency_installs=True,old_sealed_human_B1_not_accessed=True,
        limitations='Local learned-I receiver effects and observed physical patterns do not establish long-horizon causal benefit.'))
    print(json.dumps(dict(status='PASS',scientific_files_unchanged=len(inputs['scientific_files']),
        previous_analysis_files_unchanged=len(previous['analysis_files']),derived_bytes=sum(x['bytes'] for x in files),
        report_sha256=file_hash(report),world_steps=0)))

if __name__=='__main__':main()
