"""NON-CANONICAL RESURRECTION SANDBOX: single-worker append-only physical evidence."""
import paths
from paths import HERE,WT,D,MOTOR
import copy,hashlib,json,os,shutil,time,subprocess
from pathlib import Path
import numpy as np
from loom_motor_commissioning import codec
from loom_motor_commissioning.runner import identity as motor_identity,canonical,file_hash
from loom_motor_commissioning.motor import PARAMETERS
from sandbox_core import LABEL,step,resurrect,protected_state
import sandbox_evidence as evidence

EXECUTION_FILES=('paths.py','sandbox_core.py','sandbox_evidence.py','sandbox_runner.py','prepare.py','execute.py','test_components.py','test_recorder.py')
CHECKPOINT='1d7cd6fd450ea528562b2c825589ab4de18a5b38'
def atomic(path,value):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    tmp=path.with_name(path.name+'.partial')
    with tmp.open('xb') as f:f.write(canonical(value));f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
    return dict(path=path.name,sha256=file_hash(path),bytes=path.stat().st_size)
def source_gate():
    def git(*a):return subprocess.check_output(['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),*a],text=True).strip()
    if git('rev-parse','HEAD')!=CHECKPOINT or git('status','--porcelain'):raise ValueError('corrected source checkpoint/cleanliness changed')
    old=json.loads((MOTOR/'RUNTIME_IDENTITY.json').read_bytes());bound=motor_identity()
    if canonical(old)!=canonical(bound):raise ValueError('corrected M1 runtime changed')
    return dict(label=LABEL,base=bound,sandbox_files={n:file_hash(HERE/n) for n in EXECUTION_FILES},
        M1_parameters_sha256=hashlib.sha256(canonical(PARAMETERS)).hexdigest(),config_file_sha256=file_hash(D/'configuration.json'))
def runtime_check(expected):
    now=source_gate()
    if hashlib.sha256(canonical(now)).hexdigest()!=expected:raise ValueError('sandbox runtime identity changed')
    return now

class Budget:
    def __init__(self,start,initial_bytes):self.start=start;self.bytes=initial_bytes
    def add(self,size):self.bytes+=size
    def check(self):
        if time.perf_counter()-self.start>=25200:raise RuntimeError('RESOURCE_STOP seven-hour aggregate active wall ceiling')
        if self.bytes>=8000000000-32000000:raise RuntimeError('RESOURCE_STOP primary evidence closure reserve')

class Life:
    def __init__(self,e,store,authority,runtime,budget,stage,end_age,parent=None):
        self.e=e;self.store=Path(store);self.authority=authority;self.runtime=runtime;self.budget=budget
        self.stage=stage;self.end_age=end_age;self.parent=parent;self.started=time.perf_counter()
        if stage=='pilot':self.store.mkdir(parents=True,exist_ok=False)
        elif stage!='overnight' or parent is None:raise ValueError('invalid continuing stage')
        if not e.time<end_age<=4500 or e.status!='paused':raise ValueError('continuation state/target')
        if e.organism.rng.life!=authority['stream_life'] or e.organism.motor.commissioning['process']!='M1':raise ValueError('life or motor substitution')
        self.start_index=e.native_index;self.start_age=e.time;self.initial_digest=codec.digest(e)
        self.rows=[];self.waves=[];self.events=[];self.files=[];self.chunks=[];self.interventions=[];self.checkpoints=[]
        self.chunk_start_index=e.native_index;self.chunk_start_time=e.time
        self.ledger_max=0.;self.written=0;self.last_index=e.native_index
        self.write_json(f'{stage}-START.json',dict(label=LABEL,authority_sha256=authority['authority_sha256'],runtime=runtime,
            initial_digest=self.initial_digest,initial_index=e.native_index,initial_time=e.time,end_age=end_age,parent=parent))
        self.initial=self.checkpoint(stage+'-initial')
    def write_json(self,name,value):
        r=atomic(self.store/name,value);self.budget.add(r['bytes']);self.written+=r['bytes'];self.files.append(dict(r,file=name));return r
    def write_ld(self,name,value):
        r=codec.write(self.store/name,dict(label=LABEL,**value),1)
        self.budget.add(r['bytes']);self.written+=r['bytes'];self.files.append(r);return r
    def checkpoint(self,label):
        e=self.e;r=self.write_ld(f'{self.stage}-{e.native_index:09d}-{label}.ld',dict(engine=e,identity=self.runtime,life_id=self.authority['life_id']))
        restored=codec.read(self.store/r['file'],r['sha256'])['engine']
        if codec.encode(restored)!=codec.encode(e):raise ArithmeticError('checkpoint state/RNG continuity failure')
        restored.validate_state();self.checkpoints.append(r);return r
    def flush(self):
        if not self.rows:return
        e=self.e;r=self.write_ld(f'chunk-{self.chunk_start_index+1:09d}-{e.native_index:09d}.ld',dict(
            first_index=self.chunk_start_index+1,last_index=e.native_index,start_time=self.chunk_start_time,
            native=np.array(self.rows,dtype='<f8'),waves=self.waves,events=self.events,
            endpoint_status=e.status,terminal_dimension=e.terminal_dimension,
            P_endpoint_sha256=codec.digest(e.organism),rng_endpoint=e.organism.rng.counters.copy(),
            field_endpoint_sha256=hashlib.sha256(e.fields.tobytes()).hexdigest()))
        r.update(first_index=self.chunk_start_index+1,last_index=e.native_index);self.chunks.append(r)
        self.rows=[];self.waves=[];self.events=[];self.chunk_start_index=e.native_index;self.chunk_start_time=e.time
        if shutil.disk_usage(self.store).free<10000000000:raise RuntimeError('RESOURCE_STOP archive/temporary disk reserve')
    def advance(self):
        try:
            while self.e.time<self.end_age:
                self.budget.check();e=self.e;previous=e.time
                dt,w,events=step(e,self.end_age)
                if e.native_index!=self.last_index+1 or e.time!=previous+dt:raise ArithmeticError('native/time discontinuity')
                self.last_index=e.native_index;self.rows.append(evidence.native_row(e,dt));self.events.extend(events)
                self.ledger_max=max(self.ledger_max,evidence.check_ledger(events,e.c.arithmetic_tol))
                if w is not None:self.waves.append(evidence.wave_row(e,w))
                if len(self.rows)>=100:self.flush()
                if e.status=='terminal':
                    self.flush();n=e.sandbox['resurrections']+1;before=self.checkpoint(f'resurrection-{n:04d}-before')
                    intervention=resurrect(e);after=self.checkpoint(f'resurrection-{n:04d}-after')
                    ref=self.write_ld(f'resurrection-{n:04d}.ld',dict(intervention=intervention,before=before,after=after))
                    self.interventions.append(ref)
                    print(json.dumps(dict(label=LABEL,life=self.authority['life_id'],stage=self.stage,
                        event='RESURRECTION_VERIFIED',index=e.native_index,age=e.time,count=n,causes=intervention['restored_dimensions'])),flush=True)
                if e.native_index%6000==0:
                    self.flush();self.checkpoint('periodic')
                    print(json.dumps(dict(label=LABEL,life=self.authority['life_id'],stage=self.stage,event='PROGRESS',age=e.time,target=self.end_age,
                        active_wall=time.perf_counter()-self.budget.start,primary_bytes=self.budget.bytes)),flush=True)
            self.flush();e.validate_state();final=self.checkpoint('final')
            receipt=dict(label=LABEL,life_id=self.authority['life_id'],stage=self.stage,status='AGE_TARGET_COMPLETE',
                runtime=self.runtime,authority_sha256=self.authority['authority_sha256'],parent=self.parent,
                initial_checkpoint=self.initial,final_checkpoint=final,initial_digest=self.initial_digest,final_digest=codec.digest(e),
                initial_index=self.start_index,final_index=e.native_index,initial_age=self.start_age,final_age=e.time,
                end_age=self.end_age,files=self.files.copy(),chunks=self.chunks,interventions=self.interventions,checkpoints=self.checkpoints,
                new_native_steps=e.native_index-self.start_index,ending_wave=e.organism.wave_count,
                resurrections_total=e.sandbox['resurrections'],ledger_max=self.ledger_max,wall_seconds=time.perf_counter()-self.started,
                bytes_written=self.written,complete=True)
            self.write_json(f'{self.stage}-RECEIPT.json',receipt)
            return receipt
        except BaseException as error:
            fault=dict(label=LABEL,life_id=self.authority['life_id'],stage=self.stage,kind='DECLARED_SANDBOX_STOP',
                reason=f'{type(error).__name__}: {error}',index=self.e.native_index,age=self.e.time,last_recorded_index=self.last_index,
                unclosed_native_rows=len(self.rows),complete=False)
            try:self.write_json(f'{self.stage}-STOP.json',fault)
            except OSError:pass
            try:self.write_ld(f'{self.stage}-failure-tail.ld',dict(engine=self.e,unclosed_native=np.array(self.rows),
                unclosed_waves=self.waves,unclosed_events=self.events,fault=fault))
            except (OSError,ValueError):pass
            raise

def verify_segment(store,receipt):
    """No world/P execution. Native/ledger continuity includes explicit support edges."""
    store=Path(store);r=receipt
    for ref in r['files']:
        if file_hash(store/ref['file'])!=ref['sha256']:raise ValueError('evidence corruption')
    first=codec.read(store/r['initial_checkpoint']['file'],r['initial_checkpoint']['sha256'])['engine']
    last=codec.read(store/r['final_checkpoint']['file'],r['final_checkpoint']['sha256'])['engine']
    assert codec.digest(first)==r['initial_digest'] and codec.digest(last)==r['final_digest']
    last.validate_state();interventions={}
    for ref in r['interventions']:
        value=codec.read(store/ref['file'],ref['sha256']);x=value['intervention']
        before=codec.read(store/value['before']['file'],value['before']['sha256'])['engine']
        after=codec.read(store/value['after']['file'],value['after']['sha256'])['engine']
        assert codec.digest(before)==x['before_sha256'] and codec.digest(after)==x['after_sha256']
        assert before.status=='terminal' and np.any(before.body.reserves<=0) and after.status=='paused'
        assert protected_state(before)==protected_state(after)==x['protected_sha256']
        assert x['zero_learning_from_jump'] and x['long_term_and_RNG_identical']
        for d in (0,1):
            if before.body.reserves[d]<=0:
                assert after.body.reserves[d]==(.7,1.)[d] and after.organism.regulator.body_mean[d]==after.body.reserves[d]
            else:assert after.body.reserves[d]==before.body.reserves[d]
        if x['index'] in interventions:raise ValueError('duplicate intervention')
        interventions[x['index']]=x
    index=first.native_index;t=first.time;res=first.body.reserves.copy();stock=first.stocks.copy();wave=first.organism.wave_count;count=0
    for ref in r['chunks']:
        v=codec.read(store/ref['file'],ref['sha256']);assert v['first_index']==index+1 and v['start_time']==t
        cursor=0
        for row in v['native']:
            if index in interventions:res=interventions[index]['restored_reserves'].copy()
            index+=1;dt=row[evidence.SLICES['elapsed']][0];t+=dt
            assert t==row[0] and 0<dt<=.01
            n=int(row[evidence.SLICES['event_count']][0]);events=v['events'][cursor:cursor+n];cursor+=n;count+=n
            evidence.check_ledger(events,first.c.arithmetic_tol)
            for event in events:
                assert np.max(abs(np.array([event['energy_before'],event['integrity_before']])-res))<1e-11
                assert np.max(abs(np.asarray(event['stock_before'])-stock))<1e-11
                res=np.array([event['energy_after'],event['integrity_after']]);stock=np.array(event['stock_after'])
            assert np.array_equal(res,row[evidence.SLICES['reserves']]) and np.array_equal(stock,row[evidence.SLICES['stocks']])
        assert cursor==len(v['events']) and index==v['last_index']
        for w in v['waves']:
            wave+=1;assert w['wave']==wave and w['time']<=t
    if index in interventions:res=interventions[index]['restored_reserves'].copy()
    assert index==last.native_index and t==last.time==r['end_age'] and wave==last.organism.wave_count
    assert np.array_equal(last.body.reserves,res) and np.array_equal(last.stocks,stock)
    return dict(label=LABEL,status='PASS',life_id=r['life_id'],stage=r['stage'],native_rows=index-first.native_index,
        waves=wave-first.organism.wave_count,events=count,interventions=len(interventions),final_digest=codec.digest(last),world_steps=0)
