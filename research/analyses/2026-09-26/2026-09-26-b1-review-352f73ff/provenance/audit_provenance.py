"""Read-only source/custody audit. Hidden snapshots are hashed only, never decoded."""
from pathlib import Path
import ast,hashlib,json,os,subprocess,sys,zipfile,collections,shutil,importlib.metadata
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97');O=W/'exports/2026-09-26-b1-review-352f73ff/provenance';Z=O.parent/'portable'
T=W/'worktrees/loom-p-b1-apparatus-correction-20260926';D=T/'developmental_ecology';OLD=W/'worktrees/loom-p-clock-correction-20260926'
H=W/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'; BASE='68db2c581f07200966d699a4f55a65f9b96df1e9';HEAD='352f73fffa6d9781eae8aa38e708a9a05669588f'
def read(p):return json.loads(p.read_bytes())
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def ident(p):return {'sha256':sha(p),'bytes':p.stat().st_size}
def save(n,d):(O/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(n,flush=True)
(O/'empty-excludes').write_bytes(b'')
def git(*args,root=T):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+root.as_posix(),'-c','core.excludesFile='+(O/'empty-excludes').as_posix(),'-C',str(root),*args],cwd=root,env=env)
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','HEAD^').decode().strip()==BASE
assert git('merge-base',P,HEAD).decode().strip()==P
patch=git('diff','--binary','--full-index',BASE,HEAD,'--');delivered=Z/'EXACT_DIFF_68db2c58_to_352f73ff.patch'
assert patch==delivered.read_bytes()
change=git('diff','--name-status',BASE,HEAD).decode().splitlines()
unchanged={n:not git('diff','--name-only',P,HEAD,'--','developmental_ecology/'+n).strip() for n in ['loom_p','configuration.json','requirements-lock.txt','tests']}
unchanged.update({n:not git('diff','--name-only',BASE,HEAD,'--','developmental_ecology/'+n).strip() for n in ['loom_commissioning/adapter.py','loom_commissioning/clock.py','loom_commissioning/diagnostics.py','loom_commissioning/evaluation.py','loom_commissioning/initialization.py']})
assert all(unchanged.values())
exp={r:git('rev-parse',r+':EXP1-21').decode().strip() for r in [P,BASE,HEAD]};assert len(set(exp.values()))==1
modules={p.name:git('show',HEAD+':developmental_ecology/loom_commissioning/'+p.name)==p.read_bytes() for p in (D/'loom_commissioning').glob('*.py')};assert all(modules.values())
save('GIT.json',{'HEAD':HEAD,'parent':BASE,'P_ancestor':P,'branch':git('branch','--show-current').decode().strip(),'target_status':git('status','--porcelain').decode(),'old_HEAD':git('rev-parse','HEAD',root=OLD).decode().strip(),'old_status':git('status','--porcelain',root=OLD).decode(),'diff_files':change,'stat':git('diff','--stat',BASE,HEAD).decode(),'patch':{'bytes':len(patch),'sha256':hashlib.sha256(patch).hexdigest(),'package_exact':True},'unchanged':unchanged,'EXP1-21_trees':exp,'apparatus_python_committed_blob_equal':modules})
# Full package verified by extraction; compare original archive manifest and actual source bytes.
archive=W/'exports/2026-09-26-B1-operator-correction-352f73ff/B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip'
oldreceipt=read(archive.parent/'ARCHIVE_RECEIPT.json');assert sha(archive)==oldreceipt['archive_sha256'];assert archive.stat().st_size==oldreceipt['archive_bytes']
prefix='B1_OPERATOR_APPARATUS_CORRECTION_REVIEW/'
latest=read(Z/'PAYLOAD_MANIFEST.json')['files']
with zipfile.ZipFile(archive) as z:
    original_raw=z.read(prefix+'PAYLOAD_MANIFEST.json');assert hashlib.sha256(original_raw).hexdigest()==oldreceipt['manifest_sha256']
    original=json.loads(original_raw)['files'];common=set(original)&set(latest)
    differences={n:{'original':original[n],'review02':latest[n]} for n in sorted(common) if original[n]!=latest[n]}
    source_names=[n for n in common if n.startswith(('source/','baseline-68db/'))]
    verified_original_sources=[]
    for n in source_names:
        data=z.read(prefix+n)
        assert hashlib.sha256(data).hexdigest()==original[n]['sha256']
        assert data==(Z/n).read_bytes(),n
        verified_original_sources.append(n)
