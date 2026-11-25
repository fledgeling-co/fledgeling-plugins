"""The screen builder: host-app windows (a Claude-like and a ChatGPT-like frame) holding the product's cards, tool
lines and side-panel views, as live HTML the films push into and the runtime animates.

    import states_engine as E
    E.configure(product='Acme Record', who={'dana': ('DR', 'Dana Ruiz', 'Advisor · Enterprise plan')})
    S = {'ask': E.frame('claude', 'dana', 'Q3 deck check', [E.user('…'), E.tool('check_figures', done=False), …])}
    E.write(S, series_dir, banned=['Old Company', 'OLDT'])

Every state is a string of HTML. `write` puts each in states/<id>.html, writes states/index.html (every state on one
page, to look at before any scene is built), and fails when a state carries a banned name, so a retired scenario
cannot survive in a corner of one screen. The markup and class names (.dc-*, .pv-*, .cf-*) are the ones the runtime
and the example product's CSS expect; when you port your own product's kit, keep the .cf-* host frame and change the
card builders to emit your product's markup.
"""
import re
from pathlib import Path

PRODUCT = {'name': 'Acme Record'}
WHO = {}
HOST_MARKS = False
MODEL = 'Opus 5.5'

NAV = {
    'claude': [('plus', 'New chat'), ('search', 'Search'), ('chat', 'Chats', 1), ('folder', 'Projects'), ('grid', 'Artifacts'), ('clock', 'Scheduled')],
    'chatgpt': [('plus', 'New chat'), ('search', 'Search chats'), ('grid', 'Library'), ('folder', 'Projects'), ('clock', 'Tasks')],
}
HOST_WORD = {'claude': 'Claude', 'chatgpt': 'ChatGPT'}
COMPOSER = {'claude': 'Reply to Claude', 'chatgpt': 'Ask anything'}


def register_host(app, word, nav, composer):
    """Add a chat host beside Claude and ChatGPT: its name in the sidebar, its nav rows [(icon, label[, 'on'])] and its
    composer's placeholder. Give it tokens in theme.css: .k-cf[data-app=\"<app>\"] { --c-bg; --c-side; --c-rule; --c-ink;
    --c-muted; --c-bubble; --c-send }, and its mark as marks/<app>.svg when the series uses host marks. A host that is not
    a chat (an inbox, a spreadsheet, a team chat with channels) is drawn as app() with its own markup instead."""
    HOST_WORD[app], NAV[app], COMPOSER[app] = word, nav, composer


def configure(product, who, host_marks=False, model='Opus 5.5'):
    """product: the name the host shows on tool lines and the panel. who: {key: (initials, name, plan)}, the person
    signed in to each window, by role ('Investor relations', 'CFO · Enterprise'): company plus role overflowed the
    sidebar by 83 px in the source run. host_marks: True when the series' marks/ holds claude.svg and chatgpt.svg."""
    PRODUCT['name'] = product
    WHO.clear()
    WHO.update(who)
    global HOST_MARKS, MODEL
    HOST_MARKS, MODEL = host_marks, model


def ic(i, cls=''):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{i}"/></svg>'


def mark():
    # The product's badge on cards and tool lines sits on its navy square, so it uses the mark drawn for a dark ground
    # (marks/mark-on-dark.svg; the sprite falls back to mark.svg). The symbol's own viewBox scales it.
    return '<i><svg aria-hidden="true"><use href="#i-mark-on-dark"/></svg></i>'


def badge(b):
    return f'<span class="badge {b[1] if len(b) > 1 else ""}">{b[0]}</span>' if b else ''


