#!/usr/bin/env python3
"""The reference series' film table: the Diolog Guardian launch series of 25 Nov 2026 (an overview of 1:41 and nine
shorts of 21-25 s), ported onto the kit with every scene's steps as they were published. Only the machinery is the
kit's: the opening and the end slide (intro_scene, outro_scene), the pace function, the settling push and the writer.

    python3 films.py        # writes films/<id>/ after the length gate; then _kit/engine/render.py . for all ten

Picture first. Every film works on mute, so each scene has its own length and every step is in scene seconds; the
narration is placed afterwards at an offset into a scene and never moves a picture. The overview opens on its full line
with the three assistants under it, turns into the architecture (the record flowing through Diolog Guardian into the
AI tools), and the Claude chip opens into Claude, where seven workflows run. Shorts K02 to K10 run one workflow each.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '_kit' / 'engine'))
import states as S  # noqa: E402
import states_engine as E  # noqa: E402
from films_engine import (COMP, COMP_OPEN, DROP, LBL, apply_pace, ask, btn, ch, el, intro_scene, outro_scene, run,  # noqa: E402,F401
                          settle_push, u, win, write_series)

CFG = json.loads((HERE / 'series.json').read_text())
import films_engine as FE  # noqa: E402
FE.LABELS = CFG.get('labels', True)          # the label switch, read before any scene is built
LOCKUP = E.lockup(CFG['lockup']['wordmark'], CFG['lockup']['product'])
HEADLINE = 'Bring your company <span class="acc">intelligence</span><br>into the AI tools you already use.'
APPS = [('Claude', 'claude'), ('ChatGPT', 'chatgpt'), ('Your enterprise workspace', '#1F3FA6')]
SOURCES = [('doc', 'SEC filings'), ('chart', 'Earnings materials'), ('grid', 'Prior decks'), ('users', 'Investor records'),
           ('shield', 'SEC guidance and exchange rules')]
TITLES = {
 "O": "Bring your company intelligence into the AI tools you already use",
 "K02": "Your post-earnings brief, ready",
 "K03": "Investor questions, answered from the record",
 "K04": "Two assistants, one record",
 "K05": "The figure that didn’t match",
 "K06": "Analyst Q&A, prepared",
 "K07": "A new document, in the record",
 "K08": "Last quarter’s deck, this quarter’s figures",
 "K09": "Holders, checked against the newest filings",
 "K10": "Investor calls, filed and recalled"
}


def deck_roll(at, i):
    """Q1's figures roll to Q2's and the slide becomes this quarter's (lululemon's Q1 and Q2 2026 releases)."""
    st = [[at, 'text', el('#jq'), 'Q2 2026 at a glance'], [at, 'text', el('.k-art-h b', i=i), 'lululemon Q2 2026 earnings'],
          [at, 'text', el('.jfoot'), 'Figures from lululemon’s Q2 2026 earnings release, linked by Diolog']]
    for k, (sel, d) in enumerate({'#k-rev': '−4% vs Q2 2025', '#k-comp': 'Americas −12%', '#k-gm': '+200 bps', '#k-om': '−190 bps'}.items()):
        st += [[round(at + 0.12 * k, 2), 'count', el(sel), 1.0], [round(at + 0.12 * k, 2), 'text', el(sel + ' + em'), d]]
    return st


def deck_scene(sid, enter=True):
    p, s = ask(0.9, 'Build our Q2 earnings deck the way we did Q1.')
    steps = ([[0, 'enter', {'from': 'push', 'dur': 0.55}]] if enter else []) + [
        [0.4, 'frame', COMP, 0.9, 0.6], *p,
        [s, 'arrive', '#w1', 0], [s, 'frame', u(ch(0), ch(1)), 0.62, 0.7],
        [s + 0.25, 'arrive', '#w1', 1], [s + 0.25, 'tool', *run(1, ['Reading lululemon’s record…', 'Finding the Q2 materials…'], 0.8)],
        [s + 1.0, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [s + 1.0, 'frame', ch(3, p=16), 0.7, 0.8],
        [s + 1.55, 'wheel', el('.dc-row', i=3), 3], [s + 1.65, 'ink', el('#r-q2deck .t .tx'), 'review', 0.45],
        [s + 2.5, 'scroll', '#w1', 6, 0.9], [s + 2.5, 'arrive', '#w1', [4, 5], {'gap': 0.15}], [s + 2.6, 'stream', {'i': 5, 'w': '#w1'}, 0.7],
        [s + 2.8, 'arrive', '#w1', 6, {'y': 24, 'dur': 0.7}], [s + 2.8, 'frame', el('.jslide', i=6, p=10), 0.76, 0.9],
        *deck_roll(round(s + 3.6, 2), 6),
        [s + 5.9, 'scroll', '#w1', 9, 0.8], [s + 5.9, 'arrive', '#w1', [7, 8, 9], {'gap': 0.12}],
        [s + 6.1, 'frame', u(el('#fc-row'), el('.dc-quote', i=9), p=14), 0.7, 0.8],
        [s + 6.55, 'ink', el('#fc-row .t .tx'), 'bad', 0.45, 'fc'], [s + 6.85, 'ink', el('#fc-quote'), 'review', 0.5],
        [s + 7.6, 'click', btn(9, 'Use 18.8%'), {'lead': 0.65}], [s + 7.7, 'inkTo', 'fc', 'ok'],
        [s + 7.9, 'scroll', '#w1', 11, 0.7], [s + 7.9, 'arrive', '#w1', [10, 11], {'gap': 0.12}], [s + 7.95, 'frame', ch(11, p=18), 0.7, 0.8],
    ]
    return steps, s


def newdoc_steps(t0=0.25):
    return [
        [t0, 'drag', {'from': [960, 560], 'to': el('.cf-composer'), 'file': 'Q2 2026 earnings release, draft.docx'}, 1.1],
        [t0 + 1.2, 'arrive', '#w1', 0], [t0 + 1.2, 'frame', u(ch(0), ch(1)), 0.62, 0.7],
        [t0 + 1.45, 'arrive', '#w1', 1], [t0 + 1.45, 'tool', *run(1, ['Adding it to lululemon’s record…'], 0.8)],
        [t0 + 2.25, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [t0 + 2.25, 'frame', ch(3, p=16), 0.7, 0.8],
        [t0 + 3.05, 'ink', el('#f-doc .badge'), 'review', 0.3], [t0 + 3.45, 'ink', el('#f-when .d .tx'), 'ok', 0.4],
    ]


def qa_steps(t0=0.35, open_pack=False, pre=False):
    p, s = ask(t0, 'Draft the analyst Q&A pack for lululemon’s Q2 call.', pre=pre)
    st = [*p, [s, 'arrive', '#w1', 0], [s, 'frame', u(ch(0), ch(1)), 0.62, 0.7],
          [s + 0.25, 'arrive', '#w1', 1], [s + 0.25, 'tool', *run(1, ['Reading the filings and past releases…', 'Answering from published material…'], 1.0)],
          [s + 1.25, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [s + 1.25, 'frame', ch(3, p=16), 0.7, 0.8],
          [s + 1.95, 'wheel', el('.dc-row', i=3), 0], [s + 2.05, 'ink', el('.dc-row .d .tx', i=3), 'ok', 0.45],
          [s + 2.6, 'wheel', el('.dc-row', i=3), 1], [s + 3.0, 'ink', el('.dc-lead b.ok', i=3), 'ok', 0.4]]
    if open_pack:
        st += [[s + 4.0, 'click', btn(3, 'Open the pack'), {'lead': 0.65}],
               [s + 4.25, 'scroll', '#w1', 4, 0.8], [s + 4.25, 'arrive', '#w1', 4, {'y': 24, 'dur': 0.7}], [s + 4.3, 'frame', ch(4, p=14), 0.68, 0.9],
               [s + 5.2, 'ink', el('.jsrc', i=4), 'ok', 0.5]]
    return st


def own_steps(t0=0.2):
    return [
        [t0, 'arrive', '#w1', 0], [t0 + 0.4, 'frame', u(ch(0), ch(2)), 0.64, 0.8], [t0 + 0.4, 'arrive', '#w1', 1],
        [t0 + 0.4, 'tool', *run(1, ['Reading the newest 13G filings…', 'Checking each holder…'], 1.2)], [t0 + 1.6, 'arrive', '#w1', 2],
        [t0 + 1.9, 'scroll', '#w1', 4, 0.8], [t0 + 1.9, 'arrive', '#w1', [3, 4], {'gap': 0.12}], [t0 + 2.0, 'frame', ch(4, p=16), 0.7, 0.8],
        [t0 + 2.7, 'wheel', el('.dc-row', i=4), 0], [t0 + 2.8, 'ink', el('#o-r1 .d .tx'), 'review', 0.45],
        [t0 + 3.4, 'wheel', el('.dc-row', i=4), 1], [t0 + 3.5, 'ink', el('#o-r2 .d .tx'), 'review', 0.45],
        [t0 + 4.4, 'click', btn(4, 'Update the 2 lines'), {'lead': 0.65}],
        [t0 + 4.65, 'scroll', '#w1', 6, 0.7], [t0 + 4.65, 'arrive', '#w1', [5, 6], {'gap': 0.12}], [t0 + 4.7, 'frame', ch(6, p=18), 0.7, 0.8],
    ]


def inbox_steps(t0=0.0):
    p, s = ask(t0 + 4.4, 'Draft our answer on the outlook from the Q2 and Q1 releases.', open=True)
    return [
        [t0 + 0.6, 'ink', el('#q-theme .t .tx'), 'review', 0.45],
        [t0 + 1.6, 'click', btn(3, 'Open questions'), {'lead': 0.65}], [t0 + 1.7, 'panel', '#w1', 0.5],
        [t0 + 1.75, 'frame', el('.pv', p=10, open=True), 0.66, 0.8],
        [t0 + 2.4, 'wheel', el('.pv-row', open=True), 0], [t0 + 2.9, 'wheel', el('.pv-row', open=True), 1], [t0 + 3.4, 'wheel', el('.pv-row', open=True), 2],
        [t0 + 3.9, 'unwheel', el('.pv-row', open=True)], [t0 + 3.9, 'frame', COMP_OPEN, 0.9, 0.7], *p,
        [s, 'scroll', '#w1', 7, 0.8], [s, 'arrive', '#w1', [4, 5], {'gap': 0.2}], [s, 'frame', u(ch(4, open=True), ch(5, open=True), p=30), 0.6, 0.7],
        [s + 0.2, 'tool', *run(5, ['Reading the Q2 and Q1 releases…'], 0.9)],
        [s + 1.1, 'arrive', '#w1', [6, 7], {'gap': 0.12}], [s + 1.1, 'frame', ch(7, p=14, open=True), 0.7, 0.8],
        [s + 1.75, 'ink', el('#a-s1 .t .tx'), 'ok', 0.35], [s + 2.0, 'ink', el('#a-s2 .t .tx'), 'ok', 0.35],
        [s + 2.75, 'click', btn(7, 'Save to Diolog for review', open=True), {'lead': 0.65}],
        [s + 3.0, 'fade', el('#qv-draft', open=True), 1, 0.35], [s + 3.0, 'frame', el('#qv-draft', p=16, open=True), 0.7, 0.8],
        [s + 3.55, 'ink', el('#qv-row .t .tx'), 'ok', 0.45],
    ]


def calls_steps(t0=0.2, label_until=9.6):
    p, s = ask(t0 + 4.25, 'What did they ask on their last call?')
    return [
        [t0, 'drag', {'from': [960, 560], 'to': el('.cf-composer'), 'file': 'Holder call, Sep 10.txt'}, 1.05],
        [t0 + 1.15, 'arrive', '#w1', 0], [t0 + 1.15, 'frame', u(ch(0), ch(1)), 0.62, 0.7],
        [t0 + 1.4, 'arrive', '#w1', 1], [t0 + 1.4, 'tool', *run(1, ['Matching the investors on the call…', 'Pulling out each question…'], 0.9)],
        [t0 + 2.3, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [t0 + 2.3, 'frame', ch(3, p=16), 0.7, 0.8],
        [t0 + 3.0, 'wheel', el('.dc-row', i=3), 1],
        [t0 + 3.75, 'frame', COMP, 0.9, 0.7], *p,
        [s, 'scroll', '#w1', 7, 0.8], [s, 'arrive', '#w1', [4, 5], {'gap': 0.2}], [s, 'frame', u(ch(4), ch(5), p=30), 0.6, 0.7],
        [s + 0.2, 'tool', *run(5, ['Searching lululemon’s record…'], 0.7)],
        [s + 0.9, 'arrive', '#w1', [6, 7], {'gap': 0.12}], [s + 0.9, 'frame', ch(7, p=16), 0.7, 0.8],
        [s + 1.85, 'click', btn(7, 'Open in the calls view'), {'lead': 0.65}], [s + 1.95, 'panel', '#w1', 0.5],
        [s + 2.0, 'frame', el('.pv', p=10, open=True), 0.66, 0.8],
        [s + 2.55, 'wheel', el('.pv-row', open=True), 0], [s + 2.6, 'ink', el('#cv-1 .side .tx'), 'ok', 0.3],
        [s + 3.05, 'wheel', el('.pv-row', open=True), 1], [s + 3.1, 'ink', el('#cv-2 .side .tx'), 'ok', 0.3],
        [s + 3.9, 'unwheel', el('.pv-row', open=True)],
    ]


def brief_steps(t0=0.0, slow=1.0):
    k = lambda x: round(t0 + x * slow, 2)   # noqa: E731
    return [
        [k(0.15), 'stream', {'i': 2, 'w': '#w1'}, 1.2], [k(0.7), 'ink', el('.dc-title .tx', i=1), 'review', 0.45],
        [k(2.0), 'click', btn(1, 'Do it'), {'lead': 0.65}],
        [k(2.25), 'scroll', '#w1', 5, 0.9], [k(2.25), 'arrive', '#w1', 3], [k(2.3), 'frame', ch(3, p=40), 0.6, 0.7],
        [k(2.25), 'tool', *run(3, ['Reading the Q2 release…', 'Comparing with guidance…', 'Linking each figure to its source…'], 1.5)],
        [k(3.75), 'arrive', '#w1', [4, 5], {'gap': 0.12}], [k(3.75), 'frame', ch(5, p=16), 0.7, 0.8],
        [k(4.5), 'frame', u(el('.dc-lead', i=5), el('#b-r2'), p=14), 0.74, 0.9],
        [k(5.1), 'ink', el('.dc-lead b.chk', i=5), 'ok', 0.4], [k(5.3), 'wheel', el('.dc-row', i=5), 1], [k(6.5), 'unwheel', el('.dc-row', i=5)],
    ]


# ==== O: the overview =============================================================================================
_ds, _ = deck_scene('deck')
O = [
    intro_scene(LOCKUP, HEADLINE, APPS, SOURCES, S.ic('lulu', 'lg') + 'lululemon’s record',
                'The AI tools you already use', 'One record, checked against its sources'),
    win('deck', 'r3-deck', 12.0, {'orient': 1.12}, _ds + [[11.7, 'exit', {'to': 'left'}]]),
    win('newdoc', 'r3-newdoc', 6.3, {'frame': DROP, 'fill': 0.86}, [[0, 'enter', {'from': 'right'}], *newdoc_steps(), [5.95, 'exit', {}]]),
    win('qa', 'r3-qa', 6.5, {'frame': COMP, 'fill': 0.9}, [[0, 'enter', {}], *qa_steps(), [6.15, 'exit', {'to': 'left'}]]),
    win('own', 'r3-own', 6.85, {'frame': ch(0, p=24), 'fill': 0.42}, [[0, 'enter', {'from': 'right'}], *own_steps(), [6.5, 'exit', {}]],
        sfx=[[4.85, 'chime']]),
    win('inbox', 'r3-inbox', 11.5, {'frame': ch(3, p=16), 'fill': 0.66}, [[0, 'enter', {}], *inbox_steps(), [11.2, 'exit', {'to': 'left'}]],
        hidden=4, css='#inbox-w1 #qv-draft { opacity: 0; }'),
    win('calls', 'r3-calls', 10.5, {'frame': DROP, 'fill': 0.86}, [[0, 'enter', {'from': 'right'}], *calls_steps(label_until=10.0), [10.2, 'exit', {}]]),
    win('brief', 'r3-brief', 9.4, {'frame': ch([1, 2], p=24), 'fill': 0.7}, [[0, 'enter', {}], *brief_steps(), [9.05, 'exit', {'to': 'left'}]], hidden=3),
    outro_scene(LOCKUP, HEADLINE, CFG['cta'], CFG['url']),
]
# Each line starts on its beat (owner, 25 Nov: the narration didn't line up with the picture): the deck line as the
# deck lands, the inbox line once the questions are open so its 'draft' meets the prompt, the calls line once the
# call is filed so its 'recall' meets the recall.
O_VOICE = [['v1', 'intro', 0.05], ['v2', 'intro', 4.25], ['v3', 'deck', 3.4], ['v4', 'newdoc', 0.35], ['v5', 'qa', 0.6],
           ['v6', 'own', 0.7], ['v7', 'inbox', 2.6], ['v8', 'calls', 3.55], ['v9', 'brief', 0.4]]

FILMS = {'O': {'title': TITLES['O'], 'scenes': O, 'voice': O_VOICE, 'tempo': 1.0, 'lockbar': False}}   # no closing bar on the overview


# ==== the clips: one workflow each, straight into the product, ending on the result ===============================
# Round 3b (owner, 25 Nov): 20 to 24 s each, so each workflow goes one step further; no on-screen labels.
def k02():
    st = [st for st in brief_steps(0.3) if st[1] != 'unwheel'] + [
        [7.0, 'wheel', el('.dc-row', i=5), 3], [7.1, 'ink', el('.dc-row .d .tx', i=5, t='10-Q'), 'ok', 0.45], [8.1, 'unwheel', el('.dc-row', i=5)],
        [8.2, 'frame', u(el('.dc-lead', i=5), btn(5, 'Start the Q&A pack'), p=16), 0.62, 0.8],
        [9.3, 'click', btn(5, 'Start the Q&A pack'), {'lead': 0.65}],
        [9.6, 'scroll', '#w1', 8, 0.9], [9.6, 'arrive', '#w1', 6], [9.65, 'frame', ch(6, p=40), 0.6, 0.7],
        [9.6, 'tool', *run(6, ['Drafting the Q&A pack from the brief…', 'Answering each question from the record…'], 1.4)],
        [11.0, 'arrive', '#w1', [7, 8], {'gap': 0.12}], [11.0, 'frame', ch(8, p=16), 0.7, 0.8],
        [11.9, 'wheel', el('.dc-row', i=8), 0], [12.0, 'ink', el('.dc-row .d .tx', i=8), 'ok', 0.4],
        [12.8, 'wheel', el('.dc-row', i=8), 1], [13.6, 'wheel', el('.dc-row', i=8), 2], [14.5, 'unwheel', el('.dc-row', i=8)],
        [14.6, 'ink', el('.dc-lead b.ok', i=8), 'ok', 0.4]]
    return win('clip', 'r3-k2', 20.4, {'frame': ch([1, 2], p=24), 'fill': 0.7}, st, hidden=3, sfx=[[12.0, 'chime']])


def k03():
    p, s0 = ask(0, 'What’s waiting in lululemon’s inbox?', pre=True)
    st = [*p, [s0, 'arrive', '#w1', 0], [s0, 'frame', u(ch(0), ch(1), p=30), 0.6, 0.7],
          [s0 + 0.25, 'arrive', '#w1', 1], [s0 + 0.25, 'tool', *run(1, ['Counting what’s waiting…'], 0.7)],
          [s0 + 0.95, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [s0 + 0.95, 'frame', ch(3, p=16), 0.66, 0.8],
          *inbox_steps(round(s0 + 1.25, 2))]
    t = st[-1][0] + 0.9
    st += [[t, 'frame', el('.pv', p=10, open=True), 0.62, 0.8],
           [t + 0.7, 'wheel', el('.pv-row', open=True), 0], [t + 1.3, 'wheel', el('.pv-row', open=True), 1], [t + 1.9, 'wheel', el('.pv-row', open=True), 2],
           [t + 2.6, 'unwheel', el('.pv-row', open=True)], [t + 2.7, 'frame', el('#qv-draft', p=16, open=True), 0.7, 0.8]]
    return win('clip', 'r3-inbox', round(t + 7.4, 1), {'frame': COMP, 'fill': 0.9}, st, css='#clip-w1 #qv-draft { opacity: 0; }')


def k04():
    p, s = ask(3.1, 'Draft the Q&A answer on the revised outlook for lululemon’s IR team.')
    st = [[0.05, 'label', S.ic('claude', 'lg') + '<b>Dana Ruiz</b> · advisor, in Claude', [40, 96], 2.9],
          [0.05, 'label', S.ic('chatgpt', 'lg') + '<b>Your client’s IR team</b> · in ChatGPT', [990, 96], 2.9],
          [2.5, 'frame', COMP, 0.9, 0.8], *p,
          [s, 'arrive', '#w1', 0], [s, 'frame', u(ch(0), ch(1)), 0.62, 0.7],
          [s + 0.25, 'arrive', '#w1', 1], [s + 0.25, 'tool', *run(1, ['Reading the Q2 release…', 'Drafting from what lululemon has published…'], 1.0)],
          [s + 1.25, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [s + 1.25, 'frame', ch(3, p=16), 0.7, 0.8],
          [s + 1.9, 'ink', el('#qa-a-src .t .tx'), 'ok', 0.4], [s + 2.3, 'ink', el('.dc-quote', i=3), 'review', 0.5],
          [s + 3.2, 'click', btn(3, 'Save to Diolog'), {'lead': 0.65}],
          [s + 3.45, 'scroll', '#w1', 5, 0.7], [s + 3.45, 'arrive', '#w1', [4, 5], {'gap': 0.12}], [s + 3.5, 'frame', ch(5, p=18), 0.7, 0.7],
          [s + 4.7, 'frame', ch([0, 3], w='#w2', p=20), 0.5, 1.0], [s + 4.7, 'arrive', '#w2', [0, 1], {'gap': 0.2}],
          [s + 5.3, 'arrive', '#w2', [2, 3], {'gap': 0.12}], [s + 5.8, 'ink', el('#qa-b-src .t .tx', w='#w2'), 'ok', 0.4],
          [s + 6.6, 'scroll', '#w2', 4, 0.8], [s + 6.6, 'arrive', '#w2', 4, {'y': 24, 'dur': 0.7}], [s + 6.65, 'frame', ch(4, w='#w2', p=14), 0.68, 0.9],
          [s + 7.6, 'ink', el('.jsrc', w='#w2', i=4), 'ok', 0.5],
          [s + 8.8, 'frame', [0, 0, 2940, 900], 0.97, 1.1, {'free': True}]]
    return {'id': 'clip', 'kind': 'win', 'dur': round(s + 14.2, 1), 'windows': [['w1', 'r3-k4-dana'], ['w2', 'k4-marcus']], 'pos': {'w2': 'left:1500px'},
            'css': '#cliproot .k-cam { width: 2940px; }   /* both windows inside the camera, so it can travel to the client’s window */',
            'spec': {'windows': ['#w1', '#w2'], 'hidden': {'#w1': 0, '#w2': 0}, 'start': {'frame': [0, 0, 2940, 900], 'fill': 0.97, 'opts': {'free': True}}, 'steps': st}, 'sfx': []}


def k05():
    st = [[0.5, 'ink', el('#rem-bad'), 'bad', 0.5, 'rem'],
          [2.2, 'scroll', '#w1', 2, 0.7], [2.2, 'arrive', '#w1', [1, 2], {'gap': 0.25}], [2.25, 'frame', u(ch(1), ch(2)), 0.55, 0.8],
          [2.45, 'tool', *run(2, ['Checking 12 figures against the release…', 'Comparing each with its source…'], 1.4)],
          [3.9, 'scroll', '#w1', 4, 0.8], [3.9, 'arrive', '#w1', [3, 4], {'gap': 0.12}], [3.95, 'frame', ch(4, p=16), 0.7, 0.8],
          [4.8, 'frame', el('.dc-lead', i=4, p=14), 0.7, 0.7], [5.2, 'ink', el('.dc-lead b.bad', i=4), 'bad', 0.4], [5.6, 'ink', el('.dc-lead b.ok', i=4), 'ok', 0.4],
          [6.5, 'frame', u(el('.dc-quote', i=4), btn(4, 'Use $453.7 million'), p=16), 0.6, 0.8], [6.9, 'ink', el('#k5-quote'), 'review', 0.5],
          [8.2, 'click', btn(4, 'Use $453.7 million'), {'lead': 0.65}],
          [8.45, 'scroll', '#w1', 6, 0.7], [8.45, 'arrive', '#w1', [5, 6], {'gap': 0.12}], [8.5, 'frame', ch(6, p=18), 0.7, 0.8],
          [10.2, 'scroll', '#w1', 7, 0.8], [10.2, 'arrive', '#w1', 7, {'y': 24, 'dur': 0.7}], [10.25, 'frame', el('.jdoc', i=7, p=18), 0.72, 0.9],
          [11.2, 'ink', el('#rem-fixed'), 'ok', 0.5], [12.6, 'frame', u(ch(6), ch(7), p=16), 0.6, 0.9]]
    return win('clip', 'r3-k5b', 20.2, {'frame': el('.jdoc', i=0, p=18), 'fill': 0.72}, st, hidden=1, sfx=[[8.6, 'chime']])


def k06():
    st = [[x[0] * 1.2 if isinstance(x[0], (int, float)) else x[0], *x[1:]] for x in qa_steps(0, open_pack=True, pre=True)]
    t = 8.4
    st += [[t, 'ink', el('.jdoc p', i=4, t='Comparable sales decreased'), 'review', 0.5],
           [t + 1.0, 'frame', u(ch(3), ch(4), p=12), 0.5, 0.9],
           [t + 1.6, 'click', btn(3, 'Save to Diolog'), {'lead': 0.7}],
           [t + 1.9, 'scroll', '#w1', 7, 0.9], [t + 1.9, 'arrive', '#w1', 5], [t + 1.95, 'frame', ch(5, p=40), 0.6, 0.7],
           [t + 1.9, 'tool', *run(5, ['Saving the pack to Diolog…'], 0.8)],
           [t + 2.7, 'arrive', '#w1', [6, 7], {'gap': 0.12}], [t + 2.7, 'frame', ch(7, p=18), 0.7, 0.8],
           [t + 3.5, 'ink', el('#qs-ok .t .tx'), 'ok', 0.45]]
    return win('clip', 'r3-k6', 20.0, {'frame': COMP, 'fill': 0.9}, st)


def k07():
    p, s = ask(8.4, 'What does the draft say about the outlook?')
    st = [*newdoc_steps(0),
          [4.5, 'click', btn(3, 'Open the record'), {'lead': 0.65}], [4.6, 'panel', '#w1', 0.5],
          [4.65, 'frame', el('.pv', p=10, open=True), 0.62, 0.8],
          [5.5, 'wheel', el('.pv-row', open=True), 0], [5.6, 'ink', el('#rv-script .d .tx'), 'ok', 0.45],
          [6.6, 'wheel', el('.pv-row', open=True), 2], [7.4, 'unwheel', el('.pv-row', open=True)],
          [7.6, 'unpanel', '#w1', 0.45], [7.7, 'frame', COMP, 0.9, 0.7], *p,
          [s, 'scroll', '#w1', 7, 0.8], [s, 'arrive', '#w1', [4, 5], {'gap': 0.2}], [s, 'frame', u(ch(4), ch(5), p=30), 0.6, 0.7],
          [s + 0.2, 'tool', *run(5, ['Searching lululemon’s record…'], 0.7)],
          [s + 0.9, 'arrive', '#w1', [6, 7], {'gap': 0.12}], [s + 0.9, 'frame', ch(7, p=16), 0.7, 0.8],
          [s + 1.6, 'ink', el('#u-src .d .tx'), 'ok', 0.4], [s + 2.0, 'ink', el('.dc-quote', i=7), 'review', 0.6]]
    return win('clip', 'r3-k7', round(s + 7.6, 1), {'frame': DROP, 'fill': 0.86}, st)


def k08():
    p, s = ask(0, 'Build our Q2 earnings deck from the Q1 deck.', pre=True)
    st = [*p, [s, 'arrive', '#w1', 0], [s, 'frame', u(ch(0), ch(3)), 0.55, 0.7],
          [s + 0.25, 'arrive', '#w1', 1], [s + 0.25, 'tool', *run(1, ['Taking the Q1 deck’s structure…', 'Placing Q2’s figures…'], 1.2)],
          [s + 1.45, 'arrive', '#w1', [2, 3], {'gap': 0.15}],
          [s + 1.9, 'scroll', '#w1', 5, 0.9], [s + 1.9, 'arrive', '#w1', 4], [s + 1.95, 'stream', {'i': 4, 'w': '#w1'}, 0.8],
          [s + 2.3, 'arrive', '#w1', 5, {'y': 24, 'dur': 0.7}], [s + 2.3, 'frame', el('.jslide', i=5, p=10), 0.76, 0.9],
          *deck_roll(round(s + 3.2, 2), 5),
          [s + 5.9, 'scroll', '#w1', 8, 0.8], [s + 5.9, 'arrive', '#w1', [6, 7, 8], {'gap': 0.12}], [s + 6.05, 'frame', ch(8, p=16), 0.7, 0.8],
          [s + 6.8, 'ink', el('.dc-row .t .tx', i=8), 'ok', 0.45],
          [s + 8.0, 'click', btn(8, 'Save to Diolog'), {'lead': 0.65}],
          [s + 8.3, 'scroll', '#w1', 11, 0.9], [s + 8.3, 'arrive', '#w1', 9], [s + 8.35, 'frame', ch(9, p=40), 0.6, 0.7],
          [s + 8.3, 'tool', *run(9, ['Saving the deck to Diolog…'], 0.8)],
          [s + 9.1, 'arrive', '#w1', [10, 11], {'gap': 0.12}], [s + 9.1, 'frame', ch(11, p=18), 0.7, 0.8],
          [s + 9.9, 'ink', el('#ds-ok .t .tx'), 'ok', 0.45]]
    return win('clip', 'r3-k8b', round(s + 16.2, 1), {'frame': COMP, 'fill': 0.9}, st)


def k09():
    st = [[0.2, 'frame', u(ch(0), ch(2)), 0.64, 0.8], [0.2, 'arrive', '#w1', 1],
          [0.2, 'tool', *run(1, ['Reading the newest 13G filings…', 'Checking each holder…'], 1.6)], [1.8, 'arrive', '#w1', 2],
          [2.1, 'scroll', '#w1', 4, 0.8], [2.1, 'arrive', '#w1', [3, 4], {'gap': 0.12}], [2.2, 'frame', ch(4, p=16), 0.7, 0.8],
          [3.0, 'wheel', el('.dc-row', i=4), 0], [3.1, 'ink', el('#o-r1 .d .tx'), 'review', 0.45],
          [3.9, 'wheel', el('.dc-row', i=4), 1], [4.0, 'ink', el('#o-r2 .d .tx'), 'review', 0.45], [4.9, 'unwheel', el('.dc-row', i=4)],
          [5.3, 'click', btn(4, 'Open ownership'), {'lead': 0.65}], [5.4, 'panel', '#w1', 0.5], [5.45, 'frame', el('.pv', p=10, open=True), 0.62, 0.8],
          [6.3, 'wheel', el('.pv-row', open=True), 1], [6.4, 'ink', el('#ov-cedar .d .tx'), 'ok', 0.4],
          [7.1, 'wheel', el('.pv-row', open=True), 2], [7.2, 'ink', el('#ov-lark .d .tx'), 'ok', 0.4],
          [8.1, 'unwheel', el('.pv-row', open=True)], [8.3, 'unpanel', '#w1', 0.45], [8.4, 'frame', u(el('#o-r2'), btn(4, 'Update the 2 lines'), p=16), 0.66, 0.8],
          [9.4, 'click', btn(4, 'Update the 2 lines'), {'lead': 0.65}],
          [9.65, 'scroll', '#w1', 6, 0.7], [9.65, 'arrive', '#w1', [5, 6], {'gap': 0.12}], [9.7, 'frame', ch(6, p=18), 0.7, 0.8],
          [10.6, 'ink', el('.dc-lead b.ok', i=6), 'ok', 0.4]]
    return win('clip', 'r3-own', 20.0, {'frame': ch(0, p=24), 'fill': 0.42}, st, hidden=1, sfx=[[9.75, 'chime']])


def k10():
    p, s = ask(7.1, 'What did they ask on their last call?')
    st = [[0, 'drag', {'from': [960, 560], 'to': el('.cf-composer'), 'file': 'Holder call, Sep 10.txt'}, 1.05],
          [1.15, 'arrive', '#w1', 0], [1.15, 'frame', u(ch(0), ch(1)), 0.62, 0.7],
          [1.4, 'arrive', '#w1', 1], [1.4, 'tool', *run(1, ['Matching the investors on the call…', 'Pulling out each question…'], 0.9)],
          [2.3, 'arrive', '#w1', [2, 3], {'gap': 0.12}], [2.3, 'frame', ch(3, p=16), 0.7, 0.8],
          [3.3, 'click', btn(3, 'Review in the calls view'), {'lead': 0.65}], [3.4, 'panel', '#w1', 0.5],
          [3.45, 'frame', el('.cf-pbody', p=4, open=True), 0.6, 0.8],
          [4.2, 'wheel', el('#cv-a .pv-row', open=True), 0], [4.8, 'wheel', el('#cv-a .pv-row', open=True), 1], [5.3, 'unwheel', el('#cv-a .pv-row', open=True)],
          [5.6, 'click', el('#cv-a .pv-acts .dc-btn', open=True), {'lead': 0.65}], [5.75, 'swap', el('#cv-a', open=True), el('#cv-b', open=True)],
          [6.5, 'unpanel', '#w1', 0.45], [6.6, 'frame', COMP, 0.9, 0.7], *p,
          [s, 'scroll', '#w1', 7, 0.8], [s, 'arrive', '#w1', [4, 5], {'gap': 0.2}], [s, 'frame', u(ch(4), ch(5), p=30), 0.6, 0.7],
          [s + 0.2, 'tool', *run(5, ['Searching lululemon’s record…'], 0.7)],
          [s + 0.9, 'arrive', '#w1', [6, 7], {'gap': 0.12}], [s + 0.9, 'frame', ch(7, p=16), 0.7, 0.8],
          [s + 1.85, 'click', btn(7, 'Open in the calls view'), {'lead': 0.65}], [s + 1.95, 'panel', '#w1', 0.5],
          [s + 2.0, 'frame', el('.cf-pbody', p=4, open=True), 0.6, 0.8],
          [s + 2.6, 'wheel', el('#cv-b .pv-row', open=True), 0], [s + 2.65, 'ink', el('#cv-b #cv-1 .side .tx', open=True), 'ok', 0.3],
          [s + 3.2, 'wheel', el('#cv-b .pv-row', open=True), 1], [s + 3.25, 'ink', el('#cv-b #cv-2 .side .tx', open=True), 'ok', 0.3],
          [s + 3.8, 'wheel', el('#cv-b .pv-row', open=True), 2], [s + 4.6, 'unwheel', el('#cv-b .pv-row', open=True)]]
    return win('clip', 'r3-k10', round(s + 9.4, 1), {'frame': DROP, 'fill': 0.86}, st, sfx=[[5.75, 'chime']])


CLIPS = {'K02': (k02(), 0.4), 'K03': (k03(), 1.3), 'K04': (k04(), 2.4), 'K05': (k05(), 1.6), 'K06': (k06(), 1.3),
         'K07': (k07(), 0.6), 'K08': (k08(), 1.4), 'K09': (k09(), 0.4), 'K10': (k10(), 0.6)}
for fid, (sc, at) in CLIPS.items():
    FILMS[fid] = {'title': TITLES[fid], 'scenes': [sc], 'voice': [[f'q{fid[1:].lstrip("0")}', 'clip', at]], 'tempo': 1.0}
FILMS['K07']['limit'] = 0.6     # its voiced cut peaks at +1.3 dBTP after AAC without the limiter

# ---- pace (owner: "overall the round 3 videos were very fast"), then the settling push, then the projects ----------
FE.apply_labels(FILMS)
P = CFG['pace']
apply_pace(FILMS, CFG['overview'], {'overview': P['overview'], 'short': P['short']}, intro=P['intro'])
for fid, f in FILMS.items():
    if f['scenes'][-1]['kind'] == 'win':
        settle_push(f['scenes'][-1], f.get('lockbar', True))

if __name__ == '__main__':
    write_series(FILMS, HERE, S.S)