removed=sorted(set(original)-set(latest));added=sorted(set(latest)-set(original))
save('DELIVERY_COMPARISON.json',{'original_archive':{'path':str(archive),**ident(archive)},'original_payload_count':len(original),'review02_payload_count':len(latest),'common':len(common),'changed_common_entries':differences,'removed':removed,'added':added,'actual_original_source_baseline_payloads_equal':verified_original_sources,'original_non_source_payloads_not_expanded':True})
# Match entire delivered source inventories; retain pre-test target/portable baselines.
before={};sourcecheck={};baselinecheck={}
for n,v in latest.items():
    before[str(Z/n)]=v
    if n.startswith('source/'):
        rel=n[len('source/'):];actual=ident(T/rel);sourcecheck[rel]={'expected':v,'actual':actual,'equal':actual==v};before[str(T/rel)]=actual
    elif n.startswith('baseline-68db/'):
        rel=n[len('baseline-68db/'):];actual=ident(OLD/rel);baselinecheck[rel]={'expected':v,'actual':actual,'equal':actual==v};before[str(OLD/rel)]=actual
assert all(x['equal'] for x in sourcecheck.values());assert all(x['equal'] for x in baselinecheck.values())
save('SOURCE_MATCH.json',{'current_count':len(sourcecheck),'baseline_count':len(baselinecheck),'current':sourcecheck,'baseline':baselinecheck})
protected=read(Z/'docs/FINAL_PRESERVATION.json')['byte_identical_files'];proof={}
for n,h in protected.items():
    proofs={'current':sha(D/n),'parent':sha(OLD/'developmental_ecology'/n),'portable':sha(Z/'source/developmental_ecology'/n),'baseline_portable':sha(Z/'baseline-68db/developmental_ecology'/n)}
    assert set(proofs.values())=={h};proof[n]=proofs
save('PROTECTED.json',{'files':proof,'count':len(proof)})
# AST preservation of causal controller functions and constants.
new=ast.parse((D/'loom_commissioning/controllers.py').read_text());old=ast.parse((OLD/'developmental_ecology/loom_commissioning/controllers.py').read_text())
funcs=['command_pair','waypoint_command','waypoint_stage','time_due','validate_plan','privileged_input','observe_without_interference']
def fn(tree,n):return ast.dump(next(x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name==n),include_attributes=False)
astmatches={n:fn(new,n)==fn(old,n) for n in funcs}
def gain(tree):return next(ast.literal_eval(x.value) for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='WAYPOINT_SETTINGS' for t in x.targets))
assert all(astmatches.values()) and gain(new)==gain(old)
save('CAUSAL_AST.json',{'functions':astmatches,'gains_unchanged':True,'gains':gain(new)})
# Original held inventory includes sealed files: use streaming hashes only.
held_inventory_path=W/'b1_correction_20260926/HELD_PRESERVATION_BEFORE.json';heldmap=read(held_inventory_path)
assert sha(held_inventory_path)==read(Z/'docs/FINAL_PRESERVATION.json')['held_before_inventory_sha256']
held_results={}
for p,h in heldmap.items():
    actual=ident(Path(p));assert actual['sha256']==h,p
    held_results[p]=actual;before[p]=actual
save('HELD_PRESERVATION.json',{'inventory':str(held_inventory_path),'inventory_sha256':sha(held_inventory_path),'files_checked':len(held_results),'all_unchanged':True,'files':held_results,'sealed_content_decoded':False})
# Public source identities only; do not print or decode private source files.
public=read(Z/'docs/SOURCE_IDENTITIES.json')['public_sources'];public_results=[]
for row in public:
    path=Path(row['original_path']);actual=sha(path)
    public_results.append({'path':str(path),'expected':row['sha256'],'actual':actual,'equal':actual==row['sha256']});before[str(path)]=ident(path)
save('PUBLIC_SOURCE_IDENTITIES.json',{'count':len(public_results),'files':public_results})
# Import inspected identity/pure metadata functions only; no Engine or Run construction.
sys.path.insert(0,str(D))
from loom_p.records import code_identity
from loom_p.schema import Config
from loom_commissioning.contract import apparatus_identity
from loom_commissioning.authority import runtime_identity
runtime=runtime_identity();record=read(Z/'docs/RUNTIME_RECORD.json')
assert all(record[k]==v for k,v in runtime.items())
node=Path(shutil.which('node'));node_version=subprocess.check_output([str(node),'--version']).decode().strip()
assert sha(node)==record['node_executable_sha256'] and node_version==record['node_version']
packages={n:importlib.metadata.version(n) for n in record['test_packages']};assert packages==record['test_packages']
save('CURRENT_IDENTITIES.json',{'P':code_identity(),'apparatus':apparatus_identity(),'configuration_semantic':Config().identity(),'configuration_file':ident(D/'configuration.json'),'runtime':runtime,'runtime_matches_builder':True,'node':{'path':str(node),'version':node_version,**ident(node)},'test_packages':packages})
save('BEFORE_FILE_IDENTITIES.json',before)
print('Read-only audit completed. No hidden file contents emitted.')
