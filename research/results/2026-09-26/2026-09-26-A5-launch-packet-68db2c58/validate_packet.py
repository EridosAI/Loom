"""Portable stdlib-only packet validator. No Loom import or simulation."""
import argparse
import hashlib
import json
import pathlib
import runpy
import tempfile
import zipfile


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def strict(raw):
    def pairs(xs):
        d = {}
        for k, v in xs:
            assert k not in d, 'duplicate JSON key'
            d[k] = v
        return d
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def diffs(a, b, p=''):
    if type(a) is dict and type(b) is dict:
        rows = []
        for k in sorted(set(a) | set(b)):
            path = p + '/' + k.replace('~', '~0').replace('/', '~1')
            if k not in a:
                rows.append(dict(path=path, operation='add', after=b[k]))
            elif k not in b:
                rows.append(dict(path=path, operation='remove', before=a[k]))
            else:
                rows.extend(diffs(a[k], b[k], path))
        return rows
    if type(a) is list and type(b) is list and len(a) == len(b):
        return [r for i, (x, y) in enumerate(zip(a, b)) for r in diffs(x, y, p + '/' + str(i))]
    return [] if a == b and type(a) is type(b) else [dict(path=p, operation='replace', before=a, after=b)]


def verify(read, names):
    assert len(names) == len(set(names))
    fm = strict(read('FILE_MANIFEST.json'))
    assert set(names) == set(fm['files']) | {'FILE_MANIFEST.json'}
    for n, v in fm['files'].items():
        raw = read(n)
        assert len(raw) == v['bytes'] and sha(raw) == v['sha256'], n
    oldfm = strict(read('historical-held/FILE_MANIFEST.json'))
    def oldread(n):
        name = 'historical-held/' + n
        return read(name if name in names else n)
    # The complete old packet is recoverable without duplicating large immutable references.
    for n, v in oldfm['files'].items():
        raw = oldread(n)
        assert len(raw) == v['bytes'] and sha(raw) == v['sha256'], ('historical', n)
    old = strict(oldread('A5_MANIFEST.json'))
    assert sha(oldread('AUTHORITY_OBJECT.canonical.json')) == '88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
    assert old['execution']['procedure']['protocol']['launch_disposition'] == 'HOLD_CLOCK_INCOMPATIBILITY'
    m = strict(read('A5_MANIFEST.json'))
    obj = {k: v for k, v in m.items() if k != 'execution_authority'}
    assert strict(read('AUTHORITY_OBJECT.json')) == obj
    assert read('AUTHORITY_OBJECT.canonical.json') == canonical(obj)
    h = sha(canonical(obj))
    assert h == read('AUTHORITY_SHA256.txt').decode().strip() == fm['authority_sha256']
    assert m['execution_authority'] is None
    p = m['execution']['procedure']['protocol']
    assert p['launch_ready'] is True and p['launch_disposition'] == 'READY_FOR_JASON_AUTHORIZATION'
    assert p['reviewed_checkpoints']['apparatus_git_sha'] == '68db2c581f07200966d699a4f55a65f9b96df1e9'
    for n, v in p['bound_files'].items():
        assert sha(read(n)) == v, n
    for n, v in strict(read('SOURCE_IDENTITIES.json')).items():
        assert sha(read('references/' + n)) == v['sha256'], n
        assert len(read('references/' + n)) == v['bytes'], n
    for group, folder in ((m['apparatus'], 'loom_commissioning'), (strict(read('CODE_AND_RUNTIME_IDENTITIES.json'))['P'], 'loom_p')):
        for n, v in group['files'].items():
            assert sha(read('instrument/developmental_ecology/' + folder + '/' + n)) == v
    semantic = strict(read('SEMANTIC_DIFF.json'))
    actual = diffs(old, m)
    classified = semantic['manifest_fields']
    assert actual == [{k: v for k, v in r.items() if k not in ('classification', 'reason')} for r in classified]
    assert semantic['unexpected_semantic_changes'] == []
    classes = {'IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS', 'SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX'}
    assert all(r['classification'] in classes for r in classified)
    # Reconstruct every changed existing document from declared exact replacements.
    for n, edits in semantic['document_replacements'].items():
        text = oldread(n).decode('utf-8')
        for r in edits:
            assert r['classification'] in classes and text.count(r['before']) == 1
            text = text.replace(r['before'], r['after'])
        assert read(n).decode('utf-8') == text, n
    for n, expected in semantic['supporting_json_fields'].items():
        assert diffs(strict(oldread(n)), strict(read(n))) == [{k: v for k, v in r.items() if k not in ('classification', 'reason')} for r in expected], n
        assert all(r['classification'] in classes for r in expected)
    for n in semantic['byte_identical_scientific_files']:
        assert read(n) == oldread(n), n
    # Independent whitelist: all scientific/trajectory manifest terms are unchanged.
    allowed = {'apparatus', 'execution'}
    for k in set(old) - allowed:
        assert old[k] == m[k], k
    for k in ('runtime', 'adapter', 'display_intervention', 'resources'):
        assert old['execution'][k] == m['execution'][k], k
    for k in ('kind', 'configuration', 'interface'):
        assert old['execution']['controller'][k] == m['execution']['controller'][k], k
    assert old['execution']['procedure']['stages'] == m['execution']['procedure']['stages']
    oldp = old['execution']['procedure']['protocol']
    allowedp = {'packet_status', 'launch_disposition', 'launch_ready', 'reviewed_checkpoints', 'bound_files', 'schedule_interpretation', 'record_destination', 'analysis_destination', 'launch_preconditions'}
    assert set(oldp) == set(p)
    for k in set(p) - allowedp:
        assert oldp[k] == p[k], k
    res = strict(read('RESOURCE_PROJECTION.json')); oldres = strict(oldread('RESOURCE_PROJECTION.json'))
    assert {k: v for k, v in res.items() if k not in ('status', 'enforcement')} == {k: v for k, v in oldres.items() if k not in ('status', 'enforcement')}
    clock = strict(read('STATIC_SCHEDULER_COMPATIBILITY.json'))
    assert clock['native_indices_checked'] == 63001 and clock['prescribed_holds_checked'] == 6300
    assert clock['stage_end_indices'] == [9000,12000,27000,30000,45000,48000,63000]
    assert clock['former_269_5_rejection_absent'] and clock['independent_270_rejection_absent']
    prep = strict(read('PREPARATION_CHECKS.json'))
    for k in ('world_steps','field_steps','neural_steps','controller_commands','simulation_RNG_draws','new_prehistory_steps','Engine_constructors','Run_constructors','sensor_evaluations','trial_routes','trial_phases','replays'):
        assert prep[k] == 0, k
    assert prep['forbidden_calls'] == [] and prep['null_grant_denial'] == 'commissioning execution is not authorized'
    assert prep['production_history_validation_executed'] is False and prep['prospective_output_absent'] is True
    assert strict(read('HASH_BEFORE.json')) == strict(read('HASH_AFTER.json'))
    assert strict(read('PRESERVATION.json'))['worktree_clean_after'] is True
    return dict(saved_byte_checks_pass=True, authority_sha256=h, execution_grant=None,
                payload_count=len(fm['files']), launch_disposition=p['launch_disposition'],
                unexpected_semantic_changes=0, world_steps=0, controller_commands=0,
                historical_hold_preserved=True,
                scope='Launch-packet/static evidence verification only. No A5 physical result.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('path'); args = parser.parse_args()
    path = pathlib.Path(args.path)
    if path.is_file():
        with zipfile.ZipFile(path) as z:
            result = verify(z.read, z.namelist())
    else:
        result = verify(lambda n: (path/n).read_bytes(), [p.relative_to(path).as_posix() for p in path.rglob('*') if p.is_file()])
    print(json.dumps(result, indent=2))
