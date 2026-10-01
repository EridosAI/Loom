from common import *
import html

summary=json.loads((OUT/'CURVE_SHAPE_SUMMARY.json').read_bytes())
fits=list(csv.DictReader((OUT/'tables/SHAPE_MODEL_COMPARISON.csv').open()))
fun=list(csv.DictReader((OUT/'tables/FUNCTIONAL_READOUT_BY_AGE.csv').open()))
qa=json.loads((OUT/'CURVE_CONSISTENCY_REVIEW.json').read_bytes())
notes={
1:('H has early rise, long noisy middle, then several late excursions; its final-1000 slope is small relative to local fluctuations.','E grows through several phases and rises faster late than early. It is not near an established ceiling.','I has discrete early and late increases, followed by reference-driven decline. The late robust slope describes the decline, not absence of learning.'),
2:('H rises early and is lower late; a concave-down envelope is plausible, with appreciable reversals.','E is irregular and nearly level over the final 1000 s despite some late recovery.','I grows in early steps and mostly fades thereafter, with smaller later events.'),
3:('H has alternating increases and declines, including a positive late trend; a single plateau misses those phases.','E remains positively developmental late, with slower rise than early.','I has a conspicuous late jump followed by decay. A smooth monotonic curve does not describe this history.'),
4:('H has a fairly stable decelerating overall envelope but rises again late.','E peaks early, oscillates and declines late. Saturation is not a sufficient description of the reversal.','I accumulates in occasional steps separated by fading intervals.'),
5:('H broadly levels after early growth, with late decline and fluctuations.','E continues rising late at a reduced background rate; it has not demonstrated a stable asymptote.','I has a very late upward step after a long low-level history. The final-1000 robust slope is negative because it follows the long background decay; the raw step must not be averaged away.'),
6:('H approaches a fluctuating band and is nearly flat on the final-1000 robust slope, although earlier late excursions remain visible.','E shows renewed strong late growth after a long slower phase. A whole-life exponential understates this renewed development.','I has small event-linked increases; the late trend is positive at a small absolute magnitude.'),
7:('H has a decelerating envelope with a negative late background trend.','E rises early, then oscillates around a broad level and declines slightly late.','I remains strongly event-shaped and has a large very late rise.'),
8:('H rises again before its last complete checkpoint.','E is nearly flat on its final-1000 robust trend but recovers near the cutoff.','I is small and mostly declining late. No claim is made about its unobserved future.'),
9:('H grows then becomes much slower within the pilot.','E rises early and is almost flat/slightly falling late in this short history.','I begins to increase late in the pilot.'),
10:('H continues rising in the pilot.','E continues rising in the pilot.','I remains exactly zero throughout the measured pilot; the preserved physical record has no damage or repair.'),
11:('H continues rising across the pilot.','E continues rising across the pilot.','I has late event-linked growth.'),
12:('H grows strongly then declines before 600 s.','E grows earlier and slows late.','I grows early and then fades.')}
def fmt(v,d=4):
    if v is None or v=='':return '—'
    return f'{float(v):.{d}g}'
def figure(name,alt):return f'![{alt}](figures/{name}.png)\n'
def modeltable(metric):
    out=['| Life | Best full-interval descriptive RMSE | R² | Residual lag-1 | Exp τ: full / omit 600 s | Exp A: full / omit 600 s |','|---|---|---:|---:|---:|---:|']
    for n in range(1,8):
        life=f'RS-M1-{n:03d}';r=[x for x in fits if x['life']==life and x['metric']==metric];v=[x for x in r if x['exclude_first_seconds']=='0'];best=min(v,key=lambda x:float(x['RMSE']));e=next(x for x in v if x['model']=='saturating_exponential');q=next(x for x in r if x['exclude_first_seconds']=='600' and x['model']=='saturating_exponential')
        out.append(f"| {n:03d} | {best['model'].replace('_',' ')} ({fmt(best['RMSE'])}) | {fmt(best['R_squared'],3)} | {fmt(best['residual_lag1'],3)} | {fmt(e['p_or_tau_seconds'])} / {fmt(q['p_or_tau_seconds'])} | {fmt(e['a_or_A'])} / {fmt(q['a_or_A'])} |")
    return '\n'.join(out)

