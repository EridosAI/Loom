"""Report the sealed observed denominator; no simulation imports."""
from pathlib import Path
import csv,json,math,time
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent;PREP=ROOT/'motor_commissioning_preparation_20260930_v0_1';EX=PREP/'execution'
all_results=json.loads((OUT/'PASSIVE_RESULTS.json').read_bytes());R=all_results[:3]
den=json.loads((OUT/'DENOMINATOR_RECONCILIATION.json').read_bytes())
seal=json.loads((OUT/'EXECUTION_CUSTODY_SEAL.json').read_bytes());validation=json.loads((OUT/'PASSIVE_VALIDATION.json').read_bytes())
def f(x,d=4):return '—' if x is None else f'{x:.{d}f}'
def matrix_table():
    rows=[]
    for i,r in enumerate(all_results,1):
        if r['status']=='NOT_STARTED_BATCH_STOP':rows.append(f"| {i} | {r['case_id']} | Unstarted after batch stop | — | — |")
        else:rows.append(f"| {i} | {r['case_id']} | {'90 s completed' if r['has_closed_receipt'] else 'Apparatus-interrupted prefix'} | {r['verified_native_steps']} | {r['nominal_age_seconds']:.2f} |")
    return '\n'.join(rows)
def kin_table():
    return '\n'.join(f"| {r['process']} | {r['nominal_age_seconds']:.2f} | {r['kinematics']['path_length']:.6f} | {r['kinematics']['maximum_excursion']:.6f} | {r['kinematics']['displacement']:.6f} | {r['kinematics']['displacement_path_ratio']:.6f} | {r['kinematics']['grids']['025']['visited_cells']} | {r['kinematics']['grids']['025']['previously_visited_reentries']}/{r['kinematics']['grids']['025']['cell_transitions']} |" for r in R)
def movement_table():
    rows=[]
    for r in R:
        k=r['kinematics'];b=k['bouts']['0.01'];fw=b['forward_qualifying_summary'];rv=b['reverse_qualifying_summary']
        rows.append(f"| {r['process']} | {fw['count'] if fw else 0} | {f(fw['median'] if fw else None,3)} | {f(fw['maximum'] if fw else None,3)} | {rv['count'] if rv else 0} | {f(rv['median'] if rv else None,3)} | {f(rv['maximum'] if rv else None,3)} | {b['switches']} |")
    return '\n'.join(rows)
def common10_table():
    rows=[]
    for r in R:
        w=r['common_predeclared_10_second_window'];k=w['kinematics'];p=w['physical']
        rows.append(f"| {r['process']} | {k['path_length']:.6f} | {k['maximum_excursion']:.6f} | {k['displacement_path_ratio']:.6f} | {p['effort_expenditure']:.8f} | {p['total_impulse']:.6f} | {p['damage']:.8f} |")
    return '\n'.join(rows)
def energy_table():
    return '\n'.join(f"| {r['process']} | {r['physical']['expenditure']:.8f} | {r['physical']['basal_expenditure']:.8f} | {r['physical']['effort_expenditure']:.8f} | {r['physical']['final_reserves'][0]:.8f} | {r['physical']['final_reserves'][1]:.8f} | {r['physical']['total_impulse']:.6f} | {r['physical']['damage']:.8f} |" for r in R)
def heading_table():
    rows=[]
    for r in R:
        k=r['kinematics'];rows.append(f"| {r['process']} | {k['mean_speed']:.5f} | {k['mean_abs_angular_speed']:.5f} | {k['heading_net_change_degrees']:.2f}° | {k['heading_total_absolute_rotation_degrees']:.2f}° | {100*k['predominantly_rotating_fraction']:.2f}% | {100*k['predominantly_translating_fraction']:.2f}% |")
    return '\n'.join(rows)
def command_table():
    return '\n'.join(f"| {r['process']} | {r['kinematics']['common_command_rms']:.6f} | {r['kinematics']['differential_command_rms']:.6f} | {r['kinematics']['left_right_correlation']:.6f} | {100*r['kinematics']['opposed_command_fraction']:.2f}% |" for r in R)
