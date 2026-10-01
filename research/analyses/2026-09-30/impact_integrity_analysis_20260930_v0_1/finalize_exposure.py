"""Clip sampled exposure quadrature to each stated interval, without interpolation of physics."""
import csv,json
import numpy as np
from impact_analysis import HERE,read,initial,gap_series

def overwrite_json(path,obj):path.write_text(json.dumps(obj,separators=(',',':'),allow_nan=False),encoding='utf-8')
def overwrite_csv(path,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        for r in rows:w.writerow({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def main():
    halves=read(HERE/'POST_INJURY_HALF_EXPOSURE.json');allblocks=[];allrates=[]
    for name in read(HERE/'DAMAGED_LIFE_AUDIT.json')['damaged_lives']:
        data=dict(np.load(HERE/(name+'_RECORDED_NATIVE.npz')));e=initial(name);t=data['time'][:,0];dt=data['elapsed'][:,0]
        blocks=read(HERE/(name+'_EXPOSURE_BLOCKS.json'))
        with (HERE/(name+'_BEFORE_AFTER_RATES.csv')).open() as f:rates=list(csv.DictReader(f))
        gaps={key:gap_series(e,key,data)[0] for key in {z['collider'] for z in blocks}}
        def update(z,keys):
            lo=float(z['start']);hi=float(z['end']);weight=np.maximum(0,np.minimum(t,hi)-np.maximum(t-dt,lo));gap=gaps[z['collider']]
            for key,threshold in keys:z[key]=float(weight[gap<=threshold].sum())
            z['exposure_duration_basis']='native endpoint indicator times clipped native-interval overlap; sampled quadrature, not exact continuous gap occupancy'
        for z in blocks:update(z,[('time_within_0_25',.25),('time_within_1',1.)])
        for z in rates:update(z,[('within_0_25_seconds',.25),('within_1_seconds',1.)])
        for z in halves:
            if z['life_id']==name:update(z,[('time_within_0_25',.25)])
        overwrite_json(HERE/(name+'_EXPOSURE_BLOCKS.json'),blocks);overwrite_csv(HERE/(name+'_EXPOSURE_BLOCKS.csv'),blocks)
        overwrite_csv(HERE/(name+'_BEFORE_AFTER_RATES.csv'),rates);allblocks+=blocks;allrates+=rates
    overwrite_csv(HERE/'ALL_EXPOSURE_BLOCKS.csv',allblocks);overwrite_csv(HERE/'ALL_BEFORE_AFTER_RATES.csv',allrates)
    overwrite_json(HERE/'POST_INJURY_HALF_EXPOSURE.json',halves);overwrite_csv(HERE/'POST_INJURY_HALF_EXPOSURE.csv',halves)
    (HERE/'EXPOSURE_QUADRATURE_NOTE.md').write_text('Exposure times are native endpoint quadratures. Each recorded native duration is clipped to overlap the requested interval before weighting its endpoint gap indicator. This prevents whole-step assignment from exceeding a partial interval. It does not reconstruct continuous gap crossings. The earlier simple endpoint sums were refined only in this new analysis directory; no scientific record changed. Run this helper after assemble_comparisons.py when reproducing the report.\n',encoding='utf-8')
    print('Exposure quadratures clipped to interval bounds; no physical evolution.')
if __name__=='__main__':main()
