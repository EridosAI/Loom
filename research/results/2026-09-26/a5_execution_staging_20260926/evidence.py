"""Read immutable ZIP evidence using only Python's standard library."""
import base64,gzip,hashlib,io,json,pathlib,struct,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
DEFAULT=ROOT.parent/'2026-09-25-first-A1-commissioning-result-5f077481/FIRST_A1_COMMISSIONING_RESULT.zip'
if (ROOT/'references/FIRST_A1_COMMISSIONING_RESULT.zip').is_file():DEFAULT=ROOT/'references/FIRST_A1_COMMISSIONING_RESULT.zip'
EXPECTED='f37dfec92288fbe8a650b00eed611d086a3ece3b280292e95b891e371cc0d37f'
PREFIX='FIRST_COMMISSIONING_LAUNCH_PACKET/'
def digest(b):return hashlib.sha256(b).hexdigest()
def filehash(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canonical(v):return json.dumps(v,allow_nan=False,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def plain(v):
    """Decode numeric data into built-ins only. Never construct snapshot classes."""
    if isinstance(v,list):return [plain(x) for x in v]
    if not isinstance(v,dict):return v
    if '$dict' in v:
        result={}
        for k,x in v['$dict']:
            key=plain(k);assert key not in result,'Duplicate snapshot key';result[key]=plain(x)
        return result
    if '$class' in v:return {'__class__':v['$class'],**plain(v['attrs'])}
    if '$tuple' in v:return tuple(plain(x) for x in v['$tuple'])
    if '$slice' in v:return {'slice':v['$slice']}
    if '$array' in v:
        kinds={'f8':'d','f4':'f','i8':'q','i4':'i','u8':'Q','u4':'I','i2':'h','u2':'H','i1':'b','u1':'B'}
        dtype=v['dtype'];code=kinds[dtype[1:]];raw=base64.b64decode(v['$array'],validate=True)
        values=[x[0] for x in struct.iter_unpack(('<' if dtype[0] in '<|' else '>')+code,raw)]
        shape=v['shape'];it=iter(values)
        def reshape(s):return next(it) if not s else [reshape(s[1:]) for _ in range(s[0])]
        out=reshape(shape)
        assert next(it,None) is None
        return out
    raise ValueError('Unknown packed tag')
def packed_attr(obj,key):return dict(obj['attrs']['$dict'])[key]
def snapshot_data(s):
    assert digest(canonical(s['state']))==s['sha256'],'Snapshot internal checksum mismatch'
    return plain(s['state'])
def write(p,obj):
    pathlib.Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
class Evidence:
    def __init__(self,path=DEFAULT):
        self.path=pathlib.Path(path);self.zip_sha256=filehash(self.path)
        assert self.zip_sha256==EXPECTED,'Wrong historical evidence package'
        self.z=zipfile.ZipFile(self.path)
        self.manifest=self.json('FILE_MANIFEST.json')
        assert set(self.z.namelist())==set(self.manifest['files'])|{'FILE_MANIFEST.json'}
        for n,r in self.manifest['files'].items():
            b=self.z.read(n);assert len(b)==r['bytes'] and digest(b)==r['sha256'],n
        self.launch=zipfile.ZipFile(io.BytesIO(self.z.read('approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip')))
        lm=json.loads(self.launch.read(PREFIX+'FILE_MANIFEST.json'))
        for n,r in lm['files'].items():
            b=self.launch.read(PREFIX+n);assert len(b)==r['bytes'] and digest(b)==r['sha256'],n
    def json(self,n):return json.loads(self.z.read(n))
    def stream(self,n):return [json.loads(x) for x in gzip.decompress(self.z.read('evidence/trajectory-001/'+n+'.jsonl.gz')).splitlines()]
    def snapshot(self,name):return json.loads(gzip.decompress(self.z.read('evidence/trajectory-001/'+name+'.restart.json.gz')))
    def launch_json(self,n):return json.loads(self.launch.read(PREFIX+n))
    def source(self,n):return self.launch.read(PREFIX+'instrument/developmental_ecology/'+n).decode('utf-8')
    def proof(self):return {'zip_sha256':self.zip_sha256,'zip_bytes':self.path.stat().st_size,'files':self.manifest['files'],'nested_launch_manifest_verified':True}
