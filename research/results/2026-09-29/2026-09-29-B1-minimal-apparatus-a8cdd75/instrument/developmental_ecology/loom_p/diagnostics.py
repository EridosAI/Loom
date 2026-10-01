"""Predeclared observer-only information-loss calculations; no outcomes or tuning."""
import argparse
import copy
from dataclasses import asdict
from pathlib import Path
import numpy as np
from .schema import Config,Streams,radial
from .neural import Cortex,Association,follow
from .records import strict_bytes,view,code_identity

def history_through_contact_cortex(c,forces):
    cortex=Cortex(c,2,Streams(c.master_seed),np.zeros(8))
    rows=[]; packets=[]; z=np.zeros(2*c.widths[2]); mean=z.copy()
    # Frozen documented W/reference/opening: native activity/filter and packet path only.
    fixed=(cortex.shared.copy(),cortex.fine.copy(),cortex.shared_ref.copy(),cortex.fine_ref.copy(),cortex.opening.copy())
    for k,force in enumerate(forces):
        raw=1-np.exp(-force/.25)
        cortex.step(c,raw,np.full(len(cortex.groups),.5),c.native_dt)
        rows.append(dict(force=force.copy(),raw=raw,mean=cortex.diagnostic['mean'],residual=cortex.diagnostic['residual'],activity=cortex.x.copy()))
        cortex.shared,cortex.fine,cortex.shared_ref,cortex.fine_ref,cortex.opening=[x.copy() for x in fixed]
        if (k+1)%20==0:
            packet=cortex.packet(.2); beta=packet-mean; z=follow(z,beta,.2,c.tau_trace)
            packets.append(dict(packet=packet,old_mean=mean.copy(),beta=beta,trace=z.copy()))
            mean=follow(mean,packet,.2,c.tau_packet_mean)
    return dict(native=rows,waves=packets,frozen_weights=cortex.weights,frozen_A=cortex.A,provenance='Manufactured contact-load history through actual contact transfer formula and Cortex.step/packet; not claimed physically reachable')

def calculate(c):
    cases={}; n=40
    left=np.zeros((n,8)); left[3:6,0]=.2; left[11:14,2]=.2
    right=np.zeros_like(left); right[3:6,2]=.2; right[11:14,0]=.2
    reverse=left[::-1].copy()
    shift=np.roll(left,12,axis=0)
    sustained=np.zeros_like(left); sustained[2:,0]=.2
    slow=np.zeros_like(left); slow[:,0]=np.linspace(0,.2,n)
    for name,forces in [('pulse_0_then_2',left),('pulse_2_then_0',right),('reversed_local_history',reverse),('boundary_shift_12_samples',shift),('sustained_step',sustained),('slow_change',slow)]: cases[name]=history_through_contact_cortex(c,forces)
    pairs=[]
    for a,b in [('pulse_0_then_2','pulse_2_then_0'),('pulse_0_then_2','reversed_local_history'),('pulse_0_then_2','boundary_shift_12_samples'),('sustained_step','slow_change')]:
        def matrix(case,key): return np.array([r[key] for r in cases[case]['native']])
        pairs.append(dict(a=a,b=b,raw_distance=float(np.linalg.norm(matrix(a,'raw')-matrix(b,'raw'))),activity_distance=float(np.linalg.norm(matrix(a,'activity')-matrix(b,'activity'))),packet_distances=[float(np.linalg.norm(x['packet']-y['packet'])) for x,y in zip(cases[a]['waves'],cases[b]['waves'])],trace_distances=[float(np.linalg.norm(x['trace']-y['trace'])) for x,y in zip(cases[a]['waves'],cases[b]['waves'])]))
    # Two native activity paths with exactly equal trapezoid means and endpoints.
    path_a=np.array([0.,1.,0.,-1.,0.]); path_b=np.array([0.,-1.,0.,1.,0.])
    def packet(x): return np.array([np.trapezoid(x,dx=.05)/.2,x[-1]])
    compressed=dict(path_a=path_a,path_b=path_b,packet_a=packet(path_a),packet_b=packet(path_b),distance=float(np.linalg.norm(packet(path_a)-packet(path_b))),scope='Compression arithmetic only; no physical reachability or universal confusion claim')
    times=np.arange(0,91,dtype=float); adaptation=np.exp(-times/c.tau_receptor)
    association=Association(c,Streams(c.master_seed))
    for key,h in association.H.items():
        for j in range(4): h[j]=radial(np.ones_like(h[j]),.1)
    gates=np.full((8,4),.25); activity=np.full(c.central_width,.3); alpha=1-np.exp(-.25); norm_history=[]
    for sweep in range(61):
        norm_history.append(max(float(np.linalg.norm(activity[s])) for s in c.slices))
        if sweep<60: activity=(1-alpha)*activity+alpha*np.tanh(association.return_read(gates,activity))
    return dict(schema_version=1,configuration=asdict(c),configuration_sha256=c.identity(),code=code_identity(),cases=cases,distances=pairs,compression=compressed,adaptation=dict(seconds=times,residual=adaptation,scope='Exact frozen-input exponential receptor filter; no organism lifetime'),contraction=dict(block_norm=norm_history,per_sweep_bound=1-alpha+.7*alpha,map_norm=.1,scope='Manufactured legal frozen maps, zero query; weights remain nonzero while transient activity fades'),interpretation='Distances are descriptive, with zero cases retained. No learning efficacy or temporal adequacy pass gate; no tuning.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('output'); args=parser.parse_args()
    result=calculate(Config()); target=Path(args.output); target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(strict_bytes(view(result)))
    print('Saved fixed observer diagnostics:',target)
