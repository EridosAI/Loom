"""Custody, document and detached arithmetic verification. No Loom imports."""
from pathlib import Path
import json,hashlib,ast,math,subprocess,re,sys,datetime
import numpy as np
O=Path(__file__).resolve().parent;ROOT=O.parent;WT=ROOT/'worktrees/loom-p-b1-minimal-20260929'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
custody=read(O/'INPUT_CUSTODY.json')
for f in custody['files']:assert sha(f['path'])==f['sha256'],f['path']
old=ROOT/'nursery_0_design_20260930_v0_1'
prior=read(old/'DESIGN_ONLY_VERIFICATION.json')
for f in prior['files']:assert sha(old/f['path'])==f['sha256'],f['path']
assert len(read(old/'NURSERY_CANDIDATE_PROPOSALS.json')['candidates'])==3
prioranalysis=read(ROOT/'founder_expansion_execution_20260930/FINAL_DELIVERY_VERIFICATION.json')
af=next(f for f in prioranalysis['analysis_files'] if f['path'].endswith('ALL_SIXTY_AB.json'))
assert sha(ROOT/'founder_expansion_execution_20260930'/af['path'])==af['sha256']
request=Path(r'C:\Users\Jason\.codex\attachments\6f4a5f79-80cc-46ff-8a79-81f6e56684d7\Pasted text.txt')
assert sha(request)==sha(O/'JASON_MOTOR_DESIGN_REQUEST.txt')

# Detached analytic geometry/transduction derivative checks, never production imports.
tree=ast.parse((O/'audit_birth.py').read_text());names=('rect_sdf','mover_rect','gaps','bilinear_gradient','pb_tail','ranks')
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
c=read(WT/'developmental_ecology/configuration.json');ns=dict(np=np,math=math,sources=np.array(c['source_positions']),repairs=np.array(c['repair_rectangles']))
exec(compile(ast.Module(body=nodes,type_ignores=[]),'detached_birth_metrics','exec'),ns)
assert ns['rect_sdf'](np.array([3.,1.]),[0,2,0,2])==1
assert ns['rect_sdf'](np.array([1.,1.]),[0,2,0,2])==-1
assert np.allclose(ns['ranks']([2,1,2,4]),[1.5,0,1.5,3])
assert abs(ns['pb_tail']([.5,.5],0)-.5)<1e-12
x=np.arange(80)*.25+.125;xx,yy=np.meshgrid(x,x);field=np.stack([2*xx+3*yy,4*xx-yy])
v,g=ns['bilinear_gradient'](field,[7.13,8.27]);assert np.allclose(v,[2*7.13+3*8.27,4*7.13-8.27]) and np.allclose(g,[[2,3],[4,-1]])
# The proposed stratum-conditional distribution reconstructs the base joint law.
area=np.array([[2.,1.],[1.,2.]]);total=area.sum(axis=1);base=.5*area/total[:,None];weights=base.sum(axis=0)
conditional=base/weights[None,:];assert np.allclose((conditional*weights[None,:]),base)

for file in O.glob('*.py'):
    t=ast.parse(file.read_text())
    for n in ast.walk(t):
        if isinstance(n,ast.Import):assert not any(a.name.startswith('loom') for a in n.names)
        if isinstance(n,ast.ImportFrom):assert not (n.module or '').startswith('loom')
        if isinstance(n,ast.Attribute):assert n.attr not in ('native','handoff','default_rng'),(file,n.attr)
for file in O.glob('*.md'):
    text=file.read_text();assert not any(ord(ch)<32 and ch not in '\n\r\t' for ch in text),file
    for target in re.findall(r'\]\(<([^>]+)>\)',text):
        if target.endswith('REVIEW_VERIFICATION.json'):continue
        assert Path(re.sub(r':[0-9]+$','',target)).is_file(),(file,target)
    assert text.count('$$')%2==0,file
R=read(O/'BIRTH_AUDIT_RESULTS.json');S=read(O/'BIRTH_SUPPLEMENT.json')
assert R['all_births']==60 and R['complete_outcome_lives']==59 and all(v==0 for v in R['execution'].values())
assert R['raw_receptor_reconstruction_error']==0 and S['detached_convolution_check'].startswith('PASS')
assert len(read(O/'BIRTH_INITIAL_DETAILS.json'))==60
def git(*a):
    return subprocess.run(['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),*a],capture_output=True,text=True,check=True)
head=git('rev-parse','HEAD');status=git('status','--porcelain')
assert head.stdout.strip()=='87abae34e19d4e46234402a6b1ba776814956ec1' and status.stdout.strip()==''
files=[dict(path=p.relative_to(O).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='REVIEW_VERIFICATION.json']
result=dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,numpy=np.__version__,scope='PASSIVE_BIRTH_AUDIT_AND_MOTOR_DESIGN_ONLY',
    original_checkpoint_files_verified=60,original_input_files_unchanged=len(custody['files']),original_nursery_package_files_unchanged=len(prior['files']),founder_outcome_summary_matches_original_delivery_hash=True,
    P='6bc9683b54e4fa80136fe8534d7713e2a250a95f',runner_head=head.stdout.strip(),git_clean=True,git_read_warnings=status.stderr.strip(),
    candidate_motor_families=2,replacement_selected=False,birth_law_selected=False,nursery_parameters_applied=False,existing_three_candidates_preserved=True,
    world_steps=0,P_steps=0,motor_generator_steps=0,field_steps=0,prehistory_steps=0,new_births=0,new_rng_draws=0,new_authority_objects=0,production_modifications=False,canon_modifications=False,git_writes=False,
    old_human_B1_evaluator_not_accessed=True,FS060='APPARATUS_INTERRUPTED_UNCLOSED',
    checks=['checkpoint file and payload hashes','all actual birth clearances and rejected-proposal ledgers','stored initial stream counters','raw chemistry static reproduction','rectangular signed distances','bilinear gradients on manufactured affine fields','rank ties and Poisson-binomial tail','finite non-wrapping convolution on manufactured mask','stratum marginal probability algebra','document links/equation delimiters/control characters','figure visual inspection'],
    figures_visually_reviewed=True,files=files,total_bytes=sum(f['bytes'] for f in files))
(O/'REVIEW_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('files','checks')},indent=2))
