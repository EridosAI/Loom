"""One-way operator projection. Never receives an Engine or changes raw history."""
import copy
from pathlib import Path
from .contract import digest, require
from .controllers import LABELS, validate_sensor_payload, validate_history

KEPT=tuple(i for i in range(29) if i not in (10,11,12,13))
HIDDEN_LABELS=[LABELS[i] for i in KEPT]

def display_identity(kind='none'):
    require(kind in ('none','chemistry_hidden'),'unsupported display intervention')
    if kind=='none':return {'kind':'none'}
    return {'kind':'chemistry_hidden','raw_flat_indices':[10,11,12,13],
            'representation':'omitted','implementation_sha256':digest(Path(__file__).read_bytes())}

def validate_intervention(value):
    require(isinstance(value,dict) and value.get('kind') in ('none','chemistry_hidden'),
            'unsupported display intervention')
    require(value==display_identity(value['kind']),'display implementation identity mismatch')

def validate_operator_payload(payload,intervention):
    validate_intervention(intervention)
    if intervention['kind']=='none':return validate_sensor_payload(payload)
    return validate_history(payload,HIDDEN_LABELS,2)

def project(payload,intervention):
    """Copy permitted values; chemistry is absent, never zeroed or summarized."""
    validate_intervention(intervention);validate_sensor_payload(payload)
    result=copy.deepcopy(payload)
    if intervention['kind']=='chemistry_hidden':
        result['schema']=2;result['raw_labels']=HIDDEN_LABELS.copy()
        for row in result['history']:row['raw']=[row['raw'][i] for i in KEPT]
    validate_operator_payload(result,intervention)
    return result

def infer_display(payload):
    """Saved operator files contain either a complete full or omitted schema."""
    kind='none' if payload.get('schema')==1 else 'chemistry_hidden'
    value=display_identity(kind);validate_operator_payload(payload,value);return value
