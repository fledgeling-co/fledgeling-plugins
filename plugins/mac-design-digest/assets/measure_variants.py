#!/usr/bin/env python3
"""Measure the mac-design-digest takes, and render the variant and silhouette
reads that `audit_sheet.py` does not produce.

Every number quoted in `audit.html` comes out of here, and every image it shows
outside `audit-renders/` is written here, so a reviewer can reproduce the sheet
rather than take its word.

    python3 measure_variants.py          # writes variant-renders/, prints the table

What it produces, and why each one is on the sheet:

  variants-<take>-grayscale.png   The shipped tile with hue removed and luminance
                                  preserved. This is the honest capture behind
                                  rubric #10: the system Tinted appearance maps an
                                  icon onto one hue keeping luminance, so whatever
                                  survives grayscale survives Tinted, and whatever
                                  separates only by hue does not.
  variants-<take>-tinted.png      The same luminance ramped onto one hue, as the
                                  Tinted appearance actually renders it.
  variants-<take>-clear-*.png     The `bg` layer switched off and the object
                                  composited on a dark and on a light desktop —
                                  the Clear appearance, where the system supplies
                                  the ground. Only the two layered SVG takes can
                                  be read this way; a flat raster has no bg layer
                                  to remove, which IS the 76% failure mode.
  sil-<take>.png                  Rubric #3. For the SVG takes, every fill and
                                  stroke forced to black with the ground off —
                                  the exact silhouette test. For the rasters
                                  there is no layer to isolate, so the figure is
                                  segmented by luminance at the midpoint between
                                  slab and ground, and the noise in the result is
                                  itself the finding.

Requires Pillow, numpy and rsvg-convert.
"""

from __future__ import annotations

import pathlib
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw  # noqa: F401  (ImageDraw kept for ad-hoc montages)

HERE = pathlib.Path(__file__).resolve().parent
RENDERS = HERE / "audit-renders"
OUT = HERE / "variant-renders"

TAKES = ("master", "A2", "C1", "C2")
SVG_TAKES = {"master": "icon-src.svg", "A2": "icon-A2-inlaid.svg"}

# Sample boxes in 256-space. The slab box sits in the plate's lower-left quadrant,
# clear of every mark and of the socket in all four takes; the ground box sits in
# the tile's left margin, outside every slab. Same boxes for every take, so the
# figure-ground numbers are comparable rather than each hand-placed.
SLAB_BOX = (62, 150, 110, 185)
GROUND_BOX = (10, 120, 28, 140)

TINT = np.array([0.36, 0.52, 0.86])   # the Tinted appearance's hue
DESKTOPS = {"clear-dark": (26, 26, 28), "clear-light": (238, 238, 240)}

# The family metric: 16px luminance standard deviation, measured on the 32px
# render downsampled to 16 and composited over white. Median across the
# marketplace is 0.176 (recorded on proctor's sheet).
FAMILY_MEDIAN_16PX_STD = 0.176


def lum(rgb: np.ndarray) -> np.ndarray:
    x = rgb / 255.0
    x = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]


def encode(l: np.ndarray) -> np.ndarray:
    l = np.clip(l, 0, 1)
    return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055) * 255


def wcag(a: float, b: float) -> float:
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def hex_lum(h: str) -> float:
    h = h.lstrip("#")
    return float(lum(np.array([[[int(h[i:i + 2], 16) for i in (0, 2, 4)]]], dtype=float))[0, 0])


def flatten(png: pathlib.Path) -> np.ndarray:
    """The render composited over white, which is how the sheet displays it."""
    a = np.asarray(Image.open(png).convert("RGBA")).astype(float)
    al = a[..., 3:4] / 255.0
    return a[..., :3] * al + 255.0 * (1 - al)


