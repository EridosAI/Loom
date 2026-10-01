"""The exact authorized 600-second world-only preparation; no organism is created."""
import argparse
import ast
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from .schema import Config,Streams
from .chemistry import FieldSolver
from .records import strict_bytes,code_identity,view

def field_law(c):
    names=('native_dt','world_side','source_radius','source_positions','repair_rectangles','source_capacity','mover_centre','mover_amplitude','mover_period','mover_size','grid_n','medium_diffusion','solid_diffusion','chemical_decay','prehistory_seconds','field_rtol','arithmetic_tol')
    values=asdict(c)
    return {k:values[k] for k in names}

def prepare(c,directory,life=0):
    root=Path(directory); root.mkdir(parents=True,exist_ok=False)
    rng=Streams(c.master_seed,life); phase=float(rng.draw('world-phase',(1,))[0]*2*np.pi)
    solver=FieldSolver(c); fields=np.zeros((2,c.grid_n,c.grid_n)); stocks=np.full(len(c.source_positions),c.source_capacity)
    steps=round(c.prehistory_seconds/c.native_dt)
    if steps!=60000 or c.prehistory_seconds!=600 or c.native_dt!=.01: raise ValueError('This preparation is the exact reviewed 600-second field history')
    manifest=dict(schema_version=1,status='incomplete',organism_created=False,life=life,master_seed=c.master_seed,phase=phase,law=field_law(c),code=code_identity(),steps_required=steps,steps_completed=0,start_time=-600.,end_time=0.,initial_fields='zero',source_stocks='full_constant',boundary='no_flux',body='absent')
    (root/'manifest.json').write_bytes(strict_bytes(manifest)); start=time.perf_counter(); max_residual=0.; max_mass_error=0.; max_iterations=0
    try:
        for i in range(steps):
            ending=-c.prehistory_seconds+(i+1)*c.native_dt
            fields=solver.step(fields,stocks,ending,phase,c.native_dt)
            max_residual=max(max_residual,float(solver.last['relative_residual'].max())); max_mass_error=max(max_mass_error,float(np.abs(solver.last['mass_balance']).max())); max_iterations=max(max_iterations,solver.last['iterations'])
            if i==99:
                elapsed=time.perf_counter()-start
                print(json.dumps({'steps':100,'wall_seconds':elapsed,'estimated_full_wall_seconds':elapsed*600}),flush=True)
                if elapsed*600>900: raise RuntimeError('Projected prehistory cost exceeds 15 minutes; report before proceeding')
            if (i+1)%10000==0:
                print(json.dumps({'steps':i+1,'world_time':ending,'wall_seconds':time.perf_counter()-start}),flush=True)
                manifest['steps_completed']=i+1; (root/'manifest.json').write_bytes(strict_bytes(manifest))
        np.savez_compressed(root/'fields.npz',fields=fields)
        file_bytes=(root/'fields.npz').read_bytes()
        manifest.update(status='complete',steps_completed=steps,wall_seconds=time.perf_counter()-start,max_relative_residual=max_residual,max_mass_balance_error=max_mass_error,max_iterations=max_iterations,field_sha256=hashlib.sha256(fields.tobytes()).hexdigest(),file_sha256=hashlib.sha256(file_bytes).hexdigest(),file_bytes=len(file_bytes),rng_counters=rng.counters,field_min=float(fields.min()),field_max=float(fields.max()))
    except Exception as error:
        manifest.update(status='failure',error=f'{type(error).__name__}: {error}',steps_completed=i,wall_seconds=time.perf_counter()-start)
        (root/'manifest.json').write_bytes(strict_bytes(view(manifest)))
        raise
    (root/'manifest.json').write_bytes(strict_bytes(view(manifest)))
    return manifest

def load(c,directory,life=0):
    root=Path(directory); m=json.loads((root/'manifest.json').read_text())
    rng=Streams(c.master_seed,life); phase=float(rng.draw('world-phase',(1,))[0]*2*np.pi)
    if m['status']!='complete' or m['steps_completed']!=60000 or m['law']!=field_law(c) or m['phase']!=phase: raise ValueError('Unmatched or incomplete chemical prehistory')
    current=code_identity()['files']
    changed=[name for name in ('chemistry.py','geometry.py','schema.py') if m['code']['files'][name]!=current[name]]
    if changed:
        # Original bytes are immutable provenance, not executable fallback code.
        # An optical-only change must not cause another 600-second preparation.
        baseline=root/'law-source-at-preparation'
        relevant={'geometry.py':('circle_rect_area','disk_areas','rectangle_areas','mover'),
                  'schema.py':('Streams',)}
        for name in ('chemistry.py','geometry.py','schema.py'):
            original=(baseline/name).read_bytes()
            if hashlib.sha256(original).hexdigest()!=m['code']['files'][name]:
                raise ValueError(f'Unverified original prehistory source: {name}')
            present=(Path(__file__).parent/name).read_bytes()
            if name=='chemistry.py':
                if original!=present: raise ValueError('Prehistory field solver changed')
            else:
                def dependencies(source):
                    tree=ast.parse(source)
                    nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or getattr(n,'name',None) in relevant[name]]
                    return ast.dump(ast.Module(body=nodes,type_ignores=[]),include_attributes=False)
                if dependencies(original)!=dependencies(present):
                    raise ValueError(f'Prehistory geometry or random-stream dependency changed: {name}')
        m=dict(m,reuse_verification=dict(original_modules_sha256={n:m['code']['files'][n] for n in ('chemistry.py','geometry.py','schema.py')},current_modules_sha256={n:current[n] for n in ('chemistry.py','geometry.py','schema.py')},method='Original module bytes verified; chemistry byte identical; geometry area/mover and Streams AST/imports identical; field-law parameters, source state and phase matched. Optical-domain change only; no prehistory rerun.'))
    blob=(root/'fields.npz').read_bytes()
    if hashlib.sha256(blob).hexdigest()!=m['file_sha256']: raise ValueError('Prehistory archive checksum mismatch')
    with np.load(root/'fields.npz',allow_pickle=False) as data: fields=data['fields'].copy()
    if hashlib.sha256(fields.tobytes()).hexdigest()!=m['field_sha256']: raise ValueError('Prehistory array checksum mismatch')
    return fields,phase,rng,m

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('directory'); args=parser.parse_args()
    print(json.dumps(prepare(Config(),args.directory),default=str),flush=True)
