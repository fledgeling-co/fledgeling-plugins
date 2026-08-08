"""Which end of the blade does C2's hem die at, and can a taper put it there?

w15: stroke 8 through sigma 2.5 at 0.55 is the tight family's best fit - |resid| over the
first 24px falls 0.0529 -> 0.0278 and the recovery lands on C2's exactly, 0.947 at u=8
against 0.950, where the baseline is still at 0.977. It undershoots the trough (0.846
against 0.765) and the wider members buy that depth by over-running the recovery, which is
the wash failure again, so width wins over depth.

One thing left. C2's hem is not uniform: leading 0.688, middle 0.642, trailing 1.030 - deep
over two thirds and simply gone at the third, the OPPOSITE ramp to round 7's front seat,
which deepens toward the trailing end. A flat hem would lay occlusion along a stretch of
board C2 leaves open. So taper it - but the sign has to be measured, not assumed, because
the ray index runs along the hone axis and nothing says that is the blade's leading sense.
Build the taper both ways and see which one empties the third C2 leaves empty.
"""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r19/work")
SRC = pathlib.Path("build_icon.py").read_text()

FILT_ANCHOR = """  <filter id="seatShadow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>"""
ANCHOR = """    <g filter="url(#contactShadow)">
      <path d="{poly([(x + CONTACT_DX, y + CONTACT_DY) for x, y in SILHOUETTE])}" fill="#3C3327" fill-opacity="{CONTACT_OP}"/>
    </g>"""
GRAD = """  <linearGradient id="hemFall" x1="0" y1="0" x2="{BLADE_LEN}" y2="0"
                  gradientUnits="userSpaceOnUse" gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#332A1E" stop-opacity="%.2f"/>
    <stop offset="0.55" stop-color="#332A1E" stop-opacity="%.2f"/>
    <stop offset="1" stop-color="#332A1E" stop-opacity="%.2f"/>
  </linearGradient>
"""


def src_for(paint, grad):
    f = FILT_ANCHOR + """
  <filter id="hemBlur" x="-40%%" y="-40%%" width="180%%" height="180%%">
    <feGaussianBlur stdDeviation="2.5"/>
  </filter>""" + ("\n" + grad if grad else "")
    g = ANCHOR + """
    <g clip-path="url(#roughSide)" filter="url(#hemBlur)">
      <path d="{open_poly(CHAIN_UPPER)}" fill="none" stroke="%s"
            stroke-width="8.0" stroke-linecap="round"/>
    </g>""" % paint
    return SRC.replace(FILT_ANCHOR, f).replace(ANCHOR, g)


