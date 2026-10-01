from evidence import *
import shutil
e=Evidence()
write(ROOT/'HASH_BEFORE.json',e.proof())
shutil.copyfile(r'C:\Users\Jason\.codex\attachments\d48ca56e-724d-4767-bcc5-41bcaec53b4c\Pasted text.txt',ROOT/'READ_ONLY_REQUEST.txt')
for n in ('native','diagnostics','controller','events','sensor'):
    data=e.stream(n)
    print(n,len(data),'FIRST',json.dumps(data[0])[:7000])
    if n in ('native','events'):print(n,'CONTACT',json.dumps(data[632])[:7000])
for n in ('initial','final'):
    s=e.snapshot(n);print(n,'snapshot keys',list(s))
    for k,v in s.items():print(k, list(v) if isinstance(v,dict) else str(v)[:200])
print('launch files',[n for n in e.launch.namelist() if 'config' in n or 'CONTRACT' in n or 'DESIGN' in n])
print('configuration',e.source('configuration.json'))
