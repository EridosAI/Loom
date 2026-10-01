"""Audit saved 72 logs; collect current tests without executing any test bodies."""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
REVIEW=HERE.parent
TARGET=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def summary(text):
    lines=[x.strip() for x in text.splitlines() if re.search(r'\b\d+ (passed|failed|error|errors|collected)\b',x) and ' in ' in x]
    assert lines, 'missing pytest result summary'
    s=lines[-1]
    return {'text':s,'failed':int((re.search(r'(\d+) failed',s) or [None,'0'])[1]),
        'passed':int((re.search(r'(\d+) passed',s) or [None,'0'])[1]),
        'errors':int((re.search(r'(\d+) errors?',s) or [None,'0'])[1])}

result={'scope':'Saved log audit only plus one pytest --collect-only invocation; no tests rerun.',
        'checkpoint':'9d31e7902658b15762052a2a6a3d161d64338524','pairs':[]}
for group,folder in [('previous_16','old-pairs-001'),('correction_20','new-pairs-001')]:
    base=REVIEW/folder; matrix=base/'FAULT_MATRIX.json'
    declared=json.loads(matrix.read_bytes())
    for item in declared:
        fault=item['fault']; intended=item['intended_failure']; red=base/(fault+'-RED.log'); green=base/(fault+'-GREEN.log')
        red_text=red.read_text(encoding='utf-8-sig'); green_text=green.read_text(encoding='utf-8-sig')
        error_lines=[x.strip() for x in red_text.splitlines() if re.match(r'^E\s+(?:AssertionError|ValueError|RuntimeError|ArithmeticError):',x)]
        reached=[x for x in error_lines if intended in x]
        red_summary=summary(red_text); green_summary=summary(green_text)
        assert reached, (fault,'message appears only outside reached exception',error_lines)
        assert item['RED']['exit']==1 and red_summary['failed']>=1 and not red_summary['errors']
        assert item['GREEN']['exit']==0 and green_summary['passed']>=1 and not green_summary['failed'] and not green_summary['errors']
        assert not re.search(r'^E\s+(?:AssertionError|ValueError|RuntimeError|ArithmeticError):',green_text,re.M)
        frames=[x.strip() for x in red_text.splitlines() if re.match(r'^(?:tests_apparatus|loom_commissioning)[\\/].*:\d+:',x)]
        if fault.startswith('authority-'):
            injection='test callback bypass only: check=lambda:None; production verify_approval_binding is not patched'
            assert "check=(lambda:None) if fault('authority-'+name)" in red_text
            assert any('test_corrections.py:83:' in x for x in frames)
        elif fault.startswith('clock-'):
            injection='in-memory production controllers.time_due replacement with old raw >= comparison'
            assert "patch.object(controllers,'time_due',old_due" in red_text
        else:
            injection='existing test-side data or operation fault at the named fixture; production guard/assertion exercised'
        for color in ('RED','GREEN'):
            cmd=item[color]['command']
            assert '-B' in cmd and 'no:cacheprovider' in cmd and '--basetemp' in cmd
        result['pairs'].append({'group':group,'fault':fault,'test':item['test'],
            'intended_failure':intended,'injection_mechanism':injection,
            'red_exception_lines':reached,'red_trace_frames':list(dict.fromkeys(frames)),
            'red_summary':red_summary,'green_summary':green_summary,
            'red_exit':item['RED']['exit'],'green_exit':item['GREEN']['exit'],
            'red_log':str(red.relative_to(REVIEW)),'green_log':str(green.relative_to(REVIEW)),
            'red_sha256':sha(red),'green_sha256':sha(green),
            'reached_intended_exception':True,'clean_control_passed':True})
assert len(result['pairs'])==36
clock=next(x for x in result['pairs'] if x['fault']=='clock-transition')
assert clock['red_summary']['failed']==2 and clock['red_summary']['passed']==3 and clock['green_summary']['passed']==5

