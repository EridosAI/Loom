"""P equations 1–21. No world geometry, time, IDs or stock in neural interfaces."""
import copy
import numpy as np
from scipy.special import expit
from .schema import Config, Streams, RAW_WIDTHS, radial, signed_anatomy

def follow(old,target,dt,tau):
    return old+(-np.expm1(-dt/tau))*(target-old)

def tangent_step(value,velocity,radius,dt,centred=False):
    raw=velocity.copy()
    if centred: velocity=velocity-velocity.mean(axis=0)
    removed=np.zeros_like(value)
    norm2=float(np.sum(value*value)); dot=float(np.sum(value*velocity))
    if norm2 >= radius*radius*(1-1e-12) and dot>0:
        removed=dot/max(norm2,np.finfo(float).tiny)*value
        velocity=velocity-removed
    tentative=value+dt*velocity
    if centred: tentative=tentative-tentative.mean(axis=0)
    result=radial(tentative,radius)
    return result,{"raw_velocity":raw,"removed_radial":removed,"finite_correction":result-tentative}

class Cortex:
    def __init__(self,cfg,index,rng,raw):
        self.index=index; self.groups=[np.array(g,dtype=int) for g in cfg.pools[index]]
        w=cfg.widths[index]; d=RAW_WIDTHS[index]; label=f"sensory-{index}"
        self.A=signed_anatomy(rng,label+'-A',(w,w),0.25)
        self.shared=signed_anatomy(rng,label+'-shared',(len(self.groups),d),0.05,rowwise=True)
        self.fine=rng.draw(label+'-fine',(w,d),anatomy=True,sign=True)*0.001
        for ids in self.groups:
            delta=self.fine[ids]; delta-=delta.mean(axis=0)
            self.fine[ids]=radial(delta,0.004)
        self.shared_ref=self.shared.copy(); self.fine_ref=self.fine.copy()
        self.opening=np.zeros(len(self.groups)); self.mean=np.array(raw,dtype=float).copy()
        self.x=np.zeros(w); self.C=np.zeros((w,w)); self.integral=np.zeros(w)
        self.diagnostic={}
    @property
    def weights(self):
        w=self.fine.copy()
        for g,ids in enumerate(self.groups): w[ids]+=self.shared[g]
        return w
    def step(self,c,raw,support,dt):
        """Old-state simultaneous RHS: equations 1,3,15,16; trapezoid (2)."""
        raw=np.asarray(raw,dtype=float)
        if raw.shape!=self.mean.shape or not np.isfinite(raw).all(): raise ValueError('Invalid receptor vector')
        x=self.x.copy(); weights=self.weights; residual=raw-self.mean
        lateral=self.C.copy(); np.fill_diagonal(lateral,0)
        formation=x[:,None]*residual[None,:]-x[:,None]**2*weights-c.competition*(lateral@weights)
        diag={"raw":raw.copy(),"mean":self.mean.copy(),"residual":residual,"x_old":x,"weights":weights,"formation":formation,"groups":[]}
        shared_old=self.shared.copy(); fine_old=self.fine.copy()
        for g,ids in enumerate(self.groups):
            fbar=formation[ids].mean(axis=0)
            spring=c.lambda_fine_min+c.lambda_immature*(1-self.opening[g])+c.lambda_reclaim*(1-support[g])
            coarse_formation=c.eta_shared*fbar
            coarse_reference=-c.rho_shared*(self.shared[g]-self.shared_ref[g])
            fine_formation=c.eta_fine*(formation[ids]-fbar)
            coarsening=-spring*self.fine[ids]
            reference=-c.rho_fine*(self.fine[ids]-self.fine_ref[ids])
            self.shared[g],sd=tangent_step(self.shared[g],coarse_formation+coarse_reference,c.shared_radius,dt)
            self.fine[ids],fd=tangent_step(self.fine[ids],fine_formation+coarsening+reference,c.fine_radius,dt,True)
            diag['groups'].append(dict(spring=spring,opening=float(self.opening[g]),support=float(support[g]),shared_formation=coarse_formation,shared_reference=coarse_reference,fine_formation=fine_formation,coarsening=coarsening,reference=reference,shared_projection=sd,fine_projection=fd,common_activity=float(x[ids].mean()),differential_activity=x[ids]-x[ids].mean()))
        self.shared_ref=follow(self.shared_ref,shared_old,dt,c.tau_shared_reference)
        self.fine_ref=follow(self.fine_ref,fine_old,dt,c.tau_fine_reference)
        self.opening=follow(self.opening,np.ones_like(self.opening),dt,c.tau_open)
        self.x=follow(x,np.tanh(weights@residual+self.A@x),dt,c.tau_x)
        self.mean=follow(self.mean,raw,dt,c.tau_receptor)
        self.C=follow(self.C,np.outer(x,x),dt,c.tau_coactivity)
        self.integral+=dt*(x+self.x)/2
        diag['x_new']=self.x.copy(); self.diagnostic=diag
    def packet(self,duration):
        result=np.concatenate((self.integral/duration,self.x))
        self.integral.fill(0)
        return result

