"""Reaffirm an existing checkpoint review; documentation only."""
from pathlib import Path
from urllib.parse import unquote
import hashlib, json, re, sys, zipfile

ROOT = Path(__file__).resolve().parent
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
S = '50_SESSIONS/2026-09-26-05abf604-scope-confirmation-c1857b2a'
R = S + '/APPARATUS_REVIEW_SCOPE_CONFIRMATION.md'
REVIEW = '30_REVIEWS/REVIEW-P-APPARATUS-INDEPENDENT-05abf604-2026-09-24-b92e45a7.md'
B = '90_SOURCES/p_independent_apparatus_review_2026-09-24_b92e45a7'
SHA = '05abf60401d08f38750bca589b1c040e10513d7b'
A3 = '50_SESSIONS/2026-09-26-a3-evidence-intake-7c42a9d1/A3_COMMISSIONING_EVIDENCE_RECORD.md'
CLOSURE = '30_REVIEWS/REVIEW-P-APPARATUS-MECHANICAL-CLOSURE-5f077481-2026-09-25-c84f219a.md'
sha = lambda data: hashlib.sha256(data).hexdigest()

def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

def scoped(relative):
    p = (WB / relative).resolve()
    assert p.is_relative_to(WB) and p != WB
    return p

if '--publish' not in sys.argv:
    catalog = json.loads((WB / 'SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
    sources = [e for e in catalog['source_files'] if e['path'].startswith(B + '/')]
    assert len(sources) == 6
    for e in sources:
        data = (WB / e['path']).read_bytes()
        assert len(data) == e['bytes'] and sha(data) == e['sha256']
    protected_names = [e['path'] for e in sources] + [REVIEW, CLOSURE, A3, 'SOURCE_CATALOG.json', 'SOURCE_REGISTER.md', 'AGENTS.md']
    protected = {n: sha((WB / n).read_bytes()) for n in protected_names}
    receipt = json.loads((WB / B / 'REVIEW_RECEIPT.json').read_text(encoding='utf-8-sig'))
    assert receipt['apparatus_checkpoint'] == SHA
    assert [v['id'] for v in receipt['findings']] == ['A-R1', 'A-R2']
    note = f'''# Exact 05abf604 apparatus-review scope reaffirmed

**Recorded:** 2026-09-26 under Jason's current instruction. The [independent review]('../../{REVIEW}') was already registered on 2026-09-24. This confirms its exact checkpoint scope and explicitly records the commissioning-design distinction; it is not a duplicate source intake or a new independent review.

Exact apparatus commit: `{SHA}`

Commissioning apparatus: **ENGINEERING HOLD**  
P implementation: **unchanged / previously verified**  
Commissioning execution: **NOT STARTED**

Blockers:

- **A1** — approval binding does not yet bind complete arm/controller/route.
- **A2** — stage clock comparison may permit one extra 0.1 s command hold.

All other reviewed apparatus findings retain their reviewed status.

**The commissioning design itself is not marked failed.** These are apparatus implementation findings at this exact checkpoint. They do not establish failure of P or scientific/developmental efficacy. A1 and A2 above are Jason's aliases for source findings A-R1 and A-R2; they are distinct from the later physical commissioning cases A1 and A2.

The original report, receipt, complete finding table and prior registration remain unchanged. The “NOT STARTED” label belongs to this pre-run checkpoint review. The [later mechanical closure]('../../{CLOSURE}') and [current A3 commissioning record]('../../{A3}') retain their own dispositions. No rollback of later evidence or new global hold is inferred from this exact-commit request.

Sources: [original independent report]('../../{B}/LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md') · [review receipt]('../../{B}/REVIEW_RECEIPT.json'). These links identify source findings; no included tests, probes, replays or commands were rerun.

Completion: read current AGENTS/map/status, the existing registered review and original report/receipt; verified all six registered source sizes/hashes (SRC-077–SRC-082). Added only this session and a linked scope sentence within the existing historical 05abf604 section of the live map and status. No source, candidate, decision, original review, P, canon, Base World, apparatus, numerical setting or commissioning sequence was changed. No execution, Git operation or experiment number was added. Later cases/efficacy retain their existing open statuses.

[Validation and source identities](VALIDATION.json). PRIOR_NAVIGATION.zip preserves the two prior navigation files; this assistant-authored record is not a verbatim chat export.
'''.replace("]('", '](').replace("')", ')')
    new = ROOT / 'NEW' / R
    new.parent.mkdir(parents=True, exist_ok=True)
    new.write_text(note, encoding='utf-8', newline='\n')
    before = {}
    sentence = f'Checkpoint scope reaffirmed 2026-09-26: **the commissioning design itself is not marked failed**. This is an apparatus hold for exact 05abf604; later checkpoint closure and execution records retain their own statuses. [Scope confirmation]({R}).\n\n'
    for n in ['00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md']:
        data = (WB / n).read_bytes()
        before[n] = {'bytes': len(data), 'sha256': sha(data)}
        p = ROOT / 'BEFORE' / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        text = data.decode('utf-8-sig')
        heading = '## Preserved apparatus hold — 05abf604, 2026-09-24'
        start = text.index(heading)
        end = text.index('\n## ', start + len(heading))
        section = text[start:end]
        anchor = 'All other reviewed apparatus findings retain their reviewed status.\n\n'
        assert section.count(anchor) == 1
        updated = text[:start] + section.replace(anchor, anchor + sentence, 1) + text[end:]
        assert updated.replace(sentence, '', 1) == text
        p = ROOT / 'AFTER' / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(updated, encoding='utf-8', newline='\n')
    dump(ROOT / 'PLAN.json', {'session': S, 'record': R, 'before': before, 'protected': protected,
        'sources': sources, 'checkpoint': SHA})

plan = json.loads((ROOT / 'PLAN.json').read_text(encoding='utf-8'))
for n, meta in plan['before'].items():
    assert sha((WB / n).read_bytes()) == meta['sha256'], 'Concurrent navigation edit: ' + n
for n, h in plan['protected'].items():
    assert sha((WB / n).read_bytes()) == h, 'Concurrent protected edit: ' + n
assert not scoped(S).exists()
count = 0
for group in ['NEW', 'AFTER']:
    for p in (ROOT / group).rglob('*.md'):
        base = WB / p.relative_to(ROOT / group)
        for href in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^\)\n]+)\)', p.read_text(encoding='utf-8')):
            if re.match(r'^[A-Za-z]+:', href):
                continue
            path = unquote(href.strip('<>')).split('#')[0]
            if not path:
                continue
            dest = (base.parent / path).resolve()
            exists = dest.is_file()
            if dest.is_relative_to(WB):
                rel = dest.relative_to(WB)
                exists = exists or (ROOT / 'NEW' / rel).is_file() or rel.as_posix() == S + '/VALIDATION.json'
            assert exists, (str(base), href)
            count += 1
