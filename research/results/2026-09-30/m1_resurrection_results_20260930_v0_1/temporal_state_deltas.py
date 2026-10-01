"""NON-CANONICAL RESURRECTION SANDBOX. Plain saved arrays; no Loom object construction."""
import json
import numpy as np
import analyse_passive as m

def main():
    summary=json.loads((m.OUT/'DEVELOPMENTAL_SUMMARY.json').read_bytes())
    seal=json.loads((m.OUT/'EXECUTION_CUSTODY_SEAL.json').read_bytes());hashes={r['path']:r['sha256'] for r in seal['files']}
    rows=[]
    for candidate in summary['temporal_candidates']:
        name=candidate['life_id'];store=m.EX/'lives'/name;states=[]
        for checkpoint in candidate['checkpoint_comparison']:
            filename=checkpoint['file']
            if filename=='authoritative-final':
                stage='overnight' if (store/'overnight-RECEIPT.json').exists() else 'pilot'
                filename=json.loads((store/(stage+'-RECEIPT.json')).read_bytes())['final_checkpoint']['file']
            if filename=='last-full-checkpoint-not-endpoint':
                filename=next(r for r in json.loads((m.OUT/'HOST_STOP_DENOMINATOR.json').read_bytes())['rows'] if r['life_id']==name)['last_full_checkpoint']
            path=store/filename;e=m.attrs(m.read_data(path,hashes[path.relative_to(m.EX).as_posix()])['engine']);o=m.attrs(e['organism'])
            h=m.attrs(o['association'])['H'];states.append(dict(age=e['time'],theta=m.attrs(o['regulator'])['theta'],H=np.concatenate([h[k].ravel() for k in sorted(h)])))
        base=states[0];deltas=[]
        for v in states[1:]:
            td=v['theta']-base['theta'];hd=v['H']-base['H'];deltas.append((td,hd))
        row=dict(life_id=name,checkpoint_ages=[s['age'] for s in states],bank_delta_norms=[np.linalg.norm(t,axis=(1,2)).tolist() for t,h in deltas],
            H_delta_norms=[float(np.linalg.norm(h)) for t,h in deltas],causal_dependence_established=False)
        if len(deltas)==2:
            a,b=deltas
            row['bank_change_direction_cosine']=float(np.sum(a[0]*b[0])/(np.linalg.norm(a[0])*np.linalg.norm(b[0])))
            row['H_change_direction_cosine']=float(a[1]@b[1]/(np.linalg.norm(a[1])*np.linalg.norm(b[1])))
        rows.append(row)
    m.save('TEMPORAL_STATE_DELTAS.json',dict(label=m.LABEL,kind='DESCRIPTIVE_CHECKPOINT_DIFFERENCES',rows=rows,new_simulation_steps=0,
        limitation='Changes persist numerically across stored checkpoints; this does not attribute them to the selected event or establish that later behavior depends on them.'))
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