text='''# H_E_I_DEVELOPMENTAL_CURVES_v0_1

**NON-CANONICAL RESURRECTION SANDBOX — passive analysis, 1 October 2026.**

The three systems show different shapes. **H rises rapidly early, then enters a much slower, fluctuating regime. E remains developmental in several lives but reverses or levels in others. I is predominantly event-driven: abrupt increases separated by fading.** There is no common straight-line accumulation law and no evidence that all three have reached a stable learned ceiling.

[Open the local figure viewer](CURVE_REVIEW.html). It contains all twelve five-panel figures, the functional readouts, slopes and fit-residual plots. It only displays saved files.

## The measured population curves

Seven complete lives share the same 4500-second axis. The censored organism is a separate lower panel. Pilots are not pooled into the long-life comparison. These are stored per-wave measurements, not reconstructed developmental histories.

'''
text+=figure('POPULATION_H_norm','H norm: seven complete histories and separate censored prefix')
text+=figure('POPULATION_regulator_theta_E_norm','Learned E-bank norm: seven complete histories and separate censored prefix')
text+=figure('POPULATION_regulator_theta_I_norm','Learned I-bank norm: seven complete histories and separate censored prefix')
text+=r'''## What was measured and preserved

The exact implementation fields are `association.H`, a dictionary of 56 directed inter-family maps, each with four branches; `regulator.theta[0]`, the E bank; `regulator.theta[1]`, the I bank; `body.energy`; and `body.integrity`. The plotted combined H norm is $\sqrt{\sum_{m,n,j}\|H_{mn,j}\|_F^2}$. Each regulator bank is a 12-by-33 array; its norm is the Frobenius norm of that complete array. A larger norm does not establish better representation, source specificity or beneficial control.

The source wave fields are `map_update_use[:,:4]` (post-write map norms) and `regulator_bank_norm` (post-credit bank norms). H return `q` is the preceding old-map read within the same handoff, before that handoff's write. This ordering matters: the H norm and q in a row belong to different positions in the accepted read/write sequence. No neural function was called to regenerate either one.

The primary series retain every completed 0.2-second wave. Physical E/I exports retain every accepted native record, nominally 0.01 s with genuine fractional boundaries. The original birth norm is zero and is shown explicitly. No sparse matrix state is interpolated. Complete-life final checkpoints have the same norms as their last completed wave; there is no fictitious last wave at exactly 4500 s.

RS-M1-008 is deliberately cut at **2939.9548705459583 s**, its last complete causal checkpoint. Durable native/wave evidence continues to 2968.9548705465913 s, but that later prefix is outside this priority causal-curve display. It remains preserved for the broader physical audit. RS-M1-009–012 stop at 600 s; their overnight stages never started.

Every dark trend line is a **trailing 60-second arithmetic mean of stored samples in (t−60,t]**, shortened near birth. This is a descriptive smoother, not an inferred state. Native body plotting retains chronological first/last/min/max within each horizontal display bin; the compressed CSV retains all native rows. Smoothed E ramps around support are not the instantaneous support jump: the thin raw line and red marker retain that jump. The export and exact support ledger retain both sides.

Red vertical lines mark all external resurrections. Green dots mark the first positive-transfer encounter and later bouts transferring at least 0.02 E; red dots mark contact episodes causing at least 0.002 damage; purple dots mark at least 0.0001 repair. These fixed **display thresholds** avoid hiding the curves, are not competence criteria, and do not exclude lesser events from the preserved evidence. This priority display uses the previous report's one-second time-grouped source bouts. The broader geometry/time sensitivity analysis is a separate task. Marker overlap is not proof of causation.

## Local slopes: measured shape, not endpoint inference

The slope estimator is Theil–Sen applied to non-overlapping 5-second medians within each fixed window. It is robust to isolated spikes. We also export ordinary least-squares slopes, the first/last 60-second median difference, the within-window range and residual MAD. The full table includes 300 s and 600 s windows, early/middle/late bands and the final 1000 s where available. There are no significance tests or fitted significance thresholds.

For the seven complete lives, early is 0–1000 s, middle is 1750–2750 s and late is 3500–4500 s. For pilots, early/middle/late are their three 200 s thirds. The censored life uses bounded third-length early/middle bands and a separate final-1000 band. Do not compare a pilot slope as though it had 4500 s of exposure.

'''
text+=figure('LOCAL_SLOPES','Robust local slopes across fixed 600-second windows')
text+='\n### Final 1000 s of complete lives\n\nNumbers are robust predicted **norm change per 1000 s**, followed by that change as a percentage of the late median norm. Percentages measure relative structural change, not skill.\n\n| Life | H | E bank | I bank |\n|---|---:|---:|---:|\n'
for n in range(1,8):
    values=[]
    for metric in ('H_norm','regulator_theta_E_norm','regulator_theta_I_norm'):
        r=next(x for x in summary if x['life']==f'RS-M1-{n:03d}' and x['metric']==metric)['late'];v=r['theil_sen_slope']*1000;values.append(f'{v:+.4g} ({100*v/r["median"]:+.1f}%)')
    text+=f'| {n:03d} | '+ ' | '.join(values)+' |\n'
