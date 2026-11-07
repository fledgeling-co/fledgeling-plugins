#!/usr/bin/env python3
"""Tally one panel round from the lanes' answer files.

    tally.py <round-dir> [--json]

Reads every <lane>.md in the directory, takes the first "VERDICT: <letter>" and
"CONFIDENCE: <level>" lines from each, and reads the model id from <lane>.log ("model=").
A lane with no verdict line, or an answer file under 300 bytes, is a failure and casts no vote.

Then it applies the panel's rule, so the call is the same on every run:
  unanimous among valid lanes          -> decided
  top option has at least 3/4 of them  -> decided_split (record the dissent)
  anything else                        -> round_two (2-2, 2-1-1, or fewer than 3 valid lanes)
Exit code 0 when the round settles the decision, 3 when it needs round two, 1 when fewer than
two lanes answered at all.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path


def read_lane(md):
    text = md.read_text(errors='replace')
    log = md.with_suffix('.log')
    model = None
    if log.exists():
        found = re.findall(r'^model=(.+)$', log.read_text(errors='replace'), re.M)
        model = found[-1].strip() if found else None
    # The first VERDICT line wins wherever it sits in the line: grok has been seen to
    # print a sentence of preamble with no newline before it ("...stacks.VERDICT: B"),
    # and anchoring to the line start counted a valid answer as a failed lane.
    verdict = re.search(r'VERDICT:\**\s*\**\s*([A-Z])\b', text)
    conf = re.search(r'CONFIDENCE:\**\s*\**\s*(high|medium|low)\b', text, re.I)
    ok = verdict is not None and len(text.encode()) >= 300
    return {'lane': md.stem, 'model': model, 'valid': ok,
            'verdict': verdict.group(1).upper() if verdict else None,
            'confidence': conf.group(1).lower() if conf else None,
            'bytes': len(text.encode())}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    lanes = [read_lane(p) for p in sorted(Path(argv[1]).glob('*.md'))
             if not p.name.startswith(('brief', 'superseded'))]
    valid = [l for l in lanes if l['valid']]
    counts = Counter(l['verdict'] for l in valid)
    if len(valid) < 2:
        outcome, code = 'too_few_lanes', 1
    else:
        top, n = counts.most_common(1)[0]
        if n == len(valid):
            outcome, code = 'decided', 0
        elif n * 4 >= len(valid) * 3 and len(valid) >= 3:
            outcome, code = 'decided_split', 0
        else:
            outcome, code = 'round_two', 3
    result = {'lanes': lanes, 'counts': dict(counts), 'valid_lanes': len(valid), 'outcome': outcome}
    if '--json' in argv:
        print(json.dumps(result, indent=2))
    else:
        for l in lanes:
            state = f"VERDICT {l['verdict']} ({l['confidence'] or 'no confidence'})" if l['valid'] else 'FAILED, casts no vote'
            print(f"{l['lane']:<8} {l['model'] or 'model unknown':<24} {state}")
        print('counts:', ', '.join(f'{k}={v}' for k, v in counts.most_common()) or 'none')
        print('outcome:', outcome)
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv))
