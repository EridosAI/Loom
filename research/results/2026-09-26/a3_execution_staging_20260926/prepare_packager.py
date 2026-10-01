"""Prepare saved-evidence packaging tools only; do not read an active trajectory."""
import pathlib
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
old=ROOT/'a2_execution_staging_20260925/package_result.py'
t=old.read_text(encoding='utf-8').replace('A2','A3').replace('229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007','43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd')
t=t.replace("OUT=ROOT/'exports/2026-09-25-A3-commissioning-result-5f077481'","OUT=ROOT/'exports/2026-09-26-A3-commissioning-result-5f077481'")
t=t.replace('c080d089f3be5f65e88a9bdbcd774421197483d79d0a6e4ce8d7cb178eaed1c3','4c580299d098ad26eb5c6be4dd98e4e26e1fb8e4c766fa8591d516fdb6fdcfce')
t=t.replace("'wall_ceiling_seconds':3600","'wall_ceiling_seconds':4200")
t=t.replace('historical A1/V3 source evidence','historical A1/A2/V3 source evidence')
with (S/'package_result.py').open('x',encoding='utf-8') as f:f.write(t)
compile(t,str(S/'package_result.py'),'exec')
print('A3 result packager prepared; no result read or output package created.')
