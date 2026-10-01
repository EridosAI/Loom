"""Read completed logs/JUnit, checking actual failure frames and all test outcomes."""
from pathlib import Path
import collections,hashlib,json,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent;D=R/'regression'
def sha(raw):return hashlib.sha256(raw).hexdigest()
rows=[]
for pair in json.loads((D/'FAULT_MATRIX.json').read_bytes()):
    row={k:pair[k] for k in ('fault','test','intended_failure')}
    for colour in ('RED','GREEN'):
        label=pair['fault']+'-'+colour;raw=(D/(label+'.log')).read_bytes();log=raw.decode('utf8')
        errors=[x for x in log.splitlines() if re.match(r'^E\s+',x)]
        frames=[x for x in log.splitlines() if re.search(r'\.py:\d+:',x)]
        summary=next(x for x in reversed(log.splitlines()) if re.search(r'\d+ (?:failed|passed)',x))
        xml=ET.parse(D/(label+'.xml'));cases=xml.findall('.//testcase')
        assert len(cases)==1 and not xml.findall('.//error') and not xml.findall('.//skipped')
        failure=cases[0].find('failure')
        if colour=='RED':
            assert pair[colour]['exit']==1 and pair[colour]['intended'] and failure is not None
            assert pair['intended_failure'] in '\n'.join(errors) and pair['intended_failure'] in (failure.text or '')
            assert frames and '1 failed' in summary
        else:
            assert pair[colour]['exit']==0 and pair[colour]['intended'] and failure is None and '1 passed' in summary
        row[colour]=dict(exit=pair[colour]['exit'],summary=summary,exception_lines=errors,trace_frames=frames,
            log_sha256=sha(raw),junit_sha256=sha((D/(label+'.xml')).read_bytes()),command=pair[colour]['command'])
    rows.append(row)
assert len(rows)==12
suites={}
for label in ('worktree-suite','portable-suite'):
    raw=(D/(label+'.log')).read_bytes();text=raw.decode('utf8');xml=ET.parse(D/(label+'.xml'))
    cases=xml.findall('.//testcase');assert len(cases)==204
    assert not any(xml.findall('.//'+tag) for tag in ('failure','error','skipped'))
    modules=collections.Counter(x.attrib['classname'] for x in cases)
    ids=[x.attrib['classname']+'::'+x.attrib['name'] for x in cases]
    composition={'P_engineering':sum(v for k,v in modules.items() if k.startswith('tests.'))}
    for name,file in [('original_apparatus','test_apparatus'),('previous_correction','test_corrections'),('final_correction','test_final_corrections'),('clock_correction','test_clock_scheduling'),('B1_operator','test_b1_operator')]:
        composition[name]=modules['tests_apparatus.'+file]
    assert composition==dict(P_engineering=59,original_apparatus=24,previous_correction=30,final_correction=30,clock_correction=33,B1_operator=28),dict(modules)
    summary=re.search(r'204 passed in [0-9.]+s',text);assert summary,text
    suites[label]=dict(summary=summary.group(0),composition=composition,all_cases_passed=True,test_ids=ids,
        log_sha256=sha(raw),junit_sha256=sha((D/(label+'.xml')).read_bytes()))
assert suites['worktree-suite']['test_ids']==suites['portable-suite']['test_ids']
out=dict(pairs=12,logs=24,all_actual_failure_frames_verified=True,suites=suites,rows=rows)
with (R/'FAULT_AND_SUITE_AUDIT.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
md=['# Independent A–L and full-suite audit','',
    'All 12 RED/GREEN pairs reach their intended failure and pass unmutated. RED failures are checked in actual exception frames and JUnit failure bodies, not merely echoed source. Each pair has one test case and no collection error or skip.','',
    '| Pair | Intended observed failure | RED | GREEN |','|---|---|---|---|']
for row in rows:md.append('| '+' | '.join([row['fault'],row['intended_failure'],row['RED']['summary'],row['GREEN']['summary']])+' |')
md+=['', 'A reinstates the old restriction in the test and raises its actual ValueError; it is not an assertion about the hidden world. B/D/L alter detached projection inputs/condition; E/F/G/J/K inject the named causal effect. H disables consumed-token rejection around real short component holds. I disables running-state rejection around a synchronization stub; it demonstrates overlapping entry, not overlapping physical trajectories. C bypasses the real client validator in detached Node DOM execution; its actual failed assertion proves exported chemistry and is supported by the independent surface review. These scope distinctions are preserved instead of calling every pair a production-code mutant.','']
for name,item in suites.items():md.append(name+': **'+item['summary']+'**; composition '+json.dumps(item['composition'])+'.')
with (R/'FAULT_AND_SUITE_AUDIT.md').open('x',encoding='utf8') as f:f.write('\n'.join(md)+'\n')
print(json.dumps({'pairs':12,'logs':24,'suites':{k:v['summary'] for k,v in suites.items()},'composition':composition}))
