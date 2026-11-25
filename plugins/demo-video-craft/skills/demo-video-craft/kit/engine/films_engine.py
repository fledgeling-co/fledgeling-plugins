"""The film table's machinery: step helpers, the overview's opening and end slide, the pace function, the final hold,
the length gate, and the writer that turns a table of films into HyperFrames projects.

    from films_engine import *          # in the series' films.py
    FILMS = {'O': {'scenes': [...], 'voice': [[line, scene, offset]], 'lockbar': False}, 'K01': {...}}
    write_series(FILMS, SERIES, states.S)

Picture first: every scene has its own length and every step is in scene seconds. Narration is placed afterwards at
[line id, scene id, offset] and never moves the picture, so the muted master and the voiced cut are one render.

A window scene is a step list run by kit.js K.play over a state from states.py; a stage scene (the opener, the
architecture, the end slide) is components on the ground run by kit3.js K3.stage. Step grammar:

  [t, 'frame', target, fill, dur]     the camera frames a rect at `fill` of the stage width (0.62 a chat pair, 0.7 a
                                      card, 0.9 the composer), capped at 0.92 of its height and 3.2x zoom
  [t, 'arrive', '#w1', i | [i..], {gap, y, dur}]   thread items blur in (8 px, 16 px rise, 0.6 s expo.out)
  [t, 'type', '#w1', text, end] / [t, 'send', '#w1']   via ask(); a prompt present at t=0 is set whole (pre=True)
  [t, 'click', target, {lead}]        the cursor glides in an arc (0.6-0.65 s lead) and presses, with a ring
  [t, 'tool', {i, w}, [status..], dur]   a running tool line narrates in the present tense, then finishes
  [t, 'ink', target, 'ok'|'bad'|'review', dur, name] / [t, 'inkTo', name, 'ok']   the evidence marks
  [t, 'wheel', target, index] / [t, 'unwheel', target]   focus one row, the rest recede; always release
  [t, 'scroll', '#w1', item, dur] · [t, 'panel'|'unpanel', '#w1', dur] · [t, 'count', target, dur] ·
  [t, 'stream', {i, w}, dur] · [t, 'drag', {from, to, file}, dur] · [t, 'swap', a, b] · [t, 'label', html, [x, y], until]
  [0, 'enter', {from}] · [t, 'exit', {to}]   scenes arrive and leave through blur, never a hard cut
Stage steps: 'in', 'out', 'to', 'moveTo', 'grow', 'link', 'flow', 'wheel', 'cur', 'press', 'type' (kit3.js).
"""
import json
import shutil
from html.parser import HTMLParser
from pathlib import Path

LOCK = 3.2                    # the lockup bar holds over the last 3.2 s of a short
LBL = [40, 30]                # identity labels: top left, clear of the composer band
LABELS = True                 # the label switch: series.json "labels"; False drops every label from every film
CPS = 52                      # typing speed; then a 0.6 s hold so the prompt can be read
COMP = {'s': '.cf-composer', 'w': '#w1', 'p': [18, 14]}                    # the composer, measured where it sits
COMP_OPEN = {'s': '.cf-composer', 'w': '#w1', 'p': [18, 14], 'open': True}
DROP = [440, 500, 792, 400]   # the composer and the room above it, for a file carried in


# ---- targets ------------------------------------------------------------------------------------------------------
def ch(i, w='#w1', p=None, open=False):
    """Thread item(s) i (an index or a list) in window w, padded by p."""
    t = {'i': i, 'w': w}
    if p is not None:
        t['p'] = p
    if open:
        t['open'] = True
    return t


def el(s, w='#w1', i=None, t=None, p=None, open=False):
    """The first element matching selector s (inside thread item i, containing text t)."""
    o = {'s': s, 'w': w}
    if i is not None:
        o['in'] = i
    if t:
        o['t'] = t
    if p is not None:
        o['p'] = p
    if open:
        o['open'] = True
    return o


