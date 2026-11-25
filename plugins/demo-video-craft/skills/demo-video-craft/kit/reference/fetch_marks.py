#!/usr/bin/env python3
"""Fetch the third-party marks the reference series shows, into marks/, rather than committing them.

    python3 fetch_marks.py          # writes marks/claude.svg, chatgpt.svg, lulu.svg, lulu-full.svg

- Claude: "Claude AI symbol.svg" on Wikimedia Commons (CC0), filled #D97757.
- ChatGPT: "ChatGPT-Logo.svg" on Wikimedia Commons (public domain, trademarked), in currentColor (#0D0D0D on screen).
- lululemon: the logo file linked from its corporate site's header. Its 10 paths are all #140F0F; the mark is the one
  path whose left edge sits at x < 18 (x 0-16.94), the other nine are the wordmark. The mark takes #D41935, the red of
  the company's colour logo, and the wordmark takes currentColor.

Each is a trademark of its owner, shown to name the company and products on screen; the site credits them. Exit 1 when
a source has moved or its shape changed, rather than writing a mark that looks wrong.
"""
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = 'demo-video-craft/0.2 (https://github.com/fledgeling-co/fledgeling-plugins)'   # Wikimedia refuses an example.com contact
SOURCES = {
    'claude': 'https://upload.wikimedia.org/wikipedia/commons/b/b0/Claude_AI_symbol.svg',
    'chatgpt': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/ChatGPT-Logo.svg',
    'lulu': 'https://corporate.lululemon.com/~/media/Images/L/Lululemon/logo/logo-black-full.svg',
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
        return r.read().decode('utf-8')


Q = "[\"']"   # the Commons files quote attributes with either mark


def paths(svg):
    return [' '.join(d.split()) for d in re.findall(r'<path\b[^>]*\bd=' + Q + r'([^"\']+)' + Q, svg)]


def viewbox(svg):
    return re.search(r'viewBox=' + Q + r'([^"\']+)' + Q, svg).group(1)


def svg(viewbox, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{body}</svg>\n'


def main():
    out = HERE / 'marks'
    out.mkdir(exist_ok=True)
    c = get(SOURCES['claude'])
    vb = viewbox(c)
    ds = paths(c)
    if not ds:
        sys.exit('claude: no paths in the Commons file; check the source')
    (out / 'claude.svg').write_text(svg(vb, ''.join(f'<path d="{d}" fill="#D97757"/>' for d in ds)))
    g = get(SOURCES['chatgpt'])
    vb = viewbox(g)
    ds = paths(g)
    if not ds:
        sys.exit('chatgpt: no paths in the Commons file; check the source')
    (out / 'chatgpt.svg').write_text(svg(vb, ''.join(f'<path d="{d}" fill="currentColor"/>' for d in ds)))
    lu = get(SOURCES['lulu'])
    ds = paths(lu)
    if len(ds) != 10:
        sys.exit(f'lulu: expected 10 paths in the logo file, found {len(ds)}; its shape changed')

    def left(d):
        xs = [float(x) for x in re.findall(r'[ML]\s*(-?[\d.]+)', d)]
        return min(xs) if xs else 999

    mark = [d for d in ds if left(d) < 18]
    word = [d for d in ds if left(d) >= 18]
    if len(mark) != 1:
        sys.exit(f'lulu: expected one mark path at x < 18, found {len(mark)}')
    (out / 'lulu.svg').write_text(svg('0 0 17 17', f'<path d="{mark[0]}" fill="#D41935"/>'))
    (out / 'lulu-full.svg').write_text(svg('0 0 120 17', f'<path d="{mark[0]}" fill="#D41935"/>'
                                           + ''.join(f'<path d="{d}" fill="currentColor"/>' for d in word)))
    print('marks/: claude.svg, chatgpt.svg, lulu.svg, lulu-full.svg')


if __name__ == '__main__':
    main()