def rgbgray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return c, 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def render(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


def bil(g, x, y):
    x0, y0 = int(x), int(y)
    if x0 < 1 or y0 < 1 or x0 + 2 >= g.shape[1] or y0 + 2 >= g.shape[0]:
        return float("nan")
    fx, fy = x - x0, y - y0
    return float((g[y0, x0] * (1 - fx) + g[y0, x0 + 1] * fx) * (1 - fy)
                 + (g[y0 + 1, x0] * (1 - fx) + g[y0 + 1, x0 + 1] * fx) * fy)


def axis(c):
    warm = (c[..., 0] - c[..., 2] > 0.30) & (c[..., 0] - c[..., 1] > 0.15)
    ys, xs = np.nonzero(warm)
    x0, y0 = xs.mean(), ys.mean()
    u = np.stack([xs - x0, ys - y0])
    w, v = np.linalg.eigh(u @ u.T / len(xs))
    ax, ay = v[:, np.argmax(w)]
    return (x0, y0), ((ax, ay) if ax >= 0 else (-ax, -ay))


def backrays(c, g, out=90, dark=0.45):
    (x0, y0), (ax, ay) = axis(c)
    dx, dy = -ay, ax
    if dy > 0:
        dx, dy = -dx, -dy
    D = g < dark
    rows, ks = [], []
    for k in range(-24, 25):
        sx, sy = x0 + ax * k * 9.0 + dx * 40.0, y0 + ay * k * 9.0 + dy * 40.0
        if not (0 <= int(sx) < 1024 and 0 <= int(sy) < 1024) or not D[int(sy), int(sx)]:
            continue
        t = 0.0
        while t < 420 and (not (0 <= int(sy + dy * t) < 1024 and 0 <= int(sx + dx * t) < 1024)
                           or D[int(sy + dy * t), int(sx + dx * t)]):
            t += 1.0
        if t >= 420:
            continue
        bx, by = sx + dx * t, sy + dy * t
        row = [bil(g, bx + dx * u, by + dy * u) for u in range(out)]
        if not any(v != v for v in row):
            rows.append(row)
            ks.append(k)
    a = np.array(rows)
    a = a / np.median(np.median(a, axis=0)[60:88])
    ks = np.array(ks)
    th = [float(np.median(a[(ks >= lo) & (ks < hi)], axis=0)[2:7].mean())
          for lo, hi in ((-24, -8), (-8, 8), (8, 25))]
    return np.median(a, axis=0), th


def sobel(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def dilate(m, r=1):
    o = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


def rim(n, t=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u, v = (x - (n - 1) / 2) / ((n - 1) / 2), (y - (n - 1) / 2) / ((n - 1) / 2)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > t


def build(name, paint, grad):
    src = src_for(paint, grad).replace(
        "ASSETS = pathlib.Path(__file__).resolve().parent",
        "ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent")
    p = WORK / ("gen_%s.py" % name)
    p.write_text(src)
    subprocess.run(["python3", str(p)], check=True, capture_output=True, cwd=".")
    out = WORK / ("var_%s.svg" % name)
    out.write_bytes(pathlib.Path("icon.svg").read_bytes())
    return str(out)


REFIM = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")
REFC, REFG = rgbgray(REFIM.resize((1024, 1024), Image.LANCZOS))
REF = {s: rgbgray(REFIM.resize((s, s), Image.LANCZOS))[1] for s in (32, 16)}
refm, ref_th = backrays(REFC, REFG)
BASEG = rgbgray(render("icon.svg", 1024))[1]
print("C2   thirds %.3f %.3f %.3f   trough %.3f  u8 %.3f" % (*ref_th, refm[2:7].mean(), refm[8]))


def report(tag, svg):
    c, g = rgbgray(render(svg, 1024))
    m, th = backrays(c, g)
    line = ("  %-10s thirds %.3f %.3f %.3f  trough %.3f  u8 %.3f  |resid|0-24 %.4f  thirds-resid %.3f"
            % (tag, *th, m[2:7].mean(), m[8], np.abs(m[:24] - refm[:24]).mean(),
               sum(abs(a - b) for a, b in zip(th, ref_th))))
    for s in (32, 16):
        gg = rgbgray(render(svg, s))[1]
        keep = ~rim(s)
        ea, eb = (sobel(gg) > 0.10) & keep, (sobel(REF[s]) > 0.10) & keep
        pr = (ea & dilate(eb)).sum() / max(ea.sum(), 1)
        rc = (eb & dilate(ea)).sum() / max(eb.sum(), 1)
        line += " | %d FP %2d FN %2d f1 %.4f" % (s, (ea & ~dilate(eb)).sum(),
                                                 (eb & ~dilate(ea)).sum(),
                                                 2 * pr * rc / max(pr + rc, 1e-9))
    print(line + " | 1024 |d| %.4f" % np.abs(g - BASEG).mean())


report("baseline", "icon.svg")
report("flat55", build("hemflat", '#332A1E" stroke-opacity="0.55', None))
report("fade0to1", build("hemf01", "url(#hemFall)", GRAD % (0.62, 0.55, 0.00)))
report("fade1to0", build("hemf10", "url(#hemFall)", GRAD % (0.00, 0.55, 0.62)))
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)
