#!/usr/bin/env python3
"""Exercise the actual repository catalogue gate with one wrong-version row, then restore it."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
evidence = root / 'plugins/test-campaign/docs/evidence/swift-bodies'
marketplace = root / '.claude-plugin/marketplace.json'
original = marketplace.read_bytes()
text = original.decode()
start = text.index('"name": "generate-investor-portal"')
end = text.index('"source"', start)
row = text[start:end]
assert row.count('"version": "1.3.0"') == 1
mutant = (text[:start] + row.replace('"version": "1.3.0"', '"version": "1.2.0"') + text[end:]).encode()
try:
    marketplace.write_bytes(mutant)
    run = subprocess.run(['node', 'site/scripts/build-catalogue.mjs'], cwd=root,
                         capture_output=True, text=True, timeout=60)
finally:
    marketplace.write_bytes(original)
output = run.stdout + run.stderr
(evidence / 'child060-catalogue-mutant.log').write_text(output.rstrip() + '\n')
observed = run.returncode == 1 and ('generate-investor-portal: version mismatch — plugin.json says 1.3.0, '
                                  'marketplace.json says 1.2.0') in output
receipt = {'exitCode': run.returncode, 'namedFailureObserved': observed,
           'marketplaceSHA256': hashlib.sha256(original).hexdigest(),
           'mutatedSHA256': hashlib.sha256(mutant).hexdigest(),
           'sourceRestored': marketplace.read_bytes() == original,
           'mutation': 'generate-investor-portal marketplace version only:1.3.0 ->1.2.0'}
(evidence / 'child060-catalogue-mutant.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
if not observed or marketplace.read_bytes() != original:
    raise SystemExit('Wrong catalogue version was not rejected or restore failed')
