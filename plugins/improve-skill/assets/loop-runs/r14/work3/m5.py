"""Where are the candidate's dark curl pixels, and what draws them?

Renders three variants and differences them so each dark region is attributed to
an element rather than guessed: full master, master with the curl's cast shadow
removed, master with the shaving removed entirely.
"""
import subprocess, pathlib, re, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128


def render_bytes(svg_text, size, tag):
    p = OUT / f'.v-{tag}.svg'
    p.write_text(svg_text)
    t = OUT / f'.v-{tag}-{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(p), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def to_gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


if __name__ == '__main__':
    svg = (A / 'icon.svg').read_text()
    # strip the curl's cast shadow group only
    m = re.search(r'<!-- the shaving\'s shadow.*?</g>', svg, re.S)
    print('shadow block found:', bool(m), len(m.group(0)) if m else 0)
    no_shadow = svg[:m.start()] + svg[m.end():]

    g_full = to_gray(render_bytes(svg, 1024, 'full'))
    g_nosh = to_gray(render_bytes(no_shadow, 1024, 'nosh'))

    box = (150, 160, 430, 420)
    x0, y0, x1, y1 = box
    p = g_full[y0:y1, x0:x1]
    dark = p < 0.40
    print(f'pixels below 0.40 in the curl box: {dark.sum()} ({dark.mean()*100:.1f}%)')
    ys, xs = np.nonzero(dark)
    print(f'  their bbox in 1024 coords: x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}')
    # how much of that darkness survives when the cast shadow is removed
    q = g_nosh[y0:y1, x0:x1]
    print(f'  same pixels without the cast shadow: mean {q[dark].mean():.4f} vs {p[dark].mean():.4f} with')
    print(f'  cast shadow contribution over the whole box: {(q-p).mean():+.4f}')
    # a coarse map, 14 rows of the box printed as a mean-per-cell grid
    h, w = p.shape
    cell = 20
    print('\n  box mean map (rows y=160.., cols x=150.., 20px cells):')
    for r in range(0, h - cell + 1, cell):
        row = ' '.join(f'{p[r:r+cell, c:c+cell].mean():.2f}' for c in range(0, w - cell + 1, cell))
        print(f'   y={y0+r:4d} {row}')
