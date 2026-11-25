#!/usr/bin/env python3
"""The example series' film table: an overview (the opening and architecture, one workflow, the end slide) and one
short, both built picture first. Replace the workflows with your series'; keep the shape.

    python3 films.py                                   # writes films/<id>/ for every film, after the length gate
    MOTION_CRAFT_SCRIPTS=... python3 _kit/engine/build.py . O --mute-only

Each short runs one workflow straight into the product and ends on its result: to lengthen one, take the workflow a
step further (save the result, open the product's view of it), never hold longer. Voice placements are
[line id, scene id, offset]: start each line on the frame it describes.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '_kit' / 'engine'))
import states  # noqa: E402
import states_engine as E  # noqa: E402
from films_engine import (COMP, apply_pace, ask, btn, ch, el, intro_scene, outro_scene, run, settle_push, u, win,  # noqa: E402
                          write_series)

CFG = json.loads((HERE / 'series.json').read_text())
LOCKUP = E.lockup(CFG['lockup']['wordmark'], CFG['lockup']['product'])
HEADLINE = 'Bring your company <span class="acc">record</span><br>into the AI tools you already use.'
APPS = [('Claude', '#D97757'), ('ChatGPT', '#0D0D0D'), ('Your workspace', '#1F3FA6')]   # with host_marks: ('Claude', 'claude')
SOURCES = [('doc', 'SEC filings'), ('chart', 'Earnings releases'), ('grid', 'Prior decks'), ('users', 'Holder records'),
           ('shield', 'Disclosure rules')]


def check_steps(t0=0.4, pre=False):
    """Ask, the tool narrates, the card lands, the bad figure is marked against its source, one press fixes it."""
    p, s = ask(t0, 'Check our Q3 deck against the filed release.', pre=pre)
    return [
        *p,
        [s, 'arrive', '#w1', 0], [s, 'frame', u(ch(0), ch(1)), 0.62, 0.7],
        [s + 0.25, 'arrive', '#w1', 1], [s + 0.25, 'tool', *run(1, ['Reading the Q3 release…', 'Checking each figure on slide 7…'], 1.0)],
        [s + 1.25, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [s + 1.25, 'frame', ch(3, p=16), 0.7, 0.8],
        [s + 1.95, 'wheel', el('.dc-row', i=3), 1], [s + 2.05, 'ink', el('#r-gm .t .tx'), 'bad', 0.45, 'gm'],
        [s + 2.7, 'ink', el('.dc-quote .q', i=3), 'review', 0.5], [s + 3.5, 'unwheel', el('.dc-row', i=3)],
        [s + 3.7, 'click', btn(3, 'Use 41.2%'), {'lead': 0.65}], [s + 3.8, 'inkTo', 'gm', 'ok'],
        [s + 4.0, 'scroll', '#w1', 4, 0.7], [s + 4.0, 'arrive', '#w1', 4], [s + 4.05, 'frame', ch(4, p=18), 0.7, 0.8],
        [s + 4.9, 'ink', el('.dc-lead b.ok', i=4), 'ok', 0.4],
    ], s


# ==== O: the overview ===============================================================================================
_check, _s = check_steps()
O = [
    intro_scene(LOCKUP, HEADLINE, APPS, SOURCES, 'Your company’s record', 'The AI tools you already use',
                'One record, checked against its sources'),
    win('check', 'check', 9.0, {'frame': COMP, 'fill': 0.9},
        [[0, 'enter', {'from': 'push', 'dur': 0.55}], *_check, [8.7, 'exit', {'to': 'left'}]], hidden=0),
    outro_scene(LOCKUP, HEADLINE, CFG['cta'], CFG['url']),
]
FILMS = {'O': {'title': 'Your company record, in the AI tools you already use', 'scenes': O, 'lockbar': False,
               'voice': [['v1', 'intro', 0.05], ['v2', 'intro', 4.25], ['v3', 'check', round(_s, 2)]]}}


# ==== K01: one workflow, one step further, ending on its result ======================================================
def k01():
    st, s = check_steps(0, pre=True)
    st += [[s + 5.9, 'click', btn(4, 'Save to Acme Record'), {'lead': 0.65}],
           [s + 6.2, 'scroll', '#w1', 6, 0.8], [s + 6.2, 'arrive', '#w1', 5], [s + 6.25, 'frame', ch(5, p=40), 0.6, 0.7],
           [s + 6.2, 'tool', *run(5, ['Saving the deck to Acme Record…'], 0.9)],
           [s + 7.2, 'arrive', '#w1', 6], [s + 7.2, 'frame', ch(6, p=18), 0.7, 0.8],
           [s + 8.0, 'ink', el('#s-ok .t .tx'), 'ok', 0.45]]
    return win('clip', 'check', 16.6, {'frame': COMP, 'fill': 0.9}, st, sfx=[[s + 3.8, 'chime']])


FILMS['K01'] = {'title': 'The figure that didn’t match', 'scenes': [k01()], 'voice': [['q1', 'clip', 0.6]]}

# ---- pace, then the final hold, then the projects ------------------------------------------------------------------
P = CFG['pace']
apply_pace(FILMS, CFG['overview'], {'overview': P['overview'], 'short': P['short']}, intro=P['intro'])
for fid, f in FILMS.items():
    last = f['scenes'][-1]
    if last['kind'] == 'win':
        settle_push(last, f.get('lockbar', True))

if __name__ == '__main__':
    write_series(FILMS, HERE, states.S)
