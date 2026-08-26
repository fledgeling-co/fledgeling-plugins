#!/usr/bin/env python3
"""Un-blind and tally the panel. Reports non-verdicts as non-verdicts."""
import json, re, glob, os, collections

MAP = json.load(open('/tmp/eli5-evals/unblinding-map.json'))['map']
LANES = {'codex': 'OpenAI (gpt-5.6-sol, codex)',
         'agy': 'Google (gemini-3.7-flash-high, agy)',
         'grok': 'xAI (grok-4.6, via cursor-agent)',
         'fable': 'Claude (fable-5) - SAME FAMILY as builder'}

def verdict(path):
    if not os.path.exists(path): return None, 'not run'
    t = open(path, encoding='utf-8', errors='replace').read().strip()
    if not t: return None, 'empty output'
    m = re.findall(r'^\s*OVERALL:\s*\**\s*(A|B|TIE)\b', t, re.M | re.I)
    if not m:
        return None, 'no OVERALL line (truncated after preamble)' if len(t) < 600 else 'no OVERALL line'
    return m[-1].upper(), 'ok'

rows, tally = [], collections.Counter()
lane_status = collections.defaultdict(collections.Counter)

for ev in sorted(MAP):
    row = {'eval': ev}
    for lane in LANES:
        v, why = verdict(f'/tmp/eli5-evals/verdicts/{ev}.{lane}.md')
        if v is None:
            row[lane] = f'-- ({why})'
            lane_status[lane]['no verdict'] += 1
        else:
            arm = MAP[ev][v] if v in ('A','B') else 'tie'
            row[lane] = arm
            lane_status[lane]['verdict'] += 1
            if lane != 'fable':                      # out-of-family tally only
                tally[arm] += 1
    rows.append(row)

w = max(len(r['eval']) for r in rows) + 2
print(f"{'eval':<{w}}" + "".join(f"{l:<14}" for l in LANES))
print("-" * (w + 14*len(LANES)))
for r in rows:
    print(f"{r['eval']:<{w}}" + "".join(f"{str(r[l])[:13]:<14}" for l in LANES))
print("-" * (w + 14*len(LANES)))
print("\nOut-of-family tally (codex + agy + grok only):")
for k, v in tally.most_common(): print(f"  {k:<12} {v}")
print("\nLane completion:")
for l, c in lane_status.items():
    tot = sum(c.values())
    print(f"  {LANES[l]:<46} {c['verdict']}/{tot} returned a verdict")