class Association:
    def __init__(self,c,rng):
        self.slices=c.slices; self.widths=c.central_widths
        self.H={}; self.use={}; self.gate_vectors=[]; self.gate_bias=[]
        for m,pm in enumerate(self.widths):
            self.gate_vectors.append(signed_anatomy(rng,f"gate-{m}",(c.gate_branches,c.central_width-pm),0.2,True))
            self.gate_bias.append(rng.draw(f"gate-bias-{m}",(c.gate_branches,),anatomy=True,sign=True)*0.1)
            for n,pn in enumerate(self.widths):
                if m!=n:
                    self.H[(m,n)]=np.zeros((c.gate_branches,pm,pn))
                    self.use[(m,n)]=np.zeros(c.gate_branches)
        self.a=np.zeros(c.central_width); self.q=np.zeros(c.central_width)
        self.means=[np.zeros(w) for w in c.packet_widths]
        self.traces=[np.zeros(w) for w in c.packet_widths]
        self.write_count=0; self.diagnostic={}
    def packets_to_context(self,c,packets):
        old=[a.copy() for a in self.means]
        beta=[b-mu for b,mu in zip(packets,old)]
        self.traces=[follow(z,b,c.wave_dt,c.tau_trace) for z,b in zip(self.traces,beta)]
        psi=np.concatenate([np.concatenate((b,z)) for b,z in zip(beta,self.traces)])
        return beta,psi,old
    def gates(self,c,psi):
        gates=[]
        for m,sl in enumerate(self.slices):
            other=np.concatenate((psi[:sl.start],psi[sl.stop:]))
            unnorm=c.gate_epsilon+expit(self.gate_vectors[m]@other+self.gate_bias[m])
            gates.append(unnorm/unnorm.sum())
        return np.array(gates)
    def return_read(self,gates,a,details=False):
        q=np.zeros_like(a); contributions={}
        for (m,n),maps in self.H.items():
            part=np.einsum('jmn,n->jm',maps,a[self.slices[n]],optimize=False)*gates[m,:,None]
            q[self.slices[m]]+=part.sum(axis=0)
            if details: contributions[(m,n)]=part
        return (q,contributions) if details else q
    def read(self,c,psi,old_support):
        gates=self.gates(c,psi); gain=np.ones_like(psi); offset=0
        for m in range(4):
            unit=np.zeros(c.widths[m])
            for group in c.pools[m]:
                unit[group]=c.query_floor+(1-c.query_floor)*old_support[offset]; offset+=1
            gain[self.slices[m]]=np.tile(unit,4)
        y=gain*psi; start=self.a.copy(); sweeps=[start.copy()]
        alpha=-np.expm1(-c.wave_dt/(c.sweeps*c.tau_a))
        for _ in range(c.sweeps):
            q=self.return_read(gates,self.a)
            self.a=(1-alpha)*self.a+alpha*np.tanh(y+q)
            sweeps.append(self.a.copy())
        self.q,contributions=self.return_read(gates,self.a,True)
        self.diagnostic=dict(gates=gates,gain=gain,query=y,a_initial=start,a_final=self.a.copy(),sweeps=sweeps,q=self.q.copy(),contributions=contributions,read_write_count=self.write_count)
        return gates,contributions
    def write(self,c,psi,beta,gates,contributions):
        records={}
        for (m,n),maps in self.H.items():
            old=maps.copy(); old_use=self.use[(m,n)].copy()
            formation=c.wave_dt*c.eta_map*gates[m,:,None,None]*np.outer(psi[self.slices[m]],psi[self.slices[n]])[None,:,:]
            decay=-c.wave_dt*(c.lambda_map_min+c.lambda_unused*(1-old_use))[:,None,None]*old
            proposed=old+formation+decay
            for j in range(c.gate_branches): maps[j]=radial(proposed[j],c.map_radius)
            power=np.sum(contributions[(m,n)]**2,axis=1)
            drive=power/(c.use_epsilon+power)
            self.use[(m,n)]=follow(old_use,drive,c.wave_dt,c.tau_use)
            records[(m,n)]=dict(old_norm=np.linalg.norm(old,axis=(1,2)),new_norm=np.linalg.norm(maps,axis=(1,2)),write_norm=np.linalg.norm(formation,axis=(1,2)),decay_norm=np.linalg.norm(decay,axis=(1,2)),projection_norm=np.linalg.norm(maps-proposed,axis=(1,2)),old_use=old_use,use=self.use[(m,n)].copy(),use_drive=drive)
        self.means=[follow(mu,mu+b,c.wave_dt,c.tau_packet_mean) for mu,b in zip(self.means,beta)]
        self.write_count+=1; self.diagnostic['map_updates']=records