def u(*ts, p=None, open=False):
    """The union of several targets."""
    o = {'u': list(ts)}
    if p is not None:
        o['p'] = p
    if open:
        o['open'] = True
    return o


def btn(i, text, w='#w1', open=False):
    return el('.dc-btn', w, i=i, t=text, open=open)


def ask(t, text, w='#w1', hold=0.6, open=False, pre=False):
    """Type the request at CPS (or have it written already when the scene opens: pre), hold so it can be read while the
    cursor reaches send, press send. Returns (steps, time the reply can start)."""
    done = t if pre else round(t + len(text) / CPS, 2)
    sent = round(done + (1.0 if pre else hold) + 0.05, 2)
    return [[t, 'type', w, text, done], [sent, 'click', el('.cf-composer .send', w, open=open), {'lead': 0.6}], [sent + 0.05, 'send', w]], sent + 0.05


def type_in(t, target, text, hold=0.6, pre=False):
    """Type into a field of the product's own interface at CPS, then hold so it can be read; pre=True writes it whole
    at t. Returns (steps, time the next step can start)."""
    done = t if pre else round(t + len(text) / CPS, 2)
    return [[t, 'typein', target, text, done]], round(done + (1.0 if pre else hold), 2)


def run(i, msgs, dur, w='#w1'):
    """Arguments for a 'tool' step: the tool line at item i narrates msgs over dur seconds."""
    return {'i': i, 'w': w}, msgs, dur


# ---- effects follow the picture -----------------------------------------------------------------------------------
class _Kids(HTMLParser):
    VOID = {'br', 'img', 'input', 'hr', 'meta', 'link', 'wbr'}

    def __init__(self):
        super().__init__()
        self.depth, self.col, self.kids = 0, None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get('class') or '').split()
        if self.col is None and ('cf-col' in cls or 'data-items' in a):   # a chat thread, or the product's own list
            self.col = self.depth
        elif isinstance(self.col, int) and self.depth == self.col + 1:
            self.kids.append('card' if tag == 'article' or 'k-art' in cls else tag + '.' + '.'.join(cls))
        if tag not in self.VOID:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag not in self.VOID:
            self.depth -= 1
        if isinstance(self.col, int) and self.depth == self.col:
            self.col = 'done'


def kinds(html):
    p = _Kids()
    p.feed(html)
    return p.kids


def sounds(sc, S):
    """Pops when a card or artifact lands, clicks on presses, a whoosh when a file is carried in, a chime on a fix."""
    ks = {w: kinds(S[st]) for w, st in sc['windows']}
    out = list(sc.get('sfx', []))
    for st in sc['spec']['steps']:
        t, op = st[0], st[1]
        if op == 'click':
            out.append([t, 'click'])
        elif op == 'arrive':
            w = st[2].lstrip('#')
            ids = st[3] if isinstance(st[3], list) else [st[3]]
            gap = st[4].get('gap', 0.3) if len(st) > 4 and isinstance(st[4], dict) else 0.3
            for k, i in enumerate(ids):
                if i >= len(ks[w]):
                    raise SystemExit(f"{sc['id']}: arrive {i} in {w}, but its state has {len(ks[w])} thread items")
                if ks[w][i] == 'card':
                    out.append([round(t + k * gap, 2), 'pop'])
        elif op == 'drag':
            out.append([t, 'whoosh'])
        elif op == 'inkTo':
            out.append([t, 'chime'])
    return out


