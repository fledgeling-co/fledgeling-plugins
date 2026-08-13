#!/usr/bin/env python3
"""Exports and measurements for the proctor icon.

    python3 render_audit.py

Renders `icon.svg` to the shipped PNG sizes with the system squircle applied
(the marketplace tiles are decorative PNGs, not Icon Composer input, so the
mask has to be in the file), squircle-masks the raster takes for the audit
sheet, and prints the figure-ground numbers the sheet quotes so they are
measured off the shipped render rather than remembered.
"""
from __future__ import annotations

import pathlib
import subprocess

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
SKILL = pathlib.Path.home() / (".claude/plugins/cache/fledgeling-plugins/"
                               "create-mac-icon/1.3.0/skills/create-mac-icon")
SQUIRCLE = (SKILL / "assets/squircle-path.txt").read_text().strip()
EXPORTS = [("icon.png", 1024), ("icon-256.png", 256), ("icon-128.png", 128)]
RASTERS = ["icon-engineC-6269c5.png", "icon-engineC-72c971-2.png"]


def mask(size: int) -> Image.Image:
    svg = HERE / "_mask.svg"
    png = HERE / "_mask.png"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
                   f'viewBox="0 0 1024 1024"><path d="{SQUIRCLE}" fill="#fff"/></svg>')
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                    str(svg), "-o", str(png)], check=True)
    a = Image.open(png).convert("RGBA").split()[3]
    svg.unlink(missing_ok=True)
    png.unlink(missing_ok=True)
    return a


def lum(p):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(p[0]) + 0.7152 * f(p[1]) + 0.0722 * f(p[2])


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def main():
    full = HERE / "_full.png"
    subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024",
                    str(HERE / "icon.svg"), "-o", str(full)], check=True)
    base = Image.open(full).convert("RGBA")

    for name, size in EXPORTS:
        im = base.resize((size, size), Image.LANCZOS)
        im.putalpha(mask(size))
        im.save(HERE / name)
        print(f"  {name}  {size}x{size}")

    for r in RASTERS:
        src = HERE / r
        if not src.exists():
            continue
        im = Image.open(src).convert("RGBA").resize((1024, 1024), Image.LANCZOS)
        im.putalpha(mask(1024))
        out = src.with_name(src.stem + "-masked.png")
        im.save(out)
        print(f"  {out.name}")

    rgb = base.convert("RGB")

    def darkest(x0, y0, x1, y1):
        return min((rgb.getpixel((x, y)) for x in range(x0, x1, 3)
                    for y in range(y0, y1, 3)), key=lum)

    def most_orange(x0, y0, x1, y1):
        # the pixel with the strongest warm chroma — R high, B low
        return max((rgb.getpixel((x, y)) for x in range(x0, x1, 3)
                    for y in range(y0, y1, 3)), key=lambda p: p[0] - p[2])

    ground_l = rgb.getpixel((110, 500))
    ground_r = rgb.getpixel((930, 780))
    keyline = darkest(165, 300, 320, 640)      # the tree's slate left edge
    rows = darkest(420, 470, 720, 610)         # the content rows / their samples
    delta = most_orange(770, 560, 890, 780)    # the delta run, bottom-right overhang
    print("\nfigure-ground, measured on the shipped 1024 render")
    print(f"  tree keyline vs tile   {ratio(keyline, ground_l):.2f}:1")
    print(f"  content rows vs tile   {ratio(rows, ground_l):.2f}:1")
    print(f"  delta run vs tile      {ratio(delta, ground_r):.2f}:1")
    grey = rgb.convert("L").resize((32, 32), Image.LANCZOS)
    px = list(grey.getdata())
    print(f"  32px luminance spread  {(max(px) - min(px)) / 255:.3f}")
    full.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
