"""Adapt the preserved one-attempt dispatcher to the newly approved object only."""
import pathlib
S=pathlib.Path(__file__).resolve().parent
old=S.parent/'a2_execution_staging_20260925/execute_once.py'
text=old.read_text(encoding='utf-8')
text=text.replace('A2','A3').replace('229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007','43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd')
text=text.replace("for q in (R,ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481',ROOT/'exports/2026-09-25-A1-read-only-reanalysis-viewer-v1'):",
"for q in (R,ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481',ROOT/'exports/2026-09-25-A2-launch-packet-5f077481',ROOT/'exports/2026-09-25-A1-read-only-reanalysis-viewer-v1',D/'artifacts/first-commissioning-A1-20260925-5f077481',D/'artifacts/commissioning-A2-20260925-5f077481'):")
assert "'approved_case':'A3'" in text and 'commissioning-A3-20260925-5f077481' in text
assert text.count('run=runner.Run(')==1 and text.count('run.hold()')==1
with (S/'execute_once.py').open('x',encoding='utf-8') as f:f.write(text)
compile(text,str(S/'execute_once.py'),'exec')
print('A3 dispatcher prepared and syntax checked; no dispatcher invocation or simulation.')
