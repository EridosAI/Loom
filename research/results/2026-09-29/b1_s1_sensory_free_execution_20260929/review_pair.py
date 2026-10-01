"""Saved-data review only, after the single worker has exited. No world replay."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,time
S=Path(__file__).resolve().parent;ROOT=S.parent;OUT=S/'run-001';REPORT=S/'review'
PRIOR=ROOT/'b1_minimal_execution_20260929'
R=ROOT/'exports/2026-09-29-B1-S1-sensory-free-900s-proposal'
CASE='B1-MINIMAL-S1-SENSORY-FREE'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def write(p,v):
    with Path(p).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def inventory(p):return {x.relative_to(p).as_posix():{'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(p.rglob('*')) if x.is_file()}
def check(ok,why):
    if not ok:raise ValueError(why)
def main():
    execution=read(OUT/'EXECUTION_RESULT.json')
    REPORT.mkdir(exist_ok=False);start=time.perf_counter()
    write(REPORT/'REVIEW_START.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'reporting_limit_seconds':1800,'script_sha256':sha(__file__),'saved_data_only':True})
    preserved=read(OUT/'PRESERVED_FULL_AND_PRIOR_INVENTORY.json')
    check(inventory(PRIOR)==preserved,'prior FULL evidence changed')
    full=read(PRIOR/'review/B1-MINIMAL-S1-FULL.json')
    write(REPORT/'PRESERVED_S1_FULL_RESULT.json',full)
    null=None;error=None
    try:
        check(execution['attempts']==1,'no single-case attempt record')
        # Reuse the previously verified saved-record reviewer unchanged. Only its
        # input/output directory bindings are different; no apparatus is patched.
        path=PRIOR/'review_saved_records.py'
        check(sha(path)==read(PRIOR/'review/REVIEW_START.json')['script_sha256'],'original saved-data auditor changed')
        spec=importlib.util.spec_from_file_location('saved_B1_auditor',path)
        audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
        audit.S=S;audit.OUT=OUT;audit.REPORT=REPORT;audit.R=R;audit.START=start
        null=audit.review_case(CASE)
        check(null['initial_state_sha256']==full['initial_state_sha256'],'paired complete initial state differs')
        check(null['arm']=='SENSORY-FREE' and null['nonbaseline_commands']==0 and null['hold_decisions']==0,
              'sensory-free law differs from fixed (0.30,0.30)')
    except Exception as exc:
        import traceback
        error={'error':repr(exc),'traceback':traceback.format_exc()}
    check(inventory(PRIOR)==preserved,'read-only review changed prior evidence')
    matched=bool(null and null['initial_state_sha256']==full['initial_state_sha256'])
    full_witness=full['all_checks_passed'] and full['resolved_productive'] and full['feedback_changed_commands']
    null_completed=bool(null and null['all_checks_passed'] and null['completed_30_seconds'])
    null_unproductive=bool(null_completed and null['gross_transfer']==0 and not null['resolved_productive'])
    satisfied=bool(error is None and matched and full_witness and null_unproductive)
    result={'checkpoint':execution['checkpoint'],'new_outer_authority':execution['outer_authority_sha256'],
       'FULL':full,'SENSORY_FREE':null,'verification_error':error,'matched_complete_initial_state':matched,
       'FULL_productive_feedback_witness':full_witness,'SENSORY_FREE_completed_30_seconds':null_completed,
       'completed_null_unproductive':null_unproductive,
       'closure':'BOUNDED B1 MINIMAL-CLOSURE RULE SATISFIED' if satisfied else 'B1 MINIMAL CLOSURE UNRESOLVED',
       'allowed_positive_claim':"A fixed external controller restricted at runtime to the organism's permitted sensory history produced a bounded productive source interaction under held-out starting conditions." if satisfied else None,
       'FULL_acceptance_basis':'Jason explicitly accepted the preserved 29.79-second FULL result as the required productive witness. Its administrative cutoff and original receipt are unchanged.',
       'existing_FULL_evidence_unchanged':True,'new_cases_executed':execution['attempts'],
       'physical_replays':0,'controller_inference_during_review':0,'old_sealed_human_B1_accessed':False,
       'read_only_review_seconds':time.perf_counter()-start,
       'not_tested':['chemistry-hidden comparison','S2','S3','remaining 0.21 seconds of S1-FULL',
           'P learning','general navigation','developmental efficacy','Founder Search','C1/C2','nursery']}
    write(REPORT/'PAIRED_CLOSURE_RESULTS.json',result)
    print(json.dumps({'closure':result['closure'],'null':null,'verification_error':error},indent=2),flush=True)

if __name__=='__main__':main()
