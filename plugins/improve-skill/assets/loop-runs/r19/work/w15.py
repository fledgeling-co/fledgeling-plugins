"""A hem the right WIDTH, not just the right depth.

w14's flat hem lands the trough (hem30 0.788 against C2's 0.765) and then refuses to let
go: it is still at 0.86 at u=12 and only reaches board at u=16-20, where C2 is back at 0.95
by u=8. An 18-wide stroke through a sigma-5 blur is a 14px half-width; C2's hem is a 4px
one. A wash that broad is not the feature - it is the feature smeared over four times its
extent, and it costs a 32px false positive in every variant precisely because its own
outer slope becomes an edge.

Also worth having in the record: C2's hem is not uniform along the blade. Leading 0.688,
middle 0.642, trailing 1.030 - it is deep over the first two thirds and simply ABSENT at
the trailing end, which is the opposite ramp to round 7's front seat. So a tapered hem
that dies before the trailing end, not a flat one and not seatRamp's.

Sweep width, blur and opacity together against the shape, and read the 32/16px edge sets
as the consequence.
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


def variant(sigma, width, paint):
    f = FILT_ANCHOR + """
  <filter id="hemBlur" x="-40%%" y="-40%%" width="180%%" height="180%%">
    <feGaussianBlur stdDeviation="%.1f"/>
  </filter>""" % sigma
    g = ANCHOR + """
    <g clip-path="url(#roughSide)" filter="url(#hemBlur)">
      <path d="{open_poly(CHAIN_UPPER)}" fill="none" stroke="%s"
            stroke-width="%.1f" stroke-linecap="round"/>
    </g>""" % (paint, width)
    return f, g


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


def backprof(c, g, out=90, dark=0.45):
    (x0, y0), (ax, ay) = axis(c)
    dx, dy = -ay, ax
    if dy > 0:
        dx, dy = -dx, -dy
    D = g < dark
    rows = []
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
    m = np.median(np.array(rows), axis=0)
    return m / np.median(m[60:88])


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


def build(name, sigma, width, paint):
    f, g = variant(sigma, width, paint)
    src = SRC.replace(FILT_ANCHOR, f).replace(ANCHOR, g)
    assert src.count("hemBlur") == 2, name
    src = src.replace("ASSETS = pathlib.Path(__file__).resolve().parent",
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
refm = backprof(REFC, REFG)
BASEG = rgbgray(render("icon.svg", 1024))[1]


def report(tag, svg):
    c, g = rgbgray(render(svg, 1024))
    m = backprof(c, g)
    line = ("  %-14s trough %.3f (C2 %.3f)  u8 %.3f (C2 %.3f)  |resid|0-24 %.4f"
            % (tag, m[2:7].mean(), refm[2:7].mean(), m[8], refm[8], np.abs(m[:24] - refm[:24]).mean()))
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
    return m


keep = {"baseline": report("baseline", "icon.svg")}
for tag, sg, w, op in (("t8s25", 2.5, 8.0, 0.55), ("t10s30", 3.0, 10.0, 0.50),
                       ("t12s35", 3.5, 12.0, 0.45), ("t8s25_65", 2.5, 8.0, 0.65),
                       ("t10s30_62", 3.0, 10.0, 0.62)):
    keep[tag] = report(tag, build(tag, sg, w, '#332A1E" stroke-opacity="%.2f' % op))
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)

print("\nprofiles out from the back edge (C2 last)")
names = list(keep)
print("   u  " + "".join("%10s" % n for n in names) + "        C2")
for u in list(range(0, 13)) + [14, 16, 20]:
    print("  %3d " % u + "".join("%10.3f" % keep[n][u] for n in names) + "  %8.3f" % refm[u])
