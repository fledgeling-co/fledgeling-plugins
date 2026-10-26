#!/usr/bin/env python3
"""Build the feedback report HTML from a JSON spec.

Usage:
  build_report.py spec.json out.html          # write the report
  build_report.py --check spec.json           # validate only, exit 1 on any problem
  build_report.py --example                   # print a minimal valid spec

The report has two modes. "questions" renders each open question as a multiple-choice
fieldset with its recommended or default option preselected, the reasoning inside the
question, and a JSON export the reader sends back. "answers" replaces the questions with the
answers that came back and what each one changed; push-back and the other sections stay.

The spec is validated before anything is written, because a report that reaches the feedback
author with a question carrying no preselected option, or an option marked "recommended" that
no panel recommended, cannot be corrected after they have answered it.
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = (HERE.parent / 'assets' / 'report.css').read_text()
TONES = {'ok', 'warn', 'info', 'bad'}
TAGS = {'recommended', 'default'}

EXAMPLE = {
    'mode': 'questions',
    'lang': 'en-US',
    'title': 'Your website feedback: questions and push-back',
    'kicker': 'Acme website · feedback · 1 November 2026',
    'made': [
        'Every point in the feedback was checked against the website and the company files.',
        'Claude Fable 5.1, GPT-6 Astra and Gemini 4 Argon reviewed the feedback and questions independently.',
    ],
    'intro_note': 'Answer the questions below, then download your answers and send the file to Sam.',
    'return_to': 'Sam',
    'source': 'docs/reviews/2026-11-01-feedback-report.html',
    'storage_key': 'acme-feedback-2026-11-01-v1',
    'download_name': 'acme-feedback-answers.json',
    'questions': [{
        'id': 'Q1', 'for': 'Alex', 'title': 'Should the pricing page show annual prices first?',
        'why': 'The feedback asks for annual prices first, but the decisions log records monthly-first after a test in May.',
        'options': [
            {'value': 'annual', 'label': 'Annual first', 'default': True, 'tag': 'recommended', 'sub': 'Recommended: all three models'},
            {'value': 'monthly', 'label': 'Keep monthly first'},
        ],
        'status': {'tone': 'ok', 'label': 'Recommended', 'who': 'all three models'},
        'decision': 'The May test predates the new plans, so its result no longer applies.',
        'models': [{'name': 'Fable', 'tone': 'ok', 'verdict': 'agrees', 'text': 'The test predates the plan change'}],
        'dismissed': [], 'evidence': ['docs/decisions.md:14'],
    }],
    'pushbacks': [], 'understood': ['Renaming the Plans tab.'], 'found': [],
}


def e(s):
    return html.escape(str(s), quote=True)


def check(spec):
    errs = []
    mode = spec.get('mode')
    if mode not in ('questions', 'answers'):
        errs.append('mode must be "questions" or "answers"')
    for k in ('title', 'kicker', 'made', 'source'):
        if not spec.get(k):
            errs.append(f'missing {k}')
    if mode == 'questions':
        for k in ('storage_key', 'download_name', 'return_to'):
            if not spec.get(k):
                errs.append(f'missing {k} (needed for the export)')
        qs = spec.get('questions') or []
        if not qs:
            errs.append('questions mode with no questions: use answers mode or drop the section')
        ids = set()
        for q in qs:
            qid = q.get('id', '?')
            if qid in ids:
                errs.append(f'{qid}: duplicate id')
            ids.add(qid)
            for k in ('id', 'for', 'title', 'why', 'options', 'decision', 'status', 'models'):
                if not q.get(k):
                    errs.append(f'{qid}: missing {k}')
            opts = q.get('options') or []
            if len(opts) < 2:
                errs.append(f'{qid}: needs at least two options')
            defaults = [o for o in opts if o.get('default')]
            if not defaults:
                errs.append(f'{qid}: no preselected option (mark the recommended or assumed default)')
            if not q.get('multi') and len(defaults) > 1:
                errs.append(f'{qid}: single-choice question with {len(defaults)} defaults')
            for o in opts:
                if o.get('default') and o.get('tag') not in TAGS:
                    errs.append(f'{qid}/{o.get("value")}: a preselected option needs tag "recommended" or "default"')
                if not o.get('default') and o.get('tag'):
                    errs.append(f'{qid}/{o.get("value")}: only the preselected option carries a tag')
            st = q.get('status') or {}
            if st.get('tone') not in TONES:
                errs.append(f'{qid}: status.tone must be one of {sorted(TONES)}')
            for m in q.get('models') or []:
                if m.get('tone') not in TONES:
                    errs.append(f'{qid}/{m.get("name")}: model tone must be one of {sorted(TONES)}')
    else:
        if not spec.get('answers'):
            errs.append('answers mode with no answers')
        for a in spec.get('answers') or []:
            for k in ('id', 'for', 'title', 'answer', 'changed'):
                if not a.get(k):
                    errs.append(f'{a.get("id", "?")}: missing {k}')
    for i, p in enumerate(spec.get('pushbacks') or [], 1):
        for k in ('title', 'kind', 'why', 'ruling', 'models'):
            if not p.get(k):
                errs.append(f'push-back {i}: missing {k}')
    return errs


def models_block(models):
    cells = ''.join(
        f'<div class="hw-m c-{m["tone"]}"><div class="hw-mh"><b>{e(m["name"])}</b>'
        f'<span class="chip c-{m["tone"]}">{e(m["verdict"])}</span></div><p>{e(m["text"])}</p></div>'
        for m in models)
    return f'<p class="hw-l">Where each model landed</p><div class="hw-models">{cells}</div>'


def list_block(label, items, cls, code=False):
    if not items:
        return ''
    li = ''.join(f'<li><code>{e(x)}</code></li>' if code else f'<li>{e(x)}</li>' for x in items)
    return f'<p class="hw-l">{label}</p><ul class="{cls}">{li}</ul>'


def question(q):
    t = 'checkbox' if q.get('multi') else 'radio'
    opts = ''
    for o in q['options']:
        chk = ' checked' if o.get('default') else ''
        tag = o.get('tag')
        badge = f'<i class="def{" rec" if tag == "recommended" else ""}">{tag}</i>' if tag else ''
        sub = f'<em>{e(o["sub"])}</em>' if o.get('sub') else ''
        opts += (f'<label class="opt"><input type="{t}" name="{e(q["id"])}" value="{e(o["value"])}" '
                 f'data-default="{1 if o.get("default") else 0}"{chk}><span><b>{e(o["label"])}</b>{sub}{badge}</span></label>')
    st = q['status']
    how = (f'<details class="how"><summary>How the panel decided</summary><div class="hw">'
           f'<div class="hw-top"><span class="chip c-{st["tone"]}">{e(st["label"])}</span><span class="hw-who">{e(st.get("who", ""))}</span></div>'
           f'<div class="hw-dec"><p class="hw-l">Panel decision</p><p>{e(q["decision"])}</p></div>'
           f'{models_block(q["models"])}{list_block("Considered and dismissed", q.get("dismissed"), "hw-dis")}'
           f'{list_block("Evidence", q.get("evidence"), "hw-ev", code=True)}</div></details>')
    return (f'<fieldset class="card qf" id="f-{e(q["id"])}" data-id="{e(q["id"])}" data-q="{e(q["title"])}" data-who="{e(q["for"])}">'
            f'<legend class="meta">{e(q["id"])} · for {e(q["for"])}</legend><h3>{e(q["title"])}</h3>'
            f'<p class="why"><strong>Why we’re asking.</strong> {e(q["why"])}</p>{opts}{how}'
            f'<label class="note">Note (optional)<textarea name="{e(q["id"])}-note" rows="2" placeholder="Any constraint or detail behind your answer"></textarea></label></fieldset>')


def answer(a):
    return (f'<div class="card"><p class="meta">{e(a["id"])} · for {e(a["for"])}</p><h3>{e(a["title"])}</h3>'
            f'<p><span class="chip c-ok">Answer</span> {e(a["answer"])}</p>'
            f'<p class="why"><strong>What changed.</strong> {e(a["changed"])}</p></div>')


def pushback(i, p):
    extra = f'<p>{e(p["extra"])}</p>' if p.get('extra') else ''
    return (f'<div class="card" id="p{i}"><p class="meta">Push-back {i}</p><h3>{e(p["title"])}</h3>'
            f'<p><span class="chip c-info">{e(p["kind"])}</span></p>'
            f'<p class="why"><strong>Why we pushed back.</strong> {e(p["why"])}</p>'
            f'<div class="hw-dec pb"><p class="hw-l">{e(p.get("ruling_label", "Panel ruling"))}</p><p>{e(p["ruling"])}</p></div>{extra}'
            f'<details class="how"><summary>How we got there</summary><div class="hw">{models_block(p["models"])}'
            f'{list_block("Considered and dismissed", p.get("dismissed"), "hw-dis")}'
            f'{list_block("Evidence", p.get("evidence"), "hw-ev", code=True)}</div></details></div>')


def export_js(spec):
    return '''(function(){
var KEY=%s,SRC=%s,FILE=%s,TO=%s,f=document.getElementById('qform'),out=document.getElementById('out'),st=document.getElementById('status');
function collect(){var a=[];f.querySelectorAll('fieldset.qf').forEach(function(fs){var ins=[].slice.call(fs.querySelectorAll('input')),sel=ins.filter(function(i){return i.checked});
a.push({id:fs.dataset.id,for:fs.dataset.who,question:fs.dataset.q,answer:sel.map(function(i){return{value:i.value,label:i.closest('label').querySelector('b').textContent}}),is_default:ins.every(function(i){return i.checked===(i.dataset.default==='1')}),note:fs.querySelector('textarea').value.trim()})});
return{source:SRC,exported_at:new Date().toISOString(),answers:a}}
function render(){var d=collect();out.value=JSON.stringify(d,null,2);var c=d.answers.filter(function(x){return!x.is_default}).length;st.textContent=c?c+' answer'+(c>1?'s':'')+' changed from the starting choice.':'All answers are at their starting choice.';
try{localStorage.setItem(KEY,JSON.stringify(d.answers.map(function(x){return{id:x.id,v:x.answer.map(function(y){return y.value}),n:x.note}})))}catch(e){}}
try{var saved=JSON.parse(localStorage.getItem(KEY)||'null');if(saved)saved.forEach(function(s){var fs=f.querySelector('fieldset[data-id="'+s.id+'"]');if(!fs)return;fs.querySelectorAll('input').forEach(function(i){i.checked=s.v.indexOf(i.value)>-1});fs.querySelector('textarea').value=s.n||''})}catch(e){}
f.addEventListener('change',render);f.addEventListener('input',render);
document.getElementById('dl').addEventListener('click',function(){var b=new Blob([out.value],{type:'application/json'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download=FILE;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},1000);st.textContent='Downloaded '+FILE+'.'});
document.getElementById('cp').addEventListener('click',function(){var ok=function(){st.textContent='Copied. Send it back to '+TO+'.'},fb=function(){document.getElementById('jsonbox').open=true;out.focus();out.select();try{document.execCommand('copy');ok()}catch(e){st.textContent='Open “Show the JSON”, select it and copy it.'}};if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(out.value).then(ok,fb)}else fb()});
document.getElementById('rs').addEventListener('click',function(){f.querySelectorAll('input').forEach(function(i){i.checked=i.dataset.default==='1'});f.querySelectorAll('textarea').forEach(function(t){t.value=''});render()});
render();
})();''' % tuple(json.dumps(spec[k]) for k in ('storage_key', 'source', 'download_name', 'return_to'))


def build(spec):
    made = ''.join(f'<li>{e(x)}</li>' for x in spec['made'])
    note = f'<p>{e(spec["intro_note"])}</p>' if spec.get('intro_note') else ''
    parts = [f'<section id="about" class="intro"><p class="kick-d">{e(spec["kicker"])}</p><h1>{e(spec["title"])}</h1>'
             f'<div class="card"><h2 class="sm">How this report was made</h2><ul class="tight">{made}</ul>{note}</div></section>']
    script = ''
    if spec['mode'] == 'questions':
        lead = spec.get('questions_lead', 'Each question starts on the models’ <i class="def rec">recommended</i> choice or, where they couldn’t settle it, an assumed <i class="def">default</i>. Change any answer you disagree with and add a note where it helps; your answers are saved in this browser. <a href="#export">Jump to export</a>')
        qs = ''.join(question(q) for q in spec['questions'])
        parts.append(f'<section id="answer"><h2>{e(spec.get("questions_heading", "Questions for you"))}</h2><p class="lead">{lead}</p><form id="qform">{qs}</form>'
                     '<div class="card exp" id="export"><div class="btns"><button type="button" id="dl" class="btn primary">Download answers (JSON)</button>'
                     '<button type="button" id="cp" class="btn">Copy JSON</button><button type="button" id="rs" class="btn">Reset to starting choices</button></div>'
                     '<p class="meta" id="status" role="status" aria-live="polite"></p><details id="jsonbox"><summary>Show the JSON</summary>'
                     '<textarea id="out" rows="8" readonly aria-label="Answers as JSON"></textarea></details></div></section>')
        script = f'<script>{export_js(spec)}</script>'
    else:
        ans = ''.join(answer(a) for a in spec['answers'])
        parts.append(f'<section id="answer"><h2>{e(spec.get("answers_heading", "Your answers"))}</h2><p class="lead">{e(spec.get("answers_lead", "What was chosen for each question, and what changed."))}</p>{ans}</section>')
    pbs = spec.get('pushbacks') or []
    if pbs:
        parts.append(f'<section id="pushbacks"><h2>Where we’d push back</h2><p class="lead">{e(spec.get("pushbacks_lead", "Where the feedback, as written, would weaken a page or the project as a whole, and what we’d do instead."))}</p>'
                     + ''.join(pushback(i, p) for i, p in enumerate(pbs, 1)) + '</section>')
    if spec.get('understood'):
        parts.append(f'<section id="understood"><h2>{e(spec.get("understood_heading", "What we’ll do as you asked"))}</h2><div class="card"><ul class="tight">'
                     + ''.join(f'<li>{e(x)}</li>' for x in spec['understood']) + '</ul></div></section>')
    if spec.get('found'):
        parts.append(f'<section id="found"><h2>{e(spec.get("found_heading", "Other things we noticed"))}</h2><div class="card"><ul class="tight">'
                     + ''.join(f'<li>{e(x)}</li>' for x in spec['found']) + '</ul></div></section>')
    return (f'<!doctype html><html lang="{e(spec.get("lang", "en-US"))}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(spec.get("page_title", "Feedback report"))}</title>'
            f'<style>{CSS}</style></head><body><main><div class="wrap">{"".join(parts)}</div></main>{script}</body></html>\n')


def main(argv):
    if argv[1:2] == ['--example']:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    only_check = argv[1:2] == ['--check']
    args = argv[2:] if only_check else argv[1:]
    if not args or (not only_check and len(args) != 2):
        print(__doc__, file=sys.stderr)
        return 2
    spec = json.loads(Path(args[0]).read_text())
    errs = check(spec)
    if errs:
        print(f'spec has {len(errs)} problem(s):', file=sys.stderr)
        for x in errs:
            print(f'  - {x}', file=sys.stderr)
        return 1
    n_q = len(spec.get('questions') or spec.get('answers') or [])
    summary = f'{spec["mode"]}: {n_q} item(s), {len(spec.get("pushbacks") or [])} push-back(s), {len(spec.get("understood") or [])} understood, {len(spec.get("found") or [])} found'
    if only_check:
        print(f'ok · {summary}')
        return 0
    Path(args[1]).write_text(build(spec))
    print(f'wrote {args[1]} · {summary}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