# No test bodies execute. Disable inherited options/plugin/bytecode effects and
# direct every possible temporary output into a fresh directory in this review.
temp=Path(tempfile.mkdtemp(prefix='collect-only-',dir=HERE))
env=os.environ.copy()
for key in ('PYTEST_ADDOPTS','PYTHONPATH','APPARATUS_FAULT','CORRECTION_FAULT'): env.pop(key,None)
env.update(PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',TEMP=str(temp),TMP=str(temp))
command=[sys.executable,'-B','-m','pytest','tests','tests_apparatus','--collect-only','-q','-p','no:cacheprovider','--basetemp',str(temp/'pytest')]
proc=subprocess.run(command,cwd=TARGET,env=env,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(HERE/'collect-only.log').write_text(proc.stdout,encoding='utf-8')
assert proc.returncode==0, proc.stdout
nodes=[x.strip().replace('\\','/') for x in proc.stdout.splitlines() if re.match(r'^(tests|tests_apparatus)[\\/].*::test_',x)]
composition={'P_engineering':sum(x.startswith('tests/') for x in nodes),
    'previous_apparatus':sum(x.startswith('tests_apparatus/test_apparatus.py::') for x in nodes),
    'new_correction':sum(x.startswith('tests_apparatus/test_corrections.py::') for x in nodes)}
assert composition=={'P_engineering':59,'previous_apparatus':24,'new_correction':30},composition
assert len(nodes)==113
result['collection']={'exit':proc.returncode,'command':command,'cwd':str(TARGET),'temp':str(temp),
    'plugin_autoload_disabled':True,'bytecode_disabled':True,'pytest_cache_disabled':True,
    'collected_total':len(nodes),'composition':composition,'log':'authority_runtime/collect-only.log',
    'log_sha256':sha(HERE/'collect-only.log'),'test_bodies_executed':0}
result['suite_logs']={}
for name in ('worktree-suite.log','portable-suite.log'):
    path=REVIEW/name; s=summary(path.read_text(encoding='utf-8-sig'))
    assert s['passed']==113 and not s['failed'] and not s['errors']
    result['suite_logs'][name]={'summary':s,'sha256':sha(path)}
result['summary']={'pairs':36,'red_logs':36,'green_logs':36,'total_logs_audited':72,
    'all_reds_reach_intended_exception':True,'all_green_controls_pass':True,
    'red_test_failures':sum(x['red_summary']['failed'] for x in result['pairs']),
    'red_test_passes':sum(x['red_summary']['passed'] for x in result['pairs']),
    'green_test_passes':sum(x['green_summary']['passed'] for x in result['pairs']),
    'authority_callback_bypass_pairs':18,'production_clock_comparison_pairs':2,'previous_pairs':16,
    'important_qualification':'18 authority REDs bypass a test callback, not a production implementation. They establish assertion sensitivity; clean controls exercise real rejection. Clock-transition RED has 2 failed/3 passed parameter cases; GREEN has 5 passed.'}
(HERE/'SUITE_AND_FAULT_AUDIT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

table=['# Independent suite and 36-pair log audit','',
    'No test bodies were rerun. This audit read all 72 saved RED/GREEN logs and performed one collect-only invocation in the pinned environment.','',
    '| Group | Pairs | Reached RED result | Clean GREEN result |',
    '|---|---:|---|---|',
    '| Previous apparatus | 16 | 16 intended exception failures | 16 passed |',
    '| New authority | 18 | 18 intended APPROVAL BINDING BREACH assertions | 18 passed |',
    '| Clock transition | 1 | 2 failed, 3 passed parameter cases | 5 passed |',
    '| Clock final stop | 1 | 1 intended CLOCK BREACH failure | 1 passed |','',
    'The 18 authority RED cases replace only the test callback with `lambda: None` at `test_corrections.py:82`, then fail its assertion at line 83. They do not patch production `verify_approval_binding`. Their GREEN cases call the actual verifier and constructor rejection checks. The two clock cases do replace the production module comparison in memory. These qualifications prevent treating all 20 new pairs as equivalent production mutations.','',
    'Clock-transition RED failures are the two parametrized occurrences of the same below-boundary floating value `0.09999999999999999`; exact/above cases pass under the old comparator. The corrected GREEN runs all five parameter cases successfully.','',
    '| Collected group | Cases |','|---|---:|','| Unchanged P engineering | 59 |','| Previous apparatus | 24 |','| New correction | 30 |','| Total | 113 |','',
    'Saved complete-suite logs independently contain `113 passed in 77.05s (0:01:17)` for the worktree and `113 passed in 60.96s (0:01:00)` for the portable package. Collection does not itself establish passing execution.','',
    'Every JSON pair entry includes the actual reached `E ...` exception line, traceback file/line, RED/GREEN summaries, recorded exits and both log hashes. An intended string appearing only in quoted source was insufficient.','',
    '| Fault | Actual RED exception | GREEN count |','|---|---|---:|']
for row in result['pairs']:
    table.append('| '+row['fault']+' | '+row['red_exception_lines'][0].removeprefix('E').strip()+' | '+str(row['green_summary']['passed'])+' |')
(HERE/'SUITE_AND_FAULT_AUDIT.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
print(json.dumps({'summary':result['summary'],'composition':composition,'suite_logs':result['suite_logs']},indent=2))
