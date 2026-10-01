"""Describe the retained V3 reader error; do not correct or rerun the checker."""
import gzip,hashlib,json,pathlib,shutil
S=pathlib.Path(__file__).resolve().parent
B=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\first-commissioning-A1-20260925-5f077481')
O=B/'read-only-review';T=B/'trajectory-001'
receipt=json.loads((T/'manifest.json').read_bytes())
with gzip.open(T/'sensor.jsonl.gz','rt',encoding='utf-8') as f:
    first=json.loads(next(f));second=json.loads(next(f))
finding={'classification':'Read-only post-check cardinality/schema assumption error; not established apparatus failure',
    'receipt_record_counts':receipt['records'],'first_sensor_stream_entry_keys':list(first),
    'first_entry_history_length':len(first['history']),'first_entry_initial_native_index':first['history'][0]['native_index'],
    'second_sensor_stream_entry_keys':list(second),'second_entry_native_index':second['native_index'],
    'reviewed_runner_behavior':'Run.__init__ appends one SensorHistory.display() envelope; Run.advance appends one history row per native step.',
    'failed_assertion':'len(native)==len(sensors)==len(diagnostic)',
    'unexecuted_following_checks':['display history versus sensor rows','issued versus delivered commands comparison in this reader',
        'raw native versus sensor equality','native versus sensor E/I cadence comparison','reader final session counter/state comparison'],
    'preceding_assertions_reached_without_error':['final manifest equals launch and receipt',
        'complete initial/final inactive organism state equality','initial/final organism RNG counter equality',
        'final sensor display closed-schema validation'],
    'independent_completed_check':'Existing verify_segment(replay=False) validated the issued-decision journal, native sequence, checksums, receipt counts, ledger and stop classification.',
    'disposition':'Preserve error and checker unchanged. V3 post-check remains incomplete. No corrected rerun, trajectory replay, patch or continuation.',
    'checker_sha256':hashlib.sha256((O/'read_results.py').read_bytes()).hexdigest()}
assert (O/'read_results.py').read_bytes()==(S/'read_results.py').read_bytes()
with (O/'V3_COUNT_FINDING.json').open('x',encoding='utf-8') as f:json.dump(finding,f,indent=2)
note='''# V3 post-check limitation — retained without correction

The post-check in `read_results.py` stopped at its line-69 assertion that native, sensor and diagnostic stream counts must match. The actual counts are 9,183 native, 9,184 sensor and 9,183 diagnostic entries. The first sensor entry is a complete initial display envelope at native index 0; the second is the native-index-1 row. The reviewed `runner.py` writes that initial envelope in `Run.__init__` (line 124), then a row per advanced step (line 230). The checker was authored for this execution and assumed the wrong stream shape. This is a reader error, not evidence that the apparatus produced an extra native update.

The original exception and calculation source remain unchanged. V3's later per-row comparisons were not reached: display versus stream rows, raw/native equality, issued versus delivered commands in this reader, E/I comparisons and its final counter/state assertions remain incomplete. The preceding full inactive-organism/RNG comparisons and display-schema check had completed before the assertion. Separately, the reviewed segment validator completed with replay=false, validating its issued-decision journal, native sequence, receipt counts, file hashes, ledger and stop classification.

This finding explains the count discrepancy from saved records and existing source. It does not supply a corrected calculation or label V3 complete. No checker or apparatus patch, rerun, physical replay, resume or second trajectory was performed. All physical observations retain the limitation of this incomplete post-check.
'''
with (O/'V3_POST_CHECK_LIMITATION.md').open('x',encoding='utf-8') as f:f.write(note)
shutil.copyfile(S/'record_v3_finding.py',O/'record_v3_finding.py')
print(json.dumps(finding,indent=2))
