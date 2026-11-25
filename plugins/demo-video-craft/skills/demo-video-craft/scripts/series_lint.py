#!/usr/bin/env python3
"""Three sweeps over a series' sources that a render cannot see.

    series_lint.py serif PATH... [--allow lockup.css]      fail on a serif family in any font declaration
    series_lint.py collisions --product frame.css product.html --film kit.css kit3.css
    series_lint.py retired --term "#C9D3E6" --term "Old Company" PATH...
    series_lint.py --self-test

serif: reads .css, .html, .js and .py files (CSS often lives in strings) and fails on any font or font-family value
naming a serif face (Times, Georgia, Newsreader, Garamond, Palatino, Iowan, Merriweather, Playfair, Lora), var(--serif),
or a bare serif. A chat mockup in a serif reads as a broken font; an owner asked twice for every serif to go, and one
survived on disk in the film kit after the note. --allow exempts a file that legitimately carries the brand's serif
wordmark (the lockup).

collisions: fails when the film CSS styles a class the product also uses, in a rule not scoped under a k- or k3-
class. A film class `.end` once turned every row end in the product's markup into a grey overlay.

retired: fails on any occurrence of a retired value or name: a colour, a size, an old scenario's company, ticker or
person. Hex values and anything with punctuation match exactly; words match case-insensitively as whole words. Run it
before every re-render after a change, over the kits, the plan generator, the screens, the pages and the site build.
Every subcommand prints file:line for each hit and exits 1 on any.
"""
import re
import sys
import tempfile
from pathlib import Path

SERIF = re.compile(r'\b(Times( New Roman)?|Georgia|Newsreader|Garamond|Palatino|Iowan( Old Style)?|Merriweather|Playfair( Display)?|Lora)\b'
                   r'|var\(--serif\)|(?<![\w-])serif\b')
FONT_DECL = re.compile(r'font(?:-family)?\s*:\s*([^;}{"\n]*(?:"[^"\n]*"[^;}{"\n]*)*)', re.I)
EXTS = {'.css', '.html', '.htm', '.js', '.py'}


def files(paths):
    for p in map(Path, paths):
        if p.is_dir():
            yield from (f for f in sorted(p.rglob('*')) if f.suffix in EXTS and f.is_file() and 'node_modules' not in f.parts)
        elif p.is_file():
            yield p


def serif(paths, allow=()):
    allow = {Path(a).resolve() for a in allow}
    hits = []
    for f in files(paths):
        if f.resolve() in allow:
            continue
        for n, line in enumerate(f.read_text(errors='replace').splitlines(), 1):
            for m in FONT_DECL.finditer(line):
                s = SERIF.search(m.group(1))
                if s:
                    hits.append(f'{f}:{n}: {s.group(0)} in "{m.group(0)[:80]}"')
    for h in hits:
        print(h)
    print(f'serif: {"PASS" if not hits else "FAIL"} ({len(hits)} serif declarations)')
    return 1 if hits else 0


def classes_used(text):
    out = set(re.findall(r'class\s*=\s*["\']([^"\']+)["\']', text))
    used = {c for group in out for c in group.split()}
    used |= set(re.findall(r'\.([A-Za-z_][\w-]*)', re.sub(r'url\([^)]*\)|\d\.\d+|https?://\S+', '', text)))
    return used


