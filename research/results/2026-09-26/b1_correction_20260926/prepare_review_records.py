"""Documentation/custody only. No Engine, controller, snapshot loading or run."""
import hashlib,importlib.metadata,json,os,pathlib,subprocess,sys,xml.etree.ElementTree as ET
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
DOC=W/'docs/developmental_ecology/p_b1_operator_correction_20260926'
H=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
BASE='68db2c581f07200966d699a4f55a65f9b96df1e9';P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
sys.path.insert(0,str(D))
from loom_commissioning.authority import runtime_identity
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):p.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)

# These checks read file bytes and Git blobs; no private snapshot is decoded.
protected=json.loads((S/'P_CONFIG_WORLD_UNCHANGED.json').read_bytes())
for name,value in protected['byte_identical_files'].items():
    assert sha(D/name)==value
    relative='developmental_ecology/'+name.replace('\\','/')
    assert git('hash-object','--path='+relative,str(D/name)).strip()==git('rev-parse',BASE+':'+relative).strip()
p_names=[n for n in protected['byte_identical_files'] if n.startswith('loom_p') or n=='configuration.json']
for name in p_names:
    relative='developmental_ecology/'+name.replace('\\','/')
    assert git('hash-object','--path='+relative,str(D/name)).strip()==git('rev-parse',P+':'+relative).strip()
held=json.loads((S/'HELD_PRESERVATION_BEFORE.json').read_bytes())
assert all(sha(pathlib.Path(path))==value for path,value in held.items())
protected['original_P_checkpoint_blob_comparisons']=len(p_names)
protected['parent_checkpoint_blob_comparisons']=len(protected['byte_identical_files'])
protected['git_comparison_method']='Read-only git hash-object (without -w), using existing path filters, compared to committed blob IDs. Configuration checkout has existing CRLF versus LF Git storage; no file rewritten. Parent worktree bytes also match exactly.'
protected['held_before_inventory_sha256']=sha(S/'HELD_PRESERVATION_BEFORE.json')
write(S/'FINAL_PRESERVATION.json',protected)

portable=json.loads((S/'PORTABLE_SOURCE_IDENTITIES.json').read_bytes())
for name,value in portable.items():
    assert sha(D/name)==sha(S/'portable-source/developmental_ecology'/name)==value
tested=json.loads((S/'fault-matrix-sealed/TESTED_SOURCE_IDENTITIES.json').read_bytes())
assert all(sha(D/name)==value for name,value in tested.items())
rows=[]
for label in ('REGRESSION_FIRST','NEW_FIRST','FINAL_REGRESSION','CHECKPOINT_REGRESSION','SEALED_REGRESSION','PORTABLE_REGRESSION'):
    suite=ET.parse(S/(label+'.xml')).getroot().find('testsuite')
    assert suite.attrib['failures']=='0' and suite.attrib['errors']=='0'
    rows.append(dict(label=label,**suite.attrib,log_sha256=sha(S/(label+'.log')),junit_sha256=sha(S/(label+'.xml'))))
assert rows[-1]['tests']==rows[-2]['tests']=='204'
matrices=[]
for name in ('fault-matrix','fault-matrix-final','fault-matrix-sealed'):
    value=json.loads((S/name/'RED_GREEN_MATRIX.json').read_bytes())
    assert len(value['rows'])==12 and all(r['verified'] for row in value['rows'] for r in row['runs'])
    matrices.append(dict(directory=name,verified_pairs=12,matrix_sha256=sha(S/name/'RED_GREEN_MATRIX.json')))
results=dict(final_worktree=dict(tests=204,passed=204,reported_seconds=143.82),
    final_portable=dict(tests=204,passed=204,reported_seconds=143.73),baseline_expected_failures=2,
    final_fault_matrix=dict(expected_RED_assertion_failures=12,GREEN_passes=12),all_regression_logs=rows,all_fault_matrix_runs=matrices,
    final_source_matches_portable=True,final_source_matches_fault_matrix=True,
    tests_kind='manufactured/components; no prepared positive-control/B1/ecological case',
    reconstruction_scope='existing component regressions and paired manufactured records only; no ecological replay')
write(S/'REGRESSION_RESULTS.json',results)

