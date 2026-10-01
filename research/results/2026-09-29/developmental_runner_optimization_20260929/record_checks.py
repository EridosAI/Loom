"""Completed-engineering-record checks only, no new world trajectory."""
import argparse
import copy
import gc
import hashlib
import json
from pathlib import Path
import sys
import time
from benchmark import D,OUT,memory,REQUEST
from loom_p.records import state_hash
from loom_commissioning.runner import load_restart
from loom_developmental import codec,core
from loom_developmental.runner import Life,create_engineering_grant,file_hash
from loom_developmental.replay import reconstruct
from loom_developmental.verify import verify_store

def main():
    parser=argparse.ArgumentParser();parser.add_argument('check',choices=['matched-short','long-neural','selected-deep','codec-scaling'])
    choice=parser.parse_args().check;result_path=OUT/(choice+'.json')
    if result_path.exists():raise FileExistsError(result_path)
    start=time.perf_counter()
    if choice=='matched-short':
        old,_,_=load_restart(OUT.parent/'baseline/unprofiled/final.restart.json.gz')
        receipt=json.loads((OUT/'lean-short-final/segment-000.json').read_bytes())
        lean=codec.read(OUT/'lean-short-final'/receipt['final_checkpoint']['file'])['engine']
        assert codec.encode(core.causal_state(old))==codec.encode(core.causal_state(lean))
        result={'exact_causal_endpoint':True,'native_steps':60,'excluded_observer_cache':'Engine.last_native',
                'old_P_state':state_hash(old.organism),'lean_P_state':state_hash(lean.organism),'new_world_steps':0}
    elif choice=='long-neural':
        result=reconstruct(OUT/'long',first_index=1,last_index=60000)
        del result['engine'];result['new_world_steps']=0
    elif choice=='selected-deep':
        count=0
        def observe(index,e,diag):
            nonlocal count
            assert diag['native_index']==index
            count+=1
        result=reconstruct(OUT/'long',first_index=59981,last_index=60000,deep=True,fields=True,callback=observe)
        receipt=json.loads((OUT/'long/segment-000.json').read_bytes())
        saved=codec.read(OUT/'long'/receipt['final_checkpoint']['file'])['engine']
        assert codec.encode(core.causal_state(result['engine']))==codec.encode(core.causal_state(saved))
        del result['engine'];result.update(exact_final_causal_state=True,deep_rows=count,new_world_steps=0,
            fields_scope='reconstructed realized fields from saved body/stocks; no body or new trajectory evolution')
    else:
        chunk=codec.read(sorted((OUT/'long').glob('chunk-*.ld'))[0]);expected=hashlib.sha256(codec.encode(chunk)).hexdigest()
        gc.collect();blocks=[];start_block=time.perf_counter()
        for i in range(1,1801):
            blob=codec.encode(chunk);restored=codec.decode(blob)
            assert hashlib.sha256(codec.encode(restored)).hexdigest()==expected
            if i%100==0:
                blocks.append({'chunks_processed':i,'native_rows_processed':i*100,'wall_seconds':time.perf_counter()-start_block,**memory()})
                start_block=time.perf_counter()
        result={'scope':'same saved 100-row chunk reused; NOT a 1800-second life',
            'native_rows_processed':180000,'new_world_steps':0,'P_calls':0,'blocks':blocks,'bytes_equal':True}
    result['wall_seconds']=time.perf_counter()-start;result['memory']=memory()
    result_path.write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
