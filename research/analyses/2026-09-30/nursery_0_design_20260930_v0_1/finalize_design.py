"""Final documentation edits and read-only custody verification; no Loom imports."""
from pathlib import Path
import hashlib,json,re,subprocess,datetime,ast,math
import numpy as np
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
WT=ROOT/'worktrees/loom-p-b1-minimal-20260929'
def read(p):return json.loads(Path(p).read_text())
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()
def link(name,label=None):return f'[{label or name}](<{(OUT/name).as_posix()}>)'
def write(name,t):(OUT/name).write_text(t.strip()+'\n',encoding='utf-8')

main=(OUT/'NURSERY_0_DESIGN_v0_1.md').read_text()
main=main.replace('N0-B: balanced runway **recommended**','N0-B: balanced runway **conditional preference**')
main=main.replace('NURSERY_0_STATIC_LAYOUT.svg','NURSERY_0_LAYOUT_REVIEW.png')
main=main.replace('All computations in this task are saved-summary statistics, scalar accounting or static geometry.', 'All computations in this task are passive statistics from preserved native records and summaries, scalar accounting, static geometry, detached observer-metric checks on manufactured arrays, or document/figure rendering. The passive audit reads saved trajectories without advancing or reconstructing a world.')
if '![Passive exploration audit:' not in main:
    main=main.replace('## Exploration audit additions','## Exploration audit additions\n\n![Passive exploration audit: paths grow while spatial coverage stays local; movement direction reverses despite persistent body heading.](<'+(OUT/'EXPLORATION_DYNAMICS.png').as_posix()+'>)\n\n'+link('EXPLORATION_DYNAMICS.svg','Vector figure')+'; numerical tables and definitions are linked below.\n')
write('NURSERY_0_DESIGN_v0_1.md',main)
audit=(OUT/'NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md').read_text()
if 'Median command R²' not in audit:
    audit=audit.replace('No learned coefficients are supplied to an organism.', 'No learned coefficients are supplied to an organism. Median command R² is **0.93294 (left, 7 s) and 0.93328 (right, 9 s)** over whole lives, and **0.94212 / 0.94229** in the first 60 s. The sampled heading span over a life is median **1.227 rad** (range 0.796–2.056), despite 26.51 rad of absolute accumulated angular motion. This supports heading oscillation rather than continuous full-circle spinning; span is from 0.1 s display samples, so it is a sampled bound.')
    audit=audit.replace('Reversal sensitivity at 0.005, 0.01 and 0.02 speed deadbands is retained', 'Median reversal counts at 0.005, 0.01 and 0.02 speed deadbands are **99, 94 and 82**; median forward-bout durations are **3.640, 3.395 and 2.925 s**. Full reversal sensitivity is retained')
    audit += '\n\n## Passive figure\n\n![Saved-record exploration metrics show repeated reversal and slowing coverage growth.](<'+(OUT/'EXPLORATION_DYNAMICS.png').as_posix()+'>)\n\n'+link('EXPLORATION_DYNAMICS.svg','Vector figure')+'; '+link('EXPLORATION_PER_LIFE.csv','all per-life numbers')+'; '+link('EXPLORATION_COVERAGE_MSD_BY_AGE.csv','coverage and MSD by age')+'; '+link('EXPLORATION_CORRELATIONS_MSD_BY_LAG.csv','correlations and lag-MSD')+'.\n'
write('NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md',audit)

manifest=read(OUT/'SOURCE_MANIFEST.json')
for item in manifest['sources']:assert sha(item['path'])==item['sha256'],item['path']
add=OUT/'JASON_EXPLORATION_ADDENDUM.md'
manifest['exploration_addendum']=dict(path=add.as_posix(),sha256=sha(add),provenance='Verbatim user instruction received in this chat; not a launch approval')
write('SOURCE_MANIFEST.json',json.dumps(manifest,indent=2))

# Preserve every candidate value; only recommendation metadata may change.
prior=read(OUT/'provisional_pre_exploration/NURSERY_CANDIDATE_PROPOSALS.json')
now=read(OUT/'NURSERY_CANDIDATE_PROPOSALS.json')
assert now['candidates']==prior['candidates'] and len(now['candidates'])==3

# Metric component checks use manufactured arrays only, never a body/world.
src=ast.parse((OUT/'audit_exploration.py').read_text())
functions=[x for x in src.body if isinstance(x,ast.FunctionDef) and x.name in ('runs','bouts','grid_metrics','correlation_curves','firstcross')]
ns={'np':np,'math':math}
exec(compile(ast.Module(body=functions,type_ignores=[]),'detached_observer_functions','exec'),ns)
dt=np.full(200,.01)
assert ns['bouts'](np.ones(200),dt,.01)['reversals']==0
assert abs(ns['bouts'](np.ones(200),dt,.01)['forward_max']-2)<1e-12
b=ns['bouts'](np.r_[np.ones(100),-np.ones(100)],dt,.01);assert b['reversals']==1
grid,_=ns['grid_metrics'](np.array([[.1,.1],[.2,.1],[1.2,.1],[.1,.1]]),1.)
assert grid['visited']==2 and grid['transitions']==2 and grid['return_fraction']==.5
tt=np.arange(5000)*.01;pos=np.column_stack([tt,np.zeros(len(tt))]);vel=np.column_stack([np.ones(len(tt)),np.zeros(len(tt))])
curve=ns['correlation_curves'](pos,np.zeros(len(tt)),vel)
row=next(x for x in curve if x['lag_s']==2.)
assert abs(row['time_averaged_msd']-4)<1e-12 and row['heading_acf']==row['direction_acf']==1.

