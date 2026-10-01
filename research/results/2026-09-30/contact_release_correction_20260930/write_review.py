"""Review documents and scalar gap figure. No new physical or neural advance."""
from pathlib import Path
import json,math,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;PACKET=ROOT/'motor_commissioning_preparation_20260930_v0_2'
def read(p):return json.loads(p.read_bytes())
g=read(HERE/'GEOMETRY_AUDIT.json');r=read(HERE/'HISTORICAL_REGRESSION.json');step=read(HERE/'CORRECTED_STEP_1026.json')
input=read(HERE/'EXACT_PHYSICAL_INPUT.json');matrix=read(PACKET/'MATRIX.json')['cases'];pre=read(PACKET/'PREPARATION_BOUNDARY.json')
runtime=read(PACKET/'STATIC_PREFLIGHT_REPORT.json')['runtime_sha256'];commit=pre['corrected_apparatus_checkpoint']
c=input['c'];b=input['body'];phase=input['phase'];t=input['t'];u=input['command'];h=step['events'][0]['duration']
def point(start,s,constrained=False):
    decay=math.exp(-c['linear_drag']*s/c['body_mass'])
    forces=[.5*(.2+.8*start['energy'])*v*w for v,w in zip([.4+.6*start['integrity'],.7+.3*start['integrity']],u)]
    directions=[math.cos(start['angle']),math.sin(start['angle'])]
    velocity=[v*decay+sum(forces)*d/c['linear_drag']*(1-decay) for v,d in zip(start['velocity'],directions)]
    if constrained:velocity[1]=0.
    return [p+s*v for p,v in zip(start['position'],velocity)],velocity
pos,v=point(b,h,True);e=step['events'][0]
corner=dict(b,position=pos,velocity=v,angle=e['body_angle'],energy=e['energy_after'],integrity=e['integrity_after'])
def gap(pos,s):
    edge=c['mover_centre'][0]+c['mover_amplitude']*math.sin(2*math.pi*(t+s)/c['mover_period']+phase)-c['mover_size'][0]/2
    return math.hypot(max(edge-pos[0],0.),c['mover_centre'][1]-c['mover_size'][1]/2-pos[1])-c['body_radius']
samples=[]
for i in range(501):
    s=.01*i/500
    free,_=point(b,s)
    fixed,_=point(b,s,True) if s<=h else point(corner,s-h)
    samples.append((1000*s,1e6*gap(free,s),1e6*gap(fixed,s)))
# Raster is a plotted scientific artifact, not an edited supplied image.
im=Image.new('RGB',(1500,850),'white');draw=ImageDraw.Draw(im)
fontpath='C:/Windows/Fonts/segoeui.ttf'
font=ImageFont.truetype(fontpath,24);small=ImageFont.truetype(fontpath,20);title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',34)
draw.text((40,25),'Why the free path was rejected — and where contact ends',font=title,fill='#1e293b')
draw.text((40,80),'Scalar reconstruction of one 0.01 s step; no trajectory beyond native 1026.',font=font,fill='#334155')
L,T,W,H=130,180,1180,520
def xy(x,y):return (L+x/10*W,T+(22-y)/27*H)
for x in (0,2,4,6,8,10):
    q=xy(x,-5);draw.line([xy(x,-5),xy(x,22)],fill='#e2e8f0',width=2);draw.text((q[0]-12,q[1]+10),str(x),font=small,fill='#475569')
for y in (-5,0,5,10,15,20):
    q=xy(0,y);draw.line([q,xy(10,y)],fill='#94a3b8' if y==0 else '#e2e8f0',width=2);draw.text((L-65,q[1]-12),str(y),font=small,fill='#475569')
