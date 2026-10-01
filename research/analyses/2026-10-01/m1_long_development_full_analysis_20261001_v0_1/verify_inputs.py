"""Full byte verification, independently of the analysis reductions."""
from common import *
import time
started=time.perf_counter();fail=[];count=0
for item in SEAL['files']:
    p=EX/item['path']
    if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:fail.append(item['path'])
    count+=1
archive=ROOT/'M1_RESURRECTION_SANDBOX_20260930_v0_1.zip'
ah=sha(archive);assert ah=='a165c5c48e4b9ed6a84a8ba02b7b1bc23ca57f43f38bfe6d0058694969e7e651'
assert not fail
sources=[BASE/'configuration.json',BASE/'loom_p/neural.py',BASE/'loom_p/geometry.py',BASE/'loom_p/physics.py',BASE/'loom_p/schema.py',schema_file,decoder,PREP/'sandbox_core.py',PREP/'sandbox_evidence.py',PREP/'sandbox_runner.py',ROOT/'motor_commissioning_preparation_20260930_v0_2/loom_motor_commissioning/motor.py']
save('INPUT_PROVENANCE.json',dict(status='PASS',execution_files=count,execution_bytes=SEAL['bytes'],execution_seal_path=str(OLD/'EXECUTION_CUSTODY_SEAL.json'),execution_seal_sha256=sha(OLD/'EXECUTION_CUSTODY_SEAL.json'),archive=dict(path=str(archive),bytes=archive.stat().st_size,sha256=ah),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],passive_verification_seconds=time.perf_counter()-started,new_simulation_steps=0))
print('PASS: all sealed execution files and original archive byte-identical; no simulation.')
