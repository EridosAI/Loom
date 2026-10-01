"""Read-only portable custody check. Standard-library Python; no simulation.

Usage: python VERIFY_ARCHIVE.py <results.zip>
"""
import hashlib
import json
import sys
import zipfile

def main():
    with zipfile.ZipFile(sys.argv[1]) as z:
        m=json.loads(z.read('EVIDENCE_ARCHIVE_MANIFEST.json'))
        expected={r['path'] for r in m['files']}|{'EVIDENCE_ARCHIVE_MANIFEST.json'}
        assert len(z.namelist())==len(expected) and set(z.namelist())==expected
        for r in m['files']:
            data=z.read(r['path'])
            assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],r['path']
        print(json.dumps(dict(status='PASS',members=len(m['files']),denominator=m['denominator'],
                             checkpoint=m['checkpoint'],simulation_executed=False)))

if __name__=='__main__':main()
