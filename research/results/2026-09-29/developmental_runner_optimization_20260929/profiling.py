"""Context-attributed wall profiler. Its callback overhead is reported separately."""
import sys
import time
from collections import defaultdict

def label(file,name,inherited):
    f=file.replace('\\','/').lower();n=name.lower()
    if 'receiver' in n:return 'detached_D5'
    if n in ('checkpoint','save_restart','save_snapshot','load_restart','load_snapshot'):return 'snapshot_checkpoint'
    if n=='deepcopy' or f.endswith('/copy.py') or (n=='copy' and not f):return 'state_copy'
    if 'hash' in n or 'digest' in n or n in ('code_identity','apparatus_identity','file_identity','identity'):return 'hashing_binding'
    if 'json/' in f or n in ('pack','unpack','view','strict_bytes','canonical','state_bytes','scalar_count','encode','decode','put','get'):return 'serialization'
    if 'compress' in n or 'gzip' in f:return 'compression'
    if any(x in n for x in ('fsync','replace','read_bytes','write_bytes')) or n in ('write','read','open','close','flush') and not f:
        return 'filesystem_io'
    if 'validat' in n or n in ('require','_guard','cheap_finite','check_ledger'):return 'validation_accounting'
    if inherited in ('detached_D5','observer_diagnostics') and '/loom_p/' in f:return inherited
    if '/loom_p/neural.py' in f:return 'P_neural'
    if '/loom_p/physics.py' in f:return 'body_contact_viability'
    if '/loom_p/chemistry.py' in f:return 'chemical_field'
    if '/loom_p/geometry.py' in f and n=='transduce':return 'sensor_computation'
    if '/loom_commissioning/diagnostics.py' in f:return 'observer_diagnostics'
    if '/loom_developmental/evidence.py' in f:return 'tier1_extraction'
    if n=='append' and 'records.py' in f:return 'recorder_writes'
    if '/loom_developmental/codec.py' in f and n=='write':return 'recorder_writes'
    return inherited

class Meter:
    def __init__(self):self.stack=['other_harness'];self.seconds=defaultdict(float);self.events=0;self.overhead=0.
    def event(self,frame,event,arg):
        now=time.perf_counter();self.seconds[self.stack[-1]]+=now-self.last
        if event=='call':self.stack.append(label(frame.f_code.co_filename,frame.f_code.co_name,self.stack[-1]))
        elif event=='c_call':self.stack.append(label('',getattr(arg,'__name__',''),self.stack[-1]))
        elif event in ('return','c_return','c_exception'):
            if len(self.stack)>1:self.stack.pop()
        self.events+=1;self.last=time.perf_counter();self.overhead+=self.last-now
    def start(self):
        self.started=time.perf_counter();self.last=self.started;sys.setprofile(self.event)
    def stop(self):
        sys.setprofile(None);elapsed=time.perf_counter()-self.started
        return {'exclusive_seconds':dict(self.seconds),'callback_seconds':self.overhead,
                'profiled_wall_seconds':elapsed,'events':self.events,
                'warning':'Context-attributed measured execution excludes callback time; profiling perturbs throughput. Unprofiled runs determine speed.'}
