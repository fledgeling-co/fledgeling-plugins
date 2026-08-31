#!/usr/bin/env python3
"""Exercise a next-declaration mutant of the actual scanner, without changing its source."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

plugin = Path(__file__).resolve().parents[1]
source = plugin / 'skills/test-campaign/scripts/vacuity-check.py'
evidence = plugin / 'docs/evidence/swift-bodies'
original = source.read_bytes()
old = 'body = swift["blocks"][i]["body"] if swift is not None else src[pos:end]'
new = 'body = src[pos:end]'
text = original.decode()
assert text.count(old) == 1
mutant = text.replace(old, new).encode()
with tempfile.TemporaryDirectory(prefix='swift-boundary-mutant-') as directory:
    copy = Path(directory)
    (copy / 'skills/test-campaign/scripts').mkdir(parents=True)
    (copy / 'tests').mkdir()
    (copy / 'skills/test-campaign/scripts/vacuity-check.py').write_bytes(mutant)
    test = copy / 'tests/test_swift_bodies.py'
    test.write_bytes((plugin / 'tests/test_swift_bodies.py').read_bytes())
    run = subprocess.run(['python3', str(test)], capture_output=True, text=True, timeout=30)
output = run.stdout + run.stderr
(evidence / 'boundary-mutant.log').write_text('\n'.join(line.rstrip() for line in output.splitlines()) + '\n')
observed = run.returncode == 1 and 'FAIL: test_reader_after_nested_declaration_stays_in_its_parent' in output
receipt = {'exitCode': run.returncode, 'namedFailureObserved': observed,
           'sourceSHA256': hashlib.sha256(original).hexdigest(),
           'mutatedSourceSHA256': hashlib.sha256(mutant).hexdigest(),
           'sourceUnchanged': source.read_bytes() == original,
           'substitution': {'before': old, 'after': new}}
(evidence / 'boundary-mutant.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
if not observed or source.read_bytes() != original:
    raise SystemExit('The actual boundary mutant did not trip its named falsifier')
