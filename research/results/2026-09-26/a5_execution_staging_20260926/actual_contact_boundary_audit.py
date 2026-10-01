"""Saved-event reconciliation of the packet's final-actual-contact rule.

Preserves the initial support-gap analysis, including its conservative false
flag. Does not import production modules, recompute commands, or evolve a world.
"""
import gzip,hashlib,json,math,pathlib,shutil
from package_result import BASE,REVIEW,guard,js,sha,write


def touches(e,j):
    return any(c['collider']==f'source-{j}' for c in e['contacts'])


def main():
    guard(5_000_000)
    assert not (REVIEW/'ACTUAL_CONTACT_BOUNDARY_AUDIT.json').exists()
    raw=js(REVIEW/'RAW_EVIDENCE_BEFORE_ANALYSIS.json')
    assert all(sha(p)==v for p,v in raw.items())
    with gzip.open(BASE/'trajectory-001/events.jsonl.gz','rt',encoding='utf-8') as f:
        events=[json.loads(line) for line in f]
    o=js(REVIEW/'A5_OBSERVATIONS.json');summary=o['summary'];allowance=summary['residual_aware_positivity_allowance']
    rows=[]
    for visit in o['visits'][2:]:
        old=visit['one_body_diameter_macro_return'];j=visit['source']
        clear=old['first_one_body_diameter_clearance_native'];return_start=old['revisit_contact_start']
        lo=old['departure_event'];hi=old['revisit_first_support_event']
        candidates=[i for i in range(lo,hi) if touches(events[i],j) and events[i]['time']<clear['time']]
        endpoint=max(candidates);last=events[endpoint];departure=last['time']
        release=[i for i in range(endpoint,hi) if events[i].get('event_kind')=='release' and f'source-{j}' in events[i].get('colliders',[]) and events[i]['time']<=clear['time']]
        assert release and abs(events[release[-1]]['time']-departure)<1e-10
        selected=events[endpoint+1:hi]
        interruptions=[i for i in range(endpoint+1,hi) if touches(events[i],j) and departure+1e-10<events[i]['time']<return_start-1e-10]
        straddles=[i for i in range(endpoint+1,hi) if events[i]['duration']>0 and (events[i]['time']-events[i]['duration']<departure-1e-10 or events[i]['time']>return_start+1e-10)]
        sd=last['stock_after'][j];sa=events[hi]['stock_before'][j]
        ra=math.fsum(e['renewal_first'][j]+e['renewal_second'][j] for e in selected)
        debit=math.fsum(e['transfer'][j] for e in selected)
        duration=math.fsum(e['duration'] for e in selected)
        tv=old['revisit_transfer'];rv=old['revisit_renewal'];lower=max(0.,tv-sd-rv);upper=min(tv,ra)
        predicates=dict(actual_release_observed=True,one_body_diameter_clearance_observed=True,
            partially_depleted_at_actual_departure=0<sd<.2,uninterrupted_away_interval=not interruptions,
            no_boundary_straddling_events=not straddles,zero_away_debit=debit==0.,
            stock_identity_verified=abs(sa-sd-ra+debit)<1e-12,
            duration_coverage_verified=abs(duration-(return_start-departure))<1e-9,
            positive_away_renewal=ra>allowance,productive_revisit=tv>allowance,
            positive_revisit_support=visit['support_seconds']>0.,planned_visit_complete=visit['complete_stage'])
        rows.append(dict(source=j,visit=visit['visit'],last_positive_support_endpoint=old['departure_contact_endpoint'],
            final_actual_contact_event_index=endpoint,final_actual_contact_event=last,
            actual_release_event_index=release[-1],actual_release_event=events[release[-1]],
            actual_departure_time=departure,revisit_contact_start=return_start,away_seconds=return_start-departure,
            first_one_body_diameter_clearance_native=clear,preceding_clearance_sample=old['preceding_clearance_sample'],
            all_contacts_after_support_before_clearance=[dict(event_index=i,event=events[i]) for i in candidates if i>lo],
            away_event_slice=[endpoint+1,hi],interior_contact_events=interruptions,boundary_straddling_events=straddles,
            stock_at_departure=sd,stock_before_revisit=sa,away_renewal=ra,away_source_debit=debit,
            away_stock_residual=sa-sd-ra+debit,covered_duration=duration,
            revisit_transfer=tv,revisit_renewal=rv,away_restored_uptake_interval=[lower,upper],
            post_departure_renewal_uptake_lower=max(0.,tv-sd),
            away_restored_lower_fraction_of_revisit_intake=lower/tv,
            away_restored_lower_fraction_of_whole_cost=lower/summary['expenditure'],
            away_restored_lower_basal_equivalent_seconds=lower/.0015,
            forced_away_renewed_uptake_resolved=lower>allowance,predicates=predicates,
            local_bounded_revisit=all(predicates.values())))
    validated=all(js(REVIEW/(name+'.json'))['valid'] for name in ['RECORD_INTEGRITY','BOUNDARY_AND_DELIVERY','ACCOUNTING']) and not js(REVIEW/'ANALYSIS_RESULT.json')['errors']
    complete=summary['native_steps']==63000 and summary['stop_label']=='administrative_cutoff' and summary['terminal_dimension'] is None and min(summary['final_EI'])>0
    witness=validated and complete and len(rows)==2 and all(r['local_bounded_revisit'] for r in rows)
    assert all(sha(p)==v for p,v in raw.items())
    result=dict(method='Apply the predeclared final ACTUAL contact endpoint, including zero-duration impacts; sum the unchanged event ledger after that endpoint. No interpolation, erased contacts, new rule, replay, rerun, or production change.',
        governing_source='Approved OBSERVATION_AND_INTERPRETATION.md: final actual source-contact endpoint before the unattended interval; preserve every recontact.',
        initial_analysis_preserved='A5_OBSERVATIONS.json and A5_RESULT_SUMMARY.json retain a conservative support-gap flag. Source 1 had a later zero-duration departure recontact, so that initial candidate interval was correctly flagged as interrupted. This supplemental measurement uses the final actual contact required by the packet.',
        initial_support_gap_witness_flag=summary['complete_bounded_productive_recurrence_witness'],
        complete_saved_data_validation=validated,completed_nonterminal_observation=complete,
        complete_bounded_productive_recurrence_witness=witness,returns=rows,
        unchanged_raw_files_checked=len(raw),raw_evidence_unchanged=True,new_simulation_steps=0,command_recomputations=0,
        physical_replays=0,production_code_changes=0,original_analysis_outputs_changed=False)
    write(REVIEW/'ACTUAL_CONTACT_BOUNDARY_AUDIT.json',result)
    final=dict(summary)
    final.update(complete_bounded_productive_recurrence_witness=witness,
        interpretation_basis='ACTUAL_CONTACT_BOUNDARY_AUDIT.json, applying the predeclared final actual contact endpoint; initial support-gap analysis retained.',
        initial_support_gap_witness_flag=summary['complete_bounded_productive_recurrence_witness'],
        actual_contact_returns=[{k:v for k,v in r.items() if k not in ['final_actual_contact_event','actual_release_event','first_one_body_diameter_clearance_native','preceding_clearance_sample','all_contacts_after_support_before_clearance']} for r in rows])
    write(REVIEW/'A5_FINAL_RESULT_SUMMARY.json',final)
    shutil.copyfile(pathlib.Path(__file__),REVIEW/pathlib.Path(__file__).name)
    print(json.dumps(dict(final_witness=witness,validation=validated,returns=[{k:r[k] for k in ['source','actual_departure_time','revisit_contact_start','away_seconds','stock_at_departure','stock_before_revisit','away_renewal','away_restored_uptake_interval','predicates']} for r in rows]),indent=2))


if __name__=='__main__':main()
