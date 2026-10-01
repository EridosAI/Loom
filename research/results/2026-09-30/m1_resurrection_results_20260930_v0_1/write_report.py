"""NON-CANONICAL RESURRECTION SANDBOX. Post-stop report from sealed observations."""
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent;PREP=ROOT/'m1_resurrection_sandbox_20260930_v0_1';EX=PREP/'execution'
def main():
    data=json.loads((OUT/'PASSIVE_RESULTS.json').read_bytes());den=data['denominator'];lives=data['lives']
    available=[r for r in lives if 'kinematics' in r];batch=json.loads((PREP/'BATCH_AUTHORITY.json').read_bytes())
    gate=json.loads((EX/'CONTINUATION_GATE.json').read_bytes()) if (EX/'CONTINUATION_GATE.json').exists() else None
    stop=json.loads((EX/'STOP.json').read_bytes()) if (EX/'STOP.json').exists() else None
    if stop is None and (OUT/'HOST_STOP.json').exists():stop=json.loads((OUT/'HOST_STOP.json').read_bytes())
    lines=['# NON-CANONICAL RESURRECTION SANDBOX', '', '# M1 long-development result — v0.1','']
    if stop:
        boundary='Last durable evidence, not the exact crash call' if stop.get('exact_inflight_state_available') is False else 'Stopped boundary'
        lines += [f"**Stopped under the declared rule:** `{stop['reason']}`. Affected individual: {stop['life']}, stage: {stop['stage']}. {boundary}: physical age {stop['age']:.12f} s, native index {stop['native_index']}.",
            '', 'No retry, replacement organism, apparatus patch during execution or continuation after the stop occurred. Later stages remain unstarted at their preserved boundary states; completed pilots remain completed. This is an apparatus-interrupted dataset, not a negative long-development result.','']
        if stop.get('exact_inflight_state_available') is False:
            lines += [f"The native process error bypassed Python's exception/final-checkpoint handler. The last complete causal checkpoint is native {stop['last_full_checkpoint_index']} at age {stop['last_full_checkpoint_age']:.12f} s. Subsequent complete chunks retain physical/native/wave observations through the durable prefix, but no full causal state is available at its endpoint. Any unflushed rows and in-flight call are unavailable. No reconstruction or continuation was performed.",
                '', 'The external host-stop record and denominator are review artifacts, not fabricated executor receipts. The original execution directory is preserved exactly as it stood at the crash.','']
    else:lines += [f"All twelve organisms completed the mechanically selected common age of **{den['common_target']:g} s**. No outcome selected a continuation or changed M1.",'']
    lines += ['Read `FINDINGS.md` for the plain-language developmental assessment, `DEVELOPMENTAL_QUESTIONS.md` for detailed tables, and `HOST_FAILURE_REPORT.md` for the native-crash evidence.','',
        '## Exact identities','',f"- Corrected common checkpoint: `1d7cd6fd450ea528562b2c825589ab4de18a5b38`.",
        '- Preserved motor-screen runtime: `5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49`.',
        f"- Sandbox execution runtime: `{batch['runtime']}`.",
        '- Frozen historical P identity: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; corrected contact apparatus is explicitly additional provenance.',
        '- Twelve new life streams: 1000001–1000012, fixed before any birth preparation. All twelve blank states and authorities were prepared before any pilot execution.',
        '- Exact M1: amplitude 0.35, zero-mean stationary Gaussian common/differential latents with SD 0.5; OU times 16/8 s; unchanged commissioned refresh every 50 accepted native calls. See the launch/runtime records for hashes.',
        '', 'The sandbox is isolated in `m1_resurrection_sandbox_20260930_v0_1`. It imports the corrected physical engine and commissioned M1 unchanged. Canonical P/world source, configuration and historical evidence were not edited. No new Git commit, merge, push or PR was needed for the isolated wrapper; its complete files are bound by the runtime hash.',
        '', '## Complete denominator','', '| Individual | Disposition | Actual age (s) | Resurrections | Path | Max excursion | Source energy | Damage | Repair |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in lives:
        if 'kinematics' not in r:lines.append(f"| {r['life_id']} | {r['status']} | 0 | 0 | — | — | — | — | — |")
        else:
            k=r['kinematics'];p=r['physical'];lines.append(f"| {r['life_id']} | {r['status']} | {r['age']:.6f} | {len(r['resurrections'])} | {k['path']:.4f} | {k['maximum_excursion']:.4f} | {p['source_transfer']:.7g} | {p['damage']:.7g} | {p['repair']:.7g} |")
    lines += ['', 'The denominator includes all prepared starts. Fractional terminal/administrative intervals mean accepted native index is not identical to physical age / 0.01. Every quantitative age above uses the actual stored clock.',
        '', '## Intervention and continuity','',
        'At a genuine terminal boundary the runner wrote a complete pre-intervention checkpoint. It restored only the nonviable reserve (E to 0.70, I to 1.0), with no relocation, time rewind, field regeneration, source refill, replacement birth or RNG draw. A complete post-intervention checkpoint and typed intervention record preserve the support amount and both state hashes.',
        '', 'Only these transients changed: the restored dimension’s regulator body mean and association E/I packet mean were aligned with its new reserve; that E/I packet trace was cleared; unfinished sensory and motor packet integrals were discarded; wave elapsed was reset to zero. Stop metadata and explicit intervention/packet-epoch counters changed. All other causal state was compared bitwise, including learned banks, references, eligibility, H/use, sensory structures, central state, expressed controls, M1 latents/counters, pose/velocity, fields/stocks and RNG.',
        '', 'A fresh 0.2 s packet window begins at the intervention time. There is no handoff or bank/map update at the jump. Copy-only credit probes verified zero trend and learning from each restored dimension. Actual later ordinary expenditure, transfer, damage and repair remain available to credit. The full transient allowlist and discarded interval are retained per intervention.',
        '', 'The incomplete preterminal packet is discarded without a later association/bank handoff. This also discards ordinary experience in that partial packet from that handoff, although every physical observation remains recorded. This is an explicit intervention cost, not loss of accumulated long-term learned state.',
        '', 'Administrative 600-second endpoints can close a fractional native call. Unfinished packet integrals are retained across that administrative pause; the subsequent waveform closes at its existing packet boundary. Absolute physical time and all history/M1 counters continue. This clock adaptation is explicitly sandbox-only.',
        '', '## Engineering verification','',
        '- Two component passes: 379 accepted manufactured integration calls each. The second strengthened preservation checks using nonzero H/use and learned-bank/reference/eligibility state.',
        '- One recorder/continuation component pass: 82 calls, including a genuine fractional energy terminal, before/after checkpoint round trips and exact resumed state.',
        '- Total component work: 840 accepted calls plus transactional terminal-root probes, all on manufactured copies; none were pilot organisms.',
        '- The 100-step unbroken component path matched the corrected common apparatus exactly. Manufactured E-only, I-only and simultaneous restoration passed. False terminal/viable-state restoration failed closed.',
        '- Full runtime preflight passed for all twelve prepared blank states. Closed execution segments received ledger, checkpoint and support-edge verification. Post-stop analysis independently checked every available native row and accounting ledger without simulation.',
        '', '## Resource disposition','', f"Pilot/overnight wall time to stop/completion: {den['active_wall_seconds']:.3f} s. Primary files: {den['primary_bytes']:,} bytes.",
        '', 'The hard envelopes were one worker, 25,200 s active wall and 8,000,000,000 primary bytes. Continuation reserved 20% margin, 600 s additional verification and 32 MB closure. Archive/temporary/analysis headroom was declared before launch; available disk was approximately 599 GB.']
    if gate:lines += ['', f"The complete pilot selected a common total age of {gate['selected_common_total_age']:g} s, using the slowest/largest measured per-life costs. Projected wall: {gate['projected_wall']:.1f} s; projected primary bytes: {gate['projected_primary_bytes']:.0f}. No outcome variables entered."]
    else:lines += ['', 'The twelve-pilot gate was not reached. No overnight age was selected and no overnight continuation occurred.']
    if den.get('active_wall_estimated_from_file_timestamp'):
        lines += ['', 'After the native crash, no final monotonic-clock receipt was possible. The wall value above is estimated from the single-use-start file timestamp to the recorded host-stop action, including the error-dialog wait. Primary bytes were measured from the preserved files, rather than asserted to be the unavailable final in-memory counter. Neither resource ceiling was approached.']
    lines += ['', '## Bounded developmental observations','']
    for r in available:
        p=r['physical'];episodes=p['episodes'];sources=[x for x in episodes if x['collider'].startswith('source-')];productive=[x for x in sources if x['transfer']>0]
        final=next(x for x in r['checkpoint_history'] if x['file'] in ('authoritative-final','last-full-checkpoint-not-endpoint'));k=r['kinematics']
        lines += [f"### {r['life_id']}",'',
            f"At {r['age']:.6f} s: {len(sources)} literal source-contact fragments, {len(productive)} with positive transfer; {p['source_transfer']:.8g} total source energy; {p['expenditure']:.8g} expenditure; {p['damage']:.8g} damage; {p['repair']:.8g} repair. Fragments are not separate navigation successes; grouped bouts are reported in DEVELOPMENTAL_QUESTIONS.md. External support was E={r['support'][0]:.8g}, I={r['support'][1]:.8g}, reported separately.",
            '', f"Occupied centre cells (0.25 units): {k['grids']['0.25']['visited']}; re-entry fraction: {k['grids']['0.25']['reentry_fraction']}. Qualified forward/reverse switches: {k['switches']}. Last complete neural checkpoint at {final['age']:.9f} s: H norm {final['H_norm']:.7g}, q norm {final['q_norm']:.7g}; mean use {final['use']['mean']:.7g}. Regulatory bank norms E/I: {final['bank_norm']}.",
            '', 'The detailed record supplies 60-second kinematic/contact/coupling windows, every contact episode, wave history and periodic/boundary neural-reference snapshots. These describe physical and internal histories without asserting that learned state caused useful behavior.','']
    lines += ['## Developmental interpretation and limits','',
        'See DEVELOPMENTAL_QUESTIONS.md for the question-by-question assessment against the complete available denominator. It separates measured temporal change from causal learning claims.',
        '', 'No counterfactual ablation, alternative motor draw, rescue of an apparatus fault, ordinary-survival comparison, Founder selection, Nursery validation or biological-realism test was performed. Local motor algebra does not establish useful learning. A source return after internal change can be accidental; no A -> B -> C claim of causal dependence follows from temporal order alone.',
        '', '## Files and stop boundary','',
        '- `ALL_TWELVE_DISPOSITIONS.csv`: complete denominator and headline measurements.',
        '- `PASSIVE_RESULTS.json`, individual details and wave histories: full passive summaries.',
        '- `ALL_TWELVE_PATHS.png` and individual history figures: recorded trajectory/reserve/coverage views.',
        '- `EXECUTION_CUSTODY_SEAL.json`, `PASSIVE_VERIFICATION.json`, `FINAL_VERIFICATION.json`: custody and verification.',
        '- `M1_RESURRECTION_SANDBOX_20260930_v0_1.zip`: single evidence/review archive, with complete prepared states, authorities, wrapper, available raw evidence and source/dependency identities.',
        '', 'No canonical acceptance or next experiment follows automatically. Execution has stopped.']
    (OUT/'SANDBOX_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
if __name__=='__main__':main()
