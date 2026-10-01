"""Seal a portable priority review package; never touches experiment files."""
from common import *
import re,zipfile,shutil,platform
from datetime import datetime,timezone

def main():
    rows=[];scope=[]
    for n in range(1,13):
        life=f'RS-M1-{n:03d}';d=json.loads((OUT/'cache'/(life+'.json')).read_bytes());scope.append({k:d[k] for k in ('life','physical_age','curve_cutoff','last_complete_checkpoint_age','native_rows','waves','curve_waves')})
        for r in d['interventions']:
            rows.append(dict(life=life,time=r['time'],native_index=r['index'],E_before=r['before_reserves'][0],E_after=r['after_reserves'][0],I_before=r['before_reserves'][1],I_after=r['after_reserves'][1],external_E=r['external_support'][0],external_I=r['external_support'][1],zero_learning_from_jump=r['zero_learning_from_jump']))
    table('tables/SUPPORT_EVENTS.csv',rows);table('tables/OBSERVATION_SCOPE.csv',scope)
    (OUT/'reference_sources').mkdir(exist_ok=True)
    for p in [decoder,OLD/'passive_reference_sources/historical_plot_helpers.py',BASE/'loom_p/neural.py',BASE/'configuration.json',PREP/'sandbox_evidence.py',PREP/'RUNTIME_IDENTITY.json']:
        shutil.copyfile(p,OUT/'reference_sources'/p.name)
    requests=[Path(r'C:\Users\Jason\.codex\attachments\5b1a10ab-f8a7-4ced-ab67-61e961af8b02\Pasted text.txt'),Path(r'C:\Users\Jason\.codex\attachments\45601f50-028e-460a-9430-a321fe92c551\Pasted text.txt')]
    for i,p in enumerate(requests):shutil.copyfile(p,OUT/'reference_sources'/('JASON_FULL_ANALYSIS_REQUEST.txt' if i==0 else 'JASON_PRIORITY_CURVES_REQUEST.txt'))
    report=OUT/'H_E_I_DEVELOPMENTAL_CURVES_v0_1.md'
    links=re.findall(r'\]\(([^)]+)\)',report.read_text(encoding='utf8'));missing=[l for l in links if not (OUT/l).exists()];assert not missing
    # Independent residual and coefficient checks use exported model fits.
    models=json.loads((OUT/'CURVE_MODEL_FITS.json').read_bytes());max_resid=0
    for group in models.values():
        for v in group.values():
            error=np.max(abs(np.array(v['observed'])-v['predicted']-v['residual']));max_resid=max(max_resid,float(error))
    assert max_resid==0
    files=[]
    for p in OUT.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(OUT).as_posix()
        if rel.startswith('cache/') or rel.startswith('raw/') and not rel.endswith(('_H_E_I_WAVES.csv.gz','_BODY_NATIVE.csv.gz')):continue
        if p.name in ('CURVE_PACKAGE_MANIFEST.json','CURVE_ARCHIVE_RECORD.json','EARLY_COMPLETE_LIFE_FIT_REVIEW.json','SCHEMA_PROFILE.json','CHUNK_PROFILE.json'):continue
        if rel.startswith('tables/') and rel.endswith('_IMPACTS.csv'):continue
        files.append(p)
    readme='''# H / E / I developmental curves — priority review

Open `CURVE_REVIEW.html` for the saved-figure viewer, or `H_E_I_DEVELOPMENTAL_CURVES_v0_1.md` for the complete report.

NON-CANONICAL RESURRECTION SANDBOX. Passive read-only evidence analysis. No simulation, continuation, checkpoint branch, RNG draw, retry, canon update or parameter change.

The package contains 12 five-panel organism figures, 12 functional figures, three complete-life overlays (each with a separate censored panel), three fit/residual figures, one local-slope figure, chronological compressed CSVs, all descriptive fit/slope tables, source/evidence hashes and independently coded consistency checks. PNG and SVG versions are included.

`raw/*H_E_I_WAVES.csv.gz`: exact measured completed-wave H/E/I norms and derived immediate learned-current effects, q, use and M1. `raw/*BODY_NATIVE.csv.gz`: every recorded native E/I row within the stated curve boundary, plus birth. Standard gzip-compressed CSV, not downsampled. `tables/SUPPORT_EVENTS.csv` records exact intervention boundaries and both reserve values. `tables/OBSERVATION_SCOPE.csv` distinguishes full durable evidence from the conservative RS-M1-008 curve cutoff.

Shapes are descriptive and serially dependent. Fits are not mechanistic forecasts. The raw lines and event catalog preserve steps which robust slopes can suppress. No large-N inference or scalar skill score is made.

Reproducibility code is included. The plain-data extractor requires access to the original sealed execution directory and original custody manifest at the paths in `common.py`; the review itself has no dependency on Python or the simulator. Numerical analysis used Python 3.13.5, NumPy 2.3.3 and SciPy 1.16.2. Static rendering used the bundled Python/Pillow/ReportLab runtime; no dependencies were installed. Reference source copies are included for inspection, not execution.

The original 4.65 GB experiment archive is preserved separately and is not duplicated here. `EXECUTION_EVIDENCE_HASHES.json` identifies every original execution file. This is the priority curve deliverable; it does not purport to complete the broader developmental analysis request.
'''
    (OUT/'README_CURVES.md').write_text(readme,encoding='utf8');files.append(OUT/'README_CURVES.md')
    manifest=dict(label=LABEL,scope='PRIORITY H/E/I CURVES',utc=datetime.now(timezone.utc).isoformat(),files=[dict(path=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(set(files))],checks=dict(report_links_resolve=len(links),model_residual_arithmetic_exact=True,simulations=0,continuations=0,alternate_histories=0),analysis_runtime=dict(python=platform.python_version(),numpy=np.__version__))
    save('CURVE_PACKAGE_MANIFEST.json',manifest)
    archive=ROOT/'H_E_I_DEVELOPMENTAL_CURVES_v0_1_REVIEW.zip'
    assert not archive.exists(),'Do not overwrite an already sealed review archive'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(set(files+[OUT/'CURVE_PACKAGE_MANIFEST.json'])):z.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for item in manifest['files']:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
    save('CURVE_ARCHIVE_RECORD.json',dict(path=str(archive),bytes=archive.stat().st_size,sha256=sha(archive),members=len(manifest['files'])+1,all_members_verified=True))
    print(json.dumps(json.loads((OUT/'CURVE_ARCHIVE_RECORD.json').read_bytes())))
if __name__=='__main__':main()
