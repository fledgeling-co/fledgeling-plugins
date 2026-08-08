"""How dark does each image's shaving actually get against the ground beside it?

Boxes are hand-checked against the transects in m3 so neither contains the block.
The question is the one prior-learning #1 asks: where is each material's dark end,
and does it keep its hue there.
"""
import subprocess, pathlib, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128


def render(svg, size, tag='c'):
    t = OUT / f'.{tag}{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def ref(size):
    return Image.open(A / 'icon-engineC-f5665d-2.png').convert('RGBA').resize((size, size), Image.LANCZOS)


def to_gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


def report(name, g, rgb, box, ground_box):
    x0, y0, x1, y1 = box
    p = g[y0:y1, x0:x1]
    gx0, gy0, gx1, gy1 = ground_box
    gnd = g[gy0:gy1, gx0:gx1].mean()
    qs = [np.percentile(p, q) for q in (0.5, 2, 5, 10, 25, 50, 90)]
    print(f'\n{name}: ground beside it {gnd:.4f}')
    print('  percentiles 0.5/2/5/10/25/50/90: ' + ' '.join(f'{v:.3f}' for v in qs))
    print(f'  min {p.min():.4f}  = ground {p.min()-gnd:+.4f}   ({(p.min()/gnd-1)*100:+.1f}%)')
    for d in (0.10, 0.15, 0.20, 0.30):
        print(f'  fraction below ground-{d:.2f}: {(p < gnd - d).mean()*100:5.1f}%')
    # hue at the dark end: mean RGB of the darkest 2% of the box
    sub = rgb[y0:y1, x0:x1]
    thr = np.percentile(p, 2)
    sel = sub[p <= thr]
    m = sel.mean(axis=0)
    mx, mn = m.max(), m.min()
    print(f'  darkest 2% mean rgb {m.round(1)}  sat (max-min)/max {((mx-mn)/max(mx,1e-6))*100:.1f}%')
    br = np.percentile(p, 98)
    selb = sub[p >= br]
    mb = selb.mean(axis=0)
    print(f'  brightest 2% mean rgb {mb.round(1)}  sat {((mb.max()-mb.min())/max(mb.max(),1e-6))*100:.1f}%')


if __name__ == '__main__':
    c = render(A / 'icon.svg', 1024)
    r = ref(1024)
    gc, gr = to_gray(c), to_gray(r)
    ca = np.asarray(c.convert('RGB'), dtype=np.float64)
    ra = np.asarray(r.convert('RGB'), dtype=np.float64)
    # candidate curl: verified block-free (block's left corner is right of x=440 above y=430)
    report('candidate curl', gc, ca, (150, 160, 430, 420), (560, 120, 700, 200))
    # reference ribbon: verified block-free from the transects
    report('reference ribbon', gr, ra, (170, 80, 400, 370), (560, 120, 700, 200))
