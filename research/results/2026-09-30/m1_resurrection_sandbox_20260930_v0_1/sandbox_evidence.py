"""NON-CANONICAL RESURRECTION SANDBOX: lean facts, compact existing diagnostics."""
import paths
import numpy as np
from loom_motor_commissioning.evidence import native_row,NATIVE_FIELDS,SLICES,WIDTH,check_ledger,wave_row as motor_wave
from sandbox_core import LABEL
def wave_row(e,w):
    row=motor_wave(e,w);r=e.organism.regulator
    row.update(label=LABEL,time=e.time,packet_epoch=e.sandbox['packet_epoch_time'],
        regulator_reference_norm=np.linalg.norm(r.reference,axis=(1,2)),
        regulator_eligibility_norm=np.linalg.norm(r.eligibility,axis=(1,2)),
        regulator_learning_norm=np.linalg.norm(w['credit']['learning'],axis=(1,2)),
        regulator_reference_force_norm=np.linalg.norm(w['credit']['reference_force'],axis=(1,2)),
        body_mean=r.body_mean.copy(),
        sensory_reference_norm=np.array([[np.linalg.norm(c.shared_ref),np.linalg.norm(c.fine_ref)] for c in e.organism.cortices]),
        sensory_activity_norm=np.array([np.linalg.norm(c.x) for c in e.organism.cortices]),
        map_write_decay=np.stack([np.r_[v['write_norm'],v['decay_norm']] for v in w['association']['map_updates'].values()]))
    return row
