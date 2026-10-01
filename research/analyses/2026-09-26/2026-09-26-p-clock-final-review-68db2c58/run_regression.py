"""Independent invocation of the delivered bounded suites and fault matrices."""
import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path

OUT = Path(__file__).resolve().parent
WORKSPACE = OUT.parents[1]
SOURCE = WORKSPACE / 'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
PORTABLE = OUT / 'portable/developmental_ecology'
RESULTS = OUT / 'regression'
RESULTS.mkdir(exist_ok=False)

def execute(name, root, args):
    env = os.environ.copy()
    for key in ('PYTHONPATH','PYTEST_ADDOPTS','PYTEST_PLUGINS','APPARATUS_FAULT','CORRECTION_FAULT','FINAL_FAULT','CLOCK_FAULT'):
        env.pop(key, None)
    env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(root), GIT_OPTIONAL_LOCKS='0')
    cmd = [sys.executable, '-B', '-X', 'utf8', *args]
    start = time.perf_counter()
    run = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, encoding='utf-8', timeout=1200)
    log = run.stdout + run.stderr
    (RESULTS / (name + '.log')).write_text(log, encoding='utf-8')
    result = dict(name=name, root=str(root), command=cmd, exit=run.returncode, wall_seconds=time.perf_counter()-start)
    (RESULTS / (name + '.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result), flush=True)
    return result

jobs = [(label, root, ['-m','pytest','tests','tests_apparatus','-q','-p','no:cacheprovider','--basetemp',str(RESULTS/(label+'-temp'))])
        for label, root in [('worktree-suite',SOURCE),('portable-suite',PORTABLE)]]
jobs += [(label,SOURCE,[script,str(RESULTS/label)]) for label, script in [
    ('apparatus-faults','verify_apparatus.py'),('correction-faults','verify_corrections.py'),
    ('final-faults','verify_final_corrections.py'),('clock-faults','verify_clock_scheduling.py')]]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    rows = list(pool.map(lambda job: execute(*job), jobs))
(RESULTS/'RUNS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
assert all(row['exit']==0 for row in rows), rows