# ---- scenes -------------------------------------------------------------------------------------------------------
def win(sid, state, dur, start, steps, hidden=0, label=None, css='', sfx=(), size=None, phone=False, **kw):
    """A window scene: one host window holding `state`, its thread items from `hidden` on hidden until they arrive,
    the camera starting at `start` ({'frame': target, 'fill': f} or {'orient': 1.12})."""
    spec = {'windows': ['#w1'], 'hidden': {'#w1': hidden}, 'start': start, 'steps': steps}
    if size:                                   # a window that is not the 1440 x 900 host: a phone is (430, 932)
        kw['size'] = list(size)
    if phone:
        kw['phone'] = True
    if label and LABELS:
        spec['steps'] = [[0.05, 'label', label[0], LBL, label[1]]] + spec['steps']
    return {'id': sid, 'kind': 'win', 'dur': dur, 'windows': [['w1', state]], 'css': css, 'spec': spec, 'sfx': list(sfx), **kw}


def C(cid, html, x=960, y=540, w=None, shown=False, cls=''):
    """A stage component centred at (x, y); shown=True means on screen from frame 0."""
    width = f'width:{w}px' if w else ''
    return (f'<div class="k3{" k3-shown" if shown else ""} {cls}" id="{cid}" style="left:{x}px;top:{y}px">'
            f'<div class="k3z" style="{width}">{html}</div></div>')


def chip(name, mark, cid, cls='k3-hide'):
    """A host-app chip: mark is a sprite symbol name ('claude') or a swatch colour ('#1F3FA6')."""
    m = f'<svg class="lg" aria-hidden="true"><use href="#i-{mark}"/></svg>' if not mark.startswith('#') else f'<i style="background:{mark}"></i>'
    return f'<span class="k3-app big {cls}" id="{cid}">{m}{name}</span>'


