#!/usr/bin/env python3
"""The reference series' screens: the Diolog Guardian launch series of 25 Nov 2026, ported onto the kit unchanged. Claude
and ChatGPT windows holding Diolog Guardian's cards and side-panel views, filled with lululemon athletica inc.
(Nasdaq: LULU) from its published record. Every figure, guidance line, date and holder comes from the filings listed
in SOURCES.md; the firm's drafts, inbox questions, approvals and the holder call are illustrative, name no real person
or institution, and draw their figures from those filings. The advisor, Dana Ruiz, is fictional. US English.

    python3 fetch_marks.py && python3 states.py      # the hosts' and the client's marks first, then every screen

The screens are the source's own markup through the kit's builders (frame, card, row, lead, tool, by, say, box, prow,
solo, all drawing what the source's did); only the writer is the kit's.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '_kit' / 'engine'))
import states_engine as E  # noqa: E402
from states_engine import box, by, card, frame, ic, lead, prow, row, say, solo, tool, user  # noqa: E402,F401

E.configure(product='Diolog Guardian', host_marks=True, model='Opus 5.5',
            who={'dana': ('DR', 'Dana Ruiz', 'Advisor · Enterprise plan'),
                 'client': ('IR', 'Investor relations', 'lululemon · Enterprise')})

REC_D = ('Q2 earnings deck', 'Post-earnings brief', 'Analyst Q&A, Q2', 'Ownership note')

# ---- lululemon's Q2 2026 deck, in its own theme (built in the assistant; Diolog supplies theme and figures) ------
# Q1 and Q2 fiscal 2026 earnings releases (8-K Exhibit 99.1, Jun 4 and Sep 3, 2026).
KPIS = [('Net revenue', '$2.47B', '$2.42B', '−4% vs Q2 2025', 'k-rev'),
        ('Comparable sales', '+1%', '−9%', 'Americas −12%', 'k-comp'),
        ('Gross margin', '54.2%', '60.5%', '+200 bps', 'k-gm'),
        ('Operating margin', '11.2%', '18.8%', '−190 bps', 'k-om')]
LOGO = ic('lulu-full', 'full')


def deck(q='Q1', state='from'):
    """The deck artifact Claude builds: one large slide and a strip. state 'from' shows the Q1 figures, which K.count
    rolls to Q2 (each <b> carries data-to)."""
    tiles = ''.join(f'<div class="jt"><small>{n}</small><b id="{i}" data-to="{b}">{a if state == "from" else b}</b><em>{e if state == "to" else "&nbsp;"}</em></div>'
                    for n, a, b, e, i in KPIS)
    thumbs = ''.join(f'<div class="jth{" on" if k == 2 else ""}"><i></i><span>{t}</span></div>'
                     for k, t in enumerate(['lululemon', 'Highlights', 'At a glance', 'Comparable sales', 'Stores', 'Outlook']))
    return (f'<div class="k-art" id="deck"><div class="k-art-h">{ic("grid")}<span><b>lululemon {q} 2026 earnings</b> · Presentation · 12 slides</span><span class="pill">lululemon theme</span></div>'
            f'<div class="jslide"><div class="jhead"><span class="jlogo">{LOGO}</span><span class="jq" id="jq">{q} 2026 at a glance</span></div>'
            f'<div class="jtiles">{tiles}</div><div class="jfoot">Figures from lululemon’s {q} 2026 earnings release</div></div>'
            f'<div class="jstrip">{thumbs}</div></div>')


S = {}

# ==== Overview: the deck from the record, the check, the brief, the inbox ======================================
MATERIALS = card({'id': 'materials', 'title': 'lululemon’s Q2 earnings materials', 'tier': 'Published', 'tk': 'green',
                  'sub': 'lululemon athletica inc. · Nasdaq: LULU · newest version of each',
                  'rows': [
                      {'ic': 'doc', 't': 'Q2 2026 earnings release', 'd': 'Form 8-K, Exhibit 99.1 · Sep 3, 2026', 'b': ['Published', 'ok']},
                      {'ic': 'doc', 't': 'Q2 2026 earnings call transcript', 'd': 'Supplied by Dana Ruiz · Sep 3, 2026', 'b': ['Published', 'ok']},
                      {'ic': 'doc', 't': 'Form 10-Q', 'd': 'From SEC EDGAR · Sep 3, 2026', 'b': ['Published', 'ok']},
                      {'ic': 'doc', 't': 'Q1 2026 earnings deck · V12', 'd': 'Current version · its structure, reused', 'b': ['Current', 'blue'], 'id': 'r-q2deck'},
                  ],
                  'reason': 'Read from lululemon’s record. Earlier versions were left out.'})

FIGCHECK = card({'id': 'figcheck', 'title': 'Your Q2 deck: 23 of 24 figures match the record', 'tier': 'Internal',
                 'sub': 'Claude made the slides. Diolog supplied the theme and the figures, and ran the check.',
                 'lead': lead([['Figures linked', '24'], ['Match', '23', 'ok', 'fc-match'], ['Differ', '1', 'warn', 'fc-differ']]),
                 'rows': [
                     {'k': 'warn', 't': 'Slide 7 · Operating margin 18.9%', 'd': 'From the speaker notes. The release lululemon filed says <span id="fc-src">18.8%</span>.', 'b': ['Figures differ', 'warn'], 'id': 'fc-row'},
                     {'k': 'ok', 't': '23 figures match their tracked source', 'b': ['Consistent', 'ok']},
                 ],
                 'quote': '<span id="fc-quote">“Income from operations decreased 13% to $453.7 million and operating margin decreased 190 basis points to 18.8%.”</span><br><small>Q2 2026 earnings release · Sep 3, 2026 · page 1</small>',
                 'acts': [{'label': 'Use 18.8%'}, {'label': 'Open the source'}]})

FIXED = card({'id': 'fixed', 'title': 'Your Q2 deck: 24 of 24 figures match the record', 'tier': 'Internal',
              'sub': 'Slide 7 now says 18.8%, linked to the Q2 release.',
              'lead': lead([['Figures linked', '24'], ['Match', '24', 'ok'], ['Differ', '0']]),
              'acts': [{'label': 'Save to Diolog'}, {'label': 'Open the deck'}],
              'reason': 'Saving stores this file as a draft in Diolog. Nothing is sent.'})

S['o-deck'] = frame('claude', 'dana', 'Q2 earnings deck', [
    user('Pull lululemon’s Q2 earnings materials and build the earnings deck the way we did Q1.'),
    tool('search_record'), by(), MATERIALS,
    tool('get_theme'),
    say('Here’s the Q2 deck on the Q1 structure, in lululemon’s theme. Diolog supplied the figures.'),
    deck('Q1', 'from'),
    tool('run_check'), by(), FIGCHECK, by(), FIXED,
], REC_D[1:], composer='Reply to Claude')

STEP = card({'id': 'step', 'origin': 'lululemon filed its Q2 earnings release · Form 8-K · Sep 3, 2026', 'oic': 'clock',
             'title': 'lululemon’s Q2 earnings release is available', 'tier': 'Published', 'tk': 'green',
             'sub': 'lululemon athletica inc. · a step suggested for Dana Ruiz',
             'rows': [{'ic': 'spark', 't': 'Prepare the post-earnings brief', 'd': 'Results against guidance and what changed since Q1, each figure linked to its source'}],
             'acts': [{'label': 'Do it', 'ic': 'play'}, {'label': 'Skip'}],
             'reason': 'A prepare step reads, drafts, stores and checks. It never sends.'})

BRIEF = card({'id': 'brief', 'title': 'Post-earnings brief: lululemon Q2 2026', 'tier': 'Internal',
              'sub': 'Drafted from 4 sources · saved to Diolog as a draft',
              'lead': lead([['Net revenue', '$2.42B', 'chk'], ['Comparable sales', '−9%'], ['FY26 revenue outlook', '$10.35B to $10.50B']]),
              'rows': [
                  {'ic': 'chart', 't': 'Results against guidance', 'd': 'Net revenue of $2.42B, below the $2.450B to $2.475B range given in June', 'id': 'b-r1'},
                  {'ic': 'list', 't': 'What changed since Q1', 'd': 'Comparable sales −9%, from +1% in Q1; Americas −12%', 'id': 'b-r2'},
                  {'ic': 'q', 't': 'Questions analysts are likely to ask', 'd': 'The revised outlook, tariff refunds, the Americas', 'side': '3'},
                  {'ic': 'doc', 't': 'Sources', 'd': 'Q2 release · Q2 call transcript · 10-Q · Q1 release', 'side': '4'},
              ],
              'acts': [{'label': 'Open the brief'}, {'label': 'Start the Q&A pack'}],
              'reason': 'Saved to Diolog as a draft. Nothing has been sent.'})

S['o-brief'] = frame('claude', 'dana', 'lululemon Q2 results', [
    by(), STEP,
    say('lululemon’s Q2 earnings release is available. Want me to prepare your post-earnings brief?'),
    tool('get_claims', done=False, run='Reading the Q2 release…'), by(), BRIEF,
], ('Q2 earnings deck', 'Analyst Q&A, Q2', 'Ownership note'))

QCOUNT = card({'id': 'qcount', 'title': '6 investor questions this week', 'tier': 'Market-facing', 'tk': 'amber',
               'sub': 'lululemon athletica inc. · counts and approved themes only',
               'lead': lead([['New', '6'], ['Oldest waiting', '2 days'], ['On one theme', '5']]),
               'rows': [{'ic': 'q', 't': 'Approved theme: the revised full-year outlook', 'd': '5 of 6 questions · names and messages stay in Diolog', 'id': 'q-theme'}],
               'acts': [{'label': 'Open questions', 'ic': 'panel'}],
               'reason': 'Investors’ names and their messages open only in Diolog’s view.'})

ANSWER = card({'id': 'answer', 'title': 'Draft answer: the revised outlook', 'tier': 'Market-facing', 'tk': 'amber',
               'sub': 'For 5 questions on one theme · grounded in 2 sources',
               'quote': '<span id="a-quote">For 2026, lululemon now expects net revenue of $10.350 billion to $10.500 billion, a decline of 5% to 7%.<sup>1</sup> In June, the range was $11.000 billion to $11.150 billion.<sup>2</sup> The outlook includes $0.86 per share from tariff refunds received in the second quarter, and no further refunds.<sup>1</sup></span>',
               'rows': [{'ic': 'doc', 't': '1 · Q2 2026 earnings release', 'd': 'Sep 3, 2026 · page 2', 'id': 'a-s1'},
                        {'ic': 'doc', 't': '2 · Q1 2026 earnings release', 'd': 'Jun 4, 2026 · page 2', 'id': 'a-s2'}],
               'acts': [{'label': 'Save to Diolog for review'}, {'label': 'Edit'}],
               'reason': 'Saving stores this version in Diolog for review. It isn’t sent.'})

SAVED = card({'id': 'saved', 'title': 'Saved to Diolog for review', 'tier': 'Internal',
              'sub': 'Version 1 · the draft reply for 5 questions on the outlook',
              'rows': [{'k': 'ok', 't': 'Waiting for review in Diolog', 'd': 'lululemon’s IR team reviews and approves it there'}]})

QVIEW = (f'<div class="pv"><p class="crumb">Questions and replies</p><h4>The revised full-year outlook</h4><p class="meta">5 questions this week · from lululemon’s IR inbox</p>'
         + box('Questions', '5', prow('An institutional holder', 'Asks what the new range assumes for the Americas', 'Sep 8')
               + prow('A shareholder', 'Asks whether more tariff refunds are in the outlook', 'Sep 9')
               + prow('A shareholder', 'Asks why the full-year range came down', 'Sep 10')
               + prow('2 more', '', ''))
         + '<div id="qv-draft">' + box('Draft reply', 'Version 1', prow('From Dana Ruiz, in Claude', 'Grounded in the Q2 and Q1 releases', '<span class="badge">Draft</span>', 'qv-row')) + '</div>'
         + '<p class="pv-foot">This view fetches from Diolog. The questions never enter the conversation.</p></div>')

S['o-inbox'] = frame('claude', 'dana', 'Investor questions', [
    user('What’s waiting in lululemon’s inbox?'), tool('list_questions'), by(), QCOUNT,
    user('Draft our answer on the outlook from the Q2 and Q1 releases.'),
    tool('get_claims'), by(), ANSWER, by(), SAVED,
], ('Q2 earnings deck', 'Post-earnings brief', 'Analyst Q&A, Q2'), panel=QVIEW, ptitle='Questions and replies')

# the burst: five abilities, one card each
S['o-b1'] = solo('claude', card({'title': 'Analyst Q&A pack: 14 likely questions, each answered from the record', 'tier': 'Internal',
                                 'sub': 'lululemon Q2 2026 · drafted in Claude, checked by Diolog',
                                 'rows': [{'ic': 'q', 't': 'Why did comparable sales fall 9% in Q2?', 'd': 'Q2 release, page 1', 'b': ['Checked', 'ok']},
                                          {'ic': 'q', 't': 'What’s in the revised full-year outlook?', 'd': 'Q2 release, page 2', 'b': ['Checked', 'ok']}]}), 'In Claude')
S['o-b2'] = solo('chatgpt', card({'title': '2 of 3 holders in this write-up are out of date', 'tier': 'Published', 'tk': 'green',
                                  'sub': 'Ownership check · each holder against their newest filing',
                                  'rows': [{'k': 'warn', 't': 'The Vanguard Group', 'd': 'The write-up says 10.05%. Its 13G/A of Mar 27, 2026 reports no shares.', 'b': ['Out of date', 'warn']},
                                           {'k': 'warn', 't': 'BlackRock, Inc.', 'd': 'The write-up says 7.6%. The 13G/A filed Oct 27 says 5.8%.', 'b': ['Out of date', 'warn']}]}), 'In ChatGPT')
S['o-b3'] = solo('claude', card({'title': 'A holder call is filed, and 6 questions wait for review', 'tier': 'Internal',
                                 'sub': 'Transcript attached in Claude · investors matched',
                                 'rows': [{'ic': 'users', 't': 'A top-20 holder · 2 people', 'd': 'Matched to lululemon’s investor records'},
                                          {'ic': 'q', 't': '6 questions, answers and responses', 'd': 'Each kept with its timestamp'}]}), 'In Claude')
S['o-b4'] = solo('chatgpt', card({'title': 'Using the current investor deck: V18 of Sep 10', 'tier': 'Published', 'tk': 'green',
                                  'sub': 'Replaces V17 of Sep 3 · 2 slides changed',
                                  'rows': [{'k': 'ok', 't': 'Investor presentation V18.pptx', 'b': ['Current', 'ok']},
                                           {'ic': 'clock', 't': 'V17 · Sep 3, 2026', 'd': 'Superseded · shown only when asked for', 'b': ['Replaced']}]}), 'In ChatGPT')
S['o-b5'] = solo('claude', card({'title': 'Filed in lululemon’s record: the Q2 release draft', 'tier': 'Unreleased', 'tk': 'blue',
                                 'sub': 'Supplied by Dana Ruiz · Published once lululemon files it',
                                 'rows': [{'ic': 'doc', 't': 'Q2 2026 earnings release, draft.docx', 'd': '9 pages · version 1', 'b': ['Unreleased', 'blue']}]}), 'In Claude')

# ==== K01 The current version (not in the current lineup) =========================================================
PROJECT = ('<div class="k-proj"><div class="k-proj-h">' + ic('folder') + '<b>lululemon athletica inc.</b><span>Project files</span></div>'
           + ''.join(f'<div class="k-pf">{ic("doc")}<span>{n}</span><em>{d}</em></div>' for n, d in [
               ('Investor presentation V15.pptx', 'Jun 4'), ('Investor presentation V16.pptx', 'Jul 8'),
               ('Q1 deck FINAL v2.pptx', 'Jun 4'), ('Investor presentation V17.pptx', 'Sep 3')])
           + f'<div class="k-pf k-new" id="pf-new">{ic("doc")}<span>Investor presentation V18.pptx</span><em>Sep 10</em></div>'
           + '<div class="k-drop" id="drop">Drop files to add them to the project</div></div>')
S['k1-old'] = frame('claude', 'dana', 'lululemon', [PROJECT], ('Q2 earnings deck', 'Post-earnings brief'))
CLAIMS = card({'id': 'claims', 'title': 'What the Q1 release said about comparable sales', 'tier': 'Published', 'tk': 'green',
               'sub': 'lululemon athletica inc. · from the current version of each source',
               'quote': '<span id="c-quote">“Comparable sales increased 1%, or decreased 2% on a constant dollar basis.”</span>',
               'rows': [{'ic': 'doc', 't': 'Q1 2026 earnings release', 'd': '<span id="c-date">Jun 4, 2026</span> · page 1', 'b': ['Current', 'ok'], 'id': 'c-src'},
                        {'ic': 'doc', 't': 'Investor presentation V18', 'd': 'Sep 10, 2026 · slide 6 · replaces V17 of Sep 3', 'b': ['Current', 'ok'], 'id': 'c-deck'}],
               'reason': 'Answered from the current version. V17 comes back only if you ask for it.'})
S['k1-ask'] = frame('claude', 'dana', 'Comparable sales', [
    user('What did the Q1 release say about comparable sales?'), tool('get_claims'), by(), CLAIMS,
], ('lululemon', 'Q2 earnings deck'))

# ==== K02 Your post-earnings brief: the overview's state, in its own window =======================================
S['k2'] = S['o-brief']

# ==== K03 Investor questions: the overview's inbox ===============================================================
S['k3'] = S['o-inbox']

# ==== K04 Two assistants, one record =============================================================================
OUTLOOK = 'For 2026, we now expect net revenue of $10.350 billion to $10.500 billion, a decline of 5% to 7%, from $11.000 billion to $11.150 billion in June.'
DRAFT_A = card({'id': 'qa-a', 'title': 'Q&A draft: the revised outlook', 'tier': 'Internal',
                'sub': 'For lululemon’s IR team · grounded in 2 sources',
                'quote': OUTLOOK,
                'rows': [{'ic': 'doc', 't': 'Q2 2026 earnings release', 'd': 'Sep 3, 2026 · page 2', 'id': 'qa-a-src'},
                         {'ic': 'doc', 't': 'Q1 2026 earnings release', 'd': 'Jun 4, 2026 · page 2'}],
                'acts': [{'label': 'Save to Diolog'}]})
SAVED_A = card({'id': 'qa-a2', 'title': 'Saved: Q&A draft, version 1', 'tier': 'Internal', 'sub': 'In lululemon’s record, for its IR team to review',
                'rows': [{'k': 'ok', 't': 'Their IR team can open it in their own assistant'}]})
S['k4-dana'] = frame('claude', 'dana', 'Q&A for the IR team', [
    user('Draft the Q&A answer on the revised outlook for lululemon’s IR team.'), tool('get_claims'), by(), DRAFT_A, by(), SAVED_A,
], ('Q2 earnings deck',))
DRAFT_B = card({'id': 'qa-b', 'title': 'Dana’s Q&A draft, version 1', 'tier': 'Internal',
                'sub': 'Saved to lululemon’s record by Dana Ruiz · in Claude',
                'quote': OUTLOOK,
                'rows': [{'ic': 'doc', 't': 'Q2 2026 earnings release', 'd': 'Sep 3, 2026 · page 2', 'id': 'qa-b-src'}],
                'acts': [{'label': 'Open the draft'}, {'label': 'Ask Dana to change it'}]})
DOCX = ('<div class="k-art k-docx" id="docx"><div class="k-art-h">' + ic('doc') + '<span><b>Q2 call Q&A · the outlook</b> · Draft, version 1</span><span class="pill">lululemon theme</span></div>'
        f'<div class="jdoc"><div class="jdoc-h"><span class="jlogo">{LOGO}</span><span>Q2 2026 earnings call · Q&A preparation</span></div>'
        '<p class="jq2">Q. What’s behind the revised full-year outlook?</p>'
        f'<p>A. {OUTLOOK}<sup>1</sup></p>'
        '<p class="jsrc">1 · Q2 2026 earnings release, Sep 3, 2026, page 2 · Q1 2026 earnings release, Jun 4, 2026, page 2</p></div></div>')
S['k4-marcus'] = frame('chatgpt', 'client', 'Call prep', [
    user('What did Dana prepare for the call?'), tool('list_documents'), by(), DRAFT_B, DOCX,
], ('Board pre-read', 'Q2 close'))

# ==== K05 The figure that didn't match ===========================================================================
REMARKS = ('<div class="k-art k-docx" id="remarks"><div class="k-art-h">' + ic('doc') + '<span><b>Q2 prepared remarks · CFO</b> · Draft 3, attached</span></div>'
           '<div class="jdoc"><p class="jdl">CFO remarks · paragraph 2</p>'
           '<p id="rem-p">Second-quarter net revenue was $2.42 billion, down 4%. <span id="rem-bad">Income from operations was $463.7 million</span>, and operating margin was 18.8%.</p></div></div>')
CHECK5 = card({'id': 'chk5', 'title': '1 figure to fix before this goes out', 'tier': 'Internal',
               'sub': 'Q2 prepared remarks · the draft you attached',
               'lead': lead([['Income from operations, draft', '$463.7M', 'bad'], ['Q2 earnings release', '$453.7M', 'ok']]),
               'rows': [{'k': 'warn', 't': 'Income from operations', 'd': 'The draft says $463.7 million. The release lululemon filed on Sep 3 says $453.7 million.', 'b': ['Figures differ', 'warn']},
                        {'k': 'ok', 't': '11 other figures match their source', 'b': ['Consistent', 'ok']}],
               'quote': '<span id="k5-quote">“Income from operations decreased 13% to $453.7 million and operating margin decreased 190 basis points to 18.8%.”</span><br><small>Q2 2026 earnings release · Sep 3, 2026 · page 1</small>',
               'acts': [{'label': 'Use $453.7 million'}, {'label': 'Open the source'}]})
CLEAN5 = card({'id': 'clean5', 'title': 'Nothing to fix: 12 of 12 figures match', 'tier': 'Internal',
               'sub': 'Q2 prepared remarks · draft 4, checked again',
               'lead': lead([['Figures checked', '12'], ['Match', '12', 'ok'], ['Differ', '0']])})
S['k5'] = frame('claude', 'dana', 'Prepared remarks check', [
    REMARKS, user('Check the CFO’s remarks against what lululemon has published.', file='Q2 prepared remarks, draft 3.docx', sub='Word document'),
    tool('run_check'), by(), CHECK5, by(), CLEAN5,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'))

# ==== K06 Analyst Q&A, prepared ==================================================================================
QA = card({'id': 'qa', 'title': 'Analyst Q&A pack: 14 likely questions', 'tier': 'Internal',
           'sub': 'lululemon Q2 2026 · each answer from published material · checked by Diolog',
           'lead': lead([['Questions', '14'], ['Answered from the record', '14', 'ok'], ['Sources', '4']]),
           'rows': [{'ic': 'q', 't': 'Why did comparable sales fall 9% in Q2?', 'd': 'Q2 release, page 1', 'b': ['Checked', 'ok']},
                    {'ic': 'q', 't': 'What’s in the revised full-year outlook?', 'd': 'Q2 release, page 2', 'b': ['Checked', 'ok']},
                    {'ic': 'q', 't': 'How much did tariff refunds add to margin?', 'd': 'Q2 release, page 1', 'b': ['Checked', 'ok']},
                    {'ic': 'q', 't': 'How fast is international revenue growing?', 'd': 'Q2 release, page 1', 'b': ['Checked', 'ok'], 'hide': True}],
           'acts': [{'label': 'Open the pack'}, {'label': 'Save to Diolog'}],
           'reason': 'Saved to Diolog as a draft. Nothing is sent.'})
PACK = ('<div class="k-art k-docx" id="pack"><div class="k-art-h">' + ic('doc') + '<span><b>Analyst Q&A pack · Q2 2026</b> · 14 questions</span><span class="pill">lululemon theme</span></div>'
        f'<div class="jdoc"><div class="jdoc-h"><span class="jlogo">{LOGO}</span><span>Q2 2026 earnings call · analyst Q&A</span></div>'
        '<p class="jq2">1. Why did comparable sales fall in the second quarter?</p>'
        '<p>Comparable sales decreased 9%, or 10% on a constant dollar basis, with the Americas down 12% and international down 3%.<sup>1</sup></p>'
        '<p class="jq2">2. What’s in the revised full-year outlook?</p>'
        '<p>We now expect 2026 net revenue of $10.350 billion to $10.500 billion and diluted EPS of $9.48 to $9.73, which includes $0.86 per share from tariff refunds recognized in the second quarter.<sup>1</sup></p>'
        '<p class="jsrc">1 · Q2 2026 earnings release, Sep 3, 2026, pages 1 and 2</p></div></div>')
S['k6'] = frame('claude', 'dana', 'Analyst Q&A, Q2', [
    user('Draft the analyst Q&A pack for lululemon’s Q2 call.'), tool('search_record'), tool('get_claims'), by(), QA, PACK,
], ('Q2 earnings deck', 'Post-earnings brief'))

# ==== K07 A new document, in the record ==========================================================================
FILED = card({'id': 'filed', 'title': 'Added to lululemon’s record: the Q2 release draft', 'tier': 'Unreleased', 'tk': 'blue',
              'sub': 'Supplied by Dana Ruiz · Published once lululemon files it',
              'rows': [{'ic': 'doc', 't': 'Q2 2026 earnings release, draft.docx', 'd': '9 pages · version 1', 'b': ['Unreleased', 'blue'], 'id': 'f-doc'},
                       {'ic': 'clock', 't': 'Becomes Published once it’s filed', 'd': 'Sep 3, 2026, with the Form 8-K', 'id': 'f-when'}],
              'acts': [{'label': 'Open the record', 'ic': 'panel'}],
              'reason': 'Guardian’s search now reads it beside the filings, labeled as supplied by you.'})
USE = card({'id': 'use', 'title': 'What the draft release says about the outlook', 'tier': 'Unreleased', 'tk': 'blue',
            'sub': 'From the record · 1 source',
            'quote': '“For 2026, the Company now expects net revenue to be in the range of $10.350 billion to $10.500 billion, representing a decline of 5% to 7%.”',
            'rows': [{'ic': 'doc', 't': 'Q2 2026 earnings release, draft', 'd': 'Supplied by Dana Ruiz · page 2', 'b': ['Unreleased', 'blue'], 'id': 'u-src'}]})
S['k7'] = frame('claude', 'dana', 'Q2 release draft', [
    user('File this in lululemon’s record.', file='Q2 2026 earnings release, draft.docx', sub='Word document · 9 pages'), tool('view_record'), by(), FILED,
    user('What does the draft say about the outlook?'), tool('search_record'), by(), USE,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'))

# ==== K08 Last quarter's deck, this quarter's figures ============================================================
LINKED = card({'id': 'linked', 'title': 'Your Q2 deck: 24 figures, each linked to its source', 'tier': 'Internal',
               'sub': 'Claude made the slides. Diolog supplied the theme and the figures, and ran the check.',
               'lead': lead([['Figures linked', '24'], ['Match', '24', 'ok'], ['Structure', 'Q1 deck, V12']]),
               'rows': [{'k': 'ok', 't': 'If a source changes, Diolog flags this draft', 'd': 'Every figure stays linked to the filing it came from'}],
               'acts': [{'label': 'Save to Diolog'}, {'label': 'Open the deck'}]})
S['k8'] = frame('claude', 'dana', 'Q2 earnings deck', [
    user('Build the Q2 earnings deck from our Q1 deck.'), tool('get_document'), tool('get_figures'), tool('get_theme'),
    say('Same structure as Q1, with the Q2 figures, in lululemon’s theme.'), deck('Q1', 'from'), tool('run_check'), by(), LINKED,
], ('Post-earnings brief', 'Analyst Q&A, Q2'))

# ==== K09 Holders, checked against the newest filings ============================================================
# Schedule 13G/A filings on lululemon: The Vanguard Group 10.05% (filed Sep 10, 2024) and no shares (Mar 27, 2026);
# Vanguard Capital Management 7.22% (13G, Apr 28, 2026); BlackRock, Inc. 7.6% (Jan 26, 2024) and 5.8% (Oct 27, 2026);
# Capital World Investors 5.7% (13G, Nov 13, 2026).
OWN = card({'id': 'own', 'title': '2 of 3 holders in this write-up are out of date', 'tier': 'Published', 'tk': 'green',
            'sub': 'Ownership check · each holder against their newest filing',
            'lead': lead([['In the write-up', '3'], ['Match', '1', 'ok'], ['Out of date', '2', 'warn']]),
            'rows': [{'k': 'warn', 't': 'The Vanguard Group', 'd': 'The write-up says 10.05%. Its Schedule 13G/A filed Mar 27, 2026 reports no shares.', 'b': ['Out of date', 'warn'], 'id': 'o-r1'},
                     {'k': 'warn', 't': 'BlackRock, Inc.', 'd': 'The write-up says 7.6%. The Schedule 13G/A filed Oct 27, 2026 says 5.8%.', 'b': ['Out of date', 'warn'], 'id': 'o-r2'},
                     {'k': 'ok', 't': 'Capital World Investors matches its newest filing', 'b': ['Consistent', 'ok']}],
            'acts': [{'label': 'Update the 2 lines'}, {'label': 'Open ownership', 'ic': 'panel'}]})
OWN_OK = card({'id': 'ownok', 'title': 'All 3 holders now match their newest filing', 'tier': 'Published', 'tk': 'green',
               'sub': 'LULU holders note · version 2 · Vanguard Capital Management in at 7.22%', 'lead': lead([['In the write-up', '3'], ['Match', '3', 'ok'], ['Out of date', '0']])})
OVIEW = (f'<div class="pv"><p class="crumb">Ownership</p><h4>lululemon holders</h4><p class="meta">From SEC EDGAR · newest filing first</p>'
         + box('Newest holder filings', '4', prow('Capital World Investors · Schedule 13G', '5.7% · as of Sep 30 · filed Nov 13', '12 days old')
               + prow('BlackRock, Inc. · Schedule 13G/A', '5.8% · as of Sep 30 · filed Oct 27', '29 days old', 'ov-cedar')
               + prow('Vanguard Capital Management · Schedule 13G', '7.22% · as of Mar 31 · filed Apr 28', '211 days old', 'ov-lark')
               + prow('The Vanguard Group · Schedule 13G/A', 'No shares · filed Mar 27', '243 days old'))
         + '<p class="pv-foot">Every figure carries its filing date and the period it reports.</p></div>')
S['k9'] = frame('claude', 'dana', 'Ownership note', [
    user('Check this ownership write-up.', file='LULU holders note, June.docx', sub='Word document'), tool('get_holder_filings'), tool('run_check'), by(), OWN, by(), OWN_OK,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'), panel=OVIEW, ptitle='Ownership')

# ==== K10 Investor calls, filed and recalled =====================================================================
CALL = card({'id': 'call', 'title': 'A holder call is filed, and 6 questions wait for review', 'tier': 'Internal',
             'sub': 'Kept Internal · investors matched',
             'rows': [{'ic': 'users', 't': 'A top-20 holder · 2 people', 'd': 'Matched to lululemon’s investor records'},
                      {'ic': 'q', 't': '6 questions, answers and responses', 'd': 'Each kept with its timestamp'}],
             'acts': [{'label': 'Review in the calls view', 'ic': 'panel'}],
             'reason': 'Confirming the call checks lululemon’s answers for anything it hasn’t published.'})
CVIEW = (f'<div class="pv"><p class="crumb">Calls</p><h4>Holder call · Sep 10, 2026</h4><p class="meta">Filed by Dana Ruiz · Internal · 2 investors matched</p>'
         + box('Questions', '6', prow('What does the new range assume for the Americas?', 'Answered by management', '06:12', 'cv-1')
               + prow('Are further tariff refunds in the outlook?', 'Answered by management', '11:40', 'cv-2')
               + prow('How is international growth holding up?', 'Answered by management', '18:05')
               + prow('3 more', '', ''))
         + '<div class="pv-acts"><span class="dc-btn pri">Confirm the call</span></div><p class="pv-foot">The words stay in Diolog. An assistant sees counts.</p></div>')
S['k10'] = frame('claude', 'dana', 'Holder call', [
    user('File this call.', file='Holder call, Sep 10.txt', sub='Transcript · 34 minutes'), tool('file_transcript'), by(), CALL,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'), panel=CVIEW, ptitle='Calls')

# ==== Round 3: shorter prompts, tool lines that run on screen, the call recalled ===================================
def run(name, status):
    return tool(name, done=False, run=status)


S['r3-deck'] = frame('claude', 'dana', 'Q2 earnings deck', [
    user('Build our Q2 earnings deck the way we did Q1.'), run('search_record', 'Reading lululemon’s record…'), by(), MATERIALS,
    tool('get_theme'), say('Here’s Q2 on the Q1 deck’s structure, in lululemon’s theme. Diolog supplied the figures.'), deck('Q1', 'from'),
    tool('run_check'), by(), FIGCHECK, by(), FIXED,
], REC_D[1:])

S['r3-brief'] = S['o-brief']          # the step, Claude's question, the running tool, the brief

S['r3-newdoc'] = frame('claude', 'dana', 'Q2 release draft', [
    user('File this in lululemon’s record.', file='Q2 2026 earnings release, draft.docx', sub='Word document · 9 pages'), run('view_record', 'Adding it to lululemon’s record…'), by(), FILED,
    user('What does the draft say about the outlook?'), run('search_record', 'Searching lululemon’s record…'), by(), USE,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'))

S['r3-qa'] = frame('claude', 'dana', 'Analyst Q&A, Q2', [
    user('Draft the analyst Q&A pack for lululemon’s Q2 call.'), run('search_record', 'Reading the filings and past releases…'), by(), QA, PACK,
], ('Q2 earnings deck', 'Post-earnings brief'))

S['r3-own'] = frame('claude', 'dana', 'Ownership note', [
    user('Check this ownership write-up.', file='LULU holders note, June.docx', sub='Word document'),
    run('get_holder_filings', 'Reading the newest 13G filings…'), tool('run_check'), by(), OWN, by(), OWN_OK,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'), panel=OVIEW, ptitle='Ownership')

S['r3-inbox'] = frame('claude', 'dana', 'Investor questions', [
    user('What’s waiting in lululemon’s inbox?'), tool('list_questions'), by(), QCOUNT,
    user('Draft our answer on the outlook from the Q2 and Q1 releases.'), run('get_claims', 'Reading the Q2 and Q1 releases…'), by(), ANSWER, by(), SAVED,
], ('Q2 earnings deck', 'Post-earnings brief', 'Analyst Q&A, Q2'), panel=QVIEW, ptitle='Questions and replies')

RECALL = card({'id': 'recall', 'title': 'This holder’s last call: 6 questions, Sep 10', 'tier': 'Internal',
               'sub': 'From the call Dana Ruiz filed · confirmed in the calls view',
               'lead': lead([['Questions', '6'], ['Investors on the call', '2'], ['Answered on the call', '6', 'ok']]),
               'rows': [{'ic': 'clock', 't': 'Sep 10, 2026 · 34 minutes', 'd': 'Management for lululemon', 'id': 'rc-when'}],
               'acts': [{'label': 'Open in the calls view', 'ic': 'panel'}],
               'reason': 'The questions and answers open only in Diolog’s view.'})
CVIEW2 = (f'<div class="pv"><p class="crumb">Calls</p><h4>Holder call · Sep 10, 2026</h4><p class="meta">Filed by Dana Ruiz · Internal · confirmed</p>'
          + box('Questions', '6', prow('What does the new range assume for the Americas?', 'Answered by management', '06:12', 'cv-1')
                + prow('Are further tariff refunds in the outlook?', 'Answered by management', '11:40', 'cv-2')
                + prow('How is international growth holding up?', 'Answered by management', '18:05', 'cv-3')
                + prow('3 more', '', ''))
          + '<p class="pv-foot">The words stay in Diolog. An assistant sees counts.</p></div>')
S['r3-calls'] = frame('claude', 'dana', 'Holder call', [
    user('File this call.', file='Holder call, Sep 10.txt', sub='Transcript · 34 minutes'), run('file_transcript', 'Matching the investors on the call…'), by(), CALL,
    user('What did they ask on their last call?'), run('search_record', 'Searching lululemon’s record…'), by(), RECALL,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'), panel=CVIEW2, ptitle='Calls')

S['r3-k4-dana'] = frame('claude', 'dana', 'Q&A for the IR team', [
    user('Draft the Q&A answer on the revised outlook for lululemon’s IR team.'), run('get_claims', 'Reading the Q2 release…'), by(), DRAFT_A, by(), SAVED_A,
], ('Q2 earnings deck',))

S['r3-k5'] = frame('claude', 'dana', 'Prepared remarks check', [
    REMARKS, user('Check the CFO’s remarks against what lululemon has published.', file='Q2 prepared remarks, draft 3.docx', sub='Word document'),
    run('run_check', 'Checking 12 figures against the release…'), by(), CHECK5, by(), CLEAN5,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'))

S['r3-k8'] = frame('claude', 'dana', 'Q2 earnings deck', [
    user('Build our Q2 earnings deck from the Q1 deck.'), run('get_document', 'Taking the Q1 deck’s structure…'), tool('get_figures'), tool('get_theme'),
    say('Same structure as Q1, with the Q2 figures, in lululemon’s theme.'), deck('Q1', 'from'), tool('run_check'), by(), LINKED,
], ('Post-earnings brief', 'Analyst Q&A, Q2'))

# ==== Round 3b (25 Nov): the clips run 20 to 24 s, so each workflow goes one step further ==========================
S['r3-k2'] = frame('claude', 'dana', 'lululemon Q2 results', [
    by(), STEP, say('lululemon’s Q2 earnings release is available. Want me to prepare your post-earnings brief?'),
    run('get_claims', 'Reading the Q2 release…'), by(), BRIEF,
    run('search_record', 'Drafting the Q&A pack from the brief…'), by(), QA,
], ('Q2 earnings deck', 'Analyst Q&A, Q2', 'Ownership note'))

REMARKS_FIXED = ('<div class="k-art k-docx" id="remarks2"><div class="k-art-h">' + ic('doc') + '<span><b>Q2 prepared remarks · CFO</b> · Draft 4, corrected</span></div>'
                 '<div class="jdoc"><p class="jdl">CFO remarks · paragraph 2</p>'
                 '<p>Second-quarter net revenue was $2.42 billion, down 4%. <span id="rem-fixed">Income from operations was $453.7 million</span>, and operating margin was 18.8%.</p></div></div>')
S['r3-k5b'] = frame('claude', 'dana', 'Prepared remarks check', [
    REMARKS, user('Check the CFO’s remarks against what lululemon has published.', file='Q2 prepared remarks, draft 3.docx', sub='Word document'),
    run('run_check', 'Checking 12 figures against the release…'), by(), CHECK5, by(), CLEAN5, REMARKS_FIXED,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'))

QA_SAVED = card({'id': 'qasaved', 'title': 'Saved as draft version 1 of the Q2 Q&A pack', 'tier': 'Internal',
                 'sub': '14 questions · 4 sources · in lululemon’s record',
                 'rows': [{'k': 'ok', 't': '14 answers match their published sources', 'b': ['Consistent', 'ok'], 'id': 'qs-ok'},
                          {'ic': 'users', 't': 'Their IR team can open it', 'd': 'In Claude, ChatGPT or the Diolog app'}],
                 'reason': 'It waits in Diolog as a draft. Nothing has been sent.'})
S['r3-k6'] = frame('claude', 'dana', 'Analyst Q&A, Q2', [
    user('Draft the analyst Q&A pack for lululemon’s Q2 call.'), run('search_record', 'Reading the filings and past releases…'), by(), QA, PACK,
    run('save_document_draft', 'Saving the pack to Diolog…'), by(), QA_SAVED,
], ('Q2 earnings deck', 'Post-earnings brief'))

RVIEW = (f'<div class="pv"><p class="crumb">The record</p><h4>lululemon’s record</h4><p class="meta">Sources and the current version of each document</p>'
         + box('Earnings materials', '4', prow('Q2 2026 earnings release, draft', 'Supplied by Dana Ruiz · version 1 · Published once filed', '<span class="badge blue">Unreleased</span>', 'rv-script')
               + prow('Q1 2026 earnings release', 'Form 8-K, Exhibit 99.1 · Jun 4, 2026', '<span class="badge ok">Published</span>')
               + prow('Q2 2026 earnings deck', 'V3 · replaces V2 of Sep 1', '<span class="badge ok">Current</span>')
               + prow('Q1 2026 Form 10-Q', 'Jun 4, 2026', '<span class="badge ok">Published</span>'))
         + box('Sources', '2', prow('SEC EDGAR', 'Loaded 7:02am · newest filing Aug 13', '<span class="badge ok">Current</span>') + prow('IR shared drive', 'Loaded 6:30am', '<span class="badge ok">Current</span>'))
         + '<p class="pv-foot">A search returns the current version of each document, and says what it replaced.</p></div>')
S['r3-k7'] = frame('claude', 'dana', 'Q2 release draft', [
    user('File this in lululemon’s record.', file='Q2 2026 earnings release, draft.docx', sub='Word document · 9 pages'), run('view_record', 'Adding it to lululemon’s record…'), by(), FILED,
    user('What does the draft say about the outlook?'), run('search_record', 'Searching lululemon’s record…'), by(), USE,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'), panel=RVIEW, ptitle='The record')

DECK_SAVED = card({'id': 'decksaved', 'title': 'Saved as draft version 1 of the Q2 earnings deck', 'tier': 'Internal',
                   'sub': '12 slides · 24 figures linked · in lululemon’s record',
                   'rows': [{'k': 'ok', 't': 'All 24 figures match the record', 'b': ['Consistent', 'ok'], 'id': 'ds-ok'},
                            {'ic': 'doc', 't': 'If a filing changes, Diolog flags this draft', 'd': 'Every figure stays linked to its source'}],
                   'reason': 'It waits in Diolog as a draft. Presenting it is still approved in Diolog.'})
S['r3-k8b'] = frame('claude', 'dana', 'Q2 earnings deck', [
    user('Build our Q2 earnings deck from the Q1 deck.'), run('get_document', 'Taking the Q1 deck’s structure…'), tool('get_figures'), tool('get_theme'),
    say('Same structure as Q1, with the Q2 figures, in lululemon’s theme.'), deck('Q1', 'from'), tool('run_check'), by(), LINKED,
    run('save_document_draft', 'Saving the deck to Diolog…'), by(), DECK_SAVED,
], ('Post-earnings brief', 'Analyst Q&A, Q2'))

CVIEW_BOTH = ('<div id="cv-a">' + CVIEW + '</div><div id="cv-b" style="display:none">' + CVIEW2 + '</div>')
S['r3-k10'] = frame('claude', 'dana', 'Holder call', [
    user('File this call.', file='Holder call, Sep 10.txt', sub='Transcript · 34 minutes'), run('file_transcript', 'Matching the investors on the call…'), by(), CALL,
    user('What did they ask on their last call?'), run('search_record', 'Searching lululemon’s record…'), by(), RECALL,
], ('Q2 earnings deck', 'Analyst Q&A, Q2'), panel=CVIEW_BOTH, ptitle='Calls')

# ---- write ------------------------------------------------------------------------------------------------------
# US English and product truth (the second factor is an authenticator code, never a passkey), and every name the
# series' earlier fictional scenario used, so none survives on a screen. Substrings, as the source checked them.
BANNED = ['passkey', 'Face ID', 'Touch ID', 'Iris', 'Meridian', 'organis', 'colour', 'licenc', 'labelled',
          'Juniper', 'JDGR', 'Marcus', 'Laura Bennett', 'Northfield', 'Larkspur', 'Cedar Ridge', 'EBITDA', 'restaurant', 'Q3']

if __name__ == '__main__':
    out = E.write(S, HERE, substrings=BANNED)
    print(f'{len(S)} states written to {out}')
