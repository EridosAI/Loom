"""Prepare new saved-data A4 reporting helpers; preserve all prior analysis sources."""
import pathlib,shutil
S=pathlib.Path(__file__).resolve().parent;old=S.parent/'a3_execution_staging_20260926'
for n in ('evidence.py','v3_checker_v1_1.py'):shutil.copyfile(old/n,S/n)
src=(old/'a3_analysis_core.py').read_text(encoding='utf-8')
src=src.replace('A3 read-only analysis v1.0','A4 read-only analysis v1.0').replace('2026-09-25-A3-launch-packet-5f077481','2026-09-26-A4-launch-packet-5f077481')
src=src.replace("AUTH='43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd'","BATCH_AUTH='47a71e78ad4bbb920f2b29f7d9b0e3c5f520eb4905880916c85f0cc8bbb9f1e0'")
a=src.index('def record_integrity(d):');b=src.index('\ndef boundary_check(d):',a)
replacement='''def record_integrity(d):
    r=d.receipt;m=d.manifest;AUTH=m['execution_authority']['approved_execution_sha256']
    for n,v in r['files'].items():
        p=d.t/n;assert p.stat().st_size==v['bytes'] and shafile(p)==v['sha256'],n
    assert {p.name for p in d.t.iterdir() if p.is_file()}==set(r['files'])|{'manifest.json'}
    for name in ('native','events','controller','sensor','diagnostics','wave','scientific_observations'):assert len(getattr(d,name))==r['records'].get(name,0),name
    obj={k:v for k,v in m.items() if k!='execution_authority'}
    assert digest(sorted_bytes(obj))==AUTH
    assert sorted_bytes(obj)==(d.base/'APPROVED_EXECUTION.canonical.json').read_bytes()
    batch=js(d.base.parent/'APPROVED_BATCH.canonical.json');assert digest(sorted_bytes(batch))==BATCH_AUTH
    member=next(x for x in batch['cases'] if x['case_id']==m['case_id'])
    assert member['execution_object']==obj and member['execution_sha256']==AUTH
    req=js(d.base/'APPROVAL_REQUEST.json');grant=m['execution_authority']
    assert req['approved_execution']==obj and req['approved_execution_sha256']==AUTH
    assert shafile(d.base/'APPROVAL_REQUEST.json')==grant['request_sha256']
    original=(d.base.parent/'AUTHORIZATION_SOURCE.txt').read_text(encoding='utf-8').rstrip('\\n')
    assert req['notice'].startswith(original+'\\n\\n') and BATCH_AUTH in req['notice'] and AUTH in req['notice'] and m['case_id'] in req['notice']
    assert r['contract']==m==d.initial_wrapper['manifest']==d.final_wrapper['manifest']
    initial_packed=dict(d.initial_wrapper['state']['$dict'])['engine'];final_packed=dict(d.final_wrapper['state']['$dict'])['engine']
    assert digest(canonical(initial_packed))==m['initial_state']
    assert digest(canonical(final_packed))==r['final_state']==d.result['final_engine_sha256']
    assert d.result['run_constructors_attempted']==1 and d.result['no_retry_no_resume']
    for i,n in enumerate(d.native,1):assert n['native_index']==i and n['field_phase']==m['phase']
    assert len(d.native)==d.final['native_index'] and abs(d.final['time']-r['final_time'])<=TOL
    assert d.final['time']<=m['hard_stop_time']+1e-9
    status=r['status']
    if status=='administrative_cutoff':assert abs(d.final['time']-m['hard_stop_time'])<1e-9 and d.final['terminal_dimension'] is None
    elif status=='administrative_pause':assert d.final['time']<m['hard_stop_time']-1e-9 and d.final['terminal_dimension'] is None
    elif status=='terminal':assert d.final['status']=='terminal' and min(d.final['body']['energy'],d.final['body']['integrity'])<=1e-9
    elif status=='apparatus_failure':assert not r['complete'] and r['error']
    else:raise AssertionError('Unknown stop')
    return {'valid':True,'complete':r['complete'],'status':status,'stop_cause':r.get('stop_cause'),'receipt_payloads':len(r['files']),
       'record_counts':r['records'],'batch_authority_sha256':BATCH_AUTH,'case_execution_sha256':AUTH,'physical_replay':False,'controller_recomputation':False,
       'scope':'Saved receipt, checksum, exact parent/constituent grant/object, native sequence and stop checks. Production verify_segment not invoked because it recomputes commands even with replay=False.'}
'''
src=src[:a]+replacement+src[b:]
src=src.replace('def boundary_check(d):\n','def boundary_check(d):\n    AUTH=d.manifest[\'execution_authority\'][\'approved_execution_sha256\']\n').replace("'analysis_version':'A3 read-only v1.0'","'analysis_version':'A4 read-only v1.0'")
with (S/'a4_analysis_core.py').open('x',encoding='utf-8') as f:f.write(src)
prior=(old/'a3_observations.py').read_text(encoding='utf-8');part=prior[prior.index('def touch('):prior.index('def pose_history(')]
part=part.replace("labels=['repair-0']+[f'source-{i}' for i in range(8)]","labels=['mover']+[f'wall-{i}' for i in range(4)]+[f'repair-{i}' for i in range(3)]+[f'source-{i}' for i in range(8)]")
with (S/'a4_window_helpers.py').open('x',encoding='utf-8') as f:f.write('"""Saved-data windows adapted from preserved A3 helpers; no simulation."""\nfrom a4_analysis_core import *\n\n'+part)
print('Prepared new A4 saved-data helpers; original A3/V3 sources unchanged. No data analysis or simulation executed.')