text+=r'''
H has positive final-1000 slopes in 001/003/004, negative slopes in 002/005/007, and a near-zero slope in 006. The positive H slope in 001 is small beside its local fluctuations; it is not a uniform sustained rise. E has substantial positive late structural change in 001/003/005/006; 002 is comparatively level, and 004/007 decline. “More time” remains a possible explanation for incomplete E development in some organisms, not a general conclusion about all organisms or useful behavior.

I requires special care. Its robust late slope is negative in five lives and positive in two, **yet 005 has a large very late positive step**. The median-slope estimator follows the long preceding decay and must not erase that event. Similarly, 003 has a large late jump followed by decay. The raw curves, fixed-window slopes and [largest-increment catalog](tables/EVENT_STEP_CATALOG.csv) preserve these differences. A negative background slope is not evidence that no new learning event occurred.

[All local/late slopes](tables/LOCAL_AND_LATE_SLOPES.csv).

## Small descriptive model comparison

The candidate forms are $y=a+bt$, $y=A-B\exp(-t/\tau)$, and $y=a+bt^p$. Fits use non-overlapping 60-second medians, a robust soft-L1 loss and no prediction of unseen physical outcomes. Exponential and power growth amplitudes and their implied birth levels are nonnegative. Exponential τ is bounded to 1–1,000,000 s and power p to 0.05–3 for numerical identification; bound-hitting estimates are flagged, not treated as findings. Parameters in the CSV use actual seconds. Each form is fitted to 0–4500 s and again after excluding 0–600 s.

These smooth monotonic candidates are **not adequate descriptions of pronounced reversals or stepwise I histories**. Their numerical results are retained as diagnostic failures rather than forcing such lives into a growth category. RMSE, MAE, R², lag-1 residual correlation and early/late residual means are exported. A high R² across a wide birth-to-late range can coexist with systematically wrong late behavior.

### H

'''+modeltable('H_norm')+'''

For H, the exponential envelope has the lowest full-interval RMSE of these candidates in all seven lives; full-fit τ is roughly 605–1252 s and A roughly 0.000259–0.000302. That describes broad concavity, not a demonstrated fixed ceiling. Residual autocorrelation remains about 0.33–0.71. Excluding the first 600 s changes 001's τ from about 685 s to about 757,000 s, and 003's from 975 to 2738 s. The late data do not independently identify the proposed asymptote in those lives. 004/005/006 are more stable under that exclusion; 002/007 remain broadly concave-down but still have reversals. Even a stable envelope cannot guarantee a plateau under a changed experience distribution.

### E bank

'''+modeltable('regulator_theta_E_norm')+'''

There is no common saturating E trajectory. The enormous τ/A estimates for 001 are effectively an unidentifiable long-timescale rise, not an estimate of future capacity. Excluding the first 600 s moves 002's τ from roughly 1999 to 8250 s. 003/005 support slower continuing growth. 004 and 007 are better described as rise followed by oscillation/decline than as steady progress toward a known ceiling. 006's renewed late growth is visibly missed by a single whole-life exponential. Residual serial structure is strong across the E models (roughly 0.77–0.95 for the lowest-RMSE candidates), so none licenses extrapolation.

### I bank

'''+modeltable('regulator_theta_I_norm')+'''

I is event-driven. Some whole-life fits mainly explain when a large damage-associated increase occurred. Excluding early steps can move fitted τ by orders of magnitude or make R² negative. 003 reaches the artificial τ search ceiling; that is failed identification, not a million-second learning timescale. Smooth-model asymptotes are not scientifically interpretable for these step-and-decay curves.

The exponential profile table also records τ values within 10% of the minimum least-squares RMSE on a fixed logarithmic grid. This is a **sensitivity band, not a confidence interval**. A broad band, a large τ, strong residual structure or unstable A/τ after excluding the first 600 s means the observed late data do not constrain a useful asymptote.

[Complete fit table](tables/SHAPE_MODEL_COMPARISON.csv), including all 126 fits. [H residual figure](figures/MODEL_RESIDUALS_H_norm.png), [E residual figure](figures/MODEL_RESIDUALS_regulator_theta_E_norm.png), [I residual figure](figures/MODEL_RESIDUALS_regulator_theta_I_norm.png).

## Structural growth versus functional expression

`H_use_mean` is the arithmetic mean of the 224 stored branch-use statistics; it is not a success fraction. `q_norm` is the norm of the stored associative return. Learned E/I current effects are **intact minus that bank's learned contribution omitted**, at the same recorded exploration draws, need values and other bank. The outer tanh is retained. These exact algebraic receiver effects are not counterfactual movements. The spontaneous comparator is paired M1 RMS at recorded wave motor diagnostics; it precedes the new outgoing regulator controls at that handoff, so the ratio is a scale comparison, not an additive simultaneous trajectory decomposition.

| Life | E effect / M1, early → late | I effect / M1, early → late | q RMS, early → late | Mean H use, early → late |
|---|---:|---:|---:|---:|
'''
for n in range(1,8):
    life=f'RS-M1-{n:03d}';a=next(r for r in fun if r['life']==life and r['band']=='early');b=next(r for r in fun if r['life']==life and r['band']=='late')
    text+=f"| {n:03d} | {float(a['E_current_effect_over_M1'])*100:.3f}% → {float(b['E_current_effect_over_M1'])*100:.3f}% | {float(a['I_current_effect_over_M1'])*100:.3f}% → {float(b['I_current_effect_over_M1'])*100:.3f}% | {fmt(a['q_norm_RMS'],3)} → {fmt(b['q_norm_RMS'],3)} | {fmt(a['H_use_mean_mean'],3)} → {fmt(b['H_use_mean_mean'],3)} |\n"
