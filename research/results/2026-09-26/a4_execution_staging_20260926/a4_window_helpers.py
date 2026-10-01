"""Saved-data windows adapted from preserved A3 helpers; no simulation."""
from a4_analysis_core import *

def touch(e,label):return any(c['collider']==label for c in e['contacts'])
def sign(value,allowance):return 'zero' if value==0 else 'positive_resolved' if value>allowance else 'negative_resolved' if value < -allowance else 'unresolved_at_accounting_resolution'
def allowance(ledger,i,field='integrity_residual'):
    return abs(ledger['rows'][i][field])+2e-12
def contact_intervals(d,label):
    out=[]
    for i,e in enumerate(d.events):
        if e['duration']<=0 or not touch(e,label):continue
        a=e['time']-e['duration'];b=e['time']
        if out and abs(out[-1]['end']-a)<=TOL:
            out[-1]['end']=b;out[-1]['last_event']=i;out[-1]['duration']+=e['duration']
        else:out.append({'start':a,'end':b,'duration':e['duration'],'first_event':i,'last_event':i})
    return out
def fixed_windows(d,ledger):
    out=[];events=d.events;labels=['mover']+[f'wall-{i}' for i in range(4)]+[f'repair-{i}' for i in range(3)]+[f'source-{i}' for i in range(8)]
    intervals={label:contact_intervals(d,label) for label in labels}
    for start in range(0,len(d.native),20):
        block=d.native[start:start+20];old=d.sample(start-1);new=d.sample(start+len(block)-1);a=old['time'];b=new['time']
        ix=list(range(bisect.bisect_right(d.event_times,a+TOL),bisect.bisect_right(d.event_times,b+TOL)))
        inc=[i for i in ix if events[i]['duration']>0]
        straddles=[i for i in inc if events[i]['time']-events[i]['duration']<a-TOL]
        k=bisect.bisect_right(d.event_times,b+TOL)
        if k<len(events) and events[k]['duration']>0 and events[k]['time']-events[k]['duration']<b-TOL:straddles.append(k)
        er=math.fsum(abs(ledger['rows'][i]['energy_residual']) for i in ix);ir=math.fsum(abs(ledger['rows'][i]['integrity_residual']) for i in ix)
        ea=er+(len(ix)+1)*1e-12;ia=ir+(len(ix)+1)*1e-12
        de=new['reserves'][0]-old['reserves'][0];di=new['reserves'][1]-old['reserves'][1]
        support={}
        for label in labels:
            seconds=math.fsum(max(0,min(b,c['end'])-max(a,c['start'])) for c in intervals[label])
            support[label]={'seconds':seconds,'contact_containing':any(touch(events[i],label) for i in inc),'fully_supported':abs(seconds-(b-a))<=TOL}
        out.append({'first_native':block[0]['native_index'],'last_native':block[-1]['native_index'],'start_time':a,'end_time':b,
          'complete_0_2_second_interval':len(block)==20 and abs(b-a-.2)<=TOL,'EI_before':old['reserves'],'EI_after':new['reserves'],
          'energy_delta':de,'net_energy_sign':sign(de,ea),'integrity_delta':di,'net_integrity_sign':sign(di,ia),
          'energy_allowance':ea,'integrity_allowance':ia,'source_transfers':[math.fsum(events[i]['transfer'][j] for i in inc) for j in range(8)],
          'all_source_intake':math.fsum(math.fsum(events[i]['transfer']) for i in inc),'expenditure':math.fsum(events[i]['expenditure'] for i in inc),
          'repair':math.fsum(events[i]['repair'] for i in ix),'damage':math.fsum(events[i]['damage'] for i in ix),
          'positions':[old['position'],new['position']],'stocks':[old['stocks'],new['stocks']],
          'contact_support':support,'boundary_straddling_events':straddles})
    return out
def rect_gap(p,rect,r=.5):
    x,y=p;x0,x1,y0,y1=rect;dx=max(x0-x,x-x1,0);dy=max(y0-y,y-y1,0)
    return math.hypot(dx,dy)-r if dx or dy else -min(x-x0,x1-x,y-y0,y1-y)-r
