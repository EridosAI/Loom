"""Passive, timestamped operands and detached immediate-receiver sensitivities."""
import copy
import numpy as np
from scipy.special import expit
from loom_p.neural import follow
from loom_p.records import state_hash
from .contract import EXTERNAL, FIXED, SELECTION, require

def motor_receiver(before, after):
    c=before.c; m=before.organism.motor; r=before.organism.regulator
    d=after.organism.motor.diagnostic
    terms={'oscillator':c.motor_amplitude*np.sin(m.phase), 'noise':c.motor_noise_amplitude*m.nu,
           'direct_feedback':d['direct_feedback'], 'motor_evocation':d['evoked'], 'regulatory_current':d['current']}
    total=sum(terms.values()); dt=after.last_native['elapsed']
    def receive(value, attenuation=r.attenuation):
        target=np.tanh(value); tendency=follow(m.tendency,target,dt,c.tau_motor)
        return {'target':target,'tendency':tendency,'command':(1-attenuation)*tendency}
    baseline=receive(total)
    require(np.allclose(baseline['command'],d['command'],rtol=0,atol=1e-15), 'motor receiver reconstruction mismatch')
    return {'contributions':terms,'attenuation':r.attenuation.copy(),'baseline':baseline,
            'without':{**{k:receive(total-v) for k,v in terms.items()},'attenuation':receive(total,np.zeros(2))},
            'scope':'same frozen receiver, no alternate trajectory or benefit'}

def wave_receiver(before, after, wave):
    c=before.c; r=after.organism.regulator
    rd=wave['regulation']; a=before.organism.association; old_h=before.organism.regulator.h
    def association(psi, support):
        detached=copy.deepcopy(a)
        detached.read(c,psi,support)
        return detached.q.copy()
    q=association(wave['psi'],old_h)
    require(np.array_equal(q,wave['association']['q']), 'associative receiver reconstruction mismatch')
    def receiver(q_value, omit=None):
        evoked=r.Bq@q_value; body=r.Bv@after.body.reserves; bias=r.bias.copy()
        if omit=='evoked': evoked*=0
        if omit=='body': body*=0
        if omit=='bias': bias*=0
        features=np.concatenate(([1.],np.tanh(evoked+body+bias)))
        learned=np.einsum('dof,f->do',r.theta,features,optimize=False)
        exploration=rd['exploration'].copy()
        for bank in (0,1):
            if omit==f'learned_{bank}': learned[bank]*=0
            if omit==f'exploration_{bank}': exploration[bank]*=0
        weighted=rd['need'][:,None]*(learned+exploration); g=c.group_count
        controls=np.concatenate((expit(weighted[:,:g].sum(axis=0)),
            c.current_max/2*np.tanh(weighted[:,g:g+2]).sum(axis=0),
            expit(c.attenuation_bias+weighted[:,g+2:g+4].sum(axis=0))))
        return {'features':features,'weighted_logits':weighted,'controls':controls}
    baseline=receiver(q)
    require(np.array_equal(baseline['controls'],rd['controls']), 'regulator receiver reconstruction mismatch')
    omissions={name:receiver(q,name) for name in ('evoked','body','bias','learned_0','learned_1','exploration_0','exploration_1')}
    query_probes={}
    for m in range(4):
        psi=wave['psi'].copy(); psi[c.slices[m]]=0
        alternate=association(psi,old_h)
        query_probes[f'sensory_context_{m}']={'q':alternate,'q_difference':alternate-q,'receiver':receiver(alternate)}
    alternate=association(wave['psi'],np.zeros_like(old_h))
    query_probes['support_to_zero_with_query_floor']={'q':alternate,'q_difference':alternate-q,'receiver':receiver(alternate)}
    return {'baseline':baseline,'without':omissions,'query_support_dependencies':query_probes,
            'scope':'immediate defined read/receiver dependencies; unchanged RNG, maps and trajectory'}

def passive(before, after, wave, mode, discarded):
    """Every native alignment retained; expensive influence rule fixed in manifest."""
    before_hash=state_hash(before); after_hash=state_hash(after)
    row={'class':'CO','native_index':after.native_index,'input_time':before.time,'endpoint_time':after.time,
         'raw_step_start':[x.copy() for x in before.raw],'raw_endpoint':[x.copy() for x in after.raw],
         'mode':mode,'selection':SELECTION.copy()}
    if mode==EXTERNAL:
        row.update(neural_scope='inactive newborn object; no P experience or hypothetical action recorded')
    else:
        row['cortices']=[]
        for i,(old,new) in enumerate(zip(before.organism.cortices,after.organism.cortices)):
            hypothetical=discarded['hypothetical_sensory'][i] if mode==FIXED else None
            row['cortices'].append({'mean_old':old.mean.copy(),'mean_new':new.mean.copy(),
                'residual_used':before.raw[i]-old.mean,
                'activity_old':old.x.copy(),'activity_new':new.x.copy(),'activity_saturation':abs(new.x),
                'coactivity':new.C.copy(),'activity_integral':new.integral.copy(),
                'shared_old':old.shared.copy(),'fine_old':old.fine.copy(),
                'shared_reference':old.shared_ref.copy(),'fine_reference':old.fine_ref.copy(),
                'shared_applied_delta':new.shared-old.shared,'fine_applied_delta':new.fine-old.fine,
                'hypothetical_discarded':hypothetical,'pressures':copy.deepcopy(new.diagnostic['groups']),
                'weight_row_norms':np.linalg.norm(new.weights,axis=1),
                'within_pool_gram':[new.weights[g]@new.weights[g].T for g in new.groups]})
        if wave is not None:
            row['wave_alignment']={k:copy.deepcopy(wave[k]) for k in ('packets','old_means','beta','traces','psi')}
            row['wave_alignment']['query']=wave['association']['query'].copy()
            row['wave_alignment']['q']=wave['association']['q'].copy()
            row['credit_separate_E_I']={'actual_reserves':after.body.reserves,
                'old_eligibility':before.organism.regulator.eligibility.copy(),
                'old_theta':before.organism.regulator.theta.copy(),
                'old_reference':before.organism.regulator.reference.copy(),
                'applied_theta_delta':after.organism.regulator.theta-before.organism.regulator.theta,
                'credit':copy.deepcopy(wave['credit']), 'outputs':copy.deepcopy(wave['regulation'])}
            row['D5_wave']=wave_receiver(before,after,wave)
        if after.native_index%SELECTION['native_stride']==0 or wave is not None:
            row['D5_native']=motor_receiver(before,after)
    require(state_hash(before)==before_hash and state_hash(after)==after_hash, 'observer RNG/state interference')
    return row

def spectrum(activity):
    """Continuous spectrum; no invented numerical rank success threshold."""
    values=np.asarray(activity,dtype=float)
    require(values.ndim==2 and len(values)>1 and np.isfinite(values).all(), 'spectrum needs finite history')
    centred=values-values.mean(axis=0)
    return {'singular_values':np.linalg.svd(centred,compute_uv=False),
            'covariance':centred.T@centred/(len(values)-1),'sample_count':len(values),
            'rank_interpretation':'unresolved without precision/physical distinction analysis'}

def packet_pair_distances(histories, packets):
    """All candidate pair distances retained; no selection on downstream q."""
    require(len(histories)==len(packets), 'packet/history count mismatch')
    return [{'i':i,'j':j,'packet_distance':float(np.linalg.norm(np.asarray(packets[i])-packets[j])),
             'native_distance':float(np.linalg.norm(np.asarray(histories[i])-histories[j]))}
            for i in range(len(packets)) for j in range(i+1,len(packets))]
