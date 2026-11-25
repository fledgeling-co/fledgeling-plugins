#!/usr/bin/env python3
"""Keep a video site's media URLs fresh without ever renaming a published file.

    site_urls.py version <site_dir> films/acme-K02-vo.mp4 assets/posters/acme-K02.webp
    site_urls.py check   <site_dir> [page.html ...] [--origin https://videos.example.com]
    site_urls.py --self-test

A published video keeps its file name, because someone may already link to it. A browser or CDN that cached the
old file under that name will keep serving it, so every page reference carries `?v=<first 10 hex of the file's
SHA-1>`: same name, new URL, fresh fetch. `version` prints the versioned path for each file, for a build script to
use.

`check` reads the built pages (every *.html under site_dir when none are named) and finds each quoted reference to
a media file (mp4, webm, mov, m4a, mp3, webp, jpg, jpeg, png, gif, vtt), including ones inside inline JSON. A
reference fails when the file is missing on disk, when it carries no ?v=, or when its ?v= is not the hash of the
file now on disk, which is what a page built before the last render looks like. Absolute URLs on --origin are
mapped onto site_dir; other absolute URLs are skipped and counted. Exit 0 only when every reference passes.
"""
import hashlib
import re
import sys
import tempfile
from pathlib import Path

MEDIA = r'(?:mp4|webm|mov|m4a|mp3|webp|jpe?g|png|gif|vtt)'
REF = re.compile(r'["\'(]((?:https?://[^"\'()\s]+?|/?[\w./-]+?)\.' + MEDIA + r')(\?v=([0-9a-f]+))?["\')]', re.I)


def file_hash(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()[:10]


def version(site, rel):
    f = Path(site) / rel.lstrip('/')
    if not f.exists():
        sys.exit(f'{rel} is missing under {site}')
    return f'{rel}?v={file_hash(f)}'


def check(site, pages, origin=None):
    site = Path(site)
    pages = [Path(p) for p in pages] or sorted(site.rglob('*.html'))
    fails, ok, skipped = [], 0, 0
    for page in pages:
        text = page.read_text(errors='replace')
        for m in REF.finditer(text):
            url, ver = m.group(1), m.group(3)
            if url.startswith('http'):
                if origin and url.startswith(origin.rstrip('/') + '/'):
                    url = url[len(origin.rstrip('/')):]
                else:
                    skipped += 1
                    continue
            disk = (site / url.lstrip('/')) if url.startswith('/') else (page.parent / url)
            where = f'{page.relative_to(site) if page.is_relative_to(site) else page}: {m.group(1)}'
            if not disk.exists():
                fails.append(f'{where} -> no such file')
            elif not ver:
                fails.append(f'{where} -> no ?v= (a cached copy under this name would be served)')
            elif ver != file_hash(disk):
                fails.append(f'{where}?v={ver} -> stale; the file on disk is ?v={file_hash(disk)} (rebuild the page)')
            else:
                ok += 1
    for f in fails:
        print('  FAIL ' + f)
    total = ok + len(fails)
    print(f'urls: {"PASS" if not fails and total else "FAIL"} {ok}/{total} references current'
          + (f', {skipped} off-site skipped' if skipped else '') + ('' if total else ' (no media references found)'))
    return 0 if total and not fails else 1


def self_test():
    import contextlib
    import io
    results = []
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        (t / 'films').mkdir()
        (t / 'films' / 'a.mp4').write_bytes(b'one')
        good = version(t, 'films/a.mp4')

        def gate(html, origin=None):
            (t / 'index.html').write_text(html)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = check(t, [], origin)
            return rc, buf.getvalue()

        rc, out = gate(f'<video src="/{good}"></video><script type="application/json">{{"src":"/{good}"}}</script>')
        results.append(('current hashes pass, JSON included', rc == 0 and '2/2' in out, out))
        rc, out = gate('<video src="/films/a.mp4"></video>')
        results.append(('an unversioned reference fails', rc == 1 and 'no ?v=' in out, out))
        (t / 'films' / 'a.mp4').write_bytes(b'two')          # a republish under the same name
        rc, out = gate(f'<video src="/{good}"></video>')
        results.append(('a page built before the republish fails as stale', rc == 1 and 'stale' in out, out))
        rc, out = gate('<img src="/films/gone.webp?v=0123456789">')
        results.append(('a missing file fails', rc == 1 and 'no such file' in out, out))
        fresh = version(t, 'films/a.mp4')
        rc, out = gate(f'<meta property="og:image" content="https://v.example.com/{fresh}">', 'https://v.example.com')
        results.append(('an on-origin absolute URL is checked', rc == 0 and '1/1' in out, out))
        rc, out = gate('<p>no media here</p>')
        results.append(('a page with no references is not a pass', rc == 1, out))
    failed = [n for n, ok, _ in results if not ok]
    for n, ok, out in results:
        if not ok:
            print(f'--- {n}\n{out}')
    print(f'self-test: {len(results) - len(failed)}/{len(results)} passed' +
          (f'; failed: {", ".join(failed)}' if failed else ''))
    sys.exit(1 if failed else 0)


def main():
    a = sys.argv[1:]
    if '--self-test' in a:
        self_test()
    if len(a) >= 2 and a[0] == 'version':
        for rel in a[2:]:
            print(version(a[1], rel))
        return
    if len(a) >= 2 and a[0] == 'check':
        origin = None
        if '--origin' in a:
            i = a.index('--origin')
            origin = a[i + 1]
            a = a[:i] + a[i + 2:]
        sys.exit(check(a[1], a[2:], origin))
    print(__doc__.split('\n\n')[0], file=sys.stderr)
    sys.exit(2)


if __name__ == '__main__':
    main()
