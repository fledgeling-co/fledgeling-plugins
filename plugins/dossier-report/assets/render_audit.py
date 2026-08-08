#!/usr/bin/env python3
"""Render every take at the audit sheet's 2x retina sources, and mask the raster
takes with the marketplace's exact superellipse.

The sheet shows 128 / 32 / 16 css px, so the sources are 256 / 64 / 32 - a 1x
source reads blurred on every retina screen, which is the one thing an icon
audit must not do to itself.

    python3 render_audit.py
"""
import pathlib
import subprocess

from PIL import Image

ASSETS = pathlib.Path(__file__).resolve().parent
OUT = ASSETS / "audit-renders"
OUT.mkdir(exist_ok=True)
SIZES = (1024, 256, 64, 32)
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# takes: id -> (source, kind)
TAKES = {
    "a": ("icon.svg", "svg"),
    "a07": ("fidelity-runs/candidate-r07.svg", "svg"),
    "a0": ("fidelity-runs/candidate-r00.svg", "svg"),
    "b": ("icon-engineB-arrow-ecc20a.svg", "svg"),
    "c1": ("icon-engineC-c57a8c-masked.png", "png"),
    "c2": ("icon-engineC2-597699-masked.png", "png"),
}

RASTERS = (("icon-engineC-c57a8c.png", "icon-engineC-c57a8c-masked.png"),
           ("icon-engineC2-597699.png", "icon-engineC2-597699-masked.png"))


def alpha_mask(size):
    """The set's superellipse as an alpha channel. Never a rounded-rect approximation."""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
           f'viewBox="0 0 1024 1024"><path d="{SQUIRCLE}" fill="#fff"/></svg>')
    tmp = OUT / "_mask.svg"
    tmp.write_text(svg)
    png = OUT / "_mask.png"
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(tmp), "-o", str(png)],
                   check=True)
    m = Image.open(png).convert("RGBA").split()[3]
    tmp.unlink()
    png.unlink()
    return m


def mask_raster(src: pathlib.Path, dst: pathlib.Path):
    im = Image.open(src).convert("RGBA").resize((1024, 1024), Image.LANCZOS)
    im.putalpha(alpha_mask(1024))
    im.save(dst)
    return dst


def render(take, src, kind):
    p = ASSETS / src
    if not p.exists():
        print(f"  skip {take}: {src} not on disk")
        return
    for s in SIZES:
        dst = OUT / f"{take}-{s}.png"
        if kind == "svg":
            subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(p), "-o", str(dst)],
                           check=True)
        else:
            Image.open(p).convert("RGBA").resize((s, s), Image.LANCZOS).save(dst)


if __name__ == "__main__":
    for raw, out in RASTERS:
        mask_raster(ASSETS / raw, ASSETS / out)
        print(f"masked {out}")
    for take, (src, kind) in TAKES.items():
        render(take, src, kind)
        print(f"rendered {take} at {SIZES}")