node=pathlib.Path(r'C:\Program Files\nodejs\node.exe')
runtime=runtime_identity()
runtime.update(python_executable=str(pathlib.Path(sys.executable).resolve()),node_version=subprocess.check_output([str(node),'--version'],text=True).strip(),
    node_executable_sha256=sha(node),test_packages={name:importlib.metadata.version(name) for name in ('pytest','colorama','iniconfig','packaging','pluggy','pygments')},
    dependencies_installed_this_task=False,network_fetches=False,execution_environment='Actual Windows local filesystem and executable processes; not a cloud copy')
write(S/'RUNTIME_RECORD.json',runtime)

ui=dict(kind='synthetic browser appearance and interaction; no world/Engine/controller',
    observed_html_sha256=sha(S/'BROWSER_OBSERVED_SENSOR.html'),final_html_sha256=sha(D/'loom_commissioning/sensor.html'),
    actual_browser='Codex in-app browser, temporary local tab',invented_history=True,fixed_simulated_time=0.4,
    observations=['PREPARED, command disabled','Start -> PAUSED without time change','double click -> one synthetic POST; RUNNING while delayed response',
                  'return PAUSED, one fake command only','refresh -> PAUSED with one fake command','End -> ENDED with disabled controls'],
    late_change='Fast second-click and held-key suppression added after direct browser inspection; covered in final detached Node DOM test.',
    screenshot_saved=False,synthetic_server_final_receipt_saved=False,
    temporary_tab_closed=True,temporary_server_stopped=True,loopback_port_closed_verified=True,
    commissioning_or_positive_control_run=False,limits='Synthetic transport is not physical integration or human competence evidence; direct inspection and final automated DOM checks are distinct.')
write(S/'UI_REVIEW.json',ui)

request=pathlib.Path(r'C:\Users\Jason\.codex\attachments\832f5af3-01d7-417d-83b2-4e889158997a\Pasted text.txt')
wb=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
sources=[request,ROOT/'AGENTS.md',ROOT/'sources/00_LOOM_CURRENT_STATE(2).md',wb/'AGENTS.md',wb/'00_RESEARCH_MAP.md',wb/'01_WORKSPACE_STATUS.md',
 ROOT/'exports/2026-09-23-p-commissioning-design-2fb3ff84/PACKAGE/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md']
sources+=sorted((H/'B1_OPERATOR_REVIEW').glob('*'))
write(S/'SOURCE_IDENTITIES.json',dict(request_sha256=sha(request),held_review_hash='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543',
    public_sources=[dict(filename=p.name,original_path=str(p),sha256=sha(p)) for p in sources if p.is_file()],
    private_sources='Held package bytes inventoried privately; sealed manifests treated as inert JSON; snapshots hashed only. Private contents and detailed fixture inventory are excluded from this delivery.'))

ledger=dict(commissioning_cases_executed=0,prepared_positive_controls_executed=0,B1_FULL_RAW_executed=0,B1_CHEMISTRY_HIDDEN_executed=0,
    ecological_trajectories_executed=0,ecological_replays=0,new_prehistory=0,new_B1_launch_authorities=0,
    component_tests_executed=True,manufactured_record_reconstruction=True,
    scope='All stepping and reconstruction in this correction is in authorized component/manufactured tests; static held checks do not construct a Run.',
    earlier_evidence='No A1-A5 output changed, rerun or replayed; original checkpoints and interpretations preserved.',
    browser='Invented data and synthetic transport only; no feedback into a simulation.',
    local_git='New isolated code worktree and scoped local commit only; no vault Git, push, PR, merge or history rewrite.',
    authority_boundary='Stop for independent narrow correction review. Historical held B1 remains non-launchable; later regeneration and new authorization are separate.')
write(S/'EXECUTION_SCOPE_RECORD.json',ledger)
for name in ('REGRESSION_RESULTS.json','P_CONFIG_WORLD_UNCHANGED.json','FINAL_PRESERVATION.json','STATIC_HELD_COMPATIBILITY.json','RUNTIME_RECORD.json','UI_REVIEW.json','SOURCE_IDENTITIES.json','EXECUTION_SCOPE_RECORD.json'):
    (DOC/name).write_bytes((S/name).read_bytes())
print('Documentation evidence verified: 204 + 204 final tests; 12 final fault/control pairs; original P/config, parent clock/world and 124 held files unchanged.')
