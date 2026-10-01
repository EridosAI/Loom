"""A5 measurements from immutable saved records. No research-module imports."""
import csv
from a5_analysis_core import *


def contact(event,j):return any(c.get('collider')==f'source-{j}' for c in event['contacts'])


def support_segments(d,j):
    """Never bridge a recorded release or positive-duration noncontact gap."""
    spans=[];active=False
    for i,e in enumerate(d.events):
        if e.get('event_kind')=='release' and f'source-{j}' in e.get('colliders',[]):active=False
        if e['duration']<=0:continue
        if not contact(e,j):active=False;continue
        start=e['time']-e['duration']
        if active and abs(spans[-1]['end']-start)<=TOL:
            spans[-1].update(end=e['time'],last_event=i)
            spans[-1]['duration']+=e['duration']
        else:spans.append(dict(start=start,end=e['time'],duration=e['duration'],first_event=i,last_event=i))
        active=True
    return spans


class Totals:
    def __init__(self,events):
        self.events=events
        self.R=[[0.]*8];self.D=[[0.]*8];self.C=[0.];self.damage=[0.];self.repair=[0.]
        for e in events:
            self.R.append([self.R[-1][j]+e['renewal_first'][j]+e['renewal_second'][j] for j in range(8)])
            self.D.append([self.D[-1][j]+e['transfer'][j] for j in range(8)])
            self.C.append(self.C[-1]+e['expenditure']);self.damage.append(self.damage[-1]+e['damage']);self.repair.append(self.repair[-1]+e['repair'])
    def interval(self,a,b):
        # Half-open event-index slice [a,b); exact event operands, no interpolation.
        return dict(first_event=a,event_stop_exclusive=b,
                    renewal=[math.fsum(e['renewal_first'][j]+e['renewal_second'][j] for e in self.events[a:b]) for j in range(8)],
                    transfer=[math.fsum(e['transfer'][j] for e in self.events[a:b]) for j in range(8)],
                    expenditure=math.fsum(e['expenditure'] for e in self.events[a:b]),
                    damage=math.fsum(e['damage'] for e in self.events[a:b]),repair=math.fsum(e['repair'] for e in self.events[a:b]))


def fixed_windows(d,totals):
    out=[];previous=0
    for first in range(0,len(d.native),20):
        block=d.native[first:first+20];before=d.sample(first-1);after=d.sample(first+len(block)-1)
        end=bisect.bisect_right(d.event_times,after['time']+TOL)
        summary=totals.interval(previous,end)
        support=[math.fsum(e['duration'] for e in d.events[previous:end] if contact(e,j)) for j in range(8)]
        out.append(dict(first_native=first+1,last_native=first+len(block),start_time=before['time'],end_time=after['time'],
                        complete_twenty_native_steps=len(block)==20,EI_before=before['reserves'],EI_after=after['reserves'],
                        stocks_before=before['stocks'],stocks_after=after['stocks'],source_contact_seconds=support,**summary))
        previous=end
    return out


