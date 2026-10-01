"""Prepare review documents/references in this new export only; no test execution."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
TARGET=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
WORK=ROOT.parent.parent
def read(relative):return json.loads((ROOT/relative).read_bytes())
def sha(data):return hashlib.sha256(data).hexdigest()
def write(name,data):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data)
def copy(src,dest,expected=None):
    data=Path(src).read_bytes()
    if expected:assert sha(data)==expected
    write(dest,data)

delivery=read('provenance/ZIP.json')
copy(delivery['zip'],'reviewed_delivery/Loom_P_Apparatus_Correction_Review_20260924.zip',delivery['sha256'])
copy(ROOT/'portable/CORRECTION.patch','CORRECTION.patch','20e5bc0f285a5bac6e7c46443e117b4bfc54c06695c5d6b2e4a98ce38fd19ba1')
copy(Path(r'C:\Users\Jason\.codex\attachments\f48fee0a-91c6-48f5-95da-c9b471b61298\Pasted text.txt'),'references/FINAL_REVIEW_REQUEST.txt')
copy(WORK/'exports/2026-09-24-p-apparatus-review-05abf604/LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md','references/PREVIOUS_INDEPENDENT_HOLD_REVIEW.md','d315eaf57c2b25fc8bc1b0b7e2e60d55d926634791e05033c23a8ffedec03c08')
copy(TARGET/'docs/developmental_ecology/p_apparatus_correction_20260924/CORRECTION_REPORT.md','references/BUILDER_CORRECTION_REPORT.md','aea072288c3d1ca5d952ff34df66d59a57902621129a155c55319a576845a29f')
review=(ROOT/'LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md').read_text(encoding='utf-8')
table=review.split('## Concise closure table\n',1)[1].split('\n## Scope, sources and evidence boundary',1)[0]
write('CLOSURE_TABLE.md',('# Closure table — 9d31e790\n\n**HOLD BEFORE COUPLING COMMISSIONING**\n\n'+table.lstrip()).encode())
ids=read('provenance/scoped-complete/IDENTITIES.json');git=read('provenance/scoped-complete/GIT.json')
audit=read('authority_runtime/SUITE_AND_FAULT_AUDIT.json')
canonical=read('canonical-001/CANONICAL_AUTHORITY_RESULTS.json')
assert len(canonical['canonical_spec_fields'])==21
assert audit['summary']['pairs']==36 and audit['summary']['total_logs_audited']==72
assert audit['collection']['collected_total']==113
identity={'date':'2026-09-25','disposition':'HOLD BEFORE COUPLING COMMISSIONING',
 'corrected_checkpoint':git['head'],'previous_apparatus':git['parent'],'unchanged_P':git['P'],
 'branch':git['branch'],'target':str(TARGET),'P_runtime':ids['P'],'apparatus_runtime':ids['apparatus'],
 'configuration_semantic':ids['configuration_semantic'],'configuration_file':ids['configuration_file'],
 'patch':{'bytes':git['patch_bytes'],'sha256':git['patch_sha256']},'builder_zip':delivery,
 'EXP1_21':git['EXP1_21_trees'],
 'suite_composition':audit['collection']['composition'],'suite_results':{'worktree':'113 passed in 77.05s','portable':'113 passed in 60.96s'},
 'fault_audit':audit['summary'],
 'preservation':{'previous_P_files':792,'previous_apparatus_review_design_files':1908,'target_artifacts_unchanged':3106},
 'required_closures':['A-R1a: reject ambiguous approval representations','A-R1b: bind the actual invoked controller callable','A-R1c: validate pending-command and hold continuity across advancement/save/resume/replay'],
 'commissioning_authorized':False,'commissioning_executed_by_review':False,
 'authoritative_provenance_receipts':'provenance/scoped-complete/; supersedes restricted preliminary receipts'}
write('REVIEWED_IDENTITIES.json',json.dumps(identity,indent=2).encode())
readme='''# Loom P — independent post-correction review intake

**HOLD BEFORE COUPLING COMMISSIONING**

Apparatus `9d31e7902658b15762052a2a6a3d161d64338524`; previous HOLD `05abf60401d08f38750bca589b1c040e10513d7b`; unchanged P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Review date 2026-09-25.

Start with `LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md` or `CLOSURE_TABLE.md`. Three remaining approval-integrity defects require closure. The original clock comparison is independently verified, both full suites pass 113 tests, and all 36 delivered fault/control pairs reproduce. Passing counts do not cover the counterexamples.

- `REPRODUCTION_COMMANDS.md`: exact commands, expected RED/GREEN outcomes and fresh-output instructions.
- `REVIEWED_IDENTITIES.json` and `provenance/scoped-complete/`: reviewed identities and complete preservation/reconstruction receipts.
- `canonical-001/`: strict-parser comparisons and 20 independently rejected semantic substitutions.
- `authority_runtime/`: actual-callable and pending-hold counterexamples, replay consequences, neural/firewall regression, and independent audit of all 72 logs.
- `physical/`: independent Decimal clock oracle, manufactured pause/restart proofs, and a fresh original-05ab authority RED.
- `old-pairs-001/` and `new-pairs-001/`: all delivered RED/GREEN logs and command matrices.
- `reviewed_delivery/`: byte-identical corrected builder ZIP, expected SHA-256 `e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81`. Its nested archives preserve the earlier builder/reviewer packages.
- `references/` and `CORRECTION.patch`: latest review request, previous independent HOLD review, builder report and exact correction patch.
- `FILE_MANIFEST.json`: size/hash for every included payload file. The adjacent `INTAKE_RECEIPT.json` identifies the complete ZIP after reopening and verifying it.

All synthetic approval files are manufactured test data, NOT Jason approval. No commissioning case, 600-second life or new prehistory was run. This is an intake artifact only; no Workbench file was changed. Source paths in evidence preserve original execution provenance; see reproduction instructions before repeating elsewhere.

Disposable pytest temporary trees and the redundant extracted builder tree are excluded; full independent counterexample/clock component records, all 72 fault/control logs, reports and receipts are included. Incomplete preliminary provenance receipts are retained transparently and superseded by `scoped-complete/`.
'''
write('README.md',readme.encode())
print(json.dumps({'prepared':True,'canonical_fields':21,'fault_pairs':36,'suite_composition':identity['suite_composition'],'builder_zip_sha256':delivery['sha256']}))
