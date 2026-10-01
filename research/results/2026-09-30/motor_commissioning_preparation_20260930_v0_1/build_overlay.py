"""Preparation-time source assembly only; never advances an organism/world."""
from pathlib import Path
import difflib
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology/loom_developmental'
DEST=HERE/'loom_motor_commissioning'
def replace(text, old, new):
    assert text.count(old)==1, old
    return text.replace(old,new)
codec=(BASE/'codec.py').read_text()
codec=replace(codec,'from loom_p.records import registry', '''from loom_p.records import registry as original_registry
def registry():
    from .motor import Motor
    return dict(original_registry(), Motor=Motor)''')
codec=replace(codec,"elif type(x).__name__ in registry() and type(x) is registry()[type(x).__name__]:", "elif type(x).__name__ in registry() and type(x) in (registry()[type(x).__name__], original_registry().get(type(x).__name__)):")
runner=(BASE/'runner.py').read_text()
runner=replace(runner, 'from . import codec,core,evidence', 'from . import codec, evidence\nfrom loom_developmental import core')
start=runner.index('def identity():');end=runner.index('\ndef create_engineering_grant',start)
runner=runner[:start]+'''def identity():
    from loom_developmental.runner import identity as baseline_identity
    result=baseline_identity()
    root=Path(__file__).parent
    result['motor_commissioning_overlay']={f.name:file_hash(f) for f in sorted(root.glob('*.py'))}
    result['claim']='frozen P core/world with explicitly identified experimental spontaneous motor overlay'
    return result
''' + runner[end:]
start=runner.index('def create_engineering_grant');end=runner.index('\ndef atomic_json',start)
runner=runner[:start]+'''def validate_grant(g,e,parent):
    keys={'schema','kind','life_id','initial_causal_sha256','initial_index','end_index',
        'parent_receipt_sha256','request_path','request_sha256','wall_limit_seconds','storage_limit_bytes',
        'checkpoint_stride','chunk_steps','compression_level','process','parameters_sha256'}
    if set(g)!=keys or g['schema']!=1 or g['kind']!='motor-temporal-commissioning':
        raise ValueError('explicit motor commissioning grant required')
    if parent is not None or g['parent_receipt_sha256'] is not None:
        raise ValueError('no continuation')
    if e.c.identity()!=CONFIG or e.status not in ('paused','ready'):
        raise ValueError('configuration/status mismatch')
    if e.native_index!=0 or e.time!=0 or e.organism.native_count!=0 or e.organism.wave_count!=0:
        raise ValueError('original blank birth required')
    if g['initial_index']!=0 or g['end_index']!=9000 or type(g['end_index']) is not int:
        raise ValueError('fixed ninety-second scope')
    if g['initial_causal_sha256']!=codec.digest(core.causal_state(e)):
        raise ValueError('initial state mismatch')
    from .motor import PARAMETERS
    if g['parameters_sha256']!=hashlib.sha256(canonical(PARAMETERS)).hexdigest():
        raise ValueError('process parameters changed')
    m=e.organism.motor
    process=getattr(m,'commissioning',{}).get('process','CURRENT')
    if process not in ('CURRENT','M1','M2') or g['process']!=process:
        raise ValueError('process mismatch')
    if g['life_id'] not in [f'MC-FS-{i:03d}-{process}' for i in (1,2,3)]:
        raise ValueError('case not in fixed matrix')
    if e.organism.rng.life!=int(g['life_id'][6:9]):
        raise ValueError('original life stream mismatch')
    limits=(g['wall_limit_seconds'],g['storage_limit_bytes'],g['checkpoint_stride'],g['chunk_steps'],g['compression_level'])
    if limits!=(300,32000000,6000,100,1):
        raise ValueError('fixed resource/recording envelope')
    request=json.loads(Path(g['request_path']).read_bytes())
    if file_hash(g['request_path'])!=g['request_sha256']:
        raise ValueError('approval checksum mismatch')
    bound={k:v for k,v in g.items() if k not in ('request_path','request_sha256')}
    if set(request)!={'notice','approved_scope'} or request['approved_scope']!=bound or not request['notice']:
        raise ValueError('exact separate approval required')
''' + runner[end:]
old="if self.binding['apparatus']!={p.name:file_hash(p) for p in sorted(root.glob('*.py'))} or code_identity()!=self.binding['P']:"
new="if self.binding['motor_commissioning_overlay']!={p.name:file_hash(p) for p in sorted(root.glob('*.py'))} or self.binding['apparatus']!={p.name:file_hash(p) for p in sorted((Path(__import__('loom_developmental').__file__).parent).glob('*.py'))} or code_identity()!=self.binding['P']:"
runner=replace(runner,old,new)
start=runner.index('    @classmethod\n    def continue_life')
runner=runner[:start]+'''    @classmethod
    def continue_life(cls,*args,**kwargs):
        raise ValueError('No continuation/retry in motor commissioning')
'''
verify=(BASE/'verify.py').read_text().replace('from . import codec,core,evidence','from . import codec, evidence\nfrom loom_developmental import core')
for name,data in [('codec.py',codec),('runner.py',runner),('verify.py',verify)]:
    (DEST/name).write_text(data,encoding='utf8',newline='\n')
    original=(BASE/name).read_text().splitlines(True)
    (HERE/(name+'.diff')).write_text(''.join(difflib.unified_diff(original,data.splitlines(True),fromfile='frozen/'+name,tofile='overlay/'+name)),encoding='utf8')
