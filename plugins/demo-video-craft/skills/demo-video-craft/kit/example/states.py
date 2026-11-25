#!/usr/bin/env python3
"""The example series' screens: Claude windows holding Acme Record's cards, for a fictional client, Fernhill
Instruments (Nasdaq: FHLX; name and ticker checked free in SEC's company_tickers.json on 25 Nov 2026). Its figures are
invented and consistent across every screen. Replace all of it with your series' scenario.

    python3 states.py        # writes states/<id>.html and states/index.html, every state on one page to look at

A state is the whole window at the moment a scene opens. Its thread items arrive by index (0, 1, 2, ...), so list them
in the order the scene reveals them. Item 0 is the person's prompt: ask() types it, sends it, and item 0 arrives.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '_kit' / 'engine'))
import states_engine as E  # noqa: E402

E.configure(product='Acme Record', who={'dana': ('DR', 'Dana Ruiz', 'Advisor · Enterprise plan')})
card, lead = E.card, E.lead

# Every name an earlier scenario used, so none survives on a screen after a switch (E.write fails on any of them).
BANNED = []

CHECK = card({
    'id': 'check', 'title': 'Your Q3 deck: 11 of 12 figures match the filed release', 'tier': 'Internal',
    'sub': 'Fernhill Instruments · Q3 2026 earnings deck, slide 7',
    'lead': lead([('Revenue', '$412.6M', 'chk'), ('Gross margin in the deck', '41.8%', 'bad'), ('In the release', '41.2%', 'chk')]),
    'rows': [{'t': 'Revenue, $412.6 million', 'd': 'Matches the release, page 1', 'k': 'ok', 'id': 'r-rev'},
             {'t': 'Gross margin, 41.8%', 'd': 'The release says 41.2%', 'k': 'bad', 'id': 'r-gm'},
             {'t': 'Operating cash flow, $58.3 million', 'd': 'Matches the release, page 3', 'k': 'ok', 'id': 'r-ocf'}],
    'quote': '<span class="q">“Gross margin was 41.2%, compared with 40.6% in the third quarter of 2025.”</span>'
             '<small>Q3 2026 earnings release · filed Nov 5, 2026</small>',
    'acts': [{'label': 'Use 41.2%'}, {'label': 'Show the release', 'sec': True}]})

FIXED = card({
    'id': 'fixed', 'title': 'Your Q3 deck: 12 of 12 figures match the filed release', 'tier': 'Internal',
    'sub': 'Fernhill Instruments · Q3 2026 earnings deck, slide 7 updated',
    'lead': lead([('Gross margin', '41.2%', 'ok'), ('Figures checked', '12 of 12', 'chk')]),
    'rows': [{'t': 'Slide 7 now says 41.2%', 'd': 'From the Q3 2026 earnings release, page 1', 'k': 'ok', 'id': 'f-gm'}],
    'acts': [{'label': 'Save to Acme Record'}]})

SAVED = card({
    'id': 'saved', 'title': 'Saved to Acme Record for review', 'tier': 'Internal',
    'sub': 'Fernhill Instruments · Q3 2026 earnings deck, version 4',
    'rows': [{'t': 'Waiting for the IR team’s approval', 'd': 'Each figure linked to its source', 'k': 'ok', 'id': 's-ok'}]})

S = {
    'check': E.frame('claude', 'dana', 'Q3 deck check', [
        E.user('Check our Q3 deck against the filed release.'),
        E.tool('check_figures', done=False, run='Using Acme Record: check_figures'),
        E.say('I checked each figure on slide 7 against Fernhill’s Q3 release, filed Nov 5.'),
        CHECK,
        FIXED,
        E.tool('save_draft', done=False, run='Using Acme Record: save_draft'),
        SAVED,
    ], ('Q2 deck', 'Holder questions', 'Earnings brief')),
}

# ---- The product's own interface: a dashboard in a browser (K02) and the phone app (K03) ---------------------------
# Markup is the product's own; the list that arrives by index carries data-items and its scrolling region
# data-viewport. Its styles live in theme.css with the rest of the product's look.
HIT = lambda rid, doc, where, k, note: E.row({'id': rid, 't': doc, 'd': where, 'k': k, 'side': note})   # noqa: E731
S['dash'] = E.app(
    '<div class="ac-dash"><aside class="ac-side"><b class="ac-brand"><svg aria-hidden="true"><use href="#i-mark"/></svg>Acme Record</b>'
    '<span class="on">Search</span><span>Documents</span><span>Checks</span><span>Filings</span></aside>'
    '<main class="ac-main"><div class="ac-search"><svg aria-hidden="true"><use href="#i-search"/></svg><span id="q" class="ac-q">Search the record</span></div>'
    '<div class="ac-view" data-viewport><div class="ac-list" data-items>'
    + E.card({'id': 'hits', 'title': '41.2% appears in 4 documents', 'tier': 'Published', 'tk': 'green',
              'sub': 'Fernhill Instruments · gross margin, Q3 2026',
              'rows': [{'id': 'h1', 't': 'Q3 2026 earnings release', 'd': 'Filed Nov 5, 2026 · page 1', 'k': 'ok', 'b': ['Filed', 'ok']},
                       {'id': 'h2', 't': 'Q3 2026 earnings deck, slide 7', 'd': 'Version 4 · corrected', 'k': 'ok', 'b': ['Matches', 'ok']},
                       {'id': 'h3', 't': 'Q3 call script, page 2', 'd': 'Draft 2', 'k': 'bad', 'b': ['Says 41.8%', 'bad']},
                       {'id': 'h4', 't': 'Investor FAQ', 'd': 'Published Nov 6, 2026', 'k': 'ok', 'b': ['Matches', 'ok']}],
              'acts': [{'label': 'Fix the call script'}]})
    + E.card({'id': 'fixed2', 'title': 'The call script now says 41.2%', 'tier': 'Internal',
              'sub': 'Draft 3 · from the Q3 2026 earnings release, page 1',
              'rows': [{'id': 'f2', 't': '4 of 4 documents match the filed release', 'k': 'ok', 'b': ['Consistent', 'ok']}]})
    + '</div></div></main></div>', kind='browser', url='app.acme.example/search')

S['phone'] = E.app(
    '<div class="ac-phone"><header class="ac-ph-head"><small>Wednesday, Nov 26</small><b>Today</b></header>'
    '<div class="ac-ph-view" data-viewport><div class="ac-ph-list" data-items>'
    + E.card({'id': 'pc1', 'title': 'One figure needs you before the 9am call', 'tier': 'Internal', 'tk': 'amber',
              'origin': 'Checked overnight against the Q3 release', 'oic': 'clock',
              'sub': 'Q3 call script, page 2',
              'lead': E.lead([('In the script', '41.8%', 'bad'), ('In the release', '41.2%', 'chk')]),
              'acts': [{'label': 'Use 41.2%'}]})
    + E.card({'id': 'pc2', 'title': 'The call script is ready', 'tier': 'Internal',
              'sub': 'Draft 3 · 12 of 12 figures match the release',
              'rows': [{'id': 'p2', 't': 'Sent to the IR team for approval', 'k': 'ok'}]})
    + E.card({'id': 'pc3', 'title': 'Next: 3 investor questions on margin', 'tier': 'Market-facing', 'tk': 'amber',
              'sub': 'Draft answers from the Q3 release, ready to review',
              'rows': [{'id': 'p3', 't': 'Each answer quotes the release it comes from', 'k': 'ok'}],
              'acts': [{'label': 'Review the answers'}]})
    + '</div></div></div>', kind='phone')

if __name__ == '__main__':
    out = E.write(S, HERE, banned=BANNED)
    print(f'{len(S)} states written to {out}')
