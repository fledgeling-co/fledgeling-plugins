#!/usr/bin/env python3
"""F25-059: grant structural actuation in an exported production copy; require the real gate to fail."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
plugin = root / 'plugins/test-campaign'
evidence = plugin / 'docs/evidence/swift-bodies'
source = plugin / 'skills/test-campaign/scripts/campaign.py'
original = source.read_text()
old = 'if state_of(c.get("status", "open")) == "pass" and c.get("oracle") in EFFECT_RUNGS:\n            actuated[sid]'
new = 'if state_of(c.get("status", "open")) == "pass":\n            actuated[sid]'
assert original.count(old) == 1
archive = subprocess.run(['git', 'archive', '65119b6', 'plugins/test-campaign'],
                         cwd=root, capture_output=True, check=True).stdout
with tempfile.TemporaryDirectory(prefix='control-credit-mutant-') as directory:
    subprocess.run(['tar', '-xf', '-', '-C', directory], input=archive, check=True)
    copy = Path(directory) / 'plugins/test-campaign'
    for relative in ['tests/run.sh', 'tests/test_swift_bodies.py',
                     'skills/test-campaign/scripts/vacuity-check.py']:
        (copy / relative).write_bytes((plugin / relative).read_bytes())
    (copy / 'skills/test-campaign/scripts/campaign.py').write_text(original.replace(old, new))
    run = subprocess.run(['bash', str(copy / 'tests/run.sh')], capture_output=True, text=True, timeout=180)
output = run.stdout + run.stderr
(evidence / 'child059-structural-mutant.log').write_text('\n'.join(line.rstrip() for line in output.splitlines()) + '\n')
observed = run.returncode == 1 and 'FAIL  a below-outcome case does not actuate anything: exit 0, wanted 1' in output
receipt = {'exitCode': run.returncode, 'namedFailureObserved': observed,
           'productionSourceSHA256': hashlib.sha256(source.read_bytes()).hexdigest(),
           'mutatedSourceSHA256': hashlib.sha256(original.replace(old, new).encode()).hexdigest(),
           'productionSourceUnchanged': source.read_text() == original,
           'substitution': {'before': old, 'after': new}}
(evidence / 'child059-structural-mutant.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
if not observed: raise SystemExit('Named negative control did not reject structural actuation credit')
