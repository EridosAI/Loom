"""Independent R2 audit. Target files are read-only; outputs stay beside this script."""
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

OUT = Path(__file__).resolve().parent / 'r2'
TEST = 'tests/test_records.py::test_live_handoff_observation_has_physical_timestamp'

def child(mode):
    import loom_p.inspector as inspector
    import pytest
    if mode in ('ambient_absent', 'ambient_poisoned'):
        inspector.ROOT = OUT / mode
        if mode == 'ambient_poisoned':
            path = inspector.ROOT / 'artifacts/smoke-contact_ui_1s-attempt-999/manifest.json'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('INVALID JSON: test must never inspect this ambient fixture', encoding='utf-8')
        print('Ambient ROOT:', inspector.ROOT)
    if mode == 'delivered_live_branch_missing':
        from verify_correction_mutants import install
        install('live_branch_missing')
    if mode == 'actual_live_branch_removed':
        source = textwrap.dedent(inspect.getsource(inspector.Inspector.observation))
        needle = 'elif not self.replay and e and e.last_wave:'
        assert source.count(needle) == 1
        source = source.replace(needle, 'elif False:')
        namespace = dict(vars(inspector))
        exec(compile(source, '<independent disabled live branch>', 'exec'), namespace)
        inspector.Inspector.observation = namespace['observation']
    raise SystemExit(pytest.main([TEST, '-q', '-p', 'no:cacheprovider', '--tb=short', '--basetemp', str(OUT / ('tmp-' + mode))]))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        child(sys.argv[1])
    OUT.mkdir(exist_ok=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONPATH=str(Path.cwd()))
    rows = []
    for mode in ('ambient_present', 'ambient_absent', 'ambient_poisoned', 'delivered_live_branch_missing', 'green_after_delivered', 'actual_live_branch_removed', 'green_after_actual'):
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', __file__, mode], capture_output=True, text=True, encoding='utf-8', env=env)
        output = result.stdout + result.stderr
        (OUT / (mode + '.txt')).write_text(output, encoding='utf-8')
        is_red = mode.endswith('missing') or mode.endswith('removed')
        assert result.returncode == (1 if is_red else 0), (mode, output)
        if is_red:
            assert '1 failed' in output and 'Live handoff branch was not exercised' in output, output
        else:
            assert '1 passed' in output, output
        rows.append(dict(mode=mode, exit_code=result.returncode, expected_red=is_red, consequential=True))
        print(mode, result.returncode, 'verified')
    (OUT / 'SUMMARY.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