def row(r):
    """A card row: {t, d, k ('ok'|'warn'|'bad'|'info'), ic, b (badge), side, id, hide}. Text sits in .tx spans so a
    mark is drawn to the words, not to the row."""
    icon = r.get('ic') or {'ok': 'ok', 'warn': 'warn', 'bad': 'shield', 'info': 'doc'}.get(r.get('k'), 'doc')
    side = badge(r['b']) if r.get('b') else r.get('side', '')
    d = f'<span class="d"><span class="tx">{r["d"]}</span></span>' if r.get('d') else ''
    hid = ' dc-hidden' if r.get('hide') else ''
    rid = f' id="{r["id"]}"' if r.get('id') else ''
    return f'<li class="dc-row {r.get("k", "")}{hid}"{rid}>{ic(icon)}<span class="t"><span class="tx">{r["t"]}</span></span><span class="side">{side}</span>{d}</li>'


def lead(cells, track=None):
    """The figures a card leads with: [(label, value, class, id)]. Class 'ok' inks the value green, so use it only for
    'matches its source'; a checked figure that is bad news for the company takes 'chk' (neutral ink)."""
    cs = ''.join(f'<div><small>{c[0]}</small><b class="{c[2] if len(c) > 2 else ""}"{(" id=" + chr(34) + c[3] + chr(34)) if len(c) > 3 else ""}>{c[1]}</b></div>'
                 for c in cells)
    tr = f'<div class="dc-track"><span style="width:{track}%"></span></div>' if track is not None else ''
    return f'<div class="dc-lead">{cs}{tr}</div>'


def card(o):
    """The product's card: {id, origin, oic, title, tier, tk, sub, lead, quote, rows, acts: [{label, ic, sec}], reason,
    extra}. A card leads with its answer: the title says what was found ('11 of 12 figures match the record')."""
    head = ''
    if o.get('origin'):
        head += f'<div class="dc-origin">{ic(o.get("oic", "clock"))}<span>{o["origin"]}</span></div>'
    head += (f'<div class="dc-head"><div class="dc-title"><span class="tx">{o["title"]}</span></div><span class="dc-tier {o.get("tk", "")}">{o["tier"]}</span>'
             f'<div class="dc-sub"><span class="tx">{o["sub"]}</span></div></div>')
    body = o.get('lead', '') + (f'<div class="dc-quote">{o["quote"]}</div>' if o.get('quote') else '')
    if o.get('rows'):
        body += f'<ul class="dc-rows">{"".join(row(r) for r in o["rows"])}</ul>'
    hidden = sum(1 for r in o.get('rows', []) if r.get('hide'))
    if hidden:
        body += f'<span class="dc-more">Show {hidden} more</span>'
    if o.get('acts'):
        bs = ''.join(f'<span class="dc-btn{" pri" if i == 0 and not a.get("sec") else ""}">{ic(a["ic"]) if a.get("ic") else ""}{a["label"]}</span>'
                     for i, a in enumerate(o['acts']))
        body += f'<div class="dc-acts">{bs}</div>'
    if o.get('reason'):
        body += f'<p class="dc-reason">{o["reason"]}</p>'
    cid = f' id="{o["id"]}"' if o.get('id') else ''
    return f'<article class="dc"{cid}>{head}{body}{o.get("extra", "")}</article>'


def user(text, file=None, sub='Document'):
    """The person's message. One sentence of 6-14 words; a file carried in shows as a chip above it."""
    f = f'<div class="cf-file">{ic("doc")}<span><b>{file}</b><br>{sub}</span></div>' if file else ''
    return f'<div class="cf-user">{f}{text}</div>'


def tool(name, done=True, run=None):
    """A tool line, named with the product's real tool name (grep it from the product's own source). done=False draws
    it running, with `run` as its present-tense status; the 'tool' step narrates and finishes it."""
    p = PRODUCT['name']
    run = run or f'Using {p}: {name}'
    return (f'<div class="cf-tool{" done" if done else ""}" data-done="Used {p}: {name}"><span class="spin"></span>'
            f'{ic("ok", "tick")}<span class="tl">{"Used " + p + ": " + name if done else run}</span></div>')


def by():
    return f'<div class="cf-by">{mark()}{PRODUCT["name"]}</div>'


def say(text):
    return f'<div class="cf-say"><p>{text}</p></div>'


def box(h, side, inner):
    return f'<section class="pv-box"><header>{h}<span>{side or ""}</span></header>{inner}</section>'


