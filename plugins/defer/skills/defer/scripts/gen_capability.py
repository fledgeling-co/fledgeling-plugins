#!/usr/bin/env python3
"""Regenerate defer's capability_matrix.json from the diolog-swe-bench store.

Run from ~/Dev/diolog-swe-bench after `pnpm db:import`:

    pnpm --filter @diolog/swe-bench-harness capability:export > /tmp/matrix.json
    python3 gen_capability.py /tmp/matrix.json

The exporter emits per-task scores straight out of `computeLeaderboard`, so the
rolling sample window, contract staleness and identity folding all apply exactly
as they do to `pnpm leaderboard`. This script joins measured cost, grades every
lane against opus per work shape, and writes defer's capability_matrix.json.
"""
import json, statistics, random, sqlite3, os, sys
random.seed(23)
MATRIX = sys.argv[1] if len(sys.argv) > 1 else '/tmp/lbx/matrix2.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
    '~/Dev/fledgeling-plugins/plugins/defer/skills/defer/scripts/capability_matrix.json')
d = json.load(open(MATRIX)); rows = d['rows']
meta = {m['key']: m for m in d['modelMeta']}
DB = os.path.expanduser('~/Library/Application Support/Benchwarmer/benchwarmer.sqlite')
con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
cost = {}
for prov, mod, eff, c, tok, dur in con.execute(
        "SELECT provider,model,effort,AVG(costUSD),AVG(totalTokens),AVG(durationMs) "
        "FROM runs WHERE status IN ('passed','failed') GROUP BY provider,model,effort"):
    cost[f"{prov}/{mod}@{eff}"] = (c, tok, dur)
ALT = {'gemini-3.7-flash@medium': 'mini/vercel_ai_gateway/google/gemini-3.7-flash@medium',
       'gemini-3.7-flash@high': 'mini/vercel_ai_gateway/google/gemini-3.7-flash@high',
       'grok-4.5@xhigh': 'zero/x-ai/grok-4.5@xhigh', 'glm-5.2-fast@max': 'mini/zai/glm-5.2-fast@max'}
costof = lambda k: cost.get(k) or cost.get(ALT.get(k, ''), (None, None, None))
LANES = ['claude/claude-opus-5@xhigh', 'claude/fable@high', 'claude/claude-sonnet-5@xhigh',
         'codex/gpt-5.6-sol@max', 'codex/gpt-5.6-sol@xhigh', 'codex/gpt-5.6-sol@high', 'codex/gpt-5.6-sol@medium',
         'codex/gpt-5.6-terra@max', 'codex/gpt-5.6-terra@xhigh', 'codex/gpt-5.6-terra@high', 'codex/gpt-5.6-terra@medium',
         'codex/gpt-5.6-luna@max', 'codex/gpt-5.6-luna@high',
         'gemini-3.7-flash@medium', 'gemini-3.7-flash@high', 'grok-4.5@xhigh', 'glm-5.2-fast@max', 'claude/haiku@high']
REF = 'claude/claude-opus-5@xhigh'
def tier(k):
    m = meta.get(k, {})
    if m.get('eligible'): return 'A'
    if m.get('coverage', 0) >= 0.99 and m.get('sampleCoverage', 0) >= 0.6: return 'B'
    if m.get('coverage', 0) >= 0.9: return 'C'
    return 'D'
SHAPES = {
 'brownfield-integration': ('Change existing multi-file service code under compound acceptance',
   'backend tasks vendored from the real dAIolog repo, or carrying two or more independent verifier groups',
   lambda r: r['dim'] == 'backend' and ('real-repo' in r['tags'] or r['groups'] >= 2)),
 'greenfield-module': ('New self-contained module behind one acceptance surface',
   'backend tasks with no vendored repo slice and a single verifier group',
   lambda r: r['dim'] == 'backend' and 'real-repo' not in r['tags'] and r['groups'] < 2),
 'api-surface': ('BFF route handler, server action or adapter wiring', 'the frontend dimension',
   lambda r: r['dim'] == 'frontend'),
 'react-ui': ('React plus Vite component with interaction behaviour', 'ui tasks whose render type is command',
   lambda r: r['render'] == 'command'),
 'static-page': ('From-scratch HTML and CSS page with no framework', 'ui tasks whose render type is static-html',
   lambda r: r['render'] == 'static-html'),
 'deck': ('Slide and presentation authoring', 'ui tasks whose render type is slides, scored on the deck rubric',
   lambda r: r['render'] == 'slides'),
 'visual-design': ('Work graded on aesthetic and design judgement', 'ui tasks tagged design',
   lambda r: 'design' in r['tags']),
 'accessibility': ('Semantics, keyboard paths and ARIA', 'tasks tagged accessibility',
   lambda r: 'accessibility' in r['tags']),
 'algorithmic': ('Complexity-constrained or optimality-constrained implementation',
   'the optimality dimension: functional gate then reference-anchored judge', lambda r: r['dim'] == 'optimality'),
 'tool-orchestration': ('Multi-step tool calling against an audited log', 'the tool-use dimension',
   lambda r: r['dim'] == 'tool-use'),
 'regression-sensitive': ('Must not break an existing passing contract',
   'tasks declaring scoring.regression_command, a pass-to-pass guard', lambda r: r['regression']),
}
def pboot(dl, B=8000):
    if len(dl) < 3: return None
    obs = statistics.mean(dl); c = 0
    for _ in range(B):
        if abs(statistics.mean([x if random.random() < 0.5 else -x for x in dl])) >= abs(obs): c += 1
    return (c + 1) / (B + 1)
