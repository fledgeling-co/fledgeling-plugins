#!/usr/bin/env python3
"""build_page.py — render meta/items/questions into one self-contained page.

    python3 build_page.py <model-dir> --out <file.html> [--theme <tokens.json>]

The whole report is rendered here, in Python, so it reads with JavaScript off:
the status half is the part someone may open on a phone with a blocked script,
and a status report that renders blank is worse than no report. JavaScript adds
only the four things that genuinely need it — recording that an answer was
looked at, the running tally, restoring a part-finished session, and the export.

Four mechanics are subtle enough that hand-typing them per run has gone wrong,
which is why they live in a script:

  * confirmation is bound to `click` as well as `change`. Re-selecting an
    already-selected radio fires no `change` event, and that click is exactly
    how a reader confirms a default they agree with.
  * every question carries an explicit "not deciding this yet" option, so a
    skipped question exports as `deferred` rather than vanishing into the
    pre-selected default it never looked at.
  * a note attached to an answer raises `blocksAutomation` unless the reader
    clears it, because a qualified answer is not the answer its label says.
  * the export carries each option's stated consequence, not just its label, so
    whatever acts on the file cannot read more into a terse label than it meant.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys

DEFAULT_THEME = {
    "bg": "#FBFAF8", "surface": "#FFFFFF", "ink": "#1B1A18", "muted": "#5C5851",
    "line": "#E3DFD7", "accent": "#8C5A2B", "accent_soft": "#F5EDE3",
    "urgent": "#A8321E", "high": "#B46A12", "medium": "#4A6741", "low": "#6E6A63",
    "serif": "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif",
    "sans": "'Avenir Next','Segoe UI',system-ui,-apple-system,sans-serif",
    "mono": "'SF Mono',ui-monospace,'Cascadia Mono',Menlo,monospace",
}

URGENCY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
URGENCY_WORD = {"urgent": "Urgent", "high": "High", "medium": "Medium", "low": "Low"}
OWNER_WORD = {"you": "Your call", "agent": "I can do this", "someone-else": "Someone else"}

# Deliberately not a progress bar. Each word says what was actually reached, and
# none of them can be averaged into a percentage.
STAGE_WORD = {
    "not-started": "Not started", "in-progress": "Being built", "built": "Built, not deployed",
    "tested": "Tested, not deployed", "deployed": "Deployed", "accepted": "Deployed and accepted",
    "blocked": "Blocked", "unknown": "Not verifiable from here",
}
STAGE_TONE = {
    "not-started": "n", "in-progress": "w", "built": "w", "tested": "w",
    "deployed": "g", "accepted": "g", "blocked": "r", "unknown": "q",
}
EFFECT_WORD = {
    "fully-releases": "releases this completely",
    "removes-one-blocker": "removes one of its blockers",
    "enables-planning": "lets it be planned, not finished",
}

CSS = """
:root{--bg:%(bg)s;--surface:%(surface)s;--ink:%(ink)s;--muted:%(muted)s;--line:%(line)s;
--accent:%(accent)s;--accent-soft:%(accent_soft)s;--urgent:%(urgent)s;--high:%(high)s;
--medium:%(medium)s;--low:%(low)s;--serif:%(serif)s;--sans:%(sans)s;--mono:%(mono)s;
--bar:0px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#16151A;--surface:#1E1D23;
--ink:#EDEBE6;--muted:#A5A19A;--line:#33313A;--accent:#D69A63;--accent-soft:#2A2530;
--urgent:#E8836F;--high:#DFAE63;--medium:#8FB585;--low:#8C8880}}
:root[data-theme="dark"]{--bg:#16151A;--surface:#1E1D23;--ink:#EDEBE6;--muted:#A5A19A;
--line:#33313A;--accent:#D69A63;--accent-soft:#2A2530;--urgent:#E8836F;--high:#DFAE63;
--medium:#8FB585;--low:#8C8880}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
font-size:17px;line-height:1.55;-webkit-text-size-adjust:100%%;padding-bottom:var(--bar)}
.wrap{max-width:52rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}
a{color:var(--accent)}
h1,h2,h3{font-family:var(--serif);font-weight:600;line-height:1.2;margin:0}
h1{font-size:2.4rem;letter-spacing:-.01em}
h2{font-size:1.55rem;margin:3.5rem 0 .35rem;scroll-margin-top:1rem}
h3{font-size:1.12rem;font-family:var(--sans);font-weight:650;letter-spacing:-.005em}
.head{display:flex;gap:1rem;align-items:flex-start;justify-content:space-between;margin:0 0 .7rem}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;
color:var(--muted);margin:0}
.themer{display:flex;flex:0 0 auto;border:1px solid var(--line);border-radius:3px;overflow:hidden}
.themer button{font:inherit;font-family:var(--mono);font-size:.68rem;letter-spacing:.06em;
text-transform:uppercase;padding:0 .6rem;min-height:36px;border:0;border-left:1px solid var(--line);
background:transparent;color:var(--muted);cursor:pointer}
.themer button:first-child{border-left:0}
.themer button[aria-pressed="true"]{background:var(--accent-soft);color:var(--ink)}
.themer button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.stand{font-family:var(--serif);font-size:1.22rem;line-height:1.5;color:var(--ink);
margin:1rem 0 0;max-width:40rem}
.meta{color:var(--muted);font-size:.85rem;margin:1.4rem 0 0}
.rule{border:0;border-top:1px solid var(--line);margin:2.5rem 0 0}
.note{font-size:.9rem;color:var(--muted);margin:.5rem 0 0}
.contract{border-left:2px solid var(--accent);padding:.15rem 0 .15rem .95rem;margin:2rem 0 0;
font-size:.95rem;color:var(--muted)}
.contract b{color:var(--ink);font-weight:650}
.top{background:var(--accent-soft);border:1px solid var(--line);border-radius:3px;
padding:1.15rem 1.35rem;margin:2rem 0 0}
.top h3{margin:0 0 .55rem;font-size:.94rem}
.top ol{margin:0;padding-left:1.2rem}
.top li{margin:.45rem 0;font-size:.95rem}
.top li span{display:block;color:var(--muted);font-size:.85rem;margin-top:.1rem}
.grp{margin:2.6rem 0 0}
.grp>h3{color:var(--muted);font-size:.78rem;font-family:var(--mono);letter-spacing:.09em;
text-transform:uppercase;padding-bottom:.5rem;border-bottom:1px solid var(--line)}
.item{border-bottom:1px solid var(--line);padding:1.35rem 0}
.item:last-child{border-bottom:0}
.ihead{display:flex;gap:.7rem;align-items:baseline;flex-wrap:wrap}
.ihead h3{flex:1 1 16rem;min-width:0}
.chip{font-family:var(--mono);font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;
border:1px solid currentColor;border-radius:2px;padding:.13rem .42rem;white-space:nowrap}
.u-urgent{color:var(--urgent)}.u-high{color:var(--high)}
.u-medium{color:var(--medium)}.u-low{color:var(--low)}
.stage{font-family:var(--mono);font-size:.68rem;letter-spacing:.05em;padding:.13rem .45rem;
border-radius:2px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.st-g{color:var(--medium);border-color:currentColor}
.st-r{color:var(--urgent);border-color:currentColor}
.st-q{color:var(--muted);border-style:dashed}
.plain{margin:.55rem 0 0;font-size:1.02rem}
dl{margin:.85rem 0 0;display:grid;grid-template-columns:8.5rem 1fr;gap:.4rem .95rem;font-size:.93rem}
dt{color:var(--muted);font-family:var(--mono);font-size:.7rem;letter-spacing:.07em;
text-transform:uppercase;padding-top:.22rem}
dd{margin:0}
dd.ev{color:var(--muted);font-size:.86rem}
dd.ev code{font-family:var(--mono);font-size:.85em;background:var(--accent-soft);
padding:.05rem .3rem;border-radius:2px}
.wait{display:inline-block;margin:.75rem 0 0;font-size:.9rem;background:var(--accent-soft);
border:1px solid var(--line);border-radius:2px;padding:.3rem .6rem;text-decoration:none}
.q{border:1px solid var(--line);background:var(--surface);border-radius:3px;
padding:1.5rem 1.6rem;margin:1.5rem 0 0;scroll-margin-top:1rem;scroll-margin-bottom:7rem}
.q.done{border-color:var(--accent)}
.qhead{display:flex;gap:.7rem;align-items:baseline;flex-wrap:wrap}
.qhead h3{flex:1 1 16rem;font-size:1.18rem;font-family:var(--serif);font-weight:600}
.qn{font-family:var(--mono);font-size:.7rem;color:var(--muted)}
.qcard{font-family:var(--mono);font-size:.72rem;color:var(--muted);text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:1px}
.qcard:hover,.qcard:focus{color:var(--ink)}
.why{color:var(--muted);font-size:.95rem;margin:.5rem 0 0}
fieldset{border:0;padding:0;margin:1.15rem 0 0;min-width:0}
legend{padding:0;font-size:.78rem;font-family:var(--mono);letter-spacing:.08em;
text-transform:uppercase;color:var(--muted);margin-bottom:.55rem}
.opt{display:flex;align-items:flex-start;gap:.7rem;padding:.62rem .75rem;border-radius:3px;
border:1px solid transparent;cursor:pointer}
.opt:hover{background:var(--accent-soft)}
.opt input{margin:2px 0 0;flex:0 0 auto;width:17px;height:17px;accent-color:var(--accent)}
.otext{flex:1 1 auto;min-width:0}
.olabel{font-weight:600;font-size:.99rem}
.opt input:checked + .otext .olabel::before{content:"▸ ";color:var(--accent);font-weight:700}
.oconseq{color:var(--muted);font-size:.89rem;margin-top:.1rem}
.rec{font-family:var(--mono);font-size:.62rem;letter-spacing:.09em;text-transform:uppercase;
color:var(--accent);border:1px solid currentColor;border-radius:2px;padding:.08rem .35rem;
margin-left:.45rem;vertical-align:.08em;white-space:nowrap}
.because{color:var(--muted);font-size:.87rem;margin-top:.25rem;font-style:italic}
.opt.defer .olabel{font-weight:500;color:var(--muted)}
.nolabel{font-size:.8rem;color:var(--muted);display:block;margin:1.05rem 0 .3rem}
textarea{width:100%%;min-height:4.4rem;font:inherit;font-size:.94rem;padding:.6rem .7rem;
border:1px solid var(--line);border-radius:3px;background:var(--bg);color:var(--ink);resize:vertical}
.qual{display:flex;gap:.55rem;align-items:flex-start;margin:.55rem 0 0;font-size:.86rem;
color:var(--muted)}
/* `display` on a class beats the UA sheet's [hidden]{display:none}, so syncQual was
   setting the attribute on every question and none of them ever went away. The row
   showed, checked, above an empty note box — telling the reader a note they had not
   written qualified an answer they had not given. */
.qual[hidden]{display:none}
.qual input{margin:3px 0 0;accent-color:var(--accent)}
.rel{margin:1.05rem 0 0;font-size:.86rem;color:var(--muted)}
.rel b{color:var(--ink);font-weight:600}
.rel li{margin:.15rem 0}
.rel ul{margin:.25rem 0 0;padding-left:1.1rem}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.bar{position:fixed;left:0;right:0;bottom:0;background:var(--surface);
border-top:1px solid var(--line);padding:.8rem 1.25rem;display:flex;gap:.9rem;
align-items:center;justify-content:center;flex-wrap:wrap;font-size:.9rem;z-index:20}
.bar button{font:inherit;font-weight:650;font-size:.9rem;padding:.5rem 1.1rem;border-radius:3px;
border:1px solid var(--accent);background:var(--accent);color:var(--bg);cursor:pointer;
min-height:44px}
.bar button.ghost{background:transparent;color:var(--accent)}
.tally{color:var(--muted)}
.tally b{color:var(--ink)}
.warn{width:100%%;text-align:center;color:var(--muted);font-size:.8rem}
.summary{display:none}
@media (max-width:520px){dl{grid-template-columns:1fr;gap:.15rem}
dt{padding-top:.5rem}.wrap{padding:1.75rem 1rem 5rem}h1{font-size:1.85rem}
.q{padding:1.15rem 1.1rem}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media print{.bar,.wait,.themer{display:none}body{background:#FDFDFC;color:#141414;padding-bottom:0}
.q,.top{break-inside:avoid;border:1px solid #ccc}.item{break-inside:avoid}
.summary{display:block;break-before:page}
.summary li{margin:.5rem 0;font-size:.9rem}a{text-decoration:none;color:#141414}}
"""

JS = r"""
(function(){
  var MODEL = __MODEL__;
  var KEY = 'wl:' + MODEL.slug;
  var state = {};

  function el(id){ return document.getElementById(id); }

  function mark(card, id){
    var s = state[id] || (state[id] = {});
    s.confirmed = true;
    card.classList.add('done');
    card.dataset.confirmed = 'yes';
    tally();
    save();
  }

  function tally(){
    var total = MODEL.questions.length, done = 0, deferred = 0;
    MODEL.questions.forEach(function(q){
      var s = state[q.id];
      if (!s || !s.confirmed) return;
      done++;
      if (isDeferred(q)) deferred++;
    });
    var t = el('tally');
    if (!t) return;
    t.innerHTML = '<b>' + done + '</b> of ' + total + ' looked at' +
      (deferred ? ' · <b>' + deferred + '</b> put off' : '');
  }

  function isDeferred(q){
    var f = document.forms['q-' + q.id];
    if (!f) return false;
    var v = f.elements['answer'];
    if (!v) return false;
    if (v.length){
      for (var i = 0; i < v.length; i++) if (v[i].checked && v[i].value === '__defer__') return true;
      return false;
    }
    return v.value === '__defer__';
  }

  function read(q){
    var f = document.forms['q-' + q.id];
    var s = state[q.id] || {};
    var out = { id: q.id, title: q.title, kind: q.kind, defaultPolicy: q.default_policy };
    if (q.card) out.card = q.card;
    var chosen = [];
    if (q.kind === 'text'){
      var ta = f.elements['answer'];
      out.answer = (ta && ta.value || '').trim();
      out.answered = !!out.answer;
    } else {
      var v = f.elements['answer'];
      var list = v && v.length ? Array.prototype.slice.call(v) : (v ? [v] : []);
      list.forEach(function(i){ if (i.checked) chosen.push(i.value); });
      out.answer = q.kind === 'multi' ? chosen : (chosen[0] || null);
      out.answered = chosen.length > 0 && chosen[0] !== '__defer__';
      // The export carries what each chosen option actually commits to, so that
      // whatever acts on this file cannot read more into a four-word label.
      out.optionConsequences = chosen.map(function(val){
        if (val === '__defer__') return { value: val, label: 'Not deciding this yet', consequence: 'Everything this releases stays where it is.' };
        var o = (q.options || []).filter(function(x){ return x.value === val; })[0] || {};
        return { value: val, label: o.label, consequence: o.consequence };
      });
      var recs = (q.options || []).filter(function(o){ return o.recommended; }).map(function(o){ return o.value; });
      if (!out.answered) out.answerOrigin = 'none';
      else if (recs.length && chosen.every(function(c){ return recs.indexOf(c) >= 0; }) && chosen.length === recs.length)
        out.answerOrigin = 'accepted-recommendation';
      else if (recs.length) out.answerOrigin = 'chose-differently';
      else out.answerOrigin = 'own-choice';
    }
    var note = f.elements['note'];
    out.note = note ? note.value.trim() : '';
    var qual = f.elements['qualifies'];
    // A note is treated as changing the answer unless its author says otherwise.
    // The safe direction is the one that stops rather than the one that proceeds.
    out.noteQualifiesAnswer = out.note ? (qual ? !!qual.checked : true) : false;
    out.blocksAutomation = out.noteQualifiesAnswer;
    if (chosen.indexOf('__defer__') >= 0) out.state = 'deferred';
    else if (s.confirmed) out.state = 'confirmed';
    else if (q.default_policy === 'recommended') out.state = 'as-found';
    else out.state = 'unanswered';
    out.unblocks = q.unblocks || [];
    return out;
  }

  function payloadNow(){
    var answers = MODEL.questions.map(read);
    return {
      schema: 'whats-left/1',
      project: MODEL.project,
      slug: MODEL.slug,
      reportGeneratedAt: MODEL.generatedAt,
      exportedAt: new Date().toISOString(),
      // as-found means the page's own suggestion, never looked at by a human.
      // Anything acting on this file should treat it as a proposal, not a decision.
      states: { confirmed: 'looked at and settled', 'as-found': 'the page proposed it; nobody confirmed it',
                deferred: 'deliberately put off; still blocking', unanswered: 'no answer' },
      answers: answers,
      counts: {
        total: answers.length,
        confirmed: answers.filter(function(a){ return a.state === 'confirmed'; }).length,
        asFound: answers.filter(function(a){ return a.state === 'as-found'; }).length,
        deferred: answers.filter(function(a){ return a.state === 'deferred'; }).length,
        unanswered: answers.filter(function(a){ return a.state === 'unanswered'; }).length,
        blockingAutomation: answers.filter(function(a){ return a.blocksAutomation; }).length
      }
    };
  }

  function save(){
    try {
      var d = {};
      MODEL.questions.forEach(function(q){
        var f = document.forms['q-' + q.id];
        if (!f) return;
        var a = read(q);
        d[q.id] = { answer: a.answer, note: a.note, qualifies: a.noteQualifiesAnswer,
                    confirmed: (state[q.id] || {}).confirmed || false };
      });
      localStorage.setItem(KEY, JSON.stringify(d));
    } catch (e) { /* file:// and private windows both throw; the export is the record */ }
  }

  function restore(){
    var raw;
    try { raw = localStorage.getItem(KEY); } catch (e) { return; }
    if (!raw) return;
    var d;
    try { d = JSON.parse(raw); } catch (e) { return; }
    MODEL.questions.forEach(function(q){
      var s = d[q.id];
      if (!s) return;
      var f = document.forms['q-' + q.id];
      if (!f) return;
      var v = f.elements['answer'];
      if (q.kind === 'text'){ if (v && s.answer) v.value = s.answer; }
      else if (v){
        var want = [].concat(s.answer || []);
        var list = v.length ? Array.prototype.slice.call(v) : [v];
        list.forEach(function(i){ i.checked = want.indexOf(i.value) >= 0; });
      }
      if (s.note && f.elements['note']) f.elements['note'].value = s.note;
      if (f.elements['qualifies']) f.elements['qualifies'].checked = s.qualifies !== false && !!s.note;
      if (s.confirmed){ state[q.id] = { confirmed: true }; document.getElementById('q-' + q.id).classList.add('done'); }
    });
  }

  function download(){
    var payload = payloadNow();
    var blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = MODEL.slug + '-answers.json';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
    window.__wlExported = true;
  }

  MODEL.questions.forEach(function(q){
    var card = document.getElementById('q-' + q.id);
    var f = document.forms['q-' + q.id];
    if (!card || !f) return;
    var inputs = f.querySelectorAll('input[name="answer"]');
    Array.prototype.forEach.call(inputs, function(input){
      // `click` as well as `change`: re-selecting the option that is already
      // selected fires no change event, and that click is the confirmation.
      var handle = function(){ if (q.kind !== 'multi') syncQual(f); mark(card, q.id); };
      input.addEventListener('click', handle);
      input.addEventListener('change', handle);
    });
    var ta = f.elements['note'];
    if (ta) ta.addEventListener('input', function(){ syncQual(f); save(); });
    var ans = f.elements['answer'];
    if (q.kind === 'text' && ans) ans.addEventListener('input', function(){ mark(card, q.id); });
    var qual = f.elements['qualifies'];
    if (qual) qual.addEventListener('change', save);
    syncQual(f);
  });

  function syncQual(f){
    var row = f.querySelector('.qual');
    if (!row) return;
    var has = (f.elements['note'] && f.elements['note'].value.trim()) ? true : false;
    row.hidden = !has;
    if (has && f.elements['qualifies'] && !f.dataset.qualTouched) f.elements['qualifies'].checked = true;
  }

  var exp = el('export'); if (exp) exp.addEventListener('click', download);
  var pr = el('print'); if (pr) pr.addEventListener('click', function(){ window.print(); });

  window.addEventListener('beforeunload', function(e){
    var any = MODEL.questions.some(function(q){ return (state[q.id] || {}).confirmed; });
    if (any && !window.__wlExported){ e.preventDefault(); e.returnValue = ''; }
  });

  restore();
  tally();
  // Audit seam: the auditor reads the export without clicking the button.
  var TKEY = KEY + ':theme';
  function paintTheme(){
    var cur = null;
    try { cur = localStorage.getItem(TKEY); } catch (e) {}
    if (cur !== 'light' && cur !== 'dark') cur = 'system';
    if (cur === 'system') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', cur);
    Array.prototype.forEach.call(document.querySelectorAll('[data-theme-set]'), function(b){
      b.setAttribute('aria-pressed', b.getAttribute('data-theme-set') === cur ? 'true' : 'false');
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-theme-set]'), function(b){
    b.addEventListener('click', function(){
      var v = b.getAttribute('data-theme-set');
      try { if (v === 'system') localStorage.removeItem(TKEY); else localStorage.setItem(TKEY, v); } catch (e) {}
      paintTheme();
    });
  });
  paintTheme();

  window.__wl = { payload: payloadNow, state: state, model: MODEL };
})();
"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<style>{css}</style>
<script>{themescript}</script>
</head>
<body>
<main class="wrap">
<div class="head"><p class="eyebrow">{eyebrow}</p>{themer}</div>
<h1>{title}</h1>
<p class="stand">{standfirst}</p>
<p class="meta">{meta}</p>
{contract}
{top}
<hr class="rule">
<h2 id="work">Where everything stands</h2>
<p class="note">{items_note}</p>
{groups}
<hr class="rule">
<h2 id="decisions">What is waiting on you</h2>
<p class="note">{q_note}</p>
{questions}
{summary}
{methods}
</main>
{bar}
<script>{js}</script>
</body>
</html>
"""


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


def rich(s) -> str:
    """Escape, then allow `code` spans — the only markup the model may carry."""
    out = html.escape(str(s or ""), quote=True)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", out)


def build(model_dir: pathlib.Path, out: pathlib.Path, theme_path: pathlib.Path | None) -> int:
    meta = json.loads((model_dir / "meta.json").read_text())
    items = json.loads((model_dir / "items.json").read_text())
    questions = json.loads((model_dir / "questions.json").read_text())

    theme = dict(DEFAULT_THEME)
    if theme_path and theme_path.exists():
        theme.update(json.loads(theme_path.read_text()))

    warnings: list[str] = []
    q_by_id = {q["id"]: q for q in questions}
    item_by_id = {it["id"]: it for it in items}

    # ---- top strip: the cheapest asks that release the most ------------------
    top_html = ""
    ranked = []
    for q in questions:
        rel = q.get("unblocks") or []
        full = sum(1 for u in rel if u.get("effect") == "fully-releases")
        ranked.append((-(full * 2 + len(rel)), q))
    ranked.sort(key=lambda p: p[0])
    picks = [q for _, q in ranked[:3] if q.get("unblocks")]
    if picks:
        lis = []
        for q in picks:
            rel = q.get("unblocks") or []
            names = [item_by_id[u["item"]]["title"] for u in rel if u.get("item") in item_by_id]
            full = [u for u in rel if u.get("effect") == "fully-releases"]
            if full:
                effect = f"releases {len(full)} item{'s' if len(full) != 1 else ''} outright"
            else:
                effect = f"moves {len(rel)} item{'s' if len(rel) != 1 else ''} forward without finishing any"
            lis.append(
                f'<li><a href="#q-{esc(q["id"])}">{esc(q["title"])}</a>'
                f'<span>{esc(effect)} — {esc(", ".join(names[:3]))}</span></li>'
            )
        top_html = ('<div class="top"><h3>If you answer only three things, answer these</h3>'
                    f'<ol>{"".join(lis)}</ol></div>')

    # ---- items --------------------------------------------------------------
    order: list[str] = []
    for it in items:
        if it["group"] not in order:
            order.append(it["group"])
    groups_html = []
    for g in order:
        rows = [it for it in items if it["group"] == g]
        rows.sort(key=lambda it: URGENCY_ORDER.get(it.get("urgency"), 9))
        cards = []
        for it in rows:
            u = it.get("urgency", "low")
            st = it.get("stage", "unknown")
            wait = ""
            blocked = it.get("blocked_by")
            if blocked:
                first = (blocked if isinstance(blocked, list) else [blocked])[0]
                if first in q_by_id:
                    wait = (f'<a class="wait" href="#q-{esc(first)}">Waiting on you — '
                            f'{esc(q_by_id[first]["title"])} ↓</a>')
                else:
                    warnings.append(f"item {it['id']}: blocked_by {first!r} has no question")
            ev = ""
            if (it.get("evidence") or "").strip():
                ev = f'<dt>How I know</dt><dd class="ev">{rich(it["evidence"])}</dd>'
            cards.append(
                f'<article class="item" id="i-{esc(it["id"])}" data-owner="{esc(it.get("owner"))}">'
                f'<div class="ihead"><h3>{esc(it.get("title") or it["id"])}</h3>'
                f'<span class="chip u-{esc(u)}">{esc(URGENCY_WORD.get(u, u))}</span>'
                f'<span class="stage st-{esc(STAGE_TONE.get(st, "n"))}">{esc(STAGE_WORD.get(st, st))}</span></div>'
                f'<p class="plain">{esc(it["plain"])}</p>'
                f'<dl><dt>Where it got to</dt><dd>{rich(it["state"])}</dd>'
                f'<dt>What is live</dt><dd>{rich(it["live"])}</dd>{ev}'
                f'<dt>From you</dt><dd>{rich(it["from_you"])}</dd>'
                f'<dt>Then</dt><dd>{rich(it["remaining"])}</dd>'
                f'<dt>Owner</dt><dd>{esc(OWNER_WORD.get(it.get("owner"), it.get("owner")))}</dd></dl>'
                f'{wait}</article>'
            )
        groups_html.append(f'<section class="grp"><h3>{esc(g)}</h3>{"".join(cards)}</section>')

    # ---- questions ----------------------------------------------------------
    q_html = []
    for n, q in enumerate(questions, 1):
        kind = q["kind"]
        policy = q.get("default_policy", "recommended" if kind != "text" else "none")
        opts_html = []
        if kind == "text":
            body = (f'<label class="nolabel" for="a-{esc(q["id"])}">Your answer</label>'
                    f'<textarea id="a-{esc(q["id"])}" name="answer" '
                    f'placeholder="{esc(q.get("placeholder") or "")}"></textarea>')
        else:
            typ = "radio" if kind == "single" else "checkbox"
            for j, o in enumerate(q.get("options", [])):
                oid = f'o-{q["id"]}-{j}'
                pre = " checked" if (policy == "recommended" and o.get("recommended")) else ""
                badge = '<span class="rec">Recommended</span>' if o.get("recommended") else ""
                because = (f'<div class="because">{rich(o["because"])}</div>'
                           if o.get("recommended") and o.get("because") else "")
                opts_html.append(
                    f'<label class="opt" for="{oid}">'
                    f'<input type="{typ}" id="{oid}" name="answer" value="{esc(o["value"])}"{pre}>'
                    f'<span class="otext"><span class="olabel">{esc(o["label"])}</span>{badge}'
                    f'<div class="oconseq">{rich(o.get("consequence"))}</div>{because}</span></label>'
                )
            # A skip is not an answer. Recorded, it stays visibly blocking.
            did = f'o-{q["id"]}-defer'
            opts_html.append(
                f'<label class="opt defer" for="{did}">'
                f'<input type="{"radio" if kind == "single" else "checkbox"}" id="{did}" '
                f'name="answer" value="__defer__">'
                f'<span class="otext"><span class="olabel">Not deciding this yet</span>'
                f'<div class="oconseq">Recorded as put off. Everything below stays where it is.</div>'
                f'</span></label>'
            )
            legend = ("Pick one" if kind == "single" else "Pick any that apply")
            if policy == "none":
                legend += " — nothing is pre-selected, this one is yours"
            elif policy == "forced":
                legend += " — this cannot be left open"
            body = (f'<fieldset><legend>{esc(legend)}</legend>{"".join(opts_html)}</fieldset>'
                    f'<label class="nolabel" for="n-{esc(q["id"])}">Anything that changes the answer '
                    f'(optional)</label>'
                    f'<textarea id="n-{esc(q["id"])}" name="note" '
                    f'placeholder="{esc(q.get("note_hint") or "Conditions, exceptions, or a different framing.")}">'
                    f'</textarea>'
                    f'<label class="qual" hidden><input type="checkbox" name="qualifies" checked>'
                    f'<span>This note limits or changes the option above — do not act on the answer alone.</span>'
                    f'</label>')

        rel = q.get("unblocks") or []
        rel_html = ""
        if rel:
            lis = []
            for u in rel:
                it = item_by_id.get(u.get("item"))
                if not it:
                    continue
                lis.append(f'<li><a href="#i-{esc(it["id"])}">{esc(it.get("title") or it["id"])}</a> — '
                           f'{esc(EFFECT_WORD.get(u.get("effect"), u.get("effect")))}</li>')
            rel_html = f'<div class="rel"><b>Answering this</b><ul>{"".join(lis)}</ul></div>'

        # A question may name the record it came from. The link is the point:
        # the page carries the decision, the record carries the history behind it,
        # and asking a reader to search a tracker for the card is how a page of
        # fifty decisions stops being answerable in one sitting.
        card = q.get("card") or {}
        card_html = ""
        if card.get("url"):
            card_html = (f'<a class="qcard" href="{esc(card["url"])}" target="_blank" '
                         f'rel="noopener">{esc(card.get("key") or "Open the record")} \u2197</a>')

        q_html.append(
            f'<section class="q" id="q-{esc(q["id"])}" data-q="{esc(q["id"])}" '
            f'data-kind="{esc(kind)}" data-policy="{esc(policy)}">'
            f'<div class="qhead"><h3>{esc(q["title"])}</h3>{card_html}'
            f'<span class="qn">{n} of {len(questions)}</span></div>'
            f'<p class="why">{rich(q["why"])}</p>'
            f'<form name="q-{esc(q["id"])}" onsubmit="return false">{body}</form>{rel_html}</section>'
        )

    # ---- print-only decision summary ---------------------------------------
    sum_lis = []
    for q in questions:
        rec = next((o for o in q.get("options", []) if o.get("recommended")), None)
        shown = rec["label"] if rec and q.get("default_policy", "recommended") == "recommended" \
            else "nothing pre-selected"
        sum_lis.append(f'<li><b>{esc(q["title"])}</b> — as printed: {esc(shown)}. '
                       f'Answer: ______________________</li>')
    summary = ('<section class="summary"><h2>Decisions, for marking up on paper</h2>'
               '<p class="note">Printed copies carry no answers. Whatever is written here has to be '
               'typed back into the page before it can be exported or acted on.</p>'
               f'<ol>{"".join(sum_lis)}</ol></section>')

    contract = ""
    if meta.get("completionContract"):
        unk = ""
        if meta.get("unknowns"):
            lis = "".join(f"<li>{rich(u)}</li>" for u in meta["unknowns"])
            unk = f'<p style="margin:.6rem 0 0"><b>What I could not check from here:</b></p><ul>{lis}</ul>'
        contract = (f'<div class="contract"><b>Counted as done when:</b> {rich(meta["completionContract"])}{unk}</div>')

    methods = ""
    if meta.get("methods"):
        methods = (f'<hr class="rule"><h2 id="how">How this was put together</h2>'
                   f'<p class="note">{rich(meta["methods"])}</p>')

    bar = ('<div class="bar" role="status">'
           '<span class="tally" id="tally"></span>'
           '<button type="button" id="export">Download answers (JSON)</button>'
           '<button type="button" class="ghost" id="print">Print</button>'
           '<span class="warn">Answers live in this browser only. Nothing is sent anywhere, and '
           'closing the tab without downloading loses them.</span></div>')

    model_js = json.dumps({
        "slug": meta["slug"], "project": meta["project"], "generatedAt": meta["generatedAt"],
        "questions": [{"id": q["id"], "title": q["title"], "kind": q["kind"],
                       "default_policy": q.get("default_policy", "recommended" if q["kind"] != "text" else "none"),
                       "options": q.get("options", []), "unblocks": q.get("unblocks", []),
                       "card": q.get("card")}
                      for q in questions],
    })

    # The reader's own eyes, not the machine's guess. Following the operating
    # system is the default because that is usually right, but a page somebody
    # reads for half an hour in a bright room is exactly where the guess is
    # wrong, and a page that cannot be changed is one they stop reading.
    #
    # Applied in the head, before first paint: set from the body and the reader
    # watches the page change colour under them on every load.
    theme_script = (
        "(function(){try{var t=localStorage.getItem('wl:%s:theme');"
        "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}"
        "catch(e){}})();" % meta["slug"]
    )
    themer = ('<div class="themer" role="group" aria-label="Colour scheme">'
              '<button type="button" data-theme-set="system" aria-pressed="true">System</button>'
              '<button type="button" data-theme-set="light" aria-pressed="false">Light</button>'
              '<button type="button" data-theme-set="dark" aria-pressed="false">Dark</button>'
              '</div>')

    page = TEMPLATE.format(
        themescript=theme_script,
        themer=themer,
        title=esc(meta["title"]),
        css=CSS % theme,
        js=JS.replace("__MODEL__", model_js),
        eyebrow=esc(meta.get("eyebrow") or f'{meta["project"]} · private'),
        standfirst=rich(meta["standfirst"]),
        meta=esc(meta.get("lead") or f'{meta["generatedAt"]} · for {meta.get("audience", "you")} · '
                                     f'not published anywhere'),
        contract=contract, top=top_html,
        items_note=rich(meta.get("items_note") or
                        "Every item says what stage it actually reached. Built is not deployed, and "
                        "deployed is not accepted."),
        groups="".join(groups_html),
        q_note=rich(meta.get("q_note") or
                    "Where a suggestion is pre-selected, it is a suggestion until you click it. "
                    "Anything you never touch exports as unconfirmed."),
        questions="".join(q_html), summary=summary, methods=methods, bar=bar,
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    for w in warnings:
        print(f"warn  {w}")
    print(f"wrote {out} — {len(items)} items, {len(questions)} questions, {len(warnings)} warning(s)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("model_dir")
    ap.add_argument("--out", required=True)
    ap.add_argument("--theme")
    a = ap.parse_args()
    return build(pathlib.Path(a.model_dir), pathlib.Path(a.out),
                 pathlib.Path(a.theme) if a.theme else None)


if __name__ == "__main__":
    sys.exit(main())
