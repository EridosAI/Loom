"""Privileged offline evaluation, never imported by the sensor-only server."""
import json
from pathlib import Path
import numpy as np
from loom_p.records import strict_bytes, view
from .contract import classify, ROSTER
from .validators import read_stream, verify_segment

def evaluate(directory):
    root=Path(directory); validation=verify_segment(root)
    native=read_stream(root/'native.jsonl.gz'); events=read_stream(root/'events.jsonl.gz')
    diagnostic=read_stream(root/'diagnostics.jsonl.gz')
    receipt=json.loads((root/'manifest.json').read_bytes())
    tolerance=1e-12
    first={name:None for name in ('source_contact','transfer','damage','repair_contact','eligible_damaged_repair','positive_restoration','mover_contact')}
    contacts=[]
    for e in events:
        evidence={'time':e['time'],'energy':e['energy_after'],'integrity':e['integrity_after']}
        flags={'source_contact':any('source' in c for c in e['contacts']),
               'transfer':sum(e['transfer'])>tolerance,'damage':e['damage']>tolerance,
               'repair_contact':any(c['material']==3 for c in e['contacts']),
               'eligible_damaged_repair':e['integrity_before']<1 and e.get('repair_quality',0)>0,
               'positive_restoration':e['repair']>tolerance,
               'mover_contact':any(c['collider']=='mover' for c in e['contacts'])}
        for key,flag in flags.items():
            if flag and first[key] is None: first[key]=dict(evidence)
        if e['contacts']: contacts.append({'time':e['time'],'duration':e['duration'],'contacts':e['contacts']})
    # Keep operands and uncertainty; no tiny-positive-as-useful or biological gate.
    ledgers=[{'time':e['time'],'duration':e['duration'],'transfer':sum(e['transfer']),
              'cost':e['expenditure'],'repair':e['repair'],'damage':e['damage'],
              'energy_before':e['energy_before'],'energy_after':e['energy_after'],
              'stock_before':e['stock_before'],'stock_after':e['stock_after'],
              'renewal':(np.asarray(e['renewal_first'])+e['renewal_second']).tolist(),
              'sign_resolution_floor':tolerance} for e in events]
    return {'scope':'privileged evaluator only; manufactured apparatus evidence, no commissioning witness',
        'AV':[classify('V1',validation)],'CO':[classify('C1',{'first_observed_in_this_segment':first,
            'denominator':'one manufactured segment, not a birth roster','contacts':contacts})],
        'SO_preserved':read_stream(root/'scientific_observations.jsonl.gz'),
        'SO_status':'preserved; cannot ground configuration adjustment before freeze',
        'roster':ROSTER,'case_status':'manufactured fixture only',
        'lawful_births_executed':0,'births':{str(i):'unstarted' for i in (1,2,3,4)},
        'native':native,'physical_ledgers':ledgers,'diagnostics':diagnostic,
        'identity':receipt['contract'],'stop_reason':receipt['status']}

def write_review(directory,output):
    result=evaluate(directory); root=Path(output); root.mkdir(exist_ok=False)
    data=strict_bytes(view(result)); (root/'evaluation.json').write_bytes(data)
    # No live API and no sensor-controller route to these privileged records.
    template='''<!doctype html><meta charset="utf-8"><title>Loom apparatus · privileged review</title>
<style>body{font:16px system-ui;background:#f5f4ef;color:#183a3c;max-width:1100px;margin:35px auto;padding:20px}section{background:white;padding:18px;margin:15px 0;border:1px solid #ccd9d4;border-radius:10px}canvas{width:100%;height:150px}pre{overflow:auto;max-height:400px;font-size:12px}label{margin-right:20px}</style>
<h1>Privileged apparatus review</h1><p>Manufactured component fixture. These observations do not establish commissioning, survival or learning.</p>
<section><h2>Record and interpretation</h2><p id="summary"></p><p>AV and CO are the commissioning review surface. Raw SO observations are preserved separately and cannot support a configuration adjustment before freeze.</p></section>
<section><h2>Aligned native history</h2><label>Endpoint <input id="at" type="range" min="0" value="0"></label><span id="clock"></span><p>Step-start input → old receptor mean → residual → new activity. End-of-step transduction has its own timestamp.</p><canvas id="plot" width="1000" height="160"></canvas><pre id="detail"></pre></section>
<section><h2>Physical ledgers and first observations</h2><pre id="ledger"></pre></section>
<section><h2>Separate scientific observations</h2><pre id="so"></pre></section>
<script>const D=__DATA__;const slider=document.querySelector('#at');slider.max=Math.max(0,D.diagnostics.length-1);document.querySelector('#summary').textContent=D.identity.mode+' · '+D.AV[0].observation.native_records+' native records · '+D.stop_reason+' · Births 1–4 remain unstarted.';document.querySelector('#ledger').textContent=JSON.stringify({observations:D.CO,ledgers:D.physical_ledgers},null,2);document.querySelector('#so').textContent=JSON.stringify(D.SO_preserved,null,2);function render(){let d=D.diagnostics[Number(slider.value)];if(!d)return;document.querySelector('#clock').textContent=d.input_time.toFixed(3)+' → '+d.endpoint_time.toFixed(3)+' s';document.querySelector('#detail').textContent=JSON.stringify(d,null,2);let ctx=document.querySelector('#plot').getContext('2d');ctx.clearRect(0,0,1000,160);let rows=D.diagnostics.slice(0,Number(slider.value)+1);[0,1,2,3].forEach((ch,j)=>{ctx.strokeStyle=['#245c58','#b56435','#6656a3','#397eb0'][j];ctx.beginPath();rows.forEach((r,i)=>{let v=r.cortices?r.cortices[ch].activity_new[0]:r.raw_endpoint[ch][0],x=1000*i/Math.max(1,rows.length-1),y=80-65*Math.tanh(v);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke()})}slider.oninput=render;render();</script>'''
    text=template.replace('__DATA__',data.decode('utf-8').replace('<','\\u003c'))
    (root/'PRIVILEGED_REVIEW.html').write_text(text,encoding='utf-8')
    return result
