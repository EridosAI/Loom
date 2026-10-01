"""Read existing fresh logs and collect test IDs only; no test bodies executed."""
from pathlib import Path
import collections,hashlib,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
TARGET=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
rows=[]
for folder,expected in [('previous-16-pairs-001',16),('previous-20-pairs-001',20),('new-18-pairs-001',18)]:
    pairs=json.loads((ROOT/folder/'FAULT_MATRIX.json').read_bytes());assert len(pairs)==expected
    for p in pairs:
        item={'matrix':folder,'fault':p['fault'],'intended_failure':p['intended_failure'],'test':p['test']}
        for colour in ('RED','GREEN'):
            path=ROOT/folder/(p['fault']+'-'+colour+'.log');raw=path.read_bytes();log=raw.decode('utf-8')
            lines=log.splitlines();summary=next(line for line in reversed(lines) if re.search(r'\d+ (?:passed|failed)',line))
            error_lines=[line for line in lines if re.match(r'^E\s+',line)]
            frames=[line for line in lines if re.search(r'\.py:\d+:',line)]
            assert p[colour]['intended']
            if colour=='RED':
                assert p[colour]['exit']==1 and p['intended_failure'] in '\n'.join(error_lines),(p['fault'],error_lines)
                assert frames and 'failed' in summary
            else:assert p[colour]['exit']==0 and 'passed' in summary and 'failed' not in summary
            item[colour]={'exit':p[colour]['exit'],'summary':summary,'exception_lines':error_lines,'trace_frames':frames,
                'sha256':hashlib.sha256(raw).hexdigest(),'command':p[colour]['command']}
        rows.append(item)
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',GIT_OPTIONAL_LOCKS='0')
for key in ('PYTHONPATH','APPARATUS_FAULT','CORRECTION_FAULT','FINAL_FAULT'):env.pop(key,None)
cmd=[sys.executable,'-B','-X','utf8','-m','pytest','tests','tests_apparatus','--collect-only','-q','-p','no:cacheprovider']
r=subprocess.run(cmd,cwd=TARGET,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
assert r.returncode==0,r.stdout+r.stderr
with (ROOT/'collection.log').open('x',encoding='utf-8') as f:f.write(r.stdout+r.stderr)
ids=[line.strip() for line in r.stdout.splitlines() if '::' in line and not line.startswith(' ')]
composition={'P_engineering':sum(x.startswith('tests/') for x in ids),
 'original_apparatus':sum(x.startswith('tests_apparatus/test_apparatus.py::') for x in ids),
 'previous_correction':sum(x.startswith('tests_apparatus/test_corrections.py::') for x in ids),
 'final_correction':sum(x.startswith('tests_apparatus/test_final_corrections.py::') for x in ids)}
assert composition=={'P_engineering':59,'original_apparatus':24,'previous_correction':30,'final_correction':30}
assert len(ids)==143
for name,seconds in [('worktree-suite.log','94.30'),('portable-suite.log','95.95')]:
    assert '143 passed in '+seconds+'s' in (ROOT/name).read_text()
result={'scope':'Existing delivered log audit and collect-only; zero additional test bodies',
 'pairs':len(rows),'logs':len(rows)*2,'all_intended_exceptions_verified':True,
 'collection':{'command':cmd,'composition':composition,'total':len(ids),'test_ids':ids},
 'suites':{'worktree':'143 passed in 94.30s','portable':'143 passed in 95.95s'},'matrix_rows':rows}
with (ROOT/'FAULT_AND_SUITE_AUDIT.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
md=['# Delivered fault/control and suite audit','',
 'All 54 pairs / 108 logs reach their intended RED exception and GREEN control. Collection: 59 + 24 + 30 + 30 = 143; no test bodies executed by collection.','',
 '| Matrix | Fault | Reached assertion | RED | GREEN |','|---|---|---|---|---|']
for row in rows:md.append('| '+ ' | '.join([row['matrix'],row['fault'],row['intended_failure'],row['RED']['summary'],row['GREEN']['summary']])+' |')
md.extend(['','The prior authority matrix contains 18 test-callback bypass faults, unchanged from the previous review. The final matrix instead restores the old parser or removes the named production check, as documented in the full review. The old clock-transition pair contains two failed and three passed RED instances; GREEN has five passed instances. Counts do not replace inspection of the actual exception and causal fault.'])
with (ROOT/'FAULT_AND_SUITE_AUDIT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(md)+'\n')
print(json.dumps({'pairs':len(rows),'logs':2*len(rows),'composition':composition,'all_intended_exceptions_verified':True}))
