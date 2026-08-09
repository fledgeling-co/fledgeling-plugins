#!/usr/bin/env python3
"""Round 7 sweeps B and C -- the hole's width and the ember's protrusion.

Two contact sheets, both rendered from the one `band()` generator so no
variant can quietly acquire a second code path.

  B  GAP_HALF 30..34, i.e. 10 to 14 degrees clear each side of a 40-degree
     ember. The floor is hard: the ember keeps clearance on BOTH sides, since
     abutting the used arc makes it read as continuous with what is occupied.
  C  PROTRUDE_FRAC 0.05..0.13 of the band width. C's wedge stands proud by
     about 6%.

Each sheet also reports, per variant: the rendered inner and outer radius of
the graphite arc and of the ember (so the inner boundary can be checked for
continuity rather than asserted), the minimum rendered gap in pixels between
ember and arc, figure-ground, and 32/16px self-contrast.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parents[2]
sys.path.insert(0, str(ASSETS))
import build_icon as B  # noqa: E402

SHEET = HERE / "sweep"


def render(tag, w=1024):
    svg = SHEET / f"{tag}.svg"
    png = SHEET / f"{tag}-{w}.png"
    svg.write_text(B.build())
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(w),
                    str(svg), "-o", str(png)], check=True)
    return png


def geometry(png):
    """Rendered radii, read off the pixels rather than off the constants.

    The object is anything materially darker or materially warmer than the
    porcelain. The warm threshold has to be strict: the ember's spill onto the
    ground clears R > B + 40 easily, and a detector that counts the spill
    reports the ember's inner boundary about 23px inside the arc's -- a
    measurement artifact that looks exactly like the inner-edge fault this
    file exists to prevent. R > B + 90 keeps the body and drops the spill.
    """
    I = np.asarray(Image.open(png).convert("RGB"), dtype=float)
    L = (0.2126 * I[..., 0] + 0.7152 * I[..., 1] + 0.0722 * I[..., 2]) / 255
    warm = (I[..., 0] > I[..., 2] + 90) & (L < 0.72)
    obj = (L < 0.66) | warm
    out = {}
    for label, angles in (("arc", (100, 140, 180, 220, 250)),
                          ("ember", (-65, -55, -45))):
        ins, outs = [], []
        for a in angles:
            th = np.radians(a)
            rs = np.arange(120, 470, 0.5)
            xs = (512 + rs * np.cos(th)).astype(int)
            ys = (512 + rs * np.sin(th)).astype(int)
            hit = obj[ys, xs]
            if not hit.any():
                continue
            idx = np.flatnonzero(hit)
            ins.append(rs[idx[0]])
            outs.append(rs[idx[-1]])
        out[label] = (min(ins), max(ins), min(outs), max(outs))
    return out


def clearance(png):
    """Smallest angular gap, in degrees, between ember pixels and arc pixels
    on each side of the hole -- measured on the render."""
    I = np.asarray(Image.open(png).convert("RGB"), dtype=float)
    warm = (I[..., 0] > 140) & (I[..., 0] > I[..., 1] + 60) & \
           (I[..., 0] > I[..., 2] + 60)
    L = (0.2126 * I[..., 0] + 0.7152 * I[..., 1] + 0.0722 * I[..., 2]) / 255
    dark = (L < 0.55) & ~warm
    res = []
    for lo, hi in ((-100.0, -55.0), (-55.0, -10.0)):
        found = None
        for a in np.arange(lo, hi, 0.25):
            th = np.radians(a)
            rs = np.arange(170, 420, 1.0)
            xs = (512 + rs * np.cos(th)).astype(int)
            ys = (512 + rs * np.sin(th)).astype(int)
            if not warm[ys, xs].any() and not dark[ys, xs].any():
                found = a if found is None else found
            elif found is not None and (warm[ys, xs].any() or
                                        dark[ys, xs].any()):
                res.append((found, a - 0.25))
                found = None
    return res


def contrast(tag, size):
    png = render(tag, size)
    I = np.asarray(Image.open(png).convert("RGB"), dtype=float)
    L = (0.2126 * I[..., 0] + 0.7152 * I[..., 1] + 0.0722 * I[..., 2]) / 255
    return float(np.percentile(L, 90) - np.percentile(L, 10))


def figure_ground(png):
    I = np.asarray(Image.open(png).convert("RGB"), dtype=float)
    L = (0.2126 * I[..., 0] + 0.7152 * I[..., 1] + 0.0722 * I[..., 2]) / 255
    ys, xs = np.mgrid[0:1024, 0:1024]
    rr = np.hypot(xs - 512, ys - 512)
    ring = (rr > 150) & (rr < 400) & (I[..., 2] > I[..., 0] + 8)
    gl = L[rr > 430].mean()
    return (gl + 0.05) / (np.percentile(L[ring], 50) + 0.05)


def sheet(name, variants, cols=5):
    ims = [Image.open(SHEET / f"{t}-1024.png").resize((256, 256),
                                                      Image.LANCZOS)
           for t in variants]
    small = [Image.open(SHEET / f"{t}-32.png").resize((256, 256),
                                                      Image.NEAREST)
             for t in variants]
    rows = 2
    out = Image.new("RGB", (256 * len(variants), 256 * rows), "white")
    for i, (a, b) in enumerate(zip(ims, small)):
        out.paste(a, (256 * i, 0))
        out.paste(b, (256 * i, 256))
    out.save(SHEET / f"{name}.png")
    print(f"  sheet -> {SHEET / name}.png")


def main():
    SHEET.mkdir(exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "gap"

    if which == "gap":
        B.PROTRUDE_FRAC = 0.09
        tags = []
        for gh in (30.0, 31.0, 32.0, 33.0, 34.0, 40.0):
            B.GAP_HALF = gh
            tag = f"gap{gh:.0f}"
            png = render(tag)
            render(tag, 32)
            g = geometry(png)
            print(f"  GAP_HALF={gh:.0f}  clear={gh - 20:.0f}deg/side  "
                  f"arc r_in {g['arc'][0]:.0f}-{g['arc'][1]:.0f} "
                  f"r_out {g['arc'][2]:.0f}-{g['arc'][3]:.0f} | "
                  f"ember r_in {g['ember'][0]:.0f}-{g['ember'][1]:.0f} "
                  f"r_out {g['ember'][2]:.0f}-{g['ember'][3]:.0f} | "
                  f"fg {figure_ground(png):.2f} | "
                  f"holes {[(round(a), round(b)) for a, b in clearance(png)]}")
            tags.append(tag)
        sheet("sheet-gap", tags)

    else:
        B.GAP_HALF = float(sys.argv[2]) if len(sys.argv) > 2 else 32.0
        tags = []
        for pf in (0.0, 0.05, 0.07, 0.09, 0.11, 0.13):
            B.PROTRUDE_FRAC = pf
            tag = f"pro{pf * 100:.0f}"
            png = render(tag)
            render(tag, 32)
            render(tag, 16)
            g = geometry(png)
            print(f"  PROTRUDE={pf * 100:.0f}%  ({pf * B.W:.1f}px)  "
                  f"arc r_in {g['arc'][0]:.0f}-{g['arc'][1]:.0f} "
                  f"r_out {g['arc'][2]:.0f}-{g['arc'][3]:.0f} | "
                  f"ember r_in {g['ember'][0]:.0f}-{g['ember'][1]:.0f} "
                  f"r_out {g['ember'][2]:.0f}-{g['ember'][3]:.0f} | "
                  f"fg {figure_ground(png):.2f} | "
                  f"sc32 {contrast(tag, 32):.3f} sc16 {contrast(tag, 16):.3f}")
            tags.append(tag)
        sheet("sheet-protrude", tags)


if __name__ == "__main__":
    main()
