"""Build a new data-only A3 report reader from preserved generic A2 checks."""
import hashlib,pathlib,shutil
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
old=ROOT/'a2_execution_staging_20260925/a2_analysis_core.py'
t=old.read_text(encoding='utf-8').split('\ndef contact_intervals(d,j):')[0]
t=t.replace('A2','A3').replace('229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007','43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd')
t=t.replace("sys.path.insert(0,str(PACKET/'references'))","sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))")
t=t.replace("abs(d.final['time']-180)","abs(d.final['time']-m['hard_stop_time'])").replace("d.final['time']<180-1e-9","d.final['time']<m['hard_stop_time']-1e-9")
t=t.replace("a['case_deadline']==180","a['case_deadline']==d.manifest['hard_stop_time']")
t=t.replace("'contacts':e['contacts'],'colliders':e.get('colliders')}","'contacts':e['contacts'],'colliders':e.get('colliders'),'damage':e['damage'],'repair':e['repair'],'repair_quality':e.get('repair_quality')}")
a=t.index('    def interval(self,a,b):');b=t.index('\ndef record_integrity',a)
t=t[:a]+'''    def interval(self,a,b):
        if b<a-TOL:raise ValueError('Reversed event interval')
        chosen=[(i,e) for i,e in enumerate(self.events) if e['duration']>0 and e['time']>a+TOL and e['time']<=b+TOL]
        straddles=[i for i,e in enumerate(self.events) if e['duration']>0 and any(e['time']-e['duration']<cut-TOL and e['time']>cut+TOL for cut in (a,b))]
        impacts=[(i,e) for i,e in enumerate(self.events) if e['duration']==0 and e['time']>a+TOL and e['time']<=b+TOL]
        return {'start':a,'end':b,'duration':max(0.,b-a),'whole_duration_events_included':len(chosen),
           'source_transfers':[math.fsum(e['transfer'][j] for _,e in chosen) for j in range(8)],
           'gross_intake':math.fsum(math.fsum(e['transfer']) for _,e in chosen),'expenditure':math.fsum(e['expenditure'] for _,e in chosen),
           'repair':math.fsum(e['repair'] for _,e in chosen),'duration_damage':math.fsum(e['damage'] for _,e in chosen),
           'impact_damage_excluding_start_including_end':math.fsum(e['damage'] for _,e in impacts),
           'boundary_straddling_events':straddles,'complete_event_boundary_coverage':not straddles,
           'timing_rule':'Symmetric 1e-10 boundary membership; costs/transfer are whole event sums, never proportional interpolation; impacts at the start excluded, endpoint included.'}
''' +t[b:]
# Failures after an issued decision may legitimately leave one command with no delivered native step.
# The inherited positive data checks remain strict; if unsupported failure records occur, report their limitation.
with (S/'a3_analysis_core.py').open('x',encoding='utf-8') as f:f.write(t)
for n in ('evidence.py','v3_checker_v1_1.py'):
    src=ROOT/'exports/2026-09-25-A1-read-only-reanalysis-viewer-v1'/n
    shutil.copyfile(src,S/n)
compile(t,str(S/'a3_analysis_core.py'),'exec')
print('A3 generic record/ledger reader prepared; no trajectory loaded or command computed.')
