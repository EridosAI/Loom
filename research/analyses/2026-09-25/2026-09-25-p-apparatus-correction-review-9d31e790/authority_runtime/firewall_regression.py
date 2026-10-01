"""Pure-function regression: SO never becomes configuration grounds."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
from loom_commissioning import contract

parser=argparse.ArgumentParser()
parser.add_argument('--fault',action='store_true')
args=parser.parse_args()
so=contract.classify('S2',{'survival':'useful','credit':'beneficial'})
av=contract.classify('V1',{'identity':'known mismatch'})
co=contract.classify('D5',{'receiver_effect':0.001})
original=contract.configuration_grounds
if args.fault:
    # Remove only the SO rejection; preserve the same row/class validation.
    def corrupted(evidence):
        contract.require(all(x['class']==contract.CLASSES.get(x['row']) for x in evidence),'evidence class mismatch')
        return {'automatic_adjustment':False,'requires':'Jason defect-specific ruling','evidence':evidence}
    contract.configuration_grounds=corrupted
try:
    contract.configuration_grounds([av,so])
except ValueError as error:
    assert 'SO cannot' in str(error)
else:
    raise AssertionError('SO FIREWALL BREACH: scientific outcome accepted as configuration grounds')
fake=dict(so,class_='AV'); fake['class']='AV'; fake.pop('class_')
try: contract.configuration_grounds([fake])
except ValueError as error: assert 'class mismatch' in str(error)
else: raise AssertionError('mislabelled scientific outcome accepted')
request=contract.configuration_grounds([av,co])
assert request['automatic_adjustment'] is False and request['requires']=='Jason defect-specific ruling'
print(json.dumps({'SO_rejected':True,'dishonest_SO_relabel_rejected':True,'AV_CO_request_only':request},indent=2))
