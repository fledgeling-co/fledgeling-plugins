#!/usr/bin/env python3
from pathlib import Path
import numpy as np
from PIL import Image

DIR = Path(__file__).resolve().parent
SAMPLE_FRACS = (0.01, 0.08, 0.25, 0.50, 0.75, 0.92, 0.99)


def lum(rgb):
    return rgb.astype(np.float64).mean(axis=-1)


def load(name):
    return np.array(Image.open(DIR / name).convert("RGB"))


def bars_from_lum(L):
    h, w = L.shape
    # columns that are darker than surrounding
    col = L.mean(axis=0)
    # find three troughs in the middle band
    y0, y1 = int(h * 0.15), int(h * 0.72)
    band = L[y0:y1].mean(axis=0)
    dark = band < np.percentile(band, 35)
    runs = []
    i = 0
    while i < w:
        if not dark[i]:
            i += 1
            continue
        j = i
        while j < w and dark[j]:
            j += 1
        if j - i >= 20:
            runs.append((i, j))
        i = j
    # keep three widest in center
    runs = sorted(runs, key=lambda t: -(t[1] - t[0]))[:6]
    runs = sorted(runs, key=lambda t: t[0])
    # merge nearby
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] < 8:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    # take three closest to center
    cx = w / 2
    merged = sorted(merged, key=lambda t: abs((t[0] + t[1]) / 2 - cx))[:3]
    merged = sorted(merged, key=lambda t: t[0])
    out = []
    for x0, x1 in merged:
        patch = L[:, x0:x1]
        rm = patch.mean(axis=1)
        ys = np.where(rm < np.percentile(rm, 45))[0]
        yy0, yy1 = (int(ys[0]), int(ys[-1]) + 1) if len(ys) else (y0, y1)
        out.append((x0, x1, yy0, yy1))
    return out


def sample_across(rgb, bar, y=None):
    x0, x1, y0, y1 = bar
    if y is None:
        y = y0 + int(0.40 * (y1 - y0))
    y = min(max(y, y0), y1 - 1)
    bw = x1 - x0
    vals = []
    for f in SAMPLE_FRACS:
        x = x0 + int(round(f * (bw - 1)))
        vals.append(float(rgb[y, x].mean()))
    return y, vals


print("SIZES")
for n in ["REF-1024.png", "A-1024.png", "B-1024.png", "A-small.png", "B-small.png"]:
    im = Image.open(DIR / n)
    print(n, im.size, im.mode)

for n in ["REF-1024.png", "A-1024.png", "B-1024.png"]:
    rgb = load(n)
    L = lum(rgb)
    print(f"\n==== {n} {rgb.shape} lum mean={L.mean():.1f} min={L.min():.1f} ====")
    bs = bars_from_lum(L)
    print("bars (x0,x1,y0,y1)", bs)
    if not bs:
        continue
    tb = max(bs, key=lambda b: b[3] - b[2])
    for label, yfix in [("40pct", None), ("y420", 420 if rgb.shape[0] >= 421 else None)]:
        if yfix is not None and not (tb[2] <= yfix < tb[3]):
            print(f"  skip {label}")
            continue
        y, vals = sample_across(rgb, tb, yfix)
        spread = max(vals) - min(vals)
        edge = (vals[0] + vals[1] + vals[-2] + vals[-1]) / 4
        core = (vals[2] + vals[3] + vals[4]) / 3
        print(f"  {label} y={y} tallest={tb}")
        print("   fracs", list(SAMPLE_FRACS))
        print("   lum  ", [round(v, 1) for v in vals])
        print(f"   spread={spread:.1f} edge={edge:.1f} core={core:.1f} {'EDGE_BRIGHT' if edge>core+1 else 'EDGE_DARK' if edge<core-1 else 'FLAT'}")

    # orange row
    r, g, b = [rgb[..., i].astype(np.float64) for i in range(3)]
    orange = (r > 140) & (r > g + 20) & (r > b + 30)
    if orange.any():
        ys = np.where(orange.any(axis=1))[0]
        oy = int(ys.mean())
        xs = np.where(orange[oy])[0]
        x0, x1 = int(xs.min()), int(xs.max())
        print(f"  orange y={oy} x={x0}-{x1} n={int(orange.sum())}")
        ovals = []
        for f in np.linspace(0, 1, 11):
            x = x0 + int(f * (x1 - x0))
            px = rgb[oy, x]
            ovals.append((int(px[0]), int(px[1]), int(px[2]), float(px.mean())))
        print("  orange samples RGB+lum", ovals)
        print("  orange center lum", ovals[5][3], "ends", ovals[0][3], ovals[-1][3])

    print("  near_black lum<50", int((L < 50).sum()), "lum<80", int((L < 80).sum()))
    print("  p5,p10,p50,p90", [round(float(np.percentile(L, p)), 1) for p in (5, 10, 50, 90)])

# MAE
ref = load("REF-1024.png")
A = load("A-1024.png")
B = load("B-1024.png")
if A.shape != ref.shape:
    A = np.array(Image.open(DIR / "A-1024.png").convert("RGB").resize((ref.shape[1], ref.shape[0]), Image.Resampling.LANCZOS))
if B.shape != ref.shape:
    B = np.array(Image.open(DIR / "B-1024.png").convert("RGB").resize((ref.shape[1], ref.shape[0]), Image.Resampling.LANCZOS))
print("\nMAE A", np.abs(A.astype(float) - ref).mean())
print("MAE B", np.abs(B.astype(float) - ref).mean())
Lr = lum(ref)
mask = Lr < 140
print("MAE A dark", np.abs(A.astype(float) - ref)[mask].mean(), "n", int(mask.sum()))
print("MAE B dark", np.abs(B.astype(float) - ref)[mask].mean())

print("\nSMALL")
for n in ["A-small.png", "B-small.png"]:
    rgb = load(n)
    print(n, rgb.shape)
    tile = rgb[:, :128]
    L = lum(tile)
    nw = L < 248
    v = L[nw]
    print("  128 contrast p90-p10", float(np.percentile(v, 90) - np.percentile(v, 10)))
    print("  128 p10", float(np.percentile(v, 10)), "p50", float(np.percentile(v, 50)), "min", float(v.min()))
    # middle tile ~32px mag, right tile 16px mag. strip is 128*3+32 wide typically
    w = rgb.shape[1]
    # guess three 128 tiles with 16 gaps: 128, 144, 128, 144, 128
    t1 = rgb[:, 144:272] if w >= 272 else rgb[:, w // 3 : 2 * w // 3]
    t2 = rgb[:, 288:416] if w >= 416 else rgb[:, 2 * w // 3 :]
    for label, t in [("32mag", t1), ("16mag", t2)]:
        Lt = lum(t)
        print(f"  {label} mean={Lt.mean():.1f} min={Lt.min():.1f} std={Lt.std():.1f}")
