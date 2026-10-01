"""Unchanged Tier-1 native/events plus compact existing motor values per wave."""
import copy
from loom_developmental.evidence import NATIVE_FIELDS, SLICES, WIDTH, DYNAMIC, native_row, raw_tuple, check_ledger
from loom_developmental.evidence import wave_row as original_wave_row

def wave_row(e,w):
    row=original_wave_row(e,w)
    m=e.organism.motor
    row['motor_coupling']=copy.deepcopy(m.diagnostic)
    row['motor_coupling']['attenuation_used']=w['old_controls'][-2:].copy()
    if hasattr(m,'commissioning'):
        s=m.commissioning
        row['motor_process']={k:copy.deepcopy(v) for k,v in s.items() if k!='rng'}
        row['motor_process']['rng_counters']=s['rng'].counters.copy()
    else:
        row['motor_process']={'process':'CURRENT'}
    return row