if '--publish' not in sys.argv:
    print(json.dumps({'ready': True, 'sources_verified': len(plan['sources']), 'links_validated': count,
        'change': 'Two historical-section annotations and one new scope-confirmation record; current A3 status unchanged'}))
    sys.exit(0)

session = scoped(S)
session.mkdir(parents=True)
scoped(R).write_bytes((ROOT / 'NEW' / R).read_bytes())
with zipfile.ZipFile(session / 'PRIOR_NAVIGATION.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for n, meta in plan['before'].items():
        data = (ROOT / 'BEFORE' / n).read_bytes()
        assert sha(data) == meta['sha256']
        z.writestr(n, data)
for n, meta in plan['before'].items():
    assert sha((WB / n).read_bytes()) == meta['sha256'], n
    scoped(n).write_bytes((ROOT / 'AFTER' / n).read_bytes())
for n, h in plan['protected'].items():
    assert sha((WB / n).read_bytes()) == h, n
with zipfile.ZipFile(session / 'PRIOR_NAVIGATION.zip') as z:
    for n, meta in plan['before'].items():
        assert sha(z.read(n)) == meta['sha256']
for group in ['NEW', 'AFTER']:
    for p in (ROOT / group).rglob('*'):
        if p.is_file():
            assert p.read_bytes() == scoped(p.relative_to(ROOT / group)).read_bytes()
dump(session / 'VALIDATION.json', {'checkpoint': SHA, 'record': R, 'sources': plan['sources'],
    'protected_files_unchanged': plan['protected'], 'navigation_before': plan['before'],
    'navigation_after': {n: sha((WB / n).read_bytes()) for n in plan['before']},
    'recovery_zip_sha256': sha((session / 'PRIOR_NAVIGATION.zip').read_bytes()),
    'recovery_verified': True, 'links_validated': count, 'published_bytes_match': True,
    'review_rerun': False, 'git_operations': False, 'later_checkpoint_and_execution_statuses_changed': False})
print(json.dumps({'saved': str(scoped(R)), 'exact_checkpoint_status': 'ENGINEERING HOLD',
    'commissioning_design_failed': False, 'later_statuses_unchanged': True, 'links_validated': count}))