def rules(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    for m in re.finditer(r'([^{}]+)\{[^{}]*\}', css):
        sel = m.group(1).strip()
        if sel.startswith('@'):
            continue
        for part in sel.split(','):
            yield part.strip()


def collisions(product, film):
    used = set()
    for f in files(product):
        used |= classes_used(f.read_text(errors='replace'))
    hits = []
    for f in files(film):
        for sel in rules(f.read_text(errors='replace')):
            # The rule reaches the product's own markup only when no compound is a k- class and every compound's
            # classes are all product classes: ".jth.on" needs .jth, ".k-cf .dc-row" lives inside the film's frame.
            compounds = [re.findall(r'\.([A-Za-z_][\w-]*)', c) for c in re.split(r'\s+|>|\+|~', sel)]
            compounds = [c for c in compounds if c]
            if not compounds or any(x.startswith(('k-', 'k3')) for c in compounds for x in c):
                continue
            if all(all(x in used for x in c) for c in compounds):
                hits.append(f'{f.name}: "{sel}" reaches the product\'s own .{compounds[-1][-1]} outside any k- scope')
    hits = sorted(set(hits))
    for h in hits:
        print(h)
    print(f'collisions: {"PASS" if not hits else "FAIL"} ({len(hits)} unscoped film rules on product classes)')
    return 1 if hits else 0


def retired(terms, paths):
    pats = []
    for t in terms:
        if re.fullmatch(r"[\w ’'&.]+", t) and not t.startswith('#'):
            pats.append((t, re.compile(rf'(?<![\w]){re.escape(t)}(?![\w])', re.I)))
        else:
            pats.append((t, re.compile(re.escape(t), re.I if t.startswith('#') else 0)))
    hits = []
    for f in files(paths):
        for n, line in enumerate(f.read_text(errors='replace').splitlines(), 1):
            for t, p in pats:
                if p.search(line):
                    hits.append(f'{f}:{n}: {t}')
    for h in hits:
        print(h)
    print(f'retired: {"PASS" if not hits else "FAIL"} ({len(hits)} hits for {len(terms)} terms)')
    return 1 if hits else 0


def self_test():
    import contextlib
    import io
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / 'ok.css').write_text('.cf-say { font: 400 16px/1.6 var(--sans); }\n.t { font-family: "Inter", sans-serif; }\n/* a serif reads as broken */\n')
        (d / 'bad.css').write_text('.cf-word { font: 500 23px/1 var(--serif); }\n.k-end { font: 400 88px/1.08 "Newsreader", Georgia, serif; }\n')
        (d / 'bad.py').write_text("html = '<span style=\"font:600 36px/1 Georgia\">x</span>'\n")
        (d / 'lockup.css').write_text('.wm { font: 500 1em/1 "Newsreader", serif; }\n')
        (d / 'product.css').write_text('.dc-row { display: grid; } .end { color: red; } .win { x: 1 }\n')
        (d / 'film.css').write_text('.k-cf .dc-row { opacity: 1; }\n.end { position: absolute; }\n.k-win .win { a: 1 }\n.k-lockup { b: 2 }\n')
        (d / 'scenario.html').write_text('<p>Harbor Pine Foods (HPFD) beat; colour #c9d3e6 here</p>\n')
        res = []
        with contextlib.redirect_stdout(io.StringIO()) as out:
            res.append(('sans and a comment pass', serif([d / 'ok.css']) == 0))
            res.append(('three serif declarations fail', serif([d / 'bad.css', d / 'bad.py']) == 1 and out.getvalue().count(':') >= 3))
            res.append(('an allowed lockup file passes', serif([d / 'lockup.css', d / 'ok.css'], allow=[d / 'lockup.css']) == 0))
            res.append(('an unscoped film rule on a product class fails', collisions([d / 'product.css'], [d / 'film.css']) == 1
                        and '.end' in out.getvalue() and '.win' not in out.getvalue().split('collisions:')[0].split('.end')[-1]))
            res.append(('retired name, ticker and hex all hit', retired(["Harbor Pine Foods", "HPFD", '#C9D3E6'], [d / 'scenario.html']) == 1
                        and out.getvalue().count('scenario.html:1') == 3))
            res.append(('a word does not match inside another word', retired(['Dining'], [d / 'ok.css']) == 0))
    failed = [n for n, ok in res if not ok]
    print(f'series_lint: {len(res) - len(failed)}/{len(res)} checks passed' + (f'; failed: {failed}' if failed else ''))
    sys.exit(1 if failed else 0)


def main(a):
    if a == ['--self-test']:
        self_test()
    if not a:
        sys.exit(__doc__.split('\n\n')[1])
    cmd, rest = a[0], a[1:]
    if cmd == 'serif':
        allow = [rest[i + 1] for i, x in enumerate(rest) if x == '--allow']
        paths = [x for i, x in enumerate(rest) if x != '--allow' and (i == 0 or rest[i - 1] != '--allow')]
        sys.exit(serif(paths, allow))
    if cmd == 'collisions':
        if '--product' not in rest or '--film' not in rest:
            sys.exit('collisions --product FILES... --film FILES...')
        i, j = rest.index('--product'), rest.index('--film')
        prod = rest[i + 1:j] if i < j else rest[i + 1:]
        film = rest[j + 1:] if j > i else rest[j + 1:i]
        sys.exit(collisions(prod, film))
    if cmd == 'retired':
        terms = [rest[i + 1] for i, x in enumerate(rest) if x == '--term']
        paths = [x for i, x in enumerate(rest) if x != '--term' and (i == 0 or rest[i - 1] != '--term')]
        if not terms or not paths:
            sys.exit('retired --term TERM [--term TERM...] PATH...')
        sys.exit(retired(terms, paths))
    sys.exit(f'unknown subcommand {cmd}')


if __name__ == '__main__':
    main(sys.argv[1:])
