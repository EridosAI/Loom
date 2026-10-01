"""Final review packaging within the original post-run analysis allowance."""
import csv,hashlib,json,time
from pathlib import Path
import execute_authorized_expansion as x
from loom_developmental import codec
from loom_developmental.runner import file_hash,atomic_json,canonical,identity

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OUT=HERE/'analysis'
def read(p):return json.loads(p.read_bytes())
def main():
    clock=read(OUT/'ANALYSIS_CLOCK.json');stream=read(OUT/'STREAM_B_COMPLETION.json')
    assert time.perf_counter()-clock['monotonic_started']<4480
    rows=read(OUT/'ALL_SIXTY_AB.json');selection=read(OUT/'C_WINDOW_SELECTION.json');cache={}
    def actual_wave(name,index):
        if name not in cache:
            with (OUT/(name+'_waves.csv')).open(encoding='utf-8') as f:
                cache[name]={int(r['native_index']):r for r in csv.DictReader(f)}
        return cache[name][index]
    fields=['credit_E','credit_I','theta_E_norm','theta_I_norm','H_norm','H_use_mean','q_norm',
        'opening_mean','support_mean','learned_E_norm','learned_I_norm','exploration_E_norm','exploration_I_norm']
    fields += [f'c{m}_{part}_norm' for m in range(4) for part in ('shared','fine')]
    paired=[]
    for window in selection['windows']:
        if window['kind'].startswith('comparison'):continue
        index=window['last_index'];case=window['life_id']
        candidates=[r for r in rows if r.get('complete') and r.get('contact_native_count')==0 and r.get('transfer_total')==0 and r['waves']*20>=index]
        if not candidates:continue
        comparison=candidates[0]['life_id'];a=actual_wave(case,index);b=actual_wave(comparison,index)
        entry=dict(window=window['name'],life_id=case,comparison_life=comparison,native_index=index,
            age_label_seconds=index*.01,selection='earliest complete no-contact roster life at same recorded wave index',
            causal_isolation=False,new_deep_window=False)
        for key in fields:
            entry['case_'+key]=float(a[key]);entry['comparison_'+key]=float(b[key]);entry['difference_'+key]=float(a[key])-float(b[key])
        paired.append(entry)
    with (OUT/'MATCHED_AGE_COMPARISONS.csv').open('x',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(paired[0]));w.writeheader();w.writerows(paired)
    atomic_json(OUT/'MATCHED_AGE_COMPARISONS.json',dict(rows=paired,
        limitations='Observed histories differ in raw exposure, pose, E/I, geometry and prior contact. Age matching is descriptive, not a learned/unlearned counterfactual.',
        new_physical_steps=0,new_deep_windows=0))
    array_count=len(stream['previous_full_array_passes']);stream_count=sum(r['status']=='PASS' for r in stream['results'])
    pending=[r for r in stream['results'] if r['status'] not in ('PASS','UNSEALED_PREFIX_ONLY')]
    original=(HERE/'FOUNDER_SEARCH_60_LIFE_REPORT.md').read_text(encoding='utf-8');lines=[]
    for line in original.splitlines():
        if line.startswith('The expansion executed 48/48 prepared lives once.'):
            line=('All 48 prepared expansion lives were started once, in order: FS-013–FS-059 have complete runner receipts; FS-060 has an interrupted, unclosed prefix. '
                'The fixed denominator combines FS-001–FS-012, preserved unchanged, with FS-013–FS-060. No founder selection was performed.')
        if line.startswith('Detached exact saved-input P reconstruction completed for'):
            line=(f'Exact saved-input P checks completed for {array_count+stream_count} complete lives: {array_count} with retained full per-wave operand arrays (including all consequential expansion lives), and {stream_count} with compact chronological float64 summaries and hashes of the exact full-vector payloads. '
                'Every completed check compares recorded commands, actual wave outputs, dynamic RNG and crossed closed-chunk P/RNG hashes. Original lossless inputs/checkpoints remain unchanged and regenerate the full vectors; compact output avoids duplicating them. '
                f'Pending complete-life checks: {len(pending)}. FS-060 remains an unclosed prefix, not a reconstructed final life. No world or field evolution was performed.')
        lines.append(line)
    intro=f'''# Final bounded review — 60-life roster

**Execution boundary:** FS-013–FS-059 completed once. FS-060 started once and was interrupted by unexplained worker termination. The fixed roster contains 59 complete energy-nonviable endpoints plus one incomplete prefix; no retry or continuation occurred.

**Observed source experience:** FS-034 alone contacted a source and received 0.0017489243594212861 energy units. Its 96 positive-transfer entries occurred within 103 contact episodes totalling 0.6917392033767031 s; the eight corresponding next E-credit handoffs all stayed negative. The zero-of-60 contact bound is inapplicable. Useful developmental learning was not established. No founder was selected.

**Analysis coverage:** All 60 entries have saved-record A/B coverage, with the incomplete prefix labelled. All 32 selected C windows completed. {array_count+stream_count}/59 complete lives passed full saved-input P checks. Output representation differs between full-array and compact records only; scientific evidence and P/world laws are unchanged. All work uses the original 4,500-second / 2.5-GB analysis envelope.

Read [the source-encounter account](<{(OUT/'FS034_INTERPRETATION.md').resolve().as_posix()}>) for the physical event, credit, persistence/use and local receiver evidence. [Matched-age comparisons](<{(OUT/'MATCHED_AGE_COMPARISONS.csv').resolve().as_posix()}>) cover the named consequential windows without introducing new deep windows. They are explicitly confounded observational comparisons. [Interruption details](<{(HERE/'INTERRUPTION_NOTE.md').resolve().as_posix()}>) preserve FS-060's unknown tail and unresolved termination cause.

The earlier generated report is preserved as an intermediate record; this final version updates its analysis-coverage statement. The scientific archive is unchanged.

Final checks and coverage: [delivery verification](<{(HERE/'FINAL_DELIVERY_VERIFICATION.json').resolve().as_posix()}>), [remaining saved-input checks](<{(OUT/'STREAM_B_COMPLETION.json').resolve().as_posix()}>). Exact resource use and derived-file hashes are in the delivery verification. All 59 complete lives ended through energy nonviability between 428.8747258878284 and 430.84316626881713 simulated seconds; none reached the 600-second ceiling.

'''
    final=HERE/'FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md'
    with final.open('x',encoding='utf-8') as f:f.write(intro+'\n'.join(lines)+'\n')
    x.source_gate();assert hashlib.sha256(canonical(identity())).hexdigest()==x.RUNTIME
    assert file_hash(HERE/'execute_authorized_expansion.py')=='43f62fd8b257eec78649c0b13a46b058fde299f3ba9c8f7a87a1a3550d1a9752'
    checked={}
    for base in (ROOT/'founder_initial_execution_20260930',HERE):
        manifest=read(base/'EVIDENCE_ARCHIVE_MANIFEST.json');count=0
        for item in manifest['files']:
            if item['path'].startswith(('execution/lives/','execution/shared-assets/')):
                assert file_hash(base/item['path'][len('execution/'):])==item['sha256'];count+=1
        checked[base.name]=count
    for i in range(13,61):
        store=HERE/'lives'/f'FS-{i:03d}'
        assert len(list(store.glob('attempt-*.json')))==1 and not (store/'segment-001.json').exists()
    files=[dict(path=p.relative_to(HERE).as_posix(),bytes=p.stat().st_size,sha256=file_hash(p)) for p in sorted(OUT.rglob('*')) if p.is_file()]
    size=sum(r['bytes'] for r in files);elapsed=time.perf_counter()-clock['monotonic_started']
    assert size<2_500_000_000 and elapsed<4500
    atomic_json(HERE/'FINAL_DELIVERY_VERIFICATION.json',dict(status='CUSTODY_VERIFIED_WITH_INCOMPLETE_FS060',
        final_report_sha256=file_hash(final),archive=read(HERE/'ARCHIVE_VERIFICATION.json'),
        unchanged_scientific_files_checked=checked,checkpoint=x.CHECKPOINT,P_commit=x.P,runtime_sha256=x.RUNTIME,git_clean=True,
        complete_expansion_lives=47,interrupted_expansion_lives=1,total_roster=60,complete_biological_endpoints=59,
        complete_exact_P_checks=array_count+stream_count,retained_full_operand_lives=array_count,compact_operand_lives=stream_count,
        pending=pending,deep_windows=32,derived_bytes=size,analysis_wall_seconds=elapsed,
        analysis_implementation_sha256=file_hash(__file__),analysis_files=files,
        no_world_steps_after_worker_termination=True,no_retry=True,no_continuation=True,no_founder_selection=True,
        no_new_authorities=True,no_P_world_changes=True,no_git_writes=True,old_sealed_human_B1_not_accessed=True))
    print(json.dumps(dict(final_report=str(final),complete_P_checks=array_count+stream_count,derived_bytes=size,analysis_wall_seconds=elapsed)),flush=True)

if __name__=='__main__':main()
