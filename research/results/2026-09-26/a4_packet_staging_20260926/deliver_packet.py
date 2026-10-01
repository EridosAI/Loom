"""Copy the sealed review packet to one new workbench INBOX directory; no Git or simulation."""
import hashlib,json,pathlib,shutil
from validate_packet import verify
ROOT=pathlib.Path(__file__).resolve().parent.parent
PACKET=ROOT/'exports/2026-09-26-A4-launch-packet-5f077481'
DEL=ROOT/'exports/2026-09-26-A4-launch-delivery-5f077481'
TARGET=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-26-A4-launch-packet-5f077481')
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    receipt=json.loads((DEL/'DELIVERY_RECEIPT.json').read_bytes())
    assert not TARGET.exists()
    assert sha(DEL/'A4_LAUNCH_PACKET.zip')==receipt['zip_sha256']=='84b351f3b8721351575a52c915733fbb9ad499e25f04b5fa6617c0744fa70b0e'
    verify(lambda n:(PACKET/n).read_bytes(),[p.relative_to(PACKET).as_posix() for p in PACKET.rglob('*') if p.is_file()])
    TARGET.mkdir()
    for n in ('A4_LAUNCH_PACKET.zip','DELIVERY_RECEIPT.json'):shutil.copyfile(DEL/n,TARGET/n)
    shutil.copytree(PACKET,TARGET/'A4_LAUNCH_PACKET')
    out=TARGET/'A4_LAUNCH_PACKET'
    checked=verify(lambda n:(out/n).read_bytes(),[p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()])
    assert sha(TARGET/'A4_LAUNCH_PACKET.zip')==receipt['zip_sha256']
    result={'target':str(TARGET),'zip_sha256':receipt['zip_sha256'],'zip_bytes':receipt['zip_bytes'],'verification':checked,'scope':'New contribution folder only; no vault Git, navigation, source or existing contribution changes. No execution.'}
    (TARGET/'COPY_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