class Regulator:
    def __init__(self,c,rng,reserves):
        shape=(2,c.outputs,c.feature_width+1)
        self.theta=np.zeros(shape); self.reference=np.zeros(shape); self.eligibility=np.zeros(shape)
        self.body_mean=np.array(reserves,dtype=float).copy()
        self.Bq=signed_anatomy(rng,'regulator-Bq',(c.feature_width,c.central_width),0.25,True)
        self.Bv=signed_anatomy(rng,'regulator-Bv',(c.feature_width,2),0.5,True)
        self.bias=rng.draw('regulator-bias',(c.feature_width,),anatomy=True,sign=True)*0.1
        self.phi=np.zeros(c.feature_width+1); self.xi=np.zeros((2,c.outputs))
        self.h=np.zeros(c.group_count); self.current=np.zeros(2); self.attenuation=np.zeros(2)
        self.credit_diagnostic={}; self.output_diagnostic={}
    def credit(self,c,reserves):
        old_mean=self.body_mean.copy(); previous_xi=self.xi.copy(); previous_phi=self.phi.copy()
        trend=(reserves-old_mean)/c.tau_body
        self.body_mean=follow(old_mean,reserves,c.wave_dt,c.tau_body)
        self.eligibility=follow(self.eligibility,self.xi[:,:,None]*self.phi[None,None,:],c.wave_dt,c.tau_eligibility)
        learning=c.eta_bank*c.wave_dt*trend[:,None,None]*self.eligibility
        reference_force=-c.rho_bank*c.wave_dt*(self.theta-self.reference)
        tentative=self.theta+learning+reference_force
        for bank in range(2):
            for row in range(c.outputs): self.theta[bank,row]=radial(tentative[bank,row],c.bank_radius)
        self.reference=follow(self.reference,self.theta,c.wave_dt,c.tau_bank_reference)
        self.credit_diagnostic=dict(trend=trend,old_body_mean=old_mean,body_mean=self.body_mean.copy(),previous_xi=previous_xi,previous_phi=previous_phi,learning=learning,reference_force=reference_force,projection=self.theta-tentative,eligibility=self.eligibility.copy(),theta=self.theta.copy(),reference=self.reference.copy())
    def output(self,c,rng,q,reserves):
        evoked=self.Bq@q; body=self.Bv@reserves
        self.phi=np.concatenate(([1.0],np.tanh(evoked+body+self.bias)))
        self.xi=np.stack([rng.draw(f'regulation-{d}',(c.outputs,),sign=True) for d in ('E','I')])
        learned=np.einsum('dof,f->do',self.theta,self.phi,optimize=False)
        exploration=c.exploration*self.xi; logits=learned+exploration
        need=c.need_floor+(1-c.need_floor)*(1-reserves)
        weighted=need[:,None]*logits; g=c.group_count
        self.h=expit(weighted[:,:g].sum(axis=0))
        self.current=c.current_max/2*np.tanh(weighted[:,g:g+2]).sum(axis=0)
        self.attenuation=expit(c.attenuation_bias+weighted[:,g+2:g+4].sum(axis=0))
        self.output_diagnostic=dict(Bq_q=evoked,Bv_body=body,bias=self.bias.copy(),phi=self.phi.copy(),learned=learned,exploration=exploration,logits=logits,need=need,weighted=weighted,xi=self.xi.copy(),controls=self.controls.copy(),feature_saturation=np.abs(self.phi[1:]))
    @property
    def controls(self): return np.concatenate((self.h,self.current,self.attenuation))

