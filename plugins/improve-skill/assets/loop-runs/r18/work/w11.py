"""The cast shadow's penumbra: sweep its width and read the whole score, not just the FPs.

w10 attributed 3 of the 20 32px false positives to the cast layer: our |grad| there is
0.120/0.184/0.120 where the reference's is 0.016/0.021/0.011 - the reference's shadow makes
no 32px edge anywhere on the tile. r17 measured the reference's cast reaching ~150px from
contact and half-recovering by 64px against our 26px blur, so the physical fault and the
metric fault are the same fault: a penumbra too tight for its own darkness has a slope peak,
and at 32px a slope peak IS an edge.

This rebuilds the icon at several (CAST_BLUR, CAST_OP) points and replays fidelity.py's own
composite at all five sizes, so the round is authored against the measured curve rather than
against one estimate. Nothing here is committed; build_icon.py is restored at the end.
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
    va = box_mean(a * a, w) - ma ** 2
    vb = box_mean(b * b, w) - mb ** 2
    cov = box_mean(a * b, w) - ma * mb
    s = ((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2))
    return float(np.clip(s, -1, 1).mean())


def sobel(g, thresh=0.10):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    m = np.hypot(gx, gy)
    return m > thresh * 4, m / 4.0


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


def native(svg, size):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, size))
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(svg), "-o", str(t)], check=True)
    return Image.open(t).convert("RGBA")


REFS = {s: REF.resize((s, s), Image.LANCZOS) for s in SIZES}


def score(svg):
    out = {}
    for s in SIZES:
        ca = native(svg, s)
        cb = REFS[s]
        gc, gr = gray(ca), gray(cb)
        ea, ma_ = sobel(gc)
        eb, mb_ = sobel(gr)
        keep = ~rim_mask(s)
        ea, eb = ea & keep, eb & keep
        tp_p = (ea & dilate(eb)).sum()
        tp_r = (eb & dilate(ea)).sum()
        prec = tp_p / max(ea.sum(), 1)
        rec = tp_r / max(eb.sum(), 1)
        f1 = float(2 * prec * rec / max(prec + rec, 1e-9))
        aa = np.asarray(ca)[..., 3] > 16
        ab = np.asarray(cb)[..., 3] > 16
        iou = None if (ab.mean() > 0.99 and aa.mean() > 0.99) else float((aa & ab).sum() / max((aa | ab).sum(), 1))
        ld = float(np.abs(gc - gr).mean())
        sm = ssim(gc, gr)
        sc = float(np.percentile(gc, 90) - np.percentile(gc, 10))
        lum = 1 - min(ld * 4, 1.0)
        if s >= 128:
            comp = 0.40 * sm + 0.35 * lum + 0.25 * f1
        else:
            comp = 0.35 * f1 + 0.25 * iou + 0.25 * sm + 0.15 * lum
        out[s] = dict(lum_delta=ld, ssim=sm, edge_f1=f1, mask_iou=iou, self_contrast=sc,
                      composite=round(comp, 4), fp=int((ea & ~dilate(eb)).sum()),
                      fn=int((eb & ~dilate(ea)).sum()))
    return out


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
    return out


def row(tag, sc):
    print("  %-14s " % tag + "  ".join("%d:%.4f" % (s, sc[s]["composite"]) for s in SIZES)
          + "   f1 32 %.4f/16 %.4f  FP %2d  sc32 %.4f  lum1024 %.4f"
          % (sc[32]["edge_f1"], sc[16]["edge_f1"], sc[32]["fp"], sc[32]["self_contrast"], sc[1024]["lum_delta"]))


base = score("icon.svg")
print("composites by size:")
row("baseline", base)

CAND = [
    ("b40", [(r"CAST_BLUR = 26\.0", "CAST_BLUR = 40.0")]),
    ("b52", [(r"CAST_BLUR = 26\.0", "CAST_BLUR = 52.0")]),
    ("b64", [(r"CAST_BLUR = 26\.0", "CAST_BLUR = 64.0")]),
    ("b80", [(r"CAST_BLUR = 26\.0", "CAST_BLUR = 80.0")]),
    ("b64op42", [(r"CAST_BLUR = 26\.0", "CAST_BLUR = 64.0"), (r"CAST_OP = 0\.35", "CAST_OP = 0.42")]),
    ("b80op46", [(r"CAST_BLUR = 26\.0", "CAST_BLUR = 80.0"), (r"CAST_OP = 0\.35", "CAST_OP = 0.46")]),
]
for name, subs in CAND:
    row(name, score(build(name, subs)))

subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)
