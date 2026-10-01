"""Copy/hash existing decision metadata only; no replay or controller calls."""
import gzip,hashlib,json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parents[1]
D=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
OUT=R/'exports/2026-09-26-A5-clock-correction'
NEW=R/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
folders={'A1':D/'artifacts/first-commissioning-A1-20260925-5f077481/trajectory-001',
         'A2':D/'artifacts/commissioning-A2-20260925-5f077481/trajectory-001',
         'A3':D/'artifacts/commissioning-A3-20260925-5f077481/trajectory-001'}
folders.update({n:D/'artifacts/commissioning-A4-20260926-5f077481'/n/'trajectory-001' for n in ('A4-CROSS','A4-WAIT','A4-DETOUR')})
cases=[];sources={}
for name,folder in folders.items():
    receipt=json.loads((folder/'manifest.json').read_bytes());m=receipt['contract']
    assert sha(folder/'controller.jsonl.gz')==receipt['files']['controller.jsonl.gz']['sha256']
    with gzip.open(folder/'controller.jsonl.gz','rt',encoding='utf-8') as f:actions=[json.loads(l) for l in f]
    cases.append({'case':name,'scheduling_fields':{k:m[k] for k in ('initial_time','initial_index','duration_seconds','hard_stop_time')}
        | {'execution':{'procedure':{'stages':m['execution']['procedure']['stages']}}},
        'decisions':[[a['native_index'],a['time'],a['stage']['index']] for a in actions]})
    dest=OUT/'saved_stage_references'/name;dest.mkdir(parents=True)
    for filename in ('manifest.json','controller.jsonl.gz'):
        p=folder/filename;shutil.copyfile(p,dest/filename)
        sources[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size}
assert sum(len(c['decisions']) for c in cases)==5579
payload={'scope':'Historical saved clock/stage metadata. No launch manifest or execution authority. No replay.', 'cases':cases}
(NEW/'tests_apparatus/fixtures/clock_retrospective.json').write_text(json.dumps(payload,separators=(',',':')),encoding='utf-8')
(OUT/'RETROSPECTIVE_SOURCES.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
print('Extracted 5579 saved decisions; original receipts and compressed controller records copied and hashed unchanged.')