def observations(d,ledger):
    ev=d.events;totals=Totals(ev);alltot=totals.interval(0,len(ev));endtime=d.final['time']
    initialEI=[d.initial['body']['energy'],d.initial['body']['integrity']];finalEI=[d.final['body']['energy'],d.final['body']['integrity']]
    S0=d.initial['stocks'];Sf=d.final['stocks'];cost=alltot['expenditure']
    total_intake=math.fsum(alltot['transfer'])
    energy_residual=(finalEI[0]-initialEI[0])-(total_intake-cost)
    integrity_residual=(finalEI[1]-initialEI[1])-(alltot['repair']-alltot['damage'])
    stock_residuals=[Sf[j]-S0[j]-alltot['renewal'][j]+alltot['transfer'][j] for j in range(8)]
    error_budget=math.fsum(abs(r['energy_residual'])+sum(abs(v) for v in r['stock_residuals']) for r in ledger['rows'])+(len(ev)+1)*1e-12
    origins=[]
    for j in range(8):
        debit=alltot['transfer'][j];renewal=alltot['renewal'][j]
        origins.append(dict(source=j,initial_stock=S0[j],final_stock=Sf[j],renewal=renewal,debit=debit,
                            initial_origin_interval=[max(0.,debit-renewal),min(debit,S0[j])],
                            renewed_origin_interval=[max(0.,debit-S0[j]),min(debit,renewal)],
                            initial_first_bookkeeping=min(debit,S0[j]),renewed_lower_bound=max(0.,debit-S0[j]),
                            stock_ledger_residual=stock_residuals[j]))
    source_details=[];macroreturns=[];allgaps=[]
    for j in range(8):
        spans=support_segments(d,j);src=d.initial['c']['source_positions'][j]
        surface=lambda pos: math.dist(pos,src)-d.initial['c']['body_radius']-d.initial['c']['source_radius']
        contacts=[(i,e) for i,e in enumerate(ev) if contact(e,j)]
        releases=[compact_event(i,e) for i,e in enumerate(ev) if e.get('event_kind')=='release' and f'source-{j}' in e.get('colliders',[])]
        gaps=[]
        for a,b in zip(spans,spans[1:]):
            lo=bisect.bisect_right(d.times,a['end']+TOL);hi=bisect.bisect_left(d.times,b['start']-TOL)
            clear=next((n for n in d.native[lo:hi] if surface(n['position'])>=1.),None)
            row=dict(source=j,departure_contact_endpoint=a['end'],revisit_contact_start=b['start'],away_seconds=b['start']-a['end'],
                     departure_event=a['last_event'],revisit_first_support_event=b['first_event'],
                     first_one_body_diameter_clearance_native=clear,
                     preceding_clearance_sample=d.sample(clear['native_index']-2) if clear else None,
                     macro_departure_observed=clear is not None,
                     maximum_sampled_away_surface_clearance=max((surface(n['position']) for n in d.native[lo:hi]),default=None))
            gaps.append(row);allgaps.append(row)
            if clear is not None:
                away=totals.interval(a['last_event']+1,b['first_event'])
                sd=ev[a['last_event']]['stock_after'][j];sa=ev[b['first_event']]['stock_before'][j]
                renewal=away['renewal'][j];debit=away['transfer'][j]
                interruptions=[compact_event(i,ev[i]) for i in range(a['last_event']+1,b['first_event']) if contact(ev[i],j) and a['end']+TOL<ev[i]['time']<b['start']-TOL]
                row.update(stock_at_departure=sd,stock_before_revisit=sa,away_renewal=renewal,away_source_debit=debit,
                           zero_away_debit_verified=debit==0.,away_stock_residual=sa-sd-renewal+debit,
                           intervening_contact_events=interruptions,uninterrupted_contact_gap_verified=not interruptions,
                           away_all_source_totals=away,departure_native_bracket=d.bracket(a['end']),revisit_native_bracket=d.bracket(b['start']))
                macroreturns.append(row)
        force=[c.get('force',0.) for _,e in contacts if e['duration']>0 for c in e['contacts'] if c['collider']==f'source-{j}']
        impulses=[compact_event(i,e) for i,e in contacts if e['impact']]
        source_details.append(dict(source=j,centre=src,first_contact=compact_event(*contacts[0]) if contacts else None,
                              minimum_native_surface_gap=min([surface(d.initial['body']['position'])]+[surface(n['position']) for n in d.native]),
                              contact_event_count=len(contacts),positive_duration_support_seconds=math.fsum(s['duration'] for s in spans),
                              support_segments=spans,all_gaps=gaps,release_events=releases,impacts=impulses,
                              sustained_force_range=[min(force),max(force)] if force else None,origin_accounting=origins[j]))
    # Use recorded physical endpoints at declared native stage indices. They are
    # not silently rounded to nominal time for event membership.
    stage_ends=[int(Fraction(str(s['until']))*100) for s in d.manifest['execution']['procedure']['stages']]
    stage_rows=[];stage_event_ranges=[];starti=0;event_start=0
    for k,(until,spec) in enumerate(zip(stage_ends,d.manifest['execution']['procedure']['stages'])):
        ni=min(until,len(d.native))
        if starti>=len(d.native):break
        before=d.sample(starti-1);after=d.sample(ni-1)
        event_end=bisect.bisect_right(d.event_times,after['time']+TOL)
        agg=totals.interval(event_start,event_end)
        actions=[a for a in d.controller if a['stage']['index']==k]
        path=math.fsum(math.dist(d.sample(i-1)['position'],d.sample(i)['position']) for i in range(starti,ni))
        stage_rows.append(dict(stage=k,nominal_start=0 if k==0 else d.manifest['execution']['procedure']['stages'][k-1]['until'],
                              nominal_end=spec['until'],actual_start=before['time'],actual_end=after['time'],target=spec['point'],press_force=spec['press_force'],
                              start_native=starti,end_native=ni,complete=ni==until,initial_EI=before['reserves'],final_EI=after['reserves'],
                              stocks_before=before['stocks'],stocks_after=after['stocks'],sampled_path_length=path,
                              decisions=len(actions),first_decision=actions[0] if actions else None,last_decision=actions[-1] if actions else None,**agg))
        stage_event_ranges.append((event_start,event_end));starti=until;event_start=event_end
    visits=[]
    for ordinal,(k,j) in enumerate(((0,0),(2,1),(4,0),(6,1)),1):
        if k>=len(stage_rows):
            visits.append(dict(visit=ordinal,stage=k,source=j,observed=False,reason='Stage not reached before stop'));continue
        st=stage_rows[k];a,b=stage_event_ranges[k]
        touches=[(i,ev[i]) for i in range(a,b) if contact(ev[i],j)]
        positive=[(i,e) for i,e in touches if e['duration']>0]
        firsttransfer=next(((i,ev[i]) for i in range(a,b) if ev[i]['transfer'][j]>error_budget),None)
        row=dict(visit=ordinal,stage=k,source=j,observed=True,complete_stage=st['complete'],start=st['actual_start'],end=st['actual_end'],
                 first_contact=compact_event(*touches[0]) if touches else None,first_support=compact_event(*positive[0]) if positive else None,
                 first_resolved_transfer=compact_event(*firsttransfer) if firsttransfer else None,
                 source_stock_start=st['stocks_before'][j],source_stock_end=st['stocks_after'][j],
                 transfer=st['transfer'][j],renewal=st['renewal'][j],expenditure=st['expenditure'],
                 support_seconds=math.fsum(e['duration'] for _,e in positive),initial_EI=st['initial_EI'],final_EI=st['final_EI'],
                 one_body_diameter_macro_return=None)
        if ordinal>2:
            ret=next((r for r in macroreturns if r['source']==j and st['actual_start']-TOL<=r['revisit_contact_start']<=st['actual_end']+TOL),None)
            if ret:
                agg=totals.interval(ret['revisit_first_support_event'],b)
                transfer=agg['transfer'][j];rv=agg['renewal'][j];sd=ret['stock_at_departure'];ra=ret['away_renewal']
                lower=max(0.,transfer-sd-rv);upper=min(transfer,ra)
                row['one_body_diameter_macro_return']=dict(ret,revisit_transfer=transfer,revisit_renewal=rv,
                    away_restored_uptake_interval=[lower,upper],post_departure_renewal_uptake_lower=max(0.,transfer-sd),
                    away_restored_lower_fraction_of_revisit_intake=lower/transfer if transfer else None,
                    away_restored_lower_fraction_of_whole_cost=lower/cost if cost else None,
                    away_restored_lower_basal_equivalent_seconds=lower/.0015,
                    away_availability_resolved=ra>error_budget,productive_revisit_resolved=transfer>error_budget,
                    forced_away_renewed_uptake_resolved=lower>error_budget)
        visits.append(row)
    macro_departures=[]
    for k,j in ((1,0),(3,1),(5,0)):
        if k>=len(stage_rows):macro_departures.append(dict(stage=k,source=j,observed=False,reason='Departure stage not reached'));continue
        st=stage_rows[k];next_target=stage_ends[k+1] if k+1<len(stage_ends) else stage_ends[-1]
        until=d.sample(min(len(d.native),next_target)-1)['time']
        src=d.initial['c']['source_positions'][j]
        clear=next((n for n in d.native[st['start_native']:min(len(d.native),next_target)] if math.dist(n['position'],src)-1.>=1.),None)
        release_limit=clear['time'] if clear else until
        releases=[compact_event(i,e) for i,e in enumerate(ev) if st['actual_start']-TOL<=e['time']<=release_limit+TOL and e.get('event_kind')=='release' and f'source-{j}' in e.get('colliders',[])]
        rel=releases[-1] if releases else None
        macro_departures.append(dict(stage=k,source=j,nominal_time=st['nominal_start'],actual_stage_time=st['actual_start'],
            release=rel,first_one_body_diameter_clearance=clear,preceding_native=d.sample(clear['native_index']-2) if clear else None,
            all_release_events_before_clearance=releases,
            observed=bool(rel and clear)))
    allreturn=[v['one_body_diameter_macro_return'] for v in visits if v.get('one_body_diameter_macro_return')]
    witnessed=bool(len(allreturn)==2 and all(0<r['stock_at_departure']<d.initial['c']['source_capacity'] and r['uninterrupted_contact_gap_verified'] and r['zero_away_debit_verified'] and r['away_availability_resolved'] and r['productive_revisit_resolved'] for r in allreturn)
                   and d.receipt['status']=='administrative_cutoff' and d.final['native_index']==63000 and min(finalEI)>0)
    motions=[d.initial['body']['position']]+[n['position'] for n in d.native]
    minimumEI=[min([initialEI[k]]+[n['reserves'][k] for n in d.native]) for k in (0,1)]
    mover=[]
    for a in d.controller:
        f=next(x for x in a['inputs']['geometry'] if x['id']=='mover');p=a['inputs']['position'];x0,x1,y0,y1=f['rect']
        dx=max(x0-p[0],p[0]-x1,0);dy=max(y0-p[1],p[1]-y1,0)
        gap=math.hypot(dx,dy)-.5 if dx or dy else -min(p[0]-x0,x1-p[0],p[1]-y0,y1-p[1])-.5
        mover.append(dict(native_index=a['native_index'],time=a['time'],rectangle=f['rect'],velocity=f['velocity'],body_position=p,surface_gap=gap))
    totals_origin=dict(initial_interval=[math.fsum(r['initial_origin_interval'][k] for r in origins) for k in (0,1)],
                       renewed_interval=[math.fsum(r['renewed_origin_interval'][k] for r in origins) for k in (0,1)])
    summary=dict(authority_sha256=AUTH,observed_simulated_time=endtime,native_steps=len(d.native),
                 planned_simulated_ceiling=630,initial_EI=initialEI,final_EI=finalEI,minimum_native_EI=minimumEI,
                 source_transfers=alltot['transfer'],all_source_intake=total_intake,expenditure=cost,damage=alltot['damage'],repair=alltot['repair'],
                 source_renewal=alltot['renewal'],initial_stocks=S0,final_stocks=Sf,sampled_native_path_length=math.fsum(math.dist(a,b) for a,b in zip(motions,motions[1:])),
                 origin_attribution_totals=totals_origin,renewed_lower_fraction_of_cost=totals_origin['renewed_interval'][0]/cost if cost else None,
                 renewed_lower_basal_equivalent_seconds=totals_origin['renewed_interval'][0]/.0015,
                 recorded_balance_using_upper_initial_origin_only=initialEI[0]+totals_origin['initial_interval'][1]-cost,
                 renewed_supply_lower_bound_to_cover_recorded_expenditure=max(0.,cost-initialEI[0]-totals_origin['initial_interval'][1]),
                 necessity_scope='These are arithmetic bounds for the recorded expenditure and source debits, not a simulated no-renewal survival counterfactual.',
                 whole_energy_residual=energy_residual,whole_integrity_residual=integrity_residual,whole_stock_residuals=stock_residuals,
                 residual_aware_positivity_allowance=error_budget,stop_label=d.receipt['status'],stop_cause=d.receipt.get('stop_cause'),
                 complete_receipt=d.receipt['complete'],terminal_dimension=d.final['terminal_dimension'],failure=d.result['failure'],
                 complete_bounded_productive_recurrence_witness=witnessed,
                 observed_macro_returns=len(macroreturns),planned_revisits_obtained=len(allreturn),
                 interpretation='Bounded external physical witness only; no P learning/perception, indefinite support, ecological impossibility or survival counterfactual follows. Full outcome predicates remain in the approved interpretation contract.')
    return dict(summary=summary,stages=stage_rows,visits=visits,macro_departures=macro_departures,all_source_details=source_details,
                all_macro_returns=macroreturns,mover=dict(actual_controller_samples=mover,
                    minimum_sampled_gap=min((r['surface_gap'] for r in mover),default=None),
                    contact_events=[compact_event(i,e) for i,e in enumerate(ev) if any(c['collider']=='mover' for c in e['contacts'])]),
                all_impacts=[compact_event(i,e) for i,e in enumerate(ev) if e['impact'] and e['contacts']],
                all_release_events=[compact_event(i,e) for i,e in enumerate(ev) if e.get('event_kind')=='release'],
                all_repair_events=[compact_event(i,e) for i,e in enumerate(ev) if e['repair']>0.],
                limitations=['Exact continuous path length is not reconstructed; native increments are reported.',
                             'Contact interruptions remain in every original event and all support-segment gaps.',
                             'Origin intervals are bounds without molecule labels, not a new mixing law.',
                             'Event membership uses actual saved physical endpoints at native stage indices, not rounded nominal times.',
                             'Any early resource/terminal/failure stop leaves later windows unobserved; no continuation is authorized.']),fixed_windows(d,totals)


def save_plot_data(d,output):
    with (output/'ALL_NATIVE_PHYSICAL_RECORDS.csv').open('x',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['native_index','time','x','y','angle','E','I']+[f'stock_{j}' for j in range(8)]+['command_left','command_right'])
        b=d.initial['body'];w.writerow([0,0,*b['position'],b['angle'],b['energy'],b['integrity'],*d.initial['stocks'],*b['command']])
        for n in d.native:w.writerow([n['native_index'],n['time'],*n['position'],n['angle'],*n['reserves'],*n['stocks'],*n['commands']])
