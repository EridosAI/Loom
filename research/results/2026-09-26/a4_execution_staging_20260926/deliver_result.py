"""Copy the sealed A4 result into one new workbench INBOX folder; no Git/simulation."""
import hashlib,json,pathlib,shutil,time
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
SRC=ROOT/'exports/2026-09-26-A4-commissioning-result-5f077481'
TARGET=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-26-A4-commissioning-result-5f077481')
BASE=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A4-20260926-5f077481')
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def size(p):return sum(q.stat().st_size for q in p.rglob('*') if q.is_file())
def main():
    start=time.perf_counter();receipt=json.loads((SRC/'DELIVERY_RECEIPT.json').read_bytes());prior=receipt['analysis_and_packaging_wall_seconds']
    assert prior<600 and not TARGET.exists()
    assert sha(SRC/'A4_COMMISSIONING_RESULT.zip')==receipt['sha256']
    fm=json.loads((SRC/'A4_COMMISSIONING_RESULT/FILE_MANIFEST.json').read_bytes())
    assert size(BASE)+size(SRC)*2<3000000000
    TARGET.mkdir()
    for n in ('A4_COMMISSIONING_RESULT.zip','DELIVERY_RECEIPT.json'):shutil.copyfile(SRC/n,TARGET/n)
    shutil.copytree(SRC/'A4_COMMISSIONING_RESULT',TARGET/'A4_COMMISSIONING_RESULT')
    for n,v in fm['files'].items():
        p=TARGET/'A4_COMMISSIONING_RESULT'/n;assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes'],n
    assert sha(TARGET/'A4_COMMISSIONING_RESULT.zip')==receipt['sha256']
    elapsed=time.perf_counter()-start;used=size(BASE)+size(SRC)+size(TARGET)
    assert used<3000000000 and prior+elapsed<600
    report={'workbench_delivery':str(TARGET),'authority_sha256':receipt['authority_sha256'],'zip_sha256':receipt['sha256'],'verified_payloads':len(fm['files']),'primary_project_workbench_bytes':used,'combined_disk_cap_bytes':3000000000,'analysis_packaging_delivery_wall_seconds':prior+elapsed,'reporting_cap_seconds':600,'scope':'New result contribution only; no existing vault file/navigation/Git changes; no simulation or replay.'}
    (TARGET/'COPY_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
