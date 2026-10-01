"""Package existing passive-analysis artifacts only; never launches a model."""
from common import *
import ast,platform,re,shutil,zipfile,datetime
import scipy
def main():
    archive=ROOT/'FUNCTIONAL_BEHAVIOURAL_DEVELOPMENT_v0_1_REVIEW.zip'
    if archive.exists():raise FileExistsError('Preserve existing package: '+str(archive))
    files_to_copy=[PRIOR/'common.py',OLD/'passive_reference_sources/audit_exploration.py',OLD/'passive_reference_sources/historical_plot_helpers.py',PRIOR/'INPUT_PROVENANCE.json',PRIOR/'SOURCE_IDENTITY_VERIFICATION.json',PRIOR/'EXTRACTION_VERIFICATION.json',PRIOR/'CURVE_CONSISTENCY_REVIEW.json']
    reference=[];(OUT/'reference_sources').mkdir(exist_ok=True)
    for src in files_to_copy:
        dest=OUT/'reference_sources'/src.name;shutil.copyfile(src,dest);assert sha(src)==sha(dest);reference.append(dict(original=str(src),copy=str(dest.relative_to(OUT)),sha256=sha(dest)))
    prior_archive=ROOT/'H_E_I_DEVELOPMENTAL_CURVES_v0_1_REVIEW.zip';h=sha(prior_archive);assert h=='d8ff930fa2edf81a17a7df3f00755c3ffe628f4aac5acbd7c835b7a95dbdc613'
    life=[]
    for n in range(1,13):
        name=f'RS-M1-{n:03d}';f=np.load(OUT/'series'/(name+'_FUNCTIONAL.npz'));o=np.load(OUT/'cache'/(name+'_OBSERVER.npz'));life.append(dict(life=name,last_completed_wave=float(f['age'][-1]),curve_cutoff=record(name)['curve_cutoff'],physical_prefix_end=float(o['time'][-1]),wave_rows=len(f['age'])))
        for k in f.files:
            assert not np.any(np.isinf(f[k])),(name,k)
            if not k.startswith(('command_per_theta','q_per_H','use_per_H')):assert np.isfinite(f[k]).all(),(name,k)
    broken=[]
    for src in OUT.glob('*.md'):
        text=src.read_text(encoding='utf8');assert not any(ord(c)<32 and c not in '\n\r\t' for c in text),src.name
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
            if not target.startswith(('http:','https:','#')) and not (OUT/target.split('#')[0]).exists():broken.append((src.name,target))
    assert not broken,broken
    for src in OUT.glob('*.py'):ast.parse(src.read_text(encoding='utf-8-sig'))
    assert len(list((OUT/'figures').glob('*.png')))==29 and len(list((OUT/'figures').glob('*.svg')))==29
    assert len(readcsv('tables/AGE_BAND_STATUS_ANNOTATIONS.csv'))==35
    main_report=(OUT/'FUNCTIONAL_EXPRESSION_OVER_TIME_v0_1.md').read_text(encoding='utf8');assert main_report.rfind('## WHAT WOULD REQUIRE A CAUSAL BRANCH')>main_report.rfind('## ALTERNATIVE EXPLANATIONS')
    save('DELIVERY_VERIFICATION.json',dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,executable=sys.executable,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__,figures=29,figure_formats=['PNG','SVG'],age_band_rows=35,scope=life,reference_sources=reference,prior_curve_archive_unchanged_sha256=h,broken_report_links=broken,production_git_status='clean porcelain; nonfatal global ignore access warnings; command-local safe.directory only',visual_review=['001 functional','006 coupling','008 functional censoring','010 coupling zero-norm case','pooled behavioural dashboard'],world_steps=0,RNG_draws=0,canonical_changes=0,new_authorities=0))
    readme='''# Functional / behavioural development review v0.1

NON-CANONICAL M1 RESURRECTION SANDBOX. Passive analysis only.

Open **REVIEW.html** directly for all 29 figures. Read **FUNCTIONAL_EXPRESSION_OVER_TIME_v0_1.md** for findings and **BEHAVIOURAL_DEVELOPMENT_WATCHLIST_v0_1.md** for the standing observer checklist. **DATA_DICTIONARY.md** locates the exact numerical evidence and methods.

E-current command influence rises over the final 1000 seconds in five of seven complete lives; E/M1 ratio rises in four. I/q/H-use trends are mixed. Productive source interactions rise in the middle periods, but late damage also rises and environmental intake does not progressively replace support. Selected collision-context matches are heavily confounded by event selection and changing opportunity. No acquired competence is established.

All twelve available histories are retained: seven complete, one host-censored, four pilots. The review contains full derived wave series, paired deltas, age/event/context tables and passive observer summaries. It is portable for review; reproducing from raw requires the separately preserved evidence and prior extracted caches described in DATA_DICTIONARY.md. No raw experiment archive is overwritten or duplicated here.

All 37,909 execution files and original evidence/source identities passed custody checks. Zero new world steps, RNG draws, alternate trajectories, parameter/canonical edits or launch authorities. Stop for Jason review.
'''
    (OUT/'README.md').write_text(readme,encoding='utf8')
    files=[q for q in OUT.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name!='PACKAGE_MANIFEST.json']
    manifest=[dict(path=q.relative_to(OUT).as_posix(),bytes=q.stat().st_size,sha256=sha(q)) for q in sorted(files)];save('PACKAGE_MANIFEST.json',dict(schema='loom-passive-review-package-v1',files=manifest,manifest_self_excluded=True,world_steps=0))
    files.append(OUT/'PACKAGE_MANIFEST.json')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for q in sorted(files):z.write(q,OUT.name+'/'+q.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for r in manifest:
            content=z.read(OUT.name+'/'+r['path']);assert len(content)==r['bytes'] and hashlib.sha256(content).hexdigest()==r['sha256']
        count=len(z.namelist());assert count==len(files)
    archive_record=dict(archive=str(archive),bytes=archive.stat().st_size,sha256=sha(archive),members=count,all_member_hashes_verified=True,manifest_sha256=sha(OUT/'PACKAGE_MANIFEST.json'),world_steps=0)
    (ROOT/'FUNCTIONAL_BEHAVIOURAL_DEVELOPMENT_v0_1_ARCHIVE_RECORD.json').write_text(json.dumps(archive_record,indent=2)+'\n',encoding='utf8');print(json.dumps(archive_record,indent=2))
if __name__=='__main__':main()
