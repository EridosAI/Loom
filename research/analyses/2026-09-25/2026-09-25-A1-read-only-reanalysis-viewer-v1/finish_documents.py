from evidence import *
import html
js=ROOT/'viewer.js';js.write_text(js.read_text(encoding='utf-8').replace("g.fillText('s',w-right,h-8);","g.fillText('time / s',w-right,10);"),encoding='utf-8')
js.write_text(js.read_text(encoding='utf-8').replace("a.net_energy_sign==='negative_resolved'&&a.source_0_positive_duration_contact?", "a.net_energy_sign==='negative_resolved'?").replace("a.source_0_positive_duration_contact&&a.net_energy_sign==='negative_resolved'?'negative-net contact'", "a.net_energy_sign==='negative_resolved'?(a.source_0_positive_duration_contact?'negative-net contact':'negative-net · no source contact')"),encoding='utf-8')
for filename in ('write_v3_report.py','V3_READ_ONLY_REANALYSIS_REPORT.md'):
    p=ROOT/filename;p.write_text(p.read_text(encoding='utf-8').replace('design draft §6 (29','design draft §5.1 (29'),encoding='utf-8')
dataflow='''# Passive A1 viewer — exact data flow

This is derived analysis and visualization of the immutable first-A1 archive, SHA-256 `f37dfec92288fbe8a650b00eed611d086a3ece3b280292e95b891e371cc0d37f`. No live Engine, controller calculation, simulation RNG, physical replay or trajectory write exists in this viewer. The historical archive is the trajectory authority.

`evidence.py` verifies both archive manifests, reads JSON/gzip, and decodes tagged numeric snapshot values into Python built-ins without instantiating any saved class. `build_viewer_data.py` extracts display records and sums saved ledger operands into `viewer_data.js`. `index.html`, `styles.css` and `viewer.js` draw those records. No network fetch, external library, analytics, local storage, upload, simulation module or writable controller interface is present in the page. Its content-security policy denies network connections.

| Display | Exact source | Mapping / arithmetic |
|---|---|---|
| Arena walls and dimensions | Initial snapshot Config; controller initial geometry; configuration.json | Four arena boundaries; world_side=20. No invented interior obstacles. |
| Eight sources | Config source_positions/source_radius, confirmed by initial controller geometry | Actual centre coordinates and radius=0.5; S0 distinguished as the declared target. Stock never changes displayed radius. |
| Restorative wall regions | Config repair_rectangles and recorded initial controller rectangles | Exact three axis-aligned finite rectangles, including their 0.25-unit protrusions. |
| Mover | Every controller.jsonl.gz inputs.geometry mover rectangle and velocity | 919 actual samples at 0.1 s decision cadence. Latest sample at or before selected time is held visually; its sample time and age are always shown. No mover-law evaluation or interpolation. Rectangles are axis-aligned in the reviewed geometry; no orientation angle is invented. |
| Body pose and radius | Initial snapshot Body and Config.body_radius; native.jsonl.gz position/angle | Radius=0.5. Step endpoints remain discrete. Heading line is a drawing of recorded angle. Path joins actual recorded positions. |
| Exact event pose | events.jsonl.gz body_position/body_angle | Event selection uses that event's exact timestamp and position, including the sub-step first impact. Velocity/actuator/sensor values retain their latest native sample and explicit timestamp. |
| E / I / source-0 stock | Initial snapshot; native reserves/stocks; selected event energy_after/integrity_after/stock_after | Physical endpoint values; these are distinct from held sensor-interface E/I. |
| Intake, expenditure, net E | events transfer and expenditure; native endpoint reserves | Every event is assigned to its containing native endpoint using recorded end times and the unchanged event_time_tol. Each native ΔE is checked against its event sums. Cumulative plots sum recorded transfers/costs. No accounting law is rerun. |
| Commands | controller command, time and native_index; native commands | Decision j owns the following ten native steps, truncated by the saved administrative pause. The latest issued decision and the owner of the selected completed step are labelled separately at decision boundaries. No command function is called. |
| Realized actuators | native forces | Recorded physical L/R actuator forces, distinct from dimensionless paired commands. Exact-event view labels their native sample time. No force is inferred from commands. |
| Sustained contact force | events contacts[*].force for positive-duration events | Sum of recorded contact forces for that event; no force is manufactured for a zero-duration impulse. Traces use original event timestamps. Peak=0.27074663791428305 at 6.4 s. |
| Impact / integrity / restoration | events impact, impulse, damage, repair, integrity_before/after, event_kind | All impact and nonzero integrity-debit/restoration events and explicit contact boundaries get markers. All 9,185 events remain addressable, including free/transfer/debit-credit events. None are inferred from centre proximity. |
| Contact state | events certified contacts, source=0 / collider=source-0 | Event view uses the selected record; native view uses the final event in that native step. First contact is 6.31019048650431 s. |
| Fixed energy windows | Original read-only-review/A1_OBSERVATIONS.json all_fixed_windows | Preserve all 459 complete windows and one partial tail. Blue + is resolved positive-net contact; orange − is resolved negative-net contact; gray is other/unresolved/no-contact; hatched purple is partial. Negative is not failure. Last partial interval is an administrative-pause tail, not a bodily terminal event. |
| First positive-window jump | Original A1_RESULT_SUMMARY.json first_positive_net_contact_window | Select native 640, endpoint 6.4 s, and retain the original 6.2–6.4 s convention. The window begins before first contact; neither timestamp is changed. |
| Raw sensors | Sensor stream's explicitly validated initial envelope and mapped endpoint rows | 29 named observer coordinates. E/I use their held sample timestamp. Exact events do not invent intermediate sensor samples. |
| Accounting panel | Original per-event stock_before/after, both renewals, E before/after, expenditure, transfer | Debit=old stock+renewals−new stock; credit=ΔE+cost; residual=credit−all-source transfer. Native view sums its original event operands; event view shows one event. |
| Inactive neural state | V3 report / checkpoint identity only | No learning or developmental graphics; zero neural wave rows. |

## Playback and display semantics

The native scrubber has 9,184 positions including the initial state, from t=0 to t=91.83000000001007. Play/pause changes only which saved record is selected; elapsed screen time chooses an existing native index. No physical state interpolation occurs. Lines between trace/path samples are graphical connections, not additional samples. Exact-event jumps may lie between native endpoints and visibly state the distinct timestamps. The stop button uses the actual final record, not a synthesized 120-second endpoint.

Browser playback rates are 0.1×, 0.5×, 1×, 5× and 20×. Rendering may skip visible intermediate frames at high speed, but native stepping/scrubbing can inspect every recorded native endpoint. Source contact, peak force and integrity events remain individually selectable.

## Opening and safety boundary

Double-click `OPEN_A1_VIEWER.cmd` after extracting the derived package. It runs the minimal standard-library `serve_readonly.py` and opens an automatically allocated loopback HTTP address. It uses the already available pinned Python on Jason's machine, or the standard `py -3` launcher elsewhere. No packages are installed. Close the small launch window when finished; the preview also stops after 30 minutes. Reopen the launcher if the browser needs a reload afterward.

The optional server binds only 127.0.0.1, serves a six-name allowlist and rejects writes. It never exposes the source archive, filesystem listings, arbitrary paths, execution endpoints or trajectory storage. The page needs no API after loading. Direct file URLs were blocked by the in-app browser's policy, so automated file-mode launch was not claimed; the verified HTTP route is the supported launcher route.

For a manually managed local preview: `python -B serve_readonly.py --port 0 --open`. To inspect only static validation, open `STATIC_VIEWER_VALIDATION.html` normally or read its screenshots directly. The user-visible launcher opens only the passive viewer. It contains no Run, restart, prehistory, controller or native-step call.

## Scientific interpretation boundary

The force target is the recorded/configured 0.1; the stress reference is the existing 0.25 threshold. The display does not classify their difference as a defect or tune a gain. Impact and sustained-contact integrity debit totals are sums of the corresponding original ledger categories. They expose accounting evidence rather than automatically assigning a causal narrative. The cumulative energy plot and all positive/negative windows are retained together; no window selects a route or a new trial.
'''
(ROOT/'VIEWER_DATA_FLOW.md').write_text(dataflow.replace('orange − is resolved negative-net contact; gray is other/unresolved/no-contact','orange − is resolved negative-net (including approach without source contact); gray is other/unresolved'),encoding='utf-8')
states=json.loads((ROOT/'screenshots/browser-states.json').read_bytes())[-4:]
sections=[]
for s in states:
    rows=''.join(f'<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>' for k,v in s['values'])
    sections.append(f'<section><h2>{html.escape(s["name"])} · {html.escape(s["clock"])}</h2><p>{html.escape(s["sample"])}</p><img src="screenshots/{s["name"]}-screen.png" alt="Browser screenshot at {html.escape(s["clock"])}"><table>{rows}</table></section>')
