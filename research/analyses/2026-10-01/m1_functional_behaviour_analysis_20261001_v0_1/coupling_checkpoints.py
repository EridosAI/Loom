"""Sparse exact feature receiver omission; no state update or reconstructed history."""
from common import *
rows=[]
for number in range(1,13):
    life=f'RS-M1-{number:03d}';cut=record(life)['curve_cutoff']
    for file in p.checkpoint_paths(life):
        e=attrs(rd(file)['engine'])
        if e['time']>cut:continue
        o=attrs(e['organism']);r=attrs(o['regulator']);d=r['output_diagnostic'];a=attrs(o['association']);theta=r['theta']
        phi=np.r_[1,np.tanh(d['Bq_q']+d['Bv_body']+d['bias'])];assert np.max(abs(phi-d['phi']))<1e-14
        learned=np.einsum('dof,f->do',theta,phi,optimize=False);assert np.max(abs(learned-d['learned']))<1e-14
        withoutphi=np.r_[1,np.tanh(d['Bv_body']+d['bias'])];without=np.einsum('dof,f->do',theta,withoutphi,optimize=False)
        delta=controls(learned,d['exploration'],d['need'])-controls(without,d['exploration'],d['need'])
        row=dict(life=life,age=e['time'],native_index=e['native_index'],file=file.name,sha256=p.HASHES[file.relative_to(EX).as_posix()],H_norm=math.sqrt(sum(float((v*v).sum()) for v in a['H'].values())),q_norm=norm(a['q']),feature_q_input_norm=norm(d['Bq_q']),body_feature_input_norm=norm(d['Bv_body']),q_feature_phi_delta=norm(phi-withoutphi),q_feature_E_logit_effect=norm((learned-without)[0]),q_feature_I_logit_effect=norm((learned-without)[1]),q_feature_current_delta_left=delta[8],q_feature_current_delta_right=delta[9],q_feature_current_RMS=rms(delta[8:10]),q_feature_attenuation_RMS=rms(delta[10:12]),q_feature_support_RMS=rms(delta[:8]))
        for bank,name in ((0,'E'),(1,'I')):
            row[name+'_support_weights_norm']=norm(theta[bank,:8]);row[name+'_current_weights_norm']=norm(theta[bank,8:10]);row[name+'_attenuation_weights_norm']=norm(theta[bank,10:12]);row[name+'_current_learned_logits_RMS']=rms(learned[bank,8:10]);row[name+'_current_feature_bias_term_RMS']=rms(theta[bank,8:10,0])
        rows.append(row)
    print(life+' sparse association-feature receiver checks complete',flush=True)
table('tables/SPARSE_ASSOCIATIVE_FEATURE_EFFECT.csv',rows)
save('SPARSE_RECEIVER_VERIFICATION.json',dict(status='PASS',records=len(rows),uses_stored_feature_body_operands=True,resurrection_stale_output_respected=True,new_draws=0,world_steps=0,continuous_wave_curve_claimed=False))
