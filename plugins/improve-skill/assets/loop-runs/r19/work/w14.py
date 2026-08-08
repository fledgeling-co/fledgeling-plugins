"""The board behind the plane: does C2's occlusion hem vary along the blade, and what
opacity reproduces it?

w13, both images measured off their own hone axis and normalised by their own board, going
OUT from the plane's top-back edge:

    u        0     1     2     3     4     5     6     7     8    10
    C2    0.703 0.822 0.784 0.739 0.728 0.755 0.819 0.929 0.950 0.967
    ours  0.690 0.885 0.958 0.961 0.966 0.966 0.969 0.965 0.977 0.968

C2 has a trough - minimum 0.728 at u=4, back to board by u=8 - and ours is flat from u=2.
That is not a tuning difference. Round 7's seat band is CLIPPED TO truedSide by
construction, so by design our body has a seat on the side the shadow falls and none at
all on the side facing the light. The board behind a body is occluded from the sky by that
body whichever way the sun is; C2 shows it and we do not.

Two questions before authoring. Does C2's hem deepen toward the trailing end, the way its
front seat does (round 7 measured 0.66x leading, 0.41x trailing) - if so the hem wants the
existing seatRamp rather than a flat opacity. And what opacity puts our trough on C2's.
"""
import subprocess
import tempfile
import pathlib
import math
import re
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r19/work")
SRC = pathlib.Path("build_icon.py").read_text()

ANCHOR = """    <g filter="url(#contactShadow)">
      <path d="{poly([(x + CONTACT_DX, y + CONTACT_DY) for x, y in SILHOUETTE])}" fill="#3C3327" fill-opacity="{CONTACT_OP}"/>
    </g>"""


def hem(paint, width):
    return ANCHOR + """
    <g clip-path="url(#roughSide)" filter="url(#seatShadow)">
      <path d="{open_poly(CHAIN_UPPER)}" fill="none" stroke="%s"
            stroke-width="%.1f" stroke-linecap="round"/>
    </g>""" % (paint, width)


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
    return ((x0, y0), (ax, ay) if ax >= 0 else (-ax, -ay))


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
    return np.array(rows), np.array(ks)


def hemstat(c, g):
    a, ks = backrays(c, g)
    a = a / np.median(np.median(a, axis=0)[60:88])
    m = np.median(a, axis=0)
    thirds = []
    for lo, hi in ((-24, -8), (-8, 8), (8, 25)):
        sel = (ks >= lo) & (ks < hi)
        thirds.append(float(np.median(a[sel], axis=0)[2:7].mean()) if sel.sum() else float("nan"))
    return m, m[2:7].mean(), thirds


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


def build(name, extra):
    src = SRC.replace(ANCHOR, extra) if extra else SRC
    assert extra is None or src != SRC, name
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
REF32 = rgbgray(REFIM.resize((32, 32), Image.LANCZOS))[1]
REF16 = rgbgray(REFIM.resize((16, 16), Image.LANCZOS))[1]
BASEG = rgbgray(render("icon.svg", 1024))[1]

_, ref_t, ref_thirds = hemstat(REFC, REFG)
print("C2 hem trough (mean of u=2..6, own board = 1.000): %.3f" % ref_t)
print("   by position along the blade - leading / middle / trailing: %.3f  %.3f  %.3f"
      % tuple(ref_thirds))


def report(tag, svg):
    c, g = rgbgray(render(svg, 1024))
    m, t, th = hemstat(c, g)
    line = "  %-12s trough %.3f (%+.3f vs C2)  thirds %.3f %.3f %.3f" % (tag, t, t - ref_t, *th)
    for s, refg in ((32, REF32), (16, REF16)):
        gg = rgbgray(render(svg, s))[1]
        keep = ~rim(s)
        ea, eb = (sobel(gg) > 0.10) & keep, (sobel(refg) > 0.10) & keep
        pr = (ea & dilate(eb)).sum() / max(ea.sum(), 1)
        rc = (eb & dilate(ea)).sum() / max(eb.sum(), 1)
        line += " | %dpx FP %2d FN %2d f1 %.4f" % (s, (ea & ~dilate(eb)).sum(),
                                                   (eb & ~dilate(ea)).sum(),
                                                   2 * pr * rc / max(pr + rc, 1e-9))
    print(line + " | 1024 mean|d| vs current %.4f" % np.abs(g - BASEG).mean())
    return m


keep = {"baseline": report("baseline", "icon.svg")}
print("\nflat hem, stroke 18, sweeping opacity:")
for op in (0.30, 0.45, 0.60):
    tag = "hem%02d" % (op * 100)
    keep[tag] = report(tag, build(tag, hem('#332A1E" stroke-opacity="%.2f' % op, 18.0)))
print("\nwidth at the opacity nearest C2, and the ramped variant:")
keep["hem45w26"] = report("hem45w26", build("hem45w26", hem('#332A1E" stroke-opacity="0.45', 26.0)))
keep["hemramp"] = report("hemramp", build("hemramp", hem("url(#seatRamp)", 18.0)))
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)

print("\nprofiles out from the back edge (C2 last)")
names = list(keep)
print("   u  " + "".join("%10s" % n for n in names) + "        C2")
refm = hemstat(REFC, REFG)[0]
for u in list(range(0, 12)) + [12, 14, 16, 20, 24]:
    print("  %3d " % u + "".join("%10.3f" % keep[n][u] for n in names) + "  %8.3f" % refm[u])