def intro_scene(lock, headline, apps, sources, head_left, head_right, node_caption, portrait=False):
    """The overview's opening, 11.5 scene seconds (before the intro pace of 1.15): the lockup above the complete
    headline from frame 0 with a row of host chips under it; the headline leaves, the lockup travels into the
    architecture's centre node and the chips travel to their ports; the sources arrive and wire into the node, the
    node wires to the hosts, dots flow; a focus walks down the sources and the node pulses so the stage never holds
    still; the first chip pushes forward and fills the frame into the first window scene.

    lock: lockup HTML. headline: HTML with one <span class="acc">accent</span> word. apps: [(name, mark)] for chip().
    sources: [(icon, label)], five of them. head_left / head_right: the column headings. portrait=True lays the same
    grammar out for a 1080 x 1920 canvas: the sources above, the node in the middle, the hosts in a row below, joined
    by one trunk and a fan of wires running down."""
    if portrait:
        return _intro_portrait(lock, headline, apps, sources, head_left, head_right, node_caption)
    n = len(apps)
    html = [
        C('lk0', f'<div class="k3-lock0">{lock}</div>', y=196, shown=True),
        C('t0', f'<div class="k3-title">{headline}</div>', y=400, w=1560, shown=True),
        C('chips', '<div style="display:flex;gap:22px">' + ''.join(chip(nm, mk, f'ch{k + 1}') for k, (nm, mk) in enumerate(apps)) + '</div>', y=622, shown=True),
        C('hs', f'<div class="k3-head">{head_left}</div>', x=330, y=268),
        C('srcs', '<div class="k3-col r">' + ''.join(f'<span class="k3-src k3-hide" id="s{k + 1}"><svg aria-hidden="true"><use href="#i-{i}"/></svg>{t}</span>'
                                                    for k, (i, t) in enumerate(sources)) + '</div>', x=330, y=580, shown=True),
        # the node's own lockup is the traveller's twin: hidden until the traveller lands on it, then the two swap in
        # one frame, so two copies never overlap on screen
        C('node', '<div class="k3-node" id="nd">' + lock.replace('class="k-lock"', 'class="k-lock" style="opacity:0"', 1)
          + f'<small>{node_caption}</small></div>', x=960, y=580),
        C('ht', f'<div class="k3-head">{head_right}</div>', x=1590, y=388),
        C('tools', '<div class="k3-col l">' + ''.join(chip(nm, mk, f'p{k + 1}', 'k3-ph') for k, (nm, mk) in enumerate(apps)) + '</div>', x=1590, y=580, shown=True),
    ]
    ns = len(sources)
    steps = [
        *[[round(0.25 + 0.13 * k, 2), 'in', f'#ch{k + 1}', {'y': 14, 'dur': 0.5}] for k in range(n)],
        [3.65, 'out', '#t0', {'dur': 0.35}],
        [3.7, 'moveTo', '#lk0 .k-lock', {'to': '#nd .k-lock', 'dur': 0.75}],
        [4.45, 'show', '#nd .k-lock'], [4.45, 'to', '#lk0', {'opacity': 0, 'dur': 0.01}],
        *[[round(3.8 + 0.06 * k, 2), 'moveTo', f'#ch{k + 1}', {'to': f'#p{k + 1}', 'dur': 0.8}] for k in range(n)],
        [4.05, 'in', '#hs', {'y': 8, 'dur': 0.5}],
        *[[round(4.1 + 0.14 * k, 2), 'in', f'#s{k + 1}', {'x': -30, 'y': 0, 'blur': 8, 'dur': 0.55}] for k in range(ns)],
        [4.4, 'in', '#node', {'y': 0, 'scale': 0.9, 'dur': 0.6}], [4.65, 'in', '#ht', {'y': 8, 'dur': 0.5}],
        *[[round(4.85 + 0.07 * k, 2), 'link', f'#s{k + 1}', '#nd', {'name': f'a{k + 1}', 'dur': 0.5}] for k in range(ns)],
        *[[round(5.3 + 0.07 * k, 2), 'link', '#nd', f'#p{k + 1}', {'name': f'b{k + 1}', 'dur': 0.45}] for k in range(n)],
        [5.5, 'flow', [f'a{k + 1}' for k in range(ns)], {'dur': 5.3, 'travel': 0.8, 'every': 0.55, 'stagger': 0.11}],
        [6.0, 'flow', [f'b{k + 1}' for k in range(n)], {'dur': 4.8, 'travel': 0.7, 'every': 0.55, 'stagger': 0.12}],
        *[[round(5.65 + 0.8 * k, 2), 'wheel', '#srcs .k3-src', k, {'dur': 0.4}] for k in range(ns)], [9.85, 'unwheel', '#srcs .k3-src'],
        [6.3, 'to', '#nd', {'scale': 1.04, 'dur': 0.35, 'ease': 'power2.out'}], [6.7, 'to', '#nd', {'scale': 1, 'dur': 0.4}],
        [10.05, 'to', '#ch1', {'scale': 1.12, 'dur': 0.45, 'ease': 'power2.out'}],
        *[[10.05, 'to', f'#ch{k + 1}', {'opacity': 0.35, 'dur': 0.4}] for k in range(1, n)],
        [10.85, 'to', '#ch1', {'scale': 7, 'opacity': 0, 'filter': 'blur(8px)', 'dur': 0.6, 'ease': 'power3.in'}],
        *[[10.85, 'out', s, {'dur': 0.4}] for s in ('#srcs', '#node', '#hs', '#ht', *[f'#ch{k + 1}' for k in range(1, n)], '.k3-wires')],
    ]
    sfx = [[round(0.25 + 0.13 * k, 2), 'pop'] for k in range(n)] + [[3.8, 'whoosh'], [4.4, 'pop'], [10.85, 'whoosh']]
    return {'id': 'intro', 'kind': 'stage', 'dur': 11.5, 'html': html, 'steps': steps, 'sfx': sfx}


