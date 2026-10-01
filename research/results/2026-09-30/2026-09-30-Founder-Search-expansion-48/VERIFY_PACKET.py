"""Read-only standard-library packet/ZIP verification; never starts a life."""
import hashlib,json,pathlib,sys,zipfile
p=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
if p.is_file():
    with zipfile.ZipFile(p) as z:
        m=json.loads(z.read('PACKAGE_MANIFEST.json'))
        for r in m['files']:
            b=z.read(r['path']);assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
else:
    m=json.loads((p/'PACKAGE_MANIFEST.json').read_bytes())
    for r in m['files']:
        b=(p/r['path']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
print(json.dumps({'status':'PASS','files':len(m['files']),'new_lives_executed':0,'scope':'byte custody only'}))
