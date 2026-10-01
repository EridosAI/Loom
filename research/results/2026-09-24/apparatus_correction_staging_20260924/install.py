"""Copy only scoped correction files, retain review inputs as fixtures."""
import gzip, json, pathlib, shutil
S=pathlib.Path(__file__).resolve().parent
P=S.parent
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'
E=D/'artifacts/apparatus-correction-20260924-01a0c405'
for name in ('contract.py','controllers.py','runner.py','authority.py'):
    shutil.copyfile(S/name,D/'loom_commissioning'/name)
shutil.copyfile(S/'test_corrections.py',D/'tests_apparatus/test_corrections.py')
physical=P/'exports/2026-09-24-p-apparatus-review-05abf604/physical'
actions=[json.loads(x) for x in gzip.decompress((physical/'hold-continuous/controller.jsonl.gz').read_bytes()).splitlines()]
fixtures=D/'tests_apparatus/fixtures'; fixtures.mkdir(exist_ok=True)
(fixtures/'review-boundary-input.json').write_text(json.dumps(actions[1]['inputs'],indent=2),encoding='utf-8')
references=E/'references'; references.mkdir(exist_ok=True)
for name in ('RUNNER_AUTHORITY_CONTROLLER_REVIEW.md','probe_runner_authority.py','probe_route_boundary.py','probe_final_until.py',
             'RUNNER_AUTHORITY_RESULTS.json','ROUTE_BOUNDARY_RESULTS.json','FINAL_UNTIL_RESULTS.json'):
    shutil.copyfile(physical/name,references/name)
shutil.copyfile(physical.parent/'LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md',references/'LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md')
shutil.copyfile(physical/'hold-continuous/controller.jsonl.gz',references/'original-controller.jsonl.gz')
shutil.copyfile(pathlib.Path(r'C:\Users\Jason\.codex\attachments\725ba354-15b2-4016-a551-0a2e927430c9\Pasted text.txt'),references/'CORRECTION_REQUEST.txt')
shutil.copyfile(S/'legacy_red.py',E/'legacy_red.py')
print('Installed only three modified runtime files, one authority module and new regression fixtures.')
