"""Report only sealed, verified saved evidence after bounded passive analysis."""
import csv,json,time,math
from pathlib import Path
from passive_ab import guard
from loom_developmental.runner import atomic_json,file_hash

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OUT=HERE/'analysis'
def read(p):return json.loads(p.read_bytes())
def link(label,p):return f'[{label}](<{p.resolve().as_posix()}>)'
def number(x):return 'unavailable' if x is None else f'{x:.9g}'

def main():
    guard();rows=read(OUT/'ALL_SIXTY_AB.json');seal=read(HERE/'DENOMINATOR_SEALED.json')
    verification=read(HERE/'POSTRUN_VERIFICATION.json');archive=read(HERE/'ARCHIVE_VERIFICATION.json')
    c=read(OUT/'C_WINDOWS_COMPLETE.json') if (OUT/'C_WINDOWS_COMPLETE.json').exists() else {'windows':[],'pending':[]}
    reconstructed=[]
    for mode in ('consequential','remaining','all'):
        p=OUT/f'B_RECONSTRUCTION_{mode}_COMPLETION.json'
        if p.exists():reconstructed.extend(read(p)['results'])
    complete=[r for r in rows if r.get('complete')]
    full=[r for r in complete if r['state'] in ('terminal','stage_complete')]
    contacts=[r for r in rows if r.get('source_ids_contacted')]
    productive=[r for r in rows if r.get('transfer_total',0)>0]
    consequential=[r for r in rows if int(r['life_id'][3:])>=13 and any(r.get(k,0)>0 for k in ('transfer_total','repair','damage'))]
    states={k:sum(r['state']==k for r in rows) for k in sorted({r['state'] for r in rows})}
    text=['# Founder Search — fixed 60-life report','',
        f"The expansion executed {sum(r['state']!='NOT_STARTED' for r in seal['roster'])}/48 prepared lives once. The fixed denominator combines FS-001–FS-012, preserved unchanged, with FS-013–FS-060. No founder selection was performed.",
        '',f"Observed source contact: **{len(contacts)}/60** roster members. Actual positive source energy transfer: **{len(productive)}/60**. Fully observed biological/600-second endpoints: **{len(full)}/60**. Completed evidence stores (including administrative cutoffs): **{len(complete)}/60**.",
        '',f"Stop categories: `{json.dumps(states,sort_keys=True)}`. Expansion shared-stop condition: `{seal['batch_stop']}`.",
        '', '## Authority, custody and execution', '',
        'Frozen P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Lean runner: `87abae34e19d4e46234402a6b1ba776814956ec1`. Exact FS-013–FS-060 order, one worker, saved blank starts only, native 0.01 s and wave 0.2 s unchanged. Each ceiling was 600 simulated seconds, 900 active wall seconds and 83,333,333 primary bytes; common limits were 43,200 active wall seconds and 4,000,000,000 primary bytes. No allowance redistribution or simulated-age extension.',
        '',f"Recorded active execution wall-time lower bound is {seal['active_execution_wall_seconds']:.6f} active wall seconds; closed life records (excluding the unclosed prefix) total {seal['closed_life_bytes']:,} bytes. All-48 preflight and per-case rechecks used {seal['preflight_wall_seconds']:.6f} seconds. Passive store verification: {verification['all_available_complete_stores_verified']}; {verification['wall_seconds']:.6f} seconds.",
        '',f"Single expansion archive: {link('download/archive',Path(archive['path']))}; {archive['bytes']:,} bytes; SHA256 `{archive['sha256']}`. It references the preserved original archive SHA256 `e3377cb965f6801b2e9a53831af6afddffe9814eea7ba78cb1ba71da9fcfbb29` rather than duplicating its records. Derived analyses are separate and linked to this archive.",
        '', '## A — complete opportunity and physical denominator','',
        '| Life | Stop | Age / last durable time (s) | Source contacts (IDs) | Actual intake | Damage | Repair | Last recorded E | Last recorded I | Path length | Closest sampled source gap |',
        '|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        text.append(f"| {r['life_id']} | {r['state']} | {number(r.get('simulated_seconds'))} | {r.get('source_ids_contacted','unavailable')} | {number(r.get('transfer_total'))} | {number(r.get('damage'))} | {number(r.get('repair'))} | {number(r.get('energy_final'))} | {number(r.get('integrity_final'))} | {number(r.get('path_length'))} | {number(min(r['min_source_endpoint_gap']) if 'min_source_endpoint_gap' in r else None)} |")
    if seal.get('interruption_custody_sha256'):
        text += ['', '**FS-060 is administratively incomplete, not biologically terminal.** The worker disappeared with tool exit code 1 and no runner closure/failure receipt. Its saved prefix reaches native 12,400 (124.00000000002653 s), with 620 waves; its last complete physical/P checkpoint is native 12,000. The exact unflushed tail and final in-memory state are unknown. No retry, continuation or tail synthesis occurred. Root cause remains unresolved. Its A data describe the retained prefix only; its final B checkpoint columns describe native 12,000, not an invented final state. The fixed denominator remains 60, with 59 fully observed endpoints.']
    text += ['', 'Native path/orientation, mover pose, raw sensory input, commands, E/I, stocks and all physical events remain in the sealed records. The per-life A/B JSON, contact-episode CSV and near-source interval CSV retain exact native/event identifiers, impulses, repeated interactions, path extent and 1-world-unit coverage bins. Display paths are decimated only for display; source evidence is unchanged.',
        '', 'Contact subdivisions and zero-duration solver touches are not independent behavioral experiences. Contact is distinct from transfer, and sampled endpoint clearance is distinct from exact collision-event time. Repair-surface contact and actual positive repair are separate.',
        '', f"Lives exceeding 429.2193066502889 s: {sum(bool(r.get('beyond_initial_min_death_age')) for r in rows)}; exceeding 429.94828824435905 s: {sum(bool(r.get('beyond_initial_max_death_age')) for r in rows)}. These are descriptive first-cohort markers, not survival gates. The per-life report includes physical E at each reached marker and actual intake; varying expenditure alone can alter age.",
        '', '## B — internal change, contraction and later expression', '',
        'Every recorded actual wave is represented chronologically in the per-life wave tables. Raw-coordinate activity, structural shared/fine norms, opening, support, H norms/use, associative returns, E/I credit, regulator banks, learned output and exploration are kept separate. Complete saved checkpoints retain all physical and neural state.',
        '',f"Detached exact saved-input P reconstruction completed for {sum(r['status']=='PASS' for r in reconstructed)} lives. Other reconstruction statuses: `{json.dumps({k:sum(r['status']==k for r in reconstructed) for k in sorted({r['status'] for r in reconstructed})})}`. Reconstruction checks command equality, actual wave output, dynamic RNG and crossed closed-chunk P/RNG endpoints. It never evolves the world or fields. Incomplete intervals remain pending with their original evidence preserved.",
        '', '| Life | H norm | H use mean | q norm | E bank norm | I bank norm | E reference norm | I reference norm |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        b=r.get('B_final',{});text.append('| '+r['life_id']+' | '+' | '.join(number(b.get(k)) for k in ('H_norm','H_use_mean','q_norm','theta_E_norm','theta_I_norm','reference_E_norm','reference_I_norm'))+' |')
    text += ['', '| Modality | Final fine-norm range | Shared birth-change range | Fine-reference birth-change range |', '|---|---:|---:|---:|']
    for m,label in enumerate(('light','chemistry','contact','proprioception')):
        spans=[]
        for key in ('fine_norm','shared_birth_delta','fine_ref_birth_delta'):
            values=[r['B_final'][f'c{m}_{key}'] for r in complete]
            spans.append(f'{min(values):.9g}–{max(values):.9g}' if values else 'unavailable')
        text.append('| '+label+' | '+' | '.join(spans)+' |')
    text += ['', 'Fine contraction under the configured springs and timed pool opening do not establish useful learning. Structural change, reference movement, H writes, subsequent read/use, actual downstream expression and improved physical consequence are different claims. Gross intake is not identical to positive net E-credit: each consequential event is aligned with its prior and next actual handoff, retaining event E/I before/after and expenditure.', '', '## C — each consequential expansion life', '']
    if not consequential:text.append('No expansion life has recorded positive source transfer, positive repair or nonzero contact damage. No consequential life is omitted by a magnitude threshold.')
    for r in consequential:
        name=r['life_id'];rc=next((v for v in reconstructed if v['life_id']==name),None)
        ws=[w for w in c['windows'] if w['life_id']==name and not w['kind'].startswith('comparison')]
        text += [f'### {name}', '',
            f"A: contact source IDs {r['source_ids_contacted']}; {r['source_contact_episodes']} recorded source-contact episodes, {r['productive_source_episodes']} productive episodes; intake {r['transfer_total']:.12g}; damage {r['damage']:.12g}; repair {r['repair']:.12g}; first consequential native {r['first_consequential_native']}; final age {r['simulated_seconds']:.12g} s. All {r['consequential_event_count']} consequential event records are retained.",
            '', f"B: exact wave reconstruction status {rc['status'] if rc else 'pending'}; inspect {link('event / credit alignment',OUT/r['consequential_events_file'])} and the per-life exact-wave reconstruction record for operands and verified coverage.",
            '',f"C: {len(ws)} completed deterministic receiver windows. These establish only the recorded local influences shown below; no learned-vs-unlearned ecological counterfactual was run. Productive contact may be accidental, and an expressed bank change does not establish benefit.", '']
    text += ['| Window | Life | Native interval | Largest learned-E controls omission difference | Largest learned-I controls omission difference | Largest motor-evocation command omission difference |', '|---|---|---|---:|---:|---:|']
    for w in c['windows']:
        def biggest(section,key):return max((x.get(section,{}).get(key,0.) for x in w['native_samples']),default=0.)
        text.append(f"| {w['name']} | {w['life_id']} | {w['first_index']}–{w['last_index']} | {biggest('immediate_controls_omission_delta_norm','learned_0'):.9g} | {biggest('immediate_controls_omission_delta_norm','learned_1'):.9g} | {biggest('immediate_command_omission_delta_norm','motor_evocation'):.9g} |")
    text += ['',f"Deep windows completed: {len(c['windows'])}; pending after the shared analysis allowance/reserve: {len(c.get('pending',[]))}. The selection manifest records unavailable or duplicate anchors. Original FS-001–FS-012 deep windows were reused as historical evidence and not rerun.",
        '', 'No-contact comparison windows use the earliest eligible expansion roster member at corresponding ages. They are descriptive comparisons, confounded by sensory exposure, pose, body needs and geometry. Consider source stock, direct feedback, oscillator/noise, exploration, contact and injury alongside history-dependent regulation.',
        '', '## Bounded interpretation and remaining uncertainty', '']
    if not contacts and len(full)==60:
        text.append(f"Zero source contacts were observed across all 60 fully observed valid lives. Under independent ordinary-birth draws with a common fixed contact probability, the one-sided 95% upper bound is $1-0.05^{{1/60}}={1-0.05**(1/60):.6f}$, about 5% per permitted life. Opportunity sparsity is therefore a serious candidate bottleneck for this exact configuration and horizon. This does not prove absent sensory information, general incapacity to learn, or justify a nursery automatically.")
    elif contacts:
        text.append(f"Source contact occurred in {len(contacts)} roster members and positive transfer in {len(productive)}. The zero-of-60 upper-bound claim does not apply. These encounters distinguish physical opportunity from its later retention/use; their occurrence alone does not demonstrate beneficial developmental learning or justify founder selection.")
    else:text.append('The roster includes censored, incomplete or unstarted cases; a zero-of-60 fully observed bound is not applicable. Preserve the fixed administrative denominator separately from the valid observed endpoints.')
    text += ['', 'Jason accepted that the original twelve misses alone did not establish an overly sparse ecology. The present observations, the accepted expansion decision and any analyst inference remain separate. No structural norm, age marker or accidental benefit is treated as a founder score.',
        '', '## Not performed', '',
        'No retries, rewind, replacement births, new prehistory, continuation, parameter adjustment, P/world or source changes, live Tier-2/D5 work, founder scoring/selection, nursery, new population, or 900/1,800-second preparation/execution. No old sealed human B1 evaluator state was accessed. No alternative world trajectory or causal beneficial-learning test was run. Pending reconstructed intervals and receiver windows are explicitly listed, not silently counted as analyzed.',
        '', '## Review files', '',
        '- '+link('combined sealed roster',HERE/'COMBINED_DENOMINATOR_SEALED.json'),
        '- '+link('complete A table',OUT/'FULL_DENOMINATOR_A.csv'),
        '- '+link('complete A/B structured results',OUT/'ALL_SIXTY_AB.json'),
        '- '+link('passive window selection',OUT/'C_WINDOW_SELECTION.json'),
        '- '+link('archive verification',HERE/'ARCHIVE_VERIFICATION.json'),
        '', 'Stop boundary: Jason reviews this fixed 60-life evidence before any selection or further work.']
    report=HERE/'FOUNDER_SEARCH_60_LIFE_REPORT.md';report.write_text('\n'.join(text)+'\n',encoding='utf-8')
    guard()
    atomic_json(OUT/'PASSIVE_ANALYSIS_COMPLETION.json',dict(report_sha256=file_hash(report),
        total_wall_elapsed=time.perf_counter()-read(OUT/'ANALYSIS_CLOCK.json')['monotonic_started'],
        complete_roster=60,deep_windows=len(c['windows']),pending_deep_windows=len(c.get('pending',[])),
        completed_exact_reconstructed_lives=sum(r['status']=='PASS' for r in reconstructed),
        new_ecological_steps=0,selection_scores=0,source_contact_lives=len(contacts),productive_lives=len(productive),
        fully_observed_lives=len(full),administrative_denominator=60))
    print(json.dumps(dict(report=str(report),contacts=len(contacts),productive=len(productive),fully_observed=len(full))),flush=True)
if __name__=='__main__':main()
