"""Inspect delivered fresh RED exception frames and collect suite IDs, without test execution."""
from pathlib import Path
import hashlib, json, os, re, subprocess, sys
R=Path(__file__).resolve().parent
TARGET=R.parents[1]/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
rows=[]
for folder, expected in [('apparatus-faults',16),('correction-faults',20),('final-faults',18),('clock-faults',5)]:
    pairs=json.loads((R/'regression'/folder/'FAULT_MATRIX.json').read_bytes())
    assert len(pairs)==expected
    for pair in pairs:
        item={k:pair[k] for k in ('fault','test','intended_failure')}; item['matrix']=folder
        for colour in ('RED','GREEN'):
            path=R/'regression'/folder/(pair['fault']+'-'+colour+'.log')
            raw=path.read_bytes(); lines=raw.decode('utf-8').splitlines()
            summary=next(line for line in reversed(lines) if re.search(r'\d+ (?:passed|failed)',line))
            error_lines=[line for line in lines if re.match(r'^E\s+',line)]
            frames=[line for line in lines if re.search(r'\.py:\d+:',line)]
            assert pair[colour]['intended']
            if colour=='RED':
                assert pair[colour]['exit']==1 and pair['intended_failure'] in '\n'.join(error_lines),(pair['fault'],error_lines)
                assert frames and 'failed' in summary
            else:
                assert pair[colour]['exit']==0 and 'passed' in summary and 'failed' not in summary
            item[colour]=dict(exit=pair[colour]['exit'],summary=summary,exception_lines=error_lines,
                trace_frames=frames,sha256=hashlib.sha256(raw).hexdigest(),command=pair[colour]['command'])
        rows.append(item)
env=os.environ.copy()
for key in ('PYTHONPATH','PYTEST_ADDOPTS','PYTEST_PLUGINS','APPARATUS_FAULT','CORRECTION_FAULT','FINAL_FAULT','CLOCK_FAULT'):env.pop(key,None)
env.update(PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',GIT_OPTIONAL_LOCKS='0')
cmd=[sys.executable,'-B','-X','utf8','-m','pytest','tests','tests_apparatus','--collect-only','-q','-p','no:cacheprovider']
run=subprocess.run(cmd,cwd=TARGET,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
assert run.returncode==0,run.stdout+run.stderr
(R/'regression/collection.log').write_text(run.stdout+run.stderr,encoding='utf-8')
ids=[line.strip() for line in run.stdout.splitlines() if '::' in line and not line.startswith(' ')]
composition={'P_engineering':sum(x.startswith('tests/') for x in ids)}
for key,file in [('original_apparatus','test_apparatus'),('previous_correction','test_corrections'),('final_correction','test_final_corrections'),('clock_correction','test_clock_scheduling')]:
    composition[key]=sum(x.startswith('tests_apparatus/'+file+'.py::') for x in ids)
assert composition==dict(P_engineering=59,original_apparatus=24,previous_correction=30,final_correction=30,clock_correction=33)
assert len(ids)==176
suites={}
for label in ('worktree','portable'):
    log=(R/'regression'/(label+'-suite.log')).read_text(encoding='utf-8')
    summary=re.search(r'176 passed in [0-9.]+s',log)
    assert summary and not re.search(r'\d+ (?:failed|error|skipped)',log),log
    suites[label]=summary.group(0)
result=dict(scope='Fresh log audit plus collect-only, no further test bodies',pairs=len(rows),logs=len(rows)*2,
    all_intended_exceptions_verified=True,collection=dict(command=cmd,composition=composition,total=len(ids),test_ids=ids),
    suites=suites,matrix_rows=rows)
with (R/'FAULT_AND_SUITE_AUDIT.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
md=['# Independent delivered regression audit','',
    '59 pairs / 118 logs reach the intended RED exception and GREEN control. Suite collection is 59 P + 24 original apparatus + 30 prior correction + 30 final correction + 33 clock cases = 176.','',
    '| Matrix | Fault | Actual intended failure | RED | GREEN |','|---|---|---|---|---|']
for row in rows:md.append('| '+' | '.join([row['matrix'],row['fault'],row['intended_failure'],row['RED']['summary'],row['GREEN']['summary']])+' |')
md += ['', 'The prior 18 authority faults bypass their test approval callback, preserving the delivered test scope; they are not claimed as 18 production mutants. The final authority/dispatch/pending matrix removes or replaces the named production guard. The old transition fault is parameterized: two failed and three passed RED cases, five passed GREEN cases. Both updated old clock faults genuinely restore floating-time stage ownership at the native-index interface. The five new faults reinstate the fixed clock band, restore floating stage selection, disable corruption rejection, round an off-grid declaration, or permit off-cadence decisions. Actual exception lines, traceback frames and hashes are retained in the JSON audit.']
with (R/'FAULT_AND_SUITE_AUDIT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(md)+'\n')
print(json.dumps(dict(pairs=len(rows),logs=len(rows)*2,composition=composition,suites=suites)))