def prow(t, d=None, side='', pid=None):
    i = f' id="{pid}"' if pid else ''
    dd = f'<span class="d"><span class="tx">{d}</span></span>' if d else ''
    return f'<div class="pv-row"{i}><span class="t"><span class="tx">{t}</span></span><span class="side"><span class="tx">{side}</span></span>{dd}</div>'


def frame(app, who, title, items, recents=(), panel=None, ptitle='', composer=None, model=None):
    """A whole assistant window: sidebar, conversation (items, in order: the build hides and arrives them by index),
    composer, and a closed side panel holding the product's view (the 'panel' step opens it)."""
    word = HOST_WORD[app]
    wm = (ic(app, 'lg') if HOST_MARKS else '') + word
    nav = ''.join(f'<div class="cf-nav{" on" if len(n) > 2 else ""}">{ic(n[0])}{n[1]}</div>' for n in NAV[app])
    rec = ''.join(f'<div class="cf-chat{" on" if i == 0 else ""}">{r}</div>' for i, r in enumerate([title, *recents]))
    av, name, plan = WHO[who]
    ph = composer or COMPOSER[app]
    model = MODEL if model is None else model
    mdl = f'<span class="model">{model}</span>' if app == 'claude' and model else ''
    pb = (f'<section class="cf-panel"><div class="cf-pin"><div class="cf-ph">{mark()}<b>{PRODUCT["name"]}</b><span>{ptitle}</span>'
          f'<span class="cf-x">{ic("x")}</span></div><div class="cf-pbody">{panel}</div></div></section>') if panel else ''
    return (f'<div class="cf k-cf" data-app="{app}"><aside class="cf-side"><div class="cf-word">{wm}</div>{nav}'
            f'<div class="cf-rec">Recents</div>{rec}<div class="cf-me"><span class="cf-av">{av}</span><span>{name}<small>{plan}</small></span></div></aside>'
            f'<div class="cf-main"><div class="cf-top"><span>{title}</span><span>Share</span></div><div class="cf-convo"><div class="cf-col">{"".join(items)}</div></div>'
            f'<div class="cf-composer"><div class="ph">{ph}</div><div class="row"><span class="plus">{ic("plus")}</span>'
            f'<span class="chip">{ic("plug")}{PRODUCT["name"]}</span>{mdl}<span class="send">{ic("up")}</span></div></div></div>{pb}</div>')


def app(body, kind='browser', url=None, title=None):
    """The product's own interface in a window, for a product that is not shown inside a chat host. kind: 'browser'
    (tab dots and the product's URL), 'desktop' (a title bar), or 'phone' (a phone body: give the scene
    win(..., size=(430, 932))). body is the product's own screen markup: mark the list whose children arrive by index
    with data-items and its scrolling region with data-viewport, and give fields the steps type into an id."""
    if kind == 'phone':
        bar = ''
    elif kind == 'browser':
        bar = (f'<div class="k-app-bar"><span class="dots"><i></i><i></i><i></i></span>'
               f'<span class="url">{ic("lock")}{url or ""}</span></div>')
    else:
        bar = f'<div class="k-app-bar"><span class="dots"><i></i><i></i><i></i></span><span class="title">{title or PRODUCT["name"]}</span></div>'
    return f'<div class="k-app" data-kind="{kind}">{bar}<div class="k-app-body">{body}</div></div>'


def solo(app, c, label):
    """One card alone on the ground, labelled with the assistant it came from."""
    m = ic(app, 'lg') if HOST_MARKS else ''
    return f'<div class="k-solo"><div class="k-solo-app">{m}{label}</div>{by()}{c}</div>'


def lockup(wordmark, product, cls='k-lock', dark=False):
    """The brand lockup: mark, wordmark, hairline, product name. Styled by the series' lockup.css alone, sized by one
    font-size, so the pages and every placement in the films read one spec."""
    m = 'mark-on-dark' if dark else 'mark'
    return (f'<div class="{cls}{" on-dark" if dark else ""}"><svg class="mk" aria-hidden="true"><use href="#i-{m}"/></svg>'
            f'<span class="wm">{wordmark}</span><span class="sep"></span><span class="pn">{product}</span></div>')


