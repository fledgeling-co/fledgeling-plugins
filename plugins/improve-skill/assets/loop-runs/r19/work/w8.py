"""The contact layer's WIDTH, swept against C2's own profile.

w7, off the hone landmark in both images (C2's axis 39.0 deg, ours 33.4), says the two
shadows now agree on total (deficit integral 23.8 against 23.2) and on the far field, and
disagree in one place: 16-48px out. Ours climbs 0.604 -> 0.760 between u=16 and u=32 and
then SHELVES at 0.767 through u=36, where C2 climbs 0.611 -> 0.688 and keeps climbing with
no inflection anywhere. Peak +0.072 of far field too bright at u=32, and 0.043 too dark at
u=0-8. A tight core, a shelf, then a tail: that is the signature of two Gaussians whose
peaks are 30px apart, and at 32px the shelf's leading slope is a false edge - the three
cast-attributed FP cells (10,25) (11,25) (12,24), which CAST_OP=0 clears.

The physical reading is that CONTACT_BLUR = 9 asserts a contact this block does not have.
It rides as a WEDGE: RISE_NEAR 48 local units at the leading edge to RISE_FAR 132 at the
trailing one, so along most of its length the occluder stands tens of px OFF the ground,
and a penumbra's half-width grows with that gap. A sigma of 9 is the shadow of a body
lying flat. So sweep the width, fit the profile, and report what each point does to the
32px edge set as a consequence rather than as a target.
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
BANDS = ((0, 8), (8, 16), (16, 32), (32, 64), (64, 96), (96, 128), (128, 192))


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


def profile(c, g, reach=260, dark=0.45):
    warm = (c[..., 0] - c[..., 2] > 0.30) & (c[..., 0] - c[..., 1] > 0.15)
    ys, xs = np.nonzero(warm)
    x0, y0 = xs.mean(), ys.mean()
    X = np.stack([xs - x0, ys - y0])
    w, v = np.linalg.eigh(X @ X.T / len(xs))
    ax, ay = v[:, np.argmax(w)]
    if ax < 0:
        ax, ay = -ax, -ay
    dx, dy = -ay, ax
    if dy < 0:
        dx, dy = -dx, -dy
    D = g < dark
    rows = []
    for k in range(-22, 23):
        sx, sy = x0 + ax * k * 9.0, y0 + ay * k * 9.0
        bx, by = sx - dx * 40.0, sy - dy * 40.0
        if not (0 <= int(bx) < 1024 and 0 <= int(by) < 1024) or not D[int(by), int(bx)]:
            continue
        t = 0.0
        while t < 300 and D[int(min(1023, max(0, by + dy * t))), int(min(1023, max(0, bx + dx * t)))]:
            t += 1.0
        row = [bil(g, bx + dx * (t + u), by + dy * (t + u)) for u in range(reach)]
        if not any(v != v for v in row):
            rows.append(row)
    m = np.median(np.array(rows), axis=0)
    return m / np.median(m[200:260])


def sobel(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


def build(name, subs):
    src = SRC
    for pat, rep in subs:
        src, n = re.subn(pat, rep, src, count=1)
        assert n == 1, (name, pat)
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
ref_p = profile(REFC, REFG)
REF32 = rgbgray(REFIM.resize((32, 32), Image.LANCZOS))[1]
REF16 = rgbgray(REFIM.resize((16, 16), Image.LANCZOS))[1]


def edgestats(svg, s, refg):
    g = rgbgray(render(svg, s))[1]
    keep = ~rim_mask(s)
    ea = (sobel(g) > 0.10) & keep
    eb = (sobel(refg) > 0.10) & keep
    prec = (ea & dilate(eb)).sum() / max(ea.sum(), 1)
    rec = (eb & dilate(ea)).sum() / max(eb.sum(), 1)
    return (int((ea & ~dilate(eb)).sum()), int((eb & ~dilate(ea)).sum()),
            2 * prec * rec / max(prec + rec, 1e-9))


def report(tag, svg):
    c, g = rgbgray(render(svg, 1024))
    p = profile(c, g)
    r = np.abs(p[:128] - ref_p[:128]).mean()
    integ = sum((1 - p[a:b].mean()) * (b - a) for a, b in BANDS)
    fp32, fn32, f32 = edgestats(svg, 32, REF32)
    fp16, fn16, f16 = edgestats(svg, 16, REF16)
    print("  %-14s |resid|0-128 %.4f  worst %+.3f @u%3d  integral %.1f | 32px FP %2d FN %2d f1 %.4f | 16px FP %d FN %d f1 %.4f"
          % (tag, r, max(p[:128] - ref_p[:128], key=abs), int(np.argmax(np.abs(p[:128] - ref_p[:128]))),
             integ, fp32, fn32, f32, fp16, fn16, f16))
    return r, p


print("C2 profile bands: " + " ".join("%.3f" % ref_p[a:b].mean() for a, b in BANDS))
print("\nCONTACT_BLUR sweep (opacity held at 0.42 unless noted):")
report("baseline b9", "icon.svg")
keep = {}
for bl in (14.0, 18.0, 24.0, 30.0, 38.0):
    tag = "cb%02d" % bl
    svg = build(tag, [(r"CONTACT_BLUR = 9\.0", "CONTACT_BLUR = %.1f" % bl)])
    keep[tag] = report(tag, svg)[1]
print("\nwith the deficit put back (wider blur spills part of its integral under the block):")
for bl, op in ((24.0, 0.50), (30.0, 0.52), (30.0, 0.58), (38.0, 0.60)):
    tag = "cb%02d_o%02d" % (bl, op * 100)
    svg = build(tag, [(r"CONTACT_BLUR = 9\.0", "CONTACT_BLUR = %.1f" % bl),
                      (r"CONTACT_OP = 0\.42", "CONTACT_OP = %.2f" % op)])
    keep[tag] = report(tag, svg)[1]
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)

print("\nprofiles, u = 0..64 (C2 last)")
names = list(keep)
print("   u    " + "".join("%9s" % n for n in names) + "       C2")
for u in range(0, 68, 4):
    print("  %3d  " % u + "".join("%9.3f" % keep[n][u] for n in names) + "  %7.3f" % ref_p[u])