def growth_table():
    return '\n'.join(f"| {r['process']} | {a['age_seconds']:.2f} | {a['maximum_excursion']:.6f} | {a['coverage025']} | {a['coverage100']} | {a['coverage025_offset']} |" for r in R for a in r['kinematics']['ages'])
def persist_table():
    rows=[]
    for r in R:
        for p in r['kinematics']['persistence']:
            rows.append(f"| {r['process']} | {p['lag_seconds']:g} | {f(p['direction_correlation'])} | {p['valid_direction_pairs']} | {f(p['heading_correlation'])} |")
    return '\n'.join(rows)
def gain_table():
    rows=[]
    for r in R:
        c=r['coupling'];g=c['gain_before_relaxation']['distribution'];a=c['attenuation']['distribution']
        rows.append(f"| {r['process']} | {c['recorded_wave_count']} | {g['minimum']:.6f} | {g['median']:.6f} | {a['minimum']:.4f}–{a['maximum']:.4f} | {c['direct']['rms']:.6f} | {c['current']['rms']:.6f} | {c['evoked']['rms']:.3g} |")
    return '\n'.join(rows)

report=rf'''# M1/M2 motor commissioning — bounded result and apparatus stop

**The nine-case matrix is incomplete because the prepared shared-apparatus stop rule fired. Two cases completed; one has a verified 10.25 s prefix; six were never started. No retry, continuation, replacement or patch occurred. No motor mechanism is selected. CURRENT remains the reference.**

FS-001/M2 stopped while attempting native step 1026. The original physical contact-path guard raised `ArithmeticError: Free-path release prefix crosses solid before clearance`. Its last committed native index is **1025**, nominal age **10.25 s**. The executing process exited with failure; nothing remains running for this batch. This is an apparatus stop, not biological nonviability and not evidence that M2 is physically impossible.

## Exact denominator

| Order | Authorized case | Disposition | Committed native steps | Nominal recorded age (s) |
|---:|---|---|---:|---:|
{matrix_table()}

Unstarted means **unobserved**, not zero movement/contact/cost. The original executor `DENOMINATOR.json` retains its failed-case `STARTED` / zero-counter entry because that row is normally finalized after closure. It was not edited. `DENOMINATOR_RECONCILIATION.json` derives M2's actual boundary from `failure-s000.json`, the saved chunks and `failure-tail-s000.ld`.

The two completed cases each contain exactly **9000 native steps**, nominal 90 s. Their accumulated floating clock is `90.00000000000914`; this is the original binary64 sum of 9000 × 0.01, not an additional step or a changed ceiling. M2's stored clock is `10.249999999999826`.

## What the available comparison shows

- **CURRENT:** repeated local forward/reverse travel. At 90 s, path length is 4.106 units but maximum birth excursion is only 0.400 and final displacement 0.159. There were 20 qualifying forward/reverse switches. This run reproduces the preserved original FS-001's first 9000 native rows exactly, across all recorded native fields.
- **M1:** in this one matched start, path length is similar (4.035 units), while maximum excursion is 1.059 and final displacement 1.003. Effort cost is 0.18% lower than CURRENT, and neither recorded contact or damage. The larger reach therefore did not coincide with greater total effort or impacts in this particular 90 s comparison. However, M1 made **31% more absolute body-heading rotation**, spent more time predominantly rotating, and its first 10 s had less maximum excursion and more effort than CURRENT. This is a different temporal/curving regime, not a selected improvement or evidence of general superiority.
- **M2:** the 10.25 s prefix is dominated by a coherent negative common drive and movement mainly backwards relative to the body. It contacted the mover and sustained integrity damage. Over the common first 10 s, effort was **68.9% higher than CURRENT** (16.1% higher than M1). Its larger early reach is therefore confounded with a stronger realized command sample and contact dynamics; it must not be called an unqualified exploration improvement. The fixed first renewal was at **11 s**, so **no M2 target renewal occurred before the apparatus stop**. The irregular-renewal regime remains unobserved in this world screen.

The parameters were not changed and no observation was used to choose a new phase, draw, start or route. M2's birth common latent was -1.347284973074013 with differential 0.14468104530650436, exactly the prepared draw. Its two spontaneous terms stayed at approximately -0.31629005 and -0.29205650 before the first renewal. Equal population-scale RMS proposals do not force equal strength in a short realization. No cause share between timing, realized strength and collision effects is identified by this interrupted sample.

## Native path and coverage

All distances are world units. Path is the native body-centre polyline, including the segment from the preserved birth position. Coverage counts visited body-centre bins, not swept physical area. Re-entry counts a transition into an already visited bin after leaving it.

| Process | Observed seconds | Path | Maximum excursion | Final displacement | Displacement/path | 0.25-unit bins | Re-entry transitions |
|---|---:|---:|---:|---:|---:|---:|---:|
{kin_table()}

CURRENT's 0.25-bin re-entry fraction is 83.33%; M1's is 14.29%; M2's prefix is 11.11%. At the predeclared half-bin offset the fractions are 80.95%, 21.74% and 0%, respectively. At 1-unit resolution they are 50%, 40% and 25%, with only 2, 5 and 4 transitions. These small grid counts depend on alignment and are not precise arena-coverage percentages.

![Matched FS-001 paths; CURRENT and M1 complete, M2 interrupted](FS001_PATHS.png)

| Process | Age (s) | Maximum excursion | 0.25 bins | 1-unit bins | Offset 0.25 bins |
|---|---:|---:|---:|---:|---:|
{growth_table()}

## Matched first 10 seconds

Ten seconds was already a declared reporting age and is available in all three started cases. This table prevents treating M2's short prefix as a full-length comparison.

| Process | Path | Maximum excursion | Displacement/path | Effort cost | Total impulse | Damage |
|---|---:|---:|---:|---:|---:|---:|
{common10_table()}

M1's early effort cost is 45.46% above CURRENT while its maximum excursion is smaller (0.181 versus 0.250). Its larger later reach at similar total cost does not erase this early tradeoff. No interval was used as a selection gate.

## Reversals, heading and command organization

Forward/reverse bouts use native body-frame forward velocity above +0.01 or below -0.01 units/s. This table includes bouts lasting at least 0.1 s. Switches compare successive qualifying signs, ignoring deadband; they are body-velocity changes, not commanded semantic actions. Final bouts are right-censored by the recording boundary and remain included as observed durations. Complete bout lists and predeclared 0.005/0.02 sensitivity summaries are retained in each `*_DETAILS.json`.

| Process | Forward bouts | Median s | Maximum s | Reverse bouts | Median s | Maximum s | Switches |
|---|---:|---:|---:|---:|---:|---:|---:|
{movement_table()}

| Process | Mean speed | Mean absolute angular speed (rad/s) | Net heading change | Total absolute rotation | Predominantly rotating | Predominantly translating |
|---|---:|---:|---:|---:|---:|---:|
{heading_table()}

Headings are unwrapped: M1's -507° net change is not reduced modulo one turn. “Predominantly” uses the prepared ratio of body-edge rotational speed to translational speed (>2 in either direction), with activity threshold 0.005. These are kinematic classifications, not intent or actuator energy partitions.

| Process | Common command RMS | Differential command RMS | Left/right correlation | Opposed command signs |
|---|---:|---:|---:|---:|
{command_table()}

M2's recorded commands stay negative on both sides; its brief body-forward movement does not establish a spontaneous motor reversal. It occurred in the prefix containing mover interactions. M1's sustained differential tendency produces much more heading drift than CURRENT, even while its velocity direction persists longer at several lags.

![Recorded timing, coverage, velocities, heading and commands](FS001_TIMING.png)

Velocity-direction correlation uses unit velocity vectors only where both speeds exceed 0.01, sampled at exact 0.1 s indices. Heading correlation is the mean cosine of heading differences. These are lag descriptions, not fitted persistence or diffusion constants; M2 has no 16 s observation.

| Process | Lag (s) | Velocity-direction correlation | Valid pairs | Heading correlation |
|---|---:|---:|---:|---:|
{persist_table()}

## Expenditure, contact and damage

All three cases started at E=0.7, I=1. Expenditure is retained separately from intake; basal and effort terms are checked against the existing event ledger. The totals below use each case's available duration, so M2's lower total expenditure must not be interpreted as lower cost for a 90 s case.

| Process | Total expenditure | Basal | Effort | Final E | Final I | Total impulse | Damage |
|---|---:|---:|---:|---:|---:|---:|---:|
{energy_table()}

CURRENT and M1 had **no recorded wall, mover, source, restorative or other contact** in their 90 s records. M2 had mover contact only: first at **7.9372436806 s**, continuing intermittently through the final committed sample. Recorded positive-duration contact totals **0.8543180794 s**; this is not the whole time between first and last touch. Its 88 contact records are subinterval/impact records, not 88 independent collisions.

M2's impulse totals are **0.3908428989 instantaneous** and **0.1250031008 sustained**, total **0.5158459997**. Largest instantaneous impulse is **0.3088411675**. Peak sustained force is **0.1519709625**, below the 0.25 stress threshold; the **0.0078168580** recorded damage is accounted for by instantaneous impacts. M2's final E and I remain positive. Wall/other contact, repair, source contact and source transfer are zero in the **available** records. Six unstarted cases have no observations for these quantities.

Source absence is descriptive only. It is not a motor selection criterion, viability score or inference about future food access.

## Ordinary feedback/regulatory susceptibility

At every recorded wave the observer used the saved spontaneous, direct-feedback, associative and current contributions. It calculated

$$g=(1-\alpha)\,\operatorname{{sech}}^2(o+\mathrm{{direct}}+\mathrm{{evoked}}+i).$$

This is the local command-target gain before the unchanged motor relaxation; the immediate 0.01 s response additionally contains $1-e^{{-0.01/0.1}}$. It is not an experimental intervention or a learned-competence measure.

| Process | Saved waves | Minimum g | Median g | Attenuation range | Direct-feedback RMS | Regulatory-current RMS | Associative-return RMS |
|---|---:|---:|---:|---|---:|---:|---:|
{gain_table()}

No saved sample has tanh gain below 0.1 or attenuation above 0.95. There is **no recorded evidence of saturation or attenuation practically closing the ordinary additive pathway** in the observed intervals. However, actual current is only about 0.014–0.015 RMS, direct feedback is smaller, and the associative return is very small relative to spontaneous drive. In M2's strong negative initial tendency those realized inputs did not reverse the commands. Available sensitivity is not proof that the existing learning can develop adequate control. Physical contact can also restrict achieved movement despite responsive commands. Unobserved M2 time and the unstarted six cases supply no coupling evidence.

## Apparatus boundary and custody

The stored traceback follows `Life.advance` → unchanged `loom_developmental/core.py:47` → `Engine._coupled` → `physics.advance:285` → `release_probe:207` → `clear_excursion:160`. The exact rejection is:

```python
if search(probe, -1., c.geometry_tol) is not None:
    raise ArithmeticError('Free-path release prefix crosses solid before clearance')
```

The guard rejects a proposed release path that has a detected inward solid crossing before a later clear point. This explanation comes from the unchanged source and recorded exception, not a new physical rollout. The saved prefix ends during mover contact. The exception does not store the internal probe scalar values, so this report does not invent them or claim a complete root-cause diagnosis. No failed step was rerun and no guard was widened or bypassed.

M2 has ten closed chunks through step 1000 plus **25 additional committed native rows**, one wave and their events in `failure-tail-s000.ld`. The complete available denominator contains **{validation['total_native_rows']} native rows**: 9000 + 9000 + 1025. Row clocks, sequence, wave indices, native/event counts, endpoint body/reserves and physical ledgers validate. M2 has no normal final segment receipt; a verified prefix is not relabelled as a completed case. All available bytes were sealed before metrics in `EXECUTION_CUSTODY_SEAL.json`.

All prepared hashes and full-runtime preflight passed before launch. The unchanged executor repeated its full gate immediately before each of the three started cases. Its completed-case active-wall counter is **{den['raw_denominator']['active_wall_seconds']:.6f} s**; it omits the failed case because that case has no normal stop receipt. Preflight total is **{den['raw_denominator']['preflight_wall_seconds']:.6f} s**, completed-store verification **{den['raw_denominator']['verification_wall_seconds']:.6f} s**. Do not read the completed-case counter as exact total batch wall time. Available execution files occupy **{seal['bytes']:,} bytes**. The cause was the contact-path exception, not a reported wall/storage cutoff. The prepared resource limits were not enlarged.

## Identity, limitations and disposition

The nine authority hashes are the exact objects in the unchanged preparation `AUTHORITY_INDEX.md` and the copied `execution/JASON_AUTHORIZATION.json`. Frozen P baseline is `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; lean base is `87abae34e19d4e46234402a6b1ba776814956ec1`; bound overlay/runtime identity is `d1b14d75dc30e2934c76e209e0354ca236ac0115f381b4cbbf5c15093ba9a41a`. M1/M2 retain their separately identified spontaneous replacement; neither is described as identical to intact CURRENT.

Only the prepared passive comparison was performed after the stop. No neural/world replay, extra trial, outcome-based reordering, tuning, founder scoring or automatic selection was performed. Canonical P/world/sensor/source/learning laws, the original birth law, Nursery-0 geometry and viability/resilience were not changed. Normal within-life learning proceeded only inside the authorized executed cases. CURRENT is preserved as the reference.

The requested full three-start comparison remains **unavailable**. Missing evidence includes M2 after its first renewal, M2's 90 s cost/coverage/coupling, all FS-002/003 results, and cross-start consistency. These records cannot establish a preferred mechanism, developmental benefit, food competence or long-run safety. A diagnosis/correction or any future execution requires a separate Jason decision; no replacement packet or continuation is prepared here.

**Stop for Jason review.**
'''
(OUT/'MOTOR_COMMISSIONING_RESULT_v0_1.md').write_text(report,encoding='utf8')
(OUT/'README.md').write_text('''# M1/M2 motor comparison — apparatus-stopped result

Two FS-001 cases completed at 90 seconds. FS-001/M2 has a verified 10.25-second prefix. The six FS-002/003 cases remain unstarted. No retry or patch. No mechanism selected.

- [Full bounded report](MOTOR_COMMISSIONING_RESULT_v0_1.md)
- [Reconciled nine-case denominator](DENOMINATOR_RECONCILIATION.json)
- [Available metrics](AVAILABLE_CASE_METRICS.csv) and [coverage growth](COVERAGE_AND_EXCURSION_GROWTH.csv)
- [All observations](PASSIVE_RESULTS.json), with full per-case detail and wave-coupling records
- [Paths](FS001_PATHS.png) and [timing](FS001_TIMING.png); vector SVG versions also provided
- [Raw execution seal](EXECUTION_CUSTODY_SEAL.json), [passive validation](PASSIVE_VALIDATION.json), [final verification](FINAL_VERIFICATION.json)

The result archive includes all available raw execution files and the frozen review packet. The original failed-case denominator row is retained unchanged; the reconciliation explains its incomplete counter. Interrupted and unstarted cases are not silently excluded.
''',encoding='utf8')
rows=[]
for r in all_results:
    k=r.get('kinematics');p=r.get('physical')
    rows.append(dict(case_id=r['case_id'],status=r['status'],recorded_native_steps=r.get('verified_native_steps',0),
        nominal_age_seconds=r.get('nominal_age_seconds',0),path_length=k['path_length'] if k else None,
        max_excursion=k['maximum_excursion'] if k else None,displacement_path_ratio=k['displacement_path_ratio'] if k else None,
        effort_expenditure=p['effort_expenditure'] if p else None,damage=p['damage'] if p else None,source_transfer=p['source_transfer'] if p else None))
with (OUT/'ALL_NINE_DISPOSITIONS.csv').open('w',newline='',encoding='utf8') as file:
    writer=csv.DictWriter(file,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print('Bounded report written; nine-case denominator retained; no world calls.')