def _intro_portrait(lock, headline, apps, sources, head_left, head_right, node_caption):
    n, ns = len(apps), len(sources)
    html = [
        C('lk0', f'<div class="k3-lock0" style="font-size:46px">{lock}</div>', x=468, y=420, shown=True),
        C('t0', f'<div class="k3-title" style="font-size:60px">{headline}</div>', x=468, y=700, w=640, shown=True),
        C('chips', '<div class="k3-col c" style="gap:18px">' + ''.join(chip(nm, mk, f'ch{k + 1}') for k, (nm, mk) in enumerate(apps)) + '</div>', x=468, y=1080, shown=True),
        C('hs', f'<div class="k3-head">{head_left}</div>', x=468, y=330),
        C('srcs', '<div class="k3-col c" style="gap:22px">' + ''.join(f'<span class="k3-src k3-hide" id="s{k + 1}"><svg aria-hidden="true"><use href="#i-{i}"/></svg>{t}</span>'
                                                    for k, (i, t) in enumerate(sources)) + '</div>', x=468, y=600, shown=True),
        C('node', '<div class="k3-node" id="nd">' + lock.replace('class="k-lock"', 'class="k-lock" style="opacity:0"', 1)
          + f'<small>{node_caption}</small></div>', x=468, y=960),
        C('ht', f'<div class="k3-head">{head_right}</div>', x=468, y=1110),
        C('tools', '<div class="k3-row small">' + ''.join(chip(nm, mk, f'p{k + 1}', 'k3-ph') for k, (nm, mk) in enumerate(apps)) + '</div>', x=468, y=1195, shown=True),
    ]
    steps = [
        *[[round(0.25 + 0.13 * k, 2), 'in', f'#ch{k + 1}', {'y': 14, 'dur': 0.5}] for k in range(n)],
        [3.65, 'out', '#t0', {'dur': 0.35}],
        [3.7, 'moveTo', '#lk0 .k-lock', {'to': '#nd .k-lock', 'dur': 0.75}],
        [4.45, 'show', '#nd .k-lock'], [4.45, 'to', '#lk0', {'opacity': 0, 'dur': 0.01}],
        *[[round(3.8 + 0.06 * k, 2), 'moveTo', f'#ch{k + 1}', {'to': f'#p{k + 1}', 'dur': 0.8}] for k in range(n)],
        [4.05, 'in', '#hs', {'y': 8, 'dur': 0.5}],
        *[[round(4.1 + 0.14 * k, 2), 'in', f'#s{k + 1}', {'y': 14, 'blur': 8, 'dur': 0.55}] for k in range(ns)],
        [4.4, 'in', '#node', {'y': 0, 'scale': 0.9, 'dur': 0.6}], [4.65, 'in', '#ht', {'y': 8, 'dur': 0.5}],
        [4.95, 'link', '#srcs', '#nd', {'name': 'a1', 'dur': 0.5, 'dir': 'down'}],
        *[[round(5.3 + 0.07 * k, 2), 'link', '#nd', f'#p{k + 1}', {'name': f'b{k + 1}', 'dur': 0.45, 'dir': 'down'}] for k in range(n)],
        [5.5, 'flow', ['a1'], {'dur': 5.3, 'travel': 0.8, 'every': 0.3}],
        [6.0, 'flow', [f'b{k + 1}' for k in range(n)], {'dur': 4.8, 'travel': 0.7, 'every': 0.55, 'stagger': 0.12}],
        *[[round(5.65 + 0.8 * k, 2), 'wheel', '#srcs .k3-src', k, {'dur': 0.4}] for k in range(ns)], [9.85, 'unwheel', '#srcs .k3-src'],
        [6.3, 'to', '#nd', {'scale': 1.04, 'dur': 0.35, 'ease': 'power2.out'}], [6.7, 'to', '#nd', {'scale': 1, 'dur': 0.4}],
        [10.05, 'to', '#ch1', {'scale': 1.12, 'dur': 0.45, 'ease': 'power2.out'}],
        *[[10.05, 'to', f'#ch{k + 1}', {'opacity': 0.35, 'dur': 0.4}] for k in range(1, n)],
        [10.85, 'to', '#ch1', {'scale': 7, 'opacity': 0, 'filter': 'blur(8px)', 'dur': 0.6, 'ease': 'power3.in'}],
        *[[10.85, 'out', s, {'dur': 0.4}] for s in ('#srcs', '#node', '#hs', '#ht', *[f'#ch{k + 1}' for k in range(1, n)], '.k3-wires')],
    ]
    sfx = [[round(0.25 + 0.13 * k, 2), 'pop'] for k in range(n)] + [[3.8, 'whoosh'], [4.4, 'pop'], [10.85, 'whoosh']]
    return {'id': 'intro', 'kind': 'stage', 'dur': 11.5, 'html': html, 'steps': steps, 'sfx': sfx}


