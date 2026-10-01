"""Read-only checkpoint and import-byte audit; writes only this new review folder."""
import hashlib,json,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
WORKSPACE=OUT.parents[2]
TARGET=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
CURRENT=TARGET/'developmental_ecology'
OLD=WORKSPACE/'exports/2026-09-25-p-apparatus-correction-review-9d31e790/portable/developmental_ecology'
base=['git','-c','safe.directory='+TARGET.as_posix(),'-C',str(TARGET)]
sha='5f07748102cb5eaa302569c87efbae095050e9fe'
groups=[('P_and_configuration','6bc9683b54e4fa80136fe8534d7713e2a250a95f',
         ['developmental_ecology/loom_p','developmental_ecology/configuration.json']),
        ('prior_tests_and_unchanged_controller_adapter','9d31e7902658b15762052a2a6a3d161d64338524',
         ['developmental_ecology/loom_commissioning/controllers.py','developmental_ecology/loom_commissioning/adapter.py',
          'developmental_ecology/tests','developmental_ecology/tests_apparatus/test_apparatus.py',
          'developmental_ecology/tests_apparatus/test_corrections.py'])]
result={'head':subprocess.check_output(base+['rev-parse','HEAD'],text=True).strip(),'comparisons':[],'checkout_bytes':[]}
assert result['head']==sha
for name,old,paths in groups:
    cmd=base+['diff','--exit-code',old,sha,'--',*paths]
    r=subprocess.run(cmd,capture_output=True,text=True)
    assert r.returncode==0 and not r.stdout and not r.stderr
    result['comparisons'].append({'name':name,'command':cmd,'exit':r.returncode,'diff_empty':True})
for file in sorted([*CURRENT.joinpath('loom_p').glob('*.py'),CURRENT/'configuration.json',
                    CURRENT/'loom_commissioning/controllers.py',CURRENT/'loom_commissioning/adapter.py']):
    rel=file.relative_to(CURRENT);raw=file.read_bytes();previous=(OLD/rel).read_bytes()
    assert raw==previous
    result['checkout_bytes'].append({'path':rel.as_posix(),'old_portable_equals_current_raw_bytes':True,
        'sha256':hashlib.sha256(raw).hexdigest()})
for path in sorted((CURRENT/'loom_p').glob('*.py')):
    assert 'loom_commissioning' not in path.read_text(encoding='utf-8')
result['P_has_no_commissioning_import_or_literal']=True
result['all_checks_passed']=True
(OUT/'SOURCE_SCOPE.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
