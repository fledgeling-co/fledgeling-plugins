"""How far above the board it lies on does the shaving's lit face go - measured in both.

w13 walked four lines across the roll's upper-left rim: ours steps +0.18 L in 4px and then
holds 0.90-0.93 across 25-50px of band, while the reference over the same ground stays inside
a 0.02-0.06 range and never passes ~0.78. A shaving is the same wood as the board under it,
so a lit outer face 0.18 above that board is a specular highlight the material cannot make.

This puts a number on it that does not depend on the roll being registered: take the curl's
own footprint (from the SHAVING=0 twin), and the ground annulus just outside it, and ask each
image how far its bright end inside the footprint sits above the median of that annulus.
Then sweep OUT_LIT toward the measured relationship and replay the whole score.
"""
import subprocess
import tempfile
import pathlib
import re
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r18/work")
SRC = pathlib.Path("build_icon.py").read_text()
REF = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")
SIZES = [1024, 256, 128, 32, 16]


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def native(svg, size):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, size))
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(svg), "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def grow(m, px, step=5):
    out = m.copy()
    for _ in range(px // step):
        out = dilate(out, step)
    return out


def build(name, subs, env=None):
    src = SRC
    for pat, rep in subs:
        src, n = re.subn(pat, rep, src, count=1)
        assert n == 1, (name, pat)
    src = src.replace("ASSETS = pathlib.Path(__file__).resolve().parent",
                      "ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent")
    p = WORK / ("gen_%s.py" % name)
    p.write_text(src)
    subprocess.run(["python3", str(p)], check=True, capture_output=True, cwd=".", env=env)
    out = WORK / ("var_%s.svg" % name)
    out.write_bytes(pathlib.Path("icon.svg").read_bytes())
    return out


# ---- the relationship, measured
import os
env = dict(os.environ, SHAVING="0")
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True, env=env)
off = WORK / "var_noshaving.svg"
off.write_bytes(pathlib.Path("icon.svg").read_bytes())
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)

g_on = gray(native("icon.svg", 1024))
g_off = gray(native(str(off), 1024))
g_ref = gray(REF.resize((1024, 1024), Image.LANCZOS))
M = np.abs(g_on - g_off) > 0.02                      # the curl's own footprint
ring = grow(M, 40) & ~grow(M, 10)                    # board just outside it
print("curl footprint %d px, annulus %d px" % (M.sum(), ring.sum()))
for nm, g in (("ours", g_on), ("reference", g_ref)):
    base = np.median(g[ring])
    print("  %-10s annulus median %.4f | inside: p50 %.4f  p90 %.4f  p99 %.4f  max %.4f"
          % (nm, base, np.percentile(g[M], 50), np.percentile(g[M], 90),
             np.percentile(g[M], 99), g[M].max()))
    print("  %-10s lit face above its own board:  p90 %+.4f   p99 %+.4f"
          % ("", np.percentile(g[M], 90) - base, np.percentile(g[M], 99) - base))

# ---- and the sweep
REFS = {s: REF.resize((s, s), Image.LANCZOS) for s in SIZES}


def box_mean(x, w):
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[: x.shape[0], : x.shape[1]]


def ssim(a, b):
    w = max(3, min(11, a.shape[0] // 4) | 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    ma, mb = box_mean(a, w), box_mean(b, w)
    va, vb = box_mean(a * a, w) - ma ** 2, box_mean(b * b, w) - mb ** 2
    cov = box_mean(a * b, w) - ma * mb
    return float(np.clip(((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2)), -1, 1).mean())


def sob(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


def score(svg):
    out = {}
    for s in SIZES:
        ca, cb = native(svg, s), REFS[s]
        gc, gr = gray(ca), gray(cb)
        keep = ~rim_mask(s)
        ea, eb = (sob(gc) > 0.10) & keep, (sob(gr) > 0.10) & keep
        prec = (ea & dilate(eb)).sum() / max(ea.sum(), 1)
        rec = (eb & dilate(ea)).sum() / max(eb.sum(), 1)
        f1 = float(2 * prec * rec / max(prec + rec, 1e-9))
        aa, ab = np.asarray(ca)[..., 3] > 16, np.asarray(cb)[..., 3] > 16
        iou = None if (ab.mean() > 0.99 and aa.mean() > 0.99) else float((aa & ab).sum() / max((aa | ab).sum(), 1))
        ld, sm = float(np.abs(gc - gr).mean()), ssim(gc, gr)
        sc = float(np.percentile(gc, 90) - np.percentile(gc, 10))
        lum = 1 - min(ld * 4, 1.0)
        comp = (0.40 * sm + 0.35 * lum + 0.25 * f1) if s >= 128 else (0.35 * f1 + 0.25 * iou + 0.25 * sm + 0.15 * lum)
        out[s] = dict(composite=round(comp, 4), edge_f1=f1, ssim=sm, lum=ld, sc=sc,
                      fp=int((ea & ~dilate(eb)).sum()))
    return out


def row(tag, sc):
    print("  %-12s " % tag + " ".join("%d:%.4f" % (s, sc[s]["composite"]) for s in SIZES)
          + "   f1_32 %.4f  FP %2d  ssim32 %.4f  sc32 %.4f  ssim1024 %.4f lum1024 %.4f"
          % (sc[32]["edge_f1"], sc[32]["fp"], sc[32]["ssim"], sc[32]["sc"], sc[1024]["ssim"], sc[1024]["lum"]))


print("\ncomposites by size:")
row("baseline", score("icon.svg"))
# OUT_LIT scaled toward the board; TRANSMIT and CURL_BORE untouched, because an earlier
# round measured the bore against C2 and got it right - this is the outer face only.
for tag, trip in (("lit_x0.94", (228, 220, 203)),
                  ("lit_x0.88", (214, 206, 190)),
                  ("lit_x0.82", (199, 192, 177)),
                  ("lit_x0.76", (185, 178, 164))):
    row(tag, score(build(tag, [(r"OUT_LIT   = \(243, 234, 216\)",
                                "OUT_LIT   = (%d, %d, %d)" % trip)])))

subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)
