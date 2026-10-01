"""Prepare the already-reviewed single-case launch wrapper for the new exact grant."""
from pathlib import Path
R=Path(__file__).resolve().parent.parent
source=(R/'b1_compact_layout_20260927/prepare_authorized_launch_20260929.py').read_text(encoding='utf-8')
def once(a,b):
    global source
    assert source.count(a)==1
    source=source.replace(a,b)
once('One authorized compact FULL-RAW preparation.','One authorized coordinate-colour FULL-RAW preparation.')
once("PC=ROOT/'b1_pc_execution_20260926';PREVIOUS=ROOT/'b1_execution_20260927'", "PC=ROOT/'b1_pc_execution_20260926';PREVIOUS=ROOT/'b1_execution_20260929_restart_01'")
once("PACK=ROOT/'exports/2026-09-27-B1-compact-1060a17e'", "PACK=ROOT/'exports/2026-09-29-B1-colour-labels-b684912e'")
once("W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'", "W=ROOT/'worktrees/loom-p-b1-coordinate-colours-20260929'")
once("OUT=ROOT/'b1_execution_20260929'", "OUT=ROOT/'b1_execution_20260929_colours_01'")
once("AUTH='45f2349183579ed478e4c5582cdb70ba6619e06769ccfaad05f2dd36d26b173d'", "AUTH='936cd43b20c84378c3d7a2e99825fb87029c873872db6e504279ee7a931ce901'")
once("APP='1060a17e3dd14c6361f6f15c95bb58fad3110ffc'", "APP='b684912eaf7811cd318ee94c77172aca790f3a0d'")
start=source.index("    previous=read(PREVIOUS/'STATE.json')")
end=source.index("    assert read(PC/'SEQUENCE_STATE.json')",start)
source=source[:start]+'''    previous=read(PREVIOUS/'STATE.json')
    assert previous['status']=='ENDED AT 1.2 SECONDS / COMPLETE PREFIX PRESERVED FOR COLOUR-LABEL CORRECTION' and previous['live_services']==0
    closure=read(PREVIOUS/'PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json')
    assert closure['native_steps']==120 and closure['human_commands']==12 and closure['observed_lifecycle']=='ended'
    assert sha(PREVIOUS/'private/runs/B1-FULL-RAW/manifest.json')==closure['run_manifest_sha256']
    assert read(PREVIOUS/'ENDED_SERVICE_STOP_RECEIPT.json')['ended_service_stopped'] is True
    for n,v in read(PREVIOUS/'private/CLOSED_PREFIX_FILE_MANIFEST.json')['files'].items():
        assert sha(PREVIOUS/'private'/n)==v['sha256']
    for older in ('b1_execution_20260927','b1_execution_20260929'):
        assert read(ROOT/older/'STATE.json')['live_services']==0
    assert read(ROOT/'b1_coordinate_colours_20260929/FINAL_AUDIT.json')['no_new_execution'] is True
'''+source[end:]
once("roots=[PACK,PC,PREVIOUS,", "roots=[PACK,PC,PREVIOUS,ROOT/'b1_execution_20260927',ROOT/'b1_execution_20260929',ROOT/'b1_coordinate_colours_20260929',ROOT/'exports/2026-09-27-B1-compact-1060a17e',ROOT/'exports/2026-09-29-B1-coordinate-colours-b684912e',ROOT/'exports/2026-09-29-B1-coordinate-colours-b684912e.zip',")
start=source.index('    notice=')
end=source.index("    request=PRIVATE/",start)
source=source[:start]+'''    notice=('Jason replied "Authorised." on 2026-09-29 to the explicit question authorizing one fresh 30-second B1-FULL-RAW attempt under canonical authority '+AUTH+'. '
      'This authorizes exactly one fresh case at coordinate-colour apparatus '+APP+', with the same complete physical start and unchanged limits. '
      'Two earlier zero-step attempts and a 1.2-second / 120-step / 12-command attempt are closed and preserved. The existing nonzero prefix is not resumed. '
      'Prior permitted starting-reading and movement-history exposure is bound in this object; no first-naive or wholly unseen-start claim is permitted. '
      'Jason chooses every command. No assistant driving, plan view, privileged hint, retry, continuation, extension, tuning, substitution or code change. '
      'B1-CHEMISTRY-HIDDEN is not authorized. No evaluator feedback before both paired trials end or the pair is explicitly abandoned.')
'''+source[end:]
once("user_authorization_verbatim='Yes, authorised.',", "user_authorization_verbatim='Authorised.',")
source=source.replace('attempt=2,','attempt=4,')
once("prior_attempt='Preserved zero-step closure on 2026-09-27; earlier grant not reused.',", "prior_attempt='Two zero-step attempts and the complete 1.2-second / 120-step / 12-command prefix preserved. New exact authority grant; no continuation or unseen-start claim.',")
prepared=R/'b1_coordinate_colours_20260929/prepare_authorized_launch.py'
with prepared.open('x',encoding='utf-8',newline='\n') as f:f.write(source)
print('Prepared a single FULL-RAW launch wrapper; no grant, world or service created by this wrapper-generation step.')