(ROOT/'STATIC_VIEWER_VALIDATION.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>A1 viewer — four recorded states</title><style>body{font:16px Segoe UI,Arial;background:#f4f6f5;color:#163746;max-width:1100px;margin:30px auto;padding:20px}section{background:white;padding:24px;margin:24px 0;border:1px solid #d8e1e3;border-radius:8px}img{width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;border-bottom:1px solid #ddd;padding:8px}h1{font-weight:600}</style><h1>Four views of the same recorded A1</h1><p>Static browser validation, not a new simulation. Exact browser-observed timestamps and displayed values accompany each screenshot. Original A1 evidence remains canonical. V3 reanalysis: completed.</p>'+''.join(sections)+'<section><h2>Force / integrity detail at the recorded force peak</h2><img src="screenshots/05-force-integrity-detail.png" alt="Recorded force and integrity around first impact"><p>Peak sustained force occurs at 6.4 s; the first certified impact is at 6.31019048650431 s. The display preserves that distinction.</p></section></html>',encoding='utf-8')
(ROOT/'README.md').write_text('''# First A1 — derived V3 analysis and passive viewer

V3 COMPLETED — checks support the reviewed boundary claim. This reanalyses the original 91.83-second A1; it does not replace its canonical evidence package or run another trajectory.

1. Extract this derived package into a folder.
2. Double-click **OPEN_A1_VIEWER.cmd**. A local browser viewer opens. Close the small launch window when finished; the preview also stops after 30 minutes.
3. Read **V3_READ_ONLY_REANALYSIS_REPORT.md**, **V3_RESULT_v1_1.json**, **VIEWER_DATA_FLOW.md**, and **VIEWER_VERIFICATION.md**.
4. **STATIC_VIEWER_VALIDATION.html** and **screenshots/** show the four requested recorded states and force/integrity detail.

Python 3 is used only for the read-only server and analysis; the existing pinned interpreter is selected on Jason's machine, with `py -3` as the portable fallback. No package installation is needed. No simulation/Engine module is imported. The viewer has no live control interface.

The exact historical **FIRST_A1_COMMISSIONING_RESULT.zip** is preserved under **references/**. The original failed V3 checker and all its error/limitation artifacts remain inside that archive, byte-identical. New versioned analysis files live only in this derived folder. **HASH_BEFORE.json**, **HASH_AFTER.json** and **CUSTODY_PROOF.json** document custody; **FILE_MANIFEST.json** identifies the derived payloads.

Mover pose is shown from actual 0.1-second controller-geometry samples, with sample age. Exact sub-step events retain their own pose/reserves; other channels keep labelled native sample times. There is no display interpolation, physical replay, continuation, new controller calculation, RNG consumption, tuning, efficacy claim or new commissioning result.
''',encoding='utf-8')
print('Derived documentation and static validation written.')