text+='''
Both q and mean H-use generally rise from the early to late windows; neither is literally flat. **Their absolute scale remains tiny**: late mean use is approximately 4.0×10⁻¹¹–7.6×10⁻¹¹, with q RMS around 1.9×10⁻⁵–2.6×10⁻⁵. The use update is driven by squared branch return divided by 0.01 plus that power; tiny return therefore produces extremely weak use protection. Structural growth accompanied by tiny functional reading is consistent with case E in the request, but the curves alone do not prove that useful associations are being erased.

Late learned-E current effects are approximately **0.22–1.15% of M1 RMS**; learned-I effects are approximately **0.005–0.138%**. These effects increase from early to late for all seven complete lives, but their size remains small. The stored local target sensitivity remains nonzero, so this is not evidence of an entirely blocked receiver. Nor does a nonzero immediate effect establish useful physical control. RS-M1-006 is especially informative: a large late E-bank increase accompanies comparatively weak E-current expression. That makes expression a question to examine, not a diagnosed bottleneck from norm alone.

'''+figure('RS-M1-006_FUNCTIONAL','RS-M1-006 functional expression alongside its structural growth')+'''

[Functional age-band table](tables/FUNCTIONAL_READOUT_BY_AGE.csv). Each organism has its own supplementary five-panel functional figure in the viewer and figure directory.

## Individual curves and bounded readings

'''
for n in range(1,13):
    life=f'RS-M1-{n:03d}';r=next(x for x in summary if x['life']==life)
    text+=f'### {life} — observed through {r["age"]:.6f} s\n\n'
    for label,note in zip(('H','E bank','I bank'),notes[n]):text+=f'**{label}:** {note}\n\n'
    text+=figure(life+'_H_E_I_BODY',life+' measured H/E/I and body-state curves')+f'\n[Functional readouts](figures/{life}_FUNCTIONAL.png) · [raw wave CSV, gzip](raw/{life}_H_E_I_WAVES.csv.gz) · [native body CSV, gzip](raw/{life}_BODY_NATIVE.csv.gz)\n\n'
