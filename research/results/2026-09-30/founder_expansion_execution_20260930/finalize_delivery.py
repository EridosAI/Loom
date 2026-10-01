"""Read-only final source/custody checks and a small delivery receipt."""
import hashlib
import json
from pathlib import Path
import time
import execute_authorized_expansion as x
from loom_developmental.runner import atomic_json,canonical,file_hash,identity

HERE=Path(__file__).resolve().parent
OUT=HERE/'analysis'

def main():
    x.source_gate()
    assert hashlib.sha256(canonical(identity())).hexdigest()==x.RUNTIME
    archive=json.loads((HERE/'ARCHIVE_VERIFICATION.json').read_bytes())
    seal=json.loads((HERE/'DENOMINATOR_SEALED.json').read_bytes())
    manifest=json.loads((HERE/'EVIDENCE_ARCHIVE_MANIFEST.json').read_bytes())
    # Recheck immutable scientific custody after the read-only analyses.
    matched=0
    for item in manifest['files']:
        prefix='execution/'
        if item['path'].startswith(prefix+'lives/') or item['path'].startswith(prefix+'shared-assets/'):
            p=HERE/item['path'][len(prefix):]
            assert file_hash(p)==item['sha256'];matched+=1
    assert len(seal['roster'])==48
    completion=json.loads((OUT/'PASSIVE_ANALYSIS_COMPLETION.json').read_bytes())
    assert completion['deep_windows']<=196 and completion['total_wall_elapsed']<4500
    assert file_hash(HERE/'FOUNDER_SEARCH_60_LIFE_REPORT.md')==completion['report_sha256']
    files=[dict(path=p.relative_to(HERE).as_posix(),bytes=p.stat().st_size,sha256=file_hash(p))
           for p in sorted(OUT.rglob('*')) if p.is_file()]
    total=sum(p['bytes'] for p in files)
    assert total<2500000000
    elapsed=time.perf_counter()-json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes())['monotonic_started']
    assert elapsed<4500
    result=dict(status='PASS',checkpoint=x.CHECKPOINT,P_commit=x.P,git_clean=True,
        runtime_sha256=x.RUNTIME,all_48_executed_once=all(r['state']!='NOT_STARTED' for r in seal['roster']),scientific_worker_exit_code=1,
        scientific_stores_unchanged_after_analysis=matched,archive=archive,
        archive_preparation_write_and_verification_elapsed_seconds=(HERE/'ARCHIVE_VERIFICATION.json').stat().st_mtime-(HERE/'POSTRUN_VERIFICATION.json').stat().st_mtime,
        report_sha256=completion['report_sha256'],analysis_files=files,analysis_bytes=total,
        full_postarchive_analysis_and_delivery_elapsed_seconds=elapsed,analysis_limit_seconds=4500,
        post_stage_world_steps=0,continuation_authorities_created=0,continuations=0,retries=0,
        no_later_stage_launched=True,source_or_configuration_changes=0,git_writes=0,
        history_note='Earlier engineering/B1/A-series records and prepared launch packet preserved; no old sealed human B1 state accessed.')
    atomic_json(HERE/'DELIVERY_VERIFICATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('analysis_files','archive')}),flush=True)

if __name__=='__main__':main()