def outro_scene(lock, headline, cta, url, portrait=False):
    """The overview's end slide, 4.4 scene seconds: the lockup at y 330, the opening headline again at y 540, the ask
    at y 760 ("Book a demo" as a button, the URL beside it), each arriving in turn. Give the scene before it an exit."""
    ask = ('<div style="display:flex;align-items:center;gap:30px">'
           f'<span style="font:600 36px/1 Inter,sans-serif;color:#fff;background:var(--g-accent);border-radius:12px;padding:20px 30px">{cta}</span>'
           f'<span style="font:500 36px/1 Inter,sans-serif;color:var(--g-navy)">{url}</span></div>')
    if portrait:
        html = [C('lo', f'<div class="k3-lock0" style="font-size:46px">{lock}</div>', x=468, y=440),
                C('lt', f'<div class="k3-title" style="font-size:60px">{headline}</div>', x=468, y=720, w=640), C('lc', ask.replace('36px', '28px'), x=468, y=1060)]
    else:
        html = [C('lo', f'<div class="k3-lock0">{lock}</div>', y=330), C('lt', f'<div class="k3-title">{headline}</div>', y=540, w=1560),
                C('lc', ask, y=760)]
    steps = [[0.2, 'in', '#lo', {'y': 12, 'dur': 0.6}], [0.55, 'in', '#lt', {'y': 16, 'dur': 0.65}], [1.05, 'in', '#lc', {'y': 12, 'dur': 0.55}]]
    return {'id': 'outro', 'kind': 'stage', 'dur': 4.4, 'html': html, 'steps': steps, 'sfx': [[0.2, 'pop']]}


# ---- pace: one factor slows a whole film by dwelling, not by moving through syrup ----------------------------------
# Where each op keeps its own duration, so per-op motion can be capped separately from the timing between steps.
DUR_AT = {'frame': 4, 'orient': 3, 'tool': 4, 'scroll': 4, 'stream': 3, 'drag': 3, 'count': 3, 'panel': 3, 'unpanel': 3}


def pace(sc, k):
    """Step times, scene length and effects scale by k; per-op durations by min(k, 1.25); entrances, exits and travel
    by min(k, 1.2); typing end, label holds and flows by k."""
    for st in sc['spec']['steps'] if sc['kind'] == 'win' else sc['steps']:
        if isinstance(st[0], (int, float)):
            st[0] = round(st[0] * k, 2)
        op = st[1]
        i = DUR_AT.get(op)
        if i is not None and len(st) > i and isinstance(st[i], (int, float)):
            st[i] = round(st[i] * min(k, 1.25), 2)
        if op == 'type' and len(st) > 4 and isinstance(st[4], (int, float)):
            st[4] = round(st[4] * k, 2)
        if op == 'label' and len(st) > 4 and isinstance(st[4], (int, float)):
            st[4] = round(st[4] * k, 2)
        if op in ('in', 'out', 'grow', 'moveTo', 'to') and len(st) > 3 and isinstance(st[3], dict) and 'dur' in st[3]:
            st[3]['dur'] = round(st[3]['dur'] * min(k, 1.2), 2)
        if op == 'link' and len(st) > 4 and isinstance(st[4], dict) and 'dur' in st[4]:
            st[4]['dur'] = round(st[4]['dur'] * min(k, 1.2), 2)
        if op == 'flow' and isinstance(st[3], dict):
            st[3]['dur'] = round(st[3]['dur'] * k, 2)
    sc['dur'] = round(sc['dur'] * k, 1)
    sc['sfx'] = [[round(t * k, 2), kind] for t, kind in sc.get('sfx', [])]


