#!/usr/bin/env python3
"""Build the decision page HTML from a JSON spec.

Usage:
  build_decision.py spec.json out.html     # validate, then write the page
  build_decision.py --check spec.json      # validate only, exit 1 on any problem
  build_decision.py --example              # print a minimal valid spec

The page leads with the decision, then why, then what happens next, then the options with how
each model voted, the dissent, and the evidence. The spec is validated before anything is
written, because a page that names a winning option nobody voted for, counts a failed lane as a
vote, or hides an action that needs the owner's confirmation cannot be corrected after the
owner has acted on it.
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = (HERE.parent / 'assets' / 'decision.css').read_text()
STATUSES = {
    'decided': ('c-ok', 'Decided'),
    'decided_split': ('c-warn', 'Decided, with dissent'),
    'needs_you': ('c-info', 'Needs your answer'),
}
VERDICTS = {'chose': 'c-ok', 'differed': 'c-warn', 'failed': 'c-bad'}
OUTCOMES = {'chosen': 'c-ok', 'dismissed': 'c-mute', 'kept_open': 'c-info'}
CONFIDENCE = {'high', 'medium', 'low'}

EXAMPLE = {
    'lang': 'en-AU',
    'title': 'Should the import job retry failed rows or skip them?',
    'kicker': 'acme-api · decision · 7 November 2026',
    'status': 'decided_split',
    'decision': {'option': 'retry', 'summary': 'Retry each failed row up to three times, then park it in a dead-letter table.',
                 'confidence': 'medium', 'tally': '3 of 4 models'},
    'why': 'Skipped rows are invoices, and the finance team reconciles them monthly; a silent skip turns into a missing invoice. Three retries cover the transient lock errors in the logs.',
    'next': [{'action': 'Add a dead-letter table and a three-attempt retry to the import job.', 'needs_confirmation': False},
             {'action': 'Drop the old skipped-rows log table.', 'needs_confirmation': True}],
    'options': [
        {'id': 'retry', 'label': 'Retry, then dead-letter', 'outcome': 'chosen', 'votes': ['Fable', 'Grok', 'Argon'],
         'reason': 'Keeps every row and bounds the delay.'},
        {'id': 'skip', 'label': 'Skip and log', 'outcome': 'dismissed', 'votes': ['Astra'],
         'reason': 'A log nobody reads loses invoices.'},
    ],
    'models': [
        {'name': 'Fable', 'model': 'claude-fable-5-1', 'verdict': 'chose', 'option': 'retry', 'position': 'The logs show lock timeouts, which a retry clears.'},
        {'name': 'Astra', 'model': 'gpt-6-astra', 'verdict': 'differed', 'option': 'skip', 'position': 'Retries can hammer a locked table.', 'changed': 'Held in round two.'},
        {'name': 'Argon', 'model': 'gemini-4-argon-high', 'verdict': 'chose', 'option': 'retry', 'position': 'Invoices must not be dropped.'},
        {'name': 'Grok', 'model': 'grok-4.7', 'verdict': 'chose', 'option': 'retry', 'position': 'Dead-lettering makes failures visible.'},
    ],
    'dissent': ['Astra: three immediate retries can deepen a lock; back off between attempts.'],
    'evidence': ['jobs/import.ts:88', 'logs/import-2026-11-05.txt:412'],
    'made': ['Four models from four families answered independently, then the split went to a second round.'],
    'source': 'docs/decisions/2026-11-07-import-retries.html',
}


def e(s):
    return html.escape(str(s), quote=True)


def check(spec):
    """Return a list of problems; empty means the spec can be built."""
    problems = []
    for key in ('title', 'kicker', 'status', 'why', 'options', 'models', 'evidence', 'made'):
        if not spec.get(key):
            problems.append(f'missing {key}')
    status = spec.get('status')
    if status and status not in STATUSES:
        problems.append(f'status must be one of {sorted(STATUSES)}')
    options = spec.get('options') or []
    ids = [o.get('id') for o in options]
    if len(options) < 2:
        problems.append('a decision needs at least two options')
    if len(set(ids)) != len(ids):
        problems.append('option ids must be unique')
    for o in options:
        if o.get('outcome') not in OUTCOMES:
            problems.append(f'option {o.get("id")}: outcome must be one of {sorted(OUTCOMES)}')
        if not o.get('label') or not o.get('reason'):
            problems.append(f'option {o.get("id")}: needs a label and a reason')
    chosen = [o for o in options if o.get('outcome') == 'chosen']
    models = spec.get('models') or []
    valid = [m for m in models if m.get('verdict') != 'failed']
    for m in models:
        if m.get('verdict') not in VERDICTS:
            problems.append(f'model {m.get("name")}: verdict must be one of {sorted(VERDICTS)}')
        if not m.get('name') or not m.get('model') or not m.get('position'):
            problems.append(f'model {m.get("name")}: needs a name, the model id that answered, and a position')
        if m.get('verdict') != 'failed' and m.get('option') not in ids:
            problems.append(f'model {m.get("name")}: option {m.get("option")!r} is not one of the options')
    if len(valid) < 2:
        problems.append('fewer than two lanes answered; a panel of one is not a panel')
    failed = {m.get('name') for m in models if m.get('verdict') == 'failed'}
    for o in options:
        for v in o.get('votes', []):
            if v in failed:
                problems.append(f'option {o.get("id")}: counts a vote from {v}, whose lane failed')
    if status in ('decided', 'decided_split'):
        dec = spec.get('decision') or {}
        if len(chosen) != 1:
            problems.append('a decided page needs exactly one chosen option')
        elif dec.get('option') != chosen[0].get('id'):
            problems.append('decision.option must be the chosen option')
        if not dec.get('summary'):
            problems.append('decision.summary is missing')
        if dec.get('confidence') not in CONFIDENCE:
            problems.append(f'decision.confidence must be one of {sorted(CONFIDENCE)}')
        if not spec.get('next'):
            problems.append('a decided page says what happens next')
        if status == 'decided' and spec.get('dissent'):
            problems.append('status "decided" has dissent; use "decided_split"')
        if status == 'decided_split' and not spec.get('dissent'):
            problems.append('status "decided_split" needs the dissent written down')
        if len(chosen) == 1:
            backers = {m.get('name') for m in valid if m.get('option') == chosen[0].get('id')}
            if not backers:
                problems.append('no valid lane chose the winning option; say who decided and why in decision.summary and add a model card for the tie-break')
    if status == 'needs_you':
        q = spec.get('question') or {}
        if not q.get('text') or len(q.get('options') or []) < 2:
            problems.append('status "needs_you" needs question.text and at least two question.options')
        if chosen:
            problems.append('a page that needs your answer has no chosen option yet')
    for n in spec.get('next') or []:
        if 'action' not in n or 'needs_confirmation' not in n:
            problems.append('each next step needs action and needs_confirmation')
    return problems


def chip(cls, text):
    return f'<span class="chip {cls}">{e(text)}</span>'


def build(spec):
    cls, label = STATUSES[spec['status']]
    dec = spec.get('decision') or {}
    parts = [f'<header class="top"><div class="wrap"><p class="kick">{e(spec["kicker"])}</p>'
             f'<h1>{e(spec["title"])}</h1>{chip(cls, label)}</div></header><main><div class="wrap">']
    if spec['status'] == 'needs_you':
        q = spec['question']
        opts = ''.join(f'<li>{e(o)}</li>' for o in q['options'])
        parts.append(f'<section><div class="card decision"><p class="label">Your answer is needed</p>'
                     f'<h2>{e(q["text"])}</h2><ul class="tight">{opts}</ul>'
                     f'<p>{e(q.get("why", ""))}</p></div></section>')
    else:
        parts.append(f'<section><div class="card decision"><p class="label">The decision</p>'
                     f'<h2>{e(dec["summary"])}</h2><p class="meta">{e(dec.get("tally", ""))} · confidence {e(dec["confidence"])}</p></div></section>')
    parts.append(f'<section><h2 class="sm">Why</h2><p>{e(spec["why"])}</p></section>')
    if spec.get('next'):
        items = ''.join(
            f'<li>{e(n["action"])}{" " + chip("c-info", "waits for your OK") if n["needs_confirmation"] else ""}</li>'
            for n in spec['next'])
        parts.append(f'<section><h2 class="sm">What happens next</h2><ul class="tight">{items}</ul></section>')
    rows = ''.join(
        f'<tr><td><b>{e(o["label"])}</b>{" " + chip("c-info", "added by the panel") if o.get("added_by_panel") else ""}</td>'
        f'<td>{chip(OUTCOMES[o["outcome"]], o["outcome"].replace("_", " "))}</td>'
        f'<td>{e(", ".join(o.get("votes", [])) or "none")}</td><td>{e(o["reason"])}</td></tr>'
        for o in spec['options'])
    parts.append('<section><h2 class="sm">The options</h2><div class="tw"><table><thead><tr><th>Option</th><th>Outcome</th>'
                 f'<th>Chosen by</th><th>Reason</th></tr></thead><tbody>{rows}</tbody></table></div></section>')
    cards = ''.join(
        f'<div class="hw-m {VERDICTS[m["verdict"]]}"><div class="hw-mh"><b>{e(m["name"])}</b>{chip(VERDICTS[m["verdict"]], m["verdict"])}</div>'
        f'<p class="meta">{e(m["model"])}</p><p>{e(m["position"])}</p>'
        f'{"<p class=meta>" + e(m["changed"]) + "</p>" if m.get("changed") else ""}</div>'
        for m in spec['models'])
    parts.append(f'<section><h2 class="sm">How each model landed</h2><div class="hw-models">{cards}</div></section>')
    if spec.get('dissent'):
        items = ''.join(f'<li>{e(d)}</li>' for d in spec['dissent'])
        parts.append(f'<section><h2 class="sm">Dissent</h2><ul class="hw-dis">{items}</ul></section>')
    ev = ''.join(f'<li><code>{e(x)}</code></li>' for x in spec['evidence'])
    parts.append(f'<section><h2 class="sm">Evidence</h2><ul class="hw-ev">{ev}</ul></section>')
    made = ''.join(f'<li>{e(x)}</li>' for x in spec['made'])
    parts.append(f'<section><h2 class="sm">How this was decided</h2><ul class="tight">{made}</ul></section>')
    parts.append(f'</div></main><footer><div class="wrap">{e(spec.get("source", ""))}</div></footer>')
    return (f'<!doctype html><html lang="{e(spec.get("lang", "en-AU"))}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(spec.get("page_title", spec["title"]))}</title>'
            f'<style>{CSS}</style></head><body>{"".join(parts)}</body></html>\n')


def main(argv):
    if argv[1:] == ['--example']:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if len(argv) == 3 and argv[1] == '--check':
        problems = check(json.loads(Path(argv[2]).read_text()))
        for p in problems:
            print(f'FAIL  {p}')
        print('ok' if not problems else f'{len(problems)} problem(s)')
        return 1 if problems else 0
    if len(argv) == 3:
        spec = json.loads(Path(argv[1]).read_text())
        problems = check(spec)
        if problems:
            for p in problems:
                print(f'FAIL  {p}')
            return 1
        Path(argv[2]).write_text(build(spec))
        print(f'wrote {argv[2]}')
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