class Motor:
    def __init__(self,c,rng):
        self.feedback=signed_anatomy(rng,'motor-feedback',(2,15),0.1)
        self.phase=rng.draw('motor-birth-phase',(2,))*2*np.pi
        self.nu=2*rng.draw('motor-birth-nu',(2,))-1
        self.drive=rng.draw('motor-noise',(2,),sign=True)
        self.tendency=np.zeros(2); self.command=np.zeros(2); self.integral=np.zeros(2)
        self.diagnostic={}
    def step(self,c,raw,q_motor,current,attenuation,dt):
        p=np.concatenate((raw[3],raw[2]))
        oscillator=c.motor_amplitude*np.sin(self.phase)+c.motor_noise_amplitude*self.nu
        direct=self.feedback@p; evoked=q_motor[2:4].copy()
        target=np.tanh(oscillator+direct+evoked+current)
        self.tendency=follow(self.tendency,target,dt,c.tau_motor)
        self.command=(1-attenuation)*self.tendency
        self.nu=follow(self.nu,self.drive,dt,c.tau_noise)
        self.phase+=2*np.pi/np.array(c.motor_periods)*dt
        self.integral+=dt*self.command
        self.diagnostic=dict(oscillator=oscillator,direct_feedback=direct,evoked=evoked,current=current.copy(),target=target,tendency=self.tendency.copy(),command=self.command.copy(),phase=self.phase.copy(),nu=self.nu.copy(),drive=self.drive.copy())

class Organism:
    """Only raw receptor tuple and two actual reserves cross the world interface."""
    input_allowlist=('light[10]','chemistry[4]','contact[8]','proprioception[7]','actual_energy','actual_integrity')
    def __init__(self,c,rng,raw,reserves):
        self.c=c.validate(); self.rng=rng
        self.cortices=[Cortex(c,m,rng,raw[m]) for m in range(4)]
        self.association=Association(c,rng); self.regulator=Regulator(c,rng,reserves); self.motor=Motor(c,rng)
        self.regulator.output(c,rng,self.association.q,np.array(reserves))
        self.association.means=[np.zeros(2*w) for w in c.widths]+[np.array([reserves[0]]),np.array([reserves[1]]),np.zeros(4),self.regulator.controls.copy()]
        self.wave_count=0; self.native_count=0; self.wave_elapsed=0.; self.last_wave={}
    def native(self,raw,dt,refresh_noise=False):
        if refresh_noise: self.motor.drive=self.rng.draw('motor-noise',(2,),sign=True)
        offset=0
        for cortex in self.cortices:
            n=len(cortex.groups)
            cortex.step(self.c,raw[cortex.index],self.regulator.h[offset:offset+n],dt); offset+=n
        self.motor.step(self.c,raw,self.association.q[self.c.slices[6]],self.regulator.current,self.regulator.attenuation,dt)
        self.wave_elapsed+=dt; self.native_count+=1
        return self.motor.command.copy()
    def handoff(self,reserves):
        c=self.c; r=self.regulator; a=self.association
        if abs(self.wave_elapsed-c.wave_dt)>1e-10: raise ValueError('No handoff on partial wave')
        old_controls=r.controls.copy()
        packets=[x.packet(c.wave_dt) for x in self.cortices]+[np.array([reserves[0]]),np.array([reserves[1]]),np.concatenate((self.motor.integral/c.wave_dt,self.motor.command)),old_controls]
        self.motor.integral.fill(0)
        beta,psi,old_means=a.packets_to_context(c,packets)
        r.credit(c,np.asarray(reserves))
        gates,contributions=a.read(c,psi,r.h.copy())
        r.output(c,self.rng,a.q,np.asarray(reserves))
        a.write(c,psi,beta,gates,contributions)
        self.wave_count+=1; self.wave_elapsed=0.
        self.last_wave=dict(wave=self.wave_count,packets=packets,old_means=old_means,beta=beta,traces=copy.deepcopy(a.traces),psi=psi,old_controls=old_controls,new_controls=r.controls.copy(),association=copy.deepcopy(a.diagnostic),credit=copy.deepcopy(r.credit_diagnostic),regulation=copy.deepcopy(r.output_diagnostic),ordering=['packet','previous_credit','old_map_read_4_sweeps_final_q','new_draw_controls','one_map_write_use_means'])
        return self.last_wave
