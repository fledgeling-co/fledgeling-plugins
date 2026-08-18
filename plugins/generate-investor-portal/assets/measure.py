#!/usr/bin/env python3
"""Measure what the eye cannot: 16px contrast against the family, and how much
of the tile the accent actually owns.

`contrast` is the metric the family audit used — the standard deviation of
sRGB-encoded luminance over a 16x16 downsample of the 256px render, composited
on white. It reproduces the audit's published 0.049 for the icon this one
replaces, so the numbers are comparable rather than merely similar.

`accent` reports the share of tile pixels whose hue sits in the ember band at
real saturation, which is the house rule the eye argues about: one warm accent,
reserved for the focal, never spread.

    python3 measure.py icon.svg
"""
import colorsys
import glob
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]


def render(src: Path, size: int) -> Image.Image:
    if src.suffix != ".svg":
        return Image.open(src).convert("RGBA").resize((size, size), Image.LANCZOS)
    tmp = Path(tempfile.mkdtemp()) / f"r{size}.png"
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(src), "-o", str(tmp)],
                   check=True)
    return Image.open(tmp).convert("RGBA")


def lum_srgb(im: Image.Image) -> np.ndarray:
    a = np.asarray(im).astype(np.float64) / 255.0
    alpha = a[..., 3:4]
    rgb = a[..., :3] * alpha + 1.0 * (1 - alpha)          # composite on white
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def contrast16(src: Path) -> float:
    return float(lum_srgb(render(src, 256).resize((16, 16), Image.LANCZOS)).std())


def accent_share(src: Path) -> tuple[float, float]:
    im = render(src, 512)
    a = np.asarray(im).astype(np.float64) / 255.0
    alpha = a[..., 3]
    inside = alpha > 0.5
    rgb = a[..., :3]
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    # hue, in degrees, for the ember/amber band
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = np.maximum(mx - mn, 1e-6)
    h = np.select(
        [mx == r, mx == g, mx == b],
        [((g - b) / d) % 6, ((b - r) / d) + 2, ((r - g) / d) + 4],
    ) * 60.0
    warm = inside & (s > 0.34) & (v > 0.30) & (((h >= 5) & (h <= 46)))
    hot = warm & (s > 0.52) & (v > 0.55)
    n = inside.sum()
    return 100.0 * warm.sum() / n, 100.0 * hot.sum() / n


def main():
    src = Path(sys.argv[1]).resolve()
    fam = []
    for p in sorted(glob.glob(str(REPO / "plugins" / "*" / "assets" / "icon-256.png"))):
        name = os.path.basename(os.path.dirname(os.path.dirname(p)))
        fam.append((contrast16(Path(p)), name))
    fam.sort()
    vals = np.array([v for v, _ in fam])
    c = contrast16(src)
    rank = int((vals < c).sum()) + 1
    warm, hot = accent_share(src)
    print(f"16px luminance contrast (sd of sRGB luma over a 16x16 render)")
    print(f"  candidate {src.name:24s} {c:.4f}")
    print(f"  family    n={len(vals)}  median {np.median(vals):.4f}  "
          f"min {vals.min():.4f}  max {vals.max():.4f}")
    print(f"  rank      {rank} of {len(vals) + 1} (1 = lowest contrast)")
    print(f"\naccent share of the tile (512px render)")
    print(f"  warm pixels (S>0.34, V>0.30, hue 5-46)   {warm:5.2f}%")
    print(f"  saturated core (S>0.52, V>0.55)          {hot:5.2f}%")
    print(f"\nfamily, lowest first:")
    for v, n in fam:
        print(f"  {v:.4f}  {n}")


if __name__ == "__main__":
    main()
