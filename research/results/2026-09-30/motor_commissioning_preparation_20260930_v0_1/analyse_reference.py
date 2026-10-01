"""Passive preserved-record reads and scalar quadrature; no world evolution."""
import paths
from paths import HERE,ROOT,PACKET,D
import copy,hashlib,json,math
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_hermitenorm,roots_legendre
from loom_developmental import codec,evidence
from loom_p.neural import follow

inputs={}
def sha(p):
    h=hashlib.sha256(p.read_bytes()).hexdigest();inputs[str(p)]=h;return h
def read(p,h=None):
    actual=sha(p)
    if h:assert actual==h
    return codec.read(p,actual)
def moments(x):
    return dict(mean=float(np.mean(x)),rms=float(np.sqrt(np.mean(x*x))),mean_absolute=float(np.mean(abs(x))),maximum_absolute=float(np.max(abs(x))))
rows=[]
for i in (1,2,3):
    name=f'FS-{i:03d}'
    e=read(PACKET/'initial_states'/(name+'.ld'))['engine'];m=copy.deepcopy(e.organism.motor);rng=copy.deepcopy(e.organism.rng)
    osc=[]
    # Reconstruct only the independently prescribed historical spontaneous terms.
    # No Motor.step, Organism.native, handoff, field or physical step is called.
    for k in range(9000):
        if k and k%50==0:m.drive=rng.draw('motor-noise',(2,),sign=True)
        osc.append(.25*np.sin(m.phase)+.1*m.nu)
        m.nu=follow(m.nu,m.drive,.01,1.);m.phase+=2*np.pi/np.array([7.,9.])*.01
        if k==5999:
            ck=ROOT/'founder_initial_execution_20260930/lives'/name/'checkpoint-000006000-s000-periodic.ld'
            saved=read(ck)['engine'].organism.motor
            assert np.array_equal(m.phase,saved.phase) and np.array_equal(m.nu,saved.nu) and np.array_equal(m.drive,saved.drive)
    store=ROOT/'founder_initial_execution_20260930/lives'/name
    receipt_path=store/'segment-000.json';sha(receipt_path);receipt=json.loads(receipt_path.read_bytes())
    native=[];effort=0.;basal=0.
    for f in receipt['chunks']:
        if f['last_index']>9000:break
        data=read(store/f['file'],f['sha256']);native.append(data['native'])
    a=np.concatenate(native);assert len(a)==9000
    u=a[:,evidence.SLICES['commands']];dt=a[:,evidence.SLICES['elapsed']][:,0]
    cost=float(np.sum(np.mean(abs(u),axis=1)*dt*.001))
    rows.append(dict(start=name,interval_seconds=90,spontaneous=moments(np.array(osc)),actual_command=moments(u),
        actual_effort_loss=cost,actual_effort_rate=cost/90,basal_loss=.0015*90,
        phase_noise_60s_saved_checkpoint_match=True))

# Gaussian quadrature integrates distributions, not temporal candidate realizations.
z,w=roots_hermitenorm(128);w=w/math.sqrt(2*math.pi)
def gaussian_metrics(v):
    o=.35*np.tanh(math.sqrt(v)*z)
    return np.array([np.dot(w,o*o),np.dot(w,abs(o)),np.dot(w,.8*abs(np.tanh(o)))*.001])
m1=gaussian_metrics(.5)
# Folded-normal integrals for absolute terms avoid the cusp at zero.
def smooth_metrics(v):
    def f(z,p):
        o=.35*math.tanh(math.sqrt(v)*z)
        value=o*o if p==0 else (o if p==1 else .0008*math.tanh(o))
        return value*math.exp(-z*z/2)*math.sqrt(2/math.pi)
    return np.array([quad(f,0,10,args=(p,),epsabs=1e-13)[0] for p in range(3)])
m1=smooth_metrics(.5)
gx,gw=roots_legendre(96)
positive_z=(gx+1)*5
positive_w=gw*5*np.exp(-positive_z**2/2)*math.sqrt(2/math.pi)
def vector_metrics(variance):
    o=.35*np.tanh(np.sqrt(variance[:,None])*positive_z[None,:])
    return np.stack([(o*o)@positive_w,o@positive_w,.0008*np.tanh(o)@positive_w],axis=1)