def sprite(runtime_dir, marks_dir, need=()):
    """The icon sprite: the kit's generic symbols plus one symbol per marks/<name>.svg (the product mark as mark.svg,
    host marks as claude.svg and chatgpt.svg, a client's mark as <client>.svg). Fails on a missing required mark."""
    base = (Path(runtime_dir) / 'icons.svg.txt').read_text()
    extra = []
    for f in sorted(Path(marks_dir).glob('*.svg')):
        s = f.read_text()
        vb = re.search(r'viewBox="([^"]+)"', s)
        inner = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S)
        if not vb or not inner:
            raise SystemExit(f'{f}: needs a viewBox and an <svg> root')
        extra.append(f'    <symbol id="i-{f.stem}" viewBox="{vb.group(1)}">{inner.group(1).strip()}</symbol>')
    have = {f.stem for f in Path(marks_dir).glob('*.svg')}
    if 'mark' in have and 'mark-on-dark' not in have:      # one mark serves both grounds unless the series draws two
        src = (Path(marks_dir) / 'mark.svg').read_text()
        extra.append(f'    <symbol id="i-mark-on-dark" viewBox="{re.search(r"viewBox=.([^\"]+)", src).group(1)}">'
                     f'{re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1).strip()}</symbol>')
    missing = [n for n in need if n not in have]
    if missing:
        raise SystemExit(f'{marks_dir}: missing {", ".join(m + ".svg" for m in missing)}')
    return base.replace('  <defs>', '  <defs>\n' + '\n'.join(extra), 1)


def assert_clean(S, banned, substrings=()):
    """Fail when any state carries a banned word or name (case-insensitive, whole word). Use it for every retired
    name, ticker, person, counterparty and period label when a series switches scenario."""
    hits = []
    for sid, html in S.items():
        text = re.sub(r'<[^>]+>', ' ', html)
        for b in banned:
            if re.search(rf'(?<![\w]){re.escape(b)}(?![\w])', text, re.I):
                hits.append(f'{sid}: {b}')
        for b in substrings:                          # spelling stems such as 'colour' or 'organis'
            if b.lower() in text.lower():
                hits.append(f'{sid}: {b}')
    if hits:
        raise SystemExit('banned names on screen:\n  ' + '\n  '.join(hits))


def write(S, series_dir, banned=(), substrings=()):
    series = Path(series_dir)
    assert_clean(S, banned, substrings)
    out = series / 'states'
    out.mkdir(exist_ok=True)
    for sid, html in S.items():
        (out / f'{sid}.html').write_text(html)
    import json
    cfg = json.loads((series / 'series.json').read_text())
    icons = sprite(series / '_kit' / 'runtime', series / 'marks', ['mark'] + (['claude', 'chatgpt'] if cfg.get('host_marks') else []))
    faces = ''.join(f'@font-face {{ font-family: "{fam}"; src: url("../assets/fonts/{file}") format("woff2"); font-weight: 100 900; }}'
                    for fam, file in (('Inter', 'Inter.woff2'), ('Inter Tight', 'InterTight.woff2')))
    cells = ''.join(f'<section><h2>{sid}</h2><div class="k-win" style="position:relative">{html}</div></section>' for sid, html in S.items())
    (out / 'index.html').write_text(
        '<!doctype html><html lang="en-US"><meta charset="utf-8"><title>States</title>'
        '<link rel="stylesheet" href="../_kit/runtime/frame.css"><link rel="stylesheet" href="../_kit/runtime/kit.css">'
        f'<link rel="stylesheet" href="../lockup.css"><style>{faces} body{{background:#F6F7F9;margin:24px;font:14px Inter}}'
        'section{margin:0 0 40px}h2{font:600 15px Inter;margin:0 0 8px}.k-cf .cf-col > *{opacity:1}</style>'
        f'<body>{icons}{cells}</body></html>')
    return out