def apply_labels(films):
    """Drop every 'label' step when the switch is off, including labels written straight into a step list."""
    if LABELS:
        return
    for f in films.values():
        for sc in f['scenes']:
            steps = sc['spec']['steps'] if sc['kind'] == 'win' else sc['steps']
            steps[:] = [s for s in steps if s[1] != 'label']


def apply_pace(films, overview, factors, intro=1.15):
    """factors: {'overview': 1.3, 'short': 1.22}. The intro takes its own factor. Voice offsets move with their scene."""
    for fid, f in films.items():
        for sc in f['scenes']:
            k = intro if sc['id'] == 'intro' else factors['overview' if fid == overview else 'short']
            pace(sc, k)
            f['voice'] = [[lid, sid, round(off * k, 2)] if sid == sc['id'] else [lid, sid, off] for lid, sid, off in f['voice']]


def settle_push(sc, lockbar):
    """A short's final result holds with a slow push-in rather than a still frame: from max(last frame + 1.4,
    end - 4.6) to the end + 0.6 s, at the last frame's fill x 1.07 (at most 0.97), end being before the lockup bar."""
    steps = sc['spec']['steps']
    frames = [st for st in steps if st[1] == 'frame' and isinstance(st[0], (int, float))]
    if not frames:
        return
    last = max(frames, key=lambda st: st[0])
    end = sc['dur'] - (LOCK if lockbar else 0.0)
    t = round(max(last[0] + 1.4, end - 4.6), 2)
    steps.append([t, 'frame', last[2], round(min(0.97, last[3] * 1.07), 3), round(end - t + 0.6, 2)] + ([last[5]] if len(last) > 5 else []))


# ---- writing the projects -----------------------------------------------------------------------------------------
def _spec_json(spec):
    """A step list one step to a line, so a composition stays short enough to read and diff."""
    head = {k: v for k, v in spec.items() if k != 'steps'}
    body = ',\n   '.join(json.dumps(s, ensure_ascii=False) for s in spec['steps'])
    lead = json.dumps(head, ensure_ascii=False)[:-1] + (', ' if head else '')
    return lead + '"steps": [\n   ' + body + '\n  ]}'


def window_html(sc, W=1920, H=1080):
    sid = sc['id']
    ww, wh = sc.get('size', [1440, 900])
    dims = f'width:{ww}px;height:{wh}px;' if sc.get('size') else ''
    cls = 'k-win phone' if sc.get('phone') else 'k-win'
    wins = ''.join(f'<div class="{cls}" id="{sid}-{w}" style="{dims}{sc.get("pos", {}).get(w, "")}"><!--state:{st}--><!--/state:{st}--></div>'
                   for w, st in sc['windows'])
    spec = _spec_json(sc['spec'])
    for w, _ in sc['windows']:
        spec = spec.replace(f'"#{w}"', f'"#{sid}-{w}"')
    return f'''<template id="{sid}-template">
  <div id="{sid}root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    <style>
      #{sid}root .k-cam {{ position: absolute; left: 0; top: 0; width: {ww}px; height: {wh}px; transform-origin: 0 0; }}
      #{sid}root .k-cam > .k-win {{ transform: none; }}
      {sc.get("css", "")}
    </style>
    <div class="k-sc"><div class="k-cam">{wins}</div></div>
    <script>
      K.play('{sid}', {spec});
    </script>
  </div>
</template>
'''


def stage_html(sc, W=1920, H=1080):
    sid = sc['id']
    spec = _spec_json({'steps': sc['steps']})
    return f'''<template id="{sid}-template">
  <div id="{sid}root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    <div class="k-sc">{''.join(sc['html'])}</div>
    <script>
      K3.stage('{sid}', {spec});
    </script>
  </div>
</template>
'''