def blacken(svg_text: str) -> str:
    t = svg_text.replace('<g id="bg">', '<g id="bg" display="none">')
    t = re.sub(r'filter="url\(#[^)]*\)"', "", t)
    t = re.sub(r'fill="(?!none)[^"]*"', 'fill="#000"', t)
    t = re.sub(r'stroke="(?!none)[^"]*"', 'stroke="#000"', t)
    t = re.sub(r'(fill|stroke)-opacity="[^"]*"', r'\1-opacity="1"', t)
    return t


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for stale in list(OUT.glob("variants-*")) + list(OUT.glob("sil-*")):
        stale.unlink()

    print("== rubric #7, from the build scripts' named colour constants ==")
    pairs = [
        ("A  plate #F7F4ED vs ground #E7E4DC", "#F7F4ED", "#E7E4DC"),
        ("A  figure bar #4E5560 vs plate #F7F4ED", "#4E5560", "#F7F4ED"),
        ("A  seal #E8542A vs plate #F7F4ED", "#E8542A", "#F7F4ED"),
        ("A2 glaze #3A4048 vs ground #E7E4DC", "#3A4048", "#E7E4DC"),
        ("A2 inlay #F3EFE6 vs glaze #3A4048", "#F3EFE6", "#3A4048"),
        ("A2 footnote inlay #DCD6C9 vs glaze #3A4048", "#DCD6C9", "#3A4048"),
        ("A2 seal #E8542A vs glaze #3A4048", "#E8542A", "#3A4048"),
        ("A2 seal #E8542A vs porcelain collar #F3EFE6", "#E8542A", "#F3EFE6"),
    ]
    for label, a, b in pairs:
        print(f"  {label:46s} {wcag(hex_lum(a), hex_lum(b)):5.2f}:1")

    print("\n== rubric #7, measured on the 1024 renders ==")
    sx0, sy0, sx1, sy1 = (v * 4 for v in SLAB_BOX)
    gx0, gy0, gx1, gy1 = (v * 4 for v in GROUND_BOX)
    for take in TAKES:
        l = lum(flatten(RENDERS / f"{take}-1024.png"))
        sl = float(np.median(l[sy0:sy1, sx0:sx1]))
        gl = float(np.median(l[gy0:gy1, gx0:gx1]))
        print(f"  {take:7s} slab L={sl:.4f}  ground L={gl:.4f}  ->  {wcag(sl, gl):5.2f}:1")

    print("\n== rubric #4, the family metric: 16px luminance std "
          f"(marketplace median {FAMILY_MEDIAN_16PX_STD}) ==")
    for take in TAKES:
        im = Image.open(RENDERS / f"{take}-32.png").resize((16, 16), Image.LANCZOS)
        a = np.asarray(im.convert("RGBA")).astype(float)
        al = a[..., 3:4] / 255.0
        s = float(lum(a[..., :3] * al + 255.0 * (1 - al)).std())
        print(f"  {take:7s} {s:.3f}  ({s / FAMILY_MEDIAN_16PX_STD:.2f}x median)")

    print("\n== rubric #10, captured: grayscale and Tinted on the shipped tile ==")
    sx0, sy0, sx1, sy1 = SLAB_BOX
    gx0, gy0, gx1, gy1 = GROUND_BOX
    for take in TAKES:
        rgb = flatten(RENDERS / f"{take}-256.png")
        l = lum(rgb)
        Image.fromarray(np.repeat(encode(l)[..., None], 3, axis=2).astype("uint8")).save(
            OUT / f"variants-{take}-grayscale.png")
        tinted = encode(l)[..., None] * TINT[None, None, :] / TINT.max()
        Image.fromarray(np.clip(tinted, 0, 255).astype("uint8")).save(
            OUT / f"variants-{take}-tinted.png")
        sl = float(np.median(l[sy0:sy1, sx0:sx1]))
        gl = float(np.median(l[gy0:gy1, gx0:gx1]))
        print(f"  {take:7s} grayscale slab L={sl:.4f}  ground L={gl:.4f}  ->  {wcag(sl, gl):5.2f}:1")

    print("\n== rubric #10, Clear: bg layer off, object on a desktop (SVG takes only) ==")
    for take, src in SVG_TAKES.items():
        tmp = OUT / f"_{take}.svg"
        tmp.write_text((HERE / src).read_text().replace('<g id="bg">',
                                                        '<g id="bg" display="none">'))
        png = OUT / f"_{take}.png"
        subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", str(tmp), "-o", str(png)],
                       check=True)
        fg = np.asarray(Image.open(png).convert("RGBA")).astype(float)
        al = fg[..., 3:4] / 255.0
        for name, (r, g, b) in DESKTOPS.items():
            field = np.zeros_like(fg[..., :3])
            field[..., 0], field[..., 1], field[..., 2] = r, g, b
            comp = fg[..., :3] * al + field * (1 - al)
            Image.fromarray(comp.astype("uint8")).save(OUT / f"variants-{take}-{name}.png")
            l = lum(comp)
            sl = float(np.median(l[sy0:sy1, sx0:sx1]))
            fl = float(lum(np.array([[[r, g, b]]], dtype=float))[0, 0])
            print(f"  {take:7s} {name:11s} plate L={sl:.4f}  desktop L={fl:.4f}  ->  "
                  f"{wcag(sl, fl):5.2f}:1")
        tmp.unlink()
        png.unlink()

    print("\n== rubric #3, the silhouette test ==")
    for take, src in SVG_TAKES.items():
        tmp = OUT / f"_sil-{take}.svg"
        tmp.write_text(blacken((HERE / src).read_text()))
        png = OUT / f"_sil-{take}.png"
        subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", str(tmp), "-o", str(png)],
                       check=True)
        Image.fromarray(flatten(png).astype("uint8")).save(OUT / f"sil-{take}.png")
        tmp.unlink()
        png.unlink()
        print(f"  {take:7s} authored shapes filled black, ground off")
    for take in ("C1", "C2"):
        l = lum(flatten(RENDERS / f"{take}-256.png"))
        thr = (float(np.median(l[sy0:sy1, sx0:sx1])) + float(np.median(l[gy0:gy1, gx0:gx1]))) / 2
        m = l > thr
        Image.fromarray((255 - m.astype("uint8") * 255)).save(OUT / f"sil-{take}.png")
        print(f"  {take:7s} segmented at L={thr:.4f}; figure fraction {m.mean():.3f} "
              f"— a raster has no layer to isolate, so this is a threshold, not a test")


if __name__ == "__main__":
    main()