text+='''## Provenance and consistency review

The source experiment is the non-canonical M1 resurrection sandbox, runtime `752b7c335347a5f55fd3e7cdf1b904137d41e5b229b8ea2252caa8e12a455f3c`, under corrected apparatus checkpoint `1d7cd6fd450ea528562b2c825589ab4de18a5b38`, with historical P identity `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The exact sandbox, M1, configuration and P source hashes are verified against the prepared runtime record.

The original archive is unchanged: **4,653,285,580 bytes**, SHA-256 `a165c5c48e4b9ed6a84a8ba02b7b1bc23ca57f43f38bfe6d0058694969e7e651`. All **37,909 sealed execution files** were rehashed, totaling 4,258,393,873 bytes. The source manifest lists each relative evidence path and exact hash; the review package includes that manifest, not a duplicate of the experiment archive.

An independently coded calculation path recomputed all three norms directly from **807 full checkpoints** and matched the per-wave extraction with maximum absolute error **5.421010862427522×10⁻²⁰**. The extraction also matches the preserved earlier wave history, and every exported native E/I row matches its decoded source value. The priority CSVs contain **184,156 measured waves** and **3,684,048 native body rows plus birth rows**. The difference from the full durable prefix is the explicitly excluded final 29 seconds of RS-M1-008. Physical ledger checks agree with the previous totals. This is a consistency review by the same analyst using independent calculation paths, **not an external or second-person scientific review**.

[Input provenance](INPUT_PROVENANCE.json), [exact evidence manifest](EXECUTION_EVIDENCE_HASHES.json), [source verification](SOURCE_IDENTITY_VERIFICATION.json), [curve consistency review](CURVE_CONSISTENCY_REVIEW.json), [extraction verification](EXTRACTION_VERIFICATION.json).

No simulation, no P invocation, no RNG draw, no checkpoint continuation, no alternate history, no RS-M1-008 retry, no parameter or canonical-code change occurred. All analysis code and derivative files are separate from the preserved evidence. This priority report does not claim completion of the broader developmental causal-chain analysis.

## At the end of the available observation window

**H:** strongly decelerated from birth, generally fluctuating around a broad band; some lives still rise late and others decline. A universal stable asymptote is not established.

**Learned E (`regulator.theta[0]`):** still developmental in several organisms, with continuing or renewed growth; other organisms level, oscillate or decline. It is neither uniformly linear nor uniformly saturated. More time remains a candidate for some structural changes, without evidence that time alone would yield useful control.

**Learned I (`regulator.theta[1]`):** predominantly event-driven, with abrupt increases and intervening decay. Recent large steps can coexist with a negative robust background slope. A smooth saturation claim would be misleading.

**Expression:** learned current, q and use do increase, but remain small in the implemented receiver. Norm growth is not equivalent to useful learning.
'''
(OUT/'H_E_I_DEVELOPMENTAL_CURVES_v0_1.md').write_text(text,encoding='utf8')

items=[]
for key,label in [('POPULATION_H_norm','Population: H'),('POPULATION_regulator_theta_E_norm','Population: E bank'),('POPULATION_regulator_theta_I_norm','Population: I bank'),('LOCAL_SLOPES','Local slopes')]:items.append((key,label))
for n in range(1,13):
    life=f'RS-M1-{n:03d}';items.extend([(life+'_H_E_I_BODY',life+' — H / E / I / body'),(life+'_FUNCTIONAL',life+' — functional readouts')])
for metric,label in [('H_norm','H'),('regulator_theta_E_norm','E bank'),('regulator_theta_I_norm','I bank')]:items.append(('MODEL_RESIDUALS_'+metric,label+' — fits and residuals'))
options=''.join(f'<option value="{key}">{html.escape(label)}</option>' for key,label in items)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Loom — developmental curves</title><style>body{font:16px system-ui;margin:0;background:#eef2f5;color:#203047}header{position:sticky;top:0;background:#fff;padding:16px 24px;box-shadow:0 1px 6px #ccd3da;z-index:2}h1{font-size:23px;margin:0 0 8px}p{margin:6px 0}select,button{font:inherit;padding:8px;margin:6px 8px 0 0}main{max-width:1500px;margin:20px auto;background:white}img{width:100%;height:auto}a{color:#15598b}small{color:#536171}</style><header><h1>H / E / I developmental curves</h1><p>Saved evidence only. Seven complete lives, one censored prefix, four pilots. No simulation or continuation.</p><label for="view">Figure </label><select id="view">'''+options+'''</select><button id="previous">Previous</button><button id="next">Next</button><a href="H_E_I_DEVELOPMENTAL_CURVES_v0_1.md">Full report</a><p><small>Thin raw measurements; dark trailing 60-second mean. Norm growth does not establish useful learning.</small></p></header><main><img id="figure" alt="Population H developmental curves" src="figures/POPULATION_H_norm.png"></main><script>const s=document.getElementById('view'),i=document.getElementById('figure');function show(){i.src='figures/'+s.value+'.png';i.alt=s.options[s.selectedIndex].text;window.scrollTo(0,0)}s.onchange=show;document.getElementById('previous').onclick=()=>{s.selectedIndex=Math.max(0,s.selectedIndex-1);show()};document.getElementById('next').onclick=()=>{s.selectedIndex=Math.min(s.options.length-1,s.selectedIndex+1);show()};</script></html>'''
(OUT/'CURVE_REVIEW.html').write_text(page,encoding='utf8')
save('EXECUTION_EVIDENCE_HASHES.json',SEAL)
print('Priority curve report and passive local viewer written.')