HYPERFRAMES_JSON = {'$schema': 'https://hyperframes.heygen.com/schema/hyperframes.json',
                    'registry': 'https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry',
                    'paths': {'blocks': 'compositions', 'components': 'compositions/components', 'assets': 'assets'},
                    'media': {'autoProxy': True}}


def write_series(films, series_dir, S):
    """Write films/<id>/ for every film: plan.json (scene lengths, effect beats, voice placements), steps.json (each
    scene's steps, for sync_table.py), the compositions, and the HyperFrames project files. Fails before writing
    anything when a film's length or a scene's length is outside series.json's 'lengths', or a state is missing."""
    series = Path(series_dir)
    cfg = json.loads((series / 'series.json').read_text())
    lengths, overview = cfg['lengths'], cfg['overview']
    if (lengths['overview'], lengths['short']) != ([80, 110], [20, 25]):
        if not lengths.get('why'):
            raise SystemExit('series.json lengths differ from the binding 80-110 s overview and 20-25 s shorts; give "why"')
        print(f'lengths differ from the binding numbers: {lengths["why"]}')
    problems = []
    for fid, f in films.items():
        total = round(sum(sc['dur'] for sc in f['scenes']), 2)
        lo, hi = lengths['overview' if fid == overview else 'short']
        if not lo <= total <= hi:
            problems.append(f'{fid}: {total} s, outside {lo}-{hi} s')
        for sc in f['scenes']:
            if sc['dur'] > lengths['scene_max']:
                problems.append(f'{fid}/{sc["id"]}: {sc["dur"]} s, over the {lengths["scene_max"]} s scene cap')
            for _, st in sc.get('windows', []):
                if st not in S:
                    problems.append(f'{fid}/{sc["id"]}: no state {st!r} in states.py')
        print(f'{fid:5} {total:6.1f} s  ' + '  '.join(f'{sc["id"]} {sc["dur"]}' for sc in f['scenes']))
    if problems:
        raise SystemExit('the film table does not hold:\n  ' + '\n  '.join(problems))
    for fid, f in films.items():
        F = series / 'films' / fid
        if (F / 'compositions').exists():
            shutil.rmtree(F / 'compositions')
        (F / 'compositions').mkdir(parents=True)
        (F / 'hyperframes.json').write_text(json.dumps(HYPERFRAMES_JSON, indent=2))
        (F / 'package.json').write_text(json.dumps({'name': f'{fid.lower()}-film', 'private': True, 'type': 'module'}, indent=2))
        (F / 'meta.json').write_text(json.dumps({'id': fid, 'name': f'{cfg["title_prefix"]} · {f["title"]}'}, indent=2))
        size = f.get('size') or cfg.get('size') or [1920, 1080]
        plan_scenes, steps = [], {}
        for sc in f['scenes']:
            (F / 'compositions' / f'{sc["id"]}.html').write_text(stage_html(sc, *size) if sc['kind'] == 'stage' else window_html(sc, *size))
            sfx = sc['sfx'] if sc['kind'] == 'stage' else sounds(sc, S)
            plan_scenes.append({'id': sc['id'], 'src': f'{sc["id"]}.html', 'dur': sc['dur'], 'sfx': sorted(sfx)})
            steps[sc['id']] = [s for s in (sc['spec']['steps'] if sc['kind'] == 'win' else sc['steps']) if isinstance(s[0], (int, float))]
        plan = {'fps': 60, 'title': f['title'], 'tempo': f.get('tempo', 1.0), 'lock': LOCK, 'lockbar': f.get('lockbar', True),
                'captions': f.get('captions', False), 'limit': f.get('limit'), 'size': size, 'scenes': plan_scenes, 'voice': f['voice']}
        (F / 'plan.json').write_text(json.dumps(plan, indent=1, ensure_ascii=False))
        (F / 'steps.json').write_text(json.dumps(steps, ensure_ascii=False))
    print(len(films), 'films written to', series / 'films')
