"""Read-only preservation inventory and scoped correction setup. No world calls."""
import hashlib, json, pathlib, subprocess, sys
WT=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
PROJECT=pathlib.Path(__file__).resolve().parents[1]
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
OUT=WT/'developmental_ecology/artifacts/apparatus-correction-20260924-01a0c405'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(root):
    return {str(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file()}
if sys.argv[1]=='before':
    assert subprocess.check_output(['git','-C',str(WT),'rev-parse','HEAD'],text=True).strip()=='05abf60401d08f38750bca589b1c040e10513d7b'
    assert not subprocess.check_output(['git','-C',str(WT),'status','--porcelain'],text=True).strip()
    entries={}
    for root in [WT/'developmental_ecology/artifacts',PROJECT/'exports/2026-09-24-p-apparatus-review-05abf604',WB/'50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84']:
        entries.update(inventory(root))
    original=WB/'INBOX/2026-09-24-p-commissioning-apparatus/Loom_P_Commissioning_Apparatus_Review_20260924.zip'
    assert sha(original)=='87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053'
    entries[str(original)]={'bytes':original.stat().st_size,'sha256':sha(original)}
    OUT.mkdir(exist_ok=False)
    check=OUT/'temporary-capability-check.txt'; check.write_text('scoped local write/read'); assert check.read_text()=='scoped local write/read'; check.unlink()
    (OUT/'PRESERVATION_BEFORE.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
    print('Windows-local scoped write/read passed. Preserved inventory:',len(entries))
else:
    before=json.loads((OUT/'PRESERVATION_BEFORE.json').read_bytes())
    errors=[p for p,row in before.items() if not pathlib.Path(p).is_file() or sha(pathlib.Path(p))!=row['sha256'] or pathlib.Path(p).stat().st_size!=row['bytes']]
    assert not errors,errors
    (OUT/'PRESERVATION_AFTER.json').write_text(json.dumps({'checked':len(before),'all_unchanged':True,'missing_or_changed':errors},indent=2),encoding='utf-8')
    print('Preserved',len(before),'prior files byte for byte')