draw.text((L,130),'Signed surface gap (millionths of one world unit)',font=font,fill='#334155')
draw.text((650,745),'Time within step (ms)',font=font,fill='#334155')
draw.line([xy(a,c) for a,b,c in samples],fill='#1768a6',width=5)
red=[xy(a,b) for a,b,c in samples]
for j in range(0,len(red)-4,8):draw.line(red[j:j+5],fill='#b91c1c',width=4)
x=h*1000;draw.line([xy(x,-5),xy(x,22)],fill='#475569',width=2)
draw.text((xy(x,21)[0]+12,xy(x,21)[1]),'Face exit: 4.798389 ms',font=small,fill='#334155')
draw.text((790,320),'Corrected: contact, then free flight',font=font,fill='#1768a6')
draw.text((155,500),'Rejected free candidate enters the solid',font=font,fill='#b91c1c')
draw.text((40,800),'Negative gap = penetration. Geometry tolerance is 0.0001 on this vertical scale; it was not widened.',font=small,fill='#475569')
im.save(HERE/'CONTACT_GAP_DIAGNOSIS.png')
authority_table='\n'.join(f"| {i} | {x['case_id']} | `{x['authority_sha256']}` |" for i,x in enumerate(matrix,1))
report=f'''# FS-001/M2 contact apparatus diagnosis and correction

**The stop was an apparatus release-path defect in a physically legitimate flat-face-to-corner transition. The penetrating free-path guard was correct and remains active. The narrow correction and historical regression pass. A fresh nine-case packet is prepared, not authorized or executed. Overnight high-contact readiness is NOT established.**

## Exact rejected geometry

The authoritative saved boundary is MC-FS-001-M2 native 1025, time `{t:.17g}`. The rejected attempt was native 1026. Original runtime/preparation and **MOTOR_COMMISSIONING_RESULT_v0_1** remain unchanged.

| Quantity | Recovered value |
|---|---|
| Body centre / radius | (9.663002128485367, 8.999999999935511) / 0.5 |
| Heading / angular speed | 5.317310609141483 rad / 0.02164230508214243 rad/s |
| Body velocity | (-0.0930360840814401, 0) |
| Mover rectangle | x=[9.658590869197981, 11.658590869197981], y=[9.5,10.5] |
| Mover velocity / phase | (0.8263246849800095,0) / 4.301831170857631 |
| Normal / initial gap | (0,-1) / 6.448885869758669e-11 |
| Tangential distance to left edge | 0.004411259287385505 |
| Relative tangential velocity | -0.9193607690614496 |
| Delivered command | (-0.24067992715298328,-0.22884852876080816) |
| Actual new actuator forces | (-0.08932124891183013,-0.08513047983855444) |
| Geometry / overlap / event-time tolerances | 1e-10 / 1e-8 / 1e-10 |

The original `release_probe` finds zero initial separating speed and no early outward-acceleration certificate. Its whole-interval search finds a clear point at +0.01 s (gap +8.585094012691918e-6). The prefix check finds penetration at +0.005 s (gap -3.5439993126273883e-6), and raises `Free-path release prefix crosses solid before clearance`.

This is substantial relative to the tolerance, not float-spacing noise: the candidate's minimum gap is approximately **-3.9657803e-6** at +0.0057747236 s. It first crosses -geometry_tol at +0.0000338573408 s and returns to zero at +0.0081499908 s. The guard therefore cannot lawfully be removed or widened to accept that candidate.

The body's footpoint leaves the mover's flat lower face at **+0.004798389124236565 s**. Before that event the normal constraint must remain; afterwards the rounded body/rectangle-corner distance allows separation. A single free-flight decision over the whole 0.01 s interval conflated these two regimes.

![Rejected and corrected gap curves](CONTACT_GAP_DIAGNOSIS.png)

The causal path is `core.step` → `Engine._coupled` → `physics.advance` → `release_probe` → `clear_excursion`. `EXACT_FAILURE_TRACE.json` preserves the original search locals, brackets, sampled gaps/rates, acceleration/jerk bounds and exception. `GEOMETRY_AUDIT.json` supplies independent scalar roots and position/displacement samples.

## Smallest supported correction

`clear_excursion` still rejects the inadmissible free path, now using an `ArithmeticError` subclass (`BlockedRelease`). The scheduler may handle that particular rejection by locating a flat-face feature event **only when there is one active axis-aligned rectangle face and a certified monotone tangential edge crossing**. Normal projection does not change tangent motion in that regime.

The absolute relative second-derivative bound is 0.7132556261992498. Even its maximum allowed tangential rate over the interval is -0.9122282127994571, proving the edge crossing is unique and ordered. Bisection returns +0.004798389151692391 s; error against the independent scalar root is 2.7455826674682715e-11 s, inside the unchanged 1e-10 s event tolerance.

The existing constrained law is advanced to that event, contact is reevaluated, and the ordinary release and swept-impact searches operate on the remainder. A missing certificate, simultaneous active contacts or a still-blocked shortened probe continues to fail explicitly. No new time-based fallback, overlap repair, position nudge, guard bypass or tolerance change was introduced.

Corrected native 1026 has:

- sustained face contact for **0.004798389151692391 s**;
- normal impulse **0.0006868940462345461**, force **0.143150966818162**;
- zero-duration release, then **0.005201610848307609 s** free flight;
- total expenditure **1.7347642279568958e-5**, no transfer, repair or additional damage;
- final centre **(9.662071305893539,9.000003872044829)**, outside the mover;
- one native organism call and one field advance; no extra RNG draw/cadence event caused by contact subdivision.

The body may have y>9 after the corner passes; that is outside the finite mover footprint, not tunnelling through its face. Normal impulse balance, all energy/source/integrity ledgers, intermediate gaps and final gaps are checked. This model is dissipative with an externally prescribed mover: “conservation” here means its declared impulse and reserve/transfer accounting, not an invented conservation of total mechanical energy.

## Tests and engineering reconstruction

**45 mechanics/scheduler tests + 2 identity tests + 26 unchanged motor component tests pass.** The exact geometry was RED on the original implementation and GREEN after correction. Neighbours include ±0.001 tangential offsets, a reflected encounter, an unended face, an already clear corner, an incoming impact and invalid overlap. Directly asking for the rejected free release still raises. A test denying the feature certificate proves the scheduler does not suppress the guard. An independent scalar oracle and dense checks within each corrected physical subinterval check nonpenetration; existing swept-impact, oblique release/return, terminal and ledger regressions remain green.

| Historical case | Exact reconstructed extent | Result |
|---|---|---|
| CURRENT FS-001 | 9000 native steps / 90 s | Bit-identical native records, events, waves, chunk neural/field/RNG digests and endpoint |
| M1 FS-001 | 9000 native steps / 90 s | Same exact checks pass |
| M2 FS-001 | 1025 native steps / 10.25 s | Same exact checks pass; failure-status metadata normalized on an engineering copy only |

CURRENT/M1 also round-trip their saved native-6000 checkpoint and complete the remaining historical path exactly. Corrected step 1026 is bit-identical from the reconstructed endpoint and a serialized pre-failure-state copy. No M2 step beyond 1026 was attempted. The corrected sample is labelled engineering evidence, not appended to the historical life.

Test-attempt provenance is retained: an early fixture-copy path mistake and a reflected-test construction error were repaired in test setup; the default pytest temporary directory was inaccessible, so a task-local temporary directory was used. The first historical reconstruction passed all three prefixes, then its tracing hook failed before physical advance because Python 3.13 frame locals cannot be deep-copied directly. The unused hook was removed and the engineering regression repeated, passing completely. Thus there were two engineering reconstructions of the historical prefixes, not two commissioning executions. No production law was adjusted to make a test pass.

## Runtime and provenance

- Frozen P mechanism reference: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.
- Parent lean apparatus: `87abae34e19d4e46234402a6b1ba776814956ec1`.
- Corrected checkpoint: **`{commit}`**.
- Branch: `build/p-contact-release-20260930`.
- Corrected body/P-package code digest: `98bbf9053ca55ef545c6fc868e54c85342149d143319281a47f9a1fd71c28c7d`.
- Fresh packet runtime identity: **`{runtime}`**.

Production changes are confined to `loom_p/physics.py` and the exact-source binding argument of `loom_developmental/runner.py`. The entire old P package digest is not reused: physics belongs to that package, so its executable identity changes. Neural/P learning code, all configuration values, sensors, actuator constitutive equations, source laws, birth fixtures and motor-process implementation remain byte-identical. The default identity check still rejects the corrected tree; only an explicit exact corrected digest accepts it. No silent identity reconciliation occurs.

## Fresh nine-case packet — not launched

Screen ID: **MOTOR_COMMISSIONING_v0_2_CORRECTED_APPARATUS**. All nine begin independently from the already prepared zero-age states. Their complete engine bytes are identical to v0.1; only each snapshot's outer runtime identity changes. Per triplet, physical state, fields and original RNG state remain identical. M1/M2 process state, distribution, parameters and candidate RNG streams are unchanged. This fresh screen is neither a retry under an old authority nor a replacement for v0.1 evidence. Old authorizations do not apply.

| Order | Case | New authority SHA-256 |
|---:|---|---|
{authority_table}

Ceilings and recording remain **90 s / 9000 steps, 300 active wall s and 32 MB per case**, with the original 16 MB closure reserve, 100-step chunks, 6000-step checkpoints and complete Tier-1/motor evidence. Batch allowance stays 2700 active wall s; preflight/verification allowances stay 300/600 s. Require 2 GB free before batch and 1 GB before each case. Shared apparatus/resource failure stops the batch with later cases unstarted. No retry, continuation, tuning or selection permission is included.

Historical planning range remains **4.3–14.2 active minutes and about 59–77 MB primary evidence** for nine cases, before compact motor diagnostics and archive overhead. The two completed motor cases took about 67 s combined; corrected historical reconstruction took {r['seconds']:.1f} s for the available 19025-step denominator plus the two single-step checks. These support the existing envelope, not a guarantee for new contacts. The resource limits and evidence fidelity were not reduced. Full source/runtime/start preflight passed on the fresh packet, and must run again immediately before any separately authorized launch.

## Overnight readiness and stop

**NOT READY TO DECLARE AN OVERNIGHT HIGH-CONTACT SANDBOX SAFE.** The exact defect is resolved and the new bounded screen is fit to propose. These checks do not cover many hours, all curved/simultaneous contact regimes or every resource/interruption path. The original solver's explicit guards remain for uncertified cases, and the separate FS-060 interruption has not been diagnosed here. Broader readiness must be established separately; a successful 90 s screen alone would not prove it.

No fresh motor-screen case, long run, Nursery change, resurrection, motor tuning, new prehistory, push or merge occurred. v0.1 remains immutable historical evidence. Stop for Jason review.
'''
(HERE/'APPARATUS_ROOT_CAUSE_AND_CORRECTION.md').write_text(report,encoding='utf8')
(PACKET/'README.md').write_text(f'''# Motor commissioning v0.2 — prepared, not authorized

New common contact apparatus: `{commit}`. Runtime: `{runtime}`.

This is the complete original 3 starts × CURRENT/M1/M2 × 90 s screen under one corrected common apparatus. Original births, all process-state draws, parameters, ceilings, recording fidelity and interpretation criteria are unchanged. The complete engine objects are byte-identical to the previously prepared states. No case has executed.

Read `AUTHORITY_INDEX.md` for all nine fresh identities, `SEMANTIC_DIFF.json` for identity/correction changes, `MATCHED_INITIAL_STATE_PROOF.json` for exact state matching, `PARAMETERS.json` and `loom_motor_commissioning/motor.py` for unchanged equations, `RESOURCE_PLAN.json` for the unchanged envelope and `ANALYSIS_PLAN.md` for fixed passive comparisons. `STATIC_PREFLIGHT_REPORT.json` and `COMPONENT_TESTS.xml` pass.

The historical MOTOR_COMMISSIONING_RESULT_v0_1 is preserved, not replaced or supplemented. Its old authorizations cannot launch this packet. `execute_after_authorization.py` requires a separate explicit authorization record with these nine exact hashes, in order, and refuses an existing execution directory. No such authorization is supplied.

Fit for bounded commissioning proposal only. Overnight high-contact safety remains unestablished. No automatic mechanism selection, Nursery modification, resurrection or long run.
''',encoding='utf8')
print('Review and fresh packet README written; no simulation calls.')