m2bounds=[]
for initial_ratio in (math.tanh(2.),math.tanh(6.)):
    acc=np.zeros(3)
    for n in range(8,25):
        ages=np.arange(n*50)*.01
        aa=np.exp(-ages);v=.5*(initial_ratio*aa*aa+(1-aa)**2)
        acc+=vector_metrics(v).sum(axis=0)*.01/17/8
    m2bounds.append(acc)

# Exact current noise second moment at pre-update native samples, stationary law.
a=math.exp(-.5);vb=(1-a)/(1+a)
ages=np.arange(50)*.01
noise_second=float(np.mean(1-2*np.exp(-ages)+(1+vb)*np.exp(-2*ages)))
current_rms=math.sqrt(.25**2/2+.1**2*noise_second)

# Scalar integration with 12 previous signs and a rigorous bounded tail.
# nu0=(1-a)*sum(a**j*sign[j]), omitted tail <= a**12.
nu=np.zeros(1)
for j in range(12):nu=np.r_[nu+(1-a)*a**j,nu-(1-a)*a**j]
phase=np.arange(2048)*2*np.pi/2048
current_abs=0.;current_proxy=0.
for age in ages[::5]:
    aa=math.exp(-float(age));nv=np.r_[aa*nu+(1-aa),aa*nu-(1-aa)]
    # Ten phase-of-refresh samples; retain resolution qualification in report.
    for ph in np.array_split(phase,32):
        x=.25*np.sin(ph[:,None])+.1*nv[None,:]
        current_abs+=float(np.sum(abs(x)))/(10*len(phase)*len(nv))
        current_proxy+=float(np.sum(.0008*abs(np.tanh(x))))/(10*len(phase)*len(nv))

stops=[]
for folder in ('founder_initial_execution_20260930','founder_expansion_execution_20260930'):
    for p in sorted((ROOT/folder).glob('FS-*_STOP.json')):
        r=json.loads(p.read_bytes())
        if r.get('complete'):
            sha(p);stops.append(r)
wall=np.array([x['active_wall_seconds']/x['simulated_seconds'] for x in stops]);byte=np.array([x['primary_bytes']/x['simulated_seconds'] for x in stops])
result=dict(scope='passive current records plus analytical distributions; zero world/native organism evolution',
    current_first90_records=rows,current_stationary=dict(spontaneous_bound=.35,noise_native_second_moment=noise_second,
        spontaneous_rms=current_rms,mean_absolute_approx=current_abs,neutral_effort_rate_approx=current_proxy,
        integration_qualification='12 sign terms; omitted spontaneous tail <= 0.1*exp(-6); refresh phase quadrature at 0,.05,...,.45; proxy not actual command'),
    M1=dict(spontaneous_bound=.35,stationary_spontaneous_rms=float(np.sqrt(m1[0])),mean_absolute=float(m1[1]),neutral_effort_rate=float(m1[2]),
        latent_sign_run_mean_common=.5*math.pi/math.acos(math.exp(-.5/16)),latent_sign_run_mean_differential=.5*math.pi/math.acos(math.exp(-.5/8))),
    M2=dict(spontaneous_bound=.35,stationary_spontaneous_rms_bounds=[float(np.sqrt(x[0])) for x in m2bounds],
        mean_absolute_bounds=[float(x[1]) for x in m2bounds],neutral_effort_rate_bounds=[float(x[2]) for x in m2bounds],
        birth_distribution_same_as_M1=True,mean_target_sign_bout_seconds=16,
        qualification='stationary renewal-boundary variance bounds propagated through exact native pre-update ages and uniform renewal durations; birth is a fresh renewal, not claimed stationary'),
    proxy_definition='instantaneous neutral command u=0.8*tanh(o); no direct/q/current; before existing 0.1s motor smoothing; not a world/effort forecast',
    resource=dict(completed_receipts=len(stops),wall_per_sim_seconds=dict(min=float(wall.min()),median=float(np.median(wall)),max=float(wall.max())),
        bytes_per_sim_seconds=dict(min=float(byte.min()),median=float(np.median(byte)),max=float(byte.max())),
        nine_by_90_wall_seconds=[float(v*810) for v in (wall.min(),np.median(wall),wall.max())],
        nine_by_90_primary_bytes=[float(v*810) for v in (byte.min(),np.median(byte),byte.max())]))
(HERE/'AMPLITUDE_EFFORT_REFERENCE.json').write_text(json.dumps(result,indent=2),encoding='utf8')
(HERE/'REFERENCE_INPUT_HASHES.json').write_text(json.dumps(inputs,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