# Recheck historical scientific custody and both previous analysis deliveries.
old=ROOT/'impact_integrity_analysis_20260930_v0_1'
custody=read(old/'INPUT_CUSTODY.json')
for x in custody['scientific_files']:assert sha(x['path'])==x['sha256'],x['path']
prev=ROOT/'founder_expansion_execution_20260930'
priorcheck=read(prev/'FINAL_DELIVERY_VERIFICATION.json')
for x in priorcheck['analysis_files']:assert sha(prev/x['path'])==x['sha256'],x['path']
assert sha(prev/'FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md')==priorcheck['final_report_sha256']
impcheck=read(old/'FINAL_VERIFICATION.json')
for x in impcheck['files']:assert sha(old/x['path'])==x['sha256'],x['path']
archives=[]
for b in (ROOT/'founder_initial_execution_20260930',prev):
    ar=read(b/'ARCHIVE_VERIFICATION.json');assert sha(ar['path'])==ar['sha256'];archives.append(dict(path=ar['path'],sha256=ar['sha256']))
git_warnings=[]
def git(*args):
    cmd=['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),*args]
    result=subprocess.run(cmd,capture_output=True,text=True,check=True)
    if result.stderr.strip():git_warnings.append(result.stderr.strip())
    return result.stdout.strip()
assert git('rev-parse','HEAD')=='87abae34e19d4e46234402a6b1ba776814956ec1'
assert git('status','--porcelain')==''

checks=read(OUT/'EXPLORATION_AUDIT_RESULTS.json')['checks']
assert checks['native_steps_read']==2547923 and checks['native_files_verified']==25503
assert read(OUT/'EXPLORATION_AUDIT_RESULTS.json')['n_no_contact']==50
assert read(OUT/'EXPLORATION_SUPPLEMENT.json')['heading_no_1e_crossing_whole_record_through_120s']==59
for path in OUT.glob('*.md'):
    t=path.read_text()
    assert not re.search(r'@[A-Z_]+@',t),path
    for target in re.findall(r'\]\(<([^>]+)>\)',t):
        if target.endswith('DESIGN_ONLY_VERIFICATION.json'):continue
        assert Path(re.sub(r':[0-9]+$','',target)).exists(),(str(path),target)

write('README.md',f'''# Nursery-0 design review package

**Design only; exploration addendum incorporated.**

Start with {link('NURSERY_0_DESIGN_v0_1.md')}. The passive audit supports reviewing blind spontaneous-motor temporal structure before locking nursery geometry. All three exact provisional ecology/runway candidates remain unchanged; N0-B is the conditional preference only if Jason keeps the current motor process.

- {link('CURRENT_WORLD_DEVELOPMENTAL_EVIDENCE.md')}
- {link('INTEGRITY_PATHWAY_EVIDENCE_SUMMARY.md')}
- {link('NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md')}
- {link('NURSERY_CANDIDATE_PROPOSALS.json')}
- {link('LEAN_RUNNER_RESOURCE_ESTIMATE.md')}
- {link('DESIGN_ARITHMETIC.json')}
- {link('EXPLORATION_DYNAMICS.png','Exploration figure')}
- {link('NURSERY_0_LAYOUT_REVIEW.png','Provisional geometry')}
- {link('DESIGN_ONLY_VERIFICATION.json','Custody and scope verification')}

The pre-addendum draft is preserved in `provisional_pre_exploration/`. Scripts here only derive or render review documents and passive metrics. Do not rerun document writers casually: the historical drafting stages are retained for provenance. There is no launch command, runnable nursery configuration, authority object or prepared birth in this package.

Zero P, motor-generator, world or field execution. No parameter application, code/canon change, founder selection or FS-060 retry. Stop for Jason review.
''')
files=[dict(path=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='DESIGN_ONLY_VERIFICATION.json']
result=dict(status='PASS',date_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='DESIGN_ONLY_WITH_PASSIVE_NATIVE_EXPLORATION_AUDIT',
    P_commit='6bc9683b54e4fa80136fe8534d7713e2a250a95f',runner_checkpoint='87abae34e19d4e46234402a6b1ba776814956ec1',git_clean=True,git_warnings=git_warnings,
    scientific_files_unchanged=len(custody['scientific_files']),previous_founder_analysis_files_unchanged=len(priorcheck['analysis_files']),previous_impact_files_unchanged=len(impcheck['files']),archives_unchanged=archives,
    source_references_verified=len(manifest['sources']),candidate_count=3,all_candidate_values_preserved_from_pre_addendum_draft=True,
    exploration_checks=checks,detached_observer_component_checks='PASS: straight motion, reversal, reentry, MSD and correlations',
    P_steps=0,motor_generator_calls=0,world_steps=0,field_steps=0,prehistory_steps=0,new_rng_draws=0,new_births=0,new_launch_authorities=0,
    production_code_modified=False,current_configuration_modified=False,canon_modified=False,no_founder_selection=True,FS060='APPARATUS_INTERRUPTED_UNCLOSED',
    no_git_writes=True,no_push_PR_merge=True,no_dependency_install=True,figures_visually_reviewed=True,
    bytes=sum(x['bytes'] for x in files),files=files)
write('DESIGN_ONLY_VERIFICATION.json',json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ('files','archives_unchanged')},indent=2))