def gate(k, delta, p, n, cf):
    if k == REF: return 'REF'
    if n < 6 or cf < 0.7: return 'THIN'
    sig = p is not None and p < 0.05 and delta < 0
    if delta > 0.05 and not sig: g = 'GOLD'
    elif delta >= -0.05 and not sig: g = 'GREEN'
    elif delta < -0.15 or (sig and delta < -0.10): g = 'RED'
    else: g = 'AMBER'
    if tier(k) in ('C', 'D') and g in ('GOLD', 'GREEN'): g = 'AMBER'
    return g
out = {'schema': 1,
 'source': {'bench': 'diolog-2.0', 'repo': '~/Dev/diolog-swe-bench', 'store': 'benchwarmer.sqlite',
   'visible_tasks': d['n'], 'measured': '2026-08-22', 'reference_lane': REF,
   'scoring_spec': 'docs/SCORING.md - rolling newest-two clean decisions per model and task; stale, error, unscored and integrity-noise rows excluded',
   'significance': 'paired sign-flip bootstrap over the per-task delta, 8000 resamples, seed 23',
   'usd_per_task': 'mean costUSD over that key decided runs at list token rates - a proxy for plan burn, not a subscription invoice',
   'regenerate': 'python3 gen_capability.py (see references/capability.md)'},
 'gates': {'GOLD': 'beats opus by more than 5 points',
   'GREEN': 'within 5 points of opus with no significant deficit',
   'AMBER': 'within 15 points, or a GREEN held back by provisional evidence',
   'RED': 'more than 15 points behind, or a significant deficit worse than 10 points',
   'THIN': 'fewer than 6 comparable tasks, or the lane covered under 70 percent of the shape',
   'REF': 'the reference lane itself'},
 'evidence_tiers': {'A': 'ranked: 100 percent task coverage and a full two-sample window on every task',
   'B': '100 percent task coverage, 60 to 99 percent of tasks at a full window',
   'C': '90 to 99 percent task coverage', 'D': 'under 90 percent task coverage - a hint, never a gate'},
 'lanes': {}, 'shapes': {}}
for k in LANES:
    m = meta.get(k, {}); c, tok, dur = costof(k)
    out['lanes'][k] = {'tier': tier(k), 'ranked': bool(m.get('eligible')), 'rank': m.get('rank'),
        'headline': round(m['headline'], 4) if m.get('headline') is not None else None,
        'plain': round(m['plain'], 4) if m.get('plain') is not None else None,
        'task_coverage': round(m.get('coverage', 0), 3), 'sample_coverage': round(m.get('sampleCoverage', 0), 3),
        'usd_per_task': round(c, 4) if c else None, 'mean_tokens': int(tok) if tok else None,
        'mean_minutes': round(dur / 60000, 1) if dur else None,
        'harness': 'mini-swe-agent in an Apple container' if k in ALT else 'the vendor CLI on the host'}
for s, (desc, seg, f) in SHAPES.items():
    rs = [r for r in rows if f(r)]
    ent = {'description': desc, 'measured_on': seg, 'n': len(rs),
           'opus_mean': round(statistics.mean([r['scores'][REF] for r in rs]), 4), 'lanes': {}}
    for k in LANES:
        pr = [(r['scores'][k], r['scores'][REF]) for r in rs if r['scores'].get(k) is not None]
        cf = len(pr) / len(rs) if rs else 0
        if len(pr) < 3:
            ent['lanes'][k] = {'gate': 'THIN', 'n': len(pr)}; continue
        dl = [a - b for a, b in pr]; p = pboot(dl); delta = statistics.mean(dl)
        ent['lanes'][k] = {'mean': round(statistics.mean([a for a, _ in pr]), 4), 'delta': round(delta, 4),
            'p': round(p, 4), 'n': len(pr), 'coverage': round(cf, 3),
            'wins': sum(1 for x in dl if x > 1e-9), 'losses': sum(1 for x in dl if x < -1e-9),
            'gate': gate(k, delta, p, len(pr), cf)}
    out['shapes'][s] = ent
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w') as fh:
    json.dump(out, fh, indent=1); fh.write('\n')
print('wrote', OUT, os.path.getsize(OUT), 'bytes')
