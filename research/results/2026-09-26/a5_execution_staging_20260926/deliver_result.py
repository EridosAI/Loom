"""New Workbench delivery only. Does not alter originals or execute a world."""
import datetime,json,pathlib,shutil
from package_result import ROOT,BASE,REVIEW,EXPORT,PACK,ZIP,sha,size,guard,verify_folder,verify_zip,write,js
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
DEST=WB/'INBOX/2026-09-26-A5-commissioning-result-68db2c58'

def main():
    assert DEST.parent.resolve()==(WB/'INBOX').resolve() and not DEST.exists()
    count=verify_folder(PACK);assert verify_zip(ZIP)==count
    estimated=size(PACK)+size(ZIP)+100_000;guard(estimated)
    DEST.mkdir()
    shutil.copytree(PACK,DEST/'A5_COMMISSIONING_RESULT')
    shutil.copyfile(ZIP,DEST/'A5_COMMISSIONING_RESULT.zip')
    assert verify_folder(DEST/'A5_COMMISSIONING_RESULT')==count
    assert sha(DEST/'A5_COMMISSIONING_RESULT.zip')==sha(ZIP) and verify_zip(DEST/'A5_COMMISSIONING_RESULT.zip')==count
    before=js(BASE/'ORIGINAL_FILES_BEFORE.json');assert all(sha(pathlib.Path(p))==v for p,v in before.items())
    raw=js(REVIEW/'RAW_EVIDENCE_BEFORE_ANALYSIS.json');assert all(sha(pathlib.Path(p))==v for p,v in raw.items())
    receipt=js(EXPORT/'PACKAGE_RECEIPT.json')
    receipt.update(workbench_packet=str(DEST/'A5_COMMISSIONING_RESULT'),workbench_zip=str(DEST/'A5_COMMISSIONING_RESULT.zip'),
                   workbench_payloads_verified=True,workbench_zip_verified=True,originals_and_raw_still_unchanged=True,
                   combined_new_bytes_after_delivery=guard(20000),
                   reporting_elapsed_seconds=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(js(BASE/'EXECUTION_RESULT.json')['first_stop_utc'])).total_seconds())
    write(DEST/'DELIVERY_RECEIPT.json',receipt);write(EXPORT/'DELIVERY_RECEIPT.json',receipt)
    (DEST/'A5_COMMISSIONING_RESULT.zip.sha256').write_text(sha(ZIP)+'  A5_COMMISSIONING_RESULT.zip\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
