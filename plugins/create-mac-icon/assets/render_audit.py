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
# 96 and 128 are the Finder-list and marketplace-tile sizes, and audit_sheet.py
# check requires a source at each. This tuple predated them, so running this
# script left every take short of two sources and failed the gate.
SIZES = (1024, 256, 128, 96, 64, 32)
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# takes: id -> (source, kind)
TAKES = {
    "a": ("icon.svg", "svg"),
    "b": ("icon-engineB-arrow-626f04.svg", "svg-letterbox"),
    "c1": ("icon-engineC-27539d-masked.png", "png"),
    "c2": ("icon-engineC-fe8278-2-masked.png", "png"),
}


def alpha_mask(size):
    """The set's superellipse as an alpha channel."""
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
    """Full-bleed raster -> squircle-masked 1024. Never a rounded-rect approximation."""
    im = Image.open(src).convert("RGBA").resize((1024, 1024), Image.LANCZOS)
    im.putalpha(alpha_mask(1024))
    im.save(dst)
    return dst


def render(take, src, kind):
    p = ASSETS / src
    for s in SIZES:
        dst = OUT / f"{take}-{s}.png"
        if kind == "svg":
            subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(p), "-o", str(dst)],
                           check=True)
        elif kind == "svg-letterbox":
            # a take that isn't square artwork gets shown honestly: fitted, not stretched
            tmp = OUT / f"_{take}.png"
            subprocess.run(["rsvg-convert", "-w", str(s), str(p), "-o", str(tmp)], check=True)
            im = Image.open(tmp).convert("RGBA")
            canvas = Image.new("RGBA", (s, s), (247, 243, 237, 255))
            canvas.alpha_composite(im, (0, (s - im.height) // 2))
            canvas.putalpha(alpha_mask(s))
            canvas.save(dst)
            tmp.unlink()
        else:
            Image.open(p).convert("RGBA").resize((s, s), Image.LANCZOS).save(dst)


if __name__ == "__main__":
    for raw, out in (("icon-engineC-27539d.png", "icon-engineC-27539d-masked.png"),
                     ("icon-engineC-fe8278-2.png", "icon-engineC-fe8278-2-masked.png")):
        mask_raster(ASSETS / raw, ASSETS / out)
        print(f"masked {out}")
    for take, (src, kind) in TAKES.items():
        render(take, src, kind)
        print(f"rendered {take} at {SIZES}")
