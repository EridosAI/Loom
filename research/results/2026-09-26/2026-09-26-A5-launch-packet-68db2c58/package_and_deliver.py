"""Saved-file packaging and new Workbench delivery only; no Loom imports."""
import argparse
import ast
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import zipfile
from validate_packet import verify, strict

ROOT=pathlib.Path(__file__).resolve().parent.parent
PACKET=ROOT/'exports/2026-09-26-A5-launch-packet-68db2c58'
ARCHIVE=ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.zip'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
DELIVERY=WB/'INBOX/2026-09-26-A5-launch-packet-68db2c58'
W=ROOT/'worktrees/loom-p-clock-correction-20260926'
APP='68db2c581f07200966d699a4f55a65f9b96df1e9'


def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def write(p,x):
    p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())


def folder_verify(p):
    return verify(lambda n:(p/n).read_bytes(),[q.relative_to(p).as_posix() for q in p.rglob('*') if q.is_file()])


def preserved():
    inventory=strict((PACKET/'HASH_BEFORE.json').read_bytes())
    assert all(sha(pathlib.Path(p))==h for p,h in inventory.items())
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    args=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
    assert subprocess.check_output(args+['rev-parse','HEAD'],env=env).decode().strip()==APP
    assert not subprocess.check_output(args+['status','--porcelain'],env=env).strip()
    return dict(protected_files_rechecked=len(inventory),all_unchanged=True,corrected_worktree_clean=True,apparatus_checkpoint=APP)


def prepare():
    result=folder_verify(PACKET)
    old=ast.parse((PACKET/'historical-held/instrument/developmental_ecology/loom_commissioning/controllers.py').read_text())
    new=ast.parse((PACKET/'instrument/developmental_ecology/loom_commissioning/controllers.py').read_text())
    before={n.name:n for n in old.body if isinstance(n,ast.FunctionDef)}
    after={n.name:n for n in new.body if isinstance(n,ast.FunctionDef)}
    names=['validate_plan','validate_privileged','privileged_input','command_pair','observe_without_interference']
    for n in names:assert ast.dump(before[n],include_attributes=False)==ast.dump(after[n],include_attributes=False),n
    write(PACKET/'IDENTITY_IMPLEMENTATION_CHECK.json',dict(
        classification='IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS',
        unchanged_function_AST=names,actuator_arithmetic_check='See SEMANTIC_DIFF.json; unchanged after approved stage selection except exact native-deadline context.',
        changed_live_hash_explanation='callable_identity normalizes co_filename but retains source line metadata in marshalled code objects. Insertion of the native selector moves later unchanged functions; their live hashes change even when their AST and behavior do not.',
        commands_executed=0,method='Source AST comparison only; functions are not invoked.'))
    (PACKET/'AUTHORING_AND_IDENTITY_NOTE.md').write_text('''# Preparation audit note

This task changes only the packet and its preparation utilities. The new instrument source is copied byte-for-byte from the requested clean checkpoint. The live implementation hashes of several unchanged controller helper functions differ because the binding includes code-object line metadata; source AST comparisons confirm their implementations are unchanged. The new clock/selector identity and the approved native scheduling changes remain explicit in the semantic comparison.

Three authoring checks stopped before a finished object existed: a correction-package manifest was first looked up under the wrong filename; the call guard initially classified a Python class definition as a constructor; and the actuator comparison initially included the old stage-selection loop. Source inspection resolved these utility issues: the correct manifest is ARTIFACT_MANIFEST.json; class definition bodies are distinct from construction; and actuator comparison starts after stage selection, whose change is the already-reviewed correction. No production code was changed and no scientific/trajectory difference was normalized. No world, command, prehistory or simulation RNG operation was attempted or executed in those checks. The completed guarded pass records its exact allowed-call inventory in PREPARATION_CHECKS.json.

Names such as `engine.py:Engine` and `schema.py:Streams` in that inventory denote Python class-definition bodies evaluated on import, not construction. No __init__, step, command, sensor or draw method was admitted. A pure waypoint_stage call selects an integer stage from declared deadlines; it neither reads the world nor computes an actuator command.

This audit note, semantic comparison, preservation receipts and packaging checks are derived preparation evidence. The exact manifest, bound procedure/interpretation files and instrument identities define the proposed future case. Its execution grant remains null. Historical metadata stays byte-exact under historical-held, and shared original references/cache reconstruct the complete old packet.
''',encoding='utf-8',newline='\n')
    shutil.copyfile(pathlib.Path(__file__),PACKET/'package_and_deliver.py')
    files={p.relative_to(PACKET).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(PACKET.rglob('*')) if p.is_file() and p.name!='FILE_MANIFEST.json'}
    # Include the separately archived historical manifest; exclude only the outer seal.
    hp=PACKET/'historical-held/FILE_MANIFEST.json'
    files['historical-held/FILE_MANIFEST.json']=dict(sha256=sha(hp),bytes=hp.stat().st_size)
    write(PACKET/'FILE_MANIFEST.json',dict(authority_sha256=result['authority_sha256'],files=files))
    result=folder_verify(PACKET)
    assert not ARCHIVE.exists()
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(PACKET.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(PACKET).as_posix())
    with zipfile.ZipFile(ARCHIVE) as z:zip_result=verify(z.read,z.namelist())
    assert result==zip_result
    receipt=dict(packet=str(PACKET),archive=str(ARCHIVE),archive_sha256=sha(ARCHIVE),archive_bytes=ARCHIVE.stat().st_size,
                 folder_and_zip_verified=True,validation=result,preservation=preserved(),
                 execution_grant=None,A5_executed=False)
    write(ARCHIVE.with_suffix('.receipt.json'),receipt)
    ARCHIVE.with_suffix('.zip.sha256').write_text(receipt['archive_sha256']+'  '+ARCHIVE.name+'\n')
    print(json.dumps(receipt,indent=2))


def deliver():
    assert DELIVERY.parent.resolve()==(WB/'INBOX').resolve()
    assert not DELIVERY.exists()
    result=folder_verify(PACKET)
    with zipfile.ZipFile(ARCHIVE) as z:assert verify(z.read,z.namelist())==result
    receipt=strict(ARCHIVE.with_suffix('.receipt.json').read_bytes())
    assert sha(ARCHIVE)==receipt['archive_sha256']
    DELIVERY.mkdir()
    target=DELIVERY/'A5_LAUNCH_PACKET'
    shutil.copytree(PACKET,target)
    shutil.copyfile(ARCHIVE,DELIVERY/'A5_LAUNCH_PACKET.zip')
    assert folder_verify(target)==result
    assert sha(DELIVERY/'A5_LAUNCH_PACKET.zip')==sha(ARCHIVE)
    with zipfile.ZipFile(DELIVERY/'A5_LAUNCH_PACKET.zip') as z:assert verify(z.read,z.namelist())==result
    receipt.update(workbench_packet=str(target),workbench_zip=str(DELIVERY/'A5_LAUNCH_PACKET.zip'),
                   workbench_all_payloads_verified=True,workbench_zip_verified=True,final_preservation=preserved())
    write(DELIVERY/'DELIVERY_RECEIPT.json',receipt)
    (DELIVERY/'A5_LAUNCH_PACKET.zip.sha256').write_text(receipt['archive_sha256']+'  A5_LAUNCH_PACKET.zip\n')
    write(ARCHIVE.with_suffix('.delivery.json'),receipt)
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--deliver',action='store_true');args=p.parse_args()
    deliver() if args.deliver else prepare()
