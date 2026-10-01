"""Copy the sealed HOLD proposal to one new workbench INBOX; no Git or simulation."""
import hashlib,json,pathlib,shutil
from validate_packet import verify
ROOT=pathlib.Path(__file__).resolve().parent.parent
PACKET=ROOT/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
DEL=ROOT/'exports/2026-09-26-A5-launch-delivery-HOLD-5f077481'
TARGET=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-26-A5-launch-packet-HOLD-5f077481')

def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    receipt=json.loads((DEL/'DELIVERY_RECEIPT.json').read_bytes());assert not TARGET.exists()
    assert receipt['launch_ready'] is False and sha(DEL/'A5_LAUNCH_PACKET_HOLD.zip')==receipt['zip_sha256']
    verify(lambda n:(PACKET/n).read_bytes(),[p.relative_to(PACKET).as_posix() for p in PACKET.rglob('*') if p.is_file()])
    TARGET.mkdir()
    for n in ('A5_LAUNCH_PACKET_HOLD.zip','DELIVERY_RECEIPT.json'):shutil.copyfile(DEL/n,TARGET/n)
    shutil.copytree(PACKET,TARGET/'A5_LAUNCH_PACKET_HOLD')
    out=TARGET/'A5_LAUNCH_PACKET_HOLD'
    checked=verify(lambda n:(out/n).read_bytes(),[p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()])
    assert sha(TARGET/'A5_LAUNCH_PACKET_HOLD.zip')==receipt['zip_sha256']
    result={'target':str(TARGET),'zip_sha256':receipt['zip_sha256'],'zip_bytes':receipt['zip_bytes'],'verification':checked,
      'scope':'One new contribution folder only; no vault Git/navigation/source or existing contribution edits. No simulation or grant.'}
    (TARGET/'COPY_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
