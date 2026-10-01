"""Record the separately requested clock restart and prepare exactly one new invocation."""
from pathlib import Path
import json,runpy
R=Path(__file__).resolve().parent.parent
old=R/'b1_execution_20260929'
record=json.loads((old/'EXPIRED_ZERO_STEP_RESTART_REQUEST.json').read_text(encoding='utf-8-sig'))
assert record['observed_lifecycle']=='ended' and record['native_steps']==record['commands']==record['simulated_seconds']==0
state=json.loads((old/'STATE.json').read_text(encoding='utf-8-sig'))
assert not (old/'STATE_AT_FIRST_HANDOFF.preserved.json').exists()
(old/'STATE_AT_FIRST_HANDOFF.preserved.json').write_bytes((old/'STATE.json').read_bytes())
state.update(status='ENDED / ZERO-STEP WALL ALLOWANCE EXPIRED / PRESERVED',live_services=0,
             restart_request_record='EXPIRED_ZERO_STEP_RESTART_REQUEST.json')
(old/'STATE.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
source=(R/'b1_compact_layout_20260927/prepare_authorized_launch_20260929.py').read_text(encoding='utf-8')
def once(a,b):
    global source
    assert source.count(a)==1
    source=source.replace(a,b)
once("OUT=ROOT/'b1_execution_20260929';PRIVATE=OUT/'private'","OUT=ROOT/'b1_execution_20260929_restart_01';PRIVATE=OUT/'private'")
once("roots=[PACK,PC,PREVIOUS,", "roots=[PACK,PC,PREVIOUS,ROOT/'b1_execution_20260929',")
start=source.index('    notice=')
end=source.index("    request=PRIVATE/",start)
source=source[:start]+'''    notice=('Jason explicitly requested: "I\\'ve just got back to my desk. Can you restart the clock?" on 2026-09-29. '
      'This is separate authorization for exactly one fresh B1-FULL-RAW attempt under the same canonical object '+AUTH+' and checkpoint '+APP+'. '
      'The preceding attempt expired at zero simulated seconds, zero native steps and zero commands; its complete record remains preserved. '
      'No timer or terminal record is rewritten. This creates a new invocation with the original 7200-second wall allowance, 30 simulated seconds and unchanged physical start. '
      'Prior permitted starting-reading exposure remains qualified; this is not an unseen first presentation. '
      'Jason chooses all commands. No assistant driving, retry after this attempt, continuation, tuning, substitution, plan view or interface change. '
      'CHEMISTRY-HIDDEN remains ungranted and evaluator feedback remains withheld until both cases end or explicit pair abandonment.')
'''+source[end:]
once("user_authorization_verbatim='Yes, authorised.',",'''user_authorization_verbatim="I've just got back to my desk. Can you restart the clock?",''')
source=source.replace('attempt=2,','attempt=3,')
once("prior_attempt='Preserved zero-step closure on 2026-09-27; earlier grant not reused.',",
     "prior_attempt='Zero-step closure on 2026-09-27 and zero-step wall expiry on 2026-09-29 preserved. Same execution object, new separate grant from explicit clock-restart request.',")
once("assert not OUT.exists(),'Invocation already reserved; no repeat.'", """assert not OUT.exists(),'Invocation already reserved; no repeat.'
    restart=read(ROOT/'b1_execution_20260929/EXPIRED_ZERO_STEP_RESTART_REQUEST.json')
    assert restart['native_steps']==restart['commands']==restart['simulated_seconds']==0
    assert sha(ROOT/'b1_execution_20260929/private/runs/B1-FULL-RAW/manifest.json')==restart['manifest_sha256']
    assert read(ROOT/'b1_execution_20260929/STATE.json')['live_services']==0""")
prepared=R/'b1_compact_layout_20260927/restart_01_preparation.py'
with prepared.open('x',encoding='utf-8') as f:f.write(source)
runpy.run_path(str(prepared),run_name='__main__')
