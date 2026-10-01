"""Create a separate A5 saved-data reader; preserve all prior checkers."""
import pathlib,shutil
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
old=ROOT/'a3_execution_staging_20260926/a3_analysis_core.py'
t=old.read_text(encoding='utf-8')
changes={
    'A3':'A5',
    '2026-09-25-A5-launch-packet-5f077481':'2026-09-26-A5-launch-packet-68db2c58',
    '43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd':'bdff35693db38800528d91e6d2d4d2085c640268e50713731df5ec27f8b76d1d',
    "stages=d.manifest['execution']['procedure']['stages'];stage_counts=collections.Counter()":"stages=d.manifest['execution']['procedure']['stages'];stage_counts=collections.Counter()\n    ends=[int(Fraction(str(p['until']))*100) for p in stages]",
    "while j<len(stages)-1 and (a['time']>=stages[j]['until'] or math.isclose(a['time'],stages[j]['until'],rel_tol=0,abs_tol=TOL)):j+=1":"while j<len(stages)-1 and a['native_index']>=ends[j]:j+=1",
    "assert a['time']+a['hold_native_steps']*.01<=stages[j]['until']+TOL":"assert a['native_index']+a['hold_native_steps']<=ends[j]\n        allowance=1e-10+(a['native_index']*2.**-53/(1-a['native_index']*2.**-53))*(a['native_index']*.01)+2*math.ulp(a['native_index']*.01)\n        assert abs(a['time']-a['native_index']*.01)<=allowance",
}
for a,b in changes.items():
    assert a in t,a;t=t.replace(a,b)
t=t.replace('import base64,bisect,collections,gzip,hashlib,json,math,pathlib,sys','import base64,bisect,collections,gzip,hashlib,json,math,pathlib,sys\nfrom fractions import Fraction')
with (S/'a5_analysis_core.py').open('x',encoding='utf-8') as f:f.write(t)
for n in ('evidence.py','v3_checker_v1_1.py'):shutil.copyfile(ROOT/'a3_execution_staging_20260926'/n,S/n)
compile(t,str(S/'a5_analysis_core.py'),'exec')
print('Saved-data reader authored. No trajectory opened or simulation operation performed.')
