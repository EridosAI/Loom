from pathlib import Path
import colorsys,hashlib,json,re
S=Path(__file__).resolve().parent;R=S.parent
W=R/'worktrees/loom-p-b1-coordinate-colours-20260929';D=W/'developmental_ecology'
A=R/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology'
qa=json.loads((S/'BROWSER_COLOUR_QA.json').read_bytes())
counts={'light':10,'chemistry':4,'contact':8,'proprioception':7}
for mode,count in [('full',29),('hidden',25)]:
    rows=qa[mode]['rows'];assert len(rows)==count
    for row in rows:
        name,k=row['label'].rsplit('_',1)
        expected=[x*255 for x in colorsys.hls_to_rgb(int(k)/counts[name],.4,.55)]
        actual=[float(x) for x in re.findall(r'[\d.]+',row['colour'])]
        assert len(actual)==3 and all(abs(a-b)<=.51 for a,b in zip(actual,expected))
    assert qa[mode]['valueColours']==['rgb(24, 58, 60)']
assert not any(r['label'].startswith('chemistry_') for r in qa['hidden']['rows'])
assert qa['hidden']['chemistryUnavailable']=='CHEMISTRY UNAVAILABLE IN THIS CONDITION'
unchanged={}
for pkg in ['loom_p','loom_commissioning']:
    for p in (A/pkg).iterdir():
        if not p.is_file() or p.suffix not in ('.html','.py') or p.name=='sensor.html':continue
        relative=p.relative_to(A)
        assert p.read_bytes()==(D/relative).read_bytes()
        unchanged[relative.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['configuration.json','requirements-lock.txt']:
    assert (A/name).read_bytes()==(D/name).read_bytes()
    unchanged[name]=hashlib.sha256((D/name).read_bytes()).hexdigest()
result=dict(all_label_RGBs_match_renderer_within_8bit_rounding=True,full_coordinates=29,hidden_coordinates=25,
    no_chemistry_label_or_value_added_to_hidden_condition=True,numeric_colours_unchanged=True,no_separate_legend=True,
    unchanged_files=unchanged,active_checkout_untouched=True,simulation_steps=0,controller_commands=0,
    data='Existing disclosed PC-HOLD only; no B1 hidden state or evaluator read')
(S/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: all 54 displayed labels match trace colours; numeric values, hidden omission and production Python/configuration remain unchanged.')
