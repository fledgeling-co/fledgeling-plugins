#!/usr/bin/env python3
"""Print each narration line beside what is on screen while it plays, from a built film.

    sync_table.py films/O                 # after build.py (not --mute-only): timeline.json + steps.json
    sync_table.py --self-test

For every line it prints the absolute span, the scene it was placed in, and the on-screen events (typing, a send, a
tool line, a card landing, a press, a mark, a panel, a count) that fall inside the span, each at its film time. Run
it after any pace change, scene insert or new offset, and read it before the owner watches: the note "what the
narrator says doesn't line up with what's on screen" arrived right after a pace change in the source run.

Exit 1 when a line runs more than 0.1 s past the scene it was placed in, or two lines overlap. A line with no event
in its first 1.5 s is printed as a NOTE: a line should start on the frame it describes.
"""
import json
import sys
import tempfile
from pathlib import Path

SHOWN = {'type', 'send', 'tool', 'arrive', 'click', 'ink', 'inkTo', 'panel', 'unpanel', 'count', 'stream', 'drag', 'swap',
         'in', 'moveTo', 'grow', 'flow', 'enter', 'exit', 'label', 'text'}


def what(step):
    op, a = step[1], step[2] if len(step) > 2 else None
    if op == 'type':
        return f'type "{step[3][:34]}"'
    if op == 'tool':
        return f'tool "{(step[3] or [""])[0][:34]}"'
    if op == 'arrive':
        return f'arrive {step[3]}'
    if op == 'click':
        return 'press ' + (a.get('t') or a.get('s', '')) if isinstance(a, dict) else 'press'
    if op in ('ink', 'inkTo'):
        return f'{op} {step[3] if op == "ink" else step[3]}'
    if isinstance(a, str):
        return f'{op} {a}'
    return op


def table(film_dir):
    F = Path(film_dir)
    tl = json.loads((F / 'timeline.json').read_text())
    steps = json.loads((F / 'steps.json').read_text())
    events = []
    for sid, sc in tl['scenes'].items():
        for st in steps.get(sid, []):
            if st[1] in SHOWN:
                events.append((round(sc['start'] + st[0], 2), sid, what(st)))
    events.sort()
    lines = sorted(tl['lines'].items(), key=lambda kv: kv[1]['start'])
    if not lines:
        print(f'{F.name}: no narration placed (built with --mute-only?)')
        return 0
    bad = 0
    for k, (lid, ln) in enumerate(lines):
        sc = tl['scenes'][ln['scene']]
        sc_end = sc['start'] + sc['dur']
        print(f'{lid:5} {ln["start"]:6.2f}-{ln["end"]:6.2f}  {ln["scene"]} ({sc["start"]:.2f}-{sc_end:.2f})  "{ln["text"][:70]}"')
        inside = [e for e in events if ln['start'] - 0.3 <= e[0] <= ln['end']]
        for t, sid, w in inside:
            print(f'        {t:6.2f}  {w}')
        if ln['end'] > sc_end + 0.1:
            print(f'  FAIL  {lid} ends {ln["end"] - sc_end:.2f} s past its scene: lengthen the scene\'s hold or move the line')
            bad += 1
        if k + 1 < len(lines) and lines[k + 1][1]['start'] < ln['end'] + 0.2:
            print(f'  FAIL  {lid} and {lines[k + 1][0]} overlap or leave under 0.2 s between them')
            bad += 1
        if not any(ln['start'] - 0.3 <= e[0] <= ln['start'] + 1.5 for e in events):
            print(f'  NOTE  nothing changes on screen in the first 1.5 s of {lid}: does it start on the frame it describes?')
    print(f'sync: {"PASS" if not bad else "FAIL"} {len(lines) - bad}/{len(lines)} lines on their picture')
    return 1 if bad else 0


def self_test():
    with tempfile.TemporaryDirectory() as d:
        F = Path(d)
        tl = {'scenes': {'intro': {'start': 0, 'dur': 10}, 'check': {'start': 10, 'dur': 8}},
              'lines': {'v1': {'scene': 'intro', 'start': 0.1, 'end': 4.0, 'text': 'one'},
                        'v2': {'scene': 'check', 'start': 11.0, 'end': 15.0, 'text': 'two'}}}
        steps = {'intro': [[0.2, 'in', '#t0', {}]], 'check': [[0.9, 'arrive', '#w1', 0], [2.5, 'click', {'s': '.dc-btn', 't': 'Use 41.2%'}, {}]]}
        (F / 'timeline.json').write_text(json.dumps(tl))
        (F / 'steps.json').write_text(json.dumps(steps))
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = table(F)
        out = buf.getvalue()
        assert rc == 0 and 'press Use 41.2%' in out and 'sync: PASS 2/2' in out, out
        tl['lines']['v2']['end'] = 18.5
        (F / 'timeline.json').write_text(json.dumps(tl))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = table(F)
        assert rc == 1 and 'past its scene' in buf.getvalue(), buf.getvalue()
        tl['lines']['v2'].update(start=4.1, end=9.0, scene='intro')
        (F / 'timeline.json').write_text(json.dumps(tl))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = table(F)
        out = buf.getvalue()
        assert rc == 1 and 'overlap' in out and 'NOTE' in out, out
    print('sync_table: 3 checks passed')


if __name__ == '__main__':
    if sys.argv[1:] == ['--self-test']:
        self_test()
    elif len(sys.argv) == 2:
        sys.exit(table(sys.argv[1]))
    else:
        sys.exit(__doc__.split('\n\n')[1])
