#!/usr/bin/env python3
"""Start a demo video series from the skill's starter kit.

    new_series.py <dir> [--fetch]                 # the kit into <dir>/_kit/, the example series into <dir>/
    new_series.py <dir> --reference [--fetch]     # the same, with the reference series (the Guardian launch films)
    new_series.py --self-test

Copies kit/runtime and kit/engine (plus duck.py, which the score imports) into <dir>/_kit/, so the series owns its
fork of the kit, and kit/example (series.json, states.py, films.py, lines.json, respell.json, lockup.css, marks/)
into <dir>/. Refuses to overwrite an existing file. --fetch downloads the three files the kit does not ship, pinned:
Inter and Inter Tight (variable, Latin, SIL Open Font License, from Fontsource) into assets/fonts/, and GSAP 3.15.0
into assets/vendor/. Without --fetch it prints the commands.

Then: python3 states.py, open states/index.html, python3 films.py, and build each film with _kit/engine/build.py.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent / 'kit'
# The exact files the source series rendered with (Google Fonts' Latin subsets, matched by MD5), so text sets the same
FETCH = [
    ('assets/fonts/Inter.woff2', 'https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2'),
    ('assets/fonts/InterTight.woff2', 'https://fonts.gstatic.com/s/intertight/v9/NGSwv5HMAFg6IuGlBNMjxLsH8ahuQ2e8.woff2'),
    ('assets/vendor/gsap.min.js', 'https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js'),
]


def copy_tree(src, dst):
    for f in sorted(src.rglob('*')):
        if f.is_dir() or '__pycache__' in f.parts:
            continue
        out = dst / f.relative_to(src)
        if out.exists():
            sys.exit(f'{out} exists; new_series.py never overwrites a series file')
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)


def create(target, fetch, reference=False):
    target = Path(target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    copy_tree(KIT / 'runtime', target / '_kit' / 'runtime')
    copy_tree(KIT / 'engine', target / '_kit' / 'engine')
    copy_tree(KIT / 'site', target / '_kit' / 'site')
    for helper in ('duck.py', 'delivery.py'):          # the score imports duck; render.py imports delivery
        if (target / '_kit' / 'engine' / helper).exists():
            sys.exit(f'{helper} already in the series kit')
        shutil.copy2(HERE / helper, target / '_kit' / 'engine' / helper)
    copy_tree(KIT / ('reference' if reference else 'example'), target)
    extra = [tuple(x) for x in json.loads((target / 'series.json').read_text()).get('fetch', [])]
    for rel, url in FETCH + extra:
        out = target / rel
        if fetch:
            out.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(url, timeout=60) as r:
                data = r.read()
            if len(data) < 10_000:
                sys.exit(f'{url} returned {len(data)} bytes; expected a font or a script')
            out.write_bytes(data)
            print(f'fetched {rel} ({len(data):,} bytes)')
        else:
            print(f'curl -sL --fail -o {out} {url}')
    print(f'series started in {target}')
    return target


def self_test():
    with tempfile.TemporaryDirectory() as d:
        s = create(Path(d) / 'series', fetch=False)
        for script in ('states.py', 'films.py'):
            r = subprocess.run([sys.executable, script], cwd=s, capture_output=True, text=True)
            assert r.returncode == 0, f'{script} failed: {r.stderr[-800:]}'
        idx = (s / 'states' / 'index.html').read_text()
        assert 'id="i-mark"' in idx and 'id="i-doc"' in idx, 'the preview sprite lacks the product mark or the icons'
        o, k = (json.loads((s / 'films' / f / 'plan.json').read_text()) for f in ('O', 'K01'))
        o_len, k_len = sum(x['dur'] for x in o['scenes']), sum(x['dur'] for x in k['scenes'])
        assert [x['id'] for x in o['scenes']] == ['intro', 'check', 'outro'], o['scenes']
        assert 28 <= o_len <= 110 and 20 <= k_len <= 25, (o_len, k_len)
        assert o['lockbar'] is False and k['lockbar'] is True
        steps = json.loads((s / 'films' / 'K01' / 'steps.json').read_text())['clip']
        last = max(steps, key=lambda x: x[0])
        assert last[1] == 'frame' and last[0] <= k_len - 3.2, f'the short does not end on a settling push: {last}'
        assert any(b[1] == 'pop' for b in k['scenes'][0]['sfx']), 'no card landing carried a pop'
        assert (s / 'films' / 'O' / 'compositions' / 'intro.html').read_text().count("K3.stage('intro'") == 1
        try:
            create(s, fetch=False)
            raise AssertionError('a second create overwrote the series')
        except SystemExit as e:
            assert 'never overwrites' in str(e)
        # the length gate refuses a short outside its range before writing anything
        cfg = json.loads((s / 'series.json').read_text())
        cfg['lengths']['short'] = [22, 25]
        (s / 'series.json').write_text(json.dumps(cfg))
        r = subprocess.run([sys.executable, 'films.py'], cwd=s, capture_output=True, text=True)
        assert r.returncode != 0 and 'outside 22-25 s' in r.stderr, r.stderr[-400:]
    print('new_series: 10 checks passed')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--self-test']:
        self_test()
    elif a and not a[0].startswith('--'):
        create(a[0], '--fetch' in a, '--reference' in a)
    else:
        sys.exit(__doc__.split('\n\n')[1])
