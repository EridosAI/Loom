"""Load a verified phase-specific history; never prepare one or launch a life."""
from pathlib import Path
from loom_p.schema import Config
from loom_p.prehistory import load
from loom_p.engine import Engine
from .contract import digest, CONFIG, require

def from_verified_cache(directory, birth_id):
    c=Config(); require(c.identity()==CONFIG,'configuration identity mismatch')
    fields,phase,rng,provenance=load(c,directory,life=birth_id)
    engine=Engine(c,fields,phase,rng,provenance)
    receipt=Path(directory)/'manifest.json'
    initialization={'kind':'verified_phase_history','birth_id':birth_id,'phase':phase,
        'field_sha256':digest(fields.tobytes()),'cache_directory':str(Path(directory).resolve()),
        'cache_receipt_sha256':digest(receipt.read_bytes())}
    return engine,initialization

def verify_history(initialization,c,initial_fields,phase):
    directory=Path(initialization['cache_directory'])
    require(digest((directory/'manifest.json').read_bytes())==initialization['cache_receipt_sha256'],
            'field history receipt mismatch')
    fields,actual_phase,_,_=load(c,directory,life=initialization['birth_id'])
    require(actual_phase==phase==initialization['phase'] and digest(fields.tobytes())==initial_fields,
            'wrong field/mover phase')
